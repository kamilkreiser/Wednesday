# QA gate verdict - Secuura/Blockchain PRs #1734, #1735, #1736

- Tier 2, round 1 of 2. Gate model: Claude Sonnet 5.5 (claude-sonnet-5-5). Date 2026-10-27.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-t4s4-1027/` (clone in `repo/`, raw logs beside it, private `TMPDIR=/tmp/gt4s4`).
- Pushed / merged / commented / edited a ticket: nothing. Node v26.8.1, npm 11.19.0 (the seats' versions).

## BLUF
| PR | Verdict | Worst finding |
|---|---|---|
| #1734 KS-1589 A (Seat T 4th) | GO WITH NOTES | LOW: the AST guard has three reachable blind spots it does not claim to close (namespace/member call `api.fetchApiKeys('x' \|\| 'y')`, bracket call, a bare `undefined`/`null` passed as the id). All five survivors and every previously-killed mutant I ran behave as claimed. |
| #1735 KS-1752 (Seat S 4th) | GO | INFO: wording-only as claimed; the U2 cell title changed (no other file references the old title). Every number and the ordering claim reproduced. |
| #1736 KS-1505 p1 (Seat T 4th) | GO | INFO: comment-only proven with my own token instrument, with four controls that can fail. Net line delta zero; the cited line numbers are intact. |

Merge: all 15 orders (3 singles, 6 pairs, 6 triples) merge cleanly; every order of the same set gives one tree. Triples all give `9067af19644180bd046a75baf8faba67acfb243d`.

## Pins (start = end)
```
c3eb63c9d23b08132482f3211dbf8755312a7ca0  refs/heads/develop
b6c678248c98d55f935add0fb3f6a563a0749e5f  refs/pull/1734/head
336143384d329c33bbe116097a0bc58d6302717c  refs/pull/1735/head
b627c7e222280b8e16f688236053b695e77f8a57  refs/pull/1736/head
```
`lsremote_start.txt` (taken at my start) and `lsremote_end.txt` saved in the workspace; `diff` is empty (rc 0). They equal the briefed pins. All three PRs have merge-base = develop c3eb63c9. `gh api user --jq .login` = `kksecura`; PR bodies/files read through `gh` (read-only). Deps: `npm ci --ignore-scripts` (rc 0, workspace-local npm cache), `npm run build --workspace=packages/shared` (rc 0).

## #1734 KS-1589 item A

**FOUND**
- Exactly 3 files, 401+/69-: the ks1564 test, and the two Projects Documents HTML docs (+15 and +21, numstat deletions 0 for both). No product file touched. PR body states the escape clause does NOT apply and both docs are updated in the same commit; consistent with the diff.
- Docs: `git diff -U0` has one hunk per doc, no `-` line (so no existing line changed, appended only). Tag-count balance per tag name, whole file, develop vs head: both imbalance sets empty for both files.
- The guard reads the TS AST (`ts.createSourceFile` with setParentNodes, TSX kind by extension). `KS1564_ADMIN_SRC` override added; cell 0b asserts the default tree when unset.
- Cells: 13 (0, 0b, 1-7, C1-C4). Claim "9 -> 13" holds.

**TESTED / HOW**
- `packages/shared` vitest, whole package, at develop: 1 failed / 1034 passed (1035), 53 passed + 1 failed of 54 files. At #1734: 1 failed / 1038 passed (1039), same file counts. The one failure is `wallet-signature.test.ts > accepts a valid wallet signature over the message` on both sides. Ratio and delta (+4 cells) equal the claim. N/N ran (all 54 files executed).
- Mutants on COPIES of `frontend/admin/src` (taken with `git archive` of develop into `admin_base/`, copied per mutant to `/tmp/gt4s4/m_<name>`), `KS1564_ADMIN_SRC` pointing at the copy, every anchor asserted to occur exactly once, tree sha256 taken before/after (script `mut.py`, per-mutant logs `mut_*.log`, summary `mut_summary.txt`). Clean control (no change) 13/13, sha unchanged `8f9f88657...`.

  | mutant (my construction; the ticket text is the spec) | copy sha before -> after | result | red cell |
  |---|---|---|---|
  | N3 race-guard line commented out (ApiKeys.tsx:138) | 8f9f8865 -> a723f8ad | 12/13, rc 1 | 5 only |
  | N6b `void fetchApiKeys(String(orgId) \|\| ['default','org'].join('-'))` beside the plain call | -> da64c6ff | 12/13 | 4 only |
  | N7 `const f = fetchApiKeys; void f('x')` | -> f2538d03 | 12/13 | 4 only |
  | N9 orgs-loader guard line deleted (:111) | -> 806e6392 | 12/13 | 6 only |
  | N10 `submitRef` check and set deleted | -> 5f25a12c | 12/13 | 7 only |
  | N10 variant: only the check removed | -> 9a9a4d27 | 12/13 | 7 only |
  | prev-killed: placeholder literal in a stray file (N1-class) | -> 423f16d6 | 12/13 | 1 |
  | prev-killed: createApiKey `organizationId: 'x'` (N2-class) | -> f798ee86 | 12/13 | 3 |
  | prev-killed: `fetchApiKeys(orgId \|\| 'x')` (N4-class) | -> eec9b470 | 12/13 | 4 |
  | prev-killed: `fetchApiKeys(orgId ?? 'x')` (N5-class) | -> 8e18d7ff | 12/13 | 4 |
  | prev-killed: `organizationId?: string` in api.ts (N12-class) | -> e047831e | 12/13 | 2 |
  | CONTROL comment-only (`// fetchApiKeys(orgId \|\| 'x')`, `/* const f = fetchApiKeys; */`) | -> d6c4707f | 13/13, rc 0 | none (green, as the claimed N8 departure) |

  Each of the five claimed survivors is red on the cell the PR names. Previously-killed shapes stay red on the cells named. I did not have the original N1/N2/N4/N5/N11/N12 diffs, only the ticket's descriptions, so those six rows are my own reconstructions of the shapes, not the seat's exact copies; I did not run an N11 at all (the PR table gives it cell 4). This is a weaker proof than the seat's for those, stated plainly.
- Vacuity probes on the guard (each also on a copy):
  - Parse failure as "no calls": an unterminated template literal swallowing `loadKeys` -> 4 failed (3, 4, 5, 7). Loader-not-found is a red (`found` asserted true), and `calls.length > 0` backs cell 4. Not vacuous on that path.
  - A file with conflict markers plus `fetchApiKeys('x')`: red (cell 4). A garbage line before an import, or garbage inside `loadKeys`: still green 13/13, because the TS parser recovers and the checks still ran on real nodes (not vacuous; the guard still sees the loader).
  - Alias exported in a `.tsx` array (`[fetchApiKeys]`): red (value use).
  - **GREEN, not caught (the blind spots):** `api.fetchApiKeys('x' \|\| 'y')` through a namespace import (the checker excludes property-access names by design, "someone else's .fetchApiKeys"); `(api as any)['fetchApiKeys']('x')` (a string, not an identifier); `fetchApiKeys(undefined)` (the `PLAIN_IDENTIFIER` regex accepts `undefined`/`null`); an alias in a `.js` file (walker takes only .ts/.tsx; none exist in the tree today). The file header says it refuses "expressions at the call sites, not provenance"; it does not list these. The current page imports by name, so none is live today.
- Not run by me: the seat's lint (rc 1 before/after on `no-control-regex`) and its standalone type-check of this file (nothing in the repo type-checks it; the PR says so). See NOT TESTED.

**SEVERITIES**
- LOW: the three blind spots above (namespace/member call, bracket call, `undefined`/`null` as the argument). The ticket's five survivors are closed; these are adjacent shapes. Worth a follow-up line, not a blocker.
- INFO: cell 2 still reads `api.ts` by regex (text), so a signature quoted in a comment next to a changed real signature could confuse it. It was already so before, and is not among the claimed items.
- INFO: N8 deliberately green (comment quoting a bad call), confirmed by my comment-only control. Accepted by Wednesday.
- No MAJOR or MINOR.

## #1735 KS-1752

**FOUND**
- Exactly 1 file, 32+/10-. The diff touches the header comment, the U2 title string, an inline comment, and the assertion message string. The `expect([...r.authedMethods], ...).toEqual([])` call and the preceding `op.security` assertion are unchanged apart from the message text. No source, spec or yaml.
- Ordering: at the PR head `index.ts:837` = `app.use(createHealthRoutes(services, redisService));`, `index.ts:1054` = the `app.use((req,res,next) => {` of the spec gate (`resolveSpecRoute` at :1064, method gate :1070, auth gate :1084), and `services/health.ts:42` = `router.get('/api/connector/info', authenticateToken(true), ...`. 837 < 1054, as claimed.
- Two-doc escape clause: stated explicitly in the PR body (section on the two `.html` docs), with reason and "cell count unchanged at 7".
- The only other occurrence of the old cell title text is the file itself (git grep of "KS-1531 U2" on the head: 1 hit), so renaming the title strands no reference.

**TESTED / HOW** (`bash m1735.sh`, tracked spec edited in my clone and restored by `git checkout --`; HEAD spec blob sha256 `77ef8aa70f2e`, restored sha `77ef8aa70f2e`, `git status` clean after)
- ks1531 at the head: 7/7 passed. Whole api-gateway suite: develop 123 files / 1203 tests passed (rc 0); #1735 123 / 1203 (rc 0). 123/123 files ran both sides.
- `connectorApiKey` -> `bearerAuth` (one line; spec sha `77ef8aa7` -> `81770577`, matching the PR body):
  - head test file: 1 failed / 6 passed, the failing cell is U2 alone (order: ctrl, U1, U2, ctrl, R1, R2, ctrl; only the 3rd is red); R1 and R2 green. The failure is the `op.security` assertion (`expected [ { bearerAuth: [] } ] to deeply equal [ { connectorApiKey: [] } ]`), as the PR says.
  - pre-edit (develop) test file on the same mutant: same 1 / 6, U2 alone. Same ratio before and after.
- `get:` -> `post:` for this path (spec sha `d7fab3521` matching the PR): 3 failed / 4 passed = U1, U2, R1 red, **R2 green**. That is the PR's "R1 goes red while R2 stays green"; U1 and U2 are red too, and the PR's "3 failed / 4 passed" says so.
- `npm run check:test-types` at the head: rc 0. api-gateway: 158 files examined, 123 under `__tests__`, 27 errors, 27 in baseline, 0 new, 0 stale. Other four services 0 new, 0 stale. Equals the claim.

**NOT TESTED**: the sibling-path `/api/connector/{segment}` union mutant (the PR's sharper mutant that fires exactly the reworded message); the mid-run `Hook timed out` flake in the PR's honest notes (I saw no timeout in my 3 runs of the suite plus 3 file runs); the claim that the R2 title cannot discriminate authenticators (reasoning); `check:test-types` was not run at develop (baselines are tracked at HEAD, so 0 new is itself the comparison, as the PR says).

**SEVERITIES**: INFO only. The PR is honest about preflight 13/16 and quotes it as not a pass.

## #1736 KS-1505 part 1

**FOUND**
- 1 file, 21+/21-, three hunks (`@@ -618,5 +618,4`, `-624,6 +623,10`, `-635,10 +638,7`), all inside the hot-reload comment block. Every `+`/`-` line is a `//` comment (44 `[-+]` lines incl. 2 file headers; excluding headers 42, non-comment 0).
- The cited line numbers still hold: lines 837, 856, 872, 1021, 1041 of `index.ts` are byte-identical (md5 of the five lines equal) between develop and the head, so `routes/admin.ts:539` and the two docs' citations are not stale.
- Content spot checks: `scripts/generate-openapi.ts:273` is `fs.writeFileSync(OUT_PATH, newYaml, 'utf8');` and it is the only `writeFileSync` in that script, matching the comment. The node 24 / KS 659 closed/archived claims are about Linear and Seat D's measurement; I did not re-verify them (not checkable from the repo).
- Two-doc escape clause stated in the PR body (reason: not a test change, no doc figure moves).

**TESTED / HOW**
- api-gateway vitest at develop 123 files / 1203 passed, at #1736 123 / 1203 passed (rc 0 both). 123/123 ran.
- My own instrument (`tok.cjs`): TypeScript scanner token stream (trivia skipped) of `index.ts` at develop vs head: 3773 tokens each, hash `c261808b6b7f` both, equal; newline count 1292 both.
- Controls, run in the same invocation: tamper one identifier at a line start (`app.use(` -> `app.usf(`) -> hash differs (false, as required); a comment edit -> hash equal (true, as required); tamper inside a string literal -> differs; turn an `import` line into a comment -> differs. Token count > 1000 asserted so an empty read cannot pass.
- The instrument differs from the seat's esbuild emit (different tool, same question), so the two are independent.

**NOT TESTED**: no container, no rsync, no node-24 behaviour (the PR does not claim them); the Linear states of KS 659/656/987/1505.

**SEVERITIES**: INFO only.

## Merge order (my clone only: `git merge-tree --write-tree` chained with `commit-tree`, no working tree; rc 0 at every step)
| order | tree |
|---|---|
| develop + #1734 | eef07f138db95375d23783cbf2eb719f3edca767 |
| develop + #1735 | 87fd162a49680f10d9b5fcd24494305dc33bb8ee |
| develop + #1736 | 55cf6add84d377188592006e62d5d86b0b440fb9 |
| 1734,1735 = 1735,1734 | 1603e63d2c0cf618055734d25b5ebb8966b2d9f4 |
| 1734,1736 = 1736,1734 | 2227c7769354ba96dd903fe7d5d67f81bb6e7824 |
| 1735,1736 = 1736,1735 | 6940c1932c6241ccc41be87e59a52f90b27f0b69 |
| all six triple orders | 9067af19644180bd046a75baf8faba67acfb243d |
No conflicts. The three PRs touch disjoint files (ks1564 test + 2 docs / ks1531 test / index.ts). Output in `merge_out.txt`.

## What I did NOT test
- `packages/shared` lint and the separate type-check of the ks1564 file (PR claims rc 1 pre-existing / rc 0); `walkTimeouts.test.ts` ran inside the whole-package run and passed (no failure beyond wallet-signature), but I did not read it individually.
- The four platform suites, push-gate preflight legs and the shell runner (the PRs themselves do not claim them).
- No browser behaviour (tier 2); item C of KS-1589.
- The ticket's own N-labels beyond the description text (see #1734).
- The node 26 / cbor cause of the wallet-signature failure (I only confirmed it is red identically on both sides).

## My instrument errors
1. First `tok.cjs` run: the identifier-tamper control tampered the first `app.use(` which sits in a comment, so the control did not discriminate (printed "equal? true"). I fixed it to the first line-start `app.use(` and re-ran; the result above is the fixed run.
2. My mutant harness's first "RED=" column printed the test file name instead of the cell (a regex error). I re-read the cell names from the saved logs, and I patched the regex for the last two probes; all cell attributions above come from the logs.
3. The fleet hooks refused a few of my commands (a `cd`, a `git -C $VAR checkout` write verb with a variable path, an unquoted `======`, a `$G` multi-word variable). I re-issued with literal paths, in `bash` heredocs, or in script files; no effect on results.
4. The "garbled page" probe I first wrote (garbage inside `loadKeys`) stayed green because TS recovers; I did not count it as a vacuity finding and added the unterminated-template probe, which does red.

## Files outside the workspace
None written. All writes are in the workspace, `/tmp/gt4s4` (the private TMPDIR the brief required; mutant copies and vitest scratch), and this verdict folder `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_gate-t4s4-batch/`. `git status` in the cache `src` clone is empty; `find /Volumes/DevMASTER/WEDNESDAY -maxdepth 1 -newer lsremote_start.txt` lists only `.git`; no file in the WEDNESDAY root. The clone is `--shared`, its objects live in my clone. The cache `src` deploy key was used only for `ls-remote` and a fetch of the pinned refs.
