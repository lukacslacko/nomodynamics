# Nomodynamics: the mathematics of self-amending law
### Expedition N — founding document
*2026-08-26. Definition and predictions written BEFORE first simulation (program
rule: pre-register, then look). Derivation, novelty sweep, formalization,
predictions; findings go in FINDINGS.md, never edited into this file.*

## 1. The vacancy, derived (not guessed)

Three independent generators of the Treeline program converge:

1. **The deletion grid.** Game theory (1928) formalized 2-player fixed-rule games.
   Conway's celebrated deletion removed the *players*: 0-player fixed-rule games =
   cellular automata = Life (1970). The orthogonal deletion — remove the *fixity
   of the rules* — was never taken. The cell "0-player self-amending" is empty.
2. **The WLOG audit.** Computability's founding reduction — "wlog the program is
   fixed" (justified by universality: self-modification is simulable) — is valid
   for what-can-be-computed and, exactly like "wlog loopless" and "wlog
   connected" in our matroid/geodesic expeditions, invalid for behavioral
   natural history: the small self-amending systems were never *looked at*,
   because the reduction said we didn't have to.
3. **The practiced-verb scan.** Turing objectified "compute," practiced for
   millennia. "Amend" — rules acting on rules — is humanity's oldest formal
   practice (Hammurabi, constitutions, parliaments), with only fragments of
   formalization: von Neumann's universal constructor (1948) merged rule and
   substrate but buried it in a 29-state construction; Suber's Nomic (1982)
   stayed philosophy; self-modifying Petri nets (Valk 1978) and adaptive
   automata stayed CS-fringe; Fontana's algorithmic chemistry (1990s) put
   λ-terms in a soup, ALife-style. **No minimal charismatic object, no census,
   no elementary mathematics.** (Novelty sweep 2026-08-26: searches across
   self-modifying CA / Nomic formalization / self-referential Boolean networks
   confirm fragments-only; logs in the session record.)

The theory's own map says why the region was passed over — it sits on the lower
slopes of the reflection summit (encoders; instant-undecidability fear) AND in
the recreational prestige shadow (Nomic = parlor game) AND behind a silent-premise
closure ("games have fixed rules" / "programs are fixed"). Triple shadow, tiny σ:
the full discovery signature.

## 2. The object (the Turing-step)

**Nomic chain (window w = 1; the canonical system).** A *law* is a triple
(a, b, c) ∈ {−1, 0, +1}³ placed at a position i ∈ ℤ. A *code* is a finite set of
placed laws. Semantics, in one sentence:

> **While some law stands at offset a from it and no law stands at offset b, a
> law flips the presence of its own kind at offset c; all standing laws act at
> once, flips resolving by parity.**

Formally: state S ⊆ ℤ × T, T = {−1,0,+1}³ (27 types). Law (i,(a,b,c)) ∈ S is
*active* iff ∃t: (i+a, t) ∈ S and ∄t: (i+b, t) ∈ S. Every active (i,(a,b,c))
contributes one toggle to the pair (i+c, (a,b,c)); the next state is S XOR (all
toggled pairs, multiplicity mod 2). Time is synchronous. No other rules exist:
**the law is the only substance** — guards read occupancy, effects enact or
repeal the actor's own kind. Notes: (i) occupancy-guards (not type-guards) keep
the semantics elementary; (ii) toggle-own-kind unifies enactment and repeal and
is parity-clean; (iii) window 1 makes the system parameter-free; window w gives
the family. **Nomic ring**: same on ℤ/m (a circular statute book) — finite for
complete small-m analysis.

Variant axes (for the robustness/cryptomorphism study, not the main line):
guard polarity (require b-offset *occupied*), enact-only vs toggle, type-guards,
asymmetric windows. The Church–Turing-style claim to test: the qualitative
fauna is robust across variants.

## 3. Pre-registered predictions (before first run)

- **N1.** Degenerate majority: most single-law seeds die (self-repeal or guard
  starvation) or freeze.
- **N2.** Nonzero structured-growth fraction: some seeds of size ≤ 2 produce
  unbounded, patterned codes ("legal sprawl").
- **N3.** A glider exists among seeds of size ≤ 2 ("a law-packet that marches
  through the statute book, enacting ahead and repealing behind") — the
  self-copy semantics biases toward translation; Life-precedent prior.
- **N4.** Speed quantization: glider/growth-front speeds cluster on small
  rationals (statistical layer).
- **N5.** Fixed points ("constitutions") admit a local blocking characterization
  (crystal stratum), and nontrivial ones exist.
- **N6.** Cryptids: at least one seed of size ≤ 3 resists die/freeze/periodic/
  glider certificates at 10⁶-step budgets (the summit is close).
- **Risk, stated:** if the window-1 chain and its 3-4 nearest variants are boring
  across ALL small seeds (everything dies/freezes/blinks), the formalization
  fails; report the negative, debit the generators.

## 4. Method

Seed census with the turmite-census machinery transplanted: enumerate seeds (all
single laws: 27; all two-law seeds within a small window, up to translation);
simulate with certificates — extinction (S = ∅), fixed point, exact cycle
(configuration recurrence), glider (configuration recurrence modulo nonzero
translation), structured growth (front-speed + periodic bulk certificates);
everything else at budget → holdout. Then: the constitution algebra (fixed-point
characterization on rings), variant robustness, and — if specimens warrant —
naming.
