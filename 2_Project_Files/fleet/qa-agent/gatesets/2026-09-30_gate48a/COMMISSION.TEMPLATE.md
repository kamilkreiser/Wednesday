# gate48a COMMISSION — ONE Secuura PR: #1354 KS-470 (T2), ROUND 1 of its own PR; author and merger {{MERGE_SEAT}}, round 48a

Filled by fill_gate48a.py at {{FILLED_AT}} from pins_gate48a.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-30, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any of the {{N_KW}} keywords (each as a token).

## The PR
{{PIN_TABLE}}

- develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`) = #1350's squash (gate47's GO). #1354's parent IS develop (0 behind, 1 ahead); alone over develop it is clean and its squash gives END_TREE `{{END_TREE}}` == the head's own tree (pins (E)-(G)).
- {{MODE_LINE}}
- {{HOOK_LINE}}
- Author and merger {{MERGE_SEAT}} (tmux %77). Pane `QA/Secuura-batch1354`. Report dir `{{REPORT}}`.

## The rulings
- Wednesday's leg-7 ruling (2026-09-30 07:31 AEST, under Kam's 2026-09-09 advisory-baseline grant): **FIX** js-yaml GHSA-r3ph (lock-only, MOVED=1 as the outcome test) and **ONE baseline row** for undici GHSA-r53p, ticket KS-470. Its item 2 ("no `expires`") is **SUPERSEDED** by the ROUTE B ruling (07:39 AEST): `expires 2026-10-09`, the contract edit reverted byte-equal, TWO files; the seat's two deviations (the verb `npm update js-yaml`; the parent-dir mount) ACCEPTED.
- **TIER 2** (Wednesday's; the gate grades it). **ROUND 1 of its own PR; a round-1 NO GO goes back to the author for round 2.**
- **The grant's exception is the ruling that decides the verdict**: "A package appearing in BOTH a test lock and a shipped tree stops for Kam, regardless of severity." If it fires: NO GO, first, for Kam.

## What the gate must check (by name)
1. **The lock**: exactly one entry moves (js-yaml 5.2.3 -> 5.4.2), integrity/resolved == the registry, lockfileVersion and the `secuura-observability` link byte-identical; the seat's regen re-run in a scratch copy gives the same bytes; both deviations reproduced; the changed lock clean-room installs (no preflight leg covers `systemTest/`); 5.4.2 outside GHSA-r3ph's range READ FROM THE ADVISORY. (LOCK-DIFF-ONE-ENTRY, JSYAML-OUT-OF-RANGE)
2. **The row**: its fields, `expires` exactly 2026-10-09, ticket KS-470, a pure insert (no other row, no `$comment` byte changed), `baseline-contract.mjs` byte-equal to the base, GRANDFATHERED == the no-expiry rows; the number of rows expiring 2026-10-09 at END. (BASELINE-ROW-FIELDS, CONTRACT-BYTE-EQUAL, FUSE-COUNT)
3. **The audit gates** `audit:contract` / `audit:gate` (leg 6) / `audit:locks` (leg 7) at base (leg 6/7 FAIL expected), head and END (rc 0 each), each rc on its own line, counts and ids printed. (AUDIT-GATES-HEAD-END)
4. **Clause 2 re-measured and the exception checked**: the issuer image built (build only) and its served files searched with positive controls; every lock pinning undici / js-yaml at a vulnerable version, and whether its directory builds a shipped tree; the four clauses as rows. (CLAUSE2-REMEASURE, EXCEPTION-CHECKED, GRANT-CLAUSES)
5. **The row's `reason`**, sentence by sentence, TRUE of the tree / the image — a published record. (REASON-TEXT-TRUE)
6. **The two drafted tickets** (the undici override follow-up; the cleanroom remediation defect), line by line: POST AS-IS / POST AMENDED (in full) / DO NOT POST. (DRAFTED-TICKETS-CHECKED)
7. **The merge**: clean over develop, END_TREE `{{END_TREE}}`, modes 100644 x2 with a 100755 control, the census of other open PRs (2 paths; KS-470 / KS-1374 / KS-1054 titles; Peter's #1351-#1353 REPORTED, never sequenced by the gate). (CLEAN-MERGE, END-TREE, MODES, OUT-OF-KIT-CENSUS)
8. **Subject and body**: key KS-470 only, landed <= 92, TRUE of the diff, `Refs KS-470`, no closing keyword; the PR body's factual lines. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, REFS-OWN-KEY, NO-CLOSING-KEYWORD, PR-BODY-CLAIMS)
9. TIERING, DISK-ENOSPC, and **REPORT-HASH-LAST**: the report's `## MERGE ADDENDUM` is the LAST thing written; nothing goes into report.md after the verdict mail, whose body carries the report's sha256.

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} merges #1354. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- pin_gate48a.py -> pin_1.out: clean alone; END_TREE `{{END_TREE}}` == the head tree; the contract byte-equal.
- lockdiff_gate48a.py -> lockdiff_1.out: {{LOCKDIFF}}
- baseline_gate48a.py -> baseline_1.out: {{BASELINE}}
- lockcensus_gate48a.py -> lockcensus_1.out: {{LOCKCENSUS}}
- keyscan_gate48a.py -> keyscan_1.out: {{KEYSCAN}}
- gh_read_gate48a.py -> gh_read_1.out: {{CENSUS_LINE}}
- capture_mail_gate48a.py -> capture_1.out: {{CAPTURE_LINE}}
- drafts_gate48a.py -> drafts_1.out: {{DRAFTS_LINE}}
