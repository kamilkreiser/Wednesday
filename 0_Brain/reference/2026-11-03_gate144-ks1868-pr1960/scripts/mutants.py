import re,subprocess,hashlib,os,json
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate144-ks1868-pr1960'
D=W+'/repo/Blockchain/Dev'; A=D+'/services/api-gateway'; V=D+'/node_modules/.bin/vitest'
P=A+'/src/services/redis.ts'
T='src/__tests__/ks1868-gateway-redis-listener-and-connect-catch-unreadable-throw.test.ts'
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
orig=open(P).read(); H=sha(P)
# site 0 = listener block, site 1 = initRedis catch block (+ its uses)
L0s=orig.index("    redisClient.on('error', (err) => {"); L0e=orig.index("    redisClient.on('close'")
C1s=orig.index("  } catch (error) {\n    let reason"); C1e=orig.index("export function isRedisAvailable")
assert L0s<L0e<C1s<C1e
common={
 'M1_inner_try_dropped':[('try {','if (true) {'),('} catch {','} else {')],
 'M2_const_text':[("'unreadable thrown value'","'x'")],
 'M3_no_String':[(': String(m);',': m;')],
 'M5_String_for_all':[('m === undefined || m === null ? m : String(m)','String(m)')],
 'M6_null_becomes_text':[('m === undefined || m === null ? m : String(m)','m === undefined ? m : String(m)')],
 'M7_undefined_becomes_text':[('m === undefined || m === null ? m : String(m)','m === null ? m : String(m)')],
 'M9_catch_rethrows':[("reason = 'unreadable thrown value';",'throw new Error("mut");')],
}
site0=dict(common)
site0.update({
 'M0_revert':[("      let reason: string | null | undefined;\n      try {\n        const m = err?.message;\n        reason = m === undefined || m === null ? m : String(m);\n      } catch {\n        reason = 'unreadable thrown value';\n      }\n      logger.error('[Redis] Connection error', { error: reason });","      logger.error('[Redis] Connection error', { error: err.message });")],
 'M4_no_optional_chain':[('err?.message','err.message')],
 'M8_always_constant':[('const m = err?.message;','const m = (() => { throw 0; })();')],
 'M10_log_drops_error':[("logger.error('[Redis] Connection error', { error: reason });","logger.error('[Redis] Connection error', {});")],
 'M11_flag_clear_before_guard_removed':[("      isConnected = false;\n    });\n","    });\n")],
 'M12_flag_clear_only_on_readable':[("        reason = m === undefined || m === null ? m : String(m);\n","        reason = m === undefined || m === null ? m : String(m);\n        isConnected = false;\n"),("      isConnected = false;\n    });\n","    });\n")],
})
site1=dict(common)
site1.update({
 'M0_revert':[("    let reason: string | null | undefined;\n    try {\n      const m = (error as Error)?.message;\n      reason = m === undefined || m === null ? m : String(m);\n    } catch {\n      reason = 'unreadable thrown value';\n    }\n",""),("error: reason,","error: (error as Error).message,"),("'REDIS_REQUIRED_IN_PRODUCTION: ' + reason","'REDIS_REQUIRED_IN_PRODUCTION: ' + (error as Error).message"),("(dev/test only)', { error: reason }","(dev/test only)', { error: (error as Error).message }")],
 'M4_no_optional_chain':[('(error as Error)?.message','(error as Error).message')],
 'M8_always_constant':[('const m = (error as Error)?.message;','const m = (() => { throw 0; })();')],
 'M10a_prod_log_drops_error':[("        error: reason,\n","")],
 'M10b_dev_log_drops_error':[("(dev/test only)', { error: reason }","(dev/test only)', {}")],
 'M13_prod_fails_open':[("      throw new Error('REDIS_REQUIRED_IN_PRODUCTION: ' + reason);","      fallbackMode = true; return false;")],
 'M14_prod_throw_constant':[("'REDIS_REQUIRED_IN_PRODUCTION: ' + reason","'REDIS_REQUIRED_IN_PRODUCTION: ' + 'unreadable thrown value'")],
})
res=[]
for k,(s,e,M) in enumerate([(L0s,L0e,site0),(C1s,C1e,site1)]):
    for name,reps in M.items():
        blk=orig[s:e]
        for a,c in reps:
            assert a in blk,(k,name,a); blk=blk.replace(a,c,1)
        open(P,'w').write(orig[:s]+blk+orig[e:])
        r=subprocess.run(['nice','-n','10',V,'run','--root',A,T,'--maxWorkers=2'],capture_output=True,text=True)
        txt=r.stdout+r.stderr
        open(f'{W}/logs/mut_site{k}__{name}.log','w').write(txt+f'\nrc={r.returncode}\n')
        failed=sorted(set(re.findall(r'(?:FAIL|×)\s+.*?(?:control|RED) ks1868 (\w+)',txt)))
        open(P,'w').write(orig); ok=sha(P)==H
        res.append((k,name,'KILLED' if r.returncode!=0 else 'SURVIVED',failed,'restore='+str(ok),'assertionerr=%d'%txt.count('AssertionError'),'timeouts=%d'%txt.count('timed out')))
        print(*res[-1],flush=True)
json.dump(res,open(W+'/logs/mutants.json','w'))
