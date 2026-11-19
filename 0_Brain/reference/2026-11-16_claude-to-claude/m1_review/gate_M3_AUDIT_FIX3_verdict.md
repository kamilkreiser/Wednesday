VERDICT: GO WITH NOTES — head 718abe8c9a425694c1c2cf893f1d100468dbdf25

# QA gate M3-AUDIT-FIX3 (tier 1, the one short check): `coagent-audit`, branch `m3-audit-fix3`

Independent check, 2026-11-19. Findings only. I fixed, committed, pushed and merged nothing, and wrote nothing in the project folder (git read verbs only there). Every write went to `/private/tmp/claude-501/ga3` or to this folder.

- **Head (TESTED).** Friday's tool cloned the branch, and `head.txt` reads `branch=m3-audit-fix3 head=718abe8c9a425694c1c2cf893f1d100468dbdf25 want=718abe8c…`. `git rev-parse bfe435abbe86…` in the project repo gives main as briefed. `git log bfe435a..718abe8` shows two commits: `0155456` (code, tests, quarantine, runner row) and `718abe8` (docs, BACKLOG).
- **Remote.** I did not read the remote (no `ls-remote`, see NOT TESTED).
- **How figures are marked.** Every figure here is TESTED (I ran it) or READ (I read it). A builder figure is cited only when my run matched it.

## BLUF (for the owner, in plain words)

1. **The restart fault you asked to close before the beta is closed.**
   - **What changed:** the product now quietly trims any limit setting that would give some part of your own space more room than the factory defaults give.
   - **Why that fixes it:** a restart puts the defaults back, and they now never hold less than you had before. So a request that was waiting for its "checkpoint" still has room after a restart.
   - **What I tried:** about 389,000 limit settings, including every edge I could think of. I also tried 20 filled-up cases that I restarted both ways. None broke it (TESTED).
2. **Trimming never strands anything.** Every room check is made against the trimmed limits, the ones actually put in force. A setting that would not leave room is refused, and a refusal changes nothing (TESTED).
3. **The builder's figures reproduce exactly.**
   - The full check passes: 930 tests passed, 0 failed.
   - All 154 deliberate-break controls go red, each on its own named property.
   - The big generated test passes at 1,024 cases on three different seeds, now with no exemption for the restart fault (TESTED).
4. **The test edits Friday ruled on strengthen the tests, they do not weaken them.**
   - The removed exemption code is kept word for word in a quarantine file.
   - The six gate files and `qa_fix.rs` are unchanged.
5. **Merge: GO WITH NOTES.** There is no Blocker, no Major and no Minor, only three Notes. The one a later reader should see is QA3-n1: a store written by an older build, before this fix, would not be recoverable. Nothing like that exists yet, because the daemon is not built.

## Findings

| id | sev | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| QA3-n1 | Note | **Upgrade path (READ and argued, NOT TESTED).** Limits are not stored; `resume` installs the defaults. Suppose a store was filled by a build from before this fix, under an offer with fewer records, so a payer's allowance holds more than the defaults' allowance. On this build that store comes back in the old resume-defaults state. The old remedy, re-offering the earlier limits, no longer exists: every offer is now capped to at most the defaults in every part, so clause (A) refuses them all, and the owed checkpoint stays refused. No such store exists today (pre-beta, no daemon). It matters only if stores ever cross this version boundary. | reading `try_set_limits` cap (session.rs:615-637) with clause (A) (:639-) | n/a (not built) | `crates/coagent-audit/src/session.rs:612-667`; `docs/AUDIT.md` "Restart" |
| QA3-n2 | Note | The branch's own grid covers record limits from 8 per seat up, multiples of 8 only. Untested there: records 0..7 per seat, values that are not multiples of 8, records or bytes above the defaults far out to `usize::MAX`, and bytes per seat below records per seat. My sweep covers all of those, and every one passes. Coverage only. | `qa3_every_offer_is_installed_at_or_below_the_defaults_in_every_part` | TESTED: "qa3 sweep: 389240 offers, 198268 lowered, 190972 not lowered, 695 with bytes per seat below records per seat; all at or below the defaults in every part" | `tests/fix_qam1_seat.rs` `fix3_no_accepted_limit_gives_any_part_more_room_than_the_defaults` |
| QA3-n3 | Note | The pin keeps its old name, `qam1_finding_resume_defaults_leave_an_owed_checkpoints_payer_without_room`, but now asserts the opposite of that name. Renaming was not ruled. The `qa_fix2.rs` STOP comment stays as a record, as addendum 1 item 3 allows. Naming only. | — | READ | `tests/fix_qam1_seat.rs` (pin), `tests/qa_fix2.rs:608-609` |

No Blocker, no Major, no Minor.

## Rulings, items 1-7

**1. Per-part monotonicity. CONFIRMED: `pb ∸ pr ≤ db − dr` is the one comparison, and it is also necessary.**
- **Code (READ):**
  - `per_peer` = (bytes/8, records/8).
  - `own_seat` = (pb ∸ pr, pr), `budget.rs` `saturating_sub`.
  - `free_part` = own/2.
  - `requested_allowance` = ((own − own/2)/7, (pr − pr/2)/7).
  - `peer_pool` = 7·seat.
- **Monotonicity.** Every floor division here is non-decreasing, and `own − own/2` is ⌈own/2⌉, also monotone. So:
  - the records of every part depend on pr alone;
  - the seat's and the pool's bytes depend on pb alone;
  - the own seat's, the free part's and every allowance's bytes depend on pb ∸ pr alone.
- **The clamp (READ, session.rs:629-636):** `pb' = own_max + pr`, written as `(own_max+pr)*SEATS`. It runs after the `min` caps, so nothing overflows (pb' ≤ db). The records are kept.
- **Exhaustive arithmetic (TESTED, `qa3_arith.py`):** for every pr from 0 to 28,604 there are 0 violations. One byte more per seat always breaks a part (necessity: 0 counterexamples). 200,007 random u64 offers give 0 violations. The pin offer → (40722712, 171624).
- **Against the real crate (TESTED, `qa3_every_offer…`):** 389,240 offers, covering:
  - records 0..17;
  - every pr from 0 to dr+1, at 8r and 8r+7;
  - straddling the boundary for every pr, with slack 0 and 7;
  - bytes 0, 1, 7, 8, 9, near `usize::MAX`, and `usize::MAX`;
  - records above the defaults, and `usize::MAX`;
  - 100,000 random offers.

  On every offer: accepted; every part ≤ the defaults' part, by the crate's methods AND by an independent arithmetic; installed equals an independent model of the cap; records kept; bytes never raised; when lowered, the own seat bytes are exactly 5,068,886; re-offering what is installed is a no-op. **No part above the defaults was found.**

**2. CLAMP behaviour. CONFIRMED.**
- **Nothing refused when nothing is owed (TESTED):** every one of the 389,240 offers returned `Ok` on a session with nothing owed. The property's "small limits refused on a new session" check stays.
- **Records-only lowering (TESTED):** records kept on every offer.
- **Clauses (A) and seat unchanged (READ):** the `session.rs` diff touches only the doc comment and the cap block. The hunks end before `RED CONTROL limits_strand_payer`, and both clauses test `new`.
- **`set_limits` (READ):** still `let _ = self.try_set_limits(limits);` (:674-675).
- **Public surface (TESTED):** the sorted `pub` lines of `src/`, start against end, are 481 and 481, with an empty `diff`. `src/` changed only in `session.rs`, so there is no new error variant.

**3. Closes the resume-defaults state and QA2-m1, and adds no stranding route. CONFIRMED.**
- **Only two writers of `self.limits` (READ):** the constructor (:255, defaults) and `try_set_limits` (:666). `resume_with_anchor` calls `resume`.
- **QA2-m1's own input (TESTED):** "after resume: checkpoint Ok(()), defaults Ok(()), L Ok(()), checkpoint Ok(())".
- **Restart attempts (TESTED, `qa3_no_restart_strands…`):** 12 record limits from 8 per seat to dr−1. Three fill shapes: tiny requests, large requests, and seven requesters plus own events. Each was restarted with both `resume` and `resume_with_anchor`. That is 32 cases, 20 with a checkpoint owed. 30 of the offers had an OFFERED allowance above the defaults'. In every owed case:
  - the checkpoint was `Ok` before the restart under the installed limits;
  - after either restart the checkpoint was `Ok` and covered the newest own event;
  - the defaults were accepted;
  - the own offer was accepted and installed exactly as before the restart.
- **Can the clamp strand? (TESTED, `qa3_an_offer_installed_lower…`):** an allowance was filled under the defaults (687 requests), then fewer-records offers were made. pr 8..2000 were refused `LogFull` with the limits unchanged. pr 14302 and 28603 were accepted and installed lowered. The checkpoint was then `Ok(687)` in every case.
- **N1's arms unchanged (TESTED by text comparison of main and head):**
  - P2's N1 arm (45 lines) and P3's N1 exception (26 lines) are IDENTICAL.
  - So are `exception_state`, `model`, `a_fits`, `own_seat` and `resumed`.

**4. P4, the reach key, the seeds and the red rows. CONFIRMED (TESTED).**
- **The 64-case run:** "limit offer lowered by the defaults clause: 133", 11 passed.
- **The three 1,024-case release runs:**

  | seed | result | time | P4 key | P2 N1 cases | P3 exception | accepted with a requested event owed |
  |---|---|---|---|---|---|---|
  | committed | 1 passed, exit 0 | 230.78 s | 2184 | 12 | 80 | 1995 |
  | 7 | 1 passed, exit 0 | 259.36 s | 2215 | 3 | 47 | 2163 |
  | 200 | 1 passed, exit 0 | 245.13 s | 2162 | 21 | 136 | 2113 |

  No resume-defaults output appears and there is no carve-out code. Every count equals the builder's.
- **Runner, row `limits_above_defaults`:** RED on "QA2-m1 property P4: step 24: an accepted change (aim records exact, offered StoreLimits { bytes: 40779920, records: 56 }) installed StoreLimits { bytes: 40779920, records: 56 }: own seat (5097483, 7) above the defaults' (5068886, 28604)".
- **The other limits rows, each red on its own text:**
  - `limits_strand_payer`: "R5-m1 property: step 26: … because its payer, the allowance of slot 0, lacks room".
  - `limits_strand_seat`: "QA-m1 property P1: step 13: an accepted change (aim bytes short) …".
  - `limits_may_raise`: "P28: set_limits raised the limits above the default", and the code still takes the offer uncapped (READ).

**5. Removal R2. VERBATIM, and no needed guard is lost.**
- **Verbatim (TESTED):** all 13 excerpts in the quarantine file are line-for-line equal to main's `fix_qam1_seat.rs` at their labelled ranges (394 lines).
- **Removed lines (TESTED):** every removed line not in the quarantine is one of:
  - a call-site argument for the tracker;
  - a pin line quoted as `// old:`;
  - a comment rewrite;
  - the `capped` model body;
  - the seed line.
- **No guard lost:** the recogniser only let refusals PASS. Removing it makes P2 and P3 stricter: payer-short and P3 refusals now fail at once. The state it recognised cannot be built (items 1 and 3).

**6. Ruled test edits. ALL PERMITTED and STRONGER.**
- **Pin:**
  - adds "offer lowered, allowance ≤ defaults'";
  - `fits(u, in_force)&&fits(u, a_def)` replaces the old setup;
  - 3 of 3 `Ok` and `set_def == Ok(())`;
  - `set_before` Ok and `cp_then == Ok(seq)` are kept;
  - printed line (TESTED): "3 checkpoints [Ok(()), Ok(()), Ok(())]; try_set_limits(defaults) Ok(()); … checkpoint then Ok(687) of 687".
- **`qa_fix2.rs`:** exactly two hunks (TESTED diff):
  - :498 → `v.limits() != l && allowance ≤ defaults'`;
  - :596 → fits under the installed limits AND under the defaults;
  - `cp_d` and `set_d` → `Ok(())`;
  - `set_l` and `cp_d2` → `Ok(())`. These two are permitted by addendum 1: they are the remaining steps of the same remedy and assert it works.
  - Each change sits under a ruling marker, with the old lines quoted.
  - The lines `!fits(seat_now, l.per_peer())`, `cp_l`, `again_l`, `set_third` and `cp_third` are unchanged.
- **Unchanged files (TESTED):**
  - Git blobs, main against head, are EQUAL for `gate.rs`, `gate_attacks.rs`, `gate_r2.rs`, `gate_r3.rs`, `gate_r4.rs`, `gate_r5.rs` and `qa_fix.rs`.
  - sha256 prefixes at head: d6a29f1e2966b1a6, 6ef41612b4e4241c, adca67f33b042632, c1726e9d84744d7b, addc9f79bb321b3a, d16e82d53356b062, b4100b5aa2251839.
  - `qa_fix2.rs` is d2d75f3e3e447427 at head, changed by the ruled hunks only.

**7. Docs and BACKLOG. TRUE.**
- **`docs/AUDIT.md` (READ the diff against the code):**
  - "The cap" states the clause and the argument.
  - The 40,722,712 example matches my arithmetic and the grid's printed line.
  - "Restart", the charging row and "Limits, stated" are closed in the file's form ("fixed in M3 AUDIT-FIX3, the owner's answer …").
- **BACKLOG:**
  - :380 and :385 are closed as `- [x] <original unchanged> — CLOSED in commit 0155456…`.
  - :337 and :362 each gain a CORRECTED sub-line and stay open.
  - The diff is 6 lines, and nothing is deleted.
- **The daemon guidance is correct.** "After every resume re-offer own limits and read `limits()` back; no limits need be kept for correctness" holds because the cap is a deterministic function of the offer, so a re-offer installs the same limits. My restart test (c) shows exactly that, except in N1's exception, which the guidance names.

## What I ran (TESTED)

| run | command | result |
|---|---|---|
| merge check | `coagent_merge_check.sh /private/tmp/claude-501/ga3/mc m3-audit-fix3 718abe8… scripts/red-controls-audit.sh` with my RED_TARGET and RED_LOGS | `TOOL_EXIT=0`; "MERGE CHECK OK m3-audit-fix3 718abe8c…" |
| `check.sh` | inside the merge check | exit 0; "CHECK OK: fmt, clippy, test, deny all passed"; 118 result lines, 930 passed / 0 failed / 18 ignored. Warning: only the known unused `rand_core` |
| red runner | inside the merge check | exit 0; "rows: 152 cfg rows + 2 source-mutant rows"; 154 RED, 0 "NOT-RED" (count from `grep -o -c`); "GREEN: 265 tests ok"; "RED CONTROLS OK" |
| property at 1,024 cases, release | committed seed, seed 7, seed 200 | each exit 0 (table in item 4) |
| `fix_qam1_seat` (64 cases, release) and the QA2-m1 test | `--nocapture` | 11 passed, exit 0; 1 passed, exit 0 |
| my `qa_fix3` | head `fix_qam1_seat.rs` plus `qa_fix3_addon.rs`, in a work copy | 3 passed, exit 0 |
| `qa3_arith.py` | exhaustive arithmetic | 0 violations |
| added-line scan | 880 added lines | 0 hits for the owner's names, client names, "laptop", "devmaster", "/volumes", "/users/", "/home/", "/private/", "!coding", "wednesday", "tuesday". "friday" 17 hits: the ruling markers' role name. Positive controls: "audit" 88 hits; the short first name 6 hits in the project `CLAUDE.md` |

**Files** (in `gate_audit_fix3_tests/`):
- `qa_fix3_addon.rs`, `qa3_arith.py`, `qa3_arith.txt`, `qa3_run.log`;
- `prop_{committed,7,200}_1024.log`;
- `fqs_and_qa2m1_at_head.log`, `red_audit_run.log`, `check_sh_tail.txt`.

## NOT TESTED

- **The remote:** no `ls-remote`, so I cannot say whether main or the branch moved after `718abe8`.
- **The upgrade path in QA3-n1:** argued by reading, not built.
- **Mutants of the new clause** beyond the runner's `limits_above_defaults` row.
- **N1 states** in which the defaults' SEAT itself lacks room after a re-add. These existed before this round and are pinned as before; P3's exception arm is unchanged.
- **The rest of the workspace:** `red-controls-core.sh`, and the gate files in `--release -- --ignored`.
- **Disk use:** `du` on my work dir printed "0B", which I do not trust (see instrument errors), so it is unmeasured. Nothing outside my work dir was deleted, and no process of mine is left running.

## Instrument errors

- **Shell refused my first call.** My first background call was refused by the no-`cd` hook. I re-issued it without `cd` and it ran once.
- **Wait loops.** Two foreground wait loops were moved to the background by the harness. Neither started a job.
- **`zsh` path modifier.** `"$H:c…"` in an early `git show` was read as a `zsh` modifier. I re-ran it with `"${H}:…"`, and no figure came from the failed call.
- **Truncated view.** An early `grep | cut -c` view printed nothing for the grid and pin lines. I re-read them untruncated with `grep -o`, and that is the text quoted above.
- **`du` output.** `du -sh` printed "0B" for my work dir, which is not credible, so I report no disk figure.
