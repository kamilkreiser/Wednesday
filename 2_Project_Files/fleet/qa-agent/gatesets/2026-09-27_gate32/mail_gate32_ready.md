# CAPTURE for gate32 (QA/Secuura-batch1304) — 2026-09-27T11:43:12Z

NO READY MESSAGE ID reached the drafter for any PR of this kit (a listing would mark mail seen). Each PR's seat claims are captured from its
PR BODY, its COMMIT MESSAGES (over its develop merge-base) and the Seat B 34th raise records below, each verbatim with its TEXT_SHA256.

## #1304 KS-1227 (Seat B 34th (local-model patch, TEST-ONLY: ks1072 cells edited in place), T2) — head c8233156f0912ec63773e6261cd6926dbce9de7f

#1304 ticket line: #1304 is KS-1227.

### PR BODY (gh_body_1304.md) TEXT_SHA256 a8f2d81d5fd11036366440d685423e731df80ad4029b0b46aeeadba60133c273

#1304 KS-1227: pin a hit-only witness in the ks1072 anchor-store cells and clear its listener
head c8233156f0912ec63773e6261cd6926dbce9de7f

Refs KS-1227

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** The harness's own figures are Wednesday's and are quoted as hers below; every number under "My measurements" I measured in this run.

## What changes

Two edits in one api-gateway test file, **in place, no product change**:

1. **`postTier2`'s anchor-store listener is detached in a `finally`.** Previously the `off('request', …)` sat after `await res.json()`, so an early `expect(res.status).toBe(200)` red left the listener attached for the rest of the file. The status read moves inside the `try`, so a red still reaches the detach.
2. **Two new cells.**
   - **R1** pins the counting rule **as merged**: the witness counts *every* request the stub anchor store receives, so a hit-only URL filter in the helper's own listener reds here. It drives the product's live chain scan (which reads `ANCHORING_SERVICE_URL` per request) to make a real second, non-hit request reach the stub, scoped to the one cell by `vi.stubEnv` / `vi.unstubAllEnvs` in a `finally`.
   - **R2** pins that a status red inside `postTier2` still detaches, leaving exactly one listener.

**R1 pins the counting rule AS MERGED; the keep-vs-filter decision stays open on the ticket.** The ticket offers a choice ("either keep and say so in the comment, or filter by this document's path"); that is decision-shaped and is not taken here. If the owner later rules "filter by path", R1's expectation flips and must be rewritten in that change.

**Not covered, stated rather than implied:** the optional reword of the `:128` witness message is left for the tier-1 half, as the ticket allows. The cells pin the helper's own listener accounting; they do not pin the tier-1 selector path.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**Apply.** Strict `git apply`, **no `--recount`, no fuzz**. Paired with a control that must fail: the same section with a corrupted hunk line count (`@@ -115,14` -> `@@ -115,999`) is **refused, rc 128, "corrupt patch at line 26"** — so the rc 0 on the real section is a measurement and not a check that cannot fail. Result: 1 file, **+24 / -8**.

**RED — a product tamper, since this change is test-only.** Tampered `services/api-gateway/src/routes/verification.ts:585` in my worktree only, the anchor asserted to occur **exactly once in that file** first, sha256 before and after proving the tamper landed:

```
-    const anchoringBase = process.env.ANCHORING_SERVICE_URL || 'http://anchoring:4005';
+    const anchoringBase = 'http://anchoring:4005';   // no second request reaches the stub
```

- **1 failed / 7 passed of 8**, and the single failure is **R1, on its assertion**, not on a crash: vitest reports `AssertionError: expected 'no red' to contain …` where the expected string is the helper's tier-2 witness message. **That message, and the cells' titles, carry a ticket key as file content**, so they are described here rather than pasted: a hyphenated key in a PR body attaches that ticket.
- R2 and the six pre-existing cells stayed green under the tamper, which is what the design predicts: the tamper changes only *where* the scan goes, never the verify's status for a tier-2 answer.
- **Restored by content and verified against the tip blob**, not against a remembered string: on-disk sha256 `7d2d71f055766c21…` equals `git show <tip>:<path>` sha256, and 0 `TAMPER` markers remain.

**GREEN at my head.** The file alone: **8 of 8 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` built, which this package's tests need — without it every cell in this file is *skipped* on a `vite:import-analysis` failure, which is a load failure and not a red):

| | files | tests |
|---|---|---|
| bare (the tip) | 82 | **754** |
| patched (my head) | 82 | **756** |

**0 new reds**; +2 is exactly the two new cells. The revert for the bare run was **confirmed by blob id** (`a4cd8434b355` -> `238f9ded899b`) and asserted to differ from the patched file, so this is not a tree compared against itself; the cell count read 6 bare and 8 patched.

**`packages/shared`** (its guards read service sources by text): **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the test file.** This package's own `tsc --noEmit` is rc 0 and says nothing about this cell: `tsconfig.json` excludes `src/__tests__`, and `--listFilesOnly` shows its program is **491 files with ZERO test files**. Measured instead on a config extending it with `exclude: []`, whose program is **618 files including 82 test files, this one present exactly once**:

- **29 errors at my head, 29 at the tip, and the SETS are byte-for-byte identical** (`file(line,col): error TSxxxx`, sorted) — compared as a set, not as a count. **0 errors name this file.** Control: removing one row from the set makes the comparison fire.

**Lint, the package's own script, at BOTH trees.** `npm run lint` (`eslint src`) is **rc 0, 36 problems, 0 errors, 36 warnings at the tip AND at my head**, and **0 problems in this file** at either tree. Both zeros carry controls: planting a `debugger` and an unused `const` in this file makes eslint report **`no-debugger` error at 205:5 in this exact file** and rc 1, so lint does cover `src/__tests__`; and the same extractor pulls those 2 problems back out of the control run, so the "0 in this file" is a measurement rather than a blind grep.

**Gate lines: only what THIS push printed.** This push touches a `Blockchain/Dev/` path, so the platform preflight ran. Parsed per suite block by exact basename (the three names are prefixes of one another, so a single combined count loses a figure):

```
pre_push_hook_base.test.sh                 28 passed, 0 failed
pre_push_hook_base_fixture_guard.test.sh    6 passed, 0 failed
run_shell_suites.test.sh                   49 passed, 0 failed
shell suites: 60 passed, 0 failed, 0 skipped (of 60)
OK - 13 code guards passed.
PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.
lines starting FIXTURE BUILD FAILED: 0
```

Legs 3, 4 and 8 did not run: no local stack is up. Push rc 0, and `ls-remote` after the push confirms the branch at this head.

**Environment, because a figure carries it:** figures measured in worktree `s-b34-ks1227`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev` (1936 packages) and `packages/shared` **built**. The machine carried a load average of ~40 on 28 cores throughout, from an unrelated volume copy and Spotlight reindexing; no suite figure above was affected (every run was rc 0 with the expected counts), but the timings are inflated.

## Wednesday's figures, as hers
Re-checked today at this tip: strict `patch -p1 -F0 --dry-run` rc 0, and the file **8/8 green** in her scratch clone. Not my proof; mine is above.



### EVERY COMMIT MESSAGE IN THE CHAIN over 94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812 (oldest first) TEXT_SHA256 4b0c13cce61cd9f89b25e22cb5360805aee7460e7ce90c3f5293f1cd4279613d

--- commit c8233156f0912ec63773e6261cd6926dbce9de7f
KS-1227: pin a hit-only witness in the ks1072 anchor-store cells and clear its listener

Refs KS-1227

Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.

Two edits in one api-gateway test file, in place, no product change:
- postTier2's anchor-store listener is detached in a finally, so a status red still
  reaches the detach. Previously an early red left the listener attached.
- Two new cells. R1 pins the counting rule as merged: every stub request counts, so a
  hit-only URL filter in the helper's own listener reds. R2 pins that a status red inside
  postTier2 still detaches, leaving exactly one listener.

R1 pins the counting rule AS MERGED; the keep-vs-filter decision stays open on the ticket.

My own measurements, not the harness's, at develop 94c9c7aa9be7:
- strict apply, no recount and no fuzz; a corrupted hunk count is refused (rc 128)
- RED under a product tamper at api-gateway routes/verification.ts:585: 1 failed / 7 passed
  of 8, and the one failure is R1 on its assertion
- GREEN at head: 8 of 8
- api-gateway bare 82 files / 754 tests, patched 82 / 756, 0 new reds
- packages/shared 48 files / 945 tests, rc 0
- tsc over a program proven to contain the test file: 29 pre-existing errors, the same SET
  at both trees, 0 naming this file
- api-gateway lint at both trees: 36 problems, 0 errors, 0 in this file



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1227-c8233156f091-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1227-c8233156f091-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-27T06:59:50Z PUSH START",
 "end": "2026-09-27T07:08:07Z push rc=0"
}
```

## #1305 KS-1090 (Seat B 34th (local-model patch, TEST-ONLY: a NEW api-gateway cell, renamed at raise; R2-3, Refs not Closes), T2) — head 7aab743e13f45d10a43650e07f25abffccb6441e

#1305 ticket line: #1305 is KS-1090.

### PR BODY (gh_body_1305.md) TEXT_SHA256 2fed606ecc1f7e4f7476039b494c275af9cb399c3a4f1cfb75d623a4895a7700

#1305 KS-1090 R2-3: type-check the api-gateway wiring test the tsc program never saw
head 7aab743e13f45d10a43650e07f25abffccb6441e

Refs KS-1090

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run; the harness's figures are quoted as the harness's at the end.

## What changes

**One NEW api-gateway test file. No product change.**

The merged mint-scope test pins **two** of the eighteen service keys that must never receive the gateway vouch header — it checks analytics and auth only — so an allow-list widening that spares those two keys stays green. The new cells drive the **real** `createProxyRoutes` with every service pointed at one local recorder and pin, for each non-originate key, that no vouch arrives. A control cell proves originate **does** receive it, and that the factory reads exactly the eighteen service keys the file lists.

**Renamed at raise**, per the READY's own note: the builder's filename described the ticket's *other* half (the tsc-excludes-tests shape), which this change does not address. The rename is a rename — content byte-identical, sha256 `d67ae63b95d27b13…` before and after.

**Not covered, stated rather than implied.** This is R2-3 only, so it is `Refs`, not a close: the tsconfig half (R2-2) and the record (R2-4) stay open on the ticket. The cells pin *that* no vouch arrives for the sixteen non-originate keys; they do not pin the header's value for originate beyond the control's equality check.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**A defect in the READY, found and measured before applying.** Its closing code fence is **glued onto the diff's last `+` line** (`+});` immediately followed by three backticks) with no fence line after it. Taken as-is the committed file ends in stray backticks and vitest fails to **transform** it — a load failure, not a red. Stripped, and proven to be the only change: a full `diff` of the READY's raw block against what I applied is **exactly two lines** — `< +});```` / `> +});`. Nothing else differs.

**Apply.** Strict `git apply`, **no `--recount`, no fuzz**: 1 file, **+96**. Paired with a control that must fail — a **new file cannot be controlled by a path tamper** (a new file applies at any path, so that control passes and proves nothing), so the hunk line count is corrupted instead (`@@ -0,0 +1,96` -> `+1,999`): **refused, rc 128, "corrupt patch at line 100"**. So the rc 0 on the real section is a measurement.

**RED — a product tamper, since this change is test-only.** Tampered `services/api-gateway/src/routes/proxy.ts:275` in my worktree only, the anchor asserted to occur **exactly once in that file** first (and exactly once repo-wide at this tip), sha256 before/after proving it landed — the vouch condition widened to every key the old cells do not name:

- **2 failed / 2 passed of 4**, and the two failures are **both declared cells**, each on its **assertion**, not a crash: `AssertionError: expected [ [ '/api/anchoring/p1', true ], …(7) ] to deeply equal [ Array(8) ]` and the same shape for the second cell's seven keys.
- **Restored by content and verified against the tip blob** — on-disk sha256 `0968c155431e6f3b…` equals `git show <tip>:<path>`; 0 `TAMPER` markers remain.

**GREEN at my head.** The new file alone: **4 of 4 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` **built**, which these tests need):

| | files | tests |
|---|---|---|
| bare (file moved aside, not deleted) | 82 | **754** |
| patched (my head) | 83 | **758** |

**0 new reds**; +1 file and +4 tests are exactly this file. The bare run was taken with the file **absent, asserted absent** before the run, then moved back and its sha256 re-checked.

**`packages/shared`** (its guard suites read service sources by text, and this adds one): **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the new file.** This package's own `tsc --noEmit` says nothing about it: `tsconfig.json` excludes `src/__tests__`, so its program is 491 files with **zero** test files. Measured instead on a config extending it with `exclude: []`, whose program is **619 files including 83 test files, this one present exactly once**: **29 errors, the SET byte-identical to the tip's 29**, and **0 naming this file**.

**Lint, the package's own script.** `npm run lint` (`eslint src`) is **rc 0, 36 problems, 0 errors, 36 warnings** — unchanged from the tip, measured in the same worktree family. eslint is proven to cover `src/__tests__` by a planted-`debugger` control run on this package earlier in this session (it reported `no-debugger` as an **error** inside a test file, rc 1).

**Gate lines: only what THIS push printed.** This push touches a `Blockchain/Dev/` path, so the platform preflight ran. Parsed per suite block by exact basename (the three names are prefixes of one another, so one combined count loses a figure):

```
pre_push_hook_base.test.sh                 28 passed, 0 failed
pre_push_hook_base_fixture_guard.test.sh    6 passed, 0 failed
run_shell_suites.test.sh                   49 passed, 0 failed
shell suites: 60 passed, 0 failed, 0 skipped (of 60)
OK - 13 code guards passed.
PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.
lines starting FIXTURE BUILD FAILED: 0
```

Legs 3, 4 and 8 did not run: no local stack is up. Push rc 0, and `ls-remote` after the push confirms the branch at this head.

**Environment, because a figure carries it:** worktree `s-b34-ks1090`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev`, `packages/shared` **built**. The machine carried a load average of ~40 on 28 cores throughout from an unrelated volume copy and Spotlight reindexing; timings are inflated, no verdict changed.

## Wednesday's figures, as hers
Re-checked today at this tip: strict `patch -p1 -F0 --dry-run` rc 0 **after stripping the glued fence**, and **4/4 green** in her scratch clone. Not my proof; mine is above.



### EVERY COMMIT MESSAGE IN THE CHAIN over 94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812 (oldest first) TEXT_SHA256 15af9ca491242fe86a3ad838e8f4f53d1b18b2a9a88fa6bbf0e59e3a777dc5f8

--- commit 7aab743e13f45d10a43650e07f25abffccb6441e
KS-1090 R2-3: type-check the api-gateway wiring test the tsc program never saw

Refs KS-1090

Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.

One NEW api-gateway test file, no product change. The merged mint-scope test pins only two
of the eighteen service keys that must never receive the gateway vouch header, so an
allow-list widening that spares those two stays green. The new cells drive the real
createProxyRoutes with every service pointed at one local recorder and pin, for each
non-originate key, that no vouch arrives. A control proves originate does receive it and
that the factory reads exactly the eighteen keys listed.

Renamed from the builder's filename, which described the ticket's other half.

My own measurements at develop 94c9c7aa9be7:
- the READY's closing code fence is glued to its last + line; stripped, and the only
  difference between the READY's raw block and what I applied is those three backticks
- strict apply, no recount and no fuzz; a corrupted hunk count is refused rc 128
- RED under a product tamper at api-gateway routes/proxy.ts:275: 2 failed / 2 passed of 4,
  both failures being the two declared cells on their assertions
- GREEN at head: 4 of 4
- api-gateway bare 82 files / 754 tests, patched 83 / 758, 0 new reds
- packages/shared 48 files / 945 tests, rc 0
- tsc over a program proven to contain the new file: 29 pre-existing errors, the same SET
  as the tip, 0 naming this file
- api-gateway lint: rc 0, 36 problems, 0 errors, unchanged from the tip



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1090-7aab743e13f4-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1090-7aab743e13f4-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-27T07:15:17Z PUSH START",
 "end": "2026-09-27T07:22:43Z push rc=0"
}
```

## #1306 KS-1205 (Seat B 34th (local-model patch, TEST-ONLY on an AUTH surface: a NEW api-gateway cell; F3), T2) — head 00180ad72bffdcf917d618b54557a4df90f510c8

#1306 ticket line: #1306 is KS-1205.

### PR BODY (gh_body_1306.md) TEXT_SHA256 f1c41d36bb4a51455cb0ac1f2bfecd511c3fa7b441f72e5b646c036e30f5860c

#1306 KS-1205 F3: pin that a JWT claim cannot name another key's rate-limit bucket
head 00180ad72bffdcf917d618b54557a4df90f510c8

Refs KS-1205

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run.

## What changes

**One NEW api-gateway test file. No product change.**

The per-key rate limiter counts an API key under `api_key:` plus a **domained** sha256 of the key. **Nothing pinned the domain**, so a bucket built from the *bare* sha256 of the key — the same value the security service stores as `key_hash` — left the whole suite green. The cells read the bucket the **real** `authenticateToken` puts on `req.user` for two distinct keys, and assert it is not the bare hash.

**Not covered, stated rather than implied.** This is F-3 (`G-BUCKET-HASH`) only, so it is `Refs`, not a close. The cells read `req.user.rateLimitBucket`, **not Redis keys**: a tamper inside `rateLimitEnforce.ts` would not red them, which the brief states and this PR repeats. The file keeps the builder's name — unlike two of its siblings, this READY asks for no rename.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**The READY's glued closing fence**, the same defect as its siblings: the fence sits on the diff's last `+` line with no fence line after it, so taken as-is the file ends in stray backticks and vitest fails to **transform** it — a load failure, not a red. Stripped, and the only difference between the READY's raw block and what I applied is those three backticks.

**Apply.** Strict `git apply`, **no `--recount`, no fuzz**: 1 file, **+77**. **Control:** a new file cannot be controlled by a path tamper (it applies at any path), so the hunk line count is corrupted instead — **refused, rc 128**.

**The tamper line MOVED, and I re-located it rather than trusting either figure.** The READY names `middleware/auth.ts:300`; its own note predicted `:304` *if* the optional-API-key follow-up merged first — **and that did merge**. Measured at this tip, the `rateLimitBucket` assignment is at **`:313`**, and `rateLimitBucket` occurs in that file exactly twice: the optional type field at `:54` and this one. The anchor was asserted to occur **exactly once** before planting, with sha256 before and after proving the tamper landed.

**RED under that tamper** — the bucket rebuilt from the bare sha256:

- **1 failed / 2 passed of 3**, and the single failure is the **declared cell, on its assertion**: `AssertionError: expected '200 api_key:b28a76e0bb3f5dc02857f7188…' not to be '200 api_key:b28a76e0bb3f5dc02857f7188…' // Object.is equality` — i.e. the bucket became exactly the bare hash the cell forbids.
- **Restored by content and verified against the base blob** — on-disk sha256 `9abef1c21164bbbc…` equals `git show <base>:<path>`; 0 `TAMPER` markers remain.

**GREEN at my head.** The new file alone: **3 of 3 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` **built**, which these tests need):

| | files | tests |
|---|---|---|
| bare (file moved aside, asserted absent) | 82 | **754** |
| patched (my head) | 83 | **757** |

**0 new reds**; +1 file and +3 tests are exactly this file. The file was moved aside, not deleted, and moved back with its sha256 re-checked.

**`packages/shared`**: **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the new file.** The package's own `tsc --noEmit` covers **491 files with zero test files** (`tsconfig.json` excludes `src/__tests__`), so its rc 0 says nothing about this cell. On a config extending it with `exclude: []` the program is **619 files including 83 test files, this one present exactly once**: **29 errors, the SET byte-identical to the base's 29**, and **0 naming this file**.

**Lint.** `npm run lint` (`eslint src`): **rc 0, 36 problems, 0 errors** — unchanged from the base. eslint is proven to cover `src/__tests__` by a planted-`debugger` control run on this package earlier in this session (reported as an **error** inside a test file, rc 1).

**Environment, because a figure carries it:** worktree `s-b34-ks1205`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev`, `packages/shared` **built**. This PR's base is `94c9c7aa`; develop has since moved, and develop has **not** been merged into this branch.

**Gate lines: only what THIS push printed.** This push touches a `Blockchain/Dev/` path, so the platform preflight ran. Parsed per suite block by exact basename:

```
pre_push_hook_base.test.sh                 28 passed, 0 failed
pre_push_hook_base_fixture_guard.test.sh    6 passed, 0 failed
run_shell_suites.test.sh                   49 passed, 0 failed
shell suites: 60 passed, 0 failed, 0 skipped (of 60)
OK - 13 code guards passed.
PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.
lines starting FIXTURE BUILD FAILED: 0
```

Legs 3, 4 and 8 did not run: no local stack is up. Push rc 0, and `ls-remote` after the push confirms the branch at this head.

## Wednesday's figures, as hers
Re-checked today at this tip: strict `patch -p1 -F0 --dry-run` rc 0 after the fence strip, and **3/3 green** in her scratch clone. Not my proof; mine is above.



### EVERY COMMIT MESSAGE IN THE CHAIN over 94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812 (oldest first) TEXT_SHA256 0cea7b510bd0df1d5a8b415bbab995e0522c610381b0972b82299f14e085e0e9

--- commit 00180ad72bffdcf917d618b54557a4df90f510c8
KS-1205 F3: pin that a JWT claim cannot name another key's rate-limit bucket

Refs KS-1205

Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.

One NEW api-gateway test file, no product change. The per-key limiter counts an API key
under api_key plus a DOMAINED sha256 of the key. Nothing pinned the domain, so a bucket
built from the bare sha256 - the same value the security service stores as key_hash - left
the whole suite green. The cells read the bucket the real authenticateToken puts on req.user
for two keys.

My own measurements at develop 94c9c7aa9be7:
- the READY's closing code fence was glued to its last + line; stripped, and the only
  difference from the READY's raw block is those three backticks
- strict apply, no recount and no fuzz; a corrupted hunk count is refused rc 128
- the tamper line MOVED and was re-located rather than trusted: the READY names :300, its
  own note predicted :304 if the optional-key follow-up merged, and it did; at this tip the
  bucket line is :313. Anchor asserted to occur exactly once before planting.
- RED under that tamper: 1 failed / 2 passed of 3, the single failure being the declared
  cell on its assertion
- GREEN at head: 3 of 3
- api-gateway bare 82 files / 754 tests, patched 83 / 757, 0 new reds
- packages/shared 48 files / 945 tests, rc 0
- tsc over a program proven to contain the new file: 29 pre-existing errors, the same SET
  as the base, 0 naming this file
- api-gateway lint rc 0, 36 problems, 0 errors, unchanged from the base



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1205-00180ad72bff-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1205-00180ad72bff-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-27T08:13:35Z PUSH START",
 "end": "2026-09-27T08:20:22Z push rc=0"
}
```

## #1307 KS-1212 (Seat B 34th (local-model patch, TEST-ONLY: a NEW api-gateway cell, renamed at raise), T2) — head 64d8e398599687b53520bc3710cae6869bdc6b8f

#1307 ticket line: #1307 is KS-1212.

### PR BODY (gh_body_1307.md) TEXT_SHA256 520d1fc941003733351380755f9ed450440ff7ffae1ef23054c3ccb534c139d8

#1307 KS-1212: pin that the erasure door reads its own router's caseSensitive option
head 64d8e398599687b53520bc3710cae6869bdc6b8f

Refs KS-1212

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run.

## What changes

**One NEW api-gateway test file. No product change.**

The gdpr erasure door compares the canonical path using the case rule of **its own** router, `erasureDoor`. The merged cell from the earlier round makes **every** Router the factory builds case sensitive at once, so it cannot tell the door router from the factory router — and a product that reads the *factory* router's option stays green under it. The new cells build the **real** `createProxyRoutes` twice through a Router seam that makes exactly **one** of the two routers case sensitive: first the door router, then the factory router. The door must follow its own either way. A control cell pins that the factory makes exactly two `Router()` calls, so the seam cannot silently target the wrong one.

**Renamed at raise** per the READY's note — the builder's filename named the parent ticket rather than this behaviour. The rename is a rename: content sha256 `15d5dc0ee6f32ccd…` before and after.

**Not covered, stated rather than implied.** `Refs`, not a close: the cells pin the door's *source* of the case rule, not the full canonicalisation behaviour, and not the other doors in the same factory. The Router seam is a test seam; nothing about the product's own Router construction is changed.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**The READY's glued closing fence**, as with its siblings: the fence sits on the diff's last `+` line with no fence line after it, so taken as-is the committed file ends in stray backticks and vitest fails to **transform** it — a load failure, not a red. Stripped, and the only difference between the READY's raw block and what I applied is those three backticks.

**Apply.** Strict `git apply`, **no `--recount`, no fuzz**: 1 file, **+134**. **Control:** a new file cannot be controlled by a path tamper (it applies at any path), so the hunk line count is corrupted instead — **refused, rc 128**.

**The tamper line had MOVED, and I re-located it rather than trusting the brief.** The brief names `routes/proxy.ts:808`, read at an older tip; at this base the declaration is at **`:814`**, and `erasureDoorCaseSensitive` appears in that file exactly twice — the declaration and its single read at `:817`. The anchor was asserted to occur **exactly once** before planting, with sha256 before and after proving it landed.

**RED under that tamper** — the door reads the *factory* router's option instead of its own:

- **2 failed / 2 passed of 4**, and both failures are the **two declared cells, each on its assertion**, not a crash:
  - `AssertionError: expected [ 400, 'NON_CANONICAL_PATH', [] ] to deeply equal [ 200, null, …(1) ]`
  - `AssertionError: expected [ 200, null, …(1) ] to deeply equal [ 400, 'NON_CANONICAL_PATH', [] ]`
- **The two assertions are mirror images of each other, and that is the point:** with the door case sensitive and the factory default the request must be forwarded; with the factory case sensitive and the door default it must be refused. A product reading the wrong router gets exactly one of those backwards in each direction, so a single cell could not have caught it.
- **Restored by content and verified against the base blob** — on-disk sha256 `0968c155431e6f3b…` equals `git show <base>:<path>`; 0 `TAMPER` markers remain.

**GREEN at my head.** The new file alone: **4 of 4 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` **built**, which these tests need):

| | files | tests |
|---|---|---|
| bare (file moved aside, asserted absent) | 82 | **754** |
| patched (my head) | 83 | **758** |

**0 new reds**; +1 file and +4 tests are exactly this file. Moved aside rather than deleted, moved back with its sha256 re-checked.

**`packages/shared`**: **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the new file.** This package's own `tsc --noEmit` covers 491 files with **zero** test files (`tsconfig.json` excludes `src/__tests__`), so its rc 0 says nothing about this cell. On a config extending it with `exclude: []` the program is **619 files including 83 test files, this one present exactly once**: **29 errors, the SET byte-identical to the base's 29**, and **0 naming this file**.

**Lint.** `npm run lint` (`eslint src`): **rc 0, 36 problems, 0 errors** — unchanged from the base. eslint is proven to cover `src/__tests__` by a planted-`debugger` control run on this package earlier in this session (reported as an **error** inside a test file, rc 1).

**Environment, because a figure carries it:** worktree `s-b34-ks1212`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev`, `packages/shared` **built**. This PR's base is `94c9c7aa`; develop has since moved and has **not** been merged into this branch.

**Gate lines: only what THIS push printed.** This push touches a `Blockchain/Dev/` path, so the platform preflight ran. Parsed per suite block by exact basename:

```
pre_push_hook_base.test.sh                 28 passed, 0 failed
pre_push_hook_base_fixture_guard.test.sh    6 passed, 0 failed
run_shell_suites.test.sh                   49 passed, 0 failed
shell suites: 60 passed, 0 failed, 0 skipped (of 60)
OK - 13 code guards passed.
PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.
lines starting FIXTURE BUILD FAILED: 0
```

Legs 3, 4 and 8 did not run: no local stack is up. Push rc 0, and `ls-remote` after the push confirms the branch at this head.

## Wednesday's figures, as hers
Re-checked today at this tip: strict `patch -p1 -F0 --dry-run` rc 0 after the fence strip, and **4/4 green** in her scratch clone. Not my proof; mine is above.



### EVERY COMMIT MESSAGE IN THE CHAIN over 94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812 (oldest first) TEXT_SHA256 9e8e5e6d067a4eda369fa0a567db1531da65c19701553277811e3601c488b280

--- commit 64d8e398599687b53520bc3710cae6869bdc6b8f
KS-1212: pin that the erasure door reads its own router's caseSensitive option

Refs KS-1212

Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.

One NEW api-gateway test file, no product change. The gdpr erasure door compares the
canonical path with the case rule of its OWN router. The merged cell makes every Router the
factory builds case sensitive at once, so it cannot tell the door router from the factory
router, and a read of the factory router's option stays green. The new cells build the REAL
createProxyRoutes twice through a Router seam that makes exactly one of the two routers case
sensitive - first the door, then the factory - and pin that the door follows its own.

Renamed at raise per the READY's note.

My own measurements at develop 94c9c7aa9be7:
- the READY's closing code fence was glued to its last + line; stripped, and the only
  difference from the raw block is those three backticks
- strict apply, no recount and no fuzz; a corrupted hunk count is refused rc 128
- the tamper line had MOVED and was re-located rather than trusted: the brief names :808 at
  an older tip; at this base it is :814. Anchor asserted to occur exactly once before planting.
- RED under that tamper: 2 failed / 2 passed of 4, both failures being the two declared cells
  on their assertions, and the two assertions are mirror images of each other - which is the
  point, since the door must follow its own router either way
- GREEN at head: 4 of 4
- api-gateway bare 82 files / 754 tests, patched 83 / 758, 0 new reds
- packages/shared 48 files / 945 tests, rc 0
- tsc over a program proven to contain the new file: 29 pre-existing errors, the same SET as
  the base, 0 naming this file
- api-gateway lint rc 0, 36 problems, 0 errors, unchanged



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1212-64d8e3985996-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1212-64d8e3985996-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-27T09:25:34Z PUSH START",
 "end": "2026-09-27T09:32:25Z push rc=0"
}
```

## #1308 KS-1108 (Seat B 34th (local-model patch, TOOLING: systemTest/akto secrets.ts + a NEW akto unit cell carrying a RULED, disclosed 16-line lint departure), T2) — head f9348a9d10b7512d22a33a0a471f9042ad622831

#1308 ticket line: #1308 is KS-1108.

### PR BODY (gh_body_1308.md) TEXT_SHA256 fafbdc0f37380f3509ddd84dcb458ab39d194949d2b85ed0a64b35b63ccecde6

#1308 KS-1108: name the file and position when akto's secrets.yml will not parse
head f9348a9d10b7512d22a33a0a471f9042ad622831

Refs KS-1108

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run.

## What changes

`systemTest/akto`'s `loadSecretsYml` parsed `config/secrets.yml` with **no catch**. A malformed file therefore threw js-yaml's own `YAMLException`, which carries **the whole file in `mark.buffer`** and, for a bare tag or anchor value, **the value itself in `reason`**. Any uncaught print showed every credential in the file.

The parse is now wrapped. On failure it throws an `Error` naming **only the file and the position** — never the reason, the message, the mark, or a cause. Plus a new akto unit cell that plants a secret-shaped sentinel in a malformed file and asserts the thrown error does not carry it, with a control that a valid file still parses.

**Not covered, stated rather than implied.** The cells pin the *thrown* error. They do **not** capture stdout, so a future logger that prints the raw exception elsewhere would not be caught here. Key-suffix matching has limits: the redaction names a position, not a taxonomy of what could leak. `Refs`, not a close.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**The READY's hunk headers are miscounted**, so the brief's recounted copy was used. **Proven equivalent, not assumed:** stripping the `@@` lines from the READY block and from the recount leaves them **identical, 81 lines each**; the two header changes are `-36,7 -> -36,5` and `+1,82 -> +1,58`; a control fires on a one-token mutation. The READY's `-36,7` is **arithmetically wrong** — the hunk body has 4 context + 1 removed = **5** old-side lines. Under GNU `patch -F0` the READY block gives rc 2 (`malformed patch at line 24`) and the recount rc 0; under `git apply --check` the READY-headed section is refused outright.

**Apply.** Strict `git apply`, no `--recount`, no fuzz: **both sections rc 0**. Each with a control that must fail:
- section 1 is an **existing** file, so a **path tamper** is valid: rc 1, `No such file or directory`.
- section 2 is a **new** file, so the **hunk count** is corrupted instead: rc 128.
- **And the reason the path arm would not do for a new file is measured, not quoted: a wrong-path new file still applies, rc 0.** That control would have proven nothing.

**RED — the product hunk WITHHELD** (this item changes product, so no tamper is needed):
- **1 failed / 1 passed of 2**, and the failure is the declared cell **on its assertion**: `AssertionError: expected 'YAMLException: unknown scalar tag !<!…' not to contain 'ks1108-tag-Pw-4c2e91'`. That sentinel is the secret-shaped token the test plants in the file, and at the base the raw exception carries it. **That assertion is the ticket.**
- Restored and verified byte-identical to my head.

**GREEN at my head.** The cell: **2 of 2 passed**.

**Suite, bare vs patched** (`vitest run -c vitest.unit.config.ts`):

| | files | tests |
|---|---|---|
| bare (product reverted, test moved aside) | 70 | **1236** |
| patched (my head) | 71 | **1238** |

**0 new reds.**

**`tsc`.** Unlike the api-gateway packages, **akto's own tsconfig does not exclude its tests** — measured with `--listFilesOnly`: the program is **563 files and this new test is present exactly once**. So no widened program was needed. `tsc --noEmit -p tsconfig.json`: **rc 0, 0 errors**.

**Lint, and a control that actually fires.** `npm run lint` is **rc 0**. ⚠ The planted-`debugger` control used for the api-gateway packages **does not fire here** — `no-debugger` appears **0 times** in akto's `eslint.config.js`, so that plant is the wrong instrument for this package and its silence proved nothing. Replaced with a plant this package demonstrably enforces: **removing one `@param` line gives rc 1, `jsdoc/require-param`**, and restoring it returns rc 0. The zero is proven.

**Gate lines: `fleet STOP: NOT APPLICABLE (format gate only)`.** This push touches **no `Blockchain/Dev/` path**, so the pre-push hook's path filter means the platform preflight **never ran**, and none of the fleet STOP counts apply here. Measured with a control: the tokens `pre_push_hook_base`, `PREFLIGHT INCOMPLETE` and `code guards passed` appear **0, 0 and 0** times in this push's log and **4, 1 and 1** times in a `Blockchain/Dev` push of mine. What did run:

```
[format-gate] systemTest/akto — format:check OK
[format-gate] 1 package(s) checked, 0 skipped, 0 failed
```

Push rc 0; `ls-remote` after the push confirms the branch at this head.

## DISCLOSED DEPARTURE FROM THE LOCAL MODEL'S OUTPUT

**The new test file differs from the model's output by 16 lines: 12 of JSDoc and 4 of one wrapped call.** It is required by `systemTest/akto`'s **own** lint, which the model's output failed with **5 errors** (`jsdoc/require-param` ×2, `jsdoc/require-returns` ×2, `prettier/prettier` ×1) while `tsc` was green — `tsc` green is not lint green.

**`eslint --fix` could not fix it, and made it worse: 5 errors became 6.** It scaffolds a bare `@param fn` line, which then trips `jsdoc/require-param-type` and `jsdoc/require-param-description`, rules it cannot invent values for. So the JSDoc was hand-written with types and descriptions on the two **test-local** helpers (`thrownBy`, `writeSecrets`).

Classified line by line, the 16 changes are **12 JSDoc, 4 prettier-wrap, 0 other** — documentation and formatting only. The whole akto suite reads **71 files / 1238 tests** both with the model's bytes and with the committed version, so no behaviour changed. **The product hunk in `src/config/secrets.ts` is byte-identical to the recount** (its `+`/`-` line sequence compared directly: 15 lines, identical).

A candidate follow-up, not taken here and not mine to decide: whether akto's `jsdoc/require-*` rules should apply to test files at all. Nothing in `eslint.config.js` was touched.

## Wednesday's figures, as hers
Re-checked today at this tip in her scratch clone: the test file alone **1 failed / 1 passed**, with the product hunk **2 passed**, and the whole akto unit suite **71 files / 1238 tests**. Not my proof; mine is above.



### EVERY COMMIT MESSAGE IN THE CHAIN over 94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812 (oldest first) TEXT_SHA256 424d4d6713dc69a3e81dcd8f569932003b0adec0cb6f7a242bbec7cfb13a39ea

--- commit f9348a9d10b7512d22a33a0a471f9042ad622831
KS-1108: name the file and position when akto's secrets.yml will not parse

Refs KS-1108

Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.

systemTest/akto's loadSecretsYml parsed config/secrets.yml with no catch, so a malformed
file threw js-yaml's own YAMLException - which carries the whole file in mark.buffer and,
for a bare tag or anchor value, the value itself in reason. An uncaught print showed every
credential. The parse is now wrapped and throws an Error naming only the file and the
position, never the reason, the message, the mark or a cause.

My own measurements at develop 94c9c7aa9be7:
- the READY's hunk headers are MISCOUNTED, so the brief's recounted copy was used. Proven
  equivalent: stripping the @@ lines from both leaves them identical, 81 lines each. The
  READY's -36,7 is arithmetically wrong; the body has 4 context + 1 removed = 5.
- strict apply of both sections rc 0, each with a control that fires: a path tamper for the
  existing file (rc 1), a corrupted hunk count for the new file (rc 128). A path tamper was
  measured NOT to control a new file: a wrong-path new file still applies rc 0.
- RED with the product hunk withheld: 1 failed / 1 passed of 2, the failure being the
  declared cell on its assertion - the raw exception carries the planted sentinel
- GREEN at head: 2 of 2
- akto unit suite bare 70 files / 1236 tests, patched 71 / 1238, 0 new reds
- tsc over the package's own program, which contains the new test: rc 0, 0 errors
- akto lint rc 0, with a control that fires (removing one @param gives rc 1)

The new test file differs from the local model's output by 16 lines - 12 of JSDoc and 4 of
one wrapped call - required by systemTest/akto's own lint, which the model's output failed
with 5 errors. eslint --fix could not satisfy jsdoc/require-param-type or
require-param-description; it produced 6 errors. The product hunk is byte-identical to the
recount. Ruled and disclosed.



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1108r2-f9348a9d10b7-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1108r2-f9348a9d10b7-push.out",
 "lines": 11,
 "pre_push_hook_base": "NOT FOUND",
 "fixture_guard": "NOT FOUND",
 "run_shell_suites_region": "NOT FOUND",
 "run_shell_suites_prefixed": "NOT FOUND",
 "shell_suites": "NOT FOUND",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "NONE",
 "preflight_ran": false,
 "rc": "0",
 "start": "2026-09-27T09:45:53Z PUSH START",
 "end": "2026-09-27T09:46:00Z push rc=0"
}
```

## #1309 KS-1196 (Seat B 34th (local-model patch, PRODUCT: api-gateway routes/admin.ts document-type ids to crypto.randomUUID + a NEW cell; the diff REGENERATED by Wednesday), T2) — head f615d12d58d95b01b98816644334cfd06832252d

#1309 ticket line: #1309 is KS-1196.

### PR BODY (gh_body_1309.md) TEXT_SHA256 8bc9fe0e4224c96eb64f14a8e85d494867b98f91c9186e3e06aa56437accda1d

#1309 KS-1196: make admin document-type ids collision-proof with randomUUID
head f615d12d58d95b01b98816644334cfd06832252d

Refs KS-1196

**Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.** Every number under "My measurements" I measured in this run.

## What changes

`POST /api/admin/document-types` built the new id as `` `dt-${Date.now()}` `` — **from the clock alone**. Two creates in the same millisecond therefore got the **same id**, both answered 201, and the second **silently overwrote the first** in the catalogue. The id now comes from `crypto.randomUUID()`.

**One product line**, plus a new api-gateway test that drives the real admin router with the clock pinned, creates two types in the same millisecond, and pins both that the ids differ and that both types survive in the catalogue.

**Not covered, stated rather than implied.** `Refs`, not a close. Whether any caller **sorts by id** is unmeasured — a time-ordered id is no longer monotonic, and nothing here establishes that no consumer relied on that. A side finding read from the handler but not addressed: it stores `{ id, ...body }`, so a body-supplied `id` would diverge from its catalogue key.

## My measurements, at develop `94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812`

**The READY's own diff does not apply strict at this tip**, so the brief's regenerated diff was used. **Both of its claims were proven before applying, not taken on trust:**

1. **The `+`/`-` line sequences are identical, in order** — 119 lines on each side. Compared with `l and l[0] in '+-'`, never `l[:1] in '+-'`: the empty string is "in" every string, so the short form counts a trailing blank line as a change. Controls: an identical pair reads IDENTICAL, and a one-token mutation reads DIFFER.
2. **The regenerated diff applies strict** `git apply --check` **rc 0, where the READY block FAILS** — `error: patch failed: …/routes/admin.ts:679`. Its sha256 matches the brief's declared prefix `2c17773c8f2f03e1`.

⚠ **One stated figure disagreed with my measurement and the brief's author confirmed mine.** The brief declared the regenerated diff as **+109 / −1**; I measure **+118 / −1** excluding the `+++`/`---` headers (`admin.ts` +1/−1, the new test +117/−0). Cause, confirmed: the brief's count used `grep '^+[^+]'`, which cannot match an added **empty** line, so it missed the 9 blank lines in the new test. The diff itself was always right.

**Apply.** Strict `git apply`, no `--recount`, no fuzz: **both sections rc 0**. The tool also asserts that the bytes it split are the bytes it verified — `split-source CONFIRMED == KS-1196.regenerated-at-94c9c7aa.diff (5070 B, sha256 2c17773c8f2f03e1)`.

**RED — the product line WITHHELD** (this item changes product, so no tamper is needed):

- **2 failed / 2 passed of 4**, and both failures are the **two declared cells, each on its assertion**:
  - `AssertionError: expected 'dt-1758000000000' not to be 'dt-1758000000000' // Object.is equality` — the two creates returned the identical id.
  - `AssertionError: expected [ 'Beta Type' ] to deeply equal [ 'Alpha Type', 'Beta Type' ]` — the catalogue kept only the second.
- **Those two assertions are the ticket**: the collision and the silent loss, each pinned separately.
- Restored and verified byte-identical to my head.

**GREEN at my head.** The new file alone: **4 of 4 passed**.

**Suite, bare vs patched** (api-gateway is vitest; `packages/shared` **built**):

| | files | tests |
|---|---|---|
| bare (both hunks withheld) | 82 | **754** |
| patched (my head) | 83 | **758** |

**0 new reds**; +1 file and +4 tests are exactly this change.

**`packages/shared`**: **48 files / 945 tests passed**, rc 0.

**`tsc`, over a program PROVEN to contain the new file.** The package's own program is 491 files with **zero** test files, so its rc 0 says nothing here. On a config extending it with `exclude: []`: **619 files, 83 test files, this one present exactly once** — **29 errors, the SET byte-identical to the base's 29**, **0 naming this file**.

**Lint, with a control that fires.** `npm run lint` **rc 0, 36 problems, 0 errors** — unchanged from the base. Control: a planted `debugger` gives **rc 1, `no-debugger` error at 117:3 in this file**, so eslint does cover it.

⚠ **Disclosed, because it cost me a restore:** after that lint control I reverted with a copy I could not vouch for and the file came back at the **wrong** sha. I caught it by comparing blob ids, moved the untrusted copy to quarantine rather than deleting it, and **re-created the file from the section diff**, which is the authoritative source. The tree was then verified line-for-line against the regenerated diff — product `+`/`-` identical, new file 117 lines identical, zero `debugger` occurrences — and **the cell and lint were both re-run on the restored tree**, so no figure in this PR rests on the control run.

**Gate lines: only what THIS push printed.** This push touches `Blockchain/Dev/` paths, so the platform preflight ran:

```
pre_push_hook_base.test.sh                 28 passed, 0 failed
pre_push_hook_base_fixture_guard.test.sh    6 passed, 0 failed
run_shell_suites.test.sh                   49 passed, 0 failed
shell suites: 60 passed, 0 failed, 0 skipped (of 60)
OK - 13 code guards passed.
PREFLIGHT INCOMPLETE - 12/15 legs ran, 3 SKIPPED. Nothing failed.
lines starting FIXTURE BUILD FAILED: 0
```

Legs 3, 4 and 8 did not run: no local stack. Push rc 0; `ls-remote` after the push confirms the branch at this head.

**Environment:** worktree `s-b34-ks1196`, detached from `94c9c7aa9be7` (`merge-base --is-ancestor` holds), `npm ci` in `Blockchain/Dev`, `packages/shared` **built**. This PR's base is `94c9c7aa`; develop has since moved and has **not** been merged into this branch.

## Wednesday's figures, as hers
In her scratch clone at this tip: the test file alone **2 failed / 2 passed**, with the product line **4 passed**, api-gateway **83 files / 758 tests**. Not my proof; mine is above and agrees.



### EVERY COMMIT MESSAGE IN THE CHAIN over 94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812 (oldest first) TEXT_SHA256 a366903a941787ffc904f11486d8ce22379034fff0f2307dfbd857e908dfe0b7

--- commit f615d12d58d95b01b98816644334cfd06832252d
KS-1196: make admin document-type ids collision-proof with randomUUID

Refs KS-1196

Patch produced by the local model (Ornith) under a Wednesday brief, re-verified by this seat.

POST /api/admin/document-types built the new id from the clock alone, so two creates in the
same millisecond got the SAME id, both answered 201, and the second silently overwrote the
first in the catalogue. The id now comes from crypto.randomUUID(). One product line plus a
new api-gateway test.

My own measurements at develop 94c9c7aa9be7:
- the READY's diff does not apply strict at this tip, so the brief's regenerated diff was
  used. Both of its claims proven first: the +/- line sequences are identical in order (119
  lines, with controls that fire on an identical pair and on a one-token mutation), and the
  regenerated diff applies strict git apply --check rc 0 where the READY block fails at
  admin.ts:679.
- strict apply of both sections rc 0
- RED with the product line withheld: 2 failed / 2 passed of 4, both failures being the two
  declared cells on their assertions - two creates one millisecond apart returned the
  identical id dt-1758000000000, and the catalogue held only the second type
- GREEN at head: 4 of 4
- api-gateway bare 82 files / 754 tests, patched 83 / 758, 0 new reds
- packages/shared 48 files / 945 tests, rc 0
- tsc over a program proven to contain the new file: 29 pre-existing errors, the same SET as
  the base, 0 naming this file
- api-gateway lint rc 0, 36 problems, 0 errors, with a planted-debugger control that fires



### PUSH LOG STOP COUNTS (READ, bounded region; /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1196-f615d12d58d9-push.out)

```
{
 "log": "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/s-b34-ks1196-f615d12d58d9-push.out",
 "lines": 1305,
 "pre_push_hook_base": "28/0",
 "fixture_guard": "6/0",
 "run_shell_suites_region": "49/0",
 "run_shell_suites_prefixed": "49/0",
 "shell_suites": "60 passed, 0 failed, 0 skipped (of 60)",
 "CONTROL_absent_header": "NOT FOUND",
 "fixture_build_failed_lines": 0,
 "verdict_line": "PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.",
 "preflight_ran": true,
 "rc": "0",
 "start": "2026-09-27T11:11:13Z PUSH START",
 "end": "2026-09-27T11:18:30Z push rc=0"
}
```

## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i1-RED.out TEXT_SHA256 5510722809b0952fdcdec075e6b4926ee60b1bae5d40f106f5280d982717a03b


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1227/Blockchain/Dev/services/api-gateway

 ❯ src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts (8 tests | 1 failed) 1978ms
     × KS-1227 R1 - a second request reaching the stub anchor store reds the postTier2 witness even though tier 2 answered 10ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts > KS-1072 — latest-anchor selector confirmedAt tiebreak > KS-1227 R1 - a second request reaching the stub anchor store reds the postTier2 witness even though tier 2 answered
AssertionError: expected 'no red' to contain 'KS-1180: tier 2 answered, one anchor-…'

Expected: "KS-1180: tier 2 answered, one anchor-store read of this document"
Received: "no red"

 ❯ src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts:196:23
    194|     try {
    195|       const witness = await postTier2([{ blockNumber: 100, confirmedAt…
    196|       expect(witness).toContain('KS-1180: tier 2 answered, one anchor-…
       |                       ^
    197|     } finally {
    198|       vi.unstubAllEnvs();

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed (1)
      Tests  1 failed | 7 passed (8)
   Start at  16:54:02
   Duration  3.39s (transform 140ms, setup 58ms, import 912ms, tests 1.98s, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i1-GREEN.out TEXT_SHA256 47ac3e39239c8b9326657778a077d4c30afcc953f26dfa7abc69bc75f9f9702a


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1227/Blockchain/Dev/services/api-gateway


 Test Files  1 passed (1)
      Tests  8 passed (8)
   Start at  16:53:28
   Duration  7.74s (transform 84ms, setup 98ms, import 259ms, tests 7.02s, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i1-gw-BARE.out — TAIL (last 6 of 35 lines); the WHOLE file's TEXT_SHA256 c02617e17972d4a3a9612df4c7dc2388dd666ca99fefcc893e2d32e5fe7ee5c1


 Test Files  82 passed (82)
      Tests  754 passed (754)
   Start at  16:55:08
   Duration  7.69s (transform 4.32s, setup 3.73s, import 21.18s, tests 57.01s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i1-gw-PATCHED.out — TAIL (last 6 of 35 lines); the WHOLE file's TEXT_SHA256 3a3d284b51d913a43c8e5988b2bebaa00f53759d5927d7932087f6af50254ac8


 Test Files  82 passed (82)
      Tests  756 passed (756)
   Start at  16:54:41
   Duration  9.33s (transform 5.18s, setup 3.53s, import 28.36s, tests 57.88s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i1-lint-HEAD.out — TAIL (last 8 of 68 lines); the WHOLE file's TEXT_SHA256 9ac74f5584cc991dc1234d8488b2d069c271ca3a02e2620862d22ffe5e048b5f


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1227/Blockchain/Dev/services/api-gateway/src/services/redis.ts
  119:7   warning  There is no `cause` attached to the symptom error being thrown  preserve-caught-error
  731:12  warning  'error' is defined but never used                               @typescript-eslint/no-unused-vars

✖ 36 problems (0 errors, 36 warnings)
  0 errors and 1 warning potentially fixable with the `--fix` option.


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i1-tsc-setdiff.txt TEXT_SHA256 e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i2-RED.out — TAIL (last 40 of 251 lines); the WHOLE file's TEXT_SHA256 d8d62b519334ae04f1d1e06e5a83b31cb1262b1ae965a061823ec48a216a0ef2

+     true,
    ],
    [
      "/api/milestones/p2",
-     false,
+     true,
    ],
    [
      "/api/transfers/p2",
-     false,
+     true,
    ],
    [
      "/api/governance/p2",
-     false,
+     true,
    ],
    [
      "/api/dashboard/p2",
-     false,
+     true,
    ],
    [
      "/billing/p2",
-     false,
+     true,
    ],
  ]

 ❯ src/__tests__/ks1090-vouch-reaches-only-originate.test.ts:86:18


⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯


 Test Files  1 failed (1)
      Tests  2 failed | 2 passed (4)
   Start at  17:13:16
   Duration  420ms (transform 70ms, setup 37ms, import 60ms, tests 233ms, environment 0ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i2-GREEN.out TEXT_SHA256 c31e3f8d51de76da7db771aa0f01353b1d429166c288d07199fab1c435fcaa33


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1090/Blockchain/Dev/services/api-gateway

(node:50660) [DEP0060] DeprecationWarning: The `util._extend` API is deprecated. Please use Object.assign() instead.
(Use `node --trace-deprecation ...` to show where the warning was created)
(node:50660) MaxListenersExceededWarning: Possible EventEmitter memory leak detected. 11 close listeners added to [Server]. MaxListeners is 10. Use emitter.setMaxListeners() to increase limit

 Test Files  1 passed (1)
      Tests  4 passed (4)
   Start at  17:13:14
   Duration  1.99s (transform 171ms, setup 68ms, import 642ms, tests 774ms, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i2-gw-BARE.out — TAIL (last 6 of 35 lines); the WHOLE file's TEXT_SHA256 d40b20f141014a40f1aab17b696e5d5ae43508b650b9b3b8afbf0934be3a92c5


 Test Files  82 passed (82)
      Tests  754 passed (754)
   Start at  17:14:10
   Duration  7.39s (transform 3.09s, setup 3.41s, import 16.03s, tests 50.32s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i2-gw-PATCHED.out — TAIL (last 6 of 38 lines); the WHOLE file's TEXT_SHA256 64728efebb6a1599a0c9f5499a7b8b0c3a1e65fda446910d22b11ceeca4ecf57


 Test Files  83 passed (83)
      Tests  758 passed (758)
   Start at  17:14:00
   Duration  9.10s (transform 5.06s, setup 3.56s, import 19.00s, tests 58.82s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i3-RED.out TEXT_SHA256 90b08e169fedf21951dc2cda0b87d47dbaca1ca672a1f3ff020789084e78dc3b


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1205/Blockchain/Dev/services/api-gateway

stdout | src/__tests__/ks1205-api-gateway-per-key-limiter-follow.test.ts > KS-1205 G-BUCKET-HASH - a key bucket is never the stored key_hash > KS-1205 R1 - neither key is bucketed as api_key plus the bare sha256 of the key
2026-09-27 18:11:47.921 [api-gateway] [33mwarn[39m: [rateLimit] DEGRADED — per-client ceiling is no longer distributed {"reason":"redis-not-ready","clientId":"api_key:b28a76e0bb3f5dc02857f7188d95257c9456735b7c5de7a38fe0251a8d4394b6","effect":"counting per-replica in memory; the effective ceiling inflates to limit × replicas","throttledFor":"30s"}

 ❯ src/__tests__/ks1205-api-gateway-per-key-limiter-follow.test.ts (3 tests | 1 failed) 30ms
     × KS-1205 R1 - neither key is bucketed as api_key plus the bare sha256 of the key 22ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/__tests__/ks1205-api-gateway-per-key-limiter-follow.test.ts > KS-1205 G-BUCKET-HASH - a key bucket is never the stored key_hash > KS-1205 R1 - neither key is bucketed as api_key plus the bare sha256 of the key
AssertionError: expected '200 api_key:b28a76e0bb3f5dc02857f7188…' not to be '200 api_key:b28a76e0bb3f5dc02857f7188…' // Object.is equality
 ❯ src/__tests__/ks1205-api-gateway-per-key-limiter-follow.test.ts:65:19
     63|     const a = await bucketFor(KEY_A);
     64|     const b = await bucketFor(KEY_B);
     65|     expect(a).not.toBe('200 api_key:' + bareHash(KEY_A));
       |                   ^
     66|     expect(b).not.toBe('200 api_key:' + bareHash(KEY_B));
     67|   });

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed (1)
      Tests  1 failed | 2 passed (3)
   Start at  18:11:47
   Duration  377ms (transform 84ms, setup 32ms, import 230ms, tests 30ms, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i3-GREEN.out TEXT_SHA256 46739a8f48905786f4b5da857f5dc58f9c124a26c50c37cb91359ffaa85cf139


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1205/Blockchain/Dev/services/api-gateway


 Test Files  1 passed (1)
      Tests  3 passed (3)
   Start at  18:11:38
   Duration  8.46s (transform 218ms, setup 60ms, import 8.00s, tests 40ms, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i3-gw-BARE.out — TAIL (last 6 of 35 lines); the WHOLE file's TEXT_SHA256 41a5993839687763758e17c182889141cf22b7c70a0b99be824615fb102beecf


 Test Files  82 passed (82)
      Tests  754 passed (754)
   Start at  18:12:23
   Duration  7.55s (transform 3.02s, setup 3.49s, import 15.49s, tests 50.64s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i3-gw-PATCHED.out — TAIL (last 6 of 35 lines); the WHOLE file's TEXT_SHA256 1240216e417eaed2f6b8d1b582b32c86902a2080cc7fc66775a95cc431e4c8f9


 Test Files  83 passed (83)
      Tests  757 passed (757)
   Start at  18:12:13
   Duration  9.34s (transform 5.65s, setup 3.24s, import 20.94s, tests 60.00s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i4-RED.out — TAIL (last 40 of 294 lines); the WHOLE file's TEXT_SHA256 75b2f1b8d7f9ef63add4dc37976173494b47770afa27fb7f4868db6c544a96bd

    119|     expect(await send(doorUrl, '/api/gdpr/ERASURES/..')).toEqual([200,…
       |                                                          ^
    120|   });
    121|   it('KS-1212 R2 - factory router case sensitive, door router default …

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/2]⎯

 FAIL  src/__tests__/ks1212-erasure-door-reads-its-own-router-case-option.test.ts > KS-1212 - the erasure door follows its own router case rule, not the factory router > KS-1212 R2 - factory router case sensitive, door router default - GET /api/gdpr/ERASURES/.. is the door and is refused
AssertionError: expected [ 200, null, …(1) ] to deeply equal [ 400, 'NON_CANONICAL_PATH', [] ]

- Expected
+ Received

  [
-   400,
-   "NON_CANONICAL_PATH",
-   [],
+   200,
+   null,
+   [
+     "GET /api/gdpr/ERASURES/..",
+   ],
  ]

 ❯ src/__tests__/ks1212-erasure-door-reads-its-own-router-case-option.test.ts:123:61
    121|   it('KS-1212 R2 - factory router case sensitive, door router default …
    122|     CELLS_RUN += 1;
    123|     expect(await send(factoryUrl, '/api/gdpr/ERASURES/..')).toEqual([4…
       |                                                             ^
    124|   });
    125|   it('KS-1212 CONTROL - each factory built two routers with only the i…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯


 Test Files  1 failed (1)
      Tests  2 failed | 2 passed (4)
   Start at  19:23:50
   Duration  584ms (transform 74ms, setup 27ms, import 62ms, tests 413ms, environment 0ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i4-GREEN.out TEXT_SHA256 1bfee070d3b3f1edc5c0a095771c7b884544b21c2e0aafb3cb3d4a21caa5282e


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1212/Blockchain/Dev/services/api-gateway

(node:35421) [DEP0060] DeprecationWarning: The `util._extend` API is deprecated. Please use Object.assign() instead.
(Use `node --trace-deprecation ...` to show where the warning was created)

 Test Files  1 passed (1)
      Tests  4 passed (4)
   Start at  19:23:40
   Duration  9.43s (transform 341ms, setup 120ms, import 2.68s, tests 6.27s, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i4-gw-BARE.out — TAIL (last 6 of 35 lines); the WHOLE file's TEXT_SHA256 4eafe126fe654dc648944ca81ecaa00e009fdeb6decbe822bf4f25e92cb21797


 Test Files  82 passed (82)
      Tests  754 passed (754)
   Start at  19:24:24
   Duration  7.63s (transform 3.18s, setup 3.40s, import 16.70s, tests 50.53s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i4-gw-PATCHED.out — TAIL (last 6 of 37 lines); the WHOLE file's TEXT_SHA256 03a6062277e2df02de6a9e7e6385f5c6fecb1c9bed367c866a575ea573426f63


 Test Files  83 passed (83)
      Tests  758 passed (758)
   Start at  19:24:14
   Duration  8.67s (transform 4.49s, setup 3.75s, import 18.59s, tests 53.20s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-RED.out TEXT_SHA256 70f824cea23b5225fc87f81c01eb154f809e5f33b741bbd8a0492a2df0cdc3a4


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto

 ❯ tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts (2 tests | 1 failed) 10ms
     × 🔴 KS-1108 — a malformed secrets.yml throws an error that names the file and position and NOTHING of its content 7ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 1 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts > loadSecretsYml > 🔴 KS-1108 — a malformed secrets.yml throws an error that names the file and position and NOTHING of its content
AssertionError: expected 'YAMLException: unknown scalar tag !<!…' not to contain 'ks1108-tag-Pw-4c2e91'

- Expected
+ Received

- ks1108-tag-Pw-4c2e91
+ YAMLException: unknown scalar tag !<!ks1108-tag-Pw-4c2e91> (1:11)
+
+  1 | password: !ks1108-tag-Pw-4c2e91
+ ---------------^
+     at YAMLException.throwAt (file:///Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/node_modules/js-yaml/dist/js-yaml.mjs:1219:9)
+     at throwError$1 (file:///Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/node_modules/js-yaml/dist/js-yaml.mjs:1499:16)
+     at constructScalar (file:///Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/node_modules/js-yaml/dist/js-yaml.mjs:1537:3)
+     at constructFromEvents (file:///Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/node_modules/js-yaml/dist/js-yaml.mjs:1662:28)
+     at loadDocuments (file:///Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/node_modules/js-yaml/dist/js-yaml.mjs:2591:9)
+     at load (file:///Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/node_modules/js-yaml/dist/js-yaml.mjs:2635:20)
+     at loadSecretsYml (/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/src/config/secrets.ts:40:20)
+     at /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts:44:36
+     at thrownBy (/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts:19:9)
+     at /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts:44:21 {
+   reason: 'unknown scalar tag !<!ks1108-tag-Pw-4c2e91>',
+   mark: {
+     name: '',
+     buffer: 'password: !ks1108-tag-Pw-4c2e91\n',
+     position: 10,
+     line: 0,
+     column: 10,
+     snippet: ' 1 | password: !ks1108-tag-Pw-4c2e91\n---------------^'
+   }
+ }

 ❯ tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts:47:30
     45|         expect(err).toBeInstanceOf(Error);
     46|         const rendered = inspect(err, { depth: 6 });
     47|         expect(rendered).not.toContain(SENTINEL);
       |                              ^
     48|         expect((err as Error).message).toContain(`Could not parse YAML…
     49|         expect((err as Error).message).toContain(' at line 1, column '…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/1]⎯


 Test Files  1 failed (1)
      Tests  1 failed | 1 passed (2)
   Start at  19:39:04
   Duration  159ms (transform 35ms, setup 0ms, import 67ms, tests 10ms, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-GREEN-FINAL.out TEXT_SHA256 9b760cf02fc14950c8814820fc45f4875fa7d73f6de012587bc9cad5842195f0


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto


 Test Files  1 passed (1)
      Tests  2 passed (2)
   Start at  19:44:41
   Duration  190ms (transform 41ms, setup 0ms, import 76ms, tests 9ms, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-lint-HEAD.out TEXT_SHA256 8046a065258fc3279f849445c5021099554ed060844aa7515c73a563d8f700a8


> secuura-akto@1.0.0 lint
> tsc -p tsconfig.json --noEmit && eslint . --config eslint.config.js && stylelint "src/**/*.css"


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts
  16:1   error  Missing JSDoc @param "fn" declaration                                                                                                                                                    jsdoc/require-param
  16:1   error  Missing JSDoc @returns declaration                                                                                                                                                       jsdoc/require-returns
  26:1   error  Missing JSDoc @param "content" declaration                                                                                                                                               jsdoc/require-param
  26:1   error  Missing JSDoc @returns declaration                                                                                                                                                       jsdoc/require-returns
  48:50  error  Replace ``Could·not·parse·YAML·in·${path.join(repoRoot,·SECRETS_FILE_RELATIVE)}`` with `⏎············`Could·not·parse·YAML·in·${path.join(repoRoot,·SECRETS_FILE_RELATIVE)}`,⏎········`  prettier/prettier

✖ 5 problems (5 errors, 0 warnings)
  3 errors and 0 warnings potentially fixable with the `--fix` option.



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-lint-FINAL.out TEXT_SHA256 2fbea13ca93fba7f0cde58cf60a7836b586510b19e85deff9810c361409f9fe2


> secuura-akto@1.0.0 lint
> tsc -p tsconfig.json --noEmit && eslint . --config eslint.config.js && stylelint "src/**/*.css"



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-lint-CONTROL2.out TEXT_SHA256 10afb48c78161f50a97ad96e7a744fce376bd312a5e04eecc53c8f9b8149ceb0


> secuura-akto@1.0.0 lint
> tsc -p tsconfig.json --noEmit && eslint . --config eslint.config.js && stylelint "src/**/*.css"


/Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2/systemTest/akto/tests/unit/config/ks1108-secrets-parse-failure-prints-no-content.test.ts
  16:1  error  Missing JSDoc @param "fn" declaration  jsdoc/require-param

✖ 1 problem (1 error, 0 warnings)
  1 error and 0 warnings potentially fixable with the `--fix` option.



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-disclosure.diff TEXT_SHA256 59333a77e8941f0ce25707fe3957c762288c780d427279692a0f7b31edb86564

16c16,20
< /** Whatever `fn` throws, or undefined. */
---
> /**
>  * Whatever `fn` throws, or undefined.
>  * @param {() => unknown} fn - the call to run.
>  * @returns {unknown} what `fn` threw, or undefined if it did not throw.
>  */
26c30,34
< /** Write `content` as the secrets file under a temporary repo root and return that root. */
---
> /**
>  * Write `content` as the secrets file under a temporary repo root and return that root.
>  * @param {string} content - the bytes to write as the secrets file.
>  * @returns {string} the temporary repo root the file was written under.
>  */
48c56,58
<         expect((err as Error).message).toContain(`Could not parse YAML in ${path.join(repoRoot, SECRETS_FILE_RELATIVE)}`);
---
>         expect((err as Error).message).toContain(
>             `Could not parse YAML in ${path.join(repoRoot, SECRETS_FILE_RELATIVE)}`,
>         );


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-product-actual.diff TEXT_SHA256 d6bacca7e12cd17d4d6518561a95c3744e27259c56162d7777cd0bf075dfbc5b

diff --git a/systemTest/akto/src/config/secrets.ts b/systemTest/akto/src/config/secrets.ts
index 413c2d1f4..30d696b6b 100644
--- a/systemTest/akto/src/config/secrets.ts
+++ b/systemTest/akto/src/config/secrets.ts
@@ -37,5 +37,18 @@ export function loadSecretsYml(repoRoot: string): { data: SecretsYml; filePath:
         log.error('Then fill in your Akto dashboard and Secuura credentials.');
         process.exit(1);
     }
-    return { data: loadYaml(fs.readFileSync(filePath, 'utf-8')) as SecretsYml, filePath };
+    // KS-1108 (the KS-1099 shape): a js-yaml YAMLException carries the whole file in mark.buffer and, for a bare
+    // `!`/`*` value, the value itself in `reason`; an uncaught print would show every credential. Name only the
+    // file and the position — never the reason, the message, the mark or a cause.
+    const source = fs.readFileSync(filePath, 'utf-8');
+    try {
+        return { data: loadYaml(source) as SecretsYml, filePath };
+    } catch (err: unknown) {
+        const mark = (err as { mark?: { line?: number; column?: number } }).mark;
+        const where =
+            mark && typeof mark.line === 'number' && typeof mark.column === 'number'
+                ? ` at line ${String(mark.line + 1)}, column ${String(mark.column + 1)}`
+                : ' at an unknown position';
+        throw new Error(`Could not parse YAML in ${filePath}${where} (the file's content is not shown).`);
+    }
 }


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-akto-FINAL.out — TAIL (last 5 of 42 lines); the WHOLE file's TEXT_SHA256 c0c2f053e5e4aa50eb8aef828ce1b1f9c0694e9b64cec74ef033a84be49590d8

 Test Files  71 passed (71)
      Tests  1238 passed (1238)
   Start at  19:44:42
   Duration  1.50s (transform 3.27s, setup 0ms, import 6.75s, tests 3.42s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i5-push.out TEXT_SHA256 bb17ae71907a91aa8f0936563514df474fff7853379c9d2035d7551230b316b5

2026-09-27T09:45:50Z pushing feature/ks-1108-akto-secrets-parse-failure-b34-5 head f9348a9d10b7512d22a33a0a471f9042ad622831 from /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2
2026-09-27T09:45:53Z origin heads for this branch: 0 (first push requires 0)
2026-09-27T09:45:53Z effective: POLL=5s COOLOFF=90s SAME_MAX=1200s STALE_MAX=300s TOTAL_MAX=3600s
2026-09-27T09:45:53Z LOCK TAKEN by Secuura/Blockchain b34 pid 18030 for feature/ks-1108-akto-secrets-parse-failure-b34-5 (poll 1, waited 0s)
2026-09-27T09:45:53Z PUSH START
2026-09-27T09:46:00Z push rc=0
[format-gate] 1 package(s) checked, 0 skipped, 0 failed
2026-09-27T09:46:00Z LOCK RELEASED by Secuura/Blockchain b34 pid 18030 (cool-off stamp written; my next take waits 90s)
2026-09-27T09:46:00Z ls-remote after the push:
f9348a9d10b7512d22a33a0a471f9042ad622831	refs/heads/feature/ks-1108-akto-secrets-parse-failure-b34-5
2026-09-27T09:46:04Z my own orphaned login_stub pids (cwd under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1108r2): 0
0


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i6-RED.out TEXT_SHA256 11c1d342fdb3c54b386a8b05be9d0d5260439d7e86d24e981160b8b968c40e8e


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1196/Blockchain/Dev/services/api-gateway

 ❯ src/__tests__/ks1196-admin-post-api-admin-document-types.test.ts (4 tests | 2 failed) 8ms
     × KS-1196 R1 - two creates in the same millisecond answer two different ids 5ms
     × KS-1196 R2 - both types are still in the catalogue after the second create 2ms

⎯⎯⎯⎯⎯⎯⎯ Failed Tests 2 ⎯⎯⎯⎯⎯⎯⎯

 FAIL  src/__tests__/ks1196-admin-post-api-admin-document-types.test.ts > KS-1196 - two document-type creates in one millisecond never share an id > KS-1196 R1 - two creates in the same millisecond answer two different ids
AssertionError: expected 'dt-1758000000000' not to be 'dt-1758000000000' // Object.is equality
 ❯ src/__tests__/ks1196-admin-post-api-admin-document-types.test.ts:97:32
     95|     const second = await dispatch(router, { name: 'Beta Type', code: '…
     96|     expect([first._status, second._status]).toEqual([201, 201]);
     97|     expect(first._json.id).not.toBe(second._json.id);
       |                                ^
     98|   });
     99|   it('KS-1196 R2 - both types are still in the catalogue after the sec…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[1/2]⎯

 FAIL  src/__tests__/ks1196-admin-post-api-admin-document-types.test.ts > KS-1196 - two document-type creates in one millisecond never share an id > KS-1196 R2 - both types are still in the catalogue after the second create
AssertionError: expected [ 'Beta Type' ] to deeply equal [ 'Alpha Type', 'Beta Type' ]

- Expected
+ Received

  [
-   "Alpha Type",
    "Beta Type",
  ]

 ❯ src/__tests__/ks1196-admin-post-api-admin-document-types.test.ts:104:19
    102|     await dispatch(router, { name: 'Beta Type', code: 'BETA' });
    103|     const names = Array.from(catalogue.values()).map((t) => t.name).so…
    104|     expect(names).toEqual(['Alpha Type', 'Beta Type']);
       |                   ^
    105|   });
    106|   it('KS-1196 CONTROL - one create answers 201 with a dt- id stored un…

⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯[2/2]⎯


 Test Files  1 failed (1)
      Tests  2 failed | 2 passed (4)
   Start at  21:08:49
   Duration  376ms (transform 78ms, setup 60ms, import 227ms, tests 8ms, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i6-GREEN.out TEXT_SHA256 d37db462754e236843e07eb1c52c71575e571b0d2c8c1939ff547792fe973d56


 RUN  v4.1.11 /Volumes/DevMASTER/!CODING/Secuura/Blockchain/worktrees/s-b34-ks1196/Blockchain/Dev/services/api-gateway


 Test Files  1 passed (1)
      Tests  4 passed (4)
   Start at  21:08:40
   Duration  8.46s (transform 273ms, setup 68ms, import 7.88s, tests 6ms, environment 0ms)



## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i6-gw-BARE.out — TAIL (last 6 of 35 lines); the WHOLE file's TEXT_SHA256 c83795458b0c515270b8d784968180cafb5998404281191b7ce3cc7a75f86bb7


 Test Files  82 passed (82)
      Tests  754 passed (754)
   Start at  21:09:22
   Duration  7.62s (transform 3.23s, setup 3.30s, import 15.72s, tests 50.70s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i6-gw-PATCHED.out — TAIL (last 6 of 35 lines); the WHOLE file's TEXT_SHA256 2bf75d93716ea4c51e80e41aa42fd9dc97f8bfe2f600c5292045474c2b411b56


 Test Files  83 passed (83)
      Tests  758 passed (758)
   Start at  21:09:12
   Duration  9.20s (transform 5.53s, setup 3.24s, import 20.75s, tests 60.10s, environment 4ms)


## SEAT RECORD /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-09-27_seatB-34th/raise/i6-prod-now.diff TEXT_SHA256 0d78548552760f114e8e46f380cc5d70c994cbd3758be293e0eb38c4b8e51531

diff --git a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
index 2e558148f..046a17226 100644
--- a/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
+++ b/Blockchain/Dev/services/api-gateway/src/routes/admin.ts
@@ -679,7 +679,7 @@ export function createAdminRoutes(deps: AdminRouteDeps): Router {
   router.post('/api/admin/document-types', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
     try {
       const body = req.body || {};
-      const id = `dt-${Date.now()}`;
+      const id = `dt-${crypto.randomUUID()}`; // KS-1196: use crypto.randomUUID to avoid millisecond collisions
       const now = new Date().toISOString();
       const docType = {
         id,


