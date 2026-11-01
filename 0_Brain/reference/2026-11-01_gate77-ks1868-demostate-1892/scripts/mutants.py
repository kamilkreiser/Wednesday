import hashlib, subprocess
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892'
path=W+'/repo/Blockchain/Dev/services/demo-service/src/index.ts'
TEST='src/__tests__/ks1868-boot-gate-unreadable-throw.test.ts'
BLOCK="""  let message: string;
  try {
    message = String(err instanceof Error ? err.message : err);
  } catch {
    message = 'unreadable thrown value';
  }
"""
MUT={
 'M1 fallback string changed': ("message = 'unreadable thrown value';","message = 'x';"),
 'M2 read hoisted outside inner try': (BLOCK,"  const message: string = String(err instanceof Error ? err.message : err);\n"),
 'M3 inner catch rethrows': ("message = 'unreadable thrown value';","throw new Error('rethrow');"),
 'M4 gate proceeds on failure (exit removed)': ("  process.exit(1);\n}\n\nconst app","}\n\nconst app"),
 'M5 exit code 0': ("  process.exit(1);\n}\n\nconst app","  process.exit(0);\n}\n\nconst app"),
 'M6 inner catch leaves message unset': ("    message = 'unreadable thrown value';\n","    message = undefined as never;\n"),
 'M7 Error.message dropped (String(err))': ("String(err instanceof Error ? err.message : err)","String(err)"),
 'M8 FATAL prefix changed': ("logger.error(`FATAL: ${message}`)","logger.error(`ERR: ${message}`)"),
 'M9 String() wrapper dropped (probable equivalent)': ("message = String(err instanceof Error ? err.message : err);","message = (err instanceof Error ? err.message : err) as string;"),
 'M10 instanceof check dropped (always String(err))': ("err instanceof Error ? err.message : err","err"),
 'M11 non-Error branch constant': ("err instanceof Error ? err.message : err","err instanceof Error ? err.message : 'x'"),
 'M12 exit before log': ("  logger.error(`FATAL: ${message}`);\n  process.exit(1);","  process.exit(1);\n  logger.error(`FATAL: ${message}`);"),
}
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
orig=open(path).read(); h0=sha(path)
for name,(a,b) in MUT.items():
    if orig.count(a)!=1: print(name,'PATTERN COUNT',orig.count(a)); continue
    open(path,'w').write(orig.replace(a,b))
    log=f"{W}/logs/mut_{name.split()[0]}.log"
    rc=subprocess.run([W+'/scripts/vt.sh',log,TEST]).returncode
    open(path,'w').write(orig)
    assert sha(path)==h0,'RESTORE FAIL'
    tl=[l.strip() for l in open(log).read().splitlines() if l.strip().startswith('Tests ')]
    print(f"{name}: rc={rc} {'KILLED' if rc else 'SURVIVED'} {tl} sha_restored=OK",flush=True)
print('final sha',sha(path),'orig',h0)
