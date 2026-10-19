# Spark screen, part 14 (2026-10-19 ~18:55-19:25 AEDT): the KS-1641 p1 rebrief and two new briefs, three rounds, THREE PASS (all strict, no accommodation); ceiling rung 2 (three times)

By a Spark screen-and-brief sub-agent for Wednesday (receipt: claude-sonnet-5-5, row C8 (screen + brief drafting), P1-P4 no, gauge 38%). Secuura only. Nothing held, raised, pushed, merged, committed or deleted; no GitHub or Linear write; no `hold_ready`. Nothing under `!CODING` was written (only `git ls-remote` and file reads; the cache clone and the scratch clone are in Wednesday's tree and the session scratchpad). `LINEAR_API_KEY` was sourced inside script files, never printed.

## BLUF
- **KS-1641 p1 rebrief: PASS, and this time strict.** The cause of the refused hold was found and it is NOT a model miss: the round-1 output was BYTE-IDENTICAL to my golden, and `decl_splice.py` spliced a `const rows` into it anyway because it counted the object-literal KEY `rows:` in `query: async () => ({ rows: [] })` as a use of the reference's file-scope `rows`. The rebrief declares `rows` in the test itself (`const rows: any[] = [];` and `({ rows })`). Round: `PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL`, `decl_splice.out` = `spliced 0`, no `.decl.diff` in the opts. The ticket's rebrief counter is spent; a hold can be tried.
- **KS-1460 (auth `/register` over an INVITED stub, `updateUser` -> `updateUserOrThrow`): PASS**, golden BYTE-IDENTICAL, `spliced 0`.
- **KS-1568 o6 (`ROTATE_CHAIN_WAIT_MS=10s` parses as 10 ms): PASS**, golden TREE-IDENTICAL (the model omitted the two `index` lines; strict apply, no accommodation).
- The pool is thin: of 361 Backlog/Todo tickets only two new ones fit the predicate and were not decisions or live-lane files. A third was looked for and not found (see SKIPs).
- Develop moved THREE times during the work; every brief is pinned to `80868551e679`. A fourth merge (#1615) landed after the last round and touches only anchoring.

## Pinned sha
`git ls-remote origin refs/heads/develop` read at the start (18:5x) = `722e07f19cee683ea037930e601e380a9491f7b5`. It moved to `31cfb44dce840caf8ae8a6a4c1468efa7e78e247` (#1613, KS-1195: `api-gateway` `platform.ts` plus one test) at 19:03, then to `80868551e67934cb951d28eec44ce3bdf835944c` (#1614, KS-1402: originate `documents.ts`, migration 052, one test) by 19:04. I fetched each into the cache clone (`cat-file -t` = commit), diffed the file lists (none touched m365-integration, auth `routes/auth.ts` or security `index.ts`), re-pinned all `Tip:` lines to `80868551e679`, and repeated the by-hand test at that tip. Re-read before every round (ls-remote) = `80868551e679` for all three real rounds. Re-read at 19:22 = `ad784e702ca205230e39d329abefa8a85fb5946c` (#1615, KS-1603: anchoring `index.ts`, `anchorOverwriteGuard.ts`, two tests); fetched, none of my files touched.

## Census (Linear, read-only)
- Query: team `KS`, `state.type in [backlog, unstarted]`, `orderBy: updatedAt` (newest first), `first:50`, paginated until `hasNextPage=False`: **8 pages, 361 tickets** (Backlog 335, Todo 26). 118 of them are not named in any earlier SCREEN file, `queue.md` or `done.md`.
- Positive control: KS-1642, KS-1641, KS-1568 and KS-1460 are in the set. Zero control: KS-1634, KS-1628 and KS-1557 (In Progress) are NOT in it, as the filter requires.
- Descriptions read whole: KS-1648, 1647, 1651, 1649, 1635, 1636, 1630, 1514, 1568, 1587, 1566, 1530, 1591, 1600, 1242, 1460, 1602, 1501, 1458, 1494, 1498. KS-1641 was re-read through its brief and run dir.
- Prior art: KS-1460, KS-1568 and KS-1242 are named in none of SCREEN_4-13, `queue.md` or `done.md` (grep of every KS number in them).

## SKIPs (reason, measured)
- KS-1651 (the `ownership_transferred` event actor): originate `routes/documents.ts` (live seat) and "decide the event's actor contract when it gets a consumer".
- KS-1650: originate `routes/anchors.ts` (Seat J). KS-1647: originate `documents.ts` and `verification.ts`; "facts only, no fix shape chosen", a product call about how loudly to announce. KS-1630: anchoring `index.ts`.
- KS-1648 (60 s vs 3,600 s window): the ticket lists three fix shapes "not chosen" and says shape 2 masks the row and shape 1 is the honest one (a migration): a decision.
- KS-1649 (developer-portal.html:564): HTML prose, and the ticket says to change it only after #1613 merges (it has now merged; but no runnable checker for a doc row, and KS-1473 on the same file is an owner decision).
- KS-1635 (drop the dead `meetsVerificationLevel` dep): 16 files (14 tests); outside the one-product-one-test contract. KS-1636: three doc lines and a comment, no runnable checker.
- KS-1566 (the evidence-lookup cap pin): the ks1557 suite (excluded). KS-1587 m-a/m-b: needs a real Postgres; N1 is in `packages/shared`.
- KS-1530: "a decision first" (400 or pass on); KS-1591: reachability not established, recommendation "not built"; KS-1600: several mutants, integration tests; KS-1501 and KS-1458: comment/test-scan work or a ruling; KS-1494: item 3 would need a re-nest of `seedDemoUsers`' try block (a builder-refused shape) and a heavily mocked test, item 1 is in a test-only `integration/` file.
- KS-1514: "decision needed: which side is the contract". KS-1498: a migration. KS-1602: a test-file-only change (no product file; the tier needs one).
- **KS-1242** (`authenticateToken` async middleware with no catch): looked at the code; the limiter continuation already has `.catch(next)` (KS-1215), what remains is no reachable throw today and the ticket asks for "the whole gateway"; a test would need an invented throw. Not briefed, not a decision per se, just no honest red cell.
- KS-1568 main body (M10, M3b, M7, M1 cells): not taken; only the folded-in o6 was.
- Named exclusions untouched: KS-1645, 1642, 1634, 1603, 1629, 1557, 1633, 1402, 1195, 1384, 723/1454.

## Briefs and rounds (brief dirs under `local-model/night/briefs/`, run dirs under `local-model/runs/`)
All three: `brief_lint` rc 0 with empty stderr, dry-run rc 0 with no WARNING, ctx=65536, no blank context line in any edit block, ONE real round each, `--control` run first. Each test was run by hand in a scratch clone (red at the tip, green with the edit) before its brief was written.

| # | ticket / piece | dir | tier / rung | control | round verdict (verbatim) | golden |
|---|---|---|---|---|---|---|
| 1 | KS-1641 p1 REBRIEF (round 2 of 2): m365 OAuth callback caps the reflected `error_description` at 200 chars + NEW vitest file that declares `rows` itself | `ks_1641_p1b` | code_patch, rung 2 | CONTROL-PASS 7/7 BYTE-IDENTICAL, 59 s, `spliced 0` | `SPARK ROUND ks_1641_p1b: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 80868551e679 · 112s round, 55.886s model, 33694+1457 tok` | BYTE-IDENTICAL |
| 2 | KS-1460 (first item): `POST /register` INVITED-stub claim calls `updateUserOrThrow` (2 hunks in `routes/auth.ts`) + NEW vitest file mounting the real router | `ks_1460_p1` | code_patch, rung 2 | CONTROL-PASS 7/7 BYTE-IDENTICAL, 107 s, `spliced 0` | `SPARK ROUND ks_1460_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden BYTE-IDENTICAL · tip 80868551e679 · 166s round, 61.911s model, 29729+2034 tok` | BYTE-IDENTICAL |
| 3 | KS-1568 o6: `rotateChainWaitMs()` accepts only a plain digit string (else the 10 s default) + NEW vitest file on fake timers | `ks_1568_p1` | code_patch, rung 2 | CONTROL-PASS 7/7 BYTE-IDENTICAL, 60 s | `SPARK ROUND ks_1568_p1: PASS — PASS (checker rc 0 + A2a anchor OK) · golden TREE-IDENTICAL · tip 80868551e679 · 134s round, 60.839s model, 41244+1282 tok` | TREE-IDENTICAL |

Run dirs: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-19_ks_1641_p1b` (+ `-control`), `..._ks_1460_p1` (+ `-control`), `..._ks_1568_p1` (+ `-control`).

Checker lines (each `checker.out`): ks_1641_p1b `A4 (2 failed / 4 run; controls green; assertion reds)`, `A5 (4/4)`, `RESULT: PASS (7/7)`; ks_1460_p1 `A4 (2 failed / 4)`, `A5 (4/4)`, `baseline: total=1084 failed=0 | after: total=1088 failed=0`; ks_1568_p1 `A4 (2 failed / 5)`, `baseline: total=347 failed=0 | after: total=352 failed=0`, A7 rc 0. All `NEW reds: []`.

**Accommodation check (the point of this screen, read before holding):** for each of the three real rounds `out.md.checker/decl_splice.out` = `spliced 0`, `section_N.opts` names the plain `section_N.diff` (never a `.decl.diff` or `.tdz.diff`), and for ks_1641_p1b `cmp section_2.diff section_2.decl.diff` is equal. So `hold_ready`'s strict test should read A2 honestly. ks_1568_p1's TREE-IDENTICAL is the model leaving out the two `index <sha>..<sha>` lines, not a reformat.

## Things Wednesday should read before holding
1. **The KS-1641 diagnosis changes the earlier IMPROVEMENTS row.** Round 1 was not a model omission: the golden I wrote contained `{ rows: [] }`, the model reproduced it byte for byte, and `decl_splice.used_in_new` counted the key as a use. The harness made the test file it ran differ from the file in the diff, and `--control` still said CONTROL-PASS. See the IMPROVEMENTS rows below; the cheapest guard is "a control that needs an accommodation does not say PASS".
2. **Tier-1 routing.** KS-1460 is the public registration endpoint of auth: a claim over an INVITED stub that cannot confirm its activating update now answers 503 and issues no session, token or mail (same wrapper `/reset-password` and `/verify-email` already use). KS-1641 is the unauthenticated OAuth callback (shortens the reflected text only). KS-1568 reads an operator env var more strictly. No credential is read, issued or compared in a new way.
3. **Partials, none closes its ticket.** KS-1641: `:465` only (finding 1 and `:515` open). KS-1460: the first item of its priority order only; the social-id writes and the two best-effort callers are open. KS-1568: o6 only; the four guard cells are open.
4. **KS-1568 design choice, flagged:** the ticket says "refused or parsed". The brief takes "refused" (non-digits fall back to the 10 s default). For `10s` both readings give the same observable answer, and the cells pass for both. Also: `1e3`, `0x10`, `250.5` now yield the default.
5. **KS-1460 after a 503:** `createUser`'s `ON CONFLICT` write has already landed and is not rolled back; the row stays INVITED, so a retry re-enters the claim path. Stated in the brief's UNMEASURED.
6. **Open-PR overlap NOT checked** on any of the three product or test files (no GitHub query; none of the three tickets has a Linear attachment). The auth `routes/auth.ts` is a busy file: KS-1194 part 2 is in `routes/users.ts`, a different file.
7. Housekeeping: `spark/cache/work/` gained about 6 per-round clones (not pruned); `spark/state/dry/` gained 3 dry-run inputs; the cache clone fetched develop up to `ad784e702`.

## IMPROVEMENTS rows added (4, appended to `local-model/IMPROVEMENTS.md`)
1. FOUND: the KS-1641 splice was a `decl_splice.py` false positive on an object-literal key; fixes owed in three steps (key guard; no plain PASS when an accommodation fired; the A2 line says `accommodation:`), workaround and red corpus named. Corrects the 17:1x row.
2. FOUND: hook friction for brief authors (`cd` as a word inside a heredoc; `git -C $VAR` write verbs; unquoted heredoc with backticks), and a suggested `brief_fill.py`.
3. FOUND: a rebrief needs a new dir name; `brief_lint` refuses a first line that does not start `# KS-<n>`.
4. NOTE: develop moved three times; how the stale check behaved.

## NOT done
- No hold, no raise; no GitHub or Linear read of PR state.
- Not measured: the whole-suite runs beyond the checker's A6; a real Postgres for KS-1460 (a real zero-row UPDATE); real time for KS-1568's 10 s wait; the Windows/UTF-16 edge of the 200-char cap (KS-1641); KS-1242 (no honest red cell).
- A fourth candidate was not found; I did not force one.

## Files written
Briefs: `local-model/night/briefs/ks_1641_p1b/` (`KS-1641.md`, `golden.diff`, `spark.pins` tier=code_patch, ref=ks934, line=465, ctx=65536), `ks_1460_p1/` (`KS-1460.md`, `golden.diff`, `spark.pins` ref=ks806, line=257), `ks_1568_p1/` (`KS-1568.md`, `golden.diff`, `spark.pins` ref=ks1556, line=312). Scratch (not durable): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/dd32393e-b87e-4d51-ac65-b22e5897a2c1/scratchpad/s14/` (census.py/json/out, get.py, clone/, templates, fill.py, test drafts).
