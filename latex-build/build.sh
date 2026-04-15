#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")"

# Prefix YAML frontmatter with natbib nocite directive so every bib entry appears.
{
  echo '---'
  echo 'header-includes: |'
  echo '  \usepackage[authoryear,round,sort&compress]{natbib}'
  echo '  \bibliographystyle{plainnat}'
  echo '---'
  echo ''
  sed -e '/^# Compliance Theater in a Multi-Agent/d' \
      -e '/^Author: Diego Gomez.*Independent Researcher$/d' \
      ../index.md
  echo ''
  echo '\nocite{*}'
} > main-source.md

# Strip the [^mast] footnote definition BEFORE converting inline [^mast] refs
# (so the deletion regex matches the original definition syntax, not the post-conversion form)
perl -i -0pe 's/^\[\^mast\]:[^\n]*\n\n?//gsm' main-source.md

# Convert inline citations to pandoc-natbib syntax (LaTeX-only; index.md unchanged for Jekyll).
perl -i -pe '
  # Parenthetical cites — replace entire paren with [@key] (escape @ so perl does not interpolate)
  s/\(Chen 2025, arXiv:2511\.05524\)/[\@chen2025evibound]/g;
  s/\(Manheim & Garrabrant 2018, arXiv:1803\.04585\)/[\@manheim2018goodhart]/g;
  s/\(Bowyer et al\. 2503\.01747\)/[\@bowyer2025smalln]/g;

  # Name-prefix cites — replace "Author et al. (arXiv:XX)" with textual @key
  s/Sharma et al\. \(arXiv:2310\.13548\)/\@sharma2023sycophancy/g;
  s/Perez et al\. \(arXiv:2212\.09251\)/\@perez2022sycophancy/g;
  s/Bowyer et al\. \(arXiv:2503\.01747\)/\@bowyer2025smalln/g;

  # SHADE-Arena: paper name is literal, append bracketed cite
  s/SHADE-Arena \(arXiv:2506\.15740\)/SHADE-Arena [\@shadearena2025]/g;

  # MAST: footnote [^mast] becomes inline cite (content is redundant with in-text prose)
  s/\[\^mast\]/ [\@cemri2025mast]/g;
' main-source.md

rm -rf assets && cp -r ../assets .

pandoc main-source.md -s -o main.tex \
  --top-level-division=section \
  --metadata title="Compliance Theater in a Multi-Agent Security Audit Harness: A Case Study" \
  --metadata author="Diego Gomez (0xquinto), Independent Researcher" \
  --metadata date="April 2026" \
  -V mainfont="TeX Gyre Termes" \
  -V sansfont="TeX Gyre Heros" \
  -V monofont="DejaVu Sans Mono" \
  -V geometry:margin=0.9in \
  -V linestretch=1.1 \
  --include-in-header=preamble.tex \
  --natbib \
  --bibliography=references.bib \
  -V biblio-style=plainnat \
  --pdf-engine=xelatex

perl -i -pe 's/✓/{\\dejavusans ✓}/g; s/✗/{\\dejavusans ✗}/g; s/κ/{\\dejavusans κ}/g; s/≥/{\\dejavusans ≥}/g; s/≠/{\\dejavusans ≠}/g; s/×/{\\dejavusans ×}/g; s/→/{\\dejavusans →}/g; s/±/{\\dejavusans ±}/g; s/·/{\\dejavusans ·}/g; s/§/{\\dejavusans §}/g' main.tex

# Wrap Abstract subsection in proper abstract environment (NeurIPS-style indent)
perl -i -0pe 's/\\subsection\{Abstract\}\\label\{abstract\}/\\begin{abstract}/; s/(?=\\subsection\{2\. The Phenomenon)/\\end{abstract}\n\n/' main.tex

docker run --rm -v "$(pwd):/work" -w /work texlive/texlive:latest-full \
  latexmk -xelatex -interaction=nonstopmode main.tex 2>&1 | tail -5

cp main.pdf ../compliance-theater.pdf
echo "→ ../compliance-theater.pdf ($(wc -c < ../compliance-theater.pdf) bytes)"
