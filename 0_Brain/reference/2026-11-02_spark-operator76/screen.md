# Operator 76 screen, 2026-11-02 (develop fcfa5dfdba9b; descriptions read via Linear GraphQL, saved in desc/)
Method: triage_A/B1/B2 AGENT-BUILDABLE rows, size S and clearly mechanical M. 32 descriptions fetched (desc/KS-*.json; 9 in desc/, rest named below); code read at fcfa5df via the gate89 clone (tree.out). Open-PR scan: open_prs_start.json (21 PRs / 122 files, planted control services/auth = 7).

| candidate | file(s) | verdict |
|---|---|---|
| KS-1413 demo issuer password echoed in two startup banners | Start_Up/start-secuura.sh :711, Blockchain/Dev/scripts/start-local.sh :284 (+ NEW .test.sh guard) | **BRIEFED O76-P1** (bash_patch2; suggested text in the ticket; no open PR lists either file; test red-first by hand 2 pass/2 fail -> 4/0) |
| KS-1503 pin cell J (Minor 1) | api-gateway ks1470 test | SKIP: Minor 1 already on develop (cells RED KS-1503 M1/M2, CONTROL M3 in the file); the rest of the ticket is "decide" gaps |
| KS-1690 refresh grant origin-session check | auth routes/oauth.ts | SKIP: oauth.ts is held by O73-P4 (awaiting raise); also tier-1 design (fail-closed shape, auth-code sibling) |
| KS-1931 kyc dbGetVerificationsByUser returns [] | kyc src/index.ts | SKIP: held O71-P1/P2 (index.ts) and open PR 1921 lists it |
| KS-1574 GET /api/keys org arm | security src/index.ts | SKIP: in-flight file (Seat S 11th / O74 held) and an org-bound auth design |
| KS-1936, KS-1855 | api-gateway routes/admin.ts, verification.ts | SKIP: admin.ts has HELD O72-P3/P4/P5; ticket 1936 is "measure bound then restrict" (design), 1855 "guard by env" (design) |
| KS-1890 role on tenant-provisioning routes | tenant-provisioning src/index.ts | SKIP: in-flight file (O57/O62 held) and a role-policy design |
| KS-1696 deletion-log with no userId | originate routes/gdpr.ts | SKIP: ticket says "no remedy proposed ... ruled before it is built" (three shapes, GDPR audit surface) |
| KS-1640 chain-first blobs anchored:true | originate verification.ts, verificationV2.ts | SKIP: behaviour change; ks563 pins the shape and must be re-cut; verification on the evidence surface; O66 held file family |
| KS-1280 mount authenticateToken on cert verify | api-gateway verification.ts | SKIP: ticket's own first step is "measure originate"; KS-834 pending decision on whether the route stays public; admin/verification held family |
| KS-1821 confirmed write omits transactionHash | anchoring anchorSubmission.ts | SKIP: money/anchoring submission, "inferred, not reproduced" |
| KS-1819, KS-1820 role check + wallet lock | tokenisation / nft-certificate | SKIP: money (wallet fee drain); minting.service.ts in flight (Seat E 26th, PR 1909) |
| KS-1486 wallet first-login race | auth routes/wallet.ts | SKIP: needs real Postgres concurrency cell; auth |
| KS-1372 gateway lockout inert | api-gateway security.ts | SKIP: two options (wire or retire) in the ticket, a decision |
| KS-1107, KS-1699, KS-1831, KS-1833, KS-1376, KS-1535, KS-598 | auth register / originate certifications+documents / migrations | SKIP: each is a design or policy question (who may call, which bound; KS-1535 is Kam's deploy-blocker ruling), or needs a real database |
| KS-918 vite to devDependencies | services/auth package.json + lock | SKIP: lockfile regeneration needs npm; no unit test can prove it; "verify nothing in the build path needs it" is unmeasured |
| KS-1739 Node 26 cbor | shared wallet-signature test | SKIP: ticket says "needs a ruling" (pin Node vs upstream) |
| KS-785, KS-967, KS-951, KS-1646 | shell checkers / hooks | SKIP: each ticket lists fix shapes "not chosen" (design) |
| KS-1226/KS-1313 | systemTest unitSuiteSlotIndependence | SKIP: systemTest harness (four-gate rules), PR 1241 already hit the two-NO-GO cap on it, fix shape needs a pure-function extraction |
| KS-1712 | originate ks1557 integration test | SKIP: needs real Postgres and cause unestablished |
| KS-1051, KS-1148, KS-1080 | CI workflow / compose | SKIP: workflow edits are Kam-class; fix shape not chosen |
| KS-577, KS-1036 | docs paragraph | SKIP: doc fix without a red-first test (no doc_only fit in the checker's contract for a contract .md paragraph) |
| KS-1724, KS-1725, KS-1933/1935 (billing), anchoring submission | - | OUT per assignment |

Result: ONE brief. The screen found the list is dominated by (a) design/policy tickets, (b) held or in-flight files, (c) real-database or CI-config work.
