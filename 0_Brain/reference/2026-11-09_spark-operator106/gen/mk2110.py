src=open('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_spark-operator106/gen/mktest.py',encoding='utf-8').read()
exec(src.split('# ---- KS-2121')[0])
TK=B+'packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts'
MW=B+'packages/shared/src/middleware/index.ts'; TI=B+'services/tokenisation/src/index.ts'
ot=rd('ks1536-one-role-vocabulary.test.ts')
nt=rep(ot,"  it('RED ks1536 M3 no user is UnauthorizedError', async () => { expect(await run(undefined)).toBe('UnauthorizedError'); });\n",
"  it('RED ks1536 M3 no user is UnauthorizedError', async () => { expect(await run(undefined)).toBe('UnauthorizedError'); });\n  it('RED ks1536 M4 a user with no role is ForbiddenError', async () => { expect(await run({})).toBe('ForbiddenError'); });\n")
nt=rep(nt,"""    expect(t).not.toContain('PLATFORM_ADMIN_ROLES');
  });
""","""    expect(t).not.toContain('PLATFORM_ADMIN_ROLES');
  });

  it('RED ks1536 G5b tokenisation puts requirePlatformRole on each key route itself, not only twice somewhere', () => {
    const t = readFileSync(join(DEV, 'services/tokenisation/src/index.ts'), 'utf8');
    expect(t).toContain("app.post('/api/generate-key', requirePlatformRole(),");
    expect(t).toContain("app.post('/api/rotate-key', requirePlatformRole(),");
  });
""")
mw=rd('shared_middleware.ts')
nmw=rep(mw,"    if (!isPlatformRole(req.user.role)) {\n","    if (req.user.role !== undefined && !isPlatformRole(req.user.role)) { // TAMPER: a user with no role passes\n")
ti=rd('tokenisation_index.ts')
nti=rep(ti,"app.post('/api/rotate-key', requirePlatformRole(), async (req, res) => {\n","void requirePlatformRole(); // TAMPER: stray call keeps the text count at 2\napp.post('/api/rotate-key', async (req, res) => {\n")
red=dd(MW,mw,nmw)+dd(TI,ti,nti)
brief('ks_2110_o106_p1_requireplatformrole_undefined_role_row_and_per_route_pin','KS-2110',
 'KS-2110 (TEST-ONLY): requirePlatformRole has no undefined-role row, and the tokenisation key routes are pinned only by a count (SECURITY-ADJACENT: name a tier 1 gate)',
 'KS-2110 (seat S 37th filing, 2026-11-08; Backlog; Medium; gate 244 F4: an ungated /api/rotate-key behind a stray `void requirePlatformRole();` left 97 of 97 cells green, and a requirePlatformRole that passes a user with no role survived). The cells are a security gate\'s tests: the hold note names a tier 1 gate. NOT covered: a route-level cell driving the live routes (the entry module cannot be split in a test-only pass)',
 MW,[TK],
 '`requirePlatformRole()` (packages/shared/src/middleware/index.ts) guards the tokenisation key-generation and key-rotation routes. In `packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts`, M1-M3 (inside `describe(\'KS-1536: requirePlatformRole\')`) drive the middleware with five admitted spellings, four refused ones and no user, but no row passes a user object that has NO role; and cell G5 only counts that the text `requirePlatformRole()` occurs twice in `services/tokenisation/src/index.ts`, so a stray `void requirePlatformRole();` above an ungated route keeps it green. The wiring is correct at the tip (lines 225 and 294 read `app.post(\'/api/generate-key\', requirePlatformRole(), ...` and `app.post(\'/api/rotate-key\', requirePlatformRole(), ...`).',
 'Two edit points in the one test file, nothing else. (1) Directly after the M3 cell, one new cell M4: a user object `{}` (no role) reads `ForbiddenError`. (2) Directly after the G5 cell, one new cell G5b: the entry module text contains the exact route-and-middleware prefix for BOTH key routes. The whole diff, to copy EXACTLY:',
 dd(TK,ot,nt),red,
 ['M4 a user with no role is ForbiddenError','G5b tokenisation puts requirePlatformRole on each key route itself'],
 'The plant is the brief author\'s reading of the gate\'s two plants (a middleware that passes a user with no role; a stray void call above an ungated /api/rotate-key), not the gate\'s own files. Not covered: cells that drive the live routes (needs the entry module split); whether systemTest has a suite on these routes (the ticket did not search).',
 'Both cells are in the diff above; copy them verbatim. M4 reuses `run`; G5b reuses `readFileSync`, `join` and `DEV`, all defined in the file. Both pass on the correct code and fail by an assertion under the plant.',
 'shared_pkg_dir=none\nshared_pkg_name=none\n')
