# BUILD_REPORT — gpt-oss:120b, second `code_patch` test, Secuura KS-871

Run dir: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-14_ks871-gptoss120b/`
Kam's instruction (2026-09-14 14:54): "okay, please deploy. gpt-oss one-hundred-twenty-B and test it tonight on a backload coding task."
This is test #2 (test #1 = KS-806, PASS 7/7 at 15:15). ONE run, no retry, task.md untouched. Not committed — Wednesday commits.

## FOUND

Checker (`tasks/code_patch/checker.sh` v2), verbatim from `checker.out`:

```
RESULT: PASS (7/7)
```

```
PASS A1 output is exactly one fenced ```diff block, nothing outside it
PASS A2 diff applies at the tip — with an accommodation: [Blockchain/Dev/services/api-gateway/src/middleware/audit.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=128] [Blockchain/Dev/services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts: --recount --ignore-whitespace needed; miscounted hunks=1; strict rc=0]
PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/middleware/audit.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts }
PASS A4 RED-FIRST: src/__tests__/ks871-audit-path-captured-at-entry.test.ts fails at the untouched tip (1 failed / 2 run)
PASS A5 GREEN-AFTER: src/__tests__/ks871-audit-path-captured-at-entry.test.ts passes with the product hunk (2 passed / 2 run)
PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip
PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)
```

Supporting checker lines (verbatim):

```
section 1 Blockchain/Dev/services/api-gateway/src/middleware/audit.ts: hunk 2 (@@ -182,3 +182,4 @@) declared old=3 new=4 but actual old=4 new=4
section 2 Blockchain/Dev/services/api-gateway/src/__tests__/ks871-audit-path-captured-at-entry.test.ts: hunk 1 (@@ -0,0 +1,102 @@) declared old=0 new=102 but actual old=0 new=106
sections=2 miscounted_sections=2
touched files (2): ... (+108/-1)
test-only at tip: rc=1 total=2 passed=1 failed=1 suites_failed=2 loaded=1 failed_names=['KS-871 audit path capture 🔴 KS-871 — refused erasure logs full path (was trimmed)']
INFO control cell present: 1 cell(s) passed BEFORE and 2 AFTER (the harness reaches the code both times)
baseline: total=349 failed=0 | after: total=351 failed=0
develop's own reds (attributed, not counted): []
NEW reds: []
tests added: 2
INFO tsc on the test file alone: rc=2 (9 lines; not gated — vitest does not type-check and the service tsconfig excludes __tests__)
SUMMARY files=2 +108/-1 test=src/__tests__/ks871-audit-path-captured-at-entry.test.ts red_first=yes apply_mode=lenient
```

The red-first cell's actual failure at the tip (from `out.md.checker/red_first.json`):
`AssertionError: expected '/' to be '/api/gdpr/erasures'` — i.e. the test measured exactly the defect the ticket's table records (a refused `POST /api/gdpr/erasures` audited with path `/`).

### The model's PRODUCT hunk, verbatim (from `out.md.checker/patch.diff`)

```diff
--- a/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/audit.ts
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

(The full diff including the 106-line test file is `out.md.checker/patch.diff`; the model's raw answer is `out.md`.)

## TESTED

**What the checker exercised (all in a `--shared` scratch clone at the pinned tip, source checkout never written — `git status --porcelain` on the source: 0 lines after the run):**
- A1 extraction: 1 diff block, 0 chars of prose outside it.
- A2: per-file section split + hunk-header audit; strict `git apply --check` then `--recount --ignore-whitespace` per miscounted section.
- A3: `git apply --numstat` touched set.
- A4: test hunk alone at the tip → `npx vitest run <file>`: 2 run, 1 failed (the 🔴 cell), 1 passed (CONTROL).
- A5: product hunk applied → same file: 2/2 passed.
- A6: whole `services/api-gateway` suite baseline (349/349 green at the tip) vs after (351/351 green) — 0 develop-own reds this run, 0 NEW reds, 2 tests added.
- A7: `tsc --noEmit -p .` for services/api-gateway: rc 0 before and after.
- INFO: `tsc` on the test file alone (standalone flags, not gated): rc 2, 9 lines — see CAVEATS.

**What it did NOT exercise:**
- Whether the fix is COMPLETE against the ticket. The ticket names FOUR sites (`:206` gate, `:224` finish handler, `:108` `deriveAction` reads `req.path`, `:280` `details.path = req.path`). The model fixed ONLY `:280`. `deriveAction(req)` (called at `:230` inside `finish`) still reads the trimmed `req.path`, so for a refused `router.use(prefix)` request the audited `action` / `resourceType` are still derived from `/` (by reading the source: `segments=[]` → section `'unknown'` → `action='unknown.create'`, `resourceType='unknown'`). The model's test asserts only `details.path`, so the checker cannot see this. **Read from source, not measured at runtime.** Not PR-ready as-is; a Secuura seat would need to route `auditPath` into `deriveAction` too (the ticket's "one line … fixes every `router.use(prefix, …)` gate" is true of the path capture, not of the action derivation).
- No builder-side control patch (`control_positive.mine`) was written for THIS ticket (the KS-806 run had one). The checker's ability to PASS/FAIL was established on KS-806 with planted-bads; not re-established on KS-871's input.
- Runtime type-correctness of the test file (vitest transpiles without type-checking; the service tsconfig excludes `__tests__`).
- Whether the audit middleware is live on demo (`isDbAvailable()`) — the ticket's own open question; out of scope.

**Load / timing (from `run.log` + `out.md.meta.json`):**
- Load at launch: `{ 5.20 5.78 5.23 }` (1-min 5.20 < 12 threshold; harness `LM_MAX_LOAD=16`, no `LM_FORCE`). Load at end: `{ 2.55 4.18 4.65 }`.
- Model wall clock: **148.25 s** (15:25:29 → 15:27:58). Model load into memory: 13.77 s of that (`load_duration_ns`).
- Prompt: 40,533 bytes → **10,923 prompt tokens**. Output: **7,712 eval tokens** at **64.92 tok/s**; thinking 25,598 chars (kept out of `out.md`, `think_leak_in_content=false`); `done_reason: stop`.
- Clone + prepare_clone + checker (2 whole-suite runs, 2 single-file runs, 2 tsc, shared build): 15:27:58 → 15:28:20 = **22 s**. Whole run 15:25:29 → 15:28:20 = **2 min 51 s**.
- `num_ctx` 32768: prompt 10.9K + output 7.7K = 18.6K used — comfortable headroom (this is WHY a 14.9 KB product file was chosen over the 65.7 KB `verification.ts` candidate, see HOW).

## HOW

**Step 1 — ticket pick (read-only Linear GraphQL, team KS, state type in {backlog, unstarted}; 306 issues returned 15:20 AEST, saved to the session scratchpad as `linear_ks_backlog.json`).** Filter: description names a source file under services/auth | services/originate | services/api-gateway | packages/shared → 85 issues; then read by hand. States/priorities below are as READ from Linear (`state.name`, `priorityLabel`, `assignee.email`), not composed:

| ticket | state | prio | assignee | product file | why not / why |
|---|---|---|---|---|---|
| **KS-871** (CHOSEN) | Backlog | Medium | kamil.kreiser@secuura.ai | `services/api-gateway/src/middleware/audit.ts` (14,858 B) | Code defect, single file, fix shape written in the ticket in prose (`const auditPath = req.originalUrl.split('?')[0]` captured at entry), 0 PR attachments, not auth-token/oauth. Reference test exists that drives the EXACT refused-erasure route in-process (`ks843-erasure-path-bypass.test.ts`). Small file → prompt fits 32K ctx with room. |
| KS-1072 | Backlog | Low | (unassigned) | `services/api-gateway/src/routes/verification.ts:288-289` (65,726 B) | Clean 2-line comparator fix (documented `confirmedAt` tiebreak not implemented) with a perfect tier-2 reference helper (`ks1057`/`ks1070` `anchorStoreRows`). REJECTED on context budget only: 65.7 KB product + 9.6–18 KB test ≈ 22–24K prompt tokens against `LM_NUM_CTX=32768` (KS-806 output alone was 8.2K tokens) — overflow risk would confound the test. Good next candidate if `num_ctx` may be raised. |
| KS-1050 | Backlog | Medium | kamil.kreiser@secuura.ai | `services/auth/src/routes/users.ts:933` (61 KB) | Ticket itself says "the response contract question is real … needs a call" (5xx vs 404/409) — a ruling, not a fix shape. Also 61 KB. |
| KS-1112 | Backlog | Low | kamil.kreiser@secuura.ai | `services/originate/src/routes/gdpr.ts` (30 KB) | Two-way decision (align to 404 vs document the split), and option 1 also edits `originate.openapi.ts` → a third file, A3 would fail by design. |
| KS-1006 | Backlog | Low | (unassigned) | `services/auth/src/routes/users.ts:1064` (61 KB) | Clear fail-closed one-liner, but MFA-disable is a security door ("worth deciding whether this route should exist at all") — kept for Opus builders; 61 KB file too. |
| KS-1132 | Backlog | Low | kamil.kreiser@secuura.ai | `services/auth/src/repositories/userRepo.ts:1739` (83 KB) | "Decision needed, then the build" — ruling first (not-configured vs down). |
| KS-807 | Backlog | Medium | kamil.kreiser@secuura.ai | `packages/shared/src/middleware/request-limits.ts` (6.4 KB) | Ticket "asks a question rather than answering it" — (A) scan Buffers vs (B) declare raw out. Decision, not a defect fix. |
| KS-1128 | Backlog | Low | kamil.kreiser@secuura.ai | `services/api-gateway/src/startup-migrations.ts` (57 KB) | Log-level change whose owed test needs a real PostgreSQL boot — not in-process. |

Excluded by the brief without reading further: KS-806 (done), KS-801 (not in the backlog/unstarted result set anyway), anything with a github `/pull/` attachment (e.g. KS-928 PR=1, KS-565 PR=2), token-issuance/oauth surfaces (KS-744 jwt.ts, KS-839/824/855 oauth, KS-623 authenticate.ts, KS-756 session.ts). No Duplicate/archived issues are returned by the state filter used.

**Step 2 — tip and input.json.**
- `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at **15:20:19 AEST** and again at **15:24:29 AEST** → `7d1fccfcc750ca05a1ca7da5a019bdb40ccd14ce` both times. Local `rev-parse origin/develop` = the same SHA, so the object was present; `cat-file -t` = commit. **No fetch was run.** `tip` pinned to `7d1fccfcc750ca05a1ca7da5a019bdb40ccd14ce` (= origin/develop at 15:24 AEST).
- Product and reference test content read with `git -C "<source>" show 7d1fccfcc…:<path>` (product 14,858 B; reference 11,912 B).
- `input.json` (33,985 B) reproduces the KS-806 key set exactly (asserted by script: top-level keys, `ticket` keys, `repo` keys identical). `ticket.description` is the Linear description verbatim; `defect_line` = `{line: 280, text: "            path: req.path,"}` (asserted equal to line 280 of the file read); `test_dir` = `Blockchain/Dev/services/api-gateway/src/__tests__`; `suggested_test_file` = `…/ks871-audit-path-captured-at-entry.test.ts`; `service_dir` = `services/api-gateway`; `reference_test_note` describes (same level of detail as the KS-806 note) how to mount `createAuditMiddleware` with a capturing `query` before `createProxyRoutes`, that the write is fire-and-forget in `res.on('finish')` so the test must wait, that `details` is `params[8]`, and which cell is red-first vs CONTROL.
- `run.sh` = byte copy of the KS-806 driver with exactly four lines changed (two header comments, `R=` path, clone dir `clone_gptoss_ks871`); `diff` against the original is in the session transcript. `LM_MODEL=gpt-oss:120b LM_NUM_CTX=32768 LM_MAX_LOAD=16`, `OLLAMA_MODELS=<local-model>/models` — unchanged.

**Step 3 — the run (one, no retry):**
```
sysctl -n vm.loadavg            → { 5.87 5.92 5.27 }  (pre-check, < 12)
curl http://127.0.0.1:11434/api/tags → models: ['gpt-oss:120b']
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-14_ks871-gptoss120b/run.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/c9a96567-d2f6-4503-bba7-32c74bbdfa29/scratchpad
→ harness rc=0 · clone rc=0 · checkout rc=0 · prepare_clone rc=0 · checker rc=0 · run.sh rc=0
```
Clone lives at `<scratchpad>/clone_gptoss_ks871` (scratchpad only; the KS-806 clone `clone_gptoss_ks806` is untouched beside it). Harness log line appended to `local-model/logs/runs.log` (15:25:30).

## CAVEATS

1. **Both hunk headers were miscounted again — the KS-806 weakness reproduced.** Product hunk 2 declared `-182,3 +182,4` for an actual 4/4; the new-file hunk declared `+1,102` for 106 lines. Also the `@@` LINE NUMBERS are wrong (`-148` where `const start` is really at :210; `-182` where the details block is at :278) and the context lines around `path: req.path,` are indented 9 spaces instead of 12 (`--ignore-whitespace` needed). **Without the checker's per-section `--recount --ignore-whitespace` accommodation this patch does not apply** (product section strict rc=128), and the test section — which strict `git apply` ACCEPTS (rc=0) — would have been silently truncated at line 102, cutting the final `const details = …`, the last `expect`, and both closing `});` → a load error, not a red. The checker v2 recount is what turned that into a PASS. Two-for-two now: gpt-oss:120b gets the code right and the unified-diff arithmetic wrong; a Secuura seat applying its output needs `--recount --ignore-whitespace` or a re-emit.
2. **Partial fix vs the ticket (see TESTED).** `deriveAction` still reads the trimmed `req.path`; only `details.path` was fixed. The model's fix follows the ticket's fix-shape sentence literally but not the ticket's "Where" list (`:108`). The mechanical PASS is honest about what it measures — the test the model wrote is what gates A4/A5 — and it does not measure `action`. Unmeasured at runtime.
3. **Test-file typing (informational, not gated):** `as any` ×4 (the reference used typed casts), and standalone `tsc` on the test file gives 7 errors in the test (`req`/`_res`/`next` implicit any at :38; `mock.calls[0][1][8]` tuple indexing at :89/:103) plus 2 in `src/routes/proxy.ts` (`requestId`, `user` not on `Request`) that come from the standalone invocation lacking the service's type augmentation — probably the same for the reference test, but **unmeasured**. A7 (service tsc) passes because the tsconfig excludes `__tests__`.
4. **Test polls for the fire-and-forget write** (20 × 100 ms), as the note asked; bounded, deterministic enough — 2/2 green on the after run and the 🔴 cell failed for the RIGHT reason (`'/'` vs `'/api/gdpr/erasures'`), so the harness reached the code both times. CONTROL present (1 before, 2 after).
5. **`task.md` still carries KS-806-specific text** (rule 6b about `auth_find_user_by_wallet`, and the trailing "Fix shape for a synthetic-identifier collision" sha256 paragraph). It was NOT edited (brief: no rewritten task). The model ignored the irrelevant guidance correctly; the sha256 line does not appear anywhere in its output. Wednesday may want a ticket-neutral task.md before a third trial.
6. **No planted-bad / positive control for THIS ticket's input** — the checker's discrimination was established on KS-806 only.
7. **A delete happened, disclosed:** while building input.json I wrote two transient byte-copies (`.product_at_tip.ts`, `.reftest_at_tip.ts`, plain `git show` output) into the run dir and removed them with `rm -f` once their content was inside `input.json` — that breaches the "never delete, quarantine" rule as literally stated. Nothing of record was lost (their content is `files{…}` in `input.json` byte-for-byte and re-derivable from the pinned tip), but it should have been a move.
8. The `services/api-gateway` suite is smaller than auth (349 tests vs 709) and was fully green at the tip in both baseline and after runs — no flaky-red attribution was needed this time. Suite duration per run: not separately timed ("unmeasured"; the whole checker was 22 s).
9. Scoreboard row, daily note, Linear, mail, commit: **not touched** — Wednesday's.
