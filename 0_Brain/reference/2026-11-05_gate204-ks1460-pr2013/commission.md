# Gate 204 commission — Secuura / Blockchain, PR 2013 (KS-1460 rows 4 and 6 + the row-1 log: social level raise confirms the write; rehash log is truthful), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 19:2x AEDT. Model: Opus (tier 1: auth routes — sessions and tokens are issued on these paths). QA GATE: findings only; fix nothing; write nothing outside this folder; no box; post nothing to Linear or GitHub.
Write `verdict.md` here EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before the verdict)`), overwrite at the end. Final line 1 is exactly `GO`, `GO WITH NOTES` or `NO GO (<reason>)`.
Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md (clone by SHA into a subfolder HERE; only read-only git verbs against /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files), then `ready_2013.txt` here (Seat J 16th's READY, verbatim). Never `cd`; never a recursive grep/find over 0_Brain/reference, local-model/ or 5_Project_History.

## Subject (Wednesday's `git ls-remote origin`, 19:26:22 AEDT)
refs/pull/2013/head = `ea1952fa00d7f942edb298af98728d20497e53a4`; base = `5fc5569ed96ac61f64823cc9e1fa841899aa1f62`; develop NOW = `8c5da776eccf3a4361d64ca3d44f83420ef7dd60`. 6 files, +436/-4 (services/auth/src/routes/auth.ts +21/-4, two new tests, a mock-only edit in ks795, fragments).

## Wednesday's ruling you check against (binding; the 06:05:32Z table to J 16th)
Rows 4 (social callback) and 6 (POST /social/link): the SOCIAL level raise goes through updateUserOrThrow; a write that did not land answers 503 BEFORE any session, token, cookie or success answer is issued. Row 1: the "rehashed" info line only when the write landed, a warn otherwise; the login itself is unchanged. Rows 2, 3, 5 left (3 and 5 are KS-1672's).

## Questions
1. Scope: exactly 6 paths; auth.ts changes only rows 4, 6 and the row-1 log; ks795's edit is the mock only (no assertion changed: prove line by line).
2. Rows 4 and 6, base vs head on the real routes with only repos/providers doubled: write lands / write affects 0 rows / write throws. At head, on a non-landed write: 503, AND no session row, no refresh token, no Set-Cookie, no access token, no success body. On a landed write: identical to base (status, body shape, cookies). "N of M".
3. Direction: no input where head issues a session or token that base did not; no input where head refuses a login base allowed EXCEPT the ruled non-landed-write case.
4. Row 1: login answer and side effects byte-identical base vs head for landed / not landed / throws; only the log line differs as ruled; the warn line carries no password, hash or token (plant markers).
5. Mutants: reproduce 3 of the seat's 7 and one of your own (e.g. the 503 sent AFTER the session is created).
6. Suites: auth service vitest (classify failures same-on-base vs new; ks949/auth.integration timeouts are known load flakes), tsc, test-types, eslint, docs-fragments with a planted defect.
7. Merge tree onto develop 8c5da776eccf: rc and tree; shared paths with PR 2007/2010/2011 = 0 (planted control).

## Output
`verdict.md` (verdict line, BLUF, findings with severity, file:line, evidence path). Final message: verdict line + one line per finding.
