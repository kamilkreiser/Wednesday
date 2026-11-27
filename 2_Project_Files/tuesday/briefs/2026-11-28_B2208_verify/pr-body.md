## Why

The Teams app on the printer starts from three Graph calls: the user's teams, the channels of a team, and the folder
that holds a channel's files. This change builds those three calls as a library against a fake, the first slice of
the Teams module. Every choice in it (navigation only, ids sent as written, the channel select, no cache, the Graph
layer's paging walk) is the coordinator's.

## What changed

11 files, all under `src/Datasec.Suite.Teams/` and `tests/Datasec.Suite.Teams.Tests/` (8 added, 3 changed: the module's
project file gains its one reference to the Graph project and NuGet rewrote the two lock files with that reference's
closure only; no package is added).

- `TeamsBrowser.ListJoinedTeamsAsync`: `GET me/joinedTeams`, no query, every page through `GraphClient.GetPagesAsync`
  under the module's page bound (default 100).
- `TeamsBrowser.ListChannelsAsync`: `GET teams/{team-id}/channels?$select=id,displayName`.
- `TeamsBrowser.GetFilesFolderAsync`: `GET teams/{team-id}/channels/{channel-id}/filesFolder`, read as
  `ChannelFolder(DriveId, ItemId)`.
- Every id is checked by its rule before any request (`IsTeamId`, `IsChannelId`; `IsDriveSegment` for the answer's ids).
  A listed item is read only when it is an object with an id in its rule, not listed before, and a non-empty name;
  anything else ends the listing as `TeamsBrowseException` (`MalformedItem`). A files-folder answer needs a folder facet
  and both ids in the drive rule (`MalformedFolder`). Graph-layer failures leave unwrapped. Messages and `ToString`
  carry kinds, numbers and lengths only.
- The module README states the calls, the rules and the limits.

## What proves it

- Cells T01 to T13 (47 cases) against a fake handler: the Teams test executable `Total: 48, Failed: 0`; whole solution
  2611 / failed 0 locally and on both hosted legs of the branch push (locked restore on both legs; release guard
  unchanged at 28 and 29 files: the server does not reference this module).
- Eight mutants of the change each turn their intended cells red (re-run independently: 8 of 8 MATCH), plus ten more
  written independently of the change's author (8 MATCH; the two that survive have no cell row: the team id's length
  test against a padded id, and the drive rule's dot test against a files-folder answer whose id is `.` or `..`; both
  checks are present in the code; the drive rule's refusal of `.` and `..` was measured outside the cells).
- Secret scan and word scan clean over the added lines and the message.

## Named limits

1. Built and tested against a fake Graph only. How Microsoft Graph answers these calls is not measured: whether
   `me/joinedTeams` pages, whether a channel id sent with `:` and `@` unescaped is answered as the same channel, which
   shared-channel host teams the joined-teams call leaves out, and whether a migrated private channel's root folder
   carries a folder facet (if not, the call fails closed as `MalformedFolder`).
2. A next link on the Graph base address's origin that names another Graph path is followed (the Graph layer checks the
   origin, not the path); its items must still pass this module's rules.
3. The channel and drive id rules end in a regular-expression `$`, which also admits ONE trailing line feed: such an id
   passes and is sent with the line feed percent-encoded inside the same path segment (`%0A`); it never adds a segment,
   a query or a fragment. A follow-up tightens both rules to end-of-text (the landed OneDrive item rule has the same
   form).
4. The team id rule is .NET's GUID reader in its hyphenated form behind a length of 36: it also takes a `+` or a `0x`
   at the start of a group, sent as written (no separator is possible). A channel id that ends in a dot or is three or
   more dots passes and is sent as written (.NET keeps the segment; what the service does with it is not measured).
5. No cache: every call asks Graph. Channel membership type is not read.

## Who decides

The coordinator lands this pull request (squash, pinned to the reviewed head). Nothing ran against a device, a
printer, a tenant, Azure, a Microsoft host or HP. Nothing is deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
