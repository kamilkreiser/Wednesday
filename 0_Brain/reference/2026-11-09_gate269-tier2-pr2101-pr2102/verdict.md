PR 2101: GO WITH NOTES; PR 2102: GO WITH NOTES

# Gate 269 (relaunch), tier 2, round 1 of 2: PR 2101 (KS-1783) and PR 2102 (KS-1864)

Run 2026-11-09 03:54 to 04:01 AEDT. Findings only; nothing posted, nothing fixed.

| PR | head | verdict |
|---|---|---|
| 2101 | 7e0396990dfdc30742e4acef0f079e0ef44d797c | GO WITH NOTES |
| 2102 | 247e62dc7337a0f87e2b8a20d9c6107e6fcccf14 | GO WITH NOTES |

Refs: re-read at start (via ls-remote, then fetch) and at end (04:00:45): develop = 2935f723109756a60cadc5521977c7a036ec322d, PR 2101 = 7e0396990dfd..., PR 2102 = 247e62dc7337.... No difference at any point, and all equal the re-pin. Both PRs are one commit on parent fa0592f3b6f5, so they are behind develop (the old develop 6220c168 and then PR 2069's squash moved on).

Tier 2 stop line: neither PR touches a product byte (2101 = three originate test files; 2102 = four api-gateway test files plus the tool-written baseline). No NEEDS TIER 1 trigger.

## Environment note (affects how my results were produced, not the PRs)
The source checkout's hoisted node_modules has zod 3.25.76, but the repo needs ^4.6.7, so in a clone wired to those symlinks every originate jest suite dies at load (`zod_1.z.config is not a function`, packages/shared/src/validation/zod3-compat.ts:213). I moved my clone's Dev/node_modules symlink-farm aside (to /private/tmp/g269/_quarantine_2026-11-09/dev_node_modules_farm_src) and pointed Dev/node_modules at /private/tmp/g258/Blockchain/Dev/node_modules (zod 4.6.7, read-only use of another gate's tree). With that, everything below ran. Wednesday should know the source checkout's deps are stale for any seat that runs originate jest there.

---

## PR 2101 (KS-1783): GO WITH NOTES

BLUF: the three changed L6 cells now fail on a placeholder-shaped hash and pass on a real one; they passed on the placeholder before. Test-only, 3 files, +16 -3, as stated.

### Findings
1. LOW (note, not a defect): other cells of the same shape remain unpinned. FOUND: in each of the three files the cells that send chainReply's default txHash but do not assert it is real, and that pass with a placeholder default: the L1 pair `RED ... L1 ...: a string "false" verified is not a verified reply` and `CONTROL ...: a boolean false verified is not a verified reply` (verify-route.test.ts and verify.test.ts, `chainReply({ verified: 'false' })` and `chainReply({ verified: false })`), and in the v2 file `CONTROL KS-1634 v2: a reply whose verified is not true makes no match`. TESTED: base files with REAL_TX replaced by `'mock_tx_'+'a'.repeat(64)`: these cells are not in the failing list (they pass), while the CONTROL "real hash stays on-chain" cells fail, so only the on-chain controls pin it. HOW: plant2.sh, below. They are a different claim (verified-gate), the ticket named the L6 cells only, and the seat's READY said "other cells of the same shape beyond the three the ticket names" were NOT done, so this is the seat's own stated gap, not a misstatement. Name only; not fixed. The S1 and "placeholder reply" L6 cells send txHash null on purpose and are correct.
2. INFO: the assertion is `expect(reply.txHash).toMatch(REAL_TX_SHAPE)` on the reply handed in, not on the route output (the route's reply carries txHash null for a simulated reply). The in-code comment says so. That is a fixture guard, not a behaviour assertion; it does what the ticket asks. REAL_TX_SHAPE `/^[0-9a-f]{64}$/` is lowercase-hex-64 only, so an uppercase real hash would trip it (see the UPPER plant); the only hash in the files is lowercase, so no live effect.

### FOUND / TESTED / HOW
- FOUND: the three edits are exactly the L6 cells `simulated true with a real hash`: verify-route (line ~109), verify (line ~104), v2 (line 117). Each keeps `reply = chainReply({simulated:true})`, asserts `reply.txHash` matches the shape, then passes `reply` to the caller. Nothing else changed; the new constant is the only addition at module scope in two files (v2 already had it, from KS-1634 gate AZ1).
- TESTED head, 3 files: 3 suites, 22 of 22 pass (seat: 6/6, 6/6, 10/10, equals 22).
- TESTED base-vs-head with a placeholder default (the seat's plant, reproduced on all three files): on develop 2935f723, REAL_TX = `'mock_tx_'+'a'.repeat(64)` gives 10 failed / 12 passed, and the three target L6 cells are among the PASSING (the gap). On the head with the same plant: 13 failed / 9 passed, the three L6 cells now FAIL by assertion. The difference is exactly the three L6 cells, matching the seat's 2/2/6 unpatched vs 3/3/7 patched (2+2+6=10, 3+3+7=13).
- TESTED my own variants on the head (each applied to all 3 files, restored by `git checkout`, `git diff` empty after): `tx_sim_`+57 hex, `tx_`+61 hex, `abc123` (short): 13 failed each, the L6 cells among them. UPPERCASE of the real hash: only the 5 shape-pinned cells fail (3 L6 + 2 v2 N3), controls pass, so the shape pin is stricter than the presenter, as designed. On base with UPPER: only the 2 pre-existing v2 N3 cells fail, so the L6 cells did not pin shape before.
- Control that the red is real: the unplanted head is 22/22 green after every plant restore.
- Merge tree on develop 2935f723: clean (tree 5ca46271888e), rc 0. In a merge of develop + PR 2101 + PR 2102 the three files pass 22/22.
- Paths shared with PR 2102: none (paths diff of the two heads' files, and merge-tree of the two heads clean, tree fccae9af00583b). Against PRs 2070 to 2100 (31 PR heads fetched; the squash merges mean I cannot tell closed from open, so I checked all): zero overlapping paths (positive control: the same loop reports 3 hits for 2101 against its own path list). Develop's own move since fa0592f (8 files: preflight, api-gateway ks570-proxy-mount-auth test, an auth ks1858 test, 4 fragments) touches none of 2101's files.
- Words (READY mail, since I could not read the PR body or ticket comment; see below): file counts, +16 -3, per-file +6 -1/+6 -1/+4 -1 (git stat shows 7/7/5 = adds+dels), "zero product bytes", the 2/2/6 and 3/3/7 counts, and the line-117 location were each true at this head.

## PR 2102 (KS-1864): GO WITH NOTES

BLUF: the four test edits are type-only; the check on the head gives 15 errors, 15 in the baseline, 0 stale, rc 0; every removed baseline line is one the head no longer produces; the baseline file is byte-identical to what `check.cjs --update` writes; a planted type error gives rc 1.

### Findings
1. LOW (note): the `examined-test-files` floor moves 138 to 168, part of the tool-written change. It is true (the tool examines 168 test files on the head and, equally, on develop 2935f723; the 138 on develop was just a stale low floor) and the tool is documented to set the floor to the current count, but it is a reviewable +30 that the diff carries beside the 5 removed error lines. The seat and the READY named it. Raising a floor only tightens the check. No action needed beyond Kam/Wednesday knowing it is in the PR.
2. LOW (note on running the check): `check.cjs services/api-gateway` with a RELATIVE service path only works with cwd = Blockchain/Dev (I could not cd, so I passed the absolute service path; same result, same baseline). Not a PR defect.
3. INFO: ks1374 edit is `(await r.json()) as { error: { code: string } }`; the transpiled JS differs from base only by a pair of parentheses, which is a no-op. The other three files emit byte-identical JS (whitespace-normalised).

### FOUND / TESTED / HOW
- FOUND: four test files, each a one-line type edit: ks1374 (cast of `r.json()`), ks1464 (`(c: unknown[])`, `(l: string)` annotations), ks695 (`(c: unknown[])`), rateLimitEnforce (`import type { Response }`, `makeRes(): MockRes & Response`, `return res as unknown as MockRes & Response`). No assertion text, no expected value, no mock behaviour changed.
- TESTED type-only: ts.transpileModule of base vs head for each (comments and whitespace stripped): ks1464, ks695, rateLimitEnforce IDENTICAL JS; ks1374 differs by parentheses only. Runtime: the four files on the head, vitest: 4 files, 38 of 38 pass (seat: 38 of 38).
- TESTED the ratchet on the head (node check.cjs with absolute service dir): `tsc examined 206 files, 168 of them under __tests__; 15 errors: 15 in the baseline, 0 new; 0 stale baseline entries.` rc 0.
- TESTED every removed baseline line: with an empty baseline on the head, the 15 errors reported are exactly csrf.test.ts (10, TS2345) and ks1165 (4 TS2345 + 1 TS2571), i.e. the three lines that remain, and none of the five removed entries' files appear. On develop 2935f723 the same run lists 25 errors, including exactly the removed ones: ks1374 TS18046 (1), ks1464 TS7006 (2, two fingerprints), ks695 TS7006 (1), rateLimitEnforce TS2345 (6). So 5 lines removed, all 10 errors they admitted (1+1+1+1+6, ks1464 split in two lines) are gone from the head, and no still-erroring line was removed. Develop's unpatched baseline: 25 errors, 25 in baseline, 0 stale, rc 0 (also true after develop's ks570 change).
- TESTED the baseline is tool-written: copied the base baseline to a temp file and ran `--update --baseline <copy>`: it said "baseline lowered to 15 errors in 3 entries (5 stale entries dropped or reduced); examined-test-files 138 -> 168", and the result is byte-identical (cmp) to the PR's baseline file. This meets Wednesday's ruling (allowed only as written by `--update`).
- TESTED plants (restored by checkout, tree clean after): (A) appended `const g269planted: number = 'x';` to rateLimitEnforce.test.ts: rc 1, "17 errors: 15 in the baseline, 2 new" (the second is my unused-variable TS6133, so 2 not the seat's 1); (B) reverted the ks1464 fix to the base file: rc 1, 2 new (the same TS7006 pair); (E) `// @ts-nocheck` in rateLimitEnforce.test.ts: rc 1, flagged by name. Unplanted head after restore: 15/15/0, rc 0.
- Merge tree on develop 2935f723: clean (tree feb4b06965c8), rc 0. Real merge of develop + 2101 + 2102 in the clone: check.cjs 15/15/0 stale, 168 examined, and the whole api-gateway vitest suite 168 files, 1880 of 1880 pass (seat's 1875 was on fa0592f; develop's ks570 change adds 5 cells; and "501 files" in the READY is not a figure I reproduced, which is a different count, not a failure).
- Paths shared with PR 2101: none. Against PRs 2070 to 2100: zero overlap (method as above). Develop's move since fa0592f touches api-gateway `ks570-proxy-mount-auth.test.ts`, which is none of 2102's five files and adds no type error (develop's check is 25/25/0).
- Words: the READY's file count (5, +7 -11), the per-file counts, the baseline +1 -6, "15 errors / 15 / 0 stale rc 0", "after the update 15/15/0", and the planted-error rc 1 were each true at this head.

---

## What was NOT tested
- The PR bodies and the Linear ticket comments (86220b06..., 88f6775d...) themselves: the common rules allow network for git fetch only, so I did not read them. I checked the same factual claims as they appear in the T 16th READY mails (counts, red-proofs, ratchet numbers, "zero product bytes"); wording of the PR body and ticket comment as posted is unverified here. Wednesday should read them or tell me to.
- The cards (decision_queue show) were not read; the commission cites none for these two.
- Whether the PRs are open or closed: not determinable by git. I compared against all 31 PR heads 2070 to 2100 instead.
- Node 24 (this ran on whatever node is on the box; the seat said v26.8.1, not LTS 24; I did not record mine).
- The other 15 baselined api-gateway errors, other services' baselines, anything needing a booted service or the platform suites; the whole originate suite (I ran the three files, plus the whole api-gateway suite on the merged tree only).
- The pre-push preflight (13/16 legs, 3 skipped) claim in the READYs: not reproduced.
- The bot moving the tickets to In Progress (BOARD NOTE): not checked.

## Conduct and clone
- Clone: /private/tmp/g269/c (reused from the dead run; it was a partial blob:none clone, with 3 untracked node_modules symlinks), size 382 MB total for /private/tmp/g269 (du -sh at 04:00). Not removed (QA no-rm); Wednesday may remove it. Beside it: f1, f2, tp.cjs from the dead run (left), my temp files (empty_base.txt, bl_*.txt, chk_*.txt, head_all.txt, mt*.txt, paths_*.txt, devchg.txt), and the quarantined farm under _quarantine_2026-11-09/dev_node_modules_farm_src. Refs I created in the clone: refs/q/p2101, p2102, o2070 to o2100.
- Free space DevMASTER 14 GiB at start and end (above the 10 GiB floor); load1 4.05 at start, 6.75 at end (under 8).
- No cd; all git work in /private/tmp/g269/c using its literal path (the hook refuses write verbs when the path is a shell variable); my scratch scripts (plant1.sh, plant2.sh, plant3.sh, ov.sh, tp2.cjs) are in the session scratchpad. Nothing outside /private/tmp/g269, the scratchpad and this folder was written; the source checkout and g258 were only read.
- Fetch used the Blockchain deploy key via GIT_SSH_COMMAND from the shell; that is the only network use.
