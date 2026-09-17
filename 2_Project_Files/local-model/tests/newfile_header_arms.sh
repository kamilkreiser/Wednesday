#!/bin/bash
# newfile_header_arms.sh — red-proof for the code_patch A2 NEWFILE HEADER synthesis (2026-09-17 19:1x, KS-938 r1:
# runs/2026-09-17_ks938-ornith35b-night — the model's `--- /dev/null` / `+++ b/<test>` section carried 141 `+` lines and NO
# `@@ -0,0 +1,N @@`, so every apply mode said "No valid patches in input" and the verdict was FAIL A2).
# Every arm runs the REAL checker.sh end to end (sandbox-exec, off-host outbound denied) in a scratch clone at the KS-938
# tip 81ee4b729 against the SAME input (night/inputs/code_938.json) and reads its lines; nothing is re-implemented.
#   1 NEW checker, the REAL KS-938 r1 out.md (a byte-identical copy)   → PASS A2 naming "A2 NEWFILE HEADER SYNTHESIZED
#     (model omitted it; N=141)"; the as-written section kept as section_2.headerless.diff; the model's out.md unchanged
#     (this arm IS the full re-check — its gate lines and RESULT are printed after the arms)
#   2 OLD checker (checker.sh.pre-0917-newfilehdr), the same out.md    → FAIL A2 "No valid patches", stopped at A2 (the
#     control: the arm reaches the change)
#   3 the same out.md WITH `@@ -0,0 +1,141 @@` present                 → NEW: the unchanged strict PASS A2 line, no NEWFILE
#     text, and every PASS/FAIL line but A6 identical to the OLD checker's on the same file
#   4 headerless, one body line's `+` turned into a context space      → NEW: FAIL A2, "newfile header NOT SYNTHESIZED:
#     1 body line(s) not '+'-prefixed", stopped at A2
#   5 headerless, `--- /dev/null` replaced by `--- a/<path>`            → NEW: FAIL A2, "NOT SYNTHESIZED: not a new file"
#   6 headerless, a stray `@@ -0,0 +1,71 @@` in the middle of the body → NEW: FAIL A2, nothing synthesised (an `@@` anywhere)
# A6 may carry the known ks949 flake (KS-1053, ~1 in 7): when arm 1's only A6 new red is a ks949 cell, arm 1 re-runs ONCE
# and says so.
# Usage: NFH_CLONE=<clone at 81ee4b729, services/auth prepared by tasks/code_patch/prepare_clone.sh> bash newfile_header_arms.sh
#   (make the clone as night/night_run.sh does: `git clone --shared --no-checkout <source_checkout> <clone>` +
#    `git -C <clone> checkout --detach <tip>` + prepare_clone.sh, all under a mktemp -d — never in the source)
# env: NFH_CHECKER, NFH_OLD_CHECKER. Writes only under a mktemp -d. rc 0 = every arm PASS.
set -u
LM=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model
CK="${NFH_CHECKER:-$LM/tasks/code_patch/checker.sh}"
OLD="${NFH_OLD_CHECKER:-$LM/tasks/code_patch/checker.sh.pre-0917-newfilehdr}"
CLONE="${NFH_CLONE:-}"
R938=$LM/runs/2026-09-17_ks938-ornith35b-night
INPUT=$LM/night/inputs/code_938.json
SB=$LM/tests/fixtures/a3b_line/nonet.sb
TIP=81ee4b729e86a645fc9098aafa1aaf39035a9950
TESTP=Blockchain/Dev/services/auth/src/__tests__/ks938-security-mfa-disabled-leaves-the-totp.test.ts
[ -n "$CLONE" ] && [ "$(git -C "$CLONE" rev-parse HEAD 2>/dev/null)" = "$TIP" ] || { echo "FATAL: NFH_CLONE ($CLONE) is not a clone at $TIP"; exit 2; }
[ -f "$CK" ] && [ -f "$OLD" ] && [ -f "$R938/out.md" ] && [ -f "$INPUT" ] && [ -f "$SB" ] || { echo "FATAL: a subject file is missing"; exit 2; }
# positive control for /usr/bin/grep: the real checker.out carries the FAIL A2 line this work answers
/usr/bin/grep -q '^FAIL A2 diff does NOT apply' "$R938/checker.out" || { echo "FATAL: grep positive control failed (the KS-938 r1 FAIL A2 line not found)"; exit 2; }
SP="$(mktemp -d "${TMPDIR:-/tmp}/nfh_arms.XXXXXX")"; echo "scratch: $SP"
SHA0="$(shasum "$R938/out.md" | cut -d' ' -f1)"

python3 - "$R938/out.md" "$SP" "$TESTP" <<'PYFX'
import sys
src, sp, tp = sys.argv[1:4]
L = open(src, encoding="utf-8").read().split("\n")
pi = [i for i, l in enumerate(L) if l == "+++ b/" + tp]; assert len(pi) == 1, pi
pi = pi[0]; assert L[pi - 1] == "--- /dev/null" and L[pi + 1].startswith("+"), (L[pi - 1], L[pi + 1])
fence = [i for i in range(pi + 1, len(L)) if L[i].startswith("```")][0]
body = L[pi + 1:fence]; assert len(body) == 141 and all(b.startswith("+") for b in body), len(body)
def w(name, lines): open(f"{sp}/{name}.md", "w", encoding="utf-8").write("\n".join(lines))
w("hdr_present", L[:pi + 1] + ["@@ -0,0 +1,141 @@"] + L[pi + 1:])
k = next(i for i in range(pi + 1, fence) if L[i].startswith("+import "))
w("ctx_line", L[:k] + [" " + L[k][1:]] + L[k + 1:])
w("not_devnull", L[:pi - 1] + ["--- a/" + tp] + L[pi:])
w("stray_at", L[:pi + 71] + ["@@ -0,0 +1,71 @@"] + L[pi + 71:])
print(f"fixtures written (body=141, context-space line = out.md line {k + 1})")
PYFX
[ -f "$SP/stray_at.md" ] || { echo "FATAL: fixture generation failed"; exit 2; }

fail=0
ok(){ echo "ARM$1 PASS — $2"; }
bad(){ echo "ARM$1 FAIL — $2"; fail=1; }
run_ck(){ # run_ck <label> <checker> <out.md> — runs into $SP/<label>/, sets RC and CO
  local d="$SP/$1"; mkdir -p "$d"; cp "$3" "$d/out.md"; [ -f "$R938/out.md.meta.json" ] && cp "$R938/out.md.meta.json" "$d/out.md.meta.json"
  echo "  .. $1 start $(date +%H:%M:%S)"
  nice -n 5 sandbox-exec -f "$SB" bash "$2" "$INPUT" "$d/out.md" "$CLONE" > "$d/checker.out" 2>&1
  RC=$?; CO="$d/checker.out"
  echo "  .. $1 end $(date +%H:%M:%S) rc=$RC :: $(/usr/bin/grep -E '^(FAIL|RESULT)' "$CO" | cut -c1-300 | tr '\n' '|')"
}
has(){ /usr/bin/grep -q -E "$2" "$1"; }
gates(){ /usr/bin/grep -E '^(PASS|FAIL) ' "$1" | /usr/bin/grep -v -E '^(PASS|FAIL) A6 '; }

echo "--- arm 1: NEW checker, the real KS-938 r1 out.md (the full re-check)"
run_ck A1_new_real "$CK" "$R938/out.md"
A6FLAKE_NOTE=""
if has "$CO" '^FAIL A6 ' && ! has "$CO" '^FAIL A[^6]'; then
  NEWREDS="$(/usr/bin/grep '^NEW reds:' "$SP/A1_new_real/out.md.checker/suite_delta.out")"
  if echo "$NEWREDS" | /usr/bin/grep -q -i 'ks949' && [ "$(echo "$NEWREDS" | /usr/bin/grep -o "('" | /usr/bin/grep -c .)" -eq "$(echo "$NEWREDS" | /usr/bin/grep -o -i "('[^']*ks949" | /usr/bin/grep -c .)" ]; then
    A6FLAKE_NOTE="A6 failed on the ks949 flake alone on the first run ($NEWREDS) — re-ran once"
    echo "  .. $A6FLAKE_NOTE"
    mv "$SP/A1_new_real" "$SP/A1_new_real.flake1"
    run_ck A1_new_real "$CK" "$R938/out.md"
  fi
fi
H="$SP/A1_new_real/out.md.checker"
SEC_AW="$R938/out.md.checker/section_2.diff"   # the night run's split of the same section, as written
REPAIRED_OK=0
if [ -f "$H/section_2.headerless.diff" ] && cmp -s "$H/section_2.headerless.diff" "$SEC_AW" && \
   [ "$(sed -n 3p "$H/section_2.diff")" = "@@ -0,0 +1,141 @@" ] && \
   diff <(sed 3d "$H/section_2.diff") "$SEC_AW" > /dev/null; then REPAIRED_OK=1; fi
if has "$CO" "^PASS A2 diff applies at the tip — with an accommodation: \[$TESTP: A2 NEWFILE HEADER SYNTHESIZED \(model omitted it; N=141\)" && \
   has "$CO" "^section 2 $TESTP: A2 NEWFILE HEADER SYNTHESIZED \(model omitted it; N=141\)" && \
   ! has "$CO" '^FAIL A2' && [ "$REPAIRED_OK" = 1 ] && [ "$(shasum "$R938/out.md" | cut -d' ' -f1)" = "$SHA0" ]; then
  ok 1 "NEW checker on the real out.md: PASS A2 with the synthesized-header note (N=141); section_2.headerless.diff == the night run's as-written section; the repaired section == it + one @@ -0,0 +1,141 @@ line; the model's out.md sha unchanged ($SHA0)"
else bad 1 "rc=$RC repaired_ok=$REPAIRED_OK $(/usr/bin/grep -E '^(PASS A2|FAIL A2|RESULT)' "$CO" | cut -c1-300 | tr '\n' '|')"; fi

echo "--- arm 2: OLD checker, the same out.md (negative control)"
run_ck A2_old_real "$OLD" "$R938/out.md"
if has "$CO" '^FAIL A2 diff does NOT apply at the tip: .*No valid patches in input' && has "$CO" '^RESULT: FAIL \(1 failed\) — stopped at A2' && ! has "$CO" 'NEWFILE'; then
  ok 2 "OLD checker on the same out.md: FAIL A2 'No valid patches in input', RESULT: FAIL (1 failed) — stopped at A2 (the arm reaches the change)"
else bad 2 "rc=$RC $(/usr/bin/grep -E '^(PASS A2|FAIL A2|RESULT)' "$CO" | cut -c1-200 | tr '\n' '|')"; fi

echo "--- arm 3: header present — NEW vs OLD"
run_ck A3_new_hdr "$CK" "$SP/hdr_present.md"; CO3N="$CO"
run_ck A3_old_hdr "$OLD" "$SP/hdr_present.md"; CO3O="$CO"
if has "$CO3N" '^PASS A2 diff applies at the tip \(strict git apply --check, every section, hunk headers consistent\)$' && ! has "$CO3N" 'NEWFILE' && \
   diff <(gates "$CO3N") <(gates "$CO3O") > "$SP/arm3_gates.diff"; then
  ok 3 "header present: NEW prints the unchanged strict PASS A2 line, no NEWFILE text; every PASS/FAIL line except A6 identical to the OLD checker's ($(gates "$CO3N" | /usr/bin/grep -c .) lines) · A6 new=[$(/usr/bin/grep -E '^(PASS|FAIL) A6' "$CO3N" | cut -c1-60)] old=[$(/usr/bin/grep -E '^(PASS|FAIL) A6' "$CO3O" | cut -c1-60)]"
else bad 3 "$(/usr/bin/grep -E '^(PASS A2|FAIL A2)' "$CO3N" | cut -c1-200) · gate diff: $(tr '\n' '|' < "$SP/arm3_gates.diff" | cut -c1-400)"; fi

echo "--- arm 4: headerless with a non-'+' body line"
run_ck A4_new_ctx "$CK" "$SP/ctx_line.md"
if has "$CO" "^FAIL A2 diff does NOT apply at the tip: .*newfile header NOT SYNTHESIZED: 1 body line\(s\) not '\+'-prefixed" && has "$CO" '^RESULT: FAIL \(1 failed\) — stopped at A2' && ! has "$CO" 'SYNTHESIZED \(model omitted'; then
  ok 4 "one context-space body line: FAIL A2 names 'newfile header NOT SYNTHESIZED: 1 body line(s) not '+'-prefixed', stopped at A2"
else bad 4 "rc=$RC $(/usr/bin/grep -E '^(PASS A2|FAIL A2|RESULT)' "$CO" | cut -c1-400 | tr '\n' '|')"; fi

echo "--- arm 5: headerless, not /dev/null"
run_ck A5_new_notdevnull "$CK" "$SP/not_devnull.md"
if has "$CO" '^FAIL A2 diff does NOT apply at the tip: .*newfile header NOT SYNTHESIZED: not a new file' && has "$CO" '^RESULT: FAIL \(1 failed\) — stopped at A2' && ! has "$CO" 'SYNTHESIZED \(model omitted'; then
  ok 5 "--- a/<path> instead of /dev/null: FAIL A2 names 'NOT SYNTHESIZED: not a new file', stopped at A2"
else bad 5 "rc=$RC $(/usr/bin/grep -E '^(PASS A2|FAIL A2|RESULT)' "$CO" | cut -c1-400 | tr '\n' '|')"; fi

echo "--- arm 6: headerless body with a stray @@ mid-body"
run_ck A6_new_strayat "$CK" "$SP/stray_at.md"
if has "$CO" '^FAIL A2 diff does NOT apply at the tip: ' && has "$CO" '^RESULT: FAIL \(1 failed\) — stopped at A2' && ! has "$CO" 'SYNTHESIZED'; then
  ok 6 "an @@ line inside the section: nothing synthesised, FAIL A2 ($(/usr/bin/grep '^FAIL A2' "$CO" | sed -E 's/.*strict: ([^|]*)\|.*/\1/' | cut -c1-90)), stopped at A2"
else bad 6 "rc=$RC $(/usr/bin/grep -E '^(PASS A2|FAIL A2|RESULT)' "$CO" | cut -c1-400 | tr '\n' '|')"; fi

echo "--- full re-check (arm 1's run of the NEW checker on the real KS-938 r1 out.md): gate lines"
[ -n "$A6FLAKE_NOTE" ] && echo "NOTE: $A6FLAKE_NOTE"
/usr/bin/grep -E '^(PASS|FAIL|RESULT|A3b|A3i|INFO A3i|SUMMARY|test-only at tip|test after product hunk|after suite|NEW reds)' "$SP/A1_new_real/checker.out"
/usr/bin/grep -E '^NEW reds' "$SP/A1_new_real/out.md.checker/suite_delta.out" 2>/dev/null
echo "A4 red_first failed_names (both declared reds R1/R2 must be here): $(/usr/bin/grep '^test-only at tip:' "$SP/A1_new_real/checker.out" | /usr/bin/grep -o 'failed_names=.*')"
echo "arms: $([ "$fail" -eq 0 ] && echo 'ALL PASS' || echo 'SOME FAILED') (scratch $SP)"
exit $fail
