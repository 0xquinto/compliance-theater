# compliance-theater

Source for the paper *Compliance Theater in a Multi-Agent Security Audit Harness: A Case Study*.

**Read online:** https://0xquinto.github.io/compliance-theater/
**Download PDF:** [`compliance-theater.pdf`](compliance-theater.pdf)

## Contents

- `index.md` — paper source (Markdown + Jekyll frontmatter)
- `compliance-theater.pdf` — rendered paper (canonical citeable artifact)
- `assets/` — trajectory figure (`trajectory.png`) and reproducible render script (`render_trajectory.py`)
- `latex-build/` — reproducibility recipe for the PDF (pandoc + xelatex via Docker)
- `irr-pilot/` — inter-rater reliability pilot (scoring protocol, annotator instructions)
- `_config.yml` — Jekyll config for GitHub Pages

## Reproducibility harness

The harness the paper anchors its empirical claims on lives at:

**https://github.com/0xquinto/compliance-theater-harness**

Every paper anchor (§2 vivid example, §4 pre-gate counts, §5 ablation matrix, §6 rubric + trace-analyzer, §7 trajectory + evidence-gate commits) resolves to a file in that repo. See its `README.md` for per-anchor reproduction commands.

## Reproducing the PDF

The committed `compliance-theater.pdf` is the canonical artifact. To rebuild it from sources and verify reproducibility:

```
cd latex-build && bash build.sh
```

Overwrites `compliance-theater.pdf` at repo root. Requires Docker (uses `texlive/texlive:latest-full`).

## Contributors

See [CONTRIBUTORS.md](CONTRIBUTORS.md). Sole author: Diego Gomez. Drafted with a specialized seven-agent Claude team under direct author guidance — agent role definitions are published at `.claude/agents/thesis-*.md`.

## Licenses

- Prose: [CC-BY 4.0](LICENSE-prose.txt)
- Code snippets: [MIT](LICENSE-code.txt)
