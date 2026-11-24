GATE B2059: NO GO @ c16306c on main 89a10a1

Gate G1 (a CI and security control: the release guard decides what may ship; the commit touches `.github/workflows/ci.yml`
and `build/`), round 1 of 2 of lane L4, one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, lane L4, kit
B2057 (seat X67; Stamp S4: Q1 "a", Q2 "a", Q3 "after B2053" in words; Q4 to Q9 the defaults; every one the coordinator's,
none the product owner's). Head `c16306caea94d73af099e7c5ef40a1f51627ec65` on `b2057/l4-release-guard-cert-forms`, ONE
commit, one parent `89a10a1ba26a16aae7996e059d548bf53531fd44` (= main; no rebase). Main did NOT move during the gate
(89a10a1b by `gh api -X GET` at about 20:58 and 21:06; open pull requests 0; the branch still at c16306ca at 21:06).
Read and measured 2026-11-24 about 20:56 to 21:15 AEDT in my scratch `fleet/state/s324/g2059/`: `clone` (clone.py draft:
push URL `invalid://no-push`, no identity; worktree switched detached to the head), worktree `red` (89a10a1b +
`1-red.diff`). The two dotnet publishes through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a
time (2 released lock folders, both mine, in `g2059/_quarantine/locks/`; lock waits 3 and 9; no other holder's lock
touched; the lock absent at the end). No write to the project, GitHub or Jira; no push, no pull request, no re-run; no
printer, no device, no Azure; nothing deleted (moved to `_quarantine`).

**BLUF.** The head is BASE plus the two frozen patches byte for byte (temporary index: `a17a3507` = `c16306ca^{tree}`); the
ten tools equal THE TOOLS' sha256 in my copy and in the seat's `.tools/b2057/gate` (10 of 10 each); red first exactly the
three cases by `AssertionError`; green `Ran 115 tests`, `OK`; `MUTANTS: 10 of 10 MATCH, 10 of 10 undone equal` (my run of
the frozen tool); `CHECKS: 10 of 10 PASS`; the hosted push run `HOSTED c16306ca...: PASS` (my read); the two publish
folders read `GUARD: clean (14 files)` / `(15 files)` at BASE and at the head with the shipped list and with a fingerprint
listed. The change NEVER reads less than BASE (every probe row BASE read clean or the same finding), and with today's empty
list it is dormant (cost x0.9 to x1.0). **But the form it exists to close is closed only for some certificate sizes:**
wrapped base64 whose last line holds fewer than 16 base64 characters reads clean with the certificate listed (MEASURED: 407
of 1793 DER sizes from 256 to 2048 bytes at 64 columns LF, 22.7%; 341 at 76 columns CR LF, 19.0%), and indented wrapped
base64 (the seat's H12) reads clean at every size. The docstring, the commit subject and the kit's FOR RECORDS say "a bare
or line-wrapped base64 file" is judged; the cell passes only because the throwaway certificate's last 64-column line holds
46 characters. A records pass reading this head would tick owed 23's base64 form as closed while about one wrapped
certificate in five is not seen. Both are one `BARE_BASE64_RUN` re-draft in round 2 (FOUND 1 and 2).

## FOUND

1. **Major, BLOCKS (wrapped base64 with a short last line is not seen: 22.7% of certificate sizes at 64 columns).**
   `release_guard.py:77` `BARE_BASE64_RUN = re.compile(rb"[A-Za-z0-9+/]{16,}(?:(?:\r?\n|\\r\\n|\\n)[A-Za-z0-9+/]{16,})*")`:
   every joined line needs 16 base64 characters, and `=` is outside the class, so the LAST line of a wrapped certificate
   joins only when it holds 16 or more base64 characters before its padding. When it holds 1 to 15, the run ends a line
   early, the decoded bytes lack the certificate's tail, and `embedded_der_fingerprints` (`:115`-`:123`, landed) yields no
   hash because `end > len(data)`. MEASURED (`g2059/scratch/probe.py`, `logs/probe.out`; synthetic DER runs framed
   `30 82 <len>` with random bodies, each one's own SHA-256 listed, which is all the guard reads): sizes 256 to 2048 bytes,
   64-column LF wrap CLEAN for 407 of 1793 (first 289, 290, 291 ...), 76-column CR LF wrap CLEAN for 341; every clean size
   has a last line of 2 to 15 base64 characters, every seen size 16 or more. Rows C1 to C4 at one slipping size: one line
   (`x5c`) G2; 64-column wrapped CLEAN; the same as a JSON string joined by backslash n CLEAN; the same bytes in a PEM
   `CERTIFICATE` block G2 (landed rule, contrast). The landed throwaway certificate (754 bytes, 1008 base64 characters)
   wrapped at 67 columns (last line 3 characters, row A19) reads CLEAN. The docstring (`:20`-`:23`) claims "a bare or
   line-wrapped base64 file"; its Limits paragraph (`:40`-`:45`) does not name this. Not a regression (BASE reads every
   one of these clean too) and dormant while the list is empty, so nothing ships differently today; it blocks because the
   lane's one property (P2) is false for about one size in five of the most common wrapped forms and the records would
   close owed 23 on it. Fix (round 2, `2-fix.diff` only): let the run end in one short line (for example
   `(?:(?:joiner)[A-Za-z0-9+/]{1,15})?` after the repeated group), or drop the per-line minimum (any prefix glued to the
   run is already handled by the four alignments: only the alignment mod 4 matters); add a cell whose last wrapped line is
   under 16 characters (the throwaway certificate at 67 columns, or a DER run made in the test) and a mutant that restores
   `{16,}`.

2. **Major, BLOCKS with 1 (indented or blank-padded wrapped lines are not seen at any size: the seat's H12, confirmed and
   widened).** The same pattern: a joiner must be followed directly by a base64 character, so each indented line is its
   own 64-character run, under `MIN_BARE_BASE64` 128 (`:79`). MEASURED (rows A2 to A5, the throwaway certificate listed,
   64 columns): YAML block scalar with 2-space indent CLEAN; XML with 4-space indent CLEAN; tab indent CLEAN; one space
   before each LF CLEAN; control the same lines unindented G2 (A0). Grade: these are the ordinary shapes of a certificate
   in configuration text (a YAML block scalar, an indented XML element such as a SAML metadata `X509Certificate`), and the
   docstring's "line-wrapped base64 file" covers them in a reader's eyes while its Limits name only "any other line end".
   The landed PEM rule takes the same indentation (row B10, `split()` at `:145`). The seat MEASURED and named it and added
   no cell, as the frozen patches required; the gate grades it Major and closes it with 1 in the same regex re-draft:
   allow `[ \t]*` on either side of a joiner (or strip horizontal white space before matching), with an indented row in
   the same cell and a mutant.

3. **Minor, does not block alone (the Limits paragraph names only some of the shapes that read clean).** MEASURED clean
   with the certificate listed, BASE clean too: a certificate split across two JSON strings (array chunks, A10; string
   concatenation, A11), an XML character reference `&#xA;` between lines (A7), base64 of base64 (A16). Stated limits
   MEASURED as stated: base64url (A8: the certificate's base64 holds 11 `+` and 14 `/`, so the form differs), a
   JSON-escaped slash (A9), CR-only lines (A6), the empty list (A18). Fix: one sentence in the Limits paragraph in round 2.

4. **Info (PKCS#7 and CMS shapes outside the tested PEM one: all seen).** MEASURED G2 at the head: PKCS#7 in DER (B1, and
   at BASE, the landed embedded search); BER indefinite outer length (B2, also BASE); CMS EnvelopedData with the
   certificate in OriginatorInfo, DER (B3, also BASE) and PEM `CMS` (B4, new); PEM `PKCS7` with CR LF and indented body
   (B5, new); a lowercase `pkcs7` label and an `ATTRIBUTE CERTIFICATE` label (B7, B9: by the bare rule, as the docstring
   says for other labels). An undecodable `PKCS7` block is G3 with the empty list (B8, fail closed, as designed); a
   decodable one with the empty list is quiet (B6). A certificate inside EnvelopedData's encrypted content is unreadable by
   any guard (by construction; not named, like PKCS#12's encrypted bag).

5. **Info (false fires: none found).** A G2 of the new rule needs a listed SHA-256 to match a decoded frame, so a false G2
   needs a hash collision; the only new list-independent finding is G3 for an undecodable `PKCS7` / `CMS` /
   `PKCS #7 SIGNED DATA` block. MEASURED (`scratch/cost_and_fp.py`, `logs/cost_and_fp.out`), BASE and head guard on the
   same folders, lines only at the head 0 in every row: the project's .NET shared framework folders read as a
   self-contained-publish analogue (`Microsoft.NETCore.App/10.0.15` 188 files, `Microsoft.AspNetCore.App/10.0.15` 144
   files: every DLL's resources, `.deps.json`, `.runtimeconfig.json`), each `GUARD: clean` with the empty list and with
   the throwaway fingerprint listed; my own publishes (`out/linux` 14 files with `.deps.json`, `out/windows` 15 files with
   `web.config`) clean both ways.

6. **Info (cost).** MEASURED in process on this Mac (Python 3.14.10): with the list empty the head equals BASE (32 MB
   one-line and 76-column base64 text 0.02 s each, 24 MB random binary 0.12 s). With one fingerprint listed: 32 MB base64
   text 0.34 s and 0.40 s (BASE 0.04 s and 0.05 s), the 24 MB binary 0.31 s (BASE 0.14 s); the shared framework folder
   1.07 s (BASE 0.41 s); the publish folders 0.04 s. Acceptable. A crafted file of repeated `30 82 ff ff` frames costs the
   landed embedded search 1.03 s per 256 KB raw (quadratic in the frame count); the head now pays the same 1.06 s on that
   file's base64 text (BASE 0.00 s). Adversarial only, same order as the landed raw cost; not named in the docstring.

7. **Info (docstring against the code, otherwise exact).** "while the list holds a fingerprint" = `:155`-`:156`; "at least
   128" = `:79`, `:159`; "each of its four alignments" = `:161`-`:165`; "a PEM block of any other label is judged only as such
   base64 text" = rows B7, B9; "found by its 30 82 frame only (one shorter than 256 bytes is not)" = `:115`-`:123` (a
   frame over 65 539 bytes, `30 83`, is not either; certificates that large are rare). The code also joins the four
   characters backslash r backslash n (`:77`), which the docstring does not say (in favour). Also seen though unnamed:
   a `data:` URI (A12), a run glued at its end (A13), UTF-16BE with a byte-order mark (A14), UTF-16LE at an odd offset in
   a binary (A15, by the big-endian reading).

8. **Info (the coupling).** The head changes no `GUARD:` line on either leg (hosted and local, 14 and 15) and changes the
   `rules` job's `Ran 111 tests` / `UNIT-TEST FLOOR: ran 111, floor 111` to 115 / 115. Live kits that read 111: kit B2053
   (6 lines: Steps 1, 5, 7(e) `--unit 111 --floor 111`; seat X65 READY at `105b3465`, not rebased) and kit B2056 (7 lines;
   Tuesday's stamp line 247 already says that after a rebase both `--unit` and `--floor` are the new main's own values).
   After this lane lands: B2053's landing text and any B2053 rebase read `Ran 115` / floor 115 (so land B2053 FIRST, as
   ordered); B2056's seat or rebase takes `--unit 115 --floor 115` from the new main's hosted run. `git merge-tree
   --write-tree 105b3465 c16306ca` rc 0, no conflict, tree `e9852147` (the two lanes share no path).

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- `<89a10a1b>..<head>` read whole: three `M` rows, numstat 1/1, 38/7, 88/0 (= THE CODE); the commit message equals
  `commit-message.txt` (289 bytes, subject 231 characters). File sha256 at BASE and head = THE CODE's columns.
- Tree = BASE + both patches byte for byte: temporary index `read-tree 89a10a1b`, `apply --cached` both, `write-tree`
  `a17a3507` = `c16306ca^{tree}` (EQUAL); red tree `4a665788`; `2-fix.diff` alone applies (it touches only the guard).
- Red first (`g2059/red`, `logs/red-unit.log`): `Ran 115 tests`, `FAILED (failures=3)`, 0 errors, exactly
  `test_g2_base64_certificate_without_pem_markers_fires`, `test_g2_pkcs7_and_cms_pem_blocks_fire`,
  `test_g3_undecodable_pkcs7_or_cms_block_fires_and_other_labels_do_not`, each `AssertionError: 0 != 1`; 112 `ok`; the pin
  and the floor case green. Head (`logs/head-unit.log`): `Ran 115 tests`, `OK`.
- Mutants (`logs/mutants.out`, the frozen tool on my clone): 10 rows each MATCH on exactly its listed cases, `undone equal
  True`; porcelain 0 lines after; guard sha256 `e2473ad7...` after. No mutant reddens the PKCS#7 G2 half alone (held by
  the bare rule too, as the kit says). **No mutant or cell covers FOUND 1 or 2** (the cells use one certificate size and
  no indentation).
- Any listed certificate still read clean: YES (FOUND 1, 2, 3). False fires on today's or a plausible publish file: none
  (FOUND 5). Cost: FOUND 6. Docstring: FOUND 7, with the gaps of FOUND 1 to 3.
- The four new cases and nothing else of a landed case: `checks_l4.py` check 8 (0 test lines removed), check 6 (115, new
  4); the three module helpers `der`, `pkcs7_der`, `pem` are new names (no landed name at BASE: `grep -n` of the BASE test
  file's top-level definitions).
- `ci.yml` diff exactly `-          FLOOR=111` / `+          FLOOR=115` (check 2); no job fingerprint moved
  (`test_pipeline_controls.py` green in the head run; the fingerprints read the number as N).
- Hosted run: FOUND 8 and THE HEAD below.

## FRAME (stamp checklist item 11: each every/never/only sentence the change adds, three shapes outside the tested one)

| Sentence | Shapes outside the tested one | Result |
|---|---|---|
| G2: a PEM block labelled PKCS7, PKCS #7 SIGNED DATA or CMS holding a listed certificate | DER file (B1); BER indefinite (B2); EnvelopedData OriginatorInfo in PEM (B4); CR LF + indented body (B5) | covered (all G2) |
| G2: while the list holds a fingerprint, base64 without PEM markers (x5c, bare or line-wrapped; CR LF, LF, backslash n) | short last line (C2, C3, A19); indented / tab / blank-padded (A2 to A5); data: URI (A12); glued at end (A13); UTF-16BE (A14) | **FINDING 1 and 2**; the rest covered |
| Limits: not seen in URL-safe, escaped slash, other line end, under 128, empty list | A8, A9, A6, A18 as stated; split strings (A10, A11), `&#xA;` (A7), double base64 (A16) unnamed | stated limits hold; **FINDING 3** for the unnamed |
| Limits: a PEM block of any other label is judged only as such base64 text | `ATTRIBUTE CERTIFICATE` (B9), lowercase `pkcs7` (B7), `NOTE` undecodable quiet (the cell) | covered; inherits FINDING 1 and 2 |
| Limits: a DER certificate found by its 30 82 frame only | under 256 bytes (stated); over 65 539 bytes `30 83` (unstated) | FOUND 7 (Info) |
| The bare rule does nothing while the list is empty | cost x0.9 to x1.0 on three large files; A18 | covered |

## THE HEAD, MEASURED BY THE GATE (logs `g2059/logs/`)

- `tree_check.out`: the tree, numstat, message, file sha256 (above). `checks_l4.py` on my clone: `CHECKS: 10 of 10 PASS`
  (every control fired).
- Publishes (`heavy.py`, `CI=true`, `-p:NuGetAudit=false`, the two `ci.yml` lines 48 and 78 with `-o` into
  `g2059/out/`): `g-publish-linux: rc 0 (18s, lock waits 3, load1 6.75)`, `g-publish-windows: rc 0 (48s, lock waits 9,
  load1 5.86)`. Head guard: `GUARD-WARN: ... 0 fingerprints (owed)` then `GUARD: clean (14 files)` rc 0 and
  `GUARD: clean (15 files)` rc 0.
- Hosted (`hosted.out`, `hosted3.py c16306ca... --total 2153 --rules 659 --skipped-linux 4 --skipped-windows 21 --unit 115
  --floor 115 --hardened-scan --guard-linux 14 --guard-windows 15`): run 45368713342, attempt 1, four jobs success; linux
  `succeeded: 2149`, windows `succeeded: 2132`, `GUARD: clean (14 files)` / `(15 files)`; rules `Ran 115 tests in`,
  `UNIT-TEST FLOOR: ran 115, floor 115`, `RULES: clean (659 files)`; secret-scan both PLANTED-CONTROL lines, NEUTRAL-SCAN
  1881 objects; check runs beside the four: 0 (no Analyze row on a branch push). `HOSTED c16306ca...: PASS`.
- Main (`hosted-main.out`, the same reader at `--unit 111 --floor 111`): `HOSTED 89a10a1b...: PASS`. Code scanning at
  89a10a1b: csharp, python, actions results_count 0; open alerts repository-wide 0 (GET about 21:04).
- NOT RUN by the gate: the whole dotnet solution (restore, build, test: this diff holds no `.cs`, project or lock file, and
  the hosted legs read `total: 2153` twice each; the seat's local 2153/0/2149/4 RELAYED); `repo_rules.py` locally (no
  file added; the hosted `RULES: clean (659 files)` read).

## THE PROBE (scratch only, never committed: `g2059/scratch/probe.py`, `cost_and_fp.py`; output `logs/probe.out`, `logs/cost_and_fp.out`)

Head and BASE guard in process on temporary folders; the landed throwaway certificate (`cert_der()` of the head's test
module; fingerprint asserted equal to `TEST_CERT_SHA256`) and synthetic DER runs made in the probe; nothing of either
printed; a temporary deny-list per row. Rows A0 to A19, B1 to B10, C and C1 to C4 as cited above.

## SCANS

- gitleaks 8.30.1: control FIRST, a token built by `scratch/plant_control.py` from two halves and 36 random characters
  (never printed), scanned alone: rc 1, `leaks found: 1`; moved to `g2059/_quarantine/gl-control`. The three head blobs,
  the commit message and the added lines under neutral names (`scratch/neutral5`): rc 0 `no leaks found`. `gitleaks git`
  over `89a10a1b..c16306ca`: 1 commit, rc 0 `no leaks found`.
- `words.py --control` `CONTROL FIRED: 13 of 13`; over the added lines (127) and the commit message: `WORDS: clean (2
  files)`. `B2[0-9]{3}`: 0 and 0 (control: this gate's commission 7).
- The landing texts of this folder: SCANS in `landing.txt`.

## NOT RUN

- CodeQL locally (no tool on this Mac for it; the pull request's own run is the authority, `landing.txt` step 3).
- The whole dotnet solution and `repo_rules.py` locally (above). Any run on Windows or Linux by the gate (the hosted run is
  the seat's push run, read by me).
- B2056's head (no `b2056` branch on the origin at 21:06), so the "L3 landed first" numbers are DERIVED from its kit.

## LANDING

**Do not land this head** (FOUND 1 and 2 block). Round 2 of 2: a re-draft of `2-fix.diff` (the run pattern, one Limits
sentence) and of `1-red.diff` (rows for a short last line and for indentation, red first at BASE and at this head), with
a mutant for each; `FLOOR` stays 115 if the rows join the existing case, or rises by the new cases. The landing texts of
this folder are written for this head in the B2052 form so that round 2 only re-pins them; they are NOT a go.
