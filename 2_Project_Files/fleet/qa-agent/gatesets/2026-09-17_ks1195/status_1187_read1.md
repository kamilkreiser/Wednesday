matches 1
=====MSG 2026-09-16T22:10:06.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 2192
Seat A

## BLUF
Waiting on your ANSWER to "QUESTION: KS-1195 shape and census" (22:08:12Z); nothing built. The watcher is armed. KS-1187 read (1), the edge configs, is done and recorded locally. Its facts comment waits for read (2), per QUEUE item 4 (one comment for both reads).

## Recommendation
No action needed beyond the KS-1195 ANSWER. One flag for whoever re-raises Kam's card: KS-1187's description cites two nginx lines that now point at /health/deep, not /api/ (Detail).

## Detail
- **Read (1) at develop 7e89318bc**, configs only (record: `5_Project_History/2026-09-17_seatA-3rd/ks1187/read1-edge-configs.md`):
  - **Demo chain:** Caddyfile:33-35 `reverse_proxy localhost:6882` → docker-compose.yml nginx-gateway `"${GATEWAY_PORT:-6882}:80"` (:2275-2276), mounting nginx-demo.conf → `location /api/` at nginx-demo.conf:410-419, `proxy_pass http://api_gateway_pool$request_uri;` at :418.
  - The compose `api-gateway` block (:411-556) has no `ports:` key (control: 8 services do). On compose, the gateway is reachable from outside only through nginx.
  - **nginx.conf:184-185** (e2e override :28) and **nginx-production.conf:347-350** (production compose :395) proxy_pass `$request_uri` the same way.
  - **services.bicep:576-585:** the Container Apps gateway has `external: true` ingress, a template for the estate deleted 2026-07-31.
  - **Citation drift:** KS-1187 cites nginx-demo.conf:401 and nginx-production.conf:337. At the tip those are the `location = /health/deep` proxy_pass lines; the `/api/` ones are :418 and :349. nginx.conf:184-185 is correct.
  - **UNMEASURED, and reading cannot settle it:** what an absolute-form request line becomes on the upstream request after nginx's `$request_uri` and after Caddy's reverse_proxy, and Container Apps ingress's handling. Closing it needs one request through a real nginx/Caddy, which is a front end, so it is your call.
- **Read (2)**, originate's routing of the five spellings in-process, has not started. I will start it on your word, or after KS-1195, per the queue order.
- **State:** develop 7e89318bc; #1014 @ 9ba0caf78 (no GO); 2 of 3 slots free (#1014 open); 0 login_stub listeners at 22:03:10Z. Nothing deployed.

