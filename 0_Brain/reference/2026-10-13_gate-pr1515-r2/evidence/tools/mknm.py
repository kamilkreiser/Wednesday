import os,sys
M="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev"
T=sys.argv[1]+"/Blockchain/Dev"
def shell(src,dst):
    os.makedirs(dst,exist_ok=True)
    for e in os.listdir(src):
        s=os.path.join(src,e); d=os.path.join(dst,e)
        if os.path.lexists(d): continue
        if e=='@secuura':
            os.makedirs(d,exist_ok=True)
            for x in os.listdir(s):
                sx=os.path.join(s,x)
                if os.path.islink(sx) and not os.path.isabs(os.readlink(sx)):
                    os.symlink(os.readlink(sx),os.path.join(d,x))
                else:
                    os.symlink(os.path.realpath(sx),os.path.join(d,x))
        else:
            os.symlink(s,d)
for rel in ['node_modules','services/auth/node_modules','services/api-gateway/node_modules','packages/shared/node_modules','services/node_modules']:
    if os.path.isdir(os.path.join(M,rel)): shell(os.path.join(M,rel),os.path.join(T,rel))
print('ok',os.path.realpath(os.path.join(T,'node_modules/@secuura/shared')))
