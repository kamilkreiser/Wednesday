---
date: 2026-09-14
type: grant
source: Kam, panel 19:14:25 + 19:15:46 AEST (view=wednesday), verbatim in the prompt log
status: live
tier: W
---

# At 90% of the weekly Claude allowance, NO NEW agents or gates are launched — in-flight items finish and wrap, and Wednesday works the backlog with the local model (Ornith) from there. Until then: the OBVIOUS closes first.

**The operative case, so the headline matches it:** Wednesday is about to launch a seat, a QA gate, or a drafting subagent, or is choosing what to put in front of the fleet next. **Read the gauge first** — the statusline's 7-day figure, published by the seat's own statusline to `0_Brain/dashboard/data/usage_wednesday.json` — and read it in the same action as the decision. **At or over 90%: nothing new starts; whatever is mid-item finishes its item, hands over and wraps; from then on the coordinator itself works the backlog with Ornith (the night runner's shape, run by Wednesday in the day) until the allowance renews.** Under 90%: the cheapest closes go first — gated PRs merging, record-defect and true-duplicate closes, fix rounds on PRs that already exist — and the heavier build lanes only as the allowance allows.

**His words, verbatim (19:14:25):**
> *"Based on the clawed usage, close off the obvious tickets.  Once it reaches 90%, let's stop using other agents and we'll move to a model of you working with the local model to close off backlog."*

Wednesday's reading was put back to him on the panel at 19:1x (the gauge = the statusline's 7-day figure; 90% = no new launches; in-flight items finish; Wednesday + Ornith after) and he answered **19:15:46: *"Perfect, that works."*** — so the reading is his, not an assumption.

**Why he ruled it, in one line for the successor:** the 7d gauge read 65% at 15:04 and 80% at 19:10 — 15 points in six hours of a full-tilt fleet — with the renewal five and a half days away; the allowance would not have lasted the week at that pace, and the local model costs nothing.

**What it does NOT change:** the v1.3 signature classes; the QA gate on every change (the gate is a launch too — it is gated by the same rule, so at 90% a READY waits as a READY); the TESTED merge grant (a merge seat already live may still merge what is already gated); the three coordinator duties (double-checking output is not a launch); the Ornith night rule (it is the day-time extension of it).

**Mechanism (a grant is not a mechanism — 2026-08-07):**
1. `2_Project_Files/fleet/usage_gate.sh` — rc 0 under the cut, **rc 3 at/over** (`WED_USAGE_STOP`, default 90), **rc 4 gauge missing/stale (>30 min)/unparseable** (a stale gauge cannot prove headroom; `USAGE_GATE_ALLOW_STALE=1` overrides with the reason printed). `--check` prints the reading.
2. **Wired into BOTH launch paths:** `brief_and_launch.sh` STEP 0 (before the send — no brief lands for a seat that will not launch) and `cockpit.sh add` (before any pane). The test hooks (`BAL_SEND_CMD`, `COCKPIT_SESSION`) bypass it so the existing arms still run.
3. **Red-proofed before arming** from a FILE (`fleet/tests/usage_gate_arms.sh`, 8 arms: under / at / over / stale / stale-allowed / broken / missing / custom cut — all PASS), then both callers exercised against a 93% stub: refused, nothing sent, no pane (the pass path in the callers is straight-line and the next real launch exercises it).
4. **`doctor.sh`** fails hard if the script or either wiring is missing; warns `USAGE GATE CLOSED` at the cut; warns on a stale gauge. Exercised: the live gauge (✓ 80%) and the over stub (⚠ CLOSED).
5. **The Agent-tool drafters cannot be gated by a script** — the checkpoint ritual runs `usage_gate.sh --check` before any commission, and the handover carries the reading.
6. **Reported, not requested:** when the gate trips, Wednesday tells Kam on the panel in the same action (what was refused, what is still finishing, when the allowance renews) and switches to the Wednesday-plus-Ornith shape.

**Expiry:** none stated — the cut is a property of the allowance, which renews on its own clock (`resets_in` in the gauge). After a renewal the gauge reads low and the gate opens by itself; nothing to un-apply.

**Family:** [[2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule]] (the night shape this extends into the day) · [[2026-09-13_as-many-agents-as-possible-partitioned-by-code]] (the standing rule this caps) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (why it is a gate in the path) · [[2026-09-06_a-scoped-override-carries-its-own-expiry]] (the expiry is the gauge's own renewal, stated) · [[2026-09-02_coo-actionable-tickets-never-wait-for-kam]] ("close off the obvious tickets" is the COO queue, cheapest first) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
