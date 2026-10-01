# KS delta screen for the Spark — 2026-10-02

Written 06:21 AEST 2026-10-02 (shell `date`) by a Spark brief-writer sub-agent for Wednesday (session 73252fd5). Scope: Secuura/Blockchain only. Authority: the week instruction (Spark first, valid to 2026-10-04), plus the top row of `EXPIRING-GRANTS.md` (Kam, 2026-10-01 17:40) for screen and brief sub-agents while usage is past 90%.

That row ends when Kam switches accounts on Friday morning. Whether he had switched by 06:06 was **not measured** here.

**Read-only on the client systems:**
- Linear was read over GraphQL: issues, comments and issue history. The key was sourced by name from `4_Credentials/.env` and never printed. There was no mutation and no comment.
- GitHub was read with REST `GET` and `ls-remote`: the develop branch, open PRs and their files.
- Nothing was written under `!CODING/`. Git write verbs ran only in this session's scratchpad clones.
- Nothing was raised, pushed, merged, posted or mailed.

## BLUF

1. **What was screened** (frame: KS Backlog+Todo updated since 2026-10-01T00:11Z, plus the gate residue, plus KS-1015/KS-1364 one-file carves, at develop `88e8877a2a0d`):
   - **13 tickets** (`fleet/board_count.sh`, `team KS, state.type in [backlog, unstarted], updatedAt gt 2026-10-01T00:11:00Z`: TOTAL=13, a real count against the 250 limit).
   - **Board frame, same instrument:** Backlog 242 and Todo 33, so 275 open. KS updated since 00:11Z across all states: 19.
   - **Gate residue:** gate52's N-1367-1 to N-1367-9 and N-1368-1 to N-1368-5, and gate53's N-1369-1 to N-1369-8, all read in the reports.
   - **Carves:** KS-1015's untriaged pairs and KS-1364's 4 remaining operations.
2. **The delta is almost all metadata.** Linear issue history was read for all 13:
   - 7 changes are one Peter action at 11:18Z that added the label `slots-not-fully-isolated`: KS-1038, 1162, 1355, 1381, 1382, 1388, 1389.
   - KS-772 and KS-1376 gained relation links only.
   - KS-608 had an empty history row.
   - KS-1396 got Peter's comment on his own ticket.
   - **Genuinely new: KS-1401 and KS-1402.**
   - Prior verdicts are re-used for the 9 tickets with no content change, and the table says so.
3. **Spark-briefable: 1. KS-1015 carve `delegation-get`.**
   - The pair is `response_schema_conformance::GET /api/delegations/{id}`, recorded by KS-1015's 2026-09-29 sweep comment as the sibling of the referral pair that #1367 landed.
   - The change is one product file and one edit point, with a spelled-out shape (the spec follows the handler's envelope) and the #1367 test shape to copy. It is not auth (a delegation read behind the standard bearer gate; the change is to a response schema only), it is not in any open PR, and it has had 0 rounds.
4. **The round passed and is held.**
   - **Spark round 1: PASS 7/7 strict + A2a.** patch.diff is **BYTE-IDENTICAL** to the golden (cmp rc 0). Red 3/6 → 6/6. The transfer suite went from 70 to 76 with 0 new reds; tsc rc 0. The round took 49.8 s, with prompt 25,795 and completion 1,526 tokens.
   - **HELD:** `2_Project_Files/local-model/night/READY_KS-1015-DELEGATION-GET-1_spark-dsv4flash_BRIEFED-CODEPATCH-TRANSFER.OPENAPI-PASS-7of7_2026-10-02.diff.md` (hold_ready rc 0, plus one marked hand line for the YAML companion).
   - No rebrief was needed.
5. **Ornith-tier: 0.** The queue gets a measured WHY line (`night/queue.md`). `night/PAUSE_QUEUE` was rewritten with an epoch on line 1, lapsing at 2026-10-03 06:00:00 AEST.
   - **Finding:** yesterday's PAUSE_QUEUE had prose on line 1, so `night_run.sh` never treated it as live. It failed open; see IMPROVEMENTS.
6. **Next:**
   - A Claude raise seat (a cloud necessity: the Spark cannot raise) takes the held READY plus `night/briefs/KS-1015-delegation-get/KS-1015.openapi-yaml.companion.diff` as one small PR (`Refs KS-1015`), then a QA gate.
   - **Wednesday rules on N-1367-1** (the referral owner-list spec mismatch). It would be Spark-briefable after that ruling.

## Method

- **Tip:** develop `88e8877a2a0d6a626b9c2a7c4b71d3a909e6f94e` (#1369, 2026-10-01T16:15:26Z).
  - Read by GitHub REST `GET /branches/develop` at ~06:07, and by `ls-remote` from the scratch clone at 06:20. Unchanged.
  - Since yesterday's batch-3 base `0736d8b7`, develop gained #1367 (KS-1015 referral envelope), #1368 (KS-1364, 2 operations) and #1369 (KS-530 lock).
- **Source clone:** `git clone --shared` of the Blockchain checkout into `73252fd5…/scratchpad/src`.
  - Origin was set to GitHub, with the deploy-key `core.sshCommand`, IN THE SCRATCH CLONE ONLY. Then `fetch develop` and a detached checkout.
  - node_modules: the root and `packages/shared` are symlinked to the cb6b682a farm (sparkfeed, installed at `94c9c7aa`). They are excluded via the clone's `.git/info/exclude` (porcelain 0).
  - Transfer has its own `package-lock.json`. The root farm alone gives `tsc --noEmit -p services/transfer` **rc 0 at the tip**, so its lock was not farmed. This was measured both ways only on the root side; see UNMEASURED.
- **Round scripts:** batch 3's `mkclone`, `precheck`, `round`, `genyaml`, `measure` and `vt.sh` (from `79817561…/scratchpad/b3/`) were copied into `73252fd5…/scratchpad/r/`.
  - Only `SP`, `TIP` and the run-dir date were changed. The `diff` of each copy was printed and read.
  - **One deliberate change to `precheck.sh`:** the NEGATIVE now takes `NEG_FROM`/`NEG_TO` from the environment and asserts that the line changed. The old copy would have silently run an unmutated golden on a brief with no `required: true` line (IMPROVEMENTS).
- **Harness:** unchanged since batch 3. The `checker.sh` and multiset `a3c_plus.py` are not edited. Batch 3's smoke is cited, and this brief still ran build_input → golden CONTROL → NEGATIVE before its round.
- **Builder gate:** KS-1015 is **In Progress** (it moved itself at 09:08:04Z on 10-01, per gate52 N-1367-9). It was admitted with `started_ok=Wednesday-commissioned-KS-1015-one-file-carves-2026-10-02;the-#1367-lane-is-merged-and-left-the-delegation-pair-to-the-residue`. The attached PR #1367 reads merged.
- **Collision:** 21 open PRs (REST `GET /pulls?state=open` + `/pulls/N/files`, ~06:12 AEST).
  - None touches `transfer.openapi.ts`, `routes/delegations.ts`, any `*.openapi.ts` or `docs/openapi/secuura-api.yaml`.
  - Transfer is touched only by #1360 (its `package-lock.json`) and by #649/#575 (its `package.json`).
  - **Positive control:** the same census finds 11 PRs touching some `package.json`.
- **Commission exclusions applied:**
  - KS-1402 (auth, on a Kam card);
  - KS-528 / react-router audit rows (Kam's card `secuura-fuse-1009-measured-1001`);
  - auth, token, credential and security surfaces;
  - Peter's and Stuart's tickets;
  - `package.json`, `package-lock.json` and `scripts/audit/`.

## Verdict table — the 13 delta tickets (frame: KS Backlog+Todo, updatedAt > 2026-10-01T00:11Z, TOTAL=13)

The Ornith column applies the same predicate plus "simplest one-file". Every Spark NOT is also an Ornith NOT.

| Ticket | State | What changed since 00:11Z (Linear history) | Spark verdict · failing clause | Ornith |
|---|---|---|---|---|
| KS-1038 | Backlog | label added (Peter 11:18Z) | NOT, **re-used** from the 10-01 screen: e2e lockout race (Playwright); **auth surface** | NOT |
| KS-1162 | Backlog | label added | NOT, **re-used** from 09-30 DELTA: `.github/workflows` (excluded); "derive … or delete … needs Kam's nod" (**decision**) | NOT |
| KS-1355 | Todo | label added | NOT, **re-used** from 09-30 DELTA: **4 files**; spot 1 needs a designed output format (**fix shape not spelled out**) | NOT |
| KS-1376 | Backlog | relation to KS-1401 (Kamil 01:51Z) | NOT, **re-used** from the 10-01 sweep: certifications RLS FORCE with no policy (**security surface**; kintsugi RLS gap, excluded) | NOT |
| KS-1381 | Todo | label added | NOT, **re-used** from 09-30 DELTA: **many files**; "Fix shape (Kamil's call)" (**decision**) | NOT |
| KS-1382 | Todo | label added | NOT, **re-used** from 09-30 DELTA: 5 `Blockchain/Testing` security-harness entry points (**multi-file, security, decision**) | NOT |
| KS-1388 | Backlog | label added | NOT, **re-used** from 09-30 DELTA: comment lines in two `.env.example` files (**2 files, no failable test**) | NOT |
| KS-1389 | Backlog | label added | NOT, **re-used** from 09-30 DELTA: "asks for your view on one coordinated change" (**decision**; touches `.githooks`) | NOT |
| KS-1396 | Todo | comment by Peter on his own ticket (05:29Z) | NOT: **assigned to Peter** (TS 7 / oxlint migration, his lane) | NOT |
| KS-1401 | Backlog | **NEW** (created 01:49Z) | NOT, read in full: `charge_events` RLS off on kintsugi. This is an RLS gap (**security surface**, and the kintsugi RLS gap is excluded). "This ticket does not write the fix" (**fix shape not spelled out**). It is a live-database condition with no in-process red | NOT |
| KS-1402 | Backlog | **NEW** (created 09:43Z; description edited 09:53Z) | NOT: auth `/api/users/lookup` connector tokens (**auth surface**; on Kam's card `secuura-ks1402-lookup-refuses-connector-tokens`), **excluded by commission** | NOT |
| KS-608 | Backlog | empty history row (Peter 08:11Z) | NOT, **re-used** from the 10-01 screen: Peter-created, "DO NOT START — waiting on one answer" (**decision**) | NOT |
| KS-772 | Todo | relation to KS-1402 (Peter 09:43Z) | NOT, **re-used** from 09-30 DELTA: a review-stream umbrella of 20 tickets (**no single file**) | NOT |

**Positive control for this census:** KS-1402 is known to be new on 2026-10-01 (it is on Kam's card), and it is in the 13. So the filter fires. `board_count.sh` itself refuses an unvalidated zero, and TOTAL was non-zero.

## Verdict table — gate residue (gate52 report `…/2026-10-01-batch1367-g52/report.md`, gate53 `…/2026-10-02-batch1369-g53/report.md`)

| Finding | What it is | Spark verdict · failing clause | Ornith |
|---|---|---|---|
| **N-1367-1** | The owner list `GET /api/referrals/user/{userId}` spec (`referral.openapi.ts:551`, `{ codes: ReferralCode[] }`) does not match its handler (`routes/referrals.ts:169` onward, `{ success, data: { hasCode, referralCode{…}, stats, milestoneProgress… } }`). | NOT TODAY: **decision**. The gate writes "a candidate for the KS-1015 residue, **for Wednesday to rule**". No sweep pair has been recorded for it. Plausibly the sweep sees 403: the handler refuses `authUserId !== userId` at `:176`-`:178`, which is UNMEASURED. The handler has **two body shapes** (`hasCode:false` + `message`, the `hasCode: false` line at `:187`; and `hasCode:true` + nested from `:193`, the `hasCode: true` line at `:196`), so the schema shape (optional fields or `oneOf`) is a design choice. **Spark-shaped once ruled:** one file, one edit point, and the #1367/delegation test shape. | NOT |
| N-1367-2 | Whether `Refs KS-1015` is the right home for the referral lookup pair (a Linear question). | NOT: **no code** (decision) | NOT |
| N-1367-3..8 | Polish/Info: a 404 description, DB-outage 404, the hand-rolled envelope, `is_active` nullability, "public" wording, and 429/502/503 writers. Each one "predates this PR" or is runtime. | NOT: no fix shape asked for. Each is a wording or record item, or would need a ruling (e.g. 3 = description vs filter) | NOT |
| N-1367-9 | KS-1015 and KS-1364 read In Progress. | NOT: board state, no code | NOT |
| N-1368-1 | `/referrals/generate`: the sweep's 400 is plausibly the 5-code cap, not a body refusal. NOT MEASURED by the gate. | NOT: **a measurement, no code**. It supports leaving generate unmarked (batch 3's verdict stands) | NOT |
| N-1368-2..5 | Commit wording, the replica's body-parser version, a v1/v2 cite, and tsc not type-checking tests. | NOT: no code fix (wording/info) | NOT |
| N-1369-1, -5, -6, -7 | PR-body and commit wording on the merged #1369. | NOT: **no code** (the merged PR's text) | NOT |
| N-1369-2, -3 | npm 11.5.1 vs 11.19.0 `npm ls` / lock churn. | NOT: toolchain, `package-lock.json` (excluded) | NOT |
| N-1369-4 | The `// overrides KS-493` note in `Blockchain/Dev/package.json` is false for `@prisma/dev` 0.24.3. | NOT: `package.json` (**excluded**); a supply-chain record (security) | NOT |
| N-1369-8 | npm `fixAvailable` suggestion moves. | NOT: info only | NOT |

## Verdict table — carves

| Carve | Verdict · clause |
|---|---|
| **KS-1015 `GET /api/delegations/{id}`** (2026-09-29 comment) | **SPARK — BRIEFED, PASS round 1, HELD.** One file (`transfer.openapi.ts`), one edit point (`:1196`). The shape is spelled out: the handler `routes/delegations.ts:148`-`:154` answers `{ success, data: { delegation, chain } }`, and the file's three sibling delegation 200s already use `successEnvelope`. The test shape is #1367's referral test (`ref=` pinned). It is not auth (a response schema; the route sits behind the standard `jwtAuthenticate`, `index.ts:438`, unchanged). No open PR touches it; 0 rounds; the runner is vitest. |
| KS-1015 group B: `GET /api/kyc/microsoft/result/{sessionId}`, `GET /api/kyc/microsoft/user/{userId}/sessions`, `PATCH /api/did/{did}` | NOT: **identity-verification / DID surfaces** (credential-adjacent; when in doubt, treat it as security). Not opened at source. |
| KS-1015 finding 1, non-auth: `PUT /api/privacy/settings`, `PUT /api/settings/notifications`, `POST /api/documents/{id}/share` | NOT: **fix shape not spelled out.** Each fires two checks, and the ticket says "both sides … worth reading together". At `88e8877a` the notifications response is already modelled flat to the live shape (`api-gateway.openapi.ts:729`-`:741`, KS-719), so no source-visible spec/handler delta remains to brief without a fresh sweep. Share is an access-granting surface. |
| KS-1015 finding 1, `/api/auth/` + `/mfa/` pairs (13) | NOT: **auth surface** (commission). |
| KS-1015 finding 2 (10 baseline entries citing Done tickets) | NOT: systemTest baseline hygiene, which the ticket assigns to Peter. |
| KS-1364, the 4 operations left (13 of 17 are in develop via #1365 + #1368, confirmed by `git log 0736d8b7..88e8877a`) | NOT, **reasons re-checked cheaply and unchanged:** `issuer-certs`, `users/admin/{id}` and `users/me/change-password` are all registered in `services/auth/src/auth.openapi.ts` (**auth surface**). `referrals/generate` **does not refuse an absent body** (batch 3's probe: 201). `git diff --stat 0736d8b7 88e8877a -- services/referral services/auth` shows only #1367's spec + test, so the handlers are unchanged. |

**Positive control for "0 more briefable":** the same predicate, applied the same way, passed the delegation carve, which then passed on the Spark. So the screen can say yes.

## Round evidence — KS-1015 delegation-get

| Step | Result |
|---|---|
| Brief | `2_Project_Files/local-model/night/briefs/KS-1015-delegation-get/KS-1015.md`. Every template heading is filled. One edit point (line, current text, new text). Do-not-touch is named. UNMEASURED is filled. The timestamp is shell-generated (06:14). A python `==` confirmed the brief's edit block equals the golden's product hunk and its `ts` block equals the golden test file. |
| Golden (scratch clone `r/gold`) | Test alone at tip: **3 failed / 3 passed / 6**, D1-D3 by assertion. Golden 6/6. Transfer suite 4 files / 70 → 5 / 76, 0 failed. `tsc --noEmit -p services/transfer` rc 0 at tip and golden. Strict `git apply --check` of golden and companion at `88e8877a`: rc 0 each. |
| YAML | Golden alone, `generate-openapi -- --check`: rc 1. Golden + `KS-1015.openapi-yaml.companion.diff` (+38/-1), `check:openapi`: rc 0 ("CHECK PASS", 405 example blocks). |
| build_input | rc 0, "prompt source: WEDNESDAY BRIEF … the ticket description is NOT the prompt"; expected `+` lines 23 (A3c); red cells 3 (`precheck/build_input.out`). |
| Golden CONTROL (`spark_checker.sh`) | **PASS 7/7 + A2a** (strict). |
| NEGATIVE (golden, `totalDepth: z.number().int(),` → `totalDepth: z.number(),`) | **rc 1, FAIL A3c** "1 of 23 line(s) … ABSENT". The checker can fail. |
| Spark | `/health` 200 before the round (round.sh). No other Spark client in `ps`. Thinking OFF (`think=0`, `thinking_chars=0`), `done_reason=stop`, temperature 0, one request, no retry. |
| Round 1 | `runs/spark_secuura_2026-10-02_KS-1015-delegation-get`: **PASS 7/7 strict + A2a**. A3c 23/23; A4 red 3/6 by assertion; A5 6/6; A6 70 → 76, no new red; A7 tsc rc 0. **patch.diff BYTE-IDENTICAL to golden.diff (cmp rc 0).** 49.8 s / 25,795 / 1,526. |
| Kit rule 4, six clauses | (1) strict apply at a known commit, mode recorded; (2) added lines byte-identical (cmp); (3) touched set = the 2 named files; (4) RED 3/6 at tip, GREEN 6/6 with the product hunk; (5) suite 70 → 76, 0 new reds; (6) every assertion's output kept in `out.md.checker/`. **All six held.** |
| Hold | `hold_ready.py … DELEGATION-GET-1 --title-from-brief … --model-tag spark-dsv4flash`: rc 0, "golden: BYTE-IDENTICAL". **READY:** `night/READY_KS-1015-DELEGATION-GET-1_spark-dsv4flash_BRIEFED-CODEPATCH-TRANSFER.OPENAPI-PASS-7of7_2026-10-02.diff.md`. One raise-step line (the YAML companion) was added BY HAND and marked; the backup is `night/briefs/KS-1015-delegation-get/READY.md.pre-1002-handline`. |
| Records | Ladder row 58 (`SPARK_LADDER.md`, backup `.pre-1002-row58`). IMPROVEMENTS entry (backup `.pre-1002-delegation`). Brief README. |

No FAIL, so no model/harness/brief classification was owed. Counter: round 1 of 2 used.

## Queue / PAUSE_QUEUE

- `night/queue.md`: a measured WHY line was appended (backups: `queue.md.pre-1002-0620-why`, and `scratchpad/queue.md.pre-1002`).
- `night/PAUSE_QUEUE`: rewritten with line 1 = `1790971200` (2026-10-03 06:00:00 AEST), then the reason. Backups: `PAUSE_QUEUE.pre-1002-0620`, and `scratchpad/PAUSE_QUEUE.pre-1002`.
- **Probe** (`night_run.sh` `_g7_pause_live`, lines `:124`-`:140` sourced in a scratch shell, rc on its own line):
  - new file: rc 0 (live);
  - yesterday's file: rc 1;
  - human-date control: rc 1.
- **Yesterday's pause was therefore never live to the G7 leg.** It failed open. IMPROVEMENTS item (1).

## For Wednesday

- **Raise:** the delegation READY plus its YAML companion. It is 1 product line → 23, a 79-line test, and the YAML (+38/-1). Commit as `Refs KS-1015`.
- **Rule N-1367-1:** is the owner list a KS-1015 pair, and should the spec use optional fields across the two branches or a `oneOf`? With that ruling it is a one-brief Spark carve.
- **Observed, not briefed:** `GET /api/delegations?type=granted|received` answers `{ delegations, count }` (`routes/delegations.ts:125`-`:131`), which `DelegationListResponse` (requiring `granted`/`received`) does not describe. No sweep pair names it, so the shape is evidence, not a recorded failure.

## UNMEASURED

1. No Schemathesis or live run. That the delegation pair stops firing is a prediction from the rendered spec.
2. The delegation handler was not booted. That the `delegation` row serialises to the published `Delegation` component rests on KS-440's republish (`transfer.openapi.ts:500`-`:509`) and was not re-measured.
3. node_modules come from sparkfeed (installed at `94c9c7aa`), not a fresh `npm ci` at `88e8877a`. Transfer's own lock was not installed. tsc and vitest pass on the root farm, but whether the service lock's modules would change that was not measured.
4. Open PRs were read at ~06:12 AEST. A later PR is not covered.
5. Whether Kam had switched accounts by 06:06 (the end event of the grant row) was not measured.
6. The 9 re-used verdicts were not re-read. Their history since 00:11Z shows label or relation changes only.
7. KS-1015 group B (KYC/DID) was excluded by title and surface, not opened at source.
8. The served `/api/docs/openapi.json` was not read.

## Instruments filed here

`pull.py` (paginated Linear pull) and `hist.py` (Linear issue history). Both read the key from the environment and never print it.
