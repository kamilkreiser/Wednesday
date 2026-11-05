GO WITH NOTES

# Gate 201 - Secuura/Blockchain PR 2011 (KS-1185 F2+F3), round 1 of 2, tier 2

Subject: refs/pull/2011/head = 40d3f2470d4a7d4e148c55e7fdc8c6c211015bab (fetched by me from origin into my own clone; the shared checkout did not hold the object, so I cloned it locally and fetched in the clone only). Base 5fc5569ed96a; develop cb1cadfa2ee4. Runtime: Node v26.8.1 (NOT LTS - the repo rule says LTS only; results are as measured on 26, like the seat's). Evidence class for everything below is MEASURED AT RUNTIME unless marked READ ONLY.

## BLUF
Tier-2 claim holds: the diff changes no response status, body, header or auth path. Base vs head on the real route: 12 of 12 scenarios same (status, body, content-type/headers, pending-doc deletes), the only differing field being the per-request completedAt timestamp. The only behavioural change is one log line (error -> warn with status) on a late request error after the status line. Seat's numbers reproduce. Three notes, no blockers.

## Q1 Scope / no response change
- Exactly 4 paths (diff --name-only base..head): verification.ts, the new test, 2 docs fragments. In verification.ts: doc comment on ORIGINATE_FORWARD_TIMEOUT_MS, `let decidedByStatus` (+ assignment in the response callback), the 'error' listener branch. Nothing else (diff read whole).
- Probe: ev_matrix_head.jsonl vs ev_matrix_base.jsonl (probe source: _quarantine_2026-11-05/matrix_*_copy.ts). 12 scenarios: 201 ends; 401 ends; 500 ends; 201 then silence; 401 then silence; silent (error before status); closed port; socket destroyed before status; 201 + malformed chunk framing; 201 + invalid header (parse error before status resolves); garbage status line; 201 then mid-body destroy. 12 of 12 same. Normal 2xx (200, deletes 1), non-2xx (502, deletes 0), error after status (200/502 same as base), error before status (502 same as base).
- Only log differences: s3a, s3b, s5 (error after status decided): base `error "Failed to forward approved document to originate"` -> head `warn "Approved-document forward: originate's reply body did not finish..."` with {status}. All error-before-status logs identical to base.
- Not a tier-1 change; no STOP condition.

## Q2 F3 / F2
- F3 log: warn, carries `status` (201/401 observed). Marker search over all log args of all 12 head scenarios (planted MARKER in chunk framing, header value, status line): 0 hits. Node's parse-error messages are generic ("Parse Error: Invalid character in chunk size"), so err.message carried no upstream bytes in any shape I could build. See N2 for why this is a property of Node, not of the code.
- F2 PIN: 102-drip every 300 ms x 2.4 s against a 1 s bound -> 200 after >2 s; green on base AND head (it is a pin, not a fix); a wall-clock mutant reddens it (below). Control (silent originate) still 502 at the bound.

## Q3 Mutants (restored by sha256 each time: 456ff67f...)
Seat's: m1 `if (decidedByStatus)` -> false: 3 failed (the 3 F3 cells). m2 status never recorded: 3 failed. m3 wall-clock timer added: 1 failed (the F2 PIN). Mine: own1 record status only when 2xx: 1 failed (the 401 cell). own2 drop `error: err.message` from the warn meta: SURVIVES (7/7 green) - see N2. Logs ev_mut_*.log.

## Q4 Suites
- Four approve-forward files, head: 4 files / 47 of 47 pass (ev_four_head.log). Base (new file added to base tree): 3 failed / 44 passed, the 3 F3 RED cells red by assertion (ev_four_base.log). Matches the READY.
- Full api-gateway suite, --maxWorkers=2, shared node_modules stale: head 57 files failed / 180 tests failed; base 58 / 183. Failed-test set diff = exactly the 3 F3 cells (fixed on head); no new failure. The other 180 are environmental (`boundedJson is not a function`, `Cannot find package '@secuura/shared/zod3-compat'`), same on base. Cannot reproduce the seat's 1630/0-failed here; that needs a fresh install - NOT COMMISSIONED beyond classifying.
- tsc --noEmit: rc 2, 5 errors, all TS2305 on stale @secuura/shared (index.ts, admin.ts, platform.ts x2, proxy.ts); identical set on base; none in PR files. Not the seat's rc 0 - environment (stale shared build). check:test-types: rc 1 with the same 5 stale-build errors, none in PR files; NOT a clean measurement.
- eslint (verification.ts + new test): rc 0, no messages.
- docs-fragments check: OK (flow 157 new / cheat 157 new, lint clean). Planted unbalanced <div> + number token in the cheat fragment: FAIL, rc 1 (tag-balance finding). It printed ADVISORY lines about the committed page differing from the render; not compared to base (N3).

## Q5 Merge onto develop cb1cadfa2ee4
`git merge-tree --write-tree head develop`: rc 0, tree 27cb835f96b5c340ae7ca4832155772690631844. PR 2007 paths: base..develop = 9 files (api-gateway redis.ts, admin.ts, 5 tests, 2 KS-1262 fragments); shared with PR 2011's 4 paths = 0; planted control (one PR path injected into the develop list) reads 1. No conflicts.

## Q6 Seat's candidate ('end' listener logs "document forwarded" on any status) - NOTE only
CONFIRMED. verification.ts:604 logs info "Workflow approved - document forwarded to originate" in the 'end' handler regardless of status; measured s2 (401) and s2b (500): info line logged, route answers 502. Unchanged by this PR; outside F3. Route to a ticket.

## Findings
- N1 (Low, note): The doc comment says "the real originate sends none" (no 1xx). READ ONLY - I did not verify against services/originate; the PIN cell tests the gateway, not that claim. Owner may soften or cite the file.
- N2 (Low, note): the warn line still passes `error: err.message` to the log, and no cell asserts it (own2 survives). Today safe (Node's messages are generic; timeout message is ours), but if a message ever carried upstream bytes this line is where it would leak. Fix-shape: a test asserting the meta keys are exactly {status, error} and a MARKER-in-chunk cell asserting the marker is absent from the log args.
- N3 (Low, note): level change error -> warn also applies to a late error after a NON-2xx status (401/5xx), where the caller got 502. The warn text ("after its status line had decided the forward") reads fine, but alerting keyed on the error level will no longer see these. Intentional per the seat's pick; flag for the owner of any such alert. Also: docs-fragments ADVISORY (committed page vs render) not checked against base.
- N4 (Info): environment: Node 26 non-LTS; stale shared node_modules; tsc/test-types/full-suite cannot be taken as clean here (classified same-on-base).

## Not done / boundaries
No fix, no box, no Linear/GitHub post. The shared checkout was only read (cat-file, remote -v, config read); the PR head was fetched into my own clone at ./clone. Own artefacts: clone/ (incl. api-gateway-base copy), _quarantine_2026-11-05/, ev_*.log/jsonl, verification.head.orig, cheat.orig.
