# Gate 244, tier 1, round 1 of 2: KS-1536, PRs 2060 and 2061

| PR | Head | Verdict |
|---|---|---|
| 2060, KS-1536 3a | 796ea55fb8ebeb659ffacf64d24fd4f1a5b20661 | GO WITH NOTES |
| 2061, KS-1536 3b | edcb42e7ae99423740da3b1e87d6d4b60559c0fd | GO WITH NOTES. Kam should see the `admin` loss: see the top of that section. |

Head readings, origin, ls-remote. Start 18:28:02Z, mid 18:41:44Z, late 18:53:58Z: develop b27f5fb30f4a, 2060 796ea55fb8eb, 2061 edcb42e7ae99, all three the same each time. The end reading is at the foot of this file.

Severity is mine. Priority is not. No finding blocks on a defect in what either PR does at runtime: every gate I drove behaved as the PR says. The notes are about claims made to humans, one test gap on a key route, and what has not been counted.

---

## PR 2060 (3a)

**BLUF.** It does what card = a asks for the string `platform_admin`. At this head a `platform_admin` token gets the same status as an ordinary `OWNER` on all 75 enumerated gateway routes, where at the base it differed on 57. Nothing in product code still accepts the string as a role. What it does not do is reach "one list": 55 lists stay by the guard's own count, more by mine, and the guard is narrower than Kam's BLUF says.

### Findings

**F1, Moderate. "A guard fails the build if someone writes a new one" is too wide.** `packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts:89-133`; the sentence is in the PR's BLUF for Kam, and the ticket comment says "refuses a new inline platform-role list". MEASURED AT RUNTIME: planted files, G1 and G2 run per plant in my clone.

| Planted | Result |
|---|---|
| `const isSuper = (r) => r === 'super_admin' \|\| r === 'SYSTEM_ADMIN'`, a shape already in the product | green, invisible |
| `.js` under `src` holding `['super_admin','platform_admin']` | green, invisible |
| `.ts` outside `src` (`services/auth/integration/`) | green, invisible |
| `.ts` in a frontend with no `src` (`frontend/status/`) | green, invisible |
| `['super_admin', x[0]]`, a nested bracket | green, invisible |
| `r === 'platform_admin'` with `tenant_scope_bypass` in a comment on that line | green, invisible |
| Controls: plain list, `platform_admin` list, `.tsx` `new Set`, `"platform_admin"` lower-cased | red, 4 of 4 |

The first row is not hypothetical: `services/originate/src/routes/documents.ts:313` and `:1125`, `certifications.ts:1026` and `services/auth/src/middleware/authenticate.ts:249` are platform-role checks the count does not see. So "55 lists in 29 files" (which I recomputed: the baseline sums to 55 over 29) is a count of one shape, not of the lists. The body does say the guard proves wiring, not behaviour; it does not say what shapes it misses. Fix-shape: state the shape limit where the claim is made, or count comparison chains too.

**F2, Moderate. Kam's BLUF does not say how much of "one list" is left.** PR body, "BLUF for Kam": "Nine lists now ask one shared answer". The card's own question is whether the lists should be merged. The 55 appear only further down, and the ticket comment does not give the number. The remaining lists still disagree about tokens real people hold, READ ONLY:
- `services/billing/src/routes/webhooks.ts:265` `requireRole('SYSTEM_ADMIN','SUPER_ADMIN')` is exact, so a `super_admin` token, which is every Kintsugi `platform_admins` row, is refused where `isPlatformRole` says yes.
- `services/originate/src/routes/documents.ts:313`, `:1125`, `:1484` and `certifications.ts:123`, `:1026` omit `SUPER_ADMIN`.

This is what the PR says it is leaving ("each is its own authorisation change"), and the ticket stays open. The finding is only that the reader the BLUF is written for is not told. Full enumeration under Ask 3.

**F3, Minor. Two sentences overstate the refusal.** MEASURED AT RUNTIME: every route on the platform, admin and proxy routers, three roles, real gates, stubbed upstream.
- PR body: "still logs in, then is refused everywhere." False as written. 18 of 75 routes do not refuse it, for example `PUT /api/privacy/settings` and `POST /api/documents/upload`: it is an ordinary signed-in user. Accurate wording: "treated as an ordinary signed-in user".
- Ticket comment, which a client human reads: "refused on every gateway admin and platform route". `GET /api/platform/document-lookup` answered 400, not 403, for it and for `OWNER`, at the head. Same at the base. One route, no behaviour change.

**F4, Minor. Tokenisation's two key routes have no cell that can see them.** `services/tokenisation/src/index.ts:225` and `:294`; cell G5 counts the text `requirePlatformRole()` in the file. MEASURED AT RUNTIME: my plant ungated `/api/rotate-key` and left a stray `void requirePlatformRole();` above it, 97 of 97 green. The seat discloses the gap ("pinned by the shared middleware's cells and a text cell"). I rate it because these routes generate and rotate tenant keys. A second plant also survived: `requirePlatformRole` passing a user with no role, because M2 has no undefined-role row. The wiring is right at this head, READ ONLY: `app.use('/api', jwtAuthenticate())` at :49 is above both routes. Fix-shape: a tighter text match per route at minimum, a route cell if the entry module can be split; plus an undefined-role row.

**F5, Minor. Three stale pointers to removed lists.** READ ONLY.
- `services/api-gateway/src/index.ts:327-329`: says "grep that expression if the line moves", naming `SUPER_ADMIN_ROLES.includes(decoded.role)`, which this PR deletes.
- `services/api-gateway/src/utils/trustHeaders.ts:37`.
- `docs/security/AGENT-DOCUMENT-OPERATION-RULES.md:55`: `PROXY_ADMIN_ROLES`.

**F6, Note. 54 of the 94 REDs are red because the new predicate does not exist yet.** `expected undefined to be false/true`. True reds by assertion, as claimed, but they prove the export is absent, not behaviour. The behavioural weight is in the 24 gateway reds, which I reproduced and which are sound.

### Claims tested

| Claim | Result |
|---|---|
| RED 94 of 94, controls 106 of 106 at the base | Reproduced: 24+70 and 79+27, 0 cells on the wrong side |
| 200 of 200 new cells at the head | Reproduced: 97 + 103 |
| api-gateway 1837 of 1837 | Reproduced |
| Originate cells 5 of 5, tokenisation 8 of 8, `test_platform_admin.py` 19 of 19 | Reproduced. The pytest run exits non-zero on the repo's coverage floor because one file was selected; all 19 passed |
| 712 swept files; 55 in 29; 15 product importers of `isPlatformRole`; 34 touched files and their breakdown | All true |
| Every user token goes through `mapDbRole` | True. All 7 `generateTokenPair` calls read: 3 create `OWNER`, the rest come from the repo. The platform-admin branch is the only verbatim mint. `token-rotation.ts` has no importer |
| Originate list entry was unreachable | True: O1 passes, `requireRole` refuses first |

My own defects planted, 9, each naming its FAIL as "stays green": 7 caught by the right cells (admits `ISSUER_ADMIN` at `/api/admin/`, drops it at workflows, audit gate open, override open to all, verified path open, `adminScope` always platform, `PLATFORM_ADMIN` added to the set). 2 survived: F4.

---

## PR 2061 (3b)

### For Kam, at the top: Ask 1

**The `admin` loss is a wider call by Wednesday, not inside his card's words. He should see it.** He has been told on the panel (bf-2232cfc103f5, corrected by bf-89677e9b07f8, by the 2026-11-06 daily note; I did not read the panel text and found no reply and no card).

- **The card:** title and BLUF speak of `platform_admin` and of "seven more lists" in the sign-in service. Option a is "One shared list without platform_admin, after a check". Nowhere does it name `admin`. The seat itself offered option C, a card, and said "I may be reading 'One shared list' too widely".
- **The case for inside:** the ticket KS-1536 names exactly these two lists, each marked "but `admin`". A single list cannot keep `admin` without widening `PLATFORM_ROLES` everywhere, which KS-1283 fixed the other way. So it follows from "one list".
- **The case for wider:**
  - Wednesday's grant (`learnings/2026-10-27_design-changes-inside-a-ruling-are-mine.md`) covers a change of HOW that still delivers the ruled outcome. This changes WHO holds cross-tenant reach, which the tier reason names.
  - The reach is read selectively: "seven more lists" is cited to justify two, while `users.ts:444`, `:500`, `:556`, `:696`, `oauth.ts` `OAUTH_APP_ADMIN_ROLES` and `issuerCerts.ts:65` keep `admin`. So `admin` stays an admin at the same doors with no tenant to act in.
- **Weight:** zero known holders on Kintsugi by D 57th's count, no signature-class element there. Demo: see Ask 2. I read it as a receipt he should actually look at, not a stop; whether it needs his ruling before merge is his and Wednesday's. READ ONLY.
- **The ticket also says** "whether `ADMIN` and `platform_admin` should be organisation-bounded" is his call on KS-1535. That ruling (leave `ADMIN` unbounded, change before deployment) concerns upper-case `ADMIN` inside a tenant. 3b does not cross it, but it is the neighbouring question and he may want them read together.

**BLUF.** The code does what the READY's loss table says, and all of the loss table's cells are real routes with a mocked repo. Nothing a real login mints loses anything.

### Findings

**F7, Minor. "Cannot register or keep admin:read or admin:write" overstates "keep".** READY and ticket comment. `services/auth/src/routes/oauth.ts`, the PATCH handler: gate 1 only runs on scopes in the request body. A PATCH with no `scopes` passes, and an app that already stores a privileged scope keeps it. READ ONLY. The PR body's table is accurate. Holders: no such app was looked for.

**F8, Minor, unmeasured on any box. The CHECK may not be on the boxes.** Ticket comment: "compose's schema refuses that value by CHECK". True of `docker/init-platform/01-platform-schema.sql:74`. But B 69th's record, `5_Project_History/2026-10-27_seatB-69th/HANDOVER.md` about :309, says of demo and Kintsugi that the only `INSERT` on the box is `run-platform.sh:144`, the retired Container Apps path, whose table is `role VARCHAR(50) DEFAULT 'admin'` with no CHECK. If that table is what the boxes hold, a hand-inserted row that omits `role` becomes `admin`, and hand-inserts on Kintsugi happened on 2026-10-13 and 2026-10-27. The PR body carries the caveat ("depends on which ran first"); the ticket comment does not. Nobody has read the column on a box. Recommendation, READ ONLY evidence: read `\d platform_admins` with the recount.

**F9, Minor. The guard's baseline has slack after both PRs and no owner to lower it.** MEASURED AT RUNTIME on a trial merge of both: one new list in `users.ts` passes; three new read `12 > 11`, so today's count there is 9 against a baseline of 11. The body says it "can come down by 2" once both land. Neither PR does it, and no ticket line owes it. Fix-shape: a one-line follow-up.

**F10, Note. "With a tenant" is a column no mint reaches.** `platform_admins` mints carry no tenant and `users` never mints `admin`, so only the "no tenant" column can happen. The body says so. The cells are harmless.

### Claims tested

| Claim | Result |
|---|---|
| RED 32 of 32, controls 62 of 62 at the base | Reproduced, 0 cells on the wrong side |
| New cells plus `ks1210` | Reproduced as 133 of 133 by my wider glob, which also matched the older `ks1536` issuer-certs file and others |
| `services/auth` 1830 of 1831, the one is `ks949`'s walk | Reproduced exactly |
| 9 call lines in `users.ts`, stop not triggered | True, all mint sources read. Scan's 1152 files not re-run |
| The only `INSERT` names `super_admin` | True: `git grep` over the repo, plus every revision of `run-platform.sh` back to 2a29a168 names it. `UPDATE`s touch only `mfa_secret` and `password_hash` |
| The bare `admin` loss is reachable | True: `/api/users` and `/api/oauth` are proxied with no gateway role gate, so a holder really does reach these routes |

My own defects planted, 8: all caught (keeps `admin` in each file, spoofable fold, PATCH gate off, role ceiling off, list scope ignored, dead copy of the list back, ownership list loses `admin`).

### The re-merge: compare, not re-gate, on conditions

MEASURED AT RUNTIME: on trial merge 3a + develop b27f5fb30f4a + 3b, the only conflict is `docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md`, at :197-198 as the READY says. Guard 97 of 97, auth `ks1536`+`ks1210` 133 of 133, gateway 103 of 103. The conflict is two adjacent lines, each side changing one: keep 3b's :197 and 3a's :198.

A compare is enough if all of these hold; any failure means re-gate on what moved:
1. `git diff edcb42e7ae99 <new head>` minus what develop brought is that one doc only.
2. No line carries `PLATFORM_ADMIN_ROLES` or `PLATFORM_SCOPE_ROLES` at :197-198.
3. Develop has not gained a change to `routes/users.ts`, `routes/oauth.ts` or `isPlatformRole` in between. KS-2083 (`feature/ks-2083-…-y6`) touches `users.ts`: it merges clean with 3b by merge-tree, but if it lands first the move is no longer doc-only.
4. G1, G2 and the auth cells are re-run at the new head.

---

## Ask 2: what the count does not cover, and what would break

**Kintsugi count.** D 57th's report read: `platform_admins` 3, all `super_admin`, active; users 25 sums; run as a role that bypasses RLS, so not a zero under fail-closed RLS. It is a snapshot of 2026-11-06 05:20Z, and rows were hand-added twice in the month before. Recommendation, READ ONLY: re-read the same query at deploy time.

**Demo is "not counted". True today, but a record exists that neither PR cites.** B 69th, 2026-10-27, HANDOVER about :239-251: demo `platform_admins` has 1 row, `admin@secuura.com`, `super_admin`, active; `users` has 33 rows, at least two `system_admin`. Eleven days old, demo frozen by card `secuura-ks1401-058-merge-demo-billing-1104`. So the likely answer is "nothing breaks", and the owed count remains owed. What each result would mean:

| Demo row holds | On deploying 3a | On deploying 3b |
|---|---|---|
| `super_admin` (the record) | nothing | nothing |
| `platform_admin` | The whole platform console refuses it: platform routes, `/api/admin/`, audit export, workflows, tenant override, tokenisation keys. Login still works; the portal shows it as `admin` | nothing further |
| `admin` | nothing: all nine lists 3a changes already refuse it | Cross-tenant user list and edit go: 403 and 404. Portal still shows it as a super admin (`authStore.ts:24`), so a demo operator sees pages that refuse |
| `system_admin`, `Super_Admin`, `org_admin` | Gains at the gate. Downstream, originate's exact lists still refuse, so real gain is the tenant override and gateway platform scope | Gains the OAuth privileged-scope gate only |

Recovery in every row is one `UPDATE` on one row: demo-affecting, so approval-class.

**Tokens already issued.** READ ONLY for the lifetime logic; not driven.
- Access token: lives to `JWT_EXPIRES_IN`: code default 1h (`services/auth/src/services/jwt.ts:43`), compose default 1d (`docker-compose.yml:774`). Kintsugi's value not read.
- Refresh does not carry a role forward: `/refresh` and the OAuth refresh grant re-mint from `getUserByIdPreAuth`, through `mapDbRole`. A platform-admin id with no `users` row gets InvalidCredentials.
- So an issued token with a losing spelling gets 403 from deploy until it expires, then cannot renew that spelling. One with a gained spelling gains for that same window. Nothing here revokes either.
- `admin@secuura.com` exists in both tables on the record, so its refresh yields `SYSTEM_ADMIN`, not `super_admin`. Pre-existing.
- Bounded at one access lifetime, and only for a token whose row has since changed. No record of such a change on Kintsugi.
- Test tokens are separate: `ENABLE_TEST_TOKENS` only, role free-form. `tests/e2e/tests/api/admin.api.spec.ts:20` writes `admin`, 59 `/api/` lines and 0 `/api/users`, so 3b does not touch it. Whether it is on for any box: not read.

---

## Ask 3: what still accepts it, and every list

**Still accepting the string after 3a.** `git grep -w -i platform_admin`, whole repo, positive control: base hits 13 role sites, listed below. Nothing admits it as a role. Left:
- `services/auth/src/services/password.ts:273`: longer minimum. Declared exception, harmless.
- `docker/init-platform/01-platform-schema.sql:80`: CHECK still permits the value. Declared.
- `frontend/shared/src/auth/index.ts:56`: `role.toLowerCase().includes('admin')`, maps it to UI `admin`. Declared in the table. The only substring role test in the census.
- `systemTest/schemathesis/tests/test_notification_bola.py:46`: declared, harmless.
- The RLS sentinel `app.tenant_scope_bypass = 'platform_admin'`: a GUC value, not a role.

**List left out by the seat:** none that names the string. The 13 at the base: `platform.ts:65`, `auth.ts:695`, `admin.ts:606`, `:612`, `audit-export.ts:142`, `proxy.ts:1121`, `:1255`, `adminConfig.ts:60`, `tokenisation index.ts:223`, `authStore.ts:25`, `frontend/shared auth/index.ts:47`, `password.ts:273`, plus `systemTest support/platform_admin.py`.

**Every list still spelling a platform role, by my census at 3a head** (quoted-literal scan of non-test source, comment lines excluded; `users.ts` and `oauth.ts` lines change at 3b as marked):

| File | Lines | Holds |
|---|---|---|
| shared `security/keyRevokePolicy.ts` | :60 `PLATFORM_ROLES` (the one), :77, :94 | SYSTEM, SUPER; org-bounded; ADMIN |
| auth `routes/users.ts` | :182, :194 (gone at 3b), :215-216, :223, :444, :500, :556, :588, :696, :1472 | `admin` at :444 :500 :556 :696 |
| auth `routes/oauth.ts` | :1246 (gone at 3b), :1247 | `admin` |
| auth `routes/issuerCerts.ts` | :65 | `admin` |
| auth `middleware/authenticate.ts` | :228, :249 | no `admin`; :249 unseen by the guard |
| auth `services/password.ts` | :273 | exception |
| api-gateway `index.ts` | :921 | `admin`, `ADMIN`, lower-case spellings |
| api-gateway `routes/verification.ts` | :263 | exact |
| security `provisioningPolicy.ts`, `index.ts` | :43, :1152 `KEY_ADMIN_ROLES` | `ADMIN` |
| originate `middleware/auth.ts` | :149, :170 | maps `super_admin` to SYSTEM |
| originate `middleware/documentWriteRoles.ts` | :37 | exact |
| originate `routes/documents.ts` | :313, :1125, :1484 | omits `SUPER_ADMIN`; first two unseen by the guard |
| originate `routes/certifications.ts` | :123, :1026 | omits `SUPER_ADMIN`; :1026 unseen |
| originate `routes/gdpr.ts` | :172, :362, :399, :594, :627, :645 | SYSTEM, ORG |
| originate `routes/systemErrors.ts` | :172, :194, :216, :226 | SYSTEM, ORG |
| originate `routes/adminConfig.ts` | :45 | SYSTEM, ORG |
| billing `routes/webhooks.ts`, `billing.ts` | :265 | exact, refuses `super_admin` |
| vc-issuer `routes/status.ts`, `ownership.ts` | :58, :82 | exact |
| demo-service `seed/generators/access.ts`, `documents.ts` | :61, :115 | seed filters |
| frontend/admin `Layout.tsx`, `Users.tsx`, `Profile.tsx`, `store/authStore.ts` | :108 :125 :303 :319; :89; :105 :111; :24-25 | UI |
| frontend/shared `auth/index.ts` | :45-47 | UI |

Baselined files I did not open line by line are the guard's: `services/nft-certificate/src/routes/nft.routes.ts`, `services/security/src/index.ts`, `originate rbac.ts`, `gdprService.ts`. Treat this table as the census of one scan, not a proof of completeness: its instrument is a quoted-literal regex, so it shares a blind spot with any list built from variables, and the database-minted value is the known case of that (ticket comment of 2026-10-20).

---

## Merge order and other PRs

- 3a on develop: clean. 3b on develop: clean. 3b on develop + 3a: one doc conflict, as ruled.
- 3a + Y's KS-2032 + KS-1152: clean, guard 97 of 97. So the guard's frozen baseline survives both.
- **V 26th's KS-736 (c70f8182f43d):** 3a + KS-736 merges clean to tree 4367dab3af6f, the tree V reports. Adding V's item 2 (954af815c7b7, `adminConfig.ts`, its second overlap with this PR) is clean too. On that merge, `ks570` + gateway `ks1536` 117 of 117, guard 97 of 97. No semantic interaction: 3a changes one fixture line, `role: 'super_admin'`, and V's cells pass on it. V's branch was read from its local clone, since it is not at origin. Whichever lands second moves its own head; a moved 3a head voids this verdict for that PR, and the V grants are head-bound on 796ea55fb8eb.
- Also sharing paths by recent branch, not read further: T 14th's stated hold on `platform.ts` and `proxy.ts`. Branches listed as sharing paths from before 11-06 were not checked for already being squashed.

## NOT tested

- A real login, a decoded token, a running stack, any box: none. The four platform suites and any pre-merge box: not run, by commission. Both PRs' pre-merge boxes are unticked and their hook reads PREFLIGHT INCOMPLETE 13/16.
- What an admitted caller gets downstream on the gained spellings beyond the reads named: not driven.
- Tokenisation's routes at runtime: F4.
- Open-PR list: no `gh` under "network only for git fetch", so overlap comes from recent branch heads and may include merged work or miss a fork.
- The 26 and 16 tampers: sampled by my own plants, not re-run one by one. eslint, tsc and the ratchet: not re-run. The frontends: no runner. Node LTS: no, v26.8.1.
- Ticket comments: read from the seat's posted files, not from Linear. Panel text: not read.

## My own conduct

- Findings only. Wrote only this folder, `/private/tmp/g244`, and my session scratchpad. Network: git ls-remote and fetch only. No box, no docker, nothing posted.
- Dependencies: with no install allowed, each tree got a real `node_modules` of symlinks into Y's clone `worktrees/s-y6-ks1536` (same root lockfile, read only), with `@secuura/*` pointing at my own tree and shared built per tree. So this substrate is Y's dependencies, not a clean install.
- **A false red of mine, recorded:** my first whole-auth run showed 2 extra failures and a failed suite. They were my harness: those cells read `process.cwd()`, and I was running from the Wednesday folder under no-cd. Same at the base. Re-run from the service's directory: 1830 of 1831.
- My route probe ended with 1 to 2 unhandled errors from vitest while its one test passed; I did not chase them. All routes returned statuses, and `SYSTEM_ADMIN` was refused on 0 of 75, so the probe could see an admit. The probe uses test tokens or a header stand-in for the gate's principal, as the seat's cells do.
- A pretooluse hook refused three `git -C $VAR` write verbs as pointing outside; I re-ran them with the literal clone path the commission names, where it passes.
- Load: "under 8" was NOT held at every reading. Above 8 at 05:30 (8.6, 8.7), 05:37 and 05:38 (13.0, 13.1, 9.8, during my reads with other seats live), and 05:50 and 05:51 (11.1, 10.9, right after my two whole-suite runs). I held heavy runs after the first spike; the last spike is mine.
- Clone removal: the common rules say remove it; the QA brief template's standing line says never `rm`, quarantine instead. I followed the commission for this named clone: `/private/tmp/g244` removed with `rm -rf` on the literal path, after the end reading. `rm` does not follow symlinks, and Y's `node_modules` was confirmed still present afterwards. So the source tree is gone: anything re-checked needs a new clone. My probe, plant scripts and their JSON remain in the session scratchpad.

End reading, 18:56:58Z, origin: develop b27f5fb30f4a, 2060 796ea55fb8eb, 2061 edcb42e7ae99. No head moved during the gate, so neither verdict is void.
