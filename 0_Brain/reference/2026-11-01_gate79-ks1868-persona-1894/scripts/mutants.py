import hashlib, subprocess, sys, pathlib
W = pathlib.Path('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate79-ks1868-persona-1894')
P = W / 'repo/Blockchain/Dev/services/demo-service/src/routes/persona.ts'
HEAD_SHA = '5d5b25eec7e1cbe9da253dfd7100c963b7f858d6a39a9cdae1bcd8d25738dec8'
TEST = 'src/__tests__/ks1868-persona-switch-unreadable-throw.test.ts'
INNER = """    let message: string;
    try {
      message = err instanceof Error ? err.message : 'Unknown error';
    } catch {
      message = 'unreadable thrown value';
    }
"""
GEN = "res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });"
M = [
 ('M1', 'inner try removed (base read restored)', INNER, "    const message = err instanceof Error ? err.message : 'Unknown error';\n"),
 ('M2', "fallback constant -> 'Unknown error'", "message = 'unreadable thrown value';", "message = 'Unknown error';"),
 ('M3', 'catch ECHOES the thrown message in the 500 body', "message: 'Internal server error' }", "message }"),
 ('M4', 'inner catch rethrows', "message = 'unreadable thrown value';", "throw new Error('rethrow');"),
 ('M5', 'catch answers 200 instead of 500', GEN, GEN.replace('res.status(500)', 'res.status(200)')),
 ('M6', 'catch body success:true', GEN, GEN.replace('success: false', 'success: true')),
 ('M7', 'inner catch answers 500 without logging', "message = 'unreadable thrown value';", "return " + GEN),
 ('M8', 'log level error -> warn', "logger.error('Persona switch error'", "logger.warn('Persona switch error'"),
 ('M9', 'fallback = String(err)', "message = 'unreadable thrown value';", "message = String(err);"),
 ('M10', "non-Error branch 'Unknown error' -> 'unreadable thrown value'", "err.message : 'Unknown error'", "err.message : 'unreadable thrown value'"),
 ('M11', 'log carries the raw thrown value', "{ error: message }", "{ error: err }"),
 ('M12', 'catch leaks a session: body carries accessToken', "message: 'Internal server error' }", "message: 'Internal server error' }, accessToken: 'leak'"),
 ('M13', 'catch swallows: no response sent', "    return " + GEN + "\n  }\n});", "    return;\n  }\n});"),
]
def sha(): return hashlib.sha256(P.read_bytes()).hexdigest()
orig = P.read_text()
assert sha() == HEAD_SHA, 'start sha mismatch'
rows = []
for mid, desc, a, b in M:
    n = orig.count(a)
    if n != 1:
        rows.append((mid, desc, f'NOT APPLIED (anchor count {n})', '-')); continue
    P.write_text(orig.replace(a, b))
    log = W / f'logs/mut_{mid}.log'
    rc = subprocess.run([str(W / 'scripts/vt.sh'), str(log), TEST]).returncode
    txt = log.read_text()
    tl = [l.strip() for l in txt.splitlines() if l.strip().startswith('Tests ')]
    P.write_text(orig)
    ok = sha() == HEAD_SHA
    rows.append((mid, desc, ('KILLED' if rc != 0 else 'SURVIVED') + f' (rc={rc}; {tl[-1] if tl else "no Tests line"})', 'restored sha OK' if ok else 'RESTORE FAILED'))
    if not ok: break
print('| id | mutant | result | restore |'); print('|---|---|---|---|')
for r in rows: print('| ' + ' | '.join(r) + ' |')
print('final sha', sha(), 'OK' if sha() == HEAD_SHA else 'MISMATCH')
