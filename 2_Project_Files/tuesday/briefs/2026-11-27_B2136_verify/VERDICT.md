GATE B2136: GO WITH FINDINGS
@ abef700 on main 279b223

Gate G1 (Opus), round 1 of 2, on lane 2 kit 2: the data-erasure group RD-744 (High), RD-750, RD-745 (its `backend/dataErasure.js` half) and RD-824. Kit B2133 with its ADDENDUM-1 (commit E); seat N181.

There is no Blocker. I found two Major findings, two Minor findings and six Info findings, and **none blocks landing** (reasons under each).

Every number the seat reported that I re-ran agrees:
- the lane: red at BASE on exactly the named cells and green at the head, in both shapes;
- 27 mutations red on exactly their named cells (b18 equivalent);
- the whole suite at 6588 / 415;
- CodeQL rc 1 at K and rc 0 at E.

The two Majors are false-`purged` shapes on this data-destroying path that the cells do not reach. I measured both with probes:
1. a refused name replaced *during* a re-drive (RD-744);
2. a link resolved lexically through a symlinked directory and `..` (RD-824).

Neither deletes a customer byte. Each makes the record certify `purged` while an outside copy keeps the bytes. For each shape, BASE either certifies too or certifies its ENOENT twin.

The pull request's hosted build is the first real Linux run (Q-10). A red on a new cell there is a fix round.

Re-measured from 09:03:58 to 09:56:46 AEDT, 27 Nov, by `gh api -X GET` (the project's GH_CONFIG_DIR, login holding datasec count 1) and by my own runs:
- **main** = 279b22352dbcbd85664534395aeb366fec719a50 = BASE (the merge of records PR 266), at both the first and the last read. The counts blob at main is 1067fa78 (= BASE's).
- **Branch** `b2133/lane2-erasure` = abef7000195f550a7bd562e33ee8e36c7b8c1adf. The tree on GitHub, aaac1a5c, equals my clone's.
- **Compare BASE...head:** ahead 6, behind 0, seven files:
  - rd744 test 468/0, rd745 test 285/0, rd750 test 228/0, rd824 test 286/0;
  - rd838 test 7/8;
  - `backend/dataErasure.js` 93/10;
  - counts 3/3.
- **Commits:** A b96228b9 (parent BASE), B cdcf3b9c, C 21db2207, D 471d8655, K 6675c397, E abef7000, each the parent of the next. Author and committer on all six: `88359143+kamilDatasec@users.noreply.github.com`.
- **Other reads:** open PRs 0; open code-scanning alerts 22; check-runs on the head: `audit-production-deps` success only.

## Measured by me (MEASURED) vs the seat's (RELAYED)
**Trees.** My clone is a `git clone --no-checkout` of the seat's clone, under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s332/g2136/clone`. It has four dot-free worktrees:
- `t/base`: BASE plus the four new test files and the turned rd838 file, copied from E (blobs d8213e82, d14e2561, e45efcb6, ec3e72e1, f3ce01ef);
- `t/head`, `t/mut` and `t/full`: all at E.

`node_modules` in each tree is a symlink to the seat's `npm ci` (disclosed). Dot segments: 0 in each tree and in `rt` (control: the seat's `.tools/b2133/clone` reads 1). Node v24.22.2.

**Jest lock.** I took two acquisitions:
- `g2136-full`, 09:08:04 to 09:30:51;
- `g2136-lane`, 09:30:56 to 09:52:32 (it queued behind the first, FIFO wait 1105 s).

Both read `lock-wrapper rc=0`. `NODE_OPTIONS` was unset (printed as unset), and `MIN_TESTS`, `MIN_SUITES` and `VERIFY_EXPECTED_FILE` were unset for the verify. No jest ran outside the lock. Every cell and every probe case works in its own `mkdtemp` folder. Afterwards the lock base lists `queue-docker queue-jest released` (no holder), and no jest, CodeQL or lock process of mine remains. Load was 2.3 at the start and 1.6 to 5.8 during the runs.

**(1) The diff, read whole** (190 lines of `backend/dataErasure.js`).
- **RD-744:** `REFUSAL_PREFIX`, `_refusalEntry`, `_refusedInodeOf`, `_snapshotRefusedNames` and `_settleRefusedNames` are added after `_hardLinkRefusal`, which is unchanged. The four call sites push `_refusalEntry(...)`. The snapshot line is placed before `purgeStartedAt`, so it runs before the marker write, the purge hooks and every unlink. The settle line follows `_settleSurvivingTargets`.
- **RD-750:** a 6-line dedupe after both settles.
- **RD-745:** `path.resolve(_dataDir())` at the top of `purgeNow`; in the census, `root` is resolved and `add` resolves its argument.
- **RD-824:** `|| e.code === 'ENOTDIR'` at exactly three lines, plus one comment line.
- Every other line is BASE's.
- **rd838:** U2's title, four assertions and three header lines.
- **E:** one unchanged assertion moved below K8's two reads (`196d195`, `203a203`).
- **Counts:** `_updated`, `tests` and `suites` only.

**(2) Red first and green, both shapes** (`tools/glane.sh`; my judge `gjudge.py` compares the exact failed set from jest `--json`). The Linux shape is `TMPDIR=/tmp` with a persistent `RUNNER_TEMP`; the own shape is `/var/folders/...`.

| File | At BASE, both shapes | At E, both shapes |
|---|---|---|
| RD-744 | 21 cells, 3 passed; failed exactly H1 to H4, R1, R2, R4 to R7, R9 to R16 | 21 of 21 |
| RD-750 | 9 cells, 3 passed; failed exactly O1 to O6 | 9 of 9 |
| RD-745 | 14 cells, 5 passed; failed exactly K1 to K4, K6, K7, K11, K12, K14 | 14 of 14 |
| RD-824 | 14 cells, 3 passed; failed exactly N1 to N9, N13, N14 | 14 of 14 |
| RD-838 (turned) | 12 cells, 11 passed; failed exactly U2 | 12 of 12 |

**(3) The 27 mutations, my own program** (`tools/gmut.py`, written from the head file with its own single-line anchors; Linux shape; each judged on all five files in one run). All 135 judgements read PASS: each mutation was red on exactly the kit's named cells, and b18 `745-no-resolve-census` was green on all five, an equivalent mutant. After every revert the blob read 6a88926c (= head). Lane total: 155 judge PASS and 0 FAIL. The 34 neighbours plus the four new files: 38 suites, 550 tests, 0 failed.

**Ten extra mutants of mine** (each run on the 34 neighbours plus the four new files):

| Mutant | Red cells |
|---|---|
| an unreadable name resolves | none (Minor 2) |
| the snapshot follows links (`statSync`) | none (Info 4) |
| the snapshot reads the raw label | R3, R8, R9 and rd685 (c) |
| the legacy parse without its prefix guard | none (Info 4) |
| "refused again" matched by file only | **none (Minor 2)** |
| the carried entry without `refusedInode` | R1, R2, R5, R6, R10 to R16 |
| EACCES/EPERM as "nothing" at the walk's directory step | U1 |
| **the same at the walk's lstat step** | **none (Minor 2; also unpinned at BASE)** |
| `inside()` without the separator | none (Info 4) |
| RD-750's dedupe limited to carried kinds | none (Info 5) |

**(4) The whole suite, once, by the project command** (`npm --prefix t/full run verify -- --maxWorkers=2`, committed counts, Linux shape, 09:08:04 to 09:30:51):
- `verify-suite: expectation — tests=6588 suites=415 (from scripts/verify-expected-counts.json)`
- `Test Suites: 415 passed, 415 total`; `Tests:       6588 passed, 6588 total`; `Time: 1366.176 s`
- `VERDICT: PASS — 6588/6588 tests passed across 415 suites (jest exit 0)`
- `EADDRINUSE` 0 (control: `Tests:` 1). `FAIL ` lines 0 (control: `PASS ` lines 415). Porcelain after: 0.
- PASS lines for the four new files, the turned rd838 file and the erasure neighbours: rd685, rd684, rd640, rd639, rd627a and the ledger-survives file.

So the pair 6588 / 415 equals the project command's measured output: BASE's 6530 / 411 plus 58 tests and 4 suites.

**(5) The probes** (`adv/g2136-probe.test.js`). This is one jest file, run under the lane's lock at BASE and at E with the same text, each case in its own temp folders; the outputs are in `out/probe-{base,head}/`. 40 cases ran, 0 errored at either side.

| Probe | At BASE | At E |
|---|---|---|
| P1: refused store replaced by an `onPurge` hook (an app write after the snapshot, during the re-drive) | `purged`, outside canary intact | **`purged`, outside canary intact** (Major 1) |
| P1b: the same at a recovery copy | `purged` | **`purged`** (Major 1) |
| P2a to e: refused, replaced, re-driven under `./d`, `./d/`, `d//`, `d/./`, `d/zz/..` | `purged` | carried, `purged_incomplete` |
| P3: outside removed, our name unreadable (EACCES at the snapshot only) | failure "could not stat" | carried (a dead end: our name was purged, the refusal kept) |
| P4: a directory at the refused name | `purged` | carried |
| P5: refused, replaced by a second hard-linked file, refused again | 1 entry; next run `purged` | 2 entries; after the second outside name is removed, the first inode's entry stays carried |
| P7: an older non-refusal text naming "inode 5 on device 7" | `purged` | `purged` (not read as a refusal) |
| P8: a carried entry stripped of `refusedInode` | n/a | dropped next run, `purged` (Info 4) |
| P9: legacy folder inside DATA_DIR, `.emergency-backup -> emergency-backup` | **`purged` on the first run, outside canary intact** | **the same** (Minor 1, pre-existing) |
| P10: 7 DATA_DIR spellings x 3 plants | refused for every plant | **only "two of our names" changes (refused -> purged)**; outside and prefix-sibling legacy refused on both sides |
| P12: macOS, a store link to `f/..namedfork/rsrc` (a fork holding bytes) | kept, failure | removed, `purged` (Info 1) |
| P13: links through an unlisted `notes.txt` inside DATA_DIR | kept | removed, `purged`; `notes.txt` untouched |
| P14: link `sd/../f/x`, `sd` a symlinked dir, local `f` a regular file; the kernel's read through the link returns the canary | kept, failure (ENOTDIR) | **removed, `purged`, canary intact** (Major 2) |
| P14b: the same with no local `f` (ENOENT) | **removed, `purged`, canary intact** | the same (the pre-existing twin) |
| P14c: control with a real local `f/x` | failure, but it names the lexical target | the same |

Across all 40 head records, the number of names in both `filesPurged` and `filesFailed` is 0.

**(6) CodeQL, the seat's tool run by me.** I ran `pr_codeql_check.sh --checkout <my clone> --work g2136/cq/...`, CLI 2.27.4, 09:53:38 to 09:55:53.
- **At K, the control that can fail: rc 1.** `results head 30 base 29`, `KEPT js/file-system-race __tests__/rd745-...test.js:202:20 fp=791124dbb925fcd7:1 [HIGH+ 7.7]`, the same as the seat's.
- **At E: rc 0.** `results head 29 base 29`, KEPT 0, NEW 0, GONE 0.
- The E head SARIF: 29 results, 1648 locations, 0 in any changed file.

**(7) gitleaks 8.30.1.**
- Control first, a random AWS-shaped pair via stdin: rc 1, `leaks found: 2`.
- `git log -p BASE..E` (1648 lines): rc 0, `no leaks found`.
- The six commit messages (52 lines): rc 0.
- My five landing texts: `no leaks found`.

**(8) The word scan, as the kit runs it.** I used `scanlib1114.py` line 20's four names, extracted by program and never printed, with the underscore-aware pattern. Each name's `x_by_<name>_y` control fired.
- 1370 added lines: 0 name hits, 0 id hits (the kit's regex; control fired), 0 skip/only/`process.platform` hits (control fired), 0 non-ASCII, 0 `/Volumes/`, 0 "product owner"/"ruling".
- Messages: 0, 0, ASCII.
- pr-title and pr-body: 0 names, 0 ids, ASCII.

**RELAYED, not re-run:** the seat's own-shape plain verifies at K and E; its static2133 prints; its push.

## The kit's questions on the data-destroying path
- **Can ANY re-drive now certify `purged` while a name outside DATA_DIR still holds the erased bytes?**
  - A replaced inode between runs: no (R1, R7, R12 to R15; P2).
  - A missing name: no (R2, R5, R11).
  - An unreadable name: no (P3).
  - Inode reuse: no, by construction: a key equal to the refused inode with nlink 1 means that inode has one name, so the outside name is gone; a number reused after the inode was freed means the bytes were already gone.
  - A relative or trailing-slash DATA_DIR: no (R15, P2a to e).
  - Refused, replaced and refused again: no (P5).
  - **One shape YES: a replacement that lands during the re-drive, after the snapshot (Major 1).** The kit's limit list does not name it.
- **Can ANY name now be unlinked that BASE would have kept?**
  - The RD-745 resolves: no. Only "both names ours" changes (P10), and a listed name outside the data directory, or in a sibling folder whose name starts with the data directory's, is still not ours.
  - The ENOTDIR change: **yes, two shapes**. A lexical path through a regular file while the kernel's target holds data (Major 2, Linux and macOS). A macOS named fork (Info 1).
- **Can ANY record name a file in both lists, or drop a removal it should show?**
  - Both lists: 0 of 40 probe records and every cell; the catch path is the kit's named limit.
  - A dropped removal: when a carried failure wins, the deletion of the replacement file at that name is not in the record (Info 5; by the kit's design).
- **Can the legacy-text parse of an older record match a text that is not a refusal?** No. It requires the text to start with BASE's exact refusal prefix (P7). Removing the guard turns no cell red, but the parse only ever adds a carry, never a resolution (Info 4).

## Tuesday's points
**(a) Q-4, ENOTDIR.**
- **The kernel half is confirmed on macOS and Linux.** A path that uses a regular file as a directory names nothing in the kernel's resolution, except macOS `..namedfork` (P12: a resource fork written and read back through `f/..namedfork/rsrc`; the resolver answers ENOTDIR, and at E the link is removed and certified).
- **The file a path runs through is never unlinked.** N1 to N14 assert it, and P13 confirms it with an unlisted `notes.txt` inside DATA_DIR that is still `KEEP-ME` afterwards.
- **But the product does not ask the kernel.** `_linkTargetOrNull` calls `fs.realpathSync`, Node's JS implementation, which joins link text with `path.resolve` and so collapses `<symlinked dir>/..` lexically. P14 shows `realpathSync` answering ENOTDIR, while `realpathSync.native` and a plain read through the link reach `OUT/real/f/x`.
- **Grade:**
  - Major 2 for the lexical shape (not blocking: P14b shows BASE already certifies the ENOENT twin of the same link);
  - Info 1 for the macOS named fork (no production host is macOS);
  - Minor 2's walk-lstat EACCES/EPERM point, unpinned, as at BASE.
- EACCES and EPERM at the resolver stay failures (N10, N11; b26 and b27 red).

**(b) Commit E.**
- **The moved assertion keeps K8 honest.** `fs.linkSync` throws unless the second name is made, so the two-name plant is guaranteed before the purge without a check. The refusal-text assertion pins "(2 names, ...; 1 of them are ours)". The moved line still asserts nlink 2 after both reads.
- **b20 (`inside()` always true) still turns K8 red, exactly** (my judge: `failed=K8 want=K8 -> PASS`).
- **CodeQL on the analysis I can run is clean at E** (rc 0, head 29 = base 29). It reproduces rc 1 at K with the seat's fingerprint, which is the control that can fail.

**(c) The other check-then-use pairs.** All are test shapes, none a race:
- RD-744 line 252 (`existsSync(s.inside)`, the last assertion of R4) and line 257 (`unlinkSync(s.inside)`, the first act of R5) are in DIFFERENT cells, on different `s` objects.
- Lines 274/276 (R6) read `lstat` to capture dev/ino and then remove the name inside the cell's own `mkdtemp` folder: a plant, not a check guarding a later use.
- RD-750 lines 122/133/145/158/170 are each the LAST assertion of O1 to O5, and lines 128/139/152/164/175 are the FIRST act of O2 to O6 (cell boundaries at lines 126, 136, 148, 161 and 173, printed by awk).
- CodeQL at E flags none of them.

**(d) Code scanning.** I read main's javascript-typescript analysis 2257151397 at 279b2235 (29 results, every primary, related and flow-step location): **0 locations in `backend/dataErasure.js`, `recoveryLocations.js`, `dataDir.js`, `customerDataFiles.js` or any changed test file** (control: `backend/server.js` holds 346). No changed line sits on a data-flow path of the 22 open alerts. My local CodeQL at E agrees: 0 locations in changed files. The PR's CodeQL run is the authority, and main's analysis at the merge commit is the check that can fail.

## Adversarial beyond the kit: three shapes outside each property
**(A) RD-744:**
- (i) A replacement during the run. NOT COVERED: Major 1.
- (ii) A directory at the name, an unreadable name, and a relative, doubled-slash, dot or dot-dot DATA_DIR. COVERED by measurement (P2, P3, P4): carried.
- (iii) A carried entry that loses its field (P8: dropped; no writer does this today, Info 4), and a recovery-dir alias (P9: pre-existing, Minor 1).

**(B) RD-750:**
- (i) Every settle path, across 40 probe records: COVERED, 0 overlaps.
- (ii) Refused-replaced-refused-again (P5): two entries in `filesFailed`, none in `filesPurged`. A named limit (one name, two failures).
- (iii) The deletion of a replacement file is not in the record when a carried failure wins (Info 5).

**(C) RD-745:**
- (i) A legacy folder whose path starts with the data directory's name (no separator). COVERED: refused on both sides. But no cell pins the separator (Info 4).
- (ii) A relative spelling with a trailing slash, for the purge and for the carry. COVERED (P10, P2b).
- (iii) An aliasing recovery directory. NOT COVERED, pre-existing: Minor 1.
- Named, not run: DATA_DIR `/`, a case-insensitive volume, a working directory that changes mid-run.

**(D) RD-824:**
- (i) A lexical path through a file while the kernel reaches data. NOT COVERED: Major 2.
- (ii) A link through an unlisted regular file inside DATA_DIR. COVERED (P13): the file survives.
- (iii) A macOS named fork (Info 1), and EACCES/EPERM at the walk's lstat step, unpinned (Minor 2).

## Findings
1. **MAJOR, does not block landing. RD-744's "this run purged it" checks the NAME, not the inode.**
   - `_settleRefusedNames` resolves when `same && (nlink === 1 || purged.includes(prior.file))`, and `same` comes from the snapshot taken before the run.
   - Probe P1: run 1 refuses `settings.json`, which is hard-linked outside. On run 2 an `onPurge` hook (it runs after the snapshot, before every unlink) stands in for an app write: it replaces the name by tmp+rename. The run unlinks the NEW inode (nlink 1, no refusal), `purged` contains the name, and the refusal resolves. The record reads `purged`, `filesFailed: []`, and the outside canary is intact. P1b gives the same at a recovery copy.
   - THE PROPERTY (A) says "or this run purged it" of the inode, and commit A's message repeats it, so the committed text is wider than the code (B2129's class).
   - **Why it does not block:** BASE certifies EVERY such replacement, whenever it happens between runs. The head certifies only one landing in the sub-second window between the snapshot and the purge reaching that name. That is a strict, large improvement, and no customer byte is deleted by it.
   - Fix shape: compare the inode the run actually unlinked at that name (record dev:ino at the unlink, or re-lstat just before it). See FOR-RECORDS ticket candidate 1. The pr-body names it as a limit.
2. **MAJOR, does not block landing. RD-824 lets the LEXICAL resolver decide "nothing behind the link".**
   - `fs.realpathSync` (JS) collapses `sd/../f/x` to `<dir>/f/x` before following `sd`. If the local `f` is a regular file, it answers ENOTDIR, and at E the link is removed and recorded `purged`, while the kernel's target (`<sd's real parent>/f/x`, read back through the link as `CANARY-P14`) holds data.
   - BASE kept this link as a failure ("could not resolve symlink: ENOTDIR"). So it is a narrow regression of exactly the shape the commission asked about.
   - **Why it does not block:** the ENOENT twin of the same link (no local `f`, P14b) already certifies at BASE and is equally easy to build. Landing widens an existing narrow hole rather than opening a class, and only the record is false: no byte is deleted.
   - Fix shape (closes both): before removing a link on ENOENT or ENOTDIR, confirm the null with the kernel-faithful walk (`_walkLinkChain` already resolves each hop's directory by realpath) or `fs.realpathSync.native`. See FOR-RECORDS ticket candidate 2. If Tuesday opens a round 2 for anything, fold both Majors in: each is a few lines with one new cell.
3. **MINOR, does not block (pre-existing, outside the diff). The RD-685 census counts one physical name twice when a recovery directory aliases another listed one.**
   - P9: legacy folder at `<DATA_DIR>/emergency-backup`, and `.emergency-backup -> emergency-backup`. The emergency copy, hard-linked outside (nlink 2), is counted as two of our names, so `ours >= nlink`. It is unlinked and the first run certifies `purged`, with the outside canary intact, at BASE and at E alike.
   - Reachable only with the legacy folder inside DATA_DIR. The default DATA_DIR `/var/lib/printer-dashboard/data` keeps it outside. Ticket candidate 3.
4. **MINOR, does not block. Three safety-relevant branches are held by no cell:**
   - (a) the inode key in "this run refused it again". A file-only match turns nothing red, yet it would forget the first inode once the second is cleared; P5 measures today's correct behaviour.
   - (b) "unreadable is carried". The resolve-on-unreadable mutant turns nothing red; P3 measures it.
   - (c) EACCES/EPERM at the walk's lstat step stay "unwalkable". The mutant turns nothing red, the same as at BASE.
   - Today's code is right on all three. A later edit could change any of them silently.
5. **INFO.** Q-4: the kernel half is confirmed on both platforms, and the file run through is never unlinked. The macOS `..namedfork` shape is removed and certified at E (P12). Production is a Linux container.
6. **INFO.** Commit E is honest. CodeQL is reproduced: K rc 1 (the control that can fail) and E rc 0. The ADDENDUM's other check-then-use pairs are test shapes across cell boundaries or plants (point c).
7. **INFO.** Code scanning: 0 locations of main's 29 results in any changed file. My local CodeQL at E: 0 locations in changed files.
8. **INFO. Robustness of the carry:**
   - The carried text does not start with the refusal prefix, so a carried entry that lost `refusedInode` would be dropped (P8). No writer in `backend/` strips fields (`withholdOutsidePaths` copies them; `_writeState` keeps whole objects).
   - The snapshot's `lstat` is backed by the surviving-target rule (the stat mutant turns nothing red, because a symlink to the outside name is still caught as a surviving target).
   - The legacy prefix guard only ever adds carries.
   - The census separator: P10 shows a prefix-sibling folder refused.
9. **INFO.** RD-750 by design: when a carried failure wins, the record omits that this run deleted the replacement file at that name (R1, P1 shapes). A name refused, replaced and refused again holds two entries, one per inode (P5; the seat's Step 1b note).
10. **INFO. First real Linux run (Q-10).** My runs were the Linux SHAPE on macOS: the five files, and the whole suite at 6588 / 415. Hard links, the dev:ino keys, the 41-link chains (Linux limit 40) and the `process.chdir` cells are first measured on real Linux by the PR's `build`. A red on a new cell is a fix round.

## Not run by the gate
Real Linux or GNU userland; any hosted run (none exists for a pushed branch beyond npm-audit); the production setting; a hosted file system's real EACCES/EPERM; the sweeper's real timing; RD-424's mapping; Jira (not read, not written); the seat's own-shape plain verify (mine was the Linux shape, which covers the counts predicate).

## Before landing (Tuesday)
1. Open the PR from `b2133/lane2-erasure` with `pr-title.txt` and `pr-body.md`. The two Majors appear there as named limits.
2. Wait with `--min-checks 7`, including `build`, the FIRST Linux run. Its log must read `VERDICT: PASS — 6588/6588 tests passed across 415 suites`.
3. Land by a merge commit pinned to abef7000195f550a7bd562e33ee8e36c7b8c1adf (never squash or rebase, C-190), and never press "Update branch" (strict is false).
4. The Deploy demo run must read both jobs skipped; approve nothing (C-224).
5. Main's javascript-typescript analysis at the merge commit must read 29.
6. File ticket candidates 1 and 2 (or open round 2 for them) before RD-744 and RD-824 move to Testing.

See landing.txt and FOR-RECORDS.md.

Files in this folder: VERDICT.md, landing.txt, pr-title.txt, pr-body.md, FOR-RECORDS.md.

Scratch (dot-free, left in place): /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s332/g2136/
- `clone/`, worktrees `t/{base,head,mut,full}`, `rt/`
- `adv/g2136-probe.test.js`; its two in-tree copies were moved to `_quarantine/probe-copies/`
- `tools/`: gmut.py, gjudge.py, glane.sh, runlane.sh, gfull.sh, runfull.sh, gwords.py, neigh.txt
- `logs/`: lane.out, full.out, full-verify-linux.log, per-run json and log, words.txt
- `out/`: main.sarif, alerts.json, probe-base/, probe-head/, mutsave/, anchorchk/
- `cq/`: k/ and e/ work folders, k.out, e.out, rc files
- `gl/`: gitleaks inputs and outputs

Nothing was written to the project checkout, its `.tools` trees, Jira or GitHub. No PR and no push. Nothing deleted (the probe copies were quarantined with mv). No alert was dismissed or commented. No background process and no lock left.
