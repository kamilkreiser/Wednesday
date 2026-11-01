STARTABLE: YES

# B1045 DRAFTER REPORT - SEAT-M63, NexusAI RD-913 lock-only raise of the two HIGH audit rows

Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1045_SEAT-M63_nexusai-rd913-audit-highs.md` (81 lines, unstamped: 9 lines carry the four-underscore pattern, i.e. 8 slots plus the last line; `@[A-Z_]+@` count 0, with a control that reads 1).

## BLUF
- This is a builder kit for ONE commit on `b1045/nexusai-rd913-audit-highs` from main `89375808`. It runs `npm update follow-redirects joi` (lock-only). The expected raises are follow-redirects 1.16.1 to 1.16.2 and joi 18.2.9 to 18.3.1. `package.json` must stay byte-identical (blob `3908a828`).
- **The CI pass predicate was read before the check was specified.** `npm-audit.yml:41-50`: the job passes only if `npm audit --omit=dev --audit-level=moderate` exits 0. **This lane cannot make that true**, because the 12 moderate rows remain. So the kit's own predicates use the same tool:
  - P1: `--audit-level=high` gives rc 1 at main and rc 0 after.
  - P2: the CI command gives `moderate 12, high 0, total 12`.
  - P3: the moderate name set after equals main's set minus the two raised packages.
  - The kit says plainly that the branch's own hosted npm-audit run reads `failure`, that this is expected, and that RD-913 STAYS OPEN for the moderates.
- Lock-only is proved in the kit by:
  - `package.json` hash unchanged;
  - a closure of changed lock keys, stated as a property ("at least these", then "any other shape: prove or STOP");
  - semver satisfaction of every declaring range, by program with the tree's own `semver` (with a control that can fail); any major change, out-of-range version or `overrides` need is a STOP (C-196 line 2138);
  - reproduction plus a fixed point;
  - full `npm run verify` equal to the unchanged counts file (5267/311);
  - a boot proof on 8470-8479.
- Model: Sonnet `claude-sonnet-5-5` (models_latest.json:23), row C2 (model-routing.md:92). C3 (line 93) was considered and rejected: no design decision is made, because the versions are named by the advisories. Gate: G2 (line 109), with G1 (line 108) offered as Tuesday's option. The launch line carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes.

## Facts re-measured (instrument, control)
- **Main** `8937580841a39123f32955c3df067af01544418e`. Read 13:40:46 AEDT by `gh api -X GET git/ref/heads/main` under NexusAI's GH_CONFIG_DIR (gh auth reads the project account). `compare 88144175...89375808` gives ahead 2, behind 0, HISTORY.md only.
- **Blobs at main** (raw contents GET, then `git hash-object`; the package pair was also compared with `git/trees/<main>`, equal):
  - package.json `3908a828` (104 lines)
  - package-lock.json `050c1a2a` (8912 lines, lockfileVersion 3, 691 keys)
  - npm-audit.yml `61a6804d`
  - build.yml `e4e5c095`
  - deploy-demo.yml `597b3487`
  - verify-suite.sh `eb9731f5`
  - counts file `7680a3ff` (5267/311)
- **Lock parse** (`python3 -I`):
  - follow-redirects 1.16.1, production, one copy. Its parents are axios 1.20.0 (`^1.16.0`, production) and http-proxy 1.18.1 (`^1.0.0`, dev).
  - joi 18.2.9, production, one copy, required only by the root (`^18.2.9`). It has 7 `@hapi`/standard-schema dependencies, all locked inside their ranges.
  - Controls: axios 1.20.0, express 5.2.1, the nested glob 10.5.0, semver 7.7.3.
- **CI log at main** (`gh api -X GET actions/jobs/124709532222/logs`, run 41259466227, main 89375808, push, failure):
  - metadata `{"info":0,"low":0,"moderate":12,"high":2,"critical":0,"total":14}`;
  - 14 name/severity pairs, matching the ticket's list;
  - runner npm 11.19.1, node 24.22.1. Local npm is 11.19.0 and node v26.8.1 (same npm minor).
- **Advisories** (`gh api -X GET advisories/<id>`; control: a nonsense id gives 404):
  - GHSA-mrwp-f3q8-3g9p: high, follow-redirects `>=1.16.0,<=1.16.1`, patched in 1.16.2.
  - GHSA-4528-x5fx-h6hg: high, joi 18 `<18.3.1`, patched in 18.3.1.
  - The glob and minimatch moderates: patched in 14.0.2 and 11.0.1 (not lock-only, as the ticket says).
- **Branch rules** (`rules/branches/main`): `required_status_checks` is an EMPTY list, so the audit check is not required. The CodeQL thresholds are errors and high_or_higher. `branches/main/protection` gives 404 (rulesets only).
- **deploy-demo:**
  - `paths-ignore` covers only `**.md`, `docs/**` and `tests/**` (lines 29-32). So **a lock merge triggers it**.
  - The build job is gated on `vars.CI_DEPLOY_ENABLED == 'true'` (line 53). The deploy job's condition is at line 91, and it runs in environment `demo` (line 95).
  - The last 3 runs (88144175, 8a812415, 436a1bfb) were completed/skipped, with both jobs skipped.
- **Open PRs: 0.** Controls: `pulls/99999` gives 404, and the closed list gives #148, #147, #146.
- **Live branches:** 32 `b8*/b9*/b1[0-9]*/records/*/dependabot/*/deps-*` heads, all at ahead 0. Controls: `de5d8bb5...main` ahead 10; `c68fa6c2~1...c68fa6c2` lists package-lock.json.
- **Jira** (b774lib.py in-process GET; control: RD-99999999 gives 404):
  - RD-913: To Do, High, 0 comments, 0 links.
  - GHSA search: 1 hit (RD-913).
  - follow-redirects search: 11 keys.
  - The zzqxnonexist control returns 0.
  - RD-879 and RD-881 are both Testing, both lock-only, both landed.
- **Lock history** (`commits?path=package-lock.json`): 5f04d695, c68fa6c2 (RD-881), 6a69fdf4, c139e4a8 (RD-879), dda37622.
- **Ports:**
  - `lsof -nP -iTCP:8470-8479 -sTCP:LISTEN` is empty. Control: the unfiltered lsof lists `*:5000` and others.
  - A word-bounded scan of the 74 non-`.pre-` SEAT kits of 10-31 and 11-01 found 0 hits for `847x` before this kit (this kit is now the only hit). Control: `84xx` hits B1003's `8425`.
  - 8460-8539 is likewise free; 8470 was picked.
- **Panes** (`tmux list-panes -a`): tuesday, Datasec/ATTIO-R113, Datasec/Security-Composer-R112, fleet-monitor. There is no NexusAI pane.
  - M63 appears in no kit (word-bounded scan; control: M60 is in 14 files).
  - `refs/heads/b1045*` 0, `b1044*` 0 (control: b1018 gives 1).
  - `session-tools/b1045` and `worktrees/b1045*` are absent.
- **B1044:** no kit and no report in `tuesday/briefs` at 13:4x (ls, filter `B104[3-9]`, 0 rows). So its port block could not be checked. The kit asks the stamp to confirm it differs from 8470-8479.
- Lock tool sha256 is `cf01bafb...4971f`, equal to B1018's stamp.

## D-decisions
- D1. The pass check is P1/P2/P3, not the CI predicate. The CI predicate is written into the kit verbatim, along with why it stays red. A lane that "makes npm-audit green" is impossible without touching the moderates, which is out of scope.
- D2. The version rule is a property: at or above the patched version, same major, satisfying every declaring range by `semver.satisfies`. `npm update` may choose a newer in-range release than the ticket's figure; that is allowed and recorded with its publish time, not a STOP.
- D3. The lock closure allows joi's own dependencies to move only when the new joi's declared range forces it (shown by `satisfies(old, range)` = false). Joi 18.3.1's dependency set is UNMEASURED by the drafter: there was no registry read.
- D4. A boot proof is included (B497 precedent; axios and joi load at start) and uses ports 8470-8479. A real redirect is NOT TESTED.
- D5. The counts file is asserted, not written (no test is added). If B1044 lands first, the counts are re-baselined to the new main, and this is not a stop.
- D6. `fixAvailable` for the 12 moderates is recorded from the same audit JSON, read-only, as input for the product owner's ruling. No `npm audit fix` and no parent-upgrade trial.
- D7. The proposed timing is target 120 / HARD STOP 180 minutes (lighter than B1018's 150/240: no mutants, one verify).

## Q-questions for Tuesday (each with a default)
- Q-1 Model: Sonnet, C2 line 92? **Default YES.**
- Q-2 Gate tier: G2 (line 109), or G1 (line 108) because follow-redirects is a credential-header library? **Default G2** (the RD-879/RD-881 precedent, lock-only).
- Q-3 Ports 8470-8479 for B1045. Confirm that B1044's kit uses a different block, or none. **Default YES.** RD-912's cells use the harness band from 39000, so B1044 likely needs no block.
- Q-4 Should a version newer than the ticket's (still in range and same major) be accepted? **Default YES, recorded with its publish time.**
- Q-5 Landing: is a lock change merged to main acceptable when it triggers deploy-demo, with the build gated by CI_DEPLOY_ENABLED (last 3 runs skipped) and the deploy gated by the `demo` environment? **Default YES.** Tuesday reads the latest run's jobs before landing, and the demo environment is never approved under the merge grant.
- Q-6 RD-913 status after landing: comment only and leave it To Do, or move it to Testing per the code-change rule while it stays open for the moderates? **Default: comment only, leave it open** (its Done-when is unmet). The moderates go to the product owner as a separate ruling card.

## UNMEASURED
- Joi 18.3.1's and follow-redirects 1.16.2's declared dependencies and publish times, and the newest in-range releases. No registry read was made (fenced from hosted hosts); the builder reads them with `npm view`.
- Whether `npm update` on npm 11.19.0 leaves the lock a fixed point with no churn. B497 found that it did on the same npm line.
- Joi's `email({multiple})` reachability at main. The drafter's read (0 `email(` in validators.js) was at the STALE local checkout `cd2b5439`; that object lacks main (`cat-file` on 89375808 fails).
- B1044's port block and its exact paths: no kit had been filed. The paths are relayed from the commission and SWEEP-1330 lane 3.
- Whether CI_DEPLOY_ENABLED is currently 'true'. Skipped jobs are evidence, not a read of the variable (variables were not read).
- The hosted Build and CodeQL on the future PR.

## Outside the fences (disclosure)
- I wrote only the two files above, with Write/Edit. Scratch reads were saved under the session scratchpad `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f8947a38-04ac-46b8-96f3-ceebf0948b77/scratchpad/b1045/`.
- The CI job log was fetched with `gh api -X GET --allow-escape-sequences` into that scratch file and parsed after stripping escapes. It is a GET of GitHub's API, not a project host.
- Local git use was read verbs with `--no-optional-locks` only (cat-file, rev-parse, log, grep) on the stale shared checkout. `node -v` and `npm -v` were run for versions only; no other npm command was run.
- There was no decision-store read, no HTTP to any hosted, demo or production host, no az/ssh/docker, and no Jira write (`post_comment`, `create` and `do_transition` were not called).
- One fence-adjacent call: the Jira control called `issue("RD-99999999")`, which raised SystemExit with a 404, as intended.
