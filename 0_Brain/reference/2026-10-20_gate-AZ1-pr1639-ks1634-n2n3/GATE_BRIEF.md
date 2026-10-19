# Gate brief: GATE AZ1 = PR #1639 (KS-1634 N2/N3: gate AG1's test-strength notes), Sonnet 5.5, tier 2 (TEST-ONLY), round 1 of 2

Commissioned by Wednesday after Seat R 56th's READY FOR GATE (15:59Z). The author's CLAIM is beside this brief: `R56_READY_1559Z.txt` (read it WHOLE). Background: gate AG1's notes N2/N3 on `f321e95aa` (KS-1634 comment `8380fa24`, Linear, read-only). Secuura only. Tier 2: one test file, +45/-0, no product code changes. **The question is whether the new cells can FAIL for the right reason, not whether they pass.**

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/986d1a05-c6c6-443e-9186-42c238af6685/scratchpad/gate_az1/` via `git clone --shared` from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src`, then fetch `refs/pull/1639/head`, LITERAL paths in every `git -C`. **Every npm / jest / tsc command runs INTO your clone (absolute `node <clone>/node_modules/.bin/<tool>` or `--prefix`). NEVER `npm exec` from your cwd: it is Wednesday's tree.** Build `packages/shared` first.

**Heads (Wednesday's fetch into the cache clone, 03:0x AEDT 2026-10-20):** #1639 head `02168f95d66c926da807477aaf0459f1219bd698`; develop `17ab917aa6f4646d92ce2d1ee9743362ad5bc548`. Landing tree `c5c221c572ed60c62601319f3c0f4b724d33997b` (Wednesday's merge-tree, equal to the author's; strict descendant). Three-dot = 1 file. Re-read both heads at start and before the verdict.

## Questions (instrument for each; name what you did NOT run)
1. **Mutants A and B, yourself, compiling:** A = `simulated: chain.simulated === true` at `services/originate/src/routes/verificationV2.ts:240`; B = the presenter's `Boolean(b.simulated)` (`verification.ts:60`) as `=== true`. Each must red BOTH N3 cells, with every existing control green. Read the lines first; quote their text at develop.
2. **The vacuous-pass trap the author names:** the presenter also flags a fabricated tx by regex (`verification.ts:52`/`:60`). Confirm each N3 cell's tx hash is one the regex does NOT flag (so only the truthiness rule decides). Then plant your own: change one N3 cell's hash to a `mock_tx_` placeholder and show mutant A then PASSES it (proving the author's reason for the real hash).
3. **N2:** force `source` and `documentUuid` wrong at `verificationV2.ts:246-247` separately; S1 and its inverted control must red.
4. **Coverage honesty:** do any of the 7 pre-existing cells change behaviour or lose an assertion? (Diff is +45/-0: confirm nothing weakened.)
5. **Landing:** merge-tree on live develop = `c5c221c572ed…`; the full originate suite at the landing by suite count; the test file type-checked separately (originate tsconfig excludes `__tests__`, KS-1090).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 02168f95d66c... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN. Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker; every zero with a positive control. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.
