---
date: 2026-08-21
type: grant
source: "Kam, 2026-08-21 10:38 (dashboard chat, dictated — 'add to the nodes' = add to the notes/rules): 'let's add to the nodes. To do this, once you reach 70%, without me having to prompt it, but only do it if it's safe and doesn't interrupt any other flow.' Given minutes after watching the first Kam-prompted mid-day rotation execute cleanly."
status: live
supersedes: ""
---

# Auto-rotate at 70% context — unprompted, but only at a safe boundary

**The grant (recorded per go-slow rule 5):** when my own context reaches
~70%, I wrap and respawn WITHOUT waiting for Kam to ask — provided it is
SAFE: no other flow interrupted. This extends the 50% checkpoint (rhythm §2,
declare-a-default) into an autonomous rotation at 70%.

**What "safe / doesn't interrupt any other flow" means, concretely:**
1. No agent QUESTION unanswered and none imminently expected (a plan
   confirmation due in the next minutes → answer it first).
2. No mid-conversation thread with Kam left dangling — finish the exchange
   or state the handover in it.
3. Everything durable: daily note current with the handover pack, ledger
   rows written, commits pushed (HEAD == origin), wrap mail sent.
4. Agent sessions keep running untouched — the rotation is MY pane only
   (detached `tmux respawn-pane` on %0 with the launcher, the WED-111
   mechanism). Their mail waits ≤ the reboot window (~10 min), inside the
   fleet's 15-minute fallback.
5. If 70% arrives mid-task: finish the current task to a boundary first
   (the 50% checkpoint's declared default already forbids starting new work
   that won't fit) — 70% triggers the wrap at the NEXT boundary, not an
   interrupt.

**Why this exists:** Kam asked at 10:36 whether I could restart without
affecting the agents; the answer was yes and the rotation ran cleanly. His
follow-up made it standing so he never has to prompt it. It is the fleet
rotation discipline (working-rhythm §3) finally applied to the coordinator
herself — the 08-16 lesson said a session is not the right judge of its own
degradation; a numeric tripwire plus a safety checklist replaces judgement.

**Enforcement (a promise is not a mechanism):** the watcher's ctx leg
already fires at 50%; a 70% leg that says "rotate now if safe" is the
enforcement — WED ticket filed the same session this was granted. Until it
exists, the 50% wake + this file carry the rule.

**Related:** [[2026-08-16_an-ask-without-a-default-is-an-indefinite-hold]],
[[2026-08-07_we-each-have-strengths]] (degradation is structural, not felt),
[[2026-08-07_a-promise-is-not-a-mechanism]],
[[2026-08-03_go-slow-earn-autonomy]] (rule 5), [[../people/kam]]
