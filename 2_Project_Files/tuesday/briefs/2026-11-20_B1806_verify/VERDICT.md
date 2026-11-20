GATE B1806: NO GO @ 6499bd1 on main 7bf3752

Gate G1 Tier 1, round 1 of 2, OXPd 2, WP1.3, the card decoder library (kit B1786, seat X4). Head
`6499bd19bc73f56acc69101935bcbff163291a92` on main `7bf375268b9975ac9ece66579f7471ba7dbab11d`. Read and measured 2026-11-20,
20:18 to 20:50 AEDT (clocks by `date`), in the gate's own clone `/private/tmp/b1806-gate/clone` (push URL `invalid://no-push`).
Every number below was printed by a program; the programs and their logs are under `/private/tmp/b1806-gate/` (`scratch/`,
`logs/`, `probes/Fuzz/`).

**BLUF.** One Blocker and one Major, both in the assembler, both in rules the stamp wrote and the builder built as written.
So NO GO and a fix round. **The five routines are exact:** the gate wrote its own model from the source before it opened the
builder's code, and fed both 1,274,926 generated inputs: 0 inputs where the source decides against the library. **The Blocker:
when the time the caller passes goes back, or was once far ahead, no window runs out any more, and a read without its end is
put in front of the next card** (measured: a card of four digits made of two reads ten minutes apart). **The Major: after the
assembler refuses a read, it gives out the REST of that same read as a card** (measured: one lost event early in a card of 20
characters, one report per event, gives a refusal and then a card of the last 2 characters; a read slower than one second gives
the same with no fault at all). The class comment says "no part of a refused read is ever given out". Everything else the
builder claims was reproduced: scope, the frozen blocks, 132 tests, the seven mutants, the hosted lines, the no-copy check, the
three pairs. **Nothing reads a real reader yet and the server does not reference the library: no finding here can do harm
today. They are about what the two adapters and the sign-in lane would build on.**

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| 1 | **Blocker** (the commission's definition: a card string that mixes bytes of two reads) | **Yes** | **A time that goes back, or one time far ahead, stops every window, and a partial read is then put in front of the next card.** Measured (`logs/asm.log`, A4 and A5): read 1, two digits and no end, at 10:00:00; the caller's clock is set back one hour; read 2, two other digits and Enter, ten real minutes later: ONE result, a card of all four digits. With the clock running forward the same calls give `Refused: Incomplete` and then the card of read 2 alone (the control). The same through `legacy-hp`, 59 minutes after the step. After ONE call with a far-ahead time (a `Tick` with the largest time, or one `Accept` a day ahead) it is permanent: a read with no end is still waited for one day later, `Reset()` does not heal it, and a held event is given out as a card when its missing neighbour arrives 11 minutes late (three cards at once). In the soak (`logs/soak.log`): 1% of events lost, gap detection off, the clock set back 10 minutes once in 200 reads: 113 cards MIXED from two reads in 20,000 reads; 0 in the same row without the clock step. Cause: `Advance` (`CardReadAssembler.cs` lines 222 to 233) takes any earlier time as the latest seen, so time stands still until the clock passes the latest again; `Reset` (lines 201 to 209) keeps the latest time. **This is the stamp's rule (control C9, part ii) built as written; its two halves cannot both hold: "treated as the latest seen" is what lengthens the window.** The test named for the rule (`A_time_earlier_than_one_already_seen_is_the_latest_seen`) stays green with the rule removed (gate mutant g27 survives), and one of its own lines shows a card taken after the largest time. Preconditions, said plainly: the caller passes wall-clock time and that clock steps back (a time correction, a restored virtual machine) or gives one wrong value; and a read is pending without its end, or an event is missing. | In the fix round: a time earlier than the latest seen ENDS what is pending (one refusal if a read had begun or an event was held; everything dropped) and becomes the new reference, so no read outlives a step of the clock; `Reset()` forgets the time; the comment of `Accept` and `Tick` says the caller passes a time that never goes back (a monotonic clock, not the wall clock). Tests: the A4 and A5 sequences end with no mixed card; a test that fails when the rule is removed. The rule itself is the coordinator's to re-word. |
| 2 | **Major** | **Yes (round rule)** | **Part of a refused read is given out as a card.** After any refusal that drops a read in flight (the held-events bound, the window, the cap, the byte bound) the assembler "starts clean" at the next event, which can be the middle of the same card. Measured (`logs/asm.log`): A1, one report per event, event 3 of a 20-character card lost, all 42 events inside 42 ms: `Refused: MissingSequence` at the 33rd held event, then a CARD of the last 2 characters; a 36-character card: a CARD of its last 18 characters. A3, NO fault, a read of 10 digits at 150 ms per report: two `Refused: Incomplete`, then a CARD of the last 2 digits. A7 (the builder's choice b): the base moves to the highest number held, a genuine event of the next card arrives 14 ms late and is dropped as a late copy, and the next card is given out without its first character. A2: the same after the cap of 256. Soak, 20,000 honest reads each (`logs/soak.log`): 1% of events lost, one report per event: 538 wrong cards (each a part of one read); no fault but 30 ms between reports (reads of 0.5 to 1.5 s): 8,419 wrong cards; a whole read per event, or 1 to 6 reports per event: 0 wrong; both controls 20,000 exact, 0 wrong. The class comment (`CardReadAssembler.cs` lines 15 and 16: "no part of a refused read is ever given out") and the enum comment (`CardReadOutcome.cs` line 11) are untrue as measured; the test `A_read_with_a_hole_gives_one_refusal_and_no_part_of_it_leaves` only covers a read whose events all arrive before the refusal. Effect on a person: a wrong string is looked up; normally "card not known"; where another person's card string equals the part given out (short numeric cards), that other person is signed in. How many events a real printer uses for one card, and how fast a reader types, are UNMEASURED: if a printer delivers a whole card in one event, and reads take well under a second, this does not arise. The source for the same loss gives the card with one character missing (the gate's model): HP's advice to refuse such a read (report C2 line 98) is the reason for the rule. | In the fix round: after a refusal that drops a read in flight, give out NO card until a boundary of a read is seen: discard up to and including the next end the routine sees (Enter, byte 13, byte 40), or until no event has arrived for one window; `hp-text` needs neither (one event is one card). Tests: the A1, A3 and A7 sequences give refusals only. Correct the two comments to what the code then does. |
| 3 | Minor (decided by nobody) | No, but settle before any comparison with real readers | **The UUID step takes the canonical 36-character form only (kit Q4); every public implementation of the parser the source calls takes more.** The public documentation says only that the text must "conform to the string representation as described in toString" or the parser throws; it says NOTHING about shorter groups (read in the public OpenJDK source, `openjdk/jdk8u` `jdk/src/share/classes/java/util/UUID.java` lines 177 to 209, whose `toString` text at lines 357 to 365 gives every group a fixed length, and `openjdk/jdk` tag `jdk-11+28` `src/java.base/share/classes/java/util/UUID.java` lines 182 to 228, by GET on 2026-11-20). Both implementations DO take shorter groups (five groups of hex digits joined by four dashes, of almost any lengths) and print 32 hex digits. Which implementation a printer's firmware runs is UNMEASURED (the Android source could not be read inside the gate's fences). Inputs where a lenient parser gives another string than the library: 4,116 of 259,013 (`keyboard`) and 3,057 of 248,816 (`hp-text`), all from the gate's generator of such shapes. The shape that matters: a card whose reader types its number as dash-separated groups, for example five groups of four hex digits. | One question for the Workpath team (FOR-RECORDS.md, list A, item 2): what does their printer's parser return for a text of five short groups. Do not change the code blind. |
| 4 | Minor | No, but add in the fix round | **Twelve behaviours have no test that can fail** (gate mutants that leave all 132 tests green, `logs/mutants.out`): g1 only the left shift bit counts (rows K03 and K04 say they show shift, but the lower-casing hides it: no row types a shifted digit or sign); g2, g3 two rows of the usage table (no row types a sign but the dash); g6 a key twice in one step; g7 the keys held down kept from one event to the next; g8 the keys after Enter in the same step; g17 usage 0x27 of the older RF IDeas routine; g23 lower-casing by the machine's culture; g27 the clock rule of finding 1; g38, g39 the cap one higher; g45 `Reset` forgetting the time. **Each of these behaviours IS right at this head** (the gate's model agrees on every input, all 65,536 pairs of usage and modifier among them, and under the Turkish culture). | Rows for a shifted digit, each sign, a repeated key, a key held over an event boundary, a key after Enter in one step, the digit 0 through the older routine, 256 and 257 gathered; one run of block V under another culture. |
| 5 | Minor (records) | No | **A reader that decodes nothing answers every event with a refusal** (choice e): one tap of a 10-digit card delivered as 22 events gives 22 `Refused: ReaderNotEnabled` (`logs/asm.log`, A12). A caller that shows or logs each refusal shows 22. Vendor 1008 with another product id is refused (choice f); the newer Workpath rule takes any product id of that vendor, but the app owns one such pair only (`hpk.xml` lines 45 to 80), so no owned reader is lost. | The adapter lanes' kits: one message per tap, not per event. |
| 6 | Minor (records) | No | **Gap detection is on by default and assumes a step of exactly 1.** Measured (A8): a counter that grows by 2: 10 whole cards, 0 cards given out, 10 refusals, each after a wait of one window; the same through `hp-text`. A counter that starts again from 1 with no `Reset()`: 400 whole cards, 400 with no answer of any kind, for as long as the numbers stay below the old highest. With `hp-text` one lost event costs the NEXT tap (held one window, then refused). A hole followed by the next card inside the window loses both in one refusal (A6). The step on the newer printers is UNMEASURED (the kit says so). | The adapter kits choose the setting per printer generation and call `Reset()` where the printer restarts its numbers; a question for a printer (FOR-RECORDS.md, list B). |
| 7 | Minor (records) | No | **Two reads that touch inside one window are one card**: a read without its end and the next card 400 ms later give one card of both (A13); at 1000 ms the first is refused and the second is clean. With gap detection off, a lost Enter does the same. This is what any window does; it is bounded by the window (the source keeps a partial read without limit). Not counted as the Blocker: it is the kit's rule Q2 working as written, inside one second. | Say it in the class comment as a named limit. |
| 8 | Minor (records) | No | **The card string leaves by one door the library cannot close:** the public property `CardString`. A serialiser given the result object writes it (measured, `logs/side.log`); so would a logger told to take the object apart. The logging lane's list holds the stem `cardstring` (its branch, `DenyListData.cs` line 15), so the name is covered once the server logs through that library; nothing enforces that today. **Test output:** a failing assertion prints card strings into the log (6 lines with synthetic strings in one mutant's test log); the helpers `Feed.Describe` and `GoldenFile.Expected` build "CARD" plus the string for `Assert.Equal`. **Said plainly: if a later lane feeds real card values through these helpers, or puts rows measured on real cards into the golden file, a red test prints real card strings into a hosted log.** | A rule for the lanes that follow and for spike S3: no real card value in the test project; measured rows come from throw-away test cards only. |
| 9 | Minor | No | **Text.** Two comment sentences say how the app or a printer behaves with no source and no UNMEASURED: `ReaderCatalogue.cs` line 4 ("the six vendor and product id pairs the sign-in app owns"; the source is `hpk.xml` lines 45 to 80) and `CardReadAssembler.cs` lines 198 and 199 ("Call it after a printer reboot or a re-opened reader": that a printer restarts its numbers is RELAYED in the kit, not sourced in the code). Nine test-class comments name the brief's control numbers ("Control C1" to "Control C9"), which mean nothing in the repository. | Two source pointers; drop the nine numbers. Same commit as the fix. |
| 10 | Minor (records) | No | **The root README is stale**: Layout does not list the two projects and Reserved names still holds `src/Datasec.Suite.Cards` (its line 43). No sentence becomes untrue in a way that matters. | The one README pass after the wave. |

Not findings: the bound on the count of reports in one event (the builder's deviation 5): NEEDED and right (below). The
lower-casing: the invariant culture, measured under the Turkish culture. The blank rule with the characters 28 to 31. The first
event numbered 0. The refusal of a byte above 127: safe, with a named cost (below).

## Item 2, the port by a second independent reading

The gate read the named ranges of the seven source files (never `CardValidator.kt`, never a keystore), wrote its model
(`probes/Fuzz/GateModel.cs`, sha256 `8a02cceb...`, frozen at 20:23:10 before any file of the lane was opened, unchanged since:
the same sha256 at the end), then read the builder's code. Both were fed the same inputs through the library's PUBLIC
constructor (reader id and selection), with the bounds opened so that only the routine decides, then again under the default
bounds (`logs/port.log`; `logs/port-tr.log` is the same run under the culture tr-TR: equal in every line).

| Routine | Inputs | Equal in every event | Source decides AGAINST the library | Q4: a lenient platform parser would differ | Q5: the source throws, the library refuses | Q6: a byte above 127, the library refuses | Library exceptions |
|---|---|---|---|---|---|---|---|
| `keyboard` | 259,013 | 254,897 | **0** | 4,116 | 0 | 0 | 0 |
| `hp-text` | 248,816 | 117,394 | **0** | 3,057 | 0 | 128,365 | 0 |
| `legacy-rfideas` | 259,047 | 213,761 | **0** | 0 | 45,286 | 0 | 0 |
| `legacy-hp` | 248,493 | 195,378 | **0** | 0 | 0 | 53,115 | 0 |
| `legacy-elatec` | 259,557 | 147,216 | **0** | 0 | 0 | 112,341 | 0 |
| **all** | **1,274,926** | | **0** | 7,173 | 45,286 | 293,821 | 0 |

- **The inputs** (per routine): random bytes in 1 to 3 events of 0 to 4 reports of 0 to 80 bytes (60,000); every usage with
  every modifier, press, release, Enter, as one event and as four (65,536); a report of every length 0 to 17 (36,000); a
  well-formed read split at EVERY byte into two events, into two reports of one event, and report by report (about 14,000 to
  25,000); card-like text at the limits 0, 32, 33, 256 (40,000); UUID-like shapes (12,000); every byte value alone, after a
  marker and in a key slot (21,024). The 41 vectors and 13 comparison rows: the library gives the kit's result in 41 and 13,
  and so does the gate's model (41 and 13; 6 SAME, 7 DIFFERENT).
- **Under the default bounds** the only further differences are the library's own caps: the 4096-byte event bound (198 and 206
  inputs of typed text over 256 characters in one event) and the 256 cap (3, 1 and 7 inputs; in the 7 the cap's `TooLong` comes
  before `OutsideAscii`: a refusal either way).
- **The three pairs of the Workpath unit test** (parsed by program, kept in `/private/tmp/b1806-gate/pairs/`, never printed):
  the gate's model agrees 3 of 3, the library 3 of 3 (`logs/parity.out`; control: a wrong expectation is seen).
- **Where the source's behaviour is undefined, platform-dependent or throws:**
  - Q5, `PrinterAccessoryService.kt` line 507: a report of exactly 2 bytes makes the source read index 2 and throw; what the
    app does after is UNMEASURED. The library: `Refused: MalformedReport`, the partial read dropped, the rest of that event not
    read (45,286 of 45,286).
  - Q6, line 384 and `ReaderDataStore.kt` line 44: bytes become text by the platform. The library: `Refused: OutsideAscii`
    (293,821 of 293,821 inputs with such a byte).
  - Q4, `ReaderDataStore.kt` lines 25 to 30: finding 3.

**Judged by name**

- **The lower-casing and its culture.** `ToLowerInvariant` (`CardLimits.cs` line 37). The source: `lowercase()` at
  `ReaderOutputProcessor.kt` line 367 and `ReaderDataStore.kt` line 30. Only ASCII reaches it in the library (bytes above 127
  are refused first; the keyboard and RF IDeas tables give ASCII), so the two agree on every string that can leave. Measured
  under tr-TR, where the machine's own lower-casing turns I into a dotless letter (the control line): no difference in
  1,274,926 inputs. No test pins it (finding 4, g23).
- **The blank rule as built.** `CardLimits.IsBlank` counts 9 to 13, 28 to 31 and the Unicode separators. That is the published
  definition of the check the source calls; .NET's own check does not count 28 to 31. It matters for the older Elatec routine,
  whose arithmetic turns the unshifted usages 9 to 13 into 28 to 32 (`PrinterAccessoryService.kt` lines 309 to 312): a read of
  those alone is blank in both. The gate's model has the same set; 0 differences. Not run on a printer: UNMEASURED there, as
  the code comment says.
- **The UUID step.** Finding 3.
- **A byte above 127 (the builder's item 7).** In the newer family the source gets a STRING (`AccessoryReceiver.kt` lines 132
  to 134) and, for vendor 1008, the card IS that string: a card whose text holds a non-ASCII character is a valid Workpath
  card, and the library refuses it. **Safe:** it fails closed, nobody is signed in as someone else. **A sign-in fault waiting,
  for:** a customer whose HP reader (1008:69) delivers text with a character above 127, and, under the older family, any card
  whose bytes or Elatec arithmetic give a value above 127 (unshifted bytes 109 to 127 and shifted bytes 67 and above wrap
  negative, lines 307 to 312). Those people are refused at every OXPd printer while their card works on Workpath. Whether such
  cards exist is UNMEASURED: a question for the Datasec team and for a printer (FOR-RECORDS.md).
- **The first event numbered 0.** The older entry starts its last-seen number at 0 (`PrinterAccessoryService.kt` line 74) and
  drops an event equal to it (line 278), so it drops a first event numbered 0. The library takes it (measured, A8). Right not
  to copy: it would lose the first report of the first read after every start. Whether a printer numbers from 0 or 1 is for a
  printer (report C2 line 98 says the partner's fix assembled "from ordinal 1 after registration", RELAYED).

## Item 3, the required question: what is the assembler handed that is NOT a well-formed read from one honest reader, and what does it do with each?

`logs/asm.log` (13 groups of scripted calls), `logs/soak.log` (16 rows of 20,000 reads); harness `probes/Fuzz/Asm.cs`.

| Handed | What it does | Verdict |
|---|---|---|
| A read with one event missing, the rest arriving before the window ends | holds the rest; one `Refused: MissingSequence` at the window; nothing of it leaves | as the kit says |
| A read with one event missing that goes on past a bound or past the window | the refusal, then the rest of the read as a CARD | **finding 2** |
| A read slower than the window, nothing missing | `Refused: Incomplete`, then the rest as a CARD | **finding 2** |
| A time that goes back, or one time far ahead | time stands still: no refusal by time; a partial read joins the next card; held events are kept without limit of time | **finding 1** |
| A flood of events ahead of a hole | at most 32 held and 4096 bytes; 1,000,000 events of 4096 bytes: 500,000 refusals, live memory after the run no higher than before, 402 ms; 1,000,000 events of 8 bytes: 30,303 refusals (one per 33) | bounded |
| One event of very many empty reports | 4096: taken, 176 bytes allocated in order, 131,280 bytes when it is held (its copy); 4097 and 5,000,000: `Refused: MalformedReport` in 1.3 ms with 264 bytes allocated, a pending read dropped | **the builder's extra bound is NEEDED** (without it one held event of 5,000,000 empty reports is copied, 32 of them held) **and right**; a fault for a legitimate reader only if a printer puts more than 4096 reports into one event, which nothing suggests: UNMEASURED |
| One event over 4096 bytes | `Refused: MalformedReport` before a routine reads it, also when it is ahead of a hole (then the hole is given up too) | as choice c says |
| The largest events with no end | 0.2 to 24.2 microseconds and 153 to 4401 bytes per event of 4096 bytes | no hang, no growth |
| Sequence numbers: negative; repeated; 0 first; the largest; a wrap to the smallest | dropped; dropped; taken; taken, then nothing more until `Reset()`; dropped. No overflow, no exception | as the kit says; the wrap and the restart are named limits (finding 6) |
| A window at its edge | one tick before: nothing; at the window: the refusal (both kinds). The missing event one tick before the end is taken with the held one; at the end it is refused. A window of one tick and the largest window: no exception | exact |
| `Tick` and `Accept` in every order, with repeats, jumps, losses, swaps | 320,000 reads of the soak: 0 exceptions | - |
| `Reset()` in the middle of a read and with an event held | everything forgotten; the next read is clean (the time is NOT forgotten: finding 1) | - |
| A null list, a null report | `ArgumentNullException`, parameter `reports`, before anything changes; the same assembler then reads a card | as the Stamp says |
| A window, cap or bound that is not positive; a selection that does not exist | `ArgumentOutOfRangeException` naming the parameter; no value in the message | as the Stamp says |
| Random bytes of any shape | 1,274,926 inputs through the five routines: 0 exceptions | - |
| A reader not in the table or not enabled | one refusal per event (finding 5) | - |

**The only exceptions that left: the two argument exceptions.** No crash, no hang, no unbounded allocation.

**The builder's choices a to h, each by its effect on a person at a printer**

| | Choice | Effect, measured | Keep? |
|---|---|---|---|
| a | one refusal when a missing event and the read's own window run out together | one refusal, reason `MissingSequence` (A9), also when only the read's window is over and the held event is 100 ms old: the person sees one message, and loses what was held | keep |
| b | after a refusal the base is the highest number held | a late genuine event of the NEXT card is dropped as a late copy and that card is given out without it (A7: a card of 4 characters given out as its last 3). It lasts until `Reset()`: a copy one hour later is still dropped. It needs an event that overtakes its neighbour across the refusal | **part of finding 2**: the fix there (no card until a boundary) covers it |
| c | an event over a bound is refused, uses its number, drops the read and what is held | a pending read is lost with it; the next card is clean (A13) | keep |
| d | past the cap the read is refused at that byte, the rest of the event unread | the rest of an over-long read in later events is then given out (A2) | part of finding 2 |
| e | every event of a reader that decodes nothing is answered | finding 5 | keep, with a caller's rule |
| f | vendor 1008 with another product id is refused | no owned reader is lost (finding 5) | keep |
| g | blank as the Kotlin check | exact to the published definition (above) | keep |
| h | `long`, `DateTimeOffset`, a list of byte arrays; a held event is the assembler's copy | `DateTimeOffset` invites the wall clock: finding 1 | re-think the time type with the fix |

## Item 4, no card string by a side door

`logs/side.log` (reflection and a scan of the built assembly's own tables; control: the same scan over the gate's probe finds a
console, a stopwatch, files and randomness, 53 watched types). The library: 3 referenced assemblies, all of the base library;
49 outside types, none for I/O, network, console, tracing, threads, timers, randomness, reflection or logging; the one member
of time used is `DateTimeOffset.UtcTicks` of a value the caller passes; 11 text literals in all ("Card", "Refused: ",
seven parameter names, a dash, an empty text); 0 native imports; 1 static field, read-only, a read-only collection
(a write through a cast is refused); 0 record-like types; 0 debugger-display attributes; 1 `ToString` of its own
(`CardRead`), which prints `Card` or `Refused: <reason>`. A card result with a planted string, printed eight ways (its own
text, interpolation, format, the list, the assembler): the string in none. Exceptions: the parameter name only, 0 data
entries, no inner exception, no planted byte. The source scan: 31 watched words, 0 found in the 16 files (control: 31 of 31
fire). **The one door: the public property, to a serialiser, and the test helpers (finding 8).**

## Item 5, the two families and the table

The six id pairs of the built table equal `hpk.xml` lines 45 to 80, in order, by program (`logs/nocopy.out`):
3111:15354, 1008:69, 2520:1040, 2520:784, 1899:21544, 7590:272. `DesignDefault`, read from the built assembly: the older
routine for the first four, nothing for the last two, and the keyboard routine for them with the option on: the sentence of
the design (`02_architecture.md` line 368, re-read at source).

**For the product owner's team, in two lines:** if a customer's cards were enrolled through the app's other family than the
one the server is set to, the server computes a different string from the same card for every card where the two routines
differ, finds no match and refuses the sign-in: the card works on Workpath and is "not known" on every OXPd printer. In the
13 comparison rows 7 differ; for the HP reader every card differs when its data ends with byte 13 (the older routine drops it,
the newer keeps it in the string), and dashes of a UUID are removed in the newer family only.

## Item 6, cells and mutants

| Item | Reading | How |
|---|---|---|
| Suite | locked restore rc 0, no lock file changed (porcelain 0 lines); build `0 Warning(s)`, `0 Error(s)`; test `total: 132`, `failed: 0`, `succeeded: 132`, `skipped: 0` | the project's SDK 10.0.404, the gate's own home and package cache, every job under the wave's lock (119 lock folders moved into the gate's scratch; the lock is released), load1 read before each (238 reads, highest 4.71) |
| The builder's seven mutants | 7 of 7 killed, with 3, 1, 4, 3, 11, 23 and 2 red tests: the STATUS's numbers | `scratch/mutants.py` on a copy of the clone |
| The gate's 45 mutants | 33 killed, 12 survive (finding 4). After the undo the copy equals the clone (0 files differ) | the same |
| Tests | 52 methods (1, 1, 6, 17, 3, 12, 2, 4, 6), 14 inline rows, 3 member-data sources; no sleep, delay, clock, stopwatch, skip or unseeded randomness (14 watched words, 0 found, control 14 of 14); 2 seeded random uses | `scratch/text.py` |
| Constants | the expected values come from the golden file (written from blocks V and X: 41 of 41 and 13 of 13 rows equal the kit's blocks by program) and the received values from the library; no value is written into both sides | `scratch/scope.py`, reading of the nine test files |
| The golden file's honesty test | `status` reads PROVISIONAL, 0 rows carry `measured_on`; the rule function is tested on four made-up files, two of which must fail | reading; not mutated by the gate |

The builder's deviation 1 (the load gate read from a sampler): for the records. The gate's view: every job had two reads at
least 120 s apart, both far under the limit (the sampler's highest is 5.93, re-read in its file: 62 lines); the product is not
touched by it; the next kits should say "a read at least 120 s old and a fresh one", which is what was done.

## Measured rows

| Item | Reading | How |
|---|---|---|
| Refs | `main` 7bf37526; the branch 6499bd19; compare ahead 1, behind 0, 33 files (32 added, 1 modified); 4 check runs success; pull requests of any state 1 (number 1, merged), open 0; 6 branches on the origin | `gh api -X GET`, 20:19:03 and 20:42:39 |
| Merge | the head's one parent IS main, so the merge is the head's tree | `rev-list --parents`, `merge-base`. `merge-tree` NOT RUN (a hook of this workspace refuses that verb) |
| 1 Scope | 33 rows: A 32 (18 and 14), M 1, other 0; outside the property 0 (control: 6 of 6 planted rows flagged); binary 0; +3771 -0; 26 files on main, 58 at the head; the one changed file of main is the solution file; modes all 100644; extensions `.cs .csproj .json`; no path under `build/`, `.github/`, no shared root file; the library's lock names 0 packages; the test lock's 21 rows are main's 21 | `scratch/scope.py` |
| 1 Frozen | T1 2/162, T2 5/137, T3 15/448, V 41/10360, X 13/1269, each sha256 equal to the kit's FACT 8; T2 and T3 equal the two project files byte for byte; the solution file is main's with T1's two lines at the two places the kit names, 11 lines, sha256 cfc8ae50... (control: one more space is seen) | `scratch/extract.py` |
| 1 No copy | 0 added files equal a source file; of 965 distinct source lines of 30 or more non-space characters, 0 in an added file (white space removed; also with letter case ignored); 58 comment texts of the source, 0 found; identifiers, author and copyright words of the source, 0; controls fire | `scratch/nocopy.py` (it reads the seven files whole, by program, for this comparison only) |
| 1 The three pairs | 224 stored objects of 8 refs (155 blobs, 10 commits): 0 hold a value of the three pairs in any of 16 forms; 0 of 41 golden rows hold one in their keys, bytes or card value (control: a planted text is found) | `scratch/pairs.py` |
| Repository controls | `RULES: clean (58 files)` with the hash half run (1657 files); `Ran 53 tests`, `OK`; the scanner over `src`, `tests` and the history: `no leaks found` | in the clone |
| 7 Hosted run | run 44708556257: head = the reviewed head, push, attempt 1, success. linux and windows: `0 Warning(s)` 1, `0 Error(s)` 1, `Test run summary: Passed!` 1, `total: 132` 2, `succeeded: 132` 1, `failed: 0` 1, `skipped: 0` 1, `GUARD: clean (10 files)` and `(11 files)` 1 each. rules: `Ran 53 tests` 1, `UNIT-TEST FLOOR: ran 53, floor 53` 1, `RULES: clean (58 files)` 1, the hash-half note 1, `OK` 2. secret-scan: both planted-control lines 1 each, the NEUTRAL-SCAN line (189: 126 blob, 9 commit, 54 tree; 378 copies; 0 not among them) 1, `no leaks found` 3. Every count equals the STATUS. Control line: 0 in each log | `scratch/hosted.py`: GET with `--allow-escape-sequences`, return code asserted, the runner's echo of each step left out (85, 76, 42 and 130 lines) |
| 9 Text | 3,771 added lines and the commit message: names 0, B-numbers 0, clarification ids 0, ticket keys 0, seat ids 0, "product owner" 0, "coordinator" 0, words of deciding 0, card ids 0 (control line: each fires); bytes outside printable ASCII 0; hosts 0; one GUID-shaped value, synthetic (zeros, A, 2, b, 4); the subject is the kit's, 90 bytes. The words `token`, `secret`, `password`: 0. Finding 9 for the rest | `scratch/text.py` |
| 10 The texts through the function | the row is in the last section | `scratch/texts.py` |

## Item 8, code scanning

The API facts against `2026-11-20_B1796_verify/CODEQL-FIRST-PR.md`, re-read 20:42:39: **unchanged** (the four rules on `main`,
the ruleset with no bypass, the default setup with `csharp` and `python` and the extended suite, 2 analyses on `main` with 0
results, 0 alerts of any state, 7 check runs on `main`, 2 workflows), but for the expected rows: 11 workflow runs, 6 branches,
still 1 pull request (merged) and 0 open.

**What the hosted check is likely to report for this code: 0 alerts.** A reading of the query sources on this machine
(`csharp-queries` 1.11.0, `csharp-all` 7.4.2), not a run: `CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is
the only C# proof`.
- The clear-text queries need a sink (a logger, a trace, a file write): the lane has none.
- Their sources are things NAMED with `password` and the like: 0 such names in 3,771 lines (`token`, `secret`, `password`: 0).
- Insecure randomness (7.8): its source is any call on `System.Random`; the tests have two seeded generators. Its sinks are
  values assigned to something named like a password or an account key: none here (`random`, `report`, `sequence`).
- No remote source, no regular expression, no deserialiser, no process start, no file access in the library.
- Python: no Python file changes; not re-run.

**A trap for the lanes that follow:** a variable or member named with `password` (or the other words of that list) that takes
a value from a `Random` in a test draws an alert at 7.8, which blocks.

## Graded claims of the STATUS

True as measured: the commit, its one parent and 33 paths; the frozen blocks; no package; 132 tests here and on both hosted
legs; 52 attributes; all 41 and 13 rows; the seven mutants with their counts; the hosted lines; the no-copy numbers (965); the
three pairs (3 of 3); the sampler's 62 lines and its highest 5.93; 56 lock folders; the predictions file's sha256;
`reading.md` written after the port (its file time 20:12). True and said by the builder itself: its reading was not
independent of the kit (the gate's was: the model was frozen first). Not shown by the gate: the red-first runs and the port's
nine stages; the two publish folders locally (the hosted GUARD lines show 10 and 11); the Jira read. **Contradicted by the
gate's numbers: the property line "no part of a refused read is ever given out" (finding 2); FOR TUESDAY item 12b's wording
"copies ... are late copies from then on" leaves out that a genuine event is dropped too (A7).**

## FOUND / TESTED / HOW

- FOUND: 1 Blocker (time), 1 Major (the rest of a refused read), 2 Minors on code and tests (the UUID step; twelve untested
  behaviours), 1 on text, 5 for the records.
- TESTED: everything in the tables above, in the gate's own clone, with the project's SDK and the gate's own home, package
  cache and build output.
- NOT TESTED / NOT RUN:
  - Nothing on a printer, a card reader, a simulator or a tenant. **Every golden value stays PROVISIONAL**: the gate's model is
    a third reading of the same source, not a measurement. Three readers agreeing proves the port, not the reader.
  - How many events a printer uses per card, the step of its sequence number, whether it starts at 0 or 1, the speed of a
    reader, what the platform puts into the newer family's string: all UNMEASURED; findings 2 and 6 depend on them.
  - Which UUID parser the printers' firmware runs (finding 3): the public OpenJDK source was read; Android's was not.
  - The Workpath code was read, never run, compiled or pasted into a tool. Of `ReaderOutputProcessor.kt` the gate read lines
    366 to 370 and 634 to 646 by eye and the whole by program for the no-copy check only; `CardValidator.kt` and every
    keystore: never opened.
  - CodeQL for C# (cannot extract on this machine); for Python and the workflow language: not re-run (no such file changed).
  - Windows locally (the hosted leg ran); the container build; the two publishes locally.
  - Calls from several threads (the class says the caller serialises; not attacked).
  - `git merge-tree`; the merge with another lane's branch is described by rule in landing.txt, not run.
  - The kit's `.measured` sidecar and reports A1, A7, B1, B2, C1 were not opened (their lines in the kit are RELAYED); report
    C2 line 98 and the design lines 67, 68 and 368 were re-read at source.
  - The golden file's honesty function was not mutated by the gate.

## The texts through the workflow's function

`scratch/texts.py`, `logs/texts.out`: `neutral_export` cut by program from the head's `ci.yml`, the scanner at 8.30.1 with the
workflow's four options. Title alone; title and body; body alone; the squash message with a number; as written; the squash
body alone; the repository's default squash shape; landing.txt: each rc 0, "no leaks found", stored whole. Control (the squash
message with the workflow's planted value joined in): rc 1. Texts flagged: 0.

Files in this folder: VERDICT.md, FOR-RECORDS.md, pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt, landing.txt
(landing.txt opens with DO NOT LAND THIS HEAD; the texts are true at this head and are written again by the gate of the fix
round).
