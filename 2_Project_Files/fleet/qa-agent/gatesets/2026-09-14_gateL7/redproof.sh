#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_L7_918r2_924_925.sh on SCRATCH COPIES only. Never touches the real dirs.
# Green asserted FIRST (cell 0, rc 0, 15 guard lines), one red per guard at a DISTINCT exit code, every tamper asserted LANDED
# (anchor must exist; the new marker grep'd >= expected; cmp non-identical to pristine; for removals the removed token grep'd 0),
# green again LAST on the sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL and FAILS=N.
# Every cell runs under env -i with a PATH that has git/python3/grep but NO claude, GH_TOKEN unset, 180 s alarm.
# The develop guard's arms against the LIVE tree: pinned at M20 (the shipped pin) -> still (0); pinned at M18 -> the live
# M18..M20 move = #903's three files (JUDGED, at M20's pinned blobs -> excluded) + #982's three services/auth files (not guarded)
# -> MOVED commits=2 files=6, disjoint (0); an unknown develop sha -> UNJUDGEABLE (18); the JUDGED table with M20's preflight.sh
# blob replaced by a bogus id -> develop carries "a version nobody pinned" (18); the JUDGED table with M20's preflight.sh blob
# relabelled LANDED925 -> the stack has landed (22). The stack guard (exit 10): #924's base pinned to M18 -> the compare reads
# d4cf7e3cf (10). The round-1 guard (19) both arms; the head-SHA-in-both guard (20); the TTY guard (21) headless vs pty (16)
# vs neutralised (16).
set -u
G="${G:?set G to the gateL7 dir}"
L="$G/launch_qa_secuura_L7_918r2_924_925.sh"
B="$G/2026-09-14_secuura-L7-918r2-924-925-ks926-ks773-ks1046-tier2.md"
P="$G/2026-09-14_secuura-L7-918r2-924-925-ks926-ks773-ks1046-tier2.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
M18='8861e62161466c40f08d2b10a30edeb203123993'; M20='a5334350221c819f54d4a20a3308daeb9ca09617'
R1='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_918_review_5151452193.md'

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 grep head cat shasum wc cut perl cmp script sed; do ln -s "$(command -v "$t")" "$BIN/$t"; done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "bash: $(/bin/bash --version | head -1)"

run() { # name expected launcher brief prompt head918 mode landed
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" head="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QAL7_BRIEF="$brief" QAL7_PROMPT="$prompt" ${head:+QAL7_HEAD918="$head"} \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-headless" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QAL7_BRIEF="$brief" QAL7_PROMPT="$prompt" \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-pty" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QAL7_BRIEF="$brief" QAL7_PROMPT="$prompt" \
      script -q "$W/$name.typescript" perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  else
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  fi
  local ok="ok"; [ "$rc" = "$exp" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  [ "$landed" = "LANDED" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  printf '%-78s | %3s | %3s | %s | %s\n' "$name" "$exp" "$rc" "$landed" "$ok"
}
tamper() { # src dst old new expect_new_count  (a removal: new="" and the old token must read 0 after)
  local src="$1" dst="$2" old="$3" new="$4" n="$5"
  python3 - "$src" "$dst" "$old" "$new" <<'PY'
import sys
src,dst,old,new=sys.argv[1:5]
s=open(src,encoding="utf-8").read()
assert old in s, f"anchor absent: {old!r}"
open(dst,"w",encoding="utf-8").write(s.replace(old,new))
PY
  local c
  if [ -n "$new" ]; then c="$(/usr/bin/grep -cF -- "$new" "$dst")"; [ "$c" -ge "$n" ] && ! cmp -s "$src" "$dst" && echo LANDED || echo NOT-LANDED
  else c="$(/usr/bin/grep -cF -- "$old" "$dst")"; [ "$c" -eq 0 ] && ! cmp -s "$src" "$dst" && echo LANDED || echo NOT-LANDED; fi
}
DEVPIN="DEVELOP_SHA='$M20'"
saw() { /usr/bin/grep -q -- "$2" "$W/$1.out" || { echo "  $1: output lacks: $2"; FAILS=$((FAILS+1)); }; }

# ---- cell 0: green --check -------------------------------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
saw "0 green --check (scratch brief+prompt)" "all guards pass"
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" = "15" ] || { echo "  green output does not list 15 guard lines"; FAILS=$((FAILS+1)); }
saw "0 green --check (scratch brief+prompt)" "origin develop still $M20 (M20 = #903's squash"
saw "0 green --check (scratch brief+prompt)" "head #918 b54487216ebb49f1de7ed9349f089d92a3e5bfc1 present"
saw "0 green --check (scratch brief+prompt)" "head #925 5341b1daed8afe4254e05ef66ef4350fd8220d4f present"
saw "0 green --check (scratch brief+prompt)" "the stack holds"
saw "0 green --check (scratch brief+prompt)" "brief names both round-1 records"
saw "0 green --check (scratch brief+prompt)" "will refuse unless stdin is a TTY (exit 21)"
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$W/0 green --check (scratch brief+prompt).out" | cut -c1-140)"

# ---- head / stack / develop ------------------------------------------------------------------------------
run "1 wrong #918 head sha (env override)" 6 "$L" "$B" "$P" "0000000000000000000000000000000000000000" check LANDED
saw "1 wrong #918 head sha (env override)" "#918's head moved"
cp "$L" "$W/l_h925.sh"; ld="$(tamper "$L" "$W/l_h925.sh" "HEAD_925=\"\${QAL7_HEAD925:-5341b1daed8afe4254e05ef66ef4350fd8220d4f}\"" "HEAD_925=\"\${QAL7_HEAD925:-b54487216ebb49f1de7ed9349f089d92a3e5bfc1}\"" 1)"
run "1b #925 head pinned to #918's sha (launcher tamper)" 6 "$W/l_h925.sh" "$B" "$P" "" check "$ld"
saw "1b #925 head pinned to #918's sha (launcher tamper)" "#925's head moved"
cp "$L" "$W/l_b924.sh"; ld="$(tamper "$L" "$W/l_b924.sh" "BASE_924='d4cf7e3cf73e91422a229b7d0767cf6c3a04fe57'" "BASE_924='$M18'" 1)"
run "2 #924's base pinned to M18 -> the compare reads d4cf7e3cf" 10 "$W/l_b924.sh" "$B" "$P" "" check "$ld"
saw "2 #924's base pinned to M18 -> the compare reads d4cf7e3cf" "the stack is not what the brief pins"
cp "$L" "$W/l_env.sh"; ld="$(tamper "$L" "$W/l_env.sh" "4_Credentials/.env'" "4_Credentials/.env.does-not-exist'" 1)"
run "3 env file missing -> compare API unreadable" 13 "$W/l_env.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "$DEVPIN" "DEVELOP_SHA='1111111111111111111111111111111111111111'" 1)"
run "4 unknown develop sha -> unjudgeable" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
saw "4 unknown develop sha -> unjudgeable" "not provably disjoint: UNJUDGEABLE"
cp "$L" "$W/l_dev18.sh"; ld="$(tamper "$L" "$W/l_dev18.sh" "$DEVPIN" "DEVELOP_SHA='$M18'" 1)"
run "4b pinned at M18: live M18..M20 = 3 judged (at M20 blobs) + 3 services-auth -> disjoint -> 0" 0 "$W/l_dev18.sh" "$B" "$P" "" check "$ld"
saw "4b pinned at M18: live M18..M20 = 3 judged (at M20 blobs) + 3 services-auth -> disjoint -> 0" "origin develop MOVED $M18 -> $M20: commits=2 files=6"
echo "  cell 4b note: $(/usr/bin/grep -o 'origin develop MOVED[^—]*' "$W/4b pinned at M18: live M18..M20 = 3 judged (at M20 blobs) + 3 services-auth -> disjoint -> 0.out" | cut -c1-120)"
cp "$L" "$W/l_judged.sh"; ld="$(tamper "$L" "$W/l_judged.sh" "0727300f79938fd26b578ed77fca281e49662c6f:M20" "0000000000000000000000000000000000000000:M20" 1)"
run "4c JUDGED: M20's preflight.sh blob replaced by a bogus id -> unpinned version -> 18" 18 "$W/l_judged.sh" "$B" "$P" "" check "$ld"
saw "4c JUDGED: M20's preflight.sh blob replaced by a bogus id -> unpinned version -> 18" "a version nobody pinned: preflight.sh 0727300f7"
cp "$L" "$W/l_landed.sh"; ld="$(tamper "$L" "$W/l_landed.sh" "0727300f79938fd26b578ed77fca281e49662c6f:M20" "0727300f79938fd26b578ed77fca281e49662c6f:LANDED925" 1)"
run "4d JUDGED: M20's preflight.sh blob relabelled LANDED925 -> the stack has landed -> 22" 22 "$W/l_landed.sh" "$B" "$P" "" check "$ld"
saw "4d JUDGED: M20's preflight.sh blob relabelled LANDED925 -> the stack has landed -> 22" "nothing left to gate but #924"

# ---- files present ---------------------------------------------------------------------------------------
: > "$W/empty.md"
run "5 empty brief" 3 "$L" "$W/empty.md" "$P" "" check LANDED
run "6 empty prompt" 4 "$L" "$B" "$W/empty.md" "" check LANDED
cp "$L" "$W/l_qa.sh"; ld="$(tamper "$L" "$W/l_qa.sh" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN.does-not-exist'" 1)"
run "7 QA project dir missing" 2 "$W/l_qa.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_repo.sh"; ld="$(tamper "$L" "$W/l_repo.sh" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files.does-not-exist'" 1)"
run "8 repo dir missing" 5 "$W/l_repo.sh" "$B" "$P" "" check "$ld"

# ---- brief/prompt agreement -------------------------------------------------------------------------------
cp "$B" "$W/b_tier.md"; ld="$(tamper "$B" "$W/b_tier.md" "TIER 2" "TIER TWO" 1)"
run "9 brief without TIER 2" 7 "$L" "$W/b_tier.md" "$P" "" check "$ld"
cp "$P" "$W/p_tier.txt"; ld="$(tamper "$P" "$W/p_tier.txt" "TIER 2" "TIER TWO" 1)"
run "9b prompt without TIER 2" 7 "$L" "$B" "$W/p_tier.txt" "" check "$ld"
cp "$P" "$W/p_round.txt"; ld="$(tamper "$P" "$W/p_round.txt" "RE-GATE" "REGATE" 1)"
run "10 prompt without RE-GATE" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"
cp "$B" "$W/b_round.md"; ld="$(tamper "$B" "$W/b_round.md" "ROUND 2" "ROUND TWO" 1)"
run "10b brief without ROUND 2" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"

# ---- prompt clauses ---------------------------------------------------------------------------------------
cp "$P" "$W/p_think.txt"; ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think-hard" 1)"
run "11 prompt without the thinking directive" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
cp "$P" "$W/p_brief.txt"; ld="$(tamper "$P" "$W/p_brief.txt" "/fleet/qa-agent/briefs/2026-09-14_secuura-L7-918r2-924-925-ks926-ks773-ks1046-tier2.md" "/fleet/qa-agent/briefs/OTHER.md" 1)"
run "12 prompt not naming the brief path" 9 "$L" "$B" "$W/p_brief.txt" "" check "$ld"
cp "$P" "$W/p_mail.txt"; ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "POST YOUR VERDICT" 1)"
run "13 prompt without MAIL YOUR VERDICT" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"
cp "$P" "$W/p_push.txt"; ld="$(tamper "$P" "$W/p_push.txt" "NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout" "never push in the checkout" 1)"
run "14 prompt without the never-push line" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"
cp "$P" "$W/p_mem.txt"; ld="$(tamper "$P" "$W/p_mem.txt" "no memory maintenance" "no memory upkeep" 1)"
run "15 prompt without the no-memory line" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"
cp "$P" "$W/p_cred.txt"; ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "never echo a secret" 1)"
run "16 prompt without the credential line" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- the round-1 record guard (exit 19), both arms ------------------------------------------------------------
cp "$B" "$W/b_r1.md"; ld="$(tamper "$B" "$W/b_r1.md" "$R1" "/nonexistent/peter_918_review.md" 1)"
run "17 brief not naming Peter's saved #918 review path" 19 "$L" "$W/b_r1.md" "$P" "" check "$ld"
saw "17 brief not naming Peter's saved #918 review path" "does not name the round-1 record path"
cp "$L" "$W/l_r1.sh"; ld="$(tamper "$L" "$W/l_r1.sh" "R1_918='$R1'" "R1_918='/nonexistent/peter_918_review_5151452193.md'" 1)"
cp "$B" "$W/b_r1b.md"; ld2="$(tamper "$B" "$W/b_r1b.md" "$R1" "/nonexistent/peter_918_review_5151452193.md" 1)"
[ "$ld" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "17b launcher + brief agreeing on a MISSING record path" 19 "$W/l_r1.sh" "$W/b_r1b.md" "$P" "" check "$ld"
saw "17b launcher + brief agreeing on a MISSING record path" "missing or empty"

# ---- the head-SHA-in-both guard (exit 20) -------------------------------------------------------------------
cp "$B" "$W/b_sha.md"; ld="$(tamper "$B" "$W/b_sha.md" "b85f1db24596a5e0ce98fe2b1343d9f515a1a995" "b85f1db24" 1)"
run "18 brief without #924's full head SHA" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"
cp "$P" "$W/p_sha.txt"; ld="$(tamper "$P" "$W/p_sha.txt" "5341b1daed8afe4254e05ef66ef4350fd8220d4f" "5341b1dae" 1)"
run "18b prompt without #925's full head SHA" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"

# ---- the TTY guard (exit 21) and the launch modes with NO claude on PATH -------------------------------------
run "19 headless override launch (stdin from dev-null) -> TTY guard" 21 "$L" "$B" "$P" "" launch-override-headless LANDED
run "19b the SAME override launch under a pty (script) -> override guard" 16 "$L" "$B" "$P" "" launch-override-pty LANDED
cp "$L" "$W/l_notty.sh"; ld="$(tamper "$L" "$W/l_notty.sh" "[ -t 0 ] || { echo \"REFUSING: stdin is not a TTY" "[ -t 0 ] || true || { echo \"REFUSING: stdin is not a TTY" 1)"
run "19c TTY guard neutralised -> headless override launch falls to the override guard" 16 "$W/l_notty.sh" "$B" "$P" "" launch-override-headless "$ld"
run "20 a real launch (nothing installed -> brief missing)" 3 "$L" "" "" "" launch LANDED

# ---- raw-control-byte census on the set + a synthetic positive control ---------------------------------------
n=0; for f in "$L" "$B" "$P" "$G/controls_check.sh" "$G/gen_launcher_L7.py" "$G/merged_sim.py" "$G/redproof.sh"; do c="$(python3 -c "import sys;print(sum(1 for b in open(sys.argv[1],'rb').read() if b<32 and b not in (9,10)))" "$f")"; n=$((n+c)); done
printf '%-78s | %3s | %3s | %s | %s\n' "21 raw control bytes over 7 set files" 0 "$n" LANDED "$([ "$n" = 0 ] && echo ok || { FAILS=$((FAILS+1)); echo FAIL; })"
printf 'abc\0def\n' > "$W/nul.bin"; c="$(python3 -c "import sys;print(sum(1 for b in open(sys.argv[1],'rb').read() if b<32 and b not in (9,10)))" "$W/nul.bin")"
printf '%-78s | %3s | %3s | %s | %s\n' "21b census positive control (a synthetic NUL)" 1 "$c" LANDED "$([ "$c" = 1 ] && echo ok || { FAILS=$((FAILS+1)); echo FAIL; })"

# ---- distinct exit codes ----------------------------------------------------------------------------------
codes="$(/usr/bin/grep -o 'exit [0-9][0-9]*' "$L" | /usr/bin/grep -v 'exit [01]$' | sort -u | wc -l | tr -d ' ')"   # the refusal codes 2..22 (exit 0 = --check pass; the first run counted 'exit 0' and a bare 'exit ' too — redproof.first-run-*.out)
printf '%-78s | %3s | %3s | %s | %s\n' "22 distinct refusal exit codes 2..22 declared in the launcher" 21 "$codes" LANDED "$([ "$codes" = 21 ] && echo ok || { FAILS=$((FAILS+1)); echo FAIL; })"
/bin/bash -n "$L" && echo "  /bin/bash -n launcher: ok" || { echo "  bash -n FAILED"; FAILS=$((FAILS+1)); }

# ---- green again on the pristine set: sha-identical ----------------------------------------------------------
run "23 green --check again (pristine)" 0 "$L" "$B" "$P" "" check LANDED
[ "$(shasum -a 256 "$L" | cut -d' ' -f1)" = "$SHA_L0" ] && [ "$(shasum -a 256 "$B" | cut -d' ' -f1)" = "$SHA_B0" ] && [ "$(shasum -a 256 "$P" | cut -d' ' -f1)" = "$SHA_P0" ] && echo "  pristine launcher/brief/prompt sha-identical after the run" || { echo "  PRISTINE FILES CHANGED"; FAILS=$((FAILS+1)); }
echo "work dir (kept): $W"
echo "redproof: FAILS=$FAILS"
exit $([ "$FAILS" = 0 ] && echo 0 || echo 1)
