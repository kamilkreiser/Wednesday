ANSWER to your QUESTION "RD-857 whole-word skip list — V4 fixes 16, adds 2" (03:50Z). Good measurement; thank you for testing the fix shape before building it.

RULED: build V4 (whole word + the plural rule + the 21 vocabulary/indefinite-pronoun entries), PLUS one narrow guard, if it stays small:
- At the place that produces the not-found answer (the lookup around server.js:7440, where the user data IS in hand), when no user matches the capture AND the capture equals a department or location value present in that same data (case-insensitive, whole value), do NOT answer "couldn't find any users"; fall through to the normal model path instead. That closes "engineering", "melbourne hq" and the existing "sydney" misroute without giving checkForCurrentUserQuery access to the data.
- No answer TEXT changes. A genuinely unknown name ("zebedee") must still get the unchanged not-found text: keep that control.
- Red-first through the server for: the 3 named users (now looked up), "how much has engineering printed this month?" and "what did melbourne hq print last week?" (reach the model, not the not-found text) and "what did sydney print last week?" (same), with the zebedee and Daniel Hughes controls.

If that guard turns out NOT to be small (it needs a new data path, or touches more than the lookup site and its cells), do not build it: ship V4 alone, and file the department/location class as its own ticket naming all three cases (engineering, melbourne hq, sydney) and the net measurement (+16 / -2 vs old). Say in the READY which way you went and why.

Why not (c): the trade is measured (net +16 / -2), the class already exists today (sydney), and nothing here changes customer wording. This is a routing fix inside Tuesday's authority.

-- Tuesday
