# FOR RECORDS: OXPd 1.x read-only SOAP client (lane X1), gate G1 round 3 of lane X1 (CodeQL at landing), reader B1990

Not repository text. For the next OXPd records pass; nothing here was written into the project. No person is named.
Who decided: the round's opening is the product owner's ruling of card `datasec-oxpd-x1-codeql-round3-1123` ("Fix round
now", 14:41:39 on the live board); every direction inside the round (one fast-forward commit, no merge of main, the
record without the setting's name, the scrub text as a read-only field, the namespace walk, the README narrowing, the
instrument `pr37.py`) and this gate's commission are the coordinator's (Tuesday), as coordinator.

## The three rounds

- **Round 1** (kit B1976, seat X49, head `1fca08cf`; gate B1980): NO GO 1 of 2 (deep nesting crashed the host; the
  password in a CDATA split or a name; WS-Addressing August 2004; an infinite time-out accepted).
- **Round 2** (kit B1984, seat X50, head `8f5813bf`: merge `ba15e0f9` of main `cad65b86`, then one fix commit; gate
  B1987): GO WITH FINDINGS, three Minors (a password with an XML-escaped character echoed in a namespace returned; the
  work after the body not under the time-out; a false README bullet). Pull request 37 opened at `8f5813bf`; its CodeQL
  read 3 open `cs/cleartext-storage-of-sensitive-information` alerts at `Oxpd1Client.cs:238` (the setting's name, and
  the scrub text as the output of `DenyList.ReplacementFor("password")`, flowing into the record).
- **Round 3** (kit B1988, seat X52, head `85e414d6`: ONE fast-forward commit on `8f5813bf`, the two frozen patches byte
  for byte, tree `8cf35b46`; gate B1990): the record names no setting; the scrub text is `Oxpd1Soap.Placeholder`, a
  `static readonly` field equal to the deny-list's password text; `Holds` reads namespace names and attribute values
  unescaped; the README says what the time-out bounds; the false bullet removed. Pull request 37 at `85e414d6`: 8
  checks success, csharp analysis results 0, alerts 1 to 3 `fixed` (none dismissed). Verdict: see VERDICT.md.

## From this gate

See VERDICT.md FOUND. In short: no Blocker; gate B1987's FOUND 1 and FOUND 3 are fixed and re-measured with that gate's
own probe; FOUND 2 is narrowed in the README and stays a named follow-up.

## Carried (RELAYED)

- Named follow-up (not built): the parse and mask after the body are bounded by size and depth, not by `Timeout`; a cap
  on attributes per element, or the time-out token inside the copy, is owed if a device can send such an answer (gate
  B1987 FOUND 2).
- `MaxAnswerBytes` of 0 or less is accepted; a setting of spaces is sent; TLS session resumption, two concurrent calls,
  HTTP/2-only servers: no cell; the endpoint prefix and WS-Addressing 1.0 behaviour of a FutureSmart 5 device
  UNMEASURED until a first connection; the HP files by the coordinator's reading with leave to correct; R32 open.
- CodeQL could not run on this arm64 machine (x86_64 extractor); pull request 37's own analysis is the instrument, and
  it reads 0 at `85e414d6`.

## SCANS (of this folder's texts)

- `words.py` (gate copy, `CONTROL FIRED: 13 of 13`) over `pr-title.txt` (184 bytes), `squash-subject.txt` (212 bytes)
  and `squash-body.txt` (2294 bytes, 39 lines): every count 0, `WORDS: clean (3 files)`.
- `build/squash_scan.py <subject with #37> squash-body.txt --scanner /opt/homebrew/bin/gitleaks` (from the gate's `red`
  worktree, tree = the head's; `git diff --stat df762b28 85e414d6 -- build .github` 0 lines, so its `build/` and
  workflow equal main's): control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks `dir` over this folder (seven files, before this section was filled): rc 0, `no leaks found`.
- Lines outside printable ASCII: 0 in every file but `pr-body.md` line 75 (the attribution line).
