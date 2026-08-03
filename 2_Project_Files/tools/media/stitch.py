import re, sys, json, glob, os
D="/Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/reference/tac-course/transcripts"
def parse(text):
    out={}
    for m in re.finditer(r"\[(\d+):(\d+)\] ([^\n]*)", text):
        t=int(m.group(1))*60+int(m.group(2))
        out.setdefault(t, m.group(3).strip())
    return out
def merge_into(dest_name, texts):
    cues={}
    for t in texts: cues.update(parse(t))
    keys=sorted(cues)
    lines=[f"[{k//60:02d}:{k%60:02d}] {cues[k]}" for k in keys]
    p=os.path.join(D, dest_name)
    open(p,"w").write("\n".join(lines)+"\n")
    return p, len(keys), keys[0] if keys else 0, keys[-1] if keys else 0
if __name__=="__main__":
    dest=sys.argv[1]
    texts=[open(f).read() for f in sys.argv[2:]]
    existing=os.path.join(D,dest)
    if os.path.exists(existing): texts.insert(0, open(existing).read())
    print(merge_into(dest, texts))
