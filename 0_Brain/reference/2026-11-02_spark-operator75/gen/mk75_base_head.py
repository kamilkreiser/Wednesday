# Operator 75: KS-1868 governance remaining catches (jest) + auth routes. Reuses spark/gen/mk.py (rd, udiff). Template text from operators 44 and 71.
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='92a26320e30ad680459cdb96c5b68b91a5f175a5'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator75/gen/'
SV='Blockchain/Dev/services/'
OPEN_PR="No open PR touches this file or its `src/__tests__/` directory (the 23 open PRs read 2026-11-02 through the GitHub API; 141 file entries; planted control services/auth/ present in 7 entries)."
def G(ind,expr):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%expr+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
E1="err instanceof Error ? err.message : String(err)"
def pair(ind,fn,ctx,extra='',expr=E1):
    o=" "*ind+"logger.%s('%s', { %serror: %s });\n"%(fn,ctx,extra,expr)
    n=G(ind,expr)+" "*ind+"logger.%s('%s', { %serror: reason });\n"%(fn,ctx,extra)
    return (o,n)