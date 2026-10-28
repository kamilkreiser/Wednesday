# QA gate 7 (TIER 1): Secuura #1788 (KS-1240 part 2, social auth) delta round 2 of 2, and #1791 (KS-1670 site 1, m365 success redirect) round 1

- **Gate model:** Claude Opus 5.5 (claude-opus-5-5), G1 tier-1 gate (auth surfaces), subagent of Wednesday. Spark review model: deepseek-v4-flash-0731 via the tunnel. Routing receipt as commissioned: claude-opus-5-5, G1 tier-1 gate (auth surfaces), gauge 81%.
- **Pushed / merged / commented / edited / mailed / Linear-written:** nothing. Linear was read only: KS-1670 with comments first:100, through my own reader `gatework7/linear_read.py`, key never printed. KS-1240 was read by spark_review's own reader. **`gh` is not authenticated in this shell ("You are not logged into any GitHub hosts"), so the PR bodies were NOT read.** Each head's commit message stood in for its PR body and went to Spark as the PR description, flagged as such.
- **Clone:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate7-tier1/repo`.
  - The path did not exist (`ls`: No such file); it was made with `git clone --shared .../spark/cache/src`.
  - `git -C <path> rev-parse --show-toplevel` was asserted equal to the path before the first fetch, and inside every driver that fetches (`gatework7/env.sh`). Re-read at the end: same.
  - Origin = GitHub `Secuura/Distributed_Secuura`. The deploy key went through GIT_SSH_COMMAND (`3_Access_Keys/github_deploy_rw`, `-o ServerAliveInterval=30 -o IdentitiesOnly=yes`), the mechanism gates 4 and 5 recorded.
- **Worktrees** (none removed, no-delete rule), all under `/private/tmp/claude-501/gatework7/`:
  - `w1788` = 7eeedb82
  - `w1788r1` = aa4829d4 (the round-1 head)
  - `w1791` = b9d91e11
  - `wbase1791` = bd6697e0 (#1791's merge-base)
  - Probe files and test copies were moved to `gatework7/quarantine/`. Every mutated product file was restored from `git show HEAD:`. Final `git status` in all four shows only the two node_modules symlinks.
- **node_modules:** read-only symlinks made with `os.symlink`.
  - auth: `Blockchain/Dev/node_modules` and `services/auth/node_modules` both point at `.../Blockchain/Dev/node_modules` (as gate 5 did).
  - m365: `services/m365-integration/node_modules` points at that service's own shared-tree `node_modules`, and `Blockchain/Dev/node_modules` points at the Dev root.
  - Nothing was installed and nothing was written into the shared tree. Node v26.8.1 (not the repo's LTS 24).
- **Docker / Postgres / ports:** none needed and none started (`docker ps -a`: 0 names match gate7). The only ports bound were the 127.0.0.1 ephemeral listeners inside vitest runs.
- **Load:** `uptime` / `vm.loadavg` was checked before every heavy run (`out/load.txt`). load1 ran 5.2 to 12.8. **Two waits at load1 >= 12, one 60 s step each** (before sg1791 and before the wbase1791 suite). No run went ahead above 12. The w1791 suite started at 11.8.
- **Spark queue:** before each review I checked that no other `spark_review.py` was running (`pgrep`), and found none. My two reviews ran one after the other. The gate-6 agent did not hold the box while I used it.

## Pins (git ls-remote)

| ref | start (22:55:21) | end (23:09:06) |
|---|---|---|
| develop | **b67a1c8d3a52038cb5f4e6135dfb59f0249eac6e** (moved since gate 5's d531abd5: #1780 KS-1702 merged) | same |
| refs/pull/1788/head | **7eeedb825c5c2922ab48e6a0a2fe95bb10b24b78** (= brief) | same |
| refs/pull/1791/head | **b9d91e1199950aa933322de45743689e738d439a** (= brief prefix b9d91e119995, asserted in full) | same |

- #1788's merge-base with develop is still 2b7ef12fa564. #1791's is bd6697e079fc.
- **Code files shared with develop's commits since then: 0 for each PR.** #1788 and #1791 share no code file with each other.
- `git merge-tree --write-tree --name-only`, for develop + #1788, develop + #1791 and #1788 + #1791: each rc 1, conflicting on exactly the two Projects Documents html files (`out/mergetree.txt`).

## BLUF

| PR | Ticket | Verdict | One line |
|---|---|---|---|
| #1788 (round 2 of 2) | KS-1240 p2 | **GO WITH NOTES** | **Round 2 closes all three items the coordinator ruled.** (1) The leak: no token-endpoint error body reaches the client from any of the six adapters, and the body is logged server-side, bounded. (2) The profile pins: every round-1 surviving profile mutant is now killed, in all five families. (3) Refused and unresolvable providers are now classified: `/social/link` answers 503. **Delta is exactly what the author said:** one fast-forward commit, 10 files, and outside the PR's own test file only ks1617 changed (one cell: its expectation and title); `routes/` and `middleware/` are byte-unchanged. **Author's figures reproduced:** at the round-1 head the head's cells are 22 failed / 41 passed of 63, at the new head 63 / 0; auth suite 1244 -> 1258 with 0 new failures; tsc build rc 0. **My 20 mutants:** 16 killed, 4 survive (two classifier-width gaps, an unpinned log bound, and the dead AbortError branch). **One residual of the 1788-1 class, measured:** a provider that answers **200 with a non-JSON body** still puts the first 10 characters of that body in the callback's 400 (V8's `SyntaxError` text, `"<html>PROV"...`). That comes through `routes/auth.ts:1078`, which echoes any exchange error's message. Low; ticket it (see 1788-10). **This round is not a NO GO, so the two-NO-GO cap is not engaged.** |
| #1791 | KS-1670 site 1 | **GO WITH NOTES** | **The real route, driven over HTTP:** a hostile connection id (`&`, `#`, CR/LF, a full URL, a protocol-relative URL, `%2F`, encoded `&`/`=`, `?`+space, non-ASCII) changes **neither the redirect's target nor its query shape** at head (11 of 11 rows OK). The id round-trips exactly. **At base, 5 of the 11 rows break the query:** `&` adds or duplicates params, `#` moves `tenant` into the fragment, and `%2F` / `%26` decode to different ids. The target origin and path never moved, even at base, which agrees with the ticket's "not exploitable today". PR test 5/0 at head and 3 pass / 2 fail at base (reproduced). m365 suite 266 -> 271, 0 failed both sides. **Covers site 1 only, as the title and the ticket say:** the ticket itself says site 1 "can ship on its own" while sites 2 and 3 wait on the KS-1641 `:515` decision. **Sites 2 and 3 are untouched at head** (`index.ts:869` 500 `details: err?.message`; `:1168` Graph error text). This is narrowing, not a defect. Notes: the PR's test is a source-text pin (it misses a raw id added by concatenation, my N6); a lone-surrogate id now throws `URIError` after the connection was saved as connected (unreachable today); docs carry 84. |

**Merge order:** independent. The two PRs share no code file, and the docs conflict in any order. **Docs sections:** #1788 = **95** (head still carries 85 / 85.1-85.4, unchanged from round 1). #1791 carries **84** / 84.1-84.3, which collides with develop's 84. It needs the next free number after 95 and after whatever gate 6 assigns to #1787 and #1789. I did not assign it; Wednesday holds the chain.

---

## Spark shadow (run FIRST; `out/p1788/`, `out/p1788b/`, `out/p1791/`)

Method:
- `spark_gate.sh` per PR, with work dirs under the scratchpad `.../scratchpad/gate7/sg*` and `--node-modules` set to the Dev root.
- Then `spark_review.py`, with `facts_spark.json` = facts minus the two Projects Documents html files, plus HARNESS LIMIT lines: the PR body is the commit message; for #1788 the round-2 and base-arm semantics; for #1791 that the test is a text pin.
- Tunnel: `tunnel.sh check` answered UP (`127.0.0.1:47788/v1/models` 200, ssh pid 52462).

| run | spark_gate head / base product code | note |
|---|---|---|
| #1788 vs base = aa4829 (the round-1 head) | 63 / 0 ; **63 / 0** | **VACUOUS, not counted.** With a sha as `<base-ref>`, the harness wrote `merge_base: ""` and `product_files: []`, so its base arm ran head product code. This is a harness limit for delta gates. I ran the delta base arm myself (below). |
| #1788 vs develop (merge-base 2b7ef12) | **63 pass / 0 fail ; 18 pass / 45 fail**, 114 s | Non-vacuous. Base red includes round 1's own cells. |
| #1791 vs develop (merge-base bd6697e) | **5 / 0 ; 3 pass / 2 fail**, 13 s | Matches R's claim exactly. |

| PR | Spark review |
|---|---|
| #1788 | attempt 1 **invalid** (repetition abort + unparseable JSON). Attempt 2 valid: **NO GO, 3 Major, 3 Minor, 2 Note**. 147.1 s, 82,542 prompt tokens over both attempts |
| #1791 | **GO WITH NOTES, 5 Notes**, 53.1 s, 32,463 prompt tokens, one attempt |

### Spark Majors checked at source (#1788)

- **Major 1** ("classification depends on the exact text 'fetch failed', which may differ across Node versions"):
  - It is true that the classifier keys on `name === 'TypeError' && message === 'fetch failed'` (`apple.ts:20` and the same line in the other five).
  - As a defect, it is **not standing.** That string is undici's fetch rejection text for every network failure: refused, DNS, and connect timeout. Should it ever differ, the failure falls back to round 1's behaviour (unclassified: 500 on link, 400 on callback). **That is never a login.**
  - Not checked on Node 24 (NOT TESTED). Kept as a fragility note inside 1788-11.
- **Major 2** ("clients may rely on the old message"): **FALSE as a defect.** The provider body in a client-facing message is exactly what gate 5 ruled must go (1788-1). No client contract carries it.
- **Major 3** ("AbortError from a client cancel misclassified as a timeout"): **FALSE.** No adapter takes any signal except its own `AbortSignal.timeout`; there is no client-abort path into these fetches. The branch is dead code: G3 survives in both rounds (1788-5).
- **Minors:**
  - "`asked` does not pin the production constant": **FALSE.** `asked` records the `ms` the production code passes to the spied `AbortSignal.timeout`, so it does pin `PROVIDER_TIMEOUT_MS`.
  - "DNS failures not covered": true that no cell runs DNS. The same undici text applies. NOT TESTED.
  - "fetch init not asserted": scope.

**No Spark Major stands.** Spark missed:
- the SyntaxError residual (1788-10),
- the classifier-width survivors H9 and H12 (1788-11),
- the unpinned log bound (H5).

### Spark Notes judged (#1791)

- **Note 1** (text pin, not the wire): TRUE. My attack probe fills that gap (below).
- **Note 2** (the R1 regex `^encodeURIComponent\(.*\)$` also accepts `encodeURIComponent(a) + b`): **TRUE.** My N4 (`encodeURIComponent(id).replace(/%26/g,'&')`) passes R1. Only R2's exact-text check catches it, and that check covers the success line only.
- **Note 3** (C1 = exactly one interpolation is brittle): true, and deliberate.
- **Note 4** (golden not verifiable): true, immaterial.
- **Note 5** ("byte-for-byte for every server id" is unproven): **answered:**
  - Server ids are `conn_${randomUUID()}` (`index.ts:723`), i.e. `[0-9a-f-]` plus `conn_`, which `encodeURIComponent` leaves unchanged.
  - My A0 row measured the Location byte-identical at base and head.

---

## ITEM A: #1788 delta (aa4829d4eaa0..7eeedb825c5c), round 2 of 2

### Delta scope (`git diff --stat aa4829d4eaa0 7eeedb825c5c`: 10 files, +219 / -84)

- **Fast-forward:** `merge-base --is-ancestor aa4829 7eeedb` holds, and the range is one commit (7eeedb82, "gate 5 fix round 1").
- **Files:**
  - the PR's own `ks1240b...test.ts` (+83 / -…);
  - `ks1617-social-profile-fetch-failure-names-the-http-status.test.ts` (**4 lines: one cell's title and one expectation, P5 only**: the only widened file, with the coordinator's ANSWER 10:51Z per the commit message);
  - the six adapters (`apple`, `facebook`, `github`, `google`, `linkedin`, `microsoft-personal`, about 33 lines each);
  - the PR's own block in each of the two Projects Documents html files (figures and wording).
- **`routes/` and `middleware/` are byte-unchanged** (`git diff --quiet ... -- routes middleware`: rc 0). Nothing else changed.

### What the delta does (read)

- Each adapter's `timedOut()` becomes `unavailable()`, which returns:
  - `'timeout'` for `TimeoutError` / `AbortError`;
  - `'unreachable'` for `TypeError` + `'fetch failed'`;
  - null otherwise.
- `exchangeCode` maps `'unreachable'` to `ServiceUnavailableError('<P> could not be reached; please try again.')`.
- Each token-endpoint `!ok` branch now calls `logger.warn('<P> token endpoint refused the code exchange', { provider, status, body: text.slice(0, 200) })` and throws `Error('<P> token exchange failed (HTTP <status>)')`.
- Profile checks and response parsing are unchanged.

### Suites and the delta base arm (`out/deltabase_*.json`, `out/suite/`, `out/tsc_*.txt`)

- **Head's two files on round-1 product code** (copied into `w1788r1` as `gate7-headcopy-*`): **63 cells, 41 pass / 22 fail.** Equal to the author's doc figure, "22 failed / 41 passed of 63". The 22 red are:
  - 6 x "refuses the token exchange (HTTP 400)";
  - 6 x "token endpoint answers 502";
  - 6 x "refuses the CONNECTION";
  - 3 route cells (neutral callback text, link 503, callback unreachable text);
  - ks1617 P5.
  The same files at head: **63 / 0**.
- **services/auth full suite:**
  - aa4829: 106 files / **1244** tests, 1 failed.
  - 7eeedb: 106 files / **1258** tests, 2 failed.
  - The common failure is `ks1000 ... REAL: services/auth against the committed baseline passes`, environmental, as in round 1.
  - The extra failure at head is `ks949 ... the enumeration actually finds seed sites`. It timed out at **5006 ms** in the full run at load ~9 and **passes 31/31 alone**: the known 5 s-default timing cell (round 1 and the author's doc both note it). **0 new failures from the delta.**
- **`tsc -p tsconfig.json --noEmit`** (build config): rc 0 at aa4829 and at 7eeedb, so the new `logger` imports resolve.
- Not re-run: ESLint, `audit:gate`, `audit:locks`, the test-type ratchet, the hook.

### Mutants on the changed lines (own worktree `w1788`, both PR files, 63 cells; `out/mut1788/`, summary `out/mut1788.txt`)

| mutant | result | red |
|---|---|---|
| M0 head | 63 / 0 | none |
| H1 Google token Error echoes the provider body again | 60 / 3 | Google 400, Google 502, ks1617 P5 |
| H2 GitHub token Error appends the marker after logging | 60 / 3 | GitHub 400, GitHub 502, callback neutral-text route cell |
| H3 LinkedIn drops the server log line | 62 / 1 | LinkedIn 400 (logged-marker assertion) |
| H4 Apple logs the body sliced to 0 chars | 62 / 1 | Apple 400 |
| **H5 Microsoft logs the body unbounded (no slice)** | **63 / 0, SURVIVES** | none (log bound unpinned) |
| H6 Facebook hard-codes "(HTTP 400)" | 62 / 1 | Facebook 502 |
| H7 Apple: unreachable not classified | 62 / 1 | Apple refused-connection |
| H8 GitHub: unreachable answered with the timeout text | 60 / 3 | GitHub refused-connection, link 503, callback unreachable |
| **H9 GitHub: every TypeError counts as unreachable** | **63 / 0, SURVIVES** | none (the non-network control exists for Apple only) |
| H10 Apple: every TypeError counts as unreachable | 62 / 1 | Apple non-network TypeError control |
| H11 Microsoft: unreachable thrown as a plain Error | 62 / 1 | Microsoft refused-connection |
| **H12 Google: unreachable by message only (any `'fetch failed'`)** | **63 / 0, SURVIVES** | none |
| G1 Google profile `!ok` deleted (round-1 survivor) | 61 / 2 | Google profile-401 pin, ks1617 P1 |
| G14 GitHub profile `!ok` deleted (round-1 survivor) | 62 / 1 | GitHub profile-401 pin |
| G6 Google profile non-OK as 503 (round-1 survivor) | 61 / 2 | Google profile-401 pin, ks1617 P1 |
| G8 Google token 5xx as 503 (round-1 survivor) | 62 / 1 | Google 502 cell |
| H13 LinkedIn profile `!ok` disabled | 62 / 1 | LinkedIn profile-401 pin |
| H14 Facebook profile `!ok` disabled | 62 / 1 | Facebook profile-401 pin |
| H15 Microsoft profile `!ok` disabled | 61 / 2 | Microsoft profile-401 pin, ks1617 P2 |
| **G3 GitHub drops the `AbortError` branch** | **63 / 0, SURVIVES** | none (dead branch, as round 1) |

**Round 1's four survivors G1, G14, G6 and G8 are all killed now**, plus the three families round 1 did not mutate (H13 to H15). The four survivors at head are listed above; H5, H9 and H12 lie on the delta's own lines.

### Probe (own cells on the PR's harness, head; `out/probe1788_head.json`, file in `gatework7/quarantine/gate7-probe-1788.test.ts`)

| row | client sees | provider text? |
|---|---|---|
| P1 callback, GitHub token answers **200 text/html** `<html>PROVIDER_TEXT_MARKER…` | **400 `OAuth authentication failed: Unexpected token '<', "<html>PROV"... is not valid JSON`** | **first 10 chars, yes** |
| P2 callback, Google userinfo **200 text/html** | 400, same shape, `"<html>PROV"...` | **first 10 chars, yes** |
| P3 callback, Apple token 200 with a non-JSON `id_token` payload | 400 `... Unterminated string in JSON at position 36 ...` | no (position only) |
| P4 callback, GitHub token **200 `{error, error_description}`** | **200 (sign-in completed)**, but only because the stub's `/user` ignores the Bearer; see 1788-13 | no |
| P5 callback, Google token 502 html | 400 `... Google token exchange failed (HTTP 502)` | no |
| P6 callback, Facebook profile 401 | 400 `... Failed to fetch Facebook user profile` | no |
| P7 callback, Microsoft token refused connection | 400 `... Microsoft could not be reached; please try again.` | no |
| L1 link, Google token 400 json | 500 INTERNAL_ERROR generic | no |
| L2 link, Google token refused connection | **503 SERVICE_UNAVAILABLE** `Google could not be reached; please try again.` | no |
| L3 link, GitHub token 200 text/html | 500 generic | no |

### Round-1 findings, item by item

| # | Round-1 finding | Round 2 | Instrument |
|---|---|---|---|
| 1788-1 | Callback echoes the provider's raw token-error body; the PR's control pinned the echo | **CLOSED for every instance round 1 measured** (token-endpoint 4xx JSON and 5xx HTML, all six adapters). The Error carries only `(HTTP <status>)`; the body is logged server-side at 200 chars; the old pinning control now asserts **absence** (`r.raw` does not contain the marker). **Residual of the same class, not in round 1's text: see 1788-10.** | Delta base arm (18 of the 22 red cells are this fix); mutants H1, H2, H3, H4, H6 killed; probe P5. |
| 1788-2 | Profile/userinfo non-OK unpinned (G1, G14, G6 survived) | **CLOSED.** One profile-401 pin per family (5), plus ks1617 P1/P2. G1, G14, G6, G8 and H13-H15 all killed. | Mutants. |
| 1788-3 | GitHub's three sequential 10 s calls = production nginx `proxy_read_timeout 30s` | **OPEN, unchanged** (not in the ruled scope; no bound or deadline changed). Carry as ticket or note. | Read: the delta touches no `PROVIDER_TIMEOUT_MS` or call order. |
| 1788-4 | Only a timeout classified; a refused/DNS-failed provider answered 500 on link | **CLOSED for refused / unresolvable:** link 503 `could not be reached`, callback 400 with the classified text. Token 5xx stays a neutral, unclassified error by design (now pinned: G8 killed). Callback-timeout = 400 is unchanged and disclosed. **Residual test gap: 1788-11.** | PR route cells (red at aa4829); probe L2, P7; mutants H7, H8, H10, H11 killed. |
| 1788-5 | `AbortError` branch dead | **OPEN (Info), unchanged.** G3 survives. | Mutant G3. |
| 1788-6 | `routes/internal.ts:43` unbounded security call | **OPEN, out of delta** (routes/ byte-unchanged). Same KS-1240 hang; neither part covers it. | `git diff --quiet`. |
| 1788-7 | Apple `id_token` decoded, not verified | **OPEN, carried, out of scope.** | Read. |
| 1788-8 | undici's own connect timeout races our signal; if undici won, the answer was 500 | **CLOSED by consequence (reasoning).** Undici's connect timeout rejects as `TypeError: fetch failed` (cause `ConnectTimeoutError`), now classified as unreachable (503), so either winner yields a 503. | Reasoning only; no blackhole run. |
| 1788-9 | Docs carry 85; use 95 | **OPEN (merge-time).** Head still `<h2>85.` / 85.1-85.4. | Read. |

### New findings at the round-2 head

| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1788-10 | **Low (same class as 1788-1; carried lines, newly exposed)** | A provider answering **200 with a body that is not JSON** still leaks text to the client: `tokenRes.json()` / `profileRes.json()` throw V8's `SyntaxError`, whose message quotes **the first 10 characters of the body** (`"<html>PROV"...`), and `routes/auth.ts:1078` wraps every exchange error's message into the 400. The delta did not touch the `.json()` lines or the route. Fragment-sized, needs a misbehaving 200, and no deployment configures a provider today. **Root fix (ticket):** have the callback map any non-`AppError` to a neutral text and log the detail, instead of one adapter line at a time. `/social/link` does not leak (generic 500, L3). | FOUND by probe P1/P2 (measured); P3 shows a parse position only. |
| 1788-11 | Low (test gap on the delta's own lines) | The width of the new classifier is pinned only for Apple. H9 (GitHub: every `TypeError` is unreachable) and H12 (Google: any `'fetch failed'` message, whatever the name) survive. Example: a GitHub `/user/emails` answer that is not an array throws `TypeError: emails.find is not a function`; under H9 that would read "GitHub could not be reached" (503) and go unseen. The classifier also depends on undici's exact `'fetch failed'` text (Spark Major 1, fragility only). One non-network-TypeError control per family closes it. | TESTED (mutants). |
| 1788-12 | Info | The log bound is unpinned: H5 (no `.slice(0, 200)`) survives. The body is provider error text, not a credential. | TESTED H5. |
| 1788-13 | Info (carried, out of delta) | GitHub answers a bad code with **HTTP 200** `{error, error_description}`. The adapter does not check that `access_token` exists; it calls `/user` with `Bearer undefined` and relies on GitHub answering 401. Under the PR's stub, which ignores the Bearer, the sign-in completed (P4). Against real GitHub the profile call fails ("Failed to fetch GitHub user profile"). Defence in depth: refuse a token answer that has no `access_token`. | Probe P4 + read `github.ts:86`. |

**Verdict for #1788: GO WITH NOTES.** This is the second and last round under the cap, and it is **not** a NO GO. The ruled instances ship. Ticket the residue: 1788-10 (callback echoes any exchange error's message), 1788-11 (classifier-width controls), 1788-3 (30 s = nginx 30 s), 1788-6 (internal.ts), 1788-7 (Apple id_token), 1788-13 (GitHub 200-error).

---

## ITEM B: #1791 (KS-1670 site 1), round 1

Head b9d91e119995 (full sha asserted by ls-remote, start and end). Files:
- `services/m365-integration/src/index.ts`: **one line**, `connectionId=${connectionId}` becomes `connectionId=${encodeURIComponent(connectionId)}`, at `:677`;
- the new test (55 lines, 5 cells, a source-text pin);
- one block in each of the two Projects Documents html files.

### Tests

- spark_gate: 5 / 0 at head, **3 pass / 2 fail** at base (R1 and R2 red).
- Full m365 suite: wbase1791 **27 files / 266 / 0 failed**; w1791 **28 / 271 / 0 failed**. 0 vanished.
- `tsc -p tsconfig.json --noEmit`: rc 0 both sides. All as R claimed.

### Attack rows (the real route over 127.0.0.1; `out/probe1791_{wbase1791,w1791}.json`)

**Method.** I built the probe from ks1677's production-path harness (`gatework7/mkprobe1791.py`):
- real `POST /api/connections/init`, real opaque state and binding cookie, real `GET /api/callback`;
- mocked: `exchangeAuthCode`, Graph `/organization` ("Graph Org"), the DB as seeded rows.

The connection id is server-issued (`conn_${randomUUID()}`, `index.ts:723`). The only way to inject one is to make `crypto.randomUUID` return the payload for that one init (`vi.spyOn(...).mockImplementationOnce`). So each row's id is `conn_<payload>`.

For each row I checked six things:
1. the target (origin `http://frontend.test` + path `/admin/integrations`) is unchanged;
2. the query keys are exactly `[m365, connectionId, tenant]` and there is no fragment;
3. `m365=success`;
4. the decoded `connectionId` equals the issued id;
5. `tenant` is intact;
6. there is no CR/LF in Location.

| row | payload | base (bd6697) | head (b9d91e) |
|---|---|---|---|
| A0 control | real uuid | OK | OK, **Location byte-identical to base** |
| A1 `&` adds a param | `x&tenant=evil` | **FAIL**: keys `m365, connectionId, tenant, tenant`; id read as `conn_x` | OK: `conn_x%26tenant%3Devil` |
| A2 `&` overrides m365 | `x&m365=error&message=pwned` | **FAIL**: keys `m365, connectionId, m365, message, tenant` | OK |
| A3 `#` fragment | `x#frag` | **FAIL**: hash `#frag&tenant=Graph%20Org`, so `tenant` is lost | OK: `%23` |
| A4 CR/LF | `x\r\nSet-Cookie: pwn=1` | OK (express's encodeurl writes `%0D%0A`; no header injection even at base) | OK (`%0D%0A`, `%3A`, `%3D`) |
| A5 full URL | `https://evil.example/steal?a=b` | OK (it stays inside the query; the target is fixed by the prefix) | OK: fully encoded |
| A6 protocol-relative | `//evil.example` | OK (same reason) | OK |
| A7 encoded slash | `x%2Fy` | **FAIL**: the id decodes to `conn_x/y` | OK: `%252F`, round-trips `conn_x%2Fy` |
| A8 encoded `&` / `=` | `x%26tenant%3Devil` | **FAIL**: the id decodes to `conn_x&tenant=evil` | OK: `%2526...` |
| A9 `?` + space | `x?y=1 z` | OK | OK |
| A10 non-ASCII | `é✓日本` | OK | OK (UTF-8 percent-encoded, round-trips) |
| A11 lone surrogate | `x\uD800y` | id mangled to U+FFFD, still `success` | **`encodeURIComponent` throws `URIError`**, caught: the redirect becomes `m365=error&message=URI%20malformed` and the connection (already saved `connected`) is re-saved `status: 'error'`. See 1791-3. |

**Answer to the brief:**
- At head, no injected `connectionId` changes the redirect's target or its query (A1 to A10).
- **At base the target never changed either** (the origin and path are a fixed prefix), but the query did (A1, A2, A3, A7, A8).
- So the PR closes exactly the "shape of the query" fragility the ticket names.

### Mutants (own worktree `w1791`; PR test + my attack probe as a behavioural cell; `out/mut1791.txt`)

| mutant | PR test (5) | attack rows not OK |
|---|---|---|
| N0 head | 5 / 0 | A11 only |
| N1 the base line (unencoded) | 3 / 2 (R1, R2) | A1 A2 A3 A7 A8 A11 |
| N2 `encodeURI` instead of `encodeURIComponent` | 3 / 2 (R1, R2) | A1 A2 A3 A11 |
| N3 `encodeURIComponent(String(connectionId))` (equivalent) | **4 / 1 (R2 false red)** | A11 only |
| N4 `encodeURIComponent(id).replace(/%26/g,'&')` | 4 / 1 (R2 only; **R1 passes**) | A1 A2 A11 |
| N5 tenant left unencoded | 4 / 1 (R2) | A11 (Graph Org's space is encoded by express) |
| **N6 raw id added to the error redirect by concatenation (`` ` + connectionId ``)** | **5 / 0, SURVIVES** | (the probe does not drive the error path) |

### The other redirect sites (head, `git grep redirect\(` in `m365-integration/src/index.ts`) and the ticket

| line | redirect | KS-1670? |
|---|---|---|
| `:491` | `/health` (constant) | no |
| `:626` | OAuth `error_description || error`, via `encodeReflectedText(capCodePoints(...))` | no: KS-1641's cap (#1622) |
| `:630` | constant `missing_code_or_state` | no |
| `:644` | constant `invalid_state` | no |
| **`:677`** | **success: `connectionId` + `tenant`** | **site 1: this PR** |
| `:684` | `message=${encodeURIComponent(err?.message ...)}`: MSAL's error text, encoded, uncapped | the ticket's "`:515`" (develop numbering), owned by **KS-1641** as "a decision, not a cap" |

KS-1670's other two sites are not redirects: site 2 is `:869` (500 `details: err?.message`) and site 3 is `:1168` (Graph's `error.message` passed back uncapped). Both are untouched at head (`git grep`). **The ticket says: "Site 1 is a one-line change and can ship on its own. Sites 2 and 3 should wait for the `:515` decision on KS-1641."** So #1791 covers only site 1, exactly as its title and the ticket say. That is sanctioned narrowing, not a defect. KS-1670 stays open for sites 2 and 3. The ticket text predates KS-1677: it says `connectionId` is `String(state)`. At head it is `connection.id` from the state-bound lookup, which is server-issued and even less reachable.

### Findings

| # | Sev | Finding | FOUND / TESTED / HOW |
|---|---|---|---|
| 1791-1 | Low (test gap, disclosed) | The PR's cells are a source-text pin. R1's needle sees only template interpolations `connectionId=${`, so a raw id added by concatenation survives (N6). Its regex also accepts a wrapped-then-unwrapped expression (N4 passes R1; only R2's exact text catches it, and only on the success line). An equivalent rewrite false-reds R2 (N3). My HTTP probe shows the behaviour the pin cannot. Optional: lift A1/A3/A7 into the PR as wire cells. | TESTED (mutants N3, N4, N6; Spark Note 2 agrees). |
| 1791-2 | Low (ticket acceptance) | The ticket asks that "each fix needs a cell that sends **non-ASCII text across the boundary**". The PR has none (text pin). My A10 shows non-ASCII ids round-trip on the wire at head. | Read the ticket; TESTED A10. |
| 1791-3 | Info (unreachable) | `encodeURIComponent` throws `URIError` on a lone surrogate. The throw happens after `dbSaveConnection(connection)` stored `connected` with tokens. The catch then flips it to `error` and redirects `m365=error&message=URI%20malformed`. Base did not throw (U+FFFD). Unreachable: ids are `conn_` + uuid (ASCII). The `tenant` encoding on the same line had the same property before this PR (a Graph `displayName` with a lone surrogate would throw too; not tested). | TESTED A11 (base vs head); tenant case read only. |
| 1791-4 | Low (merge-time) | Docs carry `84` / 84.1-84.3 (collides with develop's 84). Renumber to the next free number after 95 and after gate 6's assignments. | grep. |

**Verdict for #1791: GO WITH NOTES.**

---

## Spark calibration rows

| PR | Spark verdict | This check | Defects Spark found that stand | Real findings Spark missed | Verdict of the verdict |
|---|---|---|---|---|---|
| #1788 r2 | NO GO (3 Major, 3 Minor, 2 Note); attempt 1 invalid (repetition abort) | GO WITH NOTES | 0 (Major 1 is a true fragility, not a defect; Majors 2 and 3 false; Minor `asked` false) | 1788-10 (200 non-JSON body fragment reaches the client), 1788-11 (H9/H12 survivors), H5, 1788-13 | **False NO GO**, 82.5k prompt tokens over two attempts. It fixated on one sentence of the PR body (the repetition guard fired on it twice). Non-vacuous row: 45 red at merge-base. Its delta-mode base arm was vacuous (harness limit, below). |
| #1791 | GO WITH NOTES (5 Notes) | GO WITH NOTES | 0 defects; Note 2 (permissive R1 regex) is true and confirmed by N4 | the base-vs-head wire behaviour (it had no runtime evidence beyond the pin), N6, A11 | **Right verdict, one sharp Note.** 32.5k tokens, one attempt. Non-vacuous: 2 red at base. |

**Harness note for Wednesday:** `spark_gate.sh` given a sha as `<base-ref>` (the round-1 head, for a delta gate) wrote `merge_base: ""` / `product_files: []`, so its base arm silently ran HEAD product code (63/0 both sides, `out/p1788/`). Delta gates need either a fix there or `<base-ref>` = develop plus a manual delta arm, which is what I did.

## Method

- Copied from gates 4 and 5:
  - clone-at-fresh-path with the toplevel assertion;
  - read-only node_modules symlinks;
  - Spark half first (spark_gate, then spark_review on facts minus the docs html, with HARNESS LIMIT lines);
  - own worktrees, mutants rewritten from `git show HEAD:` and restored, `git status` read back clean;
  - full suites both sides, compared by failing (file, title);
  - merge-tree; pins at start and end.
- Delta-specific additions:
  - the head's test files run on the round-1 product code (my own base arm);
  - every round-1 finding re-classified;
  - `git diff --quiet` over `routes/` and `middleware/` to prove nothing outside the delta moved.
- #1791-specific: an HTTP attack matrix on the production route, base vs head, with the probe reused as a behavioural cell under mutants.
- **Drivers** (all under `/private/tmp/claude-501/gatework7/`): `env.sh`, `run_sg.sh`, `run_sg2_rev.sh`, `run_mine.sh`, `mut1788.py`, `mut1791.py`, `mkprobe1788.py`, `mkprobe1791.py`, `linear_read.py`, `prep_facts.py` (copied from gate 5).

## NOT TESTED

- PR bodies (`gh` unauthenticated); Node 24 LTS; any real provider, Microsoft, nginx, gateway, stack, Docker, CI; the four platform suites.
- #1788:
  - a DNS failure and a blackholed connect (undici's connect-timeout race, 1788-8, reasoning only);
  - the 30 s GitHub case through a real nginx (1788-3, read only);
  - Apple and Facebook beyond the PR's cells and my P3/P6;
  - ESLint, the test-type ratchet, `audit:gate`, `audit:locks`, the hook;
  - the `ks1000` environmental failure (present on both sides, not diagnosed).
- #1791:
  - the error-path redirect (`:684`) under hostile input (owned by KS-1641);
  - a lone-surrogate `tenantName` (1791-3, read only);
  - a real database (ks1677's seeded-row harness only);
  - sites 2 and 3 (out of scope per the ticket).

## Evidence locations

- **Run outputs:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate7-tier1/out/`
  - `p1788/` (vacuous delta-base run), `p1788b/` and `p1791/` (facts, `facts_spark.json`, diff, `spark/review.json` and raw attempts)
  - `sg*.log`, `deltabase_r1.json`, `deltabase_head.json`
  - `mut1788/` + `mut1788.txt`, `mut1791/` + `mut1791.txt`
  - `probe1788_head.json`, `probe1791_w1791.json`, `probe1791_wbase1791.json`
  - `suite/` (four json), `tsc_*.txt`, `mergetree.txt`
  - `ticket_KS-1670.txt`, `msg1788.txt`, `msg1791.txt`, `delta1788.patch`, `diff1791.patch`
  - `pins_start.txt`, `pins_end.txt`, `load.txt`
- **Scratch:** `/private/tmp/claude-501/gatework7/` (drivers, worktrees, `quarantine/` with every probe and test copy) and `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fccaae68-37b3-43d1-9466-4e52087c3d4f/scratchpad/gate7/` (spark_gate work dirs `sg1788`, `sg1788b`, `sg1791`).
