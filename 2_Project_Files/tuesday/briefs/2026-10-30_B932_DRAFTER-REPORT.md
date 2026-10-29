STARTABLE: YES (after your stamp; H3 need not land first: the kit's D-3 takes H3's landing by a forward merge commit, never a rebase)

# B932 drafter report (2026-10-30 about 10:23 to 10:55 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B932_SEAT-H63_hpsmpoc-372-partner-home.md` (149 lines; 9 four-underscore lines = 8 slots + the last line, by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0; non-ASCII lines 0 by `LC_ALL=C grep -c '[^ -~]'`, control: a planted ellipsis line reads 1). Read-only everywhere else; gh `-X GET` under the project `.gh-config`; Jira GET through the sweep's GET-only reader; no `cd`, no hosted HTTP, no ref written, no message. No file was written in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H63` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes) re-lays `/home` (`partner/PartnerDashboard.tsx`) into the v1.2 summary columns: the tiles and PhaseFlow unchanged and in place, then a 1.55fr / 1fr grid from 1050 px with a NEW pipeline table plus the three existing panels on the left, and "Recommended next actions" (four links to built pages) plus "Practice readiness" on the right. "Where to next" and the CTA stay. The new tests go in a NEW unit file. Ports 9640-9649, branch `b932/hpsmpoc-372-partner-home`, tier-2 gate after.

## Facts re-measured (instrument; control)
- Pins: main `e21d80442980fb61ad9fb11aaf393c0b20c0ad2d` (`commits/main`); open PRs 0; `matching-refs/heads/b93` = one old head `b93/gate-b94-notes`, no `b932`; `lsof` 9640-9649 = 0; panes `%0 tuesday`, `%1 fleet-monitor`; load1 2.35 at 10:23.
- Port block: `964x` appears only in finished kits of 10-25 and 10-27 (16 kit ids listed in the kit); `H63` in 0 kit files (control `H53` 25).
- HPSMPOC-372 read whole by Jira GET (0 comments); What and AC quoted verbatim in the kit. Depends -368 and -371 are both in main.
- **Sweep pointer correction:** the sweep row says "pipeline table left" as if a table exists. **There is no pipeline table on Home at main**; the nearest is the "Customers by stage" bars. The kit builds one from `buildDirectory` over the page's EXISTING `api.listCustomers()` call (no new call). `useDirectory` is ruled out: it fans out one `getCustomer` per customer through `openapi-fetch`, which `PartnerDashboard.test.tsx` does not mock.
- Existing pins the layout must not break (measured): `playbook-home-phase-flow.spec.ts` 39-41 pins PhaseFlow BETWEEN "Welcome back" and `kpi-customers` (so the prototype's placement of its phase boxes in the left column cannot be taken without editing a spec); `PartnerDashboard.test.tsx` line 85 counts exactly 3 "Sample" labels on the page; `playbook-event-states.spec.ts` line 50 finds the page's loading and error strings with `exact: true` (a duplicate is a strict-mode failure). All three are written into the kit's SHAPE and plants.
- Built pages: `/assessments`, `/workspace`, `/engagements`, `/action-plan`, `/services`, `/revenue`, `/playbook/<id>` (modules `partner-readiness`, `phase-1`, ...), `/metrics`; `/training` is `built: false` (GlobalNav line 45) with no route directory.
- No viewport arbitrary breakpoint (`min-[Npx]:`) is used anywhere in `web/src` today (count 0); arbitrary grid templates are common.

## D-decisions (in the kit)
- D-1 PhaseFlow stays above the tiles; `home/**` byte-equal by default.
- D-2 The prototype's four targets re-pointed to built pages: `/assessments`, `/playbook/phase-1`, `/services`, `/engagements` (no `/training`, no Good / Better / Best, no customer preview).
- D-3 H3-LANDED RULE: take H3's landing by `merge --no-ff origin/main` (one forward commit, plain fast-forward push), allowed only when main's moved files miss YOUR PATHS; re-run tests and screenshots after.
- D-4 Breakpoint literal `min-[1050px]:`; the seat may move to `xl:` with screenshots as a Correction.
- D-5 Practice readiness reads the same summary as the tile.
- D-6 "Where to next" and the CTA kept unchanged.
- D-7 Sonnet C2 builder, G2 tier-2 gate; target READY 180, hard stop 270.

## Q-questions for Tuesday (each with a default)
- Q-1 Is a merge commit of main into the lane branch acceptable for taking H3's landing (D-3), given every other kit forbids rebase? Default **YES** (the squash landing flattens it; the alternative is a fresh seat on a new base).
- Q-2 Keep "Where to next" (four cards: action plan, revenue, services, playbook) beside the new four "Recommended next actions", or fold it into the right column? Default **KEEP** ("remove nothing the product owner specified"; the page came from his own dashboard mock). Two link sets overlap on `/services` only.
- Q-3 Breakpoint literal 1050 (ticket) or `xl:` 1280 (sweep's "re-tune your lg/xl")? Default **1050**, seat may move with evidence.
- Q-4 The five-width no-sideways-scroll proof is a SCRATCH Playwright script, not a committed spec (the standing line forbids a new spec without asking). Default **scratch script**; say yes here if you want a committed spec instead (it would need the shard check read).

## UNMEASURED
Anything rendered; unit and e2e counts at main; how the 1.55fr / 1fr split reads at 1050 to 1280 beside the 228 px sidebar; whether four KPI tiles fit at 1280 with the sidebar; when H3 lands; whether H3's kit B929 touches anything beyond its three files (its kit was not yet in `tuesday/briefs/` at drafting).

## Outside-the-fences disclosure
None. Scratch only under `scratchpad/drafters/b932/` (a tarball of `e21d8044`, extracted). One Jira GET of HPSMPOC-372 and one GET search, through `scratchpad/s1015/jr.py` (asserts the `project = HPSMPOC AND (` prefix).
