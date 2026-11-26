# QA-AUDIT-EMAIL-2: (i) lines naming the owner, (j) claim sentences in the lane's added lines. Usage: python3 -B qa2_sent.py <clone>
import sys, subprocess, re
C = sys.argv[1]; B, H = 'd4979df', '5aa56e1'
def git(*a): return subprocess.run(['git', '-C', C, *a], capture_output=True, text=True).stdout
KW = ['is masked', 'masked', 'is kept', 'kept', 'not caught', 'never', 'every', 'only', 'whole', 'unchanged', 'as before', 'neither', 'near', 'refused']
def added(path):
    out = []; ln = 0
    for l in git('diff', '-U0', B, H, '--', path).split('\n'):
        m = re.match(r'@@ -\d+(?:,\d+)? \+(\d+)', l)
        if m: ln = int(m.group(1)); continue
        if l.startswith('+') and not l.startswith('+++'): out.append((ln, l[1:])); ln += 1
    return out
src = {p: added(p) for p in ['docs/AUDIT.md', 'docs/M0-OUTCOMES.md', 'BACKLOG.md', 'crates/coagent-audit/src/redact.rs', 'crates/coagent-audit/build.rs',
                             'crates/coagent-audit/Cargo.toml', 'scripts/red-controls-audit.sh', 'crates/coagent-audit/tests/ae2_email.rs']}
msg = git('show', '-s', '--format=%B', H).split('\n')
print('=== (i) lines naming the owner (case-insensitive "owner"), added lines + commit message')
for p, ls in src.items():
    for n, l in ls:
        if 'owner' in l.lower(): print(f'  {p}:{n}: {l.strip()[:200]}')
for n, l in enumerate(msg, 1):
    if 'owner' in l.lower(): print(f'  commit:{n}: {l.strip()}')
print('=== (j) claim lines (keywords: ' + ', '.join(KW) + ')')
for p in ['docs/AUDIT.md', 'docs/M0-OUTCOMES.md', 'BACKLOG.md', 'crates/coagent-audit/src/redact.rs']:
    for n, l in src[p]:
        if p.endswith('redact.rs') and not (n in (7, 139, 250) or 696 <= n <= 760): continue
        if any(k in l.lower() for k in KW): print(f'  {p}:{n}: {l.strip()[:230]}')
for n, l in enumerate(msg, 1):
    if any(k in l.lower() for k in KW): print(f'  commit:{n}: {l.strip()}')
