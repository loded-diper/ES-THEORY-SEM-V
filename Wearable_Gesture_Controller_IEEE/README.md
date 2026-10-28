# Wearable Gesture Controller — IEEE theoretical mini-project report

ICT 3132 Embedded Systems, V Semester B.Tech. (IT), MIT Manipal.

**Authors:** Arya Choudhary (240911438), Sanika Singh (240911664), and Vishad Sharma (240911680).

This is a theoretical report based on the supplied project synopsis. It does not report completed hardware, data collection, training, inference conversion, or experimental measurements. The later user instruction supplies Vishad Sharma's registration number, superseding the different number in the synopsis. The report narrows the synopsis's implementation ambitions to the requested theoretical scope.

## Open in Overleaf

1. Choose **New Project → Upload Project** in Overleaf.
2. Upload `Wearable_Gesture_Controller_Overleaf.zip`.
3. Use `main.tex` as the main document and **pdfLaTeX** as the compiler.
4. Recompile. The bibliography uses BibTeX and the included `IEEEtran.bst`.

No online Overleaf project has been created or modified. The ZIP is the upload-ready deliverable.

## Files

- `main.tex`: complete report, using `\documentclass[conference]{IEEEtran}`.
- `references.bib`: five research-paper references with DOI or stable paper links.
- `figures/architecture.tex`: editable TikZ system architecture.
- `figures/workflow.tex`: editable TikZ recognition and model-comparison workflow.
- `IEEEtran.cls`: unmodified official IEEEtran class, version 1.8b.
- `IEEEtran.bst`: unmodified IEEEtran bibliography style, version 1.14.
- `Wearable_Gesture_Controller_Report.pdf`: compiled report.
- `build.sh`: repeatable local PDF build.
- `SOURCE_NOTES.md`: source provenance, citation checks, and analytical assumptions.

The diagrams are vector graphics compiled directly from TikZ. There are no external image downloads, custom fonts, shell-escape requirements, or absolute paths in the LaTeX sources. Standard IEEE conference typography, columns, and margins are retained.

## Build locally

Requires a TeX installation with pdfLaTeX, BibTeX, TikZ/PGF, `booktabs`, `balance`, and the other standard packages listed in `main.tex`.

```sh
bash build.sh
```

Temporary compilation files are written to `.build/`; the final PDF is copied to `Wearable_Gesture_Controller_Report.pdf`. Overleaf performs the equivalent LaTeX/BibTeX passes automatically.

## Scope and interpretation

- One baseline: a 32-unit LSTM.
- One lightweight alternative: a 24-unit GRU.
- One primary, conditional optimization: 8-bit post-training quantization of the GRU.
- Pruning is discussed briefly as future work, not a further experiment.
- No deployment board is selected. Runtime support, available memory, and peripherals determine feasibility.
- Sampling settings, model sizes, parameter counts, operation counts, and buffer sizes are explicitly illustrative design assumptions or analytical calculations.
- Accuracy, F1, latency, power, and other empirical outcomes remain unevaluated. No fabricated benchmark table is included.

IEEE formatting does not imply IEEE publication, peer review, or endorsement. This package is a college mini-project submission draft.
