KS-1182 demo-service errorHandler: unchecked err.status (NaN crashes the process, 200/302/600 pass through), headersSent/err.headers/expose ignored — unreachable today (KS-844 gate F4/F7)
state In Progress

## BLUF

demo-service's new `errorHandler` (`services/demo-service/src/middleware/errorHandler.ts`, PR #1006 / KS-844) applies `err.status` unchecked and ignores `headersSent`, `err.headers` and `expose`. **Unreachable today:** no current producer sets any of these. But measured on synthetic rows:

* statuses 200/302/600 go out as-is;
* 99 falls through to express's HTML page;
* **NaN crashes the process** (uncaught RangeError, exit 1, no response);
* `Allow` is dropped on a 405;
* a 4xx with `expose:false` is echoed.
  A test-quality Polish (F7) on the KS-844 test file rides along.

## Recommendation

Apply the gate's fix shape:

* `if (res.headersSent) return next(err)`;
* `status = Number.isInteger(s) && s >= 400 && s <= 599 ? s : 500`;
* echo `err.message` only when `expose !== false` (or for a typed error);
* apply `err.headers` as finalhandler does.
  Add the gate's H1–H5, H9 and H12 rows as cells. Optionally fix F7.

## Detail

Source: tier-1 QA gate on PR #1006 at `86fe59e6bf07108142fb3dbd06bef8747d2a4687`, 2026-09-17. Report: `Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks844-1006-86fe59e6b-tier1-r1/report.md`, section 6c (synthetic rows) and 6a (reachability). The findings, verbatim from its table:

| \# | finding | evidence class | severity | target | SHIPS-WITH / TICKET | oracle |
| -- | -- | -- | -- | -- | -- | -- |
| **F4** | `errorHandler.ts:33-35` applies `err.status` unchecked and ignores `headersSent` / `err.headers` / `expose`. Status 200/302/600 go out as-is; 99 falls through to express's HTML page; **NaN crashes the process (uncaught RangeError, exit 1, no response)**; `Allow` is dropped on a 405; a 4xx with `expose:false` is echoed. **No current producer** sets any of these (§6a, §6c). | MEASURED AT RUNTIME (synthetic, isolated processes) + READ (reachability) | Record (unreachable today; the NaN row would be a DoS shape if a producer appeared) | demo-service owner / KS-844 follow-up | TICKET. Fix-shape: `if (res.headersSent) return next(err)`; `status = Number.isInteger(s) && s >= 400 && s <= 599 ? s : 500`; echo `err.message` only when `expose !== false`, or for a typed error; apply `err.headers` as finalhandler does. Regression test: H1–H5, H9, H12 rows as cells. | *Comparable products* (finalhandler; the corpus's typed-4xx doctrine) |
| **F7** | The new ks844 test: (a) file name `…-mounts-no-error-handler.test.ts` vs describe "mounts an error handler that answers JSON" (name vs content); (b) cell 2's markers are blind to the shape they guard. `'    at '` cannot match express's HTML-escaped frames (`<br> &nbsp; &nbsp;at`, measured in base E1), and `/Volumes/` / `/app/` are host-bound. At base the cell reds on `<html` first, so its stack and path assertions are never the decisive ones. | READ + MEASURED (base body) | Polish | #1006 (the ks844 test) | SHIPS-WITH optional (non-blocking) | *Product* |

Reachability (the gate's READ): body-parser, raw-body and http-errors set only 400, 403, 413, 415 or 500, and no route or middleware in demo-service calls `next(err)`. Production refuses to boot (`demoGuard.ts:71`), and no external route reaches demo-service today. So the severity is Record, not higher. The NaN row would be a denial-of-service shape if a producer appeared.

Dedupe before filing (seat A, 2026-09-17): literal matches over Linear `searchIssues` (archived and comments included):
TERM 'ks727-errorhandler-class-guard': scanned 91 over 2 page(s); literal hits 12
    KS-1141 \[Backlog\] QUESTION: are `crypto-agility.guard.test.ts:44` SCAN_DIRS and `ks727-errorhandler-cla     KS-1155 [Backlog] packages/shared tree-walking guards exceed vitest's 5 s default under fleet load — 5      KS-573 [Done] systemTest (Schemathesis): assert the shared control-byte boundary is mounted in ever     KS-727 [Deployed to UAT] Security: errorHandler returns err.message verbatim on any non-production NODE_ENV -      KS-764 [Done] Security: decideKeyRevoke has no organisation arm — an ORG_ADMIN can revoke a sibling     KS-818 [Done] KS-800 follow-up: four small scanner and harness items from the re-gate (G-05…G-08)     KS-830 [Canceled] KS-727 guard suite: three CONTROL cells are red on develop — referral, staking and vc     KS-832 [Done] KS-800 scanner residues from the KS-817/831 gate: a silent guard-side false clean, an     KS-833 [Done] KS-818 residues from the #834 gate: a live entry-point list left behind, and three co     KS-845 [Done] Close the NINE bare `app.listen(0)` sites in auth and referral — the intermittent-red     KS-876 [Done] KS-860 guard walks services/ only — test listeners under packages/ are unguarded, inc     KS-953 [Backlog] CLASS: editing api-gateway/src/index.ts silently reddens packages/shared, and nothing TERM 'driveThroughRoute': scanned 0 over 1 page(s); literal hits 0 TERM 'EXPECTED_HANDLERS': scanned 127 over 3 page(s); literal hits 1     KS-830 [Canceled] KS-727 guard suite: three CONTROL cells are red on develop — referral, staking and vc TERM 'demo-service/src/middleware/errorHandler': scanned 90 over 2 page(s); literal hits 0 TERM 'headersSent': scanned 1 over 1 page(s); literal hits 1     KS-815 [Deployed to UAT] Security: two live api-gateway verify routes parse a body no control-byte guard inspe TERM 'finalhandler': scanned 0 over 1 page(s); literal hits 0 None concerns demo-service's error handler (`demo-service/src/middleware/errorHandler`0 hits;`finalhandler`0; the one`headersSent\` hit, KS-815, is an api-gateway verify route). Filed new. The KS-727 guard test-quality findings (F2/F3) are KS-1181.
