# BLUF — A SHORT Vision seat with four items, then wrap. (1) VSP-65, the only open ticket on your board: the Postgres pool has no query timeout, so a never-answering session store hangs every signed-in request. Build it to READY FOR QA. (2) File BCR3-P2 (the Polish finding) as a BACKLOG.md line. Tuesday GO'd it and it was never filed. (3) Report the CI result for QuickQuote main 6fbebd9. (4) Measure whether LIVE QuickQuote (v2.33) has the scheduled retention purge or only the lazy on-read delete, and by what date that matters. Measure and report only; publishing is Kam's typed word.

**Addressed to the cockpit seat `Datasec/Vision_Sales_Portal`.** No other Vision seat is live.

## AUTHORITY
- Tuesday's standing morning grant (Kam, 2026-08-12): sweep each active board and start its agent on agent-actionable tickets. Kam's new-account login 2026-09-27 ~08:2x AEST, verbatim: *"New account logged in. Please keep going with the work."*

## HELD (production is live here: datasec-sales-portal-rg and hpas-quickquote are production)
No deploy, no publish, no production change of any kind, no Key Vault or app-setting change, no merge without a QA gate verdict at the head plus Tuesday's GO, and nothing to any human but Tuesday. A change that would need production to prove it is reported as NOT TESTED, never run.

## ITEMS
1. **VSP-65.** Read the ticket whole, and do your PRIOR-WORK CHECK first (git log -S on the pool config, CLARIFICATIONS, history). Branch from current main (read `git ls-remote` first). Fix with a bounded query/statement timeout that fails LOUDLY (a named error, not a hang). Red-proof: a stalled store hangs at base and gives a bounded failure after the fix, plus a control showing a healthy store is unaffected. Full suite. Tier 1 (the session/auth path). READY FOR QA to tuesday-agent@ with branch + head sha, sets not counts, PRIOR WORK, NOT TESTED.
2. **BCR3-P2.** Take its wording from the gate-8 report (BCR3 round 4). Add one BACKLOG.md line, docs only, on its own branch, with its sha in your reply.
3. **CI on QuickQuote 6fbebd9.** The run id and its result, read with your own gh identity. If you cannot read it, say why.
4. **Retention purge.** Which commit is live (v2.33, reported from d4426f8), and is the scheduled purge (03a0682) in it or not? If it is not, what does the live app do with a quote past 12 months, and when is the first quote that could be affected due (the "~23 October" date carried in Tuesday's notes is unverified: measure it)? Report only. The fix reaches production only on Kam's word.

## REPLY
Plan confirmation first: `[Datasec/Vision_Sales_Portal -> Tuesday] QUESTION: plan confirmation`, and start the read-only parts without waiting. Then the READY for item 1, and one STATUS mail covering items 2-4. Wrap when done: mail the wrap to tuesday-agent@, and Tuesday retires the pane by hand.

PROVENANCE:
- VSP-65 is the only open VSP ticket (Backlog, Medium, updated 2026-09-23) | /Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/board_count.sh jira with your own 4_Credentials/.env, project = VSP AND statusCategory != Done = TOTAL 1 - Tuesday's tool, not yours | read 2026-09-27 08:4x
- items 2-4 owed | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md DELTA 92 and 81 (Tuesday's notes, relayed, not re-measured) - Tuesday's file, not yours | read 2026-09-27
- live QuickQuote v2.33 from d4426f8; retention purge follow-up 03a0682 | /Volumes/KK_T9_External_HDD/TUESDAY/0_Brain/tasks/NEXT-PICKUP-TUESDAY.md older deltas (relayed, unverified) - Tuesday's file, not yours | read 2026-09-27
Self-check note: nothing here touches production; item 4 is measure-only; item 1 ends at READY FOR QA.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 08:38
