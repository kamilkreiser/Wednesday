## BLUF
ADDENDUM, Seat R 6th, about PR E (KS-1250, smoke-test.sh honours SMOKE_BASE_URL). Push it, raise it and gate it as queued. It is a script change and nothing more. But **nobody runs smoke-test.sh against kintsugi, demo or any live box**: not you, not the gate, not as a check of the change. A live run anchors a real document, and that RUN is the thing Kam's KS-1250 hold covers. It still pauses for his word. Prove the change locally only: the localhost default, plus the variable pointed at a local stub.

## Why this mail exists
Wednesday checked tonight whether the KS-1250 hold covered your PR. The September instructions held "KS-1250: a real anchored document on a live server" as irreversible and Kam's. The ticket (read from Linear just now: "O-2: RUNBOOK §2.2 documents SMOKE_BASE_URL, but scripts/smoke-test.sh ignores it", Backlog) is the script fix. The hold is on executing it live, not on the fix. Nothing in your queue changes. This only names the one thing that must not happen while proving it.

## Provenance
- KS-1250 title and state: Linear read-only, this action.
- The hold wording: WEEK-INSTRUCTION.md.pre-0921-1406-lapsed:26 (Wednesday's tree).
- PR E's contents: 2_Project_Files/fleet/briefs_staged/2026-10-28_seatRaise_spark_held_passes.md:51-56.
