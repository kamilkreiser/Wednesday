#!/bin/bash
# redproof.sh — every declared exit code of launch_qa_secuura_873_ks931.sh fires at least once, the pass path returns 0
# on the LIVE develop (which has ALREADY moved past the M46 pin — so the pass path itself exercises the MOVED-disjoint
# content arm), the develop-moved arms (DISJOINT -> 0; ALLOWED by blob -> the cleared files vanish from the GUARDED line;
# GUARDED -> 18; UNJUDGEABLE -> 18), the LANDED arm (19), the headless-TTY arm (21) and the override-on-launch arm (16,
# under a pty). Cells that need a different pin edit a COPY of the launcher in the work dir (never the deliverable); the
# deliverable's sha256 is asserted unchanged at the end. Work dir: mktemp -d under the gate set (never deleted; quarantine
# by name). Pins were read 20:57 AEST (redproof_pins_read.out) against the live tip 311988614:
#   250ca38fd (= 346b491f2^): delta to live = 10 files, 0 guarded hits -> the explicit DISJOINT arm (3m)
#   13b19d443 (= 4569dd889^): delta to live = 66 files, guarded hits under packages/shared/ (orgId.ts, keyRevokePolicy.ts,
#              index.ts, the ks780 test) + the originate ks914 test + helpers/sharedModuleMock.ts -> GUARDED (18b); with the
#              allow-list re-pointed at orgId.ts a42d7783d + the ks780 test e3aa932f7 (their LIVE blobs) those two clear and
#              the others remain -> still 18 but the GUARDED line must not name them (3a); the same pin without the
#              re-pointing names orgId.ts (3b, the control that the clearing did something)
set -u
O='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate873'
L="$O/launch_qa_secuura_873_ks931.sh"
B="$O/2026-09-14_secuura-873-ks931-tier1-r1.md"
P="$O/2026-09-14_secuura-873-ks931-tier1-r1.prompt.txt"
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
OV="QA873_BRIEF=$B QA873_PROMPT=$P"
M46='bc067e3e91821116f3344b2aa5a1d7a5cc968d18'
# 0 — the pass path on the scratch set, against the LIVE develop (already past M46: the MOVED-disjoint arm fires here)
cell 0_pass 0 "$L" $OV
grep -q 'origin develop MOVED' "$W/0_pass.out" && echo "     (0_pass exercised a develop-MOVED arm: $(grep -o 'MOVED [0-9a-f]* -> [0-9a-f]*: commits=[0-9]* files=[0-9]*' "$W/0_pass.out"))"
grep -q 'origin develop still' "$W/0_pass.out" && echo "     (0_pass: develop still M46 — the MOVED arms are exercised by cells 3m/3a below)"
grep -q 'origin develop MOVED\|origin develop still' "$W/0_pass.out" || { echo "FAIL 0_pass printed neither a MOVED nor a still note"; FAILS=$((FAILS+1)); }
# 2/3/4/5 — presence guards
sed "s#^QA_DIR=.*#QA_DIR='/nonexistent/qa'#" "$L" > "$W/l2.sh"; cell 2_qa_dir_missing 2 "$W/l2.sh" $OV
cell 3_brief_missing 3 "$L" QA873_BRIEF=/nonexistent/brief.md QA873_PROMPT="$P"
cell 3b_brief_not_installed 3 "$L"
cell 4_prompt_missing 4 "$L" QA873_BRIEF="$B" QA873_PROMPT=/nonexistent/p.txt
sed "s#^REPO=.*#REPO='/nonexistent/repo'#" "$L" > "$W/l5.sh"; cell 5_repo_missing 5 "$W/l5.sh" $OV
# 6 — the head moved / a real SHA at the wrong branch (develop M46's SHA is not at the ks-931 branch)
cell 6_head_moved 6 "$L" $OV QA873_HEAD="$M46"
# 10 — the compare on its own assertion (the expected string moved in a copy) + the merge-base var moved to M46
sed 's#"$MERGE_BASE ahead=2 files=2" \] ||#"$MERGE_BASE ahead=3 files=2" ] ||#' "$L" > "$W/l10a.sh"; grep -q 'ahead=3 files=2' "$W/l10a.sh" || echo "FAIL 10a sed did not land"; cell 10a_compare_ahead 10 "$W/l10a.sh" $OV
sed "s#^MERGE_BASE='852e1fff773bd358170c11334d59496f05fdd8a7'#MERGE_BASE='$M46'#" "$L" > "$W/l10b.sh"; grep -q "^MERGE_BASE='$M46'" "$W/l10b.sh" || echo "FAIL 10b sed did not land"; cell 10b_merge_base_M46 10 "$W/l10b.sh" $OV
# 13 — the compare unreadable (an empty env file: no GH_TOKEN)
: > "$W/empty.env"; sed "s#^SECUURA_ENV=.*#SECUURA_ENV='$W/empty.env'#" "$L" > "$W/l13.sh"; cell 13_compare_unreadable 13 "$W/l13.sh" $OV
# 18a — GUARDED blob: develop's ssrf-guard.ts blob declared "a version nobody pinned" (the OK blob mis-pinned in a copy)
sed 's#"a1203248f913ceeb677c0ca39fb1a5ead081e852": "M46"#"0000000000000000000000000000000000000000": "nobody"#' "$L" > "$W/l18a.sh"
grep -q '"0000000000000000000000000000000000000000": "nobody"' "$W/l18a.sh" || echo "FAIL 18a sed did not land"
cell 18a_guarded_blob 18 "$W/l18a.sh" $OV
grep -q 'GUARDED develop' "$W/18a_guarded_blob.out" || { echo "FAIL 18a did not print the GUARDED-blob line"; FAILS=$((FAILS+1)); }
# 18b — GUARDED path: the pinned develop moved to 13b19d443, whose delta to the live develop (66 files) touches
# packages/shared/ (orgId.ts, keyRevokePolicy.ts, index.ts, the ks780 test) + the originate ks914 test + helpers/.
# NOTE: the JUDGED-blob pass (a) reads the LIVE develop, so it passes; the compare (b) is what refuses.
sed "s#^DEVELOP_SHA='$M46'#DEVELOP_SHA='13b19d443'#" "$L" > "$W/l18b.sh"; grep -q "^DEVELOP_SHA='13b19d443'" "$W/l18b.sh" || echo "FAIL 18b sed did not land"
cell 18b_guarded_path_ks780parent_pin 18 "$W/l18b.sh" $OV
grep -q 'GUARDED' "$W/18b_guarded_path_ks780parent_pin.out" && grep -q 'orgId.ts' "$W/18b_guarded_path_ks780parent_pin.out" || { echo "FAIL 18b did not print GUARDED naming orgId.ts"; FAILS=$((FAILS+1)); }
# 18c — UNJUDGEABLE: develop pinned at a SHA that is NOT an ancestor of the live develop (the #873 head itself: status diverged) -> 18
sed "s#^DEVELOP_SHA='$M46'#DEVELOP_SHA='c624c9a8dd24129dad46cf7a204ae75ecb875dc3'#" "$L" > "$W/l18c.sh"; cell 18c_unjudgeable_not_ahead 18 "$W/l18c.sh" $OV
grep -q 'UNJUDGEABLE' "$W/18c_unjudgeable_not_ahead.out" || { echo "FAIL 18c did not print UNJUDGEABLE"; FAILS=$((FAILS+1)); }
# 19 — LANDED: develop's ssrf-guard.ts blob declared as #873's own (the two blob strings swapped in a copy)
sed 's#{"a1203248f913ceeb677c0ca39fb1a5ead081e852": "M46"}, {"5a838e0d6440b371ab7ffa27ea1ec4ea878db150": "\#873 own"}#{"5a838e0d6440b371ab7ffa27ea1ec4ea878db150": "x"}, {"a1203248f913ceeb677c0ca39fb1a5ead081e852": "\#873 landed (sim)"}#' "$L" > "$W/l19.sh"
grep -q '"a1203248f913ceeb677c0ca39fb1a5ead081e852": "#873 landed (sim)"' "$W/l19.sh" || echo "FAIL 19 sed did not land"
cell 19_landed 19 "$W/l19.sh" $OV
# 3m — the develop-MOVED DISJOINT arm explicitly: pin 250ca38fd (its delta to the live develop = 10 files, none under a
# guarded path — the #813 / #879 / #874 / #811 / #943 squashes) -> 0 with the MOVED note naming that pin
sed "s#^DEVELOP_SHA='$M46'#DEVELOP_SHA='250ca38fd'#" "$L" > "$W/l3m.sh"; cell 3m_develop_moved_disjoint 0 "$W/l3m.sh" $OV
grep -q 'origin develop MOVED 250ca38fd' "$W/3m_develop_moved_disjoint.out" || { echo "FAIL 3m did not print the MOVED note"; FAILS=$((FAILS+1)); }
# 3a — the ALLOWED-by-blob arm: #922 has not squashed, so no SHA on origin carries its blobs yet; the CLEARING logic is
# proven with the 18b pin instead: DEV_CONTENT_ALLOWED re-pointed (in a copy) at two files that ARE in that delta, at
# their LIVE blobs (the compare's per-file sha is the live side) — packages/shared/src/security/orgId.ts a42d7783d and
# the ks780 test e3aa932f7 (read 20:57). Those two are then CLEARED; keyRevokePolicy.ts / index.ts / the originate ks914
# test / helpers remain -> still 18, but the GUARDED line must NOT name the two cleared files.
sed -e "s#^DEVELOP_SHA='$M46'#DEVELOP_SHA='13b19d443'#" \
    -e 's#D + "packages/shared/src/__tests__/ks256-spec-example-contract.test.ts": "72533d3b01a4941578b1f777f0def3f9ec9ea6f0",#D + "packages/shared/src/security/orgId.ts": "a42d7783dfc0c44fffc2c7b8cb4f2961adc32769",#' \
    -e 's#D + "packages/shared/src/openapi/examples/fixtures.ts": "b54d26929c564d9cd4e2e2f27da12df6d6d85325",#D + "packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts": "e3aa932f76419129271cb767e3df352bf694f985",#' "$L" > "$W/l3a.sh"
grep -q '"a42d7783dfc0c44fffc2c7b8cb4f2961adc32769",' "$W/l3a.sh" && grep -q '"e3aa932f76419129271cb767e3df352bf694f985",' "$W/l3a.sh" || echo "FAIL 3a sed did not land"
cell 3a_allowed_by_blob_then_guarded_elsewhere 18 "$W/l3a.sh" $OV
if grep -q 'GUARDED' "$W/3a_allowed_by_blob_then_guarded_elsewhere.out" && ! grep -q 'orgId.ts' "$W/3a_allowed_by_blob_then_guarded_elsewhere.out" && ! grep -q 'ks780-normalise-org-id-one-implementation' "$W/3a_allowed_by_blob_then_guarded_elsewhere.out" && grep -q 'keyRevokePolicy.ts' "$W/3a_allowed_by_blob_then_guarded_elsewhere.out"; then
  echo "     (3a: the two re-pointed DEV_CONTENT_ALLOWED hits were CLEARED by blob — the GUARDED line names only other paths: $(grep -o 'GUARDED [^—]*' "$W/3a_allowed_by_blob_then_guarded_elsewhere.out" | cut -c1-200))"
else echo "FAIL 3a the cleared files still appear in the GUARDED line (or no GUARDED line / keyRevokePolicy.ts missing)"; FAILS=$((FAILS+1)); fi
# 3b — the same pin WITHOUT the allowlist re-pointed -> the GUARDED line MUST name orgId.ts (the control that 3a's clearing did something)
grep -q 'orgId.ts' "$W/18b_guarded_path_ks780parent_pin.out" && echo "     (3b control = cell 18b: without the re-pointing, orgId.ts IS named in the GUARDED line)" || { echo "FAIL 3b control: orgId.ts is not named"; FAILS=$((FAILS+1)); }
# 7/15/8/9/20/12/11/14/17 — brief / prompt content guards (edited copies of the brief / prompt)
sed 's/TIER 1/TIER 2/g' "$B" > "$W/b7.md"; cell 7_tier 7 "$L" QA873_BRIEF="$W/b7.md" QA873_PROMPT="$P"
sed 's/ROUND 1/ROUND ONE/g' "$P" > "$W/p15.txt"; cell 15_round_missing 15 "$L" QA873_BRIEF="$B" QA873_PROMPT="$W/p15.txt"
sed '1s/ultrathink/think/' "$P" > "$W/p8.txt"; cell 8_ultrathink 8 "$L" QA873_BRIEF="$B" QA873_PROMPT="$W/p8.txt"
sed 's#/briefs/2026-09-14_secuura-873-ks931#/briefs/2026-09-14_secuura-87X-ks931#' "$P" > "$W/p9.txt"; cell 9_brief_path 9 "$L" QA873_BRIEF="$B" QA873_PROMPT="$W/p9.txt"
h=c624c9a8dd24129dad46cf7a204ae75ecb875dc3
sed "s/$h/${h:0:20}XXXXXXXXXXXXXXXXXXXX/g" "$P" > "$W/p20.txt"; cell 20_sha_prompt 20 "$L" QA873_BRIEF="$B" QA873_PROMPT="$W/p20.txt"
sed "s/$h/${h:0:20}XXXXXXXXXXXXXXXXXXXX/g" "$B" > "$W/b20.md"; cell 20_sha_brief 20 "$L" QA873_BRIEF="$W/b20.md" QA873_PROMPT="$P"
sed 's/MAIL YOUR VERDICT/SEND YOUR VERDICT/' "$P" > "$W/p12.txt"; cell 12_mail 12 "$L" QA873_BRIEF="$B" QA873_PROMPT="$W/p12.txt"
grep -c -i 'MAIL YOUR VERDICT' "$P" | grep -q '^1$' && echo "     (12 positive control: the deliverable prompt carries MAIL YOUR VERDICT exactly once)" || { echo "FAIL 12 positive control: MAIL YOUR VERDICT count in the prompt is not 1"; FAILS=$((FAILS+1)); }
sed 's/NEVER run a push, the real pre-push hook, or preflight.sh inside the Secuura checkout/never push/' "$P" > "$W/p11.txt"; cell 11_push 11 "$L" QA873_BRIEF="$B" QA873_PROMPT="$W/p11.txt"
sed 's/no memory maintenance/no memory upkeep/' "$P" > "$W/p14.txt"; cell 14_memory 14 "$L" QA873_BRIEF="$B" QA873_PROMPT="$W/p14.txt"
sed 's/NEVER print a credential value/never show a secret/' "$P" > "$W/p17.txt"; cell 17_credential 17 "$L" QA873_BRIEF="$B" QA873_PROMPT="$W/p17.txt"
# 21 — headless launch refuses (the TTY guard); 16 — overrides set on a real launch under a pty; 3 — real launch, not installed
MODE=launch cell 21_headless_launch 21 "$L" $OV
if command -v script > /dev/null 2>&1; then MODE=pty cell 16_override_under_pty 16 "$L" $OV; else echo "SKIP 16 (no script(1) for a pty) — INCONCLUSIVE"; fi
MODE=launch cell 3c_real_launch_not_installed 3 "$L"
# raw control-byte census over the deliverables + a synthetic NUL control
for f in "$L" "$B" "$P" "$O/gen_launcher_873.py" "$O/controls_check.sh" "$O/redproof.sh"; do
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
