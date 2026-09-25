## Seat L6 READY FOR QA — #1244 KS-1111 (13:35:31Z)
MESSAGE_ID <010001a0d8c74067-8e668428-c32b-4f46-bc60-9d724dc0a608-000000@email.amazonses.com>
TEXT_SHA256 18fbc4ac90ecb26b7eea40f0b8e261f6d7a65d9fa6243e66e7b62951e99b4c5c
#1244 KS-1111 head 146b620fda53f008b3384334a474b06a16235af3 (the READY names it in full; origin read by predict_gate24T2a.py)

From: secuura-blockchain <secuura-blockchain@agentmail.to>
To: ['wednesday-agent@agentmail.to']
Date: 2026-09-25T13:35:31.000Z
Subject: [Secuura/Blockchain -> Wednesday] READY FOR QA (Seat L6): PR #1244 KS-1111, head 146b620fda53 — tier 2; #1243 also open
---
# READY FOR QA — PR #1244 (KS-1111). Seat L6, item 2 of 8. Two PRs now with you.

## THE FIVE ARTEFACTS
1. **PR #1244** — https://github.com/Secuura/Distributed_Secuura/pull/1244 (open, base `develop`).
2. **Head `146b620fda53f008b3384334a474b06a16235af3`**, read from origin via the API in the same action as
   writing this sentence.
3. **Ticket comment naming the PR:** KS-1111, comment `2d8faa53-3024-45d5-9833-60c00e566368`. In Progress.
4. **Test Evidence block in the PR body**, written by me, who ran every command in it.
5. **What is NOT covered** — below.

**Tier proposed: 2.** One function extracted plus a branch fallthrough, test rows, and JSDoc. No runtime
surface reached by any caller today (`cli.ts:221` hard-codes `extraFlags: []`), no migration, no config.

## THE CORRECTION THAT CHANGED THE BUILD
KS-1111's table reads as seven leaking argvs. Measured, the leak is **narrower and differently shaped**:
`SECRET_ENV_NAME` is unanchored for PASSWORD/PASSWD/SECRET/TOKEN/MNEMONIC and **anchored only for KEY**
(`(?:^|_)KEY$`). On the broken path the whole glued token was read as the name, so `-eADMIN_PASSWORD` still
matched on the PASSWORD substring and was masked **by accident**, while `-eKEY` did not match and leaked.
The ticket's L01/L04/L05/L07 rows use the placeholder name `NAME`, which is not a secret name at all — so
"clear" in those rows is correct behaviour, not a leak.

**This changed what I built.** My first L03 row used `JWT_SECRET` and was **GREEN before the fix** — it would
have shipped as a regression row that pinned nothing. I caught it because the red-proof came back 2 red
instead of 3 and I read the pattern at source instead of assuming a flaky row. L03 now uses the literal name
`KEY`, which is the gate's own row, and the accident has its own cell so a later narrowing of the name pattern
cannot quietly turn it into a leak.

## NUMBERS
- `npm run test:unit`: **63 files / 1096 passed / 0 failed**, rc 0. BASE in this worktree before any edit:
  **63 / 1089 / 0**. +7 cells, no pre-existing red either side.
- `npm run lint`: **rc 0**, both tsconfigs plus eslint. First run was rc 1 — my extraction had left the big
  JSDoc attached to the wrong function. Fixed, and the tamper matrix was then RE-TAKEN on the shipped bytes.
- `npm run format:check`: rc 0. Load 4.60-5.52 across the runs, bare and serial, no timeout.

## RED PROOF — 6 arms, one per conjunct, restores sha256-asserted
- Rows added, fix absent -> **L02, L03, L08 red** (the three that actually leak).
- T-1 revert the fallthrough -> **exactly L02, L03, L08**.
- T-2 two-argument cluster narrowed to `-e` -> the `-Pe` row + the existing `R_cl2`.
- T-3 attached cluster narrowed to bare `-e` -> the `-diteN=V` row + `R_cla`, `R_cleq`.
- T-4 drop the `SECRET_ENV_NAME` test -> the two non-secret readability cells.
- T-5 drop `PASSWORD` from the pattern -> **the accident cell** (+5 others).
- T-6 treat every preceding `-flag` as an env flag -> **the `-l` non-env boundary cell, and only that one**.

**T-6 exists because I was wrong about T-4.** I labelled T-4 as the arm proving the declared non-env
boundary. It is not: T-4 tampers `maskEnvAssignment`, which is never *called* for a value behind `-l`, so the
cell stayed green and my label asserted something the arm did not do. The boundary lives in the **routing**.
I added T-6, and I corrected the label in the script rather than leaving a header that claims a proof it does
not perform.

## WHICH GATE RAN
Repo-root `systemTest/` push: **the 15-leg preflight did not run** (`.githooks/pre-push` gates on
`^Blockchain/Dev/`). 7 seconds, `[format-gate] 1 package(s) checked, 0 skipped, 0 failed`. The fleet STOP
count was **not executed** on this branch and nothing here quotes it.

## NOT COVERED
- **The masked NAME SET is unchanged.** QA-958-2 is Peter's decision; untouched, as briefed.
- **QA-961-3 is documented, not fixed** — a token docker or k6 REJECTS is printed verbatim by the tool's own
  error output through `stdio: 'inherit'`, bypassing this mask and the run-log tee. The structural fix is O-1
  (bare `-e NAME` + a `spawnSync` `env`), which changes how the runner passes secrets: out of this pass.
- No docker, no k6, no container, no environment. **Nothing deployed.** The gate's docker 28.4.0 / k6 1.6.1
  measurements are quoted as ITS findings, not re-measured — there is no docker run in this lane.
- `-l` carrying a secret-named value still prints in clear: the declared boundary, now pinned.
- `npm run knip` / `npm audit` not run.
- Latent by construction: no caller builds these argvs today, so the cells reach them through `extraFlags`.

## STATE
develop unchanged at `6e2a00bfed57`. `.push-lock-24` free — held 7 s, released, cool-off stamped. Shared
checkout: no pull, no fetch, no commit; only `worktree add` in my namespace (`s-l6-ks1117`, `s-l6-ks1111`).
0 orphaned `login_stub` pids. No container, no database, no port taken. Nothing deployed.

## WITH YOU NOW
- **#1243** KS-1117 + KS-1300 items 2-4, head `0c89e2b503d9` — tier 2.
- **#1244** KS-1111, head `146b620fda53` — tier 2.

## NEXT
Item 3 is **KS-1313** (#1241's residue, on a NEW PR from develop per your launch ruling). Per its brief I
capture real vitest 4.1.11 output FIRST across every summary shape — fail-only, skip-only, todo-only,
expected-fail, mixed, pass-only and the two-line case — enumerate the shapes I exclude and why, and run BOTH
tsconfigs. I will not touch #1241.
