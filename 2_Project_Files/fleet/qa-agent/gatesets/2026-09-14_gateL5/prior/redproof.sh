#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_ks764_577_780_799_880_985.sh on SCRATCH COPIES only. Never touches the real dirs
# (the launcher's own ls-remote and GitHub reads are READ verbs; nothing is written outside $G). Green asserted FIRST (cell 0,
# rc 0, 12 guard lines), one red per guard at a DISTINCT exit code, every tamper asserted LANDED (anchor must exist; the new
# marker grep'd >= expected; cmp non-identical to pristine; for removals the removed token grep'd 0), green again LAST on the
# sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL and FAILS=N. Every cell runs under env -i
# with a PATH that has git/python3/grep but NO claude, GH_TOKEN unset, 180 s alarm. The TTY guard (exit 21) is exercised BOTH
# ways: headless (the Bash-tool shape) -> 21; under a pseudo-terminal (python pty.spawn, the pane shape) with overrides set ->
# 16, which proves the guard PASSES a real TTY and the override guard behind it fires. The THREE head pins (exit 6) each fire
# on their own PR; the THREE compare pins (exit 10) each fire on their own assertion; the develop guard's arms are exercised
# against LIVE deltas: pinned to M18 (M18..M19 = #982, three services/auth files, disjoint), to M15 and to M9 (M9..develop carries the ks860 guard file) and to an unknown SHA.
set -u
G="${G:?set G to the gate799 scratch dir}"
L="$G/launch_qa_secuura_ks764_577_780_799_880_985.sh"
B="$G/2026-09-14_secuura-799-880-ks764-577-tier1.md"
P="$G/2026-09-14_secuura-799-880-ks764-577-tier1.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
M9='50b729d69c58474624508ed79d05c520dab22cc6'; M15='1c38077ba2aea5f4c4371c1b68796026dc577764'; M18='8861e62161466c40f08d2b10a30edeb203123993'; M19='6e78961e1d04277ecbdb0537e630afa0bf63b13c'
H799='6da848891924f859179d097d464a7b97c9783a6a'; H880='a704137de38a3055e40ee62adc343c0239f34ea9'; H985='fcd8a01e40d34d6cb4055e7b4fd58b9bb908bbe0'
MRG='e6e25421e98ba8f11153f5fc394fe79fc96549a0'

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 grep head cat shasum wc cut perl cmp sed; do ln -s "$(command -v "$t")" "$BIN/$t"; done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "bash: $(/bin/bash --version | head -1)"
echo "subject launcher: $L (sha256 ${SHA_L0:0:16})"

run() { # name expected launcher brief prompt headvar mode landed
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" head="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA799_BRIEF="$brief" QA799_PROMPT="$prompt" ${head:+QA799_HEAD="$head"} \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "check-880" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA799_BRIEF="$brief" QA799_PROMPT="$prompt" QA799_HEAD_880="$head" \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "check-985" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA799_BRIEF="$brief" QA799_PROMPT="$prompt" QA799_HEAD_985="$head" \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then   # headless (the Bash-tool shape): stdin is /dev/null
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA799_BRIEF="$brief" QA799_PROMPT="$prompt" \
      perl -e 'alarm 180; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-pty" ]; then   # the pane shape: a pseudo-terminal on stdin
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA799_BRIEF="$brief" QA799_PROMPT="$prompt" LCH="$lch" OUT="$W/$name.out" \
      perl -e 'alarm 180; exec @ARGV' python3 -c 'import os,pty,sys; out=open(os.environ["OUT"],"wb"); st=pty.spawn(["bash", os.environ["LCH"]], lambda fd: (lambda d: (out.write(d), d)[1])(os.read(fd,1024))); out.close(); sys.exit(os.waitstatus_to_exitcode(st))'; rc=$?
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
DEVPIN="DEVELOP_SHA='$M19'"

# ---- cell 0: green --check -------------------------------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
/usr/bin/grep -q "all guards pass" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" = "12" ] || { echo "  green output does not list 12 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $M19 (M19 = M18" "$W/0 green --check (scratch brief+prompt).out" || /usr/bin/grep -q "origin develop MOVED $M19 -> .*— disjoint" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the develop-still note and is not a disjoint MOVED note either (develop moved onto a guarded path? re-read)"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt both name all three head SHAs" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the head-SHA line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "develop...#799 = $M18 ahead=12 files=12; develop...#880 = $M18 ahead=4 files=5; #799...#985 = $H799 ahead=1 files=7" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the three-compare line"; FAILS=$((FAILS+1)); }
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$W/0 green --check (scratch brief+prompt).out" | cut -c1-200)"

# ---- the three head pins (exit 6), each on its own PR ----------------------------------------------------
run "1a wrong #799 head (env override) -> 6" 6 "$L" "$B" "$P" "0000000000000000000000000000000000000000" check LANDED
/usr/bin/grep -q "REFUSING: #799 — 0000000000000000000000000000000000000000 is not at" "$W/1a wrong #799 head (env override) -> 6.out" || { echo "  cell 1a did not name #799"; FAILS=$((FAILS+1)); }
run "1b wrong #880 head (env override) -> 6" 6 "$L" "$B" "$P" "1111111111111111111111111111111111111111" check-880 LANDED
/usr/bin/grep -q "REFUSING: #880 — 1111111111111111111111111111111111111111 is not at" "$W/1b wrong #880 head (env override) -> 6.out" || { echo "  cell 1b did not name #880"; FAILS=$((FAILS+1)); }
run "1c wrong #985 head (env override) -> 6" 6 "$L" "$B" "$P" "2222222222222222222222222222222222222222" check-985 LANDED
/usr/bin/grep -q "REFUSING: #985 — 2222222222222222222222222222222222222222 is not at" "$W/1c wrong #985 head (env override) -> 6.out" || { echo "  cell 1c did not name #985"; FAILS=$((FAILS+1)); }
# 1d: #985's head set to #799's head — a REAL SHA that is NOT at #985's branch -> 6 naming #985 (the head loop reads the branch, not the SHA's existence)
run "1d #985 head := #799's head (real SHA, wrong branch) -> 6" 6 "$L" "$B" "$P" "$H799" check-985 LANDED
/usr/bin/grep -q "REFUSING: #985 — $H799 is not at" "$W/1d #985 head := #799's head (real SHA, wrong branch) -> 6.out" || { echo "  cell 1d wrong reason"; FAILS=$((FAILS+1)); }

# ---- the three compare pins (exit 10), each on its own assertion -----------------------------------------
cp "$L" "$W/l_c799.sh"; ld="$(tamper "$L" "$W/l_c799.sh" '"$MERGE_BASE ahead=12 files=12" ]' '"$MERGE_BASE ahead=11 files=12" ]' 1)"
run "2a #799 compare pinned ahead=11 -> live reads ahead=12 -> 10" 10 "$W/l_c799.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "REFUSING: #799 develop...head reads '$M18 ahead=12 files=12'" "$W/2a #799 compare pinned ahead=11 -> live reads ahead=12 -> 10.out" || { echo "  cell 2a wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_c880.sh"; ld="$(tamper "$L" "$W/l_c880.sh" '"$MERGE_BASE ahead=4 files=5" ]' '"$MERGE_BASE ahead=4 files=6" ]' 1)"
run "2b #880 compare pinned files=6 -> live reads files=5 -> 10" 10 "$W/l_c880.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "REFUSING: #880 develop...head reads '$M18 ahead=4 files=5'" "$W/2b #880 compare pinned files=6 -> live reads files=5 -> 10.out" || { echo "  cell 2b wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_c985.sh"; ld="$(tamper "$L" "$W/l_c985.sh" '"$HEAD_799 ahead=1 files=7" ]' '"$MERGE_BASE ahead=1 files=7" ]' 1)"
run "2c #985 stack-parent pinned to M18 -> live merge_base is #799's head -> 10" 10 "$W/l_c985.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "REFUSING: #985 stack-parent compare reads '$H799 ahead=1 files=7'" "$W/2c #985 stack-parent pinned to M18 -> live merge_base is #799's head -> 10.out" || { echo "  cell 2c wrong reason"; FAILS=$((FAILS+1)); }
# 2d: the merge-base var itself moved to the merge commit -> #799's compare reads M18, not MRG -> 10 (the first assertion fires)
cp "$L" "$W/l_mb.sh"; ld="$(tamper "$L" "$W/l_mb.sh" "MERGE_BASE='$M18'" "MERGE_BASE='$MRG'" 1)"
run "2d MERGE_BASE := the merge commit e6e25421e -> compare reads M18 -> 10" 10 "$W/l_mb.sh" "$B" "$P" "" check "$ld"

# ---- the develop pin -------------------------------------------------------------------------------------
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "$DEVPIN" "DEVELOP_SHA='3333333333333333333333333333333333333333'" 1)"
run "3 unknown develop pin -> compare unreadable -> UNJUDGEABLE -> 18" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: UNJUDGEABLE" "$W/3 unknown develop pin -> compare unreadable -> UNJUDGEABLE -> 18.out" || { echo "  cell 3 did not say UNJUDGEABLE"; FAILS=$((FAILS+1)); }
# 3b: pinned to M15 — the LIVE M15..develop delta judged against THIS launcher's thirty guarded paths (the outcome is read, then asserted consistent)
cp "$L" "$W/l_dev15.sh"; ld="$(tamper "$L" "$W/l_dev15.sh" "$DEVPIN" "DEVELOP_SHA='$M15'" 1)"
env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA799_BRIEF="$B" QA799_PROMPT="$P" perl -e 'alarm 180; exec @ARGV' bash "$W/l_dev15.sh" --check >"$W/3b.probe.out" 2>&1 </dev/null; rc15=$?
if [ "$rc15" = "0" ]; then
  run "3b pinned to M15: live M15..M18 delta DISJOINT from the thirty paths -> 0 (MOVED note)" 0 "$W/l_dev15.sh" "$B" "$P" "" check "$ld"
  /usr/bin/grep -q "origin develop MOVED $M15 -> .*: commits=" "$W/3b pinned to M15: live M15..M18 delta DISJOINT from the thirty paths -> 0 (MOVED note).out" || { echo "  cell 3b did not report MOVED"; FAILS=$((FAILS+1)); }
  echo "  cell 3b note: $(/usr/bin/grep -o 'origin develop MOVED [^—]*' "$W/3b pinned to M15: live M15..M18 delta DISJOINT from the thirty paths -> 0 (MOVED note).out" | head -1 | cut -c1-160)"
else
  run "3b pinned to M15: live M15..M18 delta hits a guarded path -> 18 (GUARDED named)" 18 "$W/l_dev15.sh" "$B" "$P" "" check "$ld"
  echo "  cell 3b: $(/usr/bin/grep -o 'GUARDED [^—]*' "$W/3b pinned to M15: live M15..M18 delta hits a guarded path -> 18 (GUARDED named).out" | head -1 | cut -c1-240)"
fi
# 3c: pinned to M9 — the LIVE M9..M18 delta carries the ks860 guard file (the #984 set measured it) -> GUARDED naming it -> 18
cp "$L" "$W/l_dev9.sh"; ld="$(tamper "$L" "$W/l_dev9.sh" "$DEVPIN" "DEVELOP_SHA='$M9'" 1)"
run "3c pinned to M9: live delta hits the ks860 guard file (+ others) -> 18" 18 "$W/l_dev9.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED .*ks860-test-listeners-bind-loopback.test.ts" "$W/3c pinned to M9: live delta hits the ks860 guard file (+ others) -> 18.out" || { echo "  cell 3c did not name the ks860 guard among the hits"; FAILS=$((FAILS+1)); }
echo "  cell 3c: $(/usr/bin/grep -o 'GUARDED [^—]*' "$W/3c pinned to M9: live delta hits the ks860 guard file (+ others) -> 18.out" | head -1 | cut -c1-300)"
# 3d: the ks860 entry neutralised in the M9 launcher -> the guard must STILL fire if any other guarded path moved in M9..M18 (read and assert consistent with 3c's hit list)
cp "$W/l_dev9.sh" "$W/l_dev9nn.sh"; ld="$(tamper "$W/l_dev9.sh" "$W/l_dev9nn.sh" '"Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",' '"Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts.NOT-GUARDED",' 1)"
hits3c="$(/usr/bin/grep -o 'GUARDED [^—]*' "$W/3c pinned to M9: live delta hits the ks860 guard file (+ others) -> 18.out" | head -1 | sed 's/^GUARDED //')"
nhits="$(printf '%s\n' "$hits3c" | tr ' ' '\n' | /usr/bin/grep -c .)"
if [ "$nhits" -gt 1 ]; then
  run "3d M9 pin, ks860 entry neutralised: the OTHER M9..M18 hits still fire -> 18" 18 "$W/l_dev9nn.sh" "$B" "$P" "" check "$ld"
  /usr/bin/grep -q "GUARDED " "$W/3d M9 pin, ks860 entry neutralised: the OTHER M9..M18 hits still fire -> 18.out" && ! /usr/bin/grep -q "GUARDED .*ks860-test-listeners-bind-loopback.test.ts\b" "$W/3d M9 pin, ks860 entry neutralised: the OTHER M9..M18 hits still fire -> 18.out" || { echo "  cell 3d: ks860 still named or no GUARDED"; FAILS=$((FAILS+1)); }
else
  run "3d M9 pin, ks860 entry neutralised: the lone hit gone -> 0 (MOVED note)" 0 "$W/l_dev9nn.sh" "$B" "$P" "" check "$ld"
fi
# 3e: pinned to M18 — the LIVE M18..M19 delta (#982's squash, three services/auth files) -> DISJOINT -> 0 (the move this set lived through at 08:5x AEST)
cp "$L" "$W/l_dev18.sh"; ld="$(tamper "$L" "$W/l_dev18.sh" "$DEVPIN" "DEVELOP_SHA='$M18'" 1)"
run "3e pinned to M18: the live M18..M19 delta (#982, three auth files) DISJOINT -> 0" 0 "$W/l_dev18.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "origin develop MOVED $M18 -> $M19: commits=1 files=3" "$W/3e pinned to M18: the live M18..M19 delta (#982, three auth files) DISJOINT -> 0.out" || { echo "  cell 3e did not report MOVED commits=1 files=3 (develop moved again? re-read)"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_env.sh"; ld="$(tamper "$L" "$W/l_env.sh" "4_Credentials/.env'" "4_Credentials/.env.does-not-exist'" 1)"
run "4 env file missing -> compare API unreadable -> 13" 13 "$W/l_env.sh" "$B" "$P" "" check "$ld"

# ---- files present ---------------------------------------------------------------------------------------
: > "$W/empty.md"; [ ! -s "$W/empty.md" ] && le=LANDED || le=NOT-LANDED
run "5 empty brief" 3 "$L" "$W/empty.md" "$P" "" check "$le"
run "6 empty prompt" 4 "$L" "$B" "$W/empty.md" "" check "$le"
cp "$L" "$W/l_qadir.sh"; ld="$(tamper "$L" "$W/l_qadir.sh" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/does-not-exist'" 1)"
run "7 QA project dir missing (launcher tamper)" 2 "$W/l_qadir.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_repo.sh"; ld="$(tamper "$L" "$W/l_repo.sh" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/does-not-exist'" 1)"
run "8 repo dir missing (launcher tamper)" 5 "$W/l_repo.sh" "$B" "$P" "" check "$ld"

# ---- brief/prompt agreement -------------------------------------------------------------------------------
ld="$(tamper "$B" "$W/b_tier.md" "TIER 1" "TIER 3" 1)"
run "9 brief says TIER 3 everywhere (brief tamper)" 7 "$L" "$W/b_tier.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_tier.txt" "TIER 1" "TIER 3" 1)"
run "10 prompt says TIER 3 everywhere (prompt tamper)" 7 "$L" "$B" "$W/p_tier.txt" "" check "$ld"
ld="$(tamper "$B" "$W/b_round.md" "ROUND 1" "ROUND 3" 1)"
run "11 brief says ROUND 3 (brief tamper)" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_round.txt" "ROUND 1" "ROUND 3" 1)"
run "12 prompt says ROUND 3 (prompt tamper)" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"

# ---- prompt clauses ---------------------------------------------------------------------------------------
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard" 1)"
run "13 prompt lacks ultrathink first line" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_path.txt" "/briefs/2026-09-14_secuura-799-880-ks764-577-tier1.md" "/briefs/2026-09-14_secuura-OTHER-tier1.md" 1)"
run "14 prompt lacks the real brief path" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "SEND YOUR VERDICT" 1)"
run "15 prompt lacks MAIL YOUR VERDICT" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_push.txt" "or preflight.sh inside the Secuura checkout" "or preflight.sh within the Secuura checkout" 1)"
run "16 prompt lacks the NEVER-push line" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mem.txt" "Do no memory maintenance" "Do no memory upkeep" 1)"
run "17 prompt lacks no-memory-maintenance" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "NEVER print a secret value" 1)"
run "18 prompt lacks NEVER-print-a-credential" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- the head-SHA-in-both guard (exit 20), each of the three SHAs, both files ------------------------------
ld="$(tamper "$P" "$W/p_sha799.txt" "$H799" "6da848891" 1)"
run "20a prompt lacks the full #799 SHA -> 20" 20 "$L" "$B" "$W/p_sha799.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA $H799" "$W/20a prompt lacks the full #799 SHA -> 20.out" || { echo "  cell 20a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha880.md" "$H880" "a704137de" 1)"
run "20b brief lacks the full #880 SHA -> 20" 20 "$L" "$W/b_sha880.md" "$P" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA $H880" "$W/20b brief lacks the full #880 SHA -> 20.out" || { echo "  cell 20b wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$P" "$W/p_sha985.txt" "$H985" "fcd8a01e4" 1)"
run "20c prompt lacks the full #985 SHA -> 20" 20 "$L" "$B" "$W/p_sha985.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA $H985" "$W/20c prompt lacks the full #985 SHA -> 20.out" || { echo "  cell 20c wrong reason"; FAILS=$((FAILS+1)); }

# ---- launch modes with NO claude on PATH -------------------------------------------------------------------
run "21 override launch, HEADLESS (stdin dev-null) -> the TTY guard, 21" 21 "$L" "$B" "$P" "" launch-override LANDED
/usr/bin/grep -q "stdin is not a TTY" "$W/21 override launch, HEADLESS (stdin dev-null) -> the TTY guard, 21.out" || { echo "  cell 21 wrong reason"; FAILS=$((FAILS+1)); }
run "21b override launch under a PTY -> the TTY guard passes, the override guard fires, 16" 16 "$L" "$B" "$P" "" launch-override-pty LANDED
/usr/bin/grep -q "a launch with test overrides set" "$W/21b override launch under a PTY -> the TTY guard passes, the override guard fires, 16.out" || { echo "  cell 21b wrong reason (did the pty reach the override guard?)"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_notty.sh"; ld="$(tamper "$L" "$W/l_notty.sh" '[ -t 0 ] || {' '[ -t 0 ] || true || {' 1)"
run "21c TTY guard neutralised, headless override launch -> the override guard, 16 (the guard was what stood between a Bash tool and the exec)" 16 "$W/l_notty.sh" "$B" "$P" "" launch-override "$ld"
run "22 real launch (not installed yet), headless, no claude -> 3" 3 "$L" "$B" "$P" "" launch-real LANDED
/usr/bin/grep -q "brief missing or empty: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-799-880-ks764-577-tier1.md" "$W/22 real launch (not installed yet), headless, no claude -> 3.out" \
  || { echo "  cell 22 did not refuse on the REAL brief path"; FAILS=$((FAILS+1)); }

# ---- raw-control-byte census on the whole set + a synthetic positive control ---------------------------------
python3 - "$L" "$B" "$P" "$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_799.py" "$G/guards_sim.py" "$G/gh_read.py" "$G/linear_read.py" "$G/linear_titles.py" <<'PY' || FAILS=$((FAILS+1))
import sys
bad=0
for p in sys.argv[1:]:
    b=open(p,'rb').read()
    off=[i for i,x in enumerate(b) if (x<0x20 and x not in (9,10,13)) or x==0x7f]
    print(f"  raw-control-byte census {p.split('/')[-1]}: {len(off)}")
    bad+=len(off)
ctrl=b"const bad = 'doc\x00bad';\n"
c=[i for i,x in enumerate(ctrl) if (x<0x20 and x not in (9,10,13)) or x==0x7f]
print(f"  positive control (synthetic NUL): offsets {c}")
sys.exit(0 if bad==0 and c==[16] else 1)
PY

# ---- distinct exit codes exercised -------------------------------------------------------------------------
echo "  exit codes declared in the launcher (distinct): $(/usr/bin/grep -h -o 'exit [0-9][0-9]*' "$L" | sort -u | tr '\n' ' ')"
/bin/bash -n "$L" && echo "  /bin/bash -n launcher: ok" || { echo "  /bin/bash -n launcher: FAIL"; FAILS=$((FAILS+1)); }

# ---- green again on the pristine set: sha-identical ----------------------------------------------------------
SHA_L1="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B1="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P1="$(shasum -a 256 "$P" | cut -d' ' -f1)"
if [ "$SHA_L0" = "$SHA_L1" ] && [ "$SHA_B0" = "$SHA_B1" ] && [ "$SHA_P0" = "$SHA_P1" ]; then id=LANDED; else id=NOT-LANDED; fi
run "23 green again (pristine sha-identical)" 0 "$L" "$B" "$P" "" check "$id"

echo "pristine sha256: launcher ${SHA_L1:0:16} brief ${SHA_B1:0:16} prompt ${SHA_P1:0:16}"
echo "work dir (kept, never rm'd): $W"
echo "FAILS=$FAILS"
exit "$FAILS"
