# G110-F1 design note (operator 80, 2026-11-02): BRIEFED-NOT-BUILDABLE, NOT QUEUED

Why not a night/briefs dir: services/api-gateway/src/routes/admin.ts is in open PR 1928 (prscan_mid.out: 1928 still open at 18:00 AEDT; develop c2c2e03afdb3 does not contain the seven guards). mk.rd reads old text from the develop tip, where the guard blocks do not exist, so a golden cannot be generated and build_input would also refuse (file in an open PR). Build this once 1928 merges.

The seven guarded reads (from held diffs O72-P3/P4/P5, the content of PR 1928) all share the shape
    let reason: string; try { reason = (err as Error).message | err.message; } catch { reason = 'unreadable thrown value'; }
Edit per site (7 one-line edits, the existing try/catch already catches the failed coercion):
    reason = String((err as Error).message);   /  reason = String(err.message);
Sites (PR 1928 line numbers, shift by the merge): org create ~:1455, org update ~:1481, org delete ~:1526 (P3, 3 hunks); integration-test catch ~:1018, PATCH user forward ~:1507 (`details: { details: reason }`), audit export ~:1620 (P4); identity seed ~:1238 (P5).
Gate 110 measured with the real winston Console formatter: a revoked-Proxy message makes log() itself throw (NO_RESPONSE at org create/update/delete and audit export); seed 500; PATCH forward NO_RESPONSE; Symbol/toString-throws/null-proto: seed 500, forward 502.
Today vs after (ordinary Error already gets the after-state at each site): org/export routes 500 with the constant body; seed warn and continue (200 on the two identity list routes); forward 502; integration test answers its normal failure body. NO persisted write at any site. After the fix a hostile non-string message gets the ordinary-Error answer with the constant reason in logs/body: forward `details.details` becomes the constant instead of NO_RESPONSE / 502-with-text.
Tier: gate 110 ruled PR 1928 TIER 2; same here (no auth decision, no write). Test file shape: PR 1928's three tests (ks1868-admin-organization-route-catches-unreadable-throw.test.ts, ks1868-admin-forward-and-export-catches-unreadable-throw.test.ts, ks1868-admin-identity-seed-catch-unreadable-throw.test.ts); add cells with a message getter returning a revoked Proxy / toString-throws / null-prototype object, with winston NOT stubbed for at least one cell (the stubbed logger hid this class, as in gate 109 F-4).
Pass split proposal: O80-G3 org create/update/delete (3 hunks), O80-G4 forward + export + integration-test (3 hunks), O80-G5 seed (1 hunk). Runner vitest, rdir Blockchain/Dev/services/api-gateway.
