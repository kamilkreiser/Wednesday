#!/usr/bin/env python3
# Mutants at each changed site, product code only (never the tests), in wt2_mut (a head worktree of MY clone).
# Each mutant: write, run the PR's two new test files, classify, restore the original bytes, sha-verify.
import hashlib, subprocess, sys, re, json, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate159-ks1868-pr1976'
A = W + '/wt2_mut/Blockchain/Dev/services/anchoring'
REC = A + '/src/reconciler.ts'
IDX = A + '/src/cardano/threadTokenIndex.ts'
TESTS = ['src/__tests__/ks1868-reconciler-catches-unreadable-throw.test.ts',
         'src/__tests__/ks1868-thread-token-index-load-registry-catch-unreadable-throw.test.ts']

GUARD = """try {
            const m = err?.message;
            reason = m === undefined || m === null ? m : String(m);
          } catch {
            reason = 'unreadable thrown value';
          }"""

def guard_at(indent):
    pad = ' ' * indent
    return (f"try {{\n{pad}  const m = err?.message;\n{pad}  reason = m === undefined || m === null ? m : String(m);\n"
            f"{pad}}} catch {{\n{pad}  reason = 'unreadable thrown value';\n{pad}}}")

def variants(indent):
    pad = ' ' * indent
    g = guard_at(indent)
    return {
        'M1_no_inner_try': (g, f"const m = err?.message;\n{pad}reason = m === undefined || m === null ? m : String(m);"),
        'M2_always_constant': (g, f"reason = 'unreadable thrown value';"),
        'M3_no_String': (g, g.replace('? m : String(m);', '? m : m;')),
        'M4_inner_rethrows': (g, g.replace("reason = 'unreadable thrown value';", "throw new Error('rethrown');")),
        'M5_other_constant': (g, g.replace("'unreadable thrown value'", "'unknown error'")),
    }

SITES = {
    # (file, guard indent, occurrence index of the guard in that file, the log line that follows, M0 revert, M6 site mutation)
    'rec_row': (REC, 10, 0,
                "deps.log('warn', 'Reconciler: chain check errored; leaving row as-is', { anchorId: row.id, error: reason });",
                "deps.log('warn', 'Reconciler: chain check errored; leaving row as-is', { anchorId: row.id, error: err?.message });",
                # M6: abandon the rest of the rows after a failing row (the base outcome for an unreadable value)
                ("deps.log('warn', 'Reconciler: chain check errored; leaving row as-is', { anchorId: row.id, error: reason });",
                 "deps.log('warn', 'Reconciler: chain check errored; leaving row as-is', { anchorId: row.id, error: reason });\n          break;")),
    'rec_pass': (REC, 6, 0,
                 "deps.log('warn', 'Reconciler pass failed', { error: reason });",
                 "deps.log('warn', 'Reconciler pass failed', { error: err?.message });",
                 # M6: no log line on a failed pass
                 ("deps.log('warn', 'Reconciler pass failed', { error: reason });", "void reason;")),
    'idx': (IDX, 4, 0,
            None, None,
            # M6: non-strict fails CLOSED (rethrow instead of the empty registry)
            ("    return [];\n  }\n}", "    throw err;\n  }\n}")),
}

def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def run(tag):
    log = f'{W}/logs/mutant_{tag}.log'
    cmd = f'cd "{A}" && "{W}/wt2_mut/Blockchain/Dev/node_modules/.bin/vitest" run --root "{A}" --reporter=verbose --testTimeout=60000 ' + ' '.join(TESTS)
    p = subprocess.run(['bash', '-c', cmd], capture_output=True, text=True)
    out = p.stdout + p.stderr
    open(log, 'w').write(out + f'\nrc={p.returncode}\n')
    m = re.search(r'Tests\s+(.*)', out)
    assertion = out.count('AssertionError')
    timeout = len(re.findall(r'Test timed out', out))
    return p.returncode, (m.group(1).strip() if m else '?'), assertion, timeout

def nth_replace(s, old, new, n):
    idx = -1
    for _ in range(n + 1):
        idx = s.find(old, idx + 1)
        if idx < 0:
            raise SystemExit(f'occurrence {n} of pattern not found')
    return s[:idx] + new + s[idx + len(old):]

rows = []
orig = {REC: open(REC).read(), IDX: open(IDX).read()}
osha = {REC: sha(REC), IDX: sha(IDX)}
rc0, t0, a0, to0 = run('M_none_control')
rows.append(('control', 'unmutated', rc0, t0, a0, to0, 'n/a'))
for site, (f, indent, occ, logline, revert, m6) in SITES.items():
    src = orig[f]
    ms = {}
    g = guard_at(indent)
    for name, (old, new) in variants(indent).items():
        ms[name] = nth_replace(src, old, new, occ)
    if site == 'idx':
        # M0: the base catch (unguarded read in both branches)
        m0 = src.replace(g + '\n', '', 1)
        m0 = m0.replace("    let reason: string | null | undefined;\n", '', 1).replace('error: reason,', 'error: err?.message,')
        ms['M0_revert_unguarded'] = m0
        # M7: strict rethrows a NEW error instead of the original value
        ms['M7_strict_rethrow_other'] = src.replace('      throw err;', "      throw new Error(String(reason));", 1)
    else:
        ms['M0_revert_unguarded'] = src.replace(logline, revert, 1)
    ms['M6_site'] = src.replace(m6[0], m6[1], 1)
    for name, text in sorted(ms.items()):
        if text == src:
            rows.append((site, name, 'NOT-APPLIED', '', 0, 0, ''))
            continue
        open(f, 'w').write(text)
        rc, t, a, to = run(f'{site}_{name}')
        open(f, 'w').write(orig[f])
        ok = sha(f) == osha[f]
        rows.append((site, name, rc, t, a, to, 'restore-ok' if ok else 'RESTORE-FAILED'))
        if not ok:
            raise SystemExit('restore failed')
with open(f'{W}/logs/mutants_table.log', 'w') as fh:
    for r in rows:
        line = ' | '.join(str(x) for x in r)
        print(line); fh.write(line + '\n')
