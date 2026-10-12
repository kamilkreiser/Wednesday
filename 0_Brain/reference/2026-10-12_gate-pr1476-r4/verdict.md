# QA delta gate: Secuura Platform K PR #1476 round 4 (KS-806)

Head: `8e98a40d213a6cdbe5f958a42810f92e06beba0a` (feature/ks-806-the-synthetic-wallet-email-is-collision-free). Gate tier: Sonnet. Client scope: Secuura only.

## VERDICT: GO WITH NOTE

The round-4 claim holds (no product code changed, ks963 is green on the merged tree, the social-guard position is pinned), and the only open items are two test-strength gaps in the new purity pin and an unreadable PR body.

## By my runs

Clone: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/038e4bc7-9b6a-4963-ab5d-359d3201b9e0/scratchpad/gate1476r4/clone`. Dependencies came from a plain `npm ci --ignore-scripts` in Blockchain/Dev (25 s, rc 0) plus `npm run build` in packages/shared. No symlinked node_modules.

1. Prerequisites. The local project clone does not contain f5a2402625a8 or 8f674b3c46e7. After pointing my clone's origin at `git@github.com:Secuura/Distributed_Secuura.git` with the project's read-only-used sshCommand, `fetch origin develop` brought both in (`cat-file -t` returns `commit` for both). The round-3 head 5edcffd12503 came from the r3 bundle.
2. Bundle. `git bundle verify` on the r4 bundle returned rc 0. `list-heads` shows 8e98a40d213a6cdbe5f958a42810f92e06beba0a, which equals the stated head.
3. Product-code claim. `git diff --name-only 8f674b3c46e7 r4 | grep -v __tests__` lists exactly 5 files: `routes/auth.ts`, `routes/users.ts`, `routes/wallet.ts`, `services/passwordLoginGate.ts`, `utils/walletEmail.ts` (all under Blockchain/Dev/services/auth/src). Compared as PR-own deltas (`diff f5a2402 r3` against `diff 8f674b3 r4`, +/- lines only), all 5 are IDENTICAL (10, 11, 33, 5, 34 lines). Direct r3 vs r4 blob compare: `auth.ts`, `wallet.ts` and `walletEmail.ts` are byte-identical. `users.ts` and `passwordLoginGate.ts` differ only by the develop merge (develop changed both between f5a2402 and 8f674b3; the PR-own deltas match). The round-4 commit 8e98a40 touches 2 files, both tests (ks795 +34, ks963 +29). The merge c082d30 has parents 5edcffd and 8f674b3, and `diff --name-only 8f674b3 c082d30` lists only PR files (4 test files plus the 5 product files above), so there is no evil merge. CLAIM CONFIRMED: no product code changed in round 4.
4. services/auth tests on 8e98a40 (develop 8f674b3 merged in), `npx vitest run`: rc 0, 92 files / 983 tests passed, 0 failed. One run only (author did two). Matches the author's figure exactly. A positive control for the earlier broken state is that, before building packages/shared, the same command failed 80 files, so the harness does detect failures.
5. `tsc --noEmit -p tsconfig.json` in services/auth: rc 0, no output. (The first attempt before building shared failed with TS2307; this was my setup, not the PR.)
6. `npm run check:test-types`: rc 0, "92 of them under __tests__; 42 errors: 42 in the baseline, 0 new; 0 stale".
7. Baseline for mutants: ks963 + ks795 files together, 66 passed, rc 0. Each mutant was applied with an exact-match replace (a pattern miss prints PATTERN NOT FOUND, none occurred), the named test files were run, and the tree was restored with `git checkout -- .` (clean afterwards). Script: `mutants.py.txt` beside this file.

Mutant table (RED = the new cells caught it, GREEN = it survived):

| id | mutant | result |
|---|---|---|
| A1 (author's) | canonicalWalletAddress gains `void query(...)` | RED (purity cell) |
| A2 (author's) | allow-list without `Set` | RED (control cell and the real ordering cell) |
| B1 (author's) | social guard moved into the create block | RED (the "matches an existing account" cell) |
| B2 | social guard disabled | RED (3 cells) |
| B3 | reserved-domain check made case-sensitive | RED (the W-ABC@WALLET.LOCAL cell) |
| M8 | canonicalWalletAddress becomes async with a hidden `await` | RED (purity cell) |
| M9 | allow-list gains `ensureWalletRow` | RED (the "unknown helper is refused" cell, which uses that name) |
| M5 | `new Set([ensureWalletRow(...)])` before the lookup in wallet.ts | RED (ordering cell) |
| M7 | `canonicalWalletAddress(await userRepo.createUser(...))` before the lookup | RED (ordering cell) |
| M11 | canonicalWalletAddress reformatted across lines (still pure) | GREEN, correct (no false red) |
| M1 | canonicalWalletAddress calls an unnamed helper `doAudit(...)` | GREEN (false green) |
| M2 | canonicalWalletAddress calls `console.log(...)` | GREEN (false green) |
| M4 | wallet.ts drops the import and defines a local `canonicalWalletAddress` that does `void query(UPDATE ...)` | GREEN (false green) |
| M6 | a tagged-template write (sql`INSERT ...`, no parenthesis) before the lookup | GREEN (limitation of the call-shape scan, which pre-dates this PR) |
| M10 | canonicalWalletAddress refactored to `const lower = ...; return lower;` (benign) | RED (false red) |

## Findings

No Major.

Minor-1 (test strength). The purity pin for `canonicalWalletAddress` is a deny-list of the tokens in the author's description (`await`, `query(`, `fetch(`, `require(`, `import(`, `process.`, `fs`, `db`, plus any assignment), not an allow-list. Evidence: M1 (`doAudit(walletAddress)`) and M2 (`console.log`) both stay GREEN, so a helper that is called "pure" can still reach I/O through any name not in that list. This is the false green the brief asked about. The fix is to make the pin allow-list-shaped: the body may contain only member calls on a named set (`toLowerCase`) and no other call-shaped token.

Minor-2 (test strength). The allow-list in `assertWalletNothingWrittenBeforeLookup` matches NAMES, and the purity pin reads only `utils/walletEmail.ts`. Nothing ties the name used in `routes/wallet.ts` to that export. Evidence: M4 (local impure `canonicalWalletAddress` defined in wallet.ts, with its `query` call outside `getOrCreateWalletUser`) stays GREEN, so the write-before-lookup guard can be bypassed by shadowing. Suggested pin: assert wallet.ts imports `canonicalWalletAddress` from `'../utils/walletEmail'` and does not declare it locally. `Set` has no pin of its own beyond being a builtin; a local `function Set` would pass the same way (not mutated, same mechanism as M4).

Note-1. The purity cell's `/\w\s*=[^=]/` assignment ban also fails a harmless refactor (`const lower = ...; return lower;`, M10 goes RED). It is brittle in the safe direction, so it will cause a false red at some future edit, not a false green. The ordering cell's call scan also does not see tagged templates (M6); that limit pre-dates this PR.

Note-2 (A, Major-1 from round 3, closed). The red ks963 on the merged tree is now green (983/983). The new cells behave as claimed: the two pure helpers pass, an unknown helper (`await ensureWalletRow(...)`) is refused, and A1/A2/M8/M9 all go red. The allow-list does fail closed for any other helper name used directly in `getOrCreateWalletUser` (M5, M7).

Note-3 (B, Minor-1 from round 3, closed). The new cell uses a verified `wallet.local` profile that matches an existing account and asserts the uniform refusal, no social-id write, no mint and no user created. The control with an ordinary address links, so the harness can express a link. B1 (guard moved into the create block) and B2 (guard removed) both turn it red. One scope detail: the guard is `!user && isReservedWalletEmail(...)`, so a profile whose social id is already linked skips it. That is the existing login path and is unchanged by this PR.

Note-4 (C, KS-1498). I could not read the PR body (no `gh` auth in this environment; no local file contains the string KS-1498), so I cannot judge whether the body states it honestly. That is the one open item for the human reviewer. On the code: this PR does NOT make it worse. On develop 8f674b3 the lookup was exact-match on the raw address, so a lower-case login against a suspended mixed-case legacy row also found no row and created a new ACTIVE account, while the mixed-case login found the suspended row (401). The PR keeps that split (presented casing first, then canonical) and its own comment states that a legacy row in an unpresented casing is unreachable without a migration. The new accounts are stored canonical with a hash email that cannot collide with the old `first8...@wallet.local` form. The risk stays High as filed, but it is pre-existing.

Note-5 (process). The first r4 push hit the pre-push hook's clean-room leg SIGABRT ("Abort trap: 6" in `npm ci --dry-run`, api-gateway), and the retry pushed with preflight reporting "12/15 legs ran, 3 SKIPPED (legs 3 4 8, local stack not up)... NOT a pass". The author should not quote that preflight as a full pass.

## NOT tested

- The PR body wording of KS-1498 (not readable here).
- The integration suite, `check:openapi` and `eslint` (not run; the author reports them clean; the diff against develop touches no openapi or lint-relevant product surface beyond the 5 files, but I did not execute them).
- Docker, database-backed or live-stack behaviour (Docker down by instruction): the real `auth_find_user_by_wallet` casing behaviour and the KS-1498 scenario were reasoned from code, not run.
- Preflight legs 3, 4 and 8, and the Kintsugi/demo/production environments (out of scope).
- A second full-suite run (I ran the 983 once; the author ran twice).
