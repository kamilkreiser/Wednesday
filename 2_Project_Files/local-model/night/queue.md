# night/queue.md — the list Kam asked for (2026-09-14 18:15 "Prepare a list of tickets for it to work on")
#
# FORMAT (read by night_run.sh): one ticket per NON-comment line — `KS-<n>` first, then optional
# space-separated pins for build_input.sh: product=<repo path> ref=<repo path> line=<n> ctx=<num_ctx>.
# Lines starting with `#` are ignored. When a ticket's run ends its line MOVES to night/done.md with the
# verdict + run dir. Order = priority (the runner takes the first line each time).
#
# DERIVED 2026-09-14 18:2x AEST from a read-only Linear pull: team KS, state.type in [backlog, unstarted],
# includeArchived:true → 363 issues (Backlog 331 · Todo 32; 54 archived, excluded). Then the contract
# filter (rule clause 3): ONE product file (or unambiguous) · a described fix shape · a runnable
# IN-PROCESS test nearby to copy · NOT auth/oauth/token/mfa/security surfaces · NOT attached to an open
# PR · NOT in a live lane's Owns (L2 s226 / L8 s229 / L10 s227 briefs read) · NOT on Peter/Stuart ·
# NOT archived · the service must run VITEST (the checker's `npx vitest run`; originate + governance
# are jest and cannot be checked by this harness). Pinned lines/refs are as of develop 0e78c7270 (18:2x).
# Re-derive at source before the night (a ticket can close, be archived by cascade, or be taken by a lane).
#
# ─────────────────────────────────────────────────────────────────────────────────────────────────────
# FITS (3) — the honest count. The KS Backlog/Todo set is dominated by coverage-only tickets (the code
# is right, a test is owed — the contract's RED-FIRST assertion cannot pass on those), decision/ruling
# tickets, security surfaces, multi-service chains, and originate (jest). Rejections are listed below
# so the next board seat need not re-read them.
#
# 1. KS-871 · "The audit log records `req.path` AFTER the response, so a REFUSED erasure is logged with
#    the path trimmed to `/`" · Backlog · Medium · file `services/api-gateway/src/middleware/audit.ts`
#    · fix shape (ticket): "Capture the path once at entry — `const auditPath = req.originalUrl.split('?')[0]`
#    — and use that inside the finish handler. One line, and it fixes every `router.use(prefix, …)` gate
#    in the file" · WHY: one file, fix sentence + Where-list (`:108` deriveAction, `:280` details.path),
#    in-process reference `ks843-erasure-path-bypass.test.ts` drives the exact refused-erasure route;
#    14.8 KB file → ~8.3K prompt tokens. Already run by three models (all PARTIAL: fixed `:280`, missed
#    `:108`) — the generic task.md now says "fix every named site"; this is the re-test of that wording.
#    Pins: ref= (ks843 does not import audit.ts, so the auto-pick cannot find it) · line=280.
# 2. KS-1072 · "The latest-anchor selector documents a `confirmedAt` tiebreak it does not implement —
#    and since KS-1057 that selector decides the verdict" · Backlog · Low · unassigned · file
#    `services/api-gateway/src/routes/verification.ts` (65.6 KB) · fix shape (ticket): "implement the
#    documented tiebreak (or correct the comment to say there is none), and pin it with a cell driving
#    two equal-`blockNumber` anchors" · WHY: a 2-line comparator fix at one site (the builder anchors it
#    on the quoted `(b.blockNumber || 0) - (a.blockNumber || 0)` → tip line 289), reference
#    `ks1071-verify-confidence-one-mapping.test.ts` (imports ../routes/verification, drives it in-process
#    over a stub anchor store). Rejected on 09-14 for the 120B trial on CONTEXT BUDGET only (~21.8K prompt
#    tokens) — at night the budget is time, so ctx=49152.
# 3. KS-1087 · "workflow-approve deletes the pending document and answers 200 without reading
#    originate's response — a refused forward loses the document" · Backlog · High · same file
#    `services/api-gateway/src/routes/verification.ts` · fix shape (ticket, item 1): "Report approval and
#    delete the pending document only after originate returns 2xx. On any other status, or a network
#    error, keep the pending document and return an error to the caller." · WHY: item 1 is a bounded
#    one-site change (`proxyReq.end(); await redisService.deletePendingDocument(documentId)` at tip
#    :990-991 → move the delete + 200 into the response callback, gated on 2xx), item 3 is the test cell
#    ("an originate stub returning 401 must not yield 200 approved, and the pending document must
#    survive"). CAVEAT: item 2 (which credential originate accepts) is a design call — the model must NOT
#    touch it; a PASS here is item 1 only. Same reference test family as KS-1072. ctx=49152.
#
#
# ─────────────────────────────────────────────────────────────────────────────────────────────────────
# REJECTED (read, one line each — id · reason). Re-check a "coverage-only" ticket only if the contract
# ever grows a test-only mode (it would need a DIFFERENT red-first rule: the test must red under a
# planted tamper, not at the tip).
#
# coverage-only (code correct at head; a test/comment pass is owed — RED-FIRST cannot pass):
#   KS-1123 · verification.ts `??`→`||` F3 — "the shipped code is right on every one of 119 cells"; the ask is pins + comment rewording
#   KS-1130 · ks1069 tier-2 twin cells + falsified comments — "Nothing here changes behaviour"
#   KS-1120 · presentations.ts exact-or-404 — three TEST-side gaps, "the code is correct at head"
#   KS-1125 · startup-migrations tenant-failure guard has no test — needs a Module._resolveFilename fake `pg` (not vi.mock-able)
#   KS-1145 · ks949 shell suite coverage — a bash test suite, not vitest
#   KS-1142 · two corpus literals in two TEST files — test-only, packages/shared
#   KS-1143 · LEG F guard walk — the "product" is the test file `ks781-p3-3-body-parser-order.test.ts` itself; fix shapes are proposals
# decision / ruling first (no single fix shape, or the ticket says so):
#   KS-849  · kyc stale-timer clobber — "Fix shape (not chosen)": re-read in the timer OR narrow the write; "wants its own gate". Queueable if Kam rules option (a)
#   KS-960  · users.email uniqueness — "DO NOT RECONCILE THESE TWO FILES YET"; SQL, not TS
#   KS-1050 · users.ts:933 0-row update — the response contract (5xx vs 404/409) "needs a call"
#   KS-1132 · getPlatformAdmin swallows infra failure — "Decision needed, then the build"
#   KS-807  · control-byte guard cannot see a raw body — the ticket asks (A) vs (B), 2 files
#   KS-834  · [Decision] verify route auth — a decision ticket
#   KS-753  · timestamping mock-TSA fallback — open design question (503 vs verified:false), 2 files
#   KS-629  · kyc livenessVideo — "Decide which half is right"; 2 files incl. openapi
#   KS-625  · presentations/verify holder signature — "fix shape deliberately blank", Kam's ruling
#   KS-954  · leading-`//` on /api/billing — "Mechanism NOT determined … Reproduce before fixing"
#   KS-1112 · gdpr PATCH 200 "not found" — two-way decision; option 1 edits a 2nd file; originate (jest)
#   KS-761  · similarity-undiscriminating FP staleness — Peter's two options; systemTest
#   KS-808  · run-migrations.sh — shell script; item 1 is a decision
# multi-file / multi-service / structural:
#   KS-1129 · raw pg BIGINT — three sites in three services (anchoring, originate, api-gateway)
#   KS-1055 · per-tenant DBs never get file migrations — structural, 2 services, needs real PostgreSQL
#   KS-870  · admitted erasure authenticates twice — option 1 is one file but it is the AUTH chain; option 2 touches shared auth middleware
#   KS-953  · CLASS ticket (editing index.ts reddens packages/shared) — a mechanism, not a fix
#   KS-864  · system-status.ts dead-estate literals — the fix needs values from CLAUDE.md/deploy-demo.yml (facts outside the input)
#   KS-683  · anchor-status standoff — the fix is Platform S's (Stuart's side), not K's code
#   KS-579/581/582/576/580 · platform-admin identities / bulk re-key — features + security, Todo
#   KS-627  · real CIP-8/COSE wallet signature verification — a feature, wallet-connector
#   KS-668  · compose seeds *123 credentials — config/compose, not a TS product file
#   KS-915  · first privileged account on a clean stack — design
#   KS-1128 · platform tenant seed log level — its owed test needs a real PostgreSQL boot
#   KS-1146 · push preflight has no services/auth leg — scripts/, not a product file
# security surfaces (rule clause 3 — auth/oauth/token/mfa/security; kept for Opus builders):
#   KS-618 (client IP / rate-limit keys) · KS-623 (authenticate.ts) · KS-692 (tenant ownership on revoke) ·
#   KS-744 (jwt.ts) · KS-746/880/888/889/908/974/975/976 (services/security: API keys, rate-limit scope) ·
#   KS-756 (session.ts refresh token) · KS-839/824/855/1157 (oauth) · KS-938/1006 (MFA) ·
#   KS-1003 (OAuth token endpoint rate-limit zone) · KS-1005 (change-password) · KS-1009 (wallet status
#   leaks userId+role) · KS-1018 (verification-store reads in users.ts) · KS-1119 (multi-tenant verify) ·
#   KS-1121 (credentialRepo LIKE substring) · KS-1084 (gateway→originate auth headers) · KS-1124
#   (certification confidence after a failed anchoring — originate) · KS-658 (NODE_ENV) · KS-491/329 (reviews)
# originate / governance (jest — the checker runs vitest only) or a live lane's Owns:
#   KS-757 · KS-759 · KS-777 · KS-1019 · KS-1113 · KS-1118 · KS-1158 · KS-1160 · KS-1074 (anchorStateSync — L3a's file) ·
#   KS-1133/794 (openapi docs) · KS-741 (Todo, documents.ts — L2 s226's Owns)
# live lanes' tickets (never queued): L2 s226 KS-739/1068/791 (+ KS-801/1035 named) · L10 s227
#   KS-993/711/704/973 · L8 s229 KS-945/926/930/937/911/912
# Peter's / Stuart's: 25 tickets excluded at the filter (assignee), not read.
#
# RE-QUEUED 2026-09-15 05:5x by Wednesday: the three BUILD_REFUSED rows of the 05:30 hand run (stale object
# store) — now buildable on the verified tip override (night/tip_override.txt: a594eb162 vs origin 0f37b85c8,
# 0 files under Blockchain/Dev between them). Run 24/7 per Kam 2026-09-14 21:57 (G1 informational).
# KS-871 re-queued 06:0x: its 05:56 run FAILED at A1 for a SAMPLER reason (repetition loop → length cut, fence never closed); lm_call.py now carries repeat_penalty 1.15 / repeat_last_n 512 / num_predict 12288.
KS-871 ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks843-erasure-path-bypass.test.ts line=280
KS-1072 ctx=49152
KS-1087 line=991 ctx=49152
