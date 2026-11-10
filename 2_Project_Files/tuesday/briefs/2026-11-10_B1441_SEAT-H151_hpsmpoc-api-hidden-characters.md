From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail; a launch message that names a mailbox is overridden). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file; **UNMEASURED** = nobody has.

**LAUNCH ONLY AFTER B1394 (seat H144, lane L3 API) is READY and landed** (its STATUS last line `READY B1394: <sha40>` AND its pull request merged to main). Tuesday stamps the branch point as the main that holds it.

# BRIEF B1441 | SEAT-H151: HPSM-POC, BUILDER (SONNET): L3 API FOLLOW-ON, THE PRODUCT OWNER'S 10 NOV RULING ON HIDDEN CHARACTERS. NEW BRANCH `b1441/hpsmpoc-api-hidden-characters` FROM MAIN 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb. COMMITS AS NEEDED, PLAIN PUSHES OF THAT REF ONLY, NO PR. NOT MERGED, NOT DEPLOYED.

**BLUF:** API follow-on of lane L3 for the product owner's 2026-11-10 ruling, option (a) "Refuse invisible-only names; file names fold width/space only" (its detail: "Settles 324 and 257. Agent builds with tests that fail first."): **HPSMPOC-324** (a customer name in which no character is visible is refused, as a blank name is) and **HPSMPOC-257** (the feedback file-name device check folds width and white space only, no longer the full compatibility fold). Branch `b1441/hpsmpoc-api-hidden-characters` cut from main 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb (main was `fa401da9f7bdab21c46ad9717c964433a2d22650` at drafting, 2026-11-10 03:36 AEDT by `gh api -X GET repos/datasecau/HPSM-POC/branches/main`; B1394 lands before you launch). **Model: SONNET** (model-routing.md line 92, row C2: the design is ruled and the edit is spelled out below, so it is not row C3's design surface; model id `claude-sonnet-5-5`; the level is written inside the launch line). **Size: S-M (each ticket S).** Seat id H151. Ports **9950-9959** only. Your STATUS: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1441_STATUS.md`. First step is to **re-read main and close with evidence anything main already fixes**; then fix only what is still open.

**Launch (Tuesday):** `WED_USAGE_STOP=100 bash /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add Datasec/HPSM-POC-H151 "BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100 bash '/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/brief_seat.sh' '/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC' '<this kit's path>'"`. `brief_seat.sh` defaults to Opus (line 24); the level is written inside the quotes.

## READ WHOLE FIRST (read-only)
1. The lane plan: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_sweep_drafts/lanes.md` (the BLUF, "Rules every lane carries", the CI predicates, section L3). **Every file:line in it or here is a pointer you re-print with `grep -n` at your own clone.**
2. The kit of the lane you follow: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_B1394_SEAT-H144_hpsmpoc-api.md` and its STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1394_STATUS.md` (HPSMPOC-99 N-8, the invisible-only comment residue, is its item and touches the same classifier: read what it changed).
3. The project's `CLAUDE.md` and `JIRA.md` (read-only), and `.github/workflows/ci.yml` of your clone (print the `api` and `api on SQL Server` predicates into STATUS).
4. The gate notes the tickets cite, read-only, on disk: `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-22_B478_STATUS.md` (around line 128) and `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-10-13_B243_STATUS.md` (around lines 107 and 114). Missing on disk: say so and read the ticket text only.

## BINDING HOLD
UAT is on hold and HPSM-POC deploys nothing: no `az`, no docker push, no ssh, no HTTP to any hosted, demo, UAT or production host. **You open no PR; Tuesday lands it through CodeQL (never bypass, never dismiss).** No Jira write; no message to any human. Never delete (quarantine to `.tools/b1441/_quarantine/`); no force-push, amend, reset or rebase. **Never type `cd`.** **No migration** (neither ticket needs one; a need for one is a STOP). This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only. **No new product words:** the refusal reuses the existing problem code and message named below; a need for any other words is a STOP for that item.

## STEP 0: RE-READ MAIN, THEN CLOSE WHAT MAIN ALREADY FIXES
1. Clone by URL into `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1441/repo`, check out `origin/main`, print `git rev-parse HEAD`, compare with 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb, name every commit since fa401da9 that touches your files, and check B1394's squash is an ancestor (`git merge-base --is-ancestor`, rc printed; missing: STOP).
2. Each ticket: `STILL OPEN` / `PART FIXED` / `FIXED AT MAIN`, read at your main. A fixed one: `CLOSED-WITH-EVIDENCE HPSMPOC-<n>: <what main shows> | <file:line by grep -n at <sha8>> | <instrument> | <control>` in STATUS, never in Jira.

## THE TICKETS (scope quoted from Jira at drafting 2026-11-10 03:3x AEDT by the drafter's read-only REST GET; both Backlog, 0 comments)

### HPSMPOC-324: a customer name with nothing visible is refused
- Jira summary, quoted whole: "[B478-6] A customer name of only U+200B is accepted and stored: needs a product-owner decision"
- Jira done-when line, quoted: "Done when: the product owner's decision is recorded on this ticket; if it changes what the API accepts, the change is built with a test that fails first."
- Where at fa401da9 (MEASURED by the drafter, `grep -n` over the raw file): `api/src/HpsmPoc.Modules.Assessment/Endpoints/CustomerEndpoints.cs:79` (create) and `:198` (update) each read `if (string.IsNullOrWhiteSpace(body.Name)) return Problems.Unprocessable(http, "customer.name-blank", "name", "name is blank.");` (the ticket's `:77,196` were read at an older main). The classifier that already decides "nothing visible" for a feedback comment and a file name: `FeedbackEndpoints.IsInvisible` (used at `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackFiles.cs:198`: `if (!name.EnumerateRunes().Any(r => !FeedbackEndpoints.IsInvisible(r))) return null;`).
- Do: at both lines, a name in which no rune is visible is refused with **the same** `customer.name-blank` / `name` / `"name is blank."` (no new code, no new words). Reuse the classifier; if the Assessment module cannot reference the Feedback module (read the project references and say so), move or share it only inside `api/src/**` with a `NEEDS TUESDAY` line in STATUS (not the last line) naming the choice before you commit. Check how the earlier hidden-character ruling's shape check (`Shape.Customer`, the line above 79) treats the same input and say in STATUS which rule now refuses each row, so no input is refused twice with two different codes.
- Tests that fail first (in `api/tests/**`, NOT `Hpsmpoc178CustomerNameTests.cs`, which is L4's: a new class): create and update each with U+200B alone, U+200B U+2060, the Braille blank U+2800, a Hangul filler, and two controls (a visible letter plus U+200B is accepted; plain spaces are refused as today). Each refused row reads 422 with the existing code; red at main, green at your head.

### HPSMPOC-257: file names fold width and white space only
- Jira summary, quoted whole: "[B243 N-6] DECISION FOR KAM: feedback file names: the NFKC fold refuses names Windows does not reserve (LPT + superscript 4, COM + superscript 0, CON + fullwidth full stop)"
- Jira option text, quoted: "Options (from B243's fix-shape): (a) fold width and white space only; (b) keep NFKC and exempt superscripts other than 1-3; (c) keep it as built and accept the over-refusal. Whichever is ruled, a test row pins it." **The ruling is (a).**
- Where at fa401da9 (MEASURED by the drafter): `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackFiles.cs:136` `internal static IEnumerable<string> DeviceStems(string name)`, `:138` `yield return StemOf(name).TrimEnd(' ', '.');`, `:139` `yield return StemOf(name.Normalize(NormalizationForm.FormKC)).TrimEnd();`. The reserved set (`Reserved` declared at line 125, its superscript entries at line 129, printed by the drafter's `awk NR` at fa401da9; re-print) already lists `COM¹`..`LPT³` literally, so superscripts 1 to 3 stay reserved without the compatibility fold.
- Do: replace the compatibility fold at `:139` by a fold of **width** (the fullwidth forms U+FF01 to U+FF5E to their ASCII counterparts, U+3000 to a space) and **white space** (every white-space character to a plain space, then the trailing trim as now) only. Write the fold as a small named function with its own unit rows.
- The rows the ruling decides (each a test row, red or green at main as printed): `LPT` + U+2074 + `.txt` and `COM` + U+2070 + `.txt` are **accepted** (201; refused at main); fullwidth `ＣＯＮ.txt` and `CON` + U+00A0 + `.txt` stay **refused** (the width and white-space folds still reach them); `COM¹.txt` stays refused (the reserved set). **`CON` + U+FF0E + `txt`**: U+FF0E is a fullwidth form, so a width fold makes it `CON.txt` and it stays refused, although the ticket lists it as an over-refusal: build the ruled words as they read, pin the row as refused, and write one line in STATUS `FOR THE RECORDS SEAT: CON + U+FF0E stays refused under the ruled width fold` (DERIVED by the drafter; you confirm by the test). Every existing file-name test row stays green or is named in STATUS with why it changed (a row that pinned the compatibility fold for a superscript other than 1 to 3 changes by the ruling; any other change is a STOP).

## PARTITION (from both sides; the property: you edit a path only if an OWNS line names it)
**OWNED by you (L3 API follow-on), only these files and new test files:** `api/src/HpsmPoc.Modules.Assessment/Endpoints/CustomerEndpoints.cs`, `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackFiles.cs`, `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackEndpoints.cs` (only if the classifier must be shared), new test files under `api/tests/**`.

**NOT yours:**
- **B1442 (seat H152, HPSMPOC-100 and 117, may run at the same time as you)** owns: `api/src/HpsmPoc.Modules.Assessment/Persistence/**` (migrations included), `api/src/HpsmPoc.Modules.Assessment/Endpoints/PersonalDataEndpoints.cs`, any new file it names, `infra/sql/api-identity.sql`, `infra/README.md`. Disjoint from your files by name; the open-PR re-read below catches any surprise.
- **The rest of `api/**`**: owned by L3 (B1394, landed before you); you touch nothing else in it. `api/tests/HpsmPoc.Api.Tests/Assessment/Hpsmpoc178CustomerNameTests.cs` is L4's.
- **L1 web UI and its follow-on B1440 (seat H150)**: web/src/components/**, web/src/app/**, web/src/content/**, web/src/server/mock/** (B1440 mirrors your 324 refusal in the mock), web/src/styles/**, web/src/assets/**.
- **L2 web server and lib (B1393)**: web/src/server/** except mock, web/src/api/**, web/src/lib/**, web/src/data/**, web/src/design/**, web/src/instrumentation.ts, web/src/proxy*.
- **L4 CI and tooling (B1395)**: .github/**, infra/** (B1442 takes `infra/sql/api-identity.sql` and `infra/README.md` after L4 lands), scripts/**, web/scripts/**, web/e2e/**, and the test files lanes.md names.
- **L5 documents (B1396), drafting kit B1443, records (B1397 R197, B1444 R201)**: ANALYSIS repository and Jira only.
- **Owned by no lane:** every path in no OWNS line. A need for one: `NEEDS-SHARED <path> <why>` and continue.
- **Open PRs:** re-read `gh api -X GET repos/datasecau/HPSM-POC/pulls?state=open` at Step 0 and before every push; a file of yours in one is named and left.

**Any other shape:** prove it by an OWNS line or STOP that item with `NEEDS-SHARED <path> <why>`.

## CHECKS (print each predicate from your clone's `ci.yml`; lanes.md read them at fa401da9, RELAYED)
- `api`: `dotnet test HpsmPoc.slnx -c Release --no-build` plus "the 10 Azurite tests ran and passed, by name".
- `api on SQL Server (<part>)` and the roll-up `api on SQL Server`: the same tests on SQL Server. **Does it run on SQL Server as CI does?** Run the classes you touched and the feedback attachment classes on SQL Server the way CI does, and say how (container image and version, connection form). A change green on SQLite and red on SQL Server is red.
- Run at **main** and at **your head**, compared by program (passed / failed / skipped per project). A red that is not yours is named with its cause at main too.
- **Every new test row is proven RED with your fix removed (in a copy) and GREEN with it.**
- **PRIOR-WORK CHECK (standing line):** `git log --oneline -n 12 -- <each file>`, `git grep -n` for `IsInvisible`, `FormKC`, `name-blank`, the open PRs, and "Jira not searched". A READY without `## PRIOR WORK` is returned unread.

## HOUSEKEEPING
- Project dir `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC`; never `2_Project_Files/` or another seat's `.tools/b1NNN/`.
- **Clone `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1441/repo`** by URL `git@github.com:datasecau/HPSM-POC.git`, key `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/3_Access_Keys/github_deploy_rw` as repo-local `core.sshCommand`. `GH_CONFIG_DIR=/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/4_Credentials/.gh-config`, `-X GET` only.
- **Ports: 9950-9959 and nothing else** (a SQL Server container's host port counts). `lsof -nP -iTCP:9950-9959 -sTCP:LISTEN` prints 0 rows before any listener. At drafting (03:39 AEDT): 0 rows for 9940-9969 (control: 15 listeners machine-wide); 0 of the 47 non-`.pre-` SEAT kits of 9 and 10 Nov name 9940-9969 (control: `9939` found in 2). The block Tuesday named, 9740-9799, is held by the MPS kits B1400 to B1405.
- STATUS `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/1_Project_Definition/Briefs/2026-11-10_B1441_STATUS.md`: FIRST line `PROGRESS B1441: b1441/hpsmpoc-api-hidden-characters HOLD`; `WORKING: <part>` lines; sections `## PRIOR WORK`, `## CLOSED WITH EVIDENCE`, `## HELD`, `## NOT RUN`, `## FOR THE RECORDS SEAT`, the change list, each ticket's rows (input, status at main, status at head), each check with predicate and counts. **LAST line on finish exactly `READY B1441: <head sha40>`** (equal to `git ls-remote` of the branch), else `STOPPED: NEEDS TUESDAY <one question>`.
- **HARD STOP: 15:15 AEDT 2026-11-10** (absolute AEDT, Tuesday writes it). Push as soon as a ticket is green.
- Commits: plain ASCII, no B-numbers, no person names, no seat ids; end with your session's attribution line. `git push origin b1441/hpsmpoc-api-hidden-characters` only.
- Shell: no `cd`; absolute single-quoted paths; `git -C`; `python3 -I -B`; `/usr/bin/grep -i` with a positive control for every count.

## REFUSE AT ONCE (last line `STOPPED: NEEDS TUESDAY`, one question; items 1 and 2 before the clone)
1. `/usr/bin/grep -c -E '_''_''_''_'` of your copy prints 0 on the STAMPED copy (the unstamped copy reads 6: the HARD STOP, four Stamp slots, the last line; control: a planted line adds 1); `/usr/bin/grep -o -E '@[A-Z_0-9]+@' <copy> | wc -l` prints 0; the last line is `READ-WHOLE-BY-TUESDAY: DONE ...`.
2. `tmux display -p -t "$TMUX_PANE" '#{@cockpit_name}'` is not `Datasec/HPSM-POC-H151` (control `-t %1` differs); `pwd -P` is not `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC`.
3. `gh auth status` fails under the project's `GH_CONFIG_DIR`, or `pulls/99999` is not 404 (control: `pulls?state=open` 200).
4. The branch `b1441/hpsmpoc-api-hidden-characters` exists on origin, your clone is dirty, B1394's STATUS last line is not `READY B1394: <sha40>` or its squash is not in your main.
5. `df -g /Volumes/Datasec_DEV` under 25 GiB; a listener outside 9950-9959.
6. A file you must change is owned by another seat or in an open PR: STOP that item (`NEEDS-SHARED`).
7. Any password, token or cookie value visible: "a value was shown", first in STATUS, STOP.

## HOLDS
No new problem code and no new message text. No migration. No claim the ticket's own option (a) means more than its words; where the words and the ticket's examples disagree (CON + U+FF0E), the words are built and the difference is written for the records seat. No Jira write.

## STANDING LINES
PRIOR-WORK CHECK (above). No message to any human. Jira writes: none. Never delete (quarantine). This phase builds no integration with HP tools (Security Manager API, Fleet Threat Assessment, firmware tools, SIEM); next-phase items are stored and architected only. Landing: "The landing form is a head-pinned squash" (CLARIFICATIONS at records main, line 3617, printed by the drafter's `grep -n -i` at 03:38 AEDT); Tuesday lands, you never merge.

## Stamp
Tuesday stamps; leave every slot as it stands. `6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb` is replaced everywhere it appears.
- STAMP: Tuesday (s262), 2026-11-10 11:13 AEDT. Kit read whole (93 lines). The MAIN slot token was replaced everywhere by 6b0c5f2caefedf47c940c9c5287dd9e358ae7cbb (code main at 11:12, `gh api -X GET`; it holds B1394's squash as #302 856d15d1, plus #298-#301 and #303). MEASURED by Tuesday at 11:12: `compare fa401da9...6b0c5f2c` touches none of your OWNS files nor B1442's; open PRs 0; branch b1441/hpsmpoc-api-hidden-characters absent (404); ports 9950-9959 0 listeners (control: 12 machine-wide). Changed since drafting: UAT now runs 6b0c5f2c (deployed 10:48-10:50 by another seat), so the BINDING HOLD's "UAT is on hold" sentence is history; YOUR hold is unchanged: you deploy nothing and touch no hosted host. B1442 (H152) is stamped to run beside you.
- LAUNCH WINDOW: 11:13-11:45 AEDT 2026-11-10
- Hard stop (absolute AEDT, one clock): 15:15 AEDT 2026-11-10
- Panes and live seats at the stamp: %0 tuesday; %1 fleet-monitor; Datasec/HPSM-POC-R201 (%44, records: analysis repo + Jira only); NexusAI N114-N117; Security-Composer-C90; MPS M101, M102, M104, M106, M110. B1442 (H152) launches beside you.

READ-WHOLE-BY-TUESDAY: DONE (s262, 11:13 AEDT, 93 lines)
