import hashlib, subprocess, sys, os
C = sys.argv[1]
D = C + '/Blockchain/Dev/services/nft-certificate'
VITEST = C + '/Blockchain/Dev/node_modules/.bin/vitest'
GATE = D + '/src/services/nftReadGate.ts'
ROUTE = D + '/src/routes/nft.routes.ts'
M = [
 ('m1 drop filter', ROUTE, "const certificates = selectReadableCertificates(fetched, ownerId, { walletAddress, userId: userIdSelector });", "const certificates = fetched;"),
 ('m2 owner from query userId', ROUTE, "const ownerId = readerIdentity((req as any).user);", "const ownerId = readerIdentity({ userId: req.query.userId ?? (req as any).user?.userId });"),
 ('m3 wallet branch skips filter', ROUTE, "const certificates = selectReadableCertificates(fetched, ownerId, { walletAddress, userId: userIdSelector });", "const certificates = typeof walletAddress === 'string' ? fetched : selectReadableCertificates(fetched, ownerId, { walletAddress, userId: userIdSelector });"),
 ('m4 widen: owner OR userId selector', GATE, "if (typeof cert.userId !== 'string' || cert.userId.trim() !== ownerId) return false;", "if (typeof cert.userId !== 'string' || (cert.userId.trim() !== ownerId && cert.userId !== selectors.userId)) return false;"),
 ('m5 drop sentinel conjunct', GATE, "if (trimmed.toLowerCase() === LEGACY_OWNER_SENTINEL) return null;", ""),
 ('m6 drop blank conjunct', GATE, "if (trimmed === '') return null;", ""),
 ('m9 403 on foreign selector', ROUTE, "    res.json({\n      success: true,", "    if (withheld > 0 && certificates.length === 0) { res.status(403).json({ success: false }); return; }\n    res.json({\n      success: true,"),
 ('m10 count of unfiltered', ROUTE, "count: certificates.length,", "count: fetched.length,"),
 ('m11 owner from tenantId', ROUTE, "const ownerId = readerIdentity((req as any).user);", "const ownerId = readerIdentity({ userId: (req as any).user?.tenantId });"),
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
