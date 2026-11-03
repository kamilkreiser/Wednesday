STARTABLE: YES (once Tuesday fills the 7 Stamp slots; the kit has 8 four-underscore runs = 7 slots + the last-line marker)

# B1227 drafter report (SEAT-G324, HPSM-POC-442 gate round 2 of 2)

## BLUF
Kit is 49 lines (long lines, template shape), re-pointed from the B1221 kit: b1221->b1227, G321->G324, head af6fd4c7->f0000f54, round 1->round 2 of 2 (cap, NO GO is FINAL: residue.md + card-input.txt, no round 3). Adds a token-level hygiene census over both diffs, the reviewLabel.ts / server-page / equal-render check, the PDown A6 red-first check, and a full regression block 4(a)-(k) of round 1's behaviour checks.

## Facts re-measured (instruments in brackets; drafting date printed 2026-11-03 18:56:26 AEDT)
- Head f0000f54... and main f464376b... [gh api -X GET git/ref], open PRs 0 [pulls list length].
- compare main...head: ahead 2, behind 0, 36 files; af6fd4c7...head: ahead 1, 29 files [gh compare --jq]. Paths saved and counted by program: p36 = 36 lines; contains reviewLabel.ts and playbook-feedback-review.spec.ts (grep -c = 2), no playbook-feedback-b1206 name (control: the same grep pattern includes it, so a hit would count; it read 2 = the two new names).
- H111 branch b1097: 9 paths, comm -12 with the 36 = 0, self-control 9. Last commit f39ac80e.
- Dispatcher path is `api/src/HpsmPoc.Modules.Feedback/Delivery/FeedbackDispatcher.cs` (round 1's kit omitted `Delivery/`), blob 962cdb63... equal at main and head [contents API sha]. ci.yml blob 0176b491... equal at main and head. Hence the kit says to re-read the CI predicate at head but it is unchanged.
- Pointers by `grep -n` over raw files at head via gh contents API: reviewLabel.ts:4; FeedbackButton.tsx:1,:20,:28; review/page.tsx:3,:12; FeedbackModule.cs:63,:103,:169,:171; ReviewHeldMigrationTests.cs Facts at :72 and :83, new step :101-106, settle :123-124. All taken from program output, none remembered.
- CLARIFICATIONS.md:3617 and :3680 [gh raw + grep -n -i].
- Round count: B1221 line 1 = NO GO round 1; B953/B965 incidental (other class). Model: models_latest.json:17 claude-opus-5-5; model-routing.md:108 row G1, G-cap :111.
- Ports: lsof 9800-9999 = 0 listeners; 9690-9699 live (9692, 9696-9698) = H111. Word-bounded scan of 152 non-.pre- SEAT kits of 11-02/11-03: 981x = 1 hit (B1100:85, not a port: its text is a model-file note), 975x hit B1221 (G321's own), 976x B1083, 977x B1085, 978x B1085/B1103 (older kits), so 9810-9819 chosen. Control 969x = 2 hits (fires). Panes: tuesday, Datasec/NexusAI-G323, Datasec/HPSM-POC-H111, fleet-monitor; no G324 (grep -c -x 0). Free disk 218 GiB (df -k).

## D-decisions
- D1: ports 9810-9819 (817 = round-1-tree render, 9819 control listener).
- D2: gate may copy-and-re-run the round-1 gate scripts (hyg.py, plant.py, render.cjs, GateQaTests) from b1221; builders' trees/evidence stay READ-FORBIDDEN (b1225 added to the forbidden set).
- D3: added a `wt-b1227-r1` tree at af6fd4c7 so the equal-render and the gap controls compare against round 1's actual code, and so the census instrument must reproduce round 1's 51.
- D4: erase/regression items grade as round 1; "a regression of any round-1 row" is a Major; A6 step green under PDown is a Major; lead differing from round 1 is a Blocker.
- D5: the label's person word is not written in the kit (bracketed-pattern instruction) so the squash text rule holds; no card id is in the kit.
- D6: the gate also re-runs the four other feedback e2e specs (builder re-ran only the renamed one; their comments changed).

## Q-questions for Tuesday
- Q1: the builder placed the new A6 step BEFORE the review/held insert (its reading of the B1225 text). Kit asks the gate to judge it by red-first only. Default: accept if RED under PDown and not vacuous.
- Q2: B1221's NO GO text is "NO GO 0 of 2 before" in line 1; round count for this kit reads "NO GO 1 of 2 before" and S3 holds your reading. Default: as written.
- Q3: `api on SQL Server` is not a required GitHub check; kit keeps it as Tuesday's landing condition. Default: as written.

## UNMEASURED
- Whether `reviewLabel.ts` lead appears in the server HTML (left to the gate, step 2). The builder's claims (sha256s, hygiene counts, 5/6 whole-line residue) are repeated as CLAIMS only. Kit line numbers for gate-side ci.yml steps were not printed (kit says reprint at head). The local project checkout does not hold f0000f54 (stale), so every pointer came from gh raw reads.

## Outside-the-fences disclosure
Read only: DRAFTER_RULES, B1221 kit and STATUS, B1225 kit and STATUS, model-routing.md lines, models_latest.json, brief_seat.sh:24, the briefs folder (grep for ports), gh GETs on datasecau/HPSM-POC and the analysis repo CLARIFICATIONS.md, tmux list-panes, lsof, df. Two first attempts failed on my own shell slips (zsh `$H:path` modifier and a hook blocking `==`); one `git cat-file` on the stale local checkout was a read verb. Wrote only the two files plus one scratch list (kits.txt, p36.txt, h111.txt) in the session scratchpad. No decision_queue, no ledger/scoreboard/staged-briefs read.
