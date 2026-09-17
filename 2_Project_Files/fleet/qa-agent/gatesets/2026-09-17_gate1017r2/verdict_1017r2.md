=====MSG 2026-09-17T00:34:13.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 10748
QA agent -> Wednesday. TIER 1 ROUND 2 gate (round 2 of 2, the cap), PR #1017 (KS-1195) @ a067d4e3e80f0e31c1aecb278f06c4f6df4b1c66.
Session 10:19:09 -> 10:34 AEST 2026-09-17 (clocks from `date`). Findings-only: nothing fixed, merged, pushed, commented or filed. No container; 0 listeners left.
Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017r2-a067d4e3e-tier1-r2/report.md

## BLUF
VERDICT: GO WITH FINDINGS on `a067d4e3e` (delta over r1 `cbe29597d` and base `7e89318bc`) AND on the merged tree `35974a2ffce620fe37c956daf5fde1a2e4e7a738` (head merged with develop `fa887f382` = #1014's squash; = drafter's OID).

- F-1 CLOSED on the real app for every real producer.
  - Round 1's harness VERBATIM (sha fd4026582f12); my r1 column = round 1's rows (census 0 diffs, all stages identical).
  - Head: Y-first 200 Rem 1 (r1 429); Z 999 (r1 996); W-first 200 (r1 429); KS1 B 4,3,2 (per key). head = merged; base never limits.
- No Major or Blocker. L3/L4/L5/L7 unchanged (MEASURED).
- NEW, both Minor, TICKET (neither reachable by a real producer today):
  - N-1: the READY's "never the raw key, never equal to key_hash" is TRUE at head (MEASURED, planted controls), but pinned by no cell. G-BUCKET-HASH 0 reds (probe: stored form in 64/64 Redis keys); G-BUCKET-RAW-2 0 reds (raw key in 64); RAW-1 VOID (TS6133).
  - N-2: the JWT branch honours a signed `rateLimitBucket` claim. A JWT with the victim key's bucket drew the victim down: 3 -> JWT 2 -> victim 1. At r1 the JWT counted in its own bucket.
    - A signed `connectorId: api_key:<D>` does the same, even with the claim deleted (my G-CLAIM-IGNORED tamper).
    - READ: 0 producers of the claim; 0 non-test producers of a machine authMethod JWT. Needs the RS256 signing key.
- Under the cap: ships F-1 CLOSED + F-2 CLOSED; tickets N-1, N-2 and the round-1 residue (F-3, F-4, F-5, R-1, R-2, R-4) on tickets (i)-(iii).
- Lead-item rulings: item 3's claim = N-2 (ticket, not a PR blocker; fix-shape must also namespace the fallback). Item 5's HASH/RAW = N-1 (ticket, F-3 class; not a behaviour defect at head).

## Plain statements, items 1-10
1. F-1 CLOSED (above). Instrument identity asserted.
   - KS4: a JWT with userId connector:api-key no longer shares with keyless keys (99, 98; V-keyless-first 200 Rem 2).
   - fake-Redis = in-memory; merged = head.
2. A5 identity, 64 throwaway keys x shapes (in-memory and fake-Redis LABELLED substitute; head = merged):
   - (a) 64 distinct `ratelimit:api_key:<hex>` = expected.
   - (b) 0 equal the stored sha256(key).
   - (c) raw key 0 and stored form 0 in logs (every logger level, console, stdout/stderr), Redis keys, responses (incl. 429 bodies) and errors, beyond the plants.
   - Plants: R in a logger line, S as a Redis key, R in an upstream header; each found exactly once, every tree.
   - Pre-existing (base = head, Record): the raw key is forwarded upstream in `x-api-key` on every proxied request (253 base / 249 head).
   - The in-memory DEGRADED warn prints the bucket hash once per 30 s (Record).
   - Whitespace around the key shares its bucket; a case-different key has its own.
3. Fallback and claim.
   - READ: users.auth_method is VARCHAR(20) DEFAULT 'email' with NO CHECK, but no signer copies it into a JWT (login mint carries no authMethod; OAuth mint 'oauth'). The connector-token mint carries no authMethod/connectorId/rateLimit. rateLimitBucket appears only in auth.ts and rateLimitEnforce.ts.
   - MEASURED at head, still shared across tenants: JWT api_key with a shared connectorId; userId connector:api-key; oauth_app with a shared connectorId; test tokens.
   - Independent: distinct userIds. Not limited: the minted connector-JWT shape.
   - Ruling: F-1 CLOSED for every real producer; the fallback literal is a Record (STILL OPEN, unreachable) for ticket (i). Claim = N-2.
4. Round-1 items, head vs r1, all diffs explained.
   - Census 326 rows / 175 fire, all [1,0,0]; head vs r1 0 row diffs (drafter predicted 2, R-5 order-dependent); merged vs head 2 (R-5).
   - D 999 on 175/175.
   - G-ERASE: 8 rows / 7 chains at 998; erasure [201,429,429,429]; suite 2 reds (R3 + F-2).
   - Non-machine principals: 0 header rows. A1/A2/A4/plant/principals identical.
   - A3 (substitute): the 2,678 vs round-1 2,463 calls and R-2's 197 vs 181 are EXPLAINED: round 1's fake-Redis run omitted the principals and a4 stages.
   - Round 1's redisthrow is VACUOUS at head (0 throws). Re-keyed: 4 throws, [200,200,429,429], redis-command-failed x1.
   - Round 1's order stage: B now 201 (A5). Re-shaped with a stubbed clock (F-5 STILL OPEN):
     - refused at +61 s costs validate 1;
     - at +481 s costs validate + exchange;
     - every refused POST still writes an audit row.
5. Tampers (seat forms byte-identical by AST; whole suite 53/436, pending 0; tsc per row; sha restore):
   - Seat rows: T0 0 · TA 8 · G-ERASE 2 · TW 6 · TT 1 · G-BUCKET 3 · TI 0 (exactly).
   - G-BUCKET-HASH 0 (N-1) · G-BUCKET-CONNECTOR exactly 1 (b) · RAW-1 VOID · RAW-2 0 (N-1).
   - Mine: G-CLAIM-IGNORED 0 (N-2) · G-BUCKET-TENANT 3 (R3, b, F-2) · G-BUCKET-CONST 7. T0 after 0.
6. Merged `35974a2ff` over develop `fa887f382` (unmoved start/mid/close 10:33:10).
   - Suites: base 52/424, r1 53/432, head 53/436, merged 54/454, pending 0, tsc 0; shared 44/851.
   - Including tsc: 31 lines / 11 files on all four; NEW 0; plant +1.
   - eslint NEW 0 (control fires).
7. Linear (10:28:19 and pre-mail 10:33:08): attachmentsForURL(pull/1017) = exactly KS-1195, In Progress, contributes.
   - Controls: 1014 -> KS-1176; 99999 -> 0.
   - Closing phrases 0 (controls 1/1/0); KS-1187 0 (control 1).
   - `## Round 2` x1; placeholders 0.
   - KS-1195 stays In Progress on merge (5f).
8. Deploy precondition: PR body 3 lines, 1 names F-1.
   - KS-1195 comment 6e25f648 does NOT name F-1 (predates round 2; no newer comment).
   - Record + escalation candidate: the facts comment is owed by the seat's successor. Not a PR finding.
9. Carry-forward: table below. Tickets (i)-(iii) are not filed (successor's).
10. Schemathesis/Akto: NOT APPLICABLE.
   - The delta touches 3 files; the spec blobs `122d3a2f8` (docs/openapi/secuura-api.yaml) and `029e4a581` are unchanged on base/head/merged.
   - The delta changes only which bucket a documented 429 draws from.
   - Real-browser half of tier 1: NOT APPLICABLE (no rendered surface).
   - Checkout bounds identical start/mid/close; pull/1017/head unmoved.

## CLOSED / STILL OPEN / NEW
- F-1 CLOSED (SHIPS-WITH). Residue: fallback literal for JWT/test-token machine principals is STILL OPEN, unreachable, Record -> TICKET (i).
- F-2 CLOSED (SHIPS-WITH): real-chain cell red under G-ERASE; pinned on 1 of 7 chains.
- F-3 STILL OPEN, TICKET (i) (not re-run; delta adds no cell). Extended by N-1.
- F-4 STILL OPEN, TICKET (i), Record.
- F-5 STILL OPEN, TICKET (i), Record (re-measured, new shape).
- R-1 STILL OPEN, TICKET (ii).
- R-2 STILL OPEN, TICKET (i) (197 on r1 = head = merged; 181 explained).
- R-3 Record. R-4 STILL OPEN, TICKET (iii). R-5 Record (instrument).
- N-1 NEW, Minor, TICKET (i). N-2 NEW, Minor, TICKET (i).
- Records: Rec-A raw key forwarded upstream (base = head); Rec-B DEGRADED warn prints the bucket hash; Rec-C 6e25f648 lacks F-1 (escalation); Rec-D round-1 redisthrow vacuous / order re-shaped.

## Prediction slips
- Drafter: head vs r1 census 2 diffs -> 0 (R-5). The unexplained R-2 16-line gap -> explained. KS-1176 "status merged" -> In Progress. Everything else as predicted.
- Seat READY: identity words true but unpinned (N-1). Claim honouring not mentioned (N-2). Shared suite not re-run per row by me.
- Round-1 gate (self-correction): its fake-Redis figures (2,463 calls; R-2 181) came from a run omitting principals and a4, and the report did not state that stage list.
- Mine: G-BUCKET-TENANT predicted 1 -> 3 (the ks1195 R3/F-2 keys share a tenant). Audit-status parse gap in my F-5 probe. My r1 claim/variant rows are confounded by F-1 state.

## MERGE ADDENDUM
squash `a067d4e3e` onto develop `fa887f382` (then-current at close; fa887f382 = #1014's squash) (merged tree `35974a2ffce620fe37c956daf5fde1a2e4e7a738`; drafter 35974a2ff; file-disjoint from #1014's squash by content); #1017 attaches to KS-1195 only, linkKind `contributes` (as read at 10:33:08 AEST, pre-mail) — KS-1195 stays In Progress on merge (§5f: a live sweep is owed); the deploy precondition stands: F-1 CLOSED by the per-key bucket, and real keys' configured allowances and real connector traffic rates are UNMEASURED and must be measured before any deploy (PR body Round 2 section + KS-1195 comment `6e25f648`, which does not yet name F-1); KS-1187 not named; equality targets after the squash: `auth.ts` blob `7c985bdce` / `rateLimitEnforce.ts` `90bd29378` / `index.ts` `db127dbfa` / ks1195 test `4b1fc017d` / ks781 test `bc4815c4e`; api-gateway 52/424 at `7e89318bc` -> 53/436 at head -> 54/454 merged (re-measured; drafter 54/454); packages/shared 44/851 at head; dispositions: F-1 CLOSED (SHIPS-WITH; fallback-literal residue Record, TICKET (i)), F-2 CLOSED (SHIPS-WITH), F-3 STILL OPEN (TICKET (i)), F-4 STILL OPEN (TICKET (i)), F-5 STILL OPEN, re-measured (TICKET (i)), R-1 STILL OPEN (TICKET (ii)), R-2 STILL OPEN (TICKET (i)), R-3 Record, R-4 STILL OPEN (TICKET (iii)), R-5 Record (instrument); NEW: N-1 Minor — A5 identity pinned by no cell (TICKET (i)), N-2 Minor — JWT `rateLimitBucket` / `connectorId` claim reaches the `api_key:` bucket namespace (TICKET (i)); Records: Rec-A raw key forwarded upstream in x-api-key (base = head), Rec-B DEGRADED warn prints the bucket hash, Rec-C comment 6e25f648 does not name F-1 (escalation), Rec-D round-1 redisthrow VACUOUS at head / order stage re-shaped.

## NOT TESTED (equal prominence)
1. Real keys' configured allowances.
2. Real connector traffic rates / Platform S keys.
3. Count of real keys without connector_id.
4. Real Redis and the real redis.ts client (LABELLED substitute only).
5. Multi-replica counting.
6. The deployed gateway (NODE_ENV=production, UNHANDLED_REJECTION_MODE=exit).
7. Real JWT signers at runtime (READ only; N-2's reach rests on it).
8. Security validate / originate mint at runtime (READ only).
9. systemTest/schemathesis, akto, playwright, performance, k6: NOT COMMISSIONED.
10. Preflight legs 3/4/8.
11. Auth/security/originate suites.
12. Absolute-form targets (held).
13. A real browser (N/A).
14. Handler reach on gateway-answered routes.
15. Round 1's G-OAUTH/G-UNKOPT/G-JWTCATCH, perip, pins-over-base: not re-run.
16. packages/shared per tamper row.
17. Originate INTEGER rounding (R-1).
18. The audit status field under the re-shaped F-5 stage.
19. Whether two keys of one connector SHOULD share (a product decision; measured per key).

docker info rc:

0
