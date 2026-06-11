"""Futuristic neon-holo research banner: shaded 3D-look characters,
synthwave grid, glass panels. GAUSE / RISP / NicheMem."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import (Circle, Ellipse, FancyBboxPatch, Polygon, Arc)
from matplotlib.colors import LinearSegmentedColormap, to_rgb

plt.rcParams["font.family"] = "Arial Rounded MT Bold"

INK = "#0B1026"
CYAN = "#5BE8FF"
MAGENTA = "#FF5BD8"
VIOLET = "#9D7BFF"
AMBER = "#FFC95B"
MINT = "#5BFFB8"
CORAL = "#FF7B6B"

W, H = 16.0, 6.0
fig, ax = plt.subplots(figsize=(W, H), dpi=170)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# ---------------------------------------------------------------- background
grad = np.linspace(0, 1, 512).reshape(-1, 1)
sky = LinearSegmentedColormap.from_list("sky", ["#2A1B4A", "#141B3D",
                                                "#0B1026"])
ax.imshow(grad, extent=(0, W, 0, H), cmap=sky, origin="upper",
          aspect="auto", zorder=0)
rng = np.random.default_rng(5)
for _ in range(90):                                   # starfield
    x, y = rng.uniform(0, W), rng.uniform(1.1, H)
    s = rng.uniform(0.4, 1.6)
    c = rng.choice([CYAN, "white", VIOLET, MAGENTA])
    ax.plot(x, y, ".", ms=s, color=c, alpha=rng.uniform(0.35, 0.9), zorder=1)

# synthwave perspective grid (vanishing point at center horizon)
hy, vx = 1.55, W / 2
for i, t in enumerate(np.linspace(0, 1, 9)[1:]):      # horizontal lines
    y = hy - 1.55 * t ** 1.7
    a = 0.38 - 0.3 * t
    ax.plot([0, W], [y, y], color=MAGENTA, lw=1.0, alpha=max(a, 0.06),
            zorder=1)
for dx in np.linspace(-22, 22, 23):                   # radial verticals
    ax.plot([vx, vx + dx], [hy, 0], color=MAGENTA, lw=0.8, alpha=0.16,
            zorder=1)
ax.plot([0, W], [hy, hy], color=MAGENTA, lw=1.6, alpha=0.5, zorder=1)
ax.plot([0, W], [hy, hy], color=MAGENTA, lw=5, alpha=0.12, zorder=1)

# ------------------------------------------------------------------- helpers
def hexrgb(c):
    return np.array(to_rgb(c))

def ball(ax, x, y, r, color, zorder=6, rim=CYAN):
    """Phong-shaded glossy sphere with neon rim light."""
    N = 240
    u = np.linspace(-1, 1, N)
    xx, yy = np.meshgrid(u, u)
    rr2 = xx ** 2 + yy ** 2
    mask = rr2 <= 1.0
    z = np.sqrt(np.clip(1 - rr2, 0, 1))
    L = np.array([-0.45, 0.55, 0.70]); L = L / np.linalg.norm(L)
    lam = np.clip(xx * L[0] + yy * L[1] + z * L[2], 0, 1)
    spec = lam ** 60
    rimv = np.clip(1 - z, 0, 1) ** 2.2
    base = hexrgb(color)
    img = np.zeros((N, N, 4))
    col = (base * (0.22 + 0.78 * lam[..., None])
           + np.array([1, 1, 1]) * spec[..., None] * 0.85
           + hexrgb(rim) * rimv[..., None] * 0.45)
    img[..., :3] = np.clip(col, 0, 1)
    img[..., 3] = mask.astype(float)
    ax.imshow(img, extent=(x - r, x + r, y - r, y + r), origin="lower",
              zorder=zorder, interpolation="bilinear")

def glow_line(ax, xs, ys, color, lw=1.6, zorder=3):
    for mult, a in ((4.5, 0.10), (2.5, 0.22), (1.0, 0.95)):
        ax.plot(xs, ys, color=color, lw=lw * mult, alpha=a, zorder=zorder,
                solid_capstyle="round")

def glow_text(ax, x, y, s, fs, color, zorder=9, ha="center", weight="bold"):
    t = ax.text(x, y, s, ha=ha, va="center", fontsize=fs, color="white",
                zorder=zorder, fontweight=weight)
    t.set_path_effects([pe.Stroke(linewidth=5.5, foreground=color, alpha=0.55),
                        pe.Stroke(linewidth=2.4, foreground=color, alpha=0.9),
                        pe.Normal()])

def pedestal(ax, x, y, w, color=CYAN, zorder=3):
    """Floating holo ring + light cone."""
    ax.add_patch(Polygon([(x - 0.42 * w, y), (x + 0.42 * w, y),
                          (x + 0.58 * w, y + 1.15), (x - 0.58 * w, y + 1.15)],
                         fc=color, ec="none", alpha=0.06, zorder=zorder))
    for ww, a in ((1.5, 0.12), (1.18, 0.30), (1.0, 0.85)):
        ax.add_patch(Ellipse((x, y), w * ww, 0.16 * ww, fc="none", ec=color,
                             lw=1.5, alpha=a, zorder=zorder + 1))

def slab(ax, x, y, w, h, color, label, fs=7.6, zorder=5):
    """Glowing glass data-slab (futuristic book)."""
    for pad, a in ((0.045, 0.10), (0.02, 0.20)):
        ax.add_patch(FancyBboxPatch((x - w / 2 - pad, y - h / 2 - pad),
                     w + 2 * pad, h + 2 * pad,
                     boxstyle="round,pad=0.01,rounding_size=0.05",
                     fc="none", ec=color, lw=2, alpha=a, zorder=zorder))
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle="round,pad=0.01,rounding_size=0.05",
                 fc=color, ec="white", lw=0.8, alpha=0.85, zorder=zorder + 1))
    ax.add_patch(FancyBboxPatch((x - w / 2 + 0.03, y + h * 0.08), w - 0.06,
                 h * 0.30, boxstyle="round,pad=0.005,rounding_size=0.03",
                 fc="white", ec="none", alpha=0.30, zorder=zorder + 2))
    ax.text(x, y - 0.01, label, ha="center", va="center", fontsize=fs,
            color=INK, zorder=zorder + 3, fontweight="bold")

def eyes(ax, x, y, r, dx=0.30, closed=False):
    for sx in (-dx, dx):
        if closed:
            ax.add_patch(Arc((x + sx * r * 3, y), 0.55 * r, 0.45 * r,
                             theta1=200, theta2=340, color=INK, lw=2.2,
                             zorder=9, capstyle="round"))
        else:
            ax.add_patch(Circle((x + sx * r * 3, y), 0.26 * r, fc=INK,
                                ec="none", zorder=9))
            ax.add_patch(Circle((x + sx * r * 3 + 0.08 * r, y + 0.09 * r),
                                0.09 * r, fc="white", ec="none", zorder=10))

def blushes(ax, x, y, r):
    for sx in (-1, 1):
        ax.add_patch(Ellipse((x + sx * 0.62 * r, y - 0.28 * r), 0.42 * r,
                             0.22 * r, fc=MAGENTA, ec="none", alpha=0.5,
                             zorder=9))

def smile(ax, x, y, w):
    ax.add_patch(Arc((x, y), w, 0.7 * w, theta1=200, theta2=340, color=INK,
                     lw=2.0, zorder=9, capstyle="round"))

# --------------------------------------------------------------------- title
glow_text(ax, W / 2, 5.55, "ONE  PRINCIPLE,  THREE  SUBSTRATES", 21, CYAN)
sub = ax.text(W / 2, 5.08,
              "what survives a bounded budget is decided by structure  —  never by the reward or usage stream",
              ha="center", va="center", fontsize=11.5, color="#C9BCF2",
              zorder=9)
for x0, c in ((2.05, AMBER), (13.95, MINT)):
    glow_line(ax, [x0, x0 + 1.15] if x0 < 8 else [x0 - 1.15, x0],
              [5.55, 5.55], c, lw=1.6, zorder=8)

# -------------------------------------------------------------------- panels
panels = [(0.30, "GAUSE", "weight space", AMBER),
          (5.58, "RISP", "decision space", CYAN),
          (10.86, "NicheMem", "context space", VIOLET)]
for x0, name, subt, neon in panels:
    for pad, a in ((0.07, 0.08), (0.03, 0.16)):
        ax.add_patch(FancyBboxPatch((x0 - pad, 0.52 - pad), 4.84 + 2 * pad,
                     4.02 + 2 * pad,
                     boxstyle="round,pad=0.02,rounding_size=0.24",
                     fc="none", ec=neon, lw=2.5, alpha=a, zorder=2))
    ax.add_patch(FancyBboxPatch((x0, 0.52), 4.84, 4.02,
                 boxstyle="round,pad=0.02,rounding_size=0.24",
                 fc="white", ec="none", alpha=0.055, zorder=2))
    ax.add_patch(FancyBboxPatch((x0, 0.52), 4.84, 4.02,
                 boxstyle="round,pad=0.02,rounding_size=0.24",
                 fc="none", ec=neon, lw=1.6, alpha=0.95, zorder=3))
    glow_text(ax, x0 + 2.42, 4.12, name, 15.5, neon)
    ax.text(x0 + 2.42, 3.73, subt, ha="center", fontsize=10,
            color="#C9BCF2", zorder=6)

# ---- GAUSE: four glossy orb-finches on holo pedestals ----
cols = [CORAL, MINT, CYAN, VIOLET]
labs = ["R1", "R2", "R3", "R4"]
for i, (c, rl) in enumerate(zip(cols, labs)):
    x = 1.07 + i * 1.13
    pedestal(ax, x, 1.42, 0.85, color=c)
    ball(ax, x, 2.30, 0.42, c)
    ax.add_patch(Polygon([(x + 0.38, 2.34), (x + 0.58, 2.28),
                          (x + 0.38, 2.22)], fc=AMBER, ec=INK, lw=0.8,
                         zorder=9))                       # beak
    eyes(ax, x + 0.05, 2.40, 0.16)
    blushes(ax, x + 0.02, 2.32, 0.30)
    glow_text(ax, x, 1.42, rl, 8.5, c)
ax.text(2.72, 0.84, "four specialists, four niches —\ncompetition does the assigning",
        ha="center", fontsize=9.2, color="#E8E2F8", zorder=6,
        linespacing=1.15)

# ---- RISP: orb-cat asleep on glowing data slabs; storm + holo chart ----
slab(ax, 7.0, 1.52, 2.25, 0.40, "#D9756B", "CRISIS  '08")
slab(ax, 7.0, 1.96, 2.25, 0.40, CORAL, "CRISIS  '20")
slab(ax, 7.0, 2.40, 2.25, 0.40, "#FF5B7B", "CRISIS  '22")
ball(ax, 7.0, 3.06, 0.44, "#6B8FE8")
for ex in (-0.30, 0.30):                                  # ears
    ax.add_patch(Polygon([(7.0 + ex - 0.13, 3.36), (7.0 + ex, 3.62),
                          (7.0 + ex + 0.13, 3.38)], fc="#6B8FE8", ec=CYAN,
                         lw=1.0, zorder=8))
eyes(ax, 7.0, 3.10, 0.17, closed=True)
blushes(ax, 7.0, 3.00, 0.32)
smile(ax, 7.0, 2.94, 0.16)
for i, (dx, dy, fs) in enumerate([(-0.66, 0.38, 8), (-0.88, 0.52, 10),
                                  (-1.12, 0.68, 12)]):
    t = ax.text(7.0 + dx, 3.06 + dy, "z", fontsize=fs, color=CYAN,
                style="italic", fontweight="bold", zorder=9)
    t.set_path_effects([pe.Stroke(linewidth=3, foreground=CYAN, alpha=0.35),
                        pe.Normal()])
# storm cloud + glowing bolt
for dx, dy, r in [(-0.30, 0, 0.17), (0, 0.09, 0.23), (0.31, 0, 0.17)]:
    ax.add_patch(Circle((9.35 + dx, 3.42 + dy), r, fc="#3A4470", ec=VIOLET,
                        lw=1.2, zorder=6))
bolt = Polygon([(9.30, 3.20), (9.18, 2.88), (9.30, 2.88), (9.14, 2.52),
                (9.46, 2.80), (9.34, 2.80), (9.48, 3.12)],
               fc=AMBER, ec="white", lw=0.8, zorder=7)
ax.add_patch(bolt)
glow_line(ax, [8.62, 8.95, 9.25, 9.60, 9.95],
          [2.10, 2.18, 2.05, 2.22, 2.35], MINT, lw=1.6, zorder=6)
ax.text(9.40, 1.78, "ready on day 1", ha="center", fontsize=8.6,
        color=MINT, zorder=7, fontweight="bold")
ax.text(8.0, 0.84, "sleeps through the calm, keeps every playbook —\nwakes up general across  '08 ≠ '20 ≠ '22",
        ha="center", fontsize=9.2, color="#E8E2F8", zorder=6,
        linespacing=1.15)

# ---- NicheMem: orb-owl with goggle eyes hugging the runbook card ----
for i, (lab, c) in enumerate([("daily", MINT), ("weekly", CYAN),
                              ("quarterly", VIOLET)]):
    slab(ax, 11.95 + i * 1.25, 3.02, 1.08, 0.44, c, lab, 7.0)
glow_line(ax, [11.32, 15.28], [2.74, 2.74], VIOLET, lw=1.6, zorder=3)
pedestal(ax, 13.28, 1.06, 1.15, color=VIOLET)
ball(ax, 13.28, 1.95, 0.50, "#8F6BD9")
for ex in (-0.34, 0.34):                                  # tufts
    ax.add_patch(Polygon([(13.28 + ex - 0.10, 2.32), (13.28 + ex, 2.58),
                          (13.28 + ex + 0.12, 2.34)], fc="#8F6BD9",
                         ec=VIOLET, lw=1.0, zorder=8))
for ex in (-0.20, 0.20):                                  # goggle eyes
    ax.add_patch(Circle((13.28 + ex, 2.06), 0.155, fc="white", ec=INK,
                        lw=1.2, zorder=9))
    ax.add_patch(Circle((13.28 + ex, 2.06), 0.075, fc=INK, zorder=10))
    ax.add_patch(Circle((13.28 + ex + 0.03, 2.09), 0.025, fc="white",
                        zorder=11))
ax.add_patch(Polygon([(13.22, 1.94), (13.34, 1.94), (13.28, 1.84)],
                     fc=AMBER, ec=INK, lw=0.8, zorder=9))
blushes(ax, 13.28, 1.96, 0.34)
slab(ax, 13.28, 1.52, 1.05, 0.40, "#FF5B7B", "runbook", 7.4, zorder=8)
ax.text(13.28, 0.84, "the dormant runbook gets an owner,\nnot an eviction score",
        ha="center", fontsize=9.2, color="#E8E2F8", zorder=6,
        linespacing=1.15)

# -------------------------------------------------------------------- footer
ax.add_patch(FancyBboxPatch((2.1, 0.06), 11.8, 0.38,
             boxstyle="round,pad=0.02,rounding_size=0.18", fc="white",
             ec=CYAN, lw=1.2, alpha=0.08, zorder=6))
ax.text(8, 0.25, "reward-chasers forget what is dormant   —   structural owners never do   —   every prediction pre-registered, every refutation shipped",
        ha="center", va="center", fontsize=9.8, color="#C9E8F2", zorder=7,
        fontweight="bold")

fig.tight_layout(pad=0.25)
fig.savefig("research_banner.png", facecolor=INK, bbox_inches="tight")
print("saved research_banner.png")
