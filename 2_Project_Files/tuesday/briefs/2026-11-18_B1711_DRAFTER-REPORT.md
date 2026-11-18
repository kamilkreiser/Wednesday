STARTABLE: YES (once Tuesday stamps the nine slots; Q-1 to Q-4 are readings of yours to confirm, none blocks the launch; Q-3 should be settled before the stamp)

# B1711 drafter report (SEAT-R269, MPS records pass for PR #214 and #215)
Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-18_B1711_SEAT-R269_mps-records-214-215.md` (225 lines by `wc -l`; 10 four-underscore lines: nine slots and the last line `READ-WHOLE-BY-TUESDAY: ____`), sidecar `.measured` 123 lines. `stamp_check.py` exits 0 (123 claims, 123 measured, 0 TODO; run alone, rc=0). Shape copied from B1703 (R268). Drafted 2026-11-18; `date` printed 12:09:48 at the first GitHub read and 12:25:47 at the last one. Slots: STAMP, LAUNCH WINDOW, BASE, JIRA, MOVE, CREATE-C, RECORDS, REC-MERGE, Hard stop.

## BLUF
- **Planned writes: at most 5** (1 create + 2 comments + 2 moves; the poster refuses the 6th), entry **C-181** (C-180 is taken: B1703 landed, root main f25235f0, `### C-181` reads 0), rows `[B1711-DONE-1]`, `[B1711-OWED-1]` to `[B1711-OWED-3]`.
  - Create first (slot CREATE-C `C`): the stale class comment at `tests/MpsCalc.Import.Tests/PanelOptionImportTests.cs:12` ("the parity proof counts them only"), with `docs/IMPORTER.md:17` named inside the same ticket as OPTIONAL. **No second ticket** (see Corrections).
  - MPSCALC-412: comment, then Done if slot MOVE names it. All six clauses MET at main 51ed36eb.
  - MPSCALC-413: comment, then Done if named. All four clauses MET; clause 3 (what is done with each of the 12 findings) rests on one shared reason, the coordinator's reading (Q-1).
  - Recommended MOVE `412,413`; CREATE-C `C`. After the writes: 414 issues, 251 Done, 163 not Done (before 413, 249, 164).
- Model Sonnet (model-routing.md line 97 row C7, line 110 row G3; `claude-sonnet-5-5` at models_latest.json line 23; `brief_seat.sh` line 31 defaults to opus, so `BRIEF_SEAT_LEVEL=sonnet` is inside the quotes). Pane `Datasec/MPS-R269`; `R269` and `B1711` occur in no other SEAT kit of 17 and 18 November (word scan, 0 and 0); no `Datasec/MPS-` pane (tmux list-panes at 12:13, 12:20, 12:24: 0). No port, no listener.

## Corrections to the facts in the commission (read at source)
1. **C-181, not C-180**: root main is f25235f0 (B1703 landed C-180 with comments 41370 to 41374, four moves, 412 and 413 filed). Jira census now 413 / 249 Done / 164 not Done.
2. **"Log printed found 0 vulnerabilities"**: true, and read on BOTH squash web jobs (job 134494021475 for #214, 134494373415 for #215: each 1 line, step 5 `npm audit, production dependencies (blocks on high/critical)` success) and on the PR head job 134484844660. At 12:11 both squash web jobs were still running (log 404 BlobNotFound); they finished by 12:20, so the kit asks the seat to read both logs at the write.
3. **A new fact: Dependabot now reads 1 OPEN alert** (number 11, picomatch, scope development, high, created 2026-11-18T01:08:11Z, i.e. 12:08 AEDT, after the squashes). MPSCALC-413's description says 0 open. The 413 comment therefore carries a program-read fill-in `<<DEPALERTS>>` (never a hard "0 open"); a production-scope open alert HOLDS 413's move. Fixed alerts read 9.
4. **B1710 F3 recommends ONE ticket** ("One records-pass ticket (comment line :12 plus optionally :17)"); it does not recommend a second one for IMPORTER.md:17. So the kit files one ticket and names :17 as optional inside it; slot CREATE-C is the only create.
5. The squash of #214 read 7 of 8 success at 12:20 (a `package` job running) and 8 of 8 at 12:25:47; #215's squash 8 of 8 at 12:20. Analyses by `commit_sha`: 4 each, results 0, on a2af7340, 3e2bbab4, 009c908a, 51ed36eb and 8ae5db6e (control: 8ae5db6e reads 4; the `commit_sha=` URL parameter does NOT filter, it returned 100 rows, so the kit says filter by program).
6. The builder's STATUS (B1706) carries the new sentence; it ends with the compatibility basis in double quotes, which the Jira text rules ban, so the 412 comment quotes it up to `does not re-read the book` and says the basis follows in parentheses.

## Facts re-measured (instrument, control)
- Code main 51ed36eb958c33ed83703eba7e81c5b7bea261fe (`git/ref/heads/main` at 12:09, 12:11, 12:20, 12:25); `compare 8ae5db6e...main` ahead 2, behind 0, 3 files. #214: merged 2026-11-18T01:00:51Z (12:00:51 AEDT), 1 parent 8ae5db6e, 1 path ci.yml +4 -0, tree d229b1cb. #215: merged 01:01:38Z (12:01:38 AEDT), 1 parent 009c908a, 2 paths +16 -1 (1 1 and 15 0), tree c657b053. Squash file blobs equal the reviewed heads' (ci.yml 81a1a737, PriceBookImporter.cs 9a9e01dd, PanelSectionEndTests.cs 8daf8da9). Open PRs 0; `pulls/99999` 404 (control).
- Checks: heads 9 of 9 success each; #215 squash 8 of 8; #214 squash see 5; code-scanning open alerts on main 0.
- Job logs (ANSI stripped): dotnet #214 squash 743/197/3663, #215 squash 743/198/3663, `0 Warning(s)` and `0 Error(s)` once each; both web jobs `Tests  1616 passed (1616)` once, 0 lines matching `[1-9][0-9]* failed` (control: a planted `1 failed` counts 1).
- Tarball of 51ed36eb (own folder, run nowhere): ci.yml lines 62 to 65 (comment, comment, step name, command); `audit` on 3 lines (63 to 65), `npm` on 10; `npm audit --omit=dev --audit-level=high` 1 line; PriceBookImporter.cs:150 holds the new sentence; `does not compare them` only at PanelSectionEndTests.cs:192 (the absence assertion), 0 in src and docs; `the parity proof counts them only` 1 line (PanelOptionImportTests.cs:12); `counts them and compares the governed options only` 1 line (IMPORTER.md:17). `git hash-object` equals the tree blob 10 of 10, a planted byte differs 10 of 10. Pointers Q01-Q07, P01-P12, C01: 20 of 20 print; control with the last character changed 0 of 20.
- Jira (GET only, scratch helper reading the project `.env` by name in-process, no token printed): 412 and 413 Backlog, 0 comments, label records-pass-1118, type Task id 10030, transitions list 41 = Done; 207 Done; census 413 / 249 / 164 (controls: `key >= MPSCALC-1`, MPSCALC-361 Done, MPSCALC-99999 and MPSCALC-414 404, MPSCALC-1 200); markers `REC-LAND-412-18NOV`, `REC-LAND-413-18NOV`, `LAND-NEW-C-18NOV` read 0 (controls `REC-LAND-390-17NOV` finds 390, `REC-LAND-411-18NOV` finds 411); phrase searches for the new ticket as listed in the kit.
- Root: main = HEAD = f25235f0; tracked dirty exactly history.md, BACKLOG.md, JIRA.md; `remote -v` 0 lines; no `records/b1711`, no `.tools/b1711`; BACKLOG 5936, JIRA.md 861, history 1538 lines.
- Scan: copy of `scan.py` (read by `cat`; sha256 d21a053d... equals `.tools/b1665/scan.py` and `.tools/b1703/scan.py`) plus double-quote, URL and newline refusals over 11 Jira items (2 outcome sentences, 2 comments, 1 summary, 6 paragraphs) and the 4 record texts with sample fill-ins: 0 problems; 11 of 11 controls fire (plus underscore-aware name, `complet`, version exemption); planted Tuesday, B1494 and `seat M113` fire. Frozen hashes in the kit were recomputed from the finished file: 412 comment 502391441f17... (4448 characters), 413 comment b9446edfcdfa... (4163), summary b049a0c9... (237), description 60ccddf5... (3979), the two outcome sentences equal B1703's; a one-character mutant differs.

## Every who-decided phrase in the kit, and the line it was checked against
Cards read with `decision_queue.sh show <id>` only, into a scratch file (no `list`):
- **mps-413-web-audit-instrument-1118**: `status: ruled (Datasec/MPS)`; title names MPSCALC-413; `[a] Add a production audit step`, detail `Passes today with 0; developer tools updated at the next routine round`; `ruling: choice='a' ruled_ts=2026-11-18T11:22:03.800853+11:00`; `delivered_artefact` names PR #214.
- **mps-412-panel-note-words-1118**: `status: ruled (Datasec/MPS)`; title names MPSCALC-412 and the last sentence of the importer's colour-panel note; `[a] Developer fix, list it after`, detail `Corrected from the code with a test; the review reads the words; you see the sentence after it lands`; `ruled_ts=2026-11-18T11:22:00.725464+11:00`; `delivered_artefact` names PR #215 and says the final sentence was sent to the product owner on the live board after landing.
Phrases (kit line numbers are those of the file as written):
1. BLUF (2), THE BASIS, comments 412 and 413, entry "The rulings", history, BACKLOG OWED-2: "the product owner's 2026-11-18 ruling ... option ..." with the exact label and detail above: both lines checked. Written "as the coordinator relays it from the decision record".
2. 412 comment and entry: "the coordinator sent the product owner the final sentence after the landing (relayed)": checked against the 412 card's `delivered_artefact` line (Tuesday's own write; written as relayed, not as read by the seat).
3. 413 comment, BLUF (2), entry "The instrument decision": **"GitHub Dependabot alerts stay as they are" is written as the coordinator's reading**; the only source is the 413 card's BLUF (Tuesday's recommendation text: "keep GitHub's alerts as they are"), which is not the option's detail. The text says exactly that.
4. 413 comment and entry: "one shared reason answers each of the 12 findings": written as the coordinator's reading; on no card.
5. C-79 "the product owner's 2026-11-01 ruling": checked at root main `CLARIFICATIONS.md:1712` (heading), `:1714` (words), `:1716` (settles). C-109 "the product owner's 2026-11-11 ruling": checked at `:2716` (heading), `:2719` (ruling), `:2720` (settles).
6. New-ticket paragraph 2 and BASIS: "the coordinator reads the code comment as developer-only" (Tuesday's reading) and "whether either sentence goes to the product owner's word review is not decided here".
7. Every "MET" is "the coordinator's reading". No sentence says the product owner ruled the Done moves, the 12-findings reading, or the instrument beyond the option's own words.
**Caveat for Q-3:** neither card carries a field naming WHO ruled (`show` prints only choice and timestamp), and the two are 3 seconds apart (11:22:00 and 11:22:03). The kit treats them as the product owner's rulings, as B1703 did and as your commission states; if either was applied by Tuesday under a standing rule, change "the product owner's 2026-11-18 ruling" to "the coordinator's" in the five places named in item 1 before stamping.

## Input table for the chain (rule 4)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit and sidecar, root repo state, the four record files | exist at BASE |
| 1 | `.tools/b1703/` helpers and `scan.py` (read by `cat`) | exist at BASE |
| 2 | root main, code main, tarball, job logs, Jira reads, record greps | exist at BASE (read-only) |
| 3 | Step 0-2 prints, frozen hashes in the kit | Steps 0-2, kit |
| 4 | Step 3 payloads, `snap_before.json`, the new key (create first), transitions GET | Steps 2-3 and 4a |
| 5 | Step 4 results (comment ids, key, counts), worktree of `main` | Step 4, BASE |
| 6 | the Step 5 commit, `refs-before.txt` | Steps 0 and 5 |
| 7 | all | Steps 0-6 |

## D-decisions (mine; each reversible by your word)
- D-1: one comment template per key with `<<OUTCOME>>` (B1703's two frozen sentences, same bytes); no 195-style third sentence.
- D-2: MOVE slot keys `412,413`; CREATE-C replaces CREATE-P and CREATE-A (one ticket).
- D-3: markers `REC-LAND-412-18NOV`, `REC-LAND-413-18NOV`, `LAND-NEW-C-18NOV`.
- D-4: order create C, then 412 (its comment names the new key), then 413.
- D-5: 413's comment records the instrument decision in the form the acceptance check asks for (instrument, predicate, treatment of the 12), with the Dependabot half and the shared-reason half written as the coordinator's readings.
- D-6: three BACKLOG OWED rows (stale comment, development toolchain at the next routine round, old note text in held stores) plus DONE-1; the entry says rows `[B1703-OWED-1]` and `[B1703-OWED-2]` are discharged without editing them (both ids added to the exact-string exemptions of the text rule).
- D-7: the 412 comment quotes the new sentence only up to `does not re-read the book` (the basis tail holds double quotes).

## Q-questions for Tuesday (each with a default)
- Q-1: MPSCALC-413 clause 3 ("what is done with each of the 12 findings (bumped, or accepted with a reason)"). The kit reads one shared reason (all development dependencies that never ship, production audit 0, wait for the next routine round) as answering each. Default: MOVE `412,413`. If you read the clause as needing the 12 listed one by one, set MOVE `412` only; the stays-open sentence is already frozen. I did not run `npm audit` (registry is a hosted host), so the 12 are RELAYED from the B1709 review and not listed.
- Q-2: CREATE-C `C` (recommended). `NONE` keeps the text in BACKLOG row `[B1711-OWED-1]`.
- Q-3: Authority wording (see caveat above). Default: leave as the product owner's, as B1703 did.
- Q-4: C-181 still the next number at stamp time? Default yes (the seat re-derives by program and STOPs on a taken heading).

## UNMEASURED
- Any `npm audit` run (needs the registry); the 12 findings by name; whether the open Dependabot alert (picomatch) is one of the 12.
- The seat's own pane name and the final CI state of code main at the write (the seat polls up to 20 minutes).
- The sidecar's instruction-text lines (31 of 123) are marked UNMEASURED as outputs (fragments, command shapes, fill-in forms), as in B1703.
- `tmux list-panes` was read at 12:13, 12:20 and 12:24, not at the stamp.

## Outside-the-fences disclosure
- Wrote only the kit, its `.measured` sidecar (via `stamp_check.py --init`, then rewritten by a scratch script from my own reads) and this report. All scratch (Jira reader `jget.py` and `jx.py` that read the project `.env` by name in-process, `texts1711.py`, build and fill scripts, the scan copy, extracted tarball in its own folder, job logs, card text files, the CLARIFICATIONS copy) is under `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/7d54115b-162a-4248-9923-2b718612d52b/scratchpad/`; nothing in any project tree.
- Jira: GETs only (tickets, JQL with `project = MPSCALC AND ( ... )`, transitions list, issuetype). GitHub: `gh api -X GET` only, under the project `GH_CONFIG_DIR` (pulls, commits, trees, check-runs, analyses, alerts, Dependabot counts, job logs, one tarball). git: read verbs with `--no-optional-locks` on the project root (rev-parse, log, show, status, branch --list, remote -v). tmux: list-panes and display. `decision_queue.sh show` on the two named ids only; no `list`. No HTTP to any hosted site, no az, ssh, docker. A recursive `grep -r` over the briefs folder for `B1711` timed out and ran on in the background; it is read-only and holds nothing.
- Hook refusals taken: a `=-=-=-` echo separator (zsh expansion), an unquoted `$J` command variable, and one stray `cd` (refused; no effect). Advisories on `grep | cut` were taken: the counts that matter were repeated through python or with a positive control.
- I read the stamped B1703 kit via the Read tool in three pages (lines 1 to 133, 134 to 213, 214 to 286) and its `.pre-stamp` slot block and sidecar whole.
