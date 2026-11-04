GO WITH NOTES — MERGE (no HOLD-FOR-KAM)
# QA Gate 187 (Tier 1, round 1): PR 1968 / KS-1868 vc-issuer db pool error + credentialRepo read catches (log-reason strings)

Merge tree on develop c7abf98e51030f908050fede10a3546871d4f2c1: `git merge-tree --write-tree c7abf98e5103 9a3f028be706` rc 0, tree **96de28959a80e01f4e7fc7ee0540539924829cfb**.

## Subject
- `git ls-remote origin refs/pull/1968/head refs/heads/develop` (on the client checkout, a read verb):
  - START (~19:00 AEDT): head 9a3f028be706722c5cf6b7b18e7b67827c8ec145, develop c7abf98e51030f908050fede10a3546871d4f2c1
  - END (~19:07 AEDT, 08:07Z): head 9a3f028be706722c5cf6b7b18e7b67827c8ec145, develop c7abf98e51030f908050fede10a3546871d4f2c1. **Neither moved.**
- Base (develop merged into the branch) 5c1ca287ed74b6353423a8c09e253abf3129233a; it is an ancestor of c7abf98e5103 (rc 0).
- Clone: `git clone --shared` of the checkout into `repo/` (ignored). The PR ref fetch could not run (the clone's origin is the local checkout, which has no `refs/pull/*`); all three commits were already present as objects through alternates, and their identity is pinned by the ls-remote above. No write verb ran on the checkout.
- The merge tree's `services/vc-issuer` tree is a34f9c0b3d4c, **identical to the head's**; `packages/shared` d94503e350c8 identical to head's. So every vc-issuer run on the head tree is a run on the merged tree. Develop's vc-issuer tree (86367745c762) is identical to base's.
- Hosts: Node v26.8.1, TypeScript 5.9.3, vitest 4.1.12, macOS. NOT run on Node 24 (by design), no Postgres, no Docker.

**Method.** I extracted `services/vc-issuer` at base and at head (git archive) into `scratch/{base,head}`, with a node_modules made of symlinks to the builder's clean worktree `s-r84-1968` (git status clean, HEAD = 9a3f028be706) plus an APFS clone of vc-issuer's own node_modules, so vitest's cache wrote only inside my workdir (checked: nothing in s-r84-1968 newer than my start). Every vitest/tsc process ran through `harness/run_suite.sh` / `harness/run_tsc.sh`: `--root`/`-p` anchored, started with cwd `cwd/` in the workdir, under `env -i` with HOME/TMPDIR in the workdir. I ran the PR's two new files at base and head; drove the REAL `db.ts` and `credentialRepo.ts` with my own cell harness (`harness/gate187-{db,repo}-cells.test.ts`: 5 changed sites x 13 thrown values + a planted-row cell, pg/db and logger replaced, every logger call captured with `util.inspect(showHidden)`); ran 25 mutants (`harness/mutants.py`) against both the PR's tests and my harness and counted the raw table (`runs/mutants.json`); ran the whole vc-issuer suite at base and head and tsc with and without tests, each with a control that fires.

## Findings

### G187-F1 — LOW: the product hunks are NOT "log-reason strings only": they change control flow for unreadable thrown values (by design, toward the ordinary-Error state)
- **FOUND:** Commission Q1 asks for proof that every non-test hunk changes only a logged string. It does not, in two ways. (a) Control flow: in 12 base cells a hostile thrown value made the catch itself throw; at head all 12 end in the ordinary-Error state — pool listener: revoked Proxy, throwing message getter, emitted `null`, emitted `undefined` (base: listener throws out of the emitter; head: returns, logs 1 line); ready hook: revoked Proxy, throwing getter (base: `initDb` REJECTS; head: resolves `true`); getById / getRecordById / getByHash x {revoked Proxy, throwing getter} (base: the read REJECTS; head: logs and answers from the memory fallback). (b) Logged field type: in 20 cells (5 sites x {Symbol, number, object, object-whose-toString-throws message}) the `error` field changes from a raw symbol/number/object to a string (`'Symbol(g187)'`, `'7'`, the object's `toString()`, or `'unreadable thrown value'`). No return value of an ordinary path, no thrown type and no SQL changes. The PR's own flow fragment states (a) and (b) plainly; only the commission's summary ("log-reason strings only") is narrower than the change.
- **TESTED:** the 5 changed catches, 13 thrown values each, at base and head (65+65 cells), the real modules with `pg`/`../db` and the logger replaced. Not tested: a real pg pool emitting such a value.
- **HOW:** `runs/cells_compare.txt` (from `harness/compare_cells.py` over `runs/cells_{repo,db}_{base,head}.json`). Control: base vs head tables compared unequal (False), the unmutated mutant copy reproduced head's tables exactly (True, 42 + 26 rows).

### G187-F2 — LOW: 6 non-equivalent mutants survive the PR's 18 new cells (coercion line, the three credentialRepo sites)
- **FOUND:** At getById, getRecordById and getByHash, mutant B (`reason = m;`, String() dropped) and mutant C (`reason = String(m);`, null/undefined pass-through dropped) pass all 18 PR cells. Both are non-equivalent: B logs a Symbol message raw (winston's JSON drops it — the very loss the db-file R2/R5 cells guard for db.ts), C logs the text `"undefined"` for a thrown string/number/null. The repository test file has no Symbol-message and no non-Error-thrown cell; the db file has both, and kills B and C at its two sites. My harness kills all 6.
- **TESTED:** 25 mutants = 5 sites x {A constant text, B drop String, C drop null-pass, D catch rethrows, E log `err.detail` (Q3 positive control)}.
- **HOW:** `harness/mutants.py`; raw table `runs/mutants.json` (per-run logs in `runs/mut/`, ignored by the `mut/` pattern). Each mutation asserts the exact head text of the line it replaces, and the file is restored from head after each (verified by `cmp` at the end).

### G187-F3 — LOW: the new db test file's control C1 times out at the default 5000 ms on a cold whole-suite run
- **FOUND:** My first whole-suite run at head: 24/25 files, 731/732, the one failure `control ks1868 C1: an ordinary Error reaching the pool listener ...` "Test timed out in 5000ms" (9351 ms). Runs 2 and 3: 25/25, 732/732, the same cell 282 ms / 280 ms; the two new files alone 18/18 (C1 219 ms). The cell is the file's first cold `vi.resetModules()` + `import('../db')` (db.ts `require('@secuura/shared')`). The builder hit the same cell the same way (8437 ms) and disclosed it in the flow fragment; it is a CI-flake risk, not a product fault.
- **TESTED:** 3 whole-suite runs at head on this host. Not tested: CI.
- **HOW:** `runs/head_whole.txt`, `runs/head_whole_run2.txt`, `runs/head_whole_run3.txt`.

### G187-F4 — INFO, PRE-EXISTING (base = head): same-class unguarded `err?.message` reads remain in the two changed files
- **FOUND:** `db.ts` probeDb line 102; `credentialRepo.ts` lines 98 (save write catch), 324 (reader-scoped by-hash catch — same log text as the fixed getByHash), 413 (list catch), 502 (revoke update catch). Not in this PR's slice; the fragments say "probeDb is untouched" and "KS-1868 stays open".
- **TESTED:** read at head; not driven.
- **HOW:** `grep -n` over the head files for `err?.message`/`catch`.

### G187-F5 — INFO, PRE-EXISTING (base = head): the error MESSAGE is logged verbatim, so a value inside the message reaches the log
- **FOUND:** A token planted in the thrown Error's `message` appears in the log line at all 5 sites at base and at head (that is the reason field by design). Unchanged by the PR.
- **TESTED/HOW:** cell `secretInMessage` in the harness. Whether real pg messages carry row or parameter values was NOT measured.

## What passed (measured)
- **Q1 scope:** 6 files, exactly the ready file's list (paths under `Blockchain/Dev/...` and `Blockchain/Projects Documents/fragments/...`); product = `db.ts` +16/-2 and `credentialRepo.ts` +24/-3 (diff stat 18 and 27 lines). 5 hunks, all of one shape (try { m = err?.message; reason = m == null ? m : String(m) } catch { reason = 'unreadable thrown value' }; log `{ error: reason }`). Log message texts unchanged in all 5. Behaviour change: see G187-F1.
- **Q2 class bar:** 65 head cells (5 sites x 13 values); **65/65 end in exactly base's ordinary-Error state** (same threw / return value / initDb result / one log line); **0 head cells more permissive than base-ordinary**. Base cells not in the ordinary state: 12 (all fixed at head). The memory fallback reached on the hostile path is the same fallback base reaches with an ordinary Error.
- **Q3 no secret/row content:** token planted in `detail`, `hint`, `where`, `query`, `parameters`, `cause`, `stack`: absent from all logger output at 5/5 sites at base and head. Token planted in a returned DB row (credential, proof, subject, owner id): absent from logs at 3/3 read sites, base and head. **Positive control:** mutant E (log `err.detail` beside the reason) turned the token present at 5/5 sites; the `secretInMessage` cell fired at 5/5 in every run. Head's `error` field is now always a string or null/undefined, never a raw object — it cannot carry enumerable fields of a message object (base could).
- **Q4 red-proof:** the two new files at base: **11 failed / 7 passed (18)**, all 11 by `AssertionError` (6 `{threw:true}` vs fallback, 1 `{threw:true}` vs `{threw:false}`, 2 initDb `{ok:false}` vs `{ok:true,value:true}`, 2 `'<symbol>'` vs `'Symbol(ks1868)'`); the 7 controls pass at base (they pin ordinary behaviour, they do not prove the fix). At head 18/18. **Mutants: 25 run; PR tests kill 19, 6 survive (G187-F2, non-equivalent); gate harness kills 25/25.** Raw table counted from `runs/mutants.json`: A 5/5, B 2/5, C 2/5, D 5/5, E 5/5 by PR tests (= 19).
- **Q5 suites:** whole vc-issuer suite head **25 files / 732 tests rc 0** (runs 2 and 3; run 1 see G187-F3); base 23 / 714 rc 0; the 714 shared cells have identical names and status at base and head (`cmp` rc 0; one-character control rc 1). tsc `-p tsconfig.json` and `-p tsconfig.test.json`: 0 errors rc 0 at base and head; planted-error control 1 error rc 2. The ready file's figures (25/732, tsc 0, 6 files, head/base SHAs, 10 range files with 0 shared) all reproduced. **PR body: UNMEASURED** (no gh login used; unauthenticated GitHub API returns 404 for the private repo). The PR's own fragments say "KS-1868 stays open" and name the other sites as not covered.
- **Q6 merge:** merge-tree onto c7abf98e5103 rc 0, tree 96de28959a80e01f4e7fc7ee0540539924829cfb; range 5c1ca287ed74..c7abf98e5103 changes 10 files, 0 shared with the PR (control: PR files vs itself 6).

## NOT tested
- Node 24; any deploy; Docker; a real Postgres / pg pool; a service boot; HTTP routes; whether any real thrown value of these kinds occurs in production.
- Lint and the docs-fragments check (author's claims, not re-run).
- The PR body and the KS-1868 ticket (no gh / Linear access used).
- The other KS-1868 sites (G187-F4) and the four platform suites; CI.
- Winston's real transports (the logger was replaced by a recorder; the claim that a raw Symbol is dropped by JSON is from the PR's text and JSON semantics, not driven here).

## Plain answer for Kam
This change makes the credential service keep working and keep writing a sensible log line when the database layer hands back a strange, unreadable error, instead of crashing that request or the start-up step. For ordinary errors nothing changes: the same log lines, the same fallback to the in-memory store. I checked that no hidden error details or credential data leak into the logs, and nothing got looser than it already was for ordinary errors. Two small notes for the builder: three of the new tests could be tighter, and one new test can time out on a slow first run. Safe to merge.
