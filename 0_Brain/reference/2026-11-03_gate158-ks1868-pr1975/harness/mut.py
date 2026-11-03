import sys,subprocess,os,json
X=sys.argv[1]; D=sys.argv[2]
P=X+"/src/services/delegationService.ts"
orig=open(D+"/harness/delegationService.head.ts").read()
muts={
 "M1_const_to_undefined":("reason = 'unreadable thrown value';","reason = undefined;"),
 "M2_String_m_to_m":("String(m)","m"),
 "M3_inner_catch_rethrows":("} catch {\n        reason = 'unreadable","} catch (e) {\n        throw e; reason = 'unreadable"),
 "M4_optional_chain_dropped":("const m = err?.message;","const m = err.message;"),
 "M5_const_text_changed":("'unreadable thrown value'","'unknown'"),
 "M6_log_field_blanked":("reason);","undefined);"),
 "M7_read_hoisted_out_of_try":None,
}
# Locate the two blocks: occurrence 0 = verify, 1 = expire. Indent differs (4 vs 6 spaces).
def apply(src,site,name):
    ind="    " if site==0 else "      "
    blk_start=[i for i in range(len(src)) if src.startswith(ind+"let reason: string | null | undefined;",i)]
    # choose by site via the 'let reason' occurrences after catch (err: any) in the two functions
    idxs=[]; pos=0
    while True:
        j=src.find("let reason: string | null | undefined;",pos)
        if j<0: break
        idxs.append(j); pos=j+1
    start=idxs[site]
    end=src.find("\n",src.find("console.",start))  # end of console line
    blk=src[start:end]
    if name=="M7_read_hoisted_out_of_try":
        new=blk.replace("let reason: string | null | undefined;","let reason: string | null | undefined;\n    const m0 = err?.message;",1).replace("const m = err?.message;","const m = m0;",1)
        if new==blk: return None
    elif name=="M3_inner_catch_rethrows":
        import re
        new=re.sub(r"\} catch \{\n(\s+)reason = 'unreadable thrown value';",r"} catch (e) {\n\1throw e;",blk)
        if new==blk: return None
    elif name=="M6_log_field_blanked":
        new=blk[:blk.rfind("reason)")]+"undefined)"
    else:
        a,b=muts[name]; new=blk.replace(a,b,1)
        if new==blk: return None
    return src[:start]+new+src[end:]
res={}
for site in (0,1):
  for name in muts:
    m=apply(orig,site,name)
    if m is None: res[f"{name}@{'verify' if site==0 else 'expire'}"]="NOOP"; continue
    open(P,"w").write(m)
    r=subprocess.run(["npx","vitest","run","src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts"],cwd=X,capture_output=True,text=True)
    out=r.stdout+r.stderr
    failed=[l.strip()[:60] for l in out.splitlines() if l.strip().startswith("×")]
    ok=("Tests " in out)
    res[f"{name}@{'verify' if site==0 else 'expire'}"]=(("KILLED" if r.returncode!=0 else "SURVIVED") if ok else "RUNNER-BROKEN")+" "+" | ".join(x[2:30] for x in failed)
open(P,"w").write(orig)
print(json.dumps(res,indent=1))
