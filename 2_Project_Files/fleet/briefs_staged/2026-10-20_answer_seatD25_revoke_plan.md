## BLUF
YES to the revoke as you drew it, with ONE narrowing: log in as `demo@secuura.io` (ISSUER_ADMIN, the published seed account) ONLY. **If that principal is refused (403), STOP and report; do NOT fall back to admin@secuura.com and do NOT read any password from the box's environment.** Escalating to SYSTEM_ADMIN with a credential read off the box is a wider act than Kam's "Revoke it", so that branch comes back to Wednesday. The side-effect rows (one `last_login_at`, the 2-3 audit rows) are accepted. Your substitute witnesses replace step 3: accepted, and the original probe is recorded as UNMEASURABLE (only the key's hash exists), not as passed.

## Exactly
1. POST /api/auth/login as demo@secuura.io (once), from inside dev_secuura-network via api-gateway.
2. DELETE /api/security/keys/key_66e82ef0-a96f-4d4d-9e0f-b6fb6d0b08c0 with that bearer (the soft revoke at security index.ts:1285 on demo's running d75bfe2deb80, per your read).
3. Witnesses, before/after: DB row is_active true -> false, last_used_at unchanged (2026-07-30), row present; security /health stats.activeApiKeys 42 -> 41; DB active count 42 -> 41.
4. Control: the same bearer's GET /api/auth/me 200 after the revoke, and key_61774985 (uat-ps) still active.
5. Nothing else on demo. Report with each figure and its instrument; then finish your wrap.

## Received, verified at source by you (not re-read by Wednesday)
Notices posted: KS-772 ec36a174 (00:56:08Z, 1 mention node), KS-485 28c0ddf2 (00:56:10Z, 1 mention node), bodies byte-equal to the drafts. Wednesday will cite these ids to Kam.
