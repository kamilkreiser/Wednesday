B1263 ADDENDUM-1 (read at your next step boundary; it CHANGES two stamp slots; where it and the kit differ, this file wins) -- from Tuesday s241

**The product owner approved the two sentences** on the live board at 2026-11-04 09:50:17 AEDT ("Approve the two proposed sentences"). So your stamp slots change:

- **WORD-LEAD** is no longer `keep`. It is the exact string:
  `Everything sent with "Run idea / feedback past Steve", newest first, with the files people attached. A file downloads; it never opens inside the Playbook.`
- **WORD-EMPTY** is no longer `keep`. It is the exact string:
  `Items sent with "Run idea / feedback past Steve" appear here, newest first.`

Build both from the constant `REVIEW_LABEL` with a template literal, as the kit's DESIGN 6 says. The quoted text inside each sentence must equal the constant byte for byte (ASCII double quotes around it). Never type the name in code.

**What follows from the kit itself (DESIGN 5, DESIGN 6, row W):** `web/src/app/(app)/admin/feedback/page.tsx` joins your closed list, for the lead only, and `AdminFeedback.tsx:91` changes for the empty body. Row W is added (red at the head, green after; plant PWL reverts the lead and must turn W red), and PWL joins the plant budget. No other word moves. The page title, the card heading "Feedback received", the link text, the state words and "No feedback yet." stay as they are. In STATUS, write both sentences as rendered (by program, from the built page), and name the two old sentences as replaced, not as known-false.

**Unchanged:** everything else in the kit and its stamp. Record this addendum by name under Corrections, and name it in your READY line.
