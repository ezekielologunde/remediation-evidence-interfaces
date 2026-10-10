# Policy-differencing full-text checkpoint

The separately proposed Agentic IAM umbrella was added to the portfolio backlog at the user's request. It does not replace this computational review.

Primary source: [Intent-Based Access Control, v3](https://arxiv.org/html/2402.07332v3), sections 4.2 and 5.1.1. Reviewed October 9, 2026.

The benchmark explicitly compares natural-language access-control matrices both with SQL implementations and with other natural-language matrices. It evaluates role/view mapping and privilege subsumption. Its base, SQL and perturbed matrix construction includes semantically equivalent wording variations. Thus policy differencing and rewrite invariance are already covered. Do not claim either as our invention.

Possible remaining distinction to investigate: paired executable policies containing both permission-changing edits and equivalent rewrites, with concrete request witnesses in both directions and interactions between explicit denial and entity hierarchy. This is a scope distinction, not proof of a literature gap. Other formal access-control tools may already provide the complete functionality.

Next comparison must inspect Cedar synthesis/analysis benchmarks and older semantic policy differencing. A language change from SQL to Cedar alone is insufficient. If the symbolic baseline already answers the entire practical question, a model-only implementation needs a separate justified research objective rather than a claim of methodological improvement.

No new experiment, model result or novelty claim is reported.
