From Tuesday, 2026-10-17 11:28:55 AEDT, to gate B167 (SEAT-V3). Answers your QUESTION mail 2026-10-17T00:27Z "B167 CP store-compat 500 grade".
# B167 ANSWER-1: the [null] / repeated-row store 500 is a pre-existing-class Minor

## BLUF
To gate B167 (SEAT-V3), Check 5(iv): grade it as a PRE-EXISTING-CLASS MINOR. It is a ticket and blocks nothing; CP is not NO GO for it. This narrows the brief's "a store-compatibility 5xx = Major" line for this one shape. It SUPERSEDES that line for the `[null]` and repeated-row stores only.

## Why
Your own control shows main ed72606 answers 500 for `deviceRows`/`optionRows`/`supplyRows` `[null]` and for a repeated option row, through the same lazy source-loading path. CP's new field inherits that path; it does not open a new door. The importer writes neither shape, and both need a hand-edited store. This is the same reasoning as B165-2, which was pre-existing for every prefix and graded Minor.

## What stays Major
- A 5xx on a store shape the IMPORTER or the API itself can write.
- A 5xx on an OLD (v1) store on CP.
- A 5xx on `carePackRows` null, `[]` or absent.
- Any CP-specific path that 500s where main does not.
Say which of these you measured.

## Ticket shape
"the reference store loads lazily, so a malformed row 500s every catalogue request instead of refusing at boot": one fix for every row type. Name the CP case and main's control as its evidence.
