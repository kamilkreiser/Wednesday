# Gateset 2026-10-06_gate68 — README for Wednesday

**gate68** is the T1 gate for ROUND 2 OF 2 of Secuura/Blockchain PR #1393 (KS-1278, author Seat B 65th). It was drafted by one Wednesday drafting subagent between 2026-10-05 ~22:50Z and ~23:20Z by the host clock.

Every builder figure in this README is a **claim**: the gate re-measures it. Every drafter figure names the instrument that produced it, and the drafter's own results are **predictions**, not evidence.

## 0. Bottom line

**Status:** the kit is complete and the dry run has been executed (§5). The gate has **not** been launched and the routing line has **not** been added.

**Round cap.** This is round 2 of 2. If the gate says NO GO, the closed instances ship and the residue gets a ticket. There is **no round 3 without Kam.** The prompt and the launcher both enforce this, and the launcher refuses with rc 33 if the prompt lacks `ROUND 2 OF 2`.

**The head is a parameter, not a fixed pin.**
- Every script takes `--head` (or the environment variable `G68_HEAD`).
- The repin script renders `{{HEAD}}` into the prompt and also writes it to `head_at_launch.txt`.
- At launch, both the repin script and the launcher re-read refs/pull/1393/head and the branch with ls-remote, and refuse unless both match.
- The repin script also requires `--addendum <file>` naming that exact head (rc 18), and refuses any head other than `kit.json head_expected` unless `--accept-unexpected-head` is passed.

**Pins**

| What | Value | Instrument |
|---|---|---|
| Expected head | `b5adaba751d89fda0b138e0b8b74d702e2a2a429`, tree `82567f920582`, ONE parent `97ce2f337ae6` | ls-remote from the scratch clone at **23:12:20Z**: branch and pull/head both b5adaba |
| Stand-in head (previous) | `97ce2f337ae6a8bfda1e60831c2890933242c3a3`, tree `ae3680c5e170` | ls-remote at 22:50:01Z / 22:50:20Z, from the checkout and from the clone |
| Develop at the READY | `22b268143a63` | author's claim; drafter ls-remote at 22:50Z agreed |
| Develop now | `3f9ff4e1e1b93e2e704918a7825f13a72c9ec76f` (#1385 KS-938 merged), tree `2203187daaa2`, one parent 22b2 | ls-remote at 23:12:20Z, then fetched BY SHA into the scratch clone |

What changed between 97ce2f and b5adaba:
- b5adaba changes 3 files (+27/-8): the test, the flow doc and the cheat sheet. documentRepo.ts is untouched (`git diff --stat 97ce2f b5adaba`).
- The stand-in 97ce2f figures are kept in `_quarantine/standin97ce_dev22b2_era/`.

What changed on develop between 22b2 and 3f9f:
- auth `mfa.ts` and `users.ts`, the ks938 test, and **both** platform docs.
- 0 kit code paths and 0 hook paths (`c1_headb5ad_dev3f9f_ex1.out` P11).

**Tier: T1.** The change touches document revoke and a tenant-scoped UPDATE that decides whether provenance PII rows are written and whether anchors are emitted.

**Merge seat:** to be ruled by Wednesday (RULINGS Q1). The kit forbids Seat B 63rd, 64th and 65th, because 65th is wrapping cold per its own addendum.

## 1. Drafter predictions at b5adaba751d8 over develop 3f9f

| Check | File | Result |
|---|---|---|
| C1 pin | `c1_headb5ad_dev3f9f_ex1.out` | rc 0, 12/12 (see notes below) |
| C2 product | `c2_headb5ad_ex2.out` | rc 1, W6 FAIL (see notes below) |
| C3 jest | — | **NOT RUN by the drafter** (no npm). Self-test 29/29 (`c3_selftest_headb5ad_ex1.out`); every tamper LANDS on b5adaba |
| C3b real Postgres | `c3b_pgprobe_headb5ad_ex1.out`, `c3b_pgprobe_selftest_headb5ad_ex1.out` | 9/9 PASS; self-test 5/5 (see notes below) |
| C4 containment | `c4_containment_headb5ad_ex1.out` | rc 0, 5/5 (see notes below) |
| C4 merge-in | `MERGE_IN_PREDICTION.txt` | KEY (`last`) **`1711f2b944a8`**; `after-pred` **`5dab555016b7`** (they differ); git merge-tree **`6297e9c915bf`** rc 1 → **DIVERGENCE YES** |
| h2 proof | `c4_h2proof_dev3f9f_ex1.out` | 4/4. Develop flow has 17 `<h2`, 5 split across lines; the old reader finds 12, the tolerant reader 17 |
| gh | `gh_api_headb5ad_ex1.out`, `gh_prtext_headb5ad_ex1.out`, `gh_actions_headb5ad_ex1.out`, `gh_census_ex1.out` | see notes below |

**C1 notes.**
- P2 confirms the chain 32e0 → 4a16 → 97ce2f → b5adaba, and merge-base == 32e0.
- P3b: the follow-up touches only test, flow and cheat.
- P5 measures trailers on both instruments. For the content measure, both commits print 0 and control bf277eead268 prints **53**. For the raw `| wc -c` measure, both commits print 1 and the control prints **55**.
- P7: subjects are 84 chars (97ce2f) and 79 chars (b5adaba).

**C2 notes.**
- W2 key shape passes.
- W3 cast guard passes: `${id}::uuid` appears exactly once (:248, in getDocument) and `${idAsUuid}::uuid` exactly once.
- W4: the unguarded template is byte-identical to round 1's (sha256/16 `624c23a64753040f`, 487 bytes). It is **not** identical to develop's: it differs by the round-1 guard line.
- W5 census: 13 production callers, 1 opted in (:2398). That is 26 grep lines at the head versus **24 at 4a16**.
- **W6 FAIL:** an unfilled `KS-TICKET` placeholder.
- W7 passes at b5adaba: R2 is positional via slice(-2). W7 FAILED at 97ce2f, where R2 was a membership test.

**C3b notes.**
- With two concurrent sessions the guarded write gives **1/0**. The control (develop's statement) gives 1/1.
- A non-UUID gives no 22P02.
- External_id precedence holds, and cross-tenant revokes touch 0 rows.
- The probe uses machine-local PG 18.3. **Running it in the gate needs X9 (RULINGS Q3).**

**C4 containment notes.**
- Versus 4a16: the flow has 1 region and the cheat 4 regions, all inside the KS-1278 block at both ends.
- Each document minus its block equals 32e0.
- Both commits touch the test **and** both docs.

**gh notes.**
- The PR is open and `dirty`.
- Body: sha256/16 **8d8d2c59871447e6**, 8,766 bytes = 8,714 characters.
- The title is the **round-1** title.
- T1, T2, T3 and T5 are clean.
- Actions: 1 run at each head (Dependabot, skipped).
- Census: 23 others, 0 OVERLAP, 2 DOCS (#1394, #1383).

## 2. Defects found in the author's claims (READY and new-head addendum)

- **D-a FALSE in the committed flow doc**, at both 97ce2f and b5adaba (`:2293`).
  - The doc says: "At the branch base and at round 1 … answered 400 'Document is already revoked' with 0 provenance rows".
  - At the branch base 32e0 that request answered **200 with 1 provenance row**, and the status was never written. gate65 probed this, and the PR body's own table agrees.
- **D-b FALSE in the cheat sheet and the READY:** "N2 … proves the ::uuid cast is never reached for a non-UUID (22P02)".
  - N2 runs a driver simulator that ignores bound values and never raises 22P02, so it **cannot** catch the guard's removal (U1).
  - The guard is true by READ (c2 W3), and on a real database by pgprobe P3, whose planted U1 arm does raise 22P02.
- **D-c `KS-TICKET` placeholder** in committed code at documentRepo.ts:583, where KS 1424 belongs (c2 W6).
- **D-d The READY's "R2 asserts the VALUE bound after IS DISTINCT FROM" was FALSE at 97ce2f.** R2 was a membership test, which the SET clause's `'revoked'` satisfies.
  - The author's own matrix later measured G7 and T5 as uncaught.
  - b5adaba fixes this with an exact-text substring check plus slice(-2).
- **D-e New residual (gate's own T5b): appending ` OR TRUE` after the exact clause is predicted BLIND to b5adaba's R2.**
  - The clause text survives verbatim, and the last two bindings are unchanged.
  - On a real database it updates every row of every tenant (pgprobe planted arm).
  - Whether this blocks is a question for the gate and Wednesday (RULINGS Q5).
- **D-f Trailer control "53, not 55 — the 55 is WRONG".** These are two instruments, and both numbers are true: 53 is the content measure and 55 is the raw measure. The kit pins both.
- **D-g "24 grep lines"** holds at 4a16; at 97ce2f and b5adaba the count is 26.
- **D-h The READY's body figures (6,584 bytes / `c089b13d8cb5735b`) are not the live body.** The body moved twice. The new-head addendum's figures (`8d8d2c59871447e6`, 8,766 bytes) **match** the live body.
- **D-i Polish.**
  - The 97ce2f commit message has a word-per-line break ("Document\nis\nalready\nrevoked").
  - b5adaba's message says "K1 -> R1278 N1".
  - The PR title is still round 1's (Q6).

These new-head addendum claims hold:
- one diff region per doc against 97ce2f (flow pre-line 2284; cheat pre-line 3956-3957), measured with `git diff -U0`
- subject 79
- trailers 0/53
- documentRepo.ts untouched

The addendum's claim of 4/4 tamper rows caught is **unverified** here, because C3 was not run. The gate re-runs G7, G8, K1 and T5 itself.

## 3. Kit files

| File | Purpose | Self-test, and an arm that must fail |
|---|---|---|
| `kit.json` | pins, blobs, tampers (T1-T6, G7, G8, K1 corrected, K2, U1, T5b), claims, predictions | — |
| `composee5_copy.py` | Seat E 5th's readers, verbatim. sha256 `f9ab42d9…` equals the origin, by `shasum` at drafting. Never executed | — |
| `lib_gate68.py` | read-verb git; write verbs outside `!CODING` only; GitHub GETs with the token read by name | — |
| `c1_pin_gate68.py` | C1 P1-P11, P3b | `c1_selftest_ex1` 4/4; planted round-1-as-head `c1_planted_round1ashead_ex1` rc 1, 8 FAIL |
| `c2_product_gate68.py` | W1-W8 | `c2_selftest_ex2` 12/12 (6 planted arms); planted `c2_planted_round1ashead_ex2` rc 1 |
| `c3_tests_gate68.py` | redfirst / tamper / suite / tsc; **0 executed = LOAD FAILURE, never "not caught"** | `c3_selftest_headb5ad_ex1` 29/29; planted `c3_selftest_planted_round1ashead_ex1` rc 1 (tampers do not land); refusal of `!CODING` rc 2 |
| `c3b_pgprobe_gate68.py` | the real-Postgres probe (needs X9) | self-test 5/5 (planted U1 / T1 / T5b / K1 each FAIL); refusal rc 2 |
| `c4_docs_gate68.py` | containment, h2proof, predict (`--cheat-anchor last\|after-pred`), mergetree, qm M1-M8 | `c4_selftest_headb5ad_dev3f9f_ex1` 17/17 (git-auto-merged-flow and take-OURS SIMs fail M1+M8); planted branch-base-as-head rc 1; qm absent develop rc 2 by name (fabricated, and genuinely absent in the shared checkout) |
| `gh_gate68.py` | api / actions / census / prtext | `gh_selftest_ex1` 6/6 (planted closing word) |
| `prompt_gate68.txt` | the gate prompt template (`{{MERGE_SEAT}}` ×3, `{{HEAD}}` ×36) | — |
| `launch_qa_secuura_ks1278_1393r2.sh` | the per-kit launcher with `--check` | the arms in §5 |
| `repin_and_launch_gate68.sh` | the launch action with `--dry-run` | the dry run in §5 |
| `MERGE_IN_PREDICTION.txt`, `RULINGS_wednesday.md`, `ROUTING_LINE.txt`, `api/` | the prediction, the open questions, the routing line, the API snapshot (b5adaba era; 97ce2f era in `api/_standin97ce_2308Z/`) | — |

sha256 of every script is in `kit.json` → `script_sha256`. `_quarantine/` holds superseded runs, which are never deleted. The `_scratch/clone` directory is created by the dry run: it holds objects only and no refs are written.

## 4. What is NOT tested by this kit

- **C3 entirely.** jest red-first, the tamper matrix, the suite and tsc were not run by the drafter (no npm install).
- Linear: KS-1278, KS-1419 and KS-1424 were not read. Whether **KS-1424 exists** is unverified.
- The KS-1419 correction comment has not been read sentence by sentence. That is the gate's job (prompt KS1419-CORRECTION).
- Live sweep, RLS (the probe runs as superuser on a DDL subset), multi-tenant mode, preflight legs 3/4/8, and the four platform suites.
- No qm run on a **real** merge-in M, because none exists yet.
- The real-launch path of the repin script (usage gate, cockpit) was **not** run.

## 5. Dry run and launcher arms

The dry run was executed against the **live head b5adaba**, not the 97ce2f stand-in, because b5adaba was at origin by then. It was run with a **placeholder** merge seat, 66th, pending RULINGS Q1. The real run re-renders the prompt and `head_at_launch.txt`.

Dry-run output (`dry_232120.console.txt` rc 0, plus the `dry_232121.*` files):
- step A: the addendum names the head
- step 0: the routing line is missing (reported only, because this is a dry run)
- api and census rc 0
- ls-remote at 23:21:56Z: develop 3f9f, pull/head and branch b5adaba
- all instruments agree on the head, and develop is unmoved
- the kit clone was created and fetched by sha
- c1 rc 0, 11/11
- the recomputed predictions: `last` 1711f2b944a8, `after-pred` 5dab555016b7, DIVERGENCE
- launcher `--check` rc 0
- `DRY RUN COMPLETE`

Launcher `--check` arms (`launcher_check_*_ex1`):

| Arm | Result |
|---|---|
| rendered, 66th | rc 0 |
| unrendered template | rc 8 |
| GO naming 65th | rc 8 |
| head file = 97ce2f | rc 6, caught by the ls-remote check; the "head in full" grep alone passes, because the prompt also names 97ce2f in full |
| ls-remote stand-in carrying the old head | rc 6 |

Dry-run command:
```
script -q /dev/null bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-06_gate68/repin_and_launch_gate68.sh 1393 b5adaba751d89fda0b138e0b8b74d702e2a2a429 --merge-seat <NN> --addendum /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-10-06_E6Q1195_B65newhead.txt --dry-run
```

THE launch command (**NOT run**): the same command without `--dry-run`. If develop has moved past 3f9f, also pass `--repin-develop <sha>`.

## 6. Routing line (NOT added)

Back up `inbox_routing.conf`, then add the line from `ROUTING_LINE.txt`:
```
QA/Secuura-ks1278-1393r2|coagent@agentmail.to|yes
```

## 7. Pane, report and rung 5

- Pane: `QA/Secuura-ks1278-1393r2`.
- Report directory: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-06-ks1278-1393r2-g68/`.
- Rung 5, in the pane: KS-1278 / #1393, the gate68 README or the charter being read, head `b5adaba751d8`, and a `*_gate68.py --selftest` run.
- Rung 6: `NOT-TESTED.written-first.md`.
