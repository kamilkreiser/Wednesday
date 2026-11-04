"""Gate 188 mutants on the HEAD routes. Each: one exact-once text replacement, run the gate matrix + the seat's ks1561 file,
record which cells went RED, restore with `git checkout <head> -- file`, and assert the sha256 equals the pristine one."""
import hashlib, json, subprocess, sys, re

W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000'
R = W + '/repo'
HEAD = 'd03b03046d76591aec3e5a3aa4176fb4e5b78e04'
V1 = 'Blockchain/Dev/services/originate/src/routes/verification.ts'
V2 = 'Blockchain/Dev/services/originate/src/routes/verificationV2.ts'

MUTANTS = [
    ('M1-tie-rule-dropped (one original: the LAST tied row)', V1,
     "const originals = list.filter((r: any) => rowCreatedMs(r) === earliest);",
     "const originals = list.filter((r: any) => rowCreatedMs(r) === earliest).slice(-1);"),
    ('M2-same-owner-clause-dropped', V1,
     "return owner !== null && originalOwners.has(owner);",
     "return owner !== null && originalOwners.has(owner) && false;"),
    ('M3-MIN-inverted-to-MAX', V1,
     "const earliest = list.reduce((min: number, r: any) => Math.min(min, rowCreatedMs(r)), Number.MAX_SAFE_INTEGER);",
     "const earliest = list.reduce((min: number, r: any) => Math.max(min, rowCreatedMs(r)), 0);"),
    ('M4-identity-case-sensitive', V1,
     "const s = String(value).trim().toLowerCase();",
     "const s = String(value).trim();"),
    ('M5-same-org-clause-dropped', V1,
     "if (org !== null && originalOrgs.has(org)) return true;",
     "if (org !== null && originalOrgs.has(org) && false) return true;"),
    ('M6-sibling-evidence-gate-dropped', V1,
     "if (evidence && eligibility.evidenceRow(r)) return evidence;",
     "if (evidence) return evidence;"),
    ('M7-v2-presentable-filter-dropped', V2,
     "const sorted = sortRowsForPresentation(presentable);",
     "const sorted = sortRowsForPresentation(rows); void presentable;"),
    ('M8-selection-candidates-ungated', V1,
     "const candidates = rows.filter((r) => !isCertifiedStatus(r?.status) || eligibility.certifiedRow(r)); // KS-1561",
     "const candidates = rows.filter((r) => !isCertifiedStatus(r?.status) || eligibility.certifiedRow(r) || true); // KS-1561"),
]

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

pristine = {f: sha(f'{R}/{f}') for f in (V1, V2)}
rows = []
for name, f, old, new in MUTANTS:
    p = f'{R}/{f}'
    src = open(p).read()
    n = src.count(old)
    if n != 1:
        rows.append({'mutant': name, 'status': f'NOT APPLIED (matches={n})'}); continue
    open(p, 'w').write(src.replace(old, new))
    out = f'mut_{re.sub(r"[^A-Za-z0-9]+", "_", name)[:40]}'
    subprocess.run(['bash', W + '/runjest.sh', out, 'src/__tests__/(gate188|ks1561)', '--verbose'], capture_output=True, text=True)
    txt = open(f'{W}/runs/{out}.txt').read()
    failed_to_run = 'Test suite failed to run' in txt
    # Cells RED on the unmutated head (measured: N-TRUNC and N-SPLIT, the gate's findings) are not kills.
    red = [l.strip() for l in txt.splitlines() if '✕' in l and 'N-TRUNC:' not in l and 'N-SPLIT' not in l]
    subprocess.run(['git', '-C', R, 'checkout', HEAD, '--', f], check=True)
    restored = sha(p) == pristine[f]
    rows.append({'mutant': name, 'status': 'INVALID (suite failed to run)' if failed_to_run else ('KILLED' if red else 'SURVIVED'),
                 'red_cells': len(red), 'red': [r[:110] for r in red], 'restored_sha_ok': restored})
    if not restored:
        print('RESTORE FAILED', name); sys.exit(2)
json.dump(rows, open(W + '/runs/mutants.json', 'w'), indent=1)
for r in rows:
    print(r['mutant'], '|', r['status'], '|', r.get('red_cells'), '| restored', r.get('restored_sha_ok'))
    for c in r.get('red', [])[:6]:
        print('     ', c)
print('pristine', {k.split('/')[-1]: v[:16] for k, v in pristine.items()})
