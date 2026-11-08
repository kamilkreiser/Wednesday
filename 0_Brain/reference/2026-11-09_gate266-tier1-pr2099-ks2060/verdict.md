PR 2099: GO WITH NOTES

# Gate 266, tier 1, round 1: PR 2099 (KS-2060), Secuura / Blockchain

| PR | head | develop | verdict |
|---|---|---|---|
| 2099 | 0d747d09ab2345cb1f5c087880a8812c2eb1df12 | fa0592f3b6f595f02fc36af2d8fa936213378fdd | GO WITH NOTES |

**Kam's ruling:** no finding blocks the merge on a ruling. F1 changes a sentence in Kam's DPIA. The residual it names comes from Wednesday's ruling D-4, so Wednesday decides whether it goes to Kam as a third residual.

Head and develop, read from origin by `git ls-remote`:
- start: 2026-11-08T15:53:22Z, both as the commission states;
- mid: 2026-11-08T16:02:22Z, unchanged;
- end: 2026-11-08T16:04:07Z, unchanged.

The branch was `feature/ks-2060-erasure-an-erased-users-wallet-stays-on` = `refs/pull/2099/head` at every reading. This verdict holds for SHA 0d747d09 only.

## BLUF

The diff does what Kam's three KS-2060 cards say:
- erasure clears the users-row wallet;
- the governance row keeps its counters and loses its wallet, stake, power, flags and did;
- the address is blanked from proposals, votes and delegations, and the tallies are kept.

Every statement is keyed by the erased user's id. On real PostgreSQL I planted a second user, a shared delegation, votes on the same proposal and a vote that carries the erased user's address string. No other row or tally changed: 39 of 39 assertions. My harness caught two of my three planted wrong-user defects, and the third was a bad plant (see TESTED 3).

Migration 059:
- It is the minimum. Removing its third statement turns 8 of the seat's assertions red.
- It is idempotent on a populated database: row counts and md5 were equal before and after two runs.
- It has no down migration, and once NULLs exist it cannot be reversed (measured).

The notes are about words and races, not the statements:
- The DPIA's Net effect and P10 claim more than the code does for a wallet held by a legacy participant row (F1).
- The stated "concurrent vote" limit is narrower than the real race. A stale admin registration puts the wallet, stake and DRep flag back on an erased row (F2, measured under forced order).

## Findings

**F1 (Medium, words that a client human reads).** The DPIA and P10 claim no wallet stays in governance. That is not true when the erased user's wallet sits on a legacy participant row.
- Where:
  - `docs/compliance/dpia-art17-erasure-vs-onchain-immutability.md`, Net effect: "no wallet address on the users row or in governance (participant row, votes, proposals, delegations)";
  - the PR body and ticket comment, P10: "naming the old wallet finds no owner (404), because no row or owner holds it".
- Why: `userErasedSubscriber.ts:28-29` (D-4) leaves "a legacy row whose id is no user" to the backfill. `governanceService.ts:602-603` keeps legacy uuid rows on their wallet.
- So, for a user erased AFTER this ships whose wallet is held by such a row:
  - the wallet, stake and votes stay;
  - an admin naming that wallet still lands stake on the row (P10 false).
- The DPIA's "Not yet covered" names only users erased before KS-2060 shipped. The PR's limits name the same.
- FOUND: by reading. TESTED: my harness's legacy row L (`wallet_address='addr_U_shared'`, `id='legacy-uuid-row-L'`) is byte-identical after U's erasure. HOW: `/private/tmp/g266/work/wronguser.cjs` against real PostgreSQL 15.19. Evidence class: MEASURED AT RUNTIME (that the handler leaves the row); READ ONLY (that such rows exist on any box: not measured).
- Fix shape: the DPIA's "Not yet covered" and the PR and ticket limits gain one line: legacy participant rows whose id is not the user's id, until the backfill. P10 gains "unless a legacy row holds it".

**F2 (Medium, unstated limit on a data-destruction path).** A stale read-modify-write undoes the erasure, and it reaches more than the stated "concurrent vote".
- (a) Admin `registerParticipant`:
  - `governanceService.ts:624` reads the row by address;
  - the `dbSaveParticipant` upsert at `:185-190` writes `wallet_address = EXCLUDED.wallet_address` and the stake on `ON CONFLICT (id)`.
- An admin request whose read lands before the handler commits and whose write lands after it puts the wallet, stake and DRep flag back on the erased row. Measured: wallet `addr_U`, stake 9000, vote_power 9000, is_drep true, after the handler had cleared it.
- Nothing re-runs the handler. The PR body, the fragments and the ticket do not name this path.
- (b) `dbSaveProposal` (`:144-167`) rewrites `votes` whole on every call, so the restore reaches more than `castVote`:
  - `cancelProposal` (`:1181`), `finalizeProposal` (`:1100`), `executeProposal` (`:1147`);
  - the 60-second `processExpiredProposals` job (`index.ts:165`), which finalizes on its own.
- Measured: a stale castVote-shaped save put `voterAddress: "addr_U"` back. `proposer_address` stayed NULL, because it is not in the upsert's SET list.
- The handler comment names "castVote and dbSaveProposal". The PR body, fragments and ticket comment name only `castVote` and say "Read, not measured".
- FOUND: by reading. TESTED: a forced interleave (read, then handler commit, then write) on real PostgreSQL. HOW: `/private/tmp/g266/work/race.cjs`. It runs the six handler statements and the two upserts, all extracted verbatim from the head source. Evidence class: MEASURED AT RUNTIME, under forced order. Not measured under real concurrency.
- Fix shape, for the owner: a row lock (`SELECT ... FOR UPDATE`) or a guarded write on these paths, or state the admin path and the dbSaveProposal callers as limits. A regression cell should run this interleave.
- Severity: the window is one request's read-to-write time, but the result is a silent un-erasure.

**F3 (Low).** An event dead-lettered before 059 reaches a box is lost for good, not delayed.
- The precondition says the event "is dead-lettered". It does not say that a subject erased in that window stays uncleared until the backfill. Nothing replays a dead letter into this handler.
- TESTED: the handler's SQL on a database without 059 fails `23502 null value in column "wallet_address"` (my pre059 database), which matches the seat's E0. Evidence class: MEASURED that it fails; READ ONLY that nothing replays it.
- Fix shape: one clause in the PR body's "Before this deploys".

**F4 (Low, latent reader).** One frontend reader would crash on a NULL wallet, but no path reaches it at this head.
- Where:
  - `frontend/issuer/src/components/governance/GovernanceDashboard.tsx:477` calls `p.walletAddress.substring(...)`, typed `walletAddress: string` (`:94`);
  - `proposerAddress: string` (`:66`) is typed but never rendered.
- That would throw on a NULL wallet, but the list is fetched with `?isDRep=true` (`:201`), and the clear sets `is_drep=false` in the same statement as `wallet_address=NULL`. No path at this head writes a NULL wallet with is_drep true.
- I found no other reader that crashes on NULL or miscounts. Instrument: `git grep -i` over `services`, `frontend`, `sdk` and `packages` (tests and `deploy/` excluded) for the five field names and their snake_case columns, and for string methods called on them. Positive control: the same grep found this file and `auth/routes/wallet.ts:246`.
  - The SDK (`sdk/javascript/src/modules/governance.ts`) names no address field.
  - No other service reads the three governance tables. The api-gateway only proxies.
  - There is no delegation-list route, and POST /delegate cannot return NULL after the 404 guard.
- Evidence class: READ ONLY.

**F5 (Info, rollback).** 059 cannot be rolled back once a NULL exists, and the old image has no 404 guard.
- 059 has no down file. None of the 61 files in `migrations/` is named down, rollback or revert; positive control: 61 `.sql` names listed.
- `ALTER ... SET NOT NULL` after one erasure fails: `column "wallet_address" ... contains null values` (MEASURED).
- If the governance IMAGE is rolled back after erasures but 059 stays, the old `delegateVote` lacks the 404 guard and would store a delegation with a NULL address (READ ONLY). The power involved is 0, so this is inert.
- Pre-059 database plus the new image: F3. 059 plus the old image: safe until the new image has written a NULL (READ ONLY).

**F6 (Info, scope).** Two parts of the diff go wider than Kam's cards. Both are Wednesday's rulings, not Kam's, and both are disclosed.
- (a) 059's three statements. This is Wednesday's ruling (b), wider than the first card's "one statement". It is the minimum the second card's "delegation addresses blanked" needs (measured: with the third statement removed, cells M3, M4, E1-E5 and D-3 go red, 16/24).
- (b) `auth/routes/wallet.ts:489-496` refuses wallet link to every status auth maps to DEACTIVATED. That includes admin-disabled `inactive` and `deactivated` users who were never erased. Kam's KS-2060 card is about erasure.
- Nothing is erased that the cards did not name. `did` and the DRep and committee flags are D-7 and the first card's "vote power".

## TESTED, and how

All runs were in my clone, `/private/tmp/g266/repo` at 0d747d09.

1. **Wrong-user, on real PostgreSQL** (Homebrew 15.19, my own socket-only cluster under `/private/tmp/g266/pg`).
   - Substrate: the three CREATE TABLEs from `docker/init/04-sprint2-service-tables.sql`, which is what docker/init deploys. Migration 002 and `deployment/azure/migrate/init.sql` carry the same NOT NULL columns (read), so they agree.
   - The six statements were extracted verbatim from the head source.
   - Planted: users U (erased), V and X; a legacy row L; proposals by U, V, X and L, with U's vote first and in the middle; V's vote carrying U's address string; a NULL votes column, a non-array votes column, and an already-blank U entry; delegations U->V, X->U, U->X (revoked), V->X and L->V; and X's revoked row carrying U's address string.
   - Result: 39/39. Only U's row, P1's proposer address, U's two vote entries and U's side of D1-D3 changed. Order and every other key were kept.
   - Red control: the same run on a database without 059 threw 23502.
2. **059 on a populated database.** I applied it twice over the seeded rows. Counts (4, 7, 6) and md5 of the participant and delegation rows were equal before and after. All three columns read `is_nullable=YES`, and `UNIQUE (wallet_address)` stayed.
3. **My own planted defects.**
   - Plant 1: blank every vote that has an address. Killed, 3 FAIL.
   - Plant 2: subquery-based. It survived, but only because BLANK_DELEGATOR runs first, so the plant was a no-op by construction. Recorded, not counted.
   - Plant 3: blank the delegate side by delegator id. Killed, 2 FAIL.
   - Plant 4: `jsonb_set` replaced by `v.elem - 'voterAddress'` in the product file. Killed by the seat's real-PostgreSQL suite (2 FAIL) and by stand-in H11. The file's sha256 was restored and verified.
4. **The seat's suite**, `scripts/__tests__/ks2060_059_erased_wallet_and_history.test.sh`: 15/15 cells, 31/31 assertions. With 059's third statement removed: 16 passed, 8 failed. Restored by `git checkout` in my clone.
5. **Seat mutant W01** (no link refusal), reproduced: L1 ×3 and L1b red, exactly as the seat recorded (`red=L1,L1b`). Restored: 16/16.
6. **N08** (ORDER BY dropped). On a 20,000-entry votes array with `work_mem=64kB`, the mutant SQL left 0 entries out of order and blanked all of U's entries. Readers of the votes order: only `castVote`'s `.find` (`governanceService.ts:980`, order-free) and `GET /proposals/:id/votes` (`routes/governance.ts:396`, display). Instrument: fixed-string `git grep -F ".votes"`. No reader depends on the order. The survivor is acceptable.
7. **Duplicate delivery and replay.** A second run of the handler gave six zero counts and a byte-identical snapshot. Out of order: F2's forced interleave.
8. **Suites at head.**
   - governance jest: 386/386, 21 files.
   - originate `ks2060` file: 9/9.
   - auth vitest, whole suite with `--maxWorkers=3`: **1847/1847, 149 files.** So ks949's two cells pass here, and the seat's 2 reds were load timeouts. That file is not in the diff, and no other auth red exists at this head.
9. **check:openapi.** OK at head, and OK on the PR 2073 union tree (`7c98d363`, built from merge-tree 99db8ca7c318 of 2073 head `2684a29d` x 0d747d09). So recomputing the yaml at today's heads changes nothing. Positive control: a one-line drift planted in the yaml gives `CHECK FAIL`, rc 1.
10. **Merge tree on develop fa0592f3.** Clean, tree `cb66091f1204`, equal to the seat's. Develop moved c0e6e744..fa0592f3 over 6 files, none of them on this PR's 25 paths. PR 2073 shares only `secuura-api.yaml`, and both merge orders give one tree, `99db8ca7c318`.
11. **docs-fragments check.** OK, with the 2 ADVISORY lines the seat names.

## NOT tested

- The full open-PR census. The rules allow network only for git fetch, so I could not list open PRs. I relied on the seat's census for the 12 granted holders, and checked only PR 2073.
- The seat's compiled-services proof (P3, P7, P10, P12-P14, P16, P17): not re-run. Redis is not installed, and Docker is NOT RUNNING (the socket is absent), so I did not start it.
- Whole originate suite (2601 tests), the images, Node 24 (this host has v26.8.1), pgbouncer, a booted gateway, the four platform suites, any box.
- Whether legacy participant rows (F1) exist on Kintsugi or demo.
- F2 under real concurrency (forced order only).
- The ticket comment as posted: I read the seat's draft `drafts/comment_ks2060_final.md`, not Linear. The PR body likewise is the draft `drafts/pr_ks2060_body_final.md`, not GitHub.

## Own conduct

- I wrote nothing outside this gate folder and `/private/tmp/g266`. I posted nothing, pushed nothing, and ran no git write verbs on the Secuura checkout (only `git -C ... remote -v` and `config --get`, with `GIT_OPTIONAL_LOCKS=0`).
- In MY clone I set `core.sshCommand` to the project's deploy key for the partial-clone blob fetches. I made temporary edits, each restored by `git checkout` and checked with `status --porcelain`. I created one dangling commit (the union, `7c98d363`) and one ref, `refs/g266/pr2073`.
- The seat's suite deletes its own mktemp directories on exit. I pointed its TMPDIR at `/private/tmp/g266/t`, so those deletions stayed inside my area. I deleted nothing myself.
- I stopped my PostgreSQL cluster (postmaster 72801 is gone). Its data directory is kept under `/private/tmp/g266/pg`.
- **The clone is left in place: `/private/tmp/g266`, 2.4G** (by `du -sh`, which counts node_modules and the PG data directory).
- DevMASTER read 15 GiB free (`df -g`) at start and end.
- Load1 read above 8 twice (`sysctl vm.loadavg`): 8.79 at the shared build, just before the seat's 4-second suite, and 9.14 just before the auth suite. I held the auth suite until load1 read 6.91 and ran it with 3 workers. End load1 was 4.12.
- One `cd` slipped into a command and was refused by the hook; I re-issued it with absolute paths.
- One jest invocation failed on config, not on a kill, and was re-run correctly. It is not counted.
- Logs are in `/private/tmp/g266/logs` and harness scripts in `/private/tmp/g266/work`.
