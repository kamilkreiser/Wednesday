# DRAFTER REPORT: Seat T 11th, lane B (api-gateway verification, allow-list, admin)

## BLUF
- Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-05_seatT_laneB_gateway_verification_admin.md`. All three gate literals are present at line start (checked); `self_check_view.sh` ran.
- Seat **Secuura/Blockchain-T, Seat T 11th**. Measured max in `5_Project_History/history.md`: **T 10th** (line 877); T 11th 0 hits; control K 14th 1 hit. Model claude-opus-5-5 via routing row **C3** (G1 for the gate); rows C2/L1 name Sonnet for the nine non-design keys, left as Wednesday's call.
- Develop tip measured: `5fc5569ed96a` (`ls-remote`, 16:3x).
- **Two lane-plan items are NOT builds** (KS-1180, KS-1204). **Both ruled tickets belong in this lane** (measured), with two cross-lane edit hazards named.

## Queue, in order, with each ticket's remaining scope (quoted from the ticket, narrowing stated)
1. **KS-1087** (High): item 2 only. "item 2 (forwarding a credential originate accepts), a design call". Seat raises a QUESTION to Wednesday with its own measured options BEFORE building; brief does not pre-answer. Item 1 is merged (PR 1008).
2. **KS-1262** (High): N3 + N4. "N3: the per-user GET still returns the whole platform-wide record ...; N4: a second reserved id, `default` ... Both need the separate key space." Verified still present (admin.ts:1588-1594; PUT guard only at :1608).
3. **KS-1180** (Medium): evidence only. See "Looked wrong" below.
4. **KS-1185** (Medium): F2 and F3 only ("both Polish"; F1, F4 merged). Still present (verification.ts:602-607).
5. **KS-1204** (Medium): NO BUILD, listed. All code merged (PR 1035); only a box observation is owed.
6. **KS-1237** (Medium): third row X-INFO-ALWAYS-EMPTY only: "needs its own test file" against the router that owns `GET /api/connector/info` (services/health.ts, not enforcement.ts).
7. **KS-1534** (Medium, ruled today 16:09:53, card a): item (b) only, "Refuse in both reads with one shared message (fail closed)". Placed after KS-1237 so the reader is pinned first. Item (a) merged (PR 1842).
8. **KS-1505** (Medium): part 2 (log success only when bytes changed). Present (index.ts:670-678).
9. **KS-1493** (Low, ruled today 16:10:00, card a): N2 remainder: comment beside the limiter block in index.ts plus one new test file; no behaviour change. N1 merged (PR 1751). Placed after KS-1505 (same file, different region).
10. **KS-1539** (Low, unassigned): the create-path bare catch (now verification.ts:826-833; ticket said :817-823). Info reader done.
11. **KS-1542** (Low): the BigInt cell title (test:111) only.
12. **KS-1614** (Low): items 1-3 (item 4 merged), in verification.ts + the ks1185-f1 test file.

## Excluded
None. All ten lane B tickets plus KS-1534 and KS-1493 are in. Reduced to non-builds: KS-1180, KS-1204.

## Looked wrong in the lane plan
- **KS-1180's target no longer exists.** KS-1628 (PR 1589, commit 78cb3c393) deleted `ks1073-...` and `ks1072-...` tests and retired the gateway's `/api/documents/:id/verify`; `persistedAnchored` 0 hits at develop (control: `originateForwardTimeoutMs` 6). The brief makes it evidence-only; closing depends on KS-1628's deploy state, UNMEASURED.
- **KS-1204 is complete in code**; lane plan listed `admin.ts` as if a build remained.
- **Lane plan paths lack the `Blockchain/Dev/` prefix.** The brief gives the real paths.
- **KS-1614 does not need `index.ts`** (lane plan listed it); `index.ts` is only KS-1505 and KS-1493.
- **KS-1237 lists `services/enforcement.ts`**; its remaining row is a test against `services/health.ts`.
- **Cross-lane hazards (brief tells the seat to stop and QUESTION, not edit):** KS-1534 may need the 403 description in `api-gateway.openapi.ts` (lane C's KS-1645 names that file); KS-1493 names `READ_ONLY_PATHS` in `middleware/rateLimitSkip.ts` (lane C). The brief keeps KS-1493 to an `index.ts` comment + a new test file.
- Lane plan had ruled "KS-1534 default_action b" on the card; Kam ruled a, so the card default no longer applies.

## UNMEASURED (each is conditional in the brief)
- Pane id and launch time of the seat.
- Whether any open PR currently touches a lane B file (no GitHub read).
- KS-1628's deploy state (needed for KS-1180).
- KS-1087: whether the approver's role/scope passes originate's create gate; whether the gateway can mint a credential; document ownership when approver differs from creator. The seat measures these for its QUESTION.
- KS-1262: what is stored under `notif:*` on any box.
- KS-1534: whether `api-gateway.openapi.ts` needs an edit.
- `originate/src/routes/documents.ts:188` was cited from the ticket comment, not re-read (middleware/auth.ts was read).

## Method notes
- Tickets read via Linear GraphQL, `comments(first:50)` sorted client-side; develop files via `git show <sha>:<path>`; cards read from decisions.json by exact id. No repo write, no mail, no Linear write.
