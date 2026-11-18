#!/usr/bin/env python3
"""Writes replay_report.md from replay_sample.json (replay_select.py) + the grades below. Counts are computed, never typed.
Re-run: python3 replay_select.py > /dev/null && python3 replay_report_build.py"""
import json, os, collections
HERE = os.path.dirname(os.path.abspath(__file__))
S = json.load(open(os.path.join(HERE, "replay_sample.json")))
C, CE, P, M, LO, NL = "COVERED", "COVERED-ENFORCED", "PARTIAL", "MISSING", "LEDGER-ONLY", "NO-LESSON"
G = {  # row number in sample order -> (grade, gist <= 12 words, card line or missing clause)
1:(CE,"Panel tool refused a sign-off sentence repeated after each merge","chat_reply.sh repeat guard, lines 186-205 (opened). No index row and no lesson: the rule lives only in the tool"),
2:(C,"Typed a pointer and Enter in one command over ghost text","use-the-fleets-own-tool: 'Taps go through cockpit.sh say with --mail, never raw tmux send-keys'. Absent from the pane moment list (first trigger is tooling)"),
3:(C,"Permission gate keyed on tool names missed a second command tool","a-gate-keyed-on-tool-names: 'define it by capability... Unknown tools get the strictest tier'"),
4:(C,"Two seats sat at READY; no idle wake reached Friday","an-enforcement-you-must-arm: 'Agent silence is a question, not an answer'. The sharper clause (read each STATUS last line at every checkpoint) is in the ledger row only"),
5:(C,"Typed a clock by hand into two durable files","i-read-representations: 'generate timestamps'"),
6:(C,"Wait condition was already true, so the check could not fail","a-check-that-cannot-fail + exercise-mechanisms: 'prove both the fire path and the quiet path'"),
7:(C,"Build seat committed fixtures recorded from the real drive","recorded-fixtures-come-from-a-scratch-tree"),
8:(C,"Rotation failed; session replaced; three seats killed mid-step","a-rotate-run-inside-its-own-pane: 'Two minutes after any rotation, list panes and read rotate.log'. No rule or tool refuses a launch that replaces a session holding live panes (tool gap, stated in the row)"),
9:(NL,"Pull re-opened twelve ruled cards; store not pushed before pull","No lesson and no index row. Third row of this family in the sample (27, 37). Rule in the ledger: commit and push the card store before any pull. safe_pull.sh has no 'ruled beats open' merge (opened: 0 hits for 'ruled')"),
10:(C,"Commissioned a recogniser of safe shell commands; gates broke it twice","a-recogniser-of-safe-shell-commands-cannot-be-finished"),
11:(C,"Told Kam cards were visible from HTTP 201, not his view","decisions-go-on-the-fleet-activity-panel: 'A post's HTTP 201 proves storage; if he cannot see a card, ask for the board footer line first'"),
12:(C,"Reply went to terminal while his board post went unreceipted","confirm-receipt-on-the-chat-board + acknowledge-panel-instructions-on-receipt"),
13:(P,"Ran panel_sync.sh bare three times; it never returns","Missing clause, lesson rule 4: 'A tool's header comment names the incident and the ledger weight. Read it — it tells you what breaks when you skip it.' Fix row given"),
14:(CE,"Boot commands used echo ====, cd, word-split loop; all refused","pretooluse_zsh_wordsplit.sh and pretooluse_no_cd.sh: both refused this test's own first two commands (observed live). Neither rule has an index row"),
15:(C,"Shared hook composed the inbox name and refused Friday's own inbox","a-seat-scoped-hook: 'never hardcode the seat name; resolve it from the tree... and test every tree'"),
16:(C,"Watcher could not match brief's final line; checked after launch","exercise-mechanisms-before-arming: 'prove both the fire path and the quiet path' before arming. The brief_seat.sh refusal the row calls due is not built (file not found in fleet/)"),
17:(LO,"Typed a merge SHA into the note from feel","Card line (i-read-representations) says take the fact from a same-action read; she HAD read it and retyped it. 'Paste, never retype' for ids is in the ledger row only (lesson: 0 hits for sha)"),
18:(C,"Handover described a seat by its expected line, not measured","i-read-representations: 'never... my earlier prose'"),
19:(C,"Ruled 'no extension needed' on a builder's unmeasured STATUS line","a-premise-under-a-question: 'or sending a claim: verify each load-bearing premise at source; mark agent prose reported, unverified'"),
20:(C,"Four asks for Kam listed in reports, none carded","kam-items-on-fleet-activity: 'When anything needs Kam: post a fleet-activity card in the same action, never chat only'"),
21:(M,"git status in another project's repo rewrote its index file","Listed as enforced by pretooluse_no_cd.sh; the hook ALLOWS status (line 145), so it would not have refused. The card cuts this rule at 120 chars. '--no-optional-locks' is in the ledger row only. Fix row given"),
22:(CE,"Passed the override flag before reading the prior-ruling matches","decision_queue.sh lines 365-385 refuse an override with no plain refusal in the last hour (opened); card line a-prior-ruling-gate-refusal also states it"),
23:(LO,"Usage gate read the coordinator's gauge; seats ran on old account","No line. Rule (after an account switch launch ONE seat, read its statusline) is in the ledger row only; usage_gate.sh still has no per-seat config read (opened: 0 hits)"),
24:(C,"Watcher written into handover, never armed; idle wake acked unread","an-instruction-to-wait: 'Before acking an idle wake on remote work, read a figure that moves' + a-promise-is-not-a-mechanism"),
25:(LO,"Reconcile run only at percent checkpoints; twelve rulings unread 3.5 hours","Card line equals the lesson ('at each checkpoint and before any handover or wrap'). 'With every card add and panel message' is in the ledger row only. Fix row given"),
26:(C,"Records repo five commits unpushed while STATUS said committed","a-census-complete-over-a-frame: 'ask what lies outside it (other language, directory, repo, keychain)'"),
27:(CE,"Hand autostash pull swept Friday's own records into a stash","pretooluse_no_autostash.sh refuses a hand autostash pull (opened; wired in .claude/settings.local.json). No index row"),
28:(C,"safe_push with no paths read 'HEAD == origin' as success","a-check-that-cannot-fail: 'silent success are suspects... check the artefact, not the intent'"),
29:(CE,"Invented cockpit verb used as filler; hook refused the call","pretooluse_cockpit_verb.sh (opened; reads valid verbs from cockpit.sh usage)"),
30:(C,"Launched a seat while the capacity line read FULL","track-agent-capacity: 'If FULL say which limit and do not launch'. Nothing refuses it (brief_and_launch.sh: 0 hits for FULL)"),
31:(C,"Linear comments(last:1) taken as newest comment","a-pagination-default-is-a-selector: 'comments(last:N) returns the OLDEST'"),
32:(C,"Card named a field by identifier; it held personal data","a-premise-under-a-question: 'verify each load-bearing premise at source'. 'Name a field by what it holds' is ledger-only. Rule is absent from the card moment list"),
33:(C,"Told Kam what a PR does from its ticket title","a-premise-under-a-question + do-not-guess-a-comparison"),
34:(C,"Instructed an env var without reading how the tool uses it","mental-model-not-source-of-truth: 'validate any named file, path, flag... against the live source'"),
35:(C,"Run count in a brief taken from prose, not gate line","i-read-representations (now on the card body in full)"),
36:(C,"Fixed-string grep of a whole sentence read zero","a-false-absence: 'run a control that would be non-zero'. The control is what caught it"),
37:(C,"Rebase routine checked out the card store, hiding two rulings","never-delete: 'checkout -- over work'. Not enforced: pretooluse_no_rm.sh covers rm, git rm, find -delete, unlink only (opened)"),
38:(C,"Brief ordered removal of other seats' folders, citing a rule's name","regenerable-build-leftovers: 'deletes ITS OWN... other seats' trees or >1 project = card for Kam'"),
39:(C,"Note and a file edit sent in one call","a-note-is-its-own-message. Enforced on the Tuesday seat only (hook line 44 exits unless WED_AGENT=tuesday)"),
40:(C,"Seat launched on the default model; brief named another","sonnet-trials: 'Set a seat's model AT LAUNCH (SEAT_MODEL_ENV)'"),
41:(C,"Launch held on a condition with nothing to wake; duration invented","a-promise-is-not-a-mechanism + read-the-clock: 'Compute durations from two clock reads'"),
42:(C,"Note said 'answered' in the same call; the ack had refused","a-note-is-its-own-message: 'Never bundle a note with a wake ack'"),
43:(P,"Push gate by pgrep raced; two seats pushed together","Missing clause, lesson EXTENSION 2026-09-22: 'PUSH-WINDOW LOCK: an advisory mkdir lock OUTSIDE every worktree... Built into the push tool, not remembered.' The line says only 'push-window lock'. Fix row given"),
44:(C,"Hash quoted in a brief without the command that made it","i-read-representations: 'name the instrument'"),
45:(C,"Told Kam the tunnel was up from a two-day-old pickup","mental-model-not-source-of-truth + i-read-representations"),
46:(LO,"Ruled on a destructive guard without tracing the column's writers","i-endorse line covers endorsing unread artefacts; 'name every writer of the column' is in the ledger row only (lesson: 0 hits for writer)"),
47:(CE,"Tap and its note line in one command, fifth time","receiptguard.py clause 1 (opened)"),
48:(C,"Attestation copied from predecessor; clock typed into a queue file","i-read-representations: 'generate timestamps'; board_count.sh's control caught the count"),
49:(C,"Empty ctx read interpolated into mail as 'ctx: .'","a-false-absence: 'When a check returns zero or empty: before it enters a sentence...'"),
50:(CE,"Routing token mid-subject; send refused","send_brief.sh line 163 (opened)"),
51:(LO,"Expected figure in a GO without the build state it needs","a-two-answer-question line has 'In briefs say or neither'; 'an expected figure carries its environment' is in the ledger row only (lesson: 0 hits)"),
52:(C,"New guard condition refused a legitimate two-key PR","red-proof-arms: 'list every legitimate shape of the real event... Run the shapes through the rule text'"),
53:(C,"Ghost tap text at a seat's prompt, third time in a night","ghost-suggestions-in-panes + a-ghost-suggestion-is-dangerous"),
54:(C,"tail -1 over a live-appended file compared the wrong ticket","surprising-measurements-are-selector-errors: 'print what the selector picked'"),
55:(C,"Local model sat idle while attention was on another workstream","if-something-blocks (now seats=all): 'never idle Ornith' + never-idle-the-gatekeeper (wednesday)"),
56:(P,"Brief required a red cell that could only fail by throwing","Missing clause, lesson rule 4: 'Before making any instrument a REQUIRED leg, establish it can REACH the change.' Fix row given"),
57:(C,"Drafter predictions off by a line; carried into a gate brief","git-topology: 'line number... read it in the same action or attribute it to the agent who read it'"),
58:(CE,"Own merge script hit the zsh list word-split trap","pretooluse_zsh_wordsplit.sh (refused this test's own command live). Graded on the visible defect; the row text was read to 1,100 chars"),
59:(C,"Apologised to Kam for a loss that had not happened","decisions-held-narration-drifted: 'No quantity or characterisation reaches Kam without its measurement'"),
60:(C,"Told Kam 'one action'; it was three plus a possible bill","measure-the-whole-interface + a-premise-under-a-question"),
61:(C,"Declared-in-ten became 'sits in ten services' to Kam","a-safety-claim-names-the-property + decisions-held-narration-drifted. The classification row's send_brief.sh gate covers six phrases in briefs only (line 435)"),
62:(P,"Delta between two different instruments read as a moved ticket","Missing clause, lesson sibling rule 3: 'When two counts disagree, get the breakdown before deciding who drifted.' Fix row given"),
63:(C,"Card title carried an unlabelled count; Kam ruled on it","decisions-held-narration-drifted + i-read-representations"),
64:(CE,"Leading cd in a boot command; refused","pretooluse_no_cd.sh (refused this test's own first command live)"),
65:(CE,"Launch tool refused the send three times; nothing launched","brief_and_launch.sh lines 61-96 (opened)"),
66:(LO,"Mail said 'carded' while the card add had been refused","mirror line is scoped to 'mirroring a line to Kam's panel', as the lesson is (0 hits for mail, note). The any-surface rule is in ledger rows only. Fix row given"),
67:(C,"Branch name copied from a width-cut listing did not resolve","validate-brief-pointers: 'open Y and confirm'. 'A cut -c is a cap' is ledger-only (lesson: 0 hits)"),
68:(C,"Kam: lack of consistency; errors were all quantities, not rulings","decisions-held-narration-drifted"),
69:(C,"Supplied an unmeasured ctx figure to an agent","i-read-representations (now on the card body)"),
70:(C,"Kam's mid-task message acknowledged two minutes late","acknowledge-panel-instructions-on-receipt: 'send a receipt... BEFORE the work'"),
71:(C,"Gave a balanced survey when asked what Wednesday thinks","contemplation-mistakes-and-the-fixed-will: 'lead with my position, not a survey'"),
72:(C,"Agent's stated intention reported back as a completed event","artifact-presence-is-not-execution: 'find the line proving that event'"),
73:(C,"A cap dropped exactly the items that mattered, three ways","a-cap-is-never-neutral (now on the card body). board_count.sh refuses only a total equal to its limit"),
74:(C,"Four checks in one day that could not have failed","a-check-that-cannot-fail + valid-is-not-delivered"),
75:(C,"QA insight: fidelity check could not hold; sibling route unfixed","a-check-that-cannot-fail + enumerate-every-surface + a-fix-extended-beyond-the-named-paths"),
76:(LO,"Stamped a jest selector written in grep syntax","Card has the general check-that-cannot-fail line. 'Run a command literal in the tool that will consume it' is in the ledger row only (lesson: 0 hits for consuming, stamp)"),
77:(C,"Estimated clocks written into a note and a card text","i-read-representations: 'generate timestamps'. Card texts have no tool check"),
78:(C,"Six tapped cards stayed open up to 3 h 20 min","clear-fleet-activity-once-answered: 'run... decision_queue.sh rule... tapped_but_open.sh output is empty'"),
79:(CE,"Rotation stalled at the launcher's Continue prompt until Kam typed","Launch_Wednesday.command lines 376-378 SEAT_ROTATION (opened). Row was seats=wednesday at the first reading, seats=all in the tested index"),
80:(LO,"Stamped a predicted diff shape nobody had dry-run","'A predicted number is never measured: dry-run it' is in the ledger row only"),
81:(C,"Stamped a drafter's paraphrase of a gate finding","i-read-representations: 'never... my earlier prose'; lesson section on compression is not in the line"),
82:(C,"Parked a green PR behind a timer; missed Kam's tap","never-wait-a-green-item-ships"),
83:(LO,"Carded removal of a demo the signed SOW names; deleted","IRREVERSIBLE. Premise line equals the lesson; 'read the signed SOW before carding a removal' is in the ledger row only (lesson: 0 hits for SOW, contract). The premise rule is absent from the card moment list"),
84:(C,"Card said 'every view'; the source said 22 of 24","i-read-representations: 'quote a scoped claim with its scope'"),
85:(C,"Builder's 'never more than 72 px' put on a card unmeasured","a-premise-under-a-question: 'mark agent prose reported, unverified'"),
86:(CE,"Override flag on a first add; tool refused","decision_queue.sh lines 365-385 (opened)"),
87:(CE,"Three parallel notes in one seat; each refused","tuesday/tools/note_alone.sh + hook (opened; Tuesday seat only)"),
88:(LO,"PR body said eight new test files; the diff adds nine","'Numbers in a PR body are printed by a program' is in the ledger row only; tuesday/tools/pr_body_facts.py exists as a helper, not a refusal"),
89:(C,"PR title claimed what rows pin, from a READY summary","i-read-representations"),
90:(CE,"Addendum file name carried an authorising word; tap refused","cockpit.sh line 337 verb list (opened)"),
91:(CE,"Same, a day earlier","cockpit.sh line 337 (opened)"),
92:(CE,"Typed '08:2x' into stamp prose","tuesday/tools/stamp_brief.py clock_refusal (opened). Handover headings in the same row are not covered"),
93:(CE,"pgrep and pane_close in one command, fifth time","pane_close.sh detached-work check, rc 10 (opened, lines 124-140)"),
94:(P,"Load reading ran in the same command as the launch","Missing clause, lesson rule 2: 'The same split applies to any refuse-capable step: preflight → check rc → destructive.' The line names only 'a step that can refuse'; uptime cannot refuse. Fix row given"),
95:(CE,"Commissioned drafter ran merge-tree --write-tree in another project","pretooluse_no_cd.sh line 114 (opened). Whether the hook reaches a subagent's Bash was not run here"),
96:(CE,"Note issued in parallel with a board post","tuesday note_alone (opened; Tuesday seat only)"),
97:(C,"Told Kam 'four merges today'; the record says six","decisions-held-narration-drifted"),
98:(C,"Told Kam 99 percent before the gauge read returned","mirror-reports-state: 'write it AFTER the gate returns' + narration line"),
99:(C,"Commission cited wrong C-numbers and tier from memory","mental-model-not-source-of-truth + every-project-keeps-kams-clarifications"),
100:(C,"send piped to tail then launch; the brief had been refused","check-the-refusal-before-the-kill (now on the card body) + zsh-has-no-pipestatus"),
101:(C,"Told an agent its work had stopped, from one tty's process list","a-false-absence + an-absence-goes-stale-while-you-compose-the-complaint"),
102:(C,"Brief inherited the audited register's own frame (96, really 97)","a-census-complete-over-a-frame"),
103:(C,"Refused to merge on board status; branches were already in main","merge-authority ('once the gate passes') + a-recorded-blocker-is-not-a-boundary"),
104:(C,"Relayed '~8 lines' as 8; it was one","git-topology: 'line number... read it in the same action or attribute it'"),
105:(P,"Mail told a builder to push to the branch it had held","Missing clause, lesson extended rule 2: 'The SELF-CHECK line's scope is now: Kam's rulings · the mail against itself · the previous mail to this agent on every id this mail names.' Fix row given"),
}
assert len(S) == len(G) == 105, (len(S), len(G))
seat = lambda f: "Friday" if "friday" in f else ("Tuesday" if "datasec" in f else "Wednesday")
order = [C, CE, P, M, LO, NL]
cnt = collections.Counter(); bys = collections.defaultdict(collections.Counter)
for i, r in enumerate(S, 1):
    g = G[i][0]; cnt[g] += 1; bys[seat(r["file"])][g] += 1
def line(name, c):
    n = sum(c.values())
    return "| %s | %d | %s |" % (name, n, " | ".join("%d (%.0f%%)" % (c[g], 100.0 * c[g] / n) for g in order))
oth = bys["Wednesday"] + bys["Tuesday"]
files = collections.Counter(r["file"] for r in S)
months = collections.Counter(r["date"][:7] for r in S)
T = open(os.path.join(HERE, "replay_report_body.md"), encoding="utf-8").read()
tab = ["| Grade split | N | COVERED | COVERED-ENFORCED | PARTIAL | MISSING | LEDGER-ONLY | NO-LESSON |", "|---|---|---|---|---|---|---|---|",
       line("Friday seat", bys["Friday"]), line("Other seats", oth), line("  of which Wednesday", bys["Wednesday"]), line("  of which Tuesday", bys["Tuesday"]), line("ALL", cnt)]
rows = ["| # | Ledger file:line | Date | Gist | Grade | Card line, tool, or missing clause |", "|---|---|---|---|---|---|"]
for i, r in enumerate(S, 1):
    g, gist, ev = G[i]
    assert len(gist.split()) <= 12, (i, gist)
    rows.append("| %d | %s:%d | %s | %s | %s | %s |" % (i, r["file"], r["line"], r["date"], gist, g, ev.replace("|", "/")))
T = T.replace("@@COUNTS@@", "\n".join(tab)).replace("@@ROWS@@", "\n".join(rows))
T = T.replace("@@FILES@@", ", ".join("%s %d" % kv for kv in sorted(files.items()))).replace("@@MONTHS@@", ", ".join("%s: %d" % kv for kv in sorted(months.items())))
for g in order: T = T.replace("@@N_%s@@" % g, str(cnt[g])).replace("@@F_%s@@" % g, str(bys["Friday"][g])).replace("@@O_%s@@" % g, str(oth[g]))
T = T.replace("@@LOSS@@", "%d of 105 (%.1f%%)" % (cnt[P] + cnt[M], 100.0 * (cnt[P] + cnt[M]) / 105))
assert "@@" not in T, T[T.index("@@"):T.index("@@") + 40]
open(os.path.join(HERE, "replay_report.md"), "w", encoding="utf-8").write(T)
print("\n".join(tab)); print("months", dict(months)); print("written", len(T), "bytes")
