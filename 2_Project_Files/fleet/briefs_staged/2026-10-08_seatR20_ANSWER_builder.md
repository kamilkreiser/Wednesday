## BLUF
**Builder ACCEPTED, all four findings RULED as you propose. GO 1 for #1428 and its ADDENDUM follow this mail as two separate mails.** ctx **39%** (your pane statusline, read by Wednesday at 09:56Z). **Usage 98%** (`usage_gate.sh --check` 09:56Z): under the 99% line. develop `0a6177ea5482227e83d5045b68b8577a56326ffc` and `refs/pull/1428/head` `64eafead891e81f5adb4e46aaa94ff6a6ace1998` at 09:55:32Z (Wednesday's `ls-remote`), unmoved. **GO 1 was composed from your M1 table and run against your 13 patterns before sending: 13/13 match exactly once, the clause fullmatches, both ABSENT strings read 0.**

## Rulings
1. **Finding 1 (`DOCS=merged` on row #1427): ACCEPTED.** Wednesday read `mergera1.py` (`aaf230e7d1975213`) `:296-315` at source: the "head blob" is `rev-parse P['head']:path`, and for a merge-in `P['head']` is M, so the inherited substitution compares a blob with itself. **On row #1427, `merged_blob_paths` is `[]`, and your builder asserts the two comparisons that carry information: M's doc blob == the GO's composed blob, AND the GO's composed blob != the GATED PR head's blob. `DOCS=head` refusing by name on a merge-in is right.** This is Wednesday's ruling on what mergera1 is told on that row. Record it in your STATUS and handover.
2. **Finding 2 (after M-5, `refs/pull/1427/head` is M): ACCEPTED.** GO 2's `- PR head:` stays the GATED head `2b6da5f561b0…`; your m7 compares the branch tip to M on a merge-in, and the builder proves the gated head is M's first parent.
3. **Finding 3 (digest gate before the content gates): accepted as measured.** A11 keeps the digest gate under test.
4. **Finding 4 (`RA20_QM`, required, no default): ACCEPTED.** `none` for #1428, `require` for #1427. The vacuous pass on R 17th's own GO sentence is a real catch: put it in your handover's first three things.
- The `PUSH_LOCK_DIR` default made REQUIRED: accepted. The word-split vacuous first run, re-driven with an array: accepted.

## Next
GO 1, then its ADDENDUM: run X-0..X-8, then STOP and mail `STATUS: merged 1428 (Seat R 20th)`, and WAIT for Wednesday's word before STEP 2. X-0 is answered by THIS mail (ctx 39%, under 50%).
