# gate49a COMMISSION — ONE Secuura PR: #{{PR}} KS-1378 (T1, round 1), ITEM A; author and merger {{MERGE_SEAT}}, round 49a

Filled by fill_gate49a.py at {{FILLED_AT}} from pins_gate49a.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-30 (~04:00Z), restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords (each as a token).

## The PR
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1355's squash. 0 behind. END_TREE `{{END_TREE}}` (`{{SHORTSTAT}}`).
- {{MODE_LINE}}
- {{HOOK_LINE}}
- Merger {{MERGE_SEAT}} (tmux %81; the author). Pane `QA/Secuura-batch{{PR}}`. Report dir `{{REPORT}}`.

## The ruling
- **Wednesday's ANSWER plan (2026-09-30 13:45 AEST):** ITEM A, an in-range lock refresh measured then raised as ONE PR, `Refs KS-1378`, locks only, no acceptance; T1 (production entries in shipped images). "The 09-09 baseline grant is NOT used." Its STOP conditions (a major; mobile; a baseline row; anything in a shipped tree beyond the named packages) are the gate's to rule NOT fired.
- **The claim** (status itemA measured, 03:56Z): 18 locks, +102/−102, 30 moves, ADDED 0 / REMOVED 0 per lock; `npm update <pkg> --package-lock-only --ignore-scripts` in `node:24-alpine`, npm 11.19.0 (root-mounted for systemTest/akto and performance); a pristine control at the same SHA moved nothing; mobile untouched.

## What the gate must check (by name)
1. **The diff re-derived**: exactly 18 locks; per lock every changed entry (version, resolved, integrity, flags); ADDED/REMOVED 0; every moved version inside every dependant's declared range; integrity == the registry's, with a deliberately wrong one as the control. (LOCK-DELTA-18, DEPENDENT-RANGES, REGISTRY-TRUE)
2. **The refresh reproduced** in a clean container from develop, same npm; `cmp` to the head; the pristine control. (REPRODUCE-REFRESH, PRISTINE-CONTROL)
3. **The audit legs** at develop (6/7 rc 1 with exactly the six) and head (contract/6/7 0/0/0); each id absent per id; each leg still refuses a planted advisory (the offline stub); no baseline row. (AUDIT-LEGS-BASE-HEAD, SIX-IDS-ABSENT, GATE-STILL-REFUSES, NO-BASELINE-ROW)
4. **Runtime reach**: mcp-server and nft-certificate built at develop and head under the gate's own compose project names, build only; the served trees' resolved versions; whether the root lock reaches any image. (RUNTIME-REACH, ROOT-LOCK-CONSUMERS)
5. **Suites** for mcp-server and nft-certificate before/after with counts; every test naming a changed path. (SUITES, SHARED-GUARD-TESTS)
6. **`npm ci --ignore-scripts` at the head**: root + the moved standalone locks (or a named representative set). (NPM-CI-HEAD)
7. **The merge, END, modes, and the collision census** of every open PR on the 18 locks — reported, not refused. (CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS)
8. **Title, body, branch, commit**: `Refs KS-1378` only; subject lands ≤ 92; no closing keyword; the body's claims line by line; the squash subject declared WITHOUT `(#n)`. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
9. **Follow-ons, reported**; the fuse count. (FOLLOW-ONS, FUSE-COUNT)
10. TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` LAST.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} merges #{{PR}}. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate49a.py -> pin_1.out: END_TREE `{{END_TREE}}`. {{NUMSTAT}}
- lockdelta_gate49a.py -> lockdelta_1.out: {{LOCKDELTA}}
- reach_gate49a.py -> reach_1.out: {{REACH}}
- overlaps_gate49a.py -> overlaps_1.out: {{OVERLAPS}}
- keyscan_gate49a.py -> keyscan_1.out: {{KEYSCAN}}
- gh_read_gate49a.py -> gh_read_1.out: {{CENSUS_LINE}}
- capture_mail_gate49a.py -> capture_1.out: {{CAPTURE_LINE}}
