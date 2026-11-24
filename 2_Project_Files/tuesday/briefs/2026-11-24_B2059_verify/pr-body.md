The release guard judges two more certificate forms against the development CA deny-list. One commit, `c16306ca`, on
`main` `89a10a1b` (behind 0, ahead 1). Three files changed: `build/release_guard.py`, `build/tests/test_release_guard.py`
and one line of `.github/workflows/ci.yml` (`FLOOR=111` to `FLOOR=115`). No C# file, package, lock file, project file,
`Datasec.Suite.slnx` line or file under `contracts/`; no `--release` added to any job.

## Why

- The guard judged a certificate in DER and in PEM labelled `CERTIFICATE`, `TRUSTED CERTIFICATE` or `X509 CERTIFICATE`.
  A certificate inside a PKCS#7 bundle in PEM, and a certificate in base64 text with no PEM markers (a JSON `x5c` value,
  a bare or wrapped base64 file), read clean even with its fingerprint on the list. Release mode, the name rule, the
  unopened archive formats, key stores and UTF-16 PEM text were built by an earlier change and are unchanged here.

## What changed

- **PKCS#7 and CMS in PEM.** `PEM_BLOCK` also matches `PKCS7`, `PKCS #7 SIGNED DATA` and `CMS`; the landed embedded
  search finds a listed certificate inside (G2); a block of these labels that does not decode is G3.
- **Base64 without PEM markers.** `judge_bare_base64`, on the raw bytes and on each UTF-16 reading of a file with a NUL
  byte, runs only while the list holds a fingerprint: a run of base64 lines (each at least 16 characters, joined by CR LF,
  LF or the two characters backslash n) of at least 128 characters is decoded at each of its four alignments and searched
  for a listed DER certificate (G2).
- **Docstring** names both and the limits. **Workflow:** `FLOOR=115` (four new planted controls).

## What proves it

- Four new cases in `CertificateFormsBeyondThePemCertificate`: three failed first by their assertion on the base, one is a
  quiet pin; ten mutants each turn exactly their cases red; `Ran 115 tests`, `OK`.
- Both publish folders read the same guard lines as before (`GUARD: clean (14 files)`, `(15 files)`) with the shipped
  list and with a test fingerprint listed; the .NET shared framework folders read clean both ways.

## Still open

- Named limits (docstring): base64 in the URL-safe alphabet, with a JSON-escaped slash, with another line end, under 128
  characters, or with an empty list; a certificate under 256 bytes. **Open before landing (round 1 of 2): wrapped base64
  whose last line holds fewer than 16 characters, and indented wrapped lines, read clean; to be closed or named in round
  2.**
- Not built, the coordinator's choice: opening tar or gzip members (they stay G3 findings); the root `README.md` form list;
  whether a packaging job must call the guard in release mode, and whether `.pdb` files and the Windows `web.config`
  belong in a package (the ticket's NOT DECIDED 1 and 2, still open); the real development-CA fingerprint.
- Every later hosted read of the `rules` job expects `Ran 115 tests` and `UNIT-TEST FLOOR: ran 115, floor 115`.

## Who decides

Every choice in this change (scope, the third path, the bounds, the landing order) is the coordinator's, as coordinator.
Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
