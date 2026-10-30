import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s22common import *
import spec_mcp as S0m
import spec_split as SS
S0 = S0m.S
NAME, LINE, HEAD, BODY = SS.NAME, SS.LINE, SS.HEAD, SS.BODY
N = int(os.environ['CAL_N'])
WORD = {7: 'seven', 8: 'eight', 9: 'nine'}
def build():
    ks = list(range(1, N + 1))
    names = [NAME[k] for k in ks]
    sites = [s for s in S0m.SITES if s[0] in ks]
    W = WORD[N]
    other = [NAME[k] for k in range(1, 10) if k not in ks]
    part = '%dh' % N
    tname = 'ks1410-mcp-http-500-cal%d-never-echoes-the-thrown-text.test.ts' % N
    TP = 'Blockchain/Dev/services/mcp-server/src/__tests__/' + tname
    mine = ', '.join("'%s'" % x for x in names)
    sub = lambda t: t.replace('@@P@@', part.upper()).replace('@@p@@', part).replace('@@W@@', W).replace('@@MINE@@', mine)
    head = sub(HEAD).replace('part %s of 2' % part.upper(), 'calibration brief, %s hunks' % W)
    TEST = head + TEST_HEAD % dict(file='http-server.ts', const=CONST) + sub(BODY)
    wl = ', '.join('`%s` (`:%d`)' % (NAME[k], LINE[k]) for k in ks)
    ol = ', '.join('`%s`' % x for x in other) or '`POST /hash` only'
    D = 'ks_1410_cal%d_mcp_http_500_no_echo' % N
    S = dict(S0)
    S.update(dict(dir=D, ticket='KS-1410',
     title="mcp-server http-server.ts: %s 500 catch blocks must stop putting the thrown text in the response (KS-1410 class) (RUNG 4, code_patch2 LOOSE, CALIBRATION at %d hunks: %s product edits written from the contract; hunk headers and a per-hunk instruction dictated; one NEW vitest file given whole)" % (W, N, W),
     intro="DRAFT by Spark operator 27 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / mcp-server HTTP mirror) only. THIS IS A CALIBRATION BRIEF, NOT A CANDIDATE: it measures at which hunk count (between 6 and 9) the rung-4 loose shape with per-hunk skeletons stops passing. Its hunks overlap the HELD ks_1410_p5a/p5b patches (already held for raising); its patch is NOT to be held or raised. Origin: KS-1410 (the mcp-server/src/http-server.ts item: ten 500 sites). It covers %s handlers (%s). Not covered: %s. POST /hash (:62) is left alone (KS-1214 owns that route). RUNG 4 (looser): the product edits are described by behaviour, not given as a diff; the hunk headers, the unchanged context lines and a per-hunk instruction are dictated." % (W, ', '.join(names), ', '.join(other)),
     products=[(SS.P1,[edit_sites(sites)])],
     prodnote=['product, modified in place: %s hunks, one per catch block' % W.upper()],
     tests=[dict(path=TP,content=TEST)],
     testnote=['NEW file, vitest, given in full below; 7 cells (3 red, 4 control); a source-text guard (http-server.ts binds a port on import)'],
     runner='vitest` (`npx vitest run src/__tests__/%s` from `Blockchain/Dev/services/mcp-server' % tname,
     pins=S0['pins'].replace('(9 hunks)', '(%s hunks, calibration)' % N),
     wrong="In `services/mcp-server/src/http-server.ts`, route handlers end in a `catch` that computes `const message = err instanceof Error ? err.message : String(err);` and answers 500 with that text: as `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } })`, and `POST /verify` as `res.status(500).json({ verified: false, error: message })`. So the thrown error's own text (a driver message, a file-system error naming a server path, an internal host:port) reaches the caller. THIS BRIEF changes only these %s handlers: %s. The fix, at each: keep the `const message = ...` line; log the thrown text server-side with ONE `console.error('[mcp-http] <METHOD> <route> failed:', message);` call (the text is yours to word, it must start with `[mcp-http]`, pass `message`, and sit directly before the response statement%s); and answer the constant: the envelopes get `message: 'An unexpected error occurred'` (that exact string), and POST /verify gets `{ verified: false, error: 'An unexpected error occurred' }`. Status 500, code `INTERNAL_ERROR` and the envelope shapes stay. Every other handler (%s) stays exactly as it is in this brief." % (W, wl, (', or before the `if (!res.headersSent) {` line for POST /generate-package' if N==9 else ''), ol),
     where="The %s `res.status(500).json(...)` lines changed by this brief (file order, as read at the tip): %s. Each follows a `const message` line.\n- **NOT TO TOUCH:** every 500 line of the handlers not named (%s); `:62`, the same pair at the end of `POST /hash` (:41), which belongs to KS-1214; the per-item `results.push(... error: message)` lines at :104 and :163; the 400 refusals; every other line." % (W, wl, ol),
     donot="**Do NOT touch** `POST /hash` (:41-:63), the two `results.push` lines, the handlers not named (%s), any other line of `http-server.ts`, the existing tests, or any other file." % ol,
     red=['RED mcp-500%s P1' % part,'RED mcp-500%s P2' % part,'RED mcp-500%s P3' % part],
     cells="- RED `P1` (no 500 answer of the %s handlers names a caught value: at the tip all %s do), `P2` (each answers the constant: none does), `P3` (each logs with console.error just before it answers: none does): all fail by assertion at the tip and pass after the edit.\n- GREEN at the tip and after: `C1` (scanner positive and negative controls), `C2` (ten 500 answers; POST /hash still reads `message: message`), `C3` (the two per-item results lines unchanged), `C4` (two 400 messages unchanged). No cell asserts anything about the handlers not named." % (W, W),
     premises="- The ten `status(500).json` lines are at :62 :77 :111 :135 :170 :183 :193 :203 :213 :267; each preceded by a `const message = err instanceof Error ? err.message : String(err);` line (read at the tip by script; the golden asserts each).\n- :135 is `res.status(500).json({ verified: false, error: message });`.\n- The per-item lines `results.push({ success: false, title: doc.title, error: message });` (:104) and `results.push({ verified: false, error: message });` (:163) exist at the tip.\n- The file already writes to stderr (`process.stderr.write` near the end of the file); `console.error` also goes to stderr.\n- Calibration history: the 9-hunk ks_1410_p5 failed A2 twice; the 5-hunk p5a and 4-hunk p5b (per-hunk skeletons) passed 7/7. This brief measures the count between.",
     unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Whether an open PR touches mcp-server today was not re-checked by this operator (calibration only; nothing is raised).\n- Whether the model passes at this hunk count is exactly what this brief measures.",
     scope="**The %s mcp-server http-server.ts 500 answers named above only. CALIBRATION: not held, not raised.** Link, if ever, as 'Refs KS-1410'." % W,
    ))
    return S
S = build()
