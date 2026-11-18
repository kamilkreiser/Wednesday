---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Enforcement in the path: a safeguard only counts if the action cannot be completed without it

**The one idea.** A rule lives in whoever remembers it, and rules lose to reflexes. What has actually held is a guard that sits in the path of the thing it governs: a hook, a gate, a refusal. A safeguard that has to be remembered, armed, chosen, read, or that only runs while its subject is healthy, gives the comfort of having built something with none of the protection. The same scepticism applies to promises about the future: a forecast needs a mechanism behind it just as a receipt needs evidence.

## The rules

1. **When designing any safeguard:** ask "can I complete the action without it?" If yes, it is only a rule. Move it into the path (hook, gate, refusal) or accept it works only while attention is cheap. Prefer a gate in the path to a watcher beside the work. Ask also "what would have to happen for this to be off, and would I notice?" `2026-08-09_an-enforcement-you-must-arm-is-not-one.md`

2. **When a safeguard must run beside the work (a watcher, a monitor):** it needs something that arms it and something that checks it is armed: launcher start plus a preflight check at minimum, so an unarmed watcher reads as a failure, not as silence. It also needs to be findable by the next person; an enforcement nobody can find gets routed around in good faith. A tool that exists but must be chosen is in the same class: an optional mechanism is a rule with a script attached. `2026-08-09_an-enforcement-you-must-arm-is-not-one.md`

3. **When a guard needs a list of sites to protect:** enumerate from the source (the tree), never from a hand-written list. A guard's reach exceeds its author's intent, and that is the point: it can catch the coordinator's own instruction, which no review layer above would. A gate with false positives gets routed around, so keep its allow test generous and exercise it, do not just read it. `2026-08-09_an-enforcement-you-must-arm-is-not-one.md`

4. **When a briefed agent is silent:** treat silence as a question, never an answer. It is equally consistent with working, finished, stalled and dead. Finishing any long task is a checkpoint: check the inbox before starting the next thing, even when a watcher exists; the watcher is the backstop, not the plan. `2026-08-09_an-enforcement-you-must-arm-is-not-one.md`

5. **When about to promise Kam unsupervised delivery ("ready by morning"):** name the mechanism that will produce it: a scheduled fire, a briefed teammate, a checkpoint that will notice. If the honest answer is "a session that intends to keep going", say "assume it isn't done until you see the commit". Prefer in-session work he can see. If a promised item has not started by the point it could still be reprioritised, say so then, while he can still act. When a commitment is missed, lead with it, before any status; do not quietly start the work to close the gap before he asks. No re-promising the same item the same day without a mechanism as the reason. `2026-08-07_a-promise-is-not-a-mechanism.md`

6. **When a tool, run or install creates a new class of on-disk artefact (binaries, caches, checkpoints, logs, output directories, virtual environments):** write the `.gitignore` line in the same action, then check `git status`. The wrap-time status review is a backstop, not the mechanism. Related duty: a retro candidate that would change behaviour gets a lesson file the same session; "candidate" is a queue, not a destination. `2026-08-04_gitignore-artifacts-at-creation.md`

7. **When about to run, in one command, a step that can refuse followed by a destructive step (kill a pane, launch, deploy, delete):** split them. Gated send, verify at the destination, then act: three actions, not one. If the chain already fired and the first step failed, fix and re-send first, and say so. `2026-08-17_check-the-refusal-before-the-kill.md`

8. **When a verification step follows an action that can fail:** gate the verifier on the action's own success (exit status or a completion marker), and make its first assertion that its subject exists (the reference moved, the file was written, the id came back). An unconditional verifier reports on the previous state and its output looks like a finding. On a surprising verifier result, check whether the action happened before investigating the result. Note that `python3 -c "…" VAR=x` passes an argument, not an environment variable. `2026-08-17_check-the-refusal-before-the-kill.md`

9. **Before putting any content into an agent pane:** mail it through the brief sender, read it back at the destination inbox, then tap only a pointer naming the mail's subject. Identity, rulings, queue changes and authority are mail-only, including a successor's introduction after a rotation (first contact is a mail stating the rotation and that the standing queue is unchanged unless it says otherwise). A tap without mail behind it is, to the agent, the same as text nobody typed. `2026-09-01_a-tap-is-a-pointer-not-a-message.md`

10. **Before any hand-rolled fleet action (tap a pane, read Kam's messages, raise a card, count a board, send a brief):** list `2_Project_Files/fleet/`, `fleet/cockpit/` and `2_Project_Files/tools/` for the existing tool. Each tool encodes a failure that already happened; doing it by hand silently re-opens that incident. Taps go through `cockpit.sh say` with `--mail`, never raw `tmux send-keys`; Kam's messages through `kam_msgs.sh`. A hook or gate refusal is the answer, not an obstacle. Read a tool's header for what breaks if it is skipped. `2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour.md`

11. **Before closing an agent pane:** close it only through `fleet/cockpit/pane_close.sh` with the ports of any surface the handover says is left up. A pane close is a session kill: a listener whose parent is process 1 still dies if it or its parent holds the pane's terminal. Check `ps -o pid,ppid,sess,tty` on the listener and its parent; only tty `??` survives. After any close, curl every surface named as up and disclose a dead one first. Briefs to builders: a surface that must outlive the session is launched from a script file, detached, with its session and tty stated in the handover. `2026-09-03_a-pane-close-is-a-session-kill.md`

12. **When building a list of processes to stop:** identify the listener by its port and confirm by its working directory or command line; never walk parents. Guard every expansion, abort on an empty list, exclude process 1 by name, then curl the port and re-count listeners. `2026-09-03_a-pane-close-is-a-session-kill.md`

13. **When writing a guard that refuses or skips:** ask what happens when its condition is true for a long time, when the exception becomes the normal state. A refusal must end where a human or successor actually lands (a banner, a panel row, an escalation after N consecutive refusals); a log line is not a channel. Prefer a guard that degrades (does the safe part, skips the unsafe part, says so) to one that blocks the whole cycle. A guard firing repeatedly is a finding about the guard. `2026-09-10_a-refusal-nobody-reads-is-indistinguishable-from-working.md`

14. **When adding an alarm, expiry or check to a system:** name the failure state and ask whether the code holding the guard still runs in it (empty queue: the consumer is not running; dead process: it cannot report; full disk: it cannot log). Put the watcher on its own clock (scheduler, boot preflight, a launch daemon). An expiry is half a mechanism; in the same action write down what reads the marker after its date and prove that reader runs when the system is idle. Suspect this hardest just after improving the guard. `2026-09-20_a-guard-inside-the-thing-it-guards.md`

15. **When writing or diagnosing a detector that reads a pane or log for a "dead" literal and then kills or respawns:** ask what the pane shows while a seat is diagnosing the last fire: it shows the literal. Exclude quoted lines, tool-output lines and prose markers; give the predicate a self-test holding each real false positive and add new ones to the self-test first. Never tail a detector's own log into the pane it reads; redirect to a file and read that. Fix a self-killing detector before re-arming, never "claimed and owed". Do not fix it by lengthening the literal, which blinds it when the interface text changes. `2026-09-14_a-detector-keyed-on-the-banners-words-kills-the-seat-that-reports-the-last-kill.md`

16. **When writing a hook or guard "for this seat":** never hardcode the seat's name; the settings template is shared, so it binds every seat. Resolve the seat from the tree (`fleet/cockpit/seat_resolve.sh`) and test every tree. A hook that refuses a seat's own core loop (its inbox, repository, note) is a defect to fix at once, not to route around. A hook's directory name is not where it runs. `2026-11-13_a-seat-scoped-hook-in-the-shared-template-binds-every-seat.md`

17. **When briefing or reviewing a permission gate, hook, allow-list or audit filter:** define it by capability ("any tool input executed as a command, by whatever tool"; likewise written to a file, fetched), with named tools only as examples. The unknown tool gets the strictest tier, with a test: a made-up tool name carrying a command must get the strictest treatment. First step of the build and of its check: list every tool the host offers and every field that can carry a command, path or URL, read from the host at that moment (a dated measurement). Ask the check for sibling routes to the same effect. `2026-11-18_a-gate-keyed-on-tool-names-misses-the-next-tool-that-runs-a-command.md`

## What a tool already enforces

- `2_Project_Files/fleet/hooks/pre-commit`: blocks staged artefact classes (caches, checkpoints, logs, state, output and dependency directories), additions and modifications only. It lives in `.git/hooks` and does not travel with a fresh clone; it must be re-created there.
- `2_Project_Files/doctor.sh`: checks at boot that beside-the-work safeguards are armed. It does not arm them, and it does not make an optional tool get called.
- `2_Project_Files/fleet/brief_and_launch.sh`: the index's enforcing tool for send, verify, then launch. The lesson itself does not name this script; the gating of verifiers (rule 8) is not covered by it.
- `2_Project_Files/fleet/cockpit/cockpit.sh` (`say`): refuses a tap over 200 characters without `--mail`, and with `--mail` refuses unless the named mail is found at the destination inbox. A bare short tap is still allowed.
- `2_Project_Files/fleet/cockpit/pane_close.sh`: refuses if a listener or its parent holds the pane's terminal, otherwise closes and re-curls. It does not cover the stop that precedes a close (rule 12).
- `2_Project_Files/fleet/cockpit/dead_banner_check.sh`: the shared dead-banner predicate with a self-test. A second independent source before killing is a candidate, not built.

## The mistakes this family keeps catching

- A safeguard built, documented and not running, or running and simply not called.
- A confident promise of overnight work resting on nothing but intention, with the shortfall reported late.
- A refuse-capable step chained to a kill, so one refusal becomes two incidents.
- A guard whose refusal is logged honestly for hours where nobody looks.
- An alarm that can only sound while the thing it watches is still alive.
- A hand-rolled version of a fleet tool that looks right and lacks every guard the tool carries.

## Members

- `2026-08-04_gitignore-artifacts-at-creation.md` — When a tool, run or install creates a new class of artifact (binaries, caches, checkpoints, logs, venvs): add the .gitignore line in the SAME action, then check git status. A retro candidate that would change behaviour gets a lesson file the same session.
- `2026-08-07_a-promise-is-not-a-mechanism.md` — Never promise unsupervised delivery without naming the mechanism that produces it (scheduled fire, briefed teammate, checkpoint); else say 'assume it isn't done until you see the commit'. Report a shortfall while Kam can still act, leading with it.
- `2026-08-09_an-enforcement-you-must-arm-is-not-one.md` — Build safeguards in the path (hook, gate, refusal), not beside the work. A beside-the-work one needs an arming step AND a doctor check that it is armed. If I can finish the action without it, it is only a rule. Agent silence is a question, not an answer.
- `2026-08-17_check-the-refusal-before-the-kill.md` — Never chain a destructive step (kill-pane, launch, deploy, delete) after a step that can refuse, in one command: send, verify at the destination, then act. Gate any verifier on the action's success and assert its subject exists first.
- `2026-09-01_a-tap-is-a-pointer-not-a-message.md` — Before putting content into an agent pane: mail it via send_brief, verify at the destination, then tap only a pointer: cockpit.sh say --mail '<subject>' (over 200 chars refused). Identity, rulings, queue, authority are mail-only, even a successor's intro.
- `2026-09-03_a-pane-close-is-a-session-kill.md` — Before closing an agent pane: close it only through fleet/cockpit/pane_close.sh with the surfaces' ports; it refuses (rc 5) if a listener or its parent holds the pane's tty. ppid 1 proves nothing. Kill lists come from port and cwd, never pid 1.
- `2026-09-10_a-refusal-nobody-reads-is-indistinguishable-from-working.md` — When writing a guard that refuses or skips: ask what happens when its condition is true for a long time. A log line is not a channel: end refusals where a human lands (banner, panel row, escalation after N), and prefer degrading to blocking.
- `2026-09-14_a-detector-keyed-on-the-banners-words-kills-the-seat-that-reports-the-last-kill.md` — When writing a detector that reads a pane or log for a 'dead' literal and then kills: exclude quoted, tool-output and prose lines, selftest each false positive first. Never tail a detector's own log into the pane it reads; fix before re-arming.
- `2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour.md` — Before a hand-rolled fleet action: ls fleet/, fleet/cockpit/, tools/ for the tool. Taps go through cockpit.sh say with --mail, never raw tmux send-keys; Kam's messages via kam_msgs.sh; a hook or gate refusal is the answer, not an obstacle.
- `2026-09-20_a-guard-inside-the-thing-it-guards.md` — When I add an alarm, expiry or check to a system: the guard must not live in the code path that stops running in the failure state. Put the watcher outside (scheduler, doctor.sh, launchd) and name what reads every expiry.
- `2026-11-13_a-seat-scoped-hook-in-the-shared-template-binds-every-seat.md` — When writing a hook or guard "for this seat": never hardcode the seat name; resolve it from the tree (fleet/cockpit/seat_resolve.sh) and test every tree. A hook that refuses my own core loop is a defect to fix now, not route around.
- `2026-11-18_a-gate-keyed-on-tool-names-misses-the-next-tool-that-runs-a-command.md` — When briefing or reviewing a gate, hook or allow-list: define it by capability (any input executed as a command), not tool names. Unknown tools get the strictest tier; list the host's tools and fields at that moment; ask the gate for sibling routes.
