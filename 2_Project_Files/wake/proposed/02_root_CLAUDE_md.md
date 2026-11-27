# Proposal 2: root `CLAUDE.md` names the wake-pack boot, for the seat that is on it

TARGET: `CLAUDE.md`

Rewritten in round 3 (the checker's M4). Round 2's version reworded the session-start steps for every seat and deleted a sentence recorded as Kam's ruling. This version does neither.

## What it does

- **Replacement A adds one paragraph and changes no existing sentence.** The paragraph is scoped in words to "a seat that boots on a wake pack", so Tuesday's and Friday's prompts, which are unchanged and still mandate `TASKS.md`, `INDEX.md` and `entries/`, stay consistent with the rules file they read. The Wednesday seat's fallback boot (pack failed) is covered by the same wording: on that boot it is not on a pack, and the steps below the paragraph apply as written.
- **The sentence "the full lesson load STAYS" (Kam, 2026-08-06) is left exactly where it is.** It disagrees with what the launcher has done since 2026-09-02, and that is not a build seat's or a coordinator's sentence to edit. The proposed change to it is in `FOR-KAM_lesson-load-ruling.md`, for Kam to rule.
- Replacements B and C are unchanged from round 2. The checker confirmed both as true contradiction fixes: the file's own header carries Kam's 2026-08-25 ruling on the master drive, and `voice/speak.sh` records that he chose Matilda Premium.

## Replacement A: one scoped paragraph above the session-start steps

Round 4 (the second checker's N9): the paragraph said the pack is read "in place of steps 1 to 3". Step 2 is Kam's full-lesson-load sentence, so that told the pack seat not to do what the untouched sentence says, before he has answered `FOR-KAM_lesson-load-ruling.md`. It now says "in place of steps 1 and 3" and points step 2 at the question. Also round 4: "the seat's live grants" is now "the grants register whole", which is what the pack carries.

```old
## Session start (done automatically by `Launch_Wednesday.command`)

1. Read this file → `0_Brain/CLAUDE.md` → `0_Brain/identity/persona.md` +
```

```new
## Session start (done automatically by `Launch_Wednesday.command`)

**On a seat that boots on a wake pack** (the Wednesday seat, from WED-170 step 1; only when
the launcher built the pack at that launch): the launcher's boot prompt is the read list.
After this file and `0_Brain/CLAUDE.md`, such a seat reads `0_Brain/wake/WAKE-<seat>.md`
whole in place of steps 1 and 3 below; for step 2 see the question put to Kam (it is his
sentence, and this paragraph does not change it). The pack holds persona, voice protocol and
`people/kam.md` verbatim, the most reinforced rules, the one-block handover
(`0_Brain/tasks/STATE-<seat>.md`), the grants register whole and its own ledger in reduced form.
On such a seat `TASKS.md`, `INDEX.md`, `projects_index/entries/` and the scoreboard head are
read on demand. Step 4 (the daily notes) and step 5 apply to it unchanged. **A seat that is
not on a pack, and the Wednesday seat on a launch where the pack failed, follow their prompt
and the steps below exactly as written.**

1. Read this file → `0_Brain/CLAUDE.md` → `0_Brain/identity/persona.md` +
```

## Replacement B: rule 0 (master drive)

```old
0. **Portability first (Kam, 2026-07-31).** The T9 SSD is the master copy —
   everything for this project lives on the drive so Kam can pull it and plug it
   into his laptop.
```

```new
0. **Portability first (Kam, 2026-07-31).** The drive is the master copy
   (DevMASTER since Kam's 2026-08-25 ruling in the header above; the T9 is its
   sync copy) — everything for this project lives on the drive so Kam can pull it
   and plug it into his laptop.
```

## Replacement C: rule 3 (voice)

```old
   spoken updates (Moira, en_IE). Keep spoken messages to 1–3 sentences; the full
```

```new
   spoken updates (the voice is chosen by `speak.sh`: Matilda Premium, falling
   back to Moira). Keep spoken messages to 1–3 sentences; the full
```

ROLLBACK: `git revert` of the commit that applies these replacements; the file is text only and no tool parses these lines.
