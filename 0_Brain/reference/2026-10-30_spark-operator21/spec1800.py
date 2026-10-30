# KS-1800 (m365 ks1670 source-text pin: a raw connectionId by concatenation survives, gate 7 N6). Spark operator 21. test_only, ONE existing test modified in place.
PROD='Blockchain/Dev/services/m365-integration/src/index.ts'
TEST='Blockchain/Dev/services/m365-integration/src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts'
REF='Blockchain/Dev/services/m365-integration/src/__tests__/ks1641-the-oauth-callback-caps-the-reflected-error-description.test.ts'
ANCHOR="""  it('control KS-1670 C3 the invalid_state refusal redirect is untouched', () => {
    expect(SRC).toContain('/admin/integrations?m365=error&message=invalid_state');
  });
"""
CELLS=ANCHOR+"""
  // KS-1800 (gate 7 mutant N6): R1's needle is the template text `connectionId=${`, so a redirect that carries the id by STRING CONCATENATION
  // ('...connectionId=' + connectionId) is invisible to it by construction. This scan is the other half: it reads every non-comment line
  // and refuses a `connectionId=` query key that is closed by a quote and joined to something with `+`.
  function concatenatedConnectionIdLines(src: string): string[] {
    return src
      .split('\\n')
      .filter((l) => !/^\\s*(\\/\\/|\\/\\*|\\*)/.test(l))
      .filter((l) => /connectionId=['"`]\\s*\\+/.test(l));
  }

  it('RED KS-1670 R3 no redirect in the service carries the connection id by string concatenation', () => {
    expect(concatenatedConnectionIdLines(SRC)).toEqual([]);
  });

  it('control KS-1670 C4 the concatenation scan can fail: it finds a planted concatenated redirect, in either quote style', () => {
    const planted = "    res.redirect(base + '/admin/integrations?m365=success&connectionId=' + connectionId);\\n"
      + '    res.redirect(base + "/admin/integrations?m365=success&connectionId=" + connectionId);\\n';
    expect(concatenatedConnectionIdLines(planted)).toHaveLength(2);
  });

  it('control KS-1670 C5 the scan ignores a comment line, and the real template redirect is still in the source', () => {
    const commented = "    // res.redirect(base + '/x?connectionId=' + connectionId);\\n";
    expect(concatenatedConnectionIdLines(commented)).toEqual([]);
    expect(SRC).toContain('m365=success&connectionId=${encodeURIComponent(connectionId)}');
  });
"""
T=dict(dir='ks_1800_p1_concat_connection_id',ticket='KS-1800',test=TEST,product=PROD,ref=REF,
 runner='vitest` (`npx vitest run src/__tests__/ks1670-the-success-redirect-encodes-the-connection-id.test.ts` from `Blockchain/Dev/services/m365-integration`',
 rung='3-4 (test HARDENING: a weak existing source-text pin gets a mutant-killing cell; the cell is given byte-exact, the tamper is the mutant the ticket names)',
 title="m365: harden the ks1670 source-text pin so a raw connectionId carried by string concatenation goes red (KS-1800, gate 7 mutant N6; TEST-ONLY: one in-place test hunk with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 21 for Wednesday, 2026-10-30 AEDT. Secuura (m365-integration) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1800 (gate 7 finding 1791-1, Low, a disclosed test gap). The source-text pin `ks1670-the-success-redirect-encodes-the-connection-id.test.ts` finds redirects only through the needle `connectionId=${`, so a redirect built by concatenation is invisible to R1. This task adds the mutant-killing cell for N6 and two controls. Mutants N3 (an equivalent rewrite turns R2 red) and N4 are NOT addressed, and the ticket's wire-cell option is not done (the behaviour test `ks1670-the-success-redirect-keeps-a-hostile-connection-id-intact.test.ts` is the wire guard). The tamper is in `index.ts`; no file other than the test is modified.",
 tamper_line=677,
 tamper_from="    res.redirect(`${process.env.FRONTEND_URL || 'http://localhost:6882'}/admin/integrations?m365=success&connectionId=${encodeURIComponent(connectionId)}&tenant=${encodeURIComponent(connection.tenantName || '')}`);",
 tamper_to="    res.redirect(`${process.env.FRONTEND_URL || 'http://localhost:6882'}/admin/integrations?m365=success&connectionId=${encodeURIComponent(connectionId)}&tenant=${encodeURIComponent(connection.tenantName || '')}`); const rawRedirect = '/admin/integrations?m365=success&connectionId=' + connectionId; void rawRedirect;",
 statement_ok="line 677 is the one-statement success redirect; the tamper keeps it byte-for-byte (so R1, R2, C1, C2, C3 stay green: still exactly one `connectionId=${` interpolation, still encoded) and APPENDS a second statement on the same line that builds a redirect target by concatenation with the raw id; both names are declared and used (`void rawRedirect`) so the file still compiles",
 edit=(ANCHOR,CELLS),
 red=['RED KS-1670 R3 no redirect in the service carries the connection id by string concatenation'],
 what_wrong="`ks1670-the-success-redirect-encodes-the-connection-id.test.ts` reads `services/m365-integration/src/index.ts` as text. R1 only inspects interpolations that follow the literal needle `connectionId=${`, so a raw id added to a redirect by string concatenation (`'...&connectionId=' + connectionId`) is invisible to every cell: gate 7's mutant N6 survives. This task adds cell R3, which scans the non-comment lines of the source for a `connectionId=` query key closed by a quote and joined with `+`, plus controls C4 (the scan can fail on planted text, both quote styles) and C5 (it ignores a comment line; the real template redirect is still in the source).",
 where="- `services/m365-integration/src/index.ts:677` - (correct, STAYS) the success redirect line; the line the tamper edits in the checker's clone (the tamper leaves the redirect intact and appends a raw concatenated statement).\n- The test hunk adds the helper `concatenatedConnectionIdLines` and the three new cells directly after cell `control KS-1670 C3` (:52-54), inside the existing `describe`, before its closing `});`.",
 cells="- RED under the tamper: `RED KS-1670 R3` fails by assertion (`concatenatedConnectionIdLines(SRC)` returns the tampered line, not `[]`).\n- GREEN at the untouched tip: all cells, R3 included.\n- Controls C4 and C5 and the existing R1, R2, C1, C2, C3 stay green under this tamper (the tamper adds no `connectionId=${` interpolation).",
 unmeasured="- The drafter did NOT run vitest for the brief: RED-under-tamper / GREEN-at-tip is the `round.sh --control` run on this golden.\n- The scan misses a concatenation that splits the key (`'connection' + 'Id=' + id`) or builds the query with URLSearchParams: it pins the one shape the ticket names (N6), not every spelling.\n- Mutants N3 and N4 and the ticket's wire-cell options are untouched.\n- Open PRs touching m365-integration: only its package.json (read 2026-10-30), not this test or index.ts.",
 scope="**Refs KS-1800, never a close-word. Narrowing:** closes the N6 half only (concatenation). The ticket itself says whether the remainder needs a change is undecided; this does not decide it.",
)
