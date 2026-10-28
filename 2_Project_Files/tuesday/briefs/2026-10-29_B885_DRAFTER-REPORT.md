STARTABLE: YES (pins hold: main c00e28284e9acacf16462ea3c2b533936b3db210 at 10:16 AEDT, no b885 ref, 0 open PRs, ports 9710-9719 have 0 listeners; one fetch is owed by the seat because the project clone may lack c00e2828). Caution: this is a large lane; see Q-7.

# B885 DRAFTER REPORT (builder kit for Datasec/HPSM-POC-H51: v1.2 design lane L0, tickets T01 to T04, left sidebar and top bar shell)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B885_SEAT-H51_hpsmpoc-v12-shell-left-sidebar.md` (167 lines). Shape: the stamped open-sign-in kit (124 lines) and chooser-logo kit (125 lines) with their drafter reports and STATUS files. Read-only: no write to any project, Jira, GitHub or git; the design file was read with `python3 -I`, never opened in a browser.

## BLUF
- Branch `b885/hpsmpoc-v12-shell-left-sidebar`, 1 to 4 commits (tokens first so the primitives lane can start), Sonnet (row C2 line 92), tier-1 gate (row G1 line 108). Ports **9710-9719** (web 9710, stub 9711, hosted 9712, chooser 9713, own servers 9714-9719).
- Default design: full-width top bar stays (logo, "Menu" toggle, badge, Sign out, Reset demo, picker), sidebar below it, persistent from 1024 px, drawer with backdrop below; no page body edited; hidden entries are model data behind a `built` flag guarded by `nav-dead-ends`.
- The delta is mostly right; nine corrections found (below). Two change the design: the picker cannot be an eager directory select, and the print fix is a class, not a CSS rule.

## Facts re-measured (instrument, control)
- main: `gh api -X GET commits/main` = c00e2828 (2026-10-27T18:17:08Z); `pulls?state=open` printed nothing; `matching-refs/heads/b885` length 0; `lsof -nP -iTCP:9710-9719 -sTCP:LISTEN | wc -l` = 0; scan of 10-28/10-29 SEAT kits for 9700-9719 printed no file (control: 984x scan found the NexusAI kit). Panes: wednesday, Datasec/Security-Composer-R81, fleet-monitor (no HPSM pane). Load1 5.46.
- Tarball of main extracted into the scratchpad; read whole: AppShell.tsx (199), GlobalNav.tsx (92), both layouts, globals.css, tokens.css, contrast.ts/test, print-rules.test.ts, GlobalNav.test.ts, nav-dead-ends.test/spec, AppShell.burger/compact tests, shell.ts, playbook-burger-menu.spec.ts, playwright.config.ts, ci.yml web jobs, e2e.mjs header, the services pages and the directory hooks; many others by line.
- Design: lines 293-294 (MENU_SPEC, MENU_ALLOWED) and sidebar CSS read by `python3 -I`; delta role matrix matches (Partner 10, Consultant 11, Demo 11, Admin 13). Contrast recomputed: focus `#1d4f91` on navy 1.84; `#2d5e7b` border on navy 2.14; the four passing pairs match the delta.
- Kit hygiene by program: four-underscore lines = 9 (control: scratch file 1); at-sign tokens 0; person-name patterns 0; non-ASCII 0; `WED_USAGE_STOP=100` appears 3 times (outside and inside the launch quotes).

## Corrections to the delta (all in the kit's Fact marks)
1. T01 AC 8 cites `responsive.spec.ts` for five widths; it has no width loop and runs at 1440 and 820 only: a new `shell-sidebar.spec.ts` carries 390/768/1024/1280/1440.
2. Section 6 omits tests that render the shell: `HpLogo.test.tsx` R1 (lines 86-107, 109, 432, 228), `productName.test.tsx` line 63, `UatStartScreen.test.tsx` lines 138/149. Kit keeps the "Menu" button inside `header` so these stay green; D-1 option B would move them.
3. `METRICS_ROLES` is imported from `GlobalNav.tsx` by `AttributionPreviewScreen.tsx` and `MetricsDashboardScreen.tsx` (not editable here): must stay exported.
4. "4 new entries, 3 renamed": 3 new entries (one held), up to 9 label renames, and the combined Assessments entry is dropped by the design (D-4, D-6).
5. T03 Demo alias AC has no basis: the register, engagements list and directory hold no alias logic; alias exists per customer from metrics runs only. `useDirectory` at shell level would add 1 + up to 25 requests per page and break five unit files whose `@/api/browser` mock has only `resetDemoData`. Kit: lazy disclosure picker, hidden for Demo.
6. "Consultant/Demo gain Service offers: check API role rules": measured, the `/services` pages make no API call and have no role guard.
7. Print: `print-rules.test.ts` pins exactly one `.no-print` rule and one `nav` rule and the minifier joins equal-declaration rules; use the class `no-print` on the aside, add no CSS rule.
8. `PrototypeBanner` is already an `aside`; four test files find it by `/notice/i`: the sidebar landmark name must not match.
9. Additional contrast finding: sidebar-hide border 2.14:1 fails 3:1; focus on navy needs a light ring token.
Line references checked and correct: AppShell.tsx 105-125/134-140/172, playbook.ts 169-172, playbook-customer-screens 89-91/228, b17-clicks four `openMainMenu` calls, print-rules.test.ts path.

## D-decisions (defaults apply if the stamp is silent)
D-1 geometry A (top bar full width, sidebar below; B = the design's own brand block, a larger test change). D-2 1 to 4 commits, push after the tokens commit. D-3 persistent from `lg` 1024. D-4 keep existing labels (the design's labels listed for a one-word flip). D-5 lazy picker, hidden for Demo. D-6 Assessments stays until My readiness is built; the readiness lane flips one flag. D-7 Consultant and Demo gain Service offers. D-8 Sonnet builds, tier-1 gate.

## Q-questions for Tuesday at the stamp (each with a default)
- Q-1 Geometry A or B (logo stays in the top bar vs sidebar brand block). Default A; the product owner can order B after the screenshots.
- Q-2 Gate round. Default NO GO 0 of 2 on the new class "app shell restructure", tier 1.
- Q-3 Labels: keep (default) or adopt the design's nine (D-4).
- Q-4 Service offers widened to Consultant and Demo (default yes, D-7).
- Q-5 The readiness hand-off (D-6): the page lane flips one `built` flag in `GlobalNav.tsx`; confirm that single cross-lane edit is acceptable (default yes).
- Q-6 Picker hidden for Demo and lazy (default yes). Also the four Jira keys for the KEYS slot.
- Q-7 Split into two seats? The lane is large (about 25 test files to move, a 5-width screenshot set, a full e2e run). Default: one seat, target READY 360 min, hard stop 480; the natural split is C1-C2 (tokens + nav model + tests) then C3-C4 (shell + e2e), but the second needs the first's branch.
- Q-8 Port block 9710-9719 (default accepted); pane `Datasec/HPSM-POC-H51`, re-check if a sibling kit took it.

## UNMEASURED
Test counts at main; Chromium availability; whether `AppShell.compact.test.tsx` stays green with the toggle in `header` (predicted); jsdom `inert` support; how every page reads at 1024 to 1439 with the sidebar; the exact set of breaking e2e specs (predicted from greps, not run); whether the full e2e run fits the hard stop; the route names of the customer workspace (kit marks them provisional); HP-reviewer wording decisions (labels, Training principles) which are not this lane.

## Outside-the-fences disclosure
Read-only everywhere except the kit and this report. `gh api -X GET` only, under the project's `GH_CONFIG_DIR` (commits, pulls, matching-refs, tarball). Local reads: the delta, the design file (python3 -I extracts only), two model kits and reports, the B860 STATUS head, `model-routing.md` rows, `DRAFTER_RULES.md`, `models_latest.json` (grep), lsof/tmux/uptime. No Jira call, no git command inside `!CODING`, no browser, no npm. Three bash calls were refused by hooks (a `cd`, an `==` word, a `..` write redirect) and re-issued; one stray `cd /dev/null` attempt was refused. Scratch (tarball, control file) is in the session scratchpad `b885/` folder.
