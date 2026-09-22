SUBJECT: [Secuura/Blockchain-C -> Wednesday] READY FOR QA (Seat C 19th): PR 3 KS-1031 EXIT3
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-22T05:44:01.000Z
MESSAGE_ID: <010001a0c7a47dd3-7d35e82e-e650-4327-86fc-fc06abf7d21d-000000@email.amazonses.com>
CAPTURED: 2026-09-22T07:25:55Z by the gate19C (Seat C 19th twelve-PR) drafter, read-only by message id from wednesday-agent@ (key by name, never printed)
TEXT_SHA256: 6f63a538493d2fc747b2290386c13ddbf2025245d123a087e092869c8b6be73c
READY FOR QA (Seat C 19th): PR 3 KS-1031 EXIT3 — #1183 at head 03fab6783d5e1ad5893178027abc2291abeb627e (read from origin in the same action), branch
feature/ks-1031-gate-f-4-deploy-condition-apply-048-before-rolling-r16b-exit3-1, built on develop 3bad652d17cf111c1e2e1bed1ae7686894637487 (my commits' parent; tree cd9b0f6c7b84). Develop at origin at READY:
3bad652d17cf111c1e2e1bed1ae7686894637487 (UNMOVED).
Ticket(s): Refs KS-1031, linkKind contributes (attachmentsForURL read after the push and after the PR opened: KS-1031: post-push state=Backlog attachments=[] | post-PR state=In Progress attachments=[['1183', 'contributes', 'open']];
attachmentsForURL #1183 = #1183: [['KS-1031', 'contributes']] — exactly the own key set, contributes). Tier: tier 1 PROPOSED — SCRIPT bytes in tooling every start / push / deploy runs (nothing under services/ or packages/). PR 3 of 12 as tabled (push order 1 -> 12; my numbers interleave with Seat B 19th's).
Nothing merged, nothing deployed, no kintsugi step, no anchor, no rule-7 post, no ticket comment.

THE FIVE THINGS A READY IS
1. PR number: #1183. Title "KS-1031 EXIT3: run-migrations.sh exits 3 on a migration failure, never 0". Base develop. +116/-6, 2 file(s):
   Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh (+105/-0); Blockchain/Dev/scripts/run-migrations.sh (+11/-6). SCRIPT BYTES: `git diff --name-only 3bad652d1...03fab6783` = 2 path(s): ['Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh', 'Blockchain/Dev/scripts/run-migrations.sh'] — the script(s) ['Blockchain/Dev/scripts/run-migrations.sh'] + the NEW suite(s), EXACTLY the declared set; nothing under services/ or packages/: True.
2. Head SHA read from origin in the same action: 03fab6783d5e1ad5893178027abc2291abeb627e = commits.tsv = the PR's head. Head tree 4e1393f8a8e5aedb53d68b825ac975b909cc2199
   = item 0's PR-alone tree over 3bad652d1 (4e1393f8a8e5) -> EQUAL. Equality targets for the addendum: 2 (2 files, comma-separated — MG-2).
3. Ticket: KS-1031 Backlog at boot -> In Progress now (the linear[bot] walked it Backlog -> In Progress on the PR open; recorded, not moved back). Attachment: #1183 contributes. KS-1031 comments 0 (boot 0). No comment posted (you rule any ticket bytes). The seven UNASSIGNED own tickets were assigned to the board login at item 0 on your standing Q2 (assignment only).
4. Test Evidence block: in the PR body (touched / ran with RATIOS / preflight / NOT run / migrations+config = none), every evidence line quoted from raise/ks1031.log. Summary:
   - Host: this seat's macOS arm64 worktree s-c19-ks1031 at develop 3bad652d1 (npm ci --offline + packages/shared built — the in-hook preflight runs its shell suites INSIDE the pushing worktree), /bin/bash 3.2 as the checker ran it; no stack; a local postgres LISTENS on :5432 (a box fact, reported) — an lsof ESTABLISHED sampler at 250 ms around every run of mine read 0 hits.
   - Lane baseline measured FIRST, bare, in my own worktree at the tip (your Q7 / the 16th's Q11): run-shell-suites.sh standalone = 45 ok / 0 FAIL of 45 suites (rc 0, wall 666.7 s, sampler 1993 samples / 0 hits; raise/baseline-ks972-run-shell-suites.out). Lane instrument: the suites themselves + the in-hook leg-14 run at push; NO jest/vitest, NO tsc, NO connection census on this side (your Q7 04:27:09Z).
   - Stages: run_migrations_failure_exit_code.test.sh (script run-migrations.sh): B4 rc 1 / 2 FAIL / 3 pass -> B5 rc 0 / 0 FAIL / 5 pass; B6 1 sibling(s) ['ks949_main_seed_idempotence.test.sh'].
   - Tampers: no tamper (bash_patch): the script hunk IS the fix — the red is the NEW suite at the tip WITHOUT the hunk (== the checker's B4 FAIL/pass counts, rc != 0), green WITH it (== B5); both halves run here in the worktree, both blobs asserted, bash -n on both files.
   - Applied per SECTION with the checker's .diff.opts (the NEW suite, then the script; every blob + line count asserted; bash -n on both):
       --- stage 1031-EXIT3 (2026-09-22_ks1031-ornith35b-night): bash_patch script Blockchain/Dev/scripts/run-migrations.sh + NEW suite run_migrations_failure_exit_code.test.sh; run tip 8c2f7b3fd (develop 3bad652d1); sections s1 ae04617ec3fa419a (strict) s2 fdf6d090392ceb31 (strict); cat(s1,s2)==patch.diff
       checker B4 (rc, FAIL, pass) (1, 2, 3) | B5 pass 5 | B6 siblings 1
       apply 2026-09-22_ks1031-ornith35b-night/out.md.checker/section_2.diff sha256 fdf6d090392ceb31 (strict)
       strict --check rc 0 '' | with opts --check rc 0
       blob of run_migrations_failure_exit_code.test.sh after section 2 (the suite): c998bd7ed21d (GROUPING c998bd7ed21d) lines 105 (want 105) -> EQUAL
       bash -n run_migrations_failure_exit_code.test.sh rc=0
       apply 2026-09-22_ks1031-ornith35b-night/out.md.checker/section_1.diff sha256 ae04617ec3fa419a (strict)
       strict --check rc 0 '' | with opts --check rc 0
       blob of run-migrations.sh after section 1 (the script): 633e92de2308 (GROUPING 633e92de2308) lines 163 (want 163) -> EQUAL
       bash -n run-migrations.sh rc=0 (B5a)
       diff `-` lines: 6 (the READYs' `-` sum 6; new files add none)
       every file's final blob + line count == the GROUPING table (2 files: ['run_migrations_failure_exit_code.test.sh', 'run-migrations.sh'])
       bash -n Blockchain/Dev/scripts/run-migrations.sh rc=0 (final)
   - RED-FIRST (the suite alone at the tip: rc != 0 and EXACTLY the checker's B4 FAIL / pass counts) -> GREEN-AFTER (the script hunk in: rc 0, 0 FAIL, the B5 pass count); `bash <suite>` from the worktree root, 120 s budget, the checker's own counters:
       [1031-EXIT3-redfirst] bash Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh rc=1 fail_lines=2 pass_lines=3 load_error=0 timeout=0 tally=None cells=2 wall=0.9s
       red: a run in which 048 failed exited 0, not 3 (Summary: applied=1 failed=1)
       red: ERROR line present=NO, stale 'Exiting 0 so docker' present=YES
       RED-FIRST == the checker's B4 exactly (rc 1, 2 FAIL line(s), 3 pass line(s); the suite alone, the script untouched)
       [1031-EXIT3-greenafter] bash Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0 tally=None cells=0 wall=0.6s
       GREEN-AFTER == the checker's B5 (rc 0, 0 FAIL, 5 pass line(s))
   - B6 sibling suites that drive the script (grep -l of its basename in scripts/__tests__, minus the new suite), bare before and after, no NEW failure:
       siblings naming `run-migrations.sh` in Blockchain/Dev/scripts/__tests__ (minus the new suite): 1 (checker B6: 1) ['ks949_main_seed_idempotence.test.sh']
       sibling ks949_main_seed_idempotence.test.sh: before rc 0 FAIL 0 pass 27 -> after rc 0 FAIL 0 pass 27 -> no NEW failure
       B6: 1 sibling suite(s), no NEW failure (the checker's rule: no sibling's FAIL count grows)
   - Final tree + the port instrument:
       lsof -nP -iTCP:5432 -sTCP:LISTEN: 2 line(s) — a LISTENER on this box is a box fact (REPORTED), not my suite reaching it: ['postgres 974 kam_code [::1]:5432', 'postgres 974 kam_code 127.0.0.1:5432']
       [1031-EXIT3-final] bash Blockchain/Dev/scripts/__tests__/run_migrations_failure_exit_code.test.sh rc=0 fail_lines=0 pass_lines=5 load_error=0 timeout=0 tally=None cells=0 wall=0.7s
       every NEW suite of this PR green on the final tree: 1/1 (B5 counts [5])
       census: not instrumented (bash / docs lane; Q7); :5432 ESTABLISHED sampler hits over every run of this PR: 0 (must be 0); tampers: none (BLUF 6)
   - Pre-push: 0 head(s) named feature/ks-1031-gate-f-4-deploy-condition-apply-048-before-rolling-r16b-exit3-1 (must be 0; control develop: 1). In-hook preflight on this push: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed. (legs 3 4 8 — local stack not up; you can clear this by starting it.)` | shell suites: 46 passed, 0 failed (of 46) | push 05:34:30Z -> 05:40:20Z, push rc=0 — skips are not a pass. Push protocol: PROTOCOL-CLEAN — shape: first push: tracking ref added at origin's head 03fab6783d5e1ad5893178027abc2291abeb627e.
   - PUSH-WINDOW LOCK (.push-lock-19, the NORMAL path; lock19.sh = the 18th's proven MG-10 copy, 5/5 arms on a scratch path at item 0): `2026-09-22T05:34:29Z LOCK TAKEN by Secuura/Blockchain-C pid 36718 for feature/ks` -> `2026-09-22T05:40:26Z LOCK RELEASED by Secuura/Blockchain-C p`; waits on the other seat`s window: 4 poll(s); taken before snapshot, released after verify, in push19.sh itself. login_stub listeners after the push: stubs=4 remaining=0.
   - NOT run / NOT covered: the platform suites (Schemathesis / Akto / Playwright / k6 — no stack booted). The ticket(s) stay open (Refs). apply mode: STRICT on every section/canonical (strict tree == --recount tree, item 0). Linear's branchName carried the ARCHIVED `ks-754` — EXCISED on your Q6. Deploy-adjacent: nothing deploys, no image; the 048 hold line stands until you re-word it after the merge (Q-1031)
   - Migrations / config: none. Runtime images: none (scripts / docs only; nothing deploys).
5. NOT done, restated: no ticket comment; no merge; no deploy; nothing beyond the canonical unit(s) applied as stated.

ARCHIVED-TICKET READS (boot, before the first push, and at READY — UNCHANGED; 37 keys): KS-501 Done archived 2026-07-29; KS-480 Deployed to UAT archived 2026-09-14; KS-978 Deployed to UAT archived 2026-09-08; KS-721 Deployed to UAT archived 2026-09-05; KS-522 Done archived 2026-07-30; KS-726 Done archived 2026-09-14; KS-535 Done archived 2026-08-04; KS-867 Done archived 2026-09-13; KS-878 Done archived 2026-09-13; KS-914 Deployed to UAT archived 2026-09-14; KS-1238 Done archived 2026-09-19; KS-1282 Done archived 2026-09-20; KS-1062 Done archived 2026-09-13; KS-971 Done archived 2026-09-17; KS-1078 Done archived 2026-09-14; KS-921 Deployed to UAT archived 2026-09-08; KS-490 Deployed to UAT archived 2026-09-08; KS-597 Done archived 2026-09-17; KS-727 Deployed to UAT archived 2026-09-05; KS-764 Done archived 2026-09-14; KS-879 Deployed to UAT archived 2026-09-08; KS-1020 Done archived 2026-09-13; KS-835 Done archived 2026-09-14; KS-1270 Done archived 2026-09-20; KS-549 Done archived 2026-08-04; KS-733 Deployed to UAT archived 2026-09-08; KS-815 Deployed to UAT archived 2026-09-06; KS-1013 Done archived 2026-09-20; KS-1058 Done archived 2026-09-11; KS-1103 Done archived 2026-09-13; KS-666 Done archived 2026-08-29; KS-754 Done archived 2026-09-13; KS-926 Done archived 2026-09-14; KS-487 Done archived 2026-09-17; KS-386 Deployed to UAT archived 2026-09-08; KS-444 Done archived 2026-07-16; KS-1092 Done archived 2026-09-11.
SEAT B ATTACHMENT ATTRIBUTIONS (the four-condition guard by NAME, read from GitHub in the guard's own action; 1 so far this round): KS-730 #1182 head feature/ks-730-security-71-inline-handlers-still-return-errmessage-verbatim-r16b-ingest500-1 @ 8c413d782 by kksecura opened 2026-09-22T05:36:16Z -> ATTRIBUTED (c1-c4 hold) [live guard post-push at 05:40:31Z].
Live-but-foreign / content / HOLDS (14): KS-1213 In Progress; KS-932 In Progress; KS-1206 In Progress; KS-763 In Progress; KS-775 In Progress; KS-1230 In Progress; KS-1285 Done; KS-1175 In Progress; KS-1250 Backlog; KS-1280 Backlog; KS-692 Backlog; KS-1195 In Progress; KS-1265 In Progress; KS-910 In Progress — unchanged from boot. Seat B 19th's nine own keys (read only): KS-730 In Progress, 1 attachment(s); KS-1028 Backlog, 0 attachment(s); KS-1160 Backlog, 0 attachment(s); KS-1229 In Progress, 1 attachment(s); KS-629 Backlog, 0 attachment(s); KS-974 Backlog, 0 attachment(s); KS-976 Backlog, 0 attachment(s); KS-1164 Backlog, 0 attachment(s); KS-1179 In Progress, 1 attachment(s); NEW attachments since boot (Seat B 19th`s PRs, attributed by the guard): {'KS-730': ['1182']}.

BATCH (built before the pushes in worktrees/s-c19-batch, never pushed; all TWELVE): tree 5a8458a5697f7ee5b1800864b9f49347c8cbe34e = item 0's all-14 tree over 3bad652d1 (5a8458a5697f; fwd/rev/shuffle ONE sha); Start_Up/start-secuura.sh at the PAIR blob; suites on it: run-shell-suites.sh rc 0: 55 ok / 0 FAIL of 55 suites (45 baseline + 10 NEW); bash -n on the 8 touched scripts 8/8; the three doc files re-measured D4-D8 on the batch tree 3/3.

FOR THE GATE TO MEASURE: 21 paths across the 12 PRs, ONE same-file pair (Start_Up/start-secuura.sh: PR 1 + PR 2, both orders one tree eaa961172883, the PAIR blob 58cdd3dc846b / 736), 2 lanes (scripts: bash; docs: no runner); 0 overlap with Seat B 19th's partition (packages/shared, services/kyc, services/originate, services/security, systemTest/performance) — measured at item 0 (boot/measure19.py); every PR's `git diff --name-only` == its declared files exactly; the script paths and fix shapes as in the PR bodies; the branchName excisions (ks-666 / ks-754 / ks-926, all archived) and the scanner result (own key only 12/12 names + 12/12 subjects); the KS-1047 subject re-worded to the bytes on your Q-1047b.
Records: 5_Project_History/2026-09-22_seatC-19th/ (raise/ks1031.log, raise/KS-1031-push*.out, raise/ks1031-body.md, raise/baseline.json, boot/measure19.out, boot/tickets_ready-3.json).

