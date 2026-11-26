# property (j): every sentence of the lane's added lines (docs, BACKLOG, emails doc comment, commit msg) holding a claim word
import re, subprocess, sys
R = sys.argv[1]; KW = ['keeps', 'is masked', 'masked', 'is kept', 'kept', 'not caught', 'never', 'every', 'only', 'whole', 'unchanged', 'as before', 'neither']
def added(path):
    d = subprocess.run(['git', '-C', R, 'diff', '-U0', '5e11609', 'e31b29a', '--', path], capture_output=True, text=True).stdout
    out = []; ln = 0
    for l in d.split('\n'):
        m = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)', l)
        if m: ln = int(m.group(1)); continue
        if l.startswith('+') and not l.startswith('+++'): out.append((ln, l[1:])); ln += 1
    return out
src = {}
for p in ['docs/AUDIT.md', 'docs/M0-OUTCOMES.md', 'BACKLOG.md']: src[p] = added(p)
head = subprocess.run(['git', '-C', R, 'show', 'e31b29a:crates/coagent-audit/src/redact.rs'], capture_output=True, text=True).stdout.split('\n')
src['redact.rs doc comment'] = [(i + 1, re.sub(r'^\s*///\s?', '', head[i])) for i in range(695, 741)]
msg = subprocess.run(['git', '-C', R, 'log', '-1', '--format=%B', 'e31b29a'], capture_output=True, text=True).stdout.split('\n')
src['commit message'] = [(i + 1, l) for i, l in enumerate(msg) if not l.startswith('Co-Authored')]
n = 0
for p, lines in src.items():
    # join to text keeping line starts, split into sentences
    text = ''; starts = []
    for ln, l in lines: starts.append((len(text), ln)); text += l.strip() + ' '
    pos = 0
    for piece in re.split(r'(?<=[.;])\s+', text):
        st = text.find(piece, pos); pos = st + len(piece)
        class M: pass
        m = M(); m.start = (lambda st=st: st)
        s = piece.strip()
        if not s: continue
        hit = [k for k in KW if re.search(r'\b' + re.escape(k) + r'\b', s, re.I)]
        if hit:
            ln = max(l for o, l in starts if o <= m.start()); n += 1
            print(f'{n:3} {p}:{ln} [{", ".join(hit)}] {s[:300]}')
