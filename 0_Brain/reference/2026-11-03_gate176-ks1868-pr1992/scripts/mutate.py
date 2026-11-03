#!/usr/bin/env python3
"""Gate 176 mutants on the changed catch lines of PR 1992 (head blobs in the clone).
Each mutant edits ONE occurrence in ONE head file, runs (a) the PR's own test file for that module and (b) every existing
test file that imports the module (ssrf-guard only: 7 more), records killed/survived per set, restores the head blob.
Raw table -> results/mutants.tsv."""
import subprocess, os
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate176-ks1868-pr1992'
PS = W + '/repo/Blockchain/Dev/packages/shared'
VT = W + '/repo/Blockchain/Dev/node_modules/.bin/vitest'
ENV = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin', 'HOME': W + '/home', 'TMPDIR': W + '/tmp', 'NODE_ENV': 'test'}
T = 'src/__tests__/'
SSRF_OTHER = [T + f for f in ['ks1179-dns-timer-cleared.test.ts', 'ks1179-safeoutboundrequest-tests-no-cell-pins-dns.test.ts',
    'ks914-shipped-path.test.ts', 'ks914-pinned-address.test.ts', 'ks932-timeout-bounds-dns.test.ts', 'ssrf-guard.test.ts']]
G = "    } catch {\n      reason = 'unreadable thrown value';\n    }"
G_SM = "        } catch {\n          reason = 'unreadable thrown value';\n        }"
G_EI = "    } catch {\n      error = new Error('unreadable thrown value');\n    }"
SITES = [
  ('src/security/ssrf-guard.ts', [T + 'ks1868-ssrf-guard-resolve-public-addresses-catch-unreadable-throw.test.ts',
                                  T + 'ks1868-ssrf-guard-safe-outbound-request-catch-unreadable-throw.test.ts'], SSRF_OTHER, [
    ('G1 inner-catch-rethrows (dns catch, #1)', G, "    } catch (g176m) {\n      throw g176m;\n    }", 0),
    ('G1 inner-catch-rethrows (request catch, #2)', "      } catch {\n        reason = 'unreadable thrown value';\n      }", "      } catch (g176m) {\n        throw g176m;\n      }", 0),
    ('G2 constant changed (dns, #1)', "'unreadable thrown value'", "'g176 mutated'", 0),
    ('G2 constant changed (request, #2)', "'unreadable thrown value'", "'g176 mutated'", 1),
    ('G3 dns use-line reads raw .message', 'could not be resolved (${reason})', 'could not be resolved (${(err as Error).message})', 0),
    ('G3 request use-line reads raw .message', "reason: 'request_failed', error: reason }", "reason: 'request_failed', error: (err as Error).message }", 0),
    ('G4 dns catch fails OPEN (ok:true, no addresses)', "    return {\n      ok: false,\n      error: `host \"${bare}\" could not be resolved", "    return {\n      ok: true, addresses: ['203.0.113.7'],\n      error: `host \"${bare}\" could not be resolved", 0),
    ('G5 request catch tag blocked', "reason: 'request_failed', error: reason }", "reason: 'blocked', error: reason }", 0),
    ('G6 request catch drops return', "error: reason });\n      return;\n", "error: reason });\n", 0),
  ]),
  ('src/security/secrets-manager.ts', [T + 'ks1868-secrets-manager-vault-read-catch-unreadable-throw.test.ts'], [], [
    ('G1 inner-catch-rethrows', G_SM, "        } catch (g176m) {\n          throw g176m;\n        }", 0),
    ('G2 constant changed', "'unreadable thrown value'", "'g176 mutated'", 0),
    ('G3 use-line reads raw', "{ key, error: reason }", "{ key, error: error instanceof Error ? error.message : String(error) }", 0),
    ('G4 catch returns null (no env fallback)', "logger.warn('Vault read failed', { key, error: reason });", "logger.warn('Vault read failed', { key, error: reason }); return null;", 0),
  ]),
  ('src/blockchain/event-indexer.ts', [T + 'ks1868-event-indexer-handle-error-unreadable-throw.test.ts'], [], [
    ('G1 inner-catch-rethrows', G_EI, "    } catch (g176m) {\n      throw g176m;\n    }", 0),
    ('G2 constant changed', "'unreadable thrown value'", "'g176 mutated'", 0),
    ('G3 fallback re-reads the value', "error = new Error('unreadable thrown value');", "error = new Error(String(err));", 0),
    ('G4 catch swallows without onError', "      error = new Error('unreadable thrown value');\n    }", "      return;\n    }", 0),
  ]),
]
def nth(s, a, k):
    i = -1
    for _ in range(k + 1):
        i = s.find(a, i + 1)
        if i == -1: return -1
    return i
def run(tests):
    if not tests: return None
    r = subprocess.run([VT, 'run', '--root', PS] + tests, env=ENV, capture_output=True, text=True, timeout=600)
    return r.returncode
rows = []
for rel, own, other, muts in SITES:
    path = PS + '/' + rel
    orig = open(path).read()
    c_own, c_oth = run(own), run(other)
    print('CONTROL unmutated', rel, 'own rc', c_own, 'other rc', c_oth, flush=True)
    assert c_own == 0
    for name, a, b, k in muts:
        i = nth(orig, a, k)
        assert i != -1, (rel, name)
        m = orig[:i] + b + orig[i + len(a):]
        open(path, 'w').write(m)
        try:
            r1, r2 = run(own), run(other)
        finally:
            open(path, 'w').write(orig)
        res = lambda rc: '-' if rc is None else ('KILLED' if rc != 0 else 'SURVIVED')
        rows.append((rel, name, res(r1), res(r2)))
        print(*rows[-1], sep='\t', flush=True)
with open(W + '/results/mutants.tsv', 'w') as f:
    f.write('file\tmutant\tPR tests\tother module tests\n')
    for r in rows: f.write('\t'.join(r) + '\n')
k1 = sum(r[2] == 'KILLED' for r in rows)
print('total', len(rows), 'killed by PR tests', k1, 'survived PR tests', len(rows) - k1,
      'killed by either', sum('KILLED' in (r[2], r[3]) for r in rows))
