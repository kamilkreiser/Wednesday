matches 1
subject: [Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation
timestamp: 2026-09-16T21:55:36.000Z
auth: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
Seat A third successor is up (bare pane `Secuura/Blockchain`, launched 07:47:00 AEST = 21:47:00Z). Every state line in your brief re-reads the same at source. Kam's three rulings are on their tickets. The 84 orphan listeners are all one test stub, leaked 4 per push by a subshell in `bootstrap_login_diagnosis.test.sh`; none stopped. GO #1016 is signed and in my inbox, so I merge it next, after this mail, per ITEM 1.

## Recommendation
Please ANSWER with:
1. **The orphan stubs:** may I stop them, and how? My proposal: SIGTERM each of the 84 by pid, only after re-reading that pid's command = `login_stub.mjs`, cwd = `raise-0916-a/Blockchain/Dev` and ppid = 1. After each of my own pushes, stop the 4 that push created, identified the same way. The leak itself is in `systemTest/`, outside my partition: do you route the ticket, or do I file it (searched first, not built)?
2. **The queue below:** confirmed or changed.
KS-1195's shape and file census follow in a separate QUESTION before any build, as QUEUE item 3 allows.

## Detail

### State as I re-read it
- **Refs** (`git ls-remote origin`, 21:50:54Z, rc 0): develop `eb1051fd39fe3edab4e0b1d1967515b758d4ba3f`; `refs/pull/1014/head` `9ba0caf78b8ddb737541df38303b776c982521d2`; `refs/pull/1016/head` `a226d94fe8c6fbfecb81de415feb645302cdd166`. All = brief.
- **GitHub REST, ~21:51Z:**
  - 20 open PRs. Files checked against index.ts, middleware/auth.ts, middleware/rateLimitEnforce.ts, routes/verification.ts, services/enforcement.ts, routes/proxy.ts, auth routes/users.ts, services/health.ts, routes/system-status.ts, routes/health-dashboard.ts. Only #1016 (verification.ts) and #1014 (verification.ts + enforcement.ts) hit any: that is the positive control.
  - #1014: 3 files, 0 reviews. #1016: 2 files, 0 reviews.
  - `/rules/branches/develop` pull_request required approvals: 0.
- **linkKinds** (`attachmentsForURL`): #1014 = [KS-1176 contributes, In Progress]; #1016 = [KS-1072 contributes, In Progress]; control pull/99999 = [].
- **Tickets:** KS-1072 In Progress (Low, 1 comment) · KS-1176 In Progress (2, last 21:25:09Z) · KS-1195 Backlog High · KS-1187 Backlog Urgent · KS-1194 Backlog High · KS-1180 Backlog Medium, 0 comments · KS-1050 / KS-1101 Backlog Medium · KS-1196 / KS-1197 Low, KS-1198 Medium · KS-1188..KS-1193 Backlog · the §5f nine all In Progress. (KS-1195/1187/1194 read 0 comments before the three below.)
- **GO list in `secuura-blockchain@`:** GO #1016 21:38:53Z present; GO #1014 absent; control GO #1015 21:11:13Z present (also GO #1011, #1013, #1012).
- **The v1.3 grant** was re-verified at source: Message-ID `<096604C5-237F-4467-9ECF-B79F975FCB11@me.com>`, 15 pages / 2959 messages paged. On the raw header: spf=pass, envelope-from=kreiser.org@me.com, dkim=pass header.i=@me.com, dmarc=pass header.from=me.com, each checked alone. Controls: your brief's header fails the three me.com checks; empty fails all four.
- **Worktree** `raise-0916-a`: `feature/ks-1176-connector-key-level-ranks-as-none` @ `9ba0caf78`, porcelain 0. Shared `.git/config` sha at boot: `0c7e6ce57e16e99724706efc86201d54f531a0fe`.
- **Shared checkout** `2_Project_Files`: `feature/ks-597-b-caller-scoped-externalref` @ `355d82c8b`, porcelain 0, equal to its origin branch, an ancestor of develop, not switched.
  - **One boot-sync action to report:** the launcher's git step fast-forwarded LOCAL `develop` `79432c797` → `eb1051fd3` with `git fetch origin develop:develop`. That is ref-only: no checkout, no working-tree change. Your brief read local develop as stale at `79432c797`; it now equals origin.

### The three ruling comments (ITEM 0 step 3; each gated on the previous rc, read back with anchors)
- KS-1195 `59804302-7645-40da-84dc-e3bbbdd1693e` (fix-now, 07:40:11 AEST), anchors 4/4.
- KS-1187 `5cc0725e-fc30-488f-8848-2e8a5a9c5bab` (wait, 07:40:23 AEST). Ruling only: no spellings, no mechanism, no mentions. Anchors 4/4.
- KS-1194 `05e914f9-df7a-4c61-87f1-01104b1a788f` (fail-closed, 07:50:34 AEST, per your RULED mail 21:51:25Z), anchors 5/5.

### Node-listener census (read-only; nothing stopped)
- **Instruments:** `lsof -nP -iTCP -sTCP:LISTEN` at 21:49Z (100 LISTEN sockets, 84 node); per pid `lsof -a -p <pid> -d cwd -Fn` and `ps -o pid=,ppid=,etime=,lstart=,command=`. pid 1 excluded; no parent walk.
- **84 distinct pids, 1 socket each**, all on 127.0.0.1 ephemeral ports.
  - By cwd: 84 × `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/raise-0916-a/Blockchain/Dev`.
  - By command: 84 × `node /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/raise-0916-a/systemTest/__tests__/support/login_stub.mjs`.
  - By ppid: 84 × 1 (orphaned).
- **What it is:** the KS-1167 B1 throwaway gateway. It answers POST /api/auth/login with one fixed status and "serves until killed".
- **Age:** 21 start groups of 4, from 2026-09-16 21:25:36 AEST to 2026-09-17 07:21:18 AEST (the oldest ~10.5 h).
- **Cause, READ not instrumented:** `systemTest/__tests__/bootstrap_login_diagnosis.test.sh:86/:97/:105/:109` run `port="$(start_stub N)"`. `start_stub` sets `STUB_PID=$!` inside that command-substitution subshell, so the parent's EXIT trap `stop_stub` finds `STUB_PID` empty and kills nothing. 4 cells per run × 21 runs = 84. The same four lines are on develop `eb1051fd3`.
- **Correlation, not measured:** the predecessor's four push logs close 3-4 min after a stub group starts (06:04:19 → push.out 06:07, 06:22:59 → 06:25, 06:35:09 → 06:39, 07:21:15 → 07:24). So the pre-push preflight's shell suites look like the runner, and each of my pushes would add 4 more.
- **Collision risk:** only for a suite binding a FIXED port inside the ephemeral range. Not measured. The api-gateway / auth / shared vitest suites I will run are not known to bind fixed ports; I will say so before any suite run if that changes.

### Queue as I re-derived it (your 21:51:25Z order)
1. GO #1016 KS-1072: merge now (ITEM 1): pre-step, squash with `--match-head-commit`, verify at origin, then KS-1072 facts → KS-1180 comment → P-1016-3 ticket → R-1016-5 ticket, each gated, then the MERGED receipt.
2. #1014 KS-1176 round 2 @ `9ba0caf78`: hold for the delta gate; no round 3.
3. KS-1195: shape + census QUESTION, then build on your ANSWER (tier 1). Not started.
4. KS-1187 severity reads: measurement only, one facts comment, then STATUS.
5. A16 KS-1050.
6. A11 KS-1101: measure the Schemathesis cost, then ASK.
7. KS-1194 (ruled fail-closed): a shape QUESTION first; serial after A16; the merge waits for Kam's tap.
8. Side: the gdpr `x-user-email` ticket candidate, searched first, not built.

### A16 KS-1050 apply plan at the tip
Checked with `git apply --cached --check --recount` against a throwaway index file read from `eb1051fd3`. No worktree or shared index was touched.
- **Import hunk:** does not apply. #1015 rewrote `users.ts:16`. By hand it becomes `import { AppError, BadRequestError, NotFoundError, ServiceUnavailableError, ValidationError } from '../middleware/errorHandler'; // KS-1018: needed to rethrow infra errors as 503`, leaving #1015's `dbErrors` import line at :17 untouched.
- **Null-guard hunk:** rc 0, "Hunk #1 succeeded at 929 (offset -2 lines)".
- **New test file** `ks1050-profile-update-zero-rows-is-not-success.test.ts`: rc 0.
- **Negative control:** the whole READY is rc 1, "patch failed: …users.ts:13".
- **The line the ticket calls `users.ts:933`** now reads at `:934`: `    const updated = await userRepo.updateUser(user.id, updates);`
- READY split rules apply: trim the blank line, `--recount`, byte-equal assert, and eslint compared against base.

### Launcher warnings at boot, verbatim
The preflight file's `# launch 2026-09-16T21:47:00Z` = my own start (`ps -o lstart= -p $PPID`: 07:47:00 AEST). There is no KS-907 line this boot; one claude session was live (mine).
```
[F-02] No SSH identity available for git (keychain not seeded, on-disk fallback off).
       Run: ssh-add --apple-use-keychain ~/.ssh/secuura_blockchain_deploy_rw
       Or temporarily: export SECUURA_ALLOW_ONDISK_KEY=1 before launching.
       (git will use whatever core.sshCommand is already in the repo config.)
```
The repo's `core.sshCommand` key fetched rc 0.

### Boot sweep (launcher steps)
- **Linear:** 70 active on the board account (In Progress 33, Todo 23, In Review 12, Blocked 2); 83 team-wide.
  - Backlog 294 (Urgent 2, High 75, Medium 154, Low 58, None 5).
  - Completed <24h: KS-1130 only. PS assigned: 0. 0 overdue.
  - Non-board comments <24h: 1 (Stuart, KS-1175, 10:36Z, pre-existing).
- **Extranet:** 6 tasks / 0 replies / 1 doc, all pre-existing. `/api/seen` NOT called.
- **BACKLOG.md** on develop: 33 open.
- **Mail:** your brief, GO #1016, RULED KS-1194. The inbox key is scoped: own 200, coagent@ 404, count 1. The watcher was re-armed after the RULED mail.

### Declined launcher lines, as before
CC to Kam, extranet to-dos / @-mentions, `POST /api/seen`.

### Holds acknowledged
No deploy / kintsugi / demo / stack / az; nothing to Peter or Stuart; no `.github/workflows`; no force / `--no-verify` / `--admin`; `--no-track`; shared `.git/config` untouched; node only inside my worktree; never delete; the 40% cap. No vault write until your ANSWER, so today's daily-note priorities entry waits for it.

