# FOR RECORDS: lane L4 (kit B2057, seat X67), the release guard's certificate forms (PKCS#7/CMS PEM labels, base64 without PEM markers), head c16306ca (gate B2059: NO GO, round 1 of 2)

For the records lane only, AFTER a landing of a gated head; nothing here is written into a project file by the gate.
**This head is NOT to land (VERDICT.md FOUND 1 and 2); the rows below are for the round-2 head, re-checked by its gate.**
Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the product owner (kit THE
AUTHORITY: CLARIFICATIONS.md counts 0 on every subject of the lane over 1114 lines, MEASURED by the drafter and re-run by
the seat, RELAYED; Stamp S4 states Q1 "a", Q2 "a" and Q3 in words as Tuesday's decisions, Q4 to Q9 the defaults).

## The kit's FOR RECORDS (RELAYED from kit B2057, each checked by the gate against this head)
- The release guard judges a certificate inside a PEM block labelled `PKCS7`, `CMS` or `PKCS #7 SIGNED DATA` (G2; an
  undecodable such block is G3). CHECKED: `release_guard.py:75`-`:76`; the cells green; probe rows B4, B5 (G2), B8 (G3
  with the empty list), B6 (quiet with the empty list).
- While the deny-list holds a fingerprint, a certificate in base64 text without PEM markers is G2. CHECKED WITH A
  CORRECTION: true for one-line runs (`x5c`, bare, glued, `data:` URI, ZIP member, UTF-16 either order) and for wrapped
  runs whose last line holds 16 base64 characters or more; **NOT true at this head for a wrapped run whose last line holds
  1 to 15 (22.7% of DER sizes 256 to 2048 bytes at 64 columns; 19.0% at 76 columns CR LF) nor for indented or
  blank-padded wrapped lines (every size)** (VERDICT.md FOUND 1 and 2). Do not record this sentence unqualified until a
  gated head closes or names both.
- Today's two publish folders read the same guard lines as before (14 and 15 files). CHECKED: hosted and local, with the
  shipped list and with a test fingerprint listed.
- Owed items, proposed for the records pass (the records seat reads and decides; none is ticked by the gate):
  - **Owed 23:** PKCS#7 in PEM closed by this lane when a gated head lands. Base64 without markers: closed only when the
    round-2 head closes or names FOUND 1 and 2. PKCS#12 with an encrypted bag (G3 in release mode) and PEM saved as
    UTF-16 (judged): **already closed by pull request 16** (`185b9eef`); its name rule and backslash split: already closed
    by pull request 16; its compressed single-file host stays UNMEASURED (kit B1861 H13, RELAYED).
  - **Owed 14:** the release mode (0 fingerprints is exit 2): **already closed by pull request 16**; "no job is made to
    call the guard on the folder it packages" stays OPEN (kit B1861 NOT DECIDED 1; the ticket's NOT DECIDED 1).
  - **Owed 11:** the guard still reads ZIP-format files only, but since pull request 16 every other archive format it
    knows by magic is a G3 finding (probe row A17: gzip G3 at BASE and at the head), so "would not be seen" no longer
    holds; whether that closes the item is the records pass's call.
  - Owed 50's note (pull request 16 left owed 19 to 23 unticked) is the reason these three were still `[ ]`: the records
    pass reads pull request 16's landing with them.
- `FLOOR` is 115 and the `rules` job prints `Ran 115 tests` from the landing on: every later OXPd kit's `hosted3.py` call
  takes `--unit 115 --floor 115` (more if round 2 adds cases: then the round-2 head's own count).
- Named limits (docstring, MEASURED as stated by the gate): base64 in the URL-safe alphabet, with a JSON-escaped slash,
  with another line end (CR only), under 128 characters, or with an empty list; a certificate under 256 bytes.
- Not built (the coordinator's choice): the packaging-job rule and the `.pdb` / `web.config` decision (OXPD2-24, NOT
  DECIDED 1 and 2, still open in the ticket, which stays in Backlog: no Jira call); the root `README.md:67` sentence
  (Q4: its G2 form list is incomplete, not false); opening tar or gzip members (Q2).

## Added by the seat (MEASURED, H12) and graded by the gate
- Wrapped base64 with indented lines (a YAML block scalar, indented XML) is not seen, and the docstring does not name it.
  Gate: Major (FOUND 2), with tab indent and a blank before each line end measured the same.

## Added by the gate (MEASURED, for the round-2 kit and then the records)
- FOUND 1 (Major): a short last wrapped line hides the certificate (above).
- FOUND 3 (Minor): unnamed clean shapes: a certificate split across two JSON strings, an XML `&#xA;` between lines,
  base64 of base64.
- Info: a certificate inside CMS EnvelopedData's encrypted content is unreadable by any guard (by construction); one in
  its OriginatorInfo is seen (DER and PEM). A frame over 65 539 bytes (`30 83`) is not found (with the stated 256-byte
  floor, the embedded search's two bounds).
- Info: no false fire on the project's .NET shared framework folders (188 and 144 files) or the two publish folders, with
  the empty list and with a fingerprint listed; cost with one fingerprint listed about 0.34 s per 32 MB of base64 text.
- Coupling: kit B2053 (seat X65 READY at `105b3465`) reads `Ran 111` / `--unit 111 --floor 111` and lands FIRST; kit
  B2056 carries the stamped rule that after a rebase both `--unit` and `--floor` are the new main's own.
