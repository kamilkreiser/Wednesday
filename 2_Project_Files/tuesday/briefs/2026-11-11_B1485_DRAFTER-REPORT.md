STARTABLE: YES once stamped. Nothing it depends on is still running: R203 has landed as analysis #192, D59 ended `DEPLOYED B1466:`, and no HPSM-POC pane was live at 07:27.

# DRAFTER REPORT: B1485 / SEAT-R206, HPSM-POC records (UAT deploy with schema, deploy order, round-3 moves, #306, NT-1), drafted 2026-11-11 07:22:56 to 07:33 AEDT (`date`)

## BLUF
- **What the kit asks.** The kit is 144 lines and unstamped. It asks for four entries, expected C-335 to C-338:
  - **E1:** the UAT deploy of `009421a2` with the schema step. Every figure you asked for is in it: 95=95=95, the copy `hpsmpoc-b1466-pre` with its state taken from the stamp, 3 min 45 s down, the 146 s window with 0 rows, and what is NOT shown on UAT.
  - **E2:** M1 as the standing API-deploy order, with the order actually run beside it.
  - **E3:** the B1440-3 GO on the landed head `d49be881`, which unblocks HPSMPOC-410, 417 and 438, plus NT-1.
  - **E4:** the #306 landing (HPSMPOC-466) and the #308 gate record, which C-333 lacks.
  - **Jira:** up to six comments, up to four moves and one create. Each write class has its own slot, and every write slot defaults to HOLD or COMMENT-ONLY.
- **Most of the landings are already on record. Nothing is duplicated.** Records main `fecaee17` already holds #304 (C-330), #305 (C-331), #307 (C-332) and #308 (C-333). What was missing:
  - #306, which has no entry at all ("pull request 306" reads 0).
  - That #304's landed head is now gated (C-330 says "not gated").
  - #308's gate record (C-333 has none).
  - The deploy itself ("hpsmpoc-b1466-pre" reads 0).
- **Three things go beyond your scope list. Each sits behind its own slot.**
  - **MOVE-466.** HPSMPOC-466's Done-when reads met: #306 merged, and gate B1464 names its landed head `4aff7ec`.
  - **DEPLOY-NOTES.** Comments on 117 and 100. Their last comments, R203's 40974 and 40973, carry "as read at 2026-11-10 20:14". The migration has since been applied on UAT.
  - **The NT-1 pre-create rule now names the expected hits exactly.** That rule is why R203 did not file it.
- **One open decision matters most: ORDER.** Your commissioned order, M1's own words and the order actually run on UAT are three different sequences (Q1). I wrote your words as the PROPOSED default and give a recommended replacement.

## The kit
| Item | Value |
|---|---|
| File | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1485_SEAT-R206_hpsmpoc-records-deploy-1111.md`, 144 lines (`wc -l`), sha256 prefix `9ce8d23cc09174c8` |
| Pre-stamp copy | `...1111.md.pre-stamp`, identical (`cmp`) |
| 4-underscore lines | **14** = 13 slots + the last line (`/usr/bin/grep -c -E '_''_''_''_'`; control `printf 'x\n____\n'` gives 1) |
| Slots | STAMP, LAUNCH WINDOW, JIRA, MOVE (410/417/438), MOVE-466, DEPLOY-NOTES (117/100), CREATE, RECORDS, LAND, ORDER, COPY-DB, Hard stop, Panes |
| `@..@` tokens | 0 (control `@NOW@` gives 1) |
| Name scan (underscore-aware, the 9 names of `scan1462.py:10`) | 0 hits (control `_by_Inch_` fires; `Kampala` does not). The kit points to that list rather than spelling the names out |
| Non-ASCII bytes | 0 (control 2) |
| Jira payload templates scanned | 7 payloads (410, 417, 438, 466, 117, 100, NT-1 description): 0 hits for foreign `C-n`, `Tuesday`, `gate`, `B\d{2,4}`, seat ids, URLs, `seat` (each pattern fires on a control string) |
| Seat / model | **R206, Sonnet.** `model-routing.md` line 97, row C7 (client-board comments: Sonnet drafts first and posts only bodies approved by slot). Model id `claude-sonnet-5-5` (`models_latest.json` line 23). `brief_seat.sh` line 24 defaults to opus, so the level is written inside the launch quotes. Why Sonnet: same work type as R201, R202 and R203, all Sonnet. R203 ran this exact form cleanly, and its one non-create came from the kit's own rule, not a Sonnet miss. Nothing here is a security-design or destroying-path decision (rows C3 and C4) |
| Last line | `RECORDS COMMITTED: records/b1485 @ ...` / `RECORDS PUSHED:` / `RECORDS DRY RUN ONLY:` / `HANDOVER B1485:` / `STOPPED: NEEDS TUESDAY`. All five match `status_watch.sh` line 56. I kept the house form rather than `READY B1485:` (see Q7) |
| Ports | none |

## Facts MEASURED by the drafter (instrument, clock, control)
1. **Code repo** (`gh api -X GET` under the HPSM-POC `GH_CONFIG_DIR`, 07:23:24; `gh auth status` shows the Datasec account active).
   - main = `009421a28616c8b31dde86b59d4c4ca674c288fa`. Open pull requests: 0.
   - #304 to #308 all closed and merged true, with these squashes and heads:

| PR | Squash | Head | Merged (Z) |
|---|---|---|---|
| #304 | `22116082` | `d49be881` | 05:00:48 |
| #305 | `78d4b3ce` | `792c78f2` | 04:23:18 |
| #306 | `7da797e8` | `4aff7ec4` | 05:35:30 |
| #307 | `eb2e49c7` | `c16f422e` | 06:15:29 |
| #308 | `009421a2` | `aa9bac75` | 07:10:20 |

   - #306 detail: 1 commit, 1 file `web/src/content/walkthrough/steps.test.ts`, +26/-7, parent `22116082`. Runs at its squash: `ci` 42763094804 success, `Push on main` 42763094634 success.
2. **Analysis repo** (07:23:36).
   - main `fecaee17b01cbb88f8009ca5c5b7bfd0a0509778`.
   - `CLARIFICATIONS.md`: 5978 lines, 1948121 bytes, sha256 prefix `2355482a9a5ea67f`. Newest heading `### C-334` at line 5973. Control `### C-263`: once, at line 5114.
   - Open pull requests: 0. Last three merged: #192 `fecaee17`, #191 `f32c6b7b`, #190 `92839fc7`.
   - `records/b14*` refs (07:27:59): b140, b142, b143, b1444, b145, b146, b1461, b1462, b148. There is no `records/b1485` (control: `records/b1462` is listed).
3. **Prior-work counts on records main** (`grep -c -i -F`; controls: `pull request 304` gives 4, a never-present string gives 0):

| String | Count |
|---|---|
| `hpsmpoc-b1466-pre` | 0 |
| `pull request 306` | 0 |
| `REC-DEMO-ALIAS` | 0 |
| `LedgerAuditAndFollowUpRetention` | 1 (C-332) |
| `d49be881` | 2 |
| `Customer assessment pipeline` | 2 |
| `the only measured link left under 44 px` | 1 (C-317) |

4. **Jira** (read-only REST, `.env` read in-process and never printed; scratch reader `.../scratchpad/b1485/tools/jread.py`; 07:24:29 to 07:24:49).
   - Controls: HPSMPOC-1 returns 200, HPSMPOC-99999 returns 404.
   - Board: 466 issues, highest key HPSMPOC-466. 323 Done (`statusCategory = Done`) and 143 not.
   - Per ticket:

| Key | Status | Comments | Done-when |
|---|---|---|---|
| 410 | Backlog | 40899, 40969 | "the Demo view of both pages is decided ... and the decision is built or recorded" |
| 417 | Backlog | 40625, 40709, 40898, 40970 | "each link is at least 44 px high at the sizes the gates measured, or the item is recorded as declined" |
| 438 | Backlog | 40885, 40971 | "the product owner has said whether the line names Evidence submitted too, and with which words, or ... declined" |
| 466 | Backlog, 0 comments, labels `rec-2026-11-10`, `review-finding` | none | "the row catches those forms, each with a planted string that turns it red, and the exemption is narrowed or recorded as accepted, merged to main (nothing deploys), or ... declined" |
| 117 | Backlog | 40906, 40912, 40974 | no done-when line |
| 100 | Backlog | 40905, 40911, 40973 | no done-when line |
| 324 | Done / Done | not yours | not yours |

   - JQL results:

| JQL `text ~` | Result |
|---|---|
| `"11NOV"` | 0 |
| `"REC-DEMO-ALIAS-10NOV"` | 0 (control `REC-RUL-6-10NOV` gives 180, 117, 100) |
| `"Demo" AND "alias"` | 9 keys: 450, 410, 388, 387, 374, 373, 370, 297, 125 (the same set R203 read) |
| `"\"Customer assessment pipeline\""` | 1 key: HPSMPOC-457 (phase 2 dashboard rebuild; its row P2-030 names the panel as "Currently"; related, not a duplicate) |

5. **Code lines for NT-1 at `009421a2`.** Measured with `contents?ref=` raw and `awk NR`, 07:26.
   - PartnerDashboard.tsx: 163 (the panel title is at 143).
   - CustomerManagement.tsx: 112, 118, 297, 333.
   - customer/EngagementsList.tsx: 67.
   - customer/DocumentGeneration.tsx: 172.
   - customer/ApiSteps.tsx: 100.
   - customer/FirmwareTask.tsx: 49, 122.
   - playbook/SnapshotLauncher.tsx: 127, 128.
   - Each line holds the name it is cited for, and they equal R203's lines. Note the directories: R203's payload names files only, and my first fetch under guessed folders returned 0 bytes until I read the tree. The kit gives the folders.
   - `steps.test.ts` at main: row title at line 99, `EXEMPT` at line 105.
6. **Verdicts** (`wc -l`, `shasum -a 256`, `head -1`):

| Verdict | Lines | sha256 prefix | Line 1 |
|---|---|---|---|
| B1440-3 | 25 | `9b20533241d4da46` | `GATE B1440-3: GO @ d49be88 on main 009421a` |
| B1442 | 103 | `1b69d5fb298293b3` | same file R203 cited; M1/m1/m2 at lines 82/83/84 |
| B1464 | 50 | `b91ea4d5c0aef55d` | `GO WITH FINDINGS @ 4aff7ec` |
| B1463 | 102 | `962a41ffc10e2f36` | `GO WITH FINDINGS @ aa9bac7` |

   - B1440-3 also has rows 1-5 of no severity and row 6 Minor.
7. **Files on disk:**
   - B1466 STATUS: 271 lines, `471cc9447a830ff1`.
   - B1462 STATUS: 109 lines, `93d5cd2e6222f480`.
   - `nt1_not_filed.json`: 9 lines, `ea2b16384301a836`; its summary is 255 characters and the kit's is byte-equal.
   - B1466 STATUS line numbers the kit cites, printed by `grep -n -i -F`: 15-21, 52, 130, 139, 149/151, 170-185, 200, 213, 216, 219, 222, 231-233, 261, 271. The B1466 kit's slots S2 and S16 are at lines 686 and 727.
8. **Panes** (`tmux list-panes -a`, 07:27): %0 wednesday, %1 fleet-monitor, %2 Datasec/NexusAI-N122. No HPSM-POC pane.
9. **The project root is the analysis repo** (`origin` = HPSM-POC-analysis), and its local `origin/main` is stale: `e7986dc0`, against `fecaee17` on GitHub. This matters for Q7.

## RELAYED (in the kit, not re-measured by me)
- **Every deploy figure, from B1466 STATUS:** the window times, 95=95=95, max id 122, the checksum, 3 min 45 s, the 146 s / 170 s window, 0 rows in the window, packages, deployment ids, the SEEN table, PART F with 9 items, the way back, NOT TESTED.
- **Two items from R203 and the deploy record, not re-read by me:** `compare 6b0c5f2c...009421a2` (ahead 5, 46 files, +7788/-105) and CI 42773429652 success at the target. The kit marks both RELAYED.
- **The authority, from the B1466 kit S2 (line 686):**
  - The 19:40:52 ruling: "Deploy all five to UAT now, with the database update".
  - Its detail line.
  - The terminal line "go ahead and deploy to UAT".
  - The card id is not written in the kit.
- **The window-order choice:** S16 = `A: START PREV THEN DEPLOY` (line 727), plus ADDENDUM-2 and ADDENDUM-3 as summarised in B1466 STATUS.

## IN / OUT of this kit (your item 6)
| Owed item (source) | IN/OUT | Reason |
|---|---|---|
| B1466 FT 1: UAT at `009421a2`, migrated, copy, exposure | IN (E1) | core scope |
| B1466 FT 2: plain-words note for the product owner | OUT | a message to a human is yours; seats send none |
| B1466 FT 3: tables | IN (E1, relayed) | |
| B1466 FT 4: deploy C-entry with the schema step; landing entries for #304-#308; M1 as the deploy order with ADDENDUM-2/3 | IN (E1, E2, E3, E4) | #305 and #307 are fully in C-331/C-332, so they are cited and not repeated. #304 and #308 get only what C-330/C-333 lack (gate rounds). #306 gets a full entry |
| B1466 FT 5: copy DB billed until deleted | IN as state only (COPY-DB slot) | deletion is the product owner's (your card); the seat writes the stamp's sentence and never acts |
| B1466 FT 6(a): Demo pipeline panel, 4 names | IN (NT-1 + E1/E3) | added to R203's NT-1 payload |
| B1466 FT 6(b): D-13 census | IN (E2) | it is the reason start-then-deploy is tolerable |
| B1466 FT 6(c)-(f): tooling notes | IN as notes in E1, no ticket | deploy-tooling, no Jira home |
| B1466 first-stop FT 4: the "fifth clause" | IN (E2, as the window's limit) | superseded by ADDENDUM-3 but still describes the window |
| B1462 hand-off 1: move 410/417/438 once a verdict names `d49be881` | IN (MOVE) | B1440-3 is that verdict |
| B1462 hand-off 2: NT-1 | IN (CREATE) | pre-create now names the expected set exactly |
| B1462 hand-off 3: CI red at the #305 and #304 squashes | OUT | already in C-330/C-331. Later runs on main are green; no recurrence measured, so no flake ticket yet |
| B1462 hand-off 4: deploy order M1 | IN (E2) | |
| B1462 hand-off 5: E5 Minors unfixed and unticketed | OUT | no new fact; fix or ticket is your call |
| B1462 hand-off 6: eyebrow, breadcrumb, way back still read "My readiness" | OUT for a decision; pointer kept in E4 "Not settled"; the UAT eyebrow is SEEN in E1 | product word |
| (found) #306 landing and HPSMPOC-466 | IN (E4, MOVE-466) | no entry existed; the Done-when reads met |
| (found) #308 gate record missing from C-333 | IN (E4) | append-only supplement |
| (found) 117/100 comments are stale | IN (DEPLOY-NOTES) | R203's comments say "applied to no hosted database as read at 20:14" |

## D-decisions the drafter made (change any)
- **D1. Four entries, not five.** NT-1 sits inside E3, as R203 put it inside its E1. #306 and the #308 gate record share E4 because both are landing records the entries lack.
- **D2. NT-1 is created FIRST**, so the 410 comment can name its key. R203's order forced "listed in entry".
- **D3. The NT-1 pre-create is an expected-set rule:** {450, 410, 388, 387, 374, 373, 370, 297, 125} for Demo/alias and {457} for the pipeline phrase. A key outside the set is a STOP; a key inside is not. NT-1's label is `rec-2026-11-11`; its marker `REC-DEMO-ALIAS-11NOV` is new, and `REC-DEMO-ALIAS` reads 0.
- **D4. Edits to R203's NT-1 description:** "rounds 1 and 2" (F3/F4 sit in both verdicts), one UAT sentence, a Related line (410, 457), and the entry number. Also "C-330" is dropped, because the scan bans foreign C-numbers in Jira; R203's payload would have failed its own scan under my numbers.
- **D5. MET for 410/417/438 keeps R203's rule** (file:line at squash `22116082` plus a verdict naming the landed head), with GO from B1440-3. 417 also needs C-317's sentence printed once.
- **D6. E2 records and does not rule.** Its order text comes only from the ORDER slot, attributed to "the coordinator". The as-run order and its proofs sit beside it.
- **D7. The database name `hpsmpoc-b1466-pre` is a named exception** to the entries' brief-number check (a planted bare `b1466` must still fire).
- **D8. The Jira texts use "stored customer names".** The deploy record says "real customer names"; these are seeded sample customers, and the house wording is "stored name".

## Q-questions for Tuesday (each with a default)
- **Q1. ORDER (the one that matters).** Three sequences exist:
  - Yours: backup, stop, migrate, deploy, start, identity, checks.
  - M1's words: stop, migrate, deploy, start, identity.
  - As run on UAT: stop, then backup (so no write is in flight), migrate, identity, start the OLD build, deploy onto the running site. The 146 s window came from this, and S16 = A was chosen because a deploy onto a stopped site has no record here.
  - Kit default: `PROPOSED` = your words verbatim. E2 then shows the as-run differences beside it, and a reader sees "backup then stop" standing against "stop then backup" as run.
  - **My recommendation: stamp a replacement**, e.g. "stop the API; back up the database (a copy proven equal plus the restore point); run the migration on that database only; run api-identity.sql; deploy the API; start it; live checks and a schema read-back; never Down. A deploy onto the stopped API is not yet proven on this platform; until a deploy seat proves it, starting the previous build first and deploying onto the running site is allowed, with that build's multi-row audit saves failing atomically in the window."
- **Q2. MOVE (410, 417, 438).** Default COMMENT-ONLY; my recommendation is **CLOSE-IF-MET**. B1440-3 is GO at `d49be88`. For 417, its earlier links were built by #272/#278 (comments 40625/40709), and C-317 records the logo link as the only measured link left.
- **Q3. MOVE-466.** Default COMMENT-ONLY; my recommendation is **CLOSE-IF-MET** (#306 merged; gate B1464 GO WITH FINDINGS at the landed head; the six forms are pinned with planted reds). Its F1 is three extra mutants the ticket did not ask for. This is beyond your list; strike it with COMMENT-ONLY if you want the commission exact.
- **Q4. DEPLOY-NOTES (117, 100).** Default HOLD; my recommendation is **WRITE**. Their newest comments describe the migration as not applied, which is now false on UAT. Neither ticket has a Done-when line, so neither is ever moved by this kit. Note that 117's summary says the ledger "is absent on Azure SQL", and UAT now has it. Whether that closes 117 is a product call; it needs a Done-when or your word.
- **Q5. CREATE.** Default HOLD; my recommendation is **CREATE**. The expected-set rule removes R203's stop, and no ruling exists either way, which is exactly what the ticket says.
- **Q6. COPY-DB.** Write whatever the product owner's card says at the stamp (kept / deleted at hh:mm / pending). Default if unruled: "kept, billed until deleted; deletion awaits the product owner's word". The seat never touches Azure.
- **Q7. Last line.** I used the house `RECORDS COMMITTED: records/b1485 @ ...` rather than `READY B1485:`. Both match the watcher. But `status_watch.sh` `records_check` resolves `records/b1485` in the repo holding the STATUS file. That is the project root analysis checkout, whose `origin/main` is stale (`e7986dc0`) and which holds no `records/b14xx` ref (`records/b1462` is not local either). **Expect it to print "NOT FOUND" for a true claim.** Verify by `gh api -X GET repos/datasecau/HPSM-POC-analysis/pulls/<n>`, as for R203.

## UNMEASURED / NOT MEASURED by me
- Whether a deploy onto a stopped API site works on this platform: nobody has measured it.
- Whether anyone used UAT in the 146 s window (UAT keeps no request log).
- The ledger verification procedure.
- A restore of the copy.
- The current state of the copy database, and the product owner's card on it (I read no card).
- The deploy figures themselves: relayed, not re-measured.
- The Jira `Done` transition id per key, and createmeta for type 10030 (not re-read; the seat re-reads both).
- CI at `009421a2` and `compare 6b0c5f2c...009421a2` (relayed, labelled so in the kit).
- Whether `PartnerDashboard.alias.test.tsx` at the landed head affects anything beyond B1440-3's rows (the gate says test-only; I did not re-read the diff).

## Outside-the-fences disclosure
- **Written:** the kit, its `.pre-stamp` copy and this report. Scratch, in the session scratchpad `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/d570c861-638f-4956-b457-814e46e42365/scratchpad/b1485/`: `clar_main.md` (a raw copy of records main), `tree.txt`, `src/*.tsx` and `steps.test.ts` (raw reads at `009421a2`), and `tools/jread.py`, `jcomments.py`, `jdesc.py` (read-only Jira GETs; the token was never printed).
- **Nothing written** in the HPSM-POC folder, Jira or GitHub. No decision card read; no `decision_queue.sh`; no ledger, scoreboard or `briefs_staged`; no az, docker, ssh or hosted HTTP.
- **Git in the project:** `config --get remote.origin.url`, `rev-parse` and `--no-optional-locks` read verbs only, on the project root and on `.tools/b1462/analysis`.
- **Commission vs DRAFTER_RULES:** the rules name `/Volumes/Laptop-DEV/...` paths and a `cockpit.sh add` launch form. I used `/Volumes/Datasec_DEV/...` and the `launch_when_cool.sh` form, as the precedent kit and the commission do.
- **Three commands refused or failed, with no effect:**
  - One `cd` was refused by the hook.
  - One `echo ====` was refused by the zsh hook.
  - One `grep -P` is not supported by BSD grep, so I re-ran the count in python with a control.
- **One correction made in the kit before saving:** the `compare` figures were first labelled MEASURED-BY-DRAFTER and are now RELAYED. I also replaced an explicit ban-name list in the kit with a pointer to `scan1462.py:10`.
