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
