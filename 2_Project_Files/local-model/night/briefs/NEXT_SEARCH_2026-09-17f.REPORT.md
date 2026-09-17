# NEXT SEARCH 2026-09-17f (12:13–12:24 AEST): widening past SEARCH 17e

**BLUF: ONE FIT: KS-1156 part B, record R-C2, as a partial.** It is test-only vitest: one NEW 111-line file in `services/auth/src/__tests__/`. The tamper is the AUTH4 gate's T6, planted at `routes/auth.ts:677`: the refresh guard's `authMethod === 'oauth'` arm is dropped. **The real `checker.sh` gave RESULT: PASS (7/7), strict, twice** at develop `d7e95cd9f`, on the placed input. A wrong variant gave **RESULT: FAIL (1 failed), at A4 RED-FIRST**. Nothing was queued.
- **Why it fits:** the whole services/auth suite stays **751 / 751 green** with that arm dropped. A positive control shows the suite does see the other arm: dropping the `client_id` arm reds ks1151 cell 3.
- **Kam's week grant:** the diff touches no product file, so this is a test-only pin on an auth surface, which the grant allows.
- **No second fit exists in the widened pool.** Only 3 older tickets moved after their recorded refusal (KS-1156, KS-1198, KS-588). The two new unrecorded tickets filed today (KS-1205, KS-1206) are rejected, with reasons in `candidates.md` SEARCH 17f.
- **Wednesday must read before queuing:** see the next section.

## Wednesday must read before queuing

1. **Auth surface.** KS-1156 is on the census's "auth-shaped title (LAST)" list, and its guard is the OAuth refresh launder guard (KS-1151).
   - This task edits no product file; the checker's A3 enforces that (`the product file is untouched`).
   - It fits the "test-only pins on those surfaces are allowed" clause. Confirm that auth-LAST does not hold it back (the same question as the KS-744 item 1).
2. **Partial.** The PR says "Refs KS-1156 (B, R-C2)", never Closes. Still open on the ticket:
   - A.1: the limiter label set, a DECISION. KS-1205's G-OAUTH row asks the same question.
   - A.2 and A.3: comment edits.
   - R-C1 / C3: see item 4.
   - R-C3: wording, the owner's call.
   - C: deployment-side, Kam's.
3. **The ticket wording deviates on file location.** The Definition of done says to add the cells "to the ks1151 file". The brief puts them in a NEW file, as in the KS-1199 precedent. If Kam wants them inside ks1151, that is a modify-in-place re-brief. ks1151's titles are ASCII, so the emoji-title trap does not apply.
4. **Bonus witness, not graded.** Under T5 (the guard MOVED below `getSession`, the R-C1 regression), R1 and control 1 both red by assertion: `expected [ 401, false, [], +0, [ 'sess-x' ] ] to deeply equal [ 401, false, [], +0, [] ]`.
   - So the file also pins "no session lookup on a refusal" for OAuth tokens.
   - A move is not a one-line tamper, so the checker cannot grade it.
5. **The file name is the builder's slug:** `ks1156-auth4-gate-records-983-r2-984.test.ts`. It was chosen so the prompt carries one path (the 17b finding 2 trap). Rename at raise if you want a descriptive name.
6. **Line pin.** The input pins tip `d7e95cd9f` and tamper `line: 677`.
   - A later `routes/auth.ts` edit above `:677` (for example KS-1157, the OAuth session marker, Backlog) makes a REBUILD refuse on the `from` mismatch, which is fail safe.
   - The prebuilt input keeps working at its own tip.
7. **T7 note.** The case-broken tamper (`'OAuth'`) also reds R1, and it is ALSO caught by project tsc (rc 2). T6 is not caught by tsc (rc 0), so T6 is the tamper the checker uses.

## The queue line (NOT added)

```
KS-1156 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1156.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```

To rebuild instead, use these pins (all required): `product=Blockchain/Dev/services/auth/src/routes/auth.ts ref=services/auth/src/__tests__/ks1151-auth-refresh-refuses-oauth-token.test.ts line=677 ctx=65536`.

## Files

| file | sha256 | note |
|---|---|---|
| `night/briefs/KS-1156.md` | `0288aa20af8e40765c1e05aee5189b4953767c5e0dc0305ec8e22d6bfe50b182` | 225 lines, 0 backslashes, fence == golden (python equality, True) |
| `night/inputs/code_1156.json` | `ac9ef664f4bd35ef90c7d011f30375958df942af7400f0d24e3cc1ba201d1cee` | `build_input.sh` rc 0 at 12:22:06, tip `d7e95cd9f`, ~25.8K prompt tokens, ctx 65536; 4 Where sites (0 must_change), 1 red cell, tamper + `statement_ok` parsed; `suggested_test_file` == brief path. Same sha after fin2 (12:23:37). |
| golden test | `2ae3c0a30297b83e…` | `/private/tmp/claude-501/night/s17f_1156/golden.test.ts`, 111 lines, 0 non-ASCII / backslash / `$` / backtick / double quote |
| `candidates.md` | backup `candidates.md.pre-1224-search17f` | SEARCH 17f block appended in an HTML comment by `.new` + `mv`; one code span re-set by a second `.new` + `mv` (a heredoc backtick had eaten it) |

- Scratch dir: `/private/tmp/claude-501/night/s17f_1156/`. It holds:
  - scripts: `clone.sh`, `runvt.sh`, `tampers.py`, `tampers2.py`;
  - outputs: `tampers.r1.out`, `tampers.r2.out`, `runs/`, and the checker rounds `fin1/`, `fin2/`, `wrong1/`;
  - `aside/`: the premeasure copy and the three checker-applied files, moved out of the clone.
- Linear, GitHub and analysis files are in the session scratchpad `…/a5010d5c-…/scratchpad/s17f/` (`ks_bt.json`, `rows.json`, `analyse.py/.out`, `prs.json`).
- Nothing was deleted.
- **Not touched:** `queue.md` (mtime 12:05, before this search), `done.md`, the checker, the builders, and other briefs. No Linear or GitHub write, no mail, no commit.

## FOUND / TESTED / HOW

**FOUND (pool and predicate)**
- **Pool:** **327** KS tickets in state Backlog or Todo. Instrument: Linear GraphQL, `first:50` paginated until `hasNextPage` was false, 12:13:40–12:13:44.
  - `board_count.sh linear LINEAR_API_KEY '{ team: { key: { eq: "KS" } }, state: { name: { in: ["Backlog","Todo"] } } }'` exited rc 1 with "MORE PAGES EXIST — this is not a total" at its first:250 page.
  - So **327 is the paginated count, not a board_count total.**
- **Widening predicate:** a pool ticket named in a recorded refusal, whose `updatedAt` is later than the end clock of its LATEST refusal. The refusal blocks were:
  - git `3e68f4132`: T1 18:0x, 20:07–20:40, 21:0x–21:31, SEARCH 2 22:37;
  - reports 17 / 17b / 17c / 17d;
  - SEARCH 17e 11:29;
  - ROUTED 12:07.
  - **Result: 3.** KS-1156 (01:36:59Z), KS-1198 (01:37:00Z), KS-588 (01:45:04Z).
- **Census T1 rows:** 28 checked, **0 moved.**
  - Positive control: the same detector flags those 3.
  - A variant keyed on the EARLIEST refusal flags 10. The 7 extra (KS-1129, 1175, 772, 1173, 744, 1180, 960) were each re-refused or held by a later block.
- **Set-aside rows:** 0 updated past their recorded date.
- **Filed since 2026-09-16 12:00Z with no block:** KS-1205 and KS-1206. KS-1207 is ROUTED.
- KS-789 appears in no block. It is the owed bash rebrief (T2b), outside this widening, and was not read.

**TESTED (KS-1156 R-C2)**
- **Scratch clone:** `clone --shared` plus `checkout --detach d7e95cd9f`, run from a script file (12:17:49–12:17:52), then `prepare_clone.sh` rc 0 (12:19:22). All vitest and checker runs were under `sandbox-exec nonet.sb`.
- **Gap, T6 with the new file absent:** 62 files, **751 / 751 green**; project tsc rc 0 (12:19:50–12:20:05).
- **Positive control, CLIENTARM with the new file absent:** 750 / 751. ks1151 cell 3 fails with `expected 200 to be 401` (12:20:42–12:20:46).
- **New file at the tip:** 3 / 3 (12:19:37 draft; 12:20:50 final).
- **New file under each tamper** (anchor count 1; blob restored == `18946cd7c` after every row):

| tamper | result |
|---|---|
| T6 | 1 / 3 failed, R1 by assertion: `expected [ 200, true, [ 'sess-x' ], 1, …(1) ] to deeply equal [ 401, false, [], +0, [] ]`; controls green |
| T7 | R1 red; tsc rc 2 |
| CLIENTARM | 3 / 3 green |
| T5 (move) | R1 + control 1 red |
| INERT | 3 / 3 green |

- **Whole suite with the golden:** 63 files, **754 / 754** (12:20:46–12:20:50).
- **Checker `sha256 553aafe0…`:** identical at 12:17:25, before and after each of the three rounds. It did not change during this run.

**fin1** (placed input, 12:22:33–12:22:49), verbatim:
```
mode: test_only (tamper at Blockchain/Dev/services/auth/src/routes/auth.ts:677)
PASS A1 output is exactly one fenced ```diff block, nothing outside it
baseline suite rc=0 total=751 passed=751 failed=0 suites_failed=0 loaded=1 failed_names=[]
PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)
PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/auth/src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts } — the product file is untouched, as the ticket requires
A3b: no must_change sites in the input — skipped
PASS A4 RED-FIRST: src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts fails at the untouched tip (1 failed / 3 run; controls green; assertion reds)
PASS A5 GREEN-AFTER: src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts passes with the product hunk (3 passed / 3 run)
after suite rc=0 total=754 passed=754 failed=0 suites_failed=0 loaded=1 failed_names=[]
NEW reds: []
PASS A6 whole services/auth suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)
INFO tsc on the test file alone: rc=0 (0 lines; not gated — vitest does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=1 +111/-0 test=src/__tests__/ks1156-auth4-gate-records-983-r2-984.test.ts red_first=yes apply_mode=strict
RESULT: PASS (7/7)
```
- The checker-applied file was byte-identical to the golden (`cmp`).
- **fin2** (the same placed input, 12:23:21–12:23:37) printed the same PASS lines and `RESULT: PASS (7/7)`.

**wrong1** (12:22:56–12:23:12): the variant's `labelOnlyToken` drops `authMethod` instead of `client_id`, and its fixture expects are swapped to match. That makes a client_id-only token, which ks1151 cell 3 already pins. Verbatim:
```
FAIL A4 RED-FIRST: the test file is NOT red at the untouched tip (rc=0, 0 failed / 3 run) — it does not prove the defect
RESULT: FAIL (1 failed)
```

**NOT tested**
- The model run itself.
- The raise.
- The T5 row through the checker (a move is not a one-line tamper).
- Whether ks1151's own cells would also be wanted as in-place edits.
- KS-1205 / KS-1206 were not pre-measured beyond reading two tip lines: `middleware/auth.ts:300` builds `rateLimitBucket`, and `adminConfig.ts:946` is `${d.rateLimit || 1000},`.
- Secuura porcelain was read at 12:17:52 and 12:24:02 only (0 both times).

**HOW (partition, measured)**
- **Open PRs (GitHub REST pulls + files, paginated, 12:16:46–12:16:56):** 20 PRs / 102 paths.
  - **0** paths name `services/auth/src/routes/auth.ts`, `ks1151`, `ks1156` or `services/auth/src/services/jwt.ts`.
  - Controls: 60 `package.json`; 5 `services/auth/` paths (#1018 users.ts + its test, three dependabot `package.json`).
  - Also 0 PR paths name `adminConfig.ts`, `rateLimitEnforce.ts` or `middleware/auth.ts`.
- **READY diffs:** 0 `+++ b/` on `routes/auth.ts` or `ks1151` (control: 10 READYs touch `services/auth/`).
- **Staged Wednesday briefs:** KS-1156 appears only as a filed record (s225/s228 09-14); no lane owns it.
- **Partition list in the commission:**
  - `routes/auth.ts` in services/auth is not `middleware/auth.ts` (api-gateway), `users.ts` or `userRepo.ts`.
  - The test is not a proxy, admin or verification file.

## Tip

- `d7e95cd9f153e9036ed77935a73c93504fa6e3dc`, read by `git ls-remote origin develop` (ssh origin, from the Secuura checkout, a read verb) at 12:14:05 and 12:23:59, and by the builder at 12:19 and 12:22. It did not move.
- `cat-file -t` = commit, so the object is local.
- The commissioned anonymous `git ls-remote https://github.com/Secuura/Distributed_Secuura.git develop` gave rc 128, `Repository not found` (a private repo).

## Rejections (the rows are in `candidates.md` SEARCH 17f)

| ticket | verdict | reason |
|---|---|---|
| **KS-1156 B R-C2** | **FITS (briefed)** | above |
| KS-1156 A.1 | REFUSED | The label set is the ticket's own "decided" item, so it needs a decision. |
| KS-1156 A.2 / A.3 | REFUSED | Comment-only edits; no cell reds them. |
| KS-1156 R-C1 (C3) | NOT BRIEFED | T5 is a move; the R-C2 file already reds under T5. |
| KS-1156 R-C3 / C | REFUSED | Owner's call / Kam's deployment-side. |
| KS-1198 | REFUSED (reason stands) | It moved only by KS-1205's relation; still `middleware/auth.ts` (partition) with two shapes. |
| KS-588 | REFUSED | Assignee peter@obeden.com. |
| KS-1205 | REFUSED | **Product rows:** `middleware/auth.ts` (KS-1207 partition) + `rateLimitEnforce.ts`, "one tier-1 PR … after KS-1195's live sweep". **G-OAUTH:** pins what KS-1156 A.1 has not decided. **G-UNKOPT:** KS-1207's subject. **G-JWTCATCH / G-BUCKET-*:** plant in `middleware/auth.ts` (the bucket is built at `:300`). **R-2:** no spelled fix. |
| KS-1206 | REFUSED | **File:** `adminConfig.ts` carries the held, unmerged READY_KS-730-B (0 KS-730 commits on develop). **Fix site:** a validation block ahead of a SQL template (`:946`). **Open choices:** 0/absent is a pick; "decide whether this mint should take a connectorId" is a decision. **Surface:** API-key credential mint. |

## Deviations and findings

- **`board_count.sh` cannot total this pool.** Linear caps `first` at 250 and the script pages once, so on any KS Backlog/Todo pool over 250 it can only refuse. It refused correctly; the paginated pull is the count used. Worth a paging loop (not edited: `fleet/` is outside this commission).
- **Heredoc trap (mine, fixed):** an unquoted heredoc ran a markdown backtick span as a command substitution (`bad substitution`) and blanked one code span in the 17f block. It was re-set by `.new` + `mv`. The backtick count was 86 before and after the append, so no other span was affected.
- **Clock:** the brief header says 12:21 (from `date`). `new_brief.sh` was not used: its skeleton is the code_patch shape, not the test-only new-file shape (the same deviation as KS-1199).
- **Brief P5's T6 row ran on the first draft.** It differed from the final only in control 1's title and message; fin1 and fin2 re-graded T6 on the final bytes.
- **No `cd`** in any command or script. vitest ran with `--root` and tsc with `-p`.
- **Processes:** every vitest, tsc and checker run was foreground and exited. None was left running (`pgrep -fl s17f_1156` empty at 12:24:02).
