PR 2158: GO WITH NOTES
PR 2161: GO WITH NOTES

# Gate 302, TIER 1 (Opus): PR 2158 (KS-2145, Seat Y 12th code / Y 13th raise) and PR 2161 (KS-1991, Seat T 23rd)

Gated 2026-11-10 02:37Z to 03:10Z. Findings only. I posted, commented and mailed nothing. Nothing was written in !CODING.

## Pins (ls-remote from the shared checkout, read verbs only)
| ref | start 02:37:39Z | end 03:09:16Z |
|---|---|---|
| develop | d3e663692a8f414f16610236259cab14b27ff0f7 | **0e6479d7b6c06b6f8a77aae1cbad167afbdaa089 (MOVED)** |
| PR 2158 head | 74364b18dcf4e90470a58d3dd4974314b89eae5d | same |
| PR 2161 head | 0e50defb7819fe53a92ef6711a8a91e6b2d20f04 | same |
| PR 2087 head (granted vs 2158) | 954af815c7b7… | same |
| PR 2138 head (granted vs 2161) | fdf80425e9d5… | same |

Develop moved once during the gate: commit 0e6479d7, "Refs KS-2127: the pre-push hook runs the preflight when its git diff fails". It touched four files: `.githooks/pre-push`, `Blockchain/Dev/scripts/__tests__/ks2127_pre_push_failing_diff.test.sh`, and two KS-2127 fragments. Neither PR shares a path with it (0 shared; the control, the moved set against itself, gave 4). It changed 0 originate paths. Merge-tree of each head onto the new develop is clean: 2158 rc 0 (tree 988f08678ea4), 2161 rc 0 (tree 71366e0862d7). The all-four merge (develop + 2161 + 2138 + 2158 + 2087) also merges onto the new develop with rc 0. My originate results therefore stand on 0e6479d7. I did not re-run docs-fragments on 0e6479d7.

Both PRs were cut from 07d4218e9776. Develop moved from there to d3e663692a8f (PR 2121: a shell test, ks570-proxy-mount-auth.test.ts and two KS-2131 fragments). That move shares 0 paths with either PR.

## HOW (instrument and controls)
- Method: a blobless clone in this session's scratchpad (`…/scratchpad/g302/repo`), with PR heads at `refs/p/<n>`. Sparse worktrees: `w/dev` (develop d3e66369), `w/a` (2158), `w/b` (2161), `w/base` (07d4218e) and `w/m` (merge trees). Their `node_modules` and `packages/shared/dist` are read-only symlinks to `worktrees/s-t23-ks1991`'s install, the same method as gate 298.
- Jest: `jr.sh` waits until load1 is under 8, then runs jest under nice. Every jest start logged load1 under 8 (highest 7.97). tsc and eslint ran under nice while one mutant jest was running (load1 7.47 at that point).
- Real PostgreSQL: my own scratch cluster, Homebrew 15.19, `initdb` in `…/g302/pg`, port 55302, trust auth, fixture role `g302`. It is now stopped with `pg_ctl stop` and was not removed.
- Mutants: `mut.py` and `mut2.py` apply an exact-string replacement (the old string must occur exactly once), run the named jest files, list the ✕ cells, and restore the file bytes. sha256 is asserted after each restore. `git status` was clean afterwards apart from the symlinks.
- Merge controls: a planted same-line edit conflicts (rc 1) against each PR, on adminConfig.ts for 2158 and verification.ts for 2161.
- Scratch size at the end: 431 MB. DevMASTER had 92 GiB free at the start and at the end. No rm outside the scratchpad, and no fetch or write verb in !CODING.

## PR 2158 (KS-2145): FOUND / TESTED
1. **Diff:** 4 files, +236/-12, exactly as stated: adminConfig.ts, one new test file and one cheat+flow fragment pair. One commit. Title and commit start `Refs KS-2145`.
2. **Behaviour, my reads:**
   - originate `authenticate` sets `req.user` from the RS256-verified JWT. `tenantId` is the declared optional claim, and the auth service signs it as `user.tenantId`.
   - The gateway sets `x-tenant-id` to the override only when `isPlatformRole` is true, else to the token's tenant (api-gateway auth.ts 696-702 at develop). So the test's `authenticate` stand-in models the gateway truthfully, and the recent-activity read (unchanged; it uses `req.tenantId`) resolves to the ORG_ADMIN's own tenant.
   - `isPlatformRole` (shared keyRevokePolicy.ts 140) applies an ASCII fold and returns false for any non-string role.
   - D1 holds as ruled: the header is ignored for a non-platform caller (200); no usable tenant gives zero counts, an empty activity list and no query; the non-platform path never enters `runWithPlatformScope`, for the anchor count as well as the other counts.
3. **Red-first re-run:** the 7 cells against develop's handler give 4 red (C1, C2, C3, C3b) and 3 pins green (C4 to C6). At the head, 7 of 7 pass. Both match the author's claim.
4. **My own mutants, 10 of 10 caught by the cells named for them:**
   - G1b: platform for any role → C1, C2, C3, C3b
   - G2: non-platform caller reads the header → C1
   - G3: organizationId used instead of tenantId → C1, C2
   - G4: platform scope always → C1, C2
   - G5: anchor count alone under platform scope → C1, C2
   - G6: anchor count unbound → C1, C2
   - G7: early return removed → C3, C3b
   - G8: UUID shape check on the claim dropped → C3b
   - G9b: platform override ignored → C4
   - G10: users count unbound → C1, C2, C4

   My first G9 broke compilation (TS6133, 0 cells ran), so I replaced it with G9b. My first G1 matched two places, and the runner refused it.
5. **Statements Wednesday required, checked against the seat's body draft:** the draft's sha1 (trailing newline trimmed) equals the read-back `body_sha1` afffa3b3… recorded in `create_pr_ks2145.json`. All three required statements are present:
   - (a) the deviation (`req.user.tenantId`, not resolveTenantId or organizationId, migration 017, UUID-shaped only, line 1193);
   - (b) the 17 board-candidate lines. I re-grepped them at develop and the set is exactly 846, 876, 894, 920, 1283, 1681, 1683, 1710, 1747, 1781, 1979, 2118, 2143, 2198, 2201, 2262, 2280;
   - (c) PR 2087 is not the seat's.

   The behaviour-change sentence and the ignored-not-refused (200) wording are present. See G302-2158-1 for the strength of the line-1193 sentence.
6. **No other behaviour changed.** Platform roles keep the old queries and scope (C4 to C6 pins and my G9b). The ORG_ADMIN path now runs under the request-tenant RLS context instead of platform scope; that is the intended change.
7. **Closing words:** none in closing form in the title, body draft, commit or the KS-2145 comment draft (regex with a positive control). The only hyphenated key is KS-2145, and there is no at-sign in the PR text.
8. **Census:**

   | tree | suites | cells | result |
   |---|---|---|---|
   | develop d3e66369 | 220 | 2592 | all pass |
   | 2158 head | 221 | 2599 | all pass |
   | develop + 2161 + 2138 + 2158 + 2087 | 225 | 2654 | all pass |

   The first two rows match the author's figures.
   - tsc (originate tsconfig): rc 0 at develop and at the head.
   - eslint on the 2 changed files: 0 problems. The control, a planted unused variable, is reported.
   - docs-fragments check: OK. A planted literal section number gives FAIL with 2 findings. The 2 ADVISORY lines also appear at develop.
9. **Merge:**
   - With PR 2087's head: rc 0, tree c65cd261f9fe, equal to the seat's.
   - With develop: clean, both before and after develop moved.
   - Open-PR census by pull refs 2040 and above: the only PRs on adminConfig.ts are 2087 (open, granted) and 2060. 2060's head subject is on develop as cfb6c157, so it was squash-merged. Control: PR 2087's three paths appear.

## PR 2161 (KS-1991): FOUND / TESTED
1. **Diff:** 11 files, +1235/-23, exactly as stated: documents.ts, verification.ts, verificationV2.ts (comment only), the new script, 5 new test and helper files, and the fragment pair. No migration, spec, workflow, certifications.ts or certificationRepo.ts.
2. **Behaviour, my reads:**
   - `registerInPlatformRegistry` now rejects on any failure. It reads back the tenant row's `created_at::text` by external_id and tenant under the tenant GUC, and throws if the row is not found. Its insert carries that clock with `ON CONFLICT … created_at = LEAST(…)`.
   - The create route awaits it before the event, the anchor and the 201. The catch logs the stable code `KS-1991 REGISTRY_WRITE_FAILED` and answers 201.
   - `respondForExisting` registers before its 200.
   - In multi-tenant mode `req.db` is built on `manager.getPool(tenantId)`, the same pool the read-back uses. Both documents.created_at and the registry created_at are TIMESTAMPTZ, so the text round trip keeps the offset.
   - Backfill: dry run is the default, and `--apply` must be explicit. It inserts only with `ON CONFLICT DO NOTHING` after checking either hash form. Erased (`metadata @> {"anonymized":true}`), deleted and empty-hash documents are excluded. Non-active tenants are skipped. It uses the earliest eligible document per hash.

   These match O-1 to O-7 as ruled.
3. **Red-first re-run:**
   - Unit, against develop: 9 red and 3 pins (C1f, C1d, C1e3). Integration rank file, on my own PostgreSQL 15.19 cluster: 6 red and 4 pins (CONTROL, BEFORE-backfill, NATURAL, SKEWED-NOCERT). Both match the author.
   - At the head: unit 12/12, integration 33/33 (23 backfill cells on both registry shapes, including C2k and C2l `main()` end to end, plus 10 rank cells over the real v1 and v2 routers).
4. **My own mutants, 16 of 16 caught by the cells named for them:**
   - T1: create not awaited → C1c
   - T2: re-POST does not register → C1e
   - T3: failure silently swallowed → C1b, C1b2, C1e2
   - T4: the function swallows again → C1a, C1h, C1i
   - T5: upsert overwrites created_at → C1g, LEAST-1
   - T6: JS clock instead of the document clock → C1g, G-CAP-9-SKEWED, LOOKUP-NO-LOCAL-ROW
   - T7: not-found registers anyway → C1h
   - T8: backfill checks the bare form only → C2c
   - T9: backfill registers erased documents → C2d
   - T10: backfill registers deleted documents → C2d
   - T11: backfill takes the latest document, not the earliest → C2g
   - T12: backfill updates existing rows → C2f, C2b
   - T13: dry run writes → C2e
   - T14: backfill writes the bare form → C2h
   - T15: backfill reads suspended tenants → C2i
   - T16: backfill writes a null clock → C2a, G-CAP-9-UNREGISTERED-BACKFILLED

   On T13: this is the seat's M2.6 shape. Only C2e reddened, not C2k or C2l, which matches the seat's over-wide-declaration note.
5. **Statements Wednesday required, checked against the seat's body draft:** the draft's sha1 (trailing newline trimmed) equals the read-back `body_sha1` 1c767a13… in `pr_record.json`. All present:
   - O-1 reasoning in two sentences, with the stable code and the backfill as the repair;
   - the O-6 versus O-7 "two different rules" line;
   - the mandatory "The backfill is not run by this PR" section: it writes data; it was tested only on a disposable cluster; kintsugi, demo or any live box waits for Kam; demo is frozen (card named); what the operator reads first;
   - KS 1647 in words only;
   - in the READY: Node v26.8.1 not LTS, the over-wide M2.6 declaration, the mutant replacements, and O-5 as a board follow-up.

   The fragment pair has the ruled exact slug.
6. **No other behaviour changed:** see G302-2161-1 to -3 below. Single tenant (no manager) is unchanged (C1f). A different-bytes re-POST is still 409 and registers nothing (C1e3).
7. **Closing words:** none in closing form in the title, body draft, commit or comment draft. The only hyphenated key is KS-1991. The body's single at-sign is the SQL `@>` operator inside a code span, not a mention.
8. **Census:**

   | tree | suites | cells | result |
   |---|---|---|---|
   | develop | 220 | 2592 | all pass |
   | 2161 head, first run | 222 | 2596 | 1 suite failed |
   | 2161 head, re-run | 222 | 2604 | all pass (matches the author) |
   | develop + 2161 + 2138 | 223 | 2630 | all pass (2161 integration 33/33 on this tree too) |
   | develop + 2161 + 2138 + 2158 + 2087 | 225 | 2654 | all pass |

   The suite that failed on the first run is ks488-smtp-opt-in. It hit TS2300/TS2451 duplicate identifiers shared with ks1937, two script-mode test files that this PR does not touch. It passes alone (8/8). This is an order-dependent ts-jest flake, not this PR's (see NOTES).
   - tsc rc 0.
   - eslint on the 9 touched files (8 originate files and the script): 0 problems.
   - docs-fragments: OK. A planted literal section number in the flow fragment gives FAIL with 2 findings.
9. **Merge:**
   - With PR 2138's head: rc 0, tree 13ead6a75bdb.
   - With PR 2158: rc 0.
   - With develop: clean, before and after it moved.
   - Pull-ref census: documents.ts is also touched by 2054 and 2103, both squash-merged (subjects a65ae7ed and 64671e97 are on develop). verification.ts and verificationV2.ts are touched only by 2138, which is granted.

## Findings
- **G302-2158-1 (LOW, statement precision; no code change needed).** The PR body, the code comment and the READY say adminConfig.ts "passes `req.user.tenantId` as `callerTenantId` to the key-revoke policy (line 1193 at develop)". At develop, line 1193 is `callerTenantId: (req as any).user?.tenantId` inside the refusal's `logger.warn`. The policy call itself is line 1181, `decideKeyRevoke((req as any).user, …)`, which reads `user.tenantId` inside `decideTenantAccess` (shared keyRevokePolicy.ts). The substance is true: it is the same verified claim, and the policy does read it. But the cited line is a log field, not the policy input. A body edit only on a ruling (rule (d)).
- **G302-2161-1 (LOW, unstated behaviour on the re-POST path).** `respondForExisting` registers with `title: title`, the retry request's body title, while documentType and status come from the stored document. Because the upsert sets `title = EXCLUDED.title`, an idempotent re-POST that carries a different title now rewrites the registry row's title away from the stored document. Before this PR the re-POST wrote nothing to the registry. No cell pins it: C1e checks id, hash and tenant only. Whether anything shows the registry title is UNMEASURED; I found no read of it in verification.ts beyond crossTenantLookup's `SELECT *`.
- **G302-2161-2 (LOW, availability coupling not bounded in the text; inside O-1 as ruled).** The create now awaits two pool round trips: the tenant read-back and the platform upsert. The platform pool is `max: 3`, `connectionTimeoutMillis: 5000`, with no statement timeout (shared tenant-pool-manager.ts 157-172). A slow or unreachable platform database therefore adds up to about 5 s per create at the acquire step, or an unbounded wait on a hung query, before the 201. Before this PR the create never waited. The body says "waits for the cross-tenant registration" but not the bound. A note for Wednesday, not a defect against the ruling.
- **G302-2161-3 (INFO).** The body, fragments and ruling say the ERROR log carries "document id and tenant id only". It also carries `error`, the driver message (cell C1b asserts the keys documentId, error and tenantId). The messages I could construct (FK, uuid syntax, varchar length, not-found) carry no hash and no title.

## NOTES (not findings against these PRs)
- ks488-smtp-opt-in.test.ts and ks1937-email-service-logs-never-carry-the-recipient-address.test.ts both declare `EmailModule` and `saved` at script scope. Under ts-jest this is an order-dependent TS2300/TS2451 flake: it failed one whole-suite run at the 2161 head and passed on the re-run and alone. A board candidate.
- The Y lane's line numbers are at 07d4218e. adminConfig.ts is unchanged between 07d4218e and develop, so they still hold.

## NOT TESTED
- The live PR bodies, titles and GitHub comments. I had no authenticated GitHub API. I read the seats' drafts, which hash equal to the seats' own recorded read-backs, so this is custody evidence, not a live read.
- Linear comments c59b1112 and c1ee40c2, and ticket state.
- The open or closed status of PRs: the census used pull refs plus squash-merge subjects, not the PR API.
- The four platform suites, any live stack or box, Node LTS.
- A tsc config that includes test files: covered only by ts-jest diagnostics on every run.
- The seat's T23 claim that the tenant-pool port defect affects deployments on non-5432 ports: not re-measured.
- docs-fragments on the moved develop 0e6479d7.
- The RLS and real-database behaviour of PR 2158: its cells are mock-based, as the PR says.
