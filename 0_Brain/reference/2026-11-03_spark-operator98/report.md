# Spark operator 98 - report (2026-11-03, started ~17:45 AEDT)

Base: develop de8d208a8426747b3a752309e08167fa0de4b2ff = `git -C <Secuura checkout> ls-remote origin refs/heads/develop` (what round.sh reads). TRAP HIT: the brief's literal `git ls-remote <path>` returns the LOCAL checkout's develop (5dccdcb2, a stale 2026-10-29 branch), not origin's. I screened and built at 5dccdcb2 first; round.sh refused the dry-runs as STALE BRIEF (class: brief/mine, caught by the harness). Re-screened, re-keyed and rebuilt at de8d208a; all nft.routes line numbers moved (+5..+17) and the GET /certificates handler had gained readerIdentity (KS-1836), so its test passes a `user`. Future operators: ls-remote `origin`, not the path.
Open PRs (gen/prscan92.py, read-only REST): 22 PRs, 124 file entries, planted control services/originate = 5 entries. services/auth in PR 1987; restore-local-secrets in PR 1982.
Held-READY (gen/heldlist.py): 859 READY, 542 paths.

## Screen
O97's widened screen (gen/screen97w.py, screen97c.py re-keyed to 98): narrow+wide screens return only the sites O96/O97 already rejected, plus a few not yet examined. Pool is thin; nft.routes.ts had been waved off as "route-level" by O95-O97, but its handlers are plain async catches with a log call and a stand-in-able service: a hostile throw makes the async handler reject (Express 4: no reply). It is the same KS-1868 class, so I took 8 of its 15 sites, one per pass, one hunk each, plus 1 shared site.
CHOSEN (9 passes, 9 sites, vitest):
- p1 packages/shared cardano/wallet.ts enableWallet catch (177)
- p2 nft-certificate routes/nft.routes.ts GET /certificates/:id (293)
- p3 GET /certificates (262)
- p4 GET /tiers (321)
- p5 POST /estimate (217)
- p6 POST /verify/transaction (426)
- p7 POST /verify/asset (462)
- p8 POST /ipfs/pin (550)
- p9 POST /ipfs/unpin (575)
Excluded: services/auth/** (Seat F 28th); scripts/* incl. restore-local-secrets* (Seat E 31st); held files (O96 and O97 sites, all of O97's p1-p9 now held); index.ts boot files (billing, prism, tokenisation, originate, api-gateway startup-migrations: need a booted service); kyc microsoft-verification.ts:223 (the thrown value is always a CallbackKeyNotConfiguredError instance, nothing to provoke); events/index.ts (err.message?.includes on a redis loop: needs an xreadgroup stand-in and a loop, and 150 rethrows anyway); kyc entra, referral, transfer, vc-issuer (Zod / validated-error message); tracing.ts, resolver.ts:230, system-status.ts, rfc3161-verify, compression.ts, cip30, wallet.ts:421 (reasons as O97). Remaining nft.routes catches (mint, record, privacy-options, supported-chains, ipfs upload, metadata size, platform-fee) left for a later operator: mint/record/fee carry auth or mint-failure mapping; privacy-options and supported-chains have no way to throw.
Builders: gen/mk98.py + gen/sites98.py + gen/gen_nft_tests.py + gen/t98_p*.ts.txt; lint + dry-run via ld98.sh. All 9: lint rc 0, dry rc 0 at de8d208a.

## Armed 17:56:16
Controls were queued as `<brief_dir> --control` lines in spark/queue.md (17:5x, controls_queued_at.txt) - hand `round.sh --control` writes no done.md row (O96/O97 finding). loop98b.sh (pid in loop98b.pid) queues each model line only after that pass's CONTROL-PASS row, restarts the drainer with SPARK_MIN_FREE_GB=12 when the queue has lines; 300 x 30 s. holdloop98.sh (pid in holdloop98.pid) holds via the hold tool only when PASS (7/7) and patch byte-identical to golden. STOP file: $O/STOP.
Drainer first line read back: `queue: ---- 2026-11-03 17:56:37 round 1: ...o98_p1... --control`.
Controls: p1 CONTROL-PASS 17:57:52 (75 s), p2 17:59:10 (77 s).

## Verdicts (done.md rows)
Controls 9/9 CONTROL-PASS byte-identical (17:57-18:06, 61-77 s). Model rounds 9/9 PASS (7/7), golden byte-identical on round one, no rebrief: p1 18:08, p2 18:10, p3 18:12, p4, p5, p6, p7, p8, p9 (done 18:26). All 9 HELD by holdloop98 via the hold tool (READY_KS-1868-KS-1868-O98-P1..P9_spark-dsv4flash_*.diff.md in local-model/night/), hold_pN.log read back "hold rc=0 HELD".
FAIL count: 0 model / 0 brief at the model stage. Events: (1) wrong base from `ls-remote <path>` (brief/mine, caught by round.sh STALE BRIEF at dry-run, rebuilt); (2) a first background dry-run batch at the wrong tip was killed (TaskStop, pkill ld98.sh); no model round ever ran at the wrong tip.
End state 18:27: queue empty, drainer exited ("queue: empty ... after 18 round(s)"), loop98b.sh (55563) and holdloop98.sh (55567) alive and idle (bounded), DevMASTER 16 GiB free (never under 16 during the run).
