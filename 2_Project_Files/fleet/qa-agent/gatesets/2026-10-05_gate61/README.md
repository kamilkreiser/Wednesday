# Gateset 2026-10-05_gate61 — README for Wednesday

Drafted 2026-10-05, 06:55Z – 07:2xZ UTC (17:55 – 18:2x AEDT; times from `date -u` and each script's own header). Every figure below names the kit file it came from.

## 0. What this gate is, and its status

**gate61 is a T1 gate over ONE Secuura/Blockchain PR: #1383, KS-1401, "migration 049 restores tenant isolation where 039 is already recorded".**
- Author AND merger: Seat F 2nd, pane `Secuura/Blockchain-F`. GO string: `GO (Seat F 2nd): merge 1383 on gate61`.
- **The head is SINGLE-PARENT on develop** (no merge-in):
  - head `7eccb131f2d627a628d41b2cd537e81ce9e52fc4`, branch `feature/ks-1401-tenant-isolation-after-039-f2-1`
  - parent `46c3e20cfbd2` == develop (read 06:55:59Z by the drafter's ls-remote, == Wednesday's 06:54:27Z)
  - END_TREE `b393b20f29b44be8e53a3258193c803cb4e6fb26` (valid while develop is unmoved)
- **Exactly 4 paths differ from develop** (`c1_pr1383_ex1.out`): 049 +213 (100644), the suite +320 (**100755 in the tree**), flow doc +101/−1, cheat doc +40/−1. The two "−1"s are a finding (D4).
- Q-M for a LATER merge-in = gate57/59's M1-M4 extended to **M1-M7** (kit `q_m`): adds M5 develop moved forward, M6 develop's advance path-disjoint from `Blockchain/Dev/migrations/`, `scripts/__tests__/ks1401*`, `docker/init/` and every charge_events writer file (kit `writer_files`), M7 one new commit. Judged by `c4_docs_gate61.py qm`.

**Status: KIT COMPLETE, NOT LAUNCHED.**
- Every checker has a positive control and must-fail tamper arms; every `--selftest` was run and all arms fire (section 3).
- **Not run by the drafter, by commission:** PostgreSQL. `c3_run_gate61.py` suite / redfirst / tamper / legs / ks949 and `c3b_probe_gate61.py probe` have only been exercised by their judges on SYNTHETIC outputs. Their first real run is the gate's: an instrument trip is fixed and resumed (the prompt says so).
- The live dry run (section 5) returns rc 0 and reports only the routing line as missing.
- Two things are Wednesday's: the routing line (section 4) and the launch (section 7).

**What the drafter did:**
- Wrote only into this directory and into `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4633ab20-117b-4d2e-a571-ce5d0598b988/scratchpad/g61/`.
  - That scratch holds a `git clone --shared --no-checkout` of the checkout (`clone/`), origin set to `git@github.com:Secuura/Distributed_Secuura.git` with the checkout's own `core.sshCommand`.
  - ONE fetch into it (06:56:30Z): develop, `refs/pull/1383/head`, `refs/pull/1381/head`, `refs/pull/1382/head`.
  - c4's self-test wrote SIM commits / trees / blobs into THAT clone's object store only (commit-tree / hash-object / a temp index; no ref).
  - No worktree, no npm install, no PostgreSQL.
- In `/Volumes/DevMASTER/!CODING/`, ran only read verbs: `ls-remote`, `config --get`, and the `clone --shared` source read. Hashed (read) the gate57 / gate59 reports.
- Network: GitHub REST GETs only (pulls/1383, files, the open-PR census). GH_TOKEN read by name, never printed. No Linear read (X8 is the gate's).
- Not done: no launch, no routing edit, no mail, no comment, no ticket change, no `rm`. Python wrote `__pycache__/` here on import, as gate57/59's kits did.

## 1. Drafter predictions on #1383 at 7eccb131f2d6 over develop 46c3e20cfbd2 (the gate re-derives every one)

| check | file | result |
|---|---|---|
| C1 pin | `c1_pr1383_ex1.out` (rc 0, 10/10) | ls-remote pull/head == branch == API == input; open, base develop == ls-remote develop; ONE parent == develop; 4 paths with exact +/- by numstat AND API; END_TREE equal (control: develop tree `dab6adb69ea3` differs); `%(trailers)` raw **1 byte** (`\n`), control `bf277eead268` **55 raw bytes**; subject 78 chars, `(#` 0; ONE `Refs KS-1401`, only KS-1401 hyphenated (KS 1376 de-hyphenated); `ls-tree` modes suite 100755, 049 + docs 100644 |
| C2 migration | `c2_pr1383_ex1.out` (rc 0, 13/13) | L0: **64 live lines** after stripping `--` and `/* */` (139 comment lines removed; raw 214); ONE DO block, nothing live outside; `set_config('lock_timeout','5s',true)` before the first ALTER; 0 SET NOT NULL; `IF NOT EXISTS(information_schema.tables) THEN RAISE EXCEPTION`; must-not counts all 0 (the `/* Down */` block's DROP POLICY / NO FORCE / DISABLE prose is NOT counted); ONE UPDATE, `SET tenant_id = $1 WHERE tenant_id IS NULL` exactly; the array == the 4 tables; the `$p$` policy literal **byte-equal to 039's** (sha256 `798b85ba1c4f…` both); 049 the only migration change (038a `e835095a6113`, 039 `eb0909b4e259` unchanged); sorts after all 50 `.sql` at develop. 049 sha256 `6ad3a01ac2780218…` == the READY's restore hash. INFO: CREATE POLICY `ON %I` vs ALTER/DROP `public.%I`; the backfill runs under any existing FORCE (D3) |
| C3 run | NOT RUN (commission) | judges proven on synthetic outputs only (`c3_selftest_ex1.out`). The kit's expected strings were checked against the suite's own `ok`/`no` messages at the head (all present; the `$tbl …` ones by reading). Tamper anchors each occur exactly once in 049 |
| C3b probe | NOT RUN (commission) | judge proven on synthetic readings (`c3b_selftest_ex2.out`) |
| C3b census | `c3b_census_ex2.out` (rc 0) | at the head: **WRITE 2**: `originate/src/services/chargeEvents.ts:180` INSERT (via `prisma.$executeRaw`, the GUC proxy) and `originate/src/services/gdprService.ts:561` DELETE (runWithPlatformScope within 60 lines); **DDL 2**: `api-gateway/src/startup-migrations.ts:332`, `originate/src/index.ts:458`; **CALLER 6**: `originate/src/routes/certifications.ts:593 596 1219 1357` (tenant arg `tenantId`) and `:966 :1071` (`getReqTenantId(req)`); READ 3. `routes/metering.ts` and `api-gateway/src/routes/proxy.ts` carry **no** charge_events write (comments / an import only). CONTROL: 15 `billing_charge_events` lines in services/billing all EXCLUDED, 0 WRITE |
| C4 docs | `c4_docs_ex2.out` (rc 1, **5 FAIL of 21**) | PASS: D1 §4, D2 same commit, D3a one block per doc (100 / 39 lines at develop's close tag), D4 numbers [1..12, 22] + h3 22.1, D5 nothing renumbered, D6a cheat order, D7 flow self-contained, D8 timings (the `5 s lock_timeout` skipped by name), D9 the zero (0 hits at develop). **FAIL: D3b ×2 (close tag rewritten), D6b (cheat convention), D7 cheat ×2 (no live sweep, no NOT-covered note)** — carried as the self-test BASELINE (D4, D5) |
| C4 predict | `c4_predict_develop_ex1.out`, `c4_predict_sim1381_ex1.out` (rc 0) | real develop: merge clean, prediction == END_TREE `b393b20f29b4` (positive control). SIM (#1381's merge-in tree `ba3527224ff6` squashed onto develop as `0c240a056320`): conflict on EXACTLY the two docs; predicted merge-in tree **carry `5361ecd240c304dcf72454c2b0d9d35d5ce4cf8c`** / keep `d9bdf8ba1d474425703af921f556dabe26d9060d`; 13. above 22. in both docs; CONTROL 22-above-13 `ce750989e176` differs. Recompute on the REAL develop |
| C5 PR text | `c5_pr1383_ex1.out` (rc 1, **1 FAIL of 8**) | PASS: one Refs + URL; only KS-1401 hyphenated (KS 1054 / 1376 / 4 de-hyphenated); title == subject; `## Test Evidence`; "NEVER reaches demo" + kintsugi deploy; figures 53/0, 11 cells, 100755, `22.`, 15.14; not-covered names apply round + live sweep. **FAIL T2: "This does not close KS-1401 or KS 1376 as Done."** (D1). Body 10,155 B / 10,082 chars, sha256 `fc18d2c9a748b6fe…` == the READY's |
| C6 NOT COVERED | `c6_pr1383_ex1.out` (rc 0, 2/2) | one `## Not covered / owed`; all six required items in it. INFO: column nullability ABSENT; "applied to no real database", originate's GUC, 038a, gateway-runner are ELSEWHERE in the body |
| census | `census_ex2.out` (rc 0, 07:1xZ) then the dry run (07:21Z) | 23 → **24** other open PRs; **0 add or change a migration** (049 uncontested); CONTROL FIRES on #1383; EXPECTED OVERLAPS: #1381 + #1382 (both docs), **#995** (KS-741, `originate/src/index.ts`, the tenant-middleware file; `reported_overlaps` with `writer_ok`, the gate reads its patch), and **#1384** (KS-1210, Seat E 3rd, head `852fc9276320`, block 18., raised between the census and the first dry run, which refused rc 15 on it: `dry_console_ex1.out`; added to `reported_overlaps`) |

**Drafter's reading:** every artefact figure in the READY that the kit can read without PostgreSQL reproduces (head, develop, END_TREE, 4 paths, +674/−2, 100755 in the tree, 78-char title, trailers 1 byte vs control 55, body sha256 and 10,082 chars, one Refs, the restore hash `6ad3a01ac2780218`, 49 → 50 main-DB migrations: 50 `.sql` at develop of which one is `003_platform_tenancy.sql`). The open items are below.

## 2. Doubts for the GATE to rule (the prompt carries D1-D8), and READY contradictions

- **D1 CLOSING WORD (C5 T2).** The body's not-covered section opens "**This does not close KS-1401 or KS 1376 as Done.**" Linear's magic-word parser does not read negation: "close KS-1401" is a closing reference, so the merge may move KS-1401 to Done — exactly what §5f and the brief forbid. The READY's "0 auto-close refs (keyword + #n)" only looked for `#n`. A body edit fixes it without a new head. Block, or a pre-merge condition on the GO?
- **D2 charge_events writers under FORCE + WITH CHECK (C3b census).** Every write goes through the GUC proxy (INSERT) or platform scope (DELETE), and `index.ts:245-257` defaults `req.tenantId` then seeds the ALS from it. The open question is per CALLER: is the 4th argument (`tenantId` at certifications.ts:593/596/1219/1357, `getReqTenantId(req)` at :966/:1071) ALWAYS the ALS tenant? If a route writes for a different tenant (e.g. the issuer's), WITH CHECK refuses that billing INSERT after 049 on any non-bypass box: STOP-class (brief finding 3). Source-read only; no service is started.
- **D3 The NULL-only backfill runs UNDER an existing FORCE.** The UPDATE comes before 049's own ENABLE/FORCE, but certifications / oauth_apps / svc_webhooks are already forced (kintsugi: certifications forced with 0 policies). Applied by a non-superuser, non-BYPASSRLS OWNER, the UPDATE sees 0 rows and 049 prints "had 0 NULL rows; no data was written" — false. kintsugi's migrating role is UNMEASURED (P9); those three tables hold 0 rows there (B 50th), so it is harmless THERE, not in general. The author's suite applies 049 only as superuser. Probe X7 measures it.
- **D4 `  </body>` rewritten as `</body>` in BOTH docs (C4 D3b).** The "−1" of each doc: an edit to an existing line that #1381 and #1382 both anchor on (they keep `  </body>`). The READY says "my blocks sit immediately before the single `</body>`" — true, after rewriting it. Consequence: a later merge-in has two plausible trees (carry `5361ecd240c3…` / keep `d9bdf8ba1d47…` on the SIM). Rule: polish, or restore before #1381's merge-in (a new head, re-gate)? And which close tag Q-M accepts (kit default carry).
- **D5 The cheat block (C4 D6b, D7).** Numbered `22.` (the cheat convention is unnumbered `… &mdash; KS-n</h2>`), not wrapped in `<div class="section">` (KS-1404, KS-1333 and #1381's KS-1345 are), key first; and not self-contained: no §5f / live-sweep line, no NOT-covered note. Also both h2s are indented 6 spaces where the doc uses 4. gate59's report rules the same class for #1382: precedent.
- **D6 Brief COMPLETION (ITEM 3).** Not in the suite: 3.6 the gateway-runner shape (runStartupMigrations twice; CORE after 049 keeps the certifications policy — the body says source-read); 3.1 the `pg_proc` diff; 3.7 the ADD-COLUMN-guard sabotage and the owner-role FORCE arm. The suite's FORCE tamper reds a FLAG reading only — secuura_app is not the owner, so FORCE has no behavioural effect on any of its arms. Probe X5 / X8 / X9 cover FORCE, the fresh shape and pg_proc; the gateway runner stays unmeasured unless the gate runs ks949 / runStartupMigrations. Is T1 met?
- **D7 The "must-hit control 54" (C4 D9).** The docs claim "both platform-k documents contain 0 mentions … must-hit control `Schemathesis` returning 54". The zero reproduces over both docs; the 54 reproduces ONLY as `grep -c -i Schemathesis` on the FLOW doc alone (both docs: 152 lines `-i`, 115 case-sensitive). Scope mismatch in client-facing docs: polish.
- **D8 Information unless the gate finds otherwise.** (a) "Never demo" is a ruling, not a mechanism: once 049 is on develop ANY gateway boot applies it at stage 1; Wednesday's demo hold is the only guard. (b) CREATE POLICY `ON %I` resolves through search_path while every other statement names `public.%I` — byte-faithful to 039, harmless unless a runner's search_path differs. (c) `lock_timeout` is set transaction-locally inside the DO block; probe X12 measures it under psql, the gateway's pool is unmeasured. (d) #995 touches the tenant-middleware file.

**READY contradictions / notes (none blocks the artefact):**
1. "0 auto-close refs (keyword + #n)": a keyword + `KS-1401` closing phrase exists (D1).
2. "My blocks sit immediately before the single `</body>`": the close tag itself was rewritten (D4); "nobody renumbers" holds (D5 PASS).
3. "pathgatef2 … C1 C2 C3 all FAIL" reads as its controls firing; not re-measured (the gate's C1 P4 is the path census).
4. Consistent: head, develop, END_TREE, 4 paths +674/−2, mode, title, trailers, body hash, restore hash, 049 uncontested (census 0 migrations), the 50 vs 49 migration count.

**For Wednesday (not the gate's):**
- **W1 sequencing.** #1381 merges FIRST (B 61st). Once it lands, #1383 needs a docs-only merge-in (a new head) judged by `qm`; a launch after #1381 lands refuses rc 10. Launching NOW (develop unmoved) is the clean window.
- **W2** KS-1401 sits In Progress via the integration (06:50:48Z). D1 decides whether the merge would move it to Done.
- **W3** If #1384 (18.) or #1382 (19.) also lands first, the prediction is recomputed on that develop; the SIM covers #1381 only. Four PRs now append to the same two docs: every landing before #1383 adds one docs-only merge-in.

## 3. The kit's instruments (each exercised; outputs beside it as `<name>_exN.out/.err/.rc`)

| script | what it does | positive control | must-fail tamper arms (all fired) |
|---|---|---|---|
| `lib_gate61.py` | a re-keyed copy of lib_gate59: `git()` read verbs only; `wgit()` write verbs only outside `/Volumes/DevMASTER` (lexical + realpath; `G61_FORBIDDEN_ROOT` override for refusal arms); `guard_out`; GH; `move_out`; `selftest_arm` | — | (inherited from gate59, whose refusal arms were driven) |
| `c1_pin_gate61.py` | P1-P10 | `c1_pr1383_ex1` (rc 0); T0 | `c1_selftest_ex1` **15/15**: base-vs-base, 039 as a 5th path, +/- drift, a merge-in parent, a trailer, a blind 0-byte trailer control, `(#1383)`, 93 chars, a second Refs, KS 1376 hyphenated, the suite at 100644, develop moved, API head moved, a foreign `-f2-` branch |
| `c2_migration_gate61.py` | L0 + M1-M12 | `c2_pr1383_ex1` (rc 0); T0 | `c2_selftest_ex1` **23/23**: 3 stripper unit arms (`--` in a string survives; nested `/* */` removed; `--` in a DO body stripped, its string kept) + all-commented (L0), lock_timeout gone, SET NOT NULL, NOTICE-and-CONTINUE, self-insert outside / inside the block, DELETE, DROP FUNCTION, oauth_apps_auth_lookup, guard removed, top-level ALTER, second DO, 5th table, one policy byte, 038a edited, second 049_, FORCE gone, ADD COLUMN unguarded, literal table |
| `c3_run_gate61.py` | suite / redfirst / tamper / legs / ks949 | S-0, R-0, T-*-0 (synthetic) | `c3_selftest_ex1` **24/24**: SKIP, 52/53, a lying summary, the bypass control failed, a missing cell; a head arm green at base, the fixture off, SKIP at base, rc 0 at base; per tamper: reds nothing, never landed, restore not byte-equal; a dirty worktree |
| `c3b_probe_gate61.py` | probe X0-X12 / judge / census W1 | P-0, W-0 (synthetic); census real `c3b_census_ex2` | `c3b_selftest_ex2` **23/23**: 16 flipped cells (bypass role, B visible, fail-open, INSERT accepted, WITH CHECK refusing the right tenant, carve-out broken, FORCE not binding the owner, default-deny, backfill missed, fresh-shape no policy, a function changed, the lookup policy changed, a weakened qual, unstable dump, lock_timeout not honoured, a partial commit) + census: a NEW writer, a GONE writer, a NEW caller, a blind control, billing EXCLUDED. `_ex1` = history (the census control first ran on roots with no billing table → 0 → FAIL; fixed by a services/billing control grep, `c3b_census_ex1` → `_ex2`) |
| `c4_docs_gate61.py` | docs D1-D9, predict M0-M1, qm M0-M7 | `c4_predict_develop_ex1` (== END_TREE); T0 baseline-aware; T7 (`  </body>` kept passes D3); Q0 / Q0b | `c4_selftest_ex1` **18/18**: KS-1333 h2 edited (D3a), 22→23 (D4), cheat h2 gone (D6a), suite path gone (D7), host gone (D8), 12→14 (D5); Q-M on the SIM: 039 edited in the merge-in (M1 + M3), 22 above 13 (M1), a rebase (M2), a trailer (M4), develop advancing into `migrations/050` (M6), two new commits (M7), keep judged as carry (M1). BASELINE = the 5 real findings |
| `c5_prtext_gate61.py` | T1-T8 | T0 on a SYNTHETIC clean body (the real one fails T2) | `c5_selftest_ex1` **12/12** incl. T0r (the REAL body fails T2, as predicted): Refs gone, a second Refs, `Closes KS-1401`, `fixes #1383` in the commit message, KS 1376 hyphenated, `(#1383)`, Test Evidence gone, never-demo gone, 52 passed, not-covered heading gone |
| `c6_notcovered_gate61.py` | N1-N2 + N3 INFO, section-bounded | `c6_pr1383_ex1` (rc 0); T0 | `c6_selftest_ex1` **5/5**: live sweep removed, per-tenant moved above the heading, heading removed, a second heading |
| `gh_census_gate61.py` | API line + census (MIGRATION / WRITER / OVERLAP / EXPECTED) | `census_ex2` (control FIRES on #1383) | `census_selftest_ex2` **8/8** (`_ex1` 7/7 before the `writer_ok` arm was added) |
| `fill_gate61.py` | fills prompt + launcher + pins; refuses a changed READY / brief / gate57 report, a moved head / develop | the dry fill | (gate59's refusal arms, re-keyed; not re-driven) |
| `launcher_gate61.TEMPLATE.sh.txt` | gate59's launcher re-keyed: compare ahead **1** / behind 0 / 4 files; 34 keywords; the new phrase checks | SIM `--check` in the dry run | (gate59's arms; not re-driven) |
| `repin_and_launch_gate61.sh` | the launch action | `--dry-run` (section 5) | rc 9 / 11 / 10 / 15 paths as gate59 |

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1401-1383|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. Dry run and refusal arms
- `dry_console_ex1.out` (07:21:14Z) **rc 15**: the census refused on #1384 (KS-1210, opened after the drafter's census). Added to `reported_overlaps`.
- `dry_console_ex2.out` (07:22:10Z) **rc 0**: routing line reported missing (not refused in a dry run); API + ls-remote agree with the input head; develop unmoved; census clean (4 expected overlaps, 0 migrations, control FIRES); SIM fill `dry072210.SIM.*` (34 keywords, prompt sha256 `76724dabd74cb669`); race re-read clean; the SIM launcher's `--check` rc 0 (compare ahead 1 / behind 0 / 4 paths).
- `refusal_arms_ex1.out`: the SIM launcher refuses a stale pin (9), a moved develop (17), a moved head (6), a launch with no TTY (21, before `exec claude`); the repin refuses a wrong PR (9) and a short sha (9).
- Final selftest sweep 07:2xZ (scratch `g61/final/`): c1 15/15, c2 23/23, c3 24/24, c3b 23/23, c4 18/18, c5 12/12, c6 5/5, census 8/8, each rc 0 and `CHECKED n` > 0.
- All `*.SIM.*` and `pins_gate61.SIM-*.json` files are exercise output and are never launched. The real `pins_gate61.json` does not exist until the real launch writes it.

## 6. Re-draft recipe (the head or develop moved)
1. Re-fetch into a scratch clone.
2. Re-measure kit `head`, `end_tree`, `develop`, `develop_tree`, `files` (+/-), `modes`, `blobs`, `flow_numbers_*`, `block_lines`, `pr_body_read`, `reported_overlaps` (re-run `gh_census_gate61.py --json`), `writer_census_expected` (re-run `c3b … census`).
3. Re-run every `--selftest`, then c1, c2, c4 docs + predict, c5, c6, and a `--dry-run`.
4. A docs-only merge-in after #1381 lands is NOT a re-draft of the verdict: it is a NEW head judged by `c4_docs_gate61.py qm --merge-in-head <M> --develop-after <develop> [--anchor carry|keep]` (M1-M7). The launcher itself refuses a moved develop (rc 10 / 17); launch the gate before #1381 lands, or re-draft.

## 7. How Wednesday launches it (after section 4's routing line)
The pane is `QA/Secuura-ks1401-1383`. The report dir is `…/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1401-1383-g61/`. The GO the gate expects is `GO (Seat F 2nd): merge 1383 on gate61`. The verdict subject is kit `verdict_subject_template`.

Exit codes:
- rc 1: routing.
- rc 9: input.
- rc 11: the head moved, or is not the kit head.
- rc 10: develop moved (#1381 landed: merge-in + `qm`, or RE-DRAFT), or the fill refused.
- rc 15: an overlap outside reported_overlaps, or a reported overlap's head moved (#1381 / #1382 / #1384 / #995).
- rc 12 / 13 / 14 / 16: usage gate / `--check` / cockpit / override.

Add `WED_USAGE_STOP=…` only with Kam's recorded authority.
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate61/repin_and_launch_gate61.sh 1383 7eccb131f2d627a628d41b2cd537e81ce9e52fc4 --dry-run
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate61/repin_and_launch_gate61.sh 1383 7eccb131f2d627a628d41b2cd537e81ce9e52fc4
```
