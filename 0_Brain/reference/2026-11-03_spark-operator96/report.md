# Spark operator 96 - report (2026-11-03, started ~15:15 AEDT)

Base: develop 67309f28ab21 (ls-remote re-read 15:1x, unchanged). Reads via the Spark cache clone with `git show` / `git grep` at that tip (no checkout; workdir stays tiny).
Open PRs (instrument gen/prscan92.py, GitHub REST read-only): 24 PRs, 136 file entries, planted control services/originate = 5 entries, saved open_prs_start.json. 1985 (api-gateway security.ts, rateLimitEnforce.ts), 1986 (anchoring threadTokenIndex.ts), 1982 (restore-local-secrets.sh) confirmed in the list.
Held-READY instrument gen/heldlist.py: 841 READY files, 509 paths (includes O95's 8 new products) -> held_paths.out.

## Screen
gen/screen96.py: git grep at the tip over services/packages/scripts for `instanceof Error ? x.message : String(x)`, `String(err)`, `err.message` (plus a wider variable-name variant: nothing new). 79 files; 19 neither held nor in an open PR. Of those, excluded: scripts/* (not runtime), nft.routes.ts, issuerCert.ts, kyc entra, tokenisation index.ts, platformOrganizations.ts, notifications.ts (already guarded), originate index.ts (held file) - same reasons as O95; wallet.ts CIP-8 verify (needs the cbor/crypto libs mocked); compression.ts and the two `.catch(err=>)` handlers of cache-middleware / connection-pool (rejection is unobservable in-process without an unhandledRejection harness).
CHOSEN (9 passes, 14 catch sites, all services/shared + packages/shared + auth, vitest):
- p1 services/shared redis-security-store.ts RedisRateLimitStore.get + increment (2 hunks)
- p2 same file RedisBruteForceStore.get + set (2 hunks)
- p3 same file RedisCSRFStore.generate + validate (2 hunks)
- p4 services/shared cache-middleware.ts lookup catch
- p5 services/shared redis-client.ts connect catch
- p6 services/shared connection-pool.ts createConnection attempt catch + removeConnection close catch (2 hunks)
- p7 packages/shared secrets-manager.ts getSecret Vault catch
- p8 packages/shared event-indexer.ts handleError
- p9 auth routes/health.ts checkRedis + checkDatabase (2 hunks)
Note p1-p3 touch one file at hunks far apart (>20 lines): independent, one PR possible.
Builders: gen/mk96.py + gen/sites96.py + gen/t96_p*.ts.txt; lint + dry-run via ld96.sh.

## Armed 15:28:08
dry-run + lint rc 0 for all 9 (p9 dry read back). Loops (nohup, STOP file, bound): ctl96.sh pid 91899 (controls p1..p9 in order, retry on BUSY, <=40 tries each); loop96.sh pid 91900 (queue model line after CONTROL-PASS + drainer restart, 300 x 30 s = 2.5 h); holdloop96.sh pid 91901 (hold when PASS 7/7 and patch byte-identical to golden, 400 x 20 s). Armed-log lines read back: ctl96.log, loop96.log, holdloop96.log.
