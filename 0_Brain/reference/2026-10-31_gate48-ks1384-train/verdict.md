## QA GATE 48, TIER 1, round 1: the KS-1384 train (#1853 F0a, #1854 F0b, #1857 F0c, #1858 F-b)
(Opus, Sat 31 Oct 2026. Findings only. Probes, logs and mutant runs are in `probes/`.)

**Heads.** I read them with ls-remote at the start and again at the end; they did not change:
- 1853 = 969df457
- 1854 = 31e79759
- 1857 = dfc0dd61
- 1858 = 9e7dfdcf
- Base: 1838 = f27499dd, gated by gate 41.

Each PR is exactly one commit on the one below it. The delta stats match W's numbers exactly (24/+1663/-75, 11/+1394/-25, 7/+429/-18, 14/+1275/-7). Develop has moved 14 commits since 1838's base, but none of them touch anchoring or packages/shared.

**Design rev 4.** It is not in the repo; git grep finds only quotes of it in code comments. I tested against those quotes and against Kam's two rulings as the code quotes them (2026-09-14 retry; 2026-09-25 KS-1171 (c)).

**Train scope.** The F-b commit message says "Part of the KS-1384 train (F-a, F0a, F0b, F0c, F-b, R1, R2): do not merge alone". R1 and R2 are not in this stack. This verdict covers F0a to F-b on top of F-a.

## VERDICTS
| PR | Verdict |
|---|---|
| #1853 F0a | **GO WITH NOTES** |
| #1854 F0b | **FIX BEFORE MERGE** (one item, F1) |
| #1857 F0c | **GO WITH NOTES** |
| #1858 F-b | **GO WITH NOTES** (design readings 1 to 4 need Wednesday's ruling, D1 below) |
| **TRAIN** | **NO-GO as it stands → GO WITH NOTES once F1 is fixed, or once Wednesday or Kam accepts F1 in writing** |

The train is clean apart from F1. All 22 of my mutants on the money branches are killed. Every suite is green except the known threadTokenMint cell.

## FIX BEFORE MERGE
**F1 (MAJOR, narrow; F0b `attemptFamily.ts` rule 0 and `anchorSubmission.ts:777`). A family with no u_F has no mutual exclusion, so one payload can be submitted twice.**

How it happens:
- `recordMember` sets `fam.uF = chooseFamilyOutpoint(pass1Inputs)`.
- `pass1Inputs` comes only from pass-1 coins. A first member built in pass 2 from add-backs alone therefore leaves `uF` undefined.
- Every later member is then built WITHOUT `required` (`...(fam?.uF ? {required} : {})`) and on coins disjoint from member 1, because member 1's live inputs are claimed.

Measured:
- **P1a (real spendFromView).** A pass-2 build that used only an add-back reports `pass1Inputs = []`, and `chooseFamilyOutpoint([])` is undefined.
- **P1b (real submitter, F0b's own fake world).** Member 1 is accepted and its in-lock poll times out. A front-door re-POST then resets the row to (pending, NULL), as the upsert does at index.ts:1506. Result: built 2, **sent 2**, two live transactions for the same anchor and payload on disjoint coins. Both can land: a second fee and a second anchor.
- **P1c control.** The same scenario with u_F set: built 1, sent 1, and the row waits.

Reachability:
- It needs pass 1 to be unable to pay while an add-back can, which means a low-balance, busy wallet.
- It also needs a same-payload re-attempt while member 1 is still live: a re-POST, or the q9 upsert.
- The guard-3 retry path does not reach it, because member 1 must be refused, and therefore dead, first.

Rev 4's rule 0 ("never an add-back") leaves this case undefined, so this is a design gap as much as a code gap.

Smallest fix shape, for W to choose: when a family exists with no u_F and any member is live or not yet settled, wait (rule-4 style) instead of building. A cell should pin it (P1b is the shape).

## NOTES (none block on their own)
**N1 F0a, batch write-ahead (P4).**
- `writeAheadEveryRow` writes every row before it decides. With counts [1,0,1], rows 1 and 3 are already in 'submitting' carrying the unsent hash when it throws.
- The batch catch then writes 'failed' to all N rows, unguarded and leaving the hash in place. The rows end up 'failed' and naming a transaction that was never sent.
- No money is lost. This is a readback-honesty issue.
- The batch path also takes NoSpendableUtxo as a terminal batch failure. It is not the design's §3.5 wait, which only the single path implements.

**N2 F0c, a thread-mint has no TTL (P5).**
- `parseSignedBody` now maps a missing TTL to +∞.
- A mint that is 'lost', or 'accepted' but never confirmed by the outside-lock poll, stays live and claims its input and collateral for the life of the process; `settleExpiredSpenders` can never settle it. The control (finite TTL) is settled dead.
- This is liveness (coins stranded until restart), not money.

**N3 F0a, the wallet view is never pruned.** `WalletView.prune` has no production caller (grep). Dead entries, and confirmed entries older than 24 h, stay forever, so `claimed()` walks a list that only grows. The same holds for FamilyRegistry (removed only on close).

**N4 F0a/F-b, process-local state and a second process.**
- The second-process case is STATED, not hidden: attemptFamily.ts header ("a second process's transactions are outside every family at any uptime"), drivingSet.ts header, and KS-705 NOT HANDLED in anchorSubmission.ts.
- The "census" is a comment and a deploy rule only. No code or log line enforces or reports it.

**N5 changed existing cells: justified, and not weakened.**
- ks726 F2 now asserts that a swallowed write-ahead (null) stops the submit. The old window cannot open any more because null now throws. Guard 5's hash-carrying write is still pinned by the next cell, and G2 (null submits) is killed by this cell.
- ks1385 R2 ADDS `sent === 1` on real Postgres (stronger), and still asserts submits = 2 and declined > 0.
- The ks705 casts are type-only. tsc over src plus tests at the top gives 0 errors.
- The F-b edits to ks584 and the two fa reconciler files only inject the two new required dependencies.

**N6 instrument note.** W says "every cell mocks lock, provider, socket". The f0c header says it uses the REAL lock. My P3 probe on the real `withWalletLockWithin` confirms both behaviours:
- It times out at 30 ms, never runs fn after the lock frees, and the queue moves on.
- Control: a holder that frees in time lets fn run exactly once.

**N7 F-a's gate-41 gaps (nr) and (nc)** now exist as cells. (nc) runs on real Postgres with a positive control on the write path.

## D1: W's design readings (tested; they need Wednesday's ruling, not mine)
1. **m-3 as a 10-minute boot grace** (reconciler.ts:131, cell m3; mutant G15 is killed). This is weaker than the boot arm's S_boot + 7200 + 600 slots (about 2 h 10 min), which guard 3 uses.
   - Consequence after a restart: a (pending, NULL) row whose hash a re-POST nulled while a pre-restart transaction was still within its TTL can be swept 'failed' ("nothing was submitted") about 20 minutes after boot, and that transaction may still land afterwards.
   - That is a wrong terminal state, not a fee. Any second fee would need a later re-POST, which is the same exposure as before F-b.
   - The "census line" is a comment, not code (N4).
2. **R6 searches the row's own metadata_label, and the batch path is driven.** Both are TRUE in code (index.ts:2009, reconciler adoptScan).
   - Caveat: batch rows get a per-row `timestamp` (index.ts:839-853), but the batch transaction carries only the first row's payload. R4 and R6 adopt can therefore match only the first constituent row; the rest fall back to the old give-up. No money effect.
3. **Only a whole-window search is terminal, and a partial search defers R4.** TRUE: G10 and G11 are killed (fb-sweep r5 and s-cells).
4. **p6b pins the sweep side.** TRUE: G14 and G21 are killed. p6b drives the row through the wait timer.
- **W's expectUpdatedAt addition is sound.** It is compared as timestamptz, and cell tz (session time zone Australia/Sydney, with a control) passes. The rp cell's re-POST is a hand-written UPDATE that mirrors the upsert, not the product upsert itself. G12 (SQL ignores it) and G13 (R6 omits it) are both killed on real Postgres.

## (a) Money paths (by reading, plus mutants and probes)
- **Write-ahead:** the submit happens only on count === 1, and admission to the view comes only after the write-ahead resolves. Killed: G1, G2, G4.
- **Batch:** submits only on N of N rows. G3 killed.
- **Guard 3:** retries only on 'absent' (KS-1171 (c)), only for a member of this process, and only once the arm is armed or the reply lacks "already been included". Killed: G5, G6, G7, G8, G17.
- **Family u_F is required.** G9 killed, except for F1.
- **Give-up and R6.** Killed: G10, G11, G15, G16.
- **In-lock confirm write names its hash.** G20 killed.
- **Family closure needs depth 3.** G22 killed.
- **Thread-mint:** checks the caller before signing (G18) and never runs after the lock wait times out (G19).
- No submit-after-give-up path was found. No double-submit path was found apart from F1.

## (b) Concurrency
- Restart mid-flight: the row names the transaction before submit (R4 owns it), or nothing was sent.
- A re-POST racing R6: guarded by expectUpdatedAt (rp, on real Postgres).
- A re-POST racing the single path: covered by families and q9, except for F1.
- Two processes: out of scope, and stated as such (N4).

## COUNTS (each instrument named)
- **Unit, anchoring top (vitest, --maxWorkers=2):** 714/715. The only red is threadTokenMint.
- **threadTokenMint run alone: RED.** It fails the same way ("Could not serialize the data: Unsupported type", applyParamsToScript) in two separate installs: (a) the workspace root `npm ci`, and (b) a standalone `npm ci` from anchoring's own lock in an isolated directory. The test imports no product file and is unchanged across the stack, so it is not a train defect.
  - **"Passes alone" is NOT reproduced here.** Node is v26.8.1 on this host, versus gate 41's unknown version.
- **Real-Postgres lane, top:** 122/122 (10 files).
  - Container gate48-pg, postgres:15-alpine, with repo docker/init plus scripts/run-migrations.sh (applied 57, failed 0). App role secuura_app.
  - The KS-1384 files gave 20/20. pg_stat_database showed 52 tuple writes during that run.
  - Control: a bad URL gives 4 failed files and 0 passed.
- **Per-PR delta cells at head, against the lower PR's product files swapped in (sha-restored):**
  - F0a: 68/68 at head; 13 failed and 22 passed at base.
  - F0b: 29/29 at head; files red at base (new modules).
  - F0c: 10/10 at head; red at base.
  - F-b: 50/50 at head; 2 files red at base, and the 2 pre-existing reconciler files pass at base.
  - Cell counts match W: F0b 32 (24 + 5 + 3 PG); F-b 31 unit + 9 PG.
- **tsc (service tsconfig):** 0 errors. Positive control (an injected TS2322) gives 1. Over src plus tests: 0.
- **My mutants:** 22/22 killed, each restored by sha256 against a unique anchor (`probes/mut/`).

## Merge with develop
`git merge-tree` of develop cb232036 with 1858: code merges clean. It conflicts only in the 2 Projects Documents html files (**DOCS HOLD**, noted only).

## Spark shadow (`spark_gate.sh`, work dirs in the session scratchpad, base = pr/1838; copy in probes/spark)
- spark_gate.sh resolved the merge-base, but shadow_facts.py reported "merge-base (empty) · diff 0 files". Its BASE run therefore ran HEAD product code: 68/68 on both sides.
- **Instrument fault for stacked PRs:** its base side is invalid for a non-develop base. Its head side agrees with mine (68/68).
- I did not run it for the other three PRs, because the same fault would recur. The per-PR base controls above stand in for it.

## NOT TESTED
- Any chain, Blockfrost, wallet or box.
- lucid `presetWalletInputs` honouring the candidates for collateral (F0c) beyond the cells' fake mint.
- Real CSL coin selection reaching a pass-2-only build (P1a uses a fake builder; P1b overrides onBuilt).
- The product upsert in a live re-POST race.
- Node 24 LTS. This host runs Node 26.8.1 (Blockchain CLAUDE.md requires LTS).
- Schemathesis, Akto, Playwright, k6, eslint, hook legs (including leg 14 / KS-1884), preflight.
- R1 and R2.
- Two real anchoring processes.

## HOW
- **Clone:** `git clone --shared --no-checkout` from gate 47's clone into the non-existent `repo/`. Toplevel asserted, origin set to Secuura/Distributed_Secuura, push URL `no_push_qa_gate`, Blockchain deploy key set as core.sshCommand.
- **Fetch:** refs/pull/{1838,1853,1854,1857,1858}/head and develop. Detached at 9e7dfdcf.
- **Setup:** root `npm ci --ignore-scripts` (1806 packages), then a build of @secuura/shared.
- **Probe hygiene:** probes were copied into src only for their runs, then moved to `probes/_quarantine_2026-10-31/`.
- **Final state:** `git status` clean; HEAD back at 9e7dfdcf.
- **Clean-up:** gate48-pg stopped and removed by name. No git write verb was run in !CODING. Every PID I started has exited.
- **Instrument faults during the run:** my waiter loops matched their own command line in pgrep and had to be stopped with TaskStop; the hooks refused `$W` git write forms and dot-dot redirects, so I re-ran with literal paths.
- **Leftovers:** two spark worktrees remain registered in the scratchpad (`git worktree list`). They are harmless and are not deleted, per the never-delete rule.
