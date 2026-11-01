import hashlib, subprocess, pathlib
W = pathlib.Path('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate80-ks1868-governance-1895')
R = W / 'wt_head'
FD = R / 'Projects Documents/fragments'
NAME = 'KS-1868-governance-reads-unreadable-thrown-value.html'
F = {'flow': FD / 'flow' / NAME, 'cheat': FD / 'cheat' / NAME}
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def check(tag):
    log = W / f'logs/frag_{tag}.log'
    r = subprocess.run(['nice', '-n', '10', 'node', str(R / 'Blockchain/Dev/scripts/docs-fragments.mjs'), 'check', '--root', str(R)], capture_output=True, text=True)
    log.write_text(r.stdout + r.stderr + f'\nrc={r.returncode}\n')
    last = [l for l in (r.stdout + r.stderr).splitlines() if l.strip()]
    return r.returncode, (last[-1] if last else '')
orig = {k: (p.read_text(), sha(p)) for k, p in F.items()}
for k, (_, s) in orig.items(): print(f'start sha {k} {s}')
rc, last = check('check_clean'); print(f'clean head: rc={rc} | {last}')
P = [
 ('P1_flow_unclosed_div', 'flow', lambda t: t + '<div class="note">\n'),
 ('P2_flow_literal_number', 'flow', lambda t: t.replace('<h2><!--n-->.', '<h2>9999.', 1)),
 ('P3_cheat_unclosed_div', 'cheat', lambda t: t + '<div class="note">\n'),
 ('P4_cheat_carries_n_token', 'cheat', lambda t: t.replace('<h2>', '<h2><!--n-->. ', 1)),
 ('P5_flow_two_entries', 'flow', lambda t: t + '<h2><!--n-->. second entry</h2>\n'),
]
for tag, k, fn in P:
    text, s = orig[k]
    new = fn(text); assert new != text, tag
    F[k].write_text(new)
    rc, last = check(tag)
    F[k].write_text(text)
    print(f'{tag}: rc={rc} | {last} | restore {"OK" if sha(F[k]) == s else "FAILED"}')
rc, last = check('check_after'); print(f'after restore: rc={rc} | {last}')
