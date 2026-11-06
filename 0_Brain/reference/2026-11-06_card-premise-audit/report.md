# Card premise audit, 2026-11-06 (read-only)

Auditor: a read-only agent for Wednesday. Written 2026-11-06. Nothing was written to the board, git, mail or any card.

## 1. Count of cards read

21 `secuura-*` cards that Kam ruled today were read in full with `decision_queue.sh show`. The three already known were skipped: KS-365, KS-1194 and KS-736. The `wed-*` cards were out of scope.

For 19 of the 21, the ticket or tickets behind the card were read whole through Linear GraphQL (description plus every comment, sorted by createdAt). Tickets read: KS-1707 and KS-1784, 1152, 1171, 1205, 1410, 1214, 1536, 1545, 1622, 1670, 1641, 1744, 1733, 657, 753, 946, 1081, 1084, 1600, 2031, 2032, 2038, 2059, 2060.

Two cards could not be checked against a ticket (section 5):
- secuura-push-queue-prerun-preflight has no ticket.
- secuura-peter-created-on-our-account rests on a 216-ticket census that I did not read.

The 21 cards:
- ks2038
- push-queue-prerun-preflight
- ks1081
- deepmerge-row5
- ks1600
- ks2032
- ks-1171
- ks-1410
- ks-1670
- ks2031
- ks-657
- ks-1733
- ks-1545
- ks-1205
- ks-946
- ks-1536
- ks-1152
- ks1084
- ks2059
- ks2060
- peter-created-on-our-account

**Control for "I read every comment".** Every ticket returned `pageInfo.hasNextPage = false` at `comments(first:100)`. The largest count was 10, on KS-1641, so none came near the page limit. Linear gives no total comment count in this query, so that is the comparison I had.

A second control: every comment id that a card, or a seat's comment, cites as delivered appeared in my fetch. That includes d53191cf on KS-1707, 6ea34fe1 on KS-1081, a28d1286 on KS-2059, 0c4295c2 on KS-2060, 074154a7 on KS-946 and 87f7b75e on KS-1622. So the fetch sees the newest comments.

Repo reads were read-only `git show` and `git grep` at `1b1b65c7415f`. That is the local develop checkout, behind GitHub's tip, so repo facts are as of that commit only.

## 2. CONTRADICTED

**C1. secuura-ks-1536-platform-admin-role-one-list (chosen: a). The count, the "key policy" sentence and the reach of the role are all contradicted.**

- Card says: "the sign-in service keeps seven more lists" and "the seven-list count is from the ticket and was not recounted". It also says "the key policy treats it [platform_admin] as an ordinary user".
- Count. Comment `ab7fc3b2` (2026-10-20T04:20:18Z), on KS-1536: "This ticket's 'seven divergent lists' is an undercount ... So the count is **at least twelve**." The same comment says originate has `services/originate/src/routes/adminConfig.ts:60`, `SUPER_ADMIN_ROLES = [... 'platform_admin']`, and that it is "Used, not dead", giving cross-tenant tenant resolution. It also gives api-gateway 7 sites, originate 4, auth 3, anchoring 3, packages/shared 2, tokenisation 1, security 1, and says originate "alone holds four sites using the identical three-spelling literal that omits SUPER_ADMIN" (filed as KS 1701).
- "Key policy" sentence. The ticket description's own "CORRECTION to the 'measured consequence'" says the "ordinary tenant user" reading "is true of the function and false of the route". On the running mint route, `decideMint` refuses `platform_admin` with 403, because it is not in `KEY_ADMIN_ROLES`. The same role gets three different answers on one request path.
- The card's sentence holds for `decideTenantAccess` only.
- What stands. "Only someone inserting that role by hand can have it" is SUPPORTED by `0f41081f` (the `platform_admins` table starts empty, the column defaults to `super_admin`).
- Plausible effect on Kam's choice (my reading only): option a, "one shared list without platform_admin, after a check", would remove a role that api-gateway accepts in 7 sites and originate accepts in 1 site (adminConfig). The card gave six gateway places and presented the key policy as the lone dissenter. The card already says "after a check", so I think a is unlikely to flip to c. The scope of that check is larger than the card states.

**C2. secuura-ks1084-measure-now-spark-off. This is about an option's detail, not the chosen option. Kam chose b, so it has little effect.**

- Card, option a: measure "One read site and one write site" on a two-tenant stack.
- Comment `ae430016` (2026-09-25T00:02:14Z), on KS-1084: Part B is tabled because "the api-gateway `/api/batch` surface answers 401 to every caller, so the write site cannot carry `x-tenant-id` until it is reachable at all". KS-1243 is the blocker.
- The batch write site that the description lists is therefore not drivable. The only other write site named is `platform.ts:249-251`, `POST /api/admin/refresh-tenants`. The card does not say which write site would be measured.
- Plausible effect on Kam's choice (my reading only): I do not think it changed it. It would only have weakened a, and he chose b.

## 3. UNSUPPORTED, where a decision rested on it

**U1. secuura-ks-1670 (chosen: b). The redirect rule is already written elsewhere.**

- The card treats the KS-1641 `:515` redirect as an open decision and says to apply a fixed sentence to "the redirect".
- Meanwhile the card says KS-1744 "proceeds on its own written scope".
- KS-1744's description says to make that same line (now `:684`) "send `token_exchange_failed`", a short code on the URL, and to keep the detail in the log. Comment `f8f54e0d` (Peter, 2026-10-26T12:57Z, on KS-1641) says the same.
- So two different rules, a fixed sentence and a code, are aimed at the same redirect. The card does not say so.
- Everything else on the card checks out (section 4).

**U2. secuura-ks2038-who-may-approve-transfers (chosen: a). The "measured" claim for execute, cancel and the two-approval sale is not in the ticket.**

- Card: "Seat W 29th measured at handler level that a user of another tenant gets 200 on approve, reject, execute and cancel, and that one caller can satisfy a two-approval sale alone".
- KS-2038 has 0 comments. Its description says gate 215 measured reject and approve only. "Transfer `execute`, `cancel`, and the list route's reach" and "the multi-approval inference" are listed under Not measured and Read, not run.
- Seat W's own measurement may exist in mail I may not read, so it is not contradicted.
- At `1b1b65c7415f`, `services/transfer/src/index.ts` execute (`:802`) and cancel (`:870`) check only the transfer's status. They read `req.user?.userId` for the history row and have no tenant or role check. That is consistent with the card, by code read and not measured.
- "No frontend calls these doors", the two published sentences and the costs (corporate unapprovable, inheritance failing closed) are NOT CHECKABLE from the ticket.

**U3. secuura-ks-657-dead-shared-cache-code (chosen: a). The size and boundary of "the cache section" do not match.**

- Card: "its cache section (15 files) is imported by nothing; only its types are used".
- Ticket: `src/` holds 15 files in total, "including" the cache files (description; comment `962baae8`).
- Repo at `1b1b65c7415f`: `services/shared/src/cache/` has 5 files. `src/` has 13 non-test files, which also include `security/*` (6) and `utils/logger.ts`. Seven `ks1868-*` test files cover the cache and Redis code.
- "Delete the cache section" therefore means either 5 files or all of `src/` (15 in the ticket, 13 at that commit). The tsconfig compiles `src/**/*` (comment `1cf87cce`). If all of `src/` goes, the package build and its `main` go with it, and the card does not say that.
- What stands. "Imported by nothing": at that commit the only relative imports into `services/shared` are billing's three `types/svs-types` lines. "Only its types are used, by billing" and "waited since 2026-09-14" (comment `09cbc163`) also hold.
- Plausible effect on Kam's choice (my reading only): probably not, since the ticket's own comments point toward fold or repair of the dead half. The "15 files" scale and the build consequence were not his to see.

**U4. secuura-ks1084 (chosen: b). The "predecessor was c" ruling is not on the ticket.**

- Card: "Your 22 Sep ruling on this card's predecessor was c, let the local model attempt a fix unmeasured".
- The only 22 Sep ruling on the ticket (`ae430016`) is on a different card, `secuura-ks1084-part-b-api-batch-surface-unauthenticated-dead`, option a: "File the ticket for a Claude seat; part B tabled". No `c` and no "local model" appear on the ticket. NOT CHECKABLE from what I may read. The "4 Nov ignore the Spark" statement is also not on the ticket.
- The rest of the BLUF is SUPPORTED by `3ff79aef` (2026-09-25): #1211 made two reads forward the tenant; the effect is unmeasured in both directions; the other sites are untouched.

**U5. secuura-ks-1205-rate-limit-refusal-audit-row (chosen: a). The scope word is too wide.**

- Card: "every refused request still writes one audit entry (marked 429), and still costs a key check".
- The ticket's F-5 measured a refused **mutation** (a refused POST: 1 audit row, status 429).
- The key-check cost was 0 validates for the already-cached key, and 1 validate only after the 60 s cache expiry (round 2). Exchange cost appears only at +481 s.
- A refused read was not measured.
- The recommendation (keep, document, pin) does not depend on it.
- The ticket's later state (`7ba3ef3e`, 2026-11-03) confirms F-5 is still open and the other six items are fixed.

**U6. secuura-ks2031-demo-timestamp-mock-row (chosen: c). The "code fix stops new ones" statement is shown only for Kintsugi.**

- Card: "The code fix stops new ones".
- KS-753's comments show PR 1502 deployed to Kintsugi only. Demo is frozen.
- The mock-fallback check ran on a disposable local stack. So "stops new ones" is not shown for demo.
- Everything else on the card matches the ticket: 1 demo row, 0 Kintsugi, rfc3161, `verified` true, proof begins `eyJ`, "whether that proof really is a mock token was not read".
- Demo is frozen, so new rows are not expected. I think this has little effect on the choice to remove the row.

## 4. One line per remaining card

- **secuura-deepmerge-row5-redate-past-1130 (a): SUPPORTED.**
  - Registry 4.3.1, 46 versions and 2023: comment `d53191cf`.
  - The mobile app is a production dependency and the other locks are dev-only: KS-1784 description.
  - KS-1784 Done: confirmed.
  - The 5 Oct rule on re-dates: `36e76f48` and `85fbbf53`.
  - "Four services" is the four named in KS-1784, plus the workspace root.
- **secuura-ks1081-pointer-would-drop-26-variables (a): SUPPORTED.**
  - I recounted at `1b1b65c7415f`: 26 names only in `.env.example`, 18 shared names with a different value, `PII_ENCRYPTION_KEY`, `VC_SIGNING_KEY` and `ENTRA_CLIENT_SECRET` among the 26, and 20 "required" markers (case-insensitive; 17 uppercase REQUIRED).
  - The four copy instructions are named in `6ea34fe1`.
  - The 16 Sep ruling is referenced in `0c73a042`.
- **secuura-ks1600-originate-malformed-permissions (a): SUPPORTED.**
  - The 400-versus-fallback difference and "0 non-platform rows hold provisioning-capable stored scopes" are in the KS-1600 description, item 3.
  - "Which callers send a malformed value" is not measured, as the card says.
  - The ticket also gives the figures 395 and 125 for refusal differences, which the card does not mention.
- **secuura-ks2032-non-live-admin-token (a): SUPPORTED.**
  - The measurement was run by gate 214 on PostgreSQL 15.19 and shows mint 201 and revoke 200 for non-live users.
  - PR 2030 closes the organisation path only, and its refusal text says "omit organizationId".
  - The unmeasured items match.
  - The ticket has 0 comments. "A key outlives the token" and the DB-outage cost are reasoning, NOT CHECKABLE.
- **secuura-ks-1171-8k-unconfigured-chain (b): SUPPORTED.**
  - The earlier ruling c is built, merged and in Kintsugi: `4e5c20d3`, `971e55e1`.
  - 8k is still open and unreachable without a real 64-hex hash, per the description.
  - `4e5c20d3`: "An unconfigured chain client still returns not found, which counts as an answered poll".
  - Repo at `1b1b65c7415f`: `provider.ts` line 452 is `if (!blockfrost) return null;`.
  - The three callers are `confirmation.ts:79`, `cardano/index.ts:295` and `index.ts:2030`.
  - One nuance: the rule as built counts the 60 s from when polling began, not from the 400 (`2042f003`). That is the same or stricter, and the card only repeats the ruling's wording.
- **secuura-ks-1410-ks-1214-mcp-rest-mirror-file-reads (a): SUPPORTED.**
  - Four routes read `filePath` (`4d9c4d44`).
  - There is no credential check although the spec declares `X-API-Key`.
  - KS-1410 fixed nine 500s and left `POST /hash` (`f23f89e7`, `cb994edc`).
  - Port is internal by repo configuration, and the gateway forwards one MCP route (KS-1214 description).
  - The package generator tells users to expose the server (`4d9c4d44`).
  - The OpenAPI wording "Absolute path to file (for local execution)" exists at `1b1b65c7415f`.
  - Omission, not contradiction: `4d9c4d44` also records that a caller acts as the server's own `SECUURA_API_KEY`, which the card does not say.
- **secuura-ks-1670-ks-1641-m365-error-text-in-responses (b): the facts are SUPPORTED, apart from U1.**
  - The three sites and their auth conditions are in the KS-1670 description.
  - Site 1 of KS-1670 is merged and deployed (`4600daa9`).
  - KS-1410's fixed sentence is `d8ac99b6`.
  - The auth service's 200-character cap is in the KS-1641 description.
  - Lines 689, 874 and 1173 confirmed at `1b1b65c7415f`.
- **secuura-ks-1733-proposals-list-unknown-query-keys (a): SUPPORTED.**
  - Description items 1, 3 and 4 and the 15 KB figure.
  - Upper-case status is pinned: `98882ef7`, `6c736363`.
  - The "extra key gets an error" cost is in the description.
- **secuura-ks-1545-audit-log-in-band-marker (a): SUPPORTED, with a wording note.**
  - A marker is a contract change needing a spec change and a gate: description.
  - The warning line "live in code" is true of develop. Item 1 is merged (`63b3a606`, `832b5fc6`) and the non-list first window is merged (`87f7b75e`).
  - Nothing is deployed: "api-gateway deploy is owed, both boxes".
  - The card's "when the read throws" now understates the shapes logged.
  - "KS-1622 also asks whether such a window should drop the platform half" is SUPPORTED by `7816e450` and `36deb641`, not by the KS-1622 description.
- **secuura-ks-946-path-spellings-limiter-accept-p3 (a): SUPPORTED, with a scope caveat.**
  - Three of four 404 and the `//` spelling served: `b3712ab3`.
  - The `//` spelling fixed by PR 884 and deployed to Kintsugi by ancestry, "not observed live": `1a160067`.
  - Re-price P3 and the MFA route not driven: `b3712ab3`, `074154a7`.
  - The 404 test ran on the login route and on `GET /api/users/me`. Six of the eight limiter mounts are only inferred (`02f2c885`; `074154a7` found no later drive). The card does not say that.
- **secuura-ks-1152-rotate-says-rotated-when-old-key-lives (b): SUPPORTED.**
  - `e321de49` (2026-11-01): gateway `platform.ts` lines 884-919, a stand-in `pg` pool and not a real PostgreSQL, `COMMIT` with the new key committed and the old key still active, `rotated: true` at line 919.
  - Options a, b and c are the same ones the gate posed.
- **secuura-ks2059-cross-tenant-stake (a): SUPPORTED.**
  - Measured by gate 219 on real PostgreSQL, 201, at PR 2039 and the prior develop.
  - There is no tenant column.
  - The seeded SYSTEM_ADMIN is in the default tenant (`userRepo.ts:1420`).
  - Proposed High, and "measured on the register route only".
  - Wording note: the ticket says "platform admin in tenant T1", the card says "admin in one tenant".
  - The KS-1906 precedent text and "read the ticket, not the code" are NOT CHECKABLE and are not contradicted.
- **secuura-ks2060-erased-user-wallet-vote-power (a): SUPPORTED.**
  - Neither erasure writer clears `wallet_address`.
  - Governance has 0 hits for USER_ERASED.
  - 200000 of DRep vote power was measured.
  - The originate path was read from source and not run.
  - KS-234 is named in the description.

## 5. What I did NOT check

- **secuura-peter-created-on-our-account: NOT READ against tickets.**
  - The 31 tickets and the 216-ticket census (Seat S 24th) were not read. The creator field cannot establish "Peter filed" (a comment on KS-1641 notes the Linear actor is shared across the fleet).
  - NOT CHECKABLE: the "26 filed by Peter, 5 by Stuart" split, the 2026-09-06 rule's wording, and "most already have merged PRs".
  - The card was read in full.
- **secuura-push-queue-prerun-preflight: NOT CHECKED.**
  - No ticket exists. The figures (19 min, 14 branches, 4.5 h, 91%, 948 of 1033 s, load1 16 on 12 cores) come from logs and a machine read that I may not read.
  - The delivered ADDENDUM mail was not read.
- **Mail and seat reports.** I did not read mail, the QA gate verdict files, or the 0_Brain/reference folders. Statements that cite only those, such as Seat W 29th's measurements or the drafter's prior-ruling-gate searches, are NOT CHECKABLE.
- **Prior-ruling gates.** The "closest ruling" statements (KS-1516, KS-1942, KS-1906, KS-1585, the 09-25 KS-1171 ruling) were not verified against their cards. Only the KS-1171 ruling appears on its own ticket (`a5f75423`) and matches.
- **Repo.** Reads were at `1b1b65c7415f`, behind develop. I did not open the cited files for most claims. Where a card gives a line number for a different ref, I checked it only if listed above.
- **Not covered.** I did not recheck any KS-365, KS-1194 or KS-736 content, or any `wed-*` card. I did not check whether later comments postdate today's rulings beyond what the fetch returned (the latest comment read was 2026-11-06T05:46Z, KS-946).
