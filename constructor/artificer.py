#!/usr/bin/env python3
"""
artificer.py — THE SUCCESSION: a blueprint-carrying constructor.

Expedition Z-A.  Chapter six of nomodynamics: von Neumann's rung 4.

THE OBJECT.  A *charter* is one row of ℤ²:

        L  s1 s2 ... sn  Z              symbols s_i in {X, Y}  ("0" / "1")

together with a *clerk* — a bundle of ~16 placed laws sitting in ONE cell of
that row.  The clerk walks the charter, and as it walks it does four things at
each cell, all in one step:

    A   clears its own bundle from the cell it stands on;
    B   re-enacts its own bundle one cell along  (unless the end marker of its
        own handedness stands here — a CITATION in a vacancy clause);
    T_s cites the symbol s standing in its own cell BY NAME and fires a
        two-stage relay one row up and one row down;
    E_s cites the same symbol and ERASES it.

The relay (`riser`) is four kinds per payload per direction: at each stage a
`C` law clears the stage's own pair from its cell and a `W` law writes the next
stage one row further out.  After two stages the payload is deposited THREE
rows away, and both intermediate rows are empty again on the very next step.

So the charter is consumed from one end and re-issued, in duplicate, three rows
up and three rows down.  Three rows is `3R`, and the gap that opens is `6 > 2R`:
the two children are **free**, in the sense of Lemma S, at the instant the last
symbol lands.  When the clerk reaches the end marker it fires one further
relay whose payload is a whole clerk bundle of the OPPOSITE handedness, which
lands on the child's far end exactly as the child's last symbol does.

    Φ^{n+4}(S(w))  =  σ^{(0,+3)} S̄(w)  ⊔  σ^{(0,−3)} S̄(w)        exactly
    Φ^{2(n+4)}(S(w))  =  σ^{(0,−6)}S(w) ⊔ S(w) ⊔ σ^{(0,+6)}S(w)   exactly

with `S̄` the mirror-handed charter.  Resolution is OR: two neighbouring copies
write the same child into the same cells at the same step, and OR makes those
coincident writes merge instead of cancel (under parity they annihilate — see
`replication/RESULTS.md` §3.1a for the same phenomenon in THE SPLIT DECISION).

Directions can be restricted to one side, giving THE REMOVAL: a charter that
walks three rows per generation, carrying and re-reading its blueprint forever,
leaving nothing behind — rung 4a.

Run:  python3 artificer.py
"""

from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "replication"))

from xnomos import Const, state_of, step, card                      # noqa: E402
from replib import to_p, pstep, from_p, radius                      # noqa: E402


# ------------------------------------------------------------------ the kinds

SYMS = ("X", "Y", "L", "Z")          # blueprint 0, blueprint 1, left end, right end
PAYLOADS = SYMS + ("CL", "CR")       # relay payloads: a symbol, or a clerk bundle
HANDS = ("R", "L")                   # right-handed (walks east), left (walks west)


class Kinds:
    """Name <-> index table for one build."""

    def __init__(self, dirs=("u", "d")):
        self.dirs = tuple(dirs)
        self.names = []
        self.idx = {}
        self._add("NIL")                                   # phantom: never placed
        for s in SYMS:
            self._add("SYM_" + s)                          # the inert tape symbols
        # the clerk: handed parts
        for h in HANDS:
            self._add("A_" + h)                            # clear own bundle here
            self._add("B_" + h)                            # write own bundle along
            for d in self.dirs:
                self._add("S_%s_%s" % (h, d))              # birth the other clerk
        # the clerk: the reading apparatus, shared by both handednesses
        for s in SYMS:
            for d in self.dirs:
                self._add("T_%s_%s" % (s, d))              # cite s, fire the relay
            self._add("E_" + s)                            # cite s, erase s
        # the relays
        for p in PAYLOADS:
            for d in self.dirs:
                for st in (1, 2):
                    self._add("RC_%s_%s_%d" % (p, d, st))  # clear this stage here
                    self._add("RW_%s_%s_%d" % (p, d, st))  # write next stage out

    def _add(self, name):
        self.idx[name] = len(self.names)
        self.names.append(name)

    def __getitem__(self, name):
        return self.idx[name]

    def __len__(self):
        return len(self.names)

    def bundle(self, h):
        """The kinds a clerk of handedness h consists of."""
        out = ["A_" + h, "B_" + h]
        out += ["S_%s_%s" % (h, d) for d in self.dirs]
        for s in SYMS:
            out += ["T_%s_%s" % (s, d) for d in self.dirs]
            out.append("E_" + s)
        return tuple(self[x] for x in out)


O = (0, 0)
NORTH = (0, 1)
SOUTH = (0, -1)
EAST = (1, 0)
WEST = (-1, 0)
DIRVEC = {"u": NORTH, "d": SOUTH}
STEPVEC = {"R": EAST, "L": WEST}
ENDMARK = {"R": "Z", "L": "L"}          # the marker that halts a clerk of this hand
OTHER = {"R": "L", "L": "R"}


def build(dirs=("u", "d"), cite_symbols=True):
    """THE SUCCESSION.

    `cite_symbols` is the ablation dial of §1.4(c).  Offsets, targets, seed and
    mode are IDENTICAL in every setting; only the guards move:

      True     the machine as designed;
      'blind'  the reading apparatus (T_s, E_s, S_h) keeps its vacancy clause
               but its precedent becomes the anonymous `any` — the clerk still
               walks and still fires relays, but can no longer tell one symbol
               from another;
      False    every guard naming a blueprint kind becomes `(any, any)` — the
               one-line control `citation/RESULTS.md` §5.6 runs on THE LEDGER.
    """
    blind = (cite_symbols == "blind")
    K = Kinds(dirs)
    n = len(K)
    NIL = K["NIL"]
    rules = [(O, O, O)] * n
    targets = [(k,) for k in range(n)]   # default: own kind (never fires anyway)
    guards = [(NIL, NIL)] * n           # default: never active (cites the phantom)

    def law(name, a, b, c, g, h, tgt):
        k = K[name]
        rules[k] = (a, b, c)
        guards[k] = (g, h)
        targets[k] = tuple(tgt)

    # -- the tape symbols are DEAD LETTERS: their guard cites the phantom.
    #    (left as the default)

    # -- the clerk ---------------------------------------------------------
    for h in HANDS:
        bund = K.bundle(h)
        # A: "while I stand here, repeal my whole bundle here"
        law("A_" + h, O, O, O, K["A_" + h], NIL, bund)
        # B: "while I stand here and the end marker of my hand does NOT,
        #     enact my whole bundle one cell along"
        law("B_" + h, O, O, STEPVEC[h], K["B_" + h],
            K["SYM_" + ENDMARK[h]], bund)
        # S: "while my end marker stands here, fire a relay carrying a clerk
        #     of the opposite hand"
        for d in dirs:
            pay = "C" + OTHER[h]
            law("S_%s_%s" % (h, d), O, O, DIRVEC[d],
                None if (blind or not cite_symbols) else K["SYM_" + ENDMARK[h]],
                None if cite_symbols is False else NIL,
                (K["RC_%s_%s_1" % (pay, d)], K["RW_%s_%s_1" % (pay, d)]))

    # -- the reading apparatus --------------------------------------------
    for s in SYMS:
        g = None if (blind or not cite_symbols) else K["SYM_" + s]
        hh = None if cite_symbols is False else NIL
        for d in dirs:
            law("T_%s_%s" % (s, d), O, O, DIRVEC[d], g, hh,
                (K["RC_%s_%s_1" % (s, d)], K["RW_%s_%s_1" % (s, d)]))
        law("E_" + s, O, O, O, g, hh, (K["SYM_" + s],))

    # -- the relays --------------------------------------------------------
    for p in PAYLOADS:
        if p in SYMS:
            payload = (K["SYM_" + p],)
        else:
            payload = K.bundle(p[1])           # "CL" -> left bundle, "CR" -> right
        for d in dirs:
            for st in (1, 2):
                c_name = "RC_%s_%s_%d" % (p, d, st)
                w_name = "RW_%s_%s_%d" % (p, d, st)
                pair = (K[c_name], K[w_name])
                law(c_name, O, O, O, K[c_name], NIL, pair)
                if st == 1:
                    nxt = (K["RC_%s_%s_2" % (p, d)], K["RW_%s_%s_2" % (p, d)])
                    law(w_name, O, O, DIRVEC[d], K[w_name], NIL, nxt)
                else:
                    law(w_name, O, O, DIRVEC[d], K[w_name], NIL, payload)

    return K, Const(rules, targets, dim=2, guards=guards)


# ------------------------------------------------------------------ the seeds

def seed(K, w, hand="R", y=0, x=0):
    """The charter `L w Z` on row y with a clerk of handedness `hand` on the
    marker that clerk starts from (L for a right-hander, Z for a left-hander)."""
    n = len(w)
    pairs = [((x, y), K["SYM_L"]), ((x + n + 1, y), K["SYM_Z"])]
    for i, ch in enumerate(w):
        pairs.append(((x + i + 1, y), K["SYM_X" if ch == "0" else "SYM_Y"]))
    home = x if hand == "R" else x + n + 1
    for k in K.bundle(hand):
        pairs.append(((home, y), k))
    return state_of(pairs)


def read_row(K, S, y, n, x0=0):
    """Decode row y back to a blueprint string, or None if it is not a charter."""
    out = []
    for x in range(x0, x0 + n + 2):
        m = S.get((x, y), 0)
        for s in SYMS:
            if (m >> K["SYM_" + s]) & 1:
                out.append({"X": "0", "Y": "1", "L": "[", "Z": "]"}[s])
                break
        else:
            out.append(".")
    txt = "".join(out)
    if len(txt) >= 2 and txt[0] == "[" and txt[-1] == "]" and \
            all(ch in "01" for ch in txt[1:-1]):
        return txt[1:-1]
    return None


def clerks(K, S):
    """Where the clerk bundles are: {(cell, hand)}."""
    out = []
    for h in HANDS:
        b = K.bundle(h)
        mask = 0
        for k in b:
            mask |= 1 << k
        for cell, m in S.items():
            if m & mask == mask:
                out.append((cell, h))
    return sorted(out)


# ------------------------------------------------------------------ the engine

def run(C, S, t, mode="or", engine="xnomos"):
    if engine == "xnomos":
        S = dict(S)
        for _ in range(t):
            S = step(S, C, mode)
        return S
    P = to_p(S)
    for _ in range(t):
        P = pstep(P, C, mode)
    return from_p(P)


def frame(K, S, box, mark=True):
    """ASCII frame.  '0'/'1'/'['/']' = charter symbols, '>' / '<' = clerk,
    ':' = relay in flight, '#' = clerk sitting on a symbol."""
    x0, x1, y0, y1 = box
    cl = dict(clerks(K, S))
    rows = []
    for y in range(y1, y0 - 1, -1):
        line = []
        for x in range(x0, x1 + 1):
            m = S.get((x, y), 0)
            sym = None
            for s in SYMS:
                if (m >> K["SYM_" + s]) & 1:
                    sym = {"X": "0", "Y": "1", "L": "[", "Z": "]"}[s]
                    break
            hand = cl.get((x, y))
            if hand and sym:
                line.append("#")
            elif hand:
                line.append(">" if hand == "R" else "<")
            elif sym:
                line.append(sym)
            elif m:
                line.append(":")
            else:
                line.append(".")
        rows.append("".join(line))
    return rows


if __name__ == "__main__":
    K, C = build()
    print("THE SUCCESSION")
    print("  kinds = %d   R = %d   dim = 2   mode = or" % (len(K), radius(C)))
    w = "011"
    S = seed(K, w)
    n = len(w)
    print("  blueprint %r   seed card = %d   period n+4 = %d" % (w, card(S), n + 4))
    print()
    box = (-1, n + 3, -5, 5)
    for t in range(0, n + 6):
        print("   t=%2d  card=%3d" % (t, card(S)))
        for r in frame(K, S, box):
            print("         " + r)
        S = step(S, C, "or")
