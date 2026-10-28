P='Blockchain/Dev/services/mcp-server/src/http-server.ts'
TP='Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-generate-package-doctypes-default.test.ts'
E1=("    if (!apiKey) {\n",
    "    // KS-1530: a PRESENT allowedDocumentTypes that is not a list (\"\", 0, false, null, an object) used to reach the generator as []\n"
    "    // (\"all types permitted\") with a 200. The caller's value is the problem, so it is refused with a 400, as the gateway refuses the same\n"
    "    // stored value with a 403 (KS-1232). An OMITTED allowedDocumentTypes still defaults to [] below.\n"
    "    if (allowedDocumentTypes !== undefined && !Array.isArray(allowedDocumentTypes)) {\n"
    "      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'allowedDocumentTypes must be an array when given' } });\n"
    "      return;\n"
    "    }\n"
    "    if (!apiKey) {\n")
OLDCELL="""  it('RED KS-1232: allowedDocumentTypes "", 0 and false each reach the package generator as [] with status 200', async () => {
    expect([await generate(''), await generate(0), await generate(false)]).toEqual([[200, []], [200, []], [200, []]]);
  });
"""
NEWCELL="""  it('RED KS-1530: allowedDocumentTypes "", 0, false, null and an object are each refused 400 and never reach the package generator', async () => {
    const refused: [number, unknown] = [400, 'generatePackage not called once'];
    expect([await generate(''), await generate(0), await generate(false), await generate(null), await generate({})]).toEqual([refused, refused, refused, refused, refused]);
  });
  it('CONTROL KS-1530: an omitted allowedDocumentTypes still reaches the package generator as [] with status 200', async () => {
    expect(await generate(undefined)).toEqual([200, []]);
  });
"""
HDR_OLD=" * driven over loopback. A characterisation pin of TODAY's default at this site.\n"
HDR_NEW=" * driven over loopback. KS-1530 flipped the \"\", 0 and false cell: a present non-array value is now refused 400, an omitted one still defaults to [].\n"
S=dict(dir='ks_1530_p1',ticket='KS-1530',
 title='mcp-server POST /generate-package: a falsy allowedDocumentTypes ("", 0, false) reaches the package generator as [] (all types permitted) with status 200 - refuse a present non-array with 400 (RUNG 2, code_patch: one product hunk + two hunks in the existing pin test; the DRAFTER chose the 400 shape)',
 intro="DRAFT by Spark operator 7 for Wednesday, 2026-10-29 AEDT (never-keep-the-Spark-idle round). Secuura only. A local PASS is a candidate, never a merge; the normal QA gate before merge. DECISION FLAG: the ticket says 'a decision first, then a small build' (refuse with a 400, or pass it on as unusable). This brief takes the 400, which matches the ticket's own reasoning (the value is the caller's; the gateway answers the same stored value with a refusal). Whoever raises the PR must confirm that shape with the owner.",
 products=[(P,[E1])],
 prodnote=['product, modified in place: ONE hunk, a pure insertion of 7 lines before the apiKey check'],
 tests=[dict(path=TP,new=False,edits=[(OLDCELL,NEWCELL),(HDR_OLD,HDR_NEW)])],
 testnote=['EXISTING (the KS-1232 characterisation pin), modified in place: TWO hunks (the header comment line; the RED cell replaced by a RED cell and one new CONTROL cell)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1232-generate-package-doctypes-default.test.ts` from `Blockchain/Dev/services/mcp-server',
 tier='code_patch', rung='2 (one pure-insertion hunk of 7 lines byte-exact; two hunks in one existing test)',
 pins='''# code_patch, ONE insertion hunk in mcp-server http-server.ts + the existing ks1232 pin test modified in place (RED cell flipped, one control added); ref = the sibling mcp-server test (shape only); test_file pinned (in-place test); line = the line the insertion follows.
tier=code_patch
test_file=Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-generate-package-doctypes-default.test.ts
ref=Blockchain/Dev/services/mcp-server/src/__tests__/ks1541-get-info-names-a-gateway-refusal.test.ts
line=236
ctx=65536
''',
 wrong="`POST /generate-package` in `services/mcp-server/src/http-server.ts` reads `allowedDocumentTypes` from the request body and hands the generator `allowedDocumentTypes || []` (`:258`). A present value that is not a list but is falsy (`\"\"`, `0`, `false`) therefore becomes `[]`, which `MCP Deployment/troubleshooting.md:123` documents as \"all types permitted\", and the endpoint answers 200: the caller sent something that is not a list and gets back a package that says the connector is unrestricted. The gateway refuses the same stored value with a 403 (KS-1232). The change: directly before the `apiKey` check, answer 400 BAD_REQUEST when `allowedDocumentTypes` is present (not `undefined`) and is not an array, before any response header is set and before the generator runs. An omitted `allowedDocumentTypes` still defaults to `[]` at `:258`, which stays as it is. The existing characterisation pin (`ks1232-generate-package-doctypes-default.test.ts`) asserted today's behaviour and is flipped in place.",
 where="- `src/http-server.ts:236` - the line `    if (!apiKey) {`: **the insertion goes directly before it**, after the closing `}` of the agentType check at `:235`. Seven lines are added (3 comment lines, the `if`, the 400 `res.status(400).json(...)` line, `return;`, the closing `}`), exactly as under \"The exact change\".\n- `src/http-server.ts:258` (`allowedDocumentTypes: allowedDocumentTypes || [],`) is NOT touched.\n- `src/__tests__/ks1232-generate-package-doctypes-default.test.ts`: header line 6 (`driven over loopback. A characterisation pin ...`) and the `RED KS-1232` cell (`:62-64`) change as under \"The test\".",
 exactnote="ONE pure-insertion hunk in the product file.\n",
 donot="**Do NOT touch** `:258`, the `apiKey` check, the generator call, or any other line of either file.",
 testnote2="The `+` lines are byte-exact; the `-` lines are the old cell (3 lines) and the old header line. The new RED cell uses the file's own `generate(...)` helper, which reports `'generatePackage not called once'` when the generator was not called.",
 red=['RED KS-1530'],
 cells="- RED `RED KS-1530`: at the tip all five values answer 200 and reach the generator, so the equality fails by ASSERTION; after the product edit all five answer 400 and the generator is not called.\n- CONTROL (new): an omitted `allowedDocumentTypes` still answers 200 with `[]` at the tip and after.\n- CONTROL (existing, untouched): a stored list `['contract']` reaches the generator unchanged with status 200.",
 premises="- `http-server.ts:236-239` is the `apiKey` check and `:229-235` the agentType check and `:258` the `|| []` default (read at the tip).\n- The file's `generate(value)` helper POSTs `{agentType: 'generic_http', apiKey: 'sk_ks1232', allowedDocumentTypes: value}` as JSON, so `undefined` is dropped from the body (the key is omitted) and `null` / `{}` are sent as written.\n- The service's test runner is vitest. The golden is generated by script, not typed.",
 unmeasured="- Nothing was run by the drafter apart from the harness dry-run and control.\n- Whether the gateway-proxied `POST /api/mcp/generate-package` callers ever send a non-array today: unmeasured (the ticket says reachable through the gateway).\n- `MCP Deployment/troubleshooting.md:123` is not updated by this brief (the ticket's recommendation does not ask for it).\n- Open PRs touching these files: none by the git file lists of PRs 1782 and 1785-1799 read on 2026-10-29.",
 scope="**KS-1530 only.** DECISION FLAG above. Link the PR as Refs KS-1530 until the owner has confirmed the 400.",
)
