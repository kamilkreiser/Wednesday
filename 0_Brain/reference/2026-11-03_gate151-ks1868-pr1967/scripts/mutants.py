import subprocess, hashlib, json, re
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate151-ks1868-pr1967'
D=W+'/repo/Blockchain/Dev'; S=D+'/services/demo-service'; ST=S+'/src/routes/state.ts'
head=open(W+'/scripts/state_head.ts').read(); hsha=hashlib.sha256(head.encode()).hexdigest()
L_OLD="""      let message: string;
      try {
        message = err instanceof Error ? err.message : 'Unknown error';
      } catch {
        message = 'unreadable thrown value';
      }
      logger.warn('Redis unavailable, using in-memory state', { error: message });
      redis = null;"""
P_OLD="""    let message: string;
    try {
      message = err instanceof Error ? err.message : 'Unknown error';
    } catch {
      message = 'unreadable thrown value';
    }
    logger.error('Failed to toggle presenter mode', { error: message });"""
assert head.count(L_OLD)==1 and head.count(P_OLD)==1
def L(new): return head.replace(L_OLD,new)
def P(new): return head.replace(P_OLD,new)
IND6='      '; IND4='    '
M={}
M['L0 revert to unguarded err.message']=L("""      logger.warn('Redis unavailable, using in-memory state', { error: err.message });
      redis = null;""")
M['L1 inner try dropped']=L("""      const message = err instanceof Error ? err.message : 'Unknown error';
      logger.warn('Redis unavailable, using in-memory state', { error: message });
      redis = null;""")
M['L2 constant text changed']=L(L_OLD.replace("'unreadable thrown value'","'x'"))
M['L3 catch rethrows']=L(L_OLD.replace("message = 'unreadable thrown value';","throw new Error('r');"))
M['L4 redis = null removed']=L(L_OLD.replace("\n      redis = null;",""))
M['L5 redis = null only when read ok (moved into try)']=L(L_OLD.replace("\n      redis = null;","").replace("message = err instanceof Error ? err.message : 'Unknown error';","message = err instanceof Error ? err.message : 'Unknown error';\n        redis = null;"))
M['L6 instanceof inverted']=L(L_OLD.replace("err instanceof Error ?","!(err instanceof Error) ?"))
M['L7 always constant unreadable (message never read)']=L(L_OLD.replace("message = err instanceof Error ? err.message : 'Unknown error';","message = 'unreadable thrown value';"))
M['L8 Unknown error text changed']=L(L_OLD.replace("'Unknown error'","'zzz'"))
M['L9 log line dropped']=L(L_OLD.replace("      logger.warn('Redis unavailable, using in-memory state', { error: message });\n",""))
M['P0 revert to unguarded']=P("""    const message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Failed to toggle presenter mode', { error: message });""")
M['P1 inner try dropped (same as P0 form w/ let)']=P("""    let message: string;
    message = err instanceof Error ? err.message : 'Unknown error';
    logger.error('Failed to toggle presenter mode', { error: message });""")
M['P2 constant text changed']=P(P_OLD.replace("'unreadable thrown value'","'x'"))
M['P3 catch rethrows']=P(P_OLD.replace("message = 'unreadable thrown value';","throw new Error('r');"))
M['P4 always constant']=P(P_OLD.replace("message = err instanceof Error ? err.message : 'Unknown error';","message = 'unreadable thrown value';"))
M['P5 instanceof inverted']=P(P_OLD.replace("err instanceof Error ?","!(err instanceof Error) ?"))
M['P6 Unknown error text changed']=P(P_OLD.replace("'Unknown error'","'zzz'"))
M['P7 log line dropped']=P(P_OLD.replace("\n    logger.error('Failed to toggle presenter mode', { error: message });",""))
M['P8 status 500 -> 200 (outside guard, control mutant)']=head.replace("return res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });\n  }\n});\n\n","return res.status(200).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });\n  }\n});\n\n",1) if False else None
del M['P8 status 500 -> 200 (outside guard, control mutant)']
res=[]
import sys
for name,src in M.items():
    if len(sys.argv)>1 and not name.startswith(sys.argv[1]): continue
    assert src!=head, name
    open(ST,'w').write(src)
    p=subprocess.run([D+'/node_modules/.bin/vitest','run','--root',S,'--maxWorkers=2','src/__tests__/ks1868-state-redis'],capture_output=True,text=True)
    out=p.stdout+p.stderr
    failed=re.findall(r'×\s+(\w+ ks1868 \w+)',out)
    assertion='AssertionError' in out
    open(ST,'w').write(head)
    ok=hashlib.sha256(open(ST,'rb').read()).hexdigest()==hsha
    r={'mutant':name,'rc':p.returncode,'killed':p.returncode!=0,'red_cells':sorted(set(failed)),'assertion':assertion,'restored':ok}
    res.append(r); print(json.dumps(r),flush=True)
