STARTABLE: YES (after your stamp; no blocker. PORT BLOCK TAKEN: 9720-9729 for B1044, so B1045 must take another one: 9760-9769 and 9780-9789 also scanned clean at 13:4x)

# B1044 drafter report (Opus 5.5 drafter, 2026-11-01 about 13:38 to 13:53 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1044_SEAT-M62_nexusai-rd912-roster-reads.md` (112 lines, sha256 `9381da181c78364db46c9910f2d3065ca189f8ffdb30aec5cb81bc765f1b4126` before any stamp). It has 9 four-underscore lines: 8 slots plus the last line (MEASURED). `@[A-Z_]+@` tokens: 0 (control line: 1). Non-ASCII bytes: 0 (`python3 -I`). Person-name scan `kam|kreiser|wednesday`: 0 (control `tuesday`: 20). Card-id scan: 0. I wrote no `.pre-stamp` copy (the drafter rules allow two files only), so cut one before you stamp if you want it. Seat **M62** (`Datasec/NexusAI-M62`). Repo `datasecau/Reporting_Dashboard_Au`, project `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI`.

## BLUF
Seat M62 makes one commit on a new branch `b1044/nexusai-rd912-roster-reads` from main `89375808`. The commit adds one shared helper, `keepRosterRows`: an inserted block of 5 lines just before `pickUserCapture`. It keeps only the object rows of a list and returns anything that is not a list unchanged. The helper wraps three fresh reads in `backend/server.js`:
- **7314**: the email/follow-up branch. It feeds `.some` at 7315, which gives HTTP 500.
- **7334**: the read passed to `generateUserActivityAnalysisForUser`. It throws at 9862, which gives the handled error text. It also feeds the last-print handler at 10052.
- **10185**: the sibling's roster read. Its map at 10186 throws, which gives "I couldn't identify which user".

The diff shape is 4 hunks, +8 -3, rehearsed in scratch with `node --check` passing. There is one new test, `F3`, in ONE NEW `describe` appended after Group F of the rd869 file (additions only). Counts go from 5267/311 to 5268/311. Red-first at main, then 8 mutants (MX is the one recorded expected survivor). The model is Sonnet, row C2 (line 92). The seat pushes its own branch only: **no PR**. It **never touches `package.json` or `package-lock.json`** (B1045's lane). **A merge to main that touches `backend/server.js` triggers `deploy-demo.yml`.** Today the run skips: repo variables 0, environments `["dev"]`, and the last Deploy demo run at `88144175` was `skipped`. Landing is yours.

## Facts re-measured (instrument; control)
- **Main** is `8937580841a39123f32955c3df067af01544418e`. `gh api -X GET git/ref/heads/main` and `git ls-remote origin` agree. The sweep's `89375808` is confirmed.
  - `compare 88144175...89375808`: ahead 2, `HISTORY.md` only, so the code is the #147 merge.
  - `compare a4a227dc...89375808`: ahead 4. Files: server.js +1, rd869 +28, counts +2 -2, HISTORY.md.
  - The tree read gave `truncated` false, 1022 entries.
- **Blobs at main:**
  - `server.js` `b673c3b4`, 22411 lines (`git hash-object` of the raw GET). This is the blob B1018 pushed.
  - The rd869 file `e2b95919`: 675 lines, 35 `test(` sites, 8 describes.
  - The counts file `7680a3ff`: 5267/311.
  - `package-lock.json` `050c1a2a`.
- **The sweep's lines hold** at `b673c3b4`. The ticket's pointers at `88144175` are also valid: 7314, 7315, 7334, 9862, 10185, 10186, 10207, the catch 9960-9962, and the route's catch 7424/7445.
  - The census of `getAllPrinterLogs({ limit: 1000 })` gives 12 lines, the same 12 the ticket lists (control: `getAllPrinterLogs` gives 53).
  - `keepRosterRows` gives 0 (control: `Array.isArray(` gives 22).
- **Correction to the commission's ":7315 -> 500" reading:** B1023's arm appended the empty entries AFTER the real rows, and `.some` at 7315 stops at the first match. So with that arm the 7315 path would NOT throw. That explains why the ticket says it is "read from source, not run". The kit's arm is `nullfirst`, which returns `[null, undefined].concat(real)`, so 7315 really meets the empty entry. The follow-up's HTTP 500 at main is PREDICTED, and stays UNMEASURED until the seat's red-first run.
- **The 7314 path is reachable without an email in the seed.** The 16 seed users are all two-word names with no `@`, MEASURED from `scripts/seed/demo-printer-logs.csv` shapes only, with no name printed. A follow-up question about the conversation's current user takes `checkForCurrentUserQuery` 8036-8063, which leads to route branch 7311 and the read at 7314. The kit asks `how much has <derived user> printed?` and then `when did <derived user> last print?` in the same conversation. The last-print handler text `The last time ${userName} printed something was on ` (10112) is the reach control.
- **The sibling needs a plant, so a new describe is needed.** The sibling's lost user (10185) only shows for a rostered capture that is not valid without the roster. The seed has no such user, so `Admin` must be planted.
  - The test file's own comment at lines 498-499 says plants must precede the boot's first question.
  - Group F asks 10 questions in its `beforeAll`.
  - So F3 gets its own boot, in a describe placed directly after Group F (D4). The ticket said "beside F2 in the describe at 570" (Q-3).
- **Consumers filter per user.** All consumers of the three reads filter by user (9861, 9899, 10052, 10208, 10245, 7315). Dropping non-object entries therefore never changes a user's rows, and object lists come back with the same elements in the same order.
  - Scratch `node` run of the helper: object lists keep identity and order; `[1,2]` and `["Admin"]` become `[]`; `null`, `undefined` and `{}` are returned `===`; `[null]` gives `[]`; `[a,null,undefined,b]` gives `[a,b]`.
  - Control: an identity helper keeps `[null]`.
- **Anchors.** The single-line texts are not unique: the 7314 text occurs 5 times, the 7334 text 12 times, the 10185 text 2 times. The kit gives two-line anchors, each with a measured count of 1.
- **Counts and CI predicate:**
  - The counts file is 5267/311 (`_updated` 2026-10-31T19:10:11.623Z). Expected after the change: 5268/311.
  - `build.yml:83-84` runs the verify gate. `verify-suite.sh:343` fails on `-lt`, `:354` on `-gt`, and `:366` prints `VERDICT: PASS`.
  - `build.yml` triggers are lines 3-9: PR to main and push to main only.
  - `npm-audit.yml:8-12` runs on push to any branch.
  - Main runs at `89375808`: Build success, Gitleaks success, npm-audit failure (RD-913).
- **deploy-demo.yml:** the push to main has `paths-ignore` `**.md` / `docs/**` / `tests/**` (lines 26-32); build `if` at line 53, deploy `if` at line 91, `environment: demo` at line 95. `actions/variables` `total_count` is 0 and environments are `["dev"]`.
- **Landing rule:** C-190, `/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md:2062`, with `:2067` "Never squash, never rebase" and the second-threshold addendum below line 2076. It is a merge commit of the same commit, quoted in STANDING LINE 9. Jira Testing comes from NexusAI `CLAUDE.md:302`.
- **Open PRs and branches:**
  - Open PRs: 0 (control: `pulls/99999` gives 404; the closed list is #148/#147/#146).
  - 406 remote heads, 29 of which match `b8*|b9*|b1[0-9]*|records/*`, all `ahead_by` 0 (control: `compare de5d8bb5...main` gives 10).
  - `matching-refs/heads/b1044` gives 0 (control: `b1018` gives 1).
  - `session-tools/b1044*` and `worktrees/b104*` are absent (count 0). The `b1018` trees exist.
- **Seat name:** `M62` word-bounded over `tuesday/briefs/*` gives 0 files before this kit (control: `M60` gives 21). `M61` also gives 0 files; I did not take it, because you assigned M62.
- **Ports:** block 9720-9729.
  - `/usr/sbin/lsof -nP -iTCP:9720-9729 -sTCP:LISTEN` gives 0 (control: all listeners give 14).
  - A word-bounded scan of the 74 non-`.pre-` SEAT kits of 10-31 and 11-01 gives 0 hits for 9720-9729 (control: 9630 gives 6, the B1025 block).
  - 9760-9769 and 9780-9789 also gave 0/0. 9740-9749 has 15 kit hits and 9630-9639 is B1025's.
- **Live panes** (`tmux list-panes -a`, 13:44): tuesday, Datasec/ATTIO-R113, Datasec/Security-Composer-R112, fleet-monitor. No NexusAI pane.
- **Model:** `model-routing.md:92` C2 (Sonnet first). `:93` C3 was considered and rejected. Gate `:109` G2, cap `:111`. `models_latest.json:23` gives `claude-sonnet-5-5` (checked 13:27:30). `brief_seat.sh:24` defaults to opus, so the launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- **Lock tool** sha256 is `cf01bafb...4971f` (unchanged). `locks-laptop-1017` exists. load1 was 2.35 at 13:48.
- **Jira** (GET only, `session-tools/b774/b774lib.py` under `python3 -I`; control `RD-99999999` gives 404): RD-912 and RD-913 read whole, 0 comments each.
  - `project = RD AND ( text ~ "7334" )` gives 2 (RD-912, RD-910).
  - `project = RD AND ( text ~ "9862" )` gives 1 (RD-912).
  - `project = RD AND ( text ~ "getAllPrinterLogs" )` gives 12, all older (RD-61 to RD-337). None of them is about empty entries.
- **Relayed, not re-measured:** B1018's STATUS (43/43 rd869 and the 15 neighbour suites at 291/291 at `cc665c02`, which carries the same server.js blob) and B1023's verdict "GO WITH FINDINGS (round 1 of 2)" with its isolation-probe figures (seeded user, null on every read, gives the handled 9862 text in down and stand-in modes).

## D-decisions (mine, in the kit)
- **D-1:** One helper at the three reads, not guards inside each consumer. Cleaning the read covers 9862, 9899, the last-print filter 10052 and 10186. M34 proves the last-print path too.
- **D-2:** RD-910's lines 8088-8089 stay byte-equal. The helper repeats their predicate rather than replacing them (Q-2).
- **D-3:** The helper returns a non-list unchanged. Otherwise a non-list read at 7334 would move from the handled 200 to the route's 500. That branch is pinned by no cell, and mutant MX is the recorded survivor.
- **D-4:** F3 goes in its own describe with its own boot. Admin is planted before the first ask, and the empty entries go FIRST. It is one test, so the counts move by one, as the ticket says.
- **D-5:** Out of lane, census only: 7275's fallback read, 10207's fallback read, and the six sites the ticket did not examine (8181, 8220, 9446, 10377, 13956, 14073).
- **D-6:** Times are 150/240 minutes, as for B1018. B1018's own run took 77 minutes; this one has 8 mutants against 5, and the verify runs are about 26 minutes each.

## Q-questions for Tuesday (each with a default)
- **Q-1 Model:** Sonnet, C2 line 92? Default **YES**.
- **Q-2 Scope:** helper plus 7314, 7334 and 10185 only; RD-910's 8088-8089 untouched; the fallback reads 7275/10207 and the six unexamined sites OUT (census in FINDINGS)? Default **YES**. The other choice is to also route 8089 through the helper. That gives one predicate in one place, but it edits a landed, gated line and invalidates B1018's mutant table.
- **Q-3 Cell placement:** a new describe directly after Group F with its own boot (one more server boot, about 15 s), against the ticket's "beside F2 in the describe at 570"? Default **YES**. Inside Group F the Admin plant would come after 10 asks, and the file's own comment (498-499) says that does not work.
- **Q-4 Gate:** G2 (line 109, Sonnet first)? Default **G2**. The mechanism was measured by B1023, and no finding changes which user an answer shows.
- **Q-5 Times and ports:** 150/240 minutes, block 9720-9729 reserved and unused? Default **YES**.
- **Q-6 Landing order against B1045:** the two lanes share no path, so land in whichever order their gates finish? Default **YES**. B1045 landing first is listed in the kit as an expected main move (not a stop). The seat records that its verify ran on the older lock. The npm-audit red on this branch is expected until RD-913 lands.

## UNMEASURED
- The follow-up's HTTP 500 at 7315 at main. It is predicted from source; this kit's `nullfirst` arm is the first run of it.
- Whether `working / sibling` ("show me admin's activity" with Admin planted in a fresh boot) is answered by the sibling with Admin's activity in this new boot. This is RELAYED from the round-2 group at lines 492-528 (P3). The kit's reach controls stop the seat if it is not.
- Fired figures per armed row (predicted: 2/1/2 at main, 2/2/2 after).
- The neighbour suites at `89375808`. They are relayed from B1018's head, where only the rd869 file and the counts differ from today's main.
- The hosted Build, Gitleaks Scan and CodeQL for the future PR. Stand-in and Azure modes are not in the cell.
- Which seats will be live at launch. Only 4 panes were up at 13:44, and B1045's pane is expected.

## Outside the fences (disclosure)
- I wrote only the two files. Scratch files under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f8947a38-04ac-46b8-96f3-ceebf0948b77/scratchpad/b1044/` hold raw GETs, a scratch copy of the edited server.js, a helper check script, the Jira reader and the refs lists. Nothing there is in a project tree.
- No `decision_queue.sh` in any form. No ledger, staged-briefs, scoreboard, WEDNESDAY or FRIDAY reads. No non-Datasec project.
- Git in the project: `ls-remote` only (`--no-optional-locks`). `gh` was `-X GET` only, under NexusAI's `GH_CONFIG_DIR`. No hosted HTTP, no az, ssh or docker.
- One command was refused by the zsh-wordsplit hook (an `=====` separator). It was re-run with `----` and changed no state.
