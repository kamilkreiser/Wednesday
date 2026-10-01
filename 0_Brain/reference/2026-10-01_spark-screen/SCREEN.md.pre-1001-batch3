# KS Backlog + Todo screen for the Spark — 2026-10-01

Written 10:11 AEST 2026-10-01 (2026-10-01T00:11Z, shell `date`) by a Spark brief-writer sub-agent for Wednesday (session cb6b682a). Secuura/Blockchain only. Kam 2026-10-01 09:43: *"Keep working with the spark this week."*

**Read-only on the client systems.**
- Linear was read over GraphQL (Kamil's key, sourced from `4_Credentials/.env` as `LINEAR_API_KEY`, never printed). No mutation, no comment.
- GitHub was read with REST `GET` (open PRs and their `/files`, `GH_TOKEN`) and `ls-remote`.
- Nothing was written under `!CODING/`. Git write verbs ran only in this session's scratchpad clones.
- Nothing was raised, pushed, merged, posted or mailed.

## BLUF

1. **Screened: all 276 KS Backlog + Todo tickets.** Counts come from `fleet/board_count.sh`: `state.type eq backlog` TOTAL=243, `eq unstarted` TOTAL=33, both real counts against a limit of 250.
   - The pull was paginated to `hasNextPage=false`: 6 pages, 276 nodes, matching the counts.
   - Every node came with its description and `comments(first:50)`, sorted client-side. Only KS-485 has more than 50 comments; it is a security-review umbrella and is excluded either way.
2. **Since the 06:03 morning sweep, 2 tickets changed** (`board_count.sh`, `createdAt|updatedAt gt 2026-09-30T20:00Z`, TOTAL=2):
   - KS-1400 (new; a lock refresh, already landed as #1363 at the tip);
   - KS-1379 (excluded by commission).
3. **Prior verdicts re-used for 132 tickets.** These are tickets named in the 09-26, 09-28, 09-29, 09-30 (DELTA, residue) screens or the 10-01 SWEEP, with no change since (point 2). **One was re-opened as a carve: KS-1364.**
4. **Never screened before: 144.**
   - 16 are on Peter or Stuart (excluded).
   - 62 have auth-, token- or security-shaped titles (excluded by commission). I opened 16 of them anyway in case the title filter had over-flagged them; none passed.
   - 10 are decision-titled.
   - **56 were read** (description, plus the last comment).
5. **Spark-briefable: 1 ticket, carved three ways.** That ticket is **KS-1364** (*"85 of 145 request bodies are not marked `required: true`"*).
   - Its fix shape is spelled out: *"mark `requestBody.required: true` where the handler's Zod schema rejects an absent body, at the generator (`*.openapi.ts`)"*.
   - Its 17-operation table lets it be carved into one-file, one-to-two-line spec changes with a KS-747-shape in-process test.
   - The 09-29 screen had it as "multi-file (17 ops)". As a carve, every clause of the predicate holds.
6. **Three briefs, three Spark rounds, three PASSES on round 1.** All three are 7/7 strict + A2a and BYTE-IDENTICAL to the golden. They are held as READYs and together close **5 of KS-1364's 17 operations**. No rebrief was needed. (Details in "Rounds".)
7. **Harness:** 4 items are recorded in `local-model/IMPROVEMENTS.md`:
   - a stale-origin recurrence;
   - nft-certificate's own service lock (tsc rc 2 at the tip without it);
   - a NEW checker blind spot: A3c is set-based, so a mutated duplicate `+` line passed a negative control;
   - hold_ready doubling the ROWID.

   None of them reached the model.

## Method

- **Tip:** develop `723dc0722b68482a03de8577fdb5eb5b3359e725`.
  - Read by `ls-remote` at 09:47 and again at 10:10 AEST, unchanged.
  - It is #1363, KS-1378's lock refresh.
  - The object is local in the Blockchain checkout (`cat-file -t` = commit).
- **Source clone:** `git clone --shared` into this session's scratchpad, detached at the tip.
  - Root node_modules were farmed from the `sparkfeed` checkout by `tasks/code_patch/prepare_clone.sh`.
  - The nft-certificate service's own lock modules were installed with `npm ci --ignore-scripts` in an isolated scratch dir and farmed in. See IMPROVEMENTS.
- **Predicate:** kit `02_FOR_THE_COORDINATOR.md` §2, Spark tier "medium":
  - one or two product files;
  - a fix shape spelled out or derivable from the code;
  - a runnable in-process test nearby;
  - not an auth, token, credential or security surface;
  - not at the round counter;
  - a runner the checker runs.
- **Commission exclusions applied:**
  - `scripts/audit/`;
  - `package.json` and `package-lock.json`;
  - KS-729, 1015, 1378, 1399, 1379, 1380, 1387, 1395, 1397, 1398, 1250;
  - the kintsugi RLS gap;
  - auth, token, credential, MFA, OAuth and security product surfaces;
  - Peter's and Stuart's tickets;
  - #1360/#1361/#1362 files. #1361 is not an open PR. #1360 touches 15 lockfiles and #1362 touches `history.md`; neither touches a file briefed here.
- **Collision:** 23 open PRs (REST `GET /pulls?state=open`, then `/pulls/N/files` for each).
  - None touches any `*.openapi.ts` or `docs/openapi/secuura-api.yaml`.
  - The services briefed here are touched only in `package.json` (#575, #649, #948) or `package-lock.json` (#1360).

## Verdicts — the 56 never-screened tickets read

Each verdict is given with its failing clause. "decision" means the ticket itself says the shape is not chosen, or that a ruling comes first.

| Ticket | Verdict · failing clause |
|---|---|
| **KS-1364** | **SPARK — CARVED ×3, run, PASS.** It was screened 09-29 as multi-file. Carved per operation, it is one file, a spelled-out shape, a KS-747 test shape, and not auth. The 3 carves cover 5 ops. The other 12 ops are listed under "More carves". |
| KS-1400 | NOT: lockfile refresh (package-lock excluded). Already landed as #1363 at the tip. |
| KS-1333 | NOT. The first step is "a measurement, not a fix", and **I measured it at source.** `GET /api/anchors/:id` (anchoring `index.ts:827`) returns `anchor.blockNumber` from `rowToAnchor`, which already does `Number(row.block_number)` (`index.ts:1317`). So the four `anchorStateSync.ts` writers (`:262`, `:299`, `:381`, `:418` at the tip; the ticket's numbers predate #1281) receive a number. Per the ticket, the outcome is "a recorded reason and a cell pinning it, not a coercion". But the pin needs the anchoring app, which boots at import (`app.listen` `:2028`; no test imports `index.ts`), so it cannot be reached in-process. The `||`→`??` question is a ruling. **For Wednesday: the measurement answers the ticket's first done-item.** |
| KS-1332 | NOT: `.githooks/pre-push` fixture guard (Kam's path); a re-land of a multi-cell guard. |
| KS-1331 | NOT: process-group signal forwarding in `run-shell-suites.sh`. No deterministic in-process red; the sibling KS-1325 says SIGINT is unassertable without a PTY. |
| KS-1330 | NOT: re-land of round-2 signal handling. Multi-item, and its arm is gated on a PTY (KS-1325). |
| KS-1325 | NOT: a new PTY harness (feature); "nothing is broken today". |
| KS-1317 | NOT: `packages/shared/package.json` devDependency (package.json excluded). |
| KS-1278 | NOT (closest miss): the revoke read-then-update race. The fix is "a conditional update … **or** a row lock" (a choice), it spans repo + route (two files and more than 3 edits), and atomicity needs a real DB to red. |
| KS-1259 | NOT: an isolation-safety audit across the api-gateway suite (many files, nondeterministic red). |
| KS-1256 | NOT: connector allow-list fail-open (a security surface); "or fall back to a persisted source" (a choice). |
| KS-1251 | NOT: eslint config + tsconfig for the spec-example guard. No failable in-process test, and `scripts/` tooling. |
| KS-1247 | NOT: inventory of out-of-repo consumers (no code). |
| KS-1216 | NOT: "First item: a measurement, not a fix"; supply chain (security). |
| KS-1200 | NOT: "The owner decides which schema source is authoritative" (decision; schema SQL). |
| KS-1186 | NOT: `services/auth` userRepo (auth surface); already HELD per candidates.md. |
| KS-1184 | NOT: "A design call … Two shapes". |
| KS-1177 | NOT: "Owner decision on the intended behaviour, then one of these" (CSRF ordering, a security surface). |
| KS-1154 | NOT: root `package-lock.json` (excluded). |
| KS-1079 | NOT: an ops decision (enable a demo-service flag on a box). |
| KS-1076 | NOT: item 1 is already fixed on develop (09-14 comment); the rest is CI/e2e coverage. |
| KS-1048 | NOT: a `CLAUDE.md` wording change (docs, project rules). |
| KS-1044 | NOT: VM liveness monitoring (infra). |
| KS-1025 | NOT: advisory-gate reshape; the window is "Kam's"; `scripts/audit/` (excluded). |
| KS-1023 | NOT: "Filed rather than fixed, deliberately"; schema SQL in three files. |
| KS-1022 | NOT: "needs a structural guard, not per-route .uuid()"; a class ticket (design). |
| KS-1014 | NOT: "Either close KS-1011's marker … or add a preflight/boot check" (choice; stack tooling). |
| KS-997 | NOT: audit-baseline re-triage (`scripts/audit/`, excluded). |
| KS-996 | NOT: a Linear measurement (no code). |
| KS-995 | NOT: Linear behaviour record (no code). |
| KS-960 | NOT: "DO NOT RECONCILE THESE TWO FILES YET" (ruling). |
| KS-956 | NOT: Dockerfile guard residue; "cannot be written without denying the repo's own idiom" (decision). |
| KS-903 | NOT: a survey ("the deliverable is the classification"). |
| KS-889 | NOT: a measurement/ruling; "re-mint is the only path" (credential surface). |
| KS-884 | NOT: `.githooks/pre-push` (Kam's path). |
| KS-866 | NOT: merge-protocol record; "the fix is already ruled and in force". |
| KS-846 | NOT: `packages/shared/package.json` `main` (package.json excluded; build layout). |
| KS-829 | NOT: audit-gate baseline data model (`scripts/audit/`, excluded). |
| KS-807 | NOT: "Decide first, then implement"; control-byte guard (security). |
| KS-787 | NOT: a cross-platform S/K question; no K code proposed. |
| KS-777 | NOT: tracker; "All four are FIXED on #795" (a board close). |
| KS-768 | NOT: delivered in #796 (03 comment); `scripts/audit/`. |
| KS-761 | NOT: "a decision in its own right" (FP staleness detection). |
| KS-760 | NOT: Linear↔GitHub integration settings (no code). |
| KS-757 | NOT: "all three prescribed fixes are blocked". |
| KS-749 | NOT: advisory/baseline (`scripts/audit/` + frontend lock). |
| KS-735 | NOT: "the contract question — Peter's call" (portal + API; frontend). |
| KS-699 | NOT: schema-wide FK design (52 columns; migration). |
| KS-658 | NOT: "Filed, deliberately not fixed … Kam's call" (demo env config). |
| KS-648 | NOT: frontend CSP quality (security surface; frontend is outside every checker tier). |
| KS-638 | NOT: extranet test board / CI (no K code). |
| KS-636 | NOT: base-image CVE watchdog (security; workflows). |
| KS-624 | NOT: "the fix shape is deliberately blank"; the ruling is Kam's (credential/proof verification = security). |
| KS-607 | NOT: S-side observation; KS-608 (Peter's) carries the invariant. |
| KS-595 | NOT: "are the defects still live?" — a live measurement (Schemathesis catalogue, Python). |
| KS-583 | NOT: DR rehearsal (live, credential rotation). |
| KS-580 | NOT: a feature (append-only recovery audit outside the estate); credential recovery. |

**Opened from the auth-titled 62 because the title filter might have over-flagged them (16): all NOT.**
- KS-562: the lockfile layout of `@lucid-evolution` (a lock).
- KS-1053: a flake in an auth test.
- KS-1085: the launcher `Launch_Claude.command`, which is outside the repo.
- KS-1149: SSH keepalive; already done on the launcher.
- KS-1000: the auth tsconfig (auth service; it also has a PR attached per candidates.md).
- KS-598: "Either re-key the registry … or explicitly remove/disable the upsert", which is a choice; it is tenancy.
- KS-1255: the spec-example secret guard (credential detection).
- KS-1189: the audit log of logins (auth); R-5 is closed.
- KS-1241: "Establish whether `/api/v1/documents` is meant to exist" (decision).
- KS-1240: the key-validate fetch timeout (credential surface).
- KS-977: the Schemathesis `run.py` seeded login (Python, credentials).
- KS-1017: a class ticket across auth tests.
- KS-1038: the e2e lockout race (Playwright, auth).
- KS-1146: a preflight auth leg (push gate).
- KS-902: a comment in the credential guard `no-tracked-credentials.sh`.
- KS-959: "BLOCKED, organization_members has 0 rows".

**Not read, excluded at the filter (the identifiers are in scratch `lin/tri.json`):**
- the other 46 auth-titled tickets;
- the 10 decision-titled tickets (KS-1141, 767, 651, 605, 604, 603, 602, 582, 339, 305);
- the 16 tickets on Peter or Stuart.

## Rounds

| Brief (`local-model/night/briefs/…`) | Change | Rounds | Result | Wall / prompt / completion | READY |
|---|---|---|---|---|---|
| `KS-1364-nft-record-estimate/` | `nft-certificate.openapi.ts` `:879`, `:904`: `body: { content: {…} }, required: true },` (2 one-line replacements) + NEW `ks1364-nft-record-estimate-body-required.test.ts` (+50) | 1 of 2 | **PASS 7/7 strict + A2a**, BYTE-IDENTICAL (cmp rc 0). Red 2/5 → 5/5; suite 38 → 43, 0 new reds; tsc rc 0 | 39.4 s / 24,295 / 1,073 | `night/READY_KS-1364-NFT-RECORD-ESTIMATE-1_spark-dsv4flash_BRIEFED-CODEPATCH-NFT-CERTIFICATE.OPENAPI-PASS-7of7_2026-10-01.diff.md` (ROWID prefix fixed by hand, marked) |
| `KS-1364-nft-verify/` | same file, two pure insertions of `      required: true,` after `:1066`, `:1093` + NEW `ks1364-nft-verify-body-required.test.ts` (+50) | 1 of 2 | **PASS 7/7 strict + A2a**, BYTE-IDENTICAL. Red 2/5 → 5/5; 38 → 43 | 38.1 s / 24,206 / 993 | `night/READY_KS-1364-NFT-VERIFY-1_spark-dsv4flash_BRIEFED-CODEPATCH-NFT-CERTIFICATE.OPENAPI-PASS-7of7_2026-10-01.diff.md` |
| `KS-1364-analytics-reports/` | `analytics.openapi.ts` `:926` (1 one-line replacement) + NEW `ks1364-analytics-reports-body-required.test.ts` (+40) | 1 of 2 | **PASS 7/7 strict + A2a**, BYTE-IDENTICAL. Red 1/4 → 4/4; 28 → 32 | 30.9 s / 20,421 / 795 | `night/READY_KS-1364-ANALYTICS-REPORTS-1_spark-dsv4flash_BRIEFED-CODEPATCH-ANALYTICS.OPENAPI-PASS-7of7_2026-10-01.diff.md` |

- **Run dirs:** `local-model/runs/spark_secuura_2026-10-01_KS-1364-{nft-record-estimate,nft-verify,analytics-reports}`.
- **Ladder:** rows 50-52 in `SPARK_LADDER.md`. Backups `.pre-1001-*` were taken before each edit.
- **Spark:** `http://127.0.0.1:47788`, health 200 before each round, thinking OFF, one request at a time. There was no queueing and no retry.

**Smoke and controls.** The kit's smoke rule was met per brief, not merely cited.
- Yesterday's KS-1015 envelope round proved this exact harness class: code_patch, vitest, a spec-registry test, golden CONTROL PASS, a mutated-header A2a BAD. The harness files are unchanged since 09-28 18:23 (`checker.sh` mtime).
- Each brief was still run through `build_input.sh` (rc 0, "prompt source: WEDNESDAY BRIEF").
- Each golden was then run through `spark_checker.sh` as a CONTROL: PASS 7/7 + A2a.
- Each had a NEGATIVE control, the golden with a product `+` line mutated:
  - FAIL A3c on nft-record-estimate and on analytics;
  - **PASSED on nft-verify**, where the mutated line (`required: !0`) was one of two byte-identical `+` lines, so A3c found the other one, and `!0` is still true. This is a checker blind spot, recorded in IMPROVEMENTS.
  - A second nft-verify negative (`required: false`) FAILED A5/A6.

**Raise needs (all three):**
- The regenerated `docs/openapi/secuura-api.yaml`. Each brief folder has `KS-1364.openapi-yaml.companion.diff` (2, 2 and 1 added lines). With the model's files alone, `generate-openapi --check` gives rc 1; with the companion, `check:openapi` gives rc 0. Measured.
- The three goldens and three companions apply strictly in sequence on one tree. Measured.

## More carves of KS-1364 (not briefed today; same shape, each needs its handler read)

The 12 remaining operations:
- `POST /api/billing/checkout/custom` (not baselined);
- `POST /api/billing/customers/{customerId}/default-payment-method`;
- `POST /api/issuer-certs`;
- `POST /api/m365/{documents/sync, outlook/verify-hash, sites}`. Their handlers destructure `req.body`, and verify-hash is public. Needs reading.
- `POST /api/onedrive/files/{id}/sync`;
- `POST /api/referrals/generate`. Same file as the KS-1015 READY, so sequence it after that READY.
- `PATCH /api/platform/tenants/{id}` and `PATCH /api/users/admin/{id}` (admin surfaces);
- `POST /api/users/me/change-password` (auth, excluded);
- `POST /api/v2/verification/verify`.

Billing and m365 look like the next two Spark briefs. `/generate` should be sequenced after KS-1015's READY.

## For Wednesday

- **Read the three diffs.** Each is 1-2 product lines plus a 40-50 line test.
- **KS-1364 is Peter-created, Kamil-assigned.** The three READYs ref it and do not close it. It names 15 pairs as baselined against the closed KS-255, and that baseline is in `systemTest/schemathesis` (Peter's estate). Whether to un-baseline those pairs when these land is not ours.
- **KS-1333's first done-item is answerable from source** (above). Wednesday may want it carded or commented. Nothing was posted.

## UNMEASURED

1. No Schemathesis or live run. That the 5 no-body cases stop firing is a prediction from the rendered spec.
2. The 56 "read" tickets were read from the description (up to ~1,300 characters) plus the LAST comment. Long descriptions were not read to the end. A verdict that rests on an early "decision" or "not chosen" line could miss a later carve.
3. The 62-ticket auth-title filter is a regex over titles, and it over-flags (it matches "token", "tenant", "security", "session"). 16 were opened and confirmed; 46 were not.
4. The node_modules are farmed from `sparkfeed` (installed at `94c9c7aa`), not a fresh `npm ci` at the tip. nft-certificate's service modules ARE a fresh `npm ci` of the tip's service lock.
5. Open PRs were read at ~09:55 AEST. A PR opened after that is not covered.
6. The 132 re-used verdicts were not re-read. Their tickets show no create/update since 2026-09-30T20:00Z other than KS-1379 (excluded), per the board_count delta.

---

## Batch 2 — KS-1364 carves continued (appended 10:29 AEST 2026-10-01; nothing above was rewritten)

This batch was commissioned by Wednesday after she read the three batch-1 PASS diffs line by line and accepted them. All KS-1364 READYs go up as ONE PR later. Nothing was raised. The tip is unchanged: develop `723dc0722b68` by `ls-remote`. The open PRs were re-read at 10:21: 23 PRs, none new, none touching these files.

### Checker fix landed first: A3c is now a MULTISET

- **The change:** `tasks/code_patch/a3c_plus.py`.
  - The backup is `.pre-1001-multiset`; the file was written as a copy and then moved into place.
  - Each expected `+` line now consumes one `+` line, so two identical expected lines need two copies.
- **Red arm:** `local-model/tests/a3c_multiset_arm_2026-10-01.sh`. The subject is the nft-verify section, which has two identical lines.

| Arm | Exit | Want |
|---|---|---|
| Golden | 0 | 0 |
| One copy mutated to `required: !0,` | **1** | 1 (the old set-based file gave 0 on the same section) |
| One copy dropped | 1 | 1 |
| Today's three held runs | 0 each | 0 |

- **End to end:**
  - The full `spark_checker.sh` was re-run on the three batch-1 outputs in fresh clones: PASS 7/7 + A2a each.
  - The 10:0x nft-verify negative now gives rc 1, FAIL A3c.
  - The fix fired live again in the billing precheck below: two identical `+` lines, one mutated, FAIL A3c.

### Operations chosen, grouped per file

| Brief (`night/briefs/…`) | File · edit points | Ops |
|---|---|---|
| `KS-1364-billing/` | `billing.openapi.ts`: 2 pure insertions of `required: true,` after `:740`, `:880` | `POST /api/billing/checkout/custom`, `POST /api/billing/customers/{customerId}/default-payment-method` |
| `KS-1364-m365/` | `m365-integration.openapi.ts`: 3 one-line replacements `:601`, `:706`, `:1019` | `POST /api/m365/sites`, `/documents/sync`, `/outlook/verify-hash` (stays public, KS-442) |
| `KS-1364-onedrive/` | same file: 1 pure insertion after `:833` | `POST /api/onedrive/files/{id}/sync` |

**Not briefed, each with its failing clause:**
- `POST /api/referrals/generate`: `referral.openapi.ts` belongs to the KS-1015 lane.
- `POST /api/issuer-certs`: it lives in `auth.openapi.ts` (auth service).
- `PATCH /api/users/admin/{id}` and `POST /api/users/me/change-password`: auth surfaces.
- `PATCH /api/platform/tenants/{id}` (tenant-provisioning `index.ts:440`):
  - `updateTenantSchema` is a partial-update schema that ACCEPTS `{}`;
  - the 400 comes from a "No fields to update" check (`:455`), not from the zod schema, so the ticket's clause "where the handler's Zod schema rejects an absent body" does not hold;
  - it is also a platform-admin surface.
- `POST /api/v2/verification/verify` (originate):
  - the handler resolves one of four optional fields (`hash|contentHash|documentId|documentData`, `verificationV2.ts:17`), not a zod object, so the shape is not derivable without a ruling;
  - originate is jest, and there is no originate spec-registry test to copy.

These two are Wednesday's call if she wants them. **I stopped at 3 briefs, under the cap of 4, because the predicate ran out.**

### Rounds (counter: original + one rebrief; none was needed)

| Brief | Rounds | Result | Wall / prompt / completion | READY (`local-model/night/`) |
|---|---|---|---|---|
| `KS-1364-billing` | 1 of 2 | **PASS 7/7 strict + A2a**, BYTE-IDENTICAL (cmp rc 0). Red 2/5 → 5/5; billing 93 → 98; tsc rc 0 | 34.2 s / 20,311 / 984 | `READY_KS-1364-BILLING-1_spark-dsv4flash_BRIEFED-CODEPATCH-BILLING.OPENAPI-PASS-7of7_2026-10-01.diff.md` |
| `KS-1364-m365` | 1 of 2 | **PASS 7/7 strict + A2a**, BYTE-IDENTICAL. Red 3/6 → 6/6; m365 47 → 53 | 40.3 s / 21,390 / 1,258 | `READY_KS-1364-M365-1_spark-dsv4flash_BRIEFED-CODEPATCH-M365-INTEGRATION.OPENAPI-PASS-7of7_2026-10-01.diff.md` |
| `KS-1364-onedrive` | 1 of 2 | **PASS 7/7 strict + A2a**, BYTE-IDENTICAL. Red 1/4 → 4/4; m365 47 → 51 | 30.6 s / 20,155 / 775 | `READY_KS-1364-ONEDRIVE-1_spark-dsv4flash_BRIEFED-CODEPATCH-M365-INTEGRATION.OPENAPI-PASS-7of7_2026-10-01.diff.md` |

**Before each round:**
- the builder ran on the brief: rc 0, "WEDNESDAY BRIEF";
- the golden CONTROL ran: PASS 7/7 + A2a;
- the negative ran: FAIL A3c;
- each edit point was reverted on its own, and each turned exactly its own RED cell red.

The Spark answered 200 before every round, with no queueing. Ladder rows 53-55 are written, and there is an IMPROVEMENTS row (the checker fix, plus billing's `@types/pg` farm conflict).

**Smoke:** the harness is today's batch-1 harness with ONE change, A3c. That change was proven by the arm and re-checks above, so the batch-1 smoke is cited for everything else.

**Raise:**
- All six product goldens and all six YAML companions apply strictly in sequence on one tree. Measured.
- The KS-1015 envelope companion still applies on top (`--check`).
- Not run: that the stacked YAML equals a fresh `generate-openapi` of the stacked tree. The raise seat runs `npm run check:openapi`.

### KS-1364 coverage after batch 2: **11 of 17 operations**

| Batch | Ops covered |
|---|---|
| Batch 1 | 5 (nft ×4, analytics ×1) |
| Batch 2 | 6 (billing ×2, m365 ×3, onedrive ×1) |
| **Total** | **11 of 17** |

The 6 left are referrals/generate, issuer-certs, users/admin, users/me/change-password, platform/tenants and v2 verify, each with the reason given above. **Refs KS-1364, does NOT close it.**
