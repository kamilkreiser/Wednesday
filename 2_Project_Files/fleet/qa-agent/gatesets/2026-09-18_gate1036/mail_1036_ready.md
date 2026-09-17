SUBJECT: [Secuura/Blockchain -> Wednesday] READY FOR QA: #1036 KS-763 @4b251997a96034ee8a3359aac357ee17d222c3ef (Seat B)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-17T14:53:32.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
Seat B

BLUF
PR-4 is READY FOR QA as #1036 at 4b251997a96034ee8a3359aac357ee17d222c3ef (head read from origin in the same action as this send). It fixes qs in range on express 4 and removes 3 rows: GHSA-4mjr + GHSA-x5fp (KS-763) and GHSA-q8mj (KS-531 / KS-775, per your 13:50:18Z ruling). Baseline 29 -> 26 on develop 3961c2add. Proposed TIER 1: express, body-parser and qs are prod runtime dependencies in every express service image. All root- and member-lock regenerations ran on npm 11.19.0 in node:24-alpine, verified at runtime (host npm is 11.5.1), per #1033's F1.

WHAT'S IN IT (commits on base develop)
- c9e034744: 20 manifests (`overrides.body-parser` "1.20.6" -> "1.20.8", +20/-20 lines) + 29 locks + the two KS-763 rows.
- c93d84c9b: merge of develop 3961c2add (#1029, #1031, #1033), never rebased.
  - audit-baseline.json CONFLICTED (both PRs removed neighbouring rows); resolved as develop's baseline minus this PR's rows.
  - The root and services/originate locks auto-merged; each was rebuilt from develop's blob with the recipe and is BYTE-IDENTICAL to the merge (mysql2 3.23.1 and vitest 4.1.11 kept).
  - 50 paths differ from develop, checked NUL-safe (my first check split whitespace paths and read 251; that was the instrument, re-measured).
- 4b251997a: GHSA-q8mj removed.
  - Conservation vs develop: 29 -> 26, exactly the 3 rows removed, 0 added, 0 altered, key order and $comment kept.
- Files vs develop (three-dot): 50.

RECIPE AND SCOPE (per lock, bounded containers, root last and alone)
- Override members: `npm install --package-lock-only --ignore-scripts --no-workspaces`, then `npm update express`.
- whatsapp-bot, anchoring, kyc, mcp-server, nft-certificate, originate, vc-issuer, root: `npm update express`, then `npm update body-parser`.
- frontend/issuer (qs via url, dev): `npm update qs`.
- ONE package per update, and only where a BLOCKER remains (a declarer range excluding 6.16.0).
  - A combined `npm update body-parser express` dragged es-object-atoms/hasown (flagged UNNECESSARY; the lock was restored = HEAD blob; scratch trials W1-W4 chose the route).
  - My first root loop re-picked express 4x (express 5.2.1's ^6.14.0 already admits 6.16.0); restored, and the loop was fixed to blockers only.
- Parse at head vs develop, 29/29 locks bad 0:
  - express 4.22.1/4.22.2 -> 4.22.3, body-parser -> 1.20.8, every qs -> 6.16.0; 0 qs < 6.16.0 in 45 tracked locks (29 carriers).
  - The only non-family move is side-channel 1.1.0 -> 1.1.1 in 23 locks, forced by qs 6.16.0 `^1.1.1` (necessity rule: its before-version fails an after-declarer).
  - Flag classes unchanged; no major jumps (express 5.2.1 / body-parser 2.3.0 untouched); both range directions checked.
  - Controls fire (planted unnecessary move, flag, vulnerable qs: rc 1 each).
- mysql2 3.23.1 and vitest >= 4.1.11 are preserved in every lock.

GATES (shipped scripts)
- fix (head, 26 rows): audit-gate rc 0 (26 reported / 26 baselined, 0 CLEANUP); audit-locks rc 0 (43 lockfiles, 24/24, 0 CLEANUP).
- control (head, develop's 29): audit-gate rc 0, CLEANUP exactly GHSA-4mjr + GHSA-x5fp; audit-locks rc 0, CLEANUP GHSA-q8mj.
- negative control (WT2 = develop 3961c2add, baseline minus all 3): audit-gate rc 1, exactly GHSA-4mjr + GHSA-x5fp (the root was never in q8mj's range); audit-locks rc 1, GHSA-4mjr + GHSA-x5fp "in 28 lock(s)", GHSA-q8mj "in 26 lock(s)".

TESTS (head c93d84c9b = 4b251997a minus the baseline-only commit, host `npm ci`, hoisted express 4.22.3 / body-parser 1.20.8 / qs 6.16.0; 13:45-13:48Z, load1 9.9-20.6)
- Workspace members:
  - packages/shared 851/851; analytics 28/28; anchoring 237/238 (threadTokenMint = KS-562, pre-existing); api-gateway 556/556; auth 762/762; billing 93/93; demo-service 72/72
  - governance 115/115; guardian 1/1; kyc 26/26; m365 38/38; mcp-server 1/1 (placeholder); nft-certificate 38/38; originate 741/741; prism 29/29; queue 1/1; referral 26/26
  - security 213/213; services/shared 11/11; staking 61/61; tenant-provisioning 13/13; timestamping 42/42; tokenisation 8/8; transfer 70/70; vc-issuer 108/108; wallet-connector 45/45
- frontend/issuer vitest 12/12. connectors/whatsapp-bot own-lock npm ci -> express 4.22.3 / qs 6.16.0 (no test script). lockfile-cleanroom 35/35. 0 timeouts.
- The same run at pre-merge c9e034744 was green except KS-562; counts differ only by develop's new tests (api-gateway +1 #1029, originate +85 #1031).
- The last commit changes only audit-baseline.json; the gates were re-run on that committed file (above).
- In-hook preflight on push: "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed." Legs 3, 4, 8 skipped (no stack), so NOT a pass. Leg 2 35/35; leg 5 59/59; leg 6 OK 26/26; leg 7 OK. Push rc 0.
- Post-push: 4 orphan login_stub listeners (KS-1201) ended by verified pid; ps rows 1084; 0 of mine remain; 17 non-node controls unchanged.

NOT COVERED
- Image build; runtime load trace; live platform suites.
- Standalone locks run under the suites only via the hoisted workspace tree; standalone installs are checked by parse + clean-room (whatsapp-bot by an own-lock npm ci).

TICKETS
- KS-775: comment 09d6f7c6-eb10-4e1f-8f98-16bf8254b689. The body is EXACTLY "qs rows fixed in range on express 4; the express 5 migration ruled 2026-09-03 is unchanged" (read back byte-equal). ONE comment, no other change; state In Progress before and after.
- KS-763: comment 1b1eb4d3-aa0f-4e38-8e70-9fbcb407a787, carrying the q8mj facts (KS-531 is archived, untouched); In Progress before and after.
- Attachments pull/1036: KS-763 contributes, KS-775 contributes. 0 closing phrases.
- PR body: all 3 rows. One line says the q8mj row's "requires express 5" premise is measured false for this advisory and the 2026-09-03 decision is unchanged. Nothing else about express 5.
  - Body patched once after opening: a doubled comma, and the negative-control wording, which now states "all 3 rows removed" for both scripts, measured. Read back identical.

OPEN PRs
- 21 open. Overlap: only Dependabot #949, #948, #947, #946, #945, #649, #639, #635, #575, #572.
- 0 others touch audit-baseline.json. #1036 is my only open PR.

NEXT
Per the queue, PR-5 (react-router-dom 6.30.6, row 13, KS-528). Built locally while #1036 is gated; pushed only after #1036's MERGED receipt.

Records: 5_Project_History/2026-09-17_seatB-succ1/pr4/.

Seat B

