# QA Agent Invocation Brief — Datasec/NexusAI, ONE batched gate "batch 11": RD-591 (TIER 1, through-code, test harness only) + RD-735 (TIER 2, through-code, stacked on RD-618 round 2) — two verdicts, one report

**Drafted for Tuesday 2026-09-30 ~01:47–~02:40 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned on Tuesday's batch 11 commission (2026-09-30 ~01:4x AEST) and two READY mails on disk, each read WHOLE by the drafter:
- **A — RD-591** @ `67b840b89b755b59268873a544b8d5ddd7ee54e0` (branch `rd-591-worktree-band-s86n`; merge-base with main `faea66b`, six commits incl. two forward merges) — built by **NexusAI-N (S86N)** —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd591-READY-mail.txt`
- **B — RD-735** @ `7d853b0e0b666b37d220dd05ac0727b5160555d2` (branch `rd-735-csp-intake-residue-r3-s86m`, ONE commit on **RD-618 round 2 `874c4f503d0f37a032014e562972b17e903e1072`**, which is itself cut from `1904765`) — built by **NexusAI-M (S86M)** —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd735-READY-mail.txt`

**Batched under the 2026-09-18 batch-gates rule, as batches #1-#10.** A is TEST-HARNESS ONLY (`__tests__/helpers/test-server.js`, five stand-in cell files, one new cell file). B is a PRODUCT change (the anonymous CSP intake: `backend/server.js`, `backend/services/cspReport.js`) plus cells. **A and B share NO path but the counts file** (MEASURED, §1). **They DO share a semantic surface:** every server-booting cell of B (rd618, rd735, and rd646 for the cross cell) takes its port from `reservePort()` through the rd395 harness — the helper A rewrites. **Neither head carried both** (C-68, row X).
**Every head is re-read by `git ls-remote` in the launcher (retried under C-192), which refuses on a mismatch.**

SELF-CHECK: re-read end-to-end for contradictions | Tuesday s94, 2026-09-30 02:10 AEST
Self-check note: Tuesday read the brief whole (2026-09-30 02:10 AEST) after the drafter's WRONG list; tiers, members, C-187 addendum (drafter's catch), merges-first floor rule and C-192 retries all match the commission; no contradiction found.

## TUESDAY'S RULINGS (the commission; carried in substance — the gate applies them, it does not re-rule them)
- **Tiers.** **RD-591 is TIER 1 (through-code, no browser)** — Tuesday's ruling, above the READY's own "tier 2 by the lane plan … Your call if … warrants tier 1": the guard decides whether SECURITY cells (the SSRF stand-in in rd516, the redirect stand-in in rd523, rd545, rd549) can pass for the WRONG reason. **RD-735 is TIER 2 (through-code)** — the READY's own tier; its budget SHAPE is the gate's to judge for correctness (ruling c).
- **(a) ONE gate session for both, through-code only.** No browser leg. Servers are booted by the cells themselves (or by your own driver) on `127.0.0.1`, from YOUR OWN trees. **Never the demo, never any non-loopback host** (§11).
- **(b) Main is `5531d7b` at commissioning** (Tuesday's ls-remote ~01:4x AEST; the drafter's 01:48:06 AEST reading agrees; **RD-466 landed via PR #34**, `5531d7b` = `refs/pull/34/head`; its CI Build `36589067630` was still `in_progress` at 01:52:13 AEST — drafter, `gh run view`, READ ONLY). **MAIN MAY MOVE BEFORE AND DURING THE GATE.** RD-618 (`874c4f5`), RD-646/647 (`608a1cd`), RD-723 (`19fc17c`), batch 3, batch 8 and RD-197 are queued; four builder seats are merging one at a time tonight. **Take M0 = origin main AT YOUR OWN START by `git ls-remote`, say so, and RE-BASE EVERY PREDICTION in this brief on it.** If RD-618 is already on M0, MTa collapses into M0 — say so. Re-read main at start, mid and end. Never re-base mid-gate.
- **(c) RD-735's design choice is a SHAPE the gate judges.** The builder took "a per-address entry budget" instead of "one limiter token per stored entry" (READY :8). The gate does not re-open that choice; it tries to DEFEAT the shape as built (rows e1-e6) and reports what defeats it.
- **(d) C-190: every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes (test code included). The gate itself NEVER opens, comments on, approves or merges a PR.** No PR exists for either branch (drafter, `gh pr list --head`, READ ONLY, 01:5x AEST) — **CodeQL is NOT RUN at either head; say so.**
- **(e) C-57 on the merged tree, with C-187's ADDENDUM:** B and RD-618 are cut from `1904765` and carry `image-content-exposure.test.js` at `94e6e4c`; M0 carries RD-466's `7e3262b`. **C-187's ADDENDUM APPLIES** ("the pair stays ACCOUNTED when main (or the merged tree) carries RD-466"): **predicted missing 2 = C-187's pair, ACCOUNTED only when (a1)-(a4) and (b) are each MEASURED; any OTHER missing id is a STOP.** A is cut from `faea66b` (`9ede5fd`) — C-187 does not apply to A.
- **(f) The gate NEVER merges and never pushes. Findings only.** Merges exist ONLY inside your own scratch clones, as the merged-tree measurement (§8).
- **(g) STANDING (batch 7 ruling f): every jest run inside a hold gets `--forceExit` AND a hard deadline; every mutated file is restored in a `trap … EXIT`.** H-20 and H-21 (§3a).
- **(h) C-185 + its ADDENDUM:** main's CI known-failing set is **{rd638-export-always-ends E2, rd465-first-run-open-window O-1 "Turn on Authentication Control: success removes the banner"}** (O-1 ONLY while its failure is the `checkEntraStatus` TypeError). **RD-733 and RD-723 are not on M0 at drafting** (MEASURED: `git log faea66b..5531d7b` = RD-204, RD-466 only), so the set stands. Neither member touches either cell.
- **(i) MERGES GO FIRST on the jest lock tonight** (§10 clause 1): lock-free work first, ONE hold, and a merge ticket that files ahead of your grant goes ahead of you.
- **Launch order:** as gate slots free; the launcher re-pins heads at launch and reads main as it finds it.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not build
these changes and you owe no builder anything. **Every line below that reports what a builder says is a CLAIM, never evidence.** Explore two changes — a test
harness that bands ports by worktree and makes counting stand-ins REFUSE traffic from outside the test's process tree (A), and a per-address stored-entry budget
plus a wider userinfo strip on the anonymous CSP intake (B) — looking for any state in which **a guarded stand-in counts a dial it should have refused, or
refuses one it should have counted; a security cell goes green because the GUARD dropped a dial rather than because the product never made it; a cell
measuring arrival reads the guard's delay; any cell that passed at main loses a pass or slows past its budget; one address (or many) stores more than the
budget allows or evicts its own budget; a forged report keeps userinfo in the log or the ring; a cell is green while its named behaviour is broken; or the id
set loses a test silently.**

- **RD-591 is TIER 1 (through-code).** Verdict: **GO / GO WITH FINDINGS / NO GO at `67b840b`**, plus its merged-tree result.
- **RD-735 is TIER 2 (through-code).** Verdict at **`7d853b0`** (with RD-618 `874c4f5` under it), plus its merged-tree result.
- **One verdict PER ticket, one report, one mail.** A finding on one ticket never becomes another's verdict. RD-618 is NOT a member (batch 9 gated it GO WITH FINDINGS); it is the base B stands on, and the merged tree carries it.
- **TIER 1 AND TIER 2 AT THROUGH-CODE WEIGHT, FINDINGS-ONLY:** no fixes, no pushes, no PRs, no deploys, nothing to Partner Center, the demo or production (§11).

## THE CLARIFICATIONS THAT BIND THIS GATE (opened by the drafter at source, ~01:55–02:05 AEST)
File: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md` (344,985 bytes, 2001 lines, mtime 2026-09-30 01:03;
the last numbered entry is C-192 at :1994 — re-read line numbers, the file grows). **The drafter opened ONLY these (line numbers MEASURED):**
- **C-49** (:305) — the PRIOR-WORK check before rebuilding, replacing or removing anything.
- **C-57** (:416) — *"A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control."*
- **C-68** (:663) — a verdict holds only at its head; *"a clean merge-tree and a changed measured surface are not in tension"*; re-run the affected cells BY NAME.
- **C-102** (:951) — *"every existing test that relied on a LATER return in that function is a candidate for silent disarmament"* (the §3b sweep: the guard adds an early exit before every guarded stand-in's handler).
- **C-104** (:978), **C-112** (:1147) *"A declared limit is where the evidence stops — not a place it is cleared."*, **C-125** (:1326), **C-133** (:1432), **C-141** (:1486) + ADDENDA 1-4 (the `--after` tool), **C-174** (:1794) *"NEVER KILL BY PATTERN."*
- **C-115** (:1180) — `reservePort()` isolates workers WITHIN one jest run and NOT across seats; *"absence of a port clash is NOT evidence of a quiet floor."* RD-591's origin.
- **C-173** (:1775) item 9 — *"RD-591: band test ports by worktree (a stable hash of the worktree path) PLUS a stand-in that rejects and logs foreign traffic (C-115)."*
- **C-177** (:1828) + its **CORRECTED** note (5 of 7 files) + its **ADDENDUM 2026-09-30** — *"rd549 may stamp its env stand-in's request arrival at the socket's ACCEPT time"*, with Tuesday's conditions: *"a red arm with a REQUESTER-side delay must still read red"*; the C-177 guard arm holds for an rd549-shaped stand-in; the READY names the guard's cost and any other cell that measures arrival against a readiness instant. Condition 3: *"proof that each stand-in's counted cells keep main's pass set."*
- **C-184** (:1902), **C-186** (:1924) — merge turns (context for §10).
- **C-185** (:1911) + its **ADDENDUM** — the known set (ruling h): *"O-1 counts as known ONLY while its failure is"* the `checkEntraStatus` TypeError.
- **C-187** (:1932) + its **ADDENDUM** (2026-09-29) — ruling (e); the ADDENDUM names *"RD-618 `874c4f5`, RD-646/647 `608a1cd`"* by sha.
- **C-190** (:1967) — *"Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included."*
- **C-192** (:1994) — a `Permission denied (publickey)` is TRANSPORT, retried up to 5 × ~10 s; *"a FAILED ls-remote is UNKNOWN, never a value."*
- **Not opened by the drafter, so not cited:** every other C-number (C-110, C-116, C-61 and C-142 appear inside the entries above; read them if you rely on them).

## PRIOR ROUND
PRIOR ROUND (RD-591): **no prior gate.** Seven builder rounds (READY :18-19): r2 an in-process fetch dropped as vanished; r3 B6 could not fail; r4 B6's child never
vanished; r4b a socket handed to a closed server hung `close()`; r5 the fast path missed still-connecting sockets; r6/r7 rd549's arrival stamp measured the guard's
delay (C-177 ADDENDUM). RELAYED. Its red cells were cut on `1904765` (`c79926a`), forward-merged to `dd15ce1` (`4fcfbae`) and `faea66b` (`5e00f0a`).
PRIOR ROUND (RD-735): **batch 9 gated RD-618 round 2 `874c4f5` GO WITH FINDINGS**; RD-735 is "the one follow-up ticket for batch 9's A-F1r, A-F2r, A-F3c and A-N2"
(READY :2). Batch 9's report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch9/report.md` — its findings
A-F1r (:22), A-F2r (:23), A-F3c (:24), A-N2 (:26), A-N3 (:28 — the type-less pass-on guarded only by rd646's census) and its C-68 instruction (:83) *"whichever
of RD-618 and RD-646+647 merges second re-runs rd646 AND rd618 by name on the real merged tree"* are the baseline this round is measured against.

PRIOR ROUND (method, and the lessons this brief carries): the **batch 10 gate** is the most recent NexusAI gate.
ITS REPORT IS ON DISK AT: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch10/report.md`
(verdicts §0; instruments §2; floor §3; merged tree §8; WRONG §14; **self-corrections §15, S-1..S-8**). **Carried from it, each deliberately (and folded into §3a):**
1. **S-5 (a VOID arm): a nested `sandbox-exec` exits 71.** A driver already inside the belt must not boot its server through a second `sandbox-exec`; the child inherits the driver's sandbox, proven by the driver's own TEST-NET `EPERM` (H-22).
2. **S-6 (a VOID arm, 2 deadlines fired): `/bin/ps` is SETUID (`-rwsr-xr-x root`, MEASURED by the drafter) and EPERMs inside the sandbox.** Use `pgrep` for your own censuses. **THIS BATCH'S PRODUCT UNDER TEST CALLS `ps`:** RD-591's `attributePeer` runs `lsof` then `ps -axww -o pid=,ppid=,command=` for every out-of-process peer — **under your belt the guard may read EVERY child's dial as `unattributable` and REFUSE it** (H-23, row g0).
3. **S-7 (a VOID part): `--setupFilesAfterEnv` is an ARRAY option — put the test paths FIRST** (or use `--setupFilesAfterEnv=<one path>`), else jest swallows the paths as setup files (0 suites) (H-24).
4. **S-2: quote every path with a space** ("Testing Agent MAIN", "!CODING"); never `set -- $spec` (H-6, H-11).
5. **S-8 / H-18: zsh eats `=====`** (a leading `=`) as well as `:s` — `/bin/bash`, and never a bare `====` separator in the default shell (the drafter hit it tonight too — WRONG 12).
6. **S-4: a bare `END` is not `END ok`** — every driver prints exactly `END ok` (or `END VOID <reason>`), and the H-14 check matches `^END (ok|VOID)` (H-14).
7. **S-3 / batch 9 S-5: a zero stands only beside a control that fires FOR THIS PARENT SET** — here four parents (M0, `874c4f5`, `7d853b0`, `67b840b`), and `7d853b0` CONTAINS `874c4f5`.
8. **§3 of the batch 10 report: the hold was granted before Tuesday's re-file ANSWER was read, and a merge ticket then waited 2 h 43 min behind it.** That is why ruling (i) exists: **merges go first** (§10).
**Reuse instruments BY COPY** from batch 10's `evidence/` (`qa-floorlib.sh`, `qa-floorcount.py`, `qa-to.sh`, `qa-holdlib.sh`, `qa-jestwrap.sh`, `qa-runj10.sh`, `qa-mut10.py`,
`qa-mutlib10.sh`, `qa-merge10.sh`, `qa-c57-id-superset.sh`, `qa-c112-census.py`, `qa-c68census.py`, `qa-h1-selftest.sh`, `qa-h1-scan.py`, `qa-jsum.js`, `qa-mail.py`,
`qa-mailread.py`, `qa-ssprint.sh`, `qa-netbelt.sb`, `qa-netbelt-ctl.js`, `qa-cov-setup.js`, `qa-srvlib.js`, `qa-sweep-analyze.py`) at
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch10/evidence/`.
**Batch 10's `qa-floorlib.sh` defaults are STALE (`ROOT=50957`, `NEG=62649,9959,38362,20317,64933` — batch 10's seats; MEASURED by the drafter) — correct BOTH.**
**macOS has no `timeout` binary** (`qa-to.sh`: `perl alarm`, rc 142 = fired; the drafter's own `timeout` call failed tonight).

## 1. Targets — verified at drafting from the object store (01:48–~02:30 AEST)
**origin by `git ls-remote` at 2026-09-30 01:48:06 AEST (one call, first attempt succeeded):** `main` **`5531d7b83dab22906091d8a02014d4ff69cea574`** (= `refs/pull/34/head`
= `refs/heads/rd-466-image-case-names-s86o`) · `rd-591-worktree-band-s86n` **`67b840b89b755b59268873a544b8d5ddd7ee54e0`** · `rd-735-csp-intake-residue-r3-s86m`
**`7d853b0e0b666b37d220dd05ac0727b5160555d2`** · `rd-618-csp-intake-residue-s86m` `874c4f503d0f37a032014e562972b17e903e1072` (B's base) ·
`rd-646-647-redis-fail-closed-recovers-s86m` `608a1cd99adcc69f6d2cdc552f170e89710adb02` (the cross partner). **No `refs/pull/*/head` equals either member head or `874c4f5`**
(pulls #1-#34 listed; `gh pr list --head` empty for all three branches). Every sha here is a commit in the local object store (`cat-file -t`).
**Re-read at your start, mid and end, with C-192's retry. A moved TICKET head is a finding and a reason to stop, never a typo to fix. A FAILED ls-remote is UNKNOWN, never a value.**

**Chains (MEASURED, `git log --format='%h %p %ci | %s'`):**
- **A (RD-591):** `faea66b..67b840b` = exactly six commits: `c79926a` (on `1904765`, red cells, 2026-09-27) → `a2a93b2` (the fix) → `4fcfbae` (merge `dd15ce1`) →
  `47d8855` (round 6) → `5e00f0a` (merge `faea66b`, 2026-09-29 18:32:31) → **`67b840b`** (round 7, 2026-09-30 01:45:04 AEST: "rd549 stamps its env request at ACCEPT time
  (Tuesday's option (b)); counts 4208/254"). **merge-base(A, main) = `faea66b1bce5c17a2fef282c808821b3bf0825c6`** — A is NOT forward-merged onto `5531d7b` (the READY's "main faea66b merged forward" was true
  when main WAS `faea66b`; main has since moved `faea66b → f9cb440 (RD-204) → 5531d7b (RD-466)`).
- **B (RD-735):** `874c4f5..7d853b0` = ONE commit `7d853b0` (2026-09-30 00:50:36). **`1904765..874c4f5` = RD-618's three: `7e4cd2e`, `4334b96`, `874c4f5`.**
  **merge-base(B, main) = merge-base(`874c4f5`, main) = merge-base(A, B) = `1904765007e9447ac6c980f9840c0689a02abe6c`.** RD-646/647 `608a1cd` is ONE commit on `1904765`.
- **Main since the members' bases:** `faea66b..5531d7b` = RD-204 (`b86799d`, `f9cb440`) + RD-466 (`01fb77e` merge, `5531d7b` counts). Files: `.dockerignore`, `Dockerfile`,
  `__tests__/helpers/dom.js`, `__tests__/helpers/vendor-surface.css`, `__tests__/image-content-exposure.test.js`, `rd204-bootstrap-5.3.0-painting.json` (A), `rd204-vendor-coverage.test.js` (A),
  `rd418-dockerignore-round3.test.js`, counts. **`1904765..5531d7b` touches 22 paths**, among them **`backend/server.js`** (RD-681: `bc099b2` → `0d7e387`) — **the one product path B also changes.**

**Deltas (MEASURED, `git diff --numstat`):**
- **A over `faea66b`:** `__tests__/helpers/test-server.js` **+251/−10** (`cff1e54` → `bb45cd7`) · `rd486-ai-test-key-forwarding` +2/−1 · `rd516-ai-test-ssrf` +2/−1 · `rd523-aoai-redirect-refused` +2/−1 ·
  `rd545-ai-test-limit-survives-ai-off` +2/−1 · `rd549-ai-config-inert-until-confirmed` **+3/−2** (`4a35642` → `1988b46`) · **`__tests__/rd591-cross-seat-isolation.test.js` +345 (added, `6ae80ce`)** ·
  counts +3/−3. **Counts 4195/253 → 4208/254** (+13 = A0-A3, B0-B8; +1 suite). **Round 7 alone (`5e00f0a..67b840b`):** test-server +21/−1, rd549 +2/−2, counts. **Nothing under `backend/`, `static/`, `docs/`, no package file.**
- **B over `874c4f5`:** `backend/server.js` **+18/−5** (`e076121` → `86dc63f`) · `backend/services/cspReport.js` **+49/−6** (`4b38e90` → `6608eae`) · `__tests__/rd735-csp-intake-residue-r3.test.js`
  **+144 (added, `4925b58`)** · `__tests__/rd618-csp-intake-residue.test.js` **+3/−1** (`8bbfcc7` → `1007b66`, R7's regex `/i` + a comment) · counts +3/−3. **Counts 4146/248 → 4152/249** (+6 = S7, S8, B1, B2, R8, R9).
- **RD-618 over `1904765` (under B, NOT a member):** `backend/server.js` +45/−8 (`bc099b2` → `e076121`), `cspReport.js` +62/−6 (`f102d26` → `4b38e90`), `rd618-csp-intake-residue.test.js` +192 (added), counts. 4133/247 → 4146/248.
- **Blobs elsewhere:** `helpers/test-server.js` `cff1e54` at `1904765`, `faea66b`, M0, `874c4f5`, `7d853b0`, `608a1cd` · `helpers/rd395-server-harness.js` `2453a3f` everywhere (it `require`s `./test-server`) ·
  `helpers/rd554-restore-harness.js` `028fa30` at M0 and A · `image-content-exposure.test.js` `94e6e4c` at `1904765`, `874c4f5`, `7d853b0`, `608a1cd`; `9ede5fd` at `faea66b`, A; **`7e3262b` at M0** (= RD-466 `3f7e263`) ·
  `backend/server.js` `0d7e387` at M0 and A; `4ddf75f` at `608a1cd` · `package-lock.json` `9064763` at every sha named here · `rd646-647-redis-fail-closed-recovers.test.js` `ee838ec` at `608a1cd` only.
- **Counts:** `1904765` 4133/247 · `faea66b` 4195/253 · `47d8855` 4191/252 · `5e00f0a` 4195/253 · **`67b840b` 4208/254** · `874c4f5` 4146/248 · **`7d853b0` 4152/249** · `608a1cd` 4144/248 · **M0 `5531d7b` 4210/254**.
- **`__tests__` files (NUL-safe `ls-tree -r -z`):** 289 (`1904765`) · 296 (`faea66b`) · **297 (A)** · 290 (`874c4f5`) · **291 (B)** · 291 (`608a1cd`) · **298 (M0)**.
- **`helpers/test-server` require-population** (`require(…helpers/test-server…)` in `__tests__`): 54 at `faea66b`, M0, `1904765`, B; **55 at A** (the READY's "55 test-server importers"); 55 at `608a1cd` (rd646).

**Main may move (ruling b).** Call main at your start **M0**. (1) M0 must be `5531d7b` or a DESCENDANT (the launcher refuses otherwise); (2) main's movement since `5531d7b`
must not touch a member path (the launcher refuses otherwise); **RD-618 `874c4f5` or RD-646/647 `608a1cd` landing on main is EXPECTED tonight — a NOTE, and then the MT
build skips that merge (say so) and every prediction below re-bases**; (3) your merged trees: **MTa = M0 + `874c4f5`; MTb = MTa + `7d853b0`; MT1 = MTb + `67b840b`; MT2 = MT1 + `608a1cd`**
(the RD-646/647 cross tree — L-B1); **predicted at M0 = `5531d7b`: MTa 4223/255 · MTb 4229/256 · MT1 4242/257 · MT2 4253/258** (ARITHMETIC: 4210 + 13 + 6 + 13 (+ 11) / 254 + 1 + 1 + 1 (+ 1));
`__tests__` 299 · 300 · **301** · **303**; test-server require-population MT1 55, MT2 56; (4) if main moves AGAIN during your gate, your verdict names M0 and says what moved (C-68), and you measure each member onto the END main by merge-tree.

### TARGET A — RD-591 (TIER 1, through-code) @ `67b840b`
- **What changed (READ, the whole diff over `faea66b`):** `test-server.js`: **`workerBand()`** = `39000 + worktreeSlot() × 640 + (JEST_WORKER_ID − 1) × 40`, `SLOT_COUNT = floor((49152 − 39000) / 640) = 15`,
  `worktreeSlot()` = sha256(realpath of the nearest ancestor holding `.git`) mod 15; a worker id > 16 throws a named error. **`guardServer(server)`** replaces `server.emit` for
  `'connection'`: stamps `sock.rd591AcceptedAt = Date.now()` FIRST, then (i) **fast path** `isOwnSocketPeer` (an own open socket, an own `probe()` within 10 s, or an own socket
  still connecting) → handed over synchronously; else (ii) **lookup** `attributePeer`: `lsof -nP -iTCP@<addr>:<port> -Fpf` → own if this pid holds ≥ 2 fds on the tuple; **no
  other pid → `vanished` (HANDED OVER, counted, `console.warn`ed)**; else `ps -axww -o pid=,ppid=,command=` → `own` if every peer pid's parent chain reaches this pid, else
  **`foreign` (destroyed, recorded, `console.error`ed)**; an lsof/ps failure → **`unattributable` (destroyed, recorded, logged)**. `close()` destroys sockets still waiting.
  **`arrivalTime(req)`** returns `rd591AcceptedAt` for the FIRST call on a socket (`rd591ArrivalUsed` flag), `Date.now()` for every later call or an unguarded socket.
  `listenInBand` now guards every server it binds. **Five stand-ins** (rd486 `servers.forEach(guardServer)`, rd516 `guardServer(server)`, rd523 `guardServer(server); guardServer(privSrv)`,
  rd545 `servers.forEach`, rd549 `guardServer(server)`) — **one line each plus the import (C-177 as CORRECTED); rd549 also swaps its request stamp `Date.now()` → `arrivalTime(req)`.**
- **Cells (READ):** `rd591-cross-seat-isolation.test.js`: A0 (band stable), A1 (two worktrees in different slots never share a band), A2 (clear of 38900-38939 and below 49152), A3 (worker > 16 named failure);
  B0 (own connection reaches), B1 (a CHILD's reaches), B2 (an ORPHAN's never reaches, recorded with pid), B3 (the refusal is LOGGED), B4 (one stand-in: child counted, orphan refused — C-177 condition 1),
  B5 (fast path missed, lsof path forced), B6 (connect-WRITE-close still reaches — "no false zero"), B7 (close while a lookup waits CLOSES), B8 (an in-process `http.get` on the fast path while still connecting).
- **rd549's positive-arrival cells (READ at `1988b46`):** `h.readyAt = Date.now()` after `bootServer`; `bootStandInRequests()` counts `S.requests` with `q.at <= h.readyAt`; **C2/C10 (:431-434) and O4 (:480-483)
  assert `envReached: r.boot.envRequests > 0` INSIDE a `toEqual` with `hydrated`/`planted`** — so a red must show `"envReached": false` in the diff and nothing else, never "Exceeded timeout".
  Planted dials are counted by a preload's DIAL_LOG, NOT by the guarded stand-in (READ) — the guard can only affect `envReached`.
- **Builder's claims (RELAYED, READY :2-16):** RED at `1904765` (`c79926a`): A1, A3, B2, B3, B4 red; A0, A2, B0, B1 green. Mutants M-c (vanished dropped) → B6; M-d (the round-4 helper, no close guard) → B7;
  M-e (no still-connecting clause) → B8. **The rd549 red arm** (a requester-side 3 s connect delay) → C2/C10 and O4 red. Main vs branch pass sets by name (rd486, rd516, rd523, rd545, rd549, rd571,
  test-server-helper, sustainability-dark-mode): LOST 0, 0 cells slower by > 1 s. Guard arm on an rd549-shaped stand-in: child counted, orphan refused. **Full verify "4208/4208 across 254"; the 55 importers 972/972 ×3.**
  **The drafter checked (MEASURED):** `session-tools/s86n/rd591/r7-hold.out` carries `VERDICT: PASS — 4208/4208 tests passed across 254 suites`, the 55-file batch 972/972 ×3, and the red arm
  `2 failed, 28 passed` with **C2/C10 "(6 ms)" and O4 red; `r7/2-redarm.log` :222-223 and :248-249 show `-"envReached": true` / `+"envReached": false` at `:434:110` and `:483:14`** — the assertion,
  not a timeout, AS THE BUILDER RAN IT. **BUT that hold ran on `HEAD 5e00f0a dirty` (M test-server, rd549, counts) from 15:02:49Z to 15:43:46Z; the commit `67b840b` is 01:45:04 AEST = 15:45:04Z,
  AFTER the hold.** The READY's "READY verify at 67b840b's tree" is UNVERIFIED as to the committed blobs (WRONG 3). **The red arm injected its preload with `NODE_OPTIONS="-r …slow-connect-preload.js"`** (`r7-hold.sh`) — see H-15.
  `lookup-cost.out`: `lsof median ms 57 ps-table median ms 31 | ps lines 804`.
- **NAMED LIMITS — VERBATIM (READY :21-26):**
  *"- The guard delays every OUT-OF-PROCESS connection by its lookup: lsof ~57 ms plus a ps table ~31 ms (lookup-cost.out). The ps table could be cached; lsof cannot be avoided. A cell measuring arrival against a readiness instant must use arrivalTime(). Scanned all 25 guarded test files: only rd549 (handled) and rd591 B7 (the guard's own cell)."* ·
  *"- Only listenInBand/listenOnReservedPort servers and the 5 wired stand-ins are guarded. reservePort() users that bind their own servers are not."* ·
  *"- A server leaked by an EARLIER file in the SAME jest worker still descends from that worker, so it reads as own: the guard separates seats and orphans, not suites within one worker."* ·
  *"- CI needs lsof for out-of-process peers (ubuntu-latest ships it): UNVERIFIED until the branch's Build runs."* ·
  *"- rd554-restore-harness's header ("two concurrent jest runs still share 39000+") becomes false; that is not this file, so it is not edited here."*
- **NOT TESTED — VERBATIM (READY :29):**
  *"NOT TESTED: two REAL concurrent seats' full suites against each other (the orphan and foreign cells stand in for it); a macOS/Linux difference in lsof output; Linux CI."*
  → **L-A1** (lookup cost, and "only rd549 and B7 measure arrival") · **L-A2** (unguarded `reservePort()` users) · **L-A3** (a same-worker leak reads as own) · **L-A4** (CI's lsof — and ps — UNVERIFIED) ·
  **L-A5** (the rd554 header) · **L-A6** (two real concurrent seats) · **L-A7** (macOS/Linux lsof difference; Linux CI) · **L-A8** (CodeQL/CI at the head — NOT RUN, no PR).
- **The drafter's READ (MEASURE, rows g1-g9):** (i) `vanished` hands over ANY peer that closed before the lookup, own or not — a FOREIGN connect-write-close is indistinguishable from B6's own (row g3).
  (ii) `arrivalTime` is "first CALL on the socket", not "first REQUEST" (row g2). (iii) The rd554 sentence is `helpers/rd554-restore-harness.js` **:88-89** (the READY names it "rd554-restore-harness's header";
  it is a helper, not a cell, and not a header block) — row g7. (iv) **15 slots vs the NexusAI `worktrees/` directory's dozens of worktree roots: two live seats sharing a slot is LIKELY, not rare** (6 roots → P(a shared slot) ≈ 0.68, arithmetic) — row g8.

### TARGET B — RD-735 (TIER 2, through-code) @ `7d853b0`, on RD-618 r2 `874c4f5`
- **What changed (READ, the whole diff over `874c4f5`):** **A-F1r:** `createCspEntryBudget({ windowMs, max, maxKeys = 10000, clock = Date.now })` — a `Map` key → `{ start, n }`; a key whose window
  expired (`t − start ≥ windowMs`) is deleted and re-inserted fresh (moves to the END of insertion order); `grant = max(0, min(want, max − n))`; **when `size > maxKeys`: every expired key is pruned, then the
  OLDEST-inserted keys are dropped until `size ≤ maxKeys` — even keys whose window is live.** The intake (`server.js`): `all = buildCspEntries(body, now, Infinity)`; `entries = all.slice(0, 10)`; the cap line
  only when `all.length > entries.length` (A-N2); `granted = entries.length ? budget.take(req.ip, entries.length) : 0`; `granted < entries.length` → a warn line; **`granted === 0` → 429**; else store `granted`.
  Budget = `CSP_REPORT_RATE` = **60 per 60 000 ms**, keyed on **`req.ip`**, and **`app.set('trust proxy', 1)`** (`server.js:1120`). **A-F2r:** values trimmed of `/^[\u0000-\u0020]+|[\u0000-\u0020]+$/g`
  first; in the FALLBACK (a scheme-shaped value `new URL` rejects, or a non-scheme value) `AUTHORITY = /^((?:[a-z][a-z0-9+.-]*:)?[\\/]{2})([^/\\]*)/i` and everything up to the LAST `@` in the authority is dropped.
  **A-F3c:** rd618 R7 marker regex `/i`. **A-N2:** as above.
- **Cells (READ, `4925b58`):** S7 (the forged shapes), S8 (CONTROL: an `@` after the path is not userinfo; RD-495/RD-618 shapes unchanged), B1 (grants 10, 45, 5, 0 for key a; 10 for b; 10 after the window),
  B2 (the key map stays ≤ maxKeys), R8 (61 requests of 12 reports from one address: 60 stored, ≥ 440 of 500 ring slots untouched, 1-6 → 204, 7-60 → 429 budget, 61 → 429 limiter; CONTROL first request stores 10),
  R9 (5 reports with 3 empty: no cap line; 12: "kept 10 of 12"). R8 and R9 boot their own servers (rd395 harness → `reservePort()` — **A's helper on MT1**).
- **Builder's claims (RELAYED, READY :17-36):** RED at `874c4f5`'s two product files: exactly S7, B1, B2, R8, R9 fail (S8 and the 13 rd618 cells pass). GREEN 19/19. M1 (budget grants everything) → B1, R8;
  M2 (round 2's fallback back) → S7; M4 (cap counted before the empty filter) → R9; **M3b** (err.message logged ONLY for `charset.unsupported`, the gate's MF3c shape) → R7 red with the fix; M3b-control (same
  leak, round 2's case-sensitive regex) → R7 green = the defect. **Disclosed slip: "my first M3 leaked on BOTH R7 arms … that control could not isolate A-F3c. M3b is the isolated form."** C-68 by name:
  rd618, rd735, rd495, rd607: 38/38. Full verify 4152/4152 across 249. **The drafter checked (MEASURED):** `rd735-hold.log` :408 and `rd735-verify-full.log` carry `VERDICT: PASS — 4152/4152 tests passed across 249 suites`;
  `rd735-m3b.log`: M3b `1 failed, 12 passed` (R7 ✕), M3b-control `13 passed`, "anchor count 1" each.
- **NOT TESTED — VERBATIM (READY :46-49):**
  *"- The cross cell with RD-646/647 (608a1cd) on this head. The budget runs only AFTER the limiter has passed, so the named 503 comes first in principle, but rd646 was NOT run on 7d853b0 + 608a1cd. It should run on whichever lands second."* ·
  *"- Multi-replica: the budget is per process, as the ring is."* ·
  *"- The demo."*
  → **L-B1** (the RD-646/647 cross — row x2, REQUIRED here) · **L-B2** (multi-replica) · **L-B3** (the demo) · **L-B4** (the READY's own trade-off: *"an ambiguous forged value such as https://h?x=a@b is logged as https://b"*) · **L-B5** (CodeQL/CI — NOT RUN, no PR).
- **The drafter's READ (MEASURE, rows e1-e9):** (i) **the eviction rule lets one address RESET its own budget** by pushing 10,000 fresh keys through (the oldest-inserted key goes first, live or not); whether 10,000
  fresh `req.ip` values are reachable depends on (ii) **`trust proxy 1` with no ingress in front: `req.ip` is taken from a client-sent `X-Forwarded-For`** (READ, express semantics — MEASURE it) — that would bypass
  the budget AND the limiter per request; behind the Marketplace ingress it would not (READ ONLY; not reachable here). (iii) Values that START with a non-C0 Unicode space (U+00A0, U+2028, U+FEFF) or carry a tab/newline
  INSIDE the scheme (`ht\ttps://u:p@h/` — WHATWG `new URL` removes ASCII tab/newline anywhere) skip BOTH the scheme test and `AUTHORITY` (READ) — candidates that KEEP userinfo. (iv) A value `new URL` parses with a
  NON-special scheme (`foo:user:pw@host/`) has no host, so the parsed branch returns `u.protocol + u.pathname` = `foo:user:pw@host/` — userinfo-shaped text KEPT on the parsed path, which RD-735 did not touch (READ).
  (v) **The READY's trade-off example `https://h?x=a@b` parses under `new URL`** (host `h`), so it never reaches the fallback — the example as written would be logged `https://h`; the trade-off applies to an
  UNPARSEABLE variant (e.g. `https://h:99999?x=a@b`) — MEASURE both and quote.

### File overlap and merge predictions — the drafter used the READ-ONLY three-argument `git merge-tree <base> <a> <b>` (writes NO objects), NOT `--write-tree`
**MEASURED ~02:10 AEST** (legacy merge-tree output parsed for `+<<<<<<<` markers per "changed in both" path): M0 × A (base `faea66b`), M0 × B (base `1904765`), A × B, B × `608a1cd`, M0 × `608a1cd`,
A × `608a1cd` → **each: conflict markers in `scripts/verify-expected-counts.json` ONLY.** **`backend/server.js` is "changed in both" for M0 × B, A × B, B × `608a1cd`, M0 × `608a1cd` and A × `608a1cd`, and merges TEXTUALLY
CLEAN every time** — so every merged tree holds a **COMBINED `server.js` blob no parent carries** (C-68: *"a clean merge-tree and a changed measured surface are not in tension"* — batch 9 §8.9 found the same for RD-618 × `faea66b`).
**Re-measure by `git merge-tree --write-tree --name-only` in YOUR OWN scratch object dir (§8.1) on YOUR M0** (the three-argument form has no rename detection; the real measurement is yours): M0 × `874c4f5`, M0 × B,
M0 × A, A × B, B × `608a1cd`, M0 × `608a1cd` (skip what M0 already contains); **name every combined blob.**

### MERGE ORDER — the drafter's proposal, with its predicted end state and the C-68 re-run set per merge
**Proposed order: 1. RD-618 `874c4f5` (not a member; batch 9 GO WITH FINDINGS) → 2. RD-735 `7d853b0` → 3. RD-591 `67b840b`.** Why: B cannot land before RD-618 (stacked); RD-735 is the product change and
closes four batch-9 findings; RD-591 changes the harness EVERY server-booting cell uses, so landing it last means B's cells were proven on the harness B was built on, and RD-591's C-68 set then includes them.
**Challenge it:** the reverse (RD-591 first) is file-independent too — order independence is the control (§8.3), not an assumption.

| step | merge | predicted conflicts | predicted counts after (M0 = `5531d7b`) | C-68 re-run set BY NAME (on the tree after that step) |
|---|---|---|---|---|
| a | M0 + `874c4f5` (MTa) | counts only; `server.js` COMBINED | **4223/255** | rd618 (13) + rd495 + rd607 + every `csp-report` / `cspReport` reader (re-derive by `git grep -l`; positive control rd618, negative control a file that only names the URI in a comment) |
| b | + `7d853b0` (MTb) | counts only (`874c4f5` already in) | **4229/256** | rd735 (6) + the step-a set; **R8/R9 under M0's `server.js` + RD-681's changes, which neither B nor `874c4f5` carried** |
| c | + `67b840b` (MT1) | counts only | **4242/257** | **the 55 test-server importers BY NAME** (per-file counts; positive control rd591, negative control a file that only MENTIONS `test-server` in a comment) **+ every rd395-harness requirer** (B's R8/R9 and rd618 among them — they boot through A's new `reservePort()`) |
| x | + `608a1cd` (MT2, the cross tree) | counts only; `server.js` COMBINED again | **4253/258** | **rd646 (11) + rd618 + rd735 + rd495 + rd607 by name (L-B1, batch 9's instruction)** + rd646 under A's harness (it `require`s `helpers/test-server` directly) |

**End state predicted: MT1 4242/257 · MT2 4253/258 at M0 = `5531d7b` — ARITHMETIC; re-base on YOUR M0; the measurement decides.** Re-derive every set in YOUR clone at M0 with a positive control (the ticket's own
cell file must be found) and a negative control (a file that only MENTIONS the name must NOT be counted as a reader).

### How to build your trees
- **No worktree is created in the NexusAI repo, and you never work in its `2_Project_Files` checkout or any builder `worktrees/` directory.** In that repo use ONLY read verbs: `show`, `diff`, `log`, `ls-tree`,
  `cat-file`, `grep`, `ls-remote`, `rev-parse`, `merge-base`, `rev-list` (plus `count-objects` for §8.9). **NEVER `fetch`, `pull`, `push`, `checkout`, `worktree`, `commit`, `stash`, `gc`, `merge`; and `merge-tree
  --write-tree` ONLY with `GIT_OBJECT_DIRECTORY=<your own scratch dir> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects`.**
- **Every tree is K1** — `git clone --shared --no-checkout <repo> <dir>` then `checkout` in YOUR clone (origin removed; local identity; `gc.auto 0`; `core.fsmonitor false`; hooks off), under a fresh
  `mktemp -d` in `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/qa-trees/batch11.XXXXXX/`. Status-check before use. **Each K1 tree holds its own `.git`, so A's `worktreeRoot()` resolves to
  YOUR tree and `worktreeSlot()` hashes YOUR path — record each tree's slot (row g8).**
- **Each tree is EXCLUSIVE to this gate and to ONE purpose.** A fresh arm per mutant; never reuse a mutant tree for a clean arm; `batch11`-prefixed directories only.
- **The red-at-parent trees:** A — YOUR clone at `67b840b` with `helpers/test-server.js` restored to `faea66b`'s `cff1e54` AND the five stand-ins restored to their `faea66b` blobs (rd591's own file stays: its A/B cells
  must redden against the old helper — the builder's red was on `1904765`, yours is on `faea66b`); B — YOUR clone at `7d853b0` with `backend/server.js` and `backend/services/cspReport.js` restored to `874c4f5`'s
  `e076121` / `4b38e90` (rd618's R7 stays at the head's `/i`) — hashed after the restore, committed IN YOUR CLONE ONLY so each tree is a clean K1.
- `node_modules`: an APFS clone (`cp -c -R`) of the newest gate tree you trust, **after proving** `package-lock.json` is blob `9064763` there too; a real directory, never a symlink.

## 2. Why these tiers, and who is waiting
- **RD-591 TIER 1 — severity rules:** **a guarded stand-in that COUNTS a dial from outside the test's process tree in any cell that asserts a POSITIVE arrival or count (rd549 `envReached`, rd486/rd516/rd523/rd545
  counts) is a Major** (Tuesday's stated reason for (b)); **a security cell (rd516 SSRF, rd523 redirect, rd545, rd549) that stays GREEN with the product's refusal REMOVED, because the guard dropped the dial, is a
  Blocker** (the cell's green would be the wrong reason in exactly the direction that hides a vulnerability); **a cell that passed at M0 and fails or is lost at the head or on MT1 is a Major; a cell slowed past its
  own budget is a Major; a mutant the READY says reddens a cell that you find leaves it green is a Major (C-40 class); a READY/comment claim that is false is a Minor.**
- **RD-735 TIER 2 — severity rules:** **one address storing more than 60 entries in any 60 s window through the intake as deployed locally is a Major (A-F1r not closed); a forged report whose userinfo reaches the log or
  the ring in a shape the READY claims covered is a Major; a shape the READY does not claim, which keeps userinfo, is a Minor (name it); a cell green while its named behaviour is broken is a Major (C-40); a budget
  defeated only through a client-forged `X-Forwarded-For` with no ingress is the deployment's `trust proxy` question — name it and its evidence class, severity yours, not a re-rule of (c).**
- **Who is waiting:** RD-591's merge author is **NexusAI-N (S86N)**; RD-735's is **NexusAI-M (S86M)**, whose RD-618 lands first — under C-184/C-186's turn order and C-190's PR route.

## 2a. LEGITIMATE SHAPES — required measurements, row by row
**Columns: the head, the base it is measured against (P_A = `faea66b`'s helper and stand-ins for A; P_B = `874c4f5`'s two product files for B), and the MERGED tree. Every cell-run row: your own K1 tree,
under the network belt (subject to H-23), a fresh TMPDIR, `--forceExit`, a deadline, killed in a `finally` by pid.**

**G — RD-591's guard and bands.**

| row | shape | expected at `67b840b` | at P_A | predicted-by |
|---|---|---|---|---|
| g0 | **THE GUARD UNDER YOUR BELT (instrument landing, BEFORE any guarded run):** rd591 B1 (a CHILD's dial accepted) and B4 run once under your strict belt and once unbelted, in the same hold; read `server.foreignConnections` / the `[RD-591]` stderr lines | **say which applies:** if B1/B4 go red under the belt with `unattributable (ps failed: …)` or `lsof failed`, the guard cannot attribute ANY child inside the sandbox → **every guarded cell runs UNBELTED** (the full verifies ran unbelted in every earlier gate), with a TEST-NET landing control proving what the unbelted run could reach; if green, run belted | — | drafter (batch 10 S-6) |
| g1 | **RED-AT-PARENT (POSITIVE CONTROL FIRST):** `6ae80ce`'s rd591 against P_A's `test-server.js` (`cff1e54`) | — | **name the red set and quote each failure** (builder's red on `1904765`: A1, A3, B2, B3, B4; A0, A2, B0, B1 green — the builder's run was a different base, so RE-DERIVE; any cell that cannot even LOAD against the old helper (a missing export) is named as such, not counted as a red) | builder |
| g2 | **`arrivalTime` and keep-alive (the new shared surface):** a guarded stand-in you boot in-test; drive from a CHILD process (so the lookup path runs): (i) one request; (ii) two sequential requests on ONE keep-alive socket; (iii) two PIPELINED requests in one write; (iv) a first request whose handler does NOT call `arrivalTime`, then a second that does; (v) an unguarded server | (i) stamp = accept time, earlier than handler time by ≈ the lookup (quote ms); (ii) req 2 = its handler time (≥ req 1's); (iii) req 2 = handler time (quote); **(iv) req 2 gets the SOCKET's accept time — "first CALL", not "first request" (name it; say whether any cell can reach it)**; (v) handler time | — | drafter + C-177 ADDENDUM |
| g3 | **"vanished = handed over and counted" vs a FOREIGN dial:** a dialer process that is NOT a descendant of the jest worker (start it from your own shell BEFORE the jest run; it waits for a port file) connects to an **rd549-shaped** guarded stand-in, writes a COMPLETE request for the env route (`GET /openai/models …`) and closes at once — in the same run a CONTROL dialer that stays open (must read `foreign`, refused); repeat ≥ 20 times each | **measure the verdict distribution** (foreign / vanished) **and whether a vanished foreign request lands in `requests[]` with `at ≤ readyAt`** — if it does, **a positive-arrival cell can pass on a foreign dial: build the rd549 cell shape (`envReached` true with the child's real dial SUPPRESSED by the connect-delay preload) and show it green** → a Major (§2); if every foreign dial reads `foreign`, say the race did not open and give the timing | — | commission (3) |
| g4 | **THE rd549 RED ARM reads red ON `envReached`, not on a timeout:** your own connect-delay preload (the builder's shape, re-written, not copied) delaying outbound connects in the SERVER process only by 3,000 ms; then again at 300 ms and 60 ms (below / near the guard's lookup) | 3,000 ms: **C2/C10 and O4 red with the diff exactly `-"envReached": true` / `+"envReached": false`** (quote the lines and the cell's elapsed ms; no "Exceeded timeout"; every OTHER field equal); prove the preload LANDED only in the server (a landing line printed by the preload, absent from jest's own stderr); 300 / 60 ms: MEASURE and quote | — | builder + commission (1) |
| g5 | **the stamp, isolated (the other half of (b)):** a COPY of rd549 with its stamp put back to `Date.now()` (the pre-(b) form), guarded, with the guard's `attributionDelayMs` seam set to 3,000 ms on its env stand-in; and the head's `arrivalTime` form with the same delay | pre-(b) copy: **C2/C10, O4 RED** (the stamp measures the guard); head form: **GREEN** — proves the green comes from the accept-time stamp and not from a fast guard | — | drafter |
| g6 | **non-rd549 cells unaffected:** the 55 test-server importers + every rd395-harness requirer, **pass sets BY NAME at M0 vs the head** (one run each in one hold), per-cell durations from `--json` | **LOST 0**; every cell > 1 s slower at the head NAMED with both durations; `[RD-591]` stderr lines counted per file (**foreign 0, unattributable 0** in a solo run; any `vanished` line named) | — | builder + commission (2) |
| g7 | **the named limits, MEASURED (L-A1..L-A5):** (i) lookup cost: lsof and ps medians on THIS machine now, n ≥ 30 each, and the `ps` line count; (ii) **census** of `reservePort()` users that bind their own server and are NOT guarded (NUL-safe `git grep -l` at the head, positive control rd486 which IS guarded); (iii) a same-worker leak: in one jest invocation with `--runInBand`, file 1 leaks a server that dials port P after its suite ends, file 2 binds a guarded stand-in on P — the dial reads `own` (the READY's limit reproduced) — quote; (iv) CI's lsof — READ ONLY (`.github/workflows/build.yml`'s runner and any `apt`/lsof step) and **the guard's `ps -axww -o pid=,ppid=,command=` argv on Linux procps is UNVERIFIED too** (no Linux here); (v) `rd554-restore-harness.js:88-89` at the head, quoted, and say which half becomes false (two runs in DIFFERENT slots no longer share; two runs in the SAME worktree or a colliding slot still do) | each quoted with its number; "25 guarded test files" re-derived and named | — | commission (4), (6), (7) |
| g8 | **slots of the live floor (PROBE):** `worktreeSlot()` from YOUR head tree's helper, called with each live root — every builder worktree root that holds a lock ticket or a running jest during your gate (from the lock owner/queue files' `cwd=`, READ ONLY), each of YOUR trees, and the NexusAI `2_Project_Files` root | the slot of each; **name every pair sharing a slot** (such a pair has only the guard between them) | — | drafter |
| g9 | **the builder's mutants re-derived INDEPENDENTLY + your own:** M-c (vanished → dropped) → B6; M-d (no close guard) → B7; M-e (no still-connecting clause) → B8; **your own: M-own (the ancestry walk returns `own` always) → B2/B4 red?; M-fds (the ≥ 2-fds rule removed) → which?; M-stamp (`arrivalTime` returns `Date.now()` always) → rd549 C2/C10, O4 red ONLY under g5's delay?; M-band (`worktreeSlot` returns 0) → A1 red?** | each builder mutant reddens exactly its cell; each own mutant MEASURED — **any that leaves every cell green is a branch no cell sees (C-40): name it** | — | builder + drafter |

**S — the C-102 sweep's security arm (the WRONG-REASON question, Tuesday's tier-1 reason).**

| row | shape | expected at `67b840b` | at M0 | predicted-by |
|---|---|---|---|---|
| s1 | **the guard must not HIDE a real dial:** for rd516 (SSRF) and rd523 (redirect), a PRODUCT mutant that removes the refusal the cell is named for (e.g. the SSRF check / the redirect refusal — locate by coverage, one anchor each), run at M0 and at the head | **the named cells RED at both, with the same failing assertion** (the stand-in counted the forbidden dial) — a cell green at the head but red at M0 is the Blocker of §2 | red | drafter |
| s2 | every guarded negative cell's run log: `[RD-591] refused …` / `could not name the peer …` lines | **0 refused and 0 unattributable in every clean run** (a refusal in a clean run means a dial was dropped, whatever the verdict) | — | drafter |

**E — RD-735's budget (every arm quotes stored counts and statuses).**

| row | shape | expected at `7d853b0` | at P_B (`874c4f5`) | predicted-by |
|---|---|---|---|---|
| e0 | **RED-AT-PARENT (POSITIVE CONTROL FIRST):** `4925b58`'s rd735 + the head's rd618 against P_B's two product files | — | **exactly S7, B1, B2, R8, R9 red; S8 and all 13 rd618 cells green** (quote each) | builder |
| e1 | the head clean: rd735 + rd618 | **19/19** (name every title) | — | builder |
| e2 | **one address through the real intake** (a server from YOUR tree, open mode, fresh DATA_DIR): 61 requests × 12 reports in < 60 s, then 60 more after the window | ≤ 60 stored per window (quote statuses per request and the ring length after each window); the window edge: requests straddling `start + 60 000 ms` | ring gone at request #50 (batch 9) | builder + drafter |
| e3 | **MANY addresses via `X-Forwarded-For`** (`trust proxy 1`, no ingress): does `req.ip` follow a client-sent XFF? 61 requests each with a DIFFERENT XFF | **MEASURE:** if `req.ip` = the XFF value, both the limiter and the budget key on it — the ring is refillable in 50 requests again; quote the stored count; control: the same without XFF (budget holds) | — | drafter (READ (ii)) |
| e4 | **eviction resets a live budget:** unit-level on `createCspEntryBudget` with its `clock` seam: key V takes 60 (→ 0 left); 10,000 fresh keys take 1 each inside V's window; V takes again | **MEASURE:** the READ says V gets 60 again (V was the oldest-inserted and live keys are dropped); then the same THROUGH the intake if e3 showed XFF controls `req.ip` (10,001 requests are within the limiter only if the limiter also keys per XFF — say which) | — | drafter + commission |
| e5 | **window edges and the clock:** B1's shape with `clock` driven to `start + windowMs − 1`, `start + windowMs`, and BACKWARDS (a clock step of −30 s) | quote grants at each; name any grant > 60 inside one real 60 s span | — | drafter |
| e6 | **the builder's mutants re-derived INDEPENDENTLY:** M1 (budget grants everything) → {B1, R8}; M2 (round 2's fallback back) → {S7}; M4 (cap before the empty filter) → {R9}; **your own: M-evict (drop only EXPIRED keys, never live ones) → does B2 redden? M-429 (`budgetSpent` never set) → R8 red? M-key (budget keyed on a constant) → which?** | each MEASURED; a mutant that leaves rd735+rd618 19/19 is a branch no cell sees (C-40) | — | builder + drafter |

**F — A-F2r's fallback (every arm quotes the input, the stored/logged value, and which branch ran).**

| row | shape | expected at `7d853b0` | at P_B | predicted-by |
|---|---|---|---|---|
| f1 | **batch 9's s3b shapes** (userinfo holding `?`/`#`, a leading space/tab/0x01, an unparseable backslash authority, `//u:pw@h`) through `stripQueryAndFragment` AND through the real intake (log + ring) | userinfo absent in every one | kept (batch 9 A-F2r) | batch 9 + builder |
| f2 | **the READY's trade-off (L-B4):** `https://h?x=a@b` (parseable) and an UNPARSEABLE variant (`https://h:99999?x=a@b`, `https:\\h?x=a@b`) | quote each output; say which reaches the fallback; **the READY's example as written → `https://h`?** (READ (v)) | — | READY + drafter |
| f3 | **shapes that may KEEP userinfo (READ (iii)/(iv)):** a leading U+00A0 / U+2028 / U+FEFF before `https://u:p@h/`; `ht\ttps://u:p@h/` and `https\n://u:p@h/`; a non-special scheme `foo:user:pw@host/x`, `mailto:`-shaped values; `HTTPS://U:P@H` (case); `https:///u:p@h` (triple slash); percent-encoded `%40` in the userinfo | **MEASURE and quote each** — any stored or logged value holding the planted password marker is a finding (Minor unless the READY claimed the shape, then Major); control: the plain `https://u:p@h/` loses it | — | drafter |
| f4 | **ReDoS / linear time (C-190 READ + PROBE):** `stripQueryAndFragment` on a 16 KB value of `//` + `@`×n, `\\`×n, and the edge-trim class on 16 KB of `\u0001` | time at head vs P_B (quote ms); nothing super-linear | — | drafter |

**R — A-F3c and A-N2.**

| row | shape | expected at `7d853b0` | at P_B | predicted-by |
|---|---|---|---|---|
| r1 | **M3b re-derived INDEPENDENTLY (the builder's disclosed slip):** the product logs `err.message` ONLY for `charset.unsupported` (your own anchor, one match); R7 with `/i` | **R7 RED** (the charset arm sees the upper-cased marker) — quote the log line | — | builder |
| r2 | **M3b-control:** the same leak, R7's regex back to case-SENSITIVE | **R7 GREEN = the defect A-F3c** (this is the arm that proves the `/i` matters) | — | builder |
| r3 | **the builder's first M3 (disclosed as non-isolating):** err.message logged on BOTH arms — show R7 red under EITHER regex, so it could not isolate A-F3c | as disclosed | — | builder |
| r4 | **A-N2:** 5 reports (3 empty) → no cap line; 12 non-empty → "kept 10 of 12"; 12 with 4 empty → ? ; and the budget's own line when a partial grant happens ("kept N of M") — quote | as stated; name every line an operator would read | "kept 0 of 5" (batch 9) | builder + drafter |

**X — the cross-change cells (C-68).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| x1 | **B's cells under A's harness:** on MT1, rd618 + rd735 + rd495 + rd607 by name, 3 runs, per-file counts; their `[RD-591]` stderr lines counted | all green ×3; 0 refused; name the slot of MT1's tree | drafter |
| x2 | **L-B1, REQUIRED: rd646 on a tree carrying RD-735 AND RD-646/647 `608a1cd`** (MT2): rd646 (11) + rd618 + rd735 + rd495 + rd607 by name; CENSUS-B/CENSUS-M offenders; and the READY's "the named 503 comes first in principle" — with Redis configured and down, a body that would be over budget: quote the status (503 or 429?) and which middleware answered | all green; **the order of 503 vs 429 MEASURED, not read** | commission (4) |
| x3 | **the combined `server.js`:** on MT1 and MT2, the CSP intake block and the rate-limit block quoted from the merged blob; its blob id named; `node --check` rc | the intake block = B's; RD-681's and RD-646/647's hunks present | drafter |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.**

## 3. THE QUESTIONS ALL TARGETS ANSWER FIRST
0. **SESSION_SECRET UNSET, EVERY RUN** — §3a H-1's ONE permitted printer. Positive control once per target: its own cell file with a throwaway random 64-hex secret exported (never printed,
   never written) — identical results, or say what differed.
1. **Re-pin everything yourself:** `git ls-remote` at start, mid and end (three timestamped readings, branch name beside each sha, C-192's retry, attempts counted): main, both member branches, RD-618's branch,
   RD-646/647's branch, RD-723's. M0 and the "Main may move" rule re-proved; chains and exact parents; deltas; counts at `faea66b`, `67b840b`, `1904765`, `874c4f5`, `7d853b0`, `608a1cd`, M0.
2. **POSITIVE CONTROL FIRST — re-derive every red and every mutant INDEPENDENTLY** — your own scripts, never the builders' `r7-hold.sh`, `slow-connect-preload.js`, `rd549-guard-arm.js`, `rd735-hold.sh`
   or `rd735-m3b.sh` (read them for method). **Before each mutant arm, prove it still parses — `node --check` on every mutated JS file, exit 0, quoted — and that it LANDED (the exact mutated text present, the
   original absent once the new text is removed; your mutate tool's `--verify` with its negative control). A red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.**
   Quote the failing assertion of every red.
3. **Name every behaviour guarded by no cell, and every one guarded only by source text** (g2 (iv), g9's and e6's survivors at least).
4. **Full verify of each head and of MT1**, `npm run verify -- --maxWorkers=2 --forceExit`, through the lock, SESSION_SECRET UNSET, a fresh SHORT TMPDIR each, **K1 only**, **unbelted (as every earlier gate) —
   and, per g0, say whether A's guarded cells could attribute under the conditions the verify ran in.** Prove `--forceExit` reached jest or say it did not and rely on the deadline. **Predicted: `67b840b` 4208/254 ·
   `7d853b0` 4152/249 · M0 = `5531d7b` 4210/254 · MT1 4242/257 (regenerated once).** MT2's full verify only if the queue allows (else NOT RUN and named — its x2 set is required). Every failure by NAME;
   **C-185's known set is CI's, not local: a LOCAL failure of rd638 E2 or rd465 O-1 is named, never waved through.** Re-run until green is not an acceptance gate.

## 3a. INSTRUMENT RULES — H-1..H-26 (H-1..H-21 carried from the batch 10 brief; H-22..H-26 are batch 10's self-corrections S-1..S-8 and this batch's guard, folded in)
- **H-1.** The ONLY permitted SESSION_SECRET printer, verbatim:
  `if [ -n "${SESSION_SECRET+x}" ]; then echo "SESSION_SECRET SET (length ${#SESSION_SECRET})"; else echo "SESSION_SECRET UNSET"; fi`.
  **FORBIDDEN anywhere in your scripts:** `${SESSION_SECRET-…}`, `${SESSION_SECRET:-…}`, `${SESSION_SECRET+$SESSION_SECRET}`, `echo
  $SESSION_SECRET`, `printenv`, `env | grep`, `set | grep`, and **echoing an env array that could hold it (`${envs[*]}`)**.
  **Self-test it BEFORE the first hold (a control that can fail):** run the printer once with a throwaway exported and once unset, capture both, assert
  the throwaway's value is ABSENT from both (compare in-process; never print it). **After every hold, scan that hold's logs for the throwaway value** and
  report the count (0); **the scan's own positive control plants a DIFFERENT random marker, never the throwaway.** Print any needle only as
  `<first4>…<last4>`, and **mask GUIDs with or without hyphens**. Export the throwaway INSIDE the run's subshell, never in argv.
- **H-2.** Never construct a product storage object on a DATA_DIR you are measuring AFTER its server booted. Seed BEFORE; read logs RAW.
- **H-3.** Every hook you rely on (a preload, a dialer process, a planted value, a mutated line, a clock seam) gets a **LANDING CONTROL** before the measured run: prove it fired once on a known input.
  An arm whose instrument failed is VOID, is re-run, and is reported as a self-correction.
- **H-4.** The heartbeat is a **separate child** process started by the hold wrapper (`while sleep 60; do echo "HB $(date -u +%FT%TZ) <step> <pid>
  <elapsed>"; done`), killed in the wrapper's `trap … EXIT`; **the wrapper ABORTS the hold if no HB line appears within 90 s of the grant**, and after
  every hold you compute and REPORT the **max gap** between HB lines (must be ≤ 120 s). Keep the HB child's output unfiltered.
- **H-5.** Restore your own perturbations (mutated files, planted values, held ports, dialer processes, env files) before any hash, and hash the restore.
- **H-6.** Every extractor and census gets a POSITIVE CONTROL. **Every path is quoted** — `!CODING` and `Testing Agent MAIN` contain `!` and spaces; **never `set -- $spec` or an unquoted loop word over a path (batch 10 S-2).**
  **Every server you boot runs under the network belt (`qa-netbelt.sb`) with its landing control (EPERM for TEST-NET-1, 200 for loopback) — subject to H-23 for guarded cells.**
- **H-7.** Mutants are built and verified ONLY by a quoted tool with a negative control (an unmutated tree → VOID rc ≠ 0). A mutant check that prints an
  empty count is a VOID arm, never a pass.
- **H-8.** The landing rule is "the exact mutated text is present AND the original text is absent once the new text is removed" — never "the anchor is absent".
- **H-9.** Byte-level plants (C0 controls, U+00A0/U+2028/U+FEFF, tabs inside a scheme, 16 KB timing inputs) are written with `Buffer` and verified by
  `xxd -l 16` (at the plant's offset) and `wc -c` BEFORE use; never with `echo`, `printf`, a heredoc or `JSON.stringify` where the bytes matter.
- **H-10.** Prove every phenomenon reachable before measuring its absence: "the guard refuses a foreign dial" → B2/B4 red at P_A and your g3 control dialer read `foreign`; "no userinfo kept" → f1's plain
  control loses the marker AND a planted marker in a NON-userinfo field is found in the log; "0 refused in a clean run" → s2's count beside g3's refused control.
- **H-11.** Every script runs under `/bin/bash` explicitly, and every `<sha>:<path>` is written `"${sha}:${path}"`. **Never `set -- $x` or `declare -A`
  in the default shell** (macOS bash 3.2 has no associative arrays).
- **H-12.** Before the C-57 control, list every `__tests__` file any head MODIFIES or DELETES. **Predicted: A MODIFIES `helpers/test-server.js`, rd486, rd516, rd523, rd545, rd549 (titles UNCHANGED — prove it) and
  ADDS rd591 (13 ids); `874c4f5` ADDS rd618 (13 ids); B MODIFIES rd618 (titles UNCHANGED) and ADDS rd735 (6 ids).** Name the stale-parent files: every `__tests__` file main changed since each member's
  base that the member carries at its OLD blob (for B/RD-618 at least `image-content-exposure` `94e6e4c`, `helpers/image-manifest.js` `07e8711`, `helpers/dom.js` `04f182f`, and everything RD-681/RD-204/RD-466 changed; for A `dom.js`, `vendor-surface.css`, `image-content-exposure` `9ede5fd`, rd418).
- **H-13.** Every tree census is NUL-safe (`ls-tree -z`), with a positive control on a path containing a space.
- **H-14.** Every driver ends with an explicit END record, **exactly `END ok` or `END VOID <reason>`**; the check matches `^END (ok|VOID)` and a bare `END` is VOID (batch 10 S-4). A run with no END record is VOID, whatever its exit code.
- **H-15.** Pass preloads as `-r "<path>"` in argv, never through `NODE_OPTIONS`. **ONE exception is declared in this batch, for rows g3/g4 only:** a connect-delay preload must reach the SERVER that the rd395
  harness SPAWNS, and the builder's route was `NODE_OPTIONS="-r …"` on jest. Use it ONLY if you cannot reach the spawned server through argv (the harness's own `preload` option in a COPY of the cell is the
  preferred route — say which you used); if you use NODE_OPTIONS, the preload must gate itself to the server process (argv[1] ends in the server entry point) and print a landing line there, and your run must
  show that line ABSENT from jest's own stderr.
- **H-16.** A plant is checked to be what the product will treat it as before it is used (a forged report is a `csp-violation` the intake keeps — prove it stored one; a dialer's request is a complete HTTP request the stand-in's parser accepts — prove it with an own-process control).
- **H-17.** Absolute tool paths only; every arm asserts the thing actually STARTED (jest's first suite line, the server's listen line, the dialer's own `connected` line) before its rc is read.
  **Your own process censuses use `pgrep`/`pgrep -P`, never `/bin/ps` (setuid; EPERM in the sandbox — batch 10 S-6).**
- **H-18.** zsh consumes `:s`/`:a` in `$var:path` AND `=` at word start (a bare `=====` separator line is a zsh error — batch 10 S-8) — `/bin/bash`, braces, and **reject any sha256 equal to `e3b0c442…` as a VOID read**.
- **H-19.** gitleaks canaries (if you run gitleaks over the deltas) are planted as real keys, not JSON-escaped inside strings.
- **H-20 (ruling g).** **EVERY jest invocation inside a hold carries `--forceExit` AND runs under a per-step hard DEADLINE** (`qa-to.sh <seconds> …`,
  rc 142 = fired): targeted cell runs 600 s, the C-68 unions 2,400 s, a full verify 2,700 s, each g3 dialer run 180 s. A deadline that fires ABORTS that step
  (reported by name, never retried silently), the wrapper's EXIT trap runs, and the lock releases through the wrapper's own exit. **`--forceExit` hides open
  handles, so a leak census (children by pid, dialers, ports, temp dirs) runs after every jest.**
- **H-21 (ruling g).** **Every file you mutate is restored in a `trap … EXIT` installed BEFORE the first mutation** (restore by `git show
  "${sha}:${path}" > file` or from a pre-mutation copy, then hash-compare to the pinned blob); the trap also covers INT and TERM; after every hold, assert
  every mutated path's hash equals its pinned blob and report it. **A mutant tree left mutated after a deadline is a self-correction to report, and that
  tree is quarantined, never reused.**
- **H-22 (batch 10 S-5).** **Never nest `sandbox-exec`: a nested one exits 71.** A driver already inside the belt boots its server as a plain child (it inherits the sandbox); prove the inheritance by the driver's own TEST-NET `EPERM`.
- **H-23 (batch 10 S-6, NEW SUBJECT).** **RD-591's guard shells out to `lsof` and `/bin/ps` (setuid).** Row g0 decides, by measurement, whether guarded cells can attribute a child inside your belt. **Every run of a guarded
  cell reports its count of `[RD-591] refused …` lines by verdict** (`foreign` / `unattributable`) and of `could not name the peer` lines; **an `unattributable` refusal in a run is an INSTRUMENT condition, never a product
  result — that run's GREEN negative cells are VOID, not evidence** (they may be green because the dial was dropped).
- **H-24 (batch 10 S-7).** **`--setupFilesAfterEnv` (and every jest ARRAY option: `--testPathIgnorePatterns`, `--roots`, `--setupFiles`) goes AFTER the test paths, or as `--opt=<one value>`**; assert the suite count jest reports equals the files you passed.
- **H-25 (batch 10 S-1).** A comment-aware compare (k4-style) filters the parser's own comment tokens; its comment-only control must read IGNORED before it is used.
- **H-26 (C-192).** Every `git ls-remote` you run is retried up to 5 × ~10 s on `Permission denied (publickey)`; **a failed call is UNKNOWN and is never read as "moved" or "unchanged"**; report the attempt counts.

## 3b. THE NEGATIVE-ASSERTION SWEEP (C-102) — REQUIRED, scoped to what these members change
**A adds an EARLY EXIT in front of every guarded stand-in's handlers** (a refused connection is never emitted), so a negative cell over a guarded stand-in ("the product never dialled X", "0 requests reached the
private origin", "the redirect was not followed") may now be green because the GUARD dropped the dial. **B adds an early 429 exit (`budgetSpent`) and a new first branch in `stripQueryAndFragment`** (the edge trim),
so a negative cell over the intake ("nothing stored", "no marker in the log") may be green for a different line.
1. **Enumerate the changes (READ, quote each):** `git diff faea66b 67b840b -- __tests__/helpers/test-server.js`; `git diff 874c4f5 7d853b0 -- backend/server.js backend/services/cspReport.js`.
2. **Enumerate the callers' cells** on MT1: every cell over a guarded stand-in (rd486, rd516, rd523, rd545, rd549, and every `listenInBand`/`listenOnReservedPort` user — 21 files at the head by `git grep -l`, re-derive)
   that asserts an ABSENCE or a zero (positive control: rd516's private-stand-in "0 dials" cells must be found); every cell over the CSP intake asserting an absence (positive control: rd618 R7's `markerInLog: false`;
   rd646's CENSUS cells). Classify each NEGATIVE or POSITIVE.
3. **For each NEGATIVE cell: does it still reach the check it is NAMED for?** Proven by coverage (batch 10's `qa-cov-setup.js` form) at the base and at the head, **plus, for guarded cells, the s2 count (0 refused) in the
   same run** — **a negative cell whose green now comes from a different line, or from a refused connection, is DISARMED** — name it.
4. **Self-test first or ABORT:** a positive control (a cell you know reaches its named check), a negative control (a POSITIVE cell), and a non-empty population.
5. **Report per ticket:** population, negative cells, still reaching, disarmed.

## 4. TARGET A — RD-591 (TIER 1). Answer each with a measurement.
1. **Scope:** `git diff --name-status faea66b 67b840b` = the eight paths; nothing under `backend/`, `static/`, `docs/`, no package file; `test-server.js`'s exports at the head ⊇ its exports at `faea66b` (no export removed — name any).
2. **POSITIVE CONTROL FIRST (g1, g4, s1):** the rd591 red at P_A, the rd549 red arm on `envReached`, the SSRF/redirect mutants red at the head. Then g0 (instrument), g2-g9, s2.
3. **(a) the "vanished" verdict (g3)** — can a positive-arrival cell pass on a foreign dial? Build it; say yes with the green run, or no with the timing distribution.
4. **(b) the named limits (g7)** — MEASURED, each with its number; the READY's "25 guarded test files" and "only rd549 and B7" re-derived.
5. **(c) the pass sets (g6)** — LOST 0 by name, durations, per-file `[RD-591]` counts.
6. **PRIOR WORK (C-49):** the READY names RD-203 `e952f3b`, RD-227 `6d95707`, RD-571 `2a43982`, RD-641(i) `1bfc265` as KEPT (refusal proof, bind proof, every-address proof, the host seam) and rd554's retirement layer
   untouched — READ each commit's helper hunk at `faea66b` and show it byte-present at the head (`git show`, a comment-stripped compare where a line moved); say whether `listenInBand`'s bind loop is otherwise unchanged.
7. **C-190 (READ ONLY):** no PR → CodeQL NOT RUN. The head adds `execFile('lsof' …)` and `execFile('ps' …)` with a port from the socket and `fs.appendFileSync(process.env.RD591_TRACE_FILE …)` in test code —
   say whether any changed line matches a pattern CodeQL flags (command injection from a socket value? `js/file-system-race`? — READ ONLY, a note for the merge author; C-190 includes test code).

## 5. TARGET B — RD-735 (TIER 2). Answer each with a measurement.
1. **Scope:** `server.js`, `cspReport.js`, rd735 (added), rd618 (R7 regex + comment), counts; no route added or removed (a census of `app.post(`/`app.get(` at `874c4f5` and head, equal).
2. **POSITIVE CONTROL FIRST (e0):** red at P_B; then e1-e6, f1-f4, r1-r4, x1-x3.
3. **(a) the budget shape (e2-e5)** — defeated or not, by which route (many addresses, eviction, window edge, clock), each with its evidence class.
4. **(b) A-F2r's fallback (f1-f3)** — every shape that keeps userinfo, named; the trade-off (f2) quoted.
5. **(c) M3b (r1-r3)** — re-derived; the slip's non-isolation shown.
6. **(d) L-B1 (x2)** — rd646 on MT2, and the 503-vs-429 order MEASURED.
7. **PRIOR WORK (C-49/C-50):** the READY says `buildCspEntries`, `stripQueryAndFragment` and the intake are KEPT, the limiter unchanged, "Nothing removed" — READ the diff: every `-` line quoted with where its
   behaviour lives now; the limiter block at `874c4f5` and head identical (quote the blob range).
8. **C-190 (READ ONLY):** no PR → CodeQL NOT RUN; the READY's "anchored and linear" regex claim → f4's PROBE.

## 8. THE MERGED TREE (C-68, C-57, C-89, C-104, C-112, C-133, C-187). No verdict is complete without it.
1. **Build it in YOUR OWN scratch clone** under `projects/nexusai/qa-trees/batch11.*/clone-1`: `git clone --shared --no-checkout <repo> <dir>`; in the clone only: remove `origin`, set a local
   `user.name`/`user.email`, `gc.auto 0`, `core.fsmonitor false`, hooks off; `git checkout -b gate <M0>`; then `git merge --no-ff` in the PROPOSED ORDER: **`874c4f5`** (MTa), **`7d853b0`** (MTb), **`67b840b`**
   (= MT1); then, in a SEPARATE clone (`clone-x`) built from MT1's commit, `git merge --no-ff 608a1cd` (= MT2; skip if M0 already holds it). **Write your prediction for each merge BEFORE it; anything other than the
   counts file conflicting STOPS (C-57).** Re-measure every pair by `merge-tree --write-tree` in a SCRATCH object dir first. **C-104: resolve and stage before any census or run.**
2. **Resolve the counts file by REGENERATION, never by hand:** take a side (a placeholder) to complete each merge commit, then `npm run verify -- --maxWorkers=2 --forceExit --update-counts` ONCE on MT1 after all
   three merges, through the lock, SESSION_SECRET UNSET, under its deadline; commit the regenerated file in the clone. **Predicted 4242/257 at M0 = `5531d7b`.** Then a plain verify of the committed head.
3. **Order independence (a control that can fail):** clone-2 in REVERSE (`67b840b`, then `7d853b0` — which brings `874c4f5` with it). **The two `HEAD^{tree}` must be identical apart from the counts file** — quote both
   tree ids and the `git diff --name-only`; the side control run INSIDE the clone that owns both.
4. **Blob identities (C-133's C-112 control):** member paths at MT1 == their head's blob (`bb45cd7`, `a17dd70`, `252bf5a`, `27419fe`, `4711147`, `1988b46`, `6ae80ce`, `6608eae`, `4925b58`, `1007b66`); **`backend/server.js` a
   COMBINED blob (name it; neither `0d7e387` nor `86dc63f`)**; `image-content-exposure` = M0's `7e3262b`; every other `__tests__` file == M0's or a head's; `package-lock.json` `9064763`. **`__tests__`: 301 at MT1, 303 at MT2
   predicted.** **The census's "M0 left out" control must FIRE for this parent set** — redo it with A only / B only if it reads 0.
5. **id-superset control (C-57) with C-187's ADDENDUM — ruling (e): PREDICT, then measure, all K1.** merged ids ⊇ ids(M0) ∪ ids(`874c4f5`) ∪ ids(`7d853b0`) ∪ ids(`67b840b`)? **Predicted: missing 2 = C-187's pair
   (from the `874c4f5`/`7d853b0` side, `94e6e4c`), new ids 32 (rd591 13 + rd618 13 + rd735 6) = the counts delta.** The pair is ACCOUNTED only when each is MEASURED: **(a1)** base = branch = `94e6e4c` (`1904765`,
   `874c4f5`, `7d853b0`); **(a2)** merged = M0's `7e3262b` = RD-466's head blob; **(a3)** `git log 1904765..<M0> -- __tests__/image-content-exposure.test.js` lists only `8de8e5c` and `3f7e263` (MEASURED by the drafter
   at `5531d7b`); **(a4)** RD-466 changes no title in that file (id set equal by name to `9ede5fd`'s); **(b)** the replacement ids present and green on MT1. **Any other missing id is a STOP.** Use a COPY of batch 10's
   `qa-c57-id-superset.sh` (keeps the lock-holder refusal; proven first to STOP on a planted missing id and to pass a superset).
6. **The semantic overlaps git cannot see (C-68), ONE hold:** on MT1 — every C-68 set of the MERGE ORDER table BY NAME (per-file counts), rows g6 (MT1 arm), x1, x3, e1, r1, the full verify. On MT2 — x2. Then ONE mutant
   per ticket on MT1: **g9's M-c** (B6 red) and **e6's M1** (B1, R8 red).
7. **C-89 on your clone:** `git diff --quiet HEAD` holds; `git show HEAD:scripts/verify-expected-counts.json` equals the regenerated counts.
8. **Main at your END:** `git merge-tree --write-tree` (scratch objects) of each member onto the END main — counts-only? any combined blob named.
9. **Nothing leaves your clone.** No push, no remote, no PR, no ref written in NexusAI. **Count `<repo>/.git/objects` files before and after your whole session and account for any delta by FULL-DATE mtime** (live seats
   commit and merge there tonight; `--shared` clones and merge-tree freshen mtimes — say so).

## 9. CI (C-185, C-190) — NOT RUN AT ANY BRANCH HEAD (no PR exists)
- **Drafter (READ ONLY, NexusAI's own `GH_CONFIG_DIR`, ~01:52 AEST):** `gh pr list --head <branch> --state all` returned `[]` for `rd-591-worktree-band-s86n`, `rd-735-csp-intake-residue-r3-s86m` and
  `rd-618-csp-intake-residue-s86m` (control: without `--head` it returned #34 and #33). **CodeQL is NOT RUN at either member head.** M0's Build `36589067630` (headSha `5531d7b`) was `in_progress`.
- **Re-read with `gh` READ ONLY:** whether a PR now exists for either branch (a PR opened by the merge author mid-gate is theirs — read it, do not touch it); for any PR, its CodeQL `Analyze (<language>)` runs (C-190: the
  `CodeQL` summary run can read completed/neutral before the analyses exist) and any NEW high-or-higher alert in changed code; M0's Build `36589067630` conclusion and failing set against C-185's set.
  **`gh` never merges, approves, comments, reviews, labels, re-runs, dispatches, sets a variable, dismisses an alert or opens a PR.**
- **CI and RD-591 (L-A4):** CI's Linux runner, its `lsof` and its `ps` are UNVERIFIED until a PR's Build runs; say so in the verdict line.

## 10. Floor discipline — THE FOUR CLAUSES, plus MERGES GO FIRST and THE DEADLINE RULE
1. **MERGES GO FIRST (ruling i).** **The jest lock `session-tools/nexusai-lock.sh` (queue `session-tools/locks/queue-jest/`) is shared with FOUR builder seats doing merges one at a time tonight.**
   - **Do ALL lock-free work first:** pins, reads, merge-trees in scratch objects, unit-level rows on `createCspEntryBudget` and `stripQueryAndFragment` run with plain `node` (no jest, no server), census greps, prior-work reads, the f4 probe, g8.
   - **Then file ONE hold**, tagged `qa-b11-…` (e.g. `qa-b11-H1-hold`), as a tracked child of your seat. **If a MERGE ticket (a tag containing `merge`) is queued AHEAD of you, you wait behind it (that is FIFO). If a MERGE
     ticket FILES BEHIND YOU BEFORE YOUR HOLD IS GRANTED, re-file your ticket behind it:** stop YOUR OWN unstarted waiter (its ancestry proven to reach your claude pid — C-174: by pid, never by pattern), confirm your
     ticket went to `released/` as `ticket-left-*`, and re-queue with `--after <that merge ticket's tag>` (C-141 ADDENDUM 4's tool). Record each re-file (time, the merge tag, your new position). **Once your hold is
     GRANTED, carry on** — a running hold is never interrupted.
   - C-141: your hold is gate-class; builder PROOF tickets self-apply a yield to it (ADDENDA 2/3). **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another seat's process, lock directory, owner file or
     ticket, even if it looks stuck; if a holder looks stuck, mail a QUESTION (§12) and keep waiting.
2. **Hold the lock ONCE per multi-run measurement** (one hold for the whole gate is the target). Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`).
3. **Count foreign servers the C-125 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND the server entry point anywhere in the remaining argv; "ours" = the ancestor chain CONTAINS your own
   claude pid. **Record the foreign count BESIDE EVERY RESULT.** **NEGATIVE controls, all in the same run, all must classify FOREIGN:** `62649` (NexusAI-M), `9959` (NexusAI-N), `38362` (NexusAI-O), `20317` (NexusAI-P), `62677` (Tuesday s94) — Tuesday named the live seat pids at stamp (NexusAI-M, -N, -O, -P and her own)
   at stamp, each in backticks. Re-read them at start; if one has exited, say so and use the others; **a hold with NO live negative control aborts.** Reuse batch 10's instrument BY COPY with YOUR pid as `ROOT` and
   these as `NEG`: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch10/evidence/qa-floorlib.sh`
   (**its defaults are STALE — `ROOT=50957`, batch 10's seats — correct `ROOT` and `NEG` before any hold**) and `…/qa-floorcount.py`; the original counter is gate 7's
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`. **Also count every dialer process you start (g3) by pid from your ancestry, and prove 0 left after each run.**
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, "0 refused" (g3's control dialer refused), "LOST 0" (a planted lost cell caught by your compare), "missing 2 / other 0"
   (the planted-missing-id control), "userinfo absent" (f1's plain control), "guarded by no cell" (the mutant LANDED and parsed).

**5. THE DEADLINE RULE — every real-server probe, every dialer and every request has a per-step DEADLINE, a HEARTBEAT, and kills its server in a `finally`.**
Every HTTP request carries a client timeout; each step (boot 120 s, request 30 s, dialer run 180 s, targeted jest 600 s, C-68 union 2,400 s, full verify 2,700 s, exit 25 s) has a written DEADLINE (`qa-to.sh`);
a step past it is ABORTED and reported, never waited on. **Log a HEARTBEAT line at least every 2 minutes during any hold (H-4: a separate child, ≤ 120 s max gap, aborted if absent at 90 s); a step with no heartbeat
for 5 minutes is aborted and reported,** and a hold that is not progressing releases the lock. Every server, socket, dialer and child you start is killed in a `finally` (SIGTERM, then SIGKILL after a grace)
**by pid from your own ancestry, never by pattern (C-174)**, and the reap is confirmed by your floor counter. **H-20 and H-21 apply to every jest.**

## 11. HELD
- **LOCAL RUN, NOT THE DEMO:** every server request goes to a server YOU (or a cell) booted on 127.0.0.1 from YOUR tree. **g3's dialer dials only `127.0.0.1:<the stand-in's port>`.**
- **External hosts you MAY contact, and nothing else:** `git ls-remote origin` (pins, C-192 retries); `api.github.com` via `gh` READ ONLY (§9); `api.agentmail.to` (your verdict mail and any QUESTION).
  **No Azure, no npm registry, no CDN, no demo, no customer-test tenant, no Entra tenant, no Partner Center, no docker, no Redis other than the cells' own fakes.**
- **FINDINGS-ONLY (ruling f):** no fix, **no merge outside your own clones, no push, never push — not to main, not to ANY author's branch**, **no PR opened, commented, approved or merged (C-190 is the merge
  authors' route, not yours)**, no deploy, **nothing to Partner Center, the demo or production**, no money, no external comms, no mail to any human. **No `az` at all.**
- **Never write into** the builders' `session-tools/` (copy, then hash at start and end) or any `worktrees/` directory; **never run the builders' hold, preload or guard-arm scripts.**
- **Symlinks, chmod, sockets, held ports, dialer port files, env files and scratch git repos live ONLY under your own mktemp dirs.**
- **Findings-only:** do not commit (outside your clones), move any branch, file a ticket, or write anything inside the NexusAI project (`2_Project_Files`, `session-tools/`, `worktrees/`, `1_Project_Definition/`,
  `qa-reports/`). **NEVER `rm`** — quarantine, per the template §5.

## 12. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-30-gate-batch11/report.md` — ONE report covering both members; evidence in `./evidence/` beside it.

**Questions:** your routing name is **`QA/NexusAI-batch11`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by) and **PROCEED ON THE SAFEST READING without waiting**;
Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning `[Tuesday -> QA/NexusAI-batch11] ANSWER`. Approval-class items (anything
touching the demo, Azure, Partner Center, money, or a human) are NOT RUN and named. Record every question, reading and answer. An ADDENDUM mailed from `tuesday-agent@` supersedes the launcher's closing lines, whatever its subject's arrow says.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 11: RD-591 · RD-735`
Lead the body with ONE line per ticket in this form — `RD-591: <GO|GO WITH FINDINGS|NO GO> @ 67b840b (g3 foreign-vanished counted: <yes|no>; rd549 red arm on envReached: <yes|no>; LOST <n>)` · `RD-735: … @ 7d853b0
(budget defeated by: <none|route>; userinfo kept in: <n> shapes; rd646 on MT2: <n>/<n>)` — then one line naming M0, the merge order you recommend, the merged counts you measured, the C-57 result (missing / accounted / other),
and "CodeQL NOT RUN (no PR); CI lsof UNVERIFIED". Never `wednesday-agent@`. AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute: the QA project has none).
Never put the key, a token or any secret in a mail or the report.

Verdict format:
- **RD-591** naming `67b840b89b755b59268873a544b8d5ddd7ee54e0`: g0-g9, s1-s2; the limits L-A1..L-A8.
- **RD-735** naming `7d853b0e0b666b37d220dd05ac0727b5160555d2`: e0-e6, f1-f4, r1-r4; x1-x3; the limits L-B1..L-B5.
- **The merged tree (§8):** M0; both orders; counts regenerated once (measured vs 4242/257 re-based on M0); the id-superset result with C-187's (a1)-(a4)/(b); the C-68 sets by name; one mutant per ticket; C-89; the END-main
  merge-trees; the object-count accounting; **your recommended merge order.**
- **The §3b sweep:** per ticket, population / negative cells / still reaching / disarmed.
- Each of **L-A1..L-A8 and L-B1..L-B5** answered: discharged with a measurement, or left standing and named (C-112).
- All refs as **three timestamped readings (start / mid / end)**, each with its branch name and C-192 attempt count.
- **§3a H-1..H-26:** for each, that it was followed, with the self-test outputs (H-1), landing controls (H-3, H-10), max HB gap per hold (H-4), byte checks (H-9), the g0 decision (H-23), every deadline that fired
  (H-20) and every restore hash (H-21). **§10: every lock re-file, with the merge tag it went behind.**
- Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED / READ ONLY**. Severity is yours; priority is Tuesday's.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Not tested by this gate: Linux or CI at any branch head (no PR exists, so no CI Build and no lsof/ps on a Linux runner), CodeQL at any head without a PR, two real concurrent seats' full suites against each other, multi-replica deployments, a real ingress in front of the CSP intake, a real Redis, any browser, the npm registry, any deploy, docker, real Azure, Partner Center, the demo, and Windows.

## WRONG OR UNVERIFIED IN THE COMMISSION AND THE READYS — carried so the gate inherits the corrections
1. **RD-591 READY :2 "(main faea66b merged forward)"** — TRUE of `5e00f0a` when main was `faea66b`; **main is now `5531d7b`** (RD-204, RD-466). A is NOT forward-merged onto M0; merge-base(A, M0) = `faea66b`. The gate measures the merged tree.
2. **RD-591 READY :2 "tier 2 by the lane plan"** — Tuesday ruled **TIER 1** (the commission). The READY itself invited it ("Your call if its scope … warrants tier 1").
3. **RD-591 READY :16 "READY verify at 67b840b's tree"** — the round-7 hold (`r7-hold.out`) ran on **`HEAD 5e00f0a dirty`** (M `test-server.js`, rd549, counts) from 15:02:49Z to 15:43:46Z; `67b840b` was committed at
   **15:45:04Z, after it**. The verified content is presumably the committed content — UNVERIFIED by the drafter (the builder's worktree was not read); your own verify of `67b840b` decides.
4. **RD-591 READY :13 "The rd549 red arm (a requester-side 3 s connect delay) -> C2/C10 and O4 red"** — CONFIRMED in the builder's log as an `envReached` assertion (C2/C10 in 6 ms), not a timeout (§1). **Its preload rode
   `NODE_OPTIONS`** (H-15's one declared exception covers your re-derivation only if argv is impossible).
5. **RD-591 READY :26 "rd554-restore-harness's header"** — the sentence is in `__tests__/helpers/rd554-restore-harness.js` (a helper, blob `028fa30` at A and M0) at **:88-89, inside a "RESIDUAL, STATED RATHER THAN HIDDEN" comment block**, not a file header.
   And it becomes false only for runs in DIFFERENT slots (row g7 (v)).
6. **RD-591 READY :22 "Scanned all 25 guarded test files"** — UNVERIFIED which 25: the drafter counts **6 test files calling `guardServer`** (rd486, rd516, rd523, rd545, rd549, rd591) and **21 non-helper files using `listenInBand`/`listenOnReservedPort`** at the head. g7 re-derives.
7. **RD-591's own helper comment "Two worktrees can still hash into one slot (1 in SLOT_COUNT)" (test-server.js :58)** — true for ONE PAIR; the floor has many worktree roots (the NexusAI `worktrees/` directory lists well over a hundred), so a shared slot among the LIVE ones is likely. g8 measures.
8. **RD-735 READY (iii) "backend/server.js (+19/-4)"** — MEASURED **+18/−5** (`git diff --numstat 874c4f5 7d853b0`). Cosmetic. `cspReport.js` +49/−6 matches.
9. **RD-735 READY :12 "an ambiguous forged value such as https://h?x=a@b is logged as https://b"** — that value PARSES under `new URL` (READ), so it takes the parsed branch; the trade-off applies to UNPARSEABLE variants. f2 measures both.
10. **RD-735 READY "the budget … per process, which is the ring's own scope"; server comment ":1131 (because trust proxy=1) which is set by the ingress, not by the client"** — true behind an ingress; **with no ingress (the local run,
    and any deployment without one) `req.ip` comes from the client's own `X-Forwarded-For`** (READ, express semantics) — e3 measures; the Marketplace ingress shape is READ ONLY here.
11. **Commission "C-187 … "** — not in the commission; **added by the drafter:** B and RD-618 are cut from `1904765` and C-187's ADDENDUM names `874c4f5` by sha, so the C-57 prediction is **missing 2 (C-187's pair), accounted on (a1)-(a4)/(b)**, not missing 0.
12. **Drafter's own slips, disclosed:** (H-18) one `cat …; echo =======; cat …` in the default zsh died on `=======` after printing the first READY (re-read the second READY alone); one `timeout` call failed (macOS has none; re-issued without);
    the project's hook refused one `cd` (re-issued with absolute paths). One `rev-parse <sha>:<path>` table printed the SHA ITSELF for paths absent at a commit (rev-parse echoes an unresolvable argument) — re-read with presence checks
    before any blob in this brief was written. **No `merge-tree --write-tree` was run by the drafter (its commission forbade it):** every merge prediction here is the READ-ONLY three-argument form, and the launcher's guard 80 uses the same.
    No recursive search of any project tree (single-directory `ls` of `session-tools/`, `session-tools/s86n/rd591/`, `session-tools/s86m/`, `worktrees/`, the batch 10 evidence dir only).
    While testing the launcher: macOS bash 3.2 brace-expanded a double-quoted `{a, b}` pattern nested inside `$(…)` (fixed with single-quoted variables), and the drafter's own
    file tool turned a literal backslash-u-0020 into a space (the launcher builds that pattern with `printf`). Four scratch files the drafter wrote while debugging sit in the
    system `$TMPDIR` (`b11dbg.sh`, `t94.sh`, `t94b.sh`, `lm.out`; not deleted — the fleet's no-rm hook refused, as it should).

## PROVENANCE (drafter, 2026-09-30 ~01:47–~02:40 AEST, read-only; EXACT times only where a `date` call stamped them, the rest "~")
- origin refs | `git ls-remote origin` (one call; `refs/heads/*` filtered, `refs/pull/*/head` all) | **01:48:06 AEST** (date-stamped; first attempt, no publickey denial)
- every pinned sha a commit; chains, parents, dates, messages; merge-bases | `cat-file -t`, `log --format='%h %p %ci | %s'`, `merge-base` | ~01:49
- counts at 10 shas; deltas and numstats; main's movement `faea66b..5531d7b`, `1904765..5531d7b`; path overlaps | `git show` + python, `diff --numstat|--name-status|--name-only`, `comm` | ~01:50–~01:53
- merge predictions (6 pairs) | `git merge-tree <base> <a> <b>` (three-argument, read-only, no objects written), parsed for `+<<<<<<<` per path | ~01:54
- blobs (test-server, stand-ins, rd591, rd618, rd735, rd646, server.js, cspReport.js, ICE, dom.js, image-manifest, rd395 harness, rd554 harness, lock) | `git rev-parse` | ~01:55–~02:20
- RD-591's diff of the five stand-ins whole; `test-server.js` :44-100 and :202-430 at A; rd549 :52-130 and every `envReached`/`readyAt` line; rd591 titles; rd554 harness :84-92 | `git diff`, `git show`, `grep -n` | ~01:58–~02:15
- RD-735's product diff whole; `cspReport.js` rate/cap lines; `server.js` `trust proxy` (:1120) and limiter lines; rd735/rd618 requires and titles | `git diff`, `git show`, `grep -n` | ~02:00–~02:20
- test-server require-population at 5 shas; `guardServer`/`arrivalTime`/`listenInBand`/`reservePort` users at A; `__tests__` counts at 7 shas | `git grep -l`, `ls-tree -r -z` | ~02:10–~02:20
- CLARIFICATIONS: size/mtime/lines; C-numbers' line numbers; C-49, C-57, C-68, C-102, C-104, C-112, C-115, C-125, C-130, C-133 headlines; C-141 + ADDENDA 1-4, C-173, C-174, C-177 + CORRECTED + ADDENDUM, C-184-C-192 read whole | `ls -l`, `wc -l`, `grep -n`, `sed -n` | ~01:55–~02:05
- the batch 10 report §0-§3, §14-§16 (whole sections); the batch 9 report finding lines (:11-:28, :83, :242-:249) | `sed -n`, `grep -n` | ~01:50, ~02:08
- builder evidence: `s86n/rd591/` listing, `lookup-cost.out`, `r7-hold.out`, `r7-hold.sh`, `r7/2-redarm.log` (the failure lines), `slow-connect-preload.js`; `s86m/` listing, `rd735-hold.log` (Tests/VERDICT lines), `rd735-m3b.log` (whole), `rd735-verify-full.log` VERDICT | `ls -la`, `cat`, `grep` | ~02:05–~02:15
- CI: `gh pr list --head` ×3 + control; `gh run view 36589067630` | `gh`, READ ONLY, NexusAI's `GH_CONFIG_DIR` | 01:52:13 AEST
- `/bin/ps` setuid, `/usr/sbin/lsof` not | `ls -l` | ~02:06
- routing: **no `QA/NexusAI-batch11` line in `fleet/inbox_routing.conf`** (batch10 :151 exists) — Tuesday adds it; the launcher's guard 40 refuses until then | `grep -n` | ~02:20
- report dir `2026-09-30-gate-batch11` absent | `ls -d` | ~02:07
- the batch 10 brief (626 lines) and launcher (646 lines) whole | `Read` | ~01:47

## FILL AT STAMP — Tuesday, before launch (the launcher refuses until the starred items are done)
- ★ both STAMP placeholders at the top (the SELF-CHECK line and the Self-check note) — LAST, by hand, no placeholder token in the note.
- ★ the routing line `QA/NexusAI-batch11|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`.
- ★ the negative-control seats in §10 (replace the stamp placeholder there with the pids, each in backticks) AND the launcher's `NEG_SEATS` — Tuesday's own pid included.
- If RD-618 or RD-646/647 LANDS on main before launch: the launcher prints a NOTE (not a refusal); the gate skips that merge step and re-bases (ruling b). If a member head MOVES before launch: the launcher's guard 18
  refuses — re-pin that head in the launcher and every occurrence in this brief, re-read its READY, never `sed` a sha blindly.
