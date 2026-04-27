# Contributors

## Author

- **Diego Gomez** ([@0xquinto](https://github.com/0xquinto)) — sole author. Owns the thesis (compliance theater as a named MAST FM-3.2 sub-case), the §2 vivid example, all rubric design choices, and every retraction or rewrite decision in the iteration history.

## AI tooling and writing collaboration

The paper was drafted by a specialized seven-agent Claude team operating under direct author guidance. Each agent has a single defined role; the role definitions are published in this repo at `.claude/agents/thesis-*.md` so reviewers can audit the production process.

| Agent | Role |
|---|---|
| `thesis-lead` | Coordinates review rounds, routes work between specialists, maintains the issues ledger |
| `thesis-technical-writer` | Sentence-level prose, paragraph logic, abstract craft |
| `thesis-hostile-reviewer` | Once-per-draft attack from a skeptical reviewer perspective; writes the rejection email |
| `thesis-methodology-critic` | Stress-tests rigor (N=9, trajectory defensibility, rubric-fitting checks) |
| `thesis-ai-safety-reviewer` | Multi-agent systems / AI safety positioning, related work, MAST FC3 anchor |
| `thesis-defi-translator` | DeFi/audit specifics for non-DeFi reviewers; Section 4 accuracy |
| `thesis-application-strategist` | Framing for Anthropic Fellows / Research Engineer applications |

The author owns intellectual content and final decisions throughout. The agents executed prose drafting, hostile review rounds, citation verification, and structural critique — they did not generate the thesis or the rubric design.

Specific Claude models: **Opus 4.7** (extended-context drafting and review across the agent team) and **Sonnet 4.5 / 4.6** (the model fleet inside the audit harness whose self-reports §2–§5 study).

## Methodological note on AI authorship

The paper makes empirical claims about Claude agents' self-report failures. It was drafted by Claude agents. This recursion is acknowledged here and the role definitions are published precisely so the C1 refutation procedure (§2) is applied to this artifact in §8: §5's hook is independently re-executable; §2 and §4 hooks point at canonical rubric-scorer output, since primary artifacts for those pre-gate runs were not preserved.

Authorship credits the argument's framing, not the writing assistance. Per current scholarly norms (NeurIPS, Science, ACM), LLMs are not listed as authors regardless of contribution depth; specific tooling use is disclosed in acknowledgments. This repo follows that convention.

## Reproducibility harness

The runnable artifact making the paper's empirical claims independently verifiable lives at:

**https://github.com/0xquinto/compliance-theater-harness** ([CONTRIBUTORS.md there](https://github.com/0xquinto/compliance-theater-harness/blob/main/CONTRIBUTORS.md))
