#!/usr/bin/env python3
"""Regenerate every figure of the founding note from the reference engine.

    python3 note/figs.py            # all figures
    python3 note/figs.py fig1 fig3  # a subset

Every panel is produced by `xnomos.py`, so running this file is also a
cross-validation of the general cross-amendment engine against the specimens
that were originally found with the chapter-one engines (nomos2.py,
nomos2d/engine2d.py, rings/ring.py): the Jubilee panel, for instance, must
reproduce the clock law |S_t| = 4 at every t = 2^k.
"""
from __future__ import annotations

import sys
import pathlib

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from xnomos import (Const, state_of, step, card,                    # noqa: E402
                    verify_glider)

HERE = pathlib.Path(__file__).resolve().parent

VOID, ONE, TWO = "#000000", "#c03a54", "#f6e3ae"
CMAP = ListedColormap([VOID, ONE, TWO])
LINE = "#c0392b"


# --------------------------------------------------------------- 1D spacetime

def raster(S0, C, steps, lo, hi, mode="parity"):
    """Occupancy raster: 0 empty, 1 one law, 2 two or more."""
    S = dict(S0)
    rows = []
    for _ in range(steps):
        row = np.zeros(hi - lo + 1, dtype=np.uint8)
        for cell, mask in S.items():
            if lo <= cell <= hi:
                row[cell - lo] = min(2, bin(mask).count("1"))
        rows.append(row)
        S = step(S, C, mode)
    return np.array(rows)


def panel(ax, img, title):
    ax.imshow(img, cmap=CMAP, vmin=0, vmax=2, interpolation="nearest",
              aspect="auto")
    ax.set_title(title, fontsize=10)
    ax.set_xlabel("statute book (position)", fontsize=9)


def fig1():
    """Colonizer, weld, and assimilation through a sunset wall."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.4))

    # (a) the colonizer (0,1,1): only its frontmost copy is ever active.
    C = Const([(0, 1, 1)])
    panel(axes[0], raster(state_of([(5, 0)]), C, 60, 0, 65),
          "colonizer (single law)")
    axes[0].set_ylabel("time  " + r"$\rightarrow$", fontsize=9)

    # (b) two traditions meet: right-colonizer and left-colonizer weld.
    C = Const([(0, 1, 1), (0, -1, -1)])
    panel(axes[1], raster(state_of([(4, 0), (52, 1)]), C, 60, 0, 56),
          "weld: two traditions meet")

    # (c) the wall erodes from its far end on its own; the front then fills
    #     the vacated ground -- crossing time max(2L, x0+L), "refraction 2".
    C = Const([(0, 1, 1), (-1, 1, 0)])
    seed = [(2, 0)] + [(i, 1) for i in range(15, 36)]
    panel(axes[2], raster(state_of(seed), C, 70, 0, 62),
          "sunset wall: it erodes, the front inherits")

    fig.tight_layout()
    save(fig, "fig1_spacetime")


def fig2():
    """The minimal ring rotor: kind (0,1,-1) at {1,2,5} of Z/6, hop 3."""
    m, steps = 6, 3
    C = Const([(0, 1, -1)], modulus=m)
    S = state_of([(1, 0), (2, 0), (5, 0)])
    fig, axes = plt.subplots(1, steps, figsize=(6.2, 2.5))
    ang = np.linspace(np.pi / 2, np.pi / 2 - 2 * np.pi, m, endpoint=False)
    for t in range(steps):
        ax = axes[t]
        ax.add_artist(plt.Circle((0, 0), 1.0, fill=False, lw=1.0,
                                 color="#9aa3ae", zorder=0))
        for j in range(m):
            x, y = np.cos(ang[j]), np.sin(ang[j])
            on = j in S
            ax.add_artist(plt.Circle((x, y), 0.22, color=ONE if on else "white",
                                     ec="#232830", lw=1.0, zorder=2))
            ax.text(x, y, str(j), ha="center", va="center", zorder=3,
                    fontsize=7, color="white" if on else "#232830")
        ax.set_xlim(-1.45, 1.45)
        ax.set_ylim(-1.45, 1.45)
        ax.set_aspect("equal")
        ax.axis("off")
        ax.set_title(r"$t=%d$" % t, fontsize=9)
        S = step(S, C)
    fig.suptitle(r"ring rotor on $\mathbb{Z}/6$: the bloc hops $m/2=3$ per step",
                 fontsize=9)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    save(fig, "fig2_rotor")


def fig3(steps=1 << 15):
    """The Jubilee Code: quiescence punctuated by avalanches at t = 2^k."""
    # compass: E=(1,0) W=(-1,0) N=(0,-1) S=(0,1)
    C = Const([((1, 0), (0, 1), (0, -1)),      # ESN
               ((0, 1), (0, -1), (0, 1)),      # SNS
               ((-1, 0), (0, -1), (1, 0))],    # WNE
              dim=2)
    S = state_of([((-1, 0), 0), ((-1, 1), 1), ((0, 1), 2)])
    sizes = []
    for _ in range(steps):
        sizes.append(card(S))
        S = step(S, C)
    sizes = np.array(sizes)

    # The clock law (nomos2d/JUBILEE-LAW.md): the crest is at t = 2^k - 1 and
    # the code collapses to exactly four laws at t = 2^k.
    pw = [1 << k for k in range(1, 20) if (1 << k) < steps]
    resets = [int(sizes[p]) for p in pw]
    crests = [int(sizes[p - 1]) for p in pw]
    print("  Jubilee: |S| at every t=2^k -> %s  (all four? %s)"
          % (set(resets), set(resets) == {4}))
    print("  crest heights at t=2^k-1 -> %s" % crests)

    fig, ax = plt.subplots(figsize=(7.6, 2.8))
    ax.plot(np.arange(0, steps), sizes, lw=0.6, color=LINE)
    for p in pw:
        ax.axvline(p, color="#c6cbc9", lw=0.7, zorder=0)
    ax.plot(pw, resets, "o", ms=2.6, color="#232830", zorder=3,
            label=r"$|S_{2^k}| = 4$ exactly")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_xscale("log")
    ax.set_xlabel(r"time (log scale); gridlines at $t=2^k$", fontsize=9)
    ax.set_ylabel("laws in force", fontsize=9)
    ax.set_title(r"the Jubilee Code: quiescence punctuated by avalanches "
                 r"at $t=2^k$", fontsize=10)
    fig.tight_layout()
    save(fig, "fig3_jubilee")


def fig4():
    """The first free gliders: motion bought with out-degree (chapter two)."""
    fig, axes = plt.subplots(1, 3, figsize=(11, 3.2))

    # SOLO: one placed law, period 2, displacement 1.
    C = Const([(0, 1, 0), (0, 1, 1), (0, 1, 0)], [(1, 2), (0,), (0,)])
    S = state_of([(1, 0)])
    assert verify_glider(S, C, 2, 1)
    panel(axes[0], raster(S, C, 40, 0, 24), "SOLO: one law, speed 1/2")
    axes[0].set_ylabel("time  " + r"$\rightarrow$", fontsize=9)

    # TANDEM-1: two laws in a single cell, period 1, displacement 1.
    C = Const([(0, -1, 1), (0, -1, 0)], [(0, 1), (0, 1)])
    S = state_of([(1, 0), (1, 1)])
    assert verify_glider(S, C, 1, 1)
    panel(axes[1], raster(S, C, 40, 0, 44), "TANDEM-1: two laws, speed 1")

    # TRIPTYCH: a glider under parity that dies under OR.
    C = Const([(0, 1, 0), (0, -1, 1), (0, 1, -1)], [(0, 1, 2)] * 3)
    S = state_of([(c, k) for c in (1, 2, 4) for k in range(3)])
    assert verify_glider(S, C, 1, 1)
    panel(axes[2], raster(S, C, 40, 0, 44),
          "TRIPTYCH: travels under parity, not under OR")

    fig.tight_layout()
    save(fig, "fig4_gliders")


def _grid(S, pad=1):
    """Occupancy raster of a 2-D state over its own bounding box."""
    xs = [c[0] for c in S]
    ys = [c[1] for c in S]
    img = np.zeros((max(ys) - min(ys) + 1 + 2 * pad,
                    max(xs) - min(xs) + 1 + 2 * pad), dtype=np.uint8)
    for (x, y), m in S.items():
        img[y - min(ys) + pad, x - min(xs) + pad] = min(2, bin(m).count("1"))
    return img


def fig5():
    """Two dimensions: the plane fills, and a second binary counter."""
    V = {"O": (0, 0), "E": (1, 0), "W": (-1, 0), "N": (0, -1), "S": (0, 1),
         "P": (1, -1), "Q": (-1, -1), "R": (1, 1), "T": (-1, 1)}

    def off(s):
        return tuple(V[ch] for ch in s)

    fig = plt.figure(figsize=(11, 3.2))
    gs = fig.add_gridspec(1, 3, width_ratios=[1, 1, 2.1], wspace=0.28)

    # (a) LAND GRANT at t = 24: a solid square, |S_t| = (t+1)^2.
    C = Const([off("OPP"), off("OEE"), off("ONN")], [(0, 1, 2), (1,), (2,)],
              dim=2)
    S = state_of([((0, 0), 0)])
    T = 24
    for _ in range(T):
        S = step(S, C)
    assert card(S) == (T + 1) ** 2
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(_grid(S), cmap=CMAP, vmin=0, vmax=2, interpolation="nearest")
    ax.set_title(r"LAND GRANT, $t=24$: $|S_t|=(t{+}1)^2$", fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])

    # (b) SOWER: half the box.
    C = Const([off("OEE"), off("ONN")], [(0, 1), (1,)], dim=2)
    S = state_of([((0, 0), 0)])
    for _ in range(T):
        S = step(S, C)
    ax = fig.add_subplot(gs[0, 1])
    ax.imshow(_grid(S), cmap=CMAP, vmin=0, vmax=2, interpolation="nearest")
    ax.set_title(r"SOWER: $\binom{t+2}{2}$, half the box", fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])

    # (c) THE ODOMETER: laws in force, log time, resets to four (reach ~ 1.5*sqrt(t)).
    C = Const([off("OEW"), off("NQR")], [(1,), (0, 1)], dim=2)
    S = state_of([((0, 0), 0), ((1, 0), 0), ((0, 1), 1)])
    N = 1 << 14
    z = []
    for _ in range(N):
        z.append(card(S))
        S = step(S, C)
    z = np.array(z)
    pw = [1 << k for k in range(1, 14)]
    print("  Odometer: |S| at every t=2^k -> %s" % {int(z[p]) for p in pw})
    ax = fig.add_subplot(gs[0, 2])
    ax.plot(np.arange(N), z, lw=0.6, color=LINE)
    for q in pw:
        ax.axvline(q, color="#c6cbc9", lw=0.7, zorder=0)
    ax.plot(pw, [z[q] for q in pw], "o", ms=2.6, color="#232830", zorder=3,
            label=r"$|S_{2^k}| = 4$ exactly")
    ax.set_xscale("log")
    ax.legend(fontsize=8, frameon=False, loc="upper left")
    ax.set_xlabel(r"time (log scale); gridlines at $t=2^k$", fontsize=9)
    ax.set_ylabel("laws in force", fontsize=9)
    ax.set_title("THE ODOMETER: three laws, two kinds", fontsize=9)

    fig.subplots_adjust(left=0.02, right=0.99, top=0.90, bottom=0.24)
    save(fig, "fig5_plane")


def fig6():
    """Impermanence: the same law walks, and longevity is friction."""
    sys.path.insert(0, str(HERE.parent / "sunset"))
    from sunset import step_sunset, classify_sunset          # noqa: E402

    def sraster(S0, C, steps, lo, hi, tau=1):
        S, ages = dict(S0), None
        rows = []
        for _ in range(steps):
            row = np.zeros(hi - lo + 1, dtype=np.uint8)
            for cell, mask in S.items():
                if lo <= cell <= hi:
                    row[cell - lo] = min(2, bin(mask).count("1"))
            rows.append(row)
            S, ages = step_sunset(S, C, tau, ages)
        return np.array(rows)

    fig = plt.figure(figsize=(11, 3.3))
    gs = fig.add_gridspec(1, 4, width_ratios=[1, 1, 1.5, 1.1], wspace=0.3)

    C = Const([(0, 1, 1)])
    S = state_of([(0, 0)])
    ax = fig.add_subplot(gs[0, 0])
    ax.imshow(raster(S, C, 26, 0, 26), cmap=CMAP, vmin=0, vmax=2,
              interpolation="nearest", aspect="auto")
    ax.set_title("permanence: it fills", fontsize=9)
    ax.set_ylabel("time  " + r"$\rightarrow$", fontsize=9)
    ax.set_xticks([])

    ax = fig.add_subplot(gs[0, 1])
    ax.imshow(sraster(S, C, 26, 0, 26), cmap=CMAP, vmin=0, vmax=2,
              interpolation="nearest", aspect="auto")
    ax.set_title("impermanence: it walks", fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])

    # the longevity dial: one code, speed 2/(tau+1)
    C2 = Const([(0, 1, -1), (0, -1, -1)])
    S2 = state_of([(0, 0), (2, 1)])
    taus, speeds = [], []
    for tau in range(1, 13):
        r = classify_sunset(S2, C2, tau=tau, max_steps=400)
        taus.append(tau)
        speeds.append(abs(r["displacement"]) / r["period"])
    ax = fig.add_subplot(gs[0, 2])
    xs = np.linspace(1, 12, 200)
    ax.plot(xs, 2 / (xs + 1), lw=1.0, color="#9aa3ae", zorder=1,
            label=r"$2/(\tau+1)$")
    ax.plot(taus, speeds, "o", ms=4, color=LINE, zorder=2, label="measured")
    ax.set_xlabel(r"lifetime $\tau$ (steps a law survives unrenewed)",
                  fontsize=8.5)
    ax.set_ylabel("speed", fontsize=9)
    ax.set_title("longevity is friction", fontsize=9)
    ax.legend(fontsize=8, frameon=False)
    ax.set_ylim(0, 1.05)

    # the frontier without the territory
    V = {"O": (0, 0), "E": (1, 0), "N": (0, -1), "P": (1, -1)}
    Cg = Const([tuple(V[c] for c in "OPP"), tuple(V[c] for c in "OEE"),
                tuple(V[c] for c in "ONN")], [(0, 1, 2), (1,), (2,)], dim=2)
    X, ages = state_of([((0, 0), 0)]), None
    for _ in range(16):
        X, ages = step_sunset(X, Cg, 1, ages)
    ax = fig.add_subplot(gs[0, 3])
    ax.imshow(_grid(X), cmap=CMAP, vmin=0, vmax=2, interpolation="nearest")
    ax.set_title("the plane-filler,\nkeeping only its frontier", fontsize=9)
    ax.set_xticks([])
    ax.set_yticks([])

    fig.subplots_adjust(left=0.05, right=0.99, top=0.86, bottom=0.18)
    save(fig, "fig6_impermanence")


def save(fig, stem):
    for ext in ("pdf", "png"):
        fig.savefig(HERE / ("%s.%s" % (stem, ext)), dpi=170)
    plt.close(fig)
    print("wrote %s.{pdf,png}" % stem)


FIGS = {"fig1": fig1, "fig2": fig2, "fig3": fig3, "fig4": fig4,
        "fig5": fig5, "fig6": fig6}

if __name__ == "__main__":
    want = sys.argv[1:] or list(FIGS)
    for name in want:
        print("building", name)
        FIGS[name]()
