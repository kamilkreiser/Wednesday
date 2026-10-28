## NEW SEAT: you are Seat R 6th (lane Secuura/Blockchain-R, a RAISE seat, on SONNET): turn TEN of today's held Spark passes into file-disjoint PRs (PRs A, B, C, D, E, F, G, H1, I, then H2); every PR ends at READY FOR GATE, nothing merges

Your pane id: read it yourself with `tmux display -p -t "$TMUX_PANE" '#{pane_id} #{@cockpit_name}'` (it must read Secuura/Blockchain-R). Drafted by Spark operator 3, read and ruled by Wednesday 2026-10-28 16:5x.

**Routing receipt:** `model: claude-sonnet-5-5 -- C1 (raise a held local PASS as a PR) + C2 -- P1-P4 no: raising needs the board identity a local model cannot hold; no auth DESIGN is decided by this seat -- gauge 68%`.

## 🔴 WEDNESDAY'S RULINGS (2026-10-28 16:5x) — SUPERSEDE every "needs Wednesday's ruling" line below
- **This round is TEN PRs, not the 18 drafted below.** Wave 1 (A, B, D, E, F, G, H1) as written; **PR I and PR C are RULED and open in wave 1 after H1** (no QUESTION mail needed for them); wave 3 = H2 after G merges.
- **PR I (KS-1219): ACCEPTED.** JSON null/0/false scope -> 400 is a validation tightening on the authorize route. Body states the behaviour change in its first line. Its gate will be tier 1 (auth surface).
- **PR C (KS-1467 auth): ACCEPTED ON ONE CONDITION.** Before the PR opens, add ONE cell to its own test (no product line) proving the weak-password 422 body never contains the candidate password (plant a distinctive candidate, assert it is absent from the serialised body; red-proof by temporarily echoing it). If the cell cannot pass on the Spark's product lines, STOP and mail; do not adjust the product.
- **PRs J, K, L, M, N, O, P, Q: NOT IN THIS ROUND. Not yours; do not open them, do not branch them.** Each carries a defect or an open design choice found at source (M: 401 not the ticket's 503; O: unclassified rejection on POST /social/link; P: body stall unmapped; Q: key-less active tenant answering 201; J/K: shape alternatives / partial fix; L: WIDENS platform-admin access; N: bounds code with no callers). They go to a Claude build seat later under the counter. Their files below are listed for history only.
- Everything else in this brief stands (HOLDS, PUSH LOCK, KEEPALIVE, docs rule, PER-PR PROOF, PARTITION for A-I + H2).

**Why you exist:** 23 Spark passes (PASS 7/7, byte-identical to their goldens) are HELD in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/` (Wednesday and two Spark operators read each at source). No Secuura seat holds the board identity to raise them. The Spark is free quota capacity; your seat is the cost, so spend it where the passes already did the thinking.

**Develop pin:** `bd6697e079fce41db6b21e094a9eddb3d0e1d08e` (`git ls-remote origin refs/heads/develop`, read 2026-10-28 ~16:00 AEDT by the operator). It WILL move: re-read it at your boot and before every PR. The passes were built at `65bc28234507ffcf242381f8020d80b3efe83e85`; develop is 2 commits ahead and none of the 55 files the passes touch changed between the two (`git diff --name-only 65bc2823..bd6697e0` intersected with the file list: empty). Overlap with the 14 currently open PRs: 0 files (gh read with the project token, 2026-10-28).

---
## BLUF
1. **TEN PRs this round (Wednesday's rulings above): wave 1 = B, A, D, F, E, H1, G, then I and C (both RULED); wave 3 = H2 after G merges. PRs J-Q are NOT in this round.**
2. Each PR applies the Spark's patch from the READY file's canonical `patch.diff`, **in the apply mode the checker used (APPLY MODES below)**, never by hand-merging product lines. If a patch no longer applies at your pin in its recorded mode, STOP and say which hunk.
3. **`Refs`, never `Closes`, on every PR.** Nothing here is deployed.
4. Every PR ends at **READY FOR GATE, one mail per PR**. No merge without Wednesday's GO naming the head sha.

## THE PRs
Disjointness was computed by the operator from each pass's golden `+++ b/` headers (55 distinct files across the 23 passes): the only file two passes share is `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (KS-1779 p1 and KS-1780 p2). Re-derive it yourself at your pin before opening more than one branch.


### WAVE 1 (HOLD: no ruling needed)

#### PR A: KS-1591 isPlatformRole + requireKeyAdmin exact ASCII fold (two passes, disjoint files)  [HOLD]
- **Pass `ks_1591_p1`** | READY: `READY_KS-1591-KS-1591-ks_1591_p1_spark-dsv4flash_BRIEFED-CODEPATCH-KEYREVOKEPOLICY-ASCII-FOLD-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts` (exists at pin)
- **Pass `ks_1591_p2_security`** | READY: `READY_KS-1591-KS-1591-ks_1591_p2_security_spark-dsv4flash_BRIEFED-CODEPATCH-REQUIREKEYADMIN-ASCII-FOLD-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1591_p2_security/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/security/src/index.ts` (exists at pin)

#### PR B: KS-1467 packages/shared AppError subclasses keep their prototype  [HOLD]
- **Pass `ks_1467_p2_shared`** | READY: `READY_KS-1467-KS-1467-ks_1467_p2_shared_spark-dsv4flash_BRIEFED-CODEPATCH-INDEX-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/packages/shared/src/errors/index.ts` (exists at pin)
- Refs only: this is the shared half; the auth half is PR C and is a separate ruling.

#### PR D: KS-1670 m365 success redirect encodes connectionId (site 1 only)  [HOLD]
- **Pass `ks_1670_p1`** | READY: `READY_KS-1670-KS-1670-ks_1670_p1_spark-dsv4flash_BRIEFED-CODEPATCH-M365-SUCCESS-REDIRECT-ENCODE-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1670_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/m365-integration/src/index.ts` (exists at pin)
- Refs, never a close-word: sites 2 and 3 wait for the KS-1641 :515 decision. The test is a source-text pin; say so in the PR body.

#### PR E: KS-1250 smoke-test.sh honours SMOKE_BASE_URL (bash)  [HOLD]
- **Pass `ks_1250_p1`** | READY: `READY_KS-1250-KS-1250-ks_1250_p1_spark-dsv4flash_BRIEFED-BASHPATCH-SMOKE-TEST-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1250_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=1
  - `Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh` (NEW file (absent at pin))
  - `Blockchain/Dev/scripts/smoke-test.sh` (exists at pin)
- bash_patch; the test is a *.test.sh suite, run it with /bin/bash and read $? on its own line. The patch moves only `GATEWAY` to `${SMOKE_BASE_URL:-...}`: in the FULL run, section 7 onward still calls hard-coded `http://localhost:60xx` ports (smoke-test.sh lines 257-327 at the pin); the PR body must say a remote full run is not remote-clean (see the ADDENDUM at the foot of the READY file).

#### PR F: KS-1536 auth issuerCerts.ts: hasAdminRole extraction (behaviour-preserving)  [HOLD]
- **Pass `ks_1536_p1`** | READY: `READY_KS-1536-KS-1536-ks_1536_p1_spark-dsv4flash_BRIEFED-CODEPATCH-ISSUERCERTS-HASADMINROLE-EXTRACTION-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1536_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts` (exists at pin)
- Hangs from KS-1536 only because the builder needs an open ticket: `Refs KS-1536`, never a close-word; the body says 'groundwork, not a fix for the ticket'.

#### PR G: KS-1779 originate adminConfig.ts migrate-tenant-data loop lint  [HOLD]
- **Pass `ks_1779_p1`** | READY: `READY_KS-1779-KS-1779-ks_1779_p1_spark-dsv4flash_BRIEFED-CODEPATCH-ADMINCONFIG-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1779_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=1, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/originate/src/__tests__/ks1779-migrate-tenant-data-loop-has-no-lint-warnings.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (exists at pin)
- MUST merge before PR H2 (same file adminConfig.ts). The checker applied it FUZZY (apply_mode=fuzzy): see APPLY MODES.

#### PR H1: KS-1780 originate systemErrors.ts + utils/pgErrors.ts hostile-throw catches (two passes, disjoint)  [HOLD]
- **Pass `ks_1780_p1`** | READY: `READY_KS-1780-KS-1780-ks_1780_p1_spark-dsv4flash_BRIEFED-CODEPATCH-SYSTEMERRORS-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/originate/src/routes/systemErrors.ts` (exists at pin)
- **Pass `ks_1780_p3_webhooks`** | READY: `READY_KS-1780-KS-1780-ks_1780_p3_webhooks_spark-dsv4flash_BRIEFED-CODEPATCH-PGERRORS-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p3_webhooks/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/originate/src/utils/pgErrors.ts` (exists at pin)
- KS-1780 has three passes; this PR carries p1 and p3. p2 is PR H2.


### WAVE 2 (HOLD-WITH-DECISION: needs Wednesday's ruling BEFORE the PR opens)

#### PR I: KS-1219 auth oauth.ts: authorize refuses an array-valued scope  [HOLD-WITH-DECISION]
- **Pass `ks_1219_p1`** | READY: `READY_KS-1219-KS-1219-ks_1219_p1_spark-dsv4flash_BRIEFED-CODEPATCH-OAUTH-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1219_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/auth/src/routes/oauth.ts` (exists at pin)
- JSON null/0/false scope now answers 400 (was: treated as absent).
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR C: KS-1467 auth AppError prototype + errorHandler/passwordLoginGate  [HOLD-WITH-DECISION]
- **Pass `ks_1467_p1`** | READY: `READY_KS-1467-KS-1467-ks_1467_p1_spark-dsv4flash_BRIEFED-CODEPATCH2-ERRORHANDLER-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/auth/src/middleware/errorHandler.ts` (exists at pin)
  - `Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts` (exists at pin)
- Weak-password 422s (auth.ts:204, :822, users.ts:993) start to carry error.details = { feedback }; auth.ts:173 does not.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR J: KS-1776 auth routes/auth.ts demo-seed timer tolerant of a synchronous throw  [HOLD-WITH-DECISION]
- **Pass `ks_1776_p1`** | READY: `READY_KS-1776-KS-1776-ks_1776_p1_spark-dsv4flash_BRIEFED-CODEPATCH-AUTH-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1776_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/auth/src/routes/auth.ts` (exists at pin)
- The fix SHAPE (product try/catch) is the drafter's; alternatives: fix only the offending test's mock, or move the seed out of module scope.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR K: KS-1197 api-gateway enforcement.ts non-string verificationLevel ranks as none  [HOLD-WITH-DECISION]
- **Pass `ks_1197_p1`** | READY: `READY_KS-1197-KS-1197-ks_1197_p1_spark-dsv4flash_BRIEFED-CODEPATCH-ENFORCEMENT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts` (exists at pin)
- Partial, consumer-side fix chosen by the drafter; the verify-handler half is not here. Refs only.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR L: KS-1701 originate: four hand-written platform-admin literals call isPlatformRole  [HOLD-WITH-DECISION]
- **Pass `ks_1701_p1`** | READY: `READY_KS-1701-KS-1701-ks_1701_p1_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-ISPLATFORMROLE-SUPERADMIN-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1701_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=1, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts` (exists at pin)
  - `Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/originate/src/routes/certifications.ts` (exists at pin)
  - `Blockchain/Dev/services/originate/src/routes/documents.ts` (exists at pin)
- Access WIDENS: SUPER_ADMIN and mixed-case spellings become platform admin at four sites. Four files incl. the shared test helper. Not strict-apply.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR M: KS-1240 api-gateway fetch timeouts, three passes (auth.ts, proxy.ts + admin.ts, batch.ts + audit-export.ts)  [HOLD-WITH-DECISION]
- **Pass `ks_1240_p1`** | READY: `READY_KS-1240-KS-1240-ks_1240_p1_spark-dsv4flash_BRIEFED-CODEPATCH-GATEWAY-AUTH-FETCH-TIMEOUT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (exists at pin)
- **Pass `ks_1240_p2_proxy_admin`** | READY: `READY_KS-1240-KS-1240-ks_1240_p2_proxy_admin_spark-dsv4flash_BRIEFED-CODEPATCH2-PROXY-ADMIN-FETCH-TIMEOUT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p2_proxy_admin/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=1, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/api-gateway/src/routes/admin.ts` (exists at pin)
  - `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts` (exists at pin)
- **Pass `ks_1240_p3_batch_audit`** | READY: `READY_KS-1240-KS-1240-ks_1240_p3_batch_audit_spark-dsv4flash_BRIEFED-CODEPATCH2-BATCH-AUDIT-FETCH-TIMEOUT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p3_batch_audit/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` (exists at pin)
  - `Blockchain/Dev/services/api-gateway/src/routes/batch.ts` (exists at pin)
- Timeout values 5 s / 30 s / 120 s / 30 s are the drafter's; p1 answers 401 (not the ticket's 503) on timeout; p2 is not strict-apply.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR N: KS-1240 api-gateway tokenisation.ts fetch timeouts  [HOLD-WITH-DECISION]
- **Pass `ks_1240_p6_tokenisation`** | READY: `READY_KS-1240-KS-1240-ks_1240_p6_tokenisation_spark-dsv4flash_BRIEFED-CODEPATCH-TOKENISATION-CLIENT-FETCH-TIMEOUT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p6_tokenisation/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=1, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts` (exists at pin)
- 10 s is the drafter's AND tokeniseFields/detokeniseValues have no callers at the pin: Wednesday rules whether a PR for unused code is wanted. Not strict-apply.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR O: KS-1240 auth social providers fetch timeouts (github, google, linkedin, apple, facebook, microsoft-personal)  [HOLD-WITH-DECISION]
- **Pass `ks_1240_p4_social`** | READY: `READY_KS-1240-KS-1240-ks_1240_p4_social_spark-dsv4flash_BRIEFED-CODEPATCH2-SOCIAL-GITHUB-GOOGLE-LINKEDIN-FETCH-TIMEOUT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p4_social/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=1, lenient(`--recount --ignore-whitespace -C1`) rc=1
  - `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/auth/src/providers/social/github.ts` (exists at pin)
  - `Blockchain/Dev/services/auth/src/providers/social/google.ts` (exists at pin)
  - `Blockchain/Dev/services/auth/src/providers/social/linkedin.ts` (exists at pin)
- **Pass `ks_1240_p5_social2`** | READY: `READY_KS-1240-KS-1240-ks_1240_p5_social2_spark-dsv4flash_BRIEFED-CODEPATCH2-SOCIAL-APPLE-FACEBOOK-MSPERSONAL-FETCH-TIMEOUT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p5_social2/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=1, lenient(`--recount --ignore-whitespace -C1`) rc=1
  - `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/auth/src/providers/social/apple.ts` (exists at pin)
  - `Blockchain/Dev/services/auth/src/providers/social/facebook.ts` (exists at pin)
  - `Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts` (exists at pin)
- 10 s is the drafter's; timeout surfaces as a 400 on the login callback and an unclassified rejection on POST /social/link. Both passes are REANCHORED, not strict-apply.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR P: KS-1240 nft-certificate ipfs.service.ts fetch timeouts  [HOLD-WITH-DECISION]
- **Pass `ks_1240_p7_ipfs`** | READY: `READY_KS-1240-KS-1240-ks_1240_p7_ipfs_spark-dsv4flash_BRIEFED-CODEPATCH-IPFS-PROVIDER-FETCH-TIMEOUT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p7_ipfs/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts` (exists at pin)
- Three bounds 60/15/30 s are the drafter's; scope extension beyond the gateway ticket; a body stall during the gateway read is NOT mapped to the 503 the comment promises.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).

#### PR Q: KS-1240 tenant-provisioning fetch timeouts  [HOLD-WITH-DECISION]
- **Pass `ks_1240_p8_provisioning`** | READY: `READY_KS-1240-KS-1240-ks_1240_p8_provisioning_spark-dsv4flash_BRIEFED-CODEPATCH2-PROVISIONING-FETCH-TIMEOUT-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p8_provisioning/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=1, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/tenant-provisioning/src/index.ts` (exists at pin)
  - `Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts` (exists at pin)
- A key-generation timeout yields a 201 key-less tenant (keyFile null); 10 s values are the drafter's; scope extension. Not strict-apply.
- **NEEDS WEDNESDAY'S RULING BEFORE THIS PR OPENS** (the decision note is at the foot of each READY file named above, under `## DECISION NOTE`).


### WAVE 3 (sequenced after PR G merged)

#### PR H2: KS-1780 originate adminConfig.ts catches (p2_admin)  [HOLD]
- **Pass `ks_1780_p2_admin`** | READY: `READY_KS-1780-KS-1780-ks_1780_p2_admin_spark-dsv4flash_BRIEFED-CODEPATCH-ADMINCONFIG-PASS-7of7_2026-10-28.diff.md` | canonical patch: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p2_admin/out.md.checker/patch.diff` | whole-patch `git apply --check` at bd6697e079fc: strict rc=0, lenient(`--recount --ignore-whitespace -C1`) rc=0
  - `Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts` (NEW file (absent at pin))
  - `Blockchain/Dev/services/originate/src/routes/adminConfig.ts` (exists at pin)
- SHARES adminConfig.ts WITH PR G: open it only after PR G has MERGED, branch from the develop that contains G, and re-run git apply --check there. Not file-disjoint from G: that is the one sequenced pair.

## APPLY MODES (measured by the checker; the whole-patch strict/lenient matrix at the pin is in each PR line above)
Strict `git apply --check` of the whole `patch.diff` at `bd6697e079fc` FAILS for 7 of the 23 passes: `ks_1701_p1`, `ks_1240_p4_social`, `ks_1240_p5_social2`, `ks_1240_p6_tokenisation`, `ks_1240_p8_provisioning`, `ks_1240_p2_proxy_admin`, `ks_1779_p1`. Strict is NOT claimed for them. The checker accepted them per section:
- **lenient** = `git apply -p1 --recount --ignore-whitespace -C1` on that section only: `ks_1701_p1` sections 1-2 (documents.ts, certifications.ts), `ks_1240_p6_tokenisation` section 1, `ks_1240_p8_provisioning` section 1 (meteringKey.ts), `ks_1240_p2_proxy_admin` proxy.ts + admin.ts, `ks_1779_p1` (apply_mode=fuzzy; read its READY file's Sections lines).
- **REANCHORED** (the checker rebuilt every hunk of the section from its -/+ lines at the file's real location because the model's context did not match): `ks_1240_p4_social` and `ks_1240_p5_social2`, product sections 1-3. Apply the `section_N.reanchored.diff` files from the run dir's `out.md.checker/` (named in each READY file's CANONICAL PATCH note), never `patch.diff`. A strict check of `patch.diff` fails (`patch failed: ...github.ts:1`).
- Strict (whole patch clean at the pin): the other 16.
Rule for the seat: apply in the recorded mode, then prove the result with `git diff --stat` (exactly the files named for that PR, nothing else), and byte-compare every added line of a lenient/reanchored section against the READY file's diff block. If the applied product lines differ from the READY file's `+` lines, STOP.

## PER-PR PROOF (every PR)
1. Fresh clone, armed (WORK CLONE below). Pin develop at your boot; write it and its read time in the PR body.
2. Apply in the recorded mode; `git diff --stat` exactly the files listed; check the disk exec bit of every 100755 file after applying.
3. Run the package's own test file(s) and the **whole package suite before and after, keyed by cell NAME** (print failed/total; `0 total` is a load failure; 0 vanished). Run `npm run lint` and a `tsc --noEmit` that INCLUDES the test files (a child tsconfig with `exclude: []` and a listed-file-count control), per the model brief `fleet/briefs_staged/2026-10-20_seatD26_raise_spark_screen21.md` section 3. Do not copy the checker's numbers; re-measure and say which instrument.
4. **Red-proof the new test yourself:** with the test file alone (product reverted to the pin), the RED cells fail BY ASSERTION (not a load failure); with the product hunk, all pass. A source-text test (KS-1670, KS-1240 p2/p3/p8, KS-1701) proves the text, not the behaviour: the PR body says so.
5. **Test-change docs (repo skill `.claude/skills/secuura-test-discipline` section 4):** every Secuura test change updates BOTH `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` and `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` in the SAME commit: append the ticket's own entry in the shape of an existing one (KS-1364's is the example); both files, every time; the path has a SPACE, quote it in every shell command or the update silently resolves to nothing; if a PR's change truly affects neither doc, say so and why instead of skipping. These two files are the ONE place the PRs overlap by design: a docs-only conflict is resolved at the MERGE step, not before the gate (STANDING_LINES, 2026-10-27): push your head once, open the PR even if GitHub reads it CONFLICTING on the two docs only, and let the merger rebuild them and renumber the flow-diagram section to develop's highest + 1. A conflict in ANY other file is a STOP.
6. PR body states: what the Spark did (a local model wrote this patch; the checker's verdict; golden byte-identical), the apply mode, `Refs <ticket>`, what is NOT covered, and for every item flagged DECISION the ruling Wednesday gave (quote the ANSWER mail's subject). Key scanner over title, body and every commit message before pushing: the PR names only its own ticket hyphenated (`KS-1240`), every foreign key spaced or bare (`KS 1591`); declared squash subject carries no `(#n)` suffix; no attribution trailer the GO forbids.
7. **READY FOR GATE, one mail per PR** (STANDING_LINES "READY FOR QA"): PR number, head sha read from origin (`ls-remote`) in the same action, a ticket comment naming the PR (BLUF, ticket comments are the only client-facing channel), the Test Evidence block you ran, what was NOT covered, the predicted landing tree beside the develop sha it was computed against. Then stop. No merge.

## HOLD-WITH-DECISION ITEMS (HISTORY: RULED at the top of this brief — I and C accepted, J-Q not this round; no QUESTION mail needed)
Each is a PR in WAVE 2. Ask by QUESTION mail, one question per mail, topic `ruling PR <letter>`; open the PR only on the matching `[Wednesday -> ...] ANSWER: ruling PR <letter>`. The note is the foot of the READY file.
- **PR I (KS-1219):** a JSON `null`/`0`/`false` scope now answers 400 where it used to be read as absent (default allow-list). Accept?
- **PR C (KS-1467 auth):** 3 weak-password 422s now carry `error.details = { feedback }`; can the feedback ever echo the candidate password? Accept the visible change?
- **PR J (KS-1776):** product try/catch (drafter's shape) vs fix only the offending test mock vs move the seed out of module scope.
- **PR K (KS-1197):** consumer-side fix (enforcement.ts) vs validating the claim at the source; partial (POST /api/documents half only).
- **PR L (KS-1701):** access WIDENS: `SUPER_ADMIN` and mixed-case spellings become platform administrator at four originate sites. Wanted? Also interplay with PR A (isPlatformRole changes in packages/shared); files disjoint, either order, say so in both bodies.
- **PR M (KS-1240 gateway, three passes):** timeout values 5 s (auth.ts), 30 s / 120 s (proxy.ts, admin.ts), 30 s (batch.ts, audit-export.ts) are the drafter's; auth.ts answers 401 on timeout, not the ticket's 503; an admin create or a large audit export slower than the bound now ends in 502; the signal also bounds the body read.
- **PR N (KS-1240 tokenisation):** 10 s is the drafter's; `tokeniseFields` and `detokeniseValues` have NO callers at the pin (found at source by operator 3): is a PR for unused code wanted now?
- **PR O (KS-1240 social providers):** 10 s is the drafter's; a hung provider now ends as a 400 `OAuth authentication failed: <abort text>` on the login callback (state already consumed) and an unclassified rejection on `POST /social/link` (auth.ts:1360 has no local try); accept or add handling in a separate ticket?
- **PR P (KS-1240 ipfs):** bounds 60/15/30 s are the drafter's; scope extension beyond the gateway ticket; a body stall in the gateway read (`await response.arrayBuffer()`, outside the try) is NOT mapped to the 503 the constants comment promises, and a >30 s download now fails.
- **PR Q (KS-1240 provisioning):** a key-generation timeout creates an ACTIVE tenant with `vault_key_hash` NULL and answers 201 `success: true` with `keyFile: null`; 10 s values are the drafter's; scope extension. Acceptable?
Wave-1 and wave-3 PRs carry decision-free HOLDs, but several still need a sentence in the body (PR D: Refs, source-text pin; PR F: groundwork, Refs KS-1536; PR A: R3 of the security test accepts 401 or 403 for an array role; PR H2: sequenced after G).

## SEQUENCING AND ORDER
Wave 1 first, in this order (smallest hook risk first, one push at a time through the queue): B, A, D, F, E, H1, G. Wave 2 PRs open only as rulings arrive, in the order they arrive. Wave 3 = H2 after Wednesday reads PR G merged at origin.
Group files, ticket by ticket: every pair of PRs is file-disjoint except G/H2 (adminConfig.ts) and the two docs. Between two KS-1240 PRs there is no shared code file (M: api-gateway auth.ts, proxy.ts, admin.ts, batch.ts, audit-export.ts; N: api-gateway services/tokenisation.ts; O: auth providers/social/*; P: nft-certificate; Q: tenant-provisioning). Different constants share one name (module-local).

## HOLDS
- Signature classes pause for Kam: production, money, external communication, anything irreversible. No box, no `az`, no deploy, no Docker on the Studio. These PRs are not deployed; everything is `Refs`.
- **SHARED INBOX (read before you send or act on any mail):** you share ONE inbox (`secuura-blockchain@agentmail.to`) with every Secuura seat. **Seat D 38th (pane %53) is LIVE on that inbox deploying `bd6697e079fc` to the boxes; it touches NO code, opens no PR, and edits no source.** A mail naming Seat D 38th, a box, a deploy or `bd6697e079fc` deploy status is not yours; do not answer it, do not act on it. Subjects you send carry `[Secuura/Blockchain-<lane> -> Wednesday]` and your seat's name, and never the words hold / stop / checkpoint (routing tokens).
- **PUSH-WINDOW LOCK (STANDING_LINES, 2026-10-26/27):** one hook runs 11-15 min and several seats share the laptop. Join the first-come queue once per push (`T=$(PUSH_QUEUE_PID=<your waiter pid> bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/push_queue.sh join "Seat <X> <N>th")`, poll `push_queue.sh turn "$T"` until rc 0, `push_queue.sh leave "$T"` after release or on giving up), THEN take the lock only by your OWN successful `mkdir <Project>/worktrees/.push-lock` (+ a `holder` line, written only if YOUR mkdir created the dir; set a flag inside the loop on the mkdir that succeeded and proceed only on that flag; read the stderr of a failed mkdir; poll at 3 s or less, bounded). With the lock held, `pgrep -fl '^/bin/sh [.]githooks/pre-push origin git@github[.]com:'` must print nothing (the anchor is load-bearing, never simplify it) and load1 < 16; one timeout-shaped retry at load1 < 12. Release = `rm "$LOCK/holder"` then `rmdir "$LOCK"`, rc on its own line, a failed release is a loud STOP; release only after the push's rc and an `ls-remote` are in hand. A seat with several branches releases between them.
- **PER-COMMAND SSH KEEPALIVE (STANDING_LINES "Long pushes need ssh keepalives", measured 2026-10-26):** GitHub closes an idle ssh connection after ~6 minutes; `git push` opens it BEFORE the pre-push hook, so an 11-15 min hook dies at exit 141 with nothing on origin even when every leg passed. For THAT ONE push command only (never in `.git/config`, never a session export): `GIT_SSH_COMMAND="$(git config --get core.sshCommand) -o ServerAliveInterval=15 -o ServerAliveCountMax=120" git push <args>`; in a fresh clone `core.sshCommand` is UNSET, so supply the deploy key explicitly (`-i <the project's 3_Access_Keys/github_deploy_rw> -o IdentitiesOnly=yes -o StrictHostKeyChecking=accept-new`) and never export `GIT_SSH_COMMAND` in a shell that runs a push tool. After any push, `git ls-remote origin <branch>` in the SAME action before writing that it landed. An rc 141 with the ref unmoved is the known class: report it, retry under the lock, report elapsed time and attempt count rather than loop.
- Stop ONLY processes you started, by the PID you recorded; never pkill/killall/kill $(pgrep ...) by name (several seats run the same tools under the same names).
- No `--no-verify`, no force push, no `--admin`; push a NEW branch from the checked-out HEAD; to catch up with develop MERGE it in (never rebase a pushed branch). Before pushing, read `.githooks/pre-push` at your pin and cite the line that allows each push. A gating read (ls-remote before a merge, `git diff --cached` before a commit) is its own call, read, then the action. Name develop by the SHA just read (`ls-remote`), never `origin/develop`, in every merge-tree / merge-base / overlap check.
- Never delete (quarantine to a dated folder); a control must be able to fail; an exit code is read on its own line, never through a pipe; a private TMPDIR must be SHORT (`/tmp/<seat>`); rotate inside your own 80-90 band at a clean boundary, handover first.

## WORK CLONE
Cut ONE fresh clone from GitHub per PR family under `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/deploy-clones/seat<X><N>-<12-hex of the develop sha>` (absolute path outside the project checkout, a NON-EXISTENT path; assert `git -C <dir> rev-parse --show-toplevel` equals <dir> before any fetch or write). Then read back and quote in the plan confirmation: (1) `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`, then `git config --get core.hooksPath` (a fresh clone has NO pre-push gate); (2) `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai`, then `git config --show-origin user.email`; (3) `npm ci --ignore-scripts`, `npm run build --workspace=packages/shared`, ASSERT `packages/shared/dist/index.js` exists (originate and api-gateway suites cannot run without it); for originate also `npm run generate --workspace=services/originate`; (4) `npm ci` in every `systemTest/*` package enumerated from git (REFUSE if the count is 0). A worktree has no per-worktree git config: pass identity per command if you use worktrees. Drive hygiene: at wrap, remove or move the clones you made for merged work and report GB freed by `df`, not `du`.

## PARTITION
**Yours (the 55 files below, one PR each as grouped above, in your own clones), plus the two docs and `5_Project_History/<date>_seat<X>-<N>th/`:**
- PR A (KS-1591): `Blockchain/Dev/packages/shared/src/__tests__/ks1591-is-platform-role-is-an-exact-ascii-fold.test.ts`, `Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts`, `Blockchain/Dev/services/security/src/__tests__/ks1591-require-key-admin-is-an-exact-ascii-fold.test.ts`, `Blockchain/Dev/services/security/src/index.ts`
- PR B (KS-1467): `Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts`, `Blockchain/Dev/packages/shared/src/errors/index.ts`
- PR D (KS-1670): `Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts`, `Blockchain/Dev/services/m365-integration/src/index.ts`
- PR E (KS-1250): `Blockchain/Dev/scripts/__tests__/smoke_test_honours_smoke_base_url.test.sh`, `Blockchain/Dev/scripts/smoke-test.sh`
- PR F (KS-1536): `Blockchain/Dev/services/auth/src/__tests__/ks1536-issuer-certs-admin-role-gate-is-one-helper.test.ts`, `Blockchain/Dev/services/auth/src/routes/issuerCerts.ts`
- PR G (KS-1779): `Blockchain/Dev/services/originate/src/__tests__/ks1779-migrate-tenant-data-loop-has-no-lint-warnings.test.ts`, `Blockchain/Dev/services/originate/src/routes/adminConfig.ts`
- PR H1 (KS-1780): `Blockchain/Dev/services/originate/src/__tests__/ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts`, `Blockchain/Dev/services/originate/src/routes/systemErrors.ts`, `Blockchain/Dev/services/originate/src/utils/pgErrors.ts`
- PR H2 (KS-1780): `Blockchain/Dev/services/originate/src/__tests__/ks1780-admin-config-catches-cannot-hang-on-a-hostile-throw.test.ts`, `Blockchain/Dev/services/originate/src/routes/adminConfig.ts`
- PR I (KS-1219): `Blockchain/Dev/services/auth/src/__tests__/ks1219-authorize-refuses-an-array-valued-scope.test.ts`, `Blockchain/Dev/services/auth/src/routes/oauth.ts`
- PR C (KS-1467): `Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts`, `Blockchain/Dev/services/auth/src/middleware/errorHandler.ts`, `Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts`
- PR J (KS-1776): `Blockchain/Dev/services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts`, `Blockchain/Dev/services/auth/src/routes/auth.ts`
- PR K (KS-1197): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts`, `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts`
- PR L (KS-1701): `Blockchain/Dev/services/originate/src/__tests__/helpers/sharedModuleMock.ts`, `Blockchain/Dev/services/originate/src/__tests__/ks1701-platform-admin-checks-use-is-platform-role.test.ts`, `Blockchain/Dev/services/originate/src/routes/certifications.ts`, `Blockchain/Dev/services/originate/src/routes/documents.ts`
- PR M (KS-1240): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-every-hand-built-gateway-fetch-in-proxy-and-admin-is-bounded.test.ts`, `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts`, `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-the-batch-and-audit-export-upstream-fetches-are-bounded.test.ts`, `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts`, `Blockchain/Dev/services/api-gateway/src/routes/admin.ts`, `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts`, `Blockchain/Dev/services/api-gateway/src/routes/batch.ts`, `Blockchain/Dev/services/api-gateway/src/routes/proxy.ts`
- PR N (KS-1240): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-tokenisation-client-fetches-are-bounded.test.ts`, `Blockchain/Dev/services/api-gateway/src/services/tokenisation.ts`
- PR O (KS-1240): `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded-apple-facebook-microsoft.test.ts`, `Blockchain/Dev/services/auth/src/__tests__/ks1240-social-provider-fetches-are-bounded.test.ts`, `Blockchain/Dev/services/auth/src/providers/social/apple.ts`, `Blockchain/Dev/services/auth/src/providers/social/facebook.ts`, `Blockchain/Dev/services/auth/src/providers/social/github.ts`, `Blockchain/Dev/services/auth/src/providers/social/google.ts`, `Blockchain/Dev/services/auth/src/providers/social/linkedin.ts`, `Blockchain/Dev/services/auth/src/providers/social/microsoft-personal.ts`
- PR P (KS-1240): `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1240-ipfs-provider-fetches-are-bounded.test.ts`, `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts`
- PR Q (KS-1240): `Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1240-tenant-provisioning-fetches-are-bounded.test.ts`, `Blockchain/Dev/services/tenant-provisioning/src/index.ts`, `Blockchain/Dev/services/tenant-provisioning/src/meteringKey.ts`
- Granted for appending the ticket's own entry in every PR that adds a test (all of them): `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (exists at pin), `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` (exists at pin)

**Not yours (each path below checked with `git cat-file -e bd6697e079fc:<path>`, exists at the pin):**
- `.githooks/pre-push`: read-only: read the refusal branches, cite the line that allows each push; never edit
- `Blockchain/Dev/scripts/audit/audit-baseline.json`: the audit baseline (KS-1707's lane): a push refused by an audit leg is reported, never fixed here
- `Blockchain/Dev/services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.ts`: the hermetic manifest: NOT granted. If a new originate test needs a manifest line, STOP and ask (the checker's whole-suite run A6 was green without one)
- `Blockchain/Dev/services/auth/src/routes/users.ts`: users.ts:993 is the third weak-password ValidationError site that PR C's behaviour change reaches; it is NOT edited
- `Blockchain/Dev/services/api-gateway/src/index.ts`: the gateway entry point: no pass touches it
- `Blockchain/Dev/packages/shared/src/index.ts`: the shared package barrel: PR A and PR B edit other files of packages/shared, never this one
- `Blockchain/Dev/services/m365-integration/src/index.ts`: GRANTED to PR D only (KS-1670 site 1, one line); every other m365 file and line is not yours
- Seat D 38th (pane %53): a DEPLOY seat on the shared inbox; it edits no source and you do not touch its clone, boxes or mail. Any other seat's open PR (14 open at the operator's read, 93 file entries, 0 overlapping your files).
- `2_Project_Files` of the project checkout: READ-ONLY. Read repo files from a SHA, never from the Secuura MAIN checkout's working tree.

## PROTOCOL AND MAIL
Read the launch preflight file in your FIRST tool call and quote it VERBATIM, stamp and warnings included, into your plan confirmation (QUESTION mail, topic `plan confirmation`): clone facts read back, the develop sha, the per-PR apply result in its recorded mode, the wave plan. Wednesday confirms against this brief; a plan that deviates (a product line, a third file, a hand-merge, a decision item opened early) pauses for Wednesday and Kam. One question per mail (`[Secuura/Blockchain-<lane> -> Wednesday] QUESTION: <topic>`; sections Context / Question / Meanwhile / Needed-by); answers arrive as `[Wednesday -> Secuura/Blockchain-<lane>] ANSWER: <topic>`. Mail every state change; never end a turn on a "next up" line with nothing running. Approval-class items always pause for Kam. No secrets in any mail.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Card wed-spark-drafting-cost-1028 = b (Kam, live board 2026-10-28 16:42:24): keep briefing the Spark in full batches. Context only: it is why these passes exist; nothing for you to do.
- Kam, live board 2026-10-28 16:4x: "keep working and use as many agents as you can to go through all the tickets" -> other Secuura seats may launch beside you on DISJOINT files; every one is named on the shared inbox. A mail naming another seat is not yours.
- 92 older secuura- cards carry no delivery mark in the queue (gate count at send); none rules on these ten PRs' files or behaviour as far as Wednesday read (UNMEASURED per card): if a ticket you open names a Kam ruling, read the ruling's card (`decision_queue.sh show <id>`) and mail before acting on it.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- The rulings at the top of this brief (PR I accepted; PR C accepted on the no-echo cell; J-Q not this round), 2026-10-28 16:5x.
- Spark passes are raised, gated and GO'd by Wednesday; a raise seat never merges (standing since 2026-10-05).
- Peter's open PRs stay his; never touch, comment on or merge another author's PR.

PROVENANCE:
- Develop tip `bd6697e079fce41db6b21e094a9eddb3d0e1d08e` | `git -C <hold clone> ls-remote origin refs/heads/develop` | read 2026-10-28 ~16:00 AEDT (operator 3)
- The 23 passes: PASS 7/7, byte-identical to goldens | `local-model/spark/done.md` rows 13:4x-14:46 and the 23 READY files in `local-model/night/` (checker artefacts copied verbatim by hold_ready.py) | read 2026-10-28
- Per-pass file lists | each brief's `golden.diff` `+++ b/` headers (`local-model/night/briefs/<tag>/golden.diff`) | read 2026-10-28 by script; 55 distinct paths; 32 exist at the pin, 23 are NEW test files (absent at the pin)
- Whole-patch strict/lenient matrix at the pin | `git apply --check` of each `out.md.checker/patch.diff` in a clean clone at `bd6697e079fc` (copied into 0_Brain/reference/2026-10-28_spark-operator3/report.md) | read 2026-10-28
- Open PRs: 14, 93 file entries, 0 overlap with the 55 files | `gh pr list -R Secuura/Distributed_Secuura --state open --json number,files` with the project's own GH_TOKEN in a scratch GH_CONFIG_DIR, read-only | read 2026-10-28
- Decision items (13) | the `## DECISION NOTE` at the foot of each of the 13 HOLD-WITH-DECISION READY files (7 by operators 1-2, 6 by operator 3; operator 3's findings were read at source at `65bc2823`) | read 2026-10-28
- Routing rows C1/C2 | `fleet/specs/model-routing.md:91-92` | read 2026-10-28

UNMEASURED (read these yourself): Linear ticket states for the ten PRs' tickets (read each before its PR; mail any that is Done/closed); whether any seat other than D 38th is live on these files now beyond the 14 open PRs (the pane list at launch held only D 38th).

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-28 16:50 (BLUF, rulings, decision section and PARTITION agree: ten PRs, J-Q excluded)
