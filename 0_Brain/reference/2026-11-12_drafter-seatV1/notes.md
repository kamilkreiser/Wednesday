# Drafter notes, Seat V 1st brief (2026-11-12)

## Established
- No ORG_ADMIN/ISSUER_ADMIN QA login key names in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/. Present: KINTSUGI_QA_GATE_OWNER_EMAIL/PASSWORD (OWNER, no organisation, KS-1100), KINTSUGI_KAM_ADMIN_EMAIL/PASSWORD (Kam's), rotated platform-admin and Stuart super_admin files, .kintsugi_dev_credentials (DEMO_* role passwords, no email names). So item 0 = STOP, per the commission.
- Expected NOT RUN even with a login: KS-1466 (create writes a document, anchor path, 400 branch needs a catalogue change), KS-1233 (needs a platform-settings write and Redis box access). Likely NOT RUN: KS-2095 (needs existing proof with no block height), KS-2055 (needs a test transfer without an anchor). Plausibly runnable: KS-1875 (pure read), KS-1928 (if MCP reachable with the login).

## Fault to disclose
My key-name sed over `platform-s-provisioning-keys.md` printed a raw `sk_` provisioning key from a code block to my tool output (that file is markdown, not KEY=value). Nothing was copied into any file; the file is demo-targeted (uat-ps to demo). Wednesday may want it noted for rotation hygiene (the file itself says revoke if astray).

## Not established
- Whether the QA_GATE_OWNER login still works and whether OWNER may be used (not the ruled role).
- The text of card secuura-kintsugi-admin-qa-login-for-live-checks (not re-read); whether it names another file location.
- Route names, auth needs, MCP transport, test data on Kintsugi; routing-table row for Sonnet; history.md ordinal for Seat V.
- The two long briefs were read whole (D61 via 2 pages, S73 via 2 pages).

## Open questions (priority order)
1. Is the OWNER QA-gate login (KS-1100) acceptable for the live checks, or does Wednesday card Kam for the ruled ORG_ADMIN/ISSUER_ADMIN login?
2. May the seat create a test-owned transfer on Kintsugi for KS-2055 (and does that path anchor)? If yes it needs a brief-level ruling.
3. For KS-1466 and KS-1233, close under the old "no live check possible" rule (in running build) since the live check cannot run without a non-test write?
