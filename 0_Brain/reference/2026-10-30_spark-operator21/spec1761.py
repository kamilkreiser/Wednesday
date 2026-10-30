# KS-1761 (narrowed to the bare undefined/null id): ks1564 AST guard accepts fetchApiKeys(undefined)/(null) because PLAIN_IDENTIFIER matches them. Spark operator 21.
# test_only, ONE existing test modified in place, TWO hunks (the regex line, and new cells after cell 4). Tamper in the admin page ApiKeys.tsx:137.
PROD='Blockchain/Dev/frontend/admin/src/pages/ApiKeys.tsx'
TEST='Blockchain/Dev/packages/shared/src/__tests__/ks1564-admin-api-keys-page-sends-no-default-org.test.ts'
REF='Blockchain/Dev/packages/shared/src/__tests__/entrypoint-corpus.test.ts'
OLD_RE="const PLAIN_IDENTIFIER = /^[A-Za-z_$][\\w$.]*$/;\n"
NEW_RE=("// KS-1761: `undefined` and `null` are spelled like identifiers, so the old pattern accepted `fetchApiKeys(undefined)`; they are refused here.\n"
        "const PLAIN_IDENTIFIER = /^(?!(?:undefined|null)$)[A-Za-z_$][\\w$.]*$/;\n")
ANCHOR=("    expect(escapes).toEqual([]);\n"
        "  });\n")
CELLS=ANCHOR+"""
  it('4b. KS-1761 a bare undefined or null is not a plain identifier, an ordinary name or dotted path still is', () => {
    for (const bad of ['undefined', 'null']) expect(PLAIN_IDENTIFIER.test(bad), bad).toBe(false);
    for (const ok of ['orgId', 'selected.id', '_org$1', 'undefinedOrg']) expect(PLAIN_IDENTIFIER.test(ok), ok).toBe(true);
  });

  it('4c. KS-1761 fetchApiKeys(undefined) and fetchApiKeys(null) are read as calls, and the guard refuses their argument', () => {
    for (const literal of ['undefined', 'null']) {
      const args = fetchApiKeysArgs(`async function f() { await fetchApiKeys(${literal}); }`, 'planted.tsx');
      expect(args).toEqual([literal]);
      expect(args[0]).not.toMatch(PLAIN_IDENTIFIER);
    }
    expect(fetchApiKeysArgs('async function f(orgId: string) { await fetchApiKeys(orgId); }', 'planted.tsx')[0]).toMatch(PLAIN_IDENTIFIER);
  });
"""
T=dict(dir='ks_1761_p1_undefined_null_id',ticket='KS-1761',test=TEST,product=PROD,ref=REF,
 runner='vitest` (`npx vitest run src/__tests__/ks1564-admin-api-keys-page-sends-no-default-org.test.ts` from `Blockchain/Dev/packages/shared`',
 rung='4 (test HARDENING, TWO hunks in one existing guard test: a regex tightened and two cells added; the tamper is the blind spot the ticket names)',
 nh_txt='2 hunks: the one-line regex `PLAIN_IDENTIFIER` replaced by a comment plus the tightened regex, and two new cells after cell 4',
 nh_word='TWO hunks, in this order',
 nh_head='TWO EDITS in the TEST file (two hunks)',
 title="shared ks1564 guard: the AST guard accepts fetchApiKeys(undefined) and fetchApiKeys(null) because PLAIN_IDENTIFIER matches the literals - tighten it and pin it (KS-1761, ONLY the bare undefined/null blind spot; TEST-ONLY: one existing test, two in-place hunks, planted tamper in the admin page)",
 intro="DRAFT by Spark operator 21 for Wednesday, 2026-10-30 AEDT. Secuura (packages/shared guard test over the admin frontend) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1761 (gate t4s4 LOW on #1734): the AST guard in `ks1564-admin-api-keys-page-sends-no-default-org.test.ts` has three blind spots; this task closes ONLY the third (a bare `undefined` or `null` id: the regex `PLAIN_IDENTIFIER` accepts the two literals because they look like identifiers). The other blind spots (a member call `api.fetchApiKeys(...)`, a bracket call, a `.js` file) are deliberate exclusions whose boundary the ticket calls a judgement: NOT touched. The guard file is the thing edited; the product page `ApiKeys.tsx` is not modified, it is the tamper target (the checker replaces `fetchApiKeys(orgId)` at :137 with `fetchApiKeys(undefined)`, which existing cell 4 only refuses once the regex is tightened). Rung 4 for the two hunks in one file that must agree (the regex and the cells that use it).",
 tamper_line=137,
 tamper_from="    const result = await fetchApiKeys(orgId);",
 tamper_to="    const result = await fetchApiKeys(undefined);",
 statement_ok="line 137 is the single call `fetchApiKeys(orgId)` inside `loadKeys` in the page; the replacement passes the bare literal `undefined`, which parses as a call with one argument (TypeScript's parse is all the guard needs; no type check runs) and which the old regex accepted and the tightened regex refuses; `orgId` remains declared and used elsewhere in the page",
 edit=[(OLD_RE,NEW_RE),(ANCHOR,CELLS)],
 red=['4. every fetchApiKeys CALL passes a plain identifier, and the name is never taken as a value'],
 what_wrong="`PLAIN_IDENTIFIER = /^[A-Za-z_$][\\w$.]*$/` (the test file, :365) is what cells 3 and 4 use to decide that an argument is 'a plain identifier, not a literal'. The words `undefined` and `null` match it, so `fetchApiKeys(undefined)` or `fetchApiKeys(null)` (the page invents no id, but sends none either) stays GREEN. The gate t4s4 recorded it as a blind spot the guard header does not list. The fix: refuse those two words in the regex with a negative lookahead (`^(?!(?:undefined|null)$)` in front of the existing pattern, so `undefinedOrg` and dotted paths still match) and add two cells after cell 4: 4b tests the regex directly on bad and good strings, 4c feeds planted source to `fetchApiKeysArgs` and checks the argument is read as the literal and refused. The existing cell 4 is the one that goes RED under the tamper.",
 where="- `frontend/admin/src/pages/ApiKeys.tsx:137` - (correct, STAYS) `    const result = await fetchApiKeys(orgId);` - the line the tamper replaces in the checker's clone.\n- `packages/shared/src/__tests__/ks1564-admin-api-keys-page-sends-no-default-org.test.ts:365` - the one-line `const PLAIN_IDENTIFIER = ...` is replaced by TWO lines (a comment and the tightened constant). Hunk 2 adds cells `4b` and `4c` directly after cell 4 (which ends `expect(escapes).toEqual([]);` then `});`, :386-387 region), before cell 5.",
 cells="- RED under the tamper: existing cell `4.` fails by assertion (`argument \"undefined\"` does not match the tightened `PLAIN_IDENTIFIER`).\n- GREEN at the untouched tip: all cells including 4b and 4c (4c's third assertion proves an ordinary name is still accepted).\n- The other existing cells (3, 5, 6, 7, C1-C4) stay green under the tamper.",
 unmeasured="- The drafter did NOT run vitest for the brief: RED-under-tamper / GREEN-at-tip is the `round.sh --control` run on this golden.\n- Whether the Spark cache can run this packages/shared test (it imports `typescript` and walks `frontend/admin/src`): the control run measures it; a baseline red here is a HARNESS class, not a model verdict.\n- A dotted expression such as `a.b.c` still matches (the regex tail class admits a dot): recorded in the ticket as a read of the regex, NOT changed here.\n- The member-call, bracket-call and `.js` blind spots are untouched (the ticket says they are deliberate or undecided).\n- Open PRs touching packages/shared or frontend/admin: only their package.json files (read 2026-10-30), not this test or the page.",
 scope="**Refs KS-1761, never a close-word. Narrowing:** the bare `undefined`/`null` id only, one of the three blind spots. The ticket says it proposes no fix; this applies the smallest regex change and pins it, which the raise seat may decline.",
)
