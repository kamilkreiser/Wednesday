# Spark operator 95 - report (2026-11-03, 14:20-15:15 AEDT)

Base: develop 27fe5476526c (ls-remote re-read 14:2x). It moved to 67309f28ab21 at ~14:55 (PR 1984 merge: referral/referrals.ts, its test, two fragments); none of the 8 files nor their tests are among them, so no brief drifted.
Own clone: `repo/` here (clone of the Spark cache, checked out at 27fe547; gitignored). `!CODING` was only read (ls-remote). The checkout is shallow and lacks the tip, so briefs read via the cache clone.

## Sites screened
Screen = operator 94's `screen.py` over Blockchain/Dev/services plus a variant over packages/frontend/scripts, regex on `instanceof Error ? x.message : String(x)` / `err.message` / `String(err)`; 44 unheld, PR-free hits in services plus 15 in packages/frontend/scripts. Excluded first: held_paths.out (833 READY files, 493 paths), open-PR files, seat files.
CHOSEN (8; one product file each, runnable in-process test, fix shape in brief):
- p1 originate/repositories/lifecycleEventRepo.ts createLifecycleEvent catch (jest, db injected)
- p2 originate/repositories/shareRepo.ts createShare catch (jest)
- p3 demo-service/routes/reset.ts POST /reset catch (vitest, handler read off router.stack)
- p4 demo-service/services/resetService.ts resetDatabase + resetRedis catches (2 hunks, vitest)
- p5 auth/services/email.ts getAcsClient init catch (`${err?.message}` in a template; the two send catches already guarded)
- p6 packages/shared prism/identus-client.ts resolveDID catch
- p7 packages/shared resilience/service-client.ts healthCheck catch
- p8 packages/shared vc/verifier.ts verifySignature OUTER catch (inner Ed25519 catch deliberately untouched, not reachable by a resolver rejection)
EXCLUDED (reason):
- referral/routes/referrals.ts: PR 1984 / seat F 26th. Seat files (api-gateway security.ts, rateLimitEnforce.ts, services/redis.ts, anchoring threadTokenIndex.ts, scripts/restore-local-secrets.sh): none appeared as candidates; all would have been dropped by the held/PR filters or are not instanceof-coercions.
- api-gateway health-dashboard.ts / system-status.ts: the checks are module-private and only reachable through the real app (heavy ks1101 harness); not in-process-cheap.
- originate platformOrganizations.ts (3 sites): needs authenticate/requireRole + erase stack mocks; originate gdpr.ts and api-gateway notifications.ts: already carry the KS-1772/1771 describe guard.
- auth issuerCert.ts, auth cip8.ts, kyc entra-client, tokenisation index.ts, vc-issuer index.ts, billing/auth/prism index.ts: hostile throw cannot be injected without mocking crypto/cardano libs, or the file starts a server at import.
- services/shared redis-security-store.ts: no test harness in that tree (separate from packages/shared).
- nft.routes.ts (15 sites), transfer delegations/workflows (`error instanceof Error` only, no message read), referral/originate errorHandler (err is always an Error): not the KS-1868 shape or too wide for one pass.
- everything with a HELD pass in held_paths.out (originate index/errorHandler/lifecycle sites of 94 etc.).

## Open-PR exclusion list and instrument
`gen/prscan92.py` (copied from operator 94): GitHub REST API read-only with the project's token (Blockchain 4_Credentials/.env, GH_TOKEN), pulls?state=open then pulls/N/files. Result 14:2x: 23 open PRs, 124 file entries, saved `open_prs_start.json`. Planted control (services/originate path present in PR files): 5 entries found, so the scan can see. None of the 8 product files nor the 8 new test file names is in it. Held-READY instrument: `gen/heldlist.py` over night/READY_*.diff.md (ls of named dir) -> held_paths.out.

## Rounds (done.md times)
CONTROL (all CONTROL-PASS, golden BYTE-IDENTICAL, first time): p1 14:39:58 (354s incl. wait for a hand-run round), p2 14:43:01, p3 14:44:33, p4 14:45:37, p5 14:48:19, p6 14:50:04, p7 14:51:20, p8 14:53:09.
MODEL (queued only after its own CONTROL row, by advance95 in loop95): p1 14:57:05, p2 15:00:39, p3 15:02:38, p4 15:04:22, p5 15:07:49, p6 15:09:47, p7 15:11:29, p8 15:13:18. All PASS (7/7), golden BYTE-IDENTICAL, 100-234 s round, 30-45 s model time, tokens ~10-28k in.
dry-run + lint of all 8 rc 0 before queueing. No FAIL, REFUSED or BUSY-terminal round of mine; one transient BUSY (waited for another hand-run round; queue kept the line).

## HELD (READY files in local-model/night)
READY_KS-1868-KS-1868-O95-P1 ... P8 (`_spark-dsv4flash_BRIEFED-CODEPATCH2-<LABEL>-PASS-7of7_2026-11-03.diff.md`), labels in labels95.txt. hold_ready.py figures: each touched=2, red = half the cells (the R cells fail at the tip), green all, strict apply True; suite deltas originate 2385->2394 and 2390->2394, demo-service 103->107 / 103->111, auth 1623->1627, shared 1447->1451 (x3). Pre-existing originate suite reds (11) are unchanged baseline-vs-after (A6 no new red).
How verified: the patches are byte-identical to my goldens; the goldens were read at source when built (hunks printed at generation) and proved by CONTROL (strict apply in a clone, tests red at tip by assertion, green after, whole-service suite no new red, sha restore). I did not run a separate hand clone beyond the checker's own per-round clone.

## FAILs
None. Own defects caught before queueing: none needed a rebrief (operator 94's blank-context hunk pitfall avoided: contexts checked at generation).

## Caveats for the raising seat
- The tests are operator-authored (no ticket text); each brief states the BEHAVIOUR CHANGE (hostile value now answered with constant `unreadable thrown value`). p1/p2: the original thrown value is now rethrown, not a TypeError. p3: request now answered 500 instead of left open (Express 4).
- Each fix touches only the named catch; other KS-1868 sites in the same files are untouched (p4 file is complete, p3 route is separate site from p4).
- Develop moved to 67309f28ab21 after the briefs: re-check `Tip:` drift only if a file above is touched.

## Loops
loop95.sh (pid 81052, queue advance + drainer restart, bound 300 x 30 s) exited 15:14:19; holdloop95.sh (pid 4895, bound 400 x 20 s) exited 15:14:25 (STOP file). Both armed-log lines read back (loop95.log / holdloop95.log). Queue drainer pid 80083 (not mine to stop) exits on empty queue. No process of mine is running.

## Spark at end
`SPARK: ⚠ IDLE since last round 1 min ago - queue EMPTY` (spark_status.py 15:14, tunnel UP).

Files here: gen/ (mk95.py, sites95.py, t95_p*.ts.txt), ld.sh, chk95.sh, ch95.sh, hold95.sh, advance95.sh, loop95.sh, holdloop95.sh, hold_p*.log/out, chk_p*.out, dry_/lint_ outs, screen_all.out, open_prs_start.json, held_paths.out.
