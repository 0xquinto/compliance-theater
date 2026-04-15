# compliance-theater

Source for the paper *Compliance Theater in a Multi-Agent Security Audit Harness: A Case Study*.

**Read online:** https://0xquinto.github.io/compliance-theater/
**Download PDF:** [`compliance-theater.pdf`](compliance-theater.pdf)

## Contents

- `index.md` — paper source (Markdown + Jekyll frontmatter)
- `compliance-theater.pdf` — rendered paper (canonical citeable artifact)
- `assets/` — trajectory figure (`trajectory.png`) and reproducible render script (`render_trajectory.py`)
- `latex-build/` — reproducibility recipe for the PDF (pandoc + xelatex via Docker)
- `_config.yml` — Jekyll config for GitHub Pages

## Reproducing the PDF

The committed `compliance-theater.pdf` is the canonical artifact. To rebuild it from sources and verify reproducibility:

```
cd latex-build && bash build.sh
```

Overwrites `compliance-theater.pdf` at repo root. Requires Docker (uses `texlive/texlive:latest-full`).

## Licenses

- Prose: [CC-BY 4.0](LICENSE-prose.txt)
- Code snippets: [MIT](LICENSE-code.txt)
