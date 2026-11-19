STARTABLE: NO. As drafted the kit stops at Step 1P before any write: the infrastructure apply at 317bbb14 would REMOVE the hosted app setting `MpsCalc__Feedback__Path` (turning off the hosted feedback store) as well as add the template setting; and the template create-and-list check needs a signed-in user while the only machine login is the expired one.

# B1749 drafter report (SEAT-D67, MPS hosted deploy of main 317bbb14 with the infrastructure apply)
Saved by Tuesday (s293) from the Opus drafter's in-session reply. Condensed by Tuesday; the kit is the authority. Every
figure is the DRAFTER's (it ran no az and touched no host: live facts are RELAYED from the 2026-11-16 run).
THE KIT IS NOT READ BY TUESDAY AND NOT STAMPED. NOTHING WAS DEPLOYED.

## Files
Kit `2026-11-19_B1749_SEAT-D67_mps-hosted-deploy-main-317bbb14.md` (115 lines, 55879 bytes, ASCII, 12 unfilled slots);
sidecar `.measured` 89 lines (89 of 89). Scratch `fleet/state/s293/d1749/` (raw files at 317bbb14, both CI packages, the
card reads, the compare JSON).

## THE FINDINGS THAT CHANGE THE DEPLOY (each measured by the drafter from files, none from the live site)
1. **The apply removes the feedback setting.** 17 setting names saved by the 16 November seat against the 17 names in
   `infra/modules/showcase.bicep` lines 60-90 at 317bbb14: ADDED `MpsCalc__Templates__Path`; REMOVED
   `MpsCalc__Feedback__Path` (set by hand on 2026-10-13, `B73_STATUS.md:146`, never added to the infrastructure file,
   which says at :58 that it replaces every app setting). With it blank the Api opens no feedback store
   (`FeedbackStore.cs:208`): the 4 stored feedback items and 2 attachments stop loading. The other 16 compare equal once
   the two client ids are filled in.
2. **Two Entra client ids come from environment variables** (`bicepparam:8-9`) that are not in the project `.env`; without
   them the apply BLANKS four auth settings. The kit fills them in memory from the live values.
3. **`budgetStartDate` defaults to utcNow:** the apply would move the budget start from 2026-10-01 to 2026-11-01.
4. **The apply is subscription-scoped** (`main.bicep:8`): it writes a subscription-level deployment record and re-asserts
   the resource group (not "nothing outside the resource group").
5. **No permitted caller for the template check:** create and list need a Seller, Approver or Administrator
   (`TemplateEndpoints.cs:17`); the only machine login is the expired one.
6. **The deploy tool does NOT refuse a pinned older commit:** `deploy-from-ci.sh:50` picks the CI run by commit and `:57`
   verifies against it; nothing compares the pinned commit with main. (So holding PR #218 for the tool's sake is not
   needed.) Package: CI run 44431915572, artifact 14488185359, expires 2026-11-26T01:03:10Z.
7. The 16 November seat used the project's own `az` USER login (the product owner's, `infra/README.md:30`), not a
   service principal.
8. The package changes 3 DLLs (the Import one carries lineage-note words ruled in C-180 and C-181); the served bundle is
   unchanged.

## How the kit guards the apply
A names-plus-value-hash dump before and after (never a value), compared by program with two controls; a what-if classified
per resource and setting; the readback after the apply must read added 1, removed 0, changed 0. Its STOP S-12 (the
comparison at Step 1P) is PREDICTED TO FIRE as things stand. 26 STOP conditions in all (S-1 to S-26).

## Drafter's defaults
Q1 the feedback-path removal stops the seat (no rule relaxed); Q2 no caller named, so the template step does not write and
the seat ends STOPPED after the swap with the deploy standing; Q3 the subscription-scope what-if and create not allowed;
Q4 the budget start move not allowed; Q5 unruled words stop; Q6 one restart only after the template create. Order: apply
first, then the package swap. Way back: to 5e800095 only under the 16 November strict rule; settings never rolled back;
nothing set by hand.

## Environment facts to re-read at any stamp
main; CI run 44431915572 green and the artifact's expiry; the card's status; tenant `ec01829b-...`, subscription
`a6b8fe11-...`, resource group `mpscalc-showcase-rg`, site `app-mpscalc-showcase-u6agl3edszqvs` (all RELAYED from 16
November); the az user chain and the project AZURE_CONFIG_DIR; the 17 hosted names against the 17 bicep names; panes,
load, disk.

## UNMEASURED
The what-if output; whether the budget exists and its start date; today's live settings, store, activity log and bundle;
the local way-back package; that the templates folder is created on the live site; that the 16 November login is a user;
that the warning sentence prints in a real start.
