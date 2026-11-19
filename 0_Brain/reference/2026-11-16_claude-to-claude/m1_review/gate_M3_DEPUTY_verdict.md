VERDICT: GO WITH NOTES — head 8aebed83fc5baafbccb3544fb4fe10ac1d902fb4

# Gate M3 DEPUTY (tier 1, independent): branch `m3-deputy` at `8aebed83fc5baafbccb3544fb4fe10ac1d902fb4`

Base `origin/main` `8b8c6c755db66a1c481d9719707c3cdc924fb70c` (merge-base READ). Remote head READ: `git ls-remote origin m3-deputy` = `8aebed8…`. Ruling checked against: card `general-c2c-deputy-powers-1117` = a, "Build the small deputy as described". Gate run 2026-11-20. Marks: TESTED = I ran it; READ = I read the source at the head.

## BLUF (for the owner)

1. **The deputy has no power beyond your ruling.** It cannot sign a member list, remove anyone, change the limit, end the session or name another deputy, and only you sign the list (TESTED: clean-clone check, 102 red controls, my own 17 code mutations, 5 probes).
2. **Every admission the deputy signs is checked by every member** against the seven rules, in order; forged, replayed, out-of-order, old-epoch and other-session admissions are refused and nothing is stored (TESTED).
3. **One thing you should know (D-1):** when you "drop" someone by renewing the deputy's seats, the SAME deputy can let them straight back in under the renewed seats, on a fresh proposal from any guest. Withdrawing the deputy stops it; renewing does not. Sentence 3 ("anyone you do not keep leaves the session") is true at that moment only.
4. **One thing to decide before the daemon wires this in (D-2):** after ANY change you make to the member list, people who join later cannot check earlier admissions, so the deputy's newcomers can no longer start and members' views drift apart until you renew. Safe (it refuses, never accepts), but it breaks the deputy path in ordinary use. The builder raised it (design question 2, BACKLOG).
5. Notes D-3 to D-7 are test-strength and bookkeeping items; none is a merge blocker.

## Findings

| id | severity | what | input | exact output | file:line |
|---|---|---|---|---|---|
| D-1 | Minor (design, owner awareness) | "Drop" is not sticky: a provisional member dropped by a grant renewal can be re-admitted at once by the same deputy. Not a widening (it still needs another guest's proposal and a set-aside seat), but the brief's remedy "the starter renews the grant" (hostile-deputy table, "use up the seats") does not stop the same deputy. | Probe G1: admit v4; starter `next_with_deputy` same holder, seats [5,6,7]; same deputy admits v4 again on a new proposal by P | `rep.dropped == [v4]`, then `Ok(Accepted)`; `is_provisional(v4)` true | `deputy.rs:1238-1341` (rule 5 has no "dropped" memory); `gate_deputy_tests/qa_deputy_gate.rs` g1 |
| D-2 | Minor (liveness; builder's DQ2 + BACKLOG) | Rule 6 read literally ("a version this member holds"): after any unrelated starter version, a provisional newcomer cannot start and a later joiner refuses earlier admissions, so views differ (handshake fails) until the grant is renewed. Conservative: never accepts what it cannot check. | G3: admit v4 (proposal at v3), unrelated role change v4, admit v5 (proposal at v4), `start_provisional(v5, r4, [a0,a1])`. G4: starter invites v9 at v4; v9 offered a0 | G3: `Err(Admission { index: 0, error: ProposalVersionNotHeld })`. G4: `Err(ProposalVersionNotHeld)`, view hashes differ | `deputy.rs:1322-1324`, `:1155-1161`, `:934-935` |
| D-3 | Minor (R3-M1 neighbour, mitigated) | Evidence is kept per SESSION, first come (brief over design, DQ1). A first deputy's four forks fill the store; a later deputy's fork is counted, not kept, and the kept pairs no longer verify against the current roster. Nothing is blocked, and the `Conflict` error carries the evidence to the caller (it verifies). | G2: v1 forks 4× at seq 0; grant moved to v2; v2 forks once | `evidence_kept: 4, evidence_unkept: 1`; returned `ev.verify(roster) == Ok(v2)`; every kept pair `verify(current) = Err` | `deputy.rs:1129-1141` |
| D-4 | Minor (property strength) | The generated property's alphabet never reaches several admission refusals at the member: a deputy-forged guest proposal (`BadProposalSignature`), a removed candidate (`CandidateRemoved`), `ProposerIsCandidate`, `ProposerIsStarter`, `CandidateKeyInUse`, `ProposalBeforeEpoch`, `BadCandidate`, `FieldLimit`; members other than the deputy never sign roster versions. The unit tests and red rows do cover these rules; the six invariants would not catch them anyway. | 1,024 cases × 40 steps, release, committed seed and gate seed `0x6A7E00DE9D7A1120` | count 0 for each class listed, in both runs | `tests/deputy_props.rs:744-836`, `:1052-1089` |
| D-5 | Minor (test gap) | The builder's added rule `CandidateKeyInUse` (DQ4) has no test: removing it leaves every deputy test green. | gate mutant M03 (`if in_use` → `if false && in_use`) | `SURVIVED` | `deputy.rs:1276-1288` |
| D-6 | Note | `check_unsigned`'s seq/prev lines are equivalent by construction (`approve` builds seq/prev from the same view); not claimed as equivalent in the docs. | gate mutant M07 | `SURVIVED` | `deputy.rs:1358-1367` |
| D-7 | Note | `admit` (unchanged, as the brief requires) still returns `Ok` for `deputy.admission` from any roster member. No power gained (admissions are signature-checked), but the daemon must switch to `admit_view` (REQUEST 3) for the role rule to hold. | READ | n/a | `lib.rs:1103-1143`; `deputy.rs:1399-1444` |

No Blocker. No Major: no deputy power beyond the ruling, no forged or replayed admission accepted, no admission surviving voiding, no starter act blockable by deputy-filled storage, every red control red on its property, no existing guard changed in a normal build.

## Rulings, items 1-9

1. **ONE SIGNER — HOLDS.** `is_roster_signer` and `check_roster_signer` change only under `cfg(coagent_red_roster = "deputy_signs_roster")` (`lib.rs:517-545`, READ); `RosterChain::start` pins the starter key. Signed bytes: roster = `Roster` domain over `canonical(body)` (begins `{`); proposal = label `coagent-roster-proposal-v1` ‖ 0 ‖ body; admission = label `coagent-roster-deputy-admission-v1` ‖ 0 ‖ body (`deputy.rs:442-449`); prefix-free, verified only through their own functions; audit domains distinct. No path from an admission to the roster, `removed`, `cap`, `session.end` or another grant (READ; `admit_view` routes `roster.update`/`session.end` through `is_roster_signer`, `deputy.rs:1426`). TESTED: red rows `deputy_signs_roster` (D5.1-5 and A0-6.1 (a)) RED; property: deputy-signed versions 566-572 per run, all refused `BadSignature`.
2. **ADMISSION RULES — HOLD.** Rules 0-7 in order, sig (2) before seq (3), so only the deputy can cause evidence; same body twice = `Unchanged`, a different body at a held seq = `Conflict` (`deputy.rs:1175-1231`). Withdrawn deputy, removed/member/provisional candidate, unset or taken seat, raised role, proposals by deputy/candidate/starter/observer/provisional/non-member: each refused (READ; TESTED by the builder's tests in the clean-clone run and by my mutants M02, M09, M26, M27 killed). Note D-2 on rule 6.
3. **VOIDING and KEEP — HOLD.** Any epoch change or withdrawal clears the admissions (`deputy.rs:1046-1064`); epoch changes are forced by the validator for holder, seats and `cap` (`deputy.rs:150-172`); epochs are version numbers, so never reused. `dropped` = old provisional keys not on the new roster. `next_keeping` puts the kept key in its seat; a grant that still sets that seat aside is refused. TESTED: mutants M01, M05, M15, M16 killed; property voiding 514-530, keep 234-241. Note D-1.
4. **THE VIEW — HOLDS.** No admission: the roster's hash and maps (`deputy.rs:679-717`); with admissions `SHA-256(view-v1 ‖ 0 ‖ roster hash ‖ head)`; roster member wins; BTreeMap/BTreeSet only. TESTED: both view red rows RED; invariant (f) held over 2,048 cases.
5. **ROLES — HOLD.** Provisional members refused the five kinds; `deputy.admission` only from the current holder; result from starter or holder; `may_approve` unchanged (`intake.rs`, READ); `ProposalIntake::new` refuses the deputy (red row `starter_intake_accepts_deputy` RED). Mutants M18, M25 killed. Note D-7.
6. **STORAGE (5.3) — HOLDS.** `apply_roster` calls `RosterChain::apply_with_report` with nothing from admissions or evidence (`deputy.rs:1029-1075`); the starter's intake reads only the roster's grant; the deputy's intake has its own records and per-proposer quota. TESTED: `item18_*` pass; red rows `admissions_share_roster_store`, `evidence_unbounded` RED. Note D-3.
7. **THE GENERATED PROPERTY — ADEQUATE, with D-4.** Alphabet: deputy (valid, forged by others including a former holder, replayed, old epoch, other session, gap, wrong prev, conflicts in bursts, bad proposer/seat/role, deputy-signed rosters), members (both intakes, valid and not), starter (grant change/move/withdraw, keep, `cap`, invite/remove, gap/fork versions, replays), relay (drop, delay, duplicate, reorder). Invariants (a)-(f) are addendum 0 §6 item 1's six; each A0-6.1 row RED on its own text (TESTED, see table in the runner log). Reach classes are counted at real outcomes (36 asserted > 0). TESTED: release, 1,024 cases, committed seed `0xD3B07E5EED000001`: pass, 12.5 s, reach counts identical to the builder's STATUS; gate seed `0x6A7E00DE9D7A1120`: pass, 12.4 s.
8. **NOTHING EXISTING MOVED — HOLDS.** Protected files (addendum 0 §4), `Cargo.toml`, `Cargo.lock`, `red-controls-core.sh`, `docs/CRYPTO-GLUE.md`, `spikes/` and the crypto, proto, daemon, audit, cli, relay crates: `git diff --stat 8b8c6c7 8aebed8` EMPTY (TESTED). Only pre-existing test file touched: `tests/api_stability.rs`, additions only (no removed line). Old red rows: roster runner 60 old + 42 new = 102 RED, 4 equivalence GREEN; core runner 65 RED, green 296 (TESTED). No new dependency. Workspace compiles and passes: daemon and audit use the crate unchanged (TESTED, check.sh).
9. **DESIGN QUESTIONS and fix `e42586b` — fix MINIMAL AND CORRECT.** It moves rules 4-7 unchanged into one function (`SlotTaken` now read from `view.taken`, built from the same admissions) and runs them, without the signature, on the body `approve` builds; a refusal is `InvalidApproval`, that proposal ends `RefusedInvalid`, nothing else changes (READ). Regression test and red row `deputy_approve_no_validate` RED (TESTED). DQs: 1 accepted as built (D-3); 2 needs the design owner before daemon work (D-2); 3, 5, 6, 7 reasonable as built; 4 reasonable but untested (D-5); 8 (`docs/ROSTER.md` §7's stale last sentence) is Friday's call.

## What I ran (all TESTED, clean clones under a scratch work dir)

- `coagent_merge_check.sh <work>/mc m3-deputy 8aebed8… scripts/red-controls-roster.sh`: exit 0. `check.sh` exit 0 (fmt, clippy, test, deny; 1,185 tests passed, 0 failed). Roster runner exit 0: `rows: 102`, all RED; `equivalence rows: 4`, GREEN; release build refused; unknown name refused; `GREEN: 214 tests ok`.
- `scripts/red-controls-core.sh` on the same clone: exit 0, 65 rows RED, `GREEN: 296 tests ok`.
- Gate probes `qa_deputy_gate.rs` (G1-G5): 5 passed (they assert today's behaviour; D-1 to D-3 rate it).
- Property, release, 1,024 cases, two seeds (above).
- 17 gate mutants of the deputy source, each against the deputy test targets: 15 killed, 2 survived (M03 = D-5, M07 = D-6). Tree restored after each (git status: only the probe file untracked).
- Heavy runs: one of mine at a time; process count checked before each (1 other running each time).

Artifacts: `m1_review/gate_deputy_tests/` (probe file, scripts, mutation results, property logs, both runner logs, check results; paths and names masked).

## NOT TESTED

- Anything daemon-side (transport, `admit_view` wiring, absence measurement, channel teardown for dropped keys, verify-words inheritance): not built in this lane.
- "Sit between a newcomer and the members" (design 2.8.6): reasoned only, as the builder says.
- Debug-profile 128-case property inside `check.sh` ran green as part of check; I did not run the builder's third seed `0x5EED0000DE9A0003`.
- I did not re-verify the builder's STATUS table line by line beyond the items above; `docs/ROSTER.md` §8 read for the three sentences (word for word, marked "Approved by the owner, 2026-11-19 (use as drafted)") and the 5.3 and section-6 tables.

## Instrument errors

- Two of my wait loops were moved to the background by the harness after 180 s; I replaced them with shorter polls. No result depended on them.
- No other instrument error.
