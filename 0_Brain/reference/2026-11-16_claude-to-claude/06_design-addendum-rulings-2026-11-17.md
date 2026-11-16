---
date: 2026-11-17
type: reference
source: architecture agent commissioned by Friday; inputs are 05_kam-rulings-2026-11-17.md, 03/04 design files, code on main 18005d6, the five STATUS files
status: live (design addendum for the owner's review; nothing built, no code run)
project: General / CoAgent (no client)
---

# CoAgent: design addendum applying the owner's rulings of 2026-11-17

**Revises:** `04_design-revision-rulings.md` (cited **[04 §n]**) and, through it, `03_architecture-design.md` (**[03 §n]**). Neither file is edited. Where this addendum and [04] differ, this addendum wins.

**How to read the labels.**

- **[main: file:line]** means I read that line in the checkout of `coagent/2_Project_Files` on 2026-11-17. `git rev-parse HEAD main` both returned `18005d63ae1311df9649893060caf1f98510a4c1`, and `git diff --stat main` over `crates docs scripts BACKLOG.md Cargo.toml` was empty, so the files read are main.
- **[branch m1-daemon: …]**, **[branch m3-audit: …]** mean read with `git grep` on that local branch. Those branches are IN FLIGHT and unmerged; nothing here treats them as merged.
- **[STATUS …]** means the named section of a seat's report in `coagent/5_Project_History/`. A STATUS line is the seat's claim, not my measurement.
- **[inferred]** is my reasoning. **REASONED, NOT TESTED** marks a security argument of mine that no test or gate has attacked yet.
- **PROPOSED** marks a constant I chose. None is measured.
- **INTERPRETATION (for Kam)** marks every place where his words left a choice and I made it. Each gives the alternative in plain language. All are collected in section 10.
- The owner's words are quoted from `05_kam-rulings-2026-11-17.md`. Friday's READINGS in that file are named as hers.

**One word.** "The starter" is the person who started the session: the *convener* of [04 §3.4] and the `convener` field in the code. I use the owner's word.

Nothing below was measured. No project code was run.

---

## 1. n1: a session holds at most 4 people

**His words.** Card n1-people-limit, option b: "A smaller limit, such as 4". No note.

**INTERPRETATION (for Kam) I-1.** The limit is exactly 4, fixed in the code, the starter and observers included. Alternative: 4 as the normal limit with a setting that lets a starter raise it to 8. I chose the fixed number because he picked the smaller-limit option and gave one example, and because every derived figure below is then one number, not a range. (Friday's READING in the rulings file is the same.)

### 1.1 What changes, by crate

| Where | On main now | New rule | Who changes it |
|---|---|---|---|
| `coagent-roster` | `pub const CAP: u8 = 8` [main: crates/coagent-roster/src/lib.rs:34]; the validator refuses `b.cap != CAP` or more members than `CAP` [lib.rs:311]; slots must be `< b.cap` [lib.rs:334] | `CAP = 4`. The `cap` field of a roster must equal 4 exactly (the existing "equal, not at most" rule stays; [STATUS_M1_CORE §6 DQ4] called this "a one-constant change"). Slots are `0..4`. | ROSTER lane (today) |
| `coagent-roster` tests | `test7_ninth_member_is_refused` builds 9 identities and uses slot 8 [main: crates/coagent-roster/tests/roster.rs:133-154]; another test adds a fifth member in slot 4 [roster.rs:100] | The cap test becomes "a fifth member is refused" (member in slot 4 with `cap` unchanged, and with `cap` raised to 5). Tests that need five or more members are rebuilt with four. The row for the cap test in `scripts/red-controls-core.sh` (line 29) is renamed with it. | ROSTER lane |
| `coagent-relay` | `MAX_SLOTS: u8 = 8` [main: crates/coagent-relay/src/limits.rs:15]; `SLOTS` is derived from it [frame.rs:23]; `chan.create` accepts `cap` in `2..=SLOTS` [frame.rs:351]; a channel holds `[Option<SlotEntry>; SLOTS]` [state.rs:176] | `MAX_SLOTS = 4` so the relay refuses a slot number of 4 or more and a `cap` above 4. This is a courtesy limit: [04 §3.8] says the relay enforces the cap "as a courtesy" and every daemon enforces it "as the rule". A relay still at 8 does not weaken a 4-person session. | N1-PASS lane (later; see 1.3) |
| `coagent-relay` limits text | `OUT_QUEUE_BYTES` doc says "at least 7 x PAIR_MAX_BYTES" [limits.rs:78-80]; two `validate()` error strings say "* 7" while the code uses `SLOTS - 1` [limits.rs:199-206] | The words follow the constant: "(SLOTS - 1)". No behaviour change beyond the constant. | N1-PASS lane |
| `coagent-audit` (in flight) | "one peer may use at most 1/7 of the peers' part" [branch m3-audit: crates/coagent-audit/src/session.rs:13]; [STATUS_M3_AUDIT A2.7 Q19] gives the default as "each peer 1/7 of the rest (6 MiB)" | The divisor is `CAP - 1 = 3`, taken from the roster constant, not typed as a number. Each other member's share of the store grows from one seventh to one third of the peers' part. | AUDIT follow-up after its merge (N1-PASS lane) |
| `coagent-daemon` (in flight) | imports `CAP` from the roster crate [branch m1-daemon: crates/coagent-daemon/src/engine.rs:42]; builds two-member rosters only [engine.rs:1761-1769] | No code change expected from the constant alone: UNKNOWN until its tests are run against `CAP = 4`. Closed by running `scripts/check.sh` on a tree with both merged. | N1-PASS lane |
| Docs | "cap 8" in the roster README [main: crates/coagent-roster/README.md:7], the roster module doc [lib.rs:10], `docs/CRYPTO-GLUE.md` G-15 ("`cap` must be 8 and members ≤ 8") | Say 4 and cite ruling n1. `docs/M0-OUTCOMES.md` line 53 records a measurement taken at 8 members: it is a record and is not rewritten. | ROSTER lane (its own README and module doc); N1-PASS for the shared docs |

### 1.2 What is derived from the limit (N = 4)

All figures are arithmetic from [04 §3.2, §3.8], not measurements.

| Quantity | Formula | At 8 | At 4 |
|---|---|---|---|
| Pairwise channels in a session | N(N−1)/2 | 28 | 6 |
| Ordered pairs the relay buffers for | N(N−1) | 56 | 12 |
| Encryptions per message sent to everyone | N−1 | 7 | 3 |
| Largest replay to one client on attach | (N−1) × `PAIR_MAX_BYTES` (2 MiB) | 14 MiB | 6 MiB |
| Worst-case buffered bytes for one channel | N(N−1) × 2 MiB, capped at `CHANNEL_MAX_BYTES` (64 MiB) | 64 MiB (cap binds) | 24 MiB (cap no longer binds) |
| Audit store share per other member | 1/(N−1) of the peers' part | 1/7 | 1/3 |
| Entries a device can see claiming to be one person at once, when the starter is hostile | N−2 | 6 | 2 (used in section 5) |

**Per-address relay limits.** `MAX_CONNS_PER_IP = 16`, `MAX_CHANNELS_PER_IP = 16`, `MAX_MAILBOXES_PER_IP = 8` [main: limits.rs:36-46]. No comment at source derives them from the group size, so I leave them unchanged. Consequence at 4 [inferred]: behind one address (a tunnel), 16 connections now carry four full sessions where they carried two. The open relay decisions R2 (cut versus throttle) and G1-r2a/b (table filled from four addresses; tunnel totals) are not answered by n1 and stay open (section 9).

### 1.3 Plan and tests that assumed 8

- [04 §4.6] "Group tests run 3 and 8 daemons" becomes 3 and 4.
- [04 §7.1] M3 acceptance "Three-party and eight-party sessions" becomes three-party and four-party. The M6 soak was already four members.
- Spike G2 measured at 8 members [main: docs/M0-OUTCOMES.md:53]; a limit of 4 is inside what was measured. No new spike.
- The relay's gate test files may use slots 4 to 7 as valid slots. UNKNOWN: I did not read every gate test. This is why the relay constant is not changed today: a seat does not edit a gate's test without Friday's ruling, and the relay staying at 8 is harmless (1.1). The N1-PASS lane carries it with marked edits.

**Threat considered.** A smaller room is strictly less exposure: fewer members whose text can reach a host's agent ([04 §3.7] row H) and fewer entries a hostile starter can use for the verify-words attack (section 5). The one risk is the two constants drifting apart (roster 4, relay 8, or a later change to one only). Rule: the first crate that depends on both `coagent-roster` and `coagent-relay` (the daemon) carries a test asserting `coagent_roster::CAP as usize == coagent_relay::frame::SLOTS`. The relay must not depend on the roster crate ([main: crates/coagent-relay/Cargo.toml] comment and the hygiene test), so the equality cannot be a shared constant.

---

## 2. n2: any member may propose a newcomer; the starter grants permission

**His words.** Card n2-who-admits, option b: "Any member may invite", with the note: "but permission must be granted by the person who initiated."

**The design in one paragraph.** The roster keeps ONE admitting authority: only the starter's key signs a roster version, exactly as on main [main: lib.rs:304-309, 595]. What is new is a **proposal**: a member pairs with the newcomer, signs a statement "I propose this device key for this session at this roster version", and sends it to the starter. The starter's human approves or declines in a dialog on the starter's own machine. On approval the starter signs the next roster version; the new entry carries the proposer's signature, so every member can check who proposed whom and the starter cannot attribute a newcomer to a member who did not propose them. Each machine's owner still accepts the newcomer separately before anything is shared ([04 §3.4] rule 2, unchanged).

### 2.1 Interpretations in this section

- **INTERPRETATION (for Kam) I-2.** "Invite" means the member hands out the invite and pairs with the newcomer themselves (code or link, verify-words with the member). Alternative: the member only *asks* the starter to invite someone, and the starter issues the invite and pairs as today. The alternative is smaller and keeps every newcomer verified directly by the starter; I did not choose it because it is the option he did not pick (option a) with a request button added.
- **INTERPRETATION (for Kam) I-3.** Observers cannot propose. "Any member" is read as any member who can already address agents (the starter and guests). Alternative: observers may propose too. I chose the narrower reading because [04 §3.6] gives observers no act that changes the session.
- **INTERPRETATION (for Kam) I-4.** "Permission must be granted by the person" means a human act on the starter's machine, every time: no rule, no grant and no agent can approve a proposal. Alternative: the starter may pre-approve ("accept anyone Priya proposes for the next hour").
- **INTERPRETATION (for Kam) I-5.** If the starter has left, nobody can be added: the member list is frozen, as [04 §3.5] and [04 §10 assumption 6] already say. Alternative: the starter can name a deputy who may approve. A deputy is a second signer and removes the single-writer property that orders roster versions without a server; [04 §7.1] already lists hand-over under M8.
- **INTERPRETATION (for Kam) I-6.** A member cannot propose someone the starter has removed. Only the starter can bring a removed key back, directly. Alternative: allow it and show "previously removed" on the approval card.
- **INTERPRETATION (for Kam) I-7.** The starter may admit a proposed newcomer as an observer even when the proposal said guest (a downgrade), never the reverse. Alternative: the starter must admit exactly as proposed or decline.

### 2.2 What the humans do

1. Priya (a guest) chooses *Invite someone*, picks guest or observer, and gets a single-use invite as today ([04 §3.5] step 2, now issued by a member).
2. Sam joins with it. Sam and Priya pair exactly as two parties do on main (PAKE or link secret, Noise `XXpsk3`, key confirmation, three verify-words) [STATUS_M1_CORE §2 crypto items 3-4]. Sam's screen says: "Paired with Priya. Waiting for Kam, who started this session, to approve."
3. Priya's daemon sends the proposal to Kam. Kam sees a card: "Priya proposes to add Sam as a guest. Key: <fingerprint words>. You have not verified Sam. [Approve] [Approve as observer] [Decline] [Decline and stop proposals from Priya]".
4. Kam approves. His daemon signs the next roster version with Sam's entry. Every member receives it over the pairwise channels, as for any roster update.
5. Priya's daemon hands Sam the signed roster and Sam's relay slot token over their pairing channel. Sam attaches and opens pairwise channels to every member from the roster keys (Noise `KK`), including Kam.
6. Every member, Kam included, sees "Sam (guest), proposed by Priya, approved by Kam. You have not verified Sam. Share with Sam: [nothing] [summaries] [full] · [Verify Sam…]". Share level starts at nothing ([04 §3.4] rule 2). Every active grant in the session is suspended by the roster change ([04 §3.6], unchanged).

The starter's own direct invite ([04 §3.5] steps 2-4) stays as it is.

### 2.3 Wire format

**Proposal body** (canonical encoding of `coagent-proto`, which refuses more than 65,535 bytes [main: crates/coagent-proto/src/canonical.rs:25]):

```jsonc
{ "session_id": "…",
  "proposal_id": "<16 random bytes, lowercase hex>",
  "proposer": "<key id>",
  "at_version": 4,                  // the roster version the proposer holds
  "at_hash": "<hash of that version>",
  "candidate": { "key_id": "…", "noise_static": "…", "sign_pub": "…", "binding_sig": "…" },
  "role": "guest" | "observer" }
```

**Signature.** The proposer's Ed25519 device signing key over the canonical body, under a domain of its own: label `coagent-roster-proposal-v1`. On main, `SignDomain` has only `Binding` and `Roster` [main: crates/coagent-crypto/src/identity.rs:29-43], and the in-flight audit branch edits that same file [branch m3-audit: `git diff --name-only main...m3-audit` lists `crates/coagent-crypto/src/identity.rs`]. So until the audit branch has merged, the roster crate signs a proposal as `sign(SignDomain::Roster, "coagent-roster-proposal-v1" ‖ 0x00 ‖ canonical(body))`. Why that is safe [inferred; the ROSTER lane must test both directions]: a roster signature is checked only over bytes that are a canonical roster body, which begins with `{`; a proposal's signed bytes begin with the label, so neither can be taken for the other, and the proposal verifier requires the label prefix. The audit seat used the same nesting pattern before its own domain values were added [STATUS_M3_AUDIT §6 REQUEST 1]. A real `SignDomain::Proposal` is a REQUEST to the crypto crate for after the audit merge; the signed bytes change when it lands, which is acceptable because nothing is released.

**Roster entry.** `Member` gains one optional field. Entries invited by the starter directly omit it, so they encode byte-for-byte as they do today and every existing roster, hash and signature stays valid:

```jsonc
"proposal": { "proposal_id": "…", "proposer": "<key id>", "at_version": 4, "at_hash": "…",
              "role": "guest" | "observer",        // the role as PROPOSED (the entry's own role may be lower, I-7)
              "sig": "<proposer's signature>" }
```

The body the proposer signed is rebuilt from the roster's `session_id`, the entry's four key fields and these fields, so no second copy of the candidate's keys is stored. `RosterBody` gains no field: both in-flight crates build it with a struct literal [branch m1-daemon: engine.rs:1761] [branch m3-audit: crates/coagent-audit/tests/common/mod.rs:66], and `Member::new` keeps its six arguments because both call it [engine.rs:1768] [tests/common/mod.rs:42].

**Messages** (application envelopes, audit-class):

| Type | Sender | Body | Rule at the decoder (in `admit`) |
|---|---|---|---|
| `member.propose` | a guest | `{ "proposal": <signed proposal>, "note": "<display only, ≤ 256 bytes>" }` | Refused from an observer (I-3). Accepted only by the starter's daemon; any other receiver drops it. |
| `member.propose.result` | starter only | `{ "proposal_id", "result": "approved" \| "declined" \| "expired" \| "stale" \| "refused", "slot_token": "<only when approved>" }` | Refused unless the channel's sender is the starter, the same rule as `roster.update` [main: lib.rs:595]. |

The decline carries no reason text. The `note` is not signed and is never stored in the roster; it is shown escaped, as peer text.

### 2.4 Rules the validator adds (every member's daemon, every version)

Each is a distinct error and a distinct test.

1. **Shape (one version alone).** A `proposal` is refused if `proposer` is the entry's own key, if `proposer` is the starter, if `at_version` is not `added_in − 1`, or if the entry's role is guest while the proposed role was observer (I-7).
2. **Transition (the version that adds the entry).** For each newly added entry with a `proposal`: the proposer is a member of the previous version with role guest; `at_version` and `at_hash` are the previous version's number and hash; the signature verifies under the proposer's signing key as listed in the previous version; the candidate's key id is not on the previous version's `removed` list (I-6); no two entries of the new version share a `proposal_id`.
3. **First roster a joiner holds.** A joiner cannot check history from before it joined (existing rule; [STATUS_M1_CORE §6 DQ15]). For entries added earlier, the signature is checked when the proposer is still a member (a member's keys cannot change, [main: lib.rs:525-533]); when the proposer has since been removed, the entry is accepted and reported through an accessor as "proposal not checkable". The joiner's own entry is always checkable by the daemon: it must name the proposer the joiner actually paired with.
4. **Lifetime bound.** A version is refused if `members + removed` exceeds `MAX_ENTRIES_EVER = 16` (PROPOSED: four times the limit). On main the `removed` list grows without a bound of its own [main: lib.rs:354-371 has no length check]; it is stored input a peer (the starter) causes, so it gets a bound now. An honest session that reaches it must start a new session.

### 2.5 The starter's side: one state machine

Pure logic, no clock read (time is passed in), in the roster crate so every daemon and the tests share it.

A proposal arriving from channel-authenticated sender S is checked in this order; the first failure decides and the human is shown nothing for any refusal:

1. encoded size within the bound; decodes canonically;
2. `session_id` is this session; `proposer` equals S (the channel's key, never a field's claim);
3. S is on the current roster with role guest;
4. `at_version` and `at_hash` equal the current version (else `stale`: the proposer must propose again against the roster as it is now);
5. the proposal signature verifies;
6. the candidate's keys verify and its key id matches them (`verify_device`, as the validator does for members [main: lib.rs:325-329]);
7. the candidate is not a current member and not on the `removed` list;
8. there is a free seat and the lifetime bound is not reached;
9. S has no other pending proposal, has not used its session quota, and is not muted;
10. the `proposal_id` has not been seen.

Then the proposal is **pending** until the human decides or `PROPOSAL_TTL` passes. Outcomes: approved (the next roster version is built and signed), declined, expired, or stale (any roster change voids every pending proposal, because rule 4 can no longer hold).

**Bounds (PROPOSED).**

| Input a peer causes | Bound | On overflow |
|---|---|---|
| Pending proposals per proposer | 1 | refused, no card |
| Pending proposals per session | 3 (`CAP − 1`) | refused, no card |
| Proposals per proposer per session, any outcome | 8 | refused, no card, for the rest of the session |
| Remembered `proposal_id`s per session | 15 × 8 = 120 (at most 15 entries other than the starter can ever exist under the lifetime bound of 2.4, each with a quota of 8) | cannot overflow |
| `note` | 256 bytes | proposal refused |
| Encoded proposal | 2,048 bytes | refused before decoding |
| Life of a pending proposal | `PROPOSAL_TTL` = 10 minutes (the pairing mailbox's life, a design value [main: limits.rs:25]) | expires; proposer is told |

### 2.6 Threats considered

| Attempt | By | Result |
|---|---|---|
| Forge a proposal | relay | Cannot: proposals travel inside pairwise channels and carry the proposer's signature. |
| Drop or delay proposals or results | relay | Denial of service only, and visible: the proposal expires on the proposer's side and the newcomer keeps seeing "waiting". |
| Replay an old proposal | relay or member | Refused: it names a roster version and hash that are no longer current; the channel's sequence numbers refuse a replayed frame first [STATUS_M1_CORE §3 test 8]. |
| Flood the starter with approval cards | hostile member | One pending card per proposer, eight per session each, then silence; "Decline and stop proposals" mutes at once. Approval fatigue is the real risk and is the reason for I-4. |
| Propose a removed person | hostile member | Refused before any card (I-6). |
| Propose a second device of their own as a "new person" | hostile member | The starter's human decides; admission gives no access until each owner accepts ([04 §3.4] rule 2). Same residue as [04 §3.7] row I. |
| Lie about the newcomer's key (sit between the newcomer and the group) | hostile proposer | Fails without the starter's help: the newcomer's daemon refuses a first roster that does not list its own key [main: lib.rs:427-429], and a roster needs the starter's signature. |
| Hand the newcomer a fake session (a made-up "starter" key and a roster signed by it) | hostile proposer | Possible, and equal to the proposer inviting the newcomer into a session of the proposer's own. No real member is in it. The newcomer's screen says the starter is "introduced by Priya, not verified by you" until they verify. This is [04 §3.7] R10 with the proposer in the introducer's seat. |
| Attribute a newcomer to a member who did not propose them | hostile starter | Refused by every member's validator: the entry's proposal signature does not verify. |
| Admit someone without any proposal | hostile starter | Always possible; that is the starter's direct invite. The entry then shows no proposer. |
| Propose "the same person" again under a fresh key so the verify-words tries start over | hostile member with a careless or colluding starter | Closed by the inheritance rule of section 5.2 (c), which treats every newcomer after a removal as possibly the removed person. |

**If the starter is offline.** The proposal waits in the proposer's outbox like any message [03 §4.5] and expires after `PROPOSAL_TTL`; the proposer may propose again (it counts against the quota only when the starter's daemon received it). **If the starter is gone** (sent `session.leave`, or the session ended for their absence), the proposer's daemon refuses to create a proposal and says: "The person who started this session has left. Nobody can be added. Start a new session." (I-5.)

### 2.7 What changes in [04]

- [04 §3.4] authority matrix: the row "Admit or remove a member; change guest ↔ observer" stays starter-only. A new row: "Propose a new member: guest yes; observer no; starter invites directly".
- [04 §3.5] step 2 gains the member-issued invite. "The convener's key is the only valid signer" is unchanged.
- [04 §3.8] gains the two message types of 2.3.
- [04 §3.5] identity provenance gains nothing: a proposed member is `introduced_by:<proposer key id>` for everyone but the proposer, who holds `by_code_with_me`.
- [04 §9] N2's default (a) is replaced by this section.

---

## 3. n5: optional third-party connection servers, chosen by the user when connecting

**His words.** Card n5-rendezvous, option b: "Yes, as an option the user switches on". Follow-up line: "ask the user which option they choose when they try to initiate a connection. Gide them through ever which option they choose".

### 3.1 What the product asks

When a user starts a connection (issues an invite as starter or as proposing member), before any invite exists:

> How will the other person reach you?
> 1. **We are on the same network** (office, home, the same VPN or tailnet). Nothing leaves your network.
> 2. **I will open a way in myself** (a tunnel I already run, or a port I forward on my router).
> 3. **Through a relay I or my team run** (a saved relay profile).
> 4. **Through third-party connection servers** (not run by you or by this project).

Each choice leads to a short guided path that ends in an invite, and each path shows its disclosure line (3.3) before the invite is created. Paths 1 to 3 are [04 §4.2] options A1, A2/A3 and B with [04 §4.3] relay profiles; `coagent doctor net` on main already reports what can be known locally [STATUS_M1_RELAY "What exists", coagent-cli]. Path 4 is new and is specified only as far as 3.4 allows.

- **INTERPRETATION (for Kam) I-8.** The question is asked every time a connection is started. The last answer is highlighted, never applied silently. Alternative: ask once, remember, and ask again only from settings. I chose every time because his line says "when they try to initiate a connection" and because path 4 exposes other people's addresses.
- **INTERPRETATION (for Kam) I-9.** The joiner is asked too. An invite that uses path 4 says so, and the joiner's side shows "This invitation connects through <operator>'s servers. They will see your internet address and when you are connected. They cannot read what is sent. [Continue] [Ask for another way]" before it dials anything. Alternative: only the person starting the connection chooses. I chose to ask both because the starter's opt-in would otherwise disclose the joiner's address without the joiner's knowledge.
- **INTERPRETATION (for Kam) I-10.** The guided question with paths 1 to 3 is part of the one beta (n8). Path 4 is listed in the question from the start but stays marked "not available yet" until a mechanism is chosen (3.4). Alternative: hide path 4 until it works. [04 §9] N5 asked about "a later version", so I do not assume path 4 must work in the first beta; that is for him to say.

### 3.2 What stays self-hosted by default

Everything. No candidate of the third-party kind is ever generated, saved in a relay profile, stored with a contact, or tried by a client unless the local user chose or accepted path 4 for that connection. There is no fallback from a failed path 1 to 3 into path 4. The project still operates no server of any kind ([04 §4] BLUF stands).

**Rule for later crates.** An invite's relay candidate gains a `kind`: `self` (paths 1 to 3) or `third_party:<mechanism id>`. A client that meets a `third_party` candidate without a recorded local consent for this connection skips it and reports why. The candidate list on main is `{url, pin}` pairs tried in order [STATUS_M1_RELAY "What exists": `connect_candidates(&[Candidate], …)`]; the `kind` lives in the invite (the in-flight daemon's `invite` module [STATUS_M1_DAEMON §1 item 5]), not in the relay client.

### 3.3 What each path discloses, and to whom

Grounded in [04 §3.7] row N, [04 §4.2] and [04 §4.4]. In every path the relay layer cannot read content; content is protected by the pairwise channels.

| Path | Who operates the meeting point | What that operator sees | What the other participants see |
|---|---|---|---|
| 1. Same network | The person hosting the relay (a participant) | Every participant's address on that network, who talks to whom, sizes and timing | The host's private address, in the invite |
| 2. Own tunnel or forwarded port | The host, plus the tunnel provider if one is used | Host: as path 1, with public addresses unless the tunnel hides them. Tunnel provider: the relay's metadata ([04 §4.2] A2: it "terminates or carries the connection and sees relay metadata") | The tunnel name or the host's public address, in the invite |
| 3. Own or team relay | Whoever runs that relay | Every participant's public address, the traffic graph, sizes and timing | The relay's address, in the invite |
| 4. Third-party servers | A third party | UNVERIFIED per mechanism. At least what any relay sees: every participant's public address and connection timing. Whether it also learns a stable identifier for each device depends on the mechanism (3.4). | Depends on the mechanism |

### 3.4 Which third-party mechanism: UNDECIDED

I cannot ground a recommendation in the files I was given.

- The design names one candidate: iroh, which "establishes direct connections whenever possible, falling back to relay servers if necessary" and offers "Shared, Dedicated, or self-hosted relays" [04 §4.2 option C]. But "who operates them and on what terms was not on the page read today" [04 §4.2], listed as unverified item C-d [04 §8]. The prior-art file adds that iroh is at a stable 1.x with a permissive licence and that its hole-punch success figure is from secondary coverage and unverified [02 §D.4]. Neither file states the operator, the terms, the rate limits, or what the shared servers learn about a device.
- The other candidates in the files are tunnels the user runs (Tailscale Funnel, a Cloudflare quick tunnel) [04 §4.2 A2]. Those are path 2, not path 4: the user installs and runs them, and CoAgent never downloads or manages a tunnel program [04 §4.2, finding S11]. Whether the relay's WebSocket connections pass through them is unverified item C-a, and spike C2 has not been run [STATUS_M1_RELAY "NOT done": "spikes C2/C3 still not run"].
- WebRTC with public STUN servers was "not researched from a primary source" [02 §D.4].

**What would decide it.** (1) Reading iroh's documentation in full for: who operates the shared relays and discovery service, the terms of use, the limits, whether discovery can be switched off, and what identifier the servers see (item C-d). (2) A decision on shape that depends on (1): whether a third-party transport carries the existing relay protocol to the host's embedded relay (reachability only; the relay code and the pairwise channels stay as they are), or replaces the relay path for that session. I lean to the first [inferred] because it adds no second message path to test, but I have not verified that the library allows it. (3) Spike C2, which settles whether path 2 already covers most cross-network cases without any third party. Until (1) is done, path 4 stays "not available yet" and no code depends on a mechanism.

**Threat considered.** A dependency on servers nobody in the session controls: availability (the session cannot start when they are down), metadata (addresses and timing of every participant go to a party outside the session), and silent drift (terms change). The first two are disclosed at the question; the third is why the mechanism id is recorded in the invite and in the audit log's session record, so a user can later see which sessions used which operator.

---

## 4. The relay may keep a saved identity, behind a deliberate option

**His words.** Card relay-identity-restart, option b: "Allow a saved identity, switched on deliberately". No note. The rulings file's consequence line: "default stays a fresh identity per start".

### 4.1 What is on main

- The relay's TLS identity is a self-generated certificate; the invite's pin is the SHA-256 of the certificate's DER bytes [main: crates/coagent-relay/src/tls.rs:34-35, 104].
- The client accepts exactly the pinned certificate; there is no CA, name or expiry check, and the TLS handshake signature is still verified against the pinned certificate's key [tls.rs:1-5, 136-162].
- `TlsIdentity::generate` is the only constructor; the key is held in memory [tls.rs:71-75, 88-110].
- `RelayConfig` already has `identity: Option<TlsIdentity>`, and `Relay::start` generates one only when it is `None` [main: crates/coagent-relay/src/server.rs:95-96, 187-197].
- `coagent relay` has three options, `--listen`, `--allow-non-loopback`, `--status-secs` [main: crates/coagent-cli/src/args.rs:8], builds its config from `RelayConfig::loopback()` without setting `identity` [relay_cmd.rs:92-96], and its module doc says it "Creates no files" [relay_cmd.rs:2]; a test asserts the working directory stays empty [main: crates/coagent-cli/tests/cli.rs:202].
- So today a pin is valid for one run [STATUS_M1_RELAY DQ11], and after a relay restart a joiner needs a new line pasted out of band [STATUS_M1_DAEMON §4 items 9-10].

### 4.2 The new rule

**Default, unchanged.** With no identity option, `coagent relay` generates a fresh identity, opens no file, and prints exactly the lines it prints today.

**Option A, saved to a file the user names:** `coagent relay --identity-file <path>`.

- If the file does not exist: generate an identity, write it, and print `identity: saved, created <path>`.
- If it exists: load it and print `identity: saved, loaded <path>`. The fingerprint line is then the same on every start.
- Storage rules, all fail closed, none repaired silently:
  - the parent directory must exist, belong to the current user and have no group or other permission bits (0700);
  - the file is created exclusively (never over an existing file), mode 0600, written to a temporary name in the same directory and renamed;
  - on load the path must be a regular file, not a symbolic link, owned by the current user, mode 0600 exactly in its group and other bits (none set), and at most 16 KiB (PROPOSED); the size is checked before reading;
  - the program never changes a mode or an owner to make a check pass;
  - the key never appears in any output, log line, error text or `Debug` form (the existing `Debug` already redacts it [tls.rs:78-82]).
- What is stored: the exact certificate DER bytes and the PKCS#8 key bytes, behind a magic line and a version. The certificate itself must be stored, not only the key: the pin is a hash of the certificate, and a certificate regenerated from the same key has different bytes [inferred from tls.rs:100-104: the fingerprint is taken over the DER that `self_signed` returns].
- A stored identity whose key does not belong to its certificate is refused before the relay listens.
- On Windows the option is refused with a plain message until the permission checks have been written and run there (Windows is untested until the owner is at the machine, section 7).

**Option B, handed in by the parent process:** `coagent relay --identity-stdin`. The relay reads one identity blob (the same format, the same 16 KiB cap) from standard input, with a deadline, and opens no file. It prints `identity: supplied on standard input`. This is the daemon's REQUEST 1 as written: "start `coagent relay` with a given TLS identity (e.g. key on stdin or an inherited fd)" [STATUS_M1_DAEMON §5 R1]. It keeps the rule that the relay child has no access to the daemon's data directory ([04 §4.4]; [STATUS_M1_DAEMON §2 test 9]): the daemon, not the relay, reads and writes the stored identity. The relay's TLS key is not a secret that protects content, so the daemon holding it does not weaken [04 §4.4], whose rule is the other direction (the relay must not reach the daemon's keys).

The two options are mutually exclusive. The in-flight daemon reads the relay's banner by the prefixes `url: ` and `fingerprint: ` [branch m1-daemon: crates/coagent-daemon/src/relay_child.rs:99-101], so those lines keep their exact form and the new `identity:` line is printed only when an identity option is given.

- **INTERPRETATION (for Kam) I-11.** "Switched on deliberately" also covers the relay that the starter's own daemon runs for a session: the daemon stores and re-supplies an identity only when the user has turned a setting on; otherwise a restarted relay child gets a fresh identity and the joiner needs a new line, as today. Alternative: within ONE session the daemon always re-supplies the same identity to a restarted child (kept in memory only, never on disk), and only keeping it ACROSS sessions needs the setting. The alternative removes the commonest break (a relay child crash mid-session) at no storage cost, but it is not what "default: fresh per start" says literally, so I did not assume it.

### 4.3 How a joiner's pin behaves across restarts

| Case | Relay restarts with | Joiner's stored candidate | What the joiner sees |
|---|---|---|---|
| Default | a fresh identity | pin no longer matches | Connection refused in the TLS handshake, reported as a pin mismatch (the client flags it separately from other failures [tls.rs:156-160]). The host must send a new link or line. Fixed text for this case: "The relay's identity changed. That happens when the host restarted it without a saved identity. It also happens when something is impersonating the relay. Ask the host for a new invitation; do not retry." |
| Saved identity, same address | the same identity | pin matches | Reconnects with no human step. |
| Saved identity, address changed | the same identity | pin matches, address does not | Still needs the new address out of band. A saved identity fixes the pin, not the address: a relay started on an ephemeral port gets a new port. A host that wants a restart to be invisible must also fix `--listen`. |

A new address or pin that arrives out of band should be signed by the starter so the joiner's daemon can accept it without trusting the channel it came through. That needs a signing domain in the crypto crate, which is the daemon's REQUEST 7 [STATUS_M1_DAEMON A1.9 R7]; it stays a REQUEST for the crypto follow-up lane and is not part of this ruling.

### 4.4 Threats considered

- **The file is stolen.** The thief can present the relay's certificate to joiners and so sit where the relay sits: addresses, traffic graph, sizes, timing, and the power to drop traffic. Not content, and not pairing (the pairing secret is in the invite, never sent to the relay [03 §4.2]). This is why the option is off by default and why the file rules are strict.
- **A long-lived fingerprint is a tracking identifier.** Anyone who has seen two invites from the same saved relay can tell they are the same relay. The help text says so.
- **A wrong pin trains people to click through.** The relay seat's gate raised this as N8 [STATUS_M1_RELAY ADDENDUM 1 §4]. The saved identity removes the benign cause for long-lived relays; the fixed text above tells the user not to retry in the default case.
- **A typo in the path silently creates a new identity.** The `created` versus `loaded` line makes it visible; there is no other defence.

---

## 5. Verify-words: three tries each side, and what the bound is

**His words.** Card verify-words-tries, option a: "Keep three tries each side". The rulings file's consequence: "the bound of five guesses per pair per session is accepted and documented".

### 5.1 The accepted bound, stated exactly

`MAX_ATTEMPTS = 3` ceremonies per pair, per side [main: crates/coagent-crypto/src/sas.rs:55]. One comparison of words succeeds for an attacker with probability 2^-31 (three words from a 1,296-word list). A middleman who is the committer on both channels compares the two sides' words before either human sees anything and abandons every ceremony that would not match, so no mismatch is ever displayed; each comparison costs a counted ceremony on one side only. That gives 2 × 3 − 1 = 5 independent comparisons: **at most 5 × 2^-31 (about 1 in 430 million) per pair of roster entries per session** [main: sas.rs:50-54; docs/CRYPTO-GLUE.md G-14, lines 222-230]. This is the figure the ruling accepts. The product's threat model states 5, not 3. `spikes/G4-…/ANALYSIS.md` still says 3 [STATUS_M1_CORE A2.2 item 7]; the correction belongs to whoever next owns `spikes/`.

### 5.2 The two "unlimited" cases

[STATUS_M1_CORE A2.4 item 2] names two ways the count stops being bounded. Neither was ruled on by name; closing them is what makes the accepted sentence true.

**(a) A daemon restart resets the count** (counts live in memory on main [main: BACKLOG.md lines 91-93]). **Closed by persistence.** The daemon stores, per (session, slot), attempts used, every word triple shown, and hard stops, and loads them before it accepts any channel. The in-flight daemon reports having built this, with a test that kills the daemon mid-ceremony and red controls on the stored cap [STATUS_M1_DAEMON §1 item 13, §2 test 6, A1.7 `no_persisted_cap`]. That branch is unmerged; this addendum only fixes the rule. The crypto crate offers no way to load a stored count into `ChannelMap`, so the daemon keeps a parallel count [STATUS_M1_DAEMON §5 R2]; R2 and R3 stay REQUESTS for the crypto follow-up lane.

**(b) The same person re-added under a fresh key gets fresh tries.** Three sub-cases:

1. *Fresh key, same slot.* Closed on main when the caller names the slot: `insert_with_slot` makes a new key in a slot inherit the attempts the slot already used and refuses a slot that hard-stopped [main: crates/coagent-crypto/src/channel_map.rs:128-153]. **Rule:** every channel to a roster member is inserted with its slot. Plain `insert` [channel_map.rs:110] must not be reachable from daemon code. The in-flight daemon says it uses `insert_with_slot` everywhere [STATUS_M1_DAEMON §1 item 12]. Making plain `insert` unreachable in the crate itself means touching tests the two gates wrote [STATUS_M1_CORE A2.4 item 2a], so it needs Friday's ruling and is a REQUEST for the crypto follow-up lane. Until then a source check in the daemon crate (no call to `ChannelMap::insert`) holds the rule.
2. *Fresh key, another slot, after a removal.* Open on main ([main: BACKLOG.md lines 110-112]: "a hostile convener can still re-introduce a person under a fresh key into a NEW slot"). **New rule (inheritance from removed entries):** on each device, an entry added in or after a roster version that removes anyone starts with `attempts_used` equal to the highest count this device used with any entry removed so far in this session; and if this device hard-stopped with any removed entry, every entry added afterwards is refused a channel on this device until its owner deliberately overrides (the existing `verify_override_slot` act [channel_map.rs:155-161]). The daemon applies it, because the daemon sees which keys a version removed and added (`Applied::Advanced { added, removed, .. }` [main: lib.rs:391-399]) and holds the stored counts. REASONED, NOT TESTED. It needs R2 (seeding `ChannelMap`) or the daemon's parallel count.
   - **INTERPRETATION (for Kam) I-12.** This rule makes an honest newcomer pay for a removed member's failed tries: if you failed twice with someone who was then removed, the next person added gets one try with you in that session, and if you had said "the words do not match" about a removed member, you must deliberately override before you can talk to anyone added later. Alternative: do not inherit, and state plainly that a hostile starter gets five more guesses each time they remove and re-add (bounded only by the 16-entry lifetime limit of 2.4). I chose inheritance because the ruling's sentence says "per pair per session" and a re-added person is the same pair to the two humans.
3. *A second entry for the same person while the first stays.* **Documented, not closed.** Keys are the only identity the software has ([03 §4.3]); it cannot know two entries are one person. A hostile starter who is also the relay can show each victim up to `CAP − 2 = 2` entries claiming to be the other (the slots that are neither the victim's nor the starter's). With three tries per entry per side that is 6 tries per side and 6 + 6 − 1 = **11 comparisons, at most 11 × 2^-31 per session** [inferred: the G-14 schedule with a = b = 3 × (CAP − 2); REASONED, NOT TESTED]. It requires both humans to run the ceremony against two members who both claim to be the same person. Mitigation that is not a bound: when two roster entries carry the same claimed display name, every member's screen says so on both chips. The threat model states the 11.

**What a hard stop means for the starter** (the open F2 questions [STATUS_M1_CORE A1.6 item 1]): not ruled. The defaults builders assume are in section 9.

### 5.3 What changes in [04]

[04 §3.5] says "the design claims no protection from the words on introduced pairs" until spike G4 reports. G4 reported and the commit-then-reveal ceremony is on main [docs/CRYPTO-GLUE.md G-14]. The claim the design may now make is the one in 5.1 and 5.2: 5 per pair of entries per session; 11 per session against a hostile starter who lists a person twice; nothing after a deliberate override.

---

## 6. n3 and the terminal-commands ruling: every shell command asks, on every platform

**His words.** Card terminal-commands-gate, option a: "Keep it: every terminal command asks". Card n3-windows-commands, option b: "Only exact commands you tick", then his next line: "for the above, change - same rules as mac".

The policy crate is in flight (addendum 5 builds the rule; [STATUS_M2_POLICY] ADDENDUM 5 and 6 are unreported). This section says only what LATER crates must assume.

- **INTERPRETATION (for Kam) I-13.** "Same rules as mac", read with the terminal-commands ruling, means: on Windows as on the Mac, every shell command asks, and the only exception is the owner's list of exact commands. (This is Friday's READING too.) The other possible meaning is option c of the original card ("same rules as macOS and Linux" for what a trust grant may cover). Today both meanings give the same behaviour, because on the Mac no grant covers a shell command either. They differ only if the Mac rule is ever relaxed: under my reading Windows would follow; given that Windows has no sandbox ([04 §5.4]), that step should come back to him as its own question.

**What later crates must assume.**

1. Every `Bash` and `PowerShell` tool call is the highest-scrutiny class on macOS, Linux and Windows: asked every time, never approved "for the session", never covered by a grant's scope or pattern [policy addendum 5, items 2-3, in Friday's `briefs_drafts`].
2. The one exception is the owner's exact-command list: byte-exact command text, the canonical working directory and the tool. It is filled only by the owner's own input. It is never filled from a click on an approval card, from a peer's proposal, or from a grant document [policy addendum 5 item 3]. The daemon and the console therefore need an owner-only screen for this list, and no message type may carry an entry for it.
3. A listed command is still denied when a deny scan hits [policy addendum 5 item 3].
4. No crate classifies shell text as safe. The PowerShell recogniser and the POSIX simple-command recogniser of [04 §5.5], and the `find`/`grep` forms of spike B16, are not built. A recogniser of safe shell commands is never to be built (Friday's lesson of 2026-11-17).
5. Consequences for [04]: the M2 row of [04 §7.1] loses "PowerShell recogniser; `find`/`grep` forms in the POSIX recogniser". The M5 acceptance line "On Windows a command still asks unless N3 allowed otherwise" becomes "on every platform a command asks unless it is on the owner's exact-command list". "In-scope actions flow" under a grant means file-tool actions only. [04 §5.4]'s first table row (commands never auto-allowed by a grant on native Windows) is now true of every platform. On macOS and Linux, searches arrive as `Bash` calls ([04 §5.1], source S13), so every search asks; that cost was put to him on the terminal-commands card and he kept the rule.

**Threat considered.** The one the two gates demonstrated: text handed to a shell cannot be classified from outside the shell ([STATUS_M2_POLICY] ADDENDUM 3 and 4; the lesson file). The residue is approval fatigue, and a command on the exact list is trusted with everything it does.

---

## 7. n4, n8, n6, n7 and Windows testing: consequences for the plan only

| Ruling | His words | Consequence for the plan |
|---|---|---|
| n4 | Option a "Sign through Microsoft's signing service", note: "yes but lets build the other versions first as I wont be next to the windows machine until the end of the week" | macOS (and Linux) builds come first. Windows signing is set up when he is at the Windows machine. It costs money and needs his identity: his act, never a seat's ([04 §9] N4 is approval-class). No seat creates a signing account or pays for anything. |
| Windows testing | Option a "I will provide a Windows machine or VM", note: "which is better? will a VM be sufficient or is it best to do it on a proper machine. I am travelling and will be next to my windows machine on friday" | Friday answered on the panel: wait for the real machine on Friday 2026-11-20 (her reasoning, not a measurement). Until then every Windows path stays compiler-checked and labelled UNTESTED. Spikes W1 and W3 [04 §7.2] and the pipe identity checks R3 (a)-(c) [STATUS_M1_RELAY ADDENDUM 1 §4] wait for that day and need him present. No lane today owns Windows behaviour. |
| n8 | Option a "One beta with everything" | One beta at M6 carrying groups, observers and native Windows. The private two-party checkpoint that [04 §9] N8 recommended (option b) is not a release. Milestones stay as internal gates. With n1, "everything" means groups of up to 4. |
| n6 | Option a "Open from the first commit" | The repository is to be public, and stays PRIVATE until his card on publication is answered: making it public is his own click, and the pre-publication sweep found recorded spike output carrying material that must not be published (`prepub_sweep_2026-11-17.md`; Friday's lesson on recorded fixtures). Consequence for every seat from today: write every commit as if it were already public. No absolute paths, user names or other projects' names in committed output; recorded fixtures only from a scratch tree. No seat changes a repository setting. |
| n7 | Option a "Approve those obligations" | The disclosure obligations of [04 §6.2] are approved as written. The option text in [04 §9] N7 (a) includes "wording drafted at M6 for sign-off": the text itself is still shown to him before it is published. `coagent --version` already prints "beta (not independently reviewed)" [STATUS_M1_RELAY "What exists"]. |

---

## 8. Bounds table for everything this addendum adds

Every stored or buffered input a peer can cause has a bound from the first version.

| Input | Who causes it | Bound | Where enforced | Status |
|---|---|---|---|---|
| Members in a roster | starter | 4 | roster validator | CAP = 4 (section 1) |
| `removed` list plus members, session lifetime | starter | 16 | roster validator | PROPOSED (2.4) |
| Encoded roster version | starter | 65,535 bytes | canonical decoder [main: canonical.rs:25] | on main |
| Encoded proposal | any guest | 2,048 bytes | starter's proposal intake, before decoding | PROPOSED (2.5) |
| Proposal `note` | any guest | 256 bytes | starter's proposal intake | PROPOSED |
| Pending proposals | guests | 1 per proposer, 3 per session | starter's proposal intake | PROPOSED |
| Proposals per proposer per session | a guest | 8 | starter's proposal intake | PROPOSED |
| Remembered proposal ids | guests | 120 (15 possible proposers × 8) | follows from the quota and the lifetime bound | derived |
| Life of a pending proposal | a guest | 10 minutes | starter's proposal intake (time passed in) | PROPOSED |
| Verify ceremonies | a peer | 3 per entry per side; inherited across slots and removals | crypto crate and daemon (section 5) | 3 is on main; inheritance is new |
| Saved relay identity file / standard-input blob | local user or parent process (not a peer) | 16 KiB, read deadline on standard input | `coagent relay` | PROPOSED (section 4) |

---

## 9. Open design questions from the STATUS files

### 9.1 Answered by this morning's rulings

| Source | Question | Answer |
|---|---|---|
| [04 §9] N1; [STATUS_M1_CORE §6 DQ4] | How many parties; `cap` must equal 8 | 4 (section 1; I-1). |
| [04 §9] N2 | Who may bring a new person in | A member proposes, the starter approves (section 2). |
| [04 §9] N3; [STATUS_M2_POLICY A3.7 item 1, A4.6 item 1] | Commands on Windows; every shell command asks | Same rule everywhere: every command asks, plus the owner's exact list (section 6; I-13). |
| [04 §9] N4 | Sign the Windows binaries | Yes, through Microsoft's service, after the other builds, when he is at the machine. |
| [04 §9] N5 | Third-party rendezvous | Opt-in, asked at connection time, guided (section 3). The mechanism is UNDECIDED. |
| [04 §9] N6 | When the repository becomes public | "Open from the first commit"; in effect after his publication card. |
| [04 §9] N7 | Disclosure obligations | Approved as written. |
| [04 §9] N8 | Release order | One beta with everything. |
| [STATUS_M1_RELAY DQ11, ADDENDUM 1 §4 N8] | Certificate regenerated on every start | Saved identity behind a deliberate option; default fresh (section 4). |
| [STATUS_M1_DAEMON §4 items 9-10, §5 R1] | Relay restart breaks the joiner's pin; relay started with a given identity | Ruled in principle; the mechanism is section 4. Whether the daemon re-supplies an identity within one session by default is I-11. |
| [STATUS_M1_CORE A2.4 item 1] | Accept 5 × 2^-31, lower the cap to 2, or count per human pair | Accept: three tries each side (5.1). |
| [STATUS_M1_CORE A2.4 item 2] | The count is unlimited across restarts and fresh-key re-adds | Answered in part. The ruling accepts a bound "per pair per session"; section 5.2 gives the rules that make it hold. Restart: closed by persistence (in flight). Same slot: closed by mandatory slots. New slot after removal: closed by inheritance (I-12). Second simultaneous entry: documented at 11 × 2^-31. |
| [STATUS_M3_AUDIT A2.8 item 1] | A third check on the audit log | Yes (process ruling; commissioned). |
| [STATUS_M3_AUDIT A2.7 Q19] (the divisor only) | Each peer's share is 1/7 | Becomes 1/(CAP − 1) = 1/3 as a consequence of n1. The sizes themselves stay open (9.2). |

### 9.2 Still open

"Default" is what builders assume until someone rules. Items marked (design) need the design owner's word, not Kam's; items marked (owner) are his.

| Source | Question | Default builders assume |
|---|---|---|
| [STATUS_M1_CORE A1.5; A2.4 item 3] DQ1, 2, 3, 7, 9 and the `decline` step (design) | Wire changes relative to [03]/[04]: key confirmation after Noise; `hello.session_id`; roster as `{body, sig}` with `added_in`; the `SasMsg` record and committer rule; in-band `Rekey`; `SasStep::Decline` | As on main. Both gates passed them; [03]/[04] have not been updated to match. Section 2 builds on the `{body, sig}` shape and `added_in`. |
| [STATUS_M1_CORE A1.6 item 1] F2 (a) (owner) | Should a hard stop make a device distrust the starter's later re-adds in any slot | Yes, through the inheritance rule of 5.2 (I-12). |
| F2 (b) (owner) | Should a hard stop alarm or end the session | Alarm on the device that saw it; the session continues; that device refuses the member. |
| F2 (c) (design) | Should the per-slot path be mandatory | Yes for every roster member (5.2 b.1); enforcing it inside the crypto crate waits for Friday's ruling on the gate tests. |
| [STATUS_M1_CORE A1.5] DQ6, 10, 12, 13, 15 (design) | Hard-stop scope is local only; strict sequence numbers; joiner's `hello` readable by an active attacker at message 2; no `hello` on KK; first roster may be any version | As on main. DQ12 belongs in the published threat model. DQ15 is relied on by 2.4 rule 3. |
| [STATUS_M1_RELAY DQ1-5, 8-10, 12-15] (design) | Relay protocol additions (`chan_id` in `chan.slots`, `ok` replies, extra error codes, per-pair `resume_from`, token sizes, mailbox caps, added relay-wide caps, ping) | As on main and in `PROTOCOL.md`. |
| [STATUS_M1_RELAY DQ6; ADDENDUM 1 §4] (design) | Second attach refused versus replace-on-valid-token | Refused, as on main. |
| [STATUS_M1_RELAY ADDENDUM 1 §4 R2; ADDENDUM 2 §5 G1-r2a, G1-r2b] (owner) | Per-address budgets cut rather than throttle; four addresses fill the channel table; behind a tunnel one relay serves 16 live sessions in total | As on main. The seat's condition stands and n5 makes it bite: no tunnel recipe and no third-party path is presented as supported until these are answered. |
| [STATUS_M1_RELAY ADDENDUM 1 §4 N3] (owner) | Full peer address on every relay log line | Kept on the host's own stderr; to be stated in the disclosure text. |
| [STATUS_M1_RELAY ADDENDUM 1 §4 R3 (a)-(c)] (design, needs Windows) | Named-pipe caller and server identity checks | Not built. Waits for spike W3 on the real machine, 2026-11-20. No Windows build is handed out before it. |
| [STATUS_M1_DAEMON §4 items 1-8] (design) | Pairing context is the pin; fresh KK per attachment; welcome inside the pairing channel; reply is `chat.msg` with `re`; both members guest; verify persistence rules; 16 KiB text limit; one session per daemon | As on the in-flight branch (unmerged; its third check is pending). Section 2.2 step 5 follows item 3: the welcome travels in the pairing channel. |
| [STATUS_M1_DAEMON §5 R2-R5; A1.9 R6, R7] (design) | Seed `ChannelMap` with stored counts; expose `attempts_used`; export `current_uid`; `recv` cancel safety; bind the KK label into the prologue; a signing domain for `relay.moved` | REQUESTS for the crypto and relay follow-up lanes (lane plan). R2 and R7 are named in sections 4 and 5. |
| [STATUS_M1_DAEMON A1.11] G13 (design) | A recorded deviation from [03 §9.1] row A | UNKNOWN to me: I read the heading, not the item. Closed by reading `docs/DAEMON.md` on the branch and the round-2 verdict. |
| [STATUS_M3_AUDIT §5 Q1-3, 5-10, 12-14] (design) | `sig` inside the hashed header; `ts` format; heads carry session, author and roster version; broken-link evidence; gap versus reorder; summaries redacted; receipts; time-based checkpoints; bundle seal; joiner refuses pre-anchor checkpoints; proposed constants; full capture not built | As on the in-flight branch. |
| [STATUS_M3_AUDIT §6 REQUEST 2, 3; A1.7 Q11] (design) | Envelope `sig` doc for audit-class types; `ForkEvidence::verify` in the roster crate | REQUESTS. REQUEST 3 touches the roster crate: it is NOT in today's ROSTER lane (that lane must not widen); it goes to the follow-up. |
| [STATUS_M3_AUDIT A1.7 Q4, Q15-17; A2.7 Q18-20; A2.8 items 2-5] (owner for 2, 3; design for the rest) | Heads-seen carry checkpoints only until share levels are known; export limit versus segmented export; one pre-join checkpoint for a joiner; receipts reveal timing (batch or disclose); quota sizes and how long a session may be; removed members silenced; who carries share-level statements | As on the in-flight branch: hard export limit; receipts not batched and the timing leak disclosed; the daemon will carry the signed share-level statements. |
| [STATUS_M2_POLICY §4 DQ1-11; A1.7 items 1, 4, 5, 6; A4.6 items 2-5] (owner for exclusions, edits-that-execute and bounds; design for the rest) | What an exclusion does; `cat` as a read; taint and grants; git as execute; our own MCP tools' tier; `subject` versus `subjects`; command patterns; unlisted tiers; reads after the link closes; `dontAsk`; ancestor paths; edits that become execution stay highest-scrutiny; approvals ignore `agent_id`; an opaque command naming an excluded file is refused; bounds 160 words / 2,048 components / 64 KiB | UNKNOWN which survive: addendum 5 removes the shell classes these were written against and the seat has not reported (the STATUS file's ADDENDUM 5 and 6 sections say "filled in as the work completes"). Closed by its `READY FOR KAM M2-POLICY r5` report. Nothing in this addendum depends on them. |
| This addendum, 3.4 | Which third-party mechanism | UNDECIDED; path 4 shows "not available yet". |
| [04 §8] C-a, C-d | WebSockets through Funnel and quick tunnels; who operates iroh's shared relays | Unverified; spike C2 not run. |

---

## 10. Every INTERPRETATION, in one place

| # | Where | I assumed | The alternative |
|---|---|---|---|
| I-1 | 1 | The limit is exactly 4, fixed | 4 by default, raisable to 8 by the starter |
| I-2 | 2.1 | The member hands out the invite and pairs with the newcomer | The member only asks; the starter invites and pairs |
| I-3 | 2.1 | Observers cannot propose | Observers may propose |
| I-4 | 2.1 | The starter approves each proposal by hand | The starter may pre-approve a member's proposals for a time |
| I-5 | 2.1 | If the starter has left, nobody can be added | The starter can name a deputy |
| I-6 | 2.1 | A member cannot propose a removed person | Allowed, with "previously removed" on the card |
| I-7 | 2.1 | The starter may admit a proposed guest as an observer | Admit exactly as proposed, or decline |
| I-8 | 3.1 | The connection question is asked every time | Asked once and remembered |
| I-9 | 3.1 | The joiner must also accept a third-party path | Only the person starting the connection chooses |
| I-10 | 3.1 | The guided question ships in the beta; the third-party path may follow | The third-party path must work in the first beta, or stay hidden until it does |
| I-11 | 4.2 | The daemon's own relay keeps an identity only when the user turned the setting on | Within one session the same identity is always re-supplied from memory; only keeping it across sessions needs the setting |
| I-12 | 5.2 | Newcomers after a removal inherit the removed members' used tries and hard stops | No inheritance; state that a hostile starter gets five more guesses per remove-and-re-add |
| I-13 | 6 | "Same rules as mac" means every command asks plus the exact list, and Windows follows the Mac if the Mac rule ever changes | He meant only the original option c; a later relaxation on the Mac would need a separate decision for Windows |
