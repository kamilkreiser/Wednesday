GATE B1506: GO WITH FINDINGS @ 9d97328 on main 5ad366c

Tier 1, full weight. Gate run 2026-11-11 17:20 to 17:30 AEDT. Independent clone at
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s268/gate1506/clone` (push URL `invalid://no-push-gate`).
Evidence: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s268/gate1506/runs/`.

## Findings

| # | Severity | Finding |
|---|---|---|
| F1 | Minor | 0020 section, head `DEPLOY.md:169`: the roll-forward bullet now reads `- **roll forward** are as above (...)` (lower-case start, plural verb for one subject). Graded: this IS what the kit's words rule required (P-D (i) "loses the words **Route B** and only"; W-R 5 "keeps the words it has today ... minus **Route B** and"; STANDING "no word added beyond W-77 and W-R"). The builder complied and disclosed it; the defect is the kit's drafting. The meaning is still readable. Fix needs Tuesday's words (e.g. `- **Roll forward** is as above`); suitable for a later words pass, not a reason to hold the procedure. |

No Blocker, no Major.

Observations (not findings):
- O1. The banner rows pin count 1 (singular) and count 3 (plural). No row pins count 2; a mutant `done <= 2` would pass. The code is `markResult.done === 1 ? ... : <main's template>`, so 2 is plural by reading. The kit asked for no 2-row.
- O2. When the block is pasted as written, the apply's `psql -q` prints the dump script's own `set_config` / `setval` result tables to stdout before the final `echo $?`. The block is identical to 0021's form on main, so this is not new. My first harness run mis-parsed it (a harness fault, fixed and re-run; both runs restored correctly).

## The heart: R20 re-run from the edited DEPLOY.md at the head (`runs/r20-gate.txt`)
Frame: `postgres:16@sha256:f1c3376c...` read from `scripts/common.sh` at head; `pg_restore (PostgreSQL) 16.15`; `--internal` network `g1506-net`; no port published; the CI-stage image of the head (`g1506-node:head`, built from my clone); my own helper `g-node.mjs` that imports the product's `loadMigrations()`/`migrate()` and prints the CLI's template (`packages/db/src/cli/migrate.ts:55-57`). Fixture independent of the builder's: 2 tenants, 2 releases, 4 engagements (8 approvers). The post-dump row is a fifth engagement whose version uses 0020's six columns, including the FK.
Extraction by my own program (`g-block.py`, not the builder's `runblock.py`): the one fenced block of `## Rolling back a deploy that applied 0020` holding `pg_restore --clean --if-exists -f -`, head lines 154-163. Exactly three substitutions: container x2, dump x1, script x3. Reverse-substituted executed lines == block lines: True. Run as ONE bash script, as an operator pastes it.

| Step | Gate result | STATUS claim | Match |
|---|---|---|---|
| (1) dump at 0019 | ledger 19; pg_dump exit 0; `pg_restore -l` 518 entries; 7 of 28 tables with rows | 518 entries, 7 tables | yes (bytes differ: different fixture) |
| (1) 0020 applied, one-step Route B | exit 1, `cannot drop constraint content_release_pkey on table pc.content_release because other objects depend on it`, DETAIL `policy_version_last_generate_content_release_id_fkey`; ledger still 20 | same | yes |
| plant: the block with the drop statement emptied | statuses 0 0 3; ledger 20; tables unchanged | write=0 check=0 apply=3, ledger 20 | yes |
| (3) the block as written | statuses 0 0 0 | 0/0/0 | yes |
| (4) after | ledger 19, newest `0019_guided_role.sql`; 6 columns + FK gone (0); every pc/pc_meta table count+md5 equal to dump time; post row gone | same | yes |
| (4) schema vs fresh 0019 | 12 diff lines = 3 CHECKs (`feedback_attachment_filename_check`, `feedback_item_page_path_check`, `feedback_item_title_check`), AND grouping only; equal with parentheses removed | same 12 lines / 3 CHECKs | yes |
| (5) previous build | `migrations applied: none; already applied: 19` | same | yes |
| (6) roll forward | `0020_generate_issues_kept.sql; already applied: 19`; sha256 before = after = file = `2e3008f0d52b86809102be272f0ee42df9ff61e19fb135b7e26256baf27e855d`; ledger 20 | same sha | yes |
| POSITIVE control 0018->0019 one-step | exit 0, ledger 18 | same | yes |

SUMMARY checks=22 fails=0 plants=2/2 (table-state control and necessity plant). DEPLOY.md in the run: sha256 `c76924a5...` = `git show 9d97328:DEPLOY.md`.

## P-D (iii) (`runs/pd-gate.txt`, my program `g-pd.py`)
- 0021 section main 154-286 = head 191-323, `cmp` rc 0. 0022 section main 287-336 = head 324-373, `cmp` rc 0. The same by `awk NR` on the kit's literal main line numbers: rc 0 and rc 0. CONTROL: a one-character plant in the 0022 copy makes `cmp` fail (char 2463, line 25).
- Every diff hunk is inside the 0020/0024/0025 sections, with the heading lines untouched: 6 of 6 hunks (main 144, 152, 407-411, 422, 463-465, 476 -> head 144-169, 177-189, 444-468, 479-492, 533-557, 568-581, as STATUS says). CONTROL: a planted edit in 0023 is reported outside (1). The 16 `## ` headings are identical and in the same order.

## P-T: b778 rows red/green (`runs/pt-gate.txt`, `runs/pt-mutants-gate.txt`)
The head b778 was run in a `--network none` container against DEPLOY.md variants:
- Head DEPLOY.md: 106/106 pass.
- Only the 0020 section reverted to main's text: 15 red, all 15 of them 0020's new rows. 0 red outside the new describe, 0 of another section. The same holds for 0024 (15 red) and 0025 (15 red).
- Main's whole DEPLOY.md: 45 red, all in the new describe.
- Existing rows: main's b778 on main has 61 rows; head's b778 on head keeps the same 61 names. Lost 0, changed 0, added 45. Main's b778 on head DEPLOY.md: 61/61 pass. b616: 109/109 at main and head, lost 0. Readers total 170 -> 215, as claimed. CONTROL of the comparison: one row flipped gives changed 1; one row dropped gives lost 1.
- My own mutants of the head DEPLOY.md (non-vacuity, independent of the builder's plants): 0024's drop statements swapped turns 0024's (1) and (3) red; `--single-transaction` removed in 0025 turns 0025's (1) red; one character of 0020's check line turns 0020's (2) red; the stale "**Route B** and" put back in 0020 turns 0020's (7) red. Each mutant reddens only its own section's rows.
- `git diff --numstat` for b778: 316 added, 0 deleted.

## Standard steps
1. Refs (ls-remote over SSH at 17:2x and again at 17:29): branch = `9d97328c9f61f0262fd97c99662eb8599ae30429`, main = `5ad366c0074fefa0643d7b2eb0414d14e6ebf4a7`. Merge-base = main. Four commits. Changed paths, 4 of 4 in OWNS: `DEPLOY.md` (+117 -12, all inside the three sections), `Controls.tsx` (+8 -1, the :599 banner only; :605 stopped line unchanged), `b1495-mark-all-local-dom.test.tsx` (+3 -2, the helper and the row title only), `b778` (+316 -0). Open-PR overlap: #85 0/57, #86 0/2, #91 0/2 (PR heads fetched over SSH; control: #123 holds 1). The highest PR ref is #123, so no PR is newer than the kit. Sibling Composer code lanes of the day (B1495, B1504) have both landed, so overlap is 0.
2. Merge: `git merge-tree --write-tree main head` rc 0. Its tree `8a545518...` = the head tree, so main plus the head blobs exactly. CONTROL: a loose commit editing main's DEPLOY.md:144 conflicts (rc 1).
3. CI: no `.github` path at head (0; control `scripts/` 28). Hosted is CodeQL only. At the head (= the merge tree): `npm run lint` rc 0, `npm run format:check` rc 0 (`prettier --check .` covers DEPLOY.md), `npm run typecheck` rc 0. Web DOM file 9/9. Both DEPLOY readers as above. gitleaks (the project's pinned image and its `scripts/gitleaks.toml`, dir mode over `git archive` of the head): ~12.03 MB, "no leaks found", rc 0; CONTROL: a planted key gives "leaks found: 1", rc 1. Repo-wide Cf scan of 972 tracked files: 23 hits in 6 existing test fixtures at both main and head (identical), 0 in changed files; control fires.
4. Red without the fix (Part 77, `runs/w77-gate.txt`): the head test against main's `Controls.tsx` fails exactly 1 row, "reads the singular when exactly one field was marked" (`expected [...] to include 'Marked 1 secret field as local.'`). Head: 9/9. Plant "singular for every count" fails the 3-field row. Main to head: lost exactly the old row name, added exactly the new one, changed 0. The b778 rows: see P-T.
5. Closed lines: the FOR TUESDAY list of guide lines outside the three sections that still read Route B "as above for 0019" or UNMEASURED was re-printed by grep on the head. The list is correct: 0022 :354-360, 0023 :401-403, 0026 :626-627, 0027 :673-674 and :687 (the index line). None is edited, as the kit requires.
6. Probes / docs facts: postgres 16.15 matches. CLI template :55-57 matches. 0020's sha256 matches the file. 0024 has 6 `BETWEEN .. AND .. AND` CHECKs (supports "the six of pc.engagement_governance"). W-R sentences 1 to 4 and 6 are present in each section with only the slots filled. The header text is named only on the check line (pinned by row (2), green).
7. Scans (`runs/scans-gate.txt`), over 405 added lines and the 4 messages: names 0 (control: a planted `_by_<name>_` fires); B-number, ticket or seat in messages 0 (control fires). Added lines hold `B322` (main's existing words, re-flowed) and `b778` (a file path), as disclosed. Cf 0; secrets 0; GUIDs 0; hosts/URLs 0 (controls fire). The one non-ASCII code point is U+2026, the block's path placeholder, as in 0021. CodeQL pre-scan: `new RegExp(var)` 0, hand-escape 0, innerHTML 0, child_process 0 (control fires). Trailers 4 over 4 messages. Author = committer = the stamped identity on all 4.
8. Claims graded: see below.
9. Tier 1 as commissioned. Nothing security-shaped was found.

## Claims (builder STATUS)
| Claim | Grade |
|---|---|
| Head 9d97328, 4 commits on 5ad366c, main never moved | true |
| 77: singular for one, other counts unchanged, red first, plants red, web lost 1 / added 1 | true (re-run) |
| R20 measurement table (refusal, pre-step, from-file 0/0/0, ledger 19, rows back, schema 12 lines / 3 CHECKs, CLI line, same sha) | true (re-run from the file, independent fixture) |
| R24 / R25 tables (refusals, pre-steps, 4 / 10 CHECKs, sha, plants) | not re-measured (evidence files read: SUMMARY 34/0 and 28/0, plants 2/2; the 0024 omit-one runs exit 3) |
| DEPLOY.md replaced lines (old/new line numbers) | true |
| 0021/0022 byte-equal, every hunk in the three sections | true |
| 45 rows appended, 316 added 0 deleted, readers 170 -> 215, lost 0 | true |
| rows red against the previous section, 15 each, only the new section | true |
| lint / format:check / typecheck rc 0 | true; build: not shown by the gate |
| workspace whole 2014 rows, the same 2 SOW reds | not shown by the gate (not run) |
| gitleaks clean, ~12.03 MB | true |
| FOR TUESDAY guide-line list | true |
| grammar line about the 0020 roll-forward bullet | true; graded under F1 |
| M22 not run | disclosed; not a finding against this lane |

## NOT RUN
- M22 (0022's own form): not measured by the builder or the gate.
- R24 and R25 re-runs (the commission asked for at least one; R20 was re-run).
- The whole `workspace` vitest project (2014 rows; 2 rows need the withheld SOW text) and `npm run build`. Only the web DOM file of the workspace was run.
- Hosted CodeQL (Tuesday reads it on the PR).
- The demo VM, `gawk` vs macOS `awk` on the block, any seat stack. Nothing deployed.
- Open-PR state was not read by API (no hosted HTTP). The PR refs were read over SSH, and the open set #85/#86/#91 is taken from the kit and STATUS.
- Lock: the project heavy lock is a write in the project folder, which this gate may not make. Instead, before each heavy step the gate checked by `ls` that the lock was absent (it was absent every time). Two load reads before the first R20 run and the first b778 run were 24.37 and 24.02, at or just over the 24 limit. Both jobs were short (about 10 s and 5 s).

## Resources
Containers g1506-pg-main, -pg-fresh, -pg-pos, -node-*, -ver, -pt, -pt2, -w77, -static, -gl-*; network g1506-net; image g1506-node:head. All are removed. Census: containers 0, networks 0, volumes 0, images 0. Controls: 28 containers, bridge 1, 7 volumes, postgres 1 (`runs/census.txt`). No port published. Nothing written in the project folder (its repo status shows only the pre-existing `?? .tools/`).
