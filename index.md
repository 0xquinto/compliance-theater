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

## 7. Longitudinal Trajectory

The 17-run iteration window spans the first run scored under the 6-dimension compliance rubric through the first run to reach peak score (39.8 → 112.5). Of those 17 runs, 7 carry `status=discard` — typically a regression that prompted an immediate rollback — and 2 are zero-score pipeline failures caused by an agent self-closing loop, not by compliance-theater behavior. The trajectory is non-monotone by design: every high-cost run that did not advance the rubric was abandoned, and the next run incorporated the diagnosis.

We cannot attribute score jumps to individual interventions. The three largest positive jumps each bundled two to five simultaneous changes — prompt restructuring, schema coercions, coverage-gate tightening, and turn-budget increases in a single commit. Disentangling individual contributions requires controlled ablations. Those ablation arms were wired (`--pass1-mode none` and `--pass1-mode cost-control`) but never executed; the contest deadline closed before the budget justified a $182 isolation run. Section 7 therefore makes a weaker, survivable claim: evidence-gate-themed changes were coincident with all three largest positive jumps and never shipped without a rubric gain. The longitudinal record is a consistency check against the theory, not a demonstration of efficacy.

Run 9 illustrates the baseline-disclosure risk directly. Its score of 72.7 is a gain of +17.6 vs. the prior keeper (55.1, Run 5). The literal prior-run delta is +72.7 — Runs 6–8 were a 43.9-point discard and two zero-score pipeline failures.[^spearman] A reviewer reconstructing the trajectory from experiments.tsv will see +72.7 as the arithmetic difference and reasonably flag it as the headline jump. The honest figure is +17.6 against the last non-failed run; Section 8 names the Regressional-Goodhart pressure that makes this framing choice itself a form of inadvertent goalpost movement.

The next subsection presents the full trajectory table and annotates which evidence-gate theme was coincident with each run.

[^spearman]: Spearman rank correlation between run order and compliance score across the full 17-run window is r = 0.78. Excluding the two zero-score pipeline failures, r = 0.85. The abstract cites 0.78 as the more conservative number. Neither figure is adjusted for the non-monotone structure of the trajectory; both treat run order as a proxy for cumulative intervention depth.
