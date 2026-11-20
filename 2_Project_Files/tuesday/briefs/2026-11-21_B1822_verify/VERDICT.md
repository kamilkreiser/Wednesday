GATE B1822: GO WITH FINDINGS @ 9fe5356 on main c56f3f3

Gate G1 Tier 1, round 2 of 2 (the last), OXPd 2, WP1.3, the card decoder library's fix round (kit B1810, seat X10 and its
successor). Head `9fe53569da3e131c394f387ac4e8a1f78c6c9b82` on `b1786/wp13-card-decoders`, one commit on the round-1 head
`6499bd19bc73f56acc69101935bcbff163291a92`; main `c56f3f3b015fae8d47288aa9d6c636ecd8fe2191`. Read and measured 2026-11-21, 08:53 to
09:30 AEDT (clocks by `date`), model Opus 5.5 (the commission's model line). Every number below was printed by a program; the
programs and their logs are under `/private/tmp/b1822-gate/` (`scratch/`, `logs/`, `probes/Fuzz/`).

**BLUF.** **Both round-1 findings the kit put IN are closed by the gate's own run, and so are findings 4 and 9.** The round-1
review's own harnesses, re-run unchanged at the new head: the four clock reproductions (A4, A5) give a refusal and then the
second read's own card; the four refused-read reproductions (A1, A2, A3, A7) give the refusal and nothing more; the soak row
with the clock set back now gives **0 mixed cards (113 at round 1)** and every fault row with gap detection on gives **0 wrong
cards (538, 497, 8,419, 3,480, 1,164 at round 1)**; the 45 round-1 mutants: every one that still applies is killed (the twelve
round-1 survivors: ten killed by the new cells, two no longer apply and the gate's stand-ins for them are killed). **The five
routines decode exactly as before:** the round-1 port comparison, 1,274,926 inputs through the gate's own model, prints a log
byte-identical to round 1's (0 inputs where the source decides against the library), under en-AU and under tr-TR. **D2b, first
independent measurement:** one wrong time per call, 7 rows of 20,000 reads, 0 wrong cards; with the owed end removed 2,079 to
5,645 partial cards per row. **D3:** 400,000 fuzzed reads, 0 cards spanning a window or more. The branch merges onto the moved
main with no conflict (410 tests, 0 failed, on the merged tree). **Findings: Minors and records only, none a reason not to merge**
(table). **Nothing reads a real reader and the server does not reference the library.**

## Findings

| # | Severity | Blocks the merge? | Finding | Recommendation |
|---|---|---|---|---|
| 1 | Minor (the fix's own mechanism; within a named limit stated truly) | No | **ONE wrong time value carried by TWO consecutive calls ends the discarding early, and the tail of the refused read is given out as a card.** Measured (`logs/r2.log`, Q1): keyboard, "12" at 0 ms, then the press and the release of "3" both stamped one hour back, then "4" and Enter at the true time: `REFUSED Incomplete`, then `CARD 4` (a part of the read "1234"). The same through `legacy-hp` with an event and the Tick after it both at the smallest time: `CARD 4`. Control: the same wrong value on ONE call only gives the refusal and nothing more. Cause: D2b's timeline test reads only the first call after the step (`CardReadAssembler.cs` lines 328 to 336), and that call carries the same wrong value, so the rule takes it for a clock set back. The class comment names "two or more wrong times inside one read can end the discarding early" (line 54): two calls with a wrong value are two wrong times, so the sentence is TRUE; but its reach is wider than "two independent glitches": a caller that stamps a batch with one stale value meets it. Soak (`logs/r2.log`, D2b soak): two or more wrong times allowed per read, 2% of calls: 62 partial cards in 20,000 reads; 5% of calls with 1% lost: 223. Every row with one wrong time per call: 0. | Records: the adapter kits' caller rule (a time taken at each call) already excludes it; say in their kits that one stale value reused on two calls is two wrong times. No change in this lane. |
| 2 | Minor (controls of the new code; finding-4 class) | No | **Three behaviours of the new mechanism have no cell that can fail** (gate mutants that leave all 219 tests green, `logs/mutants2.out`): **n3** the time before the step is kept from the FIRST step of a series (taking it at every step leaves the suite green; the gate's probe shows 6 lines differ: under two or more wrong times it gives 42 and 139 partial cards where the head gives 62 and 223); **n17** `Reset()` clears the owed end (keeping it leaves the suite green; probe: 3 cards differ in 200,000 fuzzed reads), so D4's "as a new one" is proven for the discarding, the time and the base but not for the owed end; **n22** a dropped repeat or late copy that carries bytes keeps the reader deaf (probe: a repeat of an old event every 500 ms for 5 s, then a whole card: the card is swallowed; under n22 it is given). The comment's wording ("no event that carries a report byte") matches the code for n22. Two more survivors are equivalent and say nothing: s32 (the round-1 g32 text; the builder's equivalence argument holds, and the gate's probe shows 0 lines differ) and n1 (the step call already sets the quiet reference). | Records, for the next lane that touches the assembler: cells for n3, n17, n22. Not a reason for a third round. |
| 3 | Minor (records) | No | **D5's named exception is not in the comment.** One wrong time a day ahead ON an event with a byte in the middle of a read gives `REFUSED Incomplete`, `REFUSED Incomplete`, then the next card: two refusals for one physical read (the kit's D5 says so). The class comment says "One read gets one refusal" (line 17): true in the assembler's own terms (the piece that began at the wrong stamp is a second read to it), not true of the tap. A caller that shows each refusal shows two. | Records; the adapter kits' one-message-per-tap rule covers it. |
| 4 | Minor (records) | No | **Chatter.** After a refusal, an event with bytes and no end every 500 or 999 ms keeps the reader deaf without bound and the first whole card after it is swallowed (R12, the named cost, measured for keyboard and `legacy-hp`). Every 1000 or 1001 ms instead: ONE REFUSAL PER CHATTER EVENT (15 in 15 s), then the cards are given. A reader that emits stray bytes once a second is a refusal per second to a caller that shows refusals. | Records; the adapter kits' message rule. |
| 5 | Minor (records) | No | **D3 counts a held event that gives no character.** After a card, event 3 a key release held at 0 ms (event 2 missing), event 2 the press of "5" at 500, Enter at 1000: `REFUSED Incomplete` (the window from 0); control in order: `CARD 5`. The comment says "the earliest time of an event that gave it a byte": true if "byte" is a report byte (the release carries 8). It fails closed. | Records only. |
| 6 | Minor (records) | No | **The STATUS does not say in words that the first seat ran on Fable.** It says the kit named Fable and that the session came back on Opus 5.5 (its line 412), and the successor's line 3 says Opus 5.5. The first seat made no line of the commit (its own STATUS: the baseline and the reading only), so the commit's attribution line, `Co-Authored-By: Claude Opus 5.5`, names the model the commit was made on. | Records. |

Not findings (each measured below): the six changed cells; the internal `ReadEnd`; D6; the scope; the texts; the merge onto main.
The round-1 records items 3, 5, 6, 7 and 10 (UUID step, one refusal per event for a reader that decodes nothing, gap detection's
step of 1, two reads inside one window, the README) are unchanged by this commit and stay in the records.

## Item 1: the round-1 findings, each by the gate's own run beside round 1's

The round-1 harness `probes/Fuzz/` (copied from the kept copy; `Asm.cs`, `Port.cs`, `GateModel.cs` unchanged; `Program.cs`
changed only in its default path and one added mode), built against the head's library (`Datasec.Suite.Cards.dll` sha256
`c11505a2...`, the same bytes as the clone's build). Logs: `logs/asm.log`, `logs/soak.log`, `logs/port.log`, `logs/port-tr.log`.

**Finding 1 (Blocker, the time rule): CLOSED.**

| Row (round 1's `asm.log`) | Round 1 at 6499bd1 | The gate at 9fe5356 |
|---|---|---|
| A4: "12" at 10:00, Tick at 09:00:05, "34E" at 09:10 | `-`, `CARD "1234"` | `REFUSED Incomplete`, `CARD "34"` |
| A4 through `legacy-hp`, 59 minutes after the step | `CARD "abcd"` | `REFUSED Incomplete` |
| A5: Tick at the largest time / one day later | `-` / `-`, then `CARD "1234"` | `REFUSED Incomplete` / `-`, then `CARD "34"` |
| A5 after `Reset()`: "56", Tick one hour later, "78E" | `-`, `-`, `CARD "5678"` | `-`, `REFUSED Incomplete`, `CARD "78"` |
| A5: one Accept a day ahead, then back | `-`, `-`, `CARD "1234"` | `-`, `REFUSED Incomplete`, `CARD "34"` |
| A5: a hole under a frozen time, its event 11 minutes late | `-`, `-`, `-`, `CARD "7", CARD "5", CARD "6"` | `-`, `REFUSED MissingSequence`, `CARD "6"`, `-` |
| Soak: 1% lost, gap detection OFF, the clock set back 10 min once in 200 reads | 3,135 part, **113 MIXED** | 3,159 part, **0 MIXED** (the parts: finding 2's named limit, below) |
| Soak: 1% lost, the clock set back once in 200 reads | 3,480 part, 0 mixed, 10,988 exact | 0 part, 0 mixed, 14,165 exact |

- The gate's own form of P-T (`logs/r2.log`, P-T fuzz): 4 rows of 100,000 reads with holes, repeats, swaps that hold events,
  steps back, jumps ahead, the two ends of time, Ticks and Reset; each card's characters name the events that typed them:
  **0 cards whose stamps span one window or more** (widest 991 ms), 0 cards of two reads, 0 exceptions. Under the gate's
  stand-in for the retracted rule (s27) the same fuzz gives 8,398 such cards and 4,029 cards of two reads (control).
- **THE RETRACTION:** the old rule C9 (ii) is gone from the code (the round-1 clamp line `if (hasTime && ticks < latestTicks)`
  occurs 0 times; "latest seen" occurs once in src or tests at the head, in a test class comment that says "never the latest
  seen"; at the old head once, in `CardReadAssembler.cs`) and from every test name (`latest_seen` in the test names: 0; the cell
  `A_time_earlier_than_one_already_seen_is_the_latest_seen` is gone). Stand-in s27 (the retracted rule put back) is killed by 21
  cells.

**Finding 2 (Major, the rest of a refused read): CLOSED for every read whose events keep arriving less than one window apart,
as the comment now says.**

| Row | Round 1 | The gate |
|---|---|---|
| A1: 20-character card, event 3 lost | `REFUSED MissingSequence` at 36, `CARD "55"` at 41 | `REFUSED MissingSequence` at 36 only |
| A1: 36-character card | refusal, `CARD "-3333-444444444444"` | the refusal only |
| A2: 280 digits, the cap | `REFUSED TooLong`, `CARD "01234567890123456789"` | `REFUSED TooLong` only |
| A3: 10 digits at 150 ms | two refusals, `CARD "89"` | `REFUSED Incomplete` at event 8 only |
| A7: event 7 overtakes, the next card | refusal, `CARD "567"` (3 of 4), the next card | refusal, no result for events 6 to 15, `CARD "8"` |
| choice c: an event over the byte bound ahead of a hole | `MalformedReport`, `-`, `CARD "4"` | `MalformedReport`, `-`, `-` (the card supplies the end: the named cost) |
| Soak 1% lost, one report per event | 538 part | 0 |
| Soak 1% lost + 2% twice + 2% swapped | 497 part | 0 |
| Soak no fault, 30 ms between reports | 8,419 part | 0 (exact 10,386 both: whole cards are not taken away there) |
| Soak 1% lost, 20% of taps 300 to 900 ms after the one before | 1,164 part | 0 |
| Soak 1% lost, gap detection OFF | 3,159 part | 3,159 part: **the named limit** ("where that is not known the caller switches the check off, and then a lost event is not seen", line 48 to 50) |

The two comments are true as measured: `CardReadAssembler.cs` lines 29 to 36 and `CardReadOutcome.cs` lines 11 to 15 now say
what the code does, with the exact limit of a read that stops for a window.

**Findings 4 and 9: CLOSED.** The round-1 mutants (`scratch/mutants.py`, its texts byte-equal to the kept copy, at the head;
`logs/mutants.out`): 52 entries, 46 apply as written and 46 are KILLED (the first seat's 7 and 39 of the review's). The twelve
round-1 survivors: g1, g2, g3, g6, g7, g8, g17, g23, g38, g39 KILLED (each by the new cell the kit named); g27 and g45 DO NOT
APPLY (their lines are gone). The six that do not apply (g27, g45, g32, g33, g36, g37) have the gate's own stand-ins
(`scratch/mutants2.py`): s27 KILLED (21 red), s45 KILLED (1), s33 KILLED (5), s36 KILLED (15), s37 KILLED (7), s32 SURVIVES
and is equivalent (finding 2's table). After every undo the mutant tree equals the clone (0 files differ). Finding 9: "Control
C1" to "Control C9" in the test files: 0 (9 at the old head); `ReaderCatalogue.cs` line 4 carries its pointer (RELAYED); the
sentence of `Reset` now carries UNMEASURED (line 264).

## Item 2: what the fix changed that round 1 never saw

**The mechanism as built (read whole, `CardReadAssembler.cs` 518 lines): equal to the STATUS's section and state table**, with
these readings of the gate's own: `Advance` (lines 302 to 341) makes the step and its one refusal; `StartClean` sets the owed end
at every refusal (line 514); `Deliver` (lines 394 to 425) turns `ReadEnd.RefusedInFlight` into the discarding and moves a read's
start back for a held event (D3); `Discard` (lines 430 to 444) throws away every result and books the end event; the quiet
reference is set by every event with bytes that is not a step call, BEFORE the repeat test (line 197), so a dropped repeat
keeps the reader deaf (finding 2, n22).

**D2b, the first independent measurement: HOLDS for one wrong time per call; the named limit is real.** The gate's own soak
(`probes/Fuzz/R2.cs`, `logs/r2.log`; 20,000 honest reads per row, events 10 or 20 ms apart, reads 2 s apart, a Tick every 250 ms;
seven kinds of wrong time: the largest, the smallest, a day ahead, an hour back, one window ahead, one window and a tick ahead,
one tick back; on a Tick or on an event):

| Row | Head: exact / partial | Owed end removed (n4) | Timeline test inverted (n2) | Owed end forgotten at the quiet window (n5) |
|---|---|---|---|---|
| one wrong time on 0.5% of calls, keyboard | 17,292 / **0** | 17,292 / 2,079 | 17,292 / 799 | 17,292 / 858 |
| one wrong time on 2% of calls, keyboard | 12,789 / **0** | 12,789 / 5,645 | 12,789 / 2,215 | 12,789 / 2,283 |
| the same, 1% of events lost | 8,983 / **0** | 9,132 / 4,559 | 8,915 / 1,774 | 9,132 / 1,844 |
| the same, `legacy-hp` (and `legacy-rfideas`, `legacy-elatec`: equal) | 15,456 / **0** | 15,456 / 2,808 | 15,456 / 1,375 | 15,456 / 195 |
| two or more wrong times allowed per read, 2% of calls | 11,144 / 62 | | | |
| two or more, 5% of calls, 1% lost | 3,613 / 223 | | | |

So the owed end and the two timelines are each needed (the model's claim, now measured on the library), and with them one
wrong time per call leaves 0 partial cards in 140,000 reads. The cost, measured: at 0.5% wrong calls 2,708 whole cards of 20,000
become refusals (the head's 17,292 against 19,999 under the retracted rule): the price the kit names, paid only by a caller that
breaks the rule. The limit: finding 1.

**D3: HOLDS.** T16's calls: `CARD 9`, `REFUSED Incomplete`. After a card, event 3 "12" held at 0 ms (event 2 missing), event 2
"5" at 500, Enter at 999.9999 ms: `CARD 512`; at 1000 ms: `REFUSED Incomplete` (the window from the held event's own stamp, to
the tick). The P-T fuzz above: 0 cards spanning a window. Mutant n20 (D3 removed) killed by 1 cell. One edge: finding 5.

**The routines' decoding: UNCHANGED.** (a) The diff of the five routine files changes only the return type and the three return
values (`bool` true to `Ended` or `RefusedInFlight`, false to `None`) and adds `HasEnd => false` to the whole-buffer routine: no
byte-to-character line moves. (b) The round-1 port comparison through the gate's own model, re-run at the head: **the log is
byte-identical to round 1's** (`diff` prints nothing): 1,274,926 inputs, UNEXPLAINED DIFFERENCES 0 in each routine, **0 inputs
where the source decides against the library**, blocks V and X 41 of 41 and 13 of 13; the same under tr-TR (`port-tr.log`,
also byte-identical to round 1's). (c) Mutants of the three-valued result: n14 (RF IDeas never reports an end) killed by 4, n15
(the keyboard cap reported as no end) by 1, n16 (the `legacy-hp` cap reported as an end) by 1, n13 (the whole-buffer routine
discards) by 1.

**D6: BUILT as the kit allows.** One attribute `[System.Text.Json.Serialization.JsonIgnore]` on `CardString` (`CardRead.cs` line
27) and its comment; no package, no project line. Measured: the framework's serialiser writes `{"Outcome":0,"Reason":null}` for
a card (the string absent; control: the property holds it); the attribute read back by reflection; the library's references:
`System.Collections`, `System.Runtime`, `System.Runtime.InteropServices`, `System.Text.Json`. The comment says another serialiser
and a logger that takes an object apart still read it: true.

**The six changed cells: each justified by D1 to D4; no assertion about a bound, a reason or an exception lost** (the diff of
`HostileInputTests.cs` read line by line): four cells move their next card one quiet window later (`CARD 5` 4 to 1003 ms;
`CARD y` 4 to 1003; `CARD c` 2 to 2000 and `CARD f` 2 to 1001; `CARD g` 3 to 1000), each keeping its `MissingSequence`,
`MalformedReport` or `TooLong` assertion; the flood cell's count 303 becomes 294 (10000/34: the 34th event is read while
discarding and its Enter ends it), every refusal still asserted `MissingSequence`; the retracted cell is replaced (P-T). One
corrected comment ("4096 bytes are read (and end as a card that is too long)" was untrue at the old head too: the cap refuses at
the 257th byte). The suite at the head: 219 tests, 0 failed (132 at the old head).

**The cost to a person at the printer (D10), measured** (`logs/r2.log`):
- **Deaf time:** a read with no end refused by the window, then a whole card: at the last byte plus 999.9999 ms swallowed, at
  plus 1000 ms given, for keyboard, `legacy-hp`, `legacy-elatec` and `legacy-rfideas` alike (the comment's "one window minus one
  tick", exact). When the refused read's end arrives, a card in the same instant is given.
- **Slow taps:** five taps of 10 digits and Enter, one report per event: 40, 47 and 48 ms apart (the Enter at 960 ms) 5 cards of
  5; 50 ms apart (the Enter at 1000 ms) and slower: 0 cards of 5, 5 refusals. A reader slower than about one second per card
  gives no card at all (records item 6, decided by nobody).
- **Stamps out of call order:** 20,000 honest reads: 0.1% of stamps one tick early: 653 refusals; 1%: 5,339; 2%: 9,254; 0 wrong
  cards in each (the cost of D1, named in the comments of `Accept` and `Tick`).
- **R12 chatter:** finding 4. A card tapped in the deaf time is lost with no refusal of its own (Q2: a new read with a hole held
  after a refusal, then a step: one `MissingSequence`, and the card "78E" that follows is swallowed; then `CARD 9`).

**THE REQUIRED QUESTION: what is the assembler handed that is NOT one of the kit's tables T, R and I, and what does it do?**

| Handed | What it does (measured) | Ruling |
|---|---|---|
| Two wrong times in one read (a window ahead then an hour back; two at the largest; two at the smallest; the smallest then the largest; the largest then an hour back on an event) | refusal, then the next card; no part in these five directed forms. Soak with two or more: 62 and 223 partial per 20,000 | **the named limit, stated truly** (line 54) |
| ONE wrong value on TWO consecutive calls | refusal, then `CARD 4`, a part | **finding 1** (inside the limit's words) |
| A step during the discarding with events out of order (n+2 before n+1, a step of an hour back, then n+1, then a card) | one refusal, then `CARD 34` | closed |
| A step with an event held after a refusal whose end never came; the same with nothing owed; the whole-buffer routine with an event held | one `MissingSequence` each time; the card that supplies the owed end is swallowed; the whole-buffer routine gives the next event | closed (an event cannot be held WHILE discarding: the discarding takes events in arrival order) |
| `Reset()` in the middle of a read; while discarding; with an event held | `CARD 4567`; `CARD 89` (the tail); `CARD 9` | **the named limit** (line 56 and the comment of `Reset`) |
| Gap detection off | a lost Enter: two reads in one card (`CARD 1234`); a lost character: `CARD 134`; after a slow refused read: one refusal, then the next card | **the named limit** (lines 48 to 50); P-R is given up for lost events, as said |
| A reader that types slower than one window | every tap refused once, 0 cards | **the named cost** (lines 39 to 41) |
| Stamps out of call order by one tick | a refusal each time, no wrong card | **the named cost** (line 26) |
| One forward jump of the caller's clock that is never taken back, in the middle of a read | the read is refused, the quiet window has passed by the caller's time, and the rest is a new read | **the named limit** ("by the caller's time", line 36; a read that stops for a window, line 52) |
| A dropped repeat with bytes during the discarding | keeps the reader deaf | as the comment words it; untested (finding 2, n22) |

The only exceptions that left in any run: none (the soak, the fuzz and the directed rows: 0 exceptions).

## Item 3: scope and the texts

| Item | Reading | How |
|---|---|---|
| Refs | branch `9fe53569`, main `c56f3f3b`, `compare 6499bd19...9fe53569` ahead 1, behind 0, 25 files (20 modified, 5 added); `compare main...head` ahead 2, behind 1; check runs `secret-scan`, `windows`, `linux`, `rules` each completed success; pull requests naming the branch 0 | `gh api -X GET`, 08:53:50 and 09:11:38 |
| Scope | 25 rows: M 20, A 5, every path under `src/Datasec.Suite.Cards/` or `tests/Datasec.Suite.Cards.Tests/` and ending `.cs`; outside 0 (control: a planted slnx row flagged 1); `git diff --quiet` over the solution file, both props, README, global.json, NuGet.config, `.github`, `build`, `packaging`, both project files, both lock files and the golden folder: rc 0 (control over `CardReadAssembler.cs`: rc 1); binary rows 0; golden sha256 `4cb0c569...482e2c` (equal to round 1's) | `scratch` programs |
| Texts | 1,572 added lines and the commit message: the ban-list names (underscore-aware), B-numbers, ticket keys, clarification ids, control numbers, "product owner", "coordinator", "review", "gate", "finding", "round", words of deciding, the seat and model names: **0 hits** in added lines but 41 hex literals the seat pattern meets (`0x79` and the like, each read: none a seat id) and one comment line holding "latest seen" (the retraction stated, not the rule); in the commit message 3 hits, all in its one attribution line; 16 of 16 controls fire; added lines with a byte outside printable ASCII, a tab or a CR: 0 | gate program |
| Commit | subject `Close the time rule and the rest of a refused read in the card read assembler (WP1.3)`, a blank line, one attribution line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`; author and committer e-mail both equal the project checkout's local `user.email`, names equal its `user.name`, the same identity as the round-1 commit (compared in-process, not printed) | `git log`, `git config --local` |
| Tests | no sleep, delay, clock, stopwatch, skip, `new Random()`, `Random.Shared`, tick count, GUID or wait in the test files (14 watched words, 14 of 14 controls fire); the new generators use their own seeded arithmetic (`Script.cs` `Lcg`), not `System.Random` | gate program |
| Hosted run of the head | run `44823261122`: linux and windows `total: 219` 2 lines each, `failed: 0`, `0 Warning(s)`, `0 Error(s)`, `GUARD: clean (10 files)` / `(11 files)`; rules `Ran 53 tests`, `UNIT-TEST FLOOR: ran 53, floor 53`, `RULES: clean (63 files)`; secret-scan both planted-control lines, `NEUTRAL-SCAN: stored objects 279 (192 blob, 14 commit, 73 tree), copies written 558, objects of this commit not among them 0`, `no leaks found` 3; the runner's echo left out (130, 76, 85, 42 lines); control line 0 in each | GET with `--allow-escape-sequences`, rc asserted |
| Local | locked restore rc 0; build `0 Warning(s)` `0 Error(s)`; test `total: 219`, `failed: 0`, `succeeded: 219`, `skipped: 0`; porcelain 0 lines after | the project's SDK, the gate's own home and cache, the wave lock |

## Item 4: the moved main

**The branch merges onto main `c56f3f3` with NO conflict and needs no new commit.** A three-way merge (`git merge --no-ff
--no-commit`, in a scratch clone in the session's scratchpad, never committed or pushed; a throwaway identity was passed to that
one command because git asks for one even for a merge it does not commit): `Auto-merging Datasec.Suite.slnx`, "Automatic merge
went well". The merged index holds 83 paths, each equal to main's blob or the branch's blob by the three-way rule (0 differ);
`Datasec.Suite.slnx` is the one path changed on both sides. **The merged solution file reads exactly what the ordering rule asks
(ordinal order of the Path values in each Folder block, checked by program: src 4 in order, tests 3 in order): 13 lines, 663
bytes, sha256 `14c81d88aa7e35e92666491bd9619adffd07b3a6fdb03d4bd947a5b58d75db4c`, byte-equal to the file round 1's landing.txt
predicted for "the logging lane first, this lane after".** On the merged tree: locked restore rc 0 (Serilog from the gate's
cache), build `0 Warning(s)` `0 Error(s)`, test `total: 410`, `failed: 0` (219 of this branch and, by arithmetic, 191 of main's
logging tests).

## Item 5: code scanning: NOT RUN

`CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof`. The API facts, re-read 09:11:38: default
setup `configured`, languages `actions`, `csharp`, `python` (round 1 read `csharp`, `python`: `actions` is new), suite
`extended`; 0 open alerts; the last analyses on main (`c56f3f3`) 0 results each; the rules on main `deletion`,
`non_fast_forward`, `code_scanning`, `required_status_checks`. **What the hosted scan is likely to report for these 25 files: 0
alerts**, from a reading of the query families round 1 read, not a run: no sink of the clear-text queries (no logger, file,
console or trace in the library or the new tests); 0 names holding password, secret, token, credential, api key, private key
or auth in src or tests (control fires); **round 1's trap does not arise: the new generators do not use `System.Random` at
all** (their own `Lcg`), so the insecure-randomness query has no source in the new cells, and the two seeded `System.Random`
uses of round 1 (`HostileInputTests.cs` lines 210 and 222) feed nothing named like a credential; one new use of
`System.Text.Json` serialises a card result to a string in a test and writes it nowhere. Python and the workflow language: no
such file changed.

## Item 6: the landing texts

In this folder: `pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `landing.txt`, and `FOR-RECORDS.md`. The
scan row is the last section.

## What was NOT tested

- Nothing on a printer, a reader, a simulator or a tenant: every timing rule and every golden value stays UNMEASURED there.
- CodeQL for C# (cannot extract here); the hosted code scan runs on the pull request only.
- Windows locally (the hosted leg ran); the container build; the two publishes and the release guard (no project or package
  change); calls from several threads (the class says the caller serialises).
- The drafter's Python model was not run by the gate (the gate's measurements are on the library; the model's rows were the
  kit's, and the gate's rows agree with them where both exist: T16, I05's shape, the R18 counts at 0).
- The builder's red-first runs against the old head (the gate's equivalent is round 1's own logs beside the gate's new ones).
- The Workpath source: not opened this round (the port comparison ran from the round-1 model and frozen blocks only); no
  keystore, no `CardValidator.kt`, no pairs file.
- The CodeQL `actions` language on the pull request (no workflow file changes).

## Notes on the gate's own conduct

- **Scratch `/private/tmp/b1822-gate/`, NOT `/private/tmp/b1819-gate/` as the commission names.** That folder holds the trees of
  the earlier review B1819 (another lane; its `clone/`, 150 logs, 08:21 to 08:45 today); a second clone there would overwrite
  another review's evidence. Read as a slip of the number.
- The merge of item 4 ran in the session scratchpad (`.../scratchpad/b1822-merge`) because a workspace hook refuses git write
  verbs outside it; the first checkout of the gate's clone ran inside a Python program before the gate met that hook.
- Every heavy job (restore, build, test: 3 at the head, 6 probe builds, 46 plus 28 plus 3 mutant runs, 3 on the merged tree)
  went through the wave's lock `.tools/wave1-heavy.lock.d` by `mkdir`, with `owner.txt`, released by a move into
  `/private/tmp/b1822-gate/_quarantine/locks/`; load1 read before each and the job held while load1 was 7 or more (highest
  read 4.05, 330 reads). One probe build waited 150 s for the lock (another seat held it).

## The texts through the workflow's function

`scratch/texts.py` (round 1's program, its paths, head and attribution line changed), `logs/texts.out`: `neutral_export` cut by
program from the head's `ci.yml` (lines 120 to 128), the scanner at 8.30.1 with the workflow's four options, each text stored as
the commit message of a scratch repository in the session scratchpad. The title alone; the title and the body; the body alone;
the squash message with a number; as written with `(#PRNUM)`; the squash body alone; the repository's default squash shape
(the title and the two commit messages as a list); landing.txt: **each rc 0, "no leaks found", stored whole. Control (the squash
message with the workflow's planted value joined in): rc 1, "leaks found: 2". Texts flagged: 0.** The name and id scans over
the four texts: 0 hits of every banned class (controls fire 1 each); "nothing reads a real reader" or "does not reference" 2 in
each body; PROVISIONAL 1 in each body; "chosen by the build's coordinator or by the builder" in both bodies (in the squash body
across a line break, which the scan's pattern does not span); non-ASCII bytes outside the footer line 0; `pr-body.md` ends with
the footer line, `squash-body.txt` with the one attribution line `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`,
`squash-subject.txt` with `(#PRNUM)`; landing.txt pins the head 3 times, `--match-head-commit` once; the longest squash-body line
71 bytes.

Files in this folder: VERDICT.md, FOR-RECORDS.md, pr-title.txt, pr-body.md, squash-subject.txt, squash-body.txt, landing.txt.
