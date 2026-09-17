# NEXT SEARCH 2026-09-17n (18:45-19:02 AEST): 17m's successor at tip `81ee4b729`

**BLUF: ONE FIT, briefed and proven. Nothing queued. No second fit exists at `81ee4b729`: 0 unrecorded tickets, 2 updated since 17:36 (both refused), and 20 of the 21 partition-freed hits still stand on shape.**
- **KS-938, the `routes/mfa.ts` half** (auth tier, one product file, a fix with a new test). Two places in `mfa.ts` turn MFA off by sending `mfaSecret: undefined` / `mfaBackupCodes: undefined`: the setup-failure revert (`:241-:242`) and `POST /disable` (`:376-:377`). `updateUser` skips any field set to `undefined`, so the TOTP seed and the hashed backup codes stay in the row. The brief changes both to `null`. **Ready to queue.**
- **Lead (a) is already done:** F-1019-2 was filed as KS-1212 (Backlog, 08:03Z) and is held as READY_KS-1212. **Lead (b)** KS-1209 is still refused. **Lead (c):** only KS-528 (Seat B) and KS-1212 changed after 17:36.
- The rejection table is appended to `night/candidates.md` as `## SEARCH 17n` (backup `candidates.md.pre-1901-search17n`).

## Wednesday must read
1. **KS-938 is a split. Raise it as "Refs KS-938", never Closes.**
   - The ticket's third site, `routes/users.ts:1111`, is in open PR #1018 (KS-1050) and seat A's head, so it stays open.
   - That fix is two lines plus the missing `mfaBackupCodes` key, and can follow once #1018 merges.
2. **The old hold.** `queue.md`'s old comment block lists KS-938/1006 under "security surfaces … kept for Opus builders".
   - Today's auth-tier opening covers one-file work with no decision, and this ticket's fix (`null` at each site) is spelled out by the ticket and by the #972 gate's F-3.
   - You decide whether the hold still applies.
3. **An A6 flake to expect.** fin0 (under load) failed A6 on one cell, `ks949-platform-admin-seed-identity`. KS-1053 records that cell as a ~1-in-7 flake.
   - The whole suite with the patch and test was 755/755 twenty-three seconds later.
   - fin1 and fin2 both passed 7/7.
   - If a model round fails A6 on that cell alone, re-run before scoring it.
4. **Behaviour change.** After a disable or a failed setup, `mfa_secret` and `mfa_backup_codes` are NULL. Raise tier: tier 1, because it is a credential-lifecycle write. The response and status codes do not change.
5. **Rename the test file at raise.** The builder named it `ks938-security-mfa-disabled-leaves-the-totp.test.ts`.

## FOUND

| ticket | verdict | why | instr |
|---|---|---|---|
| **KS-938 (mfa.ts half)** | **FITS, briefed** | Stale refusal. 17g refused it as "users.ts partition + open #1018, two files; unblocks: split per file". The `mfa.ts` half touches neither `users.ts` nor `userRepo.ts`. No open PR, live head or READY `+++` path names `routes/mfa.ts`. | measured |
| KS-1212 (lead a) | held | F-1019-2 is filed and already briefed, and READY_KS-1212 exists. | read |
| KS-1209 (lead b) | stands (17l) | 27 `fail=1` sites with no per-leg record (a design). `preflight.sh` is still carried by READY_KS-1040-part1. | measured paths + read |
| KS-528 (lead c) | refused | Updated 08:35Z with acceptance criteria for the react-router v7 frontend migration. That is Seat B's audit lane, and no tier grades it. | read |
| KS-837 | refused | Read in full for the first time: "Wednesday priced line 1 and ruled DO NOT BUILD IT NOW". | read |
| 20 other partition-freed hits | stand | Each has a recorded reason that holds whatever the partition. See the candidates block for the per-id reasons. | screened |
| KS-789 | not re-derived | A bash/doc rebrief is owed (two doc_patch FAILs on 09-16). | read (done.md) |

**Pool counts and screens:**
- 326 KS Backlog/Todo at 18:45:56 (first:25 with comments, 14 pages, hasNextPage false).
- Left since 17m: KS-1202, KS-1207, KS-1211. Entered: KS-1212.
- Unrecorded in every record file: **0**.
- A `caseSensitive` symbol search over all descriptions and comments: KS-1212 only.
- Partition-freed screen: **21** hits.

## TESTED

Every run used vitest, tsc or the real `tasks/code_patch/checker.sh` under `sandbox-exec` (off-host outbound denied), in the scratch clone `/private/tmp/claude-501/night/s17n.BNmw/clone` at `81ee4b729`.

**Premeasures:**
- **Tip:** R1 and R2 red by assertion, CONTROL and COMPLETENESS green, tsc rc 0.
- **Fixed:** 4/4.
- **One block missing:** without EDIT 1 only R1 is red; without EDIT 2 only R2 is red.
- **Only the two `mfaSecret` lines fixed:** both reds stay red.
- **Gap:** the whole auth suite is 751/751 at the tip AND 751/751 with the fix (test file absent). No existing cell pins either shape.
- **Canary:** a throw at `:376` gives 9 failed, 6 of them ks732 cells.
- **Whole suite with the test placed:** fixed 755/755; tip 753/755 (the two reds).
- **Received values at the tip:** R1 `[200,[[["mfa_enabled","verification_level","updated_at"],[false,"basic",USER_ID]]]]`. R2 is the same partial write after `400,2`.

**Checker, draft input:**
- **fin1 golden: RESULT: PASS (7/7).**
  - A3b `REMOVED_LINES 241,242,376,377` (line-keyed).
  - A4: 2 failed / 4, both declared reds.
  - A6: 751 to 755, 0 new reds.
  - A7: tsc rc 0.
- Wrong variants:
  - `wrong_partial`: FAIL A3b PARTIAL FIX (:241 :242)
  - `wrong_onegreen`: FAIL A4, declared red R2 did not fail
  - `wrong_blind`: FAIL A4, not red (0/4)
  - `wrong_control`: FAIL A4 CONTROL
  - `wrong_count`: FAIL A4 COMPLETENESS
  - `wrong_indent`: FAIL A3i INDENT SHIFT
  - `wrong_extrafile`: FAIL A3 (n=3)
- fin0 golden: FAIL A6 on the ks949 flake only (see item 3 above).

**Checker, placed input `night/inputs/code_938.json` (fin2, 19:00:57-19:01:40):**
- golden **PASS 7/7**: baseline 751/751, after 755/755.
- `wrong_partial`: FAIL A3b.
- `wrong_onegreen`: FAIL A4.
- `wrong_extrafile`: FAIL A3.

**Instruments:**
- Checker sha256 `b1a5083fd6ac5611858cdd22e9e93ab47176e4fde20062169354358332efecb7`, identical before and after all 12 checker runs.
- `build_input.sh` sha `52afcfbdec99`, rc 0 on both builds: 6 line-keyed sites (4 must_change), 4 expected `+` lines, 2 declared red cells.
- Brief: 0 non-ASCII characters; its fence equals the golden test.

## NOT TESTED
- No model round (nothing queued).
- `wrong_blind`, `wrong_control`, `wrong_count` and `wrong_indent` were not re-run on the placed input. They ran on the draft input, which differs only in the Premises and Notes sections.
- The `users.ts:1111` site was not driven: it is out of scope and partitioned.
- No live stack or real PostgreSQL. The UPDATE statement was read from the stubbed `query`, not from a database.
- Whether `POST /api/users/me/mfa/verify` actually re-arms a retained seed was not measured. That is the ticket's reasoning, carried as-is.
- The ks949 flake was not reproduced on purpose. Its attribution to KS-1053 comes from the cell name and the ticket's record.
- Of the 20 other partition-freed hits, none was re-read in full. Their recorded reasons were checked against the current partition only.

## HOW
- **Tip:**
  - `ls-remote` of the source's origin URL from the scratch clone, using the source's `core.sshCommand`.
  - Clone by `git clone --shared --no-checkout` + detached checkout, from `setup.sh`.
  - `prepare_clone.sh` rc 0.
- **Partition, measured:**
  - open PRs by paginated REST GET (`gh_prs.py`);
  - seat branches by `for-each-ref` + `merge-base --is-ancestor` + a blob compare on the checkout's refs (`partition.sh`; no worktree entered);
  - READY `+++` paths plus which READY new files are already at the tip (`ready.py`).
- **Linear:** GraphQL reads (`poolfull.py`, `linear_issue.py`) with the key read inside Python, never printed. Pool diffed against 17m by `pooldiff.py`.
- **GitHub:** REST GET only.
- **Git:** no write verb against `!CODING`. The checker leaves the patch applied in the clone, so `clean.sh` restored `mfa.ts` in the scratch clone only and moved the test file to `k938/quarantine/`. Clone porcelain 0 after every clean.
- **Scripts:**
  - `s17n.BNmw/`: `setup.sh`, `prep.sh`, `pooldiff.py`, `ready.py`, `partition.sh`, `screen.py`, `grep_rec.py`, `partscreen.py`, `tipcheck.sh`.
  - `s17n.BNmw/k938/`: `pre.sh`, `variant.py`, `mkouts.py`, `runck.sh`, `clean.sh`, `build.sh`, `assemble.py`, `runall.sh`, `runplaced.sh`.
  - The brief header clock comes from `date`.
- **Files written:**
  - `night/briefs/KS-938.md` (sha256 `2d334d0b8696…`, 311 lines)
  - `night/inputs/code_938.json` (sha256 `3d8326699ec1…`, tip `81ee4b729`, ~16.9K prompt tokens)
  - the `candidates.md` block (backup `candidates.md.pre-1901-search17n`)
  - this report
- **Not touched:** `queue.md`, `night_run.sh`, `build_input.sh`, any checker. No autostart or night-runner process was running (ps, 19:00). Nothing was deleted; nothing was sent.

## Queue line (NOT added; Wednesday appends)
```
KS-938 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_938.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```
- **Raise:** "Refs KS-938 (routes/mfa.ts sites)", tier 1.
- **Source-read at READY:** in checker.out, confirm `REMOVED_LINES 241,242,376,377` and that both `KS-938 R1` and `KS-938 R2` are listed as assertion reds.
- **Rebuild pin:** `product=Blockchain/Dev/services/auth/src/routes/mfa.ts ref=services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts line=376 ctx=65536`
