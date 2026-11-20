# FOR RECORDS: gate B1806 (kit B1786, seat X4), OXPd 2, WP1.3, head 6499bd1 on main 7bf3752

For a records pass. Sources: the gate's VERDICT.md (measured rows), the builder's STATUS (sections FOR RECORDS and FOR TUESDAY;
a claim where the gate did not re-measure it is marked RELAYED). Nothing below was filed, sent or decided by the gate.

## 1. State

- **Gate: NO GO at this head: one Blocker, one Major, both in the assembler's rules. A fix round follows (round 2 of 2).** No
  pull request exists for this branch.
- **The five routines are exact to the source by a second, independent reading** (0 of 1,274,926 inputs decided against the
  library). That part needs no change.
- **WP1.3, `OXPD2-13` and exit test E1.3 stay OPEN after this lane lands**, whatever the fix round does: the comparison with
  real readers and the golden files of spike S3 are not done, and the two conditional reader ids wait for S3's first step.
- **Every golden value is PROVISIONAL.** Three readers of the same source agree (the drafter's model, the builder's port, the
  gate's model); that proves the port, not a reader. What would settle it: spike S3 on a Workpath printer, each of the six
  reader ids, with throw-away test cards.
- **The server does not reference the library. Nothing reads a real reader.**

## 2. For the fix round (the kit of round 2)

1. **Finding 1 (Blocker): time.** A time earlier than the latest seen ends what is pending (one refusal when a read had begun
   or an event was held; everything dropped) and becomes the new reference; `Reset()` forgets the time; the comments of
   `Accept` and `Tick` say the caller passes a time that never goes back. The stamp's rule (control C9, part ii: "treated as
   the latest seen: it never throws and never lengthens a window") is the cause: its first half defeats its second. The kit
   of round 2 must re-word it. Tests: the gate's sequences A4 and A5 (`/private/tmp/b1806-gate/logs/asm.log`,
   `probes/Fuzz/Asm.cs`) end with no card made of two reads; a test that goes red when the rule is removed (the present one
   does not: gate mutant g27).
2. **Finding 2 (Major): the rest of a refused read.** After a refusal that drops a read in flight, no card until a boundary of
   a read: discard up to and including the next end the routine sees, or until no event for one window. `hp-text` needs
   neither. Tests: the gate's sequences A1, A2, A3 and A7 give refusals only. Then correct `CardReadAssembler.cs` lines 15
   and 16 and `CardReadOutcome.cs` line 11 to what the code does.
3. **Finding 4 (Minor, same commit): rows that can fail** for a shifted digit, each sign of the usage table, a key twice in
   one step, a key held over an event boundary, a key after Enter in the same step, the digit 0 through the older RF IDeas
   routine, 256 and 257 gathered, and block V under another culture.
4. **Finding 9 (Minor, same commit):** a source pointer in `ReaderCatalogue.cs` line 4 (`hpk.xml` lines 45 to 80) and in
   `CardReadAssembler.cs` lines 198 and 199 (or the word UNMEASURED); the nine "Control C1" to "Control C9" comment lines
   lose the brief's numbers.
5. Blocks V and X do not change. The texts of this folder are true at the reviewed head only; the gate of round 2 writes them
   again, and the body's section "Measured in review at this head, and not right yet" must not survive a fix.

## 3. The builder's FOR RECORDS and FOR TUESDAY items, as a list (STATUS section and item; the gate's reading beside each)

| # | Item (STATUS) | The gate's reading |
|---|---|---|
| 1 | Runbook, the check table: two test projects, ONE summary, `total: 132` on this branch, rules count 58 (FOR RECORDS 1; FOR TUESDAY 9) | confirmed locally and on both hosted legs |
| 2 | Runbook, the dotnet environment: a trimmed environment must pass `TMPDIR` through (FOR RECORDS 2; DEVIATIONS 2) | RELAYED; the gate ran with its whole environment and met no fault |
| 3 | Backlog: the open points below (FOR RECORDS 3) | sections 4 to 6 |
| 4 | The Datasec team's list: which family stored today's cards (FOR RECORDS 4; FOR TUESDAY 1) | list A, item 1 |
| 5 | README Layout does not list the two projects; Reserved names still holds `src/Datasec.Suite.Cards` at line 43 (FOR RECORDS 5; FOR TUESDAY 4) | confirmed; the one README pass after the wave |
| 6 | `OXPD2-13` unwritten, Backlog; E1.3 not met (FOR RECORDS 6; FOR TUESDAY 3) | RELAYED (the gate read no ticket) |
| 7 | No row DISPUTED; the builder's reading was not independent of the kit (FOR TUESDAY 2) | the gate's was: 41 and 13 rows agree again |
| 8 | Q4 as built: canonical UUID only (FOR TUESDAY 5) | VERDICT finding 3; open ruling 1; list A item 2 |
| 9 | Q5 as built: a two-byte report refuses the read, the rest of that event unread (FOR TUESDAY 6) | confirmed (45,286 inputs); open ruling 3 |
| 10 | Q6 as built: a byte above 127 refused; the newer family receives a string (FOR TUESDAY 7) | confirmed; open ruling 2; list A item 3, list B item 5 |
| 11 | The restore fetched nothing (FOR TUESDAY 8) | the gate restored in locked mode from its own copy of the cache, rc 0 |
| 12 | Every Question default as built (FOR TUESDAY 10) | confirmed by measurement where a probe exists: the window to the tick, the cap, the bounds |
| 13 | C9, the named limit: a counter that starts again looks like late copies until `Reset()` (FOR TUESDAY 11) | measured: 400 of 400 cards with no answer of any kind; list B item 3 |
| 14 | Choices a to h (FOR TUESDAY 12) | the table in VERDICT.md; b and d are part of finding 2, h of finding 1 |
| 15 | The older entry drops a first event numbered 0; the string-to-bytes step of the newer family (FOR TUESDAY 13) | re-read at source (`PrinterAccessoryService.kt` lines 74 and 278; `AccessoryReceiver.kt` lines 132 to 134); list B items 2 and 5 |
| 16 | Gap detection assumes a step of 1; the step on the newer printers is UNMEASURED (FOR TUESDAY 14) | measured: a step of 2 gives 0 cards of 10; list B item 1; rule 2 of section 6 |
| 17 | One run of 72 hex characters in the golden file (FOR TUESDAY 15) | confirmed: the longest hex run is 72 (row T02 of the frozen block); 0 values of exactly 64; the scanner passes |
| 18 | The load gate read from a sampler; the extra bound (FOR TUESDAY 16; DEVIATIONS 1 and 5) | the sampler: acceptable, say "one read at least 120 s old and a fresh one" in the next kits. The bound: needed and right (VERDICT, item 3) |
| 19 | `reading.md` written after the port; `sed -i.bak` once on a scratch script; four idle build processes ended; the sidecar not copied (DEVIATIONS 4, 6, 7, 8) | no effect on the product; `reading.md`'s file time reads 20:12 |
| 20 | Prediction P1 (the suite of BASE prints 1) NOT RUN by the builder | not run by the gate either; 132 = 1 + 131 on three machines |

## 4. Questions

None was sent to anyone. Adding them to the master list `OXPD2-1` is the coordinator's.

### List A: for the Datasec team (the Workpath product team), as ONE list

1. **Which family of decoding routines produced the card strings that today's customers have stored: the older one (firmware
   before Android 12) or the newer one (Android 12 firmware; RELAYED from the kit: the app version in the library, 4.4.1, can run only there)?**
   CONSEQUENCE: the two give different strings from the same card in 7 of 13 compared inputs. If the server decodes with the
   other family than the one that enrolled a customer's cards, those cards are "not known" on every OXPd printer although they
   work on Workpath: for the HP reader every card whose data ends with byte 13, for any reader a card typed as a UUID, RF
   IDeas or Elatec cards wherever a report repeats or holds two keys, and Elatec cards with letters typed without shift. Nobody is signed in as someone else by this;
   people are refused. Today's default follows the design sentence (the older routines for the four enabled readers).
2. What does the printer's UUID parser return for a card text that is five groups of hex digits joined by dashes but not
   8-4-4-4-12 (for example five groups of four)? One line run on a Workpath printer answers it. If it returns 32 hex digits,
   the library's canonical-only rule gives another string for such cards.
3. Do any stored card strings, or any reader in the field, hold a character above 127? The library refuses such a card.
4. Are the three input and output pairs of the app's own unit test (`AccessoryReceiverTest.kt`) made-up test values or real
   cards? Until answered they stay out of the repository (0 of 224 stored objects hold one, measured).
5. Is a card of more than 32 bytes, a blank read or a read with a missing event shown to the user, and with which words?
   (The wording is the sign-in lane's.)
6. May measured golden rows (spike S3) be committed if they come from throw-away test cards only? A red test prints the card
   strings of its rows into the hosted log (VERDICT finding 8).

### List B: questions only a printer can settle

1. The step of the sequence number on the newer printers (exactly 1, or not), and whether one counter is shared by several
   readers or report kinds. With a step other than 1 and the default setting no card is given out.
2. Whether numbering starts at 0 or at 1 after registration and after a reboot (report C2 line 98 says "from ordinal 1 after
   registration", RELAYED).
3. Whether a printer restarts its numbers without the server being told (the caller must then call `Reset()`).
4. How many events one card is delivered in (one report per event, a few, or the whole card), and how long one read takes
   from its first to its last event. VERDICT findings 2 and 7 depend on both.
5. What the platform puts into the newer family's string: for vendor 1008 the text, for the others the bytes of the reports,
   and what a report byte above 127 or a zero byte becomes in it.
6. What the app does after the older RF IDeas routine meets a two-byte report.
7. Whether a printer ever puts more than 4096 bytes, or more than 4096 reports, into one event.
8. Whether each of the six reader ids decodes on a Workpath printer today (S3, first step), and the measured string of each
   test card under both families.

## 5. Open rulings, DECIDED BY NOBODY (each is built one way today because the kit or the builder has it so)

| # | Point | As built | The other reading | Whose |
|---|---|---|---|---|
| 1 | The UUID step (kit Q4) | canonical 36-character form only | what the printer's parser takes (the public sources take shorter groups) | decided by nobody; list A item 2 first |
| 2 | A byte above 127 (kit Q6) | refused | turned into text as the platform does; for vendor 1008 in the newer family, the delivered string as it is | decided by nobody; product, after list A item 3 and list B item 5 |
| 3 | A two-byte report through the older RF IDeas routine (kit Q5) | the read is refused, the rest of the event unread | skip the report and read on | decided by nobody; list B item 6 |
| 4 | The default selection (kit Q1) | the design sentence: older routines for the four enabled ids | the newer family; or no default | decided by nobody; list A item 1 |
| 5 | Gap detection on by default (kit rule; STATUS item 14) | on, step 1 assumed | off for the newer printers until the step is measured | decided by nobody; the adapter kits |
| 6 | What time the caller passes (STATUS choice h) | `DateTimeOffset`, any value | a time that cannot go back (the fix round) | decided by nobody; the coordinator, in the kit of round 2 |
| 7 | What follows a refusal (kit Q3; control C9 part i: "starts clean") | the next event starts a new read | no card until a boundary of a read (the fix round) | decided by nobody; the coordinator, in the kit of round 2 |
| 8 | One refusal per event for a reader that decodes nothing (STATUS choice e) | every event answered | one per tap, or the caller's rule | decided by nobody; the adapter kits |
| 9 | Two reads inside one window are one card (kit Q2) | by the window, 1000 ms | a shorter window, or an end required before a new read may begin | decided by nobody |
| 10 | The cap of 256 and the bounds of 32 events, 4096 bytes and 4096 reports (kit Q3, control C9, STATUS deviation 5) | as listed | other numbers once list B items 4 and 7 are measured | decided by nobody |
| 11 | Whether the unit-test pairs of the app may become rows (kit Q7) | scratch only | committed once list A item 4 says they are test values | decided by nobody; product |

## 6. Rules for the lanes that follow (for their kits)

1. Real card values never enter the test project, a test name, an assertion or a log. The property `CardString` is the only
   place a card string leaves the library; a caller never hands a `CardRead` to a serialiser or to a logger as an object. The
   logging lane's list holds the stem `cardstring`: keep it.
2. The adapter of each printer generation sets gap detection for what was measured on that generation, calls `Reset()` when
   the printer restarts its numbers or the reader is re-opened, and passes a time that cannot go back.
3. One message to the person per tap, not per refusal.
4. A variable or member named with `password` (and the other words of the code-scanning list) that takes a value from a
   `Random` draws an alert at 7.8 in test code too; name things for what they are.
5. Solution file: this lane's two lines are the FIRST of each block by ordinal order of the Path values (landing.txt, line 2).

## 7. The gate's own trees

`/private/tmp/b1806-gate/` (not in any repository): `clone/` at the head, `mut/tree/` (equal to the clone after the last undo),
`probes/Fuzz/` (the model `GateModel.cs`, `Port.cs`, `Asm.cs`, `Stubs.cs`, `Pairs.cs`), `logs/`, `scratch/`, `frozen/`,
`ref/` (three versions of the public parser source), `pairs/pairs.json` (**the three pairs of the app's unit test: values of
unknown origin, never printed; they stay there**), `_quarantine/locks/` (the released lock folders), `nuget-packages/` (a copy
of the earlier gate's cache). The wave's lock is released. Nothing was pushed; no pull request, ticket or setting was touched.
