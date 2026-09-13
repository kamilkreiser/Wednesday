#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_ks835_984.sh on SCRATCH COPIES only. Never touches the real dirs (the launcher's
# own ls-remote and GitHub reads are READ verbs; nothing is written outside $G). Green asserted FIRST (cell 0, rc 0, 11 guard
# lines), one red per guard at a DISTINCT exit code, every tamper asserted LANDED (anchor must exist; the new marker grep'd
# >= expected; cmp non-identical to pristine; for removals the removed token grep'd 0), green again LAST on the sha-identical
# pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL and FAILS=N. Every cell runs under env -i with a PATH
# that has git/python3/grep but NO claude, GH_TOKEN unset, 120 s alarm. The TTY guard (exit 21) is exercised BOTH ways: headless
# (the Bash-tool shape) -> 21; under a pseudo-terminal (python pty.spawn, the pane shape) with overrides set -> 16, which proves
# the guard PASSES a real TTY and the override guard behind it fires. The develop guard's arms are exercised against LIVE
# deltas: pinned to M15 (M15..M18 = 3 squashes / 6 files, none guarded, jwt.ts + oauth.ts unmoved) -> MOVED/disjoint (0);
# pinned to M9 (M9..M18 = 9 squashes / 22 files incl. the ks860 guard file AND routes/auth.ts) -> GUARDED (18); M9 with those
# two entries neutralised -> disjoint (0); the two judged files' blob arms via tampered blob lists (OTHER -> 18; LANDED -> 19).
set -u
G="${G:?set G to the gate984 scratch dir}"
L="$G/launch_qa_secuura_ks835_984.sh"
B="$G/2026-09-14_secuura-984-ks835-tier1.md"
P="$G/2026-09-14_secuura-984-ks835-tier1.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
M9='50b729d69c58474624508ed79d05c520dab22cc6'; M15='1c38077ba2aea5f4c4371c1b68796026dc577764'; M18='8861e62161466c40f08d2b10a30edeb203123993'
HEAD='d00a2015c89a4720eaeab64482bbd9b89d878024'; PARENT='f62c975c11ec97cdef04500fd98a43618e702763'; GP='e62eab87a6263e25c41c9bb814d5831842bb6c7e'

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
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA984_BRIEF="$brief" QA984_PROMPT="$prompt" ${head:+QA984_HEAD="$head"} \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then   # headless (the Bash-tool shape): stdin is /dev/null
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA984_BRIEF="$brief" QA984_PROMPT="$prompt" \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-pty" ]; then   # the pane shape: a pseudo-terminal on stdin
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA984_BRIEF="$brief" QA984_PROMPT="$prompt" LCH="$lch" OUT="$W/$name.out" \
      perl -e 'alarm 120; exec @ARGV' python3 -c 'import os,pty,sys; out=open(os.environ["OUT"],"wb"); st=pty.spawn(["bash", os.environ["LCH"]], lambda fd: (lambda d: (out.write(d), d)[1])(os.read(fd,1024))); out.close(); sys.exit(os.waitstatus_to_exitcode(st))'; rc=$?
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
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" = "11" ] || { echo "  green output does not list 11 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop still $M18 (M18; git ls-remote)" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the develop-still note (develop moved? re-read)"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt both name the head SHA $HEAD" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the head-SHA line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "ONE commit on SIX files" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the stack-parent line"; FAILS=$((FAILS+1)); }
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$W/0 green --check (scratch brief+prompt).out" | cut -c1-200)"

# ---- head / stack parent / develop ------------------------------------------------------------------------
run "1 wrong head sha (env override)" 6 "$L" "$B" "$P" "0000000000000000000000000000000000000000" check LANDED
cp "$L" "$W/l_sp.sh"; ld="$(tamper "$L" "$W/l_sp.sh" "STACK_PARENT='$PARENT'" "STACK_PARENT='$GP'" 1)"
run "2 stack parent pinned to #982's head -> compare reads ahead=2 files=7 -> 10" 10 "$W/l_sp.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "compare reads '$GP ahead=2 files=7'" "$W/2 stack parent pinned to #982's head -> compare reads ahead=2 files=7 -> 10.out" || { echo "  cell 2 did not read ahead=2 files=7"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "$DEVPIN" "DEVELOP_SHA='1111111111111111111111111111111111111111'" 1)"
run "3 unknown develop pin -> compare unreadable -> UNJUDGEABLE -> 18" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: UNJUDGEABLE" "$W/3 unknown develop pin -> compare unreadable -> UNJUDGEABLE -> 18.out" || { echo "  cell 3 did not say UNJUDGEABLE"; FAILS=$((FAILS+1)); }
# 3b: pinned to M15 — the LIVE M15..M18 delta (3 squashes, 6 files, nothing guarded, jwt.ts/oauth.ts unmoved) -> MOVED/disjoint -> 0
cp "$L" "$W/l_dev15.sh"; ld="$(tamper "$L" "$W/l_dev15.sh" "$DEVPIN" "DEVELOP_SHA='$M15'" 1)"
run "3b pinned to M15: live M15..M18 delta disjoint -> 0 (MOVED note)" 0 "$W/l_dev15.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "origin develop MOVED $M15 -> $M18: commits=3 files=6" "$W/3b pinned to M15: live M15..M18 delta disjoint -> 0 (MOVED note).out" || { echo "  cell 3b did not report MOVED commits=3 files=6"; FAILS=$((FAILS+1)); }
echo "  cell 3b note: $(/usr/bin/grep 'origin develop MOVED' "$W/3b pinned to M15: live M15..M18 delta disjoint -> 0 (MOVED note).out" | cut -c1-170)"
# 3c: pinned to M9 — the LIVE M9..M18 delta carries the ks860 guard file AND routes/auth.ts -> GUARDED naming both -> 18
cp "$L" "$W/l_dev9.sh"; ld="$(tamper "$L" "$W/l_dev9.sh" "$DEVPIN" "DEVELOP_SHA='$M9'" 1)"
run "3c pinned to M9: live delta hits ks860 guard + routes auth.ts -> 18" 18 "$W/l_dev9.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts Blockchain/Dev/services/auth/src/routes/auth.ts" "$W/3c pinned to M9: live delta hits ks860 guard + routes auth.ts -> 18.out" || { echo "  cell 3c did not name the two guarded hits"; FAILS=$((FAILS+1)); }
echo "  cell 3c: $(/usr/bin/grep -o 'GUARDED [^—]*' "$W/3c pinned to M9: live delta hits ks860 guard + routes auth.ts -> 18.out" | head -1 | cut -c1-200)"
# 3d: M9 pin with the two hit entries neutralised -> the 22-file delta is disjoint -> 0 (control: those two entries alone made 3c red)
cp "$W/l_dev9.sh" "$W/l_dev9nn.sh"; ld="$(tamper "$W/l_dev9.sh" "$W/l_dev9nn.sh" '"Blockchain/Dev/services/auth/src/routes/auth.ts",' '"Blockchain/Dev/services/auth/src/routes/auth.ts.NOT-GUARDED",' 1)"
cp "$W/l_dev9nn.sh" "$W/l_dev9nn2.sh"; ld2="$(tamper "$W/l_dev9nn.sh" "$W/l_dev9nn2.sh" '"Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts"]' '"Blockchain/Dev/packages/shared/src/__tests__/ks860-test-listeners-bind-loopback.test.ts.NOT-GUARDED"]' 1)"
[ "$ld" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "3d M9 pin, the two hit entries neutralised: 22-file delta disjoint -> 0" 0 "$W/l_dev9nn2.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "commits=9 files=22" "$W/3d M9 pin, the two hit entries neutralised: 22-file delta disjoint -> 0.out" || { echo "  cell 3d did not report commits=9 files=22"; FAILS=$((FAILS+1)); }
# 3e: the jwt.ts blob arm — M18's blob removed from the OK list -> OTHER -> GUARDED -> 18 (develop unmoved)
cp "$L" "$W/l_jwtok.sh"; ld="$(tamper "$L" "$W/l_jwtok.sh" "JWT_BLOBS_OK='d0d55c11beab2bfd8f8140e12de4016cac742134 62b6db272c911557d764ee2f0e77f1df26923426'" "JWT_BLOBS_OK='62b6db272c911557d764ee2f0e77f1df26923426'" 1)"
run "3e jwt.ts blob at develop not in the OK list -> OTHER -> 18" 18 "$W/l_jwtok.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED develop's jwt.ts blob d0d55c11b (OTHER)" "$W/3e jwt.ts blob at develop not in the OK list -> OTHER -> 18.out" || { echo "  cell 3e wrong reason"; FAILS=$((FAILS+1)); }
# 3f: the jwt.ts LANDED arm — the head blob set to M18's -> LANDED984 -> 19
cp "$L" "$W/l_jwtland.sh"; ld="$(tamper "$L" "$W/l_jwtland.sh" "JWT_BLOB_HEAD='26562a22470af688ae733000792a2b0321650145'" "JWT_BLOB_HEAD='d0d55c11beab2bfd8f8140e12de4016cac742134'" 1)"
run "3f jwt.ts head blob == develop's -> LANDED -> 19" 19 "$W/l_jwtland.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "the PR has landed; nothing to gate" "$W/3f jwt.ts head blob == develop's -> LANDED -> 19.out" || { echo "  cell 3f wrong reason"; FAILS=$((FAILS+1)); }
# 3g: the oauth.ts arms — OK list without M18's blob -> OTHER -> 18; head blob == M18's -> 19
cp "$L" "$W/l_oaok.sh"; ld="$(tamper "$L" "$W/l_oaok.sh" "OAUTH_BLOBS_OK='4b03f555e25bf1221081fdd38f530b983cc763e0 80e05458e9759fbc6c7f33bc8cd90060d30e6149 de00ffceaccd8155349e8de10aaeab3a94c33529'" "OAUTH_BLOBS_OK='80e05458e9759fbc6c7f33bc8cd90060d30e6149 de00ffceaccd8155349e8de10aaeab3a94c33529'" 1)"
run "3g oauth.ts blob at develop not in the OK list -> OTHER -> 18" 18 "$W/l_oaok.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "oauth.ts blob 4b03f555e (OTHER)" "$W/3g oauth.ts blob at develop not in the OK list -> OTHER -> 18.out" || { echo "  cell 3g wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_oaland.sh"; ld="$(tamper "$L" "$W/l_oaland.sh" "OAUTH_BLOB_HEAD='0bab1b8bdd7c9cb2b085bf94d5487a308eb51dd0'" "OAUTH_BLOB_HEAD='4b03f555e25bf1221081fdd38f530b983cc763e0'" 1)"
run "3h oauth.ts head blob == develop's -> LANDED -> 19" 19 "$W/l_oaland.sh" "$B" "$P" "" check "$ld"
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
ld="$(tamper "$P" "$W/p_path.txt" "/briefs/2026-09-14_secuura-984-ks835-tier1.md" "/briefs/2026-09-14_secuura-OTHER-tier1.md" 1)"
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
ld="$(tamper "$P" "$W/p_sha.txt" "$HEAD" "d00a2015c" 1)"
run "20a prompt lacks the full head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA" "$W/20a prompt lacks the full head SHA (exit 20).out" || { echo "  cell 20a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha.md" "$HEAD" "d00a2015c" 1)"
run "20b brief lacks the full head SHA (exit 20)" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"

# ---- launch modes with NO claude on PATH -------------------------------------------------------------------
run "21 override launch, HEADLESS (stdin dev-null) -> the TTY guard, 21" 21 "$L" "$B" "$P" "" launch-override LANDED
/usr/bin/grep -q "stdin is not a TTY" "$W/21 override launch, HEADLESS (stdin dev-null) -> the TTY guard, 21.out" || { echo "  cell 21 wrong reason"; FAILS=$((FAILS+1)); }
run "21b override launch under a PTY -> the TTY guard passes, the override guard fires, 16" 16 "$L" "$B" "$P" "" launch-override-pty LANDED
/usr/bin/grep -q "a launch with test overrides set" "$W/21b override launch under a PTY -> the TTY guard passes, the override guard fires, 16.out" || { echo "  cell 21b wrong reason (did the pty reach the override guard?)"; FAILS=$((FAILS+1)); }
run "22 real launch (not installed yet), headless, no claude -> 3" 3 "$L" "$B" "$P" "" launch-real LANDED
/usr/bin/grep -q "brief missing or empty: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-984-ks835-tier1.md" "$W/22 real launch (not installed yet), headless, no claude -> 3.out" \
  || { echo "  cell 22 did not refuse on the REAL brief path"; FAILS=$((FAILS+1)); }

# ---- raw-control-byte census on the whole set + a synthetic positive control ---------------------------------
python3 - "$L" "$B" "$P" "$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_984.py" "$G/guards_sim.py" "$G/gh_read.py" "$G/linear_read.py" "$G/linear_titles.py" <<'PY' || FAILS=$((FAILS+1))
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
