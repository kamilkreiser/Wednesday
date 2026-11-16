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

**Handover block refreshed 03:3x on 2026-11-17 by the launching seat (ctx 65%). State lives in `0_Brain/daily_friday/2026-11-17.md`; read it whole (it is long: every gate result, ruling and merge is there with its evidence).**
Grant: top row of `tasks/EXPIRING-GRANTS.md` + `learnings/2026-11-16_grant-build-coagent-overnight-until-the-morning-review.md`. CoAgent only. No deploy, publish or spend. When Kam reviews, the grant is DEAD: seats finish their step and report; further build work is re-asked.

Project: `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/` (repo `2_Project_Files`, remote kamilkreiser/coagent, private; Friday reads the remote with `3_Access_Keys/coagent_github_deploy_rw`). STATUS files: `coagent/5_Project_History/STATUS_*.md`. Briefs and addenda: `2_Project_Files/friday/briefs_drafts/2026-11-1[67]_coagent_*`. Gate verdicts and the gates' tests: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/`. Launch a seat with `2_Project_Files/friday/general_seat.sh` through `cockpit.sh add` (exact line in the daily note). A seat has no mailbox: commit and push the brief, then type the pointer with `tmux send-keys` (`cockpit.sh say` refuses). Idle wakes for a seat holding at READY by design: `wake_ack.sh %<pane id>` (the pane NAME is refused).

**THE METHOD THAT WORKED TONIGHT (keep it):** build seat ends at READY -> independent tier-1 gate (Agent tool, `model: opus`, findings only, own clone in the scratchpad, told to write failing tests and run mutations) -> return addendum with the gate's tests copied into `m1_review/` -> seat adds the gate tests UNCHANGED first, fixes, reports -> delta gate -> short list -> Friday's own merge check in a clean clone (`git clone --branch`, `scripts/check.sh`, cmp of gate files) -> merge GO for an exact SHA, fast-forward only -> Friday verifies the remote with ls-remote and re-runs check.sh on main. Every first-round gate found real faults (2 Majors relay; 11 surviving mutants core; 2 Blockers policy). Never merge on a seat's own figures.

1. **main = 18005d6 (MEASURED 03:0x: ls-remote + Friday's own check.sh: 250 passed, 0 failed, 5 ignored).** Merged: M0 scaffold, M1 CORE (coagent-proto, -crypto, -roster), M1 RELAY (coagent-relay, -ipc, -cli). CORE and RELAY panes closed.
**UPDATE 06:1x (ctx 80%, in the rotation band):** POLICY reached `READY FOR QA M2-POLICY r4` (head 9170425) and DAEMON reached `READY FOR QA M1-DAEMON r2` (head bb92225). A delta gate for EACH was commissioned by the launching seat as an in-session agent: verdicts `m1_review/gate_M2_POLICY_r4_verdict.md` and `m1_review/gate_M1_DAEMON_r2_verdict.md`. If you are a NEW seat and either file is missing or has no verdict on its first line, the gate died with the old seat: re-commission it (inputs: the previous verdict, the addendum, the builder's ADDENDUM section in its STATUS, the reference test copies in `m1_review/`). POLICY r4 is the SECOND gate round on the scan class: a NO GO there is the cap -> card Kam with the gate's answer on PLAIN versus all-T3, no further round. AUDIT: seat resumed after a 20-minute hang (interrupted by Friday at 06:08); still ends at `READY FOR KAM M3-AUDIT r3`, no gate until Kam rules its card.

2. **Seats at 05:4x — THREE seats, each working a gate RETURN; NO gate agent is running (a clean boundary for a rotation). Read each STATUS last line and pane first; arm a watcher per seat (pattern in the daily note).**
   - pane %13 `General/CoAgent-POLICY`, Opus, branch `m2-policy`: recogniser REMOVED after two NO GOs (verdicts `gate_M2_POLICY_verdict.md`, `_r2_`); round-3 gate (`gate_M2_POLICY_r3_verdict.md`) confirmed the removal is real and found NO wrong allow, but the raise-only SCAN of shell text is evadable by shell expansion (braces, attached option arguments, look-alike command names) = first NO GO on that class. Now on addendum 4: a command containing anything the shell rewrites is OPAQUE = T3 (red, every time, not batchable, not grantable); only PLAIN literal-word commands get the scan, with substring matching; the seat must prove the plain set by printing strings through real zsh and bash; suite must pass on case-sensitive AND case-insensitive volumes. Ends at `READY FOR QA M2-POLICY r4` -> commission a delta gate (rule on changed gate assertions; try to get an opaque construct classified PLAIN; re-run its own property test; mutations). If that gate is NO GO on the scan class again = the cap: card Kam, do not run a further round.
   - pane %16 `General/CoAgent-AUDIT`, Opus, branch `m3-audit`: delta gate (`gate_M3_AUDIT_r2_verdict.md`) = one Major (a peer can fill an honest member's store), SECOND NO GO on that class = the cap. Seat is fixing it as a class (addendum 2). Its last line will be `READY FOR KAM M3-AUDIT r3`. **Do NOT commission a third gate and do NOT merge until Kam rules card `general-c2c-audit-log-third-check-1117`.** The branch carries the one authorised edit to merged `coagent-crypto` (five `SignDomain` values, commit c407fe7; the gate ruled it exact and re-ran the core's red controls: 65 of 65).
   - pane %19 `General/CoAgent-DAEMON`, Opus, branch `m1-daemon`: gate (`gate_M1_DAEMON_verdict.md`) = NO GO, 4 Majors, no Blocker; peer-text containment and pairing wiring HELD under a hostile paired peer. Seat on addendum 1 (a live channel replaced only after the new handshake completes and the peer proves the keys; security state in its own file; inbox bounded, paged and acknowledged = at-least-once to the agent; cancelled wait). Ends at `READY FOR QA M1-DAEMON r2` -> delta gate. NO GO round 1 of 2.
   - Before any merge: the seat merges origin/main INTO its branch (never rebase), Cargo.lock regenerated not hand-merged, root Cargo.toml member lines from both sides kept; Friday's own check.sh in a clean scratch clone (`git clone --branch`, literal scratch path); fast-forward of main to an exact SHA; ls-remote + Friday's check on main after. AUDIT changes coagent-crypto: after it merges, every other open branch merges main again and re-runs its suite.
   - Gate verdict files Friday has read only through the gate's final report, not whole: every `_r2_`/`_r3_` file and `gate_M1_DAEMON_verdict.md`, `gate_M2_POLICY_verdict.md`, `gate_M3_AUDIT_verdict.md`. The seats were told to read each whole.
   - 13 CoAgent cards are open for Kam (n1-n8; terminal-commands-gate, verify-words-tries, relay-identity-restart, windows-testing, audit-log-third-check, all -1117). After ANY safe_pull compare `decision_queue.sh list open | grep -c general-c2c` with 13 minus what he has ruled (the union defect, OWED below).
   - Night report posted to Kam 04:2x (bf-798a8ea547715). When he is up: one short update with what changed since (policy rounds 3-4, audit cap card, daemon verdict), then the 10-23 morning fleet-activity card with counts.
3. A watcher belongs to the seat that armed it; a NEW Friday seat has none. When a combined watcher exits on one seat, re-arm for every other seat it covered in the same action (missed once at 03:17).
4. **STILL OWED TO KAM (Friday tab) before or at his review:** ONE morning summary (what is on main, what each gate found in plain words, what is still open), and cards for the decisions the night produced, each with a default: three CORE wire-format questions + the new `decline` step; verify-words bound is five guesses per pair (accept, or cap attempts at two) and the two unlimited cases; relay certificate persisted or regenerated per start; relay limits behind a tunnel (16 live sessions per address; cut versus throttle) before any tunnel recipe; POLICY: build/task files never grantable, git always asks, recursive searches always ask, approvals cover subagents; commit identity default; `claudeInChromeDefaultEnabled = False` side effect in this seat's shared config; no Windows machine means every Windows item is untested (W1 blocking); model suggestion per his 22:50 rule. Earlier posts: design revision PDF bf-dab6713443bd6 with cards n1-n8 (confirm he can SEE them); overnight update bf-006dd76f4d219.

## Kam's rulings on CoAgent (all 17 cards ruled; store has 0 open at 23:05)

a: name CoAgent, licence Apache-2.0 free, reads ask-on-first-read, trust 60 min / 8 h, identity device keys (note: "Phase 2 should have multiple options"), browser agent embedded terminal, audit hashes + previews, Rust core + TS console, nightly tests on smallest model, build model Fable for M0 then routing table, repo new private under personal GitHub, go.
**b (depart from the design):** groups and observers in phase 1; native Windows in phase 1; NO public relay (self-host only); no outside review (unreviewed beta indefinitely).
**c:** old v0.4.4 download and its credentials: leave as is (Friday disagreed once on the panel; ruling stands; do not raise it again).

## Repo and key (MEASURED 23:09)

`git@github.com:kamilkreiser/coagent.git`: exists, empty, private (anonymous 404). Deploy key pair generated by Friday at Kam's request: `3_Access_Keys/coagent_github_deploy_rw` (+ `.pub`) in THIS tree (gitignored, machine-local: NOT on the other machines). It authenticates as kamilkreiser/coagent. Write access is unproven until the seat's first push.

## OWED (Friday)

- 🔴 **`tools/safe_pull.sh` loses rulings:** its decisions.json union took upstream's OPEN copy over a locally RULED one for twelve cards on the night of 11-16/17 (repaired by re-ruling; daily note 2026-11-17, 04:2x entry; ledger row). Fix: per-id merge, ruled beats open, newest ruled_ts wins, with an arm that fails on the old behaviour. Shared tooling: claim first, mail both sisters. UNTIL FIXED: after ruling any card, run safe_pull + `git push` in the same action, and after every safe_pull compare `decision_queue.sh list open` with what should be open.
- Twelve more CoAgent cards are open for Kam: n1-n8 (design revision) and four from the night (`general-c2c-terminal-commands-gate-1117`, `-verify-words-tries-1117`, `-relay-identity-restart-1117`, `-windows-testing-1117`). Confirm he can SEE them.

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
