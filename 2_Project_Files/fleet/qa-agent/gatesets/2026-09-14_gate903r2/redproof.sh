#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_ks991_903_r2.sh on SCRATCH COPIES only. Never touches the real dirs.
# Green asserted FIRST (cell 0, rc 0, 13 guard lines), one red per guard at a DISTINCT exit code, every tamper asserted LANDED
# (anchor must exist; the new marker grep'd >= expected; cmp non-identical to pristine; for removals the removed token grep'd 0),
# green again LAST on the sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL and FAILS=N.
# Every cell runs under env -i with a PATH that has git/python3/grep but NO claude, GH_TOKEN unset, 120 s alarm.
# The develop guard's arms are exercised against the LIVE M15..M18 delta (6 files; TWO under Blockchain/Dev/scripts/__tests__/ —
# docker_build_empty_table.test.sh and ks949_main_seed_idempotence.test.sh — none = #903's files, none = deps-present.sh or
# run-shell-suites.sh): the shipped list must read GUARDED (18) when pinned at M15 (the PREFIX arm on both new suites, named);
# pinned at M17 (M17..M18 = the corpus test under packages/shared/, NOT guarded here) it must read MOVED/disjoint (0); pinned at
# M16 (M16..M18 = docker-build.sh + docker_build_empty_table.test.sh + the corpus test) the PREFIX arm fires on the one suite (18);
# M16 with the prefix neutralised → disjoint (0) — proving the prefix is what fired; M16 with the prefix neutralised AND the
# run-shell-suites slot aimed at docker-build.sh → the EXACT arm fires (18); an unknown develop sha → UNJUDGEABLE (18).
# The round-1 record guard (exit 19), both arms: the brief copy without the path → 19 ("does not name"); the launcher and a brief
# copy agreeing on a path that does not exist → 19 ("missing or empty").
# The TTY guard (exit 21): the launch path under env -i with stdin from /dev/null → 21; the SAME launch under a pty (`script`) with
# test overrides set → 16 (the override guard, one line later) — so 21 is proven to fire on a headless launch and NOT on a pty;
# the guard neutralised → a headless override launch falls through to 16.
set -u
G="${G:?set G to the gate903r2 scratch dir}"
L="$G/launch_qa_secuura_ks991_903_r2.sh"
B="$G/2026-09-14_secuura-903-ks991-tier2-r2.md"
P="$G/2026-09-14_secuura-903-ks991-tier2-r2.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
M15='1c38077ba2aea5f4c4371c1b68796026dc577764'; M16='818002259820e30817b5b5e26f91d23d8761d21b'; M17='a4ef481c897265ae01936ad10d84d547d95557d2'; M18='8861e62161466c40f08d2b10a30edeb203123993'
R1='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/peter_903_comment_5585854866.md'

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 grep head cat shasum wc cut perl cmp script sed; do ln -s "$(command -v "$t")" "$BIN/$t"; done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "bash: $(/bin/bash --version | head -1)"

run() { # name expected launcher brief prompt headvar mode landed
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" head="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA903R2_BRIEF="$brief" QA903R2_PROMPT="$prompt" ${head:+QA903R2_HEAD="$head"} \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-headless" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA903R2_BRIEF="$brief" QA903R2_PROMPT="$prompt" \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-pty" ]; then
    # a pseudo-terminal on stdin via script(1): the TTY guard must NOT fire; the override guard (16) must.
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA903R2_BRIEF="$brief" QA903R2_PROMPT="$prompt" \
      script -q "$W/$name.typescript" perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  else
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  fi
  local ok="ok"; [ "$rc" = "$exp" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  [ "$landed" = "LANDED" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  printf '%-70s | %3s | %3s | %s | %s\n' "$name" "$exp" "$rc" "$landed" "$ok"
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
DEVPIN="DEVELOP_SHA='$M18'"

# ---- cell 0: green --check -------------------------------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
/usr/bin/grep -q "all guards pass" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" = "13" ] || { echo "  green output does not list 13 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $M18 (M18" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the develop-still note"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt both name the head SHA a4f71cde660c1442d98317e26d93845340b20098" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the head-SHA line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief names the round-1 record (Peter's review) and it is present on disk" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the round-1 record line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "will refuse unless stdin is a TTY (exit 21)" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the TTY line"; FAILS=$((FAILS+1)); }
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$W/0 green --check (scratch brief+prompt).out" | cut -c1-160)"

# ---- head / develop / merge-base --------------------------------------------------------------------------
run "1 wrong head sha (env override)" 6 "$L" "$B" "$P" "0000000000000000000000000000000000000000" check LANDED
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "$DEVPIN" "DEVELOP_SHA='1111111111111111111111111111111111111111'" 1)"
run "2 unknown develop sha -> unjudgeable delta" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: UNJUDGEABLE" "$W/2 unknown develop sha -> unjudgeable delta.out" || { echo "  cell 2 did not say UNJUDGEABLE"; FAILS=$((FAILS+1)); }
# 2b: pinned to M15 with the SHIPPED list — the LIVE M15..M18 delta (6 files) carries TWO new suites under scripts/__tests__/ -> the
#     PREFIX arm fires -> 18, naming exactly those two (sorted).
cp "$L" "$W/l_dev15.sh"; ld="$(tamper "$L" "$W/l_dev15.sh" "$DEVPIN" "DEVELOP_SHA='$M15'" 1)"
run "2b pinned to M15, shipped list: prefix arm on the two new suites -> 18" 18 "$W/l_dev15.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: GUARDED Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh " "$W/2b pinned to M15, shipped list: prefix arm on the two new suites -> 18.out" || { echo "  cell 2b did not name exactly the two new suites as the guarded hits"; FAILS=$((FAILS+1)); }
echo "  cell 2b: $(/usr/bin/grep -o 'GUARDED [^—]*' "$W/2b pinned to M15, shipped list: prefix arm on the two new suites -> 18.out" | head -1 | cut -c1-200)"
# 2c: pinned to M17 with the SHIPPED list — M17..M18 = the corpus test under packages/shared/ (NOT guarded here) -> MOVED/disjoint -> 0.
cp "$L" "$W/l_dev17.sh"; ld="$(tamper "$L" "$W/l_dev17.sh" "$DEVPIN" "DEVELOP_SHA='$M17'" 1)"
run "2c pinned to M17, shipped list: corpus-test-only delta disjoint -> 0" 0 "$W/l_dev17.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "origin develop MOVED $M17 -> $M18: commits=1 files=1 — disjoint from the guard's six paths" "$W/2c pinned to M17, shipped list: corpus-test-only delta disjoint -> 0.out" || { echo "  cell 2c did not report MOVED … commits=1 files=1 — disjoint"; FAILS=$((FAILS+1)); }
echo "  cell 2c note: $(/usr/bin/grep 'origin develop MOVED' "$W/2c pinned to M17, shipped list: corpus-test-only delta disjoint -> 0.out" | cut -c1-150)"
# 2d: pinned to M16 — M16..M18 = docker-build.sh + docker_build_empty_table.test.sh + the corpus test -> the PREFIX arm on the one suite -> 18.
cp "$L" "$W/l_dev16.sh"; ld="$(tamper "$L" "$W/l_dev16.sh" "$DEVPIN" "DEVELOP_SHA='$M16'" 1)"
run "2d pinned to M16, shipped list: prefix arm on docker_build_empty_table -> 18" 18 "$W/l_dev16.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh " "$W/2d pinned to M16, shipped list: prefix arm on docker_build_empty_table -> 18.out" || { echo "  cell 2d did not name docker_build_empty_table.test.sh"; FAILS=$((FAILS+1)); }
# 2e: M16 pin with the PREFIX entry neutralised -> no exact entry matches -> disjoint -> 0 (commits=2 files=3): the prefix was what fired in 2d.
cp "$W/l_dev16.sh" "$W/l_dev16np.sh"; ld="$(tamper "$W/l_dev16.sh" "$W/l_dev16np.sh" '"Blockchain/Dev/scripts/__tests__/"]' '"Blockchain/Dev/scripts/__tests__-NOT-GUARDED/"]' 1)"
run "2e M16 pin, prefix neutralised: 3-file delta disjoint -> 0" 0 "$W/l_dev16np.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "commits=2 files=3 — disjoint" "$W/2e M16 pin, prefix neutralised: 3-file delta disjoint -> 0.out" || { echo "  cell 2e did not report commits=2 files=3 — disjoint"; FAILS=$((FAILS+1)); }
# 2f: M16 pin, prefix neutralised, the run-shell-suites slot AIMED at docker-build.sh (a file M16..M18 moved) -> the EXACT arm fires -> 18.
cp "$W/l_dev16np.sh" "$W/l_dev16aim.sh"; ld="$(tamper "$W/l_dev16np.sh" "$W/l_dev16aim.sh" '"Blockchain/Dev/scripts/run-shell-suites.sh",' '"Blockchain/Dev/scripts/docker-build.sh",' 1)"
run "2f M16 pin, prefix neutralised, slot aimed at docker-build.sh -> EXACT arm -> 18" 18 "$W/l_dev16aim.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED Blockchain/Dev/scripts/docker-build.sh " "$W/2f M16 pin, prefix neutralised, slot aimed at docker-build.sh -> EXACT arm -> 18.out" || { echo "  cell 2f did not name docker-build.sh"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_mb.sh"; ld="$(tamper "$L" "$W/l_mb.sh" "MERGE_BASE='$M18'" "MERGE_BASE='2222222222222222222222222222222222222222'" 1)"
run "3 wrong merge-base (launcher tamper)" 10 "$W/l_mb.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_env.sh"; ld="$(tamper "$L" "$W/l_env.sh" "4_Credentials/.env'" "4_Credentials/.env.does-not-exist'" 1)"
run "4 env file missing -> compare API unreadable" 13 "$W/l_env.sh" "$B" "$P" "" check "$ld"

# ---- files present ---------------------------------------------------------------------------------------
: > "$W/empty.md"; [ ! -s "$W/empty.md" ] && le=LANDED || le=NOT-LANDED
run "5 empty brief" 3 "$L" "$W/empty.md" "$P" "" check "$le"
run "6 empty prompt" 4 "$L" "$B" "$W/empty.md" "" check "$le"
cp "$L" "$W/l_qadir.sh"; ld="$(tamper "$L" "$W/l_qadir.sh" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN'" "QA_DIR='/Volumes/DevMASTER/!CODING/Testing Agent MAIN/does-not-exist'" 1)"
run "7 QA project dir missing (launcher tamper)" 2 "$W/l_qadir.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_repo.sh"; ld="$(tamper "$L" "$W/l_repo.sh" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files'" "REPO='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/does-not-exist'" 1)"
run "8 repo dir missing (launcher tamper)" 5 "$W/l_repo.sh" "$B" "$P" "" check "$ld"

# ---- brief/prompt agreement -------------------------------------------------------------------------------
ld="$(tamper "$B" "$W/b_tier.md" "TIER 2" "TIER 3" 1)"
run "9 brief says TIER 3 (brief tamper)" 7 "$L" "$W/b_tier.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_tier.txt" "TIER 2" "TIER 3" 1)"
run "10 prompt says TIER 3 (prompt tamper)" 7 "$L" "$B" "$W/p_tier.txt" "" check "$ld"
ld="$(tamper "$B" "$W/b_round.md" "ROUND 2" "ROUND 3" 1)"
run "11 brief says ROUND 3 (brief tamper)" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_round.txt" "ROUND 2" "ROUND 3" 1)"
run "12 prompt says ROUND 3 (prompt tamper)" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"

# ---- prompt clauses ---------------------------------------------------------------------------------------
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard" 1)"
run "13 prompt lacks ultrathink first line" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_path.txt" "/briefs/2026-09-14_secuura-903-ks991-tier2-r2.md" "/briefs/2026-09-14_secuura-OTHER-tier2-r2.md" 1)"
run "14 prompt lacks the real brief path" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "SEND YOUR VERDICT" 1)"
run "15 prompt lacks MAIL YOUR VERDICT" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_push.txt" "or preflight.sh inside the Secuura checkout" "or preflight.sh within the Secuura checkout" 1)"
run "16 prompt lacks the NEVER-push line" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mem.txt" "Do no memory maintenance" "Do no memory upkeep" 1)"
run "17 prompt lacks no-memory-maintenance" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "NEVER print a secret value" 1)"
run "18 prompt lacks NEVER-print-a-credential" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- the round-1 record guard (exit 19), both arms ------------------------------------------------------------
ld="$(tamper "$B" "$W/b_r1.md" "$R1" "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s213/boot/SOMEWHERE-ELSE.md" 1)"
run "19a brief lacks the round-1 record path (exit 19, first arm)" 19 "$L" "$W/b_r1.md" "$P" "" check "$ld"
/usr/bin/grep -q "does not name the round-1 record path" "$W/19a brief lacks the round-1 record path (exit 19, first arm).out" || { echo "  cell 19a wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_r1.sh"; ld="$(tamper "$L" "$W/l_r1.sh" "R1_REPORT='$R1'" "R1_REPORT='$R1.does-not-exist'" 1)"
ld2="$(tamper "$B" "$W/b_r1b.md" "$R1" "$R1.does-not-exist" 1)"; [ "$ld" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "19b launcher+brief name a MISSING record (exit 19, second arm)" 19 "$W/l_r1.sh" "$W/b_r1b.md" "$P" "" check "$ld"
/usr/bin/grep -q "missing or empty" "$W/19b launcher+brief name a MISSING record (exit 19, second arm).out" || { echo "  cell 19b wrong reason"; FAILS=$((FAILS+1)); }

# ---- the head-SHA-in-both guard (exit 20), both arms -------------------------------------------------------
ld="$(tamper "$P" "$W/p_sha.txt" "a4f71cde660c1442d98317e26d93845340b20098" "a4f71cde6" 1)"
run "20a prompt lacks the full head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA" "$W/20a prompt lacks the full head SHA (exit 20).out" || { echo "  cell 20a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha.md" "a4f71cde660c1442d98317e26d93845340b20098" "a4f71cde6" 1)"
run "20b brief lacks the full head SHA (exit 20)" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"

# ---- the TTY guard (exit 21) and the launch modes with NO claude on PATH -------------------------------------
run "21a override launch, HEADLESS (stdin closed) -> TTY guard" 21 "$L" "$B" "$P" "" launch-override-headless LANDED
/usr/bin/grep -q "stdin is not a TTY" "$W/21a override launch, HEADLESS (stdin closed) -> TTY guard.out" || { echo "  cell 21a wrong reason"; FAILS=$((FAILS+1)); }
run "21b override launch under a PTY -> the override guard (16), not 21" 16 "$L" "$B" "$P" "" launch-override-pty LANDED
/usr/bin/grep -q "a launch with test overrides set" "$W/21b override launch under a PTY -> the override guard (16), not 21.out" || { echo "  cell 21b wrong reason (TTY guard fired under a pty?)"; FAILS=$((FAILS+1)); }
run "22 real launch (not installed yet), no claude, headless" 3 "$L" "$B" "$P" "" launch-real LANDED
/usr/bin/grep -q "brief missing or empty: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-903-ks991-tier2-r2.md" "$W/22 real launch (not installed yet), no claude, headless.out" \
  || { echo "  cell 22 did not refuse on the REAL brief path"; FAILS=$((FAILS+1)); }
# 21c: the TTY guard REMOVED from a scratch launcher -> a headless override launch falls through to the override guard (16).
cp "$L" "$W/l_notty.sh"; ld="$(tamper "$L" "$W/l_notty.sh" '[ -t 0 ] || ' '[ -t 0 ] && true || true || ' 1)"
run "21c TTY guard neutralised (launcher tamper): headless -> 16" 16 "$W/l_notty.sh" "$B" "$P" "" launch-override-headless "$ld"

# ---- raw-control-byte census on the whole set + a synthetic positive control ---------------------------------
python3 - "$L" "$B" "$P" "$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_903r2.py" "$G/guards_sim.py" "$G/gh_read.py" "$G/ci_control_read.py" "$G/linear_read.py" "$G/linear_search.py" "$G/probe_neq.sh" "$G/probe_div.sh" <<'PY' || FAILS=$((FAILS+1))
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
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
exit "$FAILS"
