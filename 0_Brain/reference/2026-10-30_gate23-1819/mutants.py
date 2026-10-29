import hashlib, subprocess, sys, os
C = sys.argv[1]
D = C + '/Blockchain/Dev/services/nft-certificate'
VITEST = C + '/Blockchain/Dev/node_modules/.bin/vitest'
GATE = D + '/src/services/nftReadGate.ts'
ROUTE = D + '/src/routes/nft.routes.ts'
M = [
 ('Ma drop foreign-selector log clause', ROUTE, "if (withheld > 0 || (userIdSelector !== undefined && userIdSelector !== ownerId)) {", "if (withheld > 0) {"),
 ('Mb log on every call', ROUTE, "if (withheld > 0 || (userIdSelector", "if (withheld >= 0 || (userIdSelector"),
 ('Mc no trim on row userId', GATE, "cert.userId.trim() !== ownerId", "cert.userId !== ownerId"),
 ('Md drop row non-string guard', GATE, "typeof cert.userId !== 'string' || cert.userId.trim()", "(cert.userId as any).trim()"),
 ('Me readerIdentity returns untrimmed id', GATE, "  return trimmed;\n}", "  return id;\n}"),
 ('Mf wallet selector compares trimmed', GATE, "cert.walletAddress !== selectors.walletAddress", "cert.walletAddress.trim() !== String(selectors.walletAddress).trim()"),
 ('Mg userId selector compared case-insensitively', GATE, "selectors.userId !== ownerId) return false", "String(selectors.userId).toLowerCase() !== ownerId.toLowerCase()) return false"),
 ('Mh wallet path when walletAddress truthy (any type)', ROUTE, "typeof walletAddress === 'string'\n", "walletAddress\n"),
 ('Mi sentinel check before trim only', GATE, "if (trimmed.toLowerCase() === LEGACY_OWNER_SENTINEL) return null;", "if (id.toLowerCase() === LEGACY_OWNER_SENTINEL) return null;"),
 ('Mj 403 body names the claimed id', ROUTE, "message: 'A verified caller identity is required' }", "message: 'A verified caller identity is required', claimed: (req as any).user?.userId }"),
]
TESTS = ['src/__tests__/ks1836-nft-list-owner-bound.test.ts', 'src/__tests__/ks1836-nft-read-gate.test.ts']
ATTACK = ['src/__tests__/zz-gate23-attack.test.ts']
def sha(p): return hashlib.sha256(open(p,'rb').read()).hexdigest()
def run(files):
    env = dict(os.environ, TMPDIR='/tmp/g23')
    r = subprocess.run([VITEST, 'run', '--root', D, *files], capture_output=True, text=True, env=env)
    out = r.stdout + r.stderr
    line = [l for l in out.splitlines() if 'Tests ' in l]
    return r.returncode, (line[-1].strip() if line else out[-300:])
for name, path, old, new in M:
    src = open(path).read(); h0 = sha(path)
    n = src.count(old)
    if n != 1: print(name, 'ANCHOR COUNT', n); continue
    open(path, 'w').write(src.replace(old, new))
    try:
        tsc = subprocess.run([C + '/Blockchain/Dev/node_modules/.bin/tsc', '--noEmit', '-p', D + '/tsconfig.json'], capture_output=True, text=True)
        parse = 'tsc ok' if tsc.returncode == 0 else 'tsc rc=%d %s' % (tsc.returncode, tsc.stdout.strip().splitlines()[0][:160] if tsc.stdout.strip() else '')
        a = run(TESTS); b = run(ATTACK)
        print(f"{name} | {parse} | author: {'KILLED' if a[0] else 'SURVIVED'} ({a[1]}) | gate23 attack: {'KILLED' if b[0] else 'SURVIVED'} ({b[1]})", flush=True)
    finally:
        open(path, 'w').write(src)
        assert sha(path) == h0, 'restore failed ' + path
        assert open(path).read().count(old) == 1
print('restored, git status:')
print(subprocess.run(['git', '-C', C, 'status', '--short'], capture_output=True, text=True).stdout)
