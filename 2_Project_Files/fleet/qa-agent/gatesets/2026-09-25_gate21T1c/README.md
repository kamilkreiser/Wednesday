# Gateset 2026-09-25_gate21T1c — README for Wednesday

The drafter launched NOTHING, sent NOTHING, tapped NOTHING and committed NOTHING. It wrote nothing outside its session scratchpad.

This is ONE TIER-1 batch gate, the round's THIRD, round 1 of 2, over TWO PRs, FROZEN:
- **#1234** KS-1127 + KS-1089 + KS-1135, `6320a61d86b5d3fb9b693ea5fefb42050e1d2a43` (Seat L4; scripts/run-shell-suites.sh, the leg-14 runner)
- **#1239** KS-1263, `42c20e998a1a69887b8378968a8ff4f19106c24b` (Seat L1; originate /share + /transfer-custody via withTenant)

Pins:
- BASE for both heads is `6ab9d5021e96ea1481cb6c6ff2d6d33b414aecb7` (merge-base with develop = BASE, parent = BASE, 1 commit each).
- Develop at the fill is `d9515f4a06e0db0396a059ccd8c76b610f22a22b`, 18 ahead of BASE. It moved from aa600af94 during drafting, via #1240 KS-789,
  which touched CONTRIBUTING.md only.
- Merged trees: #1234 `fd1c013860988b0dee1aa7066e1047742c9fb758`, #1239 `737553ea7d5677150b01c3b0630d1ed54f9da003`.
- END_TREE `1a30691593d43973729590aca8604c4ff37a863f`. Both orders and `apply --cached` agree: 8 files, +489/-75.

Expected GO: `GO: merge #1234, #1239 batch`.

## 0. Merge-bases and path-disjointness (measured, predict_1.out + _meas/)
- #1234 ∩ #1239 = EMPTY (2 + 6 = 8 paths).
- The develop move (BASE..d9515f4a0: 18 commits, 44 paths) ∩ #1234 = EMPTY.
- **The move ∩ #1239 = 2 paths.** `services/originate/src/routes/documents.ts` was touched by #1225 KS-1291 `1ded2f817`, which removed the dead
  post-save "@" guard in the CREATE route. `…/__tests__/ks1228-a-refused-request-writes-no-provenance-row.test.ts` was touched by KS-1266
  `9e744421a`, which changed port 1 to port 2.
- #1239 still merges CLEAN. diff(develop, merged) == its 6 paths, and numstat is equal. The 4 non-overlap blobs equal the head blobs. On the 2
  overlap paths, `patch-id --stable` BASE..head == develop..merged (the hunks land unchanged).
- Wednesday's check (3), "move ∩ own paths == EMPTY", therefore does **not** hold for #1239. The kit replaces blob-equality with patch-id equality
  on those two paths, and tells the gate to CONFIRM that and to grade the semantic interaction by running originate on the MERGED tree.
- predict refuses any overlap beyond those two, proved by control P1: over the older develop 379c6eb1d, where the two overlaps are absent, it
  refuses rc 1.
- **For #1239's two overlap paths, the equality targets in the addendum are MERGED blobs**, which are develop-dependent.

## 1. Read these WHOLE before launching
- **The prompt** `2026-09-25_secuura-batch1234-t1.prompt.txt` (fill_4.out: 57 KB at the scratch home; the byte count changes with the home path).
  - It opens with `ultrathink`.
  - It names `mail_gate21T1c_ready.md` (L4 READY 4 + L1 READY 8, verbatim) and COMMISSION.md.
  - Sections: the BASE with #1239's overlap; the two `PR #N is KS-n.` claims; THE STACK S0-S9 (for #1239); **THE ROLLBACK CELLS R0-R6 in both
    modes**; #1239 extras; **#1234 without a standalone runner run**; LOAD / anchoring wording; the reaper; leads (a)-(h); by-name items 1-12; HOLDS;
    the GO string.
  - The Go-template braces in the docker commands are intentional.
- **The launcher** `launch_qa_secuura_batch1234-t1.sh` (266 lines, mode 755, `bash -n` rc 0). Opus by default: no `--model`.

## 2. The rollback-cell design (Kam's (c), Wednesday's condition 4) — the heart of #1239

**MODE F** = `MULTI_TENANCY_ENABLED=false`. **MODE T** = `MULTI_TENANCY_ENABLED=true` **plus `PLATFORM_DATABASE_URL`** pointing at the slot's
`secuura_platform`. All cells use the APP role (the one production runs as), against the gate's OWN slot Postgres only.

**The trap the drafter measured** (db.ts initDb / withTenant at the head): with `=true` but no `PLATFORM_DATABASE_URL`, initDb warns "falling back to
single-tenant mode", `tenantManager` stays null, and withTenant silently takes the **Prisma** branch. The committed cell maps only TEST_DATABASE_URL
and labels its describe block from the env var alone. So a naive "true" run is a mode-F run mislabelled.

- **R0 Preconditions.** Record each DSN's role, `rolsuper` / `rolbypassrls`, RLS and FORCE RLS on shares / custody_events / documents, whether
  `secuura_platform` exists, and the migration state.
- **R1 The shipped cells** (CONTROL, D1/D2, C7), one run per mode, on the merged tree. The CONTROL must be green in the same run, or D1/C7 are
  vacuous: the counter has no GUC and may see 0 rows under RLS.
- **R2 Branch witness**, by two instruments:
  - the initDb log lines;
  - a **2×2 directional tamper**. T-POOL (the pool branch COMMITs instead of ROLLBACK) should turn MODE T red and leave MODE F green. T-PRISMA (the
    callback runs outside `$transaction`) should turn MODE F red and leave MODE T green.
  - Any miss means that mode's proof is not established. **This is the red proof of the committed cells.**
- **R3 Route-level red proof, RED at BASE / GREEN at head.** The committed cells call `withTenant` directly, and withTenant already rolled back at
  BASE, so R1 is predicted green at BASE too. The gate must show that (and treat it as a finding about the cells' power), then build a scratch cell
  over the real router and the real db:
  - **D-SHARE:** a recipient-specific failure at k=2. The gate must first find one that is real: `SHARE_TARGET_NOT_FOUND` resolves the same
    document for every recipient.
  - **C-CUSTODY:** the owner flip is forced to fail by a `BEFORE UPDATE` trigger in the gate's slot DB, identical at BASE and head, dropped after.
  - Both modes, plus L1's split tamper at the head.
- **R4 Pool identity** (a new lead): see section 6.1.
- **R5 Re-measure the req.db condition** at the head and at the merged tree, with controls both ways.
- **R6** If MODE T cannot be brought up, the pool-branch proof is a **KS-1263 RESIDUAL, never implied, never green**.

## 3. What the launcher asserts on every run (`--check` and launch alike)
Exit codes in brackets:
- kit at home (2); two rows / thinking directive / capture + commission / no unfilled token (8);
- heads at branch AND pull/N/head (6); develop == pin (17);
- the GitHub compare per PR: merge_base == BASE, ahead 1, behind 18, and the file NAMES (10);
- heads in full in capture + prompt (20); tickets (32); tier lines (7);
- 27 seat items in BOTH files (30); 109 by-name keywords (33);
- base-invariant with the overlap (34); stack (35); rollback (36); req.db (37); load + anchoring (38); holds (39); no-standalone (40);
  #1234 harness (41); reaper (43);
- GO string (26); addendum (25); subject (23); BASE / develop / END_TREE (31);
- non-TTY launch (21); overrides at launch (16).

## 4. The routing line: NOT WRITTEN BY THE DRAFTER. Add it FIRST (`PROPOSED_inbox_routing_line.txt`)
    QA/Secuura-batch1234|coagent@agentmail.to|yes
The drafter's read: batch1234 is ABSENT (0); the control batch1224 is present (1). Repin step 0 refuses with rc 1 without it (control R4).

## 5. THE LAUNCH COMMAND (copy + re-pin + launch; run it in a shell that can reach tmux)
    /usr/bin/rsync -a --exclude '_sp' /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/d384786a-4d7e-451d-a78b-40a06ef20e21/scratchpad/gate21T1c/ /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1c/ && /bin/bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1c/repin_and_launch_gate21T1c.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-09-25_gate21T1c/launch_qa_secuura_batch1234-t1.sh <your session scratchpad under /private/tmp/claude-501/>

The steps and their refusal codes:
- 0 routing (1).
- 0b moved kit: predict + fill re-run at the new home (8). Proved by controls R6 and F1 on a moved copy.
- 1 ls-remote develop + both pull heads + branches (2).
- 2 pulls API heads + `mergeable`, re-read up to 3× while null (3).
- 3 heads == pins on both instruments, open, not `mergeable:false` (11).
- 3b develop moved: re-pin with predict + fill in the same action, then develop re-read (10).
- 4 usage gate (12).
- 5 `--check` (13).
- 6 `cockpit.sh add QA/Secuura-batch1234 <launcher>` (14), then a pane census.

Append `--dry-run` to rehearse steps 0-3. `repin_dryrun_1.out`: rc 0 at 08:00Z over d9515f4a0, `mergeable True` ×2.

## 6. Decide or know before launching
1. **R4 pool identity: a possible Major nobody has raised.** On MULTI_TENANCY=true the old path wrote via `req.db` =
   `createPoolProxy(req.tenantPool)`, and `req.tenantPool = manager.getPool(tenantId)` (shared/db/tenant-context.ts:93) can be a DEDICATED per-tenant
   pool. `withTenant` always uses `getDefaultPool()`. For a dedicated-DB tenant, #1239 may move these writes to the default database. Wednesday's
   condition 1 checked "ONE client", not WHICH pool. The gate is told to measure it and rule on it (or to rule it pre-existing).
2. **#1234 and Wednesday's Q3 condition** ("a run of the whole runner, before and after") cannot lawfully be met while rule 1 stands. #1218 is not
   on develop (measured). The gate records it UNMET-BY-RULE and verifies L4's in-hook line read-only. **You decide:** merge on the in-hook evidence,
   or hold #1234 until #1218 merges.
3. **`mergeable: null` policy:** GitHub read null for both right after the move, then True at 08:00Z. The repin script refuses `false` and accepts
   `null` after 3 reads, with a note (the kit's own merge-tree is the proof). If you want `null` to refuse, change step 3.
4. **Stack:** Docker was healthy at 07:47Z. Slots 2 and 3 hold kept volumes from today's earlier gates, so the rule should pick **slot 4**.
   A foreign container, `s-b26-pg-ks980` (127.0.0.1:55432, Seat B 26th's KS-980), is running. The prompt forbids touching or connecting to it.
5. **Leads the drafter found in #1234's diff:**
   - the KS-1135 "caller TMPDIR is restored" control is vacuous by construction (a child cannot change its parent's env);
   - `/tmp/rss.XXXXXX` is never removed;
   - the SKIP classifier scores a whole suite as skipped on any line-start SKIP;
   - QA-8 is a bash-3.2 defect, but the test calls `bash` from PATH. The gate runs it under /bin/bash 3.2 explicitly.
6. **MG-3 / MG-11:**
   - #1239's body names KS-1155 (×2) and KS-1228, although its only attachment is KS-1263. #1234's three attachments are its own keys, all
     `contributes`.
   - The head commit subjects are 172 chars (#1234) and 96 chars (#1239), both over the 92 limit. The squash subjects must be written fresh.
7. **Both seats are wrapped.** A NO GO fix round goes to a successor seat with the handover.

## 7. Controls: `controls_gate21T1c.sh <scratchpad> [--invert]`
Every control runs BOTH WAYS. The doctored arm must refuse with its own code. A PRISTINE twin goes through the same mechanism and must pass, so each
refusal is attributable to the defect. `--invert` flips every expectation, which proves the harness can report a mismatch.

- **controls_1.out: 66 / 3.** The 3 mismatches were the drafter's harness: its doctor refused anchors that are line-wrapped in the prompt (rc 99,
  never a vacuous pass). The doctor was made whitespace-tolerant.
- **controls_2.out** (normal arm): **72 OK / 0 MISMATCH of 72**, rc 0 (08:14Z-08:33Z).
- **controls_3.out** (`--invert`): **0 OK / 72 MISMATCH of 72**, rc 1 (to 08:52Z). Every control can fail.
- **repin_dryrun_2.out**, re-run after the controls at 08:52Z: rc 0. Develop was still d9515f4a0, `mergeable True` ×2.

Covered: launcher P C D V O G U H20 T I K B S S2 R R2 R3 R4 Q Y Y2 Hh X X2 Z A E J W N N2 M; repin R1-R6; predict P1; moved-kit fill F1.

## 8. Files
- COMMISSION.md · README.md · PROPOSED_inbox_routing_line.txt
- predict_gate21T1c.py / predict_1.out / pins_gate21T1c.json
- prompt_gate21T1c.TEMPLATE.txt · launcher_gate21T1c.TEMPLATE.sh.txt · fill_gate21T1c.py / fill_1..4.out: fill_1 refused (a seat item absent from the
  capture), fill_2 refused (a keyword wrapped across lines), fill_3 and fill_4 rc 0. The launcher_check_1 rc 36 was a case slip in the drafter's
  own anchor.
- the prompt, the launcher, launcher_check_1..2.out
- repin_and_launch_gate21T1c.sh / repin_dryrun_1.out + repin_dryrun_2.out
- controls_gate21T1c.sh / controls_1..3.out
- mail_*.md (40 captured mails + the combined capture) and capture_mail_gate21T1c.py (the dead drafter's; copied, not re-run)
- gh_body_1234.md / gh_body_1239.md
- _meas/: lsremote_2, gh_read_1, linear_reads_1, docker_info_1, capture_verify_1, path lists
- _sp/: the drafter's scratch clone, excluded by the launch command

## 9. NOT done / NOT measured by the drafter
No launch, mail, tap, commit, push, or routing-conf write. The Secuura checkout was touched only by read verbs (ls-remote, cat-file, show, diff,
merge-base, rev-parse, config --get). Every write verb ran in scratch clones under the session scratchpad.

Not pre-run (these are the gate's job): any suite, tsc, the RUNNER_SH matrix, the rollback cells, the stack, legs 3/4/8.

UNMEASURED:
- whether `secuura_platform` exists in a fresh slot and whether TenantPoolManager.init succeeds there (MODE T feasibility);
- whether a recipient-specific failure at k=2 exists for D-SHARE;
- whether the shipped CONTROL is green under the APP role with RLS;
- whether any real tenant uses a dedicated DB (R4's real-world reach);
- the usage gate's state at launch;
- Docker's health at launch.
