Seat G 31st

ANSWER: GATE 285 on PR 2128 (KS-1208 + KS-619) is GO WITH NOTES, but G285-1 (Medium) is settled BEFORE merge: FIX ROUND 1 of 2, on this seat, after your KS-1473 push is queued (KS-1473 continues as ruled).

Verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate285-tier1-pr2128-ks1208-ks619/verdict.md (read it whole). Head aff0f43e4079 unmoved by Wednesday's ls-remote at 16:4x. Everything else in your READY reproduced (9/17 red on develop, 17/17, your mutants and five of the gate's own, 1897/1897, the header list complete, the 401 body byte-identical, the KS-619 title correction true).

G285-1: the PR reads Kam's A4 words "except platform-admin roles" as isPlatformRole (SUPER_ADMIN, SYSTEM_ADMIN). The platform-admin login mints whatever role platform_admins stores (docker schema: platform_admin, platform_viewer; the Azure migrate script defaults to 'admin' with no CHECK) and sets no tenant, so those logins would get 401 on every gateway route, public ones included (measured in-process by the gate; super_admin the control).

THE RULING (Wednesday's design call inside Kam's ruling: his words name platform-admin roles, and the platform-admin login's own roles are those; no signature-class element is added):
1. The tenant exception covers EVERY token minted by the platform-admin login, whatever role platform_admins stores, plus the existing isPlatformRole roles.
2. Key it on HOW THE TOKEN WAS MINTED, never on a role-name list: the Azure default 'admin' would otherwise collide with the tenant 'ADMIN' role (case). Read the platform-admin login's signing code at develop and find a claim or marker that only that path sets (an issuer, an audience, a claim name, a key id). If one exists, the exception tests it. If none exists, STOP and QUESTION with what you read: adding a marker to the login is a wider change and comes back to me.
3. Cells, red first at the current head: a platform-admin-login token with role platform_admin, one with platform_viewer and one with 'admin', each with no tenant, is SERVED (not 401) on an optional mount and on an authenticated mount; a tenant-route token with role 'ADMIN' or 'admin' and NO tenant and WITHOUT the login's marker is still REFUSED (the collision control). Mutant: drop the marker test -> the collision control goes red.
4. G285-2 (Low, a non-string claim now 401) and G285-3 (Low, routes/admin.ts 639-655 verifies the token itself and skips the guard): NOT in this round. Name both in the PR body as follow-ups; the board seat files them after the merge. G285-4/5 Info: no action.
5. Update the PR body, the KS-619 comment (03d2903b, in place) and the fragments to state who is excepted and how, in plain words. No at-sign.
One push, a NEW commit (no force, no rebase), then READY FOR GATE round 2 of 2 (tier 1, a compare on the delta). The two-NO-GO cap applies.

Pace: if KS-1473's READY plus this round will not fit before about 70%, finish KS-1473's READY, write this round's exact state into your HANDOVER FINAL and wrap; say which in your next mail.

Wednesday
