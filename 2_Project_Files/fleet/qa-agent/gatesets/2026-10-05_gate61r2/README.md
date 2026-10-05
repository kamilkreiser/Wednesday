# Gateset 2026-10-05_gate61r2 — README for Wednesday (gate61 ROUND 2)

Drafted 2026-10-05, 09:23Z – 09:5xZ UTC (20:23 – 20:5x AEDT; times from `date -u`, the API reads and each run header). Every figure below names the kit file it came from.

## 0. What this gate is, and its status

**gate61 ROUND 2 is a T1 re-gate of ONE Secuura/Blockchain PR, #1383 (KS-1401), NARROWED to ONE commit:** the N-1383-1 fix.
- Author AND merger: **Seat F 3rd**, pane `Secuura/Blockchain-F`. Seat F 2nd wrapped and is never addressed.
- The commit: head `32e8459bc0f51d1af492aae7c0b3d9754f78c9bf`, ONE parent `7eccb131f2d6` (round 1's GO head, a fast-forward), tree `8ba2c0c8e9d1313663b408973e914cb917fadb78`, branch `feature/ks-1401-tenant-isolation-after-039-f2-1`.
- Subject: `KS-1401: 049's backfill takes the platform bypass so a non-bypass owner fills NULLs` (83 chars).
- 4 paths, +127/-4 (`ex/scope_ex1.out` S3): 049 +22/-0, suite +60/-0, flow doc +22/-0, cheat doc +23/-4.
- **develop has MOVED since round 1:** `46c3e20cfbd2` → `f01c1da5717f` = #1381's squash (KS-1345). So there is **no single-parent END_TREE** any more; the landed tree will be a docs-only merge-in's.
- **Merge order (Kam, card `secuura-ks1404-anchors-before-049-merge-order-1005` = a, 19:52:52 AEDT):** #1383 merges only AFTER Seat D 8th's KS-1404 anchor-wiring PR. develop moves again first. The verdict therefore GOes the commit and covers the later merge-in only under Q-M, via `qm_gate61r2.sh`, with close tag `keep`.
- Tier T1, migration on live data: the gate applies 049 **only to throwaway databases it creates**.

**Status: KIT COMPLETE, NOT LAUNCHED.**
- Every instrument has a quiet case and firing arms, and all were run (section 3).
- The live dry run (`ex/action_dry_quiet_ex1.out`, 09:43:37Z) returns rc 0. It reports only the routing line as missing.
- Two things are Wednesday's: the routing line (section 4) and the launch (section 5).

**What the drafter did:**
- Wrote only into this directory: `api/` (PR reads), `ex/` (exercise outputs), `dry_*` / `launch_094349.*` (exercise outputs of the launch action), `_quarantine/` (empty).
- In `/Volumes/DevMASTER/!CODING/`, ran only read verbs: `ls-remote`, `log`, `show`, `diff`, `ls-tree`, `cat-file`, `rev-parse`, `rev-list`, `merge-base`, `config --get`. Every object needed (32e8459, 7eccb131, f01c1da5) was already in the shared store, so nothing was fetched and no clone was made.
- Network: GitHub REST GETs only (pulls/1383, twice). GH_TOKEN was read by name and never printed.
- Not done: no PostgreSQL, no suite, no npm, no merge-tree (it writes objects), no launch, no routing edit, no mail, no comment, no ticket change, no `rm`.
- `PYTHONDONTWRITEBYTECODE=1` throughout: no `__pycache__`, and the round-1 kit's `__pycache__` listing is unchanged (`ex/r1_pycache_{before,after}.txt`).

## 1. Drafter predictions at 32e8459bc0f5 over 7eccb131f2d6 (the gate re-derives every one)

| check | file | result |
|---|---|---|
| R2-C1 pin + scope | `ex/scope_ex1.out` (rc 0, 26/26) | ONE parent `7eccb131f2d6`, ancestor (fast-forward); tree `8ba2c0c8e9d1` == claimed (control: parent tree `b393b20f29b4` differs); numstat == the 4 declared paths exactly, so **every other path is byte-unchanged since round 1**; modes: suite 100755, others 100644; `%(trailers)` raw 1 byte (control `bf277eead268` 55); subject 83 chars, no `(#`, keys {KS-1401}; STRICT closing refs in the message 0. INFO: the WIDE (120-char) predicate hits "Fixes gate61 finding N-1383-1 on #1383" (D6) |
| R2-C2 049 delta | same (S7a-g) | ONE pure insertion at old :102 (22 lines, 21 comment/blank). Its ONLY live line is `PERFORM set_config('app.tenant_scope_bypass', 'platform_admin', true);`. H minus the insert == 7eccb131's file byte-for-byte. The bypass is the FIRST live statement after `BEGIN` (:101), with `lock_timeout` next. 0 session-level setters. Live `tenant_scope_bypass` mentions 2 → 3. 049 sha256 `c5dc307fbbdeca0d…` == the body's claim |
| R2-C3 run | NOT RUN (no PostgreSQL by commission) | Read from the suite diff: cell 12 has 9 assertions. They are: 5 labelled `CONTROL` (role false/false, owns 4, charge_events forced true/1, 2 planted, superuser fills both), "the run COMMITTED", NOTICE == real count, 0 remain, and Q-LEAK. `|| no "` sites go 41 → 50 (53 → 62 at runtime). `KS1401_F049_UNDER_TEST` overrides cell 12 ONLY (other cells use `$F049`) |
| R2-C3b bypass read | source read, `git show 32e8459:…` | 039 :124 and :132 carry the carve-out in USING and WITH CHECK. Precedent setters use `true`: `db.ts:172` (`tx.$executeRaw … set_config('app.tenant_scope_bypass','platform_admin', true)` inside a transaction) and `tenant-guc.ts:139`. `gdprService.ts` reaches it via `runWithPlatformScope` (:419, :542, :933, :1332, :1512). Runners: `run-migrations.sh:126` = `psql -f` per file (a fresh session per file); `startup-migrations.ts:148` = `pool.query(m.sql)` (the whole file is one simple query, one implicit transaction), then :149 the `_secuura_migrations` INSERT on a pooled connection that may be the same one. Not measured: that is the gate's (iii) |
| R2-C4 docs | same (S8a-d) | Both docs: every changed line lies inside block `22.` (flow 1 hunk; cheat 3 hunks, incl. the −4 = the "11 cells, 53 assertions, 12–13 s" lines and `KS1401_FLOOR=53` → 62). Close tag `</body>` unchanged, so round-1's D4 state persists and the merge-in still restores develop's `  </body>` via `keep`. `<h2>`/`<h3>` lists unchanged (flow 23, cheat 7) |
| R2-C5 body | `ex/body_ex3.out` (rc 0, 4/4) | **The body is NEWER than the baseline:** sha256 `526650b515ef5a3d…`, 13,054 B / 12,956 chars, `updated_at` 09:29:48Z (`api/pr1383_meta_drafter.json`). Diff vs `016e2af9`: 4 lines removed, 8 added (`api/body_diff_016e2af9_vs_526650b5.out`). These are the N-1383-8 demo-mechanism sentence, kintsugi nullability, cell 12 + its traps, 62/12, 19/18/19 s, 049's new hash, and "the three tampers have not been re-run at this head". STRICT closing refs 0, planted control +1; one `Refs KS-1401`; never-demo + kintsugi deploy present; WIDE predicate 0. **Stale line:** "It also ran inside this push's own pre-push preflight at leg 14 and reported `53 passed, 0 failed` there", next to the new 62/12 (D4) |
| Q-M | `ex/qm_quiet_checkargs_ex1.out` (rc 0) | The command the gate will run: round-1 `c4_docs_gate61.py predict|qm … --head 32e8459bc0f5… --anchor keep`. NOT run by the drafter (merge-tree writes objects; the drafter writes nowhere outside this dir). #1381's advance 46c3e20c..f01c1da5 changes `originate/src/routes/webhooks.ts` + its test + both docs: **not** a kit writer file, so M6 should pass it (D7). D 8th's declared paths (compose, timestamping Dockerfile / test / config README) are outside every M6 prefix |

**Drafter's reading:** every artefact claim that can be read without PostgreSQL reproduces: head, parent, tree, 4 paths +127/-4, the one live statement, first-in-block, `true`, 100755, 0 trailers, 12 cells in the source, the 049 hash, the doc edits inside block 22 only. The open items are below.

## 2. Doubts for the GATE (the prompt carries D1-D8), and items for Wednesday

- **D1 Q-LEAK can pass vacuously.** At the pre-fix file the GUC is never set, so "empty afterwards" holds there too. The suite's Q-LEAK conjunct is falsifiable only by a tamper that sets it session-level. The kit names T-SESSION (`true` → `false`); if Q-LEAK does not red under it, that is a finding against the suite.
- **D2 Scope of the grant.** The bypass is live for the WHOLE DO block (ENABLE / FORCE / DROP + CREATE POLICY / catalog reads), not just the UPDATE. The drafter sees no statement whose meaning changes, but did not measure it.
- **D3 The gateway runner's pooled connection.** `pool.query(m.sql)` runs the file as one implicit transaction, so `is_local` resets at its end. Measured nowhere yet; the builder's Q-LEAK measured psql only. The prompt asks the gate to drive a Pool(max 1) or round 1's runner instrument.
- **D4 Body NEWER than the baseline.** Was the edit ruled by you (N-1383-8)? The drafter found no ruling file. And "leg 14 reported 53 passed" is stale or unverified.
- **D5 "all four controls hold"** (commit message) vs 5 `CONTROL`-labelled assertions in cell 12. Polish unless the gate finds a control that does not hold.
- **D6 "Fixes gate61 finding N-1383-1 on #1383"** in the commit message. Strict predicate 0; the F 3rd brief's 120-char window 1. GitHub needs `fixes #1383` adjacent and Linear needs a key, so the drafter reads it as harmless. The squash body is composed at merge (`mergef3`).
- **D7 #1381's `routes/webhooks.ts` advance** vs `svc_webhooks`, one of 049's four tables. Not a kit writer file, so M6 is blind to it. The gate rules whether that route's queries run under a tenant scope.
- **D8 Round-1 instruments at the new head.** `c2_migration_gate61.py --head` will differ from round 1 on hash-pinned lines. `c3b … probe` X7's owner arm should now read the default tenant instead of NULL. The gate rules expected vs unexpected differences.

**For Wednesday (not the gate's):**
- **W1 The body edit (D4).** If you did NOT rule the N-1383-8 edit, the gate reports the NEWER body as information. Say so in an addendum if you want it judged against a specific ruling.
- **W2 The GO string carries a suffix:** `GO (Seat F 3rd): merge 1383 on gate61 — merge only after the KS-1404 anchor-wiring PR has merged`. Its prefix is byte-equal to the F 3rd brief's `GO (Seat F 3rd): merge 1383 on gate61`. If `inbox_matchf3.py` / `mergef3.py` match the GO by EXACT subject rather than prefix, the suffix could break them. Unverified (the f3 tools are in F 3rd's record folder; not read).
- **W3 The KS-1404 PR may never come.** D 8th's brief (V7) says if kintsugi can only mint mock tokens, D 8th stops and Kam gets a card. The GO's merge-order clause then needs Kam's re-ruling, not the gate's.
- **W4 The round-1 pane** `QA/Secuura-ks1401-1383` may still exist (%31). The round-2 pane is a new name, `QA/Secuura-ks1401-1383r2`.

## 3. The kit's instruments (each exercised; outputs in `ex/`)

| file | what it does | quiet case | firing arms (all fired) |
|---|---|---|---|
| `r2_check_gate61r2.py` | `scope` S1-S9 (pin, fast-forward, 4 paths, modes, trailers, message, 049 delta, docs block-22-only, suite insert-only); `body` B1-B4 (+ WIDE and figures INFO); `--selftest`. Read verbs whitelisted | `scope_ex1` rc 0 26/26 at the real head; `body_ex3` rc 0 (NEWER body); `body_ex4_baseline` rc 0 (the 016e2af9 body) | `selftest_ex2` **28/28** arms: is_local false, a 2nd live line, bypass after lock_timeout, an edited existing line, a session-level SET, the fix commented out; an edit in block 12., a re-indented close tag, a new `<h2>`; a suite line edited, no new cell; `fixes #1383`, "does not close KS-1401", KS-1376 hyphenated, `(#1383)`; body `Closes: KS-1401`, `resolves #1383`, 2nd Refs, never-demo gone, KS-1376, "does not close KS-1401"; **REAL**: the round-1 head posing as the commit (S1, S2, S3 … fire). Real-object control: `body_ex5_oldbody_fires` rc 1 on round 1's `fc18d2c9` body ("close KS-1401"). `selftest_ex1` / `body_ex1` / `body_ex2_*` = history (before the B2 control was made "+1 over the body's own hits") |
| `qm_gate61r2.sh` | the round-1 c4 `predict|qm` with head 32e8459 and `--anchor keep` FIXED; verifies round-1 c4 / lib / kit.json sha256 against kit.json first | `qm_quiet_checkargs_ex1` rc 0 (prints the exact command) | `--anchor carry` rc 2, `--head 7eccb131…` rc 2, a short sha rc 2, a `--repo` under /Volumes/DevMASTER → c4's own guard rc 2, nothing run |
| `launch_qa_secuura_ks1401_1383r2.sh` | the pane launcher (no pins file: re-reads origin each run; head at branch AND pull/head; parent == round-1 head; prompt guards; TTY) | `launcher_check_quiet_ex1` rc 0 | the round-1 head posing (rc 6), the GO clause stripped from a SIM prompt copy (rc 26), a launch with no TTY (rc 21, before `exec claude`) |
| `launch_r2_gate61r2.sh` | the launch action: routing, API, ls-remote, head judged, develop RECORDED, scope S1-S9, overrides, usage gate, `--check`, `cockpit.sh add` | `action_dry_quiet_ex1` rc 0 | stale head rc 11, wrong PR rc 9, a REAL run with a SIM routing file lacking the line rc 1 (stops at step 0; step 4 would also refuse the override) |

## 4. Routing line — NOT added
Back up the file first. Then add ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-ks1401-1383r2|coagent@agentmail.to|yes
```
The drafter read it ABSENT (`ex/routing_absent_read.out`: 0, rc 1). Until it is present, step 0 of the real launch refuses rc 1. The dry run reports it instead.

## 5. How Wednesday launches it (after section 4)
The pane is `QA/Secuura-ks1401-1383r2`. Dry run first, then the launch under `script -q /dev/null` for the TTY guard:
```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate61r2/launch_r2_gate61r2.sh 1383 32e8459bc0f51d1af492aae7c0b3d9754f78c9bf --dry-run
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-05_gate61r2/launch_r2_gate61r2.sh 1383 32e8459bc0f51d1af492aae7c0b3d9754f78c9bf
```
Exit codes:
- rc 1: routing.
- rc 9: input.
- rc 3: API read.
- rc 2: ls-remote.
- rc 11: the head moved or is not the kit head (a RE-DRAFT).
- rc 13: the scope instrument FAILED at the head, or the launcher's `--check` refused.
- rc 16: override.
- rc 12: usage gate.
- rc 14: cockpit.

develop moving is NOT a refusal. Add `WED_USAGE_STOP=…` only with Kam's recorded authority.

## 6. Rung-5 check (after the launch)
Within ~2-5 min, read the new pane (id from the launch's pane census; `/opt/homebrew/bin/tmux capture-pane -p -t <pane_id> | tail -60`). It passes rung 5 only if it shows something only THIS commissioned agent would produce:
- the head `32e8459bc0f5`;
- the round-1 report hash `c1ecb83f16f69182` being verified;
- `NOT-TESTED.written-first.md` under `…/2026-10-05-ks1401-1383-g61r2/`;
- or `r2_check_gate61r2.py --selftest` / `CHECKED 28`.

A bare prompt, a generic greeting, or the round-1 head alone is NOT rung 5.

## 7. Report, GO / NO GO, verdict subject
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1401-1383-g61r2/` (`NOT-TESTED.written-first.md`, `evidence/`, `report.md` with the `## MERGE ADDENDUM` line last; `sha256 report.md` in the mail).
- GO (verbatim, the GO mail's subject): `GO (Seat F 3rd): merge 1383 on gate61 — merge only after the KS-1404 anchor-wiring PR has merged`
- NO GO: `NO GO (gate61 round 2): 1383 at 32e8459bc0f5 — <N-1383-r2-n: the blocker, one line>`
- Pre-merge conditions the gate carries:
  1. The KS-1404 anchor-wiring PR has merged.
  2. The docs-only merge-in passes `qm_gate61r2.sh qm` M0-M7, close tag keep.
  3. The body is re-read at merge with 0 strict closing refs.
  4. The squash subject as declared, 0 trailers, only KS-1401 hyphenated.
- Verdict subject (from coagent@ to wednesday-agent@): `[QA -> Wednesday] GATE61 ROUND 2 #1383 (Seat F 3rd author and merger; T1 KS-1401: N-1383-1 fix, 049 takes the platform bypass for its own backfill; narrowed to 32e8459bc0f5; merge after KS-1404 anchor wiring)`

## 8. NOT-RUN list (template for the gate's NOT-TESTED.written-first.md; the gate edits, never shortens)
- [ ] The live apply and the §5f live sweep: 049 is applied to no real database, and the gate applies it to none.
- [ ] kintsugi: the 8 rows' NULL count, `tenant_id` nullability, the migrating/connecting role (superuser / owner / BYPASSRLS), MULTI_TENANCY_ENABLED. Hence whether N-1383-1 would have bitten there.
- [ ] The gateway runner applied as a NON-superuser role (round 1 measured it as superuser only).
- [ ] Q-LEAK on the gateway runner's pooled connection, unless the gate measures it (R2-C3b iii).
- [ ] Per-tenant databases (CORE only).
- [ ] originate at runtime (writers are a source read + probe cells).
- [ ] lock_timeout inside the runners' own connections (psql only).
- [ ] Demo (never; nothing in the repo enforces it once 049 is on develop).
- [ ] Preflight legs 3 / 4 / 8 (PREFLIGHT-INCOMPLETE 12/15 is not a pass).
- [ ] The four platform suites (Schemathesis, Akto, Playwright, k6).
- [ ] A REAL merge-in head (none exists; develop moves again before it).
- [ ] Round 1's T-FORCE / T-QUAL / T-GUARD at the new head, unless run (budget item f).
- [ ] Rollback (`/* Down */` is prose).
- [ ] Anything skipped for budget, with the reason.

## 9. Re-draft recipe (the HEAD moved; a moved develop is NOT a re-draft)
1. Re-read `ls-remote` + pulls/1383.
2. Re-measure kit `head`, `claimed_tree`, `r2_files`, `modes`, `blobs_r2`, `commit_subject`, `body_drafter_read`.
3. Re-run `r2_check_gate61r2.py --selftest` and `scope`, then the launch action's `--dry-run`.
4. A new head that is NOT one fast-forward commit on `7eccb131` is outside round 2: re-commission.
5. The later merge-in is never a re-draft. The gate's verdict covers it via `qm_gate61r2.sh qm` (M0-M7), recomputed on the develop it merges.
