# Spark operator 62, 2026-11-02: KS-1868 tenant-provisioning index.ts Zod-preceded trio (1 held, 0 failed, 0 rebriefs)

## BLUF
O62-P1 HELD: POST /api/tenants (:337), GET /api/tenants (:378), PATCH /api/tenants/:id (:536). Control CONTROL-PASS first time (58 s), model round PASS 7/7 first time (147 s round, 87.7 s model), golden BYTE-IDENTICAL. Nothing skipped. Tip 03977e89a343ad7362760e4fb0270602fb6da5ce at start (tip_start.out) and end (tip_end.out). PR scan start and end both 22 PRs / 125 files, planted control services/originate = 6 both times; tenant-provisioning appears only as package.json (649) / package-lock.json (1360). Counter: original brief only.
Note for Wednesday: ONE judgment call to confirm, POST's persisted state on the unreadable path (below).

## Held (held_files.txt)
READY_KS-1868-KS-1868-O62-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-TENANT-PROVISIONING-ZOD-PRECHECK-POST-GET-PATCH-TENANTS-CATCHES-PASS-7of7_2026-11-02.diff.md

## O62-P1
- hold_ready: `golden: BYTE-IDENTICAL; touched=2 product_plus=27 product_minus=3 red=6/12 green=12/12 suite=84->96 strict=True`.
- Fix (shape of O61/O56-P2, in this file): rename the catch var to `thrown`, `let err: unknown = thrown;`, one try probing BOTH reads on `thrown` (`!(thrown instanceof z.ZodError)` guarding the same message expression); on throw `err = new Error('unreadable thrown value')`. Every later line (ZodError block, `details: err.errors`, message line, console.error, 500s, POST rollback) is textually untouched. Note: O57's guard is the `let message` try/catch; that cannot cover the earlier ZodError test, so the O61 rebind shape was used, with O57's constant string `unreadable thrown value`. No new helper.
- Test: src/__tests__/ks1868-tenant-provisioning-zod-precheck-catches-unreadable-throw.test.ts (new, 12 cells = 3 routes x R1 revoked Proxy, R2 getter-throwing Error, C1 ordinary ZodError, C2 ordinary Error; key-service fetch stubbed to reject).
- Existing pin ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts (`details: err.errors` x3, console.error before each 500, POST 500 `message: message`) is UNCHANGED and green: it is part of the golden suite 84->96 (84 baseline files-tests passing before, plus the 12 new). Not edited.
- Ordinary ZodError path: 400 + `details: err.errors`, identical (C1, all 3 routes: logs nothing, no rollback). Ordinary Error path: identical (C2: logs own message; POST echoes it in its 500 as today; GET/PATCH constant 500).
- Persisted state per path, POST /api/tenants (creates a tenant):
  - failure before the tenant INSERT: nothing persisted, all paths.
  - ZodError after the INSERT: 400, NO rollback (partial `provisioning` tenant stays), unchanged (C1 asserts zero DELETEs).
  - ordinary Error after the INSERT: rollback by 3 DELETEs, 500, unchanged (C2 asserts 3 DELETEs).
  - UNREADABLE value after the INSERT: today the catch throws on its first statement, no response, NO rollback, the partial tenant stays; after, it takes the ordinary-Error path: rollback 3 DELETEs + 500 (R1/R2 assert). This is the only persisted-state change and it equals what an ordinary Error already gets, so not skipped (same precedent as O57-P2's audit row). Wednesday/Kam: if "persisted state would change on any path" is meant to forbid even this, drop the POST hunk; the other two hunks are independent.
  - GET /api/tenants persists nothing. PATCH: failing UPDATE persists nothing; audit INSERT after the UPDATE is a separate non-transactional statement, unchanged.
- POST's 500 still echoes the caught message (Kam's open card, ks1410 EXEMPT); untouched. For an unreadable value that message is `unreadable thrown value`.
- Callers: only api-gateway routes/platform.ts over HTTP via fetchWithTimeout (not re-grepped this session beyond O57's list; UNMEASURED for POST/GET-list/PATCH line numbers).
- BEHAVIOUR CHANGE (PR text): unreadable thrown value: today no response + unhandled rejection; after, logged `unreadable thrown value` and the route's ordinary-Error 500; POST also rolls back a partly created tenant like an ordinary Error. No body/status/log change for ordinary ZodError, Error, or string.
- Recommended tier: 1 or 2; POST is the tenant-create route with a rollback that now runs on a new input class, so I recommend tier 1 for the POST hunk (Kam may split: GET + PATCH tier 2).

## Raise-seat notes
strict=True (plain git apply). Hunks start at old lines 337, 385 (hunk header), 551 region (see held file headers); O57 holds P1 at 424/482/651 and P2 at 603-629: nearest pairs 385-ish GET vs 424 (>3, GET hunk ends ~393 vs O57 context from 421), PATCH ~536-548 vs O57-P1 482 (ends 485) and O57-P2 603 (starts 600): all > 3 apart, any apply order; the file was NOT briefed against O57's held content (all hunks at tip). Remaining unfixed in POST: `(cleanupErr as Error).message` and the two inner `(err as Error).message` key-service warns (separate sites, not Zod-preceded; the inner `err` shadows).
Test names: R1/R2 "RED ks1868 R1|R2 <route>", controls "control ks1868 C1|C2 <route>".

## Round log (spark/done.md; done_rows.txt)
- queued control 08:21:19; 08:22:37 CONTROL-PASS (58 s, golden BYTE-IDENTICAL)
- queued model 08:22:5x; 08:25:25 PASS 7/7, 147 s round, 87.662 s model, 25145+3557 tok, BYTE-IDENTICAL
- hold_ready ~08:26. Lint rc 0, dry run rc 0 (72807 B input).

## UNMEASURED
Whole-suite CI; eslint/tsc outside the checker; real Express 4 / Postgres; whether an unreadable value is reachable in production; callers' exact line numbers for the three routes; the inner catches in POST (cleanupErr, key-service warns); behaviour of a ZodError whose `errors` getter throws (untouched, same as today).
Evidence: this folder (tip_*, prscan_*, lint_p1, dry_p1, hold_p1.log, done_rows.txt, held_files.txt, mk_p1.out, gen/mk62.py t62_p1.ts.txt hold62.sh).
