## VERDICT: GO WITH NOTE

Majors: 0 | Minors: 4 | Tier: 2 (tooling/test-only) | Gate: Sonnet independent QA

- PR: Secuura/Distributed_Secuura #1513 (KS-1520)
- Head tested: 6c86f55859a1aeb9e1a730e7a378153b22d6e929 (fetched refs/pull/1513/head, equals the stated sha exactly)
- Base: f6f2a539f4a027a0bc60d7bf4b839a352f2b7032 (merge-base with develop AND pr1513^, both equal)
- Develop used: 629349dac602fa39087e934d4b77e52b18afbc94 (fetched refs/heads/develop, equals the stated sha)
- How the tree was obtained: `git clone --shared` of the Blockchain 2_Project_Files repo into the scratchpad (source repo not touched), remote set to git@github.com:Secuura/Distributed_Secuura.git, fetch with the repo's own core.sshCommand value. Trees extracted with `git archive` (pr1513 and pr1513^, Blockchain/Dev only) into scratch dirs h2/ and b2/. All mutation was done on scratch copies. Nothing was written inside /Volumes/DevMASTER/!CODING.
- Note on paths: in the repo the files are under Blockchain/Dev/ (Blockchain/Dev/scripts/preflight/test-types-ratchet.sh and Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh).

## Findings

| # | Sev | Where | Finding |
|---|-----|-------|---------|
| 1 | Minor | Blockchain/Dev/scripts/__tests__/preflight_test_types_ratchet_leg.test.sh (stub cell block, rc-1 branch) | The rc-1 wording in the leg (`1) why="a NEW test-file type error, ..."`) is not pinned by any cell. Mutant R1text (rc-1 `why` replaced with "something") leaves the new suite at 36/0. The PR pins rc 2 and rc 3 text only. Cosmetic text, no gating effect. |
| 2 | Minor | same file, `varnames_of` cell | The five-locals cell is deliberate friction and does false-trip on a legitimate harmless local. Planted `for i in 1 2 3; do echo "$i" >/dev/null; done`: extracted names go from `DEV_ROOT failed rc svc why` to `DEV_ROOT failed i rc svc why`, so the cell would go red. A loop with no `$i` expansion does not trip it. Fix on a legitimate new local is to edit the expected string. Acceptable: the failure description names the intent. |
| 3 | Minor | same file, two prose-pinning cells | The closing-advice cell (`in the test file` absent, `a product file` present) and the rc-2 cell (`the check could not run`) pin prose, so a rewording breaks them. Verified they do catch W1/W2-style edits. Brittle by design, but each fires on exactly one cell. Acceptable. |
| 4 | Minor | same file, stub cells | Stub cells cannot see arguments passed to the checker. Mutant X4 (`check.cjs "$svc" --update`) passes every stub cell; it is caught (4 red) only by the real-checker cells, which SKIP with no workspace install (measured: with no install the X4 run is 23 passed 9 failed, identical to the no-install control). So that class is guarded only where an install exists (CI/seat with install). The builder named this attack point; the real-checker cells cover it with an install. Acceptable. |

No Major. No logic line changed in the script.

## What I ran, with exact results

1. Topology
   - merge-base(pr1513, develop) = pr1513^ = f6f2a539f4a0... ; `rev-list --count pr1513^..pr1513` = 1 commit.
   - `git diff --numstat pr1513^ pr1513`: `71 1 .../__tests__/preflight_test_types_ratchet_leg.test.sh`, `17 14 .../preflight/test-types-ratchet.sh`. Exactly two files, +88 -15. CLAUDE.md is not in the diff. (Positive control for "exactly two files": the same command against develop..pr1513 lists the two PR files plus the two api-gateway files PR #1512 changed, as expected; develop moved from the base by only those two api-gateway files.)
   - `git merge-tree --write-tree pr1513 origin/develop` (scratch clone): rc 0, tree 5aa34975fba1222fc74753647a3e7c423dce0e35, clean, equals the builder's prediction.
2. Text-only claim for the script
   - Method A: every +/- line of `diff -U0` classified; a line passes only if it is a `#` comment or an `echo "..."` whose quoted text contains no `$`, backtick or backslash. Real result: zero flagged lines. Control 1 (planted `rc=$? ; rc=0`): 2 lines flagged. Control 2 (planted `$(id)` inside an echo string): flagged.
   - Method B (independent): strip comments, blank the text of every `echo "..."`, diff base vs head. Result: the only difference is one added line `echo ""` (the closing advice was re-wrapped from 3 echo lines to 4). Control: the planted logic change gives a different normalised md5 from both base and head; the planted `$(id)` echo does NOT differ under Method B (that is what Method A covers; the two methods are complementary).
   - Reading: the added echo is a pure-text statement in the failure branch (inside `if [ "$failed" -ne 0 ]`, before `exit 1`). `bash -n` on head leg: ok. Claim "comments and closing echoes only" holds. Note it is one more echo statement, not only edited text; harmless.
3. Test file runs (environment: no install at first; see "environment" below)
   - With a workspace install (host node_modules linked into scratch, @secuura workspace links re-pointed into the scratch tree, packages/shared built with the source tree's tsc): new test, head script, /bin/bash 3.2.57: `36 passed, 0 failed`. PATH `bash` (also GNU bash 3.2.57): `36 passed, 0 failed`.
   - Original (base) test vs head script: `26 passed, 0 failed`. Control, base test vs base script: `26 passed, 0 failed`.
   - New test vs base script: `35 passed, 1 failed`; the single red cell is "the closing advice does not tell the pusher to fix 'the test file' ..." (want "no|yes", got "yes|no"). Matches the claim exactly.
   - Without an install (the first run, before I linked one): new test/head script `23 passed, 9 failed`; base test/head script `13 passed, 9 failed`. The 9 red are the real-checker cells that depend on a compiler (the leg SKIPs). The stub cells all passed in that state, which confirms claim (b) that stub cells need no compiler. The same 9 are red for the base test file, so they are not caused by the PR.
4. Tampers on a scratch copy of the leg (in place in h2/, restored from a saved copy; sha256 of the leg checked equal before and after every one: 401fca9e15ee3972... both ends). The builder's exact mutant text is not available; mine are described exactly below, so red-set sizes differ from the claim for G4, G5 and G7 only because my mutants are not identical to theirs.
   - Control (no mutation): 36/0.
   - G3 `set -- ${TYPECHECK_SERVICES:-services/auth services/api-gateway}`: 1 red (the five-locals cell). Claim: variable cell only. MATCH. Old suite: 26/0 (escape confirmed).
   - G4 `failed=$((failed+1)); break` (stop at first failing service): 6 red (the claim says 5 for its G4). Old suite: 25/1.
   - G5 `if [ "$rc" -ne 0 ] && [ "$rc" -ne 2 ]` (rc 2 treated as pass): 3 red (claim says 7 for its G5). Old suite: 24/2.
   - G7 `2) why="the check broke ..."`: 1 red (the rc-2 wording cell). MATCH in shape. Old suite 26/0 (escape).
   - D `set -- services/auth` (gateway dropped from default list): 11 red. Claim 11. MATCH. Old suite: 22/4.
   - W1 closing advice reverted to "test file": 1 red, its cell only. MATCH.
   - W2 "it did not run" replacing "the check could not run": 1 red, its cell only. MATCH.
   - Reading: the claim that the old suite had escapes is confirmed for my G3 and G7 (old suite 26/0) and for X5/X7 below. I could not confirm the claim for the builder's G4/G5 because my mutants for those are caught by the old suite, so their mutants differ from mine. That specific claim is not independently confirmed; it is not material to the verdict.
   - My own mutants (new suite red cells count / old suite result):
     - X1 `|| true` on the checker call: 12 red.
     - X2 rc 1 and rc 2 wording swapped: 1 red (the rc-2 wording cell).
     - X3 checker path changed to checkx.cjs: 14 red.
     - X4 `--update` appended to the checker call: 4 red with an install; 0 more than the no-install control without one (Minor 4).
     - X5 `rc=0` forced for the api-gateway: 5 red (old suite 26/0, an escape).
     - X6 final `exit 1` changed to `exit 0`: 11 red.
     - X7 api-gateway rc 1 forced to 0 only: 3 red (old suite 26/0, an escape).
     - X9 `$svc` argument dropped, no install: 13 red vs 9 baseline red, so caught by stub cells without an install.
     - R1text: escapes (0 red), Minor 1.
     - X8 (`OK -` vs `OK —` in the final message): the run did not report a result; untested.
   - X4 left scratch baseline files changed in h2/ (the checker's `--update` rewrote baseline-api-gateway.txt and created a clean-fixture baseline). I restored baseline-api-gateway.txt from the pr1513 tree and verified byte-identical via cmp for both baseline files, moved the stray file into the scratchpad. All scratch only.
5. Attack points: see Minors 2, 3, 4. Verdicts: stub cells do not test the checker path: true for argument-shape mutants (X4), covered by real cells where an install exists, wrong-path mutants (X3) ARE caught by stub cells; variable-name cell false-trips on a harmless local (verified), acceptable friction; two prose cells are brittle, acceptable.
6. Portability: `scripts/check-script-portability.sh` run in the head tree: `OK — 7 portability rules hold across 73 shell scripts (KS-666).` Same on the base tree: 73. The builder reported 104 scripts; my number differs because I extracted only Blockchain/Dev (not the whole repo), and the scan root is a directory scan. Rules (7) match. The PR adds no new .sh file, so the count would not change anyway.

Environment notes: the host install is not a pristine `npm ci`. Before building packages/shared in scratch, the default-run real-checker cells went red on a TS2307 for `@secuura/shared/documents/default-type` because the borrowed workspace link resolved into the stale source checkout. Re-pointing the @secuura links into the scratch tree and building shared fixed it; this is my environment, not the PR.

## What I did NOT test

- The repo's full test suites, CI, docker, or anything needing network services.
- preflight.sh end to end (only the cells that execute its step-16 block inside the test file).
- A pristine `npm ci` install; I used a linked host install.
- The builder's exact mutants (text unavailable); X8 produced no result.
- Portability across the whole repo (scanned Blockchain/Dev only; count 73 vs claimed 104).
- Behaviour on macOS other than bash 3.2.57 (both /bin/bash and PATH bash are that version here; no bash 5 run).
- GitHub review state, comments, or CI status of PR #1513 (no network posting or reading beyond the fetch).
- Anything on develop beyond the merge-tree result (no build of the merged tree).
