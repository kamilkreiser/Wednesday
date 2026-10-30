# KS-1791 (narrow): the social sign-in callback echoes a JSON SyntaxError's message (V8 quotes the first 10 chars of the provider body). Spark operator 17. code_patch2: ONE product hunk (routes/auth.ts) + the EXISTING ks1240b test modified in place (3 hunks).
P='Blockchain/Dev/services/auth/src/routes/auth.ts'
TP='Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts'
OLD=("    } catch (exchangeErr: any) {\n"
"      throw new BadRequestError(\n"
"        `OAuth authentication failed: ${exchangeErr?.message || 'invalid authorization code'}`\n"
"      );\n"
"    }\n")
NEW=("    } catch (exchangeErr: any) {\n"
"      // KS-1791: a provider that answers 200 with a body that is not JSON makes the adapter's `.json()` throw a SyntaxError whose message QUOTES the first 10 characters of that body (V8). Those are the\n"
"      // provider's bytes, so they are not echoed to the client; every other exchange failure keeps its own message, as before.\n"
"      const detail = exchangeErr?.name === 'SyntaxError' ? 'the provider answer could not be read' : exchangeErr?.message || 'invalid authorization code';\n"
"      throw new BadRequestError(`OAuth authentication failed: ${detail}`);\n"
"    }\n")
T1o="type Mode = 'ok' | 'hang' | 'stall' | 'refuse' | 'refuse5xx' | 'unauth' | 'empty200' | 'deadport';\n"
T1n="type Mode = 'ok' | 'hang' | 'stall' | 'refuse' | 'refuse5xx' | 'unauth' | 'empty200' | 'html200' | 'deadport';\n"
T2o="      if (m === 'empty200') { res.writeHead(200, { 'content-type': 'application/json' }); res.end('{}'); return; }\n"
T2n=T2o+"      // KS-1791: HTTP 200 with a body that is not JSON; the adapter's .json() throws a SyntaxError that quotes the first 10 characters of it.\n      if (m === 'html200') { res.writeHead(200, { 'content-type': 'text/html' }); res.end(`<html>${PROVIDER_MARKER}</html>`); return; }\n"
T3o="  it('🔴 POST /social/link, GitHub refuses the CONNECTION: 503 SERVICE_UNAVAILABLE (was 500)', async () => {\n"
T3n=("  it('RED KS-1791 R1 a token answer that is 200 with a non-JSON body: the login callback answers 400 with a neutral text and none of the provider\\'s bytes', async () => {\n"
"    const state = await freshState('github');\n"
"    mode['github.com/login/oauth/access_token'] = 'html200';\n"
"    const r = await call('GET', `/api/auth/social/github/callback?code=c8&state=${encodeURIComponent(state)}`);\n"
"    expect([r.status, r.code, r.message]).toEqual([400, 'BAD_REQUEST', 'OAuth authentication failed: the provider answer could not be read']);\n"
"    expect(r.raw, 'the first bytes of the provider body are not in the response').not.toContain('<html>PROV');\n"
"    expect(r.raw, 'the parser message is not in the response').not.toContain('is not valid JSON');\n"
"  }, 15000);\n\n")+T3o
S=dict(dir='ks_1791_p1_callback_syntaxerror_neutral',ticket='KS-1791',
 title="auth routes/auth.ts social sign-in callback: a provider 200 with a non-JSON body leaks its first 10 characters into the 400 through the SyntaxError message (KS-1791, narrow): map a SyntaxError exchange failure to a neutral text (RUNG 3, code_patch2: one product hunk + three hunks added to the existing ks1240b test)",
 intro="DRAFT by Spark operator 17 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / auth) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. **routes/auth.ts is an AUTH surface (the social sign-in callback): routing row 4 applies and the raise PR needs a TIER-1 gate.** The change only withholds provider bytes from a 400. Origin: KS-1791 (tier-1 gate 7 probes P1/P2, finding 1788-10 on PR 1788, which is merged). **Narrowed on purpose:** the ticket's 'root fix' (map EVERY non-AppError exchange failure to a neutral text) would change the classified texts that the existing ks1240b cells pin ('GitHub did not answer in time...', 'GitHub token exchange failed (HTTP 400)'), so this brief maps only a `SyntaxError` and leaves every other message as is. Link the PR as Refs KS-1791, never a close-word.",
 products=[(P,[(OLD,NEW)])],
 prodnote=['product, modified in place: the `catch (exchangeErr)` block of the login callback, 4 lines replaced by 6'],
 tests=[dict(path=TP,new=False,edits=[(T1o,T1n),(T2o,T2n),(T3o,T3n)])],
 testnote=['EXISTING, modified in place: 3 hunks (the Mode type gains `html200`, the stub gains an `html200` branch, one new red cell is inserted before the POST /social/link connection cell)'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts` from `Blockchain/Dev/services/auth',
 tier='code_patch2', rung='3 (two files: a product file with one hunk, an existing test with three hunks, all given byte-exact)',
 pins='''# code_patch2: auth routes/auth.ts (1 hunk) + the EXISTING ks1240b test modified in place (test_file=); ref = another social/oauth route test (shape only); line = the first changed line in the FIRST product.
tier=code_patch2
test_file=Blockchain/Dev/services/auth/src/__tests__/ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts
ref=Blockchain/Dev/services/auth/src/__tests__/ks722-oauth-state-verified.test.ts
line=1077
ctx=65536
''',
 wrong="The login callback of `services/auth/src/routes/auth.ts` wraps every exchange failure as `BadRequestError('OAuth authentication failed: ' + exchangeErr.message)` (`:1077-1081`). When a provider answers HTTP 200 with a body that is not JSON (for example an HTML error page), the adapter's `.json()` throws a `SyntaxError` whose message V8 builds by quoting the first 10 characters of the body (`Unexpected token '<', \"<html>PROV\"... is not valid JSON`), and that reaches the client in the 400. #1788 already stopped the status-error bodies being echoed; this is the same class on the `.json()` lines. Map a `SyntaxError` to a neutral text; leave every other failure's message alone.",
 where="- `services/auth/src/routes/auth.ts:1077-1081` - **must change**: the `catch (exchangeErr: any) { throw new BadRequestError(...) }` block, replaced by the block in the diff below.\n- `ks1240b-...test.ts:141` (the `type Mode`), `:195` (the `empty200` stub branch) and the cell `🔴 POST /social/link, GitHub refuses the CONNECTION: 503 ...` (`:418`): the three places that gain a hunk. The `provider body is not echoed` cell above it (`:410-416`) is the shape the new cell follows.\n- `:1056-1067` (the `?error=` and `code` checks) and `POST /social/link` (a generic 500) - (correct, STAY).",
 exactnote="ONE product hunk. The test is modified in place by three small hunks given under `## The test`.\n",
 donot="**Do NOT touch** the adapters under `providers/social/`, the `?error=` branch, the state consumption, or any other line of `auth.ts`; no other file.",
 testnote2="The test section modifies the EXISTING `ks1240b` file in place with exactly the hunks below. The `+` lines are byte-exact; do not re-indent, do not rename an existing cell.",
 red=['RED KS-1791 R1'],
 cells="- RED `R1` at the tip: the callback answers 400 with `OAuth authentication failed: Unexpected token '<', \"<html>PROV\"... is not valid JSON`, so the message equality and both `not.toContain` checks fail.\n- GREEN at the tip and after: every existing ks1240b cell, in particular the classified texts (timeout, unreachable, `GitHub token exchange failed (HTTP 400)`) and the `POST /social/link` 500 control.\n- After the edit R1 is green too.",
 premises="- `routes/auth.ts:1075-1081` is as quoted (read at the tip by script; the golden is generated from the tree at the tip, not typed).\n- The test file's `type Mode` is at `:141`, the stub's `empty200` branch at `:195`, `PROVIDER_MARKER = 'PROVIDER_TEXT_MARKER_ks1240b'` at `:142` (so the new stub body `<html>PROVIDER_TEXT_MARKER_ks1240b</html>` yields a SyntaxError quoting `<html>PROV`, the ticket's figure), `freshState` and `call` are the helpers the neighbouring route cells use (`r.raw` is the raw response text, used at `:415`).\n- The ticket's measurement: GitHub token endpoint answering `200 text/html` `<html>PROVIDER_TEXT_MARKER...` reaches the client as `\"<html>PROV\"...` (gate 7 probes P1/P2, real routes, stub provider).",
 unmeasured="- The drafter did NOT run the new cell; the RED-at-tip / GREEN-after result is the `round.sh --control` run on this golden.\n- The new stub body is `<html>${PROVIDER_MARKER}</html>` (no `upstream ` prefix, unlike the `refuse5xx` branch) so that V8's quoted 10 characters are `<html>PROV`, the ticket's figure; not run by the drafter.\n- Whether `exchangeErr.name` is `'SyntaxError'` for the body-parse failure under vitest/undici is the premise of the whole fix; the control run is the first measurement.\n- The other five adapters' `.json()` lines reach the same catch, so the one route change covers them; only GitHub is driven by the new cell.\n- The ticket's broader root fix (every non-AppError failure neutral) is NOT done.",
 scope="**KS-1791, narrowed to a `SyntaxError` exchange failure on the login callback.** Link the PR as Refs KS-1791, never a close-word. Tier-1 gate on the PR because routes/auth.ts is an auth surface.",
)
