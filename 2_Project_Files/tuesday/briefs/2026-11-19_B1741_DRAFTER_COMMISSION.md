# B1741 drafter commission — MPS lane M-G: MPSCALC-195 + MPSCALC-316 (SEAT-M163)
Commissioned by Tuesday (s293), 2026-11-19. Drafter model: Sonnet (routing row C8). You DRAFT a kit; you build nothing.

Draft ONE builder kit `2_Project_Files/tuesday/briefs/2026-11-19_B1741_SEAT-M163_mps-lane-mg-accepted-wording.md`
(+ `.measured` sidecar; return the drafter report as TEXT in your reply, Tuesday saves it) in the FORM of
`2026-11-19_B1732_SEAT-M162_mps-lane-mf-importer-doc.md` (read it whole, and the builder STATUS of that lane in the MPS
project's `1_Project_Definition/Briefs/2026-11-19_B1732_STATUS.md`, Corrections first). Follow
`2_Project_Files/tuesday/DRAFTER_RULES.md` whole (where it names /Volumes/Laptop-DEV, the volume is /Volumes/Datasec_DEV).
Project folder: '/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' (verify by listing the parent).

AUTHORITY (read it at source and quote it in the kit): the project's `1_Project_Definition/CLARIFICATIONS.md` entry C-108
(heading at line 2707 when this was written: re-find it by its heading): the product owner accepted, on 2026-11-11, "the
drafted engine-target sentence" (MPSCALC-195) and "the agreed '100 characters, an emoji counts as two' sentence in the
remaining places" (MPSCALC-316; the agreed sentence is the one of entry C-64: find C-64 and quote the sentence byte for
byte). Both tickets were commented and left open "LATER": the build is what is owed. Read both tickets whole by Jira GET
(the MPS `.env` names are JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN), every comment included (comments 41070 and 41071
are the records pass's). Source of this lane: `2026-11-19_SWEEP-1630_datasec-backlog-unblock.md` (the M-G section;
measured this afternoon: re-measure every file and line at MPS main, print the sha).

SCOPE: exactly the two accepted wordings, placed where the tickets and C-108 say.
- MPSCALC-195: the drafted engine-target sentence: find the DRAFTED sentence (in the ticket, its comments, or C-108's
  sources), quote it byte for byte with its source, and name the one place it goes. If you cannot find the drafted
  sentence word for word, that part is STARTABLE: NO; say so and draft the kit for MPSCALC-316 alone.
- MPSCALC-316: every remaining place that still states the old limit (the sweep says some still say "100 characters"
  without the agreed sentence): enumerate them BY PROGRAM across the whole repository (code, docs, tests, web, samples),
  state the frame and look outside it once, and class each: (a) takes the agreed sentence byte for byte; (b) a place the
  sentence does not fit as written (an identifier, a test title, a log line, a different limit). Class (b) is NOT edited
  by this lane: list it for Tuesday.
- TUESDAY'S ANSWER on the sweep's question 1 (a default under the standing backlog grant, not the product owner's): the
  API error string the sweep found in `QuoteEndpoints.cs` (line 1436 at the sweep's read) is text a user can see. It is
  in scope ONLY if the accepted C-64 sentence fits there byte for byte (C-108: "in the remaining places"). If it would
  need ANY other word, a shortened form or a new sentence, it is class (b): not edited, listed, and it becomes a words
  question for the product owner. Print the current string and say which class it is and why.

REQUIRED CONTENT: THE WORDS frozen in the kit with the source line of each; an old-answer census BY PROGRAM of every test,
snapshot, fixture and doc that pins the OLD text of each edited place (each: rewrite / unaffected), with its control;
the predicted diff shape MEASURED on a scratch copy (`git diff --stat`), never estimated; expected test counts quoted
from a real run or marked UNMEASURED; the project's own landing rule quoted from its CLAUDE.md or CLARIFICATIONS.md
(MPS lands by head-pinned squash; hosted CI and CodeQL, 9 checks on the last pull request: re-read the number); gate
recommendation G2 Sonnet unless an edited place is on a security or pricing path (then say which and recommend G1);
PRIOR-WORK CHECK (what MPS #49, #182 and the 2026-11-11 records pass already did for these two tickets); no customer
word beyond the two accepted wordings (anything else is a STOP); every choice not in C-108 written as Tuesday's default.
Count test cells as INDENTED lines too and print the column-1 count beside it.

HOW: read-only everywhere except your kit, sidecar and scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1741/`.
GitHub: the MPS project's own GH_CONFIG_DIR (its `4_Credentials/.gh-config`; verify the account before the first call;
every call `gh api -X GET`; repo datasecau/MPS-Commercial-Calculator). Git read verbs only in the project checkout
(`--no-optional-locks`); a scratch clone or `contents?ref=<sha>` reads for anything else. Jira GET only, credentials in
process, never printed. You MAY run the MPS test suites in your own scratch copy ONLY if the form kit's lane did so
without a project lock; otherwise mark the figures UNMEASURED. No server, no request to any app host, no deploy, no az.
No `cd`; no unquoted word starting with `=`; zsh; absolute paths; never delete; clocks from `date`.
Run `python3 -I -B /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/tools/stamp_check.py <kit>` (must exit 0); leave
every Stamp slot unfilled. ASCII; build whole, temp file, os.replace.
First line of your reply: `STARTABLE: YES|NO - why`. Then: files, recommended slots, the class (a) and class (b) lists,
corrections to this commission, D/Q defaults, UNMEASURED.
