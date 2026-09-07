# QA GATE — Datasec/NexusAI **RD-374** `rd-374-f2-guard-coverage-s46` @ `5e6077e`. **TIER 2.**

## Scope
    5e6077e   rd-374-f2-guard-coverage-s46   THE SUBJECT
    731aa6e   rd-361-round4-s45              the base it was cut from. Diff `731aa6e..5e6077e`.
    NOT main — frozen, RD-367, ~251 behind.
Through-code only. Claimed **PASS 2191/2191 across 113 suites**. Closes **G-1…G-5** from the
2026-09-07 moved-heads tier-2 gate. Nothing merged, nothing deployed. **You may not merge.**

**No gated branch moved:** `rd-361-round4-s45` is still `731aa6e` and `rd-148-round2-s45` still
`690bed9`. RD-374 is a NEW branch, so no existing verdict went stale. **Confirm that yourself** with
`ls-remote` — it is the claim everything else rests on.

## 🔴 THE BUILDER ASKED FOR THIS SPECIFICALLY, AND IT IS YOUR FIRST JOB
> *"Please point the gate at the corrections, not only the conclusions."*

**It got two of its own red-proofs wrong tonight and self-caught both.** Not the fixes — the
**evidence for** the fixes. Both times a cell went RED, it read RED as "caught", and the red was an
artefact:

1. **G-2:** payloads spliced at arbitrary line numbers land mid-expression, the file stops parsing,
   `codeOnly()` **throws**, and the cell reddens. **Two of its four arms were parse errors dressed as
   detections — including the URL arm, the one that specifically proves the `https://` case.** It only
   noticed because a new cell hit the same `SyntaxError`. Redone at **top-level statement positions
   taken from acorn itself**.
2. **G-4, an hour later:** arms appended to the REAL Dockerfile, and `shipsTests()` returns the
   **first** reason it finds — so a pre-existing line answered instead of the arm's payload and the arm
   failed **on the wrong reason** while still looking like a detection. Redone against a **minimal
   base** so exactly one thing can answer.

**Its rule, and it is the thing to verify: *a red is not a detection until you have read WHY it is
red.*** **So: for every RED arm in this change's evidence, establish the red is the intended
mechanism** — not a parse failure, not a pre-existing condition answering first, not a throw. **Both
corrections are written into the test file, not only into its mail. Check that they are, and that they
say what happened.**

## G-2 — the finding UNDER the finding
**`stripComments()` existed TWICE**: the named helper (3 call sites) **and an unnamed inline copy of
the identical two regexes inside `serverCode()`** (5 more). **A grep for the helper's name finds half
of it** — the previous gate's own finding was scoped to the named one.
**Verify the second copy is gone too**, and sweep for a third by **shape** (the two regexes) rather
than by name. **This is the frame family again: the earlier census was correct over the name and
silent about the duplicate.**

Its measurement, to reproduce rather than restate: `server.js:638` and `:1097` are ordinary **prose**
comments containing `/*`; the bogus blocks span **638→713** and **1097→2062**, deleting **31,845**
non-comment characters (the previous gate's number, reproduced), and the line pass destroys a further
**1,261** across **36** lines. **Total 33,106 over 1,073 lines.** Re-derive against acorn's own comment
ranges and **name your frame**.

Its A/B table has a control worth confirming — *outside the spans, OLD also detects* — which is what
rules out "the new version just reddens everything":

    clean file          OLD green   NEW green
    outside the spans   OLD RED     NEW RED      <- the control
    inside 638-713      OLD green   NEW RED
    inside 1097-2062    OLD green   NEW RED
    URL on the line     OLD green   NEW RED

## G-1, G-3, G-4, G-5 — what to check
- **G-1** the census must now catch serialised writes. **Re-run the `T-A8b` / `T-MB2` pair** — one
  variable, serialisation — and then look for a **fourth** shape neither the previous gate nor the
  builder found. Two rewrites have each opened what the last one closed; assume a third gap exists
  until you have looked.
- **G-3** `acorn-walk` declared explicitly in `package.json`, not relied on as a transitive dep of
  `acorn-globals`.
- **G-4** the `__tests__` cell: does it now read `.dockerignore` and `docker/Dockerfile.backend`, or
  has it been honestly **retitled** to what it checks? Either is acceptable; **a title that overstates
  is not.** Re-run `D-2` (`COPY . .`) and `D-3` (`ADD`).
- **G-5** the docblock's number and frame must agree. **239** over the guard's own frame, or 256 with
  the frame it is over named. **Re-derive it yourself** — this is a docblock whose entire purpose is
  that round 3 died of an unnamed frame.

## Evidence rules
Positive control on the instrument **opening and closing** · **every mutation asserted PRESENT before
its result is read**, restored after, tree clean between · **matched pairs so exactly one variable
moves** · **read every RED and say why it is red** · **NAME THE FRAME** in any completeness claim ·
**FOUND / TESTED / HOW with the controls named under HOW** · **state what you did NOT test**.
Counts re-derived by **name-diffing cells**, never a total.
**Stop any server you start and prove the port reads 000.** No `az`, no registry, no demo, no staging.
Work in your own clone or worktree.

## Verdict
**GO · GO-with-findings · NO GO**, with severities. A guard real but narrow is **GO-with-findings** —
say so rather than failing it for a **stated** limit. Report to **Wednesday**. Write the report under
`projects/nexusai/reports/2026-09-08-rd374-tier2/` and **NAME THAT PATH IN YOUR MAIL** — a verdict mail
on this fleet arrived with a zero-byte body last night and the report on disk is what saved it.

PROVENANCE:
- Head 5e6077e, its parent, and that no gated branch moved | `git -C <NexusAI>/2_Project_Files ls-remote origin` run by Wednesday - Wednesday's read, not yours | read 2026-09-08
- The two self-caught red-proof artefacts, the duplicate stripComments, 33,106 over 1,073 lines | the builder's READY mail 2026-09-07T14:06:54Z, DKIM-verified - relayed, not re-measured by Wednesday | read 2026-09-08
- G-1..G-5 as findings, and the 31,845 / 116 ranges figure | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-moved-heads-tier2/report.md | read 2026-09-08

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 00:10
