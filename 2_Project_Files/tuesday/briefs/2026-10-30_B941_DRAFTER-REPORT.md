STARTABLE: YES after your stamp, but NOT at once: load1 read 7.83 at 13:15 (5-minute 10.36; six builders and three gates live), so launch_when_cool will hold it; CI on the head was mid-run at 13:13 (CodeQL neutral "2 configurations not found" pending the javascript-typescript and csharp analyses; unit, api and e2e jobs in progress; web (Next.js) not listed): the gate reads them last, after a wait

# B941 drafter report (2026-10-30, about 13:12 to 13:35 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-30_B941_SEAT-G218_hpsmpoc-249-readiness-training-gate-tier2.md` (67 lines; 8 four-underscore lines = 7 slots + the last line, lines 59-65 and 67, counted by `grep -c -E '_''_''_''_'`; at-sign slot pattern 0; non-ASCII bytes 0 by `LC_ALL=C grep -c '[^ -~]'`; person-name grep 0). Shape: the stamped B939 kit (checks C1-C9, severity, Stamp, Launch line), adapted to PR #249. Everything else was read-only: gh `-X GET` under the project `.gh-config`, `git --no-optional-locks` read verbs on the shared repo, no Jira call, no `cd`, no hosted HTTP, no ref written, no message, nothing written in the project folder.

## BLUF
Seat `Datasec/HPSM-POC-G218` (Sonnet, `BRIEF_SEAT_LEVEL=sonnet` inside the quotes), ports 9730-9739. It gates PR #249 @ `7ae229e9` (2 commits on main `e21d8044`, 0 behind, 23 paths +783 -56). Round 1 of 2 on class "readiness and training pages". The gate measures:
- the CONTENT RULE, by a census of every rendered text node at five tick counts and on /training;
- the priorities, against its own oracle at 8 tick sets, including the newest-completed-run rule;
- the bands and the content and PACKAGE_HASHES byte fences;
- each extension-file hunk, and that GlobalNav line 50 is unchanged;
- the menu list per role at base and head (this is the tier-1 tripwire);
- `safeReturnPath` at base vs head, with every REFUSED row still refused;
- widths, 44 px targets, axe, and the requests the pages make;
- 14 plants (p1-p13 red, p14 green; builder p1-p10 re-made, plus e2e rows for p5, p6 and p9);
- the suites, then CI and CodeQL last;
- the overlap with #246, by merge-tree plus a combined run.

## Facts re-measured (instrument; control)
- **PR and refs (13:12):** #249 is open, draft false, mergeable true, `blocked`. It has 2 commits, both unsigned. The title is 132 characters and carries both keys. The merge ref `0b95e323` has parents `e21d8044` and `7ae229e9`, and its tree `3f15ea71` equals the head tree. Open PRs: 244-249.
- **Patch read whole** (1183 lines). Exactly one added line has non-ASCII bytes: `playbook-event-states.spec.ts:56`, whose pre-existing ellipses sit on a line the PR had to touch. The builder disclosed it.
- **Hunks (`diff -U0`):** every extension file changes on exactly its named lines. GlobalNav changes at 27, 42-45, an added comment line before `shown`, and 63. Line 50 is byte-equal. proxy.ts, PlaybookShell.tsx, HomeScreen.tsx and ModuleScreen.tsx are byte-equal. `diff --stat` over the content, lib, api, ui, styles, css, package, config, scripts, .github and playbook files is empty.
- **returnPath.ts:** one line, with `"training"` inserted in sorted place. It is forced by `returnPath.test.ts:78`. proxy `needsSignIn` holds no per-route list; RETURN_SEGMENTS is the only per-segment list.
- **Modules:** subtitles are present for `introduction` and `beyond-year-1` only (`python3 -I` over the 0.6.1 package). The builder's "4 of 6 null" is right.
- **nav-dead-ends rows:** base 5, this PR 6, #246 5. So the combined tree should have 6.
- **CodeQL:** neutral, "2 configurations not found" (`/language:csharp` and `/language:javascript-typescript`). Analyses on pull/249/head: python and actions only, 0 results. Open alerts: 0.
- **Overlap:** b928, b929, b931, b932, b935 and b936 share 0 paths. b934 (#246) shares `nav-dead-ends.test.ts`: its lines 10-12 against this PR's 26 and the new 30-35. Control: the 23 against themselves gave 23.
- **Round count:** 101 GATE VERDICT first lines. The loose `readiness|training|#249` grep hits only B404 (a different PR and class). Control: B805 and B817 counted 2.
- **Ports, trees, panes:** 9730-9739 has 0 listeners (the unrestricted listing gave 20). `.tools/b941` and `.tools/wt-b941-head` are absent. There is no G218 pane. The instrument hashes match B939's: crawl.mjs, probe.cjs, lock.sh, waitload.sh; jira.py is `8ce98a09bb510842`.

## Builder claims found wrong or loose at drafting
1. **The READY line's red-at-base count is wrong.** It reads "59 of 78 rows (24 failed, 3 files failed to load with 35 rows; 19 green by design)". `red-at-base.tsv` has 78 data rows: 24 failed, 3 FILE FAILED TO LOAD and 51 passed. TESTED line 48 itself says 51 passed. The READY line adds 35 tests to a count of rows, and "19 green" contradicts 51. Minor (text), unless the gate's red-first table changes a verdict.
2. **"CodeQL on the new head: 0 alerts, 0 check runs"** was true at the push. There are now 18 runs. Superseded: a Note.
3. **The builder's text guard is looser than its claim.** Its `allowed` regex accepts any `n / m`. The gate's census builds its own allowed set from content. Note (instrument).
4. **HOLDS TAKEN (disclosed process deviations):**
   - a `git fetch origin` with the default refspec, against the kit's explicit-refspec rule;
   - a push although its kit called a shared path a STOP (`nav-dead-ends.test.ts` with b934).

   Both are Notes.
5. **The independent per-role array parser was "not completed"** (STATUS line 62). The gate's C4 program is the measurement.
6. **No plant e2e row was run.** The gate adds e2e rows for p5, p6 and p9.
7. **The base e2e a11y journey row timed out once and was never re-run.** The gate re-runs it 3 times at base.
8. **Stale words outside the lane** (the product owner's words; the builder listed them): `HomeScreen.tsx:9` "Assessments", `ModuleScreen.tsx:46` "on the Assessments page", the `shell-sidebar.spec.ts:416` title "nine entries" (the list is now ten), and the `AssessmentsHub.tsx:25` comment "the seeded one is complete" (the seed holds no completed run). These are Notes for FOR TUESDAY.
9. **Correct, and worth carrying:** the mock seed has no completed readiness run. The gate's probe completes its own run in its own mock space, so it can see the panels.

## D-decisions (mine, in the kit)
- **D-1:** The census builds its own allowed set from content and never reuses the builder's guard. Light; never cut.
- **D-2:** The priorities oracle is the gate's own program over the content JSON, at 8 tick sets.
- **D-3:** The role tripwire:
  - the per-role list diff must be exactly Assessments -> My readiness, plus Training for the four roles;
  - `safeReturnPath` is checked at base vs head, adding `/training//evil.test`, `/training/../admin`, `/Training` and `/trainingx`.

  Anything else means STOP, tier 1.
- **D-4:** The `shown` clause ignores the replacement entry's `roles`. This is a latent Note: it holds because `my-readiness` lists no roles.
- **D-5:** Plants: p11 (segment dropped), p12 (step description), p13 (band off by one), p14 equivalent (green).
- **D-6:** Hard stop: target 140 and HARD STOP 200 minutes after Step 0.

## Q-questions for Tuesday (each with a default)
- **Q-1:** Is `returnPath.ts:9` judged as the ruled allow-list addition, with the gate staying tier 2 unless anything else auth-shaped appears? Default YES.
- **Q-2:** Are the builder's disclosed deviations (the default-refspec fetch and the shared-path push) graded Note? Default YES.
- **Q-3:** Should the fetch include a third refspec for `b934`, plus the combined-tree runs (nav-dead-ends, GlobalNav, AppShell.sidebar)? Default YES; cut first under load.
- **Q-4:** What does a NO GO mean? Default: the PR is parked and Tuesday writes a round-2 fix kit.
- **S4 also asks you to rule** on the probe completing readiness runs in its own mock space on its loopback servers. Default YES.

## Reasons not to launch now
- Load1 was 7.83 and falling, with the 5-minute figure at 10.36. Three gates and six builders are live, so the waiter will hold the launch.
- CI is mid-run. This does not block a launch, because the gate waits for CI.
- B939 (G216) fetches b930 into its own clone and runs the same combined tree from its side. That duplicates work, but nothing collides.
- No other blocker. The head and main are as briefed, the ports and trees are free, and nothing is role- or auth-shaped beyond the ruled line.

## UNMEASURED
- Every runtime number in the kit is the builder's, written as a prediction.
- Whether CodeQL re-concludes after javascript-typescript and csharp complete.
- Whether `web (Next.js)` and the e2e shards pass.
- The ticket text. Jira was not re-read; it is relayed from B930 line 15.
- Hosted-mode signed-out `/training`, beyond the hosted e2e rows.
- The combined tree with #246.

## Outside-the-fences disclosure
None breached.
- Under `.tools/` I only computed sha256 prefixes of five helper and METHOD files (read-only) and listed `.tools/b941` and `.tools/wt-b941-head` (both absent).
- I did not open `.tools/b930/` or any `wt-b930-*`.
- I read the builder's STATUS and three evidence text files, and only counted the 30 PNGs.
- Scratch lives in the session scratchpad only: PR json, body, patch, file lists, refs, package json.
