# Operator 86 sites: KS-1868 unguarded thrown-value reads (re-screened at 9a9bf86967e3).
SV='Blockchain/Dev/services/'
SOr=SV+'originate/'
def hguard(ind,expr="err instanceof Error ? err.message : String(err)"):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
REFO=SOr+'src/__tests__/ks1868-anchors-route-catches-unreadable-throw.test.ts'
WHY=("The catch logs `{ error: err instanceof Error ? err.message : String(err) }` with the read INSIDE the logger call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy: `instanceof` throws; a Proxy whose `getPrototypeOf` trap throws; an Error whose `message` getter throws) therefore throws INSIDE the catch, so the function REJECTS instead of answering what its catch is written to answer. The fix is the guard ALREADY in this module (the sibling `trackError` catch, a few lines above, merged under KS-1868): `let reason: string; try { reason = err instanceof Error ? err.message : String(err); } catch { reason = 'unreadable thrown value'; }` placed before the logger call, then `error: reason`. The expression is unchanged, so every value that could be read before is logged exactly as before.")
COMMON=dict(key='KS-1868', runner='jest', runcmd='', rdir=SOr[:-1], ref=REFO,
  reuse="This follows the guard that the SAME module already carries in `trackError` (merged KS-1868 pass: the read inside a `try`, the constant `'unreadable thrown value'` on throw), copied inline; no helper is added.",
  sib="`ks1868-anchors-route-catches-unreadable-throw.test.ts`")
T={}
P1=SOr+'src/services/errorTrackingService.ts'
E1=("  } catch (err: any) {\n    logger.error('Failed to query errors', { error: err instanceof Error ? err.message : String(err) });\n    return { errors: [], total: 0 };\n",
    "  } catch (err: any) {\n"+hguard(4)+"    logger.error('Failed to query errors', { error: reason });\n    return { errors: [], total: 0 };\n")
T['p1']=dict(COMMON, dir='ks_1868_o86_p1_originate_error_tracking_get_recent_errors_catch_guard', prod=P1, edits=[E1], nh=1,
  lines='141 (the catch of `getRecentErrors`)',
  test=SOr+'src/__tests__/ks1868-error-tracking-get-recent-errors-catch-unreadable-throw.test.ts', tsrc='t86_p1.ts.txt',
  fn='the catch of `getRecentErrors` in `src/services/errorTrackingService.ts`',
  short='the unguarded thrown-value read in the ONE catch of `getRecentErrors`',
  premise="`%s` lines 140-143 pass `error: err instanceof Error ? err.message : String(err)` straight into `logger.error` with no guard around the read, while the sibling `trackError` catch (lines 63-72) already guards the same read" % P1,
  whatwrong=WHY,
  callers="CALLERS: `routes/systemErrors.ts` (the GET list of system errors, an admin dashboard route). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a rejection of the database read is logged at error level and `getRecentErrors` answers `{ errors: [], total: 0 }` (the dashboard shows an empty list). Today (hostile value): the catch throws while building the log arguments, so `getRecentErrors` REJECTS and the route answers its generic 500. After: the empty list, exactly as for an ordinary Error. Persisted state: identical in both cases (a read; nothing is written by the catch). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown value only, the system-errors list answers an empty list (and logs a text line) instead of the generic 500; every Error with a readable message and every non-Error throw behave exactly as before. TIER 3 (admin dashboard read, originate).",
  ncells='7 cells: C1 to C4 controls, R1 to R3 red',
  red1="At the tip the catch throws (the function rejects, no error line is logged), so the assertion fails",
  dbnote="The `../db` module (`prisma.$queryRaw` rejecting with the thrown value through a plain async function) and `../utils/logger` are plain stand-ins; the real service module runs; no database.",
  greens="'control ks1868 C1' (an ordinary Error), 'C2' (a thrown plain string), 'C3' (a thrown number) and 'C4' (an Error with an empty message), all already true at the tip (4 cells)",
  redcells="`R1` to `R3` (the database read rejects with a revoked Proxy, a Proxy whose getPrototypeOf trap throws, an Error whose message getter throws) (3 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,4)))

# ---- P2: auth services/email.ts ACS + SMTP send catches (vitest)
SA=SV+'auth/'
PE=SA+'src/services/email.ts'
def tguard(ind,v,expr):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = String(%s);\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
EE1=("  } catch (err: any) {\n    console.error(`[Email/ACS] Send threw for ${options.to}: ${err?.message}`);\n",
     "  } catch (err: any) {\n"+tguard(4,'err','err?.message')+"    console.error(`[Email/ACS] Send threw for ${options.to}: ${reason}`);\n")
EE2=("  } catch (error: any) {\n    console.error(`[Email/SMTP] Failed to send to ${options.to}: ${error.message}`);\n",
     "  } catch (error: any) {\n"+tguard(4,'error','error.message')+"    console.error(`[Email/SMTP] Failed to send to ${options.to}: ${reason}`);\n")
WHY2=("The two catches build their `console.error` line with the thrown value's message read INSIDE a template literal, unguarded: `${err?.message}` (ACS) and `${error.message}` (SMTP). A thrown value whose read throws (a revoked Proxy; an Error whose `message` getter throws) or whose message cannot be turned into text (a Symbol, which a template literal refuses) therefore throws INSIDE the catch, so `sendEmail` REJECTS instead of answering. The fix is a guard placed before the console line: `let reason: string; try { reason = String(<the same read>); } catch { reason = 'unreadable thrown value'; }`, then `${reason}`. `String(x)` of every value that was readable text before gives the same text a template literal gave (a string stays, `undefined` stays `undefined`), so every line that could be written before is written byte for byte as before.")
T['p2']=dict(COMMON, runner='vitest', runcmd='run ', rdir=SA[:-1], ref=SA+'src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts',
  sib="`ks1868-oauth-authorize-token-unreadable-throw.test.ts` and `ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts`",
  reuse="This follows the guard that the merged and held KS-1868 passes use (operator 85 `password.ts`: the read inside a `try`, the constant `'unreadable thrown value'` on throw) before the log call; no helper exists in this file and none is added.",
  dir='ks_1868_o86_p2_auth_email_acs_smtp_send_catches_guard_message', prod=PE, edits=[EE1,EE2], nh=2,
  lines='167 (the ACS send catch in `sendViaAcs`) and 207 (the SMTP send catch in `sendEmail`)',
  test=SA+'src/__tests__/ks1868-email-send-catches-unreadable-throw.test.ts', tsrc='t86_p2.ts.txt',
  fn='the ACS and SMTP send catches of `src/services/email.ts`',
  short='the unguarded thrown-value read in TWO send catches (ACS, SMTP)',
  premise="`%s` lines 166-169 and 206-209 read the thrown value's message inside a template literal passed to `console.error` with no guard, in functions that answer false (ACS: then fall through to SMTP) when a provider fails" % PE,
  whatwrong=WHY2,
  callers="CALLERS: `sendVerificationEmail`, `sendPasswordResetEmail` and the other send helpers of the same file, called by `routes/auth.ts` (register, verify, reset flows). WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): at 167 a rejection of the ACS send is logged, `sendViaAcs` answers false and `sendEmail` falls through to the SMTP provider if one is configured, else answers false; at 207 a rejection of the SMTP send is logged and `sendEmail` answers false. Today (hostile value): each catch throws while building the log line, so `sendEmail` REJECTS (at 167 the SMTP fallback is never tried). After: exactly the ordinary-Error row at both sites. Persisted state: identical in both cases (nothing is written; at worst one more provider is tried at 167, as for an ordinary Error). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-text-message thrown value only, a failed ACS send falls through to SMTP as documented and a failed SMTP send answers false, both logged, instead of `sendEmail` rejecting into the calling route; a thrown `null` or `undefined` at 207 (which read `error.message` and threw a TypeError) now also answers false; every readable message and every other throw behave exactly as before. TIER 2 (transactional email, auth).",
  ncells='10 cells: C1 to C4 controls, R1 to R6 red',
  red1="At the tip the catch throws (sendEmail rejects) or the line is not written, so the assertion fails",
  dbnote="The ACS SDK (`@azure/communication-email`, a stand-in `EmailClient` whose `beginSend` rejects with the thrown value or resolves a Failed poller) and `nodemailer` (a stand-in transport whose `sendMail` rejects with the thrown value or resolves) are plain stand-ins, the provider variables are set before the real module is loaded, and `console.error` is a plain recording function; no network.",
  greens="'control ks1868 C1' (an ordinary Error from ACS), 'C2' (an ordinary Error from SMTP), 'C3' (a thrown number from ACS) and 'C4' (a thrown plain string from SMTP), all already true at the tip (4 cells)",
  redcells="`R1` to `R3` (the ACS client rejects with a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) and `R4` to `R6` (the same three shapes from the SMTP transport) (6 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,7)))

# ---- P3 / P4: kyc + wallet-connector user.erased handler-failed catch (vitest)
def guard(ind):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"try {\n"+s+"  const m = err?.message;\n"+s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
WHYC=("The handler-failed catch logs `{ userId, dsrId, error: err?.message }` with the read INSIDE the log call's arguments, unguarded, and then rethrows the original value (`throw err`) so the event bus retries and dead-letters. A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the catch, BEFORE the log line is written and before the rethrow, so the bus receives a different error (the one the read threw) and the failure is not logged; an Error whose `message` is readable but not a string (a null-prototype object, a Symbol) is handed to the log uncoerced. The fix is the house guard placed before the log call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The `throw err` line is untouched.")
def cascade(k, svc, fn, ctxlines, edits_old, ln, callers_extra, tsrc, dbnote, premise_ln):
    PROD=SV+svc+'/src/userErasedSubscriber.ts'
    old,new=edits_old
    E=(old, new)
    return dict(COMMON, runner='vitest', runcmd='run ', rdir=SV+svc, ref=SV+'auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts',
      sib="`ks1868-oauth-authorize-token-unreadable-throw.test.ts` and `ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts`",
      reuse="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (operator 81 `security/src/db.ts`, operator 82 `routes/internal.ts`, operator 85 `accountLockout.ts`: `const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw) before the log call; no helper exists in this file and none is added.",
      dir='ks_1868_o86_%s_%s_user_erased_handler_failed_catch_guard_message'%(k,svc.replace('-','_')), prod=PROD, edits=[E], nh=1,
      lines='%d (the handler-failed catch inside the `user.erased` subscription)'%ln,
      test=SV+svc+'/src/__tests__/ks1868-'+svc+'-user-erased-handler-failed-catch-unreadable-throw.test.ts', tsrc=tsrc,
      fn='the handler-failed catch of `startUserErasedSubscriber` in `src/userErasedSubscriber.ts`',
      short='the unguarded thrown-value read in the ONE handler-failed catch of the `user.erased` subscriber',
      premise=premise_ln,
      whatwrong=WHYC,
      callers=callers_extra,
      ncells='6 cells: C1 to C3 controls, R1 to R3 red',
      red1="At the tip the catch throws a different error before logging (the rethrown value is not the original and no failure line is logged) or the logged value is not text, so the assertion fails",
      dbnote=dbnote,
      greens="'control ks1868 C1' (an ordinary Error), 'C2' (a thrown plain string) and 'C3' (an Error with an empty message), all already true at the tip (3 cells)",
      redcells="`R1` to `R3` (the delete step rejects with a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (3 cells)",
      redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,4)))
KYC_OLD="      } catch (err: any) {\n        log('error', '[cascade] user.erased handler failed', {\n          userId,\n          dsrId,\n          error: err?.message,\n        });\n        throw err; // let bus retry + dead-letter\n"
KYC_NEW="      } catch (err: any) {\n"+guard(8)+"        log('error', '[cascade] user.erased handler failed', {\n          userId,\n          dsrId,\n          error: reason,\n        });\n        throw err; // let bus retry + dead-letter\n"
T['p3']=cascade('p3','kyc','', '', (KYC_OLD,KYC_NEW), 38,
  "CALLERS: `src/index.ts` (line 1317) starts the subscriber at boot with the service's `log` and its `dbDeleteUserData`; the event bus calls the handler for every `user.erased` event. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a rejection of the delete step is logged at error level with the user and DSR ids and the SAME error is rethrown, so the bus retries up to its maximum and then dead-letters the event. Today (hostile value): the catch throws while building the log arguments, so the failure is NOT logged and the bus is handed a different error (the one the read threw); it still sees a failure and retries and dead-letters the same way. After: the failure is logged and the original value is rethrown, exactly as for an ordinary Error. Persisted state: identical in both cases (the delete step already ran or failed before the catch; the catch writes nothing, and the retry decision is the bus's, unchanged). The change adds no outcome an ordinary Error does not already produce. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, the GDPR erasure failure is logged and the original value is rethrown to the bus (instead of the log being lost and a different error being thrown); a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 2 (erasure-cascade failure path, logging only; kyc).",
  't86_p3.ts.txt',
  "The `@secuura/shared` module is the real one with `initEventBus` and `getEventBus` replaced (the stand-in `subscribe` hands over the handler and returns a promise that never settles); the log function and the delete step are plain functions (the delete step rejects with the thrown value); the real subscriber module runs; no Redis, no database.",
  "`Blockchain/Dev/services/kyc/src/userErasedSubscriber.ts` lines 38-45 pass `error: err?.message` straight into `log` with no guard around the read, in a catch that then rethrows `err` for the bus to retry and dead-letter")
WC_OLD="      } catch (err: any) {\n        log('error', '[cascade] user.erased handler failed', {\n          userId,\n          dsrId,\n          error: err?.message,\n        });\n        throw err;\n"
WC_NEW="      } catch (err: any) {\n"+guard(8)+"        log('error', '[cascade] user.erased handler failed', {\n          userId,\n          dsrId,\n          error: reason,\n        });\n        throw err;\n"
T['p4']=cascade('p4','wallet-connector','', '', (WC_OLD,WC_NEW), 49,
  "CALLERS: `src/server.ts` (line 318) starts the subscriber at boot with the service's `log` and its `query`; the event bus calls the handler for every `user.erased` event that carries a `walletAddress` (the delete of the wallet sessions is skipped otherwise). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a rejection of the `DELETE FROM svc_wallet_sessions` is logged at error level with the user, DSR and wallet and the SAME error is rethrown, so the bus retries up to its maximum and then dead-letters the event. Today (hostile value): the catch throws while building the log arguments, so the failure is NOT logged and the bus is handed a different error (the one the read threw); it still sees a failure and retries and dead-letters the same way. After: the failure is logged and the original value is rethrown, exactly as for an ordinary Error. Persisted state: identical in both cases (the DELETE already ran or failed before the catch; the catch writes nothing, and the retry decision is the bus's, unchanged). The change adds no outcome an ordinary Error does not already produce. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, the GDPR wallet-session erasure failure is logged and the original value is rethrown to the bus (instead of the log being lost and a different error being thrown); a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 2 (erasure-cascade failure path, logging only; wallet-connector).",
  't86_p4.ts.txt',
  "The `@secuura/shared` module is the real one with `initEventBus` and `getEventBus` replaced (the stand-in `subscribe` hands over the handler and returns a promise that never settles); the log function and the `query` function are plain functions (the query rejects with the thrown value); the real subscriber module runs; no Redis, no database.",
  "`Blockchain/Dev/services/wallet-connector/src/userErasedSubscriber.ts` lines 49-56 pass `error: err?.message` straight into `log` with no guard around the read, in a catch that then rethrows `err` for the bus to retry and dead-letter")

# ---- P5: transfer approvalWorkflowService.ts seed / probe / escalation catches (vitest)
PT=SV+'transfer/src/services/approvalWorkflowService.ts'
def Eg(old_line, ind, cons):
    return ("%s} catch (err: any) {\n%s" % (' '*(ind-2), old_line),
            "%s} catch (err: any) {\n%s%s" % (' '*(ind-2), guard(ind), old_line.replace('err?.message','reason')))
ET1=Eg("      console.error(`[approvalWorkflowService] Failed to seed workflow ${wf.id}:`, err?.message);\n",6,0)
ET2=Eg("    console.warn('[approvalWorkflowService] DB tables not ready:', err?.message);\n",4,0)
ET3=Eg("      console.error('[approvalWorkflowService] processEscalations error:', err?.message);\n",6,0)
WHYT=("Three catches of this module pass `err?.message` straight into `console.error` / `console.warn` as an argument, with the read INSIDE the call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the catch, so `verifyDbReady` (the boot probe, which documents that a missing table is only a warning) and `processEscalations` (which answers its zero counts) REJECT instead; an Error whose `message` is readable but not a string (a null-prototype object, a Symbol) is handed to the console uncoerced. The fix is the house guard placed before each console call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `reason` in place of `err?.message`.")
T['p5']=dict(COMMON, runner='vitest', runcmd='run ', rdir=SV+'transfer', ref=SV+'auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts',
  sib="`ks1868-oauth-authorize-token-unreadable-throw.test.ts` and `ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts`",
  reuse="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (operator 81 `security/src/db.ts`, operator 82 `routes/internal.ts`, operator 85 `accountLockout.ts`: `const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw) before the call; no helper exists in this file and none is added.",
  dir='ks_1868_o86_p5_transfer_approval_workflow_seed_probe_escalation_catches_guard_message', prod=PT, edits=[ET1,ET2,ET3], nh=3,
  lines='345 (the seed-upsert catch of `seedDefaultWorkflows`), 356 (the DB-not-ready catch of `verifyDbReady`) and 629 (the catch of `processEscalations`)',
  test=SV+'transfer/src/__tests__/ks1868-approval-workflow-catches-unreadable-throw.test.ts', tsrc='t86_p5.ts.txt',
  fn='the console-argument catches of `src/services/approvalWorkflowService.ts`',
  short='the unguarded thrown-value read in THREE catches (seed, DB-not-ready probe, escalations)',
  premise="`%s` lines 345, 356 and 629 pass `err?.message` straight into `console.error` / `console.warn` with no guard around the read, in functions whose catches are written to swallow a database failure (the seed and probe at boot, the escalation sweep)" % PT,
  whatwrong=WHYT,
  callers="CALLERS: `src/index.ts` (lines 44-45) runs `verifyDbReady` at boot (it calls `seedDefaultWorkflows` after a probe query); `routes/workflows.ts` (line 223) calls `processEscalations` from the escalate route. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): at 345 a rejection of one workflow upsert is logged and the loop goes on with the next workflow; at 356 a rejection of the probe or of the seeding is logged as a warning and `verifyDbReady` resolves (the service starts; the tables are created elsewhere); at 629 a rejection of the overdue-steps read (or of a step write) is logged and `processEscalations` returns the counts reached so far (zero when the read itself failed). Today (hostile value): each catch throws while building the call's arguments, so at 345 the seed loop is abandoned and the error reaches the catch at 356, which throws again and `verifyDbReady` REJECTS to the boot caller, and `processEscalations` REJECTS to its route. After: exactly the ordinary-Error row at all three sites. Persisted state: identical in both cases (the guards sit only in the catches; the loop continuing at 345 upserts the remaining default workflows exactly as it does after an ordinary Error; at 629 a step write that already ran is not undone). The change moves a hostile failure TOWARD the already documented outcome; it adds no outcome an ordinary Error does not already produce. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, the boot probe and the seeding carry on and log (instead of `verifyDbReady` rejecting), and the escalation sweep returns its counts (instead of rejecting into the route); a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 2 (approval workflow boot probe and escalation sweep; transfer).",
  ncells='10 cells: C1 to C4 controls, R1 to R6 red',
  red1="At the tip the catch throws while building the call's arguments (the function rejects) or the logged value is not text, so the assertion fails",
  dbnote="The `../db` module (`query` rejecting with the thrown value through a plain function, `isDbAvailable` true) and `./delegationService` are plain stand-ins; `console.error` and `console.warn` are plain recording functions; the real workflow module runs; no database.",
  greens="'control ks1868 C1' (an ordinary Error at the boot probe), 'C2' (an ordinary Error at every seed upsert), 'C3' (an ordinary Error in processEscalations) and 'C4' (a thrown plain string in processEscalations), all already true at the tip (4 cells)",
  redcells="`R1`, `R2` (the probe rejects with a revoked Proxy, an Error whose message is a Symbol), `R3`, `R4` (the seed upserts reject with the same two) and `R5`, `R6` (processEscalations' read rejects with the same two) (6 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,7)))

# ---- P6: analytics db.ts pool error listener + boot-work catch (vitest)
PAN=SV+'analytics/src/db.ts'
EA1=("    pool.on('error', (err: Error) => {\n      dbLog('error', 'DB pool unexpected error', { error: err.message });\n    });\n",
     "    pool.on('error', (err: Error) => {\n"+guard(6)+"      dbLog('error', 'DB pool unexpected error', { error: reason });\n    });\n")
EA2=("    // Boot work failing must not un-flag an otherwise reachable DB.\n    dbLog('error', 'DB ready boot work failed', { error: err?.message });\n",
     "    // Boot work failing must not un-flag an otherwise reachable DB.\n"+guard(4)+"    dbLog('error', 'DB ready boot work failed', { error: reason });\n")
WHYA=("Two places in this module pass the thrown value's message straight into `dbLog`'s meta object, unguarded: the pg pool `'error'` listener (`{ error: err.message }`) and the boot-work catch of `runDbReadyHook` (`{ error: err?.message }`). A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the listener or the catch: an exception thrown by a listener of the pool's `'error'` event escapes the EventEmitter as an uncaught exception, and a throwing `runDbReadyHook` makes `initDb` REJECT instead of resolving with the availability flag; an Error whose `message` is readable but not a string (a Symbol) is handed to `JSON.stringify` uncoerced and silently dropped from the line. The fix is the house guard placed before each `dbLog` call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The probe catch of `probeDb` (`return { ok: false, error: err?.message }`, typed `error?: string`) is deliberately NOT touched.")
T['p6']=dict(COMMON, runner='vitest', runcmd='run ', rdir=SV+'analytics', ref=SV+'auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts',
  sib="`ks1868-oauth-authorize-token-unreadable-throw.test.ts` and `ks1868-issuer-certs-list-revoke-unreadable-throw.test.ts`",
  reuse="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (operator 81 `security/src/db.ts`, operator 85 `accountLockout.ts`: `const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw) before the `dbLog` call; no helper exists in this file and none is added.",
  dir='ks_1868_o86_p6_analytics_db_pool_error_and_ready_hook_catches_guard_message', prod=PAN, edits=[EA1,EA2], nh=2,
  lines='36-37 (the pg pool `error` listener in `getPool`) and 96 (the boot-work catch of `runDbReadyHook`)',
  test=SV+'analytics/src/__tests__/ks1868-analytics-db-pool-error-and-ready-hook-unreadable-throw.test.ts', tsrc='t86_p6.ts.txt',
  fn='the pool error listener and the boot-work catch of `src/db.ts`',
  short='the unguarded thrown-value read in the pool error listener and the boot-work catch',
  premise="`%s` line 37 (`{ error: err.message }` in the pool error listener) and line 96 (`{ error: err?.message }` in the `runDbReadyHook` catch) pass the thrown value's message straight into `dbLog` with no guard around the read" % PAN,
  whatwrong=WHYA,
  callers="CALLERS: `getPool` is called by every query of the service; `initDb(onReady)` is called at boot by `src/index.ts` (line 14 imports it) and `runDbReadyHook` also runs on recovery from the background re-probe. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): an error emitted by the pool is logged at error level and the process goes on; a rejection of the onReady boot work is logged at error level (the comment: boot work failing must not un-flag an otherwise reachable DB) and `initDb` resolves with the availability flag (true when the probe succeeded). Today (hostile value): the listener throws while building the meta object, which Node reports as an uncaught exception from the pool's EventEmitter, and `runDbReadyHook` throws so `initDb` REJECTS to the boot caller (and, on a recovery re-probe, to the timer callback as an unhandled rejection). After: exactly the ordinary-Error row at both sites. Persisted state: identical in both cases (nothing is written by either catch; the availability flag is set before the hook runs). The change moves a hostile failure TOWARD the already documented outcome; it adds no outcome an ordinary Error does not already produce. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message thrown value only, a pool error is logged instead of raising an uncaught exception and a failed onReady hook is logged instead of rejecting `initDb`; a Symbol message is logged as its text; every string message, every non-Error throw and every absent message behave exactly as before. TIER 2 (database client of the analytics service).",
  ncells='9 cells: C1 to C4 controls, R1 to R5 red',
  red1="At the tip the listener / the catch throws while building the meta object (the listener call throws; initDb rejects) or the logged value is not text, so the assertion fails",
  dbnote="The `pg` module is a plain stand-in (a `Pool` whose `on` hands over the `error` listener, whose `query` answers the probe and whose other methods are plain functions); `console.log` is a plain recording function; each cell loads a fresh copy of the real `db` module; no database, no network.",
  greens="'control ks1868 C1' (an ordinary Error at the pool listener), 'C2' (a plain string at the listener), 'C3' (an ordinary Error from the onReady hook) and 'C4' (a thrown number from the hook), all already true at the tip (4 cells)",
  redcells="`R1`, `R2` (the pool listener receives a revoked Proxy, an Error whose message is a Symbol) and `R3` to `R5` (the onReady hook rejects with a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (5 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,6)))

# ---- P7: api-gateway db.ts pool error listener + boot-work catch (clone of P6)
PGW=SV+'api-gateway/src/db.ts'
def _rep(v):
    if isinstance(v,str):
        return v.replace('analytics','api-gateway').replace('lines 36-37','lines 37-38').replace('line 37 (','line 37 (').replace('line 96','line 101').replace('and 96 (','and 101 (').replace('36-37 (','37-38 (').replace('p6_','p7_')
    return v
T['p7']={k:_rep(v) for k,v in T['p6'].items()}
T['p7'].update(prod=PGW, edits=[(EA1[0],EA1[1]),(EA2[0],EA2[1])], tsrc='t86_p7.ts.txt', dir='ks_1868_o86_p7_api_gateway_db_pool_error_and_ready_hook_catches_guard_message',
  test=SV+'api-gateway/src/__tests__/ks1868-api-gateway-db-pool-error-and-ready-hook-unreadable-throw.test.ts', rdir=SV+'api-gateway',
  dbnote="The `pg` module is a plain stand-in (a `Pool` whose `on` hands over the `error` listener and whose other methods are plain functions); the shared tenant-GUC query helper `queryWithTenantGuc` is replaced by a plain function that answers the probe (the rest of `@secuura/shared` is the real module); `console.log` is a plain recording function; each cell loads a fresh copy of the real `db` module; no database, no network.")
