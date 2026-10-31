## QA GATE 63, TIER 2, ROUND 1: KS-1868 PR 4 of 4, Secuura/Distributed_Secuura #1872 (mcp-server)

Gate commissioned by Wednesday, Sun 1 Nov 2026. Findings only: nothing fixed, pushed, commented, merged or mailed; no Linear ticket touched; the Secuura repo was only fetched and read (one read-only GET of the PR JSON/body and the open-PR file lists with the repo's own token; the token was not written anywhere). Evidence root: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate63-ks1868-pr4-1872/evidence/` (called `evidence/` below).

### BLUF

#1872 does what it says and nothing more. The one product change is an inner `try`/`catch` around the existing read of the thrown value in the `secuura_hash_document` catch, with the constant fallback `unreadable thrown value`; +6/-1 in `hash.ts`, one new test file (+67), two new docs fragments. The PR's added product and test lines are byte-identical to the held Spark patch (no hand edit, as claimed). Both red cells fail at the merge-base product code for the product reason (the handler rejects: `expected undefined to be true`) and all 3 pass at head. mcp-server suite: 7 files / 33 pass at head and on a scratch merge with current develop. 9 of 10 of my mutants were killed; one survived (G63-F1). Merge onto current develop is clean (rc 0), the PR touches only its own 4 files, and no open PR shares a path. The stated KS-1893 limit is accurate. Three things to know, none blocking:

- **The cells do not pin the non-Error arm** (`String(err)` for a thrown string/null/undefined/symbol): changing it to a constant survives (G63-F1).
- **The guard covers a read that THROWS, not a read that returns a hostile non-string.** An Error whose `message` getter returns a BigInt, or an object with a throwing `toJSON`, still makes the handler reject (the `JSON.stringify` is outside the guard); a getter returning `42` puts the number `42` in `error`. This is the G60-F1 class again, not a regression (base rejects earlier) (G63-F2).
- **The mcp-server `tsc` does not compile the test file** (`tsconfig` excludes `src/__tests__`), so the "tsc rc 0" in the PR body needs the test-in-program form to mean what it says; I ran that form and it is rc 0 (G63-F3, file-only).

### Heads

| Ref | At start (2026-11-01 02:22 AEDT) | At end (02:33 AEDT) |
|---|---|---|
| PR #1872 head | `55eb1114105d1f945043729e363d421c1c315b3b` | `55eb1114105d1f945043729e363d421c1c315b3b` |
| develop | `b4ec1f0603206b01e40c1eb349fe11d6bc031a09` | `b4ec1f0603206b01e40c1eb349fe11d6bc031a09` |

Merge-base of head and develop: `ddc644fb4869e615e3f3fc68480e60410dcfebcf` (one commit on it: `55eb1114`). `evidence/heads_start.txt`, `evidence/heads_end.txt`. GitHub reports the PR open, base `develop`, mergeable true / state `unstable`, 4 files, +111/-1 (`evidence/pr1872.json`). No head moved; no stop.

### VERDICT: **GO WITH NOTES**

Notes are G63-F1 and G63-F2; neither is fix-before-merge. (The two pre-merge boxes and the three human sign-off boxes are deliberately unticked in the body, and the body says so; not mine to tick.)

### Findings

| ID | Severity | Finding | Evidence |
|---|---|---|---|
| G63-F1 | minor | Mutant M10 (the non-Error arm `String(err)` replaced by the constant `'unreadable thrown value'`) SURVIVES. No cell throws a string/null/undefined/symbol, so the readable non-Error path of the new expression is unpinned (C1 pins the Error arm; R1/R2 pin the fallback). Probe shows head returns `plain string`, `null`, `undefined`, `Symbol(s)` for those, unchanged from base. Behaviour is right; it is just not held by a test. | `evidence/mutants.txt`, `evidence/own/probe_shapes.txt` |
| G63-F2 | minor | The inner try protects a THROWING read only. Error with `message` getter returning `10n` (BigInt) or `{toJSON(){throw}}` -> the handler still REJECTS (JSON.stringify of the result is outside the guard); getter returning `42` -> `{"success":false,"error":42}`. Same class as G60-F1 / the ticket's gate-36 text. Not claimed by the PR (it names revoked Proxy and throwing getter); not a regression. | `evidence/own/probe_shapes.txt` |
| G63-F3 | file-only | The service `tsconfig.json` has `"exclude": [..., "src/__tests__"]`, so `tsc -p services/mcp-server` (rc 0 here, `evidence/own/tsc_head.log`, `tsc_merge.log`) never compiles the new test. The body says "tsc --noEmit with the test file in the program ... 0 errors; a planted type error reported as TS2322": true when the program is built that way. I built it (scratch tsconfig extending the service one, include `src/**/*`): rc 0; a planted `const planted: number = "x"` in the test: rc 2, TS2322. Leg 16 (test-types) does not cover mcp-server (the body says so). | `evidence/own/tsc_with_tests.log`, `tsc_planted.log` |
| G63-F4 | file-only | Body/fragment say "9 same-shape reads in `src/tools` ... not touched". My grep of `err instanceof Error ? err.message : String(err)` at head: hash.ts 1 (the one this PR guards, still in its ternary), info.ts 3, register.ts 2, verify.ts 3 = 9 including the changed site; the untouched count is 8. (http-server.ts has 12 more: 21 in the service, matching the ticket.) Declared as a grep, count off by the changed site. | `evidence/q1_grep_same_shape.txt` |
| G63-F5 | file-only | PR 1850 (another seat's, open, mcp-server `http-server.ts` plus two ks1410 tests) is file-disjoint from #1872 as stated, but 1850 does not merge with current develop on its own (rc 1, conflicts in two `Projects Documents/*.html` pages), so `merge-tree 1850 1872` also reports rc 1 and the conflicts are 1850's, not #1872's. Whoever merges 1850 owns that. | `evidence/q4_merge_develop_1850.txt`, `q4_merge_1850_1872.txt` |

No fix-before-merge finding.

### Q1. What exactly does the PR change?

- **FOUND:** four files, `git diff --stat ddc644fb4869 refs/pr/1872` and GitHub agree (4 files, +111/-1): `Blockchain/Dev/services/mcp-server/src/tools/hash.ts` (+6/-1), `.../src/__tests__/ks1868-hash-tool-unreadable-throw.test.ts` (+67, new), `Projects Documents/fragments/{cheat,flow}/KS-1868-mcp-server-unreadable-thrown-value.html` (new). Read the whole diff (`evidence/pr.diff`).
- Product hunk: `const message = err instanceof Error ? err.message : String(err);` becomes `let message: string; try { message = <same expression>; } catch { message = 'unreadable thrown value'; }`. Nothing else in the file moves; no package.json, lockfile or config touched.
- Matches the body and the ticket item (one site of 253; ticket stays open; fallback constant `unreadable thrown value`; the body's own "what this does not prove" list).
- **Provenance claim checked:** the added lines of `hash.ts` (6) and the test (67) in the PR are identical, line for line, to the held Spark patch `.../runs/spark_secuura_2026-10-31_ks_1868_o36_p2_mcp_server_hash_tool_unreadable_throw/out.md.checker/patch.diff` (sha256 begins `66cc843b83c486f7`, as the body quotes). So "no hand edit" holds for the code.
- **MCP client behaviour:** for every readable thrown value the tool result is byte-identical to base (probe: Error, string, null, undefined, symbol all give the same `{"success":false,"error":...}`, `isError:true`). It changes only for an unreadable thrown value, where base made the handler reject and head returns `{"success":false,"error":"unreadable thrown value"}` with `isError:true`. A planted `stack` of `STACKSECRET` was not returned. The tool is registered on the stdio server only (`index.ts:14`; `registerHashTools` has no other caller), as stated. No other client-visible string changes.

### Q2. Tests: red at base for the product reason, green at head

| Run | Result |
|---|---|
| Head, new file | 3 of 3 pass |
| Merge-base `hash.ts` (`ddc644fb4869`) + head test, my own run | 2 failed / 1 passed: R1 and R2 `AssertionError: expected undefined to be true` at `expect(r?.isError).toBe(true)`; C1 passes |
| Same via the Spark harness (`evidence/spark/facts.json`) | head 3 pass / 0 fail; base product code 1 pass / 2 fail |
| Whole mcp-server suite at head | 7 files / 33 pass |
| Whole suite on scratch merge of head with develop `b4ec1f060320` (commit `d47b9fd8a9f1`, fresh `npm ci --ignore-scripts`, shared built) | 7 files / 33 pass |

"For the product reason": `r?.isError` is `undefined` only when `runHashTool()` resolves to `undefined`, i.e. the handler REJECTED and the test helper's `.catch(() => undefined)` swallowed it. C1 (an ordinary Error) passes at base in the same file, so the import, mock and server stub work: the red is not a setup or typo error. The helper's swallow is declared by its doc comment. The mock is a plain function (not `vi.fn()`) so a spy cannot itself throw on the revoked Proxy; that reasoning is sound and mutant M5 (inner catch rethrows) is killed.
Logs: `evidence/own/base_red.log`, `full_head.log`, `full_merge.log`. Counts match the body (6 files / 30 on develop, 7 / 33 with the change). The body's own 33 figure is 1 file + 3 cells over its base.

### Q3. Mutants (my own, applied to head `hash.ts` by unique anchor, restored and verified by sha256 each time)

Script `evidence/mutants.py`, output `evidence/mutants.txt` (every anchor matched exactly once; `restore_sha_ok=True` on all 10; head file sha256 `cfc06f6f4b83...d9a2` re-checked after, `git status` clean of tracked changes).

| # | Mutant | Result |
|---|---|---|
| M1 | fallback string changed | KILLED (R1, R2) |
| M2 | fallback re-reads `err.message` | KILLED (R1, R2) |
| M3 | read is `String(err)` only | KILLED (C1) |
| M4 | ternary arms swapped | KILLED (C1) |
| M5 | inner catch rethrows | KILLED (R1, R2) |
| M6 | `isError: true` dropped from the error result | KILLED (all 3) |
| M7 | fallback leaks the error's stack | KILLED (R1, R2) |
| M8 | fallback is empty string | KILLED (R1, R2) |
| M9 | `success` flag flipped in the error body | KILLED (all 3) |
| M10 | non-Error arm returns the constant instead of `String(err)` | **SURVIVED** (G63-F1) |

Plus the base-product run above (inner try removed) = killed by R1, R2. 9 killed, 1 survived, 10 applied.

### Q4. Scope and merge

- Changed files = exactly the 4 above (`git diff --name-only origin/develop...refs/pr/1872`, `evidence/q4_files.txt`). Control for the detector: against its own list it reports all 4.
- `git merge-tree --write-tree origin/develop refs/pr/1872`: **rc 0**, tree `7b7087b2c519`, no conflict (`evidence/q4_merge_tree.txt`). develop has changed 128 files since the merge-base, none in mcp-server (`git diff --stat ddc644fb4869 origin/develop -- services/mcp-server` empty). Positive control: a commit on the merge-base editing the same line of `hash.ts` merged against the PR returns **rc 1** with three unmerged stages (`evidence/q4_merge_control.txt`).
- Open PRs: 32 listed (REST, 4 pages of 100, includes #1872). **Exact-path overlap: none.** Same-service neighbour: only #1850 (`http-server.ts` + two ks1410 tests), file-disjoint (G63-F5).
- `tsc`: `tsc --noEmit -p services/mcp-server` **rc 0** at head and on the merge (`evidence/own/tsc_head.log`, `tsc_merge.log`). That program excludes the tests (G63-F3); with tests in the program rc 0, with a planted type error rc 2 (TS2322).

### Q5. Is the stated KS-1893 limit accurate?

**Yes.** The catch at head (`hash.ts:33-44`) still builds `JSON.stringify({ success: false, error: message })` from `err.message` (or `String(err)`) and returns it with `isError: true`. `hashFile` is `readFile(filePath)`, so a real failure returns Node's text, which for a missing file includes the requested path (`ENOENT: no such file or directory, open '<path>'`). C1 pins that the message is returned (`{success:false,error:'disk gone'}`), and probe rows show strings and Error messages returned verbatim. The PR changes none of this, says so in the body and both fragments, and names KS 1893 (the MCP side) and KS 1410 (the REST side, #1850's file, `http-server.ts`). Accurate, and correctly out of scope.

### COUNTS

| Measure | Value |
|---|---|
| Files changed | 4 (+111/-1) |
| New cells | 3 (C1, R1, R2); R1, R2 red at base |
| mcp-server suite at head / on scratch merge | 7 files / 33 pass / 33 pass |
| Mutants | 10 (9 killed, 1 survived) |
| Probe shapes run through the real handler | 10 (3 notable: BigInt message, throwing-toJSON message -> reject; numeric message -> number) |
| Open PRs scanned | 32; exact overlap 0; same-service 1 (#1850) |
| Findings | 5 (0 major, 2 minor, 3 file-only) |
| tsc | service config rc 0; with tests in program rc 0; planted rc 2 |

### SPARK SHADOW AND CALIBRATION

Deterministic half: `spark_gate.sh <clone> 1872 55eb1114105d1f945043729e363d421c1c315b3b develop <test file> --node-modules <complete hoisted tree> --work <scratchpad>/gate63_spark --out evidence/spark` (new work dir; rc 0, 23 s). **Did BASE really differ from HEAD? Yes.** I passed the branch name `develop`, not a sha, so the known `merge-base <head> origin/<base-ref>` defect did not bite: `facts.json` merge_base `ddc644fb4869e615e3f3fc68480e60410dcfebcf`, head `55eb1114105d1f945043729e363d421c1c315b3b`, head_mode `tip`, and the base run really failed (1 pass / 2 fail) where head passed 3 / 0, with the product file swapped back to merge-base (`diff.patch` shows the 4-file diff). Totals identical to my own run.
LLM half: `spark_review.py` with `--facts --diff --ticket KS-1868 --pr-body-file` (valid, schema clean, attempt 1, 36 s). Raw: `evidence/spark/review/review.json`. **Spark verdict: GO WITH NOTES, 5 findings, all severity Note, 0 Major, 0 Minor.**

| Spark finding | Mine | Calibration |
|---|---|---|
| S1 fixes 1 of 253 sites; ticket stays open | Same, declared | Agree (non-issue) |
| S2 root cause (revoked Proxy / throwing getter) unmeasured on a real path; ticket says none known | Same; I measured the synthetic shapes through the real handler | Agree (its `evidence_quote_found_in_input: false`: quote not literally in its input, claim still true) |
| S3 base red is behavioural: handler rejects, control passes | My Q2, same figures | Agree |
| S4 duck-typed server is more permissive than the real McpServer | True but the test only needs the handler; the registration shape is not under test | Agree as a note (quote not found in input flagged by the script) |
| S5 "stdio only" is a grep claim, not measured | I checked: `registerHashTools` called only at `index.ts:14` | Agree it was unmeasured; claim holds |
| (not raised) | G63-F1 mutant M10 survives, non-Error arm unpinned | **Spark missed** |
| (not raised) | G63-F2 BigInt / throwing-toJSON message still rejects | **Spark missed** (same as it missed G60-F1) |
| (not raised) | G63-F4 "9" vs 8 untouched same-shape reads | **Spark missed** |
| (not raised) | G63-F3 tsconfig excludes tests | **Spark missed** |

Spark false positives: 0 of 5 (two of its quotes were flagged not-found-in-input by the script's own check, but the claims are true). Spark verdict equals mine. Calibration: Spark is reliable on declared-scope and measured-vs-claimed notes and blind to everything that needs running a mutant or a probe; it found none of my four.

### UNMEASURED

- The four platform suites (Schemathesis, Akto, Playwright, Performance/k6), a running stack, a real MCP client attached to the tool, any deploy (the body lists these as not run; the two pre-merge boxes stay unticked by design).
- The pre-push hook (16 legs) and its quoted verdict: not re-run; the body's figures are the author's.
- `docs-fragments.mjs check`: not run (the sparse tree lacks `scripts/`); I read both fragments (tables only, the claims match the measured figures) and did not run the checker.
- eslint on the two files: not re-run.
- Node LTS / Node 24: this host runs the non-LTS line the author used.
- A real path that throws an unreadable value into this tool (the ticket says none is known; synthetic only).
- The real `McpServer.tool` registration and the real `@modelcontextprotocol/sdk` result serialisation (test uses a duck-typed server).
- Whether #1850 or any later PR will conflict with this one after other merges (only a point-in-time merge-tree on `b4ec1f060320`).
- The exact content of the Spark brief `READY_KS-1868-...` file (I compared the canonical `patch.diff`, not the brief).

### HOW

- **Clone:** `evidence/..` parent folder `repo`, new path, `git clone --filter=blob:none --no-checkout` via the Secuura deploy key (`GIT_SSH_COMMAND` with `IdentitiesOnly`), then `git -C <dir> rev-parse --show-toplevel` asserted equal to the dir before any fetch; `core.sshCommand` set repo-locally so partial-clone blob fetches work. Fetched `refs/pull/1872/head` (and 1850's) only; no push.
- **Worktrees** under `wt/`: `wt/head` (head, sparse cone `Blockchain/Dev` + `Projects Documents/fragments`) and `wt/merge` (scratch merge commit `d47b9fd8a9f1` = `commit-tree` of the clean merge-tree `7b7087b2c519` with parents develop `b4ec1f060320` and head). In each, `npm ci --ignore-scripts` at the `Blockchain/Dev` workspace root (as gate 60; `--ignore-scripts` to skip the build-all postinstall) and `packages/shared` built with `tsc`. Vitest 4.1.12 via `vitest run --root <mcp-server> --maxWorkers=2` under `nice -n 10`; load was 9-13 throughout (below the 14 stop).
- **Base run:** `hash.ts` from `ddc644fb4869` copied over the head file, tests unchanged, restored by copy and verified by sha256.
- **Mutants/probe:** Python script with unique anchors, `-I`; probe test file written to the worktree and moved to a `_quarantine_2026-11-01/` folder in the worktree afterwards (untracked, in the scratch worktree, no deletes).
- **Spark:** stdout `evidence/spark_gate.stdout`; the Spark harness made its own worktree under `/private/tmp/claude-501/.../scratchpad/gate63_spark` (head, with the node_modules symlink the harness adds). No Spark process left running (both PIDs exited). I started only background jobs recorded in `evidence/spark_gate.pid` and `evidence/spark_review.pid`; I stopped nothing by name.
- **Harness note:** this gate's `--node-modules` pointed at the complete hoisted tree of `wt/head` (built shared), so none of gate 60's two failed harness runs recurred.
- **Tool-hook note:** the session's git-write guard refuses `git -C $VAR/...` for write verbs; literal paths inside the project folder were needed (a harness quirk, not a finding).
