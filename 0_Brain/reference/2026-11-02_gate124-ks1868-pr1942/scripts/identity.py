import glob, hashlib, os
N='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night'; RU='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs'
SHA={'a1':'6e2c8b6ad3ff1b01c8dabdf3e54fc6dbdfeeebbd6e98717244355d7a6a026a1c','a2':'a66f10897fdab28663a2adb644932fb7a06f223a5e3484132721a628083e6aa3','a3':'0a4ecc94416937e9401c42c84e2401c02dc3fab3656bb2225da2e55cd7cc058a','a4':'df0f48219de0088d5b080594eedc3cdecd5c000828914d560614ca50ac721e4e','a5':'ac3a5ed70e1e5e83d91d3b622adb9c00ba98ea54a328ce384a4c04268a549870'}
for k in sorted(SHA):
    d=[x for x in glob.glob(f'{RU}/spark_secuura_2026-11-02_ks_1868_o79_{k}_*') if not x.endswith(('-control','-control-r2'))]
    assert len(d)==1, d
    c=d[0]+'/out.md.checker'; p=open(c+'/patch.diff','rb').read()
    held=glob.glob(f'{N}/READY_KS-1868-KS-1868-O79-{k.upper()}_*'); assert len(held)==1, held
    h=open(held[0],'rb').read()
    secs=sorted(glob.glob(c+'/section_[0-9].diff'))
    print(k, 'sha', hashlib.sha256(p).hexdigest()[:12], 'eq_brief', hashlib.sha256(p).hexdigest()==SHA[k], 'contained_in_held', p in h, 'sections', len(secs), 'concat_eq', b''.join(open(s,'rb').read() for s in secs)==p, os.path.basename(held[0])[:60])
# planted control: one byte changed is not contained
p=open(glob.glob(f'{RU}/spark_secuura_2026-11-02_ks_1868_o79_a1_*_throw/out.md.checker/patch.diff')[0],'rb').read()
print('planted (one byte flipped) contained:', p.replace(b'unreadable thrown value', b'unreadable thrown valuE', 1) in open(glob.glob(f'{N}/READY_KS-1868-KS-1868-O79-A1_*')[0],'rb').read())
