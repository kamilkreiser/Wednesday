import hashlib, subprocess
W='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate76-ks1868-nft-1891'
R=W+'/repo'
path=R+'/Blockchain/Dev/services/nft-certificate/src/cardano/provider.ts'
rel='Blockchain/Dev/services/nft-certificate/src/cardano/provider.ts'
TEST='src/__tests__/ks1868-provider-fetch-protocol-params-unreadable-throw.test.ts'
sha=lambda p: hashlib.sha256(open(p,'rb').read()).hexdigest()
orig=open(path).read(); h0=sha(path); print('head product sha',h0)
def run(name,src):
    open(path,'w').write(src)
    log=f"{W}/logs/{name}.log"
    rc=subprocess.run([W+'/scripts/vt.sh',log,TEST]).returncode
    open(path,'w').write(orig); assert sha(path)==h0,'RESTORE FAIL'
    tl=[l.strip() for l in open(log).read().splitlines() if l.strip().startswith(('Tests ','Test Files'))]
    print(f"{name}: rc={rc} {'KILLED' if rc else 'SURVIVED'} {tl} sha_restored=OK",flush=True)
base=subprocess.run(['git','-C',R,'show','refs/gate/develop:'+rel],capture_output=True,text=True,check=True).stdout
run('red_base',base)
run('green_head',orig)
BLOCK="""    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
"""
MUT={
 'M1 fallback string changed': ("reason = 'unreadable thrown value';","reason = 'x';"),
 'M2 read hoisted outside inner try': (BLOCK,"    const reason: string = err instanceof Error ? err.message : String(err);\n"),
 'M3 inner catch rethrows': ("reason = 'unreadable thrown value';","throw new Error('rethrow');"),
 'M4 return null changed to return cached stub (undefined)': ("    return null;\n  }\n}","    return undefined as never;\n  }\n}"),
 'M5 log message text changed': ("'Failed to fetch protocol parameters'","'Failed to fetch params'"),
 'M6 inner catch leaves reason unset': ("      reason = 'unreadable thrown value';\n","      reason = undefined as never;\n"),
 'M7 Error.message dropped (String(err))': ("err instanceof Error ? err.message : String(err);\n    } catch","String(err);\n    } catch"),
 'M8 log key renamed': ("{ error: reason }","{ err: reason }"),
 'M9 instanceof check dropped': ("err instanceof Error ? err.message : String(err);\n    } catch","String(err);\n    } catch"),
 'M10 non-Error branch constant': ("err instanceof Error ? err.message : String(err);\n    } catch","err instanceof Error ? err.message : 'x';\n    } catch"),
 'M11 logger.error removed': ("    logger.error('Failed to fetch protocol parameters', { error: reason });\n",""),
 'M12 return true-ish object instead of null': ("    return null;\n  }\n}","    return {} as never;\n  }\n}"),
}
for name,(a,b) in MUT.items():
    if orig.count(a)!=1: print(name,'PATTERN COUNT',orig.count(a)); continue
    run('mut_'+name.split()[0],orig.replace(a,b))
print('final sha',sha(path),'orig',h0)
