# CoAgent — design revision applying the owner's rulings of 2026-11-16

**Date:** 2026-11-16 · **Status:** design revision for the owner's review; nothing built, no project code run · **Author:** security/protocol architect (agent, Fable 5.2)
**Revises:** `03_architecture-design.md` (cited as **[AD §n]**). That file is not edited; where this document and [AD] differ, this document wins. Other inputs: `00_requirements.md` (R-items), `01_existing-code-review.md` (**[CR …]**), `02_prior-art-research.md` (**[PA …]**).
**Client:** General (the owner's personal project).

**How to read the evidence labels.** Every mechanism this revision leans on carries one of three labels:

- **[read today: Sn]** — I fetched the primary source on 2026-11-16 and read the statement. Sources are listed in Appendix A. A dagger (†) there means the fetch tool returned a summary with quotations rather than the raw page, so exact field names must be re-opened before they are pinned in code.
- **[inferred]** — my reasoning from things read today or from [AD]. Not a fact about any product.
- **[UNVERIFIED]** — from my memory, or not checked today. Every such item is collected in §8 with the spike or source that settles it.

Nothing below was measured: no code ran. Every number that looks like a measurement is an estimate or a proposed constant and says so.

---

## 1. One-page summary

**Bottom line.** The rulings roughly double phase 1. The original estimate was 28–39 agent-days; the revised estimate is **about 53–75 agent-days**. Three rulings carry almost all of that: groups and observers (+13–18), native Windows (+7–10), and no public relay (+3–5). The product is also harder to start using than the original design promised, because nobody runs a relay for the user any more.

**What changed.**

1. **Groups and observers are in phase 1** (D11 b). A session can now hold up to **8 parties**. The design keeps one rule unchanged: only the owner of a machine can approve what runs on it. Nobody else in the group — not the person who started the session, not a majority — can approve, grant or change mode on someone else's machine. An **observer** is a member who can watch what each machine's owner chooses to show them and can talk to the people, but cannot send work to anyone's agent.
2. **Encryption for groups is pairwise, not a shared group key.** Every pair of members has its own encrypted channel (the same construction the two-party design already uses), multiplexed through the blind relay. This is recommended over MLS and over sender keys for a group this small; §3.1 gives the reasons. It is also what makes "this member sees full detail, that observer sees summaries" enforceable by encryption rather than by good manners.
3. **Native Windows is in phase 1** (D10 b). Claude Code runs natively on Windows and its hooks work there, but **its sandbox does not exist on native Windows**. On Windows an approved command has no operating-system boundary around it at all. The design compensates with stricter defaults, not with an equivalent protection, because there is none to offer in phase 1.
4. **No public relay** (D3 b). Someone in each session must run the relay and make it reachable. The short spoken code alone no longer works for first contact between strangers, because the code cannot say where the relay is. First contact becomes "paste a link", and the link carries the relay address.
5. **Unreviewed beta, indefinitely** (D8 b). The product never claims a "1.0" and says, in the README, at install, and on the pairing screen, that nobody independent has reviewed it. The automated test suites are kept and extended; they are not a substitute for a review and the product says that too.
6. Rulings that matched the design's defaults (D1, D2, D5, D6, D9, D12, language, nightly tests, build model, repository) change nothing structural. D7 adds one small phase-1 obligation so phase 2 can offer several identity methods. D4 (leave v0.4.4 as is) removes the withdrawal steps from the plan.

**What it costs.**

| Ruling | Added agent-days (estimate) |
|---|---|
| D11 b — groups and observers | +13 to +18 |
| D10 b — native Windows | +7 to +10 |
| D3 b — no public relay | +3 to +5 |
| D8 b — unreviewed beta: disclosures and extra automated assurance | +1 to +2 |
| D7 — room for several identity methods later | +0.5 |
| **Total delta** | **+24.5 to +35.5** |
| **Revised phase 1** | **≈ 53–75** (was 28–39) |

Not in the figure: the cost of testing every combination of group size, platform and relay arrangement (UNESTIMATED, §7.3); the token cost of nightly model-driven tests (UNESTIMATED); Windows code-signing fees and the owner's time for identity validation.

**What is now riskier (plain).**

- **A member of the group can be hostile or compromised.** With two parties there was one counterpart; with eight there are seven, and the least careful of them sets the risk. Text from any member can end up in a host's agent context. The gate still holds, because the gate never trusted the agent; but an Approved Trust grant now effectively trusts the *least* trusted member whose text the agent has read.
- **The person who starts the session introduces everyone to everyone.** Until two members verify each other directly, they are trusting that introduction. The interface says so on every member chip.
- **On native Windows there is no sandbox.** An approved or granted command can do anything the user can do. The design's default is that commands are never auto-allowed by a grant on native Windows (new decision N3).
- **Whoever runs the relay sees every participant's IP address and traffic pattern, and exposes a listening port.** Under the old design that was a neutral operator; now it is a participant, usually on a laptop. It still cannot read content.
- **Nobody independent will ever check the cryptographic glue.** The group design adds glue (the signed member list, introductions, per-recipient disclosure). That is a larger unreviewed surface than the two-party design had.
- **Ease of deployment is worse.** "One command, no server" (R-EASE) is no longer true for the first session between people on different networks.

---

## 2. Rulings ledger

Source: the owner's rulings on the live board, 2026-11-16 (option text verbatim), including the four that landed at 23:04 and replaced the earlier "still open" list.

| # | Ruling (verbatim) | Versus [AD] | Effect | Where |
|---|---|---|---|---|
| D1 | a "Keep CoAgent" | matches default | none | — |
| D2 | a "Apache-2.0, free, no paywall" | matches default | none structural; interacts with the private-repository ruling (decision N6) | §6.8, §9 |
| D3 | b "No public relay" (card: "Self-host only") | **departs** (AD assumed an owner-run public relay) | new connectivity design; pairing changes; R-EASE restated | §4 |
| D4 | c "Leave as is" | **departs** (AD planned to withdraw v0.4.4) | [AD §12] "What to do with v0.4.4" items 1–3 are removed from the plan and from M0. Nothing else. | §7.1 |
| D5 | a "Ask on the first read of each file or folder" | matches default | none; N-party note | §6.3 |
| D6 | a "Default 60 min, maximum 8 h" | matches default | none; one new down-transition for groups | §6.4, §3.6 |
| D7 | note: "this is good for phase 1. Phase 2 should have multiple options" | phase 1 matches; adds a phase-2 requirement | contact record gains a list of identity proofs; candidates named, not chosen | §6.1 |
| D8 | b "No, ship as unreviewed beta indefinitely" | **departs** (AD recommended a paid review before "1.0") | disclosure obligations; residual risk R6 becomes permanent; compensating measures extended | §6.2 |
| D9 | a "Embedded terminal running your own claude" | matches default | none; Windows adds ConPTY (§5.7) | §5.7 |
| D10 | b "Native Windows in phase 1 as well" | **departs** | new section | §5 |
| D11 | b "Groups and observers in phase 1" | **departs** | redesign of [AD §4, §5, §9, §9.4, §10] for N parties | §3 |
| D12 | a "Hashes and short redacted previews" | matches default | none; per-recipient disclosure tiers in groups | §6.5, §3.9 |
| Language | a "Rust core, TypeScript for the browser console" | matches | none | — |
| Nightly tests | a "Nightly, on the smallest model" | matches | one safeguard against false greens | §6.6 |
| Build model | a "Fable for the M0 spikes, then the routing table" | process | none on the design | §7.2 |
| Repo home | a "A new private repository under your personal GitHub" (old tree copied in as `legacy/`) | matches | import rule for `legacy/`; interacts with D2 (N6) | §6.8 |
| Go card | a (start M0) | — | M0 is revised in §7.2 | §7 |

---

## 3. Groups and observers in phase 1 (D11 b)

**BLUF:** a session becomes a small **group** with a signed member list. Every pair of members shares its own authenticated encrypted channel. The relay stays blind and routes frames between numbered slots. Authority does not become collective: each machine is still gated only by its owner. Hard cap: **8 parties per session**.

### 3.1 The three candidate constructions, evaluated

The requirement that decides most of this is specific to CoAgent and is easy to miss: **content is deliberately not uniform across members.** [AD §5.5] lets each host choose what each counterpart sees of the host's actions: nothing, summaries, or full detail. With an observer in the room, one host will show full diffs to a collaborator and summaries to the observer. A construction where every member can decrypt every message has to rebuild per-recipient confidentiality on top.

| | **A. Pairwise Noise channels** (mesh through the relay, or host as hub) | **B. Sender keys** (Megolm-style) | **C. MLS (RFC 9420), e.g. OpenMLS** |
|---|---|---|---|
| What it is | One Noise channel per pair of members; a sender encrypts each message once per recipient. | Each sender has a symmetric ratchet plus a signing key, handed to every recipient over a pairwise secure channel; each message is encrypted once. | A group key agreed by a tree protocol; members are added and removed by ordered Commit messages; each message is encrypted once to the group. |
| Per-recipient disclosure (the deciding requirement) | **Native.** A recipient only ever receives what was encrypted to them. | Not native: one sender key means one readership. Needs several sender keys per audience, or pairwise messages anyway. | Not native: "only the members in the current epoch have access to the epoch secret" [read today: S1 §3.1] — all of them. Needs sub-groups or a pairwise layer on top. |
| Authentication of who sent a message | Channel is bound to the peer's pinned key; audit-class messages are also signed (already in [AD §10.3]). | Ed25519 signature per message [read today: S6]. | Signature per message by the sender's leaf key [read today: S1 §6.1]; holding only the group AEAD key is not enough to forge a member [read today: S2 §8.3.1.1]. |
| Removing a member | Stop encrypting to them and drop the channel. No key to rotate. | Every remaining sender must start a new ratchet and redistribute it; the Megolm document gives no membership rules at all [read today: S6]. | A Remove needs a Commit with a fresh path; the removed member gets no new entropy [read today: S1 §3.2, §12.4]. Strong and standard. |
| Late joiner and history | No keys existed for them before they joined; nothing earlier was encrypted to them. | Joiner gets ratchet state from the current index forward; earlier messages are unreadable only if senders hand over a current, not an old, ratchet value [inferred from S6]. | "messages sent before they were added to the group will not be accessible" [read today: S1 §3.2]. |
| Forward secrecy / recovery after a key leak | Per connection, plus rekey ([AD §4.2]); a fresh handshake on every reconnect. Enough for sessions that last hours. | Partial forward secrecy and **no** recovery after compromise without starting a new session [read today: S6]. | Both, by design [read today: S1 §1, §16.6] — the strongest of the three, aimed at long-lived asynchronous groups. |
| What it demands from the server | Nothing beyond forwarding. | Nothing beyond forwarding. | An ordering service: "the group must agree on a single MLS Commit message that ends each epoch" and the delivery service "is trusted to break ties" in the strongly consistent mode [read today: S2 §5.2, §5.2.1]; applications "MUST have an established way to resolve conflicting Commit messages" [read today: S1 §14]. |
| What it demands for identity | A way for each pair to learn the other's key (see §3.5). | The same, because sender keys travel over pairwise channels [read today: S6]. | An Authentication Service: "MLS assumes a trusted AS" [read today: S1 §3]; "MLS does not itself enforce any access control on group operations" [read today: S2 §3.5]. CoAgent has no accounts, so the "AS" would be the same pairing-and-introduction problem as in A — MLS does not solve it. |
| Consistency (everyone saw the same thing) | Not provided by the channels. Provided here by signed, hash-chained per-author logs that members cross-check (§3.9). | "there is no guarantee that all recipients have received the same messages" [read today: S6]. | Membership and epoch agreement are provided; a malicious member can still fragment the group with an invalid commit [read today: S1 §16.12; S2 §5.3]. |
| Replay | Noise nonces per connection plus our sequence numbers. | "A message can be decrypted successfully multiple times"; the application must track indices [read today: S6]. | Handled by the ratchet generations [read today: S1 §9.1]. |
| Cost at N = 8 | 28 pairwise channels in the group; a sender does 7 small encryptions per message. Trivial for kilobyte JSON [inferred]. | 8 ratchets, 56 key hand-overs, redone on every removal. | Logarithmic costs [read today: S1 §1] that only matter for large groups. |
| Library and maturity | `snow` 0.10.0 — already the phase-1 choice; `KK` and `XX` patterns and a `Psk(u8)` modifier exist in its API [read today: S8, S9]. No new dependency. | No library verified today. A Rust Megolm implementation exists in `vodozemac` [UNVERIFIED]; using the primitive outside its protocol would be our own composition. | `openmls` 0.9.2, MIT, published 2026-10-22 [read today: S3]; implements RFC 9420, builds and tests on `x86_64-pc-windows-msvc` in its CI [read today: S4]. Pre-1.0. A third-party audit and two 2026 security advisories exist according to search results only [UNVERIFIED beyond search level: S5]. |
| New glue we would write (the part nobody will review, D8 b) | Signed roster, introductions, slot routing. | All of A's glue, plus ratchet distribution and rotation rules. | Credential binding to our pairing, commit ordering at the relay or a tie-break rule, fork handling, state persistence, **and** a per-recipient layer for disclosure levels. |

**Hub versus mesh, within A.** With the host as hub, guests pair only with the hub and the hub forwards. That removes the introduction problem and needs N−1 channels instead of N(N−1)/2. It is rejected for three reasons: the hub reads everything, so in a Collaborate session with several hosts a host could not show member B something while showing the hub-owner nothing; the session dies with the hub's laptop; and the hub becomes a forwarding service that must be trusted not to drop or reorder between other people. A mesh multiplexed through the one relay socket each member already has costs little more [inferred].

### 3.2 Recommendation and cap

**Recommendation: pairwise Noise channels in a full mesh, multiplexed through the blind relay, under a signed member list ("roster") with a single writer.** Reasons, in order of weight:

1. **It is the only candidate where per-recipient disclosure is enforced by the encryption itself.** That requirement is a product feature here (share levels, observers), not an edge case.
2. **It adds no new cryptographic dependency and no new primitive.** The two-party design is exactly the N = 2 case, so there is one code path, not a two-party path with a group mode bolted on. Bolting group support onto a two-party key slot is the v0.4.4 failure (§3.3).
3. **It needs nothing from the relay but forwarding**, which matters more now that the relay is a participant's own machine (D3 b) and should be as dumb as possible.
4. **The properties MLS adds are aimed at a different shape of group** — large, long-lived, with members offline for days. CoAgent sessions are live, hours long, and every member is online. Fresh handshakes on reconnect and rekeying already bound a key leak to minutes [AD §4.2].
5. **Under D8 b, the amount of unreviewed glue is the thing to minimise.** MLS would give audited group-key machinery and then require more of our own glue around it than A needs in total.

**Honest cost of the recommendation:** no group-wide key agreement means no built-in proof that everyone saw the same membership or the same events. The design supplies that with the single-writer roster (§3.5) and cross-checked audit chains (§3.9); both are our glue. And pairwise channels do not scale: this recommendation is only sound with a small cap.

**Hard cap for phase 1: 8 parties per session** (the convener included, observers included; an owner's own approval devices are not parties). Eight gives at most 28 pairwise channels and 7 encryptions per message. The cap is enforced in the roster validator of every member's daemon, not only at the relay. The number is chosen for tractability — a readable roster strip, a test matrix that ends — and is **not measured**; spike G2 measures join and fan-out cost at 8.

**When to revisit MLS:** a cap above 8, members who must receive while offline, rooms that live for days, or the phase-2 gateway to server-hosted agents (the one piece of prior art that puts a blind relay and MLS under agent protocols is SLIM [PA §A, D.6]). To keep that door open the handshake `hello` advertises a key-exchange feature string (`kx.mesh.v1`), and nothing above the channel layer assumes how keys were agreed.

### 3.3 How this avoids the v0.4.4 multi-party failure

What the review found [CR S9, read today in `01_existing-code-review.md` lines 180–182]: each v0.4.4 daemon held **one** `sharedSecret`. When a third peer broadcast its public key, each existing peer overwrote that single secret with one derived against the newcomer and did not reply, so the two original peers could no longer decrypt each other; the newcomer had no key and sent plaintext; plaintext was accepted; the UI warned and carried on. Sender identity was self-asserted.

| v0.4.4 failure | Rule in this design | Test that would fail if the rule were broken |
|---|---|---|
| One key slot, overwritten by the newest arrival | Key state is a map keyed by `(session id, peer device key)`. There is no singleton and no "current key". A channel's keys are created by one completed handshake and destroyed only when that channel closes. | **Third-joiner test:** A and B exchange messages; C joins; A and B continue on the same channel without a new handshake; C cannot decrypt A↔B frames captured at the relay. |
| Key exchange by unauthenticated broadcast | There is no broadcast key exchange. A pairwise channel is opened only by a Noise handshake against a key that is in the convener-signed roster (or already pinned as a contact). | Hostile relay injects a handshake from a key not in the roster → refused before any state is created. |
| Plaintext fallback when no key exists | The decoder has no plaintext branch ([AD §4.2] already). A frame that fails authentication under its channel is dropped and logged; it is never re-interpreted. | Property test over the frame decoder: no input yields an application message without a successful AEAD open. |
| Session continued in a broken state | A member whose channel to another roster member cannot be established is shown as "not connected to X" on both sides; messages to X are queued, never downgraded. | Integration test with one pair blocked at the relay. |
| Self-asserted sender | `from` is taken from the channel's pinned key. An envelope whose `from` field disagrees with the channel is rejected. Role is taken from the roster, never from the message. | Injection suite: member claims another member's id, or the `convener` role → rejected by the decoder. |
| Relay admitted unlimited peers on a live code | The pairing mailbox stays strictly two-slot and single-use. Joining a group is a new one-time code for each joiner, issued by the convener. The relay cannot add a member: membership is the signed roster plus each host's own acceptance. | Hostile relay connects a ninth socket → it receives ciphertext it cannot open and no member encrypts to it. |

### 3.4 Roles and authority

Three roles, plus one administrative capability. "Host" keeps its [AD §2.1] meaning: it is relative to a machine, not a title held for the session.

| Role | Definition |
|---|---|
| **Host** | A member, with respect to **their own machine**. Every member with a bound agent is host of their machine, always. |
| **Guest** | A member, with respect to **someone else's machine**. Can send requests to that machine's owner (who decides whether their agent sees them), ask questions, receive shares. |
| **Observer** | A member whose roster entry says `observer`. Receives what each host chooses to show them; can chat with people. Cannot address any agent, cannot send requests, cannot propose grants. Has no agent bound, so nothing on the observer's machine is tainted. |
| **Convener** (capability, not a fourth role) | The member who created the session. Sole writer of the roster: admits and removes members and assigns guest or observer. Holds **no** authority over any other machine. |

**The authority matrix.** The gate stays with the owner of the machine the action runs on. No row gives a second party any power over machine M.

| Act | Owner of machine M | Convener (not M's owner) | Other guest | Observer | M's own agent |
|---|---|---|---|---|---|
| Approve or deny an action on M | **Yes — only this person** | No | No | No | No |
| Issue, edit or revoke a grant for M | **Yes** | No | No | No | No |
| Change M's mode; pause, stop or resume M | **Yes** | No | No | No | No |
| Decide what each member sees of M's activity (share level per member) | **Yes** | No | No | No | No |
| Hand a held request to M's agent, or decline it | **Yes** | No | No | No | No |
| Approve a share of M's content, and to which members | **Yes** | No | No | No | No (it can only propose the share) |
| Block a member locally (M stops sending to and accepting from them) | **Yes**, without asking anyone | — | — | — | No |
| Send a request addressed to M | — | Yes, as a guest | Yes | **No** | — |
| Propose a grant (advisory text only) | — | Yes | Yes | **No** | Yes |
| Chat with people | Yes | Yes | Yes | Yes | n/a |
| Admit or remove a member; change guest ↔ observer | No (unless convener) | **Yes** | No | No | No |
| End the session for everyone | No (can leave) | **Yes** | No (can leave) | No (can leave) | No |
| Leave | Yes | Yes (ends roster changes; see §3.5) | Yes | Yes | No |

Three rules make the matrix real rather than a table of intentions:

1. **No collective approval exists in phase 1.** There is no quorum, no co-signature, no "approve on behalf of". A second pair of eyes is an observer who can *say* "don't" in chat; the click is the owner's. (A four-eyes mode where a host *requires* a named member's countersignature before their own Allow enables is a possible phase-2 addition; it would add a condition to the owner's decision, never replace it.)
2. **Admission is not access.** When the convener admits a member, each host's share level for that member starts at **nothing**, and requests from that member to that host are refused, until that host's owner accepts the new member in a local dialog and picks a level. A convener can fill the room; they cannot make anyone's machine talk to the newcomer.
3. **Roles are enforced where messages are decoded.** Each daemon rejects, before any handler runs, a `request.new`, `grant.proposed`, or agent-addressed `chat.msg` whose sender's roster role is `observer`, and any roster change not signed by the convener's key. This extends the [AD §10.3] rule "no message type can carry a decision from the peer": no message from *any* member can carry a decision about another member's machine.

### 3.5 Revised §4 — linking and identity for N parties

**What the humans do.**

1. Kam runs `/collaborate`, chooses *Invite*, and is now asked *who works where* and *how many people*. He becomes the convener. The session exists with a roster of one.
2. For each person, Kam's side issues a **separate single-use invite** (link, or code where a relay is already agreed — §4.3). Each invite is created as *guest* or *observer*.
3. A joiner pairs **with the convener** exactly as in the two-party design: PAKE-keyed or link-keyed Noise `XXpsk3`, three verify-words read aloud, contact saved [AD §4.2]. The two-slot mailbox is unchanged.
4. The convener's daemon signs a new roster version that adds the joiner and sends it to every member over their pairwise channels.
5. The joiner's daemon and every existing member's daemon then open their pairwise channels automatically (below). Each existing member sees: *"Kam added Sam (guest). You have not verified Sam yourself. Share with Sam: [nothing] [summaries] [full] · [Verify Sam…]"*.
6. Work proceeds. The strip shows every member, their role, and for each one either **verified by you** or **introduced by Kam**.

**Roster.** A signed, versioned object; the convener's key is the only valid signer.

```jsonc
roster { "session_id": "…", "version": 4, "prev_hash": "sha256:…",        // hash chain of roster versions
         "convener": "<key id>", "cap": 8,
         "members": [ { "key_id": "…", "noise_static": "…", "sign_pub": "…", "binding_sig": "…",
                        "role": "guest" | "observer", "slot": 3, "added_at": "…" }, … ],
         "removed": [ { "key_id": "…", "at_version": 3 } ],
         "sig": "<convener ed25519>" }
```

Because there is exactly one writer and a version counter, roster changes are totally ordered without any ordering service. This is the property MLS needs a delivery service for [read today: S2 §5.2], obtained here by not allowing concurrent writers [inferred]. The price: if the convener leaves, the roster is frozen — members can still work and leave, but nobody can be added or removed. Convener hand-over is not in phase 1.

**Pairwise channels between members who did not pair by code.** Both sides know each other's static key from the roster, so they run Noise `KK` (both static keys known in advance [read today: S7 §7.5]) with a prologue binding the session id, the roster version hash and both slot numbers. The initiator is the member with the lower key id. A mismatch in what the two sides believe the roster is makes the handshake fail [inferred from the role of the prologue; exact `snow` call UNVERIFIED — spike G1].

**The introduction problem, stated honestly.** A channel between Sam and Priya that was set up from the roster is only as trustworthy as the convener's statement of their keys. A hostile convener who also controls the path between them — and under D3 b the convener is often the relay operator — could give each a false key for the other and sit in the middle of *that pair*. Three defences:

1. **Known contacts are checked automatically.** If Priya already has Sam as a verified contact, the roster's key for Sam must equal the pinned key or Priya's daemon refuses the member with the SSH-style warning of [AD §4.2].
2. **Pairwise verification is offered and its absence is always visible.** "Verify Sam" shows words derived from the Sam↔Priya handshake; both read them aloud. Until then the chip says *introduced by Kam*, and policy treats the member conservatively: a grant on Priya's machine cannot name an unverified-by-Priya member as a subject (§3.6).
3. **What is exposed if the introduction was false:** traffic between that one pair — their chat, and whatever each host chose to share with the other. Not authority: nothing a middleman reads or alters can approve anything.

One weakness is carried in the open. Verify-words are a short string (about 31 bits in [AD §4.2]). On first contact by code, an attacker cannot even run the handshake without the code, so the words only matter if the code leaked. On an *introduced* pair there is no such secret: the words are the only defence, and whether a middleman could search for handshake values that make both pairs of words match within the handshake deadline has not been analysed [UNVERIFIED — spike G4]. Candidate fixes, to be chosen in G4 and not before: a commit-then-reveal exchange of random values mixed into the words (the standard short-authentication-string construction) [UNVERIFIED]; or longer words and a short handshake deadline. Until G4 reports, the design claims **no** protection from the words on introduced pairs against a convener who is also the relay.

**Identity.** Unchanged for phase 1 (D7): a party is a device key; names are claims; policy keys on keys. New: a contact record carries *how* it became verified — `by_code_with_me`, `by_words_with_me`, or `introduced_by:<key id>` — and that provenance is shown wherever the name is.

**No hidden members.** Every member receives the complete roster, including observers. There is no "silent observer" role. What cannot be prevented: any member can forward what they receive to someone outside the session. That was already true with two parties.

**Removal.** The convener signs a roster version without the member. Each remaining daemon, on verifying it, closes its pairwise channel with that key and erases the channel keys. Removal therefore does not depend on the relay or on the removed member cooperating; honest members simply stop encrypting to them. Each member acknowledges the new version, and the convener's console shows *"removal confirmed by 6 of 6"*. Until a member has acknowledged, the convener is told that member may still be sending to the removed party — a hostile relay can delay a roster update but cannot hide the delay. Every envelope carries the sender's roster version, so a member that is behind is noticed by the next peer it talks to and is sent the current roster.

**Late joiner and history.** A joiner's channels are created at join. Nothing sent earlier was encrypted to any key they hold, so earlier content is unavailable to them by construction, not by policy. If a host wants a newcomer to have context, that is a **share** — a gated action on that host's machine, showing the exact content and the exact recipient [AD §3.3 step 10]. There is no "send history to new member" switch.

**Relay changes** are in §3.8 and §4.

### 3.6 Revised §5 — the two modes with N parties

**What does not change.** A mode is still a property of one machine's direction and is set only by that machine's owner [AD §5]. Tiers T0–T3, hard denies, exclusions, approval binding to the hash of the exact input, expiry to deny, Pause/Stop/Revoke — all unchanged. With N parties the *number of people who are told* changes; the number of people who *decide* stays one.

**What changes.**

| Topic | Two-party design | N-party rule |
|---|---|---|
| Who a request comes from | "the guest" | Each request names its sender (from the channel) and is addressed to **one** host. No broadcast "ask everyone's agent" in phase 1. Held requests queue per sender. |
| What the approval card shows | the request that led to the action | The request and its sender, plus: *"Your agent's context also contains text from: Sam, Priya."* Taint is session-wide [AD §3.4], so the card names everyone whose text is in the context, not only the latest requester. |
| Share level | one setting for the one guest | **A setting per member**, default *nothing* until the owner accepts that member; the suggested level in the accept dialog is *summaries*. Enforced by sending each member only their tier (§3.9). |
| A share | to the peer | To a named set of members. The approval binds the exact content **and** the exact recipient set; changing either is a new approval. |
| Chat audience | people / their agent / both | Recipients (all or named members) × audience. Text for an agent names whose agent. Observers can only send to people. |
| "Ask" on a pending card | goes to the guest | Addressed to one named member; answers are display-only as before. |
| Rate limits | per peer | Per member, plus a per-session ceiling so seven members cannot together flood one host. |
| Guest-side view | what the host chose | Each member sees, for each host, what that host chose for them. Two members may see different detail of the same action; the interface labels the level it is showing. |

**Approved Trust with several members.**

- A grant gains `subjects`: the members whose requests are admitted to the agent without being held while the grant is active. Requests from anyone else are still held.
- **A grant trusts the least-trusted member in the agent's context.** Because taint is session-wide, text from a non-subject that is already in the context can steer actions the grant then auto-allows. The grant dialog says this in one sentence and lists everyone currently in context. A member the owner has not verified personally cannot be a subject.
- Time box per D6: default 60 minutes, maximum 8 hours. Unchanged.
- **New down-transition: any roster change suspends every active grant in the session** on every machine. The owner sees *"Sam joined — trust paused"* and re-confirms with one click, or does not. Reason: a grant was issued for a known set of people; the set changed.
- The grant record is sent to its subjects; every member is told the mode changed (the mode of each machine is always visible in the strip, at every share level).

**Observers, exactly.**

| An observer can | An observer cannot |
|---|---|
| See the full roster and each machine's mode | Send a request to any agent, or text addressed to any agent |
| See, for each host, what that host set for them: nothing, summaries, or full | See anything a host has not sent them — there is no key with which to try |
| Chat with people; be asked questions by a host | Propose a grant or a needs-manifest |
| Hold signed audit headers and checkpoints for what they were shown (§3.9) | Approve, deny, pause, stop or revoke anything on any machine |
| Leave | Admit or remove anyone |

Observer confidentiality has two halves. *What observers learn:* only what was encrypted to them, plus metadata every member can infer (who is in the session, that events are occurring). *What observers can leak:* everything they were shown. The accept dialog for an observer says: "Sam will be able to keep and pass on whatever you show them."

**Transitions.** [AD §5.4] stands, with the roster-change suspension added and one clarification: nothing a convener does is a transition on another member's machine.

**Interface consequences (brief; the wireframes in [AD §6] are not redrawn here).** The strip's single peer chip becomes a roster row: name, role, verified-by-you or introduced-by, connection state, the level you share with them. The rail gains a *People* tab holding the per-member share levels and the accept/block controls. The terminal-only experience shows the roster in `/collaborate status`; accepting a new member is one more dialog of the kind in [AD §6.6].

### 3.7 Revised §9 — threat model for N parties

[AD §9.1] rows A–G stand. These rows are added.

| # | Adversary | What they try | Mitigations | What is left |
|---|---|---|---|---|
| H | **Malicious or compromised member** (guest or observer) | Steer a host's agent; read what was not shared with them; speak as another member; flood; tell different members different things. | Everything in row A applies per member. Nothing is encrypted to a member beyond their share level. `from` is the channel's key; role comes from the roster. Per-member and per-session rate limits. Any host can block a member locally at once. Signed per-author chains cross-checked between members expose equivocation with transferable proof (§3.9). Observers cannot address agents at all. | A member can leak what they were shown. A member's text, once a host hands it to the agent, is in the context for the rest of that agent session. |
| I | **Malicious convener** | Admit a confederate; present false keys for members (sit between a pair); remove honest members; fill the room. | Admission gives no access (§3.4 rule 2). Pinned contacts are checked against the roster automatically. Introduced members are labelled and cannot be grant subjects. Roster versions are hash-chained and signed, so a convener who shows different rosters to different members produces two signed versions with the same number — proof of misbehaviour once any two members compare (they do, in §3.9's head exchange). | A pair who have not verified each other can be intercepted by a convener who also controls the relay, until they verify (§3.5; strength of that verification is open, spike G4). A convener can always end or wreck the session — that is denial of service, not access. |
| J | **Removed member** | Keep reading; keep sending; rejoin. | Honest members close their channel and erase its keys on the signed roster change; no further message is encrypted to the removed key. The key id stays on the roster's `removed` list; a rejoin needs a new invite from the convener and a new acceptance by each host. Removal is confirmed per member. | Everything received before removal is kept. A member who has not yet received the roster change keeps sending until it does (visible to the convener). |
| K | **Late joiner** | Obtain earlier content. | No keys for earlier traffic exist on their device. History moves only as a gated share by the host who owns it. | A member who was present can tell them anything. |
| L | **Curious observer** / observer confidentiality | Infer more than they are shown. | Per-recipient tiers; excluded paths never appear even as names [AD §5.1]. At level *nothing* a member receives only periodic checkpoints. | Checkpoints reveal how many audit events a host produced and roughly when. Members at *summaries* see action kinds and targets (file names, command names) by definition. |
| M | **Colluding members** | Pool what each was shown; jointly pressure a host. | None needed for authority: collusion adds no power over a machine. | Pooled disclosure equals the union of what each was shown — which the host chose. Social pressure on the owner ("everyone agrees, click Allow") is R2 with more voices. |
| N | **The relay operator is a participant** (new under D3 b) | Learn who talks to whom; target a member; selectively drop or delay; exploit the relay's parser. | Content-blind as before. Roster and removal acknowledgements make selective withholding visible. The relay runs as a separate process with no access to daemon state or identity keys (§4.4). The relay frame parser is a named fuzzing target. | The operator sees every participant's **IP address**, the pairwise traffic graph, sizes and timing. A participant-run relay on a laptop is an internet-facing listener on a personal machine. |

**Why the gate still holds with a hostile member.** [AD §9.2]'s seven points do not mention the number of peers and none of them weakens: the decision input is the harness's own hook payload; the decision is made in another process by the machine's owner or by a grant that owner signed; no peer message of any type is a decision. What N changes is the *inflow* of untrusted text and the *breadth* of what a grant implicitly trusts — residual risks, not holes in the gate.

**Residual risks added to [AD §9.6].**

- **R10 — Introduced identities.** Until two members verify each other, they rely on the convener. Stated in the interface; strength of the verification step itself is open (G4).
- **R11 — A grant trusts the least-trusted member in context.** Keep groups small during trust; the roster-change suspension is the backstop.
- **R12 — No operating-system sandbox on native Windows** (§5.4).
- **R13 — A participant operates the relay** (row N).
- **R6, restated under D8 b:** the pairing glue, the roster and introduction glue, and the PAKE crate are unreviewed and there is no plan to change that. This is now a permanent property the product discloses, not a temporary one.

**Findings table [AD §9.3], rows that change.** *S9* is now designed out by §3.3 rather than by "two parties only". *S12:* the new repository has secret scanning from the first commit and `legacy/` is imported through a filter (§6.8); per D4 c the plan contains no other action on the old tree. *S14:* the paywall is removed (D2 a, as [AD] assumed).

### 3.8 Revised §10 — wire protocol for N members

**Relay layer.** Mailbox frames are unchanged and stay two-slot. Session channels change:

| Frame | Dir | Fields | Change |
|---|---|---|---|
| `chan.create` | C→R | `v`, `chan_id`, `admin_token_hash`, `cap` | New. The convener creates the channel and proves later control with the admin token. `cap` ≤ 8, enforced by the relay as a courtesy and by every daemon as the rule. |
| `chan.slots` | C→R | `admin_token`, `[ {slot, slot_token_hash} ]` | New. The convener registers or retires slots. Slot tokens are random values each member received inside their pairwise channel with the convener. They are denial-of-service hygiene, **not** security: a relay that ignores them can let anyone listen to ciphertext, and nobody encrypts to a key that is not on the roster. |
| `chan.open` | C→R | `v`, `chan_id`, `slot`, `slot_token`, `resume_from` | Was two sockets maximum; now one socket per registered slot. |
| *binary frame* | both | `to_slot` ‖ `from_slot` (stamped by the relay) ‖ `pair_seq` ‖ ciphertext | `to_slot` added. The relay buffers per ordered pair. |
| `chan.ack` | C→R | `from_slot`, `upto` | Per pair. |
| `peer.joined` / `peer.left` | R→C | `slot` | Presence per slot. |

Proposed buffer caps (constants, not measured): per ordered pair 500 frames or 2 MB or 15 minutes; per channel 64 MB in total. [AD §4.4]'s per-direction figure multiplied by 56 ordered pairs would be too much for a relay on a laptop.

**Handshakes.** Joiner ↔ convener: unchanged (`pake.msg` → `pake.confirm` → Noise `XXpsk3`). Every other pair: Noise `KK` from roster keys, prologue = `session_id ‖ hash(roster version) ‖ slots`. `hello` gains `features: ["kx.mesh.v1", "roster.v1"]`.

**Application envelope.** Additions to [AD §10.3] in bold:

```jsonc
{ "v": 1, "id": "01JD…",
  "session_id": "…",                    // **bound into every envelope and every signature**
  "from": "<key id>", "to": "<key id>", // **must equal the channel's two pinned keys, else rejected**
  "roster_v": 4,                        // **sender's roster version; a receiver that is ahead replies with the roster**
  "seq": 118, "ack": 97,                // per ordered pair — the two-party mechanism, once per pair
  "ts": "…", "type": "…", "re": null, "crit": false,
  "chain": { "author_seq": 311, "prev_hash": "sha256:…", "tiers": { "summary": "sha256:…", "full": "sha256:…" } },
                                        // **audit-class only: the author's own chain, identical for every recipient (§3.9)**
  "body": { … },                        // only the tier(s) this recipient is entitled to
  "sig": "…" }
```

New and changed message types:

| Type | Sender | Body | Audit-class |
|---|---|---|---|
| `roster.update` | convener only | the signed roster (§3.5) | yes |
| `roster.ack` | any member | `version`, `hash` | yes |
| `member.accepted` / `member.blocked` | a host, about its own machine | `member`, `share_level` (accepted) | yes |
| `request.new` | guest (never observer) | as before, plus `to_host` | yes |
| `share.content` | host | as before, plus `recipients` (the approved set) | yes |
| `grant.issued` | host | grant with `subjects` | yes |
| `audit.heads.seen` | any member | for each other author: highest `author_seq` and hash this member holds | yes |
| `session.leave` | any member | `reason` | yes |
| `session.end` | convener (for all) | `reason` | yes |

`chat.msg`, `question`/`answer`, `presence`, `resume`, `blob.chunk`, `error` are unchanged apart from addressing. The direction rule of [AD §10.3] is generalised: `action.*`, `grant.issued`, `grant.revoked`, `mode.changed`, `member.accepted` are **reports by a host about its own machine**; a daemon rejects any of them whose subject machine is not the sender's, before any handler runs.

**Ordering, ack, replay with N members.**

- **Ordering.** There is no total order across members and nothing in the gate needs one, because every decision is local to one machine. What exists: (1) strict order per ordered pair (`seq`); (2) strict order per author for audit-class events (`author_seq`, the same for every recipient); (3) total order of roster versions (single writer). The interface merges streams by arrival and shows each author's own sequence; `re` links replies to what they answer.
- **Ack and redelivery.** Cumulative per ordered pair, with a persisted outbox per pair, exactly as [AD §10.4]. A member who is offline holds up only their own pairs.
- **Replay.** Within a connection, Noise nonces. Across reconnects, `seq` and the ULID per pair. Across recipients: an envelope is bound to `session_id`, `from` and `to` inside the channel and the signature, so a member cannot present one member's envelope to another as addressed to them. Audit headers are deliberately transferable — they are signed statements — and replaying one proves only that the author made it. Decisions remain local, single-use and hash-bound, so no replay from any member can re-trigger an approval.
- **Back-pressure.** Token bucket per member and a ceiling per session. A host's action stream is coalesced per recipient, so a slow member does not slow the others.
- **Fan-out.** One encryption per recipient per message. A large share to several members is chunked once and encrypted per recipient; the approval names the set.

### 3.9 Revised §9.4 — the hash-chained audit log for N parties

**Construction.** Each member keeps one append-only **author chain** of the audit-class events they originate. An event's signed header is:

`{ session_id, author, author_seq, ts, prev_hash, type, tiers: { summary: H(salt_s ‖ summary), full: H(salt_f ‖ full) }, sig }`

`hash = SHA-256(prev_hash ‖ canonical(header))`. The header commits to each disclosure tier by a salted hash. Every recipient who is entitled to anything gets the **same header**; each gets only the tier bodies (with their salts) that the author's share level for them allows. So all members hold the same chain for a given author and can compare it, while holding different amounts of content. The salts stop a member at *summaries* from confirming a guess about the *full* body.

**Who holds what.**

| Author's share level for this member | Receives |
|---|---|
| full | every header + summary + full tier (previews are short and redacted by default, D12) |
| summaries | every header + summary tier |
| nothing | periodic checkpoints only: `audit.head {author_seq, hash, sig}` |

**Checkpoints and countersignatures.** Every 50 events or 60 seconds an author sends `audit.head` to every member; each member countersigns and returns it. An author therefore holds up to N−1 countersignatures per checkpoint, and each member holds the author's signed statement of their log state at many points in time [AD §9.4, generalised].

**Equivocation.** With two parties, a host could not tell two different stories because there was one listener. With N it could try. Members periodically exchange `audit.heads.seen` — the latest sequence and hash each holds for every *other* author. Two different signed headers or heads from one author with the same `author_seq` are a self-contained proof that the author told two stories. The daemon raises an alarm, marks the session, and stores both signed objects as evidence. The same exchange catches a convener who issued two rosters with one version number.

**Receipts.** A recipient appends a signed receipt to its own chain for each cross-party event it stores, as in [AD §9.4].

**Joiners and leavers.** A joiner's view of an author's chain starts at the head they are given at join; they can prove nothing was rewritten *after* that point and nothing about before. A removed member's last countersigned checkpoint marks the end of what they can attest.

**Export and verification.** `coagent audit export <session>` writes: the roster history with signatures; each author chain as this member holds it; tier bodies held; countersignatures; heads-seen records; the public keys. `coagent audit verify <bundle>` checks every chain, signature and countersignature offline, checks that roster versions form one chain, and reports any equivocation evidence. Two members' bundles can be verified together to check that they agree on the headers they both hold.

**Limits, stated.** As before, the log proves what each party recorded and signed and that it was not changed later; it does not prove a host recorded everything that ran on its own machine, and timestamps are local clocks. New limits: consistency is detected only between members who actually exchange heads while both are connected; a member at *nothing* attests only to counts; and all of this is glue that will not be independently reviewed (D8 b).

---

## 4. No public relay (D3 b)

**BLUF:** the project operates no relay, no rendezvous service, no join page, no domain. A relay is a role that one participant's installation plays for a session, or a small server a person or team runs for themselves. This removes a third party and removes the simplest part of the original experience. For people on different networks, first contact now requires someone to make a port reachable, and the invite must carry the address.

### 4.1 What breaks in the original design

| [AD] element | Why it breaks | Replacement |
|---|---|---|
| Default relay `relay.coagent.live` [AD §4.4, §6.5] | Nobody operates it. | The relay address is part of every invite; there is no default. |
| Short code alone as first contact [AD §4.1] | The code named a mailbox on a relay both sides already knew. With no well-known relay the code cannot say where to go. | First contact is a **link** (or QR) carrying relay address(es), the relay's TLS pin, the mailbox id and the secret. The spoken code still works wherever both sides already share a relay setting (§4.3). |
| Join page on the project site [AD §4.1 Path B] | A hosted page is hosted infrastructure. | The link is a `coagent://join#…` URI plus the same content as one line to paste: `coagent join <blob>`. Install instructions live in the repository README. |
| "Call a contact" on a rendezvous channel [AD §4.1, §4.2] | Needs a relay both can reach at an address both already know. | Each contact record stores the relay candidates last used with that contact. *Call* works when one of them is still reachable (team relay, stable tailnet name); otherwise the caller sends a fresh link. |
| Release-time relay operations, abuse limits for a public service [AD §4.4] | No public service. | Per-IP limits remain as protection for whoever runs a relay; nothing is operated by the project. |

### 4.2 The options, evaluated

| Option | How others reach it | Works when | Honest problems |
|---|---|---|---|
| **A. A participant runs the relay** — `coagent relay`, or the convener's install starting it for the session | see the next three rows | — | The operator is a participant (threat row N). A laptop that sleeps ends the session for everyone. |
| A1. Same network (LAN, office, or an existing VPN) | private address and port | Everyone is on one network. | Nothing outside the network can join. On Windows a first listen on a non-loopback interface is expected to raise a firewall prompt [UNVERIFIED]. |
| A2. A tunnel the user already has | **Tailscale, same tailnet or shared machine:** the relay's tailnet name. **Tailscale Funnel:** a public HTTPS name on port 443, 8443 or 10000; the Funnel relay "cannot decrypt data sent over this proxy"; the visitor does not need Tailscale; needs MagicDNS, HTTPS certificates and a funnel attribute in the tailnet policy; "non-configurable bandwidth limits" [read today: S23]. **Cloudflare quick tunnel:** `cloudflared tunnel --url http://localhost:<port>`, no account, a temporary `trycloudflare.com` name that "changes each time"; "for testing and development"; "no uptime guarantee"; 200 in-flight requests [read today: S24]. | The convener already uses one of these. | Neither page fetched today says whether WebSocket connections pass [UNVERIFIED — spike C2]. A quick tunnel's terms make it a demo path, not a supported one, and its name changes every run, so *Call a contact* never works over it. A tunnel provider terminates or carries the connection and sees relay metadata — acceptable, since the relay layer is untrusted by design. **CoAgent does not download, bundle or manage any tunnel program**; v0.4.4 did, and that was finding S11. The user runs their own. |
| A3. Port forward on the convener's router | public IP address and port | The convener controls a router with a public address. | Fails behind carrier-grade NAT and on most corporate and mobile networks [UNVERIFIED as to how common]. There is no domain, so no ordinary certificate: the relay uses a self-generated certificate and the invite carries its fingerprint for the joiner to pin [inferred; pinning with the Rust TLS stack is UNVERIFIED — spike C1]. The convener cannot test reachability from outside without help, because the project hosts no echo service: the first joiner's attempt *is* the test. |
| **B. A relay on the user's own cloud account or server** | a stable name or address the user controls | A person or team wants repeated use. | A real setup task (a container or small VM, a port, optionally a domain and certificate) that the project can document but not do. Costs the user money; the project prices nothing. Once done, it restores most of the original experience for that team — including the short spoken code. |
| **C. Direct peer-to-peer with hole punching** | no relay in the data path when it works | Both networks allow it. | Two machines behind NAT still need *some* third point to find each other and to fall back to. The library the original design named, iroh (1.4.1, MIT OR Apache-2.0 [read today: S25]), "establishes direct connections whenever possible, falling back to relay servers if necessary" and offers "Shared, Dedicated, or self-hosted relays" [read today: S25]. Using its shared relays would make a third party's service a dependency of every session; who operates them and on what terms was not on the page read today [UNVERIFIED]. Using self-hosted ones is option A or B again with a larger dependency. A pure "exchange connection blobs by hand" flow avoids any server and is a poor experience. Hole punching also fails on some NAT types with no fallback [UNVERIFIED as to rates]. And with N members it means up to 28 direct connections, each of which may fail separately. |
| **D. LAN only** | automatic discovery on the local network | Same room or office. | Does not meet R-LINK ("anyone's in the world"). It is the A1 case with discovery added. |

### 4.3 Recommendation

1. **The relay is embedded and startable by the convener** (option A), with the reachability left to the user and made as legible as possible. `coagent relay` remains a standalone command for option B.
2. **An invite carries a list of relay candidates**, tried in order, with the relay's certificate fingerprint. The joiner's client reports which candidate worked or, for each one that failed, why.
3. **A relay profile can be saved** (`coagent relay use <name> <url>`). Where both sides have the same profile — a team relay, a shared tailnet — the short spoken code works exactly as [AD §4.1] described. This is the path that keeps R-EASE for people who collaborate repeatedly.
4. **Peer-to-peer hole punching is not built in phase 1.** Whether a later version may depend on a third party's public rendezvous service is the owner's call (decision N5).
5. **`coagent doctor net`** tells the convener what it can determine locally: the addresses the relay is listening on; whether a tailnet interface exists; whether the address is private. It says plainly that it cannot test reachability from the internet.

### 4.4 Security of a participant-run relay

- The relay is a **separate process** from the daemon, started with no access to the identity keys, the SQLite store or the IPC endpoint. A flaw in the relay's network parser must not reach security state [inferred design rule]. On Windows the relay is a good candidate for an AppContainer, whose network isolation can grant "acting as a server" and little else [read today: S18]; whether that is practical for an unpackaged Rust executable is UNVERIFIED (spike W5).
- [AD §3.1] said the daemon never listens on non-loopback interfaces. That stays true of the **daemon**. The relay process is the one component that listens externally, on its own port, and it speaks only the relay frame protocol.
- The relay frame parser becomes internet-facing on a personal machine. It is promoted to a first-class fuzzing target and gets a strict size and rate budget before any allocation.
- The relay stops when the session ends. It never starts by itself, and the convener sees a persistent "you are hosting the relay on <address>" line while it runs.
- The pin in the invite authenticates the relay's TLS endpoint to joiners. That protects metadata from the network, not content from the relay; content is protected by the pairwise channels regardless.

### 4.5 What this does to R-EASE, plainly

R-EASE asks for "as easy to deploy and collaborate with as possible; change the natural workflow of AI users as little as possible". The original design answered with one install command and a spoken code. After D3 b:

**What a first-time user now has to do before the short code works.** Someone in the group must already have a relay that the others can reach, *and* both sides must have its address configured. For two strangers on different home networks, that means one of them must do one of: set up and expose a tunnel they already run; forward a port on a router they control; or stand up a small server. None of those is a CoAgent step and none can be done for them by a product with no hosted service. Only then does a code work — and only after the address has been conveyed once, which in practice means the first contact is a pasted link, not a spoken code.

| Situation | Experience after D3 b |
|---|---|
| Same office, same home, same VPN or tailnet | Close to the original: the convener's install starts the relay; the invite link or QR carries a private address. No extra setup. |
| A team that has set up one relay (option B) once | The original experience, including the spoken code, for everyone who has saved the team's relay profile. |
| Two people on different networks, one of whom already runs Tailscale Funnel or a similar tunnel | One extra command for that person, then a pasted link. Minutes, if the tunnel is already set up [inferred; not timed]. |
| Two people on different networks with no tunnel and no router access (the troubleshooting-a-stranger's-machine use case in R-USES) | **Not possible without one of them installing and configuring third-party tooling or a server.** This is the use case the ruling costs most. |

The [AD §12] M5 acceptance test — "a person with only Claude Code installed reaches a linked session in under three minutes using one install command" — cannot be kept as written. It is replaced in §7.1 by two measured tests: one on a shared network, one across networks with a pre-existing relay, each reporting the time actually taken. No target time is claimed for the cross-network case until it has been measured.

### 4.6 What the test suite uses

- **All automated tests use a relay started by the test on loopback** (`127.0.0.1`, ephemeral port). No test depends on any network service. The hostile relay of [AD §11.3] is the same test double with misbehaviour switched on.
- **Group tests** run 3 and 8 daemons against that loopback relay.
- **Cross-network behaviour** is tested on Linux CI with separate network namespaces: two or more private networks and a relay on a third, including a variant where one side's path drops [inferred as feasible on hosted CI runners; UNVERIFIED — spike C3].
- **Tunnel recipes** (Funnel, quick tunnel) and **port forwarding** cannot be automated without accounts and real networks. They are a manual checklist run before each release, and the documentation labels each recipe with the date it was last tried.
- **Nightly model-driven tests** (§6.6) use the loopback relay.

---

## 5. Native Windows in phase 1 (D10 b)

**BLUF:** Claude Code runs natively on Windows and its hook system works there, so the gate — which is the hook plus the daemon — carries over. What does not carry over: the sandbox, Unix sockets with peer-credential checks, POSIX path rules, and a shell whose syntax the classifier already understands. Windows gets its own installer, its own IPC transport, its own path normaliser and its own conservative shell recogniser, and it runs with one fewer layer of defence.

### 5.1 What was read today about Claude Code on Windows

| Fact | Evidence |
|---|---|
| Supported: Windows 10 1809+ or Windows Server 2019+, x64 or ARM64; install from PowerShell, CMD or WinGet; "You do not need to run as Administrator." | [read today: S12] |
| Git for Windows is **optional**. Without it, "Claude Code runs shell commands via the PowerShell tool"; with it, Claude Code uses Git Bash for the Bash tool and the PowerShell tool is also on by default for claude.ai and Console accounts. | [read today: S12, S13] |
| "On Windows without Git Bash, the tool is enabled automatically and Claude Code doesn't register the Bash tool at all. A hook that matches only `Bash` never fires there." Hooks should match `Bash\|PowerShell`. | [read today: S11†] |
| The PowerShell tool's hook input has the same fields as Bash, with the command in `tool_input.command`. | [read today: S11†, S13] |
| Claude Code "auto-detects `pwsh.exe` for PowerShell 7+ with a fallback to `powershell.exe` for PowerShell 5.1"; it spawns PowerShell with `-ExecutionPolicy Bypass` at process scope; "PowerShell profiles are not loaded"; "On Windows, sandboxing is not supported" (listed as preview limitations). | [read today: S13] |
| A command hook's string is passed to "Git Bash on Windows, or PowerShell when Git Bash isn't installed"; the `shell` field selects one explicitly. | [read today: S11†] |
| **Exec form:** when `args` is present, Claude Code "spawns it directly with `args` as the argument vector. There is no shell". "On Windows, exec form requires `command` to resolve to a real executable such as a `.exe`." Path placeholders are substituted into `command` and each `args` element. | [read today: S11†] |
| `onFailure: "block"` exists and needs v2.1.295+. Also: "On Windows without Git Bash, a shell-form `PreToolUse` or `PermissionRequest` command hook that fails with `onFailure` unset can instead block the tool call." | [read today: S11†] |
| In hook input "On Windows, the path arrives with backslash separators, even when your hook runs under Git Bash". | [read today: S11†] |
| Sandbox: "The sandbox runs on macOS, Linux, and WSL2. On native Windows, Claude Code runs commands unsandboxed." With `sandbox.failIfUnavailable` set, Claude Code exits at startup there. | [read today: S10†] |
| On Windows, Glob is part of the default tool set; on macOS, Linux and WSL, Glob and Grep are left out and "the searches reach your hooks and permission rules as `Bash` calls". | [read today: S13] |
| The Monitor *tool* is available on Windows only when Git Bash is installed. | [read today: S13] |
| Claude Code's own Windows binary is Authenticode-signed by "Anthropic, PBC". | [read today: S12] |
| Plugin `bin/` files "are on the Bash tool's `PATH`"; `${CLAUDE_PLUGIN_DATA}` resolves to `~/.claude/plugins/data/<id>/` and persists across updates; on Windows substituted paths mostly use forward slashes but "keep their native backslashes in an exec-form hook and in a hook that runs through PowerShell". | [read today: S15] |

One of these changes [AD] on every platform, not only Windows: because searches on macOS and Linux arrive as `Bash` calls running `find` and `grep`, the classifier's simple-command recogniser must cover those forms or every search becomes an `execute` prompt. Added to M0 (spike B16).

### 5.2 Installer

- **Installer first, plugin second, on Windows.** [AD §7.2] has the plugin's shell shim download the binary on first run. On Windows the hook must be a real `.exe` invoked in exec form (no shell between Claude Code and the gate), and a hook configured to fail closed blocks every tool call if the executable is missing. So on Windows the binary is installed first and *it* registers the plugin: `coagent setup` runs the documented `claude plugin install` command [AD V5]. Uninstall removes the plugin before the binary. Whether the same order should replace the shim on macOS and Linux is decided by spike W2; this revision does not assume it.
- **Format and location.** A per-user install under `%LOCALAPPDATA%`, no administrator rights, matching how Claude Code itself installs [read today: S12]. The executable directory is added to the user's `PATH` so the exec-form hook resolves it. Delivered as a signed installer and a zip from the repository's releases. A WinGet package is desirable; the submission process and its requirements were not checked today [UNVERIFIED].
- **No pipe-to-shell.** The `irm … | iex` pattern Claude Code documents for itself is not copied; [AD]'s rule from finding S11 stands.
- **Architectures.** x64 is built and tested. ARM64 Windows is built; whether it is tested depends on CI runner availability [UNVERIFIED]. If it is not tested it is labelled so.
- **Two Windows configurations are both supported and both tested:** with Git for Windows (Bash and PowerShell tools) and without (PowerShell only). They differ in which tools exist and which shell runs shell-form hooks; CoAgent's own hook avoids the second difference by using exec form.

### 5.3 Daemon and service model, and local IPC

- **Not a Windows service.** A per-user background process started on demand by `coagent.exe` (from the hook client, the MCP server or the skill) and exiting when idle, as on other platforms. A service would need an administrator to install, would run outside the user's desktop session, and would hold user-level secrets in a more privileged place [reasoning inferred; the session-isolation details of Windows services are UNVERIFIED]. Nothing starts at login in phase 1.
- **IPC: named pipes, not Unix sockets.** Reasons: named pipes are first-class in the async runtime [AD] already uses — `tokio::net::windows::named_pipe` exists with `first_pipe_instance`, `reject_remote_clients` and a raw security-attributes constructor, and "Remote clients are disabled by default" [read today: S17†]. Windows also has Unix-domain sockets, but their support in the Rust standard library and runtime, and the absence of a peer-credential check equivalent to the one [AD §9.1 row D] relies on, were not verified today [UNVERIFIED]; the pipe route needs neither.
- **The default pipe permissions are not acceptable.** "The ACLs in the default security descriptor for a named pipe grant full control to the LocalSystem account, administrators, and the creator owner. They also grant read access to members of the Everyone group and the anonymous account." [read today: S16]. The daemon therefore always creates its pipe with an explicit security descriptor granting access only to the user's logon session — Microsoft's stated way "to prevent remote users or users on a different terminal services session from accessing a named pipe" is to "use the logon SID on the DACL" [read today: S16].
- **Single instance and anti-squatting.** The first pipe instance is created with the first-instance flag; if creation fails because the name already exists, something else owns the name and the daemon refuses to start and says so [read today: S17† for the flag's behaviour; the squatting argument is inferred].
- **Caller check.** The daemon checks that the connecting process belongs to the same user before accepting a hook or MCP request, the Windows counterpart of the same-uid check. The specific API calls are from memory [UNVERIFIED — spike W3].
- **Code shape.** One `IpcListener`/`IpcStream` abstraction with a Unix-socket implementation and a named-pipe implementation; nothing above it knows which is in use.
- **Loopback console.** Unchanged in design. Whether a loopback listener raises any firewall prompt on Windows is UNVERIFIED.
- **Device keys.** [AD §11.1] named the `keyring` crate with Windows Credential Manager, from memory. Still UNVERIFIED; checked in spike W3 with a file under the user profile and a restrictive ACL as fallback.

### 5.4 The missing sandbox, and what replaces it

Nothing replaces it. That is the honest statement, and the interface makes it: the strip shows **"Sandbox: unavailable on native Windows"** for both the host and every member.

What the absence means: [AD §9.6 R1] says an approved command can do more than its text shows and that the sandbox is the only limit on that. On native Windows there is no limit. A granted `npm test` runs with the user's full rights.

What the design does instead — defence in depth by *narrower permission*, not by containment:

| Measure | What it gives | What it does not give |
|---|---|---|
| **Commands are never auto-allowed by a grant on native Windows, by default.** In Approved Trust on a native-Windows host, `execute` stays ask-every-time. Relaxing this is decision N3. | The owner reads every command before it runs. | Nothing once a command is approved. |
| **Fewer "simple read" shortcuts** (§5.5): on Windows only a short list of built-in PowerShell commands can be classified as reads; any external program is `execute`. | Removes the case where a program in the workspace shadows a familiar name. | More prompts than on macOS and Linux. |
| **Claude Code's own containment switches**, recommended by `coagent doctor`: `permissions.blockReadsOutsideWorkingDirectories` and `permissions.blockWritesOutsideWorkingDirectories` make the file tools refuse paths outside the working directories "in every permission mode"; the write key needs v2.1.314+. | A second, vendor-enforced fence around the file tools. | "The key doesn't limit shell commands, MCP tools, or the programs hooks run" [read today: S14]. |
| **The embedded terminal runs `claude` inside a job object** when the daemon owns the process. A job object manages a process tree as a unit, children join it by default, and it can terminate all of them [read today: S19]. | A reliable **Stop** that ends everything the agent started — better than the Esc-only limitation in an external terminal. | No file or network restriction; the page read today claims none, and I claim none. |
| **Advice, labelled as advice:** for work on a machine the host does not want exposed, use WSL2 (where the sandbox exists [read today: S10†]), a virtual machine, or a disposable environment. | A real boundary. | It is the user's setup, not ours. |

Not in phase 1: running approved commands, or Claude Code itself, in an AppContainer or under a restricted token. AppContainer offers file, network and process isolation [read today: S18], but CoAgent does not launch the agent's commands — Claude Code does — and whether Claude Code can run inside one is unknown [UNVERIFIED]. It is listed for phase 2 with the direct-tools executor, where the daemon does own the process.

### 5.5 Paths and shell classification

**Paths.** The normaliser must turn every spelling of a file into one canonical form before it is compared with a workspace root, an exclusion or a grant. Windows adds spellings that do not exist on POSIX. The list below is from general knowledge and each item is UNVERIFIED until spike W4 has a test for it: case-insensitive names; backslash and forward slash; drive-relative and drive-absolute forms; UNC and device-namespace prefixes; legacy short names; alternate data streams (`file:stream`); reserved device names; trailing dots and spaces; junctions and other reparse points as well as symlinks; and, in Git Bash commands, MSYS-style `/c/…` paths. Design rules that do not depend on the list being complete:

1. Canonicalise by asking the operating system for the final path of the opened object wherever the object exists; for a path that does not exist yet, canonicalise the nearest existing parent.
2. Any path the normaliser cannot canonicalise with certainty is **outside the workspace** (tier T2) — never inside by default.
3. A target containing a stream suffix, a device prefix or a reserved name is T3.
4. Windows counterparts of the credential and hard-deny patterns of [AD §5.1] are defined (user profile credential stores, PowerShell profile scripts in place of shell rc files, `%USERPROFILE%\.claude\**`, the CoAgent data directory). The exact list is produced and tested in M2.

**PowerShell.** A faithful PowerShell parser exists only as a .NET API in `System.Management.Automation.dll` [read today: S22]; using it would mean spawning or hosting PowerShell on the hook path. Claude Code itself "parses the PowerShell AST and checks each command in a compound command independently" and canonicalises common aliases [read today: S14], but that result is not exposed to hooks. Phase 1 therefore does **not** parse PowerShell. It uses a small recogniser written in Rust that accepts exactly one shape — one command name from a fixed list of read-only built-ins (and their standard aliases), followed by plain arguments — and rejects anything containing a variable, a subexpression, a script block, a pipeline, a separator, redirection, a call operator, a backtick escape or an expandable string. Everything rejected is `execute`. This is safe in the only direction that matters: [AD §5.1] already requires that the classifier "only ever *raises* scrutiny". It will ask more often than a real parser would.

**External programs on Windows are always `execute`.** On POSIX [AD] treats `git status` as a simple read. On Windows, how a bare name resolves to a file — search order, the current directory, file-extension lists — differs between PowerShell and cmd and is exactly the kind of rule an edited workspace can exploit; I have not verified those rules today [UNVERIFIED], so the design does not rely on them.

**cmd.** Claude Code has no cmd tool; CMD appears only as a shell the user may launch Claude Code from [read today: S12]. A command that invokes `cmd /c …` from Bash or PowerShell is `execute`, and its inner text is never parsed.

**Git Bash.** The Bash tool under Git for Windows goes through the existing POSIX recogniser, with one extra rule: any path argument is mapped to a Windows path before tiering, and if the mapping is uncertain the command is `execute`.

### 5.6 Code signing

- **Unsigned is not viable as a default.** For a file with no signature, SmartScreen shows "Windows protected your PC" and the "User must choose 'Run anyway'… Enterprise policy can prevent continuation entirely." And "On Windows 11 devices, the Smart App Control feature… will block execution of unsigned files unless the file has a positive reputation", applying "to all executable files, not just those downloaded from the Internet" [read today: S21]. The second point matters for a product whose hook executable runs on every tool call.
- **Signing does not remove the warning at first.** A signed new binary "could still show a SmartScreen warning until its hash or publisher certificate accumulates sufficient evidence"; "it can take several weeks and hundreds of clean installs"; "EV certificates no longer bypass SmartScreen" [read today: S21]. A small beta will see warnings for a long time either way; signing changes *"unknown publisher"* into a named one and lets reputation carry across versions.
- **The route Microsoft recommends for non-Store distribution** is Artifact Signing (formerly Trusted Signing): "Starts at $9.99/month", "Identity validation required", no hardware token, integrates with CI [read today: S20, S21]. Whether an individual (rather than an organisation) in the owner's country is eligible was not established today [UNVERIFIED].
- This costs money and puts a legal identity on the binary. It is the owner's decision (N4). Until it is made, Windows builds are unsigned, labelled as such, and the install instructions say what the user will see.
- The pinned SHA-256 inside the plugin version and the checksums in the release ([AD §7.2, §11.4]) apply to Windows unchanged; they prove integrity to CoAgent's own installer, not to Windows.

### 5.7 Other Windows differences

- **Embedded terminal (D9 a).** The daemon-owned pseudo-terminal uses the Windows pseudo-console. `portable-pty` is at 0.9.0, MIT [read today: S26]; that it supports the Windows pseudo-console, and from which Windows build, is from memory [UNVERIFIED — spike W6]. The structural rule of [AD §6.5] — only keystrokes from the authenticated local console reach that terminal — is unchanged.
- **Wake-up of an idle agent.** The plugin monitor in [AD §3.5] is a shell command; whether plugin monitors run on Windows without Git Bash was not established (the Monitor *tool* needs Git Bash there [read today: S13]) [UNVERIFIED]. The fallbacks already in [AD] — the `Stop`-hook notice and the `wait` tool — are the Windows baseline.
- **Hosting the relay from Windows** (§4): expected to raise a firewall prompt on first listen [UNVERIFIED].
- **Security software.** A new unsigned program that listens on the network, hosts a terminal and is spawned on every tool call may be flagged by endpoint protection [UNVERIFIED]; tried on a clean machine in spike W1.
- **CI.** A Windows runner is added to every job in [AD §11.4]; the nightly real-Claude-Code red tests run on Windows in both configurations of §5.2.

### 5.8 What I could not verify for Windows

Collected in §8, rows W-a to W-m. The two that the design most depends on: that an exec-form `PreToolUse` hook with `onFailure: "block"` behaves on native Windows exactly as on macOS (read in the documentation, not run), and that a named pipe restricted to the logon session can be created from the chosen runtime.

---

## 6. The smaller rulings

### 6.1 D7 — identity: phase 1 as designed, phase 2 with several methods

**Phase 1** is [AD §4.3] unchanged: device keys, local nicknames, verify-words. One addition so that phase 2 does not need a data migration: a contact record holds a **list** of typed identity proofs (empty in phase 1 apart from how the contact was verified, §3.5), and the interface has one place where proofs are shown. Policy continues to key on the device key only; a proof is a label a human reads, never an input to the gate.

**Phase 2 must offer more than one method.** Candidates, named and not chosen. None was verified today; each is a design question for phase 2:

1. Device key with verify-words (remains the base that every other method attaches to).
2. Proof of control of a code-hosting account — a signed statement published under the account.
3. Signature with an SSH key that the person already publishes.
4. Sign-in with an identity provider (OpenID Connect), yielding a provider-signed assertion bound to the device key.
5. Keyless signing certificates from a public transparency-logged authority.
6. A hardware-backed key or passkey as, or bound to, the device key.
7. A certificate issued by the person's organisation.
8. Proof of control of a domain (a DNS record or a well-known file).
9. Vouching: a contact I have verified introduces another — the roster introduction of §3.5 made durable.
10. In-person exchange by scanning a code.

A constraint the phase-2 design must respect because of D3 b: any method that needs a verification server needs one that somebody else already runs, or one the user runs; the project runs none.

### 6.2 D8 — unreviewed beta, indefinitely

**What the product must say.** Plain statements, in these places:

| Where | What |
|---|---|
| README, first screen, under a heading *Security status* | That CoAgent has **not** been reviewed by any independent security specialist and that no review is planned. That it lets other people's text influence an agent on your machine. Which parts are our own untested-by-others construction: pairing, the group roster and introductions, the per-recipient audit log, the gate's policy engine. Which parts are third-party libraries and whether each has had an independent audit — filled in from a checked list, not from memory. What it should not be used for: machines holding production credentials or regulated data, and sessions with people you do not have other reasons to trust. |
| `SECURITY.md` | How to report a problem; that there is no bounty and no guaranteed response time; the supported version. |
| First run, once | A consent screen with the same statement in three sentences. The user types a word to continue; it is not a click-through. |
| Pairing and accept screens, every time | One line: "Unreviewed beta software." Shown to both sides, with the counterpart's version. |
| The strip of the console and `/collaborate status` | The word **BETA** beside the gate level. |
| `coagent --version` and release notes | "beta (not independently reviewed)". |
| Version numbers | Stay below 1.0 for as long as D8 b stands. [AD] tied "1.0" to a review; without one there is no 1.0. |
| The published threat model | The residual risks of [AD §9.6] and §3.7, in full, including the ones that are unflattering. |
| Licence | Apache-2.0 (D2 a) carries a warranty disclaimer; the README points to it rather than restating it. I did not re-read the licence text today [UNVERIFIED]. |

The product must **not** say or imply: "audited", "secure", "end-to-end encrypted" without the qualification that the construction is unreviewed, or "safe to use with untrusted parties".

**Compensating measures the design keeps, and adds.** None of these is a review, and the README says so in one sentence.

| Kept from [AD §11.3–11.4] | Added by this revision |
|---|---|
| Gate red tests against real Claude Code on every release and nightly | The same on native Windows, both configurations |
| Property tests on the policy engine | Property tests on the roster validator and the Windows path normaliser |
| Hostile-relay suite | **Hostile-member suite** (impersonation, role escalation, equivocation, flooding, stale roster) and the third-joiner test (§3.3) |
| Injection corpus | Corpus extended with group cases: observer attempting requests, convener-forged reports about another machine |
| Fuzzing of the wire decoder, hook-JSON parser, shell classifier | Fuzzing of the relay frame parser (now internet-facing), the roster decoder, the PowerShell recogniser, the path normaliser |
| Contract tests against the newest Claude Code nightly | — |
| `cargo-deny`, `cargo-audit`, `gitleaks`, CodeQL | — |
| Mandatory verify-words on first contact | Visible provenance for every introduced member |
| No hand-rolled primitives | A written list of every piece of cryptographic *glue* we wrote, kept in the repository, so a volunteer reviewer knows exactly what to read |
| — | An adversarial read of each milestone's security-relevant diff by a separate agent that did not write it. This is not an independent review and is never described as one. |

### 6.3 D5 — reads in Controlled mode

As [AD §5.1–5.2]: ask on the first read of each file or folder, with the one-click "all reads under here, this session". In a group the approval is per session, not per requester, because the agent's context is shared by everything it has read. Showing what was read to any member remains a separate gated share.

### 6.4 D6 — Approved Trust limits

Default 60 minutes, maximum 8 hours, as [AD §5.3]. The ruling's text covers the durations; the other two parts of [AD]'s D6 recommendation (unattended running available but explicit per grant; a session is never auto-accepted) remain the design's defaults and are listed as assumptions in §10. New for groups: any roster change suspends active grants (§3.6).

### 6.5 D12 — audit content

Hashes plus short redacted previews by default; full capture is an opt-in per session, as in [AD §9.4]. "Short" was not defined in [AD]. Proposal, not ruled: the first 240 characters or 3 lines after redaction, whichever is shorter, fixed in M2. In a group, previews exist only in the *full* tier (§3.9).

### 6.6 Nightly tests on the smallest model

The red tests that drive a real agent run nightly on the smallest current Claude model. I did not look up which model that is today and do not name one [UNVERIFIED — resolved in M0 from the vendor's model list].

One safeguard is needed because of this choice. A red test asserts that a forbidden thing did **not** happen. A small model that simply never attempts the action makes that assertion pass for the wrong reason. So every red test is paired with a **positive control**: the same prompt under an allow decision must produce the action, and the denied run must show a `PreToolUse` event for that exact tool call in the hook stream. A run where the model never tried is reported **INCONCLUSIVE**, not green, and three inconclusive nights in a row on one case raise an alarm. Tests that need no model — the replay harness on pull requests, all group, relay and protocol tests — are unaffected.

### 6.7 Language, build model

Rust core and a TypeScript console, as [AD §11]. Build model: Fable for the M0 spikes, then the routing table — a process ruling with no design consequence.

### 6.8 Repository, licence, and the old tree

- A new private repository under the owner's personal GitHub, with the old tree copied in as `legacy/`.
- **Import rule for `legacy/`.** The copy excludes every `.env*` file and key directory, and the import commit is made only after the secret scanner passes on it. This is the workspace rule that secrets are never committed, applied to an import; per D4 c nothing else is planned or proposed for the old tree.
- `legacy/` is reference only. No code is ported from it [AD §12], and CI does not build it.
- **Interaction to resolve (decision N6):** D2 a says free and Apache-2.0; the repository is private. A plugin marketplace that lives in a private repository can only be installed by people with access to it, and a security tool that asks for trust while unreviewed leans on its source being readable. When the repository becomes public is the owner's call.

---

## 7. Revised delivery plan

### 7.1 Revised §12 — milestones

Effort is in agent-days as defined in [AD §12] and is an estimate. Two-party work is not a separate track: every structure is built for N from M1 and exercised at N = 2 first.

| # | Milestone | What exists at the end | Acceptance test (demonstrable) | Estimate | Was |
|---|---|---|---|---|---|
| **M0** | **Spikes and housekeeping** | Throwaway code answering every row of §7.2; results table; new repository created with `legacy/` imported through the filter; decisions N1–N8 taken or defaulted. | Each spike is marked pass, fail-with-fallback, or fail-blocking. A fail-blocking result on G1, W1 or C1 stops the plan for a decision. | 5–7 | 2–3 |
| **M1** | **Walking skeleton, three platforms** | Two daemons; link pairing; relay started by a participant on loopback and on a LAN; pinned relay certificate; IPC abstraction with Unix-socket and named-pipe back ends; MCP `send`/`inbox_read`/`wait`; key state keyed per peer from the first commit. | macOS ↔ Windows and Linux ↔ Windows exchange a request and a reply through a participant-run relay; the relay log shows ciphertext only; the key-substituting relay cannot complete a handshake. | 6–8 | 4–6 |
| **M2** | **The gate — CONTROLLED, terminal-only, two parties** | [AD] M2 content, plus: exec-form hook on Windows in both configurations; Windows path normaliser; PowerShell recogniser; `find`/`grep` forms in the POSIX recogniser. | The full red-test list of [AD §11.3] green on macOS, Linux and native Windows (with and without Git for Windows), each with its positive control. `coagent audit verify` passes on both sides. | 8–11 | 5–7 |
| **M3** | **Groups and observers** | Roster and its validator; mesh channels over the multi-slot relay; roles enforced at the decoder; per-member accept and share levels; request addressing; N-party envelope; per-author chains with tiers, head exchange and equivocation detection; removal; terminal flows. | Three-party and eight-party sessions on the loopback relay. Third-joiner test passes. Hostile-member suite green. An observer's request is rejected at the decoder. A removed member receives nothing after every remaining member has acknowledged. Two members' audit bundles verify together; a deliberately equivocating test member is caught with evidence. | 10–14 | new |
| **M4** | **Browser console — CONTROLLED, including groups** | [AD] M3 content, plus roster strip, People tab, per-member share controls, requester attribution on cards, observer view. | The M2 and M3 demos driven from the browser on all three platforms; switching between terminal and browser loses no state; every local-web attack test refused. | 8–12 | 6–8 |
| **M5** | **APPROVED TRUST** | [AD] M4 content, plus grant subjects, roster-change suspension, and the native-Windows rule for commands (per N3). | A 30-minute trust session with three members: in-scope actions flow; a credential read still prompts; a member joining suspends the grant; Revoke takes effect on the next tool call (measured); the exported bundle verifies offline. On Windows a command still asks unless N3 allowed otherwise. | 6–9 | 5–7 |
| **M6** | **Beta release** | Embedded terminal on all three platforms; packaging and (per N4) signing; installer-first flow on Windows; relay profiles, invite candidates, `coagent doctor net`; connectivity recipes with last-tried dates; every disclosure of §6.2; reconnect soak; private beta. | **Two timed onboarding tests, times reported not targeted:** (1) two people on one network, from nothing installed to a linked session; (2) two people on different networks with a relay one of them already had. A two-hour, four-member session with injected drops completes with intact, mutually verifying logs. The README's security-status section matches the facts on the day. | 10–14 | 6–8 |
| | **Phase 1 total** | | | **≈ 53–75 agent-days (estimate)** | **28–39** |
| **M7** | **Phase 2a — other makers** | As [AD] M6, plus the first additional identity methods (D7). | As [AD] M6. | 8–12 + identity UNESTIMATED (methods not chosen) | 8–12 |
| **M8** | **Phase 2b and later** (each separately scoped) | Direct guest tools with a sandboxed executor (including a Windows containment design); phone as owner device; A2A gateway; convener hand-over; a cap above 8 (MLS re-evaluation); optional peer-to-peer transport. | Per item. | 10–15+ | 10–15+ |

Removed from the plan by rulings: withdrawing the old download and the associated steps ([AD §12] items 1–3; D4 c); operating a public relay and a join page (D3 b); "external review findings closed" as an M5 condition (D8 b).

### 7.2 Revised M0 spike list

Build model for these: Fable (ruling). Each spike has a pass/fail criterion; "fallback" is what the design does on a fail.

**From [AD] Appendix B** (U11 and U14 are not M0 spikes: U11 is read at M7; U14's relay-cost half is void under D3 b and its review-price half is void under D8 b; U15 needs no test).

| # | Question | Pass criterion | Fallback on fail |
|---|---|---|---|
| B1 (U1) | Does the interactive permission dialog stay live while a `PermissionRequest` hook is pending? | With a hook that waits 20 s, an answer from either the terminal or the hook is accepted and the other is cancelled cleanly, 5 runs of 5. | One approval surface at a time. |
| B2 (U2) | What does a `PreToolUse` `ask` do in `bypassPermissions` and `dontAsk`? | Behaviour observed and recorded for each mode; pass = a prompt appears or the call is denied; **fail = the call runs**. | Never return `ask` in those modes (already the design). |
| B3 (U3) | Does a monitor line wake an idle agent, and across `/compact` and `--resume`? | Agent acts on the notice within 10 s in 9 of 10 trials on macOS and Linux. | `Stop`-hook notice, `wait`, or the human. |
| B4 (U4) | MCP elicitation: is a dialog shown that the model cannot answer? | Dialog renders; a model instructed to answer it cannot; result returns to the tool. | Console-only confirmations. |
| B5 (U5) | Skill-frontmatter hooks: `onFailure` honoured, and do they survive `--resume`? | Both observed true. | Plugin-level hooks (the baseline). |
| B6 (U6) | `ConfigChange` hook decision fields. | A settings edit that disables hooks is blocked during a session. | Hard-deny on config paths + liveness invariant. |
| B7 (U7) | `snow`: do `XXpsk3` and `KK` with the chosen suite build and round-trip? `spake2`: round-trip and RFC 9382 vectors. | Both handshakes complete in a test; a wrong PSK fails; vectors match. (Read today: the pattern and PSK-modifier types exist in `snow` 0.10.0 [S8]; the round-trip is still untested.) | A different PSK placement, or PAKE → HKDF → `XX` with the key in the prologue. |
| B8 (U8) | MCP tool-call timeout ceiling for `wait`. | Ceiling measured. | 120 s polls. |
| B9 (U9) | Can a plugin detect that the Claude Code sandbox is on? | A reliable signal found in hook input or environment. (Read today: the docs describe only the `/sandbox` panel, no programmatic flag [S10†].) | Owner-ticked checkbox and a doctor check. |
| B10 (U10) | Are hook-originated `ask` prompts forwarded by Remote Control? | One manual test shows the prompt on the phone. | Phone approval waits for M8. |
| B12 (U12) | Binary delivery through the plugin shim on macOS and Linux. | Shim downloads, verifies and runs the pinned binary on both. | Separate installer (which Windows uses regardless). |
| B13 (U13) | Licences marked "from memory" in [AD §11.1]. | `cargo-deny` passes with the allow-list. | Swap the dependency. |
| B16 (new, all platforms) | Searches on macOS/Linux arrive as `Bash` `find`/`grep` calls [read today: S13]. What exact command forms? | 20 recorded search calls are all classified `search` by the recogniser, and no non-search command is. | Searches are `execute` prompts until the recogniser is extended. |
| B17 (new) | Which is the smallest current model, and do red tests with positive controls run reliably on it? | Model identified from the vendor list; 10 consecutive runs of 3 red tests with 0 inconclusive. | Next model up for nightly; cost re-estimated. |

**Group cryptography (D11 b).**

| # | Question | Pass criterion | Fallback on fail |
|---|---|---|---|
| G1 | Mesh over one relay socket: 3 members, pairwise `KK` from a signed roster, frames routed by slot. | All three pairs exchange messages; a frame for pair (A,B) cannot be opened by C; a handshake from a key not on the roster is refused; A↔B continue uninterrupted when C joins. | **Blocking.** Without this the recommendation falls; re-evaluate hub or MLS before M1. |
| G2 | Cost at the cap: 8 members. | Time for the eighth member to reach "connected to all", and time to fan one 4 KB event out to 7, both measured on one machine; recorded, with a pass line of under 5 s and under 100 ms respectively (proposed, to be confirmed against the measurement). | Lower the cap. |
| G3 | Removal and roster lag. | After a signed removal, no remaining member's daemon emits a frame to the removed slot once it has acknowledged; a member held back by the test relay is shown as unconfirmed to the convener. | Redesign acknowledgement. |
| G4 | Desk analysis, no code: how strong are short verify-words on an **introduced** pair against a convener who is also the relay? | A written argument, with the attack cost stated, that either (a) the plain handshake-hash words suffice within a stated deadline, or (b) names the commit-then-reveal change needed. | Introduced pairs stay "unverifiable in phase 1" and the interface says so; grants never name them. |
| G5 | OpenMLS sanity check, time-boxed to half a day, so the rejection in §3.1 rests on more than reading. | A 3-member group is created; one member is removed and cannot decrypt the next message; the hours of glue needed for per-recipient disclosure are estimated. | None needed — informational. If it shows the glue is small, revisit §3.2 before M3. |

**Native Windows (D10 b).**

| # | Question | Pass criterion | Fallback on fail |
|---|---|---|---|
| W1 | The gate on native Windows, both configurations (with and without Git for Windows), with an exec-form hook calling a stub `.exe`. | In each configuration and in default and bypass modes: a denied `Write` creates no file; a denied `PowerShell` command does not run; a killed stub blocks the call; a missing executable blocks the call. No security-product block of the stub on a clean machine. | **Blocking** for D10 b: without a fail-closed hook on Windows there is no gate there. |
| W2 | Install order: installer-first with the hook resolved on `PATH`, versus a shim. | A user with only Claude Code reaches a working hook with one installer run, and uninstalling leaves no blocking hook behind. | Ship a shell-form shim per shell and accept the complexity. |
| W3 | Named-pipe IPC: explicit security descriptor for the logon session, first-instance flag, same-user caller check; device key in the credential store. | A process running as a second user cannot open the pipe; a second daemon cannot create it; hook round-trip under 20 ms median (measured); key stored and read back. | Loopback TCP with a per-user secret file (weaker; would need its own review of [AD §9.1 row D]). |
| W4 | Path normaliser: one test per spelling class in §5.5. | Every class either canonicalises to the same path or is classed outside the workspace; none is classed inside wrongly. | Treat all non-trivial paths as T2 on Windows. |
| W5 | Can the relay process be confined (AppContainer or restricted token) as an unpackaged executable? | Relay serves a session while unable to read the user's profile directory. | Relay runs unconfined on Windows, stated in the docs. |
| W6 | Embedded terminal: pseudo-console hosting interactive `claude`, inside a job object. | `claude` is usable in the browser terminal; Stop terminates the whole process tree. | External-terminal only on Windows for the beta. |

**Connectivity (D3 b).**

| # | Question | Pass criterion | Fallback on fail |
|---|---|---|---|
| C1 | Participant-run relay with a self-generated certificate pinned from the invite; raw IP address, no domain. | Joiner connects only when the fingerprint matches; a relay presenting another certificate is refused; works on a LAN between two machines. | **Blocking** for the port-forward and LAN paths as designed; fall back to plain WebSocket with a Noise handshake to the relay. |
| C2 | Do the relay's WebSocket connections pass through Tailscale Funnel and through a Cloudflare quick tunnel? | A two-party session completes through each, for 30 minutes, with one forced reconnect. Each result recorded separately. | Remove the failing recipe from the documentation. |
| C3 | Network-namespace test rig on Linux CI: two private networks and a relay on a third. | A two-party and a three-party session pass in CI on the rig; a variant with one path blocked fails with the intended error text. | Cross-network cases stay on the manual checklist. |
| C4 | Invite with several relay candidates, and a saved relay profile making the short code usable. | Joiner falls through a dead first candidate to a live second within 10 s and reports why the first failed; with a shared profile, the spoken-code flow of [AD §4.1] completes. | Single-candidate invites. |

### 7.3 Revised phase-1 estimate

All figures are agent-days and are estimates built from the component lists in §3, §4 and §5, not from measurement.

| Line | Original | Delta | Attributed to | Basis |
|---|---|---|---|---|
| [AD] phase 1 as designed | 28–39 | — | — | [AD §12] |
| Group crypto, roster, multi-slot relay | | +3 to +4 | D11 b | §3.5, §3.8 |
| N-party envelope, per-pair ack/replay, roster sync, removal | | +1.5 to +2 | D11 b | §3.8 |
| Roles, per-member accept and share levels, request addressing, grant subjects | | +2 to +3 | D11 b | §3.4, §3.6 |
| Audit chains with tiers, head exchange, equivocation, group export/verify | | +2 to +3 | D11 b | §3.9 |
| Group interface in console and terminal | | +2.5 to +3.5 | D11 b | §3.6 |
| Group tests (hostile member, third joiner, removal, 8-daemon soak) and spikes G1–G5 | | +2 to +2.5 | D11 b | §6.2, §7.2 |
| **Subtotal D11 b** | | **+13 to +18** | | |
| Installer, install order, packaging, signing pipeline | | +1 to +1.5 | D10 b | §5.2, §5.6 |
| Named-pipe IPC, daemon lifecycle, key storage | | +1.5 to +2 | D10 b | §5.3 |
| Path normaliser, PowerShell recogniser, Windows pattern lists, their tests | | +2 to +3 | D10 b | §5.5 |
| Hook path and red tests in two Windows configurations; spikes W1–W6 | | +1.5 to +2 | D10 b | §5.1, §7.2 |
| Embedded terminal on Windows, job object | | +0.5 to +1 | D10 b | §5.7 |
| Windows CI | | +0.5 | D10 b | §5.7 |
| **Subtotal D10 b** | | **+7 to +10** | | |
| Embedded participant-run relay as a separate process, certificate pinning, multi-candidate invites, relay profiles, contact relay memory | | +2 to +3 | D3 b | §4.3, §4.4 |
| `doctor net`, connectivity recipes, namespace test rig, spikes C1–C4 | | +2 to +3 | D3 b | §4.5, §4.6 |
| Removed: public relay deployment and operations, join page | | −1 | D3 b | §4.1 |
| **Subtotal D3 b** | | **+3 to +5** | | |
| Disclosures; extra fuzz targets and property tests; glue inventory; adversarial read per milestone | | +1 to +2 | D8 b | §6.2 |
| Identity-proof list in the contact record and one display place | | +0.5 | D7 | §6.1 |
| D1, D2, D5, D6, D9, D12, language, build model | | 0 | — | matched [AD]'s defaults |
| D4 c | | 0 | — | the removed steps were owner actions, not agent-days |
| Repository and `legacy/` import | | counted inside M0 | — | §6.8 |
| **Total delta** | | **+24.5 to +35.5** | | |
| **Revised phase 1** | **28–39** | | | **≈ 53–75** |

**Lines I cannot estimate.**

- **The combination matrix — UNESTIMATED.** Groups × three platforms × three relay arrangements is far more configurations than the per-ruling sums cover. How much of it needs its own tests is not knowable before M2 and M3 show which behaviours actually differ by platform. To be estimated at the end of M3.
- **Nightly model cost — UNESTIMATED.** Depends on the model identified in B17, the number of red tests, and three platforms. It is a running cost in tokens, not agent-days.
- **Phase-2 identity methods — UNESTIMATED.** The methods are not chosen (D7).
- **Calendar time.** Not estimated. It depends on the owner's decisions in §9, on identity validation for signing if N4 is yes, and on review of each milestone.
- **Rework if a blocking spike fails (G1, W1, C1) — UNESTIMATED.** By definition the design after such a failure is not this one.

---

## 8. UNVERIFIED after this revision

Every mechanism this revision leans on that I did not verify today. [AD] Appendix B rows that still stand are referenced by their spike in §7.2 and not repeated, except where today's reading changed them.

| # | Unverified mechanism | Where it is used | What settles it |
|---|---|---|---|
| G-a | `snow` 0.10.0 accepts and round-trips the exact `XXpsk3` and `KK` parameter strings; API for prologue and rekey. (Types read today; no code run.) | §3.5, §3.8 | Spike B7 / G1 |
| G-b | Mesh of `KK` channels multiplexed by slot over one relay socket behaves as designed. | §3.2 | Spike G1 |
| G-c | Strength of short verify-words on introduced pairs against a convener who is also the relay; correctness of a commit-then-reveal variant. Also applies to the composition [AD §4.2] already flagged as inference. | §3.5, R10 | Spike G4 (desk analysis). Not settled by any test; under D8 b nobody outside will check the argument. |
| G-d | The cap of 8 is comfortable (join time, fan-out). | §3.2 | Spike G2 |
| G-e | The salted tier-commitment audit construction and head-exchange equivocation detection are sound. My own design, reasoned not proven. | §3.9 | Hostile-member suite in M3; no outside review (D8 b) |
| G-f | OpenMLS audit status, advisories and exact audited versions. Search-result level only. | §3.1 | Read the audit report and the advisory database (spike G5) |
| G-g | A Megolm implementation in `vodozemac`; its licence and audit status. From memory. | §3.1 | crates.io and the project's own documentation — only matters if option B is ever reconsidered |
| G-h | RFC 9420 and RFC 9750 quotations were relayed by a summarising fetch (†); section numbers and wording to be re-opened before being quoted elsewhere. | §3.1 | Re-open the RFC text |
| C-a | WebSocket connections pass through Tailscale Funnel and through Cloudflare quick tunnels. Neither page says. | §4.2 | Spike C2 |
| C-b | Certificate-fingerprint pinning for a self-generated certificate with the Rust TLS stack. | §4.2, §4.4 | Spike C1 |
| C-c | How often port forwarding is impossible (carrier-grade NAT, corporate networks); hole-punching success rates. | §4.2 | A published measurement study; not a spike. The design does not depend on a number. |
| C-d | Who operates iroh's shared relays and discovery services, on what terms; whether they can be switched off. | §4.2, N5 | iroh's documentation, read in full, if N5 is answered "yes" |
| C-e | Network namespaces are usable on hosted CI runners for the test rig. | §4.6 | Spike C3 |
| C-f | Time to first session in each situation of §4.5. | §4.5, M6 | Measured in M6 |
| W-a | An exec-form `PreToolUse` hook with `onFailure: "block"` behaves on native Windows as documented, in both configurations and in bypass mode. Read, not run. | §5.1, §5.2 | Spike W1 |
| W-b | Hook-documentation quotations for Windows were relayed by a summarising fetch (†). | §5.1 | Re-open the page before pinning field names |
| W-c | The API calls for the pipe's security descriptor, the caller's identity check and the server check; that the logon-session restriction works from the chosen runtime. | §5.3 | Spike W3 |
| W-d | Unix-domain sockets on Windows: Rust support and peer-credential equivalent. From memory. | §5.3 | Not needed if W3 passes |
| W-e | Why a Windows service is unsuitable (session isolation details). From memory. | §5.3 | Microsoft's service documentation — the decision does not hinge on it |
| W-f | `keyring` crate and Windows Credential Manager. From memory, as in [AD]. | §5.3 | Spike W3 |
| W-g | Every Windows path-spelling class in §5.5, and the API used to obtain a final path. From memory. | §5.5 | Spike W4 |
| W-h | How PowerShell and cmd resolve a bare program name. From memory; the design avoids relying on it. | §5.5 | Microsoft documentation, if the Windows read shortcuts are ever widened |
| W-i | Firewall prompts for loopback and non-loopback listeners; behaviour of endpoint protection towards the binary. | §5.3, §5.7, §4.2 | Spike W1 on a clean machine |
| W-j | `portable-pty` supports the Windows pseudo-console and from which Windows build. (Version and licence read today.) | §5.7 | Spike W6 |
| W-k | Plugin monitors on Windows without Git Bash. | §5.7 | Spike B3 repeated on Windows |
| W-l | AppContainer or restricted token usable for the relay as an unpackaged executable; whether Claude Code could run inside one. | §4.4, §5.4 | Spike W5 (relay only) |
| W-m | Artifact Signing eligibility for an individual in the owner's country; total cost; WinGet submission requirements; ARM64 Windows CI runners. | §5.2, §5.6, N4 | Microsoft's pricing and eligibility pages; the WinGet repository's contribution rules |
| O-a | Which model is "the smallest" today and whether it drives the red tests reliably. | §6.6 | Spike B17 |
| O-b | Apache-2.0's warranty-disclaimer wording. Not re-read today. | §6.2 | Read the licence text when the README is written |
| O-c | Whether a plugin marketplace in a private repository can be installed by a collaborator with repository access, and how. | §6.8, N6 | Claude Code plugin install documentation; one manual test |
| O-d | The ten phase-2 identity candidates — existence, maturity and fit of each. Named from general knowledge. | §6.1 | Phase-2 design research |
| O-e | Every proposed constant in this document (relay buffer caps, preview length, G2 pass lines, timeouts). Chosen, not measured. | throughout | Set from measurements in M1–M3 |

---

## 9. New owner decisions

Decisions that only the owner can make and that the rulings create. Each has a recommendation and the default the plan assumes if nothing is said. Approval-class items (money, public posture) are marked ⚑ and are never acted on by default.

| # | Question | Options | Recommendation | Default if unanswered | Created by |
|---|---|---|---|---|---|
| **N1** | **How many parties may a phase-1 session hold?** | (a) 8; (b) a smaller number such as 4; (c) no fixed cap. | (a). (c) is not compatible with the recommended design. | (a): 8, subject to spike G2. | D11 b |
| **N2** | **Who may bring a new person into a session?** | (a) only the person who started it, and each machine's owner then separately accepts the newcomer; (b) any member may invite, same acceptance; (c) the starter invites and newcomers are visible to everyone at once at a default level. | (a). Admission and access stay separate, and there is one writer of the member list. | (a). | D11 b |
| **N3** | **On native Windows, where no sandbox exists, may an Approved Trust grant let commands run without asking?** | (a) never in phase 1 — commands always ask on Windows; (b) yes, but only exact commands the owner ticks, with a per-grant acknowledgement that nothing contains them; (c) same rules as macOS and Linux. | (b): it keeps trust mode useful for running tests on Windows while forcing the owner to read each command once. Not (c). | (a) — the safer one. | D10 b |
| **N4** ⚑ | **Sign the Windows binaries?** Signing costs a monthly fee and requires validating a legal identity that then appears as the publisher. Unsigned binaries trigger "Windows protected your PC" and may be blocked outright on some Windows 11 machines. | (a) sign through Microsoft's signing service; (b) sign with a certificate from another authority; (c) ship unsigned, labelled, with instructions. | (a) before any Windows build goes to a person outside the private beta, once eligibility is confirmed. | (c) for internal builds only; no Windows build is distributed outside the private beta unsigned without the owner's word. | D10 b |
| **N5** | **May a later version depend on a third party's free public rendezvous servers to connect people directly?** It would bring back "it just connects" for many networks, at the cost of every session depending on a service neither the owner nor the user controls. | (a) no — self-hosted or user-supplied reachability only; (b) yes, as an opt-in the user switches on; (c) yes, as the default. | (a) for phase 1; revisit (b) at M8 with the terms of the service in hand. | (a). | D3 b |
| **N6** | **When does the private repository become public?** Free and Apache-2.0 (D2 a) cannot reach anyone, and the plugin cannot be installed by a stranger, while the repository is private. | (a) public from the first commit; (b) private until the gate's red tests are green (end of M2), then public; (c) private until the beta release (M6); (d) private indefinitely, invite-only beta. | (b): nothing is published before the gate is demonstrably real, and the unreviewed code is readable well before anyone is asked to trust it. | (c) — nothing is made public without the owner's word. | D2 a with the repository ruling |
| **N7** ⚑ | **Approve the wording of the security-status disclosure** (§6.2) — the product will say publicly, in the owner's name, that it is unreviewed and what it should not be used for. | (a) approve the obligations as listed, wording drafted at M6 for sign-off; (b) soften; (c) strengthen (for example, refuse to run until a longer statement is acknowledged). | (a). (b) would undercut the one honest mitigation D8 b leaves. | (a) for planning; the text is not published without sign-off. | D8 b |
| **N8** | **Release order, now that phase 1 is about twice the size.** | (a) one beta at M6 with everything; (b) a private two-party checkpoint for the owner's own use at the end of M2, then the full beta at M6; (c) a public two-party beta first, groups and Windows as updates. | (b): the proven core is in the owner's hands early without publishing a product that is missing two ruled features. | (b). | D10 b and D11 b together |

---

## 10. Assumptions this revision makes

Stated so they can be corrected. None is a ruling.

1. The four rulings of 23:04 (D2 a, D3 b, D4 c, go a) are final and replace the "still open" list; this revision treats no decision in [AD §13] as open.
2. "No public relay" also excludes a project-hosted static join page and a project domain. If a static page on a code-hosting site is acceptable, it is additive and changes nothing here.
3. The parts of [AD]'s D6 recommendation not quoted in the ruling stand: unattended trust exists but is explicit per grant; a session is never accepted without a human.
4. The parts of [AD]'s D12 option (a) not quoted in the ruling stand: full capture is an opt-in per session.
5. An owner's own approval devices (the phone of [AD §6.7], not built in phase 1) do not count toward the cap.
6. If the convener leaves, the session continues with a frozen member list; hand-over is phase 2.
7. Both native-Windows configurations (with and without Git for Windows) are in scope. WSL2 remains supported as a Linux target.
8. Phase 1 remains "instruct only": no member executes anything on another's machine [AD §2.3]. Groups do not change that.
9. `legacy/` is imported through the secret filter and never built.

---

## Appendix A — sources read on 2026-11-16

All accessed 2026-11-16. † = the fetch tool returned a summary with quotations rather than the raw page; quoted sentences are as relayed.

| Ref | Source | What was checked |
|---|---|---|
| **S1** † | RFC 9420, The Messaging Layer Security (MLS) Protocol — https://www.rfc-editor.org/rfc/rfc9420.txt (read in three parts) | Forward secrecy and post-compromise security (§1); epoch secret restricted to current members (§3.1); new members cannot read earlier messages, Remove gives fresh entropy to all but the removed member (§3.2); trusted Authentication Service, largely untrusted Delivery Service (§3); credentials (§5.3); per-message signature verification (§6.1); pre-shared keys (§8.4), exporter (§8.5), epoch authenticator (§8.7); Remove requires a path (§12.4); external commits (§12.4.3.2); conflicting Commits "MUST have an established way to resolve" (§14); insider fragmentation (§16.12); mandatory cipher suite `MLS_128_DHKEMX25519_AES128GCM_SHA256_Ed25519`, 0x0001 (§17.1); logarithmic scaling (§1, §4). |
| **S2** † | RFC 9750, The MLS Architecture — https://www.rfc-editor.org/rfc/rfc9750.txt (first 100,000 characters; §8.5–8.7 not read) | One Commit per epoch; strongly consistent delivery service breaks ties (§5.2, §5.2.1); what a compromised delivery service can and cannot do (§5, §8.4.2); malformed commits and forked views (§5.3); weak sender authentication from the group key alone, signature required (§8.3.1.1); access control is the application's job (§3.5); no history for new clients (§6.7); Authentication Service compromise (§4, §8.4.3). |
| **S3** † | crates.io API — https://crates.io/api/v1/crates/openmls | `openmls` max version 0.9.2, published 2026-10-22, MIT; 0.8.3 published the same day. |
| **S4** † | OpenMLS README — https://raw.githubusercontent.com/openmls/openmls/main/README.md ; book front page https://book.openmls.tech/ | Implements RFC 9420; three cipher suites including the mandatory one; `x86_64-pc-windows-msvc` built and tested in CI; no audit or readiness statement in the README. |
| **S5** | Web search, "OpenMLS security audit report" | Search-result level only: an audit announcement and two 2026 advisories are reported by secondary pages. Not opened at source. |
| **S6** † | Megolm specification — https://gitlab.matrix.org/matrix-org/olm/-/raw/master/docs/megolm.md | Limitations: replays, no transcript consistency, no backward secrecy, partial forward secrecy, dependence on a secure peer-to-peer channel; Ed25519 per-message signatures; no membership-change rules. |
| **S7** † | The Noise Protocol Framework, revision 34, 2018-07-11 — https://noiseprotocol.org/noise.html (first 100,000 characters) | `KK` and `XX` patterns (§7.1, §7.5); PSK modifiers and listed patterns including `XXpsk3`, `KKpsk0`, `KKpsk2` (§9); handshake hash for channel binding (§11.2); rekey (§11.3). |
| **S8** † | docs.rs, `snow` 0.10.0 — https://docs.rs/snow/latest/snow/params/enum.HandshakePattern.html and …/enum.HandshakeModifier.html | `HandshakePattern` includes `KK` and `XX`; `HandshakeModifier` has `Psk(u8)` and `Fallback`. |
| **S9** † | crates.io API — https://crates.io/api/v1/crates/snow | `snow` 0.10.0, 2025-07-19, Apache-2.0 OR MIT. |
| **S10** † | Claude Code docs, Sandboxing — https://code.claude.com/docs/en/sandboxing (first 100,000 characters) | Sandbox on macOS, Linux, WSL2; unsandboxed on native Windows; `failIfUnavailable`; hooks, MCP servers and file tools run outside it; no programmatic status flag described. |
| **S11** † | Claude Code docs, Hooks — https://code.claude.com/docs/en/hooks (characters 0–200,000 of 293,529) | `shell` field; Git Bash or PowerShell for shell-form hooks on Windows; exec form and the `.exe` requirement; `onFailure` and v2.1.295; fail-to-block behaviour on Windows without Git Bash; PowerShell tool input fields; `Bash\|PowerShell` matcher; backslash paths in hook input on Windows; `PermissionRequest` behaviour. |
| **S12** | Claude Code docs, Advanced setup — https://code.claude.com/docs/en/setup (raw page text) | Windows 10 1809+/Server 2019+, x64 or ARM64; install commands; no Administrator needed; Git for Windows optional; native Windows sandboxing "Not supported"; Authenticode signature on `claude.exe`. |
| **S13** | Claude Code docs, Tools reference — https://code.claude.com/docs/en/tools-reference (raw page text, read by line) | PowerShell tool availability, `pwsh.exe`/`powershell.exe` detection, execution-policy handling, limitations (profiles not loaded, no sandbox on Windows); Glob/Grep default tool set per platform; Monitor tool needs Git Bash on Windows. |
| **S14** | Claude Code docs, Configure permissions — https://code.claude.com/docs/en/permissions (raw page text, read by line) | PowerShell rule matching, alias canonicalisation, AST parsing of compound commands; `blockReadsOutsideWorkingDirectories` / `blockWritesOutsideWorkingDirectories` and their stated limits; hook decisions do not bypass deny/ask rules. |
| **S15** | Claude Code docs, Plugin manifest reference — https://code.claude.com/docs/en/plugins-reference (raw page text) | `${CLAUDE_PLUGIN_DATA}` location and persistence; where variables resolve; path separators on Windows; `bin/` on the Bash tool's `PATH`; monitor `command` is a shell command. |
| **S16** | Microsoft Learn, Named Pipe Security and Access Rights — https://learn.microsoft.com/en-us/windows/win32/ipc/named-pipe-security-and-access-rights (raw) | Default security descriptor grants read to Everyone and anonymous; logon SID on the DACL to exclude other sessions. |
| **S17** † | docs.rs, tokio 1.54.1 — https://docs.rs/tokio/latest/tokio/net/windows/named_pipe/struct.ServerOptions.html | `first_pipe_instance`, `reject_remote_clients` (remote clients disabled by default), `create_with_security_attributes_raw`, `max_instances`. |
| **S18** | Microsoft Learn, AppContainer isolation — https://learn.microsoft.com/en-us/windows/win32/secauthz/appcontainer-isolation (raw) | File, network (including "acting as a server"), process and credential isolation. |
| **S19** | Microsoft Learn, Job Objects — https://learn.microsoft.com/en-us/windows/win32/procthread/job-objects (raw) | Process tree managed as a unit; children associated by default; terminate all; kill on close. No claim of file or network restriction on the page. |
| **S20** | Microsoft Learn, What is Artifact Signing? — https://learn.microsoft.com/en-us/azure/artifact-signing/overview (raw) | Managed signing service; identity validation and certificate profile; Basic and Premium SKUs. |
| **S21** | Microsoft Learn, SmartScreen reputation for Windows app developers — https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/smartscreen-reputation (raw) | Behaviour for unsigned, self-signed, OV/EV-signed and Store apps; EV no longer bypasses; Artifact Signing "Starts at $9.99/month"; reputation timescale; Smart App Control. |
| **S22** | Microsoft Learn, `Parser.ParseInput` — https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.language.parser.parseinput (raw) | The PowerShell parser is a .NET API in `System.Management.Automation.dll`. |
| **S23** † | Tailscale docs, Funnel — https://tailscale.com/kb/1223/funnel | Ports 443/8443/10000; relay cannot decrypt; requirements; bandwidth limits; Serve versus Funnel. WebSockets not mentioned. |
| **S24** † | Cloudflare docs, Quick Tunnels — https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/do-more-with-tunnels/trycloudflare/ | No account; testing and development only; no uptime guarantee; 200 in-flight requests; no SSE; hostname changes. WebSockets not mentioned. |
| **S25** † | iroh — https://docs.iroh.computer/ and https://crates.io/api/v1/crates/iroh | Direct connections with relay fallback; shared, dedicated or self-hosted relays; QUIC; `iroh` 1.4.1, 2026-10-21, MIT OR Apache-2.0. Operator of shared relays not stated on the page read. |
| **S26** † | crates.io API — https://crates.io/api/v1/crates/portable-pty | `portable-pty` 0.9.0, 2025-02-11, MIT. |

Local files read today: `00_requirements.md` (whole), `03_architecture-design.md` (whole, 1,011 lines), `01_existing-code-review.md` (finding S9 and the lines around it, by search), `02_prior-art-research.md` (the MLS, sandbox and Windows passages, by search). No credential files were opened. No project code was run.
