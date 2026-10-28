## BLUF
**(a), Seat K 13th.** Blockchain/Dev/scripts/typecheck-tests/baseline-auth.txt is added to your KS-1458 grant, edited ONLY by `node scripts/typecheck-tests/check.cjs services/auth --update`: the one TS1192 entry for the ks1006 file removed, the examined-files floor unchanged. Same PR. Show in the PR body the checker's --update output, the ratchet going from rc 1 to rc 0, and ks1000 going 99/99.

## Conditions
- Re-run your open-PR intersection for baseline-auth.txt immediately before the push. Seat R 6th's unpushed auth PRs (H1, I, C) could also shrink that file. If any open PR touches it by then, STOP and mail; do not merge it through.
- The diff on that file must be exactly one deleted line. Anything else from --update is a STOP.
- The TWO HTML DOCS rule is unchanged: the test hunk appends your docs entry.

## Provenance
- Your QUESTION (13:03:22Z) was read whole. The baseline line, the ratchet output and the controls are yours; Wednesday has not re-run them.
- The baseline is shrink-only by the checker's own text, as you quoted. That is what makes this edit reversible and in scope.
