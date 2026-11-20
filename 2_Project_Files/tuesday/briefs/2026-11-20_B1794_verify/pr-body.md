## What a user sees, and what the server receives

Before: on the quote screen, every typing pause longer than 2 seconds sent a save request, and every save writes a history event and a stored revision. In a minute of typing with 2.5-second pauses (22 pauses) the server received 22 save requests.

Now: after a save request, the next autosave from the same open quote screen waits until 10 seconds have passed since that request. A change made inside those 10 seconds is kept on screen and sent by one trailing save when the 10 seconds end and the 2-second quiet interval after the last edit has passed. In the same minute of typing the server receives 6 save requests by 60 seconds and a 7th at 62 seconds that carries the last edit (counted by a test that runs the screen on a fake clock).

Not delayed, as before: the first save of a visit, leaving the screen (the pending change is sent at once), Save draft, Save & calculate, and Calculate with a changed draft.

The screen reads "Unsaved changes" for the whole time a change is waiting, and the browser's unsaved-changes prompt stays armed, so a change never reads as saved while it is waiting.

## The 10 seconds

The 10 seconds is the coordinator's default under the ticket's own text, which names a minimum gap between saves as one of the options and does not pick one. It is one constant (`AUTOSAVE_MIN_GAP_MS`, beside the quiet interval) and is reversible by changing that one line. It is not a ruling of the product owner.

## Stated limits

- The gap limits autosave requests from one open quote screen. It does not limit saves from other screens, other browser tabs or other people, nor explicit saves.
- The gap is kept by the open screen: a quote left and opened again inside the 10 seconds starts with the gap open.
- A change made inside the gap stays unsaved for up to 10 seconds unless the user leaves the screen or saves. The screen reads "Unsaved changes" for that time and the unsaved-changes prompt stays armed. Closing the tab inside the gap is covered by that prompt only, as before.

## Changed

Four files: the constant in `autosave.ts`; the gap logic in `QuoteScreen.tsx` (three refs and one timer, no clock, no new listener, no new trigger); 11 new test cells and one changed expectation in two test files. The quiet interval, the server, the API client and every word on the screen are unchanged.

## Not tested

CodeQL (the hosted run on this pull request decides). A run against the real server (the browser steps run against the dev stub and with no API). A real browser tab closed or crashed inside the gap.

Not deployed. Nothing in this change deploys.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
