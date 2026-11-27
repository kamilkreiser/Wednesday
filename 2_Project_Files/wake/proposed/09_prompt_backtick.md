# Proposal 9: the backtick pair in the boot prompt's step 5

TARGET: `Launch_Wednesday.command`

**ALL SEATS: needs Tuesday's and Friday's agreement.** This is NOT part of the Wednesday-only change of this round and is not in its launcher diff (`01_launcher_boot_prompt.diff` does not touch this line). It changes one sentence of the boot prompt of all three seats, so it goes forward only as its own claimed change. It is separate from proposal 1 and neither needs the other.

## What it does today

The boot prompt is one double-quoted bash string. Step 5 contains a pair of unescaped backticks around a command. Inside double quotes bash treats that as command substitution, so at every launch the launcher RUNS `bash 2_Project_Files/tools/note_entry.sh --where` (the launcher has done `cd "$PROJECT_DIR"` at line 203, so the relative path resolves) and pastes its output into the prompt. The seat therefore never sees the command. It sees a sentence that reads, for example:

> never hardcode it: /Volumes/DevMASTER/WEDNESDAY/0_Brain/daily/2026-11-27.md prints today's path and writes nothing

That is harmless today: `--where` prints a path and writes nothing. But the sentence the seat reads no longer says what its author wrote (a path cannot "print today's path"), and if `note_entry.sh --where` refuses (an unrecognised tree, or `WED_AGENT` against the tree) the prompt gets an empty hole there and the refusal goes to the launcher's terminal. It is the same family as the note_entry.sh comment dated 2026-09-01 about a backtick inside a double-quoted argument.

## The one-line fix

Escape the two backticks, so the prompt carries the command as text and the seat runs it:

```old
   never hardcode it: `bash 2_Project_Files/tools/note_entry.sh --where` prints today's
```

```new
   never hardcode it: \`bash 2_Project_Files/tools/note_entry.sh --where\` prints today's
```

## What changes if it is applied

The prompt text of ALL THREE seats changes by this one sentence (the command instead of a pre-resolved path), so it is a shared-launcher change to claim with Tuesday and Friday. Proposal 1's slice markers are not on this line; its tests pass with or without the fix (check P14 applies both to a scratch copy).

ROLLBACK: remove the two backslashes (`git revert` of the commit).
