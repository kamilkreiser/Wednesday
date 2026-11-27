# FOR RECORDS: gate B2208 (Teams slice 1, navigation, round 1 of 2)

For the records pass after the landing (no text of the gate goes into a project file by the gate itself).

- **The Teams module, slice 1 (navigation, WP3.5 / F40) DONE when the squash lands:** the signed-in user's teams
  (`GET me/joinedTeams`), one team's channels (`GET teams/{id}/channels?$select=id,displayName`) and one channel's
  files folder (`GET teams/{id}/channels/{id}/filesFolder`, read as its drive id and item id), through the shared
  Graph layer; every id checked before any request; every item read by the module's own rules. Cells T01 to T13
  (47 cases) against a fake; eight mutants turn them red (gate re-run: 8 of 8 MATCH). Against a fake only: how
  Microsoft Graph answers each call is UNMEASURED. (RELAYED from the kit's FOR RECORDS, confirmed by the gate.)
- **Not built:** the listing of the channel's folder, scan to a channel folder, the channel message, print, file
  management, search, quick access, the panel pages, the host's module line; Recent is not built (the earlier
  ruling's application). (RELAYED from the kit.)
- **Owed to the next Teams slice (from the gate's VERDICT.md, F1 to F3):** end the channel and drive id regular
  expressions at end-of-text (`\z`, not `$`, which admits one trailing line feed), with a cell row each (a channel id
  and a files-folder answer's drive id ending in `\n`); decide whether the team rule should also require
  `[0-9A-Fa-f-]` only (the GUID reader takes `+` and `0x` at the start of a group); decide whether a channel id that
  ends in a dot or is only dots is refused (Microsoft's examples end in `thread.tacv2` / `thread.skype`). Slice 2 sends
  the drive id and item id this slice returns: tighten `IsDriveSegment` before then.
- **Owed to the OneDrive lane (Info, pre-existing, not this lane's):** `MyDriveBrowser.IsItemId`
  (`src/Datasec.Suite.OneDrive/MyDriveBrowser.cs:84`, landed) has the same `^...+$` form and so the same one-trailing
  line feed acceptance.
- **Release guard counts:** main's own published file counts are 28 (linux) and 29 (windows) since lane L3a landed
  (PR 64); kits written before then name 14 / 15. This lane changes neither (the server does not reference Teams).
- **For the first tenant run:** R12 (does `me/joinedTeams` page; is an unescaped channel id answered as the same
  channel; the shared-channel host teams) and R10 (a migrated private channel's root folder and its folder facet);
  also whether the service treats a channel id ending in a dot as written.
- Nothing here ran against a device, a printer, a tenant, Azure, a Microsoft host or HP.
