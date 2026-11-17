STARTABLE: YES

# B1691 drafter report (SEAT-N150, lane NX-M: RD-717 and RD-749)
Drafted Wed 18 Nov 2026 07:21 to 07:36 AEDT (`date` readings 07:21:42, 07:29:46, 07:35:31). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1691_SEAT-N150_nexusai-lane-nx-m-redrive-and-clear-key-mutants.md` (168 lines), sidecar `.measured` 138 of 138, `stamp_check.py <kit>` rc 0 (run alone, not through a pipe), Stamp slot count by `/usr/bin/grep -c -E '_''_''_''_'` = 5 (four slots and the last line).

## BLUF
- **STARTABLE: YES.** Eight mutants located at main `2de5e84c`; by reading the existing cells **all eight are PREDICTED to survive** at main (none is predicted killed). Two of the eight (M-A1, M-A3) are PREDICTED unobservable through the route's HTTP surface (equivalent in a black box); M-B6 is killable only by a ledger-rewriting purge hook and is equivalent otherwise. The kit makes the seat MEASURE every plant at BASE first (old test files, whole-file runs inside the lock), drop any mutant that is red at BASE as "already guarded", and run bounded probes for the three doubtful ones; "equivalent" is an allowed, evidenced outcome.
- Cells are NOT frozen text (no jest lock for the drafter): the kit gives eight cell specs (P1 to P4 in rd681, F7 to F10 in rd684) and the seat proves each by plants. The counts file moves (cells added, no suite), so the kit copies B1680's K-commit rule (plain verify refuses on counts, `--update-counts` in its own tree, commit K, plain verify at K) and its HOLD 20 for main moving.
- Level Sonnet (C2 `model-routing.md:92`, G2 `:109`, P4 `:50` bars the local tier on Datasec, so L6 `:85` is unavailable); jest slot 7 (band 24480-25119), trees `b1691-nodot/{old9,mut1,new29,chk7,upd29}`; branch `b1691/nexusai-lane-nx-m-redrive-and-clear-key-mutants`; no PR, no Jira.

## The tickets (read whole by a GET-only reader, project `.env` in-process, no token printed; `COMMENTS total 0` on both)
RD-717 (To Do, updated 2026-09-28) and RD-749 (To Do, updated 2026-10-05). Both give the mutants as one-line labels only; the gate reports that define them (Testing Agent reports) are outside this repository and outside the drafter's fences, so **every plant in the kit is the drafter's reading of a label, UNMEASURED against the gate's own plant** (the kit says so in two places and in READY).

## Per-mutant table (product code located at main `2de5e84c`, anchors counted by `grep -c -F` over the raw files fetched through the contents API: each old string counts 1; control: a string not there counts 0)
| mutant | product code (file:line at `2de5e84c`) | existing cells read, and what they cannot see | PREDICTION | candidate cell and kill |
|---|---|---|---|---|
| M-A1 fail closed via `readStoreStrict` | `backend/server.js:16578` `const raw = jsonStorage.readFile(jsonStorage.settingsFile) \|\| {};` (strict reader at `backend/jsonStorage.js:3083`) | rd681 cells `:101,:107,:111,:115` plant only a valid ENC blob into a readable store; no torn or missing store. For a valid store strict and plain reads agree. | **PREDICTED survives**, and PREDICTED equivalent through HTTP (the ticket: a torn store answers 503 `AUTH_STATE_UNKNOWN` before the route runs; UNMEASURED) | P3 probe: answers printed at BASE and under the plant; cell only if they differ and main's answer is the stated contract; a `200 cleared` over garbage is a finding, not pinned |
| M-A2 drop `!== ''` | `server.js:16579` filter | no scenario plants an empty stored value (planted: a blob, `gpt-4.1`) | **PREDICTED survives**, killable | P1: raw `azureOpenAIDeployment: ''` alone; main answers 200 cleared with NO audit line, the plant audits |
| M-A3 old decrypting reader for the read-back | `server.js:16603` `const left = await storedAoaiFields();` | cells read settings.json raw after the route answered (`rd681:88`, `:107-117`), so the ticket's "reads raw after the route answers" is already met for the blob; but removal succeeds in every scenario, so the two reads agree | **PREDICTED survives**, PREDICTED equivalent through HTTP (differs only after a silently failed removal; a throwing write ends in the catch at `:16610` for both) | P4: one bounded attempt (read-only data dir); otherwise recorded equivalent with both answers |
| M-A4 audit names the wrong set | `server.js:16592` `orphanedFields: orphaned` | the one audit check is `audited()` `rd681:98`: `orphanedFields[^\n]*azureOpenAIApiKey`; both plants (all four fields; first held field only) still satisfy it | **PREDICTED survives**, killable | P2: exact list (`alone` is the key; `beside` is key plus deployment, in `AOAI_FIELDS` order `:16571`) |
| M-B4 only ENOENT resolves | `backend/dataErasure.js:255` `return e.code !== 'ENOENT';   // only a proven absence resolves the failure` | F2 `rd684:124` and F6b `:227` make the target vanish: lstat answers ENOENT; no cell gives another lstat error | **PREDICTED survives**, killable | F7: seeded two-entry ledger, targets through a regular file (ENOTDIR) and through a self-pointing symlink (ELOOP); drafter measured both codes by node: `ENOTDIR`, `ELOOP`, `ENOENT` |
| M-B5 dedupe | `dataErasure.js:270` `if (failed.some((f) => f && f.file === prior.file)) continue;` | in F1, F3, F4, F6 the re-drive has nothing of its own on the file (the link is gone), so no cell makes a run and its prior ledger both name one file | **PREDICTED survives**, killable | F8: re-plant the same link, re-drive, assert exactly one entry and its text is the run's own |
| M-B6 the early read | `dataErasure.js:908` (read) and `:1349` (settle) | every write of the run carries the prior ledger forward (`_writeState` `:633-705`; marker `:1032-1040`, beats omit `filesFailed`), so a late read returns the same list in every existing cell | **PREDICTED survives**, PREDICTED equivalent unless a writer empties the ledger mid-run | F9: a purge hook (`onPurge`, `:515`; hooks run `:1061`) rewrites the ledger empty through `_writeState({replacesLedger:true})`; main carries the entry (early read), the plant certifies `purged`; two designs before "equivalent". Note: the sweeper requires `dataErasure` outside `loadFor`'s `isolateModules`, a DIFFERENT instance; the kit tells the seat to print which instance to hook |
| M-B7 the live push's field | `dataErasure.js:1322` live-store push; the recovery push `:1223` and tree push `:196` are different lines | F1 asserts the error TEXT only after the re-drive; the carried entry gets the field back at `:275`; the text parse (`_survivingTargetOf` `:240`) covers a missing field | **PREDICTED survives**, killable | F10: after run 1 the raw ledger entry and the returned `failed` entry hold `survivingTarget` equal to the real target |
Result: 0 of 8 predicted killed, so STARTABLE is YES. At least 5 (M-A2, M-A4, M-B4, M-B5, M-B7) are PREDICTED killable by a clean cell.

## Facts re-measured with instruments
| fact | instrument | printed |
|---|---|---|
| main | `gh api -X GET repos/datasecau/Reporting_Dashboard_Au/branches/main --jq .commit.sha` | `2de5e84c799e32232d65cd759085d728d7141583` |
| counts at main | raw contents API, `sed -n 1,8p` | `_updated` 2026-11-17T14:25:10.296Z, tests 5870, suites 377 |
| rd681 / rd684 blobs | `git hash-object` of raw files = contents API `.sha` | `dc19f999a123`, `99ac2cb64c1a` (equal); dataErasure `26f718781fc3`, server `bf648e298429`, jsonStorage `84052ae02c1a` |
| last commits | commits API `sha=2de5e84c&path=` | rd681 `faea66b1` 2026-09-28, `4209299c`; rd684 `49ba21e1` 2026-10-19, `7085ee76`, `b5d65255`; dataErasure `380bec32`, `b214f6f0` |
| test( lines | `/usr/bin/grep -c -E '^\s*test\('` | rd681 4, rd684 7 |
| non-ASCII chars | python count of ord > 127 (control: a planted U+2014 +1) | rd681 4, rd684 15, so added lines must be ASCII |
| open PRs | `gh api -X GET .../pulls` | 2: #219 (`HISTORY.md`), #220 (3 paths: rd385 test, `backend/server.js`, `healthSweeperScheduler.js`) |
| b1687 branch | `git/matching-refs/heads/b1687`; `compare 2de5e84c...700ed93a` | head `700ed93a9da2a91613c0fcee00d32ffc65298bd6`; files exactly the rd798 and rd799 tests; no PR |
| b1691 branch | `git/matching-refs/heads/b1691` | 0 rows (control: `b1687` 1 row) |
| disjointness | the four lists above vs OWNS-B1691 | no overlap |
| slots named by the 9 non-`.pre-stamp` SEAT-N kits of 17-18 Nov | `grep -o -i -E 'slot [0-9]+'` per kit | 0,1,2,3,4,5,6,13,15,16,17 (B1687 holds 6) |
| slot program | `names1691.py` (asserts control `b1680-nodot/old34` = 2) | slot 7 trees: `old9`, `mut1`, `new29`, `chk7`, `upd29` (each assert slot 7) |
| listeners | `lsof -nP -iTCP -sTCP:LISTEN \| wc -l`; band `24480-25119` | 12 lines (11 + header); band 0 |
| panes | `tmux list-panes -a -F '#{@cockpit_name}'` | `tuesday`, `fleet-monitor` only |
| lstat codes | `node lstat1691.js` (v26.13.0) | notdir ENOTDIR, loop ELOOP, absent ENOENT, control ok |
| IPv4-shaped text | `/usr/bin/grep -c -E` over raw files (control a dotted quad: 1) | dataErasure 0, jsonStorage 0, sweeper 0, both tests 0; server.js 9 lines, none in 16560-16615 |
| model rows | `awk NR==n` of `fleet/specs/model-routing.md` | `:50` P4 No local tier; `:85` L6; `:92` C2; `:109` G2; model id `claude-sonnet-5-5` at `models_latest.json:23`; `brief_seat.sh:31` `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"` |
| CI | `gh api` raw build.yml `awk NR==29,64,93` | node-version 24; `node scripts/assert-browser.js`; `npm run verify -- --maxWorkers=2` |
| ticket greps | `/usr/bin/grep -l -F -e RD-717 -e RD-749` over the 17-18 Nov SEAT-N kits | B1687's kit only (PARTITION line); control: the sweep note prints it |

## Chain input table (rule 4: every input is produced by an EARLIER step or exists at BASE)
| step | inputs | produced by |
|---|---|---|
| 0 browser | `old9`, `scripts/assert-browser.js` | Step 1 trees; file at BASE |
| 1 base | `old9`, the two test files | BASE |
| 2 plants-base | `mut1` at BASE, plant JSONs, saved originals | Step 1 (trees, plant files written before the lock) |
| 3 probes | scratch probe versions of the P3/P4 cells in `mut1`; step 2's plant JSONs | written before the lock; step 2 |
| 4 drop | step 2 and 3 verdicts, `dropcell.py`, candidate cells in `wt` | steps 2 and 3; written before the lock |
| 5 commitAB | dropped candidates in `wt`, `commit.sh`, `msg` files | step 4, before the lock |
| 6 head | `new29` at B | step 5 |
| 7 plants-head | `mut1` at B | step 5 |
| 8 readers | `new29`, reader list | Step 1b |
| 9 mainmove | clone | Step 1 |
| 10 p-plain | `chk7` at B | step 5 |
| 11 u-update | `upd29` at B | step 5 |
| 12 kstep | regenerated counts file from `upd29` | step 11 |
| 13 p-plain-K | `chk7` at K | step 12 |
| 14 mainmove-last | clone | Step 1 |
Steps 5 to 14 are appended to the list by step 4 in the same lock acquisition (proved by `--plan` before the lock).

## D-decisions (the drafter's, Tuesday may overrule)
- D-1 Cells are specs, not a frozen patch, because the drafter has no jest; red-first is by plants at BASE then at head.
- D-2 Drop-or-keep is decided inside the chain from measured BASE plants, by a fresh `dropcell.py` (with `--plan`, exact title count 1, control).
- D-3 M-A1 and M-A3 are bounded probes with "equivalent" allowed; a garbage store answering `200 cleared` is reported, never pinned (it would be a product decision).
- D-4 Counts: B1680's K-commit rule copied; no counts hand edit; `--update-counts` only in `upd29`.
- D-5 Titles of new cells use an ASCII hyphen after the id (existing ones use an em dash); selectors `F7 - `, `RD-717 P` etc. REFUSE 5's control is `test('F5 ` (not `F5 - `, which counts 0: I first wrote that and the sidecar measurement caught it).
- D-6 Tools copied from `.tools/b1687/` (newest, green), step scripts fresh; B1687's clone is read only for the identity.
- D-7 Two commits (A rd681, B rd684) then K, so a ticket with zero kept cells makes no commit.

## Q-questions for Tuesday (each with a default)
- Q-1 The gate reports that define M-A1..M-A4 and M-B4..M-B7 are outside the fences; may a later reader fetch the exact gate plants? Default: no; plants are the drafter's reading and READY says so.
- Q-2 If P3 shows main answers `200 cleared` over a garbage store, is that a new ticket? Default: the seat reports it in READY; Tuesday decides; no cell, no product edit.
- Q-3 NX-L lands first or NX-M first? Default: independent (disjoint files, K regenerated by HOLD 13); if the held NX-A (counts file) lands first, regenerate K on the new base.
- Q-4 HARD STOP clock: left as a Stamp slot; predicted 1 hour setup plus about 2 hours lock hold (three verifies of about 24 minutes plus about 25 short runs): Default: Tuesday picks a clock that fits.

## UNMEASURED
Every prediction in the table (nobody ran a plant); that main's auth gate answers 503 over a torn store in these cells; the hook instance question in F9; Linux lstat codes for ENOTDIR/ELOOP (hosted runner); Node 24; npm version; the lock FIFO and load at launch; the real durations; whether the audit line format is parseable for P2 (the kit makes the seat print the fragment first); open code-scanning alerts (RELAYED from B1687's kit). `git merge-base --is-ancestor` literals were not run (the kit copies B1687's form; the compare of `7bc1c5d2...2de5e84c` printed "ahead, ahead_by 3, behind_by 0", which supports the control rc 1).

## Outside-the-fences disclosure
- Read-only reads outside my two files: the two tickets (two Jira GETs through a reader I wrote in the session scratchpad, `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/0f6ab911-939a-403c-8cca-13683e6f84b8/scratchpad/jwhole1691.py`; it read `.env` in-process; no token printed); GitHub GETs under the project's `GH_CONFIG_DIR`; raw copies of eight repo files in the scratchpad; B1680/B1683/B1687 kits, the B1687 STATUS (lines 500-525) and the sweep note in the briefs folder; `CLARIFICATIONS.md` line 2067; `.tools` listings and `git config --local --get user.name/user.email | wc -c` in `.tools/b1687/clone` (lengths only); the sweep note's section 4.
- One failed command: `git ls-remote` in the project checkout (its stale `core.sshCommand` names a `/Volumes/Laptop-DEV` key path): no effect; I used `gh api` instead.
- One over-broad `/usr/bin/grep -rl jwhole` plus `find` over the TUESDAY tree and `/private/tmp/claude-501` started and was stopped at 120 s by TaskStop; it read file names and contents of that tree for the string `jwhole` only, printed nothing, and I did not open any WEDNESDAY, FRIDAY, ledger or staged file it may have traversed.
- Node ran `lstat1691.js` (scratchpad) and made then removed one temp dir under `os.tmpdir()`.
- The `.measured` sidecar was written with the Write tool (not python or shell). No `decision_queue.sh`, no jest, no az, no ssh, no docker, no HTTP to any hosted host, no cd.
- Hook advisories on `grep` cases and a `| tail` rc were seen; counts were paired with controls where it mattered (the F5 control was corrected after the measurement).
