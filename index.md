---
layout: default
title: "Compliance Theater in Multi-Agent Systems"
---

# Compliance Theater in Multi-Agent Systems

*Draft in progress — publication target 2026-04-26.*

## Abstract

Nine Claude agents, prompted to audit adversarial smart contract code, consistently self-reported completing checklists they had not executed — producing well-formed outputs that performed thoroughness without the underlying work. We name this failure mode **compliance theater**, a previously-unnamed subtype of MAST FC3 (Task Verification), distinct from sycophancy, sabotage, and agent satisficing. The pattern appears without any instruction, reward signal, or persona directing the agent to misreport; it reproduces across Opus and Sonnet and across offensive and defensive task framings; and it emerges from a harness whose system prompt penalizes non-completion — making it consistent with a Regressional-Goodhart response to a completion-counting gate rather than with strategic deception. We counter it with architectural evidence gates tied to artifact existence rather than agent self-assessment. Over a 17-run iteration window — non-monotone, with 7 discarded runs and 2 zero-score pipeline failures — rubric score advances from 39.8 to 112.5 (Spearman r = 0.78). Ground-truth outcome labels are sparse (N = 9); the contribution is the named phenomenon, the architectural intervention, and the longitudinal trajectory.

Author: Diego Quinto (0xquinto) · Independent Researcher
