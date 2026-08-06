---
date: 2026-08-06
type: correction
source: "w=3 regression: WED-75 Lead_Bot brief asserted the API-key handoff was 'TO Vision' — the authoritative record (Vision's own 2026-07-03 history entry) says Vision GENERATED the key and Lead_Bot receives it, and the value still in Lead_Bot's .env is a gitleaks-found LEAKED key. Caught by the Lead_Bot agent's verify-first pass. Family: 08-04 Peter to-do type (w=1) + 08-04 Tokenomics circular pointer (w=2)"
status: live
supersedes: ""
---

# Every brief fact carries provenance — enforced by a gate, not by intention

**The regression (why this is w=3):** "validate every fact in a brief against
the live source" has been written down twice — as the delegation-protocol rule,
then as [[2026-08-04_validate-brief-pointers]]. It failed a third time, and the
failure mode was the same each time: a fact that *felt* settled was taken from
a convenient summary instead of the authoritative record.

This time the summary was **my own ticket title**. WED-75 said "LEAD_BOT_API_KEY
handoff to Vision", inherited from Vision's one-line 08-04 wrap. The authoritative
source — Vision's 2026-07-03 history entry — records the opposite flow and one
fact the summary omitted entirely: the key Lead_Bot still holds was **leaked and
found by gitleaks**. A brief built on the summary would have pushed a key the
wrong direction and missed that this was a security remediation.

**Per the ledger's w≥3 rule, instruction is now proven insufficient → ENFORCEMENT:**
`2_Project_Files/fleet/send_brief.sh` is the only path for sending a brief. It
mechanically refuses to send unless the body carries:

```
PROVENANCE:
- <fact> | <source path / URL / ticket / command> | read YYYY-MM-DD
```

and refuses again if any line lacks a source or a read-date. Both refuse paths
and the send path were exercised before it was used
([[2026-08-06_exercise-mechanisms-before-arming]]); its first real send was the
Vision heads-up brief the same hour.

**What the gate can and cannot do (honest):** it cannot know whether I actually
opened the file. It converts "I never noticed I hadn't checked" into "I would
have to write a false line" — the same shape as the pre-commit artifact hook.
That shift, from omission to deliberate act, is the whole mechanism.

**The sharper sub-rule this taught:** *a summary of a record is not the record —
especially a summary written by a different project, and especially my own
ticket titles.* Direction, ownership, and causality are exactly the facts that
get flattened in summarising. Read the entry that documents the event.

**Related:** [[_ledger]], [[2026-08-04_validate-brief-pointers]] (family parent),
[[2026-08-03_mental-model-not-source-of-truth]],
[[2026-08-06_artifact-presence-is-not-execution]]
