# Feedback comparison: broader overlap and artifact audit

Date: 2026-10-09. This updates, rather than clears, the verifier-guidance candidate.

## Broader literature correction

[Is Self-Repair a Silver Bullet for Code Generation?](https://arxiv.org/html/2306.09896v5), introduction and evaluation outline, explicitly compares repair against independent sampling under equivalent budgets and considers feedback quality. [Try Again, Don't Look Back](https://arxiv.org/html/2607.26117v1) is a further matched-budget/placebo-control lead; its full experimental details still require extraction. Consequently, resource matching is established methodology, not our novelty. RAISE's omitted control supports a targeted replication but cannot alone justify an original-method paper.

Further primary leads requiring full-text comparison:
- [CloudFix](https://arxiv.org/abs/2512.09957): LLM cloud access-policy repair.
- [Does Fixing Break Security?](https://arxiv.org/abs/2608.13404): security regression during iterative infrastructure repair.
- [RegoMender conference listing](https://conf.researchr.org/track/ase-2026/ase-2026-not-in-person-presentations): policy repair; a listing is not sufficient evidence of detailed method coverage.

The possible question of interacting authorization constraints must be compared against these, not presumed novel. Record transitions from passing to failing constraints after each repair, not just final pass rate. A proposed directional-feedback experiment must distinguish information content, prompt length, extra sampling, and task difficulty. No experiments have begun.

## Pinned release inspection

Repository: https://github.com/Aizhouym/raise
Commit: `206962d130d2c69d5e15f8103fa0953345cc7690`.

Read the recursive Git tree, `data/README.md`, and `pyproject.toml` through the GitHub API. No LICENSE, COPYING or NOTICE filename was returned by the tree filter. Package metadata did not declare a license; data README did not specify reuse terms. The corpus archive's internal contents and notices have not been inspected. This is unresolved permission status, not a finding that no rights exist anywhere.

Data README confirms a scenario archive containing manifest, schema, requirement, gold policy, verification plan and references. It expressly excludes weights, checkpoints, generated samples, logs and evaluation results. No corpus downloaded or code executed. Reproducing training is materially different from replaying released results.

## Current disposition

Keep the resource-matched study as a replication candidate. Do not advertise a new estimator, new policy-differencing method, or established empirical discovery. Continue full-text review of policy repair and regression before committing to a costly study. Public availability does not automatically establish redistribution permission. A fresh, independently authored test suite could remove upstream-data dependency, but would support an independent extension, not an exact reproduction.
