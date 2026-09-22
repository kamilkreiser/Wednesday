# KS-1097-C R16B-REVIEWREQ - re-brief at develop 8c2f7b3fd of READY_KS-1097-C_ornith35b-q4_DOCPATCH-MERGED-PASS-7of7_2026-09-15.diff.md - **DOCUMENTATION (`Blockchain/Dev/CONTRIBUTING.md`, no code)** (written 2026-09-22 10:32:41 AEST by Wednesday's feed9 drafter; the hunks are the old READY's applied PASS 7/7 output re-anchored at the tip: every context and `-` line asserted byte-exact at the line numbers below, headers recounted, every `+` line ASCII)

Tip: 8c2f7b3fd4fde915b2a24542bc32259b24e092a0
File: `Blockchain/Dev/CONTRIBUTING.md`

## What is wrong (one paragraph)
KS-1097 carries six Polish findings from the tier-2 gate on PR #957 (KS-1095). **This part fixes the TWO sites inside the `## Related Issues`
block of `Blockchain/Dev/CONTRIBUTING.md`** (the merge-signal bullet list at lines 596–606), with the ticket's ruled wording: QA-957-3 at
lines 600–601 ("— not the reviewer" has no referent — drop the phrase and keep the parenthesis) and QA-957-2 at lines 603–604 ("The gate is
approval + a Test Evidence block…" still differs from the other gate statements — state it as a TESTED PR + Wednesday's GO naming the head SHA).
Nothing else changes — NOT lines 598–599 (already the ruled shape), NOT 602, NOT 605–606. Parts A (DEV-PROCESS.md), B (this file's
`## Pull Request Process`) and D (`CLAUDE.md`) are separate tasks.

## The exact change - 2 hunk(s) in `Blockchain/Dev/CONTRIBUTING.md` (3 `-` line(s), 2 `+` line(s), one `+` group per hunk)
Copy the block below BYTE FOR BYTE as your whole diff: the two file-header lines, each `@@` header, every context line (a leading space, copied from `files[product_file]` - several carry an em-dash or an arrow: copy them, never retype them), every `-` line and every `+` line, in this order. Do not add, drop, re-wrap or reword a line; a blank context line is a single space; never write a literal `\n` inside a line. Every `+` line is ASCII.
- every `+` line was ASCII already in the old READY.
```
--- a/Blockchain/Dev/CONTRIBUTING.md
+++ b/Blockchain/Dev/CONTRIBUTING.md
@@ -608,5 +608,4 @@
 - TESTED before merge, as defined in step 6 of *Adopted merge flow* above, and
   Wednesday's GO naming the head SHA (Kam, 2026-09-11)
-- **The author performs the merge**, once the PR is TESTED and has Wednesday's GO —
-  not the reviewer (Kam, 2026-09-11; see *Adopted merge flow* above)
+- **The author performs the merge**, once the PR is TESTED and has Wednesday's GO (Kam, 2026-09-11; see *Adopted merge flow* above)
 - The ticket and the review must not sit with the same person
@@ -613,5 +612,5 @@
 - **GitHub Actions is retired** (Kam, 2026-08-27) — there are no CI checks to
-  pass. The gate is approval + a Test Evidence block filled from local runs
+  pass. The gate is a TESTED PR (see *Adopted merge flow*, step 6) + Wednesday's GO naming the head SHA, with the Test Evidence block filled from local runs
 - A filled-in **Test Evidence** block in the PR description, including the four
   platform-suite lines and the unit-suite line — the author's final check
 - No unresolved review comments
```

## Where (every **must change** line must appear as a `-` line in your diff, at its number)
- `:610` - **must change**: `- **The author performs the merge**, once the PR is TESTED and has Wednesday's GO —`
- `:611` - **must change**: `  not the reviewer (Kam, 2026-09-11; see *Adopted merge flow* above)`
- `:614` - **must change**: `  pass. The gate is approval + a Test Evidence block filled from local runs`
- `:608` - (correct) `- TESTED before merge, as defined in step 6 of *Adopted merge flow* above, and` - stays
- `:609` - (correct) `  Wednesday's GO naming the head SHA (Kam, 2026-09-11)` - stays
- `:612` - (correct) `- The ticket and the review must not sit with the same person` - stays

## Required (the checker's proof - each token ABSENT in the section before, PRESENT after)
- `## Related Issues` :: Wednesday's GO (Kam, a TESTED PR (see

## Output
Exactly ONE ```diff block, ONE file section `--- a/Blockchain/Dev/CONTRIBUTING.md` / `+++ b/Blockchain/Dev/CONTRIBUTING.md`, 2 hunk(s) with the headers and counts exactly as in `## The exact change`. No prose before or after the block.

## Premises (measured at develop 8c2f7b3fd4fde915b2a24542bc32259b24e092a0 by the feed9 drafter, scratchpad `--shared --no-checkout` clone, 2026-09-22 10:32:41 AEST)
- `Blockchain/Dev/CONTRIBUTING.md` at the tip (690 lines) carries every context and `-` line of the hunk(s) above BYTE FOR BYTE at the line numbers in `## Where` (asserted by rebrief_doc.py against `git show 8c2f7b3fd:Blockchain/Dev/CONTRIBUTING.md`; each hunk's old side matches exactly ONE place in the file); the rebuilt diff applies STRICT (`git apply --check -p1` rc 0 in the clone).
- section `## Related Issues` = `:601`-`:622` at the tip (`## ` heading list from `git show`); tokens ["Wednesday's GO (Kam", 'a TESTED PR (see'] each 0 in that range before (the checker's D4 regex), each in a `+` line of the hunks above; every `-` site lies inside the range.
- Golden precheck through the real `tasks/doc_patch/checker.sh` in the clone: see `runs/2026-09-22_feed9-drafter-precheck/REVIEWREQ/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1097 on the Secuura board at 2026-09-22 10:32:41 AEST: see `board_states.log` (In Progress, not archived). `Blockchain/Dev/CONTRIBUTING.md` is on neither 18th seat's GROUPING list (Seat B: shared/anchoring/auth/originate; Seat C: api-gateway).
