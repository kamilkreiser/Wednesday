import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s22common import *
P1 = 'Blockchain/Dev/services/api-gateway/src/routes/platform.ts'
TP = 'Blockchain/Dev/services/api-gateway/src/__tests__/ks1410-platform-templates-500-never-echoes-the-thrown-text.test.ts'
OLD1 = "      } catch (err: any) { res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch templates', details: { detail: err?.message } } }); }\n"
NEW1 = ("      } catch (err: any) {\n"
"        console.error('[Templates] Failed to fetch templates:', err?.message);\n"
"        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch templates' } });\n"
"      }\n")
OLD2 = "        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed', details: { detail: msg } } });\n"
NEW2 = "        res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed' } });\n"
TEST = '''/**
 * KS-1410 class (api-gateway routes/platform.ts): two catch blocks answered 500 with the thrown text in `details.detail`: the platform
 * templates read (`Failed to fetch templates`, `err?.message`) and the clone-to-tenant route (`Clone failed`, `msg`). The sibling 500s in
 * the same file (a bare `catch` at the second templates read, and `Document lookup failed`) already answer a constant body with no details.
 * The fix: the templates catch logs the thrown text with console.error and answers the constant body; the clone catch (which already logs
 * `[Clone] Failed:`) just drops `details`. Source-text guard: createPlatformRoutes needs two pools and a wallet, so the file is read, not driven.
 */
''' + TEST_HEAD % dict(file='routes/platform.ts', const=CONST) + '''
describe('api-gateway platform.ts: no 500 answer carries the thrown text', () => {
  it('RED plat-500 P1 no 500 answer in the file names a caught value or carries details', () => {
    expect(FIVE.filter((f) => leaks(f.stmt)).map((f) => f.line > 0 && f.stmt.slice(0, 90))).toEqual([]);
  });

  it('RED plat-500 P2 the templates catch logs the thrown text with console.error just before it answers', () => {
    const first = FIVE.filter((f) => f.stmt.includes("'Failed to fetch templates'"))[0];
    expect(first).toBeDefined();
    expect(first.context).toMatch(/console\\.error\\(.*err/);
  });

  it('control plat-500 C1 the scanner flags a details leak and passes the constant bodies', () => {
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed', details: { detail: msg } } });")).toBe(true);
    expect(leaks("res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Clone failed' } });")).toBe(false);
  });

  it('control plat-500 C2 the file keeps its four 500 answers with their own messages', () => {
    expect(FIVE).toHaveLength(4);
    expect(FIVE.filter((f) => f.stmt.includes("message: 'Failed to fetch templates'"))).toHaveLength(2);
    expect(FIVE.filter((f) => f.stmt.includes("message: 'Clone failed'"))).toHaveLength(1);
    expect(FIVE.filter((f) => f.stmt.includes("message: 'Document lookup failed'"))).toHaveLength(1);
  });

  it('control plat-500 C3 the clone catch still logs the thrown text', () => {
    expect(SRC).toContain("console.error('[Clone] Failed:', msg);");
  });
});
'''

# harness quirk (IMPROVEMENTS row, op22): the A4 declaration-splice heuristic reads the identifier `router` inside a regex literal as an undeclared use and splices `let router: Router;` from the ref, which then fails the enrolled test type-check (TS2304 Router). Build the pattern from a string instead.
_old = "/^\\s*(?:app|router)\\.(get|post|put|patch|delete)\\(\\s*'([^']+)'/.exec(lines[j])"
_new = "new RegExp('^\\\\s*(?:app|rout' + 'er)\\\\.(get|post|put|patch|delete)\\\\(\\\\s*\\'([^\\']+)\\'').exec(lines[j])"
assert TEST.count(_old) == 1, TEST.count(_old)
TEST = TEST.replace(_old, _new)
# the api-gateway test type-check enrols noUnusedLocals: this file never reads CONSTANT, so drop it (TS6133 caught by the ks1090 baseline test at control r2)
assert TEST.count("const CONSTANT = 'An unexpected error occurred';\n") == 1
TEST = TEST.replace("const CONSTANT = 'An unexpected error occurred';\n", '')
S = dict(dir='ks_1410_p6_platform_templates_500_no_details', ticket='KS-1410',
 title="api-gateway routes/platform.ts: the templates read and the clone-to-tenant catch must stop putting the thrown text in a 500 body (KS-1410 class) (RUNG 4, code_patch2 LOOSE: two product edits written from the contract; hunk headers dictated; one NEW vitest file given whole)",
 intro="DRAFT by Spark operator 22 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / api-gateway) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: a census of `details: ... err.message` / `msg` echoes across services/* at the tip (the KS-1791 / KS-1410 class); platform.ts :994 and :1091 are two sites KS-1410's list (six files) does not name. Board search 2026-10-30 for 'Clone failed', 'detail: msg', 'platform.ts': no ticket covers these two sites. RUNG 4 (looser): the product edits are described by behaviour, not given as a diff; the hunk headers and unchanged context lines are dictated. No open PR touches api-gateway source (the only api-gateway file in the 22 open PRs is package.json).",
 products=[(P1,[(OLD1,NEW1),(OLD2,NEW2)])],
 prodnote=['product, modified in place: TWO hunks, the templates catch and the clone-to-tenant 500'],
 tests=[dict(path=TP,content=TEST)],
 testnote=['NEW file, vitest, given in full below; 5 cells (2 red, 3 control); a source-text guard'],
 runner='vitest` (`npx vitest run src/__tests__/ks1410-platform-templates-500-never-echoes-the-thrown-text.test.ts` from `Blockchain/Dev/services/api-gateway',
 tier='code_patch2', rung='4 (LOOSE: product lines written by the model, hunk headers dictated; new test given whole)',
 pins='''# code_patch2: api-gateway routes/platform.ts (2 hunks) + a NEW vitest file; ref = ks1196 (api-gateway vitest, shape only); line = the first changed line in the product.
tier=code_patch2
ref=Blockchain/Dev/services/api-gateway/src/__tests__/ks1196-admin-post-api-admin-document-types.test.ts
line=994
ctx=65536
started_ok=KS-1410_is_In_Progress_for_its_owner_but_its_api-gateway_passes_are_merged_(#1432);_these_two_platform.ts_sites_are_a_census_finding_of_the_same_class;_platform.ts_is_in_no_open_PR_(read_2026-10-30,_22_PRs);_no_live_seat_holds_the_file;_the_operator_did_not_check_other_live_lanes
''',
 wrong="In `services/api-gateway/src/routes/platform.ts`, two handlers answer 500 with the thrown error's text in `error.details.detail`: (1) the platform templates read (`Platform Templates` section, `catch (err: any) { res.status(500).json({ ..., message: 'Failed to fetch templates', details: { detail: err?.message } } }); }`, one line at :994) and (2) `POST /api/platform/templates/clone-to-tenant` (`... message: 'Clone failed', details: { detail: msg } ...`, :1091), so a driver message or an internal host:port reaches the caller. The fix: (1) turn the one-line catch into a block that first logs the thrown text with ONE `console.error('[Templates] Failed to fetch templates:', err?.message);` call (this file's idiom, see :885 and :1090) and then answers the same 500 envelope WITHOUT the `details` key; (2) drop `details: { detail: msg }` from the clone 500 and change nothing else (the line above it, `console.error('[Clone] Failed:', msg);`, already logs the text). Status 500, code `INTERNAL_ERROR` and both `message` strings stay.",
 where="- `services/api-gateway/src/routes/platform.ts:994` - **must change**: the one-line `} catch (err: any) { res.status(500).json(...details: { detail: err?.message }...); }` that ends the templates read (the route opened a few lines above, under the `Platform Templates (document types + workflows)` banner at :968).\n- `services/api-gateway/src/routes/platform.ts:1091` - **must change**: inside the `catch (err: unknown)` of the clone-to-tenant route (:1026), the `res.status(500).json(...)` line; `:1089-1090` (`const msg = ...`, `console.error('[Clone] Failed:', msg);`) STAY.\n- `:1017` (a bare `catch { res.status(500)... 'Failed to fetch templates' }`) and `:1170` (`Document lookup failed`) already answer a constant body: NOT touched.",
 exactnote="", loose="The product edits are described by behaviour in `## What is wrong` and `## Where`; no diff and no `+` line is given for them. Write them yourself: minimal, only what those two sections require.\n\n",
 donot="**Do NOT touch** :1017, :1170, any other line of `platform.ts`, the existing tests, or any other file.",
 testnote2="The test section is a NEW vitest file given whole. The `+` lines are byte-exact. It reads platform.ts as text; it has no top-level await.",
 red=['RED plat-500 P1','RED plat-500 P2'],
 cells="- RED `P1` (no 500 answer in platform.ts names a caught value or carries details: at the tip two do), `P2` (the templates catch logs before it answers: at the tip it does not): both fail by assertion at the tip and pass after the edit.\n- GREEN at the tip and after: `C1` (scanner positive and negative controls), `C2` (four 500 answers keep their own messages: 2 'Failed to fetch templates', 1 'Clone failed', 1 'Document lookup failed'), `C3` (the clone catch still logs `[Clone] Failed:`).",
 premises="- :994 is the one-line catch quoted above; :1091 is the clone 500 with `details: { detail: msg }`; :1090 is `console.error('[Clone] Failed:', msg);` (read at the tip by script; the golden asserts both old strings are unique).\n- The file has exactly four `.status(500).json(` lines (:994 :1017 :1091 :1170) at the tip.\n- `console.error` is this file's logging idiom (:885, :1090).",
 unmeasured="- The drafter did NOT run the new file: RED-at-tip / GREEN-after is the `round.sh --control` run on this golden.\n- Whether any client reads `error.details.detail` of these two routes is not measured (the admin UI is not searched).\n- Which errors reach these catches in production is not measured.",
 scope="**The two platform.ts 500 bodies only.** No ticket exists for them (KS-1410's list names six other files); link as 'Refs KS-1410 (same class)' and say a census found them.",
)
