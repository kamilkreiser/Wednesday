# B616 DRAFTER-REPORT (Sonnet 5.5, 2026-10-25 ~01:30-01:50 AEDT, read-only; wrote only the brief and this report)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-25_B616_SEAT-J7_composer-c-db-0026-0027-rows.md` (137 lines; 10 lines carry the four-underscore pattern: line 7 the model receipt, lines 113-120 the eight stamp slots, line 137 the last line; non-ASCII = only middle dots, as in the B587 brief).

## BLUF
Lane C-DB is startable tonight as one Sonnet seat (SEAT-J7, pane `Datasec/Security-Composer-J7`, ports 9660-9669, branch `b616/composer-c-db-0026-0027`) in three parts: P1 two db rows (B593-9, B593-10) in one new test file; P2 migration 0026 (PCOMP-17 CHECK) + reverser + DEPLOY section + up/down tests; P3 migration 0027 (PCOMP-14 index) + same. Base main `e019ac3abf628cbb6a50eb871b8f65b86a58ff6e`. No contract, API or web change; no word shown to a user. Two real risks are written into the brief as STOPs/measurements: the CHECK can fail a hosted database that holds a non-hex hash (cannot be measured from here), and a `char(64)` padding trap.

## Decisions for Tuesday at stamp (D1..Dn)
- **D1 Folder name.** Confirmed: the project folder is `/Volumes/Laptop-DEV/!CODING/Datasec/Datasec Security Composer` (cockpit/repo say "Security-Composer"). Recommend: as written.
- **D2 STATUS path.** Convention confirmed from 2026-10-24 files: `1_Project_Definition/Briefs/<date>_B<n>_STATUS.md`, so `2026-10-25_B616_STATUS.md`. Recommend: as written.
- **D3 Hosted-data risk of the CHECK (PCOMP-17).** The seat measures repo writers and every fixture the tests load, and STOPs if any violates. It cannot see any hosted DB (no az/HTTP). The migration, if a hosted row is non-hex, FAILS and rolls back whole at deploy. I put a read-only pre-deploy count query into the DEPLOY 0026 section for the operator. Recommend: accept; before any deploy card, someone with Kam's word runs that count on the demo DB. Alternative (not recommended unless a violator appears): `NOT VALID`.
- **D4 B593-9/-10 as rows without tickets.** They are gate findings, not Jira tickets (the sweep confirmed 0 hits); the records seat should open tickets before the PR lands. Recommend: ask the records seat for two PCOMP tickets so the PR can cite keys.
- **D5 Gate tier / model.** Tier 1 (migrations) as you stated; recommend Opus gate, as B593 was. Builder Sonnet as stated.
- **D6 Time boxes.** I suggested target READY +3h, hard stop +5h (smaller than B587's 5h/7h: 2 migrations, no API). Recommend: accept or tighten.
- **D7 Load threshold.** Used "below 7 at two reads 4 s apart" for db stacks (B593 ADDENDUM-1 rule), not B587's 6. load1 was 6.14 at 01:28. Recommend: keep 7.
- **D8 Names.** I let the seat pick migration file names (suggested `0026_last_generate_input_hash_form.sql`, `0027_audit_event_entity_index.sql`) and the index name `audit_event_entity_idx` (check convention). Recommend: accept; the lane's glob `0026_*`/`0027_*` covers any name.
- **D9 J6 co-existence.** The brief tells J7 to read nothing of J6's brief/STATUS and to use `b616`/`J7` names for locks, containers, networks, db names. If J6's brief gives a different lock path or ports that overlap 9660-9669, J6's wins on its own block; please confirm J6's block does not overlap (I only know 9640-9679 was empty at 01:28).

## Facts in the brief, with instrument
- Main sha `e019ac3a...` committed 2026-10-24T10:11:22Z, message "Structure: ... (migrations 0023-0025) (#87)": `gh api -X GET repos/datasecau/Datasec-Security-Composer/commits/main`; `git ls-remote origin refs/heads/main` agreed (01:28). Local clone does NOT hold that object (`git cat-file -t` failed), so the brief tells the seat to fetch once.
- Migrations on main: 25 files, last `0025_attribute_overrides.sql`; rollback holds 7 (0019-0025); db test files listed: gh api `git/trees/main?recursive=1`.
- Open PRs: #86 (dependabot vite) and #85 (draft): `gh api pulls?state=open` (file lists RELAYED from the B587 brief, re-run is a REFUSE step).
- Branches: ls-remote `refs/heads/b6*`, `b5*`, `b4*` showed b42..b69 old branches and `b587/...` at `6acb1819`; no `b616*`. (b61/b65/b67 etc. are historic, listed not stops.)
- Panes at 01:28: `tuesday`, `Datasec/NexusAI-G92`, `fleet-monitor`. Ports 9640-9679: `lsof` empty.
- PCOMP-17 and PCOMP-14: Jira GET; both Backlog, labels `composer-seed-1023` + `plan-comp-178`/`-152`, zero comments; text quoted in brief. PCOMP-22 also read (excluded).
- `last_generate_input_hash char(64)`: `0020_generate_issues_kept.sql:22`, with CHECK `policy_version_last_generate_whole` (all six columns NULL or all set), grants INSERT/UPDATE to `pc_app`; only application writer `apps/api/src/routes/lifecycle.ts:294` (`= $3`, the engine's `resolution.input_hash`); tests writing it: `packages/db/test/b61-0020.db.test.ts`, `b61-0020-down.db.test.ts` (fixtures `hash("4")`-shaped); reader `apps/api/src/last-generate.ts:64`. Instrument: tarball of main in my scratchpad + `grep`.
- `audit_event` (`0001_core_schema.sql:439-447`): PK `(tenant_id, seq)`, trigger `audit_append_only`; no other index on it in any migration (grep `CREATE INDEX` ... `audit_event` empty); readers: `outputs.ts:175,274`, `authz.ts:228`, `routes/history.ts:150`, `routes/admin.ts:382`, `routes/common.ts:100`.
- Pattern: `0023` migration/recipe text, `b587-0023-down.db.test.ts` (shape(), refusals, control with a skipped DROP, `alreadyApplied` length 22/23/24), DEPLOY sections 0023-0025 at lines ~291-430, "A later migration" at 432, "Before a deploy that brings a migration" at 36-58; `scripts/test-db.sh` (pinned postgres digest, internal network); B587 db wrapper `dbtest.sh` names `pc-b587-*` (renamed to `pc-b616-*` in the brief).
- B593-9/-10 text, mutants G05b and G31, census, fix shapes: `1_Project_Definition/Briefs/2026-10-24_B593_STATUS.md` ~lines 340-356. G31 and G05b are applied in the brief as SCRATCH MIGRATIONS (not edits of 0025), so the targeted rows go red for their own assertion rather than via checksum pins; the B593 note that the first G05 attempt was killed for the wrong reason (dropped `search_path`) is carried in.
- Existing tests that count migrations (`toHaveLength(22/23/24)`) are `through`-based and unaffected by 0026/0027 (read); `schema.db.test.ts:573` and `wp4-0017` use dynamic counts. A census that lists policy_version constraints or audit_event indexes was NOT found by my greps (UNMEASURED; the brief tells the seat to look).

## UNMEASURED
No build/test/container/db run. Not measured: npm ci cache; the B587 wrapper still working; local `postgres:16` being the pinned digest (I saw two `postgres:16` tags only); base group counts; whether any other fixture writes a non-hex `last_generate_input_hash`; `canonicalHash` emitting lowercase hex (one grep by name found no definition under `packages/engine/src`); hosted data; planner use of the index at scale; the exact audit lookup predicates; J6's lock/port details; load at launch.
(I did not run the J6 or other seats' files. Two Jira reads only of PCOMP keys; no query slipped to another project; no other client's data was seen.)

## Not startable / out of the brief
PCOMP-22 (Opus, later), PCOMP-42/-44 (as in the sweep). Everything in the lane is startable.
Note for the records seat: the `DEPLOY.md` route-B text at ~:190-206 that PCOMP-22 will touch is forbidden to J7 (only new 0026/0027 sections are added), so the later Opus seat does not conflict by path but must rebase on J7's DEPLOY additions.
