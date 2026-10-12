import sys
p = sys.argv[1]
s = open(p).read()
def rep(old, new):
    global s
    assert s.count(old) == 1, ('ANCHOR', old[:60], s.count(old))
    s = s.replace(old, new, 1)
rep("postgresql://gate@127.0.0.1:55432/gate", "postgresql://gate@127.0.0.1:55434/gate")
rep("    await pool.query('TRUNCATE svc_api_keys');",
    "    await pool.query('TRUNCATE svc_api_keys');\n    await pool.query('TRUNCATE organizations');\n"
    "    await pool.query('INSERT INTO organizations (id, tenant_id) VALUES ($1,$2),($3,$2),($4,$2),($5,$6)', [A1, TA, A2, OA, B1, TB]);")
rep("const CONN_A1 = 'platform-s:a1-ref';", "const CONN_A1 = 'platform-s:a1-ref';\nconst OA = 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';\nconst OB = 'abcdefab-cdef-4abc-8def-abcdefabcdef';")
rep("    const OA = 'aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee';\n    const OB = 'abcdefab-cdef-4abc-8def-abcdefabcdef';\n", "")
rep("async function call(t: string | null, body: unknown, extra: { query?: string; headers?: Record<string, string>; raw?: string } = {}) {",
    "async function list(t: string, org: string) {\n  const r = await fetch(`${base}/api/keys?organizationId=${encodeURIComponent(org)}`, { headers: { Authorization: `Bearer ${t}` } });\n  const j: any = await r.json().catch(() => null);\n  return { status: r.status, ids: (j?.data ?? []).map((k: any) => k.id) as string[] };\n}\n\nasync function call(t: string | null, body: unknown, extra: { query?: string; headers?: Record<string, string>; raw?: string } = {}) {")
rep("    return r.rows.map((x: any) => ({ id: x.id, org: x.organization_id, tenant: x.tenant_id, connector: x.connector_id, active: x.is_active }));",
    "    const sq = r.rows.map((x: any) => ({ id: x.id, org: x.organization_id, tenant: x.tenant_id, connector: x.connector_id, active: x.is_active }));\n"
    "    // cross-check: the module map must agree with SQL on every row both hold (the list route reads the map)\n"
    "    for (const k of mem.values()) { const q = sq.find((y: any) => y.id === k.id); if (q && ((k.organizationId ?? null) !== q.org || k.isActive !== q.active)) out.memSqlDisagree = (out.memSqlDisagree ?? 0) + 1; }\n"
    "    return sq;")

NEW = r'''
  it('R1 battery: every non-platform role x every rotate shape against connector A2 (victim must stay active)', async () => {
    out.rotshapes = [];
    const R: Array<[string, (b: any) => [any, any]]> = [
      ['rotate true', (b) => [{ ...b, rotate: true }, {}]],
      ['rotate "true"', (b) => [{ ...b, rotate: 'true' }, {}]],
      ['rotate 1', (b) => [{ ...b, rotate: 1 }, {}]],
      ['rotate "1"', (b) => [{ ...b, rotate: '1' }, {}]],
      ['rotate [true]', (b) => [{ ...b, rotate: [true] }, {}]],
      ['rotate {}', (b) => [{ ...b, rotate: {} }, {}]],
      ['rotate null', (b) => [{ ...b, rotate: null }, {}]],
      ['query ?rotate=true', (b) => [b, { query: '?rotate=true' }]],
      ['header x-rotate', (b) => [b, { headers: { 'x-rotate': 'true' } }]],
      ['body Rotate', (b) => [{ ...b, Rotate: true }, {}]],
      ['nested data.rotate', (b) => [{ ...b, data: { rotate: true } }, {}]],
      ['dup key false,true', (b) => [null, { raw: JSON.stringify(b).slice(0, -1) + ',"rotate":false,"rotate":true}' }]],
      ['dup key true,false', (b) => [null, { raw: JSON.stringify(b).slice(0, -1) + ',"rotate":true,"rotate":false}' }]],
      ['__proto__.rotate', (b) => [null, { raw: JSON.stringify(b).slice(0, -1) + ',"__proto__":{"rotate":true}}' }]],
      ['constructor.prototype.rotate', (b) => [null, { raw: JSON.stringify(b).slice(0, -1) + ',"constructor":{"prototype":{"rotate":true}}}' }]],
      ['rotate true + connectorId trailing space', (b) => [{ ...b, connectorId: `${CONN_A2} `, rotate: true }, {}]],
      ['rotate true + connectorId upper', (b) => [{ ...b, connectorId: CONN_A2.toUpperCase(), rotate: true }, {}]],
      ['rotate true + connectorId empty', (b) => [{ ...b, connectorId: '', rotate: true }, {}]],
      ['rotate true + connectorId in query only', (b) => { const { connectorId, ...rest } = b; void connectorId; return [{ ...rest, rotate: true }, { query: `?connectorId=${encodeURIComponent(CONN_A2)}` }]; }],
    ];
    const orgs: Record<string, Record<string, unknown>> = { own: { tenantId: TA, organizationId: A1 }, victim: { tenantId: TA, organizationId: A2 }, none: { tenantId: TA } };
    for (const rn of ['provisioner', 'ADMIN', 'ORG_ADMIN', 'org_admin_lc', 'ISSUER_ADMIN', 'orgless_issuer_admin', 'platform_admin', 'user', 'scopeless_connector']) {
      for (const [on, op] of Object.entries(orgs)) {
        for (const [label, mk] of R) {
          const victim = await seedVictim();
          const before = await rows();
          const [body, extra] = mk({ name: `rs ${rn} ${label}`, ...op, connectorId: CONN_A2 });
          const r = await call(tok(ROLES[rn]), body, extra);
          const after = await rows();
          const added = after.filter((a) => !before.some((b) => b.id === a.id));
          const newlyInactive = after.filter((a) => a.active === false && before.find((b) => b.id === a.id)?.active === true);
          out.rotshapes.push({ role: rn, org: on, label, status: r.status, msg: r.body?.error?.message ?? null,
            victimActive: after.find((a) => a.id === victim)?.active, retired: newlyInactive.length,
            added: added.map((a) => ({ org: a.org, connector: a.connector })), priorKeysRevoked: r.body?.data?.priorKeysRevoked });
          expect(after.find((a) => a.id === victim)?.active, `${rn}/${on}/${label}: victim retired`).toBe(true);
          expect(newlyInactive.length, `${rn}/${on}/${label}: something retired`).toBe(0);
        }
      }
    }
  }, 300_000);

  it('PLATFORM rotate CONTROL (the battery above must be able to see a retirement)', async () => {
    const victim = await seedVictim();
    const r = await call(tok(ROLES.super_admin), { name: 'ctl', tenantId: TA, organizationId: A2, connectorId: CONN_A2, rotate: true });
    const after = await rows();
    out.platformRotateControl = { status: r.status, victimActive: after.find((a) => a.id === victim)?.active, priorKeysRevoked: r.body?.data?.priorKeysRevoked };
    expect(r.status).toBe(201);
    expect(after.find((a) => a.id === victim)?.active, 'control: a platform rotate must retire the victim').toBe(false);
  });

  it('m1 battery: stored form per caller x organisation variant, and what GET /api/keys lists', async () => {
    out.m1 = [];
    const callers: Record<string, Record<string, unknown>> = {
      super_admin: ROLES.super_admin,
      ISSUER_ADMIN_OA: { role: 'ISSUER_ADMIN', tenantId: TA, organizationId: OA },
      ISSUER_ADMIN_OA_upperclaim: { role: 'ISSUER_ADMIN', tenantId: TA, organizationId: OA.toUpperCase() },
      ADMIN_OA: { role: 'ADMIN', tenantId: TA, organizationId: OA },
      provisioner_OA: { role: 'connector', type: 'connector', tenantId: TA, organizationId: OA, scopes: ['organizations:register'] },
      orgless_issuer_admin: ROLES.orgless_issuer_admin,
    };
    const vs: Record<string, string> = { canonical: OA, upper: OA.toUpperCase(), padded_upper: `  ${OA.toUpperCase()} `, tab: `\t${OA}`,
      nbsp: ` ${OA}`, zwsp: `​${OA}`, empty: '', spaces: '   ', tabnl: '\t\n', braces: `{${OA}}`, nohyphen: OA.replace(/-/g, ''),
      foreign_upper: OB.toUpperCase(), foreign_padded: ` ${OB} ` };
    expect(OA.toUpperCase(), 'control: OA has letters').not.toBe(OA);
    for (const [cn, claims] of Object.entries(callers)) {
      for (const [vn, v] of Object.entries(vs)) {
        const before = await rows();
        const r = await call(tok(claims), { name: `m1 ${cn} ${vn}`, tenantId: TA, organizationId: v });
        const after = await rows();
        const added = after.filter((a) => !before.some((b) => b.id === a.id));
        const id = r.body?.data?.id ?? null;
        const viaCanonical = id ? (await list(tok(ROLES.super_admin), OA)).ids.includes(id) : null;
        const viaUpper = id ? (await list(tok(ROLES.super_admin), OA.toUpperCase())).ids.includes(id) : null;
        const viaSent = id ? (await list(tok(ROLES.super_admin), v)).ids.includes(id) : null;
        const memOrg = id ? (mem.get(id)?.organizationId ?? null) : null;
        out.m1.push({ caller: cn, variant: vn, sent: v, status: r.status, msg: r.body?.error?.message ?? null,
          stored: added.map((a) => a.org), memOrg, listedCanonical: viaCanonical, listedUpper: viaUpper, listedAsSent: viaSent });
      }
    }
    // the org's own admin listing (non-platform list path) with the canonical and upper query
    const own = tok(callers.ISSUER_ADMIN_OA);
    out.m1list = { ownCanonical: (await list(own, OA)), ownUpper: (await list(own, OA.toUpperCase())), ownPadded: (await list(own, ` ${OA} `)) };
  }, 300_000);

  it('item 5: tenant resolved from the RAW organisation id when no tenant is sent', async () => {
    out.item5 = [];
    const callers: Record<string, Record<string, unknown>> = {
      ISSUER_ADMIN_A1: ROLES.ISSUER_ADMIN, ADMIN_A1: ROLES.ADMIN, ORG_ADMIN_A1: ROLES.ORG_ADMIN, provisioner_A1: ROLES.provisioner,
      orgless_issuer_admin: ROLES.orgless_issuer_admin, super_admin: ROLES.super_admin,
    };
    const U = '99999999-9999-4999-8999-999999999999';
    const vs: Record<string, string> = { B1: B1, B1_upper: B1.toUpperCase(), B1_padded: ` ${B1} `, B1_braces: `{${B1}}`, B1_nohyphen: B1.replace(/-/g, ''),
      A1: A1, A1_padded: ` ${A1} `, A1_braces: `{${A1}}`, OA_upper: OA.toUpperCase(), OA_padded: ` ${OA.toUpperCase()} `, unknown: U };
    for (const [cn, claims] of Object.entries(callers)) {
      for (const [vn, v] of Object.entries(vs)) {
        const before = await rows();
        const r = await call(tok(claims), { name: `i5 ${cn} ${vn}`, organizationId: v });
        const after = await rows();
        const added = after.filter((a) => !before.some((b) => b.id === a.id));
        out.item5.push({ caller: cn, variant: vn, sent: v, status: r.status, msg: r.body?.error?.message ?? null,
          stored: added.map((a) => ({ tenant: a.tenant, org: a.org })) });
      }
    }
  }, 300_000);
});'''
# insert before the final '});' of the describe
idx = s.rstrip().rfind('});')
s = s[:idx] + NEW.lstrip('\n') + '\n'
open(p, 'w').write(s)
print('patched OK')
