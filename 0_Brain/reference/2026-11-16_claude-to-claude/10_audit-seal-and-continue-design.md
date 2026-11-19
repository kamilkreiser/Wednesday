---
date: 2026-11-19
type: reference
source: security design agent commissioned by Friday; inputs are design 07 (whole), 05, 06 (§1, §8-§10), 03 §9.4, the audit verdicts r5, FIX, FIX2, FIX3 in m1_review/, and the coagent-audit crate, docs/AUDIT.md and BACKLOG.md at main 36537eb799a36e9c99860cfe952b52aee8700d95 (read with git show; nothing built, nothing run)
status: live (design for the owner's review and for briefing a build seat; NOT built)
project: General / CoAgent (no client)
---

# CoAgent audit log: "seal and continue", designed in full

**Authority.** Card audit-fixed-capacity-1117, the owner's option verbatim: "Fixed capacity now, seal and continue as the next piece". The fixed capacity is merged (main = `36537eb`). Design 07 §1.12 outlined seal and continue and marked it NOT built. The owner, 2026-11-19 21:17: "please keep working on the project overnight to get as far as you can". This document is the full design, written so that a build seat can be briefed from it.

**How to read the labels.** **[file:line]** means a line I read at `36537eb`, under `crates/coagent-audit/` unless another crate is named. **REASONED** means an argument from reading that no test has attacked. **(computed, not run)** marks a figure I worked out by arithmetic; no test produced it. **PROPOSED** marks a number I chose. **UNKNOWN** marks something I could not establish, together with what would settle it. "V" is the honest member whose computer we are describing. "Seat", "free part", "allowance" and "fixed part" are design 07's terms. Design 07's rulings I-A1 to I-A15 and its properties P1 to P9 bind this design. No part of 07 §1.4 to §1.10 is changed except where §2.9 says so (one slot size).

---

## 0. BLUF for the owner (plain words)

1. **What you get.** A session can now record for as long as it lasts. When your log fills up, or whenever you choose, your computer files the log so far away as a finished file that checks out on its own. It then carries on in the same session with the space empty again. Nobody has to reconnect, and nothing is sent to the other people.
2. **Only you decide when to file the log away.** Nobody else's activity can make your computer do it, stop it doing it, or make it fail.
3. **What stays true:**
   - Member-list changes always go through.
   - Proof that someone lied is always kept and always exported. It is carried into every later file.
   - Each person can fill only their own share of your space.
   - Every file you export checks out.
   - Your own log never re-uses a number, so a filing can never look like you lying.
4. **What it costs:**
   - **Disk.** You keep the filed-away files: up to 64 MB each. You choose how many to keep.
   - **One file proves less on its own.** A file now says "this session from item n onwards". Proving the whole session needs every file in order, and a new check, "verify all files together", does that.
   - **Old proof lives in the old files.** After a filing, your computer can catch someone telling two stories only about what they did after their latest checkpoint. Anything earlier is checked against the earlier file.
   - **The other people see it.** Your "I hold your log from item n" notes restart at the filing point.
5. **What still has a limit.** The member list itself: 256 changes and 32 people ever, per session. That is unchanged.
6. **Your decisions:** ten choices are marked `INTERPRETATION (for Kam)` in §7.1. The two that matter most:
   - **I-S1:** filing away is your act only. It never happens automatically because someone else filled their share. If it did, someone else could make your computer write files.
   - **I-S6:** each person files away on their own schedule, and nobody's filing forces anyone else's. The cost is that a computer that files less often than you stops keeping copies of your activity until it files too. It still witnesses your checkpoints.
7. **Top risks for the build:**
   - A crash in the middle of a filing (§2.8 makes this safe with one rule).
   - The exact sizes of a new fixed slot (§2.9; must be measured).
   - The program around the log must not let a peer's message trigger a filing (§2.1, a written precondition plus a red control).

---

## 1. What the code at 36537eb gives this design (the facts it rests on)

| # | Fact | Where |
|---|---|---|
| F1 | An author's own chain assumes it starts at number 1. `seq()` is the number of events held, a new event is numbered `seq()+1` with `prev_hash = last_hash`, and `restore` commits events from 1. | [src/chain.rs:155-157, 256-262, 446-487] |
| F2 | A received chain can already start at a signed checkpoint (the joiner's anchor). It refuses anything at or before it (`BeforeStart`), and `held_from` reports the first number held. | [src/received.rs:214-242, 297-300, 385-389, 493-497] |
| F3 | `verify` assumes the exporter's own chain starts at 1 with a zero `prev_hash`, and reports `own.first_seq = 1`. | [src/bundle.rs:773-781, 1033-1041] |
| F4 | `verify` refuses a countersignature whose checkpoint is not among the bundle's own checkpoints. | [src/bundle.rs:833-840] |
| F5 | A bundle's seal signs a digest of every earlier frame, so any record added to a bundle is covered by the exporter's existing seal signature. | [src/bundle.rs:283-289, 332-350, 1009-1026] |
| F6 | The store is keyed, with put, remove and list only. There is no transaction or batch, and `put` is durable before it returns. | [src/store.rs:46-62] |
| F7 | Export reads every stored record; `export_records` keeps a peer's checkpoints only above its anchor. | [src/session.rs:1989-1999; src/bundle.rs:1250-1267] |
| F8 | `resume` rebuilds a received chain from its anchor slot when one exists, otherwise from 1, and propagates any refusal (`c.accept(e)?`). | [src/session.rs:462-478] |
| F9 | The fixed part is seven tables, and capacity, seats and allowances are pure arithmetic on them. Table codes in the anchor wire format are positions in `Table::ALL`. | [src/budget.rs:57-146; src/anchor.rs:319-344] |
| F10 | Limits are never stored. The constructor and `try_set_limits` are the only writers, and every accepted limit is at most the defaults in every part (the defaults clause). | [src/session.rs:255, 612-668] |
| F11 | Cross-check records are compared with what is held and kept in their own slot. They never put another author's statement into that author's chain. | [src/session.rs:1846-1922] |
| F12 | The anchor tables replaced in place are Attestation, HeadsSeen, Anchor and LatestHead. A replaced slot passes when its order is newer. | [src/anchor.rs:133-157, 200-227] |
| F13 | There are five audit signing domains, one per signed object. | [src/domain.rs:25-56] |
| F14 | `archive_and_release` deletes the released key's records first, then writes its tombstone. | [src/session.rs:1944-1972] |

---

## 2. The construction

### 2.1 Who decides to seal, and what can never make it happen

- **Only V's caller seals**, by calling `seal_export` and then `seal_commit` (§2.2). No function that takes a peer's object, and no function other than these two, changes the segment number or removes a numbered record, apart from `archive_and_release`, which is V's act too. This is a crate property, tested as invariant S4 with red control `seal_on_receive`.
- **The crate cannot see why its caller seals.** "A peer can never force a seal" is therefore partly a property of the daemon, and is written as **daemon precondition D-S1**. The daemon's automatic seal policy may be driven only by:
  - the owner's command;
  - time;
  - V's own free part or own seat reaching a threshold.

  It may never be driven by a peer's seat, a requested allowance, or any peer message.
- **Why it matters (this is where a fifth instance of the class would come from).** Each seal writes a file of up to 64 MiB outside the store. A daemon that sealed whenever peer X's seat filled would let X make V's computer write files, and so fill V's archive disk with what X causes: "one party fills another party's storage" one level out (INTERPRETATION I-S1).
- **What X can cause V to archive is bounded.** Per seal, X's part of the file is at most X's seat, S = 5,097,490 bytes. The number of seals is V's alone. So X's archive cost is at most S × (the number of seals V chose to make) (computed, not run).
- **No seal can be refused for space**, and nothing a peer sends can make one fail (§3, invariant S5). The only refusals are:
  - `SealStale`: the store changed between the two calls; this is V's own interleaving (§2.2);
  - `NothingToSeal`: nothing would be removed;
  - a store error.

### 2.2 The steps, as the caller sees them

| Step | Call | Writes to the store | What it does |
|---|---|---|---|
| 0 (optional, recommended) | `checkpoint_now(id, now)` (exists) | one own checkpoint, charged exactly as today (I-A11 to I-A13) | Makes the newest own event the seal point. If it is refused `LogFull` (a full free part, or N1's seat), the seal still works from the latest stored own checkpoint (step 1). |
| 1 | `seal_export(&self, id) -> Result<SealPlan, AuditError>` | **none** (`&self`) | Computes the cut points (below). Builds segment k's bundle (the ordinary `export`, F7). Computes the Segment record of segment k+1 and the anchor the store will have after the seal (`post_anchor`). Records `pre_anchor = self.anchor()` inside the plan. |
| 2 | (daemon) persist `plan.bundle` durably; save `plan.post_anchor` beside the current anchor as "pending" | — | Precondition D-S3: the file is durable before step 3. |
| 3 | `seal_commit(&mut self, id, &plan, now) -> Result<SegmentInfo, AuditError>` | **one put** (the commit point), then best-effort collection | (a) Refuses with `SealStale` unless `self.anchor() == plan.pre_anchor`: nothing changed since step 1. (b) Puts the Segment record in its fixed slot. That put is the seal. (c) Rebuilds the member in memory from the store's **logical view** (§2.3), keeping the limits in force. (d) Collects garbage: puts each author's start in its Anchor slot and removes every physical key the logical view drops. A failure in (d) is not an error: the result says how many keys are left and the next seal collects them. |
| 4 | (daemon) promote the pending anchor to current; drop the old one | — | |
| — | `seal_cancel` is not needed | — | Step 1 writes nothing, so abandoning a plan costs nothing. A second `seal_export` simply makes a new plan. |

**Precondition D-S2 (daemon): no interleaving.** Between step 1 and step 3 the daemon makes no other mutating call on this member. Inbound messages are queued, bounded by the channel's own limits (D3). If the daemon breaks this, the result is `SealStale`, a safe refusal and never a loss (invariant S1). The rule also stops a peer that keeps sending from making every seal stale: the daemon does not process its messages inside the window.

**Cut points**, computed in `seal_export` from memory and a function of the store:

- **Own cut n₀.** n₀ is the number of the latest own checkpoint held. That is the newest stored own checkpoint, or the current segment's own start when no own checkpoint is newer, or none if V has never checkpointed. With none, the own chain is carried whole.
- **Peer cut c_X, for each other author X held** (current or removed). c_X is the newest checkpoint of X that V holds: from X's log, X's newest-checkpoint slot, or X's anchor, which is `newest_head()` [src/received.rs:343-346].
  - c_X is used only if it is newer than X's current anchor. Otherwise X is not cut.
  - X's events after c_X are kept and stay charged to X's seat. Without them V would expect c_X+1 again while X's live stream is ahead, and X's later events would be refused as a gap for ever.
  - INTERPRETATION I-S3 covers the choice of the newest checkpoint over the newest one V holds events up to.
- **NothingToSeal.** If no own record and no peer record would be dropped, `seal_export` refuses with `NothingToSeal`. This stops empty-segment loops caused by a caller bug.

### 2.3 The logical view: the one rule that makes the seal atomic

The store has no transaction (F6). So the seal is **one durable put** (the Segment record), and every reader works on a **logical view** of the physical store that this one rule defines:

> **Normalisation.** Let G be the Segment record in the store, if any.
> - **(own)** Drop every own event numbered ≤ G.own_start, every own checkpoint numbered ≤ G.own_start (the start itself lives in G), and every countersignature in the Attestation table whose checkpoint is numbered < G.own_start.
> - **(peer)** For each other author X, let eff_X be the newer of X's Anchor slot and G.starts[X]. Present eff_X as X's anchor (`Record::PeerStart` under X's Anchor key). Drop X's events and logged checkpoints numbered ≤ eff_X, and X's newest-checkpoint slot if it is numbered ≤ eff_X.
> - Nothing else is dropped. Rosters, the roster conflict, evidence, cross-check records and the Segment record itself are kept whole.

Normalisation is applied by `resume`, `resume_with_anchor`, `export`, `anchor()` and the accounting (`index`, `part_use`, `key_use`, `own_req`, `head_pay`, `fixed_digests`). Physical keys the view drops are **garbage**:

- garbage is not charged and not exported;
- `seal_commit` removes it in step 3(d);
- the next seal removes anything left;
- `resume` stays read-only (it writes nothing today [src/session.rs:329-493]; this design keeps that).

Why this is safe:

- **No loss without a file.** Everything the view drops is at or below a cut chosen in step 1. Every such record was in the store at step 1, so it is in `plan.bundle` (the plan's anchor equality is checked in step 3(a)).
- **No re-use of a number.** n₀ only moves forward, and own events after it are never dropped. If the Segment record itself were lost, `resume` would meet own events that do not start at 1 and refuse the store [src/chain.rs:233-241]. It would not restart at 1 and sign numbers again (the trap of gate A-m5).
- **Nothing accepted later is ever dropped.** After the seal, no record at or below a cut can be accepted:
  - own numbers only grow;
  - X's events ≤ eff_X are refused `BeforeStart` [src/received.rs:385-389];
  - X's checkpoints must advance past the newest held [src/received.rs:513-520];
  - a countersignature of an own checkpoint below n₀ finds no such checkpoint and is refused `UnknownHead` [src/chain.rs:518-520].

  So normalising again (at any resume, or at the next seal) never drops a record accepted after the seal (REASONED).
- **Existing invariants already agree with the rule.** A joiner's anchor or a release tombstone already has nothing at or below it in the store, because `join_author` and `archive_and_release` guarantee it. So the (peer) rule changes nothing for stores written before this build.

**Bonus, and a pre-existing fault this rule would close (REASONED, not run).**
- **The fault.** `archive_and_release` deletes X's events in key order and writes the tombstone last [src/session.rs:1944-1972]. A process stop part-way through leaves X's surviving events starting above 1 with no Anchor slot. `resume` then builds X's chain from 1 [src/session.rs:465] and propagates the `Gap` its first `accept` returns [src/session.rs:468; src/received.rs:412-427]. The store cannot be resumed, so "re-running the release completes it" (BACKLOG, `archive_and_release` entry) is not reachable after a stop.
- **The fix.** If release wrote the tombstone first and relied on normalisation, it would be crash-safe. Design question DQ-S3.

### 2.4 New and reused signed bytes; signing domains

| Object | Signed by | Domain | Signed bytes | New? |
|---|---|---|---|---|
| Seal-point checkpoint (step 0) | V | `AuditHead` (`coagent-audit-head-v1`) [src/domain.rs:28, 51] | `label ‖ 0x00 ‖ canonical(HeadBody)` [src/checkpoint.rs:76-89] | **No.** An ordinary checkpoint, sent to every member as today. |
| V's next own event after the seal, number n₀+1 | V | `AuditHeader` | `canonical(HeaderBody)` with `prev_hash` = hash at n₀ | **No.** The chain simply continues: the hash at n₀ commits to everything before it. |
| Segment k's bundle | V | `AuditBundleSeal` | the seal over every frame [src/bundle.rs:332-350] | **No.** |
| Segment record (inside every later export of segment k+1) | not signed by itself; covered by the bundle seal of every export that carries it (F5) | `AuditBundleSeal`, through the seal | canonical `Record::Segment(SegmentRecord)` as one frame | **New record kind. No new signature or domain.** |
| `SegmentRecord.own_start` | V | `AuditHead` | an existing V checkpoint | reused object |
| `SegmentRecord.starts[X]` | X | `AuditHead` | an existing X checkpoint | reused object |
| Countersignature of the seal point by W | W | `AuditCountersign` | unchanged (with `held_from`) | **No.** |

**No request to the crypto lane is needed.** A separately signed "segment statement" (domain `AuditSegment`) would be needed only if peers were to countersign segment boundaries. This design does not need that, because the boundary is an ordinary checkpoint that peers already countersign. If the owner prefers it, it is REQUEST R-S1 to the crypto lane (the alternative under I-S4). Nothing here builds it.

**`SegmentRecord`** (canonical JSON, `deny_unknown_fields`):

```
SegmentRecord {
  segment:   u64,                  // k+1 (segment 0 = before any seal; it has no Segment record)
  prev:      Digest32,             // segment k's seal.digest (the digest its seal signs, src/bundle.rs:142-146)
  own_start: Option<SignedHead>,   // V's checkpoint at n0, or None (own chain carried from 1)
  starts:    Vec<SignedHead>,      // per other author cut, sorted by author key id, at most 31 (OTHER_KEYS)
}
```

Size: at most 32 checkpoints of at most 449 canonical bytes each (the measured largest checkpoint is 453 framed bytes, docs/AUDIT.md §1A U5) plus the number and the digest: about 14,565 framed bytes (computed, not run). UNKNOWN until measured: a test must build the largest one, with 31 starts and every number at u64::MAX (U-S1).

### 2.5 What each peer checks on receipt

**Nothing new reaches a peer.**
- The seal point is an ordinary checkpoint (receivers check it as today [src/session.rs:1726-1782]).
- V's events after the seal continue V's chain (receivers check them as today [src/received.rs:349-461]).
- No message announces a seal.

What a peer *observes*:
1. **V's countersignatures restart.** V's `held_from` for the peer's checkpoints restarts at that peer's start + 1, because V's view of the peer now begins there [src/received.rs:297-300]. It is truthful, and `verify` already accepts any `1 ≤ held_from ≤ author_seq` [src/checkpoint.rs:203-207] (INTERPRETATION I-S8).
2. **Old countersignatures are refused.** A countersignature the peer sends for one of V's checkpoints from before the seal is refused `UnknownHead` and nothing is stored.
3. **V's status says so.** V's `status()` shows the seats emptied. It is information, not proof (07 §1.8).

A joiner admitted after V sealed gets V's latest checkpoint as its anchor, as today. `prepare_head` returns the start when no event follows it [src/chain.rs:407-411], once AuthorChain knows its start (§8).

### 2.6 Verifying one segment (bundle format 3)

- **Format numbers.** A bundle without a Segment record stays **format 2, byte for byte as today**, so every existing bundle and every pinned bundle test is unchanged. A bundle with a Segment record is **format 3**. `verify` accepts 2 and 3. It requires a Segment record if and only if the format is 3 (today it accepts 2 only [src/bundle.rs:707-709]).
- **Placement.** The Segment record is its own section, directly after the meta record. Section numbers are private [src/bundle.rs:220-233]; the section rule of `assemble` [src/bundle.rs:466-566] still gives exactly one encoding.

New checks in format 3, in `verify`'s existing order, each failing under a new field class `FieldClass::Segment`:
1. **Segment record.** `segment ≥ 1`. `own_start`, if present, is a checkpoint signed by the exporter's roster key, in this session, author = exporter, with a roster version held. Each of `starts` is a checkpoint signed by its author's roster key, in this session. The authors are strictly increasing, never the exporter, and at most 31.
2. **Own chain from the start.** With `own_start` (n₀, h₀), own events must be numbered n₀+1, n₀+2, … with the first `prev_hash` = h₀. This replaces the base of 1 and zero hash [src/bundle.rs:773-777]. Own checkpoints must be numbered above n₀, and their roster versions are non-decreasing from `own_start.roster_v`. `Report.own.first_seq = n₀ + 1` and `Report.own.anchor = Some((n₀, h₀))`. Both fields exist today [src/bundle.rs:574-590].
3. **Countersignatures** may attest `own_start` as well as the own checkpoints: the lookup at [src/bundle.rs:833-837] also tries `own_start`. The list given to `countersigner_ok` [src/bundle.rs:811-815, 852] starts with `own_start`. The author applies the same list (its checkpoint list starts at the start, §8), so author and `verify` still apply one rule (gate A-M2).
4. **Peers.** For each author X, the PeerStart record, if present, must be at least as new as `starts[X]`. It can be newer after a later release tombstone or a joiner anchor.
5. **Everything else** (rosters from version 1, evidence, cross-check records, seal) is unchanged. `history_from_genesis` stays true across seals, because rosters are carried whole.

`verify_together` changes in one place: "have" for `omitted_own` becomes the last own number held (`own_start + own_events.len()`), not `own_events.len()` [src/bundle.rs:1158].

### 2.7 Verifying a whole session made of several segments

**New `bundle::verify_segments(segments: &[Bundle]) -> Result<SegmentsReport, VerifyError>`.** It verifies one pair of neighbours at a time, so it holds at most two bundles at once: ≤ 128 MiB parsed (computed, not run; U-S4).

1. **Each bundle alone.** `verify(b)` passes.
2. **One session, one exporter.** The same session, exporter and convener throughout.
3. **Ordered.** Segment numbers are strictly increasing by one: 0 has no Segment record, and i ≥ 1 carries `segment = i`. A gap is an error ("segment missing"). Two bundles with one number are both checked and then compared with `verify_together` (§2.8 row 1 explains how two can exist); any conflict is returned as evidence.
4. **Linked by digest.** Segment i+1's `prev` equals segment i's `seal.digest`, which `verify` of segment i already checked against its content [src/bundle.rs:1016-1021].
5. **Own chain linked.** Segment i+1's `own_start` (n₀, h₀) equals a checkpoint in segment i at n₀: one of its own checkpoints, whose hash `verify` already matched to the event at n₀ [src/bundle.rs:784-797], or segment i's own start when no newer checkpoint exists.
   - Own events numbered above n₀ that appear in both segments (they were carried) must be byte-identical. A difference is V's own equivocation and is returned as `EquivocationEvidence`.
   - No own number is signed twice across the whole set (invariant S3).
6. **Peer chains linked.** For each X in segment i+1's `starts`, segment i must hold a statement of X at c_X with the same hash.
   - No such statement is an error ("segment start not in the previous segment"): the exporter skipped or spliced.
   - A statement with a different hash is evidence against X. X signed both, and the exporter cannot forge X's signature.
   - X's events above c_X held in both segments must agree.
7. **Roster history kept.** Segment i+1's rosters begin with exactly segment i's rosters (byte-equal versions), and a roster conflict in i appears in i+1.
8. **Evidence never dropped.** Segment i+1's evidence ⊇ segment i's evidence (the fixed part is kept whole and evidence is "first four kept"). Fewer is an error ("segment drops evidence held earlier"). A single bundle cannot show this today; a set can.
9. **The report:**
   - `from_genesis` (the first bundle is segment 0);
   - per segment (number, first and last own number);
   - every equivocation (each segment's, plus every cross-segment conflict);
   - every roster fork.

**What a set proves, and what it cannot.**
- **It proves** one chain per author across files, with no splice, gap or dropped evidence.
- **It cannot show** that later segments exist when they were withheld. This is the tail limit that exists today at the level of events (docs/AUDIT.md §2 "Limits, stated"), now also at the level of files.
- **What narrows it:** a countersigner of a later checkpoint, through `verify_together`, shows that V's chain went further.

### 2.8 Restart in the middle of a seal: every step

The anchor (I-A14) gets two rules, both applied before anything else:
- **R-A1.** `resume_with_anchor` lists the store, **normalises** it (§2.3), then runs `anchor.check` on the normalised listing, then resumes.
- **R-A2.** `Table::Segment` is replaced in place, with order (segment, 0). A newer Segment record passes as "newer", like an attestation.

So:
- an anchor taken after the seal (`post_anchor`) accepts a store at any point after the commit put;
- an anchor taken before the seal refuses a committed store (its runs are shorter: `Behind`) and accepts an uncommitted one;
- a forged Segment record with deeper cuts makes normalisation drop real records, so `post_anchor` refuses it (`Behind`/`Missing`).

| Crash or failure at | Store holds (physical) | Restart | Result | Lost? |
|---|---|---|---|---|
| Step 0 or 1, or before step 2 completes | the pre-seal store | `resume_with_anchor(current)` | pre-seal member | Nothing. A half-written or orphan file of segment k is an ordinary valid export. The next seal writes segment k again, as a superset, and `verify_segments` compares the two (§2.7 item 3). |
| After step 2, before the step 3 put | pre-seal store; daemon holds the current and the pending anchor | the daemon tries pending first: `Missing` (no Segment slot); then current: OK | pre-seal member | Nothing |
| Step 3(b): the put returns an error | pre-seal store | none needed: `seal_commit` returns `Store(..)` and the member is unchanged | pre-seal member; the same plan can be committed again (its pre_anchor still matches) | Nothing |
| After the step 3(b) put, before 3(c) | pre-seal store + Segment record | current anchor: refused (`Behind`); pending: OK | post-seal member (normalised) | Nothing. Garbage stays until the next seal. |
| During 3(d) collection (any put or remove; failure or stop) | post-seal + some garbage | pending: OK; plain `resume`: OK | post-seal member | Nothing |
| After 3(d), before step 4 | post-seal store | pending: OK (current refused) | post-seal member | Nothing |
| Daemon lost the pending anchor (it never saved it) | if the put happened: post-seal | current: refused; plain `resume`: OK without loss-detection | post-seal member, unanchored | Nothing lost. D-S3 says save the pending anchor before step 3; R4-m3's limit for plain `resume` applies [src/session.rs:323-327]. |
| Two seals behind (an anchor two segments old) | — | `Older { part: Fixed(Segment) }` or `Behind` | refused | — (the daemon always holds the current anchor) |

**Limits across a seal.**
- `seal_commit` keeps `self.limits`. It is not a restart.
- Every clause of `try_set_limits` is "usage + one checkpoint ≤ limit" [src/session.rs:641-665], and a seal only lowers usages. So the limits in force stay acceptable after a seal (REASONED).
- A restart in the middle comes back on the defaults, as every restart does [src/session.rs:255]. The daemon re-offers its limits (BACKLOG, corrected 2026-11-19). That is safe by the defaults clause [src/session.rs:629-636].

### 2.9 The one change to the fixed part, and why every seat stays the same

The Segment record needs a fixed slot (it must never be refused for space). Adding one without moving any seat:

| Item | Today [src/budget.rs] | This design | Bytes set aside |
|---|---|---|---|
| Evidence slot maximum (`EVIDENCE_SLOT_MAX`) | 4,100 (largest measured evidence 1,523 framed, docs/AUDIT.md §1A) | **3,972** (PROPOSED) | 128 × 3,972 = 508,416 (was 524,800) |
| New table `Table::Segment`, appended LAST to `Table::ALL` (so every anchor wire code (0, t) and the key order of the existing tables are unchanged, F9) | — | **1 slot, 16,384 framed bytes** (PROPOSED; estimate of the largest record 14,565) | 16,384 |
| `FIXED_BYTES` | 17,940,335 | **17,940,335 (unchanged)** | |
| `FIXED_RECORDS` | 540 | **541** | |
| `SEAT_BYTES` = ⌊(58,720,256 − 17,940,335) / 8⌋ | 5,097,490 | **5,097,490 (unchanged)** | |
| `SEAT_RECORDS` = ⌊(229,376 − 541) / 8⌋ | 28,604 | **28,604 (unchanged)** | |
| Fixed part + eight seats | 58,720,255 B / 229,372 records | 58,720,255 B / **229,373** records, ≤ capacity 58,720,256 / 229,376 | |
| Own seat / free part / one allowance | 5,068,886 / 2,534,443 / 362,063 | unchanged | |

All figures computed, not run.

- **Gate files.** No gate file pins `EVIDENCE_SLOT_MAX`, `FIXED_RECORDS` or 540: I searched every test file at `36537eb`. The builder files that do (`a3_props.rs` `FIXED_SLOTS` and `kind_max`; `a3_unknowns.rs`) are updated with the change listed.
- **The anchor bound.** `MAX_ANCHOR_SLOTS = FIXED_RECORDS` [src/anchor.rs:38] becomes 541. The largest anchor grows by one slot, about 330 bytes, from the 172,974 bytes gate r5 measured to well under 512 KiB (computed, not run).
- The alternative, shrinking every seat by about 2 KiB, is INTERPRETATION I-S9.

---

## 3. Every property of design 07, restated across a seal

The class is: an input caused by party A exhausts storage that party B needs for an action (07 §3, closing argument). For each property, here is what it says after a seal and why it still holds (REASONED unless a test is named; the build's generated property makes each one a test, §6.2).

| # | Property (07 §3 or docs/AUDIT.md §1A) | Across a seal | Why, with the code relied on |
|---|---|---|---|
| P1 | Control always fits: roster, evidence and own free recording are never refused for space | holds | The seal writes only the reserved Segment slot and removes records. Rosters, the conflict and evidence are carried whole, so the roster lifetime is untouched. `apply_roster` and `store_evidence` are unchanged [src/session.rs:1262-1326, 1036-1083]. After a seal the free part holds only own records made after n₀, so P1(c)'s room grows. |
| P2 | Seats do not interfere | holds, seal steps kept in both runs | The cut c_X of seat s is X's own newest checkpoint held. That is decided only by X's checkpoints accepted into X's chain, because cross-check records never enter a chain (F11). So what a seal removes from seat s, and what s can then hold, depends on the roster history, V's seal steps and seat s's inputs alone. `NothingToSeal` may differ between the two runs only when seat s has nothing to remove in either, which leaves its charges equal. |
| P3 | Bounds and exact accounting | holds, restated over the **logical** store | The usages are the sum over the normalised store (§2.3), the Segment record charged to its table. The physical store also holds the garbage of an interrupted collection. Only V's seal makes garbage, it is at most what was live before that seal (≤ capacity), and it is not exported. After a `seal_commit` whose store calls succeeded, there is no garbage (invariant S9). |
| P4 | Latest state | holds | Unchanged. The Segment slot is one record, replaced in place. |
| P5 | Accounting is a function of the store; `resume` ≡ live | holds, at every point of a seal | `seal_commit` rebuilds with the same code path as `resume` over the same normalised listing. A store stopped anywhere in §2.8 normalises to the same logical store as the live member's. |
| P6 | Evidence before space; a fork is never `LogFull` | holds | Unchanged order. Evidence is never removed by a seal. |
| P7 | An honest author is never refused for space by an honest peer (equal limits) | **holds between seals of the receiver; restated** | A seal is local. When V seals and W does not, V's own seat empties but W's seat for V still holds V's earlier events. W refuses V's later events with `LogFull` once its seat for V fills, and keeps witnessing V's checkpoints (I-A4). Restated P7: with equal limits, an honest author is never refused by an honest receiver that has sealed at least as recently, in V's segment terms. Otherwise the receiver's refusal is charged to the author's seat at the receiver, and that seat contains only the author's records. The class is not violated, because what fills W's seat for V is V's own activity. INTERPRETATION I-S6. |
| P8 | The export always verifies | holds (format 3 verify, §2.6) | The segment k file is the ordinary export. A continued store exports as format 3, whose own chain begins at `own_start`. Its countersignatures are only of checkpoints at n₀ or later, because the older ones are dropped by normalisation [check F4]. Its peers begin at their PeerStart. Invariant I5 in §6.2. |
| P9 | Release gives the seat back and loses nothing | holds | Release is unchanged and works the same after a seal. (§2.3 suggests making its order crash-safe; DQ-S3.) |
| (d1) | The free part holds only own-choice events and own checkpoints covering no requested event | holds | The seal point n₀ moves into the fixed Segment slot (`own_start`), out of the own seat. After the seal the free part holds only post-seal records. Requested events above n₀, when n₀ is older because step 0 was refused, keep their allowance charge (`own_req`, `head_payer` [src/session.rs:777-797, 859-870]). Requested events at or below n₀ are gone, so `head_payer` cannot pick a stale payer. |
| (d2) | No own call ⇒ an empty free part | holds | The seal is V's explicit act. Step 0 is V's explicit checkpoint call. |
| (d3) | Requests change own records only by number width | holds | Numbering continues (it is never reset), so widths keep growing with the session, by at most the 20 digits of a u64 (computed, not run). |
| I-A13 | Each request holds back room for its checkpoint | holds | Carried requested events keep their hold-back. A seal never raises usage. |
| N1 (gate r5) | A re-used slot's earlier occupant fills V's seat | **reduced** | The earlier occupant is a removed key, so its chain is cut at its newest checkpoint and those records leave V's slot seat. What stays is its events after its newest checkpoint (none if it checkpointed last). The same holds for the slot-0 fallback while V is off the roster [src/session.rs:735-737]. N1's exception after `resume` is unchanged. |
| N2 (gate r5) | An empty received chain is left by a failed first write | **cleared by a seal** | The rebuild comes from the store, and empty chains are not stored [src/session.rs:1609-1623]. |
| fix3 / QA2-m1 / resume-defaults | Defaults after a restart have room for every owed checkpoint | holds | Limits are untouched by `seal_commit`. A restart in the middle is an ordinary restart. The defaults clause is unchanged [src/session.rs:629-636]. QA3-n1 (older stores) is unaffected: a store from before this build has no Segment record and normalises to itself. |
| R5-m2 / roster store-first | A refused roster version is never stored | holds | `apply_roster` is unchanged. |
| R4-m1 / all or nothing | A failed write leaves the member as it was | holds | `seal_commit`'s only required write is one put. If it fails, the member is unchanged. Collection failures leave the member post-seal and correct. |
| Export bounds | `export` never exceeds the caps | holds | The capacity arithmetic is unchanged (§2.9). The Segment record is inside the fixed part. Gate test n15's inequality still holds: 17,940,335 + 40,779,920 + 65,536 ≤ 67,108,864 and 541 + 228,832 + 2 ≤ 262,144 (computed, not run). |
| Tamper evidence across segments | | holds | Within a file: unchanged. Between files: the `prev` digest under the seal, the own start equal to a checkpoint the earlier file matched to its chain, and peer starts signed by their authors (§2.7). The seal point is an ordinary checkpoint that peers countersign, so a later rewrite of segment k's own chain contradicts their countersignature of n₀. That countersignature is held in segment k+1 and by the countersigner. |

**Why no fifth instance of the class (REASONED).** Every new stored or exported thing is in §4. Each is caused by V's own act (the seal) or is a reserved fixed slot replaced in place. The only peer-caused content in a sealed file is that peer's own seat, which P2 bounds. The only way a peer could cause a file is through the daemon's seal policy, which D-S1 forbids and red control `seal_on_receive` guards inside the crate. A peer cannot refuse, delay or break a seal: no space question is asked, and the stale check is V's own interleaving under D-S2.

---

## 4. The storage table, for every new stored or exported thing

| Thing | Who causes it | Charged to | Bound | What filling it can block | What it can never block |
|---|---|---|---|---|---|
| Segment record (fixed slot `Table::Segment`) | V (its seal) | the fixed part, Segment table | 1 slot × 16,384 framed bytes, replaced in place at each seal | nothing (set aside whole; never refused for space) | anything |
| Peer starts written to Anchor slots during collection | content: X (its signed checkpoint); decision: V | the fixed part, Anchor table (existing) | 31 × 516, replaced in place | nothing | anything |
| X's events after its start, carried into segment k+1 | X | X's seat (unchanged rule) | ≤ S = 5,097,490 bytes / 28,604 records | X's further events at V (X's own seat) | anything else |
| V's own events after n₀, carried (only when step 0 was refused) | V, or G for `record_for` | free part / G's allowance (unchanged) | the existing parts | V's own recording or G's requests (unchanged) | anything else |
| Garbage left by an interrupted collection | V (its seal) | not charged (not in the logical store) | ≤ the logical store before that seal ≤ capacity 58,720,256 bytes; at most one seal's worth, because the next seal collects all (computed, not run) | the daemon's disk, transiently (outside the crate's accounting) | any crate operation (the accounting and export ignore it) |
| Sealed segment file, exported to the caller | V (its seal) | V's archive (daemon) | ≤ `MAX_BUNDLE_BYTES` = 64 MiB per file; files per session = seals V chose; retention K is V's setting (DQ-S2). X's part of each file ≤ S | the archive disk (outside the crate) | anything inside the crate; a peer can never add a file (D-S1, S4) |
| `SealPlan` in memory | V | the daemon's memory, transient | the bundle (≤ 64 MiB) + two anchors (≤ 512 KiB each, `MAX_ANCHOR_BYTES` [src/anchor.rs:40]) | — | — |
| Pending anchor in the daemon's security file | V | the daemon | ≤ 512 KiB, one at a time | — | — |
| CPU: `seal_export` | V | — | one export (≤ 229,373 records to encode) + one anchor from memory | — | — |
| CPU: `seal_commit` rebuild | V | — | a rebuild of the smaller post-seal store; signature checks of the records kept (UNKNOWN time, U-S3) | — | — |
| CPU: `verify_segments` | verifier | — | `verify` per segment + linking; ≤ 2 bundles in memory | — | — |

**Storage per seat right after a seal** (the logical store):

| Part | Holds after the seal |
|---|---|
| Peer seat of slot s | the events of each author in slot s numbered after that author's start (nothing if the author checkpointed after its last event) |
| Own seat, free part | own-choice records after n₀ (nothing if step 0 succeeded) |
| Own seat, allowance of slot g | requested events of g after n₀ and the checkpoints covering them (nothing if step 0 succeeded) |
| Fixed: roster, conflict, evidence, cross-check records | unchanged (carried whole) |
| Fixed: attestations | only those of checkpoints numbered ≥ n₀ |
| Fixed: newest-checkpoint slots | none for authors cut (their newest is now their start) |
| Fixed: anchors | each cut author's start (or a newer tombstone or anchor) |
| Fixed: Segment | this segment's record |

---

## 5. Who can do what

### 5.1 A hostile V (the exporter and sealer itself)

| Can | Cannot |
|---|---|
| Never seal (the session is then the fixed capacity of today) | Make one number of its own chain carry two statements without it being transferable evidence. Peers hold its statements, and `verify_segments` compares carried events (§2.7 item 5). |
| Show only some segments: a later tail withheld, or an early prefix withheld (`from_genesis = false`, `own.first_seq = n₀+1` says so) | Splice segments of another session or exporter, or reorder them (session, exporter, convener, segment number, `prev` digest) |
| Seal with an older own start, or older peer starts (it then keeps more than it must) | Present a start no earlier segment holds (§2.7 item 6, error), or a peer start the peer never signed (signature check) |
| Rewrite its own chain before anyone countersigned a checkpoint covering it (as today) | Rewrite segment k after peers countersigned n₀ without contradicting that countersignature (held in k+1 and by the countersigner) |
| Drop evidence or roster versions from one isolated file | Do so in a set: §2.7 items 7 and 8 refuse a later file with fewer |
| Fork its continuation: two different segment k+1 files | Without `verify_segments` / `verify_together` of the two producing own-equivocation evidence |
| Lose or delete its archived files | Make its own later exports fail `verify` |

### 5.2 A hostile peer X (a member; X may be the starter)

| Can | Cannot |
|---|---|
| Fill its own seat at V again after each of V's seals: ≤ S per segment into V's archive (V chooses how many segments) | Cause, trigger, delay, block or make fail any seal (no input path seals: S4; no space question: S5; staleness needs V's own interleaving: D-S2) |
| Withhold checkpoints so its seat at V is never emptied by a seal (it fills only its own seat) | Make a seal remove any record of another author, or any record of its own that is not in segment k's file (S1) |
| Send a checkpoint far ahead just before V seals, so that V never holds its events in between (it hides its own events from V; this affects only X's own record; I-S3) | Use another seat, the free part, the fixed part or the Segment slot |
| Tell two stories across V's seal boundary (one before, one after) | Escape detection in a set: V's segment k holds the first story; the second conflicts with it, or with V's held start, through `verify_together` or `verify_segments`. Live detection for statements at numbers ≤ c_X ends at V's seal (stated loss, §7.1 I-S2). |
| Countersign V's checkpoints from before the seal | Have such a countersignature stored (`UnknownHead`) |
| As the starter: re-add V into a used slot (N1) | Survive V's next seal in V's seat beyond its last checkpoint (N1 reduced, §3) |
| As the starter: use up the roster lifetime | Have any seal reset or extend it (rosters are carried) |

### 5.3 A hostile relay

| Can | Cannot |
|---|---|
| Delay X's events so that V seals before they arrive. V then never holds them (equivalent to dropping them, which it can already do) | Forge anything. Replays of pre-seal objects are refused (`BeforeStart`, `StaleHead`, `UnknownHead`) and nothing is stored. |
| Drop V's seal-point checkpoint on its way to peers. Peers then countersign a later one, which also covers it | Learn that V sealed from any message (no message is sent) |

### 5.4 A third-party verifier given a forged or truncated set

| Given | `verify_segments` says |
|---|---|
| All segments 0..k, honest | Ok; `from_genesis = true`; every equivocation in and across files |
| Segments i..k with i > 0 | Ok; `from_genesis = false` (and the first file's own chain says "starts at n₀+1") |
| A gap (i, i+2) | error: segment missing (number and `prev` digest) |
| A segment from another session or exporter, or a re-sealed copy by another key | error: session/exporter, or the seal signature |
| Segment k+1 whose `prev` is not segment k's digest | error: link |
| Segment k with an edited own event | `verify` of segment k fails, at the field's own class |
| Segment k+1 with an `own_start` that segment k does not hold | error: own link |
| Segment k+1 with a peer start that segment k does not hold, or holds with another hash | error, or evidence against that author |
| Segment k+1 missing evidence or roster versions that segment k holds | error |
| Two different files numbered k | both checked and compared; agreement is reported, and any conflict is evidence against the signer |
| Segments 0..j with j < k (later files withheld) | Ok for 0..j. **Not detectable from the set** (the tail limit). Detectable with any member's bundle holding a later statement of V (`verify_together`'s `omitted_own`, corrected per §2.6). |

---

## 6. For the independent check: attacks, the generated property, red controls

### 6.1 Attack list (each with the expected result)

| # | Attack | Expected |
|---|---|---|
| A1 | X floods its seat until full, hoping V's policy seals (and so writes a file) | The crate has no path from any input to a seal (S4). Red `seal_on_receive` (receive seals when X's seat is full) must fail S4. The daemon precondition D-S1 is a BACKLOG item plus a daemon test. |
| A2 | Between `seal_export` and `seal_commit`, X sends events numbered ≤ c_X into a seat with room, and W sends a newer countersignature of an own checkpoint below n₀ | `seal_commit` refuses `SealStale` and the member is unchanged; nothing is lost (S1). Red `seal_no_stale_check` must fail S1: the X events and W's countersignature are dropped although they are not in segment k's file. |
| A3 | Failing store: the put fails at call j, for every j of `seal_commit` | j = commit put: `Err(Store)`, member unchanged, a retry with the same plan succeeds. j in collection: `Ok`, garbage reported, `export` verifies, the next seal collects it. |
| A4 | Stopping store: snapshot after every store call of `seal_commit`; then `resume`, `resume_with_anchor(pre)` and `resume_with_anchor(post)` on each snapshot | Each snapshot gives either the pre-seal member (the pre anchor accepts) or the post-seal member (the post anchor accepts), as in §2.8. The resumed member ≡ a live member in that state (P5). Red `seal_delete_first` (collection before the commit put) must fail S1/P5 on a snapshot. |
| A5 | X tells V story A at number s ≤ c_X before the seal and tells W story B; V seals | `verify_together(V's segment k, W's bundle)` and `verify_segments` return evidence against X |
| A6 | Exporter splices segment k+1 of another session or exporter onto segment k | error (§5.4) |
| A7 | Exporter drops segment k from the middle of a set | error: segment missing |
| A8 | Exporter presents only the latest segment as the whole session | `Report.own.first_seq = n₀+1`, `anchor` Some, `from_genesis = false`. Red `verify_seg_own_from_one` (format 3 verify reports first_seq 1) must fail the report assertion. |
| A9 | Exporter rewrites own events of segment k after W countersigned n₀ (the countersignature held in k+1) | `verify` of segment k fails on the checkpoint hash, or `verify_segments` fails on the own link |
| A10 | Exporter drops an evidence record in segment k+1 | `verify_segments` error. Red `verify_seg_no_evidence_superset` must fail it. |
| A11 | Exporter forks its continuation (two segment k+1 with different events after n₀) | own-equivocation evidence from `verify_segments` |
| A12 | Exporter puts a peer start X never signed in the Segment record | `verify` error, `FieldClass::Segment` |
| A13 | X sends a far-ahead checkpoint just before V seals | V's start for X is that checkpoint. X's events in between are refused `BeforeStart` afterwards. No other seat or part changes (P2). Documented (I-S3). |
| A14 | After the seal, X (or the relay) replays pre-seal events, checkpoints and countersignatures | refused (`BeforeStart`, `StaleHead`, `UnknownHead`); nothing stored (P3 store unchanged) |
| A15 | Disk rolled back to the pre-seal store while the daemon holds only the post anchor | refused (`Missing`, Segment slot). The seal is not silently undone. |
| A16 | Disk attacker writes a forged Segment record with deeper cuts (real, signed checkpoints) | `resume_with_anchor(post)`: refused (`Behind`/`Missing`) after normalisation. Plain `resume`: accepted with records dropped; that is the limit of plain `resume` stated today (R4-m3). Red `anchor_before_normalise` (check before normalising) must fail S8. |
| A17 | Attestations of pre-seal checkpoints carried into segment k+1 | `export` of k+1 fails `verify` (F4). Red `seal_keeps_old_attestation` must fail P8/I5. |
| A18 | Seal while in N1's state with a checkpoint owed | the seal succeeds (S5). After it, the owed checkpoint is `Ok` (the earlier occupant's records before its newest checkpoint are gone, and its payer keeps the hold-back). |
| A19 | Seal while the free part is full, so `checkpoint_now` is `LogFull` | the seal succeeds from the latest stored own checkpoint. Own events after it are carried with their charges. Red `seal_needs_checkpoint` (refuse when step 0 fails) must fail S5. |
| A20 | Seal, then restart, then compare limits | `limits()` is unchanged by `seal_commit`. After a restart the defaults apply and the re-offer is accepted. Red `seal_resets_limits` must fail S7. |
| A21 | Self-equivocation through a restart: the Segment record removed from the store, own events after n₀ kept | `resume` refuses (own chain does not start at 1). It never restarts at 1. Red `seal_restart_own_at_one` (own numbering restarts after a seal) must fail S3. |
| A22 | A removed member's chain at the seal; then release; then the same key re-added | the cut works like a tombstone; release after it works (P9); the re-add behaves as today (A-m6 unchanged) |
| A23 | Roster fork across a seal | the conflict slot is carried; `verify_segments` compares the roster prefixes; the fork is reported |
| A24 | The own start left as an own checkpoint in the free part (cost shift from a requester's allowance into the free part) | (d1) and P3 hold only if the start moves to the Segment slot. Red `seal_start_charged_to_free` must fail (d1). |
| A25 | `NothingToSeal` loop: repeated seals with nothing to remove | refused. No Segment record is written and no file is produced. |

### 6.2 The generated property (required)

**Harness.** Extend the existing generator in `tests/a3_props.rs`: its `Kind`/`Op` alphabet [tests/a3_props.rs:84-121, 211-280] already covers every peer input, roster operations, own calls, `Resume` and `Release`. It needs:

- 2 to 8 members with fixed test keys;
- limits drawn small so seats fill;
- roster operations within 8 members, 32 keys and 256 versions;
- **every peer author also able to seal its own `SessionAudit`**, invisibly to V, and to keep sending.

**Added symbols:**
- `CheckpointNow`;
- `SealExport`;
- `SealCommit`;
- `SealExportThenInterleave(op)`: any peer op between export and commit, expecting `SealStale`;
- `SealCommitStoreFailsAt(j)`;
- `SealCommitStopsAt(j)` + {`Resume`, `ResumeWithAnchor(pre)`, `ResumeWithAnchor(post)`};
- `CollectFailsAt(j)`;
- `ReplayPreSeal(object)`;
- `CountersignPreSealHead`.

The whole alphabet of each hostile party is drawn at every step. Each fixture is generated inside the test.

**Model state kept by the test:**
- every record ever accepted (key and bytes);
- every file returned by `seal_export` and the files committed;
- every own statement ever signed;
- the expected limits.

**Invariants, asserted after every step:**

| # | Invariant | Red control (must fail it on its own assertion text) |
|---|---|---|
| I1 = P1 | control always fits | existing rows (`roster_on_seat`, `evidence_on_seat`, `requested_takes_free`) |
| I2 = P2 | seats do not interfere, seal steps kept | `shared_peer_pool`; new `seal_cut_by_other_seat` (the cut of seat s taken from a cross-check record's entry instead of s's own checkpoint) |
| I3 = P3 | bounds and exact accounting over the logical store; Segment record ≤ 16,384 | `uncharged_slot` (also on the Segment slot); new `segment_uncharged` |
| I4 = P5 | resume ≡ live at every step and every snapshot | `resume_all_own`; new `resume_no_normalise` |
| I5 = P8 | `export` Ok and `verify` Ok at every step, format 2 or 3 | new `seal_keeps_old_attestation`, `verify_seg_own_from_one` |
| S1 | **Conservation:** every record ever accepted is in the current logical store or in a committed segment file | new `seal_no_stale_check`, `seal_delete_first`, `seal_cut_plus_one` (cut c_X+1) |
| S2 | **Continuity:** `verify_segments(committed files + current export)` is Ok, and reports every equivocation the union holds | new `verify_seg_no_link` (the `prev` check skipped), `verify_seg_no_evidence_superset` |
| S3 | **No number signed twice:** across all files and the store, at most one own header and one own checkpoint per number | new `seal_restart_own_at_one` |
| S4 | **The seal is V's alone:** only `seal_commit` (and `archive_and_release`) changes the segment number or lowers a numbered run | new `seal_on_receive` |
| S5 | **A seal is never refused for space:** with a working store and a fresh plan, `seal_export` and `seal_commit` succeed in every state (full seats, full free part, N1's state, a checkpoint owed, V off the roster) unless `NothingToSeal` | new `seal_needs_checkpoint`, `seal_space_checked` |
| S6 | **Invisible to peers:** a peer receiving V's stream across V's seal accepts every event and checkpoint; V accepts its countersignature of the seal point after commit | new `seal_changes_next_prev_hash` (the first event after a seal chains to zero) |
| S7 | **Limits kept:** `seal_commit` leaves `limits()` unchanged; an owed checkpoint still has room after a seal | new `seal_resets_limits` |
| S8 | **Anchor:** `plan.post_anchor` == `anchor()` after commit; `resume_with_anchor(post)` accepts every post-commit snapshot and refuses any with a live record removed | `anchor_not_checked`; new `anchor_before_normalise` |
| S9 | **No garbage after a clean commit:** physical store == logical store after a `seal_commit` whose store calls all succeeded | new `seal_no_collect` |

**Reach requirement.** Like `fix_qam1_seat.rs`'s counters, and to avoid gate r5's N1 coverage gap, the run must print and assert:
- a seal reached in each state named in S5;
- a stop at every store-call index of `seal_commit`;
- at least three segments in one case;
- a peer seal observed by V.

Seed: committed, plus two others, at 1,024 cases in release, as the fix3 check ran.

---

## 7. Interpretations for Kam, design questions, unknowns

### 7.1 INTERPRETATION (for Kam): each choice, with the alternative

| # | I chose | The alternative |
|---|---|---|
| **I-S1** | Filing the log away happens only when you (or your own settings: a timer, or your own space filling) decide. Never because someone else filled their share. | File away automatically whenever anyone's share is full. Simpler for the user, but then another person can make your computer write a new 64 MB file whenever they like. |
| **I-S2** | After a filing, your computer catches someone telling two stories only for what they did from their latest checkpoint on. Older proof is checked against the earlier file ("verify all files together"). | Keep a copy of everyone's old statements across filings. The space then never empties, which defeats the purpose. |
| **I-S3** | Each person's record on your computer restarts at their newest checkpoint, even if a few of their items before it had not yet arrived. Those items are then not kept. | Restart at the newest checkpoint your computer holds items up to. Then a person whose share was full stays full after a filing. |
| **I-S4** | Each file stands on its own as "this session from item n onwards". Files are tied together by a fingerprint of the file before, and the whole session is proved with every file. | Each file also carries a compact summary of every earlier file. It is more to build, needs a new kind of signature (a request to the crypto lane), and still cannot prove that no later file exists. |
| **I-S5** | Filing away does not wait for others to countersign the checkpoint it files at. Their countersignatures arrive later and are kept in the next file. | Wait for them. A person who never answers could then stop you filing away. |
| **I-S6** | Everyone files away on their own schedule, and nobody's filing forces anyone else's. If you file more often than someone, their computer stops keeping copies of your activity (it still witnesses your checkpoints) until they file too. | Filings announced to everyone and followed. Then one person can force everyone to file, which is the kind of fault this design exists to prevent. |
| **I-S7** | No limit inside the log on how many times you file away. Your program keeps at most a number of files you choose. | A hard limit per session in the log itself. It protects your disk if the program misbehaves, but caps the session's length again. |
| **I-S8** | After a filing, your "I hold your log from item n" notes to each person restart from the filing point, which is the truth. | A note that keeps counting from the start of the session. It would need a change to what is signed, and it would claim you still hold what you filed away. |
| **I-S9** | The space for the new "filing record" is taken from the evidence slots, each made a little smaller (their largest real content is well under the new size), so nobody's share changes by a single byte. | Shrink every share by about 2 KB instead. That changes numbers the tests pin. |
| **I-S10** | Filing away is two steps: your program saves the file, then tells the log to carry on. Nothing is removed until the file is safe. | One step that saves the file through a callback. Shorter, but harder to recover from a crash in the middle. |

### 7.2 DESIGN QUESTIONS I could not settle

| # | Question | Why it is open | Who decides |
|---|---|---|---|
| DQ-S1 | The daemon's seal policy: which of {the owner's command, a timer, the free part at x%} is the default, and is the owner asked first? | Product choice. D-S1 constrains it but does not choose. | the owner, with the daemon and interface lanes |
| DQ-S2 | Archive retention: how many files are kept per session, where, and whether old files are deleted or offered for export | The files are outside the crate, like D7 (totals across sessions) | daemon lane; the owner for the default |
| DQ-S3 | Should `archive_and_release` be made crash-safe in the same build (tombstone first, then rely on normalisation)? §2.3 reads a fault in its current order (REASONED, not run). | It touches release, which this design otherwise leaves alone | design owner; the build seat first writes the failing test at `36537eb` |
| DQ-S4 | `Record::Segment`, `Table::Segment`, `FieldClass::Segment`, `AuditError::{SealStale, NothingToSeal}` and `Bundle.segment` are additive, but break an exhaustive `match` or a struct literal | I found no exhaustive match on `Record`. `a3_props.rs` `kind_max` has a wildcard. No test builds a `Bundle {..}` or `Meta {..}` that this design touches (`gate_return_r2.rs` builds `Meta`, which is unchanged). `gate_r5.rs:1239` builds `AuditAnchor {..}`, which this design does NOT change. Matches on `Table` or `AuditError` in tests: UNKNOWN | the build seat, by compiling; any gate file that breaks is a ruling for Friday, never an edit |
| DQ-S5 | Should a single-file `verify` refuse a format-3 file whose `own_start` it cannot link? (I chose: no; one file proves "from n₀"; linking is `verify_segments`'s job.) | Strictness versus usefulness of a lone file | design owner |
| DQ-S6 | Re-anchor (A-m6) and seals: a joiner's stale anchor still leaves events as `Gap` | Unchanged by this design; noted because seals make re-anchoring more visible | design owner (BACKLOG A-m6) |

### 7.3 UNKNOWN, and what settles each

| # | Unknown | What settles it |
|---|---|---|
| U-S1 | The largest Segment record (estimate 14,565 framed bytes, computed, not run) | A test that builds it with 31 starts and every number at u64::MAX. If it is above 16,384 − margin, raise the slot and take the bytes from evidence again (§2.9 keeps `FIXED_BYTES` within 17,940,329..17,940,336 so that the seats stay) |
| U-S2 | That 3,972 is above the largest evidence record (1,523 measured) | the existing `a3_unknowns.rs` u5 test, re-run at the new constant |
| U-S3 | The time of `seal_export` and of the `seal_commit` rebuild at full seats | A release measurement by the build seat (the rebuild re-checks a signature per kept record) |
| U-S4 | The memory of `verify_segments` over two maximum files | A release measurement |
| U-S5 | Which existing tests change colour (expected: only the builder files pinning 540, 4,100 and the evidence slot) | The build seat's first full run, recorded |

---

## 8. Build outline

**Files the build seat owns** (all under `crates/coagent-audit/` unless named):

| File | Change |
|---|---|
| `src/segment.rs` (new) | `SegmentRecord`, `SegmentInfo`, `SealPlan`, `normalise(listing) -> listing` (§2.3), `verify_segments`, `SegmentsReport` |
| `src/budget.rs` | `Table::Segment`, appended last to `Table::ALL`; `SEGMENT_SLOT_MAX = 16_384`; `EVIDENCE_SLOT_MAX = 3_972` (§2.9) |
| `src/bundle.rs` | `Record::Segment(SegmentRecord)` and its section after meta; `Bundle.segment: Option<SegmentRecord>`; `BUNDLE_FORMAT_SEGMENTED: u32 = 3` (format 2 unchanged); `verify` (§2.6); `verify_together` `omitted_own` fix; `FieldClass::Segment`; `export_records` emits the Segment record |
| `src/chain.rs` | `AuthorChain` knows a start checkpoint: `seq() = start + events`, `event(n)` offset, `last_hash` from the start, the checkpoint list beginning with the start, `checkpoint_due` counting from the start; a crate-private `restore_from(start, events, heads, countersigs)` |
| `src/session.rs` | `seal_export`, `seal_commit`, `segment()`; `resume`, `resume_with_anchor` (R-A1), `export`, `anchor()` and the accounting read the normalised listing; the rebuild path shared by `resume` and `seal_commit` (limits kept by `seal_commit`); `head_payer` and `allowances_owing_a_checkpoint` take the own start as the lower bound explicitly |
| `src/anchor.rs` | `replaced_in_place` includes `Segment`; `slot_order(Record::Segment) = (segment, 0)` |
| `src/error.rs` | `AuditError::SealStale`, `AuditError::NothingToSeal` |
| `src/lib.rs` | `pub mod segment;` |
| `build.rs`, `scripts/red-controls-audit.sh` | every new red name of §6 and its row |
| `tests/seal_props.rs` (new), `tests/seal_unit.rs` (new), `tests/seal_verify.rs` (new) | §6.2, the attacks of §6.1, and verify cases §5.4 |
| `tests/a3_props.rs`, `tests/a3_unknowns.rs` (builder files) | constants 541 and 3,972; the new u5 test for the Segment record; each change listed in STATUS |
| `docs/AUDIT.md` | a new §1B "Seal and continue"; the "Limits, stated" line on fixed capacity corrected; the storage table rows of §4 |
| `BACKLOG.md` | close "Seal and continue"; add D-S1, D-S2 and D-S3 for the daemon lane; add DQ-S2 |

**Public API additions** (all additive; DQ-S4 lists what can break a `match`):

```
impl<S: Store> SessionAudit<S> {
    pub fn seal_export(&self, id: &DeviceIdentity) -> Result<SealPlan, AuditError>;
    pub fn seal_commit(&mut self, id: &DeviceIdentity, plan: &SealPlan, now: AuditTime)
        -> Result<SegmentInfo, AuditError>;
    pub fn segment(&self) -> u64;
}
pub struct SealPlan { pub bundle: Bundle, pub post_anchor: AuditAnchor, pub segment: u64, /* private: pre_anchor, record */ }
pub struct SegmentInfo { pub segment: u64, pub own_start: Option<u64>, pub garbage_left: usize }
pub fn bundle::verify_segments(segments: &[Bundle]) -> Result<SegmentsReport, VerifyError>;
```

No change to `AuditAnchor`'s fields (a gate file builds it), `Meta`, `Report`, `ChainReport`, `StoreLimits`, `StoreKey`, the `Store` trait, any signing domain, `coagent-crypto`, `coagent-proto` or `coagent-roster`.

**Order of work for the build seat:**
1. Write a failing test for DQ-S3's reading at `36537eb`, and the U-S1 and U-S2 size tests.
2. Budget change (§2.9), with every existing test green.
3. AuthorChain with a start.
4. Normalisation, used by `resume`, `export` and `anchor`; existing tests green (a store with no Segment record normalises to itself).
5. Format 3 `verify`, then `verify_segments`.
6. `seal_export` and `seal_commit`.
7. The property and red rows.
8. Docs.

**Never weaken a gate file.** An assertion this design makes meaningless gets a ruling request to Friday, the old line quoted, and a replacement test.

**Out of scope:**
- the daemon's seal policy, archive and anchor handling (D-S1 to D-S3, DQ-S1, DQ-S2);
- any network message;
- a signed segment statement and its crypto-lane request (I-S4);
- coordinated seals (I-S6);
- release's crash order (DQ-S3), unless the design owner adds it;
- re-anchoring (A-m6);
- raising the roster lifetime.

---

## Appendix: what I read

**Whole:**
- this folder's `07_audit-storage-accounting-redesign.md`, `05_kam-rulings-2026-11-17.md`;
- `06_design-addendum-rulings-2026-11-17.md` §1, §8, §9, §10;
- `03_architecture-design.md` §9.4;
- `m1_review/gate_M3_AUDIT_r5_verdict.md`, `gate_M3_AUDIT_FIX3_verdict.md`;
- at `36537eb`, with `git show`:
  - `src/session.rs`, `chain.rs`, `received.rs`, `checkpoint.rs`, `store.rs`, `budget.rs`, `bundle.rs`, `anchor.rs`, `domain.rs`, `history.rs`, `error.rs`, `lib.rs`;
  - `src/equivocation.rs` lines 100-446;
  - `docs/AUDIT.md`;
  - `BACKLOG.md`'s audit entries.

**In part:**
- `gate_M3_AUDIT_FIX_verdict.md` and `gate_M3_AUDIT_FIX2_verdict.md` (BLUF and findings tables);
- `src/header.rs` (first 80 lines);
- `crates/coagent-proto/src/bytes.rs` (encoding: lowercase hex);
- every test file at `36537eb` by search only, for pinned constants, struct literals and `Record` matches;
- `tests/a3_props.rs` lines 60-121 and 203-280.

**Not read:** `src/redact.rs`, `src/tiers.rs`, `src/time.rs`, the earlier verdicts r1 to r4, and the test bodies beyond the searches named. Nothing was built or run. Every figure marked "(computed, not run)" came from arithmetic on the constants above (one `python3` arithmetic check of §2.9, no project code).
