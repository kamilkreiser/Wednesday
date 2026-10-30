# B953 DRAFTER REPORT (gate kit for PR #253, seat G224, tier 1)

Drafted 2026-10-30 16:5x AEDT, read-only. Kit: 2026-10-30_B953_SEAT-G224_hpsmpoc-253-security-preview-gate-tier1.md (69 lines, 0 non-ASCII, 8 four-underscore lines: S1-S7 and the last line).

## Measured at the draft (gh api -X GET, ls-remote, lsof, sed)
- PR #253 open, not draft, created 16:47 AEDT, head 963f718d, base 37bc6323, 5 commits, 36 files +1479 -27, title 126 chars. ls-remote main 37bc6323 (0 behind), merge ref ff8ec243.
- Checks on the head: CodeQL neutral; Analyze python and actions success (2 analyses on refs/pull/253/head, 0 results); Analyze javascript-typescript and csharp, api, SQL Server, web unit, web build still in progress.
- Routing: G1 at model-routing.md:108, G-cap :111. Opus id claude-opus-5-5 at models_latest.json line 17. Ports 9820-9829 free (lsof 9800-9839 = 0 listeners). .tools/b953 absent. No GATE VERDICT first line names this class (490 STATUS files; control B805/B817 printed).
- b949 is NOT on origin (ls-remote empty); b944 and b945 are.

## Recommended default per stamp slot
- S1: STAMPED <time> AEDT 2026-10-30 by Tuesday s207, kit read whole, decisions Q-1 to Q-4 accepted.
- S2: launch_when_cool at load1 below 7 on two reads, one waiter, window until 20:00 (longer than the tier-2 gates: target 150 min, hard stop 210 min); name the live seats at the stamp.
- S3: Q-1 YES, Q-2 YES (below), Q-3 YES, Q-4 NO GO parks at round 1 of 2, round-2 fix kit.
- S4: all seven items YES (same grant as B946 with 9820-9829 and HPSMPOC-387).
- S5: target 150 minutes, hard stop 210 minutes after the Step-0 date.
- S6: ls-remote branch 963f718d, main 37bc6323, merge ref ff8ec243 (parents 37bc6323, 963f718d), PR open, the check table above, open PRs 253/252/251/250/248/245.
- S7: model: claude-opus-5-5 -- G1 -- gauge <n>% -- load1 <n>.

## Q-questions
- Q-1: judge the landing tree (head onto the main read at Step 0, "comb"), expected equal to the head tree and the merge-ref tree. Default YES.
- Q-2: a name token that appears ONLY in a route id used in a URL/href (see below). Default: Note if main's /customers/quollridge already carries it for Demo; Blocker if the PR adds any other exposure; Blocker for any text, title or accessible name.
- Q-3: Fleet view words ("Firmware inventory: Not connected", "Policy coverage: Not measured", "No printer management connection in this build", estate rows "Firmware and advisories ... vendor advisory matching", "HPSM or device policy ..."). Default: ticket and design text are allowed, listed for the product owner's veto; Major only if a sentence implies a connection will exist or shows a tool value.
- Q-4: NO GO parks the PR at round 1 of 2; Tuesday writes a round-2 fix kit.

## Wrong or weak at source
1. Alias, real: the held customer's route id is `quollridge` (lib/customers.ts line 29 at main) and its API id is `CUST-SYN-QUOLLRIDGE`. Every /security/<id>/... URL and every chooser href therefore carries the name token for a Demo viewer. The builder's claim "Quollridge absent from body.outerHTML" (STATUS lines 107, 123) is probably case-sensitive. The kit makes the gate re-measure with /i and compare against main's existing /customers/quollridge pages. Not a text leak as far as I read.
2. Chooser fail-closed: useSecurityLabels returns the neutral word until getMe and getMetricsSummary are both ready, and on error (state not "ready"). I read this as fail-closed; the kit probes it with failed and slow requests and plants p13/p14.
3. SecurityFrame.tsx renders its own `<main id="main">`; the kit asks for a main count of 1 in the browser (the (app) layout must not add one).
4. Phase line: no HP-tool call found in the five files I read. Wording risk only: the tiles/rows named in Q-3, and the "Fleet and devices" title vs "Fleet & devices" menu label.
5. Builder claims already stale: "12 of 12 plants red" was run BEFORE the merge (STATUS says "not re-run after the merge"); "unit repeats x20" likewise; "CodeQL: no analysis on a push-only ref" is superseded (PR exists, analyses are arriving); base 3242 is pre-main-moves (the STATUS itself says not comparable). The whole-suite a11y journey failed 3 of 3 on the builder's tree AND on base under load; it passed as CI shards. The kit therefore uses the five shards plus 3 alone runs of a11y/shell-sidebar.
6. PR body: classification "21 product, 10 test" counts the two testing/ helpers as product (15 + 4 pages + 2 = 21); by purpose 19/12. Minor.
7. Mode line "Partner workspace" repeats the Main menu's first group label (builder Open a): confirmed in SidebarMenu.tsx line 15 text; listed for the product owner.
8. Not read by me: the Jira ticket (no GET made; scope and acceptance are quoted from the builder kit as RELAYED, the gate GETs it), the design file (read-forbidden), returnPath.test.ts.

## Reasons not to launch now
- Analyze (javascript-typescript) and (csharp) and CodeQL were still running; the gate's C8 waits up to 45 minutes, so launching now is fine but the verdict will land after CI finishes.
- Possible semantic overlap with the services lane (b949 kit names GlobalNav.tsx line 50 and shell-sidebar.spec lines) and the held sidebar-spec lane; the gate re-reads both at the verdict. Load is the main constraint (launch_when_cool).
