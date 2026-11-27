GATE B2192: GO WITH FINDINGS @ fc5975f on main 826bb7a

Gate G1 (Opus), round 1 of 2. Scope: RD-1051, the rd490 port band (branch `b2175/rd490-portband`: N186's commits A and K, then N187's merge of main, M2), and RD-1052, the candidate jest lock (not installed). The gate was read-only: no PR, no push, no install, no Jira, no cd. Its only writes went to this folder and to scratch `fleet/state/s336/g2192/`. Clocks are from `date`: gate start 01:12:30, end 01:43 AEDT, Sat 28 Nov 2026. The gate made three acquisitions of the live lock (pair, verify, mutant), each with `lock-wrapper rc=0`. At the close the base held no lock directory and no ticket.

**No Blocker. One Major, and it gates only the later `slots-jest` write: neither the merge nor the install. Three Minor. Seven Info.**
- **The branch: GO.** Merge it by MERGE COMMIT pinned to fc5975f6 (landing.txt).
- **The candidate lock: GO to install AFTER the merge with `slots-jest` ABSENT** (install-steps.md). With the file absent the candidate is one slot: today's exclusion.
- **Writing `slots-jest`: NOT YET.** M-1 must be answered first. m-2 should be, or slots buy no parallelism.

## Lane, re-measured (gh api -X GET under the NexusAI GH_CONFIG_DIR, 01:12:54 and again at the close, 01:42:35: unmoved; the switch read 0 variables and the environments `[dev]` both times)
- main `826bb7a89bfe9517f5aa538a110ab0b1dea3317f`. `heads/b2175/rd490-portband` = `fc5975f631bb1fdd2536345f8eeee9e2e4eec165`. Open PRs 0.
- compare main...head reads `ahead 3 behind 0`; the reverse reads `behind 0/3`. The files: `__tests__/helpers/test-server.js` 3/2, `__tests__/rd490-open-access-banner-browser.test.js` 22/6, `scripts/verify-expected-counts.json` 2/2.
- The commits:
  - A `07fb8eb6`, parent d2aeecf8;
  - K `f1df71f5`, parent A;
  - M2 `fc5975f6`, parents K then 826bb7a8.

  `git show --cc fc5975f6` shows the counts file as the merge's only own hunk (6655/421 over 6635/419 and 6654/421). The merge's tree differs from main's in exactly the three paths.
- The two locks: candidate sha256 `52713e55345726abc769c4601cc52daf5b5496eab96b346ebacaada300356260`, 498 lines; live `cf01bafbc51f555ca0f14d1711f01885bcec5bc6293b177fe24702226bb4971f`, 391 lines. Both equal the commission's values, at the start and at the close.
- Both seats' STATUS files were read: N186's in full, N187's by its sections and every result line. They report:
  - plain verify 6655/6655 across 421;
  - `PAIRSUM m2 shape=OWN-SLOTS-DISJOINT result=BOTH-GREEN`;
  - `MERGE2181 post PASS`;
  - gitleaks clean with a control;
  - N186's Part L: arms 1-14, S and I PASS on the candidate; S1-S10 PASS; 11 mutants, each killing its named arm; a dry install `INSTALLED OK`; live inode unchanged.

  These are RELAYED. The gate re-ran what follows.

## 1. The branch (RD-1051)
- **Read whole** (`git diff 826bb7a8 fc5975f6`, and each commit). `claimPort()` now walks `workerBand()`. The reservation before the await, the refusal proof, `listenerPids` and the after-boot check that the listener is the file's own child are all unchanged. `PORT_BAND` is gone. One new cell checks that both servers' ports lie inside `workerBand()`. The helper change is a comment only. Every added line is ASCII. The static scan of the added lines and the messages for names, seat or build ids and ruling words read 0 (control: `band` 19).
- **The pair, re-run by the gate inside ONE acquisition of the LIVE lock:**
  - The lock: `nexusai-lock.sh jest b2192-gate-pair`, acquired after 0 s (queue empty) at 01:15:55 and released at 01:17:27, `lock-wrapper rc=0`. NODE_OPTIONS was unset and node was v24.22.2.
  - The tools: N187's frozen `pair2175.sh` and `pairsum2175.py`, sha256 equal to N186's table (`9edf9985...`, `262eb56b...`).
  - The trees: the gate's own, dot-free, at fc5975f6. `g2192/t/qa` is slot 0 (worker-1 band 20000-20039); `t/qb` is slot 11 (27040-27079). Before the run no listener sat in either slot's span (15 listeners in all).
  - The result: A 73 tests, 0 failed, 0 listener-guard messages, servers on [20000, 20001]. B 73 tests, 0 failed, 0 guard messages, servers on [27040, 27041]. Ports seen on both sides: [] (1501 sampler rows). Jest A rc 0, jest B rc 0. **`PAIRSUM g2192 shape=OWN-SLOTS-DISJOINT result=BOTH-GREEN`.**
- **The cell's control, re-run by the gate (one acquisition, `b2192-gate-mutant`):** in `t/qa`, `const band = workerBand();` was replaced by the old literal `{ start: 38900, end: 38940 }`; the anchor matched exactly once. The lock was acquired after 790 s, waiting in the FIFO behind the gate's own verify, and ran 01:40:51-01:42:26. Jest rc 1, 73 tests, **exactly 1 failed: the new cell**, with `server A listens on 38900, outside this worktree's band 20000-20039 (workerBand)`. Reverting brought back blob `a92d82b1` = the head blob, with porcelain 0. This matches N186's P5.
- **The full verify, once (one acquisition, `b2192-gate-verify`, plain mode in `t/qc`, slot 3, `npm run verify -- --maxWorkers=2`):** acquired after 0 s, ran 01:17:27-01:40:51, `verify plain rc=0`, `lock-wrapper rc=0`. It read `expectation tests=6655 suites=421`, then `suites=421 tests=6655 passed=6655 failed=0 jest.success=true`, then **`VERDICT: PASS — 6655/6655 tests passed across 421 suites (jest exit 0)`**. `^PASS ` lines numbered 421 (the control for the zeros), `^FAIL ` lines 0, `EADDRINUSE` 0. The tree's porcelain after the run was 0. node_modules is a symlink to N187's clone install; its package-lock sha256 `37e5add3...` equals the head's.
- **Can the band collide?**
  - *Across slots: no.* A band is `20000 + 640*slot + 40*(worker-1)` with worker 1-16 (`workerBand()` throws above 16). Each slot owns a disjoint 640-port span, 20000-32159 in all.
  - *With a fixed listener elsewhere in `__tests__`: no.* The gate searched `__tests__` and `tests/` for literal listens and `PORT:` values. Every spawned server takes `String(port)` from a reserved port. The only literals are 3001 and 8443 in config fixtures and 9921 in an e2e note, all outside 20000-32159. Every 5-digit number in the band range is a timeout, a day number or a source-line citation. `listen(0)` servers (scheduler-failure-vocabulary, rd761 and others) get kernel ephemeral ports, from 32768 on Linux and 49152 on macOS: above the top of the bands.
  - *Inside one run:* the file shares its worker's band with the other files of that worker. Those run one after another, and each port is still proved free by refusal. Nested jest runs take band 16 (RD-982). So no new overlap.
  - *Residual:* two trees on one slot (1 in 19) still search the same ports (I-1). A tree from before this change still uses 38900 (M-1).
- gitleaks 8.30.1: the control (a random AWS pair made in memory, never printed) read `leaks found: 1`, rc 1. Clean reads, each `no leaks found`, rc 0:
  - `git log -p 826bb7a8..fc5975f6` (messages and diffs);
  - `git log -p -m --first-parent d2aeecf8..fc5975f6` (812 lines, A, K and the merge's diff against K).

## 2. The candidate lock (RD-1052): read whole against the live lock, then proved in SCRATCH bases
`diff live candidate` gives three hunks. Lines 1-97 are byte-equal, so the default base on line 84 is unchanged. +106 lines of slot code follow. In the loop, `mkdir "$LOCK"` becomes `may_take && take_free_slot`, then `LOCK=$(takeover_candidate)` feeds the unchanged stale and ownerless block. The waiting line uses `holders_text` and the reason. The owner printf gains `slot=` and `wslot=`.

The gate's own arms: `g2192/lock/arms2192.py`, logs `g2192/lock/arms-*.txt`. They ran on a scratch copy whose default base was rewritten to a scratch path (`cand.sh`; the diff is line 84 only). Every caller got a fresh `NEXUSAI_LOCK_BASE` under `g2192/lock/bases/`, with `NEXUSAI_LOCK_POLL=1` and `NEXUSAI_LOCK_OWNERLESS_GRACE=3`. **The live base was never written.** Its entries read the same by name before and after every run, and its sha256 and queue were checked at the close. No arm process was left (`pgrep -f g2192/lock/bases` 0; control `pgrep -f zsh` 19).

| B2157 s.2 item | does the code do it? | gate proof (candidate) | control on the live copy |
|---|---|---|---|
| 1 slots for jest only | YES: `[ "$kind" = jest ]`; slot 1 keeps `nexusai-jest.lock`, slot k is `.lock.k`; 1-8; anything else is one slot plus one stderr line | A6v `'3\n'`->2, `' 3 '`->2, `'03'`,`'9'`,`''`,`'two'`->1; N186 S10 docker peak 1 | A6v all 1 (FAIL) |
| 2 FIFO kept | YES: only the oldest live ticket calls `may_take`; it drops its ticket after writing the owner file | A4k3: K=3, 5 waiters, peak 3, order k1..k5, 4th in 0.5 s after the first release. A4: w4 never passes w3 | A4k3 peak 1 (FAIL) |
| 3 stale and ownerless per slot | YES, one slot dir per poll (`takeover_candidate`: first dead pid, else first ownerless). **pid test only, no pstart (m-3)** | A3: slot 2 dead -> moved aside, w4 took slot 2, live foreign slot 3 untouched. A3b: dead holder on the caller's own wslot taken over. A3c: ownerless slot 2 taken after the grace | (N186 ARM 3/7 on both) |
| 4 owner `slot=`/`wslot=`; release moves own slot only | YES | A1 owners `slot=1 wslot=1`, `slot=2 wslot=2`. A5t: TERM to the slot-2 holder -> rc 143, `done-jest-c-*`, slot 1 still held | A1 owners have no fields (FAIL) |
| 5 slot-distinct holders | YES for a caller whose cwd is its tree or that sets `NEXUSAI_WORKTREE_SLOT` (env wins, then cwd's helper, else `unknown`; unknown or ownerless runs alone). **The slot comes from cwd, never from the command (m-2)** | A2: same wslot 5 -> serial (+0.49 s), reason printed. A4: w3 (ws1) waits for w1 (ws1) with a free slot. X3: cwd qa -> `wslot=0`; cwd without helper -> unknown; no node -> unknown | A2 has no reason line (FAIL) |
| 6 worker cap stays | not the lock's code (kits keep `--maxWorkers=2`) | - | - |
| 7 `slots-jest` absent = one slot | YES: SLOTS=1 unless the file exists and holds 1-8 | A6: absent, distinct wslots -> peak 1, serial, owner `slot=1` | - |

More arms: A1 (K=2, distinct wslots, peak 2, overlap); A5, kill -9 mid-hold (I-3 below).

## 3. Adversarial: shapes outside each property, and the install moment
Branch property ("two copies on different slots never search the same ports"):
- (b1) Two trees on the SAME slot: the same ports, by arithmetic. The listener check fails the file by name (N186's base run showed that message). Only the lock's wslot check separates them. **I-1.**
- (b2) A tree from BEFORE this change, running beside any other: it still claims 38900-38939. Two such trees collide exactly as in B2157's N=3 and N=5 runs. **M-1** (below).
- (b3) A host whose ephemeral range starts below 32160: kernel source ports could land in a band. This is not new: the rd573 file's cell E2 judges it on every run. Hosted Linux defaults to 32768. **Info, no grade.**

Lock property ("never two holders on one worktree slot; never more than K"):
- (x1) **The install moment / an old copy (X1).** K=3. New n1 (ws4) holds slot 2. An OLD-script waiter takes slot 1 as soon as it is free and ran BESIDE n1. The old script never reads `wslot`, so a same-slot pair is possible. Total holders stay at most K (N186 S2). The converse is safe: X1b, an old HOLDER (no `wslot`) makes new heads wait. With `slots-jest` absent both scripts use slot 1 only: the same lock (A6; N186 ARM I `order=[H W1 W2 W3 W4]`).
- (x2) **cwd is not the jest tree (X3, m-2).** `npm --prefix <qb> run verify` started from cwd `qa` records `wslot=0` while the jest runs on slot 11. The pair form runs two trees in one acquisition and can declare only one. Every current kit wrapper (N186, N187, this gate) calls from a cwd with no `__tests__`, so each reads `unknown` and runs alone. That is safe, but it means zero parallelism.
- (x3) **kill -9 of a holding lock script (A5).** Its job runs in its own process group (`set -m`) and survives. After the pid test, a same-wslot head takes the slot over and ran beside the orphan (`orphan alive=True`, `w2 ran while w1 child still ran=True`). The live lock has the same shape with one slot. **I-3.**
- (x4, extra) Cutting `slots-jest` 3 -> 1 while holders sit in slots 2-3: a new head takes slot 1 beside them while they drain (X5, peak 3). **I-5.**

**A seat started under the old lock while the new one is installed.** The install is an atomic `mv` to a new inode, so a running old process keeps executing the old file. A `cp` in place could make it read new bytes at old offsets, which is why install-steps.md forbids it.
- An old WAITER competes for slot 1 only: harmless while `slots-jest` is absent, the x1 hazard once it is present.
- An old HOLDER makes every new head wait.
- A caller that starts between the second idle read and the `mv` is an old copy of the same kind.

Every lock process is either queued or holding, so two idle reads before the swap, and again before any `slots-jest` write, prove no old copy is live. Kits that pin the live sha256 will read a moved value after the install (I-6).

## Findings
- **M-1 (Major; gates the `slots-jest` write, not the merge, not the install).** The lock cannot tell whether a holder's tree contains RD-1051. Trees that predate the change include:
  - every red-first run at an older BASE;
  - a gate re-running a pre-merge head;
  - any unmerged older branch (530 branches on the remote).

  Each still claims 38900-38939, and two of them under `slots-jest` ≥ 2 reproduce B2157's 72-test red regardless of their worktree slots. The candidate's wslot check does not cover it, because the fixed band ignores slots. Remedy (the coordinator's choice) is either of:
  - (a) the lock records `unknown` when the caller's `__tests__/rd490-open-access-banner-browser.test.js` still holds `PORT_BAND = { start: 38900`;
  - (b) kits refuse a slotted run in a tree without the merge (`git merge-base --is-ancestor <M> HEAD`).

  FOR-RECORDS ticket candidate 1.
- **m-2 (Minor).** `wslot` comes from the caller's cwd (or the env), never from the tree the command runs in (X3). A caller running elsewhere either runs alone (every current wrapper) or records the wrong slot (`--prefix` or `--rootDir` from another tree; the pair form). Remedy: wrappers export `NEXUSAI_WORKTREE_SLOT` computed by the target tree's own helper, and the pair form declares nothing. Candidate 2.
- **m-3 (Minor).** B2157 item 3 asks for "the same pid + pstart test". The candidate, like the live lock, tests the holder by `kill -0` alone, and the owner file has no `pstart`. A recycled pid keeps a dead holder's slot until that unrelated process exits. With slots, the other slots still work. Candidate 3.
- **m-4 (Minor).** The waiting line prints nothing for slot 1 when slot 1 is free and other slots are held (it then starts `| slot 2: ...`). Cosmetic, and it changes no decision.
- **I-1 (Info).** Two trees on one slot (1 in 19) share a band. That is by design: the listener check names it, and the lock's wslot check prevents it for declared callers.
- **I-2 (Info).** `rd591-cross-seat-isolation.test.js` (line 35, `RD490_BAND`) and `rd573-...test.js` (lines 65-70, 202) still name 38900-38939 as RD-490's band. They stay green, and the wording is out of date. The kit's Q-6 left them. Candidate 4.
- **I-3 (Info).** kill -9 orphan (x3). This is pre-existing, and slots do not make it worse for distinct slots.
- **I-4 (Info).** Head-of-line: a head blocked by a same-wslot holder holds back later tickets even when a slot is free and their slot differs (A4: w4 started 2.4 s after w1's end, behind w3). That is FIFO by design.
- **I-5 (Info).** Shrinking `slots-jest` while slots are held drains rather than enforces (x4).
- **I-6 (Info).** Kits whose REFUSE lines pin the live sha256 `cf01bafb...` must change that value with the install (install-steps.md step 8).
- **I-7 (Info).** The lock's `0-18` hard-codes test-server.js's SLOT_COUNT 19. A change there degrades to `unknown`, which is safe. `NEXUSAI_WORKTREE_SLOT` is taken ahead of cwd, the reverse of B2157 item 5's order, as recorded by N186 at L2. That is harmless.

## Landing texts (this folder)
`landing.txt` (PR, checks = PR 269's 7 names, code scanning 29 and 22 open, MERGE COMMIT pinned to fc5975f6, Deploy demo read-only), `pr-title.txt`, `pr-body.md`, `install-steps.md`, `FOR-RECORDS.md`. Evidence: `gate-run.txt` (this folder) and scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s336/g2192/` (`logs/`, `lock/`).
