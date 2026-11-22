# FOR RECORDS: OXPd 2 README limits lane (lane F3: kit B1945 seat X41, kit B1952 seat X42), gate G2 round 2 of 2, reader B1954

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: the lane's cut (README text plus one pinning cell each, no
product code), round 2's two sentences and the other order pinned inside L01 (kit B1952 Q1 = a and Q3 = a, each in
words at its stamp S4; Q2 rename, Q4 the defaults), and the acceptance of the head's stale `rules` status (ANSWER-1).
Tuesday's round-1 Q3 ratification was withdrawn by name at kit B1952's head. Nothing here says the product owner
decided, ruled or approved anything about this lane (kit B1945's `ruled.py` subject-word counts over
CLARIFICATIONS.md were 0, RELAYED by kit B1952).

## State at this gate

- Verdict GO WITH FINDINGS at `5cdcb806` on main `49f686a8` (round 2 of 2). One Minor (FOUND 1: no cell reaches the
  under-lock disposed check `CloudDeviceTokenHolder.cs:318`, which the new sentence names its order by; the sentence
  is TRUE there, MEASURED by probe P2), five INFO. No change required to land.
- Mechanics held: round 2 = two `M` rows on `6177b525`; the lane = four rows on `394fa997` (2 M, 2 A); no `.cs` under
  `src/`; Data README and Data cell byte for byte round 1's; the message byte for byte the kit's; L01 green; five
  mutants each red on exactly its cells; solution 1761 / 0; head push run green on every count (stale `rules` status
  field only); merge with main `49f686a8` clean, tree `fa799353`, 1785 / 0 / 1781 / 4, RULES 553 (macOS).

## Owed items, at this gate

1. **Gate B1939 FOUND 1** (the Data README's `SavedChanges` line not true of a handler that catches): CLOSES when
   this lands (round 1's sentence, unchanged; gate B1949 measured it TRUE).
2. **Gate B1943 FOUND 1** (one token object answered to two calls for one id across a `Remove`): NAMED TRUTHFULLY at
   `5cdcb806`. The Limits sentence states both orders: held first, the id serves cleared bytes; disposed first, the
   later answer is `TokenAnswerRefused`, nothing is held, the issuer is asked again; L01 asserts all four forms (each
   order, in time and after the bound), red under `mRemovedKeepsAnswer`, `mLateKeepsAll`, `mRemovedClearsOnly`,
   `mLateClearsOnly`, `mHoldDisposedAnswer`. CLOSES when this lands. A refusal of one token object across a `Remove`
   stays not built (kit B1940's D3).
3. **Gate B1949 FOUND 1** (Limits sentence false in the old-call-first order): CLOSED at `5cdcb806` (VERDICT.md, the
   clause table; L01 old-call-first forms; probes P1, P2).
4. **Gate B1949 FOUND 2** (D2's "makes a new registration" and "compares its answer with the old one"): CLOSED at
   `5cdcb806` (`git grep -c -F 'makes a new registration' 5cdcb806 -- src` finds nothing; control on `6177b525` finds
   1).
5. **New for the backlog (B1954 FOUND 1, not owed by this lane):** a cell that reaches the under-lock disposed check
   `:318` (left unguarded since pull request 28; scratch mutant `gLockCheckOnly` leaves the suite green). Probe P2
   reached it only by holding the private entry lock by reflection.

## Carried, not in this lane

Gate B1949 INFO 1 (the Data sentence is wider: every later save on that context refuses until its tracker is cleared,
and a tracked read shows the unwritten value), INFO 2 (H3 measured once by a probe, not asserted), INFO 3 (L01
discriminates the current-entry reading), INFO 4 (no mutant of the synchronous pre-check, `SuiteDbContext.cs:95`);
gate B1954 INFO 1 to 5 (VERDICT.md: the snapshot reading of "as it was when the call was made", two locks under one
name, the late refusal masked under `mHoldDisposedAnswer`, "valid" undefined, the stale `rules` status); gate B1943
Info 2 to 4; gate B1939 Info items; kit B1945 NOT DECIDED items 1 and 2 (a latch for a caught refusal; a refusal
across holder states).

## Scans of this folder

- 05:3x `words.py` over `pr-title.txt` (182 bytes), `squash-subject.txt` (191 bytes; 188 with `#30`, under 256),
  `squash-body.txt` (1516 bytes): every class 0. `pr-body.md` (2611 bytes): `product owner` 1 and `coordinator` 2
  (the required who-decides lines) and 4 non-ASCII bytes (the required robot line), every other class 0.
- `build/squash_scan.py` from main `49f686a8`'s `build/` (worktree `g1954/both`) with `#30` in place of `#PRNUM` and
  `squash-body.txt`, `--scanner /opt/homebrew/bin/gitleaks`: control `rc 1, found 2`; message `rc 0, found 0`;
  `SQUASH-SCAN: clean`.
- 05:31 gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1` over this folder (seven
  files, before this line was appended), after the firing control of VERDICT.md SCANS: rc 0, `no leaks found`.
