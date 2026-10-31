STARTABLE: YES (after Tuesday stamps: 8 four-underscore lines, S1-S7 at lines 53-59 and the last line 67; Q-1 to Q-6 to answer in S3)

# B1027 drafter report (SEAT-G254, tier-1 gate ROUND 2 OF 2 = THE CAP of branch b1016/hpsmpoc-388-security-workspace-part-b @ 7f0d832d, HPSMPOC-388), drafted Sun 2026-11-01 08:0x AEDT

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1027_SEAT-G254_hpsmpoc-388-part-b-gate-round2.md` (67 lines; sha256 `e0196e7591862d5c9fb475c44cacb9c769ae9ca2a332cf42677ffa4e268fa214`), plus its exact copy `.md.pre-stamp` (`cmp` equal, same sha256). Seat `Datasec/HPSM-POC-G254`. Ports 9280-9289. Opus (`claude-opus-5-5`), with `BRIEF_SEAT_LEVEL=opus` inside the launch quotes. Routing row G1 at `model-routing.md:108`, cap row at `:111`.

## BLUF
- **G-number G254 is free.** The `SEAT-G<n>` names in `tuesday/briefs` end at G253. A word search for `G254` over `tuesday/briefs` and `tuesday/*.md` finds 0 files; the control `G253` finds 11. No pane has that name. **B1027 is free too**: 0 files in `tuesday/` and 0 in the project's `Briefs/` (the control `B1025` finds 3 there).
- **The subject matches the commission**, by `ls-remote` and `gh api -X GET`:
  - The branch is at `7f0d832d`, whose parent is `db9c2625`. It is 4 ahead of main `77c3132e` and 0 behind.
  - The new commit changes 5 test paths, +78 -5, exactly as you said.
  - There is no PR, no check-runs (control: main has 19) and 0 code-scanning alerts.
  - `ci.yml` is the same blob as on main (`0176b491`).
- **The product is unchanged** (my own blob-equality program): 1423 non-test paths compared, 0 differ. The control pair `77c3132e` vs `db9c2625` shows 18 differing. The 5 removed lines are all import lines. The added lines contain 0 timers, 0 skip/only, 0 non-ASCII bytes, 0 `B###`, 0 ticket keys and 0 URLs. 5 new `it(` rows.
- **Round count:** 1 of 2 NO GO already on this class (B1022), so this is round 2 of 2 = THE CAP. A NO GO here closes the class and goes to the product owner.
- **The main risk, which Tuesday should see before stamping (Q-1):** one of the NEW plants you asked for, **g18b (roadmap actions taken from the OLDEST run), is predicted to SURVIVE.**
  - Why: R3's oldest run is its only scored run, and the harness result route returns the same result for every id. The builder kit's accepted D-1 ("No per-run result map") left it that way.
  - Under B1022's table, a g18-family survivor is **Major**, so with the default grading this gate would end **NO GO at the cap**.
  - The other four new plants (g3k, g3x, g4b, g4c) are predicted red.
- **Scope is bounded as you asked.** The gate runs no browser, no server and no e2e. Round 1's product measurements carry by citation to B1022 STATUS line numbers (C6 lists each one). The gate does run: the close-check plants, blob equality, the test-line checks, CI predicates at the head (expected 3782), the commit-message grades, four fresh landing files, and FOR TUESDAY with the veto list carried from B1022 line 211.

## Facts re-measured (instrument; control)
- `ls-remote origin`, run in the shared checkout with `--no-optional-locks`:
  - main is `77c3132e213b24616e6f1af9379d2fee66c889b7`.
  - `b1016*` lists only the subject, at `7f0d832d43d62e261abbcfa2ac6f37882d9d5718`.
  - `b1027*`: none. Control: `b101*` also lists `b101/four-wordings`.
- `git rev-parse 7f0d832d^` gives `db9c2625...`. `rev-list --left-right --count 77c3132e...7f0d832d` gives `0 4`.
- `git diff --numstat db9c2625 7f0d832d` (+78 -5 in total):
  - `SecurityReports.test.tsx` 41 2
  - `SecurityRoadmap.test.tsx` 15 2
  - `reports.test.ts` 9 1
  - `security.no-write.test.tsx` 1 0
  - `testing/harness.ts` 12 0
- Against main, by awk over numstat: 31 paths, +1072 -39. The same awk over `77c3132e db9c2625` gives 31, +999 -39.
- `gh api -X GET` reads:
  - compare main...head: ahead, 4 ahead, 0 behind, 31 files. compare db9c...head: ahead, 1, 5 files.
  - Pulls for this head: 0. Open PRs: 0 (control: closed 268, 267, 266).
  - check-runs on the head: 0 (control: main has 19). code-scanning alerts on the branch ref: 0. `verification.verified`: false.
  - ci.yml at the head and at main are both blob `0176b4915d69e3a42114c94e1af172a766a0a5cb`.
  - Squash settings: `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES`.
- Blob equality, my program (`python3 -I -B`, `git ls-tree -r` of both commits, the TEST regex as in the kit):
  - db9c vs 7f0d: 1423 non-test compared, 0 differ, 5 changed in total.
  - Control 77c3 vs db9c: 1423 compared, 18 differ (first one is `app/(app)/security/[customerId]/assurance/page.tsx`), 31 changed.
- Removed lines (`diff -U0 | grep '^-[^-]'`): 5, all import lines. Two are `vitest` imports gaining `afterEach`, two are `./testing/fixtures` imports gaining `run`, and one is `./reports` gaining `issuedRow`.
- Hygiene of the added lines. Each count has a control that fired:
  - non-ASCII 0 (control `\x80` reads 1)
  - timer, skip and only patterns 0 (control `+it.skip(` reads 1)
  - fake-timer patterns 0
  - `B###`, `HPSMPOC-`, URL and `localdomain` 0 (control `+B123` reads 1)
  - One `new Promise`: this is the harness's never-answering "pending" read, not a timer.
  - 5 added `it(` rows.
- Commit message: the subject is 116 characters and there is 1 `Co-Authored-By` (Sonnet).
- Plant anchors, counted with `git show 7f0d832d:<file> | grep -c -F` across SecurityReports.tsx / reports.ts / useSecurityData.ts. Each anchor is 1 in its own file and 0 in the other two:
  - g3 guard: 1 0 0
  - g3k key `` `security-reports:${rowId}` ``: 1 0 0
  - g4/g4b/g4c `rows.find(... "report-issued") ?? null`: 0 1 0
  - g18/g18b: 0 0 1
  - p5, p6, p7: 0 1 0 each
  - g14, in harness.ts: 1
  - zero control (no-such string): 0
- From the code (read with `git show`):
  - `useAsync` (`lib/use-async.ts:7-23`) does not reset state when its key changes. So under g3k (the key doesn't change) the ASM-B list is never asked for, and R1's `waitFor` should go red.
  - `top` is `runs.find((r) => reviewedBy.get(r.id))` (`useSecurityData.ts:77`).
  - The harness result route answers one result for every id (`harness.ts:57-59`). So g18b (oldest run) shows the same actions in every existing row and in R3: predicted survivor.
- `web/vitest.config.mts` sets no `isolate` and no `pool`, so the vitest default (per-file module isolation) applies.
- Harness at the head: line 18 `reports: [reportRecord("RPT-1")], issued: true,` (count 1). Line 20 `assessmentsFor: {}, reportsFor: {},`.
- Round count: a first-line loop over 539 `*_STATUS.md` files found 130 `GATE VERDICT` lines.
  - The part-B filter hits 2: B691 (unrelated, "Part B cells") and B1022 (NO GO round 1 of 2).
  - Control `security preview` hits 3 (B953, B965, B1022).
  - B1022's last line is `VERDICT: B1022 ... @ db9c262 NO GO (round 1 of 2) on main 77c3132`.
- Landing rule: the analysis repository main is `06e8d8f9` and `CLARIFICATIONS.md` has 5035 lines (`gh api -X GET`, raw).
  - Line 4860 is the PR #253 part-A entry, "a head-pinned squash".
  - Line 5018 is the PR #268 round-2-of-2 entry, "a head-pinned squash".
  - Control: an absent string reads 0.
- Ports 9280-9289:
  - `lsof` shows 0 listeners. With a `python3 -I -B` listener on 9289 it shows 2, then 0 after.
  - Word-boundary scan of the 59 non-`.pre-` SEAT kits from 2026-10-31 and 2026-11-01: `928[0-9]` hits 0. Controls: `927[0-9]` hits 1 (B1022) and `963[0-9]` hits 1 (B1025).
- Panes at 08:02: `%0 tuesday`, `%142 Datasec/MPS-R107`, `%139 Datasec/NexusAI-G253`, `%1 fleet-monitor`. No HPSM-POC pane. Load at 08:02: `2.92 4.22 5.07`.
- `.tools` names: `b1022`, `b1025`, `wt-b1022-{base,head,mut}` and `wt-b1025-{fix,mut}` exist. Both `wt-b1025` trees are at `7f0d832`. No `b1027` name exists.
- Routing and model: `model-routing.md` lines 92 C2, 108 G1, 109 G2, 111 G-cap. `models_latest.json` line 17 is `claude-opus-5-5`. `brief_seat.sh` line 24 is `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`. I read the header of `launch_when_cool.sh` (lines 1-40): two reads 20 s apart, a 120 s gap, one waiter (a second one gets rc 5).

## D-decisions (drafter's, in the kit)
- **D-1** Product measurements carry by citation. This depends on C1 (a) finding 0 differing non-test blobs AND main not having moved; if a product byte changed, it is a STOP. So the gate runs no browser, no server and no e2e, and starts no Jira call.
- **D-2** The gate makes its own plain clone with ONE two-refspec fetch, as in B1022. A plain clone of the shared repo may not contain the head commit, because the branch tip exists there only as a remote-tracking ref.
- **D-3** The gate gets three worktrees: head, mut, and `prev` (at db9c2625, used only for the vitest name baseline). `node_modules` comes from one `npm ci` and is copied with `cp -Rc` after proving the lockfile blobs are equal.
- **D-4** Five NEW plants on the same rules:
  - g3k: the read keyed by row count instead of row id
  - g3x: g3 plus g3k together
  - g4b: `rows[1]`
  - g4c: accepts a scored row
  - g18b: actions from the oldest run

  Controls c0, c1 and g19. Every survivor needs a behaviour proof from a scratch module-mock row; one that shows no behaviour difference is graded EQUIVALENT.
- **D-5** Grading of new-plant survivors, written into the kit's round-2 severity rows:
  - g3x, g4b, g4c survivors are **Blocker**: a release-rule pin gap where a wrong or unissued report could be released.
  - g3k and g18b survivors are **Major**: safe direction, the B1022-3 precedent.
  - A g3/g4/g18/g14 red that shows ONLY in an old row does not close the finding.
- **D-6** The two cheap `npm audit` steps are included. Repeats are 3x, not 10x.
- **D-7** Target is 90 minutes, hard stop 150.
- **D-8** The landing files are written fresh into `B1027_evidence/`. Round 1's files are the starting text and are never edited. The squash body replaces all FOUR messages and has exactly one Opus trailer.
- **D-9** The kit adds a C5 check: B1022-7 (the A2 reading) must stay unpinned. B1022-16 is carried as Open and not re-run.

## Q-questions for Tuesday (default first; answer in S3)
- **Q-1 (the one that matters): how is a NEW-plant survivor graded at the cap?** g18b is predicted to survive. DEFAULT: as your commission says, grade it by B1022's table, which makes it Major, so the result is NO GO at the cap and the class goes to the product owner on a card (the residue is a per-run result map in the harness plus one two-scored-run row). Alternative: rule that a survivor of a new, non-round-1 plant at round 2 is a Minor residue to be ticketed (the G-cap line: "ship the closed instances, ticket the residue"). That would let a GO WITH FINDINGS land the closed B1022-1 to -4.
- **Q-2** Run the five new plants as listed? DEFAULT yes. Alternative: drop g18b and keep the other four (this meets "at least two").
- **Q-3** Allow the `prev` worktree for the name baseline? DEFAULT yes, and it is cut first under load (the fallback is B1022's 3777 plus a grep for the 5 titles).
- **Q-4** Include the two audits, even though the lockfile is unchanged? DEFAULT yes (they take seconds; hosted CI runs them anyway).
- **Q-5** May the PR title and squash subject carry `HPSMPOC-388`, as you stamped for B1022 (Q-5)? DEFAULT yes.
- **Q-6** Ports 9280-9289 and pane `Datasec/HPSM-POC-G254`? DEFAULT yes. No server is expected; 9289 is only the positive-control listener.

## UNMEASURED
- I ran no worktree, no npm, no vitest and no plant. Every row and plant result is a prediction for the gate to test, including g3k's red going through a `waitFor` timeout, and g18b surviving.
- The 205-row frame count at the head is the builder's claim.
- I did not check whether `git clone --no-hardlinks` of the shared repo would already contain `7f0d832d` (D-2 makes the fetch regardless).
- Whether hosted CI's audit result has changed since round 1. The registry advisories are time-dependent.
- I did not open the B1022 `plants.py` or quarantine scratch file. The kit tells the gate to read them as text.

## Outside-the-fences disclosure
- **Files written: three, not two.** The kit, its `.md.pre-stamp` copy (which your commission asked for) and this report. I wrote the kit with Write. After that, two small text fixes went in through a `python3 -I -B` exact-replace (each anchor asserted to be present once), and the `.pre-stamp` was made with `cp`. Both are content-identical to a Write/Edit; the DRAFTER_RULES fence says "with the Write/Edit tools", so I am naming it here.
- One fix removed a person's name: the first draft quoted the G-cap row's last sentence verbatim, and that sentence names the product owner. The kit now paraphrases it as "the product owner's word". The other fix corrected the wording of a `C-[0-9]` hygiene check so that `HPSMPOC-388` does not count against it.
- Scratch files, all in the session scratchpad and none in a project: `blobeq.py`, `clar.md` (a GET copy of the analysis `CLARIFICATIONS.md`) and `gl.txt` (the gate first lines).
- The 9289 control listener ran for 6 s and was gone afterwards (`lsof` read 0).
- I did not read: `decision_queue.sh`, `fleet/briefs_staged/`, `scoreboard.md`, `_ledger.md`, any WEDNESDAY or FRIDAY tree, or any non-Datasec project. In the project I did not open `.tools/b1022/` or `.tools/b1025/` contents, only listed their names, and I opened no HP document.
- Git in the shared repo was read verbs only, with `--no-optional-locks`: ls-remote, cat-file, rev-parse, rev-list, diff, show, ls-tree, log, worktree list. `gh` was `-X GET` only, under the project `GH_CONFIG_DIR`.
- No Jira. No HTTP to any hosted host.
