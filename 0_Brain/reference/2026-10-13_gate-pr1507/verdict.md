# QA gate: Secuura Platform K PR #1507 (KS-1090, leg 16 also gates services/api-gateway)

- Head: `54bc137c2d880a78f39c5f8c516077b0eea2e9b6`. `git bundle verify` says "okay", the bundle requires `cc2939bbf3521c5f6d8789befc04deda83f44cdf`, and its single ref is `refs/heads/feature/ks-1090-leg-16-gates-the-api-gateway-test-file-ratchet` = 54bc137c. `ls-remote origin` shows the same SHA on that branch. Bundle sha256/16 `261bfea977841d18`.
- Base named: develop `cc2939bbf352`, one commit below the head (`git log cc2939bb..head1507` = 54bc137c2 only).
- Real develop tip: `88c348375bd3083e0d9bef191f610ca9289c59ab` (`git ls-remote origin refs/heads/develop`, read at gate time). It is one commit past the base (KS-1185, #1505: `verification.ts` plus one new gateway test, +155/-2) and has not moved further.
- How I got the tree: a `--no-hardlinks` clone of an earlier gate's scratch repo (it holds cc2939bb), then `git fetch <bundle>` and a read-only `git fetch origin develop`, all inside my scratchpad `g1507/`. Worktrees: `head` (54bc137c), `dev` (88c34837) and `merged` (`m1507` = develop + head, commit 5a00cb9fb). Nothing was written under `!CODING`: there I used only reads plus the deploy key for a read-only fetch. The clone has no install, so in each worktree I built a node_modules shell of symlinks to the project's installed deps, re-pointed `@secuura/*` at the worktree, and built `packages/shared` in the worktree (`npx tsc` rc 0). This is the same harness as the #1505 and #1506 gates. Node v24.7.0.
- Tier: Opus, independent, 2026-10-13.

## VERDICT: GO WITH NOTE

The one-line default change does what it claims. On the real tree, the unchanged leg accepts a TS2322 planted in a gateway test (rc 0, "1 service(s)") and the new leg refuses it (rc 1, names the file and the code). Every gateway failure mode I built fails closed, and an auth failure does not hide the gateway's result.
There are no Majors. The notes: the suite proves the gateway is listed but not that a gateway failure fails the default run; the push costs about +5.4 s, not +3 s; and #1507 conflicts textually with #1506 in CLAUDE.md. KS-1517: accept as is (reasons below).

## By my runs

**1. Provenance and merge.**
- `git diff --stat cc2939bb head1507`: 3 files, +12/-6. That is the leg suite +7/-2, `test-types-ratchet.sh` +3/-3 and `CLAUDE.md` +2/-1, as claimed.
- Applying `pr1507_full.diff` (`git apply --index`) to a pristine cc2939bb gives `applied tree: f26edfd76ddb666576e4e40841ed70e9be49170b`, which equals `head1507^{tree}`. The patch also equals the commit's diff once `index` lines are stripped (SAME-DIFF).
- `git merge-tree --write-tree dev head1507` gives `ec5badba2f1b440461889fcdfea385df28a77650`, the builder's predicted tree. A real merge in the `merged` worktree gives the same tree, ec5badba2f1b.
- `git diff --stat dev merged`: the same 3 files, +12/-6. The develop delta touches only `services/api-gateway/src/routes/verification.ts` and one new gateway test, so the two are disjoint.

**2. The change itself** (`Blockchain/Dev/scripts/preflight/test-types-ratchet.sh` on the merged tree).
- The change is line 45 `set -- services/auth services/api-gateway` (applied only when `$# -eq 0`), plus the matching header (l.19) and usage line (l.36).
- One loop (l.56-68) runs `check.cjs "$svc"` for each argument and never breaks, so every service runs. Any non-zero rc increments `failed`, and the leg exits 1 if `failed != 0` (l.70-75). The `OK — $# service(s)` line (l.77) counts the arguments, so it now reads 2.
- The install precondition (l.49) runs once, before the loop, and is not per-service.
- `preflight.sh:682-692` calls the script with no arguments through `run_delegated`, so the default list is exactly what the hook runs. `TOTAL_LEGS` and the `16/16` header are unchanged (suite cells "TOTAL_LEGS is 16" and "every step header's denominator" pass).
- Edge cases, each run on the merged tree with the default list and restored after (sha256/16 of the baseline `bd23c39ea5c54eec` and of the gateway tsconfig.test.json `67af4295dc60f1a6`, the same before and after; `git status`: no tracked change):

  | case | gateway checker | leg |
  |---|---|---|
  | E1 gateway baseline absent | rc 1, "35 errors: 0 in the baseline, 35 new" | rc 1 FAIL — services/api-gateway |
  | E2 gateway baseline empty (0 bytes) | rc 1, the same 35 new | rc 1 |
  | E3 gateway baseline malformed | rc 2 `baseline-api-gateway.txt:18: not "<file> <TSxxxx> <count>"` | rc 1, "exited 2: the check could not run" |
  | E4 gateway tsconfig.test.json absent | rc 2 `no tsconfig.test.json in …/services/api-gateway` | rc 1 |
  | E5 auth checker rc 2 (auth baseline malformed), gateway clean | the gateway STILL runs: "35 in the baseline, 0 new" | rc 1, FAIL names services/auth only |
  | E6 `services/api-gateway/` (trailing slash) as an argument | the same line as without the slash (realpath plus basename) | rc 0 |

  Every one fails closed, and order does not short-circuit. The `missing directory` case is covered by the existing suite cell "a service directory that does not exist FAILS the leg" (it passes).

**3. The hole on the real tree** (`hole.sh`, planted in `services/api-gateway/src/__tests__/ks1469-front-door-trailing-slash-and-v1-alias.test.ts`, sha256/16 `ba55cf0b2ae4bd58` before and after each run):
- Unchanged leg (develop worktree): auth only, "OK — 1 service(s) type-check against their baseline.", **rc=0**. The push would be accepted.
- New leg (merged): `src/__tests__/ks1469-…test.ts(274,14): TS2322: Type 'string' is not assignable to type 'number'.` and "FAIL — services/api-gateway … exited 1", **rc=1**.
- Planted in BOTH auth (`auth.integration.test.ts(1637,14)`) and the gateway: both are named, with two FAIL lines and rc 1. An auth failure does not hide the gateway.

**4. The suite** `scripts/__tests__/preflight_test_types_ratchet_leg.test.sh`:
- Head worktree: **26 passed, 0 failed**. Merged: **26/0**. Develop's own suite on develop: 23/0.
- Head suite against the UNCHANGED script (`LEG_SH=` develop's script): **22 passed, 4 failed**, each for the right reason: got "yes no", "1", "1" and "no" (gateway line missing, checker ran once, one "0 new; 0 stale", no "2 service(s)").
- Tampers (`tamper.sh`, a copy at `scripts/preflight/zz-tamper.sh` passed in via `LEG_SH` and removed after; product script sha256 `e9dd501a…` the same before and after):
  - CONTROL (a no-op edit): 26/0.
  - Builder's four, all reproduced EXACTLY:
    - B1 auth only: 22/4.
    - B2 gateway only: 22/4.
    - B3 duplicate third entry: 23/3 (exactly-twice, both-0-new and verdict cells).
    - B4 path typo `api-gatewya`: 21/5 (adds "committed tree passes rc 0").
  - Mine:
    - G1 trailing slash `services/api-gateway/`: 26/0. This is an EQUIVALENT mutant: E6 shows the output is identical, so this is correct.
    - G2 order swapped: 26/0, also EQUIVALENT (each service runs independently, shown by E5).
    - G3 list read from env, `${PREFLIGHT_TT_SERVICES:-services/auth services/api-gateway}`: **26/0, escapes**. The tamper is live: with the variable set to `services/auth` the leg prints "OK — 1 service(s)", so the gateway gate is dropped from the environment. Pre-existing: the same tamper on develop's script passes develop's suite 23/0.
    - G4 gateway rc ignored by name (`[ "${svc##*/}" != api-gateway ]`): **26/0, escapes**.
    - G5 gateway added only if its baseline is non-empty: **26/0, escapes**.
    - G6 gateway run outside the loop with `|| true`: 25/1, caught by the verdict cell.
    - G7 gateway rc 2 tolerated by name: **26/0, escapes**.
- The two suites repaired when leg 16 was added, on the merged tree: `preflight_deps` 56/0 and `preflight_leg4_sweep_not_run` 5/0. Ratio suites: `failure_verdict_keeps_ratio` 8/0, `ratio_excludes_leg1_no_install` 6/0, `verdict_names_real_failures` 5/0, `state_is_initialised` 5/0. `run-shell-suites.sh --check-unreached`: "all 83 tracked shell suite(s) are reached".

**5. Blast radius** (`git grep` on the merged tree; the positive controls are the hits listed):
- The only consumer of the default list is `preflight.sh:690` (`run_delegated bash scripts/preflight/test-types-ratchet.sh`, no arguments).
- `preflight_deps.test.sh:335-338` stubs the script as `exit 0` in its fixture, so it is indifferent to the list (56/0).
- `package.json:44` `check:test-types` already runs auth then api-gateway, unchanged.
- `.githooks/pre-push`, `.github/workflows/*`: zero hits for `test-types` / `typecheck-tests`. Positive control: the same grep run over `Blockchain/Dev` returns 20 hits.
- Zero hits anywhere for a hard-coded `1 service(s)` or for "only services/auth is gated", apart from the line this PR rewrites. The only `[0-9] service(s)` hit is the new suite cell. Positive control: the grep returns `CLAUDE.md:385` and the suite lines.
- The leg count (16) and the hook's ratio line are untouched, so seats will still quote "13/16 legs ran" / "16/16".
- CI: `pr-security-gates.yml:100` and `security-scan.yml:495` run `run-shell-suites.sh` with no `npm ci` (comment at l.85). Those workflows are dormant (Actions retired). Without an install, the four new cells take the `SKIP (advisory)` note branch, so CI would not assert them (Note 3).

**6. KS-1517** (`stale.sh`). I hid the four `packages/shared/dist/documents/defaultDocumentType.*` files that the `./documents/default-type` export points at (`package.json:145`), then restored them. The sorted-hash digest of dist was `459622afabb33c8c` before and after, and the leg was green again after the restore.
- Merged (new leg): gateway "37 errors: 35 in the baseline, 2 new". The two errors are `src/routes/verification.ts(20,39): TS2307: Cannot find module '@secuura/shared/documents/default-type'` and the same at `src/services/enforcement.ts(10,39)`. They are listed as NEW and followed by "Fix the type error in the test file named above". **rc=1.** This matches the builder's and the #1504 gate's reproduction.
- Develop (unchanged leg) under the same stale dist: "OK — 1 service(s)", rc 0.
- Control: under the same stale dist, the gateway's PRODUCT compile `tsc --noEmit -p tsconfig.json` fails rc 2 with the same two TS2307 errors, on both trees. So the tree as built locally really is broken; only the label ("test file") is wrong.
- `deps-present.sh` never mentions `dist` (count 0; control: `tsx` 9). No preflight leg and nothing in `.githooks/pre-push` builds `packages/shared` (`grep -i shared` hits only leg 1's comments and leg 13's relink guard). The only rebuild is the root `postinstall` (`package.json:41`: `npm run build --workspaces --if-present`), i.e. `npm ci`.

**7. Cost** (`time.sh`, merged, warm, 4 runs each):
- The leg alone:
  - auth only: 2.61, 2.62, 2.59, 2.57 s.
  - both services: 5.30, 5.30, 5.33, 5.32 s.
  - gateway only: 2.80, 2.77, 2.73 s.
  - So leg 16 costs **+2.7 s**.
- The leg suite (it runs in leg 14 and calls the leg with the default list):
  - develop: 5.03, 4.90, 4.93 s.
  - merged: 7.79, 7.59, 7.66 s.
  - So leg 14 costs **+2.7 s**.
  - `run-shell-suites.sh` runs suites serially (one background job plus `wait`, l.356-362).
- Net per push: **about +5.4 s**, not +3 s.
- Rebuilding shared (`npx tsc` in packages/shared): 3.60 s.

**8. CLAUDE.md** (+2/-1): "Two services are gated today, `services/auth` and `services/api-gateway` (the leg's default list; `npm run check:test-types` runs the same two)." It is true on the merged tree: script l.45 and `package.json:44`.

## Findings

No Major.

**Minor 1: the suite pins the list but not that a gateway failure fails the default run.** `preflight_test_types_ratchet_leg.test.sh:161-172`.
- The four new cells run the default list only on the clean tree, so any change that RUNS the gateway checker but discounts its result passes 26/0:
  - G4 (rc ignored by service name), G5 (gateway gated only if a baseline exists) and G7 (rc 2 tolerated for the gateway) all escape.
  - G3 (list read from an env variable, the KS-1261 class the header at l.30-32 says cannot happen) also escapes, and so does the same tamper on develop, so it is pre-existing.
- The generic loop cells (l.141-149: error in the first or last service, missing directory) do catch any mutation that is not name-specific. That is why this is Minor, not Major: each escaping mutant needs a deliberately special-cased name or variable.
- A cheap pin, if wanted:
  - one cell that runs the leg with no arguments in a fixture Dev root holding a red `services/api-gateway`;
  - or a grep cell that the script reads no `${…:-` default.
- Not a merge blocker.

**Minor 2: the cost claim undercounts.** The builder says "+3 s per push". Measured: +2.7 s in leg 16 plus +2.7 s in leg 14, because the leg's own suite now type-checks the gateway too (§7). That is about +5.4 s serial, which is consistent with Wednesday's "7.5 s warm" fleet notice. The header line (l.19, "about 2.6 to 3.2 s each") is right per service.

**Note 1: textual conflict with #1506 in CLAUDE.md** (`CLAUDE.md:389`).
- `git merge-tree m1507 pr1506` reports a conflict on CLAUDE.md, confirmed by a trial merge.
- #1506's text says "Leg 16 gates `services/auth` only today; `npm run check:test-types` also runs `services/api-gateway`". If #1506 lands second and its side is taken, the sentence becomes FALSE.
- Whoever merges second must keep #1507's two-services fact AND #1506's fingerprint and floor text.

**Note 2: if #1506 lands first** (trial merge develop + #1507 + #1506 at 767a75dc, CLAUDE.md conflict resolved to #1506's side in scratch only):
- The checker's summary line format is unchanged in #1506 (`check.cjs:205-206`), so the suite's matched strings (`typecheck-tests: api-gateway (`, `0 new; 0 stale baseline entries`, `^typecheck-tests: `, `OK — 2 service(s)`) still hold. The gateway's fingerprinted baseline read 35/35, 0 new, at my (third) path.
- The leg is nonetheless red, rc 1, from #1506's known auth defect (TS1192 fingerprint carries an absolute path; the #1506 NO GO). The suite reads 23/3.
- So #1506's portability fix must now be checked against BOTH baselines, because the gateway is gated. Any future gateway fingerprint that captures a path turns every seat red.
- Nothing in #1507 needs to change for #1506.

**Note 3: the four new cells do not run without an install.** The `*'SKIP (advisory)'*` branch (l.164) prints a note instead. This is the same pattern as the cell it replaced. CI (dormant, no `npm ci`) would therefore never assert the default list; only seats' hooks do.

**Note 4: the failure text is "Fix the type error in the test file named above" (l.72) for every non-zero rc.** That covers rc 2 (E3/E4: there is no test file to fix) and errors in PRODUCT files reachable from the tests (the KS-1517 TS2307 shape). It is pre-existing wording, and gating the gateway sends it to more pushes. The checker counts every error in the test program, not only those in `__tests__` (`check.cjs:58-60` and 73-75 key all errors), so this leg is now also the only push-time type-check of gateway product code reachable from its tests. That is a benefit, but the message should say "the file named above".

**Note 5: header residue.** l.7 and l.13 still describe auth only ("services/auth/tsconfig.json excludes…", "The auth vitest suite does"), though the gateway has the same shape (`ks1090-…shrinking-baseline.test.ts`). l.19 is now about 150 characters. Cosmetic.

## KS-1517 recommendation

**Accept as is: merge #1507 now, and raise KS-1517 from P4 to next-up.** Do not add a hint in this PR.

Why:
- The refusal is fail-closed and not false. Under the same stale dist, the gateway's own product `tsc` fails (rc 2, the same two TS2307 errors), so the local tree really does not build. Only the label is wrong, and the error text itself ("Cannot find module '@secuura/shared/…'") points at the cause.
- Recovery is a 3.6 s rebuild (`npm run build -w @secuura/shared`, or `npm ci`).
- Landing KS-1517 first keeps a measured hole open (§3: a gateway test type error is accepted on push) to fix a message.

How often a seat is stale:
- Nothing in the hook or preflight rebuilds shared. Only `npm ci`'s postinstall does.
- So a seat's worktree is stale whenever it merges or rebases a develop where shared's EXPORTS changed and gateway code consumes the change, and has not rebuilt since.
- Develop since 2026-09-13: 40 commits touched `packages/shared/src` (of 646). 3 of them also touched `services/api-gateway/src`; since 2026-08-14 it is 14. That is a lower bound for trigger events (a consumer can land later than the export): roughly one event a week to a fortnight.
- Each event can hit every active seat once, until it rebuilds. Most shared edits keep the old dist type-compatible and do not trip it.

Cost of each option:

| option | cost |
|---|---|
| Land KS-1517 first | The hole stays open until KS-1517 is written, gated and merged (likely more than a day). The order dependency also delays #1506's interaction work. |
| Conditional hint in this PR | The leg must capture and grep the checker output instead of passing it through (`run_delegated` already captures it one level up). That means new cells, a re-gate (Sonnet delta), and a push-gate script widened past a one-line brief. Moderate risk for a cosmetic gain. |
| **Accept as is** (recommended) | Occasional confusion: about one event per week or two, each costing a seat a few minutes plus a 3.6 s rebuild. |

Mitigations for the accept option:
- Wednesday sends one fleet line now: "leg 16 reporting TS2307 on `@secuura/shared/...` means your shared build is stale: `npm run build -w @secuura/shared`, then push again."
- Scope KS-1517 to detect, not just hint. For example, `deps-present.sh` or the leg checks that every `exports` target in `packages/shared/package.json` exists under `dist` (this would have caught the reproduced case), with the rebuild command in the message.

## Not measured

- The full 16-leg pre-push hook, a real push, and the full `run-shell-suites.sh` (83 suites). I ran the 7 preflight suites named above and `--check-unreached` only. The builder's "13/16, 83/83, 462 s" is not re-run.
- Stale-dist cases other than missing export targets (e.g. a dist present but with outdated type signatures). Only the hidden-files simulation was run.
- Whether any other leg (e.g. leg 1's tsx run, or leg 14's suites importing gateway code at runtime) also fails under a stale shared dist. Not run.
- A worktree with an install but no `packages/shared/dist` at all (the builder says ks949 in leg 14 refuses it first). Not run.
- A cold-cache timing (all timings warm) and other Node versions (v24.7.0 only).
- #1506 was used only as a trial merge for the interaction notes. It is gated separately.
