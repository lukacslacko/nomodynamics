#!/usr/bin/env python3
"""
paving.py — PAVING NEEDS BREADTH: why the building front must have out-degree 2.

anon.py computes at out-degree 1; anontm.py needs out-degree 2, but only for
the eighteen kinds of the two building fronts.  Is that an artefact of my
design?  No.  It is forced.

    LEMMA (backward paths).  Let C have out-degree <= 1, so the target map
    t : K -> K is a FUNCTION.  A kind-k law can be enacted at cell j only by a
    kind-k' law at j - c_{k'} with t(k') = k.  Hence if a kind-k law stands at
    distance D from the initial support at time T, there is a t-path
    k_L -> k_{L-1} -> ... -> k_0 = k with L >= D / max|c|.  In a finite
    functional graph any forward path longer than n = |K| has entered a cycle
    and can never leave it, so its LAST vertex lies on a cycle.  Therefore:

    PROPOSITION 6.  In an out-degree-<=1 constitution, every kind that is ever
    enacted at distance > n . max|c| from the initial support lies on a CYCLE
    of the amendment digraph, and its only target is the next kind of that
    cycle.

    COROLLARY 6.1.  A statute machine in normal form cannot grow its own
    hardware at out-degree 1.  A self-clearing wire is a 1-cycle (t(w) = w) and
    can be paved; but a gate g has t(g) = w with w != g and t(w) = w, so the
    forward path from g is g -> w -> w -> ... and g never recurs: g is on no
    cycle, and no out-degree-1 constitution can ever enact a g-law on virgin
    ground.

    So the dividing line is exact, and it is the Out-Degree Law's own
    threshold seen from a second side:

        out-degree 1     computes, on the hardware it is given
                         (a linear bounded automaton: THEOREM 4)
        out-degree >= 2  can enact hardware on virgin ground, hence an
                         unbounded tape (THEOREM 5)

    Chapter two: breadth buys MOTION.  Chapter three, here: breadth buys
    MEMORY.  Both are the same threshold.

Run `python3 paving.py`.
"""

from __future__ import annotations

import sys
import os
import random

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from xnomos import Const, state_of, step, laws                     # noqa: E402


def cycle_kinds(targets):
    """The kinds lying on a cycle of the functional graph t."""
    n = len(targets)
    t = [tg[0] for tg in targets]
    on = set()
    for k in range(n):
        seen = {}
        x, i = k, 0
        while x not in seen:
            seen[x] = i
            x = t[x]
            i += 1
        # the cycle is everything from the first repeat onwards
        if x == k or True:
            cyc_start = seen[x]
            if k >= 0:
                pass
        # k is on a cycle iff k is revisited
        y = t[k]
        steps = 1
        while y != k and steps <= n:
            y = t[y]
            steps += 1
        if y == k:
            on.add(k)
    return on


def certify_proposition6(trials=400, seed=41, steps=60, span=6):
    """No non-cycle kind is ever enacted beyond n.max|c| of the initial support.

    A complete run over random out-degree-1 constitutions and random codes.
    """
    rng = random.Random(seed)
    viol = 0
    tested = 0
    far_events = 0
    for _ in range(trials):
        n = rng.randrange(1, 5)
        rules = [(rng.randrange(-1, 2), rng.randrange(-1, 2),
                  rng.randrange(-1, 2)) for _ in range(n)]
        targets = [(rng.randrange(n),) for _ in range(n)]     # out-degree 1
        cited = rng.random() < 0.5
        if cited:
            guards = [(rng.choice([None] + list(range(n))),
                       rng.choice([None] + list(range(n)))) for _ in range(n)]
        else:
            guards = None
        C = Const(rules, targets, dim=1, guards=guards)
        onc = cycle_kinds(targets)
        maxc = max(1, max(abs(r[2]) for r in rules))
        D = n * maxc
        pl = [(rng.randrange(-span, span + 1), rng.randrange(n))
              for _ in range(rng.randrange(1, 8))]
        S = state_of(pl)
        if not S:
            continue
        lo0, hi0 = min(S), max(S)
        tested += 1
        for _ in range(steps):
            S = step(S, C, "parity")
            if not S:
                break
            for cell, k in laws(S):
                d = max(lo0 - cell, cell - hi0, 0)
                if d > D:
                    far_events += 1
                    if k not in onc:
                        viol += 1
    return viol, tested, far_events


def certify_corollary(trials=300, seed=7):
    """In normal form, a gate kind is never on a cycle: check it structurally."""
    rng = random.Random(seed)
    bad = 0
    for _ in range(trials):
        nw = rng.randrange(1, 5)
        ng = rng.randrange(1, 5)
        # kinds 0..nw-1 wires (t(w)=w), nw..nw+ng-1 gates (t(g)=some wire)
        targets = [(i,) for i in range(nw)] + \
                  [(rng.randrange(nw),) for _ in range(ng)]
        onc = cycle_kinds(targets)
        if onc != set(range(nw)):
            bad += 1
    return bad, trials


def demo_front_outdegree():
    """The front of anontm.py: minimum out-degree actually used."""
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from anontm import AnonRegistry
    from turing import tm_busy_beaver3
    R = AnonRegistry(tm_busy_beaver3())
    C = R.M.const()
    front = [k for k in range(C.n) if R.M.names[k] in R.M.raw_kinds]
    outs = sorted(len(C.targets[k]) for k in front)
    rest = max(len(C.targets[k]) for k in range(C.n) if k not in front)
    return outs, rest, len(front), C.n


def _main():
    print("PAVING NEEDS BREADTH")
    viol, tested, far = certify_proposition6()
    print("  Proposition 6: %d random out-degree-1 constitutions x random "
          "codes x 60 steps" % tested)
    print("     %d law-sightings beyond n.max|c| of the initial support; "
          "%d of them" % (far, viol))
    print("     were of a kind NOT on a cycle of the amendment digraph "
          "(expected 0)")
    assert viol == 0
    bad, n = certify_corollary()
    print("  Corollary 6.1: in %d random normal-form target maps the cycle "
          "set is" % n)
    print("     exactly the wires, never a gate (%d exceptions)" % bad)
    assert bad == 0
    outs, rest, nf, tot = demo_front_outdegree()
    print("  the anonymous TM front: %d kinds of %d, out-degrees %s;" %
          (nf, tot, outs))
    print("     every other kind has out-degree %d.  Proposition 6 says the "
          "front" % rest)
    print("     CANNOT be flattened to out-degree 1: gates lie on no cycle.")
    print("paving self-tests passed")


if __name__ == "__main__":
    _main()
