STARTABLE: yes, after the stamp (pane `Datasec/HPSM-POC-H80`, ports 9510-9519, Sonnet, tier-2 gate after).

# B978 drafter report (read-only, Sat 31 Oct 2026, about 12:40 AEDT)
Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B978_SEAT-H80_hpsmpoc-413-416-418-419-pins.md` (91 lines, unstamped; 9 lines with the four-underscore pattern, control matches the template's 9).

## BLUF
Lane 3 of the sweep, four tickets (HPSMPOC-413, -418, -419, -416), seven test paths, four commits on `b978/hpsmpoc-413-416-418-419-pins` off `8ce48527`. Test-only. Every pin must be red under the gate's plant. The one lane-wide risk is the e2e: 413's rows need a browser run and its product-side plant needs a rebuilt tree.

## Measured
- main `8ce485275455e07eaa39c46a50e62e7f7f2b3c83` (2026-10-31T01:33:56Z); open PRs 0; #258, #259, #260 closed and merged.
- Blobs/lines at main: step-previous.spec.ts 80 / `4d19ba69`; NarrativeScreen.previous.test.tsx 89 / `8e75a7b6`; AssessmentScreen.restyle.test.tsx 78 / `c37ec581`; AssessmentScreen.previous.test.tsx 72 / `5be071a5`; DocumentGeneration.restyle.test.tsx 132 / `814549e5`; PackView.tsx 71 / `170b2e96` (lead at line 65); NarrativeScreen.tsx 168 / `ab78738a` (testid line 145).
- Intersection: 28 live `b9*` refs; only b954, b956, b957 touch these paths, all heads of merged PRs (landed). No `b978*` ref. Control: compare feb3da65...main lists SecurityDashboard.test.tsx (1).
- Panes: `%0`, `%93`, `%94`, `%1`; none H80. Ports 9510-9519: 0 listeners; no 30-31 Oct kit names 951x (loop printed nothing; control on 9990 in the B973 kit read 3).
- load1 6.25 at 12:37 (near the 7 line). Sonnet id `claude-sonnet-5-5` (models_latest.json line 23).
- Jira: all four read by GET, all Backlog, 0 comments; fix-shapes in the kit match them. Plants: 413 B966 p6 and B967 p1; 418 B966 p9a; 419 B967 p6 p7 p9 p10 p11 p12; 416 B964 p3 and p8.

## Q-questions (defaults)
- Q-1 (e2e port): the Playwright web-server port is UNMEASURED (config not read; not in the sweep). Default: builder points it at 9510-9519 and says how; if the config hard-codes another port, it STOPs. Tuesday: confirm or name the port.
- Q-2 (scope split): four tickets in one PR is large (about 120 min). Default: one PR, four commits. Alternative: split 413 (e2e, needs a build) from the three unit tickets.
- Q-3 (gate round): default round 1 of 2, tier 2 (test-only, plants proved by builder).
- Q-4 (416 new file name): default `PackView.lead.test.tsx` beside `PackView.tsx`.

## Stamp values suggested
Target READY 120 min after Step 0, hard stop 180. Head/main at launch `8ce48527...`, no `b978*` ref. Model receipt: `model: claude-sonnet-5-5 -- Sonnet first: test-only pins (model-routing.md row C2 line 92, class row L6 line 85, gate row G2 line 109)`. KEYS: HPSMPOC-413, -416, -418, -419.

## Not done
No worktree, test, build or Playwright run; the 413 e2e red proof and the 419 component mapping (which component renders the API list and runner alert) are left to the builder. The sweep named the API assessments list component as not located.
