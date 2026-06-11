"""Profile banner in the GAUSE-cover style: toy robots with glowing screen
faces on a holographic grid floor, sunrise city backdrop.
GAUSE / RISP / NicheMem."""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.patches import (Circle, Ellipse, FancyBboxPatch, Polygon, Arc,
                                Rectangle)
from matplotlib.colors import LinearSegmentedColormap, to_rgb

plt.rcParams["font.family"] = "Arial Rounded MT Bold"

NAVY = "#1B2350"
SCREEN = "#10173A"
CYAN = "#4FE8F7"
AMBER = "#FFA85B"
W, H = 16.0, 6.4
HOR = 2.35                       # horizon

fig, ax = plt.subplots(figsize=(W, H), dpi=170)
ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")

# ------------------------------------------------------------------ sky
grad = np.linspace(0, 1, 512).reshape(-1, 1)
sky = LinearSegmentedColormap.from_list(
    "sky", ["#FFD9B0", "#F2CFE0", "#C9D4F2", "#B8C6F0"])
ax.imshow(grad, extent=(0, W, HOR, H), cmap=sky, origin="lower",
          aspect="auto", zorder=0)
# sunrise glow
N = 300
u = np.linspace(-1, 1, N)
xx, yy = np.meshgrid(u, u)
rr = np.sqrt(xx ** 2 + yy ** 2)
glow = np.clip(1 - rr, 0, 1) ** 2.2
img = np.zeros((N, N, 4))
img[..., :3] = np.array(to_rgb("#FFE2B8"))
img[..., 3] = glow * 0.9
ax.imshow(img, extent=(8 - 4.6, 8 + 4.6, HOR - 1.4, HOR + 3.2),
          origin="lower", zorder=1, interpolation="bilinear")

# ------------------------------------------------------------- city skyline
rng = np.random.default_rng(8)
def skyline(y0, hmin, hmax, color, alpha, n, z, wmin=0.35, wmax=0.9):
    x = 0.0
    while x < W:
        w = rng.uniform(wmin, wmax)
        h = rng.uniform(hmin, hmax)
        ax.add_patch(Rectangle((x, y0), w, h, fc=color, ec="none",
                               alpha=alpha, zorder=z))
        if rng.random() < 0.5:    # antenna
            ax.plot([x + w / 2, x + w / 2], [y0 + h, y0 + h + 0.22],
                    color=color, lw=1.0, alpha=alpha, zorder=z)
        # windows
        for _ in range(int(h * w * 14)):
            wxp = rng.uniform(x + 0.05, x + w - 0.05)
            wyp = rng.uniform(y0 + 0.08, y0 + h - 0.08)
            ax.plot(wxp, wyp, ",", color="#FFEFC9",
                    alpha=alpha * rng.uniform(0.4, 1.0), zorder=z)
        x += w + rng.uniform(0.05, 0.35)
skyline(HOR, 0.7, 1.9, "#9FB0DE", 0.55, 18, 2)
skyline(HOR, 0.35, 1.0, "#7E92C9", 0.75, 24, 3)

# circuit traces, top corners
def trace(x0, y0, pts, color="#FFFFFF", a=0.5):
    xs, ys = [x0], [y0]
    for dx, dy in pts:
        xs.append(xs[-1] + dx); ys.append(ys[-1] + dy)
    ax.plot(xs, ys, color=color, lw=1.0, alpha=a, zorder=4)
    ax.plot(xs[-1], ys[-1], "o", ms=2.6, color=color, alpha=a, zorder=4)
for x0, sgn in ((0.4, 1), (15.6, -1)):
    trace(x0, 6.1, [(sgn * 0.8, 0), (0, -0.4), (sgn * 0.7, 0)])
    trace(x0, 5.6, [(sgn * 0.5, 0), (0, -0.35), (sgn * 1.0, 0), (0, -0.3)])
    trace(x0 + sgn * 0.2, 4.9, [(sgn * 0.9, 0), (0, 0.3)])

# ------------------------------------------------------------------ floor
floorg = LinearSegmentedColormap.from_list(
    "floor", ["#324078", "#222C5C", "#171F48"])
ax.imshow(grad, extent=(0, W, 0, HOR), cmap=floorg, origin="upper",
          aspect="auto", zorder=1)
# horizontal grid lines, perspective spacing
for t in np.linspace(0, 1, 11)[1:]:
    y = HOR - HOR * t ** 1.65
    for lwm, a in ((3.4, 0.10), (1.0, 0.55)):
        ax.plot([0, W], [y, y], color=AMBER if int(t * 10) % 2 else CYAN,
                lw=1.1 * lwm, alpha=a * (1 - 0.5 * t) + 0.1, zorder=2)
# radial lines to vanishing point
for dxv in np.linspace(-26, 26, 27):
    ax.plot([8, 8 + dxv], [HOR, -0.4], color="#FFB868", lw=0.9, alpha=0.20,
            zorder=2)
for lwm, a in ((4.0, 0.12), (1.4, 0.7)):
    ax.plot([0, W], [HOR, HOR], color="#FFD9A0", lw=lwm, alpha=a, zorder=2)

# ------------------------------------------------------------------ helpers
def glowdot(ax, x, y, r, color, z=9):
    for m, a in ((3.0, 0.18), (1.8, 0.38), (1.0, 1.0)):
        ax.add_patch(Circle((x, y), r * m, fc=color, ec="none", alpha=a,
                            zorder=z))

def shade(c, f):
    rgb = np.array(to_rgb(c))
    if f >= 0:
        rgb = rgb + (1 - rgb) * f
    else:
        rgb = rgb * (1 + f)
    return tuple(np.clip(rgb, 0, 1))

def rbox(ax, x, y, w, h, color, rs=0.12, z=5, ec="none", lw=0):
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h,
                 boxstyle=f"round,pad=0.012,rounding_size={rs}",
                 fc=color, ec=ec, lw=lw, zorder=z))

def robot(ax, x, y0, s, color, label_color=None, sleeping=False):
    """Chunky toy robot, GAUSE-cover proportions. y0 = foot line."""
    lc = label_color or color
    dark, lite = shade(color, -0.32), shade(color, 0.45)
    # floor reflection + shadow
    ax.add_patch(Ellipse((x, y0 - 0.04 * s), 2.5 * s, 0.30 * s, fc="black",
                         ec="none", alpha=0.30, zorder=4))
    ax.add_patch(Ellipse((x, y0 - 0.30 * s), 1.9 * s, 0.55 * s, fc=lite,
                         ec="none", alpha=0.18, zorder=4))
    # legs + feet
    for sx in (-0.42, 0.42):
        rbox(ax, x + sx * s, y0 + 0.34 * s, 0.34 * s, 0.55 * s, dark,
             rs=0.07, z=5)
        rbox(ax, x + sx * s, y0 + 0.10 * s, 0.55 * s, 0.26 * s, color,
             rs=0.09, z=6)
        ax.add_patch(Ellipse((x + sx * s - 0.10 * s, y0 + 0.13 * s),
                             0.22 * s, 0.08 * s, fc="white", alpha=0.5,
                             zorder=7))
    # body
    rbox(ax, x, y0 + 1.10 * s, 1.45 * s, 1.15 * s, color, rs=0.18, z=6)
    ax.add_patch(Ellipse((x + 0.52 * s, y0 + 1.05 * s), 0.45 * s, 1.0 * s,
                         fc=dark, ec="none", alpha=0.35, zorder=7))
    ax.add_patch(Ellipse((x - 0.42 * s, y0 + 1.42 * s), 0.55 * s, 0.35 * s,
                         fc="white", ec="none", alpha=0.40, zorder=7))
    # belly screen
    rbox(ax, x, y0 + 1.10 * s, 0.78 * s, 0.62 * s, SCREEN, rs=0.10, z=8)
    # arms
    for sx in (-1, 1):
        ax.add_patch(Ellipse((x + sx * 0.92 * s, y0 + 1.12 * s), 0.34 * s,
                             0.78 * s, angle=-sx * 14, fc=color, ec="none",
                             zorder=5))
        ax.add_patch(Ellipse((x + sx * 0.92 * s, y0 + 1.12 * s), 0.34 * s,
                             0.78 * s, angle=-sx * 14, fc="black", alpha=0.12,
                             zorder=6))
        glowdot(ax, x + sx * 1.00 * s, y0 + 0.72 * s, 0.10 * s,
                shade(color, 0.2), z=7)
    # neck + head dome
    rbox(ax, x, y0 + 1.78 * s, 0.5 * s, 0.18 * s, dark, rs=0.05, z=5)
    rbox(ax, x, y0 + 2.28 * s, 1.5 * s, 0.95 * s, color, rs=0.30, z=7)
    ax.add_patch(Ellipse((x - 0.45 * s, y0 + 2.55 * s), 0.5 * s, 0.28 * s,
                         fc="white", ec="none", alpha=0.55, zorder=8))
    ax.add_patch(Ellipse((x + 0.55 * s, y0 + 2.20 * s), 0.35 * s, 0.7 * s,
                         fc=dark, ec="none", alpha=0.30, zorder=8))
    # ear pods
    for sx in (-1, 1):
        ax.add_patch(Ellipse((x + sx * 0.78 * s, y0 + 2.28 * s), 0.18 * s,
                             0.34 * s, fc=dark, ec="none", zorder=6))
        glowdot(ax, x + sx * 0.78 * s, y0 + 2.28 * s, 0.045 * s, CYAN, z=7)
    # face screen
    rbox(ax, x, y0 + 2.26 * s, 1.08 * s, 0.62 * s, SCREEN, rs=0.16, z=9)
    # face
    ey = y0 + 2.32 * s
    if sleeping:
        for sx in (-0.26, 0.26):
            ax.add_patch(Arc((x + sx * s, ey), 0.30 * s, 0.26 * s,
                             theta1=200, theta2=340, color=CYAN, lw=2.4,
                             zorder=10, capstyle="round"))
    else:
        for sx in (-0.26, 0.26):
            glowdot(ax, x + sx * s, ey, 0.085 * s, CYAN, z=10)
            ax.add_patch(Circle((x + sx * s + 0.03 * s, ey + 0.03 * s),
                                0.028 * s, fc="white", zorder=11))
    sm = Arc((x, y0 + 2.16 * s), 0.34 * s, 0.22 * s, theta1=200, theta2=340,
             color=CYAN, lw=2.2, zorder=10, capstyle="round")
    ax.add_patch(sm)
    sm.set_path_effects([pe.Stroke(linewidth=4.5, foreground=CYAN,
                                   alpha=0.35), pe.Normal()])
    # antenna
    ax.plot([x, x], [y0 + 2.76 * s, y0 + 3.02 * s], color=dark, lw=2.4,
            zorder=6, solid_capstyle="round")
    glowdot(ax, x, y0 + 3.08 * s, 0.07 * s, shade(color, 0.3), z=7)

def holo_label(ax, x, y, s, color, fs=11):
    t = ax.text(x, y, s, ha="center", va="center", fontsize=fs,
                color="white", zorder=10, fontweight="bold")
    t.set_path_effects([pe.Stroke(linewidth=4.5, foreground=color,
                                  alpha=0.6),
                        pe.Stroke(linewidth=2.0, foreground=shade(color, -0.2),
                                  alpha=0.9), pe.Normal()])

# ------------------------------------------------------------------- title
t = ax.text(8, 5.92, "ONE  PRINCIPLE,   THREE  SUBSTRATES", ha="center",
            va="center", fontsize=19, color=NAVY, fontweight="bold",
            zorder=9)
t.set_path_effects([pe.Stroke(linewidth=6, foreground="white", alpha=0.85),
                    pe.Normal()])
t2 = ax.text(8, 5.48, "what survives a bounded budget is decided by structure — never by the reward or usage stream",
             ha="center", va="center", fontsize=10.5, color="#3D4878",
             zorder=9)
t2.set_path_effects([pe.Stroke(linewidth=4, foreground="white", alpha=0.8),
                     pe.Normal()])

# ------------------------------------------------------------------ robots
FOOT = 1.00
# GAUSE bot (amber) + four niche orbs overhead
robot(ax, 3.1, FOOT, 0.78, "#F2A23C")
orb_cols = ["#F25C5C", "#5BC98A", "#5B8FE8", "#A66BD9"]
for i, c in enumerate(orb_cols):
    ox = 3.1 + (i - 1.5) * 0.52
    glowdot(ax, ox, FOOT + 2.62 + 0.14 * np.sin(i * 2.2), 0.085, c, z=9)
# chest: 2x2 niche grid
for i, c in enumerate(orb_cols):
    gx = 3.1 - 0.12 + (i % 2) * 0.24
    gy = FOOT + 0.78 + (i // 2) * 0.22
    rbox(ax, gx, gy + 0.07, 0.18, 0.16, c, rs=0.03, z=9)
holo_label(ax, 3.1, 0.52, "GAUSE — weight space", "#F2A23C", 10.5)

# RISP bot (teal-green, sleeping face) + crisis books under arm + chart
robot(ax, 8.0, FOOT, 0.82, "#46B86B", sleeping=True)
for i, (bc, by) in enumerate(zip(["#C9763C", "#E06060", "#F2484F"],
                                 (0.18, 0.34, 0.50))):
    rbox(ax, 9.15, FOOT + by, 0.92, 0.17, bc, rs=0.04, z=8)
    ax.text(9.15, FOOT + by, f"CRISIS '{ ('08','20','22')[i] }", ha="center",
            va="center", fontsize=5.6, color="white", zorder=9,
            fontweight="bold")
xs = np.linspace(6.45, 7.15, 7)
ys = FOOT + 0.30 + np.array([0, .10, .04, .16, .10, .22, .30])
for m, a in ((3.2, 0.15), (1.0, 0.95)):
    ax.plot(xs, ys, color=CYAN, lw=1.6 * m, alpha=a, zorder=8,
            solid_capstyle="round")
holo_label(ax, 8.0, 0.52, "RISP — decision space", "#2E9956", 10.5)

# NicheMem bot (violet) + memory slabs + runbook card in hand
robot(ax, 12.9, FOOT, 0.78, "#9B6BD9")
for i, (lab, c) in enumerate(zip(("D", "W", "Q"),
                                 ("#5BC98A", "#5BB8E8", "#B88AE8"))):
    rbox(ax, 11.55, FOOT + 0.30 + i * 0.27, 0.5, 0.20, c, rs=0.04, z=8)
    ax.text(11.55, FOOT + 0.30 + i * 0.27, lab, ha="center", va="center",
            fontsize=6.2, color="white", zorder=9, fontweight="bold")
rbox(ax, 13.85, FOOT + 0.62, 0.62, 0.44, "#F2484F", rs=0.06, z=9)
ax.text(13.85, FOOT + 0.62, "RUN\nBOOK", ha="center", va="center",
        fontsize=5.8, color="white", zorder=10, fontweight="bold",
        linespacing=0.9)
holo_label(ax, 12.9, 0.52, "NicheMem — context space", "#9B6BD9", 10.5)

# footer strip
t3 = ax.text(8, 0.14, "reward-chasers forget what is dormant  —  structural owners never do  —  every prediction pre-registered, every refutation shipped",
             ha="center", va="center", fontsize=9.2, color="#D8E2FF",
             zorder=9, fontweight="bold")
t3.set_path_effects([pe.Stroke(linewidth=3.5, foreground="#1B2350",
                               alpha=0.7), pe.Normal()])

fig.tight_layout(pad=0.25)
fig.savefig("research_banner.png", facecolor="#C9D4F2",
            bbox_inches="tight")
print("saved research_banner.png")
