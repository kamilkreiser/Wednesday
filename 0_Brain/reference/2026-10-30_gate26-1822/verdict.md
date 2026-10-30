## QA GATE - TIER 2, round 1: GO WITH NOTES

**PR:** Secuura/Distributed_Secuura #1822, KS-1666 note d (Seat T 7th)
**Head:** `df52adcddf22f13b9a95cf8c39f237e7f666bef5`. ls-remote of refs/pull/1822/head matched the claim at the start and at the end.
**Develop:** `a786e06e6f6ec66245a0d0d6d36959e247f7c989`, same at both reads; it is also the merge-base (develop has not moved since the PR was cut).
**Gate:** QA gate 26. Findings only. Nothing fixed, commented, pushed, merged or deployed.

### Counts
- **Diff:** 4 files, +65/-2, exactly the 4 declared: certifications.ts 4/2, the new ks1666 test 34/0, flow doc 11/0, cheat sheet 16/0.
- **Canonical patch:** the 40 changed lines (+/-, sorted, `index` lines excluded) of the head diff for the product and test files equal the canonical `patch.diff`'s 40, line for line. The two files come in the opposite order in the patch; the content is the same.
- **certifications.ts is comment-only. Proof:** TypeScript AST printed with `removeComments: true` (`ast.js`), base vs head: EQUAL (54425 = 54425 chars). **Controls:** `signal: AbortSignal.timeout(10000),` -> 10001 (diff shows only line 618 changed, the code line, not the comment): UNEQUAL. `res.status(503)` -> 504: UNEQUAL. Every changed line in `-U0` is a `//` line (6 lines, 0 others).
- **Red-first, spark_gate:** BASE product code 3 pass / 2 fail; HEAD 5 / 0; diff stat 4 files +65/-2.
- **Red-first, my own swap** (jest 29, my clone): head 5/5. With the base's certifications.ts (old comments) restored: R1 and R2 red, C1 to C3 green (2 failed / 3 passed). Head file restored; sha256 `55c1cb29...` equal before and after.
- **Originate jest suite:** head 152 files, 1854 cells, 1854 pass, 0 fail, 0 pending. Develop a786e06e: 151 files, 1849 cells, 1849 pass, 0 fail. Delta +1 file, +5 cells, all pass, 0 reds on either side (so nothing to show as pre-existing). Matches the author's 152 / 1854. `packages/shared` was built in my clone first (tsc rc 0; `isUsableEmitterSecret` present in dist), so none of gates 24/25's stale-shared reds appeared.
- **Docs:** html_docs_check rc 0 on both docs at head. **Control:** a planted long prose paragraph before `</body>` in scratch copies: rc 1 on both ("prose outside a table in <p>"). Flow doc: develop's highest section is 120; head adds 121 (121.1 to 121.4). The 6 line numbers the doc cites at the base (520, 527, 577, 598 to 616, 673) were each checked in develop's file: all correct.
- **Predicted merge** of the head onto develop a786e06e6f6e in my clone (`merge-tree --write-tree`): CLEAN, rc 0, tree `185a36a2...`. No conflicting files (develop is the merge-base, so this is a fast-forward in effect).

### The two comments against the code (head)
**(a) TRUE.** "Writing the row first NARROWS that window, it does not remove it: when the reservation itself fails, the anchor-then-fail path is unchanged." In the code the reservation (`reserveCertificationRow`) is in a try/catch that only logs and sets `provisionalWritten=false`; the anchoring `fetch` then runs regardless, and the authoritative `saveCertification` follows. A failed reservation followed by a failed save is exactly the old anchor-then-fail path (an anchor with no document). The code's own comment ("an orphan anchor can still be created ... exactly as before") says the same, and control C2 pins it.
**(b) TRUE, with a precision note.** The call is `signal: AbortSignal.timeout(10000)` at line 618 (head), on the only `fetch` between the provisional write and the authoritative save. Nothing else is awaited between the reservation and the fetch. The signal also covers the response-body read (`upstream.json()` / `upstream.text()`), so the window from the reservation to the second write is bounded by about 10 s plus the two DB writes. "Up to 10 seconds" therefore describes the anchoring call, not the whole window. Both the PR and doc section 121.3 say so (the two DB writes are not timed), so the claim is honest; the comment itself says only "bounded by the anchoring call's AbortSignal.timeout(10000)", which is exactly what is true.

### Findings
**N1 (Info, precision, not a defect).** Comment (a) names one residual path. There is another that this PR does not describe: the anchoring service persists its `anchor_store` row before it answers 202, so a call that the 10 s signal aborts after that persist ends as `anchoringStatus='failed'`; in production the route then runs the compensating delete and answers 503, leaving an anchor with no document. That is consistent with "narrows, does not remove" (it makes the comment more right), but it is a third path the comment does not list. I read it from the code; I did not measure it. Reasonable to leave for the rest of KS-1666.
**N2 (Info).** The author's "53,964 bytes" for the comment-free transpile does not reproduce under my options (I get 53,984 bytes with `removeComments`, ES2020/CommonJS; the AST print is 54,425 chars). Different compiler options, same TypeScript 5.9.3; the equality proof does not depend on the number. Cosmetic.
**N3 (Info).** The test is a text pin (as gate 25's N4): it reads certifications.ts as text, so it proves the comments say the new words, not that they stay true if the code is later reordered. C1 and C2 pin the two code strings the comments rest on, which is the right mitigation.
**N4 (Info).** Docs say "measured 2026-10-29 UTC"; the documents' figures (152/1854) reproduced here. Unchecked: the 48 s run time, tsc/eslint figures, and the pre-push hook counts.

### TESTED / NOT TESTED / HOW
**TESTED:** head pin (start and end); diff scope; patch equality; comment-only AST proof with two mutated controls; both comments against the code; red-first by spark_gate and by my own swap; whole originate jest suite at head and at develop; html_docs_check with planted control; flow-doc numbering and cited line numbers; merge-tree.
**NOT TESTED:** tsc and eslint (author's 0 errors / planted controls not reproduced); the originate integration files (DB-backed); the four platform suites; a running stack; Node 24; timing of the 10 s window under load; the Linear ticket and PR body text (no gh/Linear read); a browser render of the two docs; the pre-push hook.
**HOW:** `git clone --shared` of the checkout into the then-non-existent `.../scratchpad/gate26/clone`; `rev-parse --show-toplevel` asserted equal before any fetch. The checkout's `core.sshCommand` was read with `git config --get` and passed to the clone's fetch with `-c`. Fetched `refs/pull/1822/head` and `develop` only. node_modules: a real directory of symlinks to the checkout's entries, with `@secuura/*` linked inside the clone, so the clone's own freshly built `packages/shared` was the one resolved. TMPDIR=/tmp/g26. Evidence: `spark/` beside this file; scratch in `.../scratchpad/gate26/`.

### Instrument errors
- **I1.** spark_gate first run: `git@github.com: Permission denied (publickey)` / `spark_gate: fetch refs/pull/1822/head failed`. The script's own fetch does not carry the deploy key. I set `core.sshCommand` in MY clone's config (same value as the checkout's) and re-ran; tool not edited.
- **I2.** Second run: `spark_gate: work dir .../gate26/work exists (this script never deletes); pass a fresh --work`. My own error (the first attempt had created it). Re-ran with `--work .../work2`; rc 0.
- **I3.** spark_gate printed an empty `rc=` in my wrapper (the pipe status variable is unset under this shell); the real result is in facts.json and the printed lines. Not a tool fault.
- **I4.** The `pretooluse_no_cd.sh` hook refused `git -C $VAR <write verb>` (checkout, apply) and `rm -rf $VAR` and a `cd`; each was re-issued with a literal scratchpad path or without the variable, against my clone only.
- **I5.** `jest` on the first full-suite call ran only when the test was named; the full runs used `--json --outputFile` and counts were read from the JSON.

### FIX-BEFORE-MERGE
(none)

Optional at merge prep: N1 (consider a one-line mention of the timeout-after-persist path in a later KS-1666 note). If develop moves before merge, the doc section renumber (121) is the merging seat's, as the author stated.
