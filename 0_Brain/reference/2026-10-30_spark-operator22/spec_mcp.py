import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s22common import *
P1 = 'Blockchain/Dev/services/mcp-server/src/http-server.ts'
TP = 'Blockchain/Dev/services/mcp-server/src/__tests__/ks1410-mcp-http-500-never-echoes-the-thrown-text.test.ts'
# file order of the 10 status(500) lines: 0 /hash (NOT touched), 1 /register, 2 /register-batch, 3 /verify (non-envelope), 4 /verify-batch, 5 /documents, 6 /workflow/:id, 7 /connector, 8 /policy, 9 /generate-package (inside if(!res.headersSent))
SITES = [(1, "'[mcp-http] POST /register failed:'", ''), (2, "'[mcp-http] POST /register-batch failed:'", ''), (3, "'[mcp-http] POST /verify failed:'", 'verified'),
         (4, "'[mcp-http] POST /verify-batch failed:'", ''), (5, "'[mcp-http] GET /documents failed:'", ''), (6, "'[mcp-http] GET /workflow/:id failed:'", ''),
         (7, "'[mcp-http] GET /connector failed:'", ''), (8, "'[mcp-http] GET /policy failed:'", ''), (9, "'[mcp-http] POST /generate-package failed:'", 'headers')]
TEST = '''/**
 * KS-1410 (the mcp-server file of the class): the catch blocks of mcp-server/src/http-server.ts answered 500 with the thrown text in the
 * response (`message: message`, and `error: message` on POST /verify), so a driver message, a file-system error naming a server path or an
 * internal host:port reached the caller. The nine handlers other than POST /hash now log the thrown text with console.error and answer the
 * constant message below. POST /hash (KS-1214's route, an authentication question) is NOT changed here and must stay as it is.
 * Source-text guard: the module binds a port and runs a production guard on import, so the file is read, not imported.
 */
''' + TEST_HEAD % dict(file='http-server.ts', const=CONST) + '''
const EXEMPT = 'POST /hash';
const CHANGED = FIVE.filter((f) => f.handler !== EXEMPT);

describe('mcp-server http-server.ts: no 500 answer carries the thrown text', () => {
  it('RED mcp-500 P1 no 500 answer outside POST /hash names a caught value', () => {
    expect(CHANGED.filter((f) => leaks(f.stmt)).map((f) => f.handler)).toEqual([]);
  });

  it('RED mcp-500 P2 each of the nine answers the constant message', () => {
    expect(CHANGED.map((f) => f.handler)).toHaveLength(9);
    expect(CHANGED.filter((f) => !f.stmt.includes("'" + CONSTANT + "'")).map((f) => f.handler)).toEqual([]);
  });

  it('RED mcp-500 P3 each of the nine logs the thrown text with console.error just before it answers', () => {
    expect(CHANGED.filter((f) => !/console\\.error\\(.*\\b(message|err)\\b/.test(f.context)).map((f) => f.handler)).toEqual([]);
  });

  it('control mcp-500 C1 the scanner flags a leaking answer and passes the constant one', () => {
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });")).toBe(true);
    expect(leaks("res.status(500).json({ verified: false, error: message });")).toBe(true);
    expect(leaks("res.status(500).json({ verified: false, error: '" + CONSTANT + "' });")).toBe(false);
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: '" + CONSTANT + "' } });")).toBe(false);
  });

  it('control mcp-500 C2 the file has exactly ten 500 answers and POST /hash is untouched', () => {
    expect(FIVE).toHaveLength(10);
    const hash = FIVE.filter((f) => f.handler === EXEMPT);
    expect(hash).toHaveLength(1);
    expect(hash[0].stmt).toContain('message: message');
  });

  it('control mcp-500 C3 the two per-item results of the batch routes are not touched', () => {
    expect(SRC).toContain('results.push({ success: false, title: doc.title, error: message });');
    expect(SRC).toContain('results.push({ verified: false, error: message });');
  });

  it('control mcp-500 C4 the 400 refusals keep their messages', () => {
    expect(SRC).toContain("message: 'Provide documentId, contentHash, or filePath'");
    expect(SRC).toContain("message: 'documents array is required'");
  });
});
'''
S = dict(dir='ks_1410_p5_mcp_http_500_no_echo', ticket='KS-1410',
 title="mcp-server http-server.ts: nine 500 catch blocks must stop putting the thrown text in the response (KS-1410 class, remaining file) (RUNG 4, code_patch2 LOOSE: nine product edits written from the contract; hunk headers dictated; one NEW vitest file given whole)",
 intro="DRAFT by Spark operator 22 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / mcp-server HTTP mirror) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1410 (the mcp-server/src/http-server.ts item: ten 500 sites). This brief covers NINE of the ten; POST /hash (:62) is left alone (KS-1214 owns that route). RUNG 4 (looser): the product edits are described by behaviour, not given as a diff; the hunk headers and unchanged context lines are dictated. The ks_1530_p1 PASS (a 400 guard in POST /generate-package, :233-239) edits the same file in a different region; the hunks are disjoint. No open PR touches mcp-server (the only mcp-server file in the 22 open PRs: none).",
 products=[(P1,[edit_sites(SITES)])],
 prodnote=['product, modified in place: NINE hunks, one per catch block'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 7 cells (3 red, 4 control); a source-text guard (http-server.ts binds a port on import)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1410-mcp-http-500-never-echoes-the-thrown-text.test.ts` from `Blockchain/Dev/services/mcp-server',
 tier='code_patch2', rung='4 (LOOSE: product lines written by the model, hunk headers dictated; new test given whole)',
 pins='''# code_patch2: mcp-server http-server.ts (9 hunks) + a NEW vitest file; ref = ks1232 (same service, shape only); line = the first changed line in the product.
tier=code_patch2
ref=Blockchain/Dev/services/mcp-server/src/__tests__/ks1232-connector-info-relay.test.ts
line=77
ctx=65536
started_ok=KS-1410_is_In_Progress_for_its_owner_but_its_api-gateway_and_transfer_passes_are_merged;_mcp-server_source_is_in_no_open_PR_(read_2026-10-30,_22_PRs);_no_live_seat_holds_the_file;_the_operator_did_not_check_other_live_lanes
''',
 wrong="In `services/mcp-server/src/http-server.ts`, nine route handlers end in a `catch` that computes `const message = err instanceof Error ? err.message : String(err);` and answers 500 with that text: eight as `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } })` and `POST /verify` as `res.status(500).json({ verified: false, error: message })`. So the thrown error's own text (a driver message, a file-system error naming a server path, an internal host:port) reaches the caller. The fix, at each of the nine: keep the `const message = ...` line; log the thrown text server-side with ONE `console.error('[mcp-http] <METHOD> <route> failed:', message);` call (the text is yours to word, it must start with `[mcp-http]`, pass `message`, and sit directly before the response statement, or before the `if (!res.headersSent) {` line for POST /generate-package); and answer the constant: the eight envelopes get `message: 'An unexpected error occurred'` (that exact string), POST /verify gets `{ verified: false, error: 'An unexpected error occurred' }`. Status 500, code `INTERNAL_ERROR` and the envelope shapes stay.",
 where="The nine `res.status(500).json(...)` lines (file order, as read at the tip): `:77` in `POST /register`; `:111` in `POST /register-batch`; `:135` in `POST /verify` (the non-envelope one); `:170` in `POST /verify-batch`; `:183` in `GET /documents`; `:193` in `GET /workflow/:id`; `:203` in `GET /connector`; `:213` in `GET /policy`; `:267` in `POST /generate-package`, inside `if (!res.headersSent) {` (:266). Each follows a `const message` line.\n- **NOT TO TOUCH:** `:62`, the same pair at the end of `POST /hash` (:41), which belongs to KS-1214; the per-item `results.push(... error: message)` lines at :104 and :163 (they land in a 200 body and are a separate decision); the 400 refusals; every other line.",
 exactnote="", loose="The product edits are described by behaviour in `## What is wrong` and `## Where`; no diff and no `+` line is given for them. Write them yourself: minimal, only what those two sections require.\n\n",
 donot="**Do NOT touch** `POST /hash` (:41-:63), the two `results.push` lines, any other line of `http-server.ts`, the existing tests, or any other file.",
 testnote2="The test section is a NEW vitest file given whole. The `+` lines are byte-exact. It reads http-server.ts as text; it has no top-level await.",
 red=['RED mcp-500 P1','RED mcp-500 P2','RED mcp-500 P3'],
 cells="- RED `P1` (no 500 answer outside POST /hash names a caught value: at the tip nine do), `P2` (each of the nine answers the constant: none does), `P3` (each logs with console.error just before it answers: none does): all fail by assertion at the tip and pass after the edit.\n- GREEN at the tip and after: `C1` (scanner positive and negative controls), `C2` (ten 500 answers; POST /hash still reads `message: message`), `C3` (the two per-item results lines unchanged), `C4` (two 400 messages unchanged).",
 premises="- The ten `status(500).json` lines are at :62 :77 :111 :135 :170 :183 :193 :203 :213 :267; each preceded by a `const message = err instanceof Error ? err.message : String(err);` line (read at the tip by script; the golden asserts each).\n- :135 is `res.status(500).json({ verified: false, error: message });`; :267 is indented 6 under `if (!res.headersSent) {` at :266, and the `const message` line is at :265.\n- The per-item lines `results.push({ success: false, title: doc.title, error: message });` (:104) and `results.push({ verified: false, error: message });` (:163) exist at the tip.\n- The file already writes to stderr (`process.stderr.write` near the end of the file); `console.error` also goes to stderr.",
 unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Whether anything consumes the old `error` string of POST /verify (ChatGPT Actions clients) is not measured.\n- Whether the ks_1530_p1 PASS and this one apply together in either order is not measured (disjoint hunks, :233-239 against :266-267).",
 scope="**The nine mcp-server http-server.ts 500 answers only.** Not a close of KS-1410; link as 'Refs KS-1410'. The raise note must say that POST /verify's `error` string is now the constant (a response-shape text change).",
)
