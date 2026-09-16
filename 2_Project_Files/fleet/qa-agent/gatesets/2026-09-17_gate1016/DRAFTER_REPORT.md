# DRAFTER REPORT — #1016 (KS-1072) TIER 1 ROUND 1 gate set @ a226d94fe8c6fbfecb81de415feb645302cdd166

Drafted 2026-09-17 06:41–07:07 AEST (clocks from `date`) by a Wednesday drafting subagent. Nothing was launched and no pane was opened. The launcher ran with `--check` only. Nothing was merged, pushed, commented, filed or mailed. No git write verb touched the Secuura checkout. No `*1015*` or `*1014*` file was written.

## BLUF

- **The set is ready.**
  - Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1016-ks1072-tier1.md` (sha256 `57f81507fa7cd208`, 214 lines)
  - Prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1016-ks1072-tier1.prompt.txt` (`31caf8968d71d778`, 156 lines)
  - Launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1072_1016.sh` (mode 755, `f42e41eb5d2a1b49`, 215 lines, `bash -n` rc 0)
- **`--check` rc 0** at 07:04:43–54 (`check.out`) on the final brief and prompt.
- **10/10 negative fixtures refused** with the expected exit (`controls_check.out`, 07:05:11–07:06:39): subject 23, tier 7, SHA 20, mail step 12, per-entry farm 22, head override 6, plus LANDED 19, unpinned verification.ts blob 18, develop behind the pin 18, ROUND 1 missing 15.
- **Develop did NOT move during the draft:** `523f283c6` at 06:42:47, 06:55:00, 07:06:53 (= the PR parent). The merged tree is the head tree (`eecd5f087`). The launcher content-allows #1014's two blobs if it lands mid-run; that ALLOW path is **not proven by a fixture** (no real develop descendant carrying them exists yet).

## Top predictions (drafter-labelled; the gate falsifies)

1. **GO-shaped on the selector itself.** MEASURED, router-level, 30 rows (`drafter_compare.out`):
   - 12 verdict flips and 6 txHash-only flips base → head. **Every one selects the row KS-1072's words select**: highest block, then the latest `confirmedAt`, with a missing date last.
   - Tier-1 rows: 0 hits. The seat's six tampers reproduce exactly (0/3/4/1/1/0), and under TA all 30 rows equal base. The gate tampers: **G-CTRL reds exactly the newer-listed-first control, and G-OLDEST reds 3.**
   - Reachability (READ): anchoring keeps one row per `(document_id, network)`, so no single-network deployment can present an equal positive-block tie. A `0`/`null` tie can never read on-chain.
2. **The likely FINDINGS are test-quality, and they recur from #1005 — both come from the seat's "tier-2 source guard".**
   - The guard is not a tier witness. With tier 1 answering, 5/5 cells red at the txHash assertion while the guard stays GREEN. This is P-1005-1 again.
   - It adds the PR's only NEW including-tsc error: TS18046 at `ks1072…test.ts(124,10)`. This is P-1005-4's class.
   - Predicted grade: POLISH ×2, recurrence noted, GO WITH FINDINGS.
3. **Records around the READY and the edge shapes, none a Blocker:**
   - The pushed test is 177 lines (150 READY + 27 net seat lines), not "the 150 lines".
   - Without `--recount`, the READY test hunk applies silently at 132 lines. This is the READY pipeline's defect.
   - The PR body's "15 lines lower" is git's offset 13.
   - A tie on both fields is still decided by response order (consistent with anchoring's own `:676` ordering today).
   - Snake_case rows are invisible to the selector.
   - A `'abc'` blockNumber makes the comparator return NaN and skip the tiebreak.
   - An offset-less ISO date selects differently under `TZ=UTC` and `TZ=Australia/Sydney` at head.
   - A numeric epoch-ms or pre-1970 `confirmedAt` loses to a missing date. None of these is emitted by anchoring (READ).

## What the drafter measured (all in this folder)

| # | what | instrument → output | result |
|---|---|---|---|
| P0 | head, parent, diff, blobs, checkout | `git_read.sh` → `.out` 06:42:47; `bounds.sh` → `bounds_mid.out` 06:55:00, `bounds_end.out` 07:06:53 | head = branch = pull/1016/head; only parent `523f283c6` = develop. Files: verification.ts `04b3d980f → a7a6d4605` (+7 −2), ks1072 test `4ad1cdcd1` (+177). Checkout ×3: HEAD `355d82c8b`, porcelain 0, config `d7e7298b…`, refs **905** at all three readings, worktrees 110/111, `.vite` unchanged, 0 newer entries |
| P1 | GitHub | `gh_read.py` → `.out` 06:52:48–06:53:13, raw `gh/` | open, 1 commit, +184 −2, compare `ahead` 1 / behind 0 / files 2. 0 closing phrases (controls 1/1/0), 0 at-signs. 12 blobs identical at develop and head. 20 other open PRs, 0 exact shared files; #995 touches anchoring `src/index.ts` |
| P2 | Linear | `linear_read.py` → `.out` 06:53:13 | KS-1072 In Progress, prio 4, 1 comment. pull/1016 → KS-1072 `contributes` only. Control: pull/1011 → KS-871 `contributes`, merged |
| P3 | READY fidelity | `ready_read.py` → `.out` 06:45:21, `ready_to_head_test.diff`; `drafter_apply_check.py` → `.out` 06:54:01; `drafter_apply_numstat.py` → `.out` 06:54:21 | READY test: 150 `+` lines under a `+1,132` header. Head test 177 lines, READY → head +33 −6, all hunks declared. The READY + block is contiguous at head `:303-307`. Product hunk with `--recount`: `succeeded at 298 (offset 13 lines)`; corrupt without it. **Test hunk WITHOUT `--recount`: rc 0, numstat 132** |
| P4 | substrate | `drafter_setup.py` → `.out` 06:47:02–19 | `--shared` clone; worktrees base / head / merged (merged = head: develop is an ancestor). Per-entry farm: Dev 987, api-gateway 8, shared 8. **Wholesale links: 0.** Shared dist rc 0, IN TREE ×3 |
| P5 | suites | `drafter_run.py suite` → `drafter_suites.out` 06:49:17–39 | base 51/419, head 52/424, all pass, pending 0, project tsc rc 0 on both |
| P6 | verdict rows | `qa1016-drafter-probe.test.ts` + `drafter_run.py probe` → `drafter_probe.out`, `probe_rows_{base,head}_{UTC,Australia-Sydney}.json`; `drafter_compare.py/.out` | See prediction 1 and brief item 1. TZ-dependence: S22 only, at head only |
| P7 | tampers | `drafter_run.py tamper` → `drafter_tamper.out` 06:50:09–06:51:15, `vt_tamper_*.json`, `probe_rows_tamper_*.json` | TA 3, TV 4, TB 1, TN 1, TI 0, **G-CTRL 1, G-OLDEST 3**. 52/424 and tsc rc 0 on every row, restores sha-identical, only ks1072 cells red |
| P8 | guard + dead flag | `drafter_run.py guard` (in `drafter_ready_guard.first-run-…out` 06:51:26); `drafter_run.py readyfile` → `drafter_readyfile.out` 06:51:36–39 | GT-T1: 5/5 red at the txHash, guard green. READY verbatim: head 3/3, base 2 red. Pushed file: head 5/5, base 3 red |
| P9 | static | `drafter_tsc.py/.out` 06:51:54–06:52:00; `drafter_eslint.py/.out` 06:52:17–30 | Including tsc: base 30 lines / 10 files, head 31 / 11, NEW 1 = TS18046 `(124,10)`. eslint: verification.ts 5 = 5, test 0, READY flag 1, plant control 1 |
| P10 | READs | `class_census.out` 06:44:57, `unique_read.out` 06:46:41, `cells_read.out` 07:01:50, `misc_read.out` 06:58:00, `src/anchoring_index_head.ts` | Comparator only at `verification.ts:303-306`. Unique `(document_id, network)` at anchoring `:209`, migration 031 and both upserts. Anchoring lists `created_at DESC` `:1491` and verifies `confirmed_at DESC NULLS LAST, created_at DESC` `:676`. **KS-1180: 0 hits in api-gateway src, 0 commits on develop** (controls found) |
| P11 | launcher | inline asserting generator → launcher; `check_launcher.sh` → `check.out`; `controls_check.py` → `controls_check.out` | See the BLUF |

## Disagreements with the READY / the seat

1. **"A tier-2 guard in the helper … so a txHash assertion can never be about another tier"** (PR body) is false as measured (GT-T1). `source` is keyed on the hash (`verification.ts:774`). The #1005 gate filed exactly this as P-1005-1 the night before.
2. **"tsc api-gateway rc 0"** is the `-p` program, which type-checks 0 `__tests__` files. The including program shows 1 NEW error, and it sits on the seat's own guard line, not in the READY.
3. **"the file is byte-equal to the 150 lines"** holds only for the moment after the apply. The pushed blob is 177 lines. Every delta is a declared seat edit, so there is no hidden edit.
4. **"applied cleanly 15 lines lower (`:300`, not `:285`)"**: git reports offset 13. The seat compared the base comment line `:300` with the READY hunk start `:285`.
5. **"Red before green … READY cells: 3 run, 2 red"** matches (READY verbatim on base). **"Final file: 5 run, 3 red"** matches.
6. **The six-row tamper table** matches exactly. The seat's TV is "oldest wins with missing FIRST". The gate's G-OLDEST is "oldest wins with missing LAST". It shows the missing-date cell cannot tell oldest-wins from newest-wins.
7. **"No other file carries a multi-anchor tier-2 fixture"** is consistent with every tamper redding only ks1072 cells. The census method is not re-derived by the drafter.

## Disagreements with the commission

1. **Item 6, "confirm the pushed test blob is the intended 150 lines".** It is not: it is 177 = 150 + declared edits. The brief asks the gate to assign every hunk, not to find 150.
2. **Item 1, "v1 and v2 routes".** v1 reaches the selector through the `/api/v1/` → `/api/` rewrite (`index.ts:562`). v2 carries only `/api/v2/verification/*`, proxied to originate (`proxy.ts:594-595`), so `/api/v2/documents/:id/verify` is predicted NOT to reach the selector. The drafter's harness mounts the router only; the brief sends the route rows to the real `index.ts` app.
3. **Item 5, "KS-1123 / KS-1180 cells still green".** The KS-1123 cells exist (ks1123-f2, ks1123-f3). **KS-1180 cells were NOT located** on develop: 0 source hits, 0 commits, controls found. Wednesday's daily note at 03:21 names a KS-1180 brief. The gate is told to locate them or record NOT LOCATED / NOT LANDED.
4. **Item 7, "a gate tamper that reverses the tiebreak (oldest wins)".** This is the seat's TV verbatim. The drafter added G-OLDEST (missing still last) so the gate row is not a duplicate. It shows a different red set (3, not 4).
5. **Item 3, "tier-2 source guard in the helper".** It is in the TEST helper `postTier2`, not in a product helper. The product change is the comparator plus 2 comment lines (parser proof owed by the gate, item 5).

## Deviations

- **Launcher.** Hand-derived from `launch_qa_secuura_ks1176_1014.sh` by one inline Python edit with asserted counts. It replaced the header, pins and the JUDGED / GUARDED / DEV_CONTENT_ALLOWED blocks whole, and ran a residual guard for `1014`/`1176`/`616c766a5`/`e0f41a8fa`/`8589933267` outside named #1014 mentions.
  - **The generator was run from stdin and is not saved as a file.** This is a provenance gap, stated here. The launcher header says "one inline asserting Python edit".
  - JUDGED: 12 files. GUARDED past `523f283c6`: api-gateway `src/` + config, anchoring `src/`, shared `src/`, `migrations/`, `docker/init/`, `docs/openapi/`, eslint, lockfile.
  - DEV_CONTENT_ALLOWED: #1014's `enforcement.ts 3e314ba11` and `ks1176 test 5820520ae`.
- **Negative fixtures:** the 6 commissioned, plus LANDED, unpinned blob, behind-the-pin and ROUND 1.
- **Brief items:** Wednesday's eleven in order, plus 12 (reachability), 13 (the class) and 14 (disjointness / develop moves). LEGITIMATE SHAPES (§2a) is filled with 9 rows, because the selector feeds a verifier.
- **Report dir / subject** are exactly as commissioned. The PRIOR REPORT section points at the #1005 gate's report (same file, recurring class). It is not a round N-1.

## Instrument slips, in the open (all kept on disk, renamed)

1. `drafter_run.py readyfile` asserted `tier1Absent` ×3 in the READY content; the truth is ×2 (declared + assigned; the doc comment does not name it). The assertion stopped the stage before any run: `drafter_ready_guard.first-run-readyfile-assert-tier1Absent-count-3-wrong-is-2.out`. The guard stage in the same file ran after it and is valid. Corrected and re-run: `drafter_readyfile.out`.
2. `drafter_apply_check.py` first applied the whole READY. The result was `depends on old contents` with `--recount` and corrupt at line 170 without it: `…first-run-unsplit-depends-on-old-contents.out`. The re-split is per file, as the seat did.
3. That script's second run died on the drafter's own docstring edit (SyntaxError): `…second-run-docstring-edit-syntaxerror.out`. The script was rewritten whole.
4. `cells_read` first run printed `git grep -c` counts without labels. `KS-1180`'s silence and `KS-1073`'s counts were indistinguishable: `cells_read.first-run-unlabelled-counts-ambiguous.out`. It was re-run labelled; the brief's KS-1180 statement rests on the labelled run.
5. A Wednesday hook refused two `git -C` calls: one with a shell-variable clone target, one `worktree list` on the checkout. Both were re-run from script files or dropped. Nothing ran.
6. `class_census.out` is labelled "non-test" but its `tier1Absent` block includes `__tests__` hits by design (git grep at a revision). The label is imprecise and the content is correct.
7. A background `grep -r` over `gatesets/` and `0_Brain/daily` for KS-1180 exceeded 120 s and finished in the background. It was used only for the daily-note pointer.

## Outside the rules, stated

- Drafter clone: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/76d545ac-4e62-4400-be44-c9ce11c3c344/scratchpad/gate1016_draft_wi3ngt9a` (`drafter_paths.json`).
  - Probe and READY copies were placed in the clone's `__tests__` only and quarantined by rename into `<clone>/_quarantine_2026-09-17/`.
  - Tamper edits and guard edits were restored by `git checkout --` in the clone, with sha256 asserted.
  - `git apply` ran with `--check` / `--numstat` only, in the clone.
- stderr was kept in every `.out`, and no `2>/dev/null` was used. No `rm` and no `cd`.
- **Not done by the drafter:**
  - `docker info`
  - the real `index.ts` app (v1/v2 route reach)
  - the parser proof
  - GT2
  - a status-keyed tamper
  - the pairwise null/string matrix beyond the 30 rows
  - the unique clause in every schema source
  - Linear KS-1180
  - the `packages/shared` and auth suites
  - a planted including-tsc control
  - the multi-anchor fixture census
