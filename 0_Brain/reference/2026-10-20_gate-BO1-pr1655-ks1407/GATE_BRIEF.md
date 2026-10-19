# Gate brief: GATE BO1 = PR #1655 (KS-1407: a successful change-password and a successful reset-password revoke all of the account's sessions (Spark passes raised unmodified + the seat's own cells)), Opus 5.5, TIER 1, round 1 of 2

Commissioned by Wednesday after the author's READY FOR GATE. The author's CLAIM is beside this brief: `READY_CLAIM.txt` (read it WHOLE).

**Project:** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` is READ ONLY. Clone INSIDE `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2a56ac36-e9ca-49f4-8d2d-f02d4a53f9ed/scratchpad/gate_bo1/` via `git clone --shared /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/src <that folder>/src`; fetch `refs/pull/1655/head` and develop there (repoint that scratch clone's origin to GitHub with a repo-local sshCommand only if the PR ref is missing, read-only, as gate BM1 did). npm ONLY with an explicit cwd inside that clone; build `packages/shared` before any service suite.

**Heads (Wednesday's ls-remote, ~10:3x AEDT 2026-10-20):** #1655 head `8e5308a87e14d4a4796e5f838de30dae0838a5bf`; develop `11af03696c9bd966580e52605cb2a361d9c3d29b`. Re-read both at start and end. **Derive the landing tree yourself** on live develop (the author's figure may predate #1651/#1652).

**Verdict file:** `verdict.md` in this folder. First line: `VERDICT: <GO|GO WITH NOTE|NO GO> at head 8e5308a87e14... (tier 1, round 1 of 2; landing tree <sha> on develop <sha>; N blockers, M notes)`. Then BLUF, findings, FOUND / TESTED / HOW, NOT RUN, wall-clock. Last line: the sha256 of `sed '1d;$d' verdict.md`, labelled with that method.

**Rules:** findings only; no GitHub or Linear writes; nothing under `!CODING`; no push; no `cd`; no `rm`; no stderr to /dev/null; no Docker (another seat uses it); every zero with a positive control; red by ASSERTION, never by load failure; each mutant `tsc` rc 0 before it counts; restore asserted after every arm. Before finishing run `git -C /Volumes/DevMASTER/WEDNESDAY status --short` and report every untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/ and 2_Project_Files/fleet/briefs_staged/.

## Questions (instrument for each; name what you did NOT run)
1. **Revocation happens exactly when it should:** after a change/reset whose write LANDED, `revokeAllUserSessions` runs once for that account; NOT for a refused change (wrong current password, weak password, unknown/expired reset token) or a write that did not land. Reset: revocation BEFORE the single-use token is burned. Drive through the real routes.
2. **Adversarial:** can an attacker holding an old session keep it alive across a change or reset by any route (a refresh token, a service token, a different session store, a token minted between the write and the revocation)? Enumerate every session/refresh store in auth and check each is covered by `revokeAllUserSessions` (read it, cite lines).
3. **The caller's own session is revoked too** (stated behaviour): confirm, and report what the API returns to the caller and what an in-repo client would do next (the author found none handles it; re-check with a positive control).
4. **Failure mode:** revocation throws after the password write (e.g. Redis down): what does the request return, and is the password changed? Report.
5. **No weakening:** auth suite by cell NAME at develop vs the landing; re-run the author's mutants (13) on a sample of at least four, plus two of your own.
6. **Landing:** merge-tree on live develop; `tsc --noEmit` rc 0; new tests type-checked in their own program.
