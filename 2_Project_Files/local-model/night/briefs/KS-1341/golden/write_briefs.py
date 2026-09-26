"""Write the KS-1341 A/B/C briefs from the verified goldens (hunks and test text are pasted, never retyped)."""
import re
import subprocess
import sys

D = '/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/6a51240d-d642-471f-b7c2-1011f35eb0ce/scratchpad/ks1341'
G = D + '/golden'
STAMP = sys.argv[1]
LSR_AT = sys.argv[2]      # shell `date` taken immediately before the final `git ls-remote`
LINEAR_AT = sys.argv[3]   # shell `date` taken immediately before the final Linear read
LINEAR_STATE = sys.argv[4]  # state name returned by that read

SECRET = """## Secret handling — does this edit change it? NO

The ONLY lines this brief changes in `webhooks.ts` are {lines} — each the response line of a `catch` block — plus {helper}. No line on
the secret path changes: `newSecret` generation (`:345`), `encryptWebhookSecret(newSecret, req.params.id)` (`:348`, body `:42-:44`),
the `UPDATE svc_webhooks SET secret_v2 = ${encrypted}` (`:349`), the one-time `res.json({ success: true, secret: newSecret })`
(`:350`), `decryptWebhookSecret` (`:46-:62`) and the HMAC signing in `deliverWebhook` (`:433`) are all byte-identical before and
after. What changes is where the THROWN TEXT goes: from the client's 500 body to `logger.error`. That text cannot carry the
plaintext secret — `encryptField` (`packages/shared/src/crypto/encryptedField.ts:315`) throws only key-state and context messages
(`:286`, `:293`, `:301`, `:318`), `plaintext` appears only at `:315/:316/:328` and in none of them, and the `UPDATE` binds the
ciphertext, never `newSecret`. So this is an error-BODY change on a route that handles a secret, not a change to secret handling.
{route_note}
"""
SHA = 'e080174c86c671349c508560744644fc0ef33388'
P = 'Blockchain/Dev/services/originate/src/routes/webhooks.ts'
T = 'Blockchain/Dev/services/originate/src/__tests__'
SITE = "    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: err.message } });"


def product_hunks(part):
    """The product-file hunks of the part's golden diff (everything before the /dev/null test hunk)."""
    txt = open(f'{G}/{part}.golden.diff').read()
    head = txt.split('--- /dev/null')[0]
    body = head.split('\n', 2)[2]  # drop the ---/+++ lines; the brief prints them itself
    return [h for h in re.split(r'(?m)^(?=@@ )', body) if h.strip()]


def test_text(letter):
    return open(f'{G}/ks1341{letter}-webhooks-500-never-answers-err-message.test.ts').read()


def nlines(letter):
    return test_text(letter).count('\n')


COMMON_HARNESS = """This service runs **jest** (ts-jest preset, `testEnvironment: 'node'`, `testMatch: ['**/__tests__/**/*.test.ts']` — read at
`Blockchain/Dev/services/originate/jest.config.js`), NOT vitest: `jest.mock`, `jest.fn`, `jest.requireMock`; `expect` takes ONE
argument. There is no database, no network beyond a loopback listener on 127.0.0.1, and no app boot: `../db`,
`../middleware/auth`, `@secuura/shared` (through `./helpers/sharedModuleMock`) and `../utils/logger` are all mocked, exactly as
in `ks1160-webhooks-post-persists-normalised-url.test.ts` lines 7-60 (the shape copied). To run the file alone, from
`Blockchain/Dev/services/originate`: `npx jest src/__tests__/{name}`."""

DONT_TOUCH_COMMON = """- every line of `webhooks.ts` other than the {n} `-` line(s) above{extra};
- `encryptWebhookSecret` / `decryptWebhookSecret` (`:42-:62`), the rotate-secret secret path (`:345-:350`: `newSecret`
  generation, `encryptWebhookSecret`, the `UPDATE ... secret_v2`, the one-time `res.json({ success: true, secret: newSecret })`),
  `deliverWebhook` (`:427-:497`), `dispatchEvent` (`:503-:547`) — including its own `logger.warn('Webhook dispatch failed', { ..., error: err.message })`
  at `:544`, which is a LOG line, not a response;
- the two swallowing `.catch(...)` branches at `:196` and `:412` and the PATCH SQLSTATE→400 branch at `:318-:324` (pre-existing,
  pinned by controls);
- the imports (`:11-:19`) — add NONE; `Response` (`:11`) and `logger` (`:16`) are already imported;
- every other file: `routes/gdpr.ts`, `routes/systemErrors.ts`, `routes/adminConfig.ts`, `utils/pgErrors.ts`, the six existing
  webhooks suites (`ks1160`, `ks423`, `ks431`, `ks444`, `ks445`, `ks914`), and `__tests__/helpers/sharedModuleMock.ts`."""


def brief(part):
    L = part.lower()
    name = f'ks1341{L}-webhooks-500-never-answers-err-message.test.ts'
    hunks = product_hunks(part)
    n = nlines(L)
    if part == 'A':
        slug, one = 'WEBHOOKS500-A', 'add the fail500 helper to routes/webhooks.ts and route GET / and POST / 500s through it'
        tip_line = f'`{SHA}` (origin develop, `git ls-remote origin refs/heads/develop`, re-read at {LSR_AT})'
        apply_note = 'Apply at the tip above. Nothing precedes this brief.'
        sites = [(200, 'GET /', 'Webhook list failed (GET /api/webhooks)'), (267, 'POST /', 'Webhook create failed (POST /api/webhooks)')]
        seq = 'FIRST of three (A → B → C). B and C both call the helper this brief adds.'
    elif part == 'B':
        slug, one = 'WEBHOOKS500-B', 'route the PATCH /:id, DELETE /:id and POST /:id/rotate-secret 500s in routes/webhooks.ts through fail500'
        tip_line = (f'`{SHA}` for every line quoted here, READ at that sha. **Apply at the develop commit that contains brief A\'s merge** '
                    f'(it does not exist yet); see `## Before queueing`.')
        apply_note = 'Apply on develop AFTER brief A is merged.'
        sites = [(325, 'PATCH /:id', 'Webhook update failed (PATCH /api/webhooks/:id)'),
                 (337, 'DELETE /:id', 'Webhook delete failed (DELETE /api/webhooks/:id)'),
                 (352, 'POST /:id/rotate-secret', 'Webhook secret rotation failed (POST /api/webhooks/:id/rotate-secret)')]
        seq = 'SECOND of three (A → B → C). Needs A merged (it calls `fail500`, which A adds).'
    else:
        slug, one = 'WEBHOOKS500-C', 'route the POST /:id/test and GET /:id/deliveries 500s in routes/webhooks.ts through fail500, and pin all seven by source'
        tip_line = (f'`{SHA}` for every line quoted here, READ at that sha. **Apply at the develop commit that contains briefs A AND B merged** '
                    f'(it does not exist yet); see `## Before queueing`.')
        apply_note = 'Apply on develop AFTER briefs A and B are merged.'
        sites = [(391, 'POST /:id/test', 'Webhook test send failed (POST /api/webhooks/:id/test)'),
                 (416, 'GET /:id/deliveries', 'Webhook delivery history read failed (GET /api/webhooks/:id/deliveries)')]
        seq = 'THIRD of three (A → B → C). Needs A merged (helper) and B merged (its SOURCE cell counts all seven sites).'

    out = []
    w = out.append
    w(f'# KS-1341-{part} {slug} — {one}\n')
    w(f'File: `{P}`  (product, modified in place)')
    w(f'Test file: `{T}/{name}`  (NEW)')
    w(f'Tip: {tip_line}')
    w('Runner: `jest` (ts-jest 29, `Blockchain/Dev/services/originate/package.json` `"test": "jest"`)\n')
    w(f'Written {STAMP} (shell `date`) from `{SHA}`, `webhooks.ts` read WHOLE (549 lines, ends with one `\\n`, blob sha1 of `git show` '
      f'output `c86b6344664f41bd6b12f4e7dc74aa37c76a52dd`, last changed at `408821134` KS-1160 #1186). **Brief {part} of 3 — {seq}**\n')

    w('## The mode — read this twice\n')
    w(f'CODE+TEST. Your diff touches EXACTLY 2 files, in this order:')
    w(f'1. `{P}` — modified in place, `--- a/{P}` / `+++ b/{P}`, EXACTLY the {len(hunks)} hunk(s) given in `## The exact change`, byte for byte.')
    w(f'2. `{T}/{name}` — a NEW file: `--- /dev/null` then `+++ b/{T}/{name}`, ONE hunk `@@ -0,0 +1,{n} @@`, every line `+`, '
      f'the text given in `## The test` byte for byte ({n} lines).\n')
    w('You never touch any other file. In particular you do NOT edit any existing test, `routes/gdpr.ts`, `routes/systemErrors.ts`, '
      '`routes/adminConfig.ts`, `utils/pgErrors.ts`, `utils/logger.ts` or `__tests__/helpers/sharedModuleMock.ts`. '
      f'{apply_note} The checker applies the TEST FILE ALONE first (every 🔴 cell must FAIL by assertion, every 🟢 control must PASS), '
      'then your product hunks on top (every cell must PASS).\n')

    w('## What is wrong (one paragraph)\n')
    w('`routes/webhooks.ts` (mounted at `/api/webhooks`) has seven catch blocks whose 500 answer is the byte-identical line '
      '`res.status(500).json({ success: false, error: { code: \'INTERNAL_ERROR\', message: err.message } });` at '
      '`:200, :267, :325, :337, :352, :391, :416` — with NO `NODE_ENV` guard, so the thrown error\'s own text reaches the client in '
      'every environment, production included. The 2026-09-26 QA gate MEASURED it under `NODE_ENV=production` '
      '(`Testing Agent MAIN/projects/secuura/reports/2026-09-26-batch1280-t1/report.md` lines 372-374, finding F-730-1, High): '
      '`DELETE /api/webhooks/:id` answered the gate\'s sentinel verbatim, and `POST /api/webhooks/:id/rotate-secret` answered the '
      'field-encryption layer\'s internal configuration message ("PII encryption is not initialised — call registerKey() + '
      'setActiveVersion()…"). None of the seven catch blocks logs the error, so simply deleting the text would destroy the only '
      'diagnostic. KS-730 fixed the same class in three sibling files, merged today as #1282/#1283/#1284, with a local helper that '
      'logs the thrown text server-side with the route named and answers a constant body — `routes/gdpr.ts:210-213`, '
      '`routes/systemErrors.ts:93-96` at the tip. This change applies that helper here, unchanged except for 2-space indentation '
      '(this file\'s style).')
    if part == 'A':
        w('\n**This brief:** add the helper (at the END of the file, so no line above it moves — B and C quote the same line numbers) '
          'and convert `:200` (GET /) and `:267` (POST /).\n')
    elif part == 'B':
        w('\n**This brief:** convert `:325` (PATCH /:id), `:337` (DELETE /:id — the MEASURED production leak) and `:352` '
          '(POST /:id/rotate-secret — the MEASURED configuration-text leak).\n')
    else:
        w('\n**This brief:** convert `:391` (POST /:id/test) and `:416` (GET /:id/deliveries), the last two; its SOURCE cell proves all '
          'seven are converted.\n')

    lines_txt = ', '.join(f'`:{a}`' for a, _, _ in sites)
    helper_txt = 'the 18-line helper inserted after `:548`' if part == 'A' else 'nothing else (the helper is A\'s)'
    note = ('The rotate-secret catch (`:352`) is in THIS brief; the 🟢 rotate-secret control (`a rotate-secret that does NOT throw ...`) pins the secret path end to end (fresh `whsec_` '
            'secret, encrypted with this row\'s AAD, stored once, returned once, nothing logged).' if part == 'B'
            else 'This brief does not touch the rotate-secret route at all (that is brief B, `:352`).')
    w(SECRET.replace('{lines}', lines_txt).replace('{helper}', helper_txt).replace('{route_note}', note))

    if part != 'A':
        w('## Before queueing (the builder, not the model)\n')
        prior = 'A' if part == 'B' else 'A and B'
        w(f'This brief is written against `{SHA}` and applies on the develop commit that contains {prior}. By construction the line numbers '
          f'do not move: A replaces `:200`/`:267` one line for one line and inserts its helper AFTER `:548`, and B replaces '
          f'`:325/:337/:352` one for one. **Verified in the scratch golden** (`golden/assemble_and_check.sh`): A → B → C apply strict '
          f'with `git apply` (no `--recount`) and reproduce the golden files byte for byte. Before queueing, re-read at the new tip:\n')
        nums = ';'.join(f'{a}p' for a, _, _ in sites)
        w('```')
        w(f"git show <new-develop-sha>:{P} | sed -n '{nums}'   # each must print the SITE line quoted in ## The exact change")
        w(f"git show <new-develop-sha>:{P} | grep -c '^function fail500('                 # must print 1")
        w('```')
        w('If either check fails, the brief is stale: do NOT queue it, rebuild it at the new tip.\n')

    w('## The exact change\n')
    w(f'Every `-` line below is the same SITE line — the SAME bytes at all seven sites (literal line-equality count 7 '
      'at the tip), so the context lines and the header are what place each hunk. Copy the hunks EXACTLY, headers included. '
      'The context lines are ASCII (the only non-ASCII line near a site, `:264`, is deliberately outside the 2-line context).\n')
    for i, h in enumerate(hunks, 1):
        m = re.match(r'@@ -(\d+)', h)
        start = int(m.group(1))
        if part == 'A' and i == 3:
            w(f'Edit {i} — PURE INSERTION of 18 lines after `:548` (the empty line after `dispatchEvent`\'s closing `}}` at `:547`), '
              'before `:549` `export default webhooksRouter;` (byte-unique, count 1). The inserted block is the helper\'s docblock, the '
              'helper, and ONE empty line after its closing `}`. Context: `:546` `  }`, `:547` `}`, `:548` empty.\n')
        else:
            ln, route, ctx = sites[i - 1]
            before = {200: ('    res.json({ success: true, webhooks: rows });', '  } catch (err: any) {'),
                      267: ('    });', '  } catch (err: any) {'),
                      325: ('      });', '    }'),
                      337: ('    res.json({ success: true });', '  } catch (err: any) {'),
                      352: ('    res.json({ success: true, secret: newSecret });', '  } catch (err: any) {'),
                      391: ('    });', '  } catch (err: any) {'),
                      416: ('    res.json({ success: true, deliveries: rows });', '  } catch (err: any) {')}[ln]
            w(f'Edit {i} — line `:{ln}` ({route}), replacement of ONE line by ONE line. Context: `:{ln-2}` is `{before[0]}`, '
              f'`:{ln-1}` is `{before[1]}`, `:{ln+1}` is `  }}`, `:{ln+2}` is `}});` — copy all four as context.\n')
        w('```diff')
        w(h.rstrip('\n'))
        w('```\n')
    w('**Do NOT touch:**\n')
    extra = ' and the 18 inserted lines' if part == 'A' else ''
    w(DONT_TOUCH_COMMON.replace('{n}', str(len(sites))).replace('{extra}', extra))
    w('\nThe helper\'s context string for each site is DISTINCT and names the route; do not shorten, merge or reword them.\n')

    w('## The test\n')
    w(f'File: `{T}/{name}` (NEW, {n} lines).')
    w(COMMON_HARNESS.replace('{name}', name))
    w('\nThe cell shape (LEAK string · four NODE_ENVs · constant body · logger received the route context · REACHED) is copied from '
      '`ks730c-adminconfig-500-never-answers-err-message.test.ts` lines 58-127, including its lesson (the KS-730 PR3 trap): a LEAK '
      'containing `does not exist` was routed into a benign 200 branch there, so a clean body alone proved nothing. Here the '
      'LEAK contains neither `does not exist` nor any SQLSTATE that `utils/pgErrors.ts:36` (`KNOWN_PG_CODES`) would classify, and '
      'every red cell asserts the logger received THIS route\'s context with the thrown text — which only the converted catch does.\n')
    if part in ('A', 'C'):
        route = 'GET /' if part == 'A' else 'GET /:id/deliveries'
        line = ':191-:196' if part == 'A' else ':406-:412'
        w(f'**This file\'s own trap:** `{route}` chains `.catch(...)` onto its query (`webhooks.ts{line}`), so a REJECTED `$queryRaw` '
          'is swallowed into a 200 and never reaches the catch under test. Its cell makes `$queryRaw` THROW SYNCHRONOUSLY '
          '(`mockImplementationOnce(() => { throw ... })`); the 🟢 control `' + ('A0' if part == 'A' else 'C0') + '` pins the swallowing branch.\n')
    else:
        w('**This file\'s own trap:** PATCH\'s catch (`webhooks.ts:318-:324`) sends a classified SQLSTATE to an honest 400 BEFORE the '
          '500 line, so the LEAK carries no SQLSTATE and no `code`; 🟢 `B0` pins that branch. rotate-secret is driven by making '
          '`encryptField` throw (the shape the gate measured), so its cell never reaches the database.\n')
    w(f'Emit this text as the new-file hunk `@@ -0,0 +1,{n} @@`, every line prefixed `+`, nothing added or dropped:\n')
    w('```ts')
    w(test_text(L).rstrip('\n'))
    w('```\n')

    w('## Cells and controls\n')
    labels = [r for _, r, _ in sites]
    tag = part
    for r in labels:
        w(f'- 🔴 `RED KS-1341 {tag}1 {r}: the thrown message is not in the 500 body under production, development, test or unset` — RED at the tip (the body carries LEAK)')
    for r in labels:
        w(f'- 🔴 `RED KS-1341 {tag}2 {r}: the thrown message is logged once, server-side, with this route named` — RED at the tip (nothing is logged)')
    if part == 'A':
        w('- 🟢 `control KS-1341 A0: a REJECTED list query is still swallowed into a 200 and never reaches the catch`')
        w('- 🟢 `control KS-1341 A: a create that does NOT throw answers 201 and logs nothing`  ← the positive control')
        w('- 🟢 `control KS-1341 A: an authored 400 keeps its own text and logs nothing`')
        w('- 🟢 `control KS-1341 A: the LEAK string is the thrown text and dodges every benign branch`')
    elif part == 'B':
        w('- 🟢 `control KS-1341 B0: a classified Postgres cast failure on PATCH still answers 400 and never reaches fail500`')
        w('- 🟢 `control KS-1341 B: a rotate-secret that does NOT throw still encrypts, stores and returns the new secret once`  ← the positive control, and the proof the secret path is unchanged')
        w('- 🟢 `control KS-1341 B: a DELETE that does NOT throw answers 200 and logs nothing`')
        w('- 🟢 `control KS-1341 B: an authored 400 keeps its own text and logs nothing`')
        w('- 🟢 `control KS-1341 B: the LEAK string is the thrown text and dodges every benign branch`')
    else:
        w('- 🔴 `RED KS-1341 C3 SOURCE: no response in the file carries err.message, and all seven sites use the helper with DISTINCT contexts` — RED at the A+B tip (2 leaking lines, 5 helper calls; measured on the golden)')
        w('- 🟢 `control KS-1341 C0: a REJECTED deliveries query is still swallowed into a 200 and never reaches the catch`')
        w('- 🟢 `control KS-1341 C: a test-send for an unknown webhook keeps its authored 404 and logs nothing`  ← the positive control')
        w('- 🟢 `control KS-1341 C: the LEAK string is the thrown text and dodges every benign branch`')
    w('\n(`it.each` expands each 🔴 row into one test per route, named with the route label as shown.)\n')

    w('## The failing case (the "tamper")\n')
    tl, troute, tctx = {'A': sites[0], 'B': sites[1], 'C': sites[1]}[part]
    new = f"    fail500(res, '{tctx}', err);"
    w(f'After your change, in `{P}` line `:{tl}` ({troute}) reads `{new}` — byte-unique in the post-change file (literal line-equality '
      f'count 1, measured on the golden). Tamper: replace it with the original SITE line `{SITE.strip()}` (4 leading spaces). '
      f'Expected: `{tag}1 {troute}` and `{tag}2 {troute}` go RED' + (' and `C3 SOURCE` goes RED' if part == 'C' else '') +
      '; every 🟢 control stays GREEN. Restore → all GREEN.\n')

    w('## Premises (each one measured, with where)\n')
    w(f'- origin develop = `{SHA}` — `git ls-remote origin refs/heads/develop` re-read at {LSR_AT} (first read earlier this session, same sha); the object is in the local store (`git cat-file -t` → commit).')
    w(f'- The seven SITE lines, byte-identical, at `:200, :267, :325, :337, :352, :391, :416` — python line-equality count 7 on `git show {SHA[:12]}:{P}`; '
      'the gate lists the same seven (`report.md:372`).')
    w('- No catch in the file logs before answering: `webhooks.ts:199-201, :266-268, :314-326, :336-338, :351-353, :390-392, :415-417` read whole.')
    w('- `fail500` does not exist in the file at the tip — `grep -c -i fail500` → 0 (positive control: `grep -c -i webhooksrouter` → 10). '
      '`does not exist` occurs 0 times in the file (same instrument, `-i`).')
    w('- The helper text is copied from `routes/gdpr.ts:210-213` at the tip (2-space body; `systemErrors.ts:93-96` has the same body at 4-space).')
    w('- A function declaration used above its declaration is already the pattern in this file: `deliverWebhook` is called at `:378` and declared at `:427`. '
      'The lint config (`Blockchain/Dev/eslint.config.mjs:24-50, :78-96`) has no `no-use-before-define` rule; `js.configs.recommended` + `tseslint.configs.recommended` do not enable it (UNMEASURED by a lint run — see below).')
    w('- `Response` is the express type imported at `:11`; `logger` is imported at `:16`.')
    w('- `extractPgCode` (`utils/pgErrors.ts:48-72`) reads `err.code`, `err.meta.code`, then `KNOWN_PG_CODES` (`:36`) in the message — the LEAK strings match none (asserted by each file\'s last control).')
    w('- The six existing webhooks suites all mock `logger` WITH an `error` fn (`ks1160:33-35`, `ks423:42-44`, `ks431:21-23`, `ks444:61-63`, `ks445:28-30`, `ks914:25-27`), and none asserts a 500 body\'s message text; '
      '`ks445` "keeps 500 for genuinely unclassified failures" (`:136-141`) asserts status only, so it stays green.')
    if part == 'B':
        w('- `encryptField` (`packages/shared/src/crypto/encryptedField.ts:315`) throws only key-state and context messages (`:286`, `:293`, `:301`, `:318`); '
          '`plaintext` appears at `:315`, `:316` and `:328` and in NONE of the thrown messages — so the text now LOGGED from rotate-secret\'s catch cannot carry the plaintext secret. '
          'The `UPDATE` at `:349` binds the ciphertext (`encrypted`), never `newSecret`.')
    w('- The golden (`golden/webhooks.A.ts`, `.AB.ts`, `.ABC.ts` and the three test files in the run directory) was BUILT and APPLIED: A → B → C apply with `git apply` strict (no `--recount`), '
      'reproduce the goldens byte for byte, and `typescript@5.9.3` `transpileModule` reports 0 syntactic diagnostics on all four files. The golden is for the checker, not shown to the model.')
    w('- After A+B+C, over non-comment lines: 0 lines match `/message: *err\\??\\.?message/`, 7 `fail500(res,` calls, 7 distinct contexts, 1 definition (measured on the golden; at A+B: 2 leaking, 5 calls).')
    w('')

    w('## UNMEASURED — stated rather than glossed\n')
    w('- **The new test file was NOT run**, at the tip or after the fix — no jest, no type-check (`tsc`/ts-jest diagnostics), no lint. RED-at-tip and GREEN-after are REASONED from the source. '
      'The first checker run is the first execution.')
    w('- Type-level risks I could not rule out without ts-jest: the `it.each` row type inferred from a non-`as const` array with a union `body` field; `mock.calls.at(-1)` needs lib ES2022 (it is used by the merged `ks730c`, so probably fine).')
    w('- Setting `process.env.NODE_ENV = \'production\'` inside a running jest worker is assumed to have no side effect on express or the mocks (the ks730 files do the same for development/demo/test; production is new here).')
    w('- The rest of the originate suite was not run, before or after; "no worse" is for the checker to measure.')
    w('- Whether the eslint run passes with the helper declared after its callers (reasoned from the config, not run).')
    w('- Open PRs were not listed through the GitHub API; only `git ls-remote` branch names were searched (see Collision).')
    w('- Whether deployed environments set `NODE_ENV`; irrelevant to the fix (it is unconditional) but the gate measured production only.')
    w('')

    w('## Collision\n')
    w(f'- KS-1341: {LINEAR_STATE}, priority 2 (High), assignee kamil.kreiser@secuura.ai, no attachments, no relations, created 2026-09-26 02:50Z (Linear re-read at {LINEAR_AT}). Round 0 — this is the first brief; the counter allows this + ONE rebrief, then Opus 5.5.')
    w('- `git ls-remote origin` branch names matching `1341|webhook`: `feature/ks-1160-…` (`8d3c5c96`, the pre-squash head of #1186, which is merged into develop as `408821134`), '
      '`feature/ks-927-webhooks-description-guard-mock` (`542492c4`: `git log {SHA[:9]}..542492c4 -- {P}` → no commits, so it does not touch this file), and `refs/pull/372/head`. None in flight on this file.')
    w('- Wednesday\'s `local-model/night/queue.md` and `done.md`: 0 rows for KS-1341.')
    w('- Adjacent, NOT this file: KS-1334 (adminConfig.ts unconditional leaks).')
    w(f'- Sequencing: A → B → C, one at a time (the Spark runs one request at a time). This is brief {part}.\n')

    w('## Scope\n')
    if part == 'C':
        w('With A and B merged, this closes KS-1341: all seven sites converted, pinned by `C3 SOURCE`. **Closes KS-1341** (only when A and B are merged; otherwise refs it).\n')
    else:
        closes = '2' if part == 'A' else '3'
        w(f'Closes {closes} of 7 sites. **Refs KS-1341, does NOT close it.** The ticket closes with brief C.\n')

    w('## Output\n')
    w(f'Exactly ONE fenced ```diff block, nothing outside it. First the product file (`--- a/{P}` / `+++ b/{P}`, the {len(hunks)} hunk(s) '
      f'exactly as given, in file order), then the new test file (`--- /dev/null` / `+++ b/{T}/{name}`, `@@ -0,0 +1,{n} @@`). '
      'Paths exactly as written here. Every `+` line on its own physical line. Every context line keeps its leading space. '
      'Do not add, reorder, reword or reindent anything.')
    return '\n'.join(out) + '\n'


for part, fname in [('A', 'brief.md'), ('B', 'brief-B.md'), ('C', 'brief-C.md')]:
    open(f'{D}/{fname}', 'w').write(brief(part))
    print('wrote', fname)
