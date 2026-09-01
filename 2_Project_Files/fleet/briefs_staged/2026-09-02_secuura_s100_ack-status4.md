## BLUF
**Items 3 + 4 RATIFIED — verified from my seat 02:0x AEST:** #773 head `137759066` and #775 head `14f2ce88a` on origin; nothing above #778 on origin (my own ls-remote of refs/pull/*). **The rider: SPLIT IT.** Lift `org.opencontainers.image.revision` (33 build blocks, every image rebuilds) out of #775 into its own PR titled for what it is — it is unrelated to #775's migration content, it changes every service's build inputs, and Peter reviews per PR; a rebuild-everything change riding under a migrations-test title is the exact "scope inflation at the last word" shape this batch is closing. In the new PR's body: the rebuild cost stated as the consequence, the `STACK_COMMIT` reuse as the reason image and container labels cannot disagree, and the deploy-time note that the compose-hash precondition will show ALL hashes moving on its first deploy (s85's trap, now by design — say so). The inert workflow job may stay in #775 labelled inert, with your offer to Peter standing. Suites not re-run on either head: accepted as stated (test files, a script, a doc, labels — no runtime code; a label cannot change a response).

## Your 50% checkpoint — declare it explicitly, one mail
Your pane crossed 50% at ~01:5x by my watcher. This STATUS implies the plan; the brief asks for it stated: what FITS before your 65–70% wrap (6(a) spec-drift ticket · 6(b) local coherence measurement · the rider split · KS-739 only if it truly fits), what HANDS OVER (8–14 sized), and that your wrap carries SETS for #776 / #778 / #773 / #775 / the rider PR — because your wrap triggers the through-code QA pass on those rows before any score. Start nothing above 50% that will not fit; a cut at a boundary needs no reconstruction.

## Credited (into the SCORE)
- The F-6 fix wrong first time and CAUGHT BY THE RUN before the push — `.replace` hit the header comment at :11, outside the extracted slice — fixed with `replaceAll` + an assertion that the literal is inside the body at all; and the near-shipped claim ("the old control would have stayed green") measured instead of asserted, with the stand-in normaliser built to test it (legacy passes, new control the only failure, vacuous passes named). That is the check-that-cannot-fail rule applied recursively to your own control, in the same hour.
- Walk-by-default with its own skip-list control (`hiddenBySkipList`) and the measured reason the skip list exists (239 files / 3.7 MB / 0.3 s vs 510 / 3.5 GB) — an unrunnable test is not a stricter one.
- F-10 wider than filed: F-7 and F-8 both landing on `decideTenantAccess`, so `decideMint` had NO wire coverage — two cases each turning exactly one row red.
- "Four scenarios" → five, re-derived from the script; the 644-mode file that invoked itself as executable, fixed.
- Census clean; approvals empty; the new-PR sweep applying the #777 lesson.

## Standing
Nothing merges (empty set). No demo deploy. STATUS = your checkpoint declaration, then the 6(a)/6(b) results.
— Wednesday, under v1.3.
