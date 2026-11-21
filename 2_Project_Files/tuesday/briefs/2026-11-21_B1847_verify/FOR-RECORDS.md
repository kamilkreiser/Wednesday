# FOR RECORDS: gate B1847 (WP3.8, the shared Graph layer), round 1, NO GO

These are for a records pass after the lane lands, which comes after its fix round and round-2 gate. Nothing here
was written to the project.

## Runbook (`SETUP_RUNBOOK.md`, check table)

- The solution builds and tests two more projects: `src/Datasec.Suite.Graph` and `tests/Datasec.Suite.Graph.Tests`.
- Local total, measured by this gate:
  - head alone: 894 -> 1070 (+176), skipped 4
  - merged with main `0804860b`: 1075 (899 + 176), skipped 4
- The fix round adds its own new cells: the round-2 gate prints the final figure.

## README (`README.md`, Layout section)

The Layout section lists neither project. It needs two lines: `src/Datasec.Suite.Graph` (the shared Graph HTTP
layer) and `tests/Datasec.Suite.Graph.Tests`. This is Q14: a records lane's or Tuesday's job, after the landing.

## BACKLOG (`BACKLOG.md`): points of the builder's FOR RECORDS and FOR TUESDAY that stay open

1. **The adapter from lane D's broker to `IGraphTokenSource`** (who writes it, where it lives). This is the kit's
   NOT DECIDED item 1. Broker failures all fold into `Unauthorized` (NOT DECIDED item 2).
2. **The token is a .NET string.** It cannot be wiped (the builder's FOR TUESDAY 1; this gate's R4: a design point).
3. **The token source has no time bound inside the layer** (R2). The adapter should bound the broker call. Report
   A11 line 95 says the Workpath app waits at most 10 s (RELAYED).
4. **Host wiring for the Graph `HttpClient`** (R3): automatic redirects off, and no default `Authorization`. Whether
   .NET strips `Authorization` on a cross-host redirect is UNMEASURED.
5. **The readings 3(a) to 3(l)** of the builder's DEVIATIONS: the gate accepted each. Two are watch points:
   - (i): a non-string deltaLink is returned as null.
   - (l): `MaxThrottleRetries` and `MaxNextLinkLength` have no upper limit (R1). The gate measured 20,001 sends at
     `MaxThrottleRetries = 20000`.
6. **The named limits of N11**: how Graph really shapes `Retry-After`, next links and upload ranges; redirects;
   decompressed bytes; no coalescing of refreshes; generated frames hold a token for one call. Beyond those: an
   exception from the caller's content factory, delay or stream passes through; a transport failure's cause is not
   attached.
7. **A tenant test is needed.** Every Graph behaviour in the tests is assumed. Exit test E3.3 is NOT proved by this
   lane, and `OXPD2-16` stays open.
8. **An upload total-wait cell** (R5).

## For the fix round, from this gate (not records; for Tuesday's fix-round kit)

- **F1 (Major).** Malformed text inside a network JSON string escapes as `InvalidOperationException`, with a body
  byte value in its inner text. The places are `GraphClient.cs:696` (nextLink), `:699` (deltaLink) and `:352`
  (`nextExpectedRanges`). The fix shape and the cells are in `VERDICT.md`.
- **F2 (Minor, text).** Two comments state Graph behaviour with no source: `GraphClient.cs` `UploadAsync`
  "pre-authorised", and `GraphCloud.cs` `Gcc`.
- **Optional.** Cap `MaxThrottleRetries` like `MaxPieceRetries` (R1).
- **Main has moved to `0804860b`.** The head merges with it cleanly, and `Datasec.Suite.slnx` was not touched on
  main's side. A fix commit on the branch, or a rebase before its first push, needs no conflict work today. The
  round-2 gate re-measures it against whatever main then is.

## Process

- The builder's deviation 1: one `sed -i` on its own lane scratch file (R6).
- This gate made every git write verb in session-scratchpad clones, because the workspace hook refuses them in
  `/private/tmp/b1847-gate`. That folder held the read clone, the tools, the logs, the moved lock folders and the
  probe.
