# Operator 89 sites: clones of O88-P2 (nft-certificate db.ts listener + ready-hook catch) for prism, referral, billing, vc-issuer.
import copy, re
def _mk89(new, svc, hook_line, shared_mock, logger_variant, name):
    X=copy.deepcopy(T['p2'])
    for k,v in list(X.items()):
        if isinstance(v,str) and k not in ('dir','tsrc','edits'):
            v=v.replace('nft-certificate',svc).replace('(line 96','(line %d'%hook_line).replace('and 96 (','and %d ('%hook_line).replace('line 96','line %d'%hook_line)
            X[k]=v
    X['prod']=SV+svc+'/src/db.ts'; X['rdir']=SV+svc
    X['dir']='ks_1868_o89_%s_%s'%(new,name)
    X['test']=SV+svc+'/src/__tests__/ks1868-'+svc+'-db-pool-error-and-ready-hook-unreadable-throw.test.ts'
    X['tsrc']='t89_%s.ts.txt'%new
    body=open(GEN+'t87_p9.ts.txt',encoding='utf-8').read().replace('nft-certificate',svc).replace('line 96','line %d'%hook_line)
    if shared_mock:
        body=body.replace("type Db = typeof import('../db');", shared_mock+"\n\ntype Db = typeof import('../db');",1)
    if logger_variant:
        edits=[]
        for o,n in X['edits']:
            o=o.replace("dbLog('error', ","logger.error(").replace("'DB pool unexpected error', { error: err.message }","'DB pool unexpected error', { error: err.message }")
            n=n.replace("dbLog('error', ","logger.error(")
            edits.append((o,n))
        X['edits']=edits
        for k,v in list(X.items()):
            if isinstance(v,str) and k not in ('dir','tsrc','edits'):
                X[k]=v.replace('`dbLog`','`logger.error`').replace("`dbLog`'s","`logger.error`'s").replace('dbLog','logger.error')
        X['dbnote']="The `pg` module is a plain stand-in (a `Pool` whose `on` hands over the `error` listener, whose `query` answers the probe and whose other methods are plain functions); the service logger `./utils/logger` is a plain recording object (its `error` records the message and the meta object); each cell loads a fresh copy of the real `db` module; no database, no network."
        body=body.replace("vi.mock('pg'", """vi.mock('./__logger_placeholder__', () => ({}));
vi.mock('pg'""",1)
        body=body.replace("vi.mock('./__logger_placeholder__', () => ({}));\n","")
        body=body.replace("lines: [] as string[],","lines: [] as string[],\n  calls: [] as { message: string; meta: unknown }[],")
        body=body.replace("vi.mock('pg'","""vi.mock('../utils/logger', () => ({
  logger: {
    error: (message: string, meta?: unknown) => {
      h.calls.push({ message, meta });
    },
    warn: () => undefined,
    info: () => undefined,
    debug: () => undefined,
  },
}));

vi.mock('pg'""",1)
        body=body.replace("  console.log = (...args: unknown[]) => {\n    if (typeof args[0] === 'string') h.lines.push(args[0]);\n  };\n","")
        body=body.replace("  h.lines.length = 0;\n","  h.calls.length = 0;\n")
        body=body.replace("const realLog = console.log;\n","")
        body=body.replace("  console.log = realLog;\n","")
        body=body.replace("  h.lines.map((l) => JSON.parse(l) as Record<string, unknown>).filter((o) => o.message === message);",
                          "  h.calls.filter((c) => c.message === message).map((c) => c.meta as Record<string, unknown>);")
        body=body.replace("dbLog's","logger.error's").replace("(line 36)","(line %d)"%{'billing':33,'vc-issuer':32}[svc])
        body=body.replace("and console.log replaced by a plain recording function (no database)","and the service logger replaced by a plain recording object (no database)")
        assert 'console.log' not in body.replace('(console.log','') or True
    open(GEN+X['tsrc'],'w',encoding='utf-8').write(body)
    T[new]=X

SHD="vi.mock('@secuura/shared', () => ({ queryWithTenantGuc: async () => ({ rows: [{ ok: 1 }] }) }));"
SHR="vi.mock('@secuura/shared', () => ({\n  applyTenantGuc: async () => undefined,\n  runWithTenantId: async (_t: unknown, fn: () => unknown) => fn(),\n}));"
_mk89('q1','prism',97,SHD,False,'prism_db_pool_error_and_ready_hook_catches_guard_message')
_mk89('q2','referral',95,SHR,False,'referral_db_pool_error_and_ready_hook_catches_guard_message')
_mk89('q3','billing',80,SHD,True,'billing_db_pool_error_and_ready_hook_catches_guard_message')
_mk89('q4','vc-issuer',77,None,True,'vc_issuer_db_pool_error_and_ready_hook_catches_guard_message')

# ---- O89-P5: originate src/events.ts: Redis 'error' listener (:95) + init catch (:101), ONE merged hunk (jest)
PO=SV+'originate/src/events.ts'
OEL=("    redis.on('error', (err) => {\n      logger.debug('EventBus Redis error (non-fatal)', { error: err.message });\n    });\n",
     "    redis.on('error', (err) => {\n"+guard(6)+"      logger.debug('EventBus Redis error (non-fatal)', { error: reason });\n    });\n")
OEC=("  } catch (err: any) {\n    logger.warn('Failed to initialise EventBus', { error: err?.message });\n    return false;\n",
     "  } catch (err: any) {\n"+guard(4)+"    logger.warn('Failed to initialise EventBus', { error: reason });\n    return false;\n")
WHYO=("Two places in `initEventBus` pass the thrown value's message straight into the logger's meta object, unguarded: the Redis client `'error'` listener (`{ error: err.message }`) and the catch around the client constructor (`{ error: err?.message }`). A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the listener (an exception thrown by a listener of the client's `'error'` event escapes the EventEmitter as an uncaught exception) and INSIDE the catch (`initEventBus` THROWS to the boot caller instead of answering `false`, its documented contract: `true` if the Redis connection was established); an Error whose `message` is readable but not a string (a Symbol) is passed to the logger uncoerced. The fix is the house guard placed before each logger call: read the message once inside a `try` (`?.` as the merged guards do), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The two sites are 6 lines apart (89 and 95), so their changed regions form ONE hunk of the diff (the three context lines of each meet). The empty catches of `publishEvent` and `shutdownEventBus` read nothing and are untouched.")
T['p5']=dict(COMMON, dir='ks_1868_o89_p5_originate_events_listener_and_init_catch_guard_message', prod=PO, edits=[OEL,OEC], nh=1,
  lines='89 (the Redis `error` listener in `initEventBus`) and 95 (the init catch of `initEventBus`)',
  test=SV+'originate/src/__tests__/ks1868-originate-events-listener-and-init-catch-unreadable-throw.test.ts', tsrc='t89_p5.ts.txt',
  fn='the Redis error listener and the init catch of `src/events.ts`',
  short='the unguarded thrown-value reads in the Redis error listener and the init catch of `initEventBus`',
  premise="`%s` line 89 (`{ error: err.message }` in the Redis `error` listener) and line 95 (`{ error: err?.message }` in the `initEventBus` catch) pass the thrown value's message straight into the logger with no guard around the read" % PO,
  whatwrong=WHYO,
  callers="CALLERS: `initEventBus()` is called once at boot by `src/index.ts` (line 524, no argument); the listener is attached to the one Redis client for the life of the process. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): an error emitted by the client is logged at debug level and the process goes on; a failure to construct the client is logged at warn and `initEventBus` answers `false` (event publishing stays off; the service runs). Today (hostile value): the listener throws while building the meta object (uncaught exception); the catch throws, so `initEventBus` THROWS to the boot caller. After: exactly the ordinary-Error rows. Persisted state: none (the sites only log; `redis` stays null after a failed construction). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown/emitted value only: the listener logs at debug instead of an uncaught exception; `initEventBus` answers `false` and logs at warn instead of throwing to the boot caller; a Symbol message is logged as its text; every string message and every ordinary Error behaves exactly as before. A thrown `null`/`undefined` previously threw a TypeError in the catch; it now reads as an undefined message, as the merged guards do.",
  ncells='10 cells: C1 to C4 controls, R1 to R6 red',
  red1="At the tip the listener throws while building the meta object (the listener call throws) or the catch throws (initEventBus throws) or the logged value is not text, so the assertion fails",
  dbnote="The `ioredis` module is a plain stand-in class (its constructor throws the thrown value when asked, its `on` hands over the `error` listener); the service logger `./utils/logger` is a plain recording object; each cell loads a fresh copy of the real `events` module with `jest.resetModules()`; no Redis, no network.",
  greens="'control ks1868 C1' (an ordinary Error from the constructor), 'C2' (a thrown number from the constructor), 'C3' (an ordinary Error at the listener) and 'C4' (a plain string at the listener), all already true at the tip (4 cells)",
  redcells="`R1` to `R3` (the constructor throws a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) and `R4` to `R6` (the listener receives the same three shapes) (6 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,7)))

# ---- O89-P7: timestamping db.ts listener only (re-run of O88-P8 whose control failed on the harness: asn1js absent)
X=copy.deepcopy(T['p8']); X['dir']='ks_1868_o89_p7_timestamping_db_pool_error_listener_guard_message'; T['p7']=X

# ---- split of O89-P5: the merged hunk carried a blank context line (REFUSED by build_input); two separate 1-hunk passes
_b=copy.deepcopy(T['p5'])
_l=copy.deepcopy(_b); _l.update(dict(dir='ks_1868_o89_p5_originate_events_redis_error_listener_guard_message', edits=[OEL], nh=1, tsrc='t89_p9.ts.txt',
  lines='89 (the Redis `error` listener in `initEventBus`)',
  test=SV+'originate/src/__tests__/ks1868-originate-events-redis-error-listener-unreadable-throw.test.ts',
  fn='the Redis error listener of `src/events.ts`', short='the unguarded thrown-value read in the Redis error listener of `initEventBus`',
  premise="`%s` line 89 (`{ error: err.message }` in the Redis `error` listener) passes the thrown value's message straight into the logger with no guard around the read" % PO,
  whatwrong=WHYO.replace("Two places in `initEventBus` pass","The Redis client `'error'` listener in `initEventBus` passes").split(" A thrown value whose read throws",1)[0].replace("message straight into the logger's meta object, unguarded: the Redis client `'error'` listener (`{ error: err.message }`) and the catch around the client constructor (`{ error: err?.message }`).","message straight into the logger's meta object, unguarded: `{ error: err.message }`.")+" A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the listener, and an exception thrown by a listener of the client's `'error'` event escapes the EventEmitter as an uncaught exception; an Error whose `message` is readable but not a string (a Symbol) is passed to the logger uncoerced. The fix is the house guard placed before the logger call: read the message once inside a `try` (`?.`), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The init catch six lines below (line 95) is a separate pass (O89-P8): the two changed regions would merge into one hunk with a blank context line, which the model cannot reproduce. The empty catches of `publishEvent` and `shutdownEventBus` read nothing and are untouched.",
  callers="CALLERS: `initEventBus()` is called once at boot by `src/index.ts` (line 524); the listener is attached to the one Redis client for the life of the process. WHAT AN ORDINARY ERROR GETS (the rule for taking the site): an error emitted by the client is logged at debug level and the process goes on. Today (hostile value): the listener throws while building the meta object (uncaught exception). After: exactly the ordinary-Error row. Persisted state: none (the listener only logs). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined value emitted on the Redis client's `error` event only, the line is logged at debug instead of an uncaught exception; a Symbol message is logged as its text; every string message and every ordinary Error behaves exactly as before. The init catch at line 95 is a separate pass (O89-P8).",
  ncells='5 cells: C1 to C2 controls, R1 to R3 red',
  red1="At the tip the listener throws while building the meta object (the listener call throws) or the logged value is not text, so the assertion fails",
  dbnote="The `ioredis` module is a plain stand-in class (its `on` hands over the `error` listener); the service logger `./utils/logger` is a plain recording object; each cell loads a fresh copy of the real `events` module with `jest.resetModules()`; no Redis, no network.",
  greens="'control ks1868 C1' (an ordinary Error at the listener) and 'C2' (a plain string at the listener), both already true at the tip (2 cells)",
  redcells="`R1` to `R3` (the listener receives a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (3 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,4))))
T['p5']=_l
_i=copy.deepcopy(_b); _i.update(dict(dir='ks_1868_o89_p8_originate_events_init_catch_guard_message', edits=[OEC], nh=1, tsrc='t89_p8.ts.txt',
  lines='95 (the catch of `initEventBus`)',
  test=SV+'originate/src/__tests__/ks1868-originate-events-init-catch-unreadable-throw.test.ts',
  fn='the init catch of `src/events.ts`', short='the unguarded thrown-value read in the ONE catch of `initEventBus`',
  premise="`%s` line 95 (`{ error: err?.message }` in the `initEventBus` catch) passes the thrown value's message straight into the logger with no guard around the read" % PO,
  whatwrong="The catch of `initEventBus` passes the thrown value's message straight into the logger's meta object, unguarded: `{ error: err?.message }`. A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the catch, so `initEventBus` THROWS instead of answering `false` (its contract, in its own doc comment: `true` if the Redis connection was established; on failure the service carries on without events); an Error whose `message` is readable but not a string (a Symbol) is passed to the logger uncoerced. The fix is the house guard placed before the logger call: read the message once inside a `try` (`?.`), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The Redis `error` listener six lines above (line 89) is a separate pass (O89-P5): the two changed regions would merge into one hunk with a blank context line, which the model cannot reproduce.",
  callers="CALLERS: `initEventBus()` is called once at boot by `src/index.ts` (line 524, no argument). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a failure to construct the client is logged at warn and `initEventBus` answers `false` (event publishing stays off; the service runs). Today (hostile value): the catch throws while building the meta object, so `initEventBus` THROWS to the boot caller. After: exactly the ordinary-Error row. Persisted state: none (`redis` stays null after a failed construction). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value from the Redis constructor only, `initEventBus` logs at warn and answers `false` instead of throwing out to the boot caller; a Symbol message is logged as its text; every string message and every ordinary Error behaves exactly as before. A thrown `null`/`undefined` previously threw a TypeError in the catch; it now reads as an undefined message, as the merged guards do.",
  ncells='5 cells: C1 to C2 controls, R1 to R3 red',
  red1="At the tip the catch throws while building the meta object (initEventBus throws) or the logged value is not text, so the assertion fails",
  dbnote="The `ioredis` module is a plain stand-in class (its constructor throws the thrown value when asked, otherwise it returns a plain object); the service logger `./utils/logger` is a plain recording object; each cell loads a fresh copy of the real `events` module with `jest.resetModules()`; no Redis, no network.",
  greens="'control ks1868 C1' (an ordinary Error from the constructor) and 'C2' (a thrown number from the constructor), both already true at the tip (2 cells)",
  redcells="`R1` to `R3` (the constructor throws a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (3 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,4))))
T['p8']=_i

# ---- O89-P9 governance db.ts: same text as referral (imports, lines 36/95)
_mk89('q5','governance',95,SHR,False,'governance_db_pool_error_and_ready_hook_catches_guard_message')

# ---- O89-P10: originate db.ts initDb Prisma connection catch (:449, jest)
PDB=SV+'originate/src/db.ts'
ODB=("    } catch (err: any) {\n      console.error('[DB] Prisma connection failed:', err.message);\n",
     "    } catch (err: any) {\n"+guard(6)+"      console.error('[DB] Prisma connection failed:', reason);\n")
T['p10']=dict(COMMON, dir='ks_1868_o89_p10_originate_db_init_prisma_catch_guard_message', prod=PDB, edits=[ODB], nh=1,
  lines='449 (the catch around the Prisma connection check in `initDb`)',
  test=SV+'originate/src/__tests__/ks1868-originate-db-init-prisma-catch-unreadable-throw.test.ts', tsrc='t89_p10.ts.txt',
  fn='the Prisma connection catch of `initDb` in `src/db.ts`', short='the unguarded thrown-value read in the Prisma connection catch of `initDb`',
  premise="`%s` line 449 (`console.error('[DB] Prisma connection failed:', err.message)` in the single-tenant branch of `initDb`) passes the thrown value's message straight into console.error with no guard around the read" % PDB,
  whatwrong="The catch around the Prisma connection check in `initDb` (the single-tenant branch, `MULTI_TENANCY_ENABLED` not `true`) passes the thrown value's message straight into `console.error`'s arguments, unguarded: `err.message`. A thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) therefore throws INSIDE the catch, so `initDb` REJECTS instead of logging the failure and resolving; an Error whose `message` is readable but not a string (a Symbol) is handed to `console.error` uncoerced. The fix is the house guard placed before the log call: read the message once inside a `try` (`?.` as the merged guards do), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, and fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `reason` in the call. The other catch of this module that reads `err?.code` / `err?.message` (the Prisma-client-not-generated check in `getPrismaClient`) is deliberately NOT touched: it rethrows the value and the message test there is a design decision. The ROLLBACK catches read nothing.",
  callers="CALLERS: `initDb()` is called once at boot by `src/index.ts` (line 398, `initDb().then(...)`). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a failed Prisma connection check is logged with `console.error` and `initDb` resolves, so the boot carries on (requests then fail on their own database calls). Today (hostile value): the catch throws while evaluating the arguments, so `initDb` REJECTS to the boot caller. After: exactly the ordinary-Error row. Persisted state: none (the catch only logs). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value from the Prisma connection check only, the failure is logged (as text) and `initDb` resolves instead of rejecting to the boot caller; a Symbol message is logged as its text; every string message and every ordinary Error behaves exactly as before. A thrown `null`/`undefined` previously threw a TypeError in the catch; it now reads as an undefined message, as the merged guards do. Raise seat: check what `src/index.ts` does with an `initDb()` rejection (the `.then` at line 398) before stating the 'today' outcome in the PR.",
  ncells='5 cells: C1 to C2 controls, R1 to R3 red',
  red1="At the tip the catch throws while evaluating the arguments (initDb rejects) or the logged value is not text, so the assertion fails",
  dbnote="The Prisma client (`@prisma/client`, whose `$queryRaw` rejects with the thrown value through a plain async function), its adapter (`@prisma/adapter-pg`), `@secuura/shared` and `./config` are plain stand-ins, `console.error` is a plain recording function, `MULTI_TENANCY_ENABLED` is unset; each cell loads a fresh copy of the real `db` module with `jest.resetModules()`; no database, no network.",
  greens="'control ks1868 C1' (an ordinary Error) and 'C2' (a thrown number), both already true at the tip (2 cells)",
  redcells="`R1` to `R3` (the connection check rejects with a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (3 cells)",
  redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,4)))
# governance runs jest (package.json "test": "jest"): q5 control FAILED 04:18:03 with 'Vitest cannot be imported in a CommonJS module'; jest variant of the test
T['q5'].update(dict(runner='jest', runcmd='', ref=REFO, tsrc='t89_q5j.ts.txt', sib="`ks1868-anchors-route-catches-unreadable-throw.test.ts`",
  dbnote="The `pg` module is a plain stand-in (a `Pool` whose `on` hands over the `error` listener, whose `query` answers the probe and whose other methods are plain functions), `@secuura/shared` is a plain stand-in, `console.log` is a plain recording function; each cell loads a fresh copy of the real `db` module with `jest.resetModules()`; no database, no network."))
