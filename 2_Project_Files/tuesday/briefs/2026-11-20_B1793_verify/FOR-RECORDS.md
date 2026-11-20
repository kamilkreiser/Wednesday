FOR THE RECORDS SEAT: RD-1008 (gate B1793, round 1). Text below is plain; no seat, brief or card id goes into Jira.

RD-1008: state and one sentence (post after the landing, with the merge commit's first 8 characters)
- State: move to Testing on the landing (the project's rule for a landed code change); not Release Ready until the
  hosted Build and CodeQL on the merge commit are read.
- Sentence: "Landed: the chat routes keep an error's own words only when it is the AI adapter's own redirect-refusal
  class, never because of a code string an AI endpoint's error body carries, at six places; on GET /api/chat/stream
  such an endpoint error now reads the constant, and on POST /api/chat and POST /api/chat/stream it no longer stops
  the rule-based fallback, so the user gets the ordinary fallback answer; a real redirect refusal reads exactly as
  before; the chat page writes a stream error event's message as text. The class check, the six places and the
  page's own escape are the coordinator's defaults, not an owner ruling; the other chat-region page writes are listed
  and not fixed."
- Acceptance wording to note in the comment: the ticket's line "gives the constant" holds for the GET stream route; the
  two POST routes give the ordinary rule-based fallback answer instead (no endpoint word in either case, measured over
  HTTP by the gate).

Candidate tickets (each with its own search before filing)
1. Chat-region page writes not covered by any ticket (RD-1014 excludes the chat region; RD-1008 names one write).
   Security, Medium for the first item, Low for the rest.
   - static/js/index.js:3523 (the tool-call status label). MEASURED REACHABLE by an AI endpoint:
     - the server forwards the model's tool-call arguments into the tool_call event of POST /api/chat/stream
       (backend/server.js:7950 spreads the event; backend/llm/azureOpenAIAdapter.js:313 passes the parsed arguments);
     - a stand-in endpoint that answered with a search_users call whose pattern held an image tag with an error
       handler got that text into the event, at the base and at the head alike;
     - in a real local Chromium the page's own stream reader wrote it into the status line as markup: one img
       element was created and its handler ran.
     The page's content security policy on a hosted instance was not measured; RD-1014 says the strict policy is
     the default and blocks inline handlers. The fix shape: escapeHtml on the label's values (args.pattern,
     args.userName, args.printerName, args.department) and on data.name.
   - :3466 and :3478 (status-event messages) and :3470 (sub-query types): the server writes constants today; no
     endpoint or user chooses them.
   - :3474 (model name): from the server's model configuration, not an endpoint or a viewer.
   - :3569 (the catch's error.message): the page's own "HTTP <status>" or a fetch error, not server-chosen text.
   - static/js/first-run-setup.js:1486, :4127, :4240 (data.message of the wizard's discover-tables and auth-enforce
     answers): an administrator's own setup screen; RD-1014's first-run rows.
2. The adapter's own code-string check (backend/llm/azureOpenAIAdapter.js:121-127, isRedirectRefusal).
   - A stream error event from the endpoint that carries the code, or the message "unexpected redirect", is renamed
     into the redirect-refusal class.
   - The user is told the endpoint redirected when it did not. The words are the adapter's own; no endpoint text.
   - Measured over HTTP on GET /api/chat/stream, the same at the base and at the head. Low.
3. Coverage: no committed behavioural cell sees a single reverted layer on the POST chat routes.
   - Five of the six class checks, each reverted alone, turn only the two source cells C1 and C2 red. No HTTP cell
     goes red.
   - A revert that keeps the class-check text and adds an `== 'AI_ENDPOINT_REDIRECT_REFUSED'` test beside it turns
     neither C1 nor C2 red. Measured with all five route-side sites reverted that way: only H3 caught it.
   - The outer catch of POST /api/chat (backend/server.js:7654) IS reachable by an endpoint error: a question that
     takes the user-cost or quick-insights path calls the analysis outside the inner try. No committed HTTP cell
     drives that path.
   - Fix shape:
     (a) a unit cell that reads each of the six predicates from the source and evaluates it on errors built by the
         real client library (the gate's progs/matrix.js form);
     (b) H cells that assert the positive answer, so the rule-based fallback is served rather than the
         "I encountered an issue" text. This catches a reverted first rethrow alone.
     (c) one H cell on the user-cost or insights path of POST /api/chat. Low.
4. GET /api/ai/status returns an AI endpoint's error text in details.error.
   - The model-list health check copies the SDK error's message, for example "400 <endpoint text>".
   - Measured over HTTP, the same at the base and at the head.
   - The setup wizard writes it through its own escape (first-run-setup.js:417-419). Info or Low: who may call the
     route, and every other renderer of it, were not measured.

Alignment comment for RD-1014
- "RD-1008 landed with one chat-region write fixed (static/js/index.js:3529, the stream error event, now through
  escapeHtml). The other chat-region rows RD-1014 excludes belong to no ticket. One of them, the tool-call status
  label (:3523), can be filled by an AI endpoint today (a candidate ticket is filed beside this)."

Follow-ups
- After landing: read the hosted Build (6216/393 on Node 24), the hosted CodeQL on the merge commit (no new alert, 22
  open, none expected to close) and the Deploy demo run (build and deploy skipped).
- The kit's MUTATIONS note that the outer catch of POST /api/chat "is reached only by an unparsed body" is wrong.
  Measured: the user-cost and insights paths reach it with an endpoint error. Correct it in any later kit that reuses
  the table.
- RD-1005 (Testing): no change asked by this lane; its second acceptance line now holds for an endpoint's error body
  on the chat routes.
