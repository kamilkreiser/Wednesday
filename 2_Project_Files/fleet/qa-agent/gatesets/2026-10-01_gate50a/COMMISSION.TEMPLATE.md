# gate50a COMMISSION — ONE Secuura PR: #{{PR}} KS-1378 (T1, round 1), ITEM A; author and merger {{MERGE_SEAT}}, round 50a

Filled by fill_gate50a.py at {{FILLED_AT}} from pins_gate50a.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-10-01 (~07:25 AEST), restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords (each as a token).

## The PR
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1361's merge. 0 behind. END_TREE `{{END_TREE}}` (`{{SHORTSTAT}}`). {{END_XCHECK}}
- {{MODE_LINE}}
- {{HOOK_LINE}}
- Merger {{MERGE_SEAT}} (tmux %86; the author). Pane `QA/Secuura-batch{{PR}}`. Report dir `{{REPORT}}`.

## The ruling
- **Wednesday's ANSWER route (a) (2026-09-30T20:54Z):** ITEM A, ONE in-range lock-refresh PR from develop 4f18c59a89db, no manifest change, its OWN gate (gate50a, T1) because it unfreezes every push, Peter's included. Route (b) (baseline the batch) REFUSED. If any advisory survives, STOP and mail. **ANSWER 20:59Z:** the lock set is FOUR; `Refs KS-1378` on the branch; the NEW ticket text is read by gate50a and filed on the GO, before the merge.
- **The claim** (the READY, 21:21:14Z): 4 locks, +19/−19, 5 moves (root 2, admin / verifier / kyc 1 each), ADDED 0 / REMOVED 0; `refresh46.sh` in `node:24-alpine`, npm 11.19.0; a pristine control at the same base; legs 6 / 7 / contract rc 1 / 1 / 0 at develop and 0 / 0 / 0 at head; 13/13 advisories cleared; 26 baselined before and after; kyc suite 33/33 both sides; four images built (build only).
- **The drafter's addition, measured:** each axios entry also moves one range line, `form-data` `^4.0.5` -> `^4.0.6` (axios 1.20.0's own manifest); form-data 4.0.6 is already resolved in all four locks.

## What the gate must rule (by name)
1. **The four lock diffs re-derived and reproduced**: containerised `node:24-alpine` regen against a pristine control at the base, byte-identical to the PR; ONLY axios 1.18.1 -> 1.20.x and dompurify 3.4.13 -> 3.4.16 moved (plus integrity / resolved); MOVED / ADDED / REMOVED per lock; the form-data range line ruled. (LOCK-DELTA-4, OWN-DEPENDENCIES, DEPENDENT-RANGES, REGISTRY-TRUE, REPRODUCE-REFRESH, PRISTINE-CONTROL)
2. **Legs 6 / 7 / audit:contract** at develop (rc 1 / 1 / 0) and head (rc 0 x3), with a refusal control per leg. (AUDIT-LEGS-BASE-HEAD, THIRTEEN-IDS-ABSENT, GATE-STILL-REFUSES, NO-BASELINE-ROW)
3. **Each of the 13 advisories mapped** to the lock entry that cleared it, re-derived. (ADVISORY-MAP)
4. **Consumers**: kyc / admin-frontend / verifier-frontend / issuer-frontend built develop vs head (build only); the served axios in the kyc image; the kyc suite; the root lock's workspace consumers (issuer at least); `npm ci` at the head. (RUNTIME-REACH, ROOT-LOCK-CONSUMERS, SUITES, NPM-CI-HEAD)
5. **mobile/secuura-app untouched** (KS 769). (MOBILE-UNTOUCHED)
6. **The merge, END, modes, the census** (Peter's #1360 touches the root and kyc locks: reported). (CLEAN-MERGE, END-TREE, MODES, COLLISION-CENSUS)
7. **The PR text**: subject, body, the Test Evidence block — every factual line checked against the head. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
8. **The proposed NEW ticket text** (client-visible): POST AS-IS / POST AMENDED (full amended text) / DO NOT POST, sentence by sentence against its sources. (NEW-TICKET-TEXT)
9. **The gatelines VERDICT wording**: which state of gatelines46.py is the clean one — a tooling finding, not for this PR. (GATELINES-VERDICT)
10. FUSE-COUNT, TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**; the `## MERGE ADDENDUM` LAST. The change is SMALL: a proportionate pass (usage 76% of the weekly allowance).

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} merges #{{PR}}. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate50a.py -> pin_1.out: END_TREE `{{END_TREE}}`. {{NUMSTAT}}
- lockdelta_gate50a.py -> lockdelta_1.out: {{LOCKDELTA}}
- reach_gate50a.py -> reach_1.out: {{REACH}}
- overlaps_gate50a.py -> overlaps_1.out: {{OVERLAPS}}
- keyscan_gate50a.py -> keyscan_1.out: {{KEYSCAN}}
- gh_read_gate50a.py -> gh_read_1.out: {{CENSUS_LINE}}
- capture_mail_gate50a.py -> capture_1.out: {{CAPTURE_LINE}}
