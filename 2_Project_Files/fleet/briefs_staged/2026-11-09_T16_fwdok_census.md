# T 16th census: forward-apply status of every READY in local-model/night/ at develop 01b26bc772a7

Drafted by the T 16th brief drafter (Sonnet), 2026-11-09 02:0x AEDT. Read-only on the Secuura project. Pin: develop `01b26bc772a713e5e4d6ffc545f7fedeeeb4afe3` (`git ls-remote origin refs/heads/develop` via a scratch clone, read 02:06 and again at the end of the run, same value).

## Counts by class (272 READY_*.diff.md; each count names its instrument)
| class | n | instrument |
|---|---|---|
| input | 272 | `ls night/READY_*.diff.md \| wc -l` = 272, equal to the census rows read |
| FORWARD-APPLIES (FWD-OK) | 157 | operator 105 instrument (first ```diff fence, else the CANONICAL PATCH file; `git apply --cached --check` forward, strict, then `--unidiff-zero`) against a temp index of the pin tree; 0 NODIFF rows |
| REV-OK (diff already in the tip) -> class SPENT | 45 | same instrument, `-R` (strict, then `--unidiff-zero`), only for rows that do not apply forward |
| NEITHER -> class DRIFTED | 70 | same instrument, neither direction applies |
| of the 157 FWD-OK: TICKET-CLOSED | 64 | Linear GraphQL read, issue by identifier: state type completed/canceled, or archivedAt set. 59 archived (their state names are inside the list below) + 5 Done |
| of the 157 FWD-OK, ticket open: FILES-TAKEN | 12 | GitHub pulls API `state=open` (46 PRs, 277 file entries, GET only) + `/pulls/N/files`; a READY is taken when any path its diff touches (`+++ b/` lines, spaces kept) is in an open PR file list |
| of the remaining: PRESENT-AT-TIP (added lines already in the touched file) | 5 | every `+` line of 14+ chars stripped, found as a stripped line of the same file at the pin (`git show pin:path`); 100% of at least 3 lines. A fifth class beyond the four Wednesday named: the cells landed in another form and a forward apply would duplicate them |
| RAISE-READY | 76 | ticket open, applies forward, no file in an open PR, not PRESENT-AT-TIP. NOT all are queueable (see flags column; 4 carry PARTIAL-OVERLAP) |
| conservation | 157 = 76 + 5 + 12 + 64 (=157); 272 = 157 + 45 + 70 |

Also closed-ticket among the non-forward rows (Wednesday quarantines those too): DRIFTED 38 of 70, SPENT 18 of 45 (same Linear read). So closed-ticket READYs in all: 120.

## Controls (each was able to fail)
- Forward-apply control: the patch of READY_KS-1015-OWNER-LIST-1 with `ZZPLANTEDZZ ` inserted into its first `-` line: strict rc fail, `--unidiff-zero` rc fail; the unmutated patch passes strict. The seat can re-run this.
- Open-PR file match: PR 2093's one file `Blockchain/Dev/services/originate/src/__tests__/ks741-emitter-marker-strip.test.ts` is found by the matcher (hit [2093]); a made-up path `Blockchain/Dev/zz/none.ts` is found nowhere (None). `email.ts` (O105-P1) is in NO open PR file list while that control path is present in the list.
- Linear: KS-2053 (known, In Progress, Low) read back correctly; KS-99999 (does not exist) returns "Entity not found", so a miss is not silently read as Open. 122 distinct keys read, 0 errors and 0 nulls among the 272 rows.
- PRESENT-AT-TIP: by `git grep -F` of the first added test title at the pin, the five 100% rows each find their title in the touched file (KS-1175 anchor-readback line 114, identity-anchoring lines 234, 255, 438; KS-1284 anchor-readback line 80; KS-1524 ks1510 test line 110); KS-1812's titles find 0 (not present).

## Instrument limits (UNMEASURED)
- Each ticket's COMMENTS were not read; only state, priority, assignee, creator and archived flag. A comment may re-scope or close a ticket without a state change.
- PRESENT-AT-TIP / PARTIAL-OVERLAP is a line-presence heuristic, not a proof the cell is equivalent. The partial rows need a whole read by the seat.
- "Live lane" files (U 18th KS-2060 unpushed work, X 9th, B 102nd): the push queue `worktrees/.push-queue` listed 0 entries at 02:0x (`ls -la`), but a seat's unpushed worktree is not visible there. The seat reads `ps` and the queue before each cut.
- GitHub: only open PRs, 46 of them; a PR opened after 02:0x is not seen. Draft status not used.
- Strict vs `--unidiff-zero`: both flags report FWD-OK; the seat's own strict `git apply -p1` (no recount) on its worktree is the proof (a row that only applies under `--unidiff-zero` must be named; the census rows below show fs/fz).

## RAISE-READY + PRESENT-AT-TIP rows (priority first; P = Linear priority at source)
| key | P | state | assignee | READY (name head) | touched files (under Blockchain/Dev/ unless shown) | class | flags |
|---|---|---|---|---|---|---|---|
| KS-591 | High | In Progress | kamil.kreiser | KS-591-BILLINGCUSTOMERSBUNDLE-1_spark-dsv4flash_BRIEFED-CODEPATCH-BILL | services/billing/src/__tests__/ks591-billing-customers-bundle-body-required.test.ts, services/billing/src/billing.openapi.ts | RAISE-READY | creator peter; openapi source (yaml drift); kind: product bytes in 1 file(s) |
| KS-1175 | High | In Progress | kamil.kreiser | KS-1175-EXPLORERBASE-PER-NETWORK-1_ornith35b-q4_BRIEFED-TESTONLY-CARDA | services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts | PRESENT-AT-TIP | cells already at tip |
| KS-1175 | High | In Progress | kamil.kreiser | KS-1175-IDENTITY-EMPTY-OBJECT-1_ornith35b-q4_BRIEFED-TESTONLY-EMPTY-ID | services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts | PRESENT-AT-TIP | cells already at tip |
| KS-1175 | High | In Progress | kamil.kreiser | KS-1175-KS-1175-1805-1-DIDPINS_spark-dsv4flash_BRIEFED-TESTONLY-ANCHOR | services/anchoring/src/__tests__/ks1175-identity-anchoring.test.ts | PRESENT-AT-TIP | cells already at tip |
| KS-1284 | High | In Progress | kamil.kreiser | KS-1284-CHUNKED-DOCUMENTID-ROUNDTRIP-1_ornith35b-q4_BRIEFED-TESTONLY-C | services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts | PRESENT-AT-TIP | cells already at tip |
| KS-1410 | High | In Progress | kamil.kreiser | KS-1410-KS-1410-RESET500_spark-dsv4flash_BRIEFED-CODEPATCH-KS-1410 res | services/demo-service/src/__tests__/reset.test.ts, services/demo-service/src/routes/reset.ts | RAISE-READY | ticket named by open PR 2059; kind: product bytes in 1 file(s) |
| KS-758 | Medium | In Progress | kamil.kreiser | KS-758-UNRESOLVEDERASURELOG-1_spark-dsv4flash_BRIEFED-CODEPATCH-UNRESO | services/originate/src/__tests__/ks758-an-unresolvable-connector-erasure-leaves-an-audit-row.test.ts, services/originate/src/services/gdprService.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-902 | Medium | Backlog | kamil.kreiser | KS-902-O101-P1_spark-dsv4flash_BRIEFED-DOCONLY-NO-TRACKED-CREDENTIALS- | scripts/preflight/no-tracked-credentials.sh | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1015 | Medium | In Progress | kamil.kreiser | KS-1015-OWNER-LIST-1_spark-dsv4flash_BRIEFED-CODEPATCH-REFERRAL.OPENAP | services/referral/src/__tests__/ks1015-referral-lookup-spec-declares-envelope.test.ts, services/referral/src/referral.openapi.ts | RAISE-READY | creator peter; openapi source (yaml drift); kind: product bytes in 1 file(s) |
| KS-1152 | Medium | In Progress | kamil.kreiser | KS-1152-R1a_ornith35b-q4_comment-PASS-9of9_2026-09-17 | packages/shared/src/middleware/index.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); ticket named by open PR 2073; kind: product bytes in 1 file(s) |
| KS-1152 | Medium | In Progress | kamil.kreiser | KS-1152-R1b_ornith35b-q4_comment-PASS-9of9_2026-09-17 | services/originate/src/middleware/auth.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); ticket named by open PR 2073; kind: product bytes in 1 file(s) |
| KS-1156 | Medium | In Progress | kamil.kreiser | KS-1156-A2_ornith35b-q4_comment-PASS-9of9_2026-09-17 | services/api-gateway/src/middleware/scopes.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1171 | Medium | In Progress | kamil.kreiser | KS-1171-8j_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15 | services/anchoring/src/__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts | RAISE-READY | ticket named by open PR 2081; kind: test-only |
| KS-1232 | Medium | In Progress | kamil.kreiser | KS-1232-INFOEMPTY-1_ornith35b-q4_BRIEFED-TESTONLY-CONNECTOR-INFO-EMPTY | services/api-gateway/src/__tests__/ks480-connector-auth.test.ts | RAISE-READY | PARTIAL-OVERLAP 11/14 lines already at tip; kind: test-only |
| KS-1364 | Medium | In Progress | kamil.kreiser | KS-1364-ORIGINATESHARESYSTEMERRO-1_spark-dsv4flash_BRIEFED-CODEPATCH-O | services/originate/src/__tests__/ks1364-share-system-errors-body-required.test.ts, services/originate/src/originate.openapi.ts | RAISE-READY | creator peter; openapi source (yaml drift); kind: product bytes in 1 file(s) |
| KS-1524 | Medium | In Progress | kamil.kreiser | KS-1524-KS-1524_spark-dsv4flash_BRIEFED-TESTONLY-platform lookup logs  | services/api-gateway/src/__tests__/ks1510-document-lookup-logs-the-thrown-error.test.ts | PRESENT-AT-TIP | cells already at tip |
| KS-1705 | Medium | Backlog | kamil.kreiser | KS-1705-KS-1705-REQBODY1705-1_spark-dsv4flash_BRIEFED-CODEPATCH-spark- | services/security/src/__tests__/ks1705-security-keys-post-and-admin-scopes-put-bodies-are-required.test.ts, services/security/src/security.openapi.ts | RAISE-READY | creator peter; AUTH/SEC SURFACE (tier 1, Sonnet stops); openapi source (yaml drift); kind: product bytes in 1 file(s) |
| KS-1812 | Medium | Backlog | unassigned | KS-1812-KS-1812-P1_spark-dsv4flash_BRIEFED-TESTONLY-ANCHORSCHEMA-PASS- | services/anchoring/src/__tests__/anchorSchema.test.ts | RAISE-READY | kind: test-only |
| KS-1815 | Medium | Backlog | unassigned | KS-1815-KS-1815-P4_spark-dsv4flash_BRIEFED-TESTONLY-ANCHORSUBMISSION-P | services/anchoring/src/__tests__/ks726-write-ahead-tx-hash.test.ts | RAISE-READY | PARTIAL-OVERLAP 13/25 lines already at tip; kind: test-only |
| KS-1197 | Low | Backlog | kamil.kreiser | KS-1197-KS-1197-ks_1197_p1_spark-dsv4flash_BRIEFED-CODEPATCH-ENFORCEME | services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts, services/api-gateway/src/services/enforcement.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1544 | Low | In Progress | kamil.kreiser | KS-1544-KS-1544-O31-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-LOOSE-AUTH-I | services/auth/src/__tests__/ks1544-class-auth-issuer-certs-list-orders-in-a-total-order.test.ts, services/auth/src/repositories/issuerCertRepo.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1663 | Low | Backlog | unassigned | KS-1663-1663-OP7_spark-dsv4flash_BRIEFED-CODEPATCH2-ANCHOROVERWRITEGUA | services/anchoring/src/__tests__/ks1385-anchor-store-keeps-the-latest-events-metadata.integration.test.ts, services/anchoring/src/__tests__/ks1663-the-custody-join-comments-name-the-role-restricted-policy.test.ts, services/anchoring/src/anchorOverwriteGuard.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1776 | Low | Backlog | kamil.kreiser | KS-1776-KS-1776-ks_1776_p1_spark-dsv4flash_BRIEFED-CODEPATCH-AUTH-PASS | services/auth/src/__tests__/ks1776-demo-user-seed-timer-cannot-escape-as-an-uncaught-throw.test.ts, services/auth/src/routes/auth.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1783 | Low | Backlog | kamil.kreiser | KS-1783-KS-1783-ks_1783_c1_v2_spark-dsv4flash_BRIEFED-TESTONLY-VERIFIC | services/originate/src/__tests__/ks1634-v2-chain-only-match-carries-simulated.test.ts | RAISE-READY | PARTIAL-OVERLAP 2/4 lines already at tip; kind: test-only |
| KS-1783 | Low | Backlog | kamil.kreiser | KS-1783-KS-1783-ks_1783_c2_verify_route_spark-dsv4flash_BRIEFED-TESTON | services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash-verify-route.test.ts | RAISE-READY | kind: test-only |
| KS-1783 | Low | Backlog | kamil.kreiser | KS-1783-KS-1783-ks_1783_c3_verify_file_spark-dsv4flash_BRIEFED-TESTONL | services/originate/src/__tests__/ks1634-a-simulated-anchor-verified-by-hash.test.ts | RAISE-READY | kind: test-only |
| KS-1864 | Low | Backlog | kamil.kreiser | KS-1864-O32-P1_spark-dsv4flash_BRIEFED-TESTONLY-TYPEFIX-API-GATEWAY-3F | services/api-gateway/src/__tests__/ks1374-global-limiter-at-demo-limit.test.ts, services/api-gateway/src/__tests__/ks1464-limiter-key-hygiene.test.ts, services/api-gateway/src/__tests__/ks695-ask3-erase-connector-door.test.ts | RAISE-READY | kind: test-only |
| KS-1864 | Low | Backlog | kamil.kreiser | KS-1864-O33-P1_spark-dsv4flash_BRIEFED-TESTONLY-TYPEFIX-API-GATEWAY-RA | services/api-gateway/src/__tests__/rateLimitEnforce.test.ts | RAISE-READY | kind: test-only |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O105-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-EMAIL-PASS- | services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts, services/originate/src/services/email.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O84-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-BRIEFED-CODE | services/auth/src/__tests__/ks1868-issuer-cert-sweep-fire-and-forget-catches-unreadable-throw.test.ts, services/auth/src/services/issuerCertSweep.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O89-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-AUTH-ISSUER- | services/auth/src/__tests__/ks1868-issuer-cert-sweep-fire-and-forget-catches-unreadable-throw.test.ts, services/auth/src/services/issuerCertSweep.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O90-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-CE | services/originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts, services/originate/src/routes/certifications.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P10_spark-dsv4flash_BRIEFED-CODEPATCH2-ANCHORING-C | services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts, services/anchoring/src/cardano/index.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-M365-USER-ER | services/m365-integration/src/__tests__/ks1868-m365-user-erased-subscriber-loop-closed-catch-unreadable-throw.test.ts, services/m365-integration/src/userErasedSubscriber.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-AUTH-USER-ER | services/auth/src/__tests__/ks1868-auth-user-erased-subscriber-catches-unreadable-throw.test.ts, services/auth/src/services/userErasedSubscriber.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-BILLING-CHAR | services/billing/src/__tests__/ks1868-billing-chargeable-events-catches-unreadable-throw.test.ts, services/billing/src/chargeable-events.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-BILLING-CHAR | services/billing/src/__tests__/ks1868-billing-chargeable-events-lookup-update-summary-catches-unreadable-throw.test.ts, services/billing/src/chargeable-events.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-CH | services/originate/src/__tests__/ks1868-originate-charge-events-pricing-connection-fetch-catches-unreadable-throw.test.ts, services/originate/src/services/chargeEvents.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-M365-TOKEN-C | services/m365-integration/src/__tests__/ks1868-m365-token-crypto-failed-catches-unreadable-throw.test.ts, services/m365-integration/src/security/tokenCrypto.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P7_spark-dsv4flash_BRIEFED-CODEPATCH2-TOKENISATION | services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts, services/tokenisation/src/vault.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P8_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-CERTIFIC | services/nft-certificate/src/__tests__/ks1868-nft-certificate-cardano-init-catch-unreadable-throw.test.ts, services/nft-certificate/src/cardano/index.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O91-P9_spark-dsv4flash_BRIEFED-CODEPATCH2-TIMESTAMPING | services/timestamping/src/__tests__/ks1868-timestamping-create-timestamp-request-exception-catch-unreadable-throw.test.ts, services/timestamping/src/tsa/qualified-tsa.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P10_spark-dsv4flash_BRIEFED-CODEPATCH2-TRANSFER-IN | services/transfer/src/__tests__/ks1868-transfer-index-load-from-db-catch-unreadable-throw.test.ts, services/transfer/src/index.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P11_spark-dsv4flash_BRIEFED-CODEPATCH2-TIMESTAMPIN | services/timestamping/src/__tests__/ks1868-timestamping-index-ensure-table-catch-unreadable-throw.test.ts, services/timestamping/src/index.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-DO | services/originate/src/__tests__/ks1868-originate-document-repo-read-list-update-catches-unreadable-throw.test.ts, services/originate/src/repositories/documentRepo.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-REFERRAL-SER | services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts, services/referral/src/services/referralService.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-PRISM-DB-PRO | services/prism/src/__tests__/ks1868-prism-db-probe-db-catch-unreadable-throw.test.ts, services/prism/src/db.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-TIMESTAMPING | services/timestamping/src/__tests__/ks1868-timestamping-db-probe-db-catch-unreadable-throw.test.ts, services/timestamping/src/db.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-WALLET-CONNE | services/wallet-connector/src/__tests__/ks1868-wallet-connector-server-session-db-catches-unreadable-throw.test.ts, services/wallet-connector/src/server.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P7_spark-dsv4flash_BRIEFED-CODEPATCH2-STAKING-VERI | services/staking/src/__tests__/ks1868-staking-verify-db-ready-catch-unreadable-throw.test.ts, services/staking/src/routes/stake.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P8_spark-dsv4flash_BRIEFED-CODEPATCH2-TIMESTAMPING | services/timestamping/src/__tests__/ks1868-timestamping-index-db-lookup-catches-unreadable-throw.test.ts, services/timestamping/src/index.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O92-P9_spark-dsv4flash_BRIEFED-CODEPATCH2-REFERRAL-LEA | services/referral/src/__tests__/ks1868-referral-leaderboard-build-leaderboard-catch-unreadable-throw.test.ts, services/referral/src/routes/leaderboard.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O93-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-M365-SHAREPO | services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts, services/m365-integration/src/sharepoint/client.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O93-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-WE | services/originate/src/__tests__/ks1868-originate-webhooks-dispatch-event-catch-unreadable-throw.test.ts, services/originate/src/routes/webhooks.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O93-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-AN | services/originate/src/__tests__/ks1868-originate-anchor-state-sync-heal-write-catch-unreadable-throw.test.ts, services/originate/src/services/anchorStateSync.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O93-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-AUTH-USER-RE | services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts, services/auth/src/repositories/userRepo.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P10_spark-dsv4flash_BRIEFED-CODEPATCH2-ANCHORING-C | services/anchoring/src/__tests__/ks1868-anchoring-classify-thread-mint-error-unreadable-throw.test.ts, services/anchoring/src/threadMintRequest.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P12_spark-dsv4flash_BRIEFED-CODEPATCH2-ANCHORING-I | services/anchoring/src/__tests__/ks1868-anchoring-is-insufficient-input-error-unreadable-throw.test.ts, services/anchoring/src/cardano/transaction.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P14_spark-dsv4flash_BRIEFED-CODEPATCH2-ANCHORING-T | services/anchoring/src/__tests__/ks1868-anchoring-thread-mint-unavailable-unreadable-throw.test.ts, services/anchoring/src/threadMintSpend.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P15_spark-dsv4flash_BRIEFED-CODEPATCH2-AUTH-IS-INF | services/auth/src/__tests__/ks1868-auth-is-infrastructure-db-error-unreadable-throw.test.ts, services/auth/src/repositories/dbErrors.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P16_spark-dsv4flash_BRIEFED-CODEPATCH2-M365-CLASSI | services/m365-integration/src/__tests__/ks1868-m365-classify-msal-token-error-unreadable-throw.test.ts, services/m365-integration/src/auth/token-manager.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P17_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-P | services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts, services/originate/src/services/provenance.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P18_spark-dsv4flash_BRIEFED-CODEPATCH2-BILLING-SEN | services/billing/src/__tests__/ks1868-billing-send-classified-billing-error-unreadable-throw.test.ts, services/billing/src/routes/billing.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-MCP-SERVER-V | services/mcp-server/src/__tests__/ks1868-mcp-server-verify-tools-catches-unreadable-throw.test.ts, services/mcp-server/src/tools/verify.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-MCP-SERVER-R | services/mcp-server/src/__tests__/ks1868-mcp-server-register-tools-catches-unreadable-throw.test.ts, services/mcp-server/src/tools/register.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-TIMESTAMPING | services/timestamping/src/__tests__/ks1868-timestamping-tsa-submit-request-catch-unreadable-throw.test.ts, services/timestamping/src/tsa/rfc3161-client.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-RE | services/originate/src/__tests__/ks1868-originate-reanchor-in-flight-rejection-reads-unreadable-throw.test.ts, services/originate/src/services/reanchorInFlight.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-BILLING-EMAI | services/billing/src/__tests__/ks1868-billing-email-send-email-catch-unreadable-throw.test.ts, services/billing/src/utils/email.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-HE | services/originate/src/__tests__/ks1868-originate-health-ready-timed-check-catch-unreadable-throw.test.ts, services/originate/src/routes/health.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P7_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-OW | services/originate/src/__tests__/ks1868-originate-own-create-client-ask-catch-unreadable-throw.test.ts, services/originate/src/services/ownCreateClient.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P8_spark-dsv4flash_BRIEFED-CODEPATCH2-DEMO-SERVICE | services/demo-service/src/__tests__/ks1868-demo-service-auth-client-authenticate-persona-catch-unreadable-throw.test.ts, services/demo-service/src/services/authClient.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O94-P9_spark-dsv4flash_BRIEFED-CODEPATCH2-NFT-CERTIFIC | services/nft-certificate/src/__tests__/ks1868-nft-certificate-classify-mint-error-unreadable-throw.test.ts, services/nft-certificate/src/utils/mintError.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O95-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-LI | services/originate/src/__tests__/ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts, services/originate/src/repositories/lifecycleEventRepo.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O95-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-ORIGINATE-SH | services/originate/src/__tests__/ks1868-share-repo-create-share-catch-unreadable-throw.test.ts, services/originate/src/repositories/shareRepo.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O95-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-DEMO-SERVICE | services/demo-service/src/__tests__/ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts, services/demo-service/src/routes/reset.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O95-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-DEMO-SERVICE | services/demo-service/src/__tests__/ks1868-demo-service-reset-service-catches-unreadable-throw.test.ts, services/demo-service/src/services/resetService.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O95-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-AUTH-EMAIL-A | services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts, services/auth/src/services/email.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O96-P9_spark-dsv4flash_BRIEFED-CODEPATCH2-AUTH-HEALTH- | services/auth/src/__tests__/ks1868-auth-health-ready-checks-unreadable-throw.test.ts, services/auth/src/routes/health.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O97-P7_spark-dsv4flash_BRIEFED-CODEPATCH2-SHARED-CARDA | packages/shared/src/__tests__/ks1868-cardano-verify-document-anchor-catch-unreadable-throw.test.ts, packages/shared/src/cardano/transaction.ts | RAISE-READY | kind: product bytes in 1 file(s) |
| KS-1868 | Low | In Progress | kamil.kreiser | KS-1868-KS-1868-O98-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SHARED-CARDA | packages/shared/src/__tests__/ks1868-cardano-wallet-enable-wallet-catch-unreadable-throw.test.ts, packages/shared/src/cardano/wallet.ts | RAISE-READY | AUTH/SEC SURFACE (tier 1, Sonnet stops); kind: product bytes in 1 file(s) |
| KS-2005 | Low | Backlog | kamil.kreiser | KS-2005-KS-2005-O103-P3_spark-dsv4flash_BRIEFED-TESTONLYINPUT-SEED-DEM | services/originate/src/__tests__/ks1990-seed-demo-users-success-follows-the-counts.test.ts | RAISE-READY | PARTIAL-OVERLAP 3/6 lines already at tip; kind: test-only |

## FILES-TAKEN (ticket open, applies, but a file is in an open PR)
- KS-591 KS-591-KS-591-TENANT-1_spark-dsv4flash_BRIEFED-CODEPATCH-TENANT-PROVIS -> PR 2073 (Refs KS-1152: a rotate whose retire failed answers rotated f)
- KS-591 KS-591-PLATFORMTENANTSCREATESTA-1_spark-dsv4flash_BRIEFED-CODEPATCH-TE -> PR 2073 (Refs KS-1152: a rotate whose retire failed answers rotated f)
- KS-1868 KS-1868-KS-1868-O94-P11_spark-dsv4flash_BRIEFED-CODEPATCH2-ANCHORING-P -> PR 2081 (Refs KS-1171: with no Blockfrost client, the re-poll no long)
- KS-1868 KS-1868-KS-1868-O94-P13_spark-dsv4flash_BRIEFED-CODEPATCH2-ANCHORING-I -> PR 2081 (Refs KS-1171: with no Blockfrost client, the re-poll no long)
- KS-2012 KS-2012-KS-2012-O103-P2_spark-dsv4flash_BRIEFED-TESTONLYINPUT-APPROVE- -> PR 2095 (Refs KS-2012: pin the error text on the approve-forward late)
- KS-2016 KS-2016-KS-2016-O103-P1_spark-dsv4flash_BRIEFED-TESTONLYINPUT-AUDIT-EX -> PR 2096 (Refs KS-2016: pin that the caller's Authorization header goe)
- KS-2022 KS-2022-KS-2022-O102-P1_spark-dsv4flash_BRIEFED-DOCONLY-STALE-GATE-CIT -> PR 2098 (Refs KS-2022: correct four stale citations of passwordLoginG)
- KS-2022 KS-2022-KS-2022-O104-P1_spark-dsv4flash_BRIEFED-DOCONLY-SUPERSEDES-O10 -> PR 2098 (Refs KS-2022: correct four stale citations of passwordLoginG)
- KS-2022 KS-2022-KS-2022-O104-P2_spark-dsv4flash_BRIEFED-DOCONLY-SUPERSEDES-O10 -> PR 2098 (Refs KS-2022: correct four stale citations of passwordLoginG)
- KS-2053 KS-2053-KS-2053-O102-P2_spark-dsv4flash_BRIEFED-TESTONLYINPUT-STRIP-AB -> PR 2093 (Refs KS-2053: pin that the x-emitter-internal strip sits abo)
- KS-2077 KS-2077-KS-2077-O102-P3_spark-dsv4flash_BRIEFED-DOCONLY-SECUURA-ARCHIT -> PR 2097 (Refs KS-2077: the architecture reference routes /api/rewards)
- KS-2099 KS-2099-KS-2099-O103-P4_spark-dsv4flash_BRIEFED-TESTONLYINPUT-EMAIL-RE -> PR 2094 (Refs KS-2099: pin that the refusal log line carries no part )

## TICKET-CLOSED, applies forward (Wednesday quarantines)
- KS-753 KS-753-MOCKVERIFIED-1_ornith35b-q4_BRIEFED-TESTONLY-MOCK-TSA | archived (state Done)
- KS-880 KS-880-DEADCONV-1_ornith35b-q4_BRIEFED-TESTONLY-ROWTOAPIKEY- | archived (state Done)
- KS-880 KS-880-LIVETENANTDEFAULT-1_ornith35b-q4_BRIEFED-TESTONLY-LIV | archived (state Done)
- KS-888 KS-888-VALIDATE-LOGONLY_spark-dsv4flash_BRIEFED-TESTONLY-KS8 | archived (state Done)
- KS-1006 KS-1006-WRONGCODE-1_ornith35b-q4_BRIEFED-TESTONLY-MFA-DISABL | archived (state Done)
- KS-1049 KS-1049-A_ornith35b-q4_DOCPATCH-PLACED-BY-WEDNESDAY-D8-PASS_ | archived (state Done)
- KS-1062 KS-1062-N79-2_ornith35b-q4_BRIEFED-TESTONLY-SKIPSETONE-SKIPB | archived (state Done)
- KS-1062 KS-1062-N88-1_ornith35b-q4_BRIEFED-TESTONLY-ALLSKIPPEDZERO-P | archived (state Done)
- KS-1062 KS-1062-N93-1_ornith35b-q4_BRIEFED-TESTONLY-ONESKIPPED-ALLFA | archived (state Done)
- KS-1101 KS-1101-N3_ornith35b-q4_BRIEFED-TESTONLY-OPTIONAL-DEGRADED-O | archived (state Done)
- KS-1118 KS-1118-F2_ornith35b-q4_TESTONLY-JEST-PASS-7of7_2026-09-15 | archived (state Done)
- KS-1123 KS-1123-F2-R15_ornith35b-q4_BRIEFED-TESTONLY-VERIFY-EMPTY-ST | archived (state Done)
- KS-1123 KS-1123-F3b-CAST-R16_ornith35b-q4_BRIEFED-TESTONLY-STALE-CON | archived (state Done)
- KS-1123 KS-1123-F3b-R15_ornith35b-q4_BRIEFED-TESTONLY-STALE-CONFIDEN | archived (state Done)
- KS-1130 KS-1130-E7twin_ornith35b-q8_TESTONLY-PASS-7of7-DECLSPLICED_2 | archived (state Done)
- KS-1133 KS-1133-B_ornith35b-q4_TESTONLY-JEST-PASS-7of7_2026-09-15 | archived (state Done)
- KS-1137 KS-1137-F2-ESTATEIMAGE-1_ornith35b-q4_BRIEFED-TESTONLY-BASH- | archived (state Done)
- KS-1139 KS-1139-ERREXITBEHAVIOUR-1_ornith35b-q4_BRIEFED-TESTONLY-VAL | archived (state Done)
- KS-1153 KS-1153-R918A_ornith35b-q4_BRIEFED-TESTONLY-BASHSUITE-ADVISO | archived (state Done)
- KS-1198 KS-1198-SKMETA-1_ornith35b-q4_BRIEFED-TESTONLY-SK-PATH-CONNE | archived (state Done)
- KS-1199 KS-1199-R15_ornith35b-q4_BRIEFED-TESTONLY-R15-PIN-PASS-8of8_ | archived (state Done)
- KS-1199 KS-1199_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09-17 | archived (state Done)
- KS-1203 KS-1203-NESTEDTYPE-1_ornith35b-q4_BRIEFED-TESTONLY-NESTED-DO | archived (state Done)
- KS-1203 KS-1203-WSTRIM-1_ornith35b-q4_BRIEFED-TESTONLY-WHITESPACE-DO | archived (state Done)
- KS-1206 KS-1206-N72-1_ornith35b-q4_BRIEFED-TESTONLY-RATELIMIT-FALSE- | archived (state Done)
- KS-1206 KS-1206-N81-1_ornith35b-q4_BRIEFED-TESTONLY-RATELIMIT-INF-WS | archived (state Done)
- KS-1223 KS-1223-REFERRALFALLBACK-1_ornith35b-q4_BRIEFED-TESTONLY-REF | archived (state Done)
- KS-1223 KS-1223-WALLET-1_ornith35b-q4_BRIEFED-TESTONLY-WALLET-OUTSID | archived (state Done)
- KS-1229 KS-1229-UNTYPEDSRC_ornith35b-q4_TESTONLY-JEST-UNTYPED-SOURCE | archived (state Done)
- KS-1229 KS-1229-VERSIONTRIM_ornith35b-q4_TESTONLY-JEST-EXACT-NOT-TRI | archived (state Done)
- KS-1230 KS-1230-N74-1_ornith35b-q4_BRIEFED-TESTONLY-NULL-ALLOWLIST-M | archived (state Done)
- KS-1230 KS-1230-N80-1_ornith35b-q4_BRIEFED-TESTONLY-NULLPAIRMID-LAST | archived (state Done)
- KS-1230 KS-1230-N86-1_ornith35b-q4_BRIEFED-TESTONLY-FIRSTOF3NULL-ALL | archived (state Done)
- KS-1230 KS-1230-N92-1_ornith35b-q4_BRIEFED-TESTONLY-FIRSTOF2NULLMIXE | archived (state Done)
- KS-1230 KS-1230-N97-1_ornith35b-q4_BRIEFED-TESTONLY-LASTOF2NULLMIXED | archived (state Done)
- KS-1234 KS-1234-ALIASOTHERROUTES-1_ornith35b-q4_BRIEFED-TESTONLY-V1- | archived (state Done)
- KS-1236 KS-1236-SUBMITLEVEL-1_ornith35b-q4_BRIEFED-TESTONLY-SUBMIT-L | archived (state Done)
- KS-1238 KS-1238-N83-5_ornith35b-q4_BRIEFED-TESTONLY-TENANTS-403-CONN | archived (state Done)
- KS-1238 KS-1238-N83-6_ornith35b-q4_BRIEFED-TESTONLY-IVREGLIVEONLY-RE | archived (state Done)
- KS-1238 KS-1238-N90-1_ornith35b-q4_BRIEFED-TESTONLY-RAW598-FOUND-DOC | archived (state Done)
- KS-1238 KS-1238-N91-1_ornith35b-q4_BRIEFED-TESTONLY-REFRESHNOAUTH-SU | archived (state Done)
- KS-1238 KS-1238-N95-1_ornith35b-q4_BRIEFED-TESTONLY-ADMINSHADOW-1366 | archived (state Done)
- KS-1240 KS-1240-KS-1240-ks_1240_p6_tokenisation_spark-dsv4flash_BRIE | archived (state Done)
- KS-1244 KS-1244-JOINEDKEY-1_ornith35b-q4_BRIEFED-TESTONLY-JOINED-API | archived (state Done)
- KS-1258 KS-1258-N68-1_ornith35b-q4_BRIEFED-TESTONLY-REQUIRED-BLOCK-N | archived (state Done)
- KS-1258 KS-1258-N68-2_ornith35b-q4_BRIEFED-TESTONLY-OPTIONAL-ADVICE- | archived (state Done)
- KS-1258 KS-1258-N77-1_ornith35b-q4_BRIEFED-TESTONLY-EXACT576-ALLOWLI | archived (state Done)
- KS-1269 KS-1269-N71-1_ornith35b-q4_BRIEFED-TESTONLY-NULL-INDEX-REVOK | archived (state Done)
- KS-1269 KS-1269-N71-2_ornith35b-q4_BRIEFED-TESTONLY-BLOCK-TAMPER-REV | archived (state Done)
- KS-1275 KS-1275-ORDER-1_ornith35b-q4_BRIEFED-TESTONLY-DECLAREDORDER- | archived (state Done)
- KS-1275 KS-1275-ORDERTHROUGHSPEC-1_ornith35b-q4_BRIEFED-TESTONLY-LIF | archived (state Done)
- KS-1282 KS-1282-N91-2_ornith35b-q4_BRIEFED-TESTONLY-TENANTS-GET-GUAR | archived (state Done)
- KS-1282 KS-1282-N96-1a_ornith35b-q4_BRIEFED-TESTONLY-GUARDS-284-362- | archived (state Done)
- KS-1282 KS-1282-N96-1b_ornith35b-q4_BRIEFED-TESTONLY-GUARDS-767-859- | archived (state Done)
- KS-1282 KS-1282-N99-1_ornith35b-q4_BRIEFED-TESTONLY-TENANTADMIN403-S | archived (state Done)
- KS-1283 KS-1283-PROVADMIN-1_ornith35b-q4_BRIEFED-TESTONLY-PROVISIONE | archived (state Done)
- KS-1507 KS-1507-EMPTYDBURLCELLS-1_spark-dsv4flash_BRIEFED-TESTONLY-U | archived (state Done)
- KS-1621 KS-1621-CTORNAMEARM-1_spark-dsv4flash_BRIEFED-TESTONLY-VERIF | Done
- KS-1621 KS-1621-HEIGHTZEROCELL-1_spark-dsv4flash_BRIEFED-TESTONLY-AN | Done
- KS-1637 KS-1637-RETIREDVERIFYAPPCELL-1_spark-dsv4flash_BRIEFED-TESTO | Done
- KS-1642 KS-1642-H9PIN-2_spark-dsv4flash_BRIEFED-TESTONLY-IDNAMESPACE | archived (state Done)
- KS-1799 KS-1799-KS-1799-B5-MESSAGEGETTER_spark-dsv4flash_BRIEFED-TES | archived (state Done)
- KS-1801 KS-1801-KS-1801-P2-ROUTES2_spark-dsv4flash_BRIEFED-TESTONLY- | Done
- KS-1827 KS-1827-KS-1827-B6-BYIDSPREAD_spark-dsv4flash_BRIEFED-TESTON | Done

## DRIFTED (neither direction applies) and SPENT (reverse applies = already in tip): key, short name, ticket state, closed?
### DRIFTED
- KS-730 KS-730-B_ornith35b-q4_CODEPATCH-PASS-7of7_2026-09-17 | Done (CLOSED/ARCHIVED) | open-PR files: 2087
- KS-888 KS-888-KS-888-MINT_spark-dsv4flash_BRIEFED-CODEPATCH-KS888-M | Done (CLOSED/ARCHIVED) | open-PR files: 2066,2085
- KS-888 KS-888-REVOKE_spark-dsv4flash_BRIEFED-CODEPATCH-KS888-REVOKE | Done (CLOSED/ARCHIVED) | open-PR files: 2066,2085
- KS-910 KS-910-LEGCOMMENT-R15_ornith35b-q4_BASHPATCH-REANCHORED-R15- | Done (CLOSED/ARCHIVED) | open-PR files: 2074
- KS-937 KS-937-KS-937_ornith15-35b-8bit_BRIEFED-BASHPATCH-BRIEFED-BA | In Progress | open-PR files: 2074
- KS-975 KS-975-item1_ornith35b-q4_TESTONLY-TAMPER-PASS-7of7_2026-09- | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-998 KS-998-FORMATGATESTDIN-1_spark-dsv4flash_BRIEFED-BASHPATCH-F | Done (CLOSED/ARCHIVED) | open-PR files: 2074
- KS-1018 KS-1018_ornith35b-q8_PASS-7of7-REANCHORED-TDZINLINED_2026-09 | Done (CLOSED/ARCHIVED) | open-PR files: 2075
- KS-1034 KS-1034_ornith35b-q4_BASHPATCH-RETRY-PASS-7of7_2026-09-16 | Done (CLOSED/ARCHIVED) | open-PR files: 2052,2070
- KS-1035 KS-1035-D_ornith35b-q4_DOCPATCH-REANCHORED-PASS-6of6_2026-09 | In Progress | open-PR files: 887
- KS-1036 KS-1036-item3_ornith35b-q4_DOCPATCH-REBRIEF-PASS-8of8_2026-0 | In Progress | open-PR files: 887
- KS-1040 KS-1040-SWEEPRC-R16B_ornith35b-q4_BRIEFED-BASHPATCH-PREFLIGH | Done (CLOSED/ARCHIVED) | open-PR files: 2069
- KS-1040 KS-1040-part1_ornith35b-q4_BASHPATCH-RETRY-PASS-7of7_2026-09 | Done (CLOSED/ARCHIVED) | open-PR files: 2069
- KS-1081 KS-1081-CANONENV-R16B_ornith35b-q4_BRIEFED-BASHPATCH-BOOTSTR | In Progress | open-PR files: 2052
- KS-1081 KS-1081_ornith35b-q4_BASHPATCH-NEWTEST-PASS-7of7_2026-09-16 | In Progress | open-PR files: 2052
- KS-1093 KS-1093_ornith35b-q4_BASHPATCH-B3CREPAIRED-RECOUNTED-PASS-7o | Done (CLOSED/ARCHIVED) | open-PR files: 2052,2070
- KS-1097 KS-1097-A_ornith35b-q4_DOCPATCH-PASS-6of6_2026-09-15 | Done (CLOSED/ARCHIVED) | open-PR files: 887
- KS-1120 KS-1120-F1_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15 | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1120 KS-1120-F2_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15 | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1120 KS-1120-F2_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15 | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1123 KS-1123-F2_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15 | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1123 KS-1123-F3_ornith35b-q8_TESTONLY-PASS-7of7_2026-09-15 | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1125 KS-1125_ornith35b-q4_BRIEFED-TESTONLY-DIRECTCALL-PASS-7of7-O | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1130 KS-1130-E1twin_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15 | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1130 KS-1130-E3twin_ornith35b-q4_TESTONLY-PASS-7of7_2026-09-15 | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1139 KS-1139-SMOKECOUNTERS-1_spark-dsv4flash_BRIEFED-BASHPATCH-SM | Done (CLOSED/ARCHIVED) | open-PR files: 2068
- KS-1203 KS-1203-UNTYPED-1_ornith35b-q4_BRIEFED-TESTONLY-UNRESOLVABLE | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1203 KS-1203-UNTYPED-1_ornith35b-q4_BRIEFED-TESTONLY-UNTYPEDBYPAS | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1209 KS-1209_ornith35b-q4_BRIEFED-BASHPATCH-FAILCLOSED-PASS-7of7_ | In Progress | open-PR files: 2069
- KS-1219 KS-1219-KS-1219-ks_1219_p1_spark-dsv4flash_BRIEFED-CODEPATCH | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1219 KS-1219_ornith35b-q4_OAUTH-ARRAY-SCOPE-400-PASS-7of7_2026-09 | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-1234 KS-1234_ornith35b-q4_BRIEFED-CODEPATCH-V1-ALIAS-BODYPARSE-PA | Done (CLOSED/ARCHIVED) | open-PR files: 2083
- KS-1250 KS-1250-KS-1250-ks_1250_p1_spark-dsv4flash_BRIEFED-BASHPATCH | Done (CLOSED/ARCHIVED) | open-PR files: 2068
- KS-1250 KS-1250_ornith35b-q4_BRIEFED-BASHPATCH-SMOKEBASEURL-PASS-7of | Done (CLOSED/ARCHIVED) | open-PR files: 2068
- KS-1334 KS-1334-ADMINCONFIG500-A_spark-dsv4flash_BRIEFED-CODEPATCH-A | Done (CLOSED/ARCHIVED) | open-PR files: 2087
- KS-1346 KS-1346-C-ADMINCONFIG-TYPEFIELDS_spark-dsv4flash_BRIEFED-COD | In Progress | open-PR files: 2087
- KS-1359 KS-1359_spark-dsv4flash_BRIEFED-AUDIT-LOG-400-BELOW-MIN-KEEP | Done (CLOSED/ARCHIVED) | open-PR files: 2073
- KS-1407 KS-1407-CHANGEPWREVOKE-1_spark-dsv4flash_BRIEFED-CODEPATCH-C | In Progress | open-PR files: 2075
- KS-1410 KS-1410-KS-1410-P5A_spark-dsv4flash_BRIEFED-CODEPATCH2-LOOSE | In Progress | open-PR files: 2059
- KS-1410 KS-1410-KS-1410-P5B_spark-dsv4flash_BRIEFED-CODEPATCH2-LOOSE | In Progress | open-PR files: 2059
- KS-1417 KS-1417-KS-1417-ENVEXAMPLEDEADGATEWAYPORT-1_spark-dsv4flash_ | Done (CLOSED/ARCHIVED) | open-PR files: 2052
- KS-1426 KS-1426-KS-1426-LOCKFILECLEANROOMSURFACE-1_spark-dsv4flash_B | Done (CLOSED/ARCHIVED) | open-PR files: 2074
- KS-1462 KS-1462-OBJECTLOG-1_spark-dsv4flash_BRIEFED-CODEPATCH-ADMINC | In Progress | open-PR files: 2087
- KS-1547 KS-1547-PREFLIGHTDENOM-1_ornith35b-q4_BRIEFED-BASHPATCH-PREF | Done (CLOSED/ARCHIVED) | open-PR files: 2069
- KS-1558 KS-1558-TICKETEDEXCEPTIONS-1_spark-dsv4flash_BRIEFED-BASHPAT | Done (CLOSED/ARCHIVED) | open-PR files: 2052,2070
- KS-1568 KS-1568-ROTATEWAITPARSE-1_spark-dsv4flash_BRIEFED-CODEPATCH- | In Progress | open-PR files: 2066,2085
- KS-1613 KS-1613-DENOMABORT-1_spark-dsv4flash_BRIEFED-BASHPATCH-PREFL | In Progress | open-PR files: 2069
- KS-1641 KS-1641-OAUTHCAP-2_spark-dsv4flash_BRIEFED-CODEPATCH-INDEX-P | Done (CLOSED/ARCHIVED) | open-PR files: 2080
- KS-1670 KS-1670-KS-1670-ks_1670_p1_spark-dsv4flash_BRIEFED-CODEPATCH | In Progress | open-PR files: 2080
- KS-1780 KS-1780-KS-1780-ks_1780_p2_admin_spark-dsv4flash_BRIEFED-COD | Done (CLOSED/ARCHIVED) | open-PR files: 2087
- KS-1797 KS-1797-KS-1797_spark-dsv4flash_BRIEFED-CODEPATCH2-OAUTH-PAS | In Progress | open-PR files: none
- KS-1802 KS-1802-KS-1802-SEEDLOG_spark-dsv4flash_BRIEFED-CODEPATCH-BR | Done (CLOSED/ARCHIVED) | open-PR files: 2087
- KS-1818 KS-1818-KS-1818-LOGGERGUARD_spark-dsv4flash_BRIEFED-CODEPATC | Done (CLOSED/ARCHIVED) | open-PR files: 2087
- KS-1868 KS-1868-KS-1868-O44-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-GO | In Progress | open-PR files: 2076
- KS-1868 KS-1868-KS-1868-O44-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-GO | In Progress | open-PR files: 2076
- KS-1868 KS-1868-KS-1868-O44-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-GO | In Progress | open-PR files: 2076
- KS-1868 KS-1868-KS-1868-O44-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-GO | In Progress | open-PR files: 2076
- KS-1868 KS-1868-KS-1868-O49-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O49-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O53-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-MC | In Progress | open-PR files: 2059
- KS-1868 KS-1868-KS-1868-O53-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-MC | In Progress | open-PR files: 2059
- KS-1868 KS-1868-KS-1868-O53-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-MC | In Progress | open-PR files: 2059
- KS-1868 KS-1868-KS-1868-O56-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O73-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-AU | In Progress | open-PR files: none
- KS-1868 KS-1868-KS-1868-O74-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O74-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O81-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O83-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-AP | In Progress | open-PR files: 2064
- KS-1868 KS-1868-KS-1868-O96-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-SH | In Progress | open-PR files: 2079
- KS-1868 KS-1868-O43-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-GOVERNANCE | In Progress | open-PR files: 2076
### SPENT
- KS-805 KS-805-PATCHREDIRECTMIN-1_spark-dsv4flash_BRIEFED-CODEPATCH- | Done (CLOSED/ARCHIVED) | open-PR files: none
- KS-908 KS-908-KS-908-R2_spark-dsv4flash_BRIEFED-CODEPATCH-KS908-CON | Done (CLOSED/ARCHIVED) | open-PR files: 2066,2085
- KS-910 KS-910_ornith35b-q4_BASHPATCH-REANCHORED-REBRIEF-PASS-7of7_2 | Done (CLOSED/ARCHIVED) | open-PR files: 2074
- KS-1034 KS-1034-1034HOOKENV-R16B_ornith35b-q4_BRIEFED-BASHPATCH-HOOK | Done (CLOSED/ARCHIVED) | open-PR files: 2052,2070
- KS-1081 KS-1081-KS-1081-O76-P2_spark-dsv4flash_BRIEFED-BASHPATCH2-EN | In Progress | open-PR files: 2052
- KS-1093 KS-1093-1093LATESTSLOT-R16B_ornith35b-q4_BRIEFED-BASHPATCH-L | Done (CLOSED/ARCHIVED) | open-PR files: 2052,2070
- KS-1097 KS-1097-1097DEVPROCESS-R16B_ornith35b-q4_BRIEFED-DOCPATCH-DE | Done (CLOSED/ARCHIVED) | open-PR files: 887
- KS-1134 KS-1134_ornith35b-q4_BRIEFED-TESTONLY-BASHSUITE-STAGE1-JOIN- | Done (CLOSED/ARCHIVED) | open-PR files: 2074
- KS-1157 KS-1157-OAUTHMINTEDBY-1_spark-dsv4flash_BRIEFED-CODEPATCH2-O | In Progress | open-PR files: none
- KS-1239 KS-1239-RAWAUTHDEAD-R16B_ornith35b-q4_BRIEFED-CODEPATCH-KS12 | Done (CLOSED/ARCHIVED) | open-PR files: 2083
- KS-1245 KS-1245-1245DEGRADEDWARN-R16B_ornith35b-q4_BRIEFED-BASHPATCH | Done (CLOSED/ARCHIVED) | open-PR files: 2068
- KS-1261 KS-1261_ornith35b-q4_BRIEFED-BASHPATCH-PREFLIGHT-INIT-PASS-7 | Done (CLOSED/ARCHIVED) | open-PR files: 2069
- KS-1334 KS-1334-ADMINCONFIG500-B_spark-dsv4flash_BRIEFED-CODEPATCH-A | Done (CLOSED/ARCHIVED) | open-PR files: 2087
- KS-1364 KS-1364-PLATFORM-TENANTS-1_spark-dsv4flash_BRIEFED-CODEPATCH | In Progress | open-PR files: 2073
- KS-1377 KS-1377-APIKEYUSAGEATOMIC-1_spark-dsv4flash_BRIEFED-CODEPATC | In Progress | open-PR files: 2066,2085
- KS-1391 KS-1391-KS-1391_spark-dsv4flash_BRIEFED-CODEPATCH-issuer fro | In Progress | open-PR files: 639,947,948
- KS-1410 KS-1410-KS-1410-P6_spark-dsv4flash_BRIEFED-CODEPATCH2-LOOSE- | In Progress | open-PR files: 2073
- KS-1504 KS-1504-AUTHMETHODLOGFIELD-1_spark-dsv4flash_BRIEFED-CODEPAT | Done (CLOSED/ARCHIVED) | open-PR files: 2064
- KS-1506 KS-1506-AUDITEXPORTAUTH-1_spark-dsv4flash_BRIEFED-CODEPATCH- | In Progress | open-PR files: 2083
- KS-1544 KS-1544-KS-1544-O28-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-LO | In Progress | open-PR files: 2087
- KS-1560 KS-1560-KS-1560_spark-dsv4flash_BRIEFED-BASHPATCH2-private-p | In Progress | open-PR files: 2078
- KS-1591 KS-1591-KS-1591-ks_1591_p1_spark-dsv4flash_BRIEFED-CODEPATCH | Done (CLOSED/ARCHIVED) | open-PR files: 2066
- KS-1591 KS-1591-KS-1591-ks_1591_p2_security_spark-dsv4flash_BRIEFED- | Done (CLOSED/ARCHIVED) | open-PR files: 2066,2085
- KS-1622 KS-1622-AUDITLOGERRORSTATUS-1_spark-dsv4flash_BRIEFED-CODEPA | In Progress | open-PR files: 2073
- KS-1622 KS-1622-LATERWINDOW1622-1_spark-dsv4flash_BRIEFED-CODEPATCH- | In Progress | open-PR files: 2073
- KS-1653 KS-1653-STUBTRANSFERSCOPE-1_spark-dsv4flash_BRIEFED-CODEPATC | Done (CLOSED/ARCHIVED) | open-PR files: 2075
- KS-1689 KS-1689-NEEDSREAUTH-1_spark-dsv4flash_BRIEFED-CODEPATCH-INDE | Done (CLOSED/ARCHIVED) | open-PR files: 2080
- KS-1716 KS-1716-KS-1716_spark-dsv4flash_BRIEFED-BASHPATCH2-format ga | Done (CLOSED/ARCHIVED) | open-PR files: 2074
- KS-1779 KS-1779-KS-1779-ks_1779_p1_spark-dsv4flash_BRIEFED-CODEPATCH | Done (CLOSED/ARCHIVED) | open-PR files: 2087
- KS-1868 KS-1868-KS-1868-O54-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O56-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O73-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-GO | In Progress | open-PR files: 2076
- KS-1868 KS-1868-KS-1868-O74-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O74-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O81-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O82-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-BR | In Progress | open-PR files: none
- KS-1868 KS-1868-KS-1868-O83-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SE | In Progress | open-PR files: 2066,2085
- KS-1868 KS-1868-KS-1868-O87-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-BR | In Progress | open-PR files: 2081
- KS-1868 KS-1868-KS-1868-O89-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-GO | In Progress | open-PR files: 2076
- KS-1868 KS-1868-KS-1868-O96-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SH | In Progress | open-PR files: 2079
- KS-1868 KS-1868-KS-1868-O96-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-SH | In Progress | open-PR files: 2079
- KS-1868 KS-1868-KS-1868-O96-P3_spark-dsv4flash_BRIEFED-CODEPATCH2-SH | In Progress | open-PR files: 2079
- KS-1868 KS-1868-KS-1868-O96-P4_spark-dsv4flash_BRIEFED-CODEPATCH2-SH | In Progress | open-PR files: 2079
- KS-1868 KS-1868-KS-1868-O96-P5_spark-dsv4flash_BRIEFED-CODEPATCH2-SH | In Progress | open-PR files: 2079
- KS-1868 KS-1868-KS-1868-O99-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-SH | In Progress | open-PR files: 2079

## Notes added by the drafter
- KS-2005 O103-P3 sits in RAISE-READY (its test file is in no open PR) but is HELD by Wednesday's ruling until PR 2087 merges (2087 OPEN at 02:0x per the pulls API).
- The KS-1868 rows (52 in RAISE-READY, incl. O105-P1) are product-byte log-only catches across 17 directories; not queued in bulk by the T 16th brief.
- Queue B picks are in `2026-11-09_seatT16_raise.md`; flags column here carries the reason each other row was not picked.
