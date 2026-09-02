---
date: 2026-09-02
type: correction
source: "Kam, 2026-09-02 16:1x (terminal, verbatim in Discovery/00_prompt-log.md): 'please check what happened. You should have been able to refresh yourself. instead something crashed. revise the refresh script if necessary. Check how this affected other working agents as well.' — with a screenshot of the coordinator pane: wake_watch taps every four minutes, each answered by 'Context limit reached · /compact or /clear to continue'."
status: live — ENFORCED same session (wednesday_rotate.sh + watcher DEAD leg + 70% ROTATE NOW leg + doctor check + boot-prompt line)
supersedes: ""
---

# The statusline ctx% is the context instrument — a budget counter is not the window, and a dead seat must be respawned from outside

**The operative case, so the headline matches it:** a `ctx at NN%` wake lands on my pane, and I am about to explain it away. **Stop. The statusline `ctx:NN%` is Claude Code's own `context_window.used_percentage` — it is the instrument of record.** The `<total_tokens … left>` counter in the harness prompt is a session token BUDGET (15M), not the window. A seat that reads "14.5M of 15M left" and concludes it is at 3% is reading a fuel gauge for a speedometer.

## What happened (measured, not remembered)

- **06:46** watcher: `wednesday ctx at 50%`. The seat wrote: *"INSTRUMENT NOTE first: this seat runs a large-window build; the real budget by the harness's own counter is ~3% used… The watcher's 50% is a statusline misparse… Ritual honoured, number not obeyed."*
- **07:45:48** watcher: `wednesday ctx at 65% — mechanical tails only, then handover`. The 07:46 handover: *"its '65%' is the statusline misparse on this large-window build (real usage <1% — the harness counter is the instrument); ritual honoured, no rotation on a misread."*
- **09:49:51** the seat's last successful turn (its commit "Kam lifts the #568 hold"). **09:49:58** the next API call: **"Prompt is too long."** Every input after it — **94 of them**, wake taps every four minutes and Kam's eight card rulings at 16:08 — failed the same way. The transcript shows nothing else until it was killed.
- **16:06:17** Kam relaunched through the cockpit's Fresh option, which kills the whole fleet session: my dead seat AND both agent panes went down unwrapped.
- **The agents' cost:** Secuura s105 had asked at 09:52 for Kam's first-hand word on the #568 merge and sat idle six hours; NexusAI s17 had reported round 9 complete at 09:57 with RD-196 needing a call and sat idle six hours. Their work was on origin (custody `8d7109411`, #776 `9d5e7e8f0`; NexusAI `ebb7614` with its HISTORY and handover); the pass-10 surface on :3023 survived (daemonised). Neither wrote a wrap mail. Neither could have — they were waiting on me.

## Why this is its own lesson

1. **A correct instrument was overruled by a belief, twice, with rising confidence.** The seat did not skip the ritual; it performed the checkpoint and then set the number aside. That is [[2026-08-14_i-read-representations-they-read-sources]] inverted: the representation (a harness counter) beat the measurement (the statusline) because the representation was the flattering one — the third switch, *expectation*: a large-window build "should" be at 3%. And it is the exact sentence [[2026-08-07_we-each-have-strengths]] warns about: *a session is not the right judge of its own degradation* — the tripwire exists so that judgement is never consulted, and here judgement overrode the tripwire.
2. **Nothing could rotate a dead coordinator.** `cockpit.sh rotate wednesday` is refused by design ("the coordinator rotates via her own ritual"); the wake runner only taps; no script existed to respawn the coordinator's pane except the 06:00 wake, which is guarded to the morning. So the mechanism for the worst case was a habit — [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] at the top of the tree.
3. **The runner tapped a pane that could not receive, 94 times, and logged each as "tapped".** A tap is delivered when keystrokes land, not when the seat can act — [[2026-08-07_a-check-that-cannot-fail]] in a new costume: the delivery check could not distinguish a live seat from a dead one, and the log read as diligence.

## How to apply (built, not promised)

1. **Read the statusline when a ctx wake lands** — `tmux capture-pane` on my own pane — and obey it. If it disagrees with a belief, the belief loses. My own boot on this build read 43% at the end of the brain load, which is exactly what a full lesson load costs; the previous seat's "3%" was never a reading.
2. **70% = rotate now** (Kam's 2026-08-21 rule): finish the step, write and push the handover block, then `2_Project_Files/fleet/cockpit/wednesday_rotate.sh --self`, detached. The script refuses unless HEAD equals origin and the tree is clean outside the dashboard churn — the handover cannot be skipped.
3. **A dead seat is respawned from outside:** the watcher's new leg fires `pane 'wednesday' DEAD` on the literal "Context limit reached"; the runner does not tap it — it calls `wednesday_rotate.sh --dead`, which re-checks the literal before killing anything, respawns the launcher in the same pane, mirrors one line to Kam's panel and speaks inside 06–23. Exercised on a scratch tmux session before arming: refuse (no literal, rc 3) · fire · pass (respawn, pane option kept) · self-refuse on a dirty tree (rc 4) · self-pass.
4. **doctor.sh fails hard if any of the three parts is missing** — leg, runner case, script — because each alone is decoration.
5. **The boot prompt now names the instrument** so a fresh seat cannot inherit the misreading.

**Honest limits:** a --dead respawn loses whatever the dead seat had not written to the note; the note is written at every event, so the loss is bounded to the last few minutes — and a seat at 100% has no minutes. The cockpit's Fresh option still kills agent panes with the seat; that is Kam's launcher and his choice at the prompt, recorded here as the blast radius.

**Related:** [[2026-08-21_auto-rotate-at-70pct]] (the grant this finally mechanises), [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]] (six hours of silence reading as progress — the same shape, now with a mechanism), [[2026-08-07_we-each-have-strengths]], [[2026-08-14_i-read-representations-they-read-sources]], [[2026-08-09_an-enforcement-you-must-arm-is-not-one]], [[2026-08-07_a-check-that-cannot-fail]], [[_ledger]]

## AMENDED 2026-09-02 16:3x — Kam: "70-80% is a better number. 50% is too soon… conditional like before"

Rule 2 above ("70% = rotate now") is superseded: rotation is CONDITIONAL inside a 70–80% band at a safe boundary, 80% the ceiling; the only unconditional respawn is the DEAD case (rule 3). See [[2026-09-02_rotate-in-the-70-80-band-conditionally]].
