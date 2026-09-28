# QA Agent Invocation Brief — Datasec/Vision_Sales_Portal, GATE 13: a NARROW RE-GATE on portal main `e59232e` — VSP-74 ROUND 2 OF 2 @ `4813e5f` (G12-F1 only, TIER 1) and VSP-75 NEW HEAD @ `110bb03` (41c4a66 + VSP-74 r2 + main e59232e, TIER 1)

**⚠ VSP-74 IS ROUND 2 OF 2 OF ITS CLASS. A NO-GO of VSP-74 here goes to Kam, not to another round.** Gate 12 spent the class's first
NO-GO (VSP74-G12-F1 at `a1794ad`). A failure rooted in VSP-74's code (`restorePlan()`, `liveTables()`, the closure, `clearTables()`)
counts against VSP-74's class **whichever head you measure it on** (it is the same code at `4813e5f` and `110bb03`) — **except** a
row lost through the pre-existing bare-name delete/insert path, which is graded by §TUESDAY'S RULINGS item 1 (STAMPED). A failure in VSP-75's
own scope (the backup side, `backupTables.js`, `dbBackup.js`, the absent-table rule, FIX 1/FIX 2) would be VSP-75's FIRST NO-GO (gate 12
GO'd `41c4a66`).

**Drafted for Tuesday on 2026-09-28 at 11:1x-11:3x AEST by a read-only drafting agent. Tuesday reviews, stamps and launches it.**
Template: gate 12's brief `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-gate12-vsp74-vsp75-vsp69.md`
(read it as PRIOR WORK for its method, §13 and its instruments; **this brief governs where they differ**).

**WHY THIS GATE IS NARROW (read this before planning).** Gate 12 measured VSP-75 `41c4a66` GO on its own scope (census, round trips,
secrets, injector, F1, lazy tables, FIX 1/FIX 2, size) and VSP-69 `e79682a` GO (now on main as `e59232e`). **Do not re-derive all of that.**
What changed since gate 12 is exactly: (1) VSP-74's `restorePlan()` rewritten to match tables and FK edges by OID over every user schema
(`4813e5f`, 3 files); (2) that merged forward into VSP-75 (`4843aed`, conflict in `restorePlan()` and its unit file only); (3) main
`e59232e` (VSP-69) merged into VSP-75 (`110bb03`, `BACKLOG.md` only). VSP-75's backup-side blobs are byte-identical to the GO'd `41c4a66`
(the launcher proves it). So this gate: **§N1 proves F1 closed and hunts its class; §N2 proves nothing regressed, on a fixed short list of
gate 12's own cells; §N3 notes F2/F3/P1 only if seen.** Anything else is out of scope unless a measurement in scope points at it.

The builder's READY mails under test (on disk, each read whole by the drafter):
- VSP-74 round 2: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp74-r4-READY-mail.txt` (dated 2026-09-28T01:17:30Z)
- VSP-75 new head: `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-28_vision-vsp75-r4-READY-mail.txt` (dated 2026-09-28T01:17:31Z)
(The `r4` in the file names is Tuesday's filing sequence; the mails call them "VSP-74 ROUND 2 of 2" and "VSP-75 NEW HEAD".)
**Every builder statement below comes from those mails, the commit messages or the BACKLOG at each head. Each one is a CLAIM. Every red,
every mutant and every suite set must be RE-DERIVED by the gate. None is taken from a READY.**
The launcher parses §PIN, refuses any placeholder, and re-reads EVERY row by `git ls-remote` immediately before launch, refusing on any
mismatch. The verified table is appended to your prompt.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-28 11:34
Re-read by Tuesday's drafting subagent on commission; Tuesday reviews the WRONG list before launch.
Self-check note: tier 1 x2; VSP-74 round 2 of 2 (NO-GO -> Kam); VSP-75 re-gate of a GO'd scope, narrow; VSP-69 is on main and not a target; one merge (VSP-75's head, a fast-forward of e59232e); CI UNMEASURED; production untouched.

NODE20-LEG: DOCKER-PULL-NEVER
<!-- Commissioned "as before" (gate 12 ran DOCKER-PULL-NEVER: `docker image inspect node:20` then `docker run --rm --pull=never` of the
     image ALREADY present; nothing is ever pulled; if the image is absent the leg is NOT RUN and the report says so). The launcher refuses
     anything else (exit 45). Re-prove the image (§N2.8). -->

GATE11-MERGED: 1976275635185db4551d5e3b015a66971f4563a5 5bdaeae6e28e280be380042a3dc8a56dbada0293 10ba4bbd29e34bf601426b68328f63725e228a86 7ef698d7e8c00c4c8e87060bec9f5284dfe8082a 6d7ea736b4f718cddd2e152f1ee0234d42d97bfe
<!-- Carried from gate 12 (the five gate-11 GO heads, all ancestors of main). The launcher requires each on MAIN-P (exit 9). -->

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent
tester. You did not build any of these changes and you owe the builder nothing. **Every line below that reports what the builder says
is a CLAIM, never evidence.**

**One gate, TWO targets, TWO verdicts (GO / NO-GO each, at its pinned sha), plus ONE merge line.**
- **VSP74** at `4813e5f` — **TIER 1 (Tuesday's ruling at gate 12, unchanged).** ROUND 2 OF 2. Why: the DESTRUCTIVE restore path. Its job is
  to decide which live tables a restore empties or changes; a wrong answer is deleted production data. Round 2 fixes ONLY gate 12's
  VSP74-G12-F1 (the closure compared FK endpoints as quoted / schema-qualified `regclass` text against bare `public` names; now by OID over
  every user schema). F2, F3 and P1 are NOT built (ticketed as VSP-81).
- **VSP75** at `110bb03` — **TIER 1 (Tuesday's ruling at gate 12, unchanged).** The NEW HEAD: `41c4a66` (GO at gate 12) + VSP-74 round 2
  merged forward (`4843aed`) + main `e59232e` merged in (`110bb03`). **This is the head that will actually merge; it contains VSP-74.**
  Graded on (a) the F1 cells ON THIS HEAD (VSP-74's code as merged, with VSP-75's absent rule re-applied on it in the conflict resolution)
  and (b) no regression of gate 12's VSP-75 GO.
- **MERGE LINE:** `110bb03` contains main `e59232e` (0 behind), so the merge is a fast-forward if main has not moved; say so from YOUR OWN
  object dir. VSP74's head `4813e5f` is NOT merged on its own (it is 3 commits behind main, the VSP-69 chain, by design: it reaches main only
  through VSP-75 — gate 12's MERGE COUPLING).

**⚠ Names, written out every time:**
- **VSP74 = Jira VSP-74 = "F-B"**: a restore emptied a live table whose dump had failed. **VSP74-G12-F1** (gate 12, Major, graded FAIL by
  Tuesday's stamp ruling): an outside table named `"QA_Outside"` with a CASCADE key to `leads` was announced kept and emptied 2 → 0 under
  `--allow-incomplete` (SET NULL: `lead_id` 1,2 → NULL,NULL); a table in another schema with a CASCADE key to `public.leads` was not refused
  and emptied 2 → 0 with no flag.
- **VSP75 = Jira VSP-75 = "F-A"**: the nightly backup named 10 tables; the PRO tables were never in it.
- **VSP74-G12-F2 / F3 / P1 = VSP-81** (the plan/clear window; silently lost child rows under a kept parent; the flag-less warning line and the
  ignored `--allow-incomplet` typo). NOT in this round.

Branches: `fix/vsp-74-restore-refuses-incomplete-2026-09-28`, `fix/vsp-75-backup-all-tables-2026-09-28`. **Neither is on main.**

## RULED BY KAM, AND SETTLED
- **Vision `1_Project_Definition/CLARIFICATIONS.md`** (`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/1_Project_Definition/CLARIFICATIONS.md`):
  read it whole. **It now carries C-01..C-07. C-07 (new since gate 12) records the settled shape of this round:** "every user table (all
  schemas except `information_schema` and `pg_*`) by OID; a non-public table counts as outside only when it has rows AND its FK chain reaches
  a restored table; outside is refused by default and kept with its parents under `--allow-incomplete`", from Tuesday's ANSWER of
  2026-09-28T00:59Z ("Keep the lower-case control cell from a1794ad green"). **C-07 is Tuesday's ruling, recorded in the clarifications file;
  it is not Kam's.** The launcher checks C-07 is present and prints a NOTE on any C-08.
- **Kam's F-B ruling "(3) both"**: the restore refuses an incomplete backup AND never empties a table it cannot restore. **That is the one
  product ruling that is Kam's.** Every §N1 cell is graded against it, **as Tuesday's stamped ruling 1 applies it** to the pre-existing
  bare-name delete/insert path (search_path shadowing, inheritance).
- **PRODUCTION IS LIVE for this project.** `datasec-sales-portal-rg` holds the live site `https://datasec-sales-portal.azurewebsites.net`,
  its production Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault `datasec-sales-kv`. Production runs Node 20
  (`.github/workflows/test.yml`, blob `0cb2d05`, unchanged at every head). **The restore CLI is run against production by an operator.
  Nothing in this gate touches production** (§13, HELD).
- **Tuesday's rulings (not Kam's), carried from gate 12:** both tiers; "if any cell loses or changes a row of a table the plan must keep,
  that is a FAIL of VSP-74 (Tier 1), not an observation"; the product-test database ruling (every `test:db` via YOUR `TEST_DATABASE_URL`; a
  write to `salesportal_test_lazy` or any builder database is a FAIL of VSP-75 and STOPS that arm); VSP-69 GO'd and merged.
- **The BUILDER's choices in round 2, each judged by the gate (say whether each needs Kam):** a non-public table without an FK path to a
  restored table is NOT outside even with rows (C-07); partitions excluded, partitioned parents included; labels `schema.table` outside
  public; identifiers quoted only in the row check (the clear and the inserts still use `"<name>"` unqualified — §WRONG (b)).
- **Deploys are HELD for Kam. Nothing merges on your word.** A merge is Tuesday's GO on a pinned head. A deploy is Kam's word.

## PRIOR ROUND
PRIOR ROUND: gate 12 (QA/Vision-gate12, 2026-09-28 09:27-10:55 AEST): **VSP74 NO-GO at `a1794ad` (VSP74-G12-F1)**, VSP75 GO at `41c4a66`
(on its own scope; "cannot merge while it contains `a1794ad`"), VSP69 GO at `e79682a` (merged since as main `e59232e`), merged tree
BACKLOG-ONLY. **Class count: VSP-74's class has ONE NO-GO spent; this is its ROUND 2 OF 2 and a NO-GO goes to Kam. VSP-75's class has
none spent.**
ITS REPORT IS ON DISK AT: gate 12 `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate12-three-targets`
(`report.md`, 700 lines). **Read at least: VERDICTS, VERBATIM OPERATOR STRINGS, N1.3 (the cascade matrix), N1.6 (refusal changes nothing),
N1.10 (THE NO-GO: the closure's identifier and schema hole), N2.9 (the deploy-time table), N4 (THE REQUIRED CELL), N5.2-N5.5 (suites,
coverage, hygiene, Node 20), FINDINGS INDEX, THE QUEUE ("Order I recommend … (3) re-gate that head: the closure cells here (mixed-case
CASCADE/SET NULL, other-schema), the cascade matrix, §N4, §N2.9, the suites and merged coverage"), NOT TESTED, and its self-findings
1-8.** Its evidence: `evidence/vsp74/class-closure-identifiers.txt`, `class-closure-replication.txt`, `matrix-*.txt`, `refusals-*.txt`,
`evidence/vsp75/` (§N2.9), `evidence/suites/`, `evidence/coverage/`, `evidence/node20/`, and **`evidence/tools/`** (50 files).
- **Instruments are REUSED BY COPY from gate 12's `evidence/tools/`** (`qa-harness-g12.cjs`, `qa-g12-db.cjs`, `qa-g12-matrix.cjs`,
  `qa-g12-one.cjs`, `qa-g12-refusals.cjs`, `qa-g12-n29.cjs`, `qa-g12-backup.cjs`, `qa-g12-lazywatch.cjs`, `qa-g12-node20.cjs`,
  `qa-g12-clusterlist.cjs`, `mutate-g12.py`, `repoint-g12.py`, `run-node20-g12.sh`, `mkmerged-g12.sh`, `seed-g12.sql`, `qa-run.py`,
  `qa-floorcount.py`, `qa-harness-floorctl.mjs`, `qa-io1-preload-fetchguard.cjs`, `mktree-portal.sh`, `lockcmp.py`, `lockwalk.py`,
  `specsets.py`, `tapsets.py`, `run-suite.sh`). **COPY what you use into THIS gate's own `evidence/tools/`, read it before you trust it,
  and RE-POINT every hard-coded path and prefix** (gate 12's copies ENFORCE `vsp_qa_g12_` and hard-code `work-g12`). **Never edit, run
  from, or write into gate 1-12's copies, evidence, trees or databases.** Record the sha1 of each copy before and after your edits. Earlier
  gates' roles (`vsp_qa_g10_*`, `vsp_qa_g11_*`, `vsp_qa_g12_nofb`) are not yours: never use, alter or drop them.
- **Self-findings from gates 2-12 bind you:** quote every path (the project path has a space and a `!`); run every loop and every
  `git show <sha>:<path>` under **bash, not zsh** (gate 12's self-finding 1: a zsh loop did not word-split); pass SQL to a wrapper as base64,
  never through a whitespace-split env var (self-finding 3); compare a restored table against the BACKUP's rows, not the source DB
  (self-finding 2); never run a `nextval` check in one transaction across tables (self-finding 4); absolute recorder paths (self-finding 5);
  a snapshot classifier must handle a table absent before and after (self-finding 6); **the portal test-DB name MUST end in `_test`**;
  npm's update-notifier egresses unless you disable it; record the load average beside every timing number.
- **PRIOR WORK: verify every claim against git history and gate 12's evidence, never against this brief.**

## PIN — HEADS (parsed and verified by the launcher)
**The launcher enforces these rules:** every row has a 40-hex head, base and commit count, and no `@`; the head is a commit; the base is
an ancestor AND the merge-base with MAIN; `git rev-list --count base..head` equals `commits`; `git ls-remote origin refs/heads/<branch>`
equals the head NOW; no target is on main. **VSP74's base is `609e967` and it is behind main by EXACTLY the VSP-69 chain (`3ede8ed`,
`e79682a`, `e59232e`); VSP75's base is main `e59232e`, 0 behind.** Non-merge commits over each base must be exactly the chains below; every
merge has two parents, its second on main or (for VSP75) on VSP74. **Never rebased:** `a1794ad` is `4813e5f`'s single parent; `41c4a66`,
`4813e5f` and `e59232e` are ancestors of `110bb03`; `4843aed` = `41c4a66` + `4813e5f`; `110bb03` = `4843aed` + `e59232e`; `e59232e` =
`609e967` + `e79682a`. **Main:** origin main must be `e59232e` or a DESCENDANT of it whose diff from `e59232e` touches none of the targets'
files (NOTE); anything else refuses.

<!-- PIN-HEADS:BEGIN -->
| id | repo | branch | head | base | commits | status |
|---|---|---|---|---|---|---|
| MAIN-P | portal | main | e59232e1983cd9424b749cd5fea518838763f90f | - | - | IN |
| VSP74 | portal | fix/vsp-74-restore-refuses-incomplete-2026-09-28 | 4813e5f5c949d638d8aa82ce282b778d55dedced | 609e967d6b03ff77dcbd692ee6e4434a5027e70b | 9 | IN |
| VSP75 | portal | fix/vsp-75-backup-all-tables-2026-09-28 | 110bb03747d4c306810eeb610387aafecc7d394a | e59232e1983cd9424b749cd5fea518838763f90f | 23 | IN |
<!-- PIN-HEADS:END -->

Every row above: `git -C <portal> ls-remote origin` read by the drafter at **2026-09-28 11:19:36 AEST**, equal to each READY's head;
`cat-file -t` = commit for all three. Counts by `rev-list --count` (11:2x).

**The chains (READ 11:2x, `rev-list --no-merges`, `log --format='%h %p %s'`):**
- **VSP74 over `609e967` (9 commits):** gate 12's eight (non-merge `d2531ea` → `bf5bdc0` ; merge `987178c` = `bf5bdc0` + `609e967` ;
  `b7bc78b` → `011becb` → `57ecad6` → `f62917f` → `a1794ad`) **+ `4813e5f`** (parent `a1794ad`; "VSP-74 round 2: the restore plan matches
  tables and keys by OID, in every schema (gate 12 VSP74-G12-F1)"; `server/dbRestore.js` +47/−13, `server/dbRestore.plan.test.js` +35/−6
  (the 6 deleted lines are the scripted-catalog stub; no assertion line deleted), `test/db/restore-incomplete.test.js` +90/−0).
- **VSP75 over `e59232e` (23 commits = 15 non-merge + 8 merges):** gate 12's 14 non-merge + `4813e5f`; merges `987178c`, `e34add4`,
  `d7a5e77`, `987afab`, `949b72e`, `2ed83fe` (as gate 12) **+ `4843aed` (parents `41c4a66` + `4813e5f`; "Conflicts in restorePlan() and its
  unit file only") + `110bb03` (parents `4843aed` + `e59232e`; "BACKLOG.md conflicted in one hunk … 278 lines")**.
- **Main `609e967..e59232e`:** `3ede8ed` (VSP-69 fix, parent `0d992e0`), `e79682a` (its forward merge), `e59232e` (merge to main,
  "gate 12 GO"). Files: `BACKLOG.md`, `server/reminders/dispatcher.js` (→ `7a67be9`), `test/db/dispatch-once.test.js` (`c3b0d92`).

Repo: portal = `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/2_Project_Files` (remote
`datasecau/vision_datasec-sales-portal`). **The portal has no CLAUDE.md inside the repo;** its rules are
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Vision_Sales_Portal/CLAUDE.md` (read it; its deploy commands are NOT for you).

**The shape (READ 11:2x at the pinned heads; re-derive it):**
| file | `a1794ad` | **`4813e5f`** | `41c4a66` (GO) | `4843aed` | **`110bb03`** | main `e59232e` |
|---|---|---|---|---|---|---|
| `server/dbRestore.js` | `236f8ce` 289 l | **`ec48af7` 323 l** | `2ee8090` 299 l | `97421ec` | **`97421ec` 333 l** | `5f4b71d` |
| `server/dbRestore.plan.test.js` (`test(`) | `24a4dd3` (7) | **`fb88859` (10)** | `9b8a2e3` (9) | `e8cb5ee` (12) | **`e8cb5ee` (12)** | — |
| `test/db/restore-incomplete.test.js` (`test(`) | `da1d223` (12) | **`b282070` (17)** | `da1d223` (12) | `b282070` | **`b282070` (17)** | — |
| `server/dbBackup.js` | `5e31eb4` | `5e31eb4` | `0b38895` | `0b38895` | **`0b38895`** | `5e31eb4` |
| `server/backupTables.js` | — | — | `ad03428` | `ad03428` | **`ad03428`** | — |
| `server/dbBackup.test.js` (`test(`) | `4fb902e` (5) | `4fb902e` | `12a6e24` (10) | `12a6e24` | **`12a6e24` (10)** | `4fb902e` |
| `test/db/restore-old-backup.test.js` | — | — | `586d558` (2) | = | **`586d558` (2)** | — |
| `test/db/backup-coverage.test.js` | — | — | `5ffb1fe` (6) | = | **`5ffb1fe` (6)** | — |
| `test/db/backup-lazy-absent.test.js` | — | — | `5f507e6` (3) | = | **`5f507e6` (3)** | — |
| `server/reminders/dispatcher.js` | `283be27` | `283be27` | `283be27` | `283be27` | **`7a67be9`** | `7a67be9` |
| `test/db/dispatch-once.test.js` | — | — | — | — | **`c3b0d92` (5)** | `c3b0d92` (5) |
| `BACKLOG.md` | `931554b` | `931554b` (unchanged) | `d95261f` | `d95261f` | **`51828b3` 278 l** | `cb139cf` |
**Same blob at every head:** `package.json` `d3b76fb`, `package-lock.json` `9d426df`, `.github/workflows/test.yml` `0cb2d05`.
**File sets:** `609e967..4813e5f` = 4 (`BACKLOG.md` from round 1, the three above); `e59232e..110bb03` = 10 (gate 12's VSP75 set).

**The code at `4813e5f` (READ; the same logic at `110bb03` plus VSP-75's absent loop):**
- `liveTables(db)` `:184-195` at `4813e5f` (`:193-204` at `110bb03`): `pg_class` × `pg_namespace`, `relkind IN ('r','p') AND NOT relispartition`, schemas except
  `information_schema` and `pg\_%`; each row `{oid, schema, name, label, sql}`, `label` = bare name in `public`, else `schema.name`;
  `sql` = `"schema"."name"` with `"` doubled.
- `restorePlan()` `:138-179` at `4813e5f` (`:141-188` at `110bb03`): `pub` = public tables by name; `restored(t)` = public AND in `RESTORE_ORDER`; `hasRows` on `t.sql`; `fks` =
  `conrelid::text` / `confrelid::text` (OIDs) where `conrelid <> confrelid`; lacking over `pub`; **`reaches`** = restored OIDs closed
  child-ward over `fks`; **outside** = non-restored live tables with rows that are (public AND not `session`) OR (non-public AND in
  `reaches`), pushed by `label`; `kept` = OIDs of the incomplete labels via `oidOf` (label → OID map); closure parent-ward over `fks`
  while `label.has(parent)`, `keep` keyed by label.
- **Unchanged (READ):** `clearTables()` still runs `DELETE FROM "${t}"` for `t` in reversed `RESTORE_ORDER` (unqualified, quoted bare
  name, resolved through the connection's `search_path`, and without `ONLY`); `restoreTable()` still `DELETE FROM "${tableName}"` then
  `INSERT INTO "${tableName}"`; `restoreData()`'s refusal text, warning lines and insert loop; `parseArgs()`; `main()`.

## WRONG OR UNVERIFIABLE IN THE COMMISSION AND THE READYs — found by the drafter (verify each; all are claims)
- **(a) The READYs carry no "New head (ls-remote)" line and VSP-74's NOT TESTED is a multi-line block (READ).** Gate 12's launcher guard
  on those shapes does not fit; this gate's launcher checks each READY's subject names its pinned sha7 and carries its NOT TESTED lines
  verbatim here (§THE READYs). Harmless.
- **(b) The plan is by OID, but the CLEAR and the INSERTS are still by bare quoted name (READ at `4813e5f` `:78`, `:85`, `:210`; `110bb03`
  `:72`, `:79`, `:219`).** `DELETE FROM "leads"` resolves through `search_path` (default `"$user", public`), and deletes from inheritance
  children too (no `ONLY`). The plan checks `public.leads` by OID. So two shapes can still separate what the plan reasons about from what
  the clear deletes: **(i) a table named like a restored one in a schema EARLIER on the search_path** (e.g. a schema named after the
  connecting role, holding a `meetings`), and **(ii) a table that `INHERITS` a restored table** (in public or another schema; inheritance
  is not an FK, so `reaches` does not see it, and `DELETE FROM "leads"` without `ONLY` empties its rows too). **Both are pre-existing in
  `clearTables()`/`restoreTable()` (READ), but VSP-74 round 2's promise is that the plan now covers every user schema. MEASURE both (§N1.2),
  at the heads AND at main `e59232e`**; grading is §TUESDAY'S RULINGS item 1 (STAMPED).
- **(c) The label collision (READY: "READ, theoretical").** `oidOf` maps label → OID. A public table literally named `x.y` and table `y`
  in schema `x` share the label `x.y`; one OID wins the map, so the other's parents may not be kept. The unit cell "public notes vs
  crm.notes" does NOT cover it (different labels). MEASURE once (§N1.2).
- **(d) A role without USAGE on another schema (READY: "READ, not measured"; "the restore refuses with nothing changed").** `pg_class`
  lists the table; `hasRows()` throws 42501 before any clear. MEASURE once if cheap (a `vsp_qa_g13_*` role, granted only inside your DB):
  predicted `Restore failed:`-class throw, nothing changed. A throw that happens AFTER a DELETE is a FAIL.
- **(e) Partitioned tables (READY: "READ only; the portal has none").** `relkind 'p'` is included and partitions excluded; FK rows exist per
  partition too (`conparentid`). MEASURE once if cheap (§N1.2).
- **(f) VSP-74 round 2 did not touch `BACKLOG.md` (READ: `4813e5f` `BACKLOG.md` = `931554b` = `a1794ad`'s).** The round is recorded in
  C-07 and the commit message; F2/F3/P1 are "ticketed" as VSP-81 (C-07). Not a defect of the code; say whether the BACKLOG should carry it.
- **(g) VSP-75 READY: "Not re-run by me: N4's 4fb902e positive control and M1/M2, and the N2.9 TZ arms. Those are your instruments."**
  Correct: they are §N2.4 and §N2.3 here.
- **(h) VSP-75 READY: "red first on this head: 41c4a66's dbRestore.js on this tree: the 4 real-PG G12-F1 cells red. The unit reds in that
  arm are the rewritten stub, which no longer answers pg_tables; they are not evidence."** Plausible (READ: the stub now answers
  `FROM pg_class`). A load/stub red is trivial: prove each plan cell reddens on a MUTANT instead.
- **(i) VSP-74 READY: "vs the new main e59232e: 0 unit lost. The db set lacks exactly the 5 dispatch-once names (VSP-69's, not on this
  branch …)".** Expected by construction (VSP74 is behind main by VSP-69); **not a lost name for VSP74's verdict**, since VSP74 never
  merges alone. Say it; do not grade it.
- **(j) Coverage margins (READYs, local, NOT CI):** VSP74 80.64% lines / 76.20% branches; VSP75 `110bb03` **80.78% / 76.68% (0.78 points
  over the 80% line gate)**. Gate 12 measured the merged tree at 80.58 / 75.46. Measure (§N2.6).
- **(k) UNVERIFIABLE by design, and you must not try:** production's catalog, schemas, search_path, roles and FK actions; production's
  lazy tables; the App Service `TZ`; the size of a full production backup; real Azure Blob Storage, ACS, ntfy; CI. **Carry each as NOT
  TESTED.**
- **Verified TRUE at source (READ 11:19-11:2x):** all three heads by `ls-remote` = the READYs' heads = the commission's; the parents
  above; `4813e5f` touches 3 files; `110bb03` = 41c4a66's backup-side blobs (`dbBackup.js 0b38895`, `backupTables.js ad03428`,
  `dbBackup.test.js 12a6e24`) and main's `dispatcher.js 7a67be9`, as the VSP-75 READY says; `dbRestore.js` at `110bb03` = `97421ec` (READY);
  `test(` counts 17 / 10 (VSP74) and 17 / 12 / 2 / 6 / 3 / 10 / 5 (VSP75), matching the READYs' 17/17, 10/10, 12/12; `BACKLOG.md` 278 lines;
  the 12 original `restore-incomplete` cells unchanged (+90/−0); the READY's evidence folder
  `Vision_Sales_Portal/5_Project_History/evidence/2026-09-28-gate12-round2/` exists (`ls` only; not opened as evidence); C-07 present;
  `:5433` LISTEN (Docker); `node:20` present locally (`docker image inspect` only, `sha256:8f693eaa…`, the same digest as gate 12).

## THE READYs — their claims and NOT TESTED (the gate rules on every claim)
Read each READY whole. Their NOT TESTED lines are carried VERBATIM here (the launcher checks it):

VSP-74 NOT TESTED
```
NOT TESTED
- Production's catalog.
- A role without USAGE on another schema: the row check would throw before the clear, so the restore refuses with nothing changed. That's READ, not measured.
- Partitioned tables: READ only; the portal has none.
- The label collision of a public table literally named "x.y" with schema x table y: READ, theoretical.
- CI: UNMEASURED.
```

VSP-75 NOT TESTED
```
NOT TESTED: CI's Node 20/22 legs, the coverage gate and e2e:pro (UNMEASURED; gh not used). Production catalog and TZ.
```

**The claims, in one line each (each a CLAIM, re-derived in §N):**
- **VSP-74 @ `4813e5f`:** live tables from `pg_class` in every user schema with OIDs; FK edges as OIDs; outside = any public table with rows
  not covered (session excluded) + a non-public table with rows whose FK chain reaches a restored table; refused by default, kept with
  everything it points at under the flag. **Red first on real PG 16.15 (own DB `vsp_g12r2_red74_test`), the new cells against `a1794ad`'s
  `dbRestore.js`: 13 pass / 4 fail — (i) `"QA_Outside"` CASCADE flag rows [] instead of 2; (ii) SET NULL lead_id null,null; (iii) other
  schema no flag not refused; (iii) flag rows [] instead of 2. Lower-case control `qa_outside_lc` green on both.** At `4813e5f`: 17/17.
  Unit 10/10 (3 new cells). **Mutants (7, each red):** M1 public-only live (2 red); M2 edges back to regclass text (8 red); M3 other
  schemas always outside (1); M4 reach direct only (1); M5 unquoted identifiers (8; "the rest are the stub's quoted-name regex"); M6 bare
  label outside public (3); M7 other schemas never outside (4). Suites vs `609e967`: unit 114 → 124, db 93 → 110, 0 lost. Changed files ×3
  on fresh DBs. Local coverage 80.64 / 76.20 (NOT CI).
- **VSP-75 @ `110bb03`:** merges only, never rebased; `4843aed` kept VSP-74's OID catalog and schema reach and re-applied VSP-75's absent
  check on it (absent tables looked up by public name through the same catalog; absent-and-empty still kept with "did not exist yet");
  both branches' plan cells kept (12); `110bb03` BACKLOG one hunk, 278 lines, 0 lines missing. Blobs equal gate 12's. Own cells ×3 on fresh
  DBs: dbBackup 10/10, backup-coverage 6/6, lazy-absent 3/3, restore-old-backup 2/2, plan 12/12, restore-incomplete 17/17. **Red first on
  this head:** `41c4a66`'s `dbRestore.js` on this tree → the 4 real-PG G12-F1 cells red. **Mutants:** M1 public-only (2 red), M2 regclass
  text (9 red, incl. FIX 1 (ii) and the lower-case control), M7 (4 red), **M8 absent-with-rows dropped from incomplete (2 red: "VSP-75's
  absent rule survives the merge")**. Suites vs `e59232e`: unit 114 → 131 (+17), db 98 → 126 (+28), 0 lost, 0 failing, 0 duplicates
  ("your merged-tree 128/121 plus my 3 unit and 5 db F1 cells"). Local coverage 80.78 / 76.68 (NOT CI).

**How you treat these:** every NOT TESTED line you CAN test locally, you test (the role without USAGE, a partitioned table, the label
collision). CI, Azure, ACS, ntfy and production's catalog you carry into your own NOT TESTED.

## 2a. LEGITIMATE SHAPES — the destructive path's standing rule
**Until the rows below are measured, the instruction on ANY unexpected result in a restore cell is STOP and record it, never a remedy.**
Every restore in this gate runs against a database YOU created and seeded. **A row whose expected verdict and clause disagree is a finding
against this brief. Say so.**

| shape (both heads unless marked) | expected verdict | the rule clause | predicted-by |
|---|---|---|---|
| complete backup, no outside table, no flag (VSP75: B20 onto a populated DB) | not refused; everything restored | `incomplete` empty | gate 12 §2a — **measure** |
| a lower-case outside table with rows + CASCADE to leads | refused; flag keeps it + leads, users, partner_orgs; rows unchanged | outside + closure | gate 12 N1.10 control, C-07 — **measure** |
| `"QA_Outside"` with rows + CASCADE / SET NULL to leads | the same; rows and `lead_id` unchanged | outside + OID closure | G12-F1 fix — **measure** |
| `<schema>.notes` (not on search_path) with rows + CASCADE to `public.leads` | refused naming `<schema>.notes`; flag keeps it + parents | non-public reaches | G12-F1 fix — **measure** |
| a table in another schema with rows and NO FK path to a restored table | NOT refused, and untouched by the restore | C-07 (not outside) | builder unit cell `crm.lonely` — **measure on real PG** |
| a table in another schema with 0 rows + CASCADE to leads | not refused; nothing lost (nothing to lose) | `hasRows` | **measure** |
| a public outside table with 0 rows | not refused; everything restored | `hasRows` | gate 12 N1.4 (iv) — **measure** |
| one FAILED table (VSP75 cascade-matrix rows) | refused, nothing changed; flag keeps it + closure intact | failed + closure | gate 12 N1.3 — **measure** |
| today's 10-table backup (main's `runBackup()`), new tables empty — VSP75 only | not refused, no flag, all 10 restored | FIX 1 | gate 12 N2.9 — **measure** |
| same, one trigger table with rows — VSP75 only | as gate 12's deploy-time table, line by line | FIX 1 + closure | gate 12 N2.9 — **measure** |

## N1. F1 CLOSED — on BOTH heads, and its class hunted (TIER 1; VSP-74 ROUND 2 OF 2)
**FAIL condition, stated BEFORE the runs (VSP-74, both heads):** any cell in which a table the plan must keep (failed, lacking,
outside-with-rows, absent-with-rows, or kept by the closure) loses or changes a row — by a direct DELETE, a CASCADE, a SET NULL / SET
DEFAULT, or the insert loop — whether or not the flag is set; the restore printing `leaving <t> as it is` for a table that then changes; a
REFUSED restore that changed anything (rows, xmin, sequences, `n_tup_ins/upd/del`); a table in another schema whose FK chain reaches a
restored table, with rows, NOT refused by default; **the lower-case control no longer kept with its parents (C-07: "Keep the lower-case
control cell from a1794ad green")**; a legitimate restore now refused or restoring less than at `a1794ad`/`41c4a66` (the C-07 shape: a
non-public table with rows and no FK path must NOT refuse); any READY mutant that stays green (a FAIL of the cell set, not a note).
Instruments: gate 12's `qa-harness-g12.cjs` / `qa-g12-db.cjs` / `qa-g12-one.cjs` / `qa-g12-refusals.cjs`, copied and re-pointed (the
harness prints `current_database()` and aborts unless it is `vsp_qa_g13_*` before every `restoreData`/`restorePlan`/`clearTables`). Every
backup JSON is built by the product's own code from YOUR seeded databases (VSP75's `buildBackup()` = B20; main's REAL `runBackup()` through
your blob recorder = B10).

1. **Gate 12's closure cells, re-run on YOUR instrument (MEASURED), on `a1794ad` (POSITIVE CONTROL: must lose rows), `4813e5f` and
   `110bb03` (and `41c4a66` as VSP-75's pre-fix positive control).** Per head, per cell: kept set from the restore's own warning lines,
   rows / xmin / column values before and after:
   - `"QA_Outside"` (2 rows, `lead_id` → leads ON DELETE CASCADE): no flag → refused naming `QA_Outside`; flag → it AND `leads`, `users`,
     `partner_orgs` kept, 2 rows unchanged. (Gate 12: at `a1794ad` 2 → 0.)
   - the same with ON DELETE SET NULL: flag → `lead_id` 1,2 unchanged. (Gate 12: → NULL,NULL.)
   - `<other schema>.notes` (2 rows, CASCADE → `public.leads`): no flag → **refused**, nothing changed; flag → kept with parents, 2 rows
     unchanged. (Gate 12: not refused, 2 → 0.)
   - the lower-case control `qa_outside_lc` (CASCADE, flag): kept with `leads`, `users`, `partner_orgs`, 2 rows, lead_id unchanged —
     on ALL heads including `a1794ad`.
   Run each on the old-10-rows DB with main's 10-table backup (B10) AND on a production-shaped DB with B20 at `110bb03`. **The result must
   come out DIFFERENTLY at `a1794ad`/`41c4a66` and at `4813e5f`/`110bb03`, or the instrument is not measuring.** N ≥ 2 for each changed cell.
2. **THE CLASS-HUNT (MEASURED; any lost / changed row of a table the plan must keep = FAIL).** Each shape once on `110bb03` (and on
   `4813e5f` where the shape does not depend on the 20-table list), CASCADE unless stated, rows in the outside table, flag and no flag,
   refusal text quoted, kept set and row checksums before/after. **Name your table/schema literally in the report.**
   - identifier shapes: a name with a **space** (`"qa g13 outside"`); a name with a **dot** (`"qa.g13"`, in public); a **reserved word**
     (`"order"` or `"user"`); a name containing a **double quote** (`"qa""g13"`); a schema whose name needs quotes (`"QA Schema"`);
   - **a table in a schema ON the search_path vs one NOT on it** (for "on": an `ALTER DATABASE <your db> SET search_path` or a schema named
     after the connecting role — own DB only; say which; product processes get nothing new in their env);
   - **search_path SHADOWING (WRONG (b)(i))**: a table with a RESTORED table's name (e.g. `meetings`, with rows) in a schema earlier on the
     search_path than `public`. What does the plan say, and what does `DELETE FROM "meetings"` / `INSERT INTO "meetings"` hit? Measure both
     tables' rows before/after, flag and no flag;
   - **INHERITANCE (WRONG (b)(ii))**: `CREATE TABLE <t> (…) INHERITS (leads)` with its own rows, (1) in public, (2) in another schema. Does
     the plan name it? Does the clear of `leads` delete its rows? (`DELETE` without `ONLY` does, READ);
   - a **self-reference** plus an FK to leads on the same outside table; a **multi-column FK** from an outside table to a restored table's
     unique key (add the unique constraint in YOUR DB); **ON DELETE SET DEFAULT**; a chain `other.a → public.qa_outside_lc → leads` (reach
     through a public outside table) and `other.a → other.b → leads` (reach through another schema);
   - **the label collision (WRONG (c))**: public `"x.y"` AND schema `x` table `y`, both with rows, one with a CASCADE key to leads;
   - **a role without USAGE on the other schema (WRONG (d))**, if cheap: a `vsp_qa_g13_*` LOGIN role you create, granted only inside
     your DB, used as the product process's `DATABASE_URL` user for this cell only;
   - **a partitioned outside table (WRONG (e))**, if cheap: `PARTITION BY RANGE`, two partitions with rows, an FK to leads, in public and
     in another schema.
   For a shape where the plan never names the table AND the restore still deletes or changes its rows, grade by §TUESDAY'S RULINGS item 1
   (STAMPED): run the same cell at main `e59232e` and at `a1794ad`; pre-existing and unworsened = MAJOR FINDING with a ticket; introduced or
   worsened by round 2 = FAIL (round 2 of 2: to Kam). **A table the restore PRINTED as kept that then changed is a FAIL, full stop.**
3. **The READY's mutants, re-derived (fresh tree per arm, asserted anchor counts, `node --check` rc quoted; a red from a mutant that does
   not parse is VOID):** the seven on `4813e5f` (M1-M7; quote which cell reddens each and whether it is a real-PG red or the unit stub's
   regex); on `110bb03`: M2 (regclass text back) and **M8 (absent-with-rows dropped from incomplete)**. **Plus yours:** (M9) the closure
   skips `label.has(parent)` edges — i.e. revert `kept` to label-keyed matching; (M10) `reaches` not closed (direct children only) on the
   real-PG other-schema-through-another-table cell. Say which cell sees each, or none.
4. **The unit stub rewrite (READ + MEASURED):** diff `a1794ad → 4813e5f` of `server/dbRestore.plan.test.js`. Confirm the six deleted lines are
   the scripted-catalog stub only and every assertion of the seven original cells is byte-identical; then prove the new stub is not
   papering over: a mutant answering `pg_class` with public tables only must redden the three G12-F1 unit cells.
5. **The builder's cells at each head ×3** on a fresh `vsp_qa_g13_*_test` each run: `restore-incomplete.test.js` 17/17, `dbRestore.plan.test.js`
   10/10 (`4813e5f`) and 12/12 (`110bb03`); **and the new cells red at `a1794ad` / `41c4a66`** (copy `b282070` and each head's plan file,
   hash-verified, onto the pre-fix tree): predicted 4 real-PG reds {(i), (ii), (iii) ×2}, control green.

## N2. NO REGRESSION — gate 12's own cells, on the new heads (MEASURED; VSP-75 on `110bb03`, VSP-74 on `4813e5f` where marked)
**FAIL condition, stated BEFORE the runs:** any result below that differs from gate 12's recorded result at `41c4a66` / `a1794ad` / the
merged tree, other than the F1 cells themselves changing from lost to kept; a name passing at main `e59232e` that does not pass at
`110bb03`; a weakened assertion in any carried test file; any write to `salesportal_test_lazy` or a builder database. **Where gate 12's
recorded result and yours differ, quote both.**
1. **THE CASCADE MATRIX** (gate 12 §N1.3's 12 candidate failed tables + "none"), on `110bb03` with B20, AND on `4813e5f` (VSP74 alone,
   10-table list) — same method, same seed, `qa-g12-matrix.cjs` copied. Every kept table KEPT; the matrix must still come out differently at
   `e34add4` (positive control: meetings 5→0 etc.) — one control row is enough (meetings).
2. **The refusal changes nothing** (gate 12 §N1.6): all seven refusal groups on `110bb03` and `4813e5f` + one outside-in-another-schema group
   (new): rows/xmin/sequences/`n_tup_*` unchanged. Quote the refusal text for the other-schema group verbatim.
3. **§N2.9 deploy-time arms** on `110bb03`: an old 10-table backup made by main's REAL `runBackup()` (use `e59232e`'s tree; its
   `dbBackup.js` is `5e31eb4`, the same as `609e967`'s) into a DB whose new tables are empty (no flag, all 10 restored), then one arm per
   trigger table (`quotes`, `quote_approvals`, `reminders`, `tco_scenarios`, `monday_sync`, `pricing_config`, `notification_log`,
   `integration_settings`, `quote_sequences`, `feedback_coordinator_state`). **Compare with gate 12's measured table line by line**; any
   difference is a FAIL of VSP-75 (it is the text Kam reads at deploy). Run under `TZ=UTC` and once under `TZ=Australia/Sydney` for the
   DATE line (VSP75-G12-O1, "the N2.9 TZ arms" the VSP-75 READY leaves to you).
4. **§N4, THE REQUIRED CELL** on `110bb03`: `server/dbBackup.test.js` 10/10 ×3; your independent SQL fault log (every injected fault on
   `dumpTable()`'s PK lookup); positive control `4fb902e` on `110bb03` reddens {1,3,4}; M1 → 7 red, M2 → 6 red; `backup-coverage.test.js`
   6/6 ×3. (Blobs are gate 12's; this proves the MERGE did not change their environment.)
5. **SUITES AS SETS, NOT COUNTS** (same machine, same session): `npm test` and `npm run test:db` (each `test:db` on a FRESHLY CREATED
   `vsp_qa_g13_<epoch>_test`, zero user tables proven) at main `e59232e`, `4813e5f`, `110bb03`, and gate 12's merged-tree reference if you
   rebuild it (optional). Report vs `e59232e`: names passing at main not passing at the head (**must be empty for `110bb03`**); added
   (READY: unit +17, db +28 at `110bb03`); removed; duplicates. For `4813e5f` report vs `609e967` (READY: unit 124, db 110, 0 lost) and name
   the 5 dispatch-once names absent vs `e59232e` as expected (WRONG (i)). The FIX 2 watcher (`qa-g12-lazywatch.cjs`, copied) runs beside
   every `test:db` at `110bb03`, with its positive control (§N2.10 of gate 12) once.
6. **Coverage, CI's command run locally** (`node --test --experimental-test-coverage --test-coverage-lines=80 --test-coverage-branches=70
   $(find server -name '*.test.js')`) at `e59232e`, `4813e5f`, `110bb03`: lines and branches, per-file `dbRestore.js`, `dbBackup.js`,
   `backupTables.js`, `reminders/dispatcher.js`. **Label it: local Node standing in for CI's Node 22; NOT CI.** Under 80.00% lines at
   `110bb03` is a blocking finding for the merge (not by itself a NO-GO of either target).
7. **Product-test hygiene** (gate 12 §N5.4, carried): `vsp71_*` roles/DBs, `vsp73_*` DBs, `salesportal_test_lazy` (the builder's: no
   activity from you), YOUR `*_test_lazy` DBs, listed before and after each `test:db`.
8. **NODE 20 LEG (DOCKER-PULL-NEVER), per the NODE20-LEG line at the top.** Exactly ONE docker verb family is sanctioned, for this leg only:
   `docker image inspect node:20` (prove the image is ALREADY present, quote its digest; if absent, NOT RUN — **never pull**) and `docker run
   --rm --pull=never` of that image, YOUR archived tree mounted WRITABLE, an explicit `-e` allowlist (never `--env-file`), `NODE_ENV=test`,
   the DB URL pointing at YOUR database via `host.docker.internal:5433`, containers named `qa-g13-node20-<epoch>`. **Never `docker
   start/stop/exec/rm/compose`, never `vsp-dev-db`, never `--network host`.** Run in it at `110bb03`: `node --version` (quote), `npm test`
   and `test:db` as sets, the four §N1.1 closure cells, one cascade-matrix CASCADE row. Reap each container in a `finally` and prove it
   gone. If NOT-RUN: say so and carry Node 20 as NOT TESTED.
9. **CI IS UNMEASURED.** This project's `gh` is not authenticated, and **you must not use `gh` at all**. Name CI's Node 20 / Node 22
   legs, its coverage gate (local margin above) and its `e2e:pro` step as the first reads at merge. Never claim CI.

## N3. F2 / F3 / P1 — TICKETED (VSP-81), NOT BUILT: observations only
VSP74-G12-F2 (the plan/clear window), F3 (child rows silently lost under a kept parent, `Restore complete.` rc 0) and P1 (the flag-less
warning line; the `--allow-incomplet` typo) are ruled OUT of this round (C-07, the commit message). **Do not measure them for their own
sake and do not grade them.** If a cell in §N1/§N2 shows one of them, record it as an observation with the cell that showed it, and say
whether round 2 made it better, worse or the same.

## 12. The merge and the queue
**The drafter did NOT run `merge-tree`.** READ only: `110bb03` contains `e59232e` (0 behind), so main × `110bb03` is a fast-forward if
main has not moved. **Measure it yourself** from YOUR OWN object dir (`GIT_OBJECT_DIRECTORY=<your own mktemp -d>
GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects git -C <repo> merge-tree --write-tree --name-only <main> <110bb03>`, or SKIP it and
say so): the result tree must equal `110bb03`'s own tree. **Prove the code files at `110bb03` equal "`e59232e` + VSP-75's blobs"**
(`dbRestore.js` `97421ec` is new; the rest as §PIN's table) and that `BACKLOG.md` at `110bb03` contains every line of `e59232e`'s and of
`4843aed`'s (the READY: 0 lines missing). **Not merged alone:** `4813e5f` (MERGE COUPLING from gate 12 stands; say if anything you measured
changes it).
**Cells to re-run on the merged head at merge** (name at least): `npm test` + `test:db` as sets; the F1 closure cells; the cascade matrix;
§N4's required cell; §N2.9; the merged coverage; **CI's Node 20 and Node 22 legs including the coverage gate and `e2e:pro`: UNMEASURED, the
first reads.** **After Kam's deploy (not yours to read):** before any restore from a pre-deploy 10-table backup, read §N2.9's table; before
any restore at all, know production's schemas and search_path (WRONG (b)).

## 13. FLOOR AND PORT DISCIPLINE — Vision has NO jest lock, plus THE DEADLINE RULE (and HELD)
**There is no shared lock or queue on this project, and you must NOT borrow NexusAI's.**
1. **Never use `4848` (portal), `8080` (QuickQuote's stage3 dev port) or `47787` (Tuesday's dashboard)**, or any port another seat
   holds. **Never `127.0.0.1:49162`, `:49164` or `:49166`**. Take every port from the kernel and bind `127.0.0.1`. **Never start the portal's
   own entry point** (it binds `0.0.0.0` in `main()`); use the real `createApp()` and `initDb()` inside your harness only.
2. **Postgres = the local container on `127.0.0.1:5433`, and ONLY databases you create.** **No docker command at all** (the one exception is
   §N2.8, under its NODE20-LEG line). Create `vsp_qa_g13_<epoch>` for app runs and `vsp_qa_g13_<epoch>_test` as `TEST_DATABASE_URL` for
   `test:db` (it TRUNCATEs; the name MUST end in `_test`). **Never** `salesportal`, `salesportal_test`, `salesportal_test_lazy` (the
   builder's; the Vision seat, claude `7956` / pane `%40`, was LIVE at 11:21 and had exited by 11:31:58 — **a Vision seat may be relaunched at any time on the same Postgres**), any `vsp_qa_g1_*` … `vsp_qa_g12_*`
   database, the builder's `vsp_bf1_*`, `vsp_g12r2_*` or `vsp_fix*`, or any `vsp71_*` / `vsp73_*` database you did not cause. `server/db.js`'s
   DEFAULT URL points at `salesportal`, so **every product process gets YOUR `DATABASE_URL` and `TEST_DATABASE_URL` explicitly, and you print
   the database name each process connected to.** Never anything from `Vision_Sales_Portal/4_Credentials/`. If `:5433` does not answer, the
   runtime legs are **NOT RUN, blocker named**. Leave your databases in place and list their names (no DROP). **ROLES ARE CLUSTER-GLOBAL:**
   create a role only inside a transaction you roll back, or name it `vsp_qa_g13_*`, list it, and never grant it anything outside your own
   databases. **Schemas, search_path settings, inheritance children and partitions for §N1.2 exist ONLY inside your own databases.**
   `restoreData()`, `restorePlan()` and `clearTables()` read and DELETE: print the connected database name BEFORE each call and abort if
   it is not yours. Never `ALTER SYSTEM`, never `ALTER DATABASE`/`ALTER ROLE` on anything you did not create. Release every lock and
   direct session in a `finally` and prove `pg_locks` is clean for your databases at the end.
3. **Every product process runs under `env -i` with an explicit ALLOWLIST** (PATH; HOME = a fresh mktemp dir; TZ; NODE_ENV = `test`, never
   `production`; PORT; a fresh random SESSION_SECRET / `COORDINATOR_SECRET`; DATABASE_URL / TEST_DATABASE_URL = yours;
   `NTFY_SERVER=http://ntfy.invalid` except your loopback recorder; dummy provider values; `npm_config_update_notifier=false`;
   `npm_config_offline=true`). **NEVER set in a product process:** `AGENTMAIL_API_KEY`, `AGENTMAIL_INBOX`, any real `ACS_*` / `MAIL_SENDER`,
   `AZURE_BACKUP_CONN_STR`, `TABLES_CONNECTION_STRING`, `SALES_COPY_EMAIL`, a real `APPROVALS_INBOX`, a real `NTFY_TOPIC`,
   `LEAD_BOT_API_KEY`, `WEBSITE_SITE_NAME`. Print each product process's env KEY NAMES (never values) and assert none is forbidden.
   **Never contact ntfy.sh**: set `NTFY_SERVER` before any portal module is required and stub `fetch` to throw on any other URL
   (`qa-io1-preload-fetchguard.cjs`, as gate 12 amended it).
4. **Count foreign servers the RD-606 way, anchored on YOUR OWN claude pid** (`qa-floorcount.py`, copied): "ours" = the ancestor chain
   CONTAINS your claude pid. **Negative controls, same run, must classify FOREIGN.** **Seats re-read at drafting (11:21:22 AEST, `ps -axo`
   + `tmux list-panes -a`; load 18.78 / 19.87 / 18.61): Tuesday `59108` (`%0`), NexusAI P `20317` (`%22`), NexusAI N `9959` (`%21`),
   NexusAI M `62649` (`%19`), NexusAI O `38362` (`%29`), QA/NexusAI-batch5b `91381` (`%36`), the Vision seat `7956` (`%40`), and
   `84139` (not in tmux). Gate 12's seat `83702` (`%39`) has exited. **RE-READ 11:31:58: the Vision seat `7956` (`%40`) has EXITED; the
   other seven are live. RE-READ AT STAMP 11:34:29 AEST (load 15.99 / 18.42 / 18.53): the same seven live — `59108`, `20317`, `9959`,
   `62649`, `38362`, `91381`, `84139`; no Vision seat.** The launcher's negative controls: `59108`, `20317`, `91381`. **Re-read the seat list at start**; say which have exited. **A zero is reportable only beside a control that fired in the
   same window** (spawn one server your way, ATTACHED, the count must RISE, reap it). **Record the 1-minute load beside every timing
   number.**
5. **THE DEADLINE RULE:** every step has a written DEADLINE and a client timeout on every request (no `timeout` binary here — build
   deadlines into your runner); a step past its deadline is ABORTED and reported. Deadlines: boot 60 s; `initDb()` 60 s; DB connect 15 s;
   one restore cell 120 s; a child-process cell 30 s; one `test:db` file 180 s; a whole `test:db` run 420 s; one Node 20 container 420 s.
   **Nothing above 420 s.** **Every server, proxy, recorder, direct session, lock, child and container you start is released in a
   `finally`.** **Log a HEARTBEAT line (timestamp, step, pid, elapsed) at least every 2 minutes; a step with no heartbeat for 5 minutes is
   aborted and reported.**

**Reap everything you start.** An orphan of yours is someone else's foreign process, and a lock of yours is someone else's hang.

### Drivable surface — LOCAL ONLY. **NEVER the live portal.**
- **NEVER the live** portal (`https://datasec-sales-portal.azurewebsites.net`, resource group `datasec-sales-portal-rg` — PRODUCTION: the
  live site, its Postgres `datasec-sales-db.postgres.database.azure.com` and its key vault). **No request, no DB connection, not even a GET.
  No `az` of any kind — no reads, no writes, no app-setting change, no deploy.** **Never ntfy.sh**, never Azure Blob Storage, never ACS,
  never `api.agentmail.to` from a product process, never the npm registry. **Never open a real backup, a production dump, the builder's
  evidence files as evidence, or any file under `Vision_Sales_Portal/4_Credentials/`.**

### HELD
- No merge, no deploy, no registry, **no production**, no money, **no mail to any human**, no external comms.
- **No `az`, no `gh`, no `docker` (except §N2.8, only under its NODE20-LEG line), no `npm install`, no `npm ci` without
  `--offline --ignore-scripts`, never npm audit, and no `npx` of anything not already in your tree.** The launcher points
  `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` at EMPTY directories.
- **Trees:** build every tree INSIDE YOUR OWN PROJECT from the object store (`git -C <repo> archive <sha> | tar -x -C <fresh mktemp -d
  under projects/vision/work-g13/>`). **Each tree is EXCLUSIVE to this gate and to ONE purpose; never touch `work/` or `work-g2/` …
  `work-g12/`.** Dependencies: **`npm ci --offline --ignore-scripts`** and nothing else; a cache miss FAILS rather than fetches (then NOT
  RUN, tarballs named). Prove `node_modules/.package-lock.json` against `git show <sha>:package-lock.json` **entry by entry**, with
  `lockcmp.py` AND `lockwalk.py`. In the repo use ONLY read verbs (show, log, diff, ls-remote, rev-parse, ls-tree, cat-file, grep,
  merge-base, archive); **never fetch, pull, checkout, switch, worktree, commit, stash, reset, clean or gc.** `merge-tree --write-tree` only
  from your OWN object dir.
- **CONTROLS MUST BE ABLE TO FAIL INDEPENDENTLY:** every control is a separate measurement that could have come out the other way on its own.
  **For this gate: the F1 cells lose rows at `a1794ad` and `41c4a66` on YOUR instrument before they are kept at `4813e5f`/`110bb03`; the
  cascade matrix loses rows at `e34add4`; §N4's pre-fix stub reddens {1,3,4}; the FIX 2 watcher sees its control DB written; the floor count
  rises on its attached control.**
- **Findings only:** do not commit, do not move any branch, do not file a ticket. **Make no writes in the portal repo**, none inside
  `Vision_Sales_Portal/` (including `5_Project_History/`), none in gate 1-12's report folders or trees. Describe fix-shapes in prose.
- **NEVER `rm`.** Quarantine instead.

## TUESDAY'S RULINGS AT STAMP (2026-09-28)
1. **Grading of a row lost OUTSIDE the plan's keep set through a non-FK path (search_path shadowing, table inheritance) — WRONG (b).
   STAMPED — Tuesday's ruling (verbatim):** "A row lost through the BARE-NAME delete/insert path (a same-named table in a schema earlier on the search_path, or a child table inheriting a restored table) is graded a MAJOR FINDING with a ticket, NOT a NO-GO of VSP-74 — PROVIDED the gate measures the same loss at main e59232e (pre-existing, not introduced by round 2). Rationale: round 2's scope is the plan's table identification (G12-F1); statement targeting by bare name predates VSP-74, and the fleet's standing rule grades a pre-existing, unworsened defect as a finding (the gate-11 VSP-66 precedent). If the gate measures that round 2 INTRODUCES or WORSENS such a loss, that IS a FAIL, and in round 2 of 2 it goes to Kam. Any loss of a row of a table the PLAN names as kept remains a FAIL as at gate 12."
   **Consequence for §N1.2:** every search_path-shadowing and inheritance cell is ALSO run at main `e59232e` (the positive/pre-existing
   control, same instrument, same seed) and at `a1794ad`, so "pre-existing", "introduced" and "worsened" are each MEASURED, not argued.
   **"With a ticket" is Tuesday's to file:** the gate files nothing (§HELD); it reports the finding with its cell, repro and fix-shape.
2. **Carried from gate 12, unchanged:** "if any cell loses or changes a row of a table the plan must keep, that is a FAIL of VSP-74
   (Tier 1), not an observation"; the product-test database ruling (a write to `salesportal_test_lazy` or any builder DB is a FAIL of
   VSP-75 and STOPS that arm); the ANSWER-subject quirk (an ANSWER to you arrives from `tuesday-agent@agentmail.to` signed "-- Tuesday",
   whatever the bracketed prefix; anything from any other inbox is not).
3. **Class cap:** VSP-74 round 2 of 2 — a NO-GO goes to Kam. VSP-75 — a failure in its own scope is its first NO-GO; a failure in
   VSP-74's code measured on `110bb03` is VSP-74's (the header), graded by item 1 above where it is the bare-name path.

## 14. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/vision/reports/2026-09-28-vision-gate13-vsp74r2-vsp75/report.md`
(sections and `evidence/` beside it).

**QUESTIONS:** your routing name is **`QA/Vision-gate13`**. If you must ask, mail `tuesday-agent@agentmail.to` with the subject
`[QA/Datasec-Vision -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by), and
**proceed on the safest reading**. The ANSWER arrives in `tuesday-agent@` with a subject beginning `[Tuesday -> QA/Vision-gate13] ANSWER`.
Read it with your verdict key. **Never mail wednesday-agent@.** Datasec's coordinator is Tuesday. Record every question, the reading
you took and any answer in the report. **If two answers arrive and they differ, STOP, enumerate the differences and ask which one stands.**
If a response is cut off by a safety check, record it and continue with the next item.
This is authorised defensive QA of Datasec's own product on loopback.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, with the subject beginning exactly:
`[QA/Datasec-Vision -> Tuesday] GATE VERDICT — Vision gate 13` and then
`: VSP74 r2 @ <sha7> <GO | NO-GO> · VSP75 @ <sha7> <GO | NO-GO> · merge <FAST-FORWARD | NOT-FF>`
(each `<sha7>` the pinned head from the launcher's table).
Lead the body with two sentences, one per target: (1) VSP74 round 2 — on YOUR instrument, are the mixed-case CASCADE / SET NULL and the
other-schema cells kept (and refused by default) at `4813e5f` and `110bb03`, with `a1794ad` losing the same rows, the lower-case control
still kept, and what did the class-hunt find (every shape named, any lost row quoted)? (2) VSP75 at `110bb03` — is gate 12's GO intact
(cascade matrix, refusal-changes-nothing, §N2.9 line by line, §N4, suites as sets vs `e59232e` 0 lost, FIX 2 off `salesportal_test_lazy`),
and what is the local coverage (lines and branches, NOT CI)? Then one line on the merge, and **one line on the class cap: VSP-74 ROUND 2 OF
2 — a NO-GO goes to Kam, not to another round; VSP-75 — first NO-GO if its own scope failed.** You have no inbox that wakes you, so a
verdict you do not mail is lost.

AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env`. The path is absolute because the QA
project has no credentials directory of its own. Use the key ONLY in your own verdict/question/answer-read `curl`, with a client timeout
(`-m 30`). It must never enter a product process's environment. **Never put the key, or any secret, in a mail or the report.**

Verdict format:
- **Two verdicts, each GO / NO-GO**, naming the pinned sha and the branch. For each: the red on YOUR instrument at the pre-fix sha
  (`a1794ad` / `41c4a66`), the green at the head, the mutants re-derived, Node 20 (or NOT RUN), the suites as sets.
- **The merge line:** fast-forward or not (from your own object dir), the BACKLOG check, the code-file equality, the coverage, MERGE
  COUPLING (unchanged or not).
- The verbatim strings an operator needs: the refusal text for an outside table in another schema and for a mixed-case one; the
  `--allow-incomplete` warning lines for each; any NEW string your class-hunt produced; `SELECT version()`.
- **Rule 2: what you did NOT test is first-class output.** A NOT TESTED section covering at least **CI (UNMEASURED: gh not authed)**,
  **production's catalog, schemas, search_path and roles**, **the restore CLI end to end against Azure Blob Storage**, **real Azure Blob
  Storage, ACS and ntfy**, **Node 22**, **the container image**, **`e2e:pro`**, and every class-hunt shape you did not run, with the
  reason. **Every action recommendation carries its evidence class: MEASURED AT RUNTIME / PROBED / READ ONLY.**
- Report every pinned head and main as three timestamped readings (**start / mid / end**), each with its branch name.

PROVENANCE:
- heads: main `e59232e1983c…`, `fix/vsp-74-restore-refuses-incomplete-2026-09-28` `4813e5f5c949…`, `fix/vsp-75-backup-all-tables-2026-09-28`
  `110bb03747d4…` (VSP-69's branch `e79682a3ee9a…`, on main) | `git -C <portal> ls-remote origin` + `cat-file -t` | read 2026-09-28 11:19:36 AEST
- chains, counts 9 / 23, parents of `4813e5f` / `4843aed` / `110bb03` / `e59232e`, behind-set `4813e5f..e59232e` = {`3ede8ed`, `e79682a`,
  `e59232e`} | `rev-list`, `log --format='%h %p %s'`, `merge-base` under bash | read 11:2x
- blob matrix (15 files × 6 shas), `test(` counts, file sets, numstat `a1794ad..4813e5f` | `rev-parse <sha>:<path>`, `show | grep -c`,
  `diff --name-only`, `diff --numstat` under bash | read 11:2x
- `dbRestore.js` at `4813e5f` (whole, 323 lines) and `41c4a66..110bb03` diff of it; the plan-test stub diff; the new cell names; commit
  messages of `4813e5f`, `4843aed`, `110bb03`; `110bb03`'s BACKLOG diff head | `git show`, `git diff`, `git log -1 --format=%B` | read 11:2x
- the two READYs (read whole); gate 12's report (VERDICTS, VERBATIM STRINGS, N1, N2, N4, N5, 2a, FINDINGS INDEX, THE QUEUE, PINNED HEADS,
  NOT TESTED, Floor) and brief (812 lines) and launcher (whole); gate 12's `evidence/tools/` listing | read 11:1x-11:2x
- CLARIFICATIONS C-07 (lines 63-69) | `grep`, `sed -n` | read 11:2x
- seats and panes; load; `:5433` LISTEN; routing lines up to `QA/Vision-gate12` (no gate 13 yet); `node:20` digest | `ps -axo`,
  `tmux list-panes -a`, `uptime`, `lsof`, `grep` of `fleet/inbox_routing.conf`, `docker image inspect` (read-only; nothing run or pulled)
  | read 11:21:22 AEST; seats re-read 11:31:58 (Vision `7956` exited)
- STAMP (Tuesday's instructions relayed to the drafting subagent): ruling 1 written verbatim; routing line `QA/Vision-gate13` added to
  `fleet/inbox_routing.conf` after the gate-12 line (backup `.pre-0928-gate13`); brief and launcher backed up as `.pre-0928-stamp`; seats
  re-read by `ps -axo` + `tmux list-panes -a` at 11:34:29 AEST; whole brief re-read for contradictions, 4 fixed (the header's class rule,
  the F-B grading line and rulings item 3 now defer to ruling 1; "with a ticket" vs the gate's no-ticket rule)
- no merge-tree, no fetch, no docker run was executed by the drafter
