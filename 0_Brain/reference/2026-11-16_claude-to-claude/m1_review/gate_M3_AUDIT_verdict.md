NO GO at 1d4a55b24224cdf8196778e0fb5c23080068ae19

# QA gate M3-AUDIT: `coagent-audit` (branch `m3-audit`)

Independent tier-1 read, 2026-11-17. Findings only: nothing fixed, committed or pushed. My clone
`/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/1d34e9cf-ed94-49aa-ba4c-99451dcbbc42/scratchpad/gate_m3_audit/repo`
(`rev-parse HEAD` = 1d4a55b…, merge-base with main = 129914b). Attack tests:
`m1_review/gate_audit_tests/gate_attacks.rs` (drop into `crates/coagent-audit/tests/`) and the mutation
driver `gate_audit_tests/mutate.py`.

**Why NO GO:** one Blocker (the `nothing` tier leaks headers through heads-seen) and four Majors
(equivocation cross-check dies after any removal; a joiner's countersignature makes the author's own
honest export fail `verify`; the nested-domain argument is false for the crate's public signing API;
peers can grow a member's store without bound and `export` writes bundles its own `verify` refuses).
The construction core holds up well: every forgery, framing, cross-session, cross-kind and
malleability attempt I made against signatures and evidence was refused.

## Ruling on the nested-domain workaround (task item 2)

**The bytes the crate itself signs are safe; the public API is not, and REQUEST 1 should land
before this merges.**

- How the bytes are built. `coagent-crypto` signs `label ‖ 0x00 ‖ msg` with `verify_strict`
  (`identity.rs:45-51, 271-281`). A binding is `"coagent-binding-v1" ‖ 0 ‖ noise_static(32)`
  (`identity.rs:104-107, 304-317`). A roster is `"coagent-roster-v1" ‖ 0 ‖ canonical(RosterBody)`
  (`roster/lib.rs:162, 307`). The audit crate signs `"coagent-binding-v1" ‖ 0 ‖ audit_label ‖ 0 ‖
  canonical(body)` (`domain.rs:76-107`). The labels contain no zero byte, so `label ‖ 0` is
  prefix-free. Roster and binding differ at byte 8.
- What I tried, all refused (tests pass): every object kind (header, head, countersignature,
  heads-seen, seal) verified under each of the other four labels, under bare `Binding` and under
  `Roster` (with and without the nested label); a real roster signature as every audit kind
  (`gate_ok_domain_every_kind_refused_under_every_other_label`); a real binding as every audit kind
  (builder `test2_a_binding_signature_is_never_an_audit_signature_and_vice_versa`); cross-session
  and cross-author evidence (`gate_ok_cross_session_statements_never_form_evidence`); Ed25519 S+L
  malleation used to mint a second header (`gate_ok_malleated_signature_cannot_frame_the_author`).
  Every signed body is canonical JSON that names its session and its signer; the canonical decoder
  re-encodes and compares, so there is no ambiguous concatenation.
- **What breaks (finding A-M3):** `domain::sign`, `domain::verify` and `nested_message` are `pub` and
  take any bytes. The argument "every audit message is longer than 32 bytes" constrains the crate's
  CALLERS, not the function. A message of `31 - label_len` bytes nests to exactly 32 bytes, and
  `verify_device` accepts the result as a device binding of the signer's key. This works for all
  five labels (`gate_domain_no_audit_domain_signature_is_a_valid_binding`). No code path in the
  crate produces such a message today, and the forged binding names a Noise key with a fixed
  22-to-28-byte prefix whose private key nobody knows. That keeps it at Major, not Blocker. But
  `docs/AUDIT.md` §3 and `CRYPTO-GLUE.md` G-17 claim it cannot happen.
- **Ruling:** land REQUEST 1 (five real `SignDomain` values) **before any audit log exists**.
  Changing a domain later changes every signature and orphans every stored log. The fallback, if
  REQUEST 1 cannot land first: make `sign`, `verify` and `nested_message` `pub(crate)` and refuse
  any message whose nested length is ≤ 32. That needs the design owner's acceptance, because the
  pinned values and the wire signatures change either way.

## Findings

| id | sev | file:line | what | how demonstrated | direction |
|---|---|---|---|---|---|
| A-B1 | **Blocker** | `session.rs:284-301`, `received.rs:282-294`, `equivocation.rs:276-283`, `session.rs:305-327` | **Tier confidentiality break.** `audit.heads.seen` carries each author's whole signed **header** (`type`, `ts`, which tiers exist, commitments) and goes to every member. A member at `nothing` for that author therefore holds its headers. That contradicts 04 §3.9 ("nothing: periodic checkpoints only"), 04 §3.8 (heads-seen = "highest author_seq and hash"), threat row L, and `docs/AUDIT.md` §2 ("cannot prove anything about any event's … type"). This is DESIGN QUESTION 4's reading. The builder's own test misses it because it scans only `PeerEvent` records (`tests/tiers.rs:152-157`). | `gate_tier_nothing_member_never_holds_a_header_of_that_author` FAILS: in the builder's own `scenario(3)`, C (at `nothing` for B) holds `seq 5 type "request.new" ts 2026-11-17T03:04:06.002Z` of B in its store and bundle. | Heads-seen entries must carry only what every member may hold: `Statement::Head` (checkpoints go to everyone), or `(author_seq, hash)` as 04 §3.8 says, with statements fetched on mismatch. Design-owner decision (reverses DESIGN Q4). Add a test that scans every record kind of a `nothing` member's store. |
| A-M1 | **Major** | `session.rs:288-292, 309-310`; `equivocation.rs:345` | **Equivocation cross-check stops working after any member removal.** `heads_seen` reports every peer chain ever held, removed authors included. `receive_heads_seen` verifies every entry against the CURRENT roster, so every record that mentions a removed author is refused, and every honest member holding one is reporting such records. The error is also mislabelled: `NotAMember` is mapped to `BadSignature`. | `gate_heads_seen_still_catches_equivocation_after_a_member_is_removed` FAILS. A equivocates between B and C; without a removal C gets 1 evidence (control); after removing an unrelated member D: `Err(BadSignature)`, no evidence. | Verify heads-seen entries against the roster HISTORY (as `bundle::verify` already does with `KeyBook`), or omit removed authors. Report `NotMember` as itself. |
| A-M2 | **Major** | `chain.rs:331-334, 356-384`; `session.rs:265-281`; `bundle.rs:820-822` | **An honest author's own export fails `verify`.** `checkpoint_now` hands a joiner the EXISTING last head, issued at an older `roster_v` that does not list the joiner. The joiner's `receive_head` countersigns on `Replay`. `AuthorChain::add_countersignature` checks the CURRENT roster and stores it. `verify` checks membership at the head's `roster_v` and refuses the whole bundle. Any newly added member can do the same deliberately to any older head (heads go to everyone), which is a cheap way to break an author's export. | `gate_an_honest_authors_export_verifies_after_a_joiner_countersigns` FAILS: `VerifyError { class: Countersignature, what: "countersigner not a member at that roster version", seq: 2 }`. | Apply one rule on both sides: the author refuses a countersigner who is not a member at `head.roster_v`. Issue a fresh anchor at the current roster version. A member should not countersign heads from versions it was not on. |
| A-M3 | **Major** | `domain.rs:76, 94, 99` | Nested-domain safety does not hold for the public API (see the ruling above). | `gate_domain_no_audit_domain_signature_is_a_valid_binding` FAILS for all five labels (`verify_device` returns Ok). | REQUEST 1 before merge, or `pub(crate)` plus a length guard. Correct `AUDIT.md` §3 and G-17. |
| A-M4 | **Major** | `received.rs:399-430`; `session.rs:265-281`; `bundle.rs:1104-1213` | **Unbounded storage, and an export its own verifier refuses.** `accept_head` stores (and `receive_head` countersigns and persists) any author-signed head, with no limit on count and no relation to held events. `export_records` does not enforce `MAX_RECORDS` or `MAX_BUNDLE_BYTES`. Honest sessions reach the cap too: measured 1,956 bytes and 2 records per received full-tier event, so 16 MiB is reached after about 8,600 received events in all, roughly 1,200 per other author in an 8-member session. | `gate_a_peer_cannot_push_an_honest_members_export_past_the_verifier_caps` (`--release --ignored`) FAILS: 65,537 heads give a **27,385,758-byte** export that the member's own parser refuses ("bundle larger than the cap"). Sizes: `gate_measure_export_bytes_per_received_event`. | Bound stored heads (e.g. keep only the latest N beyond held events, refuse heads beyond `MAX_SEQ`). `export` must refuse or split at the caps. Size the caps (DESIGN Q13) against real sessions, or make the format multi-part. |
| A-m1 | Minor | `received.rs:399-412` | `accept_head` does not apply the 2^62 sequence bound that `accept`, `join` and `verify` apply. A head at `u64::MAX` is stored, countersigned and exported. No panic followed in heads-seen, export, `verify` or `receive_heads_seen` (checked). | `gate_heads_are_bounded_like_headers` FAILS (Ok(Countersignature{author_seq: 18446744073709551615…})). | Same `MAX_SEQ` check in `accept_head`. |
| A-m2 | Minor | `redact.rs:122-533` | Redaction misses cheap, common shapes: `curl -u admin:pw`; JSON `"pass"`/`"pw"`; `passphrase:`; lower-case `export db_pass=`; single-letter `export P=`; `mysql -ppw`; `sshpass -p pw`; URL passwords containing `/` or `@` (part of the password survives); a zero-width space inside a token or a key name; base64 key material wrapped below 24 columns without a PEM header. Masked as expected: AWS secret, connection-string `Password=`, JWT, URL user:pass, multi-line PEM, `Authorization:`, Slack, Stripe, JSON `"password"`, `export DB_PASSWORD=`. Redaction runs before truncation and before hashing, and summaries are redacted too. A secret straddling the 240-character cut is masked whole (redaction runs over the full 64 KiB window first). | `gate_redaction_misses` FAILS listing 14 misses (`short hex key` is debatable). | Add `-u user:pass`, `-p<pw>`, `pass`/`pw`/`passphrase`, lower-case env names, and Unicode format characters stripped before matching. Keep saying plainly that pattern redaction cannot be complete. |
| A-m3 | Minor | `redact.rs:326-347` (`line_headers`), `364-380` (`value_range`); `chain.rs:186-191` | Redaction is **quadratic**: each match scans to end of line. The summary is redacted **before** its 4,096-byte limit is checked, so its cost is unbounded in the input size. Release build: `cookie:` repeated over 64, 128 and 256 KiB took 218, 866 and 3,503 ms; `a_key:"x" ` took 69, 266 and 1,063 ms. The full-tier preview is bounded by the 64 KiB window (about 0.2 s release per hostile event). | `gate_redaction_time_scales_linearly` (`--release --ignored`) FAILS (16× time for 4× input). | Compute line ends once; cap summary input (e.g. 4× `MAX_SUMMARY_BYTES`) before redacting. |
| A-m4 | Minor | `bundle.rs:664`; `docs/AUDIT.md` §4 | The builder's "EQUIVALENT mutant" claim for `verify`'s sequence check is **false** against the key holder. An author or re-sealing exporter can sign a properly linked chain numbered 1, 2, 2. Without the check, `verify` accepts it and reports `last_seq: 3`. No builder test covers this. | Mutant M03 SURVIVES the builder suite; `gate_ok_verify_refuses_a_linked_chain_with_a_repeated_sequence_number` kills it (passes on the real code). | Add that test; correct `AUDIT.md` §4. |
| A-m5 | Minor | `docs/AUDIT.md` §2 | Undocumented consequence: an honest author whose daemon loses its chain and re-records event n produces valid, transferable equivocation evidence against itself. This is the right outcome for the construction, but users need to be told, and `SessionAudit` cannot yet reload from its `Store` (BACKLOG), so a restart today means exactly this. | `gate_note_crash_recovery_is_indistinguishable_from_equivocation` (passes: evidence verifies). | State it in the limits list; make store reload a precondition of daemon wiring. |
| A-m6 | Minor | `session.rs:201-215, 249-261` | No re-anchor path. If a joiner receives any event of an author before `join_author`, a from-genesis view is created and `join_author` is then refused (`Replay`). A stale but genuine anchor also leaves the view refusing every live event as `Gap` forever. Liveness only. | reasoning only | Allow re-anchoring to a later author-signed head while nothing is held after the old one. |
| A-n1 | Note | `received.rs:343-359` | Watermark: no denial of service found. A non-author or another session cannot move it (checks run first), and reordered honest delivery is accepted once in order. There is no buffering: reordered delivery needs transport redelivery. | `gate_ok_watermark_cannot_be_used_to_refuse_honest_delivery` passes. | none |
| A-n2 | Note | `tiers.rs:79-87`, `header.rs:123-128` | Neither commitments nor chain hashes carry a label. The two tiers share one commitment function, and the chain hash has the same `32 bytes ‖ data` shape. Each split is unambiguous (fixed 32-byte prefix), and no code compares a commitment with a chain hash, so I found no cross-use. A label per tier would cost nothing now and change pinned values later. | reasoning | design owner, together with REQUEST 1 |
| A-n3 | Note | `session.rs:229-237` (receipts) | Receipts tell a member who is at `summaries` for the receiver, but `nothing` for the original author, the existence and receipt time of each of that author's events. That is finer than threat row L's "checkpoints reveal counts and roughly when". | reasoning | design owner: state it, or batch receipts |
| A-n4 | Note | `bundle.rs:791` | `verify` requires own-head `roster_v` to be non-decreasing and ≤ the last version, not current. An author colluding with a removed member can keep issuing heads at the old version and collect "attestations" after the removal. This only affects the author's own claims. | reasoning | state, or bind `roster_v` to the roster version current at the head's sequence |
| A-n5 | Note | `bundle.rs:709-760` | A hostile exporter can start its bundle at any roster version that lists it, dropping the earlier history, or fabricate a whole session under its own convener key. Both are stated limits: `Report.convener` must be compared, and `roster_versions.0 ≠ 1` is visible but not flagged. | reasoning | flag `v_first ≠ 1` in the report |
| A-n6 | Note | `session.rs:265-281` | A countersignature attests "I hold this head and it conflicted with nothing I hold". A `nothing` member, or one that is behind, countersigns heads it cannot check. `AUDIT.md` is accurate; the user-facing wording below says so. | reasoning | none |
| A-n7 | Note | `docs/AUDIT.md` §4 | AUDIT.md says the runner has 42 rows; it has 43 (STATUS says 43). | read | fix the count |
| A-n8 | Note | `scripts/red-controls-audit.sh` | One file outside the listed scope (new script). STATUS declares it; harmless. | `git diff --stat` | none |
| A-n9 | Note | `checkpoint.rs:197` | Mutant M05 (drop the session comparison in `Countersignature::attests`) is equivalent at both current call sites (each checks the session separately), but `attests` is `pub`. | mutation | keep, or add a direct unit test |

## What this log can and cannot prove (plain language, corrected for this gate)

> Each participant's computer keeps a signed, numbered record of what it reported doing in the
> session. **It can prove** that a participant signed a given record, in that order. Once another
> member has countersigned one of that participant's checkpoints, it can also prove that the
> participant has not changed or removed records up to that point since. If a participant showed two
> members different versions of its record, and those two members compared notes, the result is
> proof that anyone can check with the session's member list.
>
> **It cannot prove** that a participant's computer recorded everything it did (only what it chose
> to sign), that timestamps are true, or that nothing was dropped from the end of a record after
> its last countersigned checkpoint. It says nothing about members who never compared notes. It
> cannot tell you that the organiser key named in an exported file is the one you trust: compare it
> yourself. A countersignature means "this matched what I had", not "I checked everything". If a
> participant's computer loses its record and starts again, the restart looks exactly like lying.
>
> Previews and summaries are scrubbed of text that looks like a password or key, but the scrubber
> works from patterns and misses many real secrets (`curl -u user:pass`, `mysql -pSECRET`, plain
> words used as passwords, secrets split by invisible characters). Treat it as a seatbelt.
>
> **In this build (1d4a55b), additionally:** a member you share *nothing* with still learns the
> type and time of your events through other members' cross-check messages; after any member is
> removed, the cross-check stops catching anyone; and a long or flooded session can produce an
> export that the verifier refuses.

## Reproduction

- `scripts/check.sh` in my clone, with `CARGO_TARGET_DIR` in my scratch dir: **exit 0**, "CHECK OK:
  fmt, clippy, test, deny all passed". Workspace **146** tests passed, 0 failed. `coagent-audit`:
  **45** (3 unit + 42 integration: alloc_cap 1, bundle 7, countersign 3, determinism 4,
  equivocation 5, join_leave 3, no_content_in_debug 1, receive 3, redaction 4, signing 5, tamper 3,
  tiers 3). This matches STATUS.
- Red controls: the builder's runner, with only `CARGO_TARGET_DIR` and `LOGDIR` repointed to my
  scratch dir: **43 of 43 RED**, then "GREEN: 45 tests ok", "RED CONTROLS OK". I read the first
  panic message of every row. Each fails on its named property, not a side effect. Weak evidence
  strings ("Gap", "shows", "order", "peak") were checked against the full assertion text:
  `recv_accept_gap` → `Ok(Accepted{seq:6})` vs `Err(Gap)`; `debug_raw` → "SessionAudit shows the
  redacted credential"; `export_store_order` → bundle bytes differ for "member 0, order 0";
  `parse_no_frame_cap` → "claim 0x7fffffff: peak 2147483647 bytes". `seq_unbounded` goes red on
  "attempt to add with overflow", which IS its property (extreme numbers never panic).
- Scope against merge-base 129914b: 35 files, +7,925/−0. Only `crates/coagent-audit/**`,
  `docs/AUDIT.md`, `docs/CRYPTO-GLUE.md` (appended), `BACKLOG.md` (6 entries appended), one
  `members` line in root `Cargo.toml`, `Cargo.lock` (+16 lines: only the `coagent-audit` package,
  no new crate), and `scripts/red-controls-audit.sh` (A-n8). OK.
- `unsafe`: only `tests/alloc_cap.rs:24-37`, a test binary. The library is
  `#![forbid(unsafe_code)]`. The allocator is sound: it forwards `alloc` and `dealloc` to `System`
  with the same `Layout`, allocates nothing itself, uses atomic counters only, and the default
  `realloc`/`alloc_zeroed` route through the counted methods (a conservative over-count during a
  move).
- Determinism: the source scan for clock, env, `HashMap`/`HashSet`, rand and chrono is clean
  under `src/`. Every map is a `BTreeMap`, and time is passed in. Edge cases (Note level):
  `export_records` keeps the first-stored record for a duplicate key with DIFFERENT content (only
  in an abnormal store), and `sort_evidence` falls back to an empty key on an encoding failure.
- Hostile bundle parsing: every truncation of a real bundle is refused without panic
  (`gate_ok_every_truncation_of_a_real_bundle_is_refused_without_panic`, a 12-13 KB bundle swept at
  every byte), and so is trailing garbage. Duplicate records, records for unknown authors and mixed
  sessions are refused by the strict section and order checks plus the per-record session, author
  and roster checks (read, `bundle.rs:440-533, 709-954`). The builder's corruption, allocation and
  extreme-number tests pass. I did not time a maximal VALID bundle. By reading, `verify` is linear
  except `equivocations.contains` (`bundle.rs:933`), which is O(found × evidence), bounded by the
  16 MiB cap at roughly 10^8 cheap comparisons.

## Mutation testing (my mutants, one at a time, builder's full crate suite)

MUTATION_TABLE_PLACEHOLDER

## Builder's DESIGN QUESTIONS and REQUESTS

| # | Reading implemented | Ruling |
|---|---|---|
| Q1 | `sig` inside the hashed header | **Safe.** `verify_strict` rejects non-canonical S (S+L test) and small-order keys; signing is deterministic, so nobody but the author can mint a second valid header for one body. An author who re-signs with new content or a new nonce produces a different hash, and that is (correctly) equivocation. It matches 04 literally. |
| Q2 | RFC 3339 ms UTC from passed-in time | Safe. |
| Q3 | head and countersignature carry `session_id, author, roster_v`; countersignature carries `by` | Safe and better, but it **changes the wire format** of `audit.head`: design owner. A-M2 shows the rule using `roster_v` must be applied on the author side too. |
| Q4 | heads-seen carries signed statements | **Not safe as built: A-B1.** Design owner. |
| Q5 | broken-link evidence | **Sound.** I could not frame an author: cross-session, cross-kind, malleated, joiner-anchor and agreeing head/header cases are all refused or yield nothing. The one self-incrimination is honest crash recovery (A-m5), which is right but must be documented. |
| Q6 | Gap/Reorder watermark | Safe (A-n1). |
| Q7 | summaries redacted, 4 KiB cap | Safe for confidentiality; the redact-before-cap order is the cost problem in A-m3. |
| Q8 | receipts as own-chain events, not receipted | Safe; disclosure granularity A-n3 for the design owner. |
| Q9 | time checkpoints only with a new event | Safe. |
| Q10 | seal and first-roster anchor | Limits stated correctly in AUDIT.md §2 ("stops outsiders, not the exporter"; "compare `Report.convener`"). Add the `v_first` flag (A-n5). |
| Q11 | envelope `sig` = header signature for audit-class types | Changes the meaning of a merged proto field: **design owner and proto owner**. Not examined end to end (no channel integration here). |
| Q12 | joiner refuses heads before its anchor | Safe; see A-m6 for re-anchoring. |
| Q13 | constants | Preview 240/3 stays a proposal. **Bundle caps are too small for real sessions and not enforced on export (A-M4).** |
| Q14 | no full capture | Fine per the brief. |
| R1 | five `SignDomain` values | **Should land before merge** (ruling above): cheap now, and it orphans stored logs if done later. Needs the crypto crate owner. |
| R2 | envelope `sig` doc | Needed; same owner as Q11. |
| R3 | `ForkEvidence::verify` | The current route is sound inside `verify_together`: `RosterChain::start` + `apply` under the convener key, cross-checked between the two bundles, and `apply` returns `Fork` only for a validly signed same-version roster. A third party holding only a `ForkEvidence` has no API, so add it. Not blocking. |

## What I did not examine

- The merged tree with current main (18005d6, M1 RELAY): not built or tested.
- `SignedHeader::from_envelope` against the real channel/proto signing path (Q11).
- Linux and Windows.
- A fuzzer run on `Bundle::parse`.
- Timing of `verify` on a maximal VALID bundle (reasoned only).
- The internals of the merged canonical decoder and of `ed25519-dalek` `verify_strict` (trusted as
  merged; I relied on their documented behaviour and the S+L test).
- The `coagent-roster` fork rules beyond the `apply` path the audit crate uses.

## Ran or reasoned

Ran: `check.sh`; the red-control runner (43 rows plus green); 16 attack tests in `gate_attacks.rs`
(14 in the debug suite plus 2 `--release --ignored`): 8 demonstrate findings (A-B1, A-M1, A-M2,
A-M3, A-M4, A-m1, A-m2, A-m3), 7 confirm refusals or documented outcomes, 1 is a measurement; the
mutation table. Reasoned only: A-m6, A-n2 to A-n6, the duplicate/unknown/mixed bundle cases, the
quadratic bound in `verify`, and the realistic-session cap estimate (from the measured per-event
growth).

## My own slips

- A first attempt at the M03 kill-check was refused by the workspace hook because the clone path
  was in a shell variable. Nothing ran; I re-ran it with the literal path.
- `gate_measure_*` first failed to compile (missing `Store` import). Fixed in my test file only.
- The red-control runner and the mutation driver ran from separate pristine clones with separate
  target dirs. My attack-test clone was never used for mutations, so the builder-suite mutation
  results do not include my tests unless the table says so.
