# Policy-repair feasibility result and research decision

Date: 2026-10-09

## Tangible outcome

An original, standard-library-only audit now runs locally. Reproduce with:

```
python -m unittest discover -s tests -v
python src/repair_audit.py
```

The model exhaustively enumerates 24 requests: three principals, two actions, two resources and a Boolean trusted context. Five requests are allowed by an independently expressed Boolean requirement. Rules use exact equality, default denial and explicit-deny precedence. This is a deliberately limited toy language, not an implementation of AWS IAM or Cedar. An absent condition matches all values of that field. Unsupported values and fields are rejected.

All repairs are hand-authored fixtures. No model, participant, external dataset, production system or HPC job was evaluated. The two visible checks were deliberately chosen to illustrate incomplete coverage, not sampled to estimate real-world prevalence.

| Transition | Visible checks passed | Full-domain errors after repair | Newly over-permitted | Newly over-denied |
|---|---:|---:|---:|---:|
| Initial to targeted repair | 2/2 | 0 | 0 | 0 |
| Initial to overbroad repair | 2/2 | 4 | 4 | 0 |
| Correct to write-blocking repair | 2/2 | 2 | 0 | 2 |
| Correct to equivalent rewrite | 2/2 | 0 | 0 | 0 |
| Overbroad to targeted repair | 2/2 | 0 | 0 | 0 |

Ten automated tests passed, including conservation of errors over every pair of the five policies (25 comparisons), default denial, explicit denial, unsupported input, equivalence and recovery. Machine-readable output includes concrete regression witnesses and a source hash. Exhaustiveness applies only to the declared finite universe. Oracle intent was authored by us and has not been independently validated by domain experts.

## Literature decision

[CloudFix](https://arxiv.org/html/2512.09957v1), Sections III and III-A, repairs policies against supplied allow/deny request specifications. This motivates checking the distinction between passing supplied requests and preserving other decisions; it does not establish that CloudFix is unsound or that nobody has studied preservation.

[Does Fixing Break Security?](https://arxiv.org/html/2608.13404v1), Sections 4.2-4.3, already measures passing-to-failing checks during iterative IaC repair. It distinguishes ambiguous multi-resource outcomes and exclusive failures. Therefore tracking repair regressions is not a new contribution. Our request identities avoid that particular check-aggregation ambiguity within the toy domain, but this engineering choice is not established research novelty.

Decision: GO for reusable feasibility infrastructure; NO-GO for a novelty claim or manuscript asserting a new method. Do not expand this illustrative suite into thousands of synthetic cases simply to obtain a result.

## Gate for a substantive study

Candidate question: under a fixed repair budget, how much does request-suite success overstate preservation of authorization decisions outside the supplied repair suite, and does that discrepancy persist under a native policy engine and independently authored requirements?

Before collection: compare this exact question against CloudFix's complete evaluation and artifacts, AutoCedar, RAISE, formal policy repair and regression/overfitting work. RegoMender full text remains unresolved. Record whether each evaluates held-out requests, semantic preservation, evolving requirements and both error directions. Abandon or narrow the question if already covered.

If that gate survives, freeze tasks and requirements before generation; use native-engine conformance; separate repair-visible requests from exhaustive bounded audit requests; distinguish required intentional changes from regressions. Baselines: no repair, independent resampling and feedback-guided repair at matched candidate and token budgets. Report parse failures separately, both denial error directions, repair success and uncertainty at task level. Do not treat correlated requests as independent experimental samples. Multiple models and task families are needed before generalization claims. Negative or null results must be retained. Public releases require verified dataset terms.

Human decisions and review-time reductions remain out of scope. Local hardware suffices for this audit; HPC becomes relevant only for a justified, frozen multi-model experiment.
