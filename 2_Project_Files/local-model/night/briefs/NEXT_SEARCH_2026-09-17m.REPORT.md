# NEXT SEARCH 2026-09-17m (17:36-18:00 AEST): 17l's successor under the A4 all-declared-reds checker

**BLUF: ONE FIT, briefed and proven. Nothing queued. No second fit exists at the new tip `581c9db0d`.**
- **KS-1090 R2-3**: a test-only vitest pin in services/api-gateway. It checks that `x-gateway-vouch` (a bearer credential originate trusts) reaches originate and none of the other 17 proxy service keys. Tamper at `routes/proxy.ts:275`. **Ready to queue.**
- **Develop moved during the search:** `f8c7aaa39` became `581c9db0d` at 17:52:44 (**#1019 KS-1187 merged**: `proxy.ts` plus the ks1187 and ks843 tests). This moved the tamper line from `:274` to `:275`. The brief, the premeasures and every checker proof were **redone at `581c9db0d`**, and the input is pinned there.
- The checker's A4 now fails any declared red cell that stays green under the tamper. That was measured on this brief: the `wrong_onegreen` variant FAILS at A4 on both tips.
- The rejection table is appended to `night/candidates.md` as `## SEARCH 17m` (backup `candidates.md.pre-1800-search17m`).

## Wednesday must read
1. **The tip moved to `581c9db0d` (#1019 merged).**
   - The 17l READYs (KS-1123 `verification.ts`, KS-1205 `middleware/auth.ts`) are in files #1019 did not touch.
   - Any held input pinned at `f8c7aaa39` still runs at its own tip.
2. **KS-1090 is a split.** The ticket asks for "one change, one test pass". This brief is only R2-3 (the mint-scope pin).
   - R2-2 (a `tsconfig.test.json` plus a gate leg) is left out: no local-model tier grades it.
   - R2-4 is a record.
   - PR wording: **Refs KS-1090 (R2-3)**, never Closes.
3. **Partition at the new tip is clear by measurement.**
   - Now that #1019 is merged, no open PR names `proxy.ts` (21 open PRs at 17:54:10).
   - No live seat-A branch carries a different `proxy.ts` blob.
   - No 09-15/16/17 READY names it.
   - Seat B's new PRs #1021/#1022 touch lock files and `audit-baseline.json` only.
4. **A lead that cannot be briefed today:** the #1019 round-1 gate's **F-1019-2** says the router `caseSensitive` read is pinned by no cell (G-HARDFALSE gave 0 reds).
   - It is now on develop and would be a natural test-only pin.
   - It lives only on the PR, as a Record. KS-1187 is In Progress, so `build_input.sh` refuses it.
   - It needs a Backlog ticket or your ruling.
5. The builder's file name `ks1090-api-gateway-originate-tsc-never-type.test.ts` names the ticket's other half. Rename at raise.

## FOUND

| ticket | verdict | why | instr |
|---|---|---|---|
| **KS-1090 R2-3** | **FITS, briefed** | Stale refusal: 17d refused the WHOLE ticket ("no tier grades a config file; `gatewayProvenance.ts` in an open PR"), and 17l screened it at title level only. The R2-3 half is one new test file that touches neither. | measured, both tips |
| KS-1090 R2-2 / R2-4 | refused | A tsconfig plus a gate leg (no tier); a record. | read |
| KS-1210 (new) | refused | "Decide the shape before building": three owner questions on the OAuth product surface. | read |
| KS-1211 (new) | refused | Dependency pin bumps belong to Seat B (PRs #1021/#1022 are open). | read |
| KS-855 / KS-839 / KS-1202 / KS-1207 (updated) | refused | Held READY_KS-855; Kam ruled KS-839 option E and seat A builds it; KS-1202 and KS-1207 are seat A heads. | read |
| KS-530 / KS-528 (updated) | refused | Audit-row majors on Seat B's cards. | read |
| KS-1143 / KS-1144 | 17l reason **stale**, now refused on shape | `ks781-p3-3` no longer differs on any live head. But the test itself is the subject (the predicate and walk sit inside the test file, which exports nothing), the fixes are the gate's unratified proposals, and the file is far over the ~600-line modify-in-place limit. | measured + read |
| KS-1204 | refused | N-3 is test-only, but the #1014 GO ruled it a Seat A tier-1 PR together with a product guard. | read |
| KS-1205 other rows | stand | G-OAUTH is waiting on KS-1156 A.1 (unruled). G-UNKOPT is KS-1207's (still local). In G-JWTCATCH the hang-vs-401 behaviour is still an open question. F-4/F-5/N-2 are one PR after KS-1195's live sweep. | read |
| KS-1179 F-6 | stands | The builder slug collides with READY_KS-1179-F1's file. `ssrf-guard.ts` is a guard module. | read + tip read |
| KS-1185 F2/F3 · KS-1124 · KS-954 · KS-1125 | stand | KS-1185 F2/F3 are either/or picks. KS-1124 is prove-first plus options across several files. KS-954's mechanism is undetermined. KS-1125 needs a `Module._resolveFilename` fake `pg`, and ks949 pins only the file-based line. | read + git grep |
| KS-1118 / KS-1120 / KS-730 residues | stand | Held 09-15 READYs, test-header/comment rewrites, or files of held READY_KS-730-A/-B. | read |
| #1017 / #1019 / #1020 follow-ups | none briefable | #1017 went to KS-1205 (17l) and KS-1206 (a product edit in a READY file). #1019's Records are PR-only (item 4 above). #1020 went to KS-1209 (17l refused) and KS-1211 (Seat B). | read (verdict mails) |

**Pool counts and screens:**
- 328 KS Backlog/Todo at 17:38:12 (first:50, 7 pages, hasNextPage false) and at 17:38:21 (first:25 with comments, 14 pages, hasNextPage false).
- Since 17l, KS-793 and KS-810 left the pool; KS-1210 and KS-1211 entered.
- Updated after 06:20Z: 9.
- Unrecorded in every record file: 2.
- Test-gap wording screen over all 328 tickets: 72 hits. Screen over recorded multi-file / one-test-pass refusals: 10 hits. Every hit is either listed above or held/recorded with a reason that still holds.

## TESTED

Every run used the real `tasks/code_patch/checker.sh` or vitest under `sandbox-exec` (off-host outbound denied), in the scratch clone `/private/tmp/claude-501/night/s17m/clone`.

**At `581c9db0d` (final):**
- Premeasures:
  - tip: 4/4 green, tsc rc 0.
  - under the tamper: R1 and R2 red by assertion, CONTROL green, tsc rc 0.
  - the ticket's own `startsWith('vc')` example: R1 red, R2 green.
  - **gap:** the whole suite is 524/524 green under the tamper without the file, and 524/524 under the vc example.
  - canary: 7/524 red.
- Checker, draft input (fin2):
  - golden: **RESULT: PASS (7/7)**. A4: 2 failed / 4, BOTH declared reds by assertion. A6: 524 to 528, NEW reds []. A7: tsc rc 0.
  - `wrong_onegreen` (R2 probes only the spared mounts): **`FAIL A4 RED-FIRST: declared red cell(s) did NOT fail by assertion under the tamper — KS-1090 R2`**
  - `wrong_blind`: `FAIL A4 RED-FIRST` (not red, 0/4)
  - `wrong_product`: `FAIL A3 (test-only)`
  - `wrong_control`: `FAIL A4 … CONTROL`
  - `wrong_count`: `FAIL A4 … COMPLETENESS`
- Checker, placed input `night/inputs/code_1090.json` (fin3, 17:59:00-17:59:44): golden **PASS 7/7**; `wrong_onegreen` `FAIL A4`; `wrong_product` `FAIL A3`.

**At `f8c7aaa39` (before the move):**
- The same shape: gap 454/454 (vc example 454/454), canary 6/454.
- fin0 golden PASS 7/7 (A6 454 to 458), and the same five wrong variants failed at the same gates.
- fin1 on the then-placed input: golden PASS; `wrong_onegreen` `FAIL A4`; `wrong_product` `FAIL A3`.
- A guard reduced to `if (GATEWAY_VOUCH_SECRET)` gives tsc rc 2 (TS6133). That is why the tamper keeps `VOUCH_RECIPIENTS.has` in the condition.

**Instruments:**
- Checker sha256 `b1a5083fd6ac5611858cdd22e9e93ab47176e4fde20062169354358332efecb7`, identical before and after all 18 checker runs.
- `build_input.sh` sha `52afcfbdec99`, rc 0 on every build. The first draft build was refused for a missing `statement_ok:` clause; the clause was added.
- Source porcelain 0 at 17:36:41, 17:48:47, 17:53:55 and 17:59:58.
- Scratch clone untracked 0 after every run; leftover test files moved to `k1090/quarantine/`.

## NOT tested
- No model round (nothing queued).
- `wrong_blind`, `wrong_control` and `wrong_count` were not re-run on the final placed input (they were run on the draft input at both tips).
- The gate's 172-cell mount walk was not built. The pin drives one mount per key, so a widening keyed on a path rather than a key would not red it (stated in the brief notes).
- No live stack.
- F-1019-2 was not driven.
- KS-1125's fake-`pg` harness was not attempted.

## HOW
- **Tip:**
  - `ls-remote` of the source's origin URL from the scratch clone, using the source's `core.sshCommand`.
  - When develop moved, the new object was fetched into the scratch clone only (`fetch_new.sh`), then checked out by script (`checkout_new.sh`).
- **Partition, measured:**
  - seat A branches via `for-each-ref` + `merge-base --is-ancestor` + `diff --name-only`, a path counted only where the branch blob differs from the tip (`partition.sh`, `partition2.sh`);
  - #1019's `-U0` hunks against the tip;
  - open PRs by paginated REST GET (17:37:59 and 17:54:10);
  - 09-17 READY `+++` paths.
- **Linear:** GraphQL reads with the Secuura key read inside Python, never printed; counts from paginated pulls.
- **GitHub:** REST GET only.
- **Git:** no write verb against `!CODING`.
- **Scripts:**
  - `s17m/`: `setup.sh`, `partition*.sh`, `pool.py`, `poolfull.py`, `unrecorded.py`, `gapscreen.py`, `grep_rec.py`, `linear_issue.py`, `gh_prs.py`, `fetch_new.sh`, `checkout_new.sh`.
  - `s17m/k1090/`: `pre.sh`, `variant.py`, `mkouts.py`, `runck.sh`, `clean.sh`, `assemble.py`.
  - The brief header clock comes from `date`, and the fence is asserted equal to the golden test.
- **Files written:**
  - `night/briefs/KS-1090.md` (sha256 `23d199565f13…`, 243 lines)
  - `night/inputs/code_1090.json` (sha256 `9e063d050a16…`, tip `581c9db0d`, ~23.7K prompt tokens)
  - the `candidates.md` block (backup `candidates.md.pre-1800-search17m`)
  - this report
  - The superseded `f8c7aaa39` brief and input are kept in `s17m/k1090/` (`KS-1090.placed-f8c7.md`, `code_1090.placed-f8c7.json`).
- **Not touched:** `queue.md` (mtime 16:59), `night_run.sh`, `build_input.sh`, any checker. Nothing was deleted; nothing was sent.

## Queue line (NOT added; Wednesday appends)
```
KS-1090 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1090.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```
- **Raise:** "Refs KS-1090 (R2-3)", tier 2. Rename the file, for example to `ks1090-r2-3-vouch-reaches-originate-only.test.ts`.
- **Source-read at READY:** in checker.out, confirm that BOTH `KS-1090 R1` and `KS-1090 R2` are listed as assertion reds.
- **Rebuild pin:** `product=Blockchain/Dev/services/api-gateway/src/routes/proxy.ts ref=services/api-gateway/src/__tests__/ks1041-vouch-mint-scope.test.ts line=275 ctx=65536`
