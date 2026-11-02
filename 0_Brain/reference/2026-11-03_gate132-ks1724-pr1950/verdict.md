# QA GATE 132 - Secuura/Distributed_Secuura PR 1950 (KS-1724, tier 2, Sonnet)

## BLUF
**GO.** One field, `rl=$request_length`, appended last to `log_format secuura_edge`; nothing else touched. nginx -t rc 0 base+head on the repo's image, planted control rc 1. A real container logs `rl=1181` for a 1000-byte POST with every earlier field byte-identical to base. The only consumer (gatewayTimeline parseAccessLine) reads base and head lines identically (28/28 incl. 2 added cells). merge-tree clean, one path. The new field is a number. No FIX-BEFORE-MERGE. Two info notes.
Load: Node v26.8.1 only (not measured on Node 24); nginx image run for real; the demo edge itself / Caddy->nginx chain NOT tested.

## 1. Heads + diffstat
- PR head ce2130fd111c06b6e56669bf41e3760a9b205034 at start AND end (ls-remote; matches Wednesday). Merge-base 0e3a9b65cdd6. develop at start 1439e93e (as briefed); it moved to e7a3b1fb, then fcbe18cc during the gate (PR head did not move; merge-tree re-run below).
- Three-dot diff: exactly `Blockchain/Dev/docker/nginx-gateway/nginx-demo.conf`, 1 insertion, 1 deletion. Nothing else.
## 2. The hunk
`-  'xff="$http_x_forwarded_for" scope=$secuura_limit_scope';`
`+  'xff="$http_x_forwarded_for" scope=$secuura_limit_scope rl=$request_length'; # KS-1724: ...appended last so no field moves`
Changes: one trailing ` rl=$request_length` and a same-line comment after the `;`. Does not change: any earlier field, any other directive, `access_log` binding (line 198), `access_log off` locations.
## 3. nginx -t and a served container (Q2)
Image: `nginxinc/nginx-unprivileged:1.30-alpine`, the tag in `Blockchain/Dev/docker/nginx-gateway/Dockerfile` (compose builds from it; the repo pins by tag, not digest). Local image digest sha256:f5116ed4606f3eb015dd4a8e28cb9b351476dc0ad4bc6e9f93b19cec130cdf03, run by digest. conf mounted as conf.d/default.conf as compose does.
- base: rc 0 (one pre-existing warn: duplicate MIME text/html, line 323). head: rc 0 (same warn). planted (`log_formatX`): rc 1, "unknown directive". (logs/nginx_t_*.log)
- Served base and head containers, identical requests (POST 1000 bytes with X-Forwarded-For, and a GET), no upstream so both answer 502 identically:
  - base: `1.2.3.4 - - [..] "POST /api/x HTTP/1.1" 502 109 "-" "g132-probe" xff="1.2.3.4" scope=edge`
  - head: same line + ` rl=1181` (GET: ` rl=83`). With ` rl=N` stripped and the time second normalised, `diff` base vs head = empty (rc 0). Field order and format unchanged. (evidence/log_base.txt, log_head.txt)
  - 1181 = request line + headers (~181 bytes incl. the extra headers my curl sent) + 1000 body; the author's 1149 is consistent with fewer headers.
## 4. Consumers of the log format (Q3)
- Method A: recursive grep (excluding node_modules/.git) for `secuura_edge`, `xff=`, `parseAccessLine`, `access.log`, `/var/log/nginx`. Positive control: the grep finds the format definition (nginx-demo.conf:111) and the `access_log ... secuura_edge` binding (:198). Method B: `git grep` on HEAD, same hits. Method C: log shippers/tailers (loki/promtail/alloy/fluent/logstash/fail2ban/goaccess), `docker logs` + gateway, `$status`/`body_bytes_sent`.
- Consumers found: ONE parser: `systemTest/akto/src/scan/gatewayTimeline.ts` `parseAccessLine`/`foldGatewayLog` (fed by `docker logs`). It uses a regex `[date] "req" STATUS \S+ "ref" "ua"` with NO end anchor and captures only time, status, UA; trailing fields are ignored, so a new last field cannot shift anything. Not positional splitting.
- `observability/loki/alloy.river`: whole-line shipping, `stage.json` (non-JSON nginx lines pass through untouched), drop on `"level":"debug"`; no nginx-field parsing. Unaffected.
- Run: real `parseAccessLine` via vitest (`vitest.unit.config.ts`, `--root` my clone) on the REAL base and head container lines: same status, UA, epoch second-for-second; foldGatewayLog counts 2 requests; control `parseAccessLine('nope')` = null. 28 passed (26 existing + my 2; my test file is at scripts/g132_head_line.test.ts, moved out of the clone's tree after the run).
- No other consumer in the repo (docs mention `docker logs` for humans only).
## 5. No request answered differently (Q4)
The diff touches only the `log_format` string; `log_format` is evaluated only at log time. Corroborated: base and head returned identical statuses/bodies sizes (200 /health, 502, 502; 109 bytes) in the served test. Not tested against real upstreams.
## 6. merge-tree (Q5)
`merge-tree --write-tree` onto develop 1439e93e: rc 0, tree 1125c313; `diff --stat develop..result` = nginx-demo.conf only, 1+/1-. Re-run onto develop fcbe18cc (latest at end): rc 0, tree fcbe18cc..., single path (see logs/merge_tree*.log).
## 7. ks1346 logging rule (Q6)
`$request_length` is a byte count (an integer the server computes), not a request-supplied string. It cannot carry header/body/URL content, so no secret/value leak. Complies. (Existing fields `$request`, xff, UA already log request-supplied strings; unchanged and out of scope.)
## 8. Findings
- G132-F1 (info): `$request_length` counts bytes nginx has read, so for requests rejected early (413 over `client_max_body_size` 12m, or a client_body_timeout abort) rl can be less than the full intended size. For the "measure first" purpose, read rl together with the status field: a 413 line shows at most what nginx consumed, not the attempted size. Also rl includes request line + headers, not just body (author already says so in the comment).
- G132-F2 (info): the image is pinned by tag (1.30-alpine) in the Dockerfile, not digest; gate ran it by the digest the author named, which equals the local image. Nothing to change.
- G132-F3 (info): takes effect on the demo only when a deploy seat ships the file and nginx reloads (author already says so). Existing log lines are not rewritten; consumers of mixed old/new lines are fine (regex is end-unanchored).
- No recommended items; no FIX-BEFORE-MERGE.
## 9. NOT TESTED
- The live demo edge / any box, Caddy -> nginx chain, HTTP/2 request_length semantics, a body over 12m producing 413 (F1 is from nginx semantics, not measured), real upstream responses, the four platform suites, anything on Node 24, GitHub PR body/checks (not read; used the author's READY mail copied to evidence/ready_s13_pr1950.txt).
## Cleanup
Containers started: g132-t-base, g132-t-head, g132-t-planted (--rm, exited), g132-base, g132-head (docker rm -f); 0 g132 containers remain. No background processes of mine remain (the vitest/node processes visible on the host belong to the Spark operator). Clone has push disabled; nothing written to GitHub/Linear/mail. Note: a ssh wrapper script (scripts/ssh_ro.sh) carries the read key path as core.sshCommand; no key copied.
