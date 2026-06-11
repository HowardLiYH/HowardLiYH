"""Research-program banner for the GitHub profile README.
One principle, three substrates: GAUSE (weights) / RISP (decisions) / NicheMem (context)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse, FancyBboxPatch, Polygon, Arc

INK = "#2D3748"
SUN = "#F6C453"
BLUE, DBLUE = "#5A82C8", "#3D6BBF"
GREEN, RED, ORANGE = "#3C915A", "#C83C3C", "#E28C3C"
PANELS = ["#FFF7EA", "#EEF4FF", "#EFFAF2"]
FRAMES = ["#E2A86A", "#7A9CD8", "#7AC89A"]


def blob(ax, x, y, r, color, sleep=False, happy=True):
    ax.add_patch(Circle((x, y), r, fc=color, ec=INK, lw=1.8, zorder=5))
    ex, ey = 0.35 * r, 0.25 * r
    if sleep:
        for sx in (-ex, ex):
            ax.plot([x + sx - 0.15 * r, x + sx + 0.15 * r], [y + ey, y + ey],
                    color=INK, lw=1.8, zorder=6, solid_capstyle="round")
        ax.add_patch(Arc((x, y - 0.15 * r), 0.5 * r, 0.3 * r, theta1=200,
                         theta2=340, color=INK, lw=1.8, zorder=6))
        for dx, dy, s in [(1.25, 0.55, 7), (1.6, 0.8, 9), (1.95, 1.05, 11)]:
            ax.text(x + dx * r, y + dy * r, "z", fontsize=s, color=INK,
                    style="italic", fontweight="bold", zorder=6)
    else:
        for sx in (-ex, ex):
            ax.add_patch(Circle((x + sx, y + ey), 0.09 * r, fc=INK, zorder=6))
        ax.add_patch(Arc((x, y - 0.1 * r), 0.7 * r, 0.5 * r, theta1=200,
                         theta2=340, color=INK, lw=1.9, zorder=6))


def chip(ax, x, y, w, h, color, label, fs=7.5, tc="white"):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.01,rounding_size=0.03",
                 fc=color, ec=INK, lw=1.4, zorder=4))
    ax.text(x, y, label, ha="center", va="center", fontsize=fs,
            fontweight="bold", color=tc, zorder=5)


fig, ax = plt.subplots(figsize=(16, 5.4), dpi=170)
ax.set_xlim(0, 16); ax.set_ylim(0, 5.4); ax.axis("off")

# ---- title + principle ----
ax.text(8, 5.08, "ONE  PRINCIPLE,   THREE  SUBSTRATES", ha="center",
        fontsize=17, fontweight="bold", color=INK)
ax.text(8, 4.62, "what survives a bounded budget must be decided by structure  —  not by the reward or usage stream",
        ha="center", fontsize=11.5, style="italic", color=DBLUE)

panels = [(0.25, "GAUSE", "weight space", "learner populations"),
          (5.55, "RISP", "decision space", "trading strategy pools"),
          (10.85, "NicheMem", "context space", "long-horizon agent memory")]
for (x0, name, sub, dom), bg, fr in zip(panels, PANELS, FRAMES):
    ax.add_patch(FancyBboxPatch((x0, 0.55), 4.9, 3.6,
                 boxstyle="round,pad=0.02,rounding_size=0.14",
                 fc=bg, ec=fr, lw=2.5))
    ax.text(x0 + 2.45, 3.82, name, ha="center", fontsize=14.5,
            fontweight="bold", color=INK)
    ax.text(x0 + 2.45, 3.46, f"{sub}  ·  {dom}", ha="center", fontsize=9.5,
            color=INK, style="italic")

# ---- GAUSE: population partitions regimes ----
cols = ["#C86A4A", "#7A9E7E", BLUE, "#8C5AC8"]
regs = ["R1", "R2", "R3", "R4"]
for i, (c, rl) in enumerate(zip(cols, regs)):
    x = 0.95 + i * 1.18
    blob(ax, x, 2.45, 0.33, c)
    chip(ax, x, 1.7, 0.78, 0.4, c, rl, 8)
    ax.plot([x, x], [2.07, 1.93], color=c, lw=2)
ax.text(2.7, 1.05, "competition partitions the niches —\nno gate, no schedule, no diversity reward",
        ha="center", fontsize=9, color=INK)

# ---- RISP: sleeping crisis specialist + storm ----
chip(ax, 7.0, 1.62, 1.55, 0.34, "#A0522D", "CRISIS  ’08", 7.5)
chip(ax, 7.0, 1.98, 1.55, 0.34, "#B05A36", "CRISIS  ’20", 7.5)
chip(ax, 7.0, 2.34, 1.55, 0.34, RED, "CRISIS  ’22", 7.5)
blob(ax, 7.0, 2.95, 0.36, BLUE, sleep=True)
# storm icon
for cx, cy, r in [(9.15, 3.0, 0.22), (9.45, 3.08, 0.27), (9.78, 3.0, 0.22)]:
    ax.add_patch(Circle((cx, cy), r, fc="#4A5568", ec=INK, lw=1, zorder=3))
ax.add_patch(Polygon([(9.45, 2.78), (9.3, 2.42), (9.43, 2.42), (9.25, 2.05),
                      (9.58, 2.36), (9.45, 2.36), (9.6, 2.7)],
                     fc=SUN, ec="#E0A33C", lw=1, zorder=4))
ax.annotate("", xy=(8.85, 2.6), xytext=(7.85, 2.6),
            arrowprops=dict(arrowstyle="-|>", color=INK, lw=1.6))
ax.text(9.45, 1.75, "ready on\nday 1", ha="center", fontsize=8.5,
        color=GREEN, fontweight="bold")
ax.text(8.0, 1.05, "retention x invariance: keep the playbook,\nand keep it general across  ’08 ≠ ’20 ≠ ’22",
        ha="center", fontsize=9, color=INK)

# ---- NicheMem: memory cards; dormant runbook retained ----
for i, (lab, c) in enumerate([("daily ops", "#7A9E7E"), ("weekly rpt", BLUE),
                              ("quarterly", "#8C5AC8")]):
    chip(ax, 11.85 + i * 1.32, 2.9, 1.16, 0.44, c, lab, 7)
chip(ax, 12.4, 2.0, 1.7, 0.48, RED, "incident runbook", 7.5)
blob(ax, 14.0, 2.05, 0.31, BLUE, sleep=True)
ax.text(14.85, 2.05, "owned,\nidle", ha="center", fontsize=8.5, color=DBLUE,
        fontweight="bold")
ax.text(13.3, 1.05, "usage-driven memory evicts the dormant runbook;\ncompetitive ownership retains it exactly",
        ha="center", fontsize=9, color=INK)

# ---- footer ----
ax.text(8, 0.18, "reward / usage-driven allocation forgets what is dormant   →   emergent, reward-independent ownership retains it   ·   "
        "every project pre-registers its predictions and ships its refutations",
        ha="center", fontsize=10, color=INK, fontweight="bold")
fig.tight_layout(pad=0.3)
fig.savefig("research_banner.png", facecolor="white",
            bbox_inches="tight")
print("saved research_banner.png")
