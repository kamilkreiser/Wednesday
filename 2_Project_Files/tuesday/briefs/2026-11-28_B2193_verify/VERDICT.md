GATE B2193: GO WITH FINDINGS @ 028acda on main 0ee3b09

Gate G1, ROUND 1 OF 2 of lane L5 (OneDrive slice 2: upload into a My Drive folder, download for print), one Opus
reader (claude-opus-5-5), in-session, read-only, for Tuesday s336. Kit B2184 (seat X93; stamp S4: Q2 "a" the two-step
download IN WORDS, Q1 and Q3-Q7 the defaults; S8 the canonical runner 31adedc8; every choice the coordinator's, none
the product owner's). Head `028acda4fa42ed890ffe4a744bd4b59db9b997b4` on `b2159/x93-onedrive-slice2`, ONE commit, one
parent = main `0ee3b0913c539eb34ae16ca921a65307ff7fa343` (PR 60's squash, L0), tree
`888af9d511ccc420a8df4654fb528441a8caedc0`, 744 files. Main and the branch did NOT move during the gate (gh api -X GET
at 01:23:54 and 01:47:37 AEDT; open pull requests 0 both times; open code-scanning alerts 0). Measured 2026-11-28
01:23 to 01:48 AEDT in my scratch `fleet/state/s336/g2193/` (`clone`: clone.py draft, push URL `invalid://no-push`, no
identity, detached at the head; every mutant and probe ran there and was undone or moved out and proved: porcelain 0
rows at the end). Every heavy job through my copy of the kit's `heavy.py` (8 of 8 tool hashes equal to THE TOOLS;
heavy.py `31adedc8...` = S8) under the OXPd wave lock, one at a time; 49 released lock folders of mine are in
`g2193/_quarantine/locks/`; no other holder's lock touched (at the end the lock is held by `B2188 seat X97`, read,
untouched); no process of mine left. Nothing to any printer, device, tenant, Azure or Microsoft host (the probes'
only sockets were on 127.0.0.1 inside the test process); no Jira; no write to the project checkout, the seat's lane
or GitHub.

## Grades (round 1 of 2): Blocker 0, Major 0, Minor 1, Info 9. Nothing blocks landing; no fix round.

**F1 MINOR (landed rule this lane extends; owed to a later OneDrive lane, not this commit): an id ending in a line
feed passes `MyDriveBrowser.IsItemId` (pattern `^[A-Za-z0-9!._-]+$`; .NET `$` matches before a final `\n`).**
MEASURED by the gate's probe (`evidence-probes.txt`, run b): `UploadAsync("SYNTHETICFOLDER0001\n", ...)` sent the
session call to `.../me/drive/items/SYNTHETICFOLDER0001%0A:/scan-0001.pdf:/createUploadSession` (2 requests, returned);
`DownloadAsync("SYNTHETICFILE0001\n", ...)` sent `GET .../me/drive/items/SYNTHETICFILE0001` (the line feed dropped by
`Uri`) and returned. So P1 ("no request for an argument the module refuses") holds only as far as the landed id rule
refuses: an argument a strict reader would refuse reaches Graph's origin (with the token, same origin as every Graph
call; no other host). The seat named it (R15 a, FOR TUESDAY) as DERIVED; now MEASURED. The fix is one character in a
landed line (`\z`, as the seat already wrote for `IsFileName`, DEVIATION 1) plus a row in O-cells and F05/F10: a
landed-line change outside this kit's C5, so a later lane's, not a round 2 here.

**F2 INFO (design D6, a named limit; the CodeQL read may raise it): the download host is not bound, so an item answer
can point the host's download client at ANY https address.** MEASURED (G01): accepted and fetched, each with
Authorization null: `https://[::1]:8443/...`, `https://[fe80::1%25en0]/...` (zone dropped), `https://127.0.0.1/...`,
`https://169.254.169.254/latest`, a port, `https://graph.example.test/...` (the Graph host: still no token), an IDN
host, a fragment, 8192 characters. Refused before any fetch: `%75ser@`, `:@`, `%40` in the host, a backslash-`@`
form, a tab in the host, an unpaired surrogate, 8193 characters, `ftp:`, `file:`. The trust root is Graph's TLS
answer; no token can follow the address (F5). Tuesday's point (c): a port, an IPv6 literal, a path with `..` (and
`%2e%2e`: both normalised to `/download/0001` by `Uri`) are all TAKEN; percent-encoded user info is REFUSED; none
matters for the token (none carries one) and the host is unbound by design.

**F3 INFO (Tuesday's point b, the download bound: HOLDS; memory is bounded but about 4.7x the bound).** MEASURED over a
real `SocketsHttpHandler` on loopback (G04, the module's own fetch, `UseProxy=false`): no Content-Length, chunked,
endless, bound 1 MiB -> `TooLarge`, 9 ms (server got 2.2 MiB onto the socket before the close); close-delimited
endless -> `TooLarge`; chunked endless at the default 100 MiB bound -> `TooLarge`, 86 ms; Content-Length 200 MiB
declared then 17 bytes and a stall, bound 16 -> `TooLarge` at once (the read stops at bound + 1; no wait for the
rest); Content-Length 5 but 17 bytes sent -> the handler reads 5, returned 5 bytes (size 5 or no size: the lie is
truncated, never over-read); Content-Length 1000 but 17 bytes then close -> `DownloadTransport`. Memory: a body of
exactly 100 MiB returned and the process allocated about 488 MiB during the call (endless at the bound: about
357 MiB; `GC.GetTotalAllocatedBytes`, process-wide, so an upper figure): `MemoryStream` growth plus `ToArray`. Bounded,
but a host must budget about five times the bound per concurrent print download (FOR-RECORDS).

**F4 INFO (R10, named limit, now pinned): the download time-out is the Graph attempt time-out (100 s default) over the
WHOLE fetch, body included, and no cell exercises it.** MEASURED: stall before headers and stall after 2 bytes, attempt
time-out 2 s -> `DownloadTransport` at 2003 ms each. The gate's mutant `gTimeoutDropped` (no time-out at all) SURVIVED
(`Total 93 Failed 0`), as R10 predicts ("no row times out"). At the 100 MiB bound a link under about 1 MiB/s cannot
finish; no retry. The coordinator's design (kit C1 "the fetch"); for records and the print lane.

**F5 INFO (the token path; kit gate questions 1 and 6): no Graph token can reach the download host or the session host
by any path the module controls; the README names the one path it cannot.** Read: the module has no `Authorization`
line and no `new HttpClient(` (checks_l5 check 7, re-run by the gate: 0 and 0); the session call and the item call go
through `GraphClient.SendAsync`, which sets the Bearer per request (`GraphClient.cs:556`) and never on
`DefaultRequestHeaders`; the pieces go through `GraphClient.UploadAsync`, whose PUT and status GET carry no
Authorization. MEASURED: F09 green and `mDownloadBearer` red (kit row, re-run); the SAME HttpClient handed in as both
the Graph client and the download client -> item call Bearer PRESENT, download null (the token is per request);
upload pieces to a session address on the Graph host -> null. The one path: a caller's client with a DEFAULT
Authorization header DOES send it to the download host (MEASURED, G03 `caller-default-auth`: PRESENT). The README
says "the client handed in must carry no default Authorization header" (slice-2 rules, last bullet): named, and in
FOR-RECORDS for L3. Also MEASURED on .NET 10.0.404 (macOS): a followed 302 dropped that default header on the next
request, same origin and another host alike; a 302 not followed is `DownloadStatus 302`; a 429 is `DownloadStatus 429`.

**F6 INFO (kit gate question 2 and 3: no request before an argument check; an unreadable session sends no piece):
HOLDS.** Every check in `UploadAsync` (lines 107-129) and `DownloadAsync` (164-169) precedes the first `SendAsync`.
Cells F04/F05/F10 (0 requests) and the gate's mutants `gFolderIdUnchecked`, `gDownloadIdUnchecked`,
`gUploadLengthUnchecked`, `gSeekUnchecked` each turned F05 or F10 red. Probes: a name with a trailing line feed, a
non-ASCII name, a name holding a space -> `ArgumentException`, 0 requests. Session answers: an empty body, `null`, an
object, an unpaired surrogate, http-then-https duplicates read last-wins (https taken, piece sent there, no token),
https-then-http (refused, 1 request); `gSessionAddressUnread` (any unreadable answer replaced by an address) turned F06
red in 6 of 7 rows. Outside P1 (not an argument): an already-cancelled token let the FAKE record one request before
`TaskCanceledException` (HttpClient hands the request to the handler; a real handler checks the token; Info only).

**F7 INFO (kit gate question 5: no name, id or address in any text): HOLDS.** `DriveFileException`'s message is built
from the kind and the status only, no inner exception; `DriveFileBytes.ToString` the length only; argument messages
are fixed text plus the parameter name (MEASURED: a refused name `namesynthetic0001 x` and folder id
`SYNTHETICFOLDER0001/x` -> messages hold neither). F13 green; the gate's `gTransportInnerKept` (the transport text and
inner exception kept) turned F12 and F13 red. A failed Graph call leaves as the landed `GraphCallException`; the
landed layer's own log line names the session HOST (`GraphClient.cs:96`, `Graph {Method} {Host} ...`), never the path:
landed behaviour, not this lane's.

**F8 INFO (kit gate question 4: does a fake answer assert a Microsoft behaviour as fact?): NO.** `FileFake.cs` summary:
"Every answer it gives is an ASSUMPTION of the test that scripts it"; F08's summary "the fake's 409"; the README's
table marks each call "not measured against Microsoft Graph" and names 409 as "the cells' fake answers". One comment
states a .NET behaviour without a source (`MyDriveFiles.cs:324-325`: a string "that is not valid UTF-8 or holds an
unpaired surrogate escape" makes the reader throw `InvalidOperationException`). MEASURED for the surrogate (refused,
`MalformedItem`/`MalformedSession`); invalid UTF-8 is refused by `JsonDocument.Parse` as a `JsonException` before
`GetString` (DERIVED), so half of the comment's reason does not occur. Harmless either way (both are caught).

**F9 INFO (P3 and the address rule, shapes taken that the kit did not name).** MEASURED: a stored item with NO size is
taken (P3 says "when given"); a stored item whose NAME differs from the name sent is taken (not checked); a 200 in
place of 201 is taken; a size given as a string, a `remoteItem`, a file-and-folder item -> `MalformedItem`. Download
items: no size -> fetched under the bound; size 0 with a 5-byte body -> `DownloadLength`; size -1 -> `MalformedItem`
before any fetch; size 99999999999 -> `TooLarge` before any fetch. Addresses with a leading space or a trailing line
feed are trimmed by `Uri` and taken; `https://@host` has empty user info and is taken. A stream positioned at 50 is
uploaded whole from byte 0 (the layer seeks per piece). None reaches a token or an unbounded read.

**F10 INFO (process).** Seat DEVIATION 1 (`IsFileName` written with `\z` instead of the kit's `$`): correct and
narrower, MEASURED (a trailing line feed refused, 0 requests); no cell or mutant depends on it. DEVIATION 2 (the
slice-1 README heading renamed): an owned line. Extra reds under three kit mutants (F13 under `mHttpsTaken`,
`mUploadSizeUnchecked`, `mDownloadLengthUnchecked`; F06 `relative` under `mHttpsTaken`) reproduced exactly by the gate,
all inside the suite's cells.

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), whole
1. **`BASE..head` read whole, seven files** (`git diff --name-status --no-renames 0ee3b091 028acda4`): 5 A
   (`DriveFileBytes.cs` +19, `DriveFileException.cs` +49, `MyDriveFiles.cs` +329, `FileFake.cs` +151, `FileTests.cs`
   +336), 2 M (`MyDriveBrowser.cs` +1 -1, the one C5 line; `README.md` +61 -5). Every line read. The stored commit
   message equals the frozen `commit-message.txt` byte for byte (253 bytes). compare (GET 01:23:54): ahead 1, behind 0.
   checks_l5.py re-run by the gate against `0ee3b091`: `CHECKS: 9 of 9 PASS`, every control FIRED; its `added.txt`
   byte-equal to the seat's (`cmp` rc 0).
2. **The pin run, the gate's own** (fresh clone, `evidence-pin-and-mutants.txt`): locked restore (CI=true) rc 0;
   unlocked restore `LOCKS: 56 of 56 equal`; porcelain 0; build `0 Warning(s)`, `0 Error(s)` (56 projects);
   OneDrive executable `Total: 93, Errors: 0, Failed: 0`; whole solution (TIMEOUT 1800, 92 s) `total: 2488`,
   `failed: 0`, `succeeded: 2484`, `skipped: 4`, `failed Datasec.` 0, `did not end within` 0.
3. **Each mutant's reds, re-run by the gate** (kit tool `mutants_c3.py run` over the seat's rows file, sha256
   `ed0b72d9...` = the seat's STATUS; the eight OLD/NEW texts equal THE MUTANTS table): `MUTANTS: 8 of 8 MATCH, 8 of 8
   undone equal`, each red set identical to the seat's lines. The gate's own nine rows (`evidence-gate-mutant-rows.json`):
   8 MATCH (gUserInfoTaken F06 F11; gReadBoundDropped F12; gUploadLengthUnchecked, gSeekUnchecked, gFolderIdUnchecked
   F05; gDownloadIdUnchecked F10; gSessionAddressUnread F06; gTransportInnerKept F12 F13) and 1 survivor by design
   (gTimeoutDropped, F4). Porcelain and `MyDriveFiles.cs` equal after; rebuild and `Total: 93, Failed: 0`.
4. **Token to the download or session host by ANY path:** F5 (none through the module; a caller's default header is
   the README-named path). **Request before an argument check:** F6 (none; F1 is the landed id rule). **Unreadable
   session sends a piece:** F6 (never). **Fake asserting Microsoft behaviour:** F8 (no). **Name, id or address in a
   message or ToString:** F7 (none). **README names "no default Authorization header":** yes (F5).
5. **The hosted run on both legs** (gate's `hosted3.py` on push run 46014528584, `--total 2488 --rules 744`):
   `HOSTED 028acda4...: PASS` (linux succeeded 2484 skipped 4 GUARD 14; windows succeeded 2467 skipped 21 GUARD 15;
   RULES 744; UNIT-TEST FLOOR 117/117; secret-scan controls and `no leaks found`); the OneDrive test dll `passed` on
   both legs; `failed Datasec.` 0 and 0 (control `Datasec.` 217 and 251); control `--total 2489` -> `FAIL 4`, rc 1.
6. **words.py and gitleaks:** SCANS below. **CodeQL:** NOT RUN locally; the pull request's own run (landing.txt 3).

## TUESDAY'S POINTS
(a) **The rebase onto L0's landing:** the head's tree = main `0ee3b091`'s 739 entries (737 identical by mode and blob,
none removed) plus the 5 added and the 2 changed, nothing else (by program over `ls-tree -r`,
`evidence-tree-equality.txt`). The seat's unpushed pre-rebase commit `de625a7a` (read in its clone by `cat-file`/
`ls-tree` only) carries the SAME seven blobs, and `MyDriveBrowser.cs` / `README.md` are identical at `7d652c5f` and
`0ee3b091`: the rebase changed no byte of the lane. (b) F3. (c) F2.

## ADVERSARIAL: three shapes outside each property
- **P1:** a trailing line feed in a name (refused), in a folder id and in a download id (TAKEN, F1); a non-ASCII name
  (refused); a 128-character name (taken). Covered / F1.
- **P2:** duplicate `uploadUrl` keys (last wins, both orders safe); `uploadUrl` null / object / empty body (refused);
  a session address on the Graph host (taken, no token on the piece). Covered.
- **P3:** stored item with no size / another name / status 200 (taken: named limit F9); size as a string,
  `remoteItem`, file-and-folder (refused). Named limit F9.
- **P4:** a caller default header (sent: README-named, F5); a redirect followed (default header dropped by .NET,
  MEASURED) or not followed (`DownloadStatus`); the same client for Graph and download (no leak). Covered / named.
- **P5:** no Content-Length endless, a lying Content-Length both ways, a stall after headers (F3, F4). Covered;
  time-out unpinned by cells (F4).
- **P6:** argument messages, the transport mapping (`gTransportInnerKept` red), the landed layer's log line (host only,
  landed). Covered.
- **P7:** landed cells O01-O12 green under every mutant and probe run; whole solution 2488/0. Covered.

## SCANS
- gitleaks 8.30.1: control FIRST (a token-shaped value built from two halves and random characters, never printed,
  outside the clone) rc 1 `leaks found: 1`, moved to `g2193/_quarantine/scan-control`; `gitleaks git` over
  `0ee3b091..028acda4` (`1 commits scanned`, `--ignore-gitleaks-allow`) rc 0 `no leaks found`; the seven head blobs
  and the commit message under neutral names `1.txt` to `8.txt` rc 0 `no leaks found`.
- words.py: `--control` `CONTROL FIRED: 13 of 13`; over `added.txt` (946 lines = the commit's insertions) and the
  stored message: `WORDS: clean (2 files)`.
- Landing texts: `words.py` over squash-subject (with #61), squash-body, pr-title `WORDS: clean (3 files)`;
  `build/squash_scan.py` from the head's `build/` with #61: `SQUASH-SCAN: clean` (control rc 1, found 2). pr-body.md
  holds the words the commission requires ("coordinator", "product owner") and the attribution line's emoji: not
  committed text.
- CodeQL: NOT RUN locally (kit FACTS 6). Main's baseline at 0ee3b091: csharp, python, actions results 0; open alerts 0.

## NOT RUN
CodeQL locally; anything against Microsoft Graph or a real download host (every Graph answer is the fake's; the
download probes ran against a loopback server through the real .NET handler); a Windows local run (hosted only); a
merge with any main other than 0ee3b091 (none moved). No pull request opened, no push.

## MAIN AT THE END
`0ee3b0913c539eb34ae16ca921a65307ff7fa343` (GET 01:47:37); branch `b2159/x93-onedrive-slice2` =
`028acda4fa42ed890ffe4a744bd4b59db9b997b4`; open pull requests 0; open alerts 0; newest pull request 60.

## LANDING
`landing.txt`, `pr-title.txt` (153 characters), `pr-body.md`, `squash-subject.txt` (the commit subject + ` (#PRNUM)`),
`squash-body.txt`, `FOR-RECORDS.md` in this folder. Evidence: `evidence-*.txt`, `evidence-gate-mutant-rows.json`,
`evidence-probe-source.cs.txt` (the gate's probe cells, never committed; moved to `g2193/_quarantine/probe/` after each
run). Run logs: `fleet/state/s336/g2193/logs/`.
