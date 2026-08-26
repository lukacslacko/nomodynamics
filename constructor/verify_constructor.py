#!/usr/bin/env python3
"""
verify_constructor.py — the verification battery of Expedition Z-A.

Re-checks every claim of constructor/RESULTS.md.  Two engines throughout:
`xnomos.step` (dict of bitmasks) and `replib.pstep` (frozenset of placed laws),
which share no code.

    python3 verify_constructor.py          # ~40 s
    python3 verify_constructor.py -v       # ... printing frames

Sections:
    A  the constitution audit (raw Const, no trust in the builder)
    B  the rung-4c certificate: Phi^p and Phi^2p, exact, on both engines
    C  causal components and freedom, from an independent splitter
    D  the colony (rung 4c+)
    E  the anti-Fredkin bar: N1, N2, the citation ablation, discrimination
    F  THE REMOVAL: the one-directional traveller (rung 4a)
    G  the negative controls
"""

from __future__ import annotations

import itertools
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "replication"))

from xnomos import Const, state_of, step, card, laws, active_laws     # noqa
from replib import to_p, pstep, from_p, radius, dist_inf              # noqa
from artificer import (build, seed, read_row, clerks, run, frame,     # noqa
                       Kinds, SYMS, HANDS)

VERBOSE = "-v" in sys.argv
FAIL = []
NCHECK = 0


def check(name, cond, detail=""):
    global NCHECK
    NCHECK += 1
    print("  [%s] %-58s %s" % ("ok" if cond else "FAIL", name, detail))
    if not cond:
        FAIL.append(name)
    return cond


# ---------------------------------------------------------------- primitives

def supp(S):
    return set(S)


def components(S, R):
    """Causal components: maximal clusters of occupied cells under the relation
    `sup-distance <= 2R`.  Written from the definition, independent of replib."""
    cells = sorted(S)
    parent = {c: c for c in cells}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for i, a in enumerate(cells):
        for b in cells[i + 1:]:
            if max(abs(a[0] - b[0]), abs(a[1] - b[1])) <= 2 * R:
                ra, rb = find(a), find(b)
                if ra != rb:
                    parent[ra] = rb
    out = {}
    for c in cells:
        out.setdefault(find(c), {})[c] = S[c]
    return list(out.values())


def is_translate(A, B):
    """Is state A an exact translate of state B?  Returns the offset or None."""
    if len(A) != len(B) or sorted(A.values()) != sorted(B.values()):
        return None
    a0 = min(A)
    b0 = min(B)
    d = (a0[0] - b0[0], a0[1] - b0[1])
    if {(c[0] + d[0], c[1] + d[1]): m for c, m in B.items()} == A:
        return d
    return None


def mirror_state(K, S):
    """Reflect a state in the x axis AND swap the handedness of every clerk kind
    -- the involution under which THE SUCCESSION's constitution is invariant is
    y -> -y (up/down relay swap), which is what §1.3's mirror clause needs.  Used
    only as a cross-check on §2.2."""
    swap = {}
    for h in HANDS:
        for nm in ("A_", "B_"):
            swap[K[nm + h]] = K[nm + ("L" if h == "R" else "R")]
    return swap


def linmap(S, C):
    """L: the UNCONDITIONAL linear map -- every placed law fires, guards ignored,
    toggles resolved by parity.  F2-linear by construction."""
    from collections import defaultdict
    tog = defaultdict(int)
    for cell, k in laws(S):
        _, _, c = C.rules[k]
        j = C.add(cell, c)
        for t in C.targets[k]:
            tog[j] ^= 1 << t
    out = dict(S)
    for j, x in tog.items():
        m = out.get(j, 0) ^ x
        if m:
            out[j] = m
        elif j in out:
            del out[j]
    return out


def sym_diff(A, B):
    out = {}
    for c in set(A) | set(B):
        m = A.get(c, 0) ^ B.get(c, 0)
        if m:
            out[c] = m
    return out


WORDS_SHORT = ["".join(t) for L in (1, 2, 3, 4)
               for t in itertools.product("01", repeat=L)]
RNG = random.Random(20260826)
WORDS_LONG = ["".join(RNG.choice("01") for _ in range(L))
              for L in (5, 6, 7, 8, 9, 11, 13, 16, 20, 24, 32)]
WORDS = WORDS_SHORT + WORDS_LONG


# ======================================================================= A
def section_A():
    print("\nA. THE CONSTITUTION AUDIT  (read off the raw Const)")
    K, C = build()
    check("kind count = 73", len(K) == 73 and C.n == 73, "n = %d" % C.n)
    check("dimension 2, no modulus", C.dim == 2 and C.modulus is None)
    R = radius(C)
    check("interaction radius R = 1", R == 1,
          "every offset in {-1,0,1}^2, so free means gap > 2")
    # every guard reads its own cell only
    own = all(C.rules[k][0] == (0, 0) and C.rules[k][1] == (0, 0)
              for k in range(C.n))
    check("every guard reads ONLY its own cell (a = b = (0,0))", own)
    # the four blueprint/marker kinds are dead letters
    dead = all(C.guards[K["SYM_" + s]][0] == K["NIL"] for s in SYMS)
    check("the 4 charter kinds are DEAD LETTERS (guard cites the phantom)", dead)
    # NIL is never a target and never seeded
    nil_t = not any(K["NIL"] in C.targets[k] for k in range(C.n)
                    if k != K["NIL"])
    check("the phantom NIL is nobody's target", nil_t)
    S = seed(K, "011")
    check("the phantom NIL is not in the seed",
          all(not ((m >> K["NIL"]) & 1) for m in S.values()))
    # citation: how many guards name a kind?
    named = sum(1 for g, h in C.guards if g is not None or h is not None)
    cite_blueprint = sum(1 for k in range(C.n)
                         if C.guards[k][0] in (K["SYM_X"], K["SYM_Y"],
                                               K["SYM_L"], K["SYM_Z"])
                         or C.guards[k][1] in (K["SYM_X"], K["SYM_Y"],
                                               K["SYM_L"], K["SYM_Z"]))
    check("every guard is a CITATION (names a kind)", named == C.n,
          "%d / %d" % (named, C.n))
    check("guards naming a charter kind (the reading apparatus)",
          cite_blueprint == 18,
          "%d: 8 T, 4 E, 2 B (vacancy), 4 S" % cite_blueprint)
    # out-degree
    od = max(len(t) for t in C.targets)
    check("max out-degree = 16 (>= 2, as the Out-Degree Law demands for motion)",
          od == 16, "max |T_k| = %d" % od)
    # seed structure independent of blueprint
    mach = []
    for w in ("0", "1"):
        Sw = seed(K, w)
        mach.append(tuple(sorted((c, m & ~sum(1 << K["SYM_" + s]
                                              for s in ("X", "Y")))
                                 for c, m in Sw.items())))
    check("the machinery is blueprint-independent", mach[0] == mach[1])
    return K, C, R


# ======================================================================= B
def section_B(K, C, R):
    print("\nB. THE RUNG-4c CERTIFICATE   Phi^p(S) = sigma^(0,3) Sbar "
          "+ sigma^(0,-3) Sbar")
    ok_all = True
    rows = []
    for w in WORDS:
        n = len(w)
        p = n + 4
        S0 = seed(K, w)
        want1 = {}
        for dy in (3, -3):
            for c, m in seed(K, w, "L", dy).items():
                want1[c] = want1.get(c, 0) | m
        want2 = {}
        for dy in (-6, 0, 6):
            for c, m in seed(K, w, "R", dy).items():
                want2[c] = want2.get(c, 0) | m
        g1 = run(C, S0, p)
        g2 = run(C, S0, 2 * p)
        h1 = run(C, S0, p, engine="pstep")
        h2 = run(C, S0, 2 * p, engine="pstep")
        good = (g1 == want1 and g2 == want2 and h1 == want1 and h2 == want2)
        ok_all &= good
        rows.append((w, n, p, card(S0), card(g1), card(g2), good))
    check("Phi^p exact + Phi^2p exact, BOTH ENGINES, %d blueprints "
          "(lengths 1-32)" % len(WORDS), ok_all)
    for w, n, p, c0, c1, c2, good in rows[:4] + rows[-4:]:
        print("        w=%-33s n=%2d p=%2d  card %3d -> %3d -> %3d  %s"
              % (w, n, p, c0, c1, c2, "ok" if good else "FAIL"))
    # debris is empty, stated explicitly
    w = "011"
    S0 = seed(K, w)
    Sp = run(C, S0, len(w) + 4)
    kids = {}
    for dy in (3, -3):
        for c, m in seed(K, w, "L", dy).items():
            kids[c] = kids.get(c, 0) | m
    check("debris = EMPTY (Phi^p minus the two children)",
          sym_diff(Sp, kids) == {})
    # the parent is gone
    check("the parent charter is GONE at t = p "
          "(rows -2..+2 hold nothing at all)",
          all(abs(c[1]) > 2 for c in Sp))
    check("card dips BELOW the seed before fission (true fission, not budding)",
          min(card(run(C, S0, t)) for t in range(len(w) + 5)) < card(S0),
          "min card = %d < %d" % (min(card(run(C, S0, t))
                                      for t in range(len(w) + 5)), card(S0)))


# ======================================================================= C
def section_C(K, C, R):
    print("\nC. CAUSAL COMPONENTS AND FREEDOM  (independent splitter, gap > 2R)")
    for w in ("011", "1001", "01101001"):
        n = len(w)
        p = n + 4
        S0 = seed(K, w)
        Sp = run(C, S0, p)
        comps = components(Sp, R)
        tgt = seed(K, w, "L", 0)
        offs = [is_translate(cc, tgt) for cc in comps]
        d = min(dist_inf(set(a), set(b), 2)
                for i, a in enumerate(comps) for b in comps[i + 1:])
        ok = (len(comps) == 2 and all(o is not None for o in offs) and d > 2 * R)
        check("w=%-9s : 2 components, each an exact translate, gap %d > 2R = %d"
              % (w, d, 2 * R), ok,
              "offsets %s" % sorted(offs))
        if w == "011":
            for i, cc in enumerate(sorted(comps, key=lambda x: -min(x)[1])):
                print("        copy %d: cells %s" % (i, sorted(cc)[:2] + ["..."] +
                                                     sorted(cc)[-1:]))
                print("                blueprint read back: %r"
                      % read_row(K, cc, min(cc)[1], n))
                print("                clerk: %s" % clerks(K, cc))


# ======================================================================= D
def section_D(K, C, R):
    print("\nD. THE COLONY  (rung 4c+)")
    for w in ("011", "1001"):
        n = len(w)
        p = n + 4
        S0 = seed(K, w)
        S = dict(S0)
        Sp = to_p(S0)
        counts = []
        ok = True
        for g in range(0, 13):
            if g:
                S = run(C, S, p)
                for _ in range(p):
                    Sp = pstep(Sp, C, "or")
            ok &= (from_p(Sp) == S)
            comps = components(S, R)
            tgt = seed(K, w, "R" if g % 2 == 0 else "L", 0)
            allc = all(is_translate(cc, tgt) is not None for cc in comps)
            reads = all(read_row(K, cc, min(cc)[1], n) == w for cc in comps)
            gap = min([dist_inf(set(a), set(b), 2)
                       for i, a in enumerate(comps) for b in comps[i + 1:]]
                      or [99])
            ok &= allc and reads and gap > 2 * R and len(comps) == g + 1
            ok &= (card(S) == (g + 1) * card(S0))
            counts.append(len(comps))
        check("w=%-6s : generation g holds EXACTLY g+1 free exact charters, "
              "g = 0..12" % w, ok, "counts %s" % counts)


# ======================================================================= E
def section_E(K, C, R):
    print("\nE. THE ANTI-FREDKIN BAR  (§1.4)")

    # -- N1 -----------------------------------------------------------------
    w = "011"
    n = len(w)
    p = n + 4
    S0 = seed(K, w)
    S, Ls = dict(S0), dict(S0)
    diff = 0
    for t in range(1, 3 * p + 1):
        S = step(S, C, "or")
        Ls = linmap(Ls, C)
        if S != Ls:
            diff += 1
    check("N1  the guard bites: Phi^t != L^t", diff == 3 * p,
          "%d / %d steps differ" % (diff, 3 * p))

    # -- N2: the splitting test --------------------------------------------
    pairs = list(laws(S0))
    fails = 0
    tot = 0
    tests = []
    for i in range(len(pairs)):                      # split one law off
        tests.append({pairs[i]})
    tests.append({(c, k) for c, k in pairs           # machinery vs blueprint
                  if k not in (K["SYM_X"], K["SYM_Y"])})
    rr = random.Random(7)
    for _ in range(40):
        tests.append({x for x in pairs if rr.random() < .5})
    target = run(C, S0, p)
    for A in tests:
        if not A or len(A) == len(pairs):
            continue
        B = set(pairs) - A
        tot += 1
        got = sym_diff(run(C, state_of(A), p), run(C, state_of(B), p))
        if got != target:
            fails += 1
    check("N2  the splitting test: Phi^p(S) != Phi^p(A) D Phi^p(B)",
          fails > 0, "%d / %d splittings fail superposition" % (fails, tot))

    # -- the witness --------------------------------------------------------
    A = {((1, 0), K["SYM_X"])}                        # one blueprint symbol
    B = set(pairs) - A
    got = sym_diff(run(C, state_of(A), p), run(C, state_of(B), p))
    check("N2 witness: remove ONE blueprint law and the children change",
          got != target,
          "|Phi^p(A) D Phi^p(B)| = %d vs |Phi^p(S)| = %d"
          % (card(got), card(target)))

    # -- the citation ablation ---------------------------------------------
    K2, C2 = build(cite_symbols=False)
    S20 = seed(K2, w)
    S2 = run(C2, S20, p)
    comps2 = components(S2, R)
    tgt2 = seed(K2, w, "L", 0)
    good2 = [cc for cc in comps2 if is_translate(cc, tgt2) is not None]
    frozen = (run(C2, S20, p) == run(C2, S20, p + 1))
    check("ABLATION (any,any) -- every guard naming a charter kind "
          "anonymised: NO copy, and frozen",
          len(good2) == 0 and frozen,
          "%d components, %d exact copies, card %d, fixed point: %s"
          % (len(comps2), len(good2), card(S2), frozen))

    K3, C3 = build(cite_symbols="blind")
    S3 = run(C3, seed(K3, w), p)
    comps3 = components(S3, R)
    tgt = seed(K3, w, "L", 0)
    good3 = [cc for cc in comps3 if is_translate(cc, tgt) is not None]
    reads3 = {read_row(K3, cc, min(cc)[1], n) for cc in comps3}
    check("ABLATION (blind precedent): the clerk still walks but the "
          "blueprint is DESTROYED",
          len(good3) == 0 and w not in reads3,
          "%d components, 0 exact copies, decoded rows %s"
          % (len(comps3), sorted(str(x) for x in reads3)))

    # -- blueprint discrimination ------------------------------------------
    bad = 0
    for w1, w2 in itertools.combinations(WORDS_SHORT, 2):
        if len(w1) != len(w2):
            continue
        pp = len(w1) + 4
        a = run(C, seed(K, w1), pp)
        b = run(C, seed(K, w2), pp)
        if a == b:
            bad += 1
    check("DISCRIMINATION: distinct blueprints give distinct children",
          bad == 0, "%d collisions over all same-length pairs, |w| <= 4" % bad)
    # decoder recovers w from the child
    dec = all(read_row(K, run(C, seed(K, ww), len(ww) + 4), 3, len(ww)) == ww
              for ww in WORDS)
    check("the decoder recovers w from the CHILD, all %d blueprints"
          % len(WORDS), dec)


# ======================================================================= F
def section_F():
    print("\nF. THE REMOVAL  (one direction only -- rung 4a, the traveller)")
    K, C = build(dirs=("u",))
    R = radius(C)
    check("kind count = 43, R = 1", len(K) == 43 and R == 1, "n = %d" % len(K))
    ok = True
    rows = []
    for w in WORDS_SHORT + WORDS_LONG[:5]:
        n = len(w)
        p = n + 4
        S0 = seed(K, w)
        g1 = run(C, S0, p)
        g2 = run(C, S0, 2 * p)
        h2 = run(C, S0, 2 * p, engine="pstep")
        want1 = seed(K, w, "L", 3)
        want2 = seed(K, w, "R", 6)
        good = (g1 == want1 and g2 == want2 and h2 == want2)
        ok &= good
        rows.append((w, good))
    check("Phi^p(S) = sigma^(0,3) Sbar  and  Phi^2p(S) = sigma^(0,6) S, "
          "EXACTLY, both engines, %d blueprints" % len(rows), ok)
    # it is a glider in the strict sense at period 2p
    w = "01101001"
    p = len(w) + 4
    S0 = seed(K, w)
    S = dict(S0)
    good = True
    for j in range(1, 7):
        S = run(C, S, 2 * p)
        good &= (S == seed(K, w, "R", 6 * j))
    check("a GLIDER: Phi^{2p k}(S) = sigma^(0,6k) S for k = 1..6, "
          "card constant, debris none", good,
          "card %d at every k" % card(S))
    # and it reads
    K3, C3 = build(dirs=("u",), cite_symbols="blind")
    S3 = run(C3, seed(K3, w), 2 * (len(w) + 4))
    check("blind ablation destroys it (so the packet READS while it moves)",
          S3 != seed(K3, w, "R", 6))


# ======================================================================= G
def section_G(K, C, R):
    print("\nG. NEGATIVE CONTROLS")
    # parity kills the colony (Z-A-4)
    w = "011"
    n = len(w)
    p = n + 4
    S0 = seed(K, w)
    par1 = run(C, S0, p, mode="parity")
    kids = {}
    for dy in (3, -3):
        for c, m in seed(K, w, "L", dy).items():
            kids[c] = kids.get(c, 0) | m
    check("under PARITY generation 1 is still exact (no coincident writes yet)",
          par1 == kids)
    par2 = run(C, S0, 2 * p, mode="parity")
    want2 = {}
    for dy in (-6, 0, 6):
        for c, m in seed(K, w, "R", dy).items():
            want2[c] = want2.get(c, 0) | m
    check("under PARITY generation 2 CANCELS its middle child "
          "(so OR is load-bearing)", par2 != want2,
          "card %d vs %d expected under OR" % (card(par2), card(want2)))
    comps = components(par2, R)
    print("        parity gen 2: %d components, cards %s"
          % (len(comps), sorted(card(c) for c in comps)))
    # Lemma S sanity: two far-apart seeds superpose
    A = seed(K, "011", "R", 0)
    B = seed(K, "1001", "R", 400)
    U = dict(A)
    for c, m in B.items():
        U[c] = U.get(c, 0) | m
    ok = True
    SU, SA, SB = dict(U), dict(A), dict(B)
    for _ in range(20):
        SU, SA, SB = (step(SU, C, "or"), step(SA, C, "or"), step(SB, C, "or"))
        merged = dict(SA)
        for c, m in SB.items():
            merged[c] = merged.get(c, 0) | m
        ok &= (SU == merged)
    check("Lemma S control: two far-apart charters superpose exactly, 20 steps",
          ok)
    # engine agreement on a long random orbit
    rr = random.Random(11)
    ok = True
    for trial in range(6):
        w = "".join(rr.choice("01") for _ in range(rr.randrange(1, 7)))
        S = seed(K, w)
        P = to_p(S)
        for _ in range(40):
            S = step(S, C, "or")
            P = pstep(P, C, "or")
            if from_p(P) != S:
                ok = False
                break
    check("the two engines agree step-by-step, 6 orbits x 40 steps", ok)


if __name__ == "__main__":
    print("=" * 74)
    print("Expedition Z-A -- verification battery for constructor/RESULTS.md")
    print("=" * 74)
    K, C, R = section_A()
    section_B(K, C, R)
    section_C(K, C, R)
    section_D(K, C, R)
    section_E(K, C, R)
    section_F()
    section_G(K, C, R)
    print("\n" + "=" * 74)
    if FAIL:
        print("FAILED %d of %d checks: %s" % (len(FAIL), NCHECK, FAIL))
        sys.exit(1)
    print("ALL %d CHECKS PASSED" % NCHECK)
