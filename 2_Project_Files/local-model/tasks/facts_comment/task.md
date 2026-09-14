TASK: facts_comment

The INPUT is a JSON object with two keys: `issue` (a Linear issue: identifier,
title, state, description) and `facts` (an array of short strings, each
already containing whatever ids it needs — PR numbers, commit SHAs, other
ticket identifiers).

Produce a facts-only comment body, following the s218/s222 closing-comment
shape:

- Line 1 must start with exactly `## BLUF` followed by a one-sentence summary
  of the facts (no ids invented — draw only from the facts list and the
  issue's own identifier).
- Then a blank line.
- Then one bullet per entry in `facts`, in the SAME order as the input,
  each bullet reproducing that fact's content (you may tighten wording but
  must not add a fact that is not in the list, and must not drop one).
- Never write an `@` character anywhere in the output (no mentions).
- Never invent an identifier, PR number, or SHA that is not already present
  somewhere in the INPUT JSON.
- Keep the whole output under 1500 characters.
- Output nothing else — no closing remarks, no signature line.
