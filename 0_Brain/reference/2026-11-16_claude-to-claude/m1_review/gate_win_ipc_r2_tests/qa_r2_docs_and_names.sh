#!/bin/bash
# QA-WIN-IPC-R2: docs word-for-word check (first-run items 15-20, name-rule sentence) and names scan.
# Usage: bash qa_r2_docs_and_names.sh <clone> <first verdict path> <scratch dir>
set -u
C="$1"; V="$2"; S="$3"; mkdir -p "$S"
git -C "$C" show 329fb5f:crates/coagent-ipc/README.md > "$S/readme.md"
python3 -I - "$V" "$S/readme.md" <<'PY'
import sys,re
v=open(sys.argv[1],encoding='utf-8').read(); r=open(sys.argv[2],encoding='utf-8').read()
items={}
for l in v.splitlines():
    m=re.match(r'\s*- "(1[5-9]|20)\. (.*)"$', l)
    if m: items[m.group(1)]=m.group(1)+'. '+m.group(2)
rl=r.splitlines()
for k in sorted(items):
    hit=[l for l in rl if l.startswith(k+'. ')]
    print(k, 'EQUAL' if hit and hit[0]==items[k] else 'DIFF', len(hit))
alt=items['17'].replace('tight','fast'); print('control altered item 17 equal?', alt==[l for l in rl if l.startswith('17. ')][0])
norm=lambda s:' '.join(s.split())
sent="the name decodes back exactly to the folder text after ASCII case folding, slash folding and dropping one trailing separator, so two folder texts share a name only when they are equal after those three steps."
print('name sentence in verdict:', sent in norm(v), '/ in README:', sent in norm(r))
print('old sentence still in README:', 'so two different folder texts never share a name' in norm(r))
for n in ('21. ','22. '): print(n, any(l.startswith(n) for l in rl))
PY
git -C "$C" log -p --no-merges --format= e5e8633..329fb5f --not 16e83fb | grep '^+' | grep -v '^+++' > "$S/added.txt"
RX='/Users/|/Volumes/|/home/|kamil|kreiser|Secuura|Datasec'
echo "added lines: $(wc -l < "$S/added.txt") hits: $(grep -c -i -E "$RX" "$S/added.txt")"
cp "$S/added.txt" "$S/added_ctl.txt"; echo '+// planted control: /Users/somebody/x' >> "$S/added_ctl.txt"
echo "control hits: $(grep -c -i -E "$RX" "$S/added_ctl.txt")"
