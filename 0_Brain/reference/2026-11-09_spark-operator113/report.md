# Spark operator 113 — report (written by Wednesday from the operator's final message; its own Write was refused)

## BLUF
9 tickets read at source, 4 briefs (one spent), 3 PASS, all byte-identical to a golden proven by a control run first; develop 4e529633d0a1 on every ls-remote 10:11-10:23. Wednesday read all three diffs whole and HELD them 10:2x (hold_ready, strict apply at 4e529633d0a1, golden BYTE-IDENTICAL):
- KS-1902 round 2 of 2 (round 1 failed B2: the model doubled backslashes) -> night/READY_KS-1902-KS-1902-O113-P1_spark-dsv4flash_BRIEFED-BASHPATCH-AKTOFLAGVALUETOKEN-PASS-7of7_2026-11-09.diff.md. Not covered: GNU grep; over-flags `docker exec -it other-container akto-x` (no cell pins it).
- KS-1794 item 3 -> night/READY_KS-1794-KS-1794-O113-P1_..._SMOKETARGETSTRIPSCREDENTIALS-PASS-7of7_2026-11-09.diff.md. Stub curl against a .invalid host; nothing reached a real host. Not covered: BSD sed only; smoke-test.sh lines 46/55 still print $GATEWAY verbatim on skip warnings (follow-up).
- KS-1718 comment variant (doc_only) -> night/READY_KS-1718-KS-1718-O113-P1_..._REDACTSECRETSCOMMENTCOSMETIC-PASS-9of9_2026-11-09.diff.md. systemTest is Peter's harness: told by ticket comment, not asked.

## Not briefable / for a Claude seat
- KS-918: no tier carries package.json + lock; deterministic regen on npm 11.19.0; diffs in ks918_lock_regen/ (package.json.diff, package-lock.json.diff; production entries 244 -> 177). Dependabot PRs 948, 649, 575 touch the same package.json.
- KS-1794 item 2 (RUNBOOK): checker's diff extraction stops at a ``` fence; golden at night/briefs/ks_1794_o113_p2_runbook_smoke_quick/golden.diff.
- KS-1218, KS-1982: owner's call (either/or; no tier proves a Dockerfile). KS-2040: taken (secuura-api.yaml in PRs 2099, 2073). KS-1932, KS-678: design. KS-2116, KS-2115: blocked on PR 2073.

## Process notes (harness)
- Hunks with backslash-quote pairs are not copied reliably: insert a backslash-free line between backslash-free context lines (-U1).
- bash_patch: ref= must differ from test_file=; product hunk under "The exact change", suite hunk under "The test".

## Disk / UNMEASURED
DevMASTER 108 GiB before and after; boot volume 257 -> 254 GiB (work clones /private/tmp/spark_work_o113). UNMEASURED: GNU/Linux grep/sed; whether CI runs these .test.sh suites; CI npm lock placement for KS-918.
