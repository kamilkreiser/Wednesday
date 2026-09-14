#!/usr/bin/env python3
"""restart_patch_912r2_predictions.py — second restart-drafter narrative insertion, per Wednesday's 2026-09-14
12:1x AEST instruction: turn the merged-tree originate/packages-shared suite counts into explicit PREDICTIONS
(predicted-by: drafter), state the arithmetic, and tell the real gate to re-derive the develop-alone counts on its
own farm before judging the ratio. Asserted substitution: anchor must occur exactly once in each file."""
import hashlib, sys

BRIEF = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.md'
PROMPT = '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-14_gate912r2/2026-09-14_secuura-912-ks1004-tier1-r2-937-ks1059-stacked.prompt.txt'

BRIEF_ANCHOR = "never by silencing the guard.**\n"
BRIEF_INSERT = (
    "- **PREDICTIONS, predicted-by: drafter (Wednesday's 2026-09-14 12:1x AEST instruction, the #984/#982-#983 "
    "precedent) — the launcher's develop guard now CONTENT-JUDGES the four M21 (KS-764/#799) paths by blob (see "
    "the launcher's `M21_ALLOWED` dict) instead of refusing on path alone, so a merge onto a develop that still "
    "carries exactly those four blobs proceeds (`--check` read live, `check.out`: rc 0, `ALLOWED …` note). That "
    "means the merged-tree originate and packages/shared suite counts this brief and `controls_check.sh` were "
    "written against (the PR-alone 56 suites/598 cells for #912, 57/602 for the #937 stack — both over M18, "
    "unaffected by KS-764) are NO LONGER the merged-tree total once M21's content is folded in. The arithmetic, "
    "stated so it can be checked rather than trusted: **originate** — the L5 gate's own measurement of KS-764's "
    "content is +1 suite / +10 tests over M20's develop-alone 55 suites/588 cells → **56/598 develop-alone at "
    "M21** (the KS-764 admin-api-keys-revoke-route-contract.test.ts file, wholly new, disjoint from "
    "anchorStateSync/ks1004/ks1058/ks535/ks1059); ADD the PR's own already-measured delta over M18 (#912 alone: "
    "+0 suites beyond what's in the 56/598 PR-head figure's own ks1004 addition — **PREDICTED merged-tree "
    "originate for #912 = 57 suites / 608 cells** [56/598 PR-head + M21's +1 suite/+10 tests]; **for the #937 "
    "stack = 58 suites / 612 cells** [57/602 stack-head + the same +1/+10]). **packages/shared** — L5 measured "
    "+2 files / +15 tests over M20's 40/813 → **42 files / 828 tests develop-alone at M21**; neither #912 nor "
    "#937 touches `packages/shared/` at all (confirmed: neither PR's file list names it), so the **PREDICTED "
    "merged-tree packages/shared count is 42/828 directly, unchanged by which PR head**. **These four numbers "
    "(57/608, 58/612, 42/828, 42/828) are PREDICTIONS ONLY — re-derive the develop-alone originate and "
    "packages/shared counts yourself on your own clone/farm (item 4/7's own instruction) before judging the "
    "ratio against them; a mismatch between your measured count and this prediction is a BRIEF ERROR to name, "
    "NOT a finding against the PR** — the PR's own four-file delta (`git diff --numstat 8861e6216 609c44c55`) "
    "is independently pinned and unaffected by any of this arithmetic.**\n"
)

PROMPT_ANCHOR = "paragraph above.\n"
PROMPT_INSERT = (
    "  PREDICTIONS (predicted-by: drafter): the guard now clears M21's four KS-764 paths by blob, so a merge onto\n"
    "  a develop still at exactly those four blobs proceeds. The merged-tree originate/packages-shared counts are\n"
    "  therefore PREDICTIONS, not pins -- brief section states the arithmetic (56/598 PR-head + M21's +1 suite/\n"
    "  +10 tests = 57/608 for #912, 58/612 for the #937 stack; packages/shared untouched by either PR = 42/828\n"
    "  directly). RE-DERIVE these yourself before judging the ratio; a mismatch is a brief error, not a finding\n"
    "  against the PR.\n"
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
