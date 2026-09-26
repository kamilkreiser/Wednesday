"""Build the golden product files for KS-1341 A, A+B, A+B+C from the develop blob (scratchpad only)."""
import re

D = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/ks1341'
src = open(D + '/src/webhooks.ts').read().split('\n')  # last element '' (file ends with one newline)
SITE = "    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });"
CTX = {
    200: 'Webhook list failed (GET /api/webhooks)',
    267: 'Webhook create failed (POST /api/webhooks)',
    325: 'Webhook update failed (PATCH /api/webhooks/:id)',
    337: 'Webhook delete failed (DELETE /api/webhooks/:id)',
    352: 'Webhook secret rotation failed (POST /api/webhooks/:id/rotate-secret)',
    391: 'Webhook test send failed (POST /api/webhooks/:id/test)',
    416: 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)',
}
HELPER = '''/**
 * KS-1341: the only place in this router that turns a caught error into a 500.
 *
 * Seven catch blocks above put the thrown error's own text in the 500 body with NO NODE_ENV
 * guard, so it reached the client in every environment, production included (measured by the
 * 2026-09-26 gate: DELETE /:id returned the thrown text, rotate-secret returned internal
 * encryption-configuration text). Same helper as routes/gdpr.ts and routes/systemErrors.ts
 * (KS-730): log the thrown text server-side with the route named, answer the constant body.
 *
 * Declared at the END of the file on purpose: a function declaration is hoisted, and the
 * handlers above only call it at request time (deliverWebhook is called above its own
 * declaration the same way). Placing it here leaves every line above it where it was.
 */
function fail500(res: Response, context: string, err: unknown): void {
  logger.error(context, { error: err instanceof Error ? err.message : String(err) });
  res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } });
}
'''.split('\n')  # trailing '' becomes the blank line between '}' and 'export default'


def apply(lines, sites, add_helper):
    out = list(lines)
    for n in sites:
        assert out[n - 1] == SITE, (n, out[n - 1])
        out[n - 1] = "    fail500(res, '%s', err);" % CTX[n]
    if add_helper:
        assert out[547] == '' and out[548] == 'export default webhooksRouter;', (out[547], out[548])
        out = out[:548] + HELPER + out[548:]
    return out


A = apply(src, [200, 267], True)
AB = apply(A, [325, 337, 352], False)
ABC = apply(AB, [391, 416], False)
for name, l in [('webhooks.A.ts', A), ('webhooks.AB.ts', AB), ('webhooks.ABC.ts', ABC)]:
    open(D + '/golden/' + name, 'w').write('\n'.join(l))
print('line counts A/AB/ABC:', len(A) - 1, len(AB) - 1, len(ABC) - 1)
leaks = sum(1 for l in ABC if re.search(r'message: *err\??\.?message', l))
calls = [l for l in ABC if 'fail500(res,' in l]
distinct = {re.search(r"fail500\(res, '([^']+)'", l).group(1) for l in calls}
defs = sum(1 for l in ABC if l.startswith('function fail500('))
print('ABC: err.message sites', leaks, '| fail500 calls', len(calls), '| distinct', len(distinct), '| defs', defs)
AB_leaks = sum(1 for l in AB if re.search(r'message: *err\??\.?message', l))
print('AB (C source cell must be RED here): err.message sites', AB_leaks, '| calls', sum(1 for l in AB if 'fail500(res,' in l))
print('non-ASCII in any added text:', any(ord(c) > 127 for l in HELPER for c in l) or any(ord(c) > 127 for v in CTX.values() for c in v))
print('each fail500 call line byte-unique in ABC:', all(ABC.count(l) == 1 for l in calls))
