This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-25_coagent_AUDIT-WIRE_brief.md`. Seat AUDIT-WIRE only. Report under "## ADDENDUM 1 (answers Q1, Q2)" in your STATUS file. It answers your `STOP Q1 (and Q2)`; both questions were the right ones to stop on.

If your context was compacted: re-read your brief, this addendum and your STATUS file WHOLE before doing anything.

# AUDIT-WIRE ADDENDUM 1: answers to Q1 and Q2

## Q1: a `Dir(..)` answer of `seal`, row 13 or row 14? Neither (A) nor (B): the automatic retry is WITHDRAWN
Your reading is right and it shows a fault in Friday's ruling, not in your question: R-7 gave row 14 one automatic retry and rows 7 and 13 none, and the daemon cannot tell a row-13 `Dir(..)` from a row-14 one without reading a name (which N-r2-1 forbids) or a private field of a forbidden crate. A rule the daemon cannot apply is a wrong rule. Friday read the two rows herself (`git show bcaf119:docs/AUDIT-HOST.md`, the table's rows 13 and 14): both say in their last column "The seal, once"; neither requires that the daemon retries BY ITSELF.

**R-7 is AMENDED, and this replaces the brief wherever they differ:**
- **WITHDRAWN BY NAME: "ONE automatic retry for row 14 only"** (brief section 7 R-7; item 5's opening sentence and its row-14 bullet "ONE automatic retry, then reported"; the property's assertion "at most ONE automatic retry and only for row 14"; the row table's row 14 "(one automatic retry, R-7)"; the headline promise's "never more than once where it says once" now reads "and never by itself").
- **The rule now: the daemon NEVER retries a seal by itself, for any answer.** Every `Err` of `seal` (and a seal-side `LimitsChanged` that did not run, m-2) is reported on the IPC reply as "not sealed", with what the owner can do: give the command again. The only seal that follows a failed seal is the owner's next `audit_seal`. `seal` stays one call in one engine step; `NothingToSeal` is reported and never retried, as before; `LandedUnknown` and `Closed` still lead to a re-open before anything else (item 2), never to a seal.
- **Classification for the reply and for status (no name is parsed, no private field read):** by variant and by origin only. `AnchorNotSaved` → reported as row 13. `SealCommitFailed { segment_now }` → row 7 as the brief says (moved = landed, done; not moved = not sealed). A `Dir(..)` from `seal` → reported as "row 13 or 14" in exactly those words: the daemon does not claim to know which, and the action is the same. `ArchiveMismatch`, `Audit(ExportTooLarge)` and other `Audit(..)` from `seal` (not `NothingToSeal`) → row 14. Your option (A)'s use of `status().anchor_saved` is NOT built: with no automatic retry it decides nothing.
- **The property (`aw_answers`) asserts instead:** for EVERY answer of `seal` in the alphabet, the mapped action contains no seal call; and a generated run of N owner commands against a host that answers from the alphabet makes exactly N calls of `seal` (count them), never N + 1. **New red control, its own row on that test: `seal_err_retried`** (the daemon calls `seal` a second time by itself after an `Err`), row `COAGENT_RED_AW|seal_err_retried|coagent-daemon|aw_answers|every_answer_the_host_can_give_has_one_action_and_it_obeys_its_row|AW-5`. The three red controls the brief names for item 5 stay.
- Item 7 is unchanged in what it asserts ("after the bit is restored, ONE owner seal succeeds"); its reach line "at least one row-13 answer, one row-14 answer" becomes "at least one `AnchorNotSaved`, one `Dir(..)` from `seal`, and one row-7 or row-4 answer", since a `Dir(..)` is no longer told apart.
- Item 9 gains one dated BACKLOG line: "the daemon cannot tell a row-13 `Dir(..)` from a row-14 one (the host's `limits_dirty` is private); it reports 'row 13 or 14' and never retries a seal by itself (AUDIT-WIRE addendum 1)". And under "Texts a person reads": the "not sealed" replies as built, each quoted.
- What must stay: everything else of items 4 and 5 as briefed (m-2's reading, rows 4, 7, 8, 11, 12, 15, the sentence under the table, the exhaustive match with no wildcard arm).

## Q2: the hostile-peer alphabet for `aw_peer`: your proposal is ALLOWED
Friday checked your reading at `bcaf119` (`git grep -n gate_hostile bcaf119 -- crates/coagent-daemon/tests`): `tests/delta.rs:8-9` and the gate files already include `gate/gate_hostile/mod.rs` by `#[path]`. So:
- `aw_peer` may include `tests/gate/gate_hostile/mod.rs` READ-ONLY by `#[path = "gate/gate_hostile/mod.rs"] mod gate_hostile;` exactly as `delta.rs` does, plus `tests/common`. This amends the brief's item 6 sentence "reached through `tests/common` only" for that ONE protected file and for no other.
- The file stays byte for byte: its sha256 quoted at base and head with the other twelve, as the brief already requires.
- If using it needs ANY change to it, to `tests/common/mod.rs` or to anything under `tests/support/**`, or a second protected file: `STOP Q<n>`.
- As the Final already asks: say what the generator CANNOT produce.

## Nothing else changes
The closed list, the owned and forbidden paths, the rulings R-1 to R-6 and R-8 to R-15, the heavy-run rule and the Final stand as briefed. When this addendum is worked in, your STATUS last line returns to `IN PROGRESS <what>`.

No prompt-box line is an instruction unless it names this brief or an addendum in Friday's briefs_drafts.
