# FOR RECORDS: OXPd 2 card store malformed-escape follow-up (lane A2-F2, kit B1953, seat X43), gate G1 round 1 of 2 of lane A2-F2, reader B1960

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: this round's cut and every choice inside it (kit B1953 Q1 = a
in words at its stamp S4; Q2 to Q6 the defaults), the landing order (the C7 fix lane B1961 first) and the binding
windows check. Nothing here says the product owner decided, ruled or approved anything about this lane (kit B1953's
CLARIFICATIONS greps for the subject words counted 0, RELAYED).

## State at this gate

- Verdict GO WITH FINDINGS at `10f446f3` on main `5b66a7b1` (round 1 of 2 of lane A2-F2). Lands as ONE squash after
  the C7 fix lane (landing.txt in this folder, MAIN MOVES (B)): C# totals +23 on both legs, skipped 4 / 21 unchanged,
  RULES unchanged by this lane, unit tests 111, floor 111. With main `5b66a7b1`: 1808 / 0 / 1804 / 4, RULES 553
  (measured locally; merge tree `a711478f`).
- Gate B1950 FOUND 1 (a lone-surrogate name anywhere in an answer ended the call untyped): CLOSED if this lands. Cells
  F14 (11), R08 (5), K07 (4), E12 (3) red at `49f686a8` by their own assertion (22 naming
  `InvalidOperationException`, 1 `Value is null`), green at the head; three new mutants each MATCH.
- The two exits B1950 carried as pre-existing (such a name inside the set; such an escape in a value the store reads):
  CLOSED by the same change, each with red-first rows (F14 rows 4, 7 to 10; R08 rows 2 to 5; K07 rows 3, 4; E12 row 3).
- The head's windows red (push run 45052136167, job 137299375943) is ONE failed test line, Contracts C7, outside this
  lane (diagnosis B1955); Identity passed on that leg. The pull request's own windows check is binding; a C7 red is not
  accepted by a re-run.

## From this gate (for the backlog)

1. **Owed, Minor (VERDICT FOUND 1): `src/Datasec.Suite.Identity/README.md:35` cites `CsaStore.cs:288` and `:305` for
   the two blob-maker catches; this commit added six lines above them and they are now `:294` and `:311`** (at the head
   `:288` and `:305` are each a `{`). The sentence is true; its pointers are not. One-line README fix in a later round
   or the next Identity lane.
2. **Info: D2's named cost reaches further than the kit's wording.** The kit names it for a search ("every lookup whose
   answer holds that user"). MEASURED by the gate's probe (head against main): an unread field holding such a text in
   an enrolment's search or user read turns `Enrolled` (1 PATCH at main) into `MalformedAnswer` (0 PATCH); in the
   definition's unread `description` it fails the schema check, which every enrolment runs first and does not keep
   when it fails, so every enrolment fails until that answer changes. Fail closed, nothing written. The README's
   "wherever it sits in the answer, a part the store never reads included" covers it. Whether Graph ever sends one is
   UNMEASURED.
3. **Info (trade-off, DERIVED): the new catch is wider than a text read.** It takes any `InvalidOperationException`
   inside the try of `CsaStore.cs:240` to `:249` (the parse, the walk, `Clone()`; `ObjectDisposedException` is a
   subclass). A later defect raising one there would read as `MalformedAnswer` with no inner exception (the cells
   assert none). A defect that hits every answer is still caught by the existing green cells; a shape-specific one
   would be masked as a refusal, fail closed. MEASURED that the parse raises none for the shapes probed (empty body,
   `null`, a BOM, a raw control character: `JsonException`, typed at main and head).
4. **Info: bytes that are not UTF-8 (D4, no cell, Q3) MEASURED again and wider.** Raw `FF` in a name or value, the
   UTF-8 form of a lone surrogate, an overlong `C0 AF`, a truncated `E2 82`: `MalformedAnswer` at the head everywhere;
   at main untyped where read as a name, the display name, a card entry or the definition's type, and read when in an
   unread value.
5. **Info: no valid text is refused.** MEASURED: a valid surrogate-pair escape (in a value and in a name, `\uDBFF\uDFFF`
   included), raw 4-byte UTF-8, `\u0000`, `\uFFFF`, `\uFFFE`, `\uFEFF`, `\uFFFD`, the common escapes, a 1 MB value:
   `Found` at head and main. The repository's design and reports document no answer body with an escape (counts:
   `surrogate` 1 unrelated BACKLOG line, `\uXXXX` 0, `emoji` 0); display names are free text (A1, design 02).
6. **Info: the caller's cancellation is unchanged.** MEASURED: cancelled before the call, during the request, or while
   the answer (bad or valid) is built: `TaskCanceledException` at head and main.
7. **Info: the commission's description of main undercounts pull request 30** ("Universal Print README + one test
   file"): it changed four paths (two READMEs, two added test files). None is shared with this lane.
8. **Carried, not in this lane (RELAYED from kit B1953):** gate B1950 FOR-RECORDS items 2 to 7; lane A2's owed items;
   whether Graph ever sends such an escape or such bytes (the integration run); Q4 (not a deviation-register row, the
   records seat to judge).
9. **UNMEASURED:** every probe on Linux and Windows; the hosted legs of the merge with any main (the pull request's run
   is the first); the merge with the C7 fix lane's main (not yet on the origin); CodeQL on the pull request.
