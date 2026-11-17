STARTABLE: YES, after Tuesday's stamp. The launch may be now (the seat waits for the Build, Step 3b) or after the Build reads success. One thing to know first: the merged HISTORY.md already carries a numbering slip (it says C-301 and section 99 for the pull request 216 entry, which is C-300 and section 98); the kit handles it by correction, not edit (Q1).

# B1684 drafter report (SEAT-R264, NexusAI records: pull request 218 and 217), drafted Wed 18 Nov 2026 (`date` first read 03:15:31, last read 03:27:36 AEDT)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1684_SEAT-R264_nexusai-records-218.md` (179 lines, 74524 bytes, 0 non-printable, 0 non-ASCII, 9 four-underscore lines: eight slots plus the last line). Sidecar `...md.measured` (108 lines: 90 claim lines, 18 EXTRA/PTR/SHA/SCAN/TM lines). `stamp_check.py`: **90 claims, 90 measured, 0 not measured, rc 0**. Work folder `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s287/d1684/` (texts.py is the source of the 15 Jira strings; kit_template.md renders the kit; jira_get.py is the GET-only reader).

## BLUF
- Four comments (RD-1002, RD-734, RD-730, RD-729), up to three moves to Testing (RD-1002, RD-734, RD-730 by slot MOVE), RD-729 comment only (A-F1 only; stays open). **No create.** One new section (99 expected) with one entry (C-301 expected). One optional history branch `records/b1684-history`.
- Pull request 217 was NOT recorded (CLARIFICATIONS 0 lines, HISTORY at the merge commit 0 lines): the new entry and the new history entry record it (merge f8a6232a, 02:02 AEDT, HISTORY.md +18).
- The review's one finding (G2, GO WITH FINDINGS) is an Advisory on the H1 margin: entry plus the RD-729 comment, **no ticket** (D1).
- The B1679 deviations are folded in (kit section "What the previous pass learned").

## Facts re-measured with instruments (all gh -X GET under the NexusAI GH_CONFIG_DIR; Jira GET only via jira_get.py)
- #218: merged true, merged_at 2026-11-17T16:12:54Z = 03:12:54 AEDT, merge 2de5e84c799e32232d65cd759085d728d7141583, parents f8a6232a + 7bc1c5d2, 5 commits (9d88113e RD-1002, 84dcd6a8 RD-734, 111d7b60 RD-730, 6e9f1c58 RD-729, 7bc1c5d2 counts), 5 paths +63 -21; **each commit touches exactly one path** (commits API); author = committer on all 5.
- **The merge tree is NOT the head tree** (e09d1fe2 vs 77560c48): `compare 7bc1c5d2...2de5e84c` lists HISTORY.md only (the #217 file). The brief said head-pinned; the kit says "differs by HISTORY.md only" and never "equal" (the B1679 wording would have been false here).
- Checks at 03:15: 4 success, 2 skipped (Deploy demo run 44123184953), 2 in progress (Build job 134179784230 of run 44123184892; Analyze javascript-typescript). Re-read 03:21: Build still in_progress.
- Code scanning on main: 22 open / 222 fixed / 7 dismissed (142 143 144 147 148 149 150); none created after the merge (newest created 2026-11-08); all open instances still on f8a6232a; the javascript-typescript analysis of 2de5e84c is not yet written (python 2187805837 and actions 2187803877 are).
- Jira: RD-1002, RD-734, RD-730, RD-729 To Do, no comment, transition 31 In Review -> Testing offered on each; 999 issues, highest RD-1003; marker searches for the four new markers 0 (control LAND-216-995-18NOV -> RD-995, ACTIONAUTH-216-18NOV -> RD-1003).
- CLARIFICATIONS.md: 743458 bytes, 3039 lines, sha256 1f4084a1...b68b2, section 98 line 3032, C-300 line 3034, ends with newline; `## 99.` and `C-301` 0 lines. HISTORY.md at the merge commit: 10164 lines, last heading line 10148, ends with newline.
- **Slip found:** HISTORY.md lines 10148, 10150, 10160 say C-301 / section 99 for the #216 entry (real: C-300 / 98). Cause (derived from B1679's Step 7 text, "highest + 1" after the append). Fix in this kit: numbers frozen at Step 6 into `raw/entry-numbers.txt`, checked by program before Step 7, with a planted-mismatch control.
- Identity: sha256 prefix of user.email is be76c2c1baf03ec1 **only when the trailing newline is stripped** (with it: 4123cf83d812afdc). B1679's kit did not say so; this kit does, so a seat does not read a mismatch.
- Real Build log line (previous job): `VERDICT: PASS` + em dash bytes e2 80 94 + ` 5868/5868 tests passed across 377 suites (jest exit 0)`; the kit tells the seat to match the ASCII prefix and parse figures by regex, expecting 5870/5870/377.
- Panes 03:18: %0 tuesday, %1 fleet-monitor, %288 Datasec/NexusAI-N148 (the sibling), four unnamed. Port: none. Disk 1091 GiB free.
- Pointers: 27 fragments at the merge commit, each on exactly one line (ptr.py assert), plus 2 at the base.
- Jira text scan: 15 strings, 0 hits raw and filled; controls fire. sha prefixes in the kit labels.

## Partition (stated)
Sibling N148 (code, RD-689): owns `backend/server.js`, `backend/services/schedulers/healthSweeperScheduler.js`, `__tests__/rd385-shipped-root-markdown-identifiers.test.js` and the counts file only if its verify refuses on counts; its own branch and clone; **no Jira, no HISTORY.md, no CLARIFICATIONS.md** (its kit says so). By B1679's REFUSE-6 property (another pane whose kit WRITES Jira RD / CLARIFICATIONS.md / a ref or config of 2_Project_Files) it is not a hit. This kit owns Jira RD (4 comments, up to 3 moves), one CLARIFICATIONS section, `.tools/b1684`, and only HISTORY.md on `records/b1684-history`. Every read is at the merge commit 2de5e84c, never main's tip.

## Step input table (MEASURED LITERALS rule 4)
| Step | Inputs | Exists at / produced by |
|---|---|---|
| 0 | kit, df, project folder | BASE |
| 1 | repo identity, transport key, logs dir | BASE; Step 0 |
| 2 | `.tools/b1684` | Step 0 |
| 3 | helpers, `.env` names, CLARIFICATIONS.md | Step 2; BASE |
| 3b | wait1684, run 44123184892, merge sha | Step 2; kit |
| 4 | texts (kit), facts after the wait, snap_before | kit; 3b; 3 (no key fill-in: no create) |
| 5 | final dry payloads | Step 4 |
| 6 | read-backs, snap_after, before-copy | 5; 3 |
| 7 | identity prefix, origin/main, `raw/entry-numbers.txt` | 1; 6 |

## D-decisions
- D1 No ticket for the H1 margin advisory: nothing failed, remedy is one digit (1800 or 2000, the review's words), RD-729 stays open and carries it. Searches: `H1_MARGIN_MS` 0, `rd648-harness-boot-residuals` 0, `flake` with `H1` 0 tickets. No create slot exists in the kit at all.
- D2 MOVE slot is a list `1002 734 730` (subset allowed), RD-729 never moved.
- D3 RD-729 has its own text with no `<<OUTCOME>>` (fixed "stays open" wording).
- D4 Two stale or off facts are said plainly in Jira texts: RD-1002's own "counts stay at 5867" clause (main was 5868; now 5870 by RD-730's two cells), and RD-734's sums (phase bounds 148000 -> 158000, budget 158000 -> 168000 with the 10000 margin; the all-bounds path is read from sums, not run).
- D5 Decimals avoided in Jira texts (3150 ms, not seconds with a point); the handover table test path is not written in Jira (it holds `gate`), only in entries and history.
- D6 Per ticket clauses are listed in full (no notation alternatives), fixing B1679 Deviation 2.
- D7 Hard stop proposed 05:45 AEDT (wait limit 04:45; B1679's Build took 66 minutes, so expect about 04:00 to 04:20).
- D8 Branch name `records/b1684-history`.

## Questions for Tuesday (each with the default written)
- Q1 The HISTORY.md C-301/section 99 slip: default = leave the earlier text, correct in the new CLARIFICATIONS entry and the new history entry (both carry a plain correction sentence). Alternative: a separate fix in the new history entry's diff (edit lines 10148/10150/10160); I advise against editing an append-only file.
- Q2 A ticket for the H1 flake-risk advisory: default NO (entry + RD-729 comment). Say CREATE and a small follow-on kit is needed; this kit has no create text.
- Q3 Launch timing: default now (the seat waits for the Build via wait1684.py, Step 3b); alternative: launch after the Build reads success.
- Q4 Hard stop slot: default 05:45 AEDT.
- Q5 Slots: JIRA WRITE, MOVE `1002 734 730`, RECORDS WRITE, HISTORY WRITE (drafter's recommendation; the three moves rest on "code change goes to Testing" and the review's acceptance readings, RD-734's all-bounds path being the one acceptance read from sums).

## UNMEASURED
The hosted Build conclusion and its VERDICT line for 2de5e84c; the javascript-typescript analysis of the merge commit; whether the repo-local identity still prefixes be76c2c1 at launch; the exact wording of the Jira `GET transitions` after the Build; Q-answers; hosted H1 behaviour under load.

## Outside-the-fences disclosure
Read: the DRAFTER_RULES, the B1679 kit and sidecar and STATUS, the B1680 STATUS, the B1681 verdict folder, the B1683 kit (partition lines only, as a readable claim), CLARIFICATIONS.md and the model-routing file (read-only). GitHub GETs only (including one hosted job-log GET of the PREVIOUS Build job 134058565187 to copy the real VERDICT line; GitHub API, not an app host). `git ls-remote` read twice with the one-command transport. The project `.env` was read in-process by my scratch `jira_get.py` (no token printed). One Bash call was refused by the no-rm hook (an attempt to remove my own sidecar); nothing deleted, and the sidecar was overwritten by my generator instead. Never wrote in the NexusAI folder; wrote only the kit, its sidecar, this report and the scratch folder.
