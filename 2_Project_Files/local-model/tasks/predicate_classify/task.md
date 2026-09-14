TASK: predicate_classify

The INPUT is a JSON object with two keys: `predicate` (a written classification
rule, in English, over issue fields) and `issues` (an array of Linear issues:
identifier, title, description, state (name, type)).

For EVERY issue in the input, decide whether it satisfies the predicate.

Output exactly one line per issue, in the SAME order as the input, in this
exact format:

`identifier | CLASS | reason`

where:
- `CLASS` is exactly one of: `A`, `B`, `UNKNOWN`. Use `A` when the issue
  clearly satisfies the predicate, `B` when it clearly does not, and
  `UNKNOWN` only when the input does not contain enough information to
  decide.
- `reason` is ONE short clause that names the specific field value that
  drove the decision (e.g. "state type = started" or "no PR number found in
  title or description"). Do not write a generic reason.

Output nothing else — no heading, no preamble, no summary line, no blank
lines between rows.
