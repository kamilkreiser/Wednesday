# A1 findings: audit A (seat scope), listA lines 1-28

| file | audit | what was wrong | evidence |
|---|---|---|---|
| 2026-08-05_wed-work-threshold-delegation.md | A+C | Narrowed to wednesday; the rule is coordinator conduct on its own dev work and the lesson itself covers the laptop. Friday and Tuesday lose it. | L40-42: "**Laptop caveat (honest):** teammate visibility here is receipts + final report, not a live cockpit pane (that's Studio tmux)"; L25: "**Kam is never interrupting.**" |
| 2026-08-12_hpsm-continuous-readiness-grant.md | A+C | HPSM is a Datasec project, so the scope is tuesday,friday, not tuesday alone. INCIDENTAL (C, not fixed here): the rule says ENDED but status is live; the lesson frontmatter says status: live and contains no 2026-09-10 end event, so the row's 'ended' claim is not from the lesson. Either prove the end and mark dead, or restate the grant as live. | L18-19: "**The caveat that scopes everything: the project has NOT started.** The SOW is unsigned."; L5: "status: live"; projects_index/INDEX.md:82 lists HPSM under "Datasec / everything else" |
| 2026-09-09_parallel-seats-on-one-project-grant.md | A | Narrowed to wednesday,friday because Kam's words named Secuura; the lesson generalises it to standing practice for any project and the how-to (directory partition, worktrees, push lock, kill by ancestry) is client-neutral. Tuesday runs parallel Datasec seats and loses it. | L18-21: "Wednesday has a project with a live ticket backlog and one seat's worth of throughput ... It generalises the weekend-scoped ... grant into standing practice"; L86: "every parallel-seat brief on ONE checkout carries this STANDING BLOCK" |
| 2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate.md | A | Narrowed to wednesday; the rule is about any coordinator seat's own context rotation with agents live. wednesday_rotate.sh serves all three seats. | L12: "dont let your context rotation get in the way of finishing tasks. You can always delegate to agents and get them to work while you rotate."; 2_Project_Files/fleet/cockpit/wednesday_rotate.sh:58-61 has cases tuesday) and friday) ("the laptop seat") |
| 2026-09-14_at-90pct-weekly-usage-no-new-agents-wednesday-plus-local-model.md | A+C | Narrowed to wednesday; the no-new-launch cut binds every seat (the gate reads usage_<seat>.json and a per-seat stop file). Only the Ornith half is Studio-only. Friday and Tuesday lose the launch cut. NOTE FOR AUDIT B: the gate does not enforce 'cheap closes first', the Ornith switch, or Agent-tool drafters (lesson L27). | 2_Project_Files/fleet/usage_gate.sh:31-41 "SEAT (2026-09-23, Friday seat) ... usage_${SEAT}.json", :56 "USAGE_STOP.$SEAT"; lesson L27: "**The Agent-tool drafters cannot be gated by a script**" |
| 2026-09-14_true-duplicates-are-closed-and-archived-by-us-no-external-review.md | A | Narrowed to wednesday,friday (read as Secuura); the lesson says all boards, not scoped to Platform K. Tuesday loses it. | L10: "Standing rule, all boards."; L46-47: "**It generalises to every board Wednesday's seats work** — the rule is his, \"going forward\", and not scoped to Platform K." |
| 2026-09-15_a-wrapped-seats-pane-is-closed-in-the-same-action-and-a-floor-deadline-is-checked-by-listing.md | A | Narrowed to wednesday because the incident was Ornith's night; rule 1 (wrap read, score, pane_close in one action) and rule 2 (list panes before any census-gated mechanism) are for any coordinator with a cockpit. | L11: "(the Ornith night runner's G2 at 23:30; any \"no other agents run\" gate), or a seat's wrap has just been read"; L18: "**Wrap read → score → `pane_close.sh` in ONE action.**" |
| 2026-09-16_if-something-blocks-move-on-to-the-next.md | A+C | Narrowed to wednesday; Kam's correction is general queue conduct (skip the blocked item, never wait on a card). Only the held-diff and Ornith-idle clauses are Studio-only. | L17: "There are lots of tickets there. If something's blocking, move on to the next."; L28: "**A blocked item is SKIPPED, not waited on.**"; L29: "\"Decision-shaped\" is a verdict on ONE ticket after reading it, never on a tier." |
| 2026-09-17_every-project-keeps-kams-clarifications.md | A+C | Narrowed to tuesday. Kam's words say any project; at minimum Datasec means tuesday,friday. Friday (and Wednesday) lose it. Rule text also said 'Datasec project'. | L13: "create a rule to do so with any project so that clarification can be utilized at any time."; L21: "(this widens it to every project)" |
| 2026-09-17_guard-against-reinventing-prior-work-check.md | A | Narrowed to tuesday; the lesson scopes it to the Datasec projects, which Friday also serves. Friday loses it. (Not all: the lesson says Wednesday's adoption is undecided.) | L26: "**Scope:** Tuesday's seat and the Datasec projects ... Whether Wednesday adopts it is hers and Kam's"; L22: "**Every Datasec brief carries the PRIOR-WORK CHECK standing line**" |
| 2026-09-18_rotate-is-for-an-unwrapped-seat.md | A | Narrowed to wednesday; cockpit.sh rotate is the fleet tool every coordinator seat runs, and the rule (never rotate a wrapped seat; one session per project) is client-neutral. | L10: "`cockpit.sh rotate` is for a seat that has NOT wrapped; retire a wrapped seat by hand"; L28: "**Never run two sessions on one project**" |
| 2026-09-18_the-boot-spec-outgrew-the-context-window.md | A | Narrowed to wednesday; every seat boots on the same mandated whole-reads (digest, pickup, ledger). Friday and Tuesday lose the measure-before-reading rule. | L12-15: "Every file the boot prompt says to read WHOLE is a file that grows. Measure the boot's total cost at every boot"; L61: "**Measure before reading.**" |
| 2026-09-20_ks1175-hold-lifted-make-the-fix.md | A | Narrowed to wednesday; it is a ruling on Secuura tickets (KS-1175, KS-1250), which Friday also serves. Friday would not know KS-1250's live smoke run still pauses for Kam. | L18: "**LIFTED:** KS-1175's signature-class hold ... **KS-1250 is untouched and still his.**"; L31: "The pause covers RUNNING the smoke test against a live box" |
| 2026-09-22_ornith-is-studio-only-not-datasec.md | A+C | Narrowed to tuesday; Ornith is the Studio's and Friday has no local model, and shared boot text reaches every seat. The Friday launcher states the same thing. | L11: "Ornith is a studio agent. not a Datasec workflow."; L15: "a shared file speaks to both seats"; Launch_Wednesday.command:613-614 (Friday scope): "Ornith, night/ and local-model/ are the Studio's, never yours." |

CHECKED: 28  WRONG: 14

Found correct (seats field), judged from the lesson read whole:
- 2026-08-12_morning-ticket-sweep-autostart.md
- 2026-09-09_advisory-baseline-standing-authority.md
- 2026-09-10_kintsugi-first-then-demo-behind-gates.md
- 2026-09-11_secuura-we-approve-and-merge-our-own-tested-work.md
- 2026-09-14_local-model-pilot-grant-qwen3-30b-simple-checked-tasks-only.md
- 2026-09-14_ornith-runs-at-night-in-the-downtime-a-standing-rule.md
- 2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry.md
- 2026-09-15_ornith-every-issue-gets-a-tooling-or-instruction-fix.md
- 2026-09-15_ornith-q4-only-volume-week-qa-sunday-merge-once.md
- 2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do.md
- 2026-09-16_new-account-spin-up-agents-to-test-approve-merge.md
- 2026-09-18_no-claude-agents-local-model-only-until-sunday.md
- 2026-09-18_ornith-is-cheap-the-brief-is-the-cost.md
- 2026-09-18_ornith-works-constantly-standing-rule.md

Notes on the correct ones:
- 2026-08-12_morning-ticket-sweep-autostart.md (wednesday,tuesday): correct; Launch_Wednesday.command:614 says boot step 10 (morning sweep + autostart) "belong to the Studio and mini seats", Friday skips it.
- 2026-09-09_advisory-baseline-standing-authority.md (wednesday,friday): kept; the grant text is client-neutral ("a pin this fleet already holds") but it was ruled on card secuura-advisory-gate-moving-set and its "shared re-triage date" is the Secuura baseline. A grant is read narrowly. Judgement call, flagged.
- 2026-09-16_new-account-spin-up-agents-to-test-approve-merge.md (wednesday): seats kept (tied to the account on the Studio, Ornith continues). NOTE FOR AUDIT B: enforced_by usage_gate.sh is wrong for this row; the gate enforces only the 90% cut, not the grant or its exclusions (deploys, demo, workflow PRs).
- 2026-09-14_local-model-pilot... (superseded) and the two dead rows: seats moot; Studio-only anyway.

Not checked by A1: enforced_by against scripts (audit B), rule accuracy beyond what is noted (audit C), any row outside listA lines 1-28.
