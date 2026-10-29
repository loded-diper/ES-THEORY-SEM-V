# Submission 2 requirements and status

## Assignment source

Read before preparing the new package:

- Uploaded project synopsis, `ICT_3132_ES_Synopsis_Wearable_Gesture_Controller.docx`.
- Existing six-page `Wearable_Gesture_Controller_Report.pdf` in the historical report folder.
- The faculty requirements reproduced in the user's task message.

No separate faculty-guidelines attachment was present in the workspace. No claim is made that an unseen document was reviewed. This checklist implements the supplied requirements; any additional original faculty instructions should be checked before submission.

## Requirement coverage

| Requirement | Status / evidence |
| --- | --- |
| Correct team details | New package uses Vishad Sharma, **240911580**. |
| IEEE conference format, maximum six pages | `report/report.tex` uses unmodified IEEEtran conference class; compiled PDF is checked during verification. |
| Introduction and problem statement | Report Section I. |
| Literature survey | Section II; ten distinct papers published in 2020–2022. |
| At least ten verified Scopus-indexed papers | **Outstanding. Zero independently verified Scopus records.** Primary author records support the shortlist, but indexing and publisher cross-checks were blocked by network policy. See `literature/verification.csv`. |
| Explicit research gap and objectives | Section III; application-specific engineering integration gap, not an unsupported novelty claim. |
| Proposed methodology and block diagram | Section IV and editable TikZ architecture figure. |
| Pseudocode | Section V and numbered pseudocode box. |
| Results, if any | Section VI reports only executed synthetic-data metrics and host CPU measurements. |
| References and evidence | `report/references.bib`, `literature/SOURCES.md`, and local author-record evidence copies. |
| Working software | `demo/demo.py`, saved checkpoint, generated recording manifest, actual stdout, and JSON metrics. |
| Proper split separation | Independent recordings and seeds assigned to splits before windowing; training-only normalization. |
| Rejection / no-command outcome | Background class and fixed confidence threshold; unit checks cover both. |
| PowerPoint demonstration | Eight-slide `presentation.pptx`, including native editable architecture and actual saved software output. |
| Run and reproduction instructions | `README.md`. |
| Similarity report | **Separate institutional action required. Not generated.** Use the institution's approved process; no similarity percentage is asserted. |

## Evidence boundaries

Implemented: synthetic six-axis generator, causal filtering, fixed windows, trained compact GRU, confidence rejection, symbolic output, saved results, and automated pipeline checks.

Analytical or future only: LSTM comparison, 8-bit quantization, pruning, MCU sampling and inference, continuous-controller cooldown, BLE/Wi-Fi receiver, physical actuation, real-user generalization, MCU resource measurements, power, and battery life.

No online Overleaf project or similarity report has been created. This package should not be described as fully satisfying the indexing requirement until institutional verification is completed.
