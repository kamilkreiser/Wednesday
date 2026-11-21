## What this adds

Two commits on one branch: a new library `src/Datasec.Suite.Graph` (the one shared HTTP layer every Graph call of the
app modules is to go through, work package WP3.8), its test project `tests/Datasec.Suite.Graph.Tests` (197 tests), and
two lines of `Datasec.Suite.slnx`. The first commit adds the layer. The second makes a string or a property name of a
page or an upload answer that the JSON reader cannot turn into text end as the layer's own `MalformedResponse`, adds
21 test rows for it, widens the random-conversation test so that it can reach such text, and gives two code comments
their source. No package, no workflow line, no build file and no other project changes. The squash lands both as one
commit.

## What the layer does

- **Sends only through the caller's `HttpClient`.** It never sets its base address and never disposes it. Time is
  read only through the given `TimeProvider`, and every wait goes through the given `IGraphDelay`.
- **Holds no token.** A token source (`IGraphTokenSource`) is passed into each call and lives only for that call. No
  field of the library holds a token, a token source, an upload address or a response body.
- **One token per call, at most one refresh.** A 401 asks the source for one new token and retries once; a second 401
  is `Unauthorized`, never a loop.
- **Bounded retries and waits.** 429 and 503 are retried at most `MaxThrottleRetries` times (default 3). A
  `Retry-After` over `MaxRetryAfter` (default 30 s) is not waited, and all waits of a call stay within `MaxTotalWait`
  (default 60 s). Without the header the wait starts at 1 s and doubles up to 15 s. Each attempt has a time-out
  (default 100 s), and the caller's cancellation is honoured at every wait.
- **The token goes only to the base origin.** `Authorization` is sent only to the configured base address's scheme,
  host and port. An address on another origin is refused before any request.
- **Paging.** `@odata.nextLink` is followed only when it is an absolute https address on the base host and port with
  no user info and at most 8192 characters. A loop, a foreign link and more than the page bound (default 100) each end
  the walk with a failure. `@odata.deltaLink` is returned, never followed.
- **Chunked upload sessions.** Pieces (a multiple of 320 KiB, default 10 MiB) go by PUT with exact `Content-Range`
  and NO `Authorization` header. A 202 names the next start; a retry reads the session's status first and resumes
  from the range it names. Piece retries and the request count are bounded, and the same start named again and again
  ends as `UploadNoProgress`.
- **Bounded reads.** A body is read up to `MaxResponseBytes` (default 4 MiB) and no further; the body of a status that
  is not a success is not read.
- **One closed list of failures.** Every failure is a `GraphCallException` with one of 12 kinds (`Unauthorized`,
  `Throttled`, `HttpStatus`, `PagingLoop`, `PagingForeignAddress`, `PagingTooManyPages`, `MalformedResponse`,
  `ResponseTooLarge`, `Timeout`, `Transport`, `UploadSessionGone`, `UploadNoProgress`), with no inner exception.
  Beside it, only an argument error, the caller's own cancellation, and an exception thrown by the caller's own
  content factory, delay or stream leave a call.
- **Logging without secrets.** One event per attempt and one per outcome, with only the method, host, status,
  attempt, wait and outcome: never a path, a query, a header value, a body byte or a token.

## What the second commit fixes

A JSON string that is not valid UTF-8, holds an overlong form, or holds an unpaired surrogate escape (for example
`\ud800`) is accepted by the JSON parser, but turning it into text throws `InvalidOperationException`. Before the fix
that exception left the library from seven reads: the next link, the delta link and an upload range as values, and
four property-name lookups (`value`, `@odata.nextLink`, `@odata.deltaLink`, `nextExpectedRanges`) whose answer holds
an escaped name the reader has to decode to compare. Its inner text could also print a body byte. Now two guarded
regions catch exactly `InvalidOperationException` and nothing wider: the page reader ends as `MalformedResponse`, and
the upload range reader returns no start, which the caller already turns into `MalformedResponse`. Neither attaches
an inner exception, so no body byte reaches a text. An unreadable delta link is `MalformedResponse`; a delta link that
is not a string is still returned as absent.

## What it does NOT prove

- **Every Graph behaviour in the tests is assumed.** How Microsoft Graph really shapes `Retry-After`, next links,
  delta links and upload ranges is not measured here; every answer in the tests is synthetic, from a fake handler. A
  test against a real tenant is needed.
- **Exit test E3.3 is not proved** by this change, and its ticket `OXPD2-16` stays open.
- **The adapter over the token broker is later work.** Nothing here obtains a token or calls the session and token
  broker; the adapter from the broker to `IGraphTokenSource` (and a time bound on the broker call) is a later change.
- **The host does not use the layer yet.** The server does not reference the library.
- **Limits that stay.** An item of `value` holding text the reader cannot decode is returned as it is; a module that
  turns that item into text meets the same refusal from .NET. Redirects and the caller's default request headers
  are the host's: the Graph `HttpClient` should be built with automatic redirects off and no default
  `Authorization`. The token is a .NET string and cannot be wiped. `MaxThrottleRetries` and `MaxNextLinkLength` have
  no upper limit of their own; only the caller sets them.

Nothing is deployed; nothing was sent.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
