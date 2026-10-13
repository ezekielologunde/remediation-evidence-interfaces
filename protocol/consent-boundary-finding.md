# Qualified auditor access is not required by the inspected floors

Status: native Cedar/SymCC confirmation completed with Cedar 4.13.0 and CVC5 1.4.2. Scholarly novelty is not established. The original Python harness and its documented Cedar 4.10.0 environment were not executed.

## Evidence and scope

Inspected CedarBench scenario `clinical_add_consent` at commit `0201565abf5993e258764d3f0ef83a59d3b4962e` of https://github.com/neselab/cedar-synthesis-engine.

Pinned source directory: https://github.com/neselab/cedar-synthesis-engine/tree/0201565abf5993e258764d3f0ef83a59d3b4962e/cedarbench/scenarios/clinical_add_consent

The inspected sources are `policy_spec.md`, `verification_plan.py`, and its nine referenced Cedar policies. The plan contains five ceiling checks, four floor checks, and two action-liveness checks. The written requirement exempts GlobalAuditors from the department restriction when they otherwise qualify. Every inspected floor instead requires equal departments. A ceiling permitting an exception does not require that exception to be implemented.

## Counterexample

Let Q mean an active project and either a ClinicalResearcher satisfying clearance/classification constraints or a PrincipalInvestigator satisfying risk/device constraints. Let D mean matching departments, A mean auditor membership, and C mean View or patient consent.

The specification interpreted here permits `Q AND (D OR A) AND C`. The deficient candidate permits only `Q AND D AND C`. It removes cross-department auditor access. Its smaller allow set remains inside the ceilings, contains all four same-department floors, and is live for both actions.

A concrete witness is a PrincipalInvestigator who is also a GlobalAuditor, in a different department, accessing an active project with low network risk and a compliant device. View should be allowed under the stated exception but is denied by this candidate. Consent is immaterial to View. This witness does not require ClinicalResearcher membership.

## Reproduction and repair check

Run `python src/audit_consent_boundary.py`. Output is saved in `analysis/consent-boundary-audit.json`.

The independent predicate abstraction exhaustively checks 2,048 action/Boolean valuations. The candidate has zero modeled boundary violations and both actions are live. It denies 45 valuations allowed by the interpreted specification. Adding an auditor floor `Q AND A AND C` rejects the candidate on all 45 of those valuations.

These are predicate valuations, not independent samples, benchmark tasks, actual users, or an estimated error rate. The abstraction alone does not execute Cedar or prove all valuations schema-realizable. The follow-up below confirms a concrete witness natively. This result says nothing about whether a published synthesized policy actually omitted the exception.

## Native confirmation

Run `python src/native_consent_audit.py --cedar <cedar-executable> --cvc5 <cvc5-executable>`. The script downloads the pinned schema and references as data, without executing upstream Python. It independently maps the original plan to CLI calls. Raw commands, exit codes, solver counterexamples and input SHA-256 hashes are retained in `analysis/native-consent/receipt.json`. The original candidate, interpreted target, added floor and concrete request are in that directory.

Observed with official experimental Cedar CLI 4.13.0 and CVC5 1.4.2:

| Check | Result |
|---|---|
| Candidate, interpreted target, added floor schema validation | All 3 pass |
| Original safety/department/consent ceilings | 5 of 5 VERIFIED |
| Original positive floors | 4 of 4 VERIFIED |
| Original View/Edit liveness | Both pass: always-denies DOES NOT HOLD |
| Added auditor floors against deficient candidate | Both implications fail with counterexamples |
| Added auditor floors against repaired target | Both VERIFIED |
| Concrete View request, schema validation enabled | Deficient candidate DENY; interpreted target ALLOW |

The solver returns exit code zero for both VERIFIED and DOES NOT HOLD; the reproduction checks verdict text rather than conflating process success with proof success. Authorization returns 2 for DENY and 0 for ALLOW. This is independent native confirmation of a verification-plan coverage omission in one pinned scenario, not reproduction of published model performance. The documented 4.10.0 toolchain was unavailable as the requested GitHub release tag; the advertised container required authentication. Version parity remains untested.

Tool releases: https://github.com/cedar-policy/cedar/releases/tag/cedar-policy-cli-v4.13.0 and https://github.com/cvc5/cvc5/releases/tag/cvc5-1.4.2 . The downloaded Cedar archive matched its published SHA-256 checksum. Local tool binaries and cached upstream sources are excluded from Git.

## Closest-work check

NIST SP 800-192 (2017), Sections 4.2 and 5.4, already treats coverage and mutation-based checking of access-control requirements. This directly defeats a broad claim that checking the adequacy of verification obligations is new. Source: https://nvlpubs.nist.gov/nistpubs/specialpublications/nist.sp.800-192.pdf

Martin and Xie's *Toward Systematic Testing of Access Control Policies*, Sections 7-8, defines policy mutation testing, equivalent-mutant handling and compares structural coverage with fault detection. A simple mutation-survival score would substantially overlap this work. Source: https://prolangs.cs.vt.edu/rutgers/meetings/masplas06/papers/5_Martin.pdf

The pinned AutoCedar README also exposes source-to-property provenance and a coverage ledger. Therefore adding generic requirement tracing is not a defensible new contribution without a closer implementation comparison. Source: https://github.com/neselab/cedar-synthesis-engine/blob/0201565abf5993e258764d3f0ef83a59d3b4962e/README.md

## Research decision

This is a tangible verification-target coverage finding in one pinned scenario, not proof of a novel research contribution. AutoCedar already acknowledges that formal validity depends on approved intent. Do not frame this as refuting formal verification or discovering that specifications can be incomplete.

Decision after native confirmation: retain this as a reproducible benchmark-quality finding. Do not yet launch a larger model study or write a publication-ready manuscript. The remaining candidate is a narrowly scoped empirical audit of direction-specific obligation omissions in AI policy benchmarks, with independent requirement adjudication and controls for intended underspecification. Its novelty is unresolved. A broader study must first distinguish that contribution from existing mutation testing and source-coverage methods, then freeze task selection, mutation operators and rejection criteria. No HPC allocation is justified by this single case.
