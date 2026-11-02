# Operator 88: re-key operator 87's unrun leftovers (P6 events init catch, P9 nft-certificate db.ts, P10 transfer db.ts, P11 wallet-connector db.ts) as O88 passes.
import copy
T["a1"]=copy.deepcopy(T["p1"])  # O87-P1 anchoring listener (held), stash before re-keying
def _rk(old,new,name):
    X=copy.deepcopy(T[old]); X['dir']='ks_1868_o88_%s_%s'%(new,name); T[new]=X
_rk('p6','p1','auth_events_init_catch_guard_message')
_rk('p9','p2','nft_certificate_db_pool_error_and_ready_hook_catches_guard_message')
_rk('p10','p4','transfer_db_pool_error_and_ready_hook_catches_guard_message')
_rk('p11','p5','wallet_connector_db_pool_error_and_ready_hook_catches_guard_message')

# ---- O88-P3: auth events.ts Redis error LISTENER only (:95); the init catch :101 is O88-P1 (disjoint hunks, 6 lines apart)
WHYL=("The Redis client `'error'` listener in `initEventBus` passes the thrown value's message straight into the logger's meta object, unguarded: `{ error: err.message }`. A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the listener, and an exception thrown by a listener of the client's `'error'` event escapes the EventEmitter and is an uncaught exception in the auth process (the very event that says Redis is down turns into a process-level fault); an Error whose `message` is readable but not a string (a Symbol) is passed to the logger uncoerced. The fix is the house guard placed before the logger call: read the message once inside a `try`, keep `undefined`/`null` as they are (they were logged as is), coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The init catch four lines below (line 101) is O88-P1, a separate pass whose hunk is more than 3 lines away; it is NOT part of this pass. The empty catches of `publishEvent` and `shutdownEventBus` read nothing and are untouched.")
X=copy.deepcopy(T['p1'])
X.update(dict(dir='ks_1868_o88_p3_auth_events_redis_error_listener_guard_message', edits=[EV1], nh=1,
  lines='95 (the Redis `error` listener in `initEventBus`)',
  tsrc='t88_p3.ts.txt',
  test=SV+'auth/src/__tests__/ks1868-auth-events-redis-error-listener-unreadable-throw.test.ts',
  fn='the Redis error listener of `src/events.ts`',
  short='the unguarded thrown-value read in the Redis error listener of `initEventBus`',
  premise="`%s` line 95 (`{ error: err.message }` in the Redis `error` listener) passes the thrown value's message straight into the logger with no guard around the read" % PEV,
  whatwrong=WHYL,
  callers="CALLERS: `initEventBus` is called at boot by `src/index.ts`; the listener is attached to the one Redis client for the life of the process. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): an error emitted by the client is logged at debug level and the process goes on. Today (hostile value): the listener throws while building the meta object, which Node reports as an uncaught exception. After: exactly the ordinary-Error row. Persisted state: none (the listener only logs). The change moves a hostile emission TOWARD the already documented outcome; it adds no outcome an ordinary Error does not already produce. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable or non-string-message value emitted on the Redis client's `error` event only, the line is logged at debug instead of an uncaught exception; a Symbol message is logged as its text; every string message, every non-Error and every ordinary Error behaves exactly as before. The init catch at line 101 is a separate pass (O88-P1).",
  ncells='5 cells: C1 to C2 controls, R1 to R3 red',
  red1="At the tip the listener throws while building the meta object (the listener call throws) or the logged value is not text, so the assertion fails",
  dbnote="The `ioredis` module is a plain stand-in class (its `on` hands over the `error` listener); the service logger `./utils/logger` (`createLogger`) is a plain recording object; each cell loads a fresh copy of the real `events` module and calls `initEventBus`; no Redis, no network.",
  greens="'control ks1868 C1' (an ordinary Error at the listener) and 'C2' (a plain string at the listener), both already true at the tip (2 cells)",
  redcells="`R1` to `R3` (the listener receives a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (3 cells)"))
T['p3']=X

# ---- clones of O88-P2 (nft-certificate db.ts: listener :36 + ready-hook catch :96; same code, same lines) and of O87-P1 (anchoring listener only)
def _c88(src_key, new, svc, from_svc, tsrc_src, name):
    X=copy.deepcopy(T[src_key])
    for k,v in list(X.items()):
        if isinstance(v,str) and k not in ('dir','tsrc'): X[k]=v.replace(from_svc,svc)
    X['prod']=SV+svc+'/src/db.ts'; X['rdir']=SV+svc
    X['dir']='ks_1868_o88_%s_%s'%(new,name)
    X['test']=SV+svc+'/src/__tests__/'+T[src_key]['test'].split('/__tests__/')[1].replace(from_svc,svc)
    X['tsrc']='t88_%s.ts.txt'%new
    body=open(GEN+tsrc_src,encoding='utf-8').read().replace(from_svc,svc)
    open(GEN+X['tsrc'],'w',encoding='utf-8').write(body)
    T[new]=X
_c88('p2','p6','m365-integration','nft-certificate','t87_p9.ts.txt','m365_integration_db_pool_error_and_ready_hook_catches_guard_message')
_c88('p2','p7','staking','nft-certificate','t87_p9.ts.txt','staking_db_pool_error_and_ready_hook_catches_guard_message')
_c88('a1','p8','timestamping','anchoring','t87_p1.ts.txt','timestamping_db_pool_error_listener_guard_message')

# ---- O88-P9: api-gateway services/redis.ts: Redis 'error' listener (:92) + initRedis catch (:117-125) (vitest, 2 hunks)
PRD=SV+'api-gateway/src/services/redis.ts'
def _gate(ind):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"try {\n"+s+"  const m = (error as Error)?.message;\n"+s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
ERL=("    redisClient.on('error', (err) => {\n      logger.error('[Redis] Connection error', { error: err.message });\n      isConnected = false;\n",
     "    redisClient.on('error', (err) => {\n"+guard(6)+"      logger.error('[Redis] Connection error', { error: reason });\n      isConnected = false;\n")
ERC1=("  } catch (error) {\n    // Pen-test M4 fix: production REFUSES",
      "  } catch (error) {\n"+_gate(4)+"    // Pen-test M4 fix: production REFUSES")
ERC2=("    if (process.env.NODE_ENV === 'production') {\n      logger.error('[Redis] FATAL: connection failed in production \u2014 refusing to start', {\n        error: (error as Error).message,\n      });\n      throw new Error('REDIS_REQUIRED_IN_PRODUCTION: ' + (error as Error).message);\n    }\n    logger.warn('[Redis] Failed to connect, using in-memory fallback (dev/test only)', { error: (error as Error).message });\n",
     "    if (process.env.NODE_ENV === 'production') {\n      logger.error('[Redis] FATAL: connection failed in production \u2014 refusing to start', {\n        error: reason,\n      });\n      throw new Error('REDIS_REQUIRED_IN_PRODUCTION: ' + reason);\n    }\n    logger.warn('[Redis] Failed to connect, using in-memory fallback (dev/test only)', { error: reason });\n")
WHYR=("Two places in this module read the thrown value's message unguarded. (1) The Redis client `'error'` listener passes `err.message` into the logger's meta object and only THEN sets `isConnected = false`. (2) The catch of `initRedis` reads `(error as Error).message` three times: in the production FATAL log, in the message of the `REDIS_REQUIRED_IN_PRODUCTION` error it throws, and in the dev/test fallback warning. A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the listener (an uncaught exception from an EventEmitter listener, and the connected flag is never cleared, so `isRedisAvailable()` keeps answering true while Redis is down and the rate-limit and brute-force stores keep calling a dead client) and INSIDE the catch (`initRedis` rejects with a TypeError instead of answering `false` and falling back in dev/test, or instead of refusing with the named `REDIS_REQUIRED_IN_PRODUCTION` error in production); an Error whose `message` is readable but not a string (a Symbol) is passed to the logger or concatenated uncoerced. The fix is the house guard: read the message once inside a `try` (`?.` as the merged guards do), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then use `reason` in all four places. In the listener the guard sits BEFORE the log call, so `isConnected = false` runs. In the catch ONE guard is placed as the first statement of the catch (above the `Pen-test M4` comment) and serves the three reads. The production branch still THROWS (fail closed is kept: only the text after the colon changes for an unreadable value).")
T['p9']=dict(BASE, dir='ks_1868_o88_p9_api_gateway_redis_listener_and_connect_catch_guard_message', rdir=SV+'api-gateway', prod=PRD, edits=[ERL,ERC1,ERC2], nh=3,
  lines='92 (the Redis `error` listener in `initRedis`) and 117-125 (the catch of `initRedis`: production FATAL log, the thrown production error, the dev/test fallback warning)',
  test=SV+'api-gateway/src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts', tsrc='t88_p9.ts.txt',
  fn='the Redis error listener and the connect catch of `src/services/redis.ts`',
  short='the unguarded thrown-value reads in the Redis error listener and the connect catch of `initRedis`',
  premise="`%s` line 92 (`{ error: err.message }` in the Redis `error` listener, ahead of `isConnected = false`) and lines 118-125 (`(error as Error).message` three times in the `initRedis` catch) read the thrown value's message with no guard around the read" % PRD,
  whatwrong=WHYR,
  callers="CALLERS: `initRedis` is called once at boot by `src/index.ts` (line 1235, `redisConnected`); `isRedisAvailable()` gates every Redis-or-in-memory choice of this module (brute force, rate limit, workflow, privacy, signatures), `routes/verification.ts` and `services/health.ts`. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the listener logs at error level and clears the connected flag (the stores then use the in-memory fallback); the catch answers `false` with `fallbackMode = true` in dev/test, and in production logs FATAL and throws `REDIS_REQUIRED_IN_PRODUCTION: <message>` (boot refuses). Today (hostile value): the listener throws before clearing the flag; the catch throws a TypeError from inside itself. After: exactly the ordinary-Error row in both. Persisted state: none (the stores are Redis keys or in-memory maps; the change only decides which is used, as for an ordinary error). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown/emitted value only: (a) the listener logs, clears the connected flag (the gateway falls back to its in-memory stores exactly as for an ordinary connection error) and no longer raises an uncaught exception; (b) `initRedis` in dev/test answers `false` instead of rejecting; in production it still rejects (fail closed kept), now with `REDIS_REQUIRED_IN_PRODUCTION: unreadable thrown value` (or the Symbol text, or `undefined` for a thrown null) instead of a TypeError; every string message, every non-Error value other than null/undefined, and every ordinary Error behaves exactly as before. A thrown `null`/`undefined` previously threw a TypeError inside the catch; it now reads as an undefined message, as the merged guards do.",
  ncells='10 cells: C1 to C3 controls, R1 to R6 red (9 listed; see the list)',
  red1="At the tip the listener throws (or leaves the connected flag true) or the catch throws a TypeError / logs a non-text value, so the assertion fails",
  dbnote="The `ioredis` module is a plain stand-in class (its `on` hands over the listeners, `connect` rejects with the thrown value when asked, `ping` answers); the service logger `../utils/logger` is a plain recording object; each cell loads a fresh copy of the real `redis` module and sets NODE_ENV for the cell; no Redis, no network.",
  greens="'control ks1868 C1' (an ordinary Error from connect, dev/test), 'C2' (an ordinary Error from connect, production) and 'C3' (an ordinary Error at the listener), all already true at the tip (3 cells)",
  redcells="`R1` to `R3` (connect rejects with a revoked Proxy in dev/test, a revoked Proxy in production, an Error whose message is a Symbol in dev/test) and `R4` to `R6` (the listener receives a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (6 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,7)))
T['p9']['ncells']='9 cells: C1 to C3 controls, R1 to R6 red'
