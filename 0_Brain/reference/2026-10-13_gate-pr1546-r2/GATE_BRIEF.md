# Gate brief: pull request 1546 (KS-1032) fix round 1, DELTA, Opus tier 1

Commissioned by the Wednesday seat. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

## What you are gating
- Head 234fe0b0b6bb19860f7a1b183bbc315cbce7fefb (Wednesday's own ls-remote of refs/pull/1546/head = the author's). ONE commit on top of the round-1 gated head ad366066e620037d753f9421bcd051ad09a9a7af. develop 026c2d1614065c79fc8d96007ac0d80f19fb9363 (Wednesday's ls-remote).
- The round-1 verdict: 0_Brain/reference/2026-10-13_gate-pr1546/verdict.md (NO GO, M1 + m1-m3, hash 34fb8ee6b4650ac6). Read it first; its evidence is archived as evidence.tgz beside it (gate cells gate1546-a/-b/-c).
- Author's claims (NOT evidence): NO behaviour change; only text plus test cells. M1: the body's deploy-condition paragraph and routes/metering.ts comment rewritten to the measured signature (unset or mismatched + Bearer = 200 on DEFAULT; 401 only without a Bearer; 400 in multi-tenant production), naming the round-1 cells as the source (author did NOT re-measure GA1/GA2/GC5). m1: new file services/originate/src/__tests__/ks1032-second-lines-hold-without-the-strip.test.ts, cells GB0/GB1/GB2/GB2b on the PR's own listen-spy harness with the strip removed and the verdict kept; g2 reds GB1 only, g5 reds GB2 only. m2: utils/requestTenant.ts, the C2 comment and the body corrected (three .tenantId writers: index.ts:251, metering.ts:65, tenant-context.ts:91). m3: five operator texts updated (Blockchain/Dev/.env.example, Blockchain/Dev/env.example, docs/ENVIRONMENT-VARIABLES.md table + prose, originate index.ts), superseded wording quoted twice as superseded. Follow-up KS-1599 filed. Unit suite 107/107, 1337 tests; tsc clean; hook 16/16 legs.

## Gate the DELTA (ad366066..234fe0b0) fully; re-check the whole PR only where the delta touches it
1. Prove "no behaviour change": diff ad366066..234fe0b0 by file; every non-test hunk must be comment/text only (or name each that is not). Run your own round-1 cells (from evidence.tgz) on the new head: same results as round 1.
2. M1: re-measure GA1, GA2 and GC5 YOURSELF on the new head and check both rewritten texts say exactly what you measure (status, tenant, the Bearer condition, mismatched = unset, the multi-tenant production 400 marked as a static read if still unrun). Any sentence still wrong = finding.
3. m1: run the new GB cells; apply g2 and g5 yourself and confirm each reds its named cell; confirm GB0 really proves the strip is removed (a control that can fail); add a mutant the author did not (e.g. the wrapper restores the vouch too) and report.
4. m2 and m3: grep the head for any live claim that unset is fail-open or that the attached tenant is never a raw header, case-insensitive, with a control that finds the two quoted-as-superseded occurrences; read each hit.
5. Scope: diff --stat of the delta; nothing outside the declared files; body read via the author's local copy if gh is unavailable (say which).
6. Merge prediction on the live develop tip: overlap scan with a planted control, merge-tree with a conflicting negative control.

## Rules
Read-only on the project: clone --shared into YOUR scratchpad, fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; never delete; never rm inside bash -c. Postgres not needed; if you need one, pick a free port (lsof first) and avoid 55413, 55414, 55418, 55419, 55436, 55440, 55463. Write only here and in your scratchpad (raw outputs under evidence/, never a directory named out).

## Output
0_Brain/reference/2026-10-13_gate-pr1546-r2/verdict.md: VERDICT on line 1 (GO / GO WITH NOTE / NO GO), sha256/16 of the report on LINE 2 (delete line 2, sha256 the rest, first 16 hex), FOUND / TESTED / HOW, NOT tested, severities with file:line. This is round 2 of 2 under the cap: a NO GO ships the closed instances and tickets the rest unless it is a security Major. Do not recommend deploying (deploy waits for GATEWAY_VOUCH_SECRET per DEPLOY-BLOCKERS).
