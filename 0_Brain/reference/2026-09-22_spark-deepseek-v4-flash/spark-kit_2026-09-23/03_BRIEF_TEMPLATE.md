# Brief template

Fill this in. Do not improvise the shape — every heading here exists because its absence cost a
round. The model reads this; write for a careful reader with no context and no judgement.

**Generate the timestamp with the shell. Never type a clock.** A typed time is composed from
narrative and it is wrong often enough to matter.

---

```markdown
# <TICKET-ID> <SHORT-SLUG> — <one line: what changes, in plain words>

File: `<exact repo-relative path of the file being edited>`
Tip: `<the commit SHA you read the file at>`
Runner: `<the test runner, e.g. vitest / jest / bash>`

Written <shell-generated timestamp> from <the SHA above>, file read whole.

## The mode — read this twice

<TEST-ONLY | CODE+TEST | DOCS>. Your diff touches EXACTLY <N> file(s): the one on the File: line,
modified in place. You never touch <name the files that are off limits>.

## What is wrong (one paragraph)

<Plain prose. What the code does today, what it should do, and WHY the difference matters. Name
the line numbers you read it at. If a measurement established this, quote the measurement.>

## The exact change

<For each edit point — three maximum, or split the brief:>

Edit 1 — line <N>, <replacement | pure insertion | deletion>.
Context: line <N-1> is `<current text>`, line <N+1> is `<current text>` — copy both as context.

```
-<the line's CURRENT text at the tip, byte-exact>
+<the new line, byte-exact, leading whitespace included>
```

**Do NOT touch** <regions, functions, files — be specific>.

## The test

File: `<the test file>`
The shape to copy is `<the nearest existing test>` at lines <N>-<M>: <one line on what it does>.
There is no database / app boot / network here — copy that shape and nothing else.

## Cells and controls

- `<cell key>` = `<the exact test name>`   ← the one that must go RED before the fix
- `<control key>` = `<exact name>`         ← must stay GREEN throughout
<...>

## The failing case (the "tamper")

<What to break, so the new test can be proved to actually catch it: file, line, the line's current
text, and what it becomes. It must be BYTE-UNIQUE in the file — check with a literal-string count.>

## Premises (each one measured, with where)

- <claim> — read at `<file>:<line>` at the tip.
- <claim> — counted: <the command and its result>.

## UNMEASURED — stated rather than glossed

<Everything reasoned rather than run. Be specific. If you did not run the suite, say so.>

## Collision

<Is any other in-flight work touching these files? Has this ticket been attempted before, and how
many rounds has it had? If the answer is two, it does not belong here — it goes to the cloud.>

## Scope

<If this closes less than the ticket: "closes N of M; refs <TICKET>, does NOT close it." If it
closes the ticket, say that.>

## Output

Exactly ONE fenced diff block, nothing outside it. Paths exactly as the File: line gives them.
Every `+` line on its own physical line. Every context line keeps its leading space.
```

---

## The five checks before you queue it

1. Does every `+` line appear byte-exact in the brief, or is the model being asked to invent text?
2. Is the tamper line byte-unique in its file? (Count it literally, do not eyeball it.)
3. Are there three edit points or fewer?
4. Does the brief say what must NOT change?
5. Does the built input actually reference this brief — or did the builder silently fall back to
   the ticket description? **That fallback is a refusal. Fix it and rebuild.**

## BEFORE HAND-OVER — run the builder on this brief (added 2026-09-26, Wednesday)
The brief's writer runs `night/build_input.sh <KS-id> <scratch>/input.json <pins>` (with `NIGHT_BRIEFS_DIR` pointing at the brief's folder) and hands the brief over only at **rc 0** with "prompt source: WEDNESDAY BRIEF". Why: on 2026-09-26 KS-1341 brief A was refused three times BEFORE the model, each by a builder gate the writer did not know — (1) a BLANK context line in an edit block; (2) a pure insertion whose context LEADS instead of trailing the `+` lines; (3) red cells written as `it.each` rows without a `## Red cells` section of title SUBSTRINGS. Each refusal cost a round-trip, not a model round; running the builder first costs seconds.
