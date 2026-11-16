This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It extends your brief and addenda 1 and 2. Report in a section "ADDENDUM 3 (gate return)" of `coagent/5_Project_History/STATUS_M3_ROSTER.md`; while working the last line is `IN PROGRESS: A3 <item>`, and when done exactly `READY FOR QA M3-ROSTER r2`.

# M3 ROSTER — gate return (NO GO at 0a47fc9: two Majors, no Blocker)

## 0. Where you stand

The independent gate (Opus, own clone) reproduced your figures: `scripts/check.sh` exit 0 on 5 of 5 runs (301 workspace tests, 69 in the crate); 29 of 29 roster red rows red, each on its named property; the core runner unchanged; the four protected files and both root manifests byte-identical to main; no public line removed; the pinned encoding confirmed independently on a main checkout. It merged your branch into `origin/m3-audit` (417 passed) and `origin/m1-daemon` (compiles; its process tests could not run in the gate's long scratch path). 61 mutations: 49 killed. Two Majors stand, and neither has a test in your suite. This is NO GO round 1 of two for this crate.

Read the verdict WHOLE: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/m1_review/gate_M3_ROSTER_verdict.md` (202 lines). The gate's tests and mutation driver: `…/m1_review/gate_roster_tests_m3/` (`qa_gate.rs`, `qa_pin_gen.rs`, `mutate.py`, `mutation_results.tsv`).

## 1. What to do, in order

1. **First commit: the gate's test file `qa_gate.rs` added unchanged** under `crates/coagent-roster/tests/` (a wrapper with `#[rustfmt::skip]` if needed, as the core seat did); record which of its 22 tests are red at 0a47fc9 (the gate says 3: F1 and F2). It is a gate file from now on: never weakened, never deleted.

2. **F1 (Major): a member admitted as an observer through a proposal can never be promoted.** `check_proposal_shape` (lib.rs:659-664) is run for every entry with a record on EVERY version (lib.rs:596-598). FRIDAY'S RULING: "the role in the entry may not be higher than the role proposed" is an ADMISSION rule. It is checked only on the version that adds the entry (the transition from a previous version in which the key is absent). It is not checked on later versions, and not on a joiner's first roster for entries that the joiner did not see admitted. Everything else about the record stays checked as now (the signature is over the role in the record, not the entry's role, so the record stays verifiable after a promotion: the gate confirmed this). Write into `docs/ROSTER.md`, plainly, what a joiner therefore cannot check about entries admitted before it joined (it trusts the chain it was given for the roles those entries were admitted with). Tests: the gate's sequence (admit as observer, promote in the next version: accepted by a chain holder and by a joiner given the later version first); a role raise ON the admitting version still refused; red row "role rule skipped on the admitting version" stays red on its named test.

3. **F2 (Major): the intake can return an approval that every validator refuses, after it has already changed its own state.** Fix it as a CLASS, not for the two inputs the gate used:
   - `approve` builds the next body and runs the SAME validator a member would run on it (the transition from the current version) BEFORE it changes any state. If the body does not validate, `approve` returns an error naming the validator's reason and the intake is exactly as it was, except that this one proposal is marked refused-invalid and its proposer's quota stays charged. No other proposal becomes stale, no other proposer is charged. Property test: over generated intake states and proposals, every body returned by `approve` is accepted by a fresh `RosterChain` at the current version; and after a refused approval the accounting of every OTHER proposer is unchanged.
   - `receive` refuses, before any card, a candidate that the validator would refuse on sight: its signing key or its channel (Noise) key equal to any CURRENT member's (the gate's "own signing key with a fresh Noise key" twin), each with its own error. Compare keys, not only key ids.
   - At the version bound: `receive` refuses when the current version is already `MAX_VERSIONS` (an approval could not build a valid next version), and `next_with_cap` likewise.
   - `approve` with an `added_at` the validator would refuse (the gate's M48 survivor) is refused the same way.
   Red rows: "approve does not validate before changing state" (guard: the property test; the failure must say an approval produced a body the validator refused), "candidate signing key compared by key id only", "intake accepts at the version bound".

4. **F5: an approval must report what it made stale.** `approve` returns, with the body, the list of proposals it made stale (id and proposer), so the daemon can tell those proposers; `tick` reports expiries as now. Test and red row.

5. **F3: starvation is bounded and must be visible.** Keep the bounds. Add to the intake a small counter per proposer of proposals refused because the session's pending slots were full (bounded: at most one counter per current guest; it stores no proposal), readable by the starter's side, so the starter can learn that an honest member is being crowded out. State in `docs/ROSTER.md` the measured bound (the gate: 80, 100 and 130 minutes for 3, 4 and 5 colluding guests with the starter idle; formula ceil(8·h/3)·TTL) and what ends it (one "decline and mute" per hostile guest, or a removal). Test with the gate's attacker.

6. **F4: the wire form of a proposal.** FRIDAY'S RULING: the `member.propose` envelope carries the signed proposal as ONE opaque string (the canonical bytes, hex or base64: choose one, say which and why), never as a nested JSON value, so the 2,048-byte bound is applied to the string before any decoding and the bytes that were signed are the bytes that arrive. The intake keeps taking bytes. Correct your DESIGN QUESTION 6 and REQUEST 3 accordingly, and add a test that a proposal carried through a JSON value (re-serialised) is refused while the string form is accepted.

7. **F6 and your DESIGN QUESTION 3: the "removed person" rule.** FRIDAY'S RULING: do not try to close it in this crate. A removed person can always come back under entirely new keys if a member proposes them and the starter approves; the system knows keys, not people, and the starter's approval is the control. So: keep the key-id rule as it is; CORRECT the docs, which over-claim ("Refused before any card"): say exactly what is refused (the same key id) and what is not (the same person, or the same signing key with a new channel key), and that the approval card is where a human must recognise them. Add under DESIGN QUESTIONS, for the design owner: whether the card should show "this signing key was removed at version N" (which needs removed entries to keep their signing key, a change to the `Removed` type the audit crate imports), and whether the verify-attempt inheritance rule should follow the signing key rather than the slot. Build neither.

8. **F7: the eight surviving mutants that are real checks** (M11, M42, M48, M52, M56, M57, M58, M60 in the verdict's table): one guard and one red row each.

9. **F8: no owner name and no internal card id in committed files.** Seven committed lines name the owner and quote card ids. Replace each with a neutral reference ("owner ruling of 2026-11-17", "design addendum 06 section N"). Then scan every file your branch adds or changes for the owner's name, a card id pattern, an absolute path and a user name, with a positive control, and put the scan and its result in STATUS.

10. **F9, F10, F11: record, small fixes only.** F9: a refused input that arrives after a pending proposal's time has passed changes the accounting through `tick`; that is correct behaviour, so add the test that crosses a TTL and say so in the docs ("a refusal stores nothing NEW"). F10: "duplicate proposal id" is a per-version rule; say so in the docs. F11: "who may sign a version" is decided in two places (`is_roster_signer` and the key pinned at `start`); name both in STATUS and in `docs/ROSTER.md` so the later deputy lane finds them.

11. **F12 (not yours to fix): REQUEST.** Record under REQUESTS that the daemon's test harness places its Unix socket under a path that exceeds the 104-byte limit when the checkout path is long, so the merged tree's 28 process tests are unverified for this branch until they are run from a short path.

12. `scripts/check.sh` exit 0; `scripts/red-controls-core.sh`; `scripts/red-controls-roster.sh`; the gate file 22 of 22; push. Then STOP at the READY line.

## 2. Decisions you are NOT making

Not merging. Not weakening or deleting any gate test (the two protected roster gate files stay byte-identical to main; `qa_gate.rs` is added unchanged and stays so; if one of its assertions conflicts with a ruling in this addendum, STOP, quote the assertion in STATUS and wait). Not building anything for a deputy. Not changing the `Removed` type, `Member::new`, `RosterBody`, `Applied`, `CAP`, or any other crate. Not changing a number in the bounds table. Not wrapping on a dry queue. Lessons of the brief's section 2 bind unchanged. No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.

## 3. Report

Section "ADDENDUM 3 (gate return)": the gate file's red/green at 0a47fc9 and at your new head; per finding F1 to F11 what changed, the test and the red row with the panic text seen; the property test of item 3 (generator, cases run); the scan of item 9; public API added or changed since 0a47fc9 and proof the in-flight crates' calls still compile (the api-stability test); tails of check.sh and both runners; head SHA and `git ls-remote origin m3-roster`. Every UNKNOWN names why and what closes it. Last line exactly:

`READY FOR QA M3-ROSTER r2`
