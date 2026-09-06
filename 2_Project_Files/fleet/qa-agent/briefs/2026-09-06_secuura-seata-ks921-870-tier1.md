# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), SEAT A: PR #870 (KS-921)

**Charter first, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.
Findings only. You never fix, never file a ticket, never touch a builder's tree.

**TARGET — PR #870, KS-921. TIER 1.** head `191bc1cc907d8eeb7a2aef4b86e4e2a50f6bd326`, cut on
`develop a821bd0aad137347954a287707e573e417e8ce9d`.

**Why tier 1 for a shell script:** this guard is wired as **preflight leg 13 and now blocks every
push on this repository**. Its failure mode is a **false CLEAN** — the class where a green suite
proves the least — and a false BLOCK stops every author. Both directions matter here.

## 2. Spec / DoD
PR #851 broke three runtime images at once because a convention (re-link `/shared` after the runtime
stage writes `node_modules`) was enforced by nothing. This guard makes it structural. The DoD I set:
**each clause red-proofed INDEPENDENTLY** — no fixture tripping more than one — the second clause
**report-only** until it is green across the class, and the derived count derived by a parser rather
than by `git grep -c`, which counts comments.

## 3. Scope — claims to measure. Each is a CLAIM UNDER TEST.
1. **The two independent red-proofs.** Builder's table: the real tree at `d602a1536` reds clause A on
   exactly `nft-certificate`, `referral`, `staking` with `governance` GREEN and **clause B silent (0
   dev-tree findings)**; `develop`'s governance minus its one `npm prune --omit=dev` reds **clause B
   alone** with A green. Re-derive both. **Confirm no fixture trips both clauses** — that is the
   condition, and a bundled fixture would measure the pair and prove nothing about the parts.
2. **The discriminator.** The suite is said to assert NAMED services and COUNTS, not exit codes, and
   to carry `governance` as the case that must stay green. **A fixture that reds everything proves
   nothing** — verify the suite would notice an over-firing guard.
3. **HUNT — the FALSE BLOCK direction, which nobody has driven.** Name the assertion first. Construct
   Dockerfile shapes that are LEGITIMATE and must stay green: a multi-stage file with no runtime
   `node_modules` write at all; a stage that writes `node_modules` and is never the final stage; a
   `COPY` of a *subdirectory* (`node_modules/.prisma` — the builder found this exact case in its own
   first draft, where a partial restore read as a whole-tree write and produced a finding against
   `originate` that was **not real**); comments and line continuations around the instructions;
   heredocs. Every false positive here costs every author on every push.
4. **HUNT — the empty-corpus path.** The builder's second draft bug: `grep -l P $(find …)` with no
   file operands reads **STDIN**, and the pre-push hook's stdin is git's ref list, so that shape
   **hangs a push** rather than failing it. It says the case is now asserted **on TIME**, because the
   blocking form still exits 1 once stdin closes and an exit-code-only case passes against the bug.
   **Verify the timing assertion is real and that it would catch a reintroduction** — this is the
   highest-value cell in the suite and the one most likely to be quietly weakened later.
5. **The derived count.** Instrument claimed: whole-line comments stripped, continuations joined,
   installs counted only on `RUN`. It derives **4 files copy a builder's `node_modules`, 21
   re-install their own**, and says that independently reproduces KS-490's own "found FOUR". Check
   the parser against the tree, and check its edges (a `RUN` inside a heredoc; an install in a
   comment; `--mount` syntax).
6. **The class is 25, not 24.** `connectors/whatsapp-bot` is not under `services/`, so a
   `services/*` glob misses it. Confirm the guard's corpus is the 25 and not a `services/` glob.
7. **Report-only means report-only.** Clause B must not block today, and must block under
   `SHARED_RELINK_STRICT=1`. Drive both.
8. **The fixture fix, not a guard fix.** `preflight_deps.test.sh` broke because its fixture runs the
   whole preflight in a bare tree; the builder fixed the FIXTURE and says the suite's case count is
   unchanged at 36 with the failing case now passing. **Verify the guard was not weakened to make a
   test pass** — that is the specific thing to check, and the builder named it itself.
9. **Leg 13 is really in the path.** The builder reports a full 13-leg preflight PASSED in the hook on
   this commit. Verify the leg runs, prints its own line, and that a deliberately failing corpus
   makes the PUSH fail — a leg that cannot block is decoration.
10. **Merge-tree against the `develop` you read AT THE TIME, in YOUR OWN copy.** Develop moves —
    seat B is live. I ran none; nothing here is predicted.
11. **Secret gate:** no canary exists in the repo. Build a fabricated pair, prove it FIRES in the
    same scan mode, quarantine by rename, then scan the real range.

## 4. Credentials
Pointer only: the project's own `4_Credentials/.env`. You should need none.

## 5. State-mutation & cleanup
Your own `mktemp` checkout with its own index. **Never touch seat A's tree (`2_Project_Files`) or
seat B's worktree (`worktrees/seat-b`)** — both are live, and seat A's checkout carries an unrelated
branch. Never the demo VM, the shared local stack, or Docker. **No prune, and build no containers.**
Restore any tamper by inverse edit, proven by sha256. Quarantine by rename, never delete. Report the
LISTEN set before and after.

## 6. Output boundary
Findings only, one verdict, evidence class on every finding that recommends an action, NOT-TESTED at
the same prominence as the findings.

## 7. Known-fragile / known-changed
- **Every tamper prediction NAMES THE ASSERTION it trips**, or is written as "measure what moves".
  Hold me to it.
- **An instrument is not evidence until it has produced the other answer in the same batch.** Three
  instruments failed silently on this project today: `rm -f` exiting 0 on a non-existent path, a
  `grep` whose unquoted variable did not word-split under zsh (with stderr discarded, so every row
  read clean and wrong), and an exit-status printed where a count was implied.
- **A control that mutates its subject is not a control** — `git show`, never `git checkout`, in a
  tree another seat is holding.
- **The builder itself is not claiming the images still build** — no container was built, and that is
  stated deliberately rather than omitted. Do not treat that as a gap you must close; treat it as the
  boundary of the claim.
- `git grep -a` / `git diff -a`. `core.fileMode` is false here, so modes are index facts. `env bash`
  is 3.2; `/bin/dash` is present; Docker here is linux/arm64.

## 8. Logistics
Report to `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] Secuura SEAT A KS-921 (#870)`,
verdict in the first line. Report path under the QA project's own `projects/secuura/reports/`.
Budget ~35 minutes.

PROVENANCE:
- the head, its base, the two red-proof fixtures, the derived counts, the 25-vs-24 drift, the preflight 13/13 and the suite figures | the builder's READY mail 2026-09-06T11:11:33Z, read whole | read 2026-09-06 21:1x
- the DoD conditions (independent red-proofs, report-only, parser-derived count) | Wednesday's ANSWER to the builder 2026-09-06 20:50, sent through the gate | read 2026-09-06 20:50
- the two draft bugs (the `.prisma` partial-restore false finding; the empty-corpus STDIN read) and the fixture-not-guard fix | the same READY mail, read whole | read 2026-09-06 21:1x
- develop a821bd0aa | `git -C worktrees/seat-b ls-remote` (READ verbs only; no fetch, no merge-tree, no worktree add in either seat's checkout) | read 2026-09-06 20:4x
- NOT READ by me: the #870 diff itself — I have read only the builder's description of it | not read | read 2026-09-06
