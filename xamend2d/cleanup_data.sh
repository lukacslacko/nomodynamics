#!/bin/sh
# Trim the census dumps to publishable size: keep every rare-event record in
# full, subsample the two bulk categories (UNRES, ESCAPE), gzip everything.
set -e
cd /Users/lukacs/claude/math/program/phase6/xamend2d/data
merge() {   # merge $1.N shards into one file, then split by category
  pre=$1; out=$2
  cat ${pre}.0 ${pre}.1 ${pre}.2 ${pre}.3 ${pre}.4 ${pre}.5 \
      ${pre}.6 ${pre}.7 ${pre}.8 ${pre}.9 ${pre}.10 ${pre}.11 2>/dev/null > /tmp/_m.txt || true
  grep -E '^(GLIDER|NONPOW2|BALANCED)' /tmp/_m.txt > ${out}_events.txt || true
  awk 'NR%37==1' /tmp/_m.txt | grep -E '^(UNRES|ESCAPE)' > ${out}_bulk_sample.txt || true
  rm -f ${pre}.0 ${pre}.1 ${pre}.2 ${pre}.3 ${pre}.4 ${pre}.5 \
        ${pre}.6 ${pre}.7 ${pre}.8 ${pre}.9 ${pre}.10 ${pre}.11 /tmp/_m.txt
  gzip -f ${out}_events.txt ${out}_bulk_sample.txt
}
merge mp2 moore_parity
merge mo2 moore_or
merge k3p kind3_parity
grep '^ALPHA ' moore_alpha_raw.txt > alpha_measurements.txt
gzip -f alpha_measurements.txt
rm -f moore_alpha_raw.txt moore_parity_finds.txt moore_or_finds.txt \
      moore_parity_alpha_finds.txt unres_batch.txt unres_meta.json \
      escB.txt escB_survivors.txt escD_in.txt
gzip -f escC.txt escC_survivors.txt escD.txt escD_survivors.txt 2>/dev/null || true
gzip -f alpha_refined.json alpha_stage2.json 2>/dev/null || true
ls -la
