## Why

The server must answer the three calls an OXPd 1.x device makes on an authentication agent (HP's committed
description, `contracts/oxpd1/hp/.../authenticationagent.wsdl`): GetPrePromptResult, GetPostPromptResult and
SignOutNotification. This is the first slice of plan lane L1 (the 1.x agent host): the SOAP half only, with no route,
no TLS and no caller check (those are the host's lanes). Every choice in it (a transport-free endpoint in the landed
Agents project with no project file change, hand-written SOAP 1.2 with no package, the answer in the request's
WS-Addressing version, `mustUnderstand` honoured, the fault statuses and fixed texts, the 64 KiB and 64-level bounds,
no Succeeded answer in this slice) is the coordinator's.

## What changed

Two files, both added; no landed line, project file, lock file or package changes.

- `src/Datasec.Suite.Adapters.Oxpd1.Agents/Oxpd1AuthenticationAgent.cs`: `Oxpd1AuthenticationAgentEndpoint.AnswerAsync`
  takes the request body as a stream and its content type, and returns a status, a content type and bytes. It refuses,
  before the handler sees anything: a media type other than `application/soap+xml`; a body over 64 KiB (refused while
  it is read); a body that does not parse with no DTD, no resolver and no element deeper than 64 levels; an envelope
  that is not SOAP 1.2 or whose body does not hold exactly one element; WS-Addressing headers of two versions; a
  message id outside 1 to 256 characters; an unknown header block marked `mustUnderstand`; a body element that is not
  one of the three operations; an action that does not name the body's operation; and any value outside HP's schema
  (a context id of 32 to 128 ASCII letters or digits, a language code `xx-YY`, a server context id of 1 to 256
  characters, in HP's order and nothing else). Only then is the handler (`IOxpd1AuthenticationAgentHandler`, the
  host's) asked, once. Its answer is Continued, Canceled or Failed with an optional failure message, written as HP's
  response element in the request's addressing version (none when the request had none).
- Every refusal is a SOAP 1.2 fault with one of eleven fixed texts: `Sender` 400, `Receiver` and `MustUnderstand` 500.
  A handler that throws (other than a cancellation) or answers nothing is a `Receiver` fault. No fault, no `ToString`
  and no exception message the endpoint makes carries the context id, the server context id or an exception's text; the answer and the
  faults echo only the request's message id, as `RelatesTo`.
- `tests/Datasec.Suite.Adapters.Oxpd1.Agents.Tests/AuthenticationAgentTests.cs`: cells G01 to G09 (43 cases), all in
  memory.

## What proves it

- G01 reads the three operations and their actions back from the committed binding and port type and validates every
  request and answer body the cells use against the committed `authenticationagent.xsd` (with two planted bad bodies
  that must fail). The agent test executable `Total: 44, Failed: 0`; the whole solution 2607 / failed 0 locally and on
  both hosted legs (release guards unchanged: 28 and 29 files).
- Nine mutants of the change each turn their intended cell red (re-run independently: 9 of 9 MATCH). Further runs
  outside the cells: the size bound holds at 65536 / 65537 bytes, the depth bound at 64 / 65 levels, a stream read one
  byte at a time and an endless stream (stopped at 65537 bytes); a DTD, an entity, an external reference, an
  XInclude or a stylesheet reference opens no connection and reaches no handler; two and sixty-four requests at once
  on one endpoint each get their own answer (the endpoint keeps no state between requests); no reply body of any of
  87 shapes holds `Succeeded`.
- Secret scan and word scan clean over the added lines and the message.

## Named limits

1. No answer is `Succeeded`: a device can be told to continue, cancel or fail a sign-in, nothing more. Succeeded with
   the user's information is the next slice.
2. The endpoint checks no caller and binds no route: which device may call, over which transport, is the host's
   (route and TLS, and the 1.x callback credential).
3. The endpoint sets no time bound on the handler. HP recommends short time-outs (1 to 5 seconds) and no retries of the
   two prompt calls (`authentication.xsd`); the host's handler owns the bound. A cancellation thrown by the handler
   passes to the caller as an exception, also when the request itself was not cancelled (for example a time-out of the
   handler's own HTTP call): the host must catch it and answer.
4. A repeated sign-out notification is handed to the handler each time; the handler treats a repeat as done.
5. How a device frames these calls (its content type, addressing version, headers, time-outs, encoding) is not
   measured: every request a cell builds is that cell's assumption from HP's descriptions. A `ReplyTo` or `To` header
   is read for nothing; the answer always goes back on the same exchange. An `Action` with white space around it is
   refused.
6. The reader is stricter or looser than HP's schema in small ways that carry no value outside the schema to the
   handler: a character beyond the Basic Multilingual Plane in a server context id is refused; attributes on the value
   elements and an element after the SOAP body are ignored; a body whose XML declaration names another encoding than
   its bytes is read by the declaration.

## Who decides

The coordinator lands this pull request (squash, pinned to the reviewed head). Nothing ran against a device, a
printer, a tenant, Azure, a Microsoft host or HP. Nothing is deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
