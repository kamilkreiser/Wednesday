---
date: 2026-08-10
type: preference
source: "Kam, evening terminal sitting: 'can you read the conversation history between me and the 2 agents? if so, this is what would be good from you. and to escalate to me when necessary' — after the GitHub provisioning stumbled and he had been working two panes directly"
status: live
---

# Kam's direct conversations with agents are part of my supervision surface

**The ask:** when Kam works directly in agent panes, I read those
conversations and escalate to him only when necessary. He does not want to be
the only one who knows what happened in a pane.

**How to read them:** tmux scrollback is too shallow (Claude Code redraws).
The real record is the session transcript:
`/Users/kam_code/.claude/projects/<encoded-project-path>/<session>.jsonl` —
read-only, filter user/assistant text turns. This is reading, not writing:
manage-don't-do is untouched.

**When to read:** every checkpoint sweep while Kam is (or was recently)
working panes directly; after any wake fire involving a pane he touched;
before reporting fleet state that his in-pane actions may have changed
(mental-model rule — his pane work moves reality without mailing me).

**Escalation triggers (concrete, not vibes):**
1. Anything crossing a hold (cost, signup, prod, his signature classes).
2. An agent blocked on Kam >15 min while he may not know it.
3. Identity anomalies (e.g. tonight: global az sitting on the DEAD Secuura
   tenant — flagged; agent used a throwaway config correctly).
4. Kam and an agent talking past each other (the zsh `!`-negation paste —
   caught by the agent tonight; next time it might not be).
5. A deviation the agent flags in-pane that changes cost/scope (tonight:
   GHCR→ACR +AU$8/mo — within hold, relayed to Kam anyway).

**Related:** [[2026-08-05_kam-types-into-panes]] (the unsent-line rule — both
lessons exist because Kam's pane presence is a real channel),
[[2026-08-03_mental-model-not-source-of-truth]], working-rhythm §5.
