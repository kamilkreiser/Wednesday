STARTABLE: YES (after Tuesday stamps the 8 four-underscore lines; load1 15.2 at 17:04, so the waiter holds until it is below 7)

# B1142 drafter report (kit B1142 / SEAT-M79, C8 Sonnet drafter, 17:00 to 17:12 AEDT by `date`)

## BLUF
Kit `2026-11-02_B1142_SEAT-M79_mps-370-371-scan-and-docs.md` (14,297 bytes by `wc -c`, 8 slot lines by `grep -c`, 0 non-printable bytes) builds two commits on `b1142/mps-370-371-scan-and-docs` from code main `0d4022b9`: (1) `CodeOnly` keeps `{...}` of `$"..."` (nested braces counted) and strips strings before line comments, GTP1 and GTP3 as control lines, red first; (2) three `docs/API.md` sentences in the gate's wording from `B1118_STATUS.md:158-160`. Sonnet C2, gate G2 (tier 2: tests-only plus docs, the mechanism measured by the earlier G1 gate), no product byte, not deployed.

## Facts (instrument, time)
- Main `0d4022b93fcb92b7fa1d00f748d6838828e5fa42` (`gh api -X GET git/ref/heads/main` 17:02; `compare ...main` 0 ahead); open PRs #121, #120; `b1142*` refs 0 (control `b1093` 1); `.tools/b1142` absent (control `.tools/wt-b1137-records` present); `.tools/dotnet/dotnet --version` 10.0.401; `gh auth status` kamilDatasec; `df -g` 274 GiB free; panes: tuesday, Security-Composer-C80, HPSM-POC-H104/G289/G288/R136, MPS-M77, fleet-monitor (no M79).
- Scan file at the pin, fetched raw (142 lines, 0 non-ASCII): `CodeOnly` `:60-65`, `Violations` `:68-82`, detectors row `:84-113`, scan row `:115-127`. Templates: 4 files; 12 `$"` strings; 0 verbatim or raw strings; 0 odd-quote comment lines (python); the allowed helper sits in a hole at `TemplateStore.cs:188` (printed).
- Docs at the pin: 998 lines; `:861-868` has 0 non-ASCII (file total 125 lines with some); the three sentences at `:863-868`. No test reads the file's text (code search: three test files name it in comments only).
- Gate wording `B1118_STATUS.md:158-160` printed; it is ASCII.
- M77 pair: `docs/api/openapi.json` and the snapshot at 0d4022b9 are byte-equal (`cmp`, sha256 82a33eb3...); no overlap with M77 (`web/src/api/contract.sync.test.ts`) or M78 (`B1139`: engine paths, reads `docs/API.md` only).

## REFUSE lines, each against what is live
Stamp slots (fires until stamped, by design; control: the pre-stamp copy reads 8); `.tools/b1142` and `wt-b1142-*` absent (fires if present); no `b1142*` ref; main-moved regex over `compare` files (0 now; control: a one-line `docs/API.md` file); no M79 pane; df 274 against 25; gh account; dotnet 10.x. None fires now.

## D-decisions
- D-1 Scan fix in the gate's shape, but holes counted with nested braces (GTP1's own hole holds `{ }`) and `{{` as text; a single left-to-right scan is allowed. Red first on the unedited `CodeOnly`; 7 plants PA-PG including two single-half reverts.
- D-2 Clean-tree red (scan row or a `MoneyWord` read in a hole) is a STOP, not a fix: no product byte.
- D-3 S4 default: `can leave a copy of the document, full or empty, as ...`; the added comma is the only non-gate character, stated in STATUS.
- D-4 S3 goes right after the "does not detect a hand edit" sentence.
- D-5 Two commits, one push, ahead 2, exactly 2 files.

## Q-questions (each with a default)
- Q-1 The detail "the wording fixes follow as one small change" is not in C-85 or B1137_STATUS.md (0 hits), and C-85 says the ruling settles neither the word-pack sentences nor a deploy. Default: proceed on your stamp as the authority, as the brief says.
- Q-2 Gate round: "round 1 of 2 on this branch", reading that #145's two NO GOs were another artifact. Default: as written.
- Q-3 Does commit 2 merge with commit 1 before the word pack? Default: Tuesday's call at the PR; the kit marks it not deployed.
- Q-4 S2 is long and S3 contradicts nothing, but the sentence before it ("trusts its file, does not detect a hand edit") now sits beside "adopts it when the count is higher". Default: verbatim as the gate wrote it; the gate can judge.

## UNMEASURED
No dotnet build or test was run: the C# clean-tree result, `MoneyWord` over holes, the exact red names, and the time under load. Nested strings in a hole (`{(a ? "x" : "y")}`) are not present at the pin and are not handled by the kit. Block-comment-first order (a `/*` inside a string) is unchanged. Live Jira state of MPSCALC-370/371 was read from the frozen create bodies, not a fresh GET.

## Outside the fences
None. Read-only: `gh api -X GET` (ref, compare, contents at the pin, matching-refs, code search) under the MPS `.gh-config`; `ls`, `tmux list-panes`, `df`, `uptime`, `dotnet --version`; raw copies and python scans in the session scratchpad. No git write verb, decision_queue, Jira write or message; no `cd`.
