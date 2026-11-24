The first slice of the OneDrive module (WP1.8): browse My Drive, the root or one folder by its item id, through the
shared Graph layer (#10), built and tested against a fake Graph only. One commit, `4b9814f1`, on `main` `89a10a1b` (the
pull request's merge ref is built on the main of the moment). Thirteen paths: two new projects
(`src/Datasec.Suite.OneDrive/`, `tests/Datasec.Suite.OneDrive.Tests/`, with their two new lock files) and two added
lines in `Datasec.Suite.slnx`. No package, no existing lock file or project file, no workflow, no file of the Graph layer.

## Why

- The rebuild needs OneDrive's My Drive listing on the panel. The product owner's answers bound it: "a, Drop it" (OneDrive
  "Shared with me", C-82), "b, Drop Recent too; his note: rebuild without graph" (C-83), and "no deprecated Graph calls"
  (C-84); the records read his note as "no deprecated Graph calls". So: Graph is allowed; no deprecated call; no Recent; no
  Shared with me.
- The layer's own page walk (`GetPagesAsync`) follows any next link on the origin before the caller sees it, so a server
  could lead it to a deprecated call. This module checks each next link before it is requested.

## What changed

- **`MyDriveBrowser`.** `ListRootAsync` and `ListFolderAsync(itemId)` send `GET me/drive/root/children` or
  `GET me/drive/items/{id}/children`, each with `$select=id,name,size,lastModifiedDateTime,folder,file,remoteItem`, by
  `GraphClient.SendAsync`. An id outside the rule (1 to 256 ASCII letters, digits or `! . _ -`, not `.` or `..`) sends
  nothing. A next link is requested only when it is https on the base host and port, no user info, and a children call of
  four forms (`me/drive/root`, `me/drive/items/{id}`, `drives/{id}/root`, `drives/{id}/items/{id}`); anything else ends
  `NextLinkElsewhere` and is never requested; a repeat ends `PagingLoop`; page 101 ends `TooManyPages`.
- **Items by rule.** An item that is not an object, has an id outside the rule or listed twice, an empty name, both facets,
  or a size, date, child count or `remoteItem` of the wrong shape ends `MalformedItem` (page and item numbers only). A
  `remoteItem` entry is listed (`PointsToOtherDrive`) and never followed.
- **Text.** The module's README: the one call and its Microsoft page, the calls not built, what a listing reads, the
  limits. `ToString` and failure texts hold kinds, counts and sizes only.

## What proves it

- Red first: 41 of 49 cases fail by assertion on a permissive first shape. Green: 2202 / 0 / 2198 / 4 locally; the
  branch's push run 45372638705: linux 2198 succeeded, windows 2181, rules 671 files, secret scan clean. Merged with
  `main` `f5882ed7` (#48): 2220 / 0 / 2216 / 4 locally, rules 671.
- 15 mutants, each red on exactly its cells, none surviving (the select dropped; the id rule's dots, characters or length
  opened; a duplicate, both facets, a negative size or a remoteItem of the wrong shape taken; remoteItem ignored; the
  next link's path, port or repeat unchecked; the page bound off by one; a name in a text).
- Against the fake handler with the layer's own client: 43 next-link shapes (Unicode and case-folded hosts, punycode, dot
  segments, percent-escaped dots, slashes and backslashes, control characters, a deeper base path, queries, fragments)
  are each refused with nothing sent, or sent as a children call of the four forms on the base host.
- Microsoft's page for the call (driveitem-list-children, v1.0) holds no deprecation mark; the drive resource marks
  exactly two calls deprecated, Recent and Shared with me, and neither is built.

## Still open

- One folder-id case of the tests (O02's second row) has the exact shape of a real consumer OneDrive item id, and its
  origin is not established (not found in Microsoft's documentation): it is to be replaced by an obviously synthetic id
  before this lands.
- How Microsoft Graph really answers (its next-link form, item shapes, ids) is not measured: no tenant, no token, no
  Microsoft host was called. The tenant test is a later step.
- A next link of a `drives/{id}` form is followed whatever drive it names (the module cannot know the user's own drive
  id); the README's "never opens another user's drive" holds for a `remoteItem` entry only.
- A next link that repeats the address just requested with a different fragment is not caught as a repeat: the same
  request can be sent up to the page bound (100).
- A next link's query is not checked (any query on a children path is sent as the server wrote it).
- `drives/{id}/root/children` is documented by Microsoft as the drive's root relationship with list-children, not as a
  request line of the page.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this slice and every choice inside it (browse only, My Drive only; the module's
own page walk over `SendAsync`; the four children forms; an item outside the rules ends the listing; a `remoteItem`
listed, not followed; the narrow select, no thumbnails; the page bound 100; no local CodeQL). The product owner's answers
quoted above (no Shared with me, no Recent, no deprecated Graph calls) bound the slice; no choice inside it is his.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
