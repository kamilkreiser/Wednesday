# Spark operator 105 report (2026-11-09 00:2x-00:50 AEDT). Secuura only.

## BLUF
- Job 1: 881 READY_*.diff.md measured at develop 7eda23b3 (unmoved at start; moved to 092d3070 by 00:38, PR 2061). 621 moved (quarantine = MOVE, WHY rows written): 258 spent, 363 stale. 156 FWD-OK left in place, 104 (59 NEITHER + 45 REV-OK) left because an open PR lists their files. No HOLD-NOTE file sat beside any READY.
- Job 2: 1 HELD (target 3; pool exhausted under the rules, counts below). KS-2099 item 1 (Wednesday's priority) is briefed and lints, but the builder REFUSES it: ticket attached to OPEN PR 2094.
- Correction made mid-run: operator 104's instrument (strict git apply) misclassifies a hunk with leading context and none after as NEITHER ("must match at end of file"). I added a --unidiff-zero retry and RESTORED 4 READYs I had wrongly moved (KS-1240-p6, O84-P2, O89-P6, O90-P3); 2 more moved stale -> spent (O50-P1/P2). Backup of WHY before my section: WHY.before_op105_sweep_backup.md.

## Job 1 count table (final)
| class | n | action |
|---|---|---|
| REV-OK (in tip) | 258 | moved to night/_quarantine_2026-11-09/spent/ |
| NEITHER (drifted/partial) | 347 | moved to stale/ |
| NODIFF (no fence, canonical patch gone) | 16 | moved to stale/ |
| FWD-OK | 156 (incl. 4 restored) | left |
| NEITHER / REV-OK named by an open PR or live seat queue | 59 / 45 | left |
Conservation: night READY .diff.md 881 -> 260 (+1 new O105-P1 = 261); spent 258 + stale 363 = 621 moved. Full WHY rows (file, class, landing sha+subject for spent via git log -S, ticket state and owed-ness for stale): night/_quarantine_2026-11-09/WHY.md under "Operator 105 sweep" (258 + 363 rows) plus an addendum of rows I verified at source. Instrument: gen/ready_all_v2.py, results ready_all_v2.json, ready_all.tsv (strict-only first pass).
Stale by ticket state: Done/Canceled/none = not owed; 129 open-ticket rows labelled by a heuristic (new test file present at tip => landed in another form). Verified at source: KS-864, KS-1346 (gdpr/systemErrors), KS-1456, KS-1387, KS-1868-O36-P2 landed; KS-629-B owed but not Spark-shaped.

## Job 2
Held (ls night | grep O105):
READY_KS-1868-KS-1868-O105-P1_spark-dsv4flash_BRIEFED-CODEPATCH2-EMAIL-PASS-7of7_2026-11-09.diff.md
hold_ready line: `golden: BYTE-IDENTICAL; touched=2 product_plus=24 product_minus=3 red=5/8 green=8/8 suite=2592->2600 strict=True` (hold_O105-P1.out), tip 092d30706b95.
- What: ROUND 2 of 2 rebrief of stale KS-1868-O91-P11 (originate services/email.ts: the ACS init, ACS send and SMTP send catches read `.message` unguarded). Drifted because KS-1937 (90b500e19) removed the recipient from those log lines; the fix was still owed. Brief: night/briefs/ks_1868_o105_p1_*; generator gen/mkbrief1.py.
- NOT covered: the other catches/WARN lines of email.ts; behaviour change is only for unreadable/non-string messages. Recommended tier 2 (outbound-mail path, log-only).
- OVERLAP: edits the same SMTP catch (line 210) as KS-2099 item 1 below; raise one after the other.

KS-2099 item 1 (Wednesday's priority): NOT RUN. Brief and golden prepared (night/briefs/ks_2099_o105_p2_originate_email_smtp_failure_log_redacts_echoed_recipient/, gen/mkbrief3.py): one hunk replaces `error.message` with `String(error.message).replace(<address-shaped token>, '[address]')`, new test file with controls C1/C2, red cells E10 (angle-bracket echo) and E11 (nodemailer `Invalid recipient "addr"`), E12 green; ids do not collide with PR 2094's E8/E9. brief_lint rc 0 (lint_p3.out). dry-run REFUSED by build_input.sh:219 "attached to OPEN pull request(s) ['#2094']" (a ticket-level lane guard; PR 2094 is test-only item 3, but the guard is per ticket and `supersedes=` does not apply). I did not bypass or edit the tool. Runnable the moment PR 2094 merges or closes: `round.sh <brief> --dry-run`, then control, then model. Also briefable only after P1 is raised or accepted as an overlap. email.ts is in no open PR (planted-control scans: 43 PRs, 304-311 files, control services/originate 7-9 entries, email.ts hits 0).

Listed for a Claude seat (not briefed, reason): KS-2099 item 2 (thirdPartyVerifiers.ts, not asked); KS-629 Part B (generated openapi yaml + spec decision); KS-1701 (platform-role check, authorization surface); KS-1087, KS-1233 (behaviour/decision-shaped); KS-1868 O84-P2 / O89-P6 issuerCertSweep and O85-P3/P5 (auth service, credential/security surface; O84-P2/O89-P6 are still FWD-OK held in night/); KS-1490 (102-file dead-host sweep, decision/docs); KS-2022 accountLockout (excluded, T 15th).

## Round log (done.md row times)
- 00:33:14 CONTROL-PASS ks_1868_o105_p1 (124 s, BYTE-IDENTICAL)
- 00:41:21 PASS ks_1868_o105_p1 (round 178 s, model 73.246 s, 18532+3033 tok, BYTE-IDENTICAL, PASS 7/7)

## Limits record
Pin: 7eda23b3 start (tip_start.out, ls-remote) -> 092d3070 from ~00:38 (tip_r3.out, tip_end.out); model round ran at 092d3070 and passed strict apply there. Open PRs: 42/310 start (control 7), 43/311, 43/304 end (control 9). Disk 21-22 GiB throughout (disk_start/end.out). Load1 4-6. No queue.sh left running; queue.md has only comment lines. No push/PR/ticket/mail; nothing under !CODING written; nothing deleted (the unused O105-P2 certifications brief was moved to _quarantine_2026-11-09/briefs_unused/).

## UNMEASURED
- "Still owed?" for ~120 open-ticket stale rows beyond the ones named (heuristic only).
- NODIFF rows (16): not measurable (canonical patch files gone).
- Whether the 59+45 PR-named READYs are in fact those PRs' own patches (left in place by rule).
- KS-2099 item 1 patch: golden never run through the checker (refused before control).
- Held P1 raise: tier-2 gate not run; replacement prose/guard is the established house pattern.
