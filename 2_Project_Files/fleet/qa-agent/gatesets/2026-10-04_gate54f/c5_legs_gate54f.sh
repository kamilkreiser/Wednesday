#!/bin/bash
# c5_legs_gate54f.sh — gate54f C5: the three pre-push preflight legs that refused every push (2 lockfile-cleanroom.sh, 6 audit-gate.mjs,
# 7 audit-locks.mjs), run by the TESTER in its OWN worktree. macOS bash 3.2 compatible; zsh-safe: every rc is read as `cmd > f 2> g; rc=$?`
# on its own line, never through a pipe, and never from PIPESTATUS. Writes ONLY into <outdir>.
#
#   c5_legs_gate54f.sh --help
#   c5_legs_gate54f.sh plan <repo> <sha>                     READ-ONLY: the leg files exist at <sha>; both gates read AUDIT_BASELINE_PATH there.
#   c5_legs_gate54f.sh parse-selftest <outdir>               the advisory-name parser on planted lines: a FAIL line counts, a CLEANUP line does not.
#   c5_legs_gate54f.sh run <devdir> <label> <outdir> head|base
#        <devdir> = <your worktree>/Blockchain/Dev. Installs scripts/audit's OWN lock (npm ci --ignore-scripts), then legs 2, 6, 7.
#        head: want rc 0 on 2, 6 and 7, and 0 of the three advisories named.   base: want legs 6 AND 7 rc 1 and the three advisories
#        named across them (leg 2 reported). rc 2 = SKIP (registry unreachable) and is NEVER a pass; rc 3 = the gate REFUSED.
#   c5_legs_gate54f.sh bite <devdir> <outdir> [--prepare-only]
#        for EACH new row: a copy of the head baseline with ONLY that row removed, passed by AUDIT_BASELINE_PATH (the gates read it at
#        audit-gate.mjs:46 / audit-locks.mjs:64; the worktree is never edited). Want: leg 6 or 7 rc 1 naming that advisory. NO-OP CONTROL:
#        an unmodified copy by the same variable must give rc 0 on both (the path itself does not break the gates).
# Exit: 0 when every expectation of the mode held; 1 when one did not (the MISMATCH lines say which); 2 usage / refusal.
set -u
GS="$(dirname "$(/bin/realpath "$0")")"
KJ() { python3 -c 'import json,sys; v=json.load(open(sys.argv[1]))[sys.argv[2]]; print(" ".join(sorted(v)) if isinstance(v,dict) else v)' "$GS/kit.json" "$1"; }
ADV="$(KJ advisories)"; NEWROWS="$(KJ new_rows)"
usage() { sed -n '2,20p' "$0" | sed 's/^# \{0,1\}//'; }
MODE="${1:-}"
[ -n "$MODE" ] || { usage; exit 2; }
if [ "$MODE" = "--help" ] || [ "$MODE" = "-h" ]; then usage; exit 0; fi

names() {  # $1 = a leg's stderr file -> the GHSA ids it lists as FAIL rows (`  - GHSA-x [sev] pkg`), never CLEANUP rows (`  - GHSA-x (pkg, ticket)`)
  sed -n 's/^  - \(GHSA-[a-z0-9]\{4\}-[a-z0-9]\{4\}-[a-z0-9]\{4\}\) \[.*$/\1/p' "$1" | sort -u
}
class() { case "$1" in 0) echo PASS;; 1) echo FAIL;; 2) echo "SKIP (not a pass)";; 3) echo REFUSED;; *) echo "ERROR rc $1";; esac; }

case "$MODE" in
plan)
  REPO="${2:?repo}"; SHA="${3:?sha}"; BAD=0
  echo "c5 plan $(date -u +%Y-%m-%dT%H:%M:%SZ) | repo $REPO | sha $SHA (read-only: cat-file / show)"
  for P in $(python3 -c 'import json,sys; print(" ".join(json.load(open(sys.argv[1]))["legs"].values()))' "$GS/kit.json"); do
    git -C "$REPO" cat-file -e "$SHA:$P" > /dev/null 2>&1
    rc=$?
    echo "  leg file $P at $SHA: $([ $rc -eq 0 ] && echo present || echo ABSENT) (cat-file rc $rc)"; [ $rc -eq 0 ] || BAD=1
  done
  git -C "$REPO" cat-file -e "$SHA:Blockchain/Dev/scripts/audit/no-such-file.mjs" > /dev/null 2>&1
  rc=$?
  echo "  CONTROL a path that does not exist: cat-file rc $rc (want non-zero)"; [ $rc -ne 0 ] || BAD=1
  for P in Blockchain/Dev/scripts/audit/audit-gate.mjs Blockchain/Dev/scripts/audit/audit-locks.mjs; do
    L="$(git -C "$REPO" show "$SHA:$P" | grep -n 'process.env.AUDIT_BASELINE_PATH' | head -1)"
    echo "  $P reads AUDIT_BASELINE_PATH: ${L:-NOT FOUND}"; [ -n "$L" ] || BAD=1
  done
  echo "  the tester runs, from its OWN worktree at HEAD and at the base:"
  echo "    $0 run <wt>/Blockchain/Dev head-<sha12> <evidence>/legs_head head"
  echo "    $0 run <wt-base>/Blockchain/Dev base-88e8877a2a0d <evidence>/legs_base base"
  echo "    $0 bite <wt>/Blockchain/Dev <evidence>/bite"
  echo "PLAN $([ $BAD -eq 0 ] && echo OK || echo MISMATCH)"; exit $BAD ;;
parse-selftest)
  OUT="${2:?outdir}"; mkdir -p "$OUT"; F="$OUT/parse_plant.err"
  printf '%s\n' 'audit-gate: 3 distinct advisories reported, 24 baselined.' '' 'CLEANUP (advisory): 1 baseline entry is no longer reported — remove:' \
    '  - GHSA-2mjp-6q6p-2qxm (undici, KS-470)' 'FAIL — 1 NEW advisory not in the baseline:' '  - GHSA-ch52-4w7c-c8xp [high] http-cache-semantics: planted title' \
    '    https://github.com/advisories/GHSA-ch52-4w7c-c8xp' > "$F"
  N="$(names "$F" | tr '\n' ' ')"
  echo "c5 parse-selftest | planted file $F | parsed FAIL ids: [${N}]"
  [ "$N" = "GHSA-ch52-4w7c-c8xp " ] && { echo "PARSE OK — the FAIL row counts; the CLEANUP row and the advisory URL line do not"; exit 0; }
  echo "PARSE MISMATCH — want exactly [GHSA-ch52-4w7c-c8xp]"; exit 1 ;;
run|bite)
  DEV="${2:?devdir}"
  case "$DEV" in /Volumes/DevMASTER/*) echo "REFUSING: $DEV is on /Volumes/DevMASTER — run legs only in YOUR OWN worktree on the Data volume, never the shared checkout or a builder's worktree"; exit 2;; esac
  [ -f "$DEV/scripts/audit/audit-gate.mjs" ] && [ -f "$DEV/scripts/preflight/lockfile-cleanroom.sh" ] || { echo "REFUSING: $DEV is not a Blockchain/Dev directory"; exit 2; }
  TSHA="$(git -C "$DEV" rev-parse HEAD 2>/dev/null)"
  DIRTY="$(git -C "$DEV" status --porcelain --untracked-files=no 2>/dev/null)"
  [ -z "$DIRTY" ] || { echo "REFUSING: tracked changes in $DEV — the legs must read the committed tree:"; echo "$DIRTY"; exit 2; }
  ;;
*) usage; exit 2 ;;
esac

if [ "$MODE" = "run" ]; then
  LABEL="${3:?label}"; OUT="${4:?outdir}"; EXP="${5:?head|base}"; mkdir -p "$OUT"
  echo "c5 run $LABEL ($EXP) $(date -u +%Y-%m-%dT%H:%M:%SZ) | tree HEAD $TSHA | node $(node -v) | npm $(npm -v) | outdir $OUT"
  npm --prefix "$DEV/scripts/audit" ci --ignore-scripts --no-audit --no-fund > "$OUT/install_audit.out" 2> "$OUT/install_audit.err"
  rc=$?
  echo "$rc" > "$OUT/install_audit.rc"; echo "  scripts/audit npm ci rc $rc"
  [ -d "$DEV/scripts/audit/node_modules/semver" ] && echo "  semver resolvable from scripts/audit: yes" || echo "  semver resolvable from scripts/audit: NO (leg 7 will not run)"
  bash "$DEV/scripts/preflight/lockfile-cleanroom.sh" > "$OUT/leg2.out" 2> "$OUT/leg2.err"
  rc2=$?
  echo "$rc2" > "$OUT/leg2.rc"
  node "$DEV/scripts/audit/audit-gate.mjs" > "$OUT/leg6.out" 2> "$OUT/leg6.err"
  rc6=$?
  echo "$rc6" > "$OUT/leg6.rc"
  node "$DEV/scripts/audit/audit-locks.mjs" > "$OUT/leg7.out" 2> "$OUT/leg7.err"
  rc7=$?
  echo "$rc7" > "$OUT/leg7.rc"
  names "$OUT/leg6.err" > "$OUT/leg6.named"; names "$OUT/leg7.err" > "$OUT/leg7.named"
  echo "  leg 2 rc $rc2 $(class $rc2) | $(grep -c '^OK\|OK$' "$OUT/leg2.out") OK-line(s) in leg2.out | last: $(tail -1 "$OUT/leg2.out")"
  echo "  leg 6 rc $rc6 $(class $rc6) | $(grep -m1 'distinct advisories reported' "$OUT/leg6.out") | FAIL rows named in leg6.err: $(tr '\n' ' ' < "$OUT/leg6.named")"
  echo "  leg 7 rc $rc7 $(class $rc7) | $(grep -m1 -o '[0-9]* advisories match, [0-9]* already baselined' "$OUT/leg7.out") | FAIL rows named in leg7.err: $(tr '\n' ' ' < "$OUT/leg7.named")"
  BAD=0; NAMED=0
  for G in $ADV; do
    if grep -qx "$G" "$OUT/leg6.named" || grep -qx "$G" "$OUT/leg7.named"; then NAMED=$((NAMED+1)); W=named; else W="not named"; fi
    echo "  $G: $W (in $(grep -lx "$G" "$OUT/leg6.named" "$OUT/leg7.named" 2>/dev/null | sed 's#.*/##' | tr '\n' ' '))"
  done
  if [ "$EXP" = head ]; then
    if [ $rc2 -eq 0 ] && [ $rc6 -eq 0 ] && [ $rc7 -eq 0 ] && [ $NAMED -eq 0 ]; then :; else BAD=1; fi
    echo "LEGS $LABEL head: want 2/6/7 rc 0 0 0 and 0 of 3 named | got $rc2 $rc6 $rc7 and $NAMED named -> $([ $BAD -eq 0 ] && echo OK || echo MISMATCH)"
  else
    if [ $rc6 -eq 1 ] && [ $rc7 -eq 1 ] && [ $NAMED -eq 3 ]; then :; else BAD=1; fi
    echo "LEGS $LABEL base CONTROL: want 6/7 rc 1 1 and 3 of 3 named (leg 2 reported: rc $rc2) | got $rc6 $rc7 and $NAMED named -> $([ $BAD -eq 0 ] && echo OK || echo MISMATCH)"
  fi
  exit $BAD
fi

# bite
OUT="${3:?outdir}"; mkdir -p "$OUT"; BL="$DEV/scripts/audit/audit-baseline.json"
echo "c5 bite $(date -u +%Y-%m-%dT%H:%M:%SZ) | tree HEAD $TSHA | baseline $BL | outdir $OUT"
python3 - "$BL" "$OUT" $NEWROWS <<'PY'
import json, sys, shutil
bl, out, ids = sys.argv[1], sys.argv[2], sys.argv[3:]
d = json.load(open(bl, encoding='utf-8')); shutil.copyfile(bl, out + '/baseline_copy.json'); miss = [i for i in ids if i not in d['accepted']]
if miss: print('REFUSING: cannot bite — row(s) %s ABSENT from %s (this tree does not carry the PR\'s rows)' % (miss, bl)); sys.exit(2)
for i in ids:
    e = json.loads(json.dumps(d)); del e['accepted'][i]
    json.dump(e, open('%s/baseline_minus_%s.json' % (out, i), 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('  wrote baseline_minus_%s.json: %d rows (from %d)' % (i, len(e['accepted']), len(d['accepted'])))
PY
rc=$?
[ $rc -eq 0 ] || exit 2
[ "${4:-}" = "--prepare-only" ] && { echo "PREPARED ONLY (no leg run)"; exit 0; }
BAD=0
for V in copy $NEWROWS; do
  if [ "$V" = copy ]; then F="$OUT/baseline_copy.json"; else F="$OUT/baseline_minus_$V.json"; fi
  AUDIT_BASELINE_PATH="$F" node "$DEV/scripts/audit/audit-gate.mjs" > "$OUT/bite_${V}_leg6.out" 2> "$OUT/bite_${V}_leg6.err"
  r6=$?
  echo "$r6" > "$OUT/bite_${V}_leg6.rc"
  AUDIT_BASELINE_PATH="$F" node "$DEV/scripts/audit/audit-locks.mjs" > "$OUT/bite_${V}_leg7.out" 2> "$OUT/bite_${V}_leg7.err"
  r7=$?
  echo "$r7" > "$OUT/bite_${V}_leg7.rc"
  if [ "$V" = copy ]; then
    if [ $r6 -eq 0 ] && [ $r7 -eq 0 ]; then W=OK; else W=MISMATCH; BAD=1; fi
    echo "  NO-OP CONTROL (unmodified copy via AUDIT_BASELINE_PATH): leg 6 rc $r6 $(class $r6), leg 7 rc $r7 $(class $r7) -> want 0 0: $W"
  else
    N6="$(names "$OUT/bite_${V}_leg6.err" | grep -cx "$V")"; N7="$(names "$OUT/bite_${V}_leg7.err" | grep -cx "$V")"
    W=MISMATCH
    if [ $r6 -eq 1 ] && [ "$N6" = 1 ]; then W=OK; fi
    if [ $r7 -eq 1 ] && [ "$N7" = 1 ]; then W=OK; fi
    [ "$W" = OK ] || BAD=1
    echo "  BITE $V removed alone: leg 6 rc $r6 $(class $r6) names it ${N6}x | leg 7 rc $r7 $(class $r7) names it ${N7}x -> want a red leg naming it: $W"
  fi
done
echo "BITE $([ $BAD -eq 0 ] && echo OK || echo MISMATCH)"; exit $BAD
