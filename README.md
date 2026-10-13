# Evidence-age interfaces for remediation approval

**Status: Broad repair-generalization candidate rejected after full-text overlap review; narrower preservation question unverified.** See [October 13 literature gate](protocol/literature-gate-2026-10-13.md). The human-study proposal remains on hold. An original finite-domain policy-repair audit and ten passing tests are available. Hand-authored fixtures demonstrate measurement only, not AI performance or a new discovery. See [results and research decision](protocol/repair-feasibility-result-2026-10-09.md). Run `python -m unittest discover -s tests -v` and `python src/repair_audit.py`.

[Research protocol and prior-art leads](protocol/research-plan.md). This plan comes from the October 4, 2026 independent research portfolio. Its literature assessment must be refreshed before implementation and submission.

## Research identity and publication route

Author: **Ezekiel Ologunde**. Affiliation: **Independent Researcher**, with no institutional affiliation. Email: ologunde@bu.edu; no corresponding-author designation requested. Intended route: a suitable ACM journal, selected after assessing the completed contribution. No journal has accepted this work and no publisher metadata or DOI is assigned.

## Repository workflow

Keep research questions and hypotheses in `protocol/`; put code in `src/`, tests in `tests/`, and analyses in `analysis/`. Store redistributable datasets with provenance in `data/`, including source URL, retrieval date, version, license, SHA-256, schema, and role in the study. For restricted or large data, publish an acquisition script and manifest instead of copying files. Never commit credentials, private participant records, or copyrighted downloaded papers.

Freeze each experimental plan and code revision before collection. Retain failed and excluded runs with reasons. Publish analysis and result artifacts as work progresses. Keep manuscript drafts in `paper/`, clearly versioned; deposit the author-permitted final paper after journal-policy review. A planned experiment is not a result, and public code is not peer-reviewed acceptance.

Original work is intentionally unlicensed pending an author decision. Preserve applicable third-party notices. No dataset or final paper is claimed to exist merely because its directory is present.

