GATE B2149: GO WITH FINDINGS
@ 52040f2 on main 279b223

Gate G1 (Opus), round 2 of 2 on the data-erasure class. Lane 2 kit 2, round 2 (kit B2142, seat N183): RD-744 Major 1, RD-824 Major 2, and the three branches no cell held. Graded over the whole branch: nine commits, A to E of round 1 plus F, G and K2.

**Neither of round 1's two Majors survives.** Each re-drive and link shape the commission named was tried at K2, and none certifies `purged` while a name outside DATA_DIR holds the erased bytes. Each shape that round 1's head certified is now carried, a failure, or kept.

There is no Blocker. I found one Major, two Minors and five Infos, and **none blocks landing**:
- **Finding 1 (Major):** pre-existing at round 1's head, and in BASE's unchanged code.
- **Finding 3 (Minor):** pre-existing.
- **Finding 2 (Minor):** branches that no cell holds; every one is right today.

Under the round-2 rule ("ship what is closed, ticket the rest"), all nine commits may land, pinned to K2. FOR-RECORDS.md files new tickets B, C and D for these findings, plus round 1's P9 as ticket A.

Every number the seat reported that I re-ran agrees:
- red first at E and green at K2, in both shapes;
- the twelve mutations;
- the whole suite at 6606 / 417;
- CodeQL rc 0 at K2, with the control at round 1's K reading rc 1.

## Re-measured
All reads were by `gh api -X GET` (NexusAI GH_CONFIG_DIR; the login holds "datasec", count 1), from 12:18:50 to 13:06:39 AEDT on 27 Nov, plus my own runs.
- **main:** 279b22352dbcbd85664534395aeb366fec719a50 = BASE, at the first read and the last.
- **The branch:** `refs/heads/b2133/lane2-erasure` = 52040f2ed92734a450f64d39fb5610451a135bd5 (one line under heads/b2133) at both reads. Open PRs `[]`, open code-scanning alerts 22, at both reads.
- **The tree:** K2's tree on GitHub is 3d241239, which equals my clone's.
- **Compare E...K2:** ahead 3, behind 0, 4 files:
  - rd744-a test 242/0;
  - rd824-a test 283/0;
  - `backend/dataErasure.js` 49/9;
  - counts 3/3.
- **Compare main...K2:** [9,0,"279b2235",9]. BASE..K2 numstat: `backend/dataErasure.js` 137/14; six new test files 242, 468, 285, 228, 283, 286; rd838 7/8; counts 3/3. That is 76 new cells by the indented pattern (7+21+14+9+11+14).
- **Commits:** b96228b9, cdcf3b9c, 21db2207, 471d8655, 6675c397, abef7000, 934c7f5b, 76515f5b, 52040f2e, each the parent of the next. Author = committer = the repo's noreply address on all nine.
- **Check-runs on K2:** `audit-production-deps` completed success only.
- **Blobs at K2:**
  - `backend/dataErasure.js` 9fdb3851 (= the kit's);
  - the rd744 round-2 test 3644a289;
  - the rd824 round-2 test 60641f0a.

## How I measured (MEASURED) and what I relayed (RELAYED)
**Trees.** My clone is a `git clone --no-checkout --no-hardlinks` of the seat's clone, at `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/g2149/clone`. It has four worktrees:
- `t/e` at E;
- `t/head`, `t/mut` and `t/full` at K2.

`node_modules` in each is a symlink to the seat's `npm ci` (disclosed). Dot segments read 0 in every tree and in `rt` (control: the seat's `.tools/b2142/clone` reads 1). Node v24.22.2.

**Jest lock.** I took two acquisitions:
- `g2149-full`, 12:20:21 to 12:46:11 (acquired after 0 s);
- `g2149-lane`, 12:46:59 to 13:02:48. It queued FIFO behind another seat's ticket (b2143-lane) and was acquired after 1200 s.

Both read `lock-wrapper rc=0`. `NODE_OPTIONS`, `MIN_TESTS`, `MIN_SUITES` and `VERIFY_EXPECTED_FILE` were unset (printed). No jest ran outside the lock, and every probe case works in its own `mkdtemp` folders. Afterwards, no process of mine remains. The lock is now held by another seat's tag (b2143-linux-update), not mine. Load was 3.0 to 4.8.

**(1) The diff, read whole** (E..K2, `backend/dataErasure.js`):
- `_kernelTargetOrNull` added;
- the resolver's ENOENT/ENOTDIR line returns it;
- the walk's directory step uses `realpathSync.native`;
- the walk's link step joins without `path.resolve`;
- `_noteRemovable` at both pass-through returns of `_hardLinkRefusal`;
- `listedNames.removed = new Map()`;
- `_settleRefusedNames(…, dataDir, removed)` resolves on `removedHere`;
- the comment is corrected.

Every other line is E's.

**The four removal sites** (lines 212/217, 498/509, 1328/1333 and 1429/1436 at K2): each calls the check and then unlinks, with no `await` between them. Each site's `_linkTargetOrNull` call sits inside a try whose catch records a failure BEFORE the unlink: at lines 208, 507, 1319 and 1420.

**(2) Red first at E, green at K2, both shapes** (my `tools/glane.sh` and the exact-set judge `gjudge.py`; Linux shape = `TMPDIR=/tmp` plus a persistent `RUNNER_TEMP`; own shape = `/var/folders/...`):

| File | At E, both shapes | At K2, both shapes |
|---|---|---|
| rd744 round 2 | 7 cells, 3 passed; failed exactly V1, V2, V6, V7 | 7 of 7 |
| rd824 round 2 | 11 cells, 2 passed; failed exactly W1 to W8, W11 | 11 of 11 |
| round 1's five files | (round 1's gate) | 21, 9, 14, 14, 12, all green |

**(3) The twelve mutations, my own program** (`tools/gmut.py`, anchors written from K2's lines, each asserted once; Linux shape; each judged on all seven files). All 84 judgements read PASS, each red on exactly the kit's cells:

| Mutation | Red cells |
|---|---|
| b01 | V1, V2, V6, V7 |
| b02, b03 | V5 and R8 |
| b04 | V3 |
| b05 | V4 |
| b06 | W1 to W6, W11 |
| b07 | W11 |
| b08 | W10, R14, and N1 to N7, N9, N13, N14 |
| b09, b10 | W7, W8 |
| b11, b12 | W9 |

After every revert the blob read 9fdb3851. The lane total is 102 judge PASS and 0 FAIL. The neighbourhood (34 neighbours plus six lane files): 40 suites, 568 tests, 0 failed.

**Seven extra mutants of mine** (each on those 40 suites):

| Mutant | Red cells |
|---|---|
| "removed here" without `purged.includes` | none (Finding 2) |
| the recorded key without `path.resolve` | none (equivalent: every site passes an absolute path) |
| the lookup by raw label | V5, R8 |
| the kernel confirm for ENOTDIR only | W5 |
| also noting refused names | none (equivalent under the `purged.includes` guard) |
| no note at the "every name is ours" return | none (Finding 2; removing it only fails safe) |
| the walk's directory-step null removed | N8 |

**(4) The whole suite, once, by the project command** (`npm --prefix t/full run verify -- --maxWorkers=2`, committed counts, Linux shape):
- `verify-suite: expectation — tests=6606 suites=417 (from scripts/verify-expected-counts.json)`
- `Test Suites: 417 passed, 417 total`; `Tests:       6606 passed, 6606 total`; `Time: 1549.395 s`
- `VERDICT: PASS — 6606/6606 tests passed across 417 suites (jest exit 0)`
- `FAIL ` lines 0 (control: `PASS ` lines 417); `EADDRINUSE` 0 (control: `^Tests:` 1); porcelain afterwards 0.
- PASS lines for both new files, round 1's five files, and the neighbours rd685, rd684, rd640, rd639 and rd627a.

So the pair 6606 / 417 equals the project command's measured output, and equals the seat's two verifies (RELAYED).

**(5) The probes.** One acquisition ran three files at E and at K2 with the same text, in the Linux shape:
- my `adv/g2149-probe.test.js` (68 cases);
- round 1's `g2136-probe.test.js` (40 cases);
- Tuesday's stamp probe `t2142-probe.test.js` (4 cases).

All 112 cases ran with 0 errors on each side. Outputs: `out/probe-{e,head}/`. Across all 101 records at K2, the number of names in both `filesPurged` and `filesFailed` is 0.

**(6) CodeQL, the seat's tool run by me** (`pr_codeql_check.sh`, one work folder `cq/w`, 13:04:00 to 13:05:56):
- **K2: rc 0.** `results head 29 base 29`, KEPT 0, NEW 0, GONE 0.
- **The control at round 1's K (6675c397): rc 1.** `results head 30 base 29`, KEPT `js/file-system-race __tests__/rd745-…test.js:202:20 fp=791124dbb925fcd7:1 [HIGH+ 7.7]`, the seat's and round 1's fingerprint.
- **The head SARIF:** 29 results and 1648 locations, with 0 in `backend/dataErasure.js` or either new file (control: `backend/server.js` holds 346).

**(7) gitleaks 8.30.1:**
- control first, a random AWS-shaped pair via stdin: rc 1, `leaks found: 2`;
- `git log -p E..K2` (731 lines): rc 0, `no leaks found`;
- the three round-2 messages (24 lines): rc 0;
- my four landing texts: `no leaks found`.

**(8) The name scan, with the right four names.** I extracted them with the frozen `names2142.py` (sha256 b0ae9573…; it printed `names 4 found [True, True, True, True]`). Their lengths are 5, 7, 3 and 5, the right form (F-1: round 1's drafter file held 5, 7, 4 and 6). The names are never printed. The scan is underscore-aware, and each `x_by_<name>_y` control fired.
- All 1939 added lines of BASE..K2: 0 hits, 0 non-ASCII.
- All nine messages (70 lines): 0.
- pr-title, pr-body, landing and FOR-RECORDS: 0 names; 0 build, seat or session ids in the title and body (control fired).

**RELAYED, not re-run:**
- the seat's own-shape plain verify at K2;
- its static2142 prints;
- its push;
- Tuesday's stamp clauses C1 to C6 (I re-ran the stamp probe file itself: C2, C4, C5 and C6 are carried or kept at K2, purged at E).

## 1. Round 1's two Majors, now
**Can any re-drive still certify `purged` while a name outside DATA_DIR holds the erased bytes? No, on every shape tried.**
- **Inode replaced at the four sites:**
  - P1 and P1b (round 1's probes) read `purged` at E and `purged_incomplete` at K2, canary intact.
  - My matrix replaced the refused name during the re-drive at the live, copy, tree and sibling sites. I ran it under `dir`, `dir/`, a doubled slash, `dir/.`, `dir/zz/..`, a relative spelling and a symlinked DATA_DIR: 26 replaced shapes. Every one read `purged` at E and carried at K2.
  - Replaced before the snapshot: carried (round 1's P2, R1, R7 and R12 to R15, all green).
- **Non-normalised or symlinked DATA_DIR:** the recorded key (`path.resolve(p)`) and the looked-up key (`path.resolve(dataDir, prior.file)`) agree under every spelling. The liveness twin, the outside name removed during the re-drive, certified under all 26 shapes. A disagreement could only fail safe: the value compared is the refused inode.
- **Inode reuse in one run:** probe R4 (the hook removed both names and re-created ours hard-linked out) read carried, with no reuse on APFS. By construction: `removed[name] === refusedKey` means the check read that inode at that name with every name ours (or one link). An inode still held outside cannot be freed and reused.
- **Refused, replaced, refused again:**
  - V3 and P5: carried.
  - My R3a: run 3 removes the second outside name, and only the first inode's entry stays.
  - My R3b: the name is replaced during run 3, and both entries stay.

**Can any link now be removed and certified purged while the kernel reaches data through it? Yes, one family, pre-existing: Finding 1.** Everything the commission listed is closed:

| Shape | At E | At K2 |
|---|---|---|
| P14, P14b | ok true | ok false, the kernel target named |
| L6, a symlinked dir mid-chain | `purged` | failure |
| L7, an absolute text through `sd/..` | `purged` | failure |
| L8, a 41-link chain with `sd/../c2/hop21` at hop 20 | `purged` | kept |
| L9, a 41-link chain ending in an absolute `sd/..` text | `purged` | kept |
| L4, a kernel target inside DATA_DIR, unlisted | `purged` | failure |
| L4b, a kernel target inside DATA_DIR that is a listed store | `purged`, store removed | `purged`, store removed |

L4b is correct at both: the bytes are gone. The failure text of L4 names the canonical path.

## 2. The new code's own risks
- **(a) `_noteRemovable` records only a regular file the check passed, and every site unlinks next, synchronously.**
  - (b) of the property also requires `purged.includes(name)`, which only a successful unlink at that name sets.
  - Probe R5 recorded a note and then had the unlink fail (EBUSY injected after the outside name was removed). The run kept the refusal and the EBUSY failure: `purged_incomplete`.
  - No path can satisfy (b) falsely, apart from the census over-counting our names, which is pre-existing (P9, ticket A).
  - The `purged.includes` guard itself is held by no cell (Finding 2).
- **(b) `_kernelTargetOrNull`'s throw is caught at every caller.**
  - L11 injected EIO into the kernel resolution at the copy, tree, sibling and live sites. Each time, the link was kept, the failure recorded, the run completed, and an ordinary store was purged in the same run.
  - L12 did the same at the walk's directory step: the chain is unwalkable and the link kept.
  - Nothing aborts the purge run.
- **(c) The walk's unnormalised join.**
  - The next hop's directory is resolved by the kernel before `lstat` and before the loop key is taken. So `cur` is always a canonical directory plus one basename, and `path.join` with a canonical parent makes `..` and `.` safe.
  - Absolute text is taken whole, then canonicalised at the next hop.
  - The loop key and the 256-link cap are untouched (the drafter's D-7, read in the diff).
  - No crafted text escapes them. L8, L9 and L10 show kernel-faithful ends, and a kernel loop is kept (`ELOOP`).
- **(d) Code scanning.**
  - Main's analysis 2257151397 at 279b2235 (29 results, 1648 locations) has 0 locations in `backend/dataErasure.js`, either new test file or the counts file (control: `backend/server.js` 346).
  - The 22 open alerts sit in incidents.js, jsonStorage.js, entraProvisioning.js, server.js, emailService.js and uat-run.js.
  - My local CodeQL at K2 agrees.
  - The PR's CodeQL run is the authority, and main's analysis at the merge commit is the check that can fail.

## 3. Red first, green, mutations, whole suite: see (2) to (4) above. Every count matches the kit and the seat.

## 4. Three shapes outside each property
**(A2) RD-744:**
- (i) non-normalised and symlinked DATA_DIR at all four sites, both directions: COVERED (26 + 26 shapes);
- (ii) refused, replaced and refused again, with a run-3 event: COVERED (R3a, R3b);
- (iii) a name replaced by a directory during the re-drive (R6) and an unlink that fails after the note (R5): COVERED, both carried.

Named limits:
- a store replaced during the FIRST run (P1c: `purged`, outside canary intact, at E and K2) is Finding 3;
- the census alias (P9) is ticket A;
- the lstat-unlink instant is the kit's limit. It is unreachable unless another process re-creates an outside link in that instant, because the check passing proves no outside name existed.

**(D2) RD-824:**
- (i) the resolver's SUCCESS answer is lexical: NOT COVERED, Finding 1 (L1, L3);
- (ii) a mid-chain symlinked directory, absolute text, and long mixed chains: COVERED (L6 to L9);
- (iii) a kernel target inside DATA_DIR (L4, L4b): COVERED. A kernel loop beyond `..` (L10) is kept, a liveness limit (Info).

**(E2) Nothing else changes:**
- (i) round 1's 58 cells and the 40-suite neighbourhood are green at K2, and the whole suite is 6606/417;
- (ii) RD-750: 0 names in both lists across 101 records;
- (iii) RD-745's seven-spelling matrix (P10, 21 cases) is identical at E and K2.

Named, not run: real Linux (glibc), the production image's musl `realpath(3)`, a network-share DATA_DIR, and real EACCES/EPERM.

## Findings
1. **MAJOR. Does not block (pre-existing; not introduced by this branch). The resolver's SUCCESS answer is lexical, so a link can be removed and certified while the kernel reaches data through it.**
   - Probe L1: `feedback.json -> sd/../learning_data.json`, where `sd` links to a folder outside and the local `learning_data.json` is a listed store.
   - `fs.realpathSync` answers the local store. `realpathSync.native` and a read through the link reach `<outside>/real/learning_data.json` (`CANARY-g2149`).
   - The run records a surviving-target failure on the local path, then purges that store later in the loop, and `_settleSurvivingTargets` resolves the failure: `purged`, `filesFailed: []`, canary intact. The same happens at E.
   - L3 (round 1's P14c): the failure names the local `f/x`. The operator deletes it, as the text says, and the re-drive certifies `purged` with the canary intact. The same happens at E.
   - L2, the order reversed, is now caught at K2: the resolver answers ENOENT and the kernel confirms. It certified at E.
   - The success branch is BASE's code, unchanged, so landing makes nothing worse and closes L2.
   - Round 1's FOR-RECORDS candidate 2 already pointed at P14c. Ticket B in FOR-RECORDS; named in pr-body.
   - Fix shape: use the native answer whenever it differs (a few lines, one cell per shape).
2. **MINOR. Does not block. Branches no cell holds.** The mutants turned 0 of 568 tests red:
   - (a) `purged.includes` in `removedHere` (probe R5 measures today's correct result);
   - (b) the note at the "every name is ours" return (removing it only fails safe);
   - (c, d) noting only passed names and resolving the key: equivalent today.
3. **MINOR. Does not block (pre-existing, outside RD-744's carry). A store hard-linked outside and replaced by an app write during the FIRST run hides the outside link.**
   - Round 1's control P1c: `purged`, outside canary intact, at E and K2.
   - No refusal exists to carry, so RD-744's scope does not reach it.
   - Ticket C; named in pr-body.
4. **INFO. Liveness.** A link through a kernel loop beyond `..` (L10) is now kept forever as unwalkable (ELOOP). E removed it; BASE kept it (by reading the walk: lexical ENOTDIR was not "nothing" at BASE). It is conservative.
5. **INFO. The production image is `node:24-alpine` (musl)** (Dockerfile line 2). No cell has run on musl `realpath(3)`. The hosted build is ubuntu glibc (build.yml node 24), and my runs and the seat's were macOS. Named in pr-body.
6. **INFO. Commit A's message vs F.** Commit A's pushed message says "or this run purged it". F's message and the corrected comment say what the code does. pr-body says so.
7. **INFO. Round 1's carry-overs re-measured at K2, unchanged:**
   - P9 (round 1's Minor 1, now ticket A);
   - P8 (a stripped `refusedInode` is dropped; no writer strips fields);
   - P12 (macOS named fork);
   - P13 (the file run through is untouched).
8. **INFO. F-1.** The rescan with the right four names reads 0 over BASE..K2, all messages and my texts.

## Which commits could land
None of the findings blocks. Land all nine, by a merge commit pinned to 52040f2ed92734a450f64d39fb5610451a135bd5.

If Tuesday instead treats Finding 1 or 3 as blocking, neither lives in any commit of this branch: both reproduce at E and rest on BASE's code. So no commit subset is safer than K2. Landing only A to E would re-open round 1's two Majors (P1, P14 certify at E). F and G cannot land without A to E (they edit A's and D's lines). K2 is required by the counts.

## Not run by the gate
- real Linux (glibc) and musl;
- any hosted run (none exists beyond npm-audit);
- the production setting;
- real EACCES/EPERM;
- BASE itself (round 1's gate measured BASE; my comparisons are E vs K2, and BASE claims are by reading);
- Jira (not read, not written);
- the seat's own-shape plain verify (mine was the Linux shape with committed counts).

## Before landing (Tuesday)
1. Open the PR from `b2133/lane2-erasure` with `pr-title.txt` and `pr-body.md`.
2. Wait with `--min-checks 7`. `build` is the FIRST Linux run, and its log must read `VERDICT: PASS — 6606/6606 tests passed across 417 suites`. A red new cell is a fix round.
3. Merge commit pinned to 52040f2ed92734a450f64d39fb5610451a135bd5 (C-190, line 2067). Never squash, rebase or "Update branch".
4. The Deploy demo run must read both jobs skipped. Approve nothing (C-224).
5. Main's javascript-typescript analysis at the merge commit must read 29.
6. File new ticket B before RD-824 moves to Testing (FOR-RECORDS).

Files in this folder: VERDICT.md, landing.txt, pr-title.txt, pr-body.md, FOR-RECORDS.md. Round 1's landing.txt and pr-body.md are SUPERSEDED.

Scratch (dot-free, left in place): /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s333/g2149/
- `clone/` and the worktrees `t/{e,head,mut,full}` (porcelain 0 in each); `rt/`
- `adv/`: g2149-probe.test.js, plus copies of g2136-probe.test.js and t2142-probe.test.js
- `tools/`: gmut.py, gjudge.py, glane.sh, runlane.sh, gfull.sh, runfull.sh, gwords.py, rp.js, neigh.txt
- `logs/`: lane.out, full.out, full-verify-linux.log, and each run's json and log
- `out/`: main.sarif, probe-e/, probe-head/, anchorchk/, rp/
- `cq/`: k2.out, ctl.out, w/
- `gl/`: the gitleaks inputs and outputs, and names.txt (mode 600, never printed)
- `_quarantine/`: probe-copies-{e,head}/ and e-newfiles/ (moved out of the trees with mv)

Nothing was written to the project checkout, its `.tools` trees, Jira or GitHub, apart from the lock files `nexusai-lock.sh` writes. No PR and no push. Nothing was deleted. No alert was dismissed or commented on. No background process and no lock of mine is left.
