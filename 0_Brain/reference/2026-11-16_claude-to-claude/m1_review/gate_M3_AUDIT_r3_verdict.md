VERDICT: NO GO 882e0940c1a34d76a9836256c7bff67283ec5609

# QA gate M3-AUDIT round 3 (final, owner-authorised): `coagent-audit` (branch `m3-audit`)

Independent tier-1 gate, 2026-11-17. Findings only: nothing fixed, committed or pushed. `git rev-parse
HEAD` in my clone = `882e0940c1a34d76a9836256c7bff67283ec5609` = the expected head; `origin/main` =
18005d6 (Ran). My working folder:
`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/0bad48b2-2056-45a8-9019-8cc0029c12d3/scratchpad/gate_m3_audit_r3/`
(`clone` = suite and red controls, `atk` = my attack tests, `mut1..3` = mutations, `merge` = merged
tree). My tests and drivers: `m1_review/gate_audit_tests_r3/` (`gate_r3.rs`: drop it into
`crates/coagent-audit/tests/` and add `[[test]] name = "gate_r3"`, because the crate has `autotests = false`;
`mutate_r3.py`; result text files).

**Why NO GO.** The round-2 attack is closed. A removed member's records are refused, replays are
refused, and the reserved own quarter held under every flood I ran. **But the same class fails a third
time, at its edge (R3-M1, Major).** The quota is charged to whoever *signed* a stored record, not to
whoever *caused* it. So other members can spend an honest member's quota, and one record kind that must
never be refused is charged to a quota: **roster versions**, charged to the convener. Three hostile
members each send the convener ~3,500 tiny events. The convener writes one receipt per event into its
own chain. Every other member that receives the convener's chain stores those receipts against the
CONVENER's quota. In a release build, with default limits, this takes 1.4 s. After that, **every new
roster version is refused (`LogFull`) at that member**, including the one that removes the hostile
members. So "nothing is accepted from a removed member" cannot hold at that member, because it can no
longer learn of the removal. An honest convener's own traffic in a long session (about 10,000 receipts)
does the same with no attacker. The docs do not state this. The addendum asked that a per-peer quota be
one that "one peer cannot exceed whatever others do", and that no peer can grow a member's store by any
message kind. Here other peers exhaust an honest peer's quota by proxy, and that blocks session
control.

Everything else the addendum asked for is done and reproduced. That includes the two restored
round-1 gate tests, which now go red; the six round-2 mutants, now guarded; the signed share-level
statement; and the receipt-timing disclosure.

## 1. Findings

| id | sev | file:line | the exact sequence | Ran/Reasoned |
|---|---|---|---|---|
| **R3-M1** | **Major** | `session.rs:461-463` (`apply_roster` charges the roster record to `payer_for(convener)` and calls `ensure` before `RosterChain::apply`); `session.rs:613-631` (a received event, receipts included, is charged to its SIGNER); `docs/AUDIT.md:119-120, 132` | **(a) By proxy, release build, default limits** (`r3_finding_release_receipt_proxy_default_limits`): 5 members (C = convener, V, H1-H3). C shares `full` with V. H1-H3 each send C tiny no-tier events until their own quota at C is full: **10,453 events stored at C in total**. C appends a receipt per event; V receives each receipt from C and stores it against **C's** quota: **10,452 receipts, C's usage at V 6,291,450 of 6,291,456 bytes; 1.39 s**. Then C removes H1 and V calls `apply_roster(r2)` → **`Err(LogFull)`**. V stays at version 1, and so does every later roster. V's own `record` still works. **(b) No attacker** (`r3_finding_convener_quota_full_blocks_every_roster_update`, debug, 1 MiB store): 20 of C's own events plus 131 receipts C writes for an honest member's events fill C's quota at V. `apply_roster(removal of H)` → `LogFull`. Re-applying the held version 1 → also `LogFull`. H's checkpoint and a fresh heads-seen record of H are then **still accepted** at V. **(c)** The same mechanism (receipts charged to their signer) lets any members fill an honest NON-convener peer's quota at V. V then refuses that peer's real events. Same code path (Reasoned from (a)). | RAN (a, b); (c) REASONED |
| R3-m1 | Minor | `session.rs:194-212` (`start` charges every existing store record to `Own`) | `r3_finding_restart_charges_existing_peer_records_to_own`: 8 members, 1 MiB store, 7 peers fill their quotas (peers 762,640 bytes). `start` again on the same store: `usage_of(Peer(1)) = (0,0)` and all 770,792 bytes count as `Own`. The peers refill with 274,172 bytes and the store reaches 1,044,964 / 1,048,576. **Own `record` → `LogFull`**: the reserved quarter is gone after one restart. Reload is a stated precondition of daemon wiring (BACKLOG), so this is Minor. But the code already counts existing records, so the accounting it does is wrong. | RAN |
| R3-m2 | Minor | `session.rs:251-276`, `126-142`, `342-394`, `461-472` | Real checks in the R2-M1/R2-m2 code that **no test fails without** (§5): the per-peer RECORD quota (P01); the peers'-pool RECORD limit, i.e. the own reserve counted in records (P02); the receipt record reservation (P06); "advances" for a LOWER roster version (P08) and for a lower number of a held author (P09); share statements: the kind check (P16), levels learnt FROM a removed author kept (P18), `roster_v` not held accepted (P22); the evidence cap's value (P27); `set_limits` refusing to raise limits (P28). Plus round-2's N06 (`verify` reporter membership AT `roster_v`, `bundle.rs:926` → `equivocation.rs:358`), which lost its guard when the builder reversed one `r2_ok_readd_under_a_new_key` assertion, and N14 (own worst-case reservation), killed only incidentally by my restart test. | RAN |
| R3-m3 | Minor | `session.rs:285-294` (usage is never released) | `r3_finding_identity_rotation_fills_peer_pool_and_blocks_rosters_at_non_convener`: a hostile member floods, the convener removes it and adds a new key in its slot, six times. The peers' part fills (store 786,746 bytes). An honest peer then gets **42 events in, against about 65 for a fresh quota**. This needs the convener to admit the rotations; the own share holds. | RAN |
| R3-n1 | Note | `session.rs:784-806` | A heads-seen record from a reporter whose quota is full **stores** the evidence it reveals (evidence pool), then returns `Err(LogFull)`, so the caller is not given the evidence (`r3_finding_evidence_not_stored_when_peer_pool_full`: evidence records stored 1, return `LogFull`). | RAN |
| R3-n2 | Note | `session.rs:614-619`, `666-667` | `ensure` runs before the fork check. An author whose quota at V is full can send V a conflicting EVENT and gets `LogFull`, so no evidence is formed. A conflicting CHECKPOINT still yields `Fork` evidence: it is small enough to fit the receipt-reserve gap (`r3_finding_fork_from_an_author_at_quota_gives_logfull_not_evidence`). | RAN |
| R3-n3 | Note | `session.rs:462-464` | With the convener's quota full, re-applying an already-held roster version returns `LogFull`, not the roster crate's own answer (part of R3-M1 (b)). | RAN |
| R3-n4 | Note | `chain.rs:268-295`, `header.rs:34` | Share-level statements are ordinary chain events, so every member at `summaries` or above for author X learns X's level for EVERY other member. The kind name `member.accepted` is the spec's 04 §3.8 event name. A `record()` of that kind is redacted (the key id becomes `[REDACTED]`) and is refused as `BadStatement`, so the two cannot be confused (RAN, `r3_ok_share_statement_scope_rules`). | RAN / REASONED |
| R3-n5 | Note | — | Quotas are per session. Nothing bounds the total across sessions a peer shares with a member; that is the daemon's job. | REASONED |
| R3-n6 | Note | `tests/gate_r2.rs:494-509` | The edited release flood test `break`s on the first `ReporterRemoved`, so it makes one attempt. My `r3_release_flood_measurements` (a) makes 100,000 (§3). | RAN |

## 2. Measured totals (all RAN by me, own target directories in scratch)

| What | Builder | Me |
|---|---|---|
| `scripts/check.sh` at 882e094 | exit 0; 217 / 5 ignored; audit 114 | **exit 0 five times out of five**, "CHECK OK"; **217 passed, 0 failed, 5 ignored** each time. Audit crate **114** (unit 2, alloc 1, bundle 7, countersign 3, determinism 4, equivocation 5, gate 15 (+2 ignored), gate_r2 16 (+3 ignored), gate_return 24, gate_return_r2 12, honest_export_prop 2, join_leave 3, no_content 1, receive 3, redaction 4, signing 6, tamper 3, tiers 3). Runs 2-5 ran while three parallel mutation builds loaded all 12 cores. **No flake.** |
| Audit red controls (`red-controls-audit.sh`, only target and log dirs repointed) | 93 of 93 RED; green 114 | **93 of 93 RED, 0 NOT-RED; "GREEN: 114 tests ok"; "RED CONTROLS OK"; exit 0** |
| Core red controls (`red-controls-core.sh`, log and probe dirs repointed) | 65 of 65; green 100 | **65 of 65 RED; "GREEN: 100 tests ok"; "RED CONTROLS OK"; exit 0** |
| Gate release tests (`--ignored`, release) | pass | `gate` 2/2 pass (13.5 s); `gate_r2` 3/3 pass |
| Merged tree `check.sh` | exit 0; 366 / 10 | **exit 0; 366 passed, 0 failed, 10 ignored** (§7) |
| My attack tests `gate_r3` | — | 12 debug pass + 2 release pass (each `r3_finding_*` passing = finding demonstrated) |

**Flood re-measurement (3a), release build, default limits** (`r3_release_flood_measurements`; process
peak RSS from `/usr/bin/time -l`):
- (a) The round-2 attack, a removed member signing fresh records at its old version: **100,000 attempts
  in 5.75 s, 0 accepted** (every refusal `ReporterRemoved`). Store unchanged at 4,976 bytes / 3 records.
  **Victim's own `record` → Ok.** (The builder's edited test: 0 accepted, 217 µs, own Ok.)
- (b) A current member Y reporting a colluder X's headers at ever higher numbers (each record
  "advances"): **7,062 records stored, 6,291,135 bytes charged to Y (per-peer quota 6,291,456)**, 0.82 s.
  Then own record Ok, and another honest peer's event Ok.
- (c) All three peers of a 4-member session flood maximum-size events: **1,063 accepted each, about
  6.29 MB each; store 18,864,645 bytes / 6,380 records; own record Ok; the export verifies**; 7.8 s.
  Peak RSS of the whole process **206 MB** (MemStore, in-memory chains, export and parse together).
- A current member signing fresh EMPTY records: 1 stored per (reporter, recipient), the rest `NotNewer`
  (`r3_ok_current_member_fresh_empty_records_are_not_newer`, debug).
- R3-M1 (a) above: peak RSS 64 MB.

## 3. Storage and memory paths a peer message can reach (3b): my enumeration from the code

| # | Peer input → kept | Where | Bound in code | Tried to exceed (Ran) | Result |
|---|---|---|---|---|---|
| 1 | Another author's event → store `PeerEvent` + in memory `ReceivedChain.events` | `receive` 607-640, `received.rs:405` | signer's quota (bytes + 2 records, 4,096 receipt reserve) checked before accept; exact-next only | flood (c); colluding peers; rotation | held per signer; R3-m3 |
| 2 | Receipt for it → OWN chain event (memory) + store, charged to the author | 623-631 | as 1 | — | held at the RECEIVER; **but at every third member the receipt is the receiver's event, charged to the receiver → R3-M1** |
| 3 | Another member's RECEIPTS (its chain) | as 1 | charged to that member, not to the author that caused them | R3-M1 (a) | **exceeded by proxy** |
| 4 | Checkpoint → store + `heads` (≤1,024/author) | 661-679, `received.rs:450-461` | advance-only; cap; signer's quota | gate r1/r2 tests, N12/N13 killed | held |
| 5 | Joiner's anchor | 643-657 | one per author; quota | — | held (Reasoned) |
| 6 | Countersignature of own checkpoint → store + `countersigs` map | 563-587 | dedupe; refused after removal; signer's quota | builder test; P20 survives (duplicate short-cut, near-equivalent) | held |
| 7 | Heads-seen → store + `last_hs` (key (from, to∈{None, me})) + `hs_digests` | 744-808 | dedupe; advance-only; removed reporter refused; quota | (a), (b), fresh-empty; P08/P09 survive | held (quota-bounded); R3-m2 |
| 8 | Evidence → store + `evidence_stored` + `evidence_per_author` | 298-320 | ≤4 per accused author (authors = members ever); pool = one peer-quota; silently skipped if full | builder test; R3-n1, R3-n2 | held; R3-n1/n2 |
| 9 | Roster version → store + `history` | 461-476 | convener's quota (**refused when full**) | R3-M1 | **this is the failure** |
| 10 | Share-level statement → `known` (memory only) | 342-394 | one per (author, member), both current; dropped on removal | replay/order tests | held |
| 11 | `used_by` map, one entry per payer ever | 290 | members ever (convener-issued versions) | rotation test | held (Reasoned) |
| 12 | `peers` map (one `ReceivedChain` per current author) | 589-603 | current members (cap 8) | — | held (Reasoned) |
| 13 | Refused input (gap, reorder, replay, bad signature, `RosterBehind`) | `received.rs` | only the scalar `max_offered` changes | — | held (Reasoned) |
| 14 | Restart / reload | 194-212 | none: all counted as Own | R3-m1 | **fails** (Minor: reload not built) |
| 15 | Cross-session total | — | none | — | daemon (R3-n5) |

Memory (3d): every in-memory structure above is either bounded by what was stored (events, heads,
digests, evidence), or by members-ever and roster versions. Measured peak 206 MB for three full peer
quotas plus an export and parse (Ran). No buffer for out-of-order input exists (Read).

## 4. The signed share-level statement (step 4)

All RAN unless marked:
- **Who may assert:** only the author. The header signature is verified under the author's roster key,
  and a third party's or unsigned statement → `BadSignature` (builder's test, red row
  `share_stmt_no_sig` RED). The receiver's own statement and an author's statement about itself are
  refused (`r3_ok_share_statement_scope_rules`; P15 killed by it).
- **Replay across sessions:** the same identities in another session → `WrongSession`
  (`r3_ok_share_statement_cross_session_replay_refused`). Without that check (P14) the signature alone
  would NOT stop it: the session id is inside the signed header, so the statement verifies. My test is
  the only one that kills P14.
- **Across roster versions:** a statement naming a version before the member joined → `NotMember`.
  Remove and re-add under the same key: the pre-removal statement is refused, a new one counts, and the
  old one stays refused even after it (`r3_ok_share_statement_readd_same_key_new_statement_counts`).
- **Ordering:** by the author's sequence number. Downgrade delivered before upgrade → the downgrade
  stands. A later upgrade counts. A replayed old one changes nothing
  (`r3_ok_share_statement_ordering_downgrade_wins_whatever_the_arrival_order`).
- **Default when absent:** `Nothing` (builder's tests and mine).
- **Gaps (R3-m2):** the kind check (P16), the "roster_v held" check (P22) and forgetting levels FROM a
  removed author (P18) survive every test. P22 matters for a member that joined after the removal: it
  holds no pre-removal version, so with that check gone it would accept a pre-removal statement
  (Reasoned).

## 5. Mutation testing (step 5)

Driver `gate_audit_tests_r3/mutate_r3.py`. It loads round 1's 42 (`gate_audit_tests/mutate.py`) and
round 2's 27 (the ADAPT and NEW tables of `mutate_r2.py`). It re-adapts 8 to the changed source with
the same meaning (N01, N07, N14, N16, N17, N21, N22, M38; marked `[adapted r3]`). It adds **30 new
mutants (P01-P30) on code changed since 4c39916**. Each mutant was applied alone to a pristine clone
and run against the branch's full `coagent-audit` suite (plus `coagent-crypto` for crypto mutants),
then reverted with `git checkout`. The worktree was clean after each of the three runs. Survivors were
then run against my `gate_r3`.

**Totals (RAN): 99 mutants. Branch suite kills 77: round 1 40/42, round 2 25/27, new 12/30.**

| Survived the branch suite | My gate_r3 | Real unguarded security check? |
|---|---|---|
| M05 session compare in `attests`, M06 4-byte hash prefix | — | No: equivalent or near-equivalent (as in rounds 1 and 2) |
| N06 `verify` reporter BY instead of AT `roster_v` | survives | **Yes, in `verify`** (session path masked by `ReporterRemoved`). Its guard was lost by the reversed gate assertion. Minor |
| N14 own worst-case reservation 4 bytes | killed (incidentally, by a finding test) | Yes, small: own records may overshoot by one record. Minor |
| P01 per-peer record quota | survives | **Yes** (a peer of tiny records can take more than 1/7 of records) |
| P02 peers'-pool record limit | survives | **Yes: the reserved own share in RECORDS is unguarded** (7 peers + the evidence pool = 8/7 of the pool) |
| P05 receipt byte reserve | killed (incidentally) | small overshoot |
| P06 receipt record reserve | survives | small overshoot |
| P08 lower `roster_v` advances; P09 lower number advances | survive | Yes, quota-bounded (latest-state rule unguarded) |
| P14 share session check | **killed** (`r3_ok_share_statement_cross_session_replay_refused`) | Yes, now guarded by my test |
| P15 author==member | **killed** (`r3_ok_share_statement_scope_rules`) | low |
| P16 share kind check; P18 levels from removed author; P22 `roster_v` held | survive | Yes, low-to-medium (§4) |
| P19 evidence dedupe; P20 countersignature dedupe; P30 `deny_unknown_fields` | survive | near-equivalent (caps and other dedupes catch them) |
| P26 per-peer divisor 7→3 | killed (by my quota tests) | value now pinned |
| P27 evidence cap 4→1000; P28 `set_limits` may raise | survive | values not pinned |
| P29 `start` ignores existing records | killed (by the restart finding test) | see R3-m1 |

Surviving every test, branch suite and mine: **N06, P01, P02, P06, P08, P09, P16, P18, P19, P20, P22,
P27, P28, P30** (plus M05 and M06). Real unguarded checks among them: N06, P01, P02, P06, P08, P09,
P16, P18, P22, P27, P28 (R3-m2).

## 6. Gate-test integrity (step 2): every difference ruled

`diff` of the reference copies against the tree (Ran). Every edit is marked `// GATE RETURN (builder,
…)` with the old line quoted.

**`gate_attacks.rs` (round 1), 5 hunks:**
1. A-M3 import replaced by a test-local `mod domain` and `nested_message` (round 2's edit, ruled then): **necessary, not weakening.**
2. R2-n1 domain test: the signer now signs `nested` (32 bytes) instead of `msg`. **Necessary, and it restores teeth: RED under `audit_under_binding`** ("audit-domain signatures verified as device bindings": runner row Ran RED).
3. R2-n1 removal case: D gets a checkpoint B holds, so B's record carries an entry about removed D. **Necessary. RED under `hs_current_roster`** ("no longer catches A": Ran RED). The builder also redefined that red control from `member_by(latest)` (which a removed member still passes) to `member_in(latest)`. That models round 1's "check against the current roster" more faithfully. Ruled legitimate.
4. `removal_case`: `b.note_share_level(A, C, Full)` → A's signed statement. **Necessary (API now takes only the signed event).**
5. A-M4 flood `let _ =` (round 2's edit): unchanged ruling.

**`gate_r2.rs` (round 2), 14 markers:**
- Seven call sites `note_share_level(x, m, level)` → `announce(..)` (the author's signed statement), with `.unwrap()`. **Necessary; positive controls still run through genuine statements.**
- `r2_finding_share_level_input_is_unauthenticated`: C's statement naming X and an unsigned one are now refused (`BadSignature`); `== 1` → `== 0` for the leak. **Necessary (finding fixed); it now guards the fix (red row Ran RED).**
- `r2_finding_known_level_survives_removal_and_readd`: `Full` → `Nothing`. **Necessary; red row `share_keep_after_removal` RED.**
- Replay test: expects `Duplicate`, one stored copy, own record Ok. **Necessary; asserts the fix.**
- Release removed-member test: breaks on `ReporterRemoved`, asserts 0 stored and own Ok. **Necessary**, but it makes only one attempt (R3-n6). Covered by my 100,000-attempt run.
- `r2_ok_readd_under_a_new_key`: one assertion **reversed** (the old key's record at its old version after its removal: `is_ok()` → `ReporterRemoved`). **Necessary under addendum 2 item 2** ("nothing at all from it … except evidence"), and the evidence path is kept. **Side effect:** N06 in `verify` lost its only guard (R3-m2). Not a weakening of a property the addendum keeps, but it needs a replacement guard on the `verify` path.
- `gate_r2_wrapper.rs` compiles the file under `#[rustfmt::skip]` as target `gate_r2`. Fine.

**No weakening found.** Both requested restorations go red under their named controls (Ran).

## 7. Merge readiness (step 6)

In my own `merge` clone: branch `gate-merge` = 882e094 + `git merge origin/main` (18005d6), no conflicts,
nothing edited or regenerated. Merge commit eb4dc09, **tree `cee85fd…`, the same tree the builder
reported**. `check.sh` → **exit 0; fmt, clippy, test, deny all pass; 366 passed, 0 failed, 10 ignored**
(Ran, under CPU load). **Cargo.lock vs main: one added `[[package]] coagent-audit` block; no version of
any crate main already had changed** (Ran: `git diff origin/main HEAD -- Cargo.lock`). The core
red-control runner was not run on the merged tree (it ran on the branch).

## 8. Scope outside `crates/coagent-audit` (step 7)

`git diff --stat origin/main...HEAD` excluding the audit crate (Ran): **7 files**:
`BACKLOG.md` (+60), `Cargo.lock` (+16, the audit package only), `Cargo.toml` (+1 member line),
`crates/coagent-crypto/src/identity.rs` (+64), `docs/AUDIT.md` (+349), `docs/CRYPTO-GLUE.md` (+62),
`scripts/red-controls-audit.sh` (+148). The only commit touching `coagent-crypto` is **c407fe7** (`git
log 129914b..HEAD -- crates/coagent-crypto`); nothing in the crypto crate changed since 4c39916. The only
other non-audit commit is 0fa9023 (workspace member line). **Exactly what was authorised.**

## 9. Direction (not a fix, the builder's call)

Never refuse a roster version for quota. Charge it to `Own`, or exempt it: it is bounded by the
convener's signed issuance and the session cap. Charge a stored peer RECEIPT (and anything else a member
writes because of a third party) so that one member's traffic cannot consume another's quota: for example
a per-(signer, named author) sub-quota for receipts, batched receipts (DESIGN QUESTION 18), or keeping
other members' receipts out of the store beyond a small bound. Count the quota from the store on
`start`. Release removed members' usage, or bound members-ever payers. Add guards for P01, P02, P06,
P08, P09, P16, P18, P22 and N06, and a test where the victim is NOT the convener (every churn test today
has member 0 as both convener and victim, so `apply_roster` is always charged to `Own`).

## 10. For a non-technical owner: what this log can and cannot be trusted for now

1. It reliably proves who signed which record and in what order, and catches a member who tells two people different stories once they compare notes.
2. One member flooding you can no longer stop your own computer from logging; that problem from last round is fixed and measured.
3. But members working together (or simply a long, busy session) can now stop your computer from accepting the organiser's member-list changes, including the removal of the troublemakers. That is why this is still a NO.
4. Sharing levels now come only from each person's own signed statement, and the default is to share nothing; that part holds up.
5. After a restart the space reserved for your own records is not protected; restarts are not supported yet anyway, so the daemon must not be wired until they are.

## 11. Ran or reasoned; what I did not do

**Ran:** rev-parse; `check.sh` ×5 (4 under load); both red-control runners; the gate's release tests;
14 attack tests of my own (12 debug, 2 release); 99 mutants against the branch suite and 20 survivors
against my tests; the merge and its `check.sh`; the scope diffs; peak RSS of the release runs.
**Reasoned:** R3-M1 (c) for a non-convener peer (same code path as (a)); memory bounds per map; R3-n5;
P22's joiner case; convener removal (not tested; the roster rules forbid it).
**Not done:** Linux or Windows; a fuzzer on `Bundle::parse`; the core runner on the merged tree; memory of
`verify` alone; any daemon or channel integration (none exists).
**My own slips:** my first convener test filled C's quota with C's events only. The 4,096-byte receipt
reserve left a gap a roster fitted into, so it went green. I re-ran it with receipts, which carry no
reserve, and the claim rests on that run and on the release proxy run. My first evidence test assumed the
peer pool could be filled exactly; it could not, and the test now demonstrates R3-n1 instead. My first
colluder test sent headers in a broadcast record (refused by design); I fixed it to an addressed one.
**Processes:** see the final line of my report to Friday.
