---
date: 2026-11-16
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, boot #3 (Fable 5.2), handover block written 23:14 on 2026-11-16 while the overnight CoAgent build runs
supersede: replace wholesale; previous = NEXT-PICKUP-FRIDAY.md.pre-1116-2314 (the 22:5x wrap), read on demand only
---

# NEXT PICKUP — FRIDAY

**The tree is at `/Volumes/Laptop-DEV/FRIDAY` (machine: Kamils-MBP).** Quote every path. This seat boots on Fable (launcher change 22:5x held: statusline "Fable 5.2" at 22:59).

## 🔴 FIRST ACT — the overnight CoAgent build (grant ends at Kam's MORNING REVIEW, Tue 2026-11-17)

**Handover block refreshed 01:4x on 2026-11-17 by the launching seat (ctx about 48%). State lives in `0_Brain/daily_friday/2026-11-17.md`; read it whole.**
Grant: top row of `tasks/EXPIRING-GRANTS.md` + `learnings/2026-11-16_grant-build-coagent-overnight-until-the-morning-review.md`. CoAgent only. No deploy, publish or spend. When Kam reviews, the grant is DEAD: seats finish their step and report; further build work is re-asked.

Project folder: `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/` (repo `2_Project_Files`, remote kamilkreiser/coagent, private). STATUS files in `coagent/5_Project_History/`. All briefs and addenda: `2_Project_Files/friday/briefs_drafts/2026-11-1[67]_coagent_*`. Launch a seat with `2_Project_Files/friday/general_seat.sh` (see the daily notes for the exact `cockpit.sh add` line). A seat has no mailbox: the artefact behind a pointer is a committed, pushed brief file, and the pointer is typed with `tmux send-keys` (`cockpit.sh say` refuses).

1. **M0 (spikes): DONE and accepted.** main = 13bd10e (scaffold). Friday re-ran Gate G1, G2's blocks, group G1, G3, U6. Open from M0: every native-Windows spike (W1 is blocking for Windows; needs a Windows machine), C2 tunnels, C3 Linux rig.
2. **M1, two seats, each RETURNED from its tier-1 gate (round 1), NOT merged:**
   - pane %7 `General/CoAgent-CORE`, Opus, branch `m1-core` (was 3f60cf4): gate GO WITH NOTES, returned by Friday for 11 surviving mutants + F1/F3/F9/F10/F12-F16. Ends at last line `READY FOR QA M1-CORE r2`.
   - pane %8 `General/CoAgent-RELAY`, Sonnet, branch `m1-relay` (was 65fcc1b): gate NO GO (G1, G2 Major). Ends at `READY FOR QA M1-RELAY r2`. This was NO GO round 1; the cap is two rounds on one class, a third needs Kam on a card.
   - Verdicts + the gates' tests: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/`.
   - NEXT when a seat writes r2: commission a DELTA gate (Agent tool, `model: opus`, findings only, own clone in the scratchpad, project tree read-only; the round-1 gate prompts are in this session only, so rebuild from the verdict files: re-run check.sh, the red controls, the gate's own tests, re-apply the surviving mutations). On GO: brief ONE seat to merge m1-core then m1-relay into main (Cargo.lock conflict: regenerate, never hand-merge), run check.sh on main, push. Then M1's integration step (daemon wiring, MCP send/inbox/wait, two-terminal exchange through the relay) as a new brief.
3. **M2 first part:** pane %13 `General/CoAgent-POLICY`, Opus, branch `m2-policy`, new crate `coagent-policy` (decision core of the gate). Ends at `READY FOR QA M2-POLICY`; then a tier-1 gate as above.
4. A background watcher belongs to the seat that armed it. A NEW Friday seat has none: read the three STATUS last lines and the panes by hand, then arm watchers (pattern in the daily note).
5. **For Kam in the morning (Friday tab):** design revision PDF is already posted (bf-dab6713443bd6) with 8 cards (n1-n8, confirm he can SEE them); the 00:4x overnight update is posted (bf-006dd76f4d219). STILL OWED to him: a morning summary card per the 10-23 rule (what was built, gate results in plain words, counts of what waits on him), the three wire-format design questions from CORE, the relay certificate-persistence decision (gate N8), the F2 decision (attempt cap keyed on the key), commit identity default, the `claudeInChromeDefaultEnabled = False` side effect in this seat's shared config, and the model suggestion per his 22:50 rule.

## Kam's rulings on CoAgent (all 17 cards ruled; store has 0 open at 23:05)

a: name CoAgent, licence Apache-2.0 free, reads ask-on-first-read, trust 60 min / 8 h, identity device keys (note: "Phase 2 should have multiple options"), browser agent embedded terminal, audit hashes + previews, Rust core + TS console, nightly tests on smallest model, build model Fable for M0 then routing table, repo new private under personal GitHub, go.
**b (depart from the design):** groups and observers in phase 1; native Windows in phase 1; NO public relay (self-host only); no outside review (unreviewed beta indefinitely).
**c:** old v0.4.4 download and its credentials: leave as is (Friday disagreed once on the panel; ruling stands; do not raise it again).

## Repo and key (MEASURED 23:09)

`git@github.com:kamilkreiser/coagent.git`: exists, empty, private (anonymous 404). Deploy key pair generated by Friday at Kam's request: `3_Access_Keys/coagent_github_deploy_rw` (+ `.pub`) in THIS tree (gitignored, machine-local: NOT on the other machines). It authenticates as kamilkreiser/coagent. Write access is unproven until the seat's first push.

## OWED (Friday)

- **Live board filter fix: committed (468f35c235), NOT deployed.** Deploy asked of Wednesday by mail (thread 0f4782ef…); Tuesday informed (2c899d16…). Check friday-laptop-agent@ for her confirmation; until then say "committed, not live".
- Sister acks still outstanding: inbox-scope hook change (e30563fa5d), launcher Fable change (b684789c / ced43887), Kam's 16:37 Composer ruling to Tuesday (f0f1f881…).
- Wrap step 3a (doctor/PORTABILITY) for the new machine-local items: the deploy key above, `4_Credentials/clients/general/`, and `general_seat.sh`'s reliance on them.
- Untracked backup `2_Project_Files/dashboard-cloud/app/static/index.html.pre-1116-2305-hiddenfilter` (the deploy zip excludes `*.pre-*`; keep until the deploy is confirmed, it is the red arm of 09f).
- From 10-16, not carded: Spotlight Privacy + Disk Utility First Aid on Laptop-DEV; wordsplit hook for unquoted `$(ls …)` in a `for` list.
- Stale OPEN claims in `wed_claim.sh list` on Kamils-MBP / Kamils-MacBook-Pro (09-08, 09-25, 10-10, 10-26, 10-29, 11-03, 11-06): verify each is Friday's, then release.
- Linear WED-48 and WED-147 overdue; WED-162 is the CoAgent issue (update it with tonight's state).

## Standing facts a cold seat needs

- Friday drives NO Datasec and NO Secuura project (Tuesday's since 10-15). Friday holds only `General/Claude to Claude — Friday (laptop)`.
- Poller `live_chat_poll.sh --seat friday` is armed by the launcher; receipt every board message on the panel when read. `kam_rulings_today.sh` prints TAPPED-BUT-OPEN: rule those at once.
- Hooks that will refuse you: any `cd`; `git -C $VAR` with a write verb (write the path literally); a note or panel message in the same command as a send; reading two inboxes in a loop; receipt verbs in a note without the send's own output.
- By-tier boot digest ~700 KB: read every headline, open a lesson when its rule fires. ctx 13% after the load.
- Never run `tools/panel_sync.sh` bare. Push own commits with `git push`.
- The prior-ruling gate refuses on generic words from unrelated cards; override with the reason in the BLUF after reading what it matched.
