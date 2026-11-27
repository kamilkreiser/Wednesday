# Proposal 3: `0_Brain/CLAUDE.md` names the wake-pack boot, for the seat that is on it

TARGET: `0_Brain/CLAUDE.md`

Rewritten in round 3 (the checker's M4). Round 2's version replaced the whole reading-order list for every seat, including an item that said `TASKS.md` and `INDEX.md` are read on demand, while Tuesday's and Friday's unchanged prompts still mandate them. This version adds one paragraph scoped in words to a seat on a pack and leaves the six list items as they are. Item 3 of that list ("**All** of `learnings/`") is part of the question put to Kam in `FOR-KAM_lesson-load-ruling.md`; it is not touched here.

```old
## Reading order at session start

1. `identity/persona.md` and `identity/voice-protocol.md`
```

```new
## Reading order at session start

**On a seat that boots on a wake pack** (the Wednesday seat, from WED-170 step 1; only when
the launcher built the pack at that launch): the launcher's boot prompt is the read list, and
`wake/WAKE-<seat>.md`, read whole, stands in for items 1 to 5 below. The pack holds items 1
and 2 verbatim, the most reinforced rules, the one-block handover `tasks/STATE-<seat>.md`,
the seat's live grants and its ledger in reduced form; `tasks/TASKS.md` and
`projects_index/INDEX.md` are then read on demand. Item 6 applies to it unchanged. **A seat
that is not on a pack, and the Wednesday seat on a launch where the pack failed, follow the
list below exactly as written.**

1. `identity/persona.md` and `identity/voice-protocol.md`
```

ROLLBACK: `git revert` of the commit; text only, no tool parses this list.
