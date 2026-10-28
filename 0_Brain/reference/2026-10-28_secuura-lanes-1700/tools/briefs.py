# executed inside gen.py's namespace
HOLDS_T = open(S + '/holds_template.md').read()
LOCKS = {l['n']: f"Seat {l['L']} {l['ord']}" for l in LANES}
LIVE_PANES = [('Seat D 38th', '%53', 'DEPLOY seat: deploys `bd6697e079fc` to the boxes; touches NO code, opens no PR, edits no source'),
              ('Seat R 6th', '%54', 'RAISE seat: ten Spark-pass PRs (A, B, C, D, E, F, G, H1, I, then H2); owns the 24-path Yours list in its brief (55 is the count across all 23 passes)')]

QUEUE = {}

QUEUE[19] = """### 1. KS-1240 part 1 (api-gateway): every hand-built outbound fetch is bounded, and the front door answers a TIMEOUT correctly (the Spark's patch answers 401; the ticket asks for 503)
Provenance: KS-1240 is read live (see PROVENANCE). The ticket's scope sentence, quoted: "The api-gateway's connector-token exchange / key-validate `fetch` carries **no timeout**. A slow or non-answering upstream turns into a gateway request with no bound on how long it hangs." Its own "What to do": "Give the fetch an explicit timeout (AbortSignal / `AbortController`) and decide the refusal shape - a 503 on timeout is consistent with how the connector branch already answers a refused exchange." Graded Major, request-reachable, measured on both trees (an exchange that never answers hangs; one whose body is 2.5 s late hangs that long).
- **Tip facts (drafter, `git show`/`grep` at bd6697e079fc, not run):** `middleware/auth.ts` has two fetches with no `signal`: `getConnectorBearer` (`:197`, any failure returns `null`, logged; the header is left unset so a Bearer-only upstream 401s, per its comment at `:186-190`) and `validateApiKey` (`:227`; its `catch` at `:255-257` returns `null` with NO log, and the caller at `:366-369` turns a `null` for a presented `sk_` key into `401 UNAUTHORIZED 'Invalid API key'`). So today a hung or dead security service reads as "your key is invalid". `routes/proxy.ts` has five unbounded fetches (`:471`, `:502`, `:665`, `:693`, `:1261`) and a body read after the last (`:1274`, `r.arrayBuffer()`); `routes/admin.ts` has two unbounded (`:1375`, `:1440`) beside one already bounded (`:967`, `AbortSignal.timeout(8000)`); `routes/batch.ts` one (`:132`); `routes/audit-export.ts` one (`:172`, its `response.json()` read sits inside whatever signal you attach).
- **What the held Spark patch did and what is wrong with it (reference only; do not apply it):** `READY_KS-1240-...p1...GATEWAY-AUTH...` adds one 5 s constant and a signal to the two `auth.ts` fetches and leaves the existing `catch { return null }`, so a timeout answers **401**, not the ticket's 503, and a valid key reads as invalid for that request. `...p2_proxy_admin...` and `...p3_batch_audit...` add 30 s / 120 s signals whose existing catches answer 502 (proxy/admin) or an item error (batch); the values are the Spark's own.
- **What you build (the drafter's lean, NOT a ruling):** (a) a signal on all 11 unbounded fetches; (b) in `auth.ts`, make a TIMEOUT or unreachable upstream distinguishable from "key rejected" (a typed result, or a thrown marker the caller maps) so the front door answers **503 SERVICE_UNAVAILABLE** for a presented key whose validation could not complete, never a negative-cache entry (the existing 30 s negative cache at `:236-243` is for REJECTED keys only), and never `401 Invalid API key`; read how an OPTIONAL mount (`authenticateToken(false)`, KS-1207 comment at `:372-379`) must behave when validation could not complete and say what you chose; (c) for the exchange (`getConnectorBearer`) the ticket's 503 is a choice: measure what a failed exchange answers today end to end (the Bearer-only upstream's 401) and either keep that (fail closed, documented) or map it, stating which and why; (d) move `proxy.ts:1274` inside the try that maps a failure, so a body stall maps like a connect failure; (e) the bound values (lean: 5 s key validate and exchange, 30 s proxy/admin/batch/audit-export, 120 s `generate-package`) are YOURS to justify from what each call does, as named constants, each stated in the PR.
- **Why this is Opus (row C3):** the answer a client sees on the authentication path changes (401 to 503 for an upstream timeout). If you conclude the status code is a contract change that needs Kam, send a QUESTION (Context: the three call sites; Question: 503 or keep 401; Meanwhile: build the signals and the typed distinction, hold the status-code line); do not decide it silently.
- **Proof:** red first, each cell on a COPY (sha256 before and after, restore proved against HEAD): (i) a never-answering validate server: the request ends within the bound and answers 503, not 401, and nothing is cached; (ii) a server that answers the headers then stalls the body; (iii) a source-text cell counting the gateway's `fetch(` sites against the signals (a new unbounded fetch goes red); (iv) a control that a REJECTED key still answers 401 and still caches 30 s. `services/api-gateway` full suite before/after (record N/N), `tsc` including test files, lint. A test change: append both docs in the same commit.
- **Not yours:** the other `fetch(` sites in `services/api-gateway/src` not listed above (list the census you ran; any other site is a finding for the READY mail); Spark pass N (`tokenisation.ts`, no callers); `index.ts`.

### 2. KS-1240 part 2 (auth social providers): the six provider files bound their fetches and a hung provider is CLASSIFIED, not left as an unclassified rejection
Provenance: same ticket; the social-provider extension is the Spark operator's scope extension beyond the gateway ticket and is confirmed by Wednesday's R 6th ruling that PR O goes "to a Claude build seat later" with its named defect.
- **Tip facts (drafter, `grep` at bd6697e079fc, not run):** 12 fetch sites, none bounded: `github.ts` (`:23` token, `:43` profile, `:57` emails), `google.ts` (`:26`, `:45`), `linkedin.ts` (`:24`, `:42`), `apple.ts` (`:25`), `facebook.ts` (`:24`, `:39`, no init object), `microsoft-personal.ts` (`:25`, `:44`). The callers: the login callback `routes/auth.ts:1069-1080` consumes the OAuth state FIRST (`consumeOAuthState`) and then calls `provider.exchangeCode(code)` inside a try (a failure becomes `BadRequestError('OAuth authentication failed: ' + message)`, state already spent); `POST /social/link` `routes/auth.ts:1346-1365` calls `exchangeCode` with NO local try, so a rejection goes to `next(err)` unclassified.
- **The Spark's defect (reference only):** the held passes `...p4_social...` and `...p5_social2...` add a 10 s signal per fetch and nothing else: on the login callback a hung provider becomes a 400 whose text is the raw abort message, and on `/social/link` an unclassified rejection (likely a 500).
- **What you build (lean, NOT a ruling):** a signal on all 12 sites with ONE shared helper or constant per provider family; a hung or timed-out provider surfaces from `exchangeCode` as the same classified error the codebase already uses for "provider unavailable" (find it; if none exists, define the smallest one and say so), thrown FROM THE PROVIDER FILES so `routes/auth.ts` (a reserved file) is unchanged on both paths. State what each path now answers and that the consumed-state retry behaviour is unchanged (a timed-out login still needs a fresh state; say so). A non-timeout failure behaves exactly as before: pin that with a control.
- **Proof:** red first on a COPY for each provider family (a fetch that never answers; one whose body stalls), both entry paths driven through the real routes (login callback and `/social/link`), a source-text cell counting `fetch(` against signals across the six files, a control that a provider 4xx still answers as it did. `services/auth` full suite before/after (N/N), `tsc` including test files, lint. Docs appended.
- **Not yours:** `routes/auth.ts` (read-only), `oauthState`, every auth file not listed; `users.ts` and PR C's files.

"""

QUEUE[20] = """### 1. KS-1240 part 3 (nft-certificate IPFS provider): all eight outbound fetches bounded, and a body stall maps to the 503 the code promises
Provenance: KS-1240 read live; the nft-certificate extension is the Spark operator's, and Wednesday ruled (R 6th brief) that PR P goes "to a Claude build seat later" because of its named defect.
- **Tip facts (drafter, `grep` at bd6697e079fc, not run):** `services/ipfs.service.ts` has 8 outbound fetches, none bounded: Pinata `:70` (upload), `:105` (pinByHash), `:123` (unpin), Infura `:166` (add), `:195` (pin/add), `:208` (pin/rm), Web3.Storage `:239` (upload), and the gateway read `fetch(url)` at `:463` (inside `async fetch(cid)`, `:455`), whose body is read at `:485` (`await response.arrayBuffer()`). The doc comment at `:27` mentions `IPFSService.fetch()` and is not a call site.
- **The Spark's defect (reference only):** `READY_KS-1240-...p7_ipfs...` adds three constants (60 s upload, 15 s pin/unpin, 30 s gateway read) and a signal per site, but `await response.arrayBuffer()` (`:487` in its source read, `:485` at this tip) sits OUTSIDE the try that maps a connection failure to `ServiceUnavailableError('IPFS gateway')`, so a stall after the headers surfaces as the raw abort error (likely a 500), not the 503 the constants comment promises; and a legitimately large object that needs more than 30 s now fails.
- **What you build (lean):** a signal on the 8 sites; the body read inside the mapping try; per-phase bounds as named constants you justify (lean: the Spark's 60/15/30 s) and state in the PR, with the large-object trade-off said plainly; the 503 mapping proven for BOTH a connect timeout and a body stall.
- **Proof:** red first on a COPY: a gateway that answers headers then stalls the body maps to 503 (the Spark's patch would give the raw error: use it as the known-bad subject for the cell, proving the cell can fail); each provider call's signal present (source-text count against the 8 sites); existing `ipfs.service.test.ts` stays green (read-only: a red there is a QUESTION). Package suite before/after (N/N), `tsc` including test files, lint. Docs appended.
- **Not yours:** the other nft-certificate files.

### 2. KS-1240 part 4 (tenant-provisioning): bound the two outbound fetches and tell the truth about a key-less tenant
- **Tip facts (drafter, read at bd6697e079fc, not run):** `src/meteringKey.ts:45` (`fetch(${securityUrl}/api/keys ...)`, unbounded) and `src/index.ts:131` inside `requestKeyGeneration` (`generate-key`, unbounded). The tenant-create handler calls it inside a try (`index.ts:259-268`) whose catch only logs `[provisioning] Key generation failed, will need manual generation`; the tenant row is then inserted with `vault_key_hash` empty and the handler answers success with `keyFile: null`. **That fail-soft posture already exists for an UNREACHABLE tokenisation service**; a hung one currently hangs the request instead.
- **The Spark's defect (reference only):** `READY_KS-1240-...p8_provisioning...` adds a 10 s signal to each fetch, which turns a hung service into the existing fail-soft path: after 10 s an ACTIVE tenant with no vault key hash is created and the call answers `201 success: true` with `keyFile: null`. Wednesday ruled it NOT acceptable as-is without a named decision.
- **What you build (lean, NOT a ruling):** the two signals (named constants, justified; lean 10 s) in this PR no matter what; then MEASURE and quote the exact response body and DB row of the existing unreachable-service path versus the new timeout path and mail ONE QUESTION to Wednesday with the options: (A) keep the existing fail-soft shape but make the response honest (an explicit flag and message that the key is pending, same for unreachable and timeout); (B) refuse tenant creation with a 503 and insert nothing when key generation cannot complete (changes what a caller of tenant creation sees); (C) other. Build (A) behind the QUESTION's `Meanwhile` line only if it changes no existing status code; hold (B) for an ANSWER. This is an approval-class edge (tenant creation is an irreversible-adjacent operation on a shared platform): the QUESTION is not optional.
- **Proof:** red first on a COPY: a never-answering generate-key and metering-key server ends within the bound (use the Spark's unbounded behaviour as the known-bad subject); the existing `meteringKey.test.ts` and `smoke.test.ts` stay green (read-only). Package suite before/after (N/N), `tsc` including test files, lint. Docs appended.
- **Not yours:** every other tenant-provisioning file; the tokenisation service itself.

"""

QUEUE[21] = """### 1. KS-1382: the five Blockchain/Testing entry points derive TARGET_BASE from the named slot, refuse an unslotted local run, and a new suite pins it for slots 1 to 4
Provenance: KS-1382 read live (see PROVENANCE): state Todo, "Fix (Internal Audit Harness - Kamil's call)" and "Acceptance - comprehensive slot unit tests in the same PR" are written in the ticket; READ ITS WHOLE BODY AND COMMENTS FIRST (this brief quotes only the parts below).
- **Tip facts (drafter, `git grep` at bd6697e079fc, not run):** the five defaults are exactly at `ci/orchestrate.sh:37`, `ci/tools/run-schemathesis.sh:31`, `jobs/05-dast-zap.sh:23` (`TARGET=`), `jobs/06-tenant-isolation.sh:31` (`TARGET=`), `run-internal-audit.sh:30`, each `http://localhost:6882` (slot 1's gateway; `stack_env.sh:56` is `GATEWAY_PORT=$(( 6882 + PORT_OFFSET ))`). **A sixth literal the ticket does not list:** `Blockchain/Testing/tests/tenant-isolation/runner.ts:29` `process.env.TARGET_BASE || "http://localhost:6882"` (run by job 06); it is granted to you because job 06's own default would otherwise be closed in the shell and open in the runner: say in the PR that it was a drafter addition and keep the change to the one line's resolution. Other `6882` hits at the tip are documentation and run records under `Blockchain/Testing/USER SIMULATED TEST/` and a CI snippet that passes `TARGET_BASE` explicitly (`integration/github-actions-snippet.yml:80`); those stay as they are.
- **The ticket's fix, as the drafter reads it:** source `Blockchain/Dev/scripts/stack_env.sh` (it REFUSES without `PROJECT_ROOT`, `:20-21`) and default `TARGET_BASE` to `http://localhost:${GATEWAY_PORT}`; locally with no slot named, refuse to start and print the example command (the KS-1016 rule), so a missing variable is an error, never a silent slot-1 run; CI stays unslotted and passes `TARGET_BASE` explicitly (`.github/workflows/nightly-platform-suites.yml:558`, `pre-merge-platform-suites.yml:351`); add a static check that no `Blockchain/Testing` script carries a literal slot port.
- **The ticket's acceptance (build all of it):** for each of the five entry points and `SECUURA_STACK_SLOT` = 1, 2, 3, 4: with no `TARGET_BASE`, the resolved target is that slot's gateway as `stack_env.sh` computes it (read it from the script, never a copy of the arithmetic); with no slot named locally: refusal with the example command, never a fallback; with an explicit `TARGET_BASE` (the CI path): used unchanged; and the ticket's further cell for `TARGET_BASE` and the named slot DISAGREEING (the KS-1373 case): read its text and build what it says. The suite is a NEW `*.test.sh` under `Blockchain/Dev/scripts/__tests__/` (the directory `run-shell-suites.sh` discovers at `:49`/`:65`), bash 3.2 syntax, no network, each entry point driven in a dry mode that resolves the target and exits before attacking anything (add that mode only if the scripts have none, and say so; a test that starts ZAP is wrong).
- **Judgement to flag, not decide alone:** how the scripts detect "a slot was named" versus the `stack_env.sh` default of 1 (`SECUURA_SLOT_REQUESTED` exists in `systemTest/slot-target.sh:51` for exactly this and is read-only for you): if `stack_env.sh` itself cannot tell, mail a QUESTION; do NOT edit `stack_env.sh` (preflight leg 13 and the pre-push hook depend on its behaviour; KS-1389 is the open ticket about that coupling and is not yours).
- **Proof:** red first on a COPY for each of the five (the current default shows the failure: slot 3 resolves to 6882), then green; the new suite's full output; `bash Blockchain/Dev/scripts/run-shell-suites.sh` (or the leg the preflight uses) before/after with N/N; a control that cannot be a false pass: run each assertion against the UNFIXED script and show it red. A test change: append both docs in the same commit.
- **Not yours:** `stack_env.sh`, `systemTest/slot-target.sh` (KS-1389), `.github/workflows/*`, `Blockchain/Testing/USER SIMULATED TEST/*`, the Akto and Schemathesis harness code under `systemTest/`.

"""

QUEUE[22] = """### 0b. Prerequisite check for item 2
KS-1537 says "after #1497 merges" (the spec file and the regenerated yaml are among #1497's files). Read `gh pr view 1497 --json state,mergedAt` under the project's identity in QUEUE 0 and quote it in the plan confirmation. If it is not merged, do item 1 only and mail a QUESTION for item 2.

### 1. KS-1472: three wording tightenings on the OAuth authorize contract and one test-header sentence
Provenance: KS-1472 read live: "Do 1 to 3 together as a spec-text-only PR (edit `auth.openapi.ts` at the two `/api/oauth/authorize` descriptions, regenerate the yaml with `generate-openapi`, `check:openapi`). Leave 4 unless the phrase is ever reworded."
- **Tip facts (drafter, `git grep` at bd6697e079fc, not run):** the sentence "A token with no scopes satisfies no scope requirement ..." is in `auth.openapi.ts` (the two descriptions near `:2556` and `:2676`), in `docs/openapi/secuura-api.yaml`, and pinned by `ks839-contract-states-the-wildcard-allow-list-rule.test.ts`. The ticket's three points: (1) "a token" to "An OAuth token with no scopes" (a plain login JWT passes `requireScope` on RBAC; only an OAuth token is refused); (2) "requires a scope" does not cover a route that requires a scope OR a role (`requireOrgProvisioner` admits `SUPER_ROLES` by role); (3) "requires none" reads as "none of anything" (role, MFA and tenant gates can still refuse): suggested "requires no scope". Point 5 (from the KS-1468 gate): `ks1210-contract-publishes-the-closed-oauth-scope-enum.test.ts` header (about `:10-16`) says the control checks the `name` field too, but only `redirectUris` is checked: fix the sentence, or add the `name` check (your choice; say which).
- **Build:** the wording edits in the TS source; the yaml REGENERATED (`npm run generate-openapi`, then `npm run check:openapi`; never hand-edited; if the regeneration moves anything beyond the sentences, STOP and report the diff); update the ks839 pin to the new wording (its guard cell forbids one exact false claim; keep that guard working, and show it red against the old wording).
- **Proof:** the sentence before/after in TS and yaml; `check:openapi` rc; ks839 and ks1210 files green; `services/auth` suite before/after (N/N). Docs appended (test change).
- **Not yours:** point 4 (accepted test limit); `routes/oauth.ts` (R 6th PR I).

### 2. KS-1537 items m-1, N-1, N-2: the reserved metadata keys in the contract, and two integration pins (N-4 is a DECISION, not built)
Provenance: KS-1537 read live; its own text: "ACTION (owner: the originate build lane): do these four small things, in one PR, after #1497 merges". Item N-4 is "decide, then record" and is carded for Kam/Wednesday below, NOT built.
- **Tip facts (drafter, not run):** the metadata text is still "free-form issuer metadata folded into the new doc's data blob" at `originate.openapi.ts:1083` (and the three sibling operations; the ticket's line numbers are stale, re-grep at your base) and in the yaml. The silent-strip wording to match is the `actorName`/`actorEmail`/`onBehalfOf` precedent near `originate.openapi.ts:795-800`. N-1/N-2 land in `ks1508-a-planted-versionedbyid-is-not-stored.integration.test.ts` (144 lines at the tip) on a real Postgres.
- **m-1 (Minor):** add ONE sentence to each operation description: `POST /api/documents` silently drops `data.versionedById`; `/:id/version`, `/:id/sign-cert` and `/:id/sign-wallet` reserve four `metadata` keys (`versionAction`, `versionedAt`, `versionedById`, `parentDocumentId`) and overwrite a caller's value. Regenerate the yaml; add a small contract pin (the NEW `ks1537-the-contract-states-the-reserved-metadata-keys.test.ts`, in the style of the ks839 contract test) that fails if the sentence is lost.
- **N-1:** port the gate's two cells `HASH` (a create without `contentHash`: the server hash is computed over the STRIPPED blob) and `HASH2` (the thread-token `metadataHashHex`, with `STATE_THREAD_NFT_ENABLED`: sha256 of the STRIPPED blob) from the gate file the ticket cites (`gate1516-attack.integration.test.ts.txt:230-252`, a gate artefact: find it from the ticket; if you cannot, write the cells from the description and say so). Red-first against the gate's mutant X1 (the strip moved below `const hash = clientHash || generateContentHash(data)` at `routes/documents.ts:656`), in both tenancy modes.
- **N-2:** a real-Postgres cell for `POST /api/certifications/issue` with `parentDocumentId` (the gate's P5 human A, b15 form-encoded, b16 `__proto__`), red against the gate's mutants A6b and X4 on that path.
- **Proof:** every mutant on a COPY (sha256 before/after, restore proved), shown red then green; the integration file's N/N before and after; `check:openapi`; ks1508 unit file stays green. Docs appended.
- **Not yours:** N-4 (decision); any product line in `routes/*` (all READ-ONLY).

"""

QUEUE[23] = """### 1. KS-1702 (gate CN1 N2, N3, N5): three test-only gaps in migration 055's cell file; no migration or product byte changes
Provenance: KS-1702 read live; its own text: "Three test-only gaps that gate CN1 found in migration 055's cell file after the code was already correct. Nothing here is a migration defect." All three items are in `ks1557-055-backfill.integration.test.ts` (393 lines at the tip).
- **Tip facts (drafter, `git show` at bd6697e079fc, not run):** the file has a CROSSTENANT cell family (the `gx-K30` shape is described near `:201`); there is no cell for the gate's mutants O3/O4 (grep finds no `O3`/`O4` in the file); the REPORT cell is at `:301`; the header cites `/:id/sign-cert` and `/:id/sign-wallet` at `:2891` and `:3159`, which the ticket says are `:2905` and `:3173` at its merged head.
- **Item 1 (N2), two cells:** O3 = remove `ap.tenant_id = p.tenant_id` from the `parent_agrees` half only (credits `gx-K52` to c1 and `gx-K30` to c7 on the gate's fixture); O4 = scope on the CHILD's tenant (`d.tenant_id`) instead of the parent's (credits `gx-K53`). The shipped 055 skips K52, K53 and K30. Build one cell per variant, each proven red by applying the variant to a COPY of the migration SQL (the migration file itself is read-only and unchanged); add a comment (not a cell) for the inert `gx-K31` detail.
- **Item 2 (N3):** scope the REPORT comparison to the run's own tenants, and make `afterAll` cleanup cover what the run can write (the `create:connector` rows the FORWARD and RLS runs insert on other tenants' candidates), not only what it created. Prove with a foreign uncreditable version-minted document in a third tenant: the REPORT cell must not fail on it (red before, green after).
- **Item 3 (N5):** correct the header's cite drift and state the "server-set on all three minting routes since KS-1508" premise with its qualification FIRST, not after. Re-check the cited lines against your base before writing numbers.
- **Proof:** the file's cell count before/after, N/N on a real Postgres (see the Docker line in HOLDS), mutants on COPIES with sha256 before/after, `tsc` including test files, lint. Docs appended.
- **Not yours:** gate CN1's N1 (a product-behaviour residue that stays on KS-1557); the migration SQL.

### 2. KS-1588: two missing cells in the ks1009 wallet-status file (response header, and the 500 error body)
Provenance: KS-1588 read live; "Fix shape (the gate's, unchanged)": (1) a HEADER cell asserting the registered-address response carries only the Express defaults (`x-powered-by`, `content-type`, `content-length`, `etag`, `date`, `connection`, `keep-alive`) and no id/role/date header (the gate recorded exactly that set at `content-length: 15`); (2) an ERROR-PATH cell stubbing `db.query` to throw, driving the route, asserting the 500 body is exactly `{"success":false,"error":{"code":"INTERNAL_ERROR","message":"An unexpected error occurred"}}` with no seeded id, role or timestamp. Red-first against the gate's mutants N3 (id in an `X-User-Id` header, body unchanged) and N8 (the error path echoes a message or param into the 500 body).
- **Tip fact (drafter):** `ks1009-wallet-status-reveals-only-existence.test.ts` exists; it has no header or error-path cell (a grep for `header`/`throw`/`500` finds only the Authorization read and a comment). The route itself is NOT changed: both mutants are hypothetical today.
- **Proof:** each mutant is applied to a COPY of the route source (sha256 before/after, restore proved), parses before it runs, and shows its cell red; then green on the real route. `services/auth` suite before/after (N/N), `tsc` including test files, lint. Docs appended.
- **Not yours:** `routes/auth.ts` (read-only, and Spark pass J's file).

"""

QUEUE[24] = """### 1. KS-1394: audit-locks' refusal message points at a regen command that cannot regenerate systemTest/performance's lock
Provenance: KS-1394 read live (Medium; Backlog). Quoted: leg 7's message at `scripts/audit/audit-locks.mjs` says "bump the pin (containerised per-dir regen - see lockfile-cleanroom.sh)"; the command that script prints is `docker run --rm -v "$PWD/<dir>":/app -w /app node:24-alpine npm install --package-lock-only --ignore-scripts`. Two measured problems: (1) the per-directory mount fails (`EMISSINGTARGET`) for a lock with a `file:` link outside its directory (`systemTest/performance` carries `"secuura-observability": "file:../../observability"`); mounting the parent succeeds; (2) `npm install --package-lock-only` does not move a pin that still satisfies its manifest range (0 entries moved); `npm update js-yaml --package-lock-only` moved exactly one.
- **Tip facts (drafter, not run):** the message is now at `audit-locks.mjs:350-354` (the ticket's `:352` is inside it); `lockfile-cleanroom.sh` is at `scripts/preflight/lockfile-cleanroom.sh` (`:72` runs the container, `:190` prints the command); `find services packages frontend scripts -maxdepth 2` is the set it checks, none under `systemTest/`.
- **Build (the ticket's suggested shape, lean):** have `audit-locks.mjs` print its OWN per-lock command: mount the lock's parent when the lock has a `file:` link that escapes its directory, and use `npm update <package> --package-lock-only` for an advisory-driven move; and add one line noting that no preflight leg clean-rooms the `systemTest/` locks. **This is a push-gate leg (preflight leg 7): change MESSAGE TEXT AND ITS COMPUTATION ONLY.** Exit codes, the advisory logic, `audit-baseline.json` (KS-1707's), and `lockfile-cleanroom.sh` are untouched. If a cell in `gate-exit-codes.test.mjs` or `baseline-contract.test.mjs` pins the old message, that is a MAIL (QUESTION) naming the cell, not an edit, unless the pin is in a file you own (none).
- **Proof:** run the leg on a COPY of a lock tree containing an escaping `file:` link and quote the message before/after; verify the printed command is runnable by executing it in a scratch copy (the ticket's measurement: parent mount rc 0); `node --test` of the audit test files before/after (N/N); the leg's own exit code unchanged. A message-only change with no new test takes the docs skill's escape clause: say so in the PR with the reason; if you add a test, append both docs.
- **Not yours:** `audit-baseline.json`, `lockfile-cleanroom.sh`, `lock-discovery.mjs`, any lockfile.

### 2. KS-1113: the e2e DSR cell PATCHes a status the route's enum refuses
Provenance: KS-1113 read live; "Recommendation": "One change in the spec file, proven by one run of the cell against a local stack: (1) send a value the enum accepts - `'processing'` for the mark-in-progress step, or `'completed'` for the terminal step (`TERMINAL_DSR_STATUSES` in `gdprService.ts:1077`) - and assert the 200 `{success:true, message:'DSR updated'}` the route returns for a real id; (2) drop the PUT fallback (no PUT route exists); (3) optionally add one negative cell asserting `'processed'` answers 400. Keep `failOnStatusCode: false` and the NOT-IMPLEMENTED guards as they are."
- **Tip facts (drafter, not run):** the cell `15.2.5 Process DSR` PATCHes `status: 'processed'` at `gdpr-compliance.prelaunch.spec.ts:464` and PUTs the same at `:475`. `DSR_STATUSES` is `['pending','processing','completed','denied','extended']` per the ticket (verify at your base in `services/originate/src/...gdprService.ts`).
- **Judgement to flag:** the cell is titled "marks DSR as processed"; whether to send `processing` or `completed` (and rename the title to match what it observes) is yours: say which and why in the PR; do not leave a title that names an observation the cell no longer makes.
- **Proof:** ONE run of the cell against a local stack (QUESTION first: which slot, and that no other seat is using it; see the Docker/stack line in HOLDS); the cell red at the tip, green after; the optional negative cell if cheap. Docs appended (test change).
- **Not yours:** KS-1112 (the PATCH 200-versus-404 split, a decision); `gdpr.ts`.

"""

NOTYOURS_Q = {
    19: "Everything under `services/api-gateway` and `services/auth` not listed in PARTITION Yours.",
    20: "Everything under `services/nft-certificate` and `services/tenant-provisioning` not listed.",
    21: "Everything under `Blockchain/Testing`, `systemTest/` and `.github/` not listed.",
    22: "Every product route file; N-4.",
    23: "Every product file.",
    24: "Every lockfile and gate leg other than the one message.",
}


def holds_for(l):
    h = HOLDS_T
    seat = LOCKS[l['n']]
    h = h.replace('Seat W 2nd', seat).replace('Secuura/Blockchain-W', 'Secuura/Blockchain-' + l['L'])
    h = h.replace('3a71a1c920cd8e80f226cde635d8314f07342fd6', TIP).replace('3a71a1c920cd', T12)
    h = h.replace('/tmp/w', '/tmp/' + l['L'].lower())
    h = h.replace('letter W', 'letter ' + l['L'])
    h = h.replace('No Docker unless a queue item names it (none does).', 'No Docker unless a queue item names it (' + l['docker'] + ').')
    # shared inbox bullet
    SHORT = {19: 'KS-1240 api-gateway + auth social providers', 20: 'KS-1240 nft-certificate + tenant-provisioning', 21: 'KS-1382 Blockchain/Testing slot targets',
             22: 'KS-1472 + KS-1537 spec prose and pins', 23: 'KS-1702 + KS-1588 test cells', 24: 'KS-1394 + KS-1113 audit-locks message and e2e'}
    sibs = [f"{LOCKS[m['n']]} (lane {m['n']}, {SHORT[m['n']]}; pane id not yet known)" for m in LANES if m['n'] != l['n']]
    live = '; '.join(f"**{n} (pane {p})**: {d}" for n, p, d in LIVE_PANES)
    bullet = ("- **Shared inbox (read before you send or act on any mail):** `secuura-blockchain@agentmail.to` is read by many seats at once. Act only on mail naming your own full seat name (`" + seat +
              "`, ordinal included; an earlier occupant of letter " + l['L'] + " is FOREIGN). **Live on that inbox today:** " + live +
              ". **Sibling lanes of this wave (may launch beside you, each on DISJOINT files):** " + '; '.join(sibs) +
              ". A mail naming any other seat, a box, a deploy or `bd6697e079fc` deploy status is not yours; do not answer or act on it. A mail naming no seat is a QUESTION, not a guess. Arm a matcher that reads the other seats' subjects as FOREIGN and prove it on their real subjects.")
    h = re.sub(r'^- \*\*Shared inbox:\*\*.*$', lambda m: bullet, h, flags=re.M)
    # identity self-check right after heading
    return h


def partition_for(l):
    me = l['n']
    out = ['## PARTITION (written from every seat\'s side)', f"**Yours ({LOCKS[me]}, `Secuura/Blockchain-{l['L']}`), every path checked at {T12} with `git cat-file -e {T12}:<path>`:**"]
    for p, k in l['yours']:
        tag = 'NEW file, on purpose (absent at the tip)' if k == 'new' else 'exists'
        out.append(f"- `{p}` -> rc={rcs[p]} ({tag})")
    for p in (DOC1, DOC2):
        out.append(f"- `{p}` -> rc={rcs[p]} (shared, append-only, for test changes; quote the path: the space in `Projects Documents`)")
    out.append('**Read-only for you (checked present):**')
    for p, note in l['ro']:
        out.append(f"- `{p}` -> rc={rcs[p]} {note}")
    out.append('**NOT yours, live or reserved beside you (file sets listed so a collision is visible):**')
    out.append(f"- **Seat R 6th (pane %54, LIVE; PRs A-I + H2)**: its PARTITION 'Yours' list of `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-28_seatRaise_spark_held_passes.md`, {len(r6_yours)} paths, compared by script against yours: overlap {len(vs_r6[me])}. The files include (verbatim): " + '; '.join(f"`{x.replace(D, '')}`" for x in r6_yours if x.startswith(D + 'services')) + '; plus packages/shared, scripts and m365 files listed in that brief.')
    out.append(f"- **Spark pass files reserved for a LATER Claude lane (R 6th PRs J-N, not yours, not R 6th's):** {len(r6_reserved)} paths; overlap with yours: {len(vs_r6res[me])}" + (' - BY ASSIGNMENT (these are the KS-1240 pass files given to YOU by this brief; every other reserved file stays off limits): ' + ', '.join(vs_r6res[me]) if vs_r6res[me] else '') + '. Lanes 19 and 20 take the KS-1240 passes M, O, P, Q only by explicit assignment; N (tokenisation.ts, no callers) stays unclaimed.')
    for m in LANES:
        if m['n'] == me:
            continue
        out.append(f"- **Lane {m['n']} ({LOCKS[m['n']]})**: " + '; '.join(f"`{p.replace(D, '')}`" for p, k in m['yours']))
    out.append(f"- **Seat D 38th (pane %53)**: a DEPLOY seat; it edits no source and you do not touch its clone, boxes or mail.")
    out.append(f"- **Open pull requests** (14 at the drafter's read, {n_entries} file entries on {len(pr_files)} distinct paths; `gh pr list -R Secuura/Distributed_Secuura --state open --json number,files`): overlap with your files {len(vs_pr[me])}. They are dependency bumps, lockfiles and two docs/tooling PRs; they stay their authors'.")
    out.append("- Anything under `Blockchain/Dev/services/` or elsewhere not listed above, every other seat's worktree and clone, `2_Project_Files` of the project checkout (READ-ONLY; read repo files from a SHA, never from the Secuura main checkout's working tree), and the PR-gate hook `.githooks/pre-push` (read it, cite the line that allows each push, never edit).")
    return '\n'.join(out) + '\n'


def provenance_for(l):
    P = []
    P.append(f"- Develop tip `{TIP}` (committed 2026-10-28T15:29:56+11:00) | `git -C {CL} ls-remote origin refs/heads/develop` (own scratch clone, then `git cat-file -e`) | read {TODAY}")
    P.append(f"- Open Linear issues, KS team, states backlog+unstarted+started: 696 nodes, 696 unique ids, 7 pages of 100 (Backlog 352, In Progress 266, In Review 50, Todo 25, Blocked 3) | Linear GraphQL `issues(first:100, after)` cursor loop to hasNextPage false, key sourced transiently from the project `.env` | read {TODAY}")
    for k in l['tickets']:
        P.append(f"- {tstate(k)} | Linear ticket {k} (title, description and `comments(first:50)` read in full in one pass) | read {TODAY}")
    P.append(f"- Open pull requests: 14, {n_entries} file entries ({len(pr_files)} distinct paths), 0 overlap with this lane's files | `gh pr list -R Secuura/Distributed_Secuura --state open --limit 300 --json number,title,headRefName,author,files` with the project's own GH_TOKEN in a scratch GH_CONFIG_DIR, read-only | read {TODAY}")
    P.append(f"- Seat R 6th PARTITION (PRs A-I + H2; J-Q reserved) | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-28_seatRaise_spark_held_passes.md` section PARTITION, parsed by script into {len(r6_yours)} yours and {len(r6_reserved)} reserved paths | read {TODAY}")
    P.append(f"- Live panes in `fleet:0`: `wednesday`, `Secuura/Blockchain-R` (%54), `Secuura/Blockchain-D` (%53), `fleet-monitor`; no pane for any letter of this wave | `tmux list-panes -t fleet:0 -F '#{{@cockpit_name}} #{{pane_id}}'` | read {TODAY}")
    P.append(f"- Seat ordinals: newest history entries are Seat {', '.join(f'{m['L']} {prev_ord(m)}' for m in LANES)} (so the lanes are {', '.join(LOCKS.values())}) | `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` (newest at top; grep of the `## 2026-10-2x - Seat` headings) | read {TODAY}")
    P.append(f"- Letters exist in the routing table | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf` lines for `Secuura/Blockchain-{l['L']}` | read {TODAY}")
    P.append(f"- Routing: {l['row']} ({'build on an auth or security DESIGN surface: Opus' if l['row']=='C3' else 'multi-file build or feature that fails the local predicate, not decision-shaped, not auth-design and not a destroying path: Sonnet 5.5'}) | `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/specs/model-routing.md` section 4b | read {TODAY}")
    P.append(f"- Standing lines carried (two-doc rule, push queue, lock by own mkdir, anchored pre-push pattern, short TMPDIR, release deletes holder before rmdir, merge-time section numbers, per-command push keepalive, resolver reads the merge result, instrument rules, PID-only kills) | copied from the HOLDS block of `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-28_seatW_lane14_auth_ks1000_expectrun_residuals.md`, itself from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` | read {TODAY}")
    P.append(f"- Kam's live-board instruction | R 6th brief section RULED BY KAM and the drafting prompt | read {TODAY}")
    return '\n'.join(P) + '\n'


def prev_ord(m):
    n = int(re.match(r'\d+', m['ord']).group())
    return {1: '1st', 2: '2nd', 3: '3rd'}.get(n - 1, f'{n-1}th')


def build(l):
    seat = LOCKS[l['n']]
    L = l['L']
    t = []
    t.append(f"## NEW SEAT: you are {seat} in pane %__ (Wednesday fills the pane id from the launcher's \"pane ... added (%NN)\" line; if `$TMUX_PANE` differs, trust `$TMUX_PANE`, say so in your plan confirmation; lane Secuura/Blockchain-{L}, a {l['kind']}): {l['title']}; each ticket stops at READY FOR GATE\n")
    t.append(f"**Identity self-check (your SECOND action, after the preflight read):** `tmux display -p -t \"$TMUX_PANE\" '#{{@cockpit_name}}'` must print `Secuura/Blockchain-{L}`; if it prints anything else, STOP and mail a QUESTION. Never check your pane against a pane title.\n")
    t.append(f"**Routing receipt:** {l['receipt']} **Letter {L} IS in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`** (line `Secuura/Blockchain-{L}|secuura-blockchain@agentmail.to|yes`, read {TODAY}), but **earlier occupants of this letter ran earlier waves**: Wednesday read `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` and the newest entry for this letter is `Seat {L} {prev_ord(l)}`, so you are `{seat}` (re-check it at boot) and treat mail naming any earlier occupant as FOREIGN.\n")
    t.append(f"**Why you exist:** Kam, live board 2026-10-28 16:4x (verbatim): \"keep working and use as many agents as you can to go through all the tickets\". This is wave 5, lane {l['n']} of `{REF}/lanes.md`. R 6th is raising ten Spark passes on other files; this lane is on files the sweep found disjoint from R 6th, from every open PR and from the other five lanes. Every item below was re-read against develop `{T12}` (`{TIP}`, committed 2026-10-28 15:29:56 AEDT, read 2026-10-28 ~17:0x AEDT), and **a ticket item the tip already satisfies is not built; it goes in your READY mail as DONE-READY evidence.**\n")
    t.append("## BLUF")
    qn = sum(1 for _ in re.finditer(r'^### \d', QUEUE[l['n']], flags=re.M))
    t.append(f"1. **Order, one item at a time:** the QUEUE's order ({qn} item{'s' if qn != 1 else ''}). Do not open the next until the previous has its PR up. Tickets: {', '.join(l['tickets'])}.")
    t.append("2. **Partition, your side:** you edit ONLY the files in PARTITION \"Yours\". Everything else is READ-ONLY for you.")
    t.append("3. **Partition, the other side:** R 6th (LIVE), the other five wave-5 lanes and the open PRs are listed under PARTITION as NOT yours; the owned sets were compared pairwise by a script (no path shared, excluding the two `Projects Documents/` HTML docs, the one shared surface: append-only, section numbers set at merge time).")
    t.append("4. **Held on purpose (not yours):** see each QUEUE item's \"Not yours\" line.")
    t.append(f"5. **You stop at READY FOR GATE**: no merge, no deploy, no box. Develop tip when drafted: `{TIP}` (read from origin 2026-10-28 ~17:0x AEDT; both boxes are being moved to `bd6697e079fc` by Seat D 38th, not by you): your base is whatever `ls-remote` says at boot. Start from the tip, not from a ticket's line numbers.\n")
    t.append("## QUEUE")
    t.append("""### 0. FIRST ITEM, before any write: boot and the open-PR check
Your FIRST tool call reads `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.launch_preflight_last.txt`; quote it with its own launch stamp in the plan confirmation (it is per-project; the next launch overwrites it). Check `$TMUX_PANE` against the pane id in line 1, then run the identity self-check above. Your next call is the open-PR list: `GH_CONFIG_DIR=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config gh auth status` (not logged in is a QUESTION, never another identity; if you use the project's own `GH_TOKEN`, say so), then `gh pr list --state open --limit 200 --json number,title,headRefName,files`, `rc=$?` on its own line. Intersect every open PR's file list with the files PARTITION grants you. **If any open PR touches a granted file, STOP and mail a QUESTION (PR number, file); do not edit.** Report in the plan confirmation how many PRs were open and that the intersection is empty. **R 6th will open ten PRs during your session: re-run the intersection against the then-open PR list before each push.**
Then read develop with `git ls-remote origin refs/heads/develop` (drafter: `""" + TIP + """` at ~17:0x AEDT), `git cat-file -e` that sha before counting, record your base. Re-run `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` and report any line dated after 2026-10-27 that names your tickets. **Re-read each queued ticket's comments at boot (`comments(first:50)`, sorted client-side): if a comment after the drafter's read shows a PR, a ruling, or a question to a human on that ticket, STOP on that ticket and say so.**
**Plan confirmation:** a QUESTION mail, topic `plan confirmation`, to `wednesday-agent@agentmail.to`, subject starting `[Secuura/Blockchain-""" + L + """ -> Wednesday]`, body line 1 `""" + seat + """`, sent before your first write; it carries the launcher preflight warnings VERBATIM.
**Worktrees:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-""" + L.lower() + """-<ticket-key-lowercase>`, never inside `2_Project_Files`. Setup per the HOLDS line on fresh worktrees. Develop's objects reach the worktree by one objects-only transfer from your own scratch clone (STANDING_LINES line 408); no fetch or pull in the shared checkout after boot.
**Before the first edit of each owned file:** `git log origin/develop -1 -- <file>` for every file that item changes, and read `git log -p` of the last commit touching it if that commit is under a day old. If another seat or open PR is shown to touch an owned file, STOP and mail a QUESTION.
""")
    t.append(QUEUE[l['n']])
    h = holds_for(l)
    t.append(h)
    t.append(partition_for(l))
    t.append("""## UNMEASURED (WHY, and WHICH instrument closes it)
- **Open PRs touching your files after the drafter's read.** The drafter read 14 open PRs at ~17:0x; R 6th will add ten. Closed by QUEUE 0 and re-run before each push.
- **Every ratio, line number and count quoted from a ticket or from a drafter grep** is a `git show`/`git grep` reading at `""" + T12 + """` or the ticket author's figure; the drafter ran NO suite, mutant, build or script. Closed by running each suite on your clean worktree before editing.
- **Whether each ticket item is still open beyond what the QUEUE says the drafter checked** (greps at the tip). Closed by reading the code at your base.
- **Seat ordinal and pane id.** Closed by `history.md` and `$TMUX_PANE`.
- **Whether a sibling lane's seat is live beside you.** The pane list at drafting held only D 38th and R 6th. Closed by the shared-inbox matcher and QUEUE 0.
""")
    t.append("""RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam, live board 2026-10-28 16:4x (verbatim): "keep working and use as many agents as you can to go through all the tickets" (the reason this wave exists).
- Card wed-spark-drafting-cost-1028 = b (Kam, live board 2026-10-28 16:42:24): keep briefing the Spark in full batches. Context only: it is why Spark passes exist; nothing for you to do.
- Kam 2026-09-07 13:23: one ticket when one test pass proves it; split only for separate fixes (STANDING_LINES line 86).
- No other ruling was searched by the drafter for these tickets' ids and file families (the drafter did NOT run `decision_queue.sh` itself): QUEUE 0 does it. If a ticket you open names a Kam ruling, read the ruling's card (`decision_queue.sh show <id>`) and mail before acting on it.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- R 6th brief rulings, 2026-10-28 16:5x: Spark pass PRs J-Q are NOT in R 6th's round; KS-1240's passes M, O, P, Q "carry a defect or an open design choice found at source (M: 401 not the ticket's 503; O: unclassified rejection on POST /social/link; P: body stall unmapped; Q: key-less active tenant answering 201) ... They go to a Claude build seat later under the counter" (lanes 19 and 20 are that seat).
- Spark passes are raised, gated and GO'd by Wednesday; a raise seat never merges (standing since 2026-10-05); the same holds for you: you stop at READY FOR GATE.
- Peter's and Stuart's open PRs and tickets stay theirs; never touch, comment on or merge another author's PR; you are TOLD about them, never ask them.

PROVENANCE:""")
    t.append(provenance_for(l))
    t.append("SELF-CHECK: (left for Wednesday)")
    return '\n'.join(t) + '\n'


import os
for l in LANES:
    fn = f"{BR}/2026-10-28_seat{l['L']}_lane{l['n']}_{l['slug']}.md"
    open(fn, 'w').write(build(l))
    print('wrote', fn, os.path.getsize(fn))

exec(open(S + '/report.py').read())
