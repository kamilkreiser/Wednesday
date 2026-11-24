# FOR RECORDS: lane L3 rounds 1 and 2 (kits B2056 and B2062, seats X66 and X69), WP1.8 OneDrive module first slice (browse My Drive), head 51e91c26 (gate B2064: GO WITH FINDINGS, round 2 of 2; round 1 gate B2061: NO GO)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator, never the
product owner (kit B2062 THE AUTHORITY; stamp S4 of each kit states its Q-answers in words as Tuesday's; the launch of the
lane sweep is the product owner's "Scope stands, go", which rules on no content of this lane). The product owner's
answers that bound the slice, quoted as his (CLARIFICATIONS.md C-82 "a, Drop it"; C-83 "b, Drop Recent too; his note:
rebuild without graph"; C-84 "no deprecated Graph calls"; RELAYED from the kits), decide no choice inside it.

## What the two rounds give, together (CHECKED by the gate at 51e91c26 and on the squash tree 0f34cebf)
- WP1.8, the OneDrive module, first slice: browse My Drive (the root, or one folder by its id) through the shared Graph
  layer by Microsoft's list-children call (v1.0), items read by rule; built and tested against a fake Graph only (no
  tenant, no token, no Microsoft host). CHECKED: 12 cells, 50 cases green locally and on both hosted legs; 16 mutants
  MATCH; the gate's probe of the 43 next-link shapes reads exactly as round 1 (VERDICT.md THE PROBE).
- A next link is followed only when it is a children call of four forms on the base origin AND not an address already
  requested, its fragment set aside; a fragment is never sent (round 2, gate B2061 FOUND 3 closed). CHECKED: O12 red
  first on 4b9814f1 (TooManyPages, 100) and green at the head (PagingLoop, 1); probe P2 now PagingLoop at page 1 with ONE
  request (round 1: 100 requests); twelve fragment, host, scheme, port and dot-segment repeat variants each PagingLoop
  with nothing sent again; no probe request carries a fragment.
- The test literal of round 1 (O02's second row, gate B2061 FOUND 1) is replaced by `SYNTHETIC0002!12345`; the squash
  tree holds the round-1 literal in no file (gate's `git grep -i -F` rc 1 at 0f34cebf; control rc 0 at 4b9814f1), and no
  consumer-shaped id in any of its 671 files. **Its commit 4b9814f1 stays on the branch and in the pull request's ref
  (gate B2064 FOUND 1).**
- The README Limits now say a `drives/{id}` next link is followed whatever drive id it names (gate B2061 FOUND 2 closed
  as a stated limit; no binding built, the coordinator's choice Q2 "a").
- No deprecated Graph call, no Recent, no Shared with me, no search: owed 116 stays true at the head and on the squash
  tree (`checks_l3.py` check 9: 0 lines; 2 `"me/drive/` literals); Microsoft's list-children page 0 lines holding
  `deprecat` (re-read by the gate by a plain GET, 7596 bytes, the same size as rounds 1's reads).

## Owed items, proposed for the records pass (the records seat reads and decides; none is ticked by the gate)
- **Owed 116** (no recent or sharedWithMe call): true at this head and on the squash tree.
- **Owed 115** (the `remoteItem` tenant test): open, untouched. Graph's real next-link form, item shapes and ids stay
  UNMEASURED until the tenant test (C-76's test tenant).

## Named limits carried (RELAYED from kit B2062's FOR RECORDS, each CHECKED against the head)
- A `drives/{id}` next link is not bound to the user's drive (README `:41`-`:44`; probes F4, F5 sent).
- The module has no next-link length bound of its own (the layer's applies only inside `GetPagesAsync`).
- A query option outside the five the page documents can be sent when a server names it (gate B2061 Info 4; probes Q1 to
  Q4 sent with the query unchanged, the path a children path).
- **For the Graph layer (not this lane's):** the landed `GraphClient.FollowableLink` compares next links with their
  fragment (`requested.Contains(next.AbsoluteUri)`, read by the gate at the head); a proposal for whoever next touches
  the layer, not built here.
- Not built (the coordinator's choice): binding the `drives/{id}` forms to a drive id (Q2 "b"); gate B2061 Info 4 to 9.

## Added by the gates (MEASURED)
- B2061 (round 1, NO GO): FOUND 1 the real-looking test id (Major, closed by round 2); FOUND 2 the README over-claim
  (Minor, closed as a Limits line); FOUND 3 the fragment defeats the loop rule (Minor, closed in code with O12); Info 4 to
  9 (the query taken as written, the fourth form documented by composition, item-rule shapes, ids of dots, no length bound
  of the module's own, the seat's OPEN items).
- B2064 (round 2): FOUND 1 Minor, the round-1 commit 4b9814f1 (holding the replaced literal) stays reachable from the
  branch and, once the pull request is opened, from its pull ref, which outlives the merge (refs/pull/4..49/head all
  present at the gate); main and the squash tree are clean. Info: a next link that differs from a requested address by
  the case of an item id or a query option name, by a percent-escaped `,` or `$` in the query, by an empty `?` or a
  trailing `&` is a different address (RFC 3986) and is requested once more before its exact repeat is caught; a server
  that changes the query on every page reaches the page bound (100 requests, `TooManyPages` at page 101); whether Graph
  treats such variants as one address is UNMEASURED. Info: the README's opening "and nothing else" and the class
  summary's "of the same forms" (`MyDriveBrowser.cs:12`) read narrower than the four forms the code follows (round-1
  text; the Limits line states the behaviour).
- Coupling: after this lane lands, main's push run reads `--total 2221 --rules 671 --unit 117 --floor 117`.
- Local CodeQL is not runnable on this Mac (the C# extractor is x86_64): the pull request's code scanning is the CodeQL
  read.
