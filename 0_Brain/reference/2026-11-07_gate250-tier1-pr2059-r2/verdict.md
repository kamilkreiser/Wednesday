| PR | Head | Verdict |
|---|---|---|
| 2059 (KS-1410 with KS-1214), round 2 of 2 | 5d8969b36a24914c24bc6a839f819ec8be3772e9 | GO WITH NOTES |

# Gate 250, Secuura / Blockchain, PR 2059, tier 1, round 2 of 2

## BLUF

All seven of gate 239's findings are closed at this head, by my own read and run. **Nothing here blocks.** Seven new findings, all minor, can all be ticketed.

The new error middleware held. With NODE_ENV=development on a real port, 63 hostile cases got no stack, no server path and no body text out of it, and none into the log. This run used the real `boundedJson` and the real control-byte guard, which round 1 and the seat's new cells both stubbed. Every status matched the parent's. No client input can set `err.status`.

The file-read hole stays closed. Zero hits at head and at 7a644a2dd246. The pre-PR source c5c26b2835df still shows the hole, so the instrument can see it.

Two things need a person:
1. **Three sentences a client human reads are false (R2-1).** Two are in the ticket comments, which the seat cannot delete. A correcting comment is the only remedy.
2. **The middleware is wider than your commission described (R2-2).** It keeps any 4xx, not only 400, 413 and 415. The PR body says so accurately. It cannot be reached from outside today. Wednesday decides whether that is acceptable.

Severity is mine; priority is not.

## Pins (branch `feature/ks-1410-mcp-web-interface-reads-no-server-paths`, and `develop`)

| When (AEDT) | PR branch | develop |
|---|---|---|
| start, 07:49:01 | 5d8969b36a24 | b27f5fb30f4a |
| mid, all-heads fetch, about 08:00 (not stamped) | 5d8969b36a24 | b27f5fb30f4a |
| end, 08:03:21 | 5d8969b36a24 | b27f5fb30f4a |

## 1. Gate 239's findings

| Finding | State at this head | How |
|---|---|---|
| F1 base64 in curl's argv | **Closed.** Residuals: R2-5, R2-6 | MEASURED. A grep for base64 in an argument across all of `MCP Deployment/` finds none. The Jenkins recipe, as text under `sh -e`, sent the right hash for a 5 MB file, which the old recipe could not carry. Recipe hash equals the server's hash on a small file. The guide's size words hold: 750 KB and 767 KB answer 200, 768 KB answers 413. |
| F2 parser and router errors | **Closed** | MEASURED, section 2 |
| F3 sentence | **Closed** | MEASURED. The new sentence on all four routes, including beside content, documentId and contentHash. The old sentence: zero in the guides, spec and fragments, one in a `http-server.ts` comment (the control). |
| F4 stale guide line | **Closed** | READ. `resolved on` has zero hits in the guides. Line 275 now says the server reads no path. |
| F5 spec on one route of four | **Closed.** Residual: R2-7 | MEASURED by parsing the YAML. All four operation descriptions name the refusal. /hash and /verify declare 200, 400, 413. Byte copy identical by `cmp`. |
| F6 guard bound to one identifier | **Closed** | MEASURED. All four of round 1's survivors are now killed, each by AssertionError: /register via readFile, /hash `path` via readFile, guards narrowed to strings, `0` added to the refusal. |
| F7 stale headers | **Closed** | READ. `must stay as it is`: zero. `EXEMPT` survives only in the comment explaining the rename. `HASH_ROUTE` in both files (the control). |

## 2. The error middleware (`http-server.ts:324-344`)

**FAIL conditions, stated first in `evidence/attack.mjs`:** a stack, a server path, error text or a body marker in any response; a status differing from the parent's; the server not answering /health after a case.

**Run:** 63 cases plus one keep-alive check, raw sockets, at NODE_ENV=development, production and unset, with the parent in development as the control. MEASURED AT RUNTIME.

- **A stack, path or body text:** none got out. Covered: malformed JSON on every POST route, a route that does not exist and a GET with a body; bodies carrying a marker; strict-mode strings; 1 MB boundary to the byte; chunked and declared oversize; bad charset and bad encoding carrying a marker; invalid and bomb gzip; undecodable path parameters; aborted uploads; bad chunk framing. The same probes at the parent return `SyntaxError`, `PayloadTooLarge`, stack frames and the marker, so the instrument can see it.
- **The log:** head 0 markers, 0 stack lines, 0 `node_modules`, 0 `unexpected`, with 32 `rejected before` lines in the same file. Parent 4, 285, 162, 8. Lines carry name, type and status only.
- **Statuses a caller relies on:** nothing swallowed. Status equal to the parent on every case. Only 400, 413 and 415 reached the middleware. A keep-alive socket still serves the next request after a chunked 413, at head and at parent.
- **The gateway** is the one in-repo caller (`proxy.ts:1298-1306`). It does `r.json().catch(fallback)` and forwards the status, so the JSON now reaches the admin instead of `Package generation failed`. READ ONLY.
- **An attacker-set `err.status`:** no path found. No route calls `next(err)`; the only `next(err)` in the file is the middleware's own (`:338`). Every route has its own catch. The parser and router create only 400, 413, 415 and 500, plus a 403 for a `verify` option this server does not set. READ, consistent with the 63 cases. A JSON body cannot become an error's status. See R2-2 for what the code would do if one did.

**What reaches a client outside the middleware** (none of it carries server data, all the same at the parent):

| Response | Body | Source |
|---|---|---|
| 404 | Express's HTML, `Cannot GET /nosuch/SECRETVALUE`. It echoes the URL the caller sent, percent-encoded as sent. No stack, in all three modes. | Express default |
| Malformed HTTP, oversize header | Node's bare 400 or 431, no body | Node |
| Body over a structural cap | `Request body exceeds the structural limit (depth)` | `boundedJson`, real |
| Control byte in the body | `VALIDATION_ERROR`, and `details.path` echoes the caller's own key name, for example `SECRETVALUE\u0000 (key)` | real guard |
| Route throws | The constant, from the route's own catch | routes |

The 404 and the guard's `details.path` are the only echoes left. They repeat the caller's own input. That is not the error text the card's title means, as I read it, so I file no finding. If Wednesday reads it more strictly, it is a one-line 404 handler.

**Scope against Kam's card.** The title says "stop echoing error text"; the option he tapped says "on /hash and batch items". The middleware covers every route. That is inside the title and wider than the option's words, and it was Wednesday's call to keep it in this PR. It fails closed and takes nothing from a caller.

## 3. Regression against round 1's security result

Round 1's own `probe.mjs` (67 cases) and `probe2.mjs` (10) re-run unmodified, each with a stub upstream. FAIL: the sha256 of /etc/hosts in a response or an upstream call.

| Source | In responses | In upstream calls |
|---|---|---|
| Head 5d8969b36a24 | 0, 0 | 0, 0 |
| 7a644a2dd246, the commissioned parent | 0, 0 | 0, 0 |
| c5c26b2835df, pre-PR, **my added control** | **3**, 0 | **3, 3** |

**The commissioned parent cannot serve as the positive control.** It already has the fix, so its zeros are correct and say nothing about the instrument. I added the pre-PR source for that. Its /hash returned `sha256:c7dd0e…` for /etc/hosts.

Differences from round 1's recorded head run: the 500s on batch items and the traversal case are now 200 because my stub was up for that run and round 1's was not. The parent gives the same 200s. All other differences are F2's HTML turning into the constant. The traversal case reached the stub still encoded, as `/api/workflow-instances/..%2F..%2Fetc%2Fhosts`, and read no local file.

`http-server.ts` imports only `hashBuffer`. Routes dumped live from Express at `listen`: the same 11 plus the one error handler.

## 4. The round's own diff

- **New outside the findings:** none. 14 paths, all named by a finding or the fragments. Nothing else moved.
- **N1 and N2 stated plainly in the body:** yes, line 42 of the seat's saved body. The saved body and both comment drafts match the seat's recorded sha1s once the trailing newline is stripped, so I read what the record says was posted. I did not read them live.
- **Ticket comments:** from the seat's record, both posted, 0 mention nodes, state, priority and assignee unchanged, read back equal. The content is true at this head except for the clauses in R2-1.
- **Seat's numbers reproduced:** suite 16 files, 169 cells, two runs, on my substrate. Red proof against round 1's seven non-test files: 19 failed of 66, all AssertionError, the same 19 cells as the seat's list (F5b has a new title since the seat tightened it). 42 open PRs is in the push status (the 34 in `overlap_gate.out` is an earlier reading). I sampled 27-of-27 by reproduction, not all of it.

## 5. Merge

`git merge-tree --write-tree` rc 0, tree 11a9f59a4295, no conflicts. Develop is 14 commits past the base, 78 paths, overlap with the PR's 14: 0. Of 1544 heads, 642 are younger than 30 days and 640 of those are unmerged. Five touch a shared path (control: the PR head itself shows 14): KS-1725, KS-1724, KS-1868 (x-mcp-http), KS-1901 and KS-1410's first pass. These are the same five round 1 named as squash-merged leftovers. No younger head touches one, including the seat's items 2 and 3. **No merge-order constraint.** Open-PR state is inferred: no `gh` under the network rule. The seat's gate recorded 42 open PRs and none touching these paths.

## Findings

Each of these **can be ticketed**. None blocks.

### R2-1. MINOR. Three sentences a client human reads are false at this head.
- **"The POST /hash 500 logs the error's name and kind."** PR body line 34, KS-1214 comment `4eb82d57`. It logs `err.message` (`http-server.ts:51`). MEASURED: `[mcp-http] POST /hash failed: The first argument must be of type string… Received type number (5)`. The flow fragment's "log the real error" is the true one. The behaviour itself is fine; round 1 checked it does not leak a secret.
- **"The three guides… state the 1 MB limit."** PR body line 37, the READY, KS-1410 comment `e997f1d3`. Only `generic-http-agent.md` does. `ci-cd-pipeline.md` and `troubleshooting.md` have no such statement (case-insensitive; control: 2 hits in the generic guide). Those two no longer offer `content`, so nobody is misled about a limit.
- **"So does `src/mcp-server.openapi.ts`."** PR body line 37. The zod source has the refusal on /hash and /verify only: no 413, no 1 MB, no batch refusal outside a comment. READ. "Imported by nothing" is true, so no consumer is affected.
- Smaller: "19 of the 66 round-2 cells" counts `ks1901`'s 28 older cells (the flow fragment says it correctly). "NOT run: any running server" sits beside "the real server on a real port"; it means deployed.
- **Fix shape:** edit the body; one correcting comment on each ticket.

### R2-2. MINOR. The middleware keeps any 4xx, wider than the commission and the READY describe. Wednesday's call.
- **Where:** `http-server.ts:342`. The commission says 400, 413 and 415 kept, anything else 500. The READY lists only those three. The PR body line 35 states the real rule.
- **MEASURED** with synthetic errors through the real middleware on a scratch copy (`evidence/mksynth.py`): 401, 403, 404, 418 and 499 are kept, each with code `BAD_REQUEST`. A forged error object with `status: 413` is kept as `PAYLOAD_TOO_LARGE`. 2xx, 3xx, 5xx, 600, negative, NaN, 400.5 and the string `'400'` all give 500. No body or stack on any of those.
- **Not reachable from outside**, section 2. It matters only if a later change forwards a value with a status on it.
- **Fix shape:** an allowlist of the three, anything else 500. Regression: a synthetic error with status 418 asserts 500. READ ONLY for the fix.

### R2-3. MINOR. The middleware's own status read is unguarded, and its headers-sent branch breaks the log rule. Both synthetic only.
- **`:341` sits outside any try.** `describeRejected` is guarded, this read is not. MEASURED: a thrown error whose `status` getter throws, or a revoked Proxy, escapes to Express's default handler: **500 HTML with a stack in development**. With headers already sent, the same error took the **process down**. This is the class `describeThrown` was hardened against (KS-1868).
- **`:337-340`, `next(err)` after headers sent.** Express then logs the full stack and message, not name, type and status. MEASURED.
- **Not reachable today.** No route forwards a caught value or writes before calling `next`. /generate-package swallows its own mid-stream failure (curio C1).
- **Fix shape:** read the status inside the same guard.

### R2-4. MINOR. The new cells leave parts of the middleware's contract unpinned.
MEASURED, `evidence/mut.txt`, 18 plants, every edit anchor-asserted, restored by sha256. 12 killed, 6 survived at 169 of 169. Five of the survivors are below; the sixth is not evidence:
- `err.message` added to the log for everything except a parse error. **E5 pins the log on one error type only.**
- Middleware keeps 5xx too.
- `headersSent` guard removed.
- `sha256:` prefix dropped from the ci-cd recipe, which would register a differently formed hash. **F1a says what a recipe may not do; no cell says what it must.**
- `rejectNulBytes` mounted before the parser, which disables the guard. A shared-package order test may catch this; I did not run that suite.
- **Correction of my own mutant, stated so it is not counted:** G4 is mislabelled in `mut.txt` as a 415. It answered the error text on an aborted request, where the client is already gone, so it is close to equivalent and proves nothing.

One kill is for a narrow reason: a recipe using `--data` instead of `-d` died at F1a only because the same line holds `tr -d`, which satisfies the cell's `-d` pattern. READ from the pattern; I did not plant a form without `tr`.

The real-server file stubs `boundedJson` and the guard, so the suite does not run the combination I ran by hand. **Fix shape:** one real-server cell through the real guard and parser, log assertions on 413 and 415, one positive recipe cell.

### R2-5. MINOR. The Jenkins recipe still fails silently on anything that is not a plain file with a plain name.
- **Where:** `ci-cd-pipeline.md:208-217`. The GitLab loop at `:169` shares the `sha256sum` line.
- **MEASURED** (`evidence/guide_run.sh`, text of the guide under `sh -e`, macOS):
  - A subdirectory in `build/output`: `sha256sum` fails, the pipeline's rc is `cut`'s, `HASH=[sha256:]`, the request goes out, **script rc 0**. My stub accepted it; the real gateway's answer was not measured.
  - A filename with spaces: `$(basename $file)` is unquoted, the JSON breaks, 400 constant, **script rc 0**, nothing registered. That line is older than this PR.
- Round 1's defect was failure on ordinary documents, and that is gone. The silent-failure class remains for these shapes. The GitHub form has `[ -f ]` and is safe from the directory case. The comment at `:74` says a failed substitution "leaves HASH empty"; here it leaves `sha256:`.
- **Fix shape:** `[ -f ]` in the Jenkins and GitLab loops, `curl -f`. READ ONLY for the fix.

### R2-6. MINOR. Two more guides offer `content` with no limit.
`chatgpt-actions.md:150` and `openai-assistants.md:115`. Round 1's fix shape said to state the limit where `content` is offered; F1's "where" named three other files, and F1c checks only the generic guide. A ChatGPT user cannot run `sha256sum`, so this is the guide most likely to hit the 413. READ for the text, MEASURED for the limit.

### R2-7. NOTE. Spec residuals.
- `/register-batch` items are `{type: object}`, so the `error` the flow fragment says the spec declares is declared for `/verify-batch` only. MEASURED by parsing.
- The batch routes state the 413 in prose and declare only 200.
- 415 and the malformed-JSON 400 appear nowhere.
- The published /hash description contains `(KS 1410 round 2)`, which is gate language in a client document.

## Curios, not filed as defects

- **C1.** `POST /generate-package` with `scopes: 5` or `allowedDocumentTypes: {length:1}` sends 200 and part of a zip, logs the throw, and the response had not ended when my 1.5 s wait ran out, in all four runs, parent included. Older than this PR. How long it stays open was not measured.
- **C2, bears on N2.** `http-server.ts` imports `@secuura/shared`, and neither `package-generator.ts` nor `mcp-server/package.json` supplies it (`shared`: zero hits; control: 48 hits for `secuura`). A package generated from a current tree may not start at all, which changes what N2 means. READ ONLY, not run. Round 1's C2 is related.
- **C3.** Round 1's 30-byte body that allocates 100 MB still answers 200, 1989 ms, unchanged.

## NOT tested

- Any box, deployed server, client or Kintsugi; the real gateway's answer to `sha256:` or a hashless item.
- Schemathesis, Akto, Playwright, k6. NOT COMMISSIONED: no stack allowed.
- The compiled `dist` on Node 24 with zod 4. All runs were on Node v26.8.1, tsx.
- Linux: the recipes and the 96 KB figure. GNU `sha256sum`'s leading backslash on an escaped filename could not be seen on macOS's.
- The shared package's own suite, including its parser-order test. tsc and eslint not re-run.
- PR body and comments live; I read the seat's record.
- Slow-drip uploads and concurrency: only one case at a time.
- I did not re-open the outside-file census or Platform S. Round 1's result stands by the 14-path delta.

## SFDIPOT

Touched: Structure (mount order, imports), Function (every reachable error path, log), Data (boundaries, encodings, hostile values), Interfaces (wire, spec, guides, gateway by read), Operations (hostile and careless use, recipes as written). Thin: Platform (macOS only). Untouched: Time.

## My conduct

- Findings only. Nothing posted, no box, no docker, no `gh`, no `rm`. Load stayed under 8 (highest reading 5.95).
- **Writes:** this file, `evidence/` here (320 KB), `/private/tmp/g250`. **The clone is left in place per your no-rm correction: 20 MB.** It has three untracked `g250-*` scratch servers and is otherwise clean at the head. tsx keeps its compile cache at `/private/tmp/tsx-501` and under `$TMPDIR`, outside my clone. Those directories were written to by my runs and were not removed; I cannot separate my entries from other gates'.
- **Hook refusal, reported.** My first setup command tried to symlink the local `node_modules` into my clone. `pathguard.py` refused it as a write to the Blockchain tree. I did not re-issue it or use the override. I resolved dependencies read-only through tsconfig paths and a vitest alias instead. Round 1 had such a symlink; I did not.
- **Hook advisories:** the case-sensitive-grep advisory fired on my greps; every zero in this report comes from `grep -i` with a control beside it. The pipeline-rc advisory fired on my first merge-tree; I re-ran it alone for the rc above.
- **Loopback:** the servers under test and a stub ran on 127.0.0.1, ports 47950-47983. I read "network only for git fetch" as off-host traffic, as round 1 did. If you meant loopback too, the runtime evidence rests on going outside it. No listener remained at the end.
- **Substrate, named per the template. Not what the product deploys.**
  - Real: head `http-server.ts`, and `boundedJson`, `rejectControlBytes` and `enforceProductionConfig` from head sources, loaded file by file through `evidence/shim.mts`.
  - Not real: express 4.22.2 where the lockfile pins 4.22.3; body-parser 1.20.6 from the local checkout's `node_modules` (that checkout sits at 1b1b65c74, behind develop); zod 3.25 where the product has zod 4, so `z.config` is neutered in the preload. No route under test uses zod.
  - Suite runs alias `@secuura/shared` to a small stub (`shim-unit.mjs` in the clone), vitest 4.1.10 against the seat's 4.1.12.
- **Own instrument notes.** My first mutation run aborted on an asserted anchor: a pattern also matched a comment. Nothing was written; I fixed the anchors, including one that would have mutated the comment and landed nothing. The parent could not be the positive control, as section 3 says, and I noticed only after its zeros came back.

Evidence: `evidence/` in this folder (attack, synthetic and regression probes at each source, server logs, `mut.txt`, `overlap.txt`, `red.json`).
