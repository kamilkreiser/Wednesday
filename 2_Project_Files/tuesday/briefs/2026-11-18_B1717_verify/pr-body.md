## What changes

RD-1000. A chat message had no length bound, and the server's JSON body limit is 50 MB, so one very large chat message could hold the whole server for several seconds. This change bounds both.

- A chat message longer than 100000 characters is refused at once with a 400 and the one-key error answer the chat routes already use: `{ "error": "Message too long (max 100000 chars)." }`. This applies on `POST /api/chat`, `GET /api/chat/stream` and `POST /api/chat/stream`, before anything else in the handler runs (so before any model call, and before the stream opens). A message of exactly 100000 characters is still accepted. A character is counted as one JavaScript string unit (UTF-16 code unit).
- A request body under the `/api/chat` prefix larger than 2 MB is refused with a 413 by the body parser before any chat route runs. The chat prefix gets its own JSON and form parsers, mounted after the chat rate limiter and above the global parsers. Every other route keeps the 50 MB limit, and `req.rawBody` is set exactly as before.
- An empty or missing message is still answered `Message is required`, as before. An ordinary message is answered as before.

## Who chose the numbers

- The 100000-character bound is the product owner's ruling.
- The 2 MB request cap, the wording of the error and counting a character as one UTF-16 code unit are this change's defaults. They were not chosen by the product owner.

## Files

- `backend/server.js`: +32 lines, 0 removed.
- `__tests__/rd1000-chat-message-limit.test.js` (new): 11 cells against the real server, with a stand-in at the model host.
- `scripts/verify-expected-counts.json`: 5887 tests over 378 suites becomes 5898 over 379.

## The cells

Refusals, each red on main and green here: a 100001-character message on each of the three routes (400, no model call); a 2.2 MB JSON body and a 2.2 MB form body (413, no model call); the health endpoint keeps answering quickly while a 40 MB chat message is refused (on main it was blocked for several seconds); a 1000000-character message under the cap is refused by the message check (400), not the cap.

Unchanged behaviour, green on main and here: an ordinary message reaches the model; exactly 100000 characters is accepted; a 3 MB body to a route outside the chat prefix is still read; an empty message is still refused with `Message is required`.

## Verification

Full suite: 5898 of 5898 tests passed across 379 suites. Each refusal cell was also shown to fail when its part of the change is removed. Oversized chat bodies are refused for every content type the server parses, for compressed bodies (the limit applies to the uncompressed size), for chunked bodies, and for path variants such as a trailing slash or a different letter case.

Not deployed. Code-scanning alerts 145 and 146 are in another file and are left open; this change does not touch them.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
