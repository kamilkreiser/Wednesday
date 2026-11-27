# FOR RECORDS: gate B2209 (the SharePoint library, slice 1, round 1 of 2)

For the records pass after the landing (no text of the gate goes into a project file by the gate itself).

- **SharePoint library slice 1 (work package WP3.4, rows F39, F92, F95) DONE when the squash lands:** site search
  (every page, 500 a page, `*` when nothing is typed), a site's libraries (first page), the list behind a library (web
  address, then display name, else the only list; two by one rule `AmbiguousList`), its editable columns of five kinds
  (not read-only, not `_Hidden`), a folder's items (20 a page, every page, the list-item key from the eTag), an upload
  into a library folder through one session that never overwrites, and the column values written to the file's list
  item after it, every value checked against the list's columns first. Cells S01 to S16 (46 cases) against a fake; ten
  mutants turn them red (gate re-run on the rebased head: 10 of 10 MATCH). RELAYED from the kit's FOR RECORDS,
  confirmed by the gate.
- **Not built in this slice:** the print path (download, conversion), column values per listed item, the
  write-permission read, search inside a library, create, rename and delete, the simple upload under 3.5 MB, recent
  sites and search terms, thumbnails, the panel pages, the host line.
- **Owed to slice 2 or a follow-up (VERDICT.md, Minor, not blocking):** F1 refuse a stored item with no size (one
  line plus a row); F2 four cell rows for rules no cell guards today (a folder as the stored item, an http session
  address, two lists by display name, an eTag GUID not in the D form); F4 the README line "the client handed in must
  carry no default Authorization header"; F6 treat an empty web address as absent.
- **Owed to the panel and host lanes (Info):** bind the upload session's host once Microsoft's hosts are measured, or
  check the stored item before the column write (F3); a stored item's name is not compared with the name sent (F5);
  the column list carries no list id, so the scan page passes the list it read the columns from (F8); "editable" reads
  only `readOnly` and the `_Hidden` group (F7). The host's Graph client (PR 64) already has no default header and
  follows no redirect.
- **Seat X101's 42 quarantined lock folders:** every one the seat's own job, released by the runner itself (VERDICT F9).
- **The gate's texts (MEASURED 05:07 AEDT):** words.py over pr-title.txt, squash-subject.txt and squash-body.txt: 0
  hits each (the texts that enter the repository); over pr-body.md: 5 hits, all by design and never committed: the word
  "coordinator" once (the commission asks the body to name the coordinator's choices, as PR 64's did) and the 4 bytes
  of the attribution line's emoji. gitleaks over the four texts rc 0. `squash_scan.py` NOT RUN by the gate (needs the
  real number).
- Nothing here ran against a device, a printer, a tenant, Azure or any Microsoft host.
