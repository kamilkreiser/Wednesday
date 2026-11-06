# Gate 251, tier 1, round 1 of 2: verdict

| PR | head | verdict |
|---|---|---|
| 2087 (KS-1600 item 3) | 954af815c7b71497485c71fd3321f015650ef512 | **GO WITH NOTES** |

Severity is mine; priority is not. 0 Critical, 0 Major, 4 Minor, 4 Info, 1 curio.

**For Kam's eye, not a blocker by my severity (F1):** `permissions: null` stays a 201 at originate while the security service refuses it. That sits inside the ticket's four named shapes but short of the plain words of his card, "Refuse with 400, matching the security service". It is Wednesday's answer, not his, and it is narrower than his card, not wider. One line from him settles it.

Head readings, all on detached HEAD in my clone, read from origin by `ls-remote` (no builder in my tree):
- start 21:07:38Z: 2087 `954af815c7b7`, 2060 `796ea55fb8eb`, develop `b27f5fb30f4a`
- mid 21:22Z: the same three
- end 21:25:07Z, after this file was first written: the same three.

## BLUF

The change does what it says. A present `permissions` that is not an array of strings answers 400 before any database call, through originate's real middleware stack, for both caller classes, on 46 of 46 cells. The gateway does not rename the field: it forwards the body byte-identical. Nothing mints wider than it asked except the declared `['read']` fall-back, which this PR does not widen. Merged with PR 2060, the tree is clean and all 17 cells pass. The defects are in claims and test coverage, not in the code path.

## Answers to the five asks

### 1. Does the gateway rename it? Can anything mint wider than asked?

**No rename. MEASURED AT RUNTIME** (`evidence/10_*`, `evidence/12_*`): the real gateway app in-process, NODE_ENV=test, against a fake originate on loopback. FAIL condition, stated first: one byte differing at the upstream. 6 bodies on 2 paths (`/api/admin/api-keys` and `/api/v1/admin/api-keys`), 12 of 12 byte-identical on both the PR head and the merged tree, including `scopes`-only bodies, duplicate keys, odd spacing and `<`/`&` (so the gateway's HTML sanitizer did not run either). Why, by reading: `/api/admin` is in `proxyPaths` (`services/api-gateway/src/index.ts:397`), so the body is never parsed, and the mount at `routes/proxy.ts:1265-1269` rewrites only the path. A form body answers 415 at the gateway and forwards nothing.

The seat's sentence holds: a body with only `scopes` becomes `['read']`. Measured through the real stack with `['documents:read']`, `['*']` as SYSTEM_ADMIN and as ORG_ADMIN, a malformed `scopes`, and `permissions: []` beside `scopes: ['*']`: every one stored `["read"]`.

**Wider than asked: no new path. MEASURED AT RUNTIME** (`evidence/02_*`), FAIL condition F2 in the probe's header. Only the declared fall-back stores a scope not asked for: absent, `null`, `[]`, `scopes`-only all store `["read"]`. Note `[]` and `null` are nominally wider than a request for nothing, where security stores `[]`. READ ONLY: a search of the gateway's source, `packages/shared/src/security` and originate's middleware for a bare `'read'` finds only security's own default (control: `documents:write` found in 4 of the same files), so bare `read` appears to open no gate there.
Also measured: whitespace-padded and upper-case `organizations:register` from an ORG_ADMIN with no org are 201 and stored verbatim, the same as security would accept; `hasScope` is exact-match, so READ ONLY they grant nothing. `['*']` and `['organizations:*']` with no org are 403. `['*']` naming the caller's own org is 201: what it asked for, pre-existing, ruled on another card. `__proto__` and `constructor` keys store `["read"]`. Duplicate keys: the last wins, and only one parser reads the body, so there is no differential.

### 2. The two differences: inside Kam's words?

Card text: "a malformed permissions value gets a 400 at the security service, while originate falls back to read-only or stores it inertly"; option a, "Refuse with 400, matching the security service". The ticket lists four shapes: a bare string, a nested array, `[null, …]`, an object. Security's schema expression at `services/security/src/index.ts:718`, driven directly in zod (`evidence/15_*`; its route's 400 at `:1550-1551` is READ ONLY): refuses `null`, stores `[]`, defaults absent to `['read']`. So the seat's sentence is right.

- **`[]`: inside.** Security does not refuse it, so it is not malformed on either reading. Nothing is owed.
- **`null`: see F1.** Not in the ticket's list, but it fits the card's sentence exactly: 400 at security, read-only fall-back at originate.
- Number and boolean are refused though the ticket does not name them. That is inside the card, since security refuses them too. Not wider.
- The PR, the commit and the flow fragment all say the carve-out is Wednesday's, not Kam's. True per `mail/in_01_answer_plan_FILE.md`.

### 3. Callers: are 0 production senders right?

**Yes in this frame. Frame:** predicate = a request to originate's `POST /api/admin/api-keys` carrying `permissions`. Tree = origin/develop `b27f5fb30f4a`, the same tree the seat searched, and all text files. Instruments = `git grep -F admin/api-keys` (63 lines in 29 files, reproducing the seat's count exactly), and `/usr/bin/grep -E` on `api-keys` across ts, tsx, js, py, sh, yml and json outside `__tests__`, then each site read.
Result: 0 production callers. The admin UI posts to `/api/security/keys` with `scopes` (`frontend/admin/src/services/api.ts:411`, `pages/ApiKeys.tsx:177-180`). 5 test and tooling files, all string arrays: `repro-api-keys.sh:112`, `ks-4-phase5b-reconcile.api.spec.ts:242,341,407`, `path-spelling.client.ts:151` (typed `string[]`), `setup_api_key.py:117`, `test_tenant_isolation_writes.py:227`. Originate's tests: 23 `permissions:` lines at develop, as the seat says. I read the KS-1594 file's payload lines and the forged-tenant file's one; all string arrays. I did not read the rest one by one.

**Frame I added, which the seat lists as unmeasured:** local read-only checkouts of `platform-s-main`, `Extranet` and `Testing Harness and Agent`: 0 hits on the route, against controls of 9, 2 and 9 files mentioning an API key. These checkouts may be stale; I read no remote.

**Still unmeasured:** customer scripts and live traffic. `USER_TESTING/Stuart_PlatformS_PlatformK_integration_followup.md:131` names this route to Platform S and "a customer's admin", so an outside audience is documented. It gives no body shape and recommends the OAuth path. F2 is about the instrument offered for this gap.

**Who loses access:** only a SYSTEM_ADMIN or ORG_ADMIN sending a malformed value: a 201 becomes a 400. No caller in any frame above does.

### 4. Where the refusal runs, against what

`services/originate/src/routes/adminConfig.ts:999-1002`, inside the handler, after the KS-1206 rateLimit check (`:987`) and the name check (`:990`), before `requestedScopes` (`:1015`), the org decisions (`:1023-1067`), key generation (`:1070-1071`) and the INSERT (`:1092`). Read at that point: `req.body` only, nothing written by the handler. Ahead of it (READ ONLY): gateway auth and role check, originate's overload guard, body parsers, NUL guard, `authenticate()` and `requireRole`.

**No insert on the refused path: confirmed. MEASURED AT RUNTIME** (`evidence/02_*`) through the real `index.ts`. Spies on `$queryRaw`, `$executeRaw`, `$queryRawUnsafe`, `$executeRawUnsafe` (`$transaction` is absent on this client's interface, recorded in the output). 23 shapes across 2 caller classes: all 400, 0 calls, no key returned. Positive control: the same instrument reads 201, one call and the stored scopes. On develop the same 23 shapes all answer 201 with one call (`evidence/05_*`). The seat's RED holds: 11 of 11 red, 10 on 201 and 1 on 403, 6 controls green (`evidence/04_*`).

Order at the head: a malformed value with a missing name answers "name is required"; with a bad rateLimit, the rateLimit message; with a non-string `organizationId`, the permissions message. All 400, no call. Comment `:994` says "before anything else reads it", which is true of `permissions`.

### 5. Merge with PR 2060

`git merge-tree --write-tree` both ways: clean, tree `eecb2bad1aba`, equal to the seat's. A real merge commit in my clone (`5cf0532bc6a0`, not pushed) has that same tree. Shared package rebuilt from the merged source, rc 0. **The file's cells on the merged tree: 17 of 17** (`evidence/07_*`). The real-stack probe gives 83 rows identical to the PR head (`evidence/08_*`). Whole originate suite on merged, default workers: 220 suites, 2601 tests, all pass (`evidence/09b_*`). PR 2060's hunks sit at old lines 60 and 78, this PR's at 990. Merge order is free: same tree both ways. PR 2060's base is behind develop (merge-base `c5c26b2835df`), so the READY's "whichever merges second merges develop in" stands.

## Findings

**F1, Minor, needs Kam's eye. `null` is carved out of "matching".** `adminConfig.ts:999`; pinned by the test's cell at `:109`.
FOUND: `permissions: null` answers 201 `["read"]` at originate; security's schema refuses it. TESTED: `evidence/02_*`, `evidence/15_*`, both MEASURED AT RUNTIME. HOW: same value through both rules.
For the carve-out: not in the ticket's list, disclosed in the PR, and this route's `organizationId` already treats null as absent (the ticket calls that ruled, mutant R7; I did not read that ruling). Against: the card's sentence. Oracle: Purpose (the card's words). Recommendation, READ ONLY as to Kam's intent: ask him one line; no code change unless he says so. If he says refuse, the owner flips one condition and that control.

**F2, Minor. The census the PR offers for the outside-callers gap cannot see half the ticket's shapes.** PR body, "Callers", and READY item 5: a census of `svc_api_keys` rows whose `scopes` are not an array of strings "would show a past malformed mint".
FOUND: on develop, 11 of the 23 malformed shapes store a perfectly ordinary `["read"]`: every bare string (`""` included), object, number and boolean. That covers 2 of the ticket's 4 named shapes. Only array-element shapes leave a mark. TESTED: `evidence/05_*`, MEASURED AT RUNTIME. HOW: the stored value read from each INSERT.
A clean census therefore cannot clear a caller sending `permissions: "read"`, the likeliest real mistake, and a deploy seat would read 0 as "no malformed callers". Oracle: Image/Purpose, a measure that reads as more than it measures. Recommendation, MEASURED AT RUNTIME: the owner states the blind spot in that sentence. No instrument in hand covers it; live request bodies are not logged by anything I read (READ ONLY, not searched exhaustively).

**F3, Minor. The test file's own header says it never ran.** `ks1600-malformed-permissions-refused-at-the-admin-mint.test.ts:4`: "DRAFT by Seat V 26th, NOT YET RUN (no tree existed when it was written)", shipped at a head where it runs 17 of 17. `:109`'s cell title says "pending Wednesday" and `:17` "widening is hers", though she answered. FOUND by reading; TESTED: its run. Oracle: Product, the file contradicts itself in a PR a client's developer reads. Recommendation, READ ONLY: drop the draft provenance, say what it is now.

**F4, Minor. Falsy malformed values are correct in the code and unpinned in the file.** My planted mutant `if (d.permissions && !(...))`, the natural tidy-up of that condition, makes `""`, `0` and `false` skip the check and mint `['read']` silently: the exact behaviour Kam ruled out. **It survives: 0 of 17 red** (`evidence/03_mutants.txt`, G2, predicted in advance). The head itself is right on all three: 400 (`evidence/02_*`). Described regression test: three more `MALFORMED` rows, `''`, `0`, `false`, each 400 and 0 inserts; they should red that mutant. MEASURED AT RUNTIME.

**F5, Info. Two sentences a client will read are looser than the code.** (a) The PR body says the refusal comes before the 403 decisions "as the security route also validates before it authorises". Its role gate `requireKeyAdminOrProvisioner` runs before the parse (`security/src/index.ts:1266`, its own comment at `:1314`), so it is true of the org decisions only. Originate has the same shape. (b) The cheat fragment says a malformed value "used to mint a read-only key silently". That is true of 11 of 23 shapes; array shapes were stored as given, as the flow fragment correctly says.

**F6, Info. `docs/SCOPES.md:112` goes slightly stale on merge.** "originate's `POST /api/admin/api-keys` stores whatever it is given" is no longer true of non-strings. Not in this PR's four paths.

**F7, Info. "Whether the gateway renames the field is not measured" can now be answered.** True of the seat; the PR body and READY could cite this gate's measurement instead. The owner's call.

**F8, Info, pre-existing, not this PR. Latent collision on develop.** `ks488-smtp-opt-in.test.ts` and `ks1937-email-service-logs-never-carry-the-recipient-address.test.ts` are both module-less scripts declaring `EmailModule` and `saved`, so ts-jest fails whichever loads second in a worker with TS2300/TS2451. Replicated: on merged with `--maxWorkers=2` ks488 fails (`evidence/09_*`, and `09a_*`), and on plain develop in-band ks1937 fails (`evidence/09c_*`). Default workers pass (`evidence/09b_*`, `evidence/11_*`), which is why nobody has seen it. A low-core CI or an in-band run reads red for no reason. Filed nowhere by me.

**Curio, not a defect, not chased.** In NODE_ENV=test the gateway forwarded `/api/v1/admin/api-keys` upstream with its `/api/v1` prefix (seen on both trees), and I found no `/api/v1` in originate's source by a search of its non-test ts files. Whether that matters in production, where `versioningMiddleware` redirects, I did not establish. Nothing to do with this PR's diff.

## Test quality

Reproduced from the seat: RED 11 and 6, breakdown 10 and 1; mutants delete (11), `Array.isArray` only (6), after the 403 decisions (1), all equal to its declared sets; whole originate suite at the head 219 suites, 2596 tests, exact; `tsc --noEmit` rc 0; docs-fragments check rc 0. The other six mutants I did not rerun. No cell I examined passes for the wrong reason: 10 of 11 RED cells assert the message too, and moving the check after the INSERT reds 11 (G5), so the insert count is live.

My own mutants, predictions written before running (`evidence/03_mutants.txt`): G3 non-platform only 10; G4 platform only 1; G5 after the INSERT 11; G6 null elements allowed 2; G7 nested allowed 1: all matched. G1 `every`→`some`: predicted 4, measured 5. **My prediction was wrong, not the file:** `[].some()` is false, so `[]` is refused and that control reds too. Survivors: G2 (F4); G8, refusal body loses `success:false` (Info); G9, refuses `['']`, stricter than security (Info).

## PR body and ticket comment

Read `drafts/pr_item2_body.md` in the seat's record: the network rule stops me reading GitHub, so **I did not confirm it equals the live PR body**. Tested true: the +10 and 17-cell counts (4 files, +170/-0), line 718, the callers counts as framed above, the overlap and tree id, and every "unchanged on purpose" sentence. Loose: F2, F5a. No ticket comment draft exists in the seat's record, so there was none to test; the KS-1600 record is the board seat's after merge.

## What was NOT tested

- The database-backed KS-1594 cells, and any real PostgreSQL. PostgreSQL 15 is on this host, but they need a migrated platform and tenant schema, plus a generated Prisma client absent here. NOT RUN, blocker named. Risk read as low (READ ONLY): the guard is before all SQL and every KS-1594 payload is a string array.
- A lone surrogate inside a string element (`["\ud800"]`) reaching the `::jsonb` cast: passes the guard; a 500 is possible on real PostgreSQL. Untested either way. Security's door may behave alike; not checked.
- Security's real route was not driven: its schema expression was, in zod. Its 400 mapping is READ ONLY.
- Multi-tenant mode through the real stack; the real gateway plus real originate end to end; NODE_ENV=production; node:24; hook legs 3, 4, 8; eslint; the four platform suites (NOT COMMISSIONED, no stack allowed).
- The spies cover the Prisma-style surface, not a raw `pg` pool. READ ONLY, the handler uses none on this path. Gateway audit writes on a refused request not measured.
- Other open PRs on these paths: not readable under the network rule. The seat's overlap gate names only 2060 (`evidence/item2_overlap_01.out`); not re-run.
- Live traffic, customer scripts, Kintsugi and demo rows.

## My conduct

Network: git clone, fetch and ls-remote only. Nothing pushed or posted, no box, no docker. Fixed nothing. Writes: this folder and `/private/tmp/g251`. Read-only reads in the seat's record, its worktree (node_modules and the shared package's `dist` copied from it, which needed no write there; lockfile for root and originate checked identical) and sibling Secuura checkouts.

**Clone left in place per the commission's correction to the common rules: `/private/tmp/g251`, 2.1G.** It holds a local merge commit not reachable from HEAD, and three untracked gate items: `g251-gate-probe.test.ts`, `g251-gateway-body-probe.test.ts`, `_gate/`. It is detached at `954af815c7b7`, with `adminConfig.ts` restored (sha256 asserted after mutants, git checkout after the develop run).

Mistakes of mine, none surviving: (1) my first whole-suite flag overrode the config's integration ignore; that run is kept as `evidence/09a_INVALID_*` and redone. (2) My gateway probe first counted JWKS fetches as forwarded bodies; fixed by filtering them, and the row content had already shown it. (3) A first sibling-project census printed nothing even on its positive control, so I discarded it and re-ran with a wider control. (4) G1's prediction, above. A hook refused a `git -C $G checkout` written with a variable; I re-sent it with the clone's literal path, which is my own clone and within the hook's rule. Peak load 5.81, under 8.
