GATE B1433: GO WITH FINDINGS @ b7bafb8 on main 849b808

Subject: branch `b1433/nexusai-b-csp-intake-edges-and-typed-fields` of datasecau/Reporting_Dashboard_Au, head `b7bafb8d11cb8c228dc2d5384ef7eec5fe0ab6f3` (RD-759 shapes 1-2, RD-796). Main read fresh at 13:3x AEDT: `849b808c567e4d31d78e2d50b582540ae1920c67` (#185, HISTORY.md only since the branch base `3929b794`).
Verifier: read-only to origin. Own clone at `<scratchpad>/b1433v/clone` (push URL `INVALID-NO-PUSH`, repo-local deploy key), worktrees `wt-main`, `wt-head`, `wt-merge`, `wt-red` there. No path has a dot component (F-1). No push, no PR, no Jira, no mail, no `az`, no lane lock taken, no sibling tree touched. Ports 9890-9899: 0 listeners before and after (control: all-port listener count 18).

**BLUF: 0 Blockers, 0 Majors, 6 Minors.** 2 of 2 paths are inside OWNS-B. Overlap with open PRs and with sibling lanes is 0. The merge is clean and equals main plus the head blobs. Main, head and merge read the same, by program: the head and the merge add exactly the 20 new cells, remove 0 names, change no outcome on a shared name, and add no failing suite. All 16 predicted cells go red with the fix removed. The merge WOULD start a `Deploy demo` run. Its jobs are gated on `CI_DEPLOY_ENABLED`, and the last 4 push runs on main read `skipped`. The landing precondition is the counts file: it must be regenerated (5513/327) or the PR Build reads `VERDICT: FAIL` on stale counts.

## Evidence (each with its instrument)
| # | Check | Result | Instrument / control |
|---|---|---|---|
| 1 | Ref = READY sha | `ls-remote` `refs/heads/b1433/nexusai-b-csp-intake-edges-and-typed-fields` = `b7bafb8d...` (read twice, start and end) | `git ls-remote`; control `refs/heads/main` printed 849b808c |
| 2 | Commits | 1 commit, parent `3929b794`; author `Claude <noreply@anthropic.com>` | `git log --format='%H %P'` |
| 3 | Paths in OWNS-B | **2 of 2**: `backend/services/cspReport.js` (M, +33 -6; `backend/*` with no `-` line matching it), `__tests__/rd759-796-csp-intake-edges-and-typed-fields.test.js` (A, +108; `+new rd<N>-*`, N=759 is in the QUEUE and the path is absent at main) | `git diff --name-status/--numstat 3929b794 b7bafb8d` |
| 4 | Overlap: open PRs | 0 open PRs | `gh api -X GET pulls?state=open` = 0; control `state=closed&per_page=3` = 3 (#185, #184, #183) |
| 5 | Overlap: sibling branches on origin | `b1431/nexusai-t-ci-actions-browser-assert` (7 paths: `.github/workflows/*`, `scripts/assert-browser.js`, 2 tests); `b1431/nexusai-t-csp-tool-edge-cases` (4 paths: `scripts/csp-convert.py`, `scripts/refactor-inline-styles.js`, 2 tests); `b1433/...learning-manager-log-lines` (2 paths). No `b1430/*` or `b1432/*` on origin. Intersection with this branch: **0** | `git diff --name-only $(merge-base) <b>` per branch |
| 6 | Merge | `git merge-tree --write-tree origin/main b7bafb8d` rc 0, tree `ee4d0971`. It differs from main only by the 2 head paths, and from head only by `HISTORY.md` (main's blob). Blobs: cspReport `f68287be` = head, test `6a6ed3d4` = head, HISTORY `be99ded8` = main | `git diff --name-status`, `rev-parse <tree>:<path>` |
| 7 | Landing form | merge commit: the last 5 first-parent commits on main all have 2 parents | `git log --first-parent --format=%p` |
| 8 | Deploy demo | the merge **triggers** a run: `deploy-demo.yml:26-32` `push: branches [main]`, paths-ignore `**.md`, `docs/**`, `tests/**`; `backend/**` and `__tests__/**` are not ignored. Jobs `build` (`:53`) and `deploy` (`:91`) are gated on `vars.CI_DEPLOY_ENABLED == 'true'`. The last 4 push runs (3929b794, 763f0006, 9926903f, 33db7181) read `skipped`. The variable was not read directly | `git show b7bafb8d:.github/workflows/deploy-demo.yml`; `gh api -X GET .../deploy-demo.yml/runs` |
| 9 | CI at main / head / merge | `node -c` x3 rc 0,0,0 at all three; `npm run lint` rc 0 (placeholder, not proof); `npm run verify -- --maxWorkers=2` measured **5493/326 -> 5513/327 -> 5513/327** tests/suites. Failed **43 / 43 / 43**: the same 2 suites at all three (`rd404-sentinel-first-boot-vs-wipe`, `rd441-persistence-alarm-reaches-dashboard`). They failed only because I set `TMPDIR` to a `/tmp/` path, which their helper refuses ("paths contain /tmp/"). Re-run with the default TMPDIR: **43/43 pass at main, head and merge.** With that taken into account, every test passes at all three. `rd438-dot-segment-gate` passed at all three (non-dot path) | serial runs 12:18-13:33 with `JEST_BIN` wrapper keeping jest's JSON; `cmp.js` comparison of names and outcomes |
| 10 | Comparison by program | main -> head: added 20 names, all in the new file; removed 0; outcome changes on shared names 0; failing suites head minus main empty. head -> merge: identical (0/0/0) | `<scratchpad>/b1433v/bin/cmp.js` on `raw/{main,head,merge}.json` |
| 11 | Counts predicate | the committed file reads 5493/326. Measured at head and merge: 5513/327 (+20/+1). Unregenerated, verify fails "stale" by design. Tuesday regenerates the file at landing | `git show origin/main:scripts/verify-expected-counts.json` |
| 12 | Red without the fix | base blob `0c5657d4` planted in `wt-red` (`hash-object` equal): **16 failed, 4 passed**. The failed cells are exactly E-NBSP, E-LS, E-BOM, E-TRAIL, E-UNPARSEABLE, P-ENCODED, P-RELATIVE and every D-* and L-* cell. The passing cells are the controls C-MIXED, C-PLAIN, C-PATH, C-DATA. Restored by blob, `git diff --quiet` rc 0, then 20/20 pass | jest JSON per cell |
| 13 | Closed lines at main | RD-312: `dataErasure.js:1047,1051` ("purge did not start", `stateWriteFailed: true`), `:1369-1409`. Commits 2b2734a and 48e092c are ancestors of main. The cited cells (`erasure-ledger-survives-every-writer:808`, `erasure-partial-purge-leaves-a-record:522`) are in suites that passed at main. RD-590 residue: `127.0.0.1 for localhost` still occurs once at main (correct: that label lives on a different branch) | `git grep -n -i`, `merge-base --is-ancestor` rc 0 |
| 14 | Name scan | added lines 0, commit message 0, output texts 0 | `(?<![A-Za-z])<name>(?![a-z])`, re.I, over the 9 names plus the account login; controls: planted `_by_<name>_` fired 10/10, longer words 0, `\b` form on a planted `_by_<name>_` = 0 |
| 15 | Secrets / ids / hosts / Cf | non-ASCII added lines 0 (control 1); GUIDs 0 (control 1); hosts only `example.com` x8; secret-shaped words 0 (control 1). gitleaks over the branch commit: rc 0 (control: a planted `ghp_` value, rc 1). Repo-wide Cf scan over tracked text: 5 files / 5 chars at main, and the same list at merge | grep, `gitleaks git --log-opts=3929b794..b7bafb8d`, `cfscan.py` |
| 16 | Log path of the new fields | the route logs the entry as an object argument (`server.js:856` `logger.warn('... CSP violation report:', entry)`), not interpolated, so a CR/LF inside violatedDirective reaches the log as an escaped field | `git show origin/main:backend/server.js` |

## Findings
| ID | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | `authority.toLowerCase().lastIndexOf('%40')` lowercases the authority before searching. That does nothing for the needle "%40", which has no letters. It also shifts the index wherever lowercasing makes a character longer (U+0130 becomes 2 code units), and the shifted index is then applied to the original string. Result: host characters are dropped. No userinfo leaks. | `https://\u0130\u0130\u0130:p%40host.example/x` -> head `https://t.example/x`. The correct result is `https://host.example/x`; main kept the whole value |
| F2 | Minor | In an unparseable authority with no userinfo, a `%40` inside the query now replaces the host with query text. RD-735's design already did this for `@` (the authority runs past `?` and `#` on purpose), so this extends an existing shape to `%40`. Forged reports only. | `https://h:99999?a%40b` -> main `https://h:99999`, head `https://b`; the `@` form reads `https://b` at both |
| F3 | Minor | The new cells pin only 4 of the non-ASCII edge code points (U+00A0, U+2028, U+FEFF, U+3000). A mutant that cuts `isEdgeChar` to just those 4, and also drops `toLowerCase`, passes all 4 suites that load `cspReport` (48/48). U+1680, U+2000-200A, U+2029, U+202F and U+205F are unpinned. | mutation in `wt-red`, restored by blob |
| F4 | Minor | `typedDirective` cuts at 256 UTF-16 units, so the cut can split a surrogate pair and leave a lone `\ud83d`. It is harmless in the logged object. | `'a'.repeat(255)+'\u{1F600}'` -> ends `"a\ud83d"` |
| F5 | Minor (residual, pre-existing, outside the ticket's named shapes) | A leading invisible character that is NOT white space still keeps the userinfo, at both main and head: U+200B (Cf) and U+0085 (NEL). For the records pass, not this branch. | probe P5/P6, same output at main and head |
| F6 | Minor (claims) | STATUS claims graded below. Two are not shown, and the partition row is stale. | below |

## Builder STATUS claims (graded)
| Claim | Grade |
|---|---|
| head `b7bafb8d`, `HEAD^{tree}` `06fa8611` | true (`rev-parse`) |
| `cspReport.js` +33 -6; test +108 (new) | true (numstat) |
| 16 predicted RED at base, green at head; 0 unexpected; 4 controls green at both | true (row 12) |
| full suite from the non-dot path PASS 5513/5513, 327 suites | true in counts (5513/327, all passing once the TMPDIR-only suites are run with the default); the builder's literal VERDICT line is not shown to me |
| pushed, ls-remote = head | true |
| tests added +20 | true |
| targeted csp suites "6/129" | not shown (I found 4 suites naming `cspReport`, 48 tests) |
| name scan 0, gitleaks rc 0, ownership inside OWNS-B, no skip/only/todo/.each, no dependency | true (rows 3, 14, 15; `git diff` adds no `skip`, `only`, `todo` or `.each`; `package*.json` unchanged) |
| "Partition against other lanes' branches: not computed (none on origin)" | stale: two `b1431/*` branches now exist; intersection 0 (row 5) |
| "pushed branches sit on 3929b794 and were not re-verified on the new main" | true; re-verified here at merge with `849b808c` |

## Tier
The kit names no S8 tier slot for this gate. Its line 4 leaves the post-branch gate to Tuesday (G1 or G2). The change hardens a security-adjacent intake (it strips userinfo from anonymous CSP reports). None of the findings is a leak or a new exposure: F1 and F2 lose host text, and F5 is pre-existing. I raise no tier-1 item.

## NOT RUN
- Hosted CodeQL (UNMEASURED; Tuesday's read on the PR and on main after landing).
- Hosted gitleaks full-tree and history scan, npm-audit, arm-ttk: not run. No `package*.json` or `azure-marketplace/**` change; gitleaks was run over the branch commit only.
- Plain `npm run verify` with the regenerated counts file: not run. The counts predicate is computed by program (row 11).
- The repository variable `CI_DEPLOY_ENABLED` was not read; "jobs skipped" rests on the last 4 push runs.
- Jira was not read (fence). The ticket scope was read from the sweep's `tickets-by-lane.tsv` excerpts.
- Local node is v26.13.0; CI pins node 24.
