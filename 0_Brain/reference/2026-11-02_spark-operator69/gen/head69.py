# Operator 69: KS-1868 originate routes/certifications.ts route catches (inline `let reason` guard already merged in this file at :1086). Jest. Reuses spark/gen/mk.py (rd, udiff).
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='cde2dee4dffba6a61228c40d641ff567660c32b2'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator69/gen/'
SV='Blockchain/Dev/services/originate/'
TD=SV+'src/__tests__/'
REF=TD+'ks1844-get-certification-by-id-answers-a-hostile-throw.test.ts'
def G(ind,var):
    s=' '*ind
    return (s+"let reason: string;\n"+s+"try {\n"+s+"  reason = %s;\n"%var+s+"} catch {\n"+s+"  reason = 'unreadable thrown value';\n"+s+"}\n")
E="error instanceof Error ? error.message : String(error)"
def pair(ctx):
    o="      logger.error('%s', { error: %s });\n"%(ctx,E)
    n=G(6,E)+"      logger.error('%s', { error: reason });\n"%ctx
    return (o,n)
OPEN_PR="No open PR touches this file or its `src/__tests__/` neighbours (the 22 open PRs read 2026-11-02 through the GitHub API; 125 file entries; services/originate appears only as package.json in PRs 575/949/1726 and integration tests in PRs 1790/1792/1794; positive control services/auth present in 7 entries)."
