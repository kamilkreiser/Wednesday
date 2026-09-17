# DRAFTER REPORT: #1021 (KS-1211, colord row 6) tier-2 gate set, 2026-09-17 17:46–18:03 AEST

**BLUF**
- **Files:**
  - brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1021-ks1211-colord-tier2.md` (sha256 `0d133ac05a343526…`)
  - prompt: `…/briefs/2026-09-17_secuura-1021-ks1211-colord-tier2.prompt.txt` (`017a7f3303e998c3…`, 7.2 KB; the #1020 prompt was 7.8 KB)
  - launcher: `…/launchers/launch_qa_secuura_ks1211_1021.sh`, from `gen_launcher_1021.py` with the #1020 tier-2 launcher as template: 22 asserted substitutions, 62 output controls, `#1021` enumerated at 12 first (`gen_launcher.enumerate-to-scratch.out`), residual guard clean, `bash -n` rc 0 (`gen_launcher.out`, 17:59:36).
- **`--check` rc 0** at 17:59:36 (`check.out`) and again at 18:03:22 on the final brief/prompt bytes (`check_final.out`). The develop line reads: all 13 judged blobs `= base` | *origin develop still 581c9db0d (#1019 squash on the PR parent, api-gateway only)*.
- **Negative controls, `--check` only (`controls_check.out`, 18:00:15):** head override exit 6, prompt without MAIL exit 12, brief without the full SHA exit 20, brief without TIER 2 exit 7, prompt without the push/preflight ban exit 11. All as expected.
- **⚠ Develop moved during drafting.** f8c7aaa39 at 17:46:03; **581c9db0d (#1019, KS-1187, Seat A) by 17:54:41**, 3 api-gateway files. The launcher pins DEVELOP_SHA = 581c9db0d, MERGE_BASE = f8c7aaa39; compare still `f8c7aaa39 ahead=1 files=3`. Merged tree predicted `207ba797c` = develop + exactly the 3 PR files.
- **Launcher develop arm:** judges 13 blobs (the 3 PR files, with their own blobs → exit 19 LANDED; both harness package.json; audit-locks/gate, lock-discovery, baseline-contract, scripts/audit package.json; preflight.sh; lockfile-cleanroom.sh; systemTest/CLAUDE.md). GUARDED prefixes: `Blockchain/Dev/scripts/audit/`, `Blockchain/Dev/scripts/preflight/`, both harness manifests and locks, `systemTest/CLAUDE.md`, `.githooks/pre-push`. **Seat B's next row PR (hono) edits audit-baseline.json: if it merges before this gate launches, `--check` refuses exit 18 by design. Re-pin, do not bypass.**
- **Mail subject in prompt and brief:** `[QA -> Wednesday] TIER 2 GATE #1021 (KS-1211) 742e1c608 — <GO | GO WITH FINDINGS | NO GO>`, from coagent@ to wednesday-agent@ via the AgentMail API, as in #1020.

**The six lead questions: drafter predictions (raw runs in `out/`)**
1. **Scope control: PASS predicted** (`out/parse_probe.out`). Each lock: 1 `packages` key changed (`node_modules/colord`: version, resolved, integrity), entry counts 423=423 and 361=361, `dev` true both sides, `packages[""]` and all other top-level keys identical. Planted control detected. Baseline 38 → 37, only GHSA-2wm5 removed, 0 added, 0 altered, survivor order identical; planted control detected. `-w` numstat = plain. The seat's byte round-trip claim was NOT re-run.
2. **Advisory gone: PASS predicted** (`out/audit_runs.out`, `out/gate_ctrl.out`, live registry 17:54).
   - head/head: audit-locks rc 0 (43 = 45 − 1 − 1), 0 CLEANUP; audit-gate rc 0 "36 reported, 37 baselined", 0 CLEANUP.
   - head/develop baseline: audit-locks rc 0 + `CLEANUP — 1 … GHSA-2wm5-q62r-hmrv (KS-1024)` (`audit-locks.mjs:299`).
   - base without the row: audit-locks rc 1, exactly GHSA-2wm5, 2.9.3, 2 locks, **twice** (KS-1025).
   - second negative control: head without the other standalone row q8mj → rc 1 exactly q8mj.
   - audit-gate is blind to colord (rc 0 at base without the row; `audit-gate.mjs:204` skips standalone-locks rows) and CAN red (head without js-yaml GHSA-2883 → rc 1).
3. **Fixed, in range, and the evidence gap.**
   - The gate's own teed bulk-advisory response for colord@2.9.3: `vulnerable_versions "<2.9.4"`, moderate. For 2.10.0 the response has no colord key. Shipped semver 7.8.5: `satisfies('2.10.0','<2.9.4')` false (controls 2.9.3 true, 2.9.4 false); `satisfies('2.10.0','^2.9.3')` true (controls 3.0.0, 2.9.2 false). String compare would say `'2.10.0' < '2.9.4'` true.
   - Clean-room on both harness dirs: 2/2 OK at head and at base. Controls: bogus integrity → still **OK** (dry-run cannot see it); declarer range `^3.0.0` → **FAIL** (it can see that). **So clean-room alone is not sufficient.**
   - Real `npm ci --ignore-scripts`, head and base, both harnesses: rc 0, lock sha unchanged; `npm ls colord` = stylelint@17.14.1 → colord 2.10.0 / 2.9.3. **`npm run quality` rc 0 on all four:** akto 1233/1233, api-explorer 58/58, `found 0 vulnerabilities`. The READY's NOT COVERED item closes green in about 3 minutes.
   - **colord is not loaded by the harness lint:** 0 colord resolutions against 1151/1154 stylelint resolutions on the same trace. Only the `color-named` rule imports it. Forced on with a scratch config, colord loads (5 modules) and flags `red` identically on 2.10.0 and 2.9.3 (rc 2), clean file rc 0.
   - **Predicted FINDING (Minor, target: the seat's Test Evidence):** `systemTest/CLAUDE.md:449–470` makes the package `quality` gate mandatory before committing any systemTest change and "ALL FOUR full gates" before a systemTest PR; the READY ran neither. No defect behind it (measured green). The gate rules it.
4. **Reach: dev-only, harness-only predicted.** colord is in 2 of 45 tracked locks, both harness, `dev: true` (control: express 30). 0 in any package.json, Dockerfile or workflow. `pr-platform-suites.yml:515` would `npm ci` akto on a CI runner (not an image); api-explorer is in no workflow; **GitHub Actions is retired** (6 runs `failure`, 1 `skipped` on the head; `checks_read2.out`).
5. **linkKind / merged tree / overlap** (`api_read.out` 17:48:46–17:49:03; `out/merged.out`).
   - attachmentsForURL(pull/1021) = KS-1211 contributes, open; pull/99999 = 0.
   - 0 closing phrases in title, body, commit and comment (planted controls).
   - 0 of 20 other open PRs share a file; none touches scripts/audit, preflight or either harness.
   - Merged tree `207ba797c` is clean and differs from head only by #1019's 3 api-gateway files. Control: develop merged with itself gives develop's tree.
6. **§5f predicted:** not a runtime-behaviour change (no image, no service, colord not even loaded by the harness config). KS-1211 stays In Progress (6 rows remain), and no ticket moves to Done. KS-1211 went Backlog → In Progress by GitHub at 07:43:03Z; `completedAt` null.

**Where the READY disagrees with what I measured**
- Nothing measured contradicts a seat number. The disagreements are about what the evidence proves:
  1. Parse plus clean-room cannot see a bad integrity (measured).
  2. The harness quality gate is a written MUST that the READY skipped (measured green by the drafter).
  3. "Seven rows" / "row 6": KS-1211 carries 7 rows and #1021 fixes 1.
- **Severity wording:** the PR says "medium" (GitHub DB), the feed says "moderate". RECORD.

**HOLDs I came near**
- **Develop moved mid-draft.** Caught by the merged-tree probe at 17:54, not assumed. The launcher, brief and prompt were re-pinned to 581c9db0d before generation, and `--check` confirms.
- **Instrument fault, publicly corrected:** my first color-named run printed "rc 0" for all four because `$?` in the echo read the preceding `$(python3 …)` substitution, not stylelint. The saved output showed the error line. Re-run with `rc=$?` on its own line gives rc 2 / 0 / 2 / 0 (`out/cn/color_named.out`). The faulty lines are not quoted anywhere.
- **C3 control void:** `npm ci --dry-run` against a manifest `stylelint ^99.0.0` hung > 5 min. I ended pid 47432 after checking its cwd (my scratch api-explorer) and parent (my probe). Its rc 1 is the SIGTERM; the brief says so. C2 stands in as the failing control.
- The trace hook's first run had no positive control and read 0. I added the stylelint-path control (1151) before believing the 0.
- `out/audit_runs.out`'s tee summary printed Python errors (shell brace mangling inside `$(…)`). The tee files are intact and were read by a heredoc script. The data quoted comes from that read, not from the broken summary.
- **GitHub check-runs** returned 403 for this token. `checks_read.py`/`.out` quarantined by rename (`.403-quarantined`). The Actions runs read came from an inline heredoc script whose output is `checks_read2.out`; the script body was not saved as a file.
- **Clean boundaries:** launcher run with `--check` only (plus 5 negative `--check` controls). Write verbs and installs only in `/private/tmp/claude-501/drafter1021/` (clone + worktrees, porcelain 0 at close). No rm, no cd, no mail, no commit, no push, no credential echoed, no Seat A/B worktree entered.
- **Secuura checkout:** 17:46:03 porcelain 0, config `d7e7298b02c45f52`, refs 922, `.git/worktrees` 112. At 18:02:31: 0, same, 924, 112 (refs moved with seat fetches). The #1020 set's "worktrees 111" was a different instrument; I count `.git/worktrees` entries because the hook refuses `git worktree list`.

**NOT measured (the gate must, or must say it did not)**
- The seat's byte round-trip of audit-baseline.json.
- The gates and parse on the merged tree `207ba797c` (identity argued, not run).
- A real `npm ci` rejecting a bad integrity (only the dry-run half was measured).
- The Playwright, Performance and Schemathesis quality gates ("all four" rule); legs 1–15 of preflight whole.
- Any image content; api-explorer's CI install path (none found).
- Whether the gate's advisory feed changes between now and the run (KS-1025).

**Read before launching**
1. Re-run `--check`. Exit 18 means develop moved into a guarded path, most likely Seat B's hono PR touching audit-baseline.json. That calls for a re-pin, not a bypass.
2. Drafter's likely verdict: **GO WITH FINDINGS** (the Minor process finding on the missing harness quality gate), with no defect in the bytes.
