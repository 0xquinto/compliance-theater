"""
render_trajectory.py — 17-run compliance score trajectory figure for §7.
Data source: experiments.tsv rows 1-17 (c9839a8 → e7742a7).
Reproducible: python3 assets/render_trajectory.py
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# ---------------------------------------------------------------------------
# Data — 17 runs in chronological order (top-to-bottom of experiments.tsv)
# ---------------------------------------------------------------------------
runs = [
    # (label,       commit,    score,  status,    evidence_gate, zero_score)
    ("03-14",    "c9839a8",  39.8,  "keep",    False, False),
    ("03-15a",   "67f6e9f",  44.2,  "keep",    False, False),
    ("03-15b",   "2875817",  53.5,  "keep",    False, False),
    ("03-15c",   "cb0026d",  54.1,  "keep",    False, False),
    ("03-16a",   "90476dd",  55.1,  "keep",    False, False),
    ("03-16b",   "26a911d",  43.9,  "discard", False, False),
    ("03-16c",   "0283ad5",   0.0,  "discard", False, True),
    ("03-16d",   "e26a927",   0.0,  "discard", False, True),
    ("03-16e",   "63ad8c3",  72.7,  "keep",    True,  False),
    ("03-18a",   "c6f6aad",  91.9,  "keep",    True,  False),
    ("03-18b",   "3466a39",  95.3,  "keep",    False, False),
    ("03-18c",   "087dc7b",  96.7,  "keep",    False, False),
    ("03-19",    "3bc52b2",  75.4,  "discard", False, False),
    ("03-23a",   "607e15d",  86.1,  "discard", False, False),
    ("03-23b",   "0296e79",  87.0,  "discard", False, False),
    ("03-25a",   "b237188",  95.8,  "discard", False, False),
    ("03-25b",   "e7742a7", 112.5,  "keep",    True,  False),
]

indices = list(range(1, len(runs) + 1))
labels  = [r[0] for r in runs]
scores  = [r[2] for r in runs]

# ---------------------------------------------------------------------------
# Figure setup
# ---------------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(10, 4), dpi=150)

# Step connector across all points (discrete, not smoothed)
ax.step(indices, scores, where="post", color="#555555", linewidth=1.0, zorder=1)

# ---------------------------------------------------------------------------
# Plot points by category (shape-primary, color-secondary for monochrome safety)
# ---------------------------------------------------------------------------
for i, (label, commit, score, status, eg, zero) in enumerate(runs):
    x = i + 1

    if zero:
        # Zero-score pipeline failure: ×  (red, distinct)
        ax.plot(x, score, marker="x", markersize=9, markeredgewidth=2.2,
                color="#cc2222", linestyle="none", zorder=4)

    elif eg:
        # Evidence-gate-themed run: filled circle + star overlay
        ax.plot(x, score, marker="o", markersize=8, markeredgewidth=1.2,
                color="#1a1a1a", markerfacecolor="#1a1a1a", linestyle="none", zorder=3)
        # Star overlay (slightly larger, hollow, prominent)
        ax.plot(x, score, marker="*", markersize=14, markeredgewidth=0.8,
                color="#f5a623", markerfacecolor="none", linestyle="none", zorder=5)

    elif status == "keep":
        # Kept run: filled circle
        ax.plot(x, score, marker="o", markersize=7, markeredgewidth=1.2,
                color="#1a1a1a", markerfacecolor="#1a1a1a", linestyle="none", zorder=3)

    else:
        # Discarded run (non-zero): open circle
        ax.plot(x, score, marker="o", markersize=7, markeredgewidth=1.8,
                color="#1a1a1a", markerfacecolor="white", linestyle="none", zorder=3)

# ---------------------------------------------------------------------------
# Reference gridlines at D-threshold (60) and A-threshold (90)
# ---------------------------------------------------------------------------
ax.axhline(60,  color="#aaaaaa", linewidth=0.8, linestyle="--", zorder=0)
ax.axhline(90,  color="#aaaaaa", linewidth=0.8, linestyle="--", zorder=0)
ax.text(17.35, 60,  "D (60)",  va="center", ha="left", fontsize=7.5, color="#888888")
ax.text(17.35, 90,  "A (90)",  va="center", ha="left", fontsize=7.5, color="#888888")

# ---------------------------------------------------------------------------
# Axes and ticks
# ---------------------------------------------------------------------------
ax.set_xlim(0.3, 18.0)
ax.set_ylim(-8, 125)
ax.set_xticks(indices)
ax.set_xticklabels(labels, fontsize=7.5, rotation=35, ha="right")
ax.set_xlabel("Run", fontsize=9)
ax.set_ylabel("Compliance score (0–120)", fontsize=9)
ax.tick_params(axis="y", labelsize=8)

# Light grid on y only
ax.yaxis.grid(True, color="#e0e0e0", linewidth=0.6, zorder=0)
ax.set_axisbelow(True)

# Remove top/right spines for cleaner look
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)

# ---------------------------------------------------------------------------
# Legend — compact, shape-primary
# ---------------------------------------------------------------------------
leg_keep    = mlines.Line2D([], [], marker="o", markersize=7, markeredgewidth=1.2,
                             color="#1a1a1a", markerfacecolor="#1a1a1a",
                             linestyle="none", label="Keep")
leg_discard = mlines.Line2D([], [], marker="o", markersize=7, markeredgewidth=1.8,
                             color="#1a1a1a", markerfacecolor="white",
                             linestyle="none", label="Discard")
leg_eg      = mlines.Line2D([], [], marker="*", markersize=12, markeredgewidth=0.8,
                             color="#f5a623", markerfacecolor="none",
                             linestyle="none", label="Evidence-gate run")
leg_zero    = mlines.Line2D([], [], marker="x", markersize=8, markeredgewidth=2.0,
                             color="#cc2222", linestyle="none",
                             label="Zero-score failure")

ax.legend(handles=[leg_keep, leg_discard, leg_eg, leg_zero],
          fontsize=7.5, framealpha=0.9, loc="upper left",
          borderpad=0.6, labelspacing=0.4)

# ---------------------------------------------------------------------------
# Save
# ---------------------------------------------------------------------------
plt.tight_layout()
out = "/Users/diego/Dev/non-toxic/bug_bounty/compliance-theater/assets/trajectory.png"
plt.savefig(out, dpi=150, bbox_inches="tight")
print(f"Saved: {out}")
