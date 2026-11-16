This addendum is from Friday (Kam's laptop coordinator seat). Client: General (Kam's personal project). Project: CoAgent. You are the ROSTER seat. It extends your brief `2026-11-17_coagent_M3_ROSTER_brief.md` and its ADDENDUM 1. Report in a section "ADDENDUM 2" of `coagent/5_Project_History/STATUS_M3_ROSTER.md`.

# M3 ROSTER — ADDENDUM 2: the limit rule (4 by default, raisable to 8). The deputy is NOT built in this lane.

## 0. Authority and specification

- Kam, live board 2026-11-17, verbatim as Friday relayed them in ADDENDUM 1: "Decision general-c2c-i1-limit-fixed-1117: b — Four by default, the starter may raise it to eight"; "Decision general-c2c-i5-starter-gone-1117: b — The starter can name a deputy"; "Decision general-c2c-i2-who-hands-invite-1117: a — The member hands out the invitation, the starter approves".
- Your specification is the design addendum as REVISED: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/06_design-addendum-rulings-2026-11-17.md`. Read the "Revision 1" note at its top, then **section 1 (the new one; NOT "1-OLD")**, section 2.4 rule 4, the bounds table of 2.5, and section 8. Read section 2.8 (the deputy) once, for context only: you build nothing from it.
- **The deputy is split out.** The design (06 section 2.8) keeps the roster single-writer and gives the deputy a separate signed list. It is a second signed object, a second chain and a new notion of membership, and five of its choices are still with Kam (I-17 to I-21). It becomes its own lane after yours has merged, with its own gate. For you the rule of ADDENDUM 1 point 3 is now final: build nothing for a deputy.

## 1. What this SUPERSEDES (everything not named here stands)

In the BRIEF:
- Section 1, the sentence "First, a session holds at most 4 people instead of 8." It becomes: a session holds 4 people by default and the starter may raise it to 8. The sentence "The roster keeps ONE signer: the starter." STANDS for this lane.
- Section 2, the specification line "sections 1 and 2 WHOLE": section 1 now means the revised section 1. The bullet "Tests that assume 8 …" and its UNKNOWN about the gate files are void: the hard maximum stays 8, so those tests stay as they are.
- Section 3, the words "`CAP` (its value changes; its name and type do not)": `CAP` keeps its name, type AND value. The permission to edit roster rows of `scripts/red-controls-core.sh` is withdrawn: you rename no existing test, so you edit no row there.
- Section 4, deliverable 1 (replaced by section 2 below) and the number in deliverable 2 (16 becomes 32, and a second bound is added).
- Section 5, order of work, step 4: void. **No edit to `tests/gate_roster.rs` or `tests/gate_return.rs` is permitted for any reason.** Show in STATUS that `git diff main -- crates/coagent-roster/tests/gate_roster.rs crates/coagent-roster/tests/gate_return.rs` is empty.
- Section 5.1 items 1 and 2; section 5.2 rows 1 to 3 (limit compared with 8; `roster_no_cap`; lifetime bound); section 5.3 rows "members", "members plus removed", "remembered proposal ids" and "muted proposers". Replaced by sections 3 to 5 below.
- Section 7, "implement I-1 to I-7 as addendum 06 states them": I-1 and I-5 are ruled and I-2 is confirmed. You implement I-3, I-4, I-6, I-7 as before, and the new I-14, I-15, I-16 as section 1.1 of 06 states them. You choose between none of them and their alternatives.

In ADDENDUM 1:
- Point 2's hold ("leave `CAP`, the `cap` check and the cap tests exactly as they are on main") is lifted and replaced by section 2 below. Its instruction not to edit the gate files stays, now without exception.
- Point 3 stands and is final: nothing for a deputy. Its hold on "who may approve" is lifted in this sense only: build the intake's approval (brief deliverable 6) and the second half of `admit` (brief deliverable 7: `member.propose.result` from anyone but the starter is refused) as the brief says, starter-only, with each decision in ONE private function (one that says who may sign a roster version, one that says who may approve a proposal and send its result). Name the two functions in STATUS.
- "What to do now", last paragraph: ADDENDUM 2 has arrived; you write READY when the brief as amended, ADDENDUM 1 and this addendum are all done.

If your worktree already holds something this addendum overturns (a limit of 4 as a constant, a lifetime bound of 16, an edited gate file, a renamed cap test), undo it with a NEW commit and say so in STATUS. Never rewrite pushed history.

## 2. Deliverables (replace brief deliverable 1; amend deliverables 2 and 6)

What is on main, read on 2026-11-17 at `18005d6`; read it yourself: `pub const CAP: u8 = 8` (`crates/coagent-roster/src/lib.rs:34`); the cap check is `b.cap != CAP || b.members.len() > usize::from(CAP)` and returns `CapExceeded` (lib.rs:311-314); the slot check is `m.slot >= b.cap` and returns `BadSlot` (lib.rs:334-336); the existing red control `roster_no_cap` switches off both (lib.rs:310-311, 333-334); `apply` keeps every accepted version in a map with no bound (lib.rs:410, 479) and a version that changes nothing is valid (lib.rs:486-554 has no rule against it); `Applied::Advanced` has three lists (lib.rs:389-402).

1. **Constants.** `CAP` unchanged (8, the hard maximum). Add `pub const CAP_DEFAULT: u8 = 4`.
2. **The validator's limit rule** (06 section 1.1 rules 1 to 3, 6, 7). The `cap` field is valid only if it is `CAP_DEFAULT` or `CAP`. A `cap` above `CAP` is refused with `CapExceeded`, as today (the existing test offers 9 and expects that error: `tests/roster.rs:150-154`). Any other value that is not 4 or 8 is refused with a NEW variant, `BadCap`. The member count is compared with the version's own `cap`, not with the constant; more members than `cap` is `CapExceeded`. The slot rule stays as it is. Version 1 may carry 4 or 8. A raise is always valid. A lowering is valid exactly when the resulting version is valid; write no extra rule for it. The existing red control `roster_no_cap` must keep doing what it does (both checks off) and stay RED on its existing row.
3. **Reading and reporting the limit.** `ValidRoster::cap() -> u8`. A new method `RosterChain::apply_with_report(&next)` that does exactly what `apply` does and returns a `#[non_exhaustive]` report holding the existing `Applied` value and, when the limit differs from the previous version, the old and the new value. `apply` keeps its signature and its results and is the same code path (it returns the report's `Applied`). A version that only changes the limit therefore gives `Applied::Advanced` with three empty lists from `apply`: say so in its doc comment, and say that callers who must react to a limit change (suspend grants, tell the user; 06 section 1.1 rule 8) call `apply_with_report`.
4. **A pure helper for the starter's side** that builds the next `RosterBody` with a different `cap` from a `ValidRoster`, and refuses when the result would not validate. It signs nothing.
5. **Lifetime bounds** (amends brief deliverable 2; 06 section 2.4 rule 4). `MAX_ENTRIES_EVER = 32`. `MAX_VERSIONS = 256`: a version numbered above it is refused with its own error, by `start` and by `apply`, so the kept history is bounded. Both constants named and marked "proposed, not measured".
6. **The intake** (amends brief deliverable 6). "A free seat" means fewer members than the CURRENT version's `cap`. Approving a proposal never changes `cap`: with the session full at 4, the proposal is refused as full, and the starter raises the limit as a separate act through the helper of item 4. Remembered proposal ids: at most 248 (31 possible proposers × 8). Muted proposers remembered: at most 31. Pending per session stays 3.
7. **Docs.** `docs/ROSTER.md`, the crate README and the module doc state the rule in the words of 06 section 1.1, cite both of Kam's lines, and list I-14, I-15 and I-16 as implemented INTERPRETATIONS. The README's "cap 8" becomes "4 by default, 8 at most".

## 3. Properties (replace brief 5.1 items 1 and 2; the rest of 5.1 stands)

Write these tests first and commit them alone, failing or not compiling, as the brief's order of work says.

1. **Values.** `cap` 4 and 8 are accepted in version 1 and in a later version. 0, 1, 2, 3, 5, 6, 7 are refused with `BadCap`. 9 and 255 are refused with `CapExceeded`.
2. **The limit in force is the version's own.** At `cap` 4: four members are accepted (positive control); a fifth member is refused with `cap` left at 4; a member in slot 4 is refused even with three members.
3. **Raise.** A version that changes only `cap` from 4 to 8 is accepted; `apply_with_report` names 4 and 8; `apply` on the same input returns `Advanced` with three empty lists. After it, a fifth member in slot 4 is accepted. A single version that raises and adds the fifth member is accepted and the report shows both.
4. **Lowering.** From 8 to 4: refused with five members; refused with three members when one sits in slot 5; accepted with four members in slots 0 to 3, and the report names 8 and 4. After each refusal the chain's version and hash are what they were.
5. **Only the starter changes the limit.** A version that changes `cap` and is signed by another member's key is refused (this is the existing signature rule; the test is here so the property has a name).
6. **Lifetime bounds.** 32 entries (members plus removed) accepted, 33 refused. Version 256 accepted, version 257 refused by `apply`; a first roster numbered 257 refused by `start`. After each refusal the chain is unchanged.
7. **The intake and the limit.** With four members at `cap` 4, a correct proposal is refused as full and nothing is stored. For every approval the intake produces, over generated states, the body's `cap` equals the current version's `cap`. After a raise, a NEW proposal against the new version is accepted (the old one is stale by the brief's rule).
8. **Nothing that existed moved.** `test7_ninth_member_is_refused` passes unchanged. The two gate files are byte-identical to main. Every row of `scripts/red-controls-core.sh` is still RED.
9. **The two unmerged crates still fit.** Extend the API-stability test of brief 5.1 item 11: a roster built the way they build one validates, namely `cap: CAP` with two guests in slots 0 and 1, built with a `RosterBody { … }` literal and `Member::new` with six arguments, started with `RosterChain::start(&convener, session_id, &local, &first)`. Re-checked at source on 2026-11-17: branch `m1-daemon` at `8e7b032`, `crates/coagent-daemon/src/engine.rs:42, 698, 1776-1789, 1988-1990, 2784` (it also calls `chain.current().member_at_slot(…)`, `.member_keys()`, `.version()` and `admit(chain.current(), &m)`); branch `m3-audit` at `882e094`, `crates/coagent-audit/src/bundle.rs:28, 703-721, 1071-1074`, `src/session.rs:190, 464-465, 512, 574`, `tests/common/mod.rs:15, 41-42, 66-73` (it also uses `Removed`, `body_hash`, `sign`, `ValidRoster`, `role_of`, `Applied::Advanced { removed, .. }`, `RosterError::LocalNotMember`, `RosterError::Fork(ev)` and `ForkEvidence` as a stored value). All of these keep compiling and keep their meaning.
10. **The pinned encoding of the brief's step 1 stays green** (its roster is at `cap` 8).

## 4. Red controls (replace brief 5.2 rows 1 to 3; the rest of 5.2 stands)

Same runner, same rule: RED only if the named guard fails, the build was a red-control build, and the panic text names the property.

| Red control (broken variant) | Property it must break | Guard (section 3) | The failure must say |
|---|---|---|---|
| any `cap` value up to 8 accepted | values | item 1 | a limit of 6 was accepted |
| member count compared with the hard maximum, not the version's `cap` | limit in force | item 2 | a fifth member was accepted at a limit of 4 |
| slot compared with the hard maximum, not the version's `cap` | limit in force | items 2 and 4 | slot 4 was accepted at a limit of 4 |
| a limit change is not reported | raise is visible | item 3 | a raise from 4 to 8 was not reported |
| the intake ignores the current `cap` | intake and limit | item 7 | a proposal was accepted into a full session |
| the intake's approval sets `cap` to 8 | raise is never implied | item 7 | an approval changed the limit |
| entries bound not enforced | lifetime | item 6 | a 33rd entry was accepted |
| versions bound not enforced | lifetime | item 6 | version 257 was accepted |
| `roster_no_cap` (exists on main; row in the core runner, untouched) | hard maximum | `test7_ninth_member_is_refused`, unchanged | as today |

Rows two and three need care, because at a limit of 4 the member-count rule and the slot rule back each other up: a fifth member cannot sit below slot 4. The slot rule can be shown broken alone (three members, one of them in slot 5, at a limit of 4). The count rule cannot: with only it broken, the slot rule still refuses the fifth member. So the count-rule control must also switch off the slot rule, as the brief's 5.2 describes for a property with a second line of defence; both rules stay in the real code. Say in STATUS that you did this.

## 5. Bounds (replace the named rows of brief 5.3)

| Input | Who causes it | Bound | Where enforced | Test |
|---|---|---|---|---|
| members | starter | the version's `cap`: 4 or 8 | validator | section 3 items 1, 2 |
| members plus removed, session lifetime | starter | 32 (proposed) | validator | item 6 |
| roster versions kept, session lifetime | starter | 256 (proposed); each at most 65,535 bytes encoded | validator (`start`, `apply`) | item 6 |
| remembered proposal ids | guests | 248, derived | intake | brief 5.1 item 8, by accounting |
| muted proposers remembered | starter's own act | at most 31 | intake | by construction |

## 6. Decisions you are NOT making

Not building any part of the deputy: no grant field on `Member`, no admission type, no combined membership view, no second way to start a chain, and no relaxing of the check that a first roster lists the local device (lib.rs:427-429). Not choosing whether the limit may be lowered, whether a session may start at 8, or who may change the limit: I-14, I-15, I-16 are implemented as written and are with Kam. Not changing `CAP`, the relay, the daemon or the audit crate. Not editing a gate file. Not adding a field to `RosterBody` or to `Applied::Advanced`, and not changing `Member::new` or `RosterChain::start`. If you believe the rule of section 2 is wrong or unsafe, implement the conservative reading, record it under DESIGN QUESTIONS, and continue.

Under REQUESTS, in addition to the brief's: the daemon's default when it creates a session should be `CAP_DEFAULT` (it writes `cap: CAP` today, branch `m1-daemon`, `engine.rs:1781`), and the daemon must call `apply_with_report`.

The five lessons of the brief's section 2 bind this addendum unchanged. No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.

## 7. Report and last line

STATUS section "ADDENDUM 2": what you undid, if anything; the section 3 list with pass or fail; the red rows with the panic text seen; the bounds table; the two decision functions by name; the empty gate-file diff; `scripts/check.sh`, `scripts/red-controls-core.sh` and `scripts/red-controls-roster.sh` tails; head SHA and `git ls-remote origin m3-roster`. Every UNKNOWN names why it is unknown and what would close it. Your last line is unchanged, exactly:

`READY FOR QA M3-ROSTER`
