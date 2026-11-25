# QA-POLICY-AT-R2: run each example through real bash (3.2, --noprofile --norc) and zsh (-f) in a scratch folder
# holding .env and src/.env; print the argv each client function receives. usage: python3 -B argv_run.py <dir> <defs>
import subprocess, sys, os
D, DEFS = sys.argv[1], sys.argv[2]
os.makedirs(os.path.join(D, 'src'), exist_ok=True)
for p, c in [('.env', 'TOKEN=fake-1\n'), ('src/.env', 'TOKEN=fake-2\n'), ('README.md', 'readme\n')]:
    open(os.path.join(D, p), 'w').write(c)
EX = [l.rstrip('\n') for l in open(os.path.join(os.path.dirname(DEFS), 'argv_examples.txt')) if l.strip() and not l.startswith('#')]
defs = open(DEFS).read()
for cmd in EX:
    print('=' * 8, cmd)
    for sh in (['/bin/bash', '--noprofile', '--norc', '-c'], ['/bin/zsh', '-f', '-c']):
        r = subprocess.run(sh + [defs + '\n' + cmd], cwd=D, capture_output=True, text=True, stdin=subprocess.DEVNULL)
        name = os.path.basename(sh[0])
        body = (r.stdout + r.stderr).rstrip().replace(D, '<dir>')
        print(f'-- {name} (exit {r.returncode})')
        print('\n'.join('   ' + l for l in body.splitlines()) if body else '   (no output)')
