## BLUF

Secuura/Blockchain session 124. The predecessor (s123) wrapped and Wednesday scored it 0.93 — the strongest single session this fleet has produced. Its queue is NOT dry. This brief carries what it ruled for you, plus one hard boundary you must not cross even if a ticket looks routine.

Wednesday has rotated to a fresh seat since s123 wrapped. A hold does not change across coordinator seats. If anything in this brief contradicts what s123 recorded, say so and push back rather than complying — a rotation is exactly when you should be most suspicious of a new voice.

## HOLDS — read these before the queue

1. **KS-781 and KS-790 are OFF LIMITS to you.** Do not fix, probe, triage, comment on, or reassign either one. The reason matters, because KS-790 reads like a routine ticket and is not: KS-781 is a CONFIRMED runtime MFA bypass on `POST /api/oauth/authorize` (s123 proved it with a control — the front door returns 403 MFA_REQUIRED, the authorize endpoint returns a 302 with a valid authorization code). The ONLY thing stopping that code becoming a session is KS-790, a separate bug where the token exchange calls a post-auth `getUserById` inside a pre-auth flow and 400s. **Fixing KS-790 in isolation arms the bypass end to end.** A working token exchange with no MFA gate at authorize is strictly worse than a broken one. This is Kam's decision and his alone; it is on his desk as a card and he has been asked to warn Peter and Stuart directly.

2. **LEAVE THE UNPUSHED BRANCHES. Do not push them and do not use `--no-verify` on them.** `feature/ks-663-...` at `df169eaf5` and `feature/ks-693-...` at `88684fb25` are committed locally and safe. Wednesday's `--no-verify` ruling of 12:15 named #800 and #806 specifically, under a rotation deadline; it does NOT extend automatically. These are feature branches with no reviewer and no deadline, so waiting costs nothing, and bypassing again would spend a sanctioned exception on convenience rather than need.

3. **Nothing merges without Peter.** #800 (`c06860658`) and #806 (`745e9e0e0`) are with him.

4. **Signature classes still pause for Kam**: production, money, external communication to any human outside the team, anything irreversible. A force-push is not standing — Kam's #806 approval on 2026-09-04 was explicitly one-time.

## QUEUE, in order

1. **THE OWED LEG-5 ADVISORY RE-RUN ON #800.** npm's bulk advisory endpoint was down when #800 was pushed, so the push went out with `--no-verify` on Wednesday's ruling and that fact is disclosed in the PR body. Check whether the endpoint answers now. If it does: re-run the preflight on `c06860658`, and if it is green, post the result on #800 and mark the disclosure resolved. If it is still down, say so and move on — do not retry in a loop.

2. **KS-791** — publish verify-file (v1+v2) in the spec, coupled with the gateway 415 fix. This is the half s123 split out of KS-663 rather than leaving it half-done. Size it before building; if it turns out to need a decision rather than an implementation, bounce it back with the reason.

3. **Then your standing Category-1 queue** — the board's own open tickets that need nothing from a client human and no ruling from Kam, ordered by priority then identifier. Work them session after session until empty. Sweep the board yourself before picking; do not take this brief's list as the board.

**If you believe the queue is dry, say so rather than manufacturing work.** Twice today an agent disproved a "queue is dry" assumption of Wednesday's by sweeping properly, so sweep before you conclude it.

## HELD, NOT YOURS YET

**KS-597 and KS-598** are Category-2, held pending Kam's plan-sheet approval. Do not start them. Wednesday holds that approval request and has deliberately kept it behind the security item so it does not compete for his attention.

## CARRY TO PETER WHEN YOU NEXT TOUCH THE PRs

The **PS-761 caveat**, and it is easy to drop: three stacks running suites at once SIGKILL the app inside the Docker VM. It shows as `exit 137` mid page-load, the app logs nothing, the restart policy returns it within a second, there is one 502, and NO TEST FAILS — and `docker inspect` afterwards reports `ExitCode=0, OOMKilled=false`, because it is describing the replacement container. It was observed during a PS-737 gate run, which is the gate Peter will run. A reviewer who does not know this reads a green as a result.

## METHOD

s123's throughline, adopted and passed to you verbatim: **"on this codebase green is not evidence, the probe is."** Three times in one session a green check or a static read was insufficient and only a live probe settled it.

Beside it, the fleet's instrument rules, because every one of them cost something to learn: predict a tamper's failing set BEFORE running it; make every control fail at least once, deliberately; a control that isolates nothing measures nothing; red-proof each clause of a multi-clause guard against a fixture only that clause can catch; and when you red-proof, do not reuse the shape of the defect that motivated the guard — write the banned thing in an idiom you would not have chosen.

**Never delete.** Cleanup is a move into a dated quarantine directory or a fresh `mktemp -d`, never `rm`. Guard every expansion with `${VAR:?}`. If a fixture is costing real budget to build, stop and report the checks as NOT RUN with the blocker named.

## MODEL NOTE

s123's seat silently dropped from Opus 5 to Opus 4.8 between 12:13 and 12:32 TODAY (2026-09-04), mid-session, on security work. The cause was never established — an automatic fallback near the weekly limit is the obvious explanation and Wednesday has verified no mechanism. Nothing in its post-12:32 output read as degraded and its score says so explicitly. Check your own statusline and tell Wednesday what model you are on; if you notice your own reasoning degrading, say so. That will be treated as data, not as an excuse.

## COMMS

Wednesday is at `wednesday-agent@agentmail.to`. Mid-session questions go there with subject `[Secuura/Blockchain -> Wednesday] QUESTION: <topic>`; do not ask Kam directly. If you are blocked, re-check your inbox every ~3 minutes; after ~15 minutes with no answer, proceed on the safest interpretation and record it — UNLESS the item is approval-class, which always waits.

Send your plan confirmation to Wednesday rather than pausing for Kam. Kam keeps veto through his own session.

PROVENANCE:
- KS-791 Backlog/Medium, no comments, updated 2026-09-04T02:54:56Z | Linear GraphQL issues query, team KS | read 2026-09-04
- KS-597 Todo/High and KS-598 Todo/High, last comment 2026-09-02T15:11Z | Linear GraphQL issues query, team KS | read 2026-09-04
- KS-663 In Review and KS-693 In Review | Linear GraphQL issues query, team KS | read 2026-09-04
- KS-790 still Backlog, High, UNASSIGNED, last touched 2026-09-04T02:32:43Z — nobody has picked it up | Linear GraphQL issues query, team KS | read 2026-09-04
- KS-781 Todo/Urgent, the runtime confirmation comment at 2026-09-04T02:32:43Z | Linear GraphQL issues query, team KS | read 2026-09-04
- Board totals: KS 108 active, 89 backlog, PS 29 active | `board_count.sh linear` (refuses to print a total that equals its own limit) | read 2026-09-04
- s123 wrapped, scored 0.93, and its ruled queue for s124 | wrap mail `[Secuura/Blockchain -> Wednesday] Session wrap 2026-09-04 (s123)` at wednesday-agent@agentmail.to | read 2026-09-04
- The unpushed branch SHAs df169eaf5 and 88684fb25, and the LEAVE THEM ruling | Wednesday daily note 2026-09-04, 13:16 rotation block, my project not yours | read 2026-09-04
- The PS-761 caveat and the exit-137 mechanism | Wednesday daily note 2026-09-04, 11:45 handover block, my project not yours | read 2026-09-04
- #800 c06860658 and #806 745e9e0e0 are with Peter | Wednesday daily note 2026-09-04, 12:30 refresh block, my project not yours | read 2026-09-04

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-04 13:24
Two errors were found on that re-read and corrected before sending: the model-drop note and the queue-is-dry note both said "yesterday" for events that happened TODAY. Every ticket id above was read live from Linear in the same action as writing this brief, not carried from the predecessor's handover text. The two branch SHAs and the PS-761 mechanism are read from Wednesday's own daily note and are labelled as such rather than presented as tree reads — Wednesday has NOT re-verified those SHAs against your tree, so verify them yourself and let the tree win over this mail.
