# Qualified auditor access is not required by the inspected floors

Status: reproducible Boolean coverage counterexample. Native Cedar execution and scholarly novelty are not established.

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

These are predicate valuations, not independent samples, benchmark tasks, actual users, or an estimated error rate. The abstraction does not execute Cedar, prove all valuations schema-realizable, or reproduce the upstream synthesis engine. The concrete PI/auditor witness is the priority for native schema validation. This result says nothing about whether a published synthesized policy actually omitted the exception.

## Research decision

This is a tangible verification-target coverage finding in one pinned scenario, not proof of a novel research contribution. AutoCedar already acknowledges that formal validity depends on approved intent. Do not frame this as refuting formal verification or discovering that specifications can be incomplete.

Next gate: validate the witness and deficient candidate with the native schema and engine; inspect prior work on specification adequacy and policy mutation testing; then determine whether a systematic requirement-to-obligation coverage method adds something beyond existing methods. A larger study must freeze task selection, independent requirement extraction, mutation operators and rejection criteria before evaluation. No HPC allocation or publishable-manuscript claim is justified by this single case.
