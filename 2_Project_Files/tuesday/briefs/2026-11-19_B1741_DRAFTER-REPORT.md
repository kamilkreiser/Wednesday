STARTABLE: YES for an MPSCALC-316-only kit; NO for MPSCALC-195 (the accepted engine-target sentence is on no record the drafter could read).

# B1741 drafter report (SEAT-M163, MPS lane M-G)
Saved by Tuesday (s293) from the drafter's in-session reply. Condensed by Tuesday; the kit is the authority. Figures are
the DRAFTER's unless marked "Tuesday".

## Files
Kit `2026-11-19_B1741_SEAT-M163_mps-lane-mg-accepted-wording.md` (115 lines, 36466 bytes, 8 unfilled Stamp lines S0 to S6
and the last line); sidecar `.measured` 78 lines; stamp_check 75 of 75. Scratch `fleet/state/s293/d1741/`.

## MPSCALC-195 is OUT of the lane
Ticket read whole with 7 comments; comments 41070 and 41374 say the sentence is accepted but do not hold its words; C-108,
BACKLOG rows B102-2 and B1703-OWED-3, files B102, B163, B165, B1622, B1653, card mps-410-openapi-195-wording-1117 (ruled
a, does not quote it) and Tuesday's copy of the 2026-11-11 register: none holds the text. The kit tells the builder never
to write it. OWED (Tuesday): find or re-draft that sentence and put the exact words to the product owner on a card.

## Class (a): edited
- `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:1436`: "quoteRef is at most 100 characters and customer at most 200." ->
  `at most 100 characters` becomes `at most 100 UTF-16 code units (an emoji counts as two)` (the C-64 sentence,
  CLARIFICATIONS.md:1213); no other word.
- `tests/MpsCalc.Api.Tests/QuoteRefusalOrder.cs:235`: the one test row pinning the old text (3 of 9 InlineData cells).
- Scratch diff: 2 files, 2 insertions, 2 deletions. Predicted blobs: QuoteEndpoints.cs b4fd0bad -> 1b8e6026;
  QuoteRefusalOrder.cs c756bdd6 -> 57afc7d7. QuoteEndpoints.cs holds 19 non-ASCII bytes: Edit tool only.

## Class (b): NOT edited, listed
docs/api/openapi.json:988 (bare maxLength) and :1036 (maxLength with a description): the sentence needs framing words and
a contract regeneration; web/src/screens/QuoteScreen.tsx:455 (a number in code); QuoteApiTests.V0Duplicate.cs:41 and test
names :39, :121 (ASCII cases); the section-label and template-name limits (different fields). Already done on main:
docs/API.md:441 and docs/api/openapi.json:369.

## Recommended slots
S2 base MPS main 317bbb14c7258023b1d2855a9bcce1b9b07b93f6 (0 open PRs); builder Sonnet row C2; gate G2 (a validation
message on the draft-save 400 path); landing: branch push only, Tuesday opens the PR, head-pinned squash after hosted CI
and CodeQL (9 checks on #217's head); READY target Step 0 plus 40 minutes.

## Corrections to the commission
1. 195's sentence is on no record. 2. The register wording ("100 characters, an emoji counts as two") differs from the
C-64 form; the kit freezes the C-64 form. 3. C-64 says "no code change": the drafter reads it as "the counting is
unchanged" and asks Tuesday to confirm (D1). 4. Prior work on these tickets is #107, #105, #98, #167, #175, #202, #213,
not #49 or #182. 5. Line numbers moved since the sweep.

## D1 CONFIRMED BY TUESDAY, read at source (Jira GET of MPSCALC-316, date of read in the daily note)
Comment 40096 (2026-10-25) lists as "open and not ruled" the schema maxLength places and "the sentence at
QuoteEndpoints.cs ... still says characters (the ruling says no code change; a words-gate item)". Comment 41071
(2026-11-11) records the product owner's acceptance: "the agreed sentence ... is to be used in the remaining places that
comment 40472 lists", and comment 40472 lists the refusal sentence in QuoteEndpoints.cs. So the later acceptance (C-108)
reaches the refusal sentence that C-64's "no code change" had left out: the string edit is ruled; the COUNTING is not
touched. The exact sentence is C-64's (the only form given word for word); the register's shorter wording is a
paraphrase. This reading is Tuesday's and is said as such in the pull request text.

## UNMEASURED
Test and build counts (no dotnet run); pane disjointness; free disk; whether the web shows the errors[] line to users.
