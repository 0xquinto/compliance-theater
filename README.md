# compliance-theater

Source for the paper *Compliance Theater in a Multi-Agent Security Audit Harness: A Case Study*.

**Read online:** https://0xquinto.github.io/compliance-theater/

## Contents

- `index.md` — paper source (Markdown + Jekyll frontmatter)
- `assets/` — trajectory figure (`trajectory.png`) and reproducible render script (`render_trajectory.py`)
- `latex-build/` — reproducible LaTeX PDF build recipe (pandoc + xelatex via Docker)
- `_config.yml` — Jekyll config for GitHub Pages

## Build PDF locally

```
cd latex-build && bash build.sh
```

Produces `compliance-theater.pdf` at repo root. Requires Docker (uses `texlive/texlive:latest-full`).

## Licenses

- Prose: [CC-BY 4.0](LICENSE-prose.txt)
- Code snippets: [MIT](LICENSE-code.txt)
