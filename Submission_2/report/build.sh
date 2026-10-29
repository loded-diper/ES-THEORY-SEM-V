#!/usr/bin/env bash
set -euo pipefail
cd -- "$(dirname -- "${BASH_SOURCE[0]}")"
if [ -f ../tools/write_report_results.py ]; then
  python3 ../tools/write_report_results.py
fi
mkdir -p .build
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=.build report.tex
(cd .build && BIBINPUTS=..: BSTINPUTS=..: bibtex report)
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=.build report.tex
pdflatex -interaction=nonstopmode -halt-on-error -file-line-error -output-directory=.build report.tex
cp .build/report.pdf report.pdf
