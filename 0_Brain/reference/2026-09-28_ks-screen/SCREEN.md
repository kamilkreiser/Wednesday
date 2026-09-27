# KS board screen for the local models, 2026-09-28 (develop `ec32c40e2b1e2698d2e855a916f390d48dad1b45`)

Written 06:31 AEST 2026-09-28 by a screening and brief-writing drafter for Wednesday. It was read-only on the Secuura repo and board: nothing was posted, moved, commented, raised, mailed or committed, and no local model was run.

- **Base clone check:** the base clone `ks1346cd/base` read HEAD == `ec32c40e` before use, and its porcelain was 0 before and after every builder run.
- **Where the work ran:** every write verb and every test run happened in this drafter's own `--shared` clone, in its scratchpad.

## BLUF
- **Briefed: 3, all Spark.** Each is a one-file product change with a new in-process vitest file. Each golden was proven RED before the fix and GREEN after, and the file's whole suite showed no new red.
  - **KS-747:** `security.openapi.ts`, 1 insertion. The raise also needs a generated YAML companion hunk, which is measured and included.
  - **KS-908:** `security/src/index.ts`, 2 insertions. ⚠ The round counter is Wednesday's call.
  - **KS-692:** `vc-issuer/src/routes/status.ts`, 2 hunks, Kam-ruled. ⚠ It builds only with `ALLOW_BLANK_CONTEXT=1`.
- **Ornith: 0 briefed.** KS-1343 (docs) is the one Ornith-sized item; it is not briefed, because the commission requires a golden proven red/green and a doc patch has no test.
- **Cards for Kam: 4.** KS-1351 item 1, KS-1335, KS-1227 and KS-1054 are each shaped as "decide which".
- **Everything else read is cloud or skip.** The recent board is residue from capped rounds, live-seat files, multi-file/migration work, and merged tickets waiting on live sweeps.

## The frame
- **Listed:**
  - **488 open KS issues** (state type backlog/unstarted/started: Backlog 235, In Progress 212, Todo 24, In Review 12, Blocked 5). There were 5 GraphQL pages of 100, paginated until `hasNextPage=false`.
  - A second query for the named ids (KS-747, 908, 692, 1351, 1346) returned all 5.
  - A third query for `number >= 1336` in any state returned 16. The 4 Done ones among them (KS-1339, 1344, 1349, 1350) are listed below as skip.
- **Positive control:** KS-1346 (a known In Progress ticket) appears in the open set, with its 4 PR attachments (#1311, #1312, #1297, #1296). All 5 named tickets were returned.
- **Read in full: 39.** For each, the description plus `comments(first:50)`, sorted client-side. No ticket had more than 50 comments (`hasNextPage` was false for all 39). The 39 are:
  - the **36** open tickets created or updated since 2026-09-26T00:00Z;
  - the **3** named pool tickets not updated since then (KS-747, 908, 692; KS-1351 is inside the 36).
- **Not read in this screen: 449.**
  - The 2026-09-26 screen read 284 of the then-open board, and `candidates.md` was derived at 2026-09-27 22:14 from 261 Backlog/Todo tickets. Neither changed since for any ticket not updated since 09-26.
  - Title/description scan counts over all 488 (text scan, over-counts): 23 assigned to Peter or Stuart; 94 auth/MFA/token/credential/session-shaped titles; 108 carrying a decide/decision/question/owner's-call marker in the title or the first 1500 characters.
- **Open PRs: 22 measured, as a PROXY.** This drafter holds no GitHub identity, so a PR counts as open if EITHER:
  - its latest Linear attachment metadata says open/draft/inReview (Distributed_Secuura only; platform-s PRs excluded), OR
  - `ls-remote` shows a live `refs/pull/N/merge`.

  The 22 are #191 572 575 635 639 649 809 887 920 923 927 945 946 947 948 949 989 995 1129 1250 1253 1310. Their heads were fetched and their files were diffed against the merge-base with develop.
  - **Product source they touch:** #191 (draft; packages/shared tenant-context, api-gateway auth, auth db/userRepo, originate db/index), #995 (anchoring index, api-gateway trustHeaders, originate index + gatewayProvenance), #1310 (originate logger), #923 (an api-gateway test).
  - **Package manifests only:** #575, #635, #649, #948, #949 touch `package.json` files only.
  - **None of the three briefed product files is touched.**
- **Live-seat exclusions, as given:** `services/**/routes/adminConfig.ts`, `services/**/routes/webhooks.ts`, any MEMORY.md.

## Every ticket read, one line each
`id · tier · the clause that decides it · where read`

- **KS-747 · SPARK (BRIEFED)** · one product file, and the fix shape is spelled verbatim ("declare the query parameter ... required, uuid") · `security/src/security.openapi.ts:801-824` (no `request:`), `security/src/index.ts:1174-1178` (the handler 400s without it)
- **KS-908 · SPARK (BRIEFED; counter → Wednesday)** · one file, two insertions in the precedent shape at `:1351`. The counter shows 3 Ornith runs on 09-15 (`night/done.md:32,42,56`) · `security/src/index.ts:1146-1161`, `:1208-1217`, `:1351`
- **KS-692 · SPARK (BRIEFED; ALLOW_BLANK_CONTEXT)** · Kam ruled option a on 2026-09-16 15:04 ("Narrow now, bind-creator later"); one file, two hunks · `vc-issuer/src/routes/status.ts:34-40`, `:42-53`; `decisions.json` card `secuura-ks692-status-revoke-interim-posture`
- KS-1351 · card-for-Kam (item 1) + cloud (item 2) · item 1: "That is the decision this ticket asks for" (whether `VCCredentialStatus` declares the revocation fields; the type is at `packages/shared/src/vc/types.ts:27-33`). Item 2 is `let`→`const` at `vc-issuer/src/repositories/credentialRepo.ts:95`, a lint warning with no runnable red · types.ts:27, credentialRepo.ts:95
- KS-1348 · skip · open PR #1310 (originate `utils/logger.ts` + its test) · PR head diff
- KS-1347 · cloud · remaining site `scripts/openapi-examples/proxy/server.ts:31`. Its runner is `npx tsx --test` (node:test, `redact.test.ts:11`), which the checker does not run (vitest/jest only, `build_input.sh:264-269`). The module also exits at import without `HARVEST_EXAMPLES` (`server.ts:37-40`). The other site, `systemTest/playwright/global-setup.ts:42`, needs a live stack · server.ts:31
- KS-1346 · skip · live seat: `routes/adminConfig.ts` / `routes/webhooks.ts` (parts C and D are already briefed) · ticket + comments
- KS-1345 · skip · the fix is in `routes/webhooks.ts:196` / `:412` (live seat) · description
- KS-1343 · Ornith-docs candidate, NOT briefed · 2 doc files and 8 notes; two of them read "tightened or explicitly accepted as-is" (judgement), and there is no test to prove a golden red/green · description (`MULTI-TENANCY.md`, `RLS-FAIL-CLOSED-PLAN.md` cites)
- KS-1341 · skip · `routes/webhooks.ts` (live seat) · ticket
- KS-1340 · cloud · "Fix shape (not chosen here)"; the ks597 integration cell needs Postgres · description
- KS-1338 · cloud · an AST-reader change in the entrypoint-corpus guard, the "same defect class as the round's first attempt, which is why the round capped" · description
- KS-1337 · cloud · the akto site merged in #1295; the remaining `systemTest/playwright/global-setup.ts:42` needs a live stack · last comment 09-26 15:31
- KS-1336 · cloud · per-tenant-DB umbrella (5 tickets); #1286 merged · comments
- KS-1335 · card-for-Kam · "by whichever shape is chosen". Shape 1 changes the published `lastSentAt` meaning; shape 2 is DDL in 2 files plus a backfill · description (`m365-integration/src/index.ts`, `ks934...R3`)
- KS-1334 · skip · `routes/adminConfig.ts` (live seat) · ticket
- KS-1326 · cloud · residue of a round capped at NO GO (#1245 closed), perf lane, 4 residues · description + comments
- KS-1319 · cloud · the residue box asks to "name the spellings it deliberately does not cover" (judgement) in a packages/shared guard · last comment 09-26 02:41
- KS-1316 · cloud · #1268 closed at the two-NO-GO cap; a guard-reachability class · comments
- KS-1314 · cloud · #1278 NO GO at the cap; a new AST shape (B-1278-2) · comments
- KS-1313 · cloud · #1245 round 3 NO GO at the cap (ERRORS-LINE-LIVE regression) · comments
- KS-1306 · cloud · residue plus an un-run INSERT leg (needs a DB); its QUERY-OVERRIDE half is filed as KS-1340 · last comment
- KS-1304 · cloud · the `withTenant` pool choice is a tenant/RLS surface across `packages/shared` and originate `db.ts:308`; live proof NOT RUN · description
- KS-1293 · skip · residue already filed as KS-1339 (Done) · last comment
- KS-1235 · cloud (auth, excluded) · auth-service tenant GUC: "The owner's fix. Not built here."; the caller census is not done · description
- KS-1227 · card-for-Kam · "The keep-vs-filter decision this ticket raises is still open" · last comment 09-27 13:21
- KS-1205 · cloud · api-gateway per-key limiter, with 7 open items (N-2, F-4, F-5, R-2, N-1, fallback literal, Redis-key cell); JWT-claim surface · last comment 09-27 13:21
- KS-1179 · cloud · RUNTIME change on `ssrf-guard.ts`; live sweep owed · last comment
- KS-1142 · skip · re-raised and merged as #1287 on 09-26; nothing model-sized is left · comments + PR metadata
- KS-1129 · cloud · RUNTIME change; live sweep owed (§5f) · last comment
- KS-1124 · cloud · two findings across `certifications.ts` / `documents.ts`, with a measured mint/write race · description + comment 09-26
- KS-1090 · cloud · R2-2 (the tsconfig half) and R2-4 (the record) are open; a cross-service tsconfig decision · last comment 09-27 13:21
- KS-1074 · cloud · measured residual race ("a token minted between the read and the write is still erased") · last comment
- KS-1055 · cloud · multi-file (`startup-migrations.ts` + `tenant-provisioning`) migration arm · description
- KS-1054 · card-for-Kam · "Fix shapes (not a ruling)"; F-928-2 "is a design decision with deploy consequences and is Kam's" · description
- KS-934 · skip · #1274 merged; its residue is KS-1335 · last comment
- KS-794 · skip · #1276 merged; only the live sweep is owed (not model work) · last comment
- KS-766 · skip · #1285 merged (Spark-produced); nothing briefable is left · last comment + PR metadata
- KS-730 · cloud · the api-gateway share was measured UNTESTED (a class); the adminConfig share is the live seat · last comment 09-26 02:48
- KS-1339 / KS-1344 / KS-1349 / KS-1350 · skip · Done (`number >= 1336` query) · state

**Counts over the 39 read (each ticket once):** Spark 3 (briefed) · Ornith 1 (KS-1343, docs, not briefed) · cloud 21 · card-for-Kam 4 (KS-1351, 1335, 1227, 1054; KS-1351 item 2 is a cloud or human one-liner inside that card) · skip 10. Sum 39. The 4 Done tickets from the `>=1336` query are skip and not in the 39.

## For Kam (cards, not tasks)
- **KS-1351 item 1:** does `VCCredentialStatus` gain `revoked`/`revocationReason`/`revokedAt`, or does the repository stop writing fields the contract lacks? It is shared-package scope.
- **KS-1335:** for Teams-notify rotation, choose between "last attempted" changing the published `lastSentAt`, and a new `last_attempted_at` column (DDL in 2 places).
- **KS-1227:** the ks1072 anchor-store witness: keep counting every stub request, or filter by document path?
- **KS-1054:** make boot-1 migration failure visible, and choose the stage ordering. The ticket names this Kam's design decision.

## For Wednesday (process)
- **KS-908's counter.** Strictly counted, `done.md` shows 3 runs, two of them FAILs. The rule says two rounds then cloud. The brief and golden are written either way; the README says so.
- **KS-692's blank-context override.** The builder refuses without `ALLOW_BLANK_CONTEXT=1`. The blank line is unavoidable: the last changed line `:40` is followed only by the empty `:41`, and zero trailing context fails strict `git apply` (measured).
- **KS-747's raise needs the YAML companion.** It is in the brief directory. Without it `check:openapi` FAILS (measured).

## UNMEASURED
1. **Open PRs came from a proxy** (Linear attachment metadata plus live `refs/pull/*/merge`), not the GitHub API. A PR linked to no Linear issue AND without a merge ref (for example one with conflicts) would be missed.
2. **The 449 tickets not read** rest on the 09-26 screen and on `candidates.md` (09-27 22:14). They were not re-read, and none was updated since 09-26.
3. **The auth/decision counts over 488** are text-scan over-counts; they were not confirmed per ticket.
4. **No Spark round, no `spark_checker.sh` and no live stack** were run for any brief. `build_input.sh` was run for all three (rc 0; KS-692 only under the override).
5. **Round counts** were matched by ticket id at line start in `night/done.md` plus `READY_*<id>*` filenames.
6. **KS-1343's docs-only path** (doc_patch) was not tried. It fails the "golden red/green" requirement of this commission, not necessarily the kit.

Artefacts: in this drafter's scratchpad (`board.json`, `full.json`, `att.json`, `prfiles.txt`, `verify/` logs per ticket), not copied here.
