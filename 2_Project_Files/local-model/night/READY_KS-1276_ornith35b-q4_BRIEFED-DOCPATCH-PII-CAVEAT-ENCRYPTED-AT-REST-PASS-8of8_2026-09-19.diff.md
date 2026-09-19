# READY — KS-1276 (Ornith, briefed, doc_patch) — PASS 8/8 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-19_ks1276-ornith35b-night/out.md.checker/patch.diff`** (one hunk, `Blockchain/Dev/docs/VOCABULARY.md` :165-166, applies strict).

**Held 10:42 2026-09-19 by the 10:2x Wednesday seat after a source read.** Tip `3c447abc7`. The PII caveat in § 3 Lifecycle events said the payload is "stored as **unencrypted JSONB**" beside a line saying it is "encrypted at rest" since KS-537; the fix makes the caveat open with "is **encrypted at rest** (since KS-537, 2026-07-31; …)". **Refs KS-1276, never Closes** (the standing rule; the brief rewords the ticket's literal fix, which left a sentence with no verb — the reviewer's call whether that closes it). Docs only: tier 2 / through-code at the gate.

## Source read (Wednesday)
- Model +/- lines 4/4 IDENTICAL to the brief's; crossed control (KS-1269 brief) 4/4 absent.
- Applied text read in `after.md` :165-167 — reads correctly, the GDPR/caller-contract sentence below untouched.
- **Premise re-measured by Wednesday** (the brief CARRIED it from the ticket): `git show 3c447abc7:` `services/originate/src/repositories/lifecycleEventRepo.ts:61` `encodeLifecyclePayload(payload, id)` and `utils/lifecyclePayloadCodec.ts:36` `encryptField(...)` → TRUE. Nuance, stated: an empty `{}` passes through unencrypted (codec :31; carries no PII) and legacy plaintext rows decode (repo :133) — covered by "since KS-537, 2026-07-31".

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS D0 subject: clone at 3c447abc7714e98fbba596aa1045b7bb47a6d215, Blockchain/Dev/docs/VOCABULARY.md present
PASS D1 output is exactly one fenced ```diff block
PASS D2 diff applies at the tip (strict)
PASS D3 touched-file set == { Blockchain/Dev/docs/VOCABULARY.md }
PASS D4 BEFORE: '## 3. Lifecycle events' lacks ['**encrypted at rest**', '2026-07-31;'] at the tip (control: section found, 57 lines)
PASS D5 AFTER: '## 3. Lifecycle events' carries ['**encrypted at rest**', '2026-07-31;']
PASS D6 every changed region lies inside the required sections (1 section(s), measured on before/after)
PASS D7 every must-remove line (2) present before and absent after (control: all found at the tip)
PASS D8 every brief '+' line (2) is in the file AFTER, exactly
INFO D9 no insert_after anchor in the input (not an insert-only brief, or built before 00:0x)
RESULT: PASS (8/8)
