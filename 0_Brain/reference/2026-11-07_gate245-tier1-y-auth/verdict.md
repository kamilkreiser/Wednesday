# Gate 245, tier 1, round 1 of 2: verdict

| PR | Ticket | Head | Verdict |
|---|---|---|---|
| 2066 | KS-2032 | baf577c78e7f | GO WITH NOTES |
| 2073 | KS-1152 R-880-1 | 9709acff5c5f | GO WITH NOTES, one item for Kam |
| 2075 | KS-2083 | d2245bf37fe0 | GO WITH NOTES, one item for Kam, and "closes" must be corrected |

Each verdict is a statement about that SHA. Readings at origin, develop b27f5fb30f4a throughout:
- start 2026-11-06T19:01:39Z: develop b27f5fb30f4a, refs/pull/2066/head baf577c78e7f, 2073 9709acff5c5f, 2075 d2245bf37fe0
- end 2026-11-06T19:31:44Z: the same four. Nothing moved; no verdict is void.

Severity is mine; priority is not.

Environment for everything below: my clone on the boot volume, Node as the host has it (the seat's v26.8.1 line, not an LTS), node_modules copied from the seat's s-y6-sessend, whose root lock is byte-identical (53b4107f). Real PostgreSQL 15 is my own private cluster, stopped at the end, built as the containers build it: docker/init/0[1-9]*.sql, then the 59 main-DB migrations, then the app role's grants, the same recipe as the seat's y6pg.sh. No Redis exists on this host, so every session finding is on a stand-in store with the real session code.

---

## PR 2075, KS-2083: a role change ends the sessions

**BLUF.** The change does what Kam's card "Both" asks and nothing else. The 2 failing auth cells are fully explained and are not this PR. But the sentence "it closes the walk-around" is too strong: a demoted user's request in flight during the revoke can bring the session back to life, with the walk-around open again. That race is already on develop for every revoke, so this PR does not make it worse.

**For Kam, at the top:** his card's "does not cover" list is the outage, hand edits and old keys. It does not name F1 because nobody had measured it. Whether KS-2063's walk-around counts as closed with F1 open is his call. I do not read F1 as blocking this merge, because merging strictly narrows the exposure.

### The two failing auth cells: answered

**Cause: vitest's 5 s default timeout, hit by a first read of a cold tree on the external DevMASTER drive. Not load, not code, and the same at this head and at develop.**

| Measured, the ks949 walk verbatim (same skip list, same extensions) | First walk | Later walks | Files read |
|---|---|---|---|
| Seat's tree at this head, DevMASTER (s-y6-sessend, d2245bf37) | 21,755 ms | 124, 102 ms | 1,028 |
| Seat's tree at develop, DevMASTER (s-y6-base, b27f5fb30) | 17,633 ms | 143 ms | 1,028 |
| Seat's tree s-y6-ks1536, DevMASTER | 24,851 ms | 119 ms | 1,027 |
| My clone at this head, boot volume | 678 ms | 105, 97 ms | 1,028 |
| My clone at develop, boot volume | 682 ms | 111 ms | 1,028 |

- **Whole suite, boot volume, 4 workers, load about 5:** head 1765 of 1765, develop 1736 of 1736. The 29 extra are exactly this PR's cells. Run again on all three PRs merged: 1765 of 1765.
- **Reproduced at both, by a cold model:** each file's first read delayed 20 ms, the measured cold rate. Head: the same two cells fail, 5,004 and 5,001 ms. Develop: the same two, 5,004 and 5,002 ms. 29 of 31 at both. The seat's figures were 5,004 and 5,003.
- **Why two cells and not one:** the second cell starts its own walk while the tree is still cold, and gets its own 5 s. The third walk finds it warm.
- **They are timeouts, not assertions:** `STACK_TRACE_ERROR` is what vitest's JSON reporter writes for a timeout. Forcing `--testTimeout=60` gives the same message at both trees. The seat's JSON showed no assertion text either.
- **The PR cannot affect them:** the walk skips `__tests__`, the file count is identical at both, and the only product change is one condition.
- **Seat's history agrees:** s-y6-base at develop with the session-end patch also timed out at 5,005 and 5,001 ms, and the same base with no timeout in another run.
- **Not run:** real vitest on a cold DevMASTER tree, because that writes outside my clone. The drive measurement and the cell result are two separate measurements joined by the model.

### Findings

**F1, MAJOR. A role change answers 200 and the session survives, if one of the person's requests is in flight.** `services/auth/src/services/session.ts:286` (read then write, not atomic), reached on every request from `middleware/authenticate.ts:160`; `session.ts:313` is the revoke it races.
- FOUND: `updateSessionActivity` reads the record, then writes it back whole. If a revoke lands between the read and the write, the write restores `isActive: true`, with a fresh 24 h TTL. The session is by then out of `user_sessions`, so no later revoke-all can find it.
- TESTED, MEASURED AT RUNTIME, real route, real `authenticate()`, real session code, real `isSessionActive`, stand-in store:
  - Deterministic, twice: PATCH role 200, role written, gateway check true, auth check true. The old token then raises a second account: 200, peer is ORG_ADMIN. A following PATCH status suspended: 200, and the session is **still** active.
  - Rates with 1 ms store latency, 20 rounds each, two runs: no traffic 0 and 0 (control). One client serial 2 and 5. One request every 50 ms 1 and 6. Burst of 40 in 40 ms 20 and 20. Latency 0: 0 and 0.
  - Develop, status suspended, no PR: 0, 4, 4, 20, 0. The same race, so this is old behaviour, KS-360's path too, and logout's.
- Oracle: Purpose, and Product (the PR says the request "now gets 401 and changes nothing").
- Not measured: real Redis, whose latency sets the real rate. My rates belong to my latency model. That the race exists does not depend on it.
- Fix-shape (READ ONLY as to the fix): make the activity write unable to resurrect a revoked record, for example an atomic check inside the store. Regression test the owner should add: revoke between that read and that write, then assert both checks still say gone.
- Sentences this makes untrue: PR body "it closes the walk-around", flow fragment "It closes the walk-around KS-2063 names", ticket comment "Closes: the walk-around". They are true for a serial request only. They should say so and name the race.

**F2, MEDIUM. A store flag that drops after `authenticate()` gives a silent 200 with nothing revoked.** `session.ts:332` returns 0; `routes/users.ts:846` takes it.
- MEASURED AT RUNTIME, real `initRedisSession` over a fake client, the error event fired during the write: 200, role written, log `sessionsRevoked: 0` at info. After the store heals the session is live on both checks and the old token raises a second account, 200.
- The PR names a revoke that THROWS (500) and not this one. KS-1407 B1 fixed exactly this on the password path (`routes/auth.ts:906`), so the class is known. The status path has it too. Narrow window, silent result. It belongs in "does not close".

**F3, MEDIUM, old behaviour. `role: "constructor"` and `role: "__proto__"` pass the role allow-list.** `routes/users.ts:208,220`: `ROLE_ALIASES` is a plain object, so inherited names resolve. The comment beside it calls this an allow-list (KS-486); `routes/users.ts:622` uses the same normaliser on create.
- MEASURED AT RUNTIME: PATCH with either answers 200 and hands the repo a function or an object, at head and at develop. At this head the session now ends too. `toString` is 400 because of the lower-casing, as are null, empty, a number, an array and `ADMIN`.
- PROBED on my real PostgreSQL through node-pg: `users.role` is varchar(50) with no CHECK, and it stores `function Object() { [native code] }` and `{}`. `mapDbRole` then reads OWNER. Not driven through the real repo end to end. Who can do it: anyone who may PATCH that target today.

**F4, MINOR. A PATCH naming the role the row already holds cannot end a stale token.** `routes/users.ts:844` compares to the row, not the token. MEASURED: row OWNER, token ORG_ADMIN, PATCH OWNER: 200, session live, the token raises a second account. So anyone demoted before this deploys, or by hand, cannot be cut off by re-sending the role; only a real change or a status change does it. The hand edit is named; the remedy not working is not.

**F5, MINOR. Two statements in READY and the body are looser than the evidence.**
- "29 of 31 on the first run at 7,047 ms ... a cold walk": the 7,047 ms cell is "is NOT seeded when DEMO_SECUURA_PASSWORD is unset", a cold `import` of userRepo, not a walk. The walk cell in that run is 5,001 ms. Same root cause, wrong cell.
- "KS 1155 names ks949": not confirmed. The title in the seat's `linear_boot.txt` reads "packages/shared tree-walking guards exceed vitest's 5 s default"; ks949 is in `services/auth`. I did not read the ticket, because network is git only. If it does not name ks949, an auth case needs adding.

### Tested and held
- **Reds:** 11 of 11 by assertion at develop, 18 of 18 controls, 29 of 29 at head.
- **My plants, each anchor asserted, restored by git:** compare to the caller's role (3 red), revoke not awaited (2 red), promotion from OWNER skipped (1 red), every role key counts (4 red). No survivor.
- **Seat's read that auth fails closed is now measured:** flag down 401, store rejecting 500, peer unchanged both ways.
- **Role writers, my own census by a different grep:** 19 raw `UPDATE users` lines. Role is written only by this route, the boot seed and the stub claim; `createUser`'s ON CONFLICT list has no role. Agrees with the seat.
- **Who loses access:** the person whose role really changes. The admin portal form always sends `role` (`frontend/admin/src/pages/Users.tsx:281`) but sends the row's own value (`:246`), so a name edit keeps the session. READ ONLY. Akto sets status only (`lockedAccountRole.ts:287`).
- **Doors:** both gateway routes (`routes/admin.ts:1537`, `routes/proxy.ts:521`) forward the Bearer to auth. READ ONLY.

### Not tested
Real Redis. A real login or real JWT. Gateway and auth in one process. The four platform suites, including whether a fuzz of this PATCH logging out personas disturbs Schemathesis. Any box. A login in the moment between the revoke and its own session write. The refresh path after a revoke, read only in part.

---

## PR 2066, KS-2032: a tenant-level key needs a live ADMIN

**BLUF.** Does what card a asks, for role ADMIN only. Every claim I re-ran held, the KS 1585 cheat resolution is correct, and I could not find a real caller who loses access. Notes only.

### The KS 1585 cheat resolution: checked, correct
`git show --cc` on baf577c7: line 2 is PR 2046's correction (the "403 ... mint body says ... revoke refusal says" form), with this PR's shorter mint sentence. Line 3 is this PR's "Admin access" wording. Neither side was taken whole. Both quotes match the code at `services/security/src/index.ts` and the assertions in the integration cell (`:180`, `:283`). The 503 text matches `answerScopeReadFailure`. No stale copy of the old 503 text remains in non-test source or docs (positive control: the same grep finds "omit organizationId" where it should stay).

### Findings

**F1, MINOR. A comment at the mint is now false.** `services/security/src/index.ts:1329-1330`: "A null target organisation ... is still allowed". Also about line 1335: the read runs "only when it can matter (an ADMIN naming an organisation)". Both predate this PR and now mislead. READ ONLY.

**F2, MINOR. "Load timing" is not the whole story for the two shared cells.** MEASURED AT RUNTIME: the first full `packages/shared` run in a fresh merged tree, load about 5, failed threadToken at 45,234 ms (1514 of 1516). The second run of the same tree: 1515 of 1516, whole suite 8 s wall, threadToken about 1 s. So it reproduces at low load on first touch; it is a cold start, as with ks949. Alone it read 18,609 ms once, then 1,604 and 954. ks879 passed for me both times. The remaining failure, `wallet-signature`, fails at develop too (KS 1727 not read). None touches these files.

**F3, NOTE. Wednesday's text changes are wider than the card's words.** Dropping "omit organizationId" and rewording the 503 and its log title move text on the organisation path. The card says only "apply the live-admin test". The PR says so openly, statuses do not move, and nothing in source or docs matches the old strings. Not Kam's words; harmless as far as I can see.

### Tested and held
- **Reds at develop, by assertion:** policy 7, read 15, real PostgreSQL 19, total 41; controls 10, 4 and 7, total 21. At head 62 of 62.
- **Whole, on all three merged:** security 533 of 533, integration 177 of 177 (174 plus 2073's 3).
- **My plants:** absent allows (4 policy cells red; route cells stay green, because routes always pass an answer). No predicate (red in both). Revoke drops the answer (red). Tenant clause removed (red in the stand-in's SQL text cell only; on real PostgreSQL RLS still refuses, so the clause is a second lock).
- **My own error, in the open:** my first tenant-clause tamper also dropped the bind, so its 21 reds were a parameter error, not a detection. I discarded it and re-ran it with the bind kept.
- **One survivor, equivalent:** revoke branching on a raw truthy org. Mint stores a blank, tab or NBSP organisation as NULL (measured), so a blank stored org is not reachable by this route.
- **Odd inputs, MEASURED on real PostgreSQL:** blank, tab, NBSP and empty organisation: live 201, non-live 403, and revoke likewise. null 400. No tenant in the body, header tenant, other tenant: non-live refused every time. `rotate: true` non-live 403.
- **Call sites of the policy:** originate `adminConfig.ts:1180` passes no answer, unreachable by ADMIN (`requireRole` at `:45`). `connectorOrganisationErasure.ts:334` uses role `connector`. Neither is affected. READ ONLY.
- **Finding 1 of the PR, hunting a minter of an ADMIN token:** every `generateTokenPair` caller reviewed by location only, `platform_admins.role` CHECK has no ADMIN, `mapDbRole` has no ADMIN key. None found. Agrees with the seat; a read, so the claim "looks unreachable" stands as worded.

### Not tested
The gateway in front. A real login or token. The four platform suites. Any box. What a deploy map rebuilds for `packages/shared`. Whether a tenant-level key reaches more than an organisation key.

---

## PR 2073, KS-1152 R-880-1: rotated says when the old key lives

**BLUF.** The failed-retire shape is now honest, proved end to end for the first time below. One neighbouring shape still says `rotated: true` while the old key works.

**For Kam, at the top:** F1. His card asks about a retire that FAILS. Wednesday's F1 ruling adopts "is a number" and does not discuss zero. Whether 0 on an existing organisation should read as rotated is a ruling neither has made.

### Findings

**F1, MEDIUM. A count of 0 answers `rotated: true`, no warning, with the prior key still valid.** `services/api-gateway/src/routes/platform.ts:928,940`; the retire matches only `connector_id` (`services/security/src/index.ts:239`); pinned as correct by cell C1 (`ks1152-...test.ts:193`).
- MEASURED AT RUNTIME, real gateway route over real security on real PostgreSQL:
  - A prior key of the organisation minted through the public route with no connector id: 200, `rotated: true`, `priorKeysRevoked: 0`, no warning, and that key validates `valid: true`.
  - A prior key whose `connector_id` is NULL, the shape KS-869 says older rows hold (written by me as superuser): the same.
- The `priorKeysRevoked: 0` is honest; `rotated` is not what the operator will read it as. The spec's "True only when ... reported its prior keys retired" (`tenant-provisioning.openapi.ts:753`, and the yaml) is not true of 0: nothing was retired. The PR's table does state "a count (0 or more)", so this was visible, not hidden.
- Not measured: how many such rows exist on any box. A 0 on an organisation with truly no active key is legitimate, and the gateway cannot tell the two apart from the count alone.
- Old behaviour, not a regression. Recommendation, evidence class MEASURED AT RUNTIME for the shape, READ ONLY for prevalence: put it to Kam; do not hold this PR for it.

**F2, MINOR. The warning is false on a new organisation.** `platform.ts:165` says "the previous key could not be switched off and is still active". A rotate on a NEW organisation whose retire failed, or whose reply lacks the field, carries that text (cell R3 pins it), and there is no previous key. Read from the code and the cell; R3 ran. Rare, and it fails toward caution.

### The stitched probe the READY offered: done, and it holds
MEASURED AT RUNTIME, real gateway route and real security app in one process on real PostgreSQL, a real row lock (the gate 164 method):
- Clean rotate: 200, `rotated: true`, count 1, old key revoked, 1 active.
- Held lock: 200, `rotated: false`, `null`, `PRIOR_KEY_STILL_ACTIVE`, key returned; both the prior and the new key validate true.
- Retry: 200, `rotated: true`, count 2, the failed call's key revoked, 1 active.

So the retry hazard the warning names is real, and the "joined by the field's contract" limit in the body can be retired by this probe. The gateway's auth was a stub and its organisation lookup a fixture.

### Tested and held
- **Reds at develop:** 9 of 9 by assertion, 11 of 11 controls, 20 of 20 at head. Real PostgreSQL 3 of 3.
- **My plants:** `!== null` (3 red), warning without rotate (1), rotated on a new org (1), count must be positive (3, proving C1 pins the zero shape). No survivor.
- **Whole, all three merged:** gateway 1755 of 1755, tenant-provisioning 117 of 117.
- **Spec:** `generate-openapi --check` passes at this head and on all three merged. `additionalProperties: {}` is already open on that schema. The body's claim about `systemTest/schemathesis/tests/support/connector_keys.py:230` is true: it raises on not `true`, and it passes on a count of 0.
- **Consumers of `rotated`:** no other reader of this field in the tree. My grep's other hits are other meanings of the word.
- **Rulings:** the fields, "is a number", and the audit staying as is are Wednesday's, inside card b. Not wider than his option except F1's silence.

### Not tested
Platform S, another repository. A timeout between gateway and security. An unreadable thrown value on real PostgreSQL. A real grace window (`API_KEY_ROTATION_GRACE_SECONDS`). The four platform suites. Any box. Prevalence of F1's rows.

---

## Merge

- **On develop:** each PR's merge tree is clean. All three in sequence are clean; each pair is clean. **The batch shares no path.** Order among these three does not matter.
- **Against other branches, by merge-tree:** clean with 2060's and 2061's branches (KS 1536 3a, 3b), KS 1968, KS 1622, KS 2081, KS 1448, KS 2038.
- **Limit:** I found these by listing origin's 120 newest unmerged branches and filtering on shared paths. I could not read which PRs are open, because network is git only, and some listed branches may already be squash-merged.
- **Spec:** 2073's yaml passes the generator check on the merged batch. KS 2081, 1448 and 2038 also touch the yaml, so a clean text merge does not prove the generated file; whoever merges second regenerates, as Wednesday said.

---

## My own conduct

- **Fixed nothing, posted nothing, touched no box, no docker.** Network was git fetch and ls-remote only. Wrote only in this folder and /private/tmp/g245. Plus harness scratch for task output.
- **The clone: left in place, not removed.** The common rules say remove it; the QA template and my commission say never `rm` and leave it if forbidden. /private/tmp/g245 holds 9.4 GiB on the boot volume, for the coordinator's note. It has my probes, tampers restored, untracked probe test files, one local merge commit never pushed, and a disposable database's data and password file (never printed, the cluster holds only test rows).
- **The cluster is stopped,** by pg_ctl, its only process gone. Port 55745. I did not use the seat's cluster.
- **I read other seats' trees:** my walks of s-y6-sessend, s-y6-base and s-y6-ks1536 warmed those trees' caches. The next run there will look less cold. Nothing was written. The seat's own checkout and 2_Project_Files were read only, with no fetch there.
- **One command stopped:** a grep I started over all of 5_Project_History ran past its time, so I stopped it. It had also carried a red proof, which I re-ran.
- **A false zero, caught:** a `git grep -E` with `\s` returned nothing for `UPDATE users`. I threw it away and re-ran with POSIX classes and a positive control.
- **Load:** highest reading 6.24. Whole suites ran at 4 workers, not the seat's default, so my timings are not comparable to its figures on load.
- **Evidence:** raw results in /private/tmp/g245/out, probes in /private/tmp/g245/probe. They go when the clone goes.
- **Charter's "environment confirmed with a human":** no running target exists here; everything ran in my own processes. No credentials were used beyond the repo's configured deploy key, by path.
