B1263 ADDENDUM-2 (answer to your STOPPED: NEEDS TUESDAY on FeedbackReview.held.test.tsx) -- from Tuesday s241

**Answer: YES, that one line, exactly as you propose.** `web/src/components/feedback/FeedbackReview.held.test.tsx:65` changes from `"?limit=100&state=held"` to `"?limit=100&category=review&state=held"`. It becomes the first exception to the NOT-yours list, and it joins your closed list.

**Why (Tuesday read it at source, at head 0e0f42f1):** the file imports `AdminFeedback` (`:8`), renders it (`:56`) and pins its "Held for review" request (`:65`). It is a Feedback-received request pin of the same kind as the kit's U5 rows. The kit marked it NOT yours only because its name starts with `FeedbackReview`. No live seat writes it: H109 holds the shell paths, and no other HPSM-POC seat is live on this repository.

**Limits (binding):**
- No other line of that file changes. Print `git diff -U0` of the file in STATUS; exactly one changed line is allowed.
- The new string is the real serialisation your U3 row pins (print both and show they are equal).
- Plant PW1 (category removed) must turn this row red too: add it to the PW1 red set and print it by name.
- In STATUS, name the file as an EDITED existing row (old value, new value, why, and the plant that turns it red). Your gate judges it as a possible weakening.
- If any OTHER NOT-yours file turns out to pin the same request: STOP again and name it. Do not extend this answer to it.

**Unchanged:** everything else in the kit and ADDENDUM-1. Record this addendum by name under Corrections and in your READY line.
