# For the records (MPSCALC-314), gate round 1

## The ticket now
MPSCALC-314 reads Backlog, last updated 2026-10-20, 0 comments, read by Jira GET at the gate. One sentence for the comment: autosave on the web quote screen now keeps a minimum gap of 10 seconds between save requests from one open screen (a named constant, the coordinator's default under the ticket's own text, one line to change); the quiet interval, the server and the screen's words are unchanged; not deployed. A merge does not move the ticket (no project rule moves a ticket on merge).

## The three stated limits, in plain words
- The gap limits autosave requests from one open quote screen only. It does not limit saves from other screens, other browser tabs or other people, nor explicit saves (Save draft, Save & calculate, Calculate with a changed draft).
- The gap is kept by the open screen. A quote left and opened again inside the 10 seconds starts with the gap open, so two requests can fall inside 10 seconds across a leave and a return (tested, cell B12 of the gate's own attack set).
- A change made inside the gap stays unsaved for up to 10 seconds unless the user leaves the screen or saves. The screen reads "Unsaved changes" for that time and the unsaved-changes prompt stays armed.

## Two things the gate measured that the limits do not say
- A refused save also starts a gap. If a save is refused and the user then edits, the edit is held until the 10 seconds from the refused request have passed, and the refusal message stays on screen for that time (before: 2 seconds). Measured by the gate's own cell; the change is then sent and the message clears.
- Exposure on an unclean exit grew from 2 seconds to 10 seconds. Closing the tab asks the user first (the prompt stays armed all through the gap, as before); a crash, a discarded tab or a power loss inside the gap loses the waiting change, and the window for that is now the gap.

## The acceptance wording, read per gap
The ticket's acceptance sentence says a counting fake fails above one save request "per quiet interval". The build reads it per gap: the test counts saves in a 60-second run with 2.5-second pauses and fails above 6 (6 by 60 s, a 7th at 62 s; the same script without the gap makes 22). One save per 10 seconds is also at most one per 2-second quiet interval for autosave requests from one open screen. The ticket's other option (the server coalescing the history events) is not built and is not needed for this wording.

## The other save site
`web/src/proposal/ContentEditor.tsx` (the proposal content editor) also calls the draft save. It is a button only (no timer, no autosave), the ticket's text is about the autosave on the quote screen, so the ticket's text does not cover it. Nothing is changed there. A follow-up only if the product owner wants a gap on explicit saves too.

## Follow-ups (none blocking)
- The tests do not pin that an explicit save starts a gap of its own, nor that a new request restarts a running gap (two mutants survive the owned cells; the gate's own cells catch both). A later test-only change can add them.
- Nothing is deployed. Landing is the pull request, hosted CI and CodeQL; the hosted CodeQL run decides for this repository.
