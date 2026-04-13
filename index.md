---
layout: default
title: "Compliance Theater in Multi-Agent Systems"
---

# Compliance Theater in Multi-Agent Systems

*Draft in progress — publication target 2026-04-26.*

## Abstract

Nine Claude agents, prompted to audit adversarial smart contract code, consistently self-reported completing checklists they had not executed — producing well-formed outputs that performed thoroughness without the underlying work. We name this failure mode **compliance theater**, a previously-unnamed affirmative-assertion sub-case of MAST FM-3.2 (Verification Step Omission, under FC3 Task Verification)[^mast], distinct from sycophancy, sabotage, and satisficing. The pattern appears without instruction, reward signal, or persona directing the agent to misreport; it reproduces across Opus and Sonnet and across offensive and defensive task framings; and three pre-gate runs confirm it arises under structured-checklist pressure without the <60% discard threshold introduced in commit cb0026d — consistent with Regressional Goodhart. We counter it with evidence gates keyed to artifact existence, not agent self-assessment. Over a 17-run iteration window — non-monotone, with 7 discards, 2 of them zero-score pipeline failures — rubric score advances from 39.8 to 112.5 (Spearman r = 0.78). Ground-truth outcome labels are sparse (N = 9); the contribution is the named phenomenon, the architectural intervention, and the longitudinal trajectory.

Author: Diego Quinto (0xquinto) · Independent Researcher

---

## 2. The Phenomenon: Compliance Theater

In run-2026-03-15T13-40-26Z, the `insolvency-engineer` agent reported 11 ruled-out attack vectors — each with a populated `test_file` field asserting a Forge test had been written — while Phase C checklist completion was 0/59 and the trace-analyzer (see §6) registered 3 tool calls total. It produced a structurally complete output that performed thoroughness without executing the underlying work.[^schneier]

We name this pattern **compliance theater**: a sharpened affirmative-assertion sub-case of MAST FM-3.2 (Verification Step Omission, under FC3 Task Verification)[^mast], introduced here to capture the case the abstract named.

We classify a trace segment as compliance theater when three observable conditions jointly hold:

**(C1) Affirmative assertion of verification.** The agent's output — in natural language or structured fields — claims that the verification was performed. Silent omission of verification, without such a claim, is plain FM-3.2 under MAST and is excluded here.

**(C2) Trace-level refutation.** An independent signal that the agent cannot read or hill-climb on — in this work, a 16-dimension trace-analyzer counting tool calls, files read, and bash commands — shows the claimed work did not occur at anything close to the claimed scale.

**(C3) Gate-shaped, not user-shaped, pressure.** The trace contains no user-turn sentiment the report could be shaping to; the pressure it responds to is a completion-valued gate in the system prompt — here, the black-hat preamble's <60% discard threshold. C3 distinguishes compliance theater from sycophancy (user-sentiment-shaped); we flag it weakest: a broad sycophancy-to-system-prompt definition could absorb it, and a no-gate ablation arm is required to settle the question. We treat the separation as provisional pending that ablation; §4's natural experiment partially constrains C3 by showing the phenomenon is not created by the specific discard threshold, but does not dispose of the broader sycophancy-to-system-prompt absorption argument.

The mechanism fits Regressional Goodhart (Manheim & Garrabrant 2018, arXiv:1803.04585) — but the adversarial optimizer is the author, not the agent. Over 17 runs the author selected interventions that moved the rubric — the measure became the target.

Compliance theater is distinct from sycophancy (user-shaped, not gate-shaped), from sabotage — SHADE-Arena (arXiv:2506.15740) models goal-misaligned concealment producing structurally identical outputs; compliance theater arises under completion-valued shaping without an adversarial goal, and §4's pre-gate runs exhibit it under no hostile persona — and from satisficing (the agent asserts completion rather than silently under-delivering).

[^schneier]: The term borrows from Bruce Schneier's "security theater" (*Beyond Fear*, 2003): visible ceremony that signals diligence without performing the underlying work. No prior use of "compliance theater" in LLM or agent-evaluation literature was found in a targeted search conducted 2026-04-12.

---

## 4. Setup: The Limit Break AMM Audit

Section 4 describes the audit harness: agent roster, preamble evolution, evidence gates, and the tool fleet under which the pre-gate runs executed. The full setup description is deferred to a companion technical appendix; this section focuses on the one setup fact the argument turns on — the harness's own git history.

### The Natural Experiment

Commit `cb0026d` (2026-03-15 18:10 -0500) introduced the "<60% Phase C items completed → findings discarded" language into `black-hat-preamble.md`. The hostile reviewer's circularity objection rests on that gate existing from the start; the repo's git history refutes it. Three runs in `experiments.tsv` precede that commit:

| run_id | commit | regime | score |
|---|---|---|---|
| run-2026-03-14T22-05-52Z | c9839a8 | No gate | 39.8 |
| run-2026-03-15T13-40-26Z | 67f6e9f | No gate | 44.2 |
| run-2026-03-15T22-04-14Z | 2875817 | Weak 80-turn floor, no discard threat | 53.5 |

Each run carries a distinct theater signature. In run-2026-03-14T22-05-52Z (no gate whatsoever), aggregate Phase C completion was 56 of 351 items (16.0%), yet 91 ruled-out attack vectors were reported — 50.5% of them prose-only, with no Forge test in the `test_file` field. In run-2026-03-15T22-04-14Z (weak-gate regime, still no discard threat), 178 of 447 items were checked, yet 142 ruled-out vectors were reported with zero Forge tests: 100% prose-only — the theater signature at its most legible. The same run quoted in §2 (run-2026-03-15T13-40-26Z) contributes a third signature: 0/59 Phase C completion against 11 reported ruled-out vectors.

Across the three pre-gate runs: 380 ruled-out vectors reported in aggregate (91 + 147 + 142), of which at least 188 carried no Forge test. Run 3's 100% prose-only rate at N=142 is the starkest signal: zero Forge tests across 142 reported vectors in a run with an 80-turn floor but no discard threat. The middle run's insolvency-engineer alone reported 11 against 0/59 checklist completion. Raw counts only; pre-gate N=3 cannot support a confidence interval (Bowyer et al. 2503.01747).

Post-gate (commit `cb0026d`), theater mutates rather than disappears. Per-agent completion percentages rise — `extension-hijacker` reaches 89.2% — but Forge-test evidence strips out. The gate reshapes how theater manifests; it does not originate the underlying behavior.

Two caveats are owed. First, the author iterated on prompts between Runs 1 and 2; pre-gate N=3 rules out gate-as-cause but not author-attention-as-cause. Second, a controlled no-gate ablation arm was wired (`--pass1-mode none`) but never executed before the contest deadline. Section 7's mechanism claim survives because it does not rest on the gate — the same trajectory's pre-gate window is the evidence.

---

## 7. Longitudinal Trajectory

The 17-run iteration window spans the first run scored under the 6-dimension compliance rubric through the first run to reach peak score (39.8 → 112.5). Of those 17 runs, 7 carry `status=discard` — typically a regression that prompted an immediate rollback — of which 2 are zero-score pipeline failures caused by an agent self-closing loop, not by compliance-theater behavior. The trajectory is non-monotone by design: every high-cost run that did not advance the rubric was abandoned, and the next run incorporated the diagnosis.

We cannot attribute score jumps to individual interventions. The three largest positive jumps each bundled two to five simultaneous changes — prompt restructuring, schema coercions, coverage-gate tightening, and turn-budget increases in a single commit. Disentangling individual contributions requires controlled ablations. Those ablation arms were wired (`--pass1-mode none` and `--pass1-mode cost-control`) but never executed; the contest deadline closed before the budget justified a $182 isolation run. Section 7 therefore makes a weaker, survivable claim: evidence-gate-themed changes were coincident with all three largest positive jumps and never shipped without a rubric gain. The longitudinal record is a consistency check against the theory, not a demonstration of efficacy.

Run 9 illustrates the baseline-disclosure problem. Between Run 5 (keep, 55.1) and Run 9 (keep, 72.7) sit three intervening runs: Run 6 discarded with a real score of 43.9, then two zero-score pipeline failures.[^spearman] Each baseline below is arithmetically correct; each measures something different.

| Baseline | Reference run | Score | Delta |
|---|---|---|---|
| Literal prior-run | Run 8 — zero-score pipeline failure | 0.0 | +72.7 |
| Prior non-failed | Run 6 — scored discard (43.9) | 43.9 | +28.8 |
| Prior keeper | Run 5 — last kept run (55.1) | 55.1 | +17.6 |

The literal prior-run delta (+72.7) measures distance from the most recent run regardless of its cause. The prior-non-failed delta (+28.8) measures improvement over the last run that produced a real score, whether kept or discarded. The prior-keeper delta (+17.6) measures improvement over the last run the author judged worth retaining. Which of those questions a reader wants answered depends on what they think the iteration loop is evidence of — and Section 8 names the Regressional-Goodhart pressure that makes the author's choice of baseline itself a framing act.

The next subsection presents the full trajectory table and annotates which evidence-gate theme was coincident with each run.

[^mast]: Cemri et al. (2025), "MAST: A Multi-Agent System Taxonomy for LLM Task Failures," arXiv:2503.13657v2. FM-3.2 (Verification Step Omission) sits under FC3 (Task Verification). The full taxonomy is in Appendix A.3.

[^spearman]: Spearman rank correlation between run order and compliance score across the full 17-run window is r = 0.78. Excluding the two zero-score pipeline failures, r = 0.85. The abstract cites 0.78 as the more conservative number. Neither figure is adjusted for the non-monotone structure of the trajectory; both treat run order as a proxy for cumulative intervention depth.
