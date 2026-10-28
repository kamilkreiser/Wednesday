# Spark gate (deterministic + Spark review): Secuura #1775, #1776, #1779

- **Gate model:** Claude Sonnet 5.5 (claude-sonnet-5-5), tier-2 gate shadow, subagent of Wednesday. Spark review model: deepseek-v4-flash-0731 via the tunnel (UP at start).
- **Pushed / merged / commented / edited:** nothing. No product code changed. Only my own clone was written to (fetch, `remote set-url origin`, `apply --cached` into a scratch index, worktrees).
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/sparkgate-1775-1776-1028/repo` (`git clone --shared` of the cache; `rev-parse --show-toplevel` asserted equal to that path before any fetch or write, and again at the start of every script). Worktrees were under `/private/tmp/claude-501/gatework/` (spark_gate.sh refuses a work dir under WEDNESDAY) and are all removed (`git worktree list` shows only the clone). `origin` of the clone was repointed to the GitHub URL because the cache has no `refs/pull/*`.
- **Facts / logs kept:** `out_p1775b/`, `out_p1776sh/`, `out_p1776se/`, `out_p1779/` (facts.json, diff.patch, logs), `suites/` (full-suite logs), `spark_1775/`, `spark_1776/`, `spark_1779/` (review.json, prompts, wall.txt). `out_p1775/` is a failed first attempt (see Harness notes).
- **Load:** load1 was 5 to 11 at each run, never above the 12 limit.

## Pins (git ls-remote)

| ref | start | end |
|---|---|---|
| develop | bd6697e079fce41db6b21e094a9eddb3d0e1d08e | bd6697e079fce41db6b21e094a9eddb3d0e1d08e |
| refs/pull/1775/head | 4cd8bb3b4c04a995a94767e44fd256d34d1cc499 (starts with 4cd8bb3b4c04, asserted) | same |
| refs/pull/1776/head | 319b0f24f8b9a8da1047b811e2082dfae3b021f9 (starts with 319b0f24f8b9, asserted) | same |
| refs/pull/1779/head | bb7a646c8db4bcb99f74aaf8f22613aa321f22c3 (equals the brief, asserted) | same |

develop did not move. Merge-base of all three PRs with develop is `bd6697e079fc`. (#1779's end read is the same listing as the other two.)

## BLUF

| PR | Ticket | Recommendation | Why |
|---|---|---|---|
| #1775 | KS-1467 | **GO WITH NOTES** | Claims reproduce (19 red / 10 green at base, 29/29 at head, tsc 0). Code blobs byte-identical to the canonical patch. One real unmeasured: other services' suites. Spark said NO GO; I could not make any of its three Majors stand as a blocker. |
| #1776 | KS-1591 | **GO WITH NOTES** | Both new tests red at base, green at head; code blobs byte-identical to both canonical patches. Notes: reachability unproven (the ticket says so), and other `toUpperCase()` role checks remain. Spark said NO GO; its two Majors are scope notes, not defects. |
| #1779 | KS-1536 | **GO WITH NOTES, and needs a tier-1 Opus gate regardless (AUTH file, routing v1.0 rule 4)** | 3 red / 6 green at base, 9/9 at head; auth suite 1200 to 1209, 1 failed both sides; code blobs byte-identical to the canonical patch; the role logic is unchanged for the four gates. |

Spark gave NO GO / NO GO / GO WITH NOTES. I disagree with the first two. See each section. A Spark NO GO on a PR with only "unmeasured / scope" findings is a calibration signal for the pilot, not a defect signal.

### Harness notes (mine, not the PRs')
1. `spark_gate.sh --node-modules` with `s-aa-ks1537/.../packages/shared/node_modules` has no `.bin/vitest`, so the first attempt reported 0 passed on both sides (`out_p1775/`, rc 127 "vitest: command not found"). I reran with `.../s-aa-ks1537/Blockchain/Dev/node_modules` (985 entries, has vitest). All results below use that. Read-only by symlink; nothing installed.
2. Full-suite runs by hand: for services/auth, the `ks1000` file needs `Blockchain/Dev/node_modules` at the worktree's Dev root. Without that symlink it fails to load (ENOENT on lstat) and the suite shows 1101/1110 cells. With it: 1200/1209.
3. The `shared` suite has 8 `ks256-spec-example-contract` failures in my harness on BASE and HEAD alike (`Cannot find package 'yaml'` from `scripts/spec-examples`, again a missing Dev-root node_modules). These are my environment, identical both sides, not PR-related.
4. Spark prompts: the two `Projects Documents` html files add about 1.2 MB of "full text at head". #1776's prompt was 1.29 MB and the Spark answered HTTP 400 after 3 s. I reran with those two html files dropped from the facts `touched_files` (full-text section only; they stay in the diff section). Same for #1779. #1775 went through at 1.14 MB with them in. So the Spark's findings on html-doc claims in #1776/#1779 saw the doc text only through the diff hunks.

## Spark rounds (data)

| PR | attempt | prompt tokens | completion tokens | wall-clock | result |
|---|---|---|---|---|---|
| #1775 | 1 | 352,082 | 1,368 | 470 s (script wall 471 s) | valid JSON, NO GO, 6 findings (3 Major, 2 Minor, 1 Note) |
| #1776 | 1 | (1.29 MB prompt) | 0 | 3 s | HTTP 400, no result |
| #1776 | 2 (html docs out of the full-text section) | 53,805 | 1,128 | 89 s | valid, NO GO, 6 findings (2 Major, 2 Minor, 2 Note) |
| #1779 | 1 (html docs out) | 21,601 | about 1k | 48 s (47.2 s in the request) | valid, GO WITH NOTES, 5 Notes |

Claude-side cost, for comparison: I spent roughly 45 minutes of wall clock on the three PRs including the reruns, almost all of it tool and harness time.

---

## #1775 (KS-1467, shared AppError prototype): GO WITH NOTES

**Head:** 4cd8bb3b4c04 asserted. **develop:** bd6697e079fc at start and end.
**Files changed (4, +110/-1):** `Blockchain/Dev/packages/shared/src/errors/index.ts` (+1/-1: `Object.setPrototypeOf(this, AppError.prototype)` becomes `new.target.prototype`), the new test `packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts` (+73), and the two `Projects Documents` html files (+16, +20).
**Test file run:** the one new test file, through spark_gate.sh with `--node-modules` (the Dev one above).

| side | passed | failed |
|---|---|---|
| BASE product code + head test | 10 | 19 |
| HEAD | 29 | 0 |

Matches the claim "19 red / 10 green at the pin, 29/29 with the change".

**Shared suite (my own runs, `vitest run` in packages/shared, Node v26.8.1):**
- BASE: 1039 cells, 9 failed, 975 passed, 55 skipped.
- HEAD: 1068 cells, 10 failed, 1003 passed, 55 skipped. Delta is +29 cells, which is the new file.
- The claim "1034 to 1063, the same 1 Node-26-only red (cbor) before and after" is NOT reproduced as stated. My totals are 5 higher (1039 / 1068; the same +29), and my failure count includes 8 harness failures (note 3 above). The cbor cell does reproduce: `wallet-signature.test.ts:49` fails on BASE and HEAD (`expected false to be true`). The 10th failure on HEAD is `threadToken.test.ts:152`, "Test timed out in 30000ms" after a 71 s run, lucid WASM bootstrap. It did not fail on BASE nor in the #1776 HEAD suite run, so it is a load-dependent timeout. I did not rerun it.
- `tsc --noEmit -p .` in packages/shared at HEAD: rc 0. Matches "tsc rc 0".

**Byte-identity vs the canonical patch.** Canonical: `runs/spark_secuura_2026-10-28_ks_1467_p2_shared/out.md.checker/patch.diff` (named by the READY block). The PR's `git diff` for the two code files is NOT textually the same file (4814 vs 4639 bytes): git emits different hunk context counts and orders the files differently. So "byte for byte" is not true of the diff text. The result is identical: I applied the canonical patch to the merge-base in a scratch index (`git apply --cached`, check rc 0) and compared blob ids. Both code files match: test `86b64a9af8de…`, `errors/index.ts` `c9e11b92ee9b…`. **The resulting files are byte-identical to the canonical patch's.** The two html docs are not part of the Spark patch.

### Spark findings (verbatim severity) and my read

**F1: Major.** FOUND: "The fix changes the prototype of every AppError subclass instance ... the PR only ran the packages/shared suite and did not run the suites of the other services." TESTED: I read the diff and the PR's own doc line (`Not measured: the suites of the other services that import these classes`). I did not run any other service's suite. HOW: reading `errors/index.ts` at head and the doc hunk. **CONFIRMED as an unmeasured, not as a defect.** The one-line change makes each subclass keep its own prototype, which is what `instanceof` already assumed. A consumer that depended on the broken `instanceof AppError`-only behaviour would change. That is the PR's stated purpose. The PR says it did not measure it. Note, not a block.
**F2: Major.** FOUND: "the test does not verify that the errorHandler in any service ... recognizes subclasses; the ticket's bug is in services/auth's errorHandler." TESTED: read the test (C2 runs the shared handler) and the diff (no services/auth change). HOW: the diff lists no auth file. **CONFIRMED as scope**, not a defect: this PR is the shared prototype fix (`ks_1467_p2_shared`); the auth handler change is the separate `ks_1467_p1` unit, which is not in this PR. Whether p1 is a separate PR I did not check.
**F3: Major.** FOUND: "'byte-identical to the drafter's golden' is unverifiable from the provided material." TESTED: yes, by the apply-and-compare above. HOW: blob ids. **NOT REPRODUCED.** It is verifiable and it holds (with the diff-text caveat: the diff files differ in hunk framing).
**F4: Minor.** FOUND: the test's fake `Response` only has `status` and `json`. TESTED: read test lines 35-44. HOW: source. **CONFIRMED, harmless**: the handler's own use is `status` and `json`; the 29/29 on HEAD run against it.
**F5: Minor.** FOUND: "answers do not change" is tested only for the shared handler. TESTED: same read. HOW: source. **CONFIRMED**, same point as F2.
**F6: Note.** FOUND: 29 cells, P3 is a single cell. TESTED: count 29 at head. HOW: the run. **CONFIRMED, correct, nothing to act on.**

**Not tested for #1775:** any other service's suite; the services/auth handler; the docs' html (text only skimmed); whether KS-1467 p1 is another PR; any runtime path using `instanceof` on a real subclass in a deployed service; the `threadToken` timeout on a quiet machine.

**Recommendation: GO WITH NOTES.** Notes: (a) other services' suites unmeasured, run before or after merge; (b) the full shared suite has one Node-26 red (wallet-signature) on both sides, plus a load-dependent `threadToken` timeout I saw once on HEAD; (c) the "1034 to 1063" counts in the PR are 5 below my 1039 / 1068 (same +29), cause not found (the `skipped` count is 55 in mine; I did not check theirs).

---

## #1776 (KS-1591, shared + security): GO WITH NOTES

**Head:** 319b0f24f8b9 asserted. **develop:** bd6697e079fc at start and end.
**Files changed (6, +214/-2):** `packages/shared/src/security/keyRevokePolicy.ts` (+5/-3 net: `isPlatformRole` now refuses a non-string role and applies an ASCII-only fold), `services/security/src/index.ts` (`requireKeyAdmin`, the same fold; +5/-2), two new test files (shared 78 lines, security 89 lines), and the two html docs (+18, +21).
**Test files run:** each of the two new tests, one spark_gate.sh call each (shared; security), same Dev node_modules.

| test | BASE product code | HEAD |
|---|---|---|
| shared `ks1591-is-platform-role-is-an-exact-ascii-fold` | 7 passed / 6 failed | 13 / 0 |
| security `ks1591-require-key-admin-is-an-exact-ascii-fold` | 4 passed / 3 failed | 7 / 0 |
| total | 11 green / 9 red | 20 / 0 |

**Shared suite at HEAD** (my own run): 1052 cells, 9 failed, 988 passed, 55 skipped; the 9 failed are the same harness 8 plus the same wallet-signature cbor cell as in #1775. No new failure. `tsc --noEmit` in packages/shared at HEAD: rc 0. I did not run the services/security full suite.

**Byte-identity vs the canonical patches.** Canonical: `ks_1591_p1` (shared) and `ks_1591_p2_security` (security) `out.md.checker/patch.diff`, concatenated. The diff text differs in hunk context and file order (11,735 vs 11,490 bytes), as in #1775. Applied to the merge-base (check rc 0), the four resulting blobs equal the PR head blobs exactly: shared test `5cbbd51c249c…`, `keyRevokePolicy.ts` `2432251a8982…`, security test `3668bb7bdbeb…`, `services/security/src/index.ts` `7c2f7d18b8b1…`. **The claim "byte-identical to canonical patches" holds for file content.**

### Spark findings and my read
**F1: Major.** FOUND: "Reachability is NOT established ... the PR does not add any test that a dotless-i/long-s/array role can be produced by any issuer." TESTED: read the tests and the ticket line the Spark quotes. HOW: source. **CONFIRMED as stated in the ticket**, and the PR is a hardening of two predicates, not an exploit fix. Not a defect: the refusal tests are red at base and green at head. Note.
**F2: Major.** FOUND: "the PR does not sweep for other toUpperCase() role comparisons." TESTED: `git grep toUpperCase()` on head restricted to role lines. HOW: grep. **CONFIRMED**, and a real follow-up: the same pattern still exists at `services/auth/src/routes/users.ts:285` and `:377`, `services/originate/src/middleware/rbac.ts:56` and `:58`, `services/auth/src/services/password.ts:234`, and (in the base shape) the four gates in `services/auth/src/routes/issuerCerts.ts`. This PR fixes only the two named. Scope note, not a block.
**F3: Minor.** FOUND: the array-role cell accepts `[401, 403]`. TESTED: read test line 70 at head. HOW: source. **CONFIRMED.** It is a weaker pin than R1/R2 (which require 403). Because this test goes through the auth middleware, a 401 is possible. It is red at base (the array role is admitted, so 200), so it still discriminates.
**F4: Minor.** FOUND: "every ASCII spelling admitted before is admitted now" is an overstatement. TESTED: the diff only. HOW: reasoning on `replace(/[a-z]/g, upper)`. **NOT REPRODUCED as a defect.** For ASCII input, ASCII-folding equals `toUpperCase()` (the only difference is non-ASCII characters, which `toUpperCase` can map onto ASCII; that is the fix). The claim is true by construction; the tests cover examples, not the "every" universe. I did not enumerate.
**F5: Note** (`asRole` cast helper). **CONFIRMED**, harmless.
**F6: Note** (docs are not code). **CONFIRMED**, no action; I did not review the html's accuracy beyond the diff.

**Not tested for #1776:** the services/security full suite; any caller of `isPlatformRole` outside the two named; a live token path; whether any real issuer can emit a dotless-i role; the other `toUpperCase` role sites.

**Recommendation: GO WITH NOTES.** This is a security change (shared + security), so per the routing rule it deserves the tier-1 reading it would get anyway; the behaviour narrows access only for non-ASCII look-alike spellings and non-string roles. Notes: reachability unproven; the sweep (users.ts, originate rbac.ts, password.ts) is owed as follow-up; the array cell accepts 401 or 403.

---

## #1779 (KS-1536 groundwork, Spark pass ks_1536_p1): GO WITH NOTES. TIER-1 OPUS GATE REQUIRED (auth file, routing v1.0 rule 4), whatever this says.

**Head:** bb7a646c8db4 asserted (full sha above). **develop:** bd6697e079fc at start and end.
**Files changed (4, +163/-8):** `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (+13/-8; the brief says `issuerCerts.ts`, the path is `routes/issuerCerts.ts`), the new test `services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts` (+115), the two html docs (+16, +19).
**Test file run:** the one new test, via spark_gate.sh with the Dev node_modules.

| side | passed | failed |
|---|---|---|
| BASE product code + head test | 6 | 3 |
| HEAD | 9 | 0 |

Matches "3 failed / 6 passed at the pin, 9/9 with the change".

**services/auth full suite** (my runs, `vitest run --testTimeout=120000`, with the Dev-root node_modules symlink):
- BASE: 105 files, **1200 cells, 1 failed**, 1199 passed.
- HEAD: 106 files, **1209 cells, 1 failed**, 1208 passed.
- The same failing cell on both sides: `ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts > REAL: services/auth against the committed baseline passes ...`. **The counts match the claim exactly. The cell name does not**: the PR says "the same ks949 cell"; I got a ks1000 cell. Same on both sides either way, and likely sensitive to my symlinked tree, but I did not diagnose it, so I cannot say whether the PR's "ks949" is a different cell or a naming slip.

**Byte-identity vs canonical.** Canonical: `runs/spark_secuura_2026-10-28_ks_1536_p1/out.md.checker/patch.diff`. Applied to the merge-base (check rc 0), the two result blobs equal the PR head blobs: test `219f7fc23267…`, `routes/issuerCerts.ts` `a009177d404b…`. **Identical file content.** (I did not do a diff-text comparison for this PR, only blobs. The text differs between canonical and `git diff` in the two earlier PRs, so I would expect the same here.)

### Behaviour: do the four gates admit exactly the same roles?
FOUND: the extraction `hasAdminRole(role: unknown)` is `const text = String(role ?? ''); return ADMIN_ROLES.includes(text) || ADMIN_ROLES.includes(text.toUpperCase());`. TESTED: I read the whole product diff and the head file, and ran a differential of the old two-line inline form against the new helper in node over 29 inputs (undefined, null, '', each admin spelling and case variants, whitespace, dotless-i and long-s look-alikes, arrays, numbers, booleans, objects with `toString`, NaN): **0 differences**. This differential is weak (it is the same expression), so the real evidence is the reading. HOW: source.
- The old inline lines in all four gates were `const role = String(user.role ?? ''); if (ADMIN_ROLES.includes(role) || ADMIN_ROLES.includes(role.toUpperCase())) return true;`. The new line is `if (hasAdminRole(user.role)) return true;`. The expression is character-identical, the argument is the same `user.role`, and in each gate it sits in the same position: after the `if (!user) return false;` guard and before the scope checks. The scope checks are unchanged context lines in the diff.
- `git grep` of head: `ADMIN_ROLES` appears only at the declaration and inside `hasAdminRole`; `hasAdminRole(` is called at four places (lines 77, 85, 98, 114), one per gate (write, read, revoke, sign). No fifth gate and no remaining inline copy.
- The `ADMIN_ROLES` array is untouched.
- **Carried over unchanged (pre-existing, not introduced):** `'ıssuer_admin'.toUpperCase()` is `'ISSUER_ADMIN'`, so a dotless-i spelling and a long-s spelling are admitted by the issuer-cert gates, before and after. That is the KS-1591 weakness and #1776 does not touch `issuerCerts.ts`. It is a note for the Opus gate, not a behaviour change. An array role holding `'ORG_ADMIN'` is also admitted, before and after.
- The new export `hasAdminRole` is exported from a route file. Nothing else was observed importing it; an export adds a surface but no gate.

### Spark findings (all five Note; verdict GO WITH NOTES) and my read
**F1.** The PR does not tackle the ticket's seven divergent lists. TESTED: read the diff. HOW: source. **CONFIRMED**, and it is the PR's stated scope ("groundwork"). Not a defect.
**F2.** R3 is a source-text check (`SRC.split('ADMIN_ROLES.includes(').length - 1` equals 2). TESTED: read test line 83 at head. HOW: source. **CONFIRMED**: brittle by design, it pins "no inline copies" in this file only. Note: it counts 2 occurrences inside `hasAdminRole`, so it fails if anyone adds an inline copy back.
**F3.** The test mocks `authenticate` to trust an `x-test-user` header. TESTED: read test lines 12-18. HOW: source. **CONFIRMED**, standard for a route-level unit test. It means the real middleware path is not covered here.
**F4.** "byte-identical to the golden" is unverified by facts.json. TESTED: yes (blob apply-and-compare). HOW: blobs. **NOT REPRODUCED**: it holds.
**F5.** "0 vanished, 9 new" is not in facts.json. TESTED: I ran the suite by hand, 1200 to 1209, +9 cells. I did not diff cell names to confirm "0 vanished, 0 changed status". HOW: counts. **PARTLY CONFIRMED** (counts; the by-name claim is not tested).

**Not tested for #1779:** the cell-by-cell name diff ("0 vanished"); any other importer of `issuerCerts.ts`; the real `authenticate` middleware path; live issuer-cert requests; the other six divergent role lists in the ticket; whether the failing ks1000 cell is the one the PR calls ks949.

**Recommendation: GO WITH NOTES for the tier-2 shadow; tier-1 Opus gate REQUIRED regardless (auth file, routing v1.0 rule 4).** Reasons to GO: behaviour-preserving by reading, 9/9 and 1209 counts reproduce, code blobs identical to canonical. Points to hand the Opus gate: the dotless-i / long-s / array admission in `hasAdminRole` is unchanged and still open, and the "ks949" naming mismatch.

---

## What I did NOT do (all three)
- No live, integration, docker, az or network test beyond the git fetch, ls-remote and the local Spark call. No security scan.
- No full run of services/security, services/originate, or any other service's suite.
- No check of html doc accuracy beyond the diff text.
- No merge-tree against current develop. All three PRs add to the same two `Projects Documents` html files at their append points, so they will conflict with each other and with any other docs PR (the #1765 gate saw the same). Section numbers will need renumbering at merge. I did not test a resolved merge.
- Not checked whether KS-1467 p1 (services/auth errorHandler) is a separate PR or whether KS-1536 has further units.
