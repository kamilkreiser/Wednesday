# Gate 194 commission — Secuura / Blockchain, PR 2005 (KS-1959: a revoke whose database write fails answers success and the credential still verifies), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 08:xx AEDT. Model: Opus.
**TIER 1, reason:** a credential-revocation / verify path (routing v1.0 tier-1 gate). The change makes a revoke fail where it used to succeed, on a route whose outcomes decide whether a revoked credential verifies.
**Round count:** round 1 of 2.
**A rotation KILLS it:** you run as a subagent of Wednesday's seat; if that seat rotates while you run, you are killed mid-run. Write `verdict.md` EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before finish)`), then rewrite it as each question closes, so a kill leaves a truthful partial file rather than none.

## What was ruled, so what this PR must be
- The defect: gate 191 G191-F2 (HIGH, PRE-EXISTING; `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate191-ks1958-pr2003/verdict.md` lines 22-25, read 2026-11-05; also gate 152 G152-F3) and ticket KS-1959: in vc-issuer, when the revoke's DB UPDATE fails, `POST /:id/revoke` answers 200, the DB row stays unrevoked, and the very next verify (DB healthy) returns verified TRUE on both routes (credentials, presentations) in the same process (the healthy DB row outranks the revoked memory copy; 6 of 6 cells at base and at PR 2003's head). With hostile UPDATE thrown values (revoked Proxy, getter-throws message) revoke answered 500 (unguarded `err?.message` in revoke's catch, G152-F4 family) and verify was again TRUE. Gate 191 ran NO restart (its NOT-tested list).
- **Design ruled by Wednesday: option (a)** (relayed; the PR body and Wednesday's ANSWER mail to Seat K 14th are the source; check the PR body):
  1. `revoke()` keeps the memory write where it is.
  2. When `isDbAvailable()` and the UPDATE THROWS, or returns a numeric `rowCount < 1`, `revoke` throws a FRESH `CredentialStoreWriteError` with the FIXED message `the credential store could not be updated`.
  3. The catch reads the thrown value GUARDED (no unguarded `err?.message`).
  4. The revoke ROUTE maps only that error to `AppError` 503 `The revocation could not be saved. Retry the revoke.`
  5. Verify (`revocationResolvers.ts`) is UNCHANGED.
  6. A non-number `rowCount` (null/undefined/missing) is read as SUCCESS. Stated tolerance: pg always sets `rowCount` for UPDATE, and four existing test fakes rely on it. The gate MEASURES this tolerance and names it in the verdict.
- Not in scope (do not raise as defects): the KS-1958 read-side fail-closed (PR 2003, already gated GO WITH NOTES; `getById` option untouched here); Boundary 1 (no DB: memory only) unchanged; Boundary 2 (healthy DB, zero rows, then memory) per gate 191 question 5.
- **Commit `a968818a0038727399663775722017c130d4cb08`, parent `e899463d2a0b1b30f2cff46b23d001622620029a`** (develop at Wednesday's ls-remote 08:1x AEDT 2026-11-05). PR 2005 by Seat K 14th. 1 commit expected.
- **Seat's figures to RE-MEASURE (not trust):** red 5 of 8 at base -> green 8 of 8 at head; direction matrix 54 cells: more permissive 0 of 54, stricter on verify 0 of 54, verify equal 54 of 54; mutants 7 of 7 killed; vc-issuer whole workspace 758 -> 766 of 766 (758 is gate 191's count at PR 2003's head; +8 = the new tests); the five gate-191 "unreadable thrown value" guards byte-equal (sha12 `68bcdbb5`, `af4f679e` x3, `a37a6ec8`) plus a sixth guard, sha12 `e1b09425` (the new revoke-catch guard).

## Questions (tier 1: measure, do not take the READY's word)
1. **Scope.** `git diff --name-only e899463d2a0b a968818a0038727399663775722017c130d4cb08` must be exactly: `Blockchain/Dev/services/vc-issuer/src/repositories/credentialRepo.ts`, `.../routes/credentials.ts` (the revoke route only), the NEW test file, and its fragment pair (`Projects Documents/fragments/{flow,cheat}/KS-1959-*.html`; take the exact names from `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959/ready_2005.txt`). `revocationResolvers.ts` UNTOUCHED (zero diff); `getById`, `getRecordById`, `getByHash`, `getReadableByHash` hunks: none (diff + one cell each at question 2); no api-gateway file, no migration, no openapi file other than the one the PR names (see 7). Numstat per file; quote every changed product line of credentialRepo.ts and routes/credentials.ts in the verdict.
2. **Base-vs-head matrix over real HTTP.** Use gate 191's technique: real `credentialRepo`, `revocationResolvers`, shared verifier, credentials + presentations routers, errorHandler, helmet, cors, boundedJson, rejectNulBytes over a real HTTP server on 127.0.0.1:<ephemeral> with `fetch`; ONLY `../db` (an in-memory table whose SELECT/UPDATE can be made to throw or to return a chosen `rowCount`) and the vc-issuer logger replaced. COPY gate 191's harness (`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate191-ks1958-pr2003/gate_tests/gate191-matrix.test.ts` and `scripts/compare.py`, `scripts/mutants.py`, `scripts/suites.sh`) into YOUR workdir and adapt; never run in gate 191's workdir, never reuse its `logs/`. The base is the product bytes of `credentialRepo.ts` + `routes/credentials.ts` from develop `e899463d2a0b` overlaid in your clone and restored (blob equal; `git status` empty after each run); `revocationResolvers.ts` is identical on both sides. Each cell writes one JSON line; the compare script prints the table. Cells (each x both verify routes credentials + presentations where verify is read; each revoke through its real route):
   - UPDATE throws: (i) ordinary pg-like Error (with code/detail/hint/where), (ii) revoked Proxy, (iii) getter-throws message;
   - UPDATE returns `rowCount` 0;
   - UPDATE returns `rowCount` `null`, `undefined`, and the key absent (THE TOLERANCE: measure each, name the outcome, and say plainly whether head treats it as success, matching the stated tolerance);
   - healthy DB (UPDATE ok, rowCount 1): revoke 200, ONE UPDATE, then verify FALSE (revoked);
   - no DB (`isDbAvailable()` false): memory-only revoke, unchanged from base;
   - unknown id: 404 (or base's status) unchanged;
   - already-revoked id (if base has a distinct outcome);
   - SELECT throws (gate 191 q4: revoke with a failing SELECT behaves exactly as base: 12 of 12 identical at PR 2003).
   For each cell record: revoke HTTP status and body, number of UPDATEs issued, the DB row's revoked flag, the memory copy's revoked flag, then the verify response (status, verified, errors) on both routes. **Predicates, counted by YOU as "N of M":** (a) revoke outcome more permissive than base (head says success where base said failure, or head leaves the credential verifying TRUE where base left it FALSE): must be 0; (b) verify outcome more permissive than base: must be 0; (c) revoke outcomes that DIFFER base->head, each named (expected: the UPDATE-throws and rowCount-0 cells go 200 -> 503; hostile-value cells go 500 -> 503; say if any other cell differs); (d) verify outcomes that differ (expected: none beyond the same-process cell where the revoke's failure is now reported, and the verify result itself should be equal: seat says verify equal 54 of 54). **Control that can fail:** base shows revoke 200 + verify TRUE for UPDATE-throws and rowCount 0 in the same run (the instrument can show a fail-open), and a mutant that restores the swallow (question 6) turns the head cells back.
3. **Leak check.** Plant a distinctive token in the thrown message, `detail`, `hint`, `where`, a getter-thrown message and a fake stack, plus `vc_credentials_store`, a hostname and a SQLSTATE; search the WHOLE serialized body and ALL headers of every revoke response (200, 503, 404, 500 if any) and every verify response, at head and at base. Required at head: 0 hits (the 503 body is the fixed wording only). **Control that can fail, in the same run:** the same search finds the token (a) in the captured warn/error log at head and base, and (b) in the body under a mutant that rethrows the original error (`throw err` instead of the fresh fixed-message error). The header search needs its own positive control or say plainly it has none (gate 191 had none).
4. **Availability cost, as stated.** Measure: healthy revoke = 200 with exactly ONE UPDATE (no extra SELECT, no retry, same latency band as base within noise); 503 ONLY on a failed UPDATE or a numeric rowCount < 1; NO new 500 path anywhere on the routes (hostile thrown values now 503 not 500: say so; any other 500 at head = a finding). Any other consequence of the 503 that the PR body does not state is HOLD-FOR-KAM (see the rule below). Read the PR body (via the API if you hold a read identity, else the seat's read-back files from `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959/ready_2005.txt`, and say which) and list every consequence it states; compare with what you measured.
5. **The restart case.** In a revoke that returned 503 (DB row unrevoked, memory copy revoked, per design step 1): simulate a fresh process by re-running `loadFromDb` (or the module's real load path: read it, then drive it) against the same in-memory DB, then verify. Expected per Wednesday's ruling: the row is unrevoked, so a fresh process verifies VALID, and this is CONSISTENT with a truthful 503 (the caller was told the revoke was not saved, so the credential was never revoked from the caller's point of view) and is NOT a fail-open. Confirm or contradict, and state exactly what a caller sees in the same process after the 503 (memory revoked: verify FALSE in that process, DB unrevoked), and after the retry that succeeds (DB revoked, both processes verify FALSE). If a state exists where the caller got 503 AND a later healthy retry also answers 503 but the credential verifies TRUE in the revoking process: state it. Gate 191 ran no restart; this is the new measurement.
6. **Mutants** (committed bytes; each anchor count 1; restore blob-equal; count the RAW table yourself; headline = table). Reproduce at least 4 of the seat's 7 (list them from the READY, run the same mutation), plus these of your own: (m-a) THE (b)-HAZARD: move the memory write AFTER the DB write (a failed DB write then leaves memory unrevoked as well; the zero-row cell and the throws cell must kill it); (m-b) swallow restored (catch returns success); (m-c) zero-row check removed (only throws counted); (m-d) `rowCount < 1` changed to `rowCount < 0`; (m-e) the route maps ANY error to 503 (a non-write error, e.g. a malformed id handled as 400/404, must then show differently); (m-f) fixed message replaced by `err.message` (the leak cell must kill); (m-g) throw before the memory write (memory not revoked on a failed write: this is the (b) design the ruling REJECTED; judge it killed or equivalent against the stated design). Name each survivor and judge equivalence in writing, trying to separate it with an input.
7. **OpenAPI 503 claim.** Read `Blockchain/Dev/services/vc-issuer/src/openapi/vc-issuer.openapi.ts` (the seat/Wednesday says line ~1113; re-find it at head) and the diff hunk there if any: does the revoke operation declare a 503 response with the schema the route produces (shape, example wording `The revocation could not be saved. Retry the revoke.`)? If the hunk is not in the diff, is the claim in the PR body or the fragment instead? Note: Question 1 expects NO openapi file in the delta unless the READY names it; if the 503 is documented elsewhere or not at all, report where, and mark UNMEASURED any contract-test claim you did not run (the platform's Schemathesis suite is NOT run by the gate).
8. **Merge tree.** In YOUR clone, `git merge-tree --write-tree e899463d2a0b1b30f2cff46b23d001622620029a a968818a0038727399663775722017c130d4cb08`: rc and tree id (expect rc 0 and a tree equal to the head commit's own, since the parent is the current develop: check `a968818a00^{tree}`); re-read develop with `git ls-remote` at start and end.
9. **Suites and static checks, at head:** the whole vc-issuer workspace (seat: 766 of 766; gate 191 at PR 2003's head had 758 of 758 in 26 files: report files and tests, and the difference); the new test file red-first against base product bytes (seat: red 5 of 8; every red by assertion, 0 TypeError, 0 `error TS` in the failing set; a TS2554-style arity error stripped by esbuild is a type error only, say if it appears); tsc incl. tests (`tsconfig.test.json`) rc and a failing control; eslint on the touched `.ts` files with a planted control; `docs-fragments.mjs check` clean and a planted defect that gives rc 1; the five gate-191 guard sha12s re-computed by YOU at head (`68bcdbb5`, `af4f679e` x3, `a37a6ec8`) plus the sixth (`e1b09425`), and a planted one-character change detected (control); title starts `Refs KS-1959:` and is <= 92 chars (count); 0 close words before a key (use gate 191's regex and its control string).

## HOLD-FOR-KAM rule (this gate)
Beyond gate_common section 6: ANY change to a verify outcome (any verify cell that differs base->head in `verified`, `errors`, or status), and ANY reach of the 503 wording beyond the API error response (a UI string, a log line shown to a client-human, a fragment or doc that a client reads, an email), is written HOLD-FOR-KAM. State the condition and the evidence; Wednesday rules. A revoke that returns 503 where base returned 200 is the INTENDED change and is not by itself HOLD-FOR-KAM; if the PR body does not state it, write that as a finding.

## Subjects (re-pin yourself at start and end)
- Repo Secuura/Distributed_Secuura; read-only checkout to clone from: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (fetch the PR ref into YOUR clone only; never write to the checkout).
- **PR 2005** head claimed `a968818a0038727399663775722017c130d4cb08` (read from `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959/ready_2005.txt` and re-read by `git ls-remote origin refs/pull/2005/head` at start and end; if it differs from the claim, say so first and stop). Develop `e899463d2a0b1b30f2cff46b23d001622620029a`.
- The seat's READY: `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959/ready_2005.txt` (read whole). Seat K's records under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/` (the 14th's folder named in the READY) may be read.
- **Workdir:** `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959/` = `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959/`. (gate_common section 2's naming pattern ends `-pr<n>`; this folder as Wednesday created it does not carry the PR number: use it as given.) No PostgreSQL is needed (the DB seam is an in-memory table, as gate 191). Dependencies only from an install matching the lock at the head (`npm ci --ignore-scripts`; build shared); never link from the shared checkout's node_modules. Start the workdir with `.gitignore` (gate_common section 2) before anything else; every process cwd inside the workdir, `env -i`, HOME/TMPDIR inside it.
- Live seats (Wednesday's `tmux list-panes` 08:2x AEDT): D 52nd (demo deploy, box only), F 33rd (PR 2004, a different PR), K 14th (PR owner). B 93rd has WRAPPED. Do not touch their worktrees, processes, ports or clusters. No contact with demo or kintsugi.
- Never post: the gate does not push, merge, comment on the PR or any ticket, send mail, or write to any board; it only READS. (gate_common section 1 is exact: findings only, one verdict file.)

## NOT TESTED by design unless you do it (say so in the verdict)
Node 24 (gate 191 ran Node v26.8.1; say what you ran). A real deploy, demo, kintsugi. A real PostgreSQL / pg pool (the db seam is a stand-in; a pg-like Error imitates a real driver error's fields, it is not produced by pg; in particular the claim "pg always sets rowCount for UPDATE" is read from pg's documented behaviour, NOT measured here: UNMEASURED, closed by running the UPDATE against a real PG15 cluster if Wednesday wants it). A real second replica. index.ts boot (the reproduced stack, `jwtAuthenticate` replaced by a fake user, as gate 191). The api-gateway proxy and any UI/caller that acts on the revoke's 503. Latency under a real slow or hanging DB. The four platform suites and CI checks on the PR. Add anything else a reader might assume you covered.

## Verdict
`verdict.md` in `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate194-ks1959/`. Line 1 per gate_common section 6, for PR 2005, and the merge tree on develop e899463d2a0b for the merge seat. Then FOUND / TESTED / HOW with controls; `## What passed (measured)` numbered to match the questions; `## NOT tested`; `## Plain answer for Kam` (3-6 plain sentences: what a merge changes for users, including that a revoke whose save fails now says so and can be retried, and the restart behaviour after a 503). Finding ids `G194-F<k>`; pre-existing findings say PRE-EXISTING (base = head). Final message per gate_common section 7, including the head and develop at start and end, the pids stopped, and any stray file outside the workdir (there should be none).


---

# gate_common.md: the common section of every QA gate commission

Paste this file WHOLE into every gate commission (Agent-tool subagent or cockpit seat), after the
gate-specific part (subject, questions, cells). It is client-neutral: the client, repo, PR, head and
the questions live in the gate-specific part, never here.

Why this file exists (2026-11-03): the common section lived in a session scratchpad and died with it,
so gates 161-165 were briefed by copying gate 160's verdict. A mechanism is recorded by its PATH
(lesson 2026-09-07). Edit this file, never a copy.

## 1. Role
- You are a QA GATE. Findings only. You never fix, commit, push, open or edit a PR, post a comment,
  write a ticket, send mail, deploy, or tell any human anything. Your output is one verdict file.
- You report to Wednesday only, as your final message (section 7).

## 2. Where you may write (the workdir)
- Your workdir is the folder the gate-specific part names, under
  `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/<YYYY-MM-DD>_gate<N>-<ticket>-pr<n>/`.
  Write NOTHING outside it.
- At creation, before anything else, write `<workdir>/.gitignore` with at least:
  `repo/`, `scratch/`, `home/`, `tmp/`, `mut/`, `runs/**/*.bin`. Clones, throwaway trees and any
  generated credential stay ignored. The verdict, harness and results are tracked.
- YOUR SHELL'S CWD IS WEDNESDAY'S TREE, not your workdir. A relative runner scans and writes into it
  (gate 119, 2026-11-02, wrote `node_modules/.vite/...` into Wednesday's root). So:
  - anchor every runner: `vitest --root <dir>`, `npm --prefix <dir>`, `jest --rootDir <dir>`,
    `npx --prefix <dir>`; or `cd` inside a `bash -c '…'` whose path is in your workdir;
  - **AND start every test or app process with its CWD inside your workdir** (`bash -c 'cd <workdir>/cwd && …'`):
    `--root` does NOT stop code under test writing RELATIVE paths into the process cwd. Gates 183 and 184
    (2026-11-04) both appended production-logger lines to Wednesday's `logs/combined.log` this way, with
    `--root` set correctly;
  - run untrusted or stateful steps under `env -i` with `HOME=<workdir>/home` and
    `TMPDIR=<workdir>/tmp` (keep TMPDIR short: socket paths over ~104 bytes break tsx IPC).
- STOP every background process you started before you report (list them; kill by pid; never by
  basename; never pid 1). Wednesday runs `gate_stray_check.sh` before the next GO and it refuses on
  any stray file.

## 3. The client checkout is READ-ONLY to you
- READ git verbs only on the project's checkout: `ls-remote`, `show`, `log`, `diff`, `cat-file`,
  `ls-tree`, `merge-base`, `rev-parse`, `grep`. NEVER `fetch`, `pull`, `worktree`, `checkout`,
  `merge-tree --write-tree`, `commit`, `stash`, `gc` there: those write its `.git`.
- For anything that writes: `git clone --shared <checkout> <workdir>/repo`, then
  `git -C <workdir>/repo fetch origin refs/pull/<n>/head` (a PR ref cannot be truncated, a branch
  name can) and run write verbs only inside `<workdir>/repo`.
- Never print, copy or write a secret value. Results show counts, truncated hashes, modes and key
  names only. If a harness must hold a generated value, it stays in an ignored folder.

## 4. Subject: pin it, at the start AND the end
- `git ls-remote origin refs/pull/<n>/head refs/heads/develop` at the start and again at the end;
  write both into the verdict. If the head moved, say so first and stop.
- `git merge-tree --write-tree <develop> <head>` (in your clone) on the CURRENT develop: rc and tree.
- State host versions you ran on (Node, TypeScript, the test runner) and what you did NOT run on.

## 5. Method: what makes a measurement count
- **The class bar (fix-a-thrown-value / error-path PRs):** head must end in exactly the state base
  reaches with an ORDINARY Error, at every changed site. Count cells; name any head cell MORE
  permissive than base-ordinary. That count decides HOLD-FOR-KAM (section 6).
- **Red first:** the PR's new tests (and your own cells) fail at base by ASSERTION, pass at head.
  A cell that passes at base is not proving the fix; say which.
- **Drive the real thing** where you can: the real module by blob, the real route over HTTP, a real
  database. Say plainly what was read and not driven.
- **Every zero needs a control that would have produced a non-zero, run in the same action**, from a
  source independent of the thing you are testing (a different file or syntax you did not write).
  A zero from an instrument that could not fire is not a zero.
- **Mutants:** run them, then COUNT THE RAW TABLE yourself; headline = table, or say it differs.
  Name each survivor and whether it is equivalent.
- **Never re-implement a tool to check the tool**: read its lines, or make it print what it computed.
- Never `grep -r` / `find` over `/Volumes/DevMASTER/WEDNESDAY` or any local-model `runs/` or `night/`
  tree. Open named files. If a call runs past ~2 minutes, it is stopped or its reason is written.

## 6. The verdict file: `<workdir>/verdict.md`
Line 1, exactly one of:
- `GO — MERGE` · `GO WITH NOTES — MERGE (no HOLD-FOR-KAM)` · `GO WITH NOTES — HOLD-FOR-KAM (<reason>)`
  · `NO GO (<FIX-BEFORE-MERGE ids>)`

Then:
- `# QA Gate <N> (Tier <t>, round <r>): PR <n> / <ticket> <subject>`
- Subject block (section 4), method in one paragraph.
- `## Findings`: one `### G<N>-F<k> — <SEVERITY>[ — FIX-BEFORE-MERGE]: <one line>` each, with three
  fields: **FOUND** (the claim), **TESTED** (scope: what was and was not exercised), **HOW** (the
  instrument, the command, the controls). Pre-existing findings say PRE-EXISTING (base = head).
- `## What passed (measured)`: per question, the counts.
- `## NOT tested`: everything a reader might assume you covered and you did not. A reachability or
  exposure word ("reachable", "in production", "any caller") appears in a finding only if it was
  measured; otherwise it is listed here.
- `## Plain answer for Kam`: 3-6 plain sentences, no jargon, what a merge would change for users.

HOLD-FOR-KAM is WRITTEN when: any head outcome is more permissive than base-ordinary; or the change
touches a signature class (production, money or payouts, a message to a human, anything
irreversible). Wednesday RULES whether it holds; you only state the condition and the evidence.

## 7. Report back to Wednesday (your final message, short)
- The verdict's first line, the verdict path, findings by severity (ids), mutant counts, the head
  and develop you measured at start and end, every background process stopped (pids), and any stray
  file you know you wrote outside the workdir (there should be none).

## 8. Rounds
- Tier 1 / tier 2 per `0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`. Round 2 is
  a DELTA: it re-tests the round-1 FIX-BEFORE-MERGE items and the forms that held, not the whole PR,
  unless the gate-specific part says otherwise. Two NO GO rounds on one class is the cap.
