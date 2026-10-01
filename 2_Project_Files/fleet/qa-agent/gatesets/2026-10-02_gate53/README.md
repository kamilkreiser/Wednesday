# Gateset 2026-10-02_gate53 — README for Wednesday

Written by the drafter on 2026-10-02 (AEST; the work ran 2026-10-01T14:29Z – 15:24Z UTC, all times from `date -u`). Every figure below comes from the kit's own output file, which is named beside the figure.

## 0. Status and what remains

**KIT COMPLETE. It is READY to launch once the routing line (section 4) is added.**
- Launcher `--check`: rc 0 before AND after the controls (launcher_check_1.out, launcher_check_2.out).
- Launch-action `--dry-run`: rc 0 before the controls (repin_dryrun_0_before_controls.out, 14:47:00Z, taken BEFORE the connection-retry fix of section 5) and after (repin_dryrun_1.out, 15:23:40Z). The ONLY thing it reports is the missing routing line. It reads `BOTH INSTRUMENTS AGREE with the pins, 1 of 1`, and the census reads `0 touch a kit path or carry a kit key outside reported_overlaps | 12 expected overlap(s) reported`.
- Controls: normal **rc 0, 141/141 OK**; `--invert` **rc 1, 141/141 MISMATCH** (section 5).
- **Still Wednesday's: the routing line (section 4) and the launch (section 9).** A real launch also needs `WED_USAGE_STOP=100` ONLY while Kam's 17:40:22 grant holds (usage read **95%** at 14:32:51Z, rc 3); after his account switch on Fri 2026-10-02 morning, drop it and let the new account's gauge decide.

Drafted **PINNED**. Wednesday named #1369 at head `ce051988b787f510c7ca5db5bbc474ef4b8a8492` on base develop `ea6fcecc3a6f71a4f397ea678da54a06df130cd7`. The drafter re-read both:
- by `ls-remote` in the scratch clone (14:29:47Z, 14:35:59Z) and by the launch action's own `ls-remote` from the checkout (14:46Z, 14:47Z): branch == `refs/pull/1369/head`;
- by the PULLS API (gh_read_1.out, 15:03:26Z): open, base develop @ ea6fcecc3a6f, `mergeable True` / `unstable`.

A new head, or ANY develop move, means a RE-DRAFT (section 8).

**What the drafter did and did not do.**
- It launched nothing and added no routing line. It sent no mail, posted nothing, and changed no ticket or PR.
- It merged, committed and pushed nothing, and deleted nothing.
- It wrote only to this kit directory and to `g53_sp/` in its session scratchpad (`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/79817561-2a8e-42cd-8745-2ef3ab0b0516/scratchpad/g53_sp/`). Every git write verb (fetch, merge-tree --write-tree, commit-tree, `apply --cached` under a temp index, hash-object, the control plants) ran in the scratch clone only.
- In `/Volumes/DevMASTER/!CODING/` it ran only `ls-remote` (through the launcher and the launch action), a read-only `clone --shared` as a source, and file reads (gate52's report, for its sha256).
- External reads: GitHub REST GETs (the PR, files, commits, the open-PR census, compare); npm REGISTRY reads (`npm view`, and `npm audit --json --package-lock-only` on manifests + locks extracted from the clone into the scratchpad — no install, no script ran). GH_TOKEN was read by name and never printed. Linear was not read.
- No `npm ci`, suite, tsc, prisma, container or image build ran in drafting. Those are the gate's.

## 1. The PR and the BLUF

| PR | ticket | tier | head | parent | ahead / behind | files | subject declared -> lands |
|---|---|---|---|---|---|---|---|
| #1369 | KS-530 (Refs, narrows) | T1 | `ce051988b787f510c7ca5db5bbc474ef4b8a8492` | `ea6fcecc3a6f` (= develop, #1368's merge) | 1 / 0 | 3, **+3/-18** | 83 -> 91 (PR title == commit subject) |

- Pane: `QA/Secuura-batch1369` (**not routed**, see section 4). GO string (the GO mail's SUBJECT): `GO (Seat B 54th): merge 1369 on gate53`.
- Report dir: `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-02-batch1369-g53/` (it does not exist yet).
- Verdict mail: FROM coagent@ TO wednesday-agent@, subject `[QA -> Wednesday] GATE53 #1369 (Seat B54 author and merger, round 53; T1 dependency resolution: a scoped @prisma/dev override, one nested lock entry pruned, the frvp baseline row removed)`.

**END_TREE `d0f0389e191820ff3dc2d9c98d9d661336eb90e3` == the seat's PREDICTED tree** (`3 files changed, 3 insertions(+), 18 deletions(-)`). end_tree_crosscheck_1.out (`ENDTREE AGREE`) reads it four ways: pin (F) merge-tree + commit-tree; the head's own tree (parent == develop); GitHub's `refs/pull/1369/merge` (`9506173ee7d7`, parents develop + head); and the head's diff applied `--cached` onto develop under a temp index (no merge-tree). The control that differs is develop's own tree `48f5f8afa6ef` (= gate52's END_TREE_B, as it should be). pin (F) and fill both REFUSE if END_TREE ever leaves the prediction.

**Drafter predictions (the gate re-derives each one):**
- **pin_1.out `PASS`:** exactly the 3 allowed paths, numstat per path +3/-0, 0/-11, 0/-7; all 100644 (control `scripts/run-migrations.sh` 100755); pre-push hook and preflight identical in every tree; **11 unchanged pins byte-equal**: audit-gate.mjs, audit-locks.mjs, baseline-contract.mjs (`ef82d7c5211d`), baseline-contract.test.mjs (`2379c0aeee6e`), expected-case-count, lock-discovery.mjs, originate's package.json / STANDALONE lock (`3e088e4e1855`) / Dockerfile, mcp-server's lock (`ec20749768f0`), the prisma schema.
- **lockdiff_1.out `LOCKDIFF PASS: 0 FAIL of 11 checks`:** root lock 1968 -> 1967, ADDED 0 / REMOVED 1 (`node_modules/@prisma/dev/node_modules/@hono/node-server`, was 1.19.11) / CHANGED 0 / flag flips 0; `@prisma/dev` 0.24.3 value-equal AND raw-block byte-identical (771 bytes), its own `dependencies` still `"1.19.11"`; hoisted 1.19.17 unchanged; the lock's text diff == base with EXACTLY that member's 11 lines cut; 45 locks, only the root differs; manifest: only `overrides` gains `{"@prisma/dev": {"@hono/node-server": "^1.19.15"}}`, no top-level child override, +3 insert-only; baseline: removed exactly {frvp}, head == base with exactly that member cut, 24 surviving rows 0 changed by value / 0 by raw bytes, dated 7 -> 6, cohort 2026-10-09 {337j, frvp, wrjc} -> {337j, wrjc}; **substring trap**: frvp still occurs at head lines 90 and 97 (react-router reasons) with key count 0.
- **auditset_1.out `AUDITSET PASS: 0 FAIL of 4 checks`** (live `npm audit --json --package-lock-only`, host npm 11.5.1, 14:38:36Z; reports saved as npm_audit_base_1.json / npm_audit_head_1.json): BASE 11 reported / 25 baselined / CLEANUP 14 / rc 0; HEAD 9 / 24 / CLEANUP 15 / rc 0, frvp in neither set, CLEANUP newly names GHSA-92pp; **RED (develop's tree + the head's baseline) rc 1, fresh == [frvp]**; **11 -> 9 = exactly {GHSA-frvp-7c67-39w9, GHSA-92pp-h63x-v22m}, both carried ONLY by the pruned nested node, 0 newly reported.**
- **registry_1.out `REGISTRY PASS: 0 FAIL of 4 checks`:** 16 stable 2.x published (2.0.0 .. 2.1.3, `latest` 2.1.3); `^1.19.15` -> 1.19.17 (set {1.19.15, 1.19.17}); `>=1.19.15` -> 2.1.3; the lock's hoisted integrity + resolved == the registry's dist for 1.19.17 (control: 1.19.11's integrity differs).
- **images_1.out `IMAGES PASS: 37 Dockerfiles, 0 image(s) copy the root lock, 0 unresolved, control FIRED`:** 35 inside Blockchain/Dev + Tokenomics + k6; 14 compose files parsed (compose `!reset` tags read as null), 34 Dockerfile builds resolved; 80 per-directory manifest COPY sources; the one context-root copy (`Tokenomics/Dockerfile:4 COPY .`) builds with context `Tokenomics`; control `services/originate/Dockerfile:28` found; originate's prisma lines `:35 COPY prisma/ ./prisma/`, `:38 RUN npx prisma generate`.
- **keyscan_1.out `KEYSCAN PASS: 10 checks over 1 PRs, 0 FAIL (trailer control FIRED)`:** subject {KS-530}, lands 91; `Refs KS-530` once; no foreign hyphenated key on title / body / commit / branch; commit trailers empty; M1 method phrases present; control `bf277eead268` 53-byte trailer.
- **gh_read_1.out:** 21 other open PRs; **12 touch a kit path** (all on the root lock and/or root package.json): #1360 (PeterObeden, client human), #920 (kksecura, package.json) and Dependabot #949 #948 #947 #946 #945 #649 #639 #635 #575 #572. **All 12 are recorded in kit.json `reported_overlaps`** (REPORTED, never sequenced; a rebase they may need is not ours). A NEW overlap at launch refuses rc 15.

## 2. What the gate must rule

The prompt names each item, and the launcher refuses a prompt that is missing any of the 35 keywords (each as a token).
1. **NO-COLLATERAL, PRISMA-DEV-BYTE-EQUAL, OTHER-LOCKS-UNTOUCHED** (planted version + flag-flip controls).
2. **NPM-CI-HEAD, LOCK-IDEMPOTENT, INDEPENDENT-RESOLVE, COUNTERFACTUAL** (node:24-alpine / npm 11.19.0, with a control that npm RAN and CAN WRITE; the busybox-grep trap named).
3. **EXTERNAL-NOT-BUNDLED, RESOLVES-HOISTED, PRISMA-RUNS** (main entry + walk up; ERR_PACKAGE_PATH_NOT_EXPORTED named; `prisma generate` as the Dockerfile runs it; no server).
4. **CARET-NOT-GTE.**
5. **RED-FIRST, AUDIT-LEGS, REPORTED-11-TO-9, CLEANUP-VERBATIM, ROW-KEYSET, COHORT-TWO** (red-first via `AUDIT_BASELINE_PATH`, which audit-gate.mjs reads at :46).
6. **NO-IMAGE-READS-ROOT-LOCK.** 7. **SUITES-0-NEW-REDS, TSC-NO-REGRESSION.**
8. **KEYSCAN-OWN-KEY, NO-CLOSING-KEYWORD, METHOD-STATED, NO-TRAILER, SUBJECT-LANDS-AT, SUBJECT-TRUE-OF-DIFF, PR-BODY-CLAIMS.**
9. **COLLISION-CENSUS, NOT-TESTED-LIST.** 10. **CLEAN-MERGE, END-TREE, MODES.** Plus TIERING, DISK-ENOSPC, REPORT-HASH-LAST.

**Doubts the drafter found (all are in the prompt for the GATE to rule; the drafter rules none):**
- (a) **The 11 -> 9 is frvp ITSELF plus GHSA-92pp, not "two other advisories".** Measured (auditset A4): both were carried only by the pruned nested 1.19.11 node (92pp's range is <1.19.13), nothing else left or entered the reported set. The commission's framing ("two OTHER") looks wrong by one; the prompt asks the gate to say so and to make any third mover a Major.
- (b) **The three Prisma commands may never load `@hono/node-server`.** The seat's own commit message and PR body say the import is `await import("@hono/node-server")`, a DYNAMIC import inside the dev-server path (`startPrismaDevServer`). `prisma --version`, `prisma generate` and `prisma dev --help` can all pass with the module never loaded. The decisive runtime proof is then the resolution from `@prisma/dev`'s directory; the prompt asks the gate to instrument which command (if any) loads it.
- (c) **The pruned lock still records `@prisma/dev`'s `dependencies["@hono/node-server"] = "1.19.11"` while the installed copy is 1.19.17.** The gate runs `npm ls @hono/node-server --all` and rules `overridden` (expected) vs `invalid` / ELSPROBLEMS.
- (d) **PR body: "Over all 35 tracked Dockerfiles"** — the repo tracks 37 (35 under Blockchain/Dev, plus Tokenomics and systemTest k6). Counting scope, likely polish.
- (e) **PR body: "`Dockerfile:36` copies from the project root"** — the `COPY prisma/ ./prisma/` is at **:35** (:36 is blank). Polish.
- (f) **Method statement (condition 1).** The body says "npm did not produce this edit unaided" and "removed by hand", but also titles the section "How the lock was regenerated" and says "Two things corroborate that the result is a real re-resolution rather than a hand-authored lock". The gate rules whether that suggests otherwise.
- (g) **Line numbers in the commission.** frvp's substring hits at ":97/:104" are the BASE's lines; at the head they are **:90 and :97**.
- (h) **#949 (Dependabot, prisma 7.8.0 -> 7.10.0 in the root)** is the "alternative not taken" and touches the root lock. If it lands later, `@prisma/dev` 0.24.17 drops `@hono/node-server`, so the override becomes inert but harmless; it will need a rebase. Report only.
- (i) **npm audit's `fixAvailable` for `prisma` / `@prisma/dev` flips from `true` to `{prisma 6.12.0, isSemVerMajor}` at the head.** An `npm audit fix --force` would DOWNGRADE prisma. Information, not this PR's defect.
- (j) The trailer control reads 53 bytes of trailer line; the READY's "55 bytes" is the same trailer with `%(trailers)`' newlines. Same fact.
- (k) The advisory database is live: the drafter's 11 / 9 readings are at 14:38Z on host npm 11.5.1, lock-only; the gate's leg 6 runs over an installed tree with its own npm.
- (l) **NOT the gate's (Wednesday rules them):** KS-530's updatedAt moved on PR creation (state unchanged); `mergeable_state: unstable` (cause unreadable); the GHSA-92pp row's cleanup (it would edit GRANDFATHERED_NO_EXPIRY); the react-router rows still expiring 2026-10-09; the usage quota (Kam's grant).

## 3. Pins and what the gate owes
- `fill_gate53.py` FILLS the prompt `2026-10-02_secuura-batch1369.prompt.txt`, the launcher `launch_qa_secuura_batch1369.sh` and COMMISSION.md (fill_1.out rc 0). It refuses unless:
  - gate52's report still hashes to `908e955fbbcb…`;
  - END_TREE == kit.json `end_tree_predicted` (the seat's prediction);
  - `end_tree_crosscheck_1.out` carries END_TREE on all four instrument lines and ends `ENDTREE AGREE`;
  - lockdiff / auditset / registry / images / keyscan / gh_read each end in their PASS / OK line, at this develop and head.
- The launcher's exits are re-keyed from gate51a's / gate52's: **8** also requires the method + Q5 rulings and the seat's brief (in `fleet/briefs_staged/`) named; **34** is the NO-SERVER rule (no prisma dev server, no database); **35** (new) is the 11 -> 9 rule; **36** is the REAL-FIX rule (false fix = blocker, bundled?, ERR_PACKAGE_PATH_NOT_EXPORTED, never from memory); **37** adds the GHSA-92pp cleanup as not this PR's; **38** requires the usage figure (95%) and Kam's grant; **39** allows an image build ONLY if requirement 6 names one.
- Named exceptions: X1 (npm registry reads of `npm ci`, `npm install --package-lock-only`, `npm view`, `npm audit`; pulling node:24-alpine), X5 (≤1 read-only Linear query: KS-530), X6 (read-only GitHub GETs).
- `reported_overlaps` holds the 12 census hits (above); `sequenced_out_of_kit` is EMPTY.

## 4. Routing line — NOT added
Back up the file first (`inbox_routing.conf.pre-<date>`). Then add this ONE line to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/inbox_routing.conf`:
```
QA/Secuura-batch1369|coagent@agentmail.to|yes
```
Until that line is present, step 0 of the launch action refuses with rc 1 (control R1). R8 shows a routed temp file passing step 0 and stopping after 3b.

## 5. Controls: `controls_gate53.sh <scratchpad> [--invert]`
- **141 controls, one unedited script**: `controls_gate53.sh`, sha256 `c74633d2bf1a…`. controls_sha.txt shows it identical before and after both runs (run 1 15:03:51Z – 15:12:25Z, run 2 15:12:25Z – 15:23:01Z); both .err files are empty.
  - Normal run (controls_1.out): **rc 0, `141 controls, OK 141, MISMATCH 0 | ssh-denied retries 0`**.
  - `--invert` run (controls_2.out): **rc 1, `141 controls, OK 0, MISMATCH 141 | ssh-denied retries 0`**.
- Both runs wrote to the scratchpad first and were then copied in, byte-checked with `cmp`.
- **A superseded first run is kept, not deleted:** controls_0_superseded.out (14:50:16Z – 15:02:55Z, sha in controls_sha.run0.txt): 140 OK / 1 MISMATCH. The one was **R3w**: the census hit a transient `http.client.RemoteDisconnected` and the launch action correctly FAILED CLOSED (rc 3, "the PULLS API read failed") instead of rc 15. That is the instrument, not the guard: `get()` retried only HTTP 5xx. Fixed in `repin_and_launch_gate53.sh` and `gh_read_gate53.py` (a dropped connection is retried up to 3 times, 10 s apart, with a stderr `RETRY` line), then gh_read, fill, `--check` and BOTH control runs were redone from scratch.
- Side effects, kept: R1 and R8 wrote `launch_<HHMMSS>.*` step outputs here; the PN simulations wrote `pins_gate53.SIM-*.json`.
- **Coverage:**
  - **PN0–PN7** (pin): the real head as a simulation (END == the prediction, shortstat, 4 mode pins, a contract blob BYTE-EQUAL); `--develop` refused without `--simulate`; baseline-contract.mjs edited -> (K); a develop move on the baseline -> (C); the lock recorded 100755 -> MODE MISMATCH; **an unrelated develop move -> END_TREE != the prediction (refused) while (C) reads NONE**; a path outside the 3 -> (B); an extra manifest line -> numstat [4, 0].
  - **LD0–LD9** (lockdiff): the real pair 11/11 (+ the @prisma/dev byte line and the substring-trap line); hono version changed -> changed 1; a `devOptional` -> `dev` -> 1 flip; @prisma/dev's dependency rewritten to the override -> L2; **one trailing space -> L5 fails while L1 (JSON) still passes** (byte vs value); mcp-server's lock touched -> L4; a top-level child override -> M1; wrjc re-dated -> B3; **one em-dash re-escaped to `—` in a surviving row -> B2 by raw bytes 1 while B1 passes** (the seat's json.dumps trap); develop as head -> L1.
  - **AS0–AS4** (auditset, saved reports): real 11 -> 9 / 25 -> 24 / 14 -> 15 with the 92pp WHY line and RED fresh [frvp]; **the base report as the head's (= an override that changed nothing) -> HEAD FAIL new [frvp]**; a planted extra advisory -> NEWLY reported; `--today 2026-10-09` -> both react-router rows LAPSED; a second row (92pp) removed -> baselined 23.
  - **RG0–RG2** (registry, live): real 4/4; 1.19.11's integrity as the lock's -> R3; `>=1.19.15` as the value -> R2 max 2.x.
  - **IM0–IM2** (images): real; originate :28 rewritten to `COPY package*.json ./` -> HIT at context Blockchain/Dev and the control does not fire; a `COPY package-lock.json` appended to auth's Dockerfile -> 1 HIT.
  - **KS0–KS9** (keyscan): real; (#n) suffix; foreign subject key; 94-char landing; empty body; a closing keyword; a hyphenated KS-528 in the PR body -> L1; a Co-Authored-By commit -> T1; the trailer control pointed at the head -> DID NOT FIRE; the method phrase removed -> M1.
  - **ET0** (endtree 4 of 4).
  - **L0–L24 + LK1–LK35** (launcher): every exit, including 34 (NO-SERVER), 35 (11 -> 9), 36 (REAL-FIX), 37, 38 (95%), 39 (incl. the image hold), the ruling-path refusal (L17) and the filename rule. L9 is the real non-TTY path.
  - **R0–R8** (launch action): census (12 expected overlaps, 1 client-human); routing refusal; **reported_overlaps emptied -> OVERLAP #1360 rc 15**; a title key -> OVERLAP #995; sequenced right / wrong head; **an expected overlap at a moved head -> reported HEAD MOVED, rc 0**; DISJOINT; wrong head rc 11; old develop rc 10; bad scratchpad rc 9; routed stop-after-3b.
  - **PNZ / KJZ / PRZ**: the pins, kit.json and the filled prompt are unchanged.
- **Not controlled:** on a real launch, the usage gate (12), `cockpit.sh add` (14) and the override refusal (16); a `mergeable=False` refusal; a real re-pin across a develop move (only the dry run's rc 10 and PN5's refusal are controlled); a live `npm audit` inside a control (AS* use the saved reports). gh_read and fill are exercised by their real runs, not by plants.

## 6. Could not measure (the drafter)
- No `npm ci`, container, suite, tsc, prisma command, bundling read or resolution ran. Requirements 2, 3, 7 and the live legs of 5 are entirely the gate's; the seat's figures are claims until the gate runs them.
- The leg-6 prediction is lock-only on host npm 11.5.1 against a live advisory database.
- The image reading is static; nothing was built. Linear was not read.

## 7. Files
- **Config:** kit.json (written by the drafter's `g53_sp/mkkit.py`, which fills `reported_overlaps` from gh_read_1.json) · COMMISSION.TEMPLATE.md -> COMMISSION.md · README.md (this file) · READY_1369_mail.md (Wednesday's; unchanged).
- **Pin:** pin_gate53.py -> pin_1.out, pins_gate53.json (+ `pins_gate53.SIM-*.json`) · endtree_gate53.py -> end_tree_crosscheck_1.out.
- **Instruments:** lockdiff_gate53.py -> lockdiff_1.out; auditset_gate53.py -> auditset_1.out (+ npm_audit_base_1.json, npm_audit_head_1.json); registry_gate53.py -> registry_1.out; images_gate53.py -> images_1.out; gh_read_gate53.py -> gh_read_1.out / gh_read_1.json / gh_body_1369.md; keyscan_gate53.py -> keyscan_1.out; each with its .err and .rc.
- **Prompt and launcher:** prompt_gate53.TEMPLATE.txt + launcher_gate53.TEMPLATE.sh.txt, filled by fill_gate53.py (fill_1.out) -> `2026-10-02_secuura-batch1369.prompt.txt`, `launch_qa_secuura_batch1369.sh` and COMMISSION.md. Checks: launcher_check_1.out (before the controls) and launcher_check_2.out (after).
- **Launch:** repin_and_launch_gate53.sh -> repin_dryrun_0_before_controls.out, repin_dryrun_1.out.
- **Controls:** controls_gate53.sh -> controls_1.out / controls_2.out (+ .err, .rc), controls_sha.txt; the superseded run controls_0_superseded.* + controls_sha.run0.txt.
- **Provenance:** pin is a NEW COPY of gate51a's (one PR); gh_read, keyscan and repin are NEW COPIES of gate52's, re-keyed by hand; lockdiff, auditset, registry, images, endtree, fill, the templates and the controls are new for a lock + baseline PR; gate51a's and gate52's kits are untouched.

## 8. Re-draft recipe (a new head on #1369, or ANY develop move)
**Any develop move changes END_TREE, so pin (F) refuses until kit.json `end_tree_predicted` is re-set** (the launch action's step 3b therefore refuses rc 10 on a move; control PN5). A move is a re-draft, with a new prediction from the seat or the drafter.
1. Keep kit.json as `kit.json.pinned-ce051988`.
2. Set `prs.1369.head` (and, on a move, `expected_develop`, `prs.1369.expected_parent_any` and `end_tree_predicted`); re-check `expect_counts` against the new base.
3. Run, in order: `pin_gate53.py <sp>` -> `gh_read_gate53.py` (then re-run `g53_sp/mkkit.py` if the census changed, and re-pin) -> `lockdiff_gate53.py <sp>` -> `auditset_gate53.py <sp>` (live; copy its two reports in as npm_audit_{base,head}_1.json) -> `registry_gate53.py <sp>` -> `images_gate53.py <sp>` -> `keyscan_gate53.py <sp>` -> `endtree_gate53.py <sp>`.
4. Run `fill_gate53.py`.
5. Run the controls both ways. Update the head-specific patterns first: PN0k's blob, LD0s's line numbers, the AS0 counts, IM0's Dockerfile count.
6. Run `--check`, then the dry run.

## 9. The ONE launch command (run it after the routing line in section 4 is added)
While Kam's 17:40:22 grant holds (until his account switch, Fri 2026-10-02 morning):
```
WED_USAGE_STOP=100 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-02_gate53/repin_and_launch_gate53.sh /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/gatesets/2026-10-02_gate53/launch_qa_secuura_batch1369.sh /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/79817561-2a8e-42cd-8745-2ef3ab0b0516/scratchpad
```
After the switch, the same command WITHOUT `WED_USAGE_STOP=100`: the new account's gauge decides, and the usage gate's refusal (rc 12) is then final.
- Append `--dry-run` for a dry run.
- Argument 2 may be ANY existing Claude session scratchpad. If `g53_sp/clone` is absent there, pin_gate53.py rebuilds it from the checkout on a re-pin.
- After the gate's verdict and a GO, the squash key set is exactly {KS-530}. Wednesday still owns KS-530's state, the GHSA-92pp cleanup and the react-router fuse.
