#!/usr/bin/env python3
"""drafter_run.py — #1006 tamper matrix at HEAD 86fe59e6b, in the drafter's scratch clone. Each row: text anchor (Python str.count == 1),
markers asserted after, WHOLE packages/shared suite + WHOLE services/demo-service suite, sha256-asserted restore (git checkout -- <file>),
porcelain asserted equal to the T0 baseline before every row. Rows S* = the seat's table re-run on final bytes; G* = drafter rows,
including rows aimed at CONTROLS. Summary -> drafter_run_summary.json."""
import sys, json
sys.path.insert(0, '/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-17_gate1006')
from drafterlib import *
D = 'Blockchain/Dev/'
APP = D + 'services/demo-service/src/app.ts'
EH = D + 'services/demo-service/src/middleware/errorHandler.ts'
K781 = D + 'packages/shared/src/__tests__/ks781-p3-3-body-parser-order.test.ts'
K727 = D + 'packages/shared/src/__tests__/ks727-errorhandler-class-guard.test.ts'
H = T['head']
PRISTINE = {f: sha(H + '/' + f) for f in (APP, EH, K781, K727)}
P('drafter_run start', ts(), '| pristine', {f.split('/')[-1]: v[:12] for f, v in PRISTINE.items()})
BASEPORC = porcelain('head')
SPLICE = ("    // KS-844: move the marker ahead of demo-service's own terminal errorHandler.\n"
          "    const routerStack = (app as unknown as { _router: { stack: Array<{ name: string }> } })._router.stack;\n"
          "    const markerLayer = routerStack.pop();\n"
          "    expect(markerLayer?.name, 'the layer just mounted is the marker').toBe('markErrType');\n"
          "    const handlerAt = routerStack.findIndex((layer) => layer.name === 'errorHandler');\n"
          "    expect(handlerAt, \"demo-service's errorHandler layer is mounted\").toBeGreaterThan(-1);\n"
          "    routerStack.splice(handlerAt, 0, markerLayer!);\n")
ROWS = [
    ('T0', None, None, None, ()),
    ('S1_errorHandler_unmounted', APP, "  app.use(errorHandler);\n", "", (('app.use(errorHandler)', 0),)),
    ('S2_express_json_removed', APP, "  app.use(express.json());\n", "", (('express.json()', 0),)),
    ('S3_inline_terminal_handler_planted', APP, "  app.use(errorHandler);\n",
     "  app.use(errorHandler);\n  app.use((err: any, _req: any, res: any, _next: any) => { res.status(500).json({ error: String(err) }); });\n", (('app.use((err: any', 1),)),
    ('S4_second_unregistered_leaky_handler', EH, "    error: { code, message: status >= 500 ? 'Internal server error' : err.message },\n  });\n}\n",
     "    error: { code, message: status >= 500 ? 'Internal server error' : err.message },\n  });\n}\n\nexport function leakyErrorHandler(err: Error, _req: Request, res: Response, _next: NextFunction): void {\n  res.status(500).json({ message: err.message });\n}\n", (('export function leakyErrorHandler', 1),)),
    ('G1_CONTROL_AIM_splice_deleted_marker_appended_after_handler', K781, SPLICE, "", (('routerStack', 0), ('app.use(markErrType);', 1))),
    ('G2_CONTROL_AIM_marker_spliced_one_AFTER_the_handler', K781, "    routerStack.splice(handlerAt, 0, markerLayer!);\n", "    routerStack.splice(handlerAt + 1, 0, markerLayer!);\n", (('handlerAt + 1', 1),)),
    ('G3_parser_present_but_refuses_nothing', APP, "  app.use(express.json());\n", "  app.use(express.json({ type: () => false }));\n", (('type: () => false', 1),)),
    ('G4_5xx_arm_echoes_err_message', EH, "message: status >= 500 ? 'Internal server error' : err.message }", "message: err.message }", (("'Internal server error'", 0),)),
    ('G5_handler_throws_before_answering', EH, "  const status = err.status ?? err.statusCode ?? 500;\n", "  throw new Error('qa-throw');\n  const status = err.status ?? err.statusCode ?? 500;\n", (("qa-throw", 1),)),
    ('G6_4xx_echo_replaced_by_constant', EH, "message: status >= 500 ? 'Internal server error' : err.message }", "message: status >= 500 ? 'Internal server error' : 'Request error' }", (("'Request error'", 1),)),
    ('G7_ks727_header_count_reverted_to_8_9', K727, "//   Count today: 9 modules contributing 10 handlers. Both are exact sets\n", "//   Count today: 8 modules contributing 9 handlers. Both are exact sets\n", (('8 modules contributing 9 handlers', 1),)),
    ('T6_inert_comment_in_errorHandler', EH, "  const status = err.status ?? err.statusCode ?? 500;\n", "  // qa inert comment\n  const status = err.status ?? err.statusCode ?? 500;\n", (('qa inert comment', 1),)),
    ('T0_after', None, None, None, ()),
]
summary = {}
base_cells = {}
for label, f, old, new, markers in ROWS:
    P('\n== ROW', label, ts())
    porc = porcelain('head'); assert porc == BASEPORC, 'PORCELAIN DRIFT %r' % [x for x in porc if x not in BASEPORC]
    if f: edit(H + '/' + f, old, new, markers)
    try:
        rs = vitest('t_%s_shared' % label, 'head', 'shared'); rd = vitest('t_%s_demo' % label, 'head', 'demo')
    finally:
        if f: restore('head', f, PRISTINE[f])
    row = {}
    for pkg, r in (('shared', rs), ('demo', rd)):
        if r is None: row[pkg] = 'NO JSON'; continue
        reds = sorted(k for k, v in r['cells'].items() if v['status'] != 'passed')
        row[pkg] = {'files': r['files'], 'tests': r['tests'], 'passed': r['passed'], 'failed': r['failed'], 'not_passed': reds,
                    'decisive': {k: r['cells'][k]['msg'].split('\n')[0][:200] for k in reds}, 'suite_messages': r['suite_messages']}
    summary[label] = row
    P('   ROW RESULT', label, '| shared %s/%s not-passed %d | demo %s/%s not-passed %d' % (
        row['shared']['passed'] if isinstance(row['shared'], dict) else '-', row['shared']['tests'] if isinstance(row['shared'], dict) else '-', len(row['shared']['not_passed']) if isinstance(row['shared'], dict) else -1,
        row['demo']['passed'] if isinstance(row['demo'], dict) else '-', row['demo']['tests'] if isinstance(row['demo'], dict) else '-', len(row['demo']['not_passed']) if isinstance(row['demo'], dict) else -1))
json.dump(summary, open(GS + '/drafter_run_summary.json', 'w'), indent=1, ensure_ascii=False)
P('\ndrafter_run end', ts(), '| final porcelain == baseline', porcelain('head') == BASEPORC, '| pristine re-read', all(sha(H + '/' + f) == v for f, v in PRISTINE.items()))
