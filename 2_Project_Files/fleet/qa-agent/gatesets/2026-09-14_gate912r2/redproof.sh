#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh on SCRATCH COPIES only. Never touches the
# real dirs. Green asserted FIRST (cell 0, rc 0, 15 guard lines), one red per guard at a DISTINCT exit code, every tamper
# asserted LANDED (anchor must exist; the new marker grep'd >= expected; cmp non-identical to pristine; for removals the
# removed token grep'd 0), green again LAST on the sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED |
# ok/FAIL and FAILS=N. Every cell runs under env -i with a PATH that has git/python3/grep but NO claude, GH_TOKEN unset,
# 120 s alarm, stdin /dev/null (so "headless" is real). The develop guard's arms are exercised against LIVE deltas: the
# round-1 base e559f7bba (369 files on develop's side -> the API's 300 cap -> UNJUDGEABLE, 18); M17 a4ef481c8 with the
# shipped list (M17..M18 = entrypoint-corpus.test.ts under the packages/shared tests PREFIX -> 18) and with that prefix
# neutralised (-> MOVED/disjoint, 0 — the live tip moved from M18 to M19 6e78961e1 mid-build, so the counts are read, not pinned); the KS-927 commit b1cb8466f as the pin (its 40-file delta to M18 carries KS-1069/1070/1071
# on the gateway's verification.ts AND originate route/test moves -> the EXACT arm and the originate/src PREFIX arm, 18; the
# older KS-1058 commit as a pin reads UNJUDGEABLE (264 files > 250) -> 18 by the cap, kept as its own cell);
# the slot aimed at the file M17..M18 moved (EXACT arm, 18). The TTY guard (21) both ways: headless with overrides -> 21;
# under script(1)'s pty with overrides -> 16 (the guard AFTER it). The #937 head guard (22) and the stack guard (23) once each.
set -u
G="${G:?set G to the gate912r2 set dir}"
L="$G/launch_qa_secuura_ks1004_912_r2_ks1059_937_stacked.sh"
B="$G/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md"
P="$G/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
MB1='e559f7bbace5281668637755410273ff58068c15'; M17='a4ef481c897265ae01936ad10d84d547d95557d2'; M18='8861e62161466c40f08d2b10a30edeb203123993'; KS927C='b1cb8466f'
H912='609c44c55323b5c90320847b6837ca37f6586705'; H937='6fd3a8bec4e4cc858d38925e00703a37ffcf1b30'

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
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA912R2_BRIEF="$brief" QA912R2_PROMPT="$prompt" ${head:+QA912R2_HEAD="$head"} \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then   # headless: stdin is /dev/null, not a TTY
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA912R2_BRIEF="$brief" QA912R2_PROMPT="$prompt" \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-pty" ]; then   # script(1) hands the launcher a pty on stdin
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA912R2_BRIEF="$brief" QA912R2_PROMPT="$prompt" \
      perl -e 'alarm 120; exec @ARGV' script -q /dev/null bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  else
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
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
DEVPIN="DEVELOP_SHA='$M18'"
PKGPFX='"Blockchain/Dev/packages/shared/src/__tests__/",'
ORIGPFX='"Blockchain/Dev/services/originate/src/",'
GWFILE='"Blockchain/Dev/services/api-gateway/src/routes/verification.ts",'

# ---- cell 0: green --check -------------------------------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
O="$W/0 green --check (scratch brief+prompt).out"
/usr/bin/grep -q "all guards pass" "$O" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c '^  ' "$O")" = "15" ] || { echo "  green output does not list 15 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop " "$O" || { echo "  green output lacks the develop note"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "stacked head $H937 present at" "$O" || { echo "  green output lacks the #937 head line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "stack relation still merge_base $H912 / ONE file" "$O" || { echo "  green output lacks the stack line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "ahead=4 files=1" "$O" || { echo "  green output lacks the stack compare read"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief names the round-1 read (the recovered NO GO verdict file + transcription comment 5597511879) and it is present on disk" "$O" || { echo "  green output lacks the round-1 read line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt both name the head SHA $H912 and the stacked head SHA $H937" "$O" || { echo "  green output lacks the head-SHA line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt agree on TIER 1 and ROUND 2" "$O" || { echo "  green output lacks the TIER 1 / ROUND 2 line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "requires a TTY on stdin — exit 21" "$O" || { echo "  green output lacks the TTY note"; FAILS=$((FAILS+1)); }
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$O" | cut -c1-160)"

# ---- head / #937 head / develop / merge-base / stack ------------------------------------------------------
run "1 wrong head sha (env override)" 6 "$L" "$B" "$P" "0000000000000000000000000000000000000000" check LANDED
cp "$L" "$W/l_h937.sh"; ld="$(tamper "$L" "$W/l_h937.sh" "HEAD_937='$H937'" "HEAD_937='1111111111111111111111111111111111111111'" 1)"
run "1b wrong #937 head (launcher tamper) -> 22" 22 "$W/l_h937.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "the stacked head moved" "$W/1b wrong #937 head (launcher tamper) -> 22.out" || { echo "  cell 1b wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "$DEVPIN" "DEVELOP_SHA='1111111111111111111111111111111111111111'" 1)"
run "2 unknown develop sha -> unjudgeable delta" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: UNJUDGEABLE" "$W/2 unknown develop sha -> unjudgeable delta.out" || { echo "  cell 2 did not say UNJUDGEABLE"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_devmb1.sh"; ld="$(tamper "$L" "$W/l_devmb1.sh" "$DEVPIN" "DEVELOP_SHA='$MB1'" 1)"
run "2b pinned to the round-1 base e559f7bba: 369-file delta (API caps at 300) -> UNJUDGEABLE -> 18" 18 "$W/l_devmb1.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "UNJUDGEABLE status=ahead files=" "$W/2b pinned to the round-1 base e559f7bba: 369-file delta (API caps at 300) -> UNJUDGEABLE -> 18.out" || { echo "  cell 2b did not say UNJUDGEABLE status=ahead files=N"; FAILS=$((FAILS+1)); }
echo "  cell 2b: $(/usr/bin/grep -o 'UNJUDGEABLE [^—]*' "$W/2b pinned to the round-1 base e559f7bba: 369-file delta (API caps at 300) -> UNJUDGEABLE -> 18.out" | head -1 | cut -c1-80)"
cp "$L" "$W/l_dev17.sh"; ld="$(tamper "$L" "$W/l_dev17.sh" "$DEVPIN" "DEVELOP_SHA='$M17'" 1)"
run "2c pinned to M17, shipped list: packages-shared tests prefix arm -> 18" 18 "$W/l_dev17.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: GUARDED Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts " "$W/2c pinned to M17, shipped list: packages-shared tests prefix arm -> 18.out" || { echo "  cell 2c did not name entrypoint-corpus.test.ts as the (only) guarded hit"; FAILS=$((FAILS+1)); }
cp "$W/l_dev17.sh" "$W/l_dev17np.sh"; ld="$(tamper "$W/l_dev17.sh" "$W/l_dev17np.sh" "$PKGPFX" '"Blockchain/Dev/packages/shared/src/__tests__-NOT-GUARDED/",' 1)"
run "2d M17 pin, packages prefix neutralised: one-file delta disjoint -> 0" 0 "$W/l_dev17np.sh" "$B" "$P" "" check "$ld"
# NOTE (restart-drafter, 2026-09-14 12:2x AEST): this pin spans M17 through the LIVE current tip, which as of the
# M21_ALLOWED content-judged guard (Wednesday's instruction) may now ALSO pick up the four cleared M21 paths
# alongside the neutralised packages-shared prefix -- the guard then reports "ALLOWED … cleared=…" rather than
# "DISJOINT … — disjoint from the thirteen guarded paths"; either is correct (both are rc 0, exit code is what the
# `run` harness already checked above), so this assertion accepts either wording rather than pinning one.
/usr/bin/grep -Eq "origin develop MOVED $M17 -> .*(— disjoint from the thirteen guarded paths|cleared=)" "$W/2d M17 pin, packages prefix neutralised: one-file delta disjoint -> 0.out" || { echo "  cell 2d did not report a MOVED note (disjoint or content-cleared)"; FAILS=$((FAILS+1)); }
echo "  cell 2d note: $(/usr/bin/grep 'origin develop MOVED' "$W/2d M17 pin, packages prefix neutralised: one-file delta disjoint -> 0.out" | cut -c1-150)"
cp "$L" "$W/l_dev927.sh"; ld="$(tamper "$L" "$W/l_dev927.sh" "$DEVPIN" "DEVELOP_SHA='$KS927C'" 1)"
run "2e pinned to the KS-927 commit (40 files): gateway verification.ts EXACT arm + originate-src prefix arm -> 18" 18 "$W/l_dev927.sh" "$B" "$P" "" check "$ld"
O="$W/2e pinned to the KS-927 commit (40 files): gateway verification.ts EXACT arm + originate-src prefix arm -> 18.out"
/usr/bin/grep -q "not provably disjoint: GUARDED " "$O" && /usr/bin/grep -q "Blockchain/Dev/services/api-gateway/src/routes/verification.ts" "$O" && /usr/bin/grep -q "Blockchain/Dev/services/originate/src/routes/verification.ts" "$O" && /usr/bin/grep -q "ks1071-verify-confidence-one-mapping.test.ts" "$O" \
  || { echo "  cell 2e did not name the gateway verification.ts, an originate/src path AND a gateway test among the guarded hits"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_dev1058.sh"; ld="$(tamper "$L" "$W/l_dev1058.sh" "$DEVPIN" "DEVELOP_SHA='27509dc7a541d599558317a3258300d0f5e6bf3c'" 1)"
run "2e2 pinned to the KS-1058 commit: 264+-file delta (>250) -> UNJUDGEABLE -> 18" 18 "$W/l_dev1058.sh" "$B" "$P" "" check "$ld"
# NOTE (restart-drafter, pass 3): as live develop keeps growing, this delta's own file count only grows toward
# (and is capped at) the GitHub compare API's hard 300-file limit -- it read 264 when this cell was first written,
# 300 as of pass 3. Either is a correct demonstration of the >250 cap; match the whole plausible range 250-300
# rather than pin one snapshot value that live drift keeps invalidating.
/usr/bin/grep -Eq "UNJUDGEABLE status=ahead files=(2[5-9][0-9]|300)" "$W/2e2 pinned to the KS-1058 commit: 264+-file delta (>250) -> UNJUDGEABLE -> 18.out" || { echo "  cell 2e2 did not say UNJUDGEABLE files=25x-300"; FAILS=$((FAILS+1)); }
echo "  cell 2e: $(/usr/bin/grep -o 'GUARDED [^—]*' "$O" | head -1 | cut -c1-220)"
cp "$W/l_dev17np.sh" "$W/l_dev17aim.sh"; ld="$(tamper "$W/l_dev17np.sh" "$W/l_dev17aim.sh" '"Blockchain/Dev/services/originate/src/services/anchorStateSync.ts",' '"Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts",' 1)"
run "2f M17 pin, prefix neutralised, slot-1 entry aimed at entrypoint-corpus -> EXACT arm -> 18" 18 "$W/l_dev17aim.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts " "$W/2f M17 pin, prefix neutralised, slot-1 entry aimed at entrypoint-corpus -> EXACT arm -> 18.out" || { echo "  cell 2f did not name entrypoint-corpus.test.ts"; FAILS=$((FAILS+1)); }

# ---- cell 2g: M21_ALLOWED weakened (one dict entry stripped) against the REAL LIVE current develop tip --------
# Wednesday's 2026-09-14 12:1x AEST instruction: prove the M21 content-judged clearance is blob-EXACT per path,
# not a blanket exemption for the whole services/originate/src/ or packages/shared/src/__tests__/ prefix. A
# scratch copy of the REAL launcher (M18 pin unchanged, live develop read as-is -- no DEVELOP_SHA tamper) with the
# auth.ts entry stripped from M21_ALLOWED must refuse (18) on live current develop even though three of the four
# M21 paths would still clear -- one unrecognised guarded hit is enough to refuse the whole merge.
AUTHENTRY='    "Blockchain/Dev/services/originate/src/middleware/auth.ts": "f08ee1a895bc878bc2656f649833706f665686e7",'
cp "$L" "$W/l_dev21weak.sh"; ld="$(tamper "$L" "$W/l_dev21weak.sh" "$AUTHENTRY" "" 1)"
run "2g M21_ALLOWED weakened (auth.ts entry stripped) on LIVE current develop -> 18" 18 "$W/l_dev21weak.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED.*middleware/auth.ts" "$W/2g M21_ALLOWED weakened (auth.ts entry stripped) on LIVE current develop -> 18.out" || { echo "  cell 2g did not name middleware/auth.ts as the unresolved hit"; FAILS=$((FAILS+1)); }

# ---- cell 2h: pass-3 (M29/KS-780/#985) entry weakened against the REAL LIVE current develop tip ---------------
# Wednesday's 2026-09-14 13:2x AEST instruction, same technique as 2g but against one of the four M29 entries
# added in pass 3: stripping the orgId.ts entry must refuse (18) on live current develop even though the other
# seven DEV_CONTENT_ALLOWED entries (four M21 + three remaining M29) would still clear.
ORGIDENTRY='    "Blockchain/Dev/services/originate/src/services/orgId.ts": "f87b261b83248a53c1f2f10b8222a009fab31892",'
cp "$L" "$W/l_dev29weak.sh"; ld="$(tamper "$L" "$W/l_dev29weak.sh" "$ORGIDENTRY" "" 1)"
run "2h DEV_CONTENT_ALLOWED weakened (orgId.ts entry stripped) on LIVE current develop -> 18" 18 "$W/l_dev29weak.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED.*services/orgId.ts" "$W/2h DEV_CONTENT_ALLOWED weakened (orgId.ts entry stripped) on LIVE current develop -> 18.out" || { echo "  cell 2h did not name services/orgId.ts as the unresolved hit"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_mb.sh"; ld="$(tamper "$L" "$W/l_mb.sh" "MERGE_BASE='$M18'" "MERGE_BASE='2222222222222222222222222222222222222222'" 1)"
run "3 wrong merge-base (launcher tamper)" 10 "$W/l_mb.sh" "$B" "$P" "" check "$ld"
cp "$L" "$W/l_stack.sh"; ld="$(tamper "$L" "$W/l_stack.sh" '[ "$STACK_READ" = "$HEAD_SHA ahead=4 files=1" ]' '[ "$STACK_READ" = "$HEAD_SHA ahead=1 files=1" ]' 1)"
run "3b stack expectation tampered (ahead=1): the live read ahead=4 -> 23" 23 "$W/l_stack.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "the stacked delta is not ONE file over #912's head: compare reads '$H912 ahead=4 files=1'" "$W/3b stack expectation tampered (ahead=1): the live read ahead=4 -> 23.out" || { echo "  cell 3b wrong reason (expected the live read quoted)"; FAILS=$((FAILS+1)); }
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
ld="$(tamper "$B" "$W/b_round.md" "ROUND 2" "ROUND 3" 1)"
run "11 brief says ROUND 3 (brief tamper)" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_round.txt" "ROUND 2" "ROUND 3" 1)"
run "12 prompt says ROUND 3 (prompt tamper)" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"

# ---- prompt clauses ---------------------------------------------------------------------------------------
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard" 1)"
run "13 prompt lacks ultrathink first line" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_path.txt" "/briefs/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md" "/briefs/2026-09-14_secuura-OTHER-tier1-r2.md" 1)"
run "14 prompt lacks the real brief path" 9 "$L" "$B" "$W/p_path.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mail.txt" "MAIL YOUR VERDICT" "SEND YOUR VERDICT" 1)"
run "15 prompt lacks MAIL YOUR VERDICT" 12 "$L" "$B" "$W/p_mail.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_push.txt" "or preflight.sh inside the Secuura checkout" "or preflight.sh within the Secuura checkout" 1)"
run "16 prompt lacks the NEVER-push line" 11 "$L" "$B" "$W/p_push.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_mem.txt" "Do no memory maintenance" "Do no memory upkeep" 1)"
run "17 prompt lacks no-memory-maintenance" 14 "$L" "$B" "$W/p_mem.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_cred.txt" "NEVER print a credential value" "NEVER print a secret value" 1)"
run "18 prompt lacks NEVER-print-a-credential" 17 "$L" "$B" "$W/p_cred.txt" "" check "$ld"

# ---- the head-SHA-in-both guard (exit 20), four arms -------------------------------------------------------
ld="$(tamper "$P" "$W/p_sha.txt" "$H912" "609c44c55" 1)"
run "20a prompt lacks the full #912 head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA" "$W/20a prompt lacks the full #912 head SHA (exit 20).out" || { echo "  cell 20a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha.md" "$H912" "609c44c55" 1)"
run "20b brief lacks the full #912 head SHA (exit 20)" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_sha937.txt" "$H937" "6fd3a8bec" 1)"
run "20c prompt lacks the full #937 head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha937.txt" "" check "$ld"
/usr/bin/grep -q "does not name the stacked head SHA" "$W/20c prompt lacks the full #937 head SHA (exit 20).out" || { echo "  cell 20c wrong reason (expected the stacked-head arm)"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha937.md" "$H937" "6fd3a8bec" 1)"
run "20d brief lacks the full #937 head SHA (exit 20)" 20 "$L" "$W/b_sha937.md" "$P" "" check "$ld"
/usr/bin/grep -q "does not name the stacked head SHA" "$W/20d brief lacks the full #937 head SHA (exit 20).out" || { echo "  cell 20d wrong reason (expected the stacked-head arm)"; FAILS=$((FAILS+1)); }

# ---- the round-1 READ guard (exit 19), three arms ----------------------------------------------------------
ld="$(tamper "$B" "$W/b_r1.md" "reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.md" "reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.RENAMED.md" 1)"
run "19a brief does not name the round-1 verdict path" 19 "$L" "$W/b_r1.md" "$P" "" check "$ld"
/usr/bin/grep -q "brief does not name the round-1 READ" "$W/19a brief does not name the round-1 verdict path.out" || { echo "  cell 19a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_r1id.md" "5597511879" "559751XXXX" 1)"
run "19b brief does not name the transcription comment id 5597511879" 19 "$L" "$W/b_r1id.md" "$P" "" check "$ld"
/usr/bin/grep -q "brief does not name the round-1 READ" "$W/19b brief does not name the transcription comment id 5597511879.out" || { echo "  cell 19b wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_r1.sh"; ld="$(tamper "$L" "$W/l_r1.sh" "R1_READ='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.md'" "R1_READ='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.does-not-exist.md'" 1)"
ld2="$(tamper "$B" "$W/b_r1b.md" "reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.md" "reports/2026-09-09_secuura-ks1004-912-tier1-VERDICT.does-not-exist.md" 1)"
[ "$ld" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "19c round-1 read named but missing on disk" 19 "$W/l_r1.sh" "$W/b_r1b.md" "$P" "" check "$ld"
/usr/bin/grep -q "missing or empty" "$W/19c round-1 read named but missing on disk.out" || { echo "  cell 19c wrong reason"; FAILS=$((FAILS+1)); }

# ---- launch modes with NO claude on PATH -------------------------------------------------------------------
run "21a override launch, HEADLESS (stdin not a TTY) -> 21" 21 "$L" "$B" "$P" "" launch-override LANDED
/usr/bin/grep -q "stdin is not a TTY" "$W/21a override launch, HEADLESS (stdin not a TTY) -> 21.out" || { echo "  cell 21a wrong reason"; FAILS=$((FAILS+1)); }
run "21b override launch under script(1)'s pty -> 16 (the guard after the TTY guard)" 16 "$L" "$B" "$P" "" launch-override-pty LANDED
/usr/bin/grep -q "a launch with test overrides set" "$W/21b override launch under script(1)'s pty -> 16 (the guard after the TTY guard).out" || { echo "  cell 21b wrong reason (expected the override guard, i.e. the TTY guard passed under the pty)"; FAILS=$((FAILS+1)); }
# NOTE (restart-drafter, pass 3, 2026-09-14 13:3x AEST): this cell originally asserted exit 3 (brief missing) on
# the REAL default paths with no overrides, because nothing was installed yet when it was written. Between pass 2
# and pass 3 the coordinator genuinely installed this set's brief/prompt/launcher at their real fleet/qa-agent
# targets (confirmed: installed brief/prompt sha256 match this set's pass-2 deliverables exactly) -- so the REAL
# default paths now resolve to a real, present, content-valid brief and prompt, and a real headless launch with NO
# overrides correctly sails past every content guard and refuses only at the TTY gate (exit 21), same reason as
# cell 21a. This is a MORE valuable check now, not a weaker one: it proves the genuinely installed artifacts pass
# every guard for real. Exit-3 coverage on a missing brief is independently retained by cell 5 (an override-based
# scratch empty-brief file), so nothing is lost by this update.
run "22 real launch on the genuinely installed brief and prompt, no claude" 21 "$L" "$B" "$P" "" launch-real LANDED
/usr/bin/grep -q "stdin is not a TTY" "$W/22 real launch on the genuinely installed brief and prompt, no claude.out" \
  || { echo "  cell 22 did not reach the TTY guard on the real installed paths"; FAILS=$((FAILS+1)); }

# ---- raw-control-byte census on the whole set + a synthetic positive control ---------------------------------
python3 - "$L" "$B" "$P" "$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_912r2.py" "$G/gh_read.py" "$G/gh_read_937.py" "$G/linear_read.py" "$G/linear_search.py" "$G/merge_rederive.sh" <<'PY' || FAILS=$((FAILS+1))
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
