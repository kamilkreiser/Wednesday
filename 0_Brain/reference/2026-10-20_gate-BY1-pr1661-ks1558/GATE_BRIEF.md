# Gate brief: GATE BY1 = PR #1661 (KS-1558 m4: check-stack-safety.sh refuses an exception that cites no ticket), Sonnet 5.5, TIER 2, round 1 of 2

Commissioned by Wednesday after Seat G 12th's READY FOR GATE (01:15:22Z). The author's CLAIM is beside this brief: `READY_CLAIM.txt` (read it WHOLE). A developer-facing gate script plus its tests; no runtime surface.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4cf20ec9-03c1-4724-89c4-ae3e1635cfad/scratchpad/gate_by1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`; fetch `refs/pull/1661/head` and develop there. Run the script and its tests only inside that clone; never against the shared VM stack or any box.

**Heads:** read them yourself with ls-remote at start and end (Wednesday read #1661 head `7ecb3257ec69221057b98c4df20d33133451c229` at 12:1x AEDT; develop may move while #1659 merges: derive the landing on live develop).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 7ecb3257ec69... (tier 2, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. **Last line, written LAST:** the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`, labelled with exactly that command; recompute it after writing and say in your final message that it reproduces.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker; every zero with a positive control; restore asserted after every arm. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.

## Questions
1. The check refuses an exception whose REASON cites no ticket, and passes one that does; it does not accept a ticket-shaped token in the PATH half (the author's M1 / cell R4). Run the author's arms (at least 3) plus 2 of your own, including a reason with a malformed key (`KS-` with no number, lowercase `ks-1`).
2. The two existing Akto exceptions still pass (they cite KS-666 / KS-687). A ticketless exception fails OUTSIDE the census branch (the screen's claim): show it.
3. Bash portability: the script under macOS bash 3.2 AND the CI's bash if the repo names one; quoting of paths with spaces; `set -u` behaviour on an empty exception list.
4. Landing: merge-tree on live develop; the script's own test runner green before and after, by cell name.
