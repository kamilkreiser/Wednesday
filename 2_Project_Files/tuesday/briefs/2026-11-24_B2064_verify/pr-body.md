The first slice of the OneDrive module (WP1.8): browse My Drive, the root or one folder by its item id, through the
shared Graph layer (#10), built and tested against a fake Graph only. Two commits on the branch, `4b9814f1` and
`51e91c26` (the second a fix on the first, no rebase), on `main`'s `89a10a1b`; `main` is now `84f088a2` (behind 2,
ahead 2; the two commits `main` gained, #48 and #49, touch no path of this change). Thirteen paths: two new projects
(`src/Datasec.Suite.OneDrive/`, `tests/Datasec.Suite.OneDrive.Tests/`, with their two new lock files) and two added lines
in `Datasec.Suite.slnx`. No package, no existing lock file or project file, no workflow, no file of the Graph layer.

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
  `NextLinkElsewhere` and is never requested; an address already requested ends `PagingLoop`; page 101 ends
  `TooManyPages`.
- **Items by rule.** An item that is not an object, has an id outside the rule or listed twice, an empty name, both facets,
  or a size, date, child count or `remoteItem` of the wrong shape ends `MalformedItem` (page and item numbers only). A
  `remoteItem` entry is listed (`PointsToOtherDrive`) and never followed.
- **Text.** The module's README: the one call and its Microsoft page, the calls not built, what a listing reads, the
  limits. `ToString` and failure texts hold kinds, counts and sizes only.
- **The first commit's review was NO GO**, on one test literal: a folder id of O02 had the exact shape of a real consumer
  OneDrive item id and its origin could not be established. **The second commit** replaces it with an obviously synthetic
  id of the same rule (`SYNTHETIC0002!12345`), so no commit of `main` will hold it (the squash lands the final tree only);
  compares a next link with the addresses already requested, and sends it, without its fragment
  (`GetLeftPart(UriPartial.Query)`), so a link that differs only by its fragment is a loop (new cell O12; the first commit
  sent the same request up to 100 times); and replaces the README's "never opens another user's drive" with a Limits
  line saying a `drives/{id}` next link is followed whatever drive id it names.

## What proves it

- Red first: 41 of 49 cases on the first commit's permissive first shape, and O12 alone on the first commit (Expected
  `(PagingLoop, 1)`, Actual `(TooManyPages, 100)`), each by assertion. Green: 2203 / 0 / 2199 / 4 locally; the branch's
  push run 45382346368: linux 2199 succeeded, windows 2182, `Ran 111 tests`, rules 671 files, secret scan clean. The
  squash with `main` `84f088a2`, built locally: `total: 2221`, `failed: 0`; `Ran 117 tests`, `OK`;
  `RULES: clean (671 files)`; both publish folders `GUARD: clean (14 files)` and `(15 files)`, as before.
- 16 mutants, each red on exactly its cells, none surviving (the select dropped; the id rule's dots, characters or length
  opened; a duplicate, both facets, a negative size or a remoteItem of the wrong shape taken; remoteItem ignored; the
  next link's path, port or repeat unchecked; the fragment kept; the page bound off by one; a name in a text).
- Against the fake handler with the layer's own client: 43 next-link shapes (Unicode and case-folded hosts, punycode, dot
  segments, percent-escaped dots, slashes and backslashes, control characters, a deeper base path, queries, fragments)
  are each refused with nothing sent, or sent as a children call of the four forms on the base host. Twelve repeat
  variants of a requested address (an empty, `?`, `%00`, `%23`, double, tab or 2000-character fragment; an upper-case
  host or scheme; an explicit `:443`; both with a fragment; a dot segment) end `PagingLoop` with nothing sent again, and
  no request of any probe carries a fragment.
- Microsoft's page for the call (driveitem-list-children, v1.0) holds no deprecation mark; the drive resource marks
  exactly two calls deprecated, Recent and Shared with me, and neither is built.

## Still open

- How Microsoft Graph really answers (its next-link form, item shapes, ids) is not measured: no tenant, no token, no
  Microsoft host was called. The tenant test is a later step (owed 115, the `remoteItem` case, stays open).
- A next link of a `drives/{id}` form is followed whatever drive id it names (not bound to the user's drive; stated in
  the README Limits). What Graph answers for a drive the user cannot open is not measured.
- A next link that differs from a requested address by the case of an item id or of a query option name, or by a
  percent-escaped comma or dollar sign in the query, is a different address and is requested once more before its exact
  repeat ends `PagingLoop`; a server that changes the query on every page is bounded by the page bound (100). Whether
  Graph treats such variants as one address is not measured.
- A next link's query is not checked (any query on a children path is sent as the server wrote it).
- `drives/{id}/root/children` is documented by Microsoft as the drive's root relationship with list-children, not as a
  request line of the page.
- The shared Graph layer's own page walk (`GraphClient.FollowableLink`) still compares a next link with its fragment; not
  changed here.
- Local CodeQL cannot run on this machine; the code scanning of this pull request is the CodeQL read.

## Who decides

The coordinator chose, as coordinator, this slice and every choice inside it (browse only, My Drive only; the module's
own page walk over `SendAsync`; the four children forms, not bound to a drive id; the synthetic replacement id; the loop
compare without the fragment; an item outside the rules ends the listing; a `remoteItem` listed, not followed; the narrow
select, no thumbnails; the page bound 100; no local CodeQL). The product owner's answers quoted above (no Shared with
me, no Recent, no deprecated Graph calls) bound the slice; no choice inside it is his.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
