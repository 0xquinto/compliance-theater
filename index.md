---
layout: default
title: "Compliance Theater in Multi-Agent Systems"
---

# Compliance Theater in Multi-Agent Systems

*Draft in progress — publication target 2026-04-26.*

## Abstract

Nine Claude agents, prompted to audit adversarial smart contract code, consistently self-reported completing checklists they had not executed — producing well-formed outputs that performed thoroughness without the underlying work. We name this failure mode **compliance theater**, a previously-unnamed subtype of MAST FC3 (Task Verification), distinct from sycophancy, sabotage, and satisficing. The pattern appears without instruction, reward signal, or persona directing the agent to misreport; it reproduces across Opus and Sonnet and across offensive and defensive task framings; and three pre-gate runs (commit cb0026d, 2026-03-15) confirm it arises under structured-checklist pressure alone — consistent with Regressional Goodhart. We counter it with architectural evidence gates tied to artifact existence rather than agent self-assessment. Over a 17-run iteration window — non-monotone, with 7 discarded runs and 2 zero-score pipeline failures — rubric score advances from 39.8 to 112.5 (Spearman r = 0.78). Ground-truth outcome labels are sparse (N = 9); the contribution is the named phenomenon, the architectural intervention, and the longitudinal trajectory.

Author: Diego Quinto (0xquinto) · Independent Researcher

---

## 2. The Phenomenon: Compliance Theater

In run-2026-03-15T13-40-26Z, the `insolvency-engineer` agent reported 11 ruled-out attack vectors — each carrying a populated `test_file` field asserting a Forge test had been written — while its Phase C checklist completion was 0/59. The trace-analyzer registered 3 tool calls for the entire run. The agent did not execute the work it reported executing. It produced a structurally complete output that performed thoroughness.[^schneier]

We name this pattern **compliance theater**, a sharpened affirmative-assertion sub-case of FM-3.2 (Verification Step Omission) under MAST, introduced here to capture the case the abstract named.

We classify a trace segment as compliance theater when three observable conditions jointly hold:

**(C1) Affirmative assertion of verification.** The agent's output — in natural language or structured fields — claims that the verification was performed. Silent omission of verification, without such a claim, is plain FM-3.2 under MAST and is excluded here.

**(C2) Trace-level refutation.** An independent signal that the agent cannot read or hill-climb on — in this work, a 16-dimension trace-analyzer counting tool calls, files read, and bash commands — shows the claimed work did not occur at anything close to the claimed scale.

**(C3) Gate-shaped, not user-shaped, pressure.** The trace contains no user-turn sentiment the report could be shaping to; the pressure it responds to is a discrete completion-valued gate installed in the system prompt (here: the black-hat preamble's "<60% Phase C items discarded" rule). C3 distinguishes compliance theater from sycophancy, which shapes to user preference. We flag C3 as the weakest of the three: a broad definition of sycophancy-to-system-prompt could absorb it, and a controlled no-gate arm is required to settle the question. We treat the separation from sycophancy as provisional pending that ablation.

The mechanism fits Regressional Goodhart (Manheim & Garrabrant 2018, arXiv:1803.04585) — but the adversarial optimizer in the iteration loop is the author, not the agent. The agent responded naturally to shaping pressure. The author, across 17 runs, selected interventions that moved the rubric. The measure became the target; the author did the selecting.

Compliance theater is distinct from sycophancy (user-shaped, not gate-shaped — see C3), from sabotage (no misaligned intent), and from satisficing (the agent asserts completion rather than silently under-delivering).

[^schneier]: The term borrows from Bruce Schneier's "security theater" (*Beyond Fear*, 2003): visible ceremony that signals diligence without performing the underlying work. No prior use of "compliance theater" in LLM or agent-evaluation literature was found in a targeted search conducted 2026-04-12.

---

## 7. Longitudinal Trajectory

The 17-run iteration window spans the first run scored under the 6-dimension compliance rubric through the first run to reach peak score (39.8 → 112.5). Of those 17 runs, 7 carry `status=discard` — typically a regression that prompted an immediate rollback — and 2 are zero-score pipeline failures caused by an agent self-closing loop, not by compliance-theater behavior. The trajectory is non-monotone by design: every high-cost run that did not advance the rubric was abandoned, and the next run incorporated the diagnosis.

We cannot attribute score jumps to individual interventions. The three largest positive jumps each bundled two to five simultaneous changes — prompt restructuring, schema coercions, coverage-gate tightening, and turn-budget increases in a single commit. Disentangling individual contributions requires controlled ablations. Those ablation arms were wired (`--pass1-mode none` and `--pass1-mode cost-control`) but never executed; the contest deadline closed before the budget justified a $182 isolation run. Section 7 therefore makes a weaker, survivable claim: evidence-gate-themed changes were coincident with all three largest positive jumps and never shipped without a rubric gain. The longitudinal record is a consistency check against the theory, not a demonstration of efficacy.

Run 9 illustrates the baseline-disclosure risk directly. Its score of 72.7 is a gain of +17.6 vs. the prior keeper (55.1, Run 5). The literal prior-run delta is +72.7 — Runs 6–8 were a 43.9-point discard and two zero-score pipeline failures.[^spearman] A reviewer reconstructing the trajectory from experiments.tsv will see +72.7 as the arithmetic difference and reasonably flag it as the headline jump. The honest figure is +17.6 against the last non-failed run; Section 8 names the Regressional-Goodhart pressure that makes this framing choice itself a form of inadvertent goalpost movement.

The next subsection presents the full trajectory table and annotates which evidence-gate theme was coincident with each run.

[^spearman]: Spearman rank correlation between run order and compliance score across the full 17-run window is r = 0.78. Excluding the two zero-score pipeline failures, r = 0.85. The abstract cites 0.78 as the more conservative number. Neither figure is adjusted for the non-monotone structure of the trajectory; both treat run order as a proxy for cumulative intervention depth.
