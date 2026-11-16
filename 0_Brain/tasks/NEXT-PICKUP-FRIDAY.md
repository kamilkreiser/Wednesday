---
date: 2026-11-17
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, boot #4 (Fable 5.2), handover block written at the end of the boot (see the 2026-11-17 note's "Boot #4" block for stamps)
supersede: replace wholesale; previous = NEXT-PICKUP-FRIDAY.md.pre-1117-boot4 (the overnight seat's block), read on demand only
---

# NEXT PICKUP — FRIDAY

**The tree is at `/Volumes/Laptop-DEV/FRIDAY` (machine: Kamils-MacBook-Pro).** Quote every path. This seat boots on Fable.

## 🔴 FIRST ACT — CoAgent (General/Claude to Claude): three pieces to check and merge; NO new build work without Kam's word

**The overnight build grant is DEAD** (its event happened: Kam reviewed at 07:26 on 2026-11-17). What is authorised now is exactly his card answers of 07:26-07:33, recorded with his notes and Friday's readings in `0_Brain/reference/2026-11-16_claude-to-claude/05_kam-rulings-2026-11-17.md` (read it whole): a third independent check for AUDIT, DAEMON and POLICY after their fixes, then the merge method. **Whether building continues past those three is ASKED on card `general-c2c-morning-plan-1117`** (a = today, b = stop after the three, c = until he says stop). Until he answers: finish, check, merge the three; start nothing new.

**FIRST CHECK AT ANY BOOT: `tmux list-panes -a` against the pane ids below.** On 2026-11-17 a launch at 07:39:40 REPLACED the fleet session and killed three seats mid-step; the new seat found out only by listing panes (ledger row 2026-11-17; mechanism OWED below). If a seat below is gone: read its STATUS last line and `git status` in its worktree, write a resume addendum that changes no rule, relaunch.

Project: `/Volumes/Laptop-DEV/!CODING/Claude to Claude/coagent/` (repo `2_Project_Files`, remote kamilkreiser/coagent, private; Friday reads the remote with `3_Access_Keys/coagent_github_deploy_rw`). STATUS files: `coagent/5_Project_History/STATUS_*.md`. Briefs and addenda: `2_Project_Files/friday/briefs_drafts/2026-11-1[67]_coagent_*`. Gate verdicts and tests: `0_Brain/reference/2026-11-16_claude-to-claude/m1_review/`. Launch line (worked at boot #4): `cockpit.sh add "General/CoAgent-<NAME>" "bash '<general_seat.sh>' '/Volumes/Laptop-DEV/!CODING/Claude to Claude' '<FRIDAY>/4_Credentials/clients/general' '<absolute brief path>' opus"`. A seat has no mailbox: commit and push the brief, then the prompt names it (a pointer to a LATER addendum is typed with `tmux send-keys`; `cockpit.sh say` refuses). Idle wakes for a seat holding at READY by design: `wake_ack.sh %<pane id>`. Other projects' git: read verbs only (`git -C … worktree list` is refused by the hook).

**THE METHOD (keep it):** seat ends at its READY line -> independent tier-1 gate (Agent tool, `model: opus`, findings only, own clone in the scratchpad) -> on GO: the seat merges origin/main INTO its branch (never rebase; Cargo.lock regenerated), Friday's own check in a clean clone (`git clone --branch`, `scripts/check.sh`, cmp of gate files) -> merge GO for an exact SHA, fast-forward only -> Friday verifies with ls-remote and her own check.sh on main. Never merge on a seat's own figures. A NO GO at this third check goes to Kam as a card with the finding in plain words: no fourth round without his word.

0. **UPDATE (same seat, after Kam's "yes, keep building today"; stamps in the 2026-11-17 note):** the build grant is LIVE until the END OF TUESDAY 2026-11-17 (top row of EXPIRING-GRANTS); the repository STAYS PRIVATE until the beta (his card answer c; item 6 below is closed, the sweep report is kept for the beta). Kam asked: "update me when the checks finish". Two more seats run: pane %12 `General/CoAgent-ROSTER` (Opus, branch m3-roster, brief `…_M3_ROSTER_brief.md`, last line `READY FOR QA M3-ROSTER`) and pane %13 `General/CoAgent-RELAYID` (Opus, branch m1-relay-identity, brief `…_M1_RELAY_IDENTITY_brief.md`, last line `READY FOR QA M1-RELAY-IDENTITY`); each then gets a tier-1 gate. Design for the morning rulings: `reference/2026-11-16_claude-to-claude/06_design-addendum-rulings-2026-11-17.md` (13 INTERPRETATIONS in its section 10; three are open cards: i2-who-hands-invite, i5-starter-gone, i1-limit-fixed, all -1117; the rendezvous service is UNDECIDED). Lane plan: `briefs_drafts/2026-11-17_coagent_LANE-PLAN_today.md` (what may start as AUDIT, DAEMON, POLICY merge; its section 6 = the limit-of-4 merge hazard for the daemon and audit crates).
1. **main = 18005d6** (measured 03:0x; unchanged at boot #4 by `for-each-ref`).
2. **AUDIT** (branch m3-audit, 882e094, pushed; seat gone, nothing further needed from it): THIRD gate running as an in-session agent of the boot #4 seat; verdict file `m1_review/gate_M3_AUDIT_r3_verdict.md`. If that file is missing or has no VERDICT first line and you are a new seat, the gate died with the old seat: re-commission (the prompt's inputs: r2 verdict, audit addendum 2, STATUS_M3_AUDIT.md section "ADDENDUM 2", reference tests `gate_audit_tests/`, `gate_audit_tests_r2/`). On GO: a short merge seat (the AUDIT pane is gone) or a relaunched AUDIT seat does the merge-in; AUDIT changes coagent-crypto, so after it merges every other open branch merges main again and re-runs its suite.
3. **POLICY** pane %6 `General/CoAgent-POLICY` (Opus, pid 86580): resuming addendum 5 under addendum 6 (20 uncommitted files inherited; it must judge them before trusting them). Last line will be `READY FOR KAM M2-POLICY r5` -> commission the third gate (inputs: r4 verdict, addenda 5 and 6, its STATUS sections, `gate_policy_tests_r4/`; main job: confirm NO shell text lowers a decision below T3, the owner exact-command list parses nothing, both volume kinds).
4. **DAEMON** pane %7 `General/CoAgent-DAEMON` (Opus, pid 86645): resuming addendum 2 under addendum 3 (two unpushed commits 95f8c3a, ba9677a and 6 uncommitted files inherited). Last line will be `READY FOR KAM M1-DAEMON r3` -> commission the third gate (inputs: r2 verdict, addenda 2 and 3, its STATUS section, `gate_daemon_tests_r2/`).
5. Watchers (one per seat, background tasks of the boot #4 seat) die with that seat: a new seat arms its own.
6. **Pre-publication sweep** (Kam ruled n6 = "Open from the first commit"): an in-session agent is sweeping every branch and the whole history; report `0_Brain/reference/2026-11-16_claude-to-claude/prepub_sweep_2026-11-17.md`. When it lands: read it, then give Kam the result and the LINK to the repository's visibility setting in chat (his click; steps for his hands go in chat). Blocking findings are fixed by a seat first, or carded if they need his call (history rewrite is irreversible: his).
7. Rulings not yet in any seat's brief (owed when the lane is briefed, only after his answer on the morning card): n1 limit 4, n2 member proposes and the starter approves, n5 guided choice at connection time, relay saved identity (merged relay crate), n8 one beta. Windows: waits for his machine on Friday 2026-11-20; Mac first (n4).

## OWED (Friday)

- 🔴 **A launch must not replace a fleet session that holds live agent panes** (ledger 2026-11-17): find what ran at 07:37-07:39 (a new wake_watch armed 07:37:49; session created 07:39:40), then make the launcher refuse or re-attach, with an arm. Shared tooling: claim first, mail both sisters.
- 🔴 **`tools/safe_pull.sh` loses rulings** (ledger 2026-11-17, first row of the night): per-id merge, ruled beats open, with a failing arm. UNTIL FIXED: after ruling any card run safe_pull + `git push` in the same action and recount `decision_queue.sh list open`.
- The n5 card's tile-hide was not re-run after its live write failed once: `kam_rulings_today.sh` will show it if his board still has it.
- **Live board filter fix: committed (468f35c235), NOT deployed.** Deploy asked of Wednesday by mail 2026-11-16; no reply in friday-laptop-agent@ at boot #4. Until confirmed say "committed, not live", and a card's HTTP 201 is storage, not Kam's sight.
- Sister acks still outstanding (no replies at boot #4): inbox-scope hook change (e30563fa5d), launcher Fable change, Kam's 16:37 Composer ruling to Tuesday.
- Wrap step 3a (doctor/PORTABILITY) for the machine-local items: the CoAgent deploy key, `4_Credentials/clients/general/`, `general_seat.sh`'s reliance on them.
- Untracked backup `2_Project_Files/dashboard-cloud/app/static/index.html.pre-1116-2305-hiddenfilter` (keep until the deploy is confirmed).
- From 10-16, not carded: Spotlight Privacy + Disk Utility First Aid on Laptop-DEV; wordsplit hook for unquoted `$(ls …)` in a `for` list.
- Stale OPEN claims in `wed_claim.sh list` on this laptop (09-08 … 11-06): verify each is Friday's, then release.
- Linear: WED-48 and WED-147 overdue; WED-162 (CoAgent, Backlog) needs last night's and this morning's state.
- Not read at boot #4 (first act was live): yesterday's note, INDEX.md head, the sister ledgers' headlines, the 16 gate verdict files whole.

## Standing facts a cold seat needs

- Friday drives NO Datasec and NO Secuura project (Tuesday's since 10-15). Friday holds only `General/Claude to Claude — Friday (laptop)` (claim OPEN since 2026-11-16).
- Poller `live_chat_poll.sh --seat friday` is armed by the launcher; receipt every board message on the panel when read. `kam_rulings_today.sh` prints TAPPED-BUT-OPEN: rule those at once.
- Hooks that will refuse you: any `cd`; git write verbs outside this tree; a note in the same turn as another tool call; a note whose body has a receipt verb (even the tool's own word followed by a colon) without `--receipt`; reading two inboxes in a loop; `--override-prior-rulings` before a plain add was refused.
- Never type a clock: `date` or the note tool's own stamp (boot #4 typed "07:5x" three times in a reference file and had to remove them).
- Sourcing `_live_board.sh` works only under `bash -c`, not from zsh.
- By-tier boot digest is about 288K tokens: it cannot be read whole in one turn. Read lines 1-587 and every `## ` headline; open a lesson when its rule fires. Statusline after the load: read it from the pane.
- Never run `tools/panel_sync.sh` bare. Push own commits with `git push` after `safe_pull.sh`.
- The prior-ruling gate refuses on generic words from unrelated cards; run the plain add, read the matches, then override with the reason in the BLUF.
