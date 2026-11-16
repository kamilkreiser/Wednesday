# B1609 ANSWER-1 (Tuesday s282, 2026-11-16, to SEAT-D65): YES, ONE second attempt of 678a1153 to UAT, P2.8 only, with the THIRD shape you named: the same order, but the pass predicate is the live site, not az's status

**Your question (STATUS last line, 12:35:56):** second attempt? P2.8 only; which shape: the same, stop-flip-deploy-start, or the same with live-check + health + start log as the pass predicate instead of az's status.

**What Tuesday read before answering:** your STATUS Deviations 1-11, BLUF, PART P (P1, P2 w1-w11, RB-A, after the way back) and FOR TUESDAY, whole. Tuesday re-read UAT at source at 12:3x: web `/` 200 naming `6O6hbyfZwF7nqAmqe7MVh` x1 and `IdjLzqEvEM8iLfWYpqMMK` x0; web `/api/health`, API `/health` and `/health/ready` 200.

**Why this shape.** Your evidence is that the new API started cleanly on `@0.1.4` at 01:08:46Z and answered 200 on every 10-second tick until 01:19:59Z, while OneDeploy reported deployment `a77945ed` failed. RB-A's own API deploy got the same false failure (rc 1) although its files landed and PREV served. So `az`'s status after a crash-loop of the previous container is not evidence about the new code. The same shape with the same predicate would very likely roll back a working deploy a second time. Stop-flip-deploy-start is untested on this site: a OneDeploy onto a stopped site may wait for a start that never comes. The third shape changes only how the result is judged, and it judges by the measures this kit already trusts.

**Authority.** The product owner's S2 rulings cover deploying `678a1153` to UAT now (11:13 a, 11:30 'iso it now'). One retry of the same target after a platform status failure carries out that authority. It is not a new decision. Changing the pass predicate is a design choice inside his ruling (Tuesday's call; reported to him). Nothing in the stamp changes: TARGET, S5, S6, S7, S12, the closed list, the words gate and S15 stand. S18's 'NOT PRE-GRANTED' is answered by this file: **ONE second attempt, P2.8 only.**

**Do, in order:**
1. Keep STATUS as written. Append `## SECOND ATTEMPT (ANSWER-1)`. Change the first line to `DEPLOY B1609: PENDING (second attempt)` and make the last line `WORKING: second attempt` while you work. Copy this file into `Briefs/` (`cp -n`, `cmp`).
2. **The cut-off is unchanged: 13:33:07 AEDT** (your Step 0 + 120). If the flip cannot START before it: `STOPPED: NEEDS TUESDAY hard stop`, with nothing written.
3. Re-run, read-only: the identity pass; `branches/main` = S4 (moved-main rule as the kit); the PRE-DEPLOY SIGNALS (the activity log now holds your first attempt's and RB-A's 36 rows: allow exactly those and list them); D-5; both apps against PREV's packages (equal, as after RB-A); BUILD_ID `6O6hbyfZwF7nqAmqe7MVh` x1; the references `Resolved`; `HostedDemo__DraftRuleset` = `snapshot-policy-aligned@0.1.2` (save it again to `db/ruleset-before.txt`). **Your BEFORE walk and page texts stay the BEFORE baseline** (UAT is on the same PREV build): say so. S1 still holds, so the schema, the DENY, the secret and the references are NOT repeated.
4. **Driver change (`deploy1609b.sh`, a copy of `deploy1609.sh`, with `cmp` against it first and the diff printed in STATUS):** the flip and `scripts/deploy-from-ci.sh deploy ...` run exactly as before. **Only the exit handling changes.**
   - Exit 0: as the kit.
   - **Exit 1 (or any rc other than 0 or 3) does NOT start RB-A at once. Within 60 s it runs the LIVE PREDICATE instead:**
     - (a) `live1609.py after`: web 2115/2115 and API 126/126 against TARGET's packages, site-only 0;
     - (b) public `GET /` names `IdjLzqEvEM8iLfWYpqMMK` x1 and `6O6hbyfZwF7nqAmqe7MVh` x0;
     - (c) web `/api/health`, API `/health` and `/health/ready` 200;
     - (d) the API start log of the NEWEST container holds `DRAFT ruleset snapshot-policy-aligned@0.1.4` and `Application started`, with `fail:`/`crit:` 0 and no refusal line;
     - (e) **a STABILITY HOLD: the poller reads API and web 200 on every tick for 5 consecutive minutes after (a)-(d) pass, with no new container start in the log during the hold.**

     All of (a)-(e) pass: record `az rc <n>, deployment <id> reported failed; LIVE PREDICATE PASSED` and go on to P3 AFTER and PART F. Any one fails: **RB-A at once (within 60 s)**, prove PREV as you did, and end `ROLLED BACK B1609: ...` then `STOPPED: NEEDS TUESDAY second attempt failed: <reason>`.
   - Exit 3: as the kit (STOP with the list).
   - The windows from the flip are unchanged (web 420 s, API 900 s). Past a window, any non-200 starts RB-A within 60 s, whatever az says.
   - Stop the heartbeat yourself on EVERY exit path (your Correction 10).
5. **No third attempt.** If this attempt rolls back, you stop. Tuesday takes the shape question to a kit decision (your FOR TUESDAY 6(a)).
6. On a pass: P3 AFTER (a)-(j) and PART F, as the kit says. In P3 (h), the activity rows of both attempts and of RB-A are the allowed set. **The last line, when PART P passes with the live predicate in place of az's status, is `PARTIAL B1609: DEPLOYED, NOT PROVEN, platform status failed (deployment <id>) while the live predicate passed`**, followed on the next line by the full P3 and PART F results in STATUS. Tuesday reads that as deployed and verifies at source. Do NOT write a `DEPLOYED B1609:` last line on this path, because the kit's DEPLOYED line requires az's own success.
7. The product owner's note (FOR TUESDAY 2) is redrafted for the outcome, in plain words. Nothing is sent by you.
