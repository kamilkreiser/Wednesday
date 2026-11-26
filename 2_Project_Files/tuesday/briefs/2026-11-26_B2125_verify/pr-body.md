Three commits on `89663a44`; four paths; `backend/server.js` gains 15 lines and loses none (two inserts: 12 lines in the risk-condition update route, 3 lines at the top of the chat stream route). No workflow, no helper, no other test file is changed, and nothing is deployed.

## RD-893: `PUT /api/risk-conditions/:id`, the type-check half
- Three checks now sit between the existing risk_level check and the store call. A field that is PRESENT must have the type the Settings page sends: `condition_text` a string, `is_active` `true` or `false`, `email_recipients` a list. A present `null` counts as wrong. An absent field is not checked, so every field stays optional.
- A wrong value is answered 400 with the route's own one-key shape and nothing is stored: `Invalid condition_text. Must be a string`, `Invalid is_active. Must be true or false`, `Invalid email_recipients. Must be a list`. Before this change such a value was answered 200 and stored. A stored `condition_text` that is not text throws in `generateKQLQueryForCondition`, which calls `toLowerCase` on it.
- `false`, an empty list and an empty string are still accepted. A wrong level beside a wrong text is still answered with the level sentence. The risk_level check, the landed lower-casing of the level and the lines that read the body are unchanged; the diff only adds lines.
- New file `__tests__/rd893-risk-condition-put-field-types.test.js` (19 cells) boots the real server in the open first-run window, with one planted condition per request, and reads the stored file before and after each request. T1 to T13 and C1 read red before the change and green after. The precondition, P1 and A1 to A3 are controls that read green on both sides.

## RD-1009: `POST /api/chat/stream`, the early 400 only
- When a request had a content type that no body parser reads (for example `application/vnd.api+json` or `text/plain`), or had no body at all, `req.body` was undefined. The handler read its fields above its first try block, so the read threw, and in the development setting the final error handler answered 500 with the thrown text (`Cannot destructure property 'message' of 'req.body' as it is undefined.`).
- Before the field read, the route now refuses any body that the shared plain-object check (the one the user add route already uses) does not accept. The answer is the route's own `400 {"error":"Message is required"}`, sent before any model call. The refusal is one line, and the field read line is unchanged.
- New file `__tests__/rd1009-chat-stream-unparsed-body.test.js` (9 cells) boots the real server through the shared harness in the development setting, with a model stand-in. R1 to R3 read 500 with the thrown text before the change and 400 after. N1 to N5 read the same on both sides: an ordinary JSON message and a form-encoded message still stream, and an empty message, a JSON array and an over-long message keep their answers. C1 reads the source text.

The counts file moves from 6476 tests in 407 suites to 6504 in 409. The project's own command wrote it.

## Choices made by the coordinator, not by the product owner
One change for both tickets. The three types are `condition_text` a string, `is_active` a boolean and `email_recipients` an array. `null` is refused, and absent fields are not checked. There is no length or character rule for the text and no rule for the type of each recipient. The three 400 sentences are the ones above. The stream refusal is one line that reuses the route's existing `Message is required`.

## Reviewed
An independent review re-ran both new files at the base and at the head, in two shapes: a Linux-like temp setup (`TMPDIR=/tmp` with a persistent `RUNNER_TEMP`) and this machine's own temp folder. In both shapes the update file's T1 to T13 and C1, and the stream file's R1 to R3 and C1, were red at the base, and every cell of both files was green at the head. It also ran the ten one-line mutations of the change: each turned red exactly the cells named for it. It sent extra request shapes that the new files do not cover. A form-encoded `is_active=false`, `condition_text[a]=b` and a JSON duplicate key whose last value is wrong are now refused. A form-encoded `email_recipients[]` list is accepted. A JSON `null`, a JSON primitive or an empty JSON body on the stream route keeps its earlier answer. gitleaks found nothing in the commits or their messages.

## Named limits
- The PUT checks type only. An empty or very short `condition_text`, a text over 500 characters and a text with characters that create refuses are still accepted on the update route. A list of recipients is not checked element by element.
- On the stream route, a body the parsers REFUSE still reaches the final error handler, which in the development setting answers with the parser's own text. That covers malformed JSON (and a JSON primitive or `null`), an unsupported charset, an unknown or corrupt content encoding, a body over the 2 MB chat cap, and a form body that is too deep or has too many parameters. The answer for these is a product decision, and RD-1009 stays open for it. In the production setting the handler answers with a fixed sentence.
- The Log Analytics path with a stored text (the ticket's measurement) was not run, and RD-893 stays open for it.
- The hosted `build` job of this pull request is the first run of the two new files on a real Linux machine. A red result there on a new cell is a fix round.

## Deploy
None. The merge touches `backend/` and `__tests__/`, which the Deploy demo workflow does not ignore, so a run starts on the push. Both of its jobs are expected to read skipped because the switch variable is not set.
