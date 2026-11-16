NO GO at 4c399161dd9c326c7c0f9dbf23655852c1f45a67

# QA gate M3-AUDIT round 2 (delta gate): `coagent-audit` (branch `m3-audit`)

Independent tier-1 delta read, 2026-11-17. Findings only: nothing fixed, committed or pushed. Delta
`1d4a55b..4c39916` (28 files, +3,054 / -426). My clones, all under
`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m3_audit_r2/`:
`repo` (attack tests; `rev-parse HEAD` = 4c39916…), `redA` / `redC` (the two red-control runners),
`merge` (scratch branch `gate-merge` = 4c39916 + `origin/main` 18005d6), `mut` (mutations). Attack
tests: `m1_review/gate_audit_tests_r2/gate_r2.rs` (drop into `crates/coagent-audit/tests/` and add a
`[[test]] name = "gate_r2"` entry: the crate has `autotests = false`) and the driver `mutate_r2.py`.

**Why NO GO:** one Major stands (R2-M1). The addendum told the builder to "bound what a peer can make a
member store", and `docs/AUDIT.md` now says "a peer cannot grow a member's log". That is false. Every
heads-seen record a member accepts is written to its store, with no deduplication, no quota per reporter
and no rate limit. Records from a member who has been removed are accepted forever if they cite the old
roster version. One peer can fill an honest member's store in seconds. After that the member gets
`LogFull` on its OWN `record`, and the documented response is "end or pause the session's audit-class
work". Everything else round 1 raised is closed. The crypto-crate change is exactly what was authorised
and is sound. A-B1 is closed in the library, with two disclosure limits that are stated and that I
quantify below (Minor).

## 1. Gate-test integrity (the builder's three edits to `gate_attacks.rs`)

`diff` against the reference copy shows exactly three hunks, each marked `// GATE RETURN (builder, …)`
with the old line quoted. No assertion text changed. The file is compiled through `tests/gate.rs` under
`#[rustfmt::skip]` (Ran).

| Edit | Ruling |
|---|---|
| **A-M3**: the import of the crate's (now `pub(crate)`) `domain::{sign, verify, nested_message}` is replaced by a test-local `mod domain` that signs and verifies through `AuditDomain::sign_domain()` (the real crypto domains), and a local `nested_message` that rebuilds the round-1 nested bytes. | **Legitimate, and the attack was not weakened in the product. But the round-1 test no longer bites.** The test-local signer is the strongest primitive available: `DeviceIdentity::sign` under an audit domain over any bytes. Under the new encoding the nested bytes are no longer what anything signs, so `gate_domain_no_audit_domain_signature_is_a_valid_binding` stays **green under the red controls `audit_under_binding` and `one_label`** (Ran: only `gate_ok_domain_every_kind_refused_under_every_other_label` goes red). The property is carried by the builder's `signing::test2_no_audit_signature_over_32_bytes_is_a_device_binding` (red row `audit_under_binding`). It is also carried by my own replacement attacks (both pass at 4c39916): `r2_ok_no_audit_domain_signature_crosses_into_any_other_domain_or_a_binding` signs attacker bytes of every length 0-96, plus label-shaped messages, under each of the 7 domains. It checks each against all 6 others and as a device binding over every 32-byte window of the message and of `label ‖ 0 ‖ message`. `r2_ok_signatures_from_the_public_api_stay_in_their_domain` covers every signature the PUBLIC API still produces. That includes a countersignature that `receive_head` makes over an attacker-crafted head whose 32-byte `hash` the attacker chose as a Noise key, and `Bundle::reseal` over attacker-chosen contents. It goes red under both domain red controls. No public function of `coagent-audit` signs arbitrary bytes any more (read: every `sign` call site is a typed body; `HeadsSeenBody::sign` is `pub(crate)`). Note R2-n1. |
| **A-B1**: in `removal_case`, `b.heads_seen(..)` becomes `b.note_share_level(A, C, Full)` + `b.heads_seen_for(.., C)`. | **Legitimate (necessary: broadcast records now refuse headers), but the case lost the entry that made round 1 fail.** D, the removed member, has no checkpoint, and nobody knows D's levels, so `heads_seen_for` leaves D out. The record therefore contains **no statement about the removed member**, and round 1's failure was exactly such an entry. The edited test stays **green under the red control `hs_current_roster`** (Ran). The builder's `a1_m1_*` tests carry that red row. I re-added the missing case: `r2_ok_removal_case_with_an_entry_about_the_removed_member`. D has a checkpoint B holds, D is removed, and B's record, made before or after the removal, carries D's entry. C still verifies it and catches A (passes). |
| **A-M4**: in the ignored flood test, `receive_head(..).unwrap()` becomes `let _ =`. | **Legitimate.** Heads beyond the per-author cap are now refused, which is the fix. The assertion (the member's own export parses) is unchanged and passes in release (Ran). The test no longer comes near the export caps, so "export at the store limit verifies" now rests on the builder's `a1_m4_*` and on my release measurement (§4, A-M4). |

**No weakening of the product's checks was found. Two round-1 tests now guard less than before (R2-n1),
and the properties they guarded are covered elsewhere.**

## 2. The change to the merged crypto crate

- `git diff 1d4a55b..4c39916 -- crates/` outside `coagent-audit` touches **one file**:
  `crates/coagent-crypto/src/identity.rs | 64 +` (Ran). Against the merge-base 129914b, the files outside
  the audit crate are that one, plus root `Cargo.toml` (+1 `members` line) and `Cargo.lock` (+16), both
  from round 1. `coagent-proto`, `coagent-roster`, relay, ipc and cli are unchanged.
- The diff is exactly: five variants (`AuditHeader`, `AuditHead`, `AuditCountersign`, `AuditHeadsSeen`,
  `AuditBundleSeal`) with doc lines, five arms in the private `label()`, and two tests. No other line.
- **Labels:** `coagent-audit-header-v1`, `coagent-audit-head-v1`, `coagent-audit-countersign-v1`,
  `coagent-audit-heads-seen-v1`, `coagent-audit-bundle-seal-v1`, plus the existing `coagent-binding-v1` and
  `coagent-roster-v1`. All are distinct and none contains 0x00. `head-v1` vs `heads-seen-v1` differ at the 18th byte,
  so no label is a prefix of another.
- **Encoding:** `signed_message` = `label ‖ 0x00 ‖ msg` (`identity.rs:60-66`). Because no label contains
  0x00, `label ‖ 0x00` is a prefix-free code: the first zero byte ends the label. Equal signed byte strings
  therefore imply the same label and the same message. Label A + message X can never equal label B +
  message Y. Verification is `verify_strict` over the whole string. Sound (Reasoned; exercised by my
  all-lengths test).
- **All-pairs test:** `ALL_DOMAINS` has 7 entries; the double loop skips `a == b` → **42 ordered pairs**,
  each asserting `Err(BadSignature)`, with the positive control per domain (Read and Ran). Mutating one
  new label to equal another (N18: heads-seen = head) or to equal `Binding` (N25) is killed by both new
  tests and by the audit crate's own tests.
- **Serialised forms, pinned values, matches:** `SignDomain` derives only `Debug, Clone, Copy, PartialEq,
  Eq`: no serde, no discriminant used anywhere. The only `match` on it is `label()`, inside the crate. No
  other crate matches on it (grep over `crates/`: only constructors `SignDomain::Binding`/`Roster` in
  roster and tests). Existing labels are unchanged, so existing binding and roster signatures and their
  pinned values are unchanged. **The core red-control runner: 65 of 65 RED, "GREEN: 100 tests ok", "RED CONTROLS OK"** (Ran,
  my copy with LOGDIR repointed). The merged crates' behaviour is unchanged. The relay has no red-control
  runner on this branch and no test of it touches `SignDomain`; it was covered by the merged-tree
  check.sh run.
- **Ruling: the change is exactly the authorised change, and sound.** One Note (R2-n4): the all-pairs list is
  hand-kept; an eighth variant would not join it automatically.

## 3. Reproduction

| What | Builder | Me (Ran) |
|---|---|---|
| `scripts/check.sh` at 4c39916 (`CARGO_TARGET_DIR` in scratch) | exit 0; workspace 189; audit 86 | **exit 0**, "CHECK OK"; workspace **189 passed, 0 failed, 2 ignored**; audit crate **86** (unit 2, alloc 1, bundle 7, countersign 3, determinism 4, equivocation 5, gate 15 (+2 ignored), gate_return 24, honest_export_prop 2, join_leave 3, no_content 1, receive 3, redaction 4, signing 6, tamper 3, tiers 3) |
| `scripts/red-controls-audit.sh` (only `CARGO_TARGET_DIR` and `LOGDIR` repointed to scratch) | 75 of 75 RED, green 86 | **75 of 75 RED**, "GREEN: 86 tests ok", "RED CONTROLS OK" |
| `scripts/red-controls-core.sh` (only `LOGDIR` repointed; target via env) | 65 of 65, green 100 | **65 of 65 RED**, "GREEN: 100 tests ok", "RED CONTROLS OK" |
| **Merged tree** (my clone: branch `gate-merge`, `git merge origin/main` 18005d6, no conflicts, nothing edited; tree **0eae36c**, the same tree the builder's `merge-tree` reported) `check.sh` | not built | **exit 0**, fmt, clippy, test and deny all pass; **338 passed, 0 failed, 7 ignored** |
| Gate's release tests (`--release --ignored`) | 2 of 2 | **2 of 2 pass**; redaction 3/6/12 ms at 64/128/256 KiB for both inputs |

**I read every new red row's failure text. Each is red on its named property.** Spot checks of the full
assertions: `hs_headers_in_broadcast` → `left: Ok(()) right: Err(HeaderInBroadcast)`;
`hs_current_roster` → `left: Err(Evidence(NotAMember)) right: Ok([])`; `frame_cap_plus_one` /
`bundle_cap_plus_one` fail on the boundary assertion ("frame of 65536 bytes", "67108865 bytes"), i.e. the
cap moved by one. `hs_headers_to_nothing` → "C holds the header of B #6 via messages received";
`receipts_unfiltered` → "holds the receipt summary naming B"; the A-M2 rows fail with
"countersigner not a member at that roster version" from the property test.

**Scope** (Ran): 28 files. `crates/coagent-audit/**`, `crates/coagent-crypto/src/identity.rs` (authorised),
`docs/AUDIT.md`, `docs/CRYPTO-GLUE.md`, `BACKLOG.md`, `scripts/red-controls-audit.sh`. Nothing else.

## 4. Round-1 findings

| id | Status | Basis |
|---|---|---|
| **A-B1** (Blocker) | **CLOSED, with two stated limits (R2-m1, R2-m2)** | Ran. A broadcast record holding a header is refused (`HeaderInBroadcast`). With the level unknown, the default is `Nothing`, so `heads_seen_for` sends checkpoints only. After a lowered level, checkpoints only again. A positive control at `summaries` sends the header (`r2_ok_unknown_or_lowered_level_sends_checkpoints_only`). A record addressed to C and forwarded to D is refused at D (`NotAddressedToMe`) and not stored. Re-addressing it breaks B's signature, because `to` is inside the signed body (`r2_ok_forwarded_*`). Receipt summaries go only to the author or to members known to be entitled. Builder scans plus mine: no X header, tier body, salt or receipt summary reaches a `nothing` member through events, checkpoints, countersignatures, heads-seen, receipts, store or export, given correct `note_share_level` input. Evidence is built only from statements the member already holds, and nothing in the library sends evidence or another member's bundle to a member. Error values carry no content (round 1). What remains is quantified in R2-m1 (receipt headers) and R2-m2 (unauthenticated level input). |
| **A-M1** | **CLOSED, WITH A NEW ISSUE (R2-M1)** | Ran. A future version gives `RosterBehind(99)`: nothing stored, and later honest records are processed (`r2_ok_future_version_*`). A hostile member stalls only its own records; there is no buffering, so an honest record that is ahead must be resent (R2-n2). A joiner citing a version before it joined → `NotAMember`. Re-add under a new key: the old key's records at old versions verify; the new key cannot report under a version before its addition; the old key cannot report after its removal (`r2_ok_readd_under_a_new_key`). A record about a removed member, made before or after the removal, still verifies and still catches equivocation (`r2_ok_removal_case_*`). Re-adding the same key works (slot reuse): see R2-m2 for the level that carries over. The convener cannot be removed under the roster rules (Reasoned, not tested). History memory is one `BTreeSet` of ≤8 key ids per roster version, so it grows only with convener-issued versions (Reasoned). History divergence is a roster fork, which `RosterChain::apply` refuses before `push` (Reasoned). **The new issue:** a member removed at version v keeps reporting under v-1 **forever**, and every such record is stored. That is R2-M1. |
| **A-M2** | **CLOSED** | Ran. Several checkpoints share the pre-join version: only the latest (the anchor) can be countersigned by the joiner. The anchor countersignature arriving after the author has moved on is accepted. Removal then re-add of the SAME key: a head issued while removed that is not the latest before re-add is refused; the latest one is accepted; a v1 head is accepted under rule 1; the export verifies (`r2_ok_countersigner_rule_edges_and_export_verifies`). The author and `verify` call the same function with the same `(seq, roster_v)` list. An author whose history holds `v_join` can only issue later heads at ≥ `v_join`, so the list cannot change the answer between storing and verifying (Reasoned). With no checkpoint before a join, `latest_before = None` and rule 2 refuses (Read). **The property test's generator does produce the round-1 failure:** a source mutation reverting both sides to round 1 (author: current roster; verify: head `roster_v` only) is killed by `a1_m2_prop_an_honest_authors_export_always_verifies` (N26), and so is the author-side revert alone (N27). Also killed: rule-edge mutants N09 (`<=` v_join), N10 (earliest instead of latest), N11 (any pre-join head). |
| **A-M3** | **CLOSED** | §1, §2. |
| **A-M4** | **CLOSED for heads and export; NOT CLOSED for "bound what a peer can make a member store" (R2-M1)** | Ran. Head cap boundary exact: 1,024 stored, the 1,025th refused `TooManyHeads`, an equal sequence number refused `StaleHead` (builder test plus mutants N12/N13 killed). Export at the store limit: in release, B received full-tier events with 4,000-byte summaries until `LogFull`: 9,937 events, store 58,594,135 bytes / 20,071 records. Bundle **58,594,727 bytes, verifies**. Export 0.42 s, parse 0.12 s, **verify 1.19 s**. Peak RSS of the whole test process 680 MB (store, chains, bundle, bytes and parsed copy together; verify alone not isolated). The 7/8 margin holds by construction (Reasoned): `ensure_room` reserves 4 + 65,535 bytes per record before any write, and no record can exceed 65,535 because `canonical::encode` refuses. Export writes only the stored records (deduplicated), one meta record and the seal, so a full store gives at most about 56 MiB + 1 KiB < 64 MiB and at most 229,378 < 262,144 records. **But:** the heads-seen path is unbounded per peer (R2-M1), and checkpointing stops for good after 1,024 heads per author (R2-m3). Denial of audit is SURFACED (`LogFull` from every call), not hidden. That is the right shape: refusing to log is safer for integrity than acting unlogged. It becomes a lever only because any one peer can trigger it cheaply. |
| A-m1 | CLOSED | `gate_heads_are_bounded_like_headers` passes; N20 killed. |
| A-m2 | **CLOSED for the 14 listed misses; new misses and over-masking in R2-m4** | `gate_redaction_misses` passes (all 14 fixed, positive controls still masked). |
| A-m3 | **CLOSED** | Release, under CPU contention: 11 hostile shapes (URL user-info, `@` floods after user-info, `mysql -p`, `export A=`, `-u a:b`, broken hex, short base64 lines, zero-width, `pass=`, `cookie:`, `a_key:`) give 64 KiB / 16 KiB time ratios of **3.7-4.0 (linear = 4)**, at most 3.7 ms at 64 KiB. Summary input refused above 16 KiB before redaction (`chain.rs:190`). That check is **unguarded**: N17 (raising it to 64×) survives every test (R2-n5). |
| A-m4 | CLOSED | M03 killed by two tests; AUDIT.md corrected. |
| A-m5 | Documented (AUDIT.md limits); reload a precondition (BACKLOG) | Read. |
| A-m6 | Deferred (BACKLOG) | see §7 |
| A-m7 | **CLOSED** | All 14 real survivors of round 1 are now killed by the branch's suite (table §6). |
| A-n3 | Partly: summaries filtered; headers remain (R2-m1) | Ran. |
| A-n5, A-n7 | CLOSED | `history_from_genesis`; count 75. |

## 5. New findings

| id | sev | file:line | what | how demonstrated | direction |
|---|---|---|---|---|---|
| **R2-M1** | **Major** | `session.rs:474-504` (`receive_heads_seen`: `persist` at 491 for every accepted record); `equivocation.rs:348-366` (reporter only needs to be a member AT the cited `roster_v`); `docs/AUDIT.md:244` | **A peer can fill an honest member's store and so stop that member's own audit log.** Every heads-seen record that verifies is written to the store, with no duplicate check, no "keep the latest per reporter", no quota and no rate limit. A record from a member removed at v that cites v-1 verifies forever. Identical replays are stored each time, although `export` later drops the duplicates. When the store is full, the member's own `record` returns `LogFull`, and AUDIT.md §1 says the daemon must then "end or pause the session's audit-class work". AUDIT.md §5 claims "a peer cannot grow a member's log", and the addendum asked for exactly that bound. Not hidden: `LogFull` surfaces. | `r2_finding_release_removed_member_fills_default_store` (release, default limits): a member **removed at v2** signs fresh empty records citing v1. **169,022 accepted in 8.7 s; store 58,654,792 bytes; then the victim's own `record` → `Err(LogFull)`.** `r2_finding_replayed_heads_seen_fills_the_store_and_stops_own_logging` (debug, limit lowered by 2 MB): **one** honest 328-byte record replayed 5,575 times, each stored, then own `record` → `LogFull`. Zero new signatures were needed for the replay. | Store a heads-seen record only when it is new: refuse exact duplicates, and keep at most the latest record per (reporter, recipient), replacing older ones in the export (or store just the evidence it produced). Refuse records from a reporter no longer on the current roster unless their `roster_v` is before its removal AND none is held from it yet. Give every peer-induced record kind (events with their receipts, heads, heads-seen, evidence) a quota per peer, so a hostile peer can exhaust only its own share and an honest member's own chain keeps room. Correct AUDIT.md §5. Add guards and red rows. |
| R2-m1 | Minor | `session.rs:250-276` (`outgoing`); `docs/AUDIT.md:136-140` | **Receipt headers give a `nothing` member the exact count and per-event time of an author's events.** Quantified: C at `nothing` for X and at `full` (or `summaries`) for B receives one B receipt header per X event that B stored. It carries type `audit.receipt`, B's receive time to the millisecond, B's sequence number and the commitments. The summary naming X is withheld. In a three-member session C can discount its own events, so this is **always exact**, not "sometimes" as AUDIT.md says. With more members, C learns the total across the authors whose events B stored. | `r2_finding_receipt_headers_give_a_nothing_member_count_and_time_of_each_event`: X's 5 events at +100/250/400/700/1300 ms → C holds 5 receipts at 101/251/401/701/1301 ms. | Design owner (BACKLOG has it): batch or delay receipts, or keep receipts out of the chain shared with members. Meanwhile correct AUDIT.md: "count and time of each event an author disclosed to another member you share with". |
| R2-m2 | Minor | `session.rs:165-183` (`note_share_level` / `known_level`) | **The share-level input that A-B1 rests on is a bare triple.** No author signature, no roster-version binding, no link to X's signed `member.accepted` event. It also survives the member's removal and re-add under the same key. With a wrong value, honest B sends X's header to C (at `nothing`), and C's `receive_heads_seen` accepts it and exports it. This is stated in AUDIT.md ("supplied, not proven") and BACKLOG, so Minor. It is the one place where tier confidentiality depends on daemon code that does not exist yet. | `r2_finding_share_level_input_is_unauthenticated`: C holds and exports "seq 4 type request.new ts …900Z" of X. `r2_finding_known_level_survives_removal_and_readd`: after remove and re-add, `known_level(X, C)` is still `Full`. | Take X's verified `member.accepted` audit event (signed header plus summary opening) instead of a triple; or make the BACKLOG entry an explicit precondition of daemon wiring with a test. Drop known levels for a member on its removal. `heads_seen_for(recipient)` must be fed the channel's authenticated peer key (the library cannot check who asks). |
| R2-m3 | Minor | `received.rs:38-41, 458` | **Checkpointing ends for good after 1,024 heads per author.** Receivers refuse every later head with `TooManyHeads`, so nothing the author records afterwards is ever countersigned. Its tail stays droppable at export (a stated limit). The author is not told. At the default 60 s, that is about 17 h of activity. AUDIT.md gives the cap but not this consequence. | `r2_finding_checkpointing_ends_after_the_per_author_cap`: refused from seq 1,025. | Keep the latest N heads (drop the oldest that are not anchors) instead of refusing, or document it with the 17 h figure and surface it to the author. |
| R2-m4 | Minor | `redact.rs:55-64, 145-161` and the hex and assignment patterns | **Redaction: new over-masking and misses.** Over-masking of ordinary text: the name part `pass` matches inside `compass:`, `bypass:`, `passenger_count=` and `password_min_length=12`. Hex runs of 16 or more mask git SHAs, sha256 checksums and a UUID. `mysql … -p appdb` masks the database name. **Format-character stripping rewrites ALL output**, not only matches: Persian ZWNJ, emoji ZWJ sequences and Hebrew RLM are removed even where nothing is masked. Misses (11 of my 18 new shapes): `docker login -p pw`; `.netrc` `password pw`; a Cyrillic homoglyph in `password`; tag characters U+E0020; bidi isolates U+2066-2069; variation selector U+FE0F; combining grapheme joiner U+034F; Hangul filler U+3164 inside a token; a 12-digit hex key; SQL `WITH PASSWORD '…'`; `htpasswd -b`. Masked as expected: `PGPASSWORD=`, `--password x`, `X-Api-Key:`, `?access_token=`, JSON `secret`, YAML `api_key: '…'`, lower-case `authorization:`. | `r2_report_redaction_over_masking_of_ordinary_text`, `r2_report_redaction_misses_new_shapes` (printed results). | Match on the stripped text but mask ranges mapped back onto the original, so output keeps its format characters. Strip the whole Cf category plus the variation selectors, CGJ and the Hangul fillers. Match name parts at word or underscore boundaries. Keep calling it a seatbelt. |
| R2-n1 | Note | `tests/gate_attacks.rs` (edited) | Two round-1 gate tests no longer go red on the regression they were written for (§1). Covered by builder tests, red rows and my r2 tests. | red-control runs on `gate` | Keep `r2_ok_*` as their replacements. |
| R2-n2 | Note | `session.rs:485-487` | `RosterBehind(v)` is permanent for any v below the first version a member holds (a joiner can never process a record made before it joined), and there is no buffering for a v that is ahead. | Read | Name the low case differently; the daemon must resend ahead records after a roster update. |
| R2-n3 | Note | `bundle.rs:935-941` | `equivocations.contains` is O(found × evidence). With the caps now 4× larger, a hostile bundle within 64 MiB can force on the order of 10^8-10^9 struct comparisons (seconds). A valid maximum bundle verifies in 1.19 s. | Reasoned; valid case measured | Use a `BTreeSet` of encoded evidence. |
| R2-n4 | Note | `identity.rs:373-381` | The crypto crate's all-pairs list is hand-kept; nothing ties it to the enum. | Read | Build the list from an exhaustive `match` so a new variant fails to compile until listed. |
| R2-n5 | Note | tests | New delta checks with no test that fails when they are removed: N07 (entry author's membership at `roster_v`), N15 (default store limit = full cap; only release-scale), N16 (export cap boundary), N17 (summary pre-size cap), N21 (`verify` refusing a record addressed to another member), N22 (`verify` "version not held": the following `member_in` check catches it, so near-equivalent). The code is correct at each site (Read). | mutation table §6 | One guard each. |
| R2-n6 | Note | `session.rs:500-502`, 490 | `ensure_room` reserves 2 records per entry, but `compare` can return more evidence per entry. That is harmless: the byte reservation is 64 KiB per record and the record count has 32,768 of slack. | Reasoned | none |

## 6. Mutation testing

Drivers: `gate_audit_tests_r2/mutate_r2.py`. Round 1's 42 mutants were re-applied, 16 of them adapted
to changed source text with the same semantics (marked [adapted] in the driver). There are 27 new
mutants. Each was applied alone to a pristine clone, run with `cargo test -p coagent-audit
--no-fail-fast` (plus `-p coagent-crypto` for crypto mutants), and reverted with `git checkout`. Survivors
were then run against my `gate_r2.rs`.

**Round-1 mutants at 4c39916: 40 of 42 killed by the branch's suite. M05 and M06 survive (equivalent or
near-equivalent, as in round 1).** All 14 real round-1 survivors (M13-M15, M18-M20, M24-M26, M28, M35, M40-M42)
are now killed by the builder's `gate_return.rs` guards. M16, M33, M38 and M39 are killed by the gate's
`gate_ok_receiver_reports_head_conflicts…`. M30 (the `AuditDomain::label` doc table) is killed only by the
unit test. That function is documentation now; the real labels live in the crypto crate (N18, N25).

**New mutants (branch suite, then my tests):**

| id | mutation | branch suite | my tests |
|---|---|---|---|
| N01 | `known_level` default Full | killed (a1_b1 scan, gate tier test) | — |
| N02 | `receive_heads_seen` accepts a record addressed to another member | **SURVIVED** | killed: `r2_ok_forwarded_addressed_record_is_refused_and_not_stored` |
| N03 | header in broadcast accepted | killed | — |
| N04 | `heads_seen_for` headers to `nothing` | killed | — |
| N05 | summaries recipient gets checkpoints only | killed | — |
| N06 | reporter membership BY instead of AT `roster_v` (a removed member reporting at a later version) | **SURVIVED** | killed: `r2_ok_readd_under_a_new_key` |
| N07 | entry author's membership not checked | **SURVIVED** | **SURVIVED** |
| N08 | `RosterBehind` check dropped | killed | — |
| N09 | countersigner rule `<=` v_join | killed (property test) | — |
| N10 | earliest pre-join head instead of latest | killed | — |
| N11 | any pre-join head | killed | — |
| N12 | head cap `>` | killed | — |
| N13 | StaleHead `<` | killed | — |
| N14 | `ensure_room` counts frame headers only | killed | — |
| N15 | default store limit = full bundle cap | **SURVIVED** | **SURVIVED** (only my release test would see it) |
| N16 | export cap comparisons +1 | **SURVIVED** | **SURVIVED** |
| N17 | summary pre-size 64× instead of 4× | **SURVIVED** | **SURVIVED** |
| N18 | crypto label heads-seen = head | killed (both crypto tests and the audit tests) | — |
| N19 | receipt summary to anyone | killed | — |
| N20 | `accept_head` MAX_SEQ dropped | killed | — |
| N21 | `verify` accepts a record addressed to another member | **SURVIVED** | **SURVIVED** |
| N22 | `verify` "version not held" dropped | **SURVIVED** | **SURVIVED** (near-equivalent: the next membership check refuses) |
| N23 | `heads_seen_for` keeps the recipient's own chain | killed | — |
| N24 | `member_by` strictly before v | killed | — |
| N25 | crypto label bundle-seal = binding | killed | — |
| N26 | A-M2 full revert to round 1 (author: current roster; verify: head `roster_v`) | **killed by the property test** and 3 others | — |
| N27 | A-M2 author-side revert only | killed by the property test and 2 others | — |

**Totals:** branch suite kills 19 of 27 new mutants; my tests kill 2 of the 8 survivors (N02, N06). That leaves
**6 surviving every test**: N07, N15, N16, N17, N21 and the near-equivalent N22 (R2-n5).

## 7. Deferred items: should they block a library merge?

- **A-m6 (no re-anchor), BACKLOG:** liveness only. Does not block a library nothing calls.
- **Crash recovery = equivocation; no reload from the store:** stated in AUDIT.md and BACKLOG as a
  precondition of daemon wiring. Does not block the library. It **must** block wiring.
- **Raised caps (64 MiB / 262,144):** measured fine for a valid maximum bundle (1.19 s verify). The hard
  limit is an honest design choice, recorded as DESIGN QUESTION 15. Not blocking.
- **Other authors' share levels (R2-m2) and receipt batching (R2-m1):** design owner and daemon. They do not
  block the library if the daemon precondition is written down. They do block wiring.
- **R2-M1 is not a deferral.** The addendum asked for the bound and the docs claim it. It blocks under this
  gate's rule (a documented property that does not hold). The fix is local to `receive_heads_seen` plus a
  quota per peer, and does not change any wire format.

## 8. What this log can and cannot prove, and what each member can learn (corrected)

> Each participant's computer keeps a signed, numbered record of what it reported doing. **It can prove**
> that a participant signed a given record, in that order. Once another member has countersigned one of
> its checkpoints, it can prove that nothing up to that point was changed or removed since. If a
> participant told two members different stories and those members compared notes, the result is proof
> anyone can check with the session's member list. Members who join or leave later do not break that
> comparison.
>
> **It cannot prove** that a participant recorded everything it did, that timestamps are true, or that
> nothing was dropped after its last countersigned checkpoint. It says nothing about members who never
> compared notes. The organiser key named in an exported file must be compared by you. A
> countersignature means "this matched what I had". A participant whose computer loses its record and
> starts again looks exactly like one who lied. After about 1,024 checkpoints (about 17 hours of activity
> at the default pace) a participant's later records are no longer countersigned.
>
> **What another member learns about you.** If you share **nothing** with them: how many events you had at
> each checkpoint and roughly when. **And, through the receipts of any member who receives your events
> and shares with them, the number of events you sent that member and the moment of each one, to the
> millisecond. In a three-person session that is exact.** Never your event types, contents or summaries.
> At **summaries**: also each event's type, local time and summary, never the full preview. This holds
> only while the software is told your sharing levels correctly. Those levels are not yet taken from
> your own signed statement.
>
> **In this build (4c39916), additionally:** any other member can fill your log on purpose in seconds.
> After that your computer can record nothing more for that session.
>
> Previews and summaries are scrubbed of text that looks like a password or key. The scrubber still
> misses many shapes (`docker login -p`, `.netrc`, look-alike letters, some invisible characters). It
> also blanks harmless words such as `compass:` and long hex values such as commit ids, and removes
> invisible joining characters some languages and emoji need. Treat it as a seatbelt.

## 9. What I did not examine

- Linux and Windows; a fuzzer on `Bundle::parse`; a hostile maximum bundle built to maximise
  `equivocations.contains` (R2-n3 is reasoned).
- The core red-control runner on the merged tree (run on the branch only; the merged tree passed
  check.sh).
- Memory of `verify` alone (only the whole test process was measured: 680 MB peak).
- `SignedHeader::from_envelope` and the daemon and channel integration (none exists).
- The internals of the canonical decoder, `verify_strict` and the roster crate beyond the paths used.
- Convener removal (reasoned from the roster rules, not tested).

## 10. Ran or reasoned

**Ran:** check.sh (branch and merged tree); both red-control runners; the gate's 15 debug and 2
release-ignored tests; 19 attack tests of my own (16 debug, 3 release-ignored); red controls
`audit_under_binding`, `one_label` and `hs_current_roster` against `gate` and `gate_r2`; 69 mutants
(42 round-1, 27 new) against the branch suite; 10 survivors against my tests.
**Reasoned:** prefix-freeness and encoding injectivity (also exercised); the 7/8 export margin
(also measured at the limit); history growth and fork; that the author's and verify's rule inputs agree;
R2-n2, R2-n3, R2-n6; convener removal.

## 11. My own slips

- My first run of `r2_ok_readd_under_a_new_key` applied rosters the fixture had already applied (`Stale`).
  Fixed in my test.
- My first version of the replay test replayed a record with entries. `receive_heads_seen` reserves room
  for its entries, so it hit `LogFull` while the member's own one-record `record` still fitted. Re-run with
  an empty record; the claim in R2-M1 rests on the corrected run and on the release run.
- My first re-add attempts used out-of-range slots (`BadSlot`). Fixed in my test.
- To save time I stopped my first mutation driver after M42 and ran the new mutants from a second clone
  (`mut2`). The stop left N01's edit in the first clone's `session.rs`. I restored it with `git checkout`
  before reusing that clone, and its worktree was clean apart from my added test file.
- The redaction timings and the 8.7 s fill time were measured while mutation builds were running. The
  absolute numbers are pessimistic; the ratios are what matter.
- An earlier wait command was refused by a hook for a `=`-leading word. No effect.
