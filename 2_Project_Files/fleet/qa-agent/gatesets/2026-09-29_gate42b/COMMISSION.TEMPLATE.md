# gate42b COMMISSION — #1340, the audit-baseline re-date (Tier 2, round 1 of 2)

Filled by fill_gate42b.py at {{FILLED_AT}} from pins_gate42b.json (measured {{MEASURED_AT}}). Wednesday's commission to the drafter, 2026-09-29, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any.

## The PR
- https://github.com/Secuura/Distributed_Secuura/pull/1340 — `{{SUBJECT}}` — branch `{{BRANCH}}`
- head `{{HEAD}}` (one commit; parent == develop), base develop `{{DEVELOP}}` (tree `{{DEVELOP_TREE}}`), merge-base `{{MERGE_BASE}}`, ahead {{AHEAD}} / behind {{BEHIND}}
- ONE file `{{PATH}}`, +8/-8; baseline blob `{{BLOB_DEVELOP}}` -> `{{BLOB_HEAD}}`; END_TREE `{{END_TREE}}` (clean merge-tree; == the head's tree)
- Tickets: KS-530 (frvp), KS-729 (mwp4), KS-528 (wrjc + 337j), each as `Refs`, none closed.
- Tier 2 (a config/data file only — no code, manifest, lock or surface), round 1 of 2 under the cap. Pane `QA/Secuura-batch1340`. Report dir `{{REPORT}}`.
- **The fuse:** at {{FUSE}} develop's GHSA-frvp-7c67-39w9 row lapses and leg 6 refuses every push and merge. **#1340 MUST MERGE BEFORE THEN.** Merge order: #1340 ALONE.

## The authority (captured verbatim, mail_gate42b_ready.md)
Kam, from kreiser.org@me.com, {{AUTH_AT}}, Message-ID `{{AUTH_ID}}`:
> "{{AUTH_TEXT}}"

## What the gate must check
1. **Field level** — exactly the four rows differ; on each only `expires` (-> 2026-10-09) and `reason`; 25 rows before and after; top-level keys unchanged; no other file. (FIELD-FOUR-ROWS-ONLY, FIELD-EXPIRES-AND-REASON-ONLY, ROWS-25-BOTH, TOP-KEYS-UNCHANGED, ONE-FILE-ONLY)
2. **Kam's email, verbatim** — the rows, ids and tickets match his mail; no row he did not name is touched. (KAM-EMAIL-VERBATIM, NO-UNNAMED-ROW)
3. **Legs 6 and 7 at the REAL clock** — `audit-gate.mjs` / `audit-locks.mjs` rc 0 at the head; rc 0 at develop too (before the fuse). (LEGS-6-7-REAL-CLOCK-HEAD, LEGS-6-7-REAL-CLOCK-BASE)
4. **A frozen-clock proof run BY THE GATE ITSELF** — at 2026-09-30T00:01Z develop's baseline rc 1 (GHSA-frvp lapsed) and the head rc 0; control at 2026-10-10T00:01Z on the head rc 1 with the re-dated rows lapsed. A `node --import` preload freezing `Date`, the real scripts unmodified; the gate proves the preload moves the clock (positive arm) and refuses when unset. (FROZEN-CLOCK-BY-THE-GATE, PRELOAD-POSITIVE-ARM, PRELOAD-REFUSES-UNSET, FUSE-BASE-RED, FUSE-HEAD-GREEN, FUSE-CONTROL-1010-RED)
5. **The squash subject and body** — key scan (only KS-530 / KS-729 / KS-528; no `(#n)`); landed length declared + 8 <= 92 (declared {{SUBJ_LEN}}, lands {{SUBJ_LAND}}); body `Refs KS-530`, `Refs KS-729`, `Refs KS-528`, no closing keyword. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, REFS-THREE-KEYS, NO-CLOSING-KEYWORD)
6. **END tree** for the single merge — `{{END_TREE}}`. (END-TREE, MERGE-ORDER-1340-ALONE)

## GO
The GO string, as the GO mail's SUBJECT: `{{GO}}` — {{MERGE_SEAT}} merges. Verdict mail subject: `{{VERDICT_SUBJECT}}`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- fieldcheck_gate42b.py -> fieldcheck_1.out: {{FIELDCHECK}}
- keyscan_gate42b.py -> keyscan_1.out: {{KEYSCAN}}
- fuseproof_gate42b.mjs (offline predicate, the repo's own baseline-contract.mjs, no advisory fetched) — rows that CAN lapse: {{FUSEPRED}}
