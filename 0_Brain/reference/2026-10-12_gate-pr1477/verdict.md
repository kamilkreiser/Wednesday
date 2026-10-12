# VERDICT: GO WITH NOTE. PR #1477 (KS-1186), head effe35ce7c1e068a9be8f69f42bc87e54197cb7f

Independent Opus QA gate, 2026-10-12. Read-only toward the Secuura repo. All runs were done in my own clone
(`git clone --no-hardlinks`, scratchpad `g1477/`) with three trees: base f9c7880f91db, head effe35ce, and a predicted merge
onto **current** develop 8dcbddb5a45e (tree 6a04e3c7). GitHub's `refs/pull/1477/merge` is stale: it is built on 96342090,
which is one commit behind develop, so I did not use it.

## Defects
1. **Minor, stale comment at `services/auth/src/repositories/userRepo.ts:372-373`.** The comment says *"The five sibling reads below still
   return `fromRow` unawaited: KS-1186."* That is false at head. Change it in this PR or in a follow-up.
2. **Minor, test coverage gaps in `ks1186-userrepo-fromrow-sites-are-awaited.test.ts`.**
   - The non-infrastructure control exercises only `getUserByIdPreAuth`.
   - The no-fault control reaches `getUserByEmail` only through the legacy arm, because the default mock returns [] for the hash query.
   - Unlike KS-999, the test does not assert the repo log line.
   - All of the cells that discriminate base from head are still correct (see check 2).

No Major defects.

## Checks (all by my own runs)
1. **Diff.** Exactly 2 files: userRepo.ts +5/-5 and the new test +117. The 5 `-` lines are exactly the base `return fromRow(` sites at
   446, 512, 585, 594 and 627. `git diff --check` is clean. The Spark patch (sha256 prefix 1ef68e5653760cbe, matches) carries the same +/- lines.
   Its extra `-`/`+` blank-line pair is byte-identical, so it is a no-op.
2. **Red/green.** The test planted on base gives 5 failed and 7 passed: all five sites are red, and the controls plus KS-999 are green.
   Head gives 12/12. Reverting one `await` at a time reds only its own cell (446, 512, 585, 594 and 627 each give 1 failure).
   Reverting the await at :410 reds the 2 KS-999 cells, so that positive control is live.
3. **Suites and static checks.**

   | Tree | Auth suite | tsc src | tsc on the new test | eslint (userRepo + test) |
   |---|---|---|---|---|
   | base | 86 files / 908 tests | 0 errors | n/a (file not present) | 0 |
   | head | 87 / 915 | 0 | 0 | 0 |
   | merged | 88 / 920 | 0 | 0 | 0 |

   - The first merged run had one 5 s timeout in ks949, which is unrelated. ks949 passed 30/30 alone and the full re-run was 920/920.
   - Controls for the zeros: a planted type error made tsc return rc=2, and a planted `var` plus `debugger` gave eslint 2 errors.
4. **Loopback probe, re-run by me on all three trees** (real mfa, users and errorHandler routes; `probe_*.txt`).
   - **Infrastructure DEK fault:** 500 → 503 with 1 repo log line, on both `POST /api/auth/mfa/disable` and `GET /api/users/lookup`.
     getDek was called exactly once.
   - **Non-infrastructure fault:** 500 → 500.
   - **No fault:** lookup gives 200; mfa/disable gives 401 (body had no password).
   - **Control P7 (infrastructure fault on the SELECT itself):** already 503 on base. So 503 is an existing answer from these functions,
     and this PR only extends it to faults raised inside `fromRow`.
   - Real `SubjectDekProvider.getDek` passes the raw pg error through without wrapping (`packages/shared/src/crypto/subjectDek.ts:173-179`),
     so the classifier sees it in production too.

## Completeness
- After the change, userRepo.ts has 0 `return fromRow(` sites and 0 `rowTo` matches. 7 sites use `return await fromRow(`.
  The positive control for this grep: 5 `return fromRow(` sites on base.
- Every other un-awaited promise return in the file is outside a try/catch: 531, 536, 926, 996, 1040, 1049, 1094 and 1220.
  None of them has a catch that the missing await could bypass.
- **Note:** `listUsersInner` :1040 (`Promise.all(...fromRow)`) has no catch at all, so a DEK infrastructure fault on listings is still a raw 500.
  This is a different bug from KS-1186; it could be a follow-up ticket.
- **Note:** a synchronous plaintext-cutoff throw inside `fromRow` is now also logged under "DB <fn> failed". It is still rethrown as 500, and the message carries no PII.

## 503 vs 500 interplay (no new behaviour found)
- **Gateway breaker:** `api-gateway/src/routes/proxy.ts:206-212` counts any status from 500 to 599 the same way.
- **Retries:** `ServiceClient` already retries every 5xx, and nothing in services or frontends uses it. No retry predicate anywhere references status.
- **Issuer UI:** `frontend/issuer/src/utils/errorHandler.ts:113-116` maps 500, 502 and 503 to the same message.
- **Health checks:** none use these lookups.
- **Auth code:** nothing branches on ServiceUnavailable.
- **Spec:** the OpenAPI spec already declares 503 on mfa/disable, users/lookup and login.

## Not checked
I did not run the probe against a real Postgres or a real KMS/KEK. I did not run the full CI pipeline or any service other than auth.
