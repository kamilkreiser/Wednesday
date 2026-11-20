# FOR RECORDS: gate B1822 (round 2 of 2 of the card decoder lane; kit B1810), OXPd 2, WP1.3, head 9fe5356 on main c56f3f3

For a records pass. Sources: this gate's VERDICT.md (measured rows), the round-1 FOR-RECORDS.md (carried forward), the builder's
STATUS (RELAYED where the gate did not re-measure). Nothing below was filed, sent or decided by the gate.

## 1. State

- **Gate: GO WITH FINDINGS at `9fe53569da3e131c394f387ac4e8a1f78c6c9b82`.** Round 1's Blocker (time) and Major (the rest of a
  refused read) are closed by the gate's own run; findings 4 and 9 closed; D6 built. Six Minors, none a reason not to merge.
- The branch merges onto main `c56f3f3` with no conflict (measured); no pull request exists yet. Landing: `landing.txt`.
- **WP1.3, `OXPD2-13` and exit test E1.3 stay OPEN after this lane lands** (unchanged from round 1): the comparison with real
  readers and the golden files of spike S3 are not done. **Every golden value is PROVISIONAL. The server does not reference the
  library. Nothing reads a real reader.**

## 2. Round 1's list, marked

| Round-1 item | Now |
|---|---|
| Finding 1, time (Blocker) | CLOSED (VERDICT item 1); the old rule C9 (ii) retracted and gone from code and test names |
| Finding 2, the rest of a refused read (Major) | CLOSED for reads whose events keep arriving less than one window apart; the limit is in the comment |
| Finding 3, the UUID step | unchanged by rule; one sentence now in the code comment; list A item 2 stays |
| Finding 4, twelve untested behaviours | CLOSED (ten killed by new cells, two no longer apply, stand-ins killed) |
| Finding 5, one refusal per event for a reader that decodes nothing | unchanged; adapter kits |
| Finding 6, gap detection's step of 1 | unchanged; named limit; list B item 1 |
| Finding 7, two reads inside one window | now a named limit in the comment |
| Finding 8, the card string by a side door | the framework's JSON serialiser now leaves it out (D6); every other serialiser and a logger still read it; the test-helper rule stands |
| Finding 9, text | CLOSED |
| Finding 10, the README | unchanged; the one README pass after the wave |

## 3. New this round (each Minor; for the records, not for a third round)

1. **One wrong time value on two consecutive calls ends the discarding early** and gives the tail of the refused read as a card
   (measured: "1234" gives a refusal and `CARD 4`). Inside the named limit "two or more wrong times inside one read". For the
   adapter kits: the caller takes the time at each call; one stale value reused on two calls is two wrong times.
2. **Three behaviours of the new mechanism have no cell that can fail:** the time before the step kept from the first step of a
   series (gate mutant n3); `Reset()` clearing the owed end (n17; D4's property is not proven for that flag); a dropped repeat
   with bytes keeping the reader deaf (n22). Cells for the next lane that touches the assembler.
3. **D5's named exception is not in the comment:** one wrong time far ahead on an event in the middle of a read gives two
   refusals for one tap. The comment's "one read gets one refusal" is true in the assembler's terms.
4. **Chatter at one window or slower:** an event with bytes and no end once a second gives one refusal per event (15 in 15 s);
   faster chatter keeps the reader deaf and swallows the next card (the named cost).
5. **D3 counts a held event that gives no character** (a key release): stricter than "gave it a byte" read as a character;
   fails closed.
6. **The builder's STATUS does not say in words that the first seat ran on Fable**; the first seat made no line of the commit,
   and the attribution line names Opus 5.5, the model of the commit.
7. A dropped repeat of an old event with bytes keeps the reader deaf (item 2, n22): a transport that re-sends stale events
   would keep a printer's reader deaf. Whether any printer re-sends is UNMEASURED.

## 4. The builder's FOR TUESDAY and FOR RECORDS items, as a list (STATUS sections; the gate's reading beside each)

| # | Item | The gate's reading |
|---|---|---|
| 1 | The UUID step for the master list | unchanged; list A item 2 of round 1 |
| 2 | The window against a real reader (a reader slower than one window gives no card at all) | measured: reads of 960 ms to the Enter give 5 cards of 5; 1000 ms and slower give 0 of 5 |
| 3 | Head and behind_by 1 | measured; merges cleanly |
| 4 | D10's cost in the cells | measured independently: deaf to the tick (999.9999 ms swallowed, 1000 ms given) for four routines |
| 5 | THE SECOND QUESTION table | each row confirmed by the gate's required-question table; one more row found (section 3 item 1) |
| 6 | The review's mutants that no longer apply (six) | confirmed six; the gate's stand-ins: five killed, s32 equivalent |
| 7 | D6 built | confirmed |
| 8 | Findings 5, 6, 10 untouched | confirmed by the diff |
| 9 | The deaf time is what a person meets; whether an adapter tells the person anything then | decided by nobody; the adapter kits |
| 10 | FOR RECORDS 1 to 8 of the kit (one message per tap; README; no real card value in tests; never hand a result to a serialiser or logger; the adapter's caller rules; the window against a real reader; the open rulings; the older HP routine joining later reports after byte 13) | carried forward unchanged |
| 11 | DEVIATIONS: mutants by a program, not the Edit tool; six review mutants not applying; T15 not red under mT1; R18 row 3 limited to one wrong time per read; R07 and I04 call details | the gate's view: none affects the product; the R18 restriction is exactly the named limit the gate measured (section 3 item 1) |
| 12 | The successor's one `sed -i` on its scratch runner | no effect on the product |

## 5. Questions (none sent; adding them to `OXPD2-1` is the coordinator's)

Round 1's list A (the Datasec team, the family question first, with its consequence) and list B (questions only a printer can
settle) stand unchanged. Add to list B:

9. Does a printer ever deliver the same stale event again (a re-send) seconds after it was first delivered? Such re-sends keep
   the reader deaf after a refusal (section 3 items 2 and 7).
10. How long does one card read take on each reader, first event to last? The default window refuses a read of one second or
    more, and after this round a refused read gives no card at all (round 1's list B item 4, now sharper).

## 6. Open rulings, DECIDED BY NOBODY

Round 1's rulings 1 to 5 and 8 to 11 stand unchanged. Ruling 6 (what time the caller passes) and ruling 7 (what follows a
refusal) are now BUILT one way by the coordinator's kit (a time that never goes back, a step refuses; discard to the end or one
quiet window): built, and still decided by nobody beyond that kit. New:

| # | Point | As built | The other reading | Whose |
|---|---|---|---|---|
| 12 | What a dropped repeat does to the quiet window | keeps the reader deaf | does not count | decided by nobody; the next lane that touches the assembler |
| 13 | Which time before a step counts when steps come in a series | the first | the last (fewer partial cards under two or more wrong times, measured 42 against 62) | decided by nobody |
| 14 | One message per tap after two refusals for one tap (D5's exception) | two refusals | one | decided by nobody; the adapter kits |

## 7. Rules for the lanes that follow (round 1's rules 1 to 5 stand; added)

6. The caller of the assembler takes the time at each call from a monotonic clock under the lock that serialises the calls,
   never a cached or batch value, and calls `Tick` at least once per window.
7. Solution file: with the logging library on main, this lane's lines sit first in each block; the merged file is in
   landing.txt, line 2.

## 8. The gate's own trees

`/private/tmp/b1822-gate/` (not in any repository): `clone/` at the head (push URL `invalid://no-push`), `mut/tree/` (equal to the
clone after the last undo), `copies/gate/` (the round-1 copy, manifest-checked), `probes/Fuzz/` (round 1's harness plus the
gate's `R2.cs`), `logs/`, `scratch/`, `_quarantine/locks/` (165 released lock folders), `nuget-packages/` (a copy of round 1's
cache), `dotnet-home/`. In the session scratchpad: `b1822-merge/` (the merge of item 4, uncommitted) and `b1822-texts/`. The
wave's lock is released. Nothing was pushed; no pull request, ticket or setting was touched.
