STARTABLE: YES (conditional on Q-1: the npm registry for `npm ci`; without a YES in S4 the seat stops before Step 5)

# B1270 drafter report (kit: `2026-11-04_B1270_SEAT-G338_mpscalc-deps-120-121-gate-tier2.md`, 62 lines, 8 four-underscore lines, 0 `@X@` slots, 0 non-ASCII; slots: `2026-11-04_B1270_slots.json`, 8 keys, drafter facts + `@NOW@` + `@SEAT@` only)

## BLUF
- One web tier-2 gate session for both Dependabot pulls (#120 undici, #121 zod): each PR is ONE path, `web/package-lock.json` +3 -3. **The commissioning premise "package.json + lockfile" is wrong: `web/package.json` is untouched by both**, because both packages are transitive dev dependencies and the existing ranges already admit the new versions.
- undici is pulled only by `jsdom` (`^8.11.2`), zod only by `eslint-plugin-react-hooks` (`^3.25.0 || ^4.0.0`) and as a peer of `zod-validation-error`. Zero source imports of either word in the whole repo. Both lockfile entries are `dev: true`.
- **CodeQL: NO ANALYSIS exists at either PR ref** (`analyses?ref=refs/pull/N/head` length 0 for both); the check-run says `neutral` "cannot determine the alerts ... 4 configurations present on main were not found". Open alerts 0 is therefore not reportable. Controls with analyses: main (current sha), `refs/pull/157/head` and `refs/pull/155/head` (4 each).
- **Main has moved** since the PRs' base: `60ac2e5b` (one test-only commit, `ComponentQuantityRuleTests.cs`) on top of `511e6c03`. Each PR is one commit behind; `web/` and `ci.yml` are unchanged, so the kit judges a squash on `60ac2e5b`.
- Lockfiles combine cleanly as text (`git merge-file` rc 0, control conflict rc 1; hunks start 367 lines apart; combined blob `7c7d4608...`); whether `npm ci` accepts it is the seat's `wt-both`.
- Landing rule: squash, head pinned (`CLARIFICATIONS.md:758`, `:774`); Tuesday lands #120 first, re-reads main and #121, then lands #121 (kit Step 8 order rule).

## Facts re-measured with instruments (all at 11:54-12:02 AEDT, `date` printed in the same commands)
- Main `60ac2e5b214c9e9f3a6c2da329bbb0c5996f4822` (re-read 12:02:44, same). #120 head `80f336a65221c62fa75c2b59cb86e6d1f7d7461b`, #121 head `19893df030eb5d5ac65198c00adf8892dd54c8a2` (full shas; re-read 12:02, same). Both open, not draft, mergeable true, state clean (they were UNKNOWN when Tuesday read at 11:5x). Both: 1 commit, parent `511e6c03`, verified true, commit dates 2026-11-03T23:31:15Z / 23:31:24Z. Each has exactly 1 comment, a Dependabot rebase request by the project account (control: #157 has 0).
- File census (frame: `pulls/N/files`, raw patch, raw blobs): #120 `web/package-lock.json` modified 3/3, one hunk `@@ -3908,9 +3908,9 @@`; #121 same file 3/3, `@@ -4275,9 +4275,9 @@`. Nothing else. Lockfile blobs: base `4e20034b53b6f28684370b2c75f2fea579f60beb` (identical at `511e6c03` and `60ac2e5b`, 4301 lines), #120 `84043c1a2faf51108cf62e30d1e2542d9c9f175b`, #121 `6c4123d1183f2c7ba35cc4c6c2af2cabd4dc2035`, combined `7c7d4608f669a19e4b52c963cdb4debb81d6f879`. Non-ASCII 0 in all. Control for the package.json claim: `react` at `:24` prints, `undici`/`zod` print nothing (rc 1).
- Direct vs transitive: lockfile walk by `python3 -I -B`: undici <- jsdom 30.1.2 (`:2728`, dep line `:2749`, entry `:3910`); zod <- eslint-plugin-react-hooks 7.1.1 (`:2262`, `:2272`) and peer of zod-validation-error (`:4287`, `:4297`), entry `:4277`. Control `node_modules/nosuch-zz-b1270` 0.
- Imports: `git grep -n -i -w` at `511e6c03` over `web/` excluding the lockfile: undici 0, zod 0; whole repo excluding lockfile 0; control `from 'react'` 51 files.
- Upstream (gh api on public repos, reachable): undici 8.12.0/8.12.1/8.12.2/8.12.3 releases exist (88 commits, 195 files); 8.12.2 is a security release with 8 GHSA ids. zod 4.6.6/4.6.7 exist (13 commits, 20 files; source changes in `core/schemas.ts`, `util.ts`, `compile.ts`). **zod 4.6.6's release body opens with a maintainers' disclosure of a compromised credential (reverted, unpublished per the text)**: relayed, marked RELAYED in the kit, to be printed whole by the seat. This is worth Tuesday's eyes before landing #121 even if the gate passes.
- Hosted CI per head (`check-runs`): dotnet, web, python, package all success on both; CodeQL neutral. CLAIMS; not re-run.
- Ruleset `24139430` "Security scan rule": `code_scanning` (CodeQL, errors / high_or_higher), `required_status_checks` with an empty list. What it does to a PR with no analysis: UNMEASURED.
- Round census: 374 first lines, 97 GATE VERDICT, 14 NO GO (filter fires, control B1213 1 / zzz 0). 42 class names extracted (control `class "web:` 8, `quantity audit` 3); 0 name a dependency, bump, lockfile or Dependabot. New class: round 1 of 2, NO GO 0 before.
- Model: `model-routing.md:109` G2, `:111` G-cap, `:98` C8; `models_latest.json:23` claude-sonnet-5-5; `brief_seat.sh:24` defaults Opus; launch has `BRIEF_SEAT_LEVEL=sonnet` inside the quotes and `WED_USAGE_STOP=100` outside as well.
- CI predicate read (`ci.yml`, 123 lines): web job `:45`-`:66`, node 24 `:58`, steps `:61` `npm ci`, `:62` lint, `:63` test, `:66` build + check-bundle. Pass predicate written into the kit.
- Landing: `CLARIFICATIONS.md:758` and `:774` read (squash, `--match-head-commit`). Repo allows squash, merge and rebase (`allow_*` read).
- Ports: none fixed. `vite.hostguard.test.ts:19`/`:82` use ephemeral loopback ports; `lsof` listeners at 11:57 listed in the kit; scan of 104 non-`.pre-` SEAT kits of 11-03 and 11-04 for `B1270`/`G338`: 0 hits (control `G335` 5). Panes: `%0 tuesday`, `%1 fleet-monitor`. Locks: none under `T/*`. Load 2.37/2.12/2.26, 175 GiB free. `refs/heads/b1270*` 0 (control `b1093` 1).
- Copy sources `T/b1185`: `node24` (v24.21.0, 200 MB), `heavy.sh` (`:8` `sleep 120`, `:9` other-seat-lock grep), `hb.sh`, `r.sh`; its STATUS first line is a GATE VERDICT and last a VERDICT line.

## D-decisions (mine, for Tuesday to accept or strike)
- D-1 Four worktrees (`wt-base`, `wt-120`, `wt-121`, `wt-both`), each with its own `npm ci`; controls run last in `wt-base` as untracked files (no fifth tree).
- D-2 Judged against main `60ac2e5b` (not the PRs' base `511e6c03`), as a squash of each head; MAIN-MOVE refuse covers `web/`, `ci.yml`, `global.json` only.
- D-3 Seat steps in the template shape: Step 3b (release notes) is gated behind `predictions.txt`; PR bodies are read only after Steps 5-7 (they carry Dependabot's release extracts, which are claims).
- D-4 Three controls (lint `debugger;`, vitest `expect(1).toBe(2)`, `tsc` type error) because a green npm run is zero evidence until its instrument is shown to fail; a stuck-green control voids that step (Major).
- D-5 A `--require` hook to see which runs load undici/zod, with a `react` control; if the control reads 0 the seat says NOT MEASURED (vitest ESM imports may bypass it). Optional by design, not a verdict input.
- D-6 Verdict has a word per PR plus one for the combination; a combined failure is NO GO on the combination only, #121 then lands after #120 plus a Dependabot rebase.
- D-7 Target READY 150 min, hard stop 210 min (four trees at about 5 heavy jobs each plus controls; template used 120/180 for dotnet).

## Q-questions for Tuesday (each with a default)
- Q-1 May the seat run `npm ci` against `registry.npmjs.org` (precedent: the B1185 kit's S4 ruled "the npm registry for npm ci only")? Without it, Step 5 cannot run (the two new tarballs are not in any local cache). Default: YES, registry for `npm ci` only, `npm_config_cache` seat-local.
- Q-2 Tier: these bumps are dev-only transitive deps, but undici 8.12.2 is a security release; row G2 says "config/CI, tooling". Default: G2 as commissioned (dev-only, no `src` import, a bundle check in Step 3d turns it into a Major if the package reaches `dist`).
- Q-3 The zod 4.6.6 disclosure: should #121 wait for any further check than the gate (e.g. you reading the maintainers' note)? Default: gate prints it as RELAYED and grades a Note; Tuesday decides at landing.
- Q-4 CodeQL has no analysis on either PR (neutral). Default: the gate reports NO ANALYSIS (alerts not reportable), grades a Note, and Tuesday learns at the merge whether the org ruleset blocks it; the seat never triggers a run.
- Q-5 Class ruling: new class, round 1 of 2, NO GO 0 before. Default: accept.
- Q-6 Jira: no ticket known for these PRs. Default: none, kit allows 0 Jira reads.

## UNMEASURED
Nothing installed, built, linted or tested. Whether `npm ci` accepts any of the three lockfiles; hosted-CI results (claims); which suites load the packages; the accuracy of upstream notes; ruleset behaviour on a PR without analysis; the heavy/light lock state at launch.

## Outside-the-fences disclosure
- Read-only throughout. Used `gh api -X GET` under the project's `.gh-config` (public upstream repos nodejs/undici and colinhacks/zod included; releases, tags, compare), `git --no-optional-locks grep/ls-tree/cat-file/show` in `2_Project_Files` (the local checkout is at `7f6ca4c0`, behind; `511e6c03` is present, `60ac2e5b` is not, so greps ran at `511e6c03`, equal for `web/`), file reads under the project (`CLARIFICATIONS.md`, `.tools` listing of directory names, `T/b1185` `heavy.sh`/`r.sh`/`node24 --version`), `git merge-file`, `git hash-object`, `git diff --no-index` on scratch copies, `tmux list-panes`, `lsof`, `uptime`, `df`, and `/usr/bin/grep` over the briefs folder. No `decision_queue.sh`, no ledger, no `briefs_staged`, no scoreboard, no WEDNESDAY/FRIDAY tree, no Jira, no HTTP other than `gh api`.
- One slip: the shared scratchpad was written by another process mid-session (a file I saved as `ci.yml` was replaced by an unrelated one); I re-fetched into my own `scratchpad/b1270/` and used only those copies. A `ls "$P/.tools"` printed the full tree name list (names only, no content read).
- Slots: no Tuesday-read attestation is pre-written; READ-WHOLE is the bare marker `DONE @NOW@ AEDT by @SEAT@`, which Tuesday applies only after reading.
