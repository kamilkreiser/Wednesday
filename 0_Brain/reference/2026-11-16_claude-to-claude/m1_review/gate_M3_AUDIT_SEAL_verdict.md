VERDICT: GO WITH NOTES — head 841c4459e5cdda0637e4df2cdf77ba133f51bd18

# Gate M3-AUDIT-SEAL (tier 1, the one independent check): `coagent-audit`, branch `m3-audit-seal` at `841c4459e5cdda0637e4df2cdf77ba133f51bd18`

Independent check, 2026-11-20. Findings only. I fixed, committed, pushed and merged nothing, and wrote nothing in the project folder (git read verbs only there). Every write went to `/private/tmp/claude-501/qseal`, the session scratchpad, or this folder. My test files are in `gate_audit_seal_tests/` beside this file.

- **Heads (TESTED).** At the start, `git ls-remote` showed `m3-audit-seal` = `841c4459e5cd…` and `main` = `8b8c6c755db6…`, both as briefed. Merge-base of the branch with `8b8c6c7` = `8b8c6c7`.
- **MAIN HAS MOVED SINCE (TESTED, read again at the end):** `main` is now `32beb563837341560b908d9ba5b0a60de240d860`. The M3 DEPUTY lane merged 9 commits on top of `8b8c6c7`: `crates/coagent-roster/**`, `docs/ROSTER.md`, `scripts/red-controls-roster.sh` and `BACKLOG.md`. `coagent-audit` depends on `coagent-roster`, so see QS-0 and the merge condition below.
- **Marks.** TESTED = I ran it. READ = I read the source at the head. A builder figure is cited only where my own run matched it.

## BLUF (for the owner, in plain words)

1. **Filing the log away and carrying on works as designed, and it is safe at every point I could stop it.**
   - Nothing is lost, no number is signed twice, and every file checks out on its own and in a set.
   - I stopped the filing after every single disk write, including a second filing over leftovers from a first one that was interrupted (26 stop points). Each time the restart came back either exactly as before or exactly as after, and only the right anchor accepted it (TESTED).
2. **Only you decide when to file the log away (your ruling I-S1 = a), and each member files on its own schedule (I-S6 = a). The code is built that way.**
   - No message from anyone else can start a filing.
   - Another member filing their own log away changed nothing on your side, and their later messages were still accepted (TESTED).
3. **The builder's figures reproduce on the final head.**
   - The full check passes: 1,150 tests passed, 0 failed.
   - All 174 deliberate-break controls go red, each on its own named property, including the 20 new ones.
   - The big generated test passes 1,024 cases at a seed I chose (137).
   - The 17 protected files are unchanged, byte for byte.
4. **One test fault (QS-1, Minor).** At another seed of mine (91), the generated test fails on a builder-added extra check, not on a seal fault. That check treats an old, already-known behaviour (a member who is released and then re-added can have their first message accepted again) as if a filing caused it. I showed the same thing happens on the code from before this build, with no filing at all. With only that check narrowed, seed 91 passes all 1,024 cases. The test should be corrected in a follow-up. The product is not wrong here.
5. **Merge: GO WITH NOTES, with one condition (QS-0).** Your project's main branch moved after this build. Merge the current main into the branch and re-run the full check before or as part of the merge. I trial-merged it: there are no conflicts, and the audit tests on the merged tree are reported below.

## Findings

| id | sev | what | input that shows it | exact output seen | file:line |
|---|---|---|---|---|---|
| QS-0 | Note (merge condition) | `main` moved from `8b8c6c7` to `32beb56` (M3 DEPUTY: `coagent-roster` src and tests, `BACKLOG.md`), and `coagent-audit` depends on `coagent-roster`. The branch's own check and runner figures are on the `8b8c6c7` base. A trial merge (`git merge-tree`, in the scratchpad) is clean. I ran the whole `coagent-audit` suite plus clippy on the merged tree: `cargo test --locked -p coagent-audit` 40 result lines, 306 passed / 0 failed / 14 ignored, and `cargo clippy -p coagent-audit --all-targets -- -D warnings` exit 0 (`exit=0`, 11:08 → 11:22). A full `check.sh` on the merged tree was NOT run by me (time and heavy slots). | `git ls-remote origin main`; `git merge-tree --write-tree 32beb56 841c445` | `32beb563…`; tree `98775b31a8cf…`, no conflict | — |
| QS-1 | Minor (harness fault; property red at an uncommitted seed) | `seal_props`' extra check "replay" (not one of §6.2's I1-I5/S1-S9) picks `pre_seal.first()`, which can be an event of a key V released with no tombstone and the starter later re-added. Re-accepting that event is the pre-existing A-m6 behaviour (`archive_and_release` drops a chain with no tombstone, `session.rs` `None => self.peers.remove(key)`; DQ-S6), not a seal fault. **Product (TESTED):** with NO seal, base `36537eb` and head both accept X's pre-release event 1 after release + re-add, store 3 → 4 records (`qa_readd.rs`). **Harness:** with only the replay candidates narrowed to keys never released (`qa_seal_props_instrumented.rs.txt`), seed 91 passes 1,024 (24 replays skipped as A-m6). Fix for a follow-up: filter released keys out of `ReplayPreSeal`'s candidates, or assert A-m6's behaviour for them. | `SEAL_SEED=91 SEAL_CASES=1024 cargo test --release --test seal_props` (pristine 841c445) | `Test failed: Case failed: seal property replay: a pre-seal object replayed after the seal changed the store [step 29 of the run keeping None: ReplayPreSeal(0)]` (126 s, case ≈300). Diagnosis line: `author idx Some(2) seq 1 got Ok(Accepted…); chain before None; member now true; … G starts [(false, 7)]; added [PeerEvent(2) … n: 1]`. Case ops: `Roster{kind:1}` (remove) step 4, `Release` step 16, seal step 17, `Roster{kind:2}` (re-add) step 28, `ReplayPreSeal(0)` step 29 | `tests/seal_props.rs:1155-1192` |
| QS-2 | Note (ruling on the 841c445 harness change) | I2 now compares only while both runs have the same limits in force. **Ruled acceptable** (see Ruling 4). The diagnosis is right in substance and slightly broader than STATUS states: every truncation I instrumented begins at V's own `Lower` refused `LogFull` in one run only (36 of 38 at seed 91), or at the limit re-offer after a `Resume` (1) or after a stopped commit (1). That is the ruled limit rule, not seal and continue. Cost: about 3.7 % of compared cases are compared only up to the divergence; in 3 of 1,024 cases at seed 91 the seats then differed, unexamined. | instrumented `seal_props`, seed 91, release 1,024 | `QA I2 limits first differ after op: Lower: 36; Resume: 1; SealCommitStopsAt: 1; QA I2 seats differ after the limits diverged: 3; QA Lower refused: LogFull: 104` | `tests/seal_props.rs:2071-2110` |
| QS-3 | Note (surviving mutant, argued equivalent in safety) | Mutant m5: normalisation KEEPS a newest-checkpoint slot whose number equals the start (`>` → `>=`). All three seal test files stay green. Effect: one extra record in that author's set-aside LatestHead slot (fixed part, not any seat), equal to the anchor. It is never exported (`export_records` keeps peer checkpoints only above the anchor), and resume ≡ live still holds because both use the same rule. No safety property changes. But no test pins design 10 §4's row "Fixed: newest-checkpoint slots: none for authors cut". | `mut.py m5_latest_kept_at_start` (`segment.rs` `Record::PeerHead(h) => h.author_seq > *n`) | seal_props 48 cases `ok`; seal_unit 28 ok; seal_verify 11 ok | `src/segment.rs:189-195` |
| QS-4 | Note | STATUS §7 says every final run was repeated on 841c445, but lists only the 1,024-case figures for 841c445. My runs at 841c445 settle it: they reproduce the 6fa9a94 figures exactly. | `scripts/check.sh`; `scripts/red-controls-audit.sh` (fresh target and logs) | `CHECK OK … exit=0`, 148 result lines 1150 / 0 / 21; `rows: 172 cfg rows + 2 source-mutant rows`, 174 RED, 0 NOT-RED, `GREEN: 306 tests ok`, `RED CONTROLS OK`, `exit=0` | STATUS §7 |
| QS-5 | Note | `docs/AUDIT.md` §1B still lists I-S1 and I-S6 as "INTERPRETATION, built as stated, open for the owner". You ruled both "a" on 2026-11-20 07:08, matching what is built. The docs are stale on the ruling only, not on the behaviour. | READ | — | `docs/AUDIT.md:551-567` |
| QS-6 | Note | The brief listed a `Record::Segment` arm in `a3_props.rs` `kind_max`. It was not added (deviation (d)): an omitted permitted edit, not an edit beyond the closed list. The wildcard `_ => 4 + 65_535` covers it, and `a3_props` never stores a Segment record. | READ | — | `tests/a3_props.rs:69-79` |
| QS-7 | Note | The property's commit stop index cycles 0-3, so `seal_commit` call indices ≥ 4 are reached only by the unit tests: A3 and A4 (10 calls each) and my probe (a second seal over garbage, 25 calls, all 26 stop points). | READ + TESTED | `qa second seal: 25 store calls; segment 2`, every j passed | `tests/seal_props.rs` (stops), `qa_seal.rs` |
| QS-8 | Note | `restore_from` takes the Segment record's `own_start` without checking its signature. A disk attacker who forges it is caught by the anchor (R-A1) or by `verify` of the next export (format-3 check 1 checks the signature). This is the stated limit of plain `resume` (R4-m3). | READ | — | `src/chain.rs` `restore_from` |
| QS-9 | Note | `verify_segments(&[Bundle])` holds every file the caller passes; "at most two at once" applies to the pairwise comparison only. This is the design's API as written (design 10 §8). | READ | — | `src/bundle.rs` `verify_segments` |

No Blocker. No Major: every property holds under my attacks, every guard is red on its own property, no protected file changed, every edit is inside the closed list, and every figure the merge relies on reproduces.

## Rulings, items 1-9

**1. Scope and protected files (TESTED). Clean.**
- `git diff --stat origin/main...841c445`: 20 files, 5,525 insertions, 128 deletions. Every path is in `crates/coagent-audit/**` (src, build.rs, `Cargo.toml`: three `[[test]]` entries only, tests), `docs/AUDIT.md`, `BACKLOG.md` or `scripts/red-controls-audit.sh`.
- `git diff --stat origin/main HEAD -- Cargo.lock Cargo.toml` is empty. No new dependency.
- `domain.rs` is not in the diff, and `AuditDomain::ALL: [AuditDomain; 5]`, so there are still five signing domains.
- **17 protected files:** sha256 at the head equals `git show 36537eb:…` for all 17 (15 also equal the brief's listed values; `common/mod.rs` 3a9b6503…, quarantine 4398b05a…).
- **`tests/bundle.rs`:** exactly the one ruled arm, `Record::Segment(_) => FieldClass::Segment,` with the ruling marker and the `// old:` line, and nothing else.
- **`a3_props.rs`:** only `FIXED_SLOTS` 540 → 541 and `Evidence` 4_100 → 3_972, each with the old line quoted.
- **`a3_unknowns.rs`:** only the new U-S1 test.
- **`red-controls-audit.sh`:** 20 appended rows, none edited.
- **BACKLOG:** additions, plus one line closed in place in the file's form (`- [ ]` → `- [x] … — CLOSED in commit 8462a36…`). No other line was removed.
- The new `tests/seal_common/mod.rs` is inside the owned crate.

**2. Gate figures at 841c445 (TESTED). Reproduced.**
- `check.sh` ran 08:13 → 09:14, `exit=0`, `CHECK OK: fmt, clippy, test, deny all passed`, 1150 passed / 0 failed / 21 ignored over 148 lines.
- The audit runner, with a FRESH target and log directories, ran 09:14 → 09:46: 174 RED, 0 NOT-RED, `GREEN: 306 tests ok`, `RED CONTROLS OK…`, `exit=0`.
- The builder's STATUS lists no 841c445 figures for these two runs (QS-4). Mine match its 6fa9a94 figures exactly.

**3. My release 1,024-case runs (TESTED).**
- **Seed 137, pristine harness: PASS** in 367 s. Every required reach count is above zero:
  - S5 states: full seats 380, full free part 486, N1's state 175, a checkpoint owed 152, V off the roster 680;
  - commit stops at call 0, 1, 2, 3: 221, 235, 159, 116;
  - at least three segments: 833 cases;
  - a peer seal observed by V: 1,073 by an event, 181 by a checkpoint;
  - I2 compared 882 times (38 diverged); stale plans 60; garbage left 301; pre-seal replays 278.
- **Seed 91, pristine harness: FAILS** on the extra "replay" check at about case 300 (QS-1). With only that check narrowed: **PASS** at 1,024 in 393 s; I2 compared 897; three or more segments 801; S5 states 385 / 440 / 173 / 153 / 641; stops 205 / 244 / 139 / 73.

**4. The I2 harness change at 841c445: ACCEPTABLE. The property is still strong enough.**
- **Diagnosis right (TESTED):** every divergence starts at a limit change that one run refuses. See QS-2.
- **Red control `seal_cut_by_other_seat` still red** at the default 48 cases, on I2's own text: `seal property I2: after step 41 (SealCommitStopsAt(2, 0)) seat 0's charges depend on other seats' inputs: (0, 0) vs (2863, 4).`
- **My seal-specific I2 mutant m1 is caught** at 48 cases by the weakened I2. The mutant cuts a peer only when every held author has a checkpoint, so whether seat s is emptied depends on other authors. Output: `seal property I2: after step 32 (SealCommitStopsAt(2, 0)) seat 0's charges depend on other seats' inputs: (2046, 3) vs (0, 0).` (`session.rs` `seal_export`).
- **Residual:** comparison stops at the first limit divergence (about 3.7 % of compared cases).
- **Better, for a follow-up:** apply the watched run's accepted limits to both runs instead of stopping the comparison.

**5. R2 release crash order (TESTED + READ). Holds.**
- The `release_tombstone_last` branch (`session.rs` `archive_and_release`) is the base order verbatim: delete from the index in key order, then the tombstone. I compared it with `git show 36537eb:…session.rs:1944-1972`.
- Its runner row is red on the test's own text: `R2 release stop (checkpoint inside the run): the store stopped after call 1 of 9 cannot be resumed: Receive(Gap { expected: 1, got: 2 })`. This equals STATUS's recorded failure at 36537eb.
- `release_before_export` is still red on its own text: `P9: a record the release deleted is not in the returned file`.
- The R2 test stops at EVERY call index of four scenarios (9, 5, 8 and 6 calls, plus the pre-release store) and passes.
- My mutant m3 (oldest first after the tombstone) is caught by the R2 test.

**6. Seal safety core: my probes (TESTED, `qa_seal.rs`, all 5 pass).**
- (a) **A peer seals invisibly, twice:** V's anchor is unchanged by X's seal. V accepts X's later events and checkpoints, V's export verifies, resume ≡ live (export and anchor), and X's own export verifies. V seals between X's seals.
- (b) **Second seal over the first seal's garbage (collection failed), stopped after every store call (j = 0..25):**
  - j = 0 gives `Err(Store)`, the resumed export equals the pre-seal member's, and only the pre anchor accepts.
  - j ≥ 1 gives `Ok`, the resumed export equals the clean post-seal member's (reference: a member resumed from the same pre-seal store, whose plan and post anchor equal the live ones), and only the post anchor accepts.
  - No numbered record is lost: each is in the logical store or in the file.
  - A third seal leaves physical == logical, and its export verifies.
- (c) **Stale plans:**
  - Each store-changing step between export and commit is refused `SealStale` and writes nothing: a peer event, a peer checkpoint beyond held events (slot-only change), an own event, an own checkpoint, a countersignature arriving.
  - The same plan committed twice gives `SealStale`.
  - A countersignature of the seal point arriving AFTER commit is accepted, exported, and verifies (S6).
- (d) **Normalisation:** idempotent. Independent of listing order. Plain stores (no Segment record) normalise to themselves.
- (e) **`verify`:**
  - format 3 with no Segment record → `Meta "format 3 without a segment record"`;
  - format 2 with one → `Meta`;
  - a plain bundle relabelled 3 → error;
  - format 4 → error;
  - a peer start with a changed number → `Segment` (signature);
  - format 3 reports `first_seq = n₀+1`, `anchor = n₀`.
- (f) **`verify_segments`:** a broken `prev` → `Segment "segment does not link to the previous segment"`; a reordered set → refused. Dropped evidence is covered by the red row `verify_seg_no_evidence_superset` (RED) and `seal_verify` row 9.
- (g) **Format 2 byte for byte (`qa_fmt2.rs` + `qa_fmt2b.rs`).** Events carry random salts, so I fixed the inputs: 12 bundles exported by 36537eb, parsed and re-exported with `export_records` from their own records, are byte-identical on 36537eb AND on 841c445 (12 / 12, sha256 equal three ways). They also verify on the head.
- **Builder's deviations, all ACCEPTABLE:**
  - (a) newest-checkpoint slot dropped at or below G's start only: it keeps pre-build stores unchanged (the protected `gate_r4` P3 is green). Its looser variant is QS-3.
  - (b) format/content mismatch reported as `Meta`: it is a format fact.
  - (c) release deletes newest first, read from the store: needed (m3).
  - (d) no `kind_max` arm: QS-6.
  - (e) A15 refused at the anchor slot first: still `Missing`, still refused.
  - (f) default of 48 cases: needed so `seal_cut_by_other_seat` acts.
  - (g) I2 under equal limits: Ruling 4.
  - (h) share levels kept across a seal in memory; after a restart only levels with held statements come back. Fail-safe: an unset member is `ShareLevel::Nothing` (`tiers.rs:21-24`), and the docs state it.

**7. Budget constants (TESTED).**
- `budget_the_segment_slot_leaves_every_seat_unchanged` printed `EVIDENCE_SLOT_MAX 3972; SEGMENT_SLOT_MAX 16384; FIXED_BYTES 17940335; FIXED_RECORDS 541; SEAT_BYTES 5097490; SEAT_RECORDS 28604; MAX_ANCHOR_SLOTS 541` and `fixed part + eight seats = 58720255 B / 229373 records of 58720256 / 229376`.
- **U-S1:** `the largest Segment record is 14065 framed bytes (canonical 14065) of the slot's 16384; margin 2319`. The stated 1,024-byte margin holds.
- **U-S2:** evidence 1523 / 3972.

**8. Red controls (READ + TESTED) and my own mutants.**
- **Each of the 20 `cfg` branches breaks only its named behaviour (READ):**
  - `seal_cut_by_other_seat`: the cut comes from a cross-check entry;
  - `segment_uncharged`: the Segment slot is not charged;
  - `resume_no_normalise`: the physical listing is used;
  - `seal_keeps_old_attestation` and `seal_start_charged_to_free`: normalise keeps the record, and `restore_from` skips it so the rebuild still succeeds;
  - `verify_seg_own_from_one`: the report only;
  - `seal_no_stale_check`;
  - `seal_delete_first`: collection before the put;
  - `seal_cut_plus_one`;
  - `verify_seg_no_link`;
  - `verify_seg_no_evidence_superset`;
  - `seal_restart_own_at_one`;
  - `seal_on_receive`;
  - `seal_needs_checkpoint`;
  - `seal_space_checked`;
  - `seal_changes_next_prev_hash`;
  - `seal_resets_limits`;
  - `anchor_before_normalise`;
  - `seal_no_collect`;
  - `release_tombstone_last`: the base order.
- **All 20 rows ran in my runner (TESTED),** including `seal_start_charged_to_free` → `(d1): own record OwnHead 2 at or below the own start 2 is charged to the own seat`, `resume_no_normalise` → `I4: the resumed member's anchor differs`, and `anchor_before_normalise` → `S8: the pre anchor accepted the store stopped after call 1 (committed true)`. Each is red on its own invariant's text.
- **My 7 source mutants** (exact-once replacement, `qa_mutants.py.txt`):

| mutant | where | killed by |
|---|---|---|
| m1 cut needs all peers | `session.rs` seal_export | `seal_props` I2 (48 cases) |
| m2 attestations of the own start dropped | `segment.rs` normalise | `seal_props` I3 `store usage (9318, 8) is not the logical store's (7314, 4)`; `seal_unit` A17 |
| m3 release oldest first | `session.rs` archive_and_release | `seal_unit` R2 test |
| m4 own link unchecked | `bundle.rs` link_pair | `seal_verify` row 7 |
| m5 newest-checkpoint slot kept at the start | `segment.rs` normalise | **SURVIVED** (QS-3, argued equivalent in safety) |
| m6 stale check compares numbered runs only | `session.rs` seal_commit | `seal_props` S1 `a plan made before the store changed was committed` (`seal_unit` A2 alone does not catch it) |
| m7 peer start signature unchecked | `bundle.rs` verify | `seal_unit` A12 (`seal_props` does not catch it) |

**9. Names scan (TESTED).**
- Over the 5,525 added lines of `git diff origin/main...841c445`, case-insensitive, for `/Users/`, `/Volumes/`, `/home/`, the owner's first and last names and both client names (the brief's list): **0 hits**.
- Positive control: a planted line with a volume path and a surname is found (1 hit).
- The coordinator's role name "Friday" appears twice: the ruling marker addendum 1 mandates, and §1B "Friday's ruling R1".
- The commit author field is the repository's configured identity (not an added line).

## What I ran (all at 841c445 unless named)

Each heavy run was started under a gate on the brief's exact count pattern plus my own test runs, with a start mutex (`qa_waitrun.sh.txt`). At most two heavy runs were ever live machine-wide. One heavy run of mine ran at a time, except a short probe run while my runner held the other slot.
- `check.sh` (above).
- `red-controls-audit.sh`, fresh `COAGENT_AUDIT_RED_TARGET` and `COAGENT_AUDIT_RED_LOGS` (above).
- `seal_unit` (28 + 1 ignored), `seal_verify` (11) and `a3_unknowns` (5), all pass. A3: 10 store calls; A4: 10 snapshots; R2: 9 / 5 / 8 / 6 calls.
- Release seal_props: seed 91 pristine (FAIL, QS-1), seed 91 narrowed (PASS), seed 137 pristine (PASS), plus one instrumented seed-91 diagnosis run.
- 7 mutants × (seal_props 48 cases, seal_unit, seal_verify), in a separate copy of the tree.
- Probes `qa_seal.rs` (5), `qa_fmt2.rs` / `qa_fmt2b.rs` on 36537eb and 841c445, and `qa_readd.rs` on 36537eb and 841c445.
- A trial merge onto the new main, and the audit suite plus clippy on the merged tree (QS-0).

## NOT TESTED

- A full `check.sh` and the audit runner on the tree merged with the new `main` `32beb56` (QS-0): the merge condition.
- The builder's own three seeds (committed, 7, 200) at 1,024. I ran two other seeds instead, as briefed.
- Linux and Windows. Real on-disk crash timing: stops are simulated by a store that refuses calls.
- Disk used by this check: about 3.1 GB under `/private/tmp/claude-501/qseal`. No processes of mine are left.
