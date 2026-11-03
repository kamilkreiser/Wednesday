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
      reuse=reuse, dir='ks_1868_o95_%s_%s'%(k,name), prod=SV+svc+'/'+rel, edits=edits, nh=nh, lines=lines,
      test=SV+svc+'/src/__tests__/'+testbase, tsrc=tsrc, fn=fn, short=short, premise=premise, whatwrong=whatwrong, callers=callers,
      ncells=ncells, red1=red1, dbnote=dbnote, greens=greens, redcells=redcells,
      redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,nred+1)))
def guard_s(ind, var='err'):
    s=' '*ind
    return (s+"let reason: string | undefined;\n"+s+"try {\n"+s+"  const m = %s?.message;\n"%var+s+"  reason = m === undefined || m === null ? undefined : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
SOr=SV+'originate/'
JREF=SOr+'src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'
HELD_NOTE="Held READY files of other operators edit this product file at other hunks (named in the report); the hunks of this brief are disjoint from them by more than 3 lines."


# ===================== Operator 95 sites (KS-1868) =====================
def gv(ind, var, expr, const="'unreadable thrown value'"):
    s=' '*ind
    return (s+"let %s: string;\n"%var+s+"try {\n"+s+"  %s = %s;\n"%(var,expr)+s+"} catch {\n"+s+"  %s = %s;\n"%(var,const)+s+"}\n")
SEXPR="err instanceof Error ? err.message : String(err)"
def std_what(where, what_it_returns, extra=''):
    return ("%s reads the thrown value with no guard. A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the catch itself throw, so %s. The fix is the house guard placed in the catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The message text of every value that can be read is unchanged.%s")%(where, what_it_returns, extra)

# ---- P1: originate lifecycleEventRepo.createLifecycleEvent (jest)
LC_O="  } catch (err: unknown) {\n    const msg = err instanceof Error ? err.message : String(err);\n    if (msg.includes('null value in column \"parent_document_id\"')) {\n"
LC_N="  } catch (err: unknown) {\n"+gv(4,'msg',SEXPR)+"    if (msg.includes('null value in column \"parent_document_id\"')) {\n"
site('p1','originate','src/repositories/lifecycleEventRepo.ts',[(LC_O,LC_N)],1,
  '81-82 (the catch of `createLifecycleEvent`)',
  'the catch of `createLifecycleEvent` in `src/repositories/lifecycleEventRepo.ts`',
  'the unguarded thrown-value read in the ONE catch of `createLifecycleEvent`',
  std_what("The catch of `createLifecycleEvent` (a failed INSERT) reads `err instanceof Error ? err.message : String(err)` into `msg`;", "the catch throws a TypeError before it logs and before its own `throw err`, so the caller never sees the error the database raised and the failure is not logged", " Every other path of the catch (the NOT NULL mapping to `LIFECYCLE_TARGET_NOT_FOUND`, the log line, the rethrow of the original value) is unchanged."),
  "CALLERS: the lifecycle routes (`createLifecycleEvent` is awaited by the lifecycle verbs of the originate document routes) map `LIFECYCLE_TARGET_NOT_FOUND` to 404 and let any other rejection reach their own error path. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `logger.error('createLifecycleEvent failed', { documentId, action, error: <message> })` and the SAME value rethrown. Today (hostile value): a TypeError is thrown instead, nothing is logged. After: the original value is rethrown and the log line carries the constant reason. Persisted state: the INSERT failed, nothing was written. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the caller gets the original value and a log line instead of a TypeError.",
  "Premise: `lifecycleEventRepo.ts` read whole",
  't95_p1.ts.txt',
  "The database client is a plain stand-in whose `$executeRaw` rejects with the cell's value; the logger is a plain object that records `error` lines; no network, no database.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'originate_lifecycle_event_repo_create_catch_guard_message',
  "At the tip the catch throws a TypeError instead of rethrowing the value, so the assertion fails",
  reuse=REUSE_E, runner='jest', ref=JREF,
  testbase='ks1868-lifecycle-event-repo-create-catch-unreadable-throw.test.ts')

# ---- P2: originate shareRepo.createShare (jest)
SH_O="  } catch (err: any) {\n    const msg = err instanceof Error ? err.message : String(err);\n    if (msg.includes('null value in column \"target_id\"')) {\n"
SH_N="  } catch (err: any) {\n"+gv(4,'msg',SEXPR)+"    if (msg.includes('null value in column \"target_id\"')) {\n"
site('p2','originate','src/repositories/shareRepo.ts',[(SH_O,SH_N)],1,
  '139-140 (the catch of `createShare`)',
  'the catch of `createShare` in `src/repositories/shareRepo.ts`',
  'the unguarded thrown-value read in the ONE catch of `createShare`; the other functions of the file are deliberately NOT touched',
  std_what("The catch of `createShare` (a failed INSERT) reads `err instanceof Error ? err.message : String(err)` into `msg`;", "the catch throws a TypeError before it logs and before its own `throw err`, so the caller never sees the error the database raised and the failure is not logged", " Every other path of the catch (the NOT NULL mapping to `SHARE_TARGET_NOT_FOUND`, the log line, the rethrow of the original value) is unchanged."),
  "CALLERS: the share routes await `createShare` per recipient and map `SHARE_TARGET_NOT_FOUND` to 404; any other rejection reaches the route's own error path. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `logger.error('createShare failed', { targetType, error: <message> })` and the SAME value rethrown. Today (hostile value): a TypeError is thrown instead, nothing is logged. After: the original value is rethrown and the log line carries the constant reason. Persisted state: the INSERT failed, nothing was written. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the caller gets the original value and a log line instead of a TypeError.",
  "Premise: `shareRepo.ts` read whole",
  't95_p2.ts.txt',
  "The database client is a plain stand-in whose `$executeRaw` rejects with the cell's value; the logger is a plain object that records `error` lines; no network, no database. There is no existing suite for this file: the new file stands alone.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'originate_share_repo_create_share_catch_guard_message',
  "At the tip the catch throws a TypeError instead of rethrowing the value, so the assertion fails",
  reuse=REUSE_E, runner='jest', ref=JREF,
  testbase='ks1868-share-repo-create-share-catch-unreadable-throw.test.ts')

# ---- P3: demo-service routes/reset.ts (vitest)
RS_O="    const message = err instanceof Error ? err.message : 'Unknown error';\n    const failedStep = message.includes('pg_restore') ? 'database' : 'redis';\n"
RS_N=gv(4,'message',"err instanceof Error ? err.message : 'Unknown error'")+"    const failedStep = message.includes('pg_restore') ? 'database' : 'redis';\n"
RS_O="    const totalDurationMs = Date.now() - overallStart;\n"+RS_O
RS_N="    const totalDurationMs = Date.now() - overallStart;\n"+RS_N
site('p3','demo-service','src/routes/reset.ts',[(RS_O,RS_N)],1,
  '63-64 (the catch of `POST /reset`)',
  'the catch of the `POST /reset` handler in `src/routes/reset.ts`',
  'the unguarded thrown-value read in the ONE catch of the reset handler',
  std_what("The catch of the `POST /reset` handler reads `err instanceof Error ? err.message : 'Unknown error'` into `message`;", "the handler REJECTS before it answers (Express 4 does not await a handler, so the request gets no response at all), where an ordinary Error gets the 500 body with `failedStep`"),
  "CALLERS: the demo toolbar posts to `/demo-api/reset` behind the demo key; the handler awaits `resetDatabase` then `resetRedis`. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged and the handler answers 500 `{ success: false, error: { code: 'INTERNAL_ERROR', message, failedStep } }`. Today (hostile value): the handler rejects and no response is sent. After: the same 500 with the constant reason. Persisted state: none beyond what the failed steps did. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the request is answered 500 instead of left open.",
  "Premise: `reset.ts` read whole",
  't95_p3.ts.txt',
  "The reset service is replaced by plain functions (`resetDatabase` rejects with the cell's value); the route handler is read off `resetRouter.stack` and called with a duck-typed response; the logger is a plain no-op object; no network, no Express server.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'demo_service_reset_route_catch_guard_message',
  "At the tip the catch throws (the handler rejects), so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'demo-service/src/__tests__/ks1868-persona-switch-unreadable-throw.test.ts',
  testbase='ks1868-demo-service-reset-route-catch-unreadable-throw.test.ts')

# ---- P4: demo-service services/resetService.ts (vitest, 2 hunks)
RD_O="    const message = err instanceof Error ? err.message : 'Unknown pg_restore error';\n"
RD_N=gv(4,'message',"err instanceof Error ? err.message : 'Unknown pg_restore error'")
RR_O="    const message = err instanceof Error ? err.message : 'Unknown Redis error';\n"
RR_N=gv(4,'message',"err instanceof Error ? err.message : 'Unknown Redis error'")
site('p4','demo-service','src/services/resetService.ts',[(RD_O,RD_N),(RR_O,RR_N)],2,
  '70-71 and 111-112 (the catches of `resetDatabase` and `resetRedis`)',
  'the two catches of `resetDatabase` and `resetRedis` in `src/services/resetService.ts`',
  'the unguarded thrown-value read in each of the TWO catches (`resetDatabase`, `resetRedis`)',
  "Each catch reads `err instanceof Error ? err.message : '<default>'` into `message` with no guard, then logs it and rethrows a descriptive Error (`pg_restore failed: <message>`, `Redis flush failed: <message>`). A thrown value whose read throws (a revoked Proxy: `instanceof` throws on it; an Error whose `message` getter throws) makes the catch throw a bare TypeError first, so the caller gets neither the descriptive Error nor a reason. The fix is the house guard placed in each catch: read the value inside its own `try` and fall back to the constant `'unreadable thrown value'` when the read throws. The message text of every value that can be read is unchanged; `resetRedis` still quits the client in its `finally`.",
  "CALLERS: `POST /demo-api/reset` (`src/routes/reset.ts`) awaits both and answers from the message (its own catch is a separate site, NOT touched here). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at error level and the call rejects with `pg_restore failed: <message>` / `Redis flush failed: <message>`. Today (hostile value): a TypeError. After: the descriptive Error with the constant reason. Persisted state: none beyond what the failed step did. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the call rejects with the descriptive Error and the constant reason instead of a TypeError.",
  "Premise: `resetService.ts` read whole",
  't95_p4.ts.txt',
  "`child_process.execFile` is a plain function calling its callback with the cell's value; the `ioredis` default export is a plain class whose `dbsize` rejects with the cell's value; `fs.accessSync` is spied to succeed; the logger is a plain no-op object; no pg_restore, no Redis.",
  '8 cells: C1 to C4 controls, R1 to R4 red',
  "'control ks1868 C1' to 'C4' (an ordinary Error and a thrown plain string through each of the two functions), already true at the tip (4 cells)",
  "`R1` to `R4` (a revoked Proxy and an Error whose message getter throws through each of the two functions) (4 cells)", 4,
  'demo_service_reset_service_catches_guard_message',
  "At the tip the catch throws a TypeError whose message differs from the descriptive one, so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'demo-service/src/__tests__/ks1868-persona-switch-unreadable-throw.test.ts',
  testbase='ks1868-demo-service-reset-service-catches-unreadable-throw.test.ts')

# ---- P5: auth services/email.ts getAcsClient init catch (vitest)
EM_O="    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${err?.message}`);\n"
EM_N=("    let reason: string;\n    try {\n      reason = String(err?.message);\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n"
      "    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${reason}`);\n")
site('p5','auth','src/services/email.ts',[(EM_O,EM_N)],1,
  '139-140 (the catch of `getAcsClient`)',
  'the init catch of `getAcsClient` in `src/services/email.ts`',
  'the unguarded `${err?.message}` read in the ONE init catch of `getAcsClient`; the two send catches of the file already carry the guard',
  "The init catch of `getAcsClient` builds its `console.error` line with `${err?.message}` INSIDE a template literal, unguarded. A thrown value whose read throws (a revoked Proxy: property reads throw on it; an Error whose `message` getter throws) makes the template throw INSIDE the catch, so `getAcsClient` and with it `sendEmail` REJECT, where an ordinary Error logs the line, answers `null` and lets `sendEmail` fall through to SMTP. The fix is the guard the two send catches of this file already use (`String(err?.message)` read inside its own `try`, the constant `'unreadable thrown value'` when the read throws), placed in the init catch. The logged text of every value that can be read is unchanged (a value with no message still logs `undefined`).",
  "CALLERS: `sendViaAcs` awaits `getAcsClient` and `sendEmail` awaits `sendViaAcs` (account recovery, verification and notification mail). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `[Email] Failed to init ACS client (will fall back to SMTP): <message>` on `console.error`, `null` returned, `sendEmail` goes on to SMTP. Today (hostile value): the call rejects, the SMTP fallback is never tried. After: the same line with the constant reason and the SMTP fallback. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, mail falls back to SMTP instead of failing.",
  "Premise: `email.ts` read whole",
  't95_p5.ts.txt',
  "The ACS SDK is a plain class whose constructor throws the cell's value; nodemailer is a plain transport that succeeds; the provider variables are set before the module is loaded; `console.error` is a plain function that records its arguments; no network.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'auth_email_get_acs_client_init_catch_guard_message',
  "At the tip the catch throws (sendEmail rejects), so the assertion fails",
  reuse=REUSE_Q, runner='vitest', ref=SV+'auth/src/__tests__/ks1868-email-send-catches-unreadable-throw.test.ts',
  testbase='ks1868-email-acs-client-init-catch-unreadable-throw.test.ts')

# ---- P6: packages/shared prism/identus-client.ts resolveDID (vitest)
ID_O="    } catch (err) {\n      return {\n        didDocument: null,\n        didResolutionMetadata: {\n          error: 'notFound',\n          errorMessage: err instanceof Error ? err.message : String(err),\n        },\n"
ID_N="    } catch (err) {\n"+gv(6,'errorMessage',SEXPR)+"      return {\n        didDocument: null,\n        didResolutionMetadata: {\n          error: 'notFound',\n          errorMessage,\n        },\n"
site('p6','shared','src/prism/identus-client.ts',[(ID_O,ID_N)],1,
  '130-137 (the catch of `IdentusClient.resolveDID`)',
  'the catch of `IdentusClient.resolveDID` in `src/prism/identus-client.ts`',
  'the unguarded thrown-value read in the ONE catch of `resolveDID`; the other methods of the file are deliberately NOT touched',
  std_what("The catch of `resolveDID`, a resolver whose failure is the result `didDocument: null` with `didResolutionMetadata.error: 'notFound'`, reads `err instanceof Error ? err.message : String(err)` into `errorMessage`;", "`resolveDID` REJECTS, where an ordinary Error gives the notFound result"),
  "CALLERS: the PRISM resolver paths of the shared package (`resolveDID` is the DID-resolution entry of the Identus client; callers read `didResolutionMetadata.error` rather than catch). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ didDocument: null, didResolutionMetadata: { error: 'notFound', errorMessage: <message> }, didDocumentMetadata: {} }`. Today (hostile value): the call rejects. After: the same result with the constant reason. Persisted state: none (a read). **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the resolver answers notFound with the constant reason instead of rejecting.",
  "Premise: `identus-client.ts` read whole",
  't95_p6.ts.txt',
  "The global `fetch` is a plain function rejecting with the cell's value (stubbed with `vi.stubGlobal`, removed after each cell); the logger is a plain no-op object; no network.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'shared_identus_client_resolve_did_catch_guard_message',
  "At the tip the catch throws (the call rejects), so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'../packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts',
  testbase='ks1868-identus-client-resolve-did-catch-unreadable-throw.test.ts')
for _f in ('prod','test','rdir'):
    T['p6'][_f]=T['p6'][_f].replace('services/shared','packages/shared')
T['p6']['ref']=T['p6']['ref'].replace('services/../','')
T['p6']['sib']="`ks1868-response-cache-read-unreadable-throw.test.ts` and `ks1868-audit-logger-flush-unreadable-throw.test.ts`"

# ---- P7: packages/shared resilience/service-client.ts healthCheck (vitest)
SC_O="    } catch (error) {\n      return {\n        healthy: false,\n        latencyMs: Date.now() - start,\n        error: error instanceof Error ? error.message : 'Unknown error',\n      };\n"
SC_N="    } catch (error) {\n"+gv(6,'reason',"error instanceof Error ? error.message : 'Unknown error'")+"      return {\n        healthy: false,\n        latencyMs: Date.now() - start,\n        error: reason,\n      };\n"
site('p7','shared','src/resilience/service-client.ts',[(SC_O,SC_N)],1,
  '156-161 (the catch of `ServiceClient.healthCheck`)',
  'the catch of `ServiceClient.healthCheck` in `src/resilience/service-client.ts`',
  'the unguarded thrown-value read in the ONE catch of `healthCheck`; the request path and the circuit breaker are deliberately NOT touched',
  std_what("The catch of `healthCheck`, a probe whose failure is the result `{ healthy: false, latencyMs, error }`, reads `error instanceof Error ? error.message : 'Unknown error'` into the `error` field;", "`healthCheck` REJECTS, where an ordinary Error gives the unhealthy result"),
  "CALLERS: the shared service client is the inter-service HTTP wrapper; `healthCheck` is the probe callers use to check a peer service, deliberately outside the circuit breaker. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ healthy: false, latencyMs, error: <message> }`. Today (hostile value): the call rejects. After: the same result with the constant reason. Persisted state: none (a probe). **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, the probe answers unhealthy with the constant reason instead of rejecting.",
  "Premise: `service-client.ts` read whole",
  't95_p7.ts.txt',
  "The global `fetch` is a plain function rejecting with the cell's value (stubbed with `vi.stubGlobal`, removed after each cell); `setTimeout`/`clearTimeout` are faked so the 5 s abort timer does not outlive the cell; the logger factory is a plain no-op object; no network.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'shared_service_client_health_check_catch_guard_message',
  "At the tip the catch throws (the probe rejects), so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'../packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts',
  testbase='ks1868-service-client-health-check-catch-unreadable-throw.test.ts')
for _f in ('prod','test','rdir'):
    T['p7'][_f]=T['p7'][_f].replace('services/shared','packages/shared')
T['p7']['ref']=T['p7']['ref'].replace('services/../','')
T['p7']['sib']="`ks1868-response-cache-read-unreadable-throw.test.ts` and `ks1868-audit-logger-flush-unreadable-throw.test.ts`"

# ---- P8: packages/shared vc/verifier.ts verifySignature outer catch (vitest)
VF_O="    } catch (err: unknown) {\n      const msg = err instanceof Error ? err.message : String(err);\n      errors.push(`Signature verification error: ${msg}`);\n"
VF_N="    } catch (err: unknown) {\n"+gv(6,'msg',SEXPR)+"      errors.push(`Signature verification error: ${msg}`);\n"
site('p8','shared','src/vc/verifier.ts',[(VF_O,VF_N)],1,
  '417-418 (the outer catch of `verifySignature`)',
  'the outer catch of `verifySignature` in `src/vc/verifier.ts`',
  'the unguarded thrown-value read in the OUTER catch of `verifySignature` (the one that records `Signature verification error: <msg>`); the inner Ed25519 catch (`verifyErr`) and every other method are deliberately NOT touched',
  std_what("The outer catch of `verifySignature`, whose failure is the error entry `Signature verification error: <msg>` in a `{ valid: false, errors }` result, reads `err instanceof Error ? err.message : String(err)` into `msg`;", "`verifySignature` REJECTS, where an ordinary Error gives the error entry"),
  "CALLERS: `verify` awaits `verifySignature` while checking a credential (the vc-issuer verify routes call it); a rejection there escapes the verifier instead of becoming a failed verification. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): `{ valid: false, errors: ['Signature verification error: <message>'] }`. Today (hostile value): the call rejects. After: the same result with the constant reason. Persisted state: none (a read). The test reaches the catch with a DID resolver that rejects, through an HMAC-form proof (`zHMAC_` prefix). **BEHAVIOUR CHANGE the raise PR must state:** for a thrown value that cannot be read, verification fails with the constant reason instead of rejecting.",
  "Premise: `verifier.ts` read from line 300 to 430 (the signature method), the proof branches at 350-424 confirmed",
  't95_p8.ts.txt',
  "The DID resolver is a plain function rejecting with the cell's value; `verifySignature` is private and is reached through a type cast; the proof is an HMAC-form proof so the resolver is the only thing that can throw; no network, no key material.",
  '4 cells: C1, C2 controls, R1, R2 red',
  "'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown plain string), both already true at the tip (2 cells)",
  "`R1`, `R2` (a revoked Proxy, an Error whose message getter throws) (2 cells)", 2,
  'shared_vc_verifier_verify_signature_outer_catch_guard_message',
  "At the tip the catch throws (the call rejects), so the assertion fails",
  reuse=REUSE_E, runner='vitest', ref=SV+'../packages/shared/src/__tests__/ks1868-response-cache-read-unreadable-throw.test.ts',
  testbase='ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts')
for _f in ('prod','test','rdir'):
    T['p8'][_f]=T['p8'][_f].replace('services/shared','packages/shared')
T['p8']['ref']=T['p8']['ref'].replace('services/../','')
T['p8']['sib']="`ks1868-response-cache-read-unreadable-throw.test.ts` and `ks1868-audit-logger-flush-unreadable-throw.test.ts`"
