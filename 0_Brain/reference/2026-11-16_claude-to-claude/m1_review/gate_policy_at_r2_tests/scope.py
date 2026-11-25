# QA-POLICY-AT-R2 task 6: scope of the round, by program. usage: python3 -B scope.py <repo>
import subprocess, sys, re
R = sys.argv[1]
def g(*a): return subprocess.run(['git', '-C', R] + list(a), capture_output=True, text=True, check=True).stdout
B, O, H = '184b35e', 'a8d910f', '85565bd'
SIX = ['BACKLOG.md', 'crates/coagent-policy/tests/owner_common/mod.rs', 'crates/coagent-policy/tests/t25_owner_allow.rs',
       'crates/coagent-policy/tests/t28_at_names.rs', 'docs/M0-OUTCOMES.md', 'docs/POLICY.md']
names = g('diff', '--name-only', O, H).split()
print('round paths:', names, '== the six:', sorted(names) == sorted(SIX))
print('control range 184b35e..head paths:', len(g('diff', '--name-only', B, H).split()))
print('bytes outside the six (round):', len(g('diff', O, H, '--', '.', *[f':!{p}' for p in SIX])), '; control (BACKLOG let back in):',
      len(g('diff', O, H, '--', '.', *[f':!{p}' for p in SIX if p != 'BACKLOG.md'])))
print('numstat:', g('diff', '--numstat', O, H).strip().replace('\n', ' | '))
tot = 0
for p in SIX:
    removed = [l[1:] for l in g('diff', '-U0', O, H, '--', p).splitlines() if l.startswith('-') and not l.startswith('---')]
    try: base_lines = set(g('show', f'{B}:{p}').splitlines())
    except subprocess.CalledProcessError: base_lines = set(); print(f'  ({p} does not exist at the base: the whole file is this lane\'s)')
    olines = g('show', f'{O}:{p}').splitlines()
    in_base = [l for l in removed if l in base_lines]
    # a removed line "this lane added": absent from the base file and present at a8d910f
    print(f'{p}: removed {len(removed)}, of them in the base file {len(in_base)}', [l[:60] for l in in_base] if in_base else '')
    tot += len(removed)
print('removed lines in all:', tot)
for p, n in [('BACKLOG.md', 1617), ('docs/M0-OUTCOMES.md', 228)]:
    b = g('show', f'{B}:{p}').splitlines(); h = g('show', f'{H}:{p}').splitlines()
    print(f'{p}: base {len(b)} lines, head {len(h)}; head[:{n}] == base[:{n}]: {h[:n] == b[:n]}; base has exactly {n} lines: {len(b) == n}; control head[:{n}] vs base[1:{n+1}]: {h[:n] == b[1:n+1]}')
t = g('show', f'{H}:crates/coagent-policy/tests/t28_at_names.rs'); to = g('show', f'{O}:crates/coagent-policy/tests/t28_at_names.rs')
def arr(src, name):
    m = re.search(r'const ' + name + r': \[&str; (\d+)\] = \[(.*?)\];', src, re.S)
    items = re.findall(r'"((?:[^"\\]|\\.)*)"', m.group(2)); return int(m.group(1)), items
for name in ['SHAPE_RIGHT', 'SHAPE_LEFT', 'SHAPE_CMDS', 'PREFIXES', 'CLIENTS', 'SUFFIXES']:
    (no, io), (nh, ih) = arr(to, name), arr(t, name)
    diff = [(i, a, b) for i, (a, b) in enumerate(zip(io, ih)) if a != b]
    print(f'{name}: declared {no}->{nh}, items {len(io)}->{len(ih)}, differing positions {diff}')
for c in ['PROP_SEED', 'PROP_CASES']:
    print(c, [l.strip() for l in t.splitlines() if l.startswith(f'const {c}')], '== a8d910f:', [l for l in t.splitlines() if l.startswith(f'const {c}')] == [l for l in to.splitlines() if l.startswith(f'const {c}')])
print('t28 hunks:'); print('\n'.join(l for l in g('diff', '-U0', O, H, '--', 'crates/coagent-policy/tests/t28_at_names.rs').splitlines() if l[:1] in '+-@' and not l.startswith(('+++', '---'))))
