# READY — KS-1172 PART D (docs: `Blockchain/Dev/docs/VOCABULARY.md` §2 + §3 verb lists and the §3 bullet for `note` / `verified`) — Ornith ornith:35b (Q4_K_M) PASS 6/6 under the NEW `doc_patch` type (run night7 20:11; D2 REANCHORED — the model's context lines were invented, its -/+ lines were right; the diff below is the REANCHORED one that applies)
# Source read by me (Wednesday): E1 §2 list (`protect · unprotect · restore ·` + `note · verified`), E2 §3 list likewise, E3 the five-line §3 bullet verbatim from the brief. Kam 19:55: the docs test. **Bundle with Parts A+B into the one KS-1172 PR; the yaml stays a regeneration step.**

```diff
--- a/Blockchain/Dev/docs/VOCABULARY.md
+++ b/Blockchain/Dev/docs/VOCABULARY.md
@@ -45,8 +45,9 @@
 share-revoke · share-permission-change ·
 share-recipient-change · share-expiry-change · share-token-rotate · share-resend ·
 share-attach-consent ·
-delete · rename · view · download ·
-protect · unprotect · restore
+delete · rename · view · download ·
+protect · unprotect · restore ·
+note · verified
 ```
 
 - **`declare` was `certify` until 2026-08-26 (KS-661).** Terminology only — what the verb
@@ -124,8 +124,9 @@
 
 ```
 rights-unassign · share-revoke · share-permission-change · rename · delete · restore ·
-share-recipient-change · share-expiry-change · share-token-rotate · share-resend ·
-share-attach-consent · protect · unprotect
+share-recipient-change · share-expiry-change · share-token-rotate · share-resend ·
+share-attach-consent · protect · unprotect ·
+note · verified
 ```
 
 - Verbs **with** dedicated endpoints (`share`, `transfer-custody`, `revoke`, `declare`,
@@ -151,6 +151,11 @@
   attach to the current document). Also added to the flat-path vocabulary in §2 alongside
   `restore` (already accepted here since KS-389) so S can stop omitting `documentType` on
   the fallback path for all three.
+- `note` / `verified` (**Stuart's request, accepted since KS-1172, 2026-09-15**) — `note`: a user
+  attached a short plain-text note to a document; the text stays on S and the payload carries only
+  `noteSha256` / `noteLength` (a content commitment, never the text). `verified`: the Verify FLOW's
+  completion event — every required verifier has completed; verifier identities as DID / credential
+  references only. Both non-mutating, exactly the KS-387 shape; also added to the flat-path vocabulary in §2.
 - Read side: `GET /api/documents/{id}/lifecycle-events` (tenant-scoped, newest first).
 - Events persist in `document_lifecycle_events` (migration 037).
 - **⚠ PII caveat for payload authors:** `payload` is stored as **unencrypted JSONB** and is
```
