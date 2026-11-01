# QA DELTA GATE 82d, tier 2: Secuura/Distributed_Secuura PR 1897 (KS-1901 + KS-1893), delta 4c56d252 over gated head 07a4cc5b

## BLUF
**GO for merge of the delta head 4c56d2524e3d.** G82-F1 is fixed in both product files, pinned by 3 new cells that are red by assertion at the gated head and green at the delta, and the two mutants that survived in gate 82 (M3, M18) are now killed, as are 4 further string-leak variants. Every number the author claimed re-measured. One LOW note (a test gap beyond the claim, G82d-F1) and one INFO; neither blocks.

## Heads
- START (logs/head_start.log, 2026-11-01T13:43Z): PR head `4c56d2524e3db1041527fde3af415e1c608851e0`, develop `ca36945e974081be6abbc15e548f4f8d02767e14`. Both as expected.
- Parentage (logs/fetch.log): `git rev-list --parents` gives ONE parent, `07a4cc5be5e6c8637fdd553cfe67b4b5f9df2bee` = gated head.
- END (logs/head_end.log, 13:48Z): PR head and develop unchanged; worktree HEAD `4c56d252`.

## 1. Blob table (logs/namestatus.log)
`git diff --name-status 07a4cc5be5e6 4c56d2524e3d` = exactly 6 paths, all M: `http-server.ts`, `tools/hash.ts`, `ks1893-hash-tool-...test.ts`, `ks1901-mcp-http-batch-...test.ts`, the flow fragment and the cheat fragment (+37/-15). The three pre-existing test files (ks1410 part A, part B, ks1868) are not in the delta, so they are byte-equal to the gated head. Both `ks1893-*`/`ks1901-*` files were already ADDED vs develop (second list in the same log); the delta only adds cells to them. **Confirmed.**

## 2. Product diff and probes (logs/product_diff.log, logs/probe_delta_print.log, logs/probe_delta_hash_print.log, logs/gated_probe.log)
- http-server.ts: one line deleted, `if (typeof err === 'string') return err;`, plus comment text. hash.ts: one line deleted, `else if (typeof err === 'string') logged = err;`, plus comment text. Nothing else in the product files changes.
- A thrown string now falls through to the shared fallback `non-Error ${err === null ? 'null' : typeof err} thrown` (and the same text in hash.ts). That fallback interpolates only `typeof` (or the literal `null`), never the value, so it is value-free for number, boolean, bigint, symbol, null, undefined, and string (the string's own text can only reach the log through the Error and object branches, which are unchanged: Error logs `.message` by design, object logs key NAMES).
- Probe (my scripts/gate82d-probe-*.test.ts + scripts/hostile.ts, 15 thrown values: string, number 31337, Symbol('S3CR3T-VALUE'), BigInt, boolean, null, undefined, '', NaN, String object, array, object with secret value, function, revoked Proxy, plain Error). For every non-Error value I assert the marker `S3CR3T-VALUE` is in no log line, none of the console.error arguments is a raw non-string, the wire/body has no marker, status 200 on batch routes.
  - Delta head: 45/45 pass (logs/probe_delta.log). Printed lines (--disable-console-intercept): string -> `non-Error string thrown`, number -> `non-Error number thrown`, Symbol -> `non-Error symbol thrown`, BigInt -> `non-Error bigint thrown`, null/undefined likewise, on both batch routes and the hash tool; bodies are the constant `An unexpected error occurred`, hash wire `{"success":false,"error":"An unexpected error occurred"}`.
  - Control, gated head 07a4cc5b with the same probe: 3 failed | 42 passed, the 3 failing are exactly "thrown string S3CR3T-VALUE" on register-batch, verify-batch and the hash tool (logs/gated_probe.log). The probe can see the defect and sees it gone.

## 3. Survivors M3 / M18 and the new cells (logs/gated_newcells.log, logs/delta_newcells.log, logs/mut_M*d_*.log, logs/mutants_summary.log)
- New cells at the GATED head product (delta's two test files overlaid on a 07a4cc5b worktree): the two files show 39 cells, **3 failed | 36 passed**, all `AssertionError: expected '[mcp-...] ...' not to contain 'S3CR3T-STRING-MARKER'`: B6 (hash), A4c register-batch, A4c verify-batch. Red by assertion, exactly the 3 new cells. At the delta head: 39/39.
- Mutants on the delta head (5 PR test files, 56 cells, scripts/mutants.py; each source file restored, sha256 equal, git status clean):
  - M3d (string branch re-inserted in describeThrown) KILLED, 2 failed = A4c x2, 2 AssertionError.
  - M18d (string branch re-inserted in hash.ts) KILLED, 1 failed = B6.
  - M19d / M20d (string appended in the kind branch, http / hash) KILLED (A4c x2 / B6). M21d / M22d (`${String(err)}` for all primitives, http / hash) KILLED (A4c x2 / B6).
  - All rc=1 with AssertionError counts matching the failing cells; no compile error. (The "ERROR-NOT-ASSERTION" label in logs/mutants.log is my script's regex reading the "Failed Tests" banner as the Tests line; the per-mutant logs show `Tests  N failed | ...` and rc=1.)
  - The author's M19/M20 are not re-run by name; M19d/M20d and M21d/M22d are my equivalents of "string value back in the log in each file".

## 4. Suite, tsc, eslint, docs
- Whole mcp-server suite, delta head (scripts/vt.sh, vitest 4.1.12, Node v26.8.1): **Test Files 11 passed (11), Tests 86 passed (86)**, rc 0 (logs/delta_whole.log). Gate 82 had 11 files / 83. Matches the claim.
- tsc over src including tests (scripts' tsconfig.gate82.json, tsc 5.9.3): rc 0 (logs/tsc_delta_tests.log). Planted `const x: number = "s"` in `__tests__`: `error TS2322`, rc 2 (logs/tsc_delta_planted.log); plant moved out afterwards.
- eslint (Node API, cwd = Dev) on the 4 changed code/test files: `files=4 errors=0 warnings=0`, rc 0 (logs/eslint_delta.log). Planted `var`/`debugger` file: 2 errors, rc 1 (logs/eslint_delta_planted.log).
- docs-fragments check (`Blockchain/Dev/scripts/docs-fragments.mjs check`): `flow 117 legacy + 49 new, cheat 112 legacy + 49 new; lint clean, render passes html_docs_check`, OK rc 0, with the same 2 ADVISORY lines gate 82 saw (committed page lags render, by design) (logs/frag_check_delta.log). Planted unclosed `<div>` in the flow fragment: `tags are not balanced`, FAIL, rc 1 (logs/frag_check_planted.log); restored, sha256 before/after identical (logs/frag_sha_before.log, frag_sha_after.log).
- Fragment text diff (logs/frag_diff.log) is numbers and one phrase only: 36->39 cells, 28->31 red, 20/26->22/28, 8/10->9/11, 83->86, 18->20 mutants, "a thrown string" added to the value-free sentence. All agree with what I measured (31 = 28 + 3; 8 controls unchanged).

## 5. merge-tree (logs/merge_tree.log)
`git merge-tree --write-tree refs/gate/develop-d2 refs/gate/pr1897-delta` (develop `ca36945e`, delta `4c56d252`): rc 0, tree `2e1966dd43fe108e7a97f9b332ddc237518f557f`. **Clean** over the three unrelated squashes.

## FINDINGS
- **G82d-F1 (LOW, test gap, not the author's claim, no action required to merge).** The new cells pin the thrown STRING only. I added mutants that put a thrown NUMBER's value (M23d http, M24d hash) or a thrown Symbol's description (M25d http, M26d hash) into the log: all four SURVIVE (56/56 pass, logs/mutants_extra.log, logs/mut_M23d_* .. mut_M26d_*). The code is correct today (probe above: only `typeof` is logged); the guard against a future value-logging edit for non-string primitives is just not asserted. One loop over `[42, Symbol('x'), 10n, false]` with the same log assertions would close it. Same class as G82-F1, lower exposure (a number or symbol rarely carries a secret).
- **G82d-F2 (INFO).** Gate 82's out-of-scope items G82-F2 (POST /hash echo), F3 (register/verify/info tool echoes) and F4 (unguarded route-level reads) are untouched by the delta, as expected; they stay ticket-worthy follow-ups and are not part of this verdict.
- G82-F1: **CLOSED** (checks 2 and 3).

## NOT TESTED
A booted server or MCP client (handlers in process, as in gate 82 and by the author). Node LTS (host is v26). The author's own mutant list by name.

## Housekeeping
Worktrees `wt_delta` (4c56d252) and `wt_gated` (07a4cc5b + overlaid test files, probe files) live in this folder, node_modules symlinked from gate 82's wt_head (read-only use). Probe/plant files moved to `quarantine/`. No push, comment, ticket write or mail. Nothing written under /Volumes/DevMASTER/!CODING/.
