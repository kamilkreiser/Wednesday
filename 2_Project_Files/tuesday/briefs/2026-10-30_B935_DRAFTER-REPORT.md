STARTABLE: YES (after your stamp; wave 1, no dependency open: HPSMPOC-368 and -371 are in main. One coupling: the screen imports H3's `partner/parts.tsx`, so the lane takes H3's landing by one merge commit before its gate, D-1.)

# B935 drafter report (2026-10-30 about 10:36 to 11:05 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B935_SEAT-H66_hpsmpoc-382-action-plan-restyle.md` (143 lines; 9 four-underscore lines = 8 slots + the last line, by `grep -c -E '_''_''_''_'`, control `a____b` reads 1; at-sign slot pattern 0; non-ASCII lines 0 after repair, control: a planted U+201C line reads 1). Read-only everywhere else: gh `-X GET` under the project `.gh-config`, a tarball of `e21d8044` in my scratchpad, one Jira issue GET and two JQL searches, no `cd`, no hosted HTTP, no ref written, no message. Nothing was written to the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H66` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes) edits ONE file (`partner/ActionPlanScreen.tsx`, class names only) and adds one unit test (`ActionPlanScreen.restyle.test.tsx`), on branch `b935/hpsmpoc-382-action-plan-restyle` off `e21d8044`, ports 9670-9679. `action-plan.ts` and the two existing tests stay byte-equal (0 class strings in the helper, 0 class assertions in the tests). Every word, test id, accessible name, handler and href is pinned by program.

## Facts re-measured (instrument; control)
- main `e21d80442980fb61ad9fb11aaf393c0b20c0ad2d` (`commits/main`); open PRs 0; `heads/b93` only `b93/gate-b94-notes` (control `heads/b9` 9 refs); panes at 10:36 `%0 tuesday`, `%50 HPSM-POC-H59`, `%49 HPSM-POC-H60`, `%48 NexusAI-R92`, `%1 fleet-monitor`; `lsof` 9670-9679 0; word scan of 149 kit/STATUS files dated 10-29/10-30: 0 for `967x`, `H66`, `B935` (control `963x` 2); load1 5.53 at 10:36 (rising: H59 and H60 started).
- `ActionPlanScreen.tsx` 415 lines: imports `Crumbs, IllustrativeTag, MoreLink` from `./parts` (line 27, H3's file), `readinessHref` (13, H7's), `MockTag` (12, H11's); six-column row grid at `lg:` (strip 237, row 295, 11 row tokens); 16 non-ASCII lines (typographic quotes in accessible names the tests read).
- Tests: `ActionPlanScreen.test.tsx` 17 its, `action-plan.test.ts` 6 its, 0 class assertions in either. e2e readers: `playbook-partner.spec.ts` (49-184; `toHaveText("1 of 6 done")` exact at 81), `playbook-b17-clicks.spec.ts` (67-136), `playbook-event-states.spec.ts` 57, the live-API spec (not run).
- Design `actionPlan()` line 197: 4 KPI tiles (3 of them NEW counts), a `table`, a "saved locally" notice (false: the plan is the API's), a 3-button resource row to other targets.

## Sweep and ticket pointers found WRONG or incomplete
1. **`browser-store.ts` is not on the action plan's path.** Its only importer is `stores.ts` line 8, for `revenueStore` (line 169). "Read only" holds trivially; the ticket's Files line overstates it.
2. **`action-plan.ts` has nothing to restyle** (pure helpers, 0 `className`). Kept byte-equal (D-2).
3. **The screen DOES import H3's `partner/parts.tsx`** (the sweep row lists it nowhere for H8, and B929's sibling line says H8 touches none of H3's paths: true for edits, not for imports). Hence D-1.
4. **AC 1's "apart from class or layout assertions" allowance is not needed:** the existing tests hold none.

## D-decisions (in the kit)
D-1 base `e21d8044` + H3-LANDED RULE (one `merge --no-ff origin/main`, never rebase, as B932 D-3); D-2 `action-plan.ts` and existing tests byte-equal; D-3 row grid `lg:` to `xl:` unless the 1024 px screenshot proves `lg:`; D-4 keep the `ol`/`li` rows, no `table`, no import of `ui/Table` (copy `thClass`'s words); D-5 no new words; D-6 resources keep their four cards and targets; D-7 no committed spec; D-8 Sonnet C2, gate G2, READY 150 / hard stop 240.

## Q-questions for Tuesday (each with my default)
- Q-1: add the design's eyebrow "Partner enablement" above the title? Default **NO** (a new word; the ticket says restyle only).
- Q-2: add the design's four KPI tiles (Actions, Completed, In progress counts)? Default **NO** (new figures on screen; header facts become two cards instead).
- Q-3: H3 merge per D-1? Default **YES, merge** (same answer you gave B932's Q-1).
- Q-4: `action-plan.ts` byte-equal? Default **YES**.
- Q-5: breakpoint `xl:` by default, `lg:` only with screenshot proof? Default **YES**.
- Q-6: no committed spec; gate round 1 of 2 on class "action plan restyle"? Default **YES**.

## Stamp slots (my defaults)
STAMP: D-1 to D-8 accepted, Q-1 to Q-6 as defaults. KEYS: HPSMPOC-382. LAUNCH WINDOW: from stamp until 18:00 AEDT 2026-10-30 through launch_when_cool below load1 7, naming H59, H60 (H3), H61-H64 and later panes. Stamped by: the Tuesday seat. Launch authority: 2026-10-30 10:07:23 instruction, 2026-10-29 10:05:10 commission, 2026-10-16 grant, 2026-09-13 as-many-agents rule, 2026-10-24 standing order, 2026-10-22 Sonnet-first grant. Hard stop / target: 240 / 150 minutes after Step 0. Head and main: `e21d8044` or what moved (H3 landing expected, D-1). Model receipt: the line in the guidance plus load1.

## Reasons not to launch now
None blocking. Load1 was 5.53 and rising at 10:36 with the wave-1 seats starting: launch_when_cool handles it. Rank 10 in the sweep's order: if seats are scarce, H3 landing first saves this lane its merge step.

## Outside-the-fences disclosure
The Write tool decoded the typed escape text for U+201C / U+201D into the characters (1 line); repaired by a python write; the kit now has 0 non-ASCII lines, and it warns the seat about the same trap.

## UNMEASURED
Unit and e2e counts at main, Chromium availability, the rendered rows beside the 228 px sidebar at 1024 px, axe on the pills, when H3 lands.
