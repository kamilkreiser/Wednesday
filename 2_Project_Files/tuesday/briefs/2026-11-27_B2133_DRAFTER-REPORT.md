STARTABLE: YES

# B2133 drafter report (Datasec/NexusAI lane 2 kit 2: the data-erasure group RD-744, RD-750, RD-745 (`backend/dataErasure.js` half), RD-824; seat N181)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2133_SEAT-N181_nexusai-lane2-kit2-dataerasure.md` (198 lines), sidecar `...kit2-dataerasure.md.measured` (160 claim lines, `stamp_check.py <kit>` rc 0: "160 claims, 160 measured, 0 not measured"). Frozen folder (read-only to the seat): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s331/d2133/frozen/`. Scratch: `.../s331/d2133/` only.

## BLUF
- One kit, five commits on one branch `b2133/lane2-erasure` from main `279b22352dbcbd85664534395aeb366fec719a50`: A RD-744 (High), B RD-750, C RD-745 (its `backend/dataErasure.js` half and the C-F3 cells; the Dockerfile part stays with lane 4), D RD-824, K the counts. One product file, four new test files (58 cells), one existing cell turned (U2 of the RD-838 file), no PR, no deploy.
- Every hunk is made by a frozen program; every behaviour has a cell that is red at BASE and green after; **27 mutations were RUN, each red on exactly the named cells (one, the census resolving its own copy, is equivalent and says so)**; 154 judge calls, 154 PASS; the neighbours (34 files plus the four) 38 suites, 550 tests, 0 failed; the whole suite in the Linux shape 415 suites, 6588 tests (BASE 411 / 6530 plus 4 suites and 58 tests), 17 failed suites that are the non-git scratch tree by construction (same 17 names and same 96 failed cells as the lane-1 drafter's run).
- Model: **Opus builder, row C4 (`model-routing.md` line 94, data-destroying path; Sonnet column "no")**; **gate G1 on Opus (line 108)**; model id `claude-opus-5-5` (`models_latest.json` line 17).

## Facts re-measured (instrument; control)
- main `279b2235` (`gh api -X GET .../commits/main --jq .sha` at 01:42:43 AEDT; it is the merge of records PR 266); open PRs `[]`; `matching-refs/heads/b2133` 0 (control `heads/records` 58); open code-scanning alerts 22, none with a primary location in `backend/dataErasure.js` (control: `backend/server.js` 13).
- `backend/dataErasure.js` has not moved since the sweep read main `e789995a`: `compare` ahead 19, 16 files, none an erasure file; `commits?path=...&since=2026-10-20` length 0 (control: 37 commits at `per_page=100`).
- BASE blobs by `git hash-object` of the extracted tarball against `gh api contents?ref=BASE --jq .sha`: 11 pairs, 11 equal (list in the kit). The four new test paths read `Not Found` at BASE (control: dataErasure.js prints its blob).
- Tickets by Jira GET (description and every comment, read whole by program): RD-744 (0 comments), RD-745 (1: 39111, a gate note), RD-750 (0), RD-824 (0); all To Do. Scope sentences quoted in the kit. **Who decided:** the fix shapes of RD-744/745/750 are the coordinator's batch-3 RELEASE (C-169 line 1792 is "Tuesday, ANSWER"); RD-824 is an open question ("Tuesday's to rule"; CLARIFICATIONS line 1508 "Not decided here ... RD-824"). **No product-owner ruling rests on this lane** (the only comment is 39111; the only C-entry naming a key is line 1508).
- Landing: NexusAI `CLAUDE.md` line 273 "Tuesday can authorise: merges"; C-190 starts at CLARIFICATIONS line 2062, "Never squash, never rebase" at line 2067 (`awk NR==2067`); **no deploy: C-224 at line 2412**; `deploy-demo.yml` `paths-ignore` is `**.md`, `docs/**`, `tests/**` so a merge starts the gated `Deploy demo` run, which the seat does not touch.
- Seat id N181 free: `grep -l -w N181` over the briefs finds 1 file, the commission (control: N180 finds 8). Live panes: `tuesday` only. Slots by the project's own `worktreeSlot` (control `b2121-nodot/*` read 14, 5, 11 as B2121 printed): run 3 (21920-22559), mut 16 (30240-30879), verify 14 (28960-29599); `lsof` on each band 0 (control: 24 listeners machine-wide). Scan of 21 SEAT kits of 26-27 Nov: 21920 in 1 kit, 22559 1, 30240 0, 30879 0, 28960 1, 29599 1 (control 22560: 3). The collision with an earlier kit's band is by the slot hash and no seat is live.
- **PRIOR WORK** read from `gh api commits?path=backend/dataErasure.js` (37 commits): RD-685/C-169 (`724326f1`), RD-684 (`b5d65255`), RD-640 and RD-838 (`588ec631`, `092ed9ef`, `b214f6f0`, `380bec32`), RD-627a, RD-639, RD-575, RD-324: all kept; the one deliberate change to prior work is the turned cell U2, by the line of its own header ("RD-824 holds the ENOTDIR question. Change this cell with it."). Cells that read the same entries (the 34-file neighbour list) all pass after the change.
- Cell counts by `^[[:space:]]+test\(` (column-1 `^test\(` 0, `test.each` 0): RD-744 file 21, RD-750 9, RD-745 14, RD-824 14.
- Red-first at BASE (judge exact sets, both shapes): RD-744 18 of 21 red (green: R3, R8, C1); RD-750 6 of 9 (green O7 to O9); RD-745 9 of 14 (green K5, K8, K9, K10, K13); RD-824 11 of 14 (green N10 to N12); U2 red alone after the turn at BASE code. After the hunks all green in both shapes (Linux `TMPDIR=/tmp` plus a persistent `RUNNER_TEMP`; own `/var/folders/...`).
- Lane of record: one acquisition (tag `d2133-lane`), 02:35:53 to 02:38:25 AEDT, 152 s; 154 `JUDGE ... PASS`; 27 reverts equal the lane blob `6a88926c...`; `c1 suites 38 failed suites 0 tests 550 failed 0`. Whole suite of record (tag `d2133-full`): 02:38:30 to 03:00:23 AEDT, jest `Time: 1313.193 s`, `Tests: 96 failed, 6492 passed, 6588 total`, `Test Suites: 17 failed, 398 passed, 415 total`; a program compared its failed names and per-suite counts with `fleet/state/s330/d2121/logs-record/full-linux-final.json`: same 17, same 96; 0 of the 96 failure messages name `/tmp/`, `TMPDIR`, `persistent`, `sentinel`, `EADDRINUSE`, `mkdtemp`, `refusedInode`, `dataErasure`, `ENOTDIR`, `purgeNow` or a new file (control: `Received` 81, as B2127's run).
- Intermediate stages (A; A+B; A+B+C) each rc 0 with their own files and the erasure neighbours green (one acquisition, tag `d2133-perc`).
- Static: `static2133.py` over a scratch git repository (`sg5`) A, B, C, D each `STATIC <tag> PASS` with 15 OK lines (each scan's control fires). The first static run read FAIL for D: my log-wording change re-added a line that holds a non-ASCII marker; **I dropped that hunk** (named in LEFT FOR OTHERS 5), then reran. gitleaks 8 over the scratch `log -p`: rc 0 `no leaks found`; planted-key control rc 1.
- Expected numstat per commit (programs' output): A `75 4` + `468 0`; B `6 0` + `228 0`; C `8 3` + `285 0`; D `4 3`, `7 8` (turned file), `286 0`; whole branch `93 10` on `backend/dataErasure.js`. K shape `3 3` is B2127's (UNMEASURED for this tree: the project command writes it).

## Chain inputs (every step's inputs are made by an EARLIER step or exist at BASE)
| step | inputs | made by |
|---|---|---|
| 0 trees | BASE sha, frozen files, neigh.txt | Step 1 (clone), Step 0 (copies) |
| 1 quiet | lock base listing | exists |
| 2 lane | run/mut trees, frozen folder, neigh.txt, rt | step 0, Step 0 |
| 3 commits | lane green, frozen files, msg files | step 2, Step 0 |
| 4 heads | head of D | step 3 |
| 5 linux-update | verify tree at D | step 4 |
| 6 kstep | counts file from `verify` | step 5 |
| 7 plain | verify tree at K | step 6 |
| 8 cq | K sha | step 6 |
| 9 mainmove-last | BASE | Step 1 |
`neigh.txt` is a file at the drafter's scratch root (read-only), copied at Step 0 and `cmp`'d; its 34 paths each exist at BASE (a loop printed `lines 34 missing 0`).

## D-decisions (the drafter's; Tuesday may overrule)
- D-1 Commit order RD-744, RD-750, RD-745, RD-824 (the sweep lists 744, 745, 750, 824): the two record-semantics tickets share one region and come first; each commit is an independent hunk, so a seat stopped by the context band keeps the highest-risk work.
- D-2 RD-744 snapshots the refused names BEFORE any unlink and resolves a refusal only when "same inode and (nlink 1 or this run purged it)"; a carried entry is a dead end with a text that asks an operator (no admin surface; named). The carry is keyed by the ledger label, which is why RD-745's top-level resolve matters (relative labels).
- D-3 RD-745 resolves DATA_DIR at the top of `purgeNow` AND in the census. **Measured by running the mutations: the census-level resolve alone is an equivalent mutant** (no cell can see it; the purge already resolved), the top-level one is what the labels need (K11, K14). Kept both because the ticket names the census.
- D-4 RD-750: failed wins; the re-created file is still removed; the audit row counts the settled lists.
- D-5 RD-824: ENOTDIR at three lines (resolver call and the walk's two steps); the log line's wording left alone (a non-ASCII marker on its line).
- D-6 Added cells after the first discovery so no property is wider than its cells (B2127's lesson): R11 to R16, K12 to K14, N14; and moved "a name that cannot be read" out of the property into a named limit because no cell injects it.
- D-7 **Data safety beyond the commission's minimum:** every loader points the legacy emergency folder (a fixed absolute path the purge also names) into the cell's own temp folder (`isolateLegacy`), so no cell can touch a real one on any host; the existing erasure cells do not do this.
- D-8 Mutations judged on all five files at once (one jest run each), not on the changed file only.

## Q-questions for Tuesday (each with the default the kit is written on)
- **Q-1 One kit or split?** Default: one kit (the four are independent hunks of one file; the lane is 152 s, the two whole suites about 22 minutes each). Alternative: 744+750 first, 745+824 second.
- **Q-2 Builder model and gate tier.** Default: Opus builder (C4, line 94), gate G1 Opus, round 1 of 2 on its class (line 108). Sonnet is ruled out by the row.
- **Q-3 Turn the one existing cell U2 (and its three header lines) of `rd838-chain-canonical-key-and-cap.test.js`?** Default yes, by the frozen program (its header says to change it with RD-824). It is outside "additive test files".
- **Q-4 RD-824: does ENOTDIR join ENOENT/ELOOP, at both the resolver call and the chain walk?** Default yes at both; EACCES and EPERM stay failures. No ruling exists (line 1508 is "not decided"); it is the coordinator's call; Tuesday may answer "resolver only" (then U2 stays and N8 and b24/b25 drop).
- **Q-5 RD-745: resolve DATA_DIR once at the top of `purgeNow` as well as in the census?** Default yes (labels become relative for trailing-slash and relative spellings, which RD-745's comment 39111 says RD-424 needs; census-only would leave the labels as they are).
- **Q-6 RD-750: which list wins?** Default: failed (the name leaves filesPurged).
- **Q-7 RD-744 carried failure:** dead end with an operator-confirmation text and no admin surface; an older record is read from its text. Default yes; the confirmation surface is a later ticket.
- **Q-8 RD-745's Dockerfile part:** stays with lane 4 (the sweep). Default yes.
- **Q-9 The seat commits K** (the counts commit, `3 3`, 6588 / 415): default yes.
- **Q-10 Linux:** no Linux container run; the hosted build of Tuesday's PR is the first real Linux measurement and a fix round is possible. Default yes.
- **Q-11 Hard stop:** as the slot says; push nothing unproven.

## UNMEASURED (no instrument was run on it)
Real Linux and its inode space; the hosted build; the seat's clone, `npm ci`, the two verifies at the real branch (the pair 6588 / 415 is MEASURED by my whole-suite run but the project's `--update-counts` output at the real head is not); the K diff shape; CodeQL at the real head (no alert has a primary location in the file; related locations unmeasured); gitleaks over the real commits; the lock wrappers as the seat writes them; the push. RD-424's label mapping on a relative DATA_DIR. A name whose `lstat` fails for a reason other than absence (carried by construction, no cell). A directory or device node at a refused name. Inode numbers above 2^53. The seat's real timings.

## Outside-the-fences disclosure
- Writes: the kit, its `.measured` sidecar (a first-init copy moved to `fleet/state/s331/d2133/_quarantine/`), this report, and scratch under `.../s331/d2133/` (trees `w/*` extracted from the tarball, scratch git repositories `sg` to `sg5` with a scratch identity, logs, frozen files, helper scripts). Nothing else written.
- Read-only: GitHub by `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` (tarball, contents, compare, commits, alerts, matching-refs, pulls); Jira by GET through the B2127 drafter's read helper run by path (`.../d2127/jget.py`, which reads the project `.env` in process and prints no value; JQL not used; issue and comment GETs only); the project's `CLARIFICATIONS.md`, `CLAUDE.md`, `.tools/b2095/*` wrappers and `.tools/` listing (not modified); `session-tools/b1375/scanlib1114.py` line 20 (the four names were extracted by program into `.../d2133/names4.txt` and never printed); the model-routing, models_latest, DRAFTER_RULES, the sweep (rows and line 142), NEXT-PICKUP line 9, the B2127 kit, its ANSWER-1 and gate VERDICT. No decision-queue call, no card read, no `fleet/briefs_staged/`, scoreboard, `_ledger.md`, WEDNESDAY or FRIDAY tree.
- Jest: prototypes and the lane under the lock (tags `d2133-proto`, `d2133-disc`, `d2133-lane`, `d2133-full`, `d2133-perc`), `node_modules` a symlink to the B2032 drafter's `npm ci` (same lockfile sha256). Two whole-suite starts were stopped by `pkill -f "v2133.sh full"` (my own processes, 2 and 1 minutes in); the lock read released after each. No network call to a host, no az, ssh or docker; `git ls-remote` over ssh failed once (the clone's deploy key is repo-scoped to the seat's clone; I used `gh api matching-refs` instead). Several Bash calls were refused by the hooks (a `cd`, a stray `rm`, a zsh word-split, an unscoped recursive grep) and did not run.
- Nothing was sent to a human; no Jira or GitHub write; nothing deleted.

Drafting ended at the `date` below.
Fri 27 Nov 2026 03:02:59 AEDT
