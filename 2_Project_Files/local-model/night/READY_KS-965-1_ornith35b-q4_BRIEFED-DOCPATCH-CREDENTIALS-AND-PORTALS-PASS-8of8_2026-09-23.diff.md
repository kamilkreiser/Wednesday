# READY — KS-965-1 (Ornith, briefed, doc_patch, markdown) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks965-ornith35b-night/out.md.checker/patch.diff`** (from `ls` at 07:23 2026-09-23; sha256[:16] f32e4b95d1b5cf3d, 1234 B — a BYTE count; byte-equal to the out.md fence (the model's as-written block)). Checker D2 (verbatim from checker.out): `PASS D2 diff applies at the tip (strict)`; golden not located — no identity claim is made.

**Held 07:23 2026-09-23 by Wednesday 06:0x seat 2026-09-23 after a source read (hold_ready.py, doc_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks965-ornith35b-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2bc5ccf63b8c40911afb568b03cace066238ffcf` (input `doc_965.json`).
- Subject [checker.out D0, verbatim]: `PASS D0 subject: clone at 2bc5ccf63b8c40911afb568b03cace066238ffcf, USER_TESTING/CREDENTIALS-AND-PORTALS.md present`
- Output shape [checker.out D1, verbatim]: `PASS D1 output is exactly one fenced ```diff block`
- Touched-file set [checker.out D3, verbatim]: `PASS D3 touched-file set == { USER_TESTING/CREDENTIALS-AND-PORTALS.md }` — `patch.diff`'s own `+++` header names exactly `USER_TESTING/CREDENTIALS-AND-PORTALS.md`; 2 hunk(s), `+` lines 2 (ASCII), `-` lines 2 (counted from patch.diff); before.md → after.md: 2 line(s) removed, 2 added (difflib on the checker's own files).
- Tip content [out.md.checker/before.md]: byte-equal to input.json['files'][product_file]; after.md is byte-equal to patch.diff re-applied to before.md (`git apply -p1 (strict)`, scratch tempdir, sha256 64114af3ce43337a).
- Sections [checker.out D4/D5, verbatim, one pair per required section]:
  - `PASS D4 BEFORE: '## 2. Default-tenant accounts' lacks ['ADMIN_USER_PASSWORD'] at the tip (control: section found, 16 lines)`
  - `PASS D5 AFTER: '## 2. Default-tenant accounts' carries ['ADMIN_USER_PASSWORD']`
  - `PASS D4 BEFORE: '## 7. Quick smoke' lacks ['ADMIN_USER_PASSWORD'] at the tip (control: section found, 58 lines)`
  - `PASS D5 AFTER: '## 7. Quick smoke' carries ['ADMIN_USER_PASSWORD']`
- section `## 2. Default-tenant accounts` tokens ['ADMIN_USER_PASSWORD'] — before.md: found at line 61, 16 lines, every token ABSENT; after.md: found at line 61, 16 lines, every token PRESENT (re-measured with the checker's section rule)
- section `## 7. Quick smoke` tokens ['ADMIN_USER_PASSWORD'] — before.md: found at line 154, 58 lines, every token ABSENT; after.md: found at line 154, 58 lines, every token PRESENT (re-measured with the checker's section rule)
- D6 [verbatim]: `PASS D6 every changed region lies inside the required sections (2 section(s), measured on before/after)`
- D7 [verbatim]: `PASS D7 every must-remove line (2) present before and absent after (control: all found at the tip)` — re-measured: every one of the 2 must_remove line(s) in before.md and absent from after.md
- D8 [verbatim]: `PASS D8 every brief '+' line (2) is in the file AFTER, exactly` — re-measured: every one of the 2 brief '+' line(s) in after.md exactly (rstrip)
- D9 [verbatim]: `INFO D9 no insert_after anchor in the input (not an insert-only brief, or built before 00:0x)`
- RESULT [checker.out, verbatim]: `RESULT: PASS (8/8)` (total 8 = the checker's formula for must_remove=2, expected_plus=2, insert_after=None)

**PR NOTES for the raise seat:** DOC_PATCH — DOCUMENTATION ONLY, zero code bytes: `USER_TESTING/CREDENTIALS-AND-PORTALS.md` (+2/-2 per patch.diff); one file. Apply `patch.diff` strictly (`git apply -p1`) at the tip `2bc5ccf63b8c40911afb568b03cace066238ffcf` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Tier: tier 1 (documentation) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks965-ornith35b-night/input.json`. Brief (given by --title-from-brief; none located by ticket + ROWID tokens ['1']): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-965.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-23_ks965-ornith35b-night/checker.out`.

```diff
--- a/USER_TESTING/CREDENTIALS-AND-PORTALS.md
+++ b/USER_TESTING/CREDENTIALS-AND-PORTALS.md
@@ -65,7 +65,7 @@
 | Email | Password | Role | Verification | Tenant | UUID |
 |---|---|---|---|---|---|
 | `demo@secuura.io` | `demo123` | `ISSUER_ADMIN` (was `OWNER` until KS-547) | `ENHANCED` | `default` | `a0000000-0000-4000-8000-000000000010` |
-| `admin@secuura.com` | `admin123` | `SYSTEM_ADMIN` | `HIGH` | `default` | `b0000000-0000-4000-8000-000000000001` |
+| `admin@secuura.com` | `ADMIN_USER_PASSWORD` (no default - account not seeded if unset) | `SYSTEM_ADMIN` | `HIGH` | `default` | `b0000000-0000-4000-8000-000000000001` |
 | `issuer@secuura.com` | `issuer123` | `ISSUER_ADMIN` | `ENHANCED` | `default` | `a0000000-0000-4000-8000-000000000030` |
 | `verifier@secuura.com` | `verifier123` | `VERIFIER` | `STANDARD` | `default` | `a0000000-0000-4000-8000-000000000040` |
 | `holder@secuura.com` | `holder123` | `OWNER` | `BASIC` | `default` | `a0000000-0000-4000-8000-000000000050` |
@@ -175,6 +175,6 @@
 for u in \
   demo@secuura.io:demo123 \
-  admin@secuura.com:admin123 \
+  admin@secuura.com:${ADMIN_USER_PASSWORD} \
   issuer@secuura.com:issuer123 \
   verifier@secuura.com:verifier123 \
   holder@secuura.com:holder123 \
```
