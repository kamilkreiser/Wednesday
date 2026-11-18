GATE B1704: GO WITH FINDINGS @ 86ae678 on main 2de5e84

G1 gate (Opus 5.5, in-session), 2026-11-18 10:27-11:15 AEDT (clocks from `date`). Target datasecau/Reporting_Dashboard_Au, branch b1694/nexusai-picomatch-audit-exception, head 86ae678f28591215f152be556120625ec9c79f8d (A 24b26ebc, K 86ae678f) over main 2de5e84c799e32232d65cd759085d728d7141583. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s289/g1704/` (clone, red1 worktree, plants.js, wfstep.sh, scan.py, chain.sh, logs/, raw/, cq/). Nothing written in the NexusAI folder; nothing pushed; no PR, Jira, mail, `az` or deploy.

**Landing condition:** none beyond the normal one (hosted Build, Gitleaks, npm-audit and CodeQL green on the PR head; head and main unmoved; deploy switch not 'true'). No finding blocks landing. Land BEFORE NX-M (b1691), which then needs a counts regeneration (F4).

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor | **One fail-open shape remains: a report that is internally inconsistent.** A version-2 report whose `vulnerabilities` is `{}` or `[]` while `metadata.vulnerabilities` says high 5 passes (rc 0, a NOTE only). The script checks the shape of `vulnerabilities` and traces every blocking node to an advisory, but never cross-checks the metadata counts. Before this change npm's own exit status (1) would have failed it. npm 11 does not emit such a report (the real report has 5 blocking nodes and metadata high 5), and every shape the commission named fails closed (measured below). | Follow-up, not a landing blocker: fail when `metadata.vulnerabilities` moderate+high+critical is not equal to the number of blocking entries in `vulnerabilities` (or when metadata is absent). Add one cell. Do it when the entry is removed. |
| F2 | Minor | **"Or on a fix" is honoured only through the range text.** The entry stops matching if npm reports another range or package (planted: `<4.0.8`, `<=4.0.6`, `<= 4.0.7`, `>=4.0.0 <=4.0.7`, another package: all fail). If picomatch 4.0.8 ships and the advisory keeps `<=4.0.7` (still accurate), the entry keeps allowing until 18 Dec. The code comment (line 7) and commit A message state "a patched release changes the range text" as fact; that is UNMEASURED (STATUS says so too). npm's `fixAvailable` cannot be used naively: it is ALREADY truthy today on all 5 nodes (npm proposes a semver-major move of sqlite3 to 5.1.7), so a fixAvailable check would lapse the exception now. Measured live 10:33: advisory high, range `<= 4.0.7`, first_patched null, withdrawn null; npm picomatch latest 4.0.7. | Calendar check (below). Optional follow-up: lapse on `npm view picomatch version` > 4.0.7 is not available offline in CI; the cleanest is the calendar. No code change required for landing. |
| F3 | Minor | **Unused `const path = require('path')`** at scripts/audit-prod.js:12. It cannot fail CI: `npm run lint` is a placeholder (package.json `lint` is a `node -e console.log(...)` "no linter configured" line, measured). CodeQL JS suite did not flag it (0 results). | Remove it in the follow-up that removes the entry (or with F1). Do not reopen this branch for it. |
| F4 | Info (landing order) | **Counts-file collision, measured by `merge-tree` against this head:** NX-M `b1691/nexusai-lane-nx-m-redrive-and-clear-key-mutants` (head 50e6db9a, counts 5876/377) CONFLICTS on `scripts/verify-expected-counts.json` (rc 1). #220 (41907572, 5870/377), #219 (9f998e9d, 5870/377) and NX-L `b1687/...` (700ed93a, 5870/377) merge clean and do not touch the counts file. | Order: this PR, then #219 and #220 (re-run checks; counts stay 5881/378 because neither adds tests), then NX-L (clean; count-neutral as committed), then NX-M last: merge main into it, resolve the counts file by REGENERATING with `npm run verify -- --maxWorkers=2 --update-counts` on the merged tree (expected 5887/378 = 5881 + its 6 cells, PREDICTED), never by hand. |
| F5 | Info (deploy) | The merge WILL start `deploy-demo.yml` (push to main; no changed path is in its paths-ignore: `.github/`, `scripts/`, `__tests__/` are not `**.md`, `docs/**` or `tests/**`). Its jobs are gated on `vars.CI_DEPLOY_ENABLED == 'true'`. The last 3 main runs (2de5e84, 751285a, e372068) concluded `skipped` (jobs build, deploy skipped). The variable itself is not readable with this identity (GET 404). | Landing pre-check as in landing.txt: deploy jobs must read skipped. |
| F6 | Info | Commit A says the audit "has failed on every run since 2026-11-17": true in UTC (first failure 2026-11-17T17 UTC, i.e. 18 Nov 04:xx Sydney; every run before succeeded). Builder and this gate ran Node 26.13 / npm 11.20 locally; CI uses Node 24 (hosted run on the head: success). | None. |
| F7 | Info | The workflow cell (11) does not pin the job id or name; the gate measured them unchanged (below). | Optional: add `audit:` / `name: audit-production-deps` to that cell next time. |

## Ruling-scope result (CHECK 1, 4)
- Card at source (`decision_queue.sh show`, READ verb only): `nexusai-picomatch-advisory-audit-1118`, client Datasec/NexusAI, title names NexusAI's production audit check, option a "Narrow, dated exception", detail "This advisory only, lapses 18 Dec or on a fix; gated and merged; then #219 and #220 land", ruled a 2026-11-18T08:36:26+11:00. Unlike the HPSM sibling (B1699 F1), the card names THIS repo and THIS audit: no authority gap.
- Entry at head: exactly one, frozen: GHSA-fc5q-39xc-vjpf / picomatch / `<=4.0.7` / lastDay 2026-12-18 / "the product owner's 2026-11-18 ruling". One advisory, one package, one range, one date; only the production audit step changes; no other workflow touched. Not wider than the card.
- Date: allowed through 23:59:59.999 18 Dec Sydney; fails from 00:00 19 Dec Sydney (Tuesday's reading). "Or on a fix": partially (F2).
- Phrase "the product owner's 2026-11-18 ruling" (5x in added lines, 1x in commit A message): true at source.

## Measured rows (this gate; node v26.13.0, npm 11.20.0; load1 6.2-7.0 at chain start, two reads 120 s apart)
| Check | Result |
|---|---|
| refs | ls-remote branch = 86ae678f... and main = 2de5e84c... at 10:28 and again at 11:14; ahead 2 behind 0; open PRs 219, 220 |
| diff | exactly 4 paths: npm-audit.yml +7 -12, test +139 -0, audit-prod.js +86 -0, counts +3 -3; K changes only the counts file |
| merge | `merge-tree --write-tree` clean, tree 9b52061e = head tree |
| other blobs | package.json, package-lock.json, jest.config.js, build.yml, deploy-demo.yml: same blob at base and head; no other `.github/` path changed |
| workflow (js-yaml, base vs head) | jobs `["audit"]` both; job name `audit-production-deps` both; 4 steps both; first 3 steps identical; `on` and `permissions` identical; audit step runs `npm audit --omit=dev --audit-level=moderate --json > audit.json`, `set -e`, `node scripts/audit-prod.js audit.json` last |
| step body under `bash --noprofile --norc -eo pipefail`, stub npm | real report rc 0; npm crash before any JSON rc 1; truncated JSON rc 1; npm error JSON rc 1; clean report rc 0 |
| real `npm audit` (npm ci at head) | npm rc 1; version 2; nodes fdir, node-gyp, picomatch, sqlite3, tinyglobby; metadata high 5 total 5; one advisory id |
| real step on it | rc 0, exactly 1 ALLOWED line, "production audit passed (1 allowed by a dated exception)" |
| plants on the REAL report (38 main() cases + 4 CLI) | second advisory other package high/moderate/critical rc 1 (low rc 0); second advisory on picomatch high/moderate rc 1; 4 different range texts rc 1; same id on another package rc 1; same id re-rated critical rc 0 (in scope); 18 Dec 00:00, 23:59, 23:59:59.999 Sydney rc 0; 19 Dec 00:00 Sydney rc 1; 2026-12-18T13:00Z (19 Dec Sydney) rc 1; 12:59:59Z rc 0; advisory gone rc 0 + NOTE; empty, garbage, null, [], 42, npm error, version 1/3/"2"/missing, vulnerabilities missing/null/string: all rc 1; CLI no arg, missing file, directory rc 1. 35 of 38 as expected; the 3 others are F1 (2 shapes) and F2 (fixAvailable) |
| new test file at head (red1, slot 8) | 11 of 11 green |
| red-first: EXCEPTIONS emptied | red cells [1,2,4,5,6,8,9,10] = the 8 predicted (STATUS half E) |
| red-first: base workflow | red [11] only |
| plant `>` -> `>=` | red [4] (matches STATUS Correction 1) |
| plant range compare dropped | red [6] |
| plant non-exception failures ignored | red [3,5,7,8,10] |
| full plain verify at head (clone, slot 4), ONE lock acquisition 10:49:11-11:14:04 | `VERDICT: PASS - 5881/5881 tests passed across 378 suites`, rc 0, = committed 5881/378; EADDRINUSE 0; porcelain 0 before and after; listeners in bands slot 4 and slot 8: 0 before and after |
| hosted | head check-runs: audit-production-deps completed success |
| scans, 235 added lines + both messages | names (13, underscore-aware, controls fire, `Kamera` does not): 0 except `Claude` in the two Co-Authored-By trailers; B-numbers, seat ids, card ids, Jira keys, IPv4, hosts, GUIDs, secret words: 0 (controls fire); "revision" pattern hit only `--audit-level`/`--update-counts` flags; non-ASCII 0, Cf/Cc 0 (U+202E control fires) |
| CodeQL hand rows | new RegExp / `\$&` / innerHTML / child_process / chmod / eval / skip-only on added lines: 0 |
| CodeQL CLI 2.27.4 `javascript-code-scanning.qls` over the 2 changed JS files | 0 results; control plant: js/incomplete-sanitization fired |
| live advisory 10:33 | high, `<= 4.0.7`, first_patched null, withdrawn null; npm picomatch latest 4.0.7 |

## Builder STATUS claims
True (re-measured): 4 paths and line counts; A/K split; base 2de5e84 unmoved; real npm rc 1 with one id and the exact ALLOWED line; planted lodash high/moderate rc 1, low rc 0; half E red set of 8 and half W red set [11]; P1 received [4] (Correction 1 is right); 5870/377 -> 5881/378 and plain verify PASS at K; other blobs unchanged; lint is a placeholder (Correction 4); hosted npm-audit success. False: none. Not shown by STATUS, now measured: job id/name unchanged, CodeQL CLI. Unmeasured by both: a real patched picomatch (F2).

## NOT RUN
Hosted Build, Gitleaks and CodeQL on a PR (no PR exists): hosted CI is the proof. Docker/database jobs: not run (the full jest verify ran). The real-clock lapse (injected clocks only).

## Calendar (CHECK 6)
On or before 2026-12-18 (Sydney): re-check the advisory (`first_patched_version`, `withdrawn_at`, range) and `npm view picomatch dist-tags`; if a fix exists, upgrade and remove the entry (with F1 and F3); if not, the production audit goes red again from 19 Dec unless the product owner gives a NEW ruling. Do not extend without one.
