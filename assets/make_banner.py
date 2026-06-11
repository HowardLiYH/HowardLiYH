"""Kawaii research-program banner for the GitHub profile README.
One principle, three substrates: GAUSE (finches) / RISP (sleeping cat) /
NicheMem (owl librarian)."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import (Circle, Ellipse, FancyBboxPatch, Polygon, Arc,
                                Wedge)
from matplotlib.colors import LinearSegmentedColormap

plt.rcParams["font.family"] = "Chalkboard SE"

INK = "#4A3B5C"
CREAM = "#FFF9EC"

def soft_shadow(ax, x, y, w, h=0.10, alpha=0.18):
    ax.add_patch(Ellipse((x, y), w, h, fc="#6B5B7B", ec="none", alpha=alpha,
                         zorder=2))

def sparkle(ax, x, y, s, color="#FFD166", rot=0):
    pts = []
    for i in range(8):
        r = s if i % 2 == 0 else s * 0.38
        a = np.pi / 4 * i + rot
        pts.append((x + r * np.sin(a), y + r * np.cos(a)))
    ax.add_patch(Polygon(pts, fc=color, ec="white", lw=0.8, zorder=8))

def eye(ax, x, y, r, closed=False, lw=2.0):
    if closed:
        ax.add_patch(Arc((x, y), 2.2 * r, 1.8 * r, theta1=200, theta2=340,
                         color=INK, lw=lw, zorder=7, capstyle="round"))
    else:
        ax.add_patch(Circle((x, y), r, fc=INK, ec="none", zorder=7))
        ax.add_patch(Circle((x + 0.32 * r, y + 0.35 * r), 0.34 * r,
                            fc="white", ec="none", zorder=8))

def blush(ax, x, y, r):
    ax.add_patch(Ellipse((x, y), 1.6 * r, r, fc="#FF9FB2", ec="none",
                         alpha=0.75, zorder=7))

def smile(ax, x, y, w, lw=2.0):
    ax.add_patch(Arc((x, y), w, 0.7 * w, theta1=200, theta2=340, color=INK,
                     lw=lw, zorder=7, capstyle="round"))

# ----------------------------------------------------------------- characters
def finch(ax, x, y, s, body, belly, look=0.0):
    """Plump round finch with big eyes, tiny beak, wing, tail, feet."""
    soft_shadow(ax, x, y - 0.62 * s, 1.5 * s)
    ax.add_patch(Polygon([(x - 0.55 * s, y - 0.1 * s),
                          (x - 1.0 * s, y + 0.18 * s),
                          (x - 0.95 * s, y - 0.28 * s)],
                         fc=body, ec=INK, lw=1.6, zorder=4))      # tail
    ax.add_patch(Circle((x, y), 0.62 * s, fc=body, ec=INK, lw=1.8, zorder=5))
    ax.add_patch(Ellipse((x, y - 0.22 * s), 0.75 * s, 0.55 * s, fc=belly,
                         ec="none", zorder=6))                    # belly
    ax.add_patch(Ellipse((x - 0.30 * s, y - 0.05 * s), 0.42 * s, 0.30 * s,
                         angle=-25, fc=body, ec=INK, lw=1.3, zorder=6))  # wing
    ax.add_patch(Polygon([(x + 0.58 * s, y + 0.10 * s),
                          (x + 0.85 * s, y + 0.02 * s),
                          (x + 0.58 * s, y - 0.06 * s)],
                         fc="#FFB24A", ec=INK, lw=1.2, zorder=6))  # beak
    eye(ax, x + 0.20 * s + look, y + 0.18 * s, 0.105 * s)
    eye(ax, x + 0.44 * s + look, y + 0.18 * s, 0.095 * s)
    blush(ax, x + 0.14 * s, y - 0.02 * s, 0.12 * s)
    for dx in (-0.12 * s, 0.14 * s):                              # feet
        ax.plot([x + dx, x + dx], [y - 0.62 * s, y - 0.78 * s],
                color="#FFB24A", lw=2.2, zorder=4,
                solid_capstyle="round")

def cat(ax, x, y, s):
    """Sleeping cat with nightcap, curled on top of the book stack."""
    soft_shadow(ax, x, y - 0.55 * s, 2.4 * s)
    ax.add_patch(Ellipse((x + 0.55 * s, y - 0.18 * s), 1.6 * s, 0.85 * s,
                         fc="#8FA8E8", ec=INK, lw=1.8, zorder=4))  # body
    ax.add_patch(Ellipse((x + 1.25 * s, y - 0.05 * s), 0.28 * s, 0.6 * s,
                         angle=35, fc="#8FA8E8", ec=INK, lw=1.6,
                         zorder=5))                                # tail
    for ex, ang in ((-0.42, 25), (0.34, -25)):                     # ears
        ax.add_patch(Polygon([(x + ex * s, y + 0.42 * s),
                              (x + (ex + 0.16) * s, y + 0.85 * s),
                              (x + (ex + 0.38) * s, y + 0.48 * s)],
                             fc="#8FA8E8", ec=INK, lw=1.6, zorder=5))
        ax.add_patch(Polygon([(x + (ex + 0.08) * s, y + 0.48 * s),
                              (x + (ex + 0.17) * s, y + 0.72 * s),
                              (x + (ex + 0.29) * s, y + 0.50 * s)],
                             fc="#FFC9D6", ec="none", zorder=6))
    ax.add_patch(Circle((x, y), 0.58 * s, fc="#A4B8F0", ec=INK, lw=1.8,
                        zorder=6))                                 # head
    eye(ax, x - 0.22 * s, y + 0.03 * s, 0.10 * s, closed=True)
    eye(ax, x + 0.20 * s, y + 0.03 * s, 0.10 * s, closed=True)
    blush(ax, x - 0.38 * s, y - 0.16 * s, 0.10 * s)
    blush(ax, x + 0.36 * s, y - 0.16 * s, 0.10 * s)
    ax.add_patch(Polygon([(x - 0.05 * s, y - 0.10 * s),
                          (x + 0.05 * s, y - 0.10 * s),
                          (x, y - 0.18 * s)], fc="#FF9FB2", ec=INK,
                         lw=1.0, zorder=7))                        # nose
    smile(ax, x, y - 0.24 * s, 0.3 * s, lw=1.6)
    for sx in (-1, 1):                                            # whiskers
        for dy in (-0.02, -0.12):
            ax.plot([x + sx * 0.52 * s, x + sx * 0.85 * s],
                    [y + dy * s, y + (dy + 0.05) * s], color=INK, lw=1.1,
                    zorder=7, solid_capstyle="round")
    # nightcap
    ax.add_patch(Polygon([(x - 0.40 * s, y + 0.42 * s),
                          (x + 0.30 * s, y + 0.46 * s),
                          (x + 0.62 * s, y + 1.05 * s)],
                         fc="#F76C8A", ec=INK, lw=1.6, zorder=8))
    ax.add_patch(FancyBboxPatch((x - 0.46 * s, y + 0.34 * s), 0.82 * s,
                 0.14 * s, boxstyle="round,pad=0.01,rounding_size=0.05",
                 fc="white", ec=INK, lw=1.3, zorder=9))
    ax.add_patch(Circle((x + 0.66 * s, y + 1.07 * s), 0.10 * s, fc="white",
                        ec=INK, lw=1.3, zorder=9))

def owl(ax, x, y, s):
    """Round owl librarian hugging the red runbook card."""
    soft_shadow(ax, x, y - 0.80 * s, 1.7 * s)
    ax.add_patch(Ellipse((x, y - 0.1 * s), 1.3 * s, 1.5 * s, fc="#9C7BD4",
                         ec=INK, lw=1.8, zorder=5))                # body
    ax.add_patch(Ellipse((x, y - 0.32 * s), 0.85 * s, 0.85 * s, fc="#E8DFF8",
                         ec="none", zorder=6))                     # belly
    for ex in (-0.42, 0.42):                                      # tufts
        ax.add_patch(Polygon([(x + (ex - 0.12) * s, y + 0.52 * s),
                              (x + ex * s, y + 0.92 * s),
                              (x + (ex + 0.14) * s, y + 0.55 * s)],
                             fc="#9C7BD4", ec=INK, lw=1.5, zorder=5))
    for ex in (-0.26, 0.26):                                      # goggle eyes
        ax.add_patch(Circle((x + ex * s, y + 0.22 * s), 0.26 * s, fc="white",
                            ec=INK, lw=1.6, zorder=6))
        eye(ax, x + ex * s, y + 0.22 * s, 0.115 * s)
    blush(ax, x - 0.48 * s, y - 0.02 * s, 0.10 * s)
    blush(ax, x + 0.48 * s, y - 0.02 * s, 0.10 * s)
    ax.add_patch(Polygon([(x - 0.08 * s, y + 0.08 * s),
                          (x + 0.08 * s, y + 0.08 * s),
                          (x, y - 0.06 * s)], fc="#FFB24A", ec=INK, lw=1.2,
                         zorder=7))                                # beak
    # wings hugging the card
    card_y = y - 0.42 * s
    ax.add_patch(FancyBboxPatch((x - 0.52 * s, card_y - 0.20 * s), 1.04 * s,
                 0.46 * s, boxstyle="round,pad=0.01,rounding_size=0.05",
                 fc="#F25C5C", ec=INK, lw=1.6, zorder=8))
    ax.text(x, card_y + 0.03 * s, "incident\nrunbook", ha="center",
            va="center", fontsize=7.2, color="white", zorder=9,
            fontweight="bold", linespacing=0.95)
    for ex in (-1, 1):
        ax.add_patch(Ellipse((x + ex * 0.62 * s, y - 0.30 * s), 0.30 * s,
                             0.62 * s, angle=-ex * 28, fc="#9C7BD4", ec=INK,
                             lw=1.5, zorder=9))

def storm_cloud(ax, x, y, s):
    for dx, dy, r in [(-0.5, 0, 0.30), (0, 0.14, 0.40), (0.52, 0, 0.30)]:
        ax.add_patch(Circle((x + dx * s, y + dy * s), r * s, fc="#7E8BB8",
                            ec=INK, lw=1.5, zorder=5))
    ax.add_patch(FancyBboxPatch((x - 0.7 * s, y - 0.28 * s), 1.4 * s, 0.3 * s,
                 boxstyle="round,pad=0.01,rounding_size=0.1", fc="#7E8BB8",
                 ec="none", zorder=5))
    eye(ax, x - 0.16 * s, y + 0.06 * s, 0.07 * s)
    eye(ax, x + 0.16 * s, y + 0.06 * s, 0.07 * s)
    ax.add_patch(Arc((x, y - 0.10 * s), 0.3 * s, 0.2 * s, theta1=20,
                     theta2=160, color=INK, lw=1.6, zorder=7))    # frown
    ax.add_patch(Polygon([(x - 0.1 * s, y - 0.34 * s),
                          (x - 0.26 * s, y - 0.72 * s),
                          (x - 0.12 * s, y - 0.70 * s),
                          (x - 0.30 * s, y - 1.08 * s),
                          (x + 0.06 * s, y - 0.78 * s),
                          (x - 0.08 * s, y - 0.78 * s),
                          (x + 0.10 * s, y - 0.40 * s)],
                         fc="#FFD166", ec="#E8A23C", lw=1.2, zorder=6))

def book(ax, x, y, w, h, color, label, fs=7.4):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.012,rounding_size=0.045",
                 fc=color, ec=INK, lw=1.7, zorder=4))
    ax.add_patch(FancyBboxPatch((x - w / 2 + 0.045, y - h / 2 + 0.03),
                 0.07, h - 0.06, boxstyle="round,pad=0.005,rounding_size=0.02",
                 fc="white", ec="none", alpha=0.45, zorder=5))
    ax.text(x + 0.03, y, label, ha="center", va="center", fontsize=fs,
            color="white", zorder=6, fontweight="bold")

# ================================================================== canvas
fig, ax = plt.subplots(figsize=(16, 6.0), dpi=170)
ax.set_xlim(0, 16); ax.set_ylim(0, 6.0); ax.axis("off")

# dreamy gradient sky
grad = np.linspace(0, 1, 256).reshape(-1, 1)
sky = LinearSegmentedColormap.from_list("sky", ["#FFF3D6", "#FBE3EC",
                                                "#E4DBF7"])
ax.imshow(grad, extent=(0, 16, 0, 6.0), cmap=sky, origin="lower",
          aspect="auto", zorder=0)
rng = np.random.default_rng(11)
for _ in range(26):
    sparkle(ax, rng.uniform(0.3, 15.7), rng.uniform(0.25, 5.75),
            rng.uniform(0.045, 0.10),
            color=rng.choice(["#FFD166", "#FF9FB2", "#9C7BD4", "#7AC89A"]),
            rot=rng.uniform(0, np.pi))

# title
ax.text(8, 5.55, "one principle,  three substrates",
        ha="center", fontsize=23, color=INK, fontweight="bold")
ax.text(8, 5.06, "what survives a bounded budget is decided by structure — never by the reward or usage stream",
        ha="center", fontsize=12.5, color="#7A5BA8")
sparkle(ax, 2.4, 5.55, 0.14, "#FFD166")
sparkle(ax, 13.6, 5.55, 0.14, "#FF9FB2")

panels = [(0.30, "GAUSE", "weight space", "#FFF1DE", "#F2B36B"),
          (5.58, "RISP", "decision space", "#E9F0FF", "#8FA8E8"),
          (10.86, "NicheMem", "context space", "#F1E9FB", "#B79BE0")]
for x0, name, sub, bg, fr in panels:
    ax.add_patch(FancyBboxPatch((x0 + 0.06, 0.50), 4.84, 4.0,
                 boxstyle="round,pad=0.02,rounding_size=0.22",
                 fc="#6B5B7B", ec="none", alpha=0.18, zorder=1))
    ax.add_patch(FancyBboxPatch((x0, 0.58), 4.84, 4.0,
                 boxstyle="round,pad=0.02,rounding_size=0.22",
                 fc=bg, ec="white", lw=4, zorder=2))
    ax.add_patch(FancyBboxPatch((x0, 0.58), 4.84, 4.0,
                 boxstyle="round,pad=0.02,rounding_size=0.22",
                 fc="none", ec=fr, lw=1.6, zorder=3))
    ax.text(x0 + 2.42, 4.13, name, ha="center", fontsize=16.5,
            color=INK, fontweight="bold", zorder=6)
    ax.text(x0 + 2.42, 3.74, sub, ha="center", fontsize=10.5,
            color="#7A5BA8", zorder=6, style="italic")

# ---- GAUSE: four finches on niche perches ----
cols = [("#F2766B", "#FFD9C9"), ("#5BB98A", "#D9F2DD"),
        ("#5B8FD9", "#D6E5FF"), ("#B07BD4", "#EBD9F7")]
for i, (b, be) in enumerate(cols):
    x = 1.05 + i * 1.13
    ax.plot([x - 0.42, x + 0.42], [1.62, 1.62], color="#B58A5A", lw=4,
            zorder=3, solid_capstyle="round")                      # perch
    ax.plot([x, x], [1.60, 1.06], color="#B58A5A", lw=3, zorder=3,
            solid_capstyle="round")
    finch(ax, x, 2.16, 0.62, b, be)
ax.text(2.72, 0.86, "four finches, four niches — competition does the assigning",
        ha="center", fontsize=9.6, color=INK, zorder=6)

# ---- RISP: cat asleep on crisis books; storm coming; still smiling ----
book(ax, 7.05, 1.45, 2.30, 0.40, "#C98A52", "crisis  ’08")
book(ax, 7.05, 1.87, 2.30, 0.40, "#D9756B", "crisis  ’20")
book(ax, 7.05, 2.29, 2.30, 0.40, "#F25C5C", "crisis  ’22")
cat(ax, 6.85, 3.02, 0.62)
storm_cloud(ax, 9.42, 3.20, 0.62)
ax.text(9.42, 1.62, "bring it.", ha="center", fontsize=10, color="#7A5BA8",
        style="italic", zorder=6)
ax.text(8.0, 0.86, "sleeps through the calm, keeps every playbook —\nand wakes up general across  ’08 ≠ ’20 ≠ ’22",
        ha="center", fontsize=9.6, color=INK, zorder=6, linespacing=1.15)

# ---- NicheMem: owl hugging runbook; memory shelf ----
for i, (lab, c) in enumerate([("daily", "#5BB98A"), ("weekly", "#5B8FD9"),
                              ("quarterly", "#B07BD4")]):
    book(ax, 11.95 + i * 1.25, 2.95, 1.10, 0.46, c, lab, 7.2)
ax.plot([11.30, 15.30], [2.66, 2.66], color="#B58A5A", lw=4, zorder=3,
        solid_capstyle="round")                                    # shelf
owl(ax, 13.28, 1.78, 0.66)
sparkle(ax, 14.45, 2.1, 0.10, "#FFD166")
ax.text(13.28, 0.86, "the dormant runbook gets an owner, not an eviction score",
        ha="center", fontsize=9.6, color=INK, zorder=6)

# footer ribbon
ax.add_patch(FancyBboxPatch((2.3, 0.06), 11.4, 0.40,
             boxstyle="round,pad=0.02,rounding_size=0.18", fc="white",
             ec="#B79BE0", lw=1.4, alpha=0.92, zorder=6))
ax.text(8, 0.26, "reward-chasers forget what is dormant  ·  structural owners never do  ·  every prediction pre-registered, every refutation shipped",
        ha="center", va="center", fontsize=10.2, color=INK, zorder=7,
        fontweight="bold")

fig.tight_layout(pad=0.25)
fig.savefig("research_banner.png", facecolor="white", bbox_inches="tight")
print("saved research_banner.png")
