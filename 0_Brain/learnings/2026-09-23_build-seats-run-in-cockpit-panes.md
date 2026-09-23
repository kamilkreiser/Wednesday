---
date: 2026-09-23
type: preference
source: Kam, terminal, 2026-09-23 ~14:4x — "yes, use cockpit panes for build seats going forward"
status: live
tier: W
---

# Build seats run in VISIBLE cockpit panes; in-session subagents are for short reading and drafting only

**The operative case, so the headline matches it:** Friday is about to start BUILD work for a project — anything that writes code, runs a stack, or takes more than a short reading/drafting pass. **Launch it as a real Claude seat in a cockpit pane (the right-hand side of the `fleet` tmux window), briefed by mail, so Kam can watch it and type into it.** Do not run a build as an in-process Agent-tool subagent.

**What prompted it:** Kam asked whether the two drafting agents could be shown "in the iTerm pane on the right". They could not — Agent-tool subagents run inside the coordinator's session and have no pane (they are visible only through the "← for agents" view). Friday offered the split below with its cost stated (a full seat = its own boot, allowance use, mail brief); Kam said yes.

**How to apply:**
1. **Build seat → cockpit pane.** Claim the project first (`wed_claim.sh`), brief through `send_brief.sh`, launch through the cockpit tooling (never raw `send-keys`), verify the launch at rung 5+ (the pane shows the commission received).
2. **Short reading, extraction, drafting (minutes, file in → file out) → in-session subagent** is still fine; say so when doing it, and tell Kam about the "←" agent view if he wants to watch.
3. **Usage gate still applies** to every pane launch (`usage_gate.sh`), and the build seat still ends at READY FOR QA → gate → Friday's completion check.
4. Nothing here changes client isolation: one project per seat, that project's own launcher and identities.

**Family:** [[2026-08-04_delegation-v2-observability]] (Kam wants to SEE the work — the pane layout was his design pointer) · [[2026-08-11_coordinator-not-carrier]] · [[2026-08-05_wed-work-threshold-delegation]].
