# KS screen for the Spark: 2026-10-07, 11:20 batch (4 briefs delivered)

Written 2026-10-07 11:47 AEDT (shell `date`; the briefs are stamped 11:32:13) by a Spark brief-writer sub-agent for Wednesday. Secuura only. Authority: Kam's standing rules ("Spark on all tickets", 50 Spark tasks a day, the brief is the cost), the kit predicate (`spark-kit_2026-09-23/02_FOR_THE_COORDINATOR.md` §2), and the round counter (original + ONE rebrief).

**Read-only on client systems:**
- Linear: GraphQL reads only. `LINEAR_API_KEY` was sourced from the Blockchain `4_Credentials/.env` and never printed.
- GitHub: REST GET only (open PRs and their files).
- Git under `!CODING/`: read verbs only (`ls-remote`, `config --get`, `status`). After the work, the Blockchain checkout shows 0 tracked-modified lines.
- Every git write verb ran in `git clone --shared` copies under this session's scratchpad.
- `round.sh --dry-run` and `--control` fetched the tip into the Spark cache clone. That is round.sh's own step 4.

**Not touched:**
- `spark/queue.md`, `night/queue.md`, `PAUSE_QUEUE`.
- No model round was run.
- No PR, comment or ticket change.

## BLUF

1. **Tip:** develop `69f2045af2a4f5f0b83b2f76c62514512abdc7b5`. Read by `ls-remote` at 11:18, and again at 11:46, unchanged.
   - The Spark cache clone was at `d75bfe2deb80` before this screen.
   - 12 commits sit between the two. They are #1400–#1405 (KS-571 systemTest batch), KS-1437 (lock refresh) and KS-1436 (job 06 stderr to its own file, the 10-07 00:2x brief, now merged).
2. **Counts:**
   - **Delta: 26.** Instrument: `fleet/board_count.sh linear`, filter `team KS, state.type in [backlog, unstarted], updatedAt gt 2026-10-06T01:00:00Z` → `TOTAL=26` (a real count against the 250 limit). The paginated pull returned 26 nodes. **Positive control:** the filter returns KS-1435, which was created 2026-10-06 12:41Z, inside the window.
   - **Whole Backlog+Todo board: 275** (245 backlog + 30 unstarted). `board_count.sh` correctly refused to total it ("MORE PAGES EXIST"), so this number comes from a paginated GraphQL count with page size 250.
   - **KS, all states, updated since 2026-10-06T01:00Z: 49.**
3. **Delivered: 4 briefs.** All four have `round.sh --dry-run` rc 0 ("DRY-RUN OK", prompt source WEDNESDAY BRIEF) and `round.sh --control` **CONTROL-PASS 7/7 + A2a, golden BYTE-IDENTICAL**:

   | Brief dir (`2_Project_Files/local-model/night/briefs/`) | Ticket | Product | Edits | Dry-run | Control |
   |---|---|---|---|---|---|
   | `KS-1435-transfer-reject-signature-typed` | KS-1435 | `services/transfer/src/index.ts` | 1 insertion, plus 3 cells in the existing `transfer.test.ts` | rc 0 | PASS 7/7. A4: 2 failed / 55. A5: 55 / 55. Transfer suite 76 → 79 (measured by hand). `runs/spark_secuura_2026-10-07_KS-1435-transfer-reject-signature-typed-control` |
   | `KS-591-platform-tenant-id-uuid` | KS-591 (from the KS-565 10-06 addendum) | `services/tenant-provisioning/src/tenant-provisioning.openapi.ts` | 3 one-line replacements, plus a new 50-line test | rc 0 | PASS 7/7 on the third control. A4: 3 failed / 5. A5: 5 / 5. `…KS-591-platform-tenant-id-uuid-control-r3` |
   | `KS-1432-apigw-ks529-guard-real-predicate` | KS-1432 | `services/api-gateway/src/routes/verification.ts` | 2 hunks (export the guard, call it), plus 1 hunk in the existing KS-529 test | rc 0 | PASS 7/7. A4: 9 failed / 10. A5: 10 / 10. api-gateway suite 818 → 820 (measured by hand). `…KS-1432-apigw-ks529-guard-real-predicate-control` |
   | `KS-591-transfer-custody-holder-id-uuid` | KS-591 (10-06 addendum) | `services/originate/src/originate.openapi.ts` | 1 one-line replacement, plus a new 39-line jest test | rc 0 | PASS 7/7. A4: 1 failed / 3. A5: 3 / 3. originate with the golden: 93 suites / 1077 tests, 0 failed. `…KS-591-transfer-custody-holder-id-uuid-control` |

   Files in each dir:
   - every dir: `KS-<n>.md`, `golden.diff`, `spark.pins`;
   - the two spec carves also carry `openapi-yaml.companion.diff`, the regenerated `docs/openapi/secuura-api.yaml` that the raise needs. `check:openapi` rc 0 was measured with the golden plus the companion.
4. **Routing:**
   - **KS-1435.** Spark: one line, spelled by the ticket. It mirrors the KS-518 approve fix in the same file. The harness is already in the test being modified. **Ornith-tier in shape.**
   - **KS-591 tenant id.** Spark: 3 identical one-line replacements placed by line number. The test shape is already landed in the service.
   - **KS-1432.** Spark: 3 hunks, including a hand-shaped export plus call site. The test is pure and in-process.
   - **KS-591 custody.** Spark: one line. The test shape is already landed in the service. **Ornith-tier in shape.**
   - Under "Spark on all tickets", all four go to the Spark. Nothing is left for Ornith.
5. **Not queued.** Wednesday appends the four dir names to `spark/queue.md`. The pins live in each `spark.pins`. Counter: round 0 of 2 on all four.

## Verdict table: the delta (26)

| Ticket | Verdict · predicate clause that failed |
|---|---|
| **KS-1435** transfer reject `signature` untyped | **BRIEFED.** |
| **KS-1432** KS-529 guard test tests a copy | **BRIEFED.** "Suggested fix (your call)" leaves only the name open, and the brief takes the ticket's own example. The call-site-deletion half of the acceptance is NOT unit-pinned (see the brief's UNMEASURED). |
| **KS-565** sweeps register | **BRIEFED as KS-591 carve 1.** The 10-06 13:55 addendum's `PATCH /api/platform/tenants/{id}/status` `format: uuid` row, widened to GET and PATCH `{id}` because the same `app.param` guard covers them (DELETE is left; see follow-ups). The addendum's §1 response-schema drifts fail on **decision** (fix the spec or the handler envelope: did, kyc sessions, security audit), and `POST /api/verification/verify`'s 400 envelope fails on **decision** too (the handler's other 400s may be `{verified,error}`, which would need a `oneOf`). |
| **KS-591** positive_data_acceptance register | **BRIEFED as carve 2.** The 10-06 11:29 addendum's transfer-custody `newHolderId` `format: uuid` row. The `oneOf` newHolderId/newHolderEmail rows fail on **decision** ("or relax the handler"), and so does `/share`'s recipient `anyOf`. |
| KS-593 not_a_server_error register | NOT. The new 10-06 rows are issuer-certs revoke/rotate 22P02 in `services/auth/` (an **auth/credential surface**), and "22P02 → 404 or validate as 400, whichever is the platform convention" is a **decision**. gdpr consent/dsr have **no cause**. |
| KS-1434 `ApiKeyCreateRequest` lacks `rotate` | NOT: **credential surface.** It is the API-key creation contract (`services/security`). It is spec-only and spelled, but a key-rotation field fails "when in doubt, treat as one". |
| KS-1433 connector scopes `anchors:read` / `documents:revoke` unenforced | NOT: **auth/scope surface**, and "your call" between gate-or-stop-minting (**decision**). |
| KS-1413 start scripts print the demo issuer password | NOT: **credential surface**, plus 2 files (`Start_Up/start-secuura.sh`, `scripts/start-local.sh`), and "your call". |
| KS-1427 unhandledRejection posture | NOT: **decision** ("decide whether it should survive or be fail-fast"). |
| KS-1426 lockfile clean-room scans four dirs | NOT: **no fix shape** ("Not claimed: a fix"). It is also preflight tooling over lockfiles (deploy-seat partition). |
| KS-1389 slot-target.sh unslotted export | NOT: **decision** ("asks for your view on one coordinated change"), cross-file with preflight leg 13 and `.githooks/pre-push`. |
| KS-1162 retired workflows bake slot ports | NOT: `.github/workflows/*`, **no runner**. |
| KS-1355, KS-1381, KS-1382, KS-1038 | The 10-06 verdicts stand: their only change since is Peter's 06:44 slot-label touch, with no new carve. KS-1382 `:31` also sits in job 06's file, which KS-1436 has just merged. |
| KS-576 bulk re-key, KS-583 DR rehearsal | NOT: **credential (key-rotation) surface**, multi-file features, blocked on KS-577. |
| KS-621 org-scoped document reads | NOT: a tracking ticket, "deliberately NOT a fix spec" (**decision**). It is also an authorization surface. |
| KS-784 teams webhook-config | NOT: an open question to Kamil (option 1 / 2 / neither) is a **decision**, and the route is an SSRF-adjacent validator. |
| KS-1428, KS-1429, KS-1430, KS-1431, KS-492, KS-590 | NOT: **assigned to Peter** (commission). |

The pre-10-06 board (275 Backlog+Todo) was not re-read. The 10-05 and 10-06 screens' verdicts stand for every ticket outside this delta, because nothing about them has changed since. The delta filter shows that.

## Partition and exclusions honoured

- No brief touches any of these:
  - `Testing/jobs/09-aggregate-report.sh` or any KS-1136 suite;
  - `check-package-format.sh`;
  - the KS-1313 reporter or the KS-1164 breakdown code;
  - any Dockerfile, lockfile, `package.json`, compose file or deploy script;
  - `Projects Documents/*.html`.
- The `docs/openapi/secuura-api.yaml` companions are raise-side regenerations, not model files.
- KS-1402, KS-1250 and KS-1175 were not considered, and nothing assigned to Peter or Stuart was briefed.

## Collision census

- GitHub REST GET, 23 open PRs, read ~11:20 AEDT. None touches any of the eight files these briefs write:
  - the four products;
  - `transfer.test.ts` and `ks529-non-object-body-guard.test.ts`;
  - the two new test paths.
- None touches `secuura-api.yaml` either.
- **Positive control:** the same census finds #1360, #649 and #575 touching `services/transfer` / `tenant-provisioning` `package*.json`, so the census does see those directories.
- Held Spark work on the same files, different lines:
  - `KS-591-platform-tenants-create-status` (held, not merged; `tenant-provisioning.openapi.ts:360`, `:484`). Measured: that golden first, then the new tenant golden, `git apply --check` rc 0.
  - `KS-1364-originate-share-system-errors` (held; `originate.openapi.ts:1601`, `:3763`, `:3911`). This brief's hunk is `:1629`–`:1631`. Stacking was not measured.
- `done.md`, `night/READY_*` and `night/briefs/*/golden.diff`: none of the four products or tests appears (`grep -F`).

## Tooling findings (none edited; Wednesday's call)

1. **A3e matches a listed "stays" line by TEXT, not by line number** (MEASURED). In the tenant brief, `## Where` listed DELETE's `:560` params line as "(correct) … stays". It is byte-identical to the three `must change` lines (`:455`, `:482`, `:522`).
   - The golden's control failed `A3e a line the brief says STAYS was REMOVED … :560` twice: once with the line quoted, and once with only `:560` named, because the builder reads the tip text for every `:N` in `## Where`.
   - It was fixed in the brief by not listing `:560` in `## Where`. It is kept in prose under Do NOT touch. Control r3 then passed.
   - The checker should key the stays check by line (or by hunk position) when the text is not unique in the file. Otherwise any brief that changes some, but not all, copies of a repeated line cannot name the copies it keeps.
2. **`ref=` may not equal `test_file=`** (build_input: "A3 refuses the pair"). For an in-place modification of a test that already carries the harness, the brief must pin a different sibling as `ref=`. Here that was ks474 for transfer and ks1071 for api-gateway. This is not a defect, but it is undocumented in the spark README's pin list.
3. **The num_ctx 32768 warning and refusal** fire on the Spark path (the builder refused originate at ~45K tokens). The Spark's window is 384K (lesson 2026-09-23). The precedent `ctx=` pins were used: 65536 for KS-1435 and KS-1432, 98304 for the custody carve. Whether `ctx=` changes anything on the Spark backend, beyond satisfying the builder gate, was not read.

## Follow-ups (not briefed)

- **DELETE `/api/platform/tenants/{id}` `format: uuid`** (`tenant-provisioning.openapi.ts:560`). It is the fourth copy of the tenant carve, and the 3-edit maximum left it out. A one-line Ornith-tier brief, best written after the tenant carve lands (same file).
- **KS-1432 route-level pin.** An in-process cell that drives `POST /api/documents` through `createVerificationRoutes` (ks1223 harness shape) would pin the call site. That would satisfy the ticket's "deleting the check at the call site turns the test red".

## UNMEASURED

- **No model round.** Whether the Spark reproduces each golden was not measured. The controls prove the builder, the checker and the goldens only.
- **No Schemathesis, no live stack.**
  - The spec carves' sweep effect is predicted from the rendered spec.
  - KS-1435's 200 is Peter's live measurement.
- **Stacking:** the custody carve was not stack-measured against the held `KS-1364-originate-share-system-errors` golden. The tenant carve was measured in one order only.
- **node_modules** come from the Secuura checkout's install, not a fresh `npm ci` at `69f2045af2a4`.
- **Tip suite counts:** measured by hand for transfer (76) and api-gateway (818). For originate and tenant-provisioning, only the with-golden counts were measured by hand. The checker's A6 ("no NEW red vs the untouched tip") covered all four.
- **Disk:** the controls left 6 per-round clones under `spark/cache/work/` (~335 MB each): KS-1435, KS-591 tenant ×3 (two failed controls plus the pass), KS-1432 and custody. Their run dirs are under `local-model/runs/…-control*`. Nothing was removed.
