# Operator 93 sites (KS-1868). Built by mk94.py (exec'd into its namespace: T, SV, OS, mk available).
REFV=SV+'auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts'
def guard(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"try {\n"+s+"  const m = %s?.message;\n"%var+s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
def guard_e(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s instanceof Error ? %s.message : String(%s);\n"%(var,var,var)+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
REUSE_Q=("This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (operator 81 `security/src/db.ts`, operator 85 `accountLockout.ts`, operator 86 `userErasedSubscriber.ts`: `const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, the constant `'unreadable thrown value'` on throw) before the log call; no helper exists in this file and none is added.")
REUSE_E=("This follows the guard that the merged KS-1868 passes use for `err instanceof Error ? err.message : String(err)` reads (operator 51 `nft-certificate`, operator 57 `tenant-provisioning`, operator 86 `errorTrackingService.ts`: the same expression inside a `try`, the constant `'unreadable thrown value'` on throw) before the log call; no helper exists in this file and none is added.")
def site(k, svc, rel, edits, nh, lines, fn, short, whatwrong, callers, premise, tsrc, dbnote, ncells, greens, redcells, nred, name, red1, reuse=REUSE_Q, runner='vitest', ref=None, testbase=None):
    run = 'run ' if runner=='vitest' else ''
    T[k]=dict(key='KS-1868', runner=runner, runcmd=run, rdir=SV+svc, ref=ref or REFV,
      sib="`ks1868-oauth-authorize-token-unreadable-throw.test.ts` and `ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts`" if runner=='vitest' else "`ks1868-anchors-route-catches-unreadable-throw.test.ts`",
      reuse=reuse, dir='ks_1868_o97_%s_%s'%(k,name), prod=SV+svc+'/'+rel, edits=edits, nh=nh, lines=lines,
      test=SV+svc+'/src/__tests__/'+testbase, tsrc=tsrc, fn=fn, short=short, premise=premise, whatwrong=whatwrong, callers=callers,
      ncells=ncells, red1=red1, dbnote=dbnote, greens=greens, redcells=redcells,
      redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,nred+1)))
def guard_s(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | undefined;\n"+s+"try {\n"+s+"  const m = %s?.message;\n"%var+s+"  reason = m === undefined || m === null ? undefined : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
SOr=SV+'originate/'
JREF=SOr+'src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'
HELD_NOTE="Held READY files of other operators edit this product file at other hunks (named in the report); the hunks of this brief are disjoint from them by more than 3 lines."


# ===================== Operator 97 sites (KS-1868) =====================
def gv(ind, var, expr, const="'unreadable thrown value'"):
    s=' '*ind
    return (s+"let %s: string;\n"%var+s+"try {\n"+s+"  %s = %s;\n"%(var,expr)+s+"} catch {\n"+s+"  %s = %s;\n"%(var,const)+s+"}\n")
SEXPR="err instanceof Error ? err.message : String(err)"
def std_what(where, what_it_returns, extra=''):
    return ("%s reads the thrown value with no guard. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the catch itself throw, so %s. The fix is the house guard placed in the catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The message text of every value that can be read is unchanged.%s")%(where, what_it_returns, extra)


PKG_REF='Blockchain/Dev/packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts'
SIB_PKG="`ks1868-response-cache-read-unreadable-throw.test.ts` and `ks1868-audit-logger-flush-unreadable-throw.test.ts`"
REUSE_S=("This follows the guard that the merged KS-1868 passes use for `String(err)` reads (operator 51 `nft-certificate`, operator 57 `tenant-provisioning`, operator 86 `errorTrackingService.ts`: the same expression inside a `try`, the constant `'unreadable thrown value'` on throw) before the log call; no helper exists in this file and none is added.")
def what(where, ret, extra=''):
    return ("%s reads the thrown value with `String(...)`, unguarded. A thrown value whose read throws (a revoked Proxy: `String()` throws on it; an Error whose `message` getter throws, since `Error.prototype.toString` reads it) makes the catch itself throw, so %s. The fix is the house guard placed in the catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The text of every value that can be read is unchanged.%s")%(where, ret, extra)
STD_CELLS='4 cells: C1, C2 controls, R1, R2 red'
G2="'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)"
G2R="`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)"
def fixsib(k, pkg=False):
    if pkg:
        for _f in ('prod','test','rdir'):
            T[k][_f]=T[k][_f].replace('services/shared','packages/shared')
    T[k]['sib']=SIB_PKG

def catch_edit(ind, msg, var='error', pre="    } catch (error) {\n", tail="{ error: String(error) }", newtail="{ error: reason }", expr="String(error)"):
    s=' '*ind
    o=pre+s+"logger.error('%s', %s);\n"%(msg,tail)
    n=pre+gv(ind,'reason',expr)+s+"logger.error('%s', %s);\n"%(msg,newtail)
    return (o,n)

RS='src/security/redis-security-store.ts'
# ---- P1
def wd(where, ret, read="the thrown value's `message`"):
    return ("%s reads %s with no guard. A thrown value whose read throws (a revoked Proxy: any property read and `instanceof` throw on it; an Error whose `message` getter throws) makes the catch itself throw, so %s. The fix is the house guard placed in the catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The text of every value that can be read is unchanged.")%(where, read, ret)
def gv_t(ind, var, expr):
    return gv(ind, var, expr)
PKGS='Blockchain/Dev/packages/shared/'
# ---- P1 tenant-rate-limiter
O1=("    } catch (err: any) {\n      // On error, allow the request through (fail-open)\n      console.warn(\n        `[tenant-rate-limiter] Rate limit check failed, allowing request: ${err.message}`,\n      );\n")
N1=("    } catch (err: any) {\n      // On error, allow the request through (fail-open)\n"+gv(6,'reason','err.message')+"      console.warn(\n        `[tenant-rate-limiter] Rate limit check failed, allowing request: ${reason}`,\n      );\n")
site('p1','shared','src/middleware/tenant-rate-limiter.ts',[(O1,N1)],1,
  '198-204 (the catch of the middleware returned by `createTenantRateLimiter`)',
  'the fail-open catch of the middleware built by `createTenantRateLimiter` in `src/middleware/tenant-rate-limiter.ts`',
  'the unguarded `err.message` read in the ONE fail-open catch of the middleware; the Redis connection `.catch` handler at line 76 is deliberately NOT touched',
  wd("The fail-open catch of the middleware","the middleware REJECTS and `next()` is never called, so the request is neither limited nor let through, where an ordinary failure logs a warning and calls `next()`"),
  "CALLERS: every service that mounts the per-tenant limiter in its Express chain. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `console.warn('[tenant-rate-limiter] Rate limit check failed, allowing request: <message>')` and `next()`. Today (hostile value): the middleware rejects and the request hangs. After: the same warning with the constant reason and `next()`. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the request is let through (the limiter's own fail-open rule) instead of hanging.",
  "Premise: `tenant-rate-limiter.ts` read whole (lines 1-206)",
  't97_p1.ts.txt',
  "The response stand-in's `setHeader` throws the cell's value (the first call in the `try`); the limiter uses its in-memory path (no Redis URL); `console.warn` is recorded with a spy; no network.",
  STD_CELLS, G2, G2R, 2, 'shared_tenant_rate_limiter_fail_open_catch_guard_message',
  "At the tip the catch throws, so the assertion fails", reuse=REUSE_Q, runner='vitest', ref=PKG_REF,
  testbase='ks1868-tenant-rate-limiter-fail-open-catch-unreadable-throw.test.ts')
fixsib('p1',True)
# ---- P2 tenant-pool-manager
O2="    } catch (err: any) {\n      console.error('[TenantPoolManager] Failed to load tenant configs:', err.message);\n"
N2="    } catch (err: any) {\n"+gv(6,'reason','err.message')+"      console.error('[TenantPoolManager] Failed to load tenant configs:', reason);\n"
site('p2','shared','src/db/tenant-pool-manager.ts',[(O2,N2)],1,
  '333-335 (the catch of `TenantPoolManager.refreshConfigs`)',
  'the catch of `TenantPoolManager.refreshConfigs` in `src/db/tenant-pool-manager.ts`',
  'the unguarded `err.message` read in the ONE catch of `refreshConfigs`; the pool `error` handlers and the timer `.catch` in `init` are deliberately NOT touched',
  wd("The catch of `refreshConfigs`","`refreshConfigs` REJECTS where an ordinary failure is logged and swallowed (and `init` would fail at boot, or the refresh timer's rejection would be handled elsewhere)"),
  "CALLERS: `init` (boot) awaits `refreshConfigs`, and the refresh timer calls it every 60 s. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `console.error('[TenantPoolManager] Failed to load tenant configs:', <message>)` and the previous maps stay as they were. Today (hostile value): `refreshConfigs` rejects. After: the same log line with the constant reason. Persisted state: none (the in-memory maps keep their last content). **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, `refreshConfigs` logs and resolves instead of rejecting.",
  "Premise: `tenant-pool-manager.ts` read from the class head to `refreshConfigs` (lines 1-336)",
  't97_p2.ts.txt',
  "`pg` is replaced by a plain Pool stand-in whose `query` rejects with the cell's value; the manager is built with `enabled: true`; `console.error` is recorded with a spy; no network.",
  STD_CELLS, G2, G2R, 2, 'shared_tenant_pool_manager_refresh_configs_catch_guard_message',
  "At the tip the catch throws (refreshConfigs rejects), so the assertion fails", reuse=REUSE_Q, runner='vitest', ref=PKG_REF,
  testbase='ks1868-tenant-pool-manager-refresh-configs-catch-unreadable-throw.test.ts')
fixsib('p2',True)
# ---- P3 tenant-context
O3="    } catch (err: any) {\n      res.status(503).json({\n        error: 'Tenant database unavailable',\n        message: err.message,\n      });\n"
N3="    } catch (err: any) {\n"+gv(6,'reason','err.message')+"      res.status(503).json({\n        error: 'Tenant database unavailable',\n        message: reason,\n      });\n"
site('p3','shared','src/db/tenant-context.ts',[(O3,N3)],1,
  '95-99 (the catch of the middleware returned by `extractTenantContext`)',
  'the catch of the middleware returned by `extractTenantContext` in `src/db/tenant-context.ts`',
  'the unguarded `err.message` read in the ONE catch around `manager.getPool`; the status checks above it are deliberately NOT touched',
  wd("The catch around `manager.getPool`","the middleware throws out of the request and no 503 is sent, where an ordinary failure answers 503 `Tenant database unavailable`"),
  "CALLERS: every service that mounts `extractTenantContext(manager)`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): HTTP 503 with `{ error: 'Tenant database unavailable', message: <message> }` and no `next()`. Today (hostile value): the middleware throws and the request gets no tenant answer. After: the same 503 with the constant reason. Persisted state: none. **BEHAVIOUR CHANGE the reply must state:** for a thrown value that cannot be read, the client receives the 503 with the constant message instead of a failed request.",
  "Premise: `tenant-context.ts` read whole (lines 1-103)",
  't97_p3.ts.txt',
  "The manager is a plain stand-in (`isEnabled` false, `getPool` throws the cell's value); the response is a plain recorder; no database, no `pg`.",
  STD_CELLS, G2, G2R, 2, 'shared_tenant_context_get_pool_catch_guard_message',
  "At the tip the catch throws, so the assertion fails", reuse=REUSE_Q, runner='vitest', ref=PKG_REF,
  testbase='ks1868-tenant-context-get-pool-catch-unreadable-throw.test.ts')
fixsib('p3',True)
# ---- P4 key-vault getSecret
O4="      } catch (err: any) {\n        logger.warn('[SecretsManager] Failed to retrieve secret from vault', {\n          secret: name,\n          error: err.message,\n        });\n"
N4="      } catch (err: any) {\n"+gv(8,'reason','err.message')+"        logger.warn('[SecretsManager] Failed to retrieve secret from vault', {\n          secret: name,\n          error: reason,\n        });\n"
site('p4','shared','src/vault/key-vault.ts',[(O4,N4)],1,
  '107-112 (the vault catch of `SecretsManager.getSecret`)',
  'the vault catch of `SecretsManager.getSecret` in `src/vault/key-vault.ts`',
  'the unguarded `err.message` read in the vault catch of `getSecret`; the catch of `ensureVaultClient` (line 196) is deliberately NOT touched',
  wd("The vault catch of `getSecret`","`getSecret` REJECTS and the environment fallback is never tried, where an ordinary failure logs a warning and falls back"),
  "CALLERS: every service that loads a secret through the shared `SecretsManager` of `src/vault/key-vault.ts`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `logger.warn('[SecretsManager] Failed to retrieve secret from vault', { secret, error: <message> })` and the environment fallback (the value of the environment variable, or the not-found Error). Today (hostile value): the call rejects, the environment fallback is never read. After: the same warning with the constant reason and the environment fallback. Persisted state: the cache only. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, secret loading falls back to the environment instead of failing.",
  "Premise: `key-vault.ts` read from the class head to `ensureVaultClient` (lines 56-203)",
  't97_p4.ts.txt',
  "The vault client is a plain stand-in installed on the instance (`vaultInitAttempted` set so no Azure package is loaded) whose `getSecret` rejects with the cell's value; the environment variable `KS1868_SECRET` is set and removed per cell; the logger is a plain recorder; no network.",
  STD_CELLS, G2, G2R, 2, 'shared_key_vault_get_secret_vault_catch_guard_message',
  "At the tip the catch throws (getSecret rejects), so the assertion fails", reuse=REUSE_Q, runner='vitest', ref=PKG_REF,
  testbase='ks1868-key-vault-get-secret-catch-unreadable-throw.test.ts')
fixsib('p4',True)
# ---- P5 auto-migrate
O5="      } catch (err: any) {\n        await client.query('ROLLBACK').catch(() => {});\n        const message = `Failed to apply ${filename}: ${err.message || err}`;\n"
N5="      } catch (err: any) {\n        await client.query('ROLLBACK').catch(() => {});\n"+gv(8,'detail','`${err.message || err}`')+"        const message = `Failed to apply ${filename}: ${detail}`;\n"
site('p5','shared','src/db/auto-migrate.ts',[(O5,N5)],1,
  '162-166 (the migration catch of `runMigrations`)',
  'the migration catch of `runMigrations` in `src/db/auto-migrate.ts`',
  'the unguarded `err.message || err` read in the per-migration catch; the rest of the function is deliberately NOT touched',
  wd("The per-migration catch of `runMigrations`","`runMigrations` REJECTS (after the `finally` closes the pool) and the caller gets no result, where an ordinary failure is recorded in `errors` and the loop stops","the thrown value (`${err.message || err}`)"),
  "CALLERS: service boot code that awaits `runMigrations` and inspects `errors`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): ROLLBACK, `errors` gains `Failed to apply <file>: <text>`, the loop stops, the result is returned. Today (hostile value): the ROLLBACK runs, then the function rejects with a TypeError and no result. After: the same record with the constant reason in place of the text. Persisted state: none (the transaction is rolled back before the read). **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the caller receives the result with the constant reason instead of a TypeError.",
  "Premise: `auto-migrate.ts` read whole (lines 1-180)",
  't97_p5.ts.txt',
  "`pg` is replaced by a plain Pool stand-in whose client rejects the migration statement `SELECT 1;` with the cell's value; the migration file is real and lives in a temporary directory removed after each cell; `console.log` and `console.error` are silenced with spies; no network.",
  STD_CELLS, G2, G2R, 2, 'shared_auto_migrate_run_migrations_catch_guard_message',
  "At the tip the catch throws (runMigrations rejects), so the assertion fails", reuse=REUSE_Q, runner='vitest', ref=PKG_REF,
  testbase='ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts')
fixsib('p5',True)
# ---- P6 ssrf-guard resolvePublicAddresses
O6="  } catch (err) {\n    return {\n      ok: false,\n      error: `host \"${bare}\" could not be resolved (${(err as Error).message}) — refusing to contact an unverifiable destination`,\n    };\n  }\n"
N6="  } catch (err) {\n"+gv(4,'reason','(err as Error).message')+"    return {\n      ok: false,\n      error: `host \"${bare}\" could not be resolved (${reason}) — refusing to contact an unverifiable destination`,\n    };\n  }\n"
site('p6','shared','src/security/ssrf-guard.ts',[(O6,N6)],1,
  '324-329 (the lookup catch of `resolvePublicAddresses`)',
  'the lookup catch of `resolvePublicAddresses` in `src/security/ssrf-guard.ts`',
  'the unguarded `(err as Error).message` read in the lookup catch; the catches of `safeOutboundRequest` (lines 582 and 624) are deliberately NOT touched',
  wd("The lookup catch of `resolvePublicAddresses`","the call REJECTS where an ordinary lookup failure returns the refusal `{ ok: false, error }` (the guard still refuses: it fails closed, but with an exception instead of its documented return)"),
  "CALLERS: `safeOutboundRequest` (inside its DNS race) and `assertResolvedHostPublic`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ ok: false, error: 'host \"<h>\" could not be resolved (<message>) — refusing to contact an unverifiable destination' }`. Today (hostile value): the call rejects. After: the same refusal with the constant reason. The guard stays fail-closed in both: no address is ever returned. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the caller receives the refusal result instead of an exception.",
  "Premise: `ssrf-guard.ts` read from `resolvePublicAddresses` to `safeOutboundRequest` (lines 296-345 and 440-630)",
  't97_p6.ts.txt',
  "The `dns/promises` module is a plain stand-in whose `lookup` rejects with the cell's value (the pattern of `ssrf-guard.test.ts`); no network.",
  STD_CELLS, G2, G2R, 2, 'shared_ssrf_guard_resolve_public_addresses_catch_guard_message',
  "At the tip the catch throws (the call rejects), so the assertion fails", reuse=REUSE_Q, runner='vitest', ref=PKG_REF,
  testbase='ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts')
fixsib('p6',True)
# ---- P7 cardano transaction verifyDocumentAnchor
O7="  } catch (error) {\n    return {\n      verified: false,\n      error: error instanceof Error ? error.message : 'Unknown error',\n    };\n  }\n}\n"
N7="  } catch (error) {\n"+gv(4,'reason',"error instanceof Error ? error.message : 'Unknown error'")+"    return {\n      verified: false,\n      error: reason,\n    };\n  }\n}\n"
site('p7','shared','src/cardano/transaction.ts',[(O7,N7)],1,
  '224-229 (the catch of `verifyDocumentAnchor`)',
  'the catch of `verifyDocumentAnchor` in `src/cardano/transaction.ts`',
  'the unguarded `error instanceof Error ? error.message : \'Unknown error\'` read in the ONE catch of `verifyDocumentAnchor`; the other functions of the file are deliberately NOT touched',
  wd("The catch of `verifyDocumentAnchor`","the call REJECTS where an ordinary failure answers `{ verified: false, error }`","the thrown value (`error instanceof Error ? error.message : 'Unknown error'`)"),
  "CALLERS: code that verifies a document anchor against a Cardano transaction through the shared Blockfrost client. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ verified: false, error: <message> }`. Today (hostile value): the call rejects with a TypeError. After: `{ verified: false, error: 'unreadable thrown value' }`. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the caller receives `verified: false` with the constant reason instead of a TypeError.",
  "Premise: `transaction.ts` read from `confirmTransaction` to `verifyDocumentAnchor` (lines 150-230)",
  't97_p7.ts.txt',
  "The Blockfrost client is a plain stand-in whose `getTransactionMetadata` rejects with the cell's value; no network.",
  STD_CELLS, G2, G2R, 2, 'shared_cardano_verify_document_anchor_catch_guard_message',
  "At the tip the catch throws (the call rejects), so the assertion fails", reuse=REUSE_E, runner='vitest', ref=PKG_REF,
  testbase='ks1868-cardano-verify-document-anchor-catch-unreadable-throw.test.ts')
fixsib('p7',True)
# ---- P8 api-gateway health-dashboard
O8=("    let errorMessage = 'Unknown error';\n\n    if (error instanceof DOMException && error.name === 'AbortError') {\n")
N8=("    let errorMessage = 'Unknown error';\n\n    let readable = true;\n    try {\n      void (error instanceof Error && error.message);\n      void (error instanceof DOMException && error.name);\n    } catch {\n      readable = false;\n    }\n\n    if (!readable) {\n      errorMessage = 'unreadable thrown value';\n    } else if (error instanceof DOMException && error.name === 'AbortError') {\n")
site('p8','api-gateway','src/routes/health-dashboard.ts',[(O8,N8)],1,
  '80-83 (the head of the error classification in the catch of `checkService`)',
  'the catch of `checkService` in `src/routes/health-dashboard.ts`',
  'the unguarded thrown-value reads (`instanceof`, `.name`, `.message`) in the ONE catch of `checkService`; the 2xx path and the route handler are deliberately NOT touched',
  wd("The catch of `checkService`","`checkService` rejects, the aggregate silently drops the settled-rejected result, and the service is ABSENT from the dashboard instead of reported down","the thrown value (`instanceof DOMException`, `.name`, `instanceof Error`, `.message`)"),
  "CALLERS: the `GET /dashboard` handler, which maps every deployed service through `checkService` inside `Promise.allSettled`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): an entry `{ status: 'down', latencyMs, url, error: <message> }` (`timeout` for an abort, `Unknown error` for a non-Error). Today (hostile value): no entry, the service vanishes from the dashboard and the counts. After: the entry with the constant reason. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the service is reported down instead of omitted.",
  "Premise: `health-dashboard.ts` read whole (lines 1-194)",
  't97_p8.ts.txt',
  "`../config/services` is a plain stand-in with one deployed (non-localhost) service; the global `fetch` is a plain function rejecting with the cell's value (stubbed with `vi.stubGlobal`, removed after each cell); fake timers keep the abort timer from outliving the cell; the `/dashboard` handler is read off `router.stack`; no network.",
  STD_CELLS, G2, G2R, 2, 'gateway_health_dashboard_check_service_catch_guard_message',
  "At the tip the catch throws, so the service entry is absent and the assertion fails", reuse=REUSE_E, runner='vitest', ref=None,
  testbase='ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts')
# ---- P9 ssrf-guard safeOutboundRequest request()
O9="    } catch (err) {\n      done({ ok: false, reason: 'request_failed', error: (err as Error).message });\n      return;\n    }\n"
N9="    } catch (err) {\n"+gv(6,'reason','(err as Error).message')+"      done({ ok: false, reason: 'request_failed', error: reason });\n      return;\n    }\n"
site('p9','shared','src/security/ssrf-guard.ts',[(O9,N9)],1,
  '582-585 (the request-construction catch of `safeOutboundRequest`)',
  'the request-construction catch of `safeOutboundRequest` in `src/security/ssrf-guard.ts`',
  'the unguarded `(err as Error).message` read in the catch around `mod.request(...)`; the lookup catch of `resolvePublicAddresses` (line 324) and the `req.write` catch (line 624) are deliberately NOT touched',
  wd("The catch around `mod.request(...)` in `safeOutboundRequest`","the call REJECTS (the throw escapes the Promise executor) where the function documents that it returns a tagged `request_failed` result rather than throwing (KS-931)"),
  "CALLERS: the outbound webhook delivery and any caller of `safeOutboundRequest` that dropped its own try/catch on the strength of the documented return. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ ok: false, reason: 'request_failed', error: <message> }`. Today (hostile value): the returned promise rejects. After: the same result with the constant reason. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the caller receives the `request_failed` result instead of an exception.",
  "Premise: `ssrf-guard.ts` read from `safeOutboundRequest` to its end (lines 440-630)",
  't97_p9.ts.txt',
  "`https` is mocked with a plain `request` that throws the cell's value (the pattern of `ks914-shipped-path.test.ts`); the URL is the TEST-NET-3 literal `https://203.0.113.7/`, so no DNS and no network.",
  STD_CELLS, G2, G2R, 2, 'shared_ssrf_guard_safe_outbound_request_catch_guard_message',
  "At the tip the catch throws (the call rejects), so the assertion fails", reuse=REUSE_Q, runner='vitest', ref=PKG_REF,
  testbase='ks1868-ssrf-guard-safe-outbound-request-catch-unreadable-throw.test.ts')
fixsib('p9',True)
