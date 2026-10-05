LAUNCH BRIEF (Seat E 6th): successor of Seat E 5th (WRAPPED COLD at ctx 47%, #1385 head `f6b49d68209d` PUSHED, gate66 commissioned, KS-1256 NOT STARTED). Rows 0-3 in this order: (0) plan confirmation, READ-ONLY, then STOP for Wednesday's ANSWER; (1) KS-1256 under Wednesday's ruling 7, built in its OWN new worktree while gate66 runs: red-first, then raise, then ONE READY; (2) #1385's SECOND docs-only merge-in and the merge, ONLY on `GO (Seat E 6th): merge 1385 on gate66`, building the KEY-ANCHORED tree `fb6cb2c6992c` on develop `f0179806494e`; (3) handover. You REUSE the lock `.push-lock-e4` and the `*e4` tool generation, and re-seat only the seat token `e5`->`e6`. Secuura NEVER force-pushes.

# LAUNCH BRIEF: Seat E 6th, Secuura/Blockchain, lane E (pane `Secuura/Blockchain-E`). From Wednesday

## BLUF
You are **Seat E 6th**. You are a BUILD + MERGE seat for Kam's 31 Oct goal. Confirm you are the successor: `HANDOVER-seatE5-2026-10-05.md` exists (P10) and 0 `HANDOVER-seatE6*` files exist. develop at origin is **`f0179806494e42df254b9580168be3cd4a35f307`** (P1). **develop can move before you boot:** Seat F 4th may merge #1383 and Seat G 2nd may merge #1389 (P2, P3). #1383 touches both platform docs.

| Row | Ticket | What | Product files | Base | Gate | Flow `<h2>` |
|---|---|---|---|---|---|---|
| 0 | — | plan confirmation, READ-ONLY, then STOP for the ANSWER | none | — | — | — |
| 1 (BUILD) | `Refs KS-1256` | ruling 7: a thrown read -> 503; Redis unavailable -> 503, except a deliberate no-Redis config; unset with Redis up -> no restriction | `services/api-gateway/src/routes/verification.ts` (`:1214-:1238`) + a NEW ks1256 test + block `21.` in both docs | develop at ITEM 1 | Wednesday commissions it at your READY | **`21.`** (the next free number, P18) |
| 2 (MERGE-IN -> MERGE) | #1385 `Refs KS-938` | the second docs-only merge-in of develop into `f6b49d68209d`, building tree **`fb6cb2c6992cd48815b8f23a8519e9910bc27e63`**, then the squash merge | none new (adopted `s-e3-ks938`) | develop `f0179806494e` only | gate66 (commissioned) | `20.` (already in the head) |
| 3 | — | handover + history + WRAP | — | — | — | — |

**Queue order:** ITEM 0 -> ANSWER -> ITEM 1 KS-1256 (gate66 runs in parallel) -> ITEM 2, only when the GO arrives. If the GO arrives while ITEM 1 is mid-build, first finish the step you are on. Do not start a lock take or a push for ITEM 1 after that. Do ITEM 2, then go back to ITEM 1. **Never start ITEM 1 past ~45% ctx. Never START a push past ~50%. Hand over COLD at ~60%.** Read ctx off your OWN statusline. If you cannot, write "Please read my ctx." Never estimate it.

🔴 **ARM `inbox_watche4.sh <since-iso> [interval]` (usage at `inbox_watche4.sh:110`) IN THE BACKGROUND AT BOOT, BEFORE ITEM 0's MAIL** (`timeout: 7200000`). **It EXITS on every FOR-ME match. RE-ARM IT IMMEDIATELY, with `SINCE` = the newest mail you have actually READ, never a wall clock** (STANDING_LINES `:399`). After any long side-effecting action, LIST the inbox by API before the next ref write. **No mail leaves unless the watcher pid in it is NON-EMPTY and `ps -p <pid>` finds it ALIVE.** No reusable send tool carries that guard (P15): build it into your send path and drive it three ways (empty pid refused, dead pid refused, live pid sent).

**Authority:**
- Kam's delegated-merge grant 2026-09-11 ("We approve and merge our own TESTED Platform K work"), one merge per signed GO naming the head.
- Kam's card `secuura-connector-allowlist-missing-setting-ks1256-1005` = **b** (P13).
- Wednesday's ruling 7, VERBATIM from E 5th's handover `:271-:286` (P11).
- Wednesday's gate66 rulings 1-6 (P7).

## QUEUE
0. **ITEM 0: plan confirmation `QUESTION: plan confirmation (Seat E 6th)`, then STOP until the ANSWER.** READ-ONLY: no lock, fetch, worktree, ref write, install, ticket write or repo edit before the ANSWER. Carry all of the following:
   - **Refs at boot.** `ls-remote` of develop, `refs/pull/1385/head`, `/1383/`, `/1389/`, `/1393/` and `/1394/`, read in one action. If develop moved past `f0179806494e`, list the first-parent commits by PR number. Say whether any of them touches `Projects Documents/`, `services/auth/src/routes/{users,mfa}.ts`, `routes/verification.ts` or `services/redis.ts`. If develop moved at all, ITEM 2's ruled tree `fb6cb2c6992c` no longer stands as-is (P7 ruling 3: the gate re-pins and re-derives). #1383 or #1394 landing also changes both docs. Say which, and do not re-derive the ruled tree yourself.
   - **The re-seat receipt.** Use E 5th's `reseate5.py` model (POSITION-anchored, comments byte-identical, and it refuses any edit whose text begins with `#`). Drive every hand-fix in HAND-FIXES below. Print the counts.
   - **`e6 seat on e4 lock: 56 + f3 + g1 + d8 WAIT, 16 STOP, catch-all (Seat E 6th)`** as its own titled block. Include:
     - `twolocke4.sh` and `wdproofe4.sh`, run against an EMPTY scratch dir. Expect 34 arms / 73 pass and 5 arms / 12 pass (handover `:182`). Fewer arms is a FAIL.
     - every real `.push-lock-*` ATTRIBUTED by its holder file's `seat` field (STANDING `:408`), with TWO census readings a poll apart (handover `:210-:211`).
     - every `s-e*-*` worktree and every exact ref attributed.
   - **The KS-1256 `fallbackMode` measurement, DRIVEN, not read** (ruling 7's FIRST measurement; method and states in ITEM 1 (a)). Drive it from your scratch dir using `s-e3-ks938`'s installed `tsx`, as E 5th did (handover `:258-:262`), writing nothing in `!CODING`. P12 is the drafter's code reading: `fallbackMode` is set in TWO places, so the split E 5th read may not exist. **If the two cannot be cleanly separated at the call site, this mail says so and asks Q-1256-FALLBACK.**
   - **The KS-1256 site, re-read at develop by line range with its blob** (P11), plus the spec's 503 (P14).
   - **Skill rules quoted** from `.claude/skills/secuura-test-discipline/SKILL.md` at your base, with the blob id (P16).
   - **`s-e3-ks938` re-read WITHOUT writing:** HEAD `f6b49d68209d`, porcelain 0, `Blockchain/Dev/packages/shared/dist/index.js` present, `systemTest/akto/node_modules` present (P9).
   - **The gate66 merge-in prediction against develop as it stands.** Run it in your OWN `git clone --shared` scratch clone. Fetch develop BY SHA from a separately added GitHub remote (STANDING `:406`). Use `c4_docs_gate66.py mergetree` and `predict` (P8). Print the tree and the conflict set, parsed to the blank line.
   - **Mechanics.** Your watcher pid, read from a ps FILE written in an EARLIER call (handover `:316-:319`) and proven alive. Every launcher preflight warning VERBATIM. `df -m /Volumes/DevMASTER`. Your ctx.
   - **Your restatement of the OPEN questions below.**
1. **ITEM 1: KS-1256 (T1, `Refs KS-1256`), only after the ANSWER.** Do not START it past ~45% ctx.
   - **(a) `fallbackMode`, measured at ITEM 0 (above), decides (ii).** The drive: the REAL `services/api-gateway/src/services/redis.ts` (handover `:258-:262` method: a real ioredis client against a minimal RESP server, never a fake client).
     - **State A:** dev/test boot with Redis unreachable. `initRedis()`'s catch sets `fallbackMode = true` at `:122`. In production it throws instead (`:115-:121`).
     - **State B:** a runtime outage long enough for `retryStrategy`'s `times === 4` branch to set `fallbackMode = true` at `:78`. That branch has NO `NODE_ENV` guard.
     - **State C:** a reconnect after A. The `'connect'` handler clears the flag at `:85-:89`.
     - Record `isRedisAvailable()` (`:130-:132`) and what `getNotificationSettings('platform-settings')` returns in each state.
     - **Q-1256-FALLBACK is ALREADY RULED (section RULED BY WEDNESDAY BEFORE SEND, end of this brief):** with no deliberate no-Redis setting, (ii) = 503 while `fallbackMode` is active, whatever set it. Only if your drive FINDS a deliberate no-Redis setting: STOP and mail `QUESTION: KS-1256 deliberate no-Redis setting found (Seat E 6th)` before building (ii).
   - **(b) Fresh worktree** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-e6-ks1256`, created with `git worktree add --detach <abs> <develop>` (never `-b`; E 5th's brief `:152`) under THE LOCK RULE. Then, OUTSIDE the lock: `npm ci --ignore-scripts`, then `npm run build --workspace=packages/shared`. ASSERT `packages/shared/dist/index.js` exists before the first test (STANDING `:376`, `:396`).
   - **(c) Re-read KS-1256 WHOLE at source.** E 5th's last reading was `updatedAt` 2026-10-05T03:02:40.146Z (handover `:299-:300`). If it changed, STOP and mail.
   - **(d) The change at `verification.ts:1214-:1238`, per ruling 7:**
     - (i) a THROWN read -> **503** (shapes: `MaxRetriesPerRequestError`, and the `SyntaxError` from `JSON.parse` at `redis.ts:675`). Today `} catch {}` at `:1238` leaves `connectorConfig = {}`.
     - (ii) a read while Redis is UNAVAILABLE (including `fallbackMode` active, whatever set it) -> **503**; the deliberate-config exception applies only if ITEM 1 (a) finds one (then STOP and mail), per the RULED section.
     - (iii) Redis UP and the key absent -> **no restriction** (Kam's b).
     - `containerBad` -> 403 stays unchanged (`:1239-:1242`).
     - The workflow-bypass reader at `:1281-:1289` is NOT in scope. Say so.
     - Every changed line carries WHY + `KS-1256` + the prior behaviour (skill §5d).
   - **(e) Red-first BY ASSERTION, then raise.** Use the real route handler over loopback HTTP and stub ONLY the Redis read.
     - Cells: (i) at the base is not 503 (RED) and at the head is 503. (ii) is per the ANSWER. (iii) is unchanged at both. Controls at both: a malformed container -> 403, and a restricted connector with a READABLE allow-list -> refused.
     - Classify each of E 5th's measured arms by its cell: close -> null, in-flight drop with reconnect -> value, server gone -> throws, malformed bytes -> throws (handover `:263-:269`).
     - Run the api-gateway suite before and after by NAMED binary. Run `tsc` with a planted positive control. `npm run check:openapi` must return rc 0 (repo `CLAUDE.md` PR rule, per E 5th's brief `:124`). No spec edit: 503 is declared (P14).
   - **(f) Doc blocks.** Flow `21.` (P18) and cheat-sheet KS-1256 LAST (P19), both before `  </body>` with develop's close tag byte-identical. Compose in SCRATCH with `composee5.py`, the newline-tolerant reader (P17), and keep its planted `<h2>\n 99.` control both ways. The positional predicate `lines[index(close)-1] == block[-1]` does the work, not the ascending reader (handover `:59-:62`). The skill §4 timing statement includes its grep, a must-hit control, and the HOST on every timing row.
   - **(g) Commit and push.** ONE commit, 0 trailers, subject <= 92 as it LANDS (no `(#n)`). Pathgate exactly `verification.ts`, the ks1256 test and the two docs, with a firing control. Push ONCE with `pushe4.sh` BARE with `LOCK_SEAT` exported. It takes the lock itself (`pushe4.sh:134` calls `locke4.sh take`; STANDING `:373`). Never start the push past ~50% ctx.
     - **KS-1256 is a RUNTIME change:** on PREFLIGHT 12/15 (stack down), ASK before pushing (handover `:91`).
     - Before the push, read the format gate's `SKIP — <pkg> deps not installed` line, and run `npm ci --ignore-scripts` in EACH named `systemTest/<pkg>` in your OWN worktree, outside the lock (STANDING `:410`).
     - The push result is the `.rc` file plus `ls-remote` of the ref (`:401`).
   - **(h) Raise by REST with `raisee4.py`** (read its flags at ITEM 0 and name them in the plan). Expect HTTP 201, head == origin, and the body sha256 read back.
     - Body: `Refs KS-1256` + URL. Kam's card by id, with choice b and its detail VERBATIM (P13). Ruling 7 quoted. Test Evidence written by YOU.
     - NOT COVERED: `live sweep owed`; the fresh-install gap kept by Kam's b; the reader census (`admin.ts:1119/:1144/:1154`, `health.ts:52`, `verification.ts:1283`) NOT audited (P11).
   - **(i) ONE READY: `READY FOR QA (Seat E 6th): #<n> (KS-1256) -> gate<NN>`.** It carries "no independent re-key auditor" (handover `:190-:191`) and `pushe4_ff.sh:108-109` NOT DRIVEN. Re-arm the watcher.
2. **ITEM 2: #1385, ONLY on a signed mail whose subject carries exactly `GO (Seat E 6th): merge 1385 on gate66`.** Confirm by API: subject, timestamp, and `authentication_results` spf/dkim/dmarc `pass`. A GO naming any other seat is FOREIGN.
   - Re-read develop and `refs/pull/1385/head` at origin in ONE action. **If develop != `f0179806494e`, or the head != `f6b49d68209d`, STOP and mail: the gate re-derives the tree** (P7 ruling 3).
   - develop `f0179806494e` is ALREADY in the shared store (P6). Fetch NOTHING. If a later develop is ever ruled, use the objects-only route (STANDING `:404`).
   - **The target is the KEY-ANCHORED tree `fb6cb2c6992cd48815b8f23a8519e9910bc27e63`** (P7 ruling 1):
     - flow blob `2d1cd366a8cb` (git auto-merges it);
     - cheat blob `48c266810fe5`, written into the cheat-sheet conflict, the ONLY conflicted path (P8).
     - **The hand resolution `0bb86333ba28` is WRONG: it leaves one `</div>` unclosed.** Never build it.
     - **NO reformat of the KS-938 block** (ruling 2).
     - Build from #1385's head `f6b49d68209d`: compose and assert in SCRATCH before the take. In `s-e3-ks938`, MERGE develop IN (never a rebase). Commit with 0 trailers. Assert `tree(M) == fb6cb2c6992c` and parents `[f6b49d68209d, f0179806494e]`. Re-assert `dist/index.js` and akto `node_modules`.
   - **Inherited tools fail closed** (STANDING `:405`). `mergein_1385_e5.sh:6-:18`, `:34-:35` hard-codes E 5th's D, H, T, scratch session and resolution hashes (P15). Pass every knob as a required argument with no default, or write a new tool. Before the run, list each knob with its value.
   - **The GO covers M only if** `G66_SCRATCH=<your scratch> python3 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate66/c4_docs_gate66.py qm --repo <your clone> --merge-in-head <M> --develop-after f0179806494e42df254b9580168be3cd4a35f307` passes M1-M8 (P8). Anything else re-gates: STOP and mail.
   - Push with `pushe4_ff.sh` BARE with `LOCK_SEAT` exported. Positional args are `WT TARGET EXPECT` (`pushe4_ff.sh:91`), with `EXPECT` = `f6b49d68209d4fa368335d3c2fa3e4928c3efaa1`. A widened format-gate selection follows the STANDING `:410` route. Quote the in-hook PREFLIGHT ratio EXACTLY. 12/15 is accepted for a docs-only merge-in only. On rc 141 with the ref unmoved, follow the KS-1149 class (`:401`).
   - **Merge.** Run `mergee4.py --dry` first. Flags read at `mergee4.py:125-:129`: positional `pr`, required `--addendum --go-ts --gate --seat`, optional `--prev-tree --expect-develop --repo --api --dry`.
     - The `.DRY` body: subject byte-equal to the gate's declared squash subject, no `(#n)`, only KS-938 hyphenated, 0 trailers, ONE `Merged by` naming Seat E 6th.
     - Merge with the head PINNED. Verify the squash by `ls-remote` AND the API (ONE parent, subject, trailers, `Merged by` count). Then send `STATUS: merged 1385 (Seat E 6th)`.
3. **ITEM 3: handover** at `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatE6-<UTC date>.md`. Also: the history entry at the TOP of `history.md` (re-read the top first; it is at `:25` at draft, P10), drive hygiene (HOLDS), and WRAP.

## ACT / NO-ACT
**ACT (yours):**
- the new worktree `s-e6-ks1256` and branch `feature/ks-1256-thrown-settings-read-refuses-connector-create-e6-1`, which you create;
- the ADOPTED worktree `s-e3-ks938` and EXACT ref `feature/ks-938-mfa-disable-nulls-the-seed-and-backup-codes-e3-2` (#1385), for ITEM 2's merge-in push and the merge only;
- your record folder `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/<UTC boot date>_seatE-6th/`, with copies of E 5th's `raise/` tools hashed at copy (skip `__pycache__`, `.my-last-release`, and E 5th's push records);
- lock `.push-lock-e4` (reused) with `LOCK_SEAT='Secuura/Blockchain-E e6'`.

**NO-ACT (not yours; read-only):**
- **Seat F 4th** (`Secuura/Blockchain-F`, `%47`, #1383, `.push-lock-f3`, HELD at draft, P5);
- **Seat G 2nd** (`Secuura/Blockchain-G`, `%49`, #1389, `.push-lock-g1`);
- **the B lane** (`Secuura/Blockchain`, unsuffixed: #1393 Seat B 65th round 2, #1394 Seat B 64th's, gate67; `.push-lock-56`);
- **the QA session** on gate66 + gate67 (#1385 + #1394, one session, P7 ruling 6);
- `.push-lock-d8` (D lane, Seat D 9th wrapped);
- `s-e1-ks1005` and `s-e2-ks1210`, which are FOREIGN and never removed by you.

All of these seats share the `secuura-blockchain@agentmail.to` inbox. Act on a GO, ruling or instruction ONLY when its subject names `(Seat E 6th)`.

## HOLDS
- 🔴 **THE LOCK RULE.** Every ref write needs `.push-lock-e4` HELD by you, the four WAIT locks (`-56`, `-f3`, `-g1`, `-d8`) absent, and no other `.push-lock-*` (handover `:198-:211`; E 5th's brief `:91-:95`). Ref writes are: worktree add/remove, commit, merge-in, push and merge. Take and release with `locke4.sh` in ONE FOREGROUND invocation under `trap … EXIT`, and release by the HOLDER FILE's pid, never `$$`. An unattributed lock is rc 15 and a dead pid is rc 17. WAIT is bounded at 20 min, then STOP and mail. The hold covers the ref write ONLY, never `npm ci`, a build or a suite. Report each hold time. `pushe4.sh`/`pushe4_ff.sh` take the lock themselves, so never wrap them in your own take.
- **No merge without `GO (Seat E 6th): merge 1385 on gate66`.** One PR per GO. KS-1256's merge needs its own gate and GO.
- **No deploy, no demo,** no `az`, no SSH, no migration, no live sweep. No Docker beyond a LOCAL test stack for KS-1256's preflight legs, and ASK first.
- **NO force push, no `--no-verify`, no `-u`, no `--admin`, no `ALLOW_FORCE`.** Catch up by MERGING develop IN (`:395`). Never `git push --dry-run` (`:382`) and never `git fetch --dry-run` (`:402`).
- **No spec, dependency, lock, manifest or baseline edit.** No ticket state, assignee, label or project change. Close nothing (§5f). No comment to Peter or Stuart. Ticket comments go out ONLY on a GO's relay.
- **Do not reclaim `s-e3-ks938/systemTest/akto/node_modules`** (165 MB, load-bearing, P9). At WRAP, remove only what YOU created for MERGED work (`s-e6-*`, your scratch clones). `df -m` before and after (702,908 MiB at draft, P20).
- Signature classes pause for Kam: production, money, external communication, anything irreversible. A new mail from `kreiser.org@me.com` means STOP and mail Wednesday.
- zsh: `cmd > f 2>&1; rc=$?`, never through a pipe. Never `cd`. Brace every `"${M}:Projects Documents/…"`. Never a bare `tmux display -p`: use `-t "$TMUX_PANE"` (`:394`). Never a zsh variable named `path`. QUOTED heredocs only for mail bodies.
- **Mail:** to `wednesday-agent@agentmail.to`, subject prefix `[Secuura/Blockchain-E -> Wednesday] `, every subject names `(Seat E 6th)`; routing tokens only as the leading tag. Compute every mailed figure in the SAME call that sends it.
- **No attribution:** branch commits carry no `Co-Authored-By` or tool trailer (`%(trailers)` = 1 byte, with a control). Squash bodies via `mergee4.py` `no_trailer`, checked on the SENT body (`:370`).

## HAND-FIXES (re-seat `e5`->`e6`, each driven, before/after in your receipt)
1. 🔴 **Trap 4.** Re-key FIRST, pinning the whole (subject, want) tuple: `trap4_e4.py:82-:83` holds a `(Seat E 6th)` UNTAGGED fixture, which names YOU (P15). Then set `MINE = "e 6th"` (`inbox_matche4.py:102`).
   - **Backward half:** add `e 5th`, `seat e 5th`, `f 4th`, `seat f 4th`, `g 2nd`, `seat g 2nd`, `b 64th`, `seat b 64th`, `b 65th`, `seat b 65th` to `OTHER_SEATS`. All are absent at draft (P15).
   - **Forward half:** add `e 7th`, `seat e 7th` (`:407`). Once `e 7th` is in OTHER_SEATS, a `(Seat E 7th)` fixture reads FOREIGN, so E 5th's "re-key to `(Seat E 7th)` UNTAGGED" (handover `:126`) cannot hold. **Test the UNTAGGED clause with an addressee in NEITHER list, e.g. `(Seat E 9th)`** (`:411`).
   - Every must-fire control fires. E 5th's two real GOs (`GO (Seat E 5th)`…) and E 4th's read FOREIGN. Your own launch brief reads FOR ME. Write one tamper per added constant, each biting at least one arm.
2. `namechecke4.py`: `MINE = "e6"` (`:69`). Add `e5`/`seate5`, `b65`/`seatb65` to `FOREIGN` (`:138`). Treat `f4` and `g2` the way the file already treats `f3` and `g1` (exact-name only), and confirm `e4` and `e5` are both FOREIGN. **Do not build the MINE split** (handover `:146-:150`). PR PLAN rows are YOUR two rows only.
3. `locke4.sh:215`: the `LOCK_SEAT` example -> `e6`. Make refusal messages naming Seat E 5th name Seat E 6th, on LIVE text only.
4. `raisee4.py:43` `REC` and `:177` stem -> YOUR folder and `s-e6-`. Re-point the `mergee4.py:120` and `armse4.py:65` scratch defaults under YOUR session. Prove set == read.
5. `residue_audite4.py`: grep for `int(`, `\d\d`, `[0-9]{2}`, `5[0-9]` generation predicates BEFORE the first run (handover `:164-:166`). Its CONTROL A plant `nosuchlivetoole3.sh` must stay a name that no KEEP entry can exempt.
6. Every checker prints its CHECKED count, and `0 checked` is a FAIL (`:335`).

PROVENANCE:
- P1 develop at origin = `f0179806494e42df254b9580168be3cd4a35f307` ("Merge pull request #1391", parents `c5101866ef54` + `35243e53af1b`); `refs/pull/1385/head` = branch `feature/ks-938-mfa-disable-nulls-the-seed-and-backup-codes-e3-2` = `f6b49d68209d4fa368335d3c2fa3e4928c3efaa1`; read 2026-10-05T13:47:42Z, rc 0, saved `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02680bc2-8977-4789-b1d7-7ca7eff59511/scratchpad/e6drafter/lsremote1.txt` | `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop refs/pull/1385/head refs/pull/1383/head refs/pull/1389/head refs/pull/1393/head refs/pull/1394/head 'refs/heads/feature/ks-938*' 'refs/heads/feature/ks-1256*'` | read 2026-10-06
- P2 `refs/pull/1383/head` = `32e8459bc0f51d1af492aae7c0b3d9754f78c9bf` (F 4th's; touches both docs, flow `22.`); `refs/pull/1389/head` = `a7f5965a7b3fd94b25a26e73c250052db4be6aa0` (G 2nd's); either merging moves develop before E 6th boots | same ls-remote as P1 + `git show <sha>:"Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html"` read by `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02680bc2-8977-4789-b1d7-7ca7eff59511/scratchpad/e6drafter/h2nums.py` | read 2026-10-06
- P3 `refs/pull/1393/head` = `4a1620588819a35c180fb1a4a3d98d35f4814f3f`, `refs/pull/1394/head` = `a94ec8f6a2c6ec382fb7b5dbafcf8a7f9ce68427` (flow `16.`, gate67); `refs/heads/feature/ks-1256*` = 0 refs | same ls-remote as P1 | read 2026-10-06
- P4 KS-938 In Progress, board account, no project, updated 2026-10-05T07:47:55Z, 1 comment (newest 2026-09-13T07:35:55Z) | Linear GraphQL issue(id:) read-only, Secuura project key, by Wednesday 00:5x AEDT | read 2026-10-06
- P5 `.push-lock-f3` PRESENT, holder `{"seat": "Secuura/Blockchain-F f4", "pid": 85867, "branch": "feature/ks-1401-tenant-isolation-after-039-f2-1", "started_utc": "2026-10-05T13:44:21Z"}`; no other `.push-lock-*`; panes `%0` wednesday, `%47` Secuura/Blockchain-F, `%49` Secuura/Blockchain-G, no `-E` and no unsuffixed pane at 13:48:52Z | `ls -1A "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees"` + `cat …/.push-lock-f3/holder` + `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` | read 2026-10-06
- P6 shared store: `cat-file -t` = commit for `f0179806494e`, `f6b49d68209d`, `32e8459bc0f5`, `a7f5965a7b3f`; tree `fb6cb2c6992c` ABSENT; control `deadbeef…` ABSENT | `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" cat-file -t <sha>` | read 2026-10-06
- P7 Wednesday's gate66 rulings 1-6 (key-anchored `fb6cb2c6992cd48815b8f23a8519e9910bc27e63` is the target; hand `0bb86333ba28` one `</div>` unclosed, WRONG; NO reformat; re-pin `f0179806494e`; gate66 + gate67 one QA session) | read `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate66/RULINGS_wednesday.md` whole | read 2026-10-06
- P8 on `f0179806494e`: `merge-tree` rc 1, tree-with-markers `73f98d063ed2`, conflicted paths (1) = the cheat sheet only; key flow blob `2d1cd366a8cb`, key cheat blob `48c266810fe5`; CLI `predict/mergetree --repo <OWN clone> --develop-after <D>`, `qm --repo <clone> --merge-in-head <M> --develop-after <D> [--predicted <tree>]` (`c4_docs_gate66.py:22`, `:29`, `:31`); `G66_SCRATCH` (`lib_gate66.py:14`) | read `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate66/c4_mergetree_devf017_ex1.out`, `c4_predict_devf017_key_ex1.out`, `kit.json` `merge_in_predicted`, `RESULT.txt`, `README.md` | read 2026-10-06
- P9 `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-e3-ks938`: HEAD `f6b49d68209d4fa368335d3c2fa3e4928c3efaa1`, porcelain 0 lines, `systemTest/akto/node_modules` 165 MB, `Blockchain/Dev/packages/shared/dist/index.js` 17,746 bytes; `worktrees/` 501 entries; `s-e*` = `s-e1-ks1005`, `s-e2-ks1210`, `s-e3-ks938` | `git -C <wt> rev-parse HEAD` + `status --porcelain` piped to `wc -l` + `du -sm` + `stat -f %z` + `ls -1A` | read 2026-10-06
- P10 E 5th's handover `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatE5-2026-10-05.md` 356 lines, sha256 `65bce9ddba50c234…`; 0 `HANDOVER-seatE6*`; `history.md` newest `## ` at `:25` (B 64th), E 5th's at `:40` | `shasum -a 256` + `wc -l` + `ls` + `/usr/bin/grep -n '^## ' /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/history.md` | read 2026-10-06
- P11 KS-1256 site at `f0179806494e`: `Blockchain/Dev/services/api-gateway/src/routes/verification.ts` blob `b8cdee1bc408`: `:1130` `router.post('/api/documents', …`; `:1214` `let connectorConfig: Record<string, unknown> = {};`; `:1221` `const sRaw = await redisService.getNotificationSettings('platform-settings');`; `:1238` `} catch {}`; `:1239-:1242` containerBad -> 403; second reader `:1283`, `} catch {}` `:1288`, `bypassWorkflow` `:1289`; other readers `admin.ts:1119`, `:1144`, `:1154`, `services/health.ts:52` | `git show f0179806494e:<path>` piped to `sed -n 1208,1292p` + `git grep -n "getNotificationSettings('platform-settings')" f0179806494e -- Blockchain/Dev/services/api-gateway/src` | read 2026-10-06
- P12 `redis.ts` blob `fbb74be7ccc3` at `f0179806494e`: `fallbackMode = true` at `:78` (inside `retryStrategy`, `times === 4`, NO `NODE_ENV` guard) AND at `:122` (`initRedis()` catch, after the production throw `:115-:121`); cleared `:88` (`'connect'`); `isConnected = false` `:93`, `:98`; `isRedisAvailable()` `:130-:131`; `getNotificationSettings` `:671`, `JSON.parse` `:675`; `maxRetriesPerRequest: 3` `:60`; NO deliberate no-Redis switch (0 raw hits under `Blockchain/Dev` for any of REDIS_DISABLED, REDIS_ENABLED, REDIS_MODE, NO_REDIS, USE_REDIS; control `REDIS_URL` HIT at `redis.ts:17`) — CODE READING, not a drive | `git grep -n -E` (fallbackMode, isConnected, isRedisAvailable, getNotificationSettings, maxRetriesPerRequest) at f0179806494e on redis.ts + `git show` piped to `sed -n 40,84p` | read 2026-10-06
- P13 Kam's card `secuura-connector-allowlist-missing-setting-ks1256-1005`: status ruled, `choice='b' ruled_ts=2026-10-05T16:22:42.474168+11:00`, option b "Keep 'no restriction' when unset", detail "No behaviour change; the gap stays for fresh installs." | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-connector-allowlist-missing-setting-ks1256-1005` rc 0 | read 2026-10-06
- P14 spec `Blockchain/Dev/docs/openapi/secuura-api.yaml` blob `52310cab1874` (unchanged from E 5th's reading): `:27659` `"503":` "Service unavailable — temporary outage or required dependency down." (its verb `POST /api/documents` is E 5th's attribution, handover `:291-:293`) | `git ls-tree -r f0179806494e` filtered to secuura-api.yaml + `git show` piped to `sed -n 27655,27662p` | read 2026-10-06
- P15 E 5th's tools `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-05_seatE-5th/raise/` (50 entries): `inbox_matche4.py:102` `MINE = "e 5th"`, OTHER_SEATS (100 members) lacks `e 5th`, `e 6th`, `e 7th`, `f 4th`, `g 2nd`, `b 64th`, `b 65th`; `trap4_e4.py:82-:83` `(Seat E 6th)` fixture want UNTAGGED; `namechecke4.py:69` `MINE = "e5"`, FOREIGN lacks `e5`, `b65`; `locke4.sh:212` own lock `-e4`, `:215` `LOCK_SEAT` example `e5`, WAIT `:275-:278` `-56 -f3 -g1 -d8`, STOP `:329` 16 names; `pushe4_ff.sh:89` refuses without `LOCK_SEAT`, `:91` `WT TARGET EXPECT`; `mergein_1385_e5.sh:6-:18` hard-codes `D=d784…`, `H=79c87…`, `T=04fa3e…`, E 5th's scratch; `ps -p|kill -0` only in `locke4.sh`, `lockproofe4.sh`, `watchproofe4.sh` (no send tool) | `python3 ast.literal_eval` of the lists + `/usr/bin/grep -n` + `ls` | read 2026-10-06
- P16 skill at `f0179806494e`: `.claude/skills/secuura-test-discipline/SKILL.md` blob `eaf43dfd4d98`, 642 lines; the rules touching this round: §1 `:15-:16` written plan before any edit/run, `:28` say where sources disagree; §1 Secrets `:64` never open a secrets file; §2 `:90-:91` state host/environment before running; §4 `:362` both platform-k docs in the SAME commit, `:380-:385` timings with figure, date and HOST, `:417-:418` say explicitly if a doc is unaffected; §5b `:451-:452` every fix red on broken code, green after; §5d `:509-:513` WHY + ticket on every changed line, ticket URL in the PR; §5e `:535-:538` no `.env` staged, no branches/merges/tickets unless instructed; §5f `:542-:545` runtime change not Done on offline green (live sweep owed), `:549-:550` name what is unverified | `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" show f0179806494e:.claude/skills/secuura-test-discipline/SKILL.md` saved to `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02680bc2-8977-4789-b1d7-7ca7eff59511/scratchpad/e6drafter/SKILL_f017.md`, read by section with `sed -n` | read 2026-10-06
- P17 `composee5.py` sha256 `f9ab42d9fc25f189…`, 97 lines; `:42` one-`<h2>`-per-block assertion, `:66` `re.findall(r'<h2[^>]*>\s*(\d+)\.', …, re.S|re.I)`, `:82` `re.findall(r'<h2[^>]*>.*?&mdash;\s*(KS-\d+)\s*</h2>', …)`; `residue_audite4.py` sha256 `47b4968a00657f41…` | `shasum -a 256` + `wc -l` + `sed -n '42p;66p;82p'` | read 2026-10-06
- P18 flow `<h2>` numbers (newline-tolerant reader, planted `<h2>\n 99.` control HIT): develop `1`-`14`, `18`, `19`; #1385 adds `20`; #1383 `22`; #1393 `15`; #1394 `16`, `18`, `19`; #1389 none new; **`21` free in all six**; flow `  </body>` at `:2990`, blob `6f573e6ca768`, 2,991 lines | `git show <sha>:"Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html"` piped to `python3 /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02680bc2-8977-4789-b1d7-7ca7eff59511/scratchpad/e6drafter/h2nums.py` + `grep -n -i '</body>'` piped to `cat -vet` | read 2026-10-06
- P19 cheat sheet at `f0179806494e`: blob `2e91250dbd3a`, 4,414 lines, 6 keyed `<h2>`, the KS-1005 section LAST, `  </body>` at `:4413` | same reader + grep | read 2026-10-06
- P20 `df -m /Volumes/DevMASTER` = 702,908 MiB free | `df -m` | read 2026-10-06
- P21 develop `d784b613c81e..f0179806494e` = 38 paths: 34 `systemTest/schemathesis`, `systemTest/CLAUDE.md`, both docs, `history.md`; `systemTest/schemathesis/package.json` ABSENT (control `nosuchpkg` absent; `akto`/`playwright`/`performance` present) | `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" diff --name-only d784b613c81e f0179806494e` saved to `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02680bc2-8977-4789-b1d7-7ca7eff59511/scratchpad/e6drafter/adv_d784_f017.txt` + `git cat-file -t <rev>:<path>` | read 2026-10-06
- P22 KS-1256 Backlog, board account, project Security Review — Platform K, updated 2026-10-05T03:02:40Z (UNMOVED since E 5th's reading), 0 comments | Linear GraphQL issue(id:) read-only, Secuura project key, by Wednesday 00:5x AEDT | read 2026-10-06
- P23 KS-1005 In Progress, board account, updated 2026-10-05T11:33:48Z, 0 comments — named only as the cheat-sheet anchor section | Linear GraphQL issue(id:) read-only, Secuura project key, by Wednesday 00:5x AEDT | read 2026-10-06
- P24 KS-1149 Backlog, board account, updated 2026-09-14T01:13:12Z, 1 comment — the rc-141 class | Linear GraphQL issue(id:) read-only, Secuura project key, by Wednesday 00:5x AEDT | read 2026-10-06
- P25 KS-1148 Backlog, board account, project Internal tooling, updated 2026-10-05T12:06:58Z, 3 comments (newest 2026-09-25T09:47:32Z) — Kam's stale-docs ticket | Linear GraphQL issue(id:) read-only, Secuura project key, by Wednesday 00:5x AEDT | read 2026-10-06

## RULED BY KAM, NOT YET IN AN ARTEFACT
- secuura-connector-allowlist-missing-setting-ks1256-1005: "b — Keep 'no restriction' when unset" (ruled 2026-10-05 16:21, P13) -> must land in KS-1256's PR body (quoted verbatim, ITEM 1 (h)) and the READY.
- The 2026-09-11 TESTED merge grant ("We approve and merge our own TESTED Platform K work"), exercised only on a signed GO -> named in #1385's squash body via mergee4.py's addendum.
- Kam 2026-10-05 16:21 (note on the KS-1256 card): "for the month of October ... deploy all that works and is ready but only when its ready. Deploy to both servers, demo and kintsugi" -> NOT this seat's to act on (no deploy here); recorded so you do not read a deploy into it.
- The other ruled Secuura cards with no delivery mark (a board-pass backlog of ~54 across the project) are NOT this seat's to deliver; Wednesday routes them to a board seat.

## QUESTIONS for ITEM 0
**RULED (carry; confirm you read them):**
- **Ruling 7** (handover `:271-:286`).
- **Kam's card b** (P13).
- **gate66 rulings 1-6** (P7): key-anchored `fb6cb2c6992c` is the target; NO reformat; if develop moves, the gate re-derives.
- **Q-E1:** blocks numbered by ticket, never renumbered.
- **Q-DOC20:** cheat sheet LAST.
- No force push.

**OPEN (PROPOSED):**
- **Q-SEAT6:** reuse `.push-lock-e4` and the `*e4` tools, seat token `e6`, record folder `<UTC boot date>_seatE-6th`.
- **Q-WAIT6:** WAIT set unchanged: `-56`, `-f3`, `-g1`, `-d8` (`locke4.sh:275-:278`), with F 4th and G 2nd LIVE on their lanes' paths. STOP 16 per `locke4.sh:329`.
- **Q-ADOPT6:** adopt `s-e3-ks938` + its exact ref for ITEM 2 only.
- ~~Q-1256-FALLBACK (proposed)~~ **SUPERSEDED: RULED below** (RULED BY WEDNESDAY BEFORE SEND).
- **Q-ORDER6:** if the GO arrives mid-ITEM 1, finish the current step, then ITEM 2 (BLUF).

## RULED BY WEDNESDAY BEFORE SEND (2026-10-06 00:5x AEDT)
- **Q-1256-FALLBACK, RULED in advance:** if ITEM 1 (a) confirms that NO deliberate no-Redis configuration exists (your drafter found `fallbackMode` set at `redis.ts:78` during a long outage, with no production guard and no setting for running without Redis), then ruling 7's exception is EMPTY. Build (i) + (ii) + (iii), where (ii) = **503 while `fallbackMode` is active, whatever set it**: fail closed during an outage. (iii) stays: Redis up with the setting unset gives no restriction (Kam's card `secuura-connector-allowlist-missing-setting-ks1256-1005` = b). If ITEM 1 (a) finds a DELIBERATE no-Redis setting, STOP and mail Wednesday before building (ii). Either way, name the measurement in the READY.
- E 5th's handover `:280-:286` ('set in exactly one place') is FALSE at develop (`redis.ts:78` also sets it); `:16` names a stale develop (c5101866); `:126`'s `(Seat E 7th)` arm is superseded by STANDING_LINES `:407`/`:411` — test the UNTAGGED clause with `(Seat E 9th)` as this brief says.

Wednesday's re-read: Q-1256-FALLBACK made consistent across ITEM 1 (a), (d)(ii), OPEN and RULED; BLUF order == QUEUE order; provenance P4/P22-P25 filled from Linear.
SELF-CHECK: re-read end-to-end for contradictions | 2026-10-06 00:57
