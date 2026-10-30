STARTABLE: YES (after your stamp; load1 14.4 at 16:07, so the launch waits on launch_when_cool; one customer-facing word change is queued for the product owner's veto, Q-1, and does not block the launch)

# B949 drafter report (Sonnet 5.5, 2026-10-30 about 16:05 to 16:45 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B949_SEAT-H71_hpsmpoc-383-services.md` (153 lines; 9 lines with four underscores = 8 slots + the last line, counted by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0; non-ASCII lines 0). Read-only everywhere else: gh `-X GET` under the project `.gh-config`, Jira GET through `.tools/b649/jira.py`, no ref written, no mail, no `cd`, no hosted HTTP, no test run. Nothing was written in the project's Briefs folder.

## BLUF
Seat `Datasec/HPSM-POC-H71` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes), branch `b949/hpsmpoc-383-services` off `37bc6323`, two commits. Commit 1 restyles `ServicesHub`, `OfferSheet`, `ImplementationScreen`, `ManagedServiceScreen`, `service-parts` (v1.2 cards, numbered badge, track, tabs), words and figures untouched. Commit 2 (isolated so a veto is one forward revert) changes "Service offers" to "Delivery phases" in 7 code strings (GlobalNav line 50, hub crumb and `PageHeader title`, three sub-page crumbs, the hub `metadata.title`) and 13 test lines. New test file `Services.restyle.test.tsx` proves AC 2 (hub h1 = menu label = metadata title) red-first. `Services.test.tsx` stays byte-equal. Ends at READY FOR QA; tier-2 gate follows.

## Facts re-measured (instrument; control)
- Main `37bc632362c21cc8688ba70d305e88b18700d323` (`commits/main`, 16:0x). Open PRs #245, #248, #250, #251, #252: `pulls/<n>/files` intersected with the 15 lane paths by `grep -c -x -F -f`: 0 each (control: #252 list + a planted `ServicesHub.tsx` = 1). 22 `refs/heads/b9*` read with `compare/main...<branch>`: 0 on 21; b930 shows 4 (GlobalNav.tsx, GlobalNav.test.ts, AppShell.sidebar.test.tsx, shell-sidebar.spec.ts) only because #249 was squashed into 37bc6323 (it is landed, not live). `compare/e21d8044...37bc6323` lists the same 4 of my paths. `matching-refs/heads/b949` 0 (control: `heads/b9` lists 22). `lsof` 9800-9809 = 0 (and 9700-9999 = 0). Panes: tuesday, G219-G223, H59, H63, H66, H68, H69, H70, fleet-monitor: no H71. Load 14.40.
- Files at 37bc6323 (tarball, line counts and sha256 prefixes in the kit): ServicesHub 42, OfferSheet 57, ImplementationScreen 113, ManagedServiceScreen 112, service-parts 79, Services.test.tsx 79 (6 `it(`, no title or class assertion), the four pages 8/8/8/12, GlobalNav.tsx 124 (**line 50** is `label: "Service offers"`, control: `grep -n` printed it), GlobalNav.test.ts 170.
- Label strings by program (`grep -rn -i -I 'service offers'` over `web/`): 7 quoted code strings in the lane (GlobalNav 50; ServicesHub 22, 23; OfferSheet 39; ImplementationScreen 30; ManagedServiceScreen 24; services/page.tsx 4) and 13 test lines (GlobalNav.test.ts 12, 14, 15, 21, 92, 143, 153; AppShell.sidebar.test.tsx 60, 75; shell-sidebar.spec.ts 11, 370, 417; playbook-partner.spec.ts 17).
- Jira (GET): HPSMPOC-383 quoted verbatim (BLUF, scope, AC 1-2, Files); HPSMPOC-369 read for its role rule. Both Backlog, 0 comments.
- Design file sha256 `fb799db8...e8afeaa` equal. Delta section 2.10 quoted from line 128: "... Restyle only; rename nav \"Delivery phases\"."
- Model rows C2:92, G2:109 (control L6:85, G-cap:111); `models_latest.json:23` `claude-sonnet-5-5`; `brief_seat.sh:24` defaults to opus.

## Sweep pointers I found WRONG or incomplete
1. **"Delivery phases" is a menu-only word in the design.** The design's `MENU_SPEC` (line 293) says "Delivery phases", but its own page `offers()` (line 198) prints the heading "Service offers" (eyebrow "SERVICE DELIVERY / PHASES"), and its older nav map (line 156) also says "Service offers". The ticket's AC 2 (page title = menu entry) and the delta make the title follow the menu, so the kit applies the word to both. This is what the product owner is vetoing in Q-1.
2. **The sweep says "update `GlobalNav.test.ts` if it pins the label".** The label is pinned in 13 lines of FOUR existing test files (above), three of them outside the sweep's row (`AppShell.sidebar.test.tsx`, `shell-sidebar.spec.ts`, `playbook-partner.spec.ts`; the last two are e2e). Without those edits CI goes red (Q-2).
3. **Collateral outside the lane:** `partner/PartnerDashboard.tsx` line 158 (open PR #252, H5) has a tile titled "Service offers"; after commit 2 lands the dashboard and the menu disagree (Q-3).
4. The sweep calls H7's `GlobalNav.tsx` lines "44-45 flags"; at 37bc6323 those entries are `built: true` and the Services entry is on line 50 (still true). The H7 coupling is gone: #249 landed.

## D-decisions (mine, in the kit)
- D-1 base 37bc6323, no rebase if main moves unless a lane path moves. D-2 two commits (restyle, then relabel) so a veto is one forward revert. D-3 `Services.test.tsx` byte-equal; only the 13 word lines change elsewhere. D-4 one new unit file proving AC 2 by program (imports `MAIN_NAV` and the page `metadata`), red first. D-5 the hand-drawn implementation progress bar may stay (restyle needs no behaviour change). D-6 breakpoints re-tuned only on 1024 px evidence, 10 right-edge numbers at base and head. D-7 no second sample notice or badge (the earlier lane removed them on purpose). D-8 target READY 150 minutes, hard stop 240.
- Sample-content guard (phase scope): the Managed and Implementation pages show sample data; the kit forbids added words implying a connection, feed, sync, SIEM, Security Manager or Fleet Threat data, checked by a grep with positive controls. The existing playbook link "Security Manager output (Playbook)" is a link to a playbook page, kept byte-equal.
- Tier-2 gate; both BINDING lines of today's gate kits carried (rerun a load-red ALONE 3 times; markers from an EXIT trap) as STANDING LINES 12 and 13.

## Q-questions for Tuesday (each with a default)
- **Q-1 (customer-facing word, THE LABEL):** apply "Delivery phases" to the menu entry and the hub title, as the delta quotes it. Default YES; Tuesday lists the builder's CHANGED-STRING TABLE (file, line, old, new) for the product owner's veto; veto = revert commit 2 only. Alternative the owner may prefer: keep "Service offers" in both places (the design's own page heading), which makes the lane restyle-only.
- **Q-2:** may the builder edit the word on the 13 test lines, including the three outside the sweep's row? Default YES.
- **Q-3:** `PartnerDashboard.tsx` line 158 tile "Service offers" (PR #252): default not this lane; Tuesday queues a one-line follow-up (tile title and its test) after #252 lands.
- **Q-4:** gate round. Default round 1 of 2 on the class "services restyle plus label".
- **Q-5:** hard stop. Default target READY 150, hard stop 240.

## UNMEASURED
Suite counts at main; Chromium; how the three-card row and five-column task grid read at 1024/1280 beside the sidebar; the document `<title>` template (`app/layout.tsx`); whether axe flags the new badge; Consultant and Demo browser sessions (`signIn` takes no role, so those roles are covered by unit tests only); CodeQL on the new head.

## Outside-the-fences disclosure
No fence breached. Scratch under `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/8a8e5624-4358-43cb-ab64-af03ddbc5b41/scratchpad/drafters/b949/` (a tarball of 37bc6323, PR and branch file lists, a Jira reader script). I extracted the tarball as data and never executed anything from it. One of my greps printed far more than intended (the content JSON packages matched "Phase 2" text); no fence effect. The kit was written with the Write tool and checked by a python scan: 0 non-ASCII lines (the kit writes the en dash as the text "[U+2013]").
