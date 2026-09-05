## BLUF

**READY FOR RE-GATE (4) @ c9947dd received and verified at origin (`git ls-remote` → `c9947ddd90cb…`, one commit above `4e4a630`, 7 files +491/−8, expectation 1612/98 → 1623/99). RE-GATE (4) IS COMMISSIONED — pane `QA/NexusAI-s35-regate4`, brief `qa-agent/briefs/2026-09-05_nexusai-regate4-c9947dd-narrow.md`, report → `projects/nexusai/reports/2026-09-05-s35-regate4-c9947dd-narrow/`.** HOLD for its verdict; on PASS: Wednesday's completion check → SCORE the fix round → RD-308 closes → the branch is deploy-eligible on Kam's NEXT word only (his one-deploy ruling was spent on a554e52; nothing deploys on this mail). On findings: fix round → re-gate (5).

## Shapes ratified (correctness is the gate's)
- **R-2 owned as yours, plainly** — recorded that way; the deduction stands where it was assigned.
- **The third restore route found by the round's own test, not by reading** — that is the method working; the brief asks the tester to drive `initializeFiles` explicitly and to measure what a "default" contains in bytes after a purge (a default seeded from a backup would be a restore wearing a default's name — a claim to falsify, not an accusation).
- **The re-drive design** (sweeper re-drives `purged_incomplete`; grace skipped, DRAFT gate not; `purgeNow` accepts the state) — ratified as a shape; the gate measures both halves and the replay control (a COMPLETED erasure must not be re-drivable).
- **R-5 BOTH, with the limit stated in place** — the right call; the tester's perimeter test (a template literal, an array join, `path.join`) will measure whether the stated limit matches the real one.
- **The concurrency hole named in your own READY mail** — that sentence is what the 09-01 rule asked for; the brief passes it to the tester as the one measurement worth most if it can be run cheaply, optional.
- RD-312 / RD-313 filed not folded: correct per the fix-round mail's own "one line, else ticket".

## While you hold
**A second QA seat is running RD-306's pass concurrently** (`rd-306-law-window-s34` @ `edb81c5`, its own port and worktree) — touch nothing on 3111+ and leave both testers' surfaces alone. RD-163/201 resumes only after re-gate (4)'s verdict. `HISTORY.md` bottom-append. Your HANDOVER block update to this head: good — keep it current at every boundary.

## HOLDS — unchanged
No deploy. RD-310 is Kam's. Nothing touches `0000096`.

PROVENANCE:
- Head `c9947ddd90cb38d03cd1bd4284b725cfc974ea26` at origin; one commit above `4e4a630`; the diff stat | `git ls-remote origin`, `git log --oneline 4e4a630..c9947dd`, `git diff --stat 4e4a630..c9947dd` on your repo's local objects — read-only, no fetch | read 15:34
- Your claims (R-1…R-5 closure, the third route, the real fixture, RD-312/313, the concurrency hole) | your mail 2026-09-05T05:29:10Z — your words, ratified as shapes only | read 15:34
- The launch | `cockpit.sh add` for `QA/NexusAI-s35-regate4` — pane present at send time (Wednesday's own mechanism; rung 5 read from the pane's content at the next checkpoint, not from the launcher's exit code) | 15:34

SELF-CHECK: re-read end-to-end for contradictions | 15:34
(checked: "commissioned" against "rung 5 read at the next checkpoint" — the pane exists and the wrapper's guards passed; the commission's receipt is the tester's content, stated as such; "ratified" against "correctness is the gate's" — every ratified item is a design or a disclosure, none a claim about what the code does; stated.)
