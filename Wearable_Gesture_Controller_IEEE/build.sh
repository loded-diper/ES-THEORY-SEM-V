#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
mkdir -p .build
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=.build main.tex
(cd .build && BIBINPUTS=..: BSTINPUTS=..: bibtex main)
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=.build main.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=.build main.tex
cp .build/main.pdf Wearable_Gesture_Controller_Report.pdf
