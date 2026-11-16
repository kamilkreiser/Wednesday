---
date: 2026-11-17
type: reference
source: architecture agent commissioned by Friday; inputs are the three M3-AUDIT gate verdicts and their test folders, branch m3-audit at 882e094 (read, not run), docs/AUDIT.md, STATUS_M3_AUDIT.md, design files 03, 04 (section 3.9) and 06, docs/ROSTER.md on branch m3-roster at 0a47fc9
status: live (design for the owner's review; nothing built, no code run, no test run)
project: General / CoAgent (no client)
---

# CoAgent audit log: the storage accounting, redesigned as a whole

**Authority.** The owner's ruling, verbatim as Friday relayed it: "Decision general-c2c-audit-third-check-failed-1117: a — Redesign the storage accounting first, then one build and one check".

## 0. Ten lines for the owner

1. **What was wrong, in kind.** The log was one shared space divided by who SIGNED a record. But some records are written automatically because of someone else, so one person could spend another person's share.
2. The member list itself was paid from the starter's share. When that share was full, your computer refused member-list changes, including the one removing the people causing the trouble.
3. **The new rule.** The log has separate parts that cannot borrow from each other: a fixed part for the member list and for proof of lying, eight equal seats (yours and seven others), and nothing else.
4. Whatever a person's own free choices make your computer keep is counted against that person's seat, never against anyone else's and never against the fixed part.
5. Automatic replies no longer pile up. "I received your item" becomes one running note per person that replaces the last one, and cross-check messages are kept only in their latest version.
6. **So, always possible, whatever anyone sends:** apply a member-list change, keep and export proof that someone lied, record your own actions up to your own seat, and export a file that checks out.
7. **What it costs.** A session has a fixed recording capacity: about 3,800 recorded items per person held by each other member, about 1,800 of your own choosing, and about 270 done at the request of each other member (estimates, proposed, not measured). A meter shows it. A full seat stops only that seat.
8. You lose the exact receive time of each single item, the per-item "received" lines other members could see, and the per-checkpoint list of who countersigned (only each person's latest is kept).
9. **What a hostile member can still do:** fill their own seat on your computer (about 5 MB, in about a second), use up the allowance for actions done at their request, and make your computer spend time checking signatures. Seven working together can fill seven seats (about 36 MB). None of this stops the four things in line 6.
10. **Your decisions:** ten are marked `INTERPRETATION (for Kam)` in section 5. The main one: accept a fixed capacity per session now, or also build "seal and continue" (unlimited length, more to build and to check).

**How to read the labels.** **[882e094: file:line]** means I read that line in the worktree `coagent/worktrees/m3-audit`, whose `git rev-parse HEAD` returned `882e0940c1a34d76a9836256c7bff67283ec5609` with no staged or unstaged difference. Paths are under `crates/coagent-audit/` unless a crate is named. **[r3 verdict …]** and the like mean the named part of a gate verdict in `m1_review/`. **REASONED** means my argument from reading; no test has attacked it. **PROPOSED** means a number I chose; none is measured. "Starter" is the owner's word for the `convener` of the code.

---

## 1. The model

### 1.1 What was wrong in kind (three rounds, one cause)

At 882e094 every stored record is charged to a `Payer` [882e094: src/session.rs:108-117] and checked by one function, `ensure` [src/session.rs:247-278]. Four structural facts produce the class. Each survives any single patched rule.

1. **The payer is the signer.** A received event is charged to its author [src/session.rs:613-618]. A receipt is an event the RECEIVER signs because the AUTHOR chose to send something [src/session.rs:623-631; src/chain.rs:251-266]. At the receiver it is charged to the author, correctly. But the receipt then travels in the receiver's own chain to every member the receiver shares with, and there it is an ordinary event of the receiver, charged to the receiver. The gate filled the starter's share at another member with 10,452 receipts in 1.39 s [r3 verdict R3-M1 (a); `release_receipt_proxy.txt`]. The third member cannot charge the true causer even in principle: the receipt's summary, which names the author, is withheld from members not entitled to it [src/session.rs:516-524].
2. **Control records share the pool with data.** A roster version is charged to the starter's share and can be refused for space before the roster crate is even asked [src/session.rs:461-464]. So data traffic can block the member list.
3. **Logs are kept where only the latest state matters.** Countersignatures are kept one per (checkpoint, member) [src/chain.rs:443-451]; receipts one per event; cross-check records were every message in round 2 and are one "latest" per pair now, but the superseded ones stay in an append-only store [src/store.rs:17-22; src/session.rs:802-806].
4. **The accounting is running counters, not a function of what is stored.** `start` on a store that already holds records charges all of them to `Own` [src/session.rs:194-212], so one restart gives every peer a fresh share [r3 verdict R3-m1]. Usage is never released [src/session.rs:285-294; r3 verdict R3-m3]. Reservations are estimates (`RECEIPT_RECORD_MAX`, the worst-case own record) [src/session.rs:86, 281-283, 616-618] and leave gaps both ways [r3 verdict, "My own slips"; mutants N14, P05, P06].

Two ordering faults follow from the same shape: the quota check runs before the fork check, so an author at quota can equivocate without evidence being formed [src/session.rs:614-620; R3-n2]; and evidence is stored but the caller is told `LogFull` [src/session.rs:784-803; R3-n1].

**One more instance I found by reading, not reported by a gate (REASONED, not run).** `apply_roster` computes `framed_len(&Record::Roster(..))` first [src/session.rs:463]; `canonical::encode` refuses any output above 65,535 bytes [882e094: crates/coagent-proto/src/canonical.rs:25-31]. A roster version is itself allowed up to 65,535 bytes, and the `Record` wrapper adds a few bytes, so a valid version within a few bytes of the maximum is refused by the audit crate with an encoding error although the roster crate accepts it. Only the starter can make such a version. Whether a valid version can be that large is UNKNOWN (U1, section 5).

**Conclusion on scope.** The crate's construction (chains, tiers, checkpoints, evidence, export, verify) is sound and stays. Two mechanisms are the problem and are replaced: per-event receipts inside the chain, and the single signer-keyed pool. The cross-check mechanism is kept, with storage of the latest record only. What is lost is listed in 5.1.

### 1.2 Every resource a member holds for a session

| # | Resource | At 882e094 | In this design |
|---|---|---|---|
| 1 | Store bytes and records: roster versions | starter's share; refusable [session.rs:461-464] | fixed part; never refused for space (1.4) |
| 2 | Store: equivocation evidence | evidence pool = one peer share; silently skipped when the peers' part is full [session.rs:298-320] | fixed part; four slots per accused key |
| 3 | Store: own events and own checkpoints | whatever is left of the whole [session.rs:256-258] | own seat, split into "my own choice" and "at a peer's request" |
| 4 | Store: receipts | one own-chain event per received event, charged to its author here and to me at everyone else | not stored as events at all; part of the attestation (1.5 choice C) |
| 5 | Store: another author's events and checkpoints | signer's share [session.rs:613-618, 666-667] | that author's seat (signer and causer are now the same party) |
| 6 | Store: countersignatures of my checkpoints | one per (checkpoint, member), countersigner's share [session.rs:579-585] | fixed part; one latest per countersigner |
| 7 | Store: cross-check records received | latest per (reporter, recipient) by rule, older ones stay; reporter's share [session.rs:802-806] | fixed part; two slots per reporter, replaced in place |
| 8 | Store: cross-check records I send | one own record each [session.rs:728-737] | not stored |
| 9 | Store: joiner anchors | author's share [session.rs:643-657] | fixed part; one per author |
| 10 | Memory: chains | every own and received event, in vectors [chain.rs:87; received.rs:127] | same content, so bounded by the seats (about twice the store with the store's copy) |
| 11 | Memory: roster history | one key set per version, no bound on main [history.rs:18-22] | at most 256 versions and 32 keys (1.4, backstop) |
| 12 | Memory: share levels known | one per (author, member), dropped on removal [session.rs:154, 470-471] | unchanged; at most 32 × 31 entries |
| 13 | Memory: duplicate digests, evidence sets, usage map | grow with what is stored [session.rs:158-162] | bounded by the fixed tables |
| 14 | Pending or out-of-order buffers | none exist; a refusal moves one number, `max_offered` [received.rs:359-373] | none; unchanged |
| 15 | Export size and time | at most the store, plus meta and seal [bundle.rs:1227-1240] | unchanged; the capacity stays 7/8 of the bundle caps |
| 16 | CPU per message | one signature check per event, checkpoint, countersignature; 1 + up to 8 for a cross-check record [equivocation.rs:348-407] | unchanged; stated in section 2; rate limiting is not this crate's |
| 17 | Total across sessions | no bound [r3 verdict R3-n5] | not this crate's; daemon (5.3) |

### 1.3 Every input: who causes it, who signs it, who is charged

"Causes" means the party whose free choice creates the cost, traced through automatic replies. V is the member whose store we are counting.

| Input at V | Causer | Signer | Charged at 882e094 | Charged in this design |
|---|---|---|---|---|
| X's event | X | X | X | X's seat |
| Receipt V writes for X's event | X | V | X here [session.rs:630]; **V at every member V shares with** | nothing: no record is written |
| Y's receipt for X's event, arriving in Y's chain | X | Y | **Y** | does not exist |
| X's checkpoint | X | X | X | X's seat while it has room; then one fixed slot per author |
| V's countersignature returned to X | X (by checkpointing) | V | not stored by V | not stored by V |
| W's countersignature of V's checkpoint | V (by checkpointing) | W | W [session.rs:579] | fixed slot, one per countersigner |
| R's cross-check record (broadcast or addressed) | R | R; entries signed by their authors | R | fixed slots, two per reporter |
| Evidence revealed by any input | the accused author (it signed both statements) | accused | evidence pool | fixed slots, four per accused |
| Roster version | starter | starter | starter's share | fixed part |
| Second roster with a held number (fork) | starter | starter | not stored | fixed part, one slot |
| X's share-level statement | X | X | memory only | memory only |
| V's own event, V's choice | V | V | Own | own seat, "free" part |
| V's own event, recorded because peer G asked | G | V | Own | own seat, G's "requested" allowance |
| V's own checkpoint | V | V | Own | own seat |
| V's cross-check record, sent | V | V | Own | not stored |
| Refused input (bad signature, gap, replay, not a member) | sender | anyone | nothing stored | nothing stored; CPU only |

### 1.4 The rule: a fixed part and eight seats

**Capacity** stays what it is: 7/8 of the bundle caps, 58,720,256 bytes and 229,376 records [882e094: src/session.rs:70-73; src/bundle.rs:47-51]. It is divided once, statically, into parts that never lend to each other.

**(a) The fixed part.** Every entry is a slot in a table whose size comes from hard bounds, with a maximum size per slot. An object larger than its slot's maximum is refused with its own error before anything else. The whole table is set aside in advance, so an input that belongs here is never refused for space. All numbers PROPOSED.

| Table | Slots | Max framed bytes each | Bytes set aside | Replaced in place? |
|---|---|---|---|---|
| Roster versions | 256 | 65,539 | 16,777,984 | no (each version once) |
| Roster conflict (a second, different version of a held number) | 1 | 65,539 | 65,539 | no (first one kept) |
| Evidence, four per accused key, 32 keys | 128 | 4,100 | 524,800 | no (first four distinct kept) |
| Attestations of my checkpoints, latest per countersigner | 31 | 1,028 | 31,868 | yes |
| Cross-check records received, latest per (reporter, broadcast or addressed to me) | 62 | 8,196 | 508,152 | yes |
| Joiner anchor (or the tombstone left by a release, 1.9), one per author | 31 | 516 | 15,996 | yes |
| Latest checkpoint beyond the log, one per author | 31 | 516 | 15,996 | yes |
| **Total** | **540** | | **17,940,335** | |

The 256 and the 32 are the roster's bounds as built on branch m3-roster (`MAX_VERSIONS`, `MAX_ENTRIES_EVER`) [m3-roster at 0a47fc9: crates/coagent-roster/src/lib.rs:66, 70; docs/ROSTER.md:122-123, 181-182]. The audit branch is built on main, where those bounds do not exist [06 §2.4 rule 4, citing main]. So the audit crate enforces the same two numbers itself, as a backstop with its own error (`RosterLifetime`), checked before the roster chain is touched. When the roster branch has merged, the roster crate refuses first and the backstop is unreachable; a test then asserts the constants are equal.

**Is 16.8 MB for the worst-case member-list history acceptable?** It is 29% of the capacity, held for a case (256 versions of the largest size) that only the starter can produce. I chose to set it aside in full, because the property "a member-list change is never refused for space" must not depend on an estimate. I rejected compacting the roster history: `verify` rebuilds the roster chain from the first version held and checks every cross-check record and countersignature against the version it names [882e094: src/bundle.rs:703-727, 806, 918-927], so dropping old versions would make older records unverifiable. The cheap way to get most of the space back is a tighter size bound published by the roster crate (REQUEST R-1, 4.4): each kibibyte less per version returns 256 KiB.

**(b) Eight seats.** What is left, 40,779,921 bytes and 228,836 records, is divided into eight equal seats of **5,097,490 bytes and 28,604 records**: one per roster slot. Slot numbers are 0 to 7 [882e094: crates/coagent-roster/src/lib.rs:283-288; 06 §1.1 rule 3].

- **A peer's seat** pays for that seat's occupant's chain as V holds it: its events and its checkpoints. A record is charged to the seat its author occupies in V's current roster at the moment V accepts it.
- **V's own seat** pays for V's own chain: its events and checkpoints. Its limit is the seat minus one byte per record (5,068,886 bytes), because a peer's copy of an event is one byte longer than the author's own record of it (`peer_event` against `own_event`); this is what makes property P7 hold. It is split:
  - **Free part, one half (2,534,443 bytes):** events V records by its own choice (`record`, `announce_share_level`) and V's checkpoints. Nothing a peer does can consume it.
  - **Requested part, one half, in seven equal allowances (362,063 bytes per other seat):** events V records because a peer asked, through a new call that names the peer (`record_for`). One requester cannot use another's allowance or the free part.
  - One closing checkpoint (516 bytes, one record) is kept back inside the own seat, so that when the seat is full the last events can still be covered by a checkpoint.
- A seat belongs to the slot, not to the key. If the starter replaces a member, the newcomer in that slot has what is left of the seat. This is what makes a succession of identities through one seat cost one seat [closes the mechanism of r3 verdict R3-m3]. Getting the space back is 1.9.
- `set_limits` lowers the capacity of the eight seats together, never the fixed part, and never raises anything above the default.

**What the seats hold, estimated (PROPOSED, not measured).** The gates measured synthetic events: 1,956 bytes per received full-tier event with its receipt [r1 verdict A-M4]; 602 bytes per receipt record (6,291,450 bytes for 10,452) [`release_receipt_proxy.txt`]; and 5,914 bytes per maximum-size event with its receipt (6,286,450 bytes for 1,063) [`release_flood_measurements.txt` (c)]. Subtracting the receipt: about 1,350 bytes per ordinary event and about 5,300 per maximum-size one. Then a peer's seat holds about 3,800 ordinary events (about 960 at maximum size); the free part about 1,800; one requester's allowance about 270. For comparison, 882e094 gives a peer 6,291,456 bytes including its receipts, which is about 3,200 ordinary events, and gives the member's own log at least 14 MB. So what others hold of each person is about the same, and the member's own log is smaller. Real sizes are UNKNOWN (U2).

### 1.5 Design choices: each candidate, chosen or rejected

| | Candidate | Decision | Why |
|---|---|---|---|
| A | Charge the causer, not the signer | **Chosen**, by removing the cases where they differ | A third member cannot identify the causer of another member's automatic record without being told something it is not entitled to (1.1 item 1). So no automatic record may enter a log. After choices C and D, every record in a chain is its author's own choice, except events recorded at a peer's request, where the recording member knows the causer and names it (`record_for`). |
| B | Budgets per (causer, kind) with reserves | **Rejected in that form; chosen per causer** | One budget per kind per causer multiplies the limits to test (the surviving mutants P01, P02, P05, P06 were all such limits) and still needs a rule for kinds added later. Per-kind bounds exist only where the kind is latest-state, and there they are slot counts, not budgets. |
| C | Receipts free of storage: one cumulative record per (author, reader), replacing the previous | **Chosen**, as a field of the countersignature | A countersignature of X's checkpoint by V already says "this head conflicts with nothing I hold" [882e094: src/checkpoint.rs:109-129]. It gains one signed field, `held_from`: `Some(n)` when V holds every header from n to the checkpoint's number, `None` when it does not (a member at `nothing`, or one whose seat for X is full). X keeps the latest one per member. That is the receipt: "V holds my log from n to here". No new signing domain; no change to the crypto crate. |
| D | Latest state per key instead of a log, wherever the log is not the evidence | **Chosen** for countersignatures (a later one covers every earlier checkpoint of the same chain, because the hash at n commits to everything before it), cross-check records received (the entries are other authors' statements; an older record adds nothing a newer one from the same reporter lacks, and any conflict it revealed is already evidence), and joiner anchors. **Rejected** for other authors' checkpoints: for a member at `nothing` the checkpoints are all it holds, and two such members can only catch an author by comparing checkpoints at the same number, so the log is the evidence. They stay a log in the author's seat, capped at 1,024 as now [882e094: src/received.rs:41], and beyond the cap or a full seat the newest is kept in one fixed slot. |
| E | Control-plane priority with a reserve sized from the roster's hard bounds | **Chosen** (1.4 a) | |
| F | Back-pressure instead of failure | **Chosen** (1.8) | |
| G | End of a budget: sealed segments, a hard lifetime, or export-and-truncate | **A fixed capacity per session is what this build has; export-and-truncate only for removed members (1.9); "seal and continue" is designed in outline (1.12) and not built.** INTERPRETATION (for Kam) I-A2 | A fixed capacity closes the class with the fewest moving parts, and the roster already gives every session a hard lifetime (256 versions, 32 entries). The capacities in 1.4 are small for long sessions, so I recommend building 1.12 next. |
| H | Size the seats by the limit in force (4 people: quarters) | **Rejected** | After a raise from 4 to 8, four seats could already hold a quarter each, which is the whole space; the four new seats would then need space that does not exist, and a global check would let one seat squeeze another. Static eighths are, in the words of 06 §1.2, "exact at 8 and merely cautious at 4". |
| I | Release the space automatically when a member is removed | **Rejected** | Removal is the starter's act. Automatic release would let a starter make every member's computer drop its record of someone by removing them. Release is the member's own deliberate act (1.9). |
| J | Keep per-key shares and a common pool | **Rejected** | This is 882e094; rotation through re-adds fills the pool [r3 verdict R3-m3]. |

### 1.6 The invariant

**For the owner, one sentence.** Whatever anyone else sends, in any amount and any order, your computer can still apply member-list changes, keep and export proof that someone lied, and record your own actions, and each other person can use up only their own seat and their own allowance.

**For a test.** Let V be an honest member with limits L. For every finite sequence of calls on V's `SessionAudit` (every public function, with valid and invalid inputs, by any set of parties, under any roster history within 8 members, 32 entries and 256 versions), after every call:

1. **Fixed part never refuses for space.** `apply_roster` returns exactly what the roster chain returns (or `RosterLifetime` at the two bounds); evidence against a key with a free slot is stored; a countersignature, cross-check record or anchor that passes its checks is stored. None of these can return `LogFull`.
2. **Charges depend on the causer only.** The bytes and records charged to seat s, and whether an input caused by seat s is refused for space, are a function of the roster history and the inputs caused by seat s alone. For V's own seat: the free part's usage is a function of V's own `record`, `announce_share_level` and checkpoint calls alone.
3. **Bounds.** Usage of every table and seat is at most its limit; the limits sum to at most the capacity; the sum of (4 + length) over what the store holds equals the sum of the usages.
4. **Accounting is a function of the store.** A `SessionAudit` rebuilt from the store alone has the same usages, accepts and refuses the same next input, and exports the same bytes.
5. **Export.** `export` succeeds and `verify` accepts it.

Section 3 turns these into nine properties with red controls.

### 1.7 One order of checks for every input

Every function that takes a peer's object does its work in this order, and a later step never runs if an earlier one refuses:

1. **Cheap refusals:** size against the kind's maximum, session, addressee, membership of the signer (and "removed" where the rule says nothing is kept from a removed member).
2. **Signatures.**
3. **Conflicts.** Compare with what is held. Evidence found is stored in the fixed part and is ALWAYS part of what the caller gets back, whatever happens next [closes R3-n1]. A fork is reported as a fork, never as a space refusal [closes R3-n2].
4. **The roster crate's own answer** for a roster version, before any storage question [closes R3-n3].
5. **Space**, only for seat-charged inputs, with the exact size of the record that will be stored. No estimate, no worst-case reservation.
6. **Apply and store**, all or nothing.

Step 5 needs the own event to exist before it is stored, so appending to the own chain becomes two steps (make, then commit); a refusal at step 5 leaves the chain unchanged.

### 1.8 The end of a budget, and back-pressure

Nothing here is silent, and nothing here touches the fixed part.

| What is full | What V does | What V tells the peer | What stops | What continues |
|---|---|---|---|---|
| Peer X's seat at V | refuses X's further events with `LogFull`; keeps X's newest checkpoint in the fixed slot; countersigns it with `held_from: None` | X sees its receipts from V stop advancing (signed). V's status for X (below) says "full, holding through n" | V keeping copies of X's events | everything else at V; V still witnesses X's checkpoints, so X's log stays tamper-evident and cross-checked at checkpoint level; X's own log is unaffected |
| G's requested allowance in V's own seat | `record_for(G)` returns `LogFull` | the daemon must decline G's further requests that need recording | V acting for G in this session | V's own free recording; V acting for others |
| V's free part | `record` returns `LogFull`; one closing checkpoint still fits | V's status to everyone says "own log full" | V recording new actions of its own choice | V applying member-list changes, storing evidence, receiving, witnessing, exporting |
| Evidence slots of one accused (4) | further evidence against that key is returned to the caller, not stored | n/a | n/a | one already convicts |
| Roster lifetime (256 versions or 32 entries) | `RosterLifetime` | n/a | membership changes; the session must end and a new one start, as the roster design says [06 §2.4 rule 4] | everything else |

**Status.** A new read-only call gives, per seat and for the own parts: used, limit, and a state (`Ok`, `Warn` at 75% PROPOSED, `Full`), plus per author the highest number held. The daemon carries it to peers as an ordinary non-audit message inside the authenticated pairwise channel; a receiver keeps only the latest per sender, in memory. It is information, not proof; the proof is the attestation's `held_from`.

**What the product shows (PROPOSED wording, for the daemon and interface lanes; UNDECIDED D4).** At V, when Sam's seat fills: "Your computer has stopped keeping copies of Sam's activity for this session: Sam's share of your audit space is full. You keep everything received so far and still witness Sam's checkpoints." At Sam: "Kam's computer has stopped keeping copies of your activity log (its space for your records is full). Your own log is not affected." At V, own log full: "Your activity log for this session is full. New actions cannot be recorded. Export the log and continue in a new session." At V, Sam's allowance full: "The space for actions done at Sam's request is full. Sam's further requests are declined in this session."

**A long, busy, honest session** therefore ends in one of the first three rows, each visible on both sides before it happens (the meter) and when it happens. It never reaches the state the third check found: member-list changes always apply.

### 1.9 Release when a member is removed or replaced

A removed member's records stay where they are, charged to its seat, until V itself decides otherwise. One new call does it: **archive and release**. It is allowed only for a key that is not a member of V's current roster. In one step it (1) builds the ordinary sealed export of everything V holds, and returns it to the caller, (2) deletes that key's events and checkpoints from the store, (3) leaves the key's newest held checkpoint in its anchor slot as a tombstone, and keeps every evidence record and fixed-part slot, (4) lowers the seat's usage by exactly what was deleted. The returned file verifies like any export; the store after release also exports and verifies; verifying the two together shows them agreeing on the tombstone. If the same key is later re-added, V treats it as a joiner whose view starts at a checkpoint the author hands it (the existing `join_author` path); re-anchoring a chain that has moved on is still BACKLOG [r1 verdict A-m6] and this is where it will show.

Without a release, the newcomer in a used seat has only what is left of it. The starter can avoid that by using another slot.

### 1.10 Restart

The store becomes keyed (4.2): every stored object has a key that says which table or seat it belongs to, so the usages are a sum over the store and nothing else. `start` refuses a store that already holds this session (a new error), because starting an empty chain over a stored one makes the member sign its event numbers a second time, which is equivocation against itself [r1 verdict A-m5]. A new `resume` rebuilds everything from the store: roster chain, own chain, every received chain, the fixed tables, the usages. Share levels learnt from statements are rebuilt only where the statement's event is held; otherwise they revert to `nothing`, which is the safe direction. Property P5 checks that a resumed member is indistinguishable from one that never stopped [closes R3-m1].

### 1.11 A provisional member (admitted by a deputy)

06 §2.8.10 left this UNDECIDED and gave a default: "a provisional member takes no part in the audit exchange". For the accounting, that default is safe and is what this design assumes, and I state it as a rule so that it is tested:

- A key that is not in the member list of a roster version V holds is not a party. Every object it signs, or that names it as author or reporter, is refused at step 1 of 1.7 (`NotMember`) before any signature check, because V has no key for it. Stored cost: zero. CPU: one lookup. This is what the code does today on each path [882e094: src/session.rs:593-595, 574-577; src/equivocation.rs:358-361].
- `record_for` refuses a causer that is not a roster member. So V's daemon cannot record actions as "requested by" a provisional member; whether it may act for one at all is not this document's decision.
- **What a later decision to let provisional members take part must supply:** a session-lifetime bound on provisional keys. The fixed tables are sized for 32 keys ever. 06 §2.8.9 bounds admissions per epoch (at most 7) and keeps none from old epochs, which bounds what is held at one time, not how many keys ever appear. Without a lifetime bound the tables cannot be sized. A provisional member sits in a real slot [06 §2.8.8], so the seat it would be charged to already exists and no new budget is needed. This stays UNDECIDED (D1).
- A hostile deputy is a roster member (a guest) and is covered by the "one hostile member" row of section 2. Nothing a deputy signs as deputy reaches this crate.

### 1.12 "Seal and continue" (designed in outline; NOT built by this design's build)

The way to lift the fixed capacity without giving up any property above. V, by its own decision and never because a peer's traffic forces it: issues a checkpoint; exports the ordinary sealed file and hands it to the caller to keep; then rewrites its store so that every chain starts at a signed checkpoint (its own chain at its own checkpoint, each current member's chain at that member's newest checkpoint V holds, plus the events after it), keeping the fixed part whole. The seats are empty again. The existing joiner machinery already supports a received chain that starts at a checkpoint; what is new is an own chain that starts at one, a pointer in each file to the file before it, and `verify` reporting "this file starts at number n; the earlier file is needed for what came before". What it costs in trust: one file then proves less by itself than today (an exporter can show only the latest file), and it says so. A peer cannot force a seal, so a peer whose seat is full waits for V's next one; how often V seals, and how many sealed files it keeps, are V's own settings. It is additive to this design: nothing in sections 1.4 to 1.10 changes.

---

## 2. The threat table

Default limits; every number follows from 1.4 and is PROPOSED. S = one seat = 5,097,490 bytes and 28,604 records. "At V" means on an honest member V's computer. The CPU figure is the gate's: 100,000 refused cross-check records took 5.75 s in a release build, about 57 microseconds each, on the gate's machine [`release_flood_measurements.txt` (a)]; nothing in this crate limits how many messages arrive, the channel and daemon must (D3).

| Who | The most they can cost V | What they can never do |
|---|---|---|
| **One hostile member X** (not the starter) | **Its own seat:** S, in about a second at the measured rate [r3 verdict §2 (b)]; after that X's events are refused and V keeps witnessing X's checkpoints. **Fixed slots that are X's:** one attestation (1,028 bytes), two cross-check records (16,392), one anchor and one latest checkpoint (1,032); each replaced in place however many X sends. **Evidence against itself:** four slots (16,400 bytes). **V's requested allowance for X:** 362,063 bytes of V's own log, if V acts on X's requests. **Through a third member H:** H's allowance for X, 362,063 bytes, which reaches V inside H's seat, 7% of it. **CPU:** one signature check per message, nine for a cross-check record with eight entries. | Use any other seat, the free part or the fixed part. Stop V applying a roster version, including X's removal. Stop V storing or exporting evidence. Make V's export fail `verify`. Make V write anything automatically: V writes no record in reply to any message. |
| **k colluding members, up to seven of eight** | k seats: at most 7 × S = 35,682,430 bytes. k requested allowances in V's own log: at most half of V's own seat. In an honest H's log as V holds it: at most half of H's seat, the other half being H's free part. Every fixed slot of theirs. Evidence slots only for keys that really signed two stories. CPU as above, times k. | The same four things. With all seven hostile, V still has its whole free part (about 1,800 ordinary events), the whole fixed part, and a verifying export. |
| **A hostile starter** | Everything a member can, plus: **the roster reserve**, 256 versions of at most 65,539 bytes, 16.8 MB on disk (and the roster chain's own in-memory copy of each version, which 06 §2.4 reads on main and I did not re-read), after which the session's membership can no longer change; **the conflict slot** (65,539 bytes) by forking the roster, which is stored as proof against it; **identity rotation**, at most 32 entries ever, each seat still at most S whatever number of keys pass through it. | Exceed the fixed part. Make V drop anything (release is V's own act). Hide a roster fork from a member who sees both versions. **Honest limit:** the starter is the only source of member-list changes, so a starter can always withhold them, end the roster's lifetime by issuing versions, or issue a version too large to be recorded (1.1); these are the starter breaking its own session, visible as a refused version. |
| **A hostile deputy** | As a roster member: the "one hostile member" row. As deputy: nothing; no deputy object reaches the audit crate. | Anything beyond a member's row. |
| **A provisional member** | Zero bytes. One table lookup per message (no signature check: V has no key for it). | Have anything stored; be named as the requester of a recorded action (1.11). |
| **A removed member** | Zero new bytes, with one exception: evidence its messages reveal (against whoever signed two stories, four slots per accused). What it stored before removal stays in its seat until V releases it (1.9). CPU: signature checks on what it keeps sending (1 + up to 8 per cross-check record; 57 microseconds measured for an empty one). | Have any event, checkpoint, countersignature or cross-check record kept. |
| **The relay** | Zero bytes: it holds no member key, so it can only replay, reorder, delay or drop what members sent. A replay is a no-op, because every stored object has one key (4.2). CPU: at most the signature checks of whatever passes the channel's own replay protection, which is outside this crate. | Forge anything. **Honest limit:** it can delay or drop, so a member can be late learning of a removal, as today [06 §2.8.6; 04 §3.5]. |

**Residual costs, stated once more without softening.** A hostile member can make V hold about 5 MB of junk for the rest of the session unless V releases it after the removal. Seven can make V hold about 36 MB. A hostile requester can end V's willingness to act for them, and take 7% of what others hold of V. Anyone can make V burn CPU on signature checks until something outside this crate slows them. An honest member's own log is finite and fills from its own activity.

---

## 3. The properties that close the class

Nine properties. Each is a property test over generated sessions: a harness that builds 2 to 8 members with fixed test keys, applies roster operations within the bounds (add, remove, re-add the same key, a new key in a used slot), and at each step draws one input from the whole alphabet: a valid event at any tier, a replay, a gap, a forked event, a checkpoint, a forked checkpoint, a countersignature (valid, stale, by a non-member, by a removed member), a cross-check record (broadcast, addressed, advancing, not advancing, carrying a fork, from a removed reporter, addressed to someone else), a share-level statement (valid and invalid), every object with a bad signature, a roster version (valid, replayed, forked, out of order), own `record`, `record_for`, a checkpoint, `resume`, and archive-and-release. Limits are drawn small so budgets fill within a test. Every fixture is generated inside the test.

Each red control is a deliberately broken build (the existing `cfg(coagent_audit_red = …)` mechanism) that must make the named property fail on that property's own assertion text.

| # | Property (holds after every step of every generated schedule) | Red control that must make it fail |
|---|---|---|
| **P1** | **Control always fits (the adversarial-schedule property).** The victim can still (a) apply the next valid roster version and gets the roster crate's own answer, never `LogFull`; (b) store, and get back, evidence for a fresh conflict by any author with a free slot, and find it in the export; (c) record an own free event whenever the bytes of its own earlier free records and checkpoints, as the test itself counted them, leave room. | `roster_on_seat` (the version is charged to the starter's seat, as at 882e094) fails (a). `evidence_on_seat` (evidence charged to the reporter's seat) fails (b). `requested_takes_free` (`record_for` charged to the free part) fails (c). |
| **P2** | **Seats do not interfere.** Run the schedule twice: once whole, once with every input caused by seats other than s (and other than the victim) removed, roster operations kept. The bytes and records charged to s, and the set of s's inputs refused with `LogFull`, are identical. The same for the victim's free part against every peer input. | `shared_peer_pool` (882e094's check that all peers together stay under a common limit, src/session.rs:259-269). |
| **P3** | **Bounds and exact accounting.** Every table and seat is at or under its limit in bytes and in records; the sum of (4 + length) over the store equals the sum of the usages; no stored object exceeds its kind's maximum; fixed part + eight seats ≤ capacity ≤ 7/8 of the bundle caps (pinned numbers). | `no_seat_limit` (bytes); `no_seat_record_limit` (records; the guard mutants P01 and P02 lacked); `uncharged_slot` (a slot write that skips the usage). |
| **P4** | **Latest state.** However many are sent: stored attestations ≤ one per countersigner key; cross-check records ≤ two per reporter key; anchors and latest-checkpoint slots ≤ one per author; evidence ≤ four per accused; and the stored one is the latest by its rule. | `hs_store_not_latest` (exists); `cs_keep_all` (every countersignature kept). |
| **P5** | **Accounting is a function of the store.** After any prefix, `resume` on a copy of the store gives the same usage for every table, seat and key, the same answer to every possible next input, and a byte-identical export. `start` on a used store is refused. | `resume_all_own` (882e094's behaviour, src/session.rs:194-212); `start_on_used_store`. |
| **P6** | **Evidence before space.** An input that conflicts with something held yields the evidence, returned and stored, in every state of every seat; a fork is never answered with `LogFull`. | `space_before_fork` (882e094's order, src/session.rs:614-620); `evidence_not_returned` (882e094's `LogFull` after storing, src/session.rs:784-803). |
| **P7** | **An honest author is never refused for space by an honest peer.** With equal limits, every event an honest member's own log accepted is accepted by every honest member that receives it in order; the author meets its own limit first. | `own_seat_too_large` (the own limit set above a peer's seat). |
| **P8** | **The export always verifies.** After every step, including full seats, a resume and a release: `export` is `Ok`, `verify` accepts it, and `verify`'s attestations equal the author's own. | `cs_rule_current_only` and `verify_cs_rule_head_rv_only` (exist; the round-1 disagreement between author and `verify`, now under "latest per countersigner"); `store_limit_full_cap` and `export_cap_plus_one` (exist) on the pinned arithmetic. |
| **P9** | **Release gives the seat back and loses nothing.** After archive-and-release of a removed key: the seat's usage fell by exactly that key's charge; a new occupant can fill a whole seat; the returned file verifies and holds every record that was deleted; evidence and fixed slots are unchanged; the store after release exports and verifies. A release of a current member is refused. | `release_keeps_charge` (the mechanism of R3-m3); `release_before_export` (the file is built after the deletion). |

**Why these nine close the class, as an argument (REASONED).** The class is: an input caused by party A exhausts storage that party B needs for an action. P3 says all storage is in a table or a seat. P1 covers the tables B needs for control (they are set aside whole, so there is nothing to exhaust). P2 says what A causes lands only in A's seat or A's allowance, so the only storage A can exhaust is storage whose sole use is A's own further input. P4 says no fixed table can be grown by repetition. P5 says none of this can be reset or corrupted by a restart, and P9 that it can be undone only by the owner. P6 removes the two ways a full seat hid evidence. P7 says honest parties never meet a refusal they did not cause themselves. P8 says the result is always exportable. What the properties do NOT cover is in 5.3 and in "where a fourth check will look" at the end.

**Single checks that need their own guard and red row** (the third check's Minor R3-m2 and Note n3; a check that no longer exists is named as gone, not guarded):

| Gate id | The check | In this design | Guard and red row |
|---|---|---|---|
| P01 | per-peer record quota | the seat's record limit | P3, `no_seat_record_limit` |
| P02 | own reserve counted in records | the free part's record limit | P1 (c) run with a record-only limit, `free_records_unreserved` |
| P05, P06, N14 | receipt byte and record reserve; own worst-case reservation | **gone**: no receipt record, and space is checked with the exact size (1.7 step 5) | one guard for the replacement: an own record that exactly fills the remaining room is accepted, one byte more is refused; `own_size_off_by_one` |
| P08 | a cross-check record at a LOWER roster version does not advance | kept | `hs_lower_version_advances` |
| P09 | a lower number for a held author does not advance | kept | `hs_lower_seq_advances` |
| P16 | a share-level statement must be of the share-level kind | kept | `share_any_kind` |
| P18 | levels learnt FROM a removed author are forgotten | kept | `share_keep_from_removed` |
| P22 | a statement naming a roster version not held is refused | kept | `share_unheld_version` |
| P27 | the evidence cap's value | 4, pinned: a fourth distinct evidence is stored, a fifth is returned and not stored | `evidence_cap_value` |
| P28 | `set_limits` cannot raise | kept | `limits_may_raise` |
| N06 | `verify`: the reporter was a member AT the record's roster version, not merely by then | kept; guard on the `verify` path with a bundle built in the test | `verify_hs_reporter_by` |
| R3-n3 | re-applying a held roster version gives the roster crate's answer | 1.7 step 4 | P1 (a) includes replays; `roster_space_before_apply` |

---

## 4. What changes against 882e094

### 4.1 Signed and exported formats

| Object | Change |
|---|---|
| Event header, chain hash, tiers, previews, checkpoint (`audit.head`), cross-check record (`audit.heads.seen`), evidence, seal, all five signing domains | **None.** No change to `coagent-crypto`, `coagent-proto` or `coagent-roster` is required. |
| Countersignature | **One new signed field, `held_from: Option<u64>`** (1.5 C). Its signature bytes change. Nothing is released, so no stored log is orphaned. `verify` checks `1 ≤ held_from ≤ author_seq` when present. |
| Receipt events (`audit.receipt`) | **No longer produced.** The kind name stays defined and has no special handling; a member may not rely on finding one. |
| Bundle | Format number 2. One new record kind, the roster conflict (a starter-signed version with a held number and different content; `verify` reports it as a roster fork). Cross-check records in a bundle are the ones received; the ones sent are no longer stored. Countersignatures in a bundle are at most one per countersigner. `verify`'s ordering and refusal rules for existing kinds are unchanged, so a file's checks do not get weaker. |
| Store records | Keyed (4.2). The store is internal; no released data exists. |

### 4.2 The store and the public functions

- **`Store`** becomes keyed: put (insert or replace) under a key, remove a key, list entries; `records` (the values, as canonical `Record` bytes) stays because tests read it. The key names the table or seat, the author and the number or slot. Consequences that close whole cases by construction: a replay writes the same key with the same bytes and changes nothing; a superseded slot record is physically gone, so the store's real size equals the accounting.
- **Kept with the same signature and name**, so the three gate files keep compiling: `receive`, `receive_head`, `receive_heads_seen`, `add_countersignature`, `apply_roster`, `record`, `checkpoint`, `checkpoint_now`, `heads_seen`, `heads_seen_for`, `note_share_level`, `announce_share_level`, `export`, `set_limits`, `limits`, `store_usage`, `usage_of`, `StoreLimits`, `Payer`, and the errors `LogFull`, `Duplicate`, `NotNewer`, `ReporterRemoved`.
- **Meaning changed under a kept name:** `StoreLimits` is the capacity of the eight seats; `per_peer()` is one seat; `own_reserved()` is the own seat; `peer_pool()` is seven seats; `usage_of(Payer::Peer(k))` is what key k's chain occupies; `usage_of(Payer::Evidence)` is the evidence table; `receive` appends no receipt; `heads_seen` and `heads_seen_for` store nothing and cannot fail for space; `add_countersignature` keeps the latest per member (an identical one again is `Ok`, an older one is `NotNewer`); `AuthorChain::attestations` lists each member under its latest countersigned checkpoint only.
- **New:** `resume`; `record_for`; archive-and-release; the status call of 1.8; a seat-usage query; the errors for a used store at `start`, an object above its kind's maximum, and `RosterLifetime`.
- **Removed:** `AuthorChain::append_receipt` and the receipt reservation constant.

### 4.3 The existing tests

I read the test files; I ran nothing. The counts are the gate's: 114 passing and 5 ignored at 882e094 [r3 verdict §2]. What follows is by reading, and the build seat's first duty is to replace it with what actually runs red and green (U3).

**Rule.** A gate file (`gate_attacks.rs`, `gate_r2.rs`, `gate_r3.rs`) is never weakened. An assertion that the redesign makes meaningless is marked with a ruling comment, the old line quoted, and a replacement test that asserts the property in its new form. Builder-owned test files may be rewritten where their subject changed, each change listed with what guards the property now.

**Gate file `gate_r3.rs` (14 tests; all passed at 882e094, each `r3_finding_*` passing meant the weakness was shown).**

| Test | By reading | Why, and what replaces it |
|---|---|---|
| `r3_finding_convener_quota_full_blocks_every_roster_update` | **void** | It asserts `apply_roster` is `Err(LogFull)` and that the removed member is still accepted (lines 125-131). Its loop also drives the store through receipts (`c.outgoing(c.own().seq())` after each `receive`, lines 107-109), which no longer exist. Replaced by P1 (a) and a named test: the starter's own events fill its seat at a non-starter victim, the removal applies, and the removed member's checkpoint and cross-check record are then refused. |
| `r3_finding_other_members_fill_the_conveners_quota_through_its_receipts`, `r3_finding_release_receipt_proxy_default_limits` | **void** | The mechanism (a receipt per event, lines 181-187) is gone. Replaced by P2 and a release-build measurement of the same flood: zero records reach the victim through the starter, the roster applies. |
| `r3_ok_current_member_fresh_empty_records_are_not_newer` | valid as it is | One stored per (reporter, recipient); now by slot. |
| `r3_ok_colluder_advancing_records_stop_at_the_reporters_quota` | **void** | It loops until `LogFull` (lines 283-293); advancing records now replace one slot and never fill anything, so the loop would run to its five-million guard. Replaced by P4: after N advancing records the reporter holds one slot and the store has not grown. |
| `r3_release_flood_measurements` | part (b) **void** for the same reason; parts (a) and (c) valid | (c)'s numbers change (no receipts). |
| `r3_finding_restart_charges_existing_peer_records_to_own` | **void** | It calls `start` on a used store (line 417), now refused. Replaced by P5. |
| `r3_finding_evidence_not_stored_when_peer_pool_full` | **void** (line 514) | The call now returns the evidence. Replaced by P6. |
| the four `r3_ok_share_statement_*` | valid as they are | Nothing they test changes. |
| `r3_finding_identity_rotation_fills_peer_pool_and_blocks_rosters_at_non_convener` | valid as it is, and weak | Its one assertion is that the own record succeeds (line 695). P9 and P2 assert the rest: the honest peer gets a whole seat. |
| `r3_finding_fork_from_an_author_at_quota_gives_logfull_not_evidence` | **void** (line 725) | The fork is now reported as a fork. Replaced by P6. |

**Gate file `gate_r2.rs` (19 tests).** `r2_finding_receipt_headers_give_a_nothing_member_count_and_time_of_each_event` is **void**: it asserts the member holds five receipt events (line 348 onward); there are none, and the leak it demonstrated is closed. Replaced by a test that a `nothing` member receives no object whose count or time follows another author's events, by any route. `r2_finding_checkpointing_ends_after_the_per_author_cap` is **void** in its assertion that later checkpoints are refused: beyond the cap the newest checkpoint is kept in its slot and is still countersigned; replaced by a test that the stored checkpoints stay at the cap plus one slot while attestation continues. `r2_measure_release_verify_on_a_maximum_size_bundle` stays valid with different numbers. The other sixteen are unaffected by reading.

**Gate file `gate_attacks.rs` (17 tests).** No assertion becomes meaningless by reading. The release flood test now exercises the checkpoint slot beyond the cap.

**Builder-owned files: tests whose subject changed.** `join_leave.rs::receipts_name_the_stored_header` (receipts) is replaced by a test of `held_from`. `countersign.rs::test7_who_attested_to_what_is_exact` and the attestation lines of `join_leave.rs` and `gate_return.rs` (a1_m2) expect a member listed under every checkpoint it countersigned; now it is listed under its latest. `bundle.rs` and `tamper.rs` fixtures count events that included receipts. `gate_return.rs::a1_b1_*` searches for receipt summaries and has a positive control that they exist. `gate_return_r2.rs`: the three `r2m1_*` quota tests and `n15_*` pin the old arithmetic (a quarter reserved, sevenths of the rest). Each is rewritten to the new rule; the properties P1 to P4 carry what they guarded.

**Red controls (93 rows at 882e094).** Rows whose broken variant no longer has code to break are retired with the reason written in the runner, as was done once before: `no_own_reserve` and `no_peer_quota` are replaced by `shared_peer_pool`, `no_seat_limit` and `requested_takes_free`; `evidence_no_cap` is replaced by `evidence_cap_value`; `receipts_unfiltered` goes with receipts, its property carried by the replacement for the round-2 receipt test. Every other row is expected to stay. A red control must still go red on its named property.

### 4.4 Requests to other crates (none is needed for this design to hold)

- **R-1, roster crate (optional, recovers space):** publish the largest encoded size a valid roster version can have, as a constant with a test that builds that version. The audit reserve is then 256 times that instead of 256 × 65,539.
- **R-2, roster crate (after its merge):** nothing to change; the audit crate adds a test that its two backstop numbers equal `MAX_VERSIONS` and `MAX_ENTRIES_EVER`.

---

## 5. Decisions, unknowns, undecided

### 5.1 INTERPRETATION (for Kam): each choice, with the alternative in plain language

| # | I chose | The alternative |
|---|---|---|
| **I-A1** | "I received it" becomes one running signed note per person ("I hold your log from item n to item m"), replacing the last one and sent only to that person. **Lost:** the exact moment each single item was received, and other members seeing that you received it. **Gained:** receipts cannot be used to multiply a flood, and a person you share nothing with no longer learns the timing of your items through other people's receipts (the leak the second check measured). | Keep one "received" line per item, with a cap of its own. The flood route is then limited rather than removed, and the timing leak stays. |
| **I-A2** | A session has a fixed recording capacity (line 7 of the summary). A meter shows it; a full seat stops only that seat; to carry on at full recording you start a new session. | Build "seal and continue" now (1.12): the program files the full log away as a finished, checkable file and carries on in the same session, for any length. It is more to build and to check in this round. My recommendation: fixed capacity now, "seal and continue" as the next piece, because about 270 requested actions per person is small for a long session in which you let someone's requests run without asking each time. |
| **I-A3** | Eight equal seats, yours included, whatever the number of people present. With four people, half the space sits unused. | Give yourself a larger share and others smaller ones; or size seats by the limit in force (rejected, 1.5 H: after a raise from 4 to 8 the seats could squeeze each other). |
| **I-A4** | When a person's seat on your computer is full, your computer stops keeping their records but keeps witnessing their checkpoints, so their log stays tamper-evident. | Stop exchanging audit messages with them altogether, or pause the session with them until someone acts. |
| **I-A5** | A removed person's records stay on your computer, using their seat, until YOU choose "file away and free the space". | Free the space automatically at removal. Then a starter could make everyone's computer drop its record of a person by removing them. |
| **I-A6** | Cross-check messages your computer SENDS are no longer kept in your own log. | Keep the latest one per recipient (a little space, no evidence value I can find). |
| **I-A7** | Only each person's LATEST countersignature of your checkpoints is kept. It covers every earlier checkpoint, because each checkpoint commits to everything before it. **Lost:** the list of who had countersigned at each earlier point. | Keep every countersignature. It needs space set aside per checkpoint, which is the kind of estimate that failed before. |
| **I-A8** | Witnessing of checkpoints no longer ends after 1,024 checkpoints per person (about 17 hours); beyond that the newest is always kept. This removes a limit the second check recorded. | Leave the limit and its documented end. |
| **I-A9** | Actions your computer records because another member asked are counted against that member's allowance inside your log (one fourteenth of your seat each), so a requester cannot use up your log. When their allowance is full, their further requests are declined. | No allowances: simpler, and one requester can then fill your log, which is the class of fault this redesign exists to close. A different split between "my own choice" and "requested" is a number, not a principle (D6). |
| **I-A10** | 16.8 MB, 29% of the space, is set aside for the largest possible member-list history. | Ask the roster crate for a tighter size limit and get most of that back (R-1). I did not assume it. |

### 5.2 UNKNOWN: why, and what closes it

| # | Unknown | Why | What closes it |
|---|---|---|---|
| U1 | The largest encoded size of a valid roster version; whether one can come within a few bytes of 65,535 | I read the bounds, not a measurement. On main the `removed` list has no bound of its own [06 §2.4]; on the roster branch members plus removed are at most 32 | A roster-crate test that builds the largest valid version (R-1) |
| U2 | Real event sizes, and so how many events a seat holds | The gates' events are synthetic | A measurement in the daemon lane on recorded real sessions made in a scratch tree |
| U3 | Which of the 114 tests and 93 red rows change colour beyond those named in 4.3 | I ran nothing | The build seat's run at each step, recorded |
| U4 | Memory of `verify` alone, and of a member at full seats | Never isolated [r2 verdict §9]; the gate measured 206 MB for a whole test process at three full shares [r3 verdict §2] | A release measurement by the build seat |
| U5 | That the proposed slot maxima (4,096 bytes for evidence, 8,192 for a cross-check record, 1,024 for a countersignature, 512 for a checkpoint) are above the largest object the code can accept | Estimated from field sizes | A test per kind that builds the largest acceptable object; if one is larger, the maximum is raised and the table of 1.4 recomputed, before anything else is built on it |
| U6 | My reading in 1.1 that a near-maximum roster version is refused by the audit crate | Not run | A test at 882e094 in the first commit |

### 5.3 UNDECIDED (not guessed)

| # | Undecided | Who decides |
|---|---|---|
| D1 | Whether a provisional member takes part in the audit exchange, and the lifetime bound on provisional keys that would need (1.11) | Design owner, with the deputy lane |
| D2 | Whether "seal and continue" is built now or next (I-A2) | Kam |
| D3 | Who limits message RATE. This crate bounds storage and bounds CPU per message; it does not bound messages per second | Daemon and channel lanes [04 §3.8 "Token bucket per member"] |
| D4 | The product's wording and where the meter is shown | Interface lane |
| D5 | The daemon rule that makes I-A9 true: every event recorded without a local human act is recorded with `record_for` naming the member whose message triggered it. The crate cannot check this; it is a written precondition of wiring the daemon | Daemon lane; a BACKLOG entry and a daemon test |
| D6 | The split of the own seat (half free, half requested) | Kam or the design owner, after U2 |
| D7 | The total across sessions a peer shares with a member [r3 verdict R3-n5] | Daemon lane |

### 5.4 Every number proposed here

All "proposed, not measured": every row of the fixed-part table in 1.4; the seat (5,097,490 bytes, 28,604 records); the own-seat limit and its halves; the closing-checkpoint reserve; the warning level (75%); evidence per accused (4, already in the code [882e094: src/session.rs:83]); the event-count estimates. Kept from the code and not mine: capacity 7/8 of 64 MiB and of 262,144 records; record cap 65,535; 1,024 checkpoints per author.

---

## Appendix: what I read

Whole: the three verdicts (`gate_M3_AUDIT_verdict.md`, `_r2_`, `_r3_`); `gate_r3.rs`, `release_flood_measurements.txt`, `release_receipt_proxy.txt`; at 882e094 `src/session.rs`, `store.rs`, `received.rs`, `chain.rs`, `bundle.rs`, `equivocation.rs`, `checkpoint.rs`, `history.rs`, `error.rs`, `lib.rs`, and `docs/AUDIT.md`; STATUS_M3_AUDIT.md section 5 and ADDENDUM 1 (A1.5 to A1.10) and ADDENDUM 2 whole; 04 §3.8 and §3.9; 03 §9.4; 06 Revision notes, §1, §2 (with 2.8), §8, §9, §10; `05_kam-rulings-2026-11-17.md`. In part: `src/header.rs` (first 60 lines), the test files by search for the functions and assertions named in 4.3, `docs/ROSTER.md` and `crates/coagent-roster/src/lib.rs` on m3-roster by search for the bounds, `crates/coagent-proto/src/canonical.rs` lines 20-32. Not read: `src/redact.rs`, `src/tiers.rs`, `src/domain.rs`, `src/time.rs`, the round-1 and round-2 gate test files beyond the lines found by search, the mutation drivers.
