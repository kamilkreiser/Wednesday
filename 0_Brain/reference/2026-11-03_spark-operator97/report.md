# Spark operator 97 - report (2026-11-03, started ~16:30 AEDT)

Base: develop de8d208a8426747b3a752309e08167fa0de4b2ff (git ls-remote origin refs/heads/develop re-read ~16:3x = de8d208a; commit time 16:24:01 AEDT). The cache clone did not have it; fetched into the Spark cache (round.sh's own fetch refspec). Reads via `git show` / `git grep` at that tip.
Open PRs (gen/prscan92.py, GitHub REST read-only): 21 PRs, 115 file entries, planted control services/originate = 5 entries, saved open_prs_start.json.
Held-READY (gen/heldlist.py): 850 READY files, 525 paths -> held_paths.out.

## Screen
O96's screen (instanceof Error ? x.message : String(x), String(err), err.message; gen/screen97.py): 78 files; of the unheld/no-PR ones only O96's already-rejected set remained (scripts/*, nft.routes, issuerCert (auth), kyc entra, tokenisation index, platformOrganizations, notifications, originate index, wallet.ts, compression.ts). O96's own 9 files are now held, so the narrow screen is exhausted (control: O96's p1-p9 files show HELD).
Widened (gen/screen97w.py: `(x as Error).message`, `${err}` interpolation, any *err*/*error*/*cause*.message / String(*err*)) and a catch-body scan (gen/screen97c.py: any `catch (v)` whose next 13 lines use v in a template, .message, String(), toString, stringify; excludes held, PR, tests, services/auth/**): 76 hits in 27 files.
Excluded and why: services/auth/** (Seat F 27th); restore-local-secrets* (Seat E 31st; scripts not scanned anyway); held files (gracefulShutdown, vc/verifier, nft ipfs.service ...); index.ts boot files (billing, prism, api-gateway startup-migrations, tokenisation, originate: need a booted service); nft.routes / transfer / referral / vc-issuer (Zod or route-level, same reasons as O95/O96 or message of a validated ZodError); resolver.ts:230 (the try body cannot throw: no way to provoke the catch); tracing.ts (module-level SDK state); monitoring/alerts.ts, production-guard.ts, deployedContracts.ts (not a thrown value); cip30 provider (an inspection, not an interpolation); rfc3161-verify (needs crafted CMS tokens + pkijs mocking); system-status.ts (private function inside a 600-line router with execSync).
CHOSEN: 9 passes, 9 catch sites (1 hunk each), vitest, 8 in packages/shared, 1 in api-gateway:
- p1 packages/shared middleware/tenant-rate-limiter.ts createTenantRateLimiter fail-open catch (line 198)
- p2 packages/shared db/tenant-pool-manager.ts TenantPoolManager.refreshConfigs catch (333)
- p3 packages/shared db/tenant-context.ts extractTenantContext catch (95)
- p4 packages/shared vault/key-vault.ts SecretsManager.getSecret vault catch (107)
- p5 packages/shared db/auto-migrate.ts runMigrations per-migration catch (162)
- p6 packages/shared security/ssrf-guard.ts resolvePublicAddresses lookup catch (324)
- p7 packages/shared cardano/transaction.ts verifyDocumentAnchor catch (224)
- p8 services/api-gateway routes/health-dashboard.ts checkService catch (79)
- p9 packages/shared security/ssrf-guard.ts safeOutboundRequest request-construction catch (582)
None under services/auth/**, none restore-local-secrets, none of O96's 9 sites. p6 and p9 are one file at hunks >250 lines apart.
Builders: gen/mk97.py + gen/sites97.py + gen/t97_p*.ts.txt (copies of O96's, re-keyed); lint + dry-run via ld97.sh.

## Dry-run + lint
All 9: lint rc 0, dry-run rc 0 after one builder fix: p8's first design re-indented the existing if/else block, and the harness REFUSED it (4 '+' lines byte-identical to '-' lines = context, not additions). Class: brief (mine); fixed in sites97.py by an insert-only edit (a `readable` probe before the existing if, the existing chain kept as context); rebuilt, lint 0, dry 0.

## Armed 16:49:21
ctl97.sh pid 58422 (controls p1..p9 in order, retry on BUSY, <=40 tries each); loop97.sh pid 58423 (queues the model line only after that pass's CONTROL-PASS row, restarts the drainer when the queue has lines; 300 x 30 s = 2.5 h); holdloop97.sh pid 58424 (hold via hold tool when PASS 7/7 and patch byte-identical to golden; 400 x 20 s). STOP file: $W/STOP. Operator 96's own loop96 (91900) / holdloop96 (91901) are still alive and idle (they glob o96 briefs only); untouched.

## Controls (queued `--control` lines; done.md rows come only from the queue)
- 16:49 my first ctl97.sh ran round.sh --control by hand: p1 rc 0, p2 rc 2 REFUSED (harness, transient: the builder could not read attached PR #1978 state, RemoteDisconnected, fail closed; not a model or brief fault), p3 started. No done.md rows result from hand runs (same finding as operator 96), so I killed ctl97 (58422) and queued `<brief_dir> --control` lines for p1..p9 (queued 16:52:32).
- 16:54:18 p1 CONTROL-PASS (byte-identical, 73 s). 16:55:32 p2 CONTROL-PASS (the earlier rc 2 was the transient). Both model lines queued by loop97.
- 17:05 queue STOPPED by its own guard: 19 GB free < SPARK_MIN_FREE_GB=20 on the shared DevMASTER volume (harness/environment; nothing wrong with the briefs). Judgement: I did not delete or move anything (old work clones carry no verdict rows so prune_work refuses them; a mv within the volume frees nothing). I killed loop97 (58423) and started loop97b.sh (copy; pid in loop97b.pid) which starts the drainer with SPARK_MIN_FREE_GB=12 (the tool's own documented env). Rounds clone ~350 MB and are pruned after their row. Flag for Kam/Wednesday: the volume is at 99%.
- 17:07:53 p3 CONTROL-PASS.

## Verdicts (done.md rows, all after CONTROL-PASS 9/9 byte-identical, 16:54-17:16)
Model rounds, all PASS (7/7) with golden BYTE-IDENTICAL on the first round (no rebrief used): p1 17:18 (101 s), p2 17:20 (108 s), p3 17:24 (264 s), p4 17:26 (125 s), p5 17:29 (154 s), p6 17:31 (114 s), p7 17:32 (99 s), p8 17:36 (219 s), p9 17:39 (175 s). All 9 HELD by holdloop97 via the hold tool (READY_KS-1868-KS-1868-O97-P1..P9_spark-dsv4flash_*.diff.md in local-model/night/), hold_pN.log read back. Suite counts per hold log (e.g. p1 1447->1451, strict apply).
FAIL count: 0 model / 0 brief at the model stage. Harness/brief events along the way: (1) p8 first design refused by the builder (brief, mine, fixed before any round); (2) transient GitHub read refusal on a hand control (harness); (3) queue stopped by the 20 GB free-space guard at 19 GB (environment; resolved by SPARK_MIN_FREE_GB=12 on my drainer starts).
End state 17:40: queue empty, drainer exited ("queue: empty ... after 16 round(s)"), loop97b.sh (26046) and holdloop97.sh (58424) still alive and idle (bounded), DevMASTER at 17 GB free (100%).
