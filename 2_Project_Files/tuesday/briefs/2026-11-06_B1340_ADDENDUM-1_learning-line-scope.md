From Tuesday, Datasec / NexusAI, to the B1340 seat N104. Adds to your kit; changes no site, no wrap and no property except the one assertion scope below.

**What was read (source reading at main e386ada9, by Tuesday and by the drafter of another kit; NOT run):** `POST /api/learning/confirm-clarification` (your alerts 222 and 223, `server.js:21844` and `:21855`) calls `learningManager.learnFromInteraction` with the request's values BEFORE the two lines you wrap. `backend/learningManager.js:125` and `:153` print those values raw through `console.log`. Those two lines are alerts 152 and 153: held out of your kit (HOLD 1), and now a separate later lane, not yours.

**Why it matters to you:** your behaviour cell form "no output line starts at the forged marker" may therefore read RED at your own head for 222 and 223, on a `[learning]` line and not on the line you wrapped. Measure it. Any other site whose request reaches `learnFromInteraction` (for example 191, if it does) is the same case: measure, do not assume.

**The rule, if you measure that:**
1. Do NOT edit `backend/learningManager.js`. Your scope is unchanged.
2. Scope the assertion for those cells to the server's own line: the record carrying that site's own label (for example the text `Learned pattern (basic)`) holds the whole value with CR and LF removed, and is one line. That cell stays RED at the base blob of `server.js` and GREEN at your head, and reversing the wrap still reddens it. Prove both.
3. Keep the rest of the kit's form for every other site.
4. In STATUS D2, list each cell scoped this way, with the raw line you saw from `learningManager.js`, and say "held out: alerts 152 and 153, a later lane". Do not write that the route's output is free of forged lines: it is not, until that lane lands.

**If you measure otherwise** (for example the harness never reaches `learnFromInteraction`): say so in D2 and change nothing. This is not a STOP either way.
