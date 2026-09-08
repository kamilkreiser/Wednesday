# QA RE-GATE — NexusAI RD-369 ROUND 2, `rd-369-round2-s47` @ `c96837d` (base `main` `632a377`)

**Round 2 of 2 under the cap.** Round 1 returned GO-with-findings (7 Major / 4 Minor / 1 Polish /
0 Blocker) and the findings were all in the INSTRUMENT, not the fix. **This round fixes the
instrument. So the instrument is again the subject — a re-run of the suite green proves nothing.**
**A NO GO here ships the closed instances and tickets the residue; there is no round 3 without Kam.**

## WHAT ROUND 2 CLAIMS
`2278/2278` across 117 suites (floor 2270). All six findings closed. **The headline claim, and it is
the one to attack: the carrier predicate is now DERIVED, not enumerated, and over the real shipped
set it surfaces 9 files — including RD-385's tenant-access correspondence and authorised-users
roster — with no filename of theirs in the predicate, the commit, the tests or any list.**

## 🔴 THE ACCEPTANCE TEST WEDNESDAY SET — verify it was met honestly
**The predicate must find RD-385's files BY DERIVATION, never by name.** Grep the branch for
RD-385's filenames: **any occurrence in the predicate, a fixture, a list or a test is a FAIL**,
because that passes the test by defeating it. Then check the converse: **remove RD-385's files and
the predicate must still be general** — it must not have been shaped to exactly those nine.

## THE DISCRIMINATOR IS THE THING TO BREAK
*"A carrier is an internal identifier presented AS an identifier — the LABEL, not the count."*
Over a thousand unlabelled GUIDs in synthetic demo data is not a disclosure; one GUID on a line
reading `Tenant ID:` is. **That is a good rule. Find where it fails:**
1. **False negative** — a real disclosure whose label the predicate does not recognise (a different
   word, a table cell, YAML/JSON key, a heading rather than an inline label, another language).
2. **False positive** — labelled identifiers that are legitimately public or synthetic.
3. **Plant your own**, at paths and in shapes the builder did not anticipate, as you did in round 1.

## THE SIX, EACH VERIFIED CLOSED — and G3 is still the sharpest
- **G3** — `copySources()` now claims to recognise flags, join line continuations, handle multi-source
  COPY, and **THROW on anything unreadable including an EMPTY PARSE**. **Re-run your own round-1 proof:
  `--chown=node:node` on two lines must NOT change the count, and an unknown flag must THROW.** An
  empty parse throwing is the specific shape that made it silent — test that directly.
- **G2** — brace expansion, mid-pattern any-depth and parent-relative forms now throw. **Re-fuzz.**
  Five of your 22 forms were silently mis-modelled; confirm those five now throw or are correct, and
  **check the negation direction specifically**, since that is where a mis-model reverses to false-green.
- **G6** — round 1 re-anchored one level deeper, not generally. Confirm the fix is general.
- **G1 / G4 / G5** — the derived predicate; the census's ref; the unreproducible "6". Confirm the
  numbers stated are now re-derivable from the instrument itself.

## THE BUILDER'S OWN DISCLOSURES — verify, and credit
1. **It shipped a window and then killed it.** The roster signal first required an e-mail within six
   lines of a heading; the real file has them twelve away and **the count came back ZERO**. It called
   the window an arbitrary parameter that made the instrument answer "clean", removed it, and said it
   found this *"by chasing a zero I did not believe rather than shipping it."* **Confirm there is no
   residual distance window anywhere in the predicate.**
2. **It corrected the ORDER of its own claim** — it wrote that it had checked for identifiers "after
   writing rather than intending it before", then disclosed that the check ran in the same command as
   the send, so it had not yet seen the result when it wrote that. **The result itself: 3 hits in the
   diff, all synthetic fixtures it authored (`11111111-2222-…`, `66666666-7777-…`, `example.test` — a
   reserved non-routable TLD), 1 in the commit trailer.** **Verify that independently: no real tenant,
   subscription, directory or object identifier, no real address or hostname, anywhere in the branch.**

## VERDICT AND HOLDS
**Both directions, with a *what I did NOT test* section.** Classify: clean GO · GO-with-findings
RECORD-LEVEL · or a finding wrong in the CODE / a cell that cannot fail. **This is round 2 of 2 —
a NO GO ships the closed instances and tickets the rest.**
**Findings-only: fix nothing, merge nothing, deploy nothing** (`CI_DEPLOY_ENABLED` is unset, Kam's).
Read-only on the project checkout. 🔴 **Reproduce NO identifier, address, hostname or file content —
counts and shapes only, and verify that AFTER writing, not before.**
Report to Wednesday by mail and name the report's PATH.

## PROVENANCE
- 2278/2278, the 9 surfaced files, the six closures, the window defect, the identifier-check result |
  **the builder's own two mails, quoted, NOT re-derived by Wednesday** | 2026-09-08 01:25 / 01:26
- round 1's findings and its ground-truth figures (522/522, 288/288, the 105-file drop, 22 fuzzed
  forms) | **your own round-1 report** | 2026-09-08
- `main` = 632a377 · branch = c96837d | Wednesday's `ls-remote` in this action
