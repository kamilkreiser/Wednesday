## What this changes

**Before.** When the AI endpoint answered with an error, the chat routes kept the error's own words only for one kind
of error, the AI adapter's redirect refusal. The rule that picked that kind was the error's code string. The AI client
library copies that code from the error body the endpoint sends, so an endpoint could send the code with its own text,
including HTML, and have that text reach the user:

- `GET /api/chat/stream`: in the stream's error event.
- `POST /api/chat`: in the answer, or in the 500 answer's `error` field (also in `details` in the development
  setting), depending on the path the question takes.
- `POST /api/chat/stream`: in the error event, after `Analysis error: `.

The chat page then wrote a stream error event's message into the chat bubble as HTML, so markup in it became elements
in a signed-in user's page.

**Now.**

- The server keeps an error's own words only when the error is an instance of the adapter's own refusal class. An
  endpoint cannot make an error be one: when the adapter itself builds the class, the message is always the adapter's
  fixed refusal text.
- Six places in `backend/server.js` test the class instead of the code string: the helper that picks the chat error
  text, the two text choices of `POST /api/chat`, and the three places in the question analysis that rethrow the
  refusal instead of falling back. The class is imported once at the top of the file.
- The chat page writes a stream error event's message through its own `escapeHtml`, so it shows as typed.

**What a real redirect refusal says.** Exactly what it said before, on all three routes: the adapter's refusal words,
which tell the administrator to set the endpoint to the resource's own address.

**The one behaviour change.** An endpoint error that only carries the code string no longer stops the rule-based
fallback on `POST /api/chat` and `POST /api/chat/stream`. The user gets the ordinary fallback answer, as for any other
endpoint error. On `GET /api/chat/stream` such an error reads `Error processing chat message`. The fallback answers
from the same data it uses for every other endpoint failure; nothing new is shown.

## Choices

Every choice here is a default of the coordinator, not a ruling of the product owner:

- the class check, at six places (three of them rethrow sites the ticket does not name);
- the one import line;
- the page's own escape on one token;
- leaving the two health reads, which compare a code the adapter itself sets, and the adapter's own code check;
- rewriting the one existing test that expected the old answer.

## Listed, not fixed

- Other chat-region page writes in `static/js/index.js`: the tool-call status label, the two status-event messages,
  the model name, the sub-query list and the connect-failure line. An independent check found the tool-call label
  can be filled by an AI endpoint today.
- The first-run wizard's message lines.
- The adapter's own code-string check, which renames a stream error event that carries the code into the redirect
  refusal (the refusal's words only).

## Tests

- Three new files, 21 cells:
  - the helper on errors built by the real client library and the real adapter, plus source checks;
  - the page's real stream reader and escape in jsdom;
  - the real server against a stand-in endpoint that answers 400 and 500 with the code and an HTML text.
- 14 of the 21 cells are red without the change.
- One existing test rewritten.
- The full verify passes at 6216 tests in 393 suites.

## Not tested

- Any hosted instance, a real AI endpoint, Linux.
- The page under a hosted content security policy.
- The hosted Build and CodeQL on the merge commit.
- The Deploy demo run a merge starts, which must read skipped.
- An independent check rendered the stream error event in a real local Chromium; that is not part of the committed
  tests.

Not deployed.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
