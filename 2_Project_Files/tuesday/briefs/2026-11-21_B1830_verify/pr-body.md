## What this adds

One commit, three parts, and a test project (`tests/Datasec.Suite.Contracts.Tests`, 132 tests).

- **The inputs.** `contracts/oxpd2/hp` holds 37 of HP's OXPd 2 Beta 10 specification files, byte for byte: the 16
  service bundles, the five service-target specifications (the calls a printer makes INTO the server) and the 16 type
  files those five reach. `contracts/oxpd2/inputs.sha256` names each file with its SHA-256. Tests recompute every
  fingerprint, check that the folder holds exactly the listed files, and resolve every reference between the files
  (3819 inside the bundles, 365 internal and 146 external in the targets and types, 0 unresolved).
- **The generator and its output.** A generator written in C# with the base class library only
  (`contracts/oxpd2/generator`) writes `src/Datasec.Suite.Adapters.Oxpd2/Generated` (85 files, about 3.8 MB): 16
  clients with 201 methods, models for the 10 JSON operations of the five service targets, and one bounded parser. A
  test runs the generator in the test process and compares its output with the committed folder byte for byte and as
  a set, on both build legs. No description text of HP's is emitted.
- **The gateway stub**, in the test project only (below).

## The parser of network input

Every body a printer sends to a service target, and every JSON answer of a device to a client, goes through one
parser. Every body ends in a value or a refusal; a refusal names a kind and a JSON path made of schema names and
indexes only, never a byte of the body.

- The size check (1 MiB by default) runs on the length of the bytes before any JSON is read.
- Nesting is bounded (32 by default); a deeper body is refused, and an unknown value is skipped without recursion.
- Duplicate keys (also inside ignored values), comments, trailing commas, a byte-order mark, invalid UTF-8, a broken
  escape and a second value after the first are refused.
- Types, required properties, enum values, integer bounds, string lengths, item counts and property counts are
  checked against the schema. Unknown properties are ignored.

Stated limits: patterns and formats are not checked; **an enum value the inputs do not list is refused, so a value a
newer firmware adds is refused until the inputs are regenerated**; a JSON null for an optional property is refused;
where HP's schema allows "an object or anything" only the object is accepted; multipart and other non-JSON bodies are
not parsed; the bound on the request stream is the host's.

## The clients

Each client takes the caller's `HttpClient` (address, handlers and time-out are the caller's) and carries no token, no
`Authorization` header, no retry and no refresh. Path and query values are escaped; an empty or dot path value is
refused. Bodies of non-success answers are not parsed (the status is kept); a transport fault from the caller's
handler passes through unchanged.

## The gateway stub

A test helper that listens on 127.0.0.1, port 0, inside the test process, and serves the three routes of the customer
gateway (`GET /api/healthcheck`, `POST /api/negotiate`, `POST /api/send`) in front of the hub `printerhub`, so the QR
sign-in client can be unit-tested later without a tenant. It records an `Authorization` header and checks none; what
the real gateway answers to a body with no realm is not known, and the stub answers 500. Every payload, token and
address in the tests is synthetic.

## What this does not prove

- Nothing here talks to a printer, a simulator or a tenant. Every payload is synthetic, shaped by HP's schema; how a
  printer fills any field is not known from this change.
- Contract tests against simulator responses still wait for hardware; the work package's ticket stays open.
- The server does not reference the adapter. Token handling and the callback credential check are later work.

## HP's files and the repository's own rule

Keeping these 37 specification files in this private repository was agreed by the project's owner; nothing else of
the supplied files is copied, and nothing of HP's leaves the repository. The repository's rule check that refuses
copies of supplied files is not changed here: run locally with the supplied folder, it reports exactly these 37 files
and nothing else; the hosted rule job has no supplied folder and is clean. Owed as follow-ups: teach that check to
exempt exactly the files the fingerprint list names; amend the project's written rule on supplied files; add the two
new projects to the README layout.

No package, workflow or build line changes; the solution file gains two lines in the ordinal order of their paths.
Every choice about the inputs, the generator, the parser limits, the clients and the stub was made inside the build,
not by the owner. Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
