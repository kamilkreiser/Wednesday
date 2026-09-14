#!/usr/bin/env python3
"""restart_patch_912r2.py — restart/completion drafter's ONE narrative-bullet insertion into the brief AND the
prompt, documenting develop's M19->M20->M21 continuation past what the dead drafter (died ~10:36 AEST) had
observed (M19 only). Asserted substitution: anchor occurs EXACTLY once in each file before edit, refuses otherwise;
byte-length delta printed after. Same discipline as gateL9/restart_patch_L9.py and gate912r2's own dead-drafter
brief_patch scripts."""
import hashlib, sys

BRIEF = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.prompt.txt'

BRIEF_ANCHOR = "`ls-remote` again at your start — the tip may be past M19.**\n"
BRIEF_INSERT = (
    "- **Restart-drafter's close-time re-read (12:00–12:07 AEST 2026-09-14, `gh_read_close.out` + `check.out`'s "
    "fourth entry): develop moved TWICE more past M19 — M20 `a5334350221c819f54d4a20a3308daeb9ca09617` (#903's "
    "squash \"KS-991: skip a local develop that origin/develop provably supersedes\", 2026-09-14T09:18:09+10:00; "
    "`.githooks/pre-push`, `scripts/preflight/preflight.sh`, `scripts/__tests__/pre_push_hook_base.test.sh` — "
    "DISJOINT from the guarded paths, same as M19) THEN M21 `5210ddf317b2b1ed547e5d8488c3d011ceb087e1` (#799's "
    "squash \"KS-764: close the second revoke surface in originate, and bind the organisation arm to its call "
    "sites\", 2026-09-14T12:00:24+10:00 = 02:00:24Z — landed almost exactly at this restart-drafter's own first "
    "read). M18→M21 total: 3 commits, 18 files (`gh_read_close.out`). **M21 is NOT disjoint**: it lands "
    "`Blockchain/Dev/services/originate/src/__tests__/ks764-admin-api-keys-revoke-route-contract.test.ts` (NEW) "
    "and modifies `Blockchain/Dev/services/originate/src/middleware/auth.ts` (additive: declares `tenantId?: "
    "string` on `JwtPayload`, no behaviour change) and `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` "
    "(+70/-1, a second `DELETE /api-keys/:id` authorisation check via `decideKeyRevoke`) — both under the GUARDED "
    "`services/originate/src/` prefix — plus `Blockchain/Dev/packages/shared/src/__tests__/ks764-key-revoke-call-"
    "site-guard.test.ts` (NEW) under the GUARDED `packages/shared/src/__tests__/` prefix. **The live launcher "
    "`--check` REFUSES at this tip (exit 18, `check.out`'s fourth entry) — confirmed, not assumed: none of the "
    "three touches `anchorStateSync.ts`, `verification.ts`, or the ks1004/ks1058/ks535/ks1059/ks1057/ks1069/ks1070/"
    "ks1071 test files (`gh_read_close.out`'s file-list grep, 0 hits), so the KS-764 delta is SUBSTANTIVELY "
    "unrelated to this gate's surface — but it DOES add a test file under `services/originate/src/__tests__/`, "
    "which shifts the originate suite's 598/602 denominator, so the refusal is correct and NOT waved through.** "
    "`git merge-base 609c44c55 5210ddf3` and `git merge-base 6fd3a8bec 5210ddf3` both still read M18 "
    "`8861e6216` (both branches unrebased) — confirmed independently by `git merge-base` AND the GitHub compare "
    "API's `merge_base_commit` (`gh_read_close.out`: `merge_base == M18? True True`), so `DEVELOP_SHA`/`MERGE_BASE` "
    "in the launcher stay AT M18, asserted correct, NOT substituted (the L9-restart precedent's rule: the pin "
    "tracks the structural merge-base, not develop's moving tip). **You MUST `ls-remote` again at your own launch: "
    "if develop has moved on to a disjoint state (or #985 has landed disjointly), the launcher proceeds on its own "
    "MOVED note per the paragraph above; if it is STILL at or past M21 with the KS-764 delta still unmerged into "
    "a disjoint tip, `--check` will refuse (exit 18) and you must either wait, or read the delta yourself and "
    "decide — re-deriving the originate suite's total (598 + however many KS-764 adds) if you deliberately re-pin, "
    "per the launcher's own comment header — never by silencing the guard.**\n"
)

PROMPT_ANCHOR = "do the real 3-way merge\n"
PROMPT_INSERT = (
    "  Restart-drafter's close-time re-read (12:00-12:07 AEST): develop moved on to M20 (disjoint, #903) then M21\n"
    "  `5210ddf3` (#799 KS-764 — NOT disjoint: lands a new services/originate/src/__tests__/ test file plus\n"
    "  middleware/auth.ts and routes/adminConfig.ts edits, both under the GUARDED services/originate/src/ prefix,\n"
    "  and a new packages/shared/src/__tests__/ test file). None of it touches anchorStateSync.ts, verification.ts,\n"
    "  or the ks1004/ks1058/ks535/ks1059 family (gh_read_close.out, 0 hits) but it DOES shift the originate 598/602\n"
    "  denominator, so the live launcher --check REFUSES (exit 18) at this tip -- confirmed, not assumed. The\n"
    "  merge-base for both heads against this new tip is STILL M18 (git merge-base + GitHub compare API agree), so\n"
    "  DEVELOP_SHA/MERGE_BASE stay pinned at M18 -- ls-remote again at your own launch and re-judge per the\n"
    "  paragraph below.\n"
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
