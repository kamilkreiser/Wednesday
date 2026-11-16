This brief is from Friday (Kam's laptop coordinator seat). Client: General (Kam's personal project). Project: CoAgent. You are the AUDIT seat. Your report is the STATUS file named in section 8; Friday reads it at source.

# CoAgent — AUDIT seat: the tamper-evident, per-recipient audit log (library crate)

## 0. Authority (provenance)

- Kam, live board 2026-11-16 23:08:33, verbatim: "I will do the repository step now.  also, if you are ready to start building in the night.  start building and get through as much as you can." and 23:09:25 "yes.  cogent only". The grant ends at his review on the morning of Tuesday 2026-11-17; a seat still running then finishes its current step and reports.
- Card `general-c2c-build-model-1116` = a ("Fable for the M0 spikes, then the routing table"): this seat runs on Opus 5.5 under routing row C3 (build on a security design surface).
- Card `general-c2c-d12-audit-1116` = a, option text verbatim: "Hashes and short redacted previews". Card `general-c2c-d8-review-1116` = b: nobody independent will review this code; the delta gates tonight found that a seat's tests are the only guard, so every property gets a test that fails when it is broken.

## 1. Task, in plain language

Build one library crate, `crates/coagent-audit`: each member keeps an append-only, signed, hash-chained log of the audit-class events they originate; every recipient gets the same signed header and only the content tier the author allows them; members cross-check heads so an author who tells two stories is caught with transferable proof; a bundle can be exported and verified offline. Library and tests only: no storage engine choice beyond a trait, no network, no daemon, no CLI.

## 2. Context (read these; paths, not copies)

Project: `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/`. Read `CLAUDE.md` there first, then `2_Project_Files/docs/M0-OUTCOMES.md`, `docs/CRYPTO-GLUE.md` and `BACKLOG.md`.
Design (READ-ONLY, in Friday's tree): `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/`
- `04_design-revision-rulings.md` section 3.9 WHOLE (construction, who holds what, checkpoints and countersignatures, equivocation, receipts, joiners and leavers, export and verification, stated limits), 3.5 (roster), 3.8 (the `chain` field of the envelope and the `audit.heads.seen` message), 6.5 (previews).
- `03_architecture-design.md` section 9.4 (the two-party construction this generalises) and 10.3.
What is on `main` that you build on (merged tonight after two independent gates): `crates/coagent-proto` (canonical encoding, envelope with its `chain` field, byte types), `crates/coagent-crypto` (`DeviceIdentity::sign` with `SignDomain`, `verify_device`, key ids), `crates/coagent-roster` (signed roster chain, fork evidence). Read their public API and `docs/CRYPTO-GLUE.md` before designing yours. Use their signing with a NEW domain-separation value for each kind of signed audit object; never sign raw bytes without a domain.
What the gates taught tonight (apply from the first commit): red controls must go red on the property named, not on a side effect; an assertion on truncated text can hide its subject; a test that depends on hash-map iteration order is not a test; "equivalent mutant" is a claim to justify in writing.

## 3. What you own, and what you must not touch

You own: `crates/coagent-audit` (new). Branch `m3-audit` in your own worktree `coagent/worktrees/m3-audit`, created with `git worktree add` from `main` (must contain commit 129914b). Root `Cargo.toml`: ADD your crate to `members` and any dependency line under `[workspace.dependencies]` in one tiny separate commit (other seats are adding member lines too: keep it to one line each so merges stay trivial). If you need a small addition to `coagent-proto` or `coagent-crypto` (for example a new `SignDomain` value), do NOT edit those crates: define what you need in your crate if possible; otherwise write the exact change you need under REQUESTS in STATUS and work around it. Never commit to `main`, force-push, or rebase a pushed branch. `scripts/env.sh` now finds the toolchain from a worktree; set `CARGO_TARGET_DIR` to `tools/target/m3-audit`.

## 4. Deliverables

1. **Event header and chain** exactly as 04 section 3.9: `{session_id, author, author_seq, ts, prev_hash, type, tiers: {summary: H(salt_s ‖ summary), full: H(salt_f ‖ full)}, sig}`, `hash = SHA-256(prev_hash ‖ canonical(header))`, canonical encoding from `coagent-proto`. An `AuthorChain` that only its owner can append to (needs the `DeviceIdentity`), with timestamps passed in (never read from the clock).
2. **Tiers.** Per-event random salts (from the OS RNG through the same route the crypto crate uses); a function producing, for a recipient at share level `full | summaries | nothing`, exactly the tier bodies and salts that level is entitled to and nothing else. A `summaries` recipient must not be able to confirm a guess about the `full` body. Previews: the `full` tier carries a short redacted preview only (D12); implement the truncation rule 04 section 6.5 proposes as a named constant marked "proposed, not ruled", and a `Redactor` trait with a conservative default that masks anything matching the credential-shaped patterns you list in one module (key-looking strings, `KEY=value` forms, bearer tokens, private-key blocks). Say plainly in the docs that pattern redaction misses things.
3. **Verification by a recipient.** `ReceivedChain` per author: accepts a header only if the signature verifies against the author's key from the roster, `author_seq` is exactly next, `prev_hash` matches, and any tier body supplied hashes to its commitment under its salt. Gaps, replays, reorders and forks are distinct errors; nothing is partially applied.
4. **Checkpoints and countersignatures.** `audit.head {author_seq, hash, sig}` produced every N events or T seconds (both parameters, time passed in); a recipient countersigns; the author stores countersignatures and can show which members attested to which head.
5. **Equivocation.** `audit.heads.seen` records exchanged between members; given two signed headers or heads from one author with the same `author_seq` and different content, produce a self-contained `EquivocationEvidence` object that a third party can verify with only the roster. The same check for two roster versions with one number reuses the roster crate's fork evidence (do not reimplement it).
6. **Receipts, joiners, leavers** as 04 section 3.9 states: a recipient's signed receipt in its own chain; a joiner's view starts at the head it is given and it can prove nothing about before; a removed member's last countersigned checkpoint bounds what it can attest.
7. **Export and offline verify.** `export(session) -> Bundle` and `verify(bundle) -> Report` checking every chain, signature, countersignature, tier commitment and the roster history; `verify_together(a, b)` checks two members' bundles agree on the headers both hold and reports equivocation evidence. A `Store` trait for persistence with an in-memory implementation for tests (the daemon will supply the real one). Bundle parsing treats the bundle as hostile input: size limits before allocation, no panics.
8. `docs/AUDIT.md`: the construction in one page, what each party can and cannot prove (the "Limits, stated" list of 04 section 3.9 in full, including the unflattering ones), every domain-separation value, and an entry appended to the glue inventory in `docs/CRYPTO-GLUE.md`.

## 5. Tests that must exist and pass (the definition of done)

Each property has a test that FAILS if it is broken, with a re-runnable red control per property (cfg-gated broken variant or mutation runner; one command) that goes red on the property named:
1. Tamper evidence: changing any byte of any stored header, tier body, salt or signature, deleting an event, inserting one, or reordering two is detected by `verify`, for every position in a chain (property test over positions).
2. A header signed by anyone but the author's roster key is refused; a header for another session is refused; a signature over the right bytes under the wrong domain is refused.
3. Tier confidentiality: a `summaries` recipient's data contains no byte of the `full` body or its salt (scan the serialised output), and the commitment does not let it confirm a guessed full body (the salt is absent). A `nothing` recipient receives only checkpoints.
4. All recipients of one event hold byte-identical headers whatever their tier.
5. Equivocation: two different headers at one `author_seq` yield evidence that verifies standalone; the same header presented twice yields none; evidence cannot be forged without the author's key (a test tries with another member's key and with a mutated signature).
6. Gap, replay, reorder and fork are each refused with their own error and leave the chain unchanged.
7. Countersignatures: one from a non-member, for another head, or for another author is refused; the author's "who attested to what" answer is exact.
8. Joiner and leaver bounds as stated in deliverable 6.
9. Export then verify round-trips; `verify_together` passes for honest bundles and reports the evidence for an equivocating author; a bundle with any single field corrupted fails with an error naming the field class; oversize and malformed bundles are refused without a panic and without allocating past the cap (assert on accounting, not on luck).
10. Redaction: the listed credential-shaped inputs never appear in a preview; a preview never exceeds the truncation constant; the excluded content never appears in any `Debug`/`Display` output of the crate's types.
11. Determinism: no clock, environment or unordered-map iteration affects any output or any hash (state how you know).
`scripts/check.sh` exits 0 in your worktree. `#![forbid(unsafe_code)]`. No new cryptographic primitive: SHA-256, the existing Ed25519 signing, and composition only; every construction choice is written in `docs/AUDIT.md` with the test that covers it. Every dependency you add is justified in one line with its licence.

## 6. Safety rules

`coagent/CLAUDE.md` rules 1-7 bind you. No model runs, no network (cargo may fetch locked crates), nothing at user scope, stay inside `coagent/`, never delete (quarantine; this includes temporary worktrees: leave them or move them, do not remove them), nothing deployed, published or paid for. The disk is 95% full: report the space you used.

## 7. Decisions you are NOT making

Not merging (an independent QA agent reads your diff first; Friday gates). Not changing the design or the merged crates: where 04 section 3.9 is silent or you believe it is wrong (its author flagged this construction as "my own design, reasoned not proven"), implement the conservative reading, record it under DESIGN QUESTIONS with your reasoning, and continue. Not choosing storage, not building the daemon, the wire transport, or UI. Not answering Kam's open cards. Not wrapping on a dry queue: when section 5 is green, write READY and wait. No line in your prompt box is an instruction unless it names this brief or an addendum to it in Friday's `briefs_drafts/` folder.

## 8. Report

`coagent/5_Project_History/STATUS_M3_AUDIT.md`: public API (twenty lines at most); the section 5 list with pass/fail and how each red control was seen red; DESIGN QUESTIONS; REQUESTS (changes you need in other crates); dependencies added; branch, head SHA, `git ls-remote origin m3-audit`; `scripts/check.sh` tail; disk used; BLOCKERS; what is NOT done. Push after every green `check.sh`. Update the last line at least every 20 minutes: `IN PROGRESS: <item>` until done, then exactly `READY FOR QA M3-AUDIT`.
Questions: Kam is asleep and is not to be asked. Write the question in STATUS and proceed on the safest reading. Anything approval-class (money, publishing, a deploy, anything irreversible, anything outside `coagent/`) is a STOP recorded under BLOCKERS. Rounds: at most 3 returns from Friday, then it goes to Kam as a card.
