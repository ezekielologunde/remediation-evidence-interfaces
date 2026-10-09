# Computational successor screening

Date: 2026-10-09. Constraint: no human verification or participant access currently available. This is a targeted literature screen, not a cleared novelty claim. Human-interface study remains on hold.

## Comparison

| Candidate | Closest primary evidence | Disposition |
|---|---|---|
| Executable checking of summary factuality | [SummExecEdit](https://arxiv.org/abs/2412.13378), abstract inspected | Generic executable summary validation already exists. |
| Security repair without regression | [PatchEval](https://arxiv.org/abs/2511.11019), abstract; [CRSBench](https://oss-crs.openssf.org/crsbench), project page | Existing executable security/functionality benchmarks. Merely adding tests is insufficient. |
| Secure infrastructure generation | [SWE-InfraBench](https://assets.amazon.science/28/40/7bfdfa7541168a7adb7ec6674e1d/scipub-approval152134-41334456-sweinfrabench-evaluating-language-models-on-cloud-infrastructure-code.pdf), search-extracted abstract; [IaC-Eval](https://www.cs-pk.com/neurips24-iac-eval.pdf), search lead | Generation and incremental edits already benchmarked. Full texts pending. |
| Authorization-policy synthesis | [RAISE](https://arxiv.org/html/2609.33796v1), abstract and implementation link | Formally verified synthesis already studied. Not our proposed contribution. |
| Authorization-policy change understanding | [Intent-Based Access Control](https://arxiv.org/abs/2402.07332), abstract | Existing differencing is direct overlap; examine it before selecting the topic. |

Do not infer missing coverage from abstracts. These alternatives are screened for feasibility and overlap, not ranked by novelty probability.

## Working candidate for deeper review

Can a model correctly distinguish access expansion, restriction, mixed change and semantic equivalence between two authorization policies, and support each claimed change with an executable request witness?

Possible additional question: are conclusions stable under semantics-preserving rewrites, while still sensitive to small permission-changing edits? Neither metamorphic testing nor policy differencing is claimed as new. A specific unaddressed failure mode must survive full-text comparison.

## Objective evaluation contract

- Inputs: schema, entities, request domain and before/after policy sets. Policies must validate under the pinned implementation.
- Output: structured classification plus concrete principal/action/resource/context witnesses for expanded or restricted access. Free-form prose is secondary and not automatically scored as correct.
- Oracle: evaluate witnesses with the native Cedar engine. For a declared finite request domain, enumerate all requests to classify changes exactly within that domain. Enumeration is not proof over unrestricted contexts.
- Universal claims require a sound supported symbolic analysis with explicit bounds and assumptions. Unknown or timeout is not equivalence.
- For equivalence, an empty witness list is insufficient. For mixed change, require witnesses in both directions. Syntactic invalidity and evaluation errors remain separate outcomes.
- Baselines: exact finite-domain enumeration, native supported analysis, simple textual-diff heuristic, model without tools, model with identical oracle budget. Compare accuracy and cost; a model cannot claim correctness superiority over an exact oracle on its own domain.
- Splits: group all mutations and rewrites of a seed policy together. Reserve structural families, not just random rows, to limit leakage.
- Failure criteria: existing benchmarks already test this distinction; apparent novelty is only a language substitution; or results amount to known model inconsistency without new evidence or useful procedure.

## Public resources and caveats

[Cedar specification repository](https://github.com/cedar-policy/cedar-spec) supplies a formalization, differential testing infrastructure and policy/request generators. Its repository page states Apache-2.0. A pinned checkout, complete license/notice review and supported-feature audit are still required before reuse. Generated cases would be synthetic public artifacts, not operational deployment data.

RAISE links [implementation](https://github.com/Aizhouym/raise). Dataset availability, license, contamination boundaries and reproducibility have not yet been checked. Do not redistribute its data based solely on a paper link.

## Next gate

Read the Intent-Based Access Control differencer and RAISE evaluation in full; trace access-control semantic-difference and metamorphic-testing references; determine whether the proposed paired-policy task adds anything beyond existing tests. Then audit source availability and oracle feasibility. No model experiments, downloads, training or HPC jobs are justified yet. Local CPU work is sufficient for screening; batched inference could later use ASA-X if the contribution and hardware requirements are established.
