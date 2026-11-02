# QA Gate 121 verdict: Secuura/Distributed_Secuura PR 1939 (KS-1940, services/governance: a failed participant lookup answers 503 and writes nothing), TIER 1 (governance vote power / data integrity)

## BLUF
**GO WITH NOTES. Nothing has to be fixed before merge.**
- **What I ran:** the REAL governance router and the REAL shared `errorHandler`, on a real loopback listener. `../db` was replaced by my own stateful recorder (written independently of the author's harness). It journals every write, applies `ON CONFLICT (id) DO UPDATE SET <listed cols>`, refuses a second wallet row as the DDL's UNIQUE does (switchable), and seeds 4 participants and 2 proposals. Grid: **18 cells x 8 thrown values** (none, Error, string, revokedProxy, getterThrows, protoTrap, toStringThrows, nullProto) = 144 records per version. Each record holds the status, the body, the write journal, the read list, the full before/after table snapshot, the per-cell `proposalCounter` delta and the error logs. Judge: **1043 checks, 0 failed** (logs/judge.log). The positive control (head replaced by base) gives 228 failed (logs/judge_tamper.log).
- **Q1, the required outcome: YES.** On createProposal (3 shapes), registerParticipant (existing wallet with and without UNIQUE, and a new wallet) and GET /participants/:id (by id, and by wallet when either read fails), plus castVote / cancel (proposer, committee, stranger) / delegate (either read): **every** failing value at head answers `503 SERVICE_UNAVAILABLE "Governance participant store is temporarily unavailable"`. Each also has 0 write statements, identical before/after tables and a counter delta of 1 (no move). An unreadable value logs `unreadable thrown value`, and the planted secret never reaches a log.
- **Base, for contrast:** with an ordinary Error or a string, createProposal answered **201 and overwrote u-1** (100000/partner/200000/DRep became 1000/staker/1000/not DRep, proposals_created 4 became 1). Without UNIQUE, register made a **duplicate wallet row**; with UNIQUE it answered 500. GET answered 404 for an existing participant. With an unreadable value every POST answered 500 with 0 writes, and GET gave **no answer**.
- **Real PostgreSQL 15.19:** throwaway `gate121-pg`, schema = the repo's init.sql governance DDL, `wallet_address TEXT NOT NULL UNIQUE`; removed. **Before the fix the createProposal overwrite occurs** in both shapes (wallet != id, and wallet = id), and also when every participant read fails. **The duplicate-wallet defect does not occur**: the insert is refused 23505, the route answers 500 and nothing is written. **After the fix neither happens:** 503, tables unchanged.
- **Re-measure:** red-first 7 passed / 17 failed, each failure carrying an assertion failure. Green 24/24 in three runs. Governance suite 13 files 197/197 at base, 14 files 221/221 at head. tsc with tests 0 -> 0 (planted control rc 2). eslint 0/0 (planted control rc 1). docs-fragments clean, with 4 planted defects caught. merge-tree onto develop 0e3a9b65 clean, changing exactly the 5 PR paths. Merged with PR 1938's head it is also clean.
- **Mutants:** 18 run, **16 killed** (every kill by assertion), **2 survived**. M9 (readable non-Error branch, the known class) and M8b (the by-address log replaced by a constant for an ordinary Error; G121-F1, the O73-P1 residue).

## Heads
- START (logs/head_start.log, 2026-11-02T10:02:42Z): PR head `17e811c477e69e7d7a7182ab92e68e9a85abd8dd` and develop `0e3a9b65cdd632fbc1783257c6cb9833934e1404`, both as commissioned. PR 1938 head `6b5960b6bb0e`.
- END (logs/head_end.log, 10:20:32Z): all three unchanged. Local HEAD = `17e811c4`, product sha256 equals the head blobs (svc `4e32457bd36b`, routes `a021fff50e8e`), working tree clean (0 lines).
- Commits: `e81530691a60` (parent `c234c2388a16`), then the merge `17e811c4` (parents e8153069 + `bc8558db`). Merge-base with develop = `bc8558db`. develop moved 6 commits / 32 paths since `bc8558db`, and **none of them is under services/governance** (empty diff, logs/dev_gov_moved.log).
- Diffstat three-dot vs `bc8558db` (logs/product_diff.log): 5 files, **+676/-12**, exactly as claimed:
  - the new test +595
  - routes/governance.ts +20/-6 (26 lines)
  - governanceService.ts +22/-2 (24 lines)
  - two fragments, +21 and +22
  - Nothing outside services/governance and the fragment pair.
- **Q3 merge-in conditions, verified:** the merge-in's governanceService.ts change (`e8153069..17e811c4`) equals PR 1929's hunk (`c234c238..bc8558db`) line for line (MERGEIN_EQUALS_1929_HUNK). The suite after the merge-in is 221/221.
- PR body not read (no gh login used). Sources: the author's READY (evidence/f23_ready_pr1939.txt), the commit message (logs/commit_msg.txt) and the fragments.

## FINDINGS
- **G121-F1 (LOW, test gap; this is what O73-P1 leaves uncovered)** No cell asserts the by-address log line for an ORDINARY Error. T3, T3n and T2b check only the unreadable shapes. Mutant M8b (log `'unreadable thrown value'` for every value at the by-address catch) **SURVIVES** (logs/mutants_extra.log). O73-P1's C1 pinned exactly that cell. One-line fix in T3 (optional, not merge-blocking): `expect(errorLogs('DB get participant by address failed')).toEqual([['DB get participant by address failed', { walletAddress: 'addr_test1_u1', error: 'ks1940 stand-in: connection terminated' }]]);`
- **G121-F2 (LOW, test gap, known class)** M9 (the readable non-Error branch `String(err)` replaced by `'x'`, by-id catch) SURVIVES, because no cell throws a string. Same gap as G90-F3 and G117-F3. My probe shows a thrown string is handled like an Error at both versions (base 201 overwrite; head 503, 0 writes).
- **G121-F3 (INFO / recommended disclosure; Q3)** The head never newly ALLOWS anything (0 of the 119 failing cells at head write or succeed: 17 faulted cells x 7 values). But the body and fragments disclose only the proposer-cancel refusal. Three more actions that base completed correctly while one participant read was failing are now refused with 503, fail-closed:
  - (a) registering a **new** wallet when the by-address read fails (base 201 with a correct row);
  - (b) an **unregistered** proposer's first proposal when the by-address read fails (base 201, correct auto-register);
  - (c) GET /participants/<wallet> when the by-id read fails (base 200 from the second read; this is T8 by design).
  Recommend one line in the body's behaviour-change paragraph naming (a) to (c).
- **G121-F4 (INFO, wording)** The fragment says the overwrite occurs "when only the by-id read fails". It also occurs when **every** participant read fails, measured on the fake DB and on real PG (`create_u1_all_reads`). The fragment's figures and run comments ("194 -> 218", "218 tests, 13 files") predate the merge-in; at head they are 197 -> 221 and 14 files.
- **G121-F5 (INFO, convention)** Both commit subjects start `Refs KS-1940:`, not `KS-1940` as the brief's HOLDS require. The PR title was not read. These are pushed commits, and the brief forbids a rebase, so Wednesday decides whether this matters (the squash title can carry the key).
- **G121-F6 (INFO, pre-existing, healthy path, read from source, NOT run)** In createProposal, if a proposer's user id equals ANOTHER participant's wallet_address, `registerParticipant(proposerId)` finds that row and upserts it at minProposalStake. createProposal then `DELETE`s it (`proposer.id !== proposerId`) and re-inserts it under the proposer's id. The other participant's row is lost. This PR does not change it; it belongs with KS-1941.
- **G121-F7 (INFO, ks1346)** No new value enters any log line (Q7). Pre-existing as G111-F4: the readable branch still logs `err.message` / `String(err)` and the request key (id / walletAddress). The shared errorHandler now logs the constant 503 message and its stack instead of the old DB error.

## Q1. The required outcome (in full)
**Code (head).** Both helpers keep "no row -> undefined". In the catch they use the file's guarded read (byte-identical to O73-P1's guard block), log, then `throw new ServiceUnavailableError('Governance participant store')`. That is shared `AppError(503, 'SERVICE_UNAVAILABLE')`, which the shared errorHandler maps to the 503 body. GET /participants/:id gains `next` and try/catch -> `next(error)`. The 8 call sites are registerParticipant :439, getParticipant :472/:474, createProposal :527 (and :531 via register), castVote :692, cancelProposal :893, and delegateVote :929/:930. Each does its lookup before its first write (read; confirmed by 0 writes in every head cell). The ordinary-error status of this service (measured, T10 and my base cells) is 500 INTERNAL_ERROR. The head uses a dedicated 503.

**Probe** (scripts/g121_probe.test.ts run by scripts/probe.sh; copied into the clone, then moved to logs/_quarantine; NOT part of the PR). Results are in logs/probe_{base,head}.jsonl and logs/judge.log (full 144-row table). Base jest rc 1: the GET cells leave an unhandled rejection that jest attributes to the test. Head rc 0.

| cell (fault) | ordinary Error / string, base | unreadable x5, base | every failing value, head |
|---|---|---|---|
| createProposal u-1 (by-id fails once) | **201, 5 writes, u-1 overwritten** 1000/staker/1000/not DRep, counter +1 | 500, 0 writes | **503, 0 writes, tables =, counter =** |
| createProposal u-1 (all participant reads fail) | **201, overwrite** | 500, 0 writes | 503, 0 writes |
| createProposal u-2 (wallet = id, by-id fails) | **201, 3 writes, u-2 overwritten** | 500, 0 writes | 503, 0 writes |
| createProposal u-new (by-address fails) | 201, correct auto-register | 500 | 503 (G121-F3b) |
| register existing wallet, UNIQUE | 500 (insert refused 23505), 0 rows changed | 500 | 503, 0 write statements |
| register existing wallet, no UNIQUE | **201, a second row for addr_u1** | 500 | 503 |
| register new wallet | 201, correct row | 500 | 503 (G121-F3a) |
| GET /participants/u-1 (by-id fails) | 404 for an existing participant | **NO ANSWER** | 503 |
| GET /participants/addr_u1 (by-id fails, T8) | 200 from the second read | NO ANSWER | 503, second read never issued |
| GET /participants/addr_u1 (by-address fails) | 404 | NO ANSWER | 503 |
| GET absent id (no fault) | 404 | 404 | 404 (= base) |

Healthy controls (value `none`, every cell) are **byte-identical base vs head**: status, body, write journal, reads and after-snapshot, with uuids, now-timestamps and absolute proposal numbers normalised; the per-cell counter delta is compared separately. That includes T6 (unregistered proposer: INSERT uuid, DELETE uuid, INSERT u-new, INSERT proposal, UPSERT u-new) and T7 (existing wallet: one UPSERT of u-1; id, joined_at, proposals_created 4 and votes_cast 7 carried).

## Q2. Inverted-input controls
- **T6** (unregistered proposer, healthy): base = head, measured on the fake DB and on real PG (`create_unregistered none`: u-new row, wallet u-new, 1 proposal).
- **T7** (existing wallet, healthy): base = head. Real PG: u-1 becomes 5000/staker/5000, joined_at seeded, proposals_created 4.
- **T5** (absent id): 404 `NOT_FOUND "Participant not found"` at both versions, both reads issued. The author's committed controls T5/T5b/T6/T6b/T7/T9f/T10 pass at base (7 of 7).

## Q3. Disclosed behaviour change and the other three callers
| action, one read failing | base, ordinary Error | base, unreadable | head (all values) | newly allows? |
|---|---|---|---|---|
| cancelProposal by the proposer | **200, proposal cancelled (1 write)** | 500 | 503, 0 writes | no: newly REFUSES (disclosed) |
| cancelProposal by a committee member | 403 | 500 | 503 | no |
| cancelProposal by a stranger | 403 | 500 | 503 | no |
| castVote by a DRep | 403 "Voter not registered" | 500 | 503 | no |
| castVote by an unregistered user | 403 | 500 | 503 | no |
| delegateVote, delegator read fails | 404 | 500 | 503 | no |
| delegateVote, delegate (second) read fails | 404 | 500 | 503 | no |

- **Zero writes at head in every row.** The head **never newly allows** an action base refused.
- It newly refuses only while the store fails (fail-closed): the disclosed proposer cancel, plus G121-F3's three.
- With a healthy store, cancel, vote and delegate are byte-identical to base (control rows).

## Q4. getParticipant's second lookup (T8)
- At head a failing by-id read throws before the by-address read is issued: `reads == ['byId']`, 503.
- At base an ordinary Error was hidden and the second read answered 200. An unreadable value gave no answer.
- Mutant M4d (`dbGetParticipant(...).catch(() => undefined)` in getParticipant) is KILLED by T4, T4b and T8.

## Q5. O73-P1 retirement
- **What the held file guards** (READY_KS-1868-KS-1868-O73-P1_..._PASS-7of7, read whole): the two helper catch logs (`dbGetParticipant` :277, `dbGetParticipantByAddress` :287 at its tip), each with the same 6-line guard. Its cells: C1, an ordinary Error logs its message on BOTH lookups; R1 a revoked Proxy and R2 a throwing message getter, each logging the constant on both lookups. In its design both resolve undefined (fail-open).
- **Head:** the guard blocks are byte-identical to O73-P1's, at both sites. The fail-open "resolve undefined" is deliberately superseded by the 503 throw, which is stronger.
- **R1/R2 by id:** T2 asserts the constant on the by-id log.
- **R1/R2 by address:** T2b asserts the constant on the by-address log.
- **R1/R2 through getParticipant:** T4b covers them (503).
- **C1 by id:** T1 asserts the message.
- **Answer:** every site and unreadable shape is covered, same or stronger. **One cell is left: C1 on the by-address lookup** (an ordinary Error's message on the by-address log line). It is unasserted, and mutant M8b survives (G121-F1).
- The "both lookups log" shape of O73-P1 no longer applies, because by design the second read is never issued after a failed first read.
- O73-P1 can retire on merge; G121-F1's one line closes the residue.

## Q6. Real PostgreSQL (scripts/g121_pg.test.ts via scripts/pgproof.sh; logs/pg_{base,head}.jsonl, logs/pg_table.log)
- **Setup:**
  - container `gate121-pg` (postgres:15-alpine, `postgres --version` 15.19), port 127.0.0.1:55121, started by me, the only container I touched;
  - schema = init.sql :1071-1135 (svc_proposals, svc_governance_participants with `wallet_address TEXT NOT NULL UNIQUE`, svc_vote_delegations), identical to the participant DDL in the other two files (read);
  - the real routes, the real errorHandler and the real service, with `query` going to a real pg Pool;
  - only the chosen participant SELECTs throw, before reaching the server.
- 8 cells x 3 values per version. Base jest 23/24: the 1 failure is GET with a revoked Proxy (unhandled rejection). Head 24/24.

| cell | base, Error | head, Error and revokedProxy |
|---|---|---|
| createProposal u-1, by-id read fails once | **201; u-1 1000/staker/1000/not DRep, proposals_created 1; 1 proposal** | 503; u-1 unchanged; 0 proposals |
| createProposal u-1, all participant reads fail | **201; same overwrite** | 503; unchanged |
| createProposal u-2 (wallet = id) | **201; u-2 1000/staker/1000/not DRep** | 503; unchanged |
| register existing wallet addr_u1 | **500; no duplicate (UNIQUE refused), rows 3** | 503; unchanged |
| register new wallet | 201, a correct new row | 503 (G121-F3a) |
| GET u-1 | 404 (revokedProxy: NO ANSWER) | 503 |

- **Answers:**
  - before the fix, on a real DB, the **createProposal overwrite occurs**; the **duplicate-wallet defect does not occur** (23505 -> 500, nothing written);
  - after the fix, neither: 503 with the tables unchanged;
  - in the overwritten row, `wallet_address` and `joined_at` keep their values: ON CONFLICT updates neither column.
- Container removed (`docker rm -f gate121-pg` rc 0; `docker ps -a --filter name=gate121` 0 lines; logs/pg_remove.log). Other seats' containers (gate65-pg, s-w13-pg, s-e29-pg) were not touched.

## Q7. Kam's ks1346 logging rule, and PR 1938's overlap
- **Changed log lines:**
  - `logger.error('DB get participant failed', { id, error: reason })`
  - `logger.error('DB get participant by address failed', { walletAddress, error: reason })`
- `reason` is the constant `'unreadable thrown value'` for an unreadable value. In every other case it is the same expression as base (`err.message` / `String(err)`).
- The 503's message is a constant. No new value enters a log. The probe asserts the planted secret is absent from every log line for all 5 unreadable shapes at both versions.
- **Compliant.** The request key and the readable message are pre-existing (G111-F4, G121-F7).
- **PR 1938:** its governance change is routes :151 (`parsed.error.errors` -> `.issues`) plus types :385. `git merge-tree pr1938 pr1939` gives **rc 0, clean**, tree `a1506029`. In the merged routes file, `.issues` sits at :157 and the KS-1940 hunk (:75-105) is byte-identical to the PR's. **No shared line: confirmed.**

## Q8. Re-measure (Node v26.8.1 only; NOT measured on Node 24; jest 29.7.0, `--rootDir` anchored to the clone)
- **Install:** `npm ci --ignore-scripts` in governance (rc 0) and packages/shared (rc 0); shared built with tsc (rc 0) and symlinked as `node_modules/@secuura/shared` inside the clone.
- **Red-first** (logs/red_base.json, logs/runs_ks1940.log): head test file + base product (`bc8558db`) gives **7 passed / 17 failed**. All 17 carry an `expect(...)` failure. The two T4b cells also carry the product's own unhandled rejection (`Expected: 503, Received: "NO_ANSWER"` plus the TypeError / getter boom), as the fragment says.
- **Green:** 24/24, three runs (logs/green_head_{1,2,3}.json).
- **Suite:** base 13 files **197/197** (logs/suite_base.json); head 14 files **221/221** (logs/suite_head.json, three runs). The author's 221/221 re-measures exactly.
- **tsc** (logs/tsc_run.log):
  - plain config rc 0 / 0 errors at both versions;
  - with tests (scripts/tsconfig.tests.json; 13 test files at base, 14 at head) rc 0 / 0 errors at both;
  - planted `const g121Planted: number = "x"` gives TS2322 + TS6133, rc 2; restored by sha.
- **eslint** (Dev flat config; Dev node_modules borrowed by symlink from gate 117's clone, whose lockfile and eslint.config.mjs sha are identical; the symlink was moved to logs/_quarantine): the 3 changed files give **0 errors, 0 warnings**, rc 0. A planted file gives a no-debugger error and an unused-var warning, rc 1.
- **docs-fragments** (logs/frag_run.log): clean rc 0, "flow 117 legacy + 86 new, cheat 112 legacy + 86 new". Planted defects, each rc 1: flow unclosed div, flow missing `<!--n-->.`, cheat unclosed div, cheat `</table>` corrupted. All restored by sha; rc 0 after. The cheat ADVISORY at line 6235 is pre-existing (G90-F7 / G117-F7).
- **merge-tree onto develop `0e3a9b65`** (logs/merge_tree.log): **rc 0**, tree `86c65214`, clean.
  - The merged tree differs from develop in exactly the 5 PR paths, +676/-12, and the merged blobs equal the PR's.
  - Paths shared between develop's moved range and the PR: 0 (control: 32 against itself).
- **Mutants** (scripts/mutants.py + logs/mutants_extra.log): product only, the new test untouched, sha256 restored after every run (RESTORE_OK). Every kill is by assertion (logs/mutants_kind.log).

| mutant | result |
|---|---|
| M1 restore the swallow, by-id helper | KILLED T1 T1b T2 T4 T4b T8 T9a-e |
| M2 restore the swallow, by-address helper | KILLED T2b T3 T3n |
| M3a GET route answers 200 instead of forwarding the 503 | KILLED T4 T4b T8 |
| M3b helpers throw 409 instead of 503 | KILLED (14 cells) |
| M4a drop the GET route guard (catch answers 404) | KILLED T4 T4b T8 |
| M4b drop the guard in createProposal | KILLED T1 T1b T2 |
| M4c drop the guard in registerParticipant | KILLED T2b T3 T3n |
| M4d getParticipant hides the by-id failure | KILLED T4 T4b T8 |
| M4e castVote / M4f cancelProposal / M4g delegateVote second read | KILLED T9a / T9b T9c / T9e |
| M5 / M5b fallback reads the value (by-id / by-address) | KILLED T2 T4b / T2b |
| M6 swallow only unreadable values (by-id) | KILLED T2 T4b |
| M7 / M7b log dropped (by-id / by-address) | KILLED T1 T2 / T2b |
| M8 constant for every value, by-id | KILLED T1 |
| **M8b constant for every value, by-address** | **SURVIVED** (G121-F1) |
| **M9 readable non-Error branch -> 'x'** | **SURVIVED** (G121-F2) |

## Notes for the PR body
- G121-F3 (recommended): add to the behaviour-change paragraph that while a participant read fails, (a) registering a new wallet, (b) an unregistered proposer's first proposal and (c) GET by wallet address after a failed by-id read now answer 503, where base completed them. Nothing is newly allowed.
- G121-F4 (info): the overwrite also occurs when every participant read fails. The fragment's figures are the pre-merge-in ones (head: 197 -> 221, 14 files).
- G121-F1 / F2 (optional cells): an ordinary-Error log assertion on T3 (closes O73-P1's last cell), and one string-throw cell.
- G121-F5 (info): the commit subjects start `Refs KS-1940:`.
- G121-F6 (info, for KS-1941): the healthy-path row deletion when a proposer id equals another participant's wallet.
- None is FIX-BEFORE-MERGE.

## NOT TESTED
- The PR body text and title (no gh login).
- A booted governance service (index.ts was not booted; the router and errorHandler were mounted on a probe app with the auth middleware stubbed) and the gateway hop.
- The LIVE table's UNIQUE(wallet_address) (not read by any agent).
- Node 24; the four platform suites; CI; the pre-push hook legs (quoted from the READY only).
- The author's own real-PG script (I ran my own proof instead).
- G121-F6 (read from source only).
- Whether an unreadable thrown value is reachable from pg in production (reasoned as at gates 90 and 117: pg rejects with Error subclasses).

## Cleanup
- **Container:** `gate121-pg` was removed. `docker ps -a --filter name=gate121` shows 0.
- **Background runs:** none were started. `ps -axo command | grep gate121` shows 0 at END.
- **Probe and test files:** the probe test files and the planted lint file are in logs/_quarantine, and so is the borrowed eslint symlink.
- **Clone:** the working tree is clean at the PR head.

## Tier
**TIER 1 confirmed.** The change decides whether a failed read can write governance stake, tier, vote power and the DRep flag, and it changes the answers of the vote, cancel and delegate paths.
