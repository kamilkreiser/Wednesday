# QA GATE — Datasec/NexusAI RD-369, branch `rd-369-recut-s47` @ `117931e`, TIER 1 (FULL)

**Tier 1 because it changes WHAT SHIPS TO A CUSTOMER** (Kam's 2026-09-05 tiering: security
surfaces get the full weight). Base: `main` @ `e94973d`.

## WHAT THE CHANGE CLAIMS
Pen-test recovery material was shipping inside the customer image. The branch adds exactly five
files: `.dockerignore` rules, `__tests__/helpers/image-manifest.js`, the guard
`__tests__/image-content-exposure.test.js`, a redacted `docs/PEN-TEST-REPORT-2026-04-25.md`, and
`scripts/verify-expected-counts.json`. **Builder's headline: shipping carriers 6 -> NONE**, suite
`2270/2270` across 117 suites (floor 2255).

## 🔴 THE INSTRUMENT IS THE TARGET — attack this before anything else
The 6-and-NONE numbers **both come from the new `image-manifest.js`**, which derives the image's
file set from the ignore rules plus the Dockerfile COPY lines. **If the manifest is wrong, both
counts are wrong in the SAME direction and the guard cannot fail** — a green that means nothing.
1. **Does the manifest model Docker's real semantics?** Negation (`!`), directory vs file rules,
   any-depth patterns, anchoring (root vs any level), later-rule-wins ordering, multi-stage COPY
   with different WORKDIRs. **Find a pattern form Docker honours that the manifest does not, or
   prove you could not.**
2. **The builder says an unsupported pattern form THROWS rather than silently answering "not
   excluded".** Verify that — it is the difference between a gap that shouts and one that lies.
3. **Independently derive at least three files' ship/no-ship status by hand** from
   `.dockerignore` + the Dockerfile, and compare to the manifest. Disagreement is a finding.

## THE OLD GUARD'S FAILURE MODE — confirm the new one does not share it
The previous guard asserted `.dockerignore` **CONTAINS certain strings**. It never asked whether a
FILE is excluded, so it stayed green while a carrier shipped under a pattern nobody had written.
**Confirm the new guard is a membership test over derived state and not a string search in disguise.**

## THE RED-PROOF — re-run it yourself, do not read it
The builder planted `docs/internal/SESSION_NOTES_probe.md` (no secret, no pointer), confirmed the
manifest derived it as shipping, ran the guard, got **1 failed / 15**, removed it, got **15/15**.
**Reproduce that end to end.** Then go further: **plant a carrier in a DIFFERENT shape** — another
directory depth, a different extension, a name that no existing rule anticipates — and check the
guard still reddens. A red-proof that only ever uses the builder's own probe shape proves the guard
catches THAT probe.

## THE JUDGEMENT CALL WEDNESDAY MADE — test its premise, not its taste
`docs/runbooks/` is excluded as a **DIRECTORY**, broader than RD-369's single named file.
**Wednesday chose the broader form deliberately**: internal ops runbooks are not customer
deliverables, the default should be that they do not ship, and it fixes the class rather than the
instance — the NEXT runbook will not ship either. **The premise it rests on is the builder's
measurement that no runbook is referenced by `backend/server.js`. VERIFY THAT** across the whole
served tree, not just that one file. **If any runtime path reads a runbook, the exclusion breaks a
route and the finding is a BLOCKER.**

## STILL-OPEN ITEMS — confirm they are honestly open, not quietly closed
- **F3** — the builder reports the redaction is defeated by its own context: a short-form hash one
  line above the marker, the key directory eleven lines below, 22 short-form hashes remaining.
  **Confirm F3 is still open and correctly recorded.**
- **F6** — not re-measured. Confirm it is named rather than vanished.
- **F1/F5 were closed by ADDED rules, not by the re-cut itself** (the re-cut's own
  `SESSION_NOTES_*.md` rule was ROOT-ANCHORED and carried forward the exact anchoring bug F5
  names). **Check the anchoring fix is real and general, not special-cased to the four known files.**

## THE BUILDER'S OWN DISCLOSURE — verify the fix, and credit it
It reports introducing a block-comment terminator inside prose **twice** in the helper's docblock,
caught by `node --check`, and notes RD-376 is about exactly that class — *"I introduced it inside
the file built to measure it."* **Confirm the file parses, the prose form is fixed, and no other
comment in the new files terminates early.**

## WHAT WEDNESDAY ALREADY VERIFIED — do not repeat, but say if you disagree
Delete-set vs main **EMPTY**; `__tests__/helpers/strip-comments.js`,
`__tests__/helpers/verdict-domain.js` and `__tests__/scheduler-failure-vocabulary.test.js` all
present on the branch; that last file **700 lines on BOTH sides**; the branch adds exactly the five
files listed above. Verified by Wednesday in its own `--shared` clone, read-only on the project.

## VERDICT AND HOLDS
- **Verdict IN BOTH DIRECTIONS**, with a **what I did NOT test** section. Move severity either way.
- **Classify:** clean GO · GO-with-findings RECORD-LEVEL · or a finding wrong in the CODE
  (a wrong behaviour, or **a cell that cannot fail**) which earns another round.
- **You are findings-only. Fix nothing. Merge nothing. Deploy nothing** — `CI_DEPLOY_ENABLED` is
  unset and is Kam's.
- **Read-only on the project checkout.** Your own clone/worktree for anything else.
- 🔴 **Reproduce NO secret, NO pointer, NO `<sha>:<path>` in your report — shapes and counts only.**
  This ticket is about a pasteable pointer; do not create another one in the evidence.
- Report to Wednesday by mail, and name your report's PATH.

## PROVENANCE
- carriers 6 -> NONE, 2270/2270, the red-proof numbers, F1–F6 status | **the builder's own report,
  QUOTED, not re-derived by Wednesday** | 2026-09-08 00:38
- delete-set empty, three files present, 700 lines both sides, five added files | **Wednesday's own
  measurement** in a `--shared` scratchpad clone | 2026-09-08
- `main` = e94973d · branch = 117931e | Wednesday's `ls-remote` | 2026-09-08
- tier assignment | Kam 2026-09-05 20:19 tiering; security surface = full gate
