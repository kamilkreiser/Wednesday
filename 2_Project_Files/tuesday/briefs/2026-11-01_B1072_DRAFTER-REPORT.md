STARTABLE: YES (after Tuesday stamps the 8 slots; launch only after the live launch waiter exits and load1 is below 7)

# B1072 drafter report (kit SEAT-G267, tier-1 gate of branch b1059/hpsmpoc-417-412-link-targets-tile-title @ 954996c8)

Drafted Sun 1 Nov 2026 23:57 to Mon 2 Nov 2026 00:10 AEDT by the C8 Sonnet drafter (routing row C8, `model-routing.md:98`). Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1072_SEAT-G267_hpsmpoc-417-412-gate-tier1.md` (89 KB, 10 checks C1-C10, shape of the B1071 kit, web instead of dotnet).

## BLUF
The kit is startable. Pins at 00:09:59: branch `954996c8` (unchanged), main `d8981b0e` (unchanged), 0 PRs for the branch, 0 open PRs, 0 `b1072*` refs, 0 listeners on 9200-9209, no `.tools/b1072`. Opus, row G1 (`model-routing.md:108`), `BRIEF_SEAT_LEVEL=opus` inside the quotes, model id `claude-opus-5-5` (`models_latest.json:17`). The gate re-derives targets by its own browser census at base and head (11 widths incl. 360, which the builder never ran), the 24 px shift, the pill, inline flow/focus/names, the words, commit-2 revertibility, red-first, plants, e2e, and writes the four landing files.

## Facts re-measured with instruments (all `gh api -X GET`, `lsof`, `tmux`, python byte programs; controls fired)
- Branch/main/compare: head `954996c8`, ahead 2, behind 0, 6 files, +191 -7 (commit 1 `477d5191` +143 -6 four customer files; commit 2 +48 -1 two partner files; disjoint). Check-runs at head 0 (control main 19); actions runs 0; `ci.yml` blob `0176b491` at head and main (679 lines, `git hash-object` of the raw read).
- Main-moved control: `compare 77c3132e...d8981b0e` lists 31 `web/` names; `compare a026cb30...e8ac3f29` lists 1 under `customer/`; `compare d8981b0e...main` 0.
- Added-line program (difflib over the main and head tarballs of the 6 paths): 0 non-ASCII; 0 skip/only/eslint-disable/ts-ignore/setTimeout/B###/C-n/ticket key/localdomain; 2 lines hold `http://mock.test` (`parts.targets.test.tsx:19,22`; 44 existing test files at main hold the same host: kit makes it a Note). Control B123 planted reads 1.
- Builder's census frame is real: 40 states x 9 widths (390 minimum), 23 links under 44 at base, 13 at head, pack link `ClientPacks.tsx:201` 18 px. My own static census of `<Link|a` tags without `min-h-11` (single-line tags) printed 18 at main and 11 at head (kit's "19" was a lead; multi-line tags such as `ServiceReport.tsx:169` "Open the PDF" are missed by single-line scans: the kit makes the gate find it in the browser).
- Web CI predicate read at the head: `web-build` 371, `web-unit` 450, `web-e2e` 483 (five shards, 491), `web (Next.js)` 526-548 (`want` 540, `bad` 543); node 24 at 384. Repo allows squash, merge and rebase; defaults `COMMIT_OR_PR_TITLE` / `COMMIT_MESSAGES`.
- Records repo `CLARIFICATIONS.md` 5194 lines at `6775fccc`: `Delivery phases` 0, `Service offers` 7, `head-pinned squash` 91 lines; the PR #271 landing sentence is now at line 5142 (the B1071 kit cites 5143; the kit says find it by text).
- Tickets today (Jira GET through `.tools/b649/jira.py`): HPSMPOC-417 and -412 both Backlog, 0 comments; Done-when texts match the builder's relay.
- Round count: 133 gate lines in 553 STATUS files; 0 classes name 44 px/targets; the 44 px items were Notes of B964 and B967 (GO WITH FINDINGS round 1); the tile was B960-3. Nearest surface class is "partner home" (B947 NO GO round 1, B962 round 2 = the cap): the kit makes the gate answer "new class or renamed" in a paragraph, default new class, STOP for Tuesday if it concludes otherwise.
- Existing pins found: `playbook-feedback-pill.spec.ts` (pill clearance, 44 px assertion at :101, boundingBox :115), `step-previous.spec.ts:47`, `playbook-home-phase-flow.spec.ts:39-41`, `playbook-followup.spec.ts:316`; 0 `toHaveScreenshot` (control: 54 e2e files hold `expect(`); 23 unit test files pin `min-h-11`.
- Builder-claim defects the kit asks the gate to grade: commit 1 says 6 red / 3 green (builder measured 7/2); commit 2 promises "one forward revert" but the landing is a squash (after which the label is a one-line edit); the tile test duplicates the literal "Delivery phases" after the MAIN_NAV tie; STATUS first line is a stale `PROGRESS ... PENDING`; two -1280 findings screenshots share a byte size at base and head with different sha256; the pill was not measured; 360 px never run; `items-center` is a vertical-centring token that does not bear height (browser plant B2 proves it).

## D-decisions (drafter's, Tuesday accepts or strikes at the stamp)
- D-1 Tier 1 on Opus (G1: client testers see these pages), as the builder kit's GATE-ROUND slot ruled.
- D-2 Ports 9200-9209 (lsof 0 + word-boundary kit scan 0, control 919x hits only B1071; 927x-929x in B1022/B1027/B1036 are outside the block). Map: 9200 base, 9201-9203 Playwright's three, 9204 head, 9205 plant, 9206 control listener.
- D-3 Builder tools (`.tools/b1059`, `wt-b1059-*`) READ-FORBIDDEN though H93's pane is gone; G266's trees and 9190-9199 READ-FORBIDDEN. `.tools/b949` hv/runspec/spec are patterns to copy with a printed diff (they hard-code b949 ports 9801-9803).
- D-4 Widths include 360 (the user's list) and 412 (the project's own mobile device), plus the edge widths the builder used.
- D-5 Pack link `ClientPacks.tsx:201` is a Condition (both tickets stay open), not a finding; any byte in `ClientPacks.tsx` is a Blocker. The PR/squash text must not say either ticket is done.
- D-6 Gate never reads the decision board; the label question is cited as open only. Commit 2's revertibility is proved by reverse-apply in `wt-b1072-mut` (base+9 and base+3 unit counts), and the squash truth is put in the note list.
- D-7 Hard stop suggestion 240 min (target 180) because of three `npm ci`, two builds, two censuses, 26 plant runs and the whole e2e; cut order stated (e2e whole run is cut after census and plants).
- D-8 Plants: builder's P1-P6 + P4b re-run, own g1-g14 (g7/g10/g11 predicted survivors/pin gaps, g13 equivalent control, g14 brittleness control), browser plants B1/B2 (24 runs max).

## Q-questions for Tuesday (each with a default)
- Q-1 Does commit 2 (the label) land in this squash, or wait for the product owner's answer on the label? Landing commit 1 alone needs a branch the gate cannot make (the builder's seat is gone). Default: the gate delivers the data (head~1 is green, label is a one-line edit after a squash); Tuesday decides at the verdict; the kit's note list states the truth either way.
- Q-2 The `launch_when_cool` waiter file now holds a pid (60884) at 00:10, so a launch is pending; load1 7.63 at 00:10 (was 4.33 at 23:57). Default: launch G267 only after that waiter exits, one waiter at a time, load1 below 7.
- Q-3 Is a gate that finds an extra under-44 link in a changed file allowed to fail the branch (Major) when the builder's frame lacked it? Default: yes, as written (a link in `parts.tsx`/`FirmwareTask.tsx`/`DocumentGeneration.tsx` or in the gate-named set).
- Q-4 PR title key: the kit allows `HPSMPOC-417` only (squash subject carries it); default as written, both tickets stay open.

## Test of every REFUSE and STOP line against what is live and installed now (00:09:59 unless noted)
1. Unstamped slots: `/usr/bin/grep -c -E '_''_''_''_'` on the kit = 8 (lines 52-58 and the last line); control scratch file with four underscores = 1. PASS (as designed: the seat refuses until Tuesday stamps). `@[A-Z_]+@` = 0, control = 1. Non-ASCII bytes in the kit 0, control = 1.
2. Pane rules: HPSM-POC panes other than G266/R121 = 0; `HPSM-POC-G267` panes = 0; H93 not live. `tmux display -p -t` control prints another pane's name (`tuesday`). PASS.
3. Head moved: ref read `954996c8...` = expected. PR for branch 0 (the "PR now exists" branch of the line is a no-stop). PASS.
4. Main moved: `compare d8981b0e...main` = 0 files; both controls fired (31 `web/` names; 1 `customer/` name). PASS.
5. Builder last line begins `READY FOR QA: B1059 ... @ 954996c8...` = 1 (control absent string 0); `## PRIOR WORK` = 1 (case-insensitive). PASS.
6. `.tools/b1072` and `.tools/wt-b1072-*` absent (rc non-zero each; control `.tools/b198` present); `refs/heads/b1072*` 0 (control `b1059` 1). PASS.
7. Ports 9200-9209: 0 listeners; control listener on 9206 for 7 s seen (2 lines) then 0. PASS.
8. `gh auth status` under the project config: logged in (1 line, login not printed). Node v24.21.0 satisfies `engines >=20.9`; `.tools/ms-playwright` lists chromium (2 lines). `models_latest.json` line 17 = `claude-opus-5-5`, JSON read agrees. PASS.
9. Shared `2_Project_Files` lacks `954996c8` and `d8981b0e` (cat-file fails for both; control `77c3132e` prints `commit`). PASS (the kit says fetch into an own clone).
NOT TESTED by me: the in-clone fetch and its deploy key, `npm ci`/`npm audit` against the registry, Playwright launch, whether a `launch_when_cool` waiter will exit, the Opus safeguard switch.

## UNMEASURED
No clone, build, browser, vitest or plant was run; no pixel rendered. Not measured: any link's rendered height, the pill overlap, the second under-44 link the gates counted at pack 3, the wrap behaviour of `inline-flex` links at 360, the underline on `inline-flex`, today's `npm audit` state, hosted CI, CodeQL, the product owner's answer on the label.

## Outside-the-fences disclosure
- Wrote only the two files. Scratch (session scratchpad): tarballs and extracts of main and head web trees (`gh api -X GET .../tarball/<sha>`, GitHub API not a hosted site), raw reads of `ci.yml`, `CLARIFICATIONS.md`, `playwright.config.ts`, `package.json`, `e2e.mjs`, the jira helper output (filtered; no comment authors read), a first-lines gate list.
- Ran the project Jira helper (`python3 -I -B .tools/b649/jira.py HPSMPOC-417 HPSMPOC-412`, GET only) and a 7-second loopback listener on 9206 as the port control. No fetch, clone, worktree, checkout or ref write; git in the shared repo only `cat-file`.
- Read the B1071 template, B1059 kit, B1059 STATUS and its evidence text/PNG hashes, B960/B964/B967 STATUS lines. Did not read the decision board or any card, `briefs_staged`, `scoreboard.md`, `_ledger.md`, or any WEDNESDAY/FRIDAY/non-Datasec tree.
- Slips: one Bash call began with a stray `cd` and was refused by the hook (no effect); one call used a bare `=====` word and was refused by the zsh hook (no effect). The shared scratchpad is also used by other drafters running now: my `ci.yml` copy there was overwritten by another drafter's file, noticed when line cites failed, and re-fetched under `scratchpad/b1072/ci-head.yml`; every number in the kit was taken from output at the time it was read, and the ci.yml line numbers were re-verified on the re-fetched file (one fixed: node 24 is at `ci.yml:384`, not 380).
