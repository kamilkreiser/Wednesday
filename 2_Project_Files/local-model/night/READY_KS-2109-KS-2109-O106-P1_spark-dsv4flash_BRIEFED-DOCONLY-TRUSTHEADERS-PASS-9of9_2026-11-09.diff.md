# READY - KS-2109-KS-2109-O106-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2109_o106_p1_two_stale_role_list_pointers_trustheaders_and_agent_rules/out.md.checker/patch.diff` (from `ls` at 02:23 2026-11-09; sha256[:16] 712147958eb9d77b, 2799 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 02:23 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2109_o106_p1_two_stale_role_list_pointers_trustheaders_and_agent_rules/out.md.checker`; the expectations were RE-MEASURED here.** Tip `c0e6e744b7b21f3e1aa28105766764775b50ce6d`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts', 'Blockchain/Dev/docs/security/AGENT-DOCUMENT-OPERATION-RULES.md']; `+` lines 2 (ASCII), `-` lines 2.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/docs/security/AGENT-DOCUMENT-OPERATION-RULES.md, Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts)`
  - `PASS A4 RED AT BASE: all 4 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (2 comment line(s) changed in 1 code file(s); 1 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 4 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 4/4 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `SUPER_ADMIN_ROLES` in `Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_absent `PROXY_ADMIN_ROLES` in `Blockchain/Dev/docs/security/AGENT-DOCUMENT-OPERATION-RULES.md` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `(from @secuura/shared) before doing so. The blanket strip` in `Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `and so admits` in `Blockchain/Dev/docs/security/AGENT-DOCUMENT-OPERATION-RULES.md` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts
+++ b/Blockchain/Dev/services/api-gateway/src/utils/trustHeaders.ts
@@ -34,7 +34,7 @@
  * EXCEPTION: `x-tenant-override` is intentional super-admin functionality (the
  * admin portal's tenant selector). It is a *request* — auth middleware decides
  * whether to honour it based on the verified JWT's role, gating on
- * SUPER_ADMIN_ROLES before doing so. The blanket strip added 2026-04-25
+ * `isPlatformRole` (from @secuura/shared) before doing so. The blanket strip added 2026-04-25
  * (c796138f0) was matching it too, which broke the override path silently for
  * two weeks and made KS-4 untestable.
  */
--- a/Blockchain/Dev/docs/security/AGENT-DOCUMENT-OPERATION-RULES.md
+++ b/Blockchain/Dev/docs/security/AGENT-DOCUMENT-OPERATION-RULES.md
@@ -52,7 +52,7 @@
   - **Webhooks.** `/api/webhooks` is open to a key holding `webhooks:manage` (the gateway's `requireScope`).
   - **Signing.** `POST /api/documents/{id}/sign/request` and `POST /api/documents/{id}/sign` check no scope or role in originate (see the matrix, *Request / submit a signature*).
 
-  `/api/admin/` is role-gated against connectors at the gateway (`enforceAdminProxy` with `PROXY_ADMIN_ROLES` in `services/api-gateway/src/routes/proxy.ts`, which lists human roles only). Other mounts carry gates of their own (for example `requireOrgProvisioner` on register-connector in `services/api-gateway/src/routes/platform.ts`); this page does not census them.
+  `/api/admin/` is role-gated against connectors at the gateway (`enforceAdminProxy` in `services/api-gateway/src/routes/proxy.ts`, which asks `isPlatformOrOrgAdminRole` and so admits `SYSTEM_ADMIN`, `SUPER_ADMIN` and `ORG_ADMIN` only: human roles). Other mounts carry gates of their own (for example `requireOrgProvisioner` on register-connector in `services/api-gateway/src/routes/platform.ts`); this page does not census them.
 
   **A route family that looks like a door and is not: `/api/issuer-certs`** (upload a certificate and its private key, sign, revoke, rotate). Every route there uses auth's plain `authenticate()` (`services/auth/src/routes/issuerCerts.ts`), which accepts an access token only and refuses a connector token (`type: 'connector'`) by design (`services/auth/src/middleware/authenticate.ts`; `verifyAccessToken` in `services/auth/src/services/jwt.ts`). So an `sk_` key holding an `issuer-certs:*` scope is refused there. An interactive or OAuth access token reaches it on an admin role, or on an `issuer-certs:*` scope if it carries one; no path that gives an access token such a scope was found (the role-default scope set is `documents:write` for `OWNER` only, and the OAuth registrable set has no `issuer-certs` entry). Read from code, not probed on a running stack.
```
