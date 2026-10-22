# HPSM-POC telemetry (HPSMPOC-224): a smaller, safer design

*Design note for the product owner, 2026-10-22. Nothing gets built from this note unless you choose to build it. [M] = measured, with the source. [U] = unmeasured.*

## BLUF
- **Why four rounds failed.** The branch switched on the full Azure Monitor recorder, which records everything automatically, and then tried to clean the records afterwards. Each round, the reviewer found another field where a value set while the app runs got through: exception type names in round 2, event names and log categories in round 3, then late writes and outgoing-call names in round 4. [M: B436, B447 and B471 FINDINGS; B471 STATUS :17, :605]
- **One root cause.** The branch keeps a list of allowed field *names*, but it trusts whatever *values* sit in them, and it builds record names from those values. [M: `TelemetryScrub.cs:58-70`, `:102-107`; `scrub.ts:31-34`, `:156`]
- **Recommendation.** Turn the automatic recording off. Each app writes one small record of its own, and every field in it is a number or a value from a fixed list in the code. Anything else cannot be sent, because no field exists to hold it.

## The smaller design
- **What gets recorded.** Each app sends three fixed events and nothing else: `request`, `error` and `call`.
- **What each event holds:**
  - the route *template* (`/customers/{id}`, never the real path), checked against the app's own route table, else `unmatched`
  - the HTTP method, checked against the fixed list of methods, else `OTHER`
  - the status code, the duration in milliseconds, and an outcome from a fixed list
  - a reference id that the server generates itself
  - for `call`, the target is a name from a fixed list in the code (`api`, `sql`, `agent`), never a host or URL from a tag
- **Never sent:** free text, log messages, exception messages or type names, or any value taken from a request, a customer, the model or a library.
- **Timing.** The record is built once, as a new read-only object, when the response finishes. The app's other telemetry objects (OpenTelemetry spans) are never read, so nothing written to them later can reach the record.
- **What the POC still gets.** This is what the ticket asked for: when a reviewer hits an error, there is a record of which route, when, which status, how long it took, and a reference id. It also gets request volume per route, and status and duration for each call from the web to the API. [M: HPSMPOC-224's description, "reviewer errors (HPSMPOC-221) leave no trace"]
  - Showing the reference id on the error page is optional. [U: not checked whether the page has space for it]
- **What it gives up compared with the branch:**
  - exception type and stack depth
  - every log line
  - SQL and Azure SDK call rows
  - the automatic end-to-end trace map, and Live Metrics
  - the first word of a path that matched no route
- **Size.** The branch is 43 files, about 5,067 lines added, over 29 commits. [M: `git diff --stat a93b926a...4c02e8b9`, `git log`] I estimate the new design at a few hundred lines. [U]

## How one gate round would prove it
1. **Field-type test.** Reflection or type checks show the record has no field of free-text type; every text field must come from a fixed list in the code. This closes the "names built at run time" class: B471-2, B471-3, and the earlier B436-2 and B447-1/-3 [M: finding headings].
2. **Late-write test.** This is B471's own probe: a background task touches the current span after the response has gone. The captured payload must be byte-identical to a run without that probe. Closes **B471-1**, and with it B447-1, B447-2 and the API half of B436-7. [M: B471 STATUS :120-121, :115]
3. **Odd method and tag test.** Send a `fetch` with a made-up method from the web, plus API spans that carry a method tag or a `db.system` tag. No record may appear outside the three fixed events. Closes **B471-2** and **B471-3**.
4. **No-recorder test.** The app's telemetry setup must list exactly one source, its own, and zero automatic recorders. This closes the "a library adds a span" class. [U: whether Next.js records anything without a recorder registered; this test would measure it]
5. **Exact-payload test.** Re-run B471's canary set, about 231 made-up values [M: B471 :1]. Compare every captured payload against the closed set of allowed values, not by searching for the made-up values. Include a "stock" control run that does send them.
6. **README test.** The README's list of fields must match the record's own definition. Closes **B471-4**.
7. **Mutation test.** Swap one fixed-list check for a starts-with check; a committed test must fail. Closes **B471-5**'s gap.

## Keep and discard
- **Keep (these passed their gates):**
  - the start-up guard: pre-check, containment and one warning. Every form started across a 303-case and a 560-case run. [M: B471 :297-309; B431-3, B436-3 and B447-9 closed]
  - the outbound calls switched off: Statsbeat, SDK stats and resource detectors [M: B431-4 and B431-9 closed]
  - Entra sign-in for sending, the start-up test corpus, the capture transport and canary harness, and the deploy-package exemption [M: CHECK 3 15/15]
- **Discard:**
  - automatic request, HTTP-client and Azure SDK recording, and Next.js's own span recording
  - the clean-up layers: `ScrubbingProcessors.cs`, `TelemetryScrub.Span`, the span rebuild in `scrub.ts`, and the kept-field lists
  - the log-line pipeline and category lookup, and the exception type and frame records
  - the current README paragraph

## Options
- **A. Build the smaller design.** It would be a new branch from main, with one gate round and the same rule: a NO GO stops it. **Recommended.**
- **B. Use the ticket's own stop-gap.** Switch on App Service logging for a bounded window. It is quick, but it probably records paths and client addresses, so it needs its own privacy check. [U]
- **C. Leave it.** HPSMPOC-224 stays in the backlog with the findings recorded.

**If you choose nothing:** nothing gets built, and this note waits.
