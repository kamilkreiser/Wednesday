STARTABLE: YES

# B2142 DRAFTER REPORT - NexusAI lane 2 kit 2, ROUND 2 OF 2 (RD-744 Major 1, RD-824 Major 2, the three unheld branches), seat N183

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2142_SEAT-N183_nexusai-lane2-kit2-round2.md` (186 lines at the last edit; lines over 2000 characters: 1 and 154) and its sidecar `.measured` (145 claims, `stamp_check.py <kit>` rc 0, 145 of 145 measured). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s332/d2142/` (frozen files in `frozen/`). Drafted in session s332 by an in-session Opus drafter, read-only outside these three files and the scratch folder.

## BLUF
- **Both Majors are closed by measured code, and the three unheld branches are now held.** Two hunks on E's `backend/dataErasure.js` (F: 24 added / 6 removed; G: 25 / 3), two new test files (7 and 11 cells), three new commits after E (F, G, K2), no rewrite, one fast-forward push.
- **Major 2: the chain walk does NOT close P14; `fs.realpathSync.native` does.** The walk joins link text with `path.resolve` too (it answered `end: null` on P14, P14b, a 3-link chain and a 41-link chain). So the resolver's ENOENT/ENOTDIR is confirmed by the kernel's resolution, AND the walk's two joins are made kernel-faithful (Q-2, Q-3). P14 and P14b both become cells red at E and green after (W1, W5), at all four sites (W1 to W4).
- **Major 1:** "this run removed it" is now the device:inode the removal's own hard-link check read immediately before the unlink (recorded at all four sites, including one-link names: the drafter measured that recording only multi-link names turns round 1's R8 red). P1 and P1b are cells V1 and V2, red at E, green after, plus the same at the tree and sibling sites (V6, V7).
- **Measured, not predicted:** lane of record 99 judge calls, 99 PASS; twelve mutations each red on exactly its named cells; whole suite in the Linux shape 6606 / 417 (the K2 pair); CodeQL head 29 = base 29, rc 0, with the control at round 1's K reading rc 1 with the known fingerprint.

## FACTS RE-MEASURED (instrument, control)
1. Heads at 10:00:12 and again at 11:02:45 (`gh api -X GET`, NexusAI GH_CONFIG_DIR, login holding datasec count 1): main `279b22352dbcbd85664534395aeb366fec719a50`; `matching-refs/heads/b2133` one line, `refs/heads/b2133/lane2-erasure abef7000195f550a7bd562e33ee8e36c7b8c1adf` (control: `matching-refs/heads/records` length 58); open PR head refs `[]`.
2. E's `backend/dataErasure.js` = blob `6a88926cb35456368ec13986958cef25634701ef` (git show from a clone of the gate's clone, `git hash-object`); E's counts file blob `9c073f40...`, 6588 / 415; `abef7000~6` = BASE.
3. The probe of the two candidate confirms (`d2142/probe/rp.js`, Node 24, E's own walk text evaluated): see kit finding 2. Control: on the fixed file the same program printed a kernel end in all five shapes.
4. Lane of record (`frozen/lane2142.sh` under lock tag `d2142-lane`, 10:35:05 to 10:37:21, load 1.44): `logs/lane.out`; `grep -c '^judge '` 99, all `rc=0`; 99 judge logs end `PASS`; 16 `jest rc=1` lines (4 red-first, 12 mutations); every reverted blob `9fdb3851`; `c1 suites 40 failed suites 0 tests 568 failed 0`.
5. Whole suite, Linux shape, run of record (tag `d2142-full`, 10:39:49 to 11:01:34): `Test Suites: 17 failed, 400 passed, 417 total`, `Tests: 96 failed, 6510 passed, 6606 total`; the 17 / 96 are identical by suite name and per-suite count to round 1's drafter run `s331/d2133/logs/full5/full-linux.json` (program), the non-git scratch tree by construction. An earlier run with the 5-cell RD-744 file read 6604 / 417 and the same 17 / 96.
6. CodeQL 2.27.4 on scratch clone `d2142/sg2` (E plus the drafter's F, G, K2 commits; F `e6a023a3`, G `b4b20a81`, K2 `c2992dad`, identity `scratch`, scratch only): `--base 279b2235 --head b4b20a81` rc 0, `results head 29 base 29`, KEPT 0, NEW 0; control `--head 6675c397` rc 1, KEPT `js/file-system-race` at `rd745-...test.js:202:20`, `fp=791124dbb925fcd7:1`. Head SARIF: 0 of 1648 locations in the three changed files (control `backend/server.js` 346).
7. Static and gitleaks on `sg2`: F, G, K2 each 15 OK lines then `STATIC <tag> PASS`, rc 0; `node --check` rc 0; gitleaks over each staged diff and over `log -p E..K2` `no leaks found`; the planted pair `leaks found: 1`, rc 1. The ban-list scan (four names from `names2142.py`, underscore-aware, each control fired) over all 1939 added lines BASE..K2 and 66 message lines: 0.
8. Slots (python sha256 of the real path mod 19; control b2121 run 14 / mut 5 / verify 11, b2133 run 3): run 2, mut 10, vfy 12 (`verify` would be 10). Kit scan: 21280/21919 in 1 kit (B2110 lane-4 verify, no live pane), others 0 (control 21920 reads 2); `lsof` of each band 0 (control 20 listeners).
9. The jest lock base before and after every run (last at 11:01:41): `queue-docker queue-jest released`.

## D-DECISIONS (the drafter's, inside the commission)
- D-1 Tree `b2142-nodot/vfy`, not `verify` (slot collision with `mut`).
- D-2 STEP CQ carries a REQUIRED control run at round 1's K (`6675c397`), rc 1 expected, in the same work folder (base DB reused): the check that can fail.
- D-3 `judge_cells.py`, `v2133.sh` and round 1's 34-file neighbour list reused byte for byte (same sha256).
- D-4 A frozen `names2142.py` extracts the four ban-list names (see FINDINGS F-1 for why).
- D-5 V6 and V7 added so (A2)'s "at any of the four removal sites" is held by cells, not only by construction.
- D-6 `_noteRemovable` records at the one-link return as well as the all-ours return (mutation b03, multi-only, turns R8 and V5 red: both are needed).
- D-7 The walk's loop key, cap and "kept at real data" rule are untouched; only its two path joins change.
- D-8 The lock wrapper is printed in the kit as text (not "token for token as another file"), with T, FR, RT, LOGS, LN, MT, NEIGH, OWN_TMPDIR exported for both `lane2142.sh` and `v2133.sh`.

## THE CHAIN'S INPUTS (MEASURED LITERALS rule 4: each input made by an earlier step or present at E)
| step | inputs | made by |
|---|---|---|
| Step 0 | kit, report, frozen folder, neighbour list | Tuesday / this drafter (exist) |
| Step 1 | project checkout, origin, deploy key, round-1 clone identity | exist at drafting (`.tools/b2133/clone` config lengths 12 and 46) |
| Step 1b | clone at E, frozen `apply2142.py`, `names2142.py`, scanlib1114.py | Step 1, Step 0, exists |
| 0 trees | clone at E | Step 1 |
| 2 lane | run, mut, rt, frozen files, neighbour list | step 0, Step 0 |
| 3 commits | wt at E, frozen hunks and files, names file | step 0, Step 0, Step 1b |
| 4 heads | G in the clone (wt is its worktree) | step 3 |
| 5 linux-update | vfy at G | step 4 |
| 6 k2 | the counts file in vfy | step 5 |
| 7 plain | vfy at K2 | step 6 |
| 8 cq | K2 in the clone; 6675c397 in the clone (fetched with the branch) | step 6, Step 1 |
| 9 / push | origin reads | Step 1 |

## Q-QUESTIONS FOR TUESDAY (each with the default the kit is built on)
- **Q-1 Shape.** Default: three NEW commits F (RD-744), G (RD-824), K2 (counts) after E on the same branch; nothing rewritten; one fast-forward push. Alternative: one combined commit (less reviewable per ticket).
- **Q-2 RD-824's confirm.** Default: the resolver's ENOENT/ENOTDIR is confirmed by `fs.realpathSync.native`; a kernel path is the target (link removed, failure naming it), only a kernel ENOENT/ENOTDIR is "nothing", any other kernel answer keeps the link. Alternative the commission named, the chain walk: MEASURED NOT to close P14 (`{"end":null,"hops":1}`).
- **Q-3 The walk.** Default: fix it too (its link step joins without normalising, its directory step uses the native resolver), because a 41-link chain ending `sd/../f/x` with a local regular file is the same Major-2 regression (BASE kept it; E removes and certifies; W7) and the ENOENT twin is pre-existing (W8). Alternative: name both as limits and leave the walk byte for byte.
- **Q-4 RD-744's record.** Default: record the device:inode the removal's own hard-link check read (a Map on the per-run census function; no signature change at the four sites). Alternative: an explicit `lstat` immediately before each of the four unlinks (more lines; a check-then-unlink pair that CodeQL's file-system-race rule may read; unmeasured).
- **Q-5 A kernel ELOOP after a lexical ENOENT/ENOTDIR.** Default: thrown, the link kept as a failure (no plant reaches it). Alternative: hand it to the walk.
- **Q-6 Where the cells live.** Default: two NEW files (`rd744-a-refusal-resolves-on-the-inode-this-run-removed.test.js`, `rd824-a-lexical-null-is-confirmed-by-the-kernel.test.js`); round-1 files untouched. Alternative: append to round 1's files (needs a frozen edit program; counts move the same way minus 2 suites).
- **Q-7 The gate's Minor 1 (P9).** Default: NOT in this round; a separate ticket from the records pass (pre-existing, needs the legacy folder inside DATA_DIR). Alternative: fold it in (a census keyed by real parent plus basename; new cells; more risk on the landed RD-685 path).
- **Q-8 Model and gate.** Default: Opus builder (row C4, line 94), gate G1 (line 108) on Opus, round 2 of 2; after a NO GO, ship what is closed and ticket the rest.
- **Q-9 K2.** Default: the seat commits K2 (pair 6606 / 417, measured); Tuesday regenerates at landing if main's pair moved.
- **Q-10 The Linux leg.** Default: no container run; the PR's hosted build is the first real Linux run; a red on a new cell is a fix round.
- **Q-11 Hard stop.** Default: push nothing unproven; Tuesday writes the clock.

## FINDINGS FOR TUESDAY (outside the commission's questions)
- F-1 **Round 1's drafter file `s331/d2133/names4.txt` holds two of the four ban-list names with a leading `b`** (the `\b` escape half-stripped; lengths 5,7,4,6 against the right 5,7,3,5; the right ones are found in scanlib1114.py line 20 as `\b<name>\b`). Whether round 1's seat and gate used that form is UNMEASURED (each extracted its own). The drafter rescanned every added line of BASE..K2 and every message with the right four: 0 hits. A name scan over a `b`-prefixed token would have read 0 falsely on those two names.
- F-2 **Kit B2139 (lane 2 kit 3, N182) is not stamped and its REFUSE 4(b) names `abef7000` "or the head Tuesday's STAMP names"**: its stamp must name this round's landed head (K2's sha, then the merge).
- F-3 Round 1's `landing.txt`, `pr-title.txt` and `pr-body.md` (in `B2136_verify/`) describe head `abef7000` and list the two Majors as limits: superseded by this round; round 2's gate writes the new ones.
- F-4 Commit A's pushed message still says "or this run purged it"; F's message and the corrected comment say what the code does. The PR body should say so (the gate reads both messages).
- F-5 The gate's VERDICT says the walk "already resolves each hop's directory by realpath" (Major 2 fix shape); measured: its directory step did, but its link step had already collapsed `..` lexically, so the walk answered `end: null` on P14.

## UNMEASURED
The seat's clone, `npm ci` and real commits (other shas, same trees); `npm run verify -- --update-counts` at the real G and the plain verify at K2 (the pair is MEASURED by jest directly at 6606 / 417, the project command's output is not); CodeQL at the real K2 (the scratch head's javascript trees equal it: K2 adds only the counts file); the push; real Linux and a hosted file system's real errnos; the production setting; Jira (not read, not written: the tickets' current comments and states are not re-read by this drafter); RD-424's label mapping; whether round 1's seat and gate scanned with the right four names (F-1).

## OUTSIDE-THE-FENCES DISCLOSURE
- Writes: only the kit, its `.measured` and this report under `tuesday/briefs/`, and scratch under `fleet/state/s332/d2142/`. Nothing written in the NexusAI project folder, its `.tools` trees, Jira, GitHub or the card store, EXCEPT what the commission requires of every jest run: the lock files the project's `nexusai-lock.sh` writes in `session-tools/locks-laptop-1017/` (five acquisitions: `d2142-proto`, `d2142-disc`, `d2142-full` twice, `d2142-lane`; each released; the base read `queue-docker queue-jest released` after the last).
- Reads in the project: `CLARIFICATIONS.md` line 2067, `session-tools/b1375/scanlib1114.py` line 20 (names never printed), `session-tools/nexusai-lock.sh` lines 1 to 40, the `Briefs/` listing and round 1's STATUS and HANDOVER last lines, `.tools/b2133/clone` config lengths (`git config --get`, values never printed). Gate scratch `g2136/` read and cloned (`git clone --no-hardlinks`), never written.
- `gh` was `-X GET` only under the NexusAI GH_CONFIG_DIR; no HTTP to any host; no az, ssh, docker.
- Scratch git: `d2142/sg` (a clone, detached at E, local identity `scratch`) received two commits with an earlier 5-cell test file, then was MOVED to `d2142/_quarantine/sg-old-vfile` (never deleted); `d2142/sg2` holds the record commits (F `e6a023a3`, G `b4b20a81`, K2 `c2992dad`, the K2 counts file written by a program for path checks only, never for counts). The mutation programs' `os.replace` of their own marker files inside scratch trees overwrites the previous `.done` marker (as round 1's program does).
- One hook refusal: a `git -C $S/sg checkout` with the path in a variable was refused by `pretooluse_no_cd.sh`; re-run with the absolute path typed (a scratch clone in Tuesday's tree). No `cd` was typed; nothing was deleted (no `rm`); no clock typed into a Stamp slot; no message to any human.

Report closed at Fri 27 Nov 2026 11:04:39 AEDT (`date`, printed before this file was written; the kit's last edit precedes it).
