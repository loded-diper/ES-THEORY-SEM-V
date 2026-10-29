"""Six-channel SYNTHETIC pipeline demonstration; not real-user recognition evidence."""
from __future__ import annotations

import argparse
import copy
import json
import platform
import time
from pathlib import Path

import numpy as np
import torch
from torch import nn

SEED = 42
FS, WINDOW, STRIDE, LENGTH, HIDDEN = 50, 64, 32, 192, 16
LABELS = ["background", "swipe_left", "swipe_right", "wave"]
COMMANDS = ["NO_COMMAND", "LIGHT_OFF", "LIGHT_ON", "FAN_TOGGLE"]
COUNTS = {"train": 24, "validation": 8, "test": 10}  # recordings per class
THRESHOLD = 0.80  # declared before evaluation, not tuned on test data
HERE = Path(__file__).resolve().parent


def generate_recording(label: int, seed: int) -> np.ndarray:
    """Stylized signals, not a physics simulation or a human-motion dataset.

    Channels are ax, ay, az (nominal m/s^2), gx, gy, gz (nominal rad/s).
    Class-dependent formulas deliberately make a learnable toy problem.
    Random gain, phase, drift and noise vary independently by recording.
    """
    rng = np.random.default_rng(seed)
    t = np.arange(LENGTH) / FS
    f, phase, gain = rng.uniform(.7, 1.2), rng.uniform(0, 2*np.pi), rng.uniform(.7, 1.3)
    x = rng.normal(0, [.06, .06, .06, .03, .03, .03], (LENGTH, 6))
    x[:, 2] += 9.81
    x += rng.normal(0, .025, 6) + .025*np.sin(t[:, None] + np.arange(6))
    if label in (1, 2):
        sign = -1 if label == 1 else 1
        pulse = .35 + .65 * np.sin(np.pi*f*t + phase)**2
        x[:, 0] += sign*.8*gain*np.sin(2*np.pi*f*t + 2*phase)
        x[:, 1] += .12*gain*np.cos(2*np.pi*f*t + phase)
        x[:, 5] += sign*gain*pulse
    elif label == 3:
        wave = gain*np.sin(2*np.pi*f*t + phase)
        x[:, 1] += .9*wave
        x[:, 3] += 1.2*wave
        x[:, 4] += .5*gain*np.cos(2*np.pi*f*t + phase)
    return x.astype(np.float32)


def preprocess(x: np.ndarray) -> np.ndarray:
    """Causal first-order low-pass filter, independently reset per recording."""
    x = np.asarray(x, dtype=np.float32)
    if x.ndim != 2 or x.shape[1] != 6 or not np.isfinite(x).all():
        raise ValueError("Expected finite samples with shape (time, 6)")
    if len(x) < WINDOW:
        raise ValueError(f"Need at least {WINDOW} samples")
    y = np.empty_like(x)
    y[0] = x[0]
    for i in range(1, len(x)):
        y[i] = .35*x[i] + .65*y[i-1]
    return y


def window(x: np.ndarray) -> np.ndarray:
    return np.stack([x[i:i+WINDOW] for i in range(0, len(x)-WINDOW+1, STRIDE)])


def make_data():
    """Assign independent recording IDs/seeds to splits BEFORE windowing."""
    streams, manifest = {}, []
    for split_index, (split, count) in enumerate(COUNTS.items()):
        streams[split] = []
        for label in range(len(LABELS)):
            for recording in range(count):
                seed = SEED*100000 + split_index*10000 + label*100 + recording
                recording_id = f"{split}-{label}-{recording:02d}"
                x = preprocess(generate_recording(label, seed))
                streams[split].append((x, label, recording_id))
                manifest.append(dict(split=split, label=LABELS[label],
                                     recording_id=recording_id, generator_seed=seed))
    unique_train = np.concatenate([x for x, _, _ in streams["train"]])
    mean = unique_train.mean(axis=0)
    std = np.maximum(unique_train.std(axis=0), 1e-6)
    data = {}
    for split, records in streams.items():
        xs, ys, ids = [], [], []
        for x, label, recording_id in records:
            w = window((x-mean)/std)
            xs.extend(w)
            ys.extend([label]*len(w))
            ids.extend([recording_id]*len(w))
        data[split] = (torch.from_numpy(np.stack(xs)), np.array(ys), ids)
    return data, mean, std, manifest


class GestureGRU(nn.Module):
    def __init__(self):
        super().__init__()
        self.gru = nn.GRU(6, HIDDEN, batch_first=True)
        self.head = nn.Linear(HIDDEN, len(LABELS))

    def forward(self, x):
        _, h = self.gru(x)  # new zero hidden state for each window
        return self.head(h[-1])


def decide(probabilities: np.ndarray, threshold: float = THRESHOLD):
    p = np.asarray(probabilities)
    if p.shape != (len(LABELS),) or not np.isfinite(p).all():
        raise ValueError("Expected four finite class probabilities")
    label = int(p.argmax())
    confidence = float(p[label])
    command = COMMANDS[label] if label != 0 and confidence >= threshold else "NO_COMMAND"
    return LABELS[label], confidence, command


def classification_metrics(y, pred):
    cm = np.zeros((len(LABELS), len(LABELS)), dtype=int)
    np.add.at(cm, (y, pred), 1)
    tp = np.diag(cm)
    precision = tp/np.maximum(cm.sum(0), 1)
    recall = tp/np.maximum(cm.sum(1), 1)
    f1 = 2*precision*recall/np.maximum(precision+recall, 1e-12)
    return dict(accuracy=float(tp.sum()/cm.sum()), macro_precision=float(precision.mean()),
                macro_recall=float(recall.mean()), macro_f1=float(f1.mean()),
                confusion_matrix=cm.tolist(), per_class=[dict(label=label,
                precision=float(precision[i]), recall=float(recall[i]), f1=float(f1[i]),
                support=int(cm[i].sum())) for i, label in enumerate(LABELS)])


def train(data, output, mean, std):
    model = GestureGRU()
    optimizer = torch.optim.Adam(model.parameters(), lr=.004)
    loss_fn = nn.CrossEntropyLoss()
    train_x, train_y, _ = data["train"]
    val_x, val_y, _ = data["validation"]
    train_y, val_y = torch.tensor(train_y), torch.tensor(val_y)
    best_loss, best_state, best_epoch = float("inf"), None, 0
    history = []
    start = time.perf_counter()
    for epoch in range(1, 31):
        model.train()
        order = torch.randperm(len(train_x))
        for indices in order.split(64):
            optimizer.zero_grad()
            loss = loss_fn(model(train_x[indices]), train_y[indices])
            loss.backward()
            optimizer.step()
        model.eval()
        with torch.inference_mode():
            val_loss = float(loss_fn(model(val_x), val_y))
        history.append(dict(epoch=epoch, validation_cross_entropy=val_loss))
        if val_loss < best_loss:
            best_loss, best_epoch = val_loss, epoch
            best_state = copy.deepcopy(model.state_dict())
    elapsed = time.perf_counter()-start
    model.load_state_dict(best_state)
    torch.save(dict(state_dict=best_state, mean=torch.tensor(mean), std=torch.tensor(std),
                    seed=SEED, labels=LABELS, hidden=HIDDEN), output/"model.pt")
    return model, dict(epochs=30, selected_epoch=best_epoch,
                       validation_cross_entropy=best_loss, training_seconds=elapsed,
                       history=history)


def run(output: Path, retrain: bool):
    torch.set_num_threads(1)
    torch.manual_seed(SEED)
    np.random.seed(SEED)
    torch.use_deterministic_algorithms(True)
    output.mkdir(parents=True, exist_ok=True)
    data, mean, std, manifest = make_data()
    if retrain or not (output/"model.pt").exists():
        model, training = train(data, output, mean, std)
    else:
        saved = torch.load(output/"model.pt", map_location="cpu", weights_only=True)
        if not np.allclose(mean, saved["mean"].numpy()) or not np.allclose(std, saved["std"].numpy()):
            raise ValueError("Checkpoint preprocessing mismatch; rerun with --train")
        model = GestureGRU()
        model.load_state_dict(saved["state_dict"])
        training = None
    model.eval()
    test_x, test_y, ids = data["test"]
    probe = test_x[:1]
    with torch.inference_mode():
        probs = model(test_x).softmax(1).numpy()
        for _ in range(10):
            model(probe)
        times = []
        for _ in range(100):
            start = time.perf_counter_ns()
            model(probe)
            times.append((time.perf_counter_ns()-start)/1e6)
    metrics = classification_metrics(test_y, probs.argmax(1))
    decisions = [decide(p) for p in probs]
    issued = np.array([c != "NO_COMMAND" for _, _, c in decisions])
    metrics.update(synthetic_only=True, real_world_accuracy="not evaluated",
                   seed=SEED, labels=LABELS, threshold=THRESHOLD,
                   sampling_hz=FS, window_samples=WINDOW, stride_samples=STRIDE,
                   split_recordings={k:COUNTS[k]*4 for k in COUNTS},
                   split_windows={k:len(v[1]) for k,v in data.items()},
                   model="one-layer PyTorch GRU(6,16), Linear(16,4), FP32",
                   parameter_count=sum(p.numel() for p in model.parameters()),
                   parameter_payload_bytes=sum(p.numel()*p.element_size() for p in model.parameters()),
                   checkpoint_bytes=(output/"model.pt").stat().st_size,
                   accepted_command_windows=int(issued.sum()),
                   accepted_command_precision=float((probs.argmax(1)[issued]==test_y[issued]).mean()) if issued.any() else None,
                   synthetic_background_command_windows=int((issued & (test_y==0)).sum()),
                   host_inference_median_ms=float(np.median(times)),
                   host_inference_p95_ms=float(np.percentile(times,95)),
                   timing_scope="CPU batch=1, one thread, model-only, 10 warmups, 100 timed runs; not MCU or end-to-end latency",
                   environment=dict(python=platform.python_version(), numpy=np.__version__,
                                    torch=torch.__version__, platform=platform.platform(),
                                    processor=platform.processor()),
                   mcu_latency="not measured", mcu_peak_ram="not measured", power="not measured")
    rows = ["SYNTHETIC DATA ONLY - pipeline check, not real-world recognition accuracy.",
            f"seed={SEED} | train/validation/test windows: {len(data['train'][1])}/{len(data['validation'][1])}/{len(test_y)}",
            f"GRU hidden={HIDDEN}, parameters={metrics['parameter_count']}, threshold={THRESHOLD:.2f}",
            "", "Synthetic held-out examples (first window of each class):",
            f"{'TRUE CLASS':<15} {'PREDICTED':<15} {'CONFIDENCE':>10}  COMMAND"]
    examples = []
    for k in range(4):
        i = int(np.flatnonzero(test_y==k)[0])
        label, confidence, command = decisions[i]
        rows.append(f"{LABELS[k]:<15} {label:<15} {confidence:10.3f}  {command}")
        examples.append(dict(true=LABELS[k], predicted=label, confidence=confidence,
                             command=command, recording_id=ids[i]))
    rows += ["", f"Synthetic test accuracy: {metrics['accuracy']:.4f}",
             f"Synthetic test macro-F1: {metrics['macro_f1']:.4f}",
             f"Host-only median / p95 inference: {metrics['host_inference_median_ms']:.3f} / {metrics['host_inference_p95_ms']:.3f} ms",
             "No MCU deployment, appliance integration, or power measurements."]
    text = "\n".join(rows)
    print(text)
    if training is not None:
        metrics["training"] = training
        metrics["examples"] = examples
        (output/"metrics.json").write_text(json.dumps(metrics, indent=2)+"\n")
        (output/"manifest.json").write_text(json.dumps(manifest, indent=2)+"\n")
        (output/"demo_output.txt").write_text(text+"\n")
        np.savez_compressed(output/"example_input.npz", samples=generate_recording(2, SEED),
                            channels=np.array(["ax","ay","az","gx","gy","gz"]))
    return metrics


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--train", action="store_true", help="retrain and replace recorded artifacts")
    parser.add_argument("--output", type=Path, default=HERE/"artifacts")
    args = parser.parse_args()
    run(args.output, args.train)
