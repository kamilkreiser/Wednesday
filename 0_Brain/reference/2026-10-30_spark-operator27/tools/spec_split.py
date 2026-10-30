import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s22common import *
import spec_mcp as S0m
S0 = S0m.S
P1 = S0m.P1
NAME = {1:'POST /register',2:'POST /register-batch',3:'POST /verify',4:'POST /verify-batch',5:'GET /documents',6:'GET /workflow/:id',7:'GET /connector',8:'GET /policy',9:'POST /generate-package'}
LINE = {1:77,2:111,3:135,4:170,5:183,6:193,7:203,8:213,9:267}
HEAD = '''/**
 * KS-1410 (the mcp-server file of the class, part @@P@@ of 2): the catch blocks of mcp-server/src/http-server.ts answered 500 with the thrown text in the
 * response (`message: message`, and `error: message` on POST /verify), so a driver message, a file-system error naming a server path or an
 * internal host:port reached the caller. The @@W@@ handlers named in MINE below now log the thrown text with console.error and answer the
 * constant message. The other handlers of the file are covered by the other part; POST /hash (KS-1214's route) is NOT changed and must stay as it is.
 * Source-text guard: the module binds a port and runs a production guard on import, so the file is read, not imported.
 */
'''
BODY = '''
const EXEMPT = 'POST /hash';
const MINE = [@@MINE@@];
const CHANGED = FIVE.filter((f) => MINE.includes(f.handler));

describe('mcp-server http-server.ts part @@P@@: no 500 answer of these handlers carries the thrown text', () => {
  it('RED mcp-500@@p@@ P1 no 500 answer of the @@W@@ handlers names a caught value', () => {
    expect(CHANGED).toHaveLength(MINE.length);
    expect(CHANGED.filter((f) => leaks(f.stmt)).map((f) => f.handler)).toEqual([]);
  });

  it('RED mcp-500@@p@@ P2 each of the @@W@@ answers the constant message', () => {
    expect(CHANGED.filter((f) => !f.stmt.includes("'" + CONSTANT + "'")).map((f) => f.handler)).toEqual([]);
  });

  it('RED mcp-500@@p@@ P3 each of the @@W@@ logs the thrown text with console.error just before it answers', () => {
    expect(CHANGED.filter((f) => !/console\\.error\\(.*\\b(message|err)\\b/.test(f.context)).map((f) => f.handler)).toEqual([]);
  });

  it('control mcp-500@@p@@ C1 the scanner flags a leaking answer and passes the constant one', () => {
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });")).toBe(true);
    expect(leaks("res.status(500).json({ verified: false, error: message });")).toBe(true);
    expect(leaks("res.status(500).json({ verified: false, error: '" + CONSTANT + "' });")).toBe(false);
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: '" + CONSTANT + "' } });")).toBe(false);
  });

  it('control mcp-500@@p@@ C2 the file has exactly ten 500 answers and POST /hash is untouched', () => {
    expect(FIVE).toHaveLength(10);
    const hash = FIVE.filter((f) => f.handler === EXEMPT);
    expect(hash).toHaveLength(1);
    expect(hash[0].stmt).toContain('message: message');
  });

  it('control mcp-500@@p@@ C3 the two per-item results of the batch routes are not touched', () => {
    expect(SRC).toContain('results.push({ success: false, title: doc.title, error: message });');
    expect(SRC).toContain('results.push({ verified: false, error: message });');
  });

  it('control mcp-500@@p@@ C4 the 400 refusals keep their messages', () => {
    expect(SRC).toContain("message: 'Provide documentId, contentHash, or filePath'");
    expect(SRC).toContain("message: 'documents array is required'");
  });
});
'''
def spec(part):
    ks = [1,2,3,4,5] if part == 'a' else [6,7,8,9]
    names = [NAME[k] for k in ks]
    sites = [s for s in S0m.SITES if s[0] in ks]
    W = {4:'four',5:'five'}[len(ks)]
    other = [NAME[k] for k in range(1,10) if k not in ks]
    tname = 'ks1410-mcp-http-500-part-%s-never-echoes-the-thrown-text.test.ts' % part
    TP = 'Blockchain/Dev/services/mcp-server/src/__tests__/' + tname
    mine = ', '.join("'%s'" % x for x in names)
    sub = lambda t: t.replace('@@P@@', part.upper()).replace('@@p@@', part).replace('@@W@@', W).replace('@@MINE@@', mine)
    TEST = sub(HEAD) + TEST_HEAD % dict(file='http-server.ts', const=CONST) + sub(BODY)
    wl = ', '.join('`%s` (`:%d`)' % (NAME[k], LINE[k]) for k in ks)
    ol = ', '.join('`%s`' % x for x in other)
    D = 'ks_1410_p5%s_mcp_http_500_no_echo_%s' % (part, 'register_to_documents' if part == 'a' else 'workflow_to_generate_package')
    S = dict(S0)
    S.update(dict(dir=D, ticket='KS-1410',
     title="mcp-server http-server.ts part %s of 2: %s 500 catch blocks must stop putting the thrown text in the response (KS-1410 class) (RUNG 4, code_patch2 LOOSE: %s product edits written from the contract; hunk headers and a per-hunk instruction dictated; one NEW vitest file given whole)" % (part.upper(), W, W),
     intro="DRAFT by Spark operator 23 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / mcp-server HTTP mirror) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1410 (the mcp-server/src/http-server.ts item: ten 500 sites). THIS IS A SPLIT (Wednesday's ruling): the nine-hunk brief ks_1410_p5 FAILED twice at A2 because the model wrote the replaced line as a context line in 8 of 9 hunks; it is cut into two NEW briefs of at most five hunks each (a new brief, a new counter). This is part %s: %s handlers (%s). The other part covers: %s. POST /hash (:62) is left alone (KS-1214 owns that route). RUNG 4 (looser): the product edits are described by behaviour, not given as a diff; the hunk headers, the unchanged context lines and a per-hunk instruction are dictated. The ks_1530_p1 PASS (a 400 guard in POST /generate-package, :233-239) edits the same file in a different region; the hunks are disjoint. No open PR touches mcp-server." % (part.upper(), W, ', '.join(names), ', '.join(other)),
     products=[(P1,[edit_sites(sites)])],
     prodnote=['product, modified in place: %s hunks, one per catch block' % W.upper()],
     tests=[dict(path=TP,content=TEST)],
     testnote=['NEW file, vitest, given in full below; 7 cells (3 red, 4 control); a source-text guard (http-server.ts binds a port on import)'],
     runner='vitest` (`npx vitest run src/__tests__/%s` from `Blockchain/Dev/services/mcp-server' % tname,
     pins=S0['pins'].replace('(9 hunks)', '(%s hunks, part %s)' % (len(ks), part.upper())).replace('line=77', 'line=%d' % LINE[ks[0]]),
     wrong="In `services/mcp-server/src/http-server.ts`, route handlers end in a `catch` that computes `const message = err instanceof Error ? err.message : String(err);` and answers 500 with that text: as `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } })`, and `POST /verify` as `res.status(500).json({ verified: false, error: message })`. So the thrown error's own text (a driver message, a file-system error naming a server path, an internal host:port) reaches the caller. THIS BRIEF changes only these %s handlers: %s. The fix, at each: keep the `const message = ...` line; log the thrown text server-side with ONE `console.error('[mcp-http] <METHOD> <route> failed:', message);` call (the text is yours to word, it must start with `[mcp-http]`, pass `message`, and sit directly before the response statement%s); and answer the constant: the envelopes get `message: 'An unexpected error occurred'` (that exact string)%s. Status 500, code `INTERNAL_ERROR` and the envelope shapes stay. Every other handler (%s) stays exactly as it is in this brief." % (W, wl, ', or before the `if (!res.headersSent) {` line for POST /generate-package' if part=='b' else '', ", and POST /verify gets `{ verified: false, error: 'An unexpected error occurred' }`" if part=='a' else '', ol),
     where="The %s `res.status(500).json(...)` lines changed by this brief (file order, as read at the tip): %s. Each follows a `const message` line%s.\n- **NOT TO TOUCH:** every 500 line of the other part (%s); `:62`, the same pair at the end of `POST /hash` (:41), which belongs to KS-1214; the per-item `results.push(... error: message)` lines at :104 and :163; the 400 refusals (including the generate-package guard at :229-239); every other line." % (W, wl, ' (for POST /generate-package the `const message` is at :265 and the 500 line sits inside `if (!res.headersSent) {` at :266)' if part=='b' else '', ol),
     donot="**Do NOT touch** `POST /hash` (:41-:63), the two `results.push` lines, the other part's handlers (%s), any other line of `http-server.ts`, the existing tests, or any other file." % ol,
     red=['RED mcp-500%s P1' % part,'RED mcp-500%s P2' % part,'RED mcp-500%s P3' % part],
     cells="- RED `P1` (no 500 answer of the %s handlers names a caught value: at the tip all %s do), `P2` (each answers the constant: none does), `P3` (each logs with console.error just before it answers: none does): all fail by assertion at the tip and pass after the edit.\n- GREEN at the tip and after: `C1` (scanner positive and negative controls), `C2` (ten 500 answers; POST /hash still reads `message: message`), `C3` (the two per-item results lines unchanged), `C4` (two 400 messages unchanged). No cell asserts anything about the other part's handlers, so this part passes whether or not the other part is applied." % (W, W),
     premises="- The ten `status(500).json` lines are at :62 :77 :111 :135 :170 :183 :193 :203 :213 :267; each preceded by a `const message = err instanceof Error ? err.message : String(err);` line (read at the tip by script; the golden asserts each).\n- :135 is `res.status(500).json({ verified: false, error: message });`; :267 is indented 6 under `if (!res.headersSent) {` at :266, and the `const message` line is at :265.\n- The per-item lines `results.push({ success: false, title: doc.title, error: message });` (:104) and `results.push({ verified: false, error: message });` (:163) exist at the tip.\n- The file already writes to stderr (`process.stderr.write` near the end of the file); `console.error` also goes to stderr.\n- Round history this split answers: ks_1410_p5 and its rebrief (nine hunks) both FAILED A2: the model wrote the new `res.status(500)` line as an unchanged context line and never emitted the `-` line, in 8 of 9 hunks; the rebrief's general paragraph moved only the one hunk it described separately.",
     unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Whether anything consumes the old `error` string of POST /verify (ChatGPT Actions clients) is not measured.\n- Whether the ks_1530_p1 PASS and this one apply together in either order is not measured (disjoint hunks, :233-239 against %s).\n- Whether a per-hunk instruction fixes the wrong-side slip is exactly what this brief measures." % ('the hunks here' if part=='a' else ':266-267'),
     scope="**The %s mcp-server http-server.ts 500 answers named above only.** Not a close of KS-1410; link as 'Refs KS-1410'.%s" % (W, " The raise note must say that POST /verify's `error` string is now the constant (a response-shape text change)." if part=='a' else ''),
    ))
    return S
