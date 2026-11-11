# o157 report (KS-1873, Secuura/Blockchain, Spark operator) — filed by Wednesday from the operator's returned text (its Write was refused), 2026-11-12 ~06:5x AEDT

ROUND NOT RUN: harness refused the brief at build (blank context lines). Counter untouched. No held READY.

RULING (quoted from the commission): "the log line(s) carry the USER ID, never the email. No hashing, no partial mask. If the user id is not in scope at that line, STOP... If the logger already redacts an `email` field before it is written (measure it...), STOP: the ticket is already satisfied."

1. Tunnel + pin PASS (tunnel UP; ls-remote develop c78c80bd537015674fa5e22701d745946f94d4fb).
2. SATISFIED by the ruling: `user.id` (crypto.randomUUID(), same handler) in scope at users.ts:678.
3. Re-measure PASS. :678 `logger.info('Admin created user', { email, role: user.role, createdBy: req.user!.userId });`. Redaction ABSENT: auth logger.ts has only errors + timestamp formats; redact/censor grep over services/auth/src 0; a scratch run of the pinned winston logger printed the probe email verbatim in prod (json) and dev format. Census: 244 logger calls (paren-matched, control :678 fires); raw-email sites 9: users.ts:678; auth.ts:291 (dev-only SMTP link); userRepo.ts:1753,1764,1773,1796,1842,1865,1867 (demo seeds). All others maskEmail/hashEmail; users.ts:330 callerEmail is masked at :309. Only :678 is KS-1873's handler.
4. Exclusions PASS. 94 open PRs (GraphQL; control PR 2125 fired). PR 2075 is the only open PR on users.ts; its own diff (merge-base..head) is one hunk near :835 (the PATCH handler log line + a roleChanged check), not :678: waiver proposed. No PR on the baseline json. 432 READYs: 4 name users.ts (KS-1018, 1407, 1507, 1653), none contains "admin created user" (-i), none names KS-1873. KS-2125 guard count users.ts by the guard's own rule on a git archive: 9 before and 9 after the edit.

BRIEF (unrun): scratch/brief_unrun/ks_1873_o157_p1_admin_create_logs_user_id/ (KS-1873.md, golden.diff, spark.pins). One edit point at :678 `{ email, role...` -> `{ userId: user.id, role...`; new test `ks1873-admin-create-user-logs-the-user-id-not-the-email.test.ts` (real router, recording logger): R1 (no logged text contains the email), R2 (create line meta.userId equals the returned id) red at the pin; C0 (create line recorded), C1 (a planted email is detectable).

BLOCK: `round.sh --dry-run` refused: blank context lines (677, 679 around :678); a six-line remove/re-add is refused as identical -/+ lines. Only route past is `ALLOW_BLANK_CONTEXT=1` (the lint says the model drops the blanks). Not self-granted for a model round.

EVIDENCE the golden is sound: `ALLOW_BLANK_CONTEXT=1 round.sh --control` (no model call) = CONTROL-PASS, checker 7/7, R1+R2 red-first, golden byte-identical. Run dir: 2_Project_Files/local-model/runs/spark_secuura_2026-11-12_ks_1873_o157_p1_admin_create_logs_user_id-control.

ROUTE proposed: authorise the one-run override and queue (original + one rebrief), or a Claude seat with the golden; tier-1 auth file -> TIER-1 Opus gate either way. The other 8 raw-email sites: separate cards/tickets.

WEDNESDAY'S DISPOSITION (06:5x): override GRANTED for this ticket's rounds (o158): the checker's byte-identical added-lines clause fails loudly if the model drops a blank, so the risk is one spent round, not a silent pass. The 8 other sites go to S 63rd as a filing (demo seeds + a dev-only SMTP link are likely Low; S 63rd measures and files ONE ticket).
