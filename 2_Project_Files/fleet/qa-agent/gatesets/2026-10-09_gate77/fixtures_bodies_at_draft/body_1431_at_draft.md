Refs KS-1355
https://linear.app/secuura/issue/KS-1355

Raised from a Wednesday-held Spark pass, re-proved by Seat F 5th on develop `0a6177ea5482`.

## What this does

`stack_guard.sh` grouped foreign stacks by `(project, owner)`, so a project whose containers carried *different* owner labels was listed **once per owner** — an operator could not tell one project from two. It now prints **one line per project**. Where some containers carry a real owner and others carry `owner=unknown`, the line names the **real** owner and appends the unknown count.

## Behaviour change, stated plainly

A project with **two DIFFERENT real owners** now prints **ONE** line — the first `(project, owner)` tuple in `docker ps` order — where the tip printed both. **The second real owner is no longer shown.** That is a deliberate consequence of one-line-per-project, not an oversight.

The `(+N container(s) with owner unknown)` wording is **this change's own choice**; the ticket asks only that an unknown count be appended.

**NARROWING: this is KS-1355 spot 1 only. The ticket does NOT close** — the stack tooling's other non-slot-derived spots are untouched, as is the REVIEW-held `dev-reload.sh` work.

## Test Evidence

**Touched:** `Blockchain/Dev/scripts/stack_guard.sh` · `Blockchain/Dev/scripts/__tests__/stack_guard.test.sh` · `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` (flow block `42.`) · `Projects Documents/QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` (cheat section `KS-1355`).

**Ran** — `/bin/bash scripts/__tests__/stack_guard.test.sh` from `Blockchain/Dev`, in this PR's worktree:

| run | result | rc |
|---|---|---|
| **RED** — new suite, `stack_guard.sh` reverted to the base | **25 passed, 2 failed** | 1 |
| **GREEN** — as shipped | **27 passed, 0 failed** | 0 |

The red is a **product red, not a tamper**: the two failures are exactly the new cells — `a stack with an owner=unknown container is listed ONCE` (`want "1", got "2"`) and `...under its real owner, with the owner=unknown count` (`want "1", got "0"`). The suite's own **`KS-1355 CONTROL`** cell (an all-unknown stack is still listed once) **passes at the base as well**, so the suite is not failing wholesale.

`bash -n` clean on both files. Toolchain read from this worktree: bash **3.2.57(1)-release**, node **v24.7.0**, npm **11.5.1**.

**The exec bit — worth knowing if you re-apply this patch yourself.** Both scripts are **100755** in the tree. This repo sets `core.filemode=false`, so `git apply` leaves them **644 on disk** while git records **no mode change at all**. The mode here was restored by reading it back from the **index** for those two named paths only (never `checkout-index -a -f`). `git ls-tree HEAD` reads **100755** for both and `git diff --summary` is empty, so no mode change is in this commit.

**A +/- reconciliation:** `git apply --numstat` on the source patch reads **+35/-1** for the suite; the applied tree reads **+34/-0**, because the patch's single deletion is an empty line the same hunk re-adds. Both are correct — one measures the patch, the other the result. All added content lines are identical between the two.

**Gates:** `docblockra3` 0 failed (flow 30 → 31 blocks, tail `26.` → `42.`; cheat 19 → 20, tail `KS 1164` → `KS-1355`; byte-for-byte the only change from the base blob, with a 1-byte-altered fragment failing the same comparison). Path gate PASS with **3/3 controls correctly failing**. Commit carries **0 `Co-Authored-By`** trailers, against a control commit that does carry one. No per-slot literal in either file.

**Preflight on this push:** `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` **This push's own output does not name WHICH three legs skipped**, so they are recorded as *3 SKIPPED, unnamed by this push's output* rather than attributed to leg numbers. `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`; `OK — 13 code guards passed.`

**NOT run:**
- **Live run owed.** The two-owner case is proved against the suite's fixtures, **not against a live Docker host** — no stack was brought up. A runtime-behaviour change is not done on offline green.
- **The four platform suites — Schemathesis, Akto, Playwright, Performance/k6 — are UNMEASURED.** No local stack. Only the SKIP lines this push printed are quoted; none is a pass.
- KS-1355's other spots were not touched or tested.

**Migrations + config:** none. No dependency, lockfile, manifest, baseline or spec-version change. No `.env`.

## Notes for review

- The ticket does **not** move to Done: narrowing fix, and a live run is still owed.
- Flow block `42.` is cut from the raise base, as are this round's other PRs, so a keep-both merge-in on the two platform documents is expected at merge time and is not a conflict in the usual sense.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
