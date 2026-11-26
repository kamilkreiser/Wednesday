GATE B2129: GO WITH FINDINGS
@ a38a078 on main e8d5f7f

Gate G1 (Opus), round 1 of 2, on lane 2 kit 1: RD-1023 (the SCIM audit entries record the full path) and RD-759's third shape (the CSP intake refuses a data: address holding an at-sign). Kit B2127, seat N180.

There is no Blocker and no Major. I found two Minor findings and six Info findings, and **none blocks landing**. Nothing I measured contradicts what the seat reported or what Tuesday's ANSWER-1 endorsed.

On point 2(a), the host form is not the only data: shape that still keeps an at-sign. An empty or unparseable authority does too: `data://@/a@b` answers `data:///a@b`, which has no host and keeps an `@`. That is wider than the corrected commit B message's wording (Minor 1). No form keeps a userinfo, and conforming browsers never send these values. The pull request's hosted build will be the first real Linux run (Q-8); a red on a new cell there is a fix round.

Re-measured 22:03 to 22:31 AEDT, 26 Nov, by `gh api -X GET` (the project's GH_CONFIG_DIR) and by my own runs:
- main = e8d5f7f1a6a78512a7ccfc41c691a60269f20049, the merge of records PR 264. BASE..main is `HISTORY.md` only, an allowed move by HOLD 20. The counts blob at main is 53b3bc45 (= BASE's).
- Branch `b2127/lane2-scim-csp` = a38a078aec721ad1adf01cb2e79b3120905d13f0.
  - Compare BASE...head: ahead 3, behind 0, six files: scimProvisioning.js 3/2, cspReport.js 3/0, the rd759-796 test 2/2, the rd1023 test 211/0 (added), the rd759 data test 98/0 (added), the counts file 3/3.
  - Compare main...head: ahead 3, behind 2, merge base e20b30cf.
- Open PRs 0. Open code-scanning alerts 22. Check-runs on the head: `audit-production-deps` success only (npm-audit runs on a push to any branch).
- Commits: A 9fc20e95 (parent BASE), B 86d22a99 (parent A), K a38a078a (parent B). Author and committer on all three: `88359143+kamilDatasec@users.noreply.github.com` on both sides.

## Measured by me (MEASURED) vs the seat's (RELAYED)
**Trees.** My clone (`git clone --no-checkout` of the seat's clone) is under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s331/g2129/clone`. It has four dot-free worktrees:
- `t/base`: BASE plus the two new test files and the turned rd759-796 file, copied from K (blobs f493c2ce, 6c69d0ae, 31e0de08);
- `t/head`, `t/mut` and `t/full`: all at K.

`node_modules` in each tree is a symlink to the seat's `npm ci` (disclosed). Each tree has 0 dot segments (control: the seat's `.tools/b2127/clone` reads 1). The slots are 17, 11, 7 and 15; each band had 0 listeners before and after (control: 15 listeners machine-wide). Node v24.22.2. The load was high at the start (load1 41 at 22:05, from an OXPd lab test process and securityd, not mine) and 9 to 13 during my runs.

**Jest lock.** I took two acquisitions:
- `g2129-lane`, 22:07:22 to 22:07:47;
- `g2129-full`, 22:07:47 to 22:30:49.

Both were acquired after 0 s and released, with `lock-wrapper rc=0`. `NODE_OPTIONS` was unset, and `MIN_TESTS`, `MIN_SUITES` and `VERIFY_EXPECTED_FILE` were unset for the verify. No jest ran outside the lock. Afterwards the lock base lists `queue-docker queue-jest released` (no holder), and no process of mine remains.

**(1) The diff, read whole.**
- scimProvisioning.js: one import line (`const { requestPath } = require('./accessAudit');`, line 36), and `path: req.path,` changed to `path: requestPath(req),` at both entries. The keys, the 401 and 429 answers and every other line are BASE's.
- cspReport.js: a two-line comment plus `if (u.protocol === 'data:' && p.includes('@')) return null;`, inserted after `if (u.host) return ...` and before the RD-735 hostless strip. Nothing is removed.
- rd759-796 test: exactly C-DATA's title and expectation.
- Counts file: `_updated`, `tests` and `suites` only.
- The only removed lines in the whole patch are those 7: the two `req.path` lines, C-DATA's 2 and the counts file's 3.

**(2) Red-first and green, both shapes.** My judge `gjudge.py` compares the exact set of failed cells from jest `--json`. The Linux shape is `TMPDIR=/tmp` with a persistent `RUNNER_TEMP`; the own shape is this shell's `/var/folders/...` TMPDIR, never unset.

| File | At BASE, both shapes | At K, both shapes |
|---|---|---|
| SCIM | 14 cells, 4 passed; failed exactly C1, F1 to F5, H1, L1, L2, L3 | 14 of 14 |
| CSP | 12 cells, 6 passed; failed exactly D1 to D5, S1 | 12 of 12 |
| rd759-796 | 20 cells, 19 passed; failed exactly C-DATA | 20 of 20 |

**(3) The eleven mutations, my own program** (`tools/gmut.py`, written independently with its own anchors; Linux shape). Each read red on EXACTLY the kit's named cells:

| Mutation | Red cells |
|---|---|
| scim-rate-relative | C1, L1 to L3 |
| scim-auth-relative | C1, F1 to F5, H1 |
| scim-original-url | C1, F3, F4 |
| scim-no-method | F1 to F5, T1 |
| scim-token-in-entry | T1 |
| csp-no-refusal | D1 to D5, S1 |
| csp-any-data | K1, L1, N1, S1 |
| csp-pct40-too | L1, S1 |
| csp-raw-text | K1, S1 |
| csp-case-sensitive | D2, S1 |
| csp-any-scheme | N2, S1 |

After every revert the two product blobs read b1783805 / ee880c97 (= K).

**Eight extra mutants of mine:**

| Mutant | Red cells |
|---|---|
| limiter entry reads `originalUrl` | C1, L3 |
| limiter entry drops `method` | L1 to L3, T1 |
| token material in the limiter entry | T1 |
| both entries read `req.baseUrl + req.path` | C1, F1, L1 |
| refusal answers `'data'` | D1 to D5, S1 |
| refusal answers `''` | D1 to D5, S1 |
| `csp-no-refusal`, run on the rd759-796 file | C-DATA |
| **refusal moved above the host branch** | **none** (Minor 2) |
| **refusal tested as `p.indexOf('@') > 0`** | **S1 only** (Minor 2) |

**(4) Does ANY SCIM entry still record a router-relative path, or carry a query, fragment or host? No.** My probe `adv/probe_scim.js` mounts the router as server.js does and drives 13 raw targets against both entries, at BASE and at K. At K every entry carries the mounted path as sent:
- `/SCIM/V2/Users` gives `/SCIM/V2/Users`;
- `/scim/v2//Users`, `/scim/v2/%2e%2e/Users`, `/scim/v2/./Users` and `/scim/v2/Users;jsessionid=abc` are recorded as sent;
- `/scim/v2?x=1` and `/scim/v2#f` give `/scim/v2`;
- `http://u:p@evil.example/scim/v2/Users?q#f` gives `/scim/v2/Users`;
- `HTTPS://EVIL.EXAMPLE:8443/scim/v2/Groups` gives `/scim/v2/Groups`;
- `DELETE /scim/v2/Users/abc?x` gives `/scim/v2/Users/abc`.

At BASE the same targets recorded `/Users`, `/`, `//Users`, and so on. `//scim/v2/Users` is not routed (404, no entry) at either.

**Does either entry gain token material? No.** The keys are exactly `path`, `method`, `ip` in every probe entry. T1 and my two token and method mutants pin this.

**(5) Is ANY data: address with NO host and a kept literal at-sign still kept? Yes, in one family** (Minor 1). My probe `adv/probe_csp.js` ran 41 shapes at BASE and K (`logs/probe_csp.txt`):
- An empty authority (`data://@/a@b`, `data://u:p@/a@b`, `data://u@/x@y`) and `data://h:99999@/a@b` fail `new URL`. The authority branch drops the userinfo and leaves `data:///a@b`: no host, an `@` kept. Given directly, `data:///a@b` answers null, so the function is not idempotent on these.
- Unparseable hosts (`data://[::1/a@b`, `data://h%zz/a@b`, `data://h h/a@b`) and the parsed host form (`data://h/a@b`, `DATA://h/a@b`, `Data://H/a@b`, a tab or NBSP variant) keep the `@` after the authority. This is Tuesday's named limit 3.
- In none of these does a userinfo survive.

**(6) Is ANY address the intake kept at BASE now refused or changed, beyond the property? No.** Of the 41 shapes, 8 change. Every one is a hostless `data:` value whose kept text holds a literal `@`:
- backslash forms `data:\\h\a@b`, `data:/\h/a@b`, `data:\/h/a@b` (a non-special scheme, so they are opaque paths);
- `data:@`, `data:@x`, `data:,a@b?c`;
- `data:text/html,<a href=mailto:x@y>`;
- `blob:data:,@`.

Other schemes are unchanged: `mailto:`, `foo:`, `https:`, `ws:`, `file:`, `about:`, `javascript:`, `blob:https:`. So are `%40`, `%2540`, a fullwidth at-sign and the `%3F`/`%23` cuts. The two landed shapes of PR 186 are unchanged: S1 counts their lines, and the rd759-796 file's E- and P- cells pass at K.

**The refusal is one line.** S1 reads `refusal: 1`, and the diff adds exactly one code line to cspReport.js.

**(7) The whole suite, once, by the project command** (`npm --prefix t/full run verify -- --maxWorkers=2`, committed counts, Linux shape, 22:07:47 to 22:30:49):
- `verify-suite: expectation — tests=6530 suites=411 (from scripts/verify-expected-counts.json)`
- `Test Suites: 411 passed, 411 total`; `Tests: 6530 passed, 6530 total`
- `VERDICT: PASS — 6530/6530 tests passed across 411 suites (jest exit 0)`
- `EADDRINUSE` 0 (control: `Tests:` 1). `FAIL ` lines 0 (control: `PASS ` lines 411). Porcelain after: 0.
- PASS lines for both new files, the turned rd759-796 file, and the neighbours: both SCIM files, RD-428's token file, RD-618, both RD-735 files, RD-802, RD-990, RD-1012 and RD-1013.

So the pair 6530 / 411 equals the project command's measured output. That is BASE's 6504 / 409 plus 26 tests and 2 suites.

**(8) gitleaks 8.30.1.**
- Control first, a planted synthetic AKIA key pair via stdin: rc 1, `leaks found: 1`.
- `git log -p BASE..K` (431 lines): rc 0, `no leaks found`.
- The three commit messages (24 lines): rc 0.
- My five landing texts: rc 0.

**(9) The word scan, as the kit runs it.** I used `scanlib1114.py` line 20's four plain names, extracted by program and never printed, with the underscore-aware pattern. Each name's `x_by_<name>_y` control fired.
- 320 added lines: 0 name hits, 0 build/seat/card/session-id hits (the kit's id regex; control fired), 0 skip/only/platform hits (control fired), 0 non-ASCII, 0 `/Volumes/`, 0 "product owner" or "ruling".
- Messages: 0 names, 0 ids, ASCII.
- pr-title and pr-body: 0 names, 0 ids, ASCII.

**RELAYED, not re-run:** the seat's local CodeQL (head 29 = base 29, KEPT 0, NEW 0, rc 0); its own-shape plain verify; its static2127 prints; its push.

## Tuesday's points
**(a) The host form.**
- **The seat's probe is confirmed.** `data://h/a@b` and `data://h:99999/a@b` are unchanged from BASE, and `data://u:p@h/x` answers `data://h/x`.
- **Other shapes that keep an at-sign after the hunk:**
  - an upper-case scheme with a host (`DATA://h/a@b` -> `data://h/a@b`; `Data://H/a@b` keeps `H`);
  - unparseable authorities: an invalid port, `data://[::1/a@b`, `%zz` or a space in the host, kept as sent;
  - **an empty authority, which comes out hostless** (`data://@/a@b` -> `data:///a@b`).
  - Backslashes do NOT keep one: `data:` is a non-special scheme, so `data:\\h\a@b` is an opaque path and is refused.
- **Real-world reach: none from a conforming browser.** CSP Level 3, section 5.4 "Strip URL for use in reports", step 1 reads "If url's scheme is not an HTTP(S) scheme, then return url's scheme". It applies to `blocked-uri` (5.2), `document-uri` and `source-file` (5.3). So a browser reports a data: violation as just `data` in all three fields; I read this at w3.org/TR/CSP3 (spec text, not a browser run). Every limit-3 value is a forged report, and no userinfo survives in any of them.
- **Does the committed text claim more than the code does?** Yes, in two places:
  - The hunk comment ("a data: address that keeps an "@" in its path is refused") is false for the whole authority family. It is owed, as ANSWER-1 records.
  - The corrected msg-B is right for the parsed host form. Its "a data: address with no host whose kept text ... holds an at-sign" is false for the empty-authority family, where the output has no host. Minor 1.

**(b) RD-1023: does the limiter's handler read the mounted path in every shape? Yes. It never falls back to `req.path`.**
- `requestPath` falls back only when `req.baseUrl` is empty.
- The router is mounted exactly once (`createScimRouter(` counts 1 in server.js, line 22446, under `app.use('/scim/v2',` at line 22444). Express sets `req.baseUrl` to the matched mount text for every middleware below it, the limiter's handler included.
- No line in server.js assigns `req.url`, `req.originalUrl` or `req.baseUrl` (a grep for those assignments reads 0; control: `req.url` itself appears once).
- Measured: across 13 targets, both entries at K begin with the mount as sent (`/scim/v2` or `/SCIM/V2`). L1 to L3 and H1 cover the real limiter and the real server.

**(c) Code scanning.** I read the SARIF of main's javascript-typescript analysis (id 2255623191 at e8d5f7f1, 29 results), with all primary, related and flow-step locations:
- 0 locations are in cspReport.js or accessAudit.js.
- 37 locations are in scimProvisioning.js, all belonging to one result: open alert **#235** (js/http-to-file-access, **medium**, primary `backend/jsonStorage.js:524`). They sit at BASE lines 92 (`writeUsers`) and 235 to 304 (the SCIM user write routes).
- **No location is on a changed line** (BASE 35-36, 120, 156).
- At K those lines move down by one (the import), and alerts match by fingerprint. The seat's local run read KEPT 0 / NEW 0.

The ruleset gates on `high_or_higher` and `errors`, and #235 is medium. **Info 3.** The PR's CodeQL run is the authority, and main's analysis at the merge commit is the check that can fail.

## Adversarial beyond the kit: three shapes outside each property
**(A), the SCIM entries:**
- (i) A mixed-case mount, double slashes, dot and encoded segments, and a matrix parameter. COVERED by the probe: recorded as sent, with the mount.
- (ii) Absolute-form targets with userinfo, a port or an upper-case scheme, and a query or fragment on the bare base path. COVERED: pathname only.
- (iii) A refused token with a body the parser refuses (`{bad`). NAMED LIMIT, pre-existing at BASE and K alike: `express.json` on the mount answers 400 before the router, so NO entry is written (Info 5, ticket candidate 2). Also: a percent-encoded `%3F` in the path is recorded with what follows it (RD-1012's rule; Info 6).

**(B), the data: refusal:**
- (i) The empty or unparseable authority family. NAMED LIMIT, wider than the named one (Minor 1).
- (ii) Backslash forms, `@` first in the kept text, and an `@` before a query. COVERED: all refused at K. But `@`-first is pinned by no cell (Minor 2).
- (iii) A fullwidth at-sign, a double-encoded `%2540`, and an `@` after an encoded `%3F`/`%23`. COVERED: kept as before, or cut. A literal at-sign only, Q-4.

Not covered: the real CSP route driven over HTTP (the cells call the module, and S2 counts the route's one call); the production setting; real Linux.

## Findings
1. **MINOR, does not block. The authority-form limit is wider than recorded, and it has a hostless member.**
   - `data://@/a@b`, `data://u:p@/a@b`, `data://u@/x@y` and `data://h:99999@/a@b` fail `new URL`. The authority branch drops the userinfo and returns `data:///a@b`: no host, and a literal `@` in the kept text. Passed through the function again, that output is refused.
   - Unparseable hosts (`[::1`, `%zz`, a space) keep the `@` too.
   - The corrected commit B message says the refusal covers "a data: address with no host whose kept text ... holds an at-sign", and names the host form as the exception. The empty-host output contradicts the first half.
   - No userinfo survives, and conforming browsers report `data` only (CSP3 section 5.4), so the exposure is nil. But C-261's text ("refuses data: addresses that carry an at-sign") is not fully met by the authority family.
   - pr-body and FOR-RECORDS name the family as limit 3. Ticket candidate 1.
2. **MINOR, does not block. Two properties of the refusal are pinned only by S1's source text, or by nothing:**
   - Its position below the host branch: moving the refusal ABOVE `if (u.host)` turns NO cell red. That change would close limit 3, but it shows that the authority-form behaviour, either way, is held by no cell.
   - That an `@` at the first position of the kept text is refused: a `p.indexOf('@') > 0` mutant turns only S1 red. No cell sends `data:@x`.
   - Today S1's exact text catches both edits. Once a later change rewrites the line, nothing behavioural holds them. A follow-up could add cells for `data:@x` (refused) and for the chosen authority-form answer.
3. **INFO. Code scanning (point c):** alert #235's data-flow path runs through scimProvisioning.js, but on none of the changed lines. If the PR's scan names #235 or any alert as new: no merge, read it, never dismiss.
4. **INFO. Owed wording:** the hunk comment (cspReport.js lines 97-98) is wider than the code, as ANSWER-1 records. The header of the rd759-796 test file (lines 11-12 and 18) still says the third shape is "HELD" and that C-DATA "records that it is unchanged". The seat found it, and the kit allowed only two lines of that file. Both are in FOR-RECORDS.
5. **INFO. Neighbour, predates this change:** a refused SCIM token with a body `express.json` refuses (malformed JSON, over 5 MB) writes no audit entry at all, because the mount's parser answers before the router. Measured at BASE and K. This is a gap in F-4's "every authentication failure is audited". Ticket candidate 2.
6. **INFO.** Both entries record percent-encoded text as sent (`/scim/v2/Users/%3Ftoken=1` is kept whole), per RD-1012's rule for the shared rows. A token placed in the PATH by a client is recorded, as `req.path` recorded it before, now with the mount prefix. This is not a regression.
7. **INFO. First real Linux run (Q-8).** My Linux-shape runs (the three files in the lane, and the whole suite at 6530 / 411) are the closest local proxy. The SCIM file's store folder comes from `persistentTempDir`, and H1 boots through `inventory.bootShape`, the same path as the hosted-green RD-1013 file. The CSP file has no platform premise. A red on a new cell there is a fix round.
8. **INFO. Records.** RD-1023's acceptance is fully met, so it moves to Testing under CLAUDE.md line 302. RD-759 can move to Testing once the authority-form follow-up is filed and linked, or stays open for it; that is the coordinator's choice. See FOR-RECORDS.md.

## Not run by the gate
CodeQL (relayed: the seat's local run); any hosted run (none exists for a pushed branch beyond npm-audit); real Linux or GNU userland; the production setting; the real CSP route over HTTP; any browser (the CSP3 reading is spec text); Jira (not read, not written); the seat's own-shape plain verify (mine was the Linux shape, which covers the counts predicate).

## Before landing (Tuesday)
1. Open the PR from `b2127/lane2-scim-csp` with `pr-title.txt` and `pr-body.md`.
2. Wait with `--min-checks 7`, including `build`, the FIRST Linux run. Its log must read `VERDICT: PASS — 6530/6530 tests passed across 411 suites`.
3. Land by a merge commit pinned to a38a078aec721ad1adf01cb2e79b3120905d13f0 (never squash or rebase, C-190), and never press "Update branch" (strict is false).
4. The Deploy demo run must read both jobs skipped; approve nothing (C-224).
5. Main's javascript-typescript analysis at the merge commit must read 29.

See landing.txt.

Files in this folder: VERDICT.md, landing.txt, pr-title.txt, pr-body.md, FOR-RECORDS.md.

Scratch (dot-free, left in place): /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s331/g2129/
- `clone/`, worktrees `t/{base,head,mut,full}`, `rt/`
- `adv/`: probe_scim.js, probe_csp.js
- `tools/`: gmut.py, gjudge.py, glane.sh, gfull.sh, runlane.sh, runfull.sh, gwords.py
- `logs/`: lane.out, full.out, full-verify-linux.log, per-run json and log, probe_scim.txt, probe_csp.txt, words.txt
- `out/`: main.sarif, alerts.json, mutsave (mutation backups), mutsave_anchorchk (the anchor dry-run's backups)
- `gl/`: gitleaks inputs and outputs

Nothing was written to the project checkout, Jira or GitHub. No PR and no push. Nothing deleted. No background process and no lock left.
