## What changes

**RD-1005: the three chat routes**

- `POST /api/chat`, `POST /api/chat/stream` and `GET /api/chat/stream` now refuse a message that is not a string. That covers an array, an object, a number, a boolean, `null`, and a key sent twice in a form body or a query. The answer is the routes' existing `400 {"error":"Message is required"}`. It comes before the length check, before any other use of the message and before any model call.
  - Before this change, `POST /api/chat` answered 500. In development, `details` held the thrown error's own text (`message.toLowerCase is not a function`).
  - `POST /api/chat/stream` opened a 200 stream that ended in `Analysis error: (query || "").toLowerCase is not a function`.
  - `GET /api/chat/stream` with the key sent twice ended in `Stream error: query.toLowerCase is not a function`.
- A failing chat route now sends the client one constant text, `Error processing chat message`, in place of the thrown error's own text. This covers the `details` field (development only, as before) and the four stream error events. The stream routes keep their `Stream error: ` and `Analysis error: ` prefixes.
  - The thrown text is still written to the server log by the `logger.error` line at the top of each catch block.
  - The named refusal of an AI endpoint that redirected (RD-523) keeps its own words. `rd523` cells C1 and E4 pin it.
- One small helper, `chatErrorText`, holds that rule. It sits beside `chatMessageTooLong`.

**RD-1007: adding a user**

- `POST /api/auth/users` now reads its fields through the existing `isPlainRequestObject` check, which the settings writes already use.
- A body that no parser read used to make the route answer `500 Failed to add user`. That happened with `application/merge-patch+json`, `application/vnd.api+json`, `text/plain`, or no content type and no body. The route now answers its own `400 {"error":"Email, name, and password are required"}`, and no user is stored.
- The administrator check still runs first, so a viewer gets 403 for every one of these shapes.
- An ordinary JSON add works as before.

## What an ordinary user sees change

- When a chat stream fails, the dashboard's chat bubble shows `Stream error: Error processing chat message` (or `Analysis error: ...`) in place of the internal error text. For example, when the model host cannot be reached, the bubble used to show `Connection error.`.
- The dashboard always sends the message as text, so ordinary chats are unchanged.
- An administrator adding a user from the settings page sends JSON, so that is unchanged too.

## Cells

- `__tests__/rd1005-chat-message-not-text.test.js` (23 cells):
  - R01-R11: each non-string shape on each route answers 400 with no model call.
  - E1: an unparsed body on `POST /api/chat` answers 500 with the constant in `details`.
  - H1: a GET stream with the model host closed sends only constant error texts.
  - U1-U3: the helper, taken from the source text.
  - C1-C2: the source text of the chat region.
  - N1-N5: behaviour that stays.
- `__tests__/rd1007-user-add-unparsed-body.test.js` (9 cells):
  - R1-R4: the three content types and no body answer 400, and no user is stored.
  - N1-N4: an ordinary add, a missing name, an array body, and a viewer's 403.
  - C1: the source text.
- Every R, E, H, U and C cell is red on the current main and green on this branch. Each one goes red again when the line it protects is put back.
- The full verify passes with 6041 tests in 382 suites, and the expected counts file is updated to match.

## Left for a follow-up (not in this change)

- 30 other route handlers read fields from `req.body` without a guard. They include `POST /api/chat` and `POST /api/chat/stream`:
  - On `POST /api/chat`, an unparsed body still answers 500, now with the constant in `details`.
  - On `POST /api/chat/stream`, it still throws outside the route's `try`. The server's final error handler answers it, and in development that answer includes the thrown text.
- A JSON parse error is answered by the same final handler, which in development includes the parser's text.
- The RD-523 exception matches the error code string. An AI endpoint's own HTTP error body can carry that code, so the endpoint's own text can still reach the chat bubble. This was already possible before this change, and the change narrows it. Matching the adapter's own error class would close it.
- Non-string values on other routes, and the error text of routes outside the chat region.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
