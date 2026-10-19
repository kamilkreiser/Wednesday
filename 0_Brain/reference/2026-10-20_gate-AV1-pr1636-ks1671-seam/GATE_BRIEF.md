# Gate brief: GATE AV1 = PR #1636 (KS-1671 follow-up: the `code` read's cells, gate AP1 N3), Sonnet, tier 2, TEST-ONLY, round 1 of 2

Commissioned by Wednesday after Seat R 56th's READY FOR GATE (15:24Z). The author's CLAIM is beside this brief: `R56_READY_1524Z.txt` (read it WHOLE). Background: gate AP1's N3 in `../2026-10-20_gate-AP1-pr1627-ks1671/verdict.md`. Secuura only. Tier 2 (through-code): one new test file, no product change.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Make your clone INSIDE THIS SESSION'S SCRATCHPAD: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a3368218-953e-40df-ac8f-2e5abee5552f/scratchpad/gate_av1/`. Use `git clone --shared` from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src`, then fetch `refs/pull/1636/head` with that clone's core.sshCommand, using LITERAL paths in every `git -C` (a $VAR path is refused by a hook). **EVERY npm / npx / vitest / tsc command runs INTO your clone; NEVER `npm exec` from your cwd (Wednesday's tree).** Build `packages/shared` first.

**Heads (Wednesday's ls-remote via the cache clone, 02:2x AEDT 2026-10-20):** #1636 head `cc07f145ad242a48f211d74ed61526e6d448b83c`; develop `9207fe336797b136f3f12fb6da169fba7fd900b7`. Re-read both at start and before the verdict. Author's predicted landing tree `4139960887f6aac5ceaf90dde79d0cfdd7cc3e51`.

## Questions
1. **Diff:** exactly one new test file under `services/m365-integration/src/__tests__/`; zero product lines (three-dot).
2. **The cells can fail, on the LANDING tree** (develop now has #1633's binding; the branch was cut before it): put the bug back (`const code = req.query.code;` at the read) and confirm K1-K4 red with K5 green; drop the `code` read and confirm K5 red. Do the cells reach the code under test after #1633 (does the seeded pending row now need an organisation to be found)? A cell that turns green because the row is now invisible is a vacuous cell.
3. **Landing:** merge-tree on LIVE develop = the predicted tree; the full m365 suite at the landing; the test file type-checked (KS-1090).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head cc07f145ad24... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings B1../N1.., what was tested and HOW, NOT RUN. Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker; every zero with a positive control. Before you finish run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.
