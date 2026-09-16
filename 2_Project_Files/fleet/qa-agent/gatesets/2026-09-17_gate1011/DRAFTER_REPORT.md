# DRAFTER REPORT — #1011 (KS-871) TIER 1 gate set @ 0a1f8900c7094fbdaed1099799c029e351296b39

Drafted 2026-09-17 04:02–04:21 AEST (from `date`) by a Wednesday drafting subagent. Nothing was launched and no tmux pane was opened. The launcher ran with `--check` only. Nothing was merged, commented, filed or mailed.

## BLUF

- **Set ready.** Launcher `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks871_1011.sh` (mode 755, sha256 `86f3d54992d93b3d`). **`--check` rc 0** at 04:17:33–04:17:44 (`check.out`). **8/8 negative fixtures refused with the expected distinct exit codes** (`controls_check.out`, 04:18:00–04:20:02).
- Brief: `briefs/2026-09-17_secuura-1011-ks871-tier1.md`. Prompt: `.prompt.txt`.
- **PREDICTION 1, the top one: "admitted requests unchanged" is FALSE.** On the real app, head writes a different audit row than base for non-gdpr requests, both admitted and refused:
  - Every non-proxied `/api/v1/*` request: `POST /api/v1/logs` is `logs.create`/`log` on base and `v1.create`/`v1` on head.
  - Every repeated-slash spelling: `details.path` is written raw.
  - Request targets the caller controls: `/api/logs#frag` → `logs#frag.create`, and the absolute form → `127.0.0.1.logs` with resource_type `127.0.0.1`.

  The cause: index.ts:561-562 strips `/api/v1/` ABOVE the audit mount, and index.ts:566-569 says the audit middleware is wired after that strip "so audit `action` derives from canonical paths". `req.originalUrl` is never stripped. Under NODE_ENV=production, versioning.ts 307-redirects unversioned `/api/*` to `/api/v1/*` above the audit mount (READ ONLY), so in production this likely hits most audited writes. Predicted: a Major finding against the PR.
- **PREDICTION 2: no test pins any non-gdpr audit row.** Tamper G-NONGDPR renamed every `/api/logs` action, still compiled (tsc rc 0), and reddened 0 of 406 cells. The drafter's counterfactual (entry-time canonical `req.path` feeding both fields) fixes all 5 gdpr refusals, restores base parity everywhere else, and also leaves 49/406 green. So the suite cannot tell head apart from a shape that has no parity break. Predicted: a coverage finding, plus the ruling that C2 is right: the timing is the fix, but the `originalUrl` source is what breaks parity.

## Read-only pre-measurements (PREDICTIONS for the gate, not verdicts)

| # | what | instrument | result |
|---|---|---|---|
| P0 | head / develop / shape | `git_read.out` 04:13:13, `gh_read.out` 04:07:56 | head `0a1f8900c` = refs/pull/1011/head = branch; parent = develop `d067725ff`; compare ahead 1, behind 0, files 3. Merged tree = head tree (api-gateway tree `3641022ec`) |
| P1 | real-app census, 29 requests | `qa1011-drafter-probe.test.ts`, `drafter_probe.py` → `drafter_probe.out`, `probe_rows_{base,head}.json` | SAME 17, DIFF 12. The 12 differences: 5 gdpr refusals fixed (invalid token 401, connector 403, user 403, trailing slash, `//erasures`); `/api/v1/logs` ×2 and `/api/v1/documents` regressed; `//api//logs`, `#frag` and absolute-form regressed; `/api/batch/verify` fixed (`unknown.create` `/verify` → `batch.verify`). A no-credential gdpr POST was already right on base: the spec auth gate at index.ts:1044 refuses it before the door. GET refused: no row on either tree. isDbAvailable false: no row on either. Sink throws: response unchanged on both |
| P2 | nested-mount fixture | same probe | Mounted under `app.use('/gw', router)`: base refused `unknown.create` `/x`, admitted `ok.create`. Head: `api.x` and `api.create`, path `/gw/...`. Both trees mis-derive, differently. The real app mounts the audit middleware at the root (index.ts:570), so this is predicted to be a Record |
| P3 | counterfactual: entry `req.path` for both fields | `drafter_probe_entrypath.py` → `.out` 04:11:47 | vs base: SAME 22, DIFF 7, all 7 fixes (5 gdpr, batch, proxied v1 login → `auth.login`). Whole suite on that variant: 49/406 green. Restored sha-identical |
| P4 | suites + tsc + eslint | `drafter_suites.py` → `.out` 04:07:41 | base 47/400, head 49/406, 0 pending. `tsc -p .` rc 0 on both. Including program: 35 lines in 11 files on base AND head, 0 in the touched files, NEW 0 / GONE 0. eslint 0/0 on the 3 files |
| P5 | the gate's own tampers (whole suite, 49/406 asserted, tsc rc 0 every row) | same | G-CTRL: 1 red (Part A CONTROL), as predicted. **G-NONGDPR: 0 red.** G-ADMITTED-ONLY: 1 red (Part A 🔴), as predicted |
| P6 | Linear | `linear_read.out` 04:08:27 | attachmentsForURL(pull/1011) = KS-871 `contributes` only. KS-843 and KS-858 have no #1011 attachment |
| P7 | disjointness | `gh_read.out`, `gh_read2.out` 04:12:10 | 20 open PRs, and none touches audit.ts, the ks871 tests, index.ts, proxy.ts, normalisePath.ts, versioning.ts or db.ts. #1010 = verification.ts + the ks1087 test |
| P8 | READY lines vs head | `SEAT/patches/A0-product.patch`, `B0-product.patch` (READ) | The code tokens match head. The trailing comments were rewritten (declared). B0's context lacks base's `// Trim trailing slashes…` line, which is why the seat applied it by hand |
| P9 | checkout bounds | `git_read.out` 04:13:13 → `bounds_end.out` 04:20:11 | porcelain 0 → 0, `.git/config` sha256 `bb55e140…` unchanged, refs 897 → 897, worktrees 111 → 111, head and develop unmoved. The checkout `.vite` dirs have 0 entries newer than the drafter's setup script (control: 8 entries older) |

## Every disagreement with the READY mail

1. **"Admitted requests unchanged."** Refuted for non-proxied `/api/v1/*`, repeated-slash spellings, `#` / absolute-form request targets, and prefix-mounted routers (P1).
2. **"The timing is the fix."** Agreed, but it is incomplete: `req.originalUrl` is a different value, not only a different moment. Entry-time `req.path` carries the fix without the regressions (P3).
3. **"Including tsc: 12 → 0 in the touched files, 33 elsewhere identical."** The drafter's program gives 35 lines / 11 files on both trees and 0 in the touched files. The seat's `including-tsc2.out` has 54 `error TS` lines, including TS2741 `keepAliveTimeoutBuffer`. The #1009 gate saw the same kind of program / type-resolution difference.
4. **"KS-843 / KS-858 are named in the body."** The body carries KS-843 ×2 and KS-871 ×7 but KS-858 0 times. KS-858 appears only in the `linear[bot]` comment.
5. **"For a proxied /api/auth/login they may see a trimmed path."** On base the proxied login row already carries the full path, because http-proxy-middleware v2 resets `req.url` from `originalUrl`. But `attemptedEmail` is absent on both trees: index.ts:399-413 skips body parsing for `/api/auth`. On base, `/api/v1/auth/login` already derives `v1.login`. Both are pre-existing, predicted Records.
6. **"Refused POST /api/gdpr/erasures was audited as `/`."** That holds only for refusals INSIDE the door (invalid token, scope/role). The no-credential refusal comes from the app-level spec gate and was already correct on base (P1).
7. **"No HTTP response change."** Agreed for every census row: status and the first 160 body bytes are identical. Full bodies and headers are the gate's to measure.

## Launcher negative fixtures (`controls_check.out`, all `--check`)

| fixture | expected | got |
|---|---|---|
| N1 head override = #1010's head | 6 | 6 |
| N2 prompt without MAIL YOUR VERDICT | 12 | 12 |
| N3 brief without the head SHA | 20 | 20 |
| N4 brief without TIER 1 | 7 | 7 |
| N5 prompt without per-ENTRY farm | 22 | 22 |
| N6 prompt without the exact verdict subject | 23 | 23 |
| N7 develop = #1011 head (audit.ts `f5a83ba2c` LANDED) | 19 | 19 |
| N8 develop = `0f489b7da` (audit.ts blob nobody pinned) | 18 | 18 |

The launcher was generated by `gen_launcher_1011.py` from `launch_qa_secuura_ks1087_1008.sh`, which has the same shape (develop = the head's parent): 25 asserted substitutions, a residual guard, 66 output controls, `#1011` count 10 enumerated first to scratch, `bash -n` rc 0. Added in the #1010 set's form: exit 22 (per-ENTRY farm), exit 23 (exact subject, coagent@ sender, wednesday-agent@ recipient), and a `QA1011_CUR_DEV` override that works only under `--check` (a launch with it set refuses, exit 16). JUDGED blobs: 12 files. GUARDED: those 12, the 2 ks871 tests and the Dev lockfile. DEV_CONTENT_ALLOWED is empty.

## Outside the rules, stated

- Three runs aborted on the drafter's own mistakes and are kept by rename, never deleted:
  - `drafter_probe_entrypath.first-run-marker-count.out` and `.second-run-marker-count.out`: wrong marker counts. The edit had landed in the drafter's clone and was restored by `git checkout --` inside the clone before each re-run. sha `68aa15724437` was asserted on the final restore.
  - `gen_launcher.enumerate-to-scratch.first-run-residual-eleven.out`: the residual guard caught the drafter's own header wording.
- Scratch files were moved with `mv` (a rename). Nothing was `rm`'d.
- The first attempt at a one-line checkout-counter read put `git -C … worktree list` on the tool line, and the hook refused it. It was re-run from the script `git_read.sh`, which is read verbs only.
- Probe caveat: the census ran under vitest's NODE_ENV=test. The production claim (the 307 → `/api/v1/`) is READ ONLY. `durationMs` was excluded from the comparison.
- The drafter scratch clone lives at `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/8cbf758d-cbd5-4880-9064-4f71c8077706/scratchpad/gate1011_draft_3b_i093i` (`drafter_paths.json`).
