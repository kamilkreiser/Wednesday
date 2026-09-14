#!/bin/bash
# redproof.sh (ROUND 3) — every declared exit code of launch_qa_secuura_805_ks726.sh fires at least once, the pass path
# returns 0 on the LIVE develop, the develop-moved arms (DISJOINT -> 0; ALLOWED by blob -> 0; GUARDED by path -> 18;
# GUARDED by blob -> 18; GUARDED via an ABSENT-pinned path that is present -> 18; UNJUDGEABLE not-ahead -> 18;
# UNJUDGEABLE over the compare cap -> 18), the LANDED arms (19 by blob; 19 via the ABSENT token declared landed), the
# headless-TTY arm (21) and the override-on-launch arm (16, under a pty). Cells that need a different pin edit a COPY
# of the launcher in the work dir (never the deliverable); the deliverable's sha256 is asserted unchanged at the end.
# Work dir: mktemp -d under the gate set (never deleted; quarantine by name).
#
# Re-pinned from round 2's redproof.sh for the round-3 head a4d182bf9 and the round-3 JUDGED table (anchorSubmission.ts's
# own/landed blob is now d3ad106d8, not round 2's 7879a6ba1; confirmation.ts is now a judged path with its own landed
# blob 5690eb24f; a fourth ABSENT-pinned path joins — ks726-gate-f1-unreachable-chain.test.ts). M44/M45/M43/P728 are
# fixed historical commits, unaffected by this round, and are re-used unchanged; DEV0 (the develop-at-draft pin) moves
# from round 2's M46 to round 3's current develop 0f37b85c8 — 14 commits past M44, still disjoint from every guarded
# path (re-verified against the LIVE develop at redproof time, same as round 2's pattern).
set -u
O='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-15_gate805r3'
L="$O/launch_qa_secuura_805_ks726.sh"
B="$O/2026-09-15_secuura-805-ks726-tier1-r3.md"
P="$O/2026-09-15_secuura-805-ks726-tier1-r3.prompt.txt"
W="$(mktemp -d "$O/redproof.XXXXXX")"
SHA0="$(shasum -a 256 "$L" | cut -c1-16)"
echo "redproof (round 3) $(date '+%H:%M:%S %Z') work dir $W launcher sha $SHA0"
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
OV="QA805_BRIEF=$B QA805_PROMPT=$P"
DEV0='0f37b85c80b65d742a01e6529ee8194317a7cc57'; M44='346b491f27fb1cbf4d72cc1c86d417d0252a5f84'; M45='852e1fff773bd358170c11334d59496f05fdd8a7'
M43='250ca38fdd7c8d562d6497123f9514d6d48725af'; HEADSHA='a4d182bf9efaa5b19b74c4a861f22746491e91b4'; P728='a45204ac9ea101e6a26b393f1453529f3e278ee3'
# 0 — the pass path on the scratch set, against the LIVE develop (whatever it reads at redproof time)
cell 0_pass 0 "$L" $OV
grep -q 'origin develop MOVED' "$W/0_pass.out" && echo "     (0_pass exercised a develop-MOVED arm: $(grep -o 'MOVED [0-9a-f]* -> [0-9a-f]*: commits=[0-9]* files=[0-9]*' "$W/0_pass.out"))"
grep -q 'origin develop still' "$W/0_pass.out" && echo "     (0_pass: develop still at the draft pin — the MOVED arms are exercised by cells 3m/3a below)"
grep -q 'ks726-write-ahead-tx-hash.test.ts ABSENT = absent on develop' "$W/0_pass.out" && grep -q 'ks726-gate-f1-unreachable-chain.test.ts ABSENT = absent on develop' "$W/0_pass.out" && echo "     (0_pass: all FOUR added files judged ABSENT on develop, as pinned — round 2's three + round 3's new one)" || { echo "FAIL 0_pass did not judge the four added files ABSENT"; FAILS=$((FAILS+1)); }
# 2/3/4/5 — presence guards
sed "s#^QA_DIR=.*#QA_DIR='/nonexistent/qa'#" "$L" > "$W/l2.sh"; cell 2_qa_dir_missing 2 "$W/l2.sh" $OV
cell 3_brief_missing 3 "$L" QA805_BRIEF=/nonexistent/brief.md QA805_PROMPT="$P"
cell 3b_brief_not_installed 3 "$L"
cell 4_prompt_missing 4 "$L" QA805_BRIEF="$B" QA805_PROMPT=/nonexistent/p.txt
sed "s#^REPO=.*#REPO='/nonexistent/repo'#" "$L" > "$W/l5.sh"; cell 5_repo_missing 5 "$W/l5.sh" $OV
# 6 — the head moved / a real SHA at the wrong branch (current develop's SHA is not at the ks-726 branch)
cell 6_head_moved 6 "$L" $OV QA805_HEAD="$DEV0"
# 10 — the compare on its own assertion (the expected string mutated in a copy) + the merge-base var moved to M45
sed 's#"$MERGE_BASE ahead=8 files=11" \] ||#"$MERGE_BASE ahead=9 files=11" ] ||#' "$L" > "$W/l10a.sh"; grep -q 'ahead=9 files=11' "$W/l10a.sh" || echo "FAIL 10a sed did not land"; cell 10a_compare_ahead 10 "$W/l10a.sh" $OV
sed "s#^MERGE_BASE='$M44'#MERGE_BASE='$M45'#" "$L" > "$W/l10b.sh"; grep -q "MERGE_BASE='$M45'" "$W/l10b.sh" || echo "FAIL 10b sed did not land"; cell 10b_merge_base_M45 10 "$W/l10b.sh" $OV
# 13 — the compare unreadable (an empty env file: no GH_TOKEN)
: > "$W/empty.env"; sed "s#^SECUURA_ENV=.*#SECUURA_ENV='$W/empty.env'#" "$L" > "$W/l13.sh"; cell 13_compare_unreadable 13 "$W/l13.sh" $OV
# 18a — GUARDED blob: develop's anchorSubmission.ts OK-blob mis-pinned in a copy (unaffected by round 3 — anchorSubmission.ts's
# develop-OK blob is STILL M44's, only its own/landed blob changed this round)
sed 's#"66fa7e6f759284c2d96ca07fb53995e71b6c5f6b": "M44"#"0000000000000000000000000000000000000000": "nobody"#' "$L" > "$W/l18a.sh"
grep -q '"0000000000000000000000000000000000000000": "nobody"' "$W/l18a.sh" || echo "FAIL 18a sed did not land"
cell 18a_guarded_blob 18 "$W/l18a.sh" $OV
grep -q 'GUARDED develop services/anchoring/src/anchorSubmission.ts' "$W/18a_guarded_blob.out" || { echo "FAIL 18a did not name anchorSubmission.ts"; FAILS=$((FAILS+1)); }
# 18b — GUARDED path: the pinned develop moved to M43 (unaffected historical commit): its delta to the CURRENT live
# develop (re-verified 2026-09-15: ahead=15, files=96) touches exactly ONE guarded path, the yaml (develop's own blob
# d327a249a, which the allow-list does NOT carry at this pin) -> GUARDED names the yaml -> 18. This cell is also the
# CONTROL for 3a below (the same pin with the allow-list re-pointed clears it).
sed "s#^DEVELOP_SHA='$DEV0'#DEVELOP_SHA='$M43'#" "$L" > "$W/l18b.sh"; grep -q "DEVELOP_SHA='$M43'" "$W/l18b.sh" || echo "FAIL 18b sed did not land"
cell 18b_guarded_path_M43_yaml 18 "$W/l18b.sh" $OV
grep -q 'GUARDED Blockchain/Dev/docs/openapi/secuura-api.yaml' "$W/18b_guarded_path_M43_yaml.out" || { echo "FAIL 18b did not name the yaml in the GUARDED line"; FAILS=$((FAILS+1)); }
# 18c — UNJUDGEABLE: develop pinned at a SHA that is NOT an ancestor of the live develop (the #805 round-3 head itself:
# status diverged, re-verified 2026-09-15: ahead=14 behind=8 files=92) -> 18
sed "s#^DEVELOP_SHA='$DEV0'#DEVELOP_SHA='$HEADSHA'#" "$L" > "$W/l18c.sh"; cell 18c_unjudgeable_not_ahead 18 "$W/l18c.sh" $OV
grep -q 'UNJUDGEABLE status=diverged' "$W/18c_unjudgeable_not_ahead.out" || { echo "FAIL 18c did not print UNJUDGEABLE status=diverged"; FAILS=$((FAILS+1)); }
# 18d — UNJUDGEABLE over the compare cap: develop pinned at the parent of #728 (unaffected historical commit): re-verified
# 2026-09-15 ahead=150 (was 140 at round 2), the API caps files at exactly 300 > 250 -> UNJUDGEABLE -> 18 (unchanged cap)
sed "s#^DEVELOP_SHA='$DEV0'#DEVELOP_SHA='$P728'#" "$L" > "$W/l18d.sh"; cell 18d_unjudgeable_over_cap 18 "$W/l18d.sh" $OV
grep -q 'UNJUDGEABLE status=ahead files=300' "$W/18d_unjudgeable_over_cap.out" || { echo "FAIL 18d did not print UNJUDGEABLE files=300"; FAILS=$((FAILS+1)); }
# 18e — GUARDED via an ABSENT-pinned path that is PRESENT: reconciler.ts pinned ABSENT-only in a copy -> its develop blob
# is "a version nobody pinned" -> 18. Round 3 has FOUR ABSENT-pinned paths already (the three round-2 ADDED files + the
# new ks726-gate-f1-unreachable-chain.test.ts) — this sed adds a fifth, so the positive control below is 5, not round 2's 4.
sed 's#({"dc65347f63b7e754acc370396d49569810aa7e9c": "M44"}, {"55e2fe6949bc0e1c200e4ea314bd5262e2886bca": "\#805 own"})#({"ABSENT": "absent on develop"}, {"55e2fe6949bc0e1c200e4ea314bd5262e2886bca": "\#805 own"})#' "$L" > "$W/l18e.sh"
grep -c '"ABSENT": "absent on develop"' "$W/l18e.sh" | grep -q '^5$' || echo "FAIL 18e sed did not land (expect 5 ABSENT pins: round 3's four + this sed's one)"
cell 18e_guarded_absent_pinned_but_present 18 "$W/l18e.sh" $OV
grep -q 'GUARDED develop services/anchoring/src/reconciler.ts blob dc65347f6' "$W/18e_guarded_absent_pinned_but_present.out" || { echo "FAIL 18e did not name reconciler.ts"; FAILS=$((FAILS+1)); }
# 19a — LANDED: develop's anchorSubmission.ts blob declared as #805's round-3 OWN blob (d3ad106d8 — the two blob strings
# swapped in a copy; round 2's stale 7879a6ba1 is NOT this round's own blob and would prove nothing)
sed 's#{"66fa7e6f759284c2d96ca07fb53995e71b6c5f6b": "M44"}, {"d3ad106d8e5764a526456b3218e1e8d9ad1a38ba": "\#805 own (round 3)"}#{"d3ad106d8e5764a526456b3218e1e8d9ad1a38ba": "x"}, {"66fa7e6f759284c2d96ca07fb53995e71b6c5f6b": "\#805 landed (sim)"}#' "$L" > "$W/l19a.sh"
grep -q '"66fa7e6f759284c2d96ca07fb53995e71b6c5f6b": "#805 landed (sim)"' "$W/l19a.sh" || echo "FAIL 19a sed did not land"
cell 19a_landed_by_blob 19 "$W/l19a.sh" $OV
# 19b — LANDED via the ABSENT token: round 3's OWN new file (ks726-gate-f1-unreachable-chain.test.ts)'s 404 declared as
# "#805 landed" in a copy -> 19 (the ABSENT state reaches the LANDED branch when so pinned — proves the round-3 addition
# to the JUDGED table wires into the same mechanism as round 2's three)
sed 's#({"ABSENT": "absent on develop"}, {"82058c305ffaf375ef7941351063d4f236f878b9": "\#805 own (round 3, new)"})#({"82058c305ffaf375ef7941351063d4f236f878b9": "x"}, {"ABSENT": "\#805 landed (sim-absent)"})#' "$L" > "$W/l19b.sh"
grep -q '"ABSENT": "#805 landed (sim-absent)"' "$W/l19b.sh" || echo "FAIL 19b sed did not land"
cell 19b_landed_via_absent 19 "$W/l19b.sh" $OV
grep -q 'ks726-gate-f1-unreachable-chain.test.ts blob ABSENT = #805 landed (sim-absent)' "$W/19b_landed_via_absent.out" || { echo "FAIL 19b did not route the ABSENT token to LANDED"; FAILS=$((FAILS+1)); }
# 3m — the develop-MOVED DISJOINT arm with an explicit pin: M45 (unaffected historical commit; its delta to the CURRENT
# live develop is now ahead=13 files=90, none guarded — re-verified 2026-09-15, larger than round 2's 4 files because
# develop has moved much further, but still disjoint) -> 0 with the MOVED note
sed "s#^DEVELOP_SHA='$DEV0'#DEVELOP_SHA='$M45'#" "$L" > "$W/l3m.sh"; cell 3m_develop_moved_disjoint_M45 0 "$W/l3m.sh" $OV
grep -q "origin develop MOVED $M45" "$W/3m_develop_moved_disjoint_M45.out" && grep -q 'disjoint from the GUARDED list' "$W/3m_develop_moved_disjoint_M45.out" || { echo "FAIL 3m did not print the MOVED-disjoint note"; FAILS=$((FAILS+1)); }
# 3a — the ALLOWED-by-blob arm: no SHA on origin carries #922's blobs until #922 squashes (re-confirmed 2026-09-15: the
# yaml on current develop is still M44's), so the CLEARING logic is proven the other way round: pin develop at M43
# (18b's pin: the delta's ONLY guarded hit is the yaml at d327a249a) and re-point DEV_CONTENT_ALLOWED's yaml entry at
# THAT blob -> the hit is CLEARED, nothing remains -> rc 0 with the "cleared BY BLOB" note naming secuura-api.yaml.
# 18b is the control that the clearing did something (same pin, allow-list untouched -> 18).
sed -e "s#^DEVELOP_SHA='$DEV0'#DEVELOP_SHA='$M43'#" -e 's#"19f6a41933d4842c88f1ac66f913cab54c0cd0a4",#"d327a249a2ef7261b685d1baeb6aec3c9f7b677d",#' "$L" > "$W/l3a.sh"
grep -q '"d327a249a2ef7261b685d1baeb6aec3c9f7b677d",' "$W/l3a.sh" || echo "FAIL 3a sed did not land"
cell 3a_allowed_by_blob_M43_yaml_cleared 0 "$W/l3a.sh" $OV
grep -q 'cleared BY BLOB under guarded paths: secuura-api.yaml' "$W/3a_allowed_by_blob_M43_yaml_cleared.out" && echo "     (3a: the yaml hit CLEARED by blob; 18b is its control — the same pin without the re-pointed entry refused on the yaml)" || { echo "FAIL 3a did not print the cleared-by-blob note"; FAILS=$((FAILS+1)); }
# 7/15/8/9/20/12/11/14/17 — brief / prompt content guards (edited copies of the brief / prompt)
sed 's/TIER 1/TIER 2/g' "$B" > "$W/b7.md"; cell 7_tier 7 "$L" QA805_BRIEF="$W/b7.md" QA805_PROMPT="$P"
sed 's/ROUND 3/ROUND THREE/g' "$P" > "$W/p15.txt"; cell 15_round_missing 15 "$L" QA805_BRIEF="$B" QA805_PROMPT="$W/p15.txt"
sed '1s/ultrathink/think/' "$P" > "$W/p8.txt"; cell 8_ultrathink 8 "$L" QA805_BRIEF="$B" QA805_PROMPT="$W/p8.txt"
sed 's#/briefs/2026-09-15_secuura-805-ks726#/briefs/2026-09-15_secuura-80X-ks726#' "$P" > "$W/p9.txt"; cell 9_brief_path 9 "$L" QA805_BRIEF="$B" QA805_PROMPT="$W/p9.txt"
h="$HEADSHA"
sed "s/$h/${h:0:20}XXXXXXXXXXXXXXXXXXXX/g" "$P" > "$W/p20.txt"; cell 20_sha_prompt 20 "$L" QA805_BRIEF="$B" QA805_PROMPT="$W/p20.txt"
sed "s/$h/${h:0:20}XXXXXXXXXXXXXXXXXXXX/g" "$B" > "$W/b20.md"; cell 20_sha_brief 20 "$L" QA805_BRIEF="$W/b20.md" QA805_PROMPT="$P"
sed 's/MAIL YOUR VERDICT/SEND YOUR VERDICT/' "$P" > "$W/p12.txt"; cell 12_mail 12 "$L" QA805_BRIEF="$B" QA805_PROMPT="$W/p12.txt"
sed 's/NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout/never push/' "$P" > "$W/p11.txt"; cell 11_push 11 "$L" QA805_BRIEF="$B" QA805_PROMPT="$W/p11.txt"
sed 's/no memory maintenance/no memory upkeep/' "$P" > "$W/p14.txt"; cell 14_memory 14 "$L" QA805_BRIEF="$B" QA805_PROMPT="$W/p14.txt"
sed 's/NEVER print a credential value/never show a secret/' "$P" > "$W/p17.txt"; cell 17_credential 17 "$L" QA805_BRIEF="$B" QA805_PROMPT="$W/p17.txt"
# 21 — headless launch refuses (the TTY guard); 16 — overrides set on a real launch under a pty; 3 — real launch, not installed
MODE=launch cell 21_headless_launch 21 "$L" $OV
if command -v script > /dev/null 2>&1; then MODE=pty cell 16_override_under_pty 16 "$L" $OV; else echo "SKIP 16 (no script(1) for a pty) — INCONCLUSIVE"; fi
MODE=launch cell 3c_real_launch_not_installed 3 "$L"
# raw control-byte census over the deliverables + a synthetic NUL control
for f in "$L" "$B" "$P" "$O/gen_launcher_805.py" "$O/controls_check.sh" "$O/redproof.sh"; do
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
