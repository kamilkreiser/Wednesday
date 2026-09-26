# BLUF: Excellent measurement work, thank you. Three things. (1) NEW ITEM: build the QuickQuote retention-purge FIX to READY FOR QA. The live purge fails every 6 h. (2) BCR3-P2 f255db8 (docs only): GO to merge, after you confirm the merge deploys nothing. (3) VSP-65 READY received; its tier-1 gate is being drafted now. Keep the seat open for items 1-2, then wrap.

## 1. Retention purge fix (QuickQuote, tier 1: it deletes customer data)
Your measurement: the stage3 purge throws "Unrecognized 'Edm.Int32' literal" on every run (Log Analytics, 6 runs in 36 h), so "pending" rows are never removed. Build the fix the BACKLOG names: an Int64 literal, or the SDK's odata tag, whichever the table SDK documents as correct. Read the SDK docs or source, do not guess.
- PRIOR WORK: d88af73 (the rebased 03a0682) and the BACKLOG entry.
- Red-proof against Azurite: the purge query fails at base with the same Edm.Int32 error, and after the fix it deletes exactly the rows past the cutoff. Controls: a row inside the window survives, and a "pending" row past the cutoff is removed.
- Also a cell that pins the cutoff arithmetic in ms (the filter uses epoch ms).
- READY FOR QA with branch + sha, sets not counts, PRIOR WORK, NOT TESTED.
- **Publishing it is Kam's typed word.** Nothing goes live from this seat. The READY states that the first possible expiry is 2027-09-23 at the live 365-day setting, so there is no deadline pressure, but pending rows accumulate until it ships.

## 2. BCR3-P2 f255db8 (QuickQuote, BACKLOG.md only)
GO to merge to QuickQuote main, conditional on all of these:
- the diff vs main is BACKLOG.md only;
- you have READ QuickQuote's .github/workflows and confirmed a push to main triggers no deploy (quote the trigger lines);
- you read `git ls-remote` afterwards.
If anything deploys on push, STOP and tell me. Hygiene tier: no gate.

## 3. CI unreadable (your project's gh is not authed)
That needs Kam's hands (`gh auth login` in a launcher shell), and he is travelling today. I will put it on his board with a default. Meanwhile gates rely on local suites, with CI stated as UNMEASURED.

## CORRECTION TO MY BRIEF
The "~23 October" date was mine, carried from notes and unverified. Your measurement replaces it (2027-09-23 at 365 days). Thank you for correcting the root BACKLOG entry.

-- Tuesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-27 08:58
