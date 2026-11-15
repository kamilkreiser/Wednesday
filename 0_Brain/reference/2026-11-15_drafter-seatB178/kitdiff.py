import hashlib,os,re
B="/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-15_seatB-177th"
man={}
for l in open(B+"/evidence/tools_sha256_after_rekey.txt",encoding="utf-8"):
    p=l.rstrip("\n").split(None,1)
    if len(p)==2: man[os.path.basename(p[1].strip().lstrip("*"))]=p[0]
cur={}
for n in sorted(os.listdir(B+"/tools")):
    fp=B+"/tools/"+n
    if os.path.isfile(fp): cur[n]=hashlib.sha256(open(fp,"rb").read()).hexdigest()
print("manifest entries",len(man),"tools regular files",len(cur))
print("not in manifest:",sorted(set(cur)-set(man)))
print("in manifest not on disk:",sorted(set(man)-set(cur)))
print("changed since v3:",sorted(n for n in cur if n in man and cur[n]!=man[n]))
print("positive control: manifest self-compare changed =",len([n for n in man if man[n]!=man[n]]))
