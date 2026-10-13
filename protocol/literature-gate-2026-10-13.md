# Literature gate refresh: repair generalization

Date: 2026-10-13. Status: broad candidate rejected; narrower candidate remains unverified. No new experiment or novelty claim.

## Evidence matrix

| Primary source | Evidence inspected | Implication |
|---|---|---|
| CloudFix, https://arxiv.org/html/2512.09957v1 | Evaluation RQ4 explicitly repairs with supplied resource variants and evaluates 15 unseen variants. | Unseen-request generalization is already studied. Do not describe it as missing from CloudFix. |
| AutoCedar, https://arxiv.org/html/2607.03656v1 | Sections III and evaluation distinguish reviewed floors, ceilings and liveness; validity remains relative to approved intent. | Boundary preservation and both permission directions are established design elements. Removing human review does not create equivalent intent validity. |
| IAM-PolicyRefiner, https://www.amazon.science/publications/automatically-reducing-privilege-for-access-control-policies | Author publication page explicitly reports held-out request evaluation and constrained privilege reduction. | Log overfitting and preservation cannot be claimed as new problems. Full implementation comparison remains pending. |
| Quantitative Policy Repair, https://sites.cs.ucsb.edu/~weiers/policy_repair.pdf | Problem statement combines permissiveness bounds with must-allow requests. | Security and availability constraints already coexist in symbolic repair. |
| RegoMender, https://conf.researchr.org/details/ase-2026/ase-2026-research-track/194/RegoMender-A-Multi-agent-Framework-for-Automated-Rego-Policy-Repair | Official conference record establishes title/authors; complete methods not inspected. | Unresolved closest-work blocker, not evidence of an absent evaluation. |
| Restricter, https://arxiv.org/html/2601.14582v1 | Full-text endpoint located. Detailed evaluation comparison still pending. | Include in next artifact review before choosing a contribution. |

## Decision

Reject the broad framing that supplied-request success versus unseen-request success is unexplored. Preserve the toy audit as correctness infrastructure, not research evidence. Do not run a larger synthetic sweep or allocate HPC to this rejected framing.

The remaining candidate is a controlled empirical comparison of repair locality: after an intended change, are previously correct decisions outside that change preserved, particularly across unrelated roles/actions and interacting denial rules? This is a candidate distinction only. Formal noninterference, regression testing, policy differencing and AutoCedar may already subsume it.

## Falsifiable candidate, conditional on literature clearance

Question: At matched candidate budgets, does a repair strategy that succeeds on supplied corrections introduce changes outside a fixed intended change region more often than a semantic-preservation constrained strategy?

Define a reference policy P0, intended change region C and independently fixed target P*. Outside C, P* must equal P0. Evaluate target disagreements inside C and unintended allow/deny changes outside C separately. A reference authored by this project is a test oracle, not independently validated organizational intent.

Baselines: unchanged policy; deterministic symbolic repair where supported; independent model resampling; feedback-guided repair; preservation-constrained repair. Match candidate budgets, report actual tokens and runtime rather than claiming token equality from a common cap. Separate parser failures and engine errors. Evaluate policy tasks as units, not individual requests as independent samples.

Reject this candidate if closest artifacts already evaluate the same intended-change/preservation distinction with equivalent controls, or if only a change of policy language remains. Do not call a mechanical preservation guarantee a discovered empirical benefit. Negative and null outcomes remain reportable but do not establish novelty by themselves.

## Next executable gate

1. Locate and inspect CloudFix, AutoCedar, Restricter and RegoMender artifacts and licenses. Record commit/version and exact evaluation cases.
2. Determine whether existing publicly licensed tasks specify both intended changes and unaffected behavior. Do not infer intent from forum text or generated labels alone.
3. Compare non-local preservation, two error directions, equivalent rewrites and task-level held-out splits against each artifact.
4. Only if a material distinction survives, freeze native-engine conformance checks, task splits and rejection criteria before a small local pilot.
5. HPC remains deferred until the gap and pilot survive. No participant outcomes are claimed.
