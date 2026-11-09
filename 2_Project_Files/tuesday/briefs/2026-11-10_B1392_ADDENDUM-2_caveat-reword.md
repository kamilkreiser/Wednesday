From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. ADDENDUM-2 to your kit B1392 (SEAT-H142). Every hold, partition and housekeeping rule of the kit still binds you. HARD STOP 10:30 AEDT 2026-11-10.

# ONE CHANGE, ON A NEW BRANCH `b1392/hpsmpoc-caveat-reword`, CUT FROM CURRENT ORIGIN MAIN (`0820efe9` or later: print it)

**The product owner's ruling (board 2026-11-10 09:03, card hpsmpoc-walkthrough-caveat-to-uat-1110, option b, verbatim):** "Reword it without the score-and-approve instruction". He then wrote in the coordinator's terminal: "don't wait, deploy as soon as it's ready". This change goes to UAT the moment it is gated and landed.

**The change.**
- In `web/src/content/walkthrough/steps.ts`, the step 10 `caveat` (line 130 at 0820efe9; re-print it), remove the instruction clause "score the assessment and approve the narrative before you show it". Keep only what is true and needs no write: the report holds sample content and is not HP-approved guidance; on the laptop sample the screen shows "No report yet" until the assessment is completed and scored, then waits for the approved narrative; and do not promise either wait for every customer.
- Write it as plain presenter-note words in the file's existing style. It must give NO instruction to save, score or approve anything; that is the file's own rule at `steps.ts:6-7` and step 6's "View only".
- Update `steps.test.ts`'s existing pin of this caveat to the new words, and add one row that fails if any step's caveat or cue contains an instruction to score, approve or save (patterns: /\bscore the\b/i, /\bapprove the\b/i, /\bsave\b/i). The row must be RED on 0820efe9's caveat and GREEN on yours.
- Nothing else: only those 2 files.

**Prove it** in STATUS under `## ADDENDUM-2`:
- `git diff origin/main HEAD --stat`: 2 files.
- vitest for `steps.test.ts`: red-first on the old caveat (show it), green at your head.
- The full `npm test` count.
- Lint and typecheck rc 0.
- The two walkthrough e2e specs (`playbook-walkthrough.spec.ts`, `walkthrough-uat.spec.ts`) green at your head.
- The new caveat sentence quoted WHOLE on its own line, `NEW CAVEAT: <text>`, for the product owner's words list.
- A plain-ASCII commit message with no B-number or name, ending with your attribution line, then `git push origin b1392/hpsmpoc-caveat-reword`.

**Last line:** `READY B1392-2: <head sha40>` (equal to `git ls-remote` of the new branch), or `STOPPED: NEEDS TUESDAY <one question>`.
