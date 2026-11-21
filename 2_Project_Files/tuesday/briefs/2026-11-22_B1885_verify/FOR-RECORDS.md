# FOR RECORDS: OXPd 2 tolerant reading of printer callbacks (lane T, kit B1863), gate round 1, reader B1885

Not repository text. For Tuesday's records pass (backlog, runbook, design notes); nothing here was written into the project.

## What lands

- The generated parser of the five service-target specifications reads an unlisted enum value as the enum's first
  member `Unrecognized` (0, the default, attribute `Oxpd2UnrecognizedAttribute`) and an optional JSON null as absent
  (not counted toward minProperties/maxProperties). Required absent or null, null array item, null body stay refused.
  The 16 device clients stay strict. The runtime's own enum converter writes listed wire names only. A six-argument
  `TryParse` reports a count and the first 16 schema paths; nothing in `src/` reads it yet.
- Local and hosted totals: 1392 -> 1404 (11 K cells, one P03 case); rules files 443 -> 444; `Ran 60`, floor 60.

## Items the kit sends to records (the seat wrote none of them)

1. The runbook gains the regen discipline for tolerant enums: a generator change, then the lane-local regen program,
   then the landed regeneration test; never a hand edit under `Generated/`.
2. The backlog gains NOT DECIDED 1 (device REST answers read tolerantly or not: the product owner's question; today
   strict, measured by this reader over 716 client models with an optional root property and 166 with an enum site),
   NOT DECIDED 2 (a new member of a one-of result: today skipped and the object refused), NOT DECIDED 3 (who reads the
   report), and item 4 (what a printer does with a refused or tolerated callback: UNMEASURED until a printer test).

## From this gate

3. **A missing cell (F1 of VERDICT.md):** making the optional-null rule apply to STRICT (client) objects too (mutant
   mNullStrictToo: the `schema.Tolerant` condition dropped from the null rule) reddens no cell of the lane and no landed
   test; only this reader's probe G05 caught it. The code is right today. A K8 row asserting that an optional null in
   a client model stays `WrongType` closes it (in this lane's fix round if there is one, else a follow-up).
4. **H8 wording:** the kit's "DuplicateKey, as today" for a duplicate key whose FIRST value is null is false of the
   base (`WrongType` at the null). The built `DuplicateKey` is D3's null-as-absent meeting the unchanged duplicate
   check; the body is refused before and after. Second reader B1886 rules this point.
5. **The converter and enums without wire names:** `Oxpd2Json.Options` now refuses to write (and to read) an enum
   that has no `JsonStringEnumMemberName` members (the runtime's own `Oxpd2RefusalKind`, the adapter's own enums);
   the stock converter wrote their C# names. Measured (probe G06: writing `Oxpd2RefusalKind.WrongType` throws).
   Nothing in `src/` does either today. Stated in the pull request body.
6. **K6b reads one line at a time:** a comparison split across lines, a `switch`, a local holding the member, or an
   alias is not caught; it lists every line that names a target enum. Stated in the pull request body.
7. **K6b's red-first is by a stub only:** its scanner does not depend on the generator, so with the head's test file
   and the base's generator 15 tests are red (11 K cells but K6b, N3 x4, P03), not 16; this reader reproduced K6b's
   red by a test-side mutant (the offender line removed: K6b red by `Assert.Single`).
8. **D8's README line** ("a later input with a map", state it as a limit) was not added: the kit limited the README
   to one sentence. A one-line follow-up if wanted; the pull request body states it.
9. **README punctuation:** the new sentence ends with a full stop inside a numbered list whose items end with a
   semicolon (the kit's verbatim text kept). Harmless; tidy at a later README pass.
10. **Tolerance reaches the targets' ANSWER schemas too** (every object generated from a target input): the adapter
    re-parses the sink's answer with them; the answers hold no enum and the options write no null, so nothing changes
    in practice (DERIVED from the code; lane E's S03 still green).
