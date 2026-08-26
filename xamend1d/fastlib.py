#!/usr/bin/env python3
"""fastlib.py — ctypes wrapper around fastcensus.so (the bit-parallel engine).

Word layout: bit i of word[k] == "a law of kind k stands at cell (i - PAD)".
Nothing here is trusted until validate_fast.py passes.
"""
from __future__ import annotations

import ctypes
import os
import subprocess

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "fastcensus.c")
SO = os.path.join(HERE, "fastcensus.so")

if (not os.path.exists(SO)) or os.path.getmtime(SO) < os.path.getmtime(SRC):
    subprocess.check_call(["clang", "-O3", "-march=native", "-shared", "-fPIC",
                           "-o", SO, SRC])

_L = ctypes.CDLL(SO)

_L.c_step.argtypes = [np.ctypeslib.ndpointer(np.int32), ctypes.c_int32,
                      ctypes.c_int32, np.ctypeslib.ndpointer(np.uint64),
                      np.ctypeslib.ndpointer(np.uint64)]
_L.c_wide_step.argtypes = _L.c_step.argtypes
_L.c_classify.argtypes = [np.ctypeslib.ndpointer(np.int32), ctypes.c_int32,
                          ctypes.c_int32, np.ctypeslib.ndpointer(np.uint64),
                          ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
                          np.ctypeslib.ndpointer(np.int32)]
_L.c_census.argtypes = [np.ctypeslib.ndpointer(np.int32), ctypes.c_int64,
                        ctypes.c_int32, ctypes.c_int32,
                        np.ctypeslib.ndpointer(np.uint64), ctypes.c_int64,
                        ctypes.c_int32, ctypes.c_int32, ctypes.c_int32,
                        np.ctypeslib.ndpointer(np.int64),
                        np.ctypeslib.ndpointer(np.int32), ctypes.c_int32,
                        ctypes.c_int32, ctypes.c_int32]
_L.c_census.restype = ctypes.c_int32
_L.c_frontscan.argtypes = [np.ctypeslib.ndpointer(np.int32), ctypes.c_int64,
                           ctypes.c_int32, ctypes.c_int32,
                           np.ctypeslib.ndpointer(np.uint64), ctypes.c_int64,
                           ctypes.c_int32, ctypes.c_int32,
                           np.ctypeslib.ndpointer(np.int32), ctypes.c_int32]
_L.c_trace.argtypes = [np.ctypeslib.ndpointer(np.int32), ctypes.c_int32,
                       ctypes.c_int32, np.ctypeslib.ndpointer(np.uint64),
                       ctypes.c_int32, np.ctypeslib.ndpointer(np.uint64),
                       np.ctypeslib.ndpointer(np.int32)]
_L.c_trace.restype = ctypes.c_int32
_L.c_wb.restype = ctypes.c_int32
_L.c_pad.restype = ctypes.c_int32
_L.c_seedbase.restype = ctypes.c_int32

WB = _L.c_wb()
PAD = _L.c_pad()
SEEDBASE = _L.c_seedbase()
NTHREAD = max(1, (os.cpu_count() or 4))

MODES = ["parity", "or", "super", "super_or"]
# test-only translation semantics (validation of the GLIDER branch; not nomodynamics)
TEST_MODES = ["_shift_r", "_shift_l", "_swapshift"]
MODE_ID = {m: i for i, m in enumerate(MODES + TEST_MODES)}
CLASSES = ["EXTINCT", "FIXED", "BALANCED", "CYCLE", "GLIDER", "GROWING",
           "UNRESOLVED"]


# ------------------------------------------------------------------ encoding

def pack_const(rules, targets, n=None):
    """(rules, targets) -> the flat int32 block the C side expects."""
    n = n or len(rules)
    out = np.zeros(4 * n, dtype=np.int32)
    for k, (a, b, c) in enumerate(rules):
        out[k] = a
        out[n + k] = b
        out[2 * n + k] = c
    for k, t in enumerate(targets):
        tt = t if isinstance(t, (tuple, list)) else (t,)
        m = 0
        for x in tt:
            m |= 1 << x
        out[3 * n + k] = m
    return out


def pack_consts(consts):
    """consts: list of (rules, targets).  -> (nconst, n, flat int32 array)."""
    n = len(consts[0][0])
    arr = np.empty((len(consts), 4 * n), dtype=np.int32)
    for i, (r, t) in enumerate(consts):
        arr[i] = pack_const(r, t, n)
    return len(consts), n, arr.reshape(-1)


def pack_state(S, n, pad=None):
    """xnomos state dict {cell: mask} -> n uint64 words (cell c -> bit c+pad)."""
    pad = PAD if pad is None else pad
    w = np.zeros(n, dtype=np.uint64)
    for cell, m in S.items():
        for k in range(n):
            if m >> k & 1:
                w[k] |= np.uint64(1) << np.uint64(cell + pad)
    return w


def unpack_state(w, pad=None):
    pad = PAD if pad is None else pad
    S = {}
    for k, x in enumerate(w):
        x = int(x)
        while x:
            b = (x & -x).bit_length() - 1
            x &= x - 1
            S[b - pad] = S.get(b - pad, 0) | (1 << k)
    return S


# ------------------------------------------------------------------- the API

def step(cflat, n, mode, words):
    out = np.zeros(n, dtype=np.uint64)
    _L.c_step(np.ascontiguousarray(cflat, dtype=np.int32), n, MODE_ID[mode],
              np.ascontiguousarray(words, dtype=np.uint64), out)
    return out


def wide_step(cflat, n, mode, words):
    out = np.zeros(n * WB, dtype=np.uint64)
    _L.c_wide_step(np.ascontiguousarray(cflat, dtype=np.int32), n,
                   MODE_ID[mode], np.ascontiguousarray(words, dtype=np.uint64),
                   out)
    return out


def classify(cflat, n, mode, words, max_steps=200, max_card=200, max_span=40):
    out = np.zeros(5, dtype=np.int32)
    _L.c_classify(np.ascontiguousarray(cflat, dtype=np.int32), n, MODE_ID[mode],
                  np.ascontiguousarray(words, dtype=np.uint64),
                  max_steps, max_card, max_span, out)
    return dict(kind=CLASSES[out[0]], period=int(out[1]), disp=int(out[2]),
                t0=int(out[3]), card=int(out[4]))


def trace(cflat, n, mode, words, T):
    """Per-step (normalised words, anchor) — the exact data the glider
    detector keys on."""
    wout = np.zeros(T * n, dtype=np.uint64)
    aout = np.zeros(T, dtype=np.int32)
    m = _L.c_trace(np.ascontiguousarray(cflat, dtype=np.int32), n, MODE_ID[mode],
                   np.ascontiguousarray(words, dtype=np.uint64), T, wout, aout)
    return [(tuple(int(x) for x in wout[t * n:(t + 1) * n]), int(aout[t]))
            for t in range(m)]


def census(cflat, nconst, n, mode, seeds, max_steps=200, max_card=200,
           max_span=40, maxhits=4096, nthread=None, report=("GLIDER",)):
    """seeds: (nseed, n) uint64.  Returns (hist dict, hits array)."""
    seeds = np.ascontiguousarray(seeds, dtype=np.uint64)
    nseed = seeds.shape[0]
    hist = np.zeros(7, dtype=np.int64)
    hits = np.zeros(maxhits * 5, dtype=np.int32)
    nh = _L.c_census(np.ascontiguousarray(cflat, dtype=np.int32), nconst, n,
                     MODE_ID[mode], seeds.reshape(-1), nseed,
                     max_steps, max_card, max_span, hist, hits, maxhits,
                     nthread or NTHREAD,
                     sum(1 << CLASSES.index(r) for r in report))
    return ({CLASSES[i]: int(hist[i]) for i in range(7)},
            hits[:nh * 5].reshape(-1, 5))


FLAG_FRONT_R, FLAG_FRONT_L, FLAG_DEBRIS_P, FLAG_GROWS, FLAG_OSC, FLAG_GAPPY = (
    1, 2, 4, 8, 16, 32)
FCOLS = ["flags", "p", "d", "t0", "card_lo", "card_hi", "lo_lo", "lo_hi",
         "hi_lo", "hi_hi", "nblk"]


def frontscan(cflat, nconst, n, mode, seeds, T=140, Pmax=16, nthread=None):
    """Wide-frame near-miss scan.  Returns (nconst, nseed, 11) int32."""
    seeds = np.ascontiguousarray(seeds, dtype=np.uint64)
    nseed = seeds.shape[0]
    out = np.zeros(nconst * nseed * 11, dtype=np.int32)
    _L.c_frontscan(np.ascontiguousarray(cflat, dtype=np.int32), nconst, n,
                   MODE_ID[mode], seeds.reshape(-1), nseed, T, Pmax, out,
                   nthread or NTHREAD)
    return out.reshape(nconst, nseed, 11)


# ------------------------------------------------------------- seed factories

def seed_words(n, cellmasks, pad=None):
    """cellmasks: list of per-cell kind bitmasks, cell i == index i."""
    pad = PAD if pad is None else pad
    w = np.zeros(n, dtype=np.uint64)
    for i, m in enumerate(cellmasks):
        for k in range(n):
            if m >> k & 1:
                w[k] |= np.uint64(1) << np.uint64(i + pad)
    return w


def all_seeds(n, ncells, maxlaws, pad=None):
    """COMPLETE list of canonical seeds: masks over `ncells` cells, cell 0
    occupied (translation-canonical), total placed laws <= maxlaws."""
    pad = PAD if pad is None else pad
    full = (1 << n) - 1
    out = []
    cur = [0] * ncells

    def rec(i, used):
        if i == ncells:
            out.append(seed_words(n, cur, pad))
            return
        lo = 1 if i == 0 else 0
        for m in range(lo, full + 1):
            pc = bin(m).count("1")
            if used + pc > maxlaws:
                continue
            cur[i] = m
            rec(i + 1, used + pc)
        cur[i] = 0

    rec(0, 0)
    return np.array(out, dtype=np.uint64)


def sample_seeds(n, ncells, nlaws, count, rng, pad=None):
    """Uniform SAMPLE of canonical seeds with exactly nlaws laws in ncells."""
    pad = PAD if pad is None else pad
    slots = [(i, k) for i in range(ncells) for k in range(n)]
    seen = set()
    out = []
    while len(out) < count:
        idx = rng.choice(len(slots), size=nlaws, replace=False)
        cells = [slots[i] for i in idx]
        lo = min(c for c, _ in cells)
        key = tuple(sorted((c - lo, k) for c, k in cells))
        if key in seen:
            continue
        seen.add(key)
        w = np.zeros(n, dtype=np.uint64)
        for c, k in key:
            w[k] |= np.uint64(1) << np.uint64(c + pad)
        out.append(w)
    return np.array(out, dtype=np.uint64)
