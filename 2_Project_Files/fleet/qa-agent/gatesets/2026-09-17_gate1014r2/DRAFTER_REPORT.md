# DRAFTER REPORT — #1014 (KS-1176) TIER 1 ROUND 2 (of 2) DELTA gate set @ 9ba0caf78b8ddb737541df38303b776c982521d2

Drafted 2026-09-17 07:28–08:1x AEST (clocks from `date`) by a Wednesday drafting subagent. Nothing was launched and no pane was opened; the launcher ran with `--check` only (the TTY guard, exit 21, is proven by READING the launch path, never by a bare run). Nothing was merged, pushed, commented, filed or mailed. No git write verb touched the Secuura checkout; `merge-tree --write-tree` ran only in the drafter clone.

## BLUF

- **The set is ready, re-pinned after develop moved under it.**
  - Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1014r2-ks1176-tier1.md` (sha256 `6200b342a6733574`)
  - Prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1014r2-ks1176-tier1.prompt.txt` (`a08ce65e4c49a0a3`)
  - Launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1176_1014r2.sh` (mode 755, `fedbac1df282f10e`, second form, pin develop `7e89318bc`)
- **`--check` rc 0** (`check.out`, final run on the final brief / prompt / launcher). The fixtures below were built from the brief two wording edits earlier (`:1220` → `:1219`; an escaped-key description), no guarded token touched. **15/15 negative fixtures** as expected (`controls_check.out` 08:13:48–08:17:27): subject 23, tier 7, SHA 20, mail 12, per-entry farm 22, head override 6, LANDED 19, pre-#1016 develop 18 (verification.ts cleared by region on REAL API content, then the ks1072 test refused), #1016 branch head 18 (compare diverged), **verification.ts moved INTO #1014's hunk region 18**, **INTO the verify gate 18**, **moved OUTSIDE both regions → 0 (positive control)**, round-1 report 24, CLOSED / STILL OPEN / NEW 25, ROUND 2 15.
- **Develop moved during drafting: #1016 (KS-1072) landed as `7e89318bc` at 07:57:19 AEST** (touching `verification.ts`, hunk `@@ -298`). The first launcher form (pin `eb1051fd3`, #1016's two blobs pre-cleared by content) passed `--check` at 08:01:27 against the REAL landed develop — proving that arm on live data — and Wednesday's 08:04 mail then asked for the re-pin. **`7e89318bc`'s tree `e09ede17e` equals the drafter's pre-landing merge-tree prediction for `eb1051fd3` × #1016.**
  - **Merged tree (head ⨝ `7e89318bc`): `5748a1d68318ed2e310a360fb79e7a1ebc63c785`**, clean (merge-tree in the clone = local merge commit `6f32d937b`'s tree = the OID predicted at 07:35 before #1016 landed). Merged blobs: `verification.ts 28fb58343`, `enforcement.ts be466fbf4`, ks1176 test `43cebf8d7`.
  - Suites (all pass, pending 0, project tsc rc 0): base 48/410, r1 49/423, head 49/428, **dev `7e89318bc` 52/424, merged 53/442**.

## Top predictions (drafter-labelled; the gate falsifies)

1. **F-1 is CLOSED for every `type` spelling on an ARRAY allow-list.** MEASURED on the real `index.ts` app with hit counters (`drafter_spell_compare.out`, `drafter_spell_counts.out`, 385 rows/tree): admitted-disallowed rows base 0 / r1 32 / **head 0 / merged 0**. Every non-allowed type named via `type` (incl. `''`/`null`/`false`/`0` beside it, case variants, ids, whitespace, ZWSP, duplicate keys last-wins, the key `typ\u0065` escaped in the raw JSON) → 403 FORBIDDEN, enforcement 0, workflow 0, forwarded 0. Allow-list and enforcement read the same key: 126 same / 0 mismatch at head (the instrument shows 8 under G-REV). The level axis vs round 1: r1 → head 32 create diffs, all the F-1 class (every one now 403 FORBIDDEN), 0 verify, 0 pure flips; head → merged 0 on both merged trees.
2. **Residue the gate must rule (all pre-existing classes that #1014 widens, like F-1 was):**
   - **(a) served `data.documentType`** (disagreement 1): a DOCUMENT-restricted connector sending `{type:"DOCUMENT", data:{documentType:"PROPERTY_DEED"}}` → 201 at head (403 at base). Originate (READ) stores type DOCUMENT but serves `data.documentType` first, and the gateway verify gate matches on it. Predicted NEW, Major candidate, TICKET, escalation candidate.
   - **(b) a STRING allow-list is a substring match** (disagreement 2): `"SSD_DOCUMENT"` admits DOCUMENT at head (10 rows; 403 at base). `PUT /api/admin/settings` stores the value unvalidated. Predicted NEW, Minor, TICKET.
   - **(c) an untyped body is persisted as DOCUMENT** (READ) whatever the allow-list: 16 rows at every tree (disagreement 3). STILL OPEN residue, TICKET.
3. **Tampers reproduce the READY exactly, and one gate tamper shows a blind spot.** T0 0 / TF 1 / TA 4 / TW 4 / TK 9 / TR 1 / TI 0 (49/428, tsc 0, sha-restored). Gate rows: G-F3CTRL 1 (F3), G-BOTH 2 (F1, F2), **G-REV 0**: no cell pins precedence when both fields disagree, yet under G-REV the census admits `{documentType:SSD_DOCUMENT, type:DOCUMENT}` as SSD_DOCUMENT. Predicted Minor (a cell that cannot see).
4. **Predicted verdict shape:** GO WITH FINDINGS (F-1 CLOSED; residues (a)–(c) + the G-REV gap ticketed), unless the gate rules (a) Blocker-class. Under the cap even a NO GO ships F-1's closed instance.

## What the drafter measured (all in this folder)

| # | what | instrument → output | result |
|---|---|---|---|
| P0 | head, delta, trees, checkout | `git_read.sh` → `.out` 07:29:17; `bounds.sh` → `bounds_start.out` 07:34:32, `bounds_mid.out` 07:51:52, `bounds_devmove.out` 08:02:10, `bounds_end.out` 08:17:37 | head `9ba0caf78` = branch = pull/1014/head ×5 readings; only parent `616c766a5`. r1→r2: 3 files (verification.ts +6 −2 one hunk, enforcement.ts +3 −3, test +75 −5). develop `eb1051fd3` → **`7e89318bc`** between mid and devmove. Checkout: porcelain 0, config sha `d7e7298b…` ×5, worktrees 110/111 ×5, branch `feature/ks-597-b-caller-scoped-externalref` ×5, **refs 905 ×4 → 906 at end** (not the drafter; likely the #1016 merge fetch, unproven). `.vite`: results.json 5,907 b @ 01:02:02 ×5; newer entries 0 ×5 (control, any age: 8) |
| P1 | GitHub | `derive_reads.py` → `gh_read.py/.out` 07:32:47–07:34:10, `devmove_read.out` 08:02:14 | PR open, 2 commits, 3 files, +447 −3; closing phrases 0 (controls 1/1/0); KS-1187 ×0; at-mentions 0 (6 raw `@`: 4 hunk headers, 2 e-mail); compare develop...head `e0f41a8fa` ahead 2 behind 2 → **behind 3 after #1016**; 18 JUDGED blobs at develop / head / #1016; #1016 was the only open PR sharing a file. #1016 merged `7e89318bc`, tree `e09ede17e`, one parent `eb1051fd3` |
| P2 | Linear | `linear_read.py/.out` 07:34:10 | pull/1014 → KS-1176 `contributes` only; KS-1176 In Progress (2 comments); KS-1187 / KS-1190 / KS-1195..1198 Backlog, 0 attachments; controls pull/1011, pull/1015 merged, pull/1016 open (at 07:34) |
| P3 | substrate | `drafter_setup.py/.out` 07:35:11–45, `drafter_setup_devmove.py/.out` 08:02:44–58 | clone `--shared`; worktrees base / r1 / head / dev / merged, then dev2 / merged2. **Per-entry farm only** (Dev 987, api-gateway 8, shared 8) ×7, **wholesale links 0**, shared dist rc 0 + IN TREE ×7. merge-trees in the clone: head×`eb1051fd3` `1372b3b66`, head×#1016 `591ac8451`, `eb1051fd3`×#1016 `e09ede17e`, (head⨝`eb1051fd3`)×#1016 `5748a1d68`, **head×`7e89318bc` `5748a1d68`** |
| P4 | suites + red-before-green | `drafter_run.py suite/rbg` → `drafter_suites.out` 07:36, `drafter_suites_devmove.out` 08:03, `drafter_rbg.out` 07:37:14 | see BLUF; superseded dev `eb1051fd3` 51/419, merged 52/437. r2 test in r1 tree 18/1 red (F1) = READY; in base tree 18/5 red |
| P5 | tampers | `drafter_tamper.py` → `drafter_tamper.out` 07:37:50–07:39:19, `drafter_tamper_spell.out` 07:43:33–08:04 | 10 rows, anchor 1 + marker 1 + tsc 0 + 49/428 + restore sha-identical each; see prediction 3 |
| P6 | spelling census (items 1, 3) | `qa1014r2-drafter-spellings.test.ts` + `drafter_run.py spell` → `rows_spell_*.json`; `drafter_spell_compare.py/.out`, `drafter_spell_table.out`, `drafter_spell_counts.out`, `drafter_spell_compare_head_merged2.out` | 7 principals × 55 shapes on base / r1 / head / merged / merged2 / headTF / headG-REV / headG-BOTH; planted V1 flagged, clean refusal not flagged |
| P7 | level census (item 2) | the round-1 GATE's harness + oracle copied verbatim (`qa1014-gate-census.test.ts` sha `be59a3ae8272`, `r1gate_compare.py`) → `rows_census_*.json`, `drafter_census_compare_*.out` 07:45–07:49, 08:04 | see prediction 1; F-2 reproduces (201 ×5; control 429 on 3rd); F-3 collided on the merged run |
| P8 | comment-only by parser (item 4) | `drafter_commentonly.js/.out` 07:50:56 | enforcement.ts printed + kinds identical; type-only control flagged; comment control not; test header alone comment-only |
| P9 | including tsc + eslint (item 6) | `drafter_tsc.py/.out` 07:51, `drafter_tsc_merged2.out` 08:08 | 30/10 on base, r1, head, merged; NEW 0; plant +1. Post-landing dev and merged 31/11: the +1 is #1016's ks1072 test TS18046, NEW vs dev 0. eslint 0/0/5 (verification.ts 5 at base = r1 = head; count only); controls fire |
| P10 | spec (item 9) | `spec_read.out` 07:53:34 | `DocumentCreateRequest` has no `type`; security bearerAuth only; 403 text omits the allow-list refusal; predicted NOT APPLICABLE |
| P11 | launcher | `gen_launcher_1014r2.py` → `gen_launcher.out` 08:07:37; `check_launcher.sh` → `check.out`; `controls_check.py` → `controls_check.out` | see BLUF |

## Disagreements with the READY

1. **"the key enforcement reads (enforcement.ts:100)" / PR body "enforcement and originate resolve `documentType || type`".** At the gateway, true (126 same / 0 mismatch). At originate it is only half true. By READ, originate stores `documentType || type || 'DOCUMENT'` (`:565`), but it SERVES `data.documentType` first (`:311`, `:1053`), and the gateway's verify gate matches on what originate serves (`verification.ts:546`, `:551` merged). A restricted connector can therefore put a disallowed served type into `data.documentType`. That is 201 at head and r1, 403 at base for the typed variant, and 201 at every tree for the untyped variant. The brief makes this the gate's first ruling (disagreement 1).
2. **F4 "untyped → 201, as at base".** True at the gateway, but F4's allow-list `['DOCUMENT']` coincides with originate's default. For `['SSD_DOCUMENT']`, untyped bodies and ignored keys are persisted as DOCUMENT (16 rows, base = head). The cell cannot see it.
3. **R9 "a case-only variant … refused 403: the allow-list compares exactly; fail-closed, not changed".** Confirmed, and wider than case: catalogue ids and whitespace are refused too. The allow-list is exact, while enforcement matches case-insensitively and by id. Result: 22 false refusals at head on `type`, versus 9 at base on `documentType` only. "Not changed" holds against base; against r1 these went 201 → 403.
4. **Tamper table: agrees exactly** (all 7 rows, 49/428, tsc 0). The READY's rows cannot show that no cell pins precedence (G-REV 0 red).
5. **R7 "#1014 × #1016 clean":** agrees (and it held: the merge onto the landed `7e89318bc` is clean, `5748a1d68`). Superseded as a prediction by #1016 landing.
6. **R5 eslint "the same 5 pre-existing warnings as base":** the counts agree (5 = 5); rule identity was not compared by the drafter (the brief asks the gate to).
7. **Not in the READY:** a STRING allow-list is a substring match (disagreement 2), and it is widened by #1014.
8. **Commission wording, item 2, "any row that differs from round 1's head = a finding":** 32 rows differ by construction. Each is the closed F-1 instance (→ 403 FORBIDDEN), and round 1's oracle labels them VIOLATION. The brief tells the gate to add the F-1 class to its oracle with a planted admission control.

## Every deviation from the round-1 set / the #1011 round-2 pattern

- **Launcher template:** the #1014 ROUND 1 launcher itself (`launch_qa_secuura_ks1176_1014.sh`), plus the round-N exits 24/25 from the #1011 round-2 launcher.
  - **Two forms.** The first form pinned `eb1051fd3` with #1016's blobs pre-cleared; it is kept as `gen_launcher_1014r2.first-form-pin-eb1051fd3.py`, `gen_launcher.first-run-pin-eb1051fd3-superseded-by-1016-landing.out`, `launchers/launch_qa_secuura_ks1176_1014r2.sh.pre-080737` and `check.first-run-develop-moved-7e89318bc-1016-landed.out`.
  - The second form was made from the first by `edit_gen_second_form.py` (20 asserted anchors). Its generator run had 31 asserted substitutions, a residual guard, output controls, heredoc parity (PYJ parens 119/119, 0 apostrophes), a no-git-write check, a control-byte check and `bash -n` rc 0.
- **NEW guard mechanism (deliberate, Wednesday's 08:04 item 2):** `routes/verification.ts` is judged by REGION content, not only by blob.
  - At an unpinned blob it clears only if the connector allow-list block + verify-gate region hash to `70426094413b…`. That hash was measured identical on base, r1, `eb1051fd3` and `a7a6d4605`; head's region hash is `84cd74b69b53…`.
  - Test hook: `QA1014R2_VERIF_FILE` is `--check`-only, and a launch with it set refuses (exit 16, by READ).
  - The region-clear arm is proven on REAL API raw content by N8 and on a fixture by P12. The refuse arm is proven by N10 and N11 (fixtures).
- **JUDGED 18 files:** round 1's 16, plus the ks1072 test, plus originate `routes/documents.ts` (item 3 stands on it). Its GUARDED list adds originate `documents.ts`. `DEV_CONTENT_ALLOWED` is empty.
- **LANDED:** enforcement.ts / ks1176 test at round-1 OR round-2 blobs; verification.ts at `6bd095f62` or the merged `28fb58343`.
- **Brief:** Wednesday's nine items in order, plus 10 (CLOSED / STILL OPEN / NEW carry-forward) and 11 (bounds).
  - It has a LEGITIMATE SHAPES table (S1–S10, S10 unruled) and six lead disagreements.
  - Time-box 40 min (a delta).
  - Report dir `…/reports/2026-09-17-ks1176-1014r2-9ba0caf78-tier1-r2/`; subject `[QA -> Wednesday] TIER 1 GATE #1014 ROUND 2 (KS-1176) 9ba0caf78 — <verdict>`.

## Outside the rules, stated

- **Kept renamed, not deleted:**
  - `drafter_commentonly.first-run-node-cwd-wednesday-typescript-unresolved.out`: node was started with cwd `/Volumes/DevMASTER/WEDNESDAY` and `require('typescript')` failed. `logs/` was checked afterwards: none at the WEDNESDAY root or in this folder. Re-run with cwd in the clone.
  - `drafter_commentonly.second-run-fs-commented-out-by-edit.out`: my edit's trailing comment swallowed `const fs`.
  - `rows_spell_*.first-run-no-keyprobe.json` + `drafter_spell_*.first-run-no-keyprobe.out`: same-key was unjudgeable without the key probe.
  - `drafter_spell_compare.second-run-unjudged-counted-as-mismatch.out`.
  - `drafter_census_compare.first-run-zsh-set-no-wordsplit-empty.*.out`: zsh `set -- $p` does not word-split; 4 empty mis-named files.
  - `spec_read.first-run-path-block-parser-missed-quoted-codes.out`.
  - `controls_check.first-run-N7-needle-LANDED-stripped-by-case-prefix.out`: a checker bug; the launcher answered 19 correctly.
- Probe copies and including-tsc configs ran only inside the drafter clone's `__tests__` / api-gateway dir and were quarantined by rename into `<clone>/_quarantine_2026-09-17/`. Tracked porcelain was 0 after every run. The r1 tree's tracked ks1176 test was replaced for red-before-green and restored (`git diff --quiet` 0).
- Drafter clone: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/1e211184-c0a0-4757-a7c5-e9b4a44dcab4/scratchpad/gate1014r2_draft_ftt6ozpv` (`drafter_paths.json`). Checkout worktree count 111 before and after both setups.
- **Not done by the drafter:**
  - `docker info`;
  - a real originate (all originate claims are READ);
  - eslint rule-identity compare;
  - the shared / auth suites;
  - Linear re-read after #1016 merged;
  - the key probe for types whose provider list excludes `email` (4 probe-limit rows);
  - the admin portal's actual settings payload shape.
