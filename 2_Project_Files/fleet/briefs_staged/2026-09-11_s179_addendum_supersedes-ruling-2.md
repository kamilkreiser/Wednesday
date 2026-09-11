## BLUF
- **SUPERSEDES ruling 2 of Wednesday's 03:59:11Z ANSWER** — the "CORRECTION to your reason 3". **That correction was WRONG and is withdrawn. This is Wednesday's error, not yours.**
- Kam withdrew the 2026-09-06 09:42 aggregation WORDING at 09:45. **But on 2026-09-07 at 13:23 he gave a ticket-creation rule that STANDS**, verbatim:
  *"if a single test is required, we should be creating one ticket with multiple items inside it rather than multiple tickets. The only reason to create multiple tickets is if they relate to separate workloads or separate fixes."*
  Source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/brief-standing-lines.md` lines 166-186. Wednesday found it with the absence check it ran after correcting `STANDING_LINES.md` — Wednesday had checked the withdrawal and not what came after it.

## What changes for you
1. **QA-7 / QA-8:** apply THAT predicate — one test pass proves it → one ticket; separate WORKLOAD or separate FIX → separate tickets. Your own observation (QA-7's lines reach develop only when #953 merges; QA-8 is fixable on develop now) is exactly the "separate fixes" question. **Your call, with the predicate cited as the reason in the ticket.**
2. **If you have already filed:** do not refile. Add one line to the ticket naming the predicate and your decision under it.
3. **Your handover:** `STANDING_LINES.md` line 86 is Wednesday's own file and is corrected to point at the 09-07 rule. You do not need to name it as an owner's fix.

## Unchanged
Every other ruling in the 03:59:11Z ANSWER (1 and 3-8) stands, as does the brief.
