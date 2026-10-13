# Auditor obligation coverage: exploratory follow-up

## Confirmed result

Pinned upstream commit: `0201565abf5993e258764d3f0ef83a59d3b4962e`. Cedar 4.13.0 experimental CLI and CVC5 1.4.2. All work was local.

For each scenario, construct a candidate from the union of its published floor policies. Independently validate that candidate and check every original floor, ceiling and action-liveness obligation. Then check four positive auditor obligations: qualified ClinicalResearcher and PrincipalInvestigator, each with View and Edit, across departments on an active project. In the consent scenario, Edit probes require consent. This was an exploratory follow-up selected after the original omission, not a preregistered or independent sample.

| Required cross-department auditor access | Base | Consent variant |
|---|---|---|
| ClinicalResearcher View | Covered | Omitted |
| ClinicalResearcher Edit | Omitted | Omitted |
| PrincipalInvestigator View | Omitted | Omitted |
| PrincipalInvestigator Edit | Omitted | Omitted |
| Original checks satisfied by candidate | 13/13 | 11/11 |

Covered means the probe implies the floor-union candidate. Omitted means the native solver produces a counterexample to that implication while the candidate still satisfies every original check. Three candidate-plus-probe qualifications matter: the candidate validates against the schema, satisfies all ceilings, and meets all liveness checks. Without those checks, floor-union survival alone would not establish that the candidate is accepted by the full plan.

The result supports two claims only: partial positive-obligation coverage in the base; and absence in the consent variant of an auditor View obligation found in the base. We have not proven the historical cause, measured published model errors, audited all requirements, or estimated prevalence. The interpretation of written requirements is ours, without independent human adjudication. The earlier explicit auditor-removal control confirms why intentional requirement changes must be treated differently.

## Reproduction and attribution

First run the acquisition/reproduction scripts `src/native_consent_audit.py` and `src/native_consent_controls.py`, then `python src/audit_auditor_slices.py`. The latter currently locates Windows executables under the repository's ignored `.local-tools/` directory. It does not automatically install dependencies. Input hashes are in the earlier native receipts. Commands, output and solver counterexamples are in `analysis/auditor-slices/receipt.json`.

The two floor-union `.cedar` candidates concatenate upstream reference policies; they are derived from the pinned CedarBench scenario references, without edits to those policy bodies. Their Apache-2.0 license and upstream NOTICE are retained as `UPSTREAM-LICENSE` and `UPSTREAM-NOTICE`. New probes and audit code are original work, unlicensed pending the author's decision. Cached upstream sources and binaries are excluded from Git.

## Literature decision

This is not a new mutation-testing algorithm. NIST SP 800-192 already covers specification coverage and mutation testing. Martin and Xie's systematic policy testing work already compares coverage with fault detection. A further closest-work lead, Hwang et al., *Selection of Regression System Tests for Security Policy Evolution* (ASE 2012), studies test selection after policy changes. Its institutional record was located at https://orbilu.uni.lu/handle/10993/16020 and https://experts.illinois.edu/en/publications/selection-of-regression-system-tests-for-security-policy-evolutio/ ; full-text retrieval failed in this follow-up, so detailed overlap remains unresolved. Do not infer absence of a method from this retrieval failure.

The remaining possible contribution is an empirical audit of the adequacy of AI benchmark verification plans and how obligation coverage changes across requirement variants. That distinction is proposed, not cleared as novel. Existing AutoCedar source-coverage tracking must also be compared semantically, not merely by presence of traceability labels.

## Scope for a subsequent study, pending literature clearance

Question: when a benchmark variant preserves a written positive authorization requirement, does its formal acceptance plan still require that behavior?

Unit: a requirement obligation within a base/variant lineage. Aggregate by lineage; do not treat requests or closely related variants as independent samples. Inventory the full clinical lineage before choosing further examples. Record unchanged, narrowed, expanded, removed and ambiguous requirements. Exclude ambiguous ones from confirmed-omission counts while reporting their number.

Baselines: original plan; unchanged-obligation transfer where schema-compatible; requirement-aware transferred obligations. Controls: explicitly removed permissions, newly constrained requests, semantically equivalent policy rewrites and inconsistent plans. A transferred obligation is not automatically correct when consent or another intended constraint changes.

Measurements: schema/tool errors, inconsistent original plans, confirmed missing obligations, intentional changes, unresolved interpretations, and counterexample survival after justified plan repair. Include all failures and exclusions. No model training, cost claim or HPC run follows from this diagnostic.

Reject a novel-method claim if existing testing methods already implement the same mechanism. Reject a benchmark-wide empirical claim without a fixed inventory and defensible requirement interpretation. Publishable scope remains undecided; this artifact is a reproducible technical finding rather than a finished journal paper.
