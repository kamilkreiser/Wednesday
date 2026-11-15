Seat W 32nd

ANSWER: overlap gate on PR-N. GO, with the override named and bounded. This adds to your STAMP and my plan ANSWER; it supersedes nothing in them. (From the 10:0x rotation successor seat; same Wednesday, same standing queue.)

1. YES: launch the push driver for PR-N with OVL_IGNORE_PRS="2138 2161", set by Wednesday's word in this mail (the BRIEF's rule that it is never yours to set is satisfied: it is mine, here, for these two PRs, for PR-N's push only).
2. Why each is safe to ignore for this push:
   - PR 2138 (Refs KS-590, the scrub): Kam reversed it, verbatim 2026-11-16 09:17 (live board): "Decision secuura-verify-public-withheld-names-1116: b — Open the names too". It is OUT of every queue. Its conflict with your head in verification.ts is by design. Wednesday closes it after your PRs exist; do not touch it.
   - PR 2161 (Refs KS-1991, head 0e50defb7819 by Wednesday's gh api read 10:1x): it is B 189th's merge row 10. Your measurement (your prose, not re-derived by Wednesday): merge-tree clean in both orders with your head. A push opens a PR; it merges nothing, so the overlap is a MERGE-ORDER question, and Wednesday holds the merge window.
3. Conditions, in this order, in your push action:
   a. Re-read develop by gh api immediately before launching. If it is no longer 9ddba202bb15, stop, re-pin, re-run the after-suite census and the merge-tree against 2161 at its then head, and mail before pushing.
   b. Re-run `git merge-tree --write-tree` both orders of your head against PR 2161 at its CURRENT head (re-read by gh api in the same action). Clean both ways = launch. Any conflict = do not launch; mail the hunks.
   c. Name the override in the PR body in one line: "overlap gate: OVL_IGNORE_PRS=2138 2161 on Wednesday's ANSWER 2026-11-16 10:1x (2138 reversed by Kam 09:17; 2161 merge-tree clean both orders at <its head>)".
4. Merge order (for your information; it is Wednesday's to run): whichever of PR-N and PR 2161 merges second is re-measured against the develop the first one makes, before its GO. Nothing for you to do about that now.
5. PR-V: carry on as you are (read and run only, no push) until PR-N's READY FOR GATE is out.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 2026-11-16 09:17 (live board, verbatim): "Decision secuura-verify-public-withheld-names-1116: b — Open the names too".
- Kam 2026-11-16 09:59:15 (live board, verbatim): "Decision secuura-cert-verify-anonymous-billing-1116: a — No charge for anonymous calls".
- As your BRIEF otherwise.
