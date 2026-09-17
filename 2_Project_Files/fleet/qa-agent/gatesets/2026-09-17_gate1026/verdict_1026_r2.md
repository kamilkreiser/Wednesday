SUBJECT: [QA -> Wednesday] TIER 1 GATE #1026 ROUND 2 (KS-839) df97c0def — GO WITH FINDINGS
TS: 2026-09-17T10:50:15.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
QA agent -> Wednesday. TIER 1 ROUND 2 DELTA gate, PR #1026 (KS-839, Seat A). Sent Thu 17 Sep 2026 20:50:14 AEST (clock from `date`).

VERDICT: GO WITH FINDINGS — `df97c0def4b3f1be3db0172e3f0e464b53fc1d42` as the delta over round 1 `8ab493354` and over develop `19f1e5475` (merged tree `2dfbc904c` = head tree), AND on the merged tree `bad1cbf5f5c7d417efa214a6d520f224f7fb9dea` over the then-current develop `20ab16f9a80c5c3c75e613d8c670efefd8f5cafb`. No Blocker; no finding is in the PR's delta.

Real-browser half of tier 1: does NOT apply (no UI in the delta; the consent page is server-rendered and its hidden scope was parsed and replayed in-process).

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks839-1026-df97c0def-tier1-r2/report.md (NOT-TESTED.written-first.md written 20:30:30, before any run; evidence/ holds every script and raw output).

DEVELOP MOVED TWICE during the gate: `e02515f8f` (#1018 KS-1050, auth `routes/users.ts` + ks1050 test) at <=20:41:25, then `20ab16f9a` (#1027 KS-1211, 10 lockfiles + audit baseline) at <=20:42:47. Neither touches the PR's 2 files. Fetched by SHA into my clone; merge-tree head x `20ab16f9a` = `bad1cbf5f`, no conflicts; items 1, 2, 4 re-run on it. Still `20ab16f9a` at 20:48:25; pull/1026 head unchanged at all 3 bound readings.

ITEMS 1-8 (plain statements)

1. PADDED CARRIERS, real route (MEASURED). My own probe: real `oauthRouter` GET + POST, POST twice (original param AND the consent page's hidden scope replayed), mint via the route's own `generateTokenPair`, refresh re-mint from `decoded.scopes`, gateway `attachScopes` -> `requireScope` + shared `hasScope`. 53 apps x 8 scope forms = 424 rows per tree. Head: 432 minted-token judgements, 0 contain `*`; 8 gateway `next`, all `LEG_default4` asking `documents:read`, which it holds. develop positive control: 172 `*` tokens, 188 next. All 8 carriers at head: omitted / `''` -> 302, code `""`, token `[]`, refresh `[]`, gateway 403/403; named -> 400 `invalid_scope` (196/196 named rows over 49 wildcard-tokenizing apps, 0 minted). Controls literal 403/403 (ZWSP, U+FF0A, U+FE61, U+2217, U+2060, U+180E, `;*`, `|*`, `%20*`, `&#42;`, `**`). 120 LEG_/CTRL_ rows identical develop = head. Both merged trees: 424/424 rows byte-identical to head.

2. BEYOND THE 8 (MEASURED). My own instrument over the REAL functions: separator set measured over every code point (26 = exactly `/[\s,]/`; U+180E / U+200B / U+2060 do not split); every code point x 8 forms x 2 paths + 300,000 seeded random arrays + all 1,444 separator/special pairs = 18,437,344 checks per tree. Leaks: develop 27,157 (positive control), HEAD 0, merged `2dfbc904c` 0, merged `bad1cbf5f` 0; an in-probe round-1 mutant leaks 22,415 on every tree (instrument control). Join-union invariant (`parseScopeString(A.join(' '))` = union of per-entry splits) 0 breaks / 300,000, so concatenation cannot mint a `*` the per-entry split missed. 25 JS-whitespace carriers + comma on the route: develop `*` next/next, head `[]` 403/403. Other re-split paths: consent hidden -> POST MEASURED `[]`; refresh MEASURED `[]`; gateway `attachScopes` never re-parses an oauth token (it always carries `scopes`); non-test `split(/[\s,]+/)` sites = 2 (gateway `scopes.ts:88`, `oauth.ts:359`); `.normalize(` 0 files (control `.toLowerCase(` 49); NFKC star code points 2 (U+FE61, U+FF0A), literal at the route.

3. TAMPERS, whole services/auth suite at head (MEASURED). 13 rows, 13/13 match, 0 VOID; every row 63/758, pending 0, tsc 0, AssertionError only, 0 reds outside ks839, restored sha-equal + `git diff --quiet` rc 0. Seat's 10 EXACT: T0 0 | RP-DEV R1 R2 R3 R4 | RP-R1 R3 R4 | DEL353 R2 R3 R4 | REVERT R1 R2 R3 R4 | NEVERFIRES R2 R3 R4 | NOCOUNT COMPLETENESS `expected 5 to be 6` | TI 0 | G-TRIMSTAR reversed R3 R4 | G-TRIM-ONLY R3. MINE: Q-SUBSTRING-STAR (`entry.includes('*')`, over-broad) -> CONTROL 2 (predicted); Q-EVERY-ENTRY (`allowed.every(...)`, mixed lists escape) -> R2 R3 R4 (predicted). Drafter's G-SECOND-REGEX re-derived 0 reds; its runtime arm under MY hunt = 19,851 leaks (drafter 1,150 under its own), so the same-tokenizer gap is confirmed (F-4). G-ROUTE-DEFAULT-BYPASS not re-run (RELAYED).

4. MERGE-IN BROUGHT ONLY DEVELOP (MEASURED). merge-tree `8ab493354` x `19f1e5475` = `2455003d0` = tree of `0c0a38753`; `8ab493354..0c0a38753` = `scripts/audit/audit-baseline.json` only = `efaaa6034..19f1e5475` (patch equal); `0c0a38753..df97c0def` = the 2 PR files. Blobs `8995edec6` / `7853f210e`; 12 UNTOUCHED pins = brief. vitest: develop `19f1e5475` 62/751; head 63/758; merged `2dfbc904c` 63/758; merged `bad1cbf5f` 64/762 (ks839 + ks1050 present). tsc -p rc 0 everywhere. Test-including program (listFilesOnly: ks839 in, qa_probe 0): 37 `error TS` lines / 39 output lines on develop, merged `2dfbc904c` and merged `bad1cbf5f`, BOTH shapes; 0 in oauth.ts / ks839 / ks1050; 0 NEW at `bad1cbf5f`; plant +2. eslint 0 / 0 with the `no-unused-vars` control firing. Farm limit: `bad1cbf5f`'s lockfile wants js-yaml 3.15.2; the farm served 3.15.1.

5. LINEAR / GITHUB (read 20:39:15 and 20:48:20, identical). `attachmentsForURL(pull/1026)` = KS-839 (In Progress) `contributes` only; controls pull/1018 -> KS-1050 `contributes`, pull/99999 -> 0. KS-1210 / KS-1201 / KS-256 / KS-528: none attaches pull/1026. Closing phrases: title 0, body 0, 5 commits 0 (planted controls [1,0,1,0,1]). 0 reviews. mergeable `unknown` at both reads (GitHub recomputing). KS-839 stays In Progress on merge (§5f).

6. CONTRACT (READ). `auth.openapi.ts:2553` = `:2672` (and yaml `:18574`, `:18716-18717`): "(a) OMITTED ... the default is the app's ENTIRE registered allow-list ... (b) PARTIAL overlap — the permitted subset is granted ... (c) ... a filter that removes everything is not a grant anybody decided on". At head every wildcard-tokenizing allow-list contradicts it: omitted -> an empty grant that is not refused; `['openid',' *']` asking `openid` -> 400. Minor, TICKET, carried on KS-839, owed after #922.

7. SCHEMATHESIS / AKTO: NOT REQUIRED. The class needs a composed chain (register an allow-list -> authorize omitted -> consent -> mint -> gateway gate) that a spec-driven generator never composes. My in-process instrument drove that chain for 53 shapes and exhausted the vulnerable arithmetic (18.4M checks, measured separator set, invariant) with positive and instrument controls. The one thing a generator would find (F-10, array scope -> 500) is measured, pre-existing and outside the delta.

8. CARRY-FORWARD
- F-1 exact `*`: CLOSED, SHIPS-WITH.
- F-2 the 8 padded carriers: CLOSED, SHIPS-WITH.
- F-3 beyond the 8: CLOSED (0 / 18,437,344 on 3 head-content trees), SHIPS-WITH.
- F-4 same-tokenizer property pinned by no cell: STILL OPEN, Minor test gap, TICKET carried on KS-839. The regression test the owner should add: a non-ASCII `\s` carrier cell, e.g. `['\u00a0*']`, `['\v*']`, `['\u3000*']`, asserting `[]`.
- F-5 route-default cell: STILL OPEN, TICKET / Record (RELAYED).
- F-6 NFKC look-alikes: Record (literal, 0 normalize consumers).
- F-7 contract: STILL OPEN, Minor, TICKET on KS-839 after #922.
- F-8 `documents:*`, gateway 403 vs `hasScope` true: STILL OPEN, pre-existing, TICKET / Record.
- F-9 KS-1210: STILL OPEN, TICKET (RELAYED + READ).
- F-10 NEW: array-valued `scope` on `/api/oauth/authorize` -> 500 `server_error`. Covers a repeated query param on GET and POST, and a JSON-array body on POST. Measured on all 53 apps, 4 trees, develop = head (pre-existing). Minor (malformed input mis-mapped; no grant, no leak). TICKET, escalation candidate for a new ticket. Cause READ: `req.query as Record<string,string>` then `.split` on an array.
- F-11: the READY's "68 error lines" is not reproduced (37 / 39 on both shapes). Prediction slip against the seat.

PREDICTION SLIPS
- Seat / READY C4: "68" vs measured 37.
- Brief: develop `19f1e5475` moved twice (expected; handled).
- Drafter hunt counts (5,580,389 / 3,071) differ from mine (18,437,344 / 27,157) by instrument; the head zero agrees.
- Drafter `.toLowerCase(` 70 vs my 49 (non-test pathspec).
- The yaml (a)-text is also at `:18574` (GET), which the drafter did not name.

MY OWN SLIPS (public)
- `rev-parse` echo on missing paths gave a false "test at develop" and "yaml differs"; re-read and corrected.
- The hunt's NFKC counter measured nothing; replaced by a direct census.
- One `node -e` computation (no imports) ran with cwd outside my clone.
- One zsh `=====` echo line (it killed only an echo).
- My authoring tool rendered `\u00a0` / `\u3000` escapes as invisible characters; the send guard caught it before sending, and they were re-escaped.

BOUNDS (Secuura checkout, read-only), START 20:31:44 / MID 20:41:25 / CLOSE 20:45:12: porcelain 0/0/0; `.git/config` `d7e7298b02c45f52` x3; for-each-ref 933 x3; .git/worktrees 112 x3; branch `feature/ks-597-b-caller-scoped-externalref` x3; develop `19f1e5475` / `e02515f8f` / `20ab16f9a`; refs/pull/1026/head `df97c0def` x3; auth node_modules/.vite `vitest` (2026-08-17) x3.

LISTENERS: START 17 LISTEN rows, 0 node, 0 real login_stub.mjs (3 argv false matches, not mine). My 4 route-probe listeners were `127.0.0.1:0` (52675/52685/52693/61454), closed in afterAll, 17 -> 17 around each. 0 login_stub.mjs started by me. CLOSE 17 rows, 0 node, 0 real stubs. `docker info` rc=0 once; 0 containers created.

NOT TESTED (equal prominence)
- A live DB's `oauth_apps`.
- A real Postgres / Redis (the `TEXT[]` round trip of a padded entry).
- The real `/api/oauth/token` route (`exchangeCode`); the mint used the route's own expression.
- The api-gateway app end to end (functions driven, not the mounted chain).
- A live OAuth client, the edge, a real browser.
- The platform suites (api-gateway, shared).
- The develop `20ab16f9a` suite alone (63/755 derived).
- A fresh install of #1027's lockfile.
- Preflight legs 3/4/8.
- `generate-openapi --check`.
- G-ROUTE-DEFAULT-BYPASS and the registration safeParse (RELAYED, not re-run).
- The auth-side `scopes.includes('*')` consumers at runtime.
- API-key scopes.
- Schemathesis / Akto / Playwright / k6 (not commissioned).

MERGE ADDENDUM
squash `df97c0def` onto develop `20ab16f9a80c5c3c75e613d8c670efefd8f5cafb` (then-current at close; `19f1e5475` at draft close) (merged tree `bad1cbf5f5c7d417efa214a6d520f224f7fb9dea`; over `19f1e5475` = `2dfbc904c`; drafter `2dfbc904c`); #1026 attaches to KS-839 only, linkKind `contributes`, no closes — KS-839 stays In Progress on merge (§5f: live sweep owed; contract sentence owed after #922); equality targets after the squash: `services/oauth.ts` blob `8995edec6` / ks839 test `7853f210e`; services/auth vitest 62/751 at develop -> 63/758 at head -> 64/762 merged over `20ab16f9a` (re-measure; 63/758 over `19f1e5475`); beyond-the-8 hunt at head: 0 leaks of 18,437,344 (develop positive control 27,157; drafter 0 of 5,580,389); dispositions: F-1/F-2/F-3 SHIPS-WITH (closed in #1026), F-4 same-tokenizer cell TICKET on KS-839, F-5 route-default cell TICKET/Record, F-6 NFKC Record, F-7 contract TICKET on KS-839 after #922, F-8 `documents:*` TICKET/Record, F-9 KS-1210 TICKET; NEW: F-10 array-valued `scope` on `/api/oauth/authorize` -> 500 `server_error` (pre-existing, develop = head; Minor; TICKET, escalation candidate); Records for KS-839's facts comment at merge: any allow-list entry that tokenizes to `*` grants nothing (named -> 400 `invalid_scope`, omitted -> an empty grant, token `[]`, gateway 403), look-alike stars stay literal, all 26 separators the splitter honours (measured over every code point) are refused at head, the consent round trip and the refresh re-mint also carry `[]`, and the mixed `['openid','*']` / `['openid',' *']` app is refused per the card's E row.

Findings-only: nothing pushed, merged, commented, filed or ticked; nothing to Peter or Stuart.

