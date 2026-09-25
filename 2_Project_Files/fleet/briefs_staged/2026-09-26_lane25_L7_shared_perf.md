# LAUNCH BRIEF: Seat L7, Secuura/Blockchain. The packages/shared guards and systemTest/performance lane (round 25). From Wednesday

## BLUF
You are **Seat L7**, one of three parallel Claude BUILD seats in round 25 (B 29th, L7, L8). A fourth round-25 seat, **Seat M1**, only merges. **Seat L5 is still LIVE from round 24** on `Blockchain/Dev/scripts/**`. Your lane is the residue of Seat L6's round-24 lane, in two directory families no other seat touches:
- `Blockchain/Dev/packages/shared` (the tree-walking guard suites and one product file, `security/ssrf-guard.ts`);
- `systemTest/performance` (the k6 runner, the gate report and their unit suite).

It holds 9 tickets, easiest first. Five of them (KS-1314, KS-1315, KS-1316, KS-1318, KS-1319) were filed yesterday from the gate reports on L6's merges. The other four are the open residue of older tickets. Every change ends at **READY FOR QA**. You merge nothing without Wednesday's signed GO. **You deploy nothing.**
**Develop now:** `4db87c3e4b98b8e366c3dd60d5f399917bad5086`, read by the drafter with `ls-remote` at 03:37 and again at 03:44 AEST.

**Seat identity**
- Pane: `Secuura/Blockchain-C`.
- Inbox: `secuura-blockchain@agentmail.to`. It is SHARED by every Secuura seat (B 29th, L7, L8, M1 and the live L5). Mail tagged for another seat is not yours; filter on `(Seat L7)`.
- Tag every subject you send `(Seat L7)`.
- PROPOSED, for you to confirm in ITEM 0:
  - record folder `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-26_seatL7/`;
  - worktrees `s-l7-*` at the ABSOLUTE path `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/`, never under the clone (0 exist at 03:4x);
  - branches `feature/ks-<key>-<slug>-l7r25-<n>`. Use **`-l7r25-`, not `-l7-`**: an old origin branch `feature/ks-1153-l7-gate-records-…` already carries `-l7-`.

**Authority**
- Kam's week instruction (`WEEK-INSTRUCTION.md`, valid_until 2026-09-27): *"continue with the tickets, both local LLM and through the Claude agents"*.
- Kam's standing rule of 2026-09-13: as many agents as the code partition allows, with no two agents on the same code. Overnight is working time.
- Kam's open-ended TESTED grant of 2026-09-11 covers merges; Wednesday's GO naming the head SHA is the approval.

## READ FIRST
- Seat L6's handover, `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatL6-2026-09-25.md`: **read it WHOLE (120 lines).** Your lane is its residue. Three sections bind you directly:
  - §3: a tamper can fail three ways. It does not apply; it applies and is inert; or it is aimed at the wrong function. A `|| exit` guard catches only the first. **Expect a NAMED red, every time.**
  - §4: a control token written into a ticket is spent. Use a fresh one per filing round.
  - §8, the standing facts:
    - preflight 12/15 with legs 3/4/8 skipped is the standing verdict for test-only `packages/shared` changes;
    - a repo-root `systemTest/` push skips the preflight entirely;
    - install at `Blockchain/Dev`, not inside the member: `npm ci` in `packages/shared` exits 127 (KS-1317);
    - `npm run lint` in `systemTest/performance` runs TWO tsconfigs, and `tsconfig.json` excludes `tests`.
- `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md`. Apply: the five READY artefacts, INSTRUMENTS, the three-dot rule, the tamper-anchor rule, one red arm per conjunct, restoring disk modes after `git apply`, **re-key the PROSE in inherited tools**, and **a parser fix is tested against CAPTURED real output**. That last one governs items 7 and 9 outright.
- Seat B 28th's lesson (vault daily `/Volumes/DevMASTER/Notes (MASTER)/daily/2026-09-25.md`, "Lane complete — Seat B 28th"): **every cell that asserts an ABSENCE needs a control that proves the thing could have been present.**
- L6's tools, `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-25_seatL6/raise/`: `lock24.sh`, `push24.sh`, `push24_ff.sh`, `merge24.py`, and their proofs. Make NEW copies in your own folder. **L6's `merge24.py` hardcodes L6's own scratchpad as the default `MERGE24_SCRATCH`**; re-key it. B 28th's `merge24.py` (`…/2026-09-25_seatB-28th/raise/`) contains the READS of the predicted tree as well as the writes; prefer its containment.

## YOUR FILES / NOT YOURS
- **YOURS:**
  - `Blockchain/Dev/packages/shared/**`, except `package.json`;
  - `systemTest/performance/**`, except `package.json`, `package-lock.json` and the open-PR files below.
- **NOT YOURS, even though they sit inside your families:**
  - `systemTest/performance/tests/unit/support/capturedChildOutput.ts` and `tests/unit/utils/unitSuiteSlotIndependence.test.ts`. These are open PR #1245 (KS-1313, L6's cap round; Seat M1 merges it). The second file is also open PR #1241 (KS-1226), which stays OPEN and untouched; its disposition is not yours.
  - `tests/unit/fixtures/preSuiteStreams.test.ts`, `provisionDriftQuarantine.test.ts` and `provisionRedaction.test.ts`: open PR #989 (KS-973).
  - `packages/shared/package.json`: the no-package.json HOLD (dependabot #649, #635 and #575 also touch it).
- **NOT YOURS, other lanes:**
  - Seat L5 (LIVE): `.githooks/`, `Blockchain/Dev/scripts/**`, `deployment/azure/sync-secrets.sh`, `systemTest/__tests__/`;
  - Seat B 29th: `Blockchain/Dev/services/originate/`, `docs/openapi/`;
  - Seat L8: `services/vc-issuer/`, `services/kyc/`, `services/demo-service/`, `services/m365-integration/`.
- **Nobody's:** `scripts/preflight/`, `scripts/audit/`, `audit-baseline.json`, `.github/`, `systemTest/fixtures/` (#989), every other `services/*`, every `package.json` and lockfile.
- Any byte outside YOURS is a STOP.
- **Your guards read everyone's sources by TEXT.** ks860 reads listen calls in every test file, ks879 reads control bytes repo-wide, and ks781 reads api-gateway. Run each guard you change against the CURRENT develop, and say in the READY that a later merge from another lane can move its verdict. B 29th and L8 both add test files during your round.

## ITEM 0: PLAN CONFIRMATION, before ANY push
1. **Refuse the launcher's single-session pull**, and say so. Write nothing to the shared checkout `2_Project_Files` or its `.git`. The only exceptions are `worktree add` in your own namespace and a `git fetch origin develop` taken under `.push-lock-25`.
2. Re-measure develop with `ls-remote`. **The diff decides, not the SHA.** It will move: Seat M1 merges #1245 into your family if its cap gate says GO, and L5 and B 29th merge too.
3. Re-read every ticket you will touch, INCLUDING all of its comments. Sort comments client-side; never use `last:N`.
4. Send a QUESTION mail, topic `plan confirmation (Seat L7)`. It carries every launcher preflight warning VERBATIM, and answers:
   - **Q1** Your seat, pane, inbox filter, record folder and namespace. Confirm the launcher pull was refused.
   - **Q2** Your tools. Make new copies as `lock25.sh`, `push25.sh` and `merge25.py`. Re-key the namespace, the prose, the lock path (`.push-lock-25`) and the scratch default. The seat name must be a REQUIRED argument with no default, and no default may make a factual claim. Name push logs by head sha (KS-1323). Prove each tool before it guards anything:
     - a refusal AND a genuine pass;
     - containment on both sides (the shared delta is 0 AND the scratch store is non-empty).
   - **Q3** **The ks781 file carries three items** (items 2, 8 and 9: KS-1318, KS-1142, KS-1316). They are in `ks781-p3-3-body-parser-order.test.ts`: J2 at `:4982`, `CORPUS` at `:1900`/`:1977`, and `parserContinuations` at `:2447`. Propose the vehicle: sequential PRs, each branched from develop AFTER the previous one merges, or one PR carrying all three. Wednesday rules. **Never stack on an unmerged head without declaring the merged-blob equality target.**
   - **Q4** The PR grouping for everything else. Proposed: one PR per key. Wednesday rules.
   - **Q5** Item 5's scope (KS-1179). Measure and name what remains: F-5 (the deadline error text at `ssrf-guard.ts:605`); TYPECHECK-DEBT; N1 (the reachability overclaim in the comment); and N2 (a cell pinning a rejection the contract says never happens). Name every caller or test that matches the error TEXT before you change it.
   - **Q6** Item 9's shape (KS-1316). Either a fixture where an unreachable guard call reads `guarded: false`, or a line in the file recording why reachability is out of scope for a text-level walk. Say which, and why. The indirect-invocation false negative on KS-1143 is the OPPOSITE direction, and stays out of scope.
   - **Q7** Ports. You are not expected to need a database. **Your nominal range 55420-55429 is the SAME range the live L5 holds under its round-24 brief.** Do not bind any port without a mail first.
   - **Q8** Branch names and subjects, run through the hyphenated-key scanner AND the namespace-token scanner (see SHARED RESOURCES).
   - **Q-DEPLOY** You deploy nothing. Confirm.

   Proceed only on Wednesday's ANSWER.

## QUEUE
Scope is quoted from the ticket. Tier proposals are Wednesday's to rule.
1. **KS-1140, residue only** (In Progress). #1235 closed GF-1, and #1142 closed GF-2 and GF-4. The merge comment says *"GF-3 and R1 remain open"*. They are the docblock figures in `ks879-no-raw-control-bytes-repo-wide.test.ts`: `:43` "1,284 files, 12,758,153 bytes" and `:159` "(1,284 files / 12.8 MB". Restate the figures with the commit they were measured at, or drop them (the floors are `> 1,000` / `> 5 MB`). The change is comment-only. Tier 3.
2. **KS-1318** (Backlog). *"the combined cell asserts the **set of tags**, not the count — e.g. `toEqual([...])` against the three expected strings in source order"*. The cell is `ks781 :4982` `expect(defaultShapesOf(src)).toHaveLength(3)`. Red arm: make one branch emit another branch's tag; only the combined cell reds. Tier 2.
3. **KS-1315** (Backlog). *"each of the four sibling spellings has a row that reds under T-1"*, and *"each row's name is chosen so it is red before the fix"*. The four spellings are L05, L07, L04 and L01. File `tests/unit/runner/k6DockerRedaction.test.ts`. **Measure each row RED under T-1 before you claim it pins anything.** The unanchored `PASSWORD|SECRET|TOKEN` names are masked by accident. Tier 2.
4. **KS-1164, residue only** (In Progress; #1200 `4d8a5cc4e` merged the path derivation). The gate's REPORTPATH-SAMEPATH: *"refuse (or suffix) when `path.resolve(reportPath) === path.resolve(summaryPath)`; cell: the input bytes survive."* The definition of done also names *"the `k6_docker.ts` sibling handled the same way or recorded as accepted"*, now at `runner/k6_docker.ts:273`. A `systemTest/performance` product change. Tier 2.
5. **KS-1179, residue only** (In Progress; #1157, #1201 and #1224 merged). *"F-5 STILL OPEN — the deadline error text still reads (connect, transfer and drain) although DNS spends the same budget. TYPECHECK-DEBT STILL OPEN"*, plus the gate's N1 and N2 recorded at the #1224 merge. The scope comes from Q5. It touches the error text of a `packages/shared` product file (`security/ssrf-guard.ts`). Tier 2.
6. **KS-1319** (Backlog). Three items in the `walkTimeouts` pair: `src/__tests__/walkTimeouts.test.ts`, `support/walkTimeouts.setup.ts` and `vitest.config.ts:35`.
   - *"the wiring check cannot be satisfied by a commented-out line"*;
   - *"the derivation covers sub-directories and async tree-reading spellings, or names the spellings it deliberately does not cover"*;
   - *"TS1343 resolved or recorded as accepted"*.

   Report the machine's load (`uptime`) beside every run. **Time, not truth:** never loosen an assertion to fit a budget. Tier 2.
7. **KS-1314** (Backlog). Three items in the readYaml routing and canary family (`tests/unit/support/readYamlRouting.ts` and its cells):
   - *"`parserImportSites()` sees a multi-line parser import, with a positive-control row carrying the exact shape prettier produces"*. **Capture that shape from the package's own prettier, never write it by hand**;
   - *"a cell proves the loaders call `readYaml()`"*;
   - *"the canary keeps its guarantee without a per-run child spawn, or a line records why the spawn is the cheapest honest form"*.

   KS-1300 item 1 (READYAML-UNGATED) is NOT in scope, because wiring a suite into a gate touches the hook or the preflight. Tier 2.
8. **KS-1142** (Backlog). *"one literal imported by both … OR a cell in `entrypoint-corpus.test.ts` asserting CORPUS's package set ⊆ K1's literal"*. The files are `entrypoint-corpus.test.ts` (K1) and ks781 `const CORPUS = [` at `:1900` (`toBe(25)` at `:1977`). Locate by symbol, not by number. Regression: swap one CORPUS path's package for one K1 does not list; the new cell reds. **Keep K1's "reds on ordinary growth" property, and say it in the title** (R-2). Tier 2.
9. **KS-1316** (Backlog). *"a fixture where the guard call inside the continuation is unreachable reads `guarded: false`, **or** a line in the file records why reachability is deliberately out of scope for a text-level walk"*. The shape comes from Q6. This over-reports, which is the UNSAFE direction. Tier 2.

## EXCLUDED, AND WHY
- **KS-1313 / #1245:** L6's cap round, in gate24T2c; Seat M1 merges it or leaves it for Kam.
- **KS-1226:** item 1 (the 15 s budget) is a decision, and #1241 stays open, untouched.
- **KS-1300 item 1 (READYAML-UNGATED) and KS-1292:** each wires a suite or leg into the push gate, which is nobody's.
- **KS-1317, KS-846, KS-1154, KS-1216:** `package.json`, lockfile or runtime images, all under the HOLD.
- **KS-807:** a decision (scan raw bodies, or declare them out of the class).
- **KS-1141:** a QUESTION.
- **KS-953:** the class. Its instance (LEG D line pins) was fixed by #1215 (KS-1288).
- **KS-1098:** it stays open for Peter's name-set decision.
- **KS-990:** split to KS-994; no lint-only fix.
- **KS-1289:** `Blockchain/Dev/.dockerignore` changes every image's build context. That is a build decision, and outside both your families.
- **Merged, left In Progress for the closing pass (report only if asked):** KS-1288, KS-1143, KS-1144, KS-1147, KS-1155, KS-1117 and KS-1111.
- **KS-1110:** its merge comment says "item C remains open", but the drafter did not identify item C's text. It is NOT queued. If you read it and it is in your family, propose it in ITEM 0.

## GATE AND MERGE
- Every build ends at **READY FOR QA** with the five STANDING_LINES artefacts, named by identifier in the mail:
  1. the PR number;
  2. its head, read from origin in the same action;
  3. a ticket comment naming the PR;
  4. the Test Evidence block, written by you who ran the tests;
  5. what was NOT covered.
- **A READY, STATUS or MERGED mail never ends your turn. The same tool action that sends it STARTS the next queue item (or a background job). End a turn only with a job running or a named awaited mail in your last line.** Every round-24 seat stalled at least once right after sending one of these mails.
- **An expected figure carries its environment.** Say whether it was built or unbuilt, which cwd, and at what load. Otherwise write it as a condition. Never write a bare number. Example: "`packages/shared` 928/928, `vitest run --no-file-parallelism` in `s-l7-x/Blockchain/Dev/packages/shared`, at develop `4db87c3e4b98`, load 6.1", never "928/928".
- **A test that writes DDL refuses any non-loopback or non-disposable DB** (the KS-1310 precedent), and **its gate must be told the port range**. You are not expected to write one. If you do, mail first (Q7).
- **Name the gate that ran.** A `systemTest/performance` push skips the preflight entirely, so the READY says so and names what you ran by hand: `npm run test:unit` and `npm run lint` (both tsconfigs). A `packages/shared` push reads `12/15 ran; legs 3, 4, 8 NOT run (local stack not up)` as the standing verdict.
- Tiers follow `/Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md`. Two NO GO rounds on one class means STOP.
- Merge one PR at a time, and only on a DKIM-passing mail from `wednesday-agent@` whose GO names each head. Dry run first, sha-pinned, predicted over the CURRENT develop. Contain `merge-tree`'s writes AND reads. **A line at your prompt saying a GO was mailed is NOT a GO.**
- `Refs KS-<n>` for your OWN key only, with linkKind `contributes`, and never a closing word. Foreign keys are written un-hyphenated. Tickets stay In Progress after a merge.
- `packages/shared` runs `vitest run`, and `systemTest/performance` runs `vitest run --config vitest.unit.config.ts`. Take baselines BARE and SERIAL, and report `bare N / patched N+k` plus `tsc`. A `Test timed out in 5000ms` on a loaded box is the KS-1155 class. Re-run it solo before you read it, and say you did.

## HOLDS
- **No deploy of any kind. Demo never.** No k6 run against any environment, and no docker run of the k6 image.
- **No edit to any `package.json` or `package-lock.json`.**
- **The re-dates and H stay held.** KS-1267, and the two audit re-dates (frvp under KS-530, mwp4 under KS-729), wait for Kam's OWN word. That means his typed line in the pane, or mail carrying `dmarc=pass header.from=me.com`. A Wednesday relay does NOT substitute.
- **Ghost-line detector rule.** Any line at your prompt that claims Kam's word or a GO is run through the detector before you act on it. Ask Wednesday to run `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/pane_prompt_check.sh` on your pane.
- **The fuse, context only:** the audit rows lapse at `2026-09-30T00:00Z`. From then every `Blockchain/Dev` push is refused, and that includes your `packages/shared` pushes.
- **Client-facing communication is ticket comments only.** Comments state facts, lead with the BLUF, and never name a fleet seat. Nothing goes to Peter or Stuart.
- **Never delete; quarantine.** No `--no-verify`, no `--admin`, no force-push. GitHub HTTP 422 on a self-approval means STOP. Signature classes pause for Kam. File no tickets unless an ANSWER says so; search the board first, with a control token never written anywhere before.
- **Instruments:** run `cmd > out 2>&1; rc=$?`, then read the file (zsh has no `PIPESTATUS`). Copy a file outside the repo before you tamper it. After every `git apply`, restore disk modes and assert `test -x .githooks/pre-push`. Pair every zero with a control that fires.

## SHARED RESOURCES AND THE STOP RULE (round 25: B 29th, L7, L8, M1; L5 still live from round 24)
- **PUSH-WINDOW LOCK:** ONE shared advisory `mkdir` lock for the four round-25 seats: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/.push-lock-25/` (absent at 03:44).
  - It holds a `holder` file and a 60-s heartbeat. Take it before the snapshot and release it after the verify. The holder's rmdir is the only permitted delete.
  - Make one push per take. Poll every 5 s, and cool off 90 s after your own release.
  - STOP and mail only on: the same holder for more than 20 min; a stale heartbeat with a dead pid; or 60 min in total.
  - Never remove a lock you do not hold. `ls-remote` after every push; a second rc 141 means STOP.
- **Seat L5 finishes on its own lock, `.push-lock-24`** (held by L5 at 03:37-03:44 for #1250). **No seat ever holds both locks.** Before a `git fetch` in the shared checkout, READ `.push-lock-24`, never take it, and wait while it is held.
- **THE FLEET STOP COUNT, as a condition:** in YOUR worktree's own hook, on a `packages/shared` push, with `packages/shared` BUILT in that worktree:
  - `pre_push_hook_base` 28/0;
  - `fixture_guard` 6/0;
  - `run_shell_suites` 49/0;
  - shell suites 60 passed, 0 failed (of 60).

  With it UNBUILT, the same hook reads 59/1; that is an environment gap, not a STOP. **A `systemTest/performance`-only push prints none of it**, so never quote the count for one. A STOP is any other count, or a line that STARTS with `FIXTURE BUILD FAILED`. **L5's #1250 and #1253 change these numbers only after they merge**, and Wednesday re-declares the count then. On a STOP, do not retry: snapshot `for-each-ref` and `config --list --local`, and mail.
- **NAMESPACE TOKENS: unique, and not substrings of each other.** In round 24, `-r24-` matched L5's `-l5-r24-1`.

  | seat | worktrees | branch token | container | argv tag |
  |---|---|---|---|---|
  | B 29th | `s-b29-` | `-b29-` | `s-b29-pg-` | `-b29` |
  | **L7 (you)** | `s-l7-` | `-l7r25-` | `s-l7-pg-` | `-l7r25` |
  | L8 | `s-l8-` | `-l8r25-` | `s-l8-pg-` | `-l8r25` |
  | M1 | `s-m1-` | none (merges only) | none | `-m1` |
  | L5 (live, round 24) | `s-l5-` | `-l5-` | `s-l5-pg-` | `-l5` |

  - The drafter asserted that no token in the table is a substring of another (0 pairs).
  - `-l7-` alone matches an old origin branch (ks-1153), so it is NOT your token.
  - `-l5-` also matches an older ks-1152 branch that is not the live L5.
  - L6's `-l6-` and B 28th's `-r24-` belong to wrapped seats, and M1 now merges their PRs.
- **ATTRIBUTION BY NAMESPACE:** a foreign ref or worktree diff is another seat's only when BOTH hold:
  - its name matches that seat's row above;
  - origin holds your branch at your sha.

  Anything else is a STOP. L6's `s-l6-*` worktrees and branches are a WRAPPED seat's. Read them only.
- **BOARD GUARD:** a new attachment on another seat's key is theirs only when all four hold:
  - the URL is a project PR;
  - the head ref is `feature/ks-<same key>-…`;
  - the author is the board login within the round;
  - the change is addition-only.

  The only tolerated state change is the bot's Backlog → In Progress walk on PR open. Seat M1 moves KS-1313's state at #1245's merge; that move is expected.
- **PROCESSES:** kill by ancestry (`ps -o pid=,ppid=` filtered on your own claude pid), or by port plus cwd. Never kill by basename or command substring. Put `-l7r25` in long-running argv; your child-vitest matrices spawn many node processes.
- **DATABASES:** none expected (Q7).
- **Test by its handle:** in ITEM 0, name the instrument that tells "mine" from "theirs" for the inbox, `.git`, the process table, the board, the ports and the machine's load.

## WRAP
- **Wrap cold at ~80% context:** a HOLDING handover written to be read cold, with every open PR, head and next step.
- Before wrap: take the lock, `git fetch origin develop`, then `cat-file -t` the tip.

RULED BY KAM, NOT YET IN AN ARTEFACT (Secuura, `decision_queue.sh list ruled --undelivered secuura-`, read 03:45 AEST; 26 rows, filtered to this lane). You land none of them; context only.
- `secuura-audit-root-lock-0930-remeasured` => `a` (2026-09-25 12:12). This is the fuse above. It lands only in the re-date PRs, on Kam's own word.
- `secuura-agent-github-identity` => `identity` (not executed). This is why the self-approval 422 is mechanical.
- The other 24 rows do not touch `packages/shared` or `systemTest/performance`.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- **Preflight 12/15, legs 3/4/8 skipped, nothing failed, is the standing verdict for test-only `packages/shared` changes** (Wednesday to Seat L6, 2026-09-26). Do not start the stack; do not re-push for it.
- **#1241 is left OPEN;** no round 3 on it. KS-1313 is its residue, and #1245 is the cap round.
- **KS-1143:** the indirect-invocation false negative stays open and out of scope.
- **No merge-in** of develop into any PR branch. Squash subjects are the gate's ≤92-char lines. Squash bodies carry your own key only.
- **Leg 14:** a red that is not yours is re-run ONCE. A second red means STOP and mail.

## VERIFIED BEFORE SENDING (Wednesday's drafter, 2026-09-26 03:37-04:0x AEST)
PROVENANCE:
- origin develop `4db87c3e4b98b8e366c3dd60d5f399917bad5086` at 03:37:12 and again at 03:44:21 | `git ls-remote origin develop` on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-26
- board: Backlog 243 (P0 15 + P1 1 + P2 68 + P3 118 + P4 41), Todo 24, In Progress 195, total 462; an independent paginated GraphQL fetch returned 462 | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/board_count.sh linear LINEAR_API_KEY '<team KS, state …>'` + Linear GraphQL read-only, Secuura key | read 2026-09-26
- KS-1140 In Progress, 1 comment, last 2026-09-25 09:18 ("GF-3 and R1 remain open"); figures at ks879 :43 and :159 | Linear GraphQL read-only, `comments(first:50)` sorted client-side + `git grep -n` at 4db87c3e4b98 on /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files | read 2026-09-26
- KS-1318 Backlog, 0 comments; `toHaveLength(3)` at ks781 :4982 | Linear GraphQL read-only + `git grep -n` at 4db87c3e4b98 | read 2026-09-26
- KS-1315 Backlog, 0 comments; `tests/unit/runner/k6DockerRedaction.test.ts` present | Linear GraphQL read-only + `git ls-tree -r` at 4db87c3e4b98 | read 2026-09-26
- KS-1164 In Progress, 1 comment, last 2026-09-22 09:32 (REPORTPATH-SAMEPATH proposed); #1200 merged `4d8a5cc4e`; `path.join(…, scenario + '-gate-report.json')` at gate/report.ts:327; sibling `summaryMount.replace` at runner/k6_docker.ts:273 | Linear GraphQL read-only + `git log --grep` + `git grep -n` at 4db87c3e4b98 | read 2026-09-26
- KS-1179 In Progress, 1 comment, last 2026-09-25 07:18 (F-5 and TYPECHECK-DEBT still open; N1, N2 new); deadline text at ssrf-guard.ts:605 | Linear GraphQL read-only + `git grep -n` at 4db87c3e4b98 | read 2026-09-26
- KS-1319 Backlog, 0 comments; `setupFiles` at packages/shared/vitest.config.ts:35; walkTimeouts.test.ts and support/walkTimeouts.setup.ts present | Linear GraphQL read-only + `git grep -n` + `git ls-tree -r` at 4db87c3e4b98 | read 2026-09-26
- KS-1314 Backlog, 0 comments; tests/unit/support/readYamlRouting.ts present | Linear GraphQL read-only + `git ls-tree -r` at 4db87c3e4b98 | read 2026-09-26
- KS-1142 Backlog, 0 comments; `const CORPUS = [` at ks781 :1900, `toBe(25)` at :1977; entrypoint-corpus.test.ts present | Linear GraphQL read-only + `git grep -n` at 4db87c3e4b98 | read 2026-09-26
- KS-1316 Backlog, 0 comments; `parserContinuations` at ks781 :2447 | Linear GraphQL read-only + `git grep -n` at 4db87c3e4b98 | read 2026-09-26
- cross-referenced keys: KS-1300 In Progress (last 2026-09-25 15:35), KS-1143 In Progress (last 15:35), KS-1155 In Progress (last 17:18), KS-1144 In Progress (last 17:18), KS-1111 In Progress (last 15:35), KS-1226 In Progress (last 12:42), KS-1313 In Progress (last 15:46) | Linear GraphQL read-only, `issue(id:…)` | read 2026-09-26
- none of the queued tickets is assigned to Peter or Stuart (20 of 462 are) | Linear GraphQL read-only, assignee field | read 2026-09-26
- excluded tickets KS-1313 KS-1226 KS-1292 KS-1317 KS-846 KS-1154 KS-1216 KS-807 KS-1141 KS-953 KS-1098 KS-990 KS-1289 KS-1288 KS-1147 KS-1117 KS-1110 read for their blocking condition | Linear GraphQL read-only, Secuura key, descriptions + last comments | read 2026-09-26
- open PRs 29 (10 dependabot, manifests and lockfiles only); #1245 head `65eb964271b0` touches tests/unit/support/capturedChildOutput.ts and tests/unit/utils/unitSuiteSlotIndependence.test.ts; #1241 the second of those; #989 three tests/unit/fixtures tests plus systemTest/fixtures; no open PR touches a packages/shared source | GET https://api.github.com/repos/Secuura/Distributed_Secuura/pulls?state=open + /pulls/<n>/files + `git ls-remote origin refs/pull/1245/head` | read 2026-09-26
- L6's handover (120 lines; tamper shapes, spent controls, standing facts) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/HANDOVER-seatL6-2026-09-25.md | read 2026-09-26
- L6's merge24.py defaults `MERGE24_SCRATCH` to L6's own scratchpad and takes a REQUIRED `--seat` | `sed -n 1,40p` of /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-25_seatL6/raise/merge24.py | read 2026-09-26
- preflight 12/15 standing verdict for test-only packages/shared | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_answer_seatL6_lane-complete.md | read 2026-09-26
- `.push-lock-25` absent; `.push-lock-24` held by "Secuura/Blockchain L5" pid 83976 since 17:37:13Z | `ls -la` + `cat holder` /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/ | read 2026-09-26
- 0 worktrees and 0 origin branches carry `s-l7-` or `-l7r25-`; `-l7-` hits 1 old origin branch (ks-1153); the token table has 0 substring pairs | `ls` of worktrees/ + `git ls-remote --heads origin` (626 heads) + python pairwise check | read 2026-09-26
- L5's round-24 brief allocates it 55420-55429 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_lane24_L5_scripts.md (Q7) | read 2026-09-26
- STOP count 28/0 + 6/0 + run_shell_suites 49/0 + 60 of 60, unchanged while #1250/#1253 are held; unbuilt packages/shared 59/1 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_FIX_seatL5_batch1249.md + /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-26_lane24_L6_shared_perf.md | read 2026-09-26
- undelivered Secuura rulings, 26 rows | `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh list ruled --undelivered secuura-` at 03:45 | read 2026-09-26
- week instruction valid_until 2026-09-27 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/tasks/WEEK-INSTRUCTION.md | read 2026-09-26
- as-many-agents-by-code-partition rule | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-13_as-many-agents-as-possible-partitioned-by-code.md | read 2026-09-26
- detector present | `ls -la` /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/cockpit/pane_prompt_check.sh | read 2026-09-26

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-26 04:04
