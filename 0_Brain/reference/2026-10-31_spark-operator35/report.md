# Spark operator 35, 2026-10-31 (Secuura only). Filed by the operator.
Two small KS-1868-class tasks, both PASS 7/7 on the ORIGINAL brief (no rebrief used, counter untouched), both byte-identical to the golden, both HELD. Nothing raised, pushed, merged, no board touch, no git write verbs in !CODING.

## Method
- Read the O34 report, kit 02 and 03, spark README; tunnel.sh check: UP (127.0.0.1:47788, 200).
- Tip: `git ls-remote origin develop` = cb2320368ae42fa793d81776fdd7fc8404ce312d; fetched into the harness cache clone (toplevel asserted = spark/cache/src) and read with git show/grep at that sha.
- Site check at the tip: `instanceof Error` in vc-issuer non-test src = exactly two sites, credentialRepo.ts:432 and presentations.ts:182 (the pickup's line numbers were right).
- Briefs (kit 03 shape, rung 3 code_patch2, as O34): one hunk each with dictated header, a 6-line inline inner try (fallback 'unreadable thrown value'), NEW vitest file given whole (3 cells: control C1, red R1 revoked Proxy, red R2 Error with throwing message getter), shape from ks1295-store-db-unavailable-warn.test.ts. Generator: gen/mk.py. Briefs: night/briefs/ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw/ and ..._p2_presentations_loadpresentationsfromdb_unreadable_throw/ (KS-1868.md, golden.diff, spark.pins).
- Order per task: round.sh --dry-run (rc 0) -> --control (golden through the checker) -> real round, thinking OFF, one request at a time.
- Correction to the commission: it said O34 used a "safeReason helper"; O34 used an INLINE inner try, no helper (its report and brief say so; `safeReason` has zero hits in Blockchain/Dev at the tip). I followed O34's actual pattern.

## Partition evidence
- Open PRs: 43 read via the GitHub REST API (pulls?state=open then pulls/N/files, GH_TOKEN from the Secuura .env by name), 317 file entries; script prscan.py, output open_prs.json in this folder. vc-issuer paths in them: package.json x2 and package-lock.json x1 only. NEITHER target file is touched. Positive control: services/auth appears in 20 lines of the output.
- Security seat brief (2026-10-31_seatS9_ks1881_1871_1860_1861_security.md): names no vc-issuer path (grep for vc-issuer, presentations.ts, credentialRepo, safeReason: 0 hits; control: 'services/' 27 hits, files listed include transfer, api-gateway, originate, tenant-provisioning, tokenisation db.ts). Neither target skipped; both open.
- Not checked: other live seats' unpushed local work beyond PRs and that brief.

## Task P1: credentialRepo.loadFromDb (credentialRepo.ts:432)
- Control: PASS first time (232 s, golden byte-identical). Real round: PASS 7/7, 186 s round, 127.9 s model (slow, first call after idle), 14883+995 tokens. Verdict classes: none failed.
- Diff read at source (out.md.checker/patch.diff): product hunk @@ -430,5 +430,11, +7/-1 as briefed, WARN message text and em dash unchanged, `error: reason`; new test 61 lines. cmp patch.diff vs golden.diff = identical. Reds R1 and R2 fail by AssertionError (expected [] to have a length of 1), not by throw; C1 green before and after; suite 413 -> 416, 0 new reds, tsc rc 0 baseline and after.
- Note: ensureTable() at :46-48 has its own unguarded err?.message in a catch. NOT touched (outside the brief); the cell stand-in resolves its query. A further KS-1868 site, same class.
- Held: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-KS-1868-O35-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-CREDENTIALREPO-PASS-7of7_2026-10-31.diff.md
- Run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p1_credentialrepo_loadfromdb_unreadable_throw

## Task P2: loadPresentationsFromDb (presentations.ts:182)
- Control: PASS first time (60 s). Real round: PASS 7/7, 89 s round, 28.5 s model, 14523+961 tokens.
- Diff read at source: hunk @@ -180,5 +180,11, +7/-1, identical shape to P1, cmp vs golden identical; reds by assertion, C1 green; suite 413 -> 416, 0 new reds, tsc rc 0.
- Held: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1868-KS-1868-O35-P2_spark-dsv4flash_BRIEFED-CODEPATCH2-PRESENTATIONS-PASS-7of7_2026-10-31.diff.md
- Run dir: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-31_ks_1868_o35_p2_presentations_loadpresentationsfromdb_unreadable_throw

## Caveat on the HELD stamp
hold_ready.py stamps "by Wednesday" in the READY text; those were the operator's reads (the diffs, cmp and checker artefacts above), as with O34. Wednesday should re-read before relying on it. Both READYs close 2 of the 253 sites; refs KS-1868, does not close it. Done.md rows appended for both rounds.

## FAILs and classification
None in the model rounds. No control failures (O34 had 4; the O34 lessons - plain-function mocks for hostile throws, asserting by assertion not throw, cell title format, ## Red cells entries - were applied up front).

## UNMEASURED
- eslint on the new files; a real boot of vc-issuer calling these loaders; the other 251 sites; tsc beyond the checker's A7; whether the cold-import budget matters for the presentations test in a full-suite CI run (it passed in the checker's whole-suite run); live-lane overlap beyond open PRs and the S9 brief; the golden is operator-authored (proved by --control, not independent).
- Spark idle since: the 127.9 s first call suggests a cold start; not investigated.
