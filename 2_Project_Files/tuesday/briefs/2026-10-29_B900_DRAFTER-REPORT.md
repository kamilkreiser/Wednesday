STARTABLE: YES

# B900 DRAFTER REPORT (tier-1 gate kit, HPSM-POC PR #240, seat G203)
Drafted Thu 29 Oct 2026 ~15:51-16:05 AEDT (clock from `date`), read-only. Kit: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-29_B900_SEAT-G203_hpsmpoc-240-v12-shell-sidebar-gate-tier1.md` (89 lines, long paragraph lines, under the cap).

## BLUF
Startable. Model Opus (row G1, `model-routing.md:108`; id from `models_latest.json` line 17 = `claude-opus-5-5`), `BRIEF_SEAT_LEVEL=opus` and `WED_USAGE_STOP=100` placed both before `launch_when_cool.sh` and inside the quotes. Ports 9910-9919. One finding the kit makes the gate's first measurement (H-1): the head widens "Service offers" to Consultant and Demo, and the builder's STATUS does not flag it.

## Facts re-measured (instrument, control)
- PR #240 (`gh api -X GET pulls/240`): open, not draft, head `66a760a0...`, base `c00e2828...`, 19 files, +1087 -330, 5 commits, `mergeable_state` blocked, title "Shell: a left sidebar and top bar replace the header burger (design v1.2, step 1)". `pulls/240/files` listing = the builder's 19 paths (all `web/`); burger unit test and burger e2e spec are the two deletions (94 and 111 lines). Control: the numbers match the builder's STATUS independently (5 commits, 19 paths).
- main = `c00e2828...` (`git/matching-refs`); open PRs = #239, #240. `check-runs` total_count on the head = 13 (baseline, not read for status).
- Role heart (raw reads of `GlobalNav.tsx` at both shas, grep with line numbers): base `/services` `roles: PARTNER_SIDE` (line 30; partner, admin); head `services` `roles: ALL_ROLES` (line 50) so Consultant and Demo gain Service offers. `training` `ALL_ROLES` but `built:false` (line 45); `my-readiness` `built:false` (line 44). Picker gate `AppShell.tsx:146` (`role !== "demo"`), `shell-flags.ts:3`. The builder's STATUS lists Service offers inside the Consultant nine but does not name the widening; the design delta 2.1a says the API role rule must be checked before widening. Not measured: whether the BFF/API accepts those roles (left to the gate, H-1). Control weakness: a raw read, no run.
- Ports: `lsof -nP -iTCP:9910-9919 -sTCP:LISTEN` empty (rc 1; no positive control run, left to the gate). Word-boundary scan (`/usr/bin/grep -E '(^|[^0-9a-fA-F])991[0-9]([^0-9a-fA-F]|$)'`) over non-`.pre-` SEAT kits of 10-28 and 10-29: ONE hit, B876 (J30, finished Composer builder, no live pane). Frame: 2026-10-28/29 SEAT kits only. Panes at 15:51: tuesday, Security-Composer-G201, HPSM-POC-G199, NexusAI-G200, NexusAI-G198, HPSM-POC-H53, fleet-monitor; no G203, and H51 is not live.
- Kit hygiene (program): four-underscore lines 8 (7 slots + last line, control = expected 8 for an unstamped kit), non-ASCII 0, at-slot pattern 0, the owner's name 0 after one edit (a routing-row quote carried it; replaced by "the product owner's").

## D-decisions
- D-1 Class text: "the shell decides which pages each role reaches ... or breaks a guarantee the pre-change shell kept"; instances (a)-(g). Round 0 of 2 before, this is round 1 of 2 (no earlier gate judged the shell).
- D-2 Hard stop: target verdict 150 min, HARD STOP 240 min (two builds, two whole unit and e2e runs, plants with builds, plus CodeQL wait under shared load). Longer than B896 because the web e2e suite is heavy.
- D-3 Heavy plan: own lock `.tools/b900/heavy.lock`, load1 < 7 on two reads, same as B896; ports 9910-9913 Playwright, 9914/9915 builds, 9916-9919 spare. G199 (infra, whole suite plus 20 repeats) shares the machine load.
- D-4 H53 (B891) is a live neighbour: gate re-measures its branch files at the verdict and names the `ui/*` import coupling as a Note.
- D-5 Landing: head-pinned squash with explicit text (repo squashes with `COMMIT_MESSAGES`, five commits would all land). `CLARIFICATIONS.md:138` precedent, as in B863.
- D-6 The builder's own plant driver and kit are read-forbidden; the gate writes its own plants (and three more of its own aimed at role reachability).

## Q-questions for Tuesday (each with a default)
- Q-1 H-1 handling: if the Services routes refuse Consultant/Demo, the kit makes it a Blocker (a nav entry must never promise a refused route). Default: yes, Blocker. If source is unreadable: GO WITH FINDINGS (conditional) with the question to Tuesday.
- Q-2 Do any earlier NO GOs on shell/nav count toward the class? Default: none counted (the gate prints a loose scan; counts only role-reachability or shell a11y/print NO GOs).
- Q-3 Ticket keys: HPSMPOC-368 given; the builder said four keys were PENDING. Default: the gate reads 368 and whatever the PR body names; Tuesday supplies the other keys at the squash. Jira not read by the drafter.
- Q-4 Hard stop 240 min acceptable? Default: yes.
- Q-5 One Chromium download allowed if missing? Default: yes (the builder needed it).

## UNMEASURED
API/BFF role rules for `/services`; any `https://` or external asset in the 19 paths; builder counts (3039/3093, 398/446, 25 mappings, plants, contrast numbers); check-run states; Jira text; H53's current file list (builder reported 12 `ui/*` paths, 0 shared); whether Chromium is installed here.

## Outside the fences
None: read-only. Opened: DRAFTER_RULES, the three template kits (B863 and B896 read whole, B831 not re-read; shape taken from B863 and B896), B885 STATUS (whole), the design delta (whole), `model-routing.md` and `models_latest.json` (grep), `brief_seat.sh` lines 15-30. Did NOT open the B831 kit/report, B831/B863 STATUS or DRAFTER-REPORTs, the B885 kit, the prototype HTML, or any `.tools` tree; GET-only `gh api` under the project config; no Jira call, no card tool, no clone/fetch. Slot count with control: 8 (an unstamped kit reads 8).
