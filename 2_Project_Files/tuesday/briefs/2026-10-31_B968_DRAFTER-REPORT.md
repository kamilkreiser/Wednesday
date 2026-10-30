STARTABLE: YES (after your stamp; no live lane touches the spec, axe.ts, globals.css or CustomerManagement.tsx; one caution: load1 was 8.03 at 09:49, so launch_when_cool will wait, and the edited row may stay green with the rule removed, Q-1)

# B968 drafter report (Sonnet 5.5, Sat 31 Oct 2026, 09:47 to about 10:10 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B968_SEAT-H78_hpsmpoc-399-sidebar-spec-wait.md` (95 lines; 9 four-underscore lines = 8 slots + the last line, by grep; 0 non-ASCII by program; 0 `@X@` markers). Read-only everywhere else: `gh api -X GET`, no write, no cd, no build or test run, nothing sent.

## BLUF
B968 is B950 re-pinned on main `edf363427b5e9ebc538841332b40b161f770088d`. The job is unchanged: seat H78 (Sonnet), branch `b968/hpsmpoc-399-sidebar-spec-wait`, one commit, one path, hunks inside the row at lines 320-328, plant = delete globals.css line 69 in a scratch tree. The row and `wider text` row did not move. The wait element for 768 and above is unchanged; the wait for 390 changed from "first customer link or card" to a named locator: the first link in the list named `Customers` (the cards `ul`, `aria-label="Customers"`, line 290 of CustomerManagement.tsx).

## Measured at edf36342
- main = `edf36342...` (re-read; 9 commits past `37bc6323`: #245, #250, #248, #254, #255, #252, #256, #251, #257, all merged).
- Spec: 434 lines, blob `fbe1e4d22cef19a76df54da223f8665191c9e5e2`, sha256 `b50fbe76e0efb46389698ea84a2875d544904ebe2766e4b4859ea7ed6938eadb`; row `no sideways scroll on Home or Customers` lines 320-328 (the only wait is the h1 heading at 324); describe at 108, loop at 107; `wider text` test at 335, its `th button` wait at 338, describe at 332. Tree 1648 entries, not truncated, spec path once (control 0).
- `axe.ts`: 67 lines, blob `c7e31636...`, unchanged since `37bc6323` (compare count 0, control 0); `noSideScroll` lines 49-67, verdict at line 66.
- `globals.css`: 129 lines, blob `366bf6dc...`; the rule is now **line 69** (in `@layer base`, line 57; comment 66-68); #250 added three `@source not` lines at the top (lines 5-7).
- `CustomerManagement.tsx`: 357 lines, blob `19914f0c...`. Ready branch (line 272) only; loading 266, error 267, empty states 281 and 285. Cards `<ul ... md:hidden aria-label="Customers">` line 290, card link line 295; table wrapper `hidden overflow-x-auto md:block` with `data-scroll-x` line 310; `SortHeader` lines 125-135, button line 129. So `[data-scroll-x] th button` is still valid from 768 and still times out at 390.
- Open PRs #253, #258, #259, #260: spec 0, CustomerManagement 0, globals.css 0, axe.ts 0 each (control 1 / 0). Of 26 `refs/heads/b9*`: spec shared by b930 (head of merged #249) and b949 (head of merged #256) only, both landed (b949's spec blob equals main's); CustomerManagement shared by b944 (head of merged #255) only, landed; globals.css and axe.ts 0 for all. **No STOP lane.** No `b968*` ref.
- Panes: `tuesday`, `fleet-monitor`, H68, H74, H76, H77, G231-G234; no H78. Ports 9970-9979: 0 listeners. Load: `9:49 up ... load averages: 8.03 4.16 2.69`. Sonnet id `claude-sonnet-5-5` (models_latest.json line 23). Routing rows L6 line 85, C2 line 92, G2 line 109 (unchanged).

## B950 facts found stale
- Pin `37bc6323` is now `edf36342`; spec blob `7985e86c...` and sha256 `c419dd6e...` are now `fbe1e4d2...` and `b50fbe76...`. Line count (434) and the row and wider-text line numbers are unchanged.
- The drafter's task note says #256 edited the spec "one word"; it is three string edits (`Service offers` to `Delivery phases`, lines 11, 370, 417; 3 additions, 3 deletions). None is in the row.
- globals.css rule line 65 is now 69; file 125 lines is now 129 (#250 landed, so "PR #250 open" is gone; globals.css moving is no longer a likely trap).
- CustomerManagement.tsx markup: table wrapper line 248 is now 310; `th` button line 84 is now 129; mobile cards `ul` is at 290 and carries `aria-label="Customers"`.
- `axe.ts` `noSideScroll` lines 49-69 were mis-stated; the file is 67 lines, function 49-67 (the file is unchanged, so this was an earlier miscount).
- B950's coupling to lane H4 (B944) is gone: #255 landed. Co-running panes, port blocks and load figures replaced. b930 is no longer "blob equals main" (main moved past it); the kit's landed test now names the merged-PR-head rule first.
- The wait element at 390 was left open in B950; now named (Q-2).

## D-decisions
- D-1: wait element branches on `size.width`: below 768 the first link in the `Customers` list (cards); from 768 `[data-scroll-x] th button` first visible. Both exist only in the ready, non-empty state (loading and empty states replace the list), so neither a loading nor an empty state satisfies them.
- D-2: the kit tells the builder to prove the `list` locator resolves to exactly the cards at 390 (count 1, control no-such name 0), because the page also has named navigation lists I did not inspect.
- D-3: ports 9970-9972/9973/9974 mapped as B950's 9810-9814 were (web, stub, plant, hosted, chooser).
- D-4: REFUSE main-moved rule now also tolerates `CustomerManagement.tsx` moving (re-derive the wait), and stops only on the spec or `axe.ts`.
- D-5: structure, REFUSE rules, STATUS-NOW, Stamp (8 slots + last line), Launch line form kept.

## Q-questions (defaults)
- Q-1: if the waited row stays green at all five widths with the rule removed, accept "recorded as intentionally weaker" (comment only), no stress added. Default YES.
- Q-2: wait elements as D-1. Default YES. Alternative: one width-independent wait on the `Customers (N)` h2 (present in the ready state at every width, but it also shows with zero rows, so weaker). Default: no.
- Q-3: gate round. Default tier 2 (G2), round 1 of 2, class "test-only spec row".
- Q-4: target READY 120 minutes after Step 0, hard stop 180. Default YES.

## Recommended stamp values
- STAMP: `STAMPED <clock from date> AEDT 2026-10-31 by Tuesday`, brief and this report read whole, D-1..D-5 accepted, Q-1 YES, Q-2 as D-1, Q-3 tier 2 round 1 of 2.
- KEYS: HPSMPOC-399 item B908-6.
- LAUNCH WINDOW: now until load1 below 7 (launch_when_cool); live seats beside: H68, H74, H76, H77, G231-G234.
- Launch authority: 2026-10-16 HPSM-POC grant, 2026-09-13 as-many-agents rule, 2026-10-24 every-boot-works-tickets, Datasec CodeQL policy, 2026-10-22 Sonnet-first grant, usage grant (WED_USAGE_STOP=100).
- Hard stop / target READY: Step 0 plus 180 / plus 120 minutes (absolute clocks from `date` at launch).
- Head and main at launch: Tuesday re-runs `ls-remote` main (expect `edf363427b5e9ebc538841332b40b161f770088d`), `refs/heads/b968*` empty, open PRs re-listed (#253, #258, #259, #260 today); if the spec, `axe.ts` or any lane in the intersection moved, re-measure first.
- Model receipt: `model: claude-sonnet-5-5 -- Sonnet first: a one-row test edit (model-routing.md row C2 line 92, class row L6 line 85, gate row G2 line 109)`, and the load1 read at launch.

## UNMEASURED
Whether the edited row turns red with the rule removed at any width; whether `getByRole("list", { name: "Customers" })` is unique at 390; spec pass counts at main; build time under load; whether the sweep's other new lanes (b954-b957, PRs #258-#260) will edit the spec later (they did not at 10:0x).
