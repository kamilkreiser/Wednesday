SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation
TS: 2026-09-17T09:46:39.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
Seat A 6th successor is up (bare pane `Secuura/Blockchain`, launched 19:41:16 AEST = 09:41:16Z). Every ref, local head, worktree and source line in your brief re-reads the same. Your 09:45:00Z ANSWER (#1026 pre-gate fix round, spf/dkim/dmarc pass) is folded in and supersedes brief item 2. I run #1018's round 2 first, then #1026's round 2, then the rest of the queue in your order. Nothing is written to a branch, a ticket or the vault until your ANSWER.

## Recommendation
Please ANSWER with the queue confirmed or changed. Four build choices have a default I follow if you confirm without comment:
1. **#1018 tamper translations** (the guard now lives in the helper, not in users.ts):
   - TN: two rows. TN-a is `if (false && !updated)` inside `updateUserOrThrow` (`userRepo.ts`), with other-suite reds expected and named. TN-b is the call site put back to a bare `updateUser(...)` with no guard.
   - TS: the helper's thrown error re-statused so it no longer answers 503. The exact form is chosen at build so tsc stays 0, and reported.
   - G-NULLONLY: `updateUser` + `if (updated === null) throw new ServiceUnavailableError(<the same message>)`. `ServiceUnavailableError` is already imported, so null-vs-falsy is the only property changed and the row cannot go VOID. If no cell reds, I add the cell that does (the undefined read-back arm) and name it.
   - G-MSG: the label `'Profile update'` reworded. The message cell must red.
2. **#1026 splitter:** `parseScopeString` is in the SAME file, `services/oauth.ts:357` (`scope.split(/[\s,]+/).filter(s => s.length > 0)`), directly under `validateScopes` at `:352-355`. So it is callable at `:353` with no import and no layering change. Default: `:353` becomes "if any entry of `allowed`, split by `parseScopeString`, is `'*'`, return `[]`"; `:354` is byte-unchanged; no second regex.
3. **Worktree:** I switch my own `worktrees/raise-0916-a` (porcelain 0) from the KS-839 branch to the KS-1050 branch for item 1, then back for item 2. Both branch heads equal origin, so nothing is lost.
4. **KS-1050 comment `413d3b05`:** I say in the READY whether a correction should follow, and post nothing unasked.

## Detail

### Launcher warnings at boot, verbatim
The preflight file's `# launch 2026-09-17T09:41:16Z` = my own start (`ps -o lstart= -p $PPID`: Thu 17 Sep 19:41:16), so these are mine.
```
[F-02] No SSH identity available for git (keychain not seeded, on-disk fallback off).
       Run: ssh-add --apple-use-keychain ~/.ssh/secuura_blockchain_deploy_rw
       Or temporarily: export SECUURA_ALLOW_ONDISK_KEY=1 before launching.
       (git will use whatever core.sshCommand is already in the repo config.)
[KS-907] 2 other live session(s) on this project: PID 35278 (up since Thu 17 Sep 17:01:36 2026), PID 73954 (live claude session on this project).
         The boot git-sync is READ-ONLY this launch — it will NOT pull in 2_Project_Files.
```
- F-02: the repo's `core.sshCommand` key fetched and ls-remoted rc 0.
- KS-907, measured: PID 35278 = Seat B (cwd `Secuura/Blockchain`, 17:01:36). **PID 73954 is not a project seat.** Its cwd is `Testing Agent MAIN`, it started 19:40:27, and its argv opens "You are the fleet QA agent running a TIER 2 … gate, ROUND 1, on … PR #1025 (KS-528, Seat B)". The launcher counts a QA gate whose prompt names the project as a live session. That is a launcher attribution defect, for you to route; I have not touched it.

### ITEM 0 verification (all equal to the brief)
- **Refs** (`git ls-remote origin`, rc 0): develop `efaaa6034f036dd9538ee35b189217b1d08b90a9`; pull/1018 `267bd8624ce276ca62160216d042b8477bac52f1`; pull/1026 `8ab493354bbdb3fa52d2eb14654492db1a891e4a`; pull/1025 `9954a7069a16987da140654337555c9a13268b1f`; pull/922 `e60a24c5024d0adae3fae8966bbd4e243e8b581c`. develop has not moved since the brief.
- **Local heads** (`git log -1 --format='%H %P'`), each = the table: KS-744 `fb503741a` (`6252f06ac` + `81ee4b729`); KS-1180-P1 `7553821fc` (`a4dc0d8ee` + `81ee4b729`); KS-1194 `29d9f90fa` (`00236c10b` + `81ee4b729`). Branches pointing at `267bd8624` and `8ab493354` = the KS-1050 and KS-839 branches.
- **Worktree** `raise-0916-a`: KS-839 branch @ `8ab493354`, porcelain 0.
- **#1018 source lines:** `users.ts:934` @ `267bd8624` = `const updated = await userRepo.updateUser(user.id, updates);`; `:937` = the `AppError(… 500, 'PROFILE_UPDATE_NOT_PERSISTED')`; `:16` imports `AppError`, whose only other use is `:937`, so the import goes. `userRepo.ts:960` @ `efaaa6034` = `export async function updateUserOrThrow(`, which throws `ServiceUnavailableError` "`${operation}` could not be confirmed. Please retry — if you already succeeded, you may not need to." `ks1052-backup-code-burn-cause-a.test.ts` is present at develop. `git diff --stat 7e89318bc efaaa6034 -- services/auth` is empty.
- **`DRAFTER_REPORT.md` (gate1018)** read whole: the T0/TN/TS/TI rows (0/2/1/0), G-MSG 0 reds, G-NULLONLY 0 reds, PROBE-ORTHROW VOID on TS6133.
- **linkKinds** (`attachmentsForURL`): #922 [KS-679 closes]; #1018 [KS-1050 contributes]; #1026 [KS-839 contributes]; control pull/99999 [].
- **Your brief and ANSWER:** both from wednesday-agent@, spf/dkim/dmarc pass (structured and raw), read whole.
- **v1.3 grant** re-verified at source: `<096604C5-237F-4467-9ECF-B79F975FCB11@me.com>`, "Team collaboration", structured field null, raw Authentication-Results spf=pass / envelope-from=kreiser.org@me.com / dkim=pass header.i=@me.com / dmarc=pass header.from=me.com, each checked alone. Five controls (spf-fail, other envelope-from, other dkim domain, dmarc-fail, empty) each fail.

### Queue (your order, with your 09:45:00Z ANSWER; every write gated on the previous rc; at most 3 open PRs of this lineage)
1. **#1018 round 2** (tier 2): develop `efaaa6034` merged in (no rebase), then the `updateUserOrThrow(user.id, updates, 'Profile update')` fix with the `AppError` import dropped. The ks1050 harness is rebuilt on the ks1052 real-repo-over-db-stub pattern, with 🔴 503 + message + no "not applied/matched no row/did not persist" wording, 🔴 never `success: true`, and a rowCount 1 control. Red-proof at the base (200) and at the round-1 head (500). Tampers T0/TN-a/TN-b/TS/TI/G-MSG/G-NULLONLY, each with the whole auth suite and denominator asserted, tsc per row (VOID ≠ red) and sha256 restore. Then push to the same PR, post-push checks (stubs by verified pid, linkKinds), and READY FOR QA (round 2 delta). `Refs KS-1050`.
2. **#1026 round 2** (tier 1): develop merged in, the `parseScopeString` fix at `:353`, the 8 padded carriers 🔴 (scope omitted grants nothing; scope named refused), 🟢 zero-width-space `*` / fullwidth `*` literal, explicit / empty / `documents:*` unchanged. Red-proof at develop AND at `8ab493354`. Tampers = the six round-1 rows + G-TRIMSTAR reversed. Push, checks, READY (round 2 delta). KS-1210 and the `documents:*` Record are not widened into.
3. **KS-744** (tier 1): develop merged in, a real merge on `middleware/auth.ts` resolved by content (STOP and ask if unclear), api-gateway + tsc, push when the cap allows, READY. KS-1208 named, not widened.
4. **KS-1180-P1** (tier 2, test-only), 5. **KS-1194** (merge waits for Kam's tap, after #1018; merge-tree re-run against #1018's final head), 6. **KS-1213** local build, write-side refuse, measure each writer first, 7. **KS-1215** shape QUESTION only, 8. **KS-805** + the KS-839 contract sentence after #922 (still OPEN).
- The slot rule moves with the ANSWER: #1018 and #1026 both stay open through their round 2, so KS-744 is still the third slot and pushes only after #1026's round-2 READY. Default: I hold KS-744's push until then, unless you say it goes after #1018's READY as the brief had it.

### Boot sweep (launcher steps)
- **Git:** main checkout `feature/ks-597-b-caller-scoped-externalref` @ `355d82c8b`, porcelain 0, no upstream, fetch rc 0, not switched. No pull (KS-907).
- **Linear:** 79 active on the board account (In Progress 42, Todo 23, In Review 12, Blocked 2); 92 team-wide; 0 overdue. Backlog 300 (Urgent 1, High 75, Medium 156, Low 62, None 6). Completed <24h: KS-1130, KS-810, KS-793. PS assigned: 0. Non-board comments <24h: 1 (Stuart, KS-1175, 09-16 10:36Z, pre-existing). Queue tickets: KS-1050 / KS-839 In Progress; KS-744, KS-1180, KS-1194, KS-1213, KS-1215, KS-805, KS-1208 Backlog; none archived.
- **GitHub:** 21 open PRs (kksecura 11, dependabot 10). Reviews endpoint: 0 at-head approvals, 0 at-head changes requested, 21 none. Search index: approved 1 + changes_requested 1 + none 19 = 21. The two index hits are stale reviews (#927 APPROVED at `63e955e0f` ≠ head `1041d2d32`; #887 CHANGES_REQUESTED at `bb0502c80` ≠ head `3aee3deed`).
- **Extranet:** 6 tasks / 0 replies / 1 doc (tasks dated 08-07 to 08-29, doc 09-10), all pre-existing. `/api/seen` NOT called.
- **BACKLOG.md** on origin/develop: 33 open.
- **Fuse dates at develop:** `lock-discovery.mjs:209` `expires: '2026-10-19'`. `audit-baseline.json` has 17 `expires` fields, 0 on or before 2026-09-18, earliest 2026-09-24 ×6 (Seat B's lane).
- **Mail:** since the 5th's wrap, only your brief (09:41:10Z) and ANSWER (09:45:00Z) are Seat A's. Inbox key scoped: own inbox 200, coagent@ 404, inbox count 1.
- **Processes:** 0 `login_stub.mjs` (control: 1088 ps rows, 12 with `node`).
- **Usage:** `fleet/USAGE_STOP` reads 90.

### Declined launcher lines, as before
CC to Kam; extranet to-dos and @-mentions to Peter/Stuart; `POST /api/seen` (the SessionStart hook still instructs it); the rule-7 Azure deploy (your hold).

### Holds acknowledged
No deploy / kintsugi / demo / stack / az; nothing to Peter or Stuart; ticket comments are the only client-facing channel, BLUF, no @-mentions; no `.github/workflows`; no force / `--no-verify` / `--admin`; never approve my own PR; own worktree only; shared checkout and `.git/config` untouched; never delete (quarantine by move); login stubs ended by verified pid only, never Seat B's (`raise-0917-b-audit`); a GO is only a signed mail, and a prompt tap is only a pointer to one (your 09:45 tap was read as that); Seat B's package.json/lock files are not mine; usage cut 90; at 80% context finish the step, hand over with FINAL STATE, wrap. Records: `5_Project_History/2026-09-17_seatA-6th/`.

