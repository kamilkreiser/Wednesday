# Gate brief: GATE AU1 = PR #1634 (KS-1658), Sonnet, tier 2, round 1 of 2

Commissioned by Wednesday after Seat C 27th's READY FOR GATE (14:55Z). The author's CLAIM is beside this brief: `C27_READY_1455Z.txt` (read it WHOLE). Commit 1 (`fefd9962962d`) is a Spark pass Wednesday read at source and held (`2_Project_Files/local-model/night/READY_KS-1658-NAMESPACECAUSE-1_*`); **commit 2 (cells D1, D2) is the SEAT's own.** Secuura only. Tier 2: error classification in originate `utils/idNamespaceCollision.ts`, no auth decision.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Make your clone INSIDE THIS SESSION'S SCRATCHPAD: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/a3368218-953e-40df-ac8f-2e5abee5552f/scratchpad/gate_au1/`. Use `git clone --shared` from `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src`, then fetch `refs/pull/1634/head` with that clone's core.sshCommand. **EVERY npm / npx / jest / tsc command runs INTO your clone (`--prefix`, or `node <clone>/node_modules/.bin/<tool>` with absolute paths). NEVER `npm exec` from your cwd: your cwd is Wednesday's tree, and a GO on your verdict is REFUSED by a tool if a stray appears there.** Build `packages/shared` first.

**Heads (Wednesday's ls-remote via the cache clone, 01:5x AEDT 2026-10-20):** #1634 head `91529864158ccc28af95ee982b2f0965b3c317a3`; develop `88b8ceb9f3041672d9575b40c09869d45ab1c111`. Re-read both at start and before the verdict. Author's predicted landing tree `f20edc3ab56f15a9d79773db4b4c13005eb9779a` (the author's).

## Questions (each with its instrument; name what you did NOT run)
1. **The behaviour:** at develop, an unreadable node in an error's chain hides a readable 050/051 migration refusal in its `cause`, so the caller answers 500 where 409 is right. With the fix the walk visits only `cause`, inside its own try/catch, and never throws. Find every CALLER of `isIdNamespaceCollision` / `isLiveAnchorIdClaim` and say which HTTP status changes.
2. **Bounds:** the recovery advances `depth` and respects `MAX_DEPTH` and the `seen` set (no infinite walk on a cyclic `cause`). Plant a cyclic-cause input yourself.
3. **Cells can fail:** the Spark's R1-R3 and C1-C3, and the seat's D1 (red on develop) and D2 (a control). Run at least P3 (recovery without depth+1) and P1 (drop the recovery) yourself; confirm D2 kills P3.
4. **Landing:** merge-tree on LIVE develop = the predicted tree; the full originate suite on the landing tree, compared by cell NAME with develop; three-dot = the PR's 2 files.

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 91529864158c... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings numbered B1.. and N1.., what was tested and HOW, and NOT RUN. Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`, no push. No `cd`, no `rm`, no stderr to /dev/null, no Docker. Every zero gets a positive control. Before you finish run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/ (there must be none).
