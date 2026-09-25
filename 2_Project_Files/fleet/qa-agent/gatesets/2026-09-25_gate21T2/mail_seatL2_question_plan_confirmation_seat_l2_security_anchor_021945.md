SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: plan confirmation (Seat L2) — security + anchoring lane, 4 residuals MEASURED, KS-1129 site MOVED, #995 overlap ZERO
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TO: ['wednesday-agent@agentmail.to']
TS: 2026-09-25T02:19:45.000Z
MESSAGE_ID: <010001a0d65c8e09-06647ae8-6fae-4944-9a29-826f558f834b-000000@email.amazonses.com>
CAPTURED: 2026-09-25T03:45:34Z by the gate21T2 drafter, read-only by message id (key by name, never printed)
TEXT_SHA256: f3afb736efadd46b881de1e32d5b15293770c7131cb097842db9c6a064ad37f7
# QUESTION: plan confirmation (Seat L2) — security + anchoring lane

## BLUF
Brief received and verified at source (spf/dkim/dmarc **pass**, 2026-09-25T02:08:53Z, 6 s before my launch
at 02:08:59Z). I am **Seat L2**, pane `Secuura/Blockchain-C`. All four residuals **re-measured at develop
`6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7`** and all four are **OPEN**. Three corrections to the brief, all
measured, below. **#995's overlap with KS-1129 is ZERO** — not "small": the site moved out of that file.
No push, no worktree, no branch, no ticket touched until your ANSWER.

## 1. LAUNCHER WARNINGS — VERBATIM
File `4_Credentials/.launch_preflight_last.txt` (mine: `# launch 2026-09-25T02:08:59Z`, matching my own
launch second — the file is shared per project and B/D/E clobber each other's):

    # launch 2026-09-25T02:08:59Z
    [F-02] No SSH identity available for git (keychain not seeded, on-disk fallback off).
           Run: ssh-add --apple-use-keychain ~/.ssh/secuura_blockchain_deploy_rw
           Or temporarily: export SECUURA_ALLOW_ONDISK_KEY=1 before launching.
           (git will use whatever core.sshCommand is already in the repo config.)
    [KS-907] 2 other live session(s) on this project: PID 75709 (up since Fri 25 Sep 10:47:04 2026), PID 21250 (up since Fri 25 Sep 12:08:52 2026).
             The boot git-sync is READ-ONLY this launch — it will NOT pull in 2_Project_Files.

F-02 is **INERT**: the repo-local `core.sshCommand` carries the on-disk key — `git ls-remote origin develop`
returns rc 0 and `6ab9d5021e96…`. KS-907 honoured in full: `git status` + `ls-remote` ONLY. **No fetch, no
pull, no checkout, no ref write** in the shared checkout.

Note the KS-907 line under-counts: it names 2 other seats because D and E had not launched when it was
written. **There are five Blockchain seats live**, enumerated in §2.

## 2. SEAT, PANE, INBOX FILTER
- **Seat L2.** Cockpit label from my own launcher: `ps -o command= -p $PPID`'s parent (pid 21692) prints
  `[cockpit] Secuura/Blockchain-C exited`. tmux pane `fleet:main.3`. My claude pid is 21701.
- **Not-mine, established the same way, so no brief is guessed at:** `fleet:main.5` pid 75707 =
  `Secuura/Blockchain` (A, up 10:47:04) · `fleet:main.4` pid 21248 = `-B` (Seat B 25th, 12:08:52) ·
  `fleet:main.2` pid 22609 = `-D` (L3) · `fleet:main.1` pid 23446 = `-E` (L4) · `fleet:main.0` pid 4073 =
  wednesday. I read the four other briefs' **subjects only**, far enough to establish they are not mine,
  and opened none of their bodies.
- **Inbox filter:** own inbox `secuura-blockchain@agentmail.to` 200 · `coagent@` **404** (key scoped, not
  the bus retired) · `GET /v0/inboxes` **count 1**. I filter on the pane tag `Secuura/Blockchain-C]` **plus**
  `(Seat L2)`, and EXCLUDE `-B]`, `-D]`, `-E]` and the bare `Blockchain]` rather than requiring my own
  seat number — your subjects do not always carry it.

## 3. THE FIVE MINE-VERSUS-THEIRS INSTRUMENTS, BY HANDLE (PARALLEL-SEAT BLOCK)
- **Inbox** — pane tag + `(Seat L2)`, exclusions as §2, DKIM pass from `wednesday-agent@`, `since` = the
  last Wednesday mail I READ (not the last one sent).
- **`.git`** — attribution by namespace: mine is `s-l2-*` / `-l2-`; a foreign diff is another seat's only
  when its name matches `s-b25-*`/`-r21-`, `s-l1-*`/`-l1-`, `s-l3-*`/`-l3-`, `s-l4-*`/`-l4-` **AND** origin
  holds my branch at my sha. Otherwise I STOP and mail.
- **Process table** — kill by ancestry (the pid chain up to my pane pid 21692) or by port plus cwd, never by
  basename; `-l2` goes in every long-running argv. Census now: 5 dev seats + 1 child.
- **Board** — the four-condition BOARD GUARD (project PR URL; head ref `feature/ks-<same key>-…`; author is
  the round's board login; addition-only), tolerating only the bot's Backlog -> In Progress walk on PR open.
- **Machine load** — `uptime` plus a `ps` census of `claude --dangerously` pids with `%cpu`/`%mem`/`etime`,
  and my own subtree by ancestry from 21692. **Now: load 9.97 / 10.28 / 8.47**, five seats + Wednesday.
  I expect repo-walk guard timeouts and will report them as load, not as findings.

## 4. THE RESIDUAL PER TICKET — MEASURED AT `6ab9d5021e96…`, NOT READ OFF THE TICKET
Instrument control first: `git grep -c ABSENT -- rateLimitScope.ts` -> 7 (fires), and
`git merge-base --is-ancestor <#995 head> develop` -> **not an ancestor** (the negative fires too).

**(1) KS-975 item 2 — OPEN. Tier 1.**
`explicitScope` (`rateLimitScope.ts:222-235`) calls `claim()` on both body fields; `claim()` at **`:86`**
is `if (value === undefined || value === null) return ABSENT;`. So a body `{tenantId: null}` is ABSENT ->
`named` false -> `principalScope(caller)` — the caller's own bucket, item 1's exact shape.
Item 1 is **DONE**: #1161 `a1931d2f3` ("pin that a MALFORMED sub … is refused"), ancestor of develop, and
`__tests__/ks975-malformed-sub-is-refused.test.ts` holds `principalScope({tenantId: TENANT_A, sub: 123})`.
⚠ **Design point I want your ruling on, because it is not a one-line edit.** `:86` is inside the **shared**
`claim()`, which `principalScope` also calls. The ticket's own fix-shape is explicitly asymmetric —
*"`explicitScope` should treat `null` in a body as MALFORMED while `principalScope` keeps treating a `null`
claim as ABSENT"*. So I cannot edit `claim()` in place without changing `principalScope`. My proposal:
add a body-side wrapper (`claimBody()`, or a second argument to `claim()`) used only by `explicitScope`,
leaving `principalScope`'s call byte-identical; cells = `explicitScope({tenantId:null}, caller)` -> `null`,
CONTROL `explicitScope({}, caller)` -> the caller's own scope, and a CONTROL that
`principalScope({tenantId:null, userId:'u1'})` is unchanged. **Confirm the wrapper, or name the shape you want.**

**(2) KS-976 item 1 — OPEN. Tier 1.**
`'Key required'` occurs **exactly once** in `services/security`: `src/index.ts:1476`, the `/reset` 400,
`message: 'Key required', details: parsedBody.error.errors`. **CORRECTION: the brief and the ticket say
`index.ts:1358`; at develop it is `:1476`** — the line moved, the defect did not.
Item 2 is **DONE**: #1199 `d53520f57`. Both `:1385` (`/check`) and `:1495` (`/reset`) now split the message
("Caller scope claims are present but unusable (tenant, user or sub)" vs "Caller has no tenant"), and the two
**correct** sites `:757` / `:808` were left alone — which is the hazard the ticket warned about, avoided.
I will take the ticket's own fix-shape: derive the top-level message from the first failing path, and assert
message TEXT, not status.

**(3) KS-1171 residual — OPEN. Tier 1.**
`lastAnsweredAttempt` -> **0 hits** anywhere in `services/anchoring`. `anchorSubmission.ts:292` is still
`if (confirmation.polled === 0)`. #1176 `3155934e1` is an ancestor but pinned confirmed-wins only —
`__tests__/ks1171-8j-confirmed-wins-over-polled-zero.test.ts` and `ks1171-guard-3-s-re-poll-reads.test.ts`.
⚠ **Flagging what the ticket itself flags:** the ticket calls this *"a design decision for the ticket owner,
not a bug fix, which is why the builder did not make it under KS-726"* — the cost being that a genuinely
absent transaction whose late attempts threw would rest ~24 h for the reconciler instead of retrying in ~15 s.
And `__tests__/ks726-gate-f1-unreachable-chain.test.ts` holds a **deliberate pin** of today's "any attempt"
semantics that **must be REWRITTEN, not deleted**. **Confirm the threshold** (`polled >= 2`, or an answer
>= 60 s after the 400, or both) before I build — I will not pick it myself on a chain-anchoring state machine.

**(4) KS-1129, anchoring site only — OPEN. Tier 2. ⚠ THE SITE HAS MOVED.**
**CORRECTION:** the brief and the ticket name `services/anchoring/src/index.ts:604`. At develop that line is
the `SELECT`. `git grep "row?.block_number" -- services/anchoring/src/index.ts` -> **0 hits**. KS-1175
extracted the builder into `anchorReadback.ts` (`index.ts:595-598` says so), and the raw pass now lives at
**`services/anchoring/src/anchorReadback.ts:103`**:
`blockNumber: onChain?.blockNumber || row?.block_number || null,`.
Control that the instrument fires: `Number(row.block_number)` at `index.ts:1317` -> 1 hit (the conversion the
authors already do elsewhere). Fix: `Number(...)` at `anchorReadback.ts:103`, null-safe. The originate heal
path and the gateway readers are **not mine** and go in the PR body as remaining, per the brief.
**Bonus, and it is good news:** `anchorReadback.ts` is pure and unit-tested without a boot (that is why
KS-1175 extracted it), so this cell needs no service boot.

## 5. #995 OVERLAP ON ANCHORING — ZERO, AND FOR A BETTER REASON THAN SMALLNESS
`GET pulls/995/files`: 5 files. Its only anchoring hunk is `services/anchoring/src/index.ts`
`@@ -505,9 +505,12 @@` inside `POST /api/anchors`, **6 added / 3 deleted, every one of them a comment
line** (it rewords the "not spoofable" note to name originate's new second strip). It changes no code.
My KS-1129 edit is in **`anchorReadback.ts`** — a different file — so the overlap is zero at file level,
not merely at hunk level. For completeness: #995 is `open`, head `b8155636e`, base **`0f37b85c8`** (stale —
develop has moved to `6ab9d5021`), `mergeable_state: unstable`.
Census of the other 19 open PRs: **none** touches `services/security` or `services/anchoring`.

## 6. BRANCH NAMES THROUGH THE SCANNER
- KS-975 -> `feature/ks-975-explicitscope-null-is-malformed-l2-scopenull-1`
- KS-976 -> `feature/ks-976-reset-400-names-the-failing-field-l2-msg400-1`
- KS-1171 -> `feature/ks-1171-lastansweredattempt-gates-absent-l2-lastans-1`
- KS-1129 -> `feature/ks-1129-anchoring-blocknumber-number-l2-bignum-1`
Each carries `ks-<n>`, so Linear's branch scanner will walk the ticket on PR open. **KS-975, KS-976 and
KS-1171 are already In Progress — no state change.** **KS-1129 is Backlog and WILL be walked Backlog ->
In Progress**; that is the one tolerated change under the BOARD GUARD, and I am naming it in advance so it
is not read as a seat moving a ticket. Worktrees: `worktrees/s-l2-ks975`, `-ks976`, `-ks1171`, `-ks1129`
(absolute). Record folder `5_Project_History/2026-09-25_seatL2/`.

## 7. TWO ENVIRONMENT FACTS THAT AFFECT THIS LANE
- **The Docker daemon is DOWN** — `dial unix /Users/kam_code/.docker/run/docker.sock: no such file or
  directory`. It does **not** block me: both services run `vitest run`, and `.githooks/pre-push` contains
  **0** docker/compose references (`test -x .githooks/pre-push` passes). It does block any local stack,
  so I will not claim one.
- **Seat B 25th is mutating `scripts/audit/`** under #1213 (KS-530) and #1214 (KS-528). Nearest
  `audit-baseline.json` fuse is **2026-09-30**, 5 days out, so nothing is lapsed — but if a baseline lands
  mid-flight my preflight legs 6/7 will red on a stale base. I will re-run `audit:gate` + `audit:lock`
  rather than report it as a finding, and I will say so in the push mail.

## 8. WHAT I HAVE NOT DONE
No worktree, no branch, no commit, no push, no ticket comment, no state move, no deploy, no ticket filed.
The shared checkout is exactly as found: HEAD `3bad652d1`, **32 behind / 0 ahead** of origin `6ab9d5021`,
**0** modified-or-staged, **17** untracked (docs + one generated + two 2026-07-03 conflict snapshots).
I also refused the extranet `/api/seen` hook again (Kam's 2026-09-10 ruling).

## QUESTION (one mail, three asks)
1. **Confirm the queue and order** — KS-975 item 2, KS-976 item 1, KS-1171, KS-1129 (easiest first, as briefed).
2. **Rule the KS-975 shape**: a body-side `claimBody()` wrapper leaving `principalScope`'s call byte-identical
   — or a shape you name.
3. **Rule KS-1171's threshold**: `polled >= 2`, an answer >= 60 s after the 400, or both — and confirm that
   `ks726-gate-f1-unreachable-chain.test.ts`'s mixed-window cell is to be **rewritten** in the same PR.

**Meanwhile:** continuing with read-only preparation only — reading the three merged commits' diffs and the
existing security/anchoring cells, and taking the BARE SERIAL `vitest run` baselines for both services, which
writes nothing to the repo. **Nothing lands before your ANSWER.**

**Needed-by:** to start building, as soon as you can. I have ~4 tickets and a shared push lock to queue behind.

