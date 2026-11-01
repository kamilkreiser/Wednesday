import hashlib, subprocess, shutil
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892'
path=W+'/repo/Blockchain/Dev/services/demo-service/src/routes/state.ts'
base='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/2dc9c5a2-efc6-4975-a82f-157a5a9bc219/scratchpad/state_base.ts'
TEST='src/__tests__/ks1868-state-get-unreadable-throw.test.ts'
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
orig=open(path).read(); h0=sha(path)
def run(log):
    rc=subprocess.run([W+'/scripts/vt.sh',log,TEST]).returncode
    tl=[l.strip() for l in open(log).read().splitlines() if l.strip().startswith('Tests ')]
    return rc,tl
# red-first
shutil.copy(base,path); print('base sha',sha(path))
rc,tl=run(W+'/logs/red_base.log'); open(path,'w').write(orig); assert sha(path)==h0
print('RED base: rc',rc,tl,'restored OK',flush=True)
BLK="""    let message: string;
    try {
      message = err instanceof Error ? err.message : 'Unknown error';
    } catch {
      message = 'unreadable thrown value';
    }
"""
MUT={
 'M1 fallback string changed':("message = 'unreadable thrown value';","message = 'x';"),
 'M2 inner try removed (read hoisted)':(BLK,"    const message: string = err instanceof Error ? err.message : 'Unknown error';\n"),
 'M3 inner catch rethrows':("message = 'unreadable thrown value';","throw new Error('rethrow');"),
 'M4 inner catch leaves message undefined':("      message = 'unreadable thrown value';\n","      message = undefined as never;\n"),
 'M5 Error.message dropped (String(err))':("message = err instanceof Error ? err.message : 'Unknown error';","message = String(err);"),
 'M6 Unknown error constant changed':("err.message : 'Unknown error';","err.message : 'Other';"),
 'M7 logger text changed':("'Failed to read demo state'","'Failed state'"),
 'M8 logger key renamed':("{ error: message }","{ err: message }"),
 'M9 final response changed to 500':("    logger.error('Failed to read demo state', { error: message });\n    return res.json(inMemoryState);","    logger.error('Failed to read demo state', { error: message });\n    return res.status(500).json(inMemoryState);"),
 'M10 final response body emptied':("    return res.json(inMemoryState);\n  }\n});\n\n// ====","    return res.json({});\n  }\n});\n\n// ===="),
 'M11 log skipped':("    logger.error('Failed to read demo state', { error: message });\n    return res.json(inMemoryState);","    return res.json(inMemoryState);"),
 'M12 error message leaked in response':("    logger.error('Failed to read demo state', { error: message });\n    return res.json(inMemoryState);","    logger.error('Failed to read demo state', { error: message });\n    return res.json({ ...inMemoryState, error: message });"),
 'M13 inner catch swallowed log message to empty':("message = 'unreadable thrown value';","message = '';"),
}
for name,(a,b) in MUT.items():
    if orig.count(a)!=1: print(name,'PATTERN COUNT',orig.count(a),flush=True); continue
    open(path,'w').write(orig.replace(a,b))
    log=f"{W}/logs/mut_{name.split()[0]}.log"
    rc,tl=run(log); open(path,'w').write(orig)
    assert sha(path)==h0,'RESTORE FAIL'
    print(f"{name}: rc={rc} {'KILLED' if rc else 'SURVIVED'} {tl} sha_restored=OK",flush=True)
print('final sha',sha(path),'orig',h0)
