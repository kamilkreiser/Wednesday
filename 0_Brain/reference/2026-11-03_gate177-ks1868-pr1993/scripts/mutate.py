#!/usr/bin/env python3
"""Gate 177 mutants on the changed catch lines of PR 1993 (head blobs in the clone).
Each mutant edits ONE occurrence in ONE head file, runs (a) the PR's own test file for that module and (b) the gate's
oracle (harness/oracle_*.test.ts, filtered to that module), records KILLED/SURVIVED per set, restores the head blob.
No other existing test in the sparse clone imports these 4 modules (grep in results/mutants_note.txt). Raw table -> results/mutants.tsv."""
import subprocess, shutil, sys
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate177-ks1868-pr1993'
PS = W + '/repo/Blockchain/Dev/packages/shared'
AG = W + '/repo/Blockchain/Dev/services/api-gateway'
VS = W + '/repo/Blockchain/Dev/node_modules/.bin/vitest'
VA = AG + '/node_modules/.bin/vitest'
ENV = {'PATH': '/opt/homebrew/bin:/usr/bin:/bin', 'HOME': W + '/home', 'TMPDIR': W + '/tmp', 'NODE_ENV': 'test'}
for d in (PS + '/src/__gate177__', AG + '/src/__gate177__'):
    subprocess.run(['mkdir', '-p', d], check=True)
shutil.copy(W + '/harness/values.ts', PS + '/src/__gate177__/'); shutil.copy(W + '/harness/oracle_shared.test.ts', PS + '/src/__gate177__/')
shutil.copy(W + '/harness/values.ts', AG + '/src/__gate177__/'); shutil.copy(W + '/harness/oracle_agw.test.ts', AG + '/src/__gate177__/')
T = 'src/__tests__/'
ORS = 'src/__gate177__/oracle_shared.test.ts'
SITES = [
  (PS, VS, 'src/vc/verifier.ts', T + 'ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts', (ORS, 'oracle verify'), [
    ('V1 inner catch rethrows', "      } catch {\n        msg = 'unreadable thrown value';\n      }", "      } catch (g177m) {\n        throw g177m;\n      }"),
    ('V2 constant changed', "'unreadable thrown value'", "'g177 mutated'"),
    ('V3 use-line reads the raw value', "errors.push(`Signature verification error: ${msg}`);", "errors.push(`Signature verification error: ${err instanceof Error ? err.message : String(err)}`);"),
    ('V4 unreadable branch FAILS OPEN (valid:true)', "        msg = 'unreadable thrown value';\n      }", "        return { valid: true, errors: [] };\n      }"),
    ('V5 outer catch records no error (fails open for every class)', "      errors.push(`Signature verification error: ${msg}`);\n    }", "      void msg;\n    }"),
  ]),
  (PS, VS, 'src/prism/identus-client.ts', T + 'ks1868-identus-client-resolve-did-catch-unreadable-throw.test.ts', (ORS, 'oracle resolveDID'), [
    ('I1 inner catch rethrows', "      } catch {\n        errorMessage = 'unreadable thrown value';\n      }", "      } catch (g177m) {\n        throw g177m;\n      }"),
    ('I2 constant changed', "'unreadable thrown value'", "'g177 mutated'"),
    ('I3 use-line reads the raw value', "          errorMessage,\n", "          errorMessage: err instanceof Error ? err.message : String(err),\n"),
    ('I4 unreadable branch answers a NON-NULL didDocument', "        errorMessage = 'unreadable thrown value';", "        return { didDocument: {} as any, didResolutionMetadata: {}, didDocumentMetadata: {} };"),
  ]),
  (PS, VS, 'src/resilience/service-client.ts', T + 'ks1868-service-client-health-check-catch-unreadable-throw.test.ts', (ORS, 'oracle healthCheck'), [
    ('S1 inner catch rethrows', "      } catch {\n        reason = 'unreadable thrown value';\n      }", "      } catch (g177m) {\n        throw g177m;\n      }"),
    ('S2 constant changed', "'unreadable thrown value'", "'g177 mutated'"),
    ('S3 use-line reads the raw value', "        error: reason,\n", "        error: error instanceof Error ? error.message : 'Unknown error',\n"),
    ('S4 unreadable branch reports HEALTHY', "        reason = 'unreadable thrown value';", "        return { healthy: true, latencyMs: 0 };"),
  ]),
  (AG, VA, 'src/routes/health-dashboard.ts', T + 'ks1868-health-dashboard-check-service-catch-unreadable-throw.test.ts', ('src/__gate177__/oracle_agw.test.ts', 'oracle dashboard'), [
    ('H1 probe catch rethrows', "    } catch {\n      readable = false;\n    }", "    } catch (g177m) {\n      throw g177m;\n    }"),
    ('H2 constant changed', "'unreadable thrown value'", "'g177 mutated'"),
    ('H3 both probe reads removed (readable stays true)', "      void (error instanceof Error && error.message);\n      void (error instanceof DOMException && error.name);\n", ""),
    ('H4 message probe removed', "      void (error instanceof Error && error.message);\n", ""),
    ('H5 DOMException name probe removed', "      void (error instanceof DOMException && error.name);\n", ""),
    ('H6 unreadable branch reports the service UP', "      errorMessage = 'unreadable thrown value';\n    } else if", "      return [key, { status: 'up', latencyMs, url: config.url }];\n    } else if"),
  ]),
]
def run(root, vt, test, name=None):
    a = [vt, 'run', '--root', root, test] + (['-t', name] if name else [])
    if root == PS and 'gate177' in test: a += ['--config', PS + '/vitest.gate177.shared.config.ts']
    if root == AG and 'gate177' in test: a += ['--config', AG + '/vitest.gate177.agw.config.ts']
    r = subprocess.run(a, env=ENV, capture_output=True, text=True, timeout=600)
    return r.returncode
rows = []
for root, vt, rel, own, (otest, oname), muts in SITES:
    path = root + '/' + rel
    orig = open(path).read()
    c1, c2 = run(root, vt, own), run(root, vt, otest, oname)
    print('CONTROL unmutated', rel, 'PR test rc', c1, 'oracle rc', c2, flush=True)
    assert c1 == 0 and c2 == 0
    for name, a, b in muts:
        assert orig.count(a) >= 1, (rel, name)
        m = orig.replace(a, b, 1)
        assert m != orig
        open(path, 'w').write(m)
        try:
            r1, r2 = run(root, vt, own), run(root, vt, otest, oname)
        finally:
            open(path, 'w').write(orig)
        res = lambda rc: 'KILLED' if rc != 0 else 'SURVIVED'
        rows.append((rel, name, res(r1), res(r2)))
        print(*rows[-1], sep='\t', flush=True)
with open(W + '/results/mutants.tsv', 'w') as f:
    f.write('file\tmutant\tPR tests\tgate oracle\n')
    for r in rows: f.write('\t'.join(r) + '\n')
print('total', len(rows), 'killed by PR tests', sum(r[2] == 'KILLED' for r in rows), 'killed by oracle', sum(r[3] == 'KILLED' for r in rows),
      'killed by either', sum('KILLED' in (r[2], r[3]) for r in rows))
