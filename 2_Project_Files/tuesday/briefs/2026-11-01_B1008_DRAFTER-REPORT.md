STARTABLE: YES (after Tuesday stamps; the lane is clear and the row is spelled out; nothing in it was executed by the drafter)

# B1008 drafter report (SEAT-H88, round 2 of 2 on class "UAT database keep-awake template")
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1008_SEAT-H88_hpsmpoc-keep-awake-round2-wiring-row.md` (shape copied from the B999 kit; slot count 9, control: the B999 `.pre-stamp` reads 9).

## BLUF
One forward commit on the existing branch: ONE new method in class `TimingB175` (four delay spellings plus a control) that kills the gate's survivor M11, and ONE comment line in `infra/env/uat.bicepparam` (1 removed, 1 added). No template, no parameter value, no removed test line. Plants in the kit: P0 control, M11a (`startswith("[parameters(")`), M11b (any str), M13 (`rule_env_params` returns nothing) for B1003-5. Sonnet, row C2.

## Facts re-measured (instrument; control)
- Branch head `930cb5b5d163d2d19d9da8890bccfe68c8ce07aa`, main `e0b939571ca969933ad80b6579da4948f5d59948` (`git ls-remote` with patterns `refs/heads/main`, `b999*`, `b1008*`, `b1003*`: only those two lines; control: the b999 line prints). Open PRs 0 (`gh api -X GET pulls?state=open`, `length`). Local checkout is stale (`cat-file -t e0b93957` fatal), so I read origin and `git show 930cb5b5:<path>` (the commit object is local; control `cat-file -t` = commit).
- Compare `d0eff4ca...e0b93957` lists 12 files, all `web/` (control: compare `e0b93957...930cb5b5` lists exactly the four infra paths and `non-infra` count 0). None is `infra/` or `ci.yml`. Branch vs main: diverged, 1 ahead, 2 behind. Kit says re-measure and STOP on any `infra/` or `ci.yml` path.
- Test file at `930cb5b5` is 2909 lines. Anchors, each counted with `/usr/bin/grep -c -F`: `    if value == AUTO_PAUSE_EXPRESSION:` 1, `            if value != w:` 1, `def test_never_pausing_database_needs_no_dispatcher` at line 2707 (method ends 2711), `import copy` line 10, `props` line 78, `templates` 731, `databases_with_template` 1043, `pause_delay` ~1050, rule message "not one literal number" line 1066. Gate-named lines 1057, 1062, 2542, 2550 confirmed (`def rule_demo_database_stays_awake` 1062, `class TimingB175` 2550, `test_mutation_uat_back_on_the_free_offer...` 2542).
- `uat.bicepparam` at `930cb5b5` is 33 lines; line 21 is the one that starts `// first click after a pause waited out a resume of about a minute.` and ends `so this` (line 22 continues `database cannot go back to it.`), so the replacement is one line for one line and the sentence still joins.
- `infra/scripts/validate.sh` exists at the branch head (blob d6fd1317); its pass predicate is the CI `infra` job's step "validate (build, lint, params dev/uat/demo, security baseline)": `run: bash infra/scripts/validate.sh`, `WHATIF: "0"`, Bicep `v0.47.16`; the kit writes "rc 0 and last line `== validate: OK`" (the gate's wording, from `.tools/b1003` logs it recorded; I did not open those).
- `.tools/bicep/bicep`, `.tools/b198/lock.sh` present; `.tools/b1008` absent (`ls | grep -c -i b1008` = 0; control: `b999` and `b1003` list). No kit of 2026-10-31 or 2026-11-01 names H88 or B1008 (`/usr/bin/grep -l -i -w`: H88 0, B1008 0; controls H87 3, B1002 4). tmux pane titles at drafting show no HPSM-POC pane. B1007 has no kit file in `briefs/` (not mine to chase).
- Model: routing row C2 at `fleet/specs/model-routing.md` line 92 (C3 line 93 does not apply); `models_latest.json` line 23 `claude-sonnet-5-5`. `brief_seat.sh` line 24 defaults to opus; the launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- uptime at drafting: load1 5.99 (not the launch read; the kit says load1 below 7 on two reads).
- Ports: the kit uses none. `lsof -nP -iTCP -sTCP:LISTEN | wc -l` read 15 listeners; no port block was assigned, none needed (tests and bicep open no port), so no word-boundary scan applies.

## D-decisions
- D-1: the row is ONE method with four subtests and a control, not two methods. Test count expected 320 -> 321. Why: the gate asked for "one row"; the subtests name each spelling. Under plant M11a only two of the four subtests go red (the `if()` text and the text `60` are not `[parameters(` text); the kit says so up front so the builder does not "fix" it. M11b (any str) turns all four red.
- D-2: the row mutates through `databases_with_template(t)` (all databases in all nested templates), not `of_type`, because `pause_delay` reads through the same walker.
- D-3: the comment fix replaces line 21 only, with measured words "met a resume of 30 or 60 seconds (measured) and the web gave up at its 10-second limit, so it showed an error". The builder re-reads B991 and writes what it says if different.
- D-4: new commit message is specified and kept to measured claims about the new commit only; nothing about the first commit. The squash text at landing is Tuesday's.
- D-5: B1003-5 is a plant (M13: `if value != w:` -> `if False:`), expected: the line-2542 row RED, the approved-values row GREEN. A GREEN 2542 row under M13 is a STOP, not a fix.
- D-6: seat-local `heavy.lock` under `.tools/b1008/`; the shared `.tools/.git-lock` (via a `cmp`-checked copy of b198 `lock.sh`) wraps the push only. Worktrees are detached (no local ref). Target READY 45 min, hard stop 75 (suggested in the slot; Tuesday fills).
- D-7: the cost sentence of the commit (B1003-4) is not repeated by the new commit; the STATUS summary quotes the gate's figures and says not re-measured.

## Q-questions for Tuesday (each with a default)
- Q-1: The B999 kit's launch line is not in the kit text; I used the `cockpit.sh add` form (rules file) and offered `launch_when_cool.sh` as the alternative. Default: use `cockpit.sh add` as written.
- Q-2: Target/hard stop 45/75 min instead of B999's 60/100 (smaller change). Default: as suggested; you stamp.
- Q-3: Gate tier for the round-2 gate (the kit says "round-2 gate" only). Default: tier 2, same as round 1, same model row as B1003; the deploy remains a separate tier-1 act.

## UNMEASURED
- Nobody has run the new method. I did not invoke bicep or python on the repo (rules: no probing tools). The claim "green on the shipped code" is RELAYED from the gate's 10-case probe (`c3_probe_non_literal_delay.txt`: the shipped reader reports `[parameters('other')]`, `[if(true(), 60, -1)]`, a case-changed and a spaced spelling, text `60`); I read the code path in `pause_delay` and the rule and agree by reading (non-int single delay -> "not one literal number"). The kit makes the builder prove it.
- The M11a/M11b/M13 red/green expectations are by reading, not by running.
- Compiled byte-equality: expected (a `.bicepparam` comment is not compiled), unmeasured by me.
- shellcheck not installed locally (gate said so): NOT TESTED; the diff has no `.sh`.
- Whether the web's 10 s limit and the 30/60 s resumes read exactly as the gate says: RELAYED; the kit tells the builder to re-read B991.

## Outside-the-fences disclosure
Read only: the three files named in the commission, the model-routing and models_latest files, the B1003/B1002/B1006/B999 kits and reports for launch-line shape and the B-number scan, `launch_when_cool.sh` header, `cockpit.sh` header, `brief_seat.sh` grep, the project `.tools/b198/lock.sh` and `.tools/b999/lock.sh` (identical by reading), `git show 930cb5b5:` of the test file, `uat.bicepparam`, `ci.yml` (lines 570-630) and `validate.sh` (lines 1-25) and `git log`/`show --stat` of the first commit, a project directory listing of `.tools/`, `tmux list-panes -a`, `lsof` (count only), `uptime`. `gh` `-X GET` only (compare x3, pulls, under the project's `GH_CONFIG_DIR`); one compare printed a large JSON by my own jq slip (no secrets in it; the persisted output file sits in the session's tool-results folder, not in the project). A scratch copy of the test file is in the session scratchpad. No fetch, no worktree, no ref write, no card read, no `decision_queue.sh`, no HP-NDA path opened, no az/ssh/docker, no `cd` typed (an advisory hook noted three case-sensitive greps; each hit count was 1 and positive, so no false zero). The commission named the decision-card-free reading: no card id appears in the kit.
