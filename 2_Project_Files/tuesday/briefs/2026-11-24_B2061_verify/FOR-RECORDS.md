# FOR RECORDS: lane L3 round 1 of 2 (kit B2056, seat X66), WP1.8 OneDrive module first slice (browse My Drive), head 4b9814f1 (gate B2061: NO GO)

For the records lane only; nothing here is written into a project file by the gate. **Nothing of this lane has landed:**
gate B2061 reads NO GO on 4b9814f1 for FOUND 1 alone (a test literal), and round 2 follows. Record the lane as "round 1
gated, round 2 owed", not as landed. Who decided every choice of this slice: the coordinator (Tuesday), as coordinator
(kit THE AUTHORITY; Stamp S4 states Q1 "a" and Q2 "a" in words, Q3 G1, Q4 to Q9 the defaults). The product owner's
answers that bound it, quoted as his (CLARIFICATIONS.md C-82 "a, Drop it"; C-83 "b, Drop Recent too; his note: rebuild
without graph"; C-84 "no deprecated Graph calls"; RELAYED from the kit), decide no choice inside the slice.

## The kit's FOR RECORDS (RELAYED from kit B2056, each checked by the gate against the head; to be recorded only when a round of this lane lands)
- WP1.8, the OneDrive module, first slice: browse My Drive (the root, or one folder by its id) through the shared Graph
  layer by Microsoft's list-children call (v1.0), a next link followed only when it is a children call on the same
  origin, items read by rule; built and tested against a fake Graph only (no tenant, no token, no Microsoft host).
  CHECKED: `MyDriveBrowser.cs:60`, `:77`, `:245`, `:262`; O01 to O11 green, each red cell red under its mutants; the gate's
  probe of 43 next-link shapes (VERDICT.md THE PROBE). **Record it with one correction:** the `drives/{id}` forms are
  followed for any drive id (gate B2061 FOUND 2).
- No deprecated Graph call, no Recent, no Shared with me, no search (the product owner's answers recorded as C-82, C-83
  and C-84); owed 116 stays true at the head (check 9). CHECKED: `checks_l3.py` check 9 (0 lines; 2 `"me/drive/`
  literals); Microsoft's drive resource marks exactly Recent and Shared with me deprecated (drive.md:33-34, read by the
  gate by a plain GET); list-children 0 lines holding `deprecat`.
- Named limits: Graph's real next-link form and item shapes are UNMEASURED until the tenant test; an item with a
  `remoteItem` facet is listed and not followed (owed 115 stays open); no thumbnails, download, print, scan, sort, search
  or write in this slice. CHECKED (README Limits; O01's remote row).
- Not built (the coordinator's choice): Shared libraries, the panel pages, the later WP1.8 slices (scan to folder, print).

## Owed items
- **Owed 116** (no recent or sharedWithMe call): stays true at this head (check 9) and at the merge with main f5882ed7.
- **Owed 115** (the `remoteItem` tenant test): open, untouched.
- **New, for round 2 of lane L3 (gate B2061 FOUND 1, Major, blocks landing):** replace O02's literal
  `D4648F06C91D9D3D!54927` (`tests/Datasec.Suite.OneDrive.Tests/BrowseTests.cs:36`) with an obviously synthetic id; its
  origin was not established (0 hits in 28 Microsoft source files; it first appears in the drafter's own patch).
- At the coordinator's choice in round 2 or later: FOUND 2 (a README Limits sentence on the `drives/{id}` forms, or a
  drive-id binding) and FOUND 3 (the loop rule compares the address with its fragment).

## Named limits the gate adds (MEASURED by the gate's probe on macOS arm64, in process, against a fake handler)
- A next link of the form `drives/{id}/root/children` or `drives/{id}/items/{id}/children` is requested for any drive id
  that passes the id rule (gate B2061 FOUND 2).
- A next link equal to the address just requested plus a different fragment is sent again: the same request up to 100
  times, then `TooManyPages` (gate B2061 FOUND 3).
- Any query on a children path is sent as written (`$search`, `$expand`, path text inside the query); no query reaches
  another path (FOUND 4).
- `drives/{id}/root/children` is documented by composition (the drive's `root` relationship with list-children), not as
  a request line (FOUND 5).
- `lastModifiedDateTime` `01/02/2026` is read as 2 January 2026 (the invariant culture); a name of white space is listed;
  `size` 12.0 or 1e3 and a child count above 2^31 - 1 end `MalformedItem` (FOUND 6).
- Ids of dots (`...`, `a.`) are sent as written; Graph's handling UNMEASURED; no such id can reach a non-children path
  (FOUND 7).
- Local CodeQL is not runnable on this Mac (no Rosetta): the pull request's code scanning is the CodeQL read.
