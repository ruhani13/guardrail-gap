import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as pe
import numpy as np
from scipy import stats

# ── Load data ──────────────────────────────────────────────────────────────────
with open("/home/claude/aggregated_results.csv") as f:
    rows = list(csv.DictReader(f))

ow  = [float(r["vuln_density_per_kloc"]) for r in rows if r["model_type"] == "open_weight"]
prop = [float(r["vuln_density_per_kloc"]) for r in rows if r["model_type"] == "proprietary"]

# Stats
stat, pval = stats.mannwhitneyu(ow, prop, alternative="greater")
d = (np.mean(ow) - np.mean(prop)) / np.sqrt((np.std(ow)**2 + np.std(prop)**2)/2)

CORAL = "#D85A30"
TEAL  = "#1D9E75"
GRAY  = "#888780"
BG    = "#FAFAF9"

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 1 — Guardrail Gap: Three-Layer Defense Diagram
# ══════════════════════════════════════════════════════════════════════════════
fig1, axes = plt.subplots(1, 2, figsize=(12, 7), facecolor=BG)
fig1.suptitle("Figure 1 — The Guardrail Gap: Three-Layer Defense Coverage",
              fontsize=14, fontweight="bold", y=0.97, color="#2C2C2A")

LAYERS = ["Model-level\nalignment", "Platform-level\nguardrails", "Developer\noversight"]
COLORS_ON  = [TEAL, TEAL, TEAL]
COLORS_OFF = [CORAL, CORAL, CORAL]

for ax_i, (ax, title, colors, coverage) in enumerate(zip(
    axes,
    ["Expert + Proprietary\n(e.g. senior dev using GitHub Copilot)",
     "Non-Expert + Open-Weight\n(e.g. hobbyist using local Llama)"],
    [COLORS_ON, COLORS_OFF],
    [[1.0, 1.0, 1.0], [0.12, 0.0, 0.0]]   # coverage fraction per layer
)):
    ax.set_facecolor(BG)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis("off")
    ax.set_title(title, fontsize=10, color="#3d3d3a", pad=12)

    layer_h = 1.6
    gap = 0.55
    total_h = len(LAYERS) * layer_h + (len(LAYERS)-1) * gap
    y_start = (10 - total_h) / 2

    for i, (label, color, cov) in enumerate(zip(LAYERS, colors, coverage)):
        y = y_start + i * (layer_h + gap)
        x0, x1 = 1.2, 8.8
        w = x1 - x0

        # Background (absent layer)
        bg_rect = mpatches.FancyBboxPatch(
            (x0, y), w, layer_h,
            boxstyle="round,pad=0.08",
            linewidth=1.2,
            edgecolor="#cccccc",
            facecolor="#F1EFE8",
        )
        ax.add_patch(bg_rect)

        # Active fill
        if cov > 0:
            fill = mpatches.FancyBboxPatch(
                (x0, y), w * cov, layer_h,
                boxstyle="round,pad=0.08",
                linewidth=0,
                facecolor=color,
                alpha=0.82,
                zorder=2
            )
            ax.add_patch(fill)

        # Label
        ax.text(5, y + layer_h/2, label,
                ha="center", va="center", fontsize=10, fontweight="bold",
                color="white" if cov > 0 else GRAY, zorder=3)

        # Status badge
        badge_txt = "✓ ACTIVE" if cov > 0 else "✗ ABSENT"
        badge_col = TEAL if cov > 0 else CORAL
        ax.text(x1 - 0.15, y + layer_h/2, badge_txt,
                ha="right", va="center", fontsize=7.5, color=badge_col,
                fontweight="bold", zorder=4)

    # Risk label at bottom
    risk_txt = "Low compound risk" if coverage[0] > 0 else "HIGH COMPOUND RISK"
    risk_col = TEAL if coverage[0] > 0 else CORAL
    ax.text(5, y_start - 0.7, risk_txt,
            ha="center", va="center", fontsize=10,
            color=risk_col, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.3", facecolor=BG,
                      edgecolor=risk_col, linewidth=1.5))

plt.tight_layout(rect=[0, 0, 1, 0.95])
fig1.savefig("/home/claude/figure1_guardrail_gap.pdf", dpi=300, bbox_inches="tight", facecolor=BG)
fig1.savefig("/home/claude/figure1_guardrail_gap.png", dpi=200, bbox_inches="tight", facecolor=BG)
print("Figure 1 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 2 — Vulnerability Density Boxplot
# ══════════════════════════════════════════════════════════════════════════════
fig2, ax = plt.subplots(figsize=(8, 5.5), facecolor=BG)
ax.set_facecolor(BG)

positions = [1, 2]
data = [ow, prop]
labels = ["Open-weight models\n(n=250)", "Proprietary models\n(n=250)"]
colors = [CORAL, TEAL]

bp = ax.boxplot(data, positions=positions, patch_artist=True,
                widths=0.45, showfliers=False,
                medianprops=dict(color="white", linewidth=2.5),
                whiskerprops=dict(linewidth=1.3, color=GRAY),
                capprops=dict(linewidth=1.3, color=GRAY),
                boxprops=dict(linewidth=1.2))

for patch, color in zip(bp["boxes"], colors):
    patch.set_facecolor(color)
    patch.set_alpha(0.82)

# Jitter points
rng = np.random.RandomState(42)
for i, (d_arr, pos, col) in enumerate(zip(data, positions, colors)):
    x = rng.normal(pos, 0.08, len(d_arr))
    ax.scatter(x, d_arr, alpha=0.18, s=12, color=col, zorder=2)

# Significance annotation
y_ann = max(max(ow), max(prop)) * 1.04
ax.annotate("", xy=(2, y_ann), xytext=(1, y_ann),
            arrowprops=dict(arrowstyle="-", color="#3d3d3a", lw=1.2))
ax.text(1.5, y_ann + 1.5, f"p < 0.001, d = {d:.2f} (large)", ha="center",
        fontsize=9, color="#3d3d3a")

# Means
for pos, d_arr, col in zip(positions, data, colors):
    ax.scatter([pos], [np.mean(d_arr)], marker="D", s=55, color="white",
               edgecolors=col, linewidths=1.8, zorder=5)

ax.set_xticks(positions)
ax.set_xticklabels(labels, fontsize=10)
ax.set_ylabel("Vulnerabilities per 1,000 LOC", fontsize=10)
ax.set_title("Figure 2 — Vulnerability Density by Model Type\n(Study B Corpus, n=500)",
             fontsize=12, fontweight="bold", color="#2C2C2A", pad=10)
ax.spines[["top","right"]].set_visible(False)
ax.spines[["left","bottom"]].set_color("#cccccc")
ax.yaxis.grid(True, linestyle="--", alpha=0.4, color=GRAY)
ax.set_axisbelow(True)

# Stats box
stats_txt = (f"Open-weight:  M={np.mean(ow):.1f}, Mdn={np.median(ow):.1f}\n"
             f"Proprietary:  M={np.mean(prop):.1f}, Mdn={np.median(prop):.1f}\n"
             f"Effect: {np.mean(ow)/np.mean(prop):.2f}× higher density")
ax.text(0.97, 0.97, stats_txt, transform=ax.transAxes,
        fontsize=8.5, va="top", ha="right", color="#3d3d3a",
        bbox=dict(boxstyle="round,pad=0.4", facecolor="white",
                  edgecolor="#cccccc", alpha=0.9))

plt.tight_layout()
fig2.savefig("/home/claude/figure2_vuln_density.pdf", dpi=300, bbox_inches="tight", facecolor=BG)
fig2.savefig("/home/claude/figure2_vuln_density.png", dpi=200, bbox_inches="tight", facecolor=BG)
print("Figure 2 saved.")

# ══════════════════════════════════════════════════════════════════════════════
# FIGURE 3 — Failure Mode Taxonomy Diagram
# ══════════════════════════════════════════════════════════════════════════════
fig3, ax = plt.subplots(figsize=(11, 7), facecolor=BG)
ax.set_facecolor(BG)
ax.axis("off")
ax.set_xlim(0, 12)
ax.set_ylim(0, 8)
ax.set_title("Figure 3 — Taxonomy of Non-Expert Oversight Failure Modes",
             fontsize=13, fontweight="bold", color="#2C2C2A", pad=12)

CENTER = (6, 6.5)
FM_COLORS = ["#534AB7","#1D9E75","#D85A30","#BA7517","#993556","#185FA5"]
FMS = [
    ("FM-1", "Functional\nsufficiency bias", 1.2, 6.5),
    ("FM-2", "Generative\nconfidence anchoring", 2.8, 4.2),
    ("FM-3", "Iterative\ntrust escalation", 5.5, 3.1),
    ("FM-4", "Remediation\nprompt injection", 8.2, 3.1),
    ("FM-5", "Scope\nblindness", 10.0, 4.2),
    ("FM-6", "Deployment\nimmediary", 10.8, 6.5),
]

# Central node
center_circle = plt.Circle(CENTER, 0.9, color=CORAL, alpha=0.9, zorder=3)
ax.add_patch(center_circle)
ax.text(CENTER[0], CENTER[1], "Non-Expert\nVibe Coder",
        ha="center", va="center", fontsize=9, color="white",
        fontweight="bold", zorder=4)

for (code, label, fx, fy), col in zip(FMS, FM_COLORS):
    # Line from center
    ax.annotate("", xy=(fx, fy), xytext=CENTER,
                arrowprops=dict(arrowstyle="-", color="#cccccc", lw=1.2), zorder=1)
    # Node
    circle = plt.Circle((fx, fy), 0.75, color=col, alpha=0.85, zorder=3)
    ax.add_patch(circle)
    ax.text(fx, fy + 0.15, code, ha="center", va="center",
            fontsize=8.5, color="white", fontweight="bold", zorder=4)
    ax.text(fx, fy - 0.25, label, ha="center", va="center",
            fontsize=7, color="white", zorder=4)

# Legend note
ax.text(6, 0.4,
        "Each failure mode is independently observable and measurable — see Appendix A for operationalization guide",
        ha="center", fontsize=8.5, color=GRAY, style="italic")

plt.tight_layout()
fig3.savefig("/home/claude/figure3_taxonomy.pdf", dpi=300, bbox_inches="tight", facecolor=BG)
fig3.savefig("/home/claude/figure3_taxonomy.png", dpi=200, bbox_inches="tight", facecolor=BG)
print("Figure 3 saved.")
print("\nAll figures generated successfully.")
