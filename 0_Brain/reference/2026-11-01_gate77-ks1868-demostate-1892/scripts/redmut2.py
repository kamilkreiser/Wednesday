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
BLK="""    let message: string;
    try {
      message = err instanceof Error ? err.message : 'Unknown error';
    } catch {
      message = 'unreadable thrown value';
    }
"""
MUT={
 'M5 Error.message dropped (String(err))':("      message = err instanceof Error ? err.message : 'Unknown error';\n    } catch","      message = String(err);\n    } catch"),
 'M6 Unknown error constant changed':("      message = err instanceof Error ? err.message : 'Unknown error';\n    } catch","      message = err instanceof Error ? err.message : 'Other';\n    } catch"),
 'M8 logger key renamed':("logger.error('Failed to read demo state', { error: message });","logger.error('Failed to read demo state', { err: message });"),
 'M14 instanceof dropped (always err.message)':("      message = err instanceof Error ? err.message : 'Unknown error';\n    } catch","      message = (err as Error).message;\n    } catch"),
}
for name,(a,b) in MUT.items():
    if orig.count(a)!=1: print(name,'PATTERN COUNT',orig.count(a),flush=True); continue
    open(path,'w').write(orig.replace(a,b))
    log=f"{W}/logs/mut_{name.split()[0]}.log"
    rc,tl=run(log); open(path,'w').write(orig)
    assert sha(path)==h0,'RESTORE FAIL'
    print(f"{name}: rc={rc} {'KILLED' if rc else 'SURVIVED'} {tl} sha_restored=OK",flush=True)
print('final sha',sha(path),'orig',h0)
