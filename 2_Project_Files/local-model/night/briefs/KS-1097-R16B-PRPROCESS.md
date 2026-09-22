# KS-1097-B R16B-PRPROCESS - re-brief at develop 8c2f7b3fd of READY_KS-1097-B_ornith35b-q4_DOCPATCH-REFLOW-INFERRED-PASS-7of7_2026-09-15.diff.md - **DOCUMENTATION (`Blockchain/Dev/CONTRIBUTING.md`, no code)** (written 2026-09-22 10:32:32 AEST by Wednesday's feed9 drafter; the hunks are the old READY's applied PASS 7/7 output re-anchored at the tip: every context and `-` line asserted byte-exact at the line numbers below, headers recounted, every `+` line ASCII)

Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
File: `Blockchain/Dev/CONTRIBUTING.md`

## What is wrong (one paragraph)
KS-1097 carries six Polish findings from the tier-2 gate on PR #957 (KS-1095) — merge-rule docs that still gloss TESTED weakly, or
name "the reviewer" with no referent. **This part fixes the THREE sites inside `## Pull Request Process` of `Blockchain/Dev/CONTRIBUTING.md`**,
with the wording the ticket's "Rulings" section gives: QA-957-5 at lines 456–458 (a superseded proposal still reads as pending —
`docs/DEV-PROCESS.md:238` already marks it "Superseded 2026-09-11 (KS-1092)"), QA-957-3 at line 466 ("— not the reviewer" has no referent
after KS-1095's QA-1 — drop the phrase) and QA-957-3 at line 550 ("reads to the reviewer" → "reads to the QA gate"). Nothing else in the file
changes — NOT lines 531–532 (Kam's 2026-08-27 red-pen line, leave alone), NOT lines 466's continuation 467–470, NOT line 602. Part A is
`docs/DEV-PROCESS.md`; Part C is this file's `## Related Issues` block (lines 600–604); Part D is `CLAUDE.md`.

## The exact change - 3 hunk(s) in `Blockchain/Dev/CONTRIBUTING.md` (3 `-` line(s), 3 `+` line(s), one `+` group per hunk)
Copy the block below BYTE FOR BYTE as your whole diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]` - several carry an em-dash or an arrow: copy them, never retype them), every `-` line and every `+` line, in this order. Do not add, drop, re-wrap or reword a line; a blank context line is a single space; never write a literal `\n` inside a line. Every `+` line is ASCII.
- the old READY's `+` line `of the three who is not the author* — superseded 2026-09-11 (KS-1092): the approval is Wednesday's GO on a TESTED PR.` is written `of the three who is not the author* - superseded 2026-09-11 (KS-1092): the approval is Wednesday's GO on a TESTED PR.` (the standing non-ASCII-0 rule on `+` lines; the file's own em-dashes on context lines are untouched and copied byte-exact)
```
--- a/Blockchain/Dev/CONTRIBUTING.md
+++ b/Blockchain/Dev/CONTRIBUTING.md
@@ -463,7 +463,7 @@
 (v4 · 11 September 2026 — Kam ruled that we approve our own work (16:56)). This section stays the contributor-facing copy,
 and the two agree on the adopted flow. **One item in that document differs and is
 flagged there as a proposal, not yet team-agreed** — *approval may come from any
-of the three who is not the author*.
+of the three who is not the author* - superseded 2026-09-11 (KS-1092): the approval is Wednesday's GO on a TESTED PR.
 
 1. Develop on a branch.
 2. **Test your own work before the PR goes up**, and put the results in the PR
@@ -471,7 +471,7 @@
 3. Commit → push → open the PR.
 4. Peter runs periodic formal test passes; demo (UAT) is updated after his nod.
 5. Findings from the QA gate are discussed with the PR issuer.
-6. **The author merges once the PR is TESTED — not the reviewer.** TESTED = a QA
+6. **The author merges once the PR is TESTED.** TESTED = a QA
    gate verdict (GO or GO WITH FINDINGS) at the PR's current head + a Test Evidence
    block + our own suites, and **Wednesday's GO, naming the head SHA, is the approval** (Kam, 2026-09-11):
    16:56:00 *"For the time being, I / you will approve our own elements"* ·
@@ -555,6 +555,6 @@
 A line must say what happened, not what applies. "Run and passing" means a run
 whose result you read. If a suite has no bearing on the change, write
 `not run — no spec change, no new route or method`; do not tick it as done.
-A box ticked on a not-applicable rationale reads to the reviewer as a run.
+A box ticked on a not-applicable rationale reads to the QA gate as a run.
 
 ### PR Description Template
```

## Where (every **must change** line must appear as a `-` line in your diff, at its number)
- `:466` - **must change**: `of the three who is not the author*.`
- `:474` - **must change**: `6. **The author merges once the PR is TESTED — not the reviewer.** TESTED = a QA`
- `:558` - **must change**: `A box ticked on a not-applicable rationale reads to the reviewer as a run.`
- `:463` - (correct) `(v4 · 11 September 2026 — Kam ruled that we approve our own work (16:56)). This section stays the contributor-facing copy,` - stays
- `:464` - (correct) `and the two agree on the adopted flow. **One item in that document differs and is` - stays
- `:465` - (correct) `flagged there as a proposal, not yet team-agreed** — *approval may come from any` - stays

## Required (the checker's proof - each token ABSENT in the section before, PRESENT after)
- `## Pull Request Process` :: superseded 2026-09-11 (KS-1092): the approval, the PR is TESTED.**, reads to the QA gate

## Output
Exactly ONE ```diff block, ONE file section `--- a/Blockchain/Dev/CONTRIBUTING.md` / `+++ b/Blockchain/Dev/CONTRIBUTING.md`, 3 hunk(s) with the headers and counts exactly as in `## The exact change`. No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed9 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 10:32:32 AEST)
- `Blockchain/Dev/CONTRIBUTING.md` at the tip (690 lines) carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief_doc.py against `git show 8c2f7b3fd:Blockchain/Dev/CONTRIBUTING.md`; each hunk's old side matches exactly ONE place in the file); the rebuilt diff applies STRICT (`git apply --check -p1` rc 0 in the clone).
- section `## Pull Request Process` = `:366`-`:562` at the tip (`## ` heading list from `git show`); tokens ['superseded 2026-09-11 (KS-1092): the approval', 'the PR is TESTED.**', 'reads to the QA gate'] each 0 in that range before (the checker's D4 regex), each in a `+` line of the hunks above; every `-` site lies inside the range.
- Golden precheck through the real `tasks/doc_patch/checker.sh` in the clone: see `runs/2026-09-22_feed9-drafter-precheck/PRPROCESS/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1097 on the Secuura board at 2026-09-22 10:32:32 AEST: see `board_states.log` (In Progress, not archived). `Blockchain/Dev/CONTRIBUTING.md` is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
