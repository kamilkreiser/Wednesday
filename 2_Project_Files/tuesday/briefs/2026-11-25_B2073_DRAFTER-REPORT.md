STARTABLE: YES

# B2073 DRAFTER REPORT (Opus drafter, in-session, read-only): NexusAI records kit for pull requests 250 and 251 (RD-1036) plus one security ticket (the review's F-Q0), seat R321

Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2073_SEAT-R321_nexusai-records-250-251.md` (99995 bytes, 174 lines, last line `READ-WHOLE-BY-TUESDAY: ____`). Sidecar: the same name plus `.measured` (175 claims, 175 measured; `stamp_check.py <kit>` exits 0). Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s325/d2073/` (reads 05:31:38 to 05:44:29 AEDT; sidecar reads re-run 05:5x; clocks from `date`).

## BLUF
- One kit, one seat (Sonnet by default, see Q-1). In order: create ONE security ticket NEW-Q0 (Bug, Medium) for the review's F-Q0 plus F-3; then ONE result comment on RD-1036 that names the new key; then move RD-1036 to Testing. Records: CLARIFICATIONS section 112 with three entries. C-324 is pull request 251 with its review and the F-1 correction. C-325 covers who chose the fields, what the plain routes still send, F-2 as a product choice not taken, and a correction of the "config.read" wording in C-319 and C-320. C-326 is pull request 250. Last, an optional history branch `records/b2073-history`.
- Every fact of the commission was re-measured at source and matches. PR 251 landed as merge `11149d3f` (parents `e2911754` + `c1a99d4b`, merge tree = head tree `0a0f0a4a`). Deploy demo run `45440511193` read skipped, with both its jobs skipped. Main is `11149d3f` with 0 open pull requests.
- One addition the commission did not name. PR 250 (the previous pass's history branch, merge `e2911754`) has no record yet, and the form records such a landing (as C-322 did for 249). I added C-326 for it (Q-4).
- One premise of the commission is contradicted. B2043 and B2055 both ran **Sonnet**, not Opus-class: each kit says `MODEL SONNET` and `BRIEF_SEAT_LEVEL=sonnet`. The kit is written for Sonnet (Q-1).
- Card `datasec-nexusai-datasources-all-roles-fields-1125` reads **open**, with no ruling. I read it with `decision_queue.sh show` into scratch; the output names the id once. Options a and b file a ticket. Option c ("Nothing filed or built until we talk") files nothing. So a new Stamp slot **CARD** gates the create: any state other than `open` stops the whole seat (Q-2).
- One honest caveat now sits in the ticket text and is absent from the card (Q-7). The permission table marks `end_user` as "proposed" and both partner roles as "deferred" (capabilities.js 83-85). The user update route accepts only admin or viewer (server.js 3693). The create route stores any role value (server.js 3645), so a stored user can hold those roles today. That is DERIVED from source; it was not run.

## Facts re-measured with instruments (each with its control)
| Fact | Instrument and result | Control |
|---|---|---|
| main | `gh api -X GET git/ref/heads/main` 05:31, 05:44, 05:49 -> `11149d3f38b0...`; `pulls?state=open` 0; `compare 11149d3f...main` identical | `pulls/99999` 404 |
| PR 251 | `pulls/251`: merged 16:43:51Z (03:43:51 AEDT 25 Nov), merge `11149d3f`, base `e2911754`, head `c1a99d4b`, 2 commits (`23b3a023`, `c1a99d4b`), 3 files 352/3 (admin.js 27/0, test 322/0, counts 3/3); trees equal `0a0f0a4a` | `compare e2911754...11149d3f` lists exactly the 3 paths |
| PR 251 body | python: equals `B2071_verify/pr-body.md` after stripping trailing newlines | sizes 5492 vs 5491 |
| PR 250 | `pulls/250`: merged 08:51:49Z (19:51:49 AEDT 24 Nov), merge `e2911754`, parents `c74d1ad4` + `ba8418c6`, 1 file HISTORY.md 21/0, trees equal `1b46ff22` | `compare ba8418c6...e2911754` files [] |
| Checks 251 | 8 check-runs completed: 6 success; Deploy demo `build` 138610068518 and `deploy` 138610010895 skipped. 5 runs, all completed: Build 45440511368; Push on main 45440511362 (event `dynamic`); Deploy demo 45440511193 (push, skipped; its jobs skipped); npm-audit 45440511228; Gitleaks Scan 45440511253 | check-runs mapped to runs by `check_suite_id` |
| Checks 250 | 6 check-runs all success; 4 runs; Deploy demo runs for `e2911754`: 0 | same read for `11149d3f`: 1 |
| Build logs | `--allow-escape-sequences`: job 138610005396 `6323/6323 tests passed across 398 suites` (1 line); job 138326772429 `6300/6300 ... 397` (1 line) | `VERDICT: FAIL` 0 in each, beside `VERDICT: PASS` 1 in each |
| Counts file | `pointers2073.py`: at `11149d3f` 6323/398; at `e2911754` 6300/397 | - |
| Code scanning | main paged, 251 rows: 22 open (the same 22 numbers as B2055), 222 fixed, 7 dismissed; 0 created or fixed since 2026-11-22T13:00Z; **static/js/admin.js 0**; analyses at `11149d3f`: js 2240796046 29, python 0, actions 0 | `backend/server.js` 13; 222 fixed rows each carry `fixed_at` |
| Pointers | `pointers2073.py`: `pointer rows 28 fail 0` (admin.js 176/186/203/245/252/258; server.js 3645/3693/15691/15693/15703/17163/17166; capabilities.js 83/117/118/119/155; authEnforcement.js 634/644; jsonStorage.js 4168/4177/4226; index.js 4288; the counts at both commits) | `loadViewerDataSources` on admin.js line 1 at M False; anywhere in admin.js at `e2911754` False |
| Table not enforced | `git grep` at `c1a99d4b` in the gate's own clone (TUESDAY scratch, read verbs): files under backend/ and scripts/ requiring `services/capabilities`: 0 | backend files naming `authEnforcement` 6; test files naming `services/capabilities` 8 |
| RD-1036 | jr.py GET: To Do, Task, Medium, labels `records-pass-1124,security`, 0 comments, description 3541 chars, ends `[DSLIST-247-24NOV]`; transitions: id 31 `In Review` -> Testing | RD-99999999 404 |
| RD-1021 | Testing, 1 comment 41471; its item (3) wording "to every role holding config.read" | - |
| Board | 1035 issues, highest RD-1039. Label `records-pass-1124` reads 4 (RD-1036..1039); `records-pass-1125` reads 0. Markers `LAND-251-1036-25NOV`, `DSWIRE-251-25NOV` and the variant `-26NOV` read 0 each | `DSLIST-247-24NOV` -> RD-1036; `LAND-247-1021-24NOV` -> RD-1021; `HARDEN-248-24NOV` -> RD-1039 |
| Duplicate search | 14 phrases (route paths, config.read, capabilities.js, permission/capability table, not enforced, the three role names, every signed-in, stored fields, viewer-safe, getAllDataSources), 56 distinct keys; all 56 read whole by jr.py. By program, 10 mention a route not followed by `/`. Read in context, none asks these GET routes to refuse a role or the table to be enforced. Nearest neighbours: RD-469 F-13 (the same response, the identifier mask) and RD-929 (role model design). Both are named as related | each count equals the keys printed (assert in scan2073.py) |
| Records | CLARIFICATIONS.md 941642 B, 3240 lines, sha `ca688cce0fa2441a`, max section 111, max C-323. Lines naming PR 250/251/`11149d3f`/`e2911754`/C-324: all 0. "to every config.read role" on line 3217 only; "to every role holding config.read" on line 3223 only. HISTORY.md at M: 10427 lines, 1140005 B, sha `84091f838f9b3279`, 7563 non-ASCII, last heading 10408 | `C-316` 7 lines; `**Hosted checks.**` 3 lines; HISTORY `pull request 248` 1 |
| Layout | simulated append on scratch copies (sample fills): heading 3242; C-324 3244-3248; C-325 3250-3252; C-326 3254-3256; ends 3256. HISTORY heading 10429, 10448 lines | prefix byte-equal and added bytes ASCII, both True |
| Identity | `gh api commits/ba8418c6`: author and committer domain `users.noreply.github.com`, sha256 prefix `be76c2c1baf03ec1` (address never printed) | `records/b2073` refs 0; control `records/b2055` 1 |
| Scanner | `.tools/b2055/scan1947.py` copied by python read: 6267 B, sha `3707dc37c4795fbf`, `cmp` equal | bank scan 33 texts (alone, sample fills, HELD fills): 0 problems. First run 1 problem (a doubled paren in E-C1-5 under HELD forms), fixed with `<<DISP-Q0-SHORT>>`. Planted `Tuesday` (both modes), `_by_Kam_`, `secret`, `B2073`, `R321`, card shape, doubled paren and 3-word repeat all FIRE |
| Seat id | 201 non-.pre-/.measured SEAT kits of 11-18..25: R321 read 0 at 05:3x. At 05:49 the sibling OXPd kit B2072 (line 9) names R321 as this kit's seat, which is not a taking. R320 is B2072's seat | R318 in 2 files |
| Model row | `model-routing.md` 97 (C7), 98 (C8), 110 (G3); `models_latest.json` 23 `claude-sonnet-5-5`; `brief_seat.sh` 31 `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"` | - |
| Panes | `tmux list-panes -a` 05:36 and 05:44: `%0 tuesday` + 2 unnamed; no `Datasec/NexusAI-*` | - |

## D-decisions (mine, each reversible by a slot or a word)
- **D-1 Order: create first, then the comment.** This differs from B2055's order. The comment's item 1 can then name the created key through `<<Q0-CLAUSE>>`. It also means the create's 14 searches run before RD-1036 carries text that would match `every signed-in` or `config.read`.
- **D-2: no card id and no "coordinator" in any Jira text** (the scanner bans the word). The fields are "a default of this change inside his answer". The board question is "asked on his board ... no answer when this note was written".
- **D-3 F-1 is a correction, not a ticket.** The comment's item 2 and C-324's **Correction.** cover commit A's "An administrator's tab is unchanged" and the build STATUS's "none known". Neither original is edited.
- **D-4: RD-1036's description held the 247 review's F-1 (the plain routes).** The comment says that part moves to NEW-Q0. RD-1021's item (3) is not written; C-325 records its wording correction.
- **D-5 Closes B2055's Deviations 1, 2, 4, 5 and 8 by construction.** The kit now spells out the order, requires every READ item in Step 0, allows selftest fake files by name, requires saved drivers, and names the length measure. It also keeps B2043's 3, 5 and 9 closed: whole-group rerun, a REVIEWED guard list of 56 keys, and no run id in any template, with the doubled-paren check run on HELD forms too.
- **D-6: REFUSE 5 adds `backend/server.js` and `capabilities.js` to the stop paths.** The ticket's line pointers sit there.

## Q-questions for Tuesday (each with its default; the Stamp's Q-ANSWERS slot takes them)
- **Q-1 Model.** The commission said Opus because "B2043 and B2055 ran Opus-class". Measured: both kits read `MODEL SONNET` and `BRIEF_SEAT_LEVEL=sonnet`. Routing row C7 has Sonnet post a body approved byte for byte; the security texts were drafted here, by Opus. **Default: Sonnet as written.** Alternative: Opus, which changes one word in the MODEL line and one in the launch line.
- **Q-2 Creating the ticket while the card is open.** Option c of the card files nothing, so filing now forecloses c. **Default: CREATE-Q0 = NEW**, as the commission says (a and b both file). Fill the CARD slot with `open` at the stamp; anything else stops the seat. Alternative: NONE until he rules. The records then say the item is owed, and the comment uses its HELD clause.
- **Q-3 Ticket type and priority.** **Default: Bug, Medium**, as for RD-1021 and RD-1036. The secret is masked, nothing connects, and the three roles are proposed or deferred. Alternative: High, matching the gate's "Major".
- **Q-4 Entry shape.** **Default: three entries**, C-324 (251), C-325 (choice, routes, correction) and C-326 (PR 250, not in the commission but the form's practice). Alternative: drop C-326, which leaves two entries and changes the layout numbers.
- **Q-5 Correction of the C-319/C-320 wording** ("to every config.read role" / "to every role holding config.read"; the gate measured every signed-in role). **Default: include it in C-325.** Alternative: drop the Correction clause.
- **Q-6 MOVE-1036.** **Default: `1036`** (Testing, CLAUDE.md 302). RD-1036's own acceptance says "limited to the fields the product owner approves", and the comment says plainly that the fields were not approved. Alternative: NONE, keeping it in To Do until he approves the fields.
- **Q-7 The card's wording.** The card says the route sends to "end users and the two partner roles". The table marks those roles proposed or deferred, and only the create route can store them. **Default: the ticket carries this caveat (P2) and the kit does nothing to the card.** Whether to add a line on the card is yours.
- **Q-8 HISTORY and launch.** **Default:** HISTORY = WRITE, and the cockpit line as written, with Sonnet inside the quotes.

## UNMEASURED (named)
- The local `user.email` value. Its prefix matches the hash of the previous history commit's address, but `git config` is not a drafter verb.
- Whether the product owner rules between the stamp and the seat's writes. The seat reads no card, so a ruling in that window leaves "no answer when this note was written" stale.
- The review's numbers inside the texts are RELAYED from VERDICT.md and FOR-RECORDS.md: 23 cells, 7 red, 9 roles, 17 keys, 18 fields, 14 names. I ran no jest, no server and no browser.
- The role sources beyond the two user routes (the identity provider, SCIM provisioning), and how many stored users hold each role on any instance.
- Everything the seat itself runs: its helpers, ADF builder, append, Step 7 and EVIDENCE poll.

## Checks of the kit that were not run on a real output, and what I ran instead
These STOP-severity checks were each run once on prototype output:
- (a) The project scanner in `jira` and `entry` modes over all 33 texts, alone, with sample fills and with HELD fills: 0 problems, and every control fired.
- (b) The doubled-paren and 3-word-repeat checks over every filled and HELD text: 0. This is where the first-run fault was caught.
- (c) A simulated append on scratch copies of CLARIFICATIONS.md and HISTORY.md: prefix `cmp` equal, ASCII added, layout as above.

Not run: the seat's own helpers, which do not exist yet.

## Chain inputs (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | the kit; REFUSE 1-2; READ files; the scanner copy | BASE (`.tools/b2055/scan1947.py` exists, 6267 B) |
| 1 | the text bank; the scanner; REFUSE 3 reads | Step 0; the common and jira helpers of Step 1 |
| 2 | identity read, `ls-remote`, fetch | BASE; Step 1 helpers |
| 3 | GitHub, Jira and records reads; PRIOR WORK | BASE; Step 2 |
| 4 | texts and fill-ins (placeholder key) | Step 3 |
| 5a | create payload; searches; the CARD and CREATE-Q0 slots | Step 4; the Stamp |
| 5b-5c | comment with the key from 5a (or the HELD clause); transition id | 5a; Step 3 |
| 6 | created key, comment id, line counts of the two wordings | Step 5; Step 3 |
| 7 | `entry-numbers.txt`, the section written | Step 6 |
| 8 | all logs | all |

## Outside-the-fences disclosure
- **Writes:** the kit, its `.measured` and this report. Scratch under `fleet/state/s325/d2073/` holds:
  - helpers: `jr.py` (a copy of B2055's drafter reader, its comment edited by `sed -i` in scratch), `pointers2073.py`, `bank.py`, `scan2073.py`, `build_kit.py` and `fill_sidecar.py`;
  - raw files read at `11149d3f` and `e2911754`, the two Build logs, the Jira outputs and `card.txt`;
  - the simulated appends.

  Nothing was written in any project, Jira, GitHub or the card store. No `cd`, nothing deleted, nothing sent to any human, nothing of another client.
- **Reads:**
  - NexusAI `CLARIFICATIONS.md`, `CLAUDE.md`, the STATUS files of B2043, B2055 and B2069, `.tools/b2055/scan1947.py` (bytes only, for the copy) and the `.env` key names (values only in-process).
  - The gate's clone `fleet/state/s325/g2071/clone` with `git grep`/`rev-parse` (read verbs). The local `2_Project_Files` with `cat-file`/`rev-parse` only (it is stale at `c74d1ad4`).
  - `gh api -X GET` under the NexusAI `GH_CONFIG_DIR`, and Jira GET only.
  - `decision_queue.sh show <exact id>` once, into scratch: 13 lines, the id once. No `list`.
  - `tmux list-panes`, and line 9 of the sibling B2072 kit (for R321).
- **One refused command:** the hook refused an `echo ====` separator (zsh). Nothing ran; I re-issued it with `----`.
- Not read: `briefs_staged/`, scoreboard, `_ledger.md`, WEDNESDAY/FRIDAY trees, other projects. No jest, lock, listener, deploy, az, docker, ssh.
