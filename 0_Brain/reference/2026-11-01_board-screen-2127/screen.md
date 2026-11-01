# Board screen 2026-11-01 21:27 (read-only; Secuura / Distributed_Secuura)

Basis: develop d7691f35312ea158f043e87a3227e477cccb183d (ls-remote origin develop still equals it). Local clone read with git show/grep only (a fetch was refused by the no-write hook, not needed).

## 1. Open tickets by state
Predicate: Linear GraphQL, `issues(filter:{state:{type:{nin:["completed","canceled"]}}})`, first:100 with cursor paging until hasNextPage=false, all teams. Total 970.
- KS: Backlog 414, In Progress 320, In Review 52, Todo 24, Blocked 3, Duplicate 1 = 814
- PS: Backlog 82, Todo 41, Duplicate 14, In Progress 11, In Review 6, In Test 2 = 156
CAVEAT: "In Progress" is not "held by a seat". Spot check of four In Progress candidates (KS-1840, 1842, 1799, 1911): each has a PR comment and no open PR, i.e. merged and awaiting ticket closure. I treated In Progress as taken and drew candidates from Backlog only.
Open PRs: 19 (pulls API, per-PR files API, 60 distinct files). Positive control: package.json/lock and users.ts rows appear, so the scan returned data. None of the candidate files below is in it. Dependabot/revert PRs touch every service package.json and lock: no lane edits those.

## 2. SEAT CANDIDATES (all Backlog, no Kam/Peter/Stuart input, none prod/money/comms/deploy)
Exclusions never touched: persona.ts, governanceService.ts, minting.service.ts, KS-1384. Paths under Blockchain/Dev/.

LANE 1 - KS-1885 (Tier 1: auth/identity). "Social sign-in callback echoes any exchange error whole". BLUF: GET /api/auth/social/:provider/callback puts exchangeErr.message into the 400 body unless it is a SyntaxError; a newline in access_token makes fetch throw a TypeError whose message contains the token (QA gate 43: github, google, linkedin, microsoft_personal exposed; facebook not).
 Files at develop: services/auth/src/routes/auth.ts (:1076-1081, the `detail` line) + one new test in services/auth/src/__tests__/. Adapters in providers/social/* need no edit.
 No external input: fix shape is the constant-detail pattern KS-1791 already used on the same lines. Not in an open PR (auth PRs touch only routes/users.ts and one ks1006 test).

LANE 2 - KS-1901 + KS-1893 (Tier 2). mcp-server leaks thrown text. 1901: /register-batch and /verify-batch catch blocks copy err.message into results[i].error under HTTP 200 (http-server.ts:105-106, :166-167, unguarded message read). 1893: secuura_hash_document returns raw fs error text (tools/hash.ts catch, already has the 'unreadable thrown value' guard but still returns message).
 Files: services/mcp-server/src/http-server.ts, services/mcp-server/src/tools/hash.ts, 1-2 new tests in src/__tests__/ (ks1410 and ks1868-hash-tool tests exist as templates; the ks1868 hash test may need its expectation updated).
 No input: 1901's fix shape (log, answer constant `An unexpected error occurred`) is the one already merged for the 500s in KS-1410.

LANE 3 - KS-1867 (+ KS-1865, same file) (Tier 2). check-no-sql-injection.sh matches one line at a time, so 3 multi-line interpolated *RawUnsafe templates are unreported; and its `grep -v` post-filter (line 34) matches anywhere in the hit line. Files: scripts/check-no-sql-injection.sh + new/edited scripts/__tests__/check_no_sql_injection_*.test.sh. Part (b) of 1867 (trace 3 sites: packages/shared/src/db/optimization.ts:105 and two more) is read-only analysis in the PR body, no edits to those sites. Needs the ticket's table of the other two sites (not read here).

LANE 4 - KS-1815 + KS-1812 (Tier 2, test-only). 1815: ks726 :414 cell uses a paraphrase ("All inputs are spent") instead of the real node reply (ks705 ALREADY_INCLUDED), so deleting the ALREADY_INCLUDED_REPLY clause in anchorSubmission.ts is unpinned. 1812: no cell pins the pattern clause of didJwkRefusal's early return (anchorSchema.ts:166); mutant survives 183/183.
 Files: services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts (or a new file), services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts. No product file edited. Both tickets carry the mutant to re-run as acceptance.

Pairwise disjointness (file sets): L1 {auth/routes/auth.ts, auth/__tests__/new}; L2 {mcp-server/http-server.ts, tools/hash.ts, mcp __tests__}; L3 {scripts/check-no-sql-injection.sh + its tests}; L4 {anchoring ks726 test, anchoring ks1175 test}. Four different services/dirs, zero shared paths; none shares a path with the three excluded files or the 60 open-PR files. Spark list below shares no path with these lanes either.
Tier: L1 = 1; L2, L3, L4 = 2.
Tickets I looked at and rejected: KS-1873 (users.ts is in open PRs 1796/1798); KS-1795/1793 (their test files are in open PRs 1790/1792); KS-1890/1882/1881/1883 and the billing/nft/anchoring authz tickets (tier 1 design/rulings, too large); KS-1909/1782/1785 (ops/money/external).

## 3. SPARK CANDIDATES (one file, mechanical)
1. KS-1903, scripts/check-dockerfile-non-root.sh:27,32. Last USER of `root:root`, `0:0`, `ROOT` passes. Diff: after the `tr -d`, `last_user=${last_user%%:*}` and lowercase via `tr A-Z a-z`; test case lines go in the existing scripts/__tests__/check_dockerfile_non_root_reports_root.test.sh (second file, test-only).
2. KS-1902, scripts/check-akto-container-names.sh (PATTERN, ~line 82). `-u root` / `-e FOO=1` before the name pass. Diff: allow an optional value token: `(([[:space:]]+-[^[:space:]]+)([[:space:]]+[^-[:space:]][^[:space:]]*)?)*`, or match akto-<name> anywhere on a docker line; cases added to check_akto_container_names_flags.test.sh.
3. KS-1898, services/vc-issuer/src/__tests__/ks1851-credential-revoke-bound-to-the-creator.test.ts:239-256. Test-only: add `expectByteIdentical(refused, unknownIdRefusal)` plus the logger assertion to V8b-e and V9, and a memory-path owner-less cell (copy of :164-176).
4. KS-1796, services/auth/src/auth.openapi.ts:1012. Add `422: { ...commonErrorResponses[422], description: 'New password too weak' }` and change the 400 text to 'Wrong current password'; sibling reset-password (:813) is the citable source. NOTE: docs/openapi/secuura-api.yaml is generated (scripts/generate-openapi.ts) so a second generated file changes; run the generator.
5. KS-1841, services/api-gateway/Dockerfile:35. `RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*` becomes a find that removes everything but secuura-api.yaml (e.g. `find ./docs/openapi -mindepth 1 ! -name secuura-api.yaml -delete`); the ticket lists the six missed name shapes (F1-F3). Verify with a docker build only if a daemon is allowed; otherwise a shell-level fixture test.
6. KS-1884, systemTest/__tests__/manifest_readers_agree.test.sh. The four driver functions end `2>/dev/null | tail -1`. Diff: send stderr to a temp file and print it in the FAIL line when a driver answers empty. Test-script only.
(Two more were considered and left out: KS-1783 is three test files, not one; KS-1904 is six sites and borders KS-1868 lane work.)

## 4. KS-1868 sites still log-only (develop d7691f35)
All read a thrown value with the unguarded `X instanceof Error ? X.message : String(X)` inside a catch that only logs; the message is passed to logger meta and never to a response. If the read throws inside the catch, the helper rejects.
1. services/kyc/src/index.ts:192 dbSaveVerification (swallows; callers `await` it in handlers at :712, :859, :896, :970, :1016, :1045, :1114).
2. kyc/src/index.ts:202 dbGetVerification (returns undefined; callers :757, :806, :876, :929, :995, :1028, :1080, :1139).
3. kyc/src/index.ts:217 dbGetVerificationsByUser (returns []; callers :350, :774).
4. kyc/src/index.ts:235 dbGetVerificationStats (returns zeros; caller :557).
5. kyc/src/index.ts:251 dbSaveConsent (swallows; caller :725).
 (1-5 are one file: one PR, sequenced, not parallel. :323 DB save image is NOT log-only; it rethrows a constant AppError.)
6. services/security/src/index.ts:293 revokePriorConnectorKeys (logs, returns null; callers :380 saveKeyAndRetirePriors, which the register-connector route calls at :1395 and reports priorKeysRevoked null).
7. security/src/index.ts:400 inside saveKeyAndRetirePriors transaction (log, return null after ROLLBACK TO SAVEPOINT; same caller :1395). Same file as 6.
8. services/billing/src/routes/webhooks.ts:316 replay handler (logs, then answers constant 500 `Replay failed`).
Note: billing/src/utils/email.ts:44 is log-only too but sendEmail has no caller in billing/src (grep), so skipped. governanceService.ts sites excluded.

## 5. UNMEASURED
- No ticket's fix was run; no test or mutant executed. Line numbers are from git show at d7691f35 only.
- Whether any seat currently holds a Backlog ticket: not visible (Backlog items had 0 comments; assignee is Kam on most). Only open PRs were checked, not unpushed branches.
- KS-1867's other two interpolation sites and KS-1885's adapter list were taken from the ticket text, not re-read in code.
- KS-1893's hash.ts guard and the http-server.ts catch lines were read; whether the mcp-server ks1868 hash test pins the message text was not read.
- I did not count Backlog tickets that are rulings or Kam-input; the 970 is the whole open set, not an actionable set.
- KS-1796 yaml regeneration path and the PS team (156 open) were not screened.
