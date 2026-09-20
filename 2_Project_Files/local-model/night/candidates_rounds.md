<!-- HAND-WRITTEN, APPEND-ONLY. Never generated. night_run.sh re-derives night/candidates.md
     every run and OVERWRITES anything appended there — that is why rounds 1-13 of 2026-09-19 had to
     be preserved in night/candidates_rounds_archive_2026-09-19.md, and why round notes live here
     from now on. Rounds 14-19 (2026-09-19/20) left only log lines in night/queue.md; they were never
     written as tables, so this file starts at round 20. Newest section at the BOTTOM (append-only). -->

# Ornith candidate rounds — rejection tables

Each `## round N` section records one search commission: what was read, from where, and one line per
ticket or gate row with its reject reason or FIT. The table is what stops the next seat re-deriving
the same answers.

---

## round 20 — 2026-09-20 15:28-15:35 AEST (Wednesday's search-and-brief subagent)

**Verdict: 0 FITS. A refusal, measured.** Nothing was briefed, nothing queued, nothing run on the
model, no git write verb anywhere (no scratch clone was needed — nothing reached the measuring
stage). `login_stub.mjs` listeners started: 0; `pgrep -fl login_stub.mjs | wc -l` = 0 at close.

**Tip:** origin develop `e470198783bcb1ef0eac94780f87579974051423`, read with
`git -C .../Blockchain/2_Project_Files ls-remote origin refs/heads/develop` at 15:28 and again at
15:33 — unchanged across the round.

**Commission:** a WIDENING search over the board itself, because the gate lane's lists were reported
used up. Sources in order: (1) the KS board Backlog/Todo via `night/candidates.md` as regenerated
today 09:46 from **362** tickets, then Linear read-only per ticket (`comments` not needed — no row
reached that depth); (2) the round tables already written
(`candidates_rounds_archive_2026-09-19.md`, rounds 1-13; `queue.md` log lines for rounds 14-19);
(3) the gate reports under `Testing Agent MAIN/projects/secuura/reports/`.

**Counts (from commands, not memory):** **46 distinct KS tickets touched on Linear** — 23 read with
their full description, 21 more read at title + state + assignee (the auth-shaped pool), 2 more via
the `createdAt > 2026-09-19` listing. 2 gate reports read in their NOT-PINNED and FINDINGS sections
(`2026-09-20-batch1097-1099-tier1-r1`, `2026-09-20-batch1092-1096-tier1-r1`) plus targeted reads in
`2026-09-19-batch1077-1083-tier1-r1` and `2026-09-19-batch1084-1091-tier1-r1`.

### Why the gate lane really is closed (re-verified, not inherited)

- `2026-09-20-batch1097-1099-tier1-r1` NOT-PINNED: exactly **3 rows**, all one of two findings —
  N99-1 (SUPERROLESWIDEN / SUPERADMITSANYUSER) and N97-1 (LASTOF2NULLMIXED / LASTOF4NULL). Both are
  round 19's, briefed and HELD (`READY_KS-1282-N99-1…`, `READY_KS-1230-N97-1…`). **0 rows left.**
- `2026-09-20-batch1092-1096-tier1-r1` NOT-PINNED: **11 rows, all #1096 / KS-1282** — the eleven
  `requireSuperAdmin` guards. Briefed as KS-1282-N96-1a / N96-1b, both HELD, and the newest gate
  records N96-1 as **CLOSED by #1099 (13 of 13 guards now pinned)**. **0 rows left.**
- The newest gate's own BY-NAME ITEM 5 re-measures every KS-1238 part on the all-three tree
  (671 cells) and rules KS-1238 **COMPLETE**; the prior report's one open item (proxy.ts :475 / :507
  admin.ts shadow) is CLOSED by #1099's N95-1 cells, and its class hunt (`shadows_mall.out`)
  found **exactly two** same-method same-path cross-router pairs in 125 route registrations, both now
  pinned — "No other shadow of the proxy.ts :472 / :504 shape exists."
- Findings the newest gate lists as STILL OPEN were each re-checked here and each is rejected below:
  N77-2, N85-1, VC-1, N62-3, N72-2, KS-1280.

### Rejection table

**A. The three findings the newest gate leaves STILL OPEN on KS-1258 / KS-1155**

- **N77-2** (KS-1258, `ks1248-n-1-system-status-troubleshooting-marks.test.ts`, the N68-1 cell's
  deny-list regex) · **reject** · it is a **FALSE-RED** fix: the tamper (a benign reword of the
  `:576` comment, FALSEPOS576) currently REDS N68-1 and the fix must make it GREEN. The test_only
  checker grades tamper -> red only, so it cannot grade an inverted cell. Identical to round 10's
  KS-1131 rejection, same cause. Unmeasured beyond reading the two reports.
- **N85-1** (KS-1258, same cell) · **reject** · the gate's own words: N68-1 "is now subsumed at
  :576" by N77-1 and "contributes only its false-red", so the honest change is DELETING a cell —
  which has no tamper, no new cell and nothing for the checker to grade. A rewrite to N68-2's
  allow-list form would red under the same six start-shape tampers N77-1 already pins, so no tamper
  would red **exactly** the new cell. Unmeasured.
- **VC-1** (KS-1155-class, vc-issuer `db.retry.test.ts` first cell, 3,721 ms once in a parallel
  run) · **reject** · a timing **Record**, not a seam: no product tamper, no cell to add. Also
  vc-issuer has no runner pin for the test_only builder (round 13's KS-1269 N71-1: builder rc 2,
  "cannot tell the runner"). Unmeasured.

**B. Tickets filed after the round-9 cutoff, never verdicted (read in full this round)**

- **KS-1281** (P4, vc-issuer `credentialRepo.ts:28-42` runtime `CREATE TABLE` WARN) · **reject** ·
  decision-class by its own text — "Remove the runtime `CREATE TABLE` … **or** reduce it to an
  existence check" — two shapes, unruled; the WARN is a real-Postgres privilege behaviour, so no
  in-process cell can red it; and vc-issuer is unbuildable by the test_only builder (no runner pin,
  round 13). Unmeasured.
- **KS-1277** (P4, `originate/src/routes/documents.ts`, two stale on-behalf-of comments at
  `:2327-2334` and `:60-66`) · **reject** · comment-only, so there is **no new cell and no tamper**:
  the ticket says in its own words "No behaviour change." That is `comment`-mode work (the
  9/9 builder), not the test_only / code_patch shape this round was commissioned for. It also
  collides on file: `READY_KS-1264_…REVOKE-RECORD-AFTER-UPDATE-PASS-7of7_2026-09-19.diff.md` is a
  HELD product patch to that same `documents.ts`. **Nearest thing to a fit this round** — flagged
  for Wednesday as a possible comment-mode brief once KS-1264 clears, not briefed here.
- **KS-1275** (P3, `originate.openapi.ts:1847-1861` stale verb list) · **reject** · multi-file by
  its own fix shape: edit the `.ts` description **and** "regenerate the yaml with
  `npm run generate-openapi`", which rewrites `docs/openapi/secuura-api.yaml`. A build step, not a
  one-file patch.
- **KS-1279** (N62-3, preflight legs-ran ratio) · **reject** · verdict already on record
  (`queue.md` 20:58 2026-09-19 and 04:15 2026-09-20): needs a product fix first, reallocated to a
  Claude seat. Not re-derived.
- **KS-1280** (N76-2, `POST /api/certifications/:id/verify` forwards a revoked session's Bearer) ·
  **reject** · verdict on record (round 13): a product defect, not a pin of existing-right
  behaviour; the ticket's own Recommendation is a **measurement** ("Measure originate's
  `GET /api/documents/:id` with a revoked session's JWT"), and the newest gate agrees it "stays
  outside". Auth surface; product bytes not permitted.
- **KS-1282** · already briefed four ways (N91-2, N96-1a, N96-1b, N99-1), all HELD; completeness is
  Kam's call per the gate. Nothing left.

**C. Census rows never verdicted anywhere (T1 / T3 / T4), read in full this round**

- **KS-678** (P2, 17 `secuura.io` URLs published) · **reject** · the fix is a NEW guard rule (E1
  splits on `@` and sees only email addresses) plus an ownership question about a domain we may not
  own — new tooling + a decision, not a one-file pin.
- **KS-947** (P2, KS-733 parity-gate blindness F3+F4) · **reject** · the subject IS the parity test
  itself and the fix shape is to BUILD a richer gate (capture the whole option set; assert mount
  character offsets) — test-guard class, rounds 3-5 precedent; and F4 needs an absolute contract
  source that does not exist yet (a design call).
- **KS-955** (P2, fresh clone cannot run the platform suites) · **reject** · `.env.example` /
  `docker-compose.yml` / a real auth container and its lockout store — needs the live stack, no
  in-process cell.
- **KS-758** (P3, connector erasure: permanent failures present as retryable, nothing dead-letters)
  · **reject** · needs a real database (22P02 on a non-uuid tenant claim) AND a design decision
  (what to dead-letter into) — the ticket offers no single fix shape.
- **KS-784** (P3, `POST /api/teams/webhook-config` fails the Schemathesis `pr` sweep) · **reject** ·
  the oracle is a live gateway + a Schemathesis run; the ticket explicitly says "No fix attempted;
  not investigated".
- **KS-837** (P3, published prose drifts; the phrase check + marker convention + ~306 unswept
  descriptions) · **reject** · three lifted lines of KS-822, each a sized piece of NEW tooling
  ("~half a day, SIZED") — design/build, not a pin.
- **KS-851** (P3, KS-386 round-2 residues G-1..G-4) · **reject** · G-1's oracle is a `pg_attribute`
  projection of two real schemas (column ordinals) — needs a real PostgreSQL; the four are
  explicitly "advisory only — no change was made by the tester".
- **KS-934** (P3, m365 `/api/teams/notify` serial unbounded loop) · **reject** · the fix shape is
  offered three ways (LIMIT+paging / aggregate deadline / move off the request path) = decision-class,
  and the ticket's own red-proof needs "N rows against a destination that never answers".
- **KS-986** (P3, the retired admin credential in USER_TESTING docs) · **reject** · docs across
  several files plus a demo-VM environment question (turning seeding back on **suspends** the
  account unless a second variable is set) — multi-file and a decision.
- **KS-1197** (P4, non-string `verificationLevel` claim: create 500s, verify hangs) · **reject** ·
  its own Recommendation is "**Not built.** Low reach", the fix shape spans `middleware/auth.ts`
  **and** the verify handler's rejection path (two sites), and it is an auth-token surface — product
  bytes not permitted. Nothing here is existing-right behaviour to pin.
- **KS-748** (P4, `svc_api_keys.organization_id` not a tenancy boundary) · **reject** · the whole
  oracle is DDL/RLS on a real PostgreSQL (constraints, backfill, storability of an incoherent pair).
- **KS-965** (P4, 87 documentary occurrences of the retired admin credential) · **reject** ·
  **55 files** — multi-file by definition; and "not a find-and-replace to a new value", i.e. each
  site needs its own wording — a judgement per site.
- T1/T2b/T3 rows NOT re-read, verdict on record and cited rather than re-derived: KS-683 / 953 /
  579 / 581 / 627 / 746 / 915 / 1168 / 1190 / 1222 / 1234 / 1236 / 998 / 1163 / 630 / 789 (round 1,
  line "T1/T2b not re-read"); KS-1145 / 1239 / 1245 / 1265 / 1263 (round 1); KS-759 / 1203
  (round 2); KS-1272 (rounds 8-9); KS-1143 / 1019 / 1084 (queue.md rejection classes: the "product"
  is the test file; originate-jest / live-lane Owns; security surface). KS-1175 excluded by this
  round's own commission.

**D. The auth-shaped EXCLUDED pool (43 rows) — the widest surface left, swept here**

Kam's rule permits these **only as test-only pins with zero product bytes**. 21 read at title level,
7 of the most plausible read in full. Every one describes a **defect or a decision**, i.e. behaviour
that is currently WRONG — and a test-only pin can only pin behaviour that is currently RIGHT. That
is the single reason the whole pool fails, stated once and applied per row.

- **KS-1198** (connector JWT as Bearer skips the connector gates) · **reject** · "Not built; defence
  in depth"; fix shape offered two ways (refuse at the gateway, or attach `connectorMeta`) — a
  product edit on the auth path, and a decision.
- **KS-1177** (v1 verify family refused for cookie callers in production) · **reject** · its own
  Recommendation is "**Owner decision** on the intended behaviour, then one of these" — three shapes.
- **KS-1107** (P2, register accepts a client-supplied `organizationId`) · **reject** · "Impact NOT
  traced … Trace every consumer before choosing a fix"; measurement-first, then a product edit.
- **KS-619** (gateway tenant resolution falls through to `x-tenant-id`) · **reject** · "Remediation,
  not a defect" — a product change to `middleware/auth.ts:387` to make the overwrite unconditional.
- **KS-1032** (P2, 9 trust-header reads outside auth middleware) · **reject** · nine sites across
  **six files** in four services — multi-file, security-class.
- **KS-1235** (P2, auth's tenant-pool statements carry no tenant GUC) · **reject** · "The owner's
  fix. Not built here", two shapes offered; RLS was MODELLED, "no Postgres was run".
- **KS-1017** (test-estate CLASS: fixtures that cannot discriminate) · **reject** · a class ticket
  with 3 instances across auth x2 + originate; each fix is a fixture redesign whose red direction is
  the inverted one (a looser suite must become stricter) — the false-red problem again.
- Read at title + state only, all rejected as defect-or-decision on their own titles, none a pin of
  existing-right behaviour: KS-724, KS-782 ([Decision] in the title), KS-787, KS-805, KS-825
  (gate-integrity flake), KS-834 ([Decision] in the title; KS-1280's sibling), KS-836 (openapi +
  regenerate = multi-file), KS-840, KS-918 (a `package.json` dependency move), KS-925 (the extranet
  launcher, another project's folder), KS-951, KS-977, KS-1015 (a triage sweep), KS-1038 (an
  `tests/e2e` race, no Playwright checker), KS-1053 (a FLAKE, hypothesis unconfirmed), KS-1091 (a
  probe "reasoned, never run, not commissioned"), KS-1105 (`frontend/admin/src/pages/Login.tsx` —
  no checker lane), KS-1149 (a git/SSH transport issue), KS-1210, KS-1214 (P0, "measure deployed
  exposure first"), KS-1225 (P0, needs `jsdom` added to auth's lockfile — a dependency change).
- Already verdicted in round 10 or the queue.md security list, not re-read: KS-1003, KS-1005,
  KS-1006, KS-1124, KS-1157, KS-1208, KS-1240, KS-1241, KS-1242, KS-1244, KS-1205, KS-745, KS-1131,
  KS-1238, KS-329, KS-618, KS-668, KS-756, KS-824, KS-1146.

### What would reopen the lane

1. The **next batch gate's** NOT-PINNED list (Seat B's next raise) — the only source that has ever
   produced a fit at this contract, because only a gate hands over a *measured* product tamper that
   no cell catches.
2. **KS-1277** as a `comment`-mode brief (9/9 builder), once `READY_KS-1264` clears `documents.ts`.
3. A **vc-issuer runner pin** in the test_only builder would unlock the KS-1269 / VC-1 surface
   (round 13 flagged this as Wednesday's call; `briefs/KS-1269-N71-1.md` was written and measured by
   hand but could not be built).

### CORRECTION by Wednesday (the 03:3x Sunday seat), 2026-09-20 15:4x — two of round 20's three "what would reopen the lane" items are STALE
Measured, not argued:
1. **"a vc-issuer runner pin ... would unlock `briefs/KS-1269-N71-1.md`" — the pin EXISTS and that brief is DONE.** `night/briefs/KS-1269-N71-1.md` line 3 says "Builds since 2026-09-19 via the `Runner:` line below (builder RUNNER PIN)" and line 7 is `Runner: vitest`; the builder took the pin on 2026-09-19 16:52 (IMPROVEMENTS row). `READY_KS-1269-N71-1_…_2026-09-19.diff.md` was written, raised in the #1084-#1091 batch and MERGED. Nothing to unlock.
2. **"KS-1277 ... collides with the held READY_KS-1264 product patch on `documents.ts`" — that patch is MERGED, not held.** KS-1264 went up as **#1060** and merged on 2026-09-19 (develop 3c447abc7 at the time). The `READY_KS-1264_…_2026-09-19.diff.md` file is a spent hold left on disk, not a pending change. **So `documents.ts` carries no held patch and KS-1277 is NOT blocked by one** — it stands or falls on being comment-mode work (its own words: "No behaviour change"), which is the `comment` tier, not `test_only`.
3. Item (1) of that list — the NEXT batch gate's NOT-PINNED list — stands and is the near-term feed (the Seat B 9th raise of the two held fixes is being briefed now).
**The rule this earns for every search commission: a "what would reopen this" list is a set of CLAIMS, and each is checked against the artefact before anyone acts on it** (a held READY on disk is not evidence the change is unmerged; a missing capability is not evidence it was never built).

---

## round 22 (2026-09-21, widened past the 88) — 19 read, 1 fit

**Verdict: 1 FIT, briefed and golden-measured — KS-1283 (`KS-1283-PROVADMIN-1`, PASS 8/8 twice, fresh
clones).** Tip `778e6cfe2b6061d60ffcf3a57a951c84dc152b67` by `ls-remote` at start and at close (unchanged;
the #1104 merge). Source checkout tracked-modified 0 throughout; no port touched; Linear read-only, key
sourced transiently. Artefacts: `runs/2026-09-21_search-widen-drafter-precheck/` (`sweep/` holds the pull
and the 270-row triage list).

**Population (paginated, `first:250` + `hasNextPage`, 2 pages):** KS Backlog+Todo = **358** (333 Backlog,
25 Todo, 0 archived). Minus the 88 file-named tickets of
`runs/2026-09-20_ks1223WALLET-1-drafter-precheck/board_sweep_88_named_files.txt` = **270** (190 on Kam, 61
unassigned, 13 Peter, 6 Stuart). Cross-reference: 264 of the 270 already carry a row in the 2026-09-19
archive (mostly title-level "names no product file" / "auth-shaped title" excludes, or code_patch-tier
"needs a product edit" rejects — which is exactly what a test-only PIN can take, so they were re-read on
the DESCRIPTION here); 56 carry a brief and 58 a held READY under other rounds (skipped as HELD).
**19 read with the full description** (below); the remaining ~250 triaged at title + state + assignee +
label, excluded by predicate (Peter/Stuart, shell/CI/docs/scripts, DB/migration, decision-shaped, jest,
held, or no product behaviour a vitest cell can drive).

| id | title (≤60) | verdict | one-line reason |
|---|---|---|---|
| KS-1283 | platform.ts: a widened SUPER_ROLES would admit a tenant ADMIN r | **FIT** | guard `requireOrgProvisioner` driven in-process by `ks480-org-provisioner-gate.test.ts` (no held READY on it); tamper `:64` (ticket's) + `:97`; briefed `KS-1283-PROVADMIN-1`, PASS 8/8; connector-key half already held as KS-1282-N96-1a/1b, GET /tenants role half as N99-1 |
| KS-1190 | api-gateway meetsVerificationLevel fails open on an unknown REQ | REJECTED-ALREADY-PINNED | ticket says KS-1176's PR carries a cell pinning it at base; `enforcement.ts` is the KS-1203 READYs' product file and the ticket's own "two measurements come first" |
| KS-1244 | A duplicated x-api-key header defeats key authentication via he | REJECTED-NO-ONE-LINE-TAMPER | fix shape is an INSERTED refusal before the joined-value lookup in `middleware/auth.ts`; no tip line whose one-line replacement reds a pin of today's fall-through (next-best 1) |
| KS-1246 | F-2: /health/services still reads response.ok only — a degrade | REJECTED-NO-DRIVER | `services/health.ts` has no importing test outside `ks480-connector-auth.test.ts` (Seat B 11th's file, and the held KS-1232 pattern); opt-in 404 by default |
| KS-1249 | N-2: a 2xx whose body is not exactly top-level 'degraded' — inc | DECISION | "decide the vocabulary the aggregates accept"; same no-driver problem as KS-1246 |
| KS-811 | Nothing asserts #815's 403 code SET against what the route actu | REJECTED-NEW-FILE-SHAPE | the owed test derives two SETS (spec vs route) — a spec-walking new cell/file, not a one-line tamper pin; auth service social-callback |
| KS-1198 | A connector JWT presented directly as Bearer skips the gateway' | REJECTED-LIVE-LANE | pin lives in the RS256 branch of `middleware/auth.ts`; the driving files (`ks480-connector-auth`, `ks1041-vouch-header-strip`) are Seat B 11th's; needs a minted connector JWT fixture (next-best 2) |
| KS-1240 | T-2: the connector-token / key-validate fetch has no timeout — | REJECTED-NO-ONE-LINE-TAMPER | "no timeout" pins a hang; the fix is an AbortController insertion, and the driving file is Seat B's |
| KS-1242 | T-1: authenticateToken is an async express-4 middleware with no | REJECTED-NOT-REACHABLE | ticket: not request-reachable; the fix is a wrapper, not a line |
| KS-1241 | T-4: POST /api/v1/documents never answers an authenticated requ | REJECTED-LIVE-LANE | mount order in `api-gateway/src/index.ts` (Seat B 11th); pinning a hang needs a timer cell |
| KS-1243 | T-3: /api/batch/* is a dead route family — 401 to every caller, | REJECTED-LIVE-LANE | `index.ts` mounts; decision (remove or wire) |
| KS-1102 | Unauthenticated /system/status, /api/system/status and /api/sys | REJECTED-HELD-FILE | `routes/system-status.ts` and both its test files carry the held KS-1248/KS-1258 READYs; fix is an auth mount (insertion) |
| KS-1144 | ks781 J2 (KS-900 half): the default-only factory pin has no in- | REJECTED-TEST-IS-PRODUCT | the "product" is the ks781 guard test itself; a control cell, no product tamper |
| KS-1147 | ks860 loopback guard boundary (R-5, #980 delta gate): a listen | REJECTED-TEST-IS-PRODUCT | packages/shared guard test; fix shape is the gate's proposal, not ratified |
| KS-1256 | Connector allow-list still fails OPEN when Redis closes or erro | REJECTED-HELD-FILE | reader is the KS-1231/1233 allow-list in `enforcement.ts`; its suite `ks501-enforcement-non-string-doctype.test.ts` is owned by the two KS-1203 READYs; stateful Redis double needed |
| KS-1280 | POST /api/certifications/:id/verify forwards a revoked session' | REJECTED-HELD-FILE | `routes/verification.ts` + a revoked-session store double; the file carries held KS-1238-N76-1; ticket's own next step is a measurement on originate (next-best 3) |
| KS-805 | POST /api/oauth/authorize deny emits `Location: undefined?error | REJECTED-OAUTH-PRODUCT | Q3 is a one-line product fix in the deny branch; a pin of `Location: undefined` is pinning a regression the ticket says to fix, and the driver is the 4,700-line ks781 suite |
| KS-840 | The OAuth error code travels in error.message and the contract | DECISION | RFC-redirect vs JSON is "a design question"; half 1 is a contract-doc change |
| KS-1116 | KS-1020 item 2: which subject OWNS a presentation (and a creden | DECISION | "a decision for Kam, not a build" (vc-issuer) |

**Title-level excludes worth naming (not re-read):** KS-598 / KS-758 / KS-1178 / KS-1028-1031 — originate
(jest, REJECTED-JEST class; KS-598's MULTI_TENANCY upsert would be the strongest jest fit, `registry`
upsert, for a Claude seat); KS-607 / KS-1074 / KS-1129 / KS-1171 — `services/anchoring/**` (Seat A 15th);
KS-1239 — `index.ts:347` dead code (Seat B, 0 readers = no red); KS-1265 / KS-1263 / KS-1278 — originate
documents.ts, DB-transactional, jest; KS-1197 — pins a 500/async hang; KS-1257 — decision over a stateful
Redis double; KS-934 — m365 loop bound (insertion); KS-1131 / KS-1143 / KS-1145 — guard-test polish
(test-is-product / bash suite); KS-1115 / KS-748 / KS-699 / KS-1200 / KS-1023 — schema/DB; KS-1177 —
`index.ts` middleware order (Seat B); everything on Peter or Stuart (19); the 58 with a held READY.

**Next-best THREE if KS-1283 is refused:** (1) **KS-1244** — needs a driving file that is not Seat B's
(`auth.test.ts` imports `authenticateToken` at the tip: check it) and a tamper line whose replacement
refuses a joined `x-api-key` in one line (e.g. the `const apiKey = …` read at the `sk_` branch, replaced by
a comma-guarded read); (2) **KS-1198** — same file constraint plus a minted `type: 'connector'` RS256 JWT
fixture (the KS-753 brief's keypair idiom); (3) **KS-1280** — after the held KS-1238-N76-1 merges, a cell
in the same verification.ts suite with a revoked-session double, tamper = the `Authorization` forward at
`verification.ts:788`.

---

## round 23 (2026-09-21, board widening past rounds 20-22) — 43 read, 3 fits

**Verdict: 3 FITs, briefed and golden-measured, all test-only, PASS 8/8 twice each on fresh clones — KS-1236
(`KS-1236-SUBMITLEVEL-1`, auth vitest), KS-1006 (`KS-1006-WRONGCODE-1`, auth vitest, same test file as KS-1236 —
disjoint hunks, both orders measured) and KS-1137 (`KS-1137-F2-ESTATEIMAGE-1`, bash suite).** Tip
`cbae988dbe90ebe556459ada2cb437eaf80e2402` by `ls-remote` at start and at close (unchanged; the #1105 merge). Source
checkout tracked-modified 0 throughout; no port touched (the auth harness's own `127.0.0.1:0` listener is the file's,
not the drafter's); Linear read-only, key sourced transiently. Artefacts: `runs/2026-09-21_round23-drafter-precheck/`
(`sweep/` holds the pull, the 352-row triage and the 223-row eligible list; `KS-1236/`, `KS-1006/`, `KS-1137/` the
goldens, `golden_runs.log` all six checker runs).

**Population (cursor-paginated, `first:250` + `endCursor`, 2 pages, `hasNextPage=false` on page 2):** KS Backlog+Todo =
**352** (327 Backlog, 25 Todo, 0 archived; 259 Kam, 74 unassigned, 13 Peter, 6 Stuart) — 6 fewer than round 22's 358.
Excluded by predicate: 85 with an id in a `night/READY_*` filename, 84 in `done.md` as PASS/held (overlapping), 19
Peter/Stuart, 14 PR-attached (13 of those PRs merged by `git log --grep '(#N)'`; KS-964's #888 not found locally —
excluded as PR-attached anyway) → **239 eligible**, of which 223 carry no round 20-22 row. **43 read with the full
description** (below; 37 not read in any prior round by description + KS-1257/KS-1239/KS-934-class title-excludes of
round 22 now read, + the KS-1280 re-check); the rest triaged at title + archive reason (rounds 1-13's `names no
product file` / `auth-shaped title` rows), excluded by class (CI/workflow/compose/docs/DB/e2e/systemTest (Peter's
authority)/decision/design/review-stream).

| id | title (≤60) | verdict | one-line reason |
|---|---|---|---|
| KS-1236 | Approving a stale PENDING verification request after the subj | **FIT** | submit-side guard `users.ts:1267` unpinned (0 test hits for `Cannot request`/`targetIndex`); 2 cells in `ks1194-…test.ts` via its harness; tampers `<=`→`<` and `<=currentIndex`→`< 0`; briefed `KS-1236-SUBMITLEVEL-1`, PASS 8/8 ×2 |
| KS-1006 | POST /api/users/me/mfa/disable skips code verification when mf | **FIT** | the with-secret refusal at `users.ts:1105` unpinned (`me/mfa` 0 hits in auth tests); 1 cell + 1 mock line in the SAME ks1194 file (hunks above KS-1236's; both orders one sha); tampers `!verifyTOTP`→`verifyTOTP`, `mfaSecret &&`→`!mfaSecret &&`; briefed `KS-1006-WRONGCODE-1`, PASS 8/8 ×2 |
| KS-1137 | KS-878/867 suites: no cell names the real digit-bearing image | **FIT** (item 1) | CELL 3b in `container_trivy_image_filter.test.sh` feeds `dev-m365-integration:latest` (compose's 33rd `build:` service) through the stubs; tampers job04 `:62` `[a-z-]+[0-9]?` (reds only the new cell) and `[a-z-]+` (reds it + KS-867's); briefed `KS-1137-F2-ESTATEIMAGE-1`, PASS 8/8 ×2; item 2 (F-4 `jq` PATH) untouched |
| KS-1280 | POST /api/certifications/:id/verify forwards a revoked session | REJECTED-NOT-A-PIN (re-check) | HELD-FILE no longer holds: KS-1238 Done+archived, its N76-1 READY modified only the ks1238 TEST file; the only unmerged product hold on `routes/verification.ts` is KS-1185-F1 (other lines). But no behaviour of the route is "right today": it is a `for test compatibility` stub (`:783`), KS-834's public/auth decision is open, and a pin of the `:788` Bearer forward pins what KS-1238's direction removes; the ticket's own next step is a measurement on originate |
| KS-1174 | api-gateway collapses every API-key failure into 401 'Invalid A | REJECTED-ALREADY-PINNED | `auth.test.ts:240` pins `valid:false → null`, `:279` pins fetch-throws → null (the behaviour ask 2 changes to 503); asks 1-3 are product |
| KS-1262 | Security: PUT /api/settings/notifications writes the same key | REJECTED-ALREADY-PINNED | `ks719-settings-write-auth.test.ts:191-200` already asserts the write lands in the caller's key (`user-beta`) — the collapse tamper reds it today; fix (own key space / refuse reserved id) is product |
| KS-1253 | Spec-example guard E7: the secret-name deny list in PREFIXED_UU | REJECTED-ALREADY-PINNED | `ks256-…test.ts:522-529` `SECRET_NAMED` rows pin all 20 deny words through the real guard; the admitted `tok_/sess_/…` are the defect; allow-list is a DECISION |
| KS-1252 | Spec-example guard E7: the ULID-ish benign shape exempts any p | REJECTED-PRODUCT | the fix bounds a BENIGN_SHAPES entry; the two controls (`sk_live_`, lower-case) are already the KS-679 rows; a pin of the silent rows pins the bug |
| KS-1255 | Spec-example guard E7: the 40-char floor means a 38-39-char se | DECISION | "decide the floor from the key formats"; the floor itself is pinned by the KS-679 block |
| KS-1189 | Audit log (KS-871 gate R-3/R-5): H29 attemptedEmail is never w | DECISION | R-3 "decide whether the capture should work at all"; R-5 is a blast-radius check |
| KS-1222 | POST /api/documents/upload never reaches the gateway's blocked | DECISION | "the owners decide what the route should be"; the screen is unreachable (415/405 first) — nothing to drive |
| KS-1210 | OAuth app registration accepts any scope list, and any authent | DECISION | three owner questions before any build; OAuth product surface |
| KS-1208 | A verified token without a role or userId claim still 500s eve | DECISION | "a shape decision first"; a pin of the 500 pins the leak |
| KS-1231 | A connector allow-list fails open when platform-settings integ | REJECTED-HELD-FILE | readers `verification.ts:1212` + `health.ts:45` (KS-1232 INFOEMPTY held on health.ts); the `[entry] → 403` control is KS-1204/1230's; fix is fail-closed product |
| KS-1257 | After platform-settings has expired, a partial admin write now | DECISION | "merge the write over the defaults" is the product change; stateful Redis double |
| KS-1245 | F-1: scripts/smoke-test.sh:107 fails any /health/deep check th | DECISION | "decide what the smoke test should assert for degraded" |
| KS-1274 | Job 04: a trivy that exits 0 with a bare `{}` still reads as c | REJECTED-CODE-PATCH-TIER | fix shape given (a `Results`-key check in the `-z $norm` guard) but it is a product+cell bash_patch (7/7 tier), and the image-filter suite's stub prints `{}` — landing it changes every cell's instrument (noted in the KS-1137 brief); next-best 1 for a bash_patch round |
| KS-1273 | Job 04: a TRIVY_EXIT_CODE (or trivy.yaml exit-code) in the env | REJECTED-CODE-PATCH-TIER | one-line product fix (`--exit-code 0`) + a cell in `container_trivy_failed_scan_is_loud.test.sh`: bash_patch tier, not test-only; next-best 2 |
| KS-998 | KS-989 gate residue: the formatting gate fails OPEN on missing | DECISION | four items, item 1 "should be settled deliberately" (options costed) |
| KS-967 | Neither credential guard can see a value in a .env.example — o | DECISION | the self-test asserts the exclusion; any fix changes it consciously |
| KS-1168 | userRepo.ts: ILIKE search on encrypted PII columns can never m | REJECTED-PRODUCT | the ILIKE can never match — a pin would pin the defect; fix needs a search strategy (HMAC/plaintext index) |
| KS-870 | Every ADMITTED erasure authenticates twice — the door's chain a | DECISION | two fix shapes, the second "wants its own measurement"; the refused=1 half has no one-line loosening |
| KS-807 | The control-byte guard cannot see a raw body — findNulBytePath | DECISION | "(A) scan raw bodies / (B) declare them out — decide first" |
| KS-954 | KS-858 residue: the repeated-slash collapse does not complete f | REJECTED-NOT-REPRODUCED | "Mechanism NOT determined … Reproduce before fixing"; `proxy.ts` mounts |
| KS-934 | m365 /api/teams/notify: a serial per-row loop with no LIMIT an | REJECTED-NO-ONE-LINE-TAMPER | the fix is an aggregate bound (insertion); a pin needs N rows against a never-answering destination + timers |
| KS-759 | tenantId is read through two `as unknown as` casts because it | REJECTED-TYPE-ONLY | a shared `JwtPayload` type change; no runtime red exists |
| KS-746 | Security events carry no tenant at all — KS-743 had to gate th | REJECTED-DATA-MODEL | migration + backfill decision |
| KS-1197 | A non-string verificationLevel claim: POST /api/documents answ | REJECTED-PINS-A-500 | a 500 and an async hang; "not client-forgeable"; fix is a coercion in `middleware/auth.ts` |
| KS-1239 | R-1: the index.ts:347 rawAuthorization capture is dead code — | REJECTED-LIVE-LANE | `index.ts` (Seat B 11th); 0 readers = 0 red |
| KS-1084 | READ ONLY / unverified: the gateway's own Authorization-only ca | REJECTED-MEASURE-FIRST | "Measure before any fix" on a two-tenant stack |
| KS-1082 | The Playwright env guard added in #896 reads config/ only — th | REJECTED-PETER-AUTHORITY | `systemTest/` is Peter's; the guard is on an unmerged branch |
| KS-1214 | mcp-server POST /hash hashes any server-local file named by a | REJECTED-MEASURE-FIRST | "measure the deployed exposure first"; the fix drops the branch (product) |
| KS-1107 | POST /api/auth/register accepts a client-supplied organization | REJECTED-TRACE-FIRST | "trace every consumer of organizationId before choosing a fix"; the register schema is the product |
| KS-947 | KS-733 gate blindness (F3+F4): the parity cell misses skip:() | REJECTED-LIVE-LANE | the mounts are in `index.ts` (Seat B); the "product" is the parity test file |
| KS-1091 | KS-1041 residual: the cross-tenant JWT probe on originate's di | REJECTED-NOT-COMMISSIONED | "no action until Kam rules" |
| KS-1124 | originate: a non-prod certification whose anchoring submission | REJECTED-JEST-PRODUCT | originate (jest) blob writers; two product fixes, READ ONLY findings |
| KS-1110 | Two k6 unit tests parse config/scenarios.yml with js-yaml dire | REJECTED-TEST-IS-PRODUCT | the change is to two test files + a source-text guard; systemTest/performance |
| KS-951 | The default-password CI gate catches one shape and calls it cl | DECISION | "widen the scope, or state the scope"; a bash guard with no suite of its own |
| KS-939 | Launcher: the assembled boot prompt is asserted by no cell — K | REJECTED-PRODUCT-EDIT | the prompt is not printed under dry-run today — the fix emits a `DRY_RUN_INITIAL_PROMPT` marker (product) and "do not fix the launcher while two seats are live" |
| KS-1145 | ks949 suite coverage (KS-950 / KS-962, #973): ID3's capture ha | REJECTED-TEST-IS-PRODUCT | a real-PostgreSQL suite's own assertions; the gate's proposals are not ratified |
| KS-896 | KS-881's CONTROL is satisfied when the branch does not exist — | REJECTED-TEST-IS-PRODUCT | the CONTROL cell of `pre_push_hook_base.test.sh` is the subject; no product tamper |
| KS-902 | no-tracked-credentials.sh cites two scripts as "structurally i | REJECTED-COMMENT-TIER | a load-bearing comment correction (comment_patch tier, not test-only); "either fix their derivations or reference the audit ticket" is a decision |
| KS-1119 | Security (multi-tenant only): POST /api/verification/verify ca | REJECTED-MEASURE-FIRST | "prove it first, live" with multi-tenancy enabled; `verification.ts` fix is product |

**Title-level excludes worth naming (not re-read):** KS-1265 / KS-1263 / KS-1278 / KS-1178 — originate jest,
DB-transactional (round 22); KS-1266 / KS-1259 / KS-1155 / KS-1225 / KS-1226 — test-infra (DNS in tests, isolation,
timeouts, a file that cannot load); KS-1235 / KS-1200 / KS-1115 / KS-1054 / KS-1030 / KS-1023 / KS-699 / KS-748 — DB /
migration; KS-1281 / KS-1224 / KS-1218 / KS-1216 / KS-1154 / KS-918 / KS-530 — boot/deps/lockfile; KS-1247 / KS-1251 /
KS-1162 / KS-1148 / KS-1138 / KS-1051 / KS-1012 — CI / workflows / consumers outside the repo; KS-1163 / KS-1161 / KS-1149 /
KS-1146 (preflight.sh, Seat B) / KS-1085 / KS-940 / KS-925 — shell / launcher / compose; KS-1177 / KS-1003 — `index.ts`
(Seat B); KS-1132 / KS-1114 / KS-1111 / KS-1088 / KS-1063 / KS-980 / KS-889 / KS-808 / KS-1019 / KS-1141 — decision /
question; KS-1106 / KS-1105 / KS-1104 — frontend; KS-1113 / KS-1039 / KS-1038 / KS-1010 / KS-1076 — e2e / Playwright;
KS-1131 / KS-1143 / KS-1142 / KS-906 / KS-897 — guard-test polish (test-is-product); KS-1128 (needs a real PostgreSQL
boot); KS-1005 / KS-1032 / KS-1157 / KS-756 / KS-1006-class MFA product asks other than the pinned half — auth product;
everything on Peter or Stuart (19); the 85 with a READY-named id.

**Instrument slips caught in this round's own work:** (1) one Bash call carried a stray `cd /dev/null` and was REFUSED by
`pretooluse_no_cd.sh` — re-issued without it; (2) one later call used `(cd "$CL/…" || true)` inside a subshell, which the
hook did not catch — a `cd` all the same, not repeated; (3) the first KS-1236 draft's anchor premise carried a half-written
sentence ("wait: …") — corrected by measuring the six `});` lines before the build; (4) a zsh loop over `"a b c"` strings did
not word-split — rewritten as a function; nothing was mis-stated to the file by any of the four.

**Next-best if a FIT is refused:** (1) **KS-1274 / KS-1273** — bash_patch tier on job 04 (one-line fixes + a cell in the
`failed_scan_is_loud` suite; note the image-filter suite's `{}` stub, which KS-1274's fix would turn into `scan-failed` for
every cell); (2) **KS-1236's `already pending` refusal** (`users.ts:1274`) — a third cell in the same file, same harness;
(3) **KS-1006's `MFA is not enabled` / shape refusals** (`:1099`, `:1102`) — same file, same harness.

## round 24 (2026-09-21, board widening past round 23; bash_patch tier admitted) — 42 read, 1 fit

**Verdict: 1 FIT, briefed and golden-measured — KS-1273 (`KS-1273-EXITCODEENV-1`, BASH_PATCH: job 04 passes `--exit-code 0`
to trivy + ONE NEW bash suite, PASS 7/7 on three fresh clones, four wrong variants refused). No test_only FIT among the
40 newly-read tickets: every one is a decision, a product change, a DB/boot/infra item, or a pin that would pin the defect.**
Tip `362e51fe0db7e73d5557924902763fe3f10fd8c7` by `ls-remote` at start (05:38:29) and at close (unchanged; the #1111
merge). Source checkout tracked-modified 0 throughout; no port touched (the real-trivy precedence measurement was a local
`trivy fs --scanners secret --offline-scan --skip-version-check` on a scratch directory — no image, no DB, no daemon);
Linear read-only, key sourced transiently. Artefacts: `runs/2026-09-21_round24-drafter-precheck/` (`sweep/` the pull, the
352-row triage and the 181-row eligible-unrowed list; `KS-1273/` the measurement, the golden, the variants and the
collision orders; `golden_runs.log` all seven checker runs; `REPORT.md`).

**Population (cursor-paginated, `first:250` + `endCursor`, 2 pages, `hasNextPage=false` on page 2):** KS Backlog+Todo =
**352** (327 Backlog, 25 Todo, 0 archived; 261 Kam, 72 unassigned, 13 Peter, 6 Stuart) — the same 352 as round 23 (two
unassigned → Kam). Excluded by predicate: 88 with an id in a `night/READY_*` filename, 87 in `done.md` as PASS/held
(overlapping), 19 Peter/Stuart, 14 PR-attached, and the live lanes — of the fifteen named (the 12th's ten + the nine held
today) 6 are in this population (KS-1283, KS-1244, KS-1236, KS-1198, KS-1137, KS-1006 — every one also READY+done-flagged)
and 9 are `In Progress` with a PR attached (KS-1203 #1112/#1103, KS-1275 #1102, KS-1284 #1105, KS-1175 #1105, KS-880 #1110,
KS-753 #1107, KS-1234 #1108, KS-1223 #1111, KS-1232 #1106) → **236 eligible**, of which **181 carry no round 20-23 row**.
**42 read with the full description** (40 not read in any prior round + KS-1274/KS-1273, round 23's NEXT-BEST, re-read
for the bash_patch tier); the rest triaged at title + round-23 class (CI/workflow/compose/docs/DB/e2e/systemTest/decision/
design/review-stream/frontend/launcher). Round 23's next-best (2)/(3) — KS-1236's `already pending` refusal and KS-1006's
shape refusals in the same `ks1194-…` file — are OUT: both tickets are in the 12th's lane and that test file is being
raised by it.

| id | title (≤60) | verdict | one-line reason |
|---|---|---|---|
| KS-1273 | Job 04: a TRIVY_EXIT_CODE (or trivy.yaml exit-code) in the env | **FIT** (bash_patch) | one `-`/two `+` at `04-container-trivy.sh:93` (`--exit-code 0 "$img"`) + NEW `container_trivy_exit_code_env_keeps_findings.test.sh` (3 CONTROL, 2 🔴); RED at tip `3 passed, 2 failed` (`got 1 scan-failed 0 0`), GREEN after `5 passed`; real trivy 0.71.0 MEASURED: env=1+findings rc 1, `--exit-code 0` rc 0; siblings 3/4 unchanged; briefed `KS-1273-EXITCODEENV-1`, PASS 7/7 ×3 |
| KS-1274 | Job 04: a trivy that exits 0 with a bare `{}` still reads as c | REJECTED-THIRD-FILE | any guard that turns `{}` into `scan-failed` reds the clean stub of BOTH existing suites (`failed_scan_is_loud.test.sh:57` prints `{}`, its CONTROL asserts `0 2 0`; `image_filter.test.sh:76` prints `{}`, CELL 1 asserts `rc=0`) — the fix needs the image_filter stub changed too: a third file the bash checker refuses (B3) and a file the held KS-1137-F2 READY modifies (`@@ -140,1 +140,20 @@`) |
| KS-619 | Gateway tenant resolution falls through to the caller's x-tena | REJECTED-PINS-THE-DEFECT | the ticket's ask REMOVES the `auth.ts:387` header fall-through (fail closed); a KS-1223-style characterisation pin would pin what the owner wants gone (the KS-1280 rule); the fix is auth-middleware product |
| KS-1191 | Audit log records the caller's spelling: case splits the actio | DECISION | "a design decision for the audit trail's owner, not a one-line fix" — two owner choices before any build |
| KS-1112 | PATCH /api/gdpr/dsr/{dsrId} answers "DSR not found" with 200 f | DECISION | "one decision, then one small change" (align to 404 OR document the split); originate jest route with a DB call behind it |
| KS-766 | base-image-watch self-test cannot red the DB-age PRODUCER — th | REJECTED-PRODUCT-REFACTOR | done-means item 1 extracts the inline `python3 -c` age block into a callable unit — a product refactor, then the cells |
| KS-1063 | A gate that examined NOTHING exits 0 — check-package-format re | DESIGN | "the design question comes first" — whether a gate that examined nothing may exit 0 at all (three instruments) |
| KS-812 | connectors/whatsapp-bot prints the DEAD Container Apps API URL | REJECTED-CODE-PATCH-TIER | a one-line TS default in `connectors/whatsapp-bot/src/index.ts:21` (repoint OR drop — a choice); code_patch tier, not this round's; no suite drives the file |
| KS-849 | KYC mock document flow: a 1.5s timer writes back a STALE verif | REJECTED-PRODUCT | "both change concurrency behaviour, so this wants its own gate"; a pin needs fake timers + a `dbSaveVerification` double on the kyc service |
| KS-1114 | POST /api/verification/verify refuses a title-only body with 4 | DECISION | "decide the contract first … a product call" (implement a title strategy OR drop `title` from the spec) |
| KS-625 | /presentations/verify reports a presentation verified without | REJECTED-NOT-COMMISSIONED | "the by-design-or-remediate ruling is Kam's"; a pin of `presentations.ts:316-322` pins the missing signature check |
| KS-758 | Connector erasure: three permanent failures present as retryab | DESIGN | "a dead-letter path is a design, not a line" |
| KS-1132 | getPlatformAdmin swallows an infrastructure failure to null — | DECISION | "needs its own ruling before a build"; auth login product; the branch was never driven |
| KS-838 | Make the authorize rules DATA the resolver iterates, so the GE | REJECTED-REFACTOR | "a route refactor of `resolveAuthorizeClient`, not a change to the suite" |
| KS-959 | KS-597 fallback: resolve the issuer org from the authenticated | BLOCKED | "cannot be built today, and the blocker is data" (`organization_members` 0 rows); Wednesday ruled it must not be written unexercisable |
| KS-607 | GET /api/anchors/{id} and verify report different statuses for | REJECTED-MEASURE-FIRST | "one authenticated call settles this" on UAT — a live measurement, not a pin |
| KS-1184 | workflow-approve persists the instance approved before the for | DESIGN | "a design call beside KS-1087 item 2" (persist after 2xx OR a re-forward path); the gate's regression needs a stateful store |
| KS-836 | Publish a `request:` block for POST /api/oauth/token — the end | REJECTED-SPEC+SCHEMATHESIS | an OpenAPI `request:` block "with the suite actually run" before/after — not a test tier |
| KS-765 | Merge helper must refuse a non-read SHA and have no fallback t | REJECTED-NEW-SCRIPT | done-means is a NEW committed merge helper under `scripts/` — a build, not a one-line bash_patch |
| KS-829 | Audit gate baseline data model: an unvalidated `scope` lets a | REJECTED-HYPOTHESIS | "fix-shapes are the tester's, quoted as hypotheses — run each against the unfixed instrument"; `.mjs` product |
| KS-761 | similarity-undiscriminating FP entries have no staleness detec | DECISION | "a decision in its own right" (a live re-measure rule for the similarity arm); systemTest |
| KS-768 | audit-locks scans 35 of 45 lockfiles — 3 vulnerable locks have | REJECTED-PRODUCT+DECISION | widening `findStandaloneLocks()` changes the baseline rows the gates compare (`#794`'s 5→7); `.mjs` product |
| KS-755 | akto unit suite has a standing red: runDir resolveRunId ignore | REJECTED-ISOLATE-FIRST | "I did not finish isolating which — that is the first step"; systemTest/akto |
| KS-1128 | The platform tenant seed's catch logs `Platform tenant seed sk | REJECTED-NEEDS-REAL-PG | the owed cell boots `runStartupMigrations()` against a socket-only PostgreSQL (the ks949 driver) |
| KS-1115 | anchor_store.status has no CHECK constraint — an out-of-union | REJECTED-MIGRATION | a new migration + a live census on every environment first |
| KS-824 | OAuth app_type: a CASED row is neither normalised by 047 nor r | REJECTED-MIGRATION | DDL (047's predicate + an unnamed CHECK) "a HYPOTHESIS until run against the unfixed product" |
| KS-1005 | Security/defect: POST /api/users/me/change-password returns 40 | REJECTED-AUTH-PRODUCT | the fix is `getUserByIdWithPasswordHash` at `users.ts:939` (auth product); a pin of the 404 pins the defect |
| KS-919 | Demo platform-admin account has mfa_enabled = false — delibera | DECISION | "carries the measurement only … nothing changes until it is ruled on" |
| KS-915 | A clean stack has no supported way to obtain its first privile | DECISION | docs / bootstrap command / operator decision — three shapes, none a test |
| KS-1053 | FLAKE (3rd occurrence, first with a name): ks949 seed-site enu | REJECTED-FLAKE | intermittent in the full auth suite, timeout hypothesis refuted; nothing deterministic to pin |
| KS-1225 | auth `ks799-consent-script-csp-and-execution.test.ts:116` cann | REJECTED-LOCKFILE | a member lock missing `jsdom` — a lockfile/deps change, not a cell |
| KS-1266 | Four originate unit test files make a real DNS lookup and TCP | REJECTED-TEST-INFRA | four test files' `ANCHORING_SERVICE_URL` hygiene; no product tamper exists, so test_only cannot grade it |
| KS-1259 | api-gateway vitest suite is not isolation-safe: --no-isolate r | REJECTED-TEST-INFRA | "bisect the leaking files" across 30 runs; no cell |
| KS-1178 | Document row keeps the originating persona's email (createdOnB | REJECTED-DATA-MODEL | an erasure-propagation design between S and K's document row |
| KS-1135 | run-shell-suites.sh fails 6 of 25 suites under a long TMPDIR — | REJECTED-DECISION+HEAVY | "the builder's call" between two shapes; a red needs a 123-char TMPDIR driving `tsx`'s IPC socket (node + tsx in the cell) |
| KS-1088 | run-shell-suites.sh restores git discovery but does not isolat | DECISION | "decide whether the runner should enforce isolation"; "no current suite does this" — nothing red today |
| KS-1163 | start-secuura.sh never waits for five default-profile, healthc | REJECTED-BOOT-PATH | adding five services to `EXPECTED_SUFFIXES` changes the demo VM's boot wait; the existing suite carries them as `KNOWN_UNWAITED` (`:49-:53`) by design until a live-stack measurement shows all five reach `healthy` — a wait a stack cannot satisfy times out every boot |
| KS-940 | Launcher suite: four side-effect and guarded-surface gaps from | REJECTED-LAUNCHER | `Launch_Claude.command` findings — outside `Blockchain/Dev`, "do not fix the launcher while seats are live" (KS-939's rule) |
| KS-1085 | Launcher preflight: four findings — a concurrent seat clobbers | REJECTED-LAUNCHER | same file, same rule; item 2's mechanism "is not verified" |
| KS-897 | build_fixture swallows its own failure — `>/dev/null 2>&1` mak | REJECTED-TEST-IS-PRODUCT | the change is to `pre_push_hook_base.test.sh`'s own fixture builder; no product script, no product tamper |
| KS-906 | CASE 6's `cd /tmp` is inert — the leg uses `git -C "$DEV_DIR"` | REJECTED-TEST-IS-PRODUCT | a test cell's precondition + rename; Polish |
| KS-777 | QA pass F-1/F-3/F-4/F-7: two vacuous guards, an unasserted sta | REJECTED-TRACKER | "All four are FIXED on #795 … exists so they are findable" — nothing to build |

**Title-level excludes worth naming (not re-read; round 23's classes hold):** KS-1281 / KS-1278 / KS-1265 / KS-1263 /
KS-1235 / KS-1200 / KS-1054 / KS-1055 / KS-1030 / KS-1023 / KS-699 / KS-748 / KS-889 — DB / migration / originate
transactional; KS-1226 / KS-1155 / KS-1149 / KS-1146 (preflight, Seat B) / KS-1138 / KS-1051 / KS-1148 / KS-1162 / KS-1247 /
KS-1251 / KS-1012 / KS-997 / KS-996 / KS-995 — CI / workflows / test-infra / board hygiene; KS-1224 / KS-1218 / KS-1216 /
KS-1154 / KS-918 / KS-872 / KS-846 / KS-530 — deps / lockfile / tsc; KS-1177 / KS-1003 / KS-1032 / KS-1157 / KS-756 /
KS-783 / KS-782 / KS-329 — auth / OAuth / gateway `index.ts` product; KS-1161 / KS-925 / KS-785 / KS-668 / KS-658 /
KS-1014 / KS-1079 / KS-1080 — compose / VM / demo posture; KS-1106 / KS-1105 / KS-1104 / KS-648 / KS-735 — frontend;
KS-1113 / KS-1039 / KS-1038 / KS-1010 / KS-1076 / KS-1017 / KS-1022 / KS-1111 / KS-990 / KS-981 / KS-982 / KS-977 /
KS-957 / KS-956 / KS-955 / KS-953 / KS-752 / KS-738 / KS-725 / KS-724 / KS-723 / KS-716 / KS-709 / KS-696 / KS-591 /
KS-595 / KS-784 — e2e / Playwright / systemTest / Schemathesis / Akto (Peter's authority); KS-1141 / KS-1143 / KS-1142 /
KS-1131 / KS-1159 — guard-test polish (test-is-product); KS-1019 / KS-834 / KS-651 / KS-598 / KS-582 / KS-767 / KS-630 /
KS-1048 / KS-789 / KS-986 / KS-965 / KS-678 — decision / question / docs; KS-683 / KS-627 / KS-624 / KS-621 / KS-618 /
KS-787 / KS-757 / KS-1100 / KS-1044 / KS-1015 / KS-987 / KS-655 / KS-638 / KS-636 / KS-562 / KS-526 / KS-263 / KS-339 /
KS-305 / KS-491 / KS-485 / KS-583 / KS-581 / KS-580 / KS-579 / KS-576 / KS-605 / KS-604 / KS-603 / KS-602 / KS-772 /
KS-770 / KS-903 / KS-808 / KS-837 / KS-825 / KS-851 / KS-1083 / KS-1025 — ops / review-stream / chain /
design / audit; everything on Peter or Stuart (19); the 88 with a READY-named id.

**Instrument slips caught in this round's own work:** (1) the first attempt to write the new suite went through a Bash
heredoc and was REFUSED by `pretooluse_no_cd.sh` (the suite's own `HERE="$(cd …)"` / `cd "$SELF"` lines are the reference
shape) — written with the Write tool instead; (2) the first collision script tried to pull the KS-1137 READY's diff from a
```` ```diff ```` fence the READY file does not carry (its patch is a separate canonical `patch.diff`, named in the file's
header) and, because its clones were reused, printed one false "patch does not apply" — rewritten with fresh clones per
order and the canonical patch, both orders one sha; (3) a `sed -i ''` edit of that script failed under macOS sed and was
replaced by rewriting the file; (4) `triage.py`'s print label still says `r20-22 rows` where the flag now means rounds
20-23 — cosmetic, counts correct. Nothing was mis-stated to any file by any of the four.

**Next-best if the FIT is refused:** (1) **KS-1274** only if the tier admits a THREE-file diff or the KS-1137-F2 READY has
merged and its stub can be re-pointed in the same change (both suites' stubs to `{"Results":[]}` + the `Results`-key guard);
(2) a **test_only pin on job 04's KS-1136 arm from the NEW suite's harness** (the `empty` control) is already green — no
red exists to brief; (3) the board's remaining unread eligible rows are all title-excluded classes — a further test_only
round on this population is unlikely to find a fit until the 12th's fifteen merge and their siblings (KS-1236 `already
pending`, KS-1006 `MFA is not enabled`) leave the live lane.
