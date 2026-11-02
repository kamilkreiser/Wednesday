# Operator 90 sites. T['p7'] = O89-P7 timestamping listener (vitest, dbLog); clone for security. k2 = demo-service state.ts (2 hunks).
import copy
X=copy.deepcopy(T['p7'])
for k,v in list(X.items()):
    if isinstance(v,str) and k not in ('dir','tsrc'): X[k]=v.replace('timestamping','security')
X['reuse']=X['reuse'].replace("(operator 81 `security/src/db.ts`, ","(operator 81, the ready-hook and probeDb catches of THIS file; ")
X['dir']='ks_1868_o90_p1_security_db_pool_error_listener_guard_message'
X['prod']=SV+'security/src/db.ts'; X['rdir']=SV+'security'
X['test']=SV+'security/src/__tests__/ks1868-security-db-pool-error-listener-unreadable-throw.test.ts'
X['tsrc']='t90_k1.ts.txt'
body=open(GEN+'t88_p8.ts.txt',encoding='utf-8').read().replace('timestamping','security')
body=body.replace("type Db = typeof import('../db');","vi.mock('@secuura/shared', () => ({ queryWithTenantGuc: async () => ({ rows: [{ ok: 1 }] }) }));\n\ntype Db = typeof import('../db');",1)
body=body.replace("operator 87 screen","operator 90 screen")
open(GEN+X['tsrc'],'w',encoding='utf-8').write(body)
X['callers']=X['callers'].replace("Persisted state: identical in both cases (the catch-free listener writes nothing).","Persisted state: identical in both cases (the catch-free listener writes nothing). The security service's own ready-hook and probe catches are already guarded and untouched.")
T['k1']=X

PS=SV+'demo-service/src/routes/state.ts'
def _g(ind):
    s=' '*ind
    return (s+"let message: string;\n"+s+"try {\n"+s+"  message = err instanceof Error ? err.message : 'Unknown error';\n"+s+"} catch {\n"+s+"  message = 'unreadable thrown value';\n"+s+"}\n")
SE1=("    redis.on('error', (err) => {\n      logger.warn('Redis unavailable, using in-memory state', { error: err.message });\n",
     "    redis.on('error', (err) => {\n"+_g(6)+"      logger.warn('Redis unavailable, using in-memory state', { error: message });\n")
SE2=("  } catch (err) {\n    const message = err instanceof Error ? err.message : 'Unknown error';\n    logger.error('Failed to toggle presenter mode', { error: message });\n",
     "  } catch (err) {\n"+_g(4)+"    logger.error('Failed to toggle presenter mode', { error: message });\n")
Y=copy.deepcopy(T['p7'])
Y.update(dict(
 dir='ks_1868_o90_p2_demo_service_state_redis_listener_and_presenter_mode_catch_guard_message',
 prod=PS, rdir=SV+'demo-service', edits=[SE1,SE2], nh=2,
 ref=SV+'demo-service/src/__tests__/ks1868-state-get-unreadable-throw.test.ts',
 sib="`ks1868-state-get-unreadable-throw.test.ts` (the merged GET /state sibling of this very file)",
 reuse="This follows the guard that the merged GET /state catch of THIS file (lines 74-80) already uses: `message = err instanceof Error ? err.message : 'Unknown error'` inside a `try`, the constant `'unreadable thrown value'` when the read throws; no helper exists and none is added.",
 lines='44 (the Redis `error` listener in `getRedis`) and 112-113 (the catch of `POST /presenter-mode`)',
 test=SV+'demo-service/src/__tests__/ks1868-state-redis-listener-and-presenter-mode-unreadable-throw.test.ts', tsrc='t90_k2.ts.txt',
 fn='the Redis error listener and the POST /presenter-mode catch of `src/routes/state.ts`',
 short='the unguarded thrown-value reads in the Redis error listener of `getRedis` and the catch of `POST /presenter-mode`',
 premise="`%s` line 44 (`{ error: err.message }` in the Redis `error` listener, before `redis = null`) and line 113 (`err instanceof Error ? err.message : ...` in the `POST /presenter-mode` catch, outside any guard) read the thrown value with no guard around the read" % PS,
 whatwrong="Two places in this file read a thrown value unguarded. (1) The Redis client `'error'` listener passes `err.message` into `logger.warn` and only THEN sets `redis = null`: a value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the listener throw (an uncaught exception from the client's EventEmitter) and the dead client stays cached in `redis`. (2) The catch of `POST /presenter-mode` computes `err instanceof Error ? err.message : 'Unknown error'` outside any guard: `instanceof` on a revoked Proxy throws, and so does a throwing `message` getter, so the catch throws, the async handler rejects (Express 4 does not catch it) and the request never receives its 500 reply. The fix is the guard the GET /state catch of this same file already uses: the read inside a `try`, the constant `'unreadable thrown value'` when the read throws; then the existing logger call with `error: message`. The two hunks are ~70 lines apart. The GET /state catch is already guarded; the other handlers of the file are untouched.",
 callers="CALLERS: `getRedis()` is called by the GET /state and POST /presenter-mode handlers; the listener lives for the life of the client. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): an error emitted by the client is logged at warn level and the cached client is dropped (`redis = null`, the in-memory fallback is used); a failed presenter-mode write is logged at error level and the handler answers 500 `INTERNAL_ERROR`. Today (hostile value): the listener throws before `redis = null`; the catch throws and the request gets no reply. After: exactly the ordinary-Error rows. Persisted state: none (the in-memory flag is unchanged by a failed write, as for an ordinary Error). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable thrown/emitted value only: the listener logs at warn and drops the client instead of an uncaught exception; the presenter-mode handler answers 500 INTERNAL_ERROR instead of leaving the request without a reply; every ordinary Error behaves exactly as before. demo-service is the sales demo helper service (not a customer data path).",
 ncells='6 cells: C1 and C2 controls, R1 to R4 red',
 red1="At the tip the listener throws (the listener call throws) or the handler rejects (no 500 reply), so the assertion fails",
 dbnote="The `ioredis` module is a plain stand-in class (its `on` hands over the `error` listener, its `set` rejects with the value under test); the service logger `../utils/logger` is a recording stand-in; the real route handlers are invoked from the router stack with a plain response object; no Redis, no network.",
 greens="'control ks1868 C1' (an ordinary Error at the listener) and 'C2' (an ordinary Error from the presenter-mode write), both already true at the tip (2 cells)",
 redcells="`R1` and `R2` (the listener receives a revoked Proxy, an Error whose message getter throws) and `R3` and `R4` (the presenter-mode write rejects with the same two shapes) (4 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,5))))
T['k2']=Y

# ---- k3: originate routes/certifications.ts module-load initRepo().catch (:70), jest, 1 hunk
PC=SV+'originate/src/routes/certifications.ts'
CE=("initRepo().catch((err) => logger.error('Failed to init repo', { error: err instanceof Error ? err.message : String(err) }));\n",
    "initRepo().catch((err) => {\n  let reason: string;\n  try {\n    reason = err instanceof Error ? err.message : String(err);\n  } catch {\n    reason = 'unreadable thrown value';\n  }\n  logger.error('Failed to init repo', { error: reason });\n});\n")
Z=copy.deepcopy(T['p5'])
Z.update(dict(
 dir='ks_1868_o90_p3_originate_certifications_init_repo_catch_guard_message',
 prod=PC, edits=[CE], nh=1,
 reuse="This follows the guard that the SAME service already carries in `trackError` (merged KS-1868 pass: the read inside a `try`, the constant `'unreadable thrown value'` on throw), copied inline with today's read kept as it is (`err instanceof Error ? err.message : String(err)`); no helper is added.",
 sib="`ks1868-anchors-route-catches-unreadable-throw.test.ts` and `ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts` (the mock set of this router)",
 lines='70 (the module-load `initRepo().catch` arrow)',
 test=SV+'originate/src/__tests__/ks1868-certifications-init-repo-catch-unreadable-throw.test.ts', tsrc='t90_k3.ts.txt',
 fn='the module-load `initRepo().catch` of `src/routes/certifications.ts`',
 short='the unguarded thrown-value read in the `initRepo().catch` arrow at module load',
 premise="`%s` line 70 (`err instanceof Error ? err.message : String(err)` inside the `.catch` arrow of `initRepo()`) reads the rejection value with no guard around the read" % PC,
 whatwrong="`certifications.ts` starts the repository at module load: `initRepo().catch((err) => logger.error('Failed to init repo', { error: err instanceof Error ? err.message : String(err) }))`. The read of the rejection value is inside the arrow with no guard: a revoked Proxy (`instanceof` throws), an Error whose `message` getter throws, or an object with a null prototype (`String(...)` throws) makes the arrow throw before the logger runs, so the promise returned by `.catch` rejects with nobody listening: an unhandled rejection (originate's `process.on('unhandledRejection')` handler then runs its error-tracking and shutdown path). The fix is the house guard inline: the same read inside a `try`, the constant `'unreadable thrown value'` when it throws, then the same logger call with `error: reason`. Today's read for readable values is kept exactly (an Error gives its message, anything else `String(value)`). The other `.catch` of this file (provenance record, line ~710) is a separate site and untouched.",
 callers="CALLERS: none; the statement runs once when the module is first imported (by `src/app` / `src/index.ts` router mounting). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): a failed repository start is logged at error level ('Failed to init repo') and the service goes on. Today (hostile value): the arrow throws, an unhandled rejection reaches `process.on('unhandledRejection')` in index.ts (read it before stating what that does in the PR). After: exactly the ordinary-Error row. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable rejection value only: a log line instead of an unhandled rejection; every ordinary Error and every readable value behaves exactly as before.",
 ncells='5 cells: C1 and C2 controls, R1 to R3 red',
 red1="At the tip the arrow throws before it logs (nothing is logged and jest reports the unhandled rejection), so the assertion fails",
 dbnote="`../repositories/certificationRepo` is a plain stand-in whose `initRepo` rejects with the value under test through a plain function, and the other modules the router imports (`../db`, `../services/chargeEvents`, `../utils/notificationClient`, `../events`, `../repositories/documentRepo`, `../middleware/auth`, `../utils/logger`) are the same stand-ins as in the ks1844 sibling; each cell loads a fresh copy of the real router with `jest.resetModules()` and `require`; no database, no network.",
 greens="'control ks1868 C1' (an ordinary Error rejection) and 'C2' (a plain string rejection), both already true at the tip (2 cells)",
 redcells="`R1` to `R3` (the rejection is a revoked Proxy, an Error whose message getter throws, an object with a null prototype) (3 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,4))))
T['k3']=Z

# ---- k4/k5: referral milestoneService.ts (vitest): k4 = three read catches, k5 = two write catches
PM=SV+'referral/src/services/milestoneService.ts'
def _mg(ind, extra=''):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"try {\n"+s+"  const m = err?.message;\n"+s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
M1=("    } catch (err: any) {\n      logger.error('DB read user progress failed', { userId, error: err?.message });\n",
    "    } catch (err: any) {\n"+_mg(6)+"      logger.error('DB read user progress failed', { userId, error: reason });\n")
M2=("      // Table may not exist yet — fall back gracefully\n      logger.error('DB read pending rewards failed', { userId, error: err?.message });\n",
    "      // Table may not exist yet — fall back gracefully\n"+_mg(6)+"      logger.error('DB read pending rewards failed', { userId, error: reason });\n")
M3=("    } catch (err: any) {\n      logger.warn('Milestone table verification failed — table may need migration', { error: err?.message });\n",
    "    } catch (err: any) {\n"+_mg(6)+"      logger.warn('Milestone table verification failed — table may need migration', { error: reason });\n")
M4=("    } catch (err: any) { logger.error('DB save milestone failed', { error: err?.message }); }\n",
    "    } catch (err: any) {\n"+_mg(6)+"      logger.error('DB save milestone failed', { error: reason });\n    }\n")
M5=("    } catch (err: any) {\n      logger.error('DB save pending reward failed', { rewardId: reward.id, error: err?.message });\n",
    "    } catch (err: any) {\n"+_mg(6)+"      logger.error('DB save pending reward failed', { rewardId: reward.id, error: reason });\n")
MC=dict(reuse="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (`const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw, as in the held db.ts passes of the neighbouring referral service), inline; no helper exists in this file and none is added.",
 prod=PM, rdir=SV+'referral', sib="`ks1868-state-get-unreadable-throw.test.ts` style suites of other services (vitest, plain stand-ins)", ref='Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts')
K4=copy.deepcopy(T['p7']); K4.update(MC)
K4.update(dict(dir='ks_1868_o90_p4_referral_milestone_service_db_read_catches_guard_message', edits=[M1,M2,M3], nh=3,
 lines='124 (`dbGetUserProgress` catch), 159 (`dbGetPendingRewards` catch) and 238 (`verifyDbReady` catch)',
 test=SV+'referral/src/__tests__/ks1868-milestone-service-db-read-catches-unreadable-throw.test.ts', tsrc='t90_k4.ts.txt',
 fn='the three DB read catches of `src/services/milestoneService.ts`',
 short='the unguarded `err?.message` reads in the three DB read catches',
 premise="`%s` lines 124, 159 and 238 (`error: err?.message` in the catches of dbGetUserProgress, dbGetPendingRewards and verifyDbReady) pass the thrown value's message straight into the logger with no guard around the read" % PM,
 whatwrong="Three catches of `MilestoneService` pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW, so `getUserProgress` (via `dbGetUserProgress`), `getPendingRewards` (via `dbGetPendingRewards`) and `verifyDbReady` REJECT, where an ordinary Error gets a logged failure and the documented fallback (`null` -> a fresh default progress, `[]`, a resolved verification). The fix is the house guard placed before each logger call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The three hunks are ~34 and ~80 lines apart. The two WRITE catches of this file (lines 180 and 194) are a separate brief (O90-P5) and untouched here.",
 callers="CALLERS: `getUserProgress` is called by `checkAndAwardMilestones`, `getOngoingBonusPercentage` and the referral routes; `getPendingRewards` by the rewards routes; `verifyDbReady` once at boot. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the failure is logged and the method answers the fallback (fresh default progress, empty list, resolved call). Today (hostile value): the catch throws and the method rejects to its caller. After: exactly the ordinary-Error rows. Persisted state: none (read paths). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the read methods log text and answer the same fallback as for an ordinary Error instead of rejecting; a thrown null/undefined reads as an undefined message (as `?.` already did); every ordinary Error behaves exactly as before. The raise seat should read the callers (routes that await these methods) before stating what a rejection did in the PR.",
 ncells='9 cells: C1 to C3 controls, R1 to R6 red',
 red1="At the tip the catch throws while building the meta object (the method rejects) or the logged value is not text, so the assertion fails",
 dbnote="`../db` is a plain stand-in (`isDbAvailable` true, `query` rejecting with the value under test through a plain function); the service logger `../utils/logger` (`createLogger`) is a plain recording object; the real `milestoneService` singleton is called; no database, no network.",
 greens="'control ks1868 C1' (progress read), 'C2' (pending-rewards read) and 'C3' (table verification), each with an ordinary Error, already true at the tip (3 cells)",
 redcells="`R1` to `R6` (each of the three methods rejects/fails with a revoked Proxy and with an Error whose message getter throws) (6 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,7))))
T['k4']=K4
K5=copy.deepcopy(T['p7']); K5.update(MC)
K5.update(dict(dir='ks_1868_o90_p5_referral_milestone_service_db_write_catches_guard_message', edits=[M4,M5], nh=2,
 lines='180 (`dbSaveMilestoneProgress` catch) and 194 (`dbSavePendingReward` catch)',
 test=SV+'referral/src/__tests__/ks1868-milestone-service-db-write-catches-unreadable-throw.test.ts', tsrc='t90_k5.ts.txt',
 fn='the two DB write catches of `src/services/milestoneService.ts`',
 short='the unguarded `err?.message` reads in the two DB write catches',
 premise="`%s` lines 180 and 194 (`error: err?.message` in the catches of dbSaveMilestoneProgress and dbSavePendingReward) pass the thrown value's message straight into the logger with no guard around the read" % PM,
 whatwrong="Two catches of `MilestoneService` pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW, so `checkAndAwardMilestones` REJECTS after it has computed the awards, where an ordinary Error gets a logged failure and the awarded milestones and rewards are still answered (the failed save is swallowed by design). The fix is the house guard placed before each logger call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The one-line catch at line 180 becomes a block (the logger call and its message text unchanged). The three READ catches of this file (lines 124, 159, 238) are a separate brief (O90-P4) and untouched here.",
 callers="CALLERS: `checkAndAwardMilestones` (the only caller of both helpers) is called by the referral qualification path. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the failed save is logged at error level and `checkAndAwardMilestones` still answers `{ newMilestones, rewards }` (the DB write is best-effort here). Today (hostile value): the catch throws and `checkAndAwardMilestones` rejects to its caller. After: exactly the ordinary-Error row. Persisted state: identical in both cases (the failed INSERT wrote nothing; for the reward catch the later progress save still runs after it, as for an ordinary Error). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the failed save is logged as text and the awards are answered instead of the call rejecting; every ordinary Error behaves exactly as before. **Recommend TIER 1: referral reward persistence (money-adjacent); the raise seat must read what the qualification caller does on a rejection versus on the answered awards before stating 'today' in the PR.**",
 ncells='6 cells: C1 and C2 controls, R1 to R4 red',
 red1="At the tip the catch throws while building the meta object (checkAndAwardMilestones rejects) or the logged value is not text, so the assertion fails",
 dbnote="`../db` is a plain stand-in (`isDbAvailable` true; `query` answers an empty row set, and rejects with the value under test for exactly one of the two INSERT statements per cell, through a plain function); the service logger `../utils/logger` (`createLogger`) is a plain recording object; the real `milestoneService` singleton is called with a first-referral count of 1; no database, no network.",
 greens="'control ks1868 C1' (reward save) and 'C2' (progress save), each with an ordinary Error, already true at the tip (2 cells)",
 redcells="`R1` and `R2` (the reward save rejects with a revoked Proxy and with an Error whose message getter throws) and `R3` and `R4` (the same two shapes at the progress save) (4 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,5))))
T['k5']=K5

# ---- k6/k7: staking routes stake.ts / rewards.ts verifyDbReady catch (vitest, 1 hunk each)
def _sg(ind):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"try {\n"+s+"  const m = err?.message;\n"+s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
def _staking(new, fname, tsrc, line, what, logmsg, tfile):
    P=SV+'staking/src/routes/'+fname
    E=("  } catch (err: any) {\n    logger.error('%s', { error: err?.message });\n"%logmsg,
       "  } catch (err: any) {\n"+_sg(4)+"    logger.error('%s', { error: reason });\n"%logmsg)
    Q=copy.deepcopy(T['p7']); Q.update(MC)
    Q.update(dict(prod=P, rdir=SV+'staking', edits=[E], nh=1,
     dir='ks_1868_o90_%s_staking_%s_verify_db_ready_catch_guard_message'%(new.replace('k','p'), fname.split('.')[0]),
     lines='%d (the catch of `verifyDbReady`)'%line,
     test=SV+'staking/src/__tests__/'+tfile, tsrc=tsrc,
     fn='the `verifyDbReady` catch of `src/routes/%s`'%fname, short='the unguarded `err?.message` read in the `verifyDbReady` catch',
     reuse="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (`const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw), inline; no helper exists in this file and none is added.",
     sib="`ks1845-stake-all-requires-a-platform-admin.test.ts` (mounts the same module with ../db and ../utils/logger mocked)",
     ref=SV+'staking/src/__tests__/ks1845-stake-all-requires-a-platform-admin.test.ts',
     premise="`%s` line %d (`error: err?.message` in the `verifyDbReady` catch) passes the thrown value's message straight into the logger with no guard around the read" % (P, line),
     whatwrong="The catch of `verifyDbReady` (%s) passes `err?.message` straight into the logger's meta object, unguarded. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW, so `verifyDbReady` REJECTS where an ordinary Error gets a logged failure and a resolved call; an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced. The fix is the house guard placed before the logger call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The other catches of the file forward to `next(error)` and are untouched." % what,
     callers="CALLERS: `verifyDbReady` is called once at boot by `src/index.ts` (the raise seat must read the call site before stating 'today' in the PR). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at error level and the call resolves (boot goes on without the pool statistics). Today (hostile value): the catch throws and `verifyDbReady` rejects to the boot caller. After: exactly the ordinary-Error row. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the failure is logged as text and the call resolves instead of rejecting; every ordinary Error behaves exactly as before.",
     ncells='5 cells: C1 and C2 controls, R1 to R3 red',
     red1="At the tip the catch throws while building the meta object (verifyDbReady rejects) or the logged value is not text, so the assertion fails",
     dbnote="`../db` is a plain stand-in (`isDbAvailable` true, `query` rejecting with the value under test through a plain function); `../utils/logger` is a plain recording object; the real `verifyDbReady` is called; no database, no network.",
     greens="'control ks1868 C1' (an ordinary Error) and 'C2' (a plain string), both already true at the tip (2 cells)",
     redcells="`R1` to `R3` (a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (3 cells)",
     redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,4))))
    T[new]=Q
_staking('k6','stake.ts','t90_k6.ts.txt',148,'`src/routes/stake.ts` line 148','[Staking] Failed to verify DB readiness for stake positions','ks1868-staking-stake-verify-db-ready-catch-unreadable-throw.test.ts')
_staking('k7','rewards.ts','t90_k7.ts.txt',145,'`src/routes/rewards.ts` line 145','[Staking] Failed to verify DB readiness for rewards','ks1868-staking-rewards-verify-db-ready-catch-unreadable-throw.test.ts')

# ---- k8/k9: vc-issuer credentialRepo.ts (vitest): k8 = getById/getRecordById/getByHash read catches; k9 = store/list/revoke catches
PV=SV+'vc-issuer/src/repositories/credentialRepo.ts'
def _vg(ind):
    s=' '*ind
    return (s+"let reason: string | null | undefined;\n"+s+"try {\n"+s+"  const m = err?.message;\n"+s+"  reason = m === undefined || m === null ? m : String(m);\n"+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
V1=("    } catch (err: any) {\n      logger.warn('DB read failed — falling back to memory', { error: err?.message });\n    }\n  }\n\n  // Fall back to memory\n",
    "    } catch (err: any) {\n"+_vg(6)+"      logger.warn('DB read failed — falling back to memory', { error: reason });\n    }\n  }\n\n  // Fall back to memory\n")
V2=("    } catch (err: any) {\n      logger.warn('DB read failed — falling back to memory', { error: err?.message });\n    }\n  }\n\n  const exact = memoryStore.get(id);\n  if (exact) return { credential: exact",
    "    } catch (err: any) {\n"+_vg(6)+"      logger.warn('DB read failed — falling back to memory', { error: reason });\n    }\n  }\n\n  const exact = memoryStore.get(id);\n  if (exact) return { credential: exact")
V3=("    } catch (err: any) {\n      logger.warn('DB hash lookup failed — falling back to memory', { error: err?.message });\n    }\n  }\n\n  for (const value of memoryStore.values()) {",
    "    } catch (err: any) {\n"+_vg(6)+"      logger.warn('DB hash lookup failed — falling back to memory', { error: reason });\n    }\n  }\n\n  for (const value of memoryStore.values()) {")
V4=("  } catch (err: any) {\n    logger.warn('DB write failed for credential — kept in memory', {\n      credentialId: credential.id,\n      error: err?.message,\n    });\n",
    "  } catch (err: any) {\n"+_vg(4)+"    logger.warn('DB write failed for credential — kept in memory', {\n      credentialId: credential.id,\n      error: reason,\n    });\n")
V5=("    } catch (err: any) {\n      logger.warn('DB list failed — falling back to memory', { error: err?.message });\n",
    "    } catch (err: any) {\n"+_vg(6)+"      logger.warn('DB list failed — falling back to memory', { error: reason });\n")
V6=("    } catch (err: any) {\n      logger.warn('DB revoke update failed — kept in memory', { error: err?.message });\n",
    "    } catch (err: any) {\n"+_vg(6)+"      logger.warn('DB revoke update failed — kept in memory', { error: reason });\n")
VC=dict(reuse="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (`const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw), inline; no helper exists in this file and none is added. The sibling catches of this file (`ensureTable`, `loadFromDb`, line 436) already carry a guard and are untouched.",
 prod=PV, rdir=SV+'vc-issuer', sib="`ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts` (the merged sibling suite of this very file)",
 ref=SV+'vc-issuer/src/__tests__/ks1868-credentialrepo-loadfromdb-unreadable-throw.test.ts')
K8=copy.deepcopy(T['p7']); K8.update(VC)
K8.update(dict(dir='ks_1868_o90_p8_vc_issuer_credential_repo_read_catches_guard_message', edits=[V1,V2,V3], nh=3,
 lines='119 (`getById` catch), 160 (`getRecordById` catch) and 188 (`getByHash` catch)',
 test=SV+'vc-issuer/src/__tests__/ks1868-credentialrepo-read-catches-unreadable-throw.test.ts', tsrc='t90_k8.ts.txt',
 fn='the three DB read catches (getById, getRecordById, getByHash) of `src/repositories/credentialRepo.ts`',
 short='the unguarded `err?.message` reads in the getById, getRecordById and getByHash catches',
 premise="`%s` lines 119, 160 and 188 (`error: err?.message` in the catches of getById, getRecordById and getByHash) pass the thrown value's message straight into the logger with no guard around the read" % PV,
 whatwrong="Three DB read catches of the credential repository pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW, so the read REJECTS where an ordinary Error gets a logged warning and the documented in-memory fallback. The fix is the house guard placed before each logger call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The three hunks are ~28 and ~41 lines apart. The write/revoke/list catches of this file (lines 96-99, 392, 481) are a separate brief (O90-P9) and untouched here; `getReadableByHash` (line 303) is deliberately not taken (see Skipped).",
 callers="CALLERS: `getById` is the public verify path's revocation lookup (services/revocationResolvers.ts) and `revoke`; `getRecordById` serves GET /api/credentials/:id; `getByHash` is kept for the repository's own cells. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the failure is logged at warn level and the read falls back to the in-memory store. Today (hostile value): the catch throws and the read rejects to its caller. After: exactly the ordinary-Error rows. Persisted state: none (read paths). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the read logs text and falls back to memory instead of rejecting; every ordinary Error behaves exactly as before. **Recommend TIER 2 (credential verify and revocation lookup): the raise seat must read what revocationResolvers does with a rejection versus with the memory fallback before stating 'today' in the PR.**",
 ncells='9 cells: C1 to C3 controls, R1 to R6 red',
 red1="At the tip the catch throws while building the meta object (the read rejects) or the logged value is not text, so the assertion fails",
 dbnote="`../db` is a plain stand-in (`isDbAvailable` true; the table check `LIMIT 0` answers; every other statement rejects with the value under test through a plain function); `../utils/logger` is a plain recording object; the real repository functions are called with ids and a hash that no memory entry holds; no database, no network.",
 greens="'control ks1868 C1', 'C2' and 'C3' (an ordinary Error at getById, getRecordById and getByHash), already true at the tip (3 cells)",
 redcells="`R1` to `R6` (each of the three reads rejects with a revoked Proxy and with an Error whose message getter throws) (6 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,7))))
T['k8']=K8
K9=copy.deepcopy(T['p7']); K9.update(VC)
K9.update(dict(dir='ks_1868_o90_p9_vc_issuer_credential_repo_store_list_revoke_catches_guard_message', edits=[V4,V5,V6], nh=3,
 lines='96-100 (`store` DB-write catch), 392 (`selectList` catch, reached by `list`) and 481 (`revoke` DB-update catch)',
 test=SV+'vc-issuer/src/__tests__/ks1868-credentialrepo-store-list-revoke-catches-unreadable-throw.test.ts', tsrc='t90_k9.ts.txt',
 fn='the store, list (selectList) and revoke DB catches of `src/repositories/credentialRepo.ts`',
 short='the unguarded `err?.message` reads in the store, selectList and revoke catches',
 premise="`%s` lines 98, 392 and 481 (`error: err?.message` in the catches of store, selectList and revoke) pass the thrown value's message straight into the logger with no guard around the read" % PV,
 whatwrong="Three DB catches of the credential repository pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW, so `store`, `list`/`listReadable` and `revoke` REJECT where an ordinary Error gets a logged warning and the in-memory result (store: the credential is already in memory and the call resolves; list: the memory list; revoke: the revoked credential, already written to memory). The fix is the house guard placed before each logger call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason` (the multi-line `store` log keeps `credentialId`). The hunks are ~290 and ~90 lines apart. The three READ catches (lines 119, 160, 188) are a separate brief (O90-P8).",
 callers="CALLERS: `store` is called by the credential issue route; `revoke` by the revoke route; `list`/`listReadable` (via `selectList`) by the list route. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the failure is logged at warn level and the call completes on the in-memory store (the credential is kept in memory; revoke answers the revoked credential; list answers the memory list). Today (hostile value): the catch throws and the call rejects to its route. After: exactly the ordinary-Error rows. Persisted state: for store and revoke the memory write happens BEFORE the DB call in both cases, so persisted state is identical; the DB statement failed either way. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the call logs text and completes on memory instead of rejecting; every ordinary Error behaves exactly as before. **Recommend TIER 2 (credential issue/revoke): the raise seat must read what the issue and revoke routes answer on a rejection versus on the memory result before stating 'today' in the PR (a revoke that answers success while the DB row stays unrevoked is today's behaviour for an ordinary Error as well).**",
 ncells='9 cells: C1 to C3 controls, R1 to R6 red',
 red1="At the tip the catch throws while building the meta object (the call rejects) or the logged value is not text, so the assertion fails",
 dbnote="`../db` is a plain stand-in (`isDbAvailable` true; every statement answers an empty row set except the one kind a cell names, the INSERT, the UPDATE or the COUNT, which rejects with the value under test through a plain function); `../utils/logger` is a plain recording object; the real repository functions are called; no database, no network.",
 greens="'control ks1868 C1', 'C2' and 'C3' (an ordinary Error at the store INSERT, the revoke UPDATE and the list COUNT), already true at the tip (3 cells)",
 redcells="`R1` to `R6` (each of the three statements rejects with a revoked Proxy and with an Error whose message getter throws) (6 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,7))))
T['k9']=K9

# ---- k10: m365-integration oauthState.ts: save + consume DB catches (vitest, 2 hunks). OAuth path: TIER 1.
PO2=SV+'m365-integration/src/oauthState.ts'
O1=("  } catch (err: any) {\n    logger.warn('DB save OAuth state failed', { error: err?.message });\n",
    "  } catch (err: any) {\n"+_vg(4)+"    logger.warn('DB save OAuth state failed', { error: reason });\n")
O2=("  } catch (err: any) {\n    logger.warn('DB consume OAuth state failed', { error: err?.message });\n",
    "  } catch (err: any) {\n"+_vg(4)+"    logger.warn('DB consume OAuth state failed', { error: reason });\n")
K10=copy.deepcopy(T['p7']); K10.update(dict(prod=PO2, rdir=SV+'m365-integration', edits=[O1,O2], nh=2,
 reuse="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (`const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw), inline; no helper exists in this file and none is added.",
 sib="`ks1677-the-oauth-state-holds-without-a-database.test.ts` (the same module under test with ./db mocked)",
 ref=SV+'m365-integration/src/__tests__/ks1677-the-oauth-state-holds-without-a-database.test.ts',
 dir='ks_1868_o90_p10_m365_integration_oauth_state_db_catches_guard_message',
 lines='96 (`saveOAuthState` catch) and 130 (`consumeOAuthState` catch)',
 test=SV+'m365-integration/src/__tests__/ks1868-oauth-state-db-catches-unreadable-throw.test.ts', tsrc='t90_k10.ts.txt',
 fn='the two DB catches (saveOAuthState, consumeOAuthState) of `src/oauthState.ts`',
 short='the unguarded `err?.message` reads in the saveOAuthState and consumeOAuthState catches',
 premise="`%s` lines 96 and 130 (`error: err?.message` in the catches of saveOAuthState and consumeOAuthState) pass the thrown value's message straight into the logger with no guard around the read" % PO2,
 whatwrong="Two DB catches of the Microsoft 365 OAuth state store pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW, so `saveOAuthState` and `consumeOAuthState` REJECT where an ordinary Error gets a logged warning and the documented outcome (save: the state is already in the in-memory map and the call resolves; consume: `null`). The fix is the house guard placed before each logger call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The two hunks are ~34 lines apart. Nothing else in the file is touched: the token encryption and the binding-hash comparison are not edited.",
 callers="CALLERS: `saveOAuthState` is called when a sign-in starts and `consumeOAuthState` by the OAuth callback (see the ks1677 callback suite). WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the failure is logged at warn level; save resolves (the state stays in memory), consume answers `null` (the callback then refuses the unknown state: fail-closed). Today (hostile value): the catch throws and the call rejects to the route. After: exactly the ordinary-Error rows. Persisted state: identical (the DB statement failed either way; the in-memory state map is written before the DB call in both cases). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the call logs text and takes the same outcome as for an ordinary Error instead of rejecting; every ordinary Error behaves exactly as before. **Recommend TIER 1: OAuth state path (security). The change is log-only and the consume outcome `null` is the fail-closed one, but the raise seat must read the callback's handling of a rejection versus `null` before stating 'today' in the PR.**",
 ncells='6 cells: C1 and C2 controls, R1 to R4 red',
 red1="At the tip the catch throws while building the meta object (the call rejects) or the logged value is not text, so the assertion fails",
 dbnote="`../db` is a plain stand-in (`isDbAvailable` true, `query` rejecting with the value under test through a plain function); `../security/tokenCrypto` and `../utils/logger` are plain stand-ins (the crypto functions return their input, the logger records); the real `saveOAuthState` and `consumeOAuthState` are called; no database, no network.",
 greens="'control ks1868 C1' (save) and 'C2' (consume), each with an ordinary Error, already true at the tip (2 cells)",
 redcells="`R1` and `R2` (the save rejects with a revoked Proxy and with an Error whose message getter throws) and `R3` and `R4` (the same two shapes at the consume) (4 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,5))))
T['k10']=K10

# ---- k11: referral referralService.ts: four DB read catches (vitest)
PR=SV+'referral/src/services/referralService.ts'
def _rs(msg, extra):
    return ("    } catch (err: any) {\n      logger.error('%s', { error: err?.message, %s });\n"%(msg,extra),
            "    } catch (err: any) {\n"+_vg(6)+"      logger.error('%s', { error: reason, %s });\n"%(msg,extra))
R1=_rs('DB read referral code failed','id'); R2=_rs('DB read codes by owner failed','ownerId'); R3=_rs('DB read referrals by referrer failed','referrerId'); R4=_rs('DB read rewards by user failed','userId')
K11=copy.deepcopy(T['p7']); K11.update(dict(prod=PR, rdir=SV+'referral', edits=[R1,R2,R3,R4], nh=4,
 reuse="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (`const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw), inline; no helper exists in this file and none is added.",
 sib="the O90-P4 milestone-service suite (same service, same stand-ins)", ref='Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts',
 dir='ks_1868_o90_p11_referral_service_db_read_catches_guard_message',
 lines='168 (`dbGetReferralCode` catch), 180 (`dbGetCodesByOwner` catch), 204 (`dbGetReferralsByReferrer` catch) and 216 (`dbGetRewardsByUser` catch)',
 test=SV+'referral/src/__tests__/ks1868-referral-service-db-read-catches-unreadable-throw.test.ts', tsrc='t90_k11.ts.txt',
 fn='four DB read catches of `src/services/referralService.ts`',
 short='the unguarded `err?.message` reads in four DB read catches',
 premise="`%s` lines 168, 180, 204 and 216 (`error: err?.message` in the catches of dbGetReferralCode, dbGetCodesByOwner, dbGetReferralsByReferrer and dbGetRewardsByUser) pass the thrown value's message straight into the logger with no guard around the read" % PR,
 whatwrong="Four DB read catches of `ReferralService` pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW, so `getCodeById`, `getUserCodes`, `getReferralsByReferrer` and `getUserRewards` REJECT where an ordinary Error gets a logged failure and the documented fallback (`null` -> `undefined`, or an empty list). The fix is the house guard placed before each logger call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason` (the second meta field is unchanged). The four hunks are ~12 to ~24 lines apart. The three WRITE catches (lines 68, 85, 99), the by-code read (line 192) and the remaining reads of this file are untouched (see Skipped).",
 callers="CALLERS: the four public methods are called by the referral routes and by `getUserStats`/`claimRewards`. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): the failure is logged at error level and the read answers the fallback. Today (hostile value): the catch throws and the read rejects to its caller. After: exactly the ordinary-Error rows. Persisted state: none (read paths). **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the read logs text and answers the same fallback as for an ordinary Error instead of rejecting; every ordinary Error behaves exactly as before. The raise seat should read what the callers (routes, claimRewards via dbGetReward) do with an empty fallback before stating 'today' in the PR.",
 ncells='12 cells: C1 to C4 controls, R1 to R8 red',
 red1="At the tip the catch throws while building the meta object (the read rejects) or the logged value is not text, so the assertion fails",
 dbnote="`../db` is a plain stand-in (`isDbAvailable` true, `query` rejecting with the value under test through a plain function); the service logger `../utils/logger` (`createLogger`) is a plain recording object; the real `referralService` singleton is called; no database, no network.",
 greens="'control ks1868 C1' to 'C4' (an ordinary Error at each of the four reads), already true at the tip (4 cells)",
 redcells="`R1` to `R8` (each of the four reads rejects with a revoked Proxy and with an Error whose message getter throws) (8 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,9))))
T['k11']=K11

# ---- k12: referral fraudDetection.ts loadFromDb catch (1 hunk); k13: transfer delegationService.ts verifyDbReady + processExpiredDelegations (console)
PF=SV+'referral/src/services/fraudDetection.ts'
F1=("    } catch (err: any) {\n      logger.warn('Failed to load fraud data from DB — starting empty', { error: err?.message });\n",
    "    } catch (err: any) {\n"+_vg(6)+"      logger.warn('Failed to load fraud data from DB — starting empty', { error: reason });\n")
GUARD_COMMON="This follows the guard that the merged and held KS-1868 passes use for `err?.message` reads (`const m = ...message; reason = m === undefined || m === null ? m : String(m);` inside a `try`, constant on throw), inline; no helper exists in this file and none is added."
K12=copy.deepcopy(T['p7']); K12.update(dict(prod=PF, rdir=SV+'referral', edits=[F1], nh=1, reuse=GUARD_COMMON,
 sib="the O90-P4 milestone-service suite (same service, same stand-ins)", ref='Blockchain/Dev/services/auth/src/__tests__/ks1868-oauth-authorize-token-unreadable-throw.test.ts',
 dir='ks_1868_o90_p12_referral_fraud_detection_load_from_db_catch_guard_message',
 lines='114 (the catch of `loadFromDb`)', test=SV+'referral/src/__tests__/ks1868-fraud-detection-load-from-db-catch-unreadable-throw.test.ts', tsrc='t90_k12.ts.txt',
 fn='the `loadFromDb` catch of `src/services/fraudDetection.ts`', short='the unguarded `err?.message` read in the `loadFromDb` catch',
 premise="`%s` line 114 (`error: err?.message` in the `loadFromDb` catch) passes the thrown value's message straight into the logger with no guard around the read" % PF,
 whatwrong="The catch of `FraudDetectionService.loadFromDb` passes `err?.message` straight into the logger's meta object, unguarded. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW, so `loadFromDb` REJECTS where an ordinary Error gets a logged warning and a resolved call (the service starts with empty fraud data); an Error whose `message` is readable but not a string (a Symbol) is handed to the logger uncoerced. The fix is the house guard placed before the logger call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then `error: reason`. The empty catch of `dbLogFraud` reads nothing and is untouched.",
 callers="CALLERS: `loadFromDb` is called once at boot by `src/index.ts` (the raise seat must read the call site before stating 'today' in the PR). WHAT AN ORDINARY ERROR GETS (the rule for taking the site): the failure is logged at warn level and the call resolves; the in-memory fraud maps stay empty. Today (hostile value): the catch throws and `loadFromDb` rejects to the boot caller. After: exactly the ordinary-Error row. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the failure is logged as text and the call resolves instead of rejecting; every ordinary Error behaves exactly as before. Fraud-screening data fails EMPTY for an ordinary Error as well (a degraded start); the raise seat should say so.",
 ncells='5 cells: C1 and C2 controls, R1 to R3 red', red1="At the tip the catch throws while building the meta object (loadFromDb rejects) or the logged value is not text, so the assertion fails",
 dbnote="`../db` is a plain stand-in (`isDbAvailable` true, `query` rejecting with the value under test through a plain function); the service logger `../utils/logger` (`createLogger`) is a plain recording object; the real `fraudDetectionService` singleton is called; no database, no network.",
 greens="'control ks1868 C1' (an ordinary Error) and 'C2' (a plain string), both already true at the tip (2 cells)",
 redcells="`R1` to `R3` (a revoked Proxy, an Error whose message getter throws, an Error whose message is a Symbol) (3 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,4))))
T['k12']=K12
PD=SV+'transfer/src/services/delegationService.ts'
D1=("  } catch (err: any) {\n    console.warn('[delegationService] DB tables not ready:', err?.message);\n",
    "  } catch (err: any) {\n"+_vg(4)+"    console.warn('[delegationService] DB tables not ready:', reason);\n")
D2=("    } catch (err: any) {\n      console.error('[delegationService] processExpiredDelegations error:', err?.message);\n",
    "    } catch (err: any) {\n"+_vg(6)+"      console.error('[delegationService] processExpiredDelegations error:', reason);\n")
K13=copy.deepcopy(T['p7']); K13.update(dict(prod=PD, rdir=SV+'transfer', edits=[D1,D2], nh=2, reuse=GUARD_COMMON,
 sib="`ks1410-delegations-process-expired-500.test.ts` (the same module under test)", ref=SV+'transfer/src/__tests__/ks1410-delegations-process-expired-500.test.ts',
 dir='ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message',
 lines='170 (the catch of `verifyDbReady`) and 494 (the catch of `processExpiredDelegations`)', test=SV+'transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts', tsrc='t90_k13.ts.txt',
 fn='the `verifyDbReady` and `processExpiredDelegations` catches of `src/services/delegationService.ts`', short='the unguarded `err?.message` reads in the two console-logging catches',
 premise="`%s` lines 170 and 494 (`err?.message` as a console argument in the catches of verifyDbReady and processExpiredDelegations) read the thrown value with no guard around the read" % PD,
 whatwrong="Two catches of the delegation service pass `err?.message` straight into a console call, unguarded: `console.warn('[delegationService] DB tables not ready:', err?.message)` in `verifyDbReady` and `console.error('[delegationService] processExpiredDelegations error:', err?.message)` in `processExpiredDelegations`. `?.` guards a null or undefined value only: a thrown value whose read throws (a revoked Proxy: the `.message` get throws; an Error whose `message` getter throws) makes the catch THROW while the call's arguments are built, so `verifyDbReady` and `processExpiredDelegations` REJECT where an ordinary Error gets a console line and the documented outcome (`verifyDbReady` resolves, `processExpiredDelegations` answers 0). The fix is the house guard placed before each console call: read the message once inside a `try` (`?.` kept), keep `undefined`/`null` as they are, coerce anything else with `String(...)`, fall back to the constant `'unreadable thrown value'` when the read or the coercion throws; then pass `reason`. The two hunks are ~320 lines apart.",
 callers="CALLERS: `verifyDbReady` is called once at boot by `src/index.ts`; `processExpiredDelegations` by the process-expired route (ks1410 / ks1845 suites) and any scheduler. WHAT AN ORDINARY ERROR GETS (the rule for taking the sites): a console line and the outcome above. Today (hostile value): the catch throws and the call rejects (for the route that is the 500 the ks1410 suite pins for a DB error; for boot an unhandled rejection). After: exactly the ordinary-Error rows. Persisted state: none. **BEHAVIOUR CHANGE the raise PR must state:** for an unreadable, non-string-message, null or undefined thrown value only: the failure is written as text and the call takes the same outcome as for an ordinary Error instead of rejecting (the raise seat must read the ks1410 suite and the route to say whether processExpiredDelegations answering 0 versus a 500 is the same for an ordinary Error; this brief takes the site only because both read the same).",
 ncells='6 cells: C1 and C2 controls, R1 to R4 red', red1="At the tip the catch throws while building the console arguments (the call rejects) or the written value is not text, so the assertion fails",
 dbnote="`../db` is a plain stand-in (`isDbAvailable` true, `query` rejecting with the value under test through a plain function); `console.warn` and `console.error` are replaced by plain recording functions for the duration of each cell; the real `verifyDbReady` and `delegationService.processExpiredDelegations` are called; no database, no network.",
 greens="'control ks1868 C1' (verifyDbReady) and 'C2' (processExpiredDelegations), each with an ordinary Error, already true at the tip (2 cells)",
 redcells="`R1` and `R2` (verifyDbReady with a revoked Proxy and with an Error whose message getter throws) and `R3` and `R4` (the same two shapes at processExpiredDelegations) (4 cells)",
 redlines="".join("- RED ks1868 R%d\n"%i for i in range(1,5))))
T['k13']=K13
