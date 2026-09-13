#!/bin/bash
# redproof.sh — red-proof launch_qa_secuura_ks798_841_799_881_r2.sh on SCRATCH COPIES only. Never touches the real dirs.
# Green asserted FIRST (cell 0, rc 0, 13 guard lines), one red per guard at a DISTINCT exit code, every tamper asserted
# LANDED (anchor must exist; the new marker grep'd >= expected; cmp non-identical to pristine; for removals the removed
# token grep'd 0), green again LAST on the sha-identical pristine set. Prints: cell | expected rc | got rc | LANDED | ok/FAIL
# and FAILS=N. Every cell runs under env -i with a PATH that has git/python3/grep but NO claude, GH_TOKEN unset, 120 s alarm.
# The develop guard's arms are exercised against the LIVE M15..M18 delta (3 squashes, 6 files: entrypoint-corpus.test.ts
# under the packages/shared tests prefix; ks949-platform-admin-seed-identity.test.ts under the services/auth/ prefix;
# docker-build.sh + two scripts/__tests__ suites + api-gateway startup-migrations.ts — none guarded): the shipped list
# must read GUARDED (18) from M17 (the prefix arm) and from M15 (both prefixes); a pin whose delta touches nothing guarded
# once a prefix is neutralised must read MOVED/disjoint (0); the EXACT arm fires when a slot is aimed at a file the delta
# moved; the round-1 base 306d0db92 (448 files) is UNJUDGEABLE (18). The TTY guard (21) is exercised both ways: headless
# (no pty) with overrides set -> 21; under script(1)'s pty with overrides set -> 16 (the guard AFTER it), proving 21 sits
# before 16 and --check needs no pty.
set -u
G="${G:?set G to the gate881r2 set dir}"
L="$G/launch_qa_secuura_ks798_841_799_881_r2.sh"
B="$G/2026-09-14_secuura-881-ks798-841-799-tier1-r2.md"
P="$G/2026-09-14_secuura-881-ks798-841-799-tier1-r2.prompt.txt"
W="$(mktemp -d "$G/redproof.XXXXXX")"
FAILS=0
SHA_L0="$(shasum -a 256 "$L" | cut -d' ' -f1)"; SHA_B0="$(shasum -a 256 "$B" | cut -d' ' -f1)"; SHA_P0="$(shasum -a 256 "$P" | cut -d' ' -f1)"
MB1='306d0db923183f3b62b053f0242549e37bdf362c'; M15='1c38077ba2aea5f4c4371c1b68796026dc577764'; M17='a4ef481c897265ae01936ad10d84d547d95557d2'; M18='8861e62161466c40f08d2b10a30edeb203123993'

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
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA881R2_BRIEF="$brief" QA881R2_PROMPT="$prompt" ${head:+QA881R2_HEAD="$head"} \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" --check >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override" ]; then   # headless: stdin is /dev/null, not a TTY
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA881R2_BRIEF="$brief" QA881R2_PROMPT="$prompt" \
      perl -e 'alarm 120; exec @ARGV' bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
  elif [ "$mode" = "launch-override-pty" ]; then   # script(1) hands the launcher a pty on stdin
    env -i -u GH_TOKEN PATH="$NOCLAUDE_PATH" HOME="$HOME" QA881R2_BRIEF="$brief" QA881R2_PROMPT="$prompt" \
      perl -e 'alarm 120; exec @ARGV' script -q /dev/null bash "$lch" >"$W/$name.out" 2>&1 </dev/null; rc=$?
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
PKGPFX='"Blockchain/Dev/packages/shared/src/__tests__/",'
AUTHPFX='"Blockchain/Dev/services/auth/",'

# ---- cell 0: green --check -------------------------------------------------------------------------------
run "0 green --check (scratch brief+prompt)" 0 "$L" "$B" "$P" "" check LANDED
/usr/bin/grep -q "all guards pass" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks 'all guards pass'"; FAILS=$((FAILS+1)); }
[ "$(/usr/bin/grep -c '^  ' "$W/0 green --check (scratch brief+prompt).out")" = "13" ] || { echo "  green output does not list 13 guard lines"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "origin develop " "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the develop note"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief names the round-1 read (Peter's review 5140256072 + comment 5583115315) and it is present on disk" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the round-1 read line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt both name the head SHA 8ac9db66f6fd0d751f74ecc95bb314210a31ec52" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the head-SHA line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "brief and prompt agree on TIER 1 and ROUND 2" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the TIER 1 / ROUND 2 line"; FAILS=$((FAILS+1)); }
/usr/bin/grep -q "requires a TTY on stdin — exit 21" "$W/0 green --check (scratch brief+prompt).out" || { echo "  green output lacks the TTY note"; FAILS=$((FAILS+1)); }
echo "  develop note at cell 0: $(/usr/bin/grep 'origin develop ' "$W/0 green --check (scratch brief+prompt).out" | cut -c1-160)"

# ---- head / develop / merge-base --------------------------------------------------------------------------
run "1 wrong head sha (env override)" 6 "$L" "$B" "$P" "0000000000000000000000000000000000000000" check LANDED
cp "$L" "$W/l_dev.sh"; ld="$(tamper "$L" "$W/l_dev.sh" "$DEVPIN" "DEVELOP_SHA='1111111111111111111111111111111111111111'" 1)"
run "2 unknown develop sha -> unjudgeable delta" 18 "$W/l_dev.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: UNJUDGEABLE" "$W/2 unknown develop sha -> unjudgeable delta.out" || { echo "  cell 2 did not say UNJUDGEABLE"; FAILS=$((FAILS+1)); }
# 2b: pinned to the round-1 base 306d0db92 — the live delta to M18 is 212 squashes / 448 files (the compare API reports its 300-file cap) -> >250 -> UNJUDGEABLE -> 18.
cp "$L" "$W/l_devmb1.sh"; ld="$(tamper "$L" "$W/l_devmb1.sh" "$DEVPIN" "DEVELOP_SHA='$MB1'" 1)"
run "2b pinned to the round-1 base 306d0db92: 448-file delta (API caps at 300) -> UNJUDGEABLE -> 18" 18 "$W/l_devmb1.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "UNJUDGEABLE status=ahead files=" "$W/2b pinned to the round-1 base 306d0db92: 448-file delta (API caps at 300) -> UNJUDGEABLE -> 18.out" || { echo "  cell 2b did not say UNJUDGEABLE status=ahead files=N"; FAILS=$((FAILS+1)); }
echo "  cell 2b: $(/usr/bin/grep -o 'UNJUDGEABLE [^—]*' "$W/2b pinned to the round-1 base 306d0db92: 448-file delta (API caps at 300) -> UNJUDGEABLE -> 18.out" | head -1 | cut -c1-80)"
# 2c: pinned to M17 with the SHIPPED list — M17..M18 = entrypoint-corpus.test.ts only -> the packages/shared tests PREFIX arm -> 18.
cp "$L" "$W/l_dev17.sh"; ld="$(tamper "$L" "$W/l_dev17.sh" "$DEVPIN" "DEVELOP_SHA='$M17'" 1)"
run "2c pinned to M17, shipped list: packages-shared tests prefix arm -> 18" 18 "$W/l_dev17.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: GUARDED Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts " "$W/2c pinned to M17, shipped list: packages-shared tests prefix arm -> 18.out" || { echo "  cell 2c did not name entrypoint-corpus.test.ts as the (only) guarded hit"; FAILS=$((FAILS+1)); }
# 2d: pinned to M17 with the packages/shared tests PREFIX neutralised -> the one-file delta is disjoint -> MOVED -> 0.
cp "$W/l_dev17.sh" "$W/l_dev17np.sh"; ld="$(tamper "$W/l_dev17.sh" "$W/l_dev17np.sh" "$PKGPFX" '"Blockchain/Dev/packages/shared/src/__tests__-NOT-GUARDED/",' 1)"
run "2d M17 pin, packages prefix neutralised: one-file delta disjoint -> 0" 0 "$W/l_dev17np.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "origin develop MOVED $M17 -> $M18: commits=1 files=1 — disjoint from the fifteen guarded paths" "$W/2d M17 pin, packages prefix neutralised: one-file delta disjoint -> 0.out" || { echo "  cell 2d did not report MOVED … commits=1 files=1 — disjoint"; FAILS=$((FAILS+1)); }
echo "  cell 2d note: $(/usr/bin/grep 'origin develop MOVED' "$W/2d M17 pin, packages prefix neutralised: one-file delta disjoint -> 0.out" | cut -c1-150)"
# 2e: pinned to M15 with the packages prefix neutralised — M15..M18 also carries ks949-platform-admin-seed-identity.test.ts
#     under services/auth/ -> the services/auth/ PREFIX arm fires -> 18 (the arm that guards the 703 ratio and the merge shape).
cp "$W/l_dev17np.sh" "$W/l_dev15np.sh"; ld="$(tamper "$W/l_dev17np.sh" "$W/l_dev15np.sh" "DEVELOP_SHA='$M17'" "DEVELOP_SHA='$M15'" 1)"
run "2e M15 pin, packages prefix neutralised: services-auth prefix arm on ks949 -> 18" 18 "$W/l_dev15np.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "not provably disjoint: GUARDED Blockchain/Dev/services/auth/src/__tests__/ks949-platform-admin-seed-identity.test.ts " "$W/2e M15 pin, packages prefix neutralised: services-auth prefix arm on ks949 -> 18.out" || { echo "  cell 2e did not name ks949 as the ONLY guarded hit"; FAILS=$((FAILS+1)); }
echo "  cell 2e: $(/usr/bin/grep -o 'GUARDED [^—]*' "$W/2e M15 pin, packages prefix neutralised: services-auth prefix arm on ks949 -> 18.out" | head -1 | cut -c1-160)"
# 2f: pinned to M15 with BOTH prefixes neutralised -> the six-file delta is disjoint -> 0 (a control that the auth prefix alone made 2e red).
cp "$W/l_dev15np.sh" "$W/l_dev15nn.sh"; ld="$(tamper "$W/l_dev15np.sh" "$W/l_dev15nn.sh" "$AUTHPFX" '"Blockchain/Dev/services/auth-NOT-GUARDED/",' 1)"
run "2f M15 pin, both prefixes neutralised: six-file delta disjoint -> 0" 0 "$W/l_dev15nn.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "commits=3 files=6 — disjoint" "$W/2f M15 pin, both prefixes neutralised: six-file delta disjoint -> 0.out" || { echo "  cell 2f did not report commits=3 files=6 — disjoint"; FAILS=$((FAILS+1)); }
# 2g: M17 pin, packages prefix neutralised, the oauth.ts slot AIMED at entrypoint-corpus.test.ts (the file the delta moved) -> EXACT arm -> 18.
cp "$W/l_dev17np.sh" "$W/l_dev17aim.sh"; ld="$(tamper "$W/l_dev17np.sh" "$W/l_dev17aim.sh" '"Blockchain/Dev/services/auth/src/routes/oauth.ts",' '"Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts",' 1)"
run "2g M17 pin, prefix neutralised, slot-1 entry aimed at entrypoint-corpus -> 18" 18 "$W/l_dev17aim.sh" "$B" "$P" "" check "$ld"
/usr/bin/grep -q "GUARDED Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts " "$W/2g M17 pin, prefix neutralised, slot-1 entry aimed at entrypoint-corpus -> 18.out" || { echo "  cell 2g did not name entrypoint-corpus.test.ts"; FAILS=$((FAILS+1)); }
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
ld="$(tamper "$B" "$W/b_round.md" "ROUND 2" "ROUND 3" 1)"
run "11 brief says ROUND 3 (brief tamper)" 15 "$L" "$W/b_round.md" "$P" "" check "$ld"
ld="$(tamper "$P" "$W/p_round.txt" "ROUND 2" "ROUND 3" 1)"
run "12 prompt says ROUND 3 (prompt tamper)" 15 "$L" "$B" "$W/p_round.txt" "" check "$ld"

# ---- prompt clauses ---------------------------------------------------------------------------------------
ld="$(tamper "$P" "$W/p_think.txt" "ultrathink" "think hard" 1)"
run "13 prompt lacks ultrathink first line" 8 "$L" "$B" "$W/p_think.txt" "" check "$ld"
ld="$(tamper "$P" "$W/p_path.txt" "/briefs/2026-09-14_secuura-881-ks798-841-799-tier1-r2.md" "/briefs/2026-09-14_secuura-OTHER-tier1-r2.md" 1)"
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
ld="$(tamper "$P" "$W/p_sha.txt" "8ac9db66f6fd0d751f74ecc95bb314210a31ec52" "8ac9db66f" 1)"
run "20a prompt lacks the full head SHA (exit 20)" 20 "$L" "$B" "$W/p_sha.txt" "" check "$ld"
/usr/bin/grep -q "does not name the head SHA" "$W/20a prompt lacks the full head SHA (exit 20).out" || { echo "  cell 20a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_sha.md" "8ac9db66f6fd0d751f74ecc95bb314210a31ec52" "8ac9db66f" 1)"
run "20b brief lacks the full head SHA (exit 20)" 20 "$L" "$W/b_sha.md" "$P" "" check "$ld"

# ---- the round-1 READ guard (exit 19), three arms ----------------------------------------------------------
ld="$(tamper "$B" "$W/b_r1.md" "item0/peter_comment_5583115315.md" "item0/peter_comment_5583115315.RENAMED.md" 1)"
run "19a brief does not name the round-1 read path" 19 "$L" "$W/b_r1.md" "$P" "" check "$ld"
/usr/bin/grep -q "brief does not name the round-1 READ" "$W/19a brief does not name the round-1 read path.out" || { echo "  cell 19a wrong reason"; FAILS=$((FAILS+1)); }
ld="$(tamper "$B" "$W/b_r1id.md" "5140256072" "514025XXXX" 1)"
run "19b brief does not name Peter's review id 5140256072" 19 "$L" "$W/b_r1id.md" "$P" "" check "$ld"
/usr/bin/grep -q "brief does not name the round-1 READ" "$W/19b brief does not name Peter's review id 5140256072.out" || { echo "  cell 19b wrong reason"; FAILS=$((FAILS+1)); }
cp "$L" "$W/l_r1.sh"; ld="$(tamper "$L" "$W/l_r1.sh" "R1_READ='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s212/item0/peter_comment_5583115315.md'" "R1_READ='/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-13_s212/item0/peter_comment_5583115315.does-not-exist.md'" 1)"
# the brief must ALSO name that path for arm 3 to be reached: give it a brief that carries the renamed path
ld2="$(tamper "$B" "$W/b_r1b.md" "item0/peter_comment_5583115315.md" "item0/peter_comment_5583115315.does-not-exist.md" 1)"
[ "$ld" = LANDED ] && [ "$ld2" = LANDED ] && ld=LANDED || ld=NOT-LANDED
run "19c round-1 read named but missing on disk" 19 "$W/l_r1.sh" "$W/b_r1b.md" "$P" "" check "$ld"
/usr/bin/grep -q "missing or empty" "$W/19c round-1 read named but missing on disk.out" || { echo "  cell 19c wrong reason"; FAILS=$((FAILS+1)); }

# ---- launch modes with NO claude on PATH -------------------------------------------------------------------
run "21a override launch, HEADLESS (stdin not a TTY) -> 21" 21 "$L" "$B" "$P" "" launch-override LANDED
/usr/bin/grep -q "stdin is not a TTY" "$W/21a override launch, HEADLESS (stdin not a TTY) -> 21.out" || { echo "  cell 21a wrong reason"; FAILS=$((FAILS+1)); }
run "21b override launch under script(1)'s pty -> 16 (the guard after the TTY guard)" 16 "$L" "$B" "$P" "" launch-override-pty LANDED
/usr/bin/grep -q "a launch with test overrides set" "$W/21b override launch under script(1)'s pty -> 16 (the guard after the TTY guard).out" || { echo "  cell 21b wrong reason (expected the override guard, i.e. the TTY guard passed under the pty)"; FAILS=$((FAILS+1)); }
run "22 real launch (not installed yet), no claude" 3 "$L" "$B" "$P" "" launch-real LANDED
/usr/bin/grep -q "brief missing or empty: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-14_secuura-881-ks798-841-799-tier1-r2.md" "$W/22 real launch (not installed yet), no claude.out" \
  || { echo "  cell 22 did not refuse on the REAL brief path"; FAILS=$((FAILS+1)); }

# ---- raw-control-byte census on the whole set + a synthetic positive control ---------------------------------
python3 - "$L" "$B" "$P" "$G/controls_check.sh" "$G/redproof.sh" "$G/gen_launcher_881r2.py" "$G/gh_read.py" "$G/linear_read.py" "$G/linear_search.py" <<'PY' || FAILS=$((FAILS+1))
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
