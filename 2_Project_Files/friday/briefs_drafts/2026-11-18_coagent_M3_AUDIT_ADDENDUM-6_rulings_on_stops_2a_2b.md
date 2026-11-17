This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. It answers the two STOPs in your STATUS section "ADDENDUM 5 (one check return)" under "STOP — A5 item 2 (R4-M1)". Everything in addendum 5 that is not named here stands, including its last line `READY FOR QA M3-AUDIT r5`. Report under "ADDENDUM 6 (rulings on 2a and 2b)" inside your addendum 5 section.

# M3 AUDIT — ADDENDUM 6: rulings on STOP 2a and STOP 2b

You were right to stop on both, right to park the work off the pushed branch, and right not to choose. STOP 2b is a fault in Friday's wording of (d), found by your property within the hour; the charging rules I-A11, I-A12 and I-A13 stand as you built them.

## 1. STOP 2b: which form of (d) binds

`DESIGN RULING (Friday, I-A15):` (d) as written in addendum 5 ("the free part's usage is never larger with peers than without") is WITHDRAWN. Your causes 2 and 3 show why it cannot hold: when a requester pays for a checkpoint that also covers V's own events, room stays free that V's own later records then use. That is V using V's own space, not a peer consuming it. The form that binds is the one you found, in two parts, plus one stated limit:

- (d1) Content. Every record in the free part is an own-choice event of V (`record`, `announce_share_level`) or an own checkpoint that covers no requested event. Nothing recorded at a peer's request, and no checkpoint covering such a record, is ever charged to the free part.
- (d2) Empty without own calls. In any schedule in which V makes no own-choice call and no explicit own checkpoint call, the free part is exactly empty (0 bytes, 0 records), whatever peers do.
- (d3) The one way a peer still touches V's own records, stated and bounded, not removed: a peer's accepted requests advance V's sequence numbers, and a sequence number is written in decimal, so an own record made later can be a few bytes larger than it would have been (your cause 1: 939 against 937 bytes after nine requests). Do NOT change the exact-size accounting of design 07 for this. Assert the bound instead: for the same own call, the stored own record with peers is larger than without by at most the difference in decimal width of the two sequence numbers (and of any other number in the record that requests advance; name each).

P10 changes accordingly: it asserts (d1) at every step by reading the free part's records, (d2) on the schedules that qualify (keep the reach count for them above zero), and (d3) per own record; it no longer compares total usage between the two runs. Keep the three counter-schedules you found as named tests that document WHY the withdrawn form fails (each asserts what actually happens: the larger own record, the accepted 1,500-byte record, the ninth record). The red control `requested_cp_on_free` must turn (d1) red on its own text.

Docs: `docs/AUDIT.md` states (d1), (d2) and (d3) in plain words in place of the sentences addendum 5 item 2 listed, including the sentence that a member's later own records may use room that a requester's payment left free.

This SUPERSEDES addendum 5 item 2 (d) first clause, item 2 "Tests required" (ii), and the last line of addendum 5's SUPERSEDES section (the replacement text for design 07 §1.6 item 2 is now (d1) to (d3) above).

## 2. STOP 2a: the gate guard `r4_guard_an_own_checkpoint_is_space_checked`

`RULING (Friday, 2026-11-18, addendum 6):` a ruled edit of this one test in `gate_r4.rs` is permitted, and only this:

- The guard exists for one rule (the gate's mutant M23): an own checkpoint the FREE part must pay is refused `LogFull` when the free part has no room. Under I-A12 the checkpoints in its loop cover requested events, so their requesters pay and none is refused. Change the setup so that the checkpoint the guard expects refused is one the free part must pay: it covers no requested event (V's own-choice events only, or nothing). Keep the final assertion that this checkpoint returns `Err(AuditError::LogFull)` exactly as it is.
- Change as few lines as that requires. Above each changed line: `// RULING (Friday, 2026-11-18, addendum 6)` with the old line quoted in a comment. The `println!` lines stay; if a printed figure no longer exists, print its nearest equivalent and say so in STATUS.
- Then show, in STATUS, that the edited guard still does its job: with the space check on an own checkpoint removed (the gate's M23, or your red row for item 6's M23 guard) the edited guard goes RED on its own assertion text, and green on the branch.
- If the guard cannot be made to test that rule without changing its final assertion, STOP again and quote why.

The ruled edits of addendum 5 section 2 B for `r4_finding_requested_events_drive_checkpoints_into_the_free_part` (lines 160-163 and 187) go in as addendum 5 says; the asserted fixed property there is (d1) and (d2) for that test's own input (the free part stays at 0 bytes before any own record; own records possible equal the run without requests, apart from the (d3) width effect if it shows: state the figures).

## 3. Then

Put the parked item-2 work on `m3-audit` with these changes, in the order addendum 5 gives, and continue. The short check will rule on I-A11 to I-A15 and on every gate-file edit.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
