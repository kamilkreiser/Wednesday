# B1790 and B1791 drafter commission -- Datasec / MPS Commercial Calculator: two build kits, one drafter each
Commissioned by Tuesday (seat s299), 2026-11-20. Drafter model: Sonnet (routing row C8). You DRAFT one kit; you build nothing, run no test, and write nothing outside your own files.

**You are ONE of two drafters. Your launch prompt names your lane. The lanes share no file.**

| Lane | Brief | Seat | Ticket | Files the build seat OWNS (RELAYED from today's sweep: re-read at code main) | Gate tier (Tuesday's) |
|---|---|---|---|---|---|
| M-1 | B1790 | M169 | MPSCALC-314 (a minimum gap between autosaves) | `web/src/screens/quote/autosave.ts`, `web/src/screens/QuoteScreen.tsx`, and the tests `autosave.test.ts`, `autosave.b456.test.ts`, `QuoteScreen.autosave.test.tsx` | G2 |
| M-3 | B1791 | M170 | MPSCALC-418 (the infra test cannot see the value of an expression setting) | `infra/tests/test_infra.py` only | G2 |

## Authority and sources (read each at source; nothing here is the product owner's ruling)
- Standing grant: the product owner's words to work the backlog (live board 2026-11-19 16:26:43, "keep working on other outstanding tickets and the backlog"). No deploy, no customer-facing word, nothing to any person.
- The project's rules: `/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/CLAUDE.md`, WHOLE.
- The ticket, whole, by Jira GET (description and every comment). Quote its scope sentence and its acceptance check in the kit.
- Today's sweep, your lane's row and its STOP list: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_SWEEP-EVENING_datasec-backlog-refresh.md` (section JOB 2). Its file lines and blob shas are RELAYED: re-measure every one.
- **M-1 only: the decision is TUESDAY'S, as coordinator, under the ticket's own text; it is never written as the product owner's.** Read it in `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_SWEEP-1630_TUESDAY-ANSWERS.md` (the paragraph on MPSCALC-314): a minimum gap between saves in the web autosave only; 10 seconds as the default, a named constant beside `AUTOSAVE_QUIET_MS`; a change made inside the gap is never lost (one trailing save when the gap ends; a save at once on leaving the screen, on blur of the window, on unload and on an explicit save); the quiet interval is not changed; the server is not touched. **Measure before you freeze it, and STOP the kit with a Question if either is true:** (1) the screen shows a saved mark while a change is pending inside the gap (no new customer word is added by this lane); (2) an existing test pins one save per quiet interval in a way the gap must change: list every such cell with its file and line (a by-program census), because the kit must name each changed expectation.
- **M-3 only:** the kit needs a working standalone `bicep` in the seat. Read how the file finds it and whether one exists on this machine (print the path or say none; do not install anything). No real tenant id, client id or host name is written into a test: planted values are obviously fake. `az` is never called. Each new row is shown RED first by a planted change of the expression it guards.

## What exists (measured by Tuesday today unless marked)
- Code main of `datasecau/MPS-Commercial-Calculator` is `debb5e28f7bbd4e0f641a829eb353ac356afdd81` (pull request 222; 8 of 8 check runs success; 0 open pull requests; read by GET at 17:40 AEDT). Your kit's BASE is main as YOU read it.
- A records seat (`Datasec/MPS-R284`, kit B1781) is writing Jira MPSCALC and the root record files now. Your reads are GET only. Neither lane touches a file it touches.
- No MPS build seat runs. The local `2_Project_Files` checkout is stale (RELAYED): the seat works in its own clone under `.tools/<brief>/`, as the last build seats did.

## Deliverable
The kit `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_<BRIEF>_SEAT-<SEAT>_mps-<short-name>.md`, its `.measured` sidecar, and `2026-11-20_<BRIEF>_DRAFTER-REPORT.md` beside it. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s299/d<brief number>/`. Write to disk as you go.
**Form:** the newest stamped MPS build kit, `2026-11-20_B1775_SEAT-M168_mps-part-codes-round2-oracle-boundary.md` in the same folder (read it whole, in pages of at most 100 lines, for the FORM and this project's build rules: the marks, the closed lists, REFUSE AT ONCE, the heavy lock, STANDING LINES, HOLDS, the PRIOR-WORK CHECK, Questions with defaults, the Stamp slots, the launch line with `BRIEF_SEAT_LEVEL=sonnet`, STATUS as the channel, READY with a pushed branch and NO pull request; its project facts about part codes are another change's and are NOT yours). Follow `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/DRAFTER_RULES.md` whole (where it names /Volumes/Laptop-DEV the volume is /Volumes/Datasec_DEV).
**Rules of today, each binding on your kit:**
1. Keep the kit under about 80 kB. Sum the bytes of the kit plus every file its READ WHOLE list names and print the total in your report; a Sonnet seat must be able to carry it (aim under 300 kB in all). Tuesday's own stamped kits are never on a seat's READ WHOLE list.
2. Tell the seat: long files are read with `offset` and `limit` in pages of at most 100 lines; a Read refusal is a page-size message, not the context band; a HANDOVER for context cites the statusline figure.
3. If a pointer table writes a slash for a source line's pipe or a single quote for its backtick, its heading says so.
4. Every count by program; a number that counts a list in the same sentence is produced from the list; every test selector is checked against the test names it must match, and the kit tells the seat to STOP on a run of 0 tests; every predicted output is UNMEASURED unless you measured it (you run no test).
5. Who decided: every choice in the kit is written as the coordinator's or as the ticket's own text, with its source; no sentence puts a decision in the product owner's mouth.
6. A census of the tests that pin the OLD behaviour (by program), so the seat knows which expectations change and which must stay green untouched.

## How
Read-only everywhere except your kit, its sidecar, your report and your scratch folder. `gh` under `GH_CONFIG_DIR='/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator/4_Credentials/.gh-config'` (check `gh auth status` first, print no account name; every call `-X GET`; read files at main through the API or a tarball in your scratch, and run nothing from inside it). Jira GET only (credentials by name, in-process, from the project's `4_Credentials/.env`, never printed). No git write anywhere. No `cd` (a hook refuses it); zsh (no PIPESTATUS); absolute single-quoted paths (the project path holds a `!` and spaces); never delete (quarantine with `mv`). Clocks from `date` in the same command. `Source_Documents/` is never opened. Nothing of the HPSM project or of any other client is read or written.
First line of your reply: `STARTABLE: YES|NO - why`. Then, in at most 20 lines: the files; the Questions with defaults; the census of tests that pin the old behaviour; corrections to this commission and to the sweep's row (say plainly where either is wrong); the byte total of the kit's reading load; the UNMEASURED list; what you did not read.
