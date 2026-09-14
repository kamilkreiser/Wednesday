#!/usr/bin/env python3
"""restart_patch_L9.py — surgical, asserted append of the M20 develop-move observation to the L9 brief and
prompt. Does NOT touch DEVELOP_SHA / CMP_WANT / BASE_940_941 / the controls_check.sh DEV pin, because those
are verified (git merge-base, live --check) to be CORRECT UNCHANGED at M18 — see BUILD_REPORT.md 'Pins'.
Each anchor's occurrence count is asserted before AND after; any mismatch aborts with no write."""
import hashlib, sys

def sha16(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()[:16]

def assert_count(text, needle, want, label):
    got = text.count(needle)
    if got != want:
        print(f"REFUSING: {label} count {got} != expected {want}"); sys.exit(1)

BRIEF = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.md"
PROMPT = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gateL9/2026-09-14_secuura-L9-940-941-942-887-ks1075-1077-1078-961-tier2.prompt.txt"

# ---- brief ----
b = open(BRIEF).read()
b_sha0 = sha16(BRIEF)
anchor_b = "- origin develop MOVED 8861e6216 -> 6e78961e1 (#982's squash, 2026-09-13T23:00:09Z; compare M18...M19 ahead 1, 3 files all under Blockchain/Dev/services/auth/src/ — oauth.ts +23 -5, ks790 test +249, ks820-821 test +8; refs/pull/982/head still e62eab87a; the four lane heads unmoved) | git ls-remote + /branches/develop + /compare by the drafter 09:03:36 AEST (lsremote_2.out); the launcher's own --check at 09:02 printed the move as disjoint (redproof cell 0) | read 2026-09-14\n"
assert_count(b, anchor_b, 1, "brief M19 provenance line")
addition_b = "- origin develop MOVED FURTHER 6e78961e1 -> a5334350221c819f54d4a20a3308daeb9ca09617 (#903/KS-991 r2's squash \"skip a local develop that origin/develop provably supersedes\", 2026-09-13T23:18:09Z = 09:18:09 AEST; compare M19...M20 ahead 1, 3 files — .githooks/pre-push +39 -1, Blockchain/Dev/scripts/__tests__/pre_push_hook_base.test.sh +123 -1, Blockchain/Dev/scripts/preflight/preflight.sh +24; M18...M20 total = 2 commits / 6 files, NONE under the eight GUARDED paths or the three judged workflow blobs (security-scan.yml / pr-security-gates.yml / pr-platform-suites.yml unchanged M18==M20, confirmed by contents-API re-read); the four lane heads unmoved; git merge-base of #942 and #887 against M20 independently re-verified = 8861e6216 UNCHANGED — #942's own head IS a --no-ff merge of M18 (parents c1676269d + 8861e6216) and #887's parent de376a9f1 likewise merges M18, so this cannot move while their branches are unrebased; DEVELOP_SHA / CMP_WANT / the controls_check.sh DEV pin are therefore left at M18, asserted correct rather than substituted) | git ls-remote + git diff --numstat by the restart drafter 11:39:21-11:46:xx AEST (lsremote_3.out, m19_m20_diff.out); the launcher's own --check re-run 11:45:48 AEST printed the move as disjoint (\"commits=2 files=6 (.test.sh files 1) — disjoint from the three judged files (by blob) and the eight GUARDED paths\"; check.out, redproof cell 0) | read 2026-09-14\n"
b2 = b.replace(anchor_b, anchor_b + addition_b, 1)
assert_count(b2, addition_b, 1, "brief M20 addition (post)")
open(BRIEF, "w").write(b2)
b_sha1 = sha16(BRIEF)
print(f"brief: {b_sha0} -> {b_sha1}; +1 line ({len(addition_b)} bytes)")

# ---- prompt ----
p = open(PROMPT).read()
p_sha0 = sha16(PROMPT)
anchor_p = "the lane's files). develop MOVED to M19 6e78961e1 (#982's squash) at 09:00 AEST — 3 files under services/auth/, DISJOINT;"
assert_count(p, anchor_p, 1, "prompt M19 sentence")
addition_p = " develop MOVED FURTHER to M20 a5334350 (#903's squash) at 09:18 AEST — 3 files under .githooks/ and scripts/preflight+__tests__/, DISJOINT (re-observed live by the restart drafter 11:4x AEST, --check re-run rc 0);"
p2 = p.replace(anchor_p, anchor_p + addition_p, 1)
assert_count(p2, addition_p, 1, "prompt M20 addition (post)")
open(PROMPT, "w").write(p2)
p_sha1 = sha16(PROMPT)
print(f"prompt: {p_sha0} -> {p_sha1}; +1 sentence ({len(addition_p)} bytes)")
