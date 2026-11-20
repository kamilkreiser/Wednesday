STARTABLE: YES - the kit is whole, `stamp_check.py` exits 0 with the slots unfilled (104 claims, 104 measured), and every fact it freezes was re-measured at source; three points need Tuesday's eye before the stamp (Q1, Q2, Q3) and one commission fact is corrected (code scanning now HAS analyses).

# B1785 DRAFTER REPORT | OXPd 2 records pass for pull request 1 (SEAT-R286)
Drafted 2026-11-20 by the read-only drafter (Fable). Clocks by `date`: first read 17:07:20 AEDT, last source read 17:14:41, re-reads 17:26:11 to 17:26:16, kit and sidecar last built 17:28:14.

## Files written (3, plus scratch)
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1785_SEAT-R286_oxpd2-records-pr1.md` (436 lines, 107491 bytes, ASCII, 8 four-underscore lines, sha256 04f68921...).
- Sidecar: the same path plus `.measured` (105 lines: 1 head line and 104 claim lines).
- This report: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1785_DRAFTER-REPORT.md`.
- Scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s298/d1785/`: `texts.py` (every frozen text), `kit_template.md`, `build_kit.py` (builds the kit, computes every sha256, length and line number, runs the scan; writes by temp file and `os.replace`), `sidecar.py`, `jira_get.py` (GET only), `jira_census.py`, `jira_search.py`, `loglines.py`, the 9 hosted job logs under `logs/`, six files of main under `src_main/`, the Jira texts `jira_OXPD2-*.txt`. A re-cut is: edit `texts.py` or the template, run `build_kit.py`, then `sidecar.py`, then `stamp_check.py`.

## BLUF
1. Pull request 1 is merged as the commission says; every number of the commission's first bullet re-read true (main 7bf37526, one parent 7e1a01cf, tree 23d8e25f equal to the head's, 8 check rows, runs 44684936169 and 44685196570 success with 4 jobs each, `25 of 25`, 72 objects, 144 copies, `5 commits scanned.`, the third refspec, 72 against 71).
2. **Not in the commission: code scanning ran by itself after the merge.** Default setup now lists `csharp` and `python` (not `actions`), 2 analyses on main at 7bf37526 with 0 results each, 0 alerts, a sixth run 44685211085 (event dynamic). The kit records exactly that and leaves the reading of E0.4's CodeQL clause to Tuesday.
3. The project folder is not a git repository, so the kit has no records branch, commit or land: three files are rewritten once each by the temp-file rule with before-copies and a line-by-line proof.
4. `CLARIFICATIONS.md` moved three times while I drafted (C-52, C-53, C-54 appended at about 17:08, 17:17 and after 17:26). The kit uses C-47 to C-51 only; their six quoted strings are cut by program and each is found once in the file as it stood at the last build.

## Facts re-measured (instrument -> reading)
- `gh api -X GET pulls/1` -> closed, merged true, merged_at 2026-11-20T06:04:10Z, 3 commits, 25 files, +1691 -0; `mergeable_state` NOW prints `unknown` (so "clean before the merge" is RELAYED from Tuesday, and the kit says so).
- `commits/main` -> 7bf375268b9975ac9ece66579f7471ba7dbab11d, 1 parent, tree 23d8e25f...; `git/commits/6e2629bc` -> the same tree. The squash message equals `squash-subject-1.txt` plus `squash-body.txt` (by program).
- `git/matching-refs/` -> 3 refs (main, the lane branch at 6e2629bc, `refs/pull/1/head` at 6e2629bc); `delete_branch_on_merge` false; compare main...lane: diverged, ahead 3, behind 1.
- `actions/runs` -> 6 runs; check runs: 8 on the head (all success, github-actions), 7 on main's commit.
- The 8 job logs of runs 44684936169 and 44685196570 and the `secret-scan` log of 44680821033, by GET with `--allow-escape-sequences`, colour codes stripped, counted by `loglines.py`: every quoted line and count in THE LANDING.
- `rules/branches/main`, `rulesets/24139430` (repository path) -> 4 rules, required list EMPTY, active, 0 bypass actors; `branches/main/protection` -> not protected. (`orgs/datasecau/rulesets/...` answers 404: the login lacks the organisation scope; not needed.)
- `code-scanning/default-setup`, `analyses`, `alerts`, `languages`, `actions/workflows` -> as in THE CODE SCANNING READ.
- Jira (my own GET-only reader, the project's `.env` read by name in-process): 19 issues, 0 Done; OXPD2-1 6 comments, OXPD2-2 1 comment; OXPD2-8 Task id 10030 under OXPD2-3, Backlog; 58 phrase and marker searches; label searches.
- The three record files: sha256, line counts, 0 non-ASCII bytes, 18 pointer rows; a dry simulation of PART 3 from the live files gives BACKLOG 131 -> 215 lines, SETUP_RUNBOOK 100 -> 101, history 33 -> 44.
- Local: the checkout sits on the lane branch at 6e2629bc with local main 7e1a01cf and an empty porcelain (read verbs only); the launcher's sha256 and four word counts; `tmux list-panes -a` 7 lines, 0 with OXPd; no `.tools/b1785`, no B1785 file in the project's Briefs.

## Inputs of each step (each exists at base or is made by an earlier step)
| Step | Needs | From |
|---|---|---|
| 0 | the stamped kit and sidecar; the three record files | Tuesday's stamp; base |
| 1 | python3; `.tools/b1785/` | base; Step 0 |
| 2 | THE SOURCES (20 files), `gh` login, `.env`, the helpers | base; Step 1 |
| 3 | the frozen texts of the Step-0 copy; check E; `before/` copies | Step 0; Step 2 |
| 4 | the dry run's payloads; `snap_before.json`; slots JIRA and CREATE | Step 3; Step 2; stamp |
| 5 | the keys and comment ids Step 4 returned; `before/` copies; slot RECORDS | Step 4; Step 0; stamp |
| 6 | everything above | Steps 0 to 5 |

## Recommended stamp-slot values
- JIRA: `WRITE`. CREATE: `1,2,3,4,5`. RECORDS: `WRITE`.
- BASE (facts I measured, for Tuesday to re-read, not to copy as its own reads): main 7bf375268b9975ac9ece66579f7471ba7dbab11d; 7 check rows on it, the four `ci` jobs success; default setup languages csharp and python, 2 analyses with 0 results, 0 alerts; open pull requests 0; no `Datasec/OXPd2-` pane; sha256 of BACKLOG.md e7b38559..., SETUP_RUNBOOK.md 53af1d1e..., history.md 98fa2988...; highest clarification entry C-54 at 17:28. The BASE slot must ALSO say whether Tuesday has asked the product owner for the three HP items (Q2).
- Hard stop: Step-0 clock plus 90 minutes; the pass has at most 7 Jira writes and 3 file replacements and no CI poll.
- LAUNCH WINDOW: no dependency on any other pane; launch only while no OXPd pane writes Jira OXPD2 or the three record files.

## The searches run for each create (all `project = OXPD2 AND ( text ~ "\"<phrase>\"" )`, 17:12 AEDT, status 200)
- NEW 1 (README wording): `branches and tags only` 0, `merge commit` 0, `refspec` 0.
- NEW 2 (message-scan script): `squash message` 0, `commit message` 0, `scan the squash` 0, `flagged message` 0, `ignore mechanism` 0.
- NEW 3 (second scan's own checks): `objectsize` 0, `planted control` 0, `neutral name` 0, `one git process` 0, `planted repository` 0, `secret-scan` 1 (OXPD2-8).
- NEW 4 (rules): `flow mapping` 0, `quoted key` 0, `NUL byte` 0, `BASH_ENV` 0, `filter=lfs` 0, `Git LFS` 0, `repo_rules` 0, `line rules` 0, `fingerprint` 1 (OXPD2-8).
- NEW 5 (release guard): `release mode` 0, `single-file` 0, `publish shape` 0, `release_guard` 1, `release guard` 1, `development CA` 1 (each OXPD2-8), `deny-list` 1 (OXPD2-15, the logging deny-list).
- Controls: `CI/CD skeleton` -> OXPD2-8; `zzqxnonexist` -> 0; three existing markers each find their key; the seven new markers 0 each; `labels = b1785` 0 (control `b1764` 17).
- NOT run: the five whole-summary searches (the kit has the seat run each before its create).
- No true duplicate was found, so no create became a comment. OXPD2-8 names the scan, the guard and the fingerprint as the package itself; none of its text holds a follow-up.

## D-decisions (mine as drafter; each is Tuesday's to keep or cut)
- D1. Five tickets, grouped by the file a build would touch, not one per finding (three rounds leave about twenty open points): 1 README; 2 a script in build/; 3 the `secret-scan` step; 4 the rules and the fingerprint test; 5 the release guard. Every open point has a backlog line (new owed lines 19 to 30, or an existing line); seven of the twelve new lines have no ticket because they are the coordinator's or an owner's (24 to 30).
- D2. Each new ticket is a Task under Epic OXPD2-3 with labels `no-hardware`, `wp0-3`, `b1785`, in this board's own five-paragraph form, and says that no F row is named (as OXPD2-8 does).
- D3. The records seat corrects the two inexact phrases in `BACKLOG.md` line 99 and `SETUP_RUNBOOK.md` line 87 itself (they are record files, and the fetch line is now MEASURED); only the README needs a build (NEW 1).
- D4. The standing landing rule goes into the runbook's owed line 4 (line 75), so the owed numbering stays aligned with the backlog; one runbook line lists the twelve new backlog items.
- D5. Record lines keep this project's own words (seat, lane, the coordinator, a STATUS path); the Jira texts are scanned more strictly.
- D6. `READY B1785: <40 hex>` is the start of the sha256 of a manifest the seat writes (there is no commit to name).
- D7. OXPD2-8 gets no comment and no move.

## Q-questions for Tuesday (each with a default)
- Q1. Is one ticket per build file (five) right, or does Tuesday want one per finding? Default: five, as drafted.
- Q2. The OXPD2-2 comment says the coordinator has asked the product owner for three things (the simulator image, its guide, the debug bridge service key). That is the commission's own statement; C-50 itself says only that he will fetch what he is told. Default: the kit drops that clause by program unless the BASE slot confirms it.
- Q3. C-52 to C-54 arrived during drafting and touch the same checklist item (the Windows PC). Default: not used (the commission names C-47 to C-51); Tuesday may want a re-cut that adds them to the OXPD2-2 comment.
- Q4. Should OXPD2-8 carry one note of the landing? Default: no (not commissioned).
- Q5. Does Tuesday read E0.4's CodeQL clause as met now? Default: the records say it is Tuesday's to read and state the facts.

## Corrections to this commission
1. "Code scanning: no analysis exists" is no longer true: 2 analyses on main, 0 results each; the workflow language is not analysed.
2. "The exact click from round 1's CODEQL-FIRST-PR.md" for required checks is not there: that file holds the steps for a BLOCKED first merge (which did not happen). The options for required checks are in round 1's VERDICT finding 2 and FOR-RECORDS section 3 line 2, and no source holds a click path. The kit hands over the facts and the options and marks the click UNMEASURED.
3. "Item 2 (the Windows machine)" of OXPD2-2: on the ticket the PC is item 1 (a numbered list of 16; its own comment says item 1); item 2 is the readiness document's count. The comment uses the ticket's numbers.
4. "C-1 to C-51": the file now ends at C-54.
5. "8 check rows on the head" is true; main's commit has 7 (four `ci`, three of the code-scanning run), and the repository has 6 runs (the commission names two of them).
6. Backlog "line 99" is the file line; it belongs to owed item 16. Runbook line 87 holds the blank-line limit but not the word only.
7. The B1764 STATUS has no section named DEVIATIONS (its differences are in FOR TUESDAY, point 7).
8. Round 3's FOR-RECORDS item "OWNER DECISION if the first pull request reads blocked" is closed by the landing; OXPD2-10's stale text already has a coordinator comment (id 41411) saying the draft exists.

## UNMEASURED
- That `mergeable_state` read clean before the merge (Tuesday's read; the closed pull request now prints unknown).
- Whether Tuesday has asked the product owner for the three HP items (Q2).
- The five whole-summary Jira searches; that a create with a `parent` field and three labels is accepted by this board (the first build seat created 17 that way; I wrote nothing to Jira).
- Whether the `actions` language can be added to the default setup, and by whom; any click path for required checks.
- The object count a run would read after the lane branch is removed; that removed commits are no longer fetched (the third review's derived reading).
- `actions/setup-dotnet` v6.1.0, the `.pdb` files and the `web.config`: relayed from round 1, not re-read.
- C-54: not read. The builders' kits: not read (their STATUS sections FOR TUESDAY, DEVIATIONS, NOT RUN and RECORDS were; the rest of each STATUS was not).
- CLARIFICATIONS C-1 to C-40: headings only; C-34, C-39 and C-40 to C-53 were read.
- The form kit `B1766` was read whole in three pages; `DRAFTER_RULES.md` and the project `CLAUDE.md` whole; all nine review files, `landing.txt`, the lane plan and the three record files whole.

## Outside-the-fences disclosure
- Nothing was written outside my three files and the scratch folder. No Jira write, no `gh` call but `-X GET`, no git write verb, no `cd`, nothing deleted, no test or build run, no credential printed (the `gh` account name was masked in my own output). One failed call: `orgs/datasecau/rulesets/24139430` answered 404 for want of an organisation scope; I did not ask for it and read the repository path instead.
- My first log fetch wrote 8 empty files and was repeated with `--allow-escape-sequences` over the same scratch names (my own files).
- The kit names no person, no decision-card id and never the name of the keystore file at the root of the OneDrive tree. A comment on OXPD2-1 that I read (id 41412) explains why that name is a secret; I copied nothing from it.
