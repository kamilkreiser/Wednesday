import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s22common import *
P1 = 'Blockchain/Dev/services/tenant-provisioning/src/index.ts'
TP = 'Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts'
SITES = [(1, "'[provisioning] GET /api/tenants failed:'", ''), (2, "'[provisioning] GET /api/tenants/:id failed:'", ''), (3, "'[provisioning] PATCH /api/tenants/:id/status failed:'", ''),
         (4, "'[provisioning] PATCH /api/tenants/:id failed:'", ''), (5, "'[provisioning] DELETE /api/tenants/:id failed:'", ''), (6, "'[provisioning] GET /api/audit-log failed:'", '')]
TEST = '''/**
 * KS-1410 (the tenant-provisioning file of the class): the catch blocks of tenant-provisioning/src/index.ts answered 500 with the thrown text
 * as the response message (`message: message`), so a driver message or an internal host:port reached the caller. The six handlers other than
 * POST /api/tenants now log the thrown text with console.error and answer the constant message below.
 * POST /api/tenants (the key-generation path, whose 500 answer is Kam's open card secuura-ks1240-tenant-create-key-fail-answer-1028) is NOT
 * changed here and must stay as it is. Source-text guard: the module starts a server and a pool on import, so the file is read, not imported.
 */
''' + TEST_HEAD % dict(file='index.ts', const=CONST) + '''
const EXEMPT = 'POST /api/tenants';
const CHANGED = FIVE.filter((f) => f.handler !== EXEMPT);

describe('tenant-provisioning index.ts: no 500 answer carries the thrown text', () => {
  it('RED tp-500 P1 no 500 answer outside POST /api/tenants names a caught value', () => {
    expect(CHANGED.filter((f) => leaks(f.stmt)).map((f) => f.handler)).toEqual([]);
  });

  it('RED tp-500 P2 each of the six answers the constant message', () => {
    expect(CHANGED.map((f) => f.handler)).toHaveLength(6);
    expect(CHANGED.filter((f) => !f.stmt.includes("message: '" + CONSTANT + "'")).map((f) => f.handler)).toEqual([]);
  });

  it('RED tp-500 P3 each of the six logs the thrown text with console.error just before it answers', () => {
    expect(CHANGED.filter((f) => !/console\\.error\\(.*\\b(message|err)\\b/.test(f.context)).map((f) => f.handler)).toEqual([]);
  });

  it('control tp-500 C1 the scanner flags a leaking answer and passes the constant one', () => {
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } });")).toBe(true);
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'x', details: { detail: msg } } });")).toBe(true);
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: '" + CONSTANT + "' } });")).toBe(false);
  });

  it('control tp-500 C2 the file has exactly seven 500 answers and POST /api/tenants is untouched', () => {
    expect(FIVE).toHaveLength(7);
    const post = FIVE.filter((f) => f.handler === EXEMPT);
    expect(post).toHaveLength(1);
    expect(post[0].stmt).toContain('message: message');
  });

  it('control tp-500 C3 the three 400 validation answers keep their details', () => {
    expect(SRC.split("details: err.errors").length - 1).toBe(3);
  });
});
'''
S = dict(dir='ks_1410_p4_tenantprov_500_no_echo', ticket='KS-1410',
 title="tenant-provisioning index.ts: six 500 catch blocks must stop putting the thrown text in the response (KS-1410 class, remaining file) (RUNG 4, code_patch2 LOOSE: six product edits written from the contract; hunk headers dictated; one NEW vitest file given whole)",
 intro="DRAFT by Spark operator 22 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / tenant-provisioning) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1410 (28 handlers across six services put a thrown message in a 500 body; the api-gateway and transfer files were fixed, #1432 and others; tenant-provisioning and mcp-server remain). This brief covers SIX of the seven tenant-provisioning sites; the seventh (POST /api/tenants, :361) is Kam's open card and is NOT touched. RUNG 4 (looser): the product edits are described by behaviour, not given as a diff; the hunk headers and unchanged context lines are dictated. Not auth/credential code: it is the response body of the tenant list/read/update/delete/audit-log routes. No open PR touches tenant-provisioning source (the only tenant-provisioning files in the 22 open PRs are package.json and package-lock.json).",
 products=[(P1,[edit_sites(SITES)])],
 prodnote=['product, modified in place: SIX hunks, one per catch block'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 6 cells (3 red, 3 control); a source-text guard (index.ts starts a server on import)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1410-provisioning-500-never-echoes-the-thrown-text.test.ts` from `Blockchain/Dev/services/tenant-provisioning',
 tier='code_patch2', rung='4 (LOOSE: product lines written by the model, hunk headers dictated; new test given whole)',
 pins='''# code_patch2: tenant-provisioning index.ts (6 hunks) + a NEW vitest file; ref = ks1364 (same service, shape only); line = the first changed line in the product.
tier=code_patch2
ref=Blockchain/Dev/services/tenant-provisioning/src/__tests__/ks1364-platform-tenant-patch-body-required.test.ts
line=384
ctx=65536
started_ok=KS-1410_is_In_Progress_for_its_owner_but_its_api-gateway_and_transfer_passes_are_merged;_tenant-provisioning_source_is_in_no_open_PR_(read_2026-10-30,_22_PRs);_no_live_seat_holds_the_file;_the_operator_did_not_check_other_live_lanes
''',
 wrong="In `services/tenant-provisioning/src/index.ts`, six route handlers end in a `catch` that computes `const message = err instanceof Error ? err.message : String(err);` and answers `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: message } })`, so the thrown error's own text (a driver message or an internal host:port) reaches the caller. The fix, at each of the six: keep the `const message = ...` line; immediately after it, log the thrown text server-side with `console.error('[provisioning] <METHOD> <route> failed:', message);` (the text names the route as in the list below; the log text is yours to word, but it must start with `[provisioning]`, be one `console.error(` call and pass `message`); and answer the constant `{ success: false, error: { code: 'INTERNAL_ERROR', message: 'An unexpected error occurred' } }` (that exact string, no `details` key). The status 500, the code `INTERNAL_ERROR` and the envelope shape stay.",
 where="The six `res.status(500).json(...)` lines (file order, as read at the tip): `:385` in `GET /api/tenants`; `:424` in `GET /api/tenants/:id`; `:454` in `PATCH /api/tenants/:id/status`; `:515` in `PATCH /api/tenants/:id`; `:576` in `DELETE /api/tenants/:id`; `:596` in `GET /api/audit-log`. Each is the second line of a two-line pair: the `const message` line then the `res.status(500)` line.\n- **NOT TO TOUCH:** `:361`, the same two-line pair at the end of `POST /api/tenants` (:219), whose 500 answer belongs to Kam's open card secuura-ks1240-tenant-create-key-fail-answer-1028; the 400 branches (`details: err.errors`, :339 :381 :511); every `console.warn` and `console.error` already in the file.",
 exactnote="", loose="The product edits are described by behaviour in `## What is wrong` and `## Where`; no diff and no `+` line is given for them. Write them yourself: minimal, only what those two sections require.\n\n",
 donot="**Do NOT touch** `POST /api/tenants` (:219-:362), the 400 validation branches, any other line of `index.ts`, the existing tests, or any other file.",
 testnote2="The test section is a NEW vitest file given whole. The `+` lines are byte-exact. It reads index.ts as text; it has no top-level await.",
 red=['RED tp-500 P1','RED tp-500 P2','RED tp-500 P3'],
 cells="- RED `P1` (no 500 answer outside POST /api/tenants names a caught value: at the tip six do), `P2` (each of the six answers the constant message: at the tip none does), `P3` (each logs with console.error just before: at the tip none does): all fail by assertion at the tip and pass after the edit.\n- GREEN at the tip and after: `C1` (the scanner flags a leak and passes the constant answer), `C2` (seven 500 answers in the file; POST /api/tenants still reads `message: message`), `C3` (three `details: err.errors` 400 branches remain).",
 premises="- The seven `status(500).json` lines are at :361 :385 :424 :454 :515 :576 :596, each preceded by `    const message = err instanceof Error ? err.message : String(err);` (read at the tip by script; the golden is generated from the tree at the tip and asserts each pair).\n- `grep details: err.errors` finds exactly 3 lines (:339 :381 :511) at the tip.\n- The service uses `console.warn`/`console.error` for its logs (:127 :297 :326 :349 :358), no logger module.\n- No existing test reads these 500 bodies (the existing tests in `__tests__/` are an OpenAPI pin, a param guard, a timeout test and a metering test; none boots index.ts).",
 unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Which errors reach these handlers in production is not measured (a source reading, as in KS-1410).\n- The gateway in front may redact a 5xx already (api-gateway errorHandler does for its own errors; whether it rewrites an UPSTREAM 500 body is not measured here).",
 scope="**The six tenant-provisioning 500 answers only.** Not a close of KS-1410 (the POST /api/tenants site and the mcp-server file remain); link as 'Refs KS-1410'.",
)
