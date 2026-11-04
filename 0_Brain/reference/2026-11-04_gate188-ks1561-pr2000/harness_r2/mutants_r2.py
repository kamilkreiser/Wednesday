"""Gate 188 round 2 mutants on the COMMITTED round-2 bytes (f702d4da4b69) in my clone.
Each: an exact-count text replacement (count asserted), then (1) the seat's new 30-cell mock file and (2) my PG15 harness
with EXPECT=r2; RED cells counted from each runner's own output; restored by `git checkout <head> -- file`, sha256 asserted."""
import hashlib, json, re, subprocess, sys

W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000'
R = W + '/repo'
HEAD = 'f702d4da4b69478e82d3d79ea4e8746fae47f2eb'
V1 = 'Blockchain/Dev/services/originate/src/routes/verification.ts'
V2 = 'Blockchain/Dev/services/originate/src/routes/verificationV2.ts'

MUTANTS = [
    ('M1-trigger-off', V1, 1,
     "return Array.isArray(rows) && rows.length >= VERIFY_ROWSET_LIMIT;",
     "return Array.isArray(rows) && rows.length >= VERIFY_ROWSET_LIMIT * 1000;"),
    ('M3-threshold-25', V1, 1,
     "return Array.isArray(rows) && rows.length >= VERIFY_ROWSET_LIMIT;",
     "return Array.isArray(rows) && rows.length >= VERIFY_ROWSET_LIMIT + 1;"),
    ('M5-tie-bound-1', V1, 1,
     "export const ORIGINAL_ROWS_LIMIT = VERIFY_ROWSET_LIMIT;",
     "export const ORIGINAL_ROWS_LIMIT = 1;"),
    ('M6-MIN-to-MAX-all-three-reads', V1, 3,
     "(SELECT MIN(e.created_at) FROM documents e",
     "(SELECT MAX(e.created_at) FROM documents e"),
    ('M11-tenant-rank-back-to-tenant_id', V2, 1,
     "ORDER BY MIN(created_at) ASC, tenant_id",
     "ORDER BY tenant_id"),
    ('G1-id-dedupe-dropped', V1, 1,
     "return id !== null && !have.has(id);",
     "return id !== null && (have.size >= 0);"),
    ('G2-tie-cut-dropped', V1, 1,
     "tied = tied.slice(0, ORIGINAL_ROWS_LIMIT);",
     "tied = tied.slice(0);"),
    ('G3-crossTenantLookup-not-wired', V1, 1,
     "if (rowSetMayBeCut(docRows.rows)) {",
     "if (rowSetMayBeCut(docRows.rows) && docRows.rows.length < 0) {"),
    ('G4-merged-originals-put-first', V1, 1,
     "return missing.length > 0 ? [...list, ...missing] : list;",
     "return missing.length > 0 ? [...missing, ...list] : list;"),
]

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True).stdout

def red_cells(txt_path):
    reds = []
    for line in open(txt_path, errors='replace'):
        m = re.match(r'^\s+✕ (.*?)(?: \(\d+ ms\))?$', line.rstrip())
        if m: reds.append(m.group(1))
    tests = [l.strip() for l in open(txt_path, errors='replace') if l.startswith('Tests:')]
    return reds, (tests[0] if tests else 'NO TESTS LINE')

pristine = {f: sha(f'{R}/{f}') for f in (V1, V2)}
rows = []
only = sys.argv[1:]  # optional subset
for name, f, cnt, old, new in MUTANTS:
    if only and name not in only: continue
    p = f'{R}/{f}'
    src = open(p).read()
    n = src.count(old)
    if n != cnt:
        rows.append({'mutant': name, 'status': f'NOT APPLIED (matches={n}, want {cnt})'}); continue
    open(p, 'w').write(src.replace(old, new))
    tag = re.sub(r'[^A-Za-z0-9]+', '_', name)
    run(['bash', f'{W}/harness_r2/run_mock.sh', 'cur', f'mut_{tag}_mock', 'ks1561-g188-f1', '--verbose'])
    run(['bash', f'{W}/harness_r2/run_pg.sh', 'cur', f'mut_{tag}_pg', 'r2'])
    subprocess.run(['git', '-C', R, 'checkout', '-q', HEAD, '--', f])
    restored = sha(p) == pristine[f]
    mr, mt = red_cells(f'{W}/runs_r2/mut_{tag}_mock.txt')
    pr, pt = red_cells(f'{W}/runs_r2/mut_{tag}_pg.txt')
    ts_err = sum(1 for l in open(f'{W}/runs_r2/mut_{tag}_mock.txt', errors='replace') if re.search(r'error TS\d+', l))
    rows.append({'mutant': name, 'file': f.split('/')[-1], 'anchors': n, 'mock': mt, 'mock_red': len(mr), 'pg': pt, 'pg_red': len(pr),
                 'ts_errors': ts_err, 'killed': (len(mr) + len(pr)) > 0 and ts_err == 0, 'restored_sha_equal': restored,
                 'mock_red_cells': mr, 'pg_red_cells': pr})
    if not restored:
        print('RESTORE FAILED', name); break
json.dump(rows, open(f'{W}/runs_r2/mutants_r2.json', 'w'), indent=1, ensure_ascii=False)
for r in rows:
    print(r['mutant'], '|', r.get('status') or f"mock {r['mock_red']} red ({r['mock']}) | pg {r['pg_red']} red ({r['pg']}) | ts_err {r['ts_errors']} | killed {r['killed']} | restored {r['restored_sha_equal']}")
