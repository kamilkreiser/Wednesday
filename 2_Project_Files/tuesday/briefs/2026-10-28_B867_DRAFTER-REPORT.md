STARTABLE: YES

# B867 DRAFTER REPORT (kit for SEAT-G190, tier-2 gate of HPSM-POC PR #237)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B867_SEAT-G190_hpsmpoc-237-module-binding-rule-gate-tier2.md`
Drafted Wed 28 Oct 2026 04:0x-04:2x AEDT, read-only. Instruments: `gh api -X GET` under the project GH_CONFIG_DIR, `git --no-optional-locks ls-remote`, `/usr/sbin/lsof`, `tmux list-panes`, python `-I` scans, `/usr/bin/grep`.

## BLUF
Kit written in the B833/B805 shape (65,520 bytes). Stamp-slot count 8 lines (7 slots + last line), `@X@` count 0, non-ASCII 0, no person name, no card id (checked by grep). Everything relayed was re-measured and agrees. One adjustment to the relay: ports. 9890-9899 is NOT free (another repository's live gate B866 names 9890 and 9899), so the kit says "no port needed; if any, 9900-9909".

## Facts re-measured (instrument; control where one fired)
- PR #237: open, draft false, mergeable_state blocked, head `e950a5b2...`, base `df1dc0fe...`, commits 1, changed_files 1, +128 -1 (`pulls/237`, `pulls/237/files --paginate`). compare df1dc0fe...e950a5b2: ahead 1, behind 0, merge base df1dc0fe.
- ls-remote: main `df1dc0fe`; b858 branch and `refs/pull/237/head` = `e950a5b2`; `refs/pull/237/merge` `a03e46a7`; also b859 `0c85ed9b`, b860 `3dba3567` (live builder, pushed 04:03). No `b867*` ref.
- Test file by raw read at each ref: base 2117 lines, 29 top-level `def rule_`, 99 `    def test_`; head 2244 lines, 107 `    def test_`; `appservice_calls` at 1060, `rule_appservice_module_bindings` at 1067, `RULES = [` at 1088, new rows 1411-1460. (Case-sensitive greps; hook advised -i; the counts agree with the builder's 99/107/29, which is the positive control.)
- CI predicate: `ci.yml` at df1dc0fe: job `infra (Bicep validate)` line 575-576, Bicep v0.47.16 pinned lines 581-582, step `validate (build, lint, params dev/uat/demo, security baseline)` line 623, `run: bash infra/scripts/validate.sh` line 627; `validate.sh` line 21 `BICEP="$BICEP" python3 tests/test_security_baseline.py` after `cd` to `infra/`. The relayed "python3 tests/test_security_baseline.py from infra/" is correct, with the BICEP env var added.
- Checks on the head at 04:03: 13 check-runs; CodeQL queued; secrets and dependency review success; 10 others in progress (incl. four Analyze). Required contexts 5 (api, web (Next.js), infra, secrets, dependency review). Ruleset types: deletion, non_fast_forward, code_scanning, required_status_checks.
- Repo squash settings: `COMMIT_OR_PR_TITLE`, `COMMIT_MESSAGES`, allow_squash true. Landing precedent: `CLARIFICATIONS.md:138` only (PR #27 squash head-pinned); project CLAUDE.md has no hit. Kit quotes both and states the explicit subject/body requirement.
- Overlap: open PRs #237, #236. #236 paths (4): UatOpenAuthentication.cs, infra/README.md, infra/env/uat.bicepparam, web/src/server/auth/config.ts: shared with #237 = 0. b860 compare: ahead 1 behind 0, paths `web/e2e/logon-chooser-corners.spec.ts`, `web/playwright.config.ts`, `web/src/components/shell/HpLogo.test.tsx`: shared 0. **Read-through (new, Note):** the test compiles `infra/env/*.bicepparam`, and #236 changes `infra/env/uat.bicepparam`; the kit makes the gate measure whether that can change #237's counts and makes a main move on `infra/env` a REFUSE/STOP.
- Round history: first-lines loop over B-STATUS files printed B831 (#234 GO WITH FINDINGS, round 1 of 2, class "the template's open sign-in switch and key references"; found this gap as B831-1), B805 (#233 NO GO r1) and B817 (#233 GO WITH FINDINGS r2, the cap; different class). Controls B805 and B817 printed. No NO GO on this class: "NO GO 0 of 2, round 1 of 2".
- Model: routing row G2 at `model-routing.md:109` (G-cap :111) by grep; `claude-sonnet-5-5` at `models_latest.json` line 23; `brief_seat.sh:24` defaults to opus; launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.
- Ports: `lsof -nP -iTCP:9890-9909 -sTCP:LISTEN` empty (rc 1). Word-boundary scan (python -I, control `x 9890 y` true / `a9890` false) over 101 non-`.pre-` SEAT kits of 10-27 and 10-28: one hit, B866 (MPS gate, 9890 and 9899). 9900-9909 clean. Live panes: tuesday, HPSM-POC-G186, NexusAI-M52, HPSM-POC-H50, NexusAI-M50, fleet-monitor. `Datasec/HPSM-POC-G190` count 0.
- `.tools/b867` absent (`ls -d` error; control `.tools/b198` lists); `refs/heads/b867*` 0 lines; helpers `.tools/b198/lock.sh`, `.tools/b267/waitload.sh` exist.
- Builder STATUS read whole: last line begins `READY FOR QA: B858 ... @ e950a5b2...`; has PRIOR WORK. PR body read whole: no "checks pending" sentence; it says "Nine mutants" (builder STATUS also says 9) and "20 repeats" (relayed, not reproduced).

## D-decisions
- D1: gate plants are applied to a deep copy of the compiled template (in memory) AND, for at least two plants, as real edits of `infra/main.bicep` in a scratch mutant tree recompiled by the pinned local Bicep, so they pass through the suite's own compile. The base list's 23 rules are run on each plant as the "gap is real" control, and a stub `return []` control checks the 8 rows.
- D2: the builder's disclosed limits (rbac/keyvault call bindings, other appservice bindings, substring chain) are planted as g1-g4 and graded Notes with ticket text, never Blockers.
- D3: the gate checks `localdomain` count in the head commit's author/committer email fields and message (relayed landing check "0 localdomain after"), reports only the count.
- D4: the builder's slip (its own stray `__pycache__` failed a hygiene row) is turned into a gate rule: PYTHONDONTWRITEBYTECODE=1, 0 `__pycache__` proof, `arm_*` temp dirs counted and moved.
- D5: no Jira call in the gate (kit scope); the ticket key is only read from the PR text and used in the recommended squash message.
- D6: hard stop 135 min, target 75 (no npm/node/browser, so shorter than B833), plus CodeQL wait up to 40 min.

## Q-questions for Tuesday (each with a default)
- Q-1: Does B831's class count toward this one? Default: no (different class; B831 was GO WITH FINDINGS, not a NO GO). Round 1 of 2.
- Q-2: Order of landing against #236, given #236 changes `infra/env/uat.bicepparam`, which the infra test compiles? Default: path-disjoint, land whichever gate finishes first; the kit STOPs the gate only if main moves on `infra/env/**` mid-gate (then re-pin). If you prefer to land #236 first, say so in S3.
- Q-3: Keep the optional end-to-end `bash infra/scripts/validate.sh` run in the gate? Default: yes if cheap, else NOT RUN stated.
- Q-4: Should `rule_appservice_module_bindings` be in `SHOWCASE_RULES`? Default: Note only (the gate greps `showcase-ai.bicep` for an appservice call to decide).
- Q-5: The commit message carries no ticket key by the builder brief; the squash text carries HPSMPOC-358 and the gate's measured counts. Default: Tuesday words it after the verdict.

## UNMEASURED
Nothing was compiled, run or cloned by me; the head's 285/285 and 3.9 figures, the 20-repeat loops, the nine rule mutants, the hosted check results and CodeQL are the builder's or not yet available. Whether `showcase-ai.bicep` has an appservice call. Whether any importer reads the order or length of `RULES`. The CI runner's Python version. The content of the 8 new test rows beyond the titles seen at lines 1411-1460 (the full body was not read; the gate reads them).

## Outside-the-fences disclosure
Nothing outside the fences. Reads: DRAFTER_RULES, the B833 and B805 kits, the builder STATUS (B858), the B860 STATUS first lines and the Briefs directory name list, B831/other STATUS first lines, `model-routing.md`, `models_latest.json`, `brief_seat.sh` header lines, `CLARIFICATIONS.md` and project `CLAUDE.md` by grep, `gh api -X GET` reads (PR, files, compare, check-runs, branch protection, rules, repo settings, raw ci.yml, validate.sh, the test file at two refs, into the session scratchpad). My first multi-command Bash call was refused whole by a hook (unquoted `$G` variable with spaces) so nothing in it ran; I re-issued without it. Two later commands used a stray `cd_none=1` / `cd_unused=1` variable assignment (no `cd` was typed). Only the two output files were written to the project tree; scratch copies (`ci.yml`, `head.py`, `base.py`) are in the session scratchpad. No Jira, no card store, no mail, no launch, no tmux write.
