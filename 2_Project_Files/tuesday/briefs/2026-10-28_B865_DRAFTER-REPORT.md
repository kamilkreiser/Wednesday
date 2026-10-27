STARTABLE: YES (with conditions Q-1 and Q-3 below: the jest lock queue and high load will make this gate slow, not blocked)

# B865 drafter report (Sonnet 5.5 drafter, 2026-10-28 03:59 to about 04:20 AEDT)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B865_SEAT-G188_nexusai-134-rd894-probe-cells-gate-tier2.md` (116 lines).

## BLUF
Tier-2 gate kit for PR #134 (RD-894 probe cells), head `44f6f5eb...`, round 1 of 2, seat `Datasec/NexusAI-G188`, ports 9860-9869, Sonnet. Shape copied from B853. The class is tests-only cells pinned by named mutants of a backend file, so the template's red-at-main table (14 red, 7 green) is replaced by a green-at-base table plus a product-mutant matrix (GM1-GM11) and three tamper controls on the test file (GT1-GT3). Every fact below was re-measured by me; nothing was run, cloned, fetched or written in the project. All four Stamp slots-plus-last-line markers are four underscores (grep count 8, control: the template's own convention is 8).

## Facts re-measured (instrument, control)
- ls-remote (project repo, read verb): main `f4ea31c9`, `b855/...` = `refs/pull/134/head` = `44f6f5eb`, `refs/pull/134/merge` = `5cc31e8c`; `b856*`, `b862*`, `b865*` absent (control: `b855*` and `b816*` print). I mistakenly listed `refs/pull/*` whole once (read only, large output); the kit tells the gate NOT to.
- `gh api -X GET pulls/134`: open, non-draft, mergeable true, `mergeable_state` unstable (build running), 1 commit, 2 files, +184 -2, base `f4ea31c9`. `pulls/134/files`: test file 182/0 blob `0e54575e`, counts 2/2 blob `38c0ae66`. Open PRs: #134 only. compare main...head: ahead 1 behind 0, merge-base = main.
- Merge ref commit: parents (`f4ea31c9`, `44f6f5eb`), tree `c62c27c6...`, date 2026-10-27T16:55:08Z.
- Counts blobs: main `d3c0021b` 5220/310; head `38c0ae66` 5223/310, `_why` text identical, `_updated` moved.
- Test file by raw content at main and head (saved to scratchpad): 409 and 591 lines, `diff` shows 0 removed lines; new `describe` at 415, tests G 418, H 494, I 551 (I read the 177-line block whole). Note: a `--jq .content|@base64d` copy hashes to `356ed6e3` at main, not `9fd243ee` (trailing newline from jq); I used the API `files` blob shas in the kit and flagged the trap. Control: the head copy's recomputed blob was not equal to `0e54575e` for the same reason; the `files` blob is authoritative.
- `backend/jsonStorage.js` at main: re-hashed on a saved copy = `bba3742b` (matches), lines 400-419 read: probe at 402-418, catch at 415, close in inner finally. Mutant anchors in the kit rely on those lines.
- CI: check-runs on head (8): CodeQL, three Analyze runs, scan, audit-production-deps success, `build` in_progress at 03:59. `actions/runs?head_sha`: 5 runs, Build in progress, no Deploy demo. `code-scanning/analyses?ref=refs/pull/134/head`: javascript-typescript, python, actions at `44f6f5eb`, results_count 0 (control: main lists 123, 1, 0). Open alerts on PR ref: 0 (control: `alerts/9999` 404). The gate must wait for `build`.
- Verify predicate: `verify-suite.sh` blob `eb9731f5` lines 91-92 (both directions fail) and 366 (VERDICT PASS); `build.yml` blob `e4e5c095` lines 83-84, node 24 at 29 (greps of a saved copy, each line printed).
- Landing hold, measured today: `deploy-demo.yml` paths-ignore is only `**.md`, `docs/**`, `tests/**` (so `__tests__` pushes start it); both job `if`s need `vars.CI_DEPLOY_ENABLED == 'true'`; the four most recent main push runs (`7d21711d`, `f61de45f`, `0de3eb2f`, `c8e1a9a1`) read completed/skipped; the latest (`7d21711d`, the #132 landing) has jobs `deploy` and `build` both skipped with 0 steps (control: a nonsense workflow name 404s). `CLARIFICATIONS.md` lines 665, 2067, 2073, 1354, 2412 found by text.
- Model: `model-routing.md` G1 line 108, G2 line 109, G-cap line 111 (found by pattern, printed); `models_latest.json` line 23 `claude-sonnet-5-5`; `brief_seat.sh` line 24 defaults to opus (read by `sed -n 22,26p`).
- Round count: frame `grep -l -i -E '44f6f5e|#134|b855|RD-894'` over `*_STATUS.md` hits B846, B854 (records), B855 (builder), B856 (partner); no `GATE VERDICT` line names #134. NO GO census (`^GATE VERDICT .*NO GO`, control: a scratch line reads 1) hits B592, B647, B667, older gates of other classes. Earlier same-neighbourhood verdict lines read: B827 GO WITH FOLLOW-UPS round 1 of 2, B853 GO WITH FOLLOW-UPS round 1 of 2, B838 GO WITH FOLLOW-UPS round 1 of 2. So 0 of 2 before; this is round 1 of 2.
- Ports: `lsof -nP -iTCP:9860-9869 -sTCP:LISTEN` rc 1 (I did not bind a control; the kit makes the gate do it). Word-boundary scan (python3 -I, 98 non-`.pre-` SEAT kits dated 10-27 and 10-28) hit exactly two kits: B855 (the closed builder that owned the block) and B862 (live, names 9860-9869 only as partner blocks to avoid; its own is 9840-9849; the 984x control hits B862). `grep -l NexusAI-G188` over the same kits: none (rc 1). Live panes: tuesday, fleet-monitor, `NexusAI-M50`, `NexusAI-M52`, three HPSM-POC panes.
- Plumbing sha256: lock tool `cf01bafb...` and fence `55eaafcb...` equal to the template's. `session-tools/b865` and `worktrees/b865-*` absent (`ls` error; control: `session-tools/b855` exists).
- Sequencing: B856 STATUS last line (verify queued on the jest lock at a LOCAL head, nothing on origin) and B862 STATUS (baseline queued behind another seat's verify); path mentions in their briefs: B856 names only `rd892-testing-dropdown-null-level.test.js` as its edit path, B862 names only `rd407-concurrent-settings-writers.test.js` and says "no counts regeneration" at Step 5. Both are claims read from live seats' STATUS and briefs; the kit says so.
- Load1 at 03:59: 7.08 / 8.70 / 11.30.

## D-decisions
- **D-1 class and tier.** Tests-only PR: G2, Sonnet, no product byte. The hand-up rule is stated but can only arise if the gate finds a product-path issue; the one new write sink (cell H's planted file) is a test-side constant write graded in C3/C7.
- **D-2 no red-at-main table.** The builder proved the cells are green at main by design (the product is correct). The gate's proof is: green at base and gate (x2, x3), red under named mutants, red under tamper controls on their own instruments. The BASE tree needs the head's test file over main's product, which is stated as an untracked single-path change with blob proof.
- **D-3 mutants.** GM1-GM4 mirror the builder's MU1/2/4/6 (cells named), GM5 is a partial swallow of one looped code (G must go red), GM6 swallows a code outside the loop (expected all green, a Note: builder FINDINGS 6), GM7-GM9 mirror MU3/7/8, GM10 and GM11 are the known gaps (mode, write step) as Notes. GT1-GT3 are the tamper controls, my addition, because a precondition that cannot fail is the thing the class is about.
- **D-4 old cells byte-equal check** is by program from the two hunk headers (cut the hunks, compare to main's file), stronger than "0 removed lines".
- **D-5 counts**: main plus exactly 3 tests and 0 suites (11 minus 8), counts diff only `tests` and `_updated`.
- **D-6 launch line** follows DRAFTER_RULES line 60 (`WED_USAGE_STOP=100 bash .../cockpit.sh add ... "BRIEF_SEAT_LEVEL=sonnet bash '.../brief_seat.sh' ..."`), not the B853 template's `launch_when_cool.sh` form. I verified both scripts exist. The Stamp guidance mentions launch_when_cool as the window; Tuesday may swap the form (see Q-3).
- **D-7 landing** is quoted from C-190 `:2067` and C-68 `:665`, with the exact `gh pr merge 134 ... --match-head-commit 44f6f5eb...` command, and the post-merge Deploy demo reading rule (both jobs skipped, nothing waiting in `demo`, else STOP) with today's measured precedent.

## Q-questions for Tuesday (each with a default)
- **Q-1 hard stop and queue.** Other seats' verifies hold the jest lock (about 30 minutes each) and B856 and B862 are queued ahead of or beside you. Default: target verdict 150 min, HARD STOP 240 min after the gate's Step-0 date (the template's 120/180 is too short here). Change if you want the gate not to queue behind them.
- **Q-2 round-count class wording.** The class is "test-only cells pinned by named mutants of a backend file". Default: 0 of 2 before, round 1 of 2 (no NO GO on this PR or class).
- **Q-3 launch form.** Default: the kit carries the rules-file `cockpit.sh add` form. If you prefer the B853 `launch_when_cool.sh` form (recommended given load1 above 7), substitute it, keeping `BRIEF_SEAT_LEVEL=sonnet WED_USAGE_STOP=100` inside the quotes.
- **Q-4 GM6 and GM11 as Notes.** Default: Notes, not Majors (the ticket names EACCES; the builder already recorded both gaps).
- **Q-5 ports.** Default: 9860-9869 accepted; the B862 hit is a not-yours mention, not a claim.
- **Q-6 build wait.** The PR's `build` was still running at 03:59; the gate waits for it (C3), as B853 did.

## UNMEASURED
Whether `build` finishes green and `mergeable_state` reaches `clean`; any CodeQL alert beyond the three analysis rows read; the contents of B856's and B862's final heads and whether either later touches the counts file; the node-24/Linux behaviour of the cells; whether the neighbour list is 17 suites (builder claim only); the lock queue length at launch; a bound-and-freed control for the 9860-9869 `lsof` zero (left to the gate's REFUSE 3).

## Outside-the-fences disclosure
- I read the live seats' B856 and B862 STATUS files (head, last line, a few grep lines) and their briefs by grep for path names; the template and rules treat live seats' STATUS as claims, and I only used them for sequencing. No tree of any seat was opened.
- One `ls-remote` with `refs/pull/*` printed every PR head (read-only, noisy); no ref write, no fetch.
- The `gh api` call to `code-scanning/alerts/9999` printed a hint about a missing `admin:repo_hook` scope on stderr (read-only; control behaved as 404).
- All scratch copies (`t_head.js`, `t_main.js`, `js_main.js`, `vs.sh`, `build.yml`, `dd.yml`, `ctl.txt`) live in the session scratchpad. No decision-queue tool, no Jira call (the Jira facts are the builder's relayed reading; the kit tells the gate to GET RD-894 itself), no Artifact/Docs/mail tool, no `cd`. Only the two output files were written outside the scratchpad.
