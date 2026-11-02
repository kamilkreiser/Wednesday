Seat S 13th

ADDENDUM: PR 5 = add the request size to the demo edge access log (Refs KS-1724). Kam ruled it; it queues AFTER your PR 4 work and does not delay it.

RULED BY KAM, NOT YET IN AN ARTEFACT
- card secuura-ks1724-edge-request-size-measure-1102 = a, 2026-11-02 19:15:02 AEDT, option text verbatim: "add the request size field to the demo edge log format (one nginx log line and a reload, by a deploy seat under the October grant), read sizes after 7 days, then bring a lower-limit proposal back to you". This is the card built on your KS-1724 finding (the eight >=10 MB body limits).

WEDNESDAY'S DESIGN INSIDE THAT RULING (why a PR, not a box edit): the edge conf is BIND-MOUNTED from the box's repo checkout (docker-compose.yml:2298 at develop 66a36e3f777d: `./docker/nginx-gateway/nginx-demo.conf:/etc/nginx/conf.d/default.conf:ro`), and nginx-production.conf:14 says the live edge conf is mounted by both boxes. A box-only edit would be drift that the next rsync deploy reverts mid-measurement. So the line lands in the repo first; a deploy seat then ships exactly the merged file to demo.

THE CHANGE (yours to measure and build; tier 2 by Wednesday's default, Sonnet gate; say if you see a reason for tier 1):
- File: Blockchain/Dev/docker/nginx-gateway/nginx-demo.conf. At develop 66a36e3f777d the format is `log_format secuura_edge` at lines 111-112 (+ continuation lines; read the whole directive), used by `access_log /var/log/nginx/access.log secuura_edge;` at :198.
- Add nginx's `$request_length` (request line + headers + body, bytes) as ONE new field at the END of the format, so every existing field keeps its position. A short label is fine (e.g. `rl=$request_length`); say what you chose.
- BEFORE writing it: search the repo at develop for every consumer of this log format or of the edge access log (scripts, runbooks, fail2ban/alerting, log parsers, tests that pin the format) with a positive control, and say whether any parses by field position. A consumer that would break is a QUESTION to me, not a fix of yours.
- Proof: `nginx -t` on the changed conf in a throwaway nginx container of the SAME image tag the Dockerfile pins (your own scratch container, removed after, never a box), plus one request through it showing the new field with a known body size (e.g. a 1000-byte POST logs a request_length >= 1000), and the same request against the base conf showing the field absent. No other line of the file changes; nginx.conf and nginx-production.conf are NOT touched.
- PR title and commit subject start with "Refs KS-1724: " (house form). No closing keyword. Test Evidence block as for your other PRs, including NOT run (no box).
- Through the push queue like your other PRs; READY FOR GATE to me as usual.

PROVENANCE:
- Kam's ruling + option text | decisions.json card secuura-ks1724-edge-request-size-measure-1102 (status ruled, ruled_choice a, ruled_ts 2026-11-02T19:15:02+11:00), read by Wednesday 19:3x | read 2026-11-02
- bind mount at docker-compose.yml:2298; log_format at nginx-demo.conf:111-112; access_log at :198; client_max_body_size 12m at :215; "mounted by both" at nginx-production.conf:14 | git show 66a36e3f777d:<path> in Wednesday's read-only clone, 19:3x | read 2026-11-02
- the deploy step (lane D seat, after merge) is Wednesday's to brief, not S 13th's | Wednesday's design in this mail | read 2026-11-02

Wednesday

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-02 19:38
