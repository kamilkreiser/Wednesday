GO WITH NOTES
Head 0fffdfba0f9578f23d48112068d1451ea947cd29 (branch feature/ks-657-delete-the-dead-shared-cache-section), develop b27f5fb30f4a912ec2b4b78f5c27281d11e47a87. Round 1 of 2, tier 1. Readings by ls-remote: 05:18 and 05:42 AEDT, both these SHAs, no movement. No commit made.

## FOR KAM, FIRST: deleting redis-security-store.ts is a security decision the card did not put to him

The GO WITH NOTES covers the code only. It does not settle this question.

**Plain answer to Question 1: no, the store is not inside option a on the card's words. The code supports deleting it, but the evidence that someone meant to wire it up never reached Kam.**

- **The card's words.** "Its cache section (15 files) is imported by nothing; only its types are used." "Option b: only if something is meant to use it." The card never mentions a security store, rate limiting, brute force or CSRF. Wednesday said the same in ANSWER 05:40:48Z: "The security store is not in those words."
- **What Kam was told.** The panel line of 2026-11-06 16:41:05 opens "No action needed; two receipts". It says a security store imports the cache, nothing imports the store, it goes too, and "Say if you'd rather keep it." So the scope extension was disclosed. Three things were not in it:
  1. what the store does;
  2. that written documents say it should be wired in;
  3. that part of the problem it was written for is still live (finding F3).
- **What the file does.** `services/shared/src/security/redis-security-store.ts`, 417 lines, holds three stores. Its header says "These replace the in-memory stores for production deployments."
  - `RedisRateLimitStore`: fails open on error.
  - `RedisBruteForceStore`: exponential lockout.
  - `RedisCSRFStore`: 5-minute tokens, timing-safe compare.
  - There is no revocation or session state in it.
- **Written intent, which the card and the ticket trail omit:**
  - `.planning/codebase/CONCERNS.md:26` (2026-03-10, SJP-Secuura, 84b11a928, a generated "map existing codebase" doc): "already exists as a Redis-backed replacement ... wire it up and remove the in-memory originals."
  - The same file, lines 165-166: "Wire `redis-security-store.ts` into all services as the default store."
  - `Notes (MASTER)/Secuura/secuura-continuation-plan.md` (status: archived, 2026-01-10): lists "Redis security stores" under "High Priority Fixed" in a security audit remediation, at a path under `packages/shared` where git shows no such file on any ref.
- **What the history shows.** `git log --follow` gives four commits:
  - 3e21b5826, 2026-02-05, "Security hardening": created it, no ticket;
  - e50dbde98, 2026-02-18;
  - 74a330fc0, KS-657: build and type fix. Its message reserves the retire-vs-wire-up call but names only `src/cache/connection-pool.ts` as the intent in question, not the store;
  - 79145a312, KS-1868, 2026-11-04: catch hardening, three days before this deletion.
  - No commit message on any ref names wiring it. So someone planned it and nobody did it. No ticket I could read in the repo asks for it.
- **Why deleting it is still defensible, for Kam to weigh:**
  - Zero importers (Question 2 below), so nothing at runtime changes.
  - Brute force is live elsewhere and Redis-backed: `api-gateway/src/middleware/security.ts` and `services/auth` lockout.
  - CSRF is live elsewhere: `api-gateway/src/middleware/csrf.ts`.
  - The store is not a drop-in for the gateway's limiter (read: its `increment` returns `{count, resetAt}`).
  - Git keeps the file.

**The question for Kam, READ ONLY evidence:** knowing it is the documented Redis rate-limit, brute-force and CSRF replacement, delete it, or split it from this PR and keep it until a decision on F3? Whether the merge waits for his answer is not my call.

## BLUF

The deletion is technically clean on everything I could run:

- Importers: none, on a frame wider than the seat's.
- Merge tree clean: 269e0f769800.
- Builds exit 0. services/shared 20 of 20. Billing 377 of 377.
- 4 RED reproduced at current develop.
- The 494 floor is right.
- No open-looking recent branch shares a path.

The findings are the authority question above, two docs the PR leaves pointing at a deleted file, one adjacent live limiter gap the PR did not cause, and small test blindness. No finding blocks on code grounds.

## Findings

**F1. DECISION FOR KAM (not a seat finding). Security store outside the card's words.** See the top section. FOUND: `services/shared/src/security/redis-security-store.ts`, `.planning/codebase/CONCERNS.md:26,165,166`, panel line 16:41:05. TESTED: card show, git history, seat mail, chat line. HOW: READ ONLY. Whether Kam replied after 16:41 is NOT established: the local chat source in `kam_msgs.sh` holds no 2026-11-06 messages and the live source needs network I was not given.

**F2. MINOR. The PR leaves live docs naming the deleted code as current.**
- `.planning/codebase/CONCERNS.md:26,165,166` still call the store the "current mitigation" and the fix.
- `BACKLOG.md:293` names `src/cache/redis-client.ts`, and the KS-657 entry still reads as open.
- The seat's frame classed such hits as "notes and docs", and its PR body has 0 mentions of `.planning` or CONCERNS, so the one document stating intent was never surfaced.
- Diff touches neither file (counted 0).
- Recommendation, READ ONLY: reword both in the same or a follow-up change, whichever way F1 goes.

**F3. MEDIUM, PRE-EXISTING, NOT CAUSED BY THIS PR. The gateway's express-rate-limit instances look per-replica, which is the risk CONCERNS.md named.**
- `services/api-gateway/src/index.ts` has 10 `rateLimit({` calls, including `/api/auth/login` at line 981 (max 15 per 15 minutes in production), and 0 `store:` options.
- `rate-limit-redis` is not in its package.json.
- `deployment/azure/services.bicep:731-732`, in `apiGateway`: minReplicas 1, maxReplicas 20.
- `services/api-gateway/src/services/redis.ts:123` says "Rate limit + sessions are both Redis-backed". `middleware/rateLimitEnforce.ts` (per-client) and brute force are; these ten appear not to be.
- `BACKLOG.md` has 0 hits for MemoryStore, per-replica or express-rate-limit.
- Evidence class: READ ONLY. Not driven against two replicas, and the default-store behaviour is the library's documented default, not observed. Recommendation: put it in front of Kam alongside F1 and let an owner measure it. Priority is not mine.

**F4. LOW. The new test's import scan is blind to two shapes.** `src/__tests__/ks657-the-dead-cache-section-is-gone.test.ts`, G4, reads only `from '...'`.
- Planted by me: `require('../cache/redis-client')` in the kept `security/headers.ts` gives suite 20 of 20 and tsc exit 0.
- Planted by me: `src/caching/redis-client.ts` restored under a new folder name gives suite 20 of 20 and tsc exit 0.
- Fix shape if wanted: add `require(` and `import(` to the predicate. MEASURED AT RUNTIME (vitest and tsc on the merge tree). Low because nothing loads this package.

**F5. LOW. The "15 files" does not map to the deleted set, and most of what remains is also unused.**
- At 74a330fc0, `src/` holds 15 files (13 sources, 2 tests), measured, agreeing with the seat.
- Non-test `.ts` in the whole package at that date is also 15, which is the brief's derivation. Both readings give 15; neither picks out 6 files.
- If the card meant all of `src/`, then the kept `audit`, `headers`, `rate-limiter`, `validation`, `logger` and both indexes are "imported by nothing" too. They stay, and `rate-limiter.ts` keeps the in-memory Maps. Control G5 now pins those unused files as must-exist.
- Wednesday's list is explicit about keeping them, so this is not a seat error. It means the ticket's dead-code half is not finished by this PR. READ ONLY for the importer claim; my path searches returned only `types/` consumers.

**F6. INFO. Candidates for a ticket.**
- `ioredis` is declared and now has no reference in services/shared `src`. Nothing breaks: other workspaces use it and the lock is untouched.
- `services/shared/services/redis.ts` imports `redis`, declared in neither root nor package manifest, and `@secuura/shared/cache/redis`, which is in `packages/shared` and does export `CACHE_TTL` at line 172. It depends on nothing deleted. It sits outside tsconfig `rootDir`, is never compiled, and I found no importer.
- `services/shared/package.json` has no `"private"` field. `scripts/publish-shared.sh` publishes only `packages/shared`, so no publish path exists in the repo today.

**Seat row difference, not a defect.** Seat mutant M3 records "1 failed", no build reading. Restoring the real file gave me 2 failed (G2 and G4) and tsc exit 2. Stronger than claimed.

## The commission's questions

1. **Authority:** top section.
2. **Importers.** None in code.
   - Frame, all tracked files at the head:
     - relative paths into `services/shared`, `../shared/{src,cache,security,services,types,dist}`, `service-utils`, the deleted file names;
     - all `tsconfig*` paths and references (45 files in Blockchain/Dev);
     - vitest, jest and vite config: the `../shared/src` hits are `frontend/shared`;
     - dynamic `require`/`import(` forms;
     - 37 Dockerfiles, 15 compose files, 17 workflows (counts equal the seat's);
     - shell, py, js, bicep, yaml and json;
     - `mcp-server/src/package-generator.ts`, which reads only its own `mcp-server/src` and project-root files;
     - customer docs.
   - Identifier sweep for the deleted exports: 0 hits at the head in services and packages. I withdraw its value as a control: the control at c5c26b printed nothing, most likely because my `cut` removed the short `grep -c` lines, so that zero is uncontrolled. Rely on the path search, whose control did fire: it found billing's `../../shared/types` import and `Dockerfile:47`.
   - Only live link: `services/billing/Dockerfile:47` and `billing/src/chargeable-events.ts:23`, into `types/`.
   - Outside the frame:
     - other repositories. Extranet grep returned 0, but its positive control also returned 0, so that zero means nothing;
     - untracked files;
     - published or running images;
     - `.planning` is only a doc reference (F2).
3. **Working copies.** No live caller believes it uses this code.
   - Gateway has its own Redis brute-force in `services/redis.ts` and `middleware/security.ts`, and its own `csrf.ts`.
   - Auth has its own lockout.
   - `packages/shared/src/cache/redis.ts` is the live cache.
   - `packages/shared/src/security/index.ts` holds in-memory duplicates, and only `sanitizeString` was found imported from it by a service.
   - `services/redis.ts`: see F6.
4. **Floor: 494 is right, no finding.**
   - Measured walk counts: 506 at c5c26b, 507 at current develop (`transfer/src/services/transferAccess.ts` arrived), 501 on the merge tree.
   - The comment pins its figures to c5c26b, so it stays true.
   - On the tip, old floor over 507 and new floor over 501 both tolerate exactly 6 lost files.
   - Planted on the merge tree: 6 no-zod files deleted, all 268 cells green; 7 deleted, F2 alone red. So a loss of up to 6 files is invisible to this file. That is the same tolerance as before the PR.
   - The name still fits: the floor is only the blindness guard.
   - Old floor 500 on the merge tree passes by one file, so the move is not strictly forced at the tip, but keeping it would leave no slack.
   - Other floors: line 503 and `entrypoint-corpus` over 350 pass. Full `packages/shared` on the merge tree: 1498 of 1499. The one red, `wallet-signature.test.ts` "accepts a valid wallet signature", also fails at develop in this install, so it is not this PR.
5. **Package and lock:** nothing breaks. Diff touches 0 of `types/`, billing, either manifest or lock, or `services/redis.ts`. Billing's COPY input is byte-identical by that diff. `dist` has 0 cache or redis files, and `dist/index.js` exists. Build exit 0. A Docker image was not built.
6. **Tests.**
   - 4 RED reproduced at current develop b27f5f with only the new file: G1 to G4, all AssertionError, 3 controls pass.
   - Seat mutants reproduced: M1, M3, M8, all killed, build exit 2 on each.
   - Own plants: F4, both survive; floor plants above.
   - The six KS-1868 tests import or mock only `../cache/*` and `redis-security-store` plus the logger. No cell asserts anything about kept code, and the same behaviour in `packages/shared` has its own ks1868 files. Nothing is lost beyond the deleted code.
   - eslint `--max-warnings 0` on 3 files exit 0. `docs-fragments.mjs check` OK.
7. **Merge and overlap.**
   - Clean tree 269e0f769800905f4fac9a4aba538088f50a865a.
   - All 1372 remote branches fetched. Unmerged branches touching `services/shared`, the ks1725 file, the corpus test or CONCERNS: 21 including this one, newest other tip 2026-11-03. I did not check whether any of those 20 is still meant to land.
   - None from the last three days.
   - No open-PR list (see below).

## NOT tested

- Docker image builds, a running stack, the four platform suites, Node 24.
- Other services' suites apart from billing, and the shell suites. A search found no test outside `packages/shared` naming `services/shared`; a test walking all files by another route is not excluded.
- PR open or closed state, and Linear including the KS-657 ticket body and its state (network limited to git fetch, so the seat's In Review vs In Progress note is untested).
- Kam's replies after 16:41 (F1).
- A whole-history pickaxe for `RedisBruteForceStore`: all-refs attempts failed or timed out on the partial clone. Pickaxe succeeded only on `.planning`. So "never wired in any past commit" is NOT measured; it is measured at the head, plus commit messages on all refs.
- Extranet and other repositories (zero with a failed control).
- Seat's other five mutants, tsc with tests in the program, and the seat's claim that leg 14 ran 117 of 117.

## Own conduct

- Findings only. No commit, push, post, box or docker.
- Writes: this file, and the clone at `/private/tmp/g241`, now **removed with rm -rf as the commission directed, and confirmed absent**. The template's no-rm rule says otherwise; I followed the commission's specific instruction.
- Network: git only, using the seat's deploy key through clone-local config.
- `npm ci --offline --ignore-scripts` read the shared `~/.npm` cache, logs redirected to the clone, no registry contact intended. `--ignore-scripts` may explain the wallet-signature red; I did not investigate.
- My first dependency attempt copied the builder checkout's `node_modules` read-only. It carried zod 3.25.76 against a lock of 4.6.7, and the resulting build errors were an artefact of that copy. I discarded it, and no finding rests on it.
- **Load limit breached:** load1 reached 10.5 after `npm ci` and 12.7 during the billing run, partly other seats. After that I waited for it to drop below 8 before each run, but those two moments exceeded the commission's limit.
- A hook refused `git -C $R` as unresolved and I used literal paths. Another refused a chat read with no `view` filter, and I switched to `kam_msgs.sh`. My earlier unfiltered read returned only Wednesday's 16:41 line, in chat_wednesday.json and chat_log.json.
- Also read, read only: the seat's mail and evidence, Wednesday's staged brief and daily note, the Secuura vault note. Nothing in the builder's checkout was fetched or changed.
- Charter read to line 80 of its length, not end to end; the commission named the template, not the charter.
