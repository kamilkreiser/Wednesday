STARTABLE: YES (after your stamp; wave 2, its dependency HPSMPOC-374 is in main as #245. Two stale branches share paths and need your exemption (Q-6); the printed pack stays unrestyled unless you say otherwise (Q-3).)

# B957 drafter report (Sonnet 5.5, 2026-10-30 about 17:00 to 17:45 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B957_SEAT-H77_hpsmpoc-379-tabs.md` (148 lines; 9 four-underscore lines = 8 slots + the last line, counted by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0; non-ASCII lines 0 by a `python3 -I -B` scan; the HP-tools STOP paragraph present verbatim, checked by program). Read-only everywhere else; `gh api -X GET` under the project `.gh-config`; Jira GET only (HPSMPOC-379 and -91, read whole); no `cd`, no hosted HTTP, no ref written, no message. I wrote nothing in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H77` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet`), ports 9860-9869, branch `b957/hpsmpoc-379-tabs` off main `332dcc6f`. Edits four files (`FirmwareTask.tsx`, `DocumentGeneration.tsx`, `ConversationCoach.tsx`, the screen panel of `ClientPacks.tsx`), adds four `*.restyle.test.tsx`, changes NO existing test (all six have 0 class assertions, measured). Content (six template JSON, `packs.ts`, `templates.ts`) and by default `PackView.tsx` are byte-equal by sha256. The export and print proof is by program: 5 document types plus packs 1 and 3, five artefacts each (copy payload, printed `innerText`, `pdftotext` of the print PDF, page count, printed `outerHTML`), base vs head, 28 hash pairs. Model C2 (line 92), gate G2 tier 2 (line 109), both re-read; `models_latest.json` line 23 `claude-sonnet-5-5`.

## Sweep pointers found WRONG or incomplete (what is true)
1. "0 shared files, 0 open PRs": true for open PRs now (5 open, 0 shared; a planted control reads 1), but **two stale live branches share your paths**: `b97/gate-b99-notes` (tip `f0fcf36c`, 2026-10-02, 3 ahead 164 behind; FirmwareTask and its test) and `b97/internal-notes` (tip `976589a9`, 2026-10-02, 13 ahead 165 behind; ClientPacks.test, packs.test, packs.ts, four template JSON). The wave-2 rule says a shared path is a STOP, so the kit exempts them only by name and tip sha if you stamp Q-6.
2. Row H18 says "(+ tests)" and AC 1 allows class assertions to change: there are none (0 `className`/`toHaveClass` in all six test files), so the kit holds all existing tests byte-equal.
3. `app/(app)/coach/page.tsx` and `documents/page.tsx` are 8-line wrappers that hold only the page title; the restyle lives in the components. The kit expects them byte-equal. The real tab routes (`customers/[customerId]/{tasks/firmware-risk,documents,coach}/page.tsx`) are not in the sweep; they are 8-line wrappers too and stay unchanged.
4. The sweep calls the document "export"; the app has no HTML export (the design does). Export here is the print dialog, the clipboard payload and the service PDF link. The kit proves exactly those.
5. Content width: the frame's rail makes the column 762 px at 1280, yet all three screens switch to two columns at VIEWPORT widths (`xl:`, `xl:`, `lg:`). That is the real layout risk of this lane; the kit makes it D-5 with six widths (adds 1180).

## Facts re-measured (instrument; control)
- Main `332dcc6f3324158cc6b2d7297aa9ef47cfd33f94` (`commits/main`, 06:14:30Z). Open PRs #248, #250-#253: per-PR file lists intersected with the 23 lane paths: shared 0 each. `compare e21d8044...332dcc6f`: 40 files, 0 yours. 22 `refs/heads/b9*` read by `compare/main...<b>`: 20 clean, the 2 stale above. `matching-refs heads/b957` = 0; ports 9860-9869 free (`lsof` 0); `.tools/b957` absent; panes at 17:16: no H77. Load1 6.71.
- Sha256 prefixes and line counts of the 23 paths are in the kit (python scan of the extracted tarball); non-ASCII per character counted.
- Print is already pinned by `playbook-print.spec.ts` (177 lines; has a `B75_EVIDENCE` PDF mode); `pdftotext` exists at `/opt/homebrew/bin/pdftotext`. The new proof reuses them.
- Coupling: `DocumentGeneration` renders H17's `ReportPreview`, `ServiceReport`, `ApiNarrative` helpers; `ClientPacks` imports `latestReport` and `WITHHELD_LINE` from `ServiceReport`. No shared file, but H17 landing first changes the printed generated document: the kit compares base and head at the SAME main and re-runs the print proof if one of those files moves.

## D-decisions (mine, in the kit)
D-1 base `332dcc6f`, no merge step. D-2 no existing test changes. D-3 the five Tasks anchors stay anchors (the design's tabs hide the other parts). D-4 radios stay radios. D-5 breakpoints re-tuned against the content column at six widths. D-6 print held unchanged by not touching what prints. D-7 shared `ProgressBar` replaces the hand-rolled bar (existing aria value row must pass). D-8 no word changes. D-9 no committed spec; scratch spec. D-10 target READY 210, hard stop 300.

## Q-questions for Tuesday (words first, each with a default)
- **Q-1 (customer-facing words, the product owner's):** any new or changed word? Default **NONE**: the multiset program must print removed 0 added 0. The design's "Export HTML report", its "future integration" hint and its advisory line are NOT adopted (phase line).
- **Q-2 (phase line):** keep the Firmware task's PLACEHOLDER, SAMPLE and "coming soon" labels at least as visible, add no status or figure, with a deny-list word program on added lines. Default **YES**.
- **Q-3:** may the printed pack (`PackView.tsx`) and the print-visible markup be restyled? Default **NO, byte-equal** (print must be unchanged; the ticket lists PackView, so it is your call).
- **Q-4:** the five Tasks anchors drawn as a tab strip but staying anchors (no `role="tab"`, no state). Default **YES**.
- **Q-5:** target READY 210 and hard stop 300 minutes. Default YES.
- **Q-6:** exempt the two stale branches by name and tip sha (never touched). Default **YES**; if you say no, the kit STOPs at the intersection.
- **Q-7:** gate round: round 1 of 2 on the class "tabs restyle". Default YES.

## UNMEASURED
Layout at any width; the print layout after the restyle; `pdftotext` determinism; axe on the new look; suite counts; Chromium availability; the stale branches' diffs (the kit orders the builder to read them).

## Reasons not to launch now
Machine load (6.71 at 17:16, 12 seats; use `launch_when_cool`, load1 < 7). If H17 (B956) is about to land, launching H77 after it avoids a mid-build merge, but nothing blocks launching first. Pane name `-H77` re-checked free at 17:16.

## Outside-the-fences disclosure
No fence breached. Scratch (tarball extract, PR and branch file lists, a symlink `m` to the extract) is under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/8a8e5624-4358-43cb-ab64-af03ddbc5b41/scratchpad/drafters/b957/`. Two Bash calls were refused or mis-parsed by hooks (a `cd`, an unquoted `=====`, and an unquoted heredoc whose backticks ran as commands and printed "command not found" lines); none had an effect beyond a failed edit that I redid with a quoted script.
