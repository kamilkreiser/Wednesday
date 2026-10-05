# KS audit, auditor C (the newer half of Backlog+Todo), 2026-10-05

**Partition.** I took the snapshot `ks_all_2026-10-05T0205Z.json` and kept the tickets that are not archived and are in Backlog or Todo: **276**. Sorted by createdAt ascending, B has 1-138, up to and including **KS-1012** (2026-09-08T12:28:43Z). **C has 139-276: KS-1014 (2026-09-08T13:17:01Z) to KS-1406 (2026-10-04T14:32:52Z), 138 tickets.** That is 128 Backlog and 10 Todo. `audit_C.tsv` has 138 rows plus a header, which matches the expected 138.

## BLUF

| CLASS | n |
|---|---|
| TEST-OR-TOOLING | 58 |
| GENUINE-DEFECT | 33 |
| GENUINE-HARDENING | 23 |
| NEEDS-HUMAN | 10 |
| NOT-GENUINE | 8 |
| ALREADY-FIXED | 3 |
| DUPLICATE | 2 |
| UNVERIFIED | 1 |
| MERGED-AWAITING-SWEEP | 0 |

- **ARCHIVE:** yes 3, ASK 28, no 107.
  - **yes:** KS-1149 (ALREADY-FIXED), KS-1241 (DUPLICATE of KS-1234), KS-1329 (DUPLICATE of the KS-892→933→1000 chain).
  - **ASK:** every ticket Peter or Stuart created or holds, including two that are fixed: KS-1387 (6cf5c3629) and KS-1400 (#1363, merged 09-30T23:11Z).
  - **Cancel candidates, not archive-yes, because they are NOT-GENUINE:** KS-1307, 1308, 1309, 1323 and 1048.
- **No row in this half has children**, so archiving cascades to nothing.
- **31 Oct critical path:** yes 24 · unknown 13 · no 101.

**Is it genuine? Mostly yes, but it is not the backlog that blocks 31 Oct.**
- 56 of 138 (41%) are real product problems (33 defects and 23 hardening).
- 58 (42%) are test, CI, harness or docs work. This class is the single largest.
- Only 13 (9%) are not genuine, duplicates or already fixed.

The agents are not inventing defects. They are filing a lot of *their own tooling* onto the client's product board.

## Filing source and rate

The board account `kamil.kreiser@secuura.ai` is shared by Kam and the agents. I separated agent filings from Kam's by reading each body.

| Filed by | n | What it is |
|---|---|---|
| Agent, a gate/QA/audit finding | 74 | 24 defects, 16 hardening, 26 test/tooling, 2 not genuine |
| Agent, other (process notes, capped-round residue, seat environment) | 36 | 16 test/tooling, **6 of the 8 NOT-GENUINE**, 4 defects |
| Client human (Peter 22, Stuart 6) | 28 | 16 test/tooling (slot, CI and docs, all accurate), 5 defects |
| Kam's own voice | 0 | Kam *ruled* on several, for example KS-1025, 1114, 1116 and 1157, but agents wrote them |

**Rate of the surviving open Backlog/Todo in this half, per week (Mon):**

| Week | Total | Agents | Peter | Stuart |
|---|---|---|---|---|
| 09-07 (from 09-08) | 42 | 41 | 1 | 0 |
| 09-14 | 41 | 36 | 3 | 2 |
| 09-21 | 25 | 25 | 0 | 0 |
| 09-28 (to 10-04) | 30 | 8 | 18 | 4 |

**Board-wide filings by the shared account, all states:** 172 → 117 → 64 → 16 per week over the same four weeks.

So agent filing peaked in the week of 09-07/09-14 and has fallen about 10× since. This week, Peter files more than the agents do.

## Top 10 genuine defects by risk to 31 Oct

All are cited at develop `3ce8cd4026a6`. Rows marked ✔ I re-read myself after the fork read them.

1. **KS-1210** ✔ (sev 5): any authenticated user can POST `/apps`, or PATCH any app by id with any scopes (`*`, `subjects:erase`). There is no role check and no owner check: `services/auth/src/routes/oauth.ts:1148`, `:1245` use `authenticate()` only, and `services/oauth.ts:184` `updateApp(id, …)` updates by id. *Whether `seedTenantGuc` RLS at least bounds this to the tenant is not measured.*
2. **KS-1401** (sev 5): `charge_events` on the kintsugi DB has RLS off with 8 rows. Migration 039 is recorded, so it will not re-run, and no migration from 040 to 048 names the table (`startup-migrations.ts:332` only CREATEs it). *The live DB state is the ticket's own reading.*
3. **KS-1376** ✔ (sev 4): `migrations/038a_ks1054_core_tables_before_039.sql:72-89` creates `certifications` with no `tenant_id`, so 039 skips its tenant_isolation policy. A fresh DB, slot or tenant DB is left with FORCE RLS and no policy. The file's own header at `:16-17` claims it fixed this.
4. **KS-1107** ✔ (sev 4): public register accepts any `organizationId` (`services/auth/src/routes/auth.ts:139`) and stores it unchecked (`:233`). The impact on org-scoped reads has not been traced.
5. **KS-1256** ✔ (sev 4): the connector allow-list fails open. In `api-gateway/src/routes/verification.ts:1220-1238`, a missing setting becomes `(sRaw||{})` → `integrations []`, which leaves no restriction, and `catch {}` swallows read errors.
6. **KS-1116** ✔ (sev 4): `vc-issuer/src/routes/presentations.ts:366-377` returns any presentation to any bearer; the file has 0 `req.user` reads. Kam ruled `bind-creator`, but it is not built.
7. **KS-1384** (sev 4): a repeat anchor POST upserts and resets `status`/`transaction_hash`, nulling a confirmed hash (`anchoring/src/index.ts:1359-1361`).
8. **KS-1383** (sev 4): credential verify checks no proof because no DID resolver is wired (`vc-issuer/src/routes/credentials.ts:339-347`).
9. **KS-1174 + KS-1240** (sev 3, overlapping but distinct): the gateway answers 401 "Invalid API key" for a security-service outage, and its key-validate and connector-token fetches have no timeout (`api-gateway/src/middleware/auth.ts:193`, `:223`, `:227-236`). This blocks the S↔K re-key work.
10. **KS-1102** (sev 3): unauthenticated status and health routes publish internal URLs, ports and unset-key state on internet-reachable hosts (`api-gateway/src/index.ts:772-779`).

**Also sev 3:** KS-1168 (admin search ILIKEs ciphertext, `userRepo.ts:1021`, `:1065`) · KS-1184 (workflow stranded as approved, `verification.ts:991-993`) · KS-1327 (the KYC mock overwrites an admin reject, `kyc/src/index.ts:1035`) · KS-1163 (Peter; the start script does not wait for 5 services, and Kam ruled 09-22) · KS-1345, KS-1385, KS-1235 (latent).

**Not product, but critical for "ready":**
- KS-1076: no Playwright runs on CI, and the develop run fails at `test:unit`.
- KS-1051: no gate runs the service unit suites.
- KS-1289: `.dockerignore` ships `__tests__`, so a test-only change rebuilds 23 of 29 images.

## NOT-GENUINE patterns

- **Agent evidence-hygiene or process notes filed as product tickets:** KS-1307 and 1308 (wording in the body of merged PR #1242), KS-1100 (missing QA-gate records on PRs a human had already approved), KS-1048 (CLAUDE.md wording).
- **Fleet or host housekeeping that is not in the Secuura repo:** KS-1323 (push2x.sh, 0 tracked files) and KS-1309 (a Docker volume left on one agent host).
- **Code that exists only on an unmerged PR:** KS-1338 (#1268, closed unmerged). KS-1324 and KS-1325 reason about open PR #1250's code; they are kept as TEST-OR-TOOLING.
- **A premise that measures false:** KS-1333 (blockNumber is already a Number, `anchoring/src/index.ts:1317`, `:1439`, `:1451`).
- **Biggest volume problem, which is genuine but misplaced:** 42 agent-filed TEST-OR-TOOLING tickets on the client board. These are about gate scripts, harness flakes and seat environments, not product behaviour.

## NEEDS-HUMAN (who / what)

- **Kam:** KS-1025 (warn-window length) · KS-1083 (gateway vouch secret, deploy order) · KS-1091 (commission the cross-tenant JWT probe) · KS-1112 (DSR 200 vs 404).
- **Kam or Stuart:** KS-1079 (demo-service on kintsugi/demo) · KS-1247 (does anything outside the repo parse the health bodies).
- **Kam or Peter:** KS-1200 (which of 10 anchor_store schema sources is authoritative) · KS-1322 (KS keys in the published OpenAPI).
- **Kamil or Kam (ASK):** KS-1358 (405-before-auth vs the KS-406 ruling) · KS-1398 (TS 7; suggest deferring past 31 Oct).
- **UNVERIFIED:** KS-1178 (Stuart). A paired-slot erase-then-read settles it.

## Could not verify

- **Live, VM or DB state.** Nothing was re-measured, so these rest on the ticket's own reading:
  - kintsugi RLS (KS-1401, KS-1376 FORCE sequence);
  - exposure on deployed hosts (KS-1102, 1214, 1216, 1235);
  - KS-1014, 1044, 1079, 1080, 1262.
- **Exploit or impact traces not run:** KS-1107 org impact, KS-1210 tenant bound, KS-1383 id-swap, KS-1384 second fee transaction, KS-1280 revoked JWT at originate.
- **Flakes and gate counts not re-run:** KS-1259, 1328, 1290, KS-1022's "~15 routes", and the TEST-OR-TOOLING rows that rest on gate measurements quoted in the tickets (the cited files and lines were confirmed to exist).
- **KS-1149** is proved by the launcher outside the repo (`Launch_Claude.command:130`, `:135`).
- **Watch:** open PR #1360 would revert #1358 (seen during the KS-1387 check).

## Method and controls

- **Pulled:**
  - Linear GraphQL reads per ticket: description, `comments(first:50)` sorted client-side, attachments, relations and children.
  - The whole-board corpus of 1,396 issues including archived, for duplicate grep by symbol, path and error string.
  - GitHub GET on 43 referenced PRs for `merged_at`.
- **Code:** read at develop `3ce8cd4026a6`, in a `--shared` clone in scratch fetched with the checkout's sshCommand (ls-remote confirmed it was the tip at audit time). The client checkout was untouched. Nothing was written to Linear, GitHub or `!CODING`.
- **Classification:** four forks of this auditor took about 35 tickets each and read every body whole. I merged their rows and checked them: 138 ids, set-equal to the partition, 8 fields each, and the Peter/Stuart→ASK guard had 0 violations.
- **Controls:** I re-read 5 of the top-10 cites myself (✔ above). Every DUPLICATE and ALREADY-FIXED row names a survivor id, a PR with merged_at, or an ancestor commit. Zero-hit greps carry a positive control in their row (for example, KS-1323: `run-shell-suites.sh` 1 hit).
- **No-duplicate zero, a representation:** across chunk 1 no duplicate was found. Overlaps were judged distinct (KS-1053/1155, KS-1119/590, KS-1174/1240).
