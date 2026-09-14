TASK: state_census

The INPUT is a JSON array of Linear issues. Each issue has: identifier,
title, state (name, type), priority, assignee, updatedAt.

Produce a single markdown table, columns in this exact order:
`identifier | title | state name | state type | priority | assignee | updatedAt`

Rules:
- One row per issue in the input. Sort rows by identifier, ascending,
  treating the numeric part as a number (e.g. KS-9 before KS-10).
- Never add a row for an identifier that is not in the input.
- Never drop a row for an identifier that is in the input.
- If assignee is null in the input, write UNKNOWN in that cell.
- After the table, add exactly one line of the form:
  `counts: <type>=<n>, <type>=<n>, ...`
  listing every DISTINCT state type present in the input with the count of
  issues having that type, types sorted alphabetically, comma-separated.
- Output nothing else — no heading, no preamble, no explanation.
