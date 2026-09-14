#!/usr/bin/env python3
"""restart_patch_912r2_prompt.py — corrected re-run of the prompt-side half of restart_patch_912r2.py: the first
attempt's anchor ("do the real 3-way merge\n") landed MID-SENTENCE (split "do the real 3-way merge" from
"of each head onto the tip..."), reverted in-session before any downstream use, redone here at a sentence-end
anchor. Same asserted-substitution discipline: anchor must occur exactly once, refuses otherwise."""
import hashlib, sys

PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.prompt.txt'

ANCHOR = "there too, naming both trees.\n"
INSERT = (
    "  Restart-drafter's close-time re-read (12:00-12:07 AEST): develop moved on to M20 (disjoint, #903) then M21\n"
    "  `5210ddf3` (#799 KS-764 — NOT disjoint: lands a new services/originate/src/__tests__/ test file plus\n"
    "  middleware/auth.ts and routes/adminConfig.ts edits, both under the GUARDED services/originate/src/ prefix,\n"
    "  and a new packages/shared/src/__tests__/ test file). None of it touches anchorStateSync.ts, verification.ts,\n"
    "  or the ks1004/ks1058/ks535/ks1059 family (gh_read_close.out, 0 hits) but it DOES shift the originate 598/602\n"
    "  denominator, so the live launcher --check REFUSES (exit 18) at this tip -- confirmed, not assumed. The\n"
    "  merge-base for both heads against this new tip is STILL M18 (git merge-base + GitHub compare API agree), so\n"
    "  DEVELOP_SHA/MERGE_BASE stay pinned at M18 -- ls-remote again at your own launch and re-judge per the\n"
    "  paragraph above.\n"
)

src = open(PROMPT, encoding='utf-8').read()
before_hash = hashlib.sha256(src.encode()).hexdigest()[:16]
n = src.count(ANCHOR)
if n != 1:
    print(f"REFUSING: anchor occurs {n} times (expected 1)"); sys.exit(1)
idx = src.index(ANCHOR) + len(ANCHOR)
out = src[:idx] + INSERT + src[idx:]
open(PROMPT, 'w', encoding='utf-8').write(out)
after_hash = hashlib.sha256(out.encode()).hexdigest()[:16]
print(f"prompt: {before_hash} -> {after_hash}  bytes {len(src)} -> {len(out)} (+{len(out)-len(src)})")
