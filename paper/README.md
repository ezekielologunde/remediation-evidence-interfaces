# Paper

`main.tex` is the complete four-page ACM-format clinical-family case study. It is a technical preprint candidate, with limitations stated in the manuscript, not an accepted journal article or a demonstrated new method.

The PDF, editable source and clean-build-verified Overleaf archive are in `../deliverables/`. Native receipts and release validation are in `../analysis/clinical-family/`. Run `python src/verify_clinical_release.py --source paper/main.tex --receipt analysis/clinical-family/receipt.json` from the repository root to verify the data-to-manuscript checks.

Compiler: Tectonic 0.17.0 with acmart 1.83. The built-in compiler failed during environment setup. All four pages were visually reviewed; the archive rebuild matched extracted PDF text exactly. No journal or ResearchGate submission was made for this paper.
