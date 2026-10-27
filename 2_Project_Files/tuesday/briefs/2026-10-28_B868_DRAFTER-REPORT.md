STARTABLE: YES (after Tuesday stamps the 8 slots; load1 read 8.45 at 04:04, so launch only through launch_when_cool)

# B868 drafter report (gate kit for HPSM-POC PR #238, seat G191, tier 2 round 1 of 2)

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-28_B868_SEAT-G191_hpsmpoc-238-chooser-logo-tile-pins-gate-tier2.md`. Drafted 28 Oct 2026 about 04:04-04:30 AEDT, read-only, shape of B833.

## BLUF
Kit written in the B833 shape. Everything relayed re-measured and agreed: PR #238 open, head 3dba3567, base df1dc0fe, 1 commit, 3 paths (+132/+13/+84-4 = +229 -4), no overlap with #236 or #237. Ports 9880-9889 free. Stamp slots left as four underscores (8 lines, count read 8). Two things the relay did not state and the kit now carries: the CI e2e job predicate (`ci.yml:483-515`, the third `webServer` entry starts in ALL five shard jobs) and `strict: false` on the main protection (either PR can land first).

## Facts re-measured (instrument, control)
- `gh api -X GET pulls/238` (+ `/files --paginate`): state open, draft false, `mergeable_state` blocked, head/base as relayed, 1 commit, 3 files, 229/4. Control: files list matches the relayed numstat 132/13/84+4 exactly.
- `git --no-optional-locks ls-remote origin`: main `df1dc0fe...` (not moved), branch and `refs/pull/238/head` `3dba3567...`, `refs/pull/238/merge` `b1272db5...`.
- Open PRs: #236 (4 paths: UatOpenAuthentication.cs, infra/README.md, infra/env/uat.bicepparam, web/src/server/auth/config.ts), #237 (infra/tests/test_security_baseline.py), #238. Path overlap with #238: 0 and 0, by eye on three short lists (the kit orders the gate to run the `grep -c -x -F` program with controls). #236's only web hunk (`config.ts` line 88) rewords one `off(...)` message string, so it cannot change what the chooser server does; #238's config change touches neither #236's nor #237's paths.
- Check-runs on the head at 04:04: 13 listed, CodeQL neutral, 4 `Analyze` in progress, dependency review and gitleaks success, `web (Next.js)` and e2e shards not yet listed; one code-scanning analysis row (actions, 0 results). CodeQL NOT complete: Check 8 waits.
- CI: `ci.yml` at the head, `web-e2e` at lines 483-515 (needs web-build, 5-shard matrix, 20 min, `node scripts/e2e.mjs --shard "$SHARD"`), `web (Next.js)` aggregation predicate at 526-545 (quoted in the kit). Config: `retries: CI?1:0`. Verified by reading the head's `playwright.config.ts` whole: the new entry sits in the `LIVE || TIMED_ONLY ? [] : [...]` list, `reuseExistingServer: false`, port `E2E_CHOOSER_PORT` default 3599, keys `randomBytes(48)` per run.
- Landing rule: project `CLAUDE.md`, 0 hits for squash/match-head/landing; `CLARIFICATIONS.md` one hit, line 138 (PR #27 head-pinned squash; a precedent, not a written rule). Repo settings: `squash_merge_commit_title=COMMIT_OR_PR_TITLE`, `squash_merge_commit_message=COMMIT_MESSAGES`, `allow_squash_merge=true`. Main protection `strict=false`; required contexts the same five as for #235; ruleset types deletion, non_fast_forward, code_scanning, required_status_checks.
- Round count: first-lines loop over `Briefs/*_STATUS.md`: 443 files, 88 `GATE VERDICT` first lines. Chooser-logo history: B833 (#235, GO WITH FINDINGS, round 1 of 2, class "the role-selection page's logo: a supplied image asset and its markup and pins, web only"), B730/B738 (#224), B760 (other PR, NO GO), B784 (#231, GWF). No NO GO on PR #238 or on a test-pins class. Control for the loop: it prints B730, B760, B784, B831, B833 (all present); I did not separately print B805/B817.
- Ports: `lsof -nP -iTCP:9880-9889 -sTCP:LISTEN` rc 1 (no listener; I did not run a bind control, the kit orders it). Word-boundary scan over 101 non-`.pre-` SEAT kits of 10-27 and 10-28: hits B776 (G161, NexusAI, finished, pane not listed) and B860 (the closed builder of this PR). Controls: `x 9880 y` 1, `a9880` 0. Live panes at 04:04: tuesday, HPSM-POC-G186, NexusAI-M52, NexusAI-M50, fleet-monitor (G191 count 0; H50 gone).
- Model: routing row G2 `model-routing.md:109`, G-cap `:111` (grep -n); `models_latest.json` line 23 `claude-sonnet-5-5`; `brief_seat.sh` line 24 `LEVEL="${BRIEF_SEAT_LEVEL:-opus}"`. Launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes, `WED_USAGE_STOP=100`.
- `.tools/b868` absent (`ls -d` rc 1; `.tools/b860` lists).
- Kit file checks: four-underscore line count 8 (slots S1-S7 plus the last line), `@X@` count 0, non-ASCII 0.

## D-decisions (mine)
- D-1: Class stated as "the role-selection page's logo: test pins and one browser spec for the white tile coming back, web tests and Playwright config only, no product byte". Round "1 of 2" with NO GO 0.
- D-2: Plants are named p1-p8 (the gate's OWN), not the builder's m7-m10, and the kit orders the gate to write them from the ticket shapes. The "one the builder did not try" is p5 `ring-8 ring-white` (a box-shadow ring outside the box; neither `PAINT`, `ARBITRARY_PAINT` nor the inline-style regex names it, so the unit arm should be GREEN and the spec's 14 px band RED), with p6 inline `boxShadow` and p7 `border-8 border-white` if time. Layered-design outcome (unit green, spec red) graded a Note; both green a Major.
- D-3: Browser plants need a rebuild each (the spec runs against `.next`); required for p1, p2, p5 only, unit plants for all. Hard stop 180 min (target 120) versus B833's 150/90, for the rebuilds and the high load.
- D-4: Port overrides: 9880 `WEB_PORT`, 9881 `E2E_STUB_PORT`, 9882 `E2E_HOSTED_PORT`, 9883 `E2E_CHOOSER_PORT`, always together; the kit says a run without them binds 3100/3597/3598/3599 and makes that a Blocker for the gate's own process. 9884 landed render, 9885-9889 plant servers.
- D-5: The gate may GET `actions/jobs/<id>/logs` (a GET under the project config) to see whether the new spec ran on the Linux runner; allowed by the rules (gh -X GET), added explicitly.
- D-6: Main-moved STOP list includes `web/src/server/auth/config.ts`, `web/scripts/e2e.mjs`: if #236 lands first, the gate must re-read the spec's server premise.
- D-7: A LANDING CHECKLIST of 11 items is ordered at the end of STATUS.

## Q-questions for Tuesday (each with a default)
- Q-1: Does B833's GO WITH FINDINGS (the finding this PR closes) count toward the class? Default: no, it is not a NO GO round; kit writes "NO GO 0 of 2 on this PR ... round 1 of 2".
- Q-2: Third `webServer` entry: the gate measures and gives ACCEPT / ACCEPT WITH CONDITION / REFUSE; the decision is Tuesday's. Default: accept the gate's reading; a REFUSE is graded a Major.
- Q-3: If #236 lands before #238, #238 is behind main and (strict=false) still squashes cleanly; the kit's main-moved rule STOPs on a moved `config.ts`. Default: re-pin main, the gate re-reads the premise, no new head needed. Say if you prefer to land #238 first.
- Q-4: Whether to push the hosted HPSM-POC site after the merge: no product byte changes, nothing to show; default no.

## UNMEASURED
- The kit's predictions about plant outcomes (unit vs spec on p2, p5), the spec's runtime, the runner behaviour of the third server, a port clash on the runner, the timed-only and live-API runs: nobody ran them.
- `refs/pull/238/merge` tree vs head tree: not read (kit orders it).
- Whether `/api/health` answers in mock + UAT open mode (builder's runs imply it; not measured by me).
- The B805/B817 control of the verdict-line loop was not printed; the other controls were.
- Local checkout `2_Project_Files` did not contain `web/src/components/shell/HpLogo.test.tsx` (stale or different layout); I read everything from origin via `gh api` and noted this in the kit's partition.

## Outside the fences
- My first `sed`/`ls` bash call for model-routing included a typed `cd` (inside a command that read three files); the hook refused it, nothing ran. No other cd.
- One `ci.yml` copy and nothing else was written to the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/cf1516ef-104e-4a53-8f1c-9d124c834724/scratchpad/ci.yml` (a scratch read copy of the head's workflow). A first zsh `gh api` call with an unquoted `?` globbed and failed harmlessly; re-run quoted.
- No Jira, no decision_queue, no mail, no HTTP to hosted hosts, no git write, no fetch, no az/ssh/docker. Only the two output files (kit, this report) were written in the project tree.
- The kit names the ticket key HPSMPOC-361 (landing text, per the relay) and B-numbers (template practice); no person's name and no decision-card id in the kit.
