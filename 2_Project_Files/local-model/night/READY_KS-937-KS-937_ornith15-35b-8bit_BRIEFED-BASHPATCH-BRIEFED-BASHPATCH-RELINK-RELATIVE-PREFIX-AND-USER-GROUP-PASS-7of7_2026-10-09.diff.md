# READY — KS-937-KS-937 (ornith15-35b-8bit, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-10-08_ks937-omlx-ornith-1.5-35b-a3b-mlx-8bit-night/out.md.checker/patch.diff`** (from `ls` at 09:22 2026-10-09; sha256[:16] 49f69f7d29a4f628, 4914 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-10-08_ks937-omlx-ornith-1.5-35b-a3b-mlx-8bit-night/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-10-08_ks937-omlx-ornith-1.5-35b-a3b-mlx-8bit-night/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; golden not located — no identity claim is made.

**Held 09:22 2026-10-09 by Wednesday (morning seat 2026-10-09) after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-10-08_ks937-omlx-ornith-1.5-35b-a3b-mlx-8bit-night/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `0a6177ea5482227e83d5045b68b8577a56326ffc` (input `bash_patch_937RELINK-R1.json`).
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 0a6177ea5482227e83d5045b68b8577a56326ffc, Blockchain/Dev/scripts/check-shared-relink.sh and Blockchain/Dev/scripts/__tests__/check_shared_relink_case.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/check-shared-relink.sh', 'Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/check-shared-relink.sh , Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh (MODIFIED in place — test_file pinned to an existing suite, 2026-09-16 KS-1163) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/check-shared-relink.sh` (script) and `Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh` (MODIFIED in place) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/check_shared_relink_case.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_1.diff` + input.json defect_line: every one of the 6 brief `+` line(s) present; script `+` lines 6 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 2; must_change sites 2/2 each a `-` line; must_remove 2 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/check-shared-relink.sh` (+6/-2 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh` (+66/-1 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh fails at the untouched tip (rc=1, 4 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=4 pass_lines=0 load_error=0 timeout=0` [red_first.out re-count: 4 FAIL line(s), 0 pass line(s); FAIL lines: ['FAIL: F-C: a ./node_modules re-link destination is the same symlink and passes (expected exit 0, got 1)', 'FAIL: F-C: an app/node_modules re-link destination under WORKDIR / is the same symlink and passes (expected exit 0, got 1)', 'FAIL: F-E: USER root:root -> re-link -> drop privileges passes (expected exit 0, got 1)', 'FAIL: F-E: USER 0:0 -> re-link -> drop privileges passes (expected exit 0, got 1)']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 0 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=0 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 0 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive check-shared-relink.sh: no NEW failure after (3 suite(s))` [3 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/check-shared-relink.sh` (+6/-2 counted from `section_1.diff` by hold_ready — the bash checker writes no numstat.out) and the MODIFIED test `Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh` (+66/-1); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `0a6177ea5482227e83d5045b68b8577a56326ffc` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-10-08_ks937-omlx-ornith-1.5-35b-a3b-mlx-8bit-night/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-10-08_ks937-omlx-ornith-1.5-35b-a3b-mlx-8bit-night/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/check-shared-relink.sh
+++ b/Blockchain/Dev/scripts/check-shared-relink.sh
@@ -415,6 +415,8 @@
         # on clause A, which blocks today, so it was live friction on any author
         # who writes `-sf`. Accept any short-flag cluster containing `s`, and any
         # destination path ENDING at node_modules/@secuura/shared.
-        if (L ~ /ln[ \t]+-[A-Za-z]*s[A-Za-z]*[ \t]+\/shared[ \t]+(\/[^ \t]*\/)?node_modules\/@secuura\/shared([ \t]|$)/) relink[stage] = ord
+        # KS-937 F-C: a RELATIVE prefix ends there too (./node_modules/..., app/node_modules/...), so the
+        # prefix group no longer requires a leading slash.
+        if (L ~ /ln[ \t]+-[A-Za-z]*s[A-Za-z]*[ \t]+\/shared[ \t]+([^ \t]*\/)?node_modules\/@secuura\/shared([ \t]|$)/) relink[stage] = ord
         return
       }
@@ -432,6 +434,8 @@
         nuser[stage]++
         user_ord[stage, nuser[stage]] = ord
         u = L
-        sub(/^USER[ \t]+/, "", u); sub(/[ \t].*$/, "", u)
+        # KS-937 F-E: USER root:root and USER 0:0 name root too. Only the user part decides, so the
+        # :group part is dropped before effective_user_is_unprivileged compares the value.
+        sub(/^USER[ \t]+/, "", u); sub(/[ \t].*$/, "", u); sub(/:.*$/, "", u)
         user_val[stage, nuser[stage]] = u
       }
--- a/Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/check_shared_relink.test.sh
@@ -218,7 +218,72 @@
 COPY --from=shared-builder /shared /shared
 RUN ln -s /shared node_modules/@secuura/other
 USER secuura' "final stage has NO"
-
+
+# KS-937 F-C. F-4 accepts any destination ENDING at node_modules/@secuura/shared, but the prefix
+# group required a LEADING slash, so a relative prefix was a false BLOCK whose message ("final stage
+# has NO re-link") is false about the file: the link is there and identical.
+expect "F-C: a ./node_modules re-link destination is the same symlink and passes" 0 'FROM node:24-alpine AS shared-builder
+RUN npm ci --ignore-scripts
+FROM node:24-alpine AS builder
+COPY --from=shared-builder /shared /shared
+RUN npm ci --ignore-scripts
+FROM node:24-alpine
+RUN npm ci --ignore-scripts --omit=dev
+COPY --from=shared-builder /shared /shared
+RUN mkdir -p node_modules/@secuura && ln -s /shared ./node_modules/@secuura/shared
+USER secuura' "1 Dockerfile"
+
+expect "F-C: an app/node_modules re-link destination under WORKDIR / is the same symlink and passes" 0 'FROM node:24-alpine AS shared-builder
+RUN npm ci --ignore-scripts
+FROM node:24-alpine AS builder
+COPY --from=shared-builder /shared /shared
+RUN npm ci --ignore-scripts
+FROM node:24-alpine
+WORKDIR /
+RUN npm ci --prefix app --ignore-scripts --omit=dev
+COPY --from=shared-builder /shared /shared
+RUN mkdir -p app/node_modules/@secuura && ln -s /shared app/node_modules/@secuura/shared
+USER secuura' "1 Dockerfile"
+
+# KS-937 F-E. USER root:root and USER 0:0 are root, so the link IS created with privileges; the
+# value was compared whole, so both read as a non-root user and false-blocked the F-2 shape.
+expect "F-E: USER root:root -> re-link -> drop privileges passes" 0 'FROM node:24-alpine AS shared-builder
+RUN npm ci --ignore-scripts
+FROM node:24-alpine AS builder
+COPY --from=shared-builder /shared /shared
+RUN npm ci --ignore-scripts
+FROM node:24-alpine
+USER root:root
+RUN npm ci --ignore-scripts --omit=dev
+COPY --from=shared-builder /shared /shared
+RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared
+USER secuura' "1 Dockerfile"
+
+expect "F-E: USER 0:0 -> re-link -> drop privileges passes" 0 'FROM node:24-alpine AS shared-builder
+RUN npm ci --ignore-scripts
+FROM node:24-alpine AS builder
+COPY --from=shared-builder /shared /shared
+RUN npm ci --ignore-scripts
+FROM node:24-alpine
+USER 0:0
+RUN npm ci --ignore-scripts --omit=dev
+COPY --from=shared-builder /shared /shared
+RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared
+USER secuura' "1 Dockerfile"
+
+# The control for F-E: only the USER part decides. A non-root user with the root GROUP is still a
+# non-root user, so a re-link after it still fails, on the privilege rule.
+expect "F-E control: USER secuura:root is not root, and a re-link after it still fails" 1 'FROM node:24-alpine AS shared-builder
+RUN npm ci --ignore-scripts
+FROM node:24-alpine AS builder
+COPY --from=shared-builder /shared /shared
+RUN npm ci --ignore-scripts
+FROM node:24-alpine
+RUN npm ci --ignore-scripts --omit=dev
+COPY --from=shared-builder /shared /shared
+USER secuura:root
+RUN mkdir -p node_modules/@secuura && ln -s /shared node_modules/@secuura/shared' "runs after a non-root"
+
 # KS-921 F-5. Docker resolves stage names case-insensitively; keying the prune on
 # the literal made `AS Builder` + `--from=builder` a false B warning today, and a
 # false BLOCK the moment STRICT becomes the default.
```

**Wednesday's golden check (09:22 2026-10-09, golden passed to hold_ready as '-'):** `out.md.checker/patch.diff` vs `night/briefs/KS-937.golden.diff`, git `diff --git`/`index` headers stripped: `cmp -s` rc 0 (98 = 98 lines). Control: the same patch vs the KS-1438 golden (66 lines) `cmp -s` rc 1. GREEN-AFTER is the suite's own summary (111 passed / 0 failed; red-first 107 passed / 4 failed); hold_ready accepted it under its 2026-10-09 summary-green clause (IMPROVEMENTS row of the same date). **Raise-seat note:** the checker's clone was develop 0a6177ea5482; develop is now 1e7f90e26137 (#1428 touched no file in this diff, not re-applied by Wednesday). This change WIDENS a push guard (`check-shared-relink.sh`): the QA gate must prove the guard still refuses what it exists to catch.
