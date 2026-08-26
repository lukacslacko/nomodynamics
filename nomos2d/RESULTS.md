# NOMOS-2D — First contact with 2D nomodynamics
### Expedition N-B, Treeline program. 2026-08-26.

**System.** State = finite set of placed laws (p, T), p ∈ ℤ², T = (a,b,c) ∈ N³,
N = von Neumann offsets {O,E,W,N,S} (125 law-types; type names are 3-letter
words, e.g. `OEN` = a=self, b=East, c=North). Law (p,(a,b,c)) is *active* iff
p+a is occupied (by any law) and p+b is empty; every active law toggles the
presence of **its own kind** at p+c. Synchronous. Requested semantics: PARITY
(xor) and OR-toggle.

**Engine** (`engine2d.py`): dict-of-int-encoded-positions → 125-bit masks;
independent dense numpy engine (cross-checked exactly); certificate machinery:
extinction, fixed point, exact cycle, **glider** (recurrence mod translation),
**rotor** (recurrence mod 90°/180° rotation *of positions and types*),
**glide-ship** (recurrence mod reflection, with net drift), growth, sprawl.
D4-equivariance of the step is verified by self-test, so the rotation/
reflection certificates are sound. All specimen certificates re-verified
exactly (`verify_recurrence`).

---

## 0. Headline

2D delivers post-front fauna — but not the expected kind. **No gliders, no
plane-filling growth, no quarter-turn pinwheels** (all three are blocked by
structure theorems below, two outright, one softly). What 2D *does* deliver:

1. **THE JUBILEE CODE** — a bounded-size (~26 laws), never-repeating machine
   whose frontier advances in carry avalanches locked to t = 2^k, sweeping
   the entire ~1.5√t-cell extent (size spikes to ~770) and collapsing back to
   a handful of laws. 791 of 60,000 random small seeds independently converge
   to this one attractor. It is the pre-registered "bounded but
   never-repeating" cryptid, in the strongest sense the theory permits.
   (Universality: after 30k steps all 791 sit at frontier 284–290 — the
   same √t law; three deep probes from unrelated seed families — 3-law,
   2-law, 4-law — show bit-identical burst schedules.)
2. A family of **half-turn rotors** (state maps to its own 180°-rotation-
   plus-shift every step) — genuine rotation-certificate fauna: 1 found wild
   in 36k random seeds, then 238 more at 0.8% in the targeted {k,k,R²k}
   stratum that Theorem 4 predicts.
3. A 2D-specific single-law species: the **perpendicular colonizer** (growth
   direction orthogonal to its guard — impossible in 1D), whose column is
   exactly Pascal's triangle mod 2 (size(t) = 2^popcount(t)).
4. An interaction physics with 2D character: **right-of-way** at ray
   crossings (tie → mutual transparency; earlier occupant → permanent weld),
   phase-dependent gate delays, erosion fronts with immortal relics,
   entrenchment-cap constitutions.

Also: the **single-author lemma** (below) collapses the parity/OR axis —
the two requested semantics are *provably the same map*, in any dimension.
(Independently confirmed mid-expedition by the rings expedition; per the
coordinator's correction the freed budget went into deeper parity coverage
and a cross-amendment teaser, §7, where the two semantics finally split.)

---

## 1. Structure theorems (proved, then engine-verified)

**Lemma 1 (single-author).** For any target pair (q, T), the only law that
can ever toggle it is the law (q − c_T, T): a kind has one c-offset and at
most one law of a kind stands per cell. Every toggle multiplicity is 0 or 1,
so PARITY ≡ OR identically (any multiplicity-resolution rule coincides).
*Verified:* 400 random seeds × 120 steps, state-by-state equality of the two
engine implementations; census of all 125 single laws identical under both.
Consequence: **nonlinearity in nomodynamics lives only in the guards**
(occupancy AND / NOT-occupancy), never in toggle resolution.

**Theorem 2 (type conservation).** Laws toggle only their own kind, so
types(S_t) ⊆ types(S_0). An n-law seed lives forever in an ≤ n-type world.

**Theorem 3 (ray confinement).** By induction, every law of kind T ever
enacted lies in seed_T + ℕ·c_T. Hence:
- total support ⊆ union of |seed| rays: **all growth is 1-dimensional;
  growth exponent α ≤ 1.** Quadrant/cone-filling is impossible.
- an exact glider with displacement d must have every persistent kind's c
  parallel to d, c ≠ O ⇒ **gliders can only travel axis-aligned**, and are
  confined to the fixed horizontal (or vertical) lines through their seed —
  a 2D glider is a stack of coupled 1D lanes (guards may reach across lanes).
- a strictly bounded-support evolution has finitely many reachable states ⇒
  is eventually periodic. **"Bounded and aperiodic" is only possible as
  bounded *size* with unbounded reach** — exactly what the Jubilee code does.

**Theorem 4 (symmetry closure).** A recurrence S_{t+p} = g(S_t)+v (g a
rotation/reflection acting on positions *and* types) requires the type set
to be g-closed. Quarter-turn rotors need ≥ 4 types (a C4 orbit); half-turn
rotors and glide-ships are possible with 2. Any 90°-rotor or 180°-rotor is
an oscillator overall (Σ_k g^k v = 0); a glide-ship drifts v + g(v) per 2p —
translation-free rotation is impossible on the square lattice.

**Observed regularity (conjecture).** Every exact cycle found — across
~140,000 own-kind seeds and 4,000 cross-amendment universes — has period a
power of 2 (1, 2, 4, 8; cross-amendment adds 16). No odd or mixed period was
ever seen. 2-adic clockwork appears to be forced by the toggle algebra.

---

## 2. Single-law census (all 125 types; both semantics — identical, Lemma 1)

| verdict | count | who |
|---|---|---|
| fixed | 105 | all 100 types with a ≠ O (guard unmet when alone), plus the 5 a=O, b=O types |
| extinct (t=1) | 4 | `OEO OWO ONO OSO` (a=O, b≠O, c=O: instant self-repeal) |
| cycle p=2 | 4 | `OEW OWE ONS OSN` (c = −b: enact behind, then blocked; blinker) |
| growth | 12 | see below |

A single law can only be nontrivial with a = O (nothing else is occupied).
Of the 125 types, 45 are **dead letters** — provably inert in *any* state
(a = b, or b = O: guard self-contradictory). They matter later as terrain.

**Growth species (α from |support(t)| fit over t ∈ [30,300], dense runs):**

| types | mechanism | α | shape at t=300 |
|---|---|---|---|
| `OEE OWW ONN OSS` (c = b) | colonizer ray, 1 cell/step | 0.99 | 301×1 line, fill 1.0 |
| `OEN OES OWN OWS ONE ONW OSE OSW` (c ⊥ b) | **perpendicular colonizer** | 0.44 (fit; exact law: size = 2^popcount(t), mean-size exponent log₂3−1 ≈ 0.585) | 1×301 line, fill 0.053, size dips to 2 at t = 2^k |

Two distinct shape classes mod D4 (`census_gallery.txt`; spacetime art in
`gallery.txt`). The perpendicular colonizer has **no 1D analogue** (in 1D, c
cannot be orthogonal to b): first pre-registered 2D-specific species. Its
column is literally Pascal's triangle mod 2, an unbounded aperiodic-size
front from ONE law. No single law fills more than a line: Theorem 3 already
bites. No α = 2, no dendrites — census tallies:
`{fixed: 105, extinct: 4, cycle-2: 4, growth: 12}`, identical under parity
and OR (verdict-by-verdict).

## 3. Small-seed survey (2–3 laws in a 3×3 patch) and escalation cascade

First pass (256 steps, growth cap 1200, full glider/rotor/glide hashing):
**main sample n = 36,000** (reproducible RNG, seed 20260826):

| verdict | n | % |
|---|---|---|
| fixed | 24,297 | 67.5 |
| unresolved-flat (→ escalation) | 4,530 | 12.6 |
| cycle p=2 | 4,062 | 11.3 |
| unresolved-growing (→ dense α-check) | 2,821 | 7.8 |
| cycle p=4 | 260 | 0.7 |
| extinct | 30 | 0.08 |
| glider / rotor / glide / cycle>8 | 0 | — |

(An earlier equal-size randomized run found 1 **rotor** — §5.3 — preserved
and verified; the 3-law rotor pattern {k, k, R²k} is too rare for one 36k
sample to hit reliably. A dedicated 30,000-seed {k,k,R²k} hunt
(`hunt_rot3.py`) found **238 rotors** (0.8%) — all half-turn flip-flops
(p=1, dr=180°, 3 laws) across many type families: OEW/OWE, NSN/SNS,
EWE/WEW, ONS/OSN, ESN/WNS, NWE/SEW, … The pinwheel ordinance is a genuine
family, abundant exactly in the stratum Theorem 4 predicts.)

**Targeted symmetry-closed hunts** (Theorem 4 tells us where to look):
- rot2 mode {k, R²k}, n = 8,000: no rotors (2-law geometry insufficient).
- mir2 mode {k, Mk}, n = 40,000: **no glide-ships**. cycles ≤ 4.
- rot4 mode {k, Rk, R²k, R³k} in 5×5, n = 40,000: cycle-8 ×10 (the longest
  own-kind periods found; all C4-orbit quads), no quarter-turn rotors.

**Growth α-check** (400 dense 250-step runs of survey growth seeds): α ∈
[0.73, 0.99], median 0.98 — **every growth seed is fronts/filaments**;
the widest supports (252×252 bounding boxes at fill 0.008) are crosses of
rays, as Theorem 3 demands. Verdict-level agreement of parity vs OR
engines re-verified on subsamples throughout.

**Escalation cascade** on the 6,298 first-wave unresolved-flat seeds
(a statistically identical earlier 36k main batch + the original 8k×3
targeted wave; all escalated specs stored verbatim in the esc*.json files):
- **Stage B** (6,000 steps, sprawl detection at reach > 500): 5,506 sprawl
  (unbounded fractal fronts of the Pascal family), 791 still unresolved,
  1 growth, **0 new cycles**.
- **Stage C** (30,000 steps): **791 / 791 still unresolved** — zero cycles,
  zero gliders. Reach after 30k steps sits in the band 92–98·3 ≈ **284–290
  for every single survivor** (median 289): all of them tick the same √t
  clock. Sizes 14–304 (the max is a seed caught mid-avalanche at exit).
- **Stage D** (250,000 steps, light-hash, 120-seed sample of the 791 —
  full-population D was cut for machine-load reasons): **120 / 120 still
  unresolved** — no recurrence, no cycle, no glider, through a quarter
  million steps; and at t = 250,000 every one of the 120 sits at reach
  765–769 (median 767) with quiescent size 13–25 — exactly the predicted
  post-2^18-epoch Jubilee frontier of 768. Together with the three
  300k-step fully-hashed probes, the holdout class is certified aperiodic
  far beyond the pre-registered 20,000-step bar.

The 791 stage-B survivors: size 15–113 (median 16), reach ≈ 92–98 after
6,000 steps, 555 distinct type-sets — dominated by C4 orbits of `WNE`
(= chain types: guard one horizontal neighbor, block one vertical, copy
horizontal) and their 2-subsets. Deep 300,000-step probes of three
representatives from *different* seed families (3-law `ESN/SNS/WNE`, 4-law
C4 quad, 2-law `ENW/ESW`) show **bit-identical avalanche schedules** —
one universal attractor: the Jubilee code (§5.1).

## 4. Interaction teaser (`interact.py`, full ASCII in `interact_report.txt`)

- **I1 head-on rays** (`OEE` vs `OWW`): fronts weld permanently at meeting
  (both see the other as b-block); even and odd gaps both weld (even gap →
  two kinds stacked on the shared cell). No annihilation, no reflection.
- **I2 crossing rays**: a ray crossing another ray's *solid trail*: if the
  trail got there first → permanent weld; if both fronts reach the crossing
  cell **simultaneously → mutual transparency** (guards read occupancy at
  step start; both enter the same cell and pass through). "Right-of-way
  doctrine": priority to the earlier occupant, ties interpenetrate.
- **I2c blinking gate**: a ray crossing a *Pascal-blinking* trail is delayed
  0–3 steps depending on arrival phase — **phase-dependent refraction**.
- **I4 self-eroding block** (`EWO`, 12×7): erodes 1 column/step from the
  west. A deleted interior law (point defect) spreads east as a vacancy
  front and leaves **immortal relics** (laws whose east went empty first
  are permanently deactivated): loopholes eat the code and leave dead
  letters.
- **I5 entrenchment**: a row of live `OES` laws is a **fixed point** when
  capped by one inert law (occupancy is the only guard currency — a dead
  letter entrenches the code). Repeal the cap and a Pascal amendment-tail
  cascades from the free end while the row stands.

2D-specific character: right-of-way geometry, corner-anchored pumps
(the Jubilee anchor feeds its chain from a perpendicular row — impossible
in 1D), terrain made of dead-letter laws.

## 5. The gallery (five specimens; seeds, certificates, ASCII in `gallery.txt`)

1. **THE JUBILEE CODE** — seed `(-1,0)ESN (-1,1)SNS (0,1)WNE` (3 laws).
   A static anchor+pump drives the nonlinear chain s_{x+1} ⊕= s_x ∧ s_{x−1}
   along one row. Quiescent size ~26; at every epoch t = 2^k a carry
   avalanche sweeps the whole extent (size spikes to 770 at t = 2^17,
   collapses to 4 two steps later), frontier = 3·2^m after epochs
   (reach ~1.5–2.1·√t). **Certificates**: no recurrence in 300,000 steps
   (canonical hashing of every state of size ≤ 300, i.e. all but the brief
   avalanche peaks); exact 1D reduction (9 lines)
   reproduces the burst schedule bit-for-bit through 9 doublings —
   frontier at t = 2^k: 48, 95, 96, 191, 192, 383, 384, 767, 768.
   √t reach ⟹ provably neither periodic nor glider (linear drift excluded).
   The universal attractor of the entire holdout class (791 seeds).
   The 1D reduction (pump s₀ ≡ 1; s_{x+1}(t+1) = s_{x+1}(t) ⊕ (s_x ∧ s_{x−1});
   frontier and popcount at epochs):

   | t = 2^k | 1024 | 2048 | 4096 | 8192 | 16384 | 32768 | 65536 | 131072 | 262144 |
   |---|---|---|---|---|---|---|---|---|---|
   | frontier | 48 | 95 | 96 | 191 | 192 | 383 | 384 | 767 | 768 |
   | #laws | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 | 2 |

   At every epoch the whole book collapses to pump + frontier — a total
   jubilee — then rebuilds. Frontier(2^{2m}) = 3·2^{m−1};
   frontier(2^{2m+1}) = 3·2^m − 1.
2. **THE APPELLATE COLUMN** — seed `(0,0)OEN` (ONE law). Perpendicular
   colonizer; column = Pascal mod 2; size(t) = 2^popcount(t) (exact);
   collapses to 2 laws at every t = 2^k and regrows; never dies, never
   repeats, α_mean = log₂3 − 1. The simplest unbounded aperiodic object in
   the fauna, and 2D-specific.
3. **THE PINWHEEL ORDINANCE** — seed `(0,-1)NEW (1,-1)NEW (1,0)SWE`.
   Verified S_1 = rot180(S_0) + (2,−1): a 3-law flip-flop whose two phases
   are 180° rotations of each other (types NEW ↔ SWE swap). Emblem of a
   238-strong family (`hunt_rot3.py`); all 238 certificates re-verified
   exactly (S_{t0+p} == rot180(S_{t0}) + v, batch check 238/238).
   Quarter-turn rotors don't exist below 4 types (Thm 4) and none were
   found at 4 (48k C4-closed seeds).
4. **THE RIGHT-OF-WAY DOCTRINE** — `OEE` ray + `ONN` column: seeded
   equidistant → both fronts occupy the crossing cell in the same step and
   pass through each other; column seeded closer → the ray welds forever at
   x = 5. Deterministic traffic law for 2D fronts.
5. **THE TWO-CHAMBER AMENDMENT** (cross-amendment universe, §7) — laws
   `A=OSS→A` and `B=OES→A` stacked at one cell: under PARITY the two
   authors' toggles of the same target cancel — the code is *fixed forever*;
   under OR the double enactment passes and the pair ignites into sustained
   linear growth. The first seed in the program where the resolution
   semantics decides life vs deadlock.

## 6. Verdicts on the pre-registered expectations

- **(i) colonizer analogues fill quadrants/cones — REFUTED.** Colonizer
  analogues exist (rays, crosses, fractal fronts) but Theorem 3 confines
  all own-kind growth to unions of 1D rays: α ≤ 1, measured α ≤ 0.99 over
  400 growth seeds. The plane never fills.
- **(ii) 2D-specific fauna with no 1D analogue — CONFIRMED.** The
  perpendicular colonizer (c ⊥ b has no 1D counterpart), the half-turn
  rotor (rotation certificate), right-of-way crossing physics, dead-letter
  terrain/entrenchment, and the Jubilee anchor geometry (pump feeding a
  chain from a perpendicular row). No pinwheels-proper, spirals, or free
  corner-signals: the guard nonlinearity is too ray-locked for them.
- **(iii) bounded but never-repeating evolution — CONFIRMED** in the
  strongest sense available (bounded support ⇒ periodic is a theorem):
  the Jubilee code keeps bounded *card* (≾ 30 quiescent) with unbounded
  reach and no recurrence through 300k steps, with a self-similar 2-adic
  avalanche clock. 791/60,000 random seeds land on it.

## 7. Cross-amendment teaser (coordinator's correction, 2026-08-26)

Extension: law types (a,b,c,e) where e names the target kind toggled at
p+c (two-kind universes: e ∈ {self, other}; `xamend.py`). Multi-author
interference now exists, and:

- **The semantics split**: 20 / 4,000 random universes+seeds give different
  verdicts under parity vs OR (e.g. fixed-by-cancellation vs cycle; one
  seed is fixed under parity and grows +1 law/step, verified 3,000 steps,
  under OR — specimen 5).
- **Longer clocks**: period 16 appears (own-kind max was 8). Still 2^k.
- **Ray confinement breaks directionally**: relay universes (A=`ONE`→B,
  B=`OEN`→A) walk **diagonal staircases** — a direction no own-kind law can
  ever take (c-offsets are axis unit vectors, so Theorem 3 locks all motion
  to the axes). Support nevertheless stays 1-dimensional: α ≤ 1 in all
  4,000 random universes and in the designed relays; the two-kind monoid
  ℕ·c_A + ℕ·c_B spans the quadrant in principle, but parity dynamics keeps
  only a width-2 diagonal frontier. Solid 2D growth remains unobserved.

The own-kind system's degeneracies are thus *sharp* where it matters:
one bit of target-kind freedom dissolves Lemma 1 (semantics split) and the
axis-lock of Theorem 3 (diagonals appear), while 1-dimensionality of
growth survives even cross-amendment at this seed size.

## 8. Files

- `engine2d.py` — engine, certificates, D4 machinery, self-tests
- `census.py` → `census_out.json`, `census_gallery.txt` — task 2
- `survey.py` → `survey_{main,rot2,mir2,rot4}.json` — task 3 first pass
- `escalate.py` → `escB/escC/escD.json` — stages B/C/D
- `growth_check.py` → `growth_check_survey_main.json` — α distribution
- `probe_holdout.py` — deep single-seed probes (Jubilee evidence)
- `hunt_rot3.py` — targeted {k,k,R²k} rotor-family hunt (238 finds)
- `interact.py` → `interact_report.txt` — task 4
- `gallery.py` → `gallery.txt` — task 5
- `xamend.py` — cross-amendment teaser (§7)

Repro: `python3 engine2d.py` (self-tests); `python3 census.py`;
`python3 survey.py --mode main --n 36000`; `python3 escalate.py --stage B
--infiles survey_main.json ... --out escB.json`; etc. Python 3.11 + numpy.
