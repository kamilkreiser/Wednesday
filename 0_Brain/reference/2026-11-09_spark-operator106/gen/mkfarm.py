import os,sys
D='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/deps/Blockchain/Dev'
SCR='/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/02f26010-3405-430b-9101-389a22dcbb3d/scratchpad/j2'
svc,out=sys.argv[1],sys.argv[2]
os.makedirs(out,exist_ok=False)
def link_all(src):
    if not os.path.isdir(src): return
    for n in os.listdir(src):
        if n=='@secuura': continue
        dst=os.path.join(out,n)
        if not os.path.lexists(dst): os.symlink(os.path.join(src,n),dst)
link_all(D+'/services/%s/node_modules'%svc)   # service-level first (wins)
link_all(D+'/node_modules')
sc=os.path.join(out,'@secuura'); os.makedirs(sc)
for n in os.listdir(D+'/node_modules/@secuura'):
    if n=='shared': continue
    os.symlink(os.path.realpath(D+'/node_modules/@secuura/'+n),os.path.join(sc,n))
os.symlink(SCR+'/shared_src/Blockchain/Dev/packages/shared',os.path.join(sc,'shared'))
print('farm',out,len(os.listdir(out)))
