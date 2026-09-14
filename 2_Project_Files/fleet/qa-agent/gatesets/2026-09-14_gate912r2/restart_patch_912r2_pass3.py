#!/usr/bin/env python3
"""restart_patch_912r2_pass3.py -- pass-3 narrative insertion into the brief AND prompt, per Wednesday's
2026-09-14 13:2x AEST instruction: fold M29 (KS-780/#985) into the DEV_CONTENT_ALLOWED content-judged guard and
the predicted-by: drafter suite-count predictions. Asserted substitution: each anchor must occur exactly once."""
import hashlib, sys

BRIEF = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.prompt.txt'

BRIEF_ANCHOR = "unaffected by any of this arithmetic.**\n"
BRIEF_INSERT = (
    "- **Pass 3 update, predicted-by: drafter (Wednesday 2026-09-14 13:2x AEST instruction): develop moved on to "
    "M29 commit 4569dd88968fe949b3682512e457a0aec5fc4469, KS-780/#985 stacked on #799, normaliseOrgId consolidated "
    "into @secuura/shared. git diff --name-status 13b19d443 4569dd889 names SEVEN files; FOUR sit under the "
    "GUARDED prefixes (services/originate/src/__tests__/ks695-erasure-by-external-ref.test.ts, services/"
    "originate/src/__tests__/ks780-org-id-is-the-shared-implementation.test.ts, services/originate/src/services/"
    "orgId.ts, packages/shared/src/__tests__/ks780-normalise-org-id-one-implementation.test.ts); the other three "
    "(packages/shared/src/index.ts, packages/shared/src/security/keyRevokePolicy.ts, packages/shared/src/"
    "security/orgId.ts) are not under packages/shared's guarded __tests__/ subtree and are not hits. All four "
    "guarded blobs cleared into the launcher's DEV_CONTENT_ALLOWED dict, verified live two ways (git rev-parse "
    "against 4569dd889 in the checkout, cross-checked against the GitHub compare API per-file sha) -- live "
    "--check now reads rc 0 through M29, M30 (#925, disjoint) and M31 (#983, disjoint) without further edits. "
    "UPDATED PREDICTIONS supersede pass 2's separate #912/#937 figures: Wednesday's own M20-to-M29 cumulative "
    "arithmetic gives originate = 57 suites / 601 cells (M20's 55/588 +2 suites/+13 tests) and packages/shared = "
    "43 files / 835 tests (M20's 40/813 +3 files/+22 tests), both stated on the merged tree. These remain "
    "PREDICTIONS ONLY -- re-derive them yourself on your own clone/farm before judging the ratio; a mismatch is a "
    "BRIEF ERROR to name, NOT a finding against the PR.**\n"
)

PROMPT_ANCHOR = "against the PR.\n"
PROMPT_INSERT = (
    "  Pass 3 update (predicted-by: drafter): develop moved to M29 (KS-780/#985, stacked on #799) then M30/M31\n"
    "  (disjoint). Four more guarded-prefix paths cleared by blob into DEV_CONTENT_ALLOWED (originate ks695/\n"
    "  ks780 tests, originate services/orgId.ts, packages/shared ks780 test) -- live --check reads rc 0 through\n"
    "  M31. UPDATED predictions supersede pass 2's: originate = 57/601, packages/shared = 43/835, both on the\n"
    "  merged tree per Wednesday's own M20-to-M29 arithmetic. Still predictions only -- re-derive before judging.\n"
)

def patch(path, anchor, insert, label):
    src = open(path, encoding='utf-8').read()
    before_hash = hashlib.sha256(src.encode()).hexdigest()[:16]
    n = src.count(anchor)
    if n != 1:
        print(f"REFUSING {label}: anchor occurs {n} times (expected 1)"); sys.exit(1)
    idx = src.index(anchor) + len(anchor)
    out = src[:idx] + insert + src[idx:]
    open(path, 'w', encoding='utf-8').write(out)
    after_hash = hashlib.sha256(out.encode()).hexdigest()[:16]
    print(f"{label}: {before_hash} -> {after_hash}  bytes {len(src)} -> {len(out)} (+{len(out)-len(src)})")

patch(BRIEF, BRIEF_ANCHOR, BRIEF_INSERT, "brief")
patch(PROMPT, PROMPT_ANCHOR, PROMPT_INSERT, "prompt")
