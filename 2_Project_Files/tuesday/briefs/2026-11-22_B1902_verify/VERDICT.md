GATE B1902: GO WITH FINDINGS @ 5b3a5ee on main ec281cf

Tier G2, one Sonnet reader (claude-sonnet-5-5), 2026-11-22 evening. Head 5b3a5ee02753b703d348d903df464d5edff1298e, base ec281cfb35a1356d59e23e1c69e8eab1e1852f2e. Every number below was printed by a program in this gate's own scratch copies (a `gh api -X GET` tarball of each sha; node v24.22.2 / npm 11.19.1 by the kit's path; TZ=UTC). The seat's STATUS was read as a claim; none of its numbers was copied.

## Reads (the stamped kit B1901 whole in 3 pages; STATUS; Jira GET)
- origin main read at the gate: ec281cfb (unmoved); branch b1901/m174-autosave-gap-cells-429 = 5b3a5ee0 (one parent, author the repo's Datasec address, commit text carries the attribution line once); compare main...head: ahead 1, behind 0, files exactly the test file; open PRs 0; PRs of any state with that head branch 0.
- MPSCALC-429 by Jira GET (credentials in-process, never printed): Backlog, updated 2026-11-20T20:18:20, 0 comments, 0 links, label records-pass-1120d; JQL `project = MPSCALC AND ( key = MPSCALC-429 )` 1 row; control MPSCALC-361 Done.

## Rule 1: the diff (MET)
- The head file equals the base file with the kit's frozen `OLD` replaced by `NEW`, byte for byte (OLD occurs once; program compare True). Blobs: base 940d8cdf3f34bf42d60adf9e41d8e71434e51565, head 4ee4a31d1f480e431f6c7de4a8732b1f916264a9, expected-by-replacement 4ee4a31d... (all three as the kit says).
- Whole-tree deep compare of the two tarballs: exactly one differing path, `web/src/screens/QuoteScreen.autosave.test.tsx`; no file added or removed; `git diff --no-index --numstat` `32 0`; `QuoteScreen.tsx` and `quote/**` untouched, so no product byte; no other test changed.
- kit scans1901.py: 32 added lines, 0 non-ASCII (control 1), 0 Cf (control 1), 0 GUID (control 1), names 12 quiet / 12 control fired, 0 tabs, longest 142. No `eslint-disable`, `.only`, `waitForTimeout`, `Date.now`, `performance.now`, `new Date` in the added lines (count 0; control line planted: 1).

## Rule 2: re-runs (all as the kit says; head copy `npm ci --prefer-offline` rc 0, 0 vulnerabilities; load1 3.3 to 6.8 throughout, under 24)
| Run | Tests line |
|---|---|
| test file alone, head | `Tests  32 passed (32)` |
| whole `vitest run`, head | `Test Files  149 passed (149)`, `Tests  1736 passed (1736)`, rc 0 |
| whole `vitest run`, base (same node_modules, own copy with docs/ linked) | `Test Files  149 passed (149)`, `Tests  1734 passed (1734)`, rc 0 |
| `npx eslint` on the file | rc 0, no output |
| `npx eslint .` (whole web) | rc 0 |
| `npx tsc -b` | rc 0, no output |
| `red429.py` (kit's block extracted by program), 6 labels | DIFF 0 |
`red429.py` lines, each MATCH: base0 30 passed (30); head0 32 passed (32); base-m1 30 passed (30); base-m2 `1 failed | 29 passed (30)` G5; head-m1 `2 failed | 30 passed (32)` G15, G16; head-m2 `3 failed | 29 passed (32)` G15, G16, G5. (A first whole-base attempt in a copy without `docs/` failed 2 files on ENOENT of docs/api/openapi.json: my copy's layout, not the code; re-run with the layout fixed is the row above.)

## Rule 3: the ticket's acceptance check, line by line
1. "A cell for each of the two behaviours turns red under the one-line change that removes it": MET. Behaviour 1 (an explicit save starts its own gap): `head-m1` G15 and G16 red. Behaviour 2 (a new request restarts the running timer): `head-m2` G15, G16 (and G5) red.
2. "and stays green on main": MET. `head0` 32 of 32 green on the unmutated code; `base-m1` shows the base cells also stay green under change 1 (30 of 30). (The cells are not on main yet; "green on main" is read as green on the unmutated product code of main, which the head shares byte for byte.)
3. "the count of cells is printed before and after": MET. 30 before (`base0`), 32 after (`head0`); whole run 1734 before, 1736 after.
4. "no product file changes": MET (rule 1: one differing path, a test file).
5. "no other test changes": MET (same).

## Rule 4: the named overlaps and one mutation of my own
- G5 red under the no-clear change at base (`base-m2`): a NAMED PROPERTY, not a defect of the cells. G5 (`vi.getTimerCount()` is 0 after leaving the screen) was already a timer-counting cell. Consequence for the ticket text (a records finding, below): its premise "caught only by a cell that counts timers" is true only in the sense that the catcher is such a cell; it is not true that the owned cells were green.
- Both new cells red under the arms-no-gap change (`head-m1`): a NAMED PROPERTY. Read at source: with an explicit save that arms nothing, the first gap timer is the only one and ends at T+GAP, so G15 sees the third request at T+GAP, 5 s before T+5000+GAP, and G16 sees its timer count fall to 0 at T+GAP, before the new gap would have ended; each is red for the reason its title gives. G15 under the no-clear change is also legitimate: the old timer ends at T+GAP and sends the trailing save early.
- My own mutations, not among the six labels (head copy, the file alone, 32 cells; outputs in my scratchpad):
  - mA, `armGap()` moved to AFTER the awaited `api.updateDraft` (the source comment at `QuoteScreen.tsx:268` says it is synchronous, before the request): 32 passed (32), NO cell catches it, new or old. Plainly: the new cells do not pin "armed before the request"; that property is unpinned by the whole file. Out of 429's scope; a ticket candidate (FOR-RECORDS).
  - mB, gap 1 ms short (`AUTOSAVE_MIN_GAP_MS - 1`): red, G15 and G16 among the failures.
  - mC, the gap-end trailing flush removed: red, G15 among the failures.
  - mD, `gapOpenRef.current = false` removed from `armGap`: red, G15 among the failures.

## Findings (all Minor / records / text; none blocks)
1. (records) The ticket's claim that the no-clear change leaves every owned test green is wrong at main: G5 is red under it (`base-m2`). Said in FOR-RECORDS.md.
2. (records) mA above: arming after the await is pinned by no cell in the file; a ticket candidate, not this change.
3. (text) The ticket's sentence "the first change leaves the 17 cells of the flush file green" was not re-run here (that file, `quote/autosave.test.ts`, is not in this change); nothing in this verdict depends on it.

## Not a finding
The seat's STATUS equals what this gate measured on every number it states (blob, numstat, six red lines, 32/1736/149, eslint, tsc, scans). The commit text has no person's name and no sentence that the product owner decided anything.

## Not run
No `gitleaks` (the diff is 32 lines of synthetic test text, scanned by the kit's scans1901.py; no history scan). No dotnet, Playwright, build, `az`, deploy, browser or listener. Hosted CI and CodeQL are Tuesday's after the PR opens (landing.txt carries the order). Open code-scanning alerts at main read 0 (GET).

## Rules kept
Wrote only this folder and my session scratchpad; the project's `.tools/.heavy-lock-*` were NOT taken (a write in the project tree; heavy jobs ran one at a time at load1 under 7, and the machine had no seat of mine competing); no project, Jira, GitHub, or human was written to; nothing deleted; no `cd`; no credential printed; no person's name in any landing text.

## Landing files
pr-title.txt, pr-body.md, squash-subject.txt (ends `(#PRNUM)`), squash-body.txt (ends `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`), landing.txt (`pr_checks_wait.sh --min-checks 9`, PR 226's nine check names), FOR-RECORDS.md.
