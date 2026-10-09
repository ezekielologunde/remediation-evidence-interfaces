# Candidate screen: decision-relevant evidence changes

Status: literature-screening candidate, not novelty clearance or preregistration. Date: 2026-10-09.

## Selection rationale

The adaptive-deception re-entry failed its contribution gate. Segmentation's local README also records unresolved overlap with existing monitors and persistent-session tests. A generic agent-security harness remains useful engineering but is not automatically research. This reserve topic offers a different empirical question involving human judgment, subject to literature and participant feasibility gates.

## Primary-source ledger

| Source | Evidence read | Implication |
|---|---|---|
| [Reframing LLM Agent Security as an Agent-Human Interaction Problem](https://arxiv.org/html/2605.24309v1) | Full-text agenda and approval-mechanism passages | Human approval burden and information presentation are already explicit research priorities. An agenda does not establish our exact gap. |
| [Guarded Commits](https://arxiv.org/abs/2610.00037) | Author abstract record | Transactional human approval and preserved evidence are occupied topics. Full-text comparison pending. |
| [Approved Too Late](https://arxiv.org/abs/2608.26306) | Author abstract record | Verdict staleness is already studied. Do not claim discovery of stale approval. Full-text comparison pending. |
| [Human-Centered Explainability in AI-Enhanced UI Security Interfaces](https://arxiv.org/abs/2601.22653) | Author abstract record | Closest security-interface lead; experimental design and dependent variables need full-text extraction. |
| [Safe Remediation as Risk-Constrained Intervention Decision](https://arxiv.org/abs/2607.20005) | Author abstract record | Risk-sensitive remediation and human escalation overlap with the broad motivation. |

These are screening records, not peer-review or acceptance assertions. Searches also surfaced approval-interface studies and commercial guidance; unverified vendor performance numbers are not used as research evidence. Search terms covered agent approval, stale evidence, human study, time-of-check/time-of-use, and security evidence freshness. This was not an exhaustive review.

## Working research question

When evidence changes between proposal and review, does a structured explanation of decision-relevant changes improve human discrimination between still-valid and invalid remediation recommendations, compared with timestamps and generic freshness warnings?

The construct is semantic relevance, not simply elapsed time. Old evidence can remain applicable; a recent change can invalidate an action. All interfaces must expose equivalent underlying facts. A difference in access to evidence must not be mislabeled an interface effect.

## Conditional study design

- Conditions: timestamp plus accessible source details; generic changed-evidence warning plus the same details; structured before/after delta plus the same details. Keep action scope, evidence and execution controls identical.
- Cases: cross elapsed time with material versus immaterial changes. Include fresh-but-invalid and old-but-valid cases, missing data, and disagreement. Use synthetic environments and deterministic validity rules, independently reviewed before collection.
- Tasks: approve, reject or defer a synthetic remediation recommendation; explain the decision. No real infrastructure actions.
- Primary endpoint: invalid-approval rate. Paired secondary endpoint: valid-approval rate, so blanket refusal cannot look successful. Also record deferral, comprehension and decision time. Predefine treatment of timeouts.
- Hypothesis: structured deltas improve invalid-approval detection without materially degrading valid approvals. This is a hypothesis, not an expected positive result.
- Allocation: counterbalance cases and interfaces without exposing the same scenario twice to a participant; model participant and scenario variation. Separate pilot from confirmation.
- Confounds: reading volume, warning salience, default selection, expertise, order, learning, and change frequency. Match these or explicitly model them.
- Analysis: freeze primary comparison, acceptable valid-approval loss margin, exclusions, multiplicity handling and power rationale before collecting outcomes. Do not choose a sample size from a desired significance result.

## Gates before implementation as a research study

1. Read closest full texts and trace references on change blindness, security warning habituation, version differences, provenance interfaces and approval comprehension. Reject if an existing study already answers this question under comparable conditions.
2. Confirm access to an appropriate participant population and applicable ethics-review/consent arrangements. No recruitment or collection is authorized by this screening document.
3. Decide whether synthetic case correctness is defensible with independent expert review. No model-generated label should be treated as ground truth without verification.
4. Human outcomes cannot be replaced by simulated LLM participants. Without participants, a working interface is an engineering deliverable, not evidence of decision improvement.

Local compute is sufficient for this candidate. HPC would not remedy missing human evidence. No experiment, participant collection, new public dataset or manuscript result is claimed.
