STARTABLE: YES

# B2004 DRAFTER REPORT (records kit for NexusAI, seat SEAT-R306; drafter Opus, in-session, read-only)

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-23_B2004_SEAT-R306_nexusai-records.md` (266 lines, about 114 kB) and its sidecar `.measured` (126 claims, 126 measured: 68 by a named instrument, 58 marked N/A because they are instructions or prohibitions and not outputs to match; `stamp_check.py <kit>` rc=0). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s317/d2004/` (tools, raw reads, card prints). Clocks from `date`: first read 20:06:54, last read before writing 20:21:54, last check 20:28:11 AEDT 2026-11-23.

## BLUF
- **Scope as commissioned:** Kam's NexusAI words today become C-313 and C-314. C-313 covers the RD-1032 rulings: the 10:07 "Show me options first" and the 11:06 "looks great. please build and deploy", which the decision store recorded as option (a) "Darker brand colours" at 11:07:28. C-314 is the 11:37 "Deploy now": the C-224 hold is lifted for that one deploy only. C-315 records the landings of pull requests 243, 242 and 244. C-316 records the two demo deploys the records lacked (2026-10-16 and 2026-11-23), plus the deploy kit's two defects as runbook lines. Jira gets comments on RD-1032 and RD-1030 and moves both to Testing. There are 3 new tickets: the signal-file race (created, then moved to Testing because its fix already landed), the two stale comments left by RD-1030, and forced colours. One HISTORY.md branch is written.
- **Every hosted fact is final.** All 24 check-runs of the three merge commits had concluded before drafting (18 success, 6 Deploy demo skipped). The kit has no evidence wait.
- **Two findings that change the records' story.** (1) The 11:37 card's BLUF said the demo was last deployed on 21 September, with 989 commits since. That was written from records that lacked the 2026-10-16 deploy. The real move was 17fc6c51 to 21a07e3c: 570 commits and 160 merged pull requests. The 1,000-row cut (the merge of PR 120) is 149 commits after 17fc6c51, so this deploy is the first to put it on the demo. C-314 records this as a correction; the choice itself is unchanged. (2) The revision replaced on 2026-10-16 was the 2.2.0 release image (its name ends `220-fdda330`, per RD-846 comment 39503), not revision 0000099. So DN168's draft title "since 2026-09-21" would have overclaimed. C-316 is titled "since 2026-10-16" and marks the intermediate revision's date as not read.
- **Review B1999 finding 3 is honoured.** No card id appears in any entry. The entry scan refuses a card-shaped token, and the kit's control plants `nexusai-demo-deploy-c224-1123`.

## Facts re-measured (instrument -> result)
- GitHub, `gh api -X GET` under the project's GH_CONFIG_DIR:
  - main is `21a07e3c…`; 0 open PRs; PR 245 returns 404.
  - Merged times: PR 243 00:46:58Z, PR 242 02:16:15Z, PR 244 05:48:51Z.
  - Merge tree equals head tree for 243 and 244. For 242, `compare head...merge` is ahead 3 and lists exactly 243's two test files.
  - Files and adds/dels: 243 has 2 files (16/4), 242 has 4 (31/6), 244 has 8 (217/13).
- `hosted2004.py`: each merge commit has 8 check-runs and 5 workflow runs. The Deploy demo runs `45090779073`, `45099235994` and `45120108278` read skipped, with both jobs skipped. Build VERDICT lines read 6235/6235/394, 6237/6237/394 and 6245/6245/395.
- Code scanning on main: 22 open, 222 fixed, 7 dismissed. These are the same 22 open numbers as B1947; the newest open alert is from 2026-11-08; no alert was fixed after 2026-11-22T13:00Z. The javascript-typescript analysis of each merge commit has 29 results.
- `pointers2004.py`: 18 asserted rows, 0 fail, and both controls read False. In both css files at 21a07e3c, `forced-colors` counts 0 while `consumable-fill` counts 17 and 4. Each of the three toner hex values counts 1 at 21a07e3c and 0 at 85b39c77.
- Jira GET, using the project's .env loaded by name in-process:
  - RD-1032 and RD-1030 are both To Do with 0 comments. RD-99999999 returns 404.
  - The board has 1028 issues; the highest key is RD-1032. The label `records-pass-1123` covers 3 tickets.
  - The five markers each read 0; the three controls each read 1.
  - Each create's searches are spelled out in its P-label. RD-677 holds the dot colours. RD-1024 is different residue.
- Text scans used the project's scanner: a byte-equal copy of `.tools/b1947/scan1947.py` (prefix `3707dc37c4795fbf`; its selftest prints 67 ok lines).
  - 21 Jira texts in jira mode and 40 entry and history texts in entry mode: 0 hits each, alone and after sample fill-ins.
  - The first pass caught two traps, which I reworded: the magenta hex `#b44752` contains b4475, and the RD-525 helper's filename contains `live`.
  - `texthash2004.py --check` over the kit: 61 texts, 0 hash differences.
- Card prints: `decision_queue.sh show` for 4 ids, read once each into scratch, rc 0. `kam_rulings_today.sh`: 12 rows. I pointed its read marker at scratch (`KAM_READ_MARKER`) so Tuesday's marker did not move.
- No repository runbook carries either defect. `DEPLOYMENT_GUIDE.md` at 21a07e3c holds 0 lines with `acr build`, `--file`, `activity-log` or `end-time` (control: `az containerapp update` at lines 133 and 244). `scripts/deploy-dev.sh` runs `cd "$ROOT"` (line 48) before its `--file Dockerfile .` build (line 107).

## D-decisions (the drafter's; each is Tuesday's to overturn)
- D-1: one section with four entries, ordered rulings → landings → deploys. Each landing's numbers are written literally (all were final), so no fill-in waits on a poll.
- D-2: the race ticket goes in first (5a), so the RD-1030 Detail's "filed in this pass" is already true when that comment posts.
- D-3: NEW-B folds review B1964's two LEFT FOR OTHERS items and the 205/203 route count into one ticket (one review row, I-6).
- D-4: the dots (B1989 I-3) get a record line naming RD-677, which already holds them as off-palette literals. Whether the dots should match the bars is a product owner question, so nothing is filed.
- D-5: the runbook lines live only in C-316. No repository doc carries either fault; both were faults of Tuesday's deploy kit, so the fix belongs in Tuesday's demo-deploy kit form.
- D-6: no comments on RD-711, RD-615, RD-876 or RD-846. NEW-A names RD-711 and RD-615 as related.
- D-7: the hard stop defaults to the stamp clock plus 3 hours, since the commission names none.

## Q-questions for Tuesday (each with a default)
- Q-1: move RD-1032 and RD-1030 to Testing (CLAUDE.md line 302: code change → Testing; Release Ready is a human's move after verification, and the demo deploy does not change that)? **Default: both move.**
- Q-2: create the race ticket (Bug, Low) and move it to Testing, since its fix landed in PR 243? **Default: yes (MOVE-A = `A`).** Alternative: leave it in To Do.
- Q-3: one ticket for the two stale comments plus the route count, or record lines only? **Default: NEW-B, Task, Low.**
- Q-4: forced colours: a ticket? **Default: NEW-C, Bug, Low.** Alternative: a record line.
- Q-5: dot vs bar colours: record line only, with no write on RD-677? **Default: yes.** It could go to Kam as a morning-summary question.
- Q-6: no comments on RD-711 or RD-615 (FOR-RECORDS says they "may take a comment"), on RD-876 (the silent cut is now on the demo), or on RD-846? **Default: none.**
- Q-7: runbook lines in C-316 only, with no ticket and no repository edit? **Default: yes.**
- Q-8: the 06:59 morning-plan card is Datasec/Fleet and rules no NexusAI item. Leave it out of the NexusAI records? **Default: leave it out.**
- Q-9: does the launch line get `WED_USAGE_STOP=100`? The kit copies B1947's form, which has none. **Default: B1947's form.**
- Q-10: the 11:06 words are quoted as the board reader prints them (one space), with a note that B1989 quotes two spaces at 11:06:40. Can Tuesday read the raw row? **Default: as written.**

## Chain inputs (MEASURED LITERALS rule 4)
| step | inputs | produced by |
|---|---|---|
| 0 | the stamped kit, `.tools/b1947/scan1947.py` | BASE (Tuesday's stamp; the file exists, 6267 B) |
| 1 | git config, the deploy key path, origin | BASE |
| 2 | the kit's lists, the scanner copy | Step 0 |
| 3 | GitHub, Jira, CLARIFICATIONS.md | BASE; helpers from Step 2 |
| 4 | texts in the kit, Step 3 facts, slots | Steps 0 and 3 |
| 5 | Step 4 payloads, move checks from Step 3 | Steps 3 and 4; NEW-A's key from 5a feeds only the entries |
| 6 | Step 5 read-backs (keys, comment ids) | Step 5 |
| 7 | `entry-numbers.txt`, Step 5 read-backs | Steps 5 and 6 |
| 8 | everything above | Steps 0 to 7 |

## UNMEASURED
- The demo itself. Both deploys are RELAYED from DN168's STATUS, review B1999 and RD-846 comment 39503. The drafter made no Azure call and no request to the demo.
- The transitions offered on RD-1032 and RD-1030 (not read; the kit tells the seat to read them).
- The repository's configured identity (`be76c2c1…` is RELAYED from B1947's READY line).
- The raw spacing of Kam's 11:06 row.
- When the `220-fdda330` revision was put on the demo.
- The full verify of PR 243's head (relayed by its review).
- The search figure of 160 PRs comes from the GitHub search API, whose index can lag. Its frame is stated in the kit.

## Outside-the-fences disclosure
1. **Three hook refusals, all on my own typing, none of them a write:**
   - a `cd /dev/null` prefix (refused by `pretooluse_no_cd.sh`);
   - an unquoted `======` separator (zsh);
   - a command held in an unquoted variable (`$J`).

   Each was re-issued in the corrected form.
2. **Listings I did not need:**
   - `ls -la` of `/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude` printed file names only (no contents read), as a side effect of checking that the path exists.
   - `ls` of the NexusAI `.tools/` folder (names only) to check that `b2004` was absent. The B1947 kit forbids its seat from listing `.tools/`; my fences do not, but I name it.
3. **Reads under the seat rules:**
   - I read B1947's seat file `.tools/b1947/scan1947.py` and `common1947.py` (headers by grep), and `jira1947.py`'s first 30 lines, and copied `scan1947.py` into scratch. That is the project's scanner, as DRAFTER_RULES asks.
   - `kam_rulings_today.sh` was run with `KAM_READ_MARKER` pointed at scratch, so it wrote a marker file there and not Tuesday's.
   - `decision_queue.sh show` was also run on `datasec-morning-plan-1123` (a Datasec/Fleet card) to judge whether it was NexusAI.
4. **Jira and GitHub:** GETs only, including the search API. Nothing was written to the project, its repository, Jira or GitHub. No Azure command. No mail.
