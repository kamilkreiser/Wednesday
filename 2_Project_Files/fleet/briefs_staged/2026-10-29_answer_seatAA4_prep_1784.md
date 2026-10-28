## BLUF
Prep #1784 (KS-1537) now, Seat AA 4th, as docs section **90**. #1778 is MERGED and verified at origin by Wednesday: develop = **d4fc0b8f26415014a31d2b2da73ae2dfdedbc4ac**. In the ONE push:
1. Merge develop in. Take develop's two docs whole and re-apply your entry renumbered to 90.
2. Make the **wording fix gate 3 owed before merge**: the stale sentence on the org-erasure operation at originate.openapi.ts:3717 (yaml ~31333, by the gate's citation) contradicts the PR's own reserved-key text. Make it say what the code does. Regenerate the yaml; check:openapi rc 0.
3. Add the **guard cell** owed with it, per the 22:2x ruling (the cell that pins the reserved-key behaviour the corrected sentence describes). Red-prove it against a mutant copy.
Then push through the queue and mail the head with the old and new sentence quoted.

## What the completion check will compare
- Every blob except originate.openapi.ts, the yaml, the new or changed cell file and the two docs must equal the gated head 66c36a960af6128b's.
- The contract delta must be that sentence only (word-diff).
- The docs delta against develop must be section 90 only, with 0 removed lines.

## Provenance
- develop: ls-remote d4fc0b8f2641 by Wednesday this action. Its tree 427080db0df9 equals #1778's head tree; single parent 8fbda28e6e79.
- The owed items: gate 3 verdict, 0_Brain/reference/2026-10-28_gate3-batch5/verdict.md (#1784 FIX BEFORE MERGE), and Wednesday's pickup 22:2x block ("wording fix + guard cell"). Wednesday has not re-read line 3717 at develop.
