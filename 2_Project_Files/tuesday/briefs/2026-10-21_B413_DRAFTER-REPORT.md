# B413 drafter report (C8 Sonnet, 2026-10-21 15:15-15:25 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B413_SEAT-G26_hpsmpoc-pr176-gate-tier2.md` (41 lines; 2 unfilled slots, `@STAMP_TIME@` and `@LAUNCH_AUTH@`, counted by `/usr/bin/grep -o -E '@[A-Z_]+@' | sort | uniq -c` = 1 each; no `.pre-stamp` copy made, as commissioned). Structure copied from B404's kit (read whole, 40 lines). Read whole: B404 kit, B407 brief (105 lines), B407 STATUS (337 lines).

## Measured (read verbs only, gh GETs under the project GH_CONFIG_DIR, 15:15-15:20)
- main = `a542f863` (ls-remote). PR #171 landed; `compare ec0a62a1...a542f863` = ahead 1, one added `.cs` file. Head `69ac8aa8` = `refs/pull/176/head` = branch. No `b409*`, `b410*`, `b413*` on origin. Only open PR is #176.
- PR #176: open, not draft, mergeable true, mergeable_state blocked, 1 commit, 21 files, +193/-26, base shown `a542f863`. `compare a542f863...69ac8aa8` = diverged, ahead 1, behind 1; `compare ec0a62a1...69ac8aa8` = ahead 1, behind 0.
- The 21 files (gh compare): 20 modified, 1 added (`web/src/productName.test.tsx`, +167). Changed line pairs = 26 (193 - 167 = 26 additions, 26 deletions). The commission's "20 one-line string swaps" is loose (20 files, 26 lines); the kit says so.
- Required contexts (strict false): the same five as B404. Head CI at 15:16: secrets, dependency review, Analyze (actions) success; CodeQL **neutral** while three Analyze legs run; api, infra, web unit, web build, both SQL Server shards in progress; `web (Next.js)` and `web e2e` not listed yet. 1 code-scanning analysis (actions) at the head, 0 results; open alerts 0 (main also 0: non-discriminating).
- git grep over the head tree (the head object is present in the local store; `a542f863` is not): product name without `HP ` outside the HP content dirs = 9 lines (1 e2e comment, `brand.css:11`, 7 in the pin file); `DataSec` = 8 lines (`phase-flow.ts:4` comment + 7 in the pin file); `api/src` outside SeedContent = 0 for both. Sign-in `SignInScreen.tsx:55,124` already new; `app/page.tsx:9` title is `Sign in` (no product name, unchanged).
- Load 5.02/5.29/4.59 (uptime); ports 7960-7969 no listener (unfiltered 26 lines); `.tools/b413` absent, `.tools/b407` present (control).

## Update-branch: NOT needed (drafter's reading, kit tells the gate to re-measure)
Strict is false; the head is diverged only by main's one `.cs` test file against the PR's 21 web paths (disjoint); the head's CI is on its own tree. Needed only if a required context goes red for a reason main's file fixes (none expected: it is a test-only api file). Consequence if Tuesday does it anyway: new head sha, `--match-head-commit` at the new sha, CI again from zero, which costs time before tonight's freeze.

## Decisions I made in the kit (veto-able)
1. Kit adds checks 7 (update-branch and legacy merge-tree against `a542f863`) and 8 (gitleaks) beyond your six, because the template's verdict line carries merge-main and gitleaks.
2. Inverse-transformation program must be built by the gate, run in both directions, with the ruled layout strings as the only per-file exceptions; the two Tuesday defaults (tab default, caption spelling-only) are Notes, not defects.
3. Check 3 names seven planted-violation cases including comment and `content/` exclusions staying green, and mutants on `PackView.tsx:61` / `PartnerDashboard.tsx:159` (the two surfaces the builder covered by scan only).
4. Rendered look (check 5): the kit does NOT guess the mock-mode env variable; it tells the gate to quote it from `ci.yml` / `playwright.config.ts` / B393 and B407 STATUS. It adds what the builder did not open: `/customers/<id>/report`, print emulation, and the sign-in tab.
5. e2e: `web e2e` was not listed at the head at 15:16 (UNMEASURED why). If CI skips it, nobody has run the 6 changed e2e assertions; the kit makes the gate say so plainly.
6. Timing: kit proposes a verdict inside about 90 minutes, hard stop at 2 hours, because of tonight's deploy and the Wednesday 23:59 freeze (my proposal, not from the brief).
7. Hold: B409 and B410 trees named as not the gate's; heavy runs only at load1 < 8 (load was already 5 at 15:15).

## Questions with recommended answers
1. Launch now at CI-in-progress, or wait for CI to finish? Recommend launch now: the gate re-reads CI at start, mid and verdict, and the first hour is local work.
2. Should the sign-in page's tab (`Sign in`, no product name) be a Note or a finding? Recommend Note (not in the card's ruling; the builder flagged it for the product owner).
3. 90-minute target acceptable? Recommend yes, otherwise the gate's `STOPPED: NEEDS TUESDAY` at 2 hours is the backstop.

## Not done / UNMEASURED
No npm, vitest, next, dotnet, fetch, az, docker, ssh or HTTP run. Why `web e2e` was absent from the head's check list at 15:16 is UNMEASURED. B409/B410 branches are not on origin, so any overlap with `layout.tsx`, `AppShell.tsx`, `app/page.tsx` or `SignInScreen.tsx` is UNMEASURED (the kit's check 7 covers a late landing). `a542f863` not in the local object store, so the main-side grep was not run.
