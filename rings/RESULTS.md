# Nomic Rings: the finite constitution theory
### Expedition N-C results — 2026-08-26
*System: window-1 nomic chain on Z/m (NOMOS.md). State = per position a subset of
the 27 law-kinds (a,b,c) in {-1,0,1}^3; law (i,(a,b,c)) active iff i+a occupied and
i+b empty (mod m); active laws toggle their own kind at i+c; synchronous, parity
resolution. Code: `ring.py` (engine, self-testing), `fixedpoints.py`, `attractors.py`,
`cycles.py`, `hunt2.py`, `eden.py`; data in `*.json`, logs in `*.log`.*

---

## 0. Two structural lemmas that reorganize everything

**Lemma 0 (Single-Author Lemma).** For every slot (position j, kind k) there is at
most one law in the universe that could ever toggle it: the kind-k law at position
j - c(k). *Proof:* a law toggles its own kind at offset c, and c is part of the
kind; two same-kind laws at different positions target different positions (adding
c is a bijection of Z/m). Two laws at one position with different kinds target
different kinds. So the toggle multiset has multiplicity <= 1, always, on every
ring and on the chain. (Engine `step_ref` asserts this on every call; never fired.)

**Corollary (resolution vacuity).** Parity resolution == OR resolution == "any
sensible resolution": there is never a collision to resolve. The variant axis
"PARITY vs OR" collapses at window 1 — every census below covers both verbatim.

**Lemma 0'(guard triage).** Of the 27 kinds, **15 are unconditional dead letters**
(never active anywhere): the 9 with b=0 (their vacancy-guard reads their own
occupied cell) and the 6 more with a=b (self-contradictory guard "occupied and
empty"). The **12 live kinds** are (0,±1,c) — "while my neighbor's seat is
vacant" — and (±1,∓1,c) — edge-sensing. A cell flanked by two occupied cells has
0 active kinds; any occupied cell with an empty neighbor has exactly **6** active
kinds (2 guard-pairs × 3 effects).

## 1. Fixed-point algebra: the Dead Letter Theorem

**Theorem 1 (Dead Letter Theorem).** A code S is a fixed point iff **every law in
S is blocked** (guard unsatisfied). Under parity the general condition is "every
slot receives an even number of toggles", and by Lemma 0 even means zero.

**Corollary: balanced constitutions DO NOT EXIST.** No code is alive-but-
stationary; stability = total gridlock, on every ring m and on Z. The two
pre-registered stability species collapse to one. (Dynamic confirmation: 16,800
random-seed attractors, every fixed attractor had 0 active laws.) The exclusion is
architectural: balance needs two same-kind laws sharing a target, impossible
whenever the effect offset is a function of the actor's kind. Balance becomes
*possible* only in variants that erase the actor's identity from its effect —
e.g. effects that toggle occupancy / the target's kinds, or multiset law-books.
This is the sharpest known boundary of the window-1 crystal stratum.

**Exact counts.** Blockedness of (i,(a,b,c)) depends only on (a,b) and occupancy
of i-1,i,i+1 (c is free!). Per occupied cell, allowed nonempty masks:
beta = 2^27 - 1 if flanked, alpha = 2^21 - 1 if any neighbor is empty. Hence

F(m) = sum over occupancy patterns O of prod_{i in O} (alpha or beta) = tr(T^m)

with a 4x4 transfer matrix; char poly = l * (l^3 - 2^27 l^2 + (beta-alpha) l +
alpha(beta-alpha)), so F(m) = l1^m + l2^m + l3^m for m >= 3; m=1: 2^27 (every
1-ring state is fixed — time stops on a one-cell ring); m=2: 1 + 2 alpha + beta^2.

| m | F(m) (exact) | non-fixed fraction of 2^27m |
|---|--------------|------------------------------|
| 1 | 134217728 = 2^27 | 0 |
| 2 | 18014398245240832 | 1.49e-8 |
| 3 | 2417851585199257356861440 | 2.24e-8 |
| 4 | 324518543989381458950944781762560 | 2.98e-8 |
| 5..24 | exact big ints in fixedpoints.py output; log2 F(m) = 27m - o(1) | ~ m * 7.45e-9 |

Non-fixed fraction ~= m * 2^-27: **under the uniform measure the state space is
glass** — almost every code is already a frozen constitution (overwhelmingly the
fully-occupied gridlock of the chain's Gridlock Theorem). All dynamics, and all of
natural history, lives in the sparse sector.

**Law-count refinement** (alpha -> (1+x)^21 - 1, beta -> (1+x)^27 - 1): exact
number of stable constitutions with n laws, any m (table for n<=6, m<=12 in the
output). **Brute-force verification:** enumeration of ALL codes with <=4 laws on
m<=4 and <=3 laws on m<=6 (46.6M codes) matches the generating function exactly,
class by class; step()-verification on m=3 confirms fixed <=> blocked <=> 0 active.

**Minimal stable constitutions.**
- **1 law** suffices: 21 of 27 kinds are blocked in isolation (the 6 self-starters
  (0,±1,c) are not). Purest specimen: the *unsatisfiable statute* (1,1,1) —
  "while my right neighbor exists and does not exist…" — stable in any context.
- **Smallest taut constitution** (fixed, but deleting any law destabilizes what
  remains): **2 laws — the Mutual-Veto Constitution**: adjacent cells i, i+1 with
  a (0,+1,c) law at i and a (0,-1,c') law at i+1. Each law is blocked *only* by
  the other's existence; delete either and the survivor fires. Complete census:
  these are the ONLY taut 2-law codes — 9m per ring (m>=3; verified 36 = 9*4 at
  m=4; the degenerate m=2 ring has 36). Checks-and-balances is not one design
  among many: at minimal size it is the *unique* stable architecture.
- **Smallest balanced constitution: does not exist** (Theorem 1).

## 2. Attractor natural history (random codes, 400 seeds per cell)

m in {4,6,8,12,16,24} x lambda in {0.05,...,4} laws/cell; budget 50k steps.
Full table: `attractors.json` / sweep log. Headlines:

- **Zero holdouts, zero balanced-fixed, everywhere.** Transients are tiny: mean
  < 3 steps, **max <= m** across all 16,800 runs (attained at m-1..m) — set by the *Empire of One Law*:
  a lone colonizer (0,1,1) enacts itself around the ring and gridlocks it solid in
  m-1 steps (verified specimen). Randomly drafted codes equilibrate essentially
  instantly; there is no glassy relaxation regime on rings.
- **Attractor types:** extinct / porous-frozen / solid-gridlock / cycles with
  period 2 (rarely 4). Random seeds NEVER produced p > 4.
- **No critical density.** Crossovers are smooth in every observable. Extinction
  dominates ultra-sparse small rings (81% at m=4, lam=0.05), porous frozen relics
  dominate the middle (73% at m=8, lam=0.5), solid gridlock takes over by
  lam=4 (83-98%, rising as m falls). Mean final occupancy tracks the seed occupancy 1 - e^-lambda
  plus mild colonizer densification — the dynamics barely moves the density.
- **Cycle fraction is extensive**, rising with m at fixed lambda (64% at m=24,
  lam=1): blinkers (sunset clauses, p=2) are local decorations that a big ring
  almost surely hosts somewhere. The "interesting intermediate zone" of the
  pre-registration is real but modest: lam ~ 0.5-2 maximizes churn, yet its
  cycles are parity blinkers, not long constitutional epochs.

## 3. The longest constitutional cycle

Search: (A) exhaustive — all 1- and 2-law seeds, all 3-law seeds up to rotation,
m=2..8 (~1.73M seeds, 0 holdouts); (B) 550k+ randomized 4-6-law seeds; (C) **exact
functional graphs of closed subuniverses** (any kind-subset is dynamically closed
since laws toggle only their own kind): all 12 single-kind universes m<=10 (m<=22
for the winner), all 66 live-pair universes m<=8 — complete state spaces, so
these maxima are exact, not sampled.

**Champion under the task constraint (m<=8, seed <=6 laws): period 6, m=6, 5 laws**
`[(0,(0,-1,1)), (0,(0,1,-1)), (2,(0,1,-1)), (4,(0,-1,1)), (5,(0,-1,1))]` — the two
sunset clauses (enact-then-block, left- and right-handed) sharing a chamber:

    t=0  2.1.11   t=1  211.11   t=2  2.1.12
    t=3  211.1.   t=4  211.11   t=5  221.1.   t=6 = t=0   (occupancy sways +2/-2)

Exhaustively certified through 3-law seeds; the best m=8 cycle in any pair
universe (p=8, kinds (-1,1,-1)+(0,-1,1)) needs >= 9 laws even in its own basin.

**Unrestricted discovery — THE SUNSET PARLIAMENT.** The single-kind universe of
the sunset clause (0,-1,1) ("while my left seat is vacant, enact my kind to the
right") holds the long cycles. Exact max period vs m (complete 2^m-state graphs):

| m | 2 3 4 5 6 7 8 9 | 10 | 11..16 | 17 | 18 | 19 | 20 | 21 | 22 |
|---|----------------|----|--------|----|----|----|----|----|----|
| max p | 1 2 2 4 4 4 4 8 | **15** | 8,8,8,8,8,16 | 16 | **63** | 16 | 30 | 16 | **341** |

Resonant rings m = 2 (mod 4) unlock huge odd periods: 15 = 2^4-1 at m=10,
63 = 2^6-1 at m=18, **341 = (2^10-1)/3 at m=22** — while neighbors stay at
powers of two. At m=10 the mechanism is visible: a two-hole occupancy pattern
**rotates 2 cells every 3 steps** (speed 2/3, the same rational as the chain's
conversion waves), closing after 5 laps x 3 = 15 steps; a **6-law seed**
`(0,-1,1)@{0,2,4,6,8,9}` lands on it directly (m=10 spacetime in cycles.log /
hunt2 output). This is a legislative wave circling a closed statute book forever.

**Why beating period ~2m needs occupancy oscillation (theorem).** On constant
occupancy each kind evolves linearly, x -> (I+D)x, and the activity set A can
never be the whole ring, so D is nilpotent and I+D unipotent: constant-occupancy
cycles have period a power of 2, <= 2^ceil(log2 m). All observed periods > 2
indeed oscillate occupancy; the parliament's 341 is a monodromy of unipotent
products around an occupancy loop — resonance number theory left open.

## 4. Reversibility and Gardens of Eden — exact predecessor algebra

Fix the predecessor's occupancy O (2^m guesses). Per kind, stepping is linear
over F2: x XOR D x with D a masked rotate; A_k(O) is never the full ring, so for
c=±1 kinds I+D is **unipotent — unique candidate predecessor per kind**; c=0
kinds are the only lossy ones: solvable iff y vanishes on A_k(O), with free
"ghost" bits there (self-repealing laws that erase themselves without trace).
In-degree = sum over O of prod_i (2^{f_i} - [v_i = 0]) over occupied i (empty i
must have v_i = 0). So: **the step map is injective on each occupancy class
modulo ghosts; all irreversibility = c=0 self-repeals + occupancy collisions.**
Validated two ways: forward consistency (every step(x) predecessor-checked), and
**exact match of in-degrees against fully brute-forced subuniverse functional
graphs for every state** (m=3,4; several kind-sets).

- **Uniform measure: reachability is total.** Fixed points are their own
  predecessors, so GoE fraction <= non-fixed fraction = 1 - F(m)/2^27m
  ~= m * 2^-27 (exact from Task 1). Gardens of Eden are a sparse-sector affair.
- **No lone statute is un-enactable**: all 27 single-law states have predecessors
  (in-degree 57..197 at m=5 — ghost-rich histories). GoE begins at 2 laws:
  exact census 19.3% (m=3), 7.8% (m=4), 5.8% (m=5), 4.6% (m=6) of 2-law codes;
  typical specimen: a dead letter plus a distant self-starter, e.g.
  `(-1,-1,-1)@0 + (0,-1,-1)@2` on m=4 — no history writes that book.
- **Sampled GoE fraction peaks at mid-density**: at m=8 it climbs 1.6% (lam=0.1)
  -> 33% (lam=1) -> 34% (lam=2) then collapses to 5% (lam=4, near-gridlock states
  are self-fixed). Moderately dense living codes are mostly *unwritable*: the
  reachable mid-density set is thin — history concentrates fast.
- **The Vanishing Codes**: predecessors of the empty book = codes that die in one
  step = sum over flank-free occupancy patterns of 3^|O| (every cell holds a
  nonempty subset of its two self-repealer kinds); exact sequence for m=2..10:
  7, 37, 67, 241, 775, 2101, 6595, 19873, 58567 — and the empty book is the
  in-degree champion of every sample (the great sink of legal history).

## 5. Minimal viable constitution (Task 5 answer)

- Smallest stable code: **1 law** (21 of 27 kinds; e.g. the unsatisfiable statute
  (1,1,1)) — a dead letter on an empty ring.
- Smallest stable code that is *about something* — every law load-bearing:
  **the 2-law Mutual-Veto Constitution**, the unique taut architecture (9m
  copies per ring).
- Smallest balanced (self-cancelling-but-active): **nonexistent** — Theorem 1.

## Scorecard vs. expedition brief
- Fixed-point local characterization: **proved exactly** (blocked-only; parity
  slot-condition trivializes via Single-Author). Balanced species: **refuted with
  mechanism** — the charismatic possibility is dead, and its death is the result.
- Counts: **exact for all m** (transfer matrix + GF), verified by 8.78M-code brute
  force; species: gridlock only (solid vs porous texture).
- Phase diagram: **no critical lambda; smooth crossover; transients <= m**.
- Champion cycle: **p=6 (m<=8, <=6 laws, certified)**; unrestricted **Sunset
  Parliament p=341 at m=22**, exact; resonance class m = 2 mod 4 flagged open.
- GoE: exact algebra + measured fractions (0 at uniform; 33% peak mid-density;
  0 at 1 law; 4.6-19.3% at 2 laws).

*Total compute: ~7 minutes across all scripts (logs record timings).*
