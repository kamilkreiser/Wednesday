# KS-1145 A-SLUGONLYDRIFT-R16B ADD ONE CELL TO THE ks949 REAL-POSTGRESQL SUITE — AG7: a SLUG-ONLY tenant drift on a second id is repaired by the guard's `tenant_slug` arm (`UPDATE 1`, slug restored) — the coverage note CN-2 of the #973 gate (a one-arm `IS DISTINCT FROM` guard was invisible to the suite) — Wednesday's task for Ornith, TEST_ONLY, **ONE existing bash suite, ONE pure-insertion hunk, no product file** (written 2026-09-22 16:0x by the feed15 drafter; the ticket's item 2; item 1 (CN-1, ID3's capture-size assertion) is NOT in this brief — part B, tabled)

File: `Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh`
Tip: `3bad652d17cf111c1e2e1bed1ae7686894637487`
Farm: `shared+tsx`

Written from develop `3bad652d17cf111c1e2e1bed1ae7686894637487` (`git ls-remote origin refs/heads/develop` at 15:54 on 2026-09-22, read verbs only). The suite at that tip is **376 lines** (last change `818002259`, 2026-09-13, #973), read whole; its full content is in `files[...]` of your input. The product it judges is `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts` (last change `778e6cfe2`, 2026-09-21): the two-arm re-sync guard at **`:1043`** `AND (u.tenant_id IS DISTINCT FROM v.tenant_id::uuid OR u.tenant_slug IS DISTINCT FROM v.tenant_slug)` — the suite EXTRACTS that statement from the product source at `:125-:130` (awk over `mainPool.query(`), so a tamper on `:1043` is what every cell runs. Runner: **bash** (a `*.test.sh` suite, run by the checker as `/bin/bash <file>` from the clone root, bash 3.2.57). **The suite needs the workspace install and the shared build** (`:113-:114` `die`, not SKIP: `packages/shared/dist/index.js` and `node_modules/.bin/tsx`) — the `Farm:` line above tells the harness to farm them into the scratch clone before the suite runs (the 2026-09-22 opt-in; without it the bare clone dies at `:113`). A real PostgreSQL 15/18 from a Homebrew keg is started by the suite itself, unix-socket only, in its own mkdtemps (`:161-:184`); no TCP port is bound, and the live postgres on this box (`127.0.0.1:5432`) is never touched.

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the suite above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `startup-migrations.ts` or any other file: no product behaviour changes; ONE cell (AG7) is ADDED between AG5 and AG6, inside the auth-then-gateway section.

## What the change does (one paragraph)

Section 8 of the suite (`:286-:301`, "AG: auth-then-gateway") seeds the twelve users with auth's real `seedDemoUsers`, plants a drift on the contested id `...060` at `:291` — on BOTH columns (`tenant_slug='ks949-stale-slug'` AND `tenant_id='...dead'`) — and AG4 (`:296-:297`) asserts the statement re-syncs it. Because BOTH columns drift, a guard with only the `tenant_id` arm (`AND (u.tenant_id IS DISTINCT FROM v.tenant_id::uuid)`) still matches the row and the `SET` repairs both columns: the #973 gate's Tg3 tamper (the slug arm deleted) read `27 passed, 0 failed` — CN-2. Only a drift on the slug ALONE tells the two arms apart: the shipped guard reads `UPDATE 1` (the gate's R5 control), a one-arm guard reads `UPDATE 0` and the drift stays. AG7 plants exactly that on a SECOND id, `c1000000-0000-4000-8000-000000000001` (james.wilson, oxford-university — the second VALUES row of the statement at `:1030`), runs the extracted statement once more, and asserts BOTH the command tag `UPDATE 1` and the slug read back as `oxford-university`; then it puts the slug back by a direct UPDATE so every later cell (AG6's count, ID1-ID3's captures, the controls) sees the table exactly as it would without AG7 — ID2 compares the `:293` snapshot `$A` with the post-idempotence snapshot, and the restore keeps them equal under every arm. `TOTAL_CELLS` at `:82` is NOT changed in this brief: the tally line prints `(of 27 cells)` while 28 cells print `ok`; the checker counts printed cells, not the constant (part B carries `27 -> 28` with CN-1 — said plainly in the raise notes).

## The exact change — ONE hunk in the suite

A PURE INSERTION of 12 `+` lines between `:299` (the AG5 line, leading context) and `:300` (`N12=$(COUNT12 ag); ...`, trailing context) — both unique in the file, both ASCII. Copy every line byte for byte. Every `+` line is ASCII only, carries NO backslash, NO backtick, no `printf`, no bash-4 idiom (`[ ]`, `$( )`, a here-string `<<<` as the suite's own `PSQL` calls use at `:291`, `ok`/`bad` as at `:85-:86`). The three `#` lines are comments and stay. `$STMT`, `$ID0001`, `$OUT7`, `$SL7` are plain `$name` expansions inside double quotes — no `${}`, no arithmetic. There is no blank line anywhere in the fence. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh` then `+++ b/Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh`.**

```
@@ -299,2 +299,14 @@
 [ "$NB" = "$NA" ] && ok "AG5: names, role and status untouched on all 12 rows" || bad "AG5: the statement changed names, role or status"
+# KS-1145 (CN-2 of the #973 gate): a SLUG-ONLY drift on a second id. AG4's drift is on BOTH
+# columns, so a guard with only the tenant_id arm still repairs it; a drift on the slug alone
+# is the one the tenant_slug arm of the guard (startup-migrations.ts:1043) exists for.
+ID0001="c1000000-0000-4000-8000-000000000001"
+PSQL ag <<<"UPDATE users SET tenant_slug='ks949-slug-only-drift' WHERE id='$ID0001';" >/dev/null
+OUT7=$(PSQL ag <<<"$STMT"); SL7=$(PSQL ag <<<"SELECT tenant_slug FROM users WHERE id='$ID0001';")
+if [ "$OUT7" = "UPDATE 1" ] && [ "$SL7" = "oxford-university" ]; then
+  ok "AG7: a slug-only drift on ...0001 is repaired by the guard's tenant_slug arm (UPDATE 1, slug restored)"
+else
+  bad "AG7: a slug-only drift on ...0001 is NOT repaired - command tag '$OUT7', slug reads '$SL7' (the guard's tenant_slug arm is gone or inert)"
+fi
+PSQL ag <<<"UPDATE users SET tenant_slug='oxford-university' WHERE id='$ID0001';" >/dev/null
 N12=$(COUNT12 ag); NT=$(PSQL ag <<<"SELECT count(*) FROM users;")
```

Do NOT touch `:291` (AG4's both-column drift), `:296-:297` (AG4), `:300-:301` (AG6), section 9 (`:303-:318`, ID1-ID3), `TOTAL_CELLS` at `:82`, or the controls. Do NOT add a `printf`. Do NOT rename the cell: the checker names it by the literal prefix `AG7:`.

## Cells

- `ag7` = `AG7:`
- `ag4` = `AG4:`
- `ag6` = `AG6:`
- `ga1` = `GA1:`
- `id3` = `ID3:`
- `src1` = `SRC1:`

## Red cells

- AG7: (the ONE cell this diff adds — GREEN at the tip with the hunk applied, RED under SLUGARMGONE and under GUARDINERT)

## Tampers

Both tampers are ONE-line edits of the product's guard at `startup-migrations.ts:1043` (the `From` occurs EXACTLY ONCE in the file as a whole line — python whole-line scan: 1 hit at 1043). The suite reads the statement FROM the product source (`:125-:130`), so the tampered guard is what `$STMT` carries in every cell. The checker plants each and restores the file by bytes (T8).

### SLUGARMGONE — the guard keeps only its tenant_id arm (the #973 gate's Tg3, the tamper CN-2 says the suite cannot see): AG4's both-column drift is still repaired (green), a slug-only drift is not
File: `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts`
Line: 1043
From:
```
          AND (u.tenant_id IS DISTINCT FROM v.tenant_id::uuid OR u.tenant_slug IS DISTINCT FROM v.tenant_slug)
```
To:
```
          AND (u.tenant_id IS DISTINCT FROM v.tenant_id::uuid)
```
Reds: `ag7`

### GUARDINERT — the guard is made always-true (`OR true`): every boot rewrites all twelve rows, so ID3's no-change run reads UPDATE 12 and AG7's slug-only run reads UPDATE 12, not UPDATE 1
File: `Blockchain/Dev/services/api-gateway/src/startup-migrations.ts`
Line: 1043
From:
```
          AND (u.tenant_id IS DISTINCT FROM v.tenant_id::uuid OR u.tenant_slug IS DISTINCT FROM v.tenant_slug)
```
To:
```
          AND (u.tenant_id IS DISTINCT FROM v.tenant_id::uuid OR u.tenant_slug IS DISTINCT FROM v.tenant_slug OR true)
```
Reds: `ag7`, `id3`

## Controls

- `ga1`
- `ag4`
- `ag6`
- `src1`

*(All are literal prefixes of the descriptions the suite prints — `GA1:` `:275`, `AG4:` `:297`, `AG6:` `:301`, `SRC1:` `:340-:341`, `ID3:` `:315`/`:317`; each prefix names exactly one cell (the `ok` and `bad` lines of a cell share it). Under SLUGARMGONE: AG4 stays green because its drift is on both columns and the id arm matches; AG6 stays green because AG7 creates no row (an UPDATE on an existing id, then a restore); ID3 stays green because the one-arm second run still writes nothing (UPDATE 0) — exactly the blindness CN-2 names, now caught by AG7 alone. Under GUARDINERT: AG4 green (everything is rewritten, the drift included), AG6 green, SRC1 green (the statement is still an UPDATE naming no PII column); ID3 red at the tip already (its purpose) and AG7 red (UPDATE 12).)*

## THE CHANGE — state it to yourself before you write a line

At the untouched tip the suite is `27 passed, 0 failed (of 27 cells)`, rc 0 (measured on the farmed scratch clone, PostgreSQL 15.14). With this hunk: `28 passed, 0 failed (of 27 cells)`, rc 0 — AG7 green (`UPDATE 1`, slug `oxford-university`). Under **SLUGARMGONE** with this hunk: AG7 red (`command tag 'UPDATE 0', slug reads 'ks949-slug-only-drift'`), every other cell green, `27 passed, 1 failed`, rc 1. Under **GUARDINERT** with this hunk: AG7 red (`command tag 'UPDATE 12'`) and ID3 red (`command tag 'UPDATE 12', 12 of 12 updated_at moved`), `26 passed, 2 failed`, rc 1. Under SLUGARMGONE WITHOUT this hunk: `27 passed, 0 failed` — the blindness the ticket names (measured by the #973 gate as Tg3, 0 red). All reds are assertion reds (no bash diagnostic).

## Premises (measured by reading the tip)

- **Premise: the anchor.** `:299` and `:300` are non-blank, ASCII, and each occurs once (`grep -c -F -x` 1 / 1); `:302` is blank and is NOT in the fence (the insertion sits before AG6, not after it, because `:302` is blank and a hunk cannot end on it).
- **Premise: the From line.** `startup-migrations.ts` at `3bad652d1`, line 1043, byte for byte, occurs once as a whole line; `:1030` is the `...0001` VALUES row (`'c1000000-0000-4000-8000-000000000001', 'b1000000-0000-4000-8000-000000000001', 'oxford-university'`), so the restored slug is the statement's own value.
- **Premise: `PSQL` prints the command tag.** `PSQL()` at `:186` runs `psql -tA` WITHOUT `-q`, so a bare `UPDATE` answers its tag (`UPDATE 1`) as the whole output — ID3 at `:314` already compares `"$OUT" = "UPDATE 0"` the same way.
- **Premise: the cell names.** `AG7` occurs 0 times in the suite at the tip (control: `AG6` 1); no declared prefix is a prefix of another.
- **No backslash** in any `+` line (0, counted); **no backtick** (0); **no non-ASCII** (0); no bash-4 idiom; the suite after the fence parses (`bash -n` rc 0).
- **Premise: the surface.** A shell suite that starts its own PostgreSQL over a unix socket in `mktemp -d` dirs and removes them on EXIT (`:168-:173`); nothing outside `$TMPDIR` and the clone is written. Not an auth surface.

## Collision

`scripts/__tests__/ks949_main_seed_idempotence.test.sh` is in NEITHER round-19 brief's GROUPING/QUEUE (0 of the 47-path union; 10 other `scripts/__tests__/*.test.sh` are — the file is not among them); `startup-migrations.ts` is not edited (a tamper is planted and restored by the checker). `night/queue.md:70` lists KS-1145 under REJECTED ("a bash test suite, not vitest") — written before the 09-18 bash runner and the 09-22 farm. Sequencing needed: none. The `Blockchain/Dev/scripts/` directory is Seat C 19th's lane by directory (a different file) — Wednesday rules at queue time.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh` / `+++ b/Blockchain/Dev/scripts/__tests__/ks949_main_seed_idempotence.test.sh`, then the hunk above exactly as shown (`@@ -299,2 +299,14 @@`). Every one of the 12 `+` lines is its OWN physical line (the INPUT JSON shows this brief's line breaks as the two characters backslash and n inside a JSON string — DECODE them; a `+` line that carries a backslash is a FAIL).

## Notes for the raise (not for the model)

- Test-only, zero product bytes, one new cell. **Raise tier: TIER 2 (a scripts/__tests__ shell suite; no service, no runtime image).** **Refs KS-1145** (item 2 / CN-2). **NEVER Closes** — item 1 (CN-1) is part B.
- **Part B (NOT in this brief):** CN-1 folds a capture-size assertion into ID3's condition at `:314` and bumps `TOTAL_CELLS` `27 -> 28`; its neighbours `:313` (a `printf '%s\n'` backslash) and `:315` (an em-dash) are the context lines the model has collapsed on before, and CN-1 has no product tamper that reds it — brief it when a modify-in-place shape for those two lines is measured. The tally with this hunk alone prints `28 passed ... (of 27 cells)`; the raiser bumps `TOTAL_CELLS` in the same PR or takes part B.
- **Harness:** this is the first brief carrying the `Farm:` line (tasks/test_only/prepare_clone.sh + build_test_only_input.sh, 2026-09-22 15:5x, backups `.pre-0922-1558-bashfarm`).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1145 night/inputs/test_only_1145SLUGONLYDRIFT-R16B.json night/briefs/KS-1145-R16B-SLUGONLYDRIFT.md tip=3bad652d17cf111c1e2e1bed1ae7686894637487 ctx=65536
```
