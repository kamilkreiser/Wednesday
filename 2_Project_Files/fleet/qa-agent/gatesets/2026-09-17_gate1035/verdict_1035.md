SUBJECT: [QA -> Wednesday] TIER 1 GATE #1035 (KS-1204) 4b1fb0621 — GO WITH FINDINGS
FROM: CoAgent <coagent@agentmail.to>
TS: 2026-09-17T15:53:58.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
QA agent -> Wednesday | TIER 1 ROUND 1 gate #1035 (KS-1204, Seat A) | sent Fri 18 Sep 2026 01:53:57 AEST (from `date`)

## BLUF
VERDICT: GO WITH FINDINGS — on `4b1fb0621e58ff00bba096751130bc6e53df4714`, as the delta over develop `732c13459`, AND on the merged tree `d21341805c976676a417755032ba781a7b6da3b7` over then-current develop `3961c2add8e1637b32e638f8f0952c328c00833e` (unchanged at 01:36:00, 01:45:27, 01:47:53 and the pre-mail re-read 01:51:39; merged tree = the re-drafter's).

Why GO:
- The non-array refusal holds exactly as ruled on the REAL route, in both boots, at head and merged:
  - 225 / 225 non-array create rows are 403 `FORBIDDEN` with the non-array message, 0 forwarded.
  - 0 oracle violations. Planted controls 3 / 3 flagged.
  - Absent / null / array rows = develop 150 / 150. 0 new forwards.
  - N-3 holds. L1–L8 do not move.
- The seat's tamper table re-derives 8 / 8 exactly (12 reds).
- Suites are 57/556 -> 58/565 -> 58/565 on vitest 4.1.11.

Why WITH FINDINGS: every finding is pre-existing or a test / wording gap, graded TICKET under your 01:32 D1 / D2 ruling. None is a Blocker against #1035.
- The real-browser half of tier 1 does not apply: #1035 changes no rendered surface.

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-18-ks1204-1035-4b1fb0621-tier1-r1/report.md (NOT-TESTED.written-first.md at 01:34:46, before any run; evidence/ holds every script and output).

## Recommendation
1. Sign GO on `4b1fb0621` under the TESTED grant. The merge addendum is below.
2. Open three tickets. I file nothing.
   - D1: the container fail-open plus the portal save. Major, escalation candidate. Its own ticket, not KS-1230.
   - D2: the info reader. Minor.
   - N-A: the 24 h TTL expiry erasing every connector restriction in Redis mode. READ ONLY, Major pending measurement, escalation candidate.
3. Optional for the seat: the N-B cells (message class, array-like) and the N-D PR-body wording. Neither gates this verdict.

## Items 1–9
1. READERS:
   - Whole-repo case-insensitive git grep finds 12 files and 20 lines at head (control `rawAllowedTypes` 3 / 0).
   - Runtime readers:
     - `verification.ts:1225` (changed; refuses);
     - `:1260` (workflowPolicy only, after the refusal);
     - `health.ts:58` `GET /api/connector/info`;
     - MCP relays `tools/info.ts:144` AND `http-server.ts:199` (the drafter named only the first).
   - `package-generator` reads a request body. 0 readers in originate / auth / shared / portals.
   - MEASURED DISAGREEMENT (D2): info tells `[]` (= "all types permitted") for a stored `""`, `0` and `false` while 15 / 15 creates are 403. It echoes the 12 other non-arrays raw, against the spec's `array of string`. Nothing substring-matches any more.
2. STORED SHAPES:
   - The only writer is `PUT /api/admin/settings`. Seeds / migrations / scripts / frontend write 0.
   - It stores all 25 shapes plus the array-like verbatim. SYSTEM_ADMIN, ORG_ADMIN, ISSUER_ADMIN, issuer_admin and platform_admin get 200 (tenant-scoped admins write PLATFORM-wide restrictions). issuer and connector get 403; no token 401.
   - `/api/v1` writes are HTML-escaped by `sanitizeInput` (MEASURED).
   - TTL 86400 s (READ).
   - CONTAINER FAIL-OPEN (D1), MEASURED, head = develop = merged, both boots: `{"0":entry}`, `[null,entry]`, a duplicate id, a string `config`, `integrations:"x"` and `null` each let a `["SSD_DOCUMENT"]` connector create DOCUMENT 201.
   - One Settings-page save (transform PROBED; READ of `Settings.tsx:37-42,62-69` confirms the transcription) turns the array into `{"0":…}`: 403 before, 201 after.
   - RESIDUAL: UNMEASURED. Instrument: per deployment, a read-only `GET secuura:gateway:notif:platform-settings` plus `TTL`, or `GET /api/v1/admin/settings` as SYSTEM_ADMIN. Classify the container, each entry/config, and each allowedDocumentTypes type. A key past 24 h reads as absent. Who runs it: a deploy owner on Kam's authorisation, not a gate.
   - The PR body's sentence is INCOMPLETE: the refusal also catches `0`, `1`, `-1`, `true`, `false`, `" "` and `"[]"`.
3. REFUSAL ON THE REAL ROUTE:
   - The real `index.ts` ran as a real tsx process, test boot on `/api` and production on `/api/v1`, via the `application/vnd.qa1035+json` INSTRUMENT.
   - Each of head / merged × test / production has 375 group-A rows (25 shapes × 15 bodies): 225 non-array refused, 0 violations, 150 / 150 = develop, 0 new forwards. Head = merged (416 + 35 rows); test = production (411).
   - Develop forwarded 147 of the 225, including 65 DOCUMENT-typed bodies.
   - Array-like: develop gives 500 plus an untyped 201; head and merged give 403 in all 4 arms, and the process survives.
   - L7: a no-scope connector gets the scope refusal first, = develop. L8: a human JWT create = develop.
   - PATH CONTROLS: `/api/v1/documents` with `application/json` never answers on all trees in BOTH boots (the drafters said production only). `/api/documents` answers 307 in production. A real production JSON connector create never reaches the refusal (pre-existing, STILL OPEN).
   - My rows = the re-drafter's r2 rows on 240 overlapping rows ×6, 0 differing.
4. TAMPERS (whole suite at head, vitest 4.1.11, 60 s):
   - Collector proof: `vitest list` 0 `qa_` (ks1204 listed), `tsc --listFilesOnly` 0 `qa_` (verification.ts listed).
   - 21 rows, all tsc 0, 58 / 565 / 0, restored, AssertionError only.
   - Seat 8 / 8 = 12 reds. Re-drafter 7 / 7 as measured (X-MSG-MEMBER 0, X-INFO-ALWAYS-EMPTY 0).
   - Mine: Q-NO-RETURN 4, Q-CODE-OTHER 4, Q-DUCK-LENGTH 3, Q-ARRAYLIKE-OPEN 0, Q-EMPTYARR-REFUSED 1 (control), Q-ARRAY-SUBSTRING 2 (control; I predicted 1: my slip).
   - Zero-red consequences on the tampered real app:
     - X-MSG-MEMBER: a connector is told "not permitted to register document type SSD_DOCUMENT" for the type its list names.
     - X-INFO-ALWAYS-EMPTY: `["SSD_DOCUMENT"]` is told `[]` while DOCUMENT is 403.
     - Q-ARRAYLIKE-OPEN: 500 on typed creates and 201 untyped return.
   - No cell sees the message class, the info reader, the array-like, the container shapes or the `/api/v1` mount.
5. CHECKS:
   - Suites: develop 57/556, head 58/565, merged 58/565, at default AND 60 s on 4.1.11. Head is also 58/565 on `.bin/vitest` 4.1.10. 0 failed, 0 pending, ks1204 9/9, load 5.9–8.9.
   - Project tsc rc 0 ×3. The project program is 491 files and excludes tests.
   - The TEST-INCLUDING program (scratch tsconfig outside services/): develop 623 files / head and merged 624 files, 32 error lines in 11 test files, an identical per-file map on all three, 0 in ks1204, plant +1.
   - eslint: `verification.ts` 0 / 5 on all three (two warnings shifted +10); the test 0 / 0; the planted control fires as 1 WARNING.
6. MERGE-IN:
   - The only parent 732c13459 = merge-base. merge-tree gives `d21341805`, 0 conflicts.
   - develop..merged = the 2 PR files. patch-id `5fa4c81a7a9a` equal (control `3bf1aa5957cf`).
   - The api-gateway / shared / frontend-admin / mcp-server subtrees merged = head.
   - The develop move #1033 touches 0 GUARDED paths (items 3 / 4 / 5 were re-run on merged anyway).
7. COMPLETION (read 01:44:45 and again 01:51:39):
   - The body carries the residual section: accurate but incomplete (N-D).
   - KS-1230 exists (Backlog, related KS-1204, `Refs KS-1204`, 0 attachments, no duplicate). It does NOT cover D1 or D2, and a Linear search found no ticket for either.
   - attachmentsForURL(pull/1035) = [KS-1204 contributes]. Controls: pull/1014 -> KS-1176, pull/99999 -> 0.
   - 0 closing phrases in title, body and commit (regex controls 5/5).
   - KS-1204 stays In Progress on merge.
8. SCHEMATHESIS / AKTO: NOT REQUIRED.
   - The behaviour needs admin-stored state before a connector call, a two-principal stateful sequence neither tool generates. The deterministic real-app census covers it.
   - TICKET note for D2: a schema check of /api/connector/info would flag the raw echoes but NOT the `""` / `0` / `false` -> `[]` half, so D2's regression must assert info/refusal agreement.
9. CARRY-FORWARD: the table below.

## CLOSED / STILL OPEN / NEW
- #1014r2 N-2 (string substring-match): CLOSED, MEASURED. SHIPS-WITH.
- #1014r2 N-3 (precedence unpinned): CLOSED, MEASURED (G-REV 2 reds; census 0 violations). SHIPS-WITH.
- Array-like 500: CLOSED at runtime, MEASURED, but unpinned (N-B). SHIPS-WITH.
- N-4 / KS-1203 (untyped under an array list 201): STILL OPEN, MEASURED = develop. TICKET (KS-1203).
- D1 container fail-open + portal save: NEW (pre-existing), MEASURED + PROBED + READ, Major. TICKET (own; escalation candidate).
- D2 info reader: NEW (pre-existing), MEASURED, Minor. TICKET (own).
- Writer roles and shapes (KS-1230): STILL OPEN, MEASURED. TICKET KS-1230 (+ scope notes: tenant-scoped admins; sanitizeInput).
- sanitizeInput escaping on /api/v1 writes: STILL OPEN, MEASURED. TICKET note.
- 24 h TTL: STILL OPEN. Consequence NEW = N-A, READ ONLY, Major pending measurement. TICKET, escalation candidate.
- POST /api/v1/documents JSON never answers: STILL OPEN, MEASURED, both boots. TICKET / escalation candidate (existing ticket not checked).
- Unused ks1176 stub route: STILL OPEN, Polish. SHIPS-WITH.
- N-B test gaps (message class, array-like, info reader): NEW, MEASURED by tamper, Minor. SHIPS-WITH optional, else TICKET.
- N-D PR-body residual sentence omits numbers / booleans: NEW, Polish. SHIPS-WITH (wording).

## NOT TESTED (same prominence)
- The migration residual / any deployed platform-settings (KS-535, D3).
- A real Redis, including the 24 h expiry (N-A is READ ONLY).
- A real `application/json` production create (unreachable in-repo; production rows used the +json instrument), and the edge.
- Real security / auth / originate: one loopback recorder.
- The rendered admin portal: Settings.tsx was READ and its transform PROBED.
- The MCP server as a process.
- The workflow-bypass read under array lists.
- Concurrent admin writes, replay, network failure.
- Schemathesis / Akto / k6 / Playwright (not commissioned).
- A separate red-proof step of the ks1204 file at develop (RP-DEV is the equivalent reading).
- The D1 / D2 Linear dedupe was bounded to the first 50 fuzzy results.

## Bounds
- Checkout (start / mid / close, all identical): porcelain 0, config `2716d950dd2834b2`, refs 947, worktrees 112, branch feature/ks-597-b-caller-scoped-externalref, gateway .vite [vitest].
- LISTEN census: start 17 rows / 0 node / 0 stubs. Close 19 rows / 1 node / 0 stubs / 0 under my workdir; the 1 node listener is a concurrent gate's (gate1034r), not mine.
- All my listeners were identified by port + argv + cwd and SIGTERM'd; 0 alive.
- docker info rc 0; no container created.
- No push, comment, filing or rm. Quarantine by MOVE.

## Prediction slips
- Drafters / brief: the /api/v1 JSON hang is in BOTH boots, not production only.
- Drafter: missed the second MCP relay `http-server.ts:199`.
- Brief item 5: the eslint control fires as a warning, not an error.
- Mine:
  - the collector-proof matcher counted my workdir name `gate1035qa_` (run 1 aborted before any row; kept);
  - a grader KeyError (run 1, kept);
  - an api_read copy assert (kept);
  - Q-ARRAY-SUBSTRING predicted 1, measured 2.
- Seat: all 8 rows exact; its body sentence omits numbers / booleans.

## MERGE ADDENDUM
on Wednesday's signed GO naming the head: squash 4b1fb0621 onto develop 3961c2add8e1637b32e638f8f0952c328c00833e (then-current at 01:51:39; 732c13459 = the head's parent) (merged tree d21341805c976676a417755032ba781a7b6da3b7; re-drafter d21341805 — equal); #1035 attaches to KS-1204 only, linkKind contributes, no closes; KS-1204 stays In Progress on merge (§5f: a real Redis / platform-settings and the migration residual are unmeasured); KS-1230 stays Backlog; equality targets after the squash: verification.ts f888e8cd0 / ks1204 test f1f9840ed (ks1176 test 43cebf8d7, health.ts f43052734, admin.ts f47dd6a65 unchanged); api-gateway 57/556 at develop -> 58/565 at head -> 58/565 merged on vitest 4.1.11 (re-measure; head also 58/565 on 4.1.10); dispositions: N-2 CLOSED SHIPS-WITH, N-3 CLOSED SHIPS-WITH, array-like 500 CLOSED SHIPS-WITH, N-4/KS-1203 STILL OPEN TICKET, D1 container fail-open + portal save NEW Major TICKET (own ticket, not KS-1230; escalation candidate), D2 info reader NEW Minor TICKET, KS-1230 STILL OPEN TICKET (+ scope notes: tenant-scoped admins write platform-wide restrictions; sanitizeInput escaping on /api/v1), /api/v1 JSON create hang STILL OPEN TICKET, unused ks1176 stub Polish SHIPS-WITH; NEW: N-A 24 h TTL expiry erases every connector restriction in Redis mode (READ ONLY, Major pending measurement, TICKET, escalation candidate), N-B test gaps (message class, array-like, info reader; SHIPS-WITH optional else TICKET), N-D PR-body residual sentence omits numbers/booleans (Polish); Records for KS-1204's facts comment at merge: the migration residual (UNMEASURED, instrument: per deployment read-only GET of secuura:gateway:notif:platform-settings + its TTL, or GET /api/v1/admin/settings as SYSTEM_ADMIN, classifying the integrations container, each entry/config type and each config.allowedDocumentTypes type; a key past its 24 h TTL reads as absent), the container fail-open (pre-existing, head = develop, ticketed separately; one Settings-page save turns integrations into {"0": entry} and lifts every restriction), the info reader (tells [] for "", 0, false while creates are 403; ticketed separately), the /api/v1 JSON create hang (both boots, pre-existing), the refusal also catches numbers and booleans, arrays of non-strings stay unvalidated (KS-1230).

Escalation candidates for Wednesday (anything needing a push is yours to route):
- D1 (Major; reachable through the product's own Settings page).
- N-A (Major if Redis mode is deployed).
- The /api/v1 JSON create hang.

