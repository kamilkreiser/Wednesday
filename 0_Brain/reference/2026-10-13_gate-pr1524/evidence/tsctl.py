import hashlib, subprocess, re
S = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/f2077cbf-bb12-49ee-8d59-f5f537b335e0/scratchpad'
tree = S + '/repo2'; REL = 'Blockchain/Dev/services/governance'; FILE = 'src/__tests__/db.retry.test.ts'
path = tree + '/' + REL + '/' + FILE
orig = open(path, 'rb').read(); h0 = hashlib.sha256(orig).hexdigest()
new = orig.decode().replace("const DB_UP = ", "const TYPEERR: number = 'a';\nconst DB_UP = ", 1)
assert new != orig.decode()
open(path, 'wb').write(new.encode())
try:
    p = subprocess.run([tree + '/Blockchain/Dev/node_modules/.bin/jest', FILE], cwd=tree + '/' + REL, capture_output=True, text=True)
    print('jest rc', p.returncode, re.sub(r'\x1b\[[0-9;]*m', '', (p.stdout + p.stderr))[:500].replace('\n', ' | '))
    q = subprocess.run([tree + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', 'tsconfig.json'], cwd=tree + '/' + REL, capture_output=True, text=True)
    print('tsc -p rc (type error planted in excluded test file)', q.returncode, (q.stdout[:200]))
finally:
    open(path, 'wb').write(orig)
assert hashlib.sha256(open(path, 'rb').read()).hexdigest() == h0
print('restored')
