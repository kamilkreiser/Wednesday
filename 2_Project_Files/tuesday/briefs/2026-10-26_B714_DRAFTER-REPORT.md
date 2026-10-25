STARTABLE: YES

# B714 drafter report (SEAT-G134, NexusAI PR #117 counts gate, tier 2 Sonnet)

Drafted 2026-10-26 08:17-08:3x AEDT (clock from `date`: 08:17:28 at start). Kit: `2026-10-26_B714_SEAT-G134_nexusai-117-counts-gate-tier2.md` (85 lines, shape of B697). Launch needs your stamps in the 8 slots; nothing else blocks it.

## BLUF
- Gate kit for PR #117 at head `f1d23b25`, 7 commits on main `8ae0a87f`, 5 paths, +286 -21; round 1 of 2 on class "a new test cell that pins less than it claims".
- The heart is Check 3: a 53-row attribution table (each added cell killed by a gate-written mutant; controls by an over-fire mutant), plus a gap proof for the R8 arm, an environment check on the temp-repo helper (GIT_* hook shape, tmp leftovers, 3 runs), and an RD-854 honesty check (fix reproduced red, Dockerfile lines 46 and 100, ticket premise by Jira GET).
- Verify instrument is the PR's own `Build` run 40234770324 (four predicate lines); a local verify is NOT planned because the builder's own took 1339 s, over the 20-minute ticket bound (Q-2).
- At 08:17 `build` and all three `Analyze` runs were still in progress; the `CodeQL` check-run said `neutral` and only 1 of 3 analyses existed on the PR ref (not clean, not scanned yet).
- Ports 9810-9819 free; pane `Datasec/NexusAI-G134` free; M14 (B713) named in PARTITION and the lock-wait line.

## Facts re-measured (instrument, control)
- Refs, `git ls-remote origin` 08:17:48: main `8ae0a87f`, branch = `refs/pull/117/head` = `f1d23b25`, merge ref `102fdefc` (GitHub `git/commits`: parents `8ae0a87f` then `f1d23b25`, tree `e13b225d`, equal to the head commit's tree). Control: a nonexistent commit sha returns 422.
- PR: `gh api -X GET pulls/117`: open, not draft, mergeable true, state blocked, commits 7, files 5, +286 -21. Open PRs: only #117. `pulls/117/files` blobs equal the builder's five blobs; counts blob `fd0f3b0d` at the head, `a8085c1d` at main, `backend/validators.js` `37ff4001` at both (by `git hash-object` of raw `contents` GETs; control: `contents/zzz-no-such` returns Not Found). Counts file reads 5155/306 at the head, 5102/306 at main.
- Cell arithmetic: only a coarse static census was done (loop-generated titles make it unreliable, and the kit says so): test-site counts main to head rd777 26 to 27, rd848 10 to 23, rd618 14 to 14. The 130 to 183 title figure is the builder's, RELAYED, and Check 2 re-measures it with `--json`.
- Branches against main (`compare`): all live `b6*`/`records/*` are ahead 0; so the path intersection B is empty by that frame (frame: GitHub `compare` of 10 named branches; `b658` etc. behind only).
- CI at 08:17: success: Gitleaks Scan, `audit-production-deps` x2, `npm-audit` (PR and push runs); `CodeQL` completed neutral; in progress: `build`, `Analyze` x3. Analyses on the PR ref: 1 (actions). Alerts open/fixed/dismissed on head and merge ref: 0/0/0 (partly unscanned). Ruleset read: `alerts_threshold` errors, `security_alerts_threshold` high_or_higher, required checks list empty.
- CI predicate read at main raw: `build.yml:83-84` `npm run verify -- --maxWorkers=2`; `verify-suite.sh` fails both directions (`:91-92` header, `:360` stale-expectation fail, `:366` PASS line). The kit writes the pass predicate (5155/306) into itself.
- Deploy demo at main raw: push on main, `paths-ignore` `**.md`, `docs/**`, `tests/**` (`:28-32`), jobs gated on `vars.CI_DEPLOY_ENABLED` (`:53`, `:91`), `environment: demo` (`:95`); last four runs 40194248414, 40169545160, 40152375904, 40130530818 all push/completed/skipped. This merge touches `__tests__/` and `scripts/`, so a run starts and is expected `skipped`.
- Ports: `lsof -nP -iTCP:9810-9819 -sTCP:LISTEN` empty, rc 1. Word-boundary scan over the 104 non-`.pre-` SEAT kits of 10-25 and 10-26 hit 6 Composer kits (B627, B631, B633, B641, B646, B688), all finished seats citing the old block; the control form `969[0-9]` hit kits (so the scan can fire). Live panes: tuesday, NexusAI-M14, Composer J19 and G133, HPSM-POC H28 and H29, MPS-M28, fleet-monitor. No kit or pane names `NexusAI-G134`.
- Model: row G2 is at `model-routing.md:109` (read); `models_latest.json` sonnet = `claude-sonnet-5-5`, `checked_at_local` 2026-10-26 07:42:13.
- Lock tool sha256 `cf01bafb...` = the value you gave; `queue-jest/` empty; usage line from the tool's own header (`sed -n 1,40p`, not invoked).
- Landing rule read by line: C-190 `:2062` (ruling), `:2067` (merge path: "land the SAME commit. Never squash, never rebase"), `:2068`, `:2073`, addendum `:2076`; C-68 `:665`; the #112 head-pinned merge is recorded in C-222 (`:2397`). The C-190 `:2067` text itself does not say "merge commit"; the head-pinned MERGE commit is the practice recorded for #112, and the kit quotes both.
- Round count: B667 `NO GO round 2 of 2` on PR #112 (class "no cell proves ..."); B647 NO GO round 1 of 2. No gate exists yet for PR #117 (new PR).

## D-decisions
- D1: copy the B697 shape, but the heart is a per-cell kill table, not a harness table.
- D2: no local verify; Build run 40234770324 is the instrument (the 22-23 min verify is over the 20-minute ticket bound; the 3-file jest runs are 10-20 s each).
- D3: the builder's mutant ids (M35/M36/M39, HM5/7/9, CSPV1/2) are prior art only; the gate writes and anchors its own, and must add mutants for cells these leave unkilled ("property first, then at least these", with "any other shape: prove it meets the property or STOP").
- D4: CONTROL cells are graded Minor unless their job is a named guard, because the builder's own STATUS says controls stay green on the unfixed helper by design (so "every new cell red" is false for them as stated).
- D5: the dropped RD-854 is checked by reproducing the fix red in the mutant tree and one public GET of the packer file at the azure-cli 2.90.0 tag; the empty-layer question stays NOT TESTED.
- D6: Check 3e (GIT_DIR / GIT_INDEX_FILE shape, `rd852-ctx-*` leftovers, 3 runs) added because the helper makes a git repository inside jest.
- D7: cap-family flag: a Major in the 24 rd777 cells is reported as being in the family the cap closed on #112.

## Q-questions for Tuesday (each with a default)
- Q-1: does B667's "round 2 of 2" on the same family carry over to PR #117? Default: no, new PR starts at round 1 (C-222 landed #112 and ticketed these cells as RD-882).
- Q-2: local verify? Default: not run (22-23 min exceeds the 20-minute bound); Build run 40234770324 is the instrument; if Build is red or not done 90 min after Step 0, the verdict is at most GO WITH FINDINGS with "verify NOT TESTED locally".
- Q-3: tier 2 Sonnet on G2? The cells pin a security filter (`javascript:`/`data:` scheme strip), a G1-like surface, but no filter code changes and `validators.js` is byte-equal. Default: tier 2 Sonnet; promote to Opus only if you read the surface as G1.
- Q-4: the one public GET of Azure CLI's `_archive_utils.py` at tag 2.90.0 (Check 4d) under the project gh config. Default: yes (the builder did the same one GET).
- Q-5: port block 9810-9819. Default: use it (free, previous owners finished); move it if another brief took it.

## UNMEASURED
- Whether the 53 cells are each killed (Check 3 measures it); the 130 to 183 title figure (relayed); CodeQL and Build results (in progress at 08:17); the `node` = 1000 assumption; whether any hook-run environment affects the temp-repo helper; the exact lines of the helper's context-builder clauses for the H7-H9 mutants (the gate reads them first); the B713 lock holding pattern (its kit says up to 40-minute tickets).

## Outside-the-fences disclosure
- None. Read-only: `ls-remote`, `gh api -X GET` under the NexusAI `GH_CONFIG_DIR` (pulls, files, contents raw, compare, check-runs, runs, analyses, alerts, rules, branches, workflow runs, git/commits), `lsof`, `tmux list-panes`, file reads, local greps. Raw contents of 4 test/helper blobs plus two small files went to the session scratchpad only. No clone, fetch, npm, jest, Jira, az, ssh, docker, hosted host. Never ran `decision_queue.sh`, never read the forbidden stores. One zsh hook refusal (a `=====` echo separator) and one advisory (case-sensitive grep) occurred; both were retried correctly. Only the two named files were written.
