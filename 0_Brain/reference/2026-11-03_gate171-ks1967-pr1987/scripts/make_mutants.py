import sys, json
W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate171-ks1967-pr1987'
src = open(f'{W}/scratch/head_accountLockout.ts').read()
NOCLIENT_ISL = """  if (!redis) {
    // KS-1967: was `return false` ("not locked") with no client.
    logger.warn('lockout: session store unavailable on isLockedOut — refusing the login', { cause: 'no-client' });
    throw new ServiceUnavailableError();
  }"""
CATCH_ISL = """    logger.warn('lockout: session store error on isLockedOut — refusing the login', { cause: 'threw', thrownType: thrownTypeOf(err) });
    throw new ServiceUnavailableError();"""
NOCLIENT_RF = """    logger.warn('lockout: session store unavailable on recordFailure — refusing; this failure cannot be counted', { cause: 'no-client' });
    throw new ServiceUnavailableError();"""
CATCH_RF = """    logger.warn('lockout: session store error on recordFailure — refusing; this failure may not have been counted', { cause: 'threw', thrownType: thrownTypeOf(err) });
    throw new ServiceUnavailableError();"""
CATCH_RS = """    logger.warn('lockout: session store error on recordSuccess — non-fatal', { cause: 'threw', thrownType: thrownTypeOf(err) });"""
M = {
 'M01 isLockedOut no-client returns false': (NOCLIENT_ISL, "  if (!redis) return false;"),
 'M02 isLockedOut catch returns false': (CATCH_ISL, "    logger.warn('lockout: session store error on isLockedOut — refusing the login', { cause: 'threw', thrownType: thrownTypeOf(err) });\n    return false;"),
 'M03 isLockedOut catch logs the message': (CATCH_ISL, "    logger.warn('lockout: session store error on isLockedOut — refusing the login', { cause: 'threw', thrownType: (err as any)?.message });\n    throw new ServiceUnavailableError();"),
 'M04 recordFailure no-client returns 0': (NOCLIENT_RF, "    return 0;"),
 'M05 recordFailure catch returns 0': (CATCH_RF, "    return 0;"),
 'M06 recordSuccess catch made fatal (503)': (CATCH_RS, CATCH_RS + "\n    throw new ServiceUnavailableError();"),
 'M07 recordSuccess no-client made fatal (503)': ("  if (!redis) return;\n  try {\n    await redis.del(", "  if (!redis) throw new ServiceUnavailableError();\n  try {\n    await redis.del("),
 'M08 thrownTypeOf always object': ("    const name: unknown = Object.getPrototypeOf(value)?.constructor?.name;\n    return typeof name === 'string' && name !== '' ? name : 'object';", "    return 'object';"),
 'M09 thrownTypeOf without its try (revoked Proxy escapes)': ("  } catch {\n    return 'unreadable';\n  }", "  } finally {\n  }"),
 'M10 isLockedOut inverted (v === null)': ("  return v !== null;\n}", "  return v === null;\n}"),
 'M11 isLockedOut catch puts the thrown text in the 503 body': (CATCH_ISL, "    logger.warn('lockout: session store error on isLockedOut — refusing the login', { cause: 'threw', thrownType: thrownTypeOf(err) });\n    throw new ServiceUnavailableError(String((err as any)?.message));"),
 'M12 recordFailure catch rethrows the original': (CATCH_RF, "    logger.warn('lockout: session store error on recordFailure — refusing; this failure may not have been counted', { cause: 'threw', thrownType: thrownTypeOf(err) });\n    throw err;"),
 'M13 isLockedOut catch rethrows the original': (CATCH_ISL, "    logger.warn('lockout: session store error on isLockedOut — refusing the login', { cause: 'threw', thrownType: thrownTypeOf(err) });\n    throw err;"),
 'M14 isLockedOut no-client throws a plain Error (500)': (NOCLIENT_ISL, "  if (!redis) throw new Error('store down');"),
 'M15 recordSuccess catch logs the message (base line)': (CATCH_RS, "    logger.warn('lockout: redis error on recordSuccess — non-fatal', { error: (err as any)?.message });"),
 'M16 recordFailure catch logs the message': (CATCH_RF, "    logger.warn('lockout: session store error on recordFailure — refusing; this failure may not have been counted', { cause: 'threw', error: (err as any)?.message });\n    throw new ServiceUnavailableError();"),
}
idx = {}
for i, (name, (a, b)) in enumerate(M.items(), 1):
    assert src.count(a) == 1, (name, src.count(a))
    m = src.replace(a, b); assert m != src
    p = f'{W}/mut/m{i:02d}.ts'; open(p, 'w').write(m); idx[f'm{i:02d}'] = name
json.dump(idx, open(f'{W}/mut/index.json', 'w'), indent=1)
print(len(idx), 'mutants written')
