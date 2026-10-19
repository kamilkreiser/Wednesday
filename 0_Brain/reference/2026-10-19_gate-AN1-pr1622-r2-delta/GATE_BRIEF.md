# Gate brief: GATE AN1 = PR #1622 (KS-1641 finding 2) DELTA, Opus, tier 1, round 2 of 2 (THE CAP)

Commissioned by Wednesday after Seat R 55th's READY FOR DELTA GATE (12:28Z). The author's CLAIM is beside this brief: `R55_READY_DELTA_1228Z.txt` (read it WHOLE). Round 1's brief and verdict (gate AM1, NO GO: a lone-surrogate cut made `encodeURIComponent` throw and killed the m365 process) are in `../2026-10-19_gate-AM1-pr1622-ks1641/`: read `verdict.md` there WHOLE first. Secuura only.

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Every write verb runs in your own clone in your scratch: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/08573273-0b69-4d9e-abf5-9b213ac8c2f2/scratchpad/an1/`. Point every npm/vitest/tsx command INTO that clone, never from your cwd; never write a file anywhere in /Volumes/DevMASTER/WEDNESDAY except `verdict.md`; quote every `>` inside echo text. Build `packages/shared` first.

**Heads:** #1622 head `5c6daf6ae83e934d2e3655bf1abe452603fa9c59` (round 1 was `e065dc9e06d2b52b50944584e9505b95c897dee6`); develop `115797747cb60009e781d80e9059dbbed69e1ac3`. Re-read at start and before the verdict. Predicted landing tree `48f08c661e686bd23adbbc5e3da5f4d73fa33e92`.

**Round 2 of 2:** a NO GO ships nothing. Be exact about what blocks.

## Questions (each with its instrument; name what you did NOT run)
1. **B1 closed on the real process:** re-run AM1's kill input (`'A'*199` + U+1F600 + `'zz'`) and its aligned control against the landing tree with the real server (tsx, Node 24): 302 with a bounded valid URL, and `/health` 200 afterwards, process alive. Then FUZZ: at least a few hundred random strings mixing ASCII, BMP, astral pairs, lone high and lone low surrogates, `%`, `&`, `#`, CRLF, at lengths around 199-201 code points and very long; zero process deaths, every answer a 302 to the same host/path/keys. Report the maximum Location length.
2. **Defence 1 (`capCodePoints`)**: correct for every input shape including lone surrogates already present in the input (not created by the cut). Does a lone surrogate in the INPUT still reach `encodeURIComponent` unguarded anywhere on this route?
3. **Defence 2 (`encodeReflectedText`)**: the author says it is unreachable over HTTP once defence 1 holds and is pinned only by a direct cell (E7). Confirm by mutation: remove defence 1 and show defence 2 alone keeps the process alive (and a request-level cell then exercises it); remove defence 2 and show defence 1 alone suffices over HTTP. Its regex: valid pairs untouched, lone highs and lone lows replaced.
4. **N2/N3 (log caps at ~:474 and ~:464):** capped by code point too? Can either log line throw on a lone surrogate (it should not need encoding; confirm)?
5. **Cells can fail:** each of E5-E10 reds on a mutant named for it (plant your own where the author's are missing); E1-E4 unchanged.
6. **Exported helpers:** exporting from `index.ts` must not change the module's side effects at import (does importing index.ts in a test start a server or connect anything?). Check.
7. **Landing:** merge-tree on LIVE develop; m365 suite on the landing tree and at develop; a type-check that includes the test file; three-dot = the PR's 2 files.

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 5c6daf6ae83e... (tier 1 delta, round 2 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Last line: the sha256 of `sed '1d;$d' verdict.md | shasum -a 256`.

**Rules:** findings only: no fixes, no GitHub or Linear writes, nothing under `!CODING`, no push. No `cd`, no `rm`, no stderr to /dev/null, no Docker. Every zero gets a positive control. zsh: no PIPESTATUS.
