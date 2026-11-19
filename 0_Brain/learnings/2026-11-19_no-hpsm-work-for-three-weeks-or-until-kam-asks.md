---
date: 2026-11-19
type: instruction
tier: W
seats: tuesday
source: Kam, live board 2026-11-19 16:25:45 view=tuesday, a note on card datasec-morning-plan-1119 (tapped b at 16:26:00; ruled b in the store, ruled_ts 16:26:51), and a second message at 16:26:43
status: live
expires: 2026-12-10
---

# No HPSM work for three weeks (to Thursday 2026-12-10) or until Kam asks for something new; keep working the other tickets; OXPd is the next big project

**Kam's words, verbatim (16:25:45):** *"The date of the HP event is coming up.  no more HPSM work for the next 3 weeks or until I request something new"*

**And (16:26:43):** *"keep working on other outstanding tickets and the backlog.  we will move onto the OXPd project when files are ready.  this will be our next big project"*

**Tuesday's reading, said back to him on the board (HTTP 201, bf-76b68338a8ba and bf-244850292136), his word corrects it:**
- "HPSM" is the Datasec/HPSM-POC project. No ticket work, build, gate, records pass, merge or deploy there. The boot ticket sweep skips its board. The 2026-11-15 HPSM deploy row and the 2026-10-16 hosted HPSM-POC push grant are not used while the hold stands.
- It ends at the end of Thursday 2026-12-10 (21 days from 2026-11-19, weekday derived with `date -j`), or earlier on his word asking for something new. A new ask from him covers what he asks for, not the whole backlog, unless he says so.
- What he already has from HPSM (the phase decision document for him and Paul, the user guide v0.4) stays with him; nothing is chased.
- NexusAI, the MPS calculator and the Security Composer carry on under the standing backlog grant. OXPd starts when Friday's notes arrive, on the newest Fable.

**Rule:** before any brief, launch, gate, merge, records pass or sweep, if the target is HPSM-POC and today is on or before 2026-12-10, do not start it; if it seems urgent, card Kam with the measured reason and keep working elsewhere. Only his words lift the hold.

**Mechanism (in the path, exercised):** `2_Project_Files/tuesday/holds/HPSM-POC.hold` is read by `2_Project_Files/tuesday/tools/launch_when_cool.sh` (backup `.pre-1119-projecthold`), which refuses with rc 6 any launch whose pane name or command holds `HPSM-POC` while today is on or before the `until` date. Arms run in check-only mode on 2026-11-19: HPSM today refused; NexusAI passes; a lower-case HPSM name refused; refused on 2026-12-10 itself; the day after it passes with a loud "past its date" line; `LWC_HOLD_OVERRIDE` passes one launch and prints the words; an empty holds folder passes.

**What the mechanism does NOT cover (the residual):** in-session agents, and any direct `gh` or Jira action on HPSM-POC by this seat, never pass through the launch waiter. Those rest on this lesson and the pickup's top block. `brief_seat.sh` could not be edited on 2026-11-19 because a seat was running under it.

**On or after 2026-12-11:** the hold has ended by its date. Tell Kam on the board in one line that HPSM-POC work resumes under the standing backlog grant unless he says otherwise, quarantine the hold file, and mark this lesson's heading ENDED.

**Related:** [[2026-09-06_a-scoped-override-carries-its-own-expiry]], [[2026-10-24_every-boot-works-the-actionable-tickets-unprompted]], [[2026-11-19_oxpd-runs-on-the-newest-fable-tuesday-boots-on-fable]], [[2026-08-09_an-enforcement-you-must-arm-is-not-one]]
