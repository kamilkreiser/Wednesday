# gate42b COMMISSION — #1340, the audit-baseline re-date (Tier 2, round 1 of 2)

Filled by fill_gate42b.py at 2026-09-29T06:41:22Z from pins_gate42b.json (measured 2026-09-29T06:37:40Z). Wednesday's commission to the drafter, 2026-09-29, restated requirement by requirement; the gate prompt carries each by name and the launcher refuses a prompt missing any.

## The PR
- https://github.com/Secuura/Distributed_Secuura/pull/1340 — `KS-530: re-date the four audit-baseline rows Kam named to 2026-10-09` — branch `refs/heads/feature/ks-530-audit-baseline-redate-b44-1`
- head `9199a2f9f7394cdd2c78b5134e68ff7ba3e91fae` (one commit; parent == develop), base develop `2cb858335472fafcce535ca4ad328c897ed87bfb` (tree `438bc1254bbf7e27637b009e6817bfdb37fb1259`), merge-base `2cb858335472fafcce535ca4ad328c897ed87bfb`, ahead 1 / behind 0
- ONE file `Blockchain/Dev/scripts/audit/audit-baseline.json`, +8/-8; baseline blob `2230ad84181b59b815350bda8f72ab9fae350a1f` -> `5aca4edb61280b7f232a62f7e876df43e0c362f8`; END_TREE `09c593f29fd4ecf1691d99e961bfa060812932c8` (clean merge-tree; == the head's tree)
- Tickets: KS-530 (frvp), KS-729 (mwp4), KS-528 (wrjc + 337j), each as `Refs`, none closed.
- Tier 2 (a config/data file only — no code, manifest, lock or surface), round 1 of 2 under the cap. Pane `QA/Secuura-batch1340`. Report dir `2026-09-29-batch1340-g42b`.
- **The fuse:** at 2026-09-30T00:00:00Z develop's GHSA-frvp-7c67-39w9 row lapses and leg 6 refuses every push and merge. **#1340 MUST MERGE BEFORE THEN.** Merge order: #1340 ALONE.

## The authority (captured verbatim, mail_gate42b_ready.md)
Kam, from kreiser.org@me.com, 2026-09-29T04:14:47Z, Message-ID `<EB856837-268F-4CC7-B167-BE74B4824634@me.com>`:
> "Re-date GHSA-frvp-7c67-39w9 (KS-530), GHSA-mwp4-54f8-5fhr (KS-729), GHSA-wrjc-x8rr-h8h6 and GHSA-337j-9hxr-rhxg (KS-528) to 2026-10-09. The real fixes stay on those tickets."

## What the gate must check
1. **Field level** — exactly the four rows differ; on each only `expires` (-> 2026-10-09) and `reason`; 25 rows before and after; top-level keys unchanged; no other file. (FIELD-FOUR-ROWS-ONLY, FIELD-EXPIRES-AND-REASON-ONLY, ROWS-25-BOTH, TOP-KEYS-UNCHANGED, ONE-FILE-ONLY)
2. **Kam's email, verbatim** — the rows, ids and tickets match his mail; no row he did not name is touched. (KAM-EMAIL-VERBATIM, NO-UNNAMED-ROW)
3. **Legs 6 and 7 at the REAL clock** — `audit-gate.mjs` / `audit-locks.mjs` rc 0 at the head; rc 0 at develop too (before the fuse). (LEGS-6-7-REAL-CLOCK-HEAD, LEGS-6-7-REAL-CLOCK-BASE)
4. **A frozen-clock proof run BY THE GATE ITSELF** — at 2026-09-30T00:01Z develop's baseline rc 1 (GHSA-frvp lapsed) and the head rc 0; control at 2026-10-10T00:01Z on the head rc 1 with the re-dated rows lapsed. A `node --import` preload freezing `Date`, the real scripts unmodified; the gate proves the preload moves the clock (positive arm) and refuses when unset. (FROZEN-CLOCK-BY-THE-GATE, PRELOAD-POSITIVE-ARM, PRELOAD-REFUSES-UNSET, FUSE-BASE-RED, FUSE-HEAD-GREEN, FUSE-CONTROL-1010-RED)
5. **The squash subject and body** — key scan (only KS-530 / KS-729 / KS-528; no `(#n)`); landed length declared + 8 <= 92 (declared 68, lands 76); body `Refs KS-530`, `Refs KS-729`, `Refs KS-528`, no closing keyword. (SUBJECT-KEY-SCAN, SUBJECT-LANDS-AT, REFS-THREE-KEYS, NO-CLOSING-KEYWORD)
6. **END tree** for the single merge — `09c593f29fd4ecf1691d99e961bfa060812932c8`. (END-TREE, MERGE-ORDER-1340-ALONE)

## GO
The GO string, as the GO mail's SUBJECT: `GO (Seat B 44th): merge 1340 on gate42b` — Seat B 44th merges. Verdict mail subject: `[QA -> Wednesday] GATE42b batch #1340 (Seat B44, round 42b; T2: KS-530 the audit-baseline re-date, round 1 of 2)`.

## The drafter's predictions (to be re-derived by the gate, never adopted)
- fieldcheck_gate42b.py -> fieldcheck_1.out: FIELDCHECK PASS: 24 checks, 0 FAIL, 4 row(s) checked field by field
- keyscan_gate42b.py -> keyscan_1.out: KEYSCAN PASS: 8 checks, 0 FAIL
- fuseproof_gate42b.mjs (offline predicate, the repo's own baseline-contract.mjs, no advisory fetched) — rows that CAN lapse: ARM base-0930 rc 0: base baseline @ 2026-09-30T00:01:00Z -> utcToday 2026-09-30 | rows 25 checked | can-lapse 2: GHSA-frvp-7c67-39w9 (KS-530, expires 2026-09-30), GHSA-mwp4-54f8-5fhr (KS-729, expires 2026-09-30) MATCH: expected GHSA-frvp-7c67-39w9,GHSA-mwp4-54f8-5fhr | ARM head-0930 rc 0: head baseline @ 2026-09-30T00:01:00Z -> utcToday 2026-09-30 | rows 25 checked | can-lapse 0: none MATCH: expected none | ARM head-1008 rc 0: head baseline @ 2026-10-08T23:59:00Z -> utcToday 2026-10-08 | rows 25 checked | can-lapse 0: none MATCH: expected none | ARM head-1009 rc 0: head baseline @ 2026-10-09T00:01:00Z -> utcToday 2026-10-09 | rows 25 checked | can-lapse 4: GHSA-337j-9hxr-rhxg (KS-528, expires 2026-10-09), GHSA-frvp-7c67-39w9 (KS-530, expires 2026-10-09), GHSA-mwp4-54f8-5fhr (KS-729, expires 2026-10-09), GHSA-wrjc-x8rr-h8h6 (KS-528, expires 2026-10-09) MATCH: expected GHSA-337j-9hxr-rhxg,GHSA-frvp-7c67-39w9,GHSA-mwp4-54f8-5fhr,GHSA-wrjc-x8rr-h8h6 | ARM head-1010 rc 0: head baseline @ 2026-10-10T00:01:00Z -> utcToday 2026-10-10 | rows 25 checked | can-lapse 4: GHSA-337j-9hxr-rhxg (KS-528, expires 2026-10-09), GHSA-frvp-7c67-39w9 (KS-530, expires 2026-10-09), GHSA-mwp4-54f8-5fhr (KS-729, expires 2026-10-09), GHSA-wrjc-x8rr-h8h6 (KS-528, expires 2026-10-09) MATCH: expected GHSA-337j-9hxr-rhxg,GHSA-frvp-7c67-39w9,GHSA-mwp4-54f8-5fhr,GHSA-wrjc-x8rr-h8h6
