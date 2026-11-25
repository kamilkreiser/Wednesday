This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-25_coagent_AUDIT-HOST-NOTES_brief.md`. Seat AUDIT-HOST-NOTES only. Report under "## ADDENDUM 2 (Q1 answered)" in your STATUS file.

If your context was compacted: re-read your brief, addenda 1 and 2 and your STATUS file WHOLE before doing anything.

# AUDIT-HOST-NOTES ADDENDUM 2: Q1 answered: (b), with two small additions

You were right to stop, and the enumeration is exactly what addendum 1 asked for. The check's rule is "an answer the code can give that no row names", and the next lane wires the daemon by this table alone, so the table names them. The ruling:

1. **Append ONE more row (row 15), in your own proposed words, the 14 rows now there byte for byte and in order:** case "A seal call refused before it started (`SealInProgress`, `NoSealInProgress`, `TriggerOff`, `NotDue`)"; the answer "That `Err`; nothing written"; what the caller may retry "The seal when the condition holds (no window open; a trigger due)". If a word of it is not true at source for one of the four answers, write the true form and say so in STATUS.
2. **Row 14's parenthetical names what its case already covers:** add `ArchiveMismatch` and `Audit(ExportTooLarge)` to it (the bound and encode answers you found), so nobody has to infer them. This changes row 14, which addendum 1 had you write: quote it before and after.
3. **The two test-only answers** (`SealStaleTwice`, and a stale re-plan's step 1 or 2 `Err` inside the window): one sentence directly under the table saying that they can be produced only through a test hook and cannot occur in the host as built, with the docs section that says why (your §6 pointer). No row for them.
4. **Pin it:** `tests/notes_docs.rs`: 15 rows; the new row and the widened row 14 pinned; the in-test mutated copy fails when row 15 is removed (quote the panic line). Update your enumeration in STATUS so that every answer names its row or the sentence of item 3.
5. Everything else of addendum 1 stands: NO code change (the zero-byte diff of the crate's sources and red script against `52ad858`, with its control, re-quoted at the new head); `cargo fmt --all --check`; clippy for the crate; `cargo test --locked -p coagent-audit-host --test notes_docs`; push only `audit-host-notes`; no merge of main; the last line `READY FOR QA AUDIT-HOST-NOTES r2` with the new head SHA in the line above it.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
