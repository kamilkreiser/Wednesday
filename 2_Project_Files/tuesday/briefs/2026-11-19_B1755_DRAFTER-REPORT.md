STARTABLE: YES - once Tuesday posts and the product owner rules the NEW deploy card and the slots S0, S4a (SELLER-CHECKS), S4b (TEMPLATE-CHECK), S4c (WORDS) and the other Stamp slots are filled. The kit refuses at Step 0 without the new card's ruling, and with WORDS = `not approved`.

# B1755 drafter report (SEAT-D68, MPS hosted deploy kit re-cut for main 50d2a471)
Saved by Tuesday (s294) from the Opus drafter's in-session reply. Condensed by Tuesday; the kit is the authority. Every
figure is the DRAFTER's (it ran no az and touched no host: live facts are RELAYED from earlier records).

## Files
Kit `2026-11-19_B1755_SEAT-D68_mps-hosted-deploy-main-50d2a471.md` (145 lines, 72,342 bytes, ASCII, 15 unfilled slots);
sidecar `.measured` 120 of 120, stamp_check rc 0; `2026-11-19_B1755_CARD-FACTS.md` (90 lines). Scratch
`fleet/state/s294/d1755/` (raw files at 50d2a471, card reads, compare JSON, the 50d2a471 CI package, fill.py, sidecar.py).

## Ride-along since the deployed 5e800095 (gh api compare, 20:16:25: 21 commits, one parent each, 38 files, 0 open PRs)
- Seen by users: #219 73eef991 a new table "Projection" on the purchase result, only for a signed-in user with the
  PricingAnalyst role (that role gives internal-metrics, CallerResolver.cs:24), ten words not yet ruled; #218 e036c966 the
  refusal for an over-long quote reference reworded (QuoteEndpoints.cs:1436; ruled, C-64 and C-108); #204 87dc2623 once
  the settings step runs, saved templates survive a restart (its warning is for operators only).
- Seen by nobody: #200 to #203, #205 to #211, #213, #214, #216, #217, #220 (tests, docs, comments, CI, the dev stub, the
  settings-file fix). Staff-only and not reached in this deploy: #212, #215 (the importer note, ruled C-180, C-181).
- Package: CI artifact 14515692831, run 44494603501, 8 of 8 green, expires 2026-11-26T09:30:43Z; mpscalc.zip 51 files;
  verify rc 0 and the wrong-commit control refused; against the 5e800095 package 4 files changed (Api, Engine, Import
  DLLs, index.html) and two web bundles swapped (the served bundle name changes, so it proves the swap); 45 byte-equal.

## Predicted settings difference (by program, against the 16 November saved file)
Added `MpsCalc__Templates__Path`; removed none; changed none (18 names in the list and in showcase.bicep 60 to 91 are
set-equal; the 10 shared fixed values equal; the 7 computed values equal when the saved ids are supplied; by boolean only).

## STOP list S-1 to S-25 (condensed)
A slot unfilled or outside its allowed values; WORDS = not approved; the new card not ruled as S0 says or the 18:00 card
not marked superseded; S2 not 50d2a471; main moved; CI or the package not green, missing or expired; a target assert
fails (21 commits, 38 paths, showcase.bicep exactly 2 added lines, the floor commit); the az login expired (STATUS then
carries the two az login / az account set lines for the product owner); wrong tenant, subscription or user; the site
runs anything but 5e800095; M1/M2/M4 any extra, missing or changed setting or a budget start other than 2026-10-01; M3 a
supplied id differs by hash from the live one or is not GUID-shaped; M5 the what-if without ids reaches Azure or az asks
to install Bicep; M7/M9 any what-if difference beyond the one added name; M8/M10 the read-back fails or the create ends
Failed (read everything back first, never retry); the file-list property breaks or the way-back package is unproven;
deploy rc 1, or rc 3 and unproven; the warning prints or the start is refused; the test login fails when SELLER-CHECKS =
run; the synthetic template not listed after the restart; an end-check difference, a leak, a secret or client id in any
file; the hard stop.

## What differs from B1749
Commit 50d2a471 (21 commits, 38 files); Step 1P predicted to pass; the review's ten measures carried as M1 to M10 (M3 ids
by hash at 1P, before the what-if and before the create; M5 a what-if without ids refused locally; M8 a failed create
means read back then stop; M6 optional, not run by default); the authority is the NEW unruled card; three new slots
SELLER-CHECKS, TEMPLATE-CHECK, WORDS; the login check at Step 0.9 with a live token-expiry read; the writes outside the
resource group stated exactly (the subscription-scope deployment record; the resource group re-asserted with unchanged
tags); the budget start read before and after with an ARM GET; the package fetched before the what-if; apply before swap.

## Corrections to the commission
1. The operator warning sentence has no live ruling for its WORDS (the 18:00 card that said "goes as written" is
   superseded; the 16 November ruling chose a warning, not its wording): it is added to the WORDS slot.
2. `decision_queue.sh list` not used (DRAFTER_RULES forbids it); `show` only.
3. C-45's quoted words are at line 660 (654 is the heading).
4. The CI run finished green at 20:30:55: the kit carries measured package facts.
5. In practice possibly EVERY hosted user sees the projection table: on 2026-10-16 the product owner ruled every user
   holds all four roles; the 2026-10-13 record lists his own account and one staff guest with PricingAnalyst. Hosted users
   are staff; customers do not sign in.
6. `Briefs/2026-10-13_B66_STATUS.md:112` in the MPS project prints Entra client ids in plain text (not copied anywhere).

## Recommended defaults for the card (one card, four options)
a deploy now with these defaults; b deploy after the renewal with the seller checks and the test template; c the words go
to review first; d nothing. (i) deploy now; (ii) skip the seller checks again (none of the 21 changes touches the
screens they read); (iii) do not run the template check (no permitted machine login without the renewal; the store is
shown by the setting, the start log and the folder); (iv) approve the words as written (internal-only labels).
Stamp S4 defaults: Q1 the 1P stop strict; Q2 only the two named subscription-scope writes; Q3 a budget start change
stops; Q4 M6 not run; Q5 one restart, only after W3; Q6 apply before swap.

## UNMEASURED
Today's live settings, store, activity log and served bundle; Azure's what-if and create output and the refusal without
ids; Azure's own length rule at apply time; the budget service on an update with the same past start; whether the
project's az login is still valid and whether Bicep is installed in az; which users hold PricingAnalyst today (last
record 13 October); whether the web screen displays the server's #218 refusal text; the local way-back package; the
data/templates folder on the live site; the seed secret's state; the zero code-scanning alert count had no firing
control (the analyses list answers: 4 analyses on 50d2a471, 0 results each).

## Disclosure
One CI artifact downloaded from GitHub by GET; `deploy-package.py verify` run on scratch copies; no az, no test, no build,
no request to any host. Card ids appear only in Step 0.4 of the kit (STATUS only).
