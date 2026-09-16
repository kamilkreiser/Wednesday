# DRAFTER REPORT — #1014 (KS-1176) TIER 1 ROUND 1 gate set @ 616c766a57a51238450c99bbf1d59bb109e3841c

Drafted 2026-09-17 06:11–06:35 AEST (clocks from `date`) by a Wednesday drafting subagent. Nothing was launched and no pane was opened. The launcher ran with `--check` only. Nothing was merged, pushed, commented, filed or mailed. No git write verb touched the Secuura checkout.

## BLUF

- **The set is ready.**
  - Brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1014-ks1176-tier1.md` (sha256 `ccfe67ec37285aa1`)
  - Prompt: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-17_secuura-1014-ks1176-tier1.prompt.txt` (`b50f0de81169fb4a`)
  - Launcher: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_secuura_ks1176_1014.sh` (mode 755, `61aa7c5df06ca287`)
- **`--check` rc 0** at 06:30:08–36 (`check.out`) on the final brief and prompt.
- **10/10 negative fixtures refused**, each with its expected exit code (`controls_check.out`, 06:30:56–06:34:16): subject 23, tier 7, SHA 20, mail step 12, per-entry farm 22, head override 6, LANDED 19, unpinned blob 18, develop behind the pin 18, ROUND 1 missing 15.
- **Develop moved during the draft, as the commission expected:** #1011 landed as **`523f283c6`** (06:10:46 +1000): `audit.ts a7be8626f → 052131de0` + the three ks871 tests. It is file-disjoint from #1014 by content.
  - Merged tree: **`8589933267963afda8fc352279c4b694ed5bb3de`** (`merge-tree --write-tree` in the drafter's clone = the tree of its local merge commit).
  - Suites: base 48/410, head 49/423, merged 52/432. The launcher pins develop `523f283c6` and clears `audit.ts` at either blob.

## Top predictions (drafter-labelled; the gate falsifies)

1. **No level-rank widening: GO-shaped on the ruling's own terms.** MEASURED, `drafter_compare.out`:
   - Base vs head: 118 of 1,040 HTTP rows differ. **Every one is an unknown-level principal on one of the 9 none-rank types.**
   - There are **0** admissions above `none`, **0** changes for known-level principals, and **0** changes at `:557` (494 verify rows).
   - Pure function: 51 of 1,089 flips, all `unknown × {'', none, NONE}`, with oracle mismatch 0.
   - Head vs merged: 0 differences.
2. **The gate's likely FINDING is a pre-existing gap this PR widens, not a flaw in the rank logic.** A connector JWT presented as `Authorization: Bearer` gets past the connector gates. MEASURED with a throwaway RS256 key:
   - The gateway does not check `type:'connector'` and sets no `connectorMeta`. The KS-480 `documents:write` scope check, `allowedDocumentTypes` and the per-key limiter's `MACHINE_AUTH_METHODS` therefore never see it.
   - Base: a **scope-less** connector JWT already gets 201 on an untyped document, and 403 on typed ones.
   - Head: it also gets 201 on all 9 none-rank types.
   - Reachability decides severity. The token is minted only at auth `/internal/connector-token` (intra-cluster, any valid sk_ key). Predicted grade: TICKET-class Major candidate / escalation, GO WITH FINDINGS, unless the gate shows it is client-obtainable.
3. **Wednesday's ruling rests on a premise that is vacuous at the only production caller.** Both routes mount `authenticateToken(true)`, so an anonymous caller gets **401** on every row and never reaches the no-user branch. MEASURED:
   - Against the lowest authenticated human (`NONE`), a `documents:write` connector key answers identically on all 40 rows at head.
   - One residual difference is new at head: a connector configured `workflowPolicy: 'bypass'` is forwarded on an approval-requiring none type where the human is workflow-gated.
   - Prediction: RECORD. The premise holds with the right comparator, and the bypass is admin-configured policy made reachable.

## What the drafter measured (all in this folder)

| # | what | instrument → output | result |
|---|---|---|---|
| P0 | head, parent, diff, trees, checkout | `git_read.sh` → `.out` 06:11:56; `bounds.sh` → `bounds_mid.out` 06:22:44, `bounds_end.out` 06:34:26 | head `616c766a5` = branch = pull/1014/head, only parent `e0f41a8fa`. 2 files: `enforcement.ts 533cd309c → 3e314ba11`, ks1176 test `5820520ae`. develop `523f283c6` at 06:11:56, 06:22:44 and 06:34:26. Checkout: porcelain 0, config sha `d7e7298b…` ×3, worktrees 110/111 ×3, branch `feature/ks-597-b-caller-scoped-externalref` ×3, **refs 902 → 902 → 904** (two refs added between mid and end — not the drafter; likely Seat A's A15 push; unproven). `.vite` unchanged; 0 entries newer than the setup (control: 12 of any age) |
| P1 | GitHub | `gh_read.py` → `.out` 06:19:49–06:20:14, raw `gh/` | PR open, 1 commit, +371 −1, 0 closing phrases (controls 1/1/0), body KS ids {1176, 1190, 256, 388}, KS-1187 absent, 2 `@` = e-mail addresses. compare develop...head: merge_base `e0f41a8fa`, diverged, ahead 1, behind 1, files 2. 16 JUDGED blobs at develop and head. 18 other open PRs, 0 exact shared files |
| P2 | Linear | `linear_read.py` → `.out` 06:20:23 | pull/1014 → KS-1176 `contributes` only. KS-1190 Backlog p3, 0 attachments. KS-1187 Backlog p1, 0 attachments. Control: pull/1011 → KS-871 `contributes`, merged, KS-871 still In Progress |
| P3 | substrate | `drafter_setup.py` → `.out` 06:15:20–32 | clone `--shared`; worktrees base / head / merged (local `--no-ff` of `523f283c6` = `6b0ce19ec`, tree `858993326`). **Per-entry farm only**: Dev 987, api-gateway 8, shared 8. **Wholesale links: 0**, and no node_modules for any other package. Shared dist rc 0, IN TREE ×3 |
| P4 | principal × type HTTP census + pure-function universe | `qa1014-drafter-principals.test.ts`, `drafter_run.py` → `drafter_probe_head.out` 06:17:44, `drafter_probe_base_merged.out` 06:17:59; `probe_rows_*.json`; `drafter_compare.py/.out`; `drafter_parity.py/.out` | See top predictions 1–3. 26 principals × 21 create codes and × 19 verify types. The harness uses the real `authenticateToken`, router, enforcement and workflow, and the real seed. Redis and upstreams are stubbed; `index.ts` is NOT mounted |
| P5 | suites | `drafter_run.py suite` → `drafter_suites.out` 06:18:05–32 | base 48/410, head 49/423, merged 52/432. All pass, pending 0; project tsc rc 0 on each |
| P6 | including tsc | `drafter_tsc.py/.out` 06:20:44–52 | 30 lines / 10 files on all three trees, 0 in the PR files, NEW 0. ks1176 is in the program on head and merged. No plant |
| P7 | gate tampers | `drafter_tamper.py` → `drafter_tamper.out` (G-ROUTE 06:21:54) and `drafter_tamper.first-run-G-ROUTE-VOID-tsc2.out` (the VOID first form + G-CTRL, 06:21:18) | G-ROUTE: 5 red, tsc 0. Its literal first form was VOID, tsc rc 2. G-CTRL: 2 red, tsc 0. Both restores sha-identical |
| P8 | spec | `spec_read.out` 06:23 | `POST /api/documents` 403 description names `INSUFFICIENT_VERIFICATION_LEVEL` / `MFA_REQUIRED` / `AUTH_PROVIDER_NOT_ALLOWED`. Security is `bearerAuth` only; `x-api-key` is undeclared |
| P9 | launcher | `gen_launcher_1014.py` → `gen_launcher.out` 06:24:5x; `check_launcher.sh` → `check.out`; `controls_check.py` → `controls_check.out` | See the BLUF |

## Disagreements with Wednesday's ruling (and the commission)

1. **"Grants nothing beyond what an anonymous caller already gets (`enforcement.ts:136-141`)."** At the only production caller the premise is vacuous: `authenticateToken(true)` answers 401 first, and the no-user branch has no production caller. The brief keeps the question, supplies the operative comparator (a `NONE` human), and asks the gate to rule. The same sentence is repeated in the **product why-comment** (`enforcement.ts:59-60`), a comment-accuracy Record for the gate.
2. **Commission item 1 lists "the gateway JWT default 'BASIC' at `:146`".** `auth.ts:146` is the **test-token** default (dev/test + `ENABLE_TEST_TOKENS` only). The RS256 path takes `verificationLevel` verbatim, and `enforcement.ts:151` defaults an absent claim to `'none'`. Human access tokens carry mapped enum levels (`mapDbVerificationLevel` sends unknown values to `'BASIC'`), so no production human carries an unknown level, by source.
3. **"The fix must open ONLY none-level types. Any wider opening = Blocker."** On LEVELS this holds, as measured. The connector-JWT Bearer path (top prediction 2) opens those none types to a principal **with no scope**. That is a widening on a different axis, which the Blocker rule does not name. The brief sends it to the gate as L11 "the row nobody ruled", with the drafter's grade.
4. **"SSD_DOCUMENT" framing.** DOCUMENT and **PROPERTY_DEED** are also seeded at `none`, so connector keys now create all three. This is within the ruling but belongs in front of Wednesday / Kam as a product question.
5. **KS-1190 scope.** The unknown-level fail-open also exists at the verifier gate `:557`: an off-canonical verifier level passes every authenticated principal, measured at base and head. KS-1190's title names only the creator path; the drafter did not read its description text.
6. **Catalogue fill (commission item 5).** `platform.ts:880-894` writes Postgres `document_type_configs`, which the gateway enforcement never reads: `getAllDocumentTypes` reads Redis `doctype:*`, filled by `admin.ts:633/691/706/732`. There are two catalogue sources and no traced bridge (READ).

## Disagreements with the READY

1. "13 test files mock `meetsVerificationLevel: () => true`": `git grep -l` lists 15 files at head, including ks1176 and `enforcement.test.ts`. The mock count needs a parser. Not a defect.
2. "0 at-mentions": true. The 2 `@` in the body are e-mail addresses.
3. C8 "the spec already lists 403 `INSUFFICIENT_VERIFICATION_LEVEL`": true. The spec also does not declare `x-api-key` on the operation, which is a Record.
4. The READY's route cells use a fake `authenticateToken` that injects `req.user`. They cannot see the Bearer connector-JWT principal or the scope-gate ordering (top prediction 2).
5. The E control "a connector key verifying a verifier-`none` type is not refused" cannot see the `:555` skip being removed, because the fix makes the comparison pass anyway. Predicted 0 red; not measured by the drafter.
6. The READY's `:53-64` and the ruling's `:53-57` / `:136-141` / `:554-557` are base numbering for the helper. At head the no-user branch is `:143-148` and the level check `:152`. `:557` is unchanged, because `verification.ts` is untouched.

## Every deviation from the #1011 round-2 / #1013 sets

- **Launcher template:** `launch_qa_secuura_ks999_1013.sh`, the newest ROUND 1 tier-1 launcher with the ABSENT arm, not the round-2 launcher. Round 2's exits 24/25 are round-N rules that do not apply to a round 1.
  - Generated by `gen_launcher_1014.py`: 22 asserted substitutions, a residual guard with two named permitted mentions, output controls, heredoc parity, a no-git-write check, a control-byte check and `bash -n`.
  - **Four refused generator runs are kept, renamed:** override count 10 ≠ 8, permitted-mention residuals, permitted count 2 ≠ 1, SHA control count 2 ≠ 1. Each expected count was corrected to the measured one and the reason recorded.
- **JUDGED:** 16 files. `audit.ts` clears at `a7be8626f` or `052131de0`.
- **GUARDED:** past `523f283c6`, a PREFIX guard on `services/api-gateway/src/` (any gateway source change refuses), plus the level copies' directories, the auth connector-JWT mint / internal route / authenticate / types, the frontend copy, shared crypto, `docs/openapi/`, eslint and the lockfile.
- **Negative fixtures:** the 6 commissioned plus 4 more (LANDED 19, unpinned blob 18, behind-the-pin 18, ROUND 1 15).
- **Trees:** base = PR parent `e0f41a8fa`; merged against `523f283c6`, which already contains #1011.
- **Brief items:** Wednesday's twelve kept in order, plus item 13 (disjointness / develop moves). The LEGITIMATE SHAPES table (§2a) is filled because the level check is a checker: 11 rows, L11 unruled.
- **Report dir:** `Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1176-1014-616c766a5-tier1-r1/`. Subject: `[QA -> Wednesday] TIER 1 GATE #1014 (KS-1176) 616c766a5 — <verdict>`, from coagent@.

## Outside the rules, stated

- **The round-2 drafter's wholesale-link slip was NOT repeated:** 0 wholesale links (`drafter_setup.out`).
- Probe copies were placed in the clone's `__tests__` only and quarantined by rename into `<clone>/_quarantine_2026-09-17/` after each run. The suites ran after quarantine, as the 49/423 denominator confirms. The including-tsc configs were quarantined the same way.
- Tamper edits ran only in the drafter clone's head worktree, restored by `git checkout --` in that worktree with sha256 asserted.
- `merge-tree --write-tree` ran only in the drafter clone, never in the checkout.
- `git_read.sh` wrote `git show` stderr to `src/show.err` (0 bytes), not `/dev/null`.
- Renames, not deletions: `drafter_tamper.out` → `drafter_tamper.first-run-G-ROUTE-VOID-tsc2.out`, and the four `gen_launcher.*-refused.out`.
- `linear_read.py` was derived by `sed` from the round-2 set's script (2 substitutions, counted); it also reads pull/1011 as a control.
- Drafter clone: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/76d545ac-4e62-4400-be44-c9ce11c3c344/scratchpad/gate1014_draft_b8tl6bvm` (`drafter_paths.json`).
- **Not done by the drafter:** `docker info`; the real `index.ts` app (rate limiter, middleware chain); originate's persistence READ; the E-control tamper; the seat's T-rows; eslint; a planted including-tsc control; KS-1190's description text; whether a connector JWT is client-obtainable.
