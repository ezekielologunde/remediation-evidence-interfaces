# Clinical family audit: release assessment

The fixed 11-scenario clinical inventory produced 149 passing original checks, 44 schema-valid nonempty probes and 22 successful policy-order equivalence checks. Ten exception-retaining scenarios have six covered and 34 omitted positive probes. The removal scenario contributes four intentional-denial controls. Adding the adjusted probes preserves original-plan acceptance in all ten retained-exception scenarios; in the removal control it violates four original ceilings.

Scope: these are related scenarios selected after an initial finding. Counts do not estimate whole-benchmark prevalence or model error. The formal result is existence of accepted candidates that omit probe behavior. Calling the behavior required relies on our documented interpretation, without independent adjudication.

The full Hwang et al. ASE 2012 paper was retrieved from https://orbilu.uni.lu/bitstream/10993/16020/1/test_selection_ase2012-short.pdf and its methods/evaluation inspected. It selects existing system tests using mutation correlation, coverage or recorded requests after policy changes, evaluated on three Java/XACML systems. The present artifact audits stored acceptance obligations rather than selecting system tests. This distinction supports a focused empirical case-study framing; it does not establish a new algorithm or priority claim. Earlier statements that this full text was unavailable describe the preceding retrieval attempt and are superseded here.

The manuscript is a technical case-study preprint candidate. A full journal novelty claim remains unsupported. Independent interpretation review, other-family evidence and exact original-toolchain reproduction are limitations, not results to invent. No ResearchGate upload, journal submission, or upstream issue report was performed as part of this release.

Artifacts: `analysis/clinical-family/receipt.json`, `protocol/clinical-inventory-protocol.json`, `src/clinical_family_audit.py`, and `paper/main.tex`. Verification separately re-parses raw verdict text and compares table/plot values. The proof method and requirement interpretation are not independently reimplemented by that verifier.

## Released-output and transfer follow-up

The fixed released-output protocol reused all probes unchanged. All workspace schemas, specifications, plans and references match the original audited inputs by SHA-256. All 11 available clinical policies pass 149 original checks and cover all 40 positive probes. Four removal controls retain counterexamples. This negative finding must remain in the paper.

The run summary identifies an unavailable `repair_pass_20260630` directory as final inspected workspaces. Available candidates are not asserted to be final paper outputs.

An exploratory doccloud_base transfer case uses a released baseline plus an explicit non-owner View/Modify forbid. Both validate and pass all 43 original checks. Two ACL probes validate and are nonempty; baseline covers both, narrowed candidate omits both. This is one transfer case, not a full second-family audit.

Release scope: completed technical preprint package with 5 pages, 2 tables and 2 diagrams, updated abstract, methods, results, threats and conclusion. No actual released-output omission was found. A strong journal novelty claim remains unestablished; further experiments should answer a new scoped question rather than seek a preferred outcome. Native receipts are in analysis/released-clinical and analysis/doccloud-transfer. Final inspected upstream outputs and independent requirement interpretation remain unavailable. No external preprint upload or submission occurred.
