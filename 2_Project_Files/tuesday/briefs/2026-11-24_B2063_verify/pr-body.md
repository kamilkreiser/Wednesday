The release guard judges two more certificate forms against the development CA deny-list. Two commits on the branch,
`c16306ca` and `0ca131eb` (the second a fix on the first, no rebase), on `main`'s `89a10a1b`; `main` is now `f5882ed7`
(behind 1, ahead 2; the one commit `main` gained touches no path of this change). Three files changed:
`build/release_guard.py`, `build/tests/test_release_guard.py` and one line of `.github/workflows/ci.yml` (`FLOOR=111` to
`FLOOR=117`). No C# file, package, lock file, project file, `Datasec.Suite.slnx` line or file under `contracts/`; no
`--release` added to any job.

## Why

- The guard judged a certificate in DER and in PEM labelled `CERTIFICATE`, `TRUSTED CERTIFICATE` or `X509 CERTIFICATE`.
  A certificate inside a PKCS#7 bundle in PEM, and a certificate in base64 text with no PEM markers (a JSON `x5c` value,
  a bare, wrapped or indented base64 file), read clean even with its fingerprint on the list.

## What changed

- **PKCS#7 and CMS in PEM.** `PEM_BLOCK` also matches `PKCS7`, `PKCS #7 SIGNED DATA` and `CMS`; the landed embedded
  search finds a listed certificate inside (G2); a block of these labels that does not decode is G3.
- **Base64 without PEM markers.** `judge_bare_base64`, on the raw bytes and on each UTF-16 reading of a file with a NUL
  byte, runs only while the list holds a fingerprint: a run of at least 128 base64 characters is decoded at each of its
  four alignments and searched for a listed DER certificate (G2). Lines join by CR LF, LF, or the characters backslash n
  or backslash r backslash n, with any spaces or tabs on either side of each line end (`BARE_BASE64_JOIN`); every line
  but the last holds at least 16 base64 characters, the last at least 1.
- **The first commit's review was NO GO**, on two misses of that rule: a wrapped certificate whose last line holds 1 to
  15 base64 characters (about one certificate size in five at 64 or 76 columns) and any indented or blank-padded wrapped
  certificate (a YAML block scalar, an indented XML element) read clean with the certificate listed. **The second commit
  fixes both in the pattern itself** (one optional short last line; spaces and tabs around each line end), adds one case
  for each, and names in the docstring every shape still not seen.
- **Workflow:** `FLOOR=117` (six new planted controls).

## What proves it

- Six new cases in `CertificateFormsBeyondThePemCertificate`: five failed first by their assertion (three on the base,
  two on the first commit), one is a quiet pin; sixteen mutants each turn exactly their cases red; `Ran 117 tests`, `OK`.
- Every DER size from 256 to 2048 bytes, wrapped in sixteen shapes (60, 64, 67, 72 and 76 columns, CR LF or LF, 2- or
  4-space, tab or 6-space indent, a blank before each line end, JSON backslash n and backslash r backslash n, 16
  columns), is seen with its fingerprint listed: 0 clean in every shape (the first commit read 19% to 100% of them
  clean); sizes up to 16 KB sampled the same.
- The merge with `main` `f5882ed7`, built locally: `total: 2171`, `failed: 0`; `Ran 117 tests`, `OK`;
  `RULES: clean (659 files)`; both publish folders `GUARD: clean (14 files)` and `(15 files)`, as before. The .NET shared
  framework folders and the publish folders read the same lines with a test fingerprint listed. With the empty list the
  rule costs nothing; with one fingerprint about 0.4 to 0.6 s per 32 MB of base64 text.

## Still open

- Named limits (docstring): base64 in the URL-safe alphabet, with a JSON-escaped slash, with another line end (a lone CR,
  an XML character reference such as `&#xA;` between lines), with an empty line or a line under 16 characters before the
  last line, split across two strings, base64 of base64, under 128 characters, or with an empty list; a certificate under
  256 bytes or over 65 539 bytes (the landed `30 82` frame).
- Not named and not seen: lines joined by a JSON-escaped line end with a JSON-escaped tab after it (`\n\t`, an
  XML or YAML text with tab indentation stored in a JSON string); a no-break space as indentation.
- Not built, the coordinator's choice: opening tar or gzip members (they stay G3 findings); the root `README.md` form
  list; whether a packaging job must call the guard in release mode, and whether `.pdb` files and the Windows
  `web.config` belong in a package (OXPD2-24, NOT DECIDED 1 and 2, still open); the real development-CA fingerprint.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.
- Every later hosted read of the `rules` job expects `Ran 117 tests` and `UNIT-TEST FLOOR: ran 117, floor 117`.

## Who decides

Every choice in this change (scope, the bounds, the fix in the pattern rather than a pre-pass, two new cases and the
floor, the landing order) is the coordinator's, as coordinator. No choice in this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
