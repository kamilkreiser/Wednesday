# NEXT SEARCH 2026-09-17o (22:19-22:43 AEST): Ornith queue empty; search at tip `bb848b828`

**BLUF: TWO TICKETS FIT: five inputs, all briefed, built with rc 0 and passed by the real checker. Nothing is queued.**

The tip moved: #1030 (KS-1211, vitest 4.1.11) merged at 22:18:52, so develop is `bb848b8283eb5ee6a6180067315b76f1321e7b6b`, not `0a2b1603f`. Every input below is built at `bb848b828`.

1. **KS-1152 record R1 (comment_patch, four one-file inputs, Polish).** Five comments cite `services/auth/src/services/jwt.ts:263` to show that a tenant-less user gets no `tenantId` claim, and quote the spread `...(meta.tenantId ? { tenantId } : {})`.
   - At the tip, `:263` is a blank line, and that spread belongs to the CONNECTOR minter (`:295`).
   - The access minter `generateAccessToken` (`:187`) copies `user.tenantId` as it is (`:201`). jsonwebtoken 9.0.2 drops a claim whose value is undefined; this was measured.
   - Each brief replaces the pointer with `generateAccessToken`. The wording around it is the brief-writer's.
   - Four sites are briefed. The fifth, `originate/src/routes/adminConfig.ts:1019`, is not, because the held READY_KS-730-B touches that file.
   - Every golden returns **PASS (9/9) strict**. The wrong variants fail at C6 (a kept line), C7 (a reworded line) and C4+C5 (a code token changed).
2. **KS-1219 (code_patch, AUTH / OAuth product fix + new test).** Briefed **only because nothing easier fit**.
   - A `scope` that arrives as an array (a repeated query parameter, a repeated form field, or a JSON array) reaches `parseScopeString`, where `.split` throws, and the endpoint answers 500 `server_error`.
   - Two insertions in `routes/oauth.ts`, after the GET and POST destructuring, answer 400 `invalid_request` instead.
   - The golden returns **PASS (7/7)**: R1, R2 and R3 red by assertion at the tip; auth suite 762 -> 767; tsc rc 0.
   - Eight wrong variants each fail at their gate.

**Queue lines (NOT added):**
```
KS-1152 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/comment_1152R1a.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/comment_patch/task.md ctx=65536
KS-1152 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/comment_1152R1b.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/comment_patch/task.md ctx=65536
KS-1152 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/comment_1152R1c.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/comment_patch/task.md ctx=65536
KS-1152 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/comment_1152R1d.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/comment_patch/task.md ctx=65536
KS-1219 input=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/code_1219.json task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md ctx=65536
```

## Wednesday must read

1. **The tip moved to `bb848b828` (#1030 merged).** The source checkout has the object, and every build used it. #1030's 27 lockfiles and `audit-baseline.json` no longer need partitioning.
   - A new PR **#1033** opened (KS-763 mysql2 override: root package.json and lock, originate package.json and lock, audit-baseline.json). This is Seat B's PR-7, now raised.
   - None of the five inputs touches its files.
2. **KS-1152 R1 is a partial.** Raise it as "Refs KS-1152 (R1, sites 1-4 of 5)".
   - The four inputs touch four different files, are independent and can run in any order.
   - The ticket names the new pointer target (`generateAccessToken`); the sentence around it is mine. The quoted connector spread had to go, because it is not the access minter's code.
   - **Knock-on:** the ks764 guard's own comment at `ks764-key-revoke-call-site-guard.test.ts:419-420` says the docblock "contains `{ tenantId }`". After R1a/R1b that describes history. Its `+` line would need backticks, so it is not briefed.
3. **KS-1219 is AUTH-tier product code (tier 1 at raise).** Raise it as "Refs KS-1219".
   - The ticket's recommendation also covers "any other non-string authorize parameter". Only `scope` was measured and fixed.
   - The guard sits in the handlers, as the ticket says ("before the resolver runs"), not inside `resolveAuthorizeClient`. Putting it in the resolver would reuse `invalid_request`, which the KS-822 F-8 source guard cannot see. That refactor is for a Claude seat, if wanted.
   - **Both product hunks end on ONE blank trailing-context line.** This is deliberate: the third line below each insertion (`:480`, `:634`) carries an em dash, and the brief says so.
   - If a model round fails A2 on context, read the `section_*` reanchor output before scoring it.
4. **The KS-1219 prompt is ~29.6K tokens.** At ctx 65536 that leaves ~36K for the answer; the test file is 147 lines.
5. **KS-1226 (the #1030 gate's F4+F5, filed 12:21Z) was checked, as the commission asked.**
   - F5 (the `:99` regex misses a "skipped" segment) is fit-shaped: one file, a spelled fix, and the gate's probe lines as cells.
   - But it lives in `systemTest/performance/tests/unit/utils/`. `build_input.sh` refused it with rc 2 at 22:33:01: "names no product file under services/*/src or packages/shared/src".
   - The ticket also bundles F4, which is a budget decision.
   - It unblocks when a systemTest tier exists (candidates "T2 tooling" = 0), or it goes to a Claude seat.

## FOUND

| ticket | verdict | why | instr |
|---|---|---|---|
| **KS-1152 R1 (4 sites)** | **FITS, briefed x4** | The recorded 21:26 lead ("FIT-SHAPED, NOT BRIEFED, stopped at four"). No partition on the four files; adminConfig.ts is excluded (READY_KS-730-B). | measured |
| **KS-1219** | **FITS, briefed (auth product, last)** | Today's #1026 gate F-10. One product file, fix spelled. 500 at the tip was reproduced for all three carriers. | measured |
| KS-1226 | refused | F5 is fit-shaped but in systemTest (the builder has no tier for it, rc 2); F4 is a budget decision in the same ticket. | builder rc 2 |
| KS-1225 | refused | "Decide the shape": add jsdom as an auth devDependency, or record the suite as root-only. A lock/manifest change. | read |
| KS-1224 | refused | "decide whether the exact KS-531 pin is now stale". A decision; manifests and locks. | read |
| KS-1223 | refused | "Owners measure it, then decide". Reachability not measured; two services (gateway strip + referral). | read |
| KS-1222 | refused | "The owners decide what the route should be" (make the upload screen reachable, or remove it); measure first. | read |
| KS-1218 | refused | "Either ... or" (a pick). The files are systemTest/schemathesis constraints.txt and a Python runner; no tier covers them. | read |
| KS-1216 | refused | "a measurement, not a fix": a runtime load trace in a built image. Severity unmeasured. | read |
| KS-1214 | refused | "Measure the deployed exposure first", and set priority from that. | read |
| KS-1208 | stands (17g/17h) | Updated 11:54Z with the #1028 N-1 comment, which widens the shape decision (401 vs encode/reject). Gateway `middleware/auth.ts` is in Seat A's live KS-1215 head. | read + measured (heads) |
| KS-1085 | refused | Updated 10:05Z. Launcher `Launch_Claude.command` (outside Blockchain/Dev, no tier); four findings plus a master-template pass. | read |
| KS-1221 / KS-1217 / KS-1220 | held | done.md PASS today; READYs exist. | read |
| KS-824 | stands (17h) | Re-screened because `services/oauth.ts` left Seat A with #1026. Still two files, five sites, and "measure which before choosing". | read |

**Screens:**
- Linear, 22:20:22: 48 KS issues created since 2026-09-16T14:00Z OR updated since 2026-09-17T10:00Z (2 pages).
- Linear, 22:32:40: issues created after 11:55Z, which found KS-1224, KS-1225 and KS-1226.
- Record check: `grep` of queue.md, done.md, candidates.md and briefs/* per id.

## TESTED

- **KS-1152 R1:**
  - **Premises:**
    - `premises.sh`, 22:25:32-22:25:36: `git grep -nF jwt.ts:263` finds 5 sites. Control: `generateAccessToken` count = 2. `jwt.ts` lines `:175/:177/:187/:263/:295` and `userRepo.ts:246` were printed.
    - jsonwebtoken probe, 22:24:07: undefined `tenantId` -> key absent; control present.
  - **Draft builds**, 22:26:32-22:27:49: rc 0 x4. R8 golden self-check PASS C4/C4b/C5/C6/C7; R9 none; R11 none.
  - **Checker** (sha256 `3c0fba34f310...`, unchanged across runs), 22:28:24-22:28:35: golden PASS (9/9) x4; `wrong_keep` FAIL C6; `wrong_para` FAIL C7; `wrong_code` FAIL C4+C5 (x4 each).
  - **Placed builds**, 22:30:17-22:32:05: rc 0 x4. **Checker on placed**, 22:32:12-22:32:19: golden PASS (9/9) x4; `wrong_code` FAIL x4.
  - **Shared suite** (farmed clone2, R1a+R1b+R1c applied): 44 files, **851/851 before and after** (22:29:38-22:29:47). Control: renaming `tenantId?: string;` under the new docblock reds the ks764 guard (1 failed / 15).
- **KS-1219:**
  - **Measured** in clone2 under `sandbox-exec` (off-host outbound denied), 22:35:50-22:36:32:
    - test alone: tip 3 red (R1-R3, by assertion), fixed 5/5;
    - EDIT 1 only: R2 and R3 red; EDIT 2 only: R1 red;
    - whole auth suite: tip 762/762, fixed 762/762 (test absent); fixed + test 767/767; tip + test 764/767 (R1-R3);
    - tsc rc 0 in every run.
  - **Draft build** rc 0 at 22:38:32. **Checker** (sha256 `b9fd00065fba...`, unchanged):
    - golden **PASS (7/7)**;
    - `wrong_getmissing` FAIL A3c; `wrong_blind` FAIL A4/A5/A6; `wrong_onegreen2` FAIL A4 (declared R3 not red); `wrong_r3string` FAIL A5/A6; `wrong_control` FAIL A4 CONTROL; `wrong_count` FAIL A4 COMPLETENESS; `wrong_extrafile` FAIL A3; `wrong_message` FAIL A3c.
  - **Placed build** rc 0 at 22:41:18. On the placed input (22:41:23-22:42:11): golden PASS (7/7); `wrong_blind`, `wrong_onegreen2` and `wrong_extrafile` FAIL at their gates.

## NOT TESTED

- No model round (nothing queued).
- The originate jest suite for R1b/R1d. C4 proves the token stream is unchanged, and no originate test reads those files as text.
- On KS-1219's placed input, `wrong_getmissing`, `wrong_r3string`, `wrong_control`, `wrong_count` and `wrong_message` were not re-run. They ran on the draft input, which differs only in P7.
- KS-1219 carriers for parameters other than `scope`, and the real auth app (the harness mounts only the router, with json + urlencoded).
- Whether a user row with a NULL tenant_id can exist today (DB). Only the KS-1152 pointer is corrected.

## HOW

- **Tip:** `ls-remote` of the source's origin URL from scratch clone `search17o/clone`, using the source's `core.sshCommand`: 22:20:13, 22:25:32, 22:41:09, 22:42:43. Source porcelain 0 each time.
- **Partition:**
  - `gh_prs.py` (REST GET): 21 PRs at 22:20:46; 22 at 22:42:43 (#1033 new).
  - `partition.sh`: 37 live seat heads, 26 differing paths (for-each-ref + three-dot + blob compare).
  - `ready.py`: 134 READY diffs, of which 45 are dated 09-17.
  - Builders' R9/R11 re-ran at build.
- **Git:** only read verbs ran on the source checkout. Every write verb ran in `search17o/clone` or `search17o/clone2`, both restored to porcelain 0. Test files were moved to `k1219/quarantine/`; nothing was deleted.
- **Scripts:**
  - `search17o/`: `setup.sh`, `tipcheck.sh`, `pool.py`, `gh_prs.py`, `linear_issue.py`, `ready.py`, `partition.sh`.
  - `k1152/`: `premises.sh`, `mkbriefs.py`, `mkouts.py`, `mkcode.py`, `clone2.sh`, `suite.sh`.
  - `k1219/`: `prep.sh`, `pre.sh`, `mkbrief.py`, `mkouts.py`, `runck.sh`.
- **Files written:**
  - `night/briefs/KS-1152-R1a.md`, `-R1b.md`, `-R1c.md`, `-R1d.md`; `night/inputs/comment_1152R1{a,b,c,d}.json`
  - `night/briefs/KS-1219.md` (sha256 `bb192a061c36...`); `night/inputs/code_1219.json` (sha256 `31c642f6d427...`)
  - the `## SEARCH 17o` block in `candidates.md` (backup `candidates.md.pre-2245-search17o`)
  - this report
- **Not touched:** `queue.md`, `night_run.sh`, the builders, the checkers. Nothing was pushed, commented, filed or mailed.
