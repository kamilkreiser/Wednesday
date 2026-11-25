# QA-POLICY-AT-R2 task 5: the docs phrases of t25::docs_name_the_owner_origin, by program. usage: python3 -B docs_phrases.py <repo>
import subprocess, sys, re
R = sys.argv[1]
def show(s, p): return subprocess.run(['git', '-C', R, 'show', f'{s}:{p}'], capture_output=True, text=True, check=True).stdout
def phrases(src):
    i = src.index('fn docs_name_the_owner_origin'); j = src.index('for phrase in [', i); k = src.index('\n    ] {', j)
    block = src[j + len('for phrase in ['):k]
    out = []
    for m in re.finditer(r'"((?:[^"\\]|\\.)*)"', '\n'.join(l for l in block.split('\n') if not l.strip().startswith('//'))):
        s = m.group(1)
        s = re.sub(r'\\(.)', lambda x: {'n': '\n', 't': '\t', '\\': '\\', '"': '"'}.get(x.group(1), '\\' + x.group(1)), s)
        out.append(s)
    return out
T = 'crates/coagent-policy/tests/t25_owner_allow.rs'
B, O, H = '184b35e', 'a8d910f', '85565bd'
pb, po, ph = phrases(show(B, T)), phrases(show(O, T)), phrases(show(H, T))
db, do, dh = show(B, 'docs/POLICY.md'), show(O, 'docs/POLICY.md'), show(H, 'docs/POLICY.md')
print(f'phrases: base {len(pb)}, a8d910f {len(po)}, head {len(ph)}')
print('older 22 at head byte-identical to base list:', ph[:22] == pb, '; found at head (count each):', [dh.count(p) for p in ph[:22]], '; at base:', [db.count(p) for p in pb])
lane = ph[22:]
print('lane phrases:', len(lane))
for idx, p in enumerate(lane):
    changed = p not in po
    print(f'  #{22+idx+1:2} head-count {dh.count(p)} base-count {db.count(p)} a8d910f-doc-count {do.count(p)} {"CHANGED-IN-ROUND" if changed else ""} :: {p[:90]!r}')
gone = [p for p in po[22:] if p not in ph]
print('a8d910f lane phrases not at head:', [(p[:90], 'head-doc-count', dh.count(p), 'a8d910f-doc-count', do.count(p)) for p in gone])
# control: a phrase that must not be found
print('control: a made-up phrase found', dh.count('at most 161 distinct words (the scan'), 'times at head;', do.count('at most 161 distinct words (the scan'), 'at a8d910f')
