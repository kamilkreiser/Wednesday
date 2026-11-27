GATE B2209: GO WITH FINDINGS @ 65428dc on main 7ca5e4c

Gate G1, ROUND 1 OF 2 of the SharePoint library, slice 1 (kit B2198, seat X101; S4: Q2 "a" and Q8 "a" IN WORDS, the
rest the defaults; every choice the coordinator's). One Opus reader (claude-opus-5-5), in-session, read-only, for
Tuesday s338. Head `65428dc527a5643f5920ce6c64d743010a60665b` on `b2198/x101-sharepoint-slice1`, ONE commit, one parent
`7ca5e4cefb315f57f4490ce245e1fb762dbf9f6d` (PR 65), tree `3bc8976be5daf875a613bc6f2eb3c87228757616`, 795 files.
Re-measured by gh api GET (04:42:52 and 05:04:46 AEDT): main `7ca5e4ce` (tree e8085394), compare ahead 1 behind 0,
16 files (13 added, 3 modified, all under `src/Datasec.Suite.SharePoint/` and `tests/Datasec.Suite.SharePoint.Tests/`),
`matching-refs/heads/b2198` one row = the head; code-scanning open alerts 0 (and 0 alerts in all); open pull requests 0
at 04:42, then ONE at 05:04: PR 66 from `b2197/x100-l1-agent-auth` (lane L1, other files; landing.txt handles it).
Measured 04:42 to 05:04 AEDT in scratch `fleet/state/s338/g2209/` (`clone`: the kit's clone.py `draft`, push URL
`invalid://no-push`, no identity, detached at the head; worktree `probe` at the head plus ONE untracked probe file;
clone porcelain 0 rows at the end, every mutant undone equal). Every heavy job through my copy of the kit's `heavy.py`
(the eight seat tools hash 8 of 8 equal THE TOOLS; heavy.py `89223aca...` = S8; heavy-slots absent, so the canonical
lock) under `<project>/.tools/wave1-heavy.lock.d`; 45 released lock folders of mine in `g2209/_quarantine/locks/`; the
owner.txt of gates B2208 and B2207 read while they held the lock, never broken; no process of mine left. Nothing to any
printer, device, tenant, Azure, Microsoft host or HP: every request in every run went to an in-process fake handler.
No write to the project checkout, the seat's lane folder, GitHub or Jira.

## Grades (round 1 of 2): Blocker 0, Major 0, Minor 2, Info 8. Nothing blocks landing; no fix round.

**F1 MINOR (Tuesday's point b): a stored item with NO size is returned unverified.** `SharePointFiles.UploadAsync`
(`SharePointFiles.cs:118`) refuses a size that differs only when a size is present (`stored.Size is long size && size
!= length`); an upload answer that is a file with no `size` (or `"size": null`) is RETURNED with `Size` null. MEASURED
(probe GB, rows `file NO size` and `file size null`: `RETURNED kind File size none`, requests 2). Sizes 9, 11 and 0, a
fractional or string size, a folder, an item with neither facet, a null file facet, an array body and a 202 that never
ends are all refused (same probe). This is the kit's own C12 wording ("when the answer gave one") and the README states
it, so it is a built choice, not a defect of the seat; but the gate's question "a returned item whose size differs from
the bytes sent is refused, never returned" is only half met: a size the module cannot see is not "the length sent".
Fix shape (one line, slice 2 or a follow-up): `stored.Size != length` (refuse a missing size too), plus a cell row.

**F2 MINOR (cell coverage of the commission's points): four rules hold at the head but no cell turns red when each is
removed.** The gate's own mutants (rows `evidence-mutant-rows-gate.json`, run through `mutants_c3.py` exactly as the
kit's): `gFolderStored` (the stored item's `Kind: File` test dropped: a folder answer returned), `gSchemeUnchecked` (the
session address's https test dropped), `gByNameAmbiguous` (two lists matching by display name no longer
`AmbiguousList`) and `gEtagKeyAnyForm` (the eTag GUID read in any form, not only D) each printed `Total 47 Failed 0 |
red NONE` (DIFFER). The behaviour itself is right at the head (probe GB `folder size 10` refused; GA `http://...`
`MalformedSession`, no piece; GD `twoname` `AmbiguousList`; GD `etag-N-form` no key), and an http session address would
still be refused one layer down by `GraphClient.UploadAsync` (its own https check), but nothing in S01 to S16 pins
them. Controls: the gate's other three rows matched (`gQueryControl` S03, `gTwiceKept` S13, `gTextBound` S13), and the
kit's ten rows 10 of 10 MATCH. Fix shape: four `InlineData` rows (S11 `folder`, S11 `httpsession`, S06 `twoname`, S08
or S09 an N-form eTag) in the next slice.

**F3 INFO (Stamp S1 item 1, named limit): the session address's host is not bound,** and the stored item's eTag (hence
`ListItemKey`, which the caller then PATCHes with the user's token) comes from that host's answer. MEASURED (probe GA):
`https://elsewhere.example.test/s`, `https://[::1]/s`, `https://127.0.0.1:8443/s` and the Graph host itself all receive
the piece, each with `Authorization` null; probe GB `file other key` returns the other key. So whoever answers the
session address can steer which list item of that list the later fields write targets. It needs the Graph answer
(TLS, the trusted origin) to name that host first; the README names the unbound host. Same grade as gate B2193's F2 for
OneDrive. Owed to the host or panel lane: bind the session host once Microsoft's hosts are MEASURED, or check the stored
item's `parentReference`/name before the write.

**F4 INFO (Tuesday's point a, the Authorization path): no path in this module sends a token to the session address;
one path outside it does.** MEASURED: S10 green (piece `Authorization` null); probe GC `401-then-200` (the session call
re-sent with a refreshed token: both POST bodies `SessionBody`, the piece `auth null`); probe GC
`default-auth-header-on-client`: a caller `HttpClient` with a DEFAULT Authorization header puts that header on the
piece (`PUT upload.example.test auth THE CLIENT DEFAULT`). The OneDrive README says "the client handed in must carry no
default Authorization header"; this README does not. The landed host wiring (`LibraryWiring.cs:115`, PR 64) builds its
Graph client with `AllowAutoRedirect = false, UseCookies = false` and sets no default header (grep 0 hits for
`DefaultRequestHeaders` under `src/Datasec.Suite.Server/`), so no live path today. One README line in a later slice.
Redirects: the module's fake answered 307 and the layer threw `HttpStatus 307` with one request (the real handler's
redirect behaviour is the landed host's, `AllowAutoRedirect = false`; NOT tested here with a socket).

**F5 INFO (Tuesday's point a, overwrite paths): no path by which the module asks to replace an item.** READ: one
session call per upload, body always `SessionBody` (the conflict rule `fail`), made by a fresh `StringContent` per
attempt (probe GC: identical on the retried call); no query-string conflict rule, no simple PUT, no second session after
a 409 (probe GC `409`: requests 1, `GraphCallException HttpStatus 409`). Name shapes (probe GC): a trailing dot or
space, a leading space, a fullwidth full stop, a zero-width space, a precomposed or decomposed accent, `~$` are all
refused before any request (ASCII-only rule, so no Unicode normal-form twin can pass); a case-only twin
(`SCAN-0001.PDF`) is sent as written and only the server's `fail` rule can catch it (whether SharePoint compares names
case-blind is UNMEASURED); `CON`, `-`, `_` and `scan-0001..pdf` pass the rule (what SharePoint does with them is
UNMEASURED). The stored item's name is not compared with the name sent (probe GB `file other name`: returned), so a
server that renamed instead of failing would go unnoticed. Mutant `mConflictReplace` turns S10 red (re-run by the gate).

**F6 INFO (P3 edge): an EMPTY web address matches an empty one.** `FindLibraryListAsync` takes `""` as a web address
(`OptionalString` accepts any string): a library with `webUrl ""` and one list with `webUrl ""` match "by web address"
(probe GD `emptyweb-lib-and-list` -> list a, although the names differ). Two such lists give `AmbiguousList`, so it is
never a guess between two, but it is a match on nothing. Treat `""` as absent (a follow-up line).

**F7 INFO (P4, named): what "editable" reads.** Only `readOnly: true` and the `_Hidden` group (ordinal) leave a column
out: a column with `hidden: true` outside that group, a group spelt `_hidden`, and a column carrying a `calculated`
facet beside `text` are offered (probe GD). A8 row 22 names the group rule, so this mirrors the source app; whether
Graph sends `hidden` or `calculated` on these columns is UNMEASURED. Also (seat R15 f, confirmed): a hidden column and an
offered column of one name give one offered column, no refusal.

**F8 INFO (P6, API shape): the columns list carries no list id,** so `SetColumnValuesAsync` checks values against the
columns given and writes to whatever `listId` is given (probe GE `otherlist`: WRITTEN, 1 request). The scan page must
pass the list it read the columns from. Empty list id and empty key are refused (probe GE, 0 requests); an all-zero eTag
GUID becomes a key that the write then refuses (probe GD `etag-zero-guid`; seat R15 g).

**F9 INFO (Tuesday's point c, the 42 quarantined locks): every one was this seat's own job.** READ (python over
`<project>/.tools/b2198-x101/_quarantine/locks/`, 42 folders): every `owner.txt` line 1 starts `B2198 seat X101`, says
`slot 1`, and line 2 is `cwd <project>/.tools/b2198-x101/clone`; every folder's name ends with the label of its own
owner line (42 of 42, mismatch 0), which is the runner's own release naming (`heavy.py:298`, a MOVE by the runner
after the job, not a hand move); the 42 labels are exactly the jobs STATUS lists (base 3, pin 4, green 3, mutants 20,
post 2, chain 5, rebased chain 5). No other holder's lock was moved. Nothing moved back (read only).

**F10 INFO (outside this lane, the Graph layer): a cancelled token still sends one request.** Probe GF: a pre-cancelled
token on `ListLibrariesAsync` recorded ONE request at the fake before `TaskCanceledException`. The module passes the
token on; the send is the landed layer's (or `HttpClient`'s) and is a fake handler here, so not graded for this lane.

## What was measured (FOUND / TESTED / HOW)

- **`<BASE>..<head>` read whole** (16 files: the eight .cs files and README of the module, the project file, the two
  lock files, the fakes and the cells). FOUND: the code matches THE CODE section line for line (the ten mutated lines
  each occur once); the module keeps no token, makes no client, sets no header (checks_sp check 8: `.Authorization` 0,
  `new HttpClient(` 0, controls fired); every public method checks every argument before `SendAsync`/`GetPagesAsync`
  (read); the browser and files hold only readonly fields (probe GF: reflection lists `_graph`, `_maxPages` and
  constants; 32 concurrent searches on one browser each correct). HOW: Read tool and `git diff`.
- **The pin run (head, the gate's own):** locked restore (CI=true) rc 0; build `0 Warning(s)`, `0 Error(s)`; SharePoint
  executable `Total: 47, Errors: 0, Failed: 0`. **Whole solution on the head** (= the squash tree on main 7ca5e4ce, the
  head's one parent): `total: 2610`, `failed: 0`, `succeeded: 2606`, `skipped: 4`, no `failed Datasec.` line (80 s).
  `repo_rules.py <clone>` (no `--source-documents`): `RULES-NOTE: R5 hash half NOT RUN`, `RULES: clean (795 files)` =
  782 + 13.
- **The kit's ten mutants, re-run by the gate on the REBASED head** (the seat ran them only on the pre-rebase tree;
  its NOT RUN says so): my rows written from the kit's table, each OLD found once, row for row equal to the seat's file
  (sha256 differs only by JSON layout); `--list` `LIST: 10 mutants, 1 suites, 16 cells`; `run`: `MUTANTS: 10 of 10
  MATCH, 10 of 10 undone equal`, each red set equal to the seat's lines (mUnknownColumnKept also turns S12 red, inside
  the listed cells). After: clone porcelain 0; rebuild and SharePoint `Total: 47, Failed: 0`. Evidence:
  `evidence-mutants.txt`, `evidence-mutant-rows-kit.json`.
- **The gate's seven own mutants:** 3 MATCH, 4 DIFFER with red NONE (F2). Controls: the three that matched.
- **Probes** (`evidence-probe-source.cs.txt`, output `evidence-probes.txt`): six probe cells in a scratch worktree, the
  same fake handler and rig as the cells; the probe executable `Total: 53, Failed: 0` (47 + 6 probes, which print and do
  not assert). TESTED: 19 session-address shapes and 5 session bodies (GA); 19 stored-item shapes (GB); the retried
  session call, a client default header, a 409, a 307 and 17 names (GC); 11 list, 11 column and 8 folder-item shapes
  (GD); 10 queries, 12 site ids, 4 text values, 3 write ids, the messages of 5 refusals (GE: 0 hold a synthetic value);
  state and cancellation (GF). NOT TESTED: an unpaired surrogate (the file writer turned it into U+FFFD before the
  compiler saw it; the README names it UNMEASURED); a real redirect through a socket handler; anything against Graph.
- **The questions of the kit's gate list:** an argument outside its rule sends nothing (S03 green, 8 rows; probe GE: 12
  site ids, 256-character query, every refused name: requests 0) -- yes, held; a listing leaving an item out silently or
  accepting an id twice -- no (S04, S09, probe GD: duplicate ids, a duplicate JSON property, `..`, a bad date all end the
  call; the only items left out are non-offered columns, by design); the list a guess between two -- no (S06 twoweb,
  probe GD twoname: `AmbiguousList`; F6 edge); a read-only or `_Hidden` column offered -- no (S07; F7 for other
  shapes); an upload that overwrites, sends a token to the session address, or returns a non-file or a wrong length --
  no overwrite request, no token from the module, non-files refused, wrong sizes refused, a MISSING size returned (F1,
  F4, F5); a value reaching the write with an unknown name, another kind or twice -- no (S13, mutants and gTwiceKept); a
  message or ToString with a value -- no (S14; probe GE); a fake answer asserting Microsoft behaviour as fact -- no
  (every fake summary says ASSUMPTION; the README says UNMEASURED 7 times; a scan of the added lines for "Graph
  answers/returns/..." outside an UNMEASURED line found none).
- **Lock files against BASE's (check 4):** `checks_sp.py <clone> 7ca5e4ce g2209/checks`: `CHECKS: 10 of 10 PASS`, every
  control FIRED (check 4: 56 BASE lock files, 68 known packages, project entries 2 and 3). Also MEASURED by python: the
  SharePoint source lock file's `net10.0` entries are EQUAL to the landed OneDrive source lock file's (same four keys,
  same values); the test lock files differ only by the project entry (`datasec.suite.sharepoint` vs `onedrive`). No
  package added.
- **Hosted run on both legs, re-read from GitHub** (`hosted3.py 65428dc5 ... --total 2610 --rules 795 --skipped-linux 4
  --skipped-windows 21 --unit 117 --floor 117 --hardened-scan --guard-linux 28 --guard-windows 29`, no --wait): `HOSTED
  65428dc5...: PASS`, run 46042817427 attempt 1, four jobs success, no run beside the four; linux succeeded 2606, windows
  2589; the SharePoint test dll `passed` on both legs; `failed Datasec.` and `NU1004` 0 lines in both job logs. Negative
  control: the same with `--total 2611` printed `FAIL 4`, rc 1. Main's push run re-read the same way: `HOSTED
  7ca5e4ce...: PASS` at 2564 / 782, guards 28 / 29. Evidence: `evidence-hosted-head.txt`.
- **words.py and gitleaks:** `words.py --control` `CONTROL FIRED: 13 of 13`; over the 1990 added lines (lock lines
  apart, 62) and the commit message: `WORDS: clean (2 files)`; B-number grep 0 and 0 (control: the kit copy 25).
  gitleaks 8.30.1: planted control (a token built from two halves and random characters, never printed) rc 1 `leaks
  found`, then quarantined; the 16 head blobs + added lines + lock lines + message under neutral names (19 files) rc 0
  `no leaks found`; `gitleaks git` over `7ca5e4ce..65428dc5` rc 0 `no leaks found`.
- **CodeQL:** not runnable locally (kit FACTS 6); the pull request's own run is the check (landing.txt step 3).
- **Seat deviations, read:** `Approved` -> `Checked` in the synthetic column (words.py's verb list; not a call shape,
  mutant expectations unchanged) -- accepted; S12's `Due` built at +10:00 to prove the UTC conversion -- accepted; one
  `cd /` in a read-only call -- named by the seat, no effect seen; the rebase onto 7ca5e4ce changed no owned, Graph,
  Logging or Directory path (`compare e1802e24...7ca5e4ce`, seat's read; the gate's whole-solution run is on the rebased
  head) -- accepted.

## For the next round or slice (not blocking)
F1 one line + a row; F2 four rows; F4 one README line; F6 one line. F3, F5, F7, F8 stay named limits for the panel and
host lanes.
