This addendum is from Friday (Kam's laptop coordinator seat). Client: General (Kam's personal project). Project: CoAgent. You are a NEW AUDIT seat: the seat that built branch `m3-audit` is gone, and you resume its branch. This addendum extends the original brief and addenda 1 and 2. Report by appending "ADDENDUM 3 (storage accounting redesign)" to `coagent/5_Project_History/STATUS_M3_AUDIT.md`; while working, the file's last line is `IN PROGRESS: A3 <item>`, and when done it is exactly `READY FOR QA M3-AUDIT r4`.

# M3 AUDIT — addendum 3: the storage accounting, redesigned as a whole (third NO GO at 882e094, one class three times)

## 0. Authority

- Kam, live board 2026-11-17 08:50:33, view=friday (as Friday read it), verbatim: "Decision general-c2c-audit-third-check-failed-1117: a — Redesign the storage accounting first, then one build and one check".
- The build grant: Kam typed "yes, keep building today" in Friday's terminal; card `general-c2c-morning-plan-1117` = a. The grant row is at the top of `/Volumes/Laptop-DEV/FRIDAY/0_Brain/tasks/EXPIRING-GRANTS.md`. It ends at the end of Tuesday 2026-11-17: at that point you finish your current step, push if green, and report. No deploy, no publish, no spend. The repository stays private.
- Standing rulings that bind: the audit log holds hashes and short redacted previews; nobody independent will review this code, so tests are the only guard; unreviewed beta.

## 1. Where this stands

Three independent checks have failed this crate on ONE class: one party fills or exhausts storage that another party needs in order to act. Round 1: unlimited checkpoints. Round 2: any peer filled a member's store with cross-check records. Round 3 (R3-M1): records are charged to whoever signed them, not whoever caused them, so three members flooding the starter made the starter's receipts fill the starter's share at every other member in 1.4 s, after which those members could not apply any member-list version, including the removal of the attackers. Patching one rule at a time has failed three times. The owner ruled a redesign.

The redesign is written. **It is document A:**
`/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/07_audit-storage-accounting-redesign.md` (cited below as **[07 §n]**). You build exactly that. Where this addendum and [07] differ, [07] wins and you record the difference under DESIGN QUESTIONS.

## 2. Read first, in this order

1. `coagent/CLAUDE.md`, then the original brief and addenda 1 and 2 in `/Volumes/Laptop-DEV/FRIDAY/2_Project_Files/friday/briefs_drafts/` (`2026-11-17_coagent_M3_AUDIT_brief.md`, `…_ADDENDUM-1_gate_return.md`, `…_ADDENDUM-2_delta_gate_return.md`).
2. **[07] WHOLE.**
3. The third verdict WHOLE: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M3_AUDIT_r3_verdict.md` (its storage-path table §3, Minors R3-m1 to m3, Notes n1 to n6, the surviving mutants §5). Then the first two verdicts in the same folder.
4. The gate's round-3 tests and results: `…/m1_review/gate_audit_tests_r3/` (`gate_r3.rs`, `mutate_r3.py`, the two `release_*.txt` files, the two survivor files).
5. `coagent/5_Project_History/STATUS_M3_AUDIT.md` WHOLE (the earlier seat's report; its ADDENDUM 2 table A2.1 is what you are replacing).
6. The crate as it stands: `crates/coagent-audit/src/` whole, `docs/AUDIT.md`, `scripts/red-controls-audit.sh`, `BACKLOG.md`.
7. The lesson file named in section 11.

## 3. The state you inherit: confirm it before anything else

- Worktree `coagent/worktrees/m3-audit`, branch `m3-audit`, head **`882e0940c1a34d76a9836256c7bff67283ec5609`**. Friday's architecture agent read local and remote-tracking refs both at that value, with no staged or unstaged difference. **Confirm it yourself:** `git rev-parse HEAD`, `git ls-remote origin m3-audit`, and a clean worktree. If any of the three differs, STOP and write it under BLOCKERS.
- At that head, as the third check reproduced: `scripts/check.sh` exit 0, workspace 217 passed and 5 ignored, audit crate 114; audit red controls 93 of 93; core red controls 65 of 65; merged tree with `origin/main` (18005d6) 366 passed and 10 ignored. Reproduce `check.sh` and the audit red-control runner once before you change anything, and record the figures.
- The only change this branch has made to a merged crate is commit c407fe7 (five `SignDomain` values in `coagent-crypto`), authorised in addendum 1. Nothing further is authorised (section 10).
- A temporary worktree `coagent/worktrees/m3-audit-merge-check` exists from the earlier seat. Leave it. Make your own with a new name.
- `CARGO_TARGET_DIR` is `tools/target/m3-audit`. The disk is nearly full: report the space you use.

## 4. Order of work: the verifier first

1. **First commit: the round-3 gate file, unchanged.** Copy `gate_r3.rs` byte for byte into `crates/coagent-audit/tests/`, compiled through a `#[rustfmt::skip]` wrapper and a `[[test]]` entry exactly as `gate_r2` is (`tests/gate_r2_wrapper.rs`; commit 01c0c87 shows the pattern). Run it debug and `--release --ignored`. Record every test's result. Expected at 882e094, from the verdict: 12 debug and 2 release tests pass, where each passing `r3_finding_*` means the weakness is demonstrated. In the same commit add one test for [07 §5.2] U6 (a roster version within a few bytes of the 65,535-byte maximum, built in the test: does `apply_roster` refuse it while the roster chain accepts it?) and record what it shows; if such a version cannot be built under the roster's own rules, say so and why.
2. **Second commit: the property harness and every test that can be written against the API as it is, failing.** The generated-schedule harness of [07 §3], with properties P1 (a), P1 (b), P2, P3, P4 and P6 expressed with today's functions. Record, for each, the assertion text it fails on. A test that fails for a reason other than its property is not done.
3. **Third commit: the new function signatures as stubs that return an error, with the remaining tests failing at run time** (P1 (c), P5, P7, P8, P9, the single-check guards). Record the failures.
4. **Then the implementation**, in whatever order you judge, with `check.sh` green before each push.
5. **Then the red controls:** every row of section 6, each seen red on its named property's assertion text, then everything green.
6. **Then the gate files:** apply the rulings of section 8, list them.
7. Docs, the merged-tree build, the report.

Push after every green `check.sh`. Update the STATUS last line at least every 20 minutes.

## 5. Deliverables (each with its place in [07])

| # | Deliverable | [07] |
|---|---|---|
| 1 | The fixed part: seven tables with slot counts and a maximum size per slot, set aside whole; an object above its kind's maximum refused with its own error at the first step | §1.4 (a) |
| 2 | Roster versions never refused for space; the roster chain's own answer returned, also for a replayed or held version; the two lifetime backstops (256 versions, 32 keys ever) with their own error, checked before the roster chain is touched | §1.4 (a), §1.7 step 4 |
| 3 | A roster conflict (a second, different, starter-signed version of a held number) kept in its one slot, exported, and reported by `verify` as a roster fork | §1.4 (a), §4.1 |
| 4 | Eight seats by roster slot; a record charged to the seat its author occupies in the current roster when it is accepted; the own seat's limit and its split into the free part, seven requested allowances and the closing-checkpoint reserve | §1.4 (b) |
| 5 | `record_for` (an own event recorded at a named member's request), refused for a causer that is not a roster member | §1.4 (b), §1.11 |
| 6 | No receipt events. The countersignature gains the signed field `held_from`; the author keeps the latest countersignature per member; `verify` checks the field's range | §1.5 C and D, §4.1 |
| 7 | Cross-check records received: two slots per reporter, replaced in place, with the existing "advances", duplicate and removed-reporter rules. Cross-check records sent: not stored, and cannot fail for space | §1.5 D, §4.2 |
| 8 | Other authors' checkpoints: a log in the author's seat up to the existing cap; beyond the cap or a full seat, the newest kept in one slot per author and still countersigned (with `held_from: None` when the events are not held) | §1.5 D, §1.8 |
| 9 | One order of checks in every function that takes a peer's object: cheap refusals, signatures, conflicts (evidence stored in the fixed part and ALWAYS returned), the roster crate's answer, space with the exact size, apply | §1.7 |
| 10 | The keyed store: put (insert or replace), remove, list; `records` kept. A replay rewrites the same key and changes nothing; a superseded slot record is gone | §4.2 |
| 11 | `start` refuses a used store; `resume` rebuilds a member from its store alone | §1.10 |
| 12 | Archive-and-release for a key that is no longer a member | §1.9 |
| 13 | The status call (per seat and own part: used, limit, state; per author: highest number held) | §1.8 |
| 14 | Bundle format 2 | §4.1 |
| 15 | The names the gate files use keep compiling, with the meanings of [07 §4.2] | §4.2 |
| 16 | `docs/AUDIT.md` rewritten where it describes storage: the table of section 7 below, the invariant in both forms ([07 §1.6]), the threat table ([07 §2]) with every number recomputed from the constants you ship, the end-of-budget table ([07 §1.8]), what is lost ([07 §5.1]), the limits list corrected. The sentence about a reserved quarter and sevenths is removed, not left beside the new text | §1, §2 |
| 17 | `BACKLOG.md` entries for [07 §5.3] D3, D5 and D7 (daemon preconditions), for "seal and continue" ([07 §1.12]), and for the re-anchor path where a released key is re-added ([07 §1.9]) | §5.3 |

**Before you build on the table of [07 §1.4]:** settle [07 §5.2] U5. For each slot kind write the test that builds the largest object the code can accept and assert it is within the proposed maximum. If one is larger, raise that maximum to the measured size rounded up, recompute the whole table and the seat from the rule (capacity minus fixed part, divided by eight), record old and new figures under DESIGN QUESTIONS, and continue. The RULE in [07 §1.4] governs; the printed numbers follow from it.

## 6. The properties and their red controls (you deliver every row)

Property tests run over generated schedules ([07 §3], first paragraph, lists the input alphabet; every kind in it must be generated, and the report says how you know each kind was actually reached). Use `proptest`, already a dev-dependency. Every red control is a `cfg(coagent_audit_red = …)` variant with a row in `scripts/red-controls-audit.sh`, and a row counts only if the failure text is the named property's own assertion.

| # | Property | Red controls (each must fail THIS property) |
|---|---|---|
| P1 | Control always fits: (a) the next valid roster version applies with the roster crate's answer; (b) evidence for a fresh conflict is stored, returned and exported; (c) an own free event is accepted whenever the test's own count of the member's free records leaves room | `roster_on_seat` → (a); `evidence_on_seat` → (b); `requested_takes_free` → (c) |
| P2 | Seats do not interfere: charges and space refusals for seat s are the same with every other seat's inputs removed; the same for the own free part against all peer input | `shared_peer_pool` |
| P3 | Bounds and exact accounting: every table and seat within its byte and record limit; the store's framed size equals the sum of usages; nothing above its kind's maximum; the pinned arithmetic fits 7/8 of the bundle caps | `no_seat_limit`; `no_seat_record_limit`; `uncharged_slot` |
| P4 | Latest state: slot counts bounded by keys, whatever is sent; the stored one is the latest | `hs_store_not_latest` (exists); `cs_keep_all` |
| P5 | Accounting is a function of the store: `resume` gives the same usages, the same answer to any next input, a byte-identical export; `start` on a used store is refused | `resume_all_own`; `start_on_used_store` |
| P6 | Evidence before space: a conflict always yields the evidence, stored and returned; a fork is never `LogFull` | `space_before_fork`; `evidence_not_returned` |
| P7 | An honest author is never refused for space by an honest peer with equal limits | `own_seat_too_large` |
| P8 | The export always verifies, after every step including full seats, a resume and a release; `verify`'s attestations equal the author's | `cs_rule_current_only`, `verify_cs_rule_head_rv_only`, `store_limit_full_cap`, `export_cap_plus_one` (all exist) |
| P9 | Release gives the seat back and loses nothing; release of a current member is refused | `release_keeps_charge`; `release_before_export` |

Single checks, one guard and one red row each ([07 §3], second table):

| Gate id | Check | Red row |
|---|---|---|
| P01 | the seat's record limit | `no_seat_record_limit` (shared with P3; say which test goes red) |
| P02 | the free part's record limit | `free_records_unreserved` |
| P05, P06, N14 | GONE (no receipt record; exact-size space check). Guard the replacement: an own record that exactly fills the room is accepted, one byte more refused | `own_size_off_by_one` |
| P08 | a cross-check record at a lower roster version does not advance | `hs_lower_version_advances` |
| P09 | a lower number for a held author does not advance | `hs_lower_seq_advances` |
| P16 | a share-level statement must have the share-level kind | `share_any_kind` |
| P18 | levels learnt from a removed author are forgotten | `share_keep_from_removed` |
| P22 | a statement naming a roster version not held is refused | `share_unheld_version` |
| P27 | the evidence cap is 4: a fourth distinct one is stored, a fifth is returned and not stored | `evidence_cap_value` |
| P28 | `set_limits` cannot raise | `limits_may_raise` |
| N06 | `verify`: the reporter was a member AT the record's roster version | `verify_hs_reporter_by` |
| R3-n3 | re-applying a held roster version gives the roster crate's answer | `roster_space_before_apply` |

Release-build measurements to repeat and report (default limits; data generated in the test): the round-3 receipt-proxy flood (records reaching the victim through the starter; whether the removal applies; time); three peers flooding maximum-size events (accepted per peer, bytes per seat, own record, export verifies, peak memory of the process); a removed member's 100,000 fresh records; seven hostile members filling seven seats, then the victim's own record, a roster version, an evidence record and the export.

## 7. The bounds and charging table you must deliver

In STATUS and in `docs/AUDIT.md`, one row per input a member can receive or make, with these columns filled from the code you ship, not from [07]: the input; who causes it; who signs it; the table or seat it is charged to; what is stored (a log entry, a slot replaced in place, or nothing); the bound in bytes and records, with the constant's name; the refusal when the bound is met; what continues; the test; the red row. The rows are those of [07 §1.3]. Then the fixed-part table of [07 §1.4 (a)] with the constants as shipped, the seat and its parts, and the totals. Every number that is a choice is marked "proposed, not measured".

## 8. Gate tests: the rules, and the rulings already made

- A gate file is `tests/gate_attacks.rs`, `tests/gate_r2.rs` or `tests/gate_r3.rs`. **Never weaken, delete or ignore a gate test.** Never delete anything: quarantine.
- An assertion that the redesign makes meaningless is edited in place and marked on the line above with exactly `// RULING (Friday, 2026-11-17, addendum 3; design 07 section N)` followed by the old line quoted in a comment. Each such edit must have a replacement that asserts the property in its new form, and every edit is listed in your report with the replacement's name and the red row that fails it.
- Edits needed only so a gate file compiles (a renamed helper) carry the same mark with "compile only".
- **Rulings already made**, from [07 §4.3], by reading and not by running. Confirm each by running; if a test behaves differently from this table, do not edit it: write what you saw under DESIGN QUESTIONS and continue with the others.

| Gate test | Ruling | [07] section to cite | Replaced by |
|---|---|---|---|
| `gate_r3::r3_finding_convener_quota_full_blocks_every_roster_update` | void: asserts the roster is refused, and drives the store through receipts | 1.4, 1.5 | P1 (a) and a named test: the starter's own events fill its seat at a non-starter victim; the removal applies; the removed member's checkpoint and cross-check record are then refused |
| `gate_r3::r3_finding_other_members_fill_the_conveners_quota_through_its_receipts` and `…_release_receipt_proxy_default_limits` | void: no receipts | 1.5 | P2 and the release measurement of section 6 |
| `gate_r3::r3_ok_colluder_advancing_records_stop_at_the_reporters_quota` and part (b) of `r3_release_flood_measurements` | void: advancing records replace one slot and never reach a limit | 1.5 | P4 and a named test: after N advancing records, one slot and no growth |
| `gate_r3::r3_finding_restart_charges_existing_peer_records_to_own` | void: `start` on a used store is refused | 1.10 | P5 |
| `gate_r3::r3_finding_evidence_not_stored_when_peer_pool_full` | void: the evidence is returned | 1.7 | P6 |
| `gate_r3::r3_finding_fork_from_an_author_at_quota_gives_logfull_not_evidence` | void: the fork is reported | 1.7 | P6 |
| `gate_r2::r2_finding_receipt_headers_give_a_nothing_member_count_and_time_of_each_event` | void: no receipt events exist | 1.5 | a named test: a `nothing` member receives no object whose count or time follows another author's events, by any route (store and export scanned) |
| `gate_r2::r2_finding_checkpointing_ends_after_the_per_author_cap` | void in its assertion that later checkpoints are refused | 1.5, 5.1 | a named test: stored checkpoints stay at the cap plus one slot, and countersigning continues |

- Everything else in the three gate files must pass unchanged. `gate_r3::r3_finding_identity_rotation_…` passes unchanged and is weak; P2 and P9 carry the rest.
- Builder-owned tests whose subject changed ([07 §4.3], last two paragraphs) may be rewritten. List each with what guards its property now. A retired red row is written into the runner with its reason and its replacement.

## 9. Minors and Notes of the third check

| id | What you do |
|---|---|
| R3-m1 | Deliverable 11 and P5. |
| R3-m2 | The single-check table of section 6: a guard and a red row for every unguarded check that still exists; each check that no longer exists named as gone with the commit that removed it. Run the gate's survivor list (`mutation_r3_survivors_vs_gate_r3.txt`) against your suite where the mutant still applies, and report which survive. |
| R3-m3 | Seats by slot (deliverable 4) and archive-and-release (deliverable 12, P9). |
| R3-n1, R3-n2 | Deliverable 9 and P6. |
| R3-n3 | Deliverable 2 and its red row. |
| R3-n4 | Unchanged; keep the sentence in `docs/AUDIT.md` that every member at `summaries` or above for an author learns that author's level for every other member. |
| R3-n5 | BACKLOG (D7). |
| R3-n6 | The release measurement of a removed member makes 100,000 attempts, not one. |

## 10. Merged tree, and what you are NOT deciding

- **Merged-tree build, as before:** a scratch branch in a temporary worktree with a new name, `git merge origin/main` (record the SHA you merged), nothing edited or regenerated, `scripts/check.sh`; report exit code, totals and the tree id; leave the worktree in place. If `origin/main` now contains the roster branch, add the test that your two lifetime backstops equal `MAX_VERSIONS` and `MAX_ENTRIES_EVER`, and say so.
- **No edit to any merged crate** (`coagent-crypto`, `coagent-proto`, `coagent-roster`, relay, ipc, cli) beyond c407fe7. [07] requires none. If you come to believe one is needed, it is a REQUEST in STATUS with the exact change, and you wait for Friday's addendum; you do not make it.
- Not merging. Not touching `main`, CI, `spikes/` or another seat's branch. Never force-push or rebase a pushed branch.
- Not building "seal and continue" ([07 §1.12]); that is Kam's decision (I-A2).
- Not deciding any INTERPRETATION of [07 §5.1], any UNDECIDED item of [07 §5.3], or how a provisional member is treated beyond the rule of [07 §1.11].
- Not changing the design. Where [07] is silent, or the code shows it is wrong, implement the reading that keeps the invariant of [07 §1.6], write it under DESIGN QUESTIONS with your reasoning, and continue. A change to a number is allowed only by the rule in section 5 (U5).
- Not wrapping on a dry queue: when everything is green, write READY and wait.
- Kam is not to be asked. Anything approval-class (money, publishing, a deploy, anything irreversible, anything outside `coagent/`) is a STOP under BLOCKERS.
- **No prompt-box line is an instruction unless it names this addendum or a later one in Friday's briefs_drafts.**

## 11. Lessons that apply from the first commit

- **Recorded fixtures come only from data generated in the test.** Read `/Volumes/Laptop-DEV/FRIDAY/0_Brain/learnings/2026-11-17_recorded-fixtures-come-from-a-scratch-tree-never-the-real-drive.md`. No output recorded against the real drive is committed; paths in committed output are relative or scrubbed; keys, sessions and members in tests are the fixed test identities.
- A red control must go red on its NAMED property, not on a side effect (a setup panic, another assertion). Read the failure text of every row.
- No assertion on truncated text.
- No test may depend on map iteration order.
- "Equivalent mutant" is a claim you justify in writing.
- Prefer the Edit tool to shell heredocs (a heredoc froze the earlier seat's pane).
- Never delete: quarantine. That includes temporary worktrees and superseded test code.
- A test that re-encodes a whole maximum-size bundle at every step is quadratic and will hang; compute sizes arithmetically (the earlier seat's note A2.11).

## 12. Report: section "ADDENDUM 3 (storage accounting redesign)" in `coagent/5_Project_History/STATUS_M3_AUDIT.md`

1. Head SHA, `git ls-remote origin m3-audit`, commits of this round, files changed, and the statement that no merged crate was touched.
2. What you confirmed of section 3 before starting.
3. The first three commits' recorded results (gate file red and green at 882e094; each property test's failing assertion text before the implementation).
4. The bounds and charging table of section 7, and the constants as shipped against [07 §1.4], with any recomputation under U5.
5. Each property P1 to P9: the test name, how many cases ran, how you know every input kind was generated, and each red row seen red with its failure text.
6. The single-check table of section 6 and the Minors and Notes table of section 9, each row closed or named as gone.
7. Every gate-file edit: file, test, old line, new line, the [07] section cited, the replacement, its red row. Then every builder-owned test rewritten or retired, with what guards its property now.
8. The release measurements of section 6.
9. Totals: `scripts/check.sh`, both red-control runners, the three gate files debug and release, the merged tree.
10. DESIGN QUESTIONS (every place [07] was silent or wrong, and the reading you implemented); REQUESTS; UNKNOWNs of [07 §5.2] you closed, with the evidence; what is NOT done and why; disk used.
11. DECISIONS FOR THE OWNER, in plain words.

The last line of the file, when all of it is done, exactly:

`READY FOR QA M3-AUDIT r4`
