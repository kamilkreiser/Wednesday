# REPORT, HPSM-POC focus-ring PR text (drafted Wed 4 Nov 2026, between 07:22 and the `date` printed at the end of this run)

## BLUF
PR title, PR body, squash subject and squash body are written and ASCII-clean. The branch is clean to land: ahead 5, behind 8 of origin main b76c0a97, status "diverged", and NO file is changed on both sides since the merge-base c1457349 (10 branch files against 78 main files, overlap 0). Nothing in the sources contradicts the card in a way that changes the decision; three softer differences are listed next.

## Where the sources differ from the card's BLUF (first)
1. "One weaker-than-asked test row": the STATUS holds more than one. B1228-3 (plant ph2, the 252 px padding value is not pinned) is the one the card means. Also in the STATUS: B1228-7 Notes (the "300 px or its end" row does not pin a start at 300; the `covered` check reads one point) and B1198-2 (Minor pin gap, still open, not re-measured). Body says "one test row" for B1228-3 only, and says nothing of the others.
2. "No code change" (the card option) against the STATUS fix-shape for the Firefox floor: "a `browserslist` entry" (STATUS 209) and `package.json` is a protected file (STATUS 28). The body says the floor is a recorded decision, that this change adds no browser list, and that the recording is a records step.
3. The card says Chrome; the instrument was Chromium (Playwright) and Firefox and WebKit were never run (STATUS 220). Body says "Chromium only".
Not a contradiction but a limit: the 64 px page shortening and the 133 px band are measured against the previous revision of this branch (round 3), not main. How main compares is UNMEASURED; the residue file says main "has neither the overhang nor this shorter page" and the body does not claim a main comparison.

## Behind main
Compare main-side read with `gh api -X GET` as `compare c14573495e51...b76c0a979a99` (merge-base to origin main): ahead 8, 78 files. The branch's head compare reads ahead 5, behind 8. At the gate, behind was 7 (main 69338b6); the eighth is #281 (b76c0a97, HPSMPOC-440), which the gate's tree did not include. Overlap of file names: 0 (the 10 branch paths: shell-sidebar.spec.ts, globals.css, layout.tsx, the Home paths, AppShell.sidebar.test.tsx, Sidebar.tsx). Compare lists 78 files, under the 300 cap. Hosted CI on the PR's merge ref is the first run of branch plus #281; the gate re-ran on main 69338b6 only (unit 3911/0/0).

## Facts re-read
- Origin main b76c0a97 and the branch head 58ac1077 were read by `gh api` compare, not assumed; pr_body_facts.py (rc 0, read whole) gave 10 files, +618 -7, 5 product, 1 spec, 2 test modified, 2 test added: the same figures as STATUS line 31.
- Ticket keys: no branch commit message names a key (the builder brief forbade it). The keys come from the B1097 builder brief lines 23 and 28: HPSMPOC-406 item 1 and HPSMPOC-412 (the two Home sentences), HPSMPOC-399 ring clause, HPSMPOC-368 criterion 10. Main's own PR titles put keys first ("HPSMPOC-440: ...").
- Landing rule: head-pinned squash (`gh pr merge N -R datasecau/HPSM-POC --squash --match-head-commit 58ac10775f1d3cde07a3f37918c1976e900e86d2`), source STATUS 177 (CLARIFICATIONS in the analysis repo, 3617 there). The local CLARIFICATIONS.md (192 lines) has no landing rule and names no focus-ring, Firefox or B1097 entry; the analysis repo's copy has no entry on this branch's public-text naming either, and the sampled merged messages put keys in subjects.
- All five existing commit messages hold two sentences the gate found void or false in part (B1228-4: "1092 walks, 25584 presses", "customer menu 21 walks", "accepted that short pages end sooner"). The squash body replaces them and repeats none of them.
- Dates: the ruling "2026-11-04 07:16 AEDT" is from Tuesday's brief, not from a file; no clock appears in the public text beyond the date 2026-11-04.

## Questions for Tuesday
- Q-1. Title keys: all four (HPSMPOC-406 HPSMPOC-412 HPSMPOC-399 HPSMPOC-368). 399 and 368 are closed only in part (ring clause, criterion 10); the Home sentences close 406 item 1 and 412. Default: keep all four as written; the body says plainly which part. Alternative: "(part)" for 399 and 368 as PR #272 did.
- Q-2. GitHub appends " (#N)" to the squash subject; both subject files omit it. Default: omit.
- Q-3. The body names no card id, brief number, seat or lane. It does say "the product owner's decision of 2026-11-04" as the brief supplied. Default: keep.
- Q-4. The body says the weaker row "is ticketed separately" and the floor "is recorded in the project" as things that will happen. Default: keep only if those records exist by merge time; otherwise change to "is to be ticketed" and "is to be recorded".
- Q-5. The 8-versus-9 new-row claim ("Eight of the nine new browser rows fail on the earlier build"): STATUS 123 reads 8 new rows x 2 projects red, the collapsed row green by design. Default: keep.
- Q-6. After the merge the gate's wording about hosted checks: the body ends "through the hosted checks and CodeQL" without a result, because none exists yet (no PR; STATUS 176 CodeQL NOT RUN). Default: no result claimed; add the CI and CodeQL facts to the merge comment, not to the PR body.

## UNMEASURED
Firefox and WebKit; main-versus-landing page height and band; the overhang at 20 and 24 px root sizes by trips (derived only); CI and CodeQL on this head.
