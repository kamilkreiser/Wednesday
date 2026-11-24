# FOR RECORDS: lane L4 rounds 1 and 2 (kits B2057 and B2060, seats X67 and X68), the release guard's certificate forms, head 0ca131eb (gate B2063: GO WITH FINDINGS, round 2 of 2; round 1 gate B2059: NO GO)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2060 THE AUTHORITY; stamp S4 of each kit states Q1 to Q3 in words as Tuesday's; the launch of the
lane sweep is the product owner's "Scope stands, go", which rules on no content of this lane). Tuesday's round-1 stamp
answer Q5 "the bounds as built" (which froze "a bare or line-wrapped base64 file") was withdrawn by name in kit B2060;
the sentence is gone from the head (`grep -c -i -F 'bare or line-wrapped'` 0 at the head, 1 at c16306ca).

## What the two rounds give, together (CHECKED by the gate at 0ca131eb and on the squash tree 1b633300)
- A PEM block labelled `PKCS7`, `CMS` or `PKCS #7 SIGNED DATA` holding a listed certificate is G2; such a block that
  does not decode is G3 (round 1, unchanged in round 2). CHECKED: probe rows B4, B5, B7, B9 G2; B8 G3; B6 quiet.
- While the deny-list holds a fingerprint, a listed certificate in base64 text without PEM markers is G2: one line (a
  JSON `x5c` value, a `data:` URI, glued at its end), or wrapped with lines joined by CR LF, LF, or the characters
  backslash n or backslash r backslash n, with any spaces or tabs on either side of each line end, every line but the
  last at least 16 base64 characters and the last at least 1; in a file, a ZIP member or UTF-16 text (either byte order).
  CHECKED: every DER size from 256 to 2048 bytes in sixteen wrapped shapes reads 0 clean at the head (round 1: 19.0% to
  100% clean per shape); 388 sizes from 2049 to 16383 bytes (step 37) in two shapes, 0 clean; rows A0 to A5, A12 to
  A15, A19, C1 to C3, E1 to E4, E9 to E11, E13 to E22 SEEN. **This closes gate B2059 FOUND 1 and 2.**
- Today's two publish folders read the same guard lines as before (14 and 15 files), on the branch's tree (the seat,
  hosted) and on the squash tree with main f5882ed7 (the gate, local), with the shipped empty list and with a test
  fingerprint listed; the .NET shared framework folders (188 and 144 files) the same.
- `FLOOR` is 117 and the `rules` job prints `Ran 117 tests` / `UNIT-TEST FLOOR: ran 117, floor 117` from the landing on:
  every later OXPd kit's `hosted3.py` call takes `--unit 117 --floor 117`.

## Owed items, proposed for the records pass (the records seat reads and decides; none is ticked by the gate)
- **Owed 23:** PKCS#7 in PEM: closed by this lane at its landing. Base64 without PEM markers: closed by rounds 1 and 2
  together for the shapes the docstring names (CHECKED above); its named limits stay open as limits: the URL-safe
  alphabet, a JSON-escaped slash, any other line end (a lone CR, an XML character reference such as `&#xA;` between
  lines), an empty line or a line shorter than 16 before the last line, a split across two strings, base64 of base64, a
  run under 128 characters, the empty list; a certificate under 256 bytes or over 65 539 bytes (the landed `30 82`
  frame). **Not named and not seen (gate B2063 FOUND 1, Minor): a JSON-escaped tab after a JSON-escaped line end
  (`\n\t`, `\r\n\t\t`), 1793 of 1793 sizes clean.** PKCS#12 with an encrypted bag (G3 in release mode) and PEM saved
  as UTF-16: already closed by pull request 16 (`185b9eef`); its compressed single-file host stays UNMEASURED (kit B1861
  H13, RELAYED).
- **Owed 14:** the release mode (0 fingerprints is exit 2): already closed by pull request 16; "no job is made to call
  the guard on the folder it packages" stays OPEN (OXPD2-24, NOT DECIDED 1).
- **Owed 11:** the guard reads ZIP-format files only, but every other archive format it knows by magic is a G3 finding
  since pull request 16 (row A17: gzip G3 at BASE, round 1 and the head); whether that closes the item is the records
  pass's call.
- Owed 50's note (pull request 16 left owed 19 to 23 unticked) is why these three were still `[ ]`.

## Still open after this lane (none built; the coordinator's choices)
- OXPD2-24 NOT DECIDED 1 (must a packaging job call the guard in release mode; what counts as packaging) and NOT
  DECIDED 2 (do `.pdb` files and the Windows `web.config` belong in a package): still open in the ticket (no Jira call).
- The real development-CA fingerprint (owed 2): the list is empty, so the base64 rule is dormant on every hosted leg
  today.
- The root `README.md` G2 form list (kit B2057 Q4: incomplete, not false); opening tar or gzip members (they stay G3).
- Gate B2059 Info 4 to 8 (not built, as recorded there); gate B2063 FOUND 1 to 6 below.

## Added by the gates (MEASURED)
- B2059 (round 1, NO GO): FOUND 1 short last line, FOUND 2 indentation (both Major, both closed by round 2); FOUND 3
  unnamed limits (Minor, closed by round 2's Limits sentence: split strings, `&#xA;`, base64 of base64 now named).
- B2063 (round 2): FOUND 1 Minor, a JSON-escaped tab beside an escaped line end is neither seen nor named; Info: a
  no-break space as indentation, CR CR LF and a backslash-newline continuation read clean (the last two under "any
  other line end"); a first line under 16 characters (an XML tag glued to a short first piece) reads clean, named; cost
  with one fingerprint listed 0.43 to 0.59 s per 32 MB of base64 text (round 1 0.23 to 0.43 s), adversarial blank runs
  linear; no false fire anywhere measured.
- Coupling: after this lane lands, lane L3's round 2 takes `--unit 117 --floor 117` and its own +49 tests / +12 files
  (landing.txt MAIN MOVES (B)).
