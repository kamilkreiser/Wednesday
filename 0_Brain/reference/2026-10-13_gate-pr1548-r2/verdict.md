VERDICT: GO (0 Major, 0 Minor, 4 Info). Head gated 03bdfc3205e13e4d610ebd1163ab1273ba03d151. Develop measured 0662f7213cc08d962b745fa6998fc2a3f47499a5 (live; the brief's 92d1316f also measured).
REPORT_SHA256_16: 6a41c4bef88d1e55
# Gate verdict: PR #1548 (KS-1598) fix round 1, DELTA. Opus, through-code weight. Round 2 of 2 under the cap.

Recipe for line 2: delete line 2, take the sha256 of the remaining bytes, keep the first 16 hex characters.

**Head under test:** `03bdfc3205e13e4d610ebd1163ab1273ba03d151`.
- My own `ls-remote` read the same SHA for `refs/pull/1548/head` at 22:30 AEDT, mid-run and at 22:41 AEDT (`results/lsremote_start.txt`, `lsremote_mid.txt`, `lsremote_final.txt`).
- One commit; parent `9d974c4b516cc665a6c5d3b26b06eae22c09a9b3` (the round-1 gated head); tree `0f84db84`. `rev-list --count 9d974c4b..head` = 1.
- **Develop moved during the gate.** At 22:30 it was `92d1316f` (the brief's value). By the mid-run read it was **`0662f7213cc0`** ("KS-998 item 3: the gate checks lock sources and scrubs the install env", 22:38 AEDT), and it stayed there to the final read. The merge prediction below is on the LIVE tip `0662f721`, with `92d1316f` also measured.

**Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict.**

Gate: an independent Opus seat, 2026-10-13 AEDT. Findings only; I changed nothing in the project.
- **Code:** `git clone --shared` into my scratchpad (`g1548r2/repo`), push URL `DISABLED`. The project's `core.sshCommand` was copied into the clone's config for `ls-remote`/fetch only. Write verbs (worktree, `hash-object`, `read-tree`/`update-index`/`write-tree` on a private index file, one `commit-tree` conflict control, `merge-tree`) ran in that clone only. Nothing was written in `!CODING`. No GitHub, Linear or mail reads or writes.
- **Database:** my own PostgreSQL 15.14 on 127.0.0.1:**55583**, TCP only, unix socket disabled, `en_US.UTF-8`, fresh `initdb`. `lsof` at start showed 55416, 55418, 55492, 55521 listening (other seats; never touched). Schema from the head's `docker/init/*` then `scripts/run-migrations.sh`: `applied=51 failed=0`, with `Applying 049_admin_organisation_scopes.sql` (`results/pgsetup_head.txt`). Service ran as `secuura_app`, `MULTI_TENANCY_ENABLED=false` unless stated.
- **Stopped:** `pg_ctl -m fast` → 0 listeners on 55583 (control in the same instrument: 55418 shows 2 listeners); `pgrep -f vitest` = 0.
- **Where things are:** raw outputs `evidence/results/`, cells `evidence/cells/`, tools and tsconfigs `evidence/tools/`, init/migration logs `evidence/pg/`.

## Findings

| id | severity | where (head 03bdfc32) | what | minimal fix |
|---|---|---|---|---|
| **i1** | Info (new in this delta, test-only) | `ks1570b-admin-scope-route.integration.test.ts:386` (the regex), `:387` (the assertion), and the comments at `index.ts:1653-1654` and test `:339-340` | **The vocabulary-read cell is blind to any status that is not pure `[a-z]`.** It extracts with `/'([a-z]+)'/g`. Planted in my DB and measured, running only that cell: adding `archived` → **red** (`expected [ 'active', 'archived', …(6) ] to deeply equal …`); removing `invited` → **red**; renaming the constraint → **red** (`expected undefined to be truthy`). But adding **`on_hold`**, **`tier2`** or **`re-invited`** → **GREEN**, 1 passed, rc 0 (`results/plant_vocab_run.txt`, `plant_P3/4/5_*.txt`). So a vocabulary that grows by a status with `_`, a digit or `-` is not caught, and the spectrum never exercises it. Also, the comments say the cells "read the vocabulary off the live CHECK rather than carrying a typed copy"; in fact the cells iterate a typed `VOCAB` and one cell compares it with the CHECK. Every status today is `[a-z]` (live def and auth's `DB_STATUS_TO_DOMAIN`), so nothing is missed now. | Extract with `/'([^']+)'::/g` (or `ARRAY[...]` parse). Say "the typed list is checked against the live CHECK". |
| **i2** | Info (text: PR body table, commit message, ready mail) | PR body "Mutants for Round 1" row X0 (logged copy `5_Project_History/2026-10-13_seatV-9th/evidence/pr1548_body_readback.md:220`, `:290`); commit message "X0 … recorded as LOADFAIL" | **X0 was not a LOADFAIL.** The author's own log `logs/mut_X0.log` shows `Tests 45 passed (45)`, `VITEST_RC=0`; `logs/mut_X0_control.log` prints `DETECTOR: *** DETECTOR FAILED ***`. My reproduction (a type error in the test file): vitest **SURVIVED 45/45 green**, service `tsc` unchanged, while my test-inclusive program reds with 2 `error TS` naming `ks1570b…:344`. So X0 is a survivor that only a test-inclusive type-check catches. The body's prose (item 2) says exactly that and is right; only the table cell and the one-line summaries say LOADFAIL. Not counted as a kill by anyone, so no number is inflated. | Relabel the row "SURVIVED 45 green; red only under a test-inclusive tsc (KS-1554)". |
| **i3** | Info (text nit) | `index.ts:1632-1633`, test `:256-257` | "`:34` and `:41` are the NORMALISING UPDATE's `NOT IN`": `:41` is in the `UPDATE`; `:34` is the `SELECT count(*)` that decides whether to normalise, in the same `DO` block (read at the head's `046_users_status_vocabulary.sql:31-41`). The round-1 i1 correction itself (`CHECK … IN` at `:60`, name `users_status_vocabulary`, the `:47` quote) is **right**, verified against the file and the live `pg_get_constraintdef`. | "the normalising block's `NOT IN`". Optional. |
| **i4** | Info (pre-existing; carry-forward of round-1 i6 into KS-1601) | `index.ts:1657` `upper(role) = $3` | **The full enumeration widens i6 by one codepoint.** Under the database's default collation, the non-ASCII codepoints whose `upper()` lands in ASCII are **U+0131 → `I`** and **U+017F (long s) → `S`**. Neither can spell `ADMIN` except via U+0131, so the i6 conclusion is unchanged; under `COLLATE "C"`, the same count is **0**. So the same one-token fix closes both. Not in this delta and not touched by it. | For KS-1601: `upper(role COLLATE "C")`. |

**Why no Minor:** the round-1 m1 is closed, measured exhaustively and at the route, with red-first proof (below). The one new weakness (i1) is in a test cell's drift detector, has no runtime effect, and cannot hide a status the guard would admit: any vocabulary change still has to pass the 18 dead / 4 live route cells, and the guard compares against the literal `'active'` only.

## FOUND / TESTED / HOW

**1. Scope** (`results/delta.diff`, read whole)
- `git diff --numstat 9d974c4b 03bdfc32`: **2 files**: test file +105/−3, `index.ts` +25/−5. Nothing else.
- Hunks:

| file | hunk | class |
|---|---|---|
| test | `@@ -251` (+12/−9) | **Comment only** (i1 citation). Non-comment changed lines **0**; the same filter counts **9** comment lines in that hunk (control). |
| test | `@@ -317` (+99) | **Test**: new describe, 27 cells (2 m1, 1 m1 control, 1 vocab-read, 1 23514 control, 4 live, 18 dead). |
| `index.ts` | `@@ -1627` | **Comment** (+20) and **one behaviour line**: the guard SQL `lower(status) = 'active'` → `lower(status COLLATE \"C\") = 'active'`. Exactly 1 −/1 + non-comment line in the file. |

- The head's guard string is byte-identical to my round-1 X5 replacement (count 1 in head `index.ts`; the old guard count 0).

**2. m1 closed: cell H, X5, and the enumeration**
- **Cell H** (round-1 cell, unchanged; `results/H_ledger_wt_head.json`, `H_ledger_wt_base.json`):
  - head: `ACTİVE` → **404, no row**; `actİve` → **404, no row**; control `ACTIVE` → 200 with the row; `DELETED` → 404.
  - base `9d974c4b` (control): both U+0130 spellings → **200, row written**; `ACTIVE` 200; `DELETED` 404.
- **X5:** the head IS my X5, so the head H ledger is the X5 ledger, and it matches round 1's `H_ledger_X5fix.json`. The inverse (M1R, `COLLATE` removed) is killed (item 5).
- **Enumeration, not sampling** (`results/enum_fold.txt`, SQL over **every codepoint 1..0x10FFFF except surrogates = 1,112,063**, PG 15.14, db `en_US.UTF-8`):
  - `COLLATE "C"`: non-ASCII codepoints whose `lower()` differs from the input: **0**; whose `lower()` contains any ASCII byte: **0**. **Positive control, same instrument:** ASCII codepoints changed by `lower()` under `"C"` = **26**.
  - **Control, default libc collation:** non-ASCII codepoints changed by `lower()` = **1,404**. Of those, the ones landing in ASCII are exactly **U+0130 → `i`** and **U+212A (Kelvin) → `k`**. Only U+0130 lands on a letter of any vocabulary word (fullwidth letters do not fold to ASCII at all).
  - ICU `und-x-icu`: only U+212A → `k` lands in ASCII.
  - Whole strings: all 64 ASCII case spellings of `active` are true under `"C"` (64/64). Every spelling of every vocabulary word with U+0130 substituted at any subset of `i` positions: the CHECK admits all of them (32 for `active`, 1,600 in all). The default-collation guard is true for **32**; the `"C"` guard is true for **0**.
  - **The JS side** (`results/enum_js.txt`, node v24.7.0, every codepoint): the non-ASCII codepoints whose `toLowerCase()` is pure ASCII are only **U+212A → `k`** (control: 1,434 non-ASCII changed, 26 ASCII changed). With auth's `mapDbStatus` (`own(s) ?? own(s.toLowerCase())`, `services/auth/src/repositories/userRepo.ts:330`), **auth-ACTIVE ⇔ an ASCII case spelling of `active` ⇔ the `"C"` guard is true.** Guard and auth now agree on every string.
- **At the route, the whole admitted spelling space** (my cell `gate1548r2-h2-enum`, 103 cells, real app, app role):
  - head: **64 ASCII → 200, 1 row, 1 audit; 32 U+0130 → 404, 0 rows, 0 audits**; 6 fold-class strings (fullwidth `ａ`/`Ｉ`, dotless `ı`, `i`+U+0307, Kelvin, a trailing ZWSP) → **refused 23514 by the CHECK**. 103/103, rc 0.
  - base (control): **the same 32 → 200 with a row** (32 red, each `expected { … put: 200 … } to deeply equal { … put: 404 … }`).
  - Two earlier runs are kept and marked `*_cellbug`: my first REFUSE list held an entry that evaluated to plain `active`, which correctly got 200. That was my cell's bug, fixed before the counted runs.

**3. The spectrum: vocabulary plant and reach**
- **Vocabulary cell planted** (`tools/plant_vocab.sh`; the constraint is replaced in MY DB, only that cell runs, and the restored def is asserted string-identical after each plant, every time):
  - P0 unchanged (control): green.
  - P1 `+archived`, P2 `−invited`, P6 constraint renamed: **red**, each with a real message.
  - P3 `+on_hold`, P4 `+tier2`, P5 `+re-invited`: **green**. That is finding i1.
  - P7 `active` → `enabled`: the whole file reds at `beforeAll` (23514 on the fixture insert).
- **The 23514 control planted** (`results/plant_23514.txt`): constraint dropped → **red**, `expected 'inserted' to be '23514'`; unchanged → green; restored identical.
- **Reach of all 27 cells:**
  - **ALLTRUE** (status clause removed) reds the 2 m1 cells and all 18 dead cells. **ALLFALSE** (`= 'nothing'`) reds the 4 live cells and the ASCII control. That is **25/25 route cells**, each red under one of the two with `AssertionError: expected { status: … }`, 0 empty messages.
  - The 2 non-route cells red under the DB plants above. **27/27 reach their target.** (`results/mutants_r2.json`)
- **Author's runs reproduced:** head **45/45** ×3 (MT=false) and **45/45** with MT=true; red-first, head test file on `9d974c4b` code: **2 failed / 43 passed** ×2, exactly the 2 U+0130 cells, each `expected { status: 200, … }`.

**4. Type-check of the changed test file** (`tools/tsconfig.changed.json`: extends the service tsconfig, `files` = the changed test file, so `index.ts` etc. come in by import)
- **rc 0, 0 `error TS`** (`results/tsc_changed.txt`).
- **Control:** the same program plus a planted `const x: number = 'string'` file → **rc 2, 1 `error TS2322`** naming it (`tsc_planted.txt`). The planted file was moved to `g1548r2/quarantine/`.
- **Second control in the mutant run:** X0 in the test file itself → this program rc 2, 2 errors at `ks1570b…:344` (the mutated file's line).
- **All-tests program** (`tsc_alltests.txt`): 7 errors in all.
  - 0 are in `ks1570b`.
  - **2 are the ks952 errors the author names**: TS2339 at `ks952-rate-limit-scope-route.test.ts:249` and TS1343 at `ks952-rate-limit-scope.test.ts:313`.
  - 1 is my planted file.
  - 4 are TS2741 `keepAliveTimeoutBuffer` on `http` vs `node:http` Server types in 4 untouched files. **Probably an artefact of my symlinked `node_modules`** (two `@types/node` resolutions); I did not verify that.
- **eslint `--max-warnings=0`** on both changed files: **rc 0**. **Control:** a planted `var` file → rc 1, `no-var`.

**5. Mutants** (`tools/mutants_r2.py`; `results/mutants_r2_run.txt`, `mutants_r2.json`)
- **Method:**
  - suites: author route 45, my round-1 G 22, my H2 103;
  - baseline **green** first (45/0, 22/0, 103/0), with `tsc` (changed program) rc 0;
  - each mutant alone, and each anchor had to occur exactly once;
  - both files restored from byte snapshots, with sha256 asserted after every mutant: **restored identical: True**;
  - every red cell recorded by name with its message; an all-empty-message "kill" is not counted.

| mutant | result | red (author / G / H2), empty msgs |
|---|---|---|
| **C0** comment-only, `index.ts` | **SURVIVED** | 0 / 0 / 0 |
| **C0t** comment-only, test file | **SURVIVED** | 0 / 0 / 0 |
| **M1R** (author) `COLLATE` removed | KILLED | 2 / 0 / 32, 0 empty of 34 |
| **X4** (author) `COLLATE … <> 'deleted'` | KILLED | 17 / 15 / 32, 0 of 64 (matches author's 17) |
| **X4g** (my round-1 X4 literally) `lower(status) <> 'deleted'` | KILLED | 17 / 15 / 32, 0 of 64 |
| **X5a** (author) `IN ('active','pending')` | KILLED | 3 / 3 / 0 |
| **L1** (author) `LIKE '%active%'` | KILLED | 3 / 3 / 0 (the `inactive` spellings) |
| **V1** (author) inverted want, test file | KILLED | 1 / – / – (the vocabulary cell) |
| **X0** (author) type error in test file | **SURVIVED** (not a kill; tsc-inclusive rc 2) | 0 / 0 / 0. See i2. |
| **X5** (my round-1 fix) | = the head (byte-identical) | the baseline |
| **G2** (mine) `lower(status) COLLATE "C"` (collation placed after the fold) | KILLED | 2 / 0 / 32. The realistic misplacement is caught. |
| **G3** (mine) `upper(status COLLATE "C") = 'ACTIVE'` | SURVIVED | predicted equivalent: the ASCII-only fold either way |
| **G4** (mine) `IN ('active','invited')` | KILLED | 3 / 3 / 0 |
| **ALLTRUE / ALLFALSE** (reach) | KILLED | 22/18/32 and 17/4/64, 0 empty |

**6. Merge prediction on LIVE develop `0662f721`** (`results/pr_files.txt`, `dev_files*.txt`, `mt_clean.txt`, `mt_control.txt`, `merged_vs_develop.txt`)
- **Ancestry:** merge-base(head, develop) = `026c2d16`; it is an ancestor of develop (rc 0); develop is not an ancestor of the head (rc 1), so a merge is needed. Develop is 3 commits past the base (`d53d80cb`, `92d1316f`, `0662f721`).
- **Overlap scan:**
  - PR files (base..head) 4, develop-moved files 19, **overlap 0**;
  - **planted control:** one PR path added to the develop list → overlap **1**;
  - develop touches `services/security/` or `packages/` **0** times. Positive control, same grep: `services/originate/` matches **9**.
- **`merge-tree --write-tree` head × `0662f721`: rc 0**, tree `527af94f`. In it, the two security files equal the head's, and `originate/src/index.ts` equals develop's. `diff --stat develop..merged` = exactly the PR's 4 files (+298/−7 over base).
- `merge-tree` head × `92d1316f` (the brief's value): also rc 0.
- **Negative control:** a scratch commit on `0662f721` (`f76090cb`, develop's guard line rewritten to `'live'`) → **rc 1, `CONFLICT (content) … security/src/index.ts`**. The clean reading discriminates.

**Author's other numbers, re-measured on the head:**
- security integration: **11 files / 254**, rc 0. My 4 gate files hold 132 cells (22+4+3+103), leaving **7 files / 122**, as claimed. The file list is in `sec_integ_head.txt`.
- security unit: **31 files / 343**, rc 0, at load average 4.1.
- The `i3`/`i4` PR-body corrections are present in the author's logged body readback (`pr1548_body_readback.md`, byte-equal to `_after.md`): line 132 relabels R4 as bd11c34e reverted; lines 65-68 add `tenant_isolation` and move `keys/validate` out.

## NOT tested (plainly)
- **The live GitHub PR body** (I read the author's logged readback only), **Linear** (KS-1601, KS-1602, the KS-1554 comment), and the ready mail's delivery.
- **The production collation.** The `COLLATE "C"` fold is locale-independent by construction (ASCII bytewise in PG), so the fix does not depend on it. Whether production's default would fold U+0130 is moot for the guard and relevant only to the CHECK.
- **KS-1602** (ks742 hook timeout under load): not reproduced; my unit run was green at load 4.1.
- The 4 TS2741 `keepAliveTimeoutBuffer` errors: I did not establish whether they are my `node_modules` layout or real.
- The platform suites (Schemathesis, Akto, Playwright, k6), preflight legs 3/4/8, the gateway path; the merged tree's suites (develop's move touches no security or shared file, and the merged security files are byte-equal to the head's); the shared unit suite.
- Mutants ran with `MULTI_TENANCY_ENABLED=false`. Only the author file's 45 also ran with `true`.

**Could any of this hide a Major?** The behaviour change is one token in one SQL guard. The enumeration shows it admits exactly the 64 ASCII spellings of `active` and nothing else, and auth agrees on every string. It is measured at the route in both directions, and it is red-first against the round-1 head. Caller authorisation, the lock and the audit chain are untouched by this delta. I see no untested surface that could widen a grant.

## Scratch state when stopped
- PostgreSQL stopped, 0 listeners on 55583.
- Worktrees `g1548r2/wt_head` (`git status`: no tracked file modified) and `wt_base` hold my untracked gate cells (`wt_base` also holds the head's test file copied in). Both planted files are in `g1548r2/quarantine/` (moved, not deleted).
- The scratch clone holds `refs/gate/{head,develop,develop2}` and the conflict-control commit `f76090cb`. Push URL `DISABLED`.
