# Stuart's list, 19 Oct: triage

Read-only triage helper (claude-opus-5-5) for Wednesday. Secuura only. Written 2026-10-19 ~16:1x AEDT.
Input: `KAM_MESSAGE_1550.md` (Kam 15:50:40 forwarding Stuart 12:11 + 12:12), and Stuart's Linear document `da3f1fbb5ccf` ("S↔K Anchoring Review", last updated by Stuart 2026-10-19T01:09:38Z; its "Kamil's list, refreshed 19 Oct 01:10 UTC" is the same nine items as the message).

**Instruments used.** Linear API, read-only (issue + paginated comments + attachments + relations, saved under the session scratchpad `lin/*.json`). `decision_queue.sh list` / `show` (all 820 cards searched). `git ls-remote` on the Blockchain repo, plus a `clone --shared` in the session scratchpad and a fetch of develop and PR heads into that scratch clone only. File reads of NEXT-PICKUP.md, DEPLOY-BLOCKERS.md and EXPIRING-GRANTS.md. Comment authors: "K" means a Platform K agent posting under Kam's Linear account (`kamil.kreiser@secuura.ai`); "S" means `stuart.jamieson@secuura.ai`.

**Live state when I wrote this:** develop = `7e2f8157cec2` (ls-remote at 16:03 AEDT). That is **#1607 (KS-1385 (b)), merged 16:02:10 AEDT**, and its tree is `5adb4e513696`, which equals gate U1's landing tree (my scratch fetch, `rev-parse develop^{tree}`). #1597 is still open at `8ec96bbac643` (ls-remote).

---

## BLUF

Stuart's list breaks into 26 dispositions:

- **(A) 14: agent-actionable now.** These are 8 builds and 6 ticket replies or read-only censuses. None of them is a deploy.
- **(B) 5: cards for Kam.**
  1. KS-1402: who creates the holder.
  2. KS-1384: schedule the per-event anchor project.
  3. KS-1580: build the code for a key revoked by erasure, or not.
  4. The KS-1570 deploy round: has Kam seen it, and may it go once Stuart's dev-ps deploy lands.
  5. KS-1575 + KS-1596 (+ rowHash): the new signing verbs.
- **(C) 5: already done or moving today.** #1568, #1607, #1597, the KS-695 (ii) / KS-1570 merges, and PS-1299 (S-side, nothing owed by K).
- **(D) 2: blocked.** The KS-1402 demo-pk deploy and the whole Kintsugi deploy round.

**Two of Kam's rulings were never delivered, and Stuart is right to call those tickets unanswered.** That is our miss, not his.

- **KS-1195:** Kam ruled **(a) 3,000/h for S connector keys, env-tunable, new keys only** on 9 Oct 10:06 (card `secuura-ks1195-s-key-ceiling-1009`). The card has no `delivered_artefact`. The last K comment on the ticket is 2026-09-17 (`21522e2b`). The build is absent too: `rateLimit` occurs 0 times in `services/api-gateway/src/routes/platform.ts` at `7e2f8157` (git grep), so S keys still take `services/security/src/index.ts:666` `.default(1000)`.
- **KS-1384:** Kam ruled **(a) one anchor per lifecycle event**, also 9 Oct 10:06 (card `secuura-ks1384-anchor-per-event-1009`). No delivery, and no K comment carries it. Stuart's own doc still says "KS-1384 unruled" in its 16 Oct entry.

**Stuart's premise is out of date on KS-1612.** He says round 3 is at its last gate. In fact:
- Round 3 was NO GO, and Kam ruled a fourth round at 11:08 AEDT (card `secuura-ks1612-round3-nogo-1019`). That was before his 12:11 message.
- **#1568 merged as `04a4a3393` at 13:46 AEDT** (Linear attachment `mergedAt 2026-10-19T02:46:13Z`; develop log; K comment `9fa073a2`).
- **#1607 (KS-1385 (b), holder update keeps issuer fields) merged at 16:02 as `7e2f8157`.**

**A new deploy precondition nobody has written down.** On develop, a Platform S custody transfer answers **500**; on Kintsugi it answers 404 (S measurements: KS-1402 `e7e7f826` 14 Oct, `2b0d2f7e` 15 Oct). The next Kintsugi round would therefore regress S from 404 to 500. Fixing the 500 should be a DEPLOY-BLOCKERS row. Also, DEPLOY-BLOCKERS.md:39 still says "#1568 not yet merged". It merged, and it carries **both** 050 and 051, each with its own apply-time census.

---

## The table

| # | Item | Ticket state / assignee | Last comment (date, author) | Linked PRs (Linear) / on develop (git) | What Stuart asks | Disposition |
|---|---|---|---|---|---|---|
| 1 | **KS-1402** custody transfers | In Progress, High / kamil.kreiser | 2026-10-15T06:32 S (`2b0d2f7e`); **last K reply 2026-10-12T07:18 (`eb8f6c8e`)**, so S's 14 and 15 Oct comments have no answer | #1374 merged 10-04 (`2d85b84e1`); #1437 merged 10-09 (`613070f29`); both on develop (git log `--grep KS-1402`). No commit after 14 Oct touches the 500 (same grep: 0) | (i) fix the develop 500; (ii) rule on the holder stub; (iii) deploy demo-pk with `PII_LOOKUP_HMAC_KEY` | **(i) A, build, M.** Reproduce the 500 in `services/originate/src/routes/documents.ts` (route at `:1586`, catch per Stuart `:2002-2003` at `8cbadd8d4`); cause unmeasured. Needed before ANY Kintsugi round (see BLUF). **(ii) B, card B1.** Not ruled: no card mentions stub or holder (searched all 820). Kam's 10-06 (a) was the lookup only. The 10-12 daily note:64 planned "the holder-stub ruling … remain[s] cards for Kam", and none was posted. **(iii) D**, see row 6. A demo deploy at Kintsugi's `65d7722f8` would carry #1437 without the erasure, but it only moves uat-ps from 403 to 404 while the stub is unruled. Not worth a card on its own. |
| 2a | **KS-1195** key ceiling | In Progress, High / kamil.kreiser | 2026-10-18T11:42 S (`4a274576`, fifth measurement: tripped 29 min into one run); last K 2026-09-17 | #1017 merged (`d7e95cd9f`); #1463 KS-1205 merged. Kam's 10-09 (a) is **not built**: `platform.ts` has 0 `rateLimit`; the security default is `1000` at `index.ts:666` and `3600` at `:667` | Rule a requestable limit or a dev default near 2,000/h | **A, build S + ticket reply.** Already ruled (a) 3,000/h on 9 Oct, which exceeds his 2,000. Build: register-connector passes `rateLimit` from env, default 3000, new keys only; tier-1 gate. Reply: post Kam's ruling verbatim now, with a "build in progress" note and no date. **Flag:** existing S keys on Kintsugi and demo stay at 1,000 until rotated, and rotating live client keys is Kam's (stated in the card's own option text). Local S slots mint fresh keys, so S's suite benefits as soon as K develop has it. |
| 2b | **PS-1299** | Backlog / peter@obeden.com, 0 comments, filed by S 10-18 | none | n/a (S-side) | S's own mitigation (run k-live first) | **C (S-side, nothing for K).** Made moot once 2a lands. |
| 3 | **KS-1634** simulated hash-only anchors unlabelled | In Progress, High / unassigned | 2026-10-19T01:30 K (`66b8981b`: third site in v2 found by gate O1; link changed to Refs) | #1597 OPEN at `8ec96bbac643` (ls-remote 16:03). Its diff = `verification.ts` `:712` and `:1191` (`verified === true`, `simulated: chain.simulated`) + 2 test files (scratch `git diff`) | Land the two-site fix **with the S-shaped cell**; every S flat anchor is in that class | **C, moving today, R lane.** #1597 ruled (1) at 15:2x (NEXT-PICKUP.md:19); KS-1638 (the hook fix it waited on) is on develop as `ce9860621`. **A, build M: the S-shaped cell is NOT in #1597.** Its 12 cells are mocked anchoring replies (test names read in the scratch clone); none is a bare `POST /api/anchors` under a connector key with a fresh v4 id, then verified through the gateway. Put that cell, the v2 site (`verificationV2.ts:231`) and KS-1640 into the queued follow-up (Spark brief `night/briefs/ks_1634_v2_p1/`, NEXT-PICKUP.md:20). **A, read-only census + reply:** R 50th's census found 0 qualifying rows on both boxes (`98cd2203`), but Stuart says dev-ps's count on Kintsugi "is not zero" (`1a4bafbe`). Both can be true: the census needs a simulated hash, and Kintsugi may anchor for real. Kintsugi's anchoring mode is unmeasured here. Re-run with Stuart's predicate (rows whose `document_id` matches no `documents.id`/`external_id`, hash placeholder or null) and reply. |
| 4a | **KS-1603** unguarded flat-anchor upsert | Backlog, High / unassigned | 2026-10-18T20:31 K (`6c1fc0cd`: second upsert `originate/src/routes/anchors.ts:109`, no guard, can rewrite `content_hash`) | none (git grep 0) | Interim ownership check on the flat anchor route | **A, build M, tier-1.** A security fix shape is Wednesday's to rule. Scope: refuse the `DO UPDATE` on `(document_id, network)` unless the stored row's first writer (connector provenance tenant/org) is the caller's. Covers both upserts (`anchoring/src/index.ts:1372`, `originate/src/routes/anchors.ts:109`). This protects S's existing rows; their ids are public through verify-by-hash (`e434bf98`). |
| 4b | **KS-1384** structural fix (per-event row + tenant column) | Backlog, High, label Decision / kamil.kreiser | 2026-10-18T22:42 S (`750da63c`: S's flat ids are fresh v4, never exposed early) | none | Schedule the multi-PR project | **B, card B2** (scheduling a multi-PR project). Sizing in `4384fa9a`: hot-table migration + backfill with 3 source rules, 5 writers, 6 SQL files, two services. **A, ticket reply S: deliver Kam's 9 Oct ruling (a) verbatim** (undelivered, see BLUF). |
| 5 | **KS-1612 + KS-1385** | KS-1612 In Progress / kamil.kreiser, last 2026-10-19T02:49 K (`9fa073a2`). KS-1385 In Progress / kamil.kreiser, last 2026-10-18T11:39 K | | #1568 merged `04a4a3393` (13:46 AEDT); #1549 merged `8cbadd8d4` (10-15); #1607 merged **`7e2f8157` 16:02 AEDT** | "Round 3 at its last gate. Land or re-plan, run the pre-check query before deploying, say when it rides Kintsugi" | **C.** Landed as round 4 (gate P1 GO WITH NOTE + delta R1 GO), and #1607 is on develop too. **Premise out of date** (see BLUF). **D** for "rides Kintsugi": blocked with the whole round (row 6). The 050 + 051 censuses are already the deploy seat's job (DEPLOY-BLOCKERS.md:37-39; line 39 is stale). **A, ticket reply S on KS-1385:** #1607 landed; the deploy conditions in plain words; no date. |
| 6 | **KS-695 (ii) + KS-1580 + KS-1570 round** | KS-695 In Progress, last 2026-10-13T06:59 S (`9efb2a68`), last K 10-12. KS-1580 Backlog, 0 comments. KS-1570 In Progress / unassigned, 0 comments | | #1497 `343a7b4e2`, #1535 `2cdf1d7a9`, #1539 `0bf6ef764`, #1541 `29bb45342`, #1547 `92d1316ff`, KS-1564 `a7cffc8d9`: all on develop 10-13 (git log). KS-1580: none | "Merged both sides 13 Oct, nothing deployed. Kintsugi waits on dev-ps carrying S ≥ aeae5ca, which is your deploy of 7cb1a4e" | **C** for the merges. **D** for the deploy, blocked on all of these: **(1) Stuart's own dev-ps deploy.** His doc says "S's deploy of `7cb1a4e` pending on Stuart" (list item 6), and PS-1284 has S post the note on KS-695 when it lands. So "your deploy" is not a K action. If Kam personally runs dev-ps, it is still outside Wednesday's grants (the October grant names kintsugi and demo only, EXPIRING-GRANTS.md:24). **(2)** DEPLOY-BLOCKERS.md:7 global row, still OPEN: "until KS-1570 is merged **and Kam has seen it**" (card B4). **(3)** the KS-1032 vouch secret (:31). **(4)** the 050/051 censuses (:37-39). **(5)** NEW: the KS-1402 develop 500. **KS-1580: B, card B3** (a new public error contract; the ticket itself says "nobody has decided whether to build it"). |
| 7 | **KS-1557** certify via lineage, write side | In Progress, High / kamil.kreiser | 2026-10-18T13:12 K (`28394c95`: gate F1 N4, the `:241` cross-tenant cell red under `MULTI_TENANCY_ENABLED=true` on untouched develop) | #1531 read side merged (`3a8713376`); KS-1538 legacy path `e4e320ba4`. **Write side unbuilt:** at `7e2f8157`, `certifications.ts` checks access only on the legacy path (`:219`, `documentId && !parentDocumentId`); the lineage branch (`:413-426`, `:543`) has a cycle check but no parent-access check | Build it; settle the multi-tenancy harness mode first | **A, build M (two steps).** (1) Settle the harness: run the ks1557 + ks1119 suites as `secuura_app` in both MT modes, and decide whether `:241` red under MT=true is a harness artefact or a read-side defect. Test discipline is Wednesday's. (2) Write side to Kam's ruling (b), *caller may send its own hash* (card `secuura-ks1557-certify-hash-semantics-1013`, delivered `c033e6fb`), plus a parent-access predicate. Stuart confirmed S sends the parent's hash, so S is compatible (`c1712c38`). |
| 8a | **KS-1454** signatureHash on sign | Backlog, Medium / kamil.kreiser, **0 comments**, last update 10-13 | none | none (git grep 0) | "Untouched; S's switch stays off until served" | **A, build M.** Optional `metadata.signatureHash` (`^[a-f0-9]{64}$`) in `anchoring/src/anchorSchema.ts`, limited to `sign`, returned on the by-id read and on verify-by-hash. S's detached sign is a flat anchor with a fresh id per event, so the KS-1385 latest-wins overwrite never reaches it (`11f96449`). **Flag:** this adds a field to the published chain contract. If Wednesday reads that as Kam's, fold it into card B5 as option 0. |
| 8b | **KS-723** declare `GET /api/anchors/{id}` | In Progress, High / kamil.kreiser | 2026-09-29T09:21 S (`ad1ed631`); no K comment ever | #1394 merged (`4eaf7741a`, the tx-hash read). The id read is undeclared | Same | **A, build S-M.** Kam ruled "ours" (card `secuura-ks723-whose-to-raise-1005` = a). The Spark brief for this route was rejected because declaring it would make the gateway 405 two live POST routes (card bluf), so it needs a Claude seat. Do it before 8a, because KS-1454's read-back rides on it (Stuart's doc, priority item 6). |
| 9a | **KS-1584** census reply | In Progress, High / unassigned | 2026-10-13T04:49 S (`15f6cab8`); no K comment ever | #1541 `29bb45342`, #1547 `92d1316ff` on develop | Read (SELECT only) the `svc_api_keys` row behind S's provisioning key on each box; confirm `organization_id` IS NULL | **A, read-only census (box access) + ticket reply.** This is also deploy-round item DEPLOY-BLOCKERS.md:19/:29 (the corrected predicate includes whitespace org ids). **Flag:** if the row is bound, re-minting and handing a key to S is Kam's (key rotation + credential handover to a client). |
| 9b | **KS-1604** fix shape | Backlog, Medium / unassigned | 2026-10-14T00:42 S (`f2de56a1`: bind at the ORGANISATION level; actor level on the connector's word) | none | Reply on the fix shape | **A, ticket reply.** Wednesday can rule the shape. S's proposal is the only one that does not undo KS-1175 (binding to the caller's own DID would blank every S identity). Say the build is unscheduled, with no date. |
| 9c | **KS-1575 + KS-1596** (sign without a version; `timestamp` verb; plus S's `rowHash` ask on KS-1575 `f7b4754e`) | KS-1575 Backlog / kamil.kreiser, last 2026-10-13T00:24 S. KS-1596 Backlog / unassigned, 0 comments | | none | A reply on the timestamp verb | **B, card B5** (new lifecycle shapes and fields in the published contract). **A, holding reply now:** "received, with Kam, not scheduled". This commits to nothing. |
| 9d | **KS-1629** GET that writes | Backlog, Low / unassigned | 2026-10-19T02:47 K (`b1b32a07`: with 051 a GET now permanently blocks registering that id on a simulate box) | none | "A word" | **A, build S (Spark-briefable)** + reply. Return without persisting; cell: the row count does not change with `SIMULATE_ANCHORING=true`. Do not edit the merged 051 header; record the omission in the PR. **A, read-only:** is `SIMULATE_ANCHORING` set on the demo VM? The comment says this is open (RUNBOOK says true; project CLAUDE.md says unset). |
| 9e | **KS-1633** certify anchors before writing its row | Backlog, Medium / unassigned, 0 comments | none | none | "A word" | **A, build M** (the ticket's option 1: write the `documents` row first, as `POST /api/documents` does) + reply. Same file as row 7, so the same lane, after it. |
| 10 | Housekeeping (Stuart's doc, not in the message): **KS-1387** | In Progress / kamil.kreiser, last 2026-10-18T17:04 K | | #1581 `b45b69171` | "Fixed and proven by a clean rebuild of develop on 19 Oct (33 services); close it" | **A, ticket close.** Ask S to paste the rebuild evidence on the ticket, or record his doc's claim as the evidence, then close. The K comment says a clean `docker compose build` was the real check and was not run. |

Ticket-reply sizes: each is S, one comment. All replies are Linear comments on Secuura tickets, which is within grants.

---

## Draft cards (B)

### B1 `secuura-ks1402-who-creates-the-holder-1019`
**Title:** KS-1402: Platform S's people are not K users, so every S custody transfer finds no holder. Who creates the holder?

**BLUF:** Your 6 Oct ruling (a) works: originate now resolves the holder itself (#1437, on Kintsugi since 12 Oct). Stuart measured that every S transfer then answers 404 RECIPIENT_NOT_FOUND (KS-1402 `05020fec`, 12 Oct): S registers organisations, never people, and K creates no user from `onBehalfOf`. The custody transfer is still not recorded, and S falls back to a flat anchor. Stuart has waited on this since 12 Oct (PS-1091 is blocked on it). Separately, develop answers 500 on the same route since 14 Oct; we fix that either way, and it does not need you.

**Options:**
- **(a) K creates an INVITED stub user on transfer, as `POST /api/certifications/issue` already does for `holderEmail` (KS-74).** A K build with a tier-1 gate (it writes a user row from a connector call, so the tenant boundary and PII must be proved). S changes nothing. It keeps "on-behalf-of resolution is K-side", the principle behind your 6 Oct (a).
- **(b) S calls `POST /api/users/stub` before each transfer (PS-1091).** No K change; S's key is allowed today. This is work we would be asking Stuart's team to do.
- **(c) Hold.** S's rights-assign cell stays red.

**Recommendation:** (a).
**Default if unanswered:** nothing is built on the stub. The 500 fix proceeds. KS-1402 gets a status reply saying the stub decision is with you. Nothing is asked of Stuart.

### B2 `secuura-ks1384-schedule-per-event-anchors-1019`
**Title:** KS-1384: you ruled one anchor per lifecycle event on 9 Oct. It is a multi-PR project and is not scheduled. When should it start?

**BLUF:** Your 9 Oct (a) was never built and never posted to the ticket; Wednesday posts it now. Seat J sized the work at develop `83ed01af`: a migration and backfill on the live anchor table (three source rules), five code writers bound to the tenant, six SQL files, two services. Stuart prefers it (it also closes KS-1603 for good). Anything merged to develop rides the next Kintsugi round, and that round is already waiting on Stuart.

**Options:**
- **(a) Start now.** One Claude seat; design PR first, each PR Opus-gated, merging as ready. It joins the deploy round already queued.
- **(b) Design now, merge after the Kintsugi round lands.** The small interim ownership check on the flat-anchor route (KS-1603) goes ahead now on its own.
- **(c) Hold the project.** Only the interim check is built.

**Recommendation:** (b). Fees: production anchors nothing today (Stuart's doc B4), so the per-event fee you accepted does not bite yet.
**Default if unanswered:** (c). The interim check is built under the existing grant; the project is not started; Wednesday raises it again at the next morning receipt.

### B3 `secuura-ks1580-erasure-revoked-key-code-1019`
**Title:** KS-1580: Platform S asks for an error code that says "this key was revoked by erasure". Build it?

**BLUF:** After an organisation erasure, K revokes the key last. A retry then gets a plain 401 "Invalid API key". S cannot tell that 401 from any other revoked key, so it infers "already erased" from its own attempt count (on S develop `aeae5ca`). Stuart says nothing waits on this (KS-695 `7221c520`, `4738f54c`). The code would be a new error contract on a public route: a reason recorded at revoke, plus a sub-code on the gateway's 401.

**Options:**
- **(a) Build it after the Kintsugi round.** Small, tier-1 gate.
- **(b) Decline.** S keeps its attempt-count rule.
- **(c) Build it now.** It rides the pending round.

**Recommendation:** (a).
**Default if unanswered:** not built. The ticket gets a reply saying it is with you, and S's rule stands.

### B4 `secuura-ks1570-round-may-deploy-1019`
**Title:** The KS-1570 round has been on develop since 13 Oct. Have you seen it, and may Kintsugi take it once Stuart's dev-ps deploy lands?

**BLUF:**
- Your 13 Oct note said the ADMIN role must be bounded before any deploy. It is: five of five pieces merged on 13 Oct (#1535, #1539, #1541, #1547, KS-1564). The deploy-blocker row closes only on your word.
- The order Stuart set still holds: Kintsugi only after his dev-ps runs S `aeae5ca` or later. That deploy is his and is pending.
- Since then develop also carries KS-1612 and KS-1385 (migrations 050 and 051), and a new 500 on S's custody transfers that we will fix before any deploy.

**Options:**
- **(a) Yes.** Once Stuart notes dev-ps on KS-695 and the 500 fix is merged, Wednesday runs the read-only census seat, then one Kintsugi deploy under your October grant, carrying every open deploy-blocker condition. Demo follows only after Kintsugi is verified and uat-ps carries `aeae5ca`.
- **(b) Yes, but send me a one-page summary of the KS-1570 round first.**
- **(c) Hold all deploys.**

**Recommendation:** (a). The October grant ends Sat 31 Oct.
**Default if unanswered:** no deploy; the row stays OPEN.

### B5 `secuura-s-signing-contract-additions-1019`
**Title:** Platform S asks K for new signing records on chain. Build which, and when?

**BLUF:**
- **KS-1575:** record a signature against an existing K document without making a new version. On that ticket S also asks that every anchor accept `metadata.rowHash`, a plain hash that pins S's own ledger.
- **KS-1596:** add a `timestamp` verb for a timestamp added after signing. For PDF and Office files it makes a new version; for a detached signature it is a flat anchor.

All three change the published contract and depend on how events map to anchors (KS-1384). KS-1454 (the signature hash) is the base the others build on and goes ahead either way.

**Options:**
- **(a) Build all three after KS-1454, inside the KS-1384 project.**
- **(b) Build the `timestamp` verb and `rowHash` now; build KS-1575 with KS-1384.**
- **(c) Not now.** Reply that they are parked.

**Recommendation:** (a).
**Default if unanswered:** a holding reply on both tickets ("received, with Kam, not scheduled"). Nothing is built.

---

## (A) items by lane (no file collisions with the live seats)

**Live seats.** R holds `api-gateway` (KS-623, KS-1503, #1608 `src/index.ts`, #1609 `src/services/health.ts`, KS-1622 → `routes/platform.ts`, the KS-1545 audit-log hunk per `1f73d7ac8`), originate `routes/verification.ts` (#1597), and KS-1637 (#1589 residue tests). Files were read from the PR diffs in the scratch clone; for R's unraised tickets the files are inferred from the ticket text. **J has merged #1607 (16:02); J's lane is `anchoring/src/index.ts` + `anchorOverwriteGuard.ts`, free once J wraps.** J's Low follow-up for INF-1/INF-2 may touch anchoring tests, so check its file list first.

1. **New seat: originate custody (free now).** KS-1402 500 repro + fix (`originate/src/routes/documents.ts` ~`:1586`). This is the first job: it blocks every deploy. Then the holder stub per card B1, if ruled (a).
2. **New seat or R after KS-1622: gateway `routes/platform.ts`.** KS-1195 register-connector `rateLimit` (Kam's ruled (a)). It is the same file as R's KS-1622, but a different hunk (register-connector vs audit-log). Either R takes it after KS-1622, or a new seat takes it now and R rebases KS-1622. Recommend the new seat now: it is S's priority 2.
3. **One seat, the anchoring lane (after J wraps).** In order: KS-1603 interim ownership check (`anchoring/src/index.ts:1372` + `originate/src/routes/anchors.ts:109`) → KS-1629 (`anchors.ts:168-219`, same file) → KS-723 (OpenAPI spec + gateway method routing) → KS-1454 (`anchorSchema.ts` + read paths + spec). KS-723 goes before KS-1454 because both touch the spec. KS-1629 alone is Spark-briefable if this seat is busy, but it shares `anchors.ts` with KS-1603, so sequence them.
4. **One seat, originate certifications (free now for the write side; the verify cell waits for #1597).** KS-1557 step 1 (the MT harness, read-only runs) → KS-1557 write side (`certifications.ts`) → KS-1633 (`certifications.ts`, same file). If step 1 finds a read-side defect at `:241`, that touches `verification.ts`, so it waits until #1597 merges.
5. **Spark / R after #1597 merges.** The KS-1634 v2 site + KS-1640 + Stuart's S-shaped cell (`verificationV2.ts` + a gateway-level test). The Spark brief is already queued (NEXT-PICKUP.md:20); add the S-shaped cell to it.
6. **No files (Wednesday or a read-only census seat with box access).**
   - Ticket replies: KS-1195 (deliver Kam's 10-09 ruling), KS-1384 (deliver Kam's 10-09 ruling), KS-1385/1612 (#1607 landed + deploy conditions, no date), KS-1402 (status: 500 being fixed, stub with Kam), KS-1604 (shape), KS-1629/KS-1633 (triage word), KS-1575/KS-1596 (holding), KS-1387 (close on evidence).
   - Read-only on both boxes: the KS-1584 provisioning-key row, the KS-1634 census with Stuart's predicate, and `SIMULATE_ANCHORING` on demo (KS-1629).

**Deploys:** none of the (A) items is a deploy. Every deploy Stuart asks for (KS-1402 demo-pk, KS-1612 "rides Kintsugi", the KS-695 / KS-1570 round) is (D) under DEPLOY-BLOCKERS.md:7 (OPEN, global) and Stuart's dev-ps precondition (:23). The October grant covers kintsugi then demo only, until Sat 31 Oct (EXPIRING-GRANTS.md:24).

**External communication beyond a ticket comment (Kam's):**
- Any answer to Stuart in the chat where he posted this list.
- Option (b) of B1 (asking S to build the stub call).
- Re-minting or handing over S's provisioning key (KS-1584) or rotating S's live connector keys (KS-1195).
- Any date promised for a Kintsugi or demo landing.

**Unmeasured, stated as such:**
- The cause of the KS-1402 500.
- Kintsugi's anchoring mode (simulated or real).
- Which revision Kintsugi and demo run today. My source is the 10-12 K comment and Stuart's doc; I did not probe the boxes.
- Whether Kam personally runs dev-ps deploys.
- The files R's unraised tickets (KS-623, KS-1503, KS-1622) will touch. I inferred them from the ticket text.
