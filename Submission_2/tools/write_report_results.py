"""Write report macros from the recorded experiment, never handwritten benchmarks."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
m = json.loads((root/'demo/artifacts/metrics.json').read_text())
values = {
    'TestWindows': str(m['split_windows']['test']),
    'TestAccuracy': f"{100*m['accuracy']:.1f}\\%",
    'MacroFone': f"{m['macro_f1']:.3f}",
    'MacroPrecision': f"{m['macro_precision']:.3f}",
    'MacroRecall': f"{m['macro_recall']:.3f}",
    'AcceptedWindows': str(m['accepted_command_windows']),
    'BackgroundCommands': str(m['synthetic_background_command_windows']),
    'MedianLatency': f"{m['host_inference_median_ms']:.3f}",
    'PninetyfiveLatency': f"{m['host_inference_p95_ms']:.3f}",
    'WeightBytes': str(m['parameter_payload_bytes']),
    'CheckpointBytes': str(m['checkpoint_bytes']),
}
out = '% Generated from demo/artifacts/metrics.json. Synthetic data and host timing only.\n'
out += ''.join('\\newcommand{\\'+key+'}{'+value+'}\n' for key,value in values.items())
(root/'report/results.tex').write_text(out)
print('Updated report/results.tex from saved metrics.')
