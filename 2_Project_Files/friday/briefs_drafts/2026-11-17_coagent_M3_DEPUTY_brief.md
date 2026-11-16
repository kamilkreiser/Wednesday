This brief is from Friday (Kam's laptop coordinator seat). Client: General (Kam's personal project). Project: CoAgent. You are the DEPUTY seat. Your report is the STATUS file named in section 8; Friday reads it at source.

# CoAgent — DEPUTY seat: the starter's deputy, a second signed list that never writes the roster (crate `coagent-roster`)

**This lane starts only after branch `m3-roster` has passed its gate and merged to `main`.** If you are reading this and `main` does not hold the roster lane's work (section 2 says how to tell), write BLOCKED in STATUS and wait.

## 0. Authority (provenance)

- The build grant: Kam typed "yes, keep building today" in Friday's terminal; card `general-c2c-morning-plan-1117` = a. The grant row is the first row of `/Volumes/Laptop-DEV/FRIDAY/0_Brain/tasks/EXPIRING-GRANTS.md`; read that row and nothing else in that file. It ends at the end of Tuesday 2026-11-17: if that date has passed when you start, the grant is dead; write BLOCKED and wait for Friday. Limits: no deploy, no publish, no spend. The repository stays private (card `general-c2c-repo-public-cleanup-1117` = c).
- The ruling this lane builds, Kam, live board 2026-11-17, verbatim: "Decision general-c2c-deputy-powers-1117: a — Build the small deputy as described". The option's text on the card: "Build the small deputy as described — Lets in proposed people only, provisionally, into seats the starter set aside". The description he ruled on, in Friday's words to him: the starter remains the only one who writes the member list; the deputy can only let in someone another member proposed, only into seats the starter set aside for it, and only while the deputy cannot reach the starter; people let in that way are provisional and the starter keeps or drops them on return; the deputy cannot remove anyone, raise the limit, end the session or name another deputy. He did NOT choose "the deputy should be able to do more".
- Before it, same day, verbatim: "Decision general-c2c-i5-starter-gone-1117: b — The starter can name a deputy".
- Model: opus level (a second signed object that decides admission to a session).
- Card `general-c2c-d8-review-1116` = b: nobody independent will review this code. A seat's tests are the only guard.

## 1. Task, in plain language

Add the deputy to one library crate, `crates/coagent-roster`. The starter stays the only key that signs a roster version. In the roster the starter can mark one guest as deputy and set aside seats for them. The deputy signs "admissions" into those seats, one after another, as their own short chain; each admission must carry a proposal signed by another member. Members treat the people admitted this way as provisional members. When the starter's next roster version changes or drops the deputy's grant, every provisional member the starter did not keep is gone. Library and tests only: no daemon, no network, no storage engine, no screens.

"The starter" is the `convener` of the code.

## 2. Context (read these; paths, not copies)

Project: `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/`. Read `CLAUDE.md` there first, then in `2_Project_Files/`: ALL of `crates/coagent-roster/` (source, `build.rs`, README, every test file), `docs/ROSTER.md`, `scripts/red-controls-roster.sh`, `BACKLOG.md`, and the roster lane's report `coagent/5_Project_History/STATUS_M3_ROSTER.md` with whatever gate addenda follow it.

Design (READ-ONLY, in Friday's tree): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/06_design-addendum-rulings-2026-11-17.md`. Read the Revision notes at its top, then **section 2.8 WHOLE (2.8.1 to 2.8.11)**, section 2.3 to 2.5 (proposals and the starter's intake, which you build beside), section 1.1 (the limit), section 5.2 (verify-words; for 2.8.8) and section 10. **Section 2.8 is your specification.** Where it and this brief differ, stop and write the difference under DESIGN QUESTIONS.

One gate verdict to read before you design any stored state: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M3_AUDIT_r3_verdict.md`, finding **R3-M1** (its line 16 and the R3-M1 row of its findings table). In one sentence: storage was charged to whoever SIGNED a record, not to whoever CAUSED it, so members could fill the starter's allowance at a third member by proxy, and that member then refused every later roster version. That was the third failure of one class ("one party fills another's storage"). Section 5.3 exists so that this lane does not make a fourth.

### 2.1 What you build on, and how to check it is there

This brief was written against branch `m3-roster` at head `0a47fc9b16770754874a376edb27a03a432f8775`, read in its worktree on 2026-11-17, BEFORE its gate. It may have changed. **Your first act: check every symbol below against `main`. If one is missing, renamed, or does something else, STOP, list the differences under BLOCKERS, and wait for Friday.** Do not adapt silently.

In `crates/coagent-roster/src/lib.rs`:
- constants `CAP = 8`, `CAP_DEFAULT = 4`, `MAX_ENTRIES_EVER = 32`, `MAX_VERSIONS = 256` (lines 57-70);
- `Member` with the optional field `proposal: Option<ProposalRecord>`, `#[serde(default, skip_serializing_if = "Option::is_none")]` (85-107); `Member::new` with six arguments (120-139); `Member::proposed` (143-169); `Member::rebuilt_proposal(&SessionId)` (173-192);
- `ValidRoster::{signed, version, hash, role_of, is_convener, member_keys, cap, proposer_of, unchecked_proposals}` (377-416) and the crate-private `device_of` (418-422);
- `next_with_cap` (429-443), which clones the body and changes only `cap`, `version`, `prev_hash`;
- `is_roster_signer` (448-450), "THE ONE place that decides who may sign a roster version", and `check_roster_signer` (454-465);
- `impl RosterView for ValidRoster` (467-480);
- `validate_body` (533-634), every single-version rule; `check_transition` (860-936), whose "existing member unchanged" comparison lists the fields one by one, `proposal` included (900-912);
- `Applied` with two variants and three lists (709-722); `ApplyReport { applied, cap_change }`, `#[non_exhaustive]` (735-743);
- `RosterChain::start` (760-780), which refuses a first roster that does not list the local device (768-770); `apply` (793-795); `apply_with_report` (798-856), where a different object at a held version number is `RosterError::Fork` (804-819);
- `admit` (981-1021): `roster.update` and `session.end` go through `is_roster_signer` (1007-1011); `member.propose.result` goes through `intake::may_approve` (1014-1019); observers may not send `member.propose` (998).

In `src/intake.rs`: `may_approve(roster, key)` is `roster.is_convener(key)` (145-147); `ProposalIntake::{new, tick, receive, approve, decline, decline_and_mute, outcome, pending_proposal, used_by, accounting}`; the ten checks in the module doc (5-18); the constants `PROPOSAL_TTL`, `PENDING_PER_PROPOSER = 1`, `PENDING_PER_SESSION = 3`, `QUOTA_PER_PROPOSER = 8`, `MAX_REMEMBERED_IDS` (36-47); `approve` gives the newcomer the LOWEST free slot below `cap` (387-389) and copies `cap` unchanged.

In `src/proposal.rs`: `PROPOSAL_LABEL` (29), `MAX_PROPOSAL_BYTES = 2048` (33), `proposal_message`, the one function that chooses signing domain and bytes (153-160; today `SignDomain::Roster` over label, a zero byte, and the canonical body), `verify_proposal_sig` (164), `SignedProposal`, `ProposalRecord` (241), `propose`.

Red controls: the roster lane's own list `RED_ROSTER` in `crates/coagent-roster/build.rs`, switched on by `COAGENT_RED_ROSTER` (`cfg(coagent_red_roster = "…")`), runner `scripts/red-controls-roster.sh` (29 rows at that head). Tests at that head: 69 in the crate; `tests/pinned_encoding.rs` pins a two-member roster as main produced it before the lane.

Three things in that code this lane MUST change, each a known touch point, none a surprise:
1. `check_transition`'s field-by-field comparison will refuse any change to a new `Member` field unless you carve it out. The carve-out is for the grant field ONLY.
2. `ProposalIntake::approve` picks the lowest free slot. Once seats can be set aside, it must never pick a set-aside seat.
3. `next_with_cap` copies the body. With a grant in the body, a copied grant keeps its old epoch, which rule 3 of 06 section 2.8.2 forbids when `cap` changes.

### 2.2 Other crates that use this crate

Check at your start which of these have merged, and read their uses of this crate at `main` (or on their branch if still unmerged). On 2026-11-17 they were, on branch `m1-daemon` at `8e7b032`: `admit, Member, Role, RosterBody, RosterChain, SignedRoster, CAP`, a `RosterBody { … }` literal with `cap: CAP`, `Member::new` with six arguments, `RosterChain::start(&convener, session_id, &local, &first)`, `chain.current().member_at_slot(…)`, `.member_keys()`, `.version()`, `kk_initiate` / `kk_respond` given `chain.current()` (`crates/coagent-daemon/src/engine.rs:42, 698, 705, 1776-1789, 1988-1990, 2266, 2348, 2620, 2784`). On branch `m3-audit` at `882e094`: `Applied, ForkEvidence, RosterChain, RosterError, SignedRoster, ValidRoster`, `Applied::Advanced { .. }` and `{ removed, .. }`, `RosterError::Fork(ev)`, `RosterError::LocalNotMember`, `member_keys`, `role_of`, and in tests `body_hash, sign, Member, Removed, Role, RosterBody, CAP` (`crates/coagent-audit/src/bundle.rs:28, 703-721, 1071-1074`; `src/session.rs:190, 464-465, 512, 574, 778`; `tests/common/mod.rs:15, 41-42, 66-73`). Neither built a `Member { … }` struct literal then; re-check, because a new public field on `Member` breaks one.

### 2.3 Lessons that bind you (apply from the first commit)

1. A recorded fixture is generated from a scratch tree the seat builds, never from the real drive; committed output holds no absolute path, no user name and no other project's name. Lesson: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/learnings/2026-11-17_recorded-fixtures-come-from-a-scratch-tree-never-the-real-drive.md`. Write every commit as if the repository were already public. Scratch files stay inside `coagent/` (the roster seat let three land in a session temp folder and had to move them).
2. A recogniser of "safe" shell commands is never to be built (`…/learnings/2026-11-17_a-recogniser-of-safe-shell-commands-cannot-be-finished.md`). Nothing here reads shell text.
3. Every stored or buffered input a peer can cause has a bound, stated in a table, from the first version; and for each, who CAUSES it and who is CHARGED (section 5.3).
4. A red control must go red on its NAMED property, not on a side effect or a second rule. No assertion on truncated text. No test depending on map iteration order.
5. Prefer the Edit tool to shell heredocs. Never delete: quarantine.

## 3. What you own, and what you must not touch

You own, exclusively: `crates/coagent-roster/**` EXCEPT its gate test files; `scripts/red-controls-roster.sh`; `docs/ROSTER.md`.

Create your own worktree and branch: `git worktree add` at `coagent/worktrees/m3-deputy`, branch `m3-deputy`, from `main` at its current SHA. Record that SHA in STATUS. Set `CARGO_TARGET_DIR` to `tools/target/m3-deputy`.

You must not touch: the daemon, MCP, audit, relay, policy, IPC, CLI, proto and crypto crates (this includes the `build.rs` of proto and crypto, and `crates/coagent-crypto/src/identity.rs`); any test file a gate wrote (`tests/gate_roster.rs`, `tests/gate_return.rs`, and any file the roster lane's gate added: they have `gate` in their name; if in doubt, ask in STATUS); `scripts/red-controls-core.sh`; root `Cargo.toml` and `Cargo.lock` (you need no new crate and no new dependency; if you find you do, stop and write it under REQUESTS); `docs/CRYPTO-GLUE.md`; `spikes/`; `main`. `BACKLOG.md`: append only, in one separate commit. Never commit to `main`, force-push, or rebase a pushed branch.

**Does the design need another crate? No.** The combined membership view implements the existing `RosterView` trait from this crate, as `ValidRoster` does. The signing domain is handled as the roster lane handled it (one function; a REQUEST for the real value). What the daemon and the audit crate must do with provisional members is written under REQUESTS, not built.

Public API you must keep source-compatible: everything section 2.2 lists, and everything the roster lane added (its STATUS, "Public API added"), with these exact freedoms: you may add a field to `Member` (optional, skipped when absent); you may add fields to `ApplyReport` (it is `#[non_exhaustive]`); you may add `RosterError` and `RoleError` variants; you may add items. You may not change `Member::new`, `Member::proposed`, `RosterBody`, `Applied`, `RosterChain::start`, `RosterChain::apply`, `sign`, `body_hash`, `admit`'s signature, or what any of them returns for an input that is valid today.

## 4. Deliverables

Section references are to `06_design-addendum-rulings-2026-11-17.md`.

1. **The grant** (2.8.2). `Member` gains an optional field `deputy` holding `{ epoch, slots }`. Absent on every entry that is not the deputy, and then not encoded, so every roster that exists today encodes byte-for-byte as before. `slots` is non-empty and strictly ascending (one encoding per grant).
2. **The validator's grant rules** (2.8.2 rules 1 to 4), each its own `RosterError` variant: more than one grant; a grant on the starter's entry; a grant on an observer; a granted slot at or above `cap`; a granted slot a member occupies; `members + granted slots` above `cap`; an epoch that is not the version in which this exact grant under this `cap` first stood; a carried grant whose epoch changed. In `check_transition`, the grant is the ONLY field of an existing entry that may change besides the role; every other field stays refused as today. `is_roster_signer` keeps its meaning: the starter, nobody else. A deputy changes NOTHING about who may sign a roster version.
3. **The starter's helpers.** A pure function that builds the next `RosterBody` naming, changing or withdrawing a deputy, and one that builds the "keep" version: it adds chosen provisional members to the roster directly, in the seats they hold, and sets a new grant or none. Both refuse when the result would not validate; neither signs. `next_with_cap` on a roster with a grant must return a body that validates (the grant re-issued under the new version's epoch) or refuse; say which you chose and why. `ProposalIntake::approve` must never place a newcomer in a set-aside seat, and "a free seat" for the starter's intake means a seat that is neither occupied nor set aside.
4. **Admissions** (2.8.3). The admission type: `session_id`, `epoch`, `seq`, `prev`, the entry (the candidate's four key fields, role, slot, `added_at`, and the proposal as the SHORT record `ProposalRecord`, from which the signed proposal is rebuilt with the entry's keys), and the deputy's signature. Label `coagent-roster-deputy-admission-v1`. ONE private function chooses the signing domain and the signed bytes, as `proposal_message` does; if `main` has a signing-domain value for it, use it, otherwise sign under `SignDomain::Roster` over the label, a zero byte and the canonical body, and REQUEST the real value. Encoded size at most 4,096 bytes (a named constant, "proposed, not measured"), checked before decoding.
5. **The session chain.** One type that owns a `RosterChain` and the admissions of the current epoch. It offers: apply a roster version (returning the existing report plus, in new `ApplyReport` fields or a wrapping report, the grant change and the exact list of provisional keys dropped); apply an admission by the seven rules of 2.8.3 in their order, each refusal its own error, **nothing stored on any refusal**; the current combined view; per-compartment accounting (5.3). A roster version is validated by `RosterChain` exactly as today: your type adds rules, it relaxes none. When the epoch changes or the grant goes, admissions of the old epoch are discarded and can never be re-applied.
6. **The combined view** (2.8.3, "effective membership"). It implements `RosterView`. **With no admission it is indistinguishable from the roster it wraps: the same hash, the same lookups.** With admissions its hash is `SHA-256("coagent-roster-view-v1" ‖ 0x00 ‖ roster hash ‖ hash of the last admission)`, so it changes with every admission and two members at different points of the deputy's chain do not match. A roster member always wins over an admission for the same key.
7. **Roles at the decoder.** A function like `admit` that takes the combined view. A provisional member has the role in its admission, and additionally may NOT send `member.propose`, `member.propose.result`, `roster.update`, `session.end` or the admission message. The admission message type (`deputy.admission`) and `member.propose.result` are accepted from the current grant holder; the result is still accepted from the starter; from anyone else both are refused. ONE private function says who may admit provisionally, beside `may_approve` and `is_roster_signer`; `may_approve` keeps meaning "may approve into the roster", and `ProposalIntake::new` must still refuse the deputy.
8. **The deputy's intake.** Pure logic, time passed in, the same shape and the same bounds as the starter's intake, with its own accounting. Differences: the local device must hold the current grant; the proposer must be a guest on the ROSTER (not provisional, not the deputy); the proposal must name the roster version the deputy holds, at or after the grant's epoch; the candidate must not be a member, provisional, or on the `removed` list; "a free seat" is a set-aside seat no admission of this epoch took. Approval takes a value that says since when the starter has been unreachable, refuses if that is less than the absence period (5 minutes, a named constant, "proposed": design 2.8.4, I-19 as ruled), and returns the next UNSIGNED admission; a separate function signs. The intake never signs and never approves by itself. This is the one place the "only while the starter cannot be reached" rule lives in this crate; the docs say plainly that it binds an honest program only.
9. **A provisional newcomer's start** (2.8.7). A second way to begin, beside `RosterChain::start`: the starter key as stated by the proposer, the starter's current signed version, and the admissions of the current epoch in order. It checks the roster as `RosterChain` does except for the local-device check, checks every admission by deliverable 5's rules, and requires the LAST admission's entry to be the local device. `RosterChain::start` itself is not changed and still refuses a roster that does not list the local device.
10. **Evidence** (2.8.5). Two different admissions with one session, epoch and `seq`, both verifying under the deputy's key, form an evidence object any third party can check with the roster version that names the deputy. The same admission twice is not evidence. The first accepted stands; the second is refused and reported with the evidence.
11. **Docs.** `docs/ROSTER.md` gains the deputy: the construction on one page; the exact signed bytes; every rule with its test; the table of 5.3; the four "who can do what" tables of section 6 below, in full, the unflattering rows included; the three known limits of design 2.8.10; I-17 and I-21 listed as INTERPRETATIONS built as stated and still open; the three sentences of section 9.

## 5. Tests that must exist and pass (the definition of done)

**Order of work (verifier first).**
1. Check section 2.1 against `main`. Run the crate's tests, `scripts/red-controls-core.sh` and `scripts/red-controls-roster.sh` and record the results. Then, before changing any source, add a pinned-value test for a roster that contains a PROPOSED member (fixed identity bytes, as `tests/pinned_encoding.rs` does) and commit it alone, green. Both pinned tests must stay green to the end.
2. Write the tests of 5.1. Commit them alone, failing or not compiling, and say which in STATUS. Do not claim a test passes until you have seen it run (the roster seat's STATUS has a correction for exactly that).
3. Then implement.

### 5.1 Properties

Each has a test that FAILS if the property is broken. "Refused" always includes: the chain, the admissions and every counter are exactly what they were.

1. **Old encodings unchanged.** Both pinned tests hold.
2. **Grant rules, one version.** Each of the eight refusals of deliverable 2 that one version can show, with its own error; a grant with an empty slot list, a descending one and a repeated slot refused; a correct grant accepted (positive control).
3. **Epoch.** A new grant must carry the new version's number. An unchanged grant must carry its old epoch. A changed holder, a changed slot list or a changed `cap` with the old epoch is refused. A version that only changes `cap` while a grant stands is accepted only with the new epoch.
4. **The carve-out is exactly the grant.** On an existing entry the grant may appear, change and disappear. Every other field change is refused as before, and the roster lane's tests for that pass unchanged. Changing the grant holder's role to observer is refused.
5. **The roster still has one signer.** A roster version signed by the deputy is refused, whether signed plainly in the roster domain or with the admission label. `is_roster_signer` is false for the grant holder (a test names this).
6. **Admission signature.** Signed by a member who is not the grant holder: refused. Signed by the previous holder after the grant moved: refused. Every field of the admission changed to another valid value: refused. Cross-domain, every direction among the three signed kinds (roster version, proposal, admission): the signed bytes of one are never accepted as another, shown with the worst-case signer for each.
7. **Admission rules.** Each of the seven rules of 2.8.3 refuses with its own error; an admission that breaks two reports the earlier; a correct one is accepted (positive control). In particular: a proposal signed by the deputy itself; by the candidate; by an observer; by a provisional member; by a non-member; a candidate on the `removed` list; a candidate already a member; a candidate already provisional; a slot that was not set aside; a slot an earlier admission took; a role above the proposed one.
8. **The deputy's chain.** A gap in `seq`, a wrong `prev`, an admission for another epoch, an admission for another session: each refused with its own error. The same admission again is harmless and stores nothing more. An admission arriving before the roster version that carries its grant is refused and can be applied after that version arrives.
9. **Evidence.** Two different admissions at one `seq` yield evidence that verifies standalone; the same one twice yields none; evidence cannot be made with another member's key or a changed signature; evidence for a different epoch than the roster version offered is refused.
10. **A changed grant voids.** After a starter version with a new epoch or no grant: the view holds no provisional member; the report lists exactly the keys dropped; every old admission, offered again, is refused; the admissions compartment is empty (by accounting).
11. **Keep.** After the starter's "keep" version, the kept key is a roster member in its old seat and no longer provisional, the others are dropped and reported, and the new grant (if any) does not include the kept seat.
12. **An unrelated roster change leaves admissions standing** (same grant, same epoch, for example another member's role change).
13. **The view.** With no admission: the same hash and the same `member_at_slot` / `slot_of` answers as the roster, for every slot, and the crate's existing mesh test passes when given the view. With admissions: the hash differs from the roster's, differs after each further admission, and a provisional member is found at its seat. A key that is both a roster member and admitted is reported once, as the roster member.
14. **Roles.** The rules of deliverable 7, each way: what a provisional guest and a provisional observer may and may not send; that the grant holder may send the two deputy messages and a former holder, another guest and a provisional member may not; that the starter's rights are unchanged; that role and identity come from the view and the channel, never from the message.
15. **A provisional newcomer's start.** Accepted when the last admission is its own. Refused when its key is absent, when its admission is not the last, when any earlier admission is invalid, when the roster is not signed by the stated starter. `RosterChain::start` still refuses the same roster for that device.
16. **The deputy's intake.** A device that does not hold the grant cannot create one; the starter's `ProposalIntake::new` still refuses the deputy; each difference of deliverable 8 has its refusal; the bounds are the starter's and are counted separately; approval without the absence value does not compile or is impossible by type, and with one shorter than the absence period is refused; an approved body has the right `epoch`, `seq`, `prev` and a set-aside seat; nothing is signed by the intake; no source file reads a clock (the existing scan, extended, with its positive control).
17. **The starter's side.** Over generated states, the starter's intake never assigns a set-aside seat. With three members, one set-aside seat and a limit of 4, the starter's intake says full. `next_with_cap` with a grant behaves as you documented. The grant helper and the keep helper refuse whatever would not validate.
18. **Nobody fills what another needs** (5.3). With the admissions compartment full, the evidence compartment full and the deputy's intake full: a starter's roster version still applies, the starter's intake still accepts a correct proposal, and an honest member's own state is unchanged. With the starter's intake full: the deputy's intake still accepts a correct proposal. With one proposer at its quota at the deputy: another proposer's correct proposal is accepted. Each compartment's usage is read from the accounting, not inferred.
19. **Nothing that existed moved.** Every test the crate had at your branch point passes unchanged; every row of both red-control runners is still RED; gate files are byte-identical to `main` (show the empty diff).
20. **API stability.** Extend `tests/api_stability.rs` with the uses of section 2.2 as you find them at your start.
21. **Determinism.** No output or hash depends on map iteration order; say how you know.

`scripts/check.sh` exits 0 in your worktree. `#![forbid(unsafe_code)]` stays. No new cryptographic primitive.

### 5.2 Red controls you must deliver

Add them to the roster lane's mechanism (`RED_ROSTER` in the crate's own `build.rs`, `COAGENT_RED_ROSTER`, `scripts/red-controls-roster.sh`). A row counts as RED only if the named guard fails, the build was a red-control build, and the panic text names the property. A control still refused by a second rule is not red: widen it and keep both rules in the real code.

| Red control (broken variant) | Property it must break | Guard (5.1) | The failure must say |
|---|---|---|---|
| two grants accepted | one deputy | 2 | a second deputy was accepted |
| grant on the starter or on an observer accepted | grant holder | 2 | a grant on a non-guest was accepted |
| set-aside seat may be occupied | seats | 2 | a member sat in a set-aside seat |
| members plus set-aside seats not compared with the limit | the limit holds | 2 | set-aside seats exceeded the limit |
| epoch not checked | epoch | 3 | a changed grant kept its old epoch |
| any field of an existing entry may change with the grant | carve-out | 4 | an entry's keys changed under cover of a grant change |
| the grant holder counts as a roster signer | one signer | 5 | a roster version signed by the deputy was accepted |
| admission signature not verified | admission signature | 6 | an admission the deputy did not sign was accepted |
| admission label not required | cross-domain | 6 | a roster-domain signature was taken as an admission |
| a former holder's signature accepted | admission signature | 6 | a withdrawn deputy admitted someone |
| proposal on an admission not verified | admission rules | 7 | an admission without another member's proposal was accepted |
| the deputy may be the proposer | admission rules | 7 | the deputy admitted someone alone |
| a provisional member may propose | admission rules | 7 | a provisional member's proposal was used |
| a removed key may be admitted | admission rules | 7 | a removed key was admitted by the deputy |
| a seat that was not set aside may be used | admission rules | 7 | an admission took a seat that was not set aside |
| role above the proposed one allowed | admission rules | 7 | proposed observer was admitted as guest |
| `seq` / `prev` not checked | deputy's chain | 8 | an admission out of sequence was accepted |
| epoch of an admission not checked | deputy's chain | 8, 10 | an admission of an old epoch was accepted |
| a second admission at one `seq` replaces the first | evidence | 9 | a conflicting admission replaced the first |
| the same admission twice is evidence | evidence | 9 | one admission was reported as two stories |
| admissions survive a changed grant | voiding | 10 | a provisional member survived a withdrawn grant |
| dropped keys not reported | voiding | 10 | a dropped member was not reported |
| the view's hash ignores admissions | view | 13 | two different admission chains gave one view |
| the view differs from the roster with no admission | view | 13 | a session without admissions changed its hash |
| a provisional member may send `member.propose` | roles | 14 | a provisional member's proposal message was admitted |
| anyone may send the admission message | roles | 14 | a guest's admission message was admitted |
| newcomer's start skips earlier admissions | newcomer | 15 | an invalid earlier admission was accepted at start |
| newcomer's start accepts a roster without its admission | newcomer | 15 | a device with no admission started a chain |
| the deputy's intake ignores the absence period | absence | 16 | the deputy approved with the starter reachable |
| the starter's intake accepts the deputy as local | intake | 16 | a deputy opened the starter's intake |
| the starter's intake may assign a set-aside seat | starter's side | 17 | the starter's intake used a set-aside seat |
| admissions counted against the roster's store | isolation | 18 | a roster version was refused because of admissions |
| evidence unbounded | isolation | 18 | more evidence was kept than the bound |

Add a row for anything else a mutation survives. "Equivalent mutant" is a claim you justify in writing in `docs/ROSTER.md`.

### 5.3 Storage: who causes it, who is charged, and what it can never block

Deliver this table in `docs/ROSTER.md` and STATUS, with a test for every row. The rule behind it: **each compartment has its own fixed bound; none shares room with another; and nothing in a compartment a deputy or a member can fill is ever consulted when a starter's roster version, or another party's own act, is accepted.**

| Stored thing (at each member unless said) | Who CAUSES it | Who is CHARGED | Bound | What filling it can block | What it can never block | Test |
|---|---|---|---|---|---|---|
| Roster versions kept | starter | starter (the roster compartment) | 256 versions, each at most 65,535 bytes (roster lane) | further roster versions (the session is frozen for changes) | n/a: only the starter fills it | roster lane |
| The grant | starter | inside the roster version | at most 7 seats | n/a | n/a | 5.1 item 2 |
| Admissions of the current epoch | deputy | the admissions compartment | as many as set-aside seats (at most 7), each at most 4,096 bytes | further admissions (the seats are used) | any roster version; the starter's intake; any member's own act | items 10, 18 |
| Admissions of old epochs | deputy | nobody: not kept | 0 | nothing | n/a | item 10 |
| Fork evidence about the deputy | deputy (it takes the deputy's signature to cause any) | the evidence compartment | PROPOSED: 4 pairs per session, first come; later ones are counted, not kept | nothing | everything | items 9, 18 |
| Dropped-key report | starter (by changing the grant) | returned to the caller, not kept | at most 7 keys | nothing | n/a | item 10 |
| Deputy's intake: pending proposals (at the deputy only) | each proposing member | that proposer | 1 per proposer; 3 in all | for at most 10 minutes, three members' pending proposals delay a fourth's | the deputy's own roster and admission handling; the starter's intake (another device) | items 16, 18 |
| Deputy's intake: proposals per proposer per session | each proposing member | that proposer | 8, any outcome | that proposer's further proposals to the deputy | any other proposer; that proposer's quota at the starter | item 18 |
| Deputy's intake: remembered proposal ids | proposing members | derived | 248 | nothing (cannot overflow) | n/a | by accounting |
| A newcomer's start input | proposer (hands it over) | one call | one roster version and at most 7 admissions | that start only | n/a | item 15 |
| Set-aside SEATS (not storage, but the same class) | starter sets them aside; deputy fills them | the deputy's seats | the grant | the deputy's further admissions | the starter's own seats: `cap` minus set-aside seats are never the deputy's to fill | item 17 |

Two things to write down honestly: the three-pending bound at the deputy is shared between proposers for up to 10 minutes (as at the starter); and a member can have one newcomer approved by both the starter and the deputy, which wastes a set-aside seat until the grant is renewed (design 2.8.10).

Under REQUESTS for the audit lane (do not build): admissions and deputy evidence, if the audit log ever stores them, must be charged to a compartment of their own and never to the allowance from which roster versions are accepted (verdict R3-M1).

## 6. Who can do what (deliver all four tables in `docs/ROSTER.md`; a test for every row that code can decide)

**A hostile deputy.**

| Attempt | Result |
|---|---|
| Sign or alter a roster version | Refused by every member (5.1 item 5). |
| Block, override or outrun a change by the starter | Cannot: nothing the deputy signs is in the starter's chain; a starter version that changes or drops the grant voids the admissions wherever it arrives. |
| Stay deputy after being withdrawn | Only against members who have not yet received the newer version, until they do. |
| Admit someone alone | Refused: the proposal must be signed by another roster guest. |
| Admit a removed key, exceed the set-aside seats, raise a role | Refused. |
| Fill the set-aside seats with confederates, with one roster guest who proposes for them | POSSIBLE. They are provisional, labelled, see nothing on a machine until its owner accepts them, and go when the starter renews the grant. This is the trust the starter takes on. |
| Use up the seats so nobody else gets in | POSSIBLE. The starter renews the grant. |
| Approve while the starter is in fact reachable | POSSIBLE for a modified program: no other member can check absence. Everything else in this table still holds. |
| Tell different members different admissions | Evidence (5.1 item 9); members who saw different ones disagree about that seat until the starter renews the grant. |
| Sit between a newcomer and the members | Cannot without the starter's key (design 2.8.6). REASONED, NOT TESTED in this crate: say so. |

**A hostile starter.** Everything a starter could already do, plus: name a confederate as deputy (visible to all: the grant is in the roster); drop every provisional member at will by renewing the grant (their power by the ruling); show different grants to different members (that is a roster fork, existing evidence). A starter cannot: make a member accept an admission the deputy did not sign; use a set-aside seat without changing the grant.

**A hostile member.** Flood the deputy with proposals: bounded per proposer (5.3). Propose a removed key, a current member, or themselves: refused before any card. Send one newcomer to both the starter and the deputy: both may approve; the roster entry counts; a set-aside seat is wasted until the grant is renewed. Present an admission or a grant they made up: refused (signatures). A removed person returning with the same signing key and a new channel key has a new key id and is NOT recognised as removed (design 2.8.10; the roster lane's DESIGN QUESTION 3): state it, do not try to close it.

**The relay.** Cannot forge a grant, an admission or a proposal. Can withhold or delay any of them: members who are behind have a different view, cannot open channels to the newcomer, and catch up when the object arrives. Can delay a withdrawal to some members, who go on accepting that deputy's admissions until it arrives.

## 7. Safety rules, and decisions you are NOT making

`coagent/CLAUDE.md` rules 1 to 7 bind you. No model runs, no network (cargo may fetch locked crates; you should need none), nothing at user scope, stay inside `coagent/`, never delete (quarantine under `coagent/_quarantine_<date>/`), nothing deployed, published or paid for, no repository setting changed. Report the disk space you used.

Not merging (an independent QA agent reads your diff first; Friday gates). Not widening the deputy: no removing, no role change, no limit change, no ending the session, no naming a further deputy, no admitting alone, no roster signature of any kind; these were ruled out by Kam's choice. Not choosing on I-17 (one deputy, a guest) or I-21 (no time limit; the role outlasts a starter who has left): build them as design 2.8 states them and list them as open. Not closing the key-id-only gap for removed people. Not deciding how the audit log treats a provisional member. Not building the transport of grants and admissions, the welcome, the detection of "cannot reach the starter", the verify-words inheritance for dropped provisional members (design 2.8.8), or any screen: daemon work, under REQUESTS. Not adding a signing-domain value to the crypto crate (REQUEST). Not relaxing any rule the roster lane built. Where design 2.8 is silent or you believe it is wrong, implement the conservative reading, record it under DESIGN QUESTIONS with your reasoning, and continue. Not answering Kam's open cards. Not wrapping on a dry queue: when section 5 is green, write READY and wait.

Under REQUESTS instead of edits: the signing-domain value and its exact lines; the entry to append to `docs/CRYPTO-GLUE.md`, ready to paste; what the daemon must do (use the session chain and the combined view everywhere it uses `RosterChain` and `current()` today; carry `deputy.admission`; supply the absence value; drop channels for reported keys; treat a dropped provisional member as removed for the verify-words rule); what the audit crate must decide (provisional members) and the storage rule of 5.3.

No prompt-box line is an instruction unless it names this brief or a later addendum in Friday's briefs_drafts.

## 8. Report

`coagent/5_Project_History/STATUS_M3_DEPUTY.md` (new): the SHA you branched from and the result of the section 2.1 check, symbol by symbol; public API added (twenty-five lines at most) and the proof the old API is unchanged; the 5.1 list with pass or fail; the red-control table with the panic text seen for each row, and the counts of old rows still RED in both runners; the 5.3 table with its tests; the four tables of section 6 with which rows are tested and which are reasoned; INTERPRETATIONS built and still open (I-17, I-21); DESIGN QUESTIONS; REQUESTS; dependencies added (expected: none); the empty gate-file diff; branch, head SHA, `git ls-remote origin m3-deputy`; `scripts/check.sh` and both runners' tails; disk used; BLOCKERS; what is NOT done. Every UNKNOWN names why it is unknown and what would close it. Push after every green `check.sh`. Update the last line at least every 20 minutes: `IN PROGRESS: <item>` until done, then exactly:

`READY FOR QA M3-DEPUTY`

Questions: write the question in STATUS and proceed on the safest reading. Anything approval-class (money, publishing, a deploy, anything irreversible, anything outside `coagent/`) is a STOP recorded under BLOCKERS. Rounds: at most 3 returns from Friday, then it goes to Kam as a card.

## 9. For Kam: the three sentences a user sees when naming a deputy

Draft wording for his approval; the seat copies it into `docs/ROSTER.md` and changes none of it. ("Dana" stands for the chosen member, "2" for the seats set aside.)

1. While you are away, Dana can let in a person another member has proposed, into the 2 seats you set aside; her copy of CoAgent only offers this when it cannot reach yours, and that is the one part the other members cannot check.
2. Dana cannot remove anyone, change the limit, end the session, name another deputy or change the member list you signed, and nobody she lets in sees anything on a machine until that machine's owner accepts them.
3. When you are back you choose who stays: anyone you do not keep leaves the session, and you can withdraw Dana's role at any time.
