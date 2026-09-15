# READY — KS-1172 + KS-1173 PART D (`docs/VOCABULARY.md` §2 + §3 lists and the §3 bullet for `note` / `certified` / `verified`) — Ornith ornith:35b (Q4_K_M) PASS 6/6 FIRST RUN under `doc_patch` (run night11 20:34; supersedes the two-verb READY). The diff below is the checker's applied body (REANCHORED if D2 said so — see the run's checker.out).
# Source read by me (Wednesday): both lists + the seven-line bullet verbatim from the brief. The yaml stays a regeneration step.

```diff
--- a/Blockchain/Dev/docs/VOCABULARY.md
+++ b/Blockchain/Dev/docs/VOCABULARY.md
@@ -47,6 +47,7 @@
 share-attach-consent ·
 delete · rename · view · download ·
 protect · unprotect · restore
+note · certified · verified
 ```
 
 - **`declare` was `certify` until 2026-08-26 (KS-661).** Terminology only — what the verb
@@ -126,6 +126,7 @@
 rights-unassign · share-revoke · share-permission-change · rename · delete · restore ·
 share-recipient-change · share-expiry-change · share-token-rotate · share-resend ·
 share-attach-consent · protect · unprotect
+note · certified · verified
 ```
 
 - Verbs **with** dedicated endpoints (`share`, `transfer-custody`, `revoke`, `declare`,
@@ -151,6 +151,13 @@
   attach to the current document). Also added to the flat-path vocabulary in §2 alongside
   `restore` (already accepted here since KS-389) so S can stop omitting `documentType` on
   the fallback path for all three.
+- `note` / `certified` / `verified` (**Stuart's Flow project, KS-1172 + KS-1173, 2026-09-15**) — `note`: a user
+  attached a short plain-text note to a document; the text stays on S and the payload carries only
+  `noteSha256` / `noteLength` (a content commitment, never the text). `certified`: the Certify FLOW completed
+  (every required declaration made and the organisation's signature applied — one row per flow, after its
+  `declare` and `sign` events; not the transitional `certify` alias). `verified`: the Verify FLOW completed —
+  every required verifier confirmed; verifier identities as DID / credential references only. All three
+  non-mutating, exactly the KS-387 shape; also added to the flat-path vocabulary in §2.
 - Read side: `GET /api/documents/{id}/lifecycle-events` (tenant-scoped, newest first).
 - Events persist in `document_lifecycle_events` (migration 037).
 - **⚠ PII caveat for payload authors:** `payload` is stored as **unencrypted JSONB** and is
```
