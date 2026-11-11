# o158 report (KS-1873, Secuura/Blockchain, Spark operator, claude-sonnet-5-5), 2026-11-12 ~07:0x AEDT

RESULT: PASS on round 1 (original brief, no rebrief). HELD. Counter 1 of 2.

Override: ALLOW_BLANK_CONTEXT=1 (granted by the o158 commission, KS-1873 only). Clause confirmed first:
- override at night/build_input.sh:792; byte-identity clause = A3x, tasks/code_patch2/checker.sh:230 (brief_bytes.py), tier code_patch2. It fired: "A3x ... byte-identical ... diff=0".

1. Re-pin: tunnel 200; develop = c78c80bd537015674fa5e22701d745946f94d4fb (unchanged).
2. Round: runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id; checker 7/7 + A2a; golden BYTE-IDENTICAL; 206s (72.9s model).
   A4 red 2 of 4 (R1,R2; controls C0,C1 green); A5 green 4/4; A6 suite 1839->1843 no new red; A7 tsc rc 0.
3. Source read of every +/- line: one product change users.ts:678
   - `{ email, role: user.role, createdBy: ... }`  ->  `{ userId: user.id, role: user.role, createdBy: ... }`
   plus the new 133-line test ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts. Equals golden.diff; ruling honoured (id, no hash/mask).
4. HELD by hold_ready.py (strict apply ok, strict=True). READY:
   /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_KS-1873-KS-1873-1_spark-dsv4flash_BRIEFED-CODEPATCH2-USERS-PASS-7of7_2026-11-12.diff.md
   (Held twice: DevMASTER unmounted briefly mid-session and the first READY write did not survive the remount; re-held, file confirmed present.)
5. Brief MOVED to this folder's brief_spent/; night/briefs holds no copy.

TIER NOTE: users.ts is an auth file -> TIER-1 Opus gate on the PR (routing v1.0 rule 4).
Carry-forward (o157): PR 2075 waiver proposed; KS-2125 users.ts guard count 9 before/after; 8 other raw-email sites to S 63rd.
No push, PR, board, Linear write or mail.
