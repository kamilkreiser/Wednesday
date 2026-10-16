# Drafter report — NexusAI gate 24 (RD-848 @ 065a0d8), for Tuesday

**Written 2026-10-17, finished 07:57 AEDT by `date`. A read-only drafting agent (Opus 5.5) wrote this for Tuesday.**

## BLUF
- **What I drafted:** the gate-24 brief, the launcher and this report. The launcher's `--check` passes every content guard. It now refuses on exactly two things Tuesday owns: the stamp (9 placeholders) and the routing line (exit 40). **The head has not moved:** `065a0d8f` on `rd-848-dockerfile-build-stage-s100o`, base main `17fc6c5`, both re-read at 07:56:59 AEDT.
- **Tier: TIER 1, round 1 of 2.** The Dockerfile is the deploy recipe. `deploy-demo.yml` runs `az acr build` and then deploys on every push to main whenever `CI_DEPLOY_ENABLED` is `true`, and I could not read that variable. The defect class only shows up at the image level. The new guard is a checker whose false negatives would re-open RD-846. "Already-gated follow-up" does not apply, because gate 23 gated RD-846 and never this diff.
- **The biggest trap:** two of the builder's headline proofs are true but cannot tell fixed from unfixed.
  - "Head builds on vfs": the base builds on vfs too, because its line-74 copy is latent.
  - "/app diff vs the demo image is EMPTY over 202 entries": since RD-846, production takes nothing from the build stage's pair.
  - What does tell them apart is the re-arm pair (P-base FAILS, P-head PASSES) plus a per-step census showing no no-layer COPY in any stage. The brief makes those the verdict's clause.
- **A probable guard false negative, found by reading the code (not run):** the guard treats `--chown`/`--chmod` as text. `COPY --chown=0:0 <held files>` therefore counts as "new" even though the real layer is empty. The live file has no `--chown`, so at most this is Minor. Row r6's M-chown0 measures it on vfs.
- **Tuesday must stamp before launch:**
  - the SELF-CHECK line and note;
  - T1–T7 (read T1 twice: it newly allows one `az acr run` against main's image by digest);
  - the routing line `QA/NexusAI-gate24|tuesday-agent@agentmail.to|no`.

## Files (absolute paths)
- Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_nexusai-gate24-rd848.md`
- Launcher (chmod +x, `bash -n` OK): `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate24.sh`
- This report: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-17_nexusai-gate24-DRAFTER-REPORT.md`
- The READY is already in `briefs/` as `2026-10-17_nexusai-rd848-READY-mail.txt`, so no copy is needed and the launcher needs no override.

## SHAs measured (commands quoted)
- `git -C "/Volumes/Laptop-DEV/!CODING/Datasec/NexusAI/2_Project_Files" ls-remote origin`, first attempt, rc 0, 07:38:45 AEDT:
  - `17fc6c5157d5446cc015e97555fdc1ffcdc986ee HEAD`
  - `17fc6c5157d5446cc015e97555fdc1ffcdc986ee refs/heads/main`
  - `065a0d8f0f871ecd77636231014511edf167cc8b refs/heads/rd-848-dockerfile-build-stage-s100o`
- The same two refs re-read at 07:56:59 AEDT, unchanged. The launcher's `--check` read them again, unchanged after 1 attempt.
- `git cat-file -t 065a0d8f` = `commit`; `git cat-file -t 17fc6c5` = `commit`. `rev-parse` gives the full shas above.
- `rev-list --count 17fc6c5..065a0d8f` = 4, with no merge commits: `9f20773`, `b2fc9bf`, `6e0e437`, `065a0d8`.
- No PR: `ls-remote origin 'refs/pull/*'` shows no ref at `065a0d8` (`refs/pull/86/head` = `3a45914`), read at 07:40:19 AEDT. **CodeQL has never run on this head.**
- Lock tool `shasum -a 256` = `3c33f5ae58e1be20282467a90b27a23a2de998eedd0e56c03f3c06360031a792`, which is the pin. Line 79 names the T9 base, and the T9 queues are present.

## TRAPS — where a claim is true but misleading, or the gate could pass without testing the thing
1. **Neither of the builder's headline proofs can tell base from head.**
   - "b2fc9bf: rc=0 Step 47/47 on vfs": 17fc6c5 also passes on vfs, because its no-layer copy is followed by a `RUN`.
   - "/app diff EMPTY": production has inherited the pair from `base` since RD-846, so removing a build-stage copy cannot change `/app` unless it breaks the build.
   - Both are now labelled no-regression checks. The brief's verdict clause is r1 (P-base FAIL / P-head PASS / M-readd848 FAIL, plus a census showing 0 no-layer COPY at head and exactly 1 at base).
2. **The ACR candidate is `b2fc9bf`, not the head.** cr4s tagged `rd848-cand-b2fc9bf`. The builder argues the two images are equivalent because `b2fc9bf..065a0d8` touches only `__tests__/` and the counts file. I confirmed that diff by READ, but the counts file IS in the build context (it is not in `.dockerignore`). The gate builds `065a0d8` itself.
3. **The builder's in-image lister is weak** (`manifest-in-image.sh`):
   - 16-hex digests;
   - follows symlinks and records no symlink target;
   - `node_modules` is one digest over regular files only, so `.bin` symlinks and every mode and owner inside it are invisible;
   - no image config;
   - `while read` mangles names that start with blanks.
   - "202 entries, EMPTY" means less than it sounds. r2 uses full sha256, lists every `node_modules` entry, and diffs the config.
4. **"Main's demo image" is a mutable tag.** cr4t pulled `nexusai:2.2.1-s99o-17fc6c5` by tag (digest `c12c43e5…`). Nobody measured whether the demo runs that digest. T1(a) lets the gate list it **by digest**.
5. **The guard's flag identity is textual** (`dockerfile-stages.js:214`): `--chown=0:0`, `root:root`, `node` vs `node:node`, `1000:1000` vs `node:node`. These are false negatives in the unsafe direction. Probe: r6 M-chown0, with the guard run on the same text and the build on vfs.
6. **The guard ignores mtime.** The "BYTE-IDENTICAL, not same-name" cell asserts that a different file with the same bytes is redundant. A naive diff compares stat, including mtime, so that layer is probably not empty. This over-reports, which is the safe direction: a NOTE (optional r6 M-sameBytes).
7. **The guard's test builds its context from `git ls-files` at describe-load.** In a tree with no `.git` the suite errors (loud). Jest trees must be clean clones.
8. **`git log` with no rev in the NexusAI repo reads the stale root checkout (`cd2b543`).** My first pickaxe for the pair's history returned NOTHING. With `065a0d8f` it returns `b2fc9bf`, `3f7e263`, `8de8e5c`. The brief requires explicit revs.
9. **The builder's probe commits sit in the shared object store** (`48c7676`, `396771f`, and `317018d`, a superseded placement that was wrong) and are reachable from any `--shared` clone. The brief forbids building or citing them. Loose objects: 242 (gate 23 counted 204).
10. **Gate 23's `evidence/inst/` holds `.throwaway-ss` (gate 23's T3 secret) and `quarantine/`.** A lazy `cp -R inst/` would copy a secret into gate 24's evidence. The brief says copy BY NAME, and the launcher checks that the brief names `.throwaway-ss`.
11. **Gate 23's docker objects still exist**: `qa-b23-dind-vfs`/`-ovl` and five r3/export containers. Each dind holds a pulled `node:24-alpine`, so reusing it is tempting. H-35 makes them FOREIGN, and the launcher NOTEs them.
12. **Gate 23 freshened mtimes in the NexusAI object store through `--shared` clones** (its §14 item 9). T6 defaults to `--no-local` (about a 35 MB pack) so the expected object delta is zero.
13. **Main is about to move.** At 07:56, `s100o-merge-rd802-verify` was in `queue-jest`: S100O is merging RD-801+822 and RD-802. Those merges regenerate `scripts/verify-expected-counts.json`.
    - The batch-23 pattern would have refused the launch on that.
    - I made a counts-only move a NOTE: it does not touch the image, and it means RD-848's merge will need C-57.
    - A move touching `Dockerfile`, `.dockerignore` or the npm pair still REFUSES.
    - Expect merge tickets ahead of the gate on the jest lock.
14. **"4525/284 = 4506/283 + 19" could be true while names swapped.** r4 compares names as SETS: base ⊆ head, and head − base = exactly the 19 rd848 names. Because `__tests__` changed, a base verify is its own hold (H3), with a READ ONLY fallback named if it starves.
15. **The CodeQL pre-scan is pattern-only and the builder says so.** `globRegex` (`:85`) builds a `new RegExp` from a Dockerfile token. That is probably not "remote input" to CodeQL, but the gate states it READ ONLY. The PR run decides, and none exists.
16. **`docker system df` is slow** (over 120 s; 178.7 GB of volumes, 39.5 GB build cache). It must never run inside a hold's deadline. The load at 07:52 was 15.8, and the plan ANSWER's limit is 40.

## What I could NOT verify (left for the gate or for Tuesday)
- The value of `CI_DEPLOY_ENABLED`, i.e. whether merging auto-deploys the demo. The gate is forbidden to read repo variables. **Tuesday may know it, and it bears on the tier and on priority.**
- Whether cr4s was built with `--build-arg BUILD_COMMIT_SHA`: its log does not carry the az command line.
- My reading in trap 5 (M-chown0 empty on vfs) and trap 6 (mtime) is inference from the code, not a measurement.
- I could not check the brief's "rd442 reads LICENSE" question in §3b. It is posed as a question for the gate.

## Tuesday must STAMP before launch
1. The `SELF-CHECK: re-read end-to-end for contradictions | <time>` line and the `Self-check note:`, both at the top of the brief, last and by hand.
2. Rulings T1–T7 (`RULED: @STAMP@` → "default" or the ruling):
   - **T1 (ACR):** default (a) lets the gate decide. At most one `az acr build` to `nexusai:gate24-065a0d8`, plus **one `az acr run` of the gate's lister inside its own image and inside `nexusai@sha256:c12c43e5…`**. That second part is new relative to gate 23, and it is the only way to re-measure the READY's demo-image claim.
   - T2 (image network)
   - T3 (throwaway secret)
   - T4 (where the gate lives)
   - T5 (Node 26)
   - **T6 (clone mode, default `--no-local`, new)**
   - T7 (anything else)
3. Add `QA/NexusAI-gate24|tuesday-agent@agentmail.to|no` to `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf`. The launcher never writes it.
4. Confirm the tier. If Tuesday knows `CI_DEPLOY_ENABLED`, put it in T7.

## `--check` output (07:55–07:57 AEDT; the drafter ran only `bash -n` and `--check`)
The first two runs refused at guard 81 because the brief lacked `_prebuilds` and then the literal `sqlite3 binding`. I fixed the brief both times. After the counts-move change (trap 13) the final run exited **40**:
```
NOTE: foreign containers present (builder rd84x-*, gate 23 qa-b23-*): qa-b23-r3-head qa-b23-r3-noarg qa-b23-r3-base qa-b23-exp-host-head qa-b23-exp-host-base qa-b23-dind-vfs qa-b23-dind-ovl rd846-dind-vfs rd846-dind — never started, stopped, removed or reused (H-35)
NOTE: 1 merge-tagged ticket(s) in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/session-tools/locks/queue-jest now — the gate files behind them (brief §9)
NOTE: no tmux pane named 'Datasec/NexusAI-M' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-N' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-P' — not a negative control this launch
NOTE: no tmux pane named 'Datasec/NexusAI-R' — not a negative control this launch
NOTE: fleet-monitor has no single live claude — not a negative control
guards pass (9 MODEL 6 8 18 18b 90 22 93 98 70 70D 31 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 38R 86); stamp, route and/or READY NOT complete.
  ls-remote attempts this run: 1 (C-192); origin main 17fc6c5; RD-848 065a0d8f0f871ecd77636231014511edf167cc8b; lock tool sha256 3c33f5ae58e1…; docker server 29.7.2; model claude-opus-5-5
  NEG seats (38R, derived live; coordinator pane 'tuesday'): `4056` (Datasec/NexusAI-O); `91571` (tuesday);
REFUSING (32): 9 stamp placeholder(s) remain in the brief (the SELF-CHECK line, the Self-check note and the RULED: slots T1-T7) — ...
REFUSING (40): no 'QA/NexusAI-gate24|tuesday-agent@agentmail.to|no' line in .../fleet/inbox_routing.conf — ...
```
**Negative control on the launcher:** with `QA_A_HEAD_OVERRIDE=<6e0e437 full sha>`, it printed `REFUSING: RD-848 is not 4 linear non-merge commits on 17fc6c5` (guard 8). The guard can fail.

**What the launcher keeps from batch 23:**
- the embedded prompt, which must name the brief path (guard 14 refuses otherwise);
- `--check`;
- C-192 retries;
- the model read from `models_latest.json`;
- the lock pin and T9 base;
- live negative-control derivation (38R);
- stamp and route last;
- the `SESSION_SECRET` unset;
- `exec claude --model claude-opus-5-5` from the QA project dir.

**What changed:**
- four linear commits (guard 8);
- a four-file delta (guard 22);
- line pins at base :23/:74 and head :23/:69, and no `--chown` in the head file (guard 93);
- counts 4506/283 → 4525/284 and census 336 → 338 (guard 98);
- instruments from gate 23's `inst/` on this drive (guard 31);
- T1–T7 slots and §2b C1–C10 (guard 19);
- a counts-only main move is a NOTE.

## Launch command (after the stamp and the routing line)
```
bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh' add 'QA/NexusAI-gate24' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate24.sh'"
```
Pre-flight: `bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate24.sh' --check` should print `all guards pass:` and exit 0.

## Drafter's own actions (disclosed)
- **NexusAI repo, read verbs only:** `ls-remote`, `cat-file`, `rev-parse`, `log`, `show`, `diff`, `grep`, `ls-tree`, `count-objects`.
- **Reads:** `session-tools/s100o/` and gate 23's report and `inst/` (cat, grep, shasum).
- **Docker, read only:** `version`, `ps -a`, `images`, and one `system df` that ran in the background and returned late.
- **The launcher's `--check`**, three times, plus one negative-control run.
- **Not done:** no clone, build, container, `az`, `gh`, mail, pane tap or lock ticket.
- **Files written:** the three outputs above and two scratch `--check` captures in my session scratchpad.
