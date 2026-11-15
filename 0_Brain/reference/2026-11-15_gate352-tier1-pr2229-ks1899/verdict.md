PR 2229: GO WITH NOTES (at head 03141ad9ba97b3a9d40f3ccc53b4f6190e9ca0df; tier 1)

Gate 352 (tier 1, Opus), 2026-11-15 04:45Z to 04:57Z (15:45 to 15:57 AEDT). Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub. Nothing was written under `/Volumes/DevMASTER/!CODING/`.

**Pins.**
- First pin: `gh api` at 04:45:50Z, then `git ls-remote` at 04:46:14Z (`scratch/pin1.out`).
- Re-pin: `gh api` at 04:55:47Z (`scratch/pin2.out`). My second `ls-remote` was refused with "Permission denied (publickey)" because the deploy key was not exported in that shell, so I re-pinned with `gh api` instead.

| Ref | SHA | Moved between pins? |
|---|---|---|
| develop | 4e4347818772cf259cd3b4849ea576b7495f3453 | No |
| refs/pull/2229/head | 03141ad9ba97b3a9d40f3ccc53b4f6190e9ca0df (open, not merged) | No |
| refs/pull/2131/head | 89081fae75e54e78e509d50a81cb0cd82c00eedd | No |

**What the PR is.**
- It is ONE commit, on develop 48883ba5976b, as the READY says.
- develop has since moved by one commit (4e4347818, KS-1493). That commit touches only `api-gateway/src/__tests__/ks1493-…test.ts`.
- `merge-tree --write-tree` of develop × head is clean in both orders and gives tree 7f0f3b307f2d. I committed that tree locally as merge probe afc0d7339ce4, which was never pushed.
- numstat:
  - `credentialRepo.ts` +19 -2
  - `routes/credentials.ts` +3 -1
  - the new test file +324

## FOUND

**G352-2229-1 (Low; design, Wednesday's call, not a NO GO). If `revoke()` is called without `reader`, it is NOT bound (it fails open).**
- `revoke(id, reason?, reader?)` skips the creator rule whenever `reader` is omitted.
- Nothing in the types forces a caller to pass `reader`. The opposite holds for `store()`, whose default `OWNERLESS` fails closed.
- Census, by `git grep -F 'revoke('` across `services/vc-issuer` at the head, with `credentialRepo.*` member uses counted per file:
  - The ONLY product caller is `routes/credentials.ts:321`, and it passes `req`.
  - `routes/status.ts` calls `manager.revoke` (the status-list manager) and never calls `credentialRepo.revoke`.
  - `revocationResolvers.ts` mentions `credentialRepo.revoke` only in a comment. Its one call is to `getById`.
  - Callers without a reader are tests only: `credentialRepo.test.ts:71,141,148`, plus the new file's O5 and R5.
  - `ks1959`'s `revoke(...)` is an HTTP helper (`:171`), not the repository function.
  - Positive control: the same search finds the route call, the definition (`credentialRepo.ts:546`) and the three builder-named test lines.
- So today no caller is unbound, and the builder's census claim is correct.
- The open default is pinned. My `reader_required` mutant (`!reader ||`, i.e. fail closed when no reader is given) turns red O5, R5 and 1 cell in `credentialRepo.test.ts`.
- The cost: a future second product caller that forgets `reader` gets an unbound revoke, which is the KS-1899 defect again.
- The builder declared this (gate point 1) and took it as a fallback, with no ANSWER to its plan mail. The F36 rulings file does not rule on it.
- **Action:** none for this PR. If Wednesday wants it closed, file a follow-up for a required principal: a bound wrapper (the KS-1683 pattern), with the three `credentialRepo.test.ts` calls migrated.

**G352-2229-2 (Low; measured). On the memory fallback, the creator now sees a revoke that was NOT saved.**
- KS-1684's owner write runs before the UPDATE, as the memory write already did under ruling (a) on KS-1959. So when the UPDATE throws (503 "Retry the revoke."), memory keeps the revoked copy WITH its owner.
- My probe P1 (`scratch/gate352-probe.test.ts`, the builder's harness plus 2 cells):
  - The creator's revoke answers 503, and the stored row stays unrevoked.
  - Then, with the SELECT throwing, the creator's GET gives **200 with `revoked: true`**.
  - A foreign caller still gets the 404.
  - A healthy GET shows the row unrevoked.
- The same cell over develop's product is RED: there the creator got 404, because the memory copy had no owner.
- This is not a leak: only the creator is admitted, and the cloak holds. It is an availability change that can show an unsaved state, on the fallback path only.
- It belongs with KS-1900 and KS-1993, the follow-on rows already ruled. Say it in the KS-1993 brief.
- **Action:** none for this PR.

**G352-2229-3 (Info; measured). The route's own pre-check is now redundant, and no test pins it.**
- My `route_no_precheck` mutant drops the route's `mayReadCredential` check and keeps only `!record`. The WHOLE vc-issuer suite stays green: 884/884.
- The reason: the repository refusal now produces the same 404 bytes (O4 ×7, R6).
- This is defence in depth, and the builder chose it (gate point 2). Nothing is wrong with it, but if someone deletes the pre-check later, no cell will notice.

**G352-2229-4 (Info; measured). Two mutants survive; both are equivalent under today's invariants.**
- `owner_overwrite` (always `memoryOwners.set`, with no `has` check): 884/884 green. It is equivalent because owner columns are never rewritten (`store()`'s ON CONFLICT and `loadFromDb` set the same owner).
- `getById_read` (take the credential from a second `getById` read instead of `record.credential`): 884/884 green. It is equivalent in a single process. With two reads it would open a check-then-use gap, which the head closes by using the one record.
- Neither is a test gap that matters now.

**G352-2229-5 (Low; stale cell text outside the write set).**
- `ks1116…test.ts:779` cell Q1 is titled "revoke() puts a DB row into memory with NO owner entry". Its comment says Alice "is refused here too, which is an AVAILABILITY defect (NOTE 2, ticketed), not asserted".
- After this PR, both statements are false. The owner entry IS written (R4), and Alice is admitted (R3b).
- The cell still passes, and it still pins what it asserts (Bob 404).
- **Action:** a board-seat candidate filing to retitle it. Nothing is needed in this PR, because the file is not in its grant.

**G352-2229-6 (Low; body wording).**
- The body's merge-tree line says "rc 0 (0 clean, 1 conflict)" for both orders against PR 2131, which contradicts itself.
- What I measured:
  - head × 2131 rc 0 and 2131 × head rc 0, the same tree e32de392f673, with no conflicted paths;
  - planted control (an edit to `presentations.ts:344` committed on top of the head), rc 1 in both orders, naming `presentations.ts`.
- The conclusion (clean) is right; only the labels are wrong.
- The body's suite numbers were measured on the old base 48883ba5. At the current develop they are identical (below).

## TESTED

**Q1. Same rule as the route, refusal before any write, every caller updated.**
- **Same rule (read at the head).**
  - `revoke()` calls `mayReadCredential(reader, record.owner)` (`credentialRepo.ts:553`). The import is from `../ownership` (`:23`), the same function the route uses at `routes/credentials.ts:310` and that GET `/:id` uses at `:280`. No copy exists.
  - `mayReadCredential` (`ownership.ts`):
    - a usable `userId` claim is required;
    - an owner-less row goes to `ownerlessCredentialReadable`: `isPlatformRole` (SYSTEM_ADMIN or SUPER_ADMIN, ASCII case fold) AND a tenant claim equal to the row's tenant. This is KS-1906.
    - otherwise `mayRead`: the same userId AND the same tenant.
- **Same rule (measured).**
  - R2: SYSTEM_ADMIN and SUPER_ADMIN of the row's tenant pass.
  - R1o: OWNER, ORG_ADMIN, and SUPER_ADMIN of another tenant are refused.
  - My `rule_mayRead` mutant swaps in `mayRead`, the presentations rule. It turns R2 red (SUPER_ADMIN refused) and R1o red (ORG_ADMIN admitted).
  - My probe P2: through the route, on a memory-only owner-less credential, ORG_ADMIN gets 404 and SUPER_ADMIN of the tenant gets 200, at the head.
- **Refusal before any write.**
  - Order in the code: `getRecordById` (a read) → refusal `return undefined` (`:553`) → the revoked copy is built → `memoryStore.set` → `memoryOwners` set-if-absent → UPDATE.
  - `refusal_after_memory` mutant: R1m ×7 red.
  - `refusal_after_update` mutant: R1 ×7, R1m ×7, R1o ×3 and R6 red (18).
  - `no_refusal` mutant: the same 18 red.
- **Cloak.**
  - The route maps `undefined` to its existing 404 `'Credential not found'`.
  - R6 is byte-identical to an unknown id.
  - My `route_refusal_403` mutant turns R6 red. O4 does not go red under it, because the route pre-check answers first (G352-2229-3).
- **Callers:** see G352-2229-1. There is one product caller, and it is updated: `route_no_req` turns R6 red.

**Q2. KS-1684.**
- R3: a DB-only row is revoked by its creator through the route. Then the SELECT throws.
  - The creator gets 200 with `revoked: true`.
  - Bob gets 404, byte-identical to an unknown id.
- R3b: the same, with the DB unavailable instead.
- R3c: an owner-less row, revoked by a platform admin of its tenant. On the fallback, that admin still reads it, and tenant 2's admin gets 404.
- All of these are green at the head. All are red over develop's product (red-first, below).
- Mutants: `no_owner_write`, `owner_ownerless` and `owner_wrong_key` each turn R3, R3b, R3c, R4 and R5 red (5).
- O6 (an owner set by `store()` is kept): green.
- Also see G352-2229-2: the creator's view after a failed (503) revoke.

**Q3. The KS-1959 503 path and every existing cell.**
- The UPDATE / 503 block is byte-unchanged in the diff. O3 is green: 503, fixed text, row unrevoked.
- Per-cell comparison of the vitest JSON (develop run 1 vs head run 1), keyed by file + fullName:
  - 847 develop cells; 0 missing at the head; 0 changed status.
  - 37 new cells, all in the new file.
- This includes:
  - all of `ks1959-revoke-write-fails-closed` (cell Z: 503 + text);
  - `ks1958` "revoke is unchanged … reads through memory and answers 200" (the builder's gate point 3; `revoke()` now reads through `getRecordById`, which has the same memory fallback as `getById`);
  - `ks1851` and `ks1906`, the revoke binding.

**Q4. Red-proof, reproduced by me (vitest JSON, filter `ks1899-ks1684`).**

| Run | Result |
|---|---|
| Head | 37/37 |
| develop product (both product files from 4e434781) | **23 failed / 14 passed**: R1×7, R1m×7, R1o×3, R6, R3, R3b, R3c, R4, R5. Equals the READY. |
| `no_refusal` (delete `:553`) | 18 red: R1×7, R1m×7, R1o×3, R6. Equals the READY's M1. |
| `no_owner_write` (delete `:569`) | 5 red: R3, R3b, R3c, R4, R5. Equals M2. |
| `route_no_req` | 1 red: R6. Equals M3. |
| Mine: `rule_mayRead` | 2 red: R2, R1o |
| Mine: `refusal_after_memory` | 7 red: R1m×7 |
| Mine: `refusal_after_update` | 18 red |
| Mine: `reader_required` | 2 red in the file (O5, R5) + 1 in `credentialRepo.test.ts` (whole suite) |
| Mine: `owner_ownerless` | 5 red |
| Mine: `owner_wrong_key` | 5 red |
| Mine: `route_refusal_403` | 1 red: R6 |
| Mine: `owner_overwrite` | 0 red. Survivor, equivalent (G352-2229-4). |
| Mine: `getById_read` | 0 red. Survivor, equivalent (G352-2229-4). |
| Mine: `route_no_precheck` (whole suite) | 0 red of 884 (G352-2229-3) |

- Every plant was restored with `git checkout HEAD --`.
- `hash-object` read back the head blobs every time: e93e2bca (repo) and 38f3ea32 (route).
- All three worktrees end at porcelain 0.

**Whole vc-issuer suite (Node v26.8.1; runs interleaved; load average about 23-25).**

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop 4e4347818772 | 29 files, 847/847, rc 0 | 29 files, 847/847, rc 0 |
| head 03141ad9ba97 | 30 files, 884/884, rc 0 | 30 files, 884/884, rc 0 |
| merge probe afc0d733 (tree 7f0f3b30) | 30 files, 884/884, rc 0 (same cell set as head) | not run |
| head with develop's product | 861 pass / 23 fail; all 23 are the new cells | not run |

847 + 37 = 884. This equals the READY's numbers on the old base.

**Static checks.**

| Check | Result |
|---|---|
| `tsc --noEmit -p services/vc-issuer/tsconfig.json` | rc 0 at dev, head and merge |
| tsc, planted-error control | rc 2, 2 errors |
| `npm run check:test-types` | rc 0 at dev and head; vc-issuer 0 errors (43 files at dev, 44 at head) |
| eslint on the 3 changed files, absolute paths | rc 0, 0 lines |
| eslint, planted control | rc 1 (no-debugger) |

The planted file was restored and its blob read back e93e2bca.

**Body.**

| Check | Result |
|---|---|
| `## Test Evidence` | present (1) |
| PREFLIGHT line quoted verbatim | 1 hit; the body says it "is not a pass" |
| Self-hold regex | 0 hits; its control hits |
| Close-word regex | 0 hits; its control hits |
| Title | starts `Refs KS-1899:` |

## HOW
- **Clone:** `scratch/clone`, made with `git clone --reference` to the Blockchain project's object store (read-only alternates).
  - It was fetched with that project's deploy key via a one-shot `GIT_SSH_COMMAND` inside `scratch/clone.sh`.
  - Push URL `DISABLED`, re-checked at the end.
  - Every write verb ran through `scratch/g.sh` against MY clone.
- **Worktrees** (sparse `Blockchain/Dev`), each with its own `npm ci --ignore-scripts` and a `packages/shared` build:
  - `wt-dev` at 4e4347818772;
  - `wt-head` at 03141ad9ba97;
  - `wt-merge` at the local merge probe afc0d7339ce4.
- **Scripts:** `setup.sh`, `plant.py`, `plants.sh`, `suites.sh`, `static.sh`, `mt_control.sh`.
- **Outputs:** `out-*`, `suites.out`, `tsc-*`, `ttypes-*`, `eslint-*`, `mt_*.out`, `pr2229.json`, `pr2229_body.md`.
- **Probe:** `gate352-probe.test.ts`. It ran inside `wt-head`, then was moved out to `scratch/`, and the worktree went back to porcelain 0.
- **Local-only commits in my clone:** one planted-conflict commit (eeb3c80b) and one merge probe.
- **GitHub reads:** `gh api` GET with the Blockchain gh config (`gh auth status` = kksecura).
- **READY:** read whole from `/private/tmp/wed_newmail/batch_20261115T043638Z.txt`. I also read the F36 rulings file.

## NOT TESTED
UNMEASURED:
- a real PostgreSQL (every cell uses the in-memory fake table);
- a second replica (R6's scripted owner change stands in for one);
- a running vc-issuer or the local stack;
- the hook's 3 skipped legs;
- Schemathesis, Akto, Playwright and k6;
- other services' suites;
- Node 24;
- Linear (ticket state and the two comments not read);
- the F 36th HANDOVER (not opened).

The merge probe ran the whole suite once only.
