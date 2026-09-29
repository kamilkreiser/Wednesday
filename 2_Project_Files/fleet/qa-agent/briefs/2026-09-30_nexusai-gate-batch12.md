# QA Agent Invocation Brief — Datasec/NexusAI, ONE batched gate "batch 12": RD-591 (TIER 1) + RD-735 (TIER 2, on RD-618 round 2) + RD-657, RD-649, RD-608, RD-653, RD-671 (TIER 2) — seven verdicts, one report

**Drafted for Tuesday 2026-09-30 ~09:10–~10:30 AEST by a read-only drafting agent; Tuesday reviews, stamps and launches.**
Commissioned on Tuesday's batch 12 commission (2026-09-30 ~09:1x AEST). Seven READY mails on disk, each read WHOLE by the drafter (all in `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/`):
- **A — RD-591** @ `67b840b89b755b59268873a544b8d5ddd7ee54e0` (`rd-591-worktree-band-s86n`; merge-base with main `faea66b`, six commits incl. two forward merges) — NexusAI-N (S86N) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd591-READY-mail.txt`
- **B — RD-735** @ `7d853b0e0b666b37d220dd05ac0727b5160555d2` (`rd-735-csp-intake-residue-r3-s86m`, ONE commit on **RD-618 round 2 `874c4f503d0f37a032014e562972b17e903e1072`**, cut from `1904765`) — NexusAI-M (S86M) —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd735-READY-mail.txt`
- **C — RD-657** @ `5584ea45617477338c2b5a01a0011cc92158a7f0` (`rd-657-health-version-from-package-s86m`, ONE commit on `5531d7b`) — NexusAI-M (S86M) — PRODUCT (`/api/health`'s version) + `package.json` + `package-lock.json` —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd657-READY-mail.txt`
- **D — RD-649** @ `20fea841f5723ebd2981836a41a779b7d88f44dd` (`rd-649-csp-limiter-at-load-s86n`, two commits on `67e8928`) — NexusAI-N — TEST-ONLY —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd649-READY-mail.txt`
- **E — RD-608** @ `9fd5c9a34af35358fbad704a173910bb9c1aee3c` (`rd-608-limiter-census-s86n`, two commits on `67e8928`) — NexusAI-N — TEST-ONLY —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd608-READY-mail.txt`
- **F — RD-653** @ `8bc88f5c1835e3d0b7e7ef124717973d733fc90c` (`rd-653-rd408-length-scan-s86n`, two commits on `67e8928`) — NexusAI-N — TEST-ONLY —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd653-READY-mail.txt`
- **G — RD-671** @ `3ef057f343c2cc9f93ab416d2c420646d8c349d0` (`rd-671-rd665-rule-tighten-s86n`, two commits on `ca7de45` = today's main) — NexusAI-N — TEST-ONLY —
  `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-rd671-READY-mail.txt`

**This gate SUCCEEDS gate 11** (`QA/NexusAI-batch11`, RD-591 + RD-735), which ended UNFINISHED: no `report.md`, no verdict. It was stopped by Opus 5.5's safeguards on its attack-style rows and parked at a model-switch dialog (THE MODEL RULE, below). **Gate 11's brief is the base for members A and B: its rows for them are carried here verbatim (§1 TARGET A/B, §2a G/S/E/F/R/X, §3a, §3b, §4, §5).** Its evidence may be REUSED only as PRIOR measurements you re-check (H-29), never as a verdict.
**Batched under the 2026-09-18 batch-gates rule, as batches #1-#11.** The members share NO path but the counts file, except **`backend/server.js`, shared by B (with RD-618 under it) and C** (and by the cross partner RD-646/647 `608a1cd`) — MEASURED, §1. They share SEMANTIC surfaces: A's rewritten port helper is under every server-booting cell of B, C, D, E and F (C-68, row X and rows y1-y4).
**Every head is re-read by `git ls-remote` in the launcher (retried under C-192), which refuses on a mismatch.**

SELF-CHECK: re-read end-to-end for contradictions | Tuesday s94, 2026-09-30 09:36 AEST
Self-check note: Tuesday read this brief WHOLE (2026-09-30 09:36 AEST) after the drafter's WRONG list. Two stamp rulings: (1) WRONG 9 RULED — RD-657's rd327 R7 retitle is AUTHORISED: C-181 required R7 to be re-anchored, so the rename is the ticket's own ruled change; it is ACCOUNTED only when §8.5's blob conditions hold (merged rd327 = b34b7d7; the other side = base a4db84d; the new R7 present and green on MT1) — no QUESTION needed. (2) WRONG 4 CORRECTED — gate 11 was stopped by the safeguards FOUR times (02:33, 02:37, 02:41, 02:45 AEST, counted by Tuesday in gate 11's session transcript); only two were recorded on disk. RD-614 is NOT a member (it needs a browser leg; ruling (a) says none) — it goes to a later gate. No contradiction found otherwise.

## TUESDAY'S RULINGS (the commission; carried in substance — the gate applies them, it does not re-rule them)
- **Tiers.** **RD-591 is TIER 1 (through-code, no browser)** — Tuesday's ruling of gate 11, carried: the guard decides whether SECURITY cells (the SSRF stand-in in rd516, the redirect stand-in in rd523, rd545, rd549) can pass for the WRONG reason. **RD-735 is TIER 2 (through-code)**, its budget SHAPE the gate's to judge (ruling c). **RD-657, RD-649, RD-608, RD-653 and RD-671 are TIER 2 (through-code)** — each READY's own proposed tier, adopted by the commission.
- **(a) ONE gate session for all seven, through-code only.** No browser leg. Servers are booted by the cells themselves (or by your own driver) on `127.0.0.1`, from YOUR OWN trees. **Never the demo, never any non-loopback host** (§11).
- **(b) Main is `ca7de45` at commissioning** (the drafter's `git ls-remote` 2026-09-30 09:10:39 AEST, first attempt: `main` = `refs/heads/rd-197-emphasis-ground-guard-s84p` = `refs/pull/36/head` = **`ca7de453bea6e2c43657fc57104df8250959e72f`**). **RD-197 landed** (merge `c0cff62`, counts `ca7de45`, 4230/255); before it **RD-466** (`5531d7b`) and **RD-703** (`59c7fdc` merge, `67e8928` counts, 4221/254). **MERGES ARE STOPPED until NexusAI-P reports on rd549 O4 (ruling j)**; when they restart they go one at a time. **Take M0 = origin main AT YOUR OWN START by `git ls-remote`, say so, and RE-BASE EVERY PREDICTION in this brief on it.** If RD-618 (`874c4f5`) or RD-646/647 (`608a1cd`) or RD-732 (`daf2210`) is already on M0, say so and re-base. Re-read main at start, mid and end. Never re-base mid-gate.
- **(c) RD-735's design choice is a SHAPE the gate judges.** The builder took "a per-address entry budget" instead of "one limiter token per stored entry". The gate does not re-open that choice; it tries to DEFEAT the shape as built (rows e1-e6) and reports what defeats it.
- **(d) C-190: every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes (test code included). The gate itself NEVER opens, comments on, approves or merges a PR.** No PR exists for any of the seven branches or for RD-618 (drafter, `gh pr list --head <branch> --state all`, READ ONLY, NexusAI's own `GH_CONFIG_DIR`, ~09:11 AEST: `[]` for all eight; control without `--head` returned #36, #35, #34 MERGED) — **CodeQL is NOT RUN at any member head; say so.**
- **(e) C-57 on the merged tree, with C-187's ADDENDUM and one rename the drafter adds:** B and RD-618 are cut from `1904765` and carry `image-content-exposure.test.js` at `94e6e4c`; M0 carries RD-466's `7e3262b`. **C-187's ADDENDUM APPLIES** ("the pair stays ACCOUNTED when main (or the merged tree) carries RD-466"). **RD-657 RENAMES rd327's R7** (old `R7 CONTROL — version keeps its meaning: still the product version 2.0.1` → new `R7 CONTROL — version keeps its meaning: it is package.json's version (one source, C-181)`; MEASURED by title diff `5531d7b → 5584ea4`) — **the drafter's reading, NOT a Tuesday ruling:** ACCOUNTED under C-133 on blobs + C-133's authorised-rename ADDENDUM, the "grant" being C-181's build condition that R7 be re-anchored in the C-131 shape. **Predicted missing 3 = C-187's pair + RD-657's old R7 title**; any OTHER missing id is a STOP. If you judge the R7 grant absent, it is a STOP you NAME and mail as a QUESTION (never a silent pass).
- **(f) The gate NEVER merges and never pushes. Findings only.** Merges exist ONLY inside your own scratch clones, as the merged-tree measurement (§8).
- **(g) STANDING (batch 7 ruling f): every jest run inside a hold gets `--forceExit` AND a hard deadline; every mutated file is restored in a `trap … EXIT`.** H-20 and H-21 (§3a).
- **(h) C-185 + its ADDENDUM:** main's CI known-failing set is **{rd638-export-always-ends E2, rd465-first-run-open-window O-1 "Turn on Authentication Control: success removes the banner"}** (O-1 ONLY while its failure is the `checkEntraStatus` TypeError). **RD-733 and RD-723 are not on M0 at drafting** (MEASURED: `git log 5531d7b..ca7de45` = RD-703 and RD-197 only), so the set stands. **rd549 O4 is NOT in it** (ruling j).
- **(i) MERGES GO FIRST on the jest lock** (§10 clause 1): lock-free work first; **the gate re-files behind any merge ticket filed before its grant; once granted it carries on.** Merge turns: P, M, N, O as the commission names them — the C-186 ADDENDUM at CLARIFICATIONS **:1933** (its duplicate note at :1939 cites it as ":1931", a line number the file has since outgrown) rules the order O, P, M, N, then O again, the turn passing after each green push Build.
- **(j) rd549 O4 on M0 — CAUSE UNDETERMINED; the gate must NAME O4's state on M0 and must NOT treat RD-591 as its fix unless it MEASURES cause (i).** Main's push Build **36635558304** on `ca7de45` (**attempt 1**, run started 21:47:11Z, completed 22:40:03Z, conclusion **failure**) failed **4229/4230** on exactly one cell: rd549 `O4 — open-mode config restored onto a deployment whose ENVIRONMENT carries sign-in: …`, diff `-"envReached": true` / `+"envReached": false` at `:482` (drafter, `gh api …/runs/36635558304/attempts/1` + the job log, READ ONLY, ~09:12 AEST; `Test Suites: 1 failed, 254 passed, 255 total` / `Tests: 1 failed, 4229 passed, 4230 total` / `VERDICT: FAIL — jest exited non-zero (1)`). **Attempt 2 (a RE-RUN) was `in_progress` at 23:11:57Z** — C-185: *no re-run is used as a clearance*; read its result READ ONLY and say what it is, never as a clearance. **NexusAI-P is measuring two causes: (i) jest-side handler lag — the stand-in's handler stamps `Date.now()` after `h.readyAt` although the server dialled before readiness (RD-591's `arrivalTime` accept-time stamp addresses this, at most); vs (ii) the server's env dial LANDING AFTER `readyAt` (RD-591 does not fix this).** P's result, if it arrives, is a CLAIM beside your own measurement (rows o1-o4). **Main's rd549 is UNGUARDED** (blob `4a35642`, `requests.push({ at: Date.now(), url: req.url })`, no `guardServer`; MEASURED) — so the guard's lookup delay cannot be O4's cause on M0.
- **(k) THE MODEL RULE (Kam, 2026-09-30 09:07, card (b)) — see the next section. It governs every row.**
- **(l) The shared `session-tools/s78g/c133-accounting.py` was REPLACED at 2026-09-29T23:07:38Z by RD-658** (C-133 condition (2) decided on BLOBS; sha256 **`6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f`** — MEASURED by the drafter, file mtime 2026-09-30 09:07:38 AEST). **Use it (BY COPY, hash the copy) and say which version you used** (H-30).
- **Launch order:** as a gate slot frees; the launcher re-pins heads at launch and reads main as it finds it.

## THE MODEL RULE (Kam, live board 2026-09-30 09:07, ruling card `nexusai-gate11-opus55-safeguard-model-switch`, option (b)) — REQUIRED READING before any row
Kam's words, verbatim: *"Decision nexusai-gate11-opus55-safeguard-model-switch: b — Let QA gates switch to Opus 4.8 when flagged"*. Option (b) read: *"Answer that dialog per session (not 'switch automatically' for every seat), so the attack-style rows can run."* (Recorded in Tuesday's lesson `0_Brain/learnings/…_qa-gates-may-switch-to-opus48-when-flagged.md`, commit `623db55e4`.)
1. **The gate runs the FULL rows, including the attack-style ones** — e2-e4 (the forged-address budget attacks), f3-f4 (the userinfo shapes and the 16 KB timing inputs through the intake), g3's outside dialer, and every other row in §2a. Nothing is narrowed because it might be flagged. **Every row is an authorised, findings-only measurement against YOUR OWN loopback servers built from YOUR OWN trees** (§11).
2. **If one of your responses is stopped by Opus 5.5's safeguards, you STOP that step** (it is NOT RUN, and it is not re-worded to slip past), **write ONE line to `evidence/classifier-stops.txt`** (`<AEST timestamp> | <row id> | stopped by the safeguards while composing <what> | model <name> | NOT RUN`), **mail Tuesday a STATUS** — `tuesday-agent@agentmail.to`, subject exactly `[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch`, body: the row, the time, whether a hold is running and what it is doing — **and WAIT** (end your turn with the line `PARKED: flagged — awaiting the Opus 4.8 switch`).
3. **Before you park, release what you hold:** let a RUNNING jest step finish under its deadline, then let the hold exit through its own path (H-28) — **never sit parked holding the jest lock** (gate 11 sat at the dialog holding the lock while merges waited).
4. **Tuesday switches THAT pane's model** (the session's own model switch) and taps you with a mail naming the switch. **You never answer the model dialog yourself, and nobody ever chooses "Switch automatically"** (a persistent setting shared with the coordinator seat — outside Kam's per-session grant).
5. **After the switch, resume at the stopped row**, re-filing any hold behind merge tickets (§10). **The report must state which rows ran on which model** (a MODEL column in the row table: `Opus 5.5` / `Opus 4.8`, with the switch time), and quote `classifier-stops.txt` whole.
6. This is a grant for QA gates only, per session. It changes no other seat.

## Charter
Read `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` in full first. You are an independent tester. You did not build
these changes and you owe no builder anything. **Every line below that reports what a builder says is a CLAIM, never evidence.** Explore seven changes — a test harness
that bands ports by worktree and makes counting stand-ins REFUSE traffic from outside the test's process tree (A); a per-address stored-entry budget plus a wider userinfo
strip on the anonymous CSP intake (B); `/api/health`'s version read from `package.json`, which moves to 2.2.1 (C); a preload that proves the csp-report limiter is built at
load (D); a run-time census of the limiters on POST /api/setup/ai-test (E); a narrower length scan in rd408-r2 (F); a structural rule over the ARM template's availability
test (G) — looking for any state in which **a guarded stand-in counts a dial it should have refused, or refuses one it should have counted; a security cell goes green
because the GUARD dropped a dial rather than because the product never made it; a cell measuring arrival reads the guard's (or the event loop's) delay; any cell that passed
at main loses a pass or slows past its budget; one address (or many) stores more than the budget allows or evicts its own budget; a forged report keeps userinfo in the log
or the ring; health reports a version that is not package.json's; a preload's anchor misses and the cell passes anyway; a census or a length scan goes blind; a template
rule accepts a shape it names as refused; a cell is green while its named behaviour is broken; or the id set loses a test silently.**

- **RD-591 is TIER 1 (through-code).** Verdict: **GO / GO WITH FINDINGS / NO GO at `67b840b`**, plus its merged-tree result.
- **RD-735 is TIER 2 (through-code).** Verdict at **`7d853b0`** (with RD-618 `874c4f5` under it), plus its merged-tree result.
- **RD-657, RD-649, RD-608, RD-653, RD-671 are TIER 2 (through-code).** A verdict each at `5584ea4`, `20fea84`, `9fd5c9a`, `8bc88f5`, `3ef057f`, plus the merged-tree result.
- **One verdict PER ticket, one report, one mail.** A finding on one ticket never becomes another's verdict. RD-618 is NOT a member (batch 9 gated it GO WITH FINDINGS); it is the base B stands on, and the merged tree carries it. RD-732 is NOT a member (released; shares `package-lock.json` with C).
- **TIER 1 AND TIER 2 AT THROUGH-CODE WEIGHT, FINDINGS-ONLY:** no fixes, no pushes, no PRs, no deploys, nothing to Partner Center, the demo or production (§11).

## THE CLARIFICATIONS THAT BIND THIS GATE (opened by the drafter at source, ~09:15–09:25 AEST)
File: `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md` (350,166 bytes, 2020 lines, mtime 2026-09-30 09:08;
the last numbered entry is C-193 at :2015 — re-read line numbers, the file grows). **The drafter opened ONLY these (line numbers MEASURED):**
- **C-49** (:305) — the PRIOR-WORK check before rebuilding, replacing or removing anything (headline read).
- **C-57** (:416) — *"A merge conflict confined to `scripts/verify-expected-counts.json` is resolved by regeneration, with an id-superset control."*
- **C-68** (:663) — a verdict holds only at its head; *"a clean merge-tree and a changed measured surface are not in tension"*; re-run the affected cells BY NAME.
- **C-89** (:833), **C-102** (:951) *"every existing test that relied on a LATER return in that function is a candidate for silent disarmament"*, **C-104** (:978), **C-112** (:1147) *"A declared limit is where the evidence stops — not a place it is cleared."*, **C-115** (:1180) *"absence of a port clash is NOT evidence of a quiet floor."*, **C-125** (:1326), **C-141** (:1488) + ADDENDA 1-4 (:1496-:1509, the `--after` tool), **C-173** (:1777) item 9 *"band test ports by worktree (a stable hash of the worktree path) PLUS a stand-in that rejects and logs foreign traffic (C-115)."*, **C-174** (:1796) *"NEVER KILL BY PATTERN."* (headlines; C-173/C-174 as quoted).
- **C-133** (:1432) whole, its authorised-rename ADDENDUM (:1440) and its **RD-658 ADDENDUM (:1443)** — *"condition (2) is decided on BLOBS, and commit lists are evidence only"*; the script version (ruling l). **C-150** (:1578) whole — the same rule's origin.
- **C-177** (:1830) + its **CORRECTED** note (5 of 7 files) + its **ADDENDUM 2026-09-30** (:1844) — *"rd549 may stamp its env stand-in's request arrival at the socket's ACCEPT time"*, with Tuesday's conditions: *"a red arm with a REQUESTER-side delay must still read red"*; condition 3: *"proof that each stand-in's counted cells keep main's pass set."*
- **C-181** (:1877) whole — RD-657's ruling: health's version is package.json's, ONE source; package.json on main is "2.2.1"; the build conditions (R7 re-anchored in the C-131 shape with a red proof; one cell proves ONE source without grep); **not covered: the image label's IMAGE_VERSION**.
- **C-184** (:1904), **C-186** (:1926) + its ADDENDUM "THE TURN PASSES" (:1933; duplicate :1939-:1940) — merge turns (context for §10).
- **C-185** (:1913) + its **ADDENDUM** (:1919) — the known set (ruling h): *"O-1 counts as known ONLY while its failure is"* the `checkEntraStatus` TypeError; *"No re-run is used as a clearance"*.
- **C-187** (:1944) + its **ADDENDUM** (:1956) — ruling (e): *"the pair stays ACCOUNTED when main (or the merged tree) carries RD-466"*, conditions (a1)-(a4) and (b).
- **C-190** (:1979) — *"Every merge to NexusAI main goes through a PULL REQUEST, and a PR must add NO NEW high-or-higher CodeQL alert in the code it changes. Test code is included."*
- **C-192** (:2006) — a `Permission denied (publickey)` is TRANSPORT, retried up to 5 × ~10 s; *"a FAILED ls-remote is UNKNOWN, never a value."*
- **Not opened by the drafter, so not cited:** every other C-number (C-110, C-116, C-131, C-142, C-161, C-88 appear inside the entries above; read them if you rely on them).

## PRIOR ROUND
PRIOR ROUND (RD-591, RD-735): **gate 11 — UNFINISHED, NO VERDICT.** Brief `/Volumes/KK_T9_External_HDD/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-09-30_nexusai-gate-batch11-rd591-rd735.md`;
evidence `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-30-gate-batch11/evidence/` (no `report.md`). What it measured (READ by the drafter in `HOLD.out`, one hold `qa-b11-H1-hold`, granted 2026-09-29T17:31:58Z after 2775 s behind `s86o-merge-rd703`, controls fired, belt strict `{"testnet":"EPERM","loopback":200}`):
- **P1 full verify of `67b840b`** (K1 tree `k1-A-verify`, `HEAD=67b840b tree=13ac0b8`, `--maxWorkers=2 --forceExit`, SESSION_SECRET UNSET, unbelted), end 17:50:04Z: *"VERDICT: PASS — 4208/4208 tests passed across 254 suites (jest exit 0)"*; `vA-full.json` 4208 total / 0 failed / 254 suites (drafter parsed).
- **P1 full verify of `7d853b0`** (`k1-B-verify`, `HEAD=7d853b0 tree=2c50aed`), end 18:07:50Z: *"VERDICT: PASS — 4152/4152 tests passed across 249 suites (jest exit 0)"*; `vB-full.json` 4152 / 0 / 249.
- **P2 MT1 at gate 11's M0 = `5531d7b`** (clone-1 @ `51a8494` = `5531d7b` + `874c4f5` + `7d853b0` + `67b840b`): `--update-counts` *"VERDICT: PASS — 4242/4242 tests passed across 257 suites (jest exit 0)"* with *"expectation UPDATED — tests=4242 suites=257"*, committed in the clone as `b4e35d1`; C-89 `diff --quiet HEAD rc=0`; then the plain verify *"VERDICT: PASS — 4242/4242 tests passed across 257 suites (jest exit 0)"* (end 18:48:52Z).
- **Then the hold idled in `wait-P3` for 31 min (18:48:53Z → 19:20:07Z) holding the jest lock, and was TERMinated at 19:20:15Z** (`SIGNAL INT/TERM … restoring and exiting`; lock released). H-28 exists because of this.
- **`classifier-stops.txt`** (drafter read it whole): TWO lines — *"2026-09-30 02:41:25 AEST | response after reading ANSWER option-1 stopped by the safety classifier; … NOT RUN and not reproduced"* and *"2026-09-30 02:45:59 AEST | response after the hold was filed (ticket qa-b11-H1-hold, … queue position 1 behind s86o-merge-rd703) stopped by the safety classifier; … moving to the next row (C-57 part)."* **The commission and Tuesday's lesson say FIVE stops; only two are on disk — the other three are UNRECORDED (WRONG 4).**
- **Nothing else of gate 11 stands.** Its §2a rows (g0-g9, s1-s2, e0-e6, f1-f4, r1-r4, x1-x3) did not report; its census files (c68-*, g7-*, g8-slots, unit-b-*) were measured at gate 11's M0 `5531d7b` or earlier. **Its MT1 is STALE: M0 is now `ca7de45` (RD-703 and RD-197 landed since).** H-29 says how any of it may be reused.
PRIOR ROUND (RD-618 under B): **batch 9 gated RD-618 round 2 `874c4f5` GO WITH FINDINGS**; RD-735 is "the one follow-up ticket for batch 9's A-F1r, A-F2r, A-F3c and A-N2". Batch 9's report:
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch9/report.md` — findings A-F1r (:22), A-F2r (:23), A-F3c (:24), A-N2 (:26), A-N3 (:28) and its C-68 instruction (:83)
*"whichever of RD-618 and RD-646+647 merges second re-runs rd646 AND rd618 by name on the real merged tree"* (line numbers as gate 11's drafter measured them; re-read).
PRIOR ROUND (RD-657, RD-649, RD-608, RD-653, RD-671): **no prior gate for any.** RD-649 guards gate 6's mutant (iv); RD-608 builds on gate 1's `qa-limiter-census-preload.js`; RD-653 answers gate 7 r2's O-5; RD-671 answers the pkg221 gate's F-4 (each READY's own words, RELAYED).
PRIOR ROUND (method): the **batch 10 gate** is the most recent FINISHED NexusAI gate — report `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch10/report.md`
(self-corrections §15, S-1..S-8, folded into H-22..H-26 as in gate 11).
**Reuse instruments BY COPY** — gate 11's are the newest: `qa-floorlib.sh`, `qa-floorcount.py`, `qa-holdlib.sh`, `qa-to.sh`, `qa-jestwrap.sh`, `qa-jsum.js`, `qa-runj11.sh`, `qa-mut11.py`, `qa-mutlib11.sh`, `qa-merge11.sh`, `qa-verify11.sh`, `qa-build11.sh`, `qa-c112-census11.py`,
`qa-h1-selftest.sh`, `qa-h1-scan.py`, `qa-mailread.py`, `qa-ssprint.sh`, `qa-netbelt.sb`, `qa-netbelt-nodns.sb`, `qa-netbelt-ctl.js`, `qa-pin.sh` at
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-30-gate-batch11/evidence/`; and from batch 10 (not re-copied by gate 11): `qa-c57-id-superset.sh`, `qa-c68census.py`, `qa-mail.py`, `qa-cov-setup.js`, `qa-srvlib.js`, `qa-sweep-analyze.py` at
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-29-gate-batch10/evidence/`.
**Gate 11's `qa-floorlib.sh` defaults are STALE (`ROOT=${ROOT:-98861}`, `NEG=${NEG:-62649,9959,38362,20317,62677}` — gate 11's seat; MEASURED by the drafter) — correct BOTH.** The floor instrument this brief names:
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-30-gate-batch11/evidence/qa-floorlib.sh`; the original counter is gate 7's
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`.
**macOS has no `timeout` binary** (`qa-to.sh`: `perl alarm`, rc 142 = fired).

## 1. Targets — verified at drafting from the object store (09:10–~10:15 AEST)
**origin by `git ls-remote` at 2026-09-30 09:10:39 AEST (one call, first attempt succeeded):** `main` **`ca7de453bea6e2c43657fc57104df8250959e72f`** (= `refs/pull/36/head` = `refs/heads/rd-197-emphasis-ground-guard-s84p`) ·
`rd-591-worktree-band-s86n` **`67b840b89b755b59268873a544b8d5ddd7ee54e0`** · `rd-735-csp-intake-residue-r3-s86m` **`7d853b0e0b666b37d220dd05ac0727b5160555d2`** · `rd-657-health-version-from-package-s86m` **`5584ea45617477338c2b5a01a0011cc92158a7f0`** ·
`rd-649-csp-limiter-at-load-s86n` **`20fea841f5723ebd2981836a41a779b7d88f44dd`** · `rd-608-limiter-census-s86n` **`9fd5c9a34af35358fbad704a173910bb9c1aee3c`** · `rd-653-rd408-length-scan-s86n` **`8bc88f5c1835e3d0b7e7ef124717973d733fc90c`** ·
`rd-671-rd665-rule-tighten-s86n` **`3ef057f343c2cc9f93ab416d2c420646d8c349d0`** · `rd-618-csp-intake-residue-s86m` `874c4f503d0f37a032014e562972b17e903e1072` (B's base) · `rd-646-647-redis-fail-closed-recovers-s86m` `608a1cd99adcc69f6d2cdc552f170e89710adb02` (the cross partner) ·
`rd-732-ip-address-10-7-2-s86m` `daf221037d20966c64739d0e71e034ff516904b6` (C's lockfile neighbour, not a member) · `rd-703-wide-run-boundary-s86o` `67e8928…` (landed). **None of `67b840b`, `7d853b0`, `874c4f5`, `608a1cd` is an ancestor of `ca7de45`** (MEASURED). Every sha here is a commit in the local object store.
**Re-read at your start, mid and end, with C-192's retry. A moved TICKET head is a finding and a reason to stop, never a typo to fix. A FAILED ls-remote is UNKNOWN, never a value.**

**Main since gate 11's M0 (MEASURED, `git log --format='%h %p %ci | %s' 5531d7b..ca7de45`):** RD-703 `bd8e8cd` → merge `59c7fdc` (main `5531d7b` in) → `67e8928` (counts 4221/254) · RD-197 (seven commits from 2026-09-26, `7d87d74`…`43e729c`) → merge `c0cff62` (main `67e8928` in) → **`ca7de45`** (counts 4230/255).
Files: `__tests__/helpers/image-manifest.js`, `__tests__/helpers/rd703-parked-NOT-RUN/rd699-be-run-glue.test.js`, `__tests__/rd197-emphasis-on-notice-ground.test.js`, `__tests__/rd699-decode-branches-behaviour.test.js`, counts. **No member path, no `backend/`, no package file.**

**Chains and bases (MEASURED):**
- **A (RD-591):** `faea66b..67b840b` = six commits `c79926a`, `a2a93b2`, `4fcfbae`, `47d8855`, `5e00f0a`, **`67b840b`**; **merge-base(A, M0) = `faea66b`** (unchanged since gate 11). Not forward-merged onto `5531d7b` or `ca7de45`.
- **B (RD-735):** `874c4f5..7d853b0` = ONE commit; `1904765..874c4f5` = `7e4cd2e`, `4334b96`, `874c4f5`; **merge-base(B, M0) = `1904765`**. RD-646/647 `608a1cd` is ONE commit on `1904765`.
- **C (RD-657):** ONE commit `5584ea4` on **`5531d7b`** (2026-09-30 02:13:08 +1000) — NOT forward-merged onto `67e8928`/`ca7de45`.
- **D (RD-649):** `62385d9` (the change) → **`20fea84`** (counts) on **`67e8928`**. **E (RD-608):** `b896c7b` → **`9fd5c9a`** on `67e8928`. **F (RD-653):** `cdc6438` → **`8bc88f5`** on `67e8928`. None forward-merged onto `ca7de45` (RD-197 not in them).
- **G (RD-671):** `4088b20` → **`3ef057f`** on **`ca7de45`** — **G fast-forwards M0** (`merge-tree` M0 × G: no change in both; MEASURED).

**Deltas (MEASURED, `git diff --numstat <merge-base> <head>`):**
- **A:** as gate 11 (§ TARGET A below): `test-server.js` +251/−10, rd486/rd516/rd523/rd545 +2/−1, rd549 +3/−2, rd591 +345 (added), counts. 4195/253 → **4208/254**.
- **B over `874c4f5`:** `server.js` +18/−5, `cspReport.js` +49/−6, rd735 +144 (added), rd618 +3/−1, counts. 4146/248 → **4152/249**. (Over `1904765`, B+RD-618: `server.js` +58/−8, `cspReport.js` +106/−7, rd618 +194, rd735 +144.)
- **C over `5531d7b`:** `backend/server.js` **+3/−1** (`0d7e387` → `c9f0d65`: `version: '2.0.1'` → a comment + `version: require('../package.json').version,` at :18247) · `package.json` **+1/−1** (`cdb1168` → `384805d`: `"1.3.0"` → `"2.2.1"`) · `package-lock.json` **+2/−2** (`9064763` → `64d8eda`: ONLY the two root `"version"` lines, top level and `packages[""]`; READ whole diff) · `__tests__/rd327-build-digest-on-public-health.test.js` +7/−2 (`a4db84d` → `b34b7d7`; R7 RETITLED — ruling e) · `__tests__/rd657-health-version-one-source.test.js` +66 (added, `c66efcd`) · `__tests__/helpers/rd657-package-version-preload.js` +17 (added, `15eb6f1`) · counts. 4210/254 → **4213/255**.
- **D over `67e8928`:** `__tests__/rd607-redis-limiters-keep-their-own-counts.test.js` +50 (`9c3a879` → `431ec80`; adds R5, R5-CTRL) · `__tests__/helpers/rd649-limiter-name-clash-preload.js` +54 (added, `af97704`) · `__tests__/helpers/rd607-fake-redis.js` +7/−3 (`9ea53cd` → `e90fa2c`, the header) · counts. 4221/254 → **4223/254**.
- **E over `67e8928`:** `__tests__/rd608-ai-test-limiter-census.test.js` +97 (added, `5e43fa7`) · `__tests__/helpers/rd608-limiter-census-preload.js` +97 (added, `c44df7e`) · counts. → **4223/255**.
- **F over `67e8928`:** `__tests__/rd408-r2-misconfigured-explains.test.js` +49/−5 (`7b0606d` → `c82761e`; adds the CONTROL cell) · counts. → **4222/254**.
- **G over `ca7de45`:** `__tests__/rd665-standard-availability-test.test.js` +67/−4 (`7b8dee9` → `e6649cc`; adds two CONTROL (RD-671) cells) · counts. 4230/255 → **4232/255**.
- **Counts (MEASURED at each sha):** `1904765` 4133/247 · `faea66b` 4195/253 · `5531d7b` 4210/254 · `67e8928` 4221/254 · **M0 `ca7de45` 4230/255** · `67b840b` 4208/254 · `874c4f5` 4146/248 · `7d853b0` 4152/249 · `608a1cd` 4144/248 · `5584ea4` 4213/255 · `20fea84` 4223/254 · `9fd5c9a` 4223/255 · `8bc88f5` 4222/254 · `3ef057f` 4232/255 · `daf2210` 4210/254.
- **`__tests__` files (NUL-safe `ls-tree -r -z`):** 289 (`1904765`) · 296 (`faea66b`) · 298 (`5531d7b`) · 297 (`67e8928`) · **298 (M0)** · 297 (A) · 290 (`874c4f5`) · 291 (B) · 291 (`608a1cd`) · 300 (C) · 298 (D) · 299 (E) · 297 (F) · 298 (G).
- **Requirer populations (`git grep -l -E "require\([^)]*<helper>['\"]" <sha> -- __tests__`):** `helpers/test-server`: 54 at `faea66b`, `5531d7b`, M0, B, C, D, E, F, G; **55 at A** (rd591) and at `608a1cd` (rd646). `rd395-server-harness`: 22 at `1904765`, 23 at `874c4f5`, 23 at M0, **24 at B, C, E** (rd735 / rd657 / rd608 each add one), 23 at D, F, G, 22 at `608a1cd`.
- **Blobs elsewhere:** `helpers/test-server.js` `cff1e54` at every sha but A (`bb45cd7`) · `helpers/rd395-server-harness.js` `2453a3f` everywhere · `helpers/rd554-restore-harness.js` `028fa30` at M0 and A · `image-content-exposure.test.js` `94e6e4c` at `1904765`, `874c4f5`, B, `608a1cd`; `9ede5fd` at `faea66b`, A, `daf2210`; **`7e3262b` at `5531d7b`, `67e8928`, M0, C, D, E, F, G** · `backend/server.js` **`0d7e387` at M0, A, D, E, F, G**; `c9f0d65` at C; `86dc63f` at B; `e076121` at `874c4f5`; `4ddf75f` at `608a1cd`; `bc099b2` at `1904765` · `backend/services/cspReport.js` `f102d26` at `1904765` and M0, `4b38e90` at `874c4f5`, `6608eae` at B · rd618 `8bbfcc7` (`874c4f5`) → `1007b66` (B), absent at M0 · rd735 `4925b58` (B) · rd646 `ee838ec` (`608a1cd` only) · **`package-lock.json` `9064763` at every sha named here EXCEPT C (`64d8eda`) and `daf2210` (`f74a4e8`)** · `package.json` `cdb1168` everywhere but C (`384805d`) · rd549 `4a35642` at M0 (the UNGUARDED `Date.now()` stamp; unchanged `faea66b..ca7de45`), `1988b46` at A.
- **The RD-649 preload's ANCHOR `const _rlOpts = (name, extra) => {`** is present exactly ONCE in `backend/server.js` at M0 (:1197), `1904765` (:1197), `874c4f5` (:1233), B (:1246), C (:1197), D (:1197) and `608a1cd` (:1283) — MEASURED; the merged trees' COMBINED blobs are yours to measure (row l3).

**Main may move (ruling b).** Call main at your start **M0**. (1) M0 must be `ca7de45` or a DESCENDANT (the launcher refuses otherwise); (2) main's movement since `ca7de45` must not touch a member TEST path (the launcher refuses otherwise); `backend/server.js`, `cspReport.js`, rd618, `package-lock.json` moving is a NOTE; **RD-618, RD-646/647 or RD-732 landing is a NOTE, and then the MT build skips that merge (say so) and every prediction below re-bases**; (3) your merged trees are defined in § MERGE ORDER; (4) if main moves AGAIN during your gate, your verdict names M0 and says what moved (C-68), and you measure each member onto the END main by merge-tree.

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
  AFTER the hold.** The READY's "READY verify at 67b840b's tree" is UNVERIFIED as to the committed blobs (gate 11's WRONG 3 — carried as W11-3; gate 11's own P1 verify of `67b840b` then measured 4208/4208, PRIOR under H-29). **The red arm injected its preload with `NODE_OPTIONS="-r …slow-connect-preload.js"`** (`r7-hold.sh`) — see H-15.
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

### TARGET C — RD-657 (TIER 2, through-code) @ `5584ea4`, on `5531d7b`
- **What changed (READ, the whole diff over `5531d7b`):** `buildFullHealthDetails` (server.js :18247) reads `version: require('../package.json').version` instead of the literal `'2.0.1'`; `package.json` `1.3.0` → `2.2.1`; `package-lock.json`'s two ROOT `version` fields → `2.2.1` (no dependency line); rd327's R7 re-anchored and RETITLED (ruling e); new `rd657-health-version-one-source.test.js` (P1, V1, CTRL) and `helpers/rd657-package-version-preload.js` (puts a COPY of `package.json` with version `9.8.7-rd657` into Node's require cache in the spawned server, loaded with `node -r`).
- **The only other product reader of a package version** (READ, `git grep` at `5584ea4` over `backend static scripts Dockerfile`): `expressVersion: require('express/package.json').version` (:18250) — unaffected. `1.3.0` appears nowhere else but rd657's own comment. `2.0.1` in `__tests__` at M0: rd327 (the old R7) and `rd385-shipped-root-markdown-identifiers.test.js:617` (a planted `version 2.0.1.4` string in a NEGATIVE control of a markdown scanner — not a version reader; use it as your census's negative control).
- **Builder's claims (RELAYED, READY):** RED at `5531d7b`'s `server.js`, `package.json` and `package-lock.json` with the new cells and re-anchored R7 in place: exactly P1, V1, CTRL, R7 fail (4 of 41, rd657 + rd327). GREEN 41/41. **M1** (server hard-codes `'2.2.1'`) → ONLY V1 red; **M2** (the old `'2.0.1'` back, package.json at 2.2.1) → V1, CTRL, R7 red. C-68 by name, the package-lock readers (dockerfile-install-and-labels, rd418-dockerignore-round3, rd442-licence-terms-of-service): 24/24. Full verify 4213/4213 across 255. **Disclosed slip:** the first hold's output was truncated at 40 lines by the builder's `run()`; `rd657-hold2.log` re-ran red, M1, M2. `merge-tree 5584ea4 × daf2210` clean. **The drafter checked (MEASURED):** `session-tools/s86m/rd657-verify-full.log` carries `VERDICT: PASS — 4213/4213 tests passed across 255 suites (jest exit 0)`; the drafter's three-argument `merge-tree` of `5584ea4 × daf2210` (base `f9cb440`) has `package-lock.json` changed in both with **0 conflict markers** (a COMBINED lock blob neither side carries).
- **NOT TESTED — VERBATIM (READY):** *"- A Docker image build: package.json is COPYed by the Dockerfile's deps stage and the app's require is relative, so that should hold, but I did not build an image for this."* · *"- The demo."* · *"- The release process's own bump (it is Kam's, per C-181)."*
  → **L-C1** (no image build) · **L-C2** (the demo) · **L-C3** (the release bump is Kam's) · **L-C4** (C-181's "not covered": IMAGE_VERSION) · **L-C5** (CodeQL/CI — NOT RUN, no PR).
- **The drafter's READ (MEASURE, rows v0-v7):** (i) the lock moves off `9064763`, so "one `node_modules` serves every tree" needs a proof for C (row v5). (ii) RD-732 (`daf2210`, released) also changes the lock; if it lands first, C's lock merges into a combined blob (row v6). (iii) The shipped `package.json` version now reaches the public health body — the four public-body variants (V, U, E, M in rd327) quote it.

### TARGET D — RD-649 (TIER 2, through-code, test-only) @ `20fea84`, on `67e8928`
- **What changed (READ):** rd607 gains **R5** (claiming `'csp-report'` a second time makes the server exit 1 before answering, naming the clash) and **R5-CTRL** (the same hook with an unused name boots); `helpers/rd649-limiter-name-clash-preload.js` hooks `Module._extensions['.js']` for `backend/server.js` ONLY, finds `ANCHOR = 'const _rlOpts = (name, extra) => {'` and the next `'\n};\n'`, and appends ` _rlOpts(<name>, {});` on that closing line (line numbers unchanged); it writes what it did to stdout and `RD649_MARKER_FILE`, and on a missing OR DUPLICATED anchor says `ANCHOR NOT FOUND, nothing injected` and compiles the file unchanged; inert unless `RD649_CLAIM_NAME` is set. `rd607-fake-redis.js`'s header now cites gate 6 report §4.2 (redis 7.4.11 at `8fa0791`) and names the NOSCRIPT-recovery gap.
- **Builder's claims (RELAYED, READY):** branch rd607 9/9; **M-iv** (the csp limiter built lazily again, gate 6's mutant) → EXACTLY R5 red (`{booted:true, exitedBeforeAnswering:false, namesTheClash:false}`, hook marker present); full verify 4223/4223 across 254. **The drafter checked (MEASURED):** `session-tools/s86n/rd649/verify-hold.out` carries `VERDICT: PASS — 4223/4223 tests passed across 254 suites (jest exit 0)` — **on `HEAD 62385d9 dirty:`**, i.e. the PARENT of the READY head `20fea84` (the counts commit); the verified content is presumably the committed content (WRONG 6).
- **NOT TESTED — VERBATIM (READY):** *"NOT TESTED: R5 in Redis mode. It is not needed, because the name check runs before a store is chosen. The re-run of gate 6's other mutants against this branch."*
  → **L-D1** (R5 in Redis mode) · **L-D2** (gate 6's other mutants not re-run) · **L-D3** (CodeQL/CI — NOT RUN).
- **The drafter's READ (MEASURE, rows l0-l5):** (i) the READY says a missed anchor is "a red cell, not a boot that passed because nothing was injected" — PROVE it (row l1): R5 must go red when the anchor is absent or doubled, and R5-CTRL must too, or R5-CTRL's green would be the no-hook boot. (ii) B and RD-618 and `608a1cd` rewrite `server.js` ABOVE the anchor (it moves :1197 → :1233/:1246/:1283) — the anchor must land ONCE in every COMBINED blob (row l3). (iii) rd607 is ALSO in B's C-68 set (rd495, rd607, rd618, rd735) — on the merged tree rd607 is D's blob `431ec80`.

### TARGET E — RD-608 (TIER 2, through-code, test-only) @ `9fd5c9a`, on `67e8928`
- **What changed (READ):** `rd608-ai-test-limiter-census.test.js` (CTRL, C1) and `helpers/rd608-limiter-census-preload.js`, which wraps express-rate-limit's factory in the SPAWNED server and writes a ledger of the limiters that RAN on each POST /api/setup/ai-test, labelled by each limiter's own refusal message (a message-less limiter by the file that built it).
- **Builder's claims (RELAYED, READY):** CTRL = census loaded, 8 limiters under known labels, 1 request; C1 = exactly [general, setup, ai-test] ran, each passed it on, ai-test `hasSkip` false. **8, not 7:** `services/scimProvisioning.js` builds SCIM's own (gate 6's F-4 limiter), which rd607's S1 never sees (S1 counts only server.js); round 1 was VOID on this. Arms (hold `s86n-rd608-r2`): B1-B4 → C1 red / R8 GREEN; B5, B6 → census 2/2 / R8 RED; M-drop → C1 red / R8 red; M-skip → C1 red / R8 GREEN (RD-545's shape). Full verify 4223/4223 across 255. **The drafter checked (MEASURED):** `s86n/rd608/verify-hold.out` carries `VERDICT: PASS — 4223/4223 tests passed across 255 suites` **on `HEAD b896c7b dirty:`** — the parent of `9fd5c9a` (WRONG 6).
- **NOT TESTED / NAMED LIMIT — VERBATIM (READY):** *"NOT TESTED: the census in Redis mode (labels do not depend on the store); a limiter created through a factory other than express-rate-limit."* · *"NAMED LIMIT: the labels are the limiters' message texts, so rewording a message turns CTRL red. That is intended, but it is a coupling."*
  → **L-E1** (Redis mode) · **L-E2** (another limiter factory) · **L-E3** (message-text coupling) · **L-E4** (CodeQL/CI — NOT RUN).
- **The drafter's READ (MEASURE, rows k0-k4):** (i) the census counts limiters BUILT; B adds a per-address entry budget that is NOT an express-rate-limit instance, and `608a1cd` changes the limiter store — CTRL's "8" must be re-measured on MTb, MT1 and MT2 (C-68). (ii) M-skip and B1-B4 leave R8 GREEN — C1 is then the ONLY cell that sees them: the census is load-bearing, so its own blindness (a limiter the factory wrapper does not see) is row k3.

### TARGET F — RD-653 (TIER 2, through-code, test-only) @ `8bc88f5`, on `67e8928`
- **What changed (READ):** rd408-r2's short-SESSION_SECRET length cell counts a `23` only where it is REPORTED as a length — `reportsLength(text, n)` matches n beside got/length/len/size or characters/chars/bytes, or on a line naming SESSION_SECRET exactly (not `/secret/i`, because the boot's own volume path contains "secret"); the short boot's volume is `b-secret-short-23-vol` so every run carries an incidental bare 23 (gate 7's requested regression, made permanent), and `noiseLive` asserts it is really there; a new CONTROL cell: 5 leak forms seen (5b07f55's `SESSION_SECRET too short (got 23, need 32+ random chars).` verbatim among them), 4 noise forms not (the DATA_DIR path, `23 printers in 23 ms`, today's FATAL line, `port 3023`).
- **Builder's claims (RELAYED, READY):** green 11/11; OLD (the pre-RD-653 bare-23 rule with the -23- volume) → the length cell red `{length:true}` (O-5 reproduced deterministically); LEAK (preflight's fatal prints `(got N)`) → the length cell red, and the case cell's FATAL-line check red too (expected). Full verify 4222/4222 across 254 **on `HEAD cdc6438 dirty:`** per `s86n/rd653/verify-hold.out` (MEASURED; the parent of `8bc88f5`; WRONG 6).
- **NAMED LIMIT — VERBATIM (READY):** *"NAMED LIMIT: a leak phrased without any of those words, and not on a SESSION_SECRET line (for example a bare "(23)" on some other line), would pass. The old rule caught that, at the cost of O-5. The trade is the ticket's own fix-shape."*
  → **L-F1** (a leak phrased without the words passes) · **L-F2** (CodeQL/CI — NOT RUN).
- **The drafter's READ (MEASURE, rows n0-n4):** (i) this ticket NARROWS a negative cell ("neither the value nor its length is in … the process output") — it is a C-102 case by construction (§3b). (ii) rd408-r2 takes ports from `reservePort()` (it `require`s `helpers/test-server`), so on MT1 its boots run in A's bands: the noise set gains whatever port numbers A's bands produce (39000-49151) — a band port is never a bare `23`, but MEASURE that no line of a MT1 run is counted by `reportsLength` (row n4).

### TARGET G — RD-671 (TIER 2, through-code, test-only) @ `3ef057f`, on `ca7de45`
- **What changed (READ):** rd665's `allResources()` walks children and nested deployments' templates and compares types case-insensitively (a child's last-segment type counts); `webtestsOf()` and the availability-alert lookup use it; `HEALTH_URL`: `RequestUrl` must be exactly `[uri(concat('https://', reference(resourceId('Microsoft.App/containerApps', variables('appName')), '<api-version>').configuration.ingress.fqdn), '/api/health')]` (only the API version may vary), and the problem line quotes the URL it got; two CONTROL (RD-671) cells.
- **Builder's claims (RELAYED, READY):** green 6/6; **M-top** (the top-level-only filter back) → EXACTLY the nesting control red (child 0, deployment 0); **M-substr** (the substring test back) → EXACTLY the URL control red (all four variants accepted). Full verify 4232/4232 across 255 **on `HEAD 4088b20 dirty:`** per `s86n/rd671/verify-hold.out` (MEASURED; the parent of `3ef057f`; WRONG 6). **DISCLOSED FLOOR BREACH:** at ~2026-09-29T22:18Z the builder ran `npx jest __tests__/rd665-standard-availability-test.test.js` once OUTSIDE `session-tools/nexusai-lock.sh` (a pure JSON-template file, ~1 s, no server, no port); recorded in HANDOVER-S86N.md (RELAYED; not your finding to re-rule, but name it).
- **NAMED LIMIT / NOT TESTED — VERBATIM (READY):** *"NAMED LIMIT: HEALTH_URL is exact on purpose, so any legitimate rewrite of the expression (a different ingress property, a variable in place of variables('appName')) turns 'the shipped template passes the rule' red. The problem text says why."* · *"NOT TESTED: an ARM deployment of a template with a nested webtest. The rule is structural; I did not measure what ARM itself does with the nesting shapes."*
  → **L-G1** (exact HEALTH_URL) · **L-G2** (no ARM deployment) · **L-G3** (CodeQL/CI — NOT RUN).
- **The drafter's READ (MEASURE, rows w0-w3):** (i) "only the API version may vary" — READ: `HEALTH_URL` (rd665 :42 at `3ef057f`) is an anchored regex whose version slot is `'\d{4}-\d{2}-\d{2}(?:-preview)?'`, so the drafter PREDICTS every non-date and injected-fragment variant is rejected — PROBE it (w2) rather than trust the read. (ii) The TYPE compare is case-insensitive, but `HEALTH_URL` carries no `/i` flag (READ) — `HTTPS://` and whitespace variants are predicted REJECTED; say whether that is intended (the named limit L-G1 says exact on purpose).

### File overlap and merge predictions — the drafter used the READ-ONLY three-argument `git merge-tree <base> <a> <b>` (writes NO objects), NOT `--write-tree`
**MEASURED ~09:25 AEST, on M0 = `ca7de45`** (legacy output parsed for `+<<<<<<<` per "changed in both" path): **every pair among M0 and the seven heads, and each with `608a1cd` (36 pairs) → conflict markers in `scripts/verify-expected-counts.json` ONLY**, except M0 × G (no path changed in both: G fast-forwards M0). **`backend/server.js` is "changed in both" and merges TEXTUALLY CLEAN** for M0 × B, M0 × `608a1cd`, and for B × {A, C, D, E, F, G, `608a1cd`} and `608a1cd` × {A, C, D, E, F, G} (the `1904765`-cut side against main's RD-681 `server.js`) — **so every merged tree carrying B holds a COMBINED `server.js` blob no parent carries: RD-681's (main) + RD-618's + RD-735's + RD-657's health line (+ RD-646/647's on MT2).**
**Shared paths other than the counts file (by each member's own delta): B × C `backend/server.js`; B × `608a1cd` and C × `608a1cd` `backend/server.js`. Nothing else.** C × `daf2210` (not a member): `package-lock.json`, clean, combined.
**Re-measure by `git merge-tree --write-tree --name-only` in YOUR OWN scratch object dir (§8.1) on YOUR M0** (the three-argument form has no rename detection); **name every combined blob.**

### MERGE ORDER — the drafter's proposal, with its predicted end state and the C-68 re-run set per merge
**Proposed order: 1. RD-671 `3ef057f` → 2. RD-653 `8bc88f5` → 3. RD-608 `9fd5c9a` → 4. RD-649 `20fea84` → 5. RD-657 `5584ea4` → 6. RD-618 `874c4f5` (NOT a member) → 7. RD-735 `7d853b0` → 8. RD-591 `67b840b`.**
Why: the four test-only members first (G fast-forwards; D, E, F touch only their own cells); C next (a three-line product change and the lockfile, before the CSP intake rewrites the same `server.js`); B cannot land before RD-618 (stacked); RD-591 last because it changes the harness EVERY server-booting cell uses, so its C-68 set then covers every earlier member's cells. **Merges are STOPPED (ruling j)** — if P's measurement shows rd549 O4 is cause (i), Tuesday may bring RD-591 forward; **your o-rows say whether it would help.**
**Challenge it:** order independence is the control (§8.3), not an assumption.

| step | merge | predicted conflicts | predicted counts after (M0 = `ca7de45`, 4230/255) | C-68 re-run set BY NAME (on the tree after that step) |
|---|---|---|---|---|
| t1 | M0 + `3ef057f` | none (fast-forward) | **4232/255** | rd665 (6) |
| t2 | + `8bc88f5` | counts only | **4233/255** | rd408-r2 (11) |
| t3 | + `9fd5c9a` | counts only | **4235/256** | rd608 (2) + rd516 (its R8 is kept) + rd607 |
| t4 | + `20fea84` (= **MTt**) | counts only | **4237/256** | rd607 (9 with R5, R5-CTRL) + every `rd607-fake-redis` requirer (re-derive) + rd608 |
| p | + `5584ea4` (= **MTp**) | counts only | **4240/257** | rd657 (3) + rd327 + the package-lock readers (dockerfile-install-and-labels, rd418-dockerignore-round3, rd442-licence-terms-of-service) + every cell that reads `/api/health`'s body (`git grep -l`; positive control rd327, negative control rd385) |
| a | + `874c4f5` (= **MTa**) | counts only; `server.js` COMBINED | **4253/258** | rd618 (13) + rd495 + rd607 + every `csp-report`/`cspReport` reader (positive control rd618, negative control a comment-only mention) + rd657/rd327 on the combined blob |
| b | + `7d853b0` (= **MTb**) | counts only | **4259/259** | rd735 (6) + the step-a set + rd608 CTRL on the combined blob |
| c | + `67b840b` (= **MT1**) | counts only | **4272/260** | **the 55 test-server importers BY NAME** (per-file counts; positive control rd591, negative control a comment-only mention) **+ every rd395-harness requirer** (27 predicted: B's R8/R9, rd618, rd657, rd607, rd608 among them) + rd408-r2 and rd327 (both `reservePort()` users) + rd549 (rows o3) |
| x | + `608a1cd` (= **MT2**, the cross tree) | counts only; `server.js` COMBINED again | **4283/261** | **rd646 (11) + rd618 + rd735 + rd495 + rd607 (R5's anchor in the new blob) + rd608 CTRL by name (L-B1, batch 9's instruction)** + rd646 under A's harness |

**Arithmetic (not measured):** 4230 + 2 + 1 + 2 + 2 + 3 + 13 + 6 + 13 (+ 11) / 255 + 0 + 0 + 1 + 0 + 1 + 1 + 1 + 1 (+ 1). **`__tests__` files predicted: MTt 301 · MTp 303 · MTa 304 · MTb 305 · MT1 306 · MT2 308. test-server requirers MT1 55, MT2 56. rd395 requirers MT1 27.**
**Cross-check with gate 11 (PRIOR, H-29):** its MT1 at `5531d7b` measured 4242/257 = 4210 + 32/+3; the same three merges on `ca7de45` predict 4262/258 — the order above only adds the five new members on top.
**Re-derive every set in YOUR clone at M0** with a positive control (the ticket's own cell file must be found) and a negative control (a file that only MENTIONS the name must NOT be counted as a reader).

### How to build your trees
- **No worktree is created in the NexusAI repo, and you never work in its `2_Project_Files` checkout or any builder `worktrees/` directory.** In that repo use ONLY read verbs: `show`, `diff`, `log`, `ls-tree`,
  `cat-file`, `grep`, `ls-remote`, `rev-parse`, `merge-base`, `rev-list` (plus `count-objects` for §8.9). **NEVER `fetch`, `pull`, `push`, `checkout`, `worktree`, `commit`, `stash`, `gc`, `merge`; and `merge-tree
  --write-tree` ONLY with `GIT_OBJECT_DIRECTORY=<your own scratch dir> GIT_ALTERNATE_OBJECT_DIRECTORIES=<repo>/.git/objects`.**
- **Every tree is K1** — `git clone --shared --no-checkout <repo> <dir>` then `checkout` in YOUR clone (origin removed; local identity; `gc.auto 0`; `core.fsmonitor false`; hooks off), under a fresh
  `mktemp -d` in `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/qa-trees/batch12.XXXXXX/`. Status-check before use. **Each K1 tree holds its own `.git`, so A's `worktreeRoot()` resolves to
  YOUR tree and `worktreeSlot()` hashes YOUR path — record each tree's slot (row g8).**
- **Each tree is EXCLUSIVE to this gate and to ONE purpose.** A fresh arm per mutant; never reuse a mutant tree for a clean arm; `batch12`-prefixed directories only. **Gate 11's trees (`qa-trees/batch11.*`) are NOT yours — never run in them, never write to them** (READ their evidence only, H-29).
- **The red-at-parent trees:** A and B exactly as gate 11 specified (A: YOUR clone at `67b840b` with `helpers/test-server.js` and the five stand-ins restored to their `faea66b` blobs; B: YOUR clone at `7d853b0` with `server.js` and `cspReport.js` restored to `874c4f5`'s `e076121` / `4b38e90`). **C:** YOUR clone at `5584ea4` with `backend/server.js`, `package.json` and `package-lock.json` restored to `5531d7b`'s `0d7e387` / `cdb1168` / `9064763` (the new cells and the re-anchored R7 stay). **D:** YOUR clone at `20fea84` with `backend/server.js` carrying M-iv (row l0) — D changes no product file, so its "red at parent" IS the mutant. **E, F, G:** likewise their READY's own arms (rows k0, n0, w0). Each hashed after the restore, committed IN YOUR CLONE ONLY so each tree is a clean K1.
- `node_modules`: an APFS clone (`cp -c -R`) of the newest gate tree you trust, **after proving** `package-lock.json` is blob `9064763` there — and **for C's trees and every merged tree carrying C, after proving the lock differs from `9064763` ONLY in the two root `"version"` lines** (row v5); a real directory, never a symlink. **Never `npm install` / `npm ci`** (no registry, §11).

## 2. Why these tiers, and who is waiting
- **RD-591 TIER 1 — severity rules:** **a guarded stand-in that COUNTS a dial from outside the test's process tree in any cell that asserts a POSITIVE arrival or count (rd549 `envReached`, rd486/rd516/rd523/rd545
  counts) is a Major** (Tuesday's stated reason for tier 1); **a security cell (rd516 SSRF, rd523 redirect, rd545, rd549) that stays GREEN with the product's refusal REMOVED, because the guard dropped the dial, is a
  Blocker** (the cell's green would be the wrong reason in exactly the direction that hides a vulnerability); **a cell that passed at M0 and fails or is lost at the head or on MT1 is a Major; a cell slowed past its
  own budget is a Major; a mutant the READY says reddens a cell that you find leaves it green is a Major (C-40 class); a READY/comment claim that is false is a Minor.**
- **RD-735 TIER 2 — severity rules:** **one address storing more than 60 entries in any 60 s window through the intake as deployed locally is a Major (A-F1r not closed); a forged report whose userinfo reaches the log or
  the ring in a shape the READY claims covered is a Major; a shape the READY does not claim, which keeps userinfo, is a Minor (name it); a cell green while its named behaviour is broken is a Major (C-40); a budget
  defeated only through a client-forged `X-Forwarded-For` with no ingress is the deployment's `trust proxy` question — name it and its evidence class, severity yours, not a re-rule of (c).**
- **RD-657, RD-649, RD-608, RD-653, RD-671 TIER 2 — severity rules:** **health's `version` differing from `package.json`'s on any public or full body is a Major (C-181 not met); a lock change beyond the two root version fields is a Major (the READY says "No dependency line is touched");
  a preload whose anchor misses while R5 or R5-CTRL stays GREEN is a Major (a cell that cannot fail); a census that misses a limiter which RAN, or a length scan that misses a leak form the READY claims covered, is a Major; a leak form the READY names as NOT covered (L-F1) is the ticket's accepted trade — reproduce it, name it, no severity beyond Minor;
  a template shape the rule is named to reject that passes is a Major; a mutant the READY says reddens exactly one cell that reddens none (or others) is a Major (C-40); a READY/comment claim that is false is a Minor.**
- **Who is waiting:** RD-591, RD-649, RD-608, RD-653 and RD-671's merge author is **NexusAI-N (S86N)**; RD-735's and RD-657's is **NexusAI-M (S86M)**, whose RD-618 lands before RD-735 — under C-184/C-186's turns and C-190's PR route. **NexusAI-P** owns the rd549 O4 measurement (ruling j).

## 2a. LEGITIMATE SHAPES — required measurements, row by row
**Columns: the head, the base it is measured against (P_A = `faea66b`'s helper and stand-ins for A; P_B = `874c4f5`'s two product files for B; P_C = `5531d7b`'s three product files for C), and the MERGED tree. Every cell-run row: your own K1 tree,
under the network belt (subject to H-23), a fresh TMPDIR, `--forceExit`, a deadline, killed in a `finally` by pid. EVERY ROW ALSO RECORDS THE MODEL IT RAN ON (THE MODEL RULE, H-27).**
**Rows g0-g9, s1-s2, e0-e6, f1-f4, r1-r4 and x1-x3 below are gate 11's, carried VERBATIM (their "at M0" now means YOUR M0, `ca7de45` or later).**

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
| x3 | **the combined `server.js`:** on MT1 and MT2, the CSP intake block and the rate-limit block quoted from the merged blob; its blob id named; `node --check` rc | the intake block = B's; RD-681's, RD-657's (health `version:`) and RD-646/647's hunks present | drafter |

**Y — the cross-change cells the new members add (C-68).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| y1 | **C, D, E, F under A's harness:** on MT1, rd657, rd327, rd607 (with R5/R5-CTRL), rd608 and rd408-r2 by name, 3 runs, per-file counts, each run's `[RD-591]` stderr lines counted (H-23) | all green ×3; 0 refused, 0 unattributable; name the slot of MT1's tree | drafter |
| y2 | **the COMBINED `server.js` on MTp, MTb, MT1, MT2:** its blob id; the health `version:` line (C's), the CSP intake block (B's), RD-681's hunk (main's), RD-646/647's (MT2); `node --check` rc | every hunk present exactly once; `version: require('../package.json').version,` present once and `version: '2.0.1',` absent | drafter |
| y3 | **rd608's CTRL and C1 on MTb, MT1 and MT2** (B adds an entry budget that is not an express-rate-limit instance; `608a1cd` changes the limiter store) | quote the census: the limiter COUNT and every label per tree; C1's ran-set on each | drafter (E READ (i)) |
| y4 | **rd607 R5/R5-CTRL on MTa, MTb, MT1 and MT2:** the preload's marker line quoted per tree (`injected _rlOpts("csp-report") …`), the anchor's line number in each combined blob | R5 red→refuses-at-boot green, R5-CTRL green, marker = injected, ONCE, every tree | drafter (D READ (ii)) |

**O — rd549 O4 on M0 (ruling j; REQUIRED; name its state on M0 before any claim about RD-591).**

| row | shape | expected | predicted-by |
|---|---|---|---|
| o0 | **READ ONLY first:** main's Build 36635558304 — attempt 1's failing set and O4's diff (quote the job log lines), attempt 2's conclusion when you read it (`gh api …/runs/36635558304/attempts/<n>`, READ ONLY), and any later push Build on M0; rd549's blob on M0 (`4a35642`, unguarded `Date.now()` stamp) and how `bootServer` in the rd395 harness decides readiness (quote the lines that set `h.readyAt`'s instant) | attempt 1 = rd549 O4 only; attempt 2 named as a RE-RUN, never a clearance (C-185) | commission |
| o1 | **O4's state on M0, locally:** rd549 by name on YOUR M0 tree ×5 solo, and inside ONE full verify of M0 (the load CI had); per run: O4 pass/fail, and for O4's boot the stand-in's counted `requests[].at` vs `h.readyAt` (a COPY of the cell that also records them — never the pinned file) | name O4's state on M0 ("red k of n under load / green n of n solo" or whatever you measure); **no clearance by re-run** | commission |
| o2 | **cause (i) vs (ii), measured:** in a COPY of rd549 on M0, add (1) a SERVER-side stamp — a preload in the SPAWNED server (the harness's own `preload` option, H-15) that records when the env dial's socket CONNECTS and when its request is WRITTEN; (2) a stand-in-side ACCEPT stamp (a `'connection'` listener PREPENDED on the stand-in); (3) the handler stamp (as the cell has); (4) `h.readyAt`. Under load (the full-verify window, or `--maxWorkers=2` with a CPU-burner child you start and kill by pid) until O4's shape reproduces or ≥ 30 boots | **classify every late boot:** (i) = connect/write ≤ `readyAt` but handler > `readyAt` (jest-side lag); (ii) = the server's connect/write > `readyAt` (the dial lands after readiness); **also (i′)** = accept itself > `readyAt` although the server connected before it (the jest worker's event loop was busy — an accept-time stamp does NOT fix this) — quote the distribution | commission + drafter |
| o3 | **RD-591's stamp on the same load:** the o2 COPY at A's `arrivalTime` form on MT1 (and the head `67b840b`) | **say whether `arrivalTime` would have kept O4 green for the late boots o2 classified as (i), and that it cannot for (ii)/(i′)**; RD-591 is O4's fix ONLY if (i) dominates and o3 shows it — otherwise say "not measured as O4's fix" | commission |
| o4 | **P's report, if it arrives during the gate:** quote it as RELAYED beside o1-o3 | agreement or disagreement named, with evidence classes | commission |

**V — RD-657 (health's version, one source).**

| row | shape | expected at `5584ea4` | at P_C (`5531d7b`'s three product files) | predicted-by |
|---|---|---|---|---|
| v0 | **RED-AT-PARENT (POSITIVE CONTROL FIRST):** rd657 + the head's rd327 against P_C | — | **exactly P1, V1, CTRL, R7 red, 4 of 41** (quote each failing assertion) | builder |
| v1 | the head clean: rd657 + rd327 | **41/41** (name every title) | — | builder |
| v2 | **the builder's mutants re-derived INDEPENDENTLY:** M1 (server hard-codes `'2.2.1'`) → {V1}; M2 (`'2.0.1'` back, package.json 2.2.1) → {V1, CTRL, R7}; **your own: M-lock (package-lock's root version left at 1.3.0) → P1 only?; M-path (health reads `require('../../package.json')` or a copy under `backend/`) → which?; M-cache (health reads the version ONCE at module load into a const) → does V1 still see the preload's copy?** | each MEASURED; a mutant leaving all 41 green is a branch no cell sees (C-40) | — | builder + drafter |
| v3 | **a real local boot** (open mode, fresh DATA_DIR, YOUR tree): GET `/api/health` and each public-body variant rd327 names (V, U, E, M) — quote `version` and `build` | `"version":"2.2.1"` everywhere; `build` as rd327 defines | `"2.0.1"` | builder + drafter |
| v4 | **the preload landed (H-3):** V1's boot prints the preload's own landing; the COPY in the require cache is what `/api/health` read (`9.8.7-rd657`); CTRL's boot has no preload | quote both | — | drafter |
| v5 | **the lockfile and `node_modules`:** `git diff 5531d7b 5584ea4 -- package-lock.json` = exactly the two root `"version"` lines (quote); `npm ls --depth=0` (OFFLINE; no registry) in C's tree over the cloned `node_modules` — rc and any `invalid`/`extraneous` line; say whether one `node_modules` serves C | two lines; no dependency line; `npm ls` clean or every line named | — | drafter |
| v6 | **RD-732's lock (not a member):** `merge-tree --write-tree` (scratch objects) of `5584ea4` × `daf2210` and of MTp × `daf2210` — the combined lock blob named, the two root versions AND ip-address 10.7.2 both present | clean, combined, both hunks | — | drafter (READ (ii)) |
| v7 | **C-68 census:** every cell reading `/api/health`'s body or pinning a version string, BY NAME on MTp and MT1 (`git grep -l` at the tree; positive control rd327; negative control rd385's `version 2.0.1.4` plant) | all green; the list named | — | drafter |

**L — RD-649 (the csp-report limiter built at load).**

| row | shape | expected at `20fea84` | at M0 | predicted-by |
|---|---|---|---|---|
| l0 | **RED-AT-PARENT = M-iv re-derived INDEPENDENTLY (POSITIVE CONTROL FIRST):** the csp-report limiter built lazily again (locate by coverage, one anchor) | **EXACTLY R5 red** — quote `{booted, exitedBeforeAnswering, namesTheClash}` and the marker; the other 8 green | — | builder |
| l1 | **the anchor-miss path (the READY's "a red cell, not a boot that passed"):** a COPY of `server.js` in a fresh tree with the anchor text altered (one character), and another with the anchor DUPLICATED; run R5 and R5-CTRL on each | **R5 RED and R5-CTRL RED on both** (marker `ANCHOR NOT FOUND, nothing injected`) — **R5-CTRL green here is a Major: it would pass on a boot the hook never touched** | — | drafter (D READ (i)) |
| l2 | **the hook stays in its lane (H-3):** with `RD649_CLAIM_NAME` unset the preload changes nothing (a boot with and without it, identical limiter census); with it set, only `backend/server.js` is rewritten (a second module compiled unchanged — prove by its hash of compiled source or a sentinel) | inert / one file only | — | drafter |
| l3 | **the anchor on every COMBINED blob:** MTa, MTb, MT1, MT2 — marker quoted, line number quoted, `node --check` of the combined blob | injected ONCE per tree | — | drafter (D READ (ii)) — same as y4 |
| l4 | **PRIOR WORK (C-49), READ ONLY:** RD-607's at-load build (`80d083b`) KEPT; S1, R1-R4 unchanged (title diff); the fake's new header's citation — the gate 6 report §4.2 exists and says redis 7.4.11 at `8fa0791` (locate the report by a single-directory `ls` of the reports dir) | kept; citation true | — | builder |
| l5 | **gate 6's other mutants (L-D2):** name them from gate 6's report (READ ONLY) and say whether any is re-runnable here in scope; run ONE if cheap | named; NOT RUN or measured | — | drafter |

**K — RD-608 (the limiter census).**

| row | shape | expected at `9fd5c9a` | at M0 | predicted-by |
|---|---|---|---|---|
| k0 | **POSITIVE CONTROL FIRST — the census can fail:** M-drop (ai-test limiter removed from the route) and M-skip (ai-test gains a `skip`) re-derived INDEPENDENTLY | M-drop: C1 red + R8 red; **M-skip: C1 red, R8 GREEN** (quote) | — | builder |
| k1 | the head clean: rd608 + rd516 by name | 2/2 + rd516 all green; CTRL's census quoted (8 labels, SCIM's by file) | — | builder |
| k2 | **B1, B5 re-derived:** B1 (a second limiter not named `…limiter` on the route) → C1 red / R8 green; B5 (a non-limiter middleware named `…Limiter…`) → census 2/2 / R8 red | as the READY says | — | builder |
| k3 | **the census's own blindness (E READ (ii), L-E2):** a limiter built by wrapping express-rate-limit's handler in another function, or via a require path the wrapper does not patch (e.g. a second copy under a different resolution) — does C1 see it run? | **MEASURE and name** — a limiter that RUNS and is not counted is a finding (Major if the READY claims the case, else Minor) | — | drafter |
| k4 | **the message-text coupling (L-E3):** reword one limiter's message by one word | CTRL red naming the unknown label (quote) — the named limit reproduced | — | builder |

**N — RD-653 (the rd408-r2 length scan).**

| row | shape | expected at `8bc88f5` | at M0 | predicted-by |
|---|---|---|---|---|
| n0 | **POSITIVE CONTROL FIRST:** OLD (the pre-RD-653 bare-23 rule with the `-23-` volume) and LEAK (preflight's fatal prints `(got N)`) re-derived INDEPENDENTLY | OLD: the length cell red `{length:true}` deterministically (O-5); LEAK: the length cell red (and the case cell's FATAL check red, expected) | OLD's red is M0's O-5 | builder |
| n1 | the head clean: rd408-r2 by name ×3 | 11/11 ×3; `noiseLive` true each run (the incidental 23 really present) | — | builder |
| n2 | **L-F1 reproduced:** a LEAK arm that prints a bare `(23)` on a line naming neither SESSION_SECRET nor a length word; another that prints `len=23`… and `23 chars` on separate lines | **MEASURE:** the bare `(23)` passes (the accepted trade — name it); the others red | — | builder + drafter |
| n3 | **what the old rule caught that the new misses:** enumerate by PROBE (`reportsLength` over a table of ≥ 12 phrasings a real leak could take: `23 characters`, `23-char`, `length: 23`, `(23)`, `=23`, `size 23`, `got 23`, `SESSION_SECRET … 23`, a JSON `{"len":23}`, a localized `23 caractères`, `twenty-three`, `0x17`) | quote the table (seen / missed); **any missed form the CONTROL claims covered is a Major** | — | drafter |
| n4 | **under A's bands (MT1):** rd408-r2 ×3 on MT1; every line `reportsLength` counts, quoted with its source | 0 incidental matches from band ports; 11/11 ×3 | — | drafter (F READ (ii)) |

**W — RD-671 (the RD-665 template rule).**

| row | shape | expected at `3ef057f` | at M0 | predicted-by |
|---|---|---|---|---|
| w0 | **POSITIVE CONTROL FIRST:** M-top and M-substr re-derived INDEPENDENTLY | M-top: EXACTLY the nesting CONTROL red (child 0, deployment 0); M-substr: EXACTLY the URL CONTROL red | — | builder |
| w1 | the head clean: rd665 by name | 6/6; the shipped template passes | — | builder |
| w2 | **HEALTH_URL's variable slot (G READ (i)):** the API version as `''`, `'x'`, `'2024-03-01'), '/evil'` (an injected close), a trailing space; and `HTTPS://`, a doubled `//api/health`, whitespace inside `concat(` | quote accept/reject for each; **an injected fragment accepted is a Major** | — | drafter |
| w3 | **nesting depth and type case:** a webtest nested two deployments deep; `microsoft.insights/WEBTESTS` as a child last-segment `WebTests`; a `copy` loop | quote found/rejected per shape | — | drafter |

**A row whose expected verdict and clause disagree is a finding against this brief — say so.**

## 3. THE QUESTIONS ALL TARGETS ANSWER FIRST
0. **SESSION_SECRET UNSET, EVERY RUN** — §3a H-1's ONE permitted printer. Positive control once per target: its own cell file with a throwaway random 64-hex secret exported (never printed,
   never written) — identical results, or say what differed.
1. **Re-pin everything yourself:** `git ls-remote` at start, mid and end (three timestamped readings, branch name beside each sha, C-192's retry, attempts counted): main, all seven member branches, RD-618's,
   RD-646/647's, RD-732's. M0 and the "Main may move" rule re-proved; chains and exact parents; deltas; counts at every sha §1 lists.
2. **POSITIVE CONTROL FIRST — re-derive every red and every mutant INDEPENDENTLY** — your own scripts, never the builders' `r7-hold.sh`, `slow-connect-preload.js`, `rd549-guard-arm.js`, `rd735-hold.sh`, `rd735-m3b.sh`,
   `rd657-hold*.sh`, `s86n/rd649|rd608|rd653|rd671/*-hold.sh` or `s86n/rd608/mutate.py` (read them for method). **Before each mutant arm, prove it still parses — `node --check` on every mutated JS file, exit 0, quoted — and that it LANDED (the exact mutated text present, the
   original absent once the new text is removed; your mutate tool's `--verify` with its negative control). A red from a mutant that does not parse, or a green from one that never landed, is a VOID arm.**
   Quote the failing assertion of every red.
3. **Name every behaviour guarded by no cell, and every one guarded only by source text** (g2 (iv), g9's, e6's, v2's and k3's survivors at least).
4. **Full verify of each head and of MT1**, `npm run verify -- --maxWorkers=2 --forceExit`, through the lock, SESSION_SECRET UNSET, a fresh SHORT TMPDIR each, **K1 only**, **unbelted (as every earlier gate) —
   and, per g0, say whether A's guarded cells could attribute under the conditions the verify ran in.** Prove `--forceExit` reached jest or say it did not and rely on the deadline. **Predicted: `67b840b` 4208/254 ·
   `7d853b0` 4152/249 · `5584ea4` 4213/255 · `20fea84` 4223/254 · `9fd5c9a` 4223/255 · `8bc88f5` 4222/254 · `3ef057f` 4232/255 · M0 = `ca7de45` 4230/255 (o1's load run) · MT1 4272/260 (regenerated once).**
   **`67b840b` and `7d853b0` MAY be satisfied by gate 11's P1 verifies as PRIOR evidence under H-29** (heads unchanged; re-check, then cite) — say which you did. MT2's full verify only if the queue allows (else NOT RUN and named — its x2 set is required). Every failure by NAME;
   **C-185's known set is CI's, not local: a LOCAL failure of rd638 E2 or rd465 O-1 is named, never waved through; a failure of rd549 O4 anywhere is reported against ruling (j) and rows o1-o3.** Re-run until green is not an acceptance gate.

## 3a. INSTRUMENT RULES — H-1..H-30 (H-1..H-26 carried VERBATIM from gate 11's brief, except H-12 and H-20, which gain this batch's members; H-27..H-30 are this batch's)
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
  ADDS rd591 (13 ids); `874c4f5` ADDS rd618 (13 ids); B MODIFIES rd618 (titles UNCHANGED) and ADDS rd735 (6 ids); C MODIFIES rd327 (R7 RETITLED — ruling e) and ADDS rd657 (3 ids) + `helpers/rd657-package-version-preload.js`; D MODIFIES rd607 (ADDS R5, R5-CTRL; other titles UNCHANGED — prove it) and `helpers/rd607-fake-redis.js`, ADDS `helpers/rd649-limiter-name-clash-preload.js`; E ADDS rd608 (2 ids) + `helpers/rd608-limiter-census-preload.js`; F MODIFIES rd408-r2 (ADDS one CONTROL; other titles UNCHANGED); G MODIFIES rd665 (ADDS two CONTROL (RD-671); other titles UNCHANGED).** Name the stale-parent files: every `__tests__` file main changed since each member's
  base that the member carries at its OLD blob (for B/RD-618 at least `image-content-exposure` `94e6e4c`, `helpers/image-manifest.js` `07e8711`, `helpers/dom.js` `04f182f`, and everything RD-681/RD-204/RD-466 changed; for A `dom.js`, `vendor-surface.css`, `image-content-exposure` `9ede5fd`, rd418; for C, D, E, F everything RD-703 and RD-197 changed since `5531d7b`/`67e8928` — `helpers/image-manifest.js`, the rd703-parked and rd699 files, rd197).
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
  rc 142 = fired): targeted cell runs 600 s, the C-68 unions 2,400 s, a full verify 2,700 s, each g3 dialer run 180 s, each o2 load run 2,700 s, and every in-hold wait for the next part 600 s (H-28). A deadline that fires ABORTS that step
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
- **H-27 (THE MODEL RULE, Kam 2026-09-30 09:07).** A response stopped by Opus 5.5's safeguards STOPS that step (NOT RUN, never re-worded to slip past); ONE line to `evidence/classifier-stops.txt`; a STATUS mail `[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged — requesting the Opus 4.8 switch`; release the lock per H-28; end the turn `PARKED: flagged — awaiting the Opus 4.8 switch`. **You never answer the model dialog; nobody chooses "Switch automatically".** Every row in the report carries the MODEL it ran on; the switch time is quoted.
- **H-28 (gate 11's idle hold).** **A hold never idles holding the jest lock.** Every wait INSIDE a hold for the agent's next part (gate 11's `wait-P3` loop) carries a DEADLINE of 10 minutes; on expiry the hold exits through its own EXIT trap (restores, reaps, releases) and the next part is re-filed behind any merge ticket (§10). **Split the jest work into holds of at most ~90 minutes of planned jest each** (e.g. H1 = the heads' full verifies; H2 = MT1 regenerate + plain verify + the C-68 unions; H3 = mutant and row arms), re-filing between holds; say how many you used and why. **Before parking under H-27, let the running jest step finish and let the hold exit.**
- **H-29 (PRIOR evidence from gate 11).** Gate 11's evidence is READ ONLY and is PRIOR, never a verdict. A prior measurement may stand in for a run of your own ONLY when you re-check it and say so: (1) the head it measured is still the pinned head (your ls-remote); (2) its tree id equals `git rev-parse <head>^{tree}` (gate 11 recorded `tree=13ac0b8` for `67b840b` and `tree=2c50aed` for `7d853b0`; the drafter re-derived both); (3) its log's VERDICT line and its `--json` file agree (parse `numTotalTests`, `numFailedTests`, `numTotalTestSuites`, `success`); (4) its floor/belt/SESSION_SECRET lines are present in the same hold (`HOLD.out`); (5) sha256 of each file you cite, quoted. **Only gate 11's P1 full verifies of `67b840b` and `7d853b0` qualify. Its MT1 (at `5531d7b`) does NOT stand for your merged tree** (M0 moved); cite it as a cross-check of the arithmetic only. Copy what you cite into YOUR evidence dir (never edit gate 11's).
- **H-30 (C-133's script version, ruling l).** The id-superset accounting uses a COPY of `session-tools/s78g/c133-accounting.py` whose sha256 you MEASURE and quote — **expected `6f938bfcf2557d9f986894734e4b79390dfb90fbc7c62d63b989fbe58f6f972f` (the RD-658 version, in place since 2026-09-29T23:07:38Z)**; if it differs, name the version you used and why. Never edit the shared script; never use the `.pre-rd658-…` copy except as a named comparison.

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
5. **Report per ticket (all seven):** population, negative cells, still reaching, disarmed.
6. **The new members' negative cells (batch 12 additions, same method, same self-test):**
   - **F (RD-653) NARROWS a negative cell by design:** rd408-r2's "neither the value nor its length is in the health body, the page or the process output" now counts a `23` only where `reportsLength` says it is REPORTED. Enumerate what reaches the cell's check at M0's rule and at the head's (n2, n3) — every leak form the head no longer sees is named; the ones the CONTROL claims are the Majors.
   - **D (RD-649) adds a hook that can SILENTLY do nothing** (anchor miss → compile unchanged): R5-CTRL is a POSITIVE cell whose green is only meaningful if the hook ran (l1).
   - **E (RD-608)**: C1 is a POSITIVE cell ("exactly [general, setup, ai-test] ran") and CTRL guards the census's liveness; the negative reading ("no other limiter ran") depends on the wrapper seeing every limiter (k3).
   - **C (RD-657)**: rd327's R5/R6 are NEGATIVE cells over the public health body ("only allow-listed keys", "no raw identifier") — the body now carries `2.2.1`; show they still reach their checks on MTp.
   - **G (RD-671)**: the two CONTROL (RD-671) cells assert REJECTION — prove each reaches the branch it is named for (a0's mutants are that proof; say so).

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

## 6. TARGETS C-G (TIER 2 each). Answer each with a measurement.
1. **Scope, per ticket:** `git diff --name-status <merge-base> <head>` = the files §1 lists, nothing else; D, E, F and G touch nothing under `backend/`, `static/`, `docs/`, no package file; C touches exactly `backend/server.js`, `package.json`, `package-lock.json` among product paths.
2. **POSITIVE CONTROL FIRST per ticket:** v0 (C), l0 (D), k0 (E), n0 (F), w0 (G). Then the rest of each ticket's rows.
3. **C (RD-657):** (a) one source (v2's M-cache and M-path, v4); (b) the public bodies (v3); (c) the lockfile and `node_modules` (v5, v6); (d) C-181's conditions met — R7 re-anchored in the C-131 shape with a red proof (v0, M2), one cell proving ONE source without grep (V1, v4); (e) the R7 RENAME's accounting (ruling e, §8.5).
4. **D (RD-649):** (a) M-iv → exactly R5 (l0); (b) the anchor-miss path red, both cells (l1); (c) the anchor on every combined blob (l3/y4).
5. **E (RD-608):** (a) the census's mutants (k0, k2); (b) its blindness (k3); (c) CTRL's count on MTb/MT1/MT2 (y3).
6. **F (RD-653):** (a) OLD and LEAK red (n0); (b) the phrasing table (n3); (c) L-F1 reproduced (n2); (d) under A's bands (n4).
7. **G (RD-671):** (a) M-top/M-substr exactly (w0); (b) the variable slot and injected fragments (w2); (c) depth and case (w3).
8. **PRIOR WORK (C-49), each READY's claim READ at the diff:** C — "Nothing removed except the literal", rd327 R7 KEPT as a control (re-anchored), IMAGE_VERSION untouched; D — RD-607's at-load build KEPT, S1 and R1-R4 unchanged; E — gate 1's `qa-limiter-census-preload.js` ledger kept, its express wrapper and SIGUSR2 stack walk left out; F — RD-408 round 2's (`8cca478`) value check, timestamp stripping and case cells KEPT, only the bare-token scan replaced; G — RD-665's rule and four cells KEPT. Every `-` line quoted with where its behaviour lives now.
9. **C-190 (READ ONLY), per ticket:** no PR → CodeQL NOT RUN. Say whether any changed line matches a pattern CodeQL flags (C's `require` of a JSON file; D's `fs.writeFileSync(MARKER, …)` and `Module._extensions` override; E's preload's file writes; F's regexes — linear?; G's regexes over template text) — READ ONLY, a note for the merge author; C-190 includes test code.

## 7. rd549 O4 ON M0 (ruling j). Answer with a measurement.
1. **O4's state on M0** (o0, o1): CI attempt 1 quoted; attempt 2 named as a re-run; your local solo and under-load results.
2. **Cause (i), (ii) or (i′)** (o2): the distribution, with the instants.
3. **RD-591 and O4** (o3): **"RD-591 fixes O4" is claimable ONLY if (i) is measured to dominate and o3 shows `arrivalTime` keeps those boots green.** Otherwise the verdict line says "RD-591 not measured as O4's fix".
4. **Whether O4 blocks any member's merge is Tuesday's** (C-185: an O4 failure is outside the known set — a STOP for merges until ruled). Report; do not rule.

## 8. THE MERGED TREE (C-68, C-57, C-89, C-104, C-112, C-133, C-187). No verdict is complete without it.
1. **Build it in YOUR OWN scratch clone** under `projects/nexusai/qa-trees/batch12.*/clone-1`: `git clone --shared --no-checkout <repo> <dir>`; in the clone only: remove `origin`, set a local
   `user.name`/`user.email`, `gc.auto 0`, `core.fsmonitor false`, hooks off; `git checkout -b gate <M0>`; then `git merge --no-ff` in the PROPOSED ORDER: **`3ef057f`, `8bc88f5`, `9fd5c9a`, `20fea84`** (= MTt), **`5584ea4`** (= MTp),
   **`874c4f5`** (MTa), **`7d853b0`** (MTb), **`67b840b`** (= MT1); then, in a SEPARATE clone (`clone-x`) built from MT1's commit, `git merge --no-ff 608a1cd` (= MT2; skip if M0 already holds it). **Write your prediction for each merge BEFORE it; anything other than the
   counts file conflicting STOPS (C-57).** Re-measure every pair by `merge-tree --write-tree` in a SCRATCH object dir first. **C-104: resolve and stage before any census or run.**
2. **Resolve the counts file by REGENERATION, never by hand:** take a side (a placeholder) to complete each merge commit, then `npm run verify -- --maxWorkers=2 --forceExit --update-counts` ONCE on MT1 after all
   merges, through the lock, SESSION_SECRET UNSET, under its deadline; commit the regenerated file in the clone. **Predicted 4272/260 at M0 = `ca7de45`.** Then a plain verify of the committed head.
3. **Order independence (a control that can fail):** clone-2 in REVERSE (`67b840b`, `7d853b0` — which brings `874c4f5` — `5584ea4`, `20fea84`, `9fd5c9a`, `8bc88f5`, `3ef057f`). **The two `HEAD^{tree}` must be identical apart from the counts file** — quote both
   tree ids and the `git diff --name-only`; the side control run INSIDE the clone that owns both.
4. **Blob identities (C-133's C-112 control):** member paths at MT1 == their head's blob — A (`bb45cd7`, `a17dd70`, `252bf5a`, `27419fe`, `4711147`, `1988b46`, `6ae80ce`), B (`6608eae`, `4925b58`, `1007b66`), C (`c66efcd`, `15eb6f1`, `b34b7d7`, `384805d`, `64d8eda`), D (`431ec80`, `e90fa2c`, `af97704`), E (`5e43fa7`, `c44df7e`), F (`c82761e`), G (`e6649cc`) (A's and B's as gate 11 measured them; re-derive);
   **`backend/server.js` a COMBINED blob (name it; none of `0d7e387`, `c9f0d65`, `86dc63f`)**; `image-content-exposure` = M0's `7e3262b`; every other `__tests__` file == M0's or a head's; **`package-lock.json` = C's `64d8eda`** (unless RD-732 landed: then a combined blob, named). **`__tests__`: 306 at MT1, 308 at MT2
   predicted.** **The census's "M0 left out" control must FIRE for this parent set** — redo it with one member only if it reads 0.
5. **id-superset control (C-57) with C-187's ADDENDUM and RD-657's rename — ruling (e): PREDICT, then measure, all K1.** merged ids ⊇ ids(M0) ∪ ids(each of the seven heads) ∪ ids(`874c4f5`)? **Predicted: missing 3** = C-187's pair
   (from the `874c4f5`/`7d853b0` side, `94e6e4c`) **+ rd327's OLD R7 title** (from M0's and the D/E/F/G/A side, `a4db84d`); **new ids 43 vs M0** (rd591 13 + rd618 13 + rd735 6 + rd657 3 + rd327's NEW R7 1 + rd607 R5/R5-CTRL 2 + rd608 2 + rd408-r2 CONTROL 1 + rd665 CONTROL ×2 2); **counts delta +42** (43 new − the old R7). The C-187 pair is ACCOUNTED only when each of **(a1)** base = branch = `94e6e4c` (`1904765`, `874c4f5`, `7d853b0`); **(a2)** merged = M0's `7e3262b` = RD-466's head blob; **(a3)** `git log 1904765..<M0> -- __tests__/image-content-exposure.test.js` lists only `8de8e5c` and `3f7e263` (re-verified by the launcher at `ca7de45`); **(a4)** RD-466 changes no title in that file; **(b)** the replacement ids present and green on MT1 — is MEASURED. **The R7 rename is ACCOUNTED (drafter's reading, ruling e) only when C-133's two conditions hold ON BLOBS: merged rd327 = C's `b34b7d7`; the other side's blob = the base's (`a4db84d` at M0 and at `5531d7b`); and the new R7 is present and green on MT1.** **Any other missing id is a STOP.** Use a COPY of batch 10's
   `qa-c57-id-superset.sh` (keeps the lock-holder refusal; proven first to STOP on a planted missing id and to pass a superset) with the C-133 script per H-30.
6. **The semantic overlaps git cannot see (C-68), in holds per H-28:** on MT1 — every C-68 set of the MERGE ORDER table BY NAME (per-file counts), rows g6 (MT1 arm), x1, x3, y1-y4, e1, r1, o3, n4, the full verify. On MT2 — x2, y3, y4. Then ONE mutant
   per ticket on MT1: **g9's M-c** (B6 red), **e6's M1** (B1, R8 red), **v2's M2** (V1, CTRL, R7 red), **l0's M-iv** (R5 red), **k0's M-skip** (C1 red), **n0's LEAK** (the length cell red), **w0's M-substr** (the URL CONTROL red).
7. **C-89 on your clone:** `git diff --quiet HEAD` holds; `git show HEAD:scripts/verify-expected-counts.json` equals the regenerated counts.
8. **Main at your END:** `git merge-tree --write-tree` (scratch objects) of each member onto the END main — counts-only? any combined blob named.
9. **Nothing leaves your clone.** No push, no remote, no PR, no ref written in NexusAI. **Count `<repo>/.git/objects` files before and after your whole session and account for any delta by FULL-DATE mtime** (live seats
   commit and merge there; `--shared` clones and merge-tree freshen mtimes — say so).

## 9. CI (C-185, C-190) — NOT RUN AT ANY BRANCH HEAD (no PR exists)
- **Drafter (READ ONLY, NexusAI's own `GH_CONFIG_DIR`, ~09:11-09:13 AEST):** `gh pr list --head <branch> --state all` returned `[]` for all seven member branches and `rd-618-csp-intake-residue-s86m` (control: without `--head`, #36 rd-197, #35 rd-703, #34 rd-466, all MERGED). **CodeQL is NOT RUN at any member head.**
  M0's push Build **36635558304**: attempt 1 `failure` (rd549 O4 only, 4229/4230); **attempt 2 `in_progress`** at 23:11:57Z (a re-run).
- **Re-read with `gh` READ ONLY:** whether a PR now exists for any member branch (a PR opened by the merge author mid-gate is theirs — read it, do not touch it); for any PR, its CodeQL `Analyze (<language>)` runs (C-190: the
  `CodeQL` summary run can read completed/neutral before the analyses exist) and any NEW high-or-higher alert in changed code; M0's Build 36635558304, every attempt, and its failing set against C-185's set (row o0).
  **`gh` never merges, approves, comments, reviews, labels, re-runs, dispatches, sets a variable, dismisses an alert or opens a PR.**
- **CI and RD-591 (L-A4):** CI's Linux runner, its `lsof` and its `ps` are UNVERIFIED until a PR's Build runs; say so in the verdict line.

## 10. Floor discipline — THE FOUR CLAUSES, plus MERGES GO FIRST and THE DEADLINE RULE
1. **MERGES GO FIRST (ruling i).** **The jest lock `session-tools/nexusai-lock.sh` (queue `session-tools/locks/queue-jest/`) is shared with the builder seats; merges are stopped at drafting (ruling j) and restart one at a time.**
   - **Do ALL lock-free work first:** pins, reads, merge-trees in scratch objects, unit-level rows on `createCspEntryBudget` and `stripQueryAndFragment` with plain `node` (no jest, no server), census greps, prior-work reads, the f4 and n3 probes, w2/w3 against the rule function run in plain `node`, g8, o0, the H-29 re-checks.
   - **Then file your holds (H-28)**, each tagged `qa-b12-…` (e.g. `qa-b12-H1-verifies`), each a tracked child of your seat. **If a MERGE ticket (a tag containing `merge`) is queued AHEAD of you, you wait behind it (that is FIFO). If a MERGE
     ticket FILES BEHIND YOU BEFORE YOUR HOLD IS GRANTED, re-file your ticket behind it:** stop YOUR OWN unstarted waiter (its ancestry proven to reach your claude pid — C-174: by pid, never by pattern), confirm your
     ticket went to `released/` as `ticket-left-*`, and re-queue with `--after <that merge ticket's tag>` (C-141 ADDENDUM 4's tool). Record each re-file (time, the merge tag, your new position). **Once your hold is
     GRANTED, carry on** — a running hold is never interrupted; **between holds, re-file behind any merge ticket.**
   - C-141: your hold is gate-class; builder PROOF tickets self-apply a yield to it (ADDENDA 2/3). **QUEUE, NEVER TAKE OVER:** never kill, signal, move or edit another seat's process, lock directory, owner file or
     ticket, even if it looks stuck; if a holder looks stuck, mail a QUESTION (§12) and keep waiting.
2. **Hold the lock for a planned block of work, never idle (H-28)** — at most ~90 minutes of planned jest per hold. Every hold is a TRACKED CHILD of your seat, never detached (`nohup … &`).
3. **Count foreign servers the C-125 way, anchored on YOUR OWN claude pid:** `basename(argv[0]) == node` AND the server entry point anywhere in the remaining argv; "ours" = the ancestor chain CONTAINS your own
   claude pid. **Record the foreign count BESIDE EVERY RESULT.** **NEGATIVE controls, all in the same run, all must classify FOREIGN:** `62649` (NexusAI-M), `9959` (NexusAI-N), `38362` (NexusAI-O), `20317` (NexusAI-P), `62677` (Tuesday s94) — Tuesday named the live seat pids at stamp (NexusAI-M, -N, -O, -P and her own), each in backticks.
   Re-read them at start; if one has exited, say so and use the others; **a hold with NO live negative control aborts.** Reuse gate 11's instrument BY COPY with YOUR pid as `ROOT` and
   these as `NEG`: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-30-gate-batch11/evidence/qa-floorlib.sh`
   (**its defaults are STALE — `ROOT=98861`, gate 11's seats — correct `ROOT` and `NEG` before any hold**) and `…/qa-floorcount.py`; the original counter is gate 7's
   `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-22-gate7-rd645/evidence/qa-floorcount.py`. **Also count every dialer and every CPU-burner child you start (g3, o2) by pid from your ancestry, and prove 0 left after each run.**
4. **A zero is reportable only beside a control that fired in the same window** — the floor count, "0 refused" (g3's control dialer refused), "LOST 0" (a planted lost cell caught by your compare), "missing 3 / other 0"
   (the planted-missing-id control), "userinfo absent" (f1's plain control), "guarded by no cell" (the mutant LANDED and parsed), "0 incidental matches" (n4 beside n0's LEAK red).

**5. THE DEADLINE RULE — every real-server probe, every dialer and every request has a per-step DEADLINE, a HEARTBEAT, and kills its server in a `finally`.**
Every HTTP request carries a client timeout; each step (boot 120 s, request 30 s, dialer run 180 s, targeted jest 600 s, C-68 union 2,400 s, full verify 2,700 s, in-hold part wait 600 s, exit 25 s) has a written DEADLINE (`qa-to.sh`);
a step past it is ABORTED and reported, never waited on. **Log a HEARTBEAT line at least every 2 minutes during any hold (H-4: a separate child, ≤ 120 s max gap, aborted if absent at 90 s); a step with no heartbeat
for 5 minutes is aborted and reported,** and a hold that is not progressing releases the lock. Every server, socket, dialer and child you start is killed in a `finally` (SIGTERM, then SIGKILL after a grace)
**by pid from your own ancestry, never by pattern (C-174)**, and the reap is confirmed by your floor counter. **H-20 and H-21 apply to every jest.**

## 11. HELD
- **LOCAL RUN, NOT THE DEMO:** every server request goes to a server YOU (or a cell) booted on 127.0.0.1 from YOUR tree. **g3's dialer dials only `127.0.0.1:<the stand-in's port>`.**
- **External hosts you MAY contact, and nothing else:** `git ls-remote origin` (pins, C-192 retries); `api.github.com` via `gh` READ ONLY (§9); `api.agentmail.to` (your verdict mail, STATUS and any QUESTION).
  **No Azure, no npm registry (never `npm install`/`npm ci`), no CDN, no demo, no customer-test tenant, no Entra tenant, no Partner Center, no docker, no ARM deployment, no Redis other than the cells' own fakes.**
- **FINDINGS-ONLY (ruling f):** no fix, **no merge outside your own clones, no push, never push — not to main, not to ANY author's branch**, **no PR opened, commented, approved or merged (C-190 is the merge
  authors' route, not yours)**, no deploy, **nothing to Partner Center, the demo or production**, no money, no external comms, no mail to any human. **No `az` at all.**
- **Never write into** the builders' `session-tools/` (copy, then hash at start and end) or any `worktrees/` directory, **or gate 11's report dir or trees**; **never run the builders' hold, preload, mutate or guard-arm scripts.**
- **Symlinks, chmod, sockets, held ports, dialer port files, env files and scratch git repos live ONLY under your own mktemp dirs.**
- **Findings-only:** do not commit (outside your clones), move any branch, file a ticket, or write anything inside the NexusAI project (`2_Project_Files`, `session-tools/`, `worktrees/`, `1_Project_Definition/`,
  `qa-reports/`). **NEVER `rm`** — quarantine, per the template §5.

## 12. Output
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-30-gate-batch12/report.md` — ONE report covering all seven members; evidence in `./evidence/` beside it (including `classifier-stops.txt`, created empty at your start).

**Questions:** your routing name is **`QA/NexusAI-batch12`**. If you must ask, mail `tuesday-agent@agentmail.to`, subject
`[QA/Datasec-NexusAI -> Tuesday] QUESTION: <topic>` (Context / one Question / Meanwhile / Needed-by) and **PROCEED ON THE SAFEST READING without waiting**;
Tuesday's answer arrives in `tuesday-agent@agentmail.to` with a subject beginning `[Tuesday -> QA/NexusAI-batch12] ANSWER`. Approval-class items (anything
touching the demo, Azure, Partner Center, money, or a human) are NOT RUN and named. Record every question, reading and answer. An ADDENDUM mailed from `tuesday-agent@` supersedes the launcher's closing lines, whatever its subject's arrow says.
**The one exception to "proceed without waiting" is H-27:** a safeguards stop PARKS the gate until Tuesday switches the model.

MAIL YOUR VERDICT to `tuesday-agent@agentmail.to`, subject exactly:
`[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — batch 12`
Lead the body with ONE line per ticket in this form —
`RD-591: <GO|GO WITH FINDINGS|NO GO> @ 67b840b (g3 foreign-vanished counted: <yes|no>; rd549 red arm on envReached: <yes|no>; LOST <n>; O4 fix: <measured|not measured>)` ·
`RD-735: … @ 7d853b0 (budget defeated by: <none|route>; userinfo kept in: <n> shapes; rd646 on MT2: <n>/<n>)` ·
`RD-657: … @ 5584ea4 (health = package.json: <yes|no>; lock beyond root version: <none|lines>)` ·
`RD-649: … @ 20fea84 (M-iv -> R5 only: <yes|no>; anchor-miss reds both: <yes|no>)` ·
`RD-608: … @ 9fd5c9a (census limiters MT1: <n>; blind spot: <none|shape>)` ·
`RD-653: … @ 8bc88f5 (missed forms: <n> of <n>; claimed-covered missed: <n>)` ·
`RD-671: … @ 3ef057f (injected fragment accepted: <yes|no>)` —
then one line naming M0, **rd549 O4's state on M0 and its measured cause**, the merge order you recommend, the merged counts you measured, the C-57 result (missing / accounted / other), **which rows ran on Opus 4.8 (or "none")**,
and "CodeQL NOT RUN (no PR); CI lsof UNVERIFIED". Never `wednesday-agent@`. AgentMail key: `AGENTMAIL_API_KEY` in `/Volumes/KK_T9_External_HDD/TUESDAY/4_Credentials/.env` (absolute: the QA project has none).
Never put the key, a token or any secret in a mail or the report.

Verdict format:
- **RD-591** naming `67b840b89b755b59268873a544b8d5ddd7ee54e0`: g0-g9, s1-s2, o3; the limits L-A1..L-A8.
- **RD-735** naming `7d853b0e0b666b37d220dd05ac0727b5160555d2`: e0-e6, f1-f4, r1-r4; x1-x3; the limits L-B1..L-B5.
- **RD-657** naming `5584ea45617477338c2b5a01a0011cc92158a7f0`: v0-v7, y1-y2; L-C1..L-C5. **RD-649** naming `20fea841f5723ebd2981836a41a779b7d88f44dd`: l0-l5, y4; L-D1..L-D3. **RD-608** naming `9fd5c9a34af35358fbad704a173910bb9c1aee3c`: k0-k4, y3; L-E1..L-E4.
  **RD-653** naming `8bc88f5c1835e3d0b7e7ef124717973d733fc90c`: n0-n4; L-F1..L-F2. **RD-671** naming `3ef057f343c2cc9f93ab416d2c420646d8c349d0`: w0-w3; L-G1..L-G3.
- **rd549 O4 on M0 (§7):** o0-o4, its state and cause, and whether RD-591 is measured as its fix.
- **The merged tree (§8):** M0; both orders; counts regenerated once (measured vs 4272/260 re-based on M0); the id-superset result with C-187's (a1)-(a4)/(b) and the R7 rename; the C-68 sets by name; one mutant per ticket; C-89; the END-main
  merge-trees; the object-count accounting; **your recommended merge order.**
- **The §3b sweep:** per ticket, population / negative cells / still reaching / disarmed.
- Each of **L-A1..L-A8, L-B1..L-B5, L-C1..L-C5, L-D1..L-D3, L-E1..L-E4, L-F1..L-F2 and L-G1..L-G3** answered: discharged with a measurement, or left standing and named (C-112).
- All refs as **three timestamped readings (start / mid / end)**, each with its branch name and C-192 attempt count.
- **§3a H-1..H-30:** for each, that it was followed, with the self-test outputs (H-1), landing controls (H-3, H-10), max HB gap per hold (H-4), byte checks (H-9), the g0 decision (H-23), every deadline that fired
  (H-20), every restore hash (H-21), **every safeguards stop and the model per row (H-27), every hold and its planned/actual length (H-28), every PRIOR measurement re-checked and cited (H-29), the C-133 script's sha256 (H-30).** **§10: every lock re-file, with the merge tag it went behind.**
- Every action recommendation carries its evidence class: **MEASURED AT RUNTIME / PROBED / READ ONLY**. Severity is yours; priority is Tuesday's.
- **Rule 2: a NOT TESTED section.** It MUST carry this line, verbatim:

  Not tested by this gate: Linux or CI at any branch head (no PR exists, so no CI Build and no lsof/ps on a Linux runner), CodeQL at any head without a PR, two real concurrent seats' full suites against each other, multi-replica deployments, a real ingress in front of the CSP intake, a real Redis, a Docker image build, an ARM deployment, any browser, the npm registry, any deploy, docker, real Azure, Partner Center, the demo, and Windows.

## WRONG OR UNVERIFIED IN THE COMMISSION AND THE READYS — carried so the gate inherits the corrections
**Carried from gate 11's brief (W11-1..W11-11, each still true at `67b840b`/`7d853b0`; read them there):** RD-591 READY's "main faea66b merged forward" (merge-base with M0 is `faea66b`; main is now `ca7de45`); its "tier 2" (Tuesday ruled TIER 1); its "READY verify at 67b840b's tree" (the hold ran on `HEAD 5e00f0a dirty`, the commit came after — gate 11's P1 verify of `67b840b` then measured 4208/4208 on tree `13ac0b8`, PRIOR under H-29); the rd549 red arm rode `NODE_OPTIONS`; "rd554-restore-harness's header" is `helpers/rd554-restore-harness.js:88-89`; "25 guarded test files" UNVERIFIED (6 `guardServer` callers, 21 `listenInBand`/`listenOnReservedPort` users); "1 in SLOT_COUNT" is per pair; RD-735 READY "server.js (+19/-4)" is +18/−5; `https://h?x=a@b` PARSES; `trust proxy 1` with no ingress takes `req.ip` from a client XFF; C-187 applies to B (gate 11's drafter's addition).
1. **Commission "Merge turns: P, M, N, O (the C-186 ADDENDUM at CLARIFICATIONS:1931)"** — the ADDENDUM "THE TURN PASSES" is at **:1933** now (C-186 itself at :1926); `:1931` is the stale number its own duplicate note (:1939) cites. The ADDENDUM's order is **O, P, M, N, then O again**; "P, M, N, O" is the same cycle starting at P. Cited as measured.
2. **Commission "RD-657 changes package.json 1.3.0 -> 2.2.1"** — CONFIRMED (`cdb1168` → `384805d`), and its lock change is ONLY the two root version fields (READ whole diff). **"RD-657 and RD-732 both touch package-lock.json"** — CONFIRMED; the three-argument merge-tree `5584ea4 × daf2210` (base `f9cb440`) is clean with 0 conflict markers — a COMBINED lock blob (row v6).
3. **Commission "Main's push Build 36635558304 on ca7de45 FAILED 4229/4230 on rd549 O4"** — CONFIRMED for **attempt 1** (job `109635197795`, completed 22:40:02Z). **The run's CURRENT state is attempt 2, `in_progress`** (a re-run started 22:43:58Z) — `gh run view 36635558304` shows `status in_progress, conclusion ""`, which reads like "not failed" unless the attempt is named. C-185: no re-run is a clearance.
4. **Commission "stopped by Opus 5.5's safeguards 5 times" / Tuesday's lesson "five times"** — gate 11's `evidence/classifier-stops.txt` holds only **TWO** lines (02:41:25 and 02:45:59 AEST). The other three stops are UNRECORDED on disk (UNVERIFIED by the drafter). H-27 makes the one-line record mandatory.
5. **Commission "HOLD.out (its P1/P2 full verifies … and the MT1 --update-counts + plain verify ran)"** — CONFIRMED (quoted in PRIOR ROUND). **Gate 11's MT1 was at M0 = `5531d7b`**, so it cannot stand for this gate's merged tree (H-29).
6. **The four S86N READYs' "Full verify PASS" (RD-649 4223/254, RD-608 4223/255, RD-653 4222/254, RD-671 4232/255)** — each `verify-hold.out` stamps the run **`HEAD <parent> dirty:`** (`62385d9`, `b896c7b`, `cdc6438`, `4088b20`), i.e. the commit BEFORE the READY head (the READY head is the counts commit on top). The verified content is presumably the committed content — UNVERIFIED by the drafter (the builders' worktrees were not read); your own verify of each head decides. (Same shape as W11-3 for RD-591.)
7. **RD-657 READY "(parent 5531d7b = main at build time, by ls-remote)"** — true then; main is now `ca7de45` (RD-703, RD-197). C is NOT forward-merged; merge-base(C, M0) = `5531d7b`. **RD-649/608/653 READYs "from main 67e8928, not rebased"** — true; RD-197 landed since. **RD-671 "from main ca7de45"** — true; it fast-forwards M0.
8. **RD-657 READY "Counts 4210/254 -> 4213/255"** — CONFIRMED. **"RED … exactly P1, V1, CTRL, R7 fail, 4 of 41"** — RELAYED (the drafter did not read `rd657-hold2.log` whole; only the verify VERDICT line).
9. **Drafter's addition, not in the commission: RD-657 RETITLES rd327's R7** (ruling e) — the C-57 prediction is missing **3**, not 2. The "grant" for the rename is the drafter's reading of C-181's build condition, not a Tuesday ruling — Tuesday may want to rule it at stamp.
10. **RD-608 READY "The server builds 8 limiters, not 7"** — RELAYED; the drafter did not count limiters. y3/k1 measure.
11. **Drafter's own slips, disclosed:** the project's hook refused one `cd` (re-issued with absolute paths); zsh ate `:s` in `$H:scripts/…` on one `git show` loop (re-issued under `/bin/bash` with `"${S}:…"`, H-11/H-18 — the counts table above is from the re-issue); one census used `\x27` inside a double-quoted `grep -E` and returned 0 for every sha (re-issued from a script file; the 54/55 populations above are the re-issue's, and match gate 11's); one `grep -cF` of rd549's O4 `toEqual` literal inside `$(…)` was brace-expanded by bash (the launcher builds that pattern in a single-quoted variable; presence at M0 is also shown by blob identity `4a35642` = `faea66b`'s, where gate 11's launcher proved it). **No `merge-tree --write-tree` was run by the drafter:** every merge prediction is the three-argument form. **No fetch.** The drafter read builder evidence by single-directory `ls` and `grep` of named files only; no recursive search of any project tree. `gh` was used READ ONLY with NexusAI's own `GH_CONFIG_DIR` (run/attempt/job metadata and ONE job log, saved to the drafter's own scratchpad).

## PROVENANCE (drafter, 2026-09-30 ~09:10–~10:30 AEST, read-only; EXACT times only where a `date` call stamped them, the rest "~")
- origin refs | `git ls-remote origin` (one call; `refs/heads/*` and `refs/pull/*/head`) | **09:10:39 AEST** (date-stamped; first attempt, no publickey denial)
- chains, parents, dates, messages; merge-bases; ancestry of `874c4f5`/`608a1cd`/A/B in M0 | `log --format`, `merge-base`, `rev-list`, `merge-base --is-ancestor` | ~09:11
- counts, `__tests__` counts, lock/package/server/test-server/ICE blobs at 15 shas | `git show` + python, `ls-tree -r -z`, `rev-parse` | ~09:12
- M0's Build 36635558304: run, attempts 1 and 2, attempt 1's job and its log's failure lines | `gh run view`, `gh api …/attempts/1`, `…/jobs/109635197795/logs` (READ ONLY) | **23:11:57Z = 09:11:57 AEST** (date-stamped) – ~09:14
- `gh pr list --head` for 8 branches + control | `gh`, READ ONLY | ~09:11
- RD-657 × RD-732 three-argument merge-tree; RD-657's lock/package diff whole | `merge-tree <base> <a> <b>`, `git diff` | ~09:13
- `c133-accounting.py`: size, sha256, mtime | `ls -la`, `shasum -a 256`, `stat` | ~09:13
- CLARIFICATIONS: size/lines/mtime; C-number line numbers; C-133 + both ADDENDA, C-150, C-177 + CORRECTED + ADDENDUM, C-181, C-184–C-187 + ADDENDA, C-190, C-192, C-193 read whole | `ls -l`, `wc -l`, `grep -n`, `sed -n` | ~09:14–~09:16
- pairwise path overlaps and three-argument merge-trees, 36 pairs | `diff --name-only`, `comm`, `merge-tree <base> <a> <b>` | ~09:18
- RD-649's preload whole; the `_rlOpts` ANCHOR at 7 shas; RD-618+735's server.js hunks around the limiter; RD-657's server.js diff | `git show`, `grep -cF`, `git diff` | ~09:20
- test titles and requires of rd657, rd327, rd607, rd608, rd408-r2, rd665; title diffs base→head for rd327, rd607, rd408-r2, rd665 | `git show`, `grep`, `diff` | ~09:22–~09:26
- requirer populations (test-server, rd395 harness) at 13 shas; package-version readers; `2.0.1` mentions | `git grep -l` (commit-scoped), `git grep -n` | ~09:24–~09:27
- member blobs for the §8.4 list; RD-649/608/653/671 chains' full shas | `rev-parse`, `rev-list` | ~09:25
- gate 11: brief (559 lines) and launcher (631 lines) whole; `HOLD.out` whole; `classifier-stops.txt` whole; `vA/vB/mt1-*-full.json` parsed; evidence dir listing; `qa-floorlib.sh` defaults | `Read`, `python3 json`, `ls -la`, `grep` | ~09:05–~09:30
- builder evidence: `s86m/` listing (rd657 files), `rd657-verify-full.log` VERDICT; `s86n/rd649|rd608|rd653|rd671` listings and each `verify-hold.out`'s HEAD and VERDICT lines | `ls`, `grep` | ~09:28
- Kam's model ruling: Tuesday's lesson file (whole) and its commit `623db55e4` | `git show --stat`, `cat` | ~09:29
- routing: `QA/NexusAI-batch11` at `fleet/inbox_routing.conf:152`; **no `QA/NexusAI-batch12` line** — Tuesday adds it; the launcher's guard 40 refuses until then | `grep -n` | ~09:27
- report dir `2026-09-30-gate-batch12` absent | `ls -d` | ~09:27

## FILL AT STAMP — Tuesday, before launch (the launcher refuses until the starred items are done)
- ★ both STAMP placeholders at the top (the SELF-CHECK line and the Self-check note) — LAST, by hand, no placeholder token in the note.
- ★ the routing line `QA/NexusAI-batch12|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`.
- ★ the negative-control seats in §10 (replace the stamp placeholder there with the pids, each in backticks) AND the launcher's `NEG_SEATS` — Tuesday's own pid included.
- Optional: rule on WRONG 9 (the R7 rename's grant) so the gate need not ask.
- If RD-618, RD-646/647 or RD-732 LANDS on main before launch: the launcher prints a NOTE (not a refusal); the gate skips that merge step and re-bases (ruling b). If a member head MOVES before launch: the launcher's guard 18
  refuses — re-pin that head in the launcher and every occurrence in this brief, re-read its READY, never `sed` a sha blindly.
