"""Gate 172 mutants. Reads the head blobs from argv dir, writes mut/<id>/<file> + mut/index.json. Each edit must apply exactly once."""
import json, os, sys
SRC, OUT = sys.argv[1], sys.argv[2]
files = {k: open(os.path.join(SRC, k.replace('/', '__'))).read() for k in ['src/routes/auth.ts', 'src/services/password.ts', 'vitest.setup.ts']}
REG = "    if (await isPasswordBreached(data.password)) {\n      throw new ValidationError(BREACHED_PASSWORD_MESSAGE, weakPasswordIssues([BREACHED_PASSWORD_MESSAGE], 'password'));\n    }\n"
STRENGTH_REG = "    // Password strength check\n    const strength = checkPasswordStrength(data.password);"
RESET_STRENGTH = "    const tokenHash = createHash('sha256').update(data.token).digest('hex');\n    const stored = await userRepo.getResetToken(tokenHash);"
WRITE = "    await userRepo.updateUserOrThrow(user.id, { passwordHash: newHash }, 'Password reset');\n"
CONSUME = "    await userRepo.consumeResetToken(tokenHash);\n\n    logger.info('Password reset completed'"
A, P, S = 'src/routes/auth.ts', 'src/services/password.ts', 'vitest.setup.ts'

def nth_replace(text, old, new, which):  # which: 0 = first, 1 = second occurrence
    i = -1
    for _ in range(which + 1):
        i = text.index(old, i + 1)
    return text[:i] + new + text[i + len(old):]

M = []
def m(mid, desc, f, edits):
    M.append((mid, desc, f, edits))

m('m01', 'register: breach check removed', A, [('nth', REG, '', 0)])
m('m02', 'reset: breach check removed', A, [('nth', REG, '', 1)])
m('m03', 'register: breach check moved BEFORE the strength check', A, [('nth', REG, '', 0), ('once', STRENGTH_REG, REG + STRENGTH_REG)])
m('m04', 'reset: breach check moved BEFORE the token lookup', A, [('nth', REG, '', 1), ('once', RESET_STRENGTH, REG + RESET_STRENGTH)])
m('m05', 'reset: breach check moved AFTER the password write', A, [('nth', REG, '', 1), ('once', WRITE, WRITE + REG)])
m('m06', 'reset: breach check moved AFTER the token is consumed', A, [('nth', REG, '', 1), ('once', CONSUME, "    await userRepo.consumeResetToken(tokenHash);\n" + REG + "\n    logger.info('Password reset completed'")])
m('m07', 'refusal text changed', P, [('once', "'This password has appeared in a data breach, choose another'", "'This password is known to be breached'")])
m('m08', 'refusal carries no details', A, [('all', "throw new ValidationError(BREACHED_PASSWORD_MESSAGE, weakPasswordIssues([BREACHED_PASSWORD_MESSAGE], 'password'));", 'throw new ValidationError(BREACHED_PASSWORD_MESSAGE);')])
m('m09', 'fail CLOSED on a throw', P, [('once', "{ thrownType: thrownTypeOf(err) });\n    return false;", "{ thrownType: thrownTypeOf(err) });\n    return true;")])
m('m10', 'fail CLOSED on non-200', P, [('once', "{ status: res.status });\n      return false;", "{ status: res.status });\n      return true;")])
m('m11', 'no timeout signal', P, [('once', "      signal: AbortSignal.timeout(2_000),\n", '')])
m('m12', 'timeout 2 s -> 20 s', P, [('once', 'AbortSignal.timeout(2_000)', 'AbortSignal.timeout(20_000)')])
m('m13', 'full SHA-1 sent in the URL', P, [('once', "const url = `https://api.pwnedpasswords.com/range/${prefix}`;", "const url = `https://api.pwnedpasswords.com/range/${prefix}${suffix}`;")])
m('m14', 'suffix sent in a header', P, [('once', "headers: { 'Add-Padding': 'true' },", "headers: { 'Add-Padding': 'true', 'X-Suffix': suffix },")])
m('m15', 'catch logs the message text', P, [('once', '{ thrownType: thrownTypeOf(err) }', '{ thrownType: thrownTypeOf(err), error: (err as Error)?.message }')])
m('m16', 'thrownTypeOf returns the value as text', P, [('once', "    if (value === null) return 'null';", "    return String((value as Error)?.message ?? value);\n    if (value === null) return 'null';")])
m('m17', 'switch ignored (always on)', P, [('once', "  if (process.env.HIBP_ENABLED === 'false') return false;\n", '')])
m('m18', 'switch made opt-in (on only when "true")', P, [('once', "process.env.HIBP_ENABLED === 'false'", "process.env.HIBP_ENABLED !== 'true'")])
m('m19', 'setup: overrides an explicit value', S, [('once', "if (process.env.HIBP_ENABLED === undefined) process.env.HIBP_ENABLED = 'false';", "process.env.HIBP_ENABLED = 'false';")])
m('m20', 'setup: default removed', S, [('once', "if (process.env.HIBP_ENABLED === undefined) process.env.HIBP_ENABLED = 'false';", '')])
m('m21', 'hash not upper-cased (suffix never matches)', P, [('once', "digest('hex').toUpperCase();\n    const prefix", "digest('hex');\n    const prefix")])
m('m22', 'refusal is a 400 BadRequestError', A, [('all', "throw new ValidationError(BREACHED_PASSWORD_MESSAGE, weakPasswordIssues([BREACHED_PASSWORD_MESSAGE], 'password'));", 'throw new BadRequestError(BREACHED_PASSWORD_MESSAGE);')])
m('m23', 'register: refuses but AFTER createUser (written first)', A, [('nth', REG, '', 0), ('once', '    await userRepo.createUser(user);\n', '    await userRepo.createUser(user);\n' + REG)])
m('m24', 'body parse: count ignored -> padding line 0 counts; equivalent probe: compare on trimmed lowercase', P, [('once', 'if (hashSuffix === suffix) return true;', 'if (hashSuffix.toLowerCase() === suffix.toLowerCase()) return true;')])

index = []
for mid, desc, f, edits in M:
    t = files[f]
    for kind, old, new, *w in [(e[0], e[1], e[2], *e[3:]) for e in edits]:
        if kind == 'nth':
            t = nth_replace(t, old, new, w[0])
        elif kind == 'once':
            assert t.count(old) == 1, (mid, 'count', t.count(old), old[:60])
            t = t.replace(old, new)
        elif kind == 'all':
            assert t.count(old) == 2, (mid, 'count', t.count(old))
            t = t.replace(old, new)
    assert t != files[f], mid
    d = os.path.join(OUT, mid); os.makedirs(d, exist_ok=True)
    open(os.path.join(d, f.replace('/', '__')), 'w').write(t)
    index.append({'id': mid, 'file': f, 'desc': desc})
json.dump(index, open(os.path.join(OUT, 'index.json'), 'w'), indent=1)
print(len(index), 'mutants')
