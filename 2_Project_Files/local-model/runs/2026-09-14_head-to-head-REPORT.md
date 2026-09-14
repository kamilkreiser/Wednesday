# Head-to-head — three local models, two Secuura tickets, read against the ticket (2026-09-14)

Kam (16:00): "test them head to head or compare their results during a quiet time. Speed doesn't matter … but the accuracy will matter, and metrics don't always tell the truth."
This is the part the mechanical checker cannot do: each patch READ against its ticket, plus three cheap runtime probes in the existing scratch clones. Written by the Wednesday-assistant subagent. Read-only everywhere except this file; nothing under `!CODING/` was touched (source checkout `git status --porcelain` = 0 entries before and after). No recommendation on which model to keep — Kam decides.

Run dirs: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-14_<ticket>-<model>[-v034|-r2]/`

---

## FOUND

**Headline, in one paragraph.** On KS-806 every model that produced anything wrote the SAME product line — because `tasks/code_patch/task.md` hands the exact expression (`crypto.createHash('sha256')…slice(0, 24)`) to the model; the contest there is test quality and diff arithmetic, not the fix. On KS-871 every model that produced anything wrote the SAME PARTIAL fix — path captured at entry and used for `details.path` only — leaving `deriveAction(req)` (ticket site `:108`, called at `:230` inside `finish`) reading the trimmed path, so a refused erasure is now audited with the right `path` but still with `action='unknown.create'`, `resourceType='unknown'`. **Measured at runtime, not inferred** (TESTED §B): the tip, the gpt-oss:120b fix and the Ornith fix all give `['unknown.create','unknown']` for the refused case. The checker's two 7/7 PASSes on KS-871 are honest about what they measure (the model's own test, which asserts only `details.path`) and blind to the rest of the ticket. Both 120B "FAIL A2" runs on Ollama 0.34.0 have CORRECT content on KS-806 (measured: red-first for the right reason, green-after, control present — TESTED §A) and the same partial content on KS-871; only the unified-diff mechanics differ from the 0.18.2 runs. Ornith's two empty KS-806 answers are one deterministic server-side cut, not two model failures: byte-identical thinking length (15,728 chars), `done:false`, no `done_reason`, and the Ollama log shows the request returned 200 followed by `srv stop: cancel task` at the identical token position (`n_tokens = 17027`) both times — at `temperature: 0` a re-run is a replay, not a re-roll. gpt-oss:20b on KS-871 thought for 92K chars until the 32K context was full (`truncated = 1`, `done_reason: length`) and emitted nothing.

**Verified facts about the tickets that change how the patches read:**
- KS-806 has ONE product site (ticket `:171` = tip `:200`). Fix-shape item 2 ("verify `createUser`'s ON CONFLICT actually updates rather than fabricating — unverified by me") is now verified by reading `userRepo.ts:664-735` at the tip: `INSERT … ON CONFLICT (email_lookup_hash) … DO UPDATE SET password_hash/display_name/email_verified/tenant_id/tenant_slug/updated_at` — it does NOT update `id` or `wallet_address`, and `createUser` returns the in-memory `user` (fresh uuid, ACTIVE, no MFA) regardless. So on a collision the second wallet gets a fabricated object whose `id` is not in the DB, and because `wallet_address` is never updated the lookup misses again next time — it takes the create branch on EVERY authentication. The ticket's "if it behaves as written" is confirmed; the hash fix closes it by removing the collision. No model could address item 2 (it is a verification, and the output format is diff-only) — a PR description would need to say this; none can.
- KS-871's acceptance line "and the GET with its full path" is NOT APPLICABLE to `audit.ts`: `AUDITED_METHODS = POST/PUT/PATCH/DELETE` (`:58`, gate `:205`) — GET is never audited. No model said so (format forbids prose); no model tested GET either.
- KS-871 sites inside `res.on('finish')` that read `req.path` at the tip: `:230→:108` (`deriveAction`, ticket-named), `:247` and `:274` (login special-cases, not ticket-named, latent for any refused `/api/auth/login`), `:280` (`details.path`, ticket-named), `:319` (warn-log path, cosmetic). The ticket's fix shape ("capture once at entry … use that inside the finish handler") plus its Where-list means a complete patch routes the captured path into `deriveAction` as well.
- Nothing at the tip keys on the `...` in `...@wallet.local` (`git grep` over services/packages: only `wallet.ts:200` itself and a doc comment in `passwordLoginGate.ts:180` that describes the OLD shape and is stale under every fix).

---

## TESTED (runtime, scratchpad clones only)

**A. The two KS-806 diffs that failed A2 — applied by CONTENT, mechanics bypassed.** A script took each model's `-`/`+` product line pair and every `+` line after the test-file header, wrote them straight into the clean scratch clone, ran the test at the tip (test only), then with the product change, then restored the clone (`git checkout -- wallet.ts`, test file moved out by `mv`).

| run | red-first at tip | reason | green after | control cell | whole auth suite after |
|---|---|---|---|---|---|
| ks806-gptoss120b-v034 | 1 failed / 2 run | `expected 'addr_tes...@wallet.local' not to be 'addr_tes...@wallet.local'` | 2/2 | yes (`CONTROL — first wallet receives token pair`, passes before and after) | not run (product line byte-identical to the 0.18.2 PASS bar the trailing `// KS-806`) |
| ks806-gptoss20b | 1 failed / 2 run | same assertion, same reason | 2/2 | yes | **711/711 green** (709 + 2 added) — the dropped `...` breaks nothing |

Verdict: for both A2-FAIL runs the content is right; only the diff arithmetic is wrong.

**B. KS-871 action probe.** A 3-cell probe (refused → `details.path`; refused → `[params[3], params[4]]` i.e. `action`,`resource_type`; admitted control) was copied into `src/__tests__/` of three clones, run, and moved out again:

| clone state | refused path | refused action/resourceType | admitted control |
|---|---|---|---|
| untouched tip (`clone_gptoss120b-v034_ks871`) | FAIL `'/'` | FAIL `['unknown.create','unknown']` | pass |
| gpt-oss:120b 0.18.2 fix applied (`clone_gptoss_ks871`) | pass | **FAIL `['unknown.create','unknown']`** | pass |
| Ornith fix applied (`clone_ornith35b_ks871`) | pass | **FAIL `['unknown.create','unknown']`** | pass |

Verdict: every KS-871 fix produced today is partial — path fixed, action not. Expected complete value is `['gdpr.create','gdpr']` (the admitted control shows that is what `deriveAction` yields when it sees the full path).

**Not tested:** the 120B-v034 KS-871 product hunk at runtime (byte-for-byte the same two effective lines as the 0.18.2 hunk, plus a no-op `-`/`+` on an unchanged comment; the probe result would be identical). Type-checking of any test file (vitest does not type-check; service tsconfig excludes `__tests__`).

---

## HOW (commands; all paths absolute, no `cd` in any call — the one `cd` lives inside a scratchpad script)

```
cat <run>/checker.out ; cat <run>/out.md ; cat <run>/out.md.meta.json ; cat <run>/run.log           # every run dir
python3 - <<EOF  json.load(open('<run>/input.json'))  → ticket.description verbatim, files[product_file] with line numbers
cat /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/code_patch/task.md              # what the models were told (fix shape given!)
sed -n 70,150p /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/lib/lm_call.py            # temperature 0, stream false, 600 s timeout
python3 -c 'json.load(open("…ks806-ornith35b-r2/out.md.raw.json"))'                                # done:false, content "", thinking 15728 chars, cut mid-line
/usr/bin/grep -n "GIN\].*api/chat\|n_gen = \|cancel task\|stop processing" …/logs/ollama_serve_v0.34.log   # per-request last n_gen, the two cancel lines
python3 - manifests/…/ornith/35b → params blob = {"stop":["<|im_end|>"],"temperature":0.6,"top_k":20,"top_p":0.95}   # no num_predict cap
git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" show f09b6294…:Blockchain/Dev/services/auth/src/repositories/userRepo.ts | sed -n 660,735p   # createUser ON CONFLICT
git -C <scratch clone> grep -n -i "wallet\.local" HEAD -- Blockchain/Dev/services Blockchain/Dev/packages                    # what keys on the literal
# TESTED A:  python3 <scratch>/h2h/apply_by_content.py <run> <clone> ; bash <scratch>/h2h/vitest_in.sh <svc> <label> <out> <testfile>
# TESTED B:  cp <scratch>/h2h/ks871-action-probe.test.ts <svc>/src/__tests__/zz-h2h-…test.ts ; vitest_in.sh … ; mv it back out
# restore:   mv <testfile> <scratch>/h2h/quarantine_*.test.ts ; git -C <scratch clone> checkout -- <product file> ; git status --porcelain → []
```
Scratchpad artefacts (not project files): `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c9a96567-d2f6-4503-bba7-32c74bbdfa29/scratchpad/h2h/` (scripts, probe, vitest JSON/out per run, quarantined test copies).

---

## PER-RUN

### KS-806 — synthetic wallet email buckets on `slice(0, 8)` (auth, `wallet.ts:200`)
Ticket fix shape: (1) full address or hash as local-part; (2) verify `createUser` ON CONFLICT; (3) test: two addresses sharing an 8-char prefix → two accounts, red-proofed. Sites: `:200` only.

#### ks806-gptoss120b (Ollama 0.18.2) — checker PASS 7/7
1. **Produced:** one diff, two files. Product hunk verbatim:
   ```diff
   @@ -165,7 +165,7 @@
      // Create a new wallet user via userRepo (persists to DB)
      const user: User = {
        id: uuidv4(),
   -    email: `${walletAddress.slice(0, 8)}...@wallet.local`,
   +    // KS-806: use hash of full wallet address for synthetic email to avoid collisions
   +    email: `${crypto.createHash('sha256').update(walletAddress).digest('hex').slice(0, 24)}...@wallet.local`,
        emailVerified: false,
        phoneVerified: false,
        mfaEnabled: false,
   ```
2. **Fix shape:** yes — item 1 exactly as the task prompt dictated (24 hex = 96 bits of SHA-256; not "full address" but injective for any practical purpose; keeps `@wallet.local`; keeps `...`). Site `:200` fixed. Item 2: not applicable to a diff (see FOUND — verified by me, not by the model). Item 3: yes.
3. **Test:** drives `POST /api/auth/wallet/verify` twice (`addr_test1qrjjw7rrks796example…` / `…differentaddress…`, shared prefix 25 chars), captures `createUser` args, asserts 2 users created and `email1 !== email2`. Pins the whole ticket (one site). Real red-first: checker A4 = 1 failed / 1 run at the tip. **No CONTROL cell** (task rule 4 asked for one; checker INFO line says so). Dead code: a `vi.hoisted` `state` object (status/mfa/lockedOut) is declared and never read — copied from the reference test. `createdUsers` is a plain module const captured by the mock factory (works because the factory runs at the lazy `import()` in `beforeAll`).
4. **Mechanics:** hunk header line number wrong (`-165` vs real `197`; git tolerates the offset) and count wrong (declared 7/7, actual 7/8 — two `+` lines for one `-`). Applies only with `--recount --ignore-whitespace`; strict rc=128. Test-file hunk correct (145 lines declared and actual).
5. **Merge as-is?** With edits — re-emit the hunk header, add a control cell, delete the dead `state`, and the PR must state the ON CONFLICT finding. The product line itself is mergeable.

#### ks806-gptoss120b-v034 (Ollama 0.34.0, same prompt, temperature 0) — checker FAIL A2
1. **Produced:** one diff. Product hunk verbatim:
   ```diff
   @@ -197,7 +197,7 @@
      // Create a new wallet user via userRepo (persists to DB)
      const user: User = {
        id: uuidv4(),
   -    email: `${walletAddress.slice(0, 8)}...@wallet.local`,
   +    email: `${crypto.createHash('sha256').update(walletAddress).digest('hex').slice(0, 24)}...@wallet.local`, // KS-806
        emailVerified: false,
        phoneVerified: false,
        mfaEnabled: false,
        role: 'OWNER',
   @@ -0,0 +1,115 @@
   +++ b/…/ks806-wallet-synthetic-email-injective.test.ts
   @@ -0,0 +1,115 @@
   ```
2. **Fix shape:** yes — same expression, one-line form with trailing comment (closer to "minimal" than the 0.18.2 two-line version). Site `:200` fixed. **Content verified at runtime (TESTED §A).**
3. **Test:** BETTER than the 0.18.2 run: has a CONTROL cell (first wallet gets the minted token), uses a `currentWallet` set-before-each-request exactly as rule 6b asks, resets `createdUsers`/`state` in `beforeEach`, `state` IS used (lockout mock + reset). Red cell asserts 2 created users with different emails. Red-first for the right reason (measured). Oddity: the `isLockedOut` mock compares against `${WALLET1.slice(0, 8)}...@wallet.local` — harmless (lockedOut is always false) but shows it pattern-matched the reference rather than reasoned.
4. **Mechanics — three faults:** (a) product hunk declared 7/7, actual 8/8 (four trailing context lines); (b) the `--- /dev/null` header is missing — a stray `@@ -0,0 +1,115 @@` sits where it should be, so git reads "patch fragment without header at line 13"; (c) new-file count declared 115, actual 148. Line number `-197` is correct this time.
5. **Merge as-is?** No (does not apply). After a mechanical re-emit: with edits (same PR-text caveat). Content-wise this is the best KS-806 answer of the day.

#### ks806-gptoss20b (Ollama 0.34.0) — checker FAIL A2
1. **Produced:** one diff. Product hunk verbatim:
   ```diff
   @@
      const user: User = {
        id: uuidv4(),
   -    email: `${walletAddress.slice(0, 8)}...@wallet.local`,
   +    email: `${crypto.createHash('sha256').update(walletAddress).digest('hex').slice(0, 24)}@wallet.local`, // KS-806
        emailVerified: false,
        phoneVerified: false,
        mfaEnabled: false,
        role: 'OWNER',
   @@
   ```
2. **Fix shape:** yes, with one deviation — it DROPS the `...` literal (email becomes `<24hex>@wallet.local`). Nothing keys on it (git grep) and the whole auth suite stays 711/711 with it applied (TESTED §A); arguably cleaner, but rule 5 said minimal. Site `:200` fixed.
3. **Test:** follows rule 6a/6b literally — everything in one `vi.hoisted` state (`walletAddress`, `createdUsers`), CONTROL cell present, red cell uses `addr_test1abcde…` / `addr_test1fghij…` (10 shared chars), reads `createdUsers[0].email` after each call and asserts inequality. Red-first for the right reason (measured). Title says `RED —` not `🔴 KS-806 —` (task asked for the KS id in the title; the checker does not gate on it). `verify()` carries unused `extra`/`path` parameters with defaults — fine under `noUnusedParameters` since they are used in the body.
4. **Mechanics:** every hunk header is a bare `@@` with no ranges, plus a stray trailing `@@` after the product hunk — git: "No valid patches in input". Context indentation and content are otherwise right. Nothing to recount; it needs a re-emit.
5. **Merge as-is?** No (does not apply). After re-emit: with edits (the `...` decision is a one-line reviewer call).

#### ks806-ornith35b and ks806-ornith35b-r2 — checker FAIL A1 (empty content), twice
1. **Produced:** nothing (`out.md` = one newline, both runs). Meta both runs: `eval_count null, done_reason null, thinking_chars 15728` (identical), wall 83.2 s then 73.3 s. r2's saved `out.md.raw.json`: `done: false`, `message.content: ""`, thinking cut mid-identifier (`const ADDR_A = 'addr_test1qxyzabc0000…`). The thinking that exists is on-track: it found line 200, planned the sha256 line, counted a correct `@@ -197,7 +197,7 @@`, and was designing the two-address test when it was cut.
2–3. **N/A.**
4. **Server side:** `ollama_serve_v0.34.log` shows for both requests `[GIN] 200` then `srv stop: cancel task` then `stop processing: n_tokens = 17027` (12,032 prompt + ~4,995 generated) — the only two requests of the day with a `cancel task` line. Every other request releases normally before its 200. Model params blob has no `num_predict`; the harness sends `temperature: 0`, so the replay is exact. Cause unresolved (server/parser side, not the model's reasoning); the KS-871 prompt on the same model did not trigger it.
5. **Merge as-is?** Nothing to merge. r2 could not have differed from r1 at temperature 0.

### KS-871 — audit log reads `req.path` after the response (api-gateway, `audit.ts:280`)
Ticket fix shape: capture once at entry (`const auditPath = req.originalUrl.split('?')[0]`) and use it inside the finish handler; Where-list `:206` (gate, correct), `:224→:108` (`deriveAction` reads `req.path`), `:280` (`details.path`). Acceptance: refused erasure audited with `/api/gdpr/erasures` (GET: N/A — not audited); admitted unchanged; fix at the capture point.

Site table (same for all three fixes produced):

| site (tip line) | what | 120B 0.18.2 | 120B 0.34.0 | Ornith |
|---|---|---|---|---|
| `:206-208` entry gate | reads `req.path` at entry — correct, leave | n/a | n/a | n/a |
| `:230 → :108` `deriveAction(req)` in finish | **ticket-named** | **not fixed** | **not fixed** | **not fixed** |
| `:280` `details.path` | **ticket-named** | fixed | fixed | fixed |
| `:247`, `:274` login checks in finish | not named; same class | not fixed | not fixed | not fixed |
| `:319` warn-log path | not named; cosmetic | not fixed | not fixed | not fixed |
| GET `/api/gdpr/erasures/:ref` | acceptance line | N/A (GET not audited) | N/A | N/A |

#### ks871-gptoss120b (Ollama 0.18.2) — checker PASS 7/7 (BUILD_REPORT says PARTIAL — confirmed, and now measured)
1. **Produced:** one diff, two files. Product hunk verbatim:
   ```diff
   @@ -148,2 +148,3 @@
      const start = Date.now();
   +  const auditPath = req.originalUrl.split('?')[0]; // KS-871
    
   @@ -182,3 +182,4 @@
            method: req.method,
   -            path: req.path,
   +            path: auditPath, // KS-871
            status: res.statusCode,
            durationMs: Date.now() - start,
   ```
2. **Fix shape:** capture point right (after `const start`, before the listener), used at `:280` only. `deriveAction` untouched → refused erasure audited as `action='unknown.create'`, `resource_type='unknown'` (TESTED §B). Follows the ticket's fix-shape SENTENCE, ignores its Where-list. Partial.
3. **Test:** CONTROL (admitted, `delete process.env[FLAG]`, WITH_SCOPE → 200 → path) and 🔴 (ROLE_ONLY, flag on → 403 → path). Polls 20×100 ms for the fire-and-forget insert. Asserts `details.path` only — cannot see the action gap. Real red-first: A4 1 failed / 2 run, failure `expected '/' to be '/api/gdpr/erasures'`. Typing loose: `as any` ×4, `(req, _res, next)` implicit-any (standalone tsc: 7 errors in the test — not gated). Does not assert the upstream was reached in the control.
4. **Mechanics:** hunk line numbers wrong (`-148` vs real `210`; `-182` vs `278`), hunk 2 declared 3/4 actual 4/4, context indented 8 spaces where the source has 12 (needs `--ignore-whitespace`), new-file count declared 102 actual 106 (strict apply would have silently truncated the test — see BUILD_REPORT caveat 1). Applies only with `--recount --ignore-whitespace`.
5. **Merge as-is?** No — incomplete against the ticket (audit rows for refused erasures would carry the wrong action, which is what a SIEM groups on), and the mechanics need a re-emit.

#### ks871-gptoss120b-v034 (Ollama 0.34.0) — checker FAIL A2
1. **Produced:** one diff, **product file only — no test file at all** (rule 3/4 violated outright). Product hunk verbatim:
   ```diff
   @@ -250,7 +250,8 @@
              const start = Date.now();
    
   -          // Wrap res.json so the login-success path can extract the userId from
   +          // Wrap res.json so the login-success path can extract the userId from
              // the response body. Without this, /api/auth/login audit entries have a null
              // actor — defeating the whole point of the audit log for the most
              // important event. The wrapper is non-invasive: it captures the body
              // synchronously then defers to the original res.json().
   +          const auditPath = req.originalUrl.split('?')[0]; // KS-871: capture path at entry
              const origJson = res.json.bind(res);
              let capturedBody: unknown = null;
              res.json = function patched(body: unknown) {
   @@ -280,7 +281,7 @@
              const details = JSON.stringify({
                method: req.method,
   -            path: req.path,
   +            path: auditPath,
                status: res.statusCode,
                durationMs: Date.now() - start,
                tenantId: u?.tenantId || null,
   ```
2. **Fix shape:** effectively the same two lines as the 0.18.2 run → same partial. Extra noise: a `-`/`+` pair on an unchanged comment line, and the new line is placed under the res.json comment block so the comment now describes the wrong thing.
3. **Test:** none. Nothing pins anything. (Whether the thinking contained a test is unknowable — raw saving was added after this run.)
4. **Mechanics:** line numbers wrong (`-250` vs real `210`), context indented 10 spaces where the source has 4, hunk 1 declared 7/8 actual 10/11, hunk 2 declared 7/7 actual 6/6; strict "patch fragment without header at line 16", lenient "patch does not apply".
5. **Merge as-is?** No — no test, does not apply, partial fix, spurious comment churn. Worst of the day's non-empty outputs.

#### ks871-gptoss20b (Ollama 0.34.0) — checker FAIL A1 (`done_reason: length`)
1. **Produced:** nothing. Meta: `eval_count 21881`, `thinking_chars 92028`, `done_reason "length"`, wall 249 s; server log `n_tokens = 32767, truncated = 1` — it filled the 32K context (10.9K prompt + 21.9K thinking) and never started the answer.
2–4. **N/A.** 5. Nothing to merge. (Its KS-806 thinking was 23.6K chars for a complete answer; KS-871 sent it into a loop — a `num_ctx` of 32K is a real ceiling for this model on this task.)

#### ks871-ornith35b (Ollama 0.34.0) — checker PASS 7/7
1. **Produced:** one diff with `diff --git` + fake `index 1234567..abcdefg` lines (harmless to `git apply` without `--3way`). Product hunk verbatim:
   ```diff
   @@ -203,6 +203,8 @@
        const start = Date.now();
    
   +    // KS-871: capture the path once at entry — req.path is trimmed by express after the response is sent, so we use req.originalUrl instead.
   +    const auditPath = req.originalUrl.split('?')[0];
   +
        // Wrap res.json so the login-success path can extract the userId from the
        // response body. Without this, /api/auth/login audit entries have a null
        // actor — defeating the whole point of the audit log for the most
   @@ -277,7 +279,7 @@
              const details = JSON.stringify({
                method: req.method,
   -            path: req.path,
   +            path: auditPath, // KS-871: use the captured path, not req.path (which is trimmed after response)
                status: res.statusCode,
                durationMs: Date.now() - start,
                tenantId: u?.tenantId || null,
   ```
2. **Fix shape:** same partial as the 120B (TESTED §B: `['unknown.create','unknown']` with this fix applied). Placement is the cleanest of the three (own comment, blank line, before the res.json block). The comment's mechanism is wrong — `req.path` is trimmed by the `router.use(prefix)` mount during routing, not "after the response is sent" — a reviewer would reword it.
3. **Test:** the best test of the three KS-871 outputs: typed casts instead of `as any` (`as RequestHandler`, `Parameters<typeof createProxyRoutes>[0]`), a `pollQueryCalls` helper bounded to 2 s that throws if the write never happens (as the reference note asked), CONTROL asserts `received.length === 1` (upstream actually reached) as well as the path. Red cell first, control second. Asserts `details.path` only — same blind spot. Standalone tsc: 5 errors in the test (`vi.fn` type vs `query` signature; `calls[0][1]` tuple index) — not gated, same class as the 120B's.
4. **Mechanics:** hunk 1 declared 6/8 actual 5/8; hunk 2 declared 7/7 actual 6/6; new-file count declared 95 actual 112; line numbers close (`-203` vs `210`, `-277` vs `278`). Applies only with `--recount --ignore-whitespace` (strict rc=128 on the product section).
5. **Merge as-is?** No — same incomplete fix; after adding the `deriveAction` routing and a recount, with edits (comment wording, test typing).

---

## COMPARISON

### KS-806 (fix given in the prompt; one site)
- **Accuracy of the fix:** 1= gpt-oss:120b (both runtimes) and gpt-oss:20b — identical hash expression, site fixed; the 20B's dropped `...` is a harmless deviation (711/711 measured). 3 Ornith — no output (server-side cut, deterministic).
- **Test quality:** 1 gpt-oss:120b on 0.34.0 (control cell, rule-6b-literal `currentWallet`, clean resets) ≈ 2 gpt-oss:20b (control cell, hoisted state exactly as rule 6a asks; title lacks the KS id) > 3 gpt-oss:120b on 0.18.2 (no control cell, dead `state` object) > Ornith (none). All three real tests go red at the tip for the RIGHT reason (measured for all three).
- **Mechanics:** 1 gpt-oss:120b on 0.18.2 (applies with recount) > 2 gpt-oss:120b on 0.34.0 (missing `--- /dev/null`, two miscounts — does not apply) ≈ 2 gpt-oss:20b (bare `@@` — does not apply) > Ornith (nothing).

### KS-871 (fix sentence given in the ticket; two named sites)
- **Accuracy of the fix:** three-way tie, all PARTIAL — gpt-oss:120b (0.18.2), gpt-oss:120b (0.34.0), Ornith each fixed `:280` and left `:108` (measured: refused erasure still `unknown.create`). Nobody fixed the whole ticket. gpt-oss:20b — no output (context exhausted).
- **Test quality:** 1 Ornith (typed, bounded poll that throws, upstream-reached assertion) > 2 gpt-oss:120b 0.18.2 (`as any`, silent 2 s poll) > 3 gpt-oss:120b 0.34.0 (no test) = gpt-oss:20b (no output). Neither real test asserts `action`, so neither can catch its own fix being partial.
- **Mechanics:** 1= Ornith and gpt-oss:120b 0.18.2 (both apply only with `--recount --ignore-whitespace`; Ornith 3 miscounts, 120B 2 miscounts + whitespace) > gpt-oss:120b 0.34.0 (does not apply) > gpt-oss:20b (nothing).

### Run-to-run variance (same model, same prompt bytes — sha256 identical — temperature 0)
- gpt-oss:120b on KS-806: Ollama 0.18.2 → PASS 7/7 with a weaker test; Ollama 0.34.0 → FAIL A2 with a stronger test and one more mechanical fault. Thinking 24.5K vs 13.5K chars; output 8,169 vs 5,248 tokens. Same product line to the byte (bar comment placement).
- gpt-oss:120b on KS-871: 0.18.2 → PASS with a test; 0.34.0 → product-only, no test. Same partial fix.
- Ornith on KS-806: two runs, byte-identical thinking length and identical cut position — at temperature 0 on the same runtime the model is a deterministic function of the prompt; "re-run" changed nothing and could not.
- So what varied today was the RUNTIME (0.18.2 vs 0.34.0 — different kernels/templating/parsers), not sampling. The checker's PASS/FAIL flipped on diff arithmetic (a missing header line, a miscounted hunk) while the semantic content stayed the same — the mechanical verdict is the most runtime-sensitive part of the score and the least informative about the fix.

### What a single run per model can and cannot establish
- CAN: what this model, on this runtime, with this prompt, does — as a deterministic point sample (temperature 0). Whether its content is right (by reading + by a content-applied run). Where its blind spots are (both PASS runs on KS-871 passed their own test and failed the ticket).
- CANNOT: a pass RATE, robustness to prompt wording, or how often the diff arithmetic lands — those need several prompts per model, or temperature > 0 with several seeds, on ONE runtime. It also cannot separate "model" from "Ollama version" unless each model is run on both, which only the 120B was.
- Also NOT established today: any model's ability to find sites the fix sentence did not spell out. Both tickets told the model the fix; on the one ticket with a second site (`:108`), 0 of 3 found it. The task prompt's own "Fix shape" paragraph is KS-806-specific and was still in the KS-871 prompt.

Speed footnote (from `out.md.meta.json`; not a criterion): KS-806 — 120B/0.18.2 164.6 s (8,169 tok, 62.6 tok/s) · 120B/0.34.0 119.7 s (5,248, 67.0) · 20B 90.3 s (7,782, 95.2) · Ornith 83.2 s / 73.3 s (~4,995 tok before the cut, ~83 tok/s per server log). KS-871 — 120B/0.18.2 148.3 s (7,712, 64.9) · 120B/0.34.0 98.6 s (4,791, 67.3) · 20B 249.2 s (21,881, 91.9, length) · Ornith 77.0 s (4,887, 83.5).
