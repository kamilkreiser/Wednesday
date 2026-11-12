# Drafter notes: Seat B 164th brief (drafted 2026-11-13 about 02:40 to 03:0x AEDT)

Output: `brief_B164.md` (46,994 bytes; commission said ~45 KB; STAMP block blank, no SELF-CHECK line). Nothing written outside this folder except the session scratchpad (`rc164` scratch clone, `moved_*`, `own_*`, `body_*`, `census164.json`).

## B 163rd's measured meter readings (kit meter, 1M window; from its wrap mail and HANDOVER)
| point | reading | delta |
|---|---|---|
| first read | 15.2 | |
| PLAN | 25.2 | +10.0 |
| SET-UP CLOSED | 32.6 | +7.4 |
| READY 2218 built (product, Jest suite on merged tree, pair proof vs 2099, 12 KB READY) | 43.8 | +11.2 |
| MERGED 2218 sent (r) | 49.7 | +5.9 |
| READY 2178 built (title only, no suite, no fragment pair) | 55.5 | r + 5.8 |
| MERGED 2178 sent | 57.8 | r + 8.1 (READY + 2.3) |
| wrap start | 59.9 | +2.1 |
Thirteen first-MERGED readings now: previous twelve sum 655.2, plus 49.7 = 704.9, mean 54.2; three of thirteen at or under 50 (49.2, 48.7, 49.7).

## Proposed second-row line for 2207 after 2208 (for Wednesday to rule at the stamp)
**r at or under 50.0: 2207 DIRECTLY; above 50.0 to 54: STATUS first; above 54: WRAP naming 2207; a 2207 READY above 58 is a STATUS then WRAP.** Why: B 163rd's 52 line worked because 2178 cost r + 5.8 to its READY (57.8 under the 58 tripwire). 2207 is dearer than 2178 (ten config files to read, a fragment pair, a tsc leg if it costs no new install) so priced r + 7 to r + 7.5 to its READY and about r + 10 to its MERGED send; at r = 50.0 that is READY about 57 to 57.5 and MERGED about 60 (PACE); at 52 the READY would be 59 to 59.5, over the tripwire. First-row estimate (not measured): PLAN 25, SET-UP 32 to 37, READY 2208 43 to 48 (2218 cost +11.2 with a Jest suite and a pair proof; 2208 swaps these for two installs, a build and audit:locks, no pair proof), MERGED 2208 sent 49 to 54, so a STATUS is the likelier outcome. The number is the drafter's reading from shapes, not a measurement.

## Findings that DISAGREE with the commission or earlier briefs
1. **Check-runs wording.** The commission and B 163rd's brief say 2208's head shows a 12th failing run named `Standalone locks pass clean-room npm ci` (a name the other heads lack). Measured (`gh api commits/<head>/check-runs`, failing names counted with `sort | uniq -c`): 2207's head (19 runs, 11 failure) ALREADY has that name failing once; 2208's head (20 runs, 12 failure) has it TWICE (completed 03:50:12Z and 03:50:13Z, github-actions). The extra run is a second run of a name that already fails at 2207, not a new name. Why it runs twice is unmeasured. The brief says so (BLUF 11).
2. **KS-961.** Earlier briefs cite KS-961 as the Actions billing block (from Wednesday's pickup; B 163rd's drafter could not read it). The drafter's Linear read now returns KS-961 = "The aggregate workspace suite never runs on a PR — wire it advisory (Kam: wire-nonblocking), and it is RED on develop today", state In Review. That is not a billing block. The brief tells the seat NOT to cite KS-961 as the cause; the billing attribution is unconfirmed (the ruling Kam made about billing may live in another ticket or a note; not found).
3. **Three tools differ from v3, not two.** B 163rd's HANDOVER says two (merged_build, run_merge). Hashing each of the 31 manifest lines against REC163 `tools/` now: `merge_b163.py` (the hygiene edit), `merged_build_b163.py`, `run_merge_b163.sh` differ (28 of 31 equal). The hygiene edit came after the v3 manifest.
4. **KIT finding root cause read.** The swallow is in `tools/ghx_b163.sh` (`gh "$@" 2>&1 | sed`, stderr folded into stdout), captured by `run_merge_b163.sh` line 50 into `TITLE_JSON=$(...)`; line 51 on non-zero rc prints only `STOP: title read failed` (exit 3); `do_merge_b163.sh` line 14 makes it exit 11. The brief gives the counted edit (print `$TITLE_JSON` on that branch) and the same-GO rerun rule. The transient itself is unmeasured.
5. KS-278 appears in 2207's body (and gate 328's text) but no KS-278 issue exists in the KS team at Linear (empty result); the brief does not name it.

## Measured facts (all in the brief with instruments)
- develop a997d35d74b1 has ONE parent 6a32735db216 and tree 9e402b145674 = B 163rd's expected 2178 tree. All heads equal Wednesday's 02:39:43 read (my ls-remote at 02:40:37).
- Expected trees on develop a997d35d74b1: 2208 `f8505e1fd9c6` (rc 0 both orders; equals B 163rd's synthetic chain value after 2218, so 2178 did not disturb it); 2207 `f5934b542651` (rc 0 both orders). Planted develop-side conflicts: 2208 package.json line 38 rc 1/1, control line 10 rc 0/0; 2207 billing tsconfig line 18 rc 1/1, control line 5 rc 0/0 (my first plant function read rc through a pipe in a subshell and reported 0/0 for everything; I caught it from the implausible result and redid it reading rc from the merge-tree call itself; only the second run's figures are quoted).
- Gate positive controls reproduce: 2208 head vs 581296f039b4 -> e7ed9cd4b587; 2207 head vs b7137aa97c79 -> d390c397ee1d. Chain control: 2207 after a synthetic 2208 squash `e7e94f112469` (both orders), 2208 after synthetic 2207 the same tree.
- Moved paths and first-parent commits: 2208 66 and 16; 2207 73 and 17; overlaps 0 of 5 and 0 of 12; the two rows share no path.
- Fragment file counts (ls-tree): develop 361/356; merge tree of either row 362/357; both 363/358 by arithmetic. Tool counts DERIVED from B 163rd's measured 241 (develop cf6a) and 242 (2218's tree): develop a997 242, each merge tree 243, both 244. The tool was not run.
- 97 open PRs, max 32 files; census: only PRs 2208 and 2207 themselves on their own paths (control PR 2125 fires). Only other tsconfig-touching open PR is 2191 (originate test config, outside the ten). PR 2099, 2052, 2200, 2201, 2184 unmoved.
- Bodies: 2208 6,781 bytes, 2207 6,312 bytes, neither has a notes heading; closing-word regex 0 hits each. KS states: KS-2179, KS-2177, KS-1398, KS-2136, KS-2173, KS-2149, KS-1959, KS-2060 In Progress.
- GitHub: mergeStateStatus UNSTABLE, mergeable MERGEABLE, review decision empty on 2208, 2207, 2184; REST mergeable_state unknown; quota 4,976 of 5,000.
- History ordinals: 162nd 2, 163rd 1, 164th 0 (1,126 headings; positive control).

## Could not measure
- No suite, install, build, tsc, audit:locks or docs-fragments tool ran (the scratch clone has no checkout; nothing was installed). Every build, test and tsc figure in the brief is a gate's figure, labelled so.
- PR-side planted conflicts for 2208 and 2207 (develop-side only).
- Cause of UNSTABLE, of the 11/12 failing check-runs, and of 2208's doubled Standalone-locks run.
- The inbox after 02:4x (no GO or gate round for 2099, 2052, 2200, 2201, 2184 was checked), the launcher preflight, pane owners, `git worktree list`, re-key token counts, the usage gauge.
- 2200 and 2201 heads were read by ls-remote only (their objects are not in the scratch clone, so no merge-tree for them; they are ADDENDUM-only).
- Whether the commission's Wednesday-side card text for KS-1398 matches (I read the Linear title only).

## Slips
- First plant function misread rc (above), redone. Two hook refusals (a `=====` echo separator; an unquoted `$G` git prefix in zsh), redone under bash heredocs. One Python cut script raised ValueError on a stale anchor before writing anything (no partial write), redone. The brief ran 51,000 bytes in the first draft and was trimmed to 46,994 by counted cuts (Spark lines, duplicated gate figures, a PROVENANCE line for a key no longer named).
- Nothing written under /Volumes/DevMASTER/!CODING/ ; the only git verbs there were `ls-remote` through REC163's clone.
