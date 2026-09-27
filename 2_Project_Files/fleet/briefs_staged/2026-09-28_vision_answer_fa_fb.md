# BLUF: F-B = option (3), BOTH, as its own ticket stacked on VSP-70's branch. F-A = measure first, then build the full backup list. VSP-68 joins gate 11 (tier 2). Keep VSP-70's head at 10ba4bb untouched while gate 11 runs.

## F-B (restore empties a live table whose dump failed) — RULED (3)
- Default: the restore REFUSES a backup that carries any failed table (metadata.failed_tables non-empty, or any tables[t].error), and names them; `--allow-incomplete` lets an operator proceed on purpose.
- Even with that flag, clearTables() NEVER deletes a table whose entry carries .error (defence in depth: a flag is a human decision, emptying a table is not).
- File it as a NEW VSP ticket. Build it on a branch stacked on 10ba4bb (VSP-70), NOT on VSP-70's own branch: gate 11 is pinned to 10ba4bb and a moving head voids it.
- Red first, with a real-Postgres cell: a backup JSON with one failed table, restored into your own database. Today the table is emptied; after the fix it is refused, and with the flag the table's rows survive.
- It goes to the next Vision gate, not gate 11.

## F-A (the backup omits most PRO tables, quotes included) — MEASURE FIRST, then build
1. Establish whether the 10-table list is STALE or DELIBERATE: `git log -S` on TABLES_TO_BACKUP and RESTORE_ORDER, against when each missing table's CREATE TABLE entered schema.sql. Quote the dates.
2. Excluding `session` is right: live sessions must not be restored. Say so. Name anything else you would deliberately exclude, with the reason.
3. File the ticket carrying that measurement plus the proposed list and a foreign-key-safe RESTORE_ORDER, derived from schema.sql's REFERENCES clauses (show the derivation).
4. Then build it (backup list + restore order + a cell asserting that every schema.sql table except the named exclusions is in TABLES_TO_BACKUP, so the list cannot drift again). Stack it after F-B, because both touch dbRestore.js.
- Your grep of CREATE TABLE is a claim about the code, not about production's catalog; production is unread (the firewall) and stays so. Say that in the ticket.
- Tuesday tells Kam today that the live nightly backup does not contain quotes. That is his to know; the fix reaches production only with his deploy word.

## VSP-68
Accepted into gate 11 as a fourth target, TIER 2 (internal alert only, no client-facing effect).

## ORDER
Continue VSP-73 now if it is quick. Otherwise F-B, then F-A, then VSP-73, VSP-69, VSP-72.

-- Tuesday
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 06:18
