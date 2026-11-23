# B1998 FOR RECORDS (gate G1, round 1 of 2 of lane FK; kit B1993, seat X54; head 81ae47ed)

Who decided: every choice of lane FK (D0 to D5, Q1 to Q7: F1 to F3 not rebuilt, F6 said and pinned with no runtime
change, K8's two counts exact) is the coordinator's (Tuesday's) as coordinator; none is the product owner's. The
strict reading K8 protects is C-63 ("Keep both strict for now"), unchanged by this lane. Nothing here is a
customer-facing word.

## From the kit (RELAYED, kit B1993 FOR RECORDS; the gate re-measured each where marked)
- Item 36 F1, F2 and F3 were closed by pull request 7 (merge `0804860b`, 2026-11-21); `BACKLOG.md` names pull request 7
  nowhere, so item 36's three lines are owed a tick with that pull request (a records pass). Gate: `0804860b` is an
  ancestor of `d804de5e` (rc 0); its subject names all three; at `d804de5e` `Oxpd2Schema.Properties` / `EnumValues`
  and `Oxpd2InboundCatalogue.Operations` are `Array.AsReadOnly` views (`Oxpd2Schema.cs:86`, `:119`, `:193`;
  `Oxpd2InboundCatalogue.cs:10`), `HighestMaxBodyBytes = Array.MaxLength - 1` with the constructor bound
  (`Oxpd2ParseLimits.cs:19`, `:24`), their cells (`ReadOnlyListTests.cs:130`, `:148`, `:156`; `LimitTests.cs:32`,
  `:46`) and the astral N9 rows (`InboundTests.cs:248` to `:255`). BACKLOG.md sha256 `7589759f...` equal to the
  kit's: item 36 still unticked.
- Item 36 F6 is closed by this commit: each generated client's summary says what passes out of its methods, and three
  cells pin it; F6's N11 half was already written in N11's summary on `main` (`ClientTests.cs:285` to `:289`).
- Item 67's pull-request-20 part is closed by this commit: K8 covers every optional root property, 716 models and 2117
  properties pinned. Gate: an independent count from the committed generated text (two ways: the `Fill` blocks of the
  16 client `Oxpd2Schemas.cs`, and the `(required)` marks of the 16 `Models.cs`) gives 716 and 2117 at the head and at
  `d804de5e`.
- Named limits: a nested optional property (H12); the real network's `HttpIOException` (H4, now MEASURED, below); a
  1xx/3xx beyond the three statuses and a 2xx body (H9, H10); the open-stream mutant is equivalent (H19).
- Runbook candidate: `hosted3.py` needs `--guard-linux 14 --guard-windows 15` since the host composition landed (its
  defaults 10 and 11 FAIL on `main`).
- Carried, not in this lane: item 36's F4, F5, F7 and D11 (records and the logging lane); alternatives (b) and (c) of
  D1.

## Deviations of the seat (RELAYED, seat STATUS; the gate agrees with each)
- DEVIATIONS 1: `ObjectNode` is at `Oxpd2Json.cs:399`, not `:398` (a pointer only).
- DEVIATIONS 2: the mutants run and the hosted wait ran in the background of the shell tool, each one unchanged call.
- DEVIATIONS 3 (H5): no generated client calls `SendRawAsync` (gate: 201 public methods in the 16 clients, 201 calls of
  `SendForJsonAsync`, 0 of `SendRawAsync`); the named limit has no member today.

## The gate's own, for the records seat (owed items; none filed by the gate)
1. FOUND 1 (Minor): the new summary sentence is true on every path of `Oxpd2ClientCore` but is not the whole list a
   caller meets. MEASURED on 127.0.0.1 with a real `SocketsHttpHandler` (.NET 10.0.404, macOS arm64, gate probe, never
   committed): (a) a body that ends early passes out as `System.Net.Http.HttpIOException` (an `IOException`; content
   length and chunked); (b) with a caller's handler that decompresses, a corrupt gzip body passes out as
   `System.IO.InvalidDataException` (neither type the sentence names); (c) `HttpClient.Timeout` during the send passes
   out as `TaskCanceledException` (inner `TimeoutException`); (d) `HttpClient.Timeout` does NOT bound the body read:
   headers then silence ended only at the caller's token (2916 ms, `TaskCanceledException`, inner `IOException`);
   (e) "never reads the body of a non-success answer" holds for the client's code, but the platform handler drains an
   unread 404 body to reuse the connection (two 404 answers with 1000-byte bodies: 2 requests on 1 connection).
   Nothing in (a) to (e) is parsed, handed back or turned into a refusal. Owed: one sentence in the adapter README or
   the next generator pass ("also a cancellation, and whatever the caller's handlers throw; the platform may drain a
   non-success body it does not hand to the client"), and a records line that the body read is bounded by the
   caller's token only.
2. Named limit, new (MEASURED): H4 holds on this platform: `HttpIOException` is the type a real socket's early end
   raises, and it passes out as the `IOException` the cells pin. Linux and Windows UNMEASURED.
3. For the L4 gate (not this lane's): L4's branch `26f4b57a` changes 13 files, among them
   `src/Datasec.Suite.Lab/Device/DeviceChannel.cs`, `Datasec.Suite.Lab.csproj`, its lock file, the Lab README and
   `tests/Datasec.Suite.Lab.Tests/ProbeTests.cs` beside the Print folder and the registration line (a fact for that
   gate to weigh against its kit; FK shares none of them).
