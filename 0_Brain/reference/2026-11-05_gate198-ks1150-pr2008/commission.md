# Gate 198 commission — Secuura / Blockchain, PR 2008 (KS-1150 R-2 + R-3: OAuth refresh grant denylists the presented jti; a ServiceUnavailableError answers 503), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 17:4x AEDT. Model: Opus (routing v1.0 row G1: auth/credential surface). QA GATE: findings only; fix nothing; write nothing outside this folder; no box; post nothing to Linear or GitHub.
Write `verdict.md` here EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before the verdict)`), overwrite at the end. Final line 1 is exactly `GO`, `GO WITH NOTES` or `NO GO (<reason>)`.
Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md (method: clone by SHA into a subfolder HERE; only read-only git verbs against the shared checkout /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files), then `ready_2008.txt` and `ready_2008_correction.txt` here (the correction restores two words lost from the mail text: "has no `next`" and "0 `error TS` lines").

## Subject (Wednesday's ls-remote, 17:4x AEDT)
refs/pull/2008/head = `65142195fca6a01a1ded43dd59d5ae527b3e3b33`; develop = base = `5fc5569ed96ac61f64823cc9e1fa841899aa1f62`. Seat J 16th (Opus). 6 files per the READY.
KS-1150's Done-when for these two items: "a replayed OAuth refresh token is refused with 400 and its jti reads as denylisted (R-2), with a red-first cell" and "a `ServiceUnavailableError` from either user lookup on `/token` answers 503 `SERVICE_UNAVAILABLE` (R-3), with a red-first cell"; "the ks790 / ks820-821 / ks823 harnesses stay green".
Wednesday's ruling D1 (binding): denylist the presented jti on a successful refresh; NO session rotation and NO burn-the-session (that decides KS-1690's session-binding question, which is not in this PR). D2: ServiceUnavailableError -> 503, every other throw keeps today's 500.

## Questions (measure; the READY's figures are claims)
1. Scope: exactly the 6 paths; ks823 and ks835 change ONLY their mock line (denylistRefreshJti as a no-op), no assertion. Prove it with a hunk count and a byte-equal check of every other line.
2. R-2 behaviour, real route with only Redis/repos doubled: a refresh token used once succeeds and a second presentation of the same token is refused 400 and its jti is denylisted; a REFUSED presentation (bad client, wrong binding, expired) denylists nothing; the denylist write happens BEFORE createSession and the mint; a failed denylist write delivers no token pair and leaves the old token live. Base vs head table.
3. D1 boundary: show the head performs no session rotation or session revocation on refresh (grep and a behavioural cell); KS-1690's half is untouched.
4. R-3: a ServiceUnavailableError from each user lookup -> 503 with the fixed description (it must NOT echo the thrown message: plant a marker in the error message and search the whole body and headers, expect 0); every other throw -> 500 as at base; the guarded instanceof survives a revoked Proxy (the KS-1868 cell) and the request is always answered.
5. Direction: head never MORE permissive than base for any presentation (no 200 at head where base refused). "N of M".
6. Mutants: reproduce 4 of the seat's 9 plus two of your own: (i) denylist written before the success checks (burns refused tokens); (ii) the 503 branch echoes err.message.
7. Suites at base and head: the whole services/auth suite (vitest JSON), tsc, test-type ratchet, eslint, each with a planted-defect control. The seat reports load-induced timeouts in ks949 and auth.integration on BOTH sides: classify every failure you see as same-on-base or new.
8. Merge tree in your clone, rc and tree id.
9. PR body read whole (gh may be unavailable: the seat's drafts folder and a body sha are acceptable if you say so): it must state D1's boundary, the 503 mapping, the concurrent-replay race as a known limit not fixed here, Node v26 not 24, the NOT-run list.

## Output
`verdict.md` (verdict line, BLUF, findings F1..Fn with severity, file:line, evidence path, fix), evidence files here. Final message: the verdict line and one line per finding.
