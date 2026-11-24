STARTABLE: YES

# B2041 DRAFTER REPORT: kit SEAT-R314, OXPd 2 owed item 114 (the Azure lines of CLAUDE.md)

## BLUF
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-24_B2041_SEAT-R314_oxpd2-r-claudemd-azure.md` (48140 bytes, sha256 ff0978bf… at 13:39:50). Sidecar `.measured` beside it: 63 claims, 63 measured, `stamp_check.py` exit 0.
- It does exactly three record writes: (1) ONE exact-string edit of `CLAUDE.md` lines 58 to 62 (89 lines before and after; lines 58, 59, 60 and 62 change; line 61 is byte-equal); (2) the tick of owed item 114, with one `Closed:` line under it; (3) one history entry of 7 lines. No C-entry, no Jira call, no Azure call.
- The fix for B2040's hold: TEXT CLAUDE-NEW quotes his C-81 note as two verbatim spans taken by program, under the heading "his word". The narrowing comes after, as a SEPARATE sentence marked **"The coordinator's practice, not his word:"**. The spend sentence is marked "the coordinator's reading, told to him on the board, not his word (C-81)". The sentence-by-sentence who-decided table is in the kit's THE AUTHORITY (S1 to S8).
- Seat id R314 is free. A word scan (`grep -l -w`) of the 53 non-`.pre-`, non-`.measured` SEAT kits of 2026-11-23 and 2026-11-24 found R314 in 0 files; the control R313 was found in 1.
- Slots: STAMP, LAUNCH WINDOW, BASE, RECORDS (default HOLD), Q-ANSWERS, STOP-CHECKS, Hard stop, and the READ-WHOLE last line. That is 8 `____` lines (kitcheck.py).

## Facts re-measured (instrument; control)
- **Base files equal B2040's READY.manifest** (`shasum -a 256` at 13:32:18 and again at 13:39:50):
  - CLAUDE.md 1a2e5629…
  - BACKLOG.md bcb9c741…
  - history.md 1a2da4f7…
  - CLARIFICATIONS.md bda1e11c…
  - the register e2621f1b…
- **B2040's last line** is `READY B2040: 92715942… | C-83 | … | CLAUDE.md left`.
- **Owed item 114** (BACKLOG.md):
  - It is at line 824, as the commission says.
  - Its Discovered line is at 830, and 115 starts at 831.
  - The anchor heading is at 853.
  - There are 117 owed lines, numbered 1 to 117 with no gap (regex).
  - `Closed: ticked in place` count: 33. `- Discovered:` count: 117 (control).
- **C-81** (`texts.py`):
  - The heading is at line 902 (the commission's 902 is the heading). The answer line with his note is at 930.
  - The note is 140 characters. It starts `create a new resource group` and ends `issue new steps so agents have full control to spin up and create services/ vms etc`, each once.
- **C-82 and the spend reading:**
  - C-82's heading is at 980. The "Leave it" answer line is at 994 and ends `: b, Leave it`.
  - C-81's spend sentence (`anything over about A$50 a month is put to him first`) is at line 978, once.
- **The project scanner** (`b1785.scan_record`, via importlib):
  - On the whole C-81 note it gives `['S-NAME']`, because the note holds his login address. That is why the kit quotes the two spans and not the address (Q1).
  - On all 8 written texts it gives 0 problems, both unfilled and with the prototype fill. There are 0 bytes above 126.
  - Controls fired: `filed_by_kamil_` gave S-NAME, and a coordinator path gave S-COORDPATH.
- **The commission's VERIFY (f):**
  - history.md holds `the first Azure run of OXPd` on 1 line, line 11, in B2034's entry, relayed from the B2031 STATUS (control: `(records seat)` 13).
  - BACKLOG item 112 (the first real device run) is still `[ ]` at line 809 (control: `113. - [x]` at line 816).
  - The project Briefs folder holds 86 `_STATUS.md` files, with B2040 the highest.
  - history.md has 0 lines with `simulator`. Every records entry's NOT-done line says nothing was run on the printer (7 lines).
  - B2021's STATUS says "The lab's write has still not run against a device".
  - So "No agent has run anything on a printer, a simulator or a Microsoft 365 tenant yet" holds at drafting. The kit's P-6 re-checks it at the seat's run.
- **Dry builds** (in scratch, never written to the project):
  - CLAUDE.md: sha256 ce5c1f69…, 11941 bytes, 89 line feeds, changed lines exactly [58, 59, 60, 62].
  - BACKLOG: 868 → 869 line feeds; the anchor moves 853 → 854.
  - history: 305 → 312 line feeds.
- **Panes:** `tmux list-panes -a` shows `%0 tuesday` and two unnamed panes. There is no `Datasec/OXPd2-` pane.

## D-decisions (the drafter's)
- **D1:** The new CLAUDE.md sha256 is a STOP-on-difference prediction (ce5c1f69). The edit has no fill-in and P-2 pins the base.
- **D2:** The kit gives line 58 the wording "any spend, but as the Azure sentences below say", and line 59 the wording "any Azure resource outside the resource group `oxpd2-dev-rg`". The rest of the file's rule stays.
- **D3:** "His own sign-in stays in `4_Credentials/.azure`" is his ("Leave it", C-82). "never by his sign-in" sits inside the coordinator's practice. C-82 records the agents' own folder as "the coordinator's arrangement".
- **D4:** "nothing outside that group" is in the practice sentence, with the measured refusal from the boundary proof (history, AuthorizationFailed).
- **D5:** No HP, Jira or Azure step is in the kit. The two login folders are named, never opened, listed or hashed.

## Q-questions for Tuesday (each with a default; also in the kit as Q1 to Q5)
- **Q1:** Should S2 quote the note as two verbatim spans, leaving out the address between them? The default is yes, because the whole note fires S-NAME in the project scanner. Alternative: quote the whole note with a scanner exception.
- **Q2:** Should line 58 read "any spend, but as the Azure sentences below say"? Default: as frozen. Alternative: keep "any spend" unchanged.
- **Q3:** Should "reports each resource when it is made" sit in the coordinator's practice, as the commission's (b) asks? C-81 records it as part of the spend reading told to him. Default: as frozen.
- **Q4:** Line 62 as frozen, with P-6 re-checking it at the run? Default: yes.
- **Q5:** No C-entry and no new owed item? Default: yes. I found no C-entry owed.

## Chain table (every step's inputs exist at BASE or come from an earlier step)
| Step | Inputs | Produced by |
|---|---|---|
| 0 | kit, sidecar, the five project files, the scanner | BASE |
| 1 | the b2040.py and b1785.py models (read), scratch copies | BASE; Step 0 |
| 2 | THE SOURCES, the manifest, the Briefs listing | BASE |
| 3 | the frozen texts, the before-copies, the scanner copy | the kit; Step 0 |
| 4a | the live CLAUDE.md, CLAUDE-OLD and CLAUDE-NEW | BASE; the kit |
| 4b | the live BACKLOG.md, BL-CLOSE-114 filled with the CLAUDE sha8s | BASE; Step 4a's prints |
| 4c | the live history.md, the H-texts filled with the sha8s and the clock | BASE; Step 4a; `date` |

## RAN / NOT RUN
- **RAN** (scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s322/b2041/`):
  - `texts.py`, which builds the texts and the dry builds and runs the scan;
  - `kitcheck.py`, which re-parses the 9 texts from the written kit: all equal, and a one-character mutant differs;
  - `sidecar.py`;
  - `stamp_check.py` exit 0.
- **The scanner** is the project's own `b1785.py`, not a list of the drafter's.
- **NEVER RUN:**
  - the seat's `b2041.py` and its selftest;
  - HOLD R and R2 on the live files;
  - the tick proof on the live file.

## UNMEASURED
- Whether the product owner has accepted the coordinator's practice (S5) or the spend reading (S6). The kit says it is NOT recorded.
- Whether he has made Azure resources himself in `oxpd2-dev-rg` since the boundary proof. Line 62 speaks only of agents.

## Outside-the-fences disclosure
- **Read-only reads:**
  - the project's CLAUDE.md (whole), BACKLOG.md ranges, CLARIFICATIONS.md C-81 to C-83 and lines 1 to 4, and history.md lines 1 to 33;
  - B2040's STATUS (whole) and its READY.manifest, and B2031's STATUS (grep lines);
  - b1785.py's scanner section (sed). It was loaded by importlib, which executes its module top level. That is the same as B2040's drafter did, and it makes no request.
  - EXPIRING-GRANTS.md, grep lines for the Azure row (row 9; the commission names it). Line 14's row was printed incidentally.
  - `models_latest.json` lines, model-routing.md line 98, the stamp_check.py header, and `brief_seat.sh` line 24.
- **Writes:**
  - the kit, its sidecar, and this report;
  - scratch under `fleet/state/s322/b2041/` (texts.py, texts.json, kitcheck.py, sidecar.py, the dry builds, stamp_check.out, and `measured.v1.quarantine`, the first sidecar, moved there with `mv` after I corrected two line pointers in the kit; not deleted).
- **Not done:** no Jira call, no az, no gh, no git verb in any project repo. No write in the project folder.
- **Hook refusals:** two Bash calls were refused by hooks (a `cd`, and an unquoted `=====` separator) and re-issued without them.
