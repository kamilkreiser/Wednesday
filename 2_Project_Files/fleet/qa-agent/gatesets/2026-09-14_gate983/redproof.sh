#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_ks823_983.sh on SCRATCH COPIES only. Never touches the real dirs.
# Green asserted FIRST (cell 0, rc 0, 12 guard lines), one red per guard at a DISTINCT exit code, every tamper asserted
# LANDED (anchor must exist; the new marker grep'd >= expected; cmp non-identical to pristine; for removals the removed
# token grep'd 0), green again LAST on the sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL
# and FAILS=N. Every cell runs under env -i with a PATH that has git/python3/grep but NO claude, GH_TOKEN unset, 120 s alarm.
# The develop guard's arms are exercised against the LIVE deltas to M18 (probed 07:4x AEST, devpins_probe.out): M15..M18 =
# 3 commits / 6 files incl. ONE under services/auth/ (the ks949 seed-identity test) and NOT the ks860 guard file; M12..M18 =
# 6 commits / 9 files incl. the ks860 guard file AND that auth test. So: the shipped list pinned at M15 reads GUARDED (18) by
# the PREFIX arm; M15 with the prefix neutralised reads MOVED/disjoint (0); M12 with the prefix neutralised reads GUARDED by
# the EXACT ks860 entry alone (18); M12 with the prefix AND the ks860 entry neutralised reads disjoint (0, the control); M15
# with the prefix neutralised and the api-gateway auth.ts slot AIMED at startup-migrations.ts (in the delta) reads 18 (the
# exact arm works for another slot). The stack-parent guard (21) and the no-TTY guard (22) are each fired once; the TTY pass
# path is driven under `script` with claude ABSENT from PATH, so it reaches the exec line and dies 127 (command not found).
set -u
G="${G:?set G to the gate983 scratch dir}"
L="$G/launch_qa_secuura_ks823_983.sh"
B="$G/2026-09-14_secuura-983-ks823-tier1.md"
P="$G/2026-09-14_secuura-983-ks823-tier1.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
M18='8861e62161466c40f08d2b10a30edeb203123993'; M15='1c38077ba2aea5f4c4371c1b68796026dc577764'; M12='3fc158c3975b71654f71d67a89913dc6c98bf08b'
HEAD='f62c975c11ec97cdef04500fd98a43618e702763'; PARENT='e62eab87a6263e25c41c9bb814d5831842bb6c7e'

BIN="$W/bin"; mkdir -p "$BIN"
for t in git python3 grep head cat shasum wc cut perl cmp script; do ln -s "$(command -v "$t")" "$BIN/$t"; done
NOCLAUDE_PATH="$BIN:/usr/bin:/bin"
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v claude' >/dev/null 2>&1 && { echo "claude IS on the restricted PATH — abort"; exit 99; }
env -i PATH="$NOCLAUDE_PATH" bash -c 'command -v git' >/dev/null 2>&1 || { echo "git is NOT on the restricted PATH — abort (positive control)"; exit 99; }
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
echo "bash: $(/bin/bash --version | head -1)"

run() { # name expected launcher brief prompt headvar mode landed
  local name="$1" exp="$2" lch="$3" brief="$4" prompt="$5" head="$6" mode="$7" landed="$8" rc
  if [ "$mode" = "check" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA983_BRIEF="$brief" QA983_PROMPT="$prompt" ${head:+QA983_HEAD="$head"} \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA983_BRIEF="$brief" QA983_PROMPT="$prompt" \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-notty" ]; then
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-tty" ]; then
    # `script` gives the child a pty: [ -t 0 ] is true; claude is absent, so bash's exec fails with 127.
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" TERM=dumb \
      perl -e 'alarm 120; exec @ARGV' script -q "$W/$name.typescript" bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  else
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  fi
  local ok="ok"; [ "$rc" = "$exp" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  [ "$landed" = "LANDED" ] || { ok="FAIL"; FAILS=$((FAILS+1)); }
  printf '%-66s | %3s | %3s | %s | %s\n' "$name" "$exp" "$rc" "$landed" "$ok"
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
PREFIX='"Blockchain/Dev/services/auth/",'
KS860='"Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts",'
GWAUTH='"Blockchain/Dev/services/api-gateway/src/middleware/auth.ts",'

# ---- cell 0: green --check -------------------------------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
/usr/bin/grep -q "all guards pass" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" = "12" ] || { echo "  green output does not list 12 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $M18 (M18" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the develop note"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "stack parent refs/pull/982/head still $PARENT" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the stack-parent line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt both name the head SHA $HEAD" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the head-SHA line"; FAILS=$((FAILS+1)); }
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$W/0 green --check (scratch brief+prompt).out" | cut -c1-140)"

# ---- head / parent / develop / merge-base ---------------------------------------------------------------
run "1 wrong head sha (env override)" 6 "$L" "$B" "$P" "0000000000000000000000000000000000000000" check LANDED
cp "$L" "$W/l_par.sh"; ld="$(tamper "$L" "$W/l_par.sh" "STACK_PARENT='$PARENT'" "STACK_PARENT='3333333333333333333333333333333333333333'" 1)"
run "21 stack parent moved (launcher tamper) -> 21" 21 "$W/l_par.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "the stack parent refs/pull/982/head is no longer 3333333333333333333333333333333333333333" "$W/21 stack parent moved (launcher tamper) -> 21.out" || { echo "  cell 21 wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "$DEVPIN" "DEVELOP_SHA='1111111111111111111111111111111111111111'" 1)"
run "2 unknown develop sha -> unjudgeable delta" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: UNJUDGEABLE" "$W/2 unknown develop sha -> unjudgeable delta.out" || { echo "  cell 2 did not say UNJUDGEABLE"; FAILS=$((FAILS+1)); }
# 2b: pinned to M15 with the SHIPPED list — the live M15..M18 delta (6 files) carries ONE file under services/auth/ -> the PREFIX arm -> 18.
cp "$L" "$W/l_dev15.sh"; ld="$(tamper "$L" "$W/l_dev15.sh" "$DEVPIN" "DEVELOP_SHA='$M15'" 1)"
run "2b pinned to M15, shipped list: prefix arm on the ks949 auth test -> 18" 18 "$W/l_dev15.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: GUARDED Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts " "$W/2b pinned to M15, shipped list: prefix arm on the ks949 auth test -> 18.out" || { echo "  cell 2b did not name the ks949 auth test as the (only) guarded hit"; FAILS=$((FAILS+1)); }
echo "  cell 2b: $(/usr/bin/grep -o 'GUARDED [^—]*' "$W/2b pinned to M15, shipped list: prefix arm on the ks949 auth test -> 18.out" | head -1 | cut -c1-160)"
# 2c: pinned to M15 with the PREFIX entry neutralised — nothing else in M15..M18 is guarded -> MOVED/disjoint -> 0.
cp "$W/l_dev15.sh" "$W/l_dev15np.sh"; ld="$(tamper "$W/l_dev15.sh" "$W/l_dev15np.sh" "$PREFIX" '"Blockchain/Dev/services/auth-NOT-GUARDED/",' 1)"
run "2c M15 pin, prefix neutralised: 6-file delta disjoint -> 0" 0 "$W/l_dev15np.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "origin develop MOVED $M15 -> $M18: commits=3 files=6 — disjoint from the guard's five paths" "$W/2c M15 pin, prefix neutralised: 6-file delta disjoint -> 0.out" || { echo "  cell 2c did not report MOVED … commits=3 files=6 — disjoint"; FAILS=$((FAILS+1)); }
echo "  cell 2c note: $(/usr/bin/grep 'origin develop MOVED' "$W/2c M15 pin, prefix neutralised: 6-file delta disjoint -> 0.out" | cut -c1-150)"
# 2d: pinned to M12 with the PREFIX neutralised — M12..M18 carries the ks860 guard file -> the EXACT arm alone -> 18.
cp "$W/l_dev15np.sh" "$W/l_dev12np.sh"; ld="$(tamper "$W/l_dev15np.sh" "$W/l_dev12np.sh" "DEVELOP_SHA='$M15'" "DEVELOP_SHA='$M12'" 1)"
run "2d M12 pin, prefix neutralised: EXACT arm on the ks860 guard file -> 18" 18 "$W/l_dev12np.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: GUARDED Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts " "$W/2d M12 pin, prefix neutralised: EXACT arm on the ks860 guard file -> 18.out" || { echo "  cell 2d did not name the ks860 guard file as the ONLY guarded hit"; FAILS=$((FAILS+1)); }
# 2e: M12 pin, prefix AND ks860 entries neutralised -> the 9-file delta is disjoint -> 0 (the control that the ks860 entry alone made 2d red).
cp "$W/l_dev12np.sh" "$W/l_dev12nn.sh"; ld="$(tamper "$W/l_dev12np.sh" "$W/l_dev12nn.sh" "$KS860" '"Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts.NOT-GUARDED",' 1)"
run "2e M12 pin, prefix + ks860 entries neutralised: disjoint -> 0" 0 "$W/l_dev12nn.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "commits=6 files=9 — disjoint" "$W/2e M12 pin, prefix + ks860 entries neutralised: disjoint -> 0.out" || { echo "  cell 2e did not report commits=6 files=9 — disjoint"; FAILS=$((FAILS+1)); }
# 2f: M15 pin, prefix neutralised, the api-gateway auth.ts slot AIMED at startup-migrations.ts (in the delta) -> the exact arm on another slot -> 18.
cp "$W/l_dev15np.sh" "$W/l_dev15aim.sh"; ld="$(tamper "$W/l_dev15np.sh" "$W/l_dev15aim.sh" "$GWAUTH" '"Blockchain/Dev/services/api-gateway/src/startup-migrations.ts",' 1)"
run "2f M15 pin, prefix neutralised, gateway slot aimed at startup-migrations -> 18" 18 "$W/l_dev15aim.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED Blockchain/Dev/services/api-gateway/src/startup-migrations.ts " "$W/2f M15 pin, prefix neutralised, gateway slot aimed at startup-migrations -> 18.out" || { echo "  cell 2f did not name startup-migrations.ts"; FAILS=$((FAILS+1)); }
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
ld="$(tamper "$B" "$W/b_tier.md" "TIER 1" "TIER 3" 1)"
run "9 brief says TIER 3 (brief tamper)" 7 "$L" "$W/b_tier.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_tier.txt" "TIER 1" "TIER 3" 1)"
run "10 prompt says TIER 3 (prompt tamper)" 7 "$L" "$B" "$W/p_tier.txt" "" check "$ld"
ld="$(tamper "$B" "$W/b_round.md" "ROUND 1" "ROUND 3" 1)"
run "11 brief says ROUND 3 (brief tamper)" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_round.txt" "ROUND 1" "ROUND 3" 1)"
run "12 prompt says ROUND 3 (prompt tamper)" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"

# ---- prompt clauses ---------------------------------------------------------------------------------------
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard" 1)"
run "13 prompt lacks ultrathink first line" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_path.txt" "/briefs/2026-09-14_secuura-983-ks823-tier1.md" "/briefs/2026-09-14_secuura-OTHER-tier1.md" 1)"
run "14 prompt lacks the real brief path" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "SEND YOUR VERDICT" 1)"
run "15 prompt lacks MAIL YOUR VERDICT" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_push.txt" "or preflight.sh inside the Secuura checkout" "or preflight.sh within the Secuura checkout" 1)"
run "16 prompt lacks the NEVER-push line" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mem.txt" "Do no memory maintenance" "Do no memory upkeep" 1)"
run "17 prompt lacks no-memory-maintenance" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "NEVER print a secret value" 1)"
run "18 prompt lacks NEVER-print-a-credential" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- the head-SHA-in-both guard (exit 20), both arms -------------------------------------------------------
ld="$(tamper "$P" "$W/p_sha.txt" "$HEAD" "f62c975c1" 1)"
run "20a prompt lacks the full head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA" "$W/20a prompt lacks the full head SHA (exit 20).out" || { echo "  cell 20a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha.md" "$HEAD" "f62c975c1" 1)"
run "20b brief lacks the full head SHA (exit 20)" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"

# ---- launch modes with NO claude on PATH -------------------------------------------------------------------
run "23 override launch, no claude on PATH -> 16" 16 "$L" "$B" "$P" "" launch-override LANDED
run "24 real launch (not installed yet), no claude -> 3" 3 "$L" "$B" "$P" "" launch-real LANDED
/usr/bin/grep -q "brief missing or empty: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.md" "$W/24 real launch (not installed yet), no claude -> 3.out" \
  || { echo "  cell 24 did not refuse on the REAL brief path"; FAILS=$((FAILS+1)); }
# 22: a launcher copy whose DEFAULT brief/prompt point at the scratch set (no overrides set), stdin NOT a TTY -> every guard
#     passes, the override check passes, the TTY guard refuses -> 22.
cp "$L" "$W/l_tty.sh"
ld1="$(tamper "$L" "$W/l_tty.sh" 'BRIEF="${QA983_BRIEF:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.md}"' "BRIEF=\"\${QA983_BRIEF:-$B}\"" 1)"
ld2="$(tamper "$W/l_tty.sh" "$W/l_tty2.sh" 'PROMPT_FILE="${QA983_PROMPT:-$WED/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-983-ks823-tier1.prompt.txt}"' "PROMPT_FILE=\"\${QA983_PROMPT:-$P}\"" 1)"
[ "$ld1" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "22 real launch shape (defaults -> scratch set), stdin not a TTY -> 22" 22 "$W/l_tty2.sh" "" "" "" launch-notty "$ld"
/usr/bin/grep -q "stdin is not a TTY" "$W/22 real launch shape (defaults -> scratch set), stdin not a TTY -> 22.out" || { echo "  cell 22 wrong reason"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $M18" "$W/22 real launch shape (defaults -> scratch set), stdin not a TTY -> 22.out" || { echo "  cell 22 did not reach the DEV_NOTE echo (a guard refused earlier)"; FAILS=$((FAILS+1)); }
# 22b: the same launcher under a pty (script) -> the TTY guard passes -> cd -> exec claude, which is ABSENT -> 127.
run "22b the same under a pty (script), claude absent -> 127 at the exec line" 127 "$W/l_tty2.sh" "" "" "" launch-tty "$ld"
/usr/bin/grep -q "claude: command not found\|exec: claude: not found\|claude: No such file" "$W/22b the same under a pty (script), claude absent -> 127 at the exec line.out" "$W/22b the same under a pty (script), claude absent -> 127 at the exec line.typescript" 2>/dev/null \
  || { echo "  cell 22b did not reach the exec line (no 'claude: not found' from the exec)"; FAILS=$((FAILS+1)); }

# ---- raw-control-byte census on the whole set + a synthetic positive control ---------------------------------
python3 - "$L" "$B" "$P" "$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_983.py" "$G/gh_read.py" "$G/linear_read.py" <<'PY' || FAILS=$((FAILS+1))
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
run "25 green again (pristine sha-identical)" 0 "$L" "$B" "$P" "" check "$id"

echo "pristine sha256: launcher ${SHA_L1:0:16} brief ${SHA_B1:0:16} prompt ${SHA_P1:0:16}"
echo "work dir (kept, never rm'd): $W"
echo "FAILS=$FAILS"
echo "$(date '+%Y-%m-%d %H:%M:%S %Z')"
exit "$FAILS"
