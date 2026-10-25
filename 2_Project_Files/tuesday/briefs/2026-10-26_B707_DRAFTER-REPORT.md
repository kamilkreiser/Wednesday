STARTABLE: YES (after Tuesday stamps the eight slots; nothing blocks the launch at 07:38 AEDT)

# B707 drafter report (kit: `2026-10-26_B707_SEAT-G133_composer-94-round2-gate-tier2.md`, 82 lines)

## BLUF
Round-2 tier-2 gate (row G2, Sonnet) of Composer PR #94 at head `99585f7d`, cloned in shape from the round-1 gate kit B699. Seat `Datasec/Security-Composer-G133`, ports 9740-9749, B-number B707, findings `B707-n`. Kit carries the cap sentence (G-cap `model-routing.md:111`: same-class NO GO ships the closed instances, residue ticketed with cells, no round 3), the three rulings verbatim, a counterfactual procedure so the gate (not the builder) decides what is "of ruling (b)", and the no-loosening check by program.

## Facts re-measured (instrument, time AEDT)
- `ls-remote` 07:34: main `0b52848c`; branch = `refs/pull/94/head` = `99585f7d125adeda6b082fb297639bd625ba0ac4`; merge ref `2321ad46`. Control: the head sha matches the builder STATUS and `pulls/94` independently.
- `git/commits` GET: merge ref parents = main `0b52848c` + head; merge tree `799640ab`; head parent `0307e31a`; head tree `b1050c8d`. `pulls/94`: open, not draft, 2 commits, 1 file, +384 -20, mergeable true, clean.
- `compare 0b52848c...head`: ahead 2, behind 1. So the clone's `rev-list --left-right --count origin/main...origin/pr94` must read `1 2`, not `0 N` as round 1 did (main moved by PR #93). Written into the kit.
- check-runs at the head 07:34: 3 of 3 `completed success` (CodeQL, both Analyze). Analyses of the head: 2 (results_count 0, error empty), beside 2 for `0307e31a` (control: the older head's rows are listed, so the filter returns rows). Open alerts on the PR ref: 0 (state `open` only; the kit tells the gate to read all states on three refs). The builder's "CodeQL running" is stale.
- Head file via `git show`, `/usr/bin/grep -c -F`: `heredocWord` 2, `heredocBodyEnd` 2, `OPENING_FENCE_LINE` 2, `toLowerCase` 1, `HEREDOC_WORD` 0, nonsense control 0. 786 lines; 39 literal `it(` (control `^describe` 1). Blobs `DEPLOY.md` f70ce89d, `support.ts` 13eb5f3e at the head. `git diff --numstat 0307e31a 99585f7d` = `178 8`.
- Commit message trailer count 1.
- Ports: `lsof -nP -iTCP:9740-9749 -sTCP:LISTEN` rc 1. Word-boundary scan of `2026-10-2[56]_*SEAT*.md` hit 8 kits (B623 B624 B627 B631 B641 B649 B679 B681), all finished seats, none a live pane; B700-B706 do not name the block. `G133` appears in no kit.
- Panes 07:34: tuesday, NexusAI-G132, NexusAI-M13, Security-Composer-J18 (builder, live), MPS-G131, fleet-monitor. No `.tools/b707` (control: `.tools/b705` exists).
- Model: row G2 at `model-routing.md:109`, G-cap `:111`; `levels.sonnet.model_id` = `claude-sonnet-5-5`. `gh auth status` Datasec-login count 1. Repo allows squash/merge/rebase (all true).
- Load 3.67/4.96/4.73 at 07:34; 2.99/4.44/4.55 at 07:36.
- Kit hygiene: four-underscore lines 9 (eight slots + last line), `@[A-Z_]+@` 0, non-ASCII bytes 0, person-name grep (three first-name/seat words) 0.

## Discrepancies found in the builder STATUS (put in the kit as things the gate must settle)
1. Removed lines: STATUS says 7; numstat says 8. Kit makes the gate read all removed lines and reconcile.
2. The extra open-backtick branch has no red-at-head proof ("red by construction"). Kit asks for a swap proof and a property mutant per branch.
3. `G1404`, `G1772`, `M0` (the `;#` family) are called ruling-(b) class with NO counterfactual. Kit: counterfactual is the gate's job; unsettled becomes RULING-BOUNDARY (a Note listed for Tuesday), not silent.
4. Whole-repo lint/format/typecheck not run by the builder; gitleaks only on the staged change. Both added to C4/C6.
5. Builder predicted 9 new rows and got 10; kit asks which row.

## D-decisions
- D1: Round 2 of 2 on PR #94's own record, per the B695/B705 stamps; G-cap sentence written so the gate knows the outcome shape.
- D2: Reuse of the round-1 gate's harness AND corpus generators (`mkcorpus*.py`) allowed, mutant drivers not; the builder's tree, corpus, seed-705 fuzz, mutants and pty tables are READ-FORBIDDEN (only its STATUS and commission are read).
- D3: Fresh fuzz seed chosen by the gate at Step 0 (not 699, not 705), recorded before the run.
- D4: Hard stop suggested 2.5 h target / 4 h hard (longer than round 1's 2/3 h, because the pty re-run is 142 shapes + fuzz + group run). Container budget raised to about 40 (round 1 used 27).
- D5: A usage-pause line added (the B705 seat lost a session to the weekly limit).

## Q-questions for Tuesday (each with a default)
- Q-1 Ports 9740-9749: eight finished seats' kits name them, nothing listens. Default: accept.
- Q-2 Plumbing from `.tools/b626/scripts/` as round 1. Default: no answer reads NO (gate writes its own route).
- Q-3 Round count "2 of 2 on PR #94's own record" with the cap sentence. Default: accept.
- Q-4 Scratch mutants/corpus in `-mut` and `-probe` only. Default: NO (C3 NOT TESTED).
- Q-5 Reuse list includes the corpus generators. Default: accept.
- Q-6 The builder pane J18 may still be open and shares the docker daemon; `heavy.sh` will wait on its `pc-b705` lines. Default: launch anyway.

## UNMEASURED
No build, test, container, pty, corpus, mutant or fuzz run. Not measured: that the J18 pane is idle; that the CLARIFICATIONS lines 582/855/1799/1802/1823 say what B699/B705 quote (only that lines 1799, 1802, 1823 begin with the PR #88/#87 landing text; quotation RELAYED); the squash commit's tree; the head's `it` count at runtime (41 is the builder's); that `.tools/b626/scripts` run unchanged under rename.

## Outside-the-fences disclosure
Read-only reads only, outside my two files: the DRAFTER_RULES, the B699 gate kit and STATUS, the B705 kit, STATUS and addendum (a Tuesday briefs file), the B706 kit (grep for weekly-limit lines only), the B699 evidence directory listings (`ls` only, no file content), `.tools/` listings, `scripts/ci.sh` and `vitest.config.ts` grep lines, CLARIFICATIONS lines 582/855/1799/1802/1823 (first 160 characters), `pulls`/`check-runs`/`code-scanning`/`git/commits`/`compare` by `gh api -X GET` under the Composer `GH_CONFIG_DIR`, `ls-remote`, `git show`/`diff`/`rev-parse`/`cat-file` (the head file was written to the session scratchpad as `head.ts` for counting; nothing in the project). One Bash call was refused by a hook (a separator starting with `=`); re-run without it. No `cd`, no Artifact/Docs/mail/chat tool, no HTTP to a hosted host, no `decision_queue.sh`, no ledger/scoreboard/briefs_staged/Wednesday/Friday trees.
