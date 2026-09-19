#!/bin/bash
# test_only_multiline_tamper_arms.sh <clone-dir> [scratch-out-dir] — arms for the test_only BLOCK TAMPER (2026-09-19)
#
# The defect: a test_only tamper was ONE line (`Line:` + a one-line From/To). The #1070-#1076 gate's REVOKEGUARDAFTER404
# and REVOKEGUARDBELOWREASON are 4-line guard MOVES in vc-issuer/src/routes/status.ts, so they could not be briefed.
# The fix: a From fence of 2+ lines is a BLOCK tamper, matched EXACTLY and UNIQUELY as whole lines in the product file at
# the tip (else REFUSED, naming why); the checker plants it after the same check and restores by bytes (T8).
#
# <clone-dir> must be a `git clone --shared` of the Secuura checkout, checked out at f9c28a8b8 and farmed by
# tasks/test_only/prepare_clone.sh (vc-issuer's node_modules), with a clean `git status`. The arms write only into the
# scratch-out dir and that clone. They are read-only on the Secuura checkout (the builder's git show / ls-tree).
#   (a) night/briefs/KS-1269-N71-2.md (two block tampers) builds; the REAL checker on the brief's own diff plants both
#       blocks, gives RESULT PASS (8/8), and status.ts is byte-identical to the tip blob afterwards
#   (b) a 2-line block that occurs TWICE in status.ts (:231 and :300) is REFUSED, naming the count and the lines
#   (c) a block that does not occur (one byte changed) is REFUSED; (c2) a block with a wrong `Line:` cross-check is REFUSED
#   (d) the existing single-line briefs KS-1230-N74-1 (api-gateway) and KS-1269-N71-1 (vc-issuer, Runner: pin) build
#       BYTE-IDENTICAL input, stdout and stderr with the new and the OLD (.pre-0919-multiline) builder
#   (e) NEGATIVE CONTROL: the OLD builder refuses (a)'s brief (rc 2, "From/To must be ONE line each"), so (a) is green
#       only because of the fix
#   (f) after (a) the clone's `git status` shows ONLY the test file the checker applied (the product file is clean); with
#       that file checked out again the status is empty
#   (g) T8 still fires for a block: TO_TEST_SKIP_RESTORE=REVOKEGUARDBELOWREASON makes the checker stop "stopped at T8"
#       (the clone's status.ts is then checked out again by this arm)
#   (h) single-line regression through the NEW checker: KS-1269-N71-1 + its held canonical diff gives RESULT PASS (8/8)
# rc 0 only when every arm PASSes. bash 3.2. stderr never discarded (captured per arm).
set -uo pipefail
LM="$(cd "$(dirname "$0")/.." && pwd)"
NEW="$LM/tasks/test_only/build_test_only_input.sh"
OLD="$LM/tasks/test_only/build_test_only_input.sh.pre-0919-multiline"
CHK="$LM/tasks/test_only/checker.sh"
B712="$LM/night/briefs/KS-1269-N71-2.md"
B711="$LM/night/briefs/KS-1269-N71-1.md"
B1230="$LM/night/briefs/KS-1230-N74-1.md"
P711="$LM/runs/2026-09-19_ks1269-ornith35b-night3/out.md.checker/patch.diff"
CLONE="${1:-}"
[ -d "$CLONE/.git" ] || { echo "usage: test_only_multiline_tamper_arms.sh <prepared-clone-at-f9c28a8b8> [out-dir]" >&2; exit 1; }
O="${2:-$(mktemp -d "${TMPDIR:-/tmp}/multiline_arms.XXXXXX")}"; mkdir -p "$O"
echo "arms out: $O · clone: $CLONE"
for f in "$NEW" "$OLD" "$CHK" "$B712" "$B711" "$B1230" "$P711"; do [ -f "$f" ] || { echo "missing $f" >&2; exit 1; }; done
ST=Blockchain/Dev/services/vc-issuer/src/routes/status.ts
TFR=Blockchain/Dev/services/vc-issuer/src/__tests__/ks1269-status-revoke-refuses-a-non-integer-index.test.ts
TIP=f9c28a8b82874708edd9de72c40cdb9bfc6ee4cf
[ "$(git -C "$CLONE" rev-parse HEAD)" = "$TIP" ] || { echo "clone HEAD is not $TIP" >&2; exit 1; }
[ -z "$(git -C "$CLONE" status --porcelain)" ] || { echo "clone not clean at start" >&2; git -C "$CLONE" status --porcelain >&2; exit 1; }
TIPSHA="$(git -C "$CLONE" show "$TIP:$ST" | shasum -a 256 | cut -c1-64)"
F=0
ok() { echo "PASS $1"; }
no() { echo "FAIL $1"; F=$((F+1)); }
# out.md holding exactly one ```diff block = the brief's own `## The exact change` fence under the two file headers
mk_out() {
  python3 - "$1" "$2" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
tf = re.search(r"^File:\s*`([^`]+)`", t, re.M).group(1)
xs = re.search(r"^## The exact change.*?$(.*?)(?=^##\s)", t, re.M | re.S).group(1)
body = re.search(r"^```\n(.*?)^```", xs, re.M | re.S).group(1)
open(sys.argv[2], "w", encoding="utf-8").write(f"```diff\n--- a/{tf}\n+++ b/{tf}\n{body}```\n")
PY
}
# a variant of the N71-2 brief whose `## Tampers` section is replaced by ONE block tamper (From/To given as text)
mk_variant() {   # <out.md> <line-or-empty> <from-text-file> <to-text-file>
  python3 - "$B712" "$1" "$2" "$3" "$4" <<'PY'
import re, sys
src, out, line, ff, tf = sys.argv[1:6]
t = open(src, encoding="utf-8").read()
frm = open(ff, encoding="utf-8").read().rstrip("\n"); to = open(tf, encoding="utf-8").read().rstrip("\n")
sec = ("## Tampers\n\n### VARIANT — arms only\nFile: `Blockchain/Dev/services/vc-issuer/src/routes/status.ts`\n"
       + (f"Line: {line}\n" if line else "") + "From:\n```\n" + frm + "\n```\nTo:\n```\n" + to + "\n```\nReds: `badreason`\n\n")
t2 = re.sub(r"^## Tampers\b.*?(?=^## Controls)", lambda m: sec, t, count=1, flags=re.M | re.S)
assert t2 != t
open(out, "w", encoding="utf-8").write(t2)
PY
}

# (a) block tampers build; the real checker plants + restores them; RESULT PASS (8/8); status.ts == tip blob after
bash "$NEW" KS-1269 "$O/a.json" "$B712" ctx=65536 > "$O/a_build.out" 2> "$O/a_build.err"; rc_ab=$?
mk_out "$B712" "$O/a_out.md"
bash "$CHK" "$O/a.json" "$O/a_out.md" "$CLONE" > "$O/a_chk.out" 2>&1; rc_ac=$?
NOWSHA="$(shasum -a 256 "$CLONE/$ST" | cut -c1-64)"
NBLK="$(/usr/bin/grep -c "^tamper .*: planted .* (block " "$O/a_chk.out")"
if [ "$rc_ab" -eq 0 ] && [ "$(python3 -c 'import json,sys; print(sum(1 for t in json.load(open(sys.argv[1]))["tampers"] if t.get("block")))' "$O/a.json")" = 2 ] \
   && [ "$rc_ac" -eq 0 ] && /usr/bin/grep -q "^RESULT: PASS (8/8)$" "$O/a_chk.out" && [ "$NBLK" -eq 2 ] \
   && [ "$(/usr/bin/grep -c '^PASS T8\[' "$O/a_chk.out")" -eq 2 ] && [ "$NOWSHA" = "$TIPSHA" ]; then
  ok "(a) KS-1269-N71-2: builds 2 block tampers; checker planted $NBLK blocks, 2x T8 PASS, RESULT PASS (8/8); status.ts sha256 ${NOWSHA:0:12} == tip blob"
else no "(a) build rc $rc_ab, checker rc $rc_ac, blocks planted $NBLK, status.ts ${NOWSHA:0:12} vs tip ${TIPSHA:0:12}; $(tail -2 "$O/a_chk.out" | tr '\n' ' ') $(head -c 300 "$O/a_build.err")"; fi

# (f) the restore leaves the clone clean: only the applied test file is modified; with it checked out, nothing
ST_A="$(git -C "$CLONE" status --porcelain)"
git -C "$CLONE" checkout -- "$TFR" > "$O/f_checkout.out" 2>&1
ST_F="$(git -C "$CLONE" status --porcelain --untracked-files=all)"
if [ "$ST_A" = " M $TFR" ] && [ -z "$ST_F" ]; then
  ok "(f) after (a): git status = only ' M <the test file>' (the product file clean); after checking the test file out: empty"
else no "(f) git status after (a): [$ST_A]; after test-file checkout: [$ST_F]"; fi

# (b) a 2-line block that occurs twice (:231, :300) is refused, naming the count
printf '%s\n' "    if (req.body.index !== undefined && !Number.isInteger(req.body.index)) {" "      throw new AppError('index must be an integer', 400);" > "$O/b_from.txt"
printf '%s\n' "    if (req.body.index != null && !Number.isInteger(req.body.index)) {" "      throw new AppError('index must be an integer', 400);" > "$O/b_to.txt"
mk_variant "$O/b_brief.md" "" "$O/b_from.txt" "$O/b_to.txt"
bash "$NEW" KS-1269 "$O/b.json" "$O/b_brief.md" ctx=65536 > "$O/b.out" 2> "$O/b.err"; rc_b=$?
if [ "$rc_b" -eq 2 ] && /usr/bin/grep -q "occurs 2 times in .*starting at lines \[231, 300\]" "$O/b.err" && [ ! -e "$O/b.json" ]; then
  ok "(b) a 2-line block occurring twice: rc 2, 'occurs 2 times … starting at lines [231, 300]', no input written"
else no "(b) rc $rc_b; $(head -c 300 "$O/b.err")"; fi

# (c) a block that does not occur (one byte changed in its 2nd line) is refused; (c2) a wrong Line: cross-check refused
python3 - "$B712" "$O" <<'PY'
import re, sys
t = open(sys.argv[1], encoding="utf-8").read()
blk = re.search(r"^### REVOKEGUARDBELOWREASON.*?^From:\n```\n(.*?)\n```\nTo:\n```\n(.*?)\n```", t, re.M | re.S)
frm, to = blk.group(1), blk.group(2)
open(sys.argv[2] + "/c_from.txt", "w").write(frm.replace("!Number.isInteger", "!Number.isFinite", 1) + "\n")
open(sys.argv[2] + "/c2_from.txt", "w").write(frm + "\n"); open(sys.argv[2] + "/c_to.txt", "w").write(to + "\n")
PY
mk_variant "$O/c_brief.md" "" "$O/c_from.txt" "$O/c_to.txt"
bash "$NEW" KS-1269 "$O/c.json" "$O/c_brief.md" ctx=65536 > "$O/c.out" 2> "$O/c.err"; rc_c=$?
if [ "$rc_c" -eq 2 ] && /usr/bin/grep -q "From block does not occur in" "$O/c.err" && [ ! -e "$O/c.json" ]; then
  ok "(c) a block with one byte changed: rc 2, 'does not occur', no input written"
else no "(c) rc $rc_c; $(head -c 300 "$O/c.err")"; fi
mk_variant "$O/c2_brief.md" "231" "$O/c2_from.txt" "$O/c_to.txt"
bash "$NEW" KS-1269 "$O/c2.json" "$O/c2_brief.md" ctx=65536 > "$O/c2.out" 2> "$O/c2.err"; rc_c2=$?
if [ "$rc_c2" -eq 2 ] && /usr/bin/grep -q "Line: 231 but the From block starts at .*:230" "$O/c2.err" && [ ! -e "$O/c2.json" ]; then
  ok "(c2) the right block with Line: 231 (it starts at 230): rc 2, the cross-check names both"
else no "(c2) rc $rc_c2; $(head -c 300 "$O/c2.err")"; fi

# (d) single-line briefs: NEW builder output byte-identical to the OLD builder's (input, stdout, stderr)
for B in "$B1230:KS-1230" "$B711:KS-1269"; do
  BF="${B%%:*}"; BI="${B##*:}"; N="$(basename "$BF" .md)"
  bash "$NEW" "$BI" "$O/d_${N}_new.json" "$BF" ctx=65536 > "$O/d_${N}_new.out" 2> "$O/d_${N}_new.err"; rn=$?
  bash "$OLD" "$BI" "$O/d_${N}_old.json" "$BF" ctx=65536 > "$O/d_${N}_old.out" 2> "$O/d_${N}_old.err"; ro=$?
  if [ "$rn" -eq 0 ] && [ "$ro" -eq 0 ] && cmp -s "$O/d_${N}_new.json" "$O/d_${N}_old.json" && cmp -s "$O/d_${N}_new.err" "$O/d_${N}_old.err" \
     && [ "$(sed "s#$O/d_${N}_new.json#X#" "$O/d_${N}_new.out")" = "$(sed "s#$O/d_${N}_old.json#X#" "$O/d_${N}_old.out")" ]; then
    ok "(d) $N (single-line tampers): new input byte-identical to the old builder's ($(shasum -a 256 < "$O/d_${N}_new.json" | cut -c1-12)), stdout/stderr identical"
  else no "(d) $N: rc new=$rn old=$ro; cmp: $(cmp "$O/d_${N}_new.json" "$O/d_${N}_old.json" 2>&1 | head -1)"; fi
done

# (e) NEGATIVE CONTROL: the OLD builder cannot express (a)'s brief
bash "$OLD" KS-1269 "$O/e.json" "$B712" ctx=65536 > "$O/e.out" 2> "$O/e.err"; rc_e=$?
if [ "$rc_e" -eq 2 ] && /usr/bin/grep -q "From/To must be ONE line each" "$O/e.err" && [ ! -e "$O/e.json" ]; then
  ok "(e) OLD builder on KS-1269-N71-2: rc 2 'From/To must be ONE line each' — the arm discriminates"
else no "(e) OLD builder on KS-1269-N71-2: rc $rc_e (expected 2); $(head -c 200 "$O/e.err")"; fi

# (g) T8 fires for a block tamper left unrestored (arms-only hook), then this arm restores the clone
TO_TEST_SKIP_RESTORE=REVOKEGUARDBELOWREASON bash "$CHK" "$O/a.json" "$O/a_out.md" "$CLONE" > "$O/g_chk.out" 2>&1; rc_g=$?
DIRTY_G="$(git -C "$CLONE" status --porcelain -- "$ST")"
git -C "$CLONE" checkout -- "$ST" "$TFR" > "$O/g_checkout.out" 2>&1
if [ "$rc_g" -ne 0 ] && /usr/bin/grep -q "RESULT: FAIL .*stopped at T8" "$O/g_chk.out" && /usr/bin/grep -q "^FAIL T8\[REVOKEGUARDBELOWREASON\] RESTORE FAILED" "$O/g_chk.out" \
   && [ -n "$DIRTY_G" ] && [ -z "$(git -C "$CLONE" status --porcelain --untracked-files=all)" ]; then
  ok "(g) skip-restore hook on the block tamper: FAIL T8 RESTORE FAILED, 'stopped at T8' (the file WAS dirty: [$DIRTY_G]); clone clean again"
else no "(g) rc $rc_g; $(/usr/bin/grep -E '^(FAIL T8|RESULT)' "$O/g_chk.out" | tr '\n' ' ') dirty=[$DIRTY_G]"; fi

# (h) single-line regression through the NEW checker: KS-1269-N71-1 + its held canonical diff
python3 - "$P711" "$O/h_out.md" <<'PY'
import sys
open(sys.argv[2], "w").write("```diff\n" + open(sys.argv[1]).read().rstrip("\n") + "\n```\n")
PY
bash "$CHK" "$O/d_KS-1269-N71-1_new.json" "$O/h_out.md" "$CLONE" > "$O/h_chk.out" 2>&1; rc_h=$?
git -C "$CLONE" checkout -- "$TFR" > "$O/h_checkout.out" 2>&1
if [ "$rc_h" -eq 0 ] && /usr/bin/grep -q "^RESULT: PASS (8/8)$" "$O/h_chk.out" && [ "$(/usr/bin/grep -c "^tamper .*: planted .* (block " "$O/h_chk.out")" -eq 0 ] \
   && [ -z "$(git -C "$CLONE" status --porcelain --untracked-files=all)" ]; then
  ok "(h) KS-1269-N71-1 (single-line tampers) + its held diff through the NEW checker: RESULT PASS (8/8), no block path taken; clone clean after"
else no "(h) rc $rc_h; $(tail -2 "$O/h_chk.out" | tr '\n' ' ')"; fi

N_ARMS=10
[ "$F" -eq 0 ] && { echo "RESULT: PASS ($N_ARMS/$N_ARMS arms)"; exit 0; }
echo "RESULT: FAIL ($F arm(s))"; exit 1
