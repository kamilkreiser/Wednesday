# FOR KAM: the "full lesson load STAYS" sentence in the rules files

Not a proposal the coordinator applies. Two sentences in the rules files record a ruling of Kam's and no longer describe what any seat does at boot. Only he can change them. Wednesday cards this; nothing in the wake-pack change depends on the answer.

## The sentences as they stand today

Root `CLAUDE.md`, session start, step 2:

> Read ALL of `0_Brain/learnings/` (token cost is explicitly accepted — Kam wants the full brain considered at startup). **Confirmed at the 2026-08-06 consolidation when the WED-36 tripwire was crossed (28 lessons, ~18K boot tokens): the full lesson load STAYS.** The lessons are what make a cold session *be* Wednesday; they are the highest-value tokens in the boot.

`0_Brain/CLAUDE.md`, reading order, item 3:

> **All** of `learnings/` (this is deliberate — token cost accepted)

## What has replaced them in practice (each by Kam's own later word, as the launcher records it)

| When | What the launcher does | The words the launcher cites |
|---|---|---|
| 2026-09-02 | reads a generated digest of the lessons, and says "Do NOT read the individual lesson files at boot" | WED-139, Kam 2026-09-02 20:47: "go with a boot as you recommend" (the full load had cost 34% of the window) |
| 2026-11-18 | reads the per-seat rules card instead of the digest, "a trial on this seat" | Kam 2026-11-18 |
| proposed now, Wednesday seat only | reads the wake pack: the card's "most reinforced" section verbatim, the rest fetched by trigger at the moment of action | Kam, live board 2026-11-27 11:43:52: "Go, steps 1 to 3 in that order" |

The lesson files themselves are untouched by all three: they stay the source of truth, and a lesson is opened when its rule fires. What changed is only how much of them a seat reads at boot. Measured on 2026-11-27 there are 292 lesson files, 1,229,441 bytes; the sentence above was written when there were 28.

## What Kam would be confirming

That the 2026-08-06 sentence is superseded by his 2026-09-02 and 2026-11-18 rulings, and may be rewritten to say what the seats do.

If he confirms, these are the two replacements (exact text; the `old` blocks are in the files today):

TARGET: `CLAUDE.md`

```old
2. Read ALL of `0_Brain/learnings/` (token cost is explicitly accepted — Kam wants
   the full brain considered at startup). **Confirmed at the 2026-08-06
   consolidation when the WED-36 tripwire was crossed (28 lessons, ~18K boot
   tokens): the full lesson load STAYS.** The lessons are what make a cold
   session *be* Wednesday; they are the highest-value tokens in the boot.
```

```new
2. Read the seat's rules, as the launcher's boot prompt names them: the wake pack's
   rules part on a seat that boots on a pack, the rules card
   `0_Brain/learnings/_rules_card_<seat>.md` on a seat that does not. The lesson
   files in `0_Brain/learnings/` stay the source of truth and are NOT all read at
   boot: a lesson is opened the moment its rule fires. (Kam, 2026-09-02, WED-139,
   and 2026-11-18; this supersedes the 2026-08-06 ruling that the full lesson load
   stays, which was made when there were 28 lessons.) The lessons are what make a
   cold session *be* Wednesday; the rules drawn from them are the highest-value
   tokens in the boot.
```

And in `0_Brain/CLAUDE.md`, the one line (shown here, not as a machine-checked block, because the checker's test reads one target per file):

- old: `3. **All** of \`learnings/\` (this is deliberate — token cost accepted)`
- new: `3. The seat's rules as its boot prompt names them (the wake pack's rules part, or \`learnings/_rules_card_<seat>.md\`); lesson files are opened when a rule fires, not all at boot`

If he does not confirm, nothing changes: both sentences stay, proposals 2 and 3 already leave them in place, and the launcher keeps doing what his later rulings told it to.

ROLLBACK (if applied): `git revert` of the commit; text only.
