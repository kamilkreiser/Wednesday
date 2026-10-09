# KS screen for the Spark: 2026-10-09, 14:00 delta (1 brief delivered: KS-998 stdin robustness note)

Written 2026-10-09 14:16 AEDT (shell `date` 14:16:05) by a Spark brief-writer sub-agent for Wednesday. Secuura only. Method: SCREEN_0300's (delta, union, positive control, exclusions before screening), the kit predicate (`spark-kit_2026-09-23/02_FOR_THE_COORDINATOR.md` §2), and the kit 03 brief shape. The brief copies the shape of the PASSED `night/briefs/KS-998-format-gate-grep-fixed`.

**Read-only on client systems:**
- **Linear:** GraphQL reads only. The key was sourced from the Blockchain `4_Credentials/.env` in a `set -a` subshell and never printed.
- **GitHub:** REST GET only (open PRs and their files).
- **Git under `!CODING/`:** `ls-remote`, `cat-file` and `status` only. `git status --porcelain --untracked-files=no` on the Blockchain checkout read 0 lines at 14:16:05.
- **Write verbs in scratch only:** every one ran in `git clone --shared --no-checkout` copies under `scratchpad/spark1400/` (`clone`, `wt`). `apply --cached` used a throwaway `GIT_INDEX_FILE`.

**Not touched:** `spark/queue.md` (git status 0 lines), `queue.sh`, `night/queue.md`, mail, Linear writes, GitHub writes. No real round was run. Nothing was deleted. Nothing was created under `!CODING/`.

## BLUF

1. **Tip:** develop `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6` (KS-1452 lock refresh), read by `ls-remote` at 14:06:30, 14:14:26 and 14:16:05 AEDT, unchanged. It is the sha Wednesday read at 14:05:19.
2. **Delta: 18 distinct open tickets** (instrument: `scratchpad/spark1400/q/lin.py`; both queries were paginated until `hasNextPage` was false).
   - Created since 2026-10-07T16:00Z, open: 3.
   - Updated since then, open: 18.
   - In both: KS-1451, KS-1452, KS-1453. This is the **positive control**.
   - Created in any state: 4. The fourth is KS-1450, which is Done.
3. **Delivered: 1 brief (target 6). The pool is thin; it was not the method that stopped short.**
   - 15 of 18 tickets are live or drafted lanes.
   - Of the 3 screened, 2 fail the predicate (KS-593, KS-1451).
   - The harder screen's only never-run candidate, KS-937, is an excluded lane.
   - KS-998 passes the predicate on its unbriefed robustness note: a real, measured defect.

   | brief dir | ticket | tier · rung | dry-run | golden |
   |---|---|---|---|---|
   | `night/briefs/KS-998-format-gate-npm-stdin/` | KS-998 (In Progress, Kamil), "Robustness note" only | bash_patch · rung 1 (1 hunk, 1→4 lines + NEW 93-line suite) | `round.sh --dry-run` **rc 0**, `DRY-RUN OK … input built at 81d2e5f4c415 (42837 B)`; `input.ticket.description == brief` True (17,036 chars) | `apply --cached --check` at tip **rc 0**; reversed **rc 1** (control) |

4. **Owner calls for Wednesday (none acted on):**
   - **(a) Counter on KS-998.** Item 1 spent its counter on 09-16 (Ornith, 2 FAILs, reallocated to Claude). Item 4 then got a fresh per-item counter and PASSED. This brief assumes the same per-item precedent: the note has 0 rounds. If you count per ticket, this goes to the Claude lane that owns item 1.
   - **(b) Merge order.** Item 1's Claude lane edits `check-package-format.sh:146-150`, four lines above this hunk. Land this first, or fold it into that lane.
   - **(c) The pool is dry until the gate77 lanes land.** The delta's mechanical work is all owned (lanes listed below). The next screen yield comes when #1429-#1436 merge and leave residues, or when new KS tickets are filed. Widening beyond the delta (a full Backlog re-read) is your call. The harder screen read 487 tickets on 10-08.
   - **(d) Security routing.** KS-593's remaining open register items route as "Claude: security surface". They are `POST /api/issuer-certs/{id}/revoke` and `/rotate` (5/5 per sweep), `POST /api/auth/wallet/verify` and `/api/m365/outlook/exchange-token`.

## FOUND / TESTED / HOW

- **FOUND:** in `systemTest/scripts/check-package-format.sh` at the tip, the per-package loop reads its selection from a here-string on stdin (`:138` … `:196 done <<< "$selected"`). Inside it, `:152` runs `npm run --silent format:check` with no stdin redirect. A `format:check` that reads stdin therefore swallows the remaining package names. **A red package after it passes the gate (exit 0).** The ticket called this hazard one "the fixtures cannot detect"; they can.
  - Latent in the live tree: all 4 real gated packages run `prettier --check … .`, which does not read stdin. This was read from each `package.json` at the tip.
- **TESTED:** the new suite was run at the tip and with the fix, on macOS with bash 3.2.57, npm 11.5.1 and node v24.7.0. Siblings were run on both sides:

  | suite | at tip | with fix |
  |---|---|---|
  | new suite | **rc 1, 6 passed / 3 failed** (exactly the 3 red cells); stderr 0 B | **rc 0, 9/0**; stderr 0 B |
  | `package_format_gate` | 33/0 | 33/0 |
  | `ks998_format_gate_push_label_is_literal` | 8/0 | 8/0 |
  | `pre_push_hook_base` | 28/0 | 28/0 |
  | `pre_push_hook_current_develop` | 4/0 | 4/0 |

  All four sibling suites returned rc 0 on both sides.
- **HOW:**
  - Files were extracted with `git archive` from the scratch clone. A second shared clone, checked out at the tip, produced the golden: `git diff`, with the product hunk hand-reduced to trailing context only, because `:151` is blank and the code_patch builder's blank-context rule (`night/build_input.sh:572-585`) warns the model will not reproduce one.
  - The golden was applied to a fresh index of the tip. Each indexed file was then compared with `cmp` against the measured file: identical.
  - The brief's two fences were extracted with awk and compared with `cmp`: identical to the measured test file and the golden hunk.
  - sha256/16: brief `a075f8ffcfacb066`, golden `7c902e7891931b84`, pins `b8c87c7ec7d10ac5`.

## Verdict per ticket (screened: 3)

| Ticket | Verdict · predicate clause |
|---|---|
| **KS-998** formatting gate residue | **PASS → briefed (the Robustness note only).** It is one product file, and the ticket spells the fix ("`< /dev/null` on the `npm run --silent format:check` invocation"). There is an in-process fixture suite to copy (`package_format_gate.test.sh:27-89`). It is not a security surface, and this item has had 0 rounds. Runner: bash.<br>The other items are **not briefable**:<br>- Item 1 is counter-spent (`night/done.md:184-185`, reallocated to Claude), and its "install it also" half has no spelled mechanism.<br>- Item 2 is a **decision**: working tree vs the pushed commits, with no option ruled.<br>- Item 3 is **test-only with no product change**: nothing to red, and test_only is not wired into `round.sh` (per the README).<br>- Item 4 has landed (`7bcc2ed54`). |
| KS-593 not_a_server_error register | **NOT.** #1428 has merged (`1e7f90e26`). No comment since 10-07T16Z; the latest is 10-07T14:53Z. The remaining pairs fail as follows:<br>- **Security surface:** issuer-certs revoke/rotate (the 22P02→404 mapping), `auth/wallet/verify` (CIP-8; also mechanism "not established … replay `xPmeIe`"), `m365 exchange-token`.<br>- **Admin/ruled:** `users/admin/list` and `/create` (the KS-592 ruling; the KS-1447 owner question).<br>- **Measure-first:** `gdpr/consent` and `/dsr` (intermittent, "cause unknown").<br>- **Merged:** documents share. |
| KS-1451 bare `slot-literal-ok:` marker | **NOT: not one file and no single runner.** The ticket requires all five guards to change "in one change, so they stay in agreement". Those are bash, two vitest packages, Playwright and pytest; that is 5 files, more than code_patch2/bash_patch2 allow, across 4 runners. A carve would make the guards disagree, which the ticket forbids. This is unchanged from the 10-08 harder screen. |

## Harder-screen candidates re-checked

The harder screen delivered 2 candidates, and neither is open for briefing:
- **KS-1438:** run twice on the Spark (FAIL B3x both times, `spark/done.md:50-51`). The counter is spent, and it goes to a Claude seat (an excluded lane).
- **KS-937:** never run (0 rows in `spark/done.md`). It is excluded as the held Ornith pass (commission list).

The harder screen's rejection table (32 rows) proposed no further candidates. So the never-run residue is 0 briefable. The positive control is KS-937: it is never-run and is found by the same check.

## Exclusions before screening (15 of 18), by reason

- **Live or drafted lanes (commission list):**
  - KS-1274 (#1427, R 22nd live)
  - KS-1449 (#1429), KS-1328 (#1430), KS-1355 (#1431), KS-1410 (#1432), KS-1139 (#1433), KS-1171 (#1434): awaiting gate77
  - KS-808 (#1436)
  - KS-1452 and KS-1453 (lock refresh)
  - KS-1402 (lane K)
  - KS-723 (lane U)
  - KS-1385 (lane W)
  - KS-695
  - KS-1195
- **Assigned to Peter or Stuart:** 0 in the delta. Every delta ticket is Kamil's or unassigned (KS-1328).
- **Done or Canceled:** KS-1450 (created set only, Done). Excluded by the state filter.
- **Security surface:** KS-1402 and KS-1195 are also security surfaces (auth lookup, the per-key rate limiter); both are already excluded as lanes.
- **Open-PR file collision:** GitHub REST GET at about 14:08 AEDT read **30 open PRs and 152 file entries**. 0 touch `check-package-format.sh`, `package_format_gate.test.sh` or `.githooks/`.
  - Positive control: 9 `systemTest/` entries and 13 `Blockchain/Dev/scripts/` entries were seen.
  - #1428 (KS-593) and #1422 (KS-998) are no longer open.
  - Not in the delta, and listed only for completeness: KS-1384, KS-1438, KS-937, KS-1175, KS-1387, KS-1172.

## UNMEASURED

- **`round.sh --control` not run.** The checker legs (B1-B7) were not run on the golden; only `--dry-run` was. The red and green split was measured by running the suites directly, not through `tasks/bash_patch/checker.sh`.
- **The dry run fetched develop into the Wednesday-side Spark cache.** The log line was "fetching develop from origin … not yet local", and it left `spark/state/dry/KS-998-format-gate-npm-stdin_20261009-141546/`. The fetch went into the Wednesday-side cache, not the Secuura checkout.
- **Linux, GNU tools and other npm majors were not run.** That `npm run` passes stdin on other versions is reasoned, not measured.
- **Linear comments were capped at `first:50` per ticket.** No delta ticket reached the cap; the maximum was 26, on KS-593.
- **Field-level history of the updated-only tickets was not read.** That covers why KS-998 was updated at 10-07T18:53Z; the assumption is that a PR attach or merge did it.
- **Live seats' unpushed work on the format gate was not checked.** Only open PRs were read.
