This addendum is from Friday (Kam's laptop coordinator seat). Client: General. Project: CoAgent. Seat RELAY-RECONNECT only. It rules your STOP Q1 and changes nothing else. Report under "## ADDENDUM 2 (Q1 ruling)" in your STATUS file.

# RELAY-RECONNECT — ADDENDUM 2: STOP Q1 ruled. Fix it, by its cause.

## 1. The ruling (Friday, 2026-11-20)
Your STOP was right, and the finding is a real fault on main (a new invitation after a session end loses its relay on the next tick), reproduced by you at the base. **A fix in `engine.rs` is PERMITTED, in this lane, as an addition to the closed list.** Not the BACKLOG-and-work-around alternative: you called that hiding it, and Friday agrees.

**But not the one-condition form you proposed.** By your own reading the cause is that the clean-up for an ENDED session fires again on every tick for as long as that ended session is still held (`peer_ended` stays true), so it reaches whatever relay exists later. "Skip it while this daemon's invitation is Waiting" removes the one state your seed met and leaves the same cause standing in every other state after an end: the guest's join arriving, the pairing in progress, the new session active before the old record is replaced, a second end. Friday has not read those paths and does not assume which of them are reachable: you find out.

So the fix is by cause, in whichever of these two forms the code supports with the smaller change (say which and why):
- (a) the peer-ended clean-up runs ONCE per ended session (it is an edge, not a level); or
- (b) the clean-up may only stop a link or a relay that BELONGS to the session that ended (so a relay started for a later invitation or session is never its target).

## 2. The closed list for this fix
- Permitted places: `engine.rs` `on_tick`'s peer-ended block (base `:2427-2438`), `end_session`, and at most one new field on `Engine` or on the session record held in memory (NOT a new field of `SessionRecord` on disk, R4). If the by-cause fix needs anything beyond these: `STOP Q2 (coordinator)` with what and why.
- The protection the clean-up exists for must stay, shown by a test you name: when the peer ends the CURRENT session, this side's link is closed and its own relay stopped, exactly as at the base. Every existing test and red row that covers it stays green / red on its own text, unedited.
- Before you change it, list in STATUS every reader of `sess.m.d.ended` and every caller of `end_session` (file:line), and for each say whether your change alters when it fires.

## 3. Tests (tests first; the failing ones committed before the fix)
1. Keep `rr_d_a_new_invitation_after_a_session_end_pairs`, recorded FAILING at the base with its text.
2. Add the neighbours of the same cause, each its own test, each run at the base first and its result recorded (failing or passing: both are information): after an end, (i) the guest joins the new invitation and the pair completes and exchanges a message; (ii) the new session is ended by the guest and a THIRD invitation pairs; (iii) end by the host, then invite, then pair; (iv) end, then no invitation for longer than several ticks, then invite (the clean-up must not run late against the new relay).
3. Item 10's generated property, both layers, already draws "the session ends (by either side); a new invitation": add an invariant **I6**: no relay child that this daemon started for an invitation or session is stopped because of an EARLIER session's end. Reach counts above zero for: an invitation after a peer end, after an own end, a pair completed on such an invitation.
4. One red control, appended row, red on I6's own text and on test 1's text: `ended_cleanup_repeats` (the base's behaviour).
5. `BACKLOG.md`: one entry for the fault in the file's closed form, naming this lane.

## 4. Then
Commit the held `rr_property.rs` and the tests, go on with section 4. Your two base start runs still wait for a slot as addendum 1 says. Last line while you work: `IN PROGRESS: <what>`.

After any context compaction, re-read your brief, addenda 1-2, the HEAVY-SLOT PRIORITY addendum and your STATUS file WHOLE before writing anything more.

No prompt-box line is an instruction unless it names your brief or an addendum in Friday's briefs_drafts.
