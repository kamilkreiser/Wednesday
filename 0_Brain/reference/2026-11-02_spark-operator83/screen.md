# Operator 83 screen: further KS-1868 supply at develop 0e3a9b65cdd6 (2026-11-02 late evening)

Method: `git grep -E "(instanceof Error \? X.message : String\(|String\((err|error|e)\)|\b(err|error|e)\??\.message)"` over `Blockchain/Dev/services/*/src` non-test files at the tip (screen_raw.out, 289 hits, 75 files), then the never-brief filter (open-PR files from open_prs_start.json: 23 PRs / 160 files, planted control services/originate 16 entries; every held file of O80/O81/O82 in held_files.out; governance; originate gdprService.ts, db.ts, verification.ts, verificationV2.ts, certifications.ts, certificationRepo.ts, retentionScheduler.ts; every service src/index.ts except security; billing/money), then reading the catch context. "Read depth": D = catch and its caller path read; S = catch shape and the lines around it read only. Zod pre-check sites: none among the rows below (the pre-read sites are listed as SKIP). Rule applied to every row: the guard sits only in the catch, so the state before the catch is the same for a hostile value and an ordinary Error; a row is QUALIFIES when the catch does nothing with the value except log it (then answer/continue) and the hostile value can reach it; ordinary-equal = yes means the after-state is exactly the ordinary-Error one.

## A. Briefed by this operator (held or queued; see report.md)
| site | file:line | today (hostile) | after | ordinary-equal | verdict |
|---|---|---|---|---|---|
| revoke-on-rotate catch | security/src/index.ts:306 | log() JSON.stringify throws in catch, `revokePriorConnectorKeys` rejects (in-memory priors already retired) | returns null, as ordinary | yes | O83-P1 HELD |
| revoke-on-rotate savepoint catch | security/src/index.ts:419 | callback rejects after ROLLBACK TO SAVEPOINT, whole rotate transaction rolls back, POST /api/keys 500, no key issued | null, transaction commits, 201 with priorKeysRevoked null (the ordinary row) | yes | O83-P1 HELD |
| sign/request catch | originate/src/routes/documents.ts:1285 | no answer + unhandled rejection | constant 500 | yes | O83-P2 |
| lifecycle-events list catch | documents.ts:3196 | same | constant 500 | yes | O83-P2 |
| sig-json catch (public) | documents.ts:3718 | same | constant 500 | yes | O83-P2 |
| sign catch | documents.ts:1366 | same | constant 500 | yes | O83-P3 |
| sign-cert catch | documents.ts:3468 | same | constant 500 | yes | O83-P3 |
| sign-wallet catch | documents.ts:3657 | same | constant 500 | yes | O83-P3 |
| logDegraded Redis-error read | api-gateway/src/middleware/rateLimitEnforce.ts:51 | read throws inside the try, request let through UNCOUNTED (`in-memory fallback ALSO failed`) | degrades to the in-memory ceiling, request counted, limit applies | yes | O83-P4 |
| writeErr catch | rateLimitEnforce.ts:302 | middleware rejects | request let through, line logged | yes | O83-P4 |

## B. Qualifying, NOT briefed (supply). Counts are sites.
| group | file:line | today -> after (ordinary-equal) | depth | note |
|---|---|---|---|---|
| issuer cert sweep (auth) | auth/src/services/issuerCertSweep.ts:66 | hostile markExpiredCerts error aborts the whole sweep (no expiring-soon pass, rejects to the timer catch); after: continues as the ordinary Error does (yes) | D | best next pass; 6 sites: 66, 83, 95, 113, 155, 163 (the .catch arrow bodies need block bodies); TIER 1 (issuer certs); vitest |
| oauth state (auth) | auth/src/services/oauthState.ts:136 | hostile Redis error: callback handler rejects; after: logs and `return false`, callback refused (yes) | D | 1 site |
| gateway audit write | api-gateway/src/middleware/audit.ts:334 | fire-and-forget IIFE: a hostile write error becomes an unhandled rejection; after: warn line (yes) | D | 1 site |
| gateway brute force | api-gateway/src/middleware/security.ts:198 | hostile Redis error: request hangs; after: `next()` (the file's documented fail-open, ordinary row) (yes) | D | 1 site; TIER 1 |
| gateway document-create last line of defence | api-gateway/src/routes/verification.ts:952 | the `.catch` that exists to stop `unhandledRejection -> gracefulShutdown` throws inside itself, so the gateway exits (per the comment at :949); after: log + 500 if headers not sent (yes) | D | highest value single site; harness is the document-create pipeline (heavy) |
| gateway clone | api-gateway/src/routes/platform.ts:1092 | `console.error` then constant 500 'Clone failed'; hostile: no answer; after constant 500 (yes) | S | tenant clone endpoint; TIER 1 |
| originate documents.ts other routes | documents.ts:1092, 1237, 1860, 2507, 2726, 3027, 364, 232, 1451 | constant 500 after the log (232 is a seed `.catch`, 1451 returns the `pending` anchor); hostile: no answer (yes) | S for 1092/1860/2507/2726/3027/232/1451, D for 364 and 1237 | 364 and 1237 have an inner `dbErr?.message?.includes` that throws a TypeError first for a hostile `listDocuments`/`getDocument` rejection, so the outer catch is reached by a hostile value only from a LATER step: needs a different red cell; 9 sites |
| errorTrackingService | originate/src/services/errorTrackingService.ts:141 | returns `{errors:[],total:0}` after the log; hostile: rejects (yes) | D | 1 site |
| lifecyclePayloadCodec | originate/src/utils/lifecyclePayloadCodec.ts:58 | returns `{payloadUnavailable:true}`; hostile: rejects the whole list (yes) | D | 1 site |
| anchorStateSync | originate/src/services/anchorStateSync.ts:600 | verify-heal write swallow; hostile: rejects the verify (yes) | S | 1 site; anchoring |
| tokenisation vault | tokenisation/src/vault.ts:81 | decrypt-failed `console.error` then `{token, value:null}`; hostile: rejects (yes) | D | 1 site; `(err as Error)?.message ?? String(err)` |
| shared stores (all services import them) | shared/src/security/redis-security-store.ts (15: 59,74,93,106,117,138,151,181,193,218,230,242,273,302,322); shared/src/cache/cache-middleware.ts (3), connection-pool.ts (5), compression.ts (1), redis-client.ts (1) | `logger.error(..., {error: String(error)})` then a fallback (null / fail-open / next()); hostile: String throws in the catch (yes, ordinary row) | S (two read: redis-security-store get/set) | 25 sites of the plain `String(x)` shape, fix = the `signatories.ts` guard; TIER 1 (rate-limit, brute-force and CSRF stores); shared package, the runner was not checked |
| originate platformOrganizations (erase-connector) | platformOrganizations.ts:112, 145, 168 | constant 500 after the log (yes) | D | qualifies by shape but is the GDPR erase route next to Seat E 29th (gdprService.ts, db.ts, KS-1943): HOLD until that lane lands |

Supply count: 6 + 1 + 1 + 1 + 1 + 1 + 9 + 1 + 1 + 1 + 1 + 25 = 49 sites that qualify and are not briefed (about 17 passes of 3; excluding the shared package 24 sites, about 8 passes).

## C. SKIP, with the reason (not counted)
| site | file:line | reason |
|---|---|---|
| rateLimit fallbackErr | rateLimitEnforce.ts:277 | once `logDegraded` is guarded (O83-P4) the catch is reached only by an in-process Map failure; no red cell can reach it; left as is |
| documentRepo catches | originate/src/repositories/documentRepo.ts:266, 298, 518, 697 | they log and RETHROW the original value; today a hostile value is replaced by the logger's own TypeError, which the route catches and answers 500; guarding only the repo lets the hostile original reach the route catches, most of which are unguarded: worse, not equal. Only after the documents.ts routes are guarded (P2/P3 and the rest of group B) |
| documentRepo.ts:504 fkMsg, lifecycleEventRepo.ts:82, shareRepo.ts:140, issuerCert.ts:114/199/219/349/363, mintError.ts:37, extractPgCode-first catches (documents.ts:2933, 3166) | pre-reads: the value is read to CLASSIFY (substring match / pg code / message built into a new error), not just logged: a Zod-pre-check-like half fix |
| mcp-server tools verify.ts/info.ts/register.ts (8 sites) | the message is echoed into the tool RESPONSE (`error: message`); the KS-1410/KS-1901 "never echo the thrown text" ruling decides the response first; `describeThrown` lives in http-server.ts (Seat V lane) |
| kyc microsoft-entra-client.ts:100, 129 | `error.response?.data ||` pre-read, then rethrown with `error.response?.data` |
| auth routes/health.ts:41, 61 | `String(error)` is returned in the health response body (echo) |
| api-gateway routes audit-export/batch/notifications | already carry the KS-1346 safe read |
| analytics services, vc-issuer credentialRepo/presentations, originate notificationClient/metering/errorTrackingService:67, nft-certificate cardano/provider.ts:68 | already guarded (`let reason ... catch { reason = 'unreadable thrown value' }`); only the coercion follow-up (G114-F1 class) would remain, not measured |
| billing/**, chargeEvents.ts | money, excluded |
| every src/index.ts except security, governance, gdprService.ts, db.ts, verification.ts, verificationV2.ts, certifications.ts, certificationRepo.ts, retentionScheduler.ts, minting.service.ts, nft.routes.ts, analytics.ts, errorHandler.ts files, kyc/microsoft-verification.ts | never-brief (open PR, held pass of O80-O82, or named by Wednesday) |
| anchoring threadMintRequest.ts:77, m365 token-manager.ts:214, cardano/index.ts:133, reanchorInFlight.ts:193/229, ownCreateClient.ts:88 | different read shapes (`typeof err?.message === 'string'` or the text copied into a returned/answered field); not read to a verdict (UNMEASURED) |
