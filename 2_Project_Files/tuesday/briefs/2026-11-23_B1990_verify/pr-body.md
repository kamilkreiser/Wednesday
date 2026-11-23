New library `Datasec.Suite.Adapters.Oxpd1` (plan work package WP0.4, the OXPd 1.x stubs) and its test project. Head
`85e414d6` on `b1976/x1-oxpd1-read-client`: the first commit `1fca08cf` (the library, its tests and HP's 14 service
descriptions), one merge of main `cad65b86`, and two fix commits (`8f5813bf`, then `85e414d6`, which fixes the three
code-scanning alerts this pull request raised). Against main: 31 files, 30 added under `contracts/oxpd1/`,
`src/Datasec.Suite.Adapters.Oxpd1/` and `tests/Datasec.Suite.Adapters.Oxpd1.Tests/`, and two added lines in
`Datasec.Suite.slnx`. No other file changes, and no package is added. The landing is one squash; the merge commit does
not reach main.

## Why

- The printer to support first is an HP Color LaserJet MFP M577, an OXPd 1.x (FutureSmart 5) device. Nothing in the
  repository could read an OXPd 1.x device. This client reads what the pre-install checks need, and writes nothing.

## What changed

- `Oxpd1Client`: `GetDiscoveryTreeAsync` (a GET of `/DevMgmt/DiscoveryTree.xml`, no credentials, the answer checked to
  be well-formed and returned masked, never interpreted) and `ReadAsync(Oxpd1Read)` over a closed enum of five SOAP 1.2
  reads, each to `https://<host>:7627/hp/device/webservices/OXPd/<service>` with the binding's `soapAction` and
  WS-Addressing 1.0 `Action`, `To`, `MessageID` and `ReplyTo` headers (`mustUnderstand="1"` on `Action` and `To`).
- Pinned TLS: a certificate is accepted only when the SHA-256 of its DER bytes is a pin, on every handshake; no
  redirect, no proxy, HTTP/1.1 only; no plain-HTTP and no accept-any setting.
- Answers: read strictly (no DTD, no external resolution), bounded in bytes (`MaxAnswerBytes`) and in depth (an element
  deeper than 64 is refused while the answer is read, before any tree is built; the masking copy is bounded too).
- The admin password: read from a named setting at each call; names on the deny-list are masked; the password and its
  Basic form are scrubbed from attribute values and from the joined text of each run of text and CDATA nodes, and a
  scrubbed value reads `[removed:password]` (the deny-list's own text, held by the library as a read-only field); a
  masked answer that still holds either ends the call `MalformedAnswer`, and namespace names and attribute values (a
  namespace declaration's included) are compared as they are, unescaped; the fault code is scrubbed before it is cut
  to 256 characters.
- The record: written through `SuiteLoggerFactory` (behind the deny-list); it holds the read, the URL, the outcome, the
  status, the scrubbed request and the masked answer, and names no setting.
- `Timeout` bounds the connection, the request and the body read, and is refused by the options unless it is positive,
  finite and at most five minutes (`MaxTimeout`). The parse and mask after the body are bounded by `MaxAnswerBytes` and
  the depth bound, not by `Timeout` (the library README says so).
- Every call ends in one `Oxpd1Outcome` (11 values).
- `contracts/oxpd1/`: HP's 14 service descriptions from the SDK 1.8.4.1 jar's `META-INF/wsdls/`, byte for byte, with
  `inputs.sha256`; `.gitattributes` keeps their bytes. The library reads none of them at run time.
- Tests: 23 cells against a stub device on 127.0.0.1 (Kestrel, a certificate made in the test) whose routes, actions
  and addressing namespace are read from the committed bindings; every password and record in them is synthetic.
- `Datasec.Suite.slnx`: the two projects, so the hosted legs build and run the 23 cells.

## What proves it

- Red first (macOS arm64): over the first commit, 21 cells, 10 failed, each by an assertion, then 21 / 0; over
  `8f5813bf`, the two new cells (a password holding `&`, `<`, `"`, a tab or a line feed echoed in a namespace, 45 rows;
  the record's shape and the scrub text), 23 cells, 2 failed, each by an assertion, then 23 / 0. 31 mutants, each red on
  exactly its cells (one named survivor: a second XML layer no cell can redden alone).
- Deep answers (5,000 levels in a result and in the tree, 60,000 in a fault code, up to 140,000) each end
  `MalformedAnswer` and the process lives.
- Whole solution at the head: 1927 / 0 / 1923 / 4, rules 617 files; with main `df762b28`: 1942 / 0 / 1938 / 4, rules
  628 files. The head's push run and this pull request's run pass on both legs (1927 and 1942 each).
- Code scanning on this pull request: the csharp analysis of `85e414d6` reads 0 results, and the three
  `cs/cleartext-storage-of-sensitive-information` alerts raised at `8f5813bf` (the setting's name in the record, and
  the scrub text as the output of a call keyed on "password") read fixed; none was dismissed.

## Still open

- Not run against a device. Whether a FutureSmart 5 device accepts WS-Addressing 1.0 headers marked `mustUnderstand`,
  and whether the endpoint path holds for the three services whose specifications do not state it, are not measured.
- The parse and mask after the body are not under the time-out: an answer of about 0.9 MB with 90,000 attributes on
  one element took about 7 s to return with a 1 s time-out. The README now says what the time-out bounds; a cap on
  attributes per element, or the time-out inside the masking copy, is owed if a device can send such an answer.
- The reverse-engineering clause of HP's terms is not settled; the client is built from the published descriptions only.

## Who decides

The coordinator chose, as coordinator, this lane and every choice inside it (one library on the logging library only,
the endpoint and action from the bindings, WS-Addressing 1.0, the depth bound of 64, the five-minute time-out cap, the
pin rule duplicated, the descriptions by copy, the record without the setting's name, the scrub text as a read-only
field) and the landing order. The fix of the code-scanning alerts was opened by the product owner's answer to a card
("fix round now"); no choice inside this change is the product owner's.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
