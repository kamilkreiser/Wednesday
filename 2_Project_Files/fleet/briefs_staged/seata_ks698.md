# GO — seat A (s141b): take KS-698. Rhythm §2 guard attached.

## BLUF
**Take KS-698 — your pick, and the right one:** a real self-contained security defect (one request
permanently poisons a rate-limit key) beats the two dependency bumps (KS-729/KS-664) for tonight.
**Rhythm §2 holds at 65%:** if partway in you judge it will NOT finish cleanly — build + red-proofs +
READY — before your 80–85% band, **WRAP mid-task and hand KS-698 to a successor rather than rush a
security fix.** A half-verified security change is worse than a clean handover.

## RULES (unchanged)
READY FOR QA only — no merge/deploy, gates are Wednesday's (batched, held). Verify the defect in code
at develop `306d0db92…` (re-read `ls-remote`), new branch, red-proof each clause, honest limits stated.
demo frozen, client-comms ticket-only. Name the next KS + open decisions in your handover whenever you
wrap.

— Wednesday
