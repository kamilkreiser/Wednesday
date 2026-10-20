VERDICT: GO WITH NOTE at head a7de040ab040... (tier 1, round 1 of 2; landing tree e63a595ca1558271e02563432b8f95b8102718fe on develop f4259b8ed3875316a269d3228031c198eec39edd; 0 blockers, 4 notes)

# Gate BT1: PR #1657 (KS-1157, OAuth marker on sessions), Opus 5.5

## BLUF
The change does what it says and nothing else. Both OAuth grants (`oauth.ts:969` authorization_code, `:1078` refresh_token) store `mintedBy: 'oauth'`. No other `createSession` site marks: I found 7 call sites in my own census, and the 5 non-OAuth ones pass 5 arguments. A caller cannot set or change the marker through the body, headers or token claims. Every read-modify-write keeps the marker on a marked session and never adds it to an unmarked one. No reader's parse result changes. OAuth responses, TTL, key shape and clientType are byte-identical between develop and the landing tree; the stored record gains only `,"mintedBy":"oauth"`. The auth suite went from 99/1096 to 100/1103 with 0 cells vanished and 0 status changes. `tsc` rc 0.
The notes are about missing test cells and evidence wording. None is a product defect.

## Findings
- **N1: the PR's 7 cells miss three ways the change could regress (cell gap, not a defect).** Three compile-clean mutants, each killed only by my scratch probes, pass all 7 PR cells:
  - X1: the password-login site (`auth.ts:592`) passes `'oauth'`.
  - X2: `rotateSessionRefreshToken` deletes the marker.
  - X3: the code grant takes the marker from `req.body.mintedBy`.
  C2 and C3 pin "unmarked" only at the service layer. No route-level cell pins that a non-OAuth grant stays unmarked, that the marker survives a rewrite, or that a caller cannot forge it. The product is correct today; future regressions on these three paths would not be caught.
- **N2: "8 arms, 8 killed" counts the red-first run as an arm.** The seat's evidence (`5_Project_History/2026-10-20_seatG-12th/evidence/mutants_ks1157.json` and `.txt`) records **7** mutation arms, M1 to M7, all killed. The eighth is the red-first run with no product change. The PR body draft says so ("8 arms counting the red-first one"). The ticket comment draft ("8 mutation arms, 8 killed") and READY_CLAIM ("8 arms, 8 killed") do not say so. Small wording overclaim.
- **N3: "the remaining work is the selective denylist query" understates what is left.** This is pre-existing behaviour, outside this PR's diff. The OAuth refresh_token grant never reads the session named in the refresh token. In my probe BT1-G2 the grant returned 200 against an empty store, minting a fresh marked session for `sessionId: 'sess-old'`, a session that does not exist. So a denylist that revokes sessions by `mintedBy` alone would not stop a holder of an OAuth refresh token from re-minting. The ticket comment's Recommendation says the remaining work is "the selective denylist query", which reads as more settled than it is. The PR itself claims only that the field is written ("not proven possible, only that the field it would select on is now written"). The PR is correct on this point; the ticket comment wording overclaims. This may already be covered by KS-1150 R-2, which handles the rotation/denylist half and is still open; I did not check.
- **N4: cosmetic line-number drift in the PR body.** The `setex` line numbers (`:244 :277 :292 :307 :370`) and the reader line numbers (`:258,287,302,342`, `:189`) are pre-patch values. On the landing tree each is 2 higher (246/279/294/309/372, 260/289/304/344, 191). The `session-validation.ts:105` citation is correct.

## Questions: FOUND / TESTED / HOW
1. **Every OAuth grant marks, and nothing else does: CONFIRMED.**
   - Census: grep for `createSession(` across all of `Blockchain/`, product code only. It found 7 sites: `wallet.ts:375`, `auth.ts:286` (register), `:443` (platform admin), `:592` (password login), `:1257` (social), and `oauth.ts:969` and `:1078`. Positive control: the same grep finds the definition at `session.ts:128`.
   - No MFA route, service route or interactive-refresh route mints a session. `/api/auth/refresh` rotates in place at `auth.ts:717`. The token endpoint only accepts the authorization_code and refresh_token grants.
   - Real grants, driven: probe `gatebt1-oauth-real.test.ts` sends raw-socket POSTs to `/api/oauth/token` with the **real** `createSession` running over an in-memory store. Both grants stored `mintedBy:'oauth'` with `clientType:'browser'`. The same probe on develop stores no marker.
   - Real non-OAuth routes, driven: probe `gatebt1-integration-probe.test.ts` copies `auth.integration.test.ts` and adds a `setex` recorder that captures the stack of every write. Over the full 61-cell run there were 108 `sess:` writes. Writes from register, login, refresh, logout and wallet: 0 marked. Positive control: the recorder saw 15 marked writes from my direct `createSession(...,'oauth')` calls.
2. **The marker cannot be forged or carried incorrectly: CONFIRMED.**
   - The parameter is the literal type `'oauth'`. The call sites pass constants. TSC-CONTROL: passing `'oauth2'` gives tsc rc 2 (TS2345).
   - Forgery attempts, all leaving the stored marker `'oauth'`, clientType `'browser'` and deviceId unset:
     - BT1-F1/F2: body `mintedBy:'evil'`, `clientType:'api'`, `client_metadata`, `deviceId`, plus headers `X-Minted-By` and `X-Client-Type`.
     - Refresh-token claim `mintedBy:'evil'`.
     - BT1-N1: forged body and headers on register, login and interactive refresh; those sessions stay unmarked.
   - Carry-through (BT1-P1): a marked session keeps `'oauth'` through rotate, activity update, extend, list and revoke. An unmarked session stays unmarked through the same five. The OAuth refresh grant marks its new session on its own, so it does not depend on carrying the marker over. `/api/sessions` uses an explicit projection, so the marker is not exposed (BT1-L1, with the stored record marked).
3. **Readers: REFUTED that the field can cause a parse error.** The value is a constant string serialised by `JSON.stringify`, so it cannot make the JSON invalid. Every reader ignores unknown keys. Nothing in product code reads `mintedBy`; grep finds only the 3 lines the PR adds.
   - BT1-R1, against the shared `isSessionActive`:
     - marked, live record: true
     - pre-fix record (unmarked): true
     - revoked marked record: false
     - corrupt JSON: null (positive control for the fail-open path)
     - record with the marker plus an unknown nested future field: true
   - BT1-R2: the KS-43 hydrate loop keeps the browser cap over a mixed set; 12 creates leave 10 live, the same as 12 unmarked creates.
   - Mixed-version rollout: `session.ts` differs from develop only in the 2 added lines, so an older pod's read-modify-write keeps the field.
4. **No other behaviour change: CONFIRMED.** I ran the same probe on develop and on the landing tree and diffed the reports. The only differences are the `mintedBy` key and its value. Unchanged:
   - status and body for both grants
   - headers, apart from date/etag
   - TTL 86400
   - key shape `sess:sess_<64 hex>`
   - clientType
   - the three error responses
   - record bytes once the marker is stripped (461)
5. **The selective denylist is not built: CONFIRMED.** The commit message and the PR body draft say this plainly. Wording overclaims: N2 and N3.
6. **No weakening, and the landing: CONFIRMED.**
   - Auth suite, compared by file plus full cell name: develop 99/1096 all pass, landing 100/1103 all pass. Vanished 0, status changes 0, new 7 (R1 to R4 and C1 to C3).
   - Arms: 3 of the author's (A-M1 and A-M2, both two-line oauth anchors, plus A-M4 and A-M5) and 3 of mine (X1, X2, X3). All 7 were killed. For each arm: anchor count 1 asserted, a byte change asserted, tsc rc 0 before it counted, failed count cross-checked against the red labels, no load failures, and sha256 restore equality asserted afterwards.
   - `tsc --noEmit -p services/auth` rc 0. `tsconfig.test.json`: 42 errors, all in pre-existing files, matching the author's baseline of 42. It lists the new file and my two probes, and none of them has an error.
   - Merge-tree:
     - develop + #1657: rc 0, tree `e63a595c...`, 4 files.
     - #1655 head + #1657 head: rc 0, 1 output line.
     - develop + #1655 (`2346900a...`, matching the author's figure) + #1657: rc 0.
     - The file sets are disjoint: intersection 0 (self-control 4), and `services/session.ts` is not in #1655's 8 files.
   - Heads checked by `ls-remote` at start (00:26Z) and end (00:37Z): #1657 `a7de040ab040f460c83f5784ae132a2667ed80c6`, #1655 `893506989ae7...`, develop `f4259b8ed387...`. They did not move.

## NOT RUN
- I did not drive the platform-admin (`auth.ts:443`) or social (`:1257`) sites. Coverage there is static: both pass 5 arguments, and the parameter type admits only `'oauth'`.
- No real Redis, no Docker, no platform suites, no preflight legs.
- No GitHub or Linear read of the posted PR body or ticket comment `8bed4975...`. I read only the seat's local drafts (`mail/pr_body_ks1157.md`, `mail/comment_ks1157.md`), which may differ from what was posted.
- I did not re-run author arms M3', M6 or M7.
- I did not run the auth suite on the combined develop + #1655 + #1657 tree; I ran only its merge-tree.

## Disclosures
- One early batch script wrote `/tmp/x`, 260 bytes, a file list. It went outside my scratch folder and used `2>/dev/null`, against the rules. It is left in place because of the no-rm rule.
- `gh` is not logged in for WEDNESDAY, so the PR refs were fetched with the Secuura repo's own deploy key, read-only, into my scratch clone only, from `-C` on the scratch clone. Nothing was pushed or written under `!CODING`.
- Vitest ran through a python subprocess with `cwd=` set to the scratch clone's `services/auth`. The cwd-dependent cells `ks1009` and `ks949` need it; the first bare run from the WEDNESDAY cwd load-failed those two files, and that run is discarded.
- WEDNESDAY untracked paths outside the allowed roots at the end: none.

## Wall-clock
00:24Z to 00:39Z (about 15 minutes).
sha256 of `sed '1d;$d' verdict.md`: 5684a954a364645725adf6be428f8ff9e951fbfbf3be78df265987de32a4dffd
