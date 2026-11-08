import difflib
R='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-08_spark-operator102/gen/'
B='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_2053_o102_p2_strip_above_documents_mounts/'
tp='Blockchain/Dev/services/originate/src/__tests__/ks741-emitter-marker-strip.test.ts'
ip='Blockchain/Dev/services/originate/src/index.ts'
t=open(R+'ks741.test.ts.tip',encoding='utf-8').read()
old="    expect(mountLine(without, 'app.use(createEmitterMarkerStrip());')).toBe(-1);\n  });\n});\n"
assert t.count(old)==1
cell='''
  it('the strip mount line sits above BOTH /api/documents mounts (KS-2053)', () => {
    const source = fs.readFileSync(indexPath, 'utf8');
    const strip = mountLine(source, 'app.use(createEmitterMarkerStrip());');
    const publicDocuments = mountLine(source, "app.use('/api/documents', publicDocumentsRouter);");
    const documents = mountLine(source, "app.use('/api/documents', documentsRouter);");
    expect(strip).toBeGreaterThan(0);
    expect(publicDocuments).toBeGreaterThan(0);
    expect(documents).toBeGreaterThan(0);
    expect(strip).toBeLessThan(publicDocuments);
    expect(strip).toBeLessThan(documents);
  });
'''
new="    expect(mountLine(without, 'app.use(createEmitterMarkerStrip());')).toBe(-1);\n  });\n"+cell+"});\n"
n=t.replace(old,new)
def d(a,b,p):
    return 'diff --git a/%s b/%s\n'%(p,p)+''.join(difflib.unified_diff(a.splitlines(True),b.splitlines(True),'a/'+p,'b/'+p,n=3))
open(B+'golden.diff','w',encoding='utf-8').write(d(t,n,tp))
s=open(R+'origin_index.ts.tip',encoding='utf-8').read()
l1='app.use(createEmitterMarkerStrip());\n'
assert s.count(l1)==1
s2=s.replace(l1,'')
l2="app.use('/api/documents', documentsRouter);\n"
assert s2.count(l2)==1
s2=s2.replace(l2,l2+l1)
open(B+'golden_red.diff','w',encoding='utf-8').write(d(s,s2,ip))
