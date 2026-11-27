## Why

The SharePoint app needs the Graph calls its scan-to-library and browse flows make: find a site, its document
libraries, the list behind a library and its editable columns, a folder's items, an upload into a library folder that
never overwrites, and the column values written to the uploaded file. This is the first slice of the SharePoint
library, built and tested against a fake Graph only. Every choice in it (the slice's scope, every page of the site
search and the folder listing, the first page only of libraries, lists and columns, every upload through one session,
the list-item key from the eTag, no reference to the OneDrive module) is the coordinator's.

## What changed

16 files, all under `src/Datasec.Suite.SharePoint/` and `tests/Datasec.Suite.SharePoint.Tests/` (13 added, 3 changed:
the module's project file gains its reference to the Graph project and NuGet rewrote the two lock files; no package is
added).

- `SharePointBrowser`: `SearchSitesAsync` (`sites?search=<q>&$top=500`, every page; `*` as written when nothing is
  typed, a typed query escaped whole), `ListLibrariesAsync`, `FindLibraryListAsync` (web address, then display name,
  else the only list; two matches by one rule is `AmbiguousList`), `ListColumnsAsync` (only columns that are not
  read-only, not in the `_Hidden` group and of one of five kinds), `ListFolderAsync` (20 a page with the select, every
  page, the list-item key from the GUID inside each item's eTag).
- `SharePointFiles`: `UploadAsync` (ONE `createUploadSession` call whose conflict rule is `fail`, then the pieces with
  no Authorization header; the stored item must be a file whose size, when given, is the length sent) and
  `SetColumnValuesAsync` (ONE `PATCH .../fields` after every value is checked against the offered columns).
- `SharePointIds`, `SharePointException`, the entry types, `ColumnValue`, and the module README (the calls, the rules,
  the limits). Every call goes through the shared `GraphClient`; the module keeps no token, sets no header and makes no
  HTTP client. Messages and `ToString` hold kinds and numbers only.

## What proves it

- Cells S01 to S16 (46 cases) against a fake handler; the test executable `Total: 47, Failed: 0`; the whole solution
  `total: 2610`, `failed: 0`, `succeeded: 2606`, `skipped: 4`; `RULES: clean (795 files)`.
- Ten mutants of the rules each turn their cells red and are undone byte-equal (10 of 10 MATCH).
- The branch's push run: linux, windows, secret-scan and rules green; the two lock files pass the locked restore on
  both legs; the release guard counts unchanged.

## Named limits

- Against fakes only: how Microsoft Graph answers each call (the escaping, `$top` and `$select`, the item shapes, the
  eTag form, the value forms per column kind, the status for a name already taken, the hosts of upload sessions) is
  not measured. Every fake answer is an assumption of the cell that scripts it.
- The upload session's host is not bound: an answer naming another https host receives the file's bytes (with no
  token), and the stored item it answers gives the list-item key the column write then uses.
- A stored item that gives no size is returned without a size check; its name is not compared with the name sent.
- The client handed in must carry no default Authorization header (the pieces go through the same client).
- Libraries, lists and columns: the first page only. A library web address that differs from its list's only by a
  trailing slash or its encoding falls to the name rule. Only `readOnly` and the `_Hidden` group decide "editable".
- The file name rule is narrower than SharePoint's own (ASCII letters, digits, `.`, `_`, `-`).
- Not built: the print path, column values per listed item, the write-permission read, search inside a library,
  create, rename and delete, the simple upload, recent sites and search terms, thumbnails, the panel pages and the host
  wiring.

Nothing here ran against a device, a printer, a tenant, Azure or any Microsoft host. Nothing is deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
