# FOR RECORDS: lane L5, OneDrive slice 2, round 1 of 2 (kit B2184, seat X93), head 028acda4 (gate B2193: see VERDICT.md line 1)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2184 THE AUTHORITY; stamp S4 states Q2 "a" in words). Nothing here ran against a tenant, a printer
or a device.

## Plan lane L5 (gap M6, "OneDrive scan-to-folder and download-for-print"): DONE against a fake (on this squash)
(RELAYED from the kit's FOR RECORDS; CHECKED by the gate: OneDrive executable `Total: 93, Failed: 0`; whole solution
`total: 2488`, `failed: 0` locally and on both hosted legs; the kit's eight mutants re-run by the gate MATCH.)
- `MyDriveFiles.UploadAsync` puts a file into the root or a folder of My Drive through one upload session (session
  call with the conflict rule `fail`, pieces through the landed chunked upload, the stored item read and its size
  checked); `MyDriveFiles.DownloadAsync` reads a file's item and fetches its bytes from the item's download address
  with no Graph token, under a 100 MiB default bound. Cells F01 to F13 (43 cases) against a fake.
- Against a fake only: how Microsoft Graph answers each call is UNMEASURED.
- Not built: the simple PUT for small files, `GET .../content`, a retry of the download, a DELETE of an abandoned
  session, other drives (SharePoint, Teams), the panel's scan and print pages.

## For later lanes (gate findings; grades and evidence in VERDICT.md)
- **L3 (the host) and the panel lane (L4):** the download `HttpClient` handed to `MyDriveFiles` must carry NO default
  Authorization header (the module adds none; a default header IS sent to the download host, MEASURED by the gate's
  probe). Whether it follows redirects is the host's choice (a redirect not followed is `DownloadStatus`).
- **The download time-out is the Graph attempt time-out** (`GraphOptions.AttemptTimeout`, 100 s by default) over the
  WHOLE fetch, body included, with no retry: a print file near the 100 MiB bound needs about 1 MiB/s or better, or it
  ends as `DownloadTransport`. A later lane that prints large files decides a separate download time-out or a retry.
- **The download address's host is not bound** (design D6): the module will GET any https address an item answer
  names (loopback, link-local and IPv6 literals included, MEASURED by the gate's probe), always without a token.
- **The landed id rule `MyDriveBrowser.IsItemId`** ends its pattern in `$`: an id ending in a line feed passes it
  (MEASURED by the gate's probe): as an upload folder id it reaches the session call as `%0A` in the address; as a
  download id it is sent with the line feed dropped. A later OneDrive lane owns the fix (`\z`, as this lane's
  `IsFileName` already uses; VERDICT.md F1).
- **Memory:** a download at the 100 MiB bound allocated about 488 MiB in the process during the call (MemoryStream
  growth plus the final copy; MEASURED by the gate's loopback probe, process-wide counter). A host that prints large
  files sizes its memory for that, or a later lane reads into one buffer of the item's size.

## Seen, not this lane's
- `release_guard.py` prints `GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)` on both legs (its own
  owed note; RELAYED from the seat's STATUS).
- An orphan test host from an older gate clone (`/private/tmp/b1839-gate/...Sessions.Tests`, parent 1, six days old)
  named by the seat; not touched by the seat or the gate.
