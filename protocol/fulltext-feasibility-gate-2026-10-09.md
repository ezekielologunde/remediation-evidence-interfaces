# Full-text and feasibility gate

Date: 2026-10-09. Decision: human-outcomes study on hold. The user confirmed that participant access and an ethics-review route are not yet established. No recruitment, collection or participant simulation has occurred.

## Reviewed evidence

- [Human-Centered Explainability in AI-Enhanced UI Security Interfaces](https://arxiv.org/pdf/2601.22653), methodology: reports a 24-person within-subject study of four explanation modalities, including counterfactuals, with counterbalanced tasks and analyst-validated labels. This is close enough that generic explanation improvements cannot be our contribution. Methods passages inspected; reported results not independently reproduced.
- [Guarded Commits](https://arxiv.org/html/2610.00037v1), section 6: explicitly distinguishes enforcement of a policy-valid resolution from correctness of the reviewer decision. This supports separating execution guarantees from human comprehension, but does not establish the absence of prior human studies. The HTML displays a date inconsistent with its identifier month; verify bibliographic metadata before manuscript citation.
- [Approved Too Late](https://arxiv.org/html/2608.26306v1), section IV: separates approval-expiry rates from utility and cautions about differing accepted-case denominators. Our human design must likewise report valid approvals and invalid approvals separately, including deferrals and timeouts.
- [Polymorphic warnings, CHI 2015](https://scholarsarchive.byu.edu/facpub/9306/): institutional abstract record identifies changing warning appearance as an established habituation intervention. Full text remains to be reviewed. Visual novelty cannot be conflated with semantic information.

## Revised comparison boundary

Keep access to source facts identical. Distinguish a raw before/after display from a structured dependency explanation. Match highlighting, layout and reading burden as far as feasible. Include material and immaterial changes, and fresh-but-invalid versus old-but-valid evidence. Counterfactual explanations are a necessary conceptual comparator. No claim that this exact design is novel has cleared review.

## Feasibility disposition

Do not build a participant-facing study or write a results paper before recruitment feasibility and applicable review requirements are resolved. A local synthetic prototype could validate scenario logic but would not demonstrate human decision improvement. Existing public traces may support a separate computational question; they do not provide missing randomized interface outcomes.

Continue portfolio screening toward public-data computational research. Candidate direction: evaluate whether evidence-change summaries preserve decision-critical facts and avoid falsely invalidating harmless changes. This is only a lead. It must be checked against change summarization, factual consistency, code-review explanation and agent approval benchmarks before implementation. The labels must come from explicit task predicates or independently adjudicated records, not an LLM judge alone. Results from that study could not be described as reduced human error.
