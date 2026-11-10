B1483 DRAFTER REPORT (Opus drafter for Tuesday), kit `2026-11-10_B1483_SEAT-N121_nexusai-write-gate-case-fix.md` in this folder. Drafted Tue 10 Nov 2026 22:06:26 to about 22:20 AEDT. The drafter built nothing, pushed nothing, touched no hosted host, no Jira, no mail. Reads: `gh api -X GET` under the NexusAI `GH_CONFIG_DIR`; a scratch clone (`git clone --no-hardlinks` of `.tools/b1480/clone`, push URL set to `invalid://nopush`) in the session scratchpad; every git write verb ran only in that scratch clone. Nothing was written under `/Volumes/Datasec_DEV/!CODING/`.

## BLUF
- **The fix is two characters plus two comment lines:** add the `i` flag to both router-level gate regexes in `backend/server.js` on `b1480/nexusai-s-viewer-write-gates` (`/^\/config\/?$/` at `:22062` and `/^\/[^/]+\/?$/` at `:21985`, at `f913fef`). Measured in a bare Express 5.2.1 app against 51 raw request lines: that gate refuses every form Express routes to the gated handler, and nothing else. The other 17 gates sit inside their handlers and need no change.
- **I chose the `i` flag over the verifier's "better" option, a gate inside the router's own routing.** A mirror `express.Router()` gate measured exactly the same on all 51 lines. But it adds runtime route registrations, and the committed route census (C1 "live route set equals the committed inventory rows") and the inventory read the live router, so it would move them. Tuesday may overrule this (D2).
- **What the kit covers:** one fix commit A on write-gates (fix plus a new cell file of 3 tests). Red-first runs against `f913fef` with two plants. A counts commit B. A merge commit M of B into column-mapping, then a counts commit K. Two plain pushes. The predicted pairs are 5516/332 for write-gates and 5519/333 for column-mapping. Both are PREDICTED, not measured.
- **Decision for Tuesday (D1, measured):** the counts commits on the stack conflict at landing if `l1-design-inventory` lands on its own with its own counts commit first (scratch `merge-tree` rc 1 on `scripts/verify-expected-counts.json`). The stack lands conflict-free only from its top (rc 0 onto `849b808c`), or after a later regeneration (C-57).

## WHAT EXPRESS ROUTES (MEASURED-BY-DRAFTER)
Instrument: `/private/tmp/claude-501/-Volumes-Datasec-DEV-TUESDAY/90f78cba-aa68-4adc-98aa-7d2087ff2f7f/scratchpad/expr/measure.js` (sha256 prefix `e92a9e90ba13`; source in the appendix). It requires `express` from `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/.tools/b1480/clone/node_modules` (read-only) and prints `{"node":"v26.13.0","express":"5.2.1","router":"2.2.0","pathToRegexp":"8.4.1"}`. Those equal `package-lock.json` at `f913fef` (lines 3578-3579 `express` 5.2.1, 6185-6186 `path-to-regexp` 8.4.1, 6734-6735 `router` 2.2.0, read with `git show f913fef:package-lock.json | grep -n -A3`). `package.json:58` is `"express": "^5.1.0"`. `package*.json` are equal at `849b808c` and `2a584f7` (`git diff --quiet` rc 0; control `-- backend/server.js` rc 1).
The handler routers are built exactly as the product builds them: `express.Router()` with no options (`backend/routes/sustainability.js:164`, POST `/config` at `:339`; `backend/routes/feedback.js:16`, PATCH `/:id` at `:337`, DELETE `/:id` at `:487`). `server.js` sets no routing option (`/usr/bin/grep -n -i` for `case sensitive|casesensitive|strict routing|app.set(|app.enable(|methodoverride` gives one hit, `app.set('trust proxy', 1)` at `:1080`; control `requireAdminFor` 38 hits) and rewrites no `req.url` (pattern count 0; control `req.path` 28).
The app mounts four gate designs in turn: none, old (the branch's regexes), regex-i (the same with `i`), mirror (an `express.Router()` that registers the same method and path). Raw sockets send the request lines, so no client normalises them. Runs: 22:09:01 (printed) and 22:17:35 to 22:17:38 (to a file, rc 0, 52 lines).
Counts over the second run, request lines that reached a handler: none 25 (23 on gated routes, plus the two ungated feedback writes `POST /` and `/:id/triage` kept as controls); old 9 (the 2 controls plus **7 sustainability case forms past the gate**); regex-i 2 (the controls only); mirror 2 (the controls only).
| request line (raw) | none (handler reached?) | old gate | regex-i | mirror |
|---|---|---|---|---|
| POST /api/sustainability/config | 200 handler | 403 | 403 | 403 |
| POST .../CONFIG, .../Config, .../cOnFiG, /API/SUSTAINABILITY/CONFIG | 200 handler | **200 handler** | 403 | 403 |
| POST /Api/Sustainability/config | 200 handler | 403 | 403 | 403 |
| POST .../config/ | 200 handler | 403 | 403 | 403 |
| POST .../CONFIG/ | 200 handler | **200 handler** | 403 | 403 |
| POST .../config?x=1 | 200 handler | 403 | 403 | 403 |
| POST .../CONFIG#x (raw fragment) | 200 handler | **200 handler** | 403 | 403 |
| POST http://127.0.0.1/api/sustainability/CONFIG (absolute form) | 200 handler | **200 handler** | 403 | 403 |
| POST .../config//, ...//config, /api//sustainability/config, //api/... | 404 | 404 | 404 | 404 |
| POST .../config/., ..././config, .../x/../config | 404 | 404 | 404 | 404 |
| POST .../%63onfig, .../%43ONFIG, .../con%66ig, /api/%73ustainability/config | 404 | 404 | 404 | 404 |
| POST .../config%2F, config%20, config;x, config.json, configx, config/x, `\config` | 404 | 404 | 404 | 404 |
| POST /api/su(U+017F)tainability/config raw UTF-8 / its %C5%BF form | 400 / 404 | same | same | same |
| `post` (lower-case method) .../config | 400 | 400 | 400 | 400 |
| PATCH /api/feedback/zz, /api/FEEDBACK/zz, /Api/Feedback/ZZ, zz/, a%2Fb (id "a/b"), a;b, %7a%7a (id "zz"), `.`, `..` | 200 handler | 403 | 403 | 403 |
| PATCH /api/feedback/zz//, /api/feedback//zz | 404 | 404 | 404 | 404 |
| DELETE /api/feedback/zz, /API/FEEDBACK/ZZ/, zz?x=1 | 200 handler | 403 | 403 | 403 |
| DELETE /api/feedback/zz//, //zz | 404 | 404 | 404 | 404 |
| POST /api/feedback/zz/triage, POST /api/feedback/ (ungated controls) | 200 handler | 200 handler | 200 handler | 200 handler |
| GET /api/sustainability/CONFIG (control: GET untouched) | 200 | 200 | 200 | 200 |
Reading: Express routes any letter case in any segment (mount prefix included), one optional trailing slash, a query, a raw fragment, and the absolute form. It does not route doubled slashes, percent-encoded letters, dot segments or look-alikes. **The gate need not refuse the second group, and the kit's Test 3 pins that boundary.** The product differs from the bare app in one place I know of: `PATCH /api/feedback/a%2Fb` answers 400 in the product (verifier's probe, viewer, base and head) and 200 in the bare app, so a product middleware refuses `%2F` first. That does not weaken the gate. The verifier's product probe agrees with this table on every row both sources cover (`probe-base.json`, `probe-head.json`: `CONFIG`, `Config`, `/API/...` read 200 at base and head; `config/` and `?x=1` read 403 at head; `//config` and `%63onfig` read 404).

## OTHER FACTS (MEASURED-BY-DRAFTER, with clocks)
- 22:07:14, `gh api -X GET`: main `849b808c567e4d31d78e2d50b582540ae1920c67`. `b1480/*` refs: l1 `70709c61...`, session-revocation `5fbad1ba...`, setup-column-mapping `2a584f7d...`, viewer-write-gates `f913fefb...`. Open PRs 0. `matching-refs/heads/b148` length 4.
- Stack: `git log --oneline 70709c6..f913fef` gives 5 commits. `2a584f7` has parents `18a0b1c5716387d1495e6447ea05997f68c58012` and `f913fef`, and its message form is quoted in the kit. `git diff --stat 70709c6..f913fef`: 8 files, +315/-72.
- Gate code at `f913fef` (`git show f913fef:backend/server.js | sed -n`): `feedbackItemWriteGate` at `:21984-21990`, `sustainabilityConfigWriteGate` at `:22061-22067`. At `2a584f7`: `:21967` and `:22044`.
- Counts file: 5493/326 at `849b808c`, `70709c6` and `2a584f7` (`git show`).
- Test tables: rd958 has 16 route rows and rd793 has 4 (`grep -E "^\s+\['(POST|PATCH|DELETE)'" | wc -l`).
- Scratch fix (22:13 to 22:14): exactly the two regex edits (python replace; each pattern occurred once, 1 1). `git diff -U0`: 2 hunks. `node --check` OK. Scratch commit `1567395469f0bb30db84506ee9aa15b4f9079653` on `f913fef`. `git merge-tree --write-tree` rc 0 against `2a584f7` (tree `23675cf3...`), against `849b808c` (`2a406c5b...`) and against `5fbad1b` (rc 0, run alone with no pipe).
- **Counts landing (D1), with the firing control.** Scratch counts commit `a490f767...` on the scratch fix (5516/332). Scratch l1 counts commit `f8cbe337...` on `70709c6` (5507/329), landed on `849b808c` by `commit-tree` as `9060bc65...`. Then `merge-tree` of `9060bc65` with `a490f767` gives **rc 1, `CONFLICT (content): Merge conflict in scripts/verify-expected-counts.json`**. The same without the gates counts commit (`1567395`) gives rc 0. `a490f767` straight onto `849b808c` gives rc 0. `2a584f7` merged with `a490f767` gives rc 0, so the kit's step 5 merge is clean. The column-mapping counts commit onto main is UNMEASURED; it is the same shape as the rc 0 case.
- Port slots (22:12:05, the helper's formula `sha256(realpath) readUInt32BE(0) % 19` over every `b1*-nodot/*`, `b1*-trees/*` and `.tools/b1*/*` worktree or clone; control `b1430-nodot/b1` = 6, the B1480 kit's value): **slots 1 and 8 hold no tree**. Kit trees: `b1483-nodot/v36` and `v37` at slot 1, `v6` and `v33` at slot 8, `.tools/b1483/probe4` at slot 13 (one other tree there, `b1431-trees/t4`).
- 22:12:15: lock held by `qa-b1433b-gate`, `queue-jest` 1 ticket, load 18.56 21.38 22.51. Live panes: `Datasec/HPSM-POC-D59`, `fleet-monitor`, `wednesday`. Ports 9900-9939: 0 listeners (control 11 overall).
- Auth middleware (for the records line): `backend/server.js:2628` at `f913fef` is `if (req.path.startsWith('/api/'))`, case-sensitive. So an anonymous `/API/...` gets the `/login` redirect (302) rather than 401. The verifier's probe reads 302 on all four upper-case anonymous rows at base and head. No handler is reached, so it is not a bypass, and it is outside these branches' lines.
- Input files (line count, sha256 prefix): VERDICT-gates 51 `4b5c3fc99f72`; VERDICT-colmap 41 `f00d92eedcad`; probe-base.json 293 `2c74d9245a1b`; probe-head.json 293 `6b99deec762a`; probe-test.js.txt 75 `d4766a312120`; B1480 kit 258 `21b6bba133cf`; ALL-LANES ADDENDUM-1 14 `0eea2af700e5`; B1480 STATUS 181 `5581f8e086a1`; B1480 HANDOVER 33 `d40952d84905`.

## PREDICTED (not measured; the seat measures)
- Pairs: write-gates 5513/331 + 3/1 = **5516/332**; column-mapping 5516/332 + 3/1 = **5519/333**. The builder measured column-mapping as write-gates + 3/1 (B1480 STATUS :120).
- Red-first at `f913fef`: Test 1 is red on exactly 3 of 80 rows (upper, title and upper-slash of the sustainability config). Test 2 (administrator on the variant forms) and Test 3 (boundary) are green. Plant P2 (a case-sensitive feedback regex) turns 4 rows red. Plant P3 (the costs handler gate removed) turns 4 rows red.
- **Test 2's administrator statuses on the non-canonical forms were not measured on the product.** The verifier drove the variants as a viewer and as anonymous only. The kit makes any unexplained difference a STOP.
- Lock hold: about 90 minutes once the waiter's turn comes (4 verifies at about 20 to 23 minutes each, RELAYED from B1480 STATUS :80, :91, :101, plus about 5 minutes of red-first). Time in the FIFO before that: UNMEASURED.

## DECISIONS FOR TUESDAY
- **D1 Landing with counts commits.** Option one: land the stack from its top. The column-mapping PR carries l1, the gates and column-mapping, with counts 5519/333. Option two: land l1 first, then regenerate the counts on each later branch after a forward merge of main (C-57), which is outside this kit. The independent branch `session-revocation-clarification` (5499/328) also conflicts on the counts file with whichever lands second. That is the usual C-57 regeneration.
- **D2 Design.** The kit builds the `i` flag. If Tuesday wants routing and gating to share one matcher (the verifier's "better"), the measured cost is new runtime routes. The census C1 and the inventory would then need a regeneration, which this kit forbids. It would need a different kit.
- **D3 Counts rule.** The B1480 kit's COUNTS AT LANDING rule 3 says counts commits come only from a written ADDENDUM. This kit is written to be that instruction for exactly the two branches, on main `849b808c`, with the heads the seat prints. It has REFUSE 5 and the (d) check in case main's counts move.
- **D4 Stamp.** HARD STOP should allow about 90 minutes of lock hold plus the FIFO. The pre-stamp slot count is 5 (four slots and the last line).

## STOP CONDITIONS IN THE KIT (summary)
- Origin heads differ from `f913fef` / `2a584f7` / `70709c6`, or main's counts are not 5493/326.
- A `server.js` hunk outside the two gate functions, or any path outside the 3 owned paths.
- An unpredicted base red, a plant that stays green after two tries, or an administrator variant status it cannot explain.
- A pair different from the prediction that the name comparison does not explain (`PAIR-DIFFERS` ends the chain).
- A merge conflict at step 5.
- A branch head moved on origin before the push, or main moved on an owned path.
- A band listener that stays, or two environmental reds on one tree.
- Jest outside the lock.
- Any hint to open a PR, deploy, regenerate the inventory, write Jira or touch a HELD ticket.

## THE GATE'S MINORS: none is built
- Gates F2: no code, and the kit's partition rule reads it as a false positive.
- Gates F3: held.
- Gates F4: needs a history rewrite, so it is listed.
- Colmap F2: a roles ruling, listed.
- Colmap F3: by design.
- The anonymous `/API` 302: a records line.

## APPENDIX: the measurement script (scratch; the kit does not depend on it)
Gate designs as measured: `old` = `/^\/config\/?$/.test(req.path)` and `/^\/[^/]+\/?$/.test(req.path)`; `regex-i` = the same with `/i`; `mirror` = `express.Router()` with `patch('/:id')`, `delete('/:id')` and `post('/config')` answering 403; `none` = pass-through. Handler routers as in the product. Request = one raw line + ` HTTP/1.1`, `Host: 127.0.0.1`, `Content-Length: 0`, `Connection: close`, over `net.connect` to an ephemeral loopback port, closed after each design. The 51 request lines are the rows of the table above. The script stays at the scratchpad path named above for this session only.
