# Gate 205 commission — Secuura / Blockchain, PR 2014 (KS-1968 B2: breached password refused at change-password), TIER 1, ROUND 1 of 2

Written by Wednesday 2026-11-05 ~20:11 AEDT. Model: Opus (tier 1: an auth route; a password rule and a third-party call; Kam's card says the tier-1 Opus gate). QA GATE: findings only; fix nothing; write nothing outside this folder; no box; post nothing to Linear or GitHub.
Write `verdict.md` here EARLY as a stub (line 1 `NO GO (INCOMPLETE: killed before the verdict)`; Wednesday already wrote one), overwrite at the end. Final line 1 is exactly `GO`, `GO WITH NOTES` or `NO GO (<reason>)`.
Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md (clone by SHA into a subfolder HERE; only read-only git verbs against /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files), then `ready_2014.txt` here (Seat J 16th's READY, verbatim). Never `cd`; never a recursive grep/find over 0_Brain/reference, local-model/ or 5_Project_History. NO network call to api.pwnedpasswords.com or any other external host: double the breach fetch.

## Subject (Wednesday's `git ls-remote origin`, 20:11:00 AEDT)
refs/pull/2014/head = `fb1e054d53a8fb258f050034e5b26c637ab9c664`; base = `5fc5569ed96ac61f64823cc9e1fa841899aa1f62` (seat-stated: one commit on it; verify); develop NOW = `688c5cc177f85a11e050357856eb69ee4f4a9069`. Seat-stated 4 files, +236/-1 (services/auth/src/routes/users.ts +12/-1, a new test, a fragment pair).

## Kam's ruling you check against (binding)
Card `secuura-hibp-breach-check-never-runs-1103` = a (ruled 2026-11-03T15:54:16+11:00): "Wire it in: refuse a breached password at sign-up, reset and change-password; if the breach service is down, allow it (as written)". Detail: "behind the existing HIBP_ENABLED switch, tier 1 Opus gate. The user sees 'this password has appeared in a data breach, choose another'. Outage = allowed, so sign-ups never depend on a third party." This PR is B2 = change-password only (B1 register + reset is separate).

## Questions
1. Scope: exactly the seat's 4 paths; password.ts unchanged; users.ts changes only the change-password handler.
2. Order, base vs head on the real route with only repos and the breach fetch doubled: the breach check runs AFTER the current-password check and the strength rules, and BEFORE the hash, the store, the write and the session revocation. Prove that a breached password causes NO write, NO session revocation and NO hash call; a wrong current password and a weak password make NO breach lookup.
3. Decision table: {breached / not breached} x {service ok / throws / non-200 / timeout} x {HIBP_ENABLED unset / true / false}. Head: 422 VALIDATION_ERROR with the ruled text and details on newPassword only when breached AND the service answered; every outage cell and every disabled cell is identical to base. "N of M".
4. Privacy: only the first 5 hex characters of the SHA-1 leave the process (k-anonymity); the password, the full hash and the suffix appear in NO log line, error body or thrown message (plant marker passwords and grep the captured output).
5. Direction: no input where head allows a change base refused; the only new refusal is the ruled breached-and-answered case.
6. Mutants: reproduce 3 of the seat's 7 and one of your own (e.g. the lookup after the write; the full hash sent).
7. Suites: auth service vitest (classify failures same-on-base vs new; ks949 load timeouts and ks795/ks819 cold-import hook timeouts are known), tsc, test-types, eslint, docs-fragments with a planted defect.
8. Merge tree onto develop 688c5cc177f8: rc and tree; shared paths with everything merged since 5fc5569ed96a (PR 2007, 2010, 2011, 2012) = 0, planted control. Also report any shared path with OPEN PR 2008 (KS-1150, auth oauth.ts) and PR 2013 (KS-1460, auth.ts) — those merge first.

## Output
`verdict.md` (verdict line, BLUF, findings with severity, file:line, evidence path). Final message: verdict line + one line per finding.
