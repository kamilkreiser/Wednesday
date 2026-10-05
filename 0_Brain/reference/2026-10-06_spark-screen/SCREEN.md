# KS screen for the Spark — 2026-10-06 (the 80%-Spark rule)

Written 2026-10-06 10:10 AEDT (shell `date`) by a Spark brief-writer sub-agent for Wednesday (Secuura scope). Authority: Kam 2026-10-06 09:37 (the weekly Claude allowance is past 70%, so the Spark takes 80% of tasks), the kit predicate (`spark-kit_2026-09-23/02_FOR_THE_COORDINATOR.md` §2) and the round counter (original + ONE rebrief).

**Read-only on client systems.**
- Linear: GraphQL reads only, `LINEAR_API_KEY` sourced transiently from the Blockchain `4_Credentials/.env`, never printed or written.
- GitHub: REST `GET` only (open PRs + files; one `compare`), `GH_TOKEN` from the same file, same handling.
- Git on the Blockchain checkout: read verbs only (`ls-remote`, `show`, `grep`, `ls-tree`, `log`, `cat-file`, `rev-parse`, `status`). Every write verb ran in two `git clone --shared` copies under this session's scratchpad (`sparkscreen/clone`, `sparkscreen/clone2`).
- The checkout reads 0 tracked-modified lines after the screen, HEAD still `c56dd7c32`.
- Nothing was raised, pushed, posted or mailed. `queue.sh` and a real `round.sh` were NOT started.

## BLUF

1. **Pool:** 10 tickets (`fleet/board_count.sh linear`, filter `team KS, state.type in [backlog, unstarted], updatedAt gt 2026-10-05T13:00:00Z`: `TOTAL=10`, a real count against the 250 limit). Same instrument, all states: 20. Added to the pool:
   - the gate residues: gate64, 65, 66 and 67 verdict mails, plus the gate60, 62 and 63 reports' finding rows;
   - KS-1127's leg-14 half;
   - a full census of the KS-1364/KS-591 "request body not marked required" class over the published spec at the tip;
   - KS-593's negative-offset and `::uuid`-cast class.
2. **Briefs written and queued: 2.** Both are rung 1, code_patch, measured red→green, and `round.sh --dry-run` rc 0.

   | Brief | What | Dry-run |
   |---|---|---|
   | `night/briefs/KS-1364-apigw-batch-certify-delegate/KS-1364.md` (sha256 `bb11b321978f62c9…`) | api-gateway: `POST /api/batch/certifications` + `/delegations` mark `requestBody.required` (2 one-line insertions, vitest) | **rc 0**, "DRY-RUN OK", prompt source WEDNESDAY BRIEF, 2 expected `+`, 2 red cells, ~13.3K tokens |
   | `night/briefs/KS-593-signatories-non-uuid-id/KS-593.md` (sha256 `87ecb9ca8c7e4eda…`) | originate `routes/signatories.ts`: `isUUID()` on the three query validators so a malformed id is a 400, not a `::uuid` 500 (3 one-line replacements, jest) | **rc 0**, "DRY-RUN OK", prompt source WEDNESDAY BRIEF, 3 must_change, 3 expected `+`, 3 red cells, ~16.6K tokens |

   `brief_lint.py` rc 0 on both. Both lines were appended to `spark/queue.md` (`queue.sh` was not running, measured by `pgrep`).
3. **Why only 2:** the pool is close to exhausted for the Spark tiers. The leading reasons:
   - the KS-1364/591 body-required class is now 2 operations from done; every other unmarked body is held, auth, security, credential or in a lane;
   - every new ticket is a decision, a lane, or multi-file;
   - the gate residues worth having are bash test-only cells, which **no wired tier can run** (see Tooling).
4. **Ornith-tier: technically yes, routed to the Spark.**
   - Both briefs are one-line-per-edit, spelled out, and carry a failable cell.
   - Under the 80%-Spark rule they go to the Spark, so Ornith's empty queue has this written reason: the only Ornith-shaped work in today's pool was queued on the Spark.
   - No other candidate was Ornith-shaped.
5. **develop moved during the screen:** `22b268143a63` → `3f9ff4e1e1b9` (#1385 KS-938 merged at ~10:05: auth `mfa.ts`/`users.ts` + the two platform-k HTML docs).
   - Neither brief's files changed (GitHub `compare`, then round.sh's own stale-brief check on both).
   - Seat E's KS-938 lane is now merged.

## Method

- **Tip.** `ls-remote` read `22b268143a6377c9a82cd03379daa596cd26d644` at the start. The checkout already held the commit object (its `origin/develop` ref is stale at `32e058975d4e`; nothing was fetched there).
- **Scratch clones.** `git clone --shared --no-checkout` of the checkout, then a detached checkout at `22b2`. `tasks/code_patch/prepare_clone.sh` farmed node_modules (api-gateway / originate + root + shared) and built `@secuura/shared` in each clone. The checkout reads 0 dirty lines before and after.
- **Class census.** `docs/openapi/secuura-api.yaml` at the tip was parsed with PyYAML. Every `requestBody` without `required: true` was listed with its component's `required` list: 75 operations. The `.openapi.ts` source pass (`bodies.py`) gives 87 rows; the difference is mcp-server and tokenisation, which are not in the published YAML.
- **Already-briefed check.** Each row was checked against held/queued briefs (`night/briefs/KS-591-*`, `KS-1364-*`, `KS-593-*` goldens and `## Do NOT touch` / control cells).
- **Per brief:**
  1. RED at the tip by assertion.
  2. GREEN with the golden.
  3. Whole service suite at the tip and with the golden.
  4. `tsc --noEmit` on the service.
  5. `git apply --check` strict on a clean clone.
  6. ASCII check.
  7. The brief's fences cut from the golden by script (`fill.py`), and the test fence equal to the measured file.
  8. For KS-1364: `generate-openapi --check` (rc 1 as expected), then regenerate and `check:openapi` rc 0. The YAML companion is filed beside the brief.
- **Collision census.** GitHub REST, 24 open PRs. 0 touch either product file or test path. #1394 touches the YAML, which is the KS-1364 raise companion, not a model file. Positive control: 11 PRs touch some `package.json`.

## Verdict table — the delta (KS Backlog+Todo, updatedAt > 2026-10-05T13:00Z, TOTAL=10)

| Ticket | Verdict · failing clause |
|---|---|
| KS-1424 updateDocument UUID-addressed 0-row write | NOT: **decision** ("Changing the other 12 needs its own decision"), and `documentRepo.ts` is **Seat B's live lane** (#1393). |
| KS-1423 gate64 minors on #1389 | NOT. N-1389-3 (assert 128+SIG) and N-1389-6 (pin item 3) are **bash test-only** cells in the runner suite, and **no wired tier runs a bash test-only change** (bash_patch needs a product `.sh` fix; test_only is not wired in round.sh). N-1389-1/4/5 are PR-text and figures. The `c4_docs_gate64.py` defect is WEDNESDAY fleet tooling, not the KS repo. |
| KS-1422 pre-push stale origin/develop | NOT: three remedies "in order of narrowness" (a choice); `.githooks/pre-push`, which every gate pins (NO-NEW-LEG); bash, no in-process cell. |
| KS-1421 Akto `Server: nginx` accept | NOT: **decision** (the 10-05 comment lists 3 mechanisms, "this needs one of"); about 15 cases over 5 files; a security-tier harness (Peter's split). |
| KS-1414 Schemathesis 4.29 negative_data_rejection | NOT: **no fix**. It records a tool false positive ("kept visible"). |
| KS-1412 gate61 r2 follow-ups | NOT: **KS-1401's files are excluded** (migration 049 + its suite); r2-2 is the two platform HTML docs (off limits). |
| KS-1051 originate suite gated nowhere | NOT: prior verdict holds (CI/gate wiring, no in-process red); the new comment adds no carve. |
| KS-1038 auth-exhaustive races its lockout | NOT: Playwright e2e (**no runner**), "Suggested fix (not prescribed)", auth surface. |
| KS-709 Akto PASS on nothing executed | NOT: "fail **or** mark as a distinct non-pass" (**decision**); flips 4 security workflows red (a policy change); `systemTest/akto` is Peter's split; security-tier surface. |
| KS-492 Review G | NOT: an epic (security regression coverage), Peter's. |

## Gate residues read (gate6x verdict mails / reports)

| Finding | Verdict · clause |
|---|---|
| N-1389-3, N-1389-6 (gate64, runner cells) | NOT: **bash test-only, no tier** (see Tooling). |
| N-1393-1..7 (gate65, #1393) | NOT: **Seat B live lane** (`documentRepo.ts`, `routes/documents.ts`). |
| N-1385-1 (gate66, KS-938 cells count NULL params) | NOT: KS-938's test (Seat E's PR, merged ~10:05 as #1385); auth/MFA surface. N-1385-2..6 are auth/MFA follow-ups (security). |
| N-1394-1..8 (gate67) | NOT: **Seat B live lane** (#1394, anchors tx). "GET /api/anchors/queue unreachable behind /:id" is a route-order **decision** ("needs a backlog row by the owner"). |
| N-1387-2 (gate62: KS-1388 cells pin only the first line, `grep -m1`) | NOT: **bash test-only, no tier.** It is the one real Spark-sized residue lost to the harness gap. |
| N-1388-1..6 (gate63, KS-1404 TSA trust anchors) | NOT: **security surface** (TSA verification). |
| N-1384-1..10 (gate60, KS-1210 oauth apps) | NOT: **auth surface**. |
| N-1376-1..9 (gate D2, KS-1404 RFC 3161) | NOT: **security surface**. |

## Named candidates

- **KS-1127 leg-14 half.** NOT.
  - Leg 14 already runs `run-shell-suites.sh`, whose verdict line now carries the skip tally (#1234). The open bullet ("leg 14 quotes that line") has **no spelled edit**.
  - It sits in `scripts/preflight/preflight.sh`, which every gate pins as NO-NEW-LEG.
  - Bash; no in-process cell.
- **KS-1364 / KS-591 body-required class** (75 unmarked bodies in the published YAML at the tip):
  - **BRIEFED: `POST /api/batch/certifications` + `/delegations`.** The component `required` list is non-empty and the handler 400s an absent body.
  - **Already held/passed by earlier Spark carves:**
    - analytics exports;
    - anchors (×2);
    - billing customers, bundle and credits/use;
    - teams (×2);
    - nft mint, upload, platform-fee, pin, unpin and estimate-size;
    - share, ingest and resolve-by-service;
    - stake;
    - tenants create and status;
    - timestamps verify;
    - transfers and delegations (×2).
  - **`PUT /api/nft/admin/platform-fee`** (the 10-05 comment's new row) is already in the held `KS-591-nft-mint-upload-fee` PASS. Caught before briefing; it would have been a duplicate.
  - **`DELETE /api/platform/tenants/{id}`:** NOT. The held `KS-591-platform-tenants-create-status` PASS carries a NEGATIVE control (TNC3) asserting DELETE stays optional, so marking it required would red a held test. That is a **decision** for Wednesday (the handler does refuse `{}`: `confirm !== true` → 400, `index.ts:494`-`:496`).
  - **`POST /api/identity-credentials/issue`:** NOT. A **credential surface** (VC issuance); "when in doubt, treat as one".
  - **`POST /api/batch/verify`, privacy/settings, settings/notifications, referrals/generate, verification/verify, client-errors, billing PUT customers/{id}, did, webhooks PATCH, documents revoke:** NOT. The component `required` list is empty and/or the handler accepts `{}`, so the lint rule's premise fails (a per-op **decision**, per the ticket's "23 operations happily accept an empty body").
  - **auth, security, issuer-certs, wallet, kyc, m365 connections/exchange-token, tokenisation:** NOT. **auth/security/credential/token surfaces.**
  - **register-connector:** NOT. **Seat E's lane** (connector allow-list).
  - **mcp-server:** NOT. Not in the published spec, and connector-adjacent (Seat E).
  - **admin/credits:** NOT. A contract **decision** (`delta` vs `credits`), recorded by the 10-05 carve.
- **KS-593 (not_a_server_error):**
  - **BRIEFED: GET `/api/signatories` (its measured ninth operation) + the `/check` sibling.**
  - **Negative-offset sites:**
    - adminConfig ×2 already held;
    - auth `users.ts` ×2: auth service, and Seat E's KS-938 just touched `users.ts`;
    - tenant-provisioning `GET /api/audit-log` (`index.ts:556`): NOT, **no in-process harness**. Importing `index.ts` runs a top-level `await platformPool.query` and `app.listen`; the only test there exercises an extracted guard module;
    - api-gateway `notifications.ts:112`: NOT, `Array.slice(-1)` cannot 500, so it is not this class;
    - `platform.ts:383`: recorded as already guarded by the 10-05 carve.
  - Other register rows are a live lane (lifecycle-events, revoke: `routes/documents.ts`), held (share), or auth/security (`users/admin/*`, rate-limit, exchange-token, webhook rotate-secret).

## Briefs written

| Brief dir (under `2_Project_Files/local-model/night/briefs/`) | Files beside it | Measured | Dry-run rc |
|---|---|---|---|
| `KS-1364-apigw-batch-certify-delegate/` | `KS-1364.md`, `golden.diff`, `openapi-yaml.companion.diff`, `spark.pins` (`tier=code_patch`, `ref=` billing ks1364 spec test, `line=352`, `started_ok=`) | new test alone 2 failed / 3 passed (5) → 5/5; api-gateway 91/812 → 92/817, 0 failed; tsc rc 0; gen --check rc 1 → regen + check:openapi rc 0; strict apply rc 0 | **0** |
| `KS-593-signatories-non-uuid-id/` | `KS-593.md`, `golden.diff` (`-U2`), `spark.pins` (`tier=code_patch`, `ref=` ks730c, `line=144`) | new test alone 3 failed / 3 passed (6) → 6/6; with ks1293 2 suites / 16 passed (no manifest line needed); originate 90/1063 → 91/1069, 0 failed; tsc rc 0; strict apply rc 0 | **0** |

Queue lines added to `spark/queue.md`: `KS-1364-apigw-batch-certify-delegate`, `KS-593-signatories-non-uuid-id`. Pins live in each `spark.pins`. Counter: round 0 of 2 on both.

## Tooling findings (none edited; Wednesday's call)

1. **No tier runs a bash test-only change** (MEASURED from source).
   - `build_bash_input.sh` has a product-fix mode and a self-testing mode only (no tamper mode); `brief_lint.py` refuses `test_only`; `night/build_input.sh` takes vitest/jest only.
   - Today this blocked two otherwise Spark-sized gate residues: N-1387-2 (`grep -m1` pins only the first line) and N-1389-3 (assert 128+SIG, not just non-zero).
   - **The fix that opens the class:** a bash TAMPER mode (`## Tamper` line/from/to on the product `.sh` or `.env.example`, the test hunk alone must red under the tamper), mirroring code_patch's TEST-ONLY mode.
2. **Cosmetic, round.sh stale-brief print** (`round.sh:204`-`:206`).
   - A path that exists at neither commit (a NEW test file) is re-tried as `$SUBDIR/$p` and printed doubled (`Blockchain/Dev/Blockchain/Dev/...__tests__/new.test.ts`).
   - Harmless for a new file (nothing to drift).
   - The line misstates what was checked.
3. **`--control` was not run.** Its run dirs land in `local-model/runs/` and `cache/work/`, outside this commission's write scope. The goldens were proved by hand instead (see Briefs). Wednesday may run `round.sh <dir> --control` before draining.

## UNMEASURED

- No Spark round and no `--control` round, so whether the checker accepts each golden end to end is not measured. The dry-run proves the builder only.
- No Schemathesis, no live stack, no real Postgres.
  - KS-1364's sweep effect is a prediction; neither batch op is in the ticket's measured table.
  - KS-593's list-route 500 is the ticket's 2026-08-28 live measurement. The `/check` sibling's 500 is reasoned from identical code.
- node_modules come from the Secuura checkout's install (HEAD `c56dd7c32`), not a fresh `npm ci` at the tip.
- The ~200 tickets outside today's delta were not re-read. Their 10-05 verdicts stand by the delta filter (no update since 13:00Z).
- The other signatory routes (`/:id`, revoke, update) and the rest of originate's `query(...).isString()` → `::uuid` sites were not screened for the KS-593 class. `routes/documents.ts` is a live lane anyway.
- Open PRs were read at ~10:0x AEDT; a later PR is not covered.

## Instruments (scratch, not filed)

All under `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/e2216636-d4a8-4372-af80-77a0943bf859/scratchpad/sparkscreen/`:
- `pull.py`: paginated Linear GraphQL pull; the key is read from the environment.
- `bodies.py`: the source pass over `*.openapi.ts`.
- `req.py`: the YAML pass with component `required` lists.
- `fill.py`: fills a brief from its golden; asserts no placeholder is left.
- `tpl_*.md`: the brief templates.
- `*_golden.diff`: the goldens.
- `*suite*.out`: the suite runs.
- `dry_*.out`: the dry-runs.
