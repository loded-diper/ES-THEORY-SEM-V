# ICT 3132 Embedded Systems — Submission 2

**Wearable Gesture Controller: An IMU-Based Edge Device for Gesture-Driven Smart Home Control**

V Semester B.Tech. IT, MIT Manipal.

| Team member | Registration number |
| --- | --- |
| Arya Choudhary | 240911438 |
| Sanika Singh | 240911664 |
| Vishad Sharma | **240911580** |

This package adds a working, hardware-free software demonstration to the earlier theoretical design. **All classification data are synthetic.** There is no real-user accuracy claim, selected MCU, physical appliance integration, or measured MCU performance.

## Deliverables

- [IEEE report PDF](report/report.pdf) — five pages, including references (within the six-page maximum).
- [LaTeX report](report/report.tex), [bibliography](report/references.bib), [TikZ sources](report/figures/), and generated result constants in `report/results.tex`.
- [PowerPoint presentation](presentation.pptx) — eight slides with editable architecture shapes, speaker notes, source links, and output from the actual demonstration.
- [Python demonstration](demo/demo.py), [tests](demo/test_demo.py), and [dependency list](demo/requirements.txt).
- [Recorded metrics](demo/artifacts/metrics.json), [stdout](demo/artifacts/demo_output.txt), [rendered stdout](demo/artifacts/demo_output.png), [recording split manifest](demo/artifacts/manifest.json), saved model `demo/artifacts/model.pt`, and a six-channel example input.
- [Literature sources](literature/SOURCES.md), [verification audit](literature/verification.csv), and local primary-source evidence.
- [Faculty requirement checklist](ASSIGNMENT_CHECKLIST.md), [verification summary](VERIFICATION.json), and the original synopsis in `source_documents/project_synopsis.docx`.

## Run the demonstration

Use Python **3.10–3.12** on an ordinary laptop. The recorded run used Python 3.12, NumPy 2.3.5, and PyTorch 2.5.1+cpu. No GPU, internet connection after dependency installation, external dataset, sensor, or other device is needed.

From the repository root:

```sh
cd Submission_2
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r demo/requirements.txt
python demo/demo.py
```

On Windows, activate the environment with `.venv\Scripts\activate` and use `python` in place of `python3`. To avoid installing GPU packages on Linux/Windows, install CPU-only PyTorch first, then the same requirements:

```sh
python -m pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cpu
python -m pip install -r demo/requirements.txt
```

The default command loads the small bundled checkpoint and prints held-out examples and live host-only timing. If the checkpoint is missing, it trains automatically. It does not overwrite the saved experimental snapshot unless `--train` is supplied. Live timing varies between runs and machines.

Reproduce training and replace the saved metrics, checkpoint, manifest, and output:

```sh
python demo/demo.py --train
```

To keep the submitted snapshot unchanged while testing a fresh run:

```sh
python demo/demo.py --train --output /tmp/gesture-reproduction
```

Example commands printed by the actual run:

```text
background   -> NO_COMMAND
swipe_left   -> LIGHT_OFF
swipe_right  -> LIGHT_ON
wave         -> FAN_TOGGLE
```

These are symbolic console outputs. No light, fan, wireless link, or appliance is controlled.

## What the code does

1. Assign independent generated recordings to training, validation, and test partitions before creating windows. Save all recording IDs and generator seeds.
2. Generate six channels: `ax, ay, az, gx, gy, gz`. Gravity is a nominal z-axis offset; synthetic pulse/oscillation formulas distinguish the toy classes. Recording frequency, phase, gain, drift, and noise vary. This is **not a validated physical simulator**.
3. Causally low-pass filter each recording; fit normalization on unique training samples only.
4. Create windows of 64 samples × 6 channels, with stride 32 and nominal sampling frequency 50 Hz.
5. Train `GRU(6,16) + Linear(16,4)` with Adam, learning rate 0.004, batch size 64, and 30 epochs. Select the lowest-validation-loss checkpoint.
6. Evaluate the held-out synthetic test partition. Output `NO_COMMAND` for background or a maximum class probability below the predeclared 0.80 threshold.

Seed: **42**. There are 24/8/10 recordings per class for training/validation/test, respectively. Each recording has 192 samples and creates five windows. The split contains 96/32/40 independent recordings and 480/160/200 windows. These are generator counts, not statistics about human participants.

## Recorded results and limits

| Metric | Recorded value |
| --- | --- |
| Synthetic held-out accuracy | 100.0% |
| Synthetic macro precision / recall / F1 | 1.000 / 1.000 / 1.000 |
| Test windows / recordings | 200 / 40 |
| Accepted command windows | 150 |
| Synthetic background command windows | 0 |
| Host median / p95 model-only latency | 0.668 / 0.949 ms |
| FP32 parameters / parameter payload | 1220 / 4880 bytes |
| Saved checkpoint size | 7720 bytes |

The confusion matrix has 50 correct examples per class. Classification precision, recall, and F1 are macro-averaged over all four classes before command rejection. The perfect score reflects simple, shared generating formulas in independently seeded recordings. It verifies this software pipeline, **not real-world gesture-recognition accuracy**. The saved JSON contains per-class support, the confusion matrix, model settings, training history, environment versions, and timing boundaries.

Host timing uses CPU, one thread, batch size one, ten warmups, and 100 timed model calls. It excludes acquisition, filtering, window filling, command mapping, and printing. MCU latency, on-device RAM/flash use, power, energy, and battery life are not measured. Parameter payload is not total memory usage. The LSTM comparison is analytical; no LSTM or quantized model was trained or evaluated.

The software emits independent window decisions. Debouncing, continuous event matching, false activations per hour, unknown-motion detection, accessibility studies, and real appliance control remain future work.

## Run checks

```sh
cd demo
python -m unittest -v test_demo.py
cd ..
```

Seven checks cover split separation, normalization provenance, filter causality, malformed inputs, rejection rules, a known confusion matrix, and tensor/window dimensions.

## Compile the report and use Overleaf

With pdfLaTeX, BibTeX, TikZ, and the standard packages named in `report/report.tex` installed:

```sh
bash report/build.sh
```

This regenerates `report/results.tex` from the saved actual metrics, performs LaTeX/BibTeX passes, and writes `report/report.pdf`. The unmodified IEEEtran class and bibliography style are included. No custom margins or smaller body font are used.

For Overleaf, upload `Submission_2_Overleaf.zip`, set the main document to `report.tex`, and select pdfLaTeX. The ZIP contains the frozen result constants, bibliography, figure sources, and template files. It needs no Python execution or absolute paths. **No online Overleaf project has been created.**

## Rebuild the slides

```sh
python -m pip install -r tools/requirements-docs.txt
python tools/build_presentation.py
```

The script uses `metrics.json` and the actual saved stdout rather than handwritten performance numbers. If you retrain and want updated documents, rebuild both the report and the slides. The deck includes presenter notes and primary-source links. Standard font substitution is possible on other operating systems.

## Submission documents and source records

The report has been revised as a formal academic paper with administrative notes removed. The project team has confirmed that the references have been checked. The source audit records that confirmation separately from the assistant's earlier network-limited attempts; those historical logs are retained for traceability.

Institutional documents such as a similarity report are managed separately from the paper and software package. No similarity percentage or external document is asserted by the build scripts.

The older `Wearable_Gesture_Controller_IEEE` folder is a historical theoretical draft and is superseded by this package. Current team details and scope are those in this README and the new report.
