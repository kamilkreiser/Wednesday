# DRAFTER REPORT — #1035 (KS-1204) TIER 1 ROUND 1 gate @ 4b1fb0621

Re-drafted 2026-09-18 00:57:34 → 01:3x AEST (clocks from `date`). A first drafter ran 2026-09-17 23:42 → 23:54 and died at the account session limit. `GS/` = this directory. The dead drafter's scripts are `drafter_*` with outputs under `GS/out/`; the re-drafter's scripts are `redraft_*`, `api_read_1035.py`, `gen_launcher_1035.py`, `make_fixtures_1035.py` and `check_launcher_1035.sh`, with outputs under `GS/out/r2/`.

- **The Secuura checkout:** only read verbs ran there (`ls-remote`, `status --porcelain`, `rev-parse`, `show`, `diff`, `grep`, `cat-file`, `for-each-ref`, `branch --show-current`, `log`, `merge-base` via the clone).
- **The re-drafter clone:** every build, vitest run, tamper, harness, `merge-tree` and `commit-tree` ran in `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8f7ffae4-dc85-433a-8a53-4d87581eb627/scratchpad/gate1035/gate1035_redraft_24e4lwaf/`. Worktrees there: `wt_head` 4b1fb0621, `wt_dev` 3961c2add, `wt_merged` 2295ed89b (a clone-only commit of tree d21341805). The side install is `vitest41111/`, and moved-aside probe and tsc dirs are under `_quarantine/`.
- **The dead drafter's clone** (`/private/tmp/claude-501/drafter1035/…`) was READ for comparison only, never run in.
- Nothing was pushed, filed, commented, merged or mailed. The launcher ran with `--check` only. Nothing was fetched.

## BLUF

- **SET READY: launcher `--check` rc=0** at head `4b1fb0621` / develop `3961c2add` (01:22:02 and 01:23:05). **18 / 18 controls PASS** (`out/r2/check.out`). The head was unchanged at 01:30:13.
  - **Caution:** at 01:29:12 a seat started 4 `login_stub.mjs` listeners from `worktrees/raise-0916-a`, the seat worktree #1035 was built in. A push is in flight. **Re-run `--check` immediately before launch.**
- **Predicted verdict: GO WITH FINDINGS** under the drafted RULE BEFORE LAUNCH (D1 = TICKET). It becomes **NO GO** if Wednesday rules the container fail-open in scope.
- **Lead 3: the refusal on the REAL route (MEASURED twice, 23:53 and 01:10; head = merged; test AND production).**
  - Each tree × boot has 240 graded rows (20 stored shapes × 12 bodies). 132 of them are refused 403 `FORBIDDEN` with the non-array message: 11 non-array shapes, including `0`, `1`, `false` and `true`, which the seat never tried.
  - **0 oracle violations.** The planted controls were flagged 2 / 2.
  - **Absent / null / array rows match develop 108 / 108.** No row forwards at head that did not forward at develop.
  - N-3 precedence holds.
  - Array-like `{0,length}`: develop answers 500 (`allowedTypes.includes is not a function`) and head answers 403. The process survives under both rejection modes.
  - The dead drafter's rows equal the re-drafter's, 281 / 281, on head and on develop.
- **The production boot needed an INSTRUMENT.** `POST /api/v1/documents` with `application/json` never answers, on both trees. This is pre-existing: `express.json` consumes the stream before the hand-parsing route.
  - The census used `application/vnd.qa1035+json` instead. It passes `enforceJsonContentType` but not `express.json`.
  - Controls: the JSON request times out, and `/api/documents` answers 307.
- **Lead 1: readers (READ + MEASURED).**
  - `GET /api/connector/info` (`health.ts:58`) tells a connector **`[]` (= "all types permitted") for a stored `""` / `0` / `false` while every create is 403**. It echoes the other non-arrays raw, which breaks the spec's `array of string`.
  - The MCP `tools/info.ts` relays it.
  - There are 0 readers in originate, auth, shared or the portals.
  - No cell sees this (tamper X-INFO-ALWAYS-EMPTY gives 0 reds).
- **Lead 2: stored shapes.**
  - **The only writer is `PUT /api/admin/settings`.** It stores all 21 shapes verbatim for SYSTEM_ADMIN, **ORG_ADMIN and ISSUER_ADMIN** (200). `/api/v1` writes are HTML-escaped by `sanitizeInput`. Redis keeps them with a 24 h TTL (READ).
  - Seeds, migrations, scripts and the frontend write 0 allow-lists.
  - **A CONTAINER FAIL-OPEN, pre-existing, in the same authorisation block (unchanged lines 1212-1219):**
    - `integrations` as an object, `[null, entry]`, a duplicate id, a string `config`, or `null` each leave a restricted connector unrestricted (201).
    - **One admin-portal Settings save (transcribed, PROBED) turns the stored array into `{"0": entry}`.** That drops every restriction.
  - **Migration residual: UNMEASURED.** The instrument is a read-only GET of `secuura:gateway:notif:platform-settings` per deployment, not run under KS-535.
- **The seat's claims re-derive:**
  - Tamper table **8 / 8 exactly, 12 reds** (parsed from its ROWS literal, never executed).
  - Suites **57/556 develop, 58/565 head and merged**, at default and at 60 s on vitest 4.1.11. Head is **also 58/565 on the seat's 4.1.10**.
  - tsc 0 on all three trees. The test-including program gives 32 error lines in 11 test files on all three trees, 0 in ks1204; the plant adds +1.
  - eslint: `verification.ts` 0 / 5 on all three trees, the test 0 / 0, and the control fires.
- **Completion items, already true:**
  - The PR body carries the migration-residual section (13:36:37Z).
  - **KS-1230** exists: Backlog, our account, related KS-1204, `Refs KS-1204`, no duplicate.
  - `attachmentsForURL(pull/1035)` = KS-1204 contributes only.
  - KS-1204 is In Progress.

## Outputs

- **Brief:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1035-ks1204-tier1.md` (38.5 KB, sha256 `0bfcb1c8b5cdd8d4`).
- **Prompt:** `…/briefs/2026-09-17_secuura-1035-ks1204-tier1.prompt.txt` (19,558 b, under 19,800; sha256 `e5b98583edca2875`).
- **Launcher:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1204_1035.sh` (sha256 `372ec6ba55d88fe6`, 241 lines, mode 755).
  - Generated by `gen_launcher_1035.py` from `launch_qa_secuura_ks1215_1034.sh` (`out/r2/gen_launcher.out`): 29 asserted substitutions, all count 1.
  - Pins were re-read from the repo: 19 files at 732c13459 AND 3961c2add, and the 2 PR blobs at head.
  - Guards run: a residual-token check over the body (19 tokens), output controls, heredoc parity (PY 0 / 8=8; PYJ 0 / 96=96), no git write verb, no control bytes, `bash -n` 0.
  - The generator left `launch_qa_secuura_ks1204_1035.sh.pre-012246` beside the launcher. That is the first generation, before a tail-text fix ("items 3, 4, 5, 7" → "3, 4, 5, 6").
- **Verdict subject** (exit 23 guards it): `[QA -> Wednesday] TIER 1 GATE #1035 (KS-1204) 4b1fb0621 — <GO | GO WITH FINDINGS | NO GO>`, FROM coagent@ TO wednesday-agent@.
- **Report directory named:** `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1204-1035-4b1fb0621-tier1-r1/`.
- **PRIOR REPORT named:** `…/reports/2026-09-17-ks1176-1014r2-9ba0caf78-tier1-r2/`.

## Launcher `--check` (`out/r2/check_first.out`, `out/r2/check.out`)

- **rc=0.**
  - Head on origin at the branch.
  - Compare `732c13459 ahead=1 files=2`.
  - All 19 JUDGED blobs = develop.
  - `origin develop MOVED 732c13459 -> 3961c2add: commits=1 files=5 — GUARDED hits 0`.
  - Every brief and prompt guard passes.
- **JUDGED by blob at the CURRENT develop (19):**
  - `routes/verification.ts` `28fb58343` (LANDED `f888e8cd0` → 19) and the ks1204 test ABSENT (LANDED `f1f9840ed` → 19).
  - `index.ts`, `routes/admin.ts`, `services/{health,redis,enforcement}.ts`, `middleware/{auth,contentType}.ts`, the ks1176 test.
  - Gateway `package.json` / `vitest.config.ts` / `vitest.setup.ts` / `tsconfig.json`.
  - Shared `utils/gracefulShutdown.ts`, frontend admin `pages/Settings.tsx`, mcp-server `tools/info.ts` and `package-generator.ts`, and Dev `eslint.config.mjs`.
- **GUARDED on a develop move:** `services/api-gateway/src/`, the 4 gateway config files, `packages/shared/src/`, `eslint.config.mjs`, `Settings.tsx` and the 2 mcp-server readers. `DEV_CONTENT_ALLOWED` is empty.
- **Controls, want = got (18 / 18):**

| control | want = got |
|---|---|
| verification.ts fixture = develop bytes `28fb58343` | 0 |
| verification.ts fixture = #1035 bytes `f888e8cd0` | 19 LANDED |
| verification.ts fixture = develop + 1 line (`7ac7551d1`) | 18 |
| CUR_DEV = `732c13459` (the pinned arm) | 0 |
| CUR_DEV = `3961c2add` (a REAL develop move, disjoint) | 0 |
| CUR_DEV = `27e53ec3a` (behind → UNJUDGEABLE) | 18 |
| CUR_DEV = `fd81a75f0` (#1034's head: JUDGED `auth.ts` `bf09d315a` unpinned) | 18 |
| CUR_DEV = `4b1fb0621` (#1035 itself) | 19 |
| HEAD = `732c13459` | 6 |
| prompt without the subject / per-ENTRY farm / PRIOR REPORT / NOT-TESTED-first / CLOSED-STILL OPEN-NEW | 23 / 22 / 24 / 24 / 25 |
| brief without MERGE ADDENDUM / full SHA; ROUND 2; TIER 2 | 25 / 20 / 15 / 7 |

- **NOT proven:** the GUARDED compare arm on a real commit ahead of 732c13459 that touches a GUARDED path outside the JUDGED set. None exists; the fd81a75f0 control is caught by the JUDGED arm first. The launch path itself was never run (TTY guard exit 21 untested, by rule).
- **Launch-order risk:** #1034 (`middleware/auth.ts`) is JUDGED and GUARDED. **If #1034 merges before this gate launches, `--check` refuses (exit 18) and the set must be re-pinned.**

## What was REUSED from the dead drafter, and what was RE-DERIVED

| item | dead drafter (23:42–23:54, develop 732c13459) | re-drafter (01:05–01:30, develop 3961c2add) |
|---|---|---|
| setup / merge-in | `drafter_setup_1035.py`: head = one commit on 732c13459, merge-tree = head tree | **re-run fresh** (`redraft_setup_1035.py`): develop moved; merged tree **d21341805** over 3961c2add, 0 conflicts. Every relevant subtree merged = head; patch-id equal `5fa4c81a7a9a` |
| vitest 4.1.11 side install + farm | `drafter_vitest41111_1035.py` + `drafter_farm_1035.py` | **re-run fresh** in the session scratch (`redraft_farm_1035.py`). 3961c2add's vitest closure = 732c13459's (40 entries). 987 / 8 / 8 per entry, 0 wholesale links, shared IN TREE, 4.1.11 via `vitest.mjs`, 4.1.10 control |
| suites / tsc / eslint | `drafter_suites_1035.py`: 57/556 · 58/565; 32-line map; eslint 0/5 | **re-run** on 3 trees by an asserted derivation (`redraft_suites_1035.py`). All numbers identical, plus merged 58/565 and head on 4.1.10 58/565 |
| real-app probe | **it DID run** (its "not yet done" record was stale): head + develop, test census, the production WRITER + path controls, the array-like in test. Its production census had hung on `/api/v1/documents` (run 1) | **re-run on 3 trees** with the r2 template (per-step Content-Type), **adding the production census** through the `+json` instrument and the array-like in production × both modes. Its test-census rows = the new rows 281/281 on both trees |
| census of LISTEN | `drafter_census_1035.py` (23:47: 17 / 0 / 0) | `redraft_census_1035.py` (01:09:58 and 01:11:01: 17 / 0 / 0; at 01:30:07: 21 / 4 / 4 = a SEAT's stubs from `raise-0916-a`, started 01:29:12, not mine) |
| tamper table | not reached | **new** (`redraft_tamper_1035.py`): the seat's 8 (parsed) + 7 re-drafter rows |
| reader / stored-shape census, Linear / GitHub / mail | not reached | **new** (READ + `api_read_1035.py`) |
| launcher, fixtures, controls, brief, prompt | not reached | **new** |

## Measured leads (predictions for the gate)

### 3. The refusal on the real route (`out/r2/table.out`, grader `redraft_table_1035.py`, oracle from the receipt's words)

| tree × boot | create rows | 201 fwd | 403 non-array | 403 member | 400 | oracle violations |
|---|---|---|---|---|---|---|
| head test `/api` | 265 | 64 | **132** | 55 | 13 | **0** |
| merged test | 265 | 64 | 132 | 55 | 13 | 0 |
| head production `/api/v1` (+json) | 265 | 62 | **132** | 55 | 13 | **0** |
| merged production | 265 | 62 | 132 | 55 | 13 | 0 |
| develop test | 265 | 150 | 0 | 62 | 52 | n/a |
| develop production | 265 | 148 | 0 | 63 | 51 | n/a |

- Every non-array refusal carries code `FORBIDDEN` and the message "Connector document-type allow-list is not a list; refusing until it is corrected".
- Head vs merged: 0 differing rows, in both boots. Test vs production: 0 differing rows at head and merged (groups A/B/D).
- **The one develop row that differs between test and production:** the stored JSON-looking string, read back through `/api/v1` as `[&quot;SSD_DOCUMENT&quot;]` (`sanitizeInput`).
- **Array-like `{0:"SSD_DOCUMENT",length:1}`:**
  - develop gives 500 `INTERNAL_ERROR` ("Document-create pipeline threw … allowedTypes.includes is not a function") in test and production, modes unset and `survive`. The process serves the next create (201).
  - head and merged give 403 non-array in all 4 arms.

### 1. Readers (git grep whole repo, case-insensitive; 12 files; outside `Blockchain/Dev` 0; spellings `allowed_document_types` / `allowedDocTypes` 0; positive control `rawAllowedTypes` ×3)

| reader | kind | vs the refusal |
|---|---|---|
| `api-gateway/src/routes/verification.ts:1225` POST /api/documents | runtime, CHANGED | refuses every non-array (measured) |
| `verification.ts:1260-1266` same route, bypass lookup | runtime | reads `workflowPolicy` only; runs after the refusal |
| `api-gateway/src/services/health.ts:58` GET /api/connector/info | runtime | **`""` / `0` / `false` → `[]`** while creates are 403. Other non-arrays are echoed raw (measured, head test) |
| `mcp-server/src/tools/info.ts:144` | relay of the above | inherits it (READ) |
| `mcp-server/src/package-generator.ts:106,398`, `http-server.ts:226,258` | the generate-package REQUEST body, not the store | `.length` / `.join`: a string input would throw (READ) |
| `frontend/admin/src/services/api.ts:1075` | a TS type (`McpPackageRequest`) | no writer of the store |
| `MCP Deployment/troubleshooting.md:123`, both `openapi.yaml:367` | docs / spec | "empty list = all types permitted"; `array of string` |

### 2. Stored shapes (`out/r2/table.out` admin rows)

- **Writer:** `routes/admin.ts:1123-1129` only. It does a shallow merge with no validation.
  - Roles (`ADMIN_ROLES :571`): SYSTEM_ADMIN 200, **ORG_ADMIN 200, ISSUER_ADMIN 200**, issuer 403, no token 401.
  - It stores all 20 shapes + the array-like verbatim.
- **Mount-path difference:** writes through `/api/v1/admin/settings` are parsed globally and HTML-escaped by `sanitizeInput` (`index.ts:458`). Writes through `/api/admin/settings` (a `proxyPaths` prefix) are not.
- **Store:** `redis.ts:680-687` uses `setex(…notif:platform-settings, 86400)` in Redis mode, and a Map with no TTL in the fallback.
- **Other sources:** seeds / migrations / scripts / frontend write 0 allow-lists. `SEED_INTEGRATIONS` (`admin.ts:378`) goes to `setIntegration` (a different store, never read by create).
- **Container shapes** (restricted entry `["SSD_DOCUMENT"]`, create `DOCUMENT`):

| stored `integrations` | head = develop = merged, both boots |
|---|---|
| `[entry]` (control) | 403 member |
| `{"0": entry}` (object) | **201** |
| `[null, entry]` | **201** |
| `[{id, config:{}}, entry]` (duplicate id) | **201** |
| `[{id, config:"SSD_DOCUMENT"}]` | **201** |
| `null` | **201** |
| after ONE Settings.tsx save (transcribed) editing only `general.platformName` | **201** (was 403) |

- **Migration residual: UNMEASURED.**
  - Instrument: per deployment, a read-only `GET secuura:gateway:notif:platform-settings` plus its `TTL`, or `GET /api/v1/admin/settings` as SYSTEM_ADMIN. Classify the `integrations` container type and each `config.allowedDocumentTypes` type.
  - Only a hand-made API PUT can have stored a non-array, and in Redis mode it expires 24 h after the last settings write.
  - The PR body's sentence names string / object / empty string. The refusal also catches numbers and booleans.

### 4. Tampers (`out/r2/tamper.out`, WHOLE suite 58/565 every row, tsc 0 every row, restored blob + `git diff --quiet` every row, vitest 4.1.11, 60 s)

| row | aimed at | reds | cells |
|---|---|---|---|
| T0 / T0-DEFAULT / TI | seat | 0 / 0 / 0 | — |
| RP-DEV (develop bytes `28fb58343`) | seat | 4 | string-vs-DOCUMENT, string / object / empty-string |
| NOGUARD | seat | 4 | same 4 |
| STRING-ONLY | seat | 1 | object |
| FALSY-OPEN | seat | 1 | empty string |
| G-REV | seat | 2 | both N-3 cells |
| **seat total** | | **12 = 8/8 as predicted** | all AssertionError |
| X-NULL-REFUSED | a CONTROL cell | 1 | "absent, null or empty-array … no restriction" |
| X-UNTYPED-OPEN | the refusal (veto 3) | 3 | string / object / empty string |
| X-STATUS-400 | the refusal (veto 1) | 4 | same 4 as RP-DEV |
| X-OBJECT-AS-LIST | the predicate | 1 | object (the array-like is unpinned) |
| X-DT-ONLY | a CONTROL (ks1176 F) | 1 | ks1176 "restricted to DOCUMENT naming SSD_DOCUMENT via `type`" |
| **X-MSG-MEMBER** | the refusal message | **0** | no cell tells a non-array refusal from a member refusal |
| **X-INFO-ALWAYS-EMPTY** (health.ts) | the info reader | **0** | no cell sees what a connector is told |

## NOT TESTED by the drafters

- A real Redis, a deployed platform-settings, or the migration residual (KS-535).
- The real admin portal page: Settings.tsx was TRANSCRIBED, not rendered.
- A real originate / security / auth, or the edge.
- The consequence runs of the two zero-red tamper rows.
- `vitest list --filesOnly` proof for the probe (the probe is a tsx process, not a vitest file; the tsc `--listFilesOnly` proof ran: 0 `qa_` in the project program).
- The launch path (TTY guard).
- Schemathesis / Akto (not commissioned).

## Slips (named against their predictor)

- **Dead drafter:**
  - Its recorded state ("the real-app probe on both trees NOT yet done") was stale: the probe HAD run at 23:53–23:54.
  - Its production census (run 1) hung on `/api/v1/documents` for 240 s before it knew about the body-parser interaction.
  - Its first template-count assert (2) did not count the header-comment occurrence.
- **Re-drafter:**
  - One tool call carried a `cd` and was refused by the hook; it was re-issued without.
  - The generator's first file count said "eighteen" for 19 files; its own output control caught it (19 ≠ 18) and nothing was written until fixed.
  - The first launcher tail said "items 3, 4, 5, 7"; it was fixed to 3, 4, 5, 6 and regenerated (`.pre-012246` kept).
- **Seat:**
  - `tamper_1204.py`'s header comment says "edits to api-gateway middleware/auth.ts"; its rows edit `routes/verification.ts` (inert).
  - Its suite numbers are on vitest 4.1.10 (`npx`). They hold on 4.1.11 too.
- **Checkout reading:** `.git/config` sha256 changed `f9ef2cb7e4b9fa5a` (23:42) → `2716d950dd2834b2` (01:05) and refs 945 → 947 between the two drafters, by neither drafter. Record.

## For Wednesday to rule in the brief before launch (RULE BEFORE LAUNCH)

- **D1, the container fail-open, decides the verdict class.**
  - Drafted default: out of #1035's scope, a NEW pre-existing TICKET (predicted Major, escalation candidate) → **GO WITH FINDINGS**.
  - If ruled in scope (the fail-closed ruling covers the container) → **NO GO**, round 1 of 2.
  - Also rule whether KS-1230's scope should absorb it (the write side cannot fix the portal's own object-shaped save), or whether it needs its own ticket.
- **D2, the info reader** telling `[]` while refusing: drafted default is a NEW Minor TICKET. It could fold into KS-1230 only if Wednesday says so.
- **D3, the residual:** drafted default is UNMEASURED; the gate names the instrument and does not read a deployed store. A deployed read would be a separate commission for Kam.
- **Launch hygiene:**
  - Re-run `bash launchers/launch_qa_secuura_ks1204_1035.sh --check` right before launch: a seat push from `raise-0916-a` was in flight at 01:29.
  - If #1034 merges first, the launcher refuses (exit 18) by design and the set needs a re-pin.
