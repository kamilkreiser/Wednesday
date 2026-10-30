STARTABLE: YES (after your stamp; wave 1, no dependency open. H3 is already in main, so no merge step. One existing test line must change (Q-1) and two wording points need your word (Q-2, Q-3).)

# B944 drafter report (Sonnet 5.5, 2026-10-30 about 14:55 to 15:30 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B944_SEAT-H69_hpsmpoc-373-lists.md` (150 lines; 9 four-underscore lines = 8 slots + the last line, counted by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0; non-ASCII lines 0 by a python scan; the HP-tools STOP paragraph present verbatim, checked by program). Read-only everywhere else; gh `-X GET` under the project `.gh-config`; Jira GET only (HPSMPOC-373, -399, -401, -402, read whole); no `cd`, no hosted HTTP, no ref written, no message. I wrote nothing in the project's Briefs folder. (I made a stray `.pre-stamp` copy by mistake and moved that one file out to the drafter scratchpad (b944/stray.pre-stamp) at once; the real .pre-stamp is yours to make.)

## BLUF
Seat `Datasec/HPSM-POC-H69` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet`), ports 9750-9759, branch `b944/hpsmpoc-373-lists` off main `7365165d`. Edits `CustomerManagement.tsx` and `EngagementsList.tsx`, adds two `*.restyle.test.tsx`, changes ONE line of one existing test. Stage chips replace the Stage filter select; both lists get a `ProgressBar` named "N of M steps"; both tables take the `ui/Table` class constants; the row-actions menu becomes `position: fixed` (same DOM, so Tab order holds) so the last row's menu is fully visible at 1024 px. Model C2 (line 92), gate G2 tier 2 (line 109), both re-read.

## What PR #244 (H3, `7365165d`) means for this lane
Four files only: `customer/parts.tsx` (`StagePill` wrapper `whitespace-nowrap` -> `md:whitespace-nowrap`), `ui/Table.tsx` (`thClass`/`tdClass` gain `max-md:px-1`, `thClass` gains `max-md:tracking-normal`; `rowHeadClass` inherits), and their two tests. For us: the Customers table is `hidden md:block`, so the `max-md:` parts never reach it, but its phone cards render `StagePill` (now wrapping) and need an overflow proof; the Engagements table shows at every width, so at 390 px it gets the compact head and cells and a wrapping pill: proof required. The kit says: import the constants, never copy their strings; do not edit either file; STOP and ask if a primitive must change.

## Sweep pointers found WRONG or incomplete (what is true)
1. Row H4 / AC 4 "the Demo role still sees aliases": neither list file, `directory.ts` nor `useDirectory.ts` contains any alias logic (0 hits for `alias`); both lists print `r.name` raw. Alias handling (`useCustomerShownAs`) lives in the customer frame, heading and metrics pages. So AC 4 is held only by not changing names. The kit forbids adding alias logic and has the seat prove names equal at base and head (D-10, Q-5).
2. The "stage select" is the Stage FILTER select (lines 196-199), not a column cell. The existing unit row `CustomerManagement.test.tsx` line 57 drives it as a combobox, so AC 1 "existing tests unchanged apart from class or layout assertions" cannot hold to the letter (Q-1).
3. The directory has no answered count (`DirectoryRow` and `CustomerSummary` carry none), so the ticket's fallback applies: the figure is the existing "N of 8 steps" from `journeyProgress`. "Answered of 16" is an API ask for the PR body.
4. Template pointer: B935 uses `LC_ALL=C /usr/bin/grep -P` for non-ASCII; macOS `/usr/bin/grep` has no `-P` (error seen). My kit says use `python3 -I`. Other kits copying that line will fail at that step.
5. The sweep's "9 columns" is not stated; measured: 8 columns now, 9 with Progress.

## Facts re-measured (instrument; control)
- Main `7365165d50193082ec3daf6eca137cd0ff0d4588` (`commits/main`). Open PRs #245-#252: `pulls/<n>/files` intersected with the seven lane paths by `grep -x -F -f`: shared 0 on all 8 (45 files; planted control reads 1, unplanted 0). 19 live `refs/heads/b9*` branches read by `compare/main...<b>`: shared 0 on each. Read-only imports hit only `globals.css` in #250 (H2; not imported by us). No `b944` ref (control: `heads/b9` = 19 refs); ports 9750-9759 free (`lsof` 0); `.tools/b944` absent (control `b198` lists); no 10-30 kit mentions H69/B944/975x.
- Files at main (tarball): `CustomerManagement.tsx` 288 lines, `EngagementsList.tsx` 74, tests 140 / 126 / 45 lines with 7 / 9 / 1 `it(`; sha256 prefixes in the kit. No `*.restyle.test.tsx` for either (folder listed; control `parts.restyle.test.tsx` present). Non-ASCII per character counted by python.
- Menu clip (B908-4): wrapper `relative inline-block` line 60, `ul absolute ... mt-1` line 67 inside `overflow-x-auto data-scroll-x`. Upward-only opening would fail for a short table (the scroller's top clips too), so the kit uses fixed positioning in the same DOM; a portal would break the Tab order that unit rows 82-83 and `playbook-customer-screens.spec.ts` 219-227 pin. CSP allows inline styles (`proxy.ts` line 81).
- `shell-sidebar.spec.ts` line 335 reads `[data-scroll-x] th button` and `[data-scroll-x] .sr-only`: the kit pins both.
- Design: chips row ("All" first), `.progress` bar, "N / 16 answered": words not adopted (see Q-2/Q-3).
- Model rows: L6 85, C2 92, G2 109 (`/usr/bin/grep -n -i`); `models_latest.json` line 23 `claude-sonnet-5-5`. Panes at 15:03: tuesday, H59, H63, H66, H68, G216-G220, fleet-monitor; no H69. Load1 11.87 at 14:59.

## D-decisions (mine, in the kit)
D-1 base on H3's landing, no merge step. D-2 change line 57 of one test only. D-3 progress = step count via a shared exported helper `rowProgress` (additive export). D-4 bar carries the name, printed figure `aria-hidden`. D-5 wide columns lg -> xl and measure 10 right-edge numbers (HPSMPOC-401). D-6 menu `position: fixed`, same DOM, flip up, close on scroll/resize. D-7 cards get the bar too. D-8 the only added words are existing ones. D-9 sort unchanged, progress not sortable (needs `directory.ts`). D-10 aliases held by not touching names. D-11 no committed spec; scratch spec. D-12 target READY 180, hard stop 270.

## Q-questions for Tuesday (each with a default)
- **Q-1:** May the seat change line 57 of `CustomerManagement.test.tsx` (combobox -> chip click), one line, quoted in the PR? Default **YES** (the ticket's own scope sentence removes the select).
- **Q-2 (customer-facing words, the product owner's):** chip text. Default: reuse the existing words "Stage", "All stages" and the five `STAGES` labels; do NOT adopt the design's "All". Flag for the product owner.
- **Q-3 (customer-facing words):** the progress figure. Default: "N of M steps" (already shown on Engagements; "5 of 8 steps" is pinned by an existing test). The design's "N / 16 answered" needs data the directory lacks; not shown as done.
- **Q-4:** Make the scrollers focusable `TableScroll` regions? Default **NO** (keeps roles and the line-335 selectors; adopt only if axe flags `scrollable-region-focusable`, then ask, because it adds an accessible name).
- **Q-5:** Should the lists show Demo aliases (new behaviour)? Default **NO, not here**; a separate ticket if wanted.
- **Q-6:** Hard stop 270 minutes and target READY 180? Default YES.

## UNMEASURED
Layout at any width (nothing rendered); `position: fixed` behaviour inside the real scroller; axe on chips/bar; suite counts; Chromium availability; `commits?path=` history of the two screens (the kit orders it as PRIOR-WORK CHECK); the page-score-bar part of HPSMPOC-402 (not this lane).

## Reasons not to launch now
Machine load (11.87 at 14:59; use `launch_when_cool`, load1 < 7). No lane conflict. Launch after H69's name is confirmed free.

## Outside-the-fences disclosure
No fence breached. Scratch (tarball extract, symlink, PR file lists, Jira text) is under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/bac710bd-bbd2-4bfc-92fb-a9e7c76b9ed8/scratchpad/drafters/b944/`. Nothing written in the project's `1_Project_Definition/Briefs/`.
