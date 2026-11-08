# Gate 260, tier 1 COMPARE, round 2 of 2 (the cap: a NO GO ends it, closed findings ship, the residue is ticketed): PR 2091 (KS-528, react-router 6 -> 7). Launched 2026-11-08 by the 22:4x Wednesday seat

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole first. Corrections: develop abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82 and PR 2091 head e5742b73748b6ae49f942f4bb8a797f4e076e5b2, both by Wednesday's `git ls-remote origin` at 23:04:49 AEDT; re-read both at start and end, and if either moved say so first. QA no-rm (leave your clone at /private/tmp/g260, name its size); one clone; stop under 12 GiB free on DevMASTER; load1 under 8; never cd; never write into /Volumes/DevMASTER/!CODING/ (read-only, its .git included).

This is a COMPARE gate on round 1's findings, not a fresh review. Round 1 = gate 255, GO WITH NOTES at 258e049aaf75: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_gate255-tier1-pr2091-ks528/verdict.md (read whole). Wednesday did NOT merge it as is because F1 is a user-visible behaviour change the PR body denied. The builder's READY for round 2 (Seat R 89th; its claims, not Wednesday's): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-08_seatR-89th/mail/ready_pr2091_r2_r89.md, evidence under that folder's evidence/.

Questions, in order:
1. F1: does the issuer show its 'Loading...' screen again on lazy navigation at the new head, as it did under react-router 6? Reproduce in a real browser against your OWN build of the head and of its parent 258e049aaf75 (the round-1 head) and of develop, with a held lazy chunk; the builder measured 8 of 8 on the head and control and 0 of 8 at round 1. Your own predicate must be visibility, not DOM presence (the builder's first run had that fault). Admin and verifier: still unaffected?
2. F2: do the PR body, the two docs fragments and KS-528 comment 2083ebbe now say true things (the 'no intended behaviour change' claim gone or made true; round 1's walk could not see F1)? Read the live body and comment through the GitHub and Linear APIs read-only.
3. F3: the import-comment wording against the installed 6.30.6 and 7.18.5 packages.
4. F4: the widened package-format checker: red-first on its six new mutants, 25 of 25 at the head, real files unchanged by the run. Can any of the checker's NEW rules refuse a legitimate shape already on develop (run it on develop's real manifests)?
5. Anything round 2 changed beyond F1-F4 (diff 258e049aaf75..e5742b73748b, 26 files): name each file outside the four findings and judge it.
6. Merge-tree of the head on the current develop, rc and tree; the 11 PRs the builder's overlap grant ignored: does any of them now conflict with the head (merge-tree each)?

Verdict line 1: GO, GO WITH NOTES or NO GO. Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_gate260-tier1-pr2091-r2/verdict.md, with a NOT TESTED list. Findings only; post nothing anywhere.
