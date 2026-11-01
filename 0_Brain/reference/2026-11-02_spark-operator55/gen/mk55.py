# Operator 55: KS-1868 billing/src/routes/webhooks.ts Stripe-webhook path sites :166 :184 :215 (code_patch2, O49-P3 shape)
import sys, os, importlib.util
MK='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/gen/mk.py'
spec=importlib.util.spec_from_file_location('mk',MK); mk=importlib.util.module_from_spec(spec); spec.loader.exec_module(mk)
TIP=mk.TIP='03977e89a343ad7362760e4fb0270602fb6da5ce'
BR='/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/'
GEN='/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_spark-operator55/gen/'
SV='Blockchain/Dev/services/billing/'
PROD=SV+'src/routes/webhooks.ts'
REF=SV+'src/__tests__/ks1868-billing-webhook-replay-unreadable-throw.test.ts'
def guard(ind, expr, var):
    s=' '*ind
    return (s+"let %s: string;\n"%var+s+"try {\n"+s+"  %s = %s;\n"%(var,expr)+s+"} catch {\n"+s+"  %s = 'unreadable thrown value';\n"%var+s+"}\n")
T={}

L166="      logger.error('Webhook signature verification failed', { error: String(error) });\n"
T['p1']=dict(dir='ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw', fn='the Stripe webhook signature-verification catch', line=166, tsrc='t55_p1.ts.txt', ncells='3 cells (2 red, 1 control)',
  test=SV+'src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts',
  oldblock=L166, newblock=guard(6,'String(error)','reason')+"      logger.error('Webhook signature verification failed', { error: reason });\n",
  redlines="- RED ks1868 R1\n- RED ks1868 R2\n", redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws)",
  greens="'control ks1868 C1' (an ordinary `Error` logs `Error: bad signature`, the route answers the constant 400 and no database call is made), the control showing the normal path is unchanged.",
  descr=dict(
   site_intro="the signature-verification catch block of the `POST /webhooks/stripe` handler in `services/billing/src/routes/webhooks.ts` (line 166)",
   consequence="Today a hostile value thrown by `constructWebhookEvent` makes the catch block itself throw, so nothing is logged and the handler's promise rejects instead of answering the constant 400 `Invalid signature`.",
   red1="At the tip the route never answers (Express 4 does not see an async handler's rejection), so the request hits the cell's deadline and the status assertion fails",
   whatwrong="In `webhooks.ts` the Stripe webhook handler verifies the delivery with `stripeService.constructWebhookEvent(req.body, signature)` inside a try; its catch logs `logger.error('Webhook signature verification failed', { error: String(error) })` (the read is on line 166) and then answers the constant `res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid signature' } })`. If verification throws a revoked Proxy, `String(error)` throws a TypeError inside the catch; if it throws an Error whose `message` getter throws, `String(error)` (Error.prototype.toString reads `.message`) throws. Either way the catch throws before the line is logged and before the 400 is sent, so the handler rejects and the request is left unanswered. The fix reads the thrown value inside its own inner `try` into a local `reason` using the SAME expression `String(error)`, falling back to the constant `unreadable thrown value`, and the log call uses `error: reason`. The response stays the constant 400 `Invalid signature`; the thrown text is only ever logged, never sent. An ordinary Error still logs `error: Error: <its message>` exactly as today.",
   callers="CALLERS: this IS the route handler (`router.post('/stripe', ...)`), the only route the gateway forwards to billing. This catch runs BEFORE the idempotency claim, before `handleWebhookEvent` and before any database write, so no webhook_events row, credit or payment state exists to change. **BEHAVIOUR CHANGE the raise PR must state (Stripe-facing):** for a hostile throw from signature verification, Stripe today receives NO response (the request hangs until Stripe's own timeout counts the delivery as failed and schedules a retry); after the fix it receives the constant 400 `Invalid signature`, exactly what an ordinary verification error already gets (Stripe treats any non-2xx as a failed delivery and retries it as for the ordinary case). Nothing is persisted either way, no paid event is processed, skipped or marked duplicate by this change. A hostile value here is defence-in-depth: `constructWebhookEvent` is Stripe's own SDK.",
   dbnote="`../db` (`isDbAvailable` true, `query` counting calls), `../services/stripeService` (`constructWebhookEvent` throwing the value; `addCertificationCredits`) and `../utils/logger` are replaced; the real router runs on a loopback listener behind `express.json()` and the shared `errorHandler` (the harness of the pinned ref); no database and no network beyond 127.0.0.1. Because the tip leaves the request unanswered, the cell gives the request a short deadline and counts the unhandled rejection itself instead of letting the runner report it."))
L184="        error: error instanceof Error ? error.message : String(error),\n"
OLD184="    } catch (error) {\n      logger.error('[Webhook] Refusing delivery \u2014 idempotency unavailable', {\n        eventId: event.id,\n        eventType: event.type,\n"+L184+"      });\n"
NEW184="    } catch (error) {\n"+guard(6,'error instanceof Error ? error.message : String(error)','reason')+"      logger.error('[Webhook] Refusing delivery \u2014 idempotency unavailable', {\n        eventId: event.id,\n        eventType: event.type,\n        error: reason,\n      });\n"
T['p2']=dict(dir='ks_1868_o55_p2_billing_stripe_webhook_claim_unreadable_throw', fn='the Stripe webhook idempotency-claim catch', line=184, tsrc='t55_p2.ts.txt', ncells='4 cells (2 red, 2 control)',
  test=SV+'src/__tests__/ks1868-billing-webhook-stripe-claim-unreadable-throw.test.ts',
  oldblock=OLD184, newblock=NEW184,
  redlines="- RED ks1868 R1\n- RED ks1868 R2\n", redcells="`R1` (revoked Proxy) and `R2` (Error whose `message` getter throws)",
  greens="'control ks1868 C1' (an ordinary `Error` from the claim logs its message and the route answers the constant 503) and 'control ks1868 C2' (an unavailable database logs the claim error text), the controls showing the normal path is unchanged.",
  descr=dict(
   site_intro="the idempotency-claim catch block of the `POST /webhooks/stripe` handler in `services/billing/src/routes/webhooks.ts` (line 184)",
   consequence="Today a hostile value thrown out of `claimEvent` makes the catch block itself throw, so nothing is logged and the handler's promise rejects instead of answering the 503 that asks Stripe to redeliver.",
   red1="At the tip the route never answers (Express 4 does not see an async handler's rejection), so the request hits the cell's deadline and the status assertion fails",
   whatwrong="In `webhooks.ts` the Stripe webhook handler claims the event with `claimed = await claimEvent(event.id, event.type, event)` inside a try; its catch logs `logger.error('[Webhook] Refusing delivery \u2014 idempotency unavailable', { eventId: event.id, eventType: event.type, error: error instanceof Error ? error.message : String(error) })` (the read is on line 184) and then answers `res.status(503)` with a constant body (`SERVICE_UNAVAILABLE`, message asking to retry the delivery). If the value thrown out of `claimEvent` is a revoked Proxy, `error instanceof Error` itself throws a TypeError inside the catch; if it is an Error whose `message` getter throws, `error.message` throws. Either way the catch throws before the line is logged and before the 503 is sent, so the handler rejects and the request is left unanswered. (`claimEvent` throws its own ClaimUnavailableError for every database failure, so a hostile value reaches this catch only when something `claimEvent` calls outside its own try, such as `logger.warn`, throws one; this is defence-in-depth.) The fix reads the thrown value inside its own inner `try` into a local `reason`, falling back to the constant `unreadable thrown value`, and the log call uses `error: reason`. The response stays the same constant 503; the thrown text is only ever logged. An ordinary Error still logs `error: <its message>`.",
   callers="CALLERS: this IS the route handler (`router.post('/stripe', ...)`). The catch runs BEFORE any side effect: `claimEvent` either never reached the INSERT (`isDbAvailable()` false, where its `logger.warn` is the call the test makes throw) or failed at it, and the handler returns before `handleWebhookEvent`. **BEHAVIOUR CHANGE the raise PR must state (Stripe-facing):** for a hostile throw out of the claim, Stripe today receives NO response (the request hangs until Stripe's timeout counts the delivery as failed and retries it); after the fix it receives the constant 503 `SERVICE_UNAVAILABLE`, exactly what an ordinary claim failure already gets (503 is a failed delivery Stripe retries with backoff). Persisted state: no webhook_events row is written by this path in either version (the claim did not win), no credits are granted, nothing is marked duplicate, so no paid event is skipped or double-processed by this change; the redelivery is claimed fresh as for an ordinary 503.",
   dbnote="`../db` (`isDbAvailable` returning false, `query` counting calls), `../services/stripeService` (`constructWebhookEvent` returns a `customer.created` event; `addCertificationCredits` counting calls) and `../utils/logger` (`warn` throws the value when one is set, the way a failing log sink would) are replaced; the real router runs on a loopback listener behind `express.json()` and the shared `errorHandler`; no database and no network beyond 127.0.0.1. The value is thrown from a plain function, not `vi.fn()`, on purpose. Because the tip leaves the request unanswered, the cell gives the request a short deadline and counts the unhandled rejection itself."))
OLD215="      const message = error instanceof Error ? error.message : String(error);\n"
NEW215=guard(6,'error instanceof Error ? error.message : String(error)','message').replace("      let message: string;\n","      let message: string;\n",1)
T['p3']=dict(dir='ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw', fn='the Stripe webhook handler catch (claim release)', line=215, tsrc='t55_p3.ts.txt', ncells='5 cells (3 red, 2 control)',
  test=SV+'src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts',
  oldblock=OLD215, newblock=NEW215,
  redlines="- RED ks1868 R1\n- RED ks1868 R2\n- RED ks1868 R3\n", redcells="`R1` (revoked Proxy), `R2` (Error whose `message` getter throws) and `R3` (after a revoked-Proxy failure the redelivery must be processed)",
  greens="'control ks1868 C1' (an ordinary `Error` logs its message, releases the claim, answers the constant 500) and 'control ks1868 C2' (after an ordinary Error the redelivery is processed), the controls showing the normal path, and the after-state of the hostile cells, are what an ordinary Error already gets.",
  descr=dict(
   site_intro="the handler catch block of the `POST /webhooks/stripe` handler in `services/billing/src/routes/webhooks.ts` (line 215), which hands the idempotency claim back",
   consequence="Today a hostile value thrown by `handleWebhookEvent` makes the catch block itself throw at its first line, so nothing is logged, `releaseClaim` is never reached, the 500 is never sent, and the webhook_events row stays 'processing'.",
   red1="At the tip the route never answers (Express 4 does not see an async handler's rejection), so the request hits the cell's deadline and the status assertion fails; R3 additionally fails because the redelivery is acknowledged as a duplicate",
   whatwrong="In `webhooks.ts` the Stripe webhook handler, after winning the idempotency claim, runs `handleWebhookEvent(event)` and `finaliseEvent(...)` inside a try; its catch starts `const message = error instanceof Error ? error.message : String(error);` (line 215), then logs it, calls `await releaseClaim(event.id, message)` (which sets the row to 'failed' so a redelivery can re-claim it) and answers the constant `res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Webhook handler failed' } })`. If the handler throws a revoked Proxy, `error instanceof Error` itself throws a TypeError inside the catch; if it throws an Error whose `message` getter throws, `error.message` throws. Either way the catch throws on its first line, so nothing is logged, the claim is NOT released and the 500 is never sent. The fix declares `let message: string;` and reads the thrown value inside its own inner `try` into it, falling back to the constant `unreadable thrown value`; every later line of the catch (the log, `releaseClaim`, the 500) is UNCHANGED and now runs, with `message` being the constant. An ordinary Error still gives `message = <its message>`.",
   callers="CALLERS: this IS the route handler (`router.post('/stripe', ...)`). **MONEY-ADJACENT BEHAVIOUR CHANGE the raise PR must state (Stripe-facing and persistence):** for a hostile throw out of `handleWebhookEvent` (for example `addCertificationCredits` rejecting) today (1) Stripe receives NO response and times out, (2) the webhook_events row stays 'processing', (3) Stripe's redelivery loses the claim (`ON CONFLICT ... WHERE status = 'failed'` does not match 'processing') and is answered `200 {received:true, duplicate:true}` WITHOUT processing, so a paid event whose handler failed is skipped; (4) only an admin POST /webhooks/replay recovers it. After the fix (1) Stripe receives the constant 500 (retried with backoff), (2) the row is set to 'failed' by `releaseClaim`, (3) the redelivery re-claims the row and is processed, which is EXACTLY what an ordinary Error already does today (cells C1 and C2 are green at the tip). The change therefore makes the hostile-throw path identical to the ordinary-Error path; it does not introduce a new retry behaviour. Unchanged and not touched by this brief: `handleCheckoutComplete` grants the credits and then makes further calls (log lines); a value thrown AFTER a successful grant is released and re-processed on redelivery today for an ordinary Error, and after the fix for a hostile value too, i.e. the same existing double-grant window an ordinary Error already has; whether that window should be closed is a design question outside this brief.",
   dbnote="`../db` (`isDbAvailable` true, `query` a small in-memory stand-in for the webhook_events claim table: INSERT wins when the row is absent or 'failed', loses when 'processing' or 'processed'; the 'failed' and 'processed' UPDATEs set the row), `../services/stripeService` (`constructWebhookEvent` returns a `checkout.session.completed` event; `addCertificationCredits` throws the value when one is set, else counts a grant) and `../utils/logger` are replaced; the real router runs on a loopback listener behind `express.json()` and the shared `errorHandler`; no database and no network beyond 127.0.0.1. The value is thrown from a plain function, not `vi.fn()`, on purpose. Because the tip leaves the first request unanswered, the cell gives each request a short deadline and counts the unhandled rejection itself."))
TESTSRC=None
def build(k):
    X=T[k]
    old=mk.rd(PROD); assert old.count(X['oldblock'])==1
    new=old.replace(X['oldblock'],X['newblock'])
    pd=mk.udiff(PROD,old,new); pd_body=pd.split('\n',1)[1]
    tbody=open(GEN+X['tsrc'],encoding='utf-8').read()
    td=mk.udiff(X['test'],'',tbody,True); nlines=len(tbody.splitlines())
    golden=pd+td
    d=BR+X['dir']; os.makedirs(d,exist_ok=True)
    open(d+'/golden.diff','w',encoding='utf-8').write(golden)
    pins=("# code_patch2: billing webhooks.ts (1 hunk) + a NEW test file; ref = shape only; line = the changed line.\ntier=code_patch2\nref=%s\nline=%d\nctx=65536\n"
          "started_ok=KS-1868_is_In_Progress_(umbrella_ticket,_file-disjoint_sites);_services/billing_src/routes/webhooks.ts_and_src/__tests__/_are_in_no_open_PR_(19_PRs_108_files_read_2026-11-02_by_op55,_billing_only_as_package.json/package-lock.json_in_575/649/1360,_positive_control_services/billing_in_3_entries);_live_lanes_beyond_PRs_not_checked\n")%(REF,X['line'])
    open(d+'/spark.pins','w').write(pins)
    D=X['descr']; tp=X['test'].split('/')[-1]
    txt=f"""# KS-1868 billing: {X['fn']} must still report when the thrown value cannot be read (one site of the 253; RUNG 3, code_patch2: one product hunk given as a skeleton, one NEW test file given whole)

DRAFT by Spark operator 55 for Wednesday, 2026-11-02. Secuura (billing) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. Origin: KS-1868 (253 catch sites read a thrown value as `X instanceof Error ? X.message : String(X)`; none is guarded against a thrown value whose read itself throws, e.g. a revoked Proxy). This brief fixes ONE site, inline, with no shared helper: {D['site_intro']}. {D['consequence']} No open PR touches this file or its `src/__tests__/` directory (the 19 open PRs read 2026-11-02 through the GitHub API; 108 file entries; services/billing appears only as package.json / package-lock.json in PRs 575, 649 and 1360; planted positive control: the same scan finds services/billing in 3 entries). Sibling sites of this same file are separate briefs (O55-P1..P3); the replay handler was fixed by PR 1906.

File: `{PROD}`  (product, modified in place: ONE hunk)
Test file: `{X['test']}`  (NEW file, vitest, given in full below; {X['ncells']})
Tip: `{TIP}` (origin develop; every line number and quote below was read from it)
Runner: `vitest` (`npx vitest run src/__tests__/{tp}` from `Blockchain/Dev/services/billing`)
Tier: `code_patch2`
Rung: **3 (one product hunk, skeleton dictated; new test given whole)**

## The mode - read this twice

CODE+TEST. Your diff touches EXACTLY 2 file(s), in this order:
1. `{PROD}` - modified in place: EXACTLY the one hunk under "The exact change", byte for byte.
2. `{X['test']}` - a NEW file: `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, ONE hunk `@@ -0,0 +1,{nlines} @@`, every line `+`.

You never touch any other file and no other line of the files above.

## What is wrong (one paragraph)

{D['whatwrong']}

## Where

`{PROD}:{X['line']}`. {D['callers']}

## The exact change

ONE hunk in the product file. The file header lines and the `@@` header are DICTATED: copy them character for character, do not recount. Context lines start with ONE space, removed lines with `-`, added lines with `+` (byte-exact; spaces only). The log message text contains an em dash; copy it unchanged.

```diff
{pd_body}```

The `+` lines are byte-exact: copy them. Indentation is spaces only. Context lines begin with one space (the diff marker) followed by the file text.

**Do NOT touch** any message text, any other line of the file, or any other catch block in it. 

## The test

File: `{X['test']}`

The test section is a NEW test file given whole. The `+` lines are byte-exact. The shape is copied from `{REF}` (env set first, `vi.mock` of `../db`, the services and the logger, then a top-level-await import of the router mounted on an express app). {D['dbnote']} ****

```diff
{td}```

## Red cells
{X['redlines']}
## Cells and controls

- RED at the tip, GREEN after: {X['redcells']}. {D['red1']}; after the edit the result carries the constant `unreadable thrown value`.
- GREEN at the tip and after: {X['greens']}
- The stand-in rejecting with the thrown value is a plain function, not `vi.fn()`, on purpose: a vitest spy inspects what it rejects with and may fail on a revoked Proxy before the code under test sees it.

## Premises (each one measured, with where)

- `{PROD}:{X['line']}` is the `instanceof Error` read at the tip (read whole with `git show` at `{TIP[:12]}`).
- Open PRs: 19 read 2026-11-02 via the GitHub REST API (pulls?state=open, then pulls/N/files); none touches `{PROD}` or `src/__tests__/` (19 PRs, 108 file entries; services/billing only as package.json / package-lock.json); the positive control services/billing appears in 3 file entries.
- This file is neither `tenant-context.ts` nor `tenant-pool-manager.ts` and is outside services/auth, services/originate, services/anchoring, services/tenant-provisioning and vc-issuer.\n- services/billing uses its own node_modules (SPARK_NM_EXCLUDE); the pinned ref `ks1868-billing-webhook-replay-unreadable-throw.test.ts` (the test of PR 1906, the same file's replay handler) runs in the baseline.

## UNMEASURED - stated rather than glossed

- The golden is written by the operator from the diff design; it is proved by the harness `--control` run (round.sh), not by this text. tsc and eslint on the new file were not run outside the checker. The other sites of the 253 were not touched or measured. Whether a real path throws such a value here is not known (KS-1868 says the same). The service boot path and a real Postgres were not run.

## Scope

**This one site only.** Refs KS-1868; does NOT close it, and introduces no shared helper.

## Output

Exactly ONE fenced ```diff block, nothing outside it: 2 file section(s) in the order of `## The mode`; the first section starts `diff --git a/<path> b/<path>`; a NEW file's section is `diff --git`, `new file mode 100644`, `--- /dev/null` (NEVER `--- a/`), `+++ b/<path>`, then the hunk header `@@ -0,0 +1,N @@` and every body line starting `+`. The opening fence line is exactly ```diff. Every `+` line on its own physical line. Every context line keeps its leading space. Use the dictated `@@` header unchanged.
"""
    open(d+'/KS-1868.md','w',encoding='utf-8').write(txt)
    print('wrote',d); print(pd)
for k in sys.argv[1:]: build(k)
