matches 1
=====MSG 2026-09-16T22:31:17.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 3995
Seat A

## BLUF
- The KS-1187 severity reads are done, and ONE facts comment is posted on KS-1187: 8a59cf75-c4cc-44a5-ac71-b6e3dd853f92 (anchors 6/6). Measurement only; nothing built; nothing to Peter or Stuart; named in no PR.
- **Read (2), MEASURED in-process:** originate routes what the absolute-form bypass delivers upstream. `POST /api/gdpr/erasures` reaches `POST /erasures`; `GET /api/gdpr/erasures/abc` reaches `GET /erasures/:externalRef`. The `/api/v1/...` forms reach no route (404). **None of the five spellings reaches any route** (404 each). Positive and negative controls behave.
- **Read (1), READ only:** every in-repo edge forwards `/api/` with `proxy_pass …$request_uri`, and the demo has Caddy in front. Whether nginx or Caddy passes an absolute-form line through is UNMEASURED.

## Recommendation
Re-raise Kam's card with these reads. The open severity condition is the edge. Closing it needs one request through a real nginx/Caddy front end, which is your call; I have not done it and will not without your word.
Next from me, unless you say otherwise: A16 KS-1050 (a slot is free: #1014 + #1017 open).

## Detail
- **Instrument:** `5_Project_History/2026-09-17_seatA-3rd/ks1187/read2_harness.ts` (sha256 b9bcb956…), run by `tsx` with its cwd in my worktree's services/originate.
  - gdpr.ts blob a1c7482a2 = develop 7e89318bc. DATABASE_URL pointed at 127.0.0.1:9 (closed); no DB, no stack.
  - It imports the real gdprRouter, mounted as originate's index.ts:288, on a bare express 4.22.2 app with an unrouted 404 after it.
  - In memory only: the router-level authenticate() is a pass-through (1 layer), and all 17 route layers' handlers are a 299 recorder naming the route reached. That is routing only, not auth or roles.
- **Rows:** P1 `POST /api/gdpr/erasures` 299 → POST /erasures · S1 `%65rasures` 404 · S2 `./erasures` 404 · S3 `erasures;x=1` 404 · S4 `/api/v1/gdpr/%65rasures` 404 · S5 `x/../erasures` 404 · N1 `not-a-route` 404 · U1 `POST /api/v1/gdpr/erasures` 404 · U2 `GET /api/gdpr/erasures/abc` 299 → GET /erasures/:externalRef · U3 `GET /api/v1/gdpr/erasures/abc` 404.
- **Where the request lines come from (READ from the gates' records):**
  - U1-U3 and P1-as-bypass are the upstream lines in the #1011 round-1 gate's evidence/bypass_run.out. Absolute-form arrived upstream as origin-form `POST /api/gdpr/erasures` in test and production mode, arbitrary host and user role alike; the v1 variants arrived as `/api/v1/...`.
  - S1-S5 are the spellings in verdict_1011r2.md :87-90. It quotes the upstream line for `%65` and `x/../`; for `./` and `;x=1` it records a hit without quoting the line, so those rows assume the path arrived as sent.
- **Runs:** 4 attempts, all recorded. #1 MODULE_NOT_FOUND (express resolved from the records folder; fixed by resolving through gdpr.ts's createRequire). #2 `DATABASE_URL environment variable is required` at originate config.ts import. #3 the 7 briefed rows. #4 adds U1-U3.
  - After every run: the originate porcelain, including ignored files, was unchanged; the worktree porcelain was 0; no node listener of mine remained. The listeners seen were yours (the KS-1201 clone) and the #1014 gate's.
- **Not measured:** originate's authenticate()/requireRole on a forwarded connector bearer; its full middleware chain (index.ts:215-257 READ: no req.url rewrite; the provenance middleware's internals not read); the edge.
- **Read (1) detail on the ticket:**
  - the Caddyfile:33-35 → nginx-gateway 6882 → nginx-demo.conf:410-419 (proxy_pass :418) chain;
  - api-gateway has no compose `ports:` (control: 8 other services do);
  - nginx.conf:184-185 (e2e) and nginx-production.conf:347-350 (production compose) behave the same way;
  - services.bicep:576-585 is the template of the deleted estate;
  - the citation drift: :401/:337 are /health/deep, the /api/ lines are :418/:349.
- **State:** #1017 @ cbe29597d (gate being drafted, no GO); #1014 @ 9ba0caf78 (gate running, no GO); develop 7e89318bc. Nothing deployed.

