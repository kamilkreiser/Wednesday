import json,sys
G="/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate186-ks1459-pr1798/runs/"
def load(v):
    return {(r['route'],r['caller'],r['current'],r['target']):r for r in json.load(open(G+v+'.json'))}
def allow(r): return r['status']==200
ADM=['STANDARD','ENHANCED','HIGH','GOVERNMENT']
def cmp(a,b,label):
    A,B=load(a),load(b); assert A.keys()==B.keys()
    more=[k for k in A if allow(B[k]) and not allow(A[k])]
    less=[k for k in A if allow(A[k]) and not allow(B[k])]
    diff=[k for k in A if (A[k]['status'],A[k]['code'],A[k]['level'],A[k]['row'],A[k]['calls'])!=(B[k]['status'],B[k]['code'],B[k]['level'],B[k]['row'],B[k]['calls'])]
    reach=[k for k in diff if k[3] in ADM]
    print(f"{label}: cells={len(A)} differing={len(diff)} {b}-more-permissive-than-{a}={len(more)} {b}-more-restrictive={len(less)} differing-with-zod-admitted-target={len(reach)}")
    return diff,more,less,reach
if __name__=='__main__':
    mode=sys.argv[1]
    if mode=='pair':
        d,m,l,r=cmp(sys.argv[2],sys.argv[3],sys.argv[4] if len(sys.argv)>4 else 'cmp')
        for k in d:
            A,B=load(sys.argv[2])[k],load(sys.argv[3])[k]
            print('  ',k,A['status'],A['code'],'->',B['status'],B['code'],'| level',A['level'],'->',B['level'])
