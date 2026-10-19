# Spark screen, part 18 (2026-10-20 ~05:25-05:42 AEDT): KS-1679 (certificationId and certifiedAt, rung 3), ONE brief, PASS, golden BYTE-IDENTICAL

model: claude-sonnet-5-5 -- Spark screen-18 brief-writing sub-agent -- P1-P4 no

By a Spark brief-writing sub-agent for Wednesday. Secuura only. Nothing held, raised, pushed, merged, committed or deleted; no GitHub or Linear write; no `hold_ready`. Nothing under `!CODING` was written (the Linear key was read inside a scratch script file and never printed; read-only query of KS-1679 plus its comments(first:50), none on it).

## BLUF
- **KS-1679 is briefed as `ks_1679_p1`, code_patch2 rung 3** (one product file in ONE hunk + one MODIFIED existing test, the ks1293 manifest line, + one NEW jest file: 3 files, 3 edit points). lint rc 0 (empty stderr), dry-run rc 0 (no WARNING), CONTROL-PASS first (78 s), then ONE real round: `SPARK ROUND ks_1679_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 292fe0b1642a · 203s round, 126.765s model, 43443+4600 tok`.
- **Design choice: STRIP both keys (the KS-1508 / KS-1660 pattern) and log each drop, not spread the caller's data BEFORE the server's fields.** Line text, `certifications.ts:646`: `const { versionedById: droppedVersionedById, parentDocumentId: droppedParentDocumentId, ...dataWithoutVersionedById } = (data ?? {}) as Record<string, unknown>;` gains `certificationId: droppedCertificationId, certifiedAt: droppedCertifiedAt, `. Why: same idiom as the two sibling keys four lines above; the reorder stores the same blob but silently, and would leave two keys protected by strip and three by position in one object literal; a position fix is not pinned by any log cell. The reorder was run as a mutant (below): the stored-blob cells stay green, R4 and R5 (the log cells) red.
- contentHash untouched (the ticket's exclusion), stated in the brief.
- The only live seat is the kintsugi deploy seat; nobody else touches `certifications.ts`. Open-PR overlap on GitHub was NOT checked.

## Pinned sha
`git ls-remote origin refs/heads/develop` after the fetch into the literal cache path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src` (`cat-file -t` = commit): `292fe0b1642a2c40cee18af863174f158ee7be51`, as the task said; it did not move (re-read before the dry-run, before the control and before the real round: same sha). The cache's local HEAD was still `f7d35d628cdc` (the screen-17 sha); round.sh builds its clone at the ls-remote sha. KS-1660's strip (`c9ab6b36ff92`) is in this tip (line 646).

## Ticket (read-only)
KS-1679, priority 3 (Medium), Backlog. Mechanism as filed: the server writes `title`, `certificationId`, `certifiedAt`, `parentDocumentId` and then spreads `...dataWithoutVersionedById`. At the tip the spread is at :667; the destructure at :646 and the two logs at :649-:654 are the lines KS-1660 added. Suggested shape: destructure out, log each drop with tenant and actor ids, cells per role, a control that no log fires with nothing supplied. All taken.

## Brief (dir `local-model/night/briefs/ks_1679_p1/`: `KS-1679.md`, `golden.diff`, `spark.pins`; tier code_patch2)
- Product: ONE hunk (`@@ -643,13 +643,20 @@`): 1 comment line added, the destructure line replaced by a longer one, 6 lines added (two `if (dropped… !== undefined) { logger.info('KS-1679: …', { tenantId: getReqTenantId(req), userId: issuer.id }); }` blocks). Hunk header carries no function-context text.
- Modified test: `ks1293-originate-suite-is-hermetic.test.ts`, one `SUBJECTS` line inserted after the ks1660 name (the new test mentions the anchoring env key; without the line the MANIFEST-DRIFT cell is red, measured: 1 failed / 10).
- New test `ks1679-the-same-caller-spread-still-overwrites.test.ts` (173 lines; the name is the builder's title slug, per the screen-16 finding; confirmed by the dry-run). Cells: R1 certificationId overwritten (ISSUER_ADMIN and SYSTEM_ADMIN), R2 certifiedAt overwritten (both roles), R3 non-string values for both keys (both roles), R4 certificationId drop logged with the tenant and without the value, R5 same for certifiedAt, C1 CONTROL the server's values persist (stored `certificationId` = the 201 body's `id`, stored `certifiedAt` = its `issuedAt`, route parent kept, caller's other data and title kept), C2 CONTROL other caller keys pass beside both planted keys, C3 CONTROL no KS-1679 log with neither key. 13 cells: 8 red at develop (assertion reds: "Expected uuid, Received CALLER-CERT-ID" and the like), 13/13 with the edit. Labels `RED KS-1679 Rn:` / `CONTROL KS-1679 Cn:` are in `## Red cells` and the titles (the screen-16 trap).
- Server values asserted as the 201 body's `id` and `issuedAt` (route :489 sets `issuedAt: now`, the same `now` the derived row uses), plus UUID and ISO regexes on them, so a cell cannot go green by two wrong equal values.

## Design choices (Wednesday's rule): choice / rejected alternative run as a mutant BEFORE the brief / cell that reds
All mutants run by hand in the scratch clone `/private/tmp/wed_screen18/clone` (develop `292fe0b1642a`) with `mut.py` (jest on the new test plus `tsc --noEmit`, file restored after each).

| choice | alternative mutated | cells that red (each of 13 otherwise green) |
|---|---|---|
| strip both keys and log | M1: no strip, no log, server keys written AFTER the spread | R4 R5 (2 failed / 13); R1 R2 R3 stay green, which is why the log cells exist |
| strip both | M2: only `certificationId` stripped | R2 R3 R5 |
| strip both | M3: only `certifiedAt` stripped | R1 R3 R4 |
| log only when supplied | M4 / M5: guard flipped to `=== undefined` (one per key) | C3 R4 R5 each |
| log never carries the value | M6: `dropped: droppedCertificationId` added to the log context | R4 |
| log carries the tenant | M7: tenantId removed from the certifiedAt log | R5 |
Compile check: every mutant ran `tsc --noEmit -p tsconfig.json`; each printed exactly the ONE error the unmutated tip prints in my scratch clone (`adminConfig.ts(25,3) TS2305 isProvisioningCapable` missing from a stale shared dist, the screen-16 note), and no other `TS####`. The checker's own baseline in its built clone is `tsc rc=0`, so that error is the scratch clone's, not develop's.

## Rounds
| step | result |
|---|---|
| lint | rc 0, empty stderr |
| dry-run | rc 0, no WARNING; `code_patch2: product_files=1 test_files=[ks1293 modified, ks1679 new]`; endpoint was DOWN at that moment (`curl rc=7`); the real round's own `tunnel.sh up` brought it up (no human step) |
| control | `SPARK ROUND ks_1679_p1: CONTROL-PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 292fe0b1642a · 78s round, no model (control)` (`runs/spark_secuura_2026-10-20_ks_1679_p1-control`) |
| real round (ONE) | `SPARK ROUND ks_1679_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 292fe0b1642a · 203s round, 126.765s model, 43443+4600 tok` (`runs/spark_secuura_2026-10-20_ks_1679_p1`) |

Checker lines: `A3x declared=3 measured=3 ok=3 diff=0`; `A4 RED-FIRST (8 failed / 23 run; controls green; assertion reds)`; `A5 (23/23)`; `baseline total=1555 failed=0 | after total=1568 failed=0`; `A6 no NEW red`; `A7 tsc rc 0 (baseline rc=0)`; `RESULT: PASS (7/7)`; `A2a hunks=2 ok=2 bad=0 skipped_newfile=1`. **Accommodation check:** `decl_splice_3.out` = `spliced 0`, `tdz_inline` = `inlined 0`, every `section_N.opts` names the plain `section_N.diff`, `cmp section_3.diff section_3.decl.diff` equal. No FAIL, no rebrief, no refusal. First attempt at everything, because the fetch was done before every control and round.

## Things Wednesday should read before holding
1. **Display, not a trust decision**, as the ticket says (the KS-1557 read side already re-checks the id). Only the derived document's stored blob changes. The echoed 201 `data`, `certification_metadata` and the top-level `contentHash` (an explicit `||` chain preferring `data.contentHash`) still carry caller input; the contentHash is the ticket's own exclusion and a separate decision.
2. Same file as KS-1660 in the same block: if another seat edits lines 640-655 expect a rebase. Open-PR overlap NOT checked (KS-1656, 1659, 1664, 1559 name the file).
3. Forward-only: rows already written keep what the caller planted (the ticket says no backfill).
4. Two log lines per request when both keys are planted; each names only the tenant and the actor.
5. Cells read the record handed to the mocked save, not `metadata->>'certificationId'` in Postgres.

## NOT done / NOT tested
- No Postgres, no real anchoring, no open-PR query, no whole-workspace run beyond the checker's A6/A7 for originate. No hold, no raise, no `hold_ready`. No IMPROVEMENTS row (nothing new found: the fetch-before-every-round, label-substring, ks1293 manifest and builder-slug rules from screens 16 and 17 were all applied and all held).
- Housekeeping: `spark/cache/work/` gained 2 per-round clones (control and real), `spark/state/dry/` one dry-run input; the cache clone fetched develop `292fe0b1642a` (its HEAD is unchanged).

## Files written
Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1679_p1/` (`KS-1679.md`, `golden.diff`, `spark.pins`). One `#` line in `local-model/spark/queue.md`. Scratch (not durable): `/private/tmp/wed_screen18/` (get.py, clone/, h.sh, mk.py, mut.py, mkbrief.py, edit.py, golden.diff, red/green/mutant outputs, lint/dry/ctl/real outputs).
