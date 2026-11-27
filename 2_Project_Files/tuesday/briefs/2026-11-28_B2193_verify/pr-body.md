OneDrive slice 2. One commit, `028acda4`, on `main` `0ee3b091` (behind 0, ahead 1). Seven files, all inside
`src/Datasec.Suite.OneDrive/` and `tests/Datasec.Suite.OneDrive.Tests/`: five added (`MyDriveFiles.cs`,
`DriveFileException.cs`, `DriveFileBytes.cs`, `FileFake.cs`, `FileTests.cs`), two changed (`MyDriveBrowser.cs`, one
line; the module `README.md`). No package, no project or lock file, no solution line, no workflow, no line of
`src/Datasec.Suite.Graph`, no landed cell.

## Why

The panel's scan and print pages need two calls on the user's own drive: put a scanned file into a chosen My Drive
folder, and read a file's bytes for printing. This change adds both to the OneDrive module, tested against a fake.

## What changed

- **`MyDriveFiles.UploadAsync(folderId, fileName, content, length, tokens, ct)`**: every argument is checked before
  any request (the folder id by the browse slice's id rule; the name by this module's narrow rule: 1 to 128 ASCII
  letters, digits, `.`, `_`, `-`, no leading or trailing dot; a readable, seekable stream holding exactly `length`
  bytes, 1 or more). Then ONE session call, `POST me/drive/root:/{name}:/createUploadSession` or
  `POST me/drive/items/{id}:/{name}:/createUploadSession` with the body `{"item":{"@microsoft.graph.conflictBehavior":"fail"}}`,
  through `GraphClient.SendAsync` (the token goes there). Its `uploadUrl` must be absolute https, with no user info,
  at most 8192 characters; otherwise the upload ends as `MalformedSession` and no piece is sent. The pieces go through
  the existing `GraphClient.UploadAsync`, which sends no Authorization header. The stored item must be a file whose
  size, when given, is the length sent.
- **`MyDriveFiles.DownloadAsync(itemId, tokens, ct)`**: the id checked first; ONE item call, `GET me/drive/items/{id}`,
  through `GraphClient.SendAsync`; a folder (`NotAFile`), a size above the bound (`TooLarge`) or a download address
  outside the same address rule (`MalformedItem`) is refused before any fetch. Then ONE plain `GET` of the item's
  `@microsoft.graph.downloadUrl` through the `HttpClient` the caller hands in, **with no header added**, under the Graph
  options' attempt time-out joined with the caller's token. A status other than 200 is `DownloadStatus`; the body is
  read to at most the bound plus one byte (`TooLarge` past it, the rest not read); a length other than the item's size
  is `DownloadLength`; a failure below HTTP or the time-out is `DownloadTransport`.
- **`DriveFileException`** (seven kinds; its message holds the kind and the status number only, no inner exception) and
  **`DriveFileBytes`** (`ToString` holds the length only). A failed Graph call is not wrapped: it leaves as the layer's
  own `GraphCallException`.
- **`MyDriveBrowser.ReadItem`** is now `internal`, so uploaded and downloaded items are read by the same item rules
  as listed ones.
- **The module README** gains a section for this slice: the three calls with their source rows in the project's
  analysis of the source app, each "not measured against Microsoft Graph"; the rules; the failure kinds; the limits.

## What proves it

- Thirteen new cells, F01 to F13 (43 cases), against a fake handler that records every request's method, address,
  Authorization header, Content-Range and body. F09 is the token cell: the item call carries the synthetic Bearer, the
  download request carries no Authorization header. F04, F05 and F10 send zero requests for every refused argument;
  F06 sends exactly one request (the session call, no piece) for each unreadable session answer; F11 never fetches an
  item it refuses; F13 finds no name, id or address in any failure text or `ToString`.
- The OneDrive test executable `Total: 93` (50 before), `Failed: 0`; the whole solution `total: 2488` (43 more than
  `main`), `failed: 0`, locally and on both hosted legs (linux `succeeded: 2484`, windows `succeeded: 2467`); build
  `0 Warning(s)`, `0 Error(s)`; rules 744 files; release guard 14 and 15 files (unchanged); secret scan clean.
- Eight planted faults in `MyDriveFiles.cs` (the conflict rule, a Bearer header on the download request, the https
  test, the stored size check, the name's dot tests, the size bound, the downloaded length check, the file kind check)
  each turn their cells red, and each was undone and proved; further planted faults (the user-info test, the read
  bound, the stream checks, both id checks, the session address rule, the transport mapping) also turn cells red.

## Still open

- Built against a fake only: how Microsoft Graph and its download hosts answer each of these calls (the session
  answer, a name already taken, the item, the download address and its body) is not measured.
- The host that hands in the download `HttpClient` must give it no default Authorization header; whether it follows a
  redirect from the download host is the host's choice (a redirect not followed ends as `DownloadStatus`).
- The download is not retried and has no time-out of its own: a slow 100 MiB download must finish within the Graph
  options' attempt time-out (100 s by default) or it ends as `DownloadTransport`.
- The download address's host is not bound (which hosts Microsoft uses is not measured): the module fetches whatever
  https address the item answer names, without a token.
- A session left open after a failed upload is not deleted; its expiry is Microsoft's.
- The file name rule is narrower than OneDrive's. The browse slice's id rule (`MyDriveBrowser.IsItemId`, its pattern
  ends in `$`) takes an id ending in one line feed: such a folder id reaches the session call as `%0A` in its address,
  and such a download id is sent with the line feed dropped. The fix (`\z`, as the new file-name rule already uses)
  belongs to a later change of the browse rule.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this change and every choice inside it (an upload session for every size; the
two-step download with no header on the download address; the conflict rule `fail`; the narrow file-name rule; the
100 MiB bound as a constructor argument; one address rule for both answers; the browse slice's item rules). No choice
in this change is the product owner's.

Nothing is deployed; nothing was sent to or run against any tenant, printer or device.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
