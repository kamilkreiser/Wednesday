STARTABLE: YES, WITH ONE KNOWN WAIT (after your stamp. The lane cannot reach a green suite without one line of `nav-dead-ends.test.ts`, which is H61's file, and one token of `server/auth/returnPath.ts`. The kit lets the seat build everything now and do those two lines only after H61 (B930) lands. That is its D-7 tail, ending `STOPPED: NEEDS TUESDAY D-7`.)

# B937 drafter report (Fri 2026-10-30 about 10:36 to 11:05 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B937_SEAT-H68_hpsmpoc-387-customer-security-preview-a.md` (157 lines; 9 four-underscore lines = 8 slots + the last line; at-sign slots 0; non-ASCII lines 0, control: a raw byte reads 1). Seat `Datasec/HPSM-POC-H68`, ports 9690-9699, branch `b937/hpsmpoc-387-customer-security-preview-a`, ticket HPSMPOC-387. Shape copied from B928 (stamped) and B931. Everything was read-only: gh `-X GET` under the project `.gh-config`, Jira only through `.tools/b649/jira.py` (GET), no `cd`, no hosted HTTP, no ref written. No file was written in the project's Briefs folder.

## BLUF
HPSMPOC-387 asks for a Partner/Customer view switch, the customer menu from the `customer-nav.ts` stub, and three read-only views (Security dashboard, Fleet and devices, Security assessments) under new `components/security/**` and `app/(app)/security/**`.
- **Switch:** two `aria-pressed` buttons, mounted from `Sidebar.tsx` line 72, after the menu. Two existing tests that are not ours rule out links and rule out placing it first: `AppShell.sidebar.test.tsx:219` expects 8 links in the aside, and `shell-sidebar.spec.ts:227` expects the first Tab to land on Home. `AppShell.tsx` is never touched. If the seat finds it needs AppShell, it stops.
- **Mode and routes:** the route is the mode (`/security...` means customer). The views live at `/security/[customerId]/<view>` plus a `/security` chooser.
- **"Reviewed":** the finding's own disposition is accepted, amended or risk-accepted. The kit adds a new single-source `reviewed.ts`. No existing helper means this: the report still shows `open` findings.
- **Unreviewed answers:** no number derived from them appears on any part-A view.
- **AC tests:** a spy on both browser API clients covers no-write; there are also no-price, Demo-alias and role tests; 12 plants.

## Facts measured (instrument; control)
- **Repo and seats:** main `e21d8044` (`commits/main`). Open PRs 0. `matching-refs/heads/b937` 0 (control `heads/b93` 1). `.tools/b937` absent. Panes at 10:45: tuesday, fleet-monitor, NexusAI-R92, HPSM-POC-H59..H63 (no H68). Ports 9690-9699: 0 listeners. Kit scan for `969x`: 0 (control `962x` finds B930). load1 was 6.33 at 10:36 and 5.95 at 10:45.
- **Jira:** HPSMPOC-387, -388 and -393 read whole; each is Backlog with 0 comments. -393 is `gather` and "NOT to be built" (Framework alignment).
- **Stub:** `customer-nav.ts` has 8 entries with the literal type `built: false` and its test says "rendered by nothing". Its importers are its own test and `nav-dead-ends.test.ts:6`.
- **Roles and reads:** `Role` is consultant | admin | partner | demo (`session.ts:8`). Every read used is x-roles `[Admin, Consultant, Partner, Demo]`. The `(client)` layout has no AppShell or Sidebar, so a customer with no role can never see the switch.
- **Data:** the API result carries the real `customer.name` (never rendered). The mock seeds no reviewed finding, so the evidence script must make one through the consultant flow.

## Sweep pointers found WRONG or incomplete
1. "0 shared files" holds for paths, but there are three semantic couplings:
   - **(a)** `nav-dead-ends.test.ts:26` uses `>= 9` and counts unbuilt customer entries. It turns red at H13 alone (6 left), and red again after H61's planned `>= 8` (5 left).
   - **(b)** `returnPath.test.ts:73` requires `RETURN_SEGMENTS` to equal the app folders, so a new `security` folder turns it red.
   - **(c)** `loading-states.test.tsx:23` pins 4 layouts, so the kit allows no layout file under security.
2. **H61's kit B930** says H13's "eight built:false entries stay under your guard" (wrong once H13 lands). It does not name `returnPath.ts`, but H61's own `/training` folder breaks the same test. It also lists only lines 60/74 of `AppShell.sidebar.test.tsx`, but adding Training probably moves line 219's link count from 8 to 9 (UNMEASURED: no run).
3. The design puts the switch in the top bar. The sweep's sidebar choice holds only as buttons placed after the menu.

## Q-questions for Tuesday (recommended default first)
- **Q-1 Gate tier: tier 1 (G1 line 108), Opus first, round 1 of 2 on the class "customer security preview".** Why:
  - AC 1 is a confidentiality rule about customer findings, and a leak only shows on screen.
  - AC 5 is the Demo alias surface in front of HP.
  - The tail edits a sign-in return-path allow-list in `server/auth`.
  - G1 names "anything handed to a client tester", and these views are in Kam's Monday screenshot set.
  - The alternative is G2, the sweep's default.
- **Q-2 Reviewed rule: disposition only (D-3).** The alternative also requires assessment status reviewed or report-issued.
- **Q-3 Answer-derived surfaces: none in part A (D-4).** The alternative builds the design's per-question table, worded "Pending consultant review".
- **Q-4 D-7 grant: yes**, one line each in `nav-dead-ends.test.ts` (floor 5) and `returnPath.ts` (`"security"`), only on a base or merge that holds H61's landing. The alternative is to hold H68's launch until B930 lands.
- **Q-5 Times:** target READY 300 minutes, hard stop 420.

## What HPSMPOC-388 (wave 3) will need from this lane
- From `components/security/`: `reviewed.ts` (`REVIEWED_STATES`, `reviewedFindings`), `SecurityFrame` with the banner, the alias label hook and its list variant, and the held-vs-API loader.
- `customerNavHref` and the `/security/[customerId]/<slug>` pattern. 388 flips `findings`, `roadmap`, `reports` and `assurance` to built, and lowers the `nav-dead-ends` floor to 1 (Framework alignment stays held).
- The no-write and no-price harnesses, written over an exported VIEWS list it can append to.
- Its own inputs: H16's `remediation-store.ts` (-377), read-only, and `listReports`/`listNarratives` GETs for its "issued and approved" rule.

## Reasons not to launch now
None that block. Launching now means the seat ends at D-7 waiting for B930. Load is near 7 with five HPSM-POC seats live, so it is `launch_when_cool`.
