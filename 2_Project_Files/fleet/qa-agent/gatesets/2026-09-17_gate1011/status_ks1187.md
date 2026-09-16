hits: 1
SUBJECT: [Secuura/Blockchain -> Wednesday] STATUS: KS-1187 filed (Urgent) - absolute-form erasure-door bypass; originate does NOT re-check subjects:erase (READ)
FROM: secuura-blockchain <secuura-blockchain@agentmail.to>
TS: 2026-09-16T18:55:18.000Z
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}
----
Seat A

## BLUF
- F-1011-4 filed as KS-1187: Urgent, Backlog, board account, related KS-843. KS-858 is archived, so it is named in the description, not linked. NOT linked to #1011. Not built. No one else told.
- Severity read (i) — originate re-checks subjects:erase? READ: NO. services/originate/src/routes/gdpr.ts:164 is authenticate(); :488 POST /erasures and :523 GET /erasures/:externalRef are requireRole('connector') only (:431); "subjects:erase" appears nowhere in services/originate/src. A scope-less connector that reaches originate executes executeErasureByExternalRef (:498). The user role is refused there by role (READ, not driven).
- Severity read (ii) — does the edge forward absolute-form? UNMEASURED, not stack-free:
  - both compose files publish NO gateway host port;
  - every nginx front proxies /api/ as proxy_pass http://api_gateway_pool$request_uri (nginx.conf:184-185, nginx-demo.conf:401, nginx-production.conf:337);
  - the VM demo's Caddy fronts nginx (Caddyfile:34);
  - the Container Apps template exposes the gateway app directly (services.bicep:576-585, external: true).
  Whether nginx's $request_uri keeps the http://host is the deciding fact. My expectation is origin-form, but that is not measured. The kintsugi front end is outside the repo and not read. The ticket names the instrument that closes each condition.
- Board search quoted on the ticket (absolute-form 1 hit: a KS-858 comment about normaliser cells, not this; subjects:erase 6; erasures 25; proxy.ts 62, all other subjects).

## Recommendation
Nothing needed from me now. Your escalation to Kam can cite: the door bypass MEASURED by the gate; originate's missing scope re-check READ at source; edge exposure UNMEASURED.

## Detail
- .git/config sha change during the #1011 gate: it IS mine. Each "git switch -c <branch> origin/develop" wrote branch.<name>.remote/merge tracking into the shared config. The four entries are ks-1183, ks-871, ks-745 and ks-999; KS-999's was created ~18:31Z, inside the gate's start/mid window. From here, new branches use --no-track.
- Now starting #1011 round 2: D3 (canonical req.path captured at entry for both fields), the three F-1011-5 real-app cells, a tamper table incl. G-NONGDPR / G-V1 / G-D3 / TE and the round-1 source as tampers.

Seat A

