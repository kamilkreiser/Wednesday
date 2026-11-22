# FOR RECORDS: OXPd 2 README limits lane (lane F3: kit B1945, seat X41), gate G2 round 1 of 2, reader B1949

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: the lane's cut (README text plus one pinning cell each, no
product code) and every choice inside it (kit B1945 Q1 = a and Q3 = a, each in words at its stamp S4; Q2, Q4, Q5 the
defaults). Nothing here says the product owner decided, ruled or approved anything about this lane (kit B1945's
`ruled.py` subject-word counts over CLARIFICATIONS.md were 0, RELAYED).

## State at this gate

- Verdict NO GO at `6177b525` on main `394fa997` (round 1 of 2). Back as a fix round: the Universal Print
  registration README only (two sentences), text only; the Data README and both cells keep.
- Mechanics all held: four paths (2 M, 2 A), no `.cs` under `src/`, the message byte for byte the kit's; both cells
  green; each mutant red on exactly its cells; solution 1761 / 0; hosted PASS (run 45045255551); merge with lane A2-F's
  head `a56ed63b` clean, 1785 / 0 (macOS).

## Owed items, at this gate

1. **Gate B1939 FOUND 1** (the Data README's `SavedChanges` line not true of a handler that catches): the head's
   sentence is TRUE (MEASURED: the cell; probes P1 interceptor async and sync, P2 removal, P3). It CLOSES when this
   lane lands. Optional wider clause, the coordinator's: every later save on that context refuses (not only the next)
   until its tracker is cleared, and a tracked read through that context shows the unwritten value (P3: `tracked read
   ActorId user-9; no-tracking read user-1`).
2. **Gate B1943 FOUND 1** (one token object answered to two calls for one id across a `Remove`): NOT YET NAMED
   truthfully. The head names it in one order only and states it for all orders (B1949 FOUND 1: old call answered first
   gives `TokenAnswerRefused`, no cleared bytes, MEASURED by probe P8 in time and late); and the late-answer bullet's
   new sentence says "`GetAsync(id)` makes a new registration for the same id", against the README's own "a new
   registration is a new id" (B1949 FOUND 2). Both are text; the fix round's gate re-reads them.
3. **New for the backlog (Info, not owed by this lane):** no mutant guards the synchronous pre-check
   (`SuiteDbContext.cs:95`); the README says that path is read from the code. P1's sync form measured it once.

## Carried, not in this lane

Gate B1943 Info 2 (T14's wait), Info 3, Info 4; gate B1939 Info items; kit B1945 NOT DECIDED items 1 and 2 (a latch
for a caught refusal; a refusal across holder states).

## Scans of this folder

`words.py` over `pr-title.txt`, `squash-subject.txt`, `squash-body.txt` and gitleaks over every text of this folder:
see the lines appended below by the reader after the last edit.

- 04:03 `words.py` over `pr-title.txt` (159 bytes), `squash-subject.txt` (168 bytes; under 256 with any number in place
  of `#PRNUM`), `squash-body.txt` (1106 bytes): every class 0, `WORDS: clean (3 files)`. `pr-body.md` (2413 bytes):
  `product owner` 1 and `coordinator` 2 (the required who-decides lines) and 4 non-ASCII bytes (the required robot
  line), every other class 0.
- 04:03 gitleaks 8.30.1 `dir` over this folder (six files, before this section was appended), after the firing control
  of VERDICT.md SCANS: rc 0, `no leaks found`.
- The squash texts describe the round-2 README in general terms; the fix round's gate re-reads them against that text.
