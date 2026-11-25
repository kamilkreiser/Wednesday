# FOR RECORDS: lane L1 round 1 of 2 of the MPS Commercial Calculator (kit B2106, seat M176), MPSCALC-233, 316 and 120, head b740f548 (gate B2107: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator. The product
owner's words are only the rulings the kit quotes: C-119 (233, his 2026-11-11 acceptance of option (a) Refuse: "Refuse.
Two quotes with one reference break the audit trail."), C-64 and C-108 (316: the agreed unit sentence; whether C-108
reaches the two schema places is "not ruled" by the 2026-11-20 note, comment 41400), C-125 (120: "Yes. It is already
the practice and is written down."). All RELAYED from the kit's THE AUTHORITY; the gate did not re-read
CLARIFICATIONS.md.

## The acceptance clauses (the gate's reading at b740f548; line pointers printed by grep -n at the head)

### MPSCALC-233 ("Duplicate returns a draft whose quoteRef differs from the source; a given reference that clashes is refused or made unique by a stated rule; the new quote names its source; the source quote and its versions are unchanged; contract regenerated.")
1. **quoteRef differs from the source: MET for a typed reference and for most derived ones, NOT MET for one derived
   shape (gate finding F1).** A typed reference equal to the source's own is refused (cell N2). A derived reference is
   the source's plus `-COPY`, EXCEPT when the source's reference is 96 to 100 UTF-16 units and is itself a derived
   copy's (or is any 100-unit reference ending `-COPY`): `CopyRef` (`QuoteEndpoints.cs:592-609`, unchanged by this
   lane) cuts the source to 95 units and adds `-COPY`, which gives back exactly the source's reference. MEASURED by the
   gate's probe cells GP1 (a 100-unit source ending `-COPY`: the copy's reference equals it) and GP1b (a source of 100
   `B`: the clone of its clone holds its source's reference), both hosts. Reachable from the web Clone button (it
   sends no reference). Pre-existing, not a regression; the seat's STATUS read clause 1 MET with only the
   no-reference edge. The docs sentence "A copy never shares its source's reference" (`docs/API.md:444`,
   `docs/api/openapi.json:369`, kept by this lane) is false for that shape. A source with no reference gives a copy
   with none (the seat's edge; unchanged).
2. **A given reference that clashes is refused: MET for a reference the caller types** (cells N1, N3, N4; code
   `QuoteStore.cs:138` `AddIfRefFree`, `QuoteEndpoints.cs:563`; stated at `docs/API.md:444`, `openapi.json:369` and
   `:1036`). By the coordinator's Q5 a DERIVED reference is not refused, so two quotes can still hold one reference by
   cloning one source twice (the cell `V0_two_clones_of_one_quote_may_share_the_derived_reference`), by a derived
   reference after a typed one (gate probe GP2: typed `Q-SYN-1-COPY` on another source, then a derived clone of
   `Q-SYN-1`: two holders), by create and by an edit of a draft (gate probe GP3; the kit's FACT 7(b)). Read as MET on
   the coordinator's reading of "a given reference"; the derived case is a records line.
3. **The new quote names its source: MET, untouched** (the `duplicated-from` event; the existing cells).
4. **The source quote and its versions are unchanged: MET** (N1: no `duplicated-to` event on the source after a
   refusal, and the held quote keeps its reference; the existing cell
   `V0_the_source_quote_keeps_its_revision_and_reference_and_names_the_copy`).
5. **Contract regenerated: MET** (commit 2; the gate re-ran `sync-contract.mjs f8644cce...` and got the three committed
   blobs byte for byte; `contract.sync.test.ts` and `contract.test.ts` `Tests  4 passed (4)`).

### MPSCALC-316 ("either the contract text in both places names the unit ... or the rule counts text elements")
- **MET on the coordinator's reading of C-108 (Q11), OPEN for the product owner's reading.** `openapi.json:988`
  (`QuoteDraft.quoteRef`) carries "At most 100 UTF-16 code units (an emoji counts as two)." and `:1036`
  (`DuplicateRequest.quoteRef`) starts its description with the same sentence; `maxLength` stays 100 (8 places at
  base and head). The ticket keeps `needs-ruling`: the records note says whether C-108 reaches the schema places is not
  ruled. The ticket stays open until the product owner says so.

### MPSCALC-120 (fix shape: "it gets its own short section in docs/API.md and later seats cite that")
- **MET.** `docs/API.md:8` `## Contract version (...; MPSCALC-120)`: the rule and the nine version values. The gate
  MEASURED the list: `git log` of `docs/api/openapi.json` at 56f508a7, 36 commits, `info.version` by JSON parse: 2 x
  `0.1.0-lane2b`, 1 `0.2.0-b12`, 10 `0.3.0-b17`, 1 each `0.4.0-b80`, `0.5.0-b85`, `0.6.0-b83`, `0.7.0-b94`,
  `0.8.0-b103`, 18 `0.9.0-b103` (equal to the kit's Reading 7). **Gate finding F2 (Minor):** the section states the
  rule and is silent that the contract changed 17 times after `0.9.0-b103` with no bump, this change among them (a new
  refusal of a public operation, described in the contract; Q8 no bump), while `docs/API.md:153` records an earlier
  bump (`0.7.0-b94`) with "no new member". A later seat citing the section will find it not followed: the records
  should say which changes the rule covers (the coordinator's, or a words question to the product owner).

## Owed lines (the kit's FACT 7, confirmed by the gate where marked; none edited by this lane)
- (a) The dev stub's clone does not refuse a repeated typed reference: `web/src/api/stub/purchaseQuotes.ts:281`
  `holdCopy`, its comment at `:273`; the stub also trims a typed reference and the server does not (C-168, RELAYED).
- (b) `POST /api/v1/quotes` and `PATCH .../draft` still store a `quoteRef` another quote holds (CONFIRMED by the gate's
  probe GP3, both hosts); a derived clone may equal a typed one (GP2); a restart loads every persisted quote as it is,
  clashes included (`QuoteStore.cs:108-111`, by reading). Whether create or an edit must refuse is the product owner's.
- (c) MPSCALC-195: the accepted engine-target sentence is on no record the drafter or the seat could read, and the
  sweep's pointer (`Briefs/2026-10-16_B158_STATUS.md:233`) is the rate-limit row B158-9 (re-printed by the seat). It
  stays open; asking the product owner for its words is the coordinator's to card.
- (d) `web/src/api/generated/SOURCE.txt` names commit f8644cce..., which a squash does not keep on main (BACKLOG row
  `[B1703-OWED-4]` already owes that resync).
- (e) The two sibling length sentences still say "characters": `QuoteEndpoints.cs:1450` and `:1454` at base, `:1458`
  and `:1462` at the head (the 200-character fields and the notes field).
- (f) NEW from the gate: the derived `-COPY` cut can return the source's own reference (F1 above); the fix is a
  rule for that case (for example, a counter or a refusal), which is a product choice: a records line, not this lane.
- (g) NEW from the gate: `DuplicateRequest.quoteRef`'s description (`openapi.json:1036`) says "A reference that another
  quote already holds is refused" without "current version" and "the same UTF-16 code units", which the operation's
  description (`:369`) and `docs/API.md:444` carry (Info).

## Seat process slips the seat disclosed (RESIDUE of its STATUS; none touched a project file or the pushed branch)
One `sed -i` on its own scratch file (the holds forbid it); one `rm -rf /dev/null` line (a delete command against the
never-delete rule; the device intact); one `git -c user.name/user.email` commit in a throwaway control clone (never
pushed; the identity rule forbids the form). The two pushed commits carry the repo's configured address as author and
committer (re-read by the gate through the compare API).

## What a records seat writes (proposals, the coordinator decides)
- MPSCALC-233: a comment with the five clauses as above (clause 1 NOT MET for the long derived shape; clause 2 MET for
  typed references), the squash sha, and the owed lines (a), (b), (f); move it only as the coordinator rules.
- MPSCALC-316: a comment that the two schema places carry the agreed sentence on the coordinator's reading of C-108;
  the ticket stays open with `needs-ruling` for the product owner.
- MPSCALC-120: a comment naming the section and F2's question.
- MPSCALC-195: unchanged; its words are still owed.
- Nothing deploys with this landing; an MPS hosted deploy is a card of the product owner's.
