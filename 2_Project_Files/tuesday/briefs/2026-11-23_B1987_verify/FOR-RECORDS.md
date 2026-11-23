# FOR RECORDS: OXPd 1.x read-only SOAP client (lane X1), gate G1 round 2 of 2 of lane X1, reader B1987

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the coordinator (Tuesday), as coordinator: this lane and every choice inside it (kit B1976 at round 1; kit
B1984 at round 2, its Q1 = a in words at stamp S4, Q2 to Q6 the defaults), the landing order and this gate's commission.
Nothing here says the product owner decided, ruled or approved anything about this lane.

## The two rounds

- **Round 1** (kit B1976, seat X49, head `1fca08cf` on `da8d64a8`; gate B1980): NO GO 1 of 2. FOUND 1 Major, a nested
  answer of about 35 kB ended the host process (stack overflow in the masking copy; MEASURED at 5,000 levels on a SOAP
  read and on the tree GET, 60,000 in a fault code); FOUND 2 Minor, the returned answer could hold the admin password
  (CDATA split, element or attribute name); FOUND 3 Major for function, WS-Addressing August 2004 sent while every
  addressing element of HP's committed descriptions is WS-Addressing 1.0; FOUND 4 Minor, an infinite time-out accepted.
- **Round 2** (kit B1984, seat X50, head `8f5813bf`: one merge of main `cad65b86`, merge commit `ba15e0f9`, tree
  `d579d9d9` = `git merge-tree`'s, then one fix commit = the three frozen patches byte for byte, tree `0dc0d950`; gate
  B1987): the four round-1 findings are FIXED and re-measured by this gate's own probe (deep shapes up to 140,000 levels:
  `MalformedAnswer`, process alive; A1 to A13: the password nowhere; WS-Addressing 1.0 in every header, 0 August 2004
  strings in `src/`; `InfiniteTimeSpan`, zero, -5 s and 30 days refused by the options). Verdict: see VERDICT.md.

## From this gate (each a Minor that can ship with a ticket; none a Blocker)

1. **Minor (P3): a password with an XML-escaped character, echoed inside a namespace URI, is returned.** MEASURED
   (probe N1 to N5, passwords holding `&`, `<`, `"`, a tab, a line feed): `Answered`, and the returned `Answer`'s
   namespace names (and the namespace declaration's value) hold the password; `ToString()` in every `SaveOptions` does
   not (it escapes), and `WriteTo` with `NewLineHandling.None` shows the tab and line-feed forms. The record is clean in
   every row. The same shapes with a password of plain characters end `MalformedAnswer` (Holds sees them), and the text
   and attribute-value controls are scrubbed. Cause: `Mask` copies namespace declarations unscrubbed and `Holds`
   compares serialised text only. Fix direction (the coordinator's): `Holds` also reads every element's and attribute's
   namespace name and every declaration's value as they are; a K12 row with a password holding `&`.
2. **Minor (P4, README "A call is bounded in time"): post-body work is not under the time-out.** MEASURED: 90,000
   attributes on one element (889 kB, under the 1 MiB bound): `Answered` after 7,432 ms with `Timeout` 1 s (probe K7);
   28,000 namespace declarations on one element, 5.6 s (K1) and 5.1 s in the tree (K1t). Size-bounded and finite (no
   crash, no leak); only a pinned device can send it. Fix direction: cap attributes per element, or check the time-out
   token in the masking copy, or narrow the README sentence to the network part (kit B1984's own frame table already
   says so, in the kit only).
3. **Minor (documentation): `src/Datasec.Suite.Adapters.Oxpd1/README.md:72` to `:73` "Not built by the solution yet"
   is false at the head** (the seat's STATUS named it; re-printed here). One bullet to remove.
4. **Info: CodeQL on the lane** is first read on the pull request (a branch push runs no Analyze job: the branch head's
   check runs are the four CI jobs only, MEASURED); this gate's local CodeQL could not run (the toolchain's C# extractor
   is x86_64 only; this machine is arm64: "Bad CPU type in executable"), so the pull request's csharp analysis is the
   first and only CodeQL read of this lane (landing.txt step 3).
5. **Info: the slnx edits of lanes X1 and H do not conflict** (`git merge-tree --write-tree 8f5813bf 0c65be47` rc 0,
   tree `7ad207ef`, three separate hunks: X1's two lines, H's `Jobs.Transport` and `Server.Tests` lines).

## Carried (RELAYED)

- Not built (gate B1980 INFO): `MaxAnswerBytes` of 0 or less is accepted (re-MEASURED: every answer `TooLarge`); a
  setting of spaces is sent (re-MEASURED: 403); TLS session resumption, two concurrent calls, HTTP/2-only servers: no
  cell.
- The endpoint path prefix is in no committed file: it rests on HP's Authorization specification's pattern and is
  UNMEASURED for the other three services until a first connection; the stub's route matches case-insensitively, so K01
  checks the prefix by ordinal comparison.
- **UNMEASURED until a device:** what a FutureSmart 5 device does with WS-Addressing 1.0 headers marked
  `mustUnderstand` (a SOAP 1.2 node that does not understand them faults every read: closed, no write, no leak); the
  path prefix for DeviceInfo, Authentication and Accessories; any device answer.
- From kit B1976: the HP files by the coordinator's reading with leave to correct; R32 open; one shared pin helper owed
  later; a lab command that calls this client owed (wave 2).

## SCANS (of this folder's texts)

- `words.py` (gate copy, `CONTROL FIRED: 13 of 13`) over `pr-title.txt` (184 bytes, under 256), `squash-subject.txt`
  (193 bytes) and `squash-body.txt` (1802 bytes, 32 lines): every count 0, `WORDS: clean (3 files)`.
- `build/squash_scan.py <subject with #36> squash-body.txt --scanner /opt/homebrew/bin/gitleaks` (from the gate's `red`
  worktree's `build/`, equal to main's: no `build/**` path in this diff): control `rc 1, found 2`, message `rc 0, found
  0`, `SQUASH-SCAN: clean`.
- gitleaks `dir` over this folder (seven files, before this SCANS section was filled): rc 0, `no leaks found`.
- Lines outside printable ASCII in this folder: 0 in every file but `pr-body.md` line 65 (the attribution line).
