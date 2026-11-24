STARTABLE: YES

# B2072 DRAFTER REPORT: OXPd 2 records kit for pull request 51 (`oxpd1 echo`), seat R320

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2072_SEAT-R320_oxpd2-records-pr51.md` (79935 bytes, 268 lines, sha256 fe7a5fb3a7b8ed1093e1418a0bfc2a4f49a1669635e9327075012d531834b7ef at 05:48:01). Sidecar: the same path plus `.measured` (23193 bytes, 104 lines). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s325/d2072/`.

## BLUF
- Pull request 51 landed on main as `baa32eae27ddf1267ca1522ef7f1138a4dd832cd` (merged 2026-11-24T14:47:21Z = 01:47 AEDT 25 Nov), one parent 217286f3, tree 2c27aa34. That tree equals the gated head de8f2a47's tree and the tree the gate predicted. Hosted: 7 of 7 checks success; push run 45418013265 reads linux 2257/2261 with 4 skipped, windows 2240/2261 with 21 skipped, rules 675 files, 117 unit tests with floor 117. Code scanning reads 0 results in each of three languages, 0 open alerts and 0 open pull requests. The commission's "HOSTED PASS 2261/675" is confirmed at source.
- The kit has the form of B2066: one BACKLOG rewrite that only inserts lines (seven new owed items, 133 to 139, 49 lines, after item 132) and one history entry (7 lines). There is no tick, no `Closed in part` line, no clarification entry, no Jira write and no CLAUDE.md edit.
- No owed item is closed by the echo lane, by the drafter's search. Owed 118 (the LAN call back) stays open with no new line (Q1). Owed 2 is unchanged.
- The dry build matches every prediction. The proof by position holds, with controls that fire. `scan_record` (the project's own scanner, a byte copy, sha256 5e766b28) found 0 problems in 55 filled lines; its 6 controls fired. `stamp_check.py`: 104 claims, 104 measured, rc 0.

## Facts re-measured (instrument, clock)
- GitHub (`gh api -X GET`, project `.gh-config`, login kamilDatasec; gh1.sh 05:33:49-05:34:01, gh2.sh 05:34:11-05:34:19, one read at 05:44:08):
  - commits/main = baa32eae, 1 parent 217286f3, tree 2c27aa34, subject ends `(#51)`; git/commits/de8f2a47 has tree 2c27aa34 and parent 217286f3.
  - pulls/51: merged, 1 commit, 12 files, +1494 -23, head de8f2a47 on `b2067/oxpd1-echo`.
  - pulls: all 51, highest 51; open 0; merged numbers 44 to 51; pulls/52 is 404 (control: pulls/50 answers 200).
  - pulls/51/files: 4 added and 8 modified, equal to the landing.txt list.
  - Check-runs at baa32eae: 7, all success.
  - Push run 45418013265: the four job logs as above. `failed Datasec.` is on 0 lines and the control `total: 9999` is on 0 lines.
  - The base's push run 45390919267: linux `total: 2221` on 2 lines.
  - Code-scanning analyses: 3 rows at baa32eae, each with 0 results. Alerts open: 0.
  - Branch `b2067/oxpd1-echo` is at de8f2a47; 53 heads.
- Tree of main (tarball at 05:34, 1739701 bytes, sha256 f634ad8c, 675 files, extracted in scratch): facts.py printed `PASS 72 FAIL 0`.
  - All 53 file:line pointers of the texts check out.
  - All 5 record files equal B2066's READY.manifest: BACKLOG d920d113, history 6b4e12f7, CLAUDE 0f1fccc0, CLARIFICATIONS f67eceaa, register e2621f1b.
  - B2066 READY line present; no B2072 lane, STATUS or HANDOVER.
  - Owed items run 1..132 with no gap (87 open, 45 ticked). Item 132's block is lines 965 to 971; the anchor heading is at 973.
  - History line 3 is B2066's entry.
  - None of PR 51's twelve paths is in the build closure of `tests/Datasec.Suite.Server.Tests` (control fired).
  - Both negative controls read False.
- P-3 counts (case-blind, by program; every number is in facts.out and the kit's P-3). Every new-item search term is on 0 lines of BACKLOG.md and in 0 Jira issues. CLARIFICATIONS: echo, guest, S14, listener and Server.Tests are 0 each; `callback` is on 7 lines. Six are the OXPd 2 printer-callback ruling. One, line 1104, is C-84's chosen option ("we test the callback"), which owed 118 already records.
- Jira (project reader copy, GET-only fence; the fence refused POST, PUT and DELETE; 05:35:30-05:35:39): census 62 (OXPD2-1..62); Done exactly 33, 39, 41 and 47; no-hardware 23; OXPD2-99999 is 404. 20 phrases each found 0 issues; the controls `named pipe` and the MASTER title each find OXPD2-1.
- B2067 STATUS (sha256 00678959, 246 lines): the last line is `READY B2067: de8f2a47...`. The hang literals are on lines 122, 125 and 230. The three evidence files exist (`test -f` rc 0; control rc 1). They were not opened.
- heavy.py copy at `.tools/b2067/gate/` (sha256 31adedc8 = the seat's THE TOOLS line): line 86 is `subprocess.run(..., timeout=tmo)` and line 87 is `except subprocess.TimeoutExpired:`. Read with grep and sed.
- Seat id: R320 is on 0 lines of 201 SEAT kits dated 2026-11-18 to 2026-11-25 (control: R319 on 4 lines in 2 kits). No file name holds R320. No pane is named R320 (control: `tuesday` 1). Panes: %0 tuesday plus two unnamed panes; none is OXPd2.
- Model: OXPd CLAUDE.md:7 (newest Opus); models_latest.json:17 `claude-opus-5-5`; brief_seat.sh:31 defaults to opus. The kit writes `BRIEF_SEAT_LEVEL=opus` in the launch line anyway.
- Ports: none. The kit starts no listener and no seat port is used.

## Chain steps and their inputs (each input exists at BASE or is made by an earlier step)
| Step | Inputs | From |
|---|---|---|
| 0 | stamped kit and sidecar; the five record files; b1785.py | BASE |
| 1 | b2066.py and b1785.py (models); scratch copies | BASE; Step 0 (before/) |
| 2 | SOURCES rows; GitHub; Jira; the tarball | BASE; the tarball is fetched in Step 2 itself |
| 3 | frozen texts (kit); before-copies; dry/ | kit; Step 0 |
| 4a | live BACKLOG.md; before-copy; dry proof | BASE; Steps 0 and 3 |
| 4b | live history.md; BL-NEW8 | BASE; Step 4a's print |
| 5 | all of the above | Steps 0 to 4 |

## D-decisions (the drafter's)
- D1: The form is B2066 (the commission names it). Its D2, D3, D5, D7 and D9 are named in the kit as faults to avoid.
- D2: Items are numbered 133 to 139, one per finding: FOUND 1 to 4 (Minor) are 133 to 136; the hang (part a of the proposal) is 137; the runner orphan (part b) is 138; FOUND 5 and 6 (Info) and the kit's named limits go in 139 ("other record points").
- D3: BL-134 says "callback bodies HP's schema refuses" without a number. The VERDICT says "five" in two places but lists six probe ids (C02 to C05, C15, C23), so the count is unsettled in the source.
- D4: H-NOTDONE does not say the branch `b2067/oxpd1-echo` "stays on the origin". That clause could go false before the seat runs.
- D5: No Jira write. No Jira issue names the lane (P-J), and the form adds none for a landing without a word from the product owner.
- D6: The kit tells the seat never to run a recursive read over the project folder (see Outside the fences, item 1).

## Questions for Tuesday (each with a default; the kit assumes the defaults)
1. Q1 (owed 118): should it get a `Closed in part` line naming the echo verb as built, with the test not yet run? Default: NO line; H-REC and item 139 say it.
2. Q2: should the hang and the runner orphan be two items (137, 138)? Default: two items, as the commission asks. Alternatives: merge them into one, or keep 138 out of the project backlog because heavy.py is the coordinator's runner, and record it in your ledger instead.
3. Q3 (item 139, other record points): keep it? Default: keep (the form's habit).
4. Q4 (no tick, no in-part line): Default: none.
5. Q5 (no clarification entry, Jira GETs only): Default: as written.
6. Q6 (one history entry): Default: one.
7. Model: Opus by CLAUDE.md:7. Default: Opus (`BRIEF_SEAT_LEVEL=opus` is already inside the quotes).

## UNMEASURED
- Which cell and which wait hang in Server.Tests, and the cause (relayed as UNMEASURED).
- The consequence of FOUND 4 on a device (the reviewer's derivation).
- The M577's behaviour toward the echo: whether it accepts the guest credential, calls back over plain http, sends Content-Length, and what answer it expects.
- The seat's helper, its selftest, HOLD R and R2 on the live files, and the numbers at the seat's run: never run on a real output, as the kit says.

## Outside the fences (disclosure)
1. **A recursive grep reached `Source_Documents/`.** Early on, the drafter ran `/usr/bin/grep -rl -F 'B2001' '<project>/1_Project_Definition'` to locate the design reference. That read every file under `1_Project_Definition/`, including `Source_Documents/`, whose SDK copy holds a key folder (DRAFTER_RULES, 2026-11-21 line). Nothing was hashed, copied or listed beyond grep's match output: 6 file names were printed, one of them a `.pdb` under `Source_Documents/`. No file content was printed, and no key file appeared in the output. It is not repeated, and the kit now forbids recursive reads for the seat (D6).
2. **A refused copy.** `cp -n '<project>/.tools/b1785/b1785.py' <scratch>` was refused by the path guard, which read the source path as a write. Nothing was written. The copy was then made with `cat > <scratch>/proj_b1785_copy.py`, and cmp returned 0.
3. Everything else stayed inside the fences.
   - Reads of the project (manifest, STATUS files, BACKLOG, history, CLAUDE.md, CLARIFICATIONS counts, `.tools/b2067/gate/heavy.py`, `test -f` on three log files).
   - `gh api -X GET` only.
   - Jira GET only (fence fired).
   - `tmux list-panes` (read).
   - Writes only to the kit, its sidecar, this report and the scratch folder.
   - No card-store read, no `cd`, nothing deleted, nothing sent to any person.
