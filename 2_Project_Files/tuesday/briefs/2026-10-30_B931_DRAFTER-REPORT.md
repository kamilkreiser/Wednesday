STARTABLE: YES (after your stamp; wave 1, no dependency open: HPSMPOC-368 and -371 are in main)

# B931 drafter report (2026-10-30 about 10:23 to 10:55 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B931_SEAT-H62_hpsmpoc-385-playbook-grid.md` (144 lines; 9 four-underscore lines = 8 slots + the last line, by `grep -c -E '_''_''_''_'`, control `a____b` reads 1; at-sign slot pattern 0; non-ASCII lines 0, control: a planted ellipsis byte line reads 1). Read-only everywhere else: gh `-X GET` under the project `.gh-config`, a tarball of `e21d8044` in my scratchpad, one Jira issue GET and two JQL searches, no `cd`, no hosted HTTP, no ref written, no message. Nothing was written to the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H62` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes) edits three files (`PlaybookShell.tsx`, `PlaybookHome.tsx`, `ModuleScreen.tsx`) and adds three unit test files, on branch `b931/hpsmpoc-385-playbook-grid` off `e21d8044`, ports 9630-9639. The rail goes; the home is ALREADY a card grid in code (only a breakpoint re-tune); "All modules" is the one new string; the viewed count and the product-name link stay in a one-line top strip of the shell. No dependency on H3.

## Facts re-measured (instrument; control)
- main `e21d80442980fb61ad9fb11aaf393c0b20c0ad2d` (`commits/main`); open PRs 0; `heads/b93` only `b93/gate-b94-notes` (control `heads/b9` 9 refs); panes `%0 tuesday`, `%1 fleet-monitor`; `lsof` 9630-9639 0; port/seat word scan of 130 kit/STATUS files dated 10-29/10-30: 0 for `963x` and `H62` (control `979x` 10); load1 2.55 at 10:23. Local clone lacks `e21d8044` (its origin/main is `94274a75`): the kit makes the seat fetch.
- `PlaybookShell.tsx` 64 lines: rail nav "Playbook modules" `lg:w-72` lines 25-60, `main#main` 61, `moduleHref` 12 (7 importers). `PlaybookHome.tsx` 60 lines: `ol aria-label="Modules"` grid `md:grid-cols-2 xl:grid-cols-3` line 37. `ModuleScreen.tsx` 67 lines: prev/next nav 53-64, no "All modules" (grep of `web/src` and `web/e2e`: the only hit is the rail's disclosure, line 35).
- `SnapshotLauncher.tsx`: 8 export lines (23 to 61); `PartnerDashboard.tsx` line 11 imports `MockTag` (the "home dashboard" of the ticket).
- Design: `resources()` line 206, `moduleText()` line 207; grid 3 / 2 / 1 columns at viewport 1250 and 620 px; module page has "All modules" in the header.

## Sweep pointers found WRONG or incomplete
1. **AC 2's cited proof is not a module page.** `playbook-customer-screens.spec.ts` line 91 checks Resources current on `/documents`. The module-page proof is `shell-sidebar.spec.ts` lines 370-372 (`/playbook/discovery`). And AC 2 is GlobalNav's job (`currentItem`, longest match), not the shell's.
2. **On `/playbook/snapshot-assessment` the current entry is Assessments, not Resources** (`GlobalNav.tsx` line 42 `also`; H7's file). AC 2 holds for 10 of 11 modules; it would hold for all 11 once H7 retires the Assessments entry (its `my-readiness` replacement has no `also`). The kit makes the seat report it, never fix it.
3. **"The home becomes a grid" is already met in code**: `PlaybookHome.tsx` line 37.
4. **Hidden outside-lane test:** `web/src/productName.test.tsx` lines 82-85 render shell plus home and require ONE link named exactly "HP Security Services Playbook" to `/playbook`, which today is the rail's link. Removing the rail naively turns it red. Handled by D-2.

## D-decisions (in the kit)
- D-1 base `e21d8044`, no rebase; the playbook files import no H3 primitive.
- D-2 keep a one-line top strip in the shell (a `div`, not a `nav`, `no-print`): the product-name link and the viewed chip, on every playbook page.
- D-3 grid stays `md:2 / xl:3` unless the screenshots show cards under about 280 px.
- D-4 `BlockRenderer.tsx`, `SnapshotLauncher.tsx`, `layout.tsx` and the existing playbook tests stay byte-equal.
- D-5 the chip keeps the existing words "N of 11 modules viewed".
- D-6 no committed Playwright spec; browser proofs come from an uncommitted scratch spec under `.tools/b931/`.
- D-7 Sonnet C2 builds; gate G2 tier 2; target READY 180, hard stop 270 minutes.

## Q-questions for Tuesday (each with my default)
- Q-1 (D-2): top strip with the link and the count on every playbook page? Default **YES**: it keeps `productName.test.tsx` green unchanged and keeps AC 4 on module pages. The alternative is the count on the home only (the design's place).
- Q-2 (D-5): chip words "N of 11 modules viewed" (existing), not "N of 11 viewed"? Default **existing words**.
- Q-3 (D-4): SnapshotLauncher and BlockRenderer byte-equal? Default **YES** (nothing in the scope needs them).
- Q-4 (D-6): no committed e2e spec? Default **YES** (standing rule: a new spec needs asking; the existing `playbook-quality` and `shell-sidebar` specs cover AC 2 and AC 3).
- Q-5: gate round. Default round 1 of 2 on class "playbook rail removal".
- Q-6: hard stop 270, target READY 180? Default YES.

## Stamp slots (my defaults)
STAMP: D-1 to D-7 accepted, Q-1 to Q-6 as defaults. KEYS: HPSMPOC-385. LAUNCH WINDOW: from stamp until 18:00 AEDT 2026-10-30 through launch_when_cool below load1 7, with the other HPSM-POC lane panes named. Stamped by: the Tuesday seat. Launch authority: the 2026-10-30 10:07:23 instruction, 2026-10-29 10:05:10 commission, 2026-10-16 grant, 2026-09-13 as-many-agents rule. Hard stop / target: 270 / 180 minutes after Step 0. Head and main: `e21d8044` or what moved (other lanes landing is expected; the kit's main-moved rule lists the files that would stop it). Model receipt: the line in the guidance plus load1.

## Reasons not to launch now
None. One thing to know: H7 (GlobalNav, readiness) and H15 (pages inside this layout) touch neighbouring behaviour; neither shares a file.

## UNMEASURED
Unit and e2e counts at main, Chromium availability, the rendered grid beside the 228 px sidebar, axe on the new top strip.
