# Literature-supported computational follow-up

Date: 2026-10-09. Status: candidate protocol and artifact feasibility audit, not a cleared novelty claim.

## Decision on the previous framing

Generic policy semantic differencing is not a new method: [Margrave](https://doi.org/10.1109/ICSE.2005.1553562) already analyzes change impact. LLM4AC adds language-based policy comparison. [AutoCedar](https://arxiv.org/html/2607.03656v1) and [RAISE](https://arxiv.org/html/2609.33796v1) cover verifier-guided synthesis. Do not build a renamed version as an original contribution.

## Concrete unresolved comparison

RAISE Appendix G explicitly notes that guided exploration uses extra samples without an extra-resampling control, that training uses one seed, and that generated verification plans define correctness. These are author-stated limitations, not evidence that the method fails. A follow-up can ask whether semantic verifier guidance improves policy synthesis under matched resource budgets and on held-out policy structures. Completing an omitted control is an empirical extension, not automatically a new algorithm.

Primary question: does correct semantic feedback improve executable policy correctness beyond extra unguided sampling, when candidate-generation budget is matched?

## Proposed staged design

1. First reproduce a small published evaluation with a pinned verifier and documented scenario provenance. Reproduction failure must be resolved or reported before comparisons.
2. Inference-only pilot: same frozen model and tasks, shared initial candidates, then either unguided resampling, binary failure feedback, detailed correct feedback, or deliberately mismatched feedback. Mismatched feedback is an experimental negative control in an isolated evaluator, never deployed authorization advice.
3. Match total generated candidates for the primary comparison. Record tokens, verifier calls and elapsed time separately; also report success under fixed token caps. Candidate matching is not compute matching, since prompt lengths and verification costs differ.
4. Predeclare task-family splits, generation seeds, stopping rules and error treatment. Count verifier unknown/timeouts separately. Evaluate all allocated cases, not only successfully repaired ones.
5. Only after a justified pilot, consider multi-seed training with equal extra-sampling controls. Inference-only results cannot establish training-stage causal effects.

Endpoints: full-plan success, over-permission and over-restriction failures, invalid syntax, unknowns/timeouts, tokens and verifier calls per solved task. Report paired task-level uncertainty and cluster by source scenario family. Equivalence or null results remain valid outcomes. Do not select seeds or task subsets for favorable margins.

## Ground-truth boundary

No human labels are available. Score compliance with explicit executable specifications, not faithfulness to ambiguous natural-language intentions. Use controlled formal specifications and deterministic renderings for any original cases; describe them as synthetic. A symbolic checker does not verify that its own specification represents a person's intent. No human usability or operational-security claims follow.

## Artifact audit

On October 9 the [RAISE repository](https://github.com/Aizhouym/raise) advertised source and a scenario archive, but no released weights, checkpoints, logs or evaluation results. README states that full verification/training additionally needs Cedar CLI, cvc5, veRL and a model. GitHub repository metadata returned a null license, and the root listing contained no license file. This does not establish the licensing of every nested artifact. No code or corpus has been copied, redistributed or executed in this audit.

Before reuse: inspect file-level permissions and artifact manifests; pin revisions and hashes; verify the toolchain and model availability. If rights remain unclear, do not redistribute upstream material or silently call a fresh independent implementation an exact reproduction. A separately authored formal corpus may permit an independent study, but changes comparability and requires its own literature gate.

## Compute and remaining gates

Local CPU: source/permission review and verifier controls. Local available model: small feasibility only after oracle validation. ASA-X: optional batched inference or multi-seed training after checking actual GPU memory, queue limits and software. No job has been submitted and no budget has been assumed.

The strongest current lead is the resource-matched feedback comparison because the missing control is explicit in the literature. Remaining work is artifact clearance, closest-work review of budget-matched verifier feedback, and protocol freeze. No full manuscript should be drafted as if the hypothesis were already supported.
