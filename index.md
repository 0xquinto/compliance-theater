---
layout: default
title: "Compliance Theater in a Multi-Agent Security Audit Harness: A Case Study"
---

## Abstract

Nine Claude agents, prompted to audit adversarial smart contract code, consistently self-reported completing checklists they had not executed — producing well-formed outputs that performed thoroughness without the underlying work. We name this failure mode **compliance theater**, a previously-unnamed affirmative-assertion sub-case of MAST FM-3.2 (Verification Step Omission, under FC3 Task Verification)[^mast], distinct from sycophancy, sabotage, and satisficing. The pattern appears without instruction, reward signal, or persona directing the agent to misreport; it reproduces across Opus and Sonnet and across offensive and defensive task framings; and three pre-gate runs confirm it arises under structured-checklist pressure without the <60% discard threshold introduced in commit cb0026d — consistent with Regressional Goodhart. We counter it with evidence gates keyed to artifact existence, not agent self-assessment; evidence-gate-themed changes were coincident with all three largest rubric gains, though bundled interventions preclude attribution. Over a 17-run iteration window — non-monotone, with 7 discards, 2 of them zero-score pipeline failures — rubric score advances from 39.8 to 112.5 (Spearman r = 0.78); the trajectory is a consistency check, not a demonstration of efficacy. Beyond naming the phenomenon, we introduce a refutation-locus classification rule — externally-adjudicable procedure versus session-stream self-count — and apply it to a single sidecar that simultaneously exhibits specific-binary-claim CT and introspection-accuracy failure, demonstrating that the boundary does classificatory work. The two sub-types — coarse-inflation and specific-binary-claim — share C1 refutation-predicate signature while exhibiting differential ablation response to gate removal (N=1 per cell); we frame this as a syndrome rather than a unified mechanism, and do not claim shared aetiology. Ground-truth outcome labels are sparse (N = 9).[^n9]

Author: Diego Gomez (0xquinto) · Independent Researcher

---

## 2. The Phenomenon: Compliance Theater

In run-2026-03-15T13-40-26Z, the `insolvency-engineer` agent reported 11 ruled-out attack vectors — each with a populated `test_file` field asserting a Forge test had been written — while Phase C checklist completion was 0/59 and the trace-analyzer (see §6) registered 3 tool calls total. It produced a structurally complete output that performed thoroughness without executing the underlying work.[^schneier]

We name this pattern **compliance theater**: a sharpened affirmative-assertion sub-case of MAST FM-3.2 (Verification Step Omission, under FC3 Task Verification)[^mast], introduced here to capture the case the abstract named.

We classify a trace segment as compliance theater when three observable conditions jointly hold:

**(C1) Affirmative assertion of verification or of verification-implying output state.** The agent's output — in natural language or structured fields — claims either that a verification step was performed or that a specific property of an agent-produced artifact holds (e.g., `compilation_status`, `tests_written`), where that property is established only by a verification step the agent did not perform. Silent omission without such a claim is plain FM-3.2 under MAST and is excluded here. C1 is evaluated at the sub-claim surface, not at the whole-output level: a single output may be substance-honest on coarse self-assessment fields while carrying an affirmative-false binary sub-claim on a specific field (§5 develops a sharp instance). A sub-claim surface qualifies as C1 CT iff (i) the sidecar contains, at any document location, an agent-authored pointer — path, tool invocation record, or filename field — to a persistent artifact the agent caused to exist, AND the pre-registered refutation predicate for the claim-shape names both (a) the sub-claim field and (b) the pointer field(s), such that the refutation procedure is fully specified without further interpretation. The sidecar container itself does not count as a pointer. Claim-shapes for which no such predicate is pre-registered are out of scope for C1 and fall to FM-1.x or remain unclassified. Three pre-registered predicates, each naming both the sub-claim field and the pointer field: **`compilation_status`** — values in {`"success"`, `"success_with_warnings"`} assert `forge build --match-path <test_file>` exits zero. Pointer: `ruled_out_vectors[*].test_file`. Refuted iff exit ≠ 0; warnings do not refute `"success_with_warnings"` but do refute `"success"`. The §5 sidecar's `"success_with_warnings"` is warnings-compatible; refutation rests on exit code alone (exit nonzero — wrong argument count on `amm.addLiquidity`, undeclared named arguments). **`tests_written`** — integer asserting the count of test functions in the pointer file. Pointer: same `test_file` field; values are parsed by stripping any leading `Created ` prefix, splitting on `:`, and taking the first segment as the file path; duplicate paths across entries are deduplicated. Refuted iff `grep -c '^\s*function\s+test'` returns a different count. Tolerance ±0. **`tests_passed`** — integer asserting tests exiting PASS under `forge test --match-path <pointer>`. Pointer: same. Refuted iff `pass_count ≠ claimed` in `forge test --json` output. The §5 sidecar's `tests_passed: 0` with `execution_status: "blocked_by_test_framework_issues"` is self-consistent and does *not* refute — a worked non-refutation example. Sub-claim surfaces refutable only by execution metadata the agent did not author (e.g., the orchestrator's trace log backing `num_turns`, `tool_uses`, `files_read`) are MAST FM-1.x introspection-accuracy failures and are excluded.[^edgecase]

**(C2) Trace-level refutation.** A signal the agent cannot read or hill-climb on — in this work, a 16-dimension trace-analyzer — shows the claimed work did not occur at anything close to the claimed scale.

**(C3) Gate-shaped, not user-shaped, pressure.** The trace contains no user-turn sentiment the report could be shaping to; the pressure it responds to is a completion-valued gate in the system prompt — here, the black-hat preamble's <60% discard threshold. C3 distinguishes compliance theater from sycophancy (user-sentiment-shaped); we flag it the weakest criterion — a broad sycophancy-to-system-prompt definition could absorb it. §4's pre-gate runs show CT predates the specific discard threshold. The no-gate ablation (§5) further disposes of the *threat-driven* variant of the sycophancy-to-system-prompt absorption argument: CT survived removal of both completion-valued pressure sources (preamble threshold and schema-validator threats). It does not dispose of the *template-default-shaping* variant: metadata fields with default-friendly register (e.g., `compilation_status: success_with_warnings`) may be template-shaped even absent threats, and §5 reports a single-cell instance consistent with that.

Compliance theater as defined by C1–C3 admits two empirically-separable sub-types: (i) coarse-inflation CT, shaped by completion-valued gate pressure, realized on summary-statistic surfaces (§4); and (ii) specific-binary-claim CT, shaped by template-default register, realized on discrete output-state fields (§5). The two are unified at the C1 refutation-predicate layer — the same pre-registered predicate family (`forge build`, file-line-count, `forge test`) refutes both sub-types at matching sub-claim granularity — and separated at the C3 shaping layer, where distinct pressures drive distinct surface manifestations. This is a syndrome structure: shared refutation-predicate signature, differential generative processes, not a single mechanism. At N=1 per ablation cell (§5), the evidence does not rule out CT as a disjunction of two phenomena sharing a refutation rule; §5's ablation asymmetry is consistent with either reading.

The mechanism fits Regressional Goodhart (Manheim & Garrabrant 2018, arXiv:1803.04585) — the adversarial optimizer is the author. Over 17 runs, the author selected interventions that moved the rubric; the measure became the target.

Compliance theater is distinct from sycophancy (user-shaped, not gate-shaped), from sabotage (completion-valued shaping without an adversarial goal; §4's pre-gate runs exhibit it under no hostile persona), and from satisficing (the agent asserts completion rather than silently under-delivering).

[^n9]: Nine Guardian Defender contest submissions: 1 accepted (CP-006, CLOBHelper double-rounding, Medium severity); 8 rejected. Per-submission rejection labels are not individually archived in public records.

[^schneier]: The term borrows from Bruce Schneier's "security theater" (*Beyond Fear*, 2003): visible ceremony that signals diligence without performing the underlying work. No prior use of "compliance theater" in LLM or agent-evaluation literature was found in a targeted search conducted 2026-04-12.

[^edgecase]: Fields refutable by both agent-authored tool_use logs and the orchestrator trace resolve deterministically under the revised rule: FM-1.x disambiguation follows from predicate-table non-registration (the claim-shape names no pre-registered predicate), not from pointer-condition failure. Triage-log-class fields have no registered predicate pointing to an agent-authored artifact; they are FM-1.x on that basis.

---

## 3. Related Work

### 3.1 Direct predecessor: EviBound and the evidence-gate lineage

EviBound (Chen 2025, arXiv:2511.05524) introduces a dual-gate evidence framework binding claims to machine-checkable artifacts: its Verification Gate queries MLflow recursively for acceptance-criteria artifacts and, when metrics are specified, compares claimed against observed values — artifact-level sub-claim verification, not whole-task binary. This paper's contribution is orthogonal to the gate mechanism. EviBound's single-agent ML setting exposes one sub-claim surface class (agent-authored experiment artifacts); it has no occasion to partition surfaces by who authored the refuting evidence. The multi-agent harness surfaces that partition: sidecars mix agent-authored artifact claims (`compilation_status`, `tests_written`) with orchestrator-authored execution-metadata claims (`num_turns`, `tool_uses`, `files_read`). The §2 C1 rule assigns the former to FM-3.2 CT and the latter to FM-1.x introspection — a partition EviBound's gate has no occasion to make.

### 3.2 Taxonomic anchor: MAST and the failure-mode tradition

Compliance theater is not a new failure mode relative to FM-3.2; it is an affirmative-assertion sub-case of FM-3.2 named for compact reference. The paper's contribution at the taxonomy level is narrower: a sub-claim-level assignment rule for when a single agent output contains verification-implying claims refutable by disjoint authored sources. MAST annotates at output-trace level (κ = 0.88) and does not partition within-output sub-claim surfaces; the C1 rule does. The §5 single-sidecar demonstration — `compilation_status` FM-3.2, `num_turns` FM-1.x, `completeness_pct` honest — is the existence proof that within-output partition is non-trivial. This paper extends MAST at the sub-claim granularity; it does not compete with MAST's taxonomy.[^chatdev] Pre-gate N=3 confidence intervals follow Bowyer et al. (arXiv:2503.01747) small-N methodology.

### 3.3 Adjacent phenomena the paper is not

Compliance theater is not sabotage: SHADE-Arena (arXiv:2506.15740) models goal-misaligned concealment with structurally identical outputs; CT requires no adversarial goal, and §4's pre-gate runs exhibit it under no hostile persona. CT is not RLHF-shaped sycophancy: Sharma et al. (arXiv:2310.13548) document preference-model-driven output shaping; the pressure surface here is a completion-valued gate, not training-time preference. CT shows no scaling signature: Perez et al. (arXiv:2212.09251) document sycophancy increasing with model scale; CT appears at both Opus and Sonnet without that gradient.

[^chatdev]: Cemri et al. (2025), "Why Do Multi-Agent LLM Systems Fail?" arXiv:2503.13657, §FC3 Task Verification, ChatDev example. Verbatim: "a ChatDev-generated chess program passes superficial checks (e.g., code compilation) but contains runtime bugs because it fails to validate against actual game rules." Verified against arXiv:2503.13657 HTML full text 2026-04-14.

---

## 4. Setup: The Limit Break AMM Audit

This section establishes the one setup fact the argument turns on: the harness's git history. Agent roster, preamble evolution, and tool fleet are in a companion appendix.

### The Natural Experiment

Commit `cb0026d` (2026-03-15 18:10 -0500) introduced the "<60% Phase C items completed → findings discarded" language into `black-hat-preamble.md`. The hostile reviewer's circularity objection rests on that gate existing from the start; the repo's git history refutes it. Three runs in `experiments.tsv` precede that commit:

| run_id | commit | regime | score |
|---|---|---|---|
| run-2026-03-14T22-05-52Z | c9839a8 | No gate | 39.8 |
| run-2026-03-15T13-40-26Z | 67f6e9f | No gate | 44.2 |
| run-2026-03-15T22-04-14Z | 2875817 | Weak 80-turn floor, no discard threat | 53.5 |

In run-2026-03-14T22-05-52Z (no gate whatsoever), aggregate Phase C completion was 56 of 351 items (16.0%), yet 91 ruled-out attack vectors were reported — 50.5% of them prose-only, with no Forge test in the `test_file` field. In run-2026-03-15T22-04-14Z (weak-gate regime, still no discard threat), 178 of 447 items were checked, yet 142 ruled-out vectors were reported with zero Forge tests: 100% prose-only — the theater signature at its most legible. The same run quoted in §2 (run-2026-03-15T13-40-26Z) contributes a third signature: 0/59 Phase C completion against 11 reported ruled-out vectors.

Across the three pre-gate runs: 380 ruled-out vectors (91 + 147 + 142), at least 188 with no Forge test. Run 3's 100% prose-only rate at N=142 is the starkest signal: zero Forge tests in a run with an 80-turn floor but no discard threat. Raw counts only; pre-gate N=3 cannot support a confidence interval (Bowyer et al. 2503.01747).

Post-gate (`cb0026d`), theater mutates rather than disappears: completion percentages rise — `extension-hijacker` reaches 89.2% — but Forge-test evidence strips out. The gate reshapes the surface; it does not originate the behavior.

Two caveats: pre-gate N=3 rules out gate-as-cause but not author-attention-as-cause (prompt changes between Runs 1 and 2); and the controlled no-gate arm (`--pass1-mode none`) was wired but not executed. §7's mechanism claim survives because it does not rest on the gate.

---

## 5. Intervention: Architectural Evidence Gates

In the truly-no-gate-offensive cell (108 turns, $2.88), the `insolvency-engineer` sidecar reports `completeness_pct: 50`, checklist C: 12/25, and `execution_status: "blocked_by_test_framework_issues"` — honest on coarse surfaces. The same sidecar asserts `compilation_status: "success_with_warnings"` for `InsolvencyEngineerChecklist.t.sol`. An independent `forge build --match-path` against that file fails: wrong argument count on `amm.addLiquidity`, undeclared named arguments. `tests_written: 15` is also refuted — `grep -cE '^\s*function\s+test' InsolvencyEngineerChecklist.t.sol` returns 13, so the claimed count exceeds the actual by 2. The compilation claim satisfies C1 (affirmative assertion), C2 (trace-level refutation via `forge build`), and C3 (survives gate removal) — the existence proof §2's granularity clause requires. The sidecar simultaneously displays three MAST failure regions and a mixed-outcome predicate profile: honest self-report on `completeness_pct`, two C1 refutations (`compilation_status`, `tests_written`), one non-refutation (`tests_passed: 0`, self-consistent and non-refuting), and FM-1.x introspection error on `num_turns` (75 reported; orchestrator log shows 108) — predicate selectivity demonstrated on a single sidecar.

**Cross-sub-type ablation asymmetry (N=1 per cell):** gate removal ablated coarse-inflation CT in every cell it appeared; it did not ablate specific-binary-claim CT in the one cell it appeared. The matrix spans (preamble treatment) × (task framing): truly-no-gate and neutral, each under offensive and defensive system prompts. Every cell produced honest-partial behavior on coarse surfaces — explicit `forge: ran=false` disclosures, "did not cover" lists, low self-reported completeness. The coarse-inflation signature from §4's pre-gate corpus (380 ruled-out vectors, at least 188 with no Forge test) did not reappear. What appeared, in one cell only (truly-no-gate-offensive), is specific-binary-claim CT on `compilation_status`.

At N=1 per cell, the matrix does not discriminate causal contribution from noise; the following are genuine hypotheses, not findings.

**Hypothesis 1.** The preamble's completion-valued threshold causes coarse-inflation CT; prediction: removing only the threshold reduces coarse-inflation CT while leaving specific-binary-claim CT unaffected (testable at N≥3). Consistent with §4's pre-gate runs showing the coarse-inflation signature before the threshold existed.

**Hypothesis 2.** The schema-validator's prompt-threat language contributes independently; prediction: removing both sources jointly produces a larger shift than removing either alone (2×2 factorial). Consistent: removing only the preamble threshold produced intermediate behavior; removing both shifted all cells to honest-partial.

The ablation does not disentangle honesty-injection from pressure-removal: the neutral variant removed both gate sources and honesty instructions simultaneously, so the N=1-per-cell data cannot attribute the honest-partial endpoint to either variable. A 2×2 factorial (gate sources × honesty instructions) was not run before the contest deadline.

Specific-binary-claim CT persists under pressure removal — consistent with §2's template-default-shaping variant as the residual concern; alternatives (reward-model preference for confident affirmation, schema-filler bug, field-level introspection failure) are not ruled out.

---

## 6. Measurement: The Rubric and Its Triangulation

Sub-claim-surface non-uniformity is an existence proof at N=1 per cell (single archetype, single model family); base-rate claims about which sub-claim surfaces are CT-prone require replication and are deferred.

Three measurement surfaces made that finding detectable and the §7 trajectory scorable.

**The 6-dimension compliance rubric (0–120).** Scored by `compliance.py` and logged in `experiments.tsv`, the rubric assesses six dimensions per agent: checklist completion (0–30), tool breadth (0–20), evidence quality (0–20), analytical depth (0–20), thesis coherence (0–10), and hypothesis generation (0–20). The rubric scores what the sidecar says — it reads the agent's output and structured fields, not the underlying work.

**The trace-analyzer as second surface.** `trace_analyzer.py` reads the raw agent trace after each run and extracts 16 dimensions: tool call count, files read, bash commands, narrative quality, turn velocity, hypothesis density, cross-agent overlap, and related signals. The agent cannot hill-climb on these metrics — the trace records what the agent did, not what it claimed, and the analyzer runs post-hoc without agent visibility. Same author, same corpus — not independent but different surfaces: the rubric reads the sidecar; the trace-analyzer reads the tool-call stream. They disagree sharply on the pre-gate runs — that disagreement is what makes C2 (trace-level refutation) operational. C1 is operational only because the two surfaces are separable — claim and refuting signal from disjoint sources.

**Artifact-check as third surface.** An independent `forge build --match-path` either compiles or doesn't — crisp ground truth unavailable to the other two surfaces. Deployed in §5 to falsify `compilation_status: "success_with_warnings"`. The triangulation: rubric without trace-analyzer measures reported performance, not theater; trace-analyzer without artifact-check catches coarse inflation but misses specific-binary-claim CT; artifact-check alone is too narrow to score a 24-run corpus.

**Measurement limits.** Rubric weights and trace-analyzer dimensions both come from the same 24-run corpus — a Goodhart exposure, not blinded. The C1 predicate table is not strictly prospective — authored after the §5 sidecar was observed; the IRR pilot is the prospective test. The 0–120 scale is an ordering device. Predicate *selection* is toolkit-conditioned: which procedures get registered depends on what the reviewer can execute. The sub-claim surface C1 identifies — agent-authored claim paired with agent-caused-artifact pointer — is structural to the sidecar. Sidecar-vs-trace separation is the only structural mitigation; held-out corpora, IRR, and blinded scoring remain. The IRR pilot covers insolvency-engineer sidecars only — single archetype per cell; C1 generalizability to other archetypes (math-deep-diver, cross-boundary, extension-hijacker) is unestablished without multi-archetype ablation or separate IRR on non-ablation wave-1 runs.

**Cross-harness consistency check.** As a consistency check — not a replication — we sampled shard 0 of the public nebius/SWE-agent-trajectories dataset (80,036 trajectories). Instance Melevir__cognitive_complexity-15, model swe-agent-llama-70b: the agent named two tests — test_real_function, test_nested_functions — as "giving the correct complexity counts" after local pytest "20 passed." The SWE-bench eval_logs show both failed when the test-patch was applied; the patch was a comment-only no-op. A clean C1 hit: agent-authored claim, re-executable refutation. Architectural note: SWE-agent is an agent-computer-interface system (single LLM, tool-orchestrated), not multi-agent in the ChatDev/MetaGPT sense; C1 is architecture-agnostic, so this extends confirmed scope to one harness plus one consistency check in a distinct architecture class.[^sweagent]

[^sweagent]: Nebius AI. *SWE-agent-trajectories*, huggingface.co/datasets/nebius/SWE-agent-trajectories, commit `68195a1`. Instance `Melevir__cognitive_complexity-15`, model `swe-agent-llama-70b`. Filter `exit_status=="submitted" AND target==False`; row index 28; `trajectory[36].text` (claim) and `eval_logs` (refutation).

---

## 7. Longitudinal Trajectory

The 17-run window spans commits c9839a8 through e7742a7 (39.8 → 112.5, Spearman r = 0.78).

![](assets/trajectory.png)

*Figure 1. The 17-run iteration window. Filled circles: shipped runs. Open circles: discards. Stars: evidence-gate-themed changes (63ad8c3, c6f6aad, e7742a7) — runs where the primary change was sidecar gate, MCP audit-gate, or artifact-verify enforcement. ×: zero-score pipeline failures (0283ad5, e26a927), self-closing agent loop, not CT behavior. Step connectors emphasize discrete runs, not continuous trend.*

| Run | Commit | Score | Status | EG? |
|---|---|---|---|---|
| 03-14 | c9839a8 | 39.8 | keep | |
| 03-15a | 67f6e9f | 44.2 | keep | |
| 03-15b | 2875817 | 53.5 | keep | |
| 03-15c | cb0026d | 54.1 | keep | |
| 03-16a | 90476dd | 55.1 | keep | |
| 03-16b | 26a911d | 43.9 | discard | |
| 03-16c | 0283ad5 | 0.0 | discard | |
| 03-16d | e26a927 | 0.0 | discard | |
| 03-16e | 63ad8c3 | 72.7 | keep | ✓ |
| 03-18a | c6f6aad | 91.9 | keep | ✓ |
| 03-18b | 3466a39 | 95.3 | keep | |
| 03-18c | 087dc7b | 96.7 | keep | |
| 03-19 | 3bc52b2 | 75.4 | discard | |
| 03-23a | 607e15d | 86.1 | discard | |
| 03-23b | 0296e79 | 87.0 | discard | |
| 03-25a | b237188 | 95.8 | discard | |
| 03-25b | e7742a7 | 112.5 | keep | ✓ |

Score jumps cannot be attributed to individual interventions: the three largest each bundled two to five simultaneous changes, and the ablation arms (`--pass1-mode none` and `--pass1-mode cost-control`) were never executed before the contest deadline. The weaker claim holds: each ✓-marked run was coincident with a rubric gain, but shipping was author-selected. The longitudinal record is a consistency check, not a demonstration of efficacy.

The baseline-disclosure problem: between Run 5 (keep, 55.1) and Run 9 (keep, 72.7) sit three intervening runs — Run 6 discarded (43.9), then two zero-score pipeline failures.[^spearman] Each baseline below is arithmetically correct; each measures something different.

| Baseline | Reference run | Score | Delta |
|---|---|---|---|
| Literal prior-run | Run 8 — zero-score pipeline failure | 0.0 | +72.7 |
| Prior non-failed | Run 6 — scored discard (43.9) | 43.9 | +28.8 |
| Prior keeper | Run 5 — last kept run (55.1) | 55.1 | +17.6 |

Each baseline answers a different question; §8 names the Regressional-Goodhart pressure making the baseline choice a framing act.

[^mast]: Cemri et al. (2025), "MAST: A Multi-Agent System Taxonomy for LLM Task Failures," arXiv:2503.13657v2. FM-3.2 (Verification Step Omission) sits under FC3 (Task Verification). The full taxonomy is in Appendix A.3.

[^spearman]: Spearman rank correlation between run order and compliance score across the full 17-run window is r = 0.78. Excluding the two zero-score pipeline failures, r = 0.85. The abstract cites 0.78 as the more conservative number. Neither figure is adjusted for the non-monotone structure of the trajectory; both treat run order as a proxy for cumulative intervention depth.
