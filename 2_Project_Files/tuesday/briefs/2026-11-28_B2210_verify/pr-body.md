## Why

The agent host needs a public way to make six OXPd 1.x context calls (the sign-in reserve and release, and the open,
start reading, stop reading and close of an HID accessory). The client's senders are internal and its public surface is
closed lists of reads, so this adds one new public class in the OXPd 1.x module that sends them through the client's
own guest sender, with no second client and no change to a landed line.

## What changed (two new files, nothing else)

- `src/Datasec.Suite.Adapters.Oxpd1/Oxpd1Context.cs`: `Oxpd1ContextKind` (six members, a closed list), an internal
  catalogue whose rows are the committed bindings' services, namespaces, operations and actions, the call record
  `Oxpd1ContextCall` (one factory per kind, every argument checked when the call is made, `Execute` false by default),
  the result `Oxpd1ContextResult` and `Oxpd1ContextCaller.CallAsync`.
- `tests/Datasec.Suite.Adapters.Oxpd1.Tests/ContextTests.cs`: cells N01 to N10, 39 cases, against the stub device on
  127.0.0.1.

## The choices (each the coordinator's)

- The guest user for all six, through the client's internal guest sender (the least credential the service
  descriptions admit: "either guest or device administrator credentials").
- Each call a dry run unless `Execute` is set; each result that may have taken effect (answered, or unknown) carries its
  undo as a dry run: a reserve the release of the id it returned, an open its close, a start of reading its stop. A
  refused call (no setting, refused pin, 401, 403) carries none.
- A reserve is answered only by one text-only result whose text is HP's `common:Nonce` (32 to 128 ASCII letters or
  digits); anything else is a malformed answer with no id and no undo.
- The callback binding of a start of reading is `Soap12`, as the echo calls write it.
- No README change in this commit.

## What proves it

- N01 reads each row back from the committed bindings and validates each request body against the committed schemas
  (with a planted control the schema refuses).
- N02 to N10: dry runs send nothing and read no setting; the guest header on every executed call; the reserve's answer
  shapes; the undo on every end; refused arguments; no id or credential in any text.
- Eight mutants of the new class each turn their cells red; the whole solution and both hosted legs are green.

## Named limits

- How a printer answers any of the six, and whether it accepts the guest user for them, is not measured: every stub
  answer is the cell's assumption.
- The client's record file holds each envelope as sent, so it holds the context ids and the agent id; a scrub needs a
  change in `Oxpd1Client.cs`.
- A reserve whose end is unknown (time-out, fault, malformed answer) carries no undo: no id was read.
- An undo sent for a call that did not take effect ends in the service's `IllegalOperation` fault (by its description);
  no cell sends it to a device.
- The guest request carries the client's password setting as its password (the client's guest sender, unchanged
  here); the service descriptions' guest password is free.
- When the client's mask changes a reserve's returned id (the setting's value inside the id), `CallAsync` throws after
  the request was sent, with no result and no undo.
- A fault code is passed on as the client scrubs it (the password only).
- Where an accessory context id comes from, the report events and any call beyond the six are not in this change.

Nothing here ran against a printer, a device, a tenant, a Microsoft host or HP. Nothing is deployed.
