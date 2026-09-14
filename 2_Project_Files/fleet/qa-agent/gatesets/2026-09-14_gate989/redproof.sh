#!/bin/bash
# redproof.sh — every declared exit code of launch_qa_secuura_989_ks973.sh fires at least once, the pass path returns 0
# on the LIVE develop, the develop-moved arms (DISJOINT -> 0; ALLOWED by blob -> 0; GUARDED -> 18; UNJUDGEABLE -> 18), the
# LANDED arm (19), the headless-TTY arm (21) and the override-on-launch arm (16, under a pty). Cells that need a different
# pin edit a COPY of the launcher in the work dir (never the deliverable); the deliverable's sha256 is asserted unchanged
# at the end. Work dir: mktemp -d under the gate set (never deleted; quarantine by name).
set -u
O='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate989'
L="$O/launch_qa_secuura_989_ks973.sh"
B="$O/2026-09-14_secuura-989-ks973-tier1-r1.md"
P="$O/2026-09-14_secuura-989-ks973-tier1-r1.prompt.txt"
W="$(mktemp -d "$O/redproof.XXXXXX")"
SHA0="$(shasum -a 256 "$L" | cut -c1-16)"
echo "redproof $(date '+%H:%M:%S %Z') work dir $W launcher sha $SHA0"
FAILS=0; FIRED=""
cell() {  # name expected-rc launcher-path [env assignments...]  -- runs --check unless $MODE=launch|pty
  local name="$1" want="$2" lp="$3"; shift 3
  local out="$W/$name.out"
  if [ "${MODE:-check}" = launch ]; then env "$@" bash "$lp" < /dev/null > "$out" 2>&1; rc=$?
  elif [ "${MODE:-check}" = pty ]; then script -q /dev/null env "$@" bash "$lp" < /dev/null > "$out" 2>&1; rc=$?
  else env "$@" bash "$lp" --check > "$out" 2>&1; rc=$?; fi
  FIRED="$FIRED $rc"
  if [ "$rc" = "$want" ]; then echo "ok   $name rc=$rc (want $want): $(tail -1 "$out" | cut -c1-150)"
  else echo "FAIL $name rc=$rc (want $want): $(tail -1 "$out" | cut -c1-200)"; FAILS=$((FAILS+1)); fi
}
OV="QA989_BRIEF=$B QA989_PROMPT=$P"
# 0 — the pass path on the scratch set, against the LIVE develop (M38 today; a moved develop is judged by content)
cell 0_pass 0 "$L" $OV
grep -q 'origin develop MOVED' "$W/0_pass.out" && echo "     (0_pass exercised a develop-MOVED arm: $(grep -o 'MOVED [0-9a-f]* -> [0-9a-f]*: commits=[0-9]* files=[0-9]*' "$W/0_pass.out"))"
grep -q 'origin develop still' "$W/0_pass.out" && echo "     (0_pass: develop still M38 — the MOVED arms are exercised by cells 3m/3a below)"
# 2/3/4/5 — presence guards
sed "s#^QA_DIR=.*#QA_DIR='/nonexistent/qa'#" "$L" > "$W/l2.sh"; cell 2_qa_dir_missing 2 "$W/l2.sh" $OV
cell 3_brief_missing 3 "$L" QA989_BRIEF=/nonexistent/brief.md QA989_PROMPT="$P"
cell 3b_brief_not_installed 3 "$L"
cell 4_prompt_missing 4 "$L" QA989_BRIEF="$B" QA989_PROMPT=/nonexistent/p.txt
sed "s#^REPO=.*#REPO='/nonexistent/repo'#" "$L" > "$W/l5.sh"; cell 5_repo_missing 5 "$W/l5.sh" $OV
# 6 — the head moved / a real SHA at the wrong branch (develop M38's SHA is not at the ks-791 branch)
cell 6_head_moved 6 "$L" $OV QA989_HEAD=0e78c7270188ac45c1c29f927bdf90728f10215d
# 10 — the compare on its own assertion (the expected string moved in a copy) + the merge-base var moved
sed 's#"$MERGE_BASE ahead=2 files=5" \] ||#"$MERGE_BASE ahead=3 files=5" ] ||#' "$L" > "$W/l10a.sh"; grep -q 'ahead=3 files=5' "$W/l10a.sh" || echo "FAIL 10a sed did not land"; cell 10a_compare_ahead 10 "$W/l10a.sh" $OV
sed "s#^MERGE_BASE='0e78c7270188ac45c1c29f927bdf90728f10215d'#MERGE_BASE='54e9b835d486c771d0e6f5461dd9cbbfc77cc75c'#" "$L" > "$W/l10b.sh"; cell 10b_merge_base_M37 10 "$W/l10b.sh" $OV
# 13 — the compare unreadable (an empty env file: no GH_TOKEN)
: > "$W/empty.env"; sed "s#^SECUURA_ENV=.*#SECUURA_ENV='$W/empty.env'#" "$L" > "$W/l13.sh"; cell 13_compare_unreadable 13 "$W/l13.sh" $OV
# 18a — GUARDED blob: develop's provision.ts blob declared "a version nobody pinned" (the OK blob mis-pinned in a copy)
sed 's#"b95f4ee393ab5da261eff06d95069f8bdf24ee3f": "M38"#"0000000000000000000000000000000000000000": "nobody"#' "$L" > "$W/l18a.sh"
grep -q '"0000000000000000000000000000000000000000": "nobody"' "$W/l18a.sh" || echo "FAIL 18a sed did not land"
cell 18a_guarded_blob 18 "$W/l18a.sh" $OV
# 18b — GUARDED path, proven on the LOGIC (no develop commit under the compare cap moves a guarded systemTest path — the
# last three that touched systemTest/fixtures sit 254 / 309 / 376 files behind M38, read 18:27): pin M37 54e9b835d (delta to
# the live develop = KS-487's two files, BACKLOG.md + a ks444 originate test) AND add "BACKLOG.md" to the GUARDED list in a
# copy -> the compare branch names it -> 18. The JUDGED-blob pass (a) reads the LIVE develop, so it passes; (b) refuses.
sed -e "s#^DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'#DEVELOP_SHA='54e9b835d486c771d0e6f5461dd9cbbfc77cc75c'#" -e 's#GUARDED = \["systemTest/fixtures/",#GUARDED = ["BACKLOG.md", "systemTest/fixtures/",#' "$L" > "$W/l18b.sh"
grep -q 'GUARDED = \["BACKLOG.md", "systemTest/fixtures/",' "$W/l18b.sh" || echo "FAIL 18b sed did not land"
cell 18b_guarded_path_M37pin 18 "$W/l18b.sh" $OV
grep -q 'GUARDED BACKLOG.md' "$W/18b_guarded_path_M37pin.out" || { echo "FAIL 18b did not print GUARDED BACKLOG.md"; FAILS=$((FAILS+1)); }
# 18c — UNJUDGEABLE: develop pinned at a SHA that is NOT an ancestor of the live develop (the #989 head itself: status diverged/behind) -> 18
sed "s#^DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'#DEVELOP_SHA='9d0e2016ae60658ec908ee5e500583fd3a318c8a'#" "$L" > "$W/l18c.sh"; cell 18c_unjudgeable_not_ahead 18 "$W/l18c.sh" $OV
grep -q 'UNJUDGEABLE' "$W/18c_unjudgeable_not_ahead.out" || { echo "FAIL 18c did not print UNJUDGEABLE"; FAILS=$((FAILS+1)); }
# 19 — LANDED: develop's provision.ts blob declared as #989's own (the two blob strings swapped in a copy)
sed 's#{"b95f4ee393ab5da261eff06d95069f8bdf24ee3f": "M38"}, {"68c801d626c2b65d76bd6c48d5323a5ce70a82c7": "\#989 own"}#{"68c801d626c2b65d76bd6c48d5323a5ce70a82c7": "x"}, {"b95f4ee393ab5da261eff06d95069f8bdf24ee3f": "\#989 landed (sim)"}#' "$L" > "$W/l19.sh"
grep -q '"b95f4ee393ab5da261eff06d95069f8bdf24ee3f": "#989 landed (sim)"' "$W/l19.sh" || echo "FAIL 19 sed did not land"
cell 19_landed 19 "$W/l19.sh" $OV
# 3m — the develop-MOVED DISJOINT arm explicitly: pin M37 54e9b835d (its delta to the live develop = KS-487's files:
# BACKLOG.md + a ks444 originate test — none under a guarded path) -> 0 with the MOVED note
sed "s#^DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'#DEVELOP_SHA='54e9b835d486c771d0e6f5461dd9cbbfc77cc75c'#" "$L" > "$W/l3m.sh"; cell 3m_develop_moved_disjoint 0 "$W/l3m.sh" $OV
grep -q 'origin develop MOVED 54e9b835d' "$W/3m_develop_moved_disjoint.out" || { echo "FAIL 3m did not print the MOVED note"; FAILS=$((FAILS+1)); }
# 3a — the ALLOWED-by-blob arm: the same M37 pin + "BACKLOG.md" GUARDED (as 18b) + DEV_CONTENT_ALLOWED carrying BACKLOG.md
# at its LIVE blob dca47caa1 (read 18:30 by git rev-parse at M38) -> the hit is CLEARED -> 0 with the "cleared BY BLOB" note.
# 3b (control) = 18b above: the same without the allowlist entry -> 18 naming BACKLOG.md.
sed -e "s#^DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'#DEVELOP_SHA='54e9b835d486c771d0e6f5461dd9cbbfc77cc75c'#" -e 's#GUARDED = \["systemTest/fixtures/",#GUARDED = ["BACKLOG.md", "systemTest/fixtures/",#' -e 's#^DEV_CONTENT_ALLOWED = {$#DEV_CONTENT_ALLOWED = {"BACKLOG.md": "dca47caa155e3f743ad401fc62a56618ec6f47fa",#' "$L" > "$W/l3a.sh"
grep -q '"BACKLOG.md": "dca47caa155e3f743ad401fc62a56618ec6f47fa"' "$W/l3a.sh" || echo "FAIL 3a sed did not land"
cell 3a_allowed_by_blob 0 "$W/l3a.sh" $OV
grep -q 'cleared BY BLOB under guarded paths: BACKLOG.md' "$W/3a_allowed_by_blob.out" && echo "     (3a: the guarded hit was CLEARED by its pinned blob — the ALLOWED note printed)" || { echo "FAIL 3a the ALLOWED note did not print"; FAILS=$((FAILS+1)); }
# 3c — the allowlist with the WRONG blob (a further edit / a regeneration) must NOT clear -> 18
sed -e "s#^DEVELOP_SHA='0e78c7270188ac45c1c29f927bdf90728f10215d'#DEVELOP_SHA='54e9b835d486c771d0e6f5461dd9cbbfc77cc75c'#" -e 's#GUARDED = \["systemTest/fixtures/",#GUARDED = ["BACKLOG.md", "systemTest/fixtures/",#' -e 's#^DEV_CONTENT_ALLOWED = {$#DEV_CONTENT_ALLOWED = {"BACKLOG.md": "0000000000000000000000000000000000000000",#' "$L" > "$W/l3c.sh"
cell 3c_allowlist_wrong_blob_not_cleared 18 "$W/l3c.sh" $OV
grep -q 'GUARDED BACKLOG.md' "$W/3c_allowlist_wrong_blob_not_cleared.out" && echo "     (3c control: a wrong blob in the allowlist does NOT clear the hit)" || { echo "FAIL 3c control"; FAILS=$((FAILS+1)); }
# 7/15/8/9/20/12/11/14/17 — brief / prompt content guards (edited copies of the brief / prompt)
sed 's/TIER 1/TIER 2/g' "$B" > "$W/b7.md"; cell 7_tier 7 "$L" QA989_BRIEF="$W/b7.md" QA989_PROMPT="$P"
sed 's/ROUND 1/ROUND ONE/g' "$P" > "$W/p15.txt"; cell 15_round_missing 15 "$L" QA989_BRIEF="$B" QA989_PROMPT="$W/p15.txt"
sed '1s/ultrathink/think/' "$P" > "$W/p8.txt"; cell 8_ultrathink 8 "$L" QA989_BRIEF="$B" QA989_PROMPT="$W/p8.txt"
sed 's#/briefs/2026-09-14_secuura-989-ks973#/briefs/2026-09-14_secuura-98X-ks973#' "$P" > "$W/p9.txt"; cell 9_brief_path 9 "$L" QA989_BRIEF="$B" QA989_PROMPT="$W/p9.txt"
h=9d0e2016ae60658ec908ee5e500583fd3a318c8a
sed "s/$h/${h:0:20}XXXXXXXXXXXXXXXXXXXX/g" "$P" > "$W/p20.txt"; cell 20_sha_prompt 20 "$L" QA989_BRIEF="$B" QA989_PROMPT="$W/p20.txt"
sed "s/$h/${h:0:20}XXXXXXXXXXXXXXXXXXXX/g" "$B" > "$W/b20.md"; cell 20_sha_brief 20 "$L" QA989_BRIEF="$W/b20.md" QA989_PROMPT="$P"
sed 's/MAIL YOUR VERDICT/SEND YOUR VERDICT/' "$P" > "$W/p12.txt"; cell 12_mail 12 "$L" QA989_BRIEF="$B" QA989_PROMPT="$W/p12.txt"
sed 's/NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout/never push/' "$P" > "$W/p11.txt"; cell 11_push 11 "$L" QA989_BRIEF="$B" QA989_PROMPT="$W/p11.txt"
sed 's/no memory maintenance/no memory upkeep/' "$P" > "$W/p14.txt"; cell 14_memory 14 "$L" QA989_BRIEF="$B" QA989_PROMPT="$W/p14.txt"
sed 's/NEVER print a credential value/never show a secret/' "$P" > "$W/p17.txt"; cell 17_credential 17 "$L" QA989_BRIEF="$B" QA989_PROMPT="$W/p17.txt"
# 21 — headless launch refuses (the TTY guard); 16 — overrides set on a real launch under a pty; 3 — real launch, not installed
MODE=launch cell 21_headless_launch 21 "$L" $OV
if command -v script > /dev/null 2>&1; then MODE=pty cell 16_override_under_pty 16 "$L" $OV; else echo "SKIP 16 (no script(1) for a pty) — INCONCLUSIVE"; fi
MODE=launch cell 3c_real_launch_not_installed 3 "$L"
# raw control-byte census over the deliverables + a synthetic NUL control
for f in "$L" "$B" "$P" "$O/gen_launcher_989.py" "$O/controls_check.sh" "$O/redproof.sh"; do
  [ -f "$f" ] || continue
  n=$(python3 -c "import sys;b=open(sys.argv[1],'rb').read();print(sum(1 for x in b if (x<0x20 and x not in (9,10,13)) or x==0x7f))" "$f")
  [ "$n" = 0 ] && echo "ok   control-bytes 0 in $(basename "$f")" || { echo "FAIL control-bytes $n in $f"; FAILS=$((FAILS+1)); }
done
printf 'abc\0def' > "$W/nul.ctl"; n=$(python3 -c "import sys;b=open(sys.argv[1],'rb').read();print(sum(1 for x in b if (x<0x20 and x not in (9,10,13)) or x==0x7f))" "$W/nul.ctl"); [ "$n" = 1 ] && echo "ok   control-byte census positive control = 1" || { echo "FAIL census control"; FAILS=$((FAILS+1)); }
bash -n "$L" && echo "ok   bash -n" || { echo "FAIL bash -n"; FAILS=$((FAILS+1)); }
# every declared exit code fired?
for want in 0 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21; do
  case " $FIRED " in *" $want "*) ;; *) echo "FAIL exit $want never fired"; FAILS=$((FAILS+1));; esac
done
SHA1="$(shasum -a 256 "$L" | cut -c1-16)"; [ "$SHA0" = "$SHA1" ] && echo "ok   launcher sha unchanged $SHA1" || { echo "FAIL launcher sha changed $SHA0 -> $SHA1"; FAILS=$((FAILS+1)); }
echo "fired:$FIRED"
echo "FAILS=$FAILS $(date '+%H:%M:%S')"
exit $((FAILS > 0))
