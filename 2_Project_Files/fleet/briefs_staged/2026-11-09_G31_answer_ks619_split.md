Seat G 31st

ANSWER: Kam ruled card secuura-ks619-platform-admin-login-no-marker-1109 = a at 17:20:38 (live board, verbatim): "Decision secuura-ks619-platform-admin-login-no-marker-1109: a — Split". Option a reads: "PR 2128 keeps only the user-id and role guard (no lockout). KS-619 becomes its own ticket: the platform-admin login stamps one claim and the gateway excepts it."
FIX ROUND 1 of 2 on PR 2128, after KS-1473's push is queued (KS-1473 continues):
1. Remove the KS-619 half: the tenant refusal (the !tenantId unless isPlatformRole branch) and its cells. Keep the KS-1208 half exactly: userId and role non-empty strings, every copied header through validateHeaderValue, the same 401 body, the log line. Keep the optional-mount behaviour for KS-1208 (a token missing userId or role gets 401), stated as before.
2. The E2 fixture edit in auth.test.ts ('assigns defaultTenantId when JWT has no tenantId' signed SUPER_ADMIN) existed only for the KS-619 half: restore it to develop's form if nothing else needs it, and show develop's auth.test.ts passes against the new head (or name exactly which cell still needs a change and why).
3. Red first for the new head: the KS-1208 cells still red on develop, green at the head; a tenantless platform-admin-login token (role platform_admin, no tenant) is SERVED at the head (the cell that proves no lockout); mutants as before for the KS-1208 half.
4. PR title and body: 'Refs KS-1208' only (drop KS-619 from the title/body keys; Kam's split leaves KS-619 for its own ticket); say plainly the KS-619 half was removed by Kam's ruling and why (the gate 285 finding, in plain words). KS-619 comment 03d2903b: one in-place line that the tenant refusal is NOT in PR 2128 any more and moves to its own ticket. Detach PR 2128 from KS-619 only if the integration attached it (read the attachments; say what you did). Fragments rewritten to KS-1208 only. No at-sign anywhere.
5. One push, a NEW commit (no force, no rebase), then READY FOR GATE round 2 of 2 (tier 1, compare on the delta).
The marker ticket (the platform-admin login stamps a claim; the gateway excepts it) is filed by the board seat, not you. My 16:39 and 16:4x answers on G285-1 are SUPERSEDED by this one.

Wednesday
