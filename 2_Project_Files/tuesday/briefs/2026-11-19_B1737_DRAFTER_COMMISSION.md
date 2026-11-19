# B1737 drafter commission — NexusAI lane N-F: RD-835 + RD-861 (SEAT-N158)
Draft ONE builder kit `2_Project_Files/tuesday/briefs/2026-11-19_B1737_SEAT-N158_nexusai-lane-nf-browser-escapes.md`
(+ `.measured` sidecar; return the drafter report as TEXT in your reply, Tuesday saves it) in the FORM of
`2026-11-19_B1733_SEAT-N157_nexusai-lane-ns-datasource-admin.md` (read it whole, and its builder STATUS
`!CODING/Datasec/NexusAI/1_Project_Definition/Briefs/2026-11-19_B1733_STATUS.md` Corrections first: prevent each by name,
in particular: ONE lock acquisition (test your own judge/kept tools on a recorded fixture before the lock), and absorb a
main move inside the same acquisition). Follow `2_Project_Files/tuesday/DRAFTER_RULES.md` whole.
BASE: the lane's base is NexusAI main AFTER PR 231 lands (a merge commit whose tree equals branch head
f06b080e3ffce9f6be869e66eb7b0e6ab0dac1d5's tree; counts 6086/384). PR 231 is not merged yet: measure every file and line
at f06b080e (gh contents ?ref=), say so, and leave the BASE slot for Tuesday's stamp (re-measure rule: if main's tree
differs from f06b080e's tree in an owned path, STOP).
Scope (sweep `2026-11-19_SWEEP-1115_datasec-actionable-lanes.md` lines 66-73; read RD-835 and RD-861 whole by Jira GET):
the browser-script escapes: static/js/index.js (the eight `esc` closures and the user table / userNameWithInfo),
static/js/settings.js (showValidationModal), static/js/first-run-setup.js (testConnection), new tests under __tests__/
(beside rd778-dom-text-stays-text.test.js), the expected-counts file. Partition: NO backend/** file. Old-answer census by
program (tests pinning the current DOM output of those functions). Gate: G2 Sonnet unless the change is an XSS fix on an
attacker-reachable sink, in which case recommend G1 Opus with the reason. CodeQL: the kit runs
`2_Project_Files/tuesday/tools/codeql/pr_codeql_check.sh` (see `tools/codeql/GATE_STEP.md`) twice (CQ-1 before the lock,
CQ-2 before the push). PRIOR-WORK CHECK: what RD-778 (#?) and earlier escape work already did. No ruling exists for this
lane: write every choice as Tuesday's default. Read-only everywhere; NexusAI GH_CONFIG_DIR
'/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config' (verify kamilDatasec); Jira GET only, credentials
in-process. Pick a jest worktree slot no kit or gate named on 18-19 Nov (taken: 5, 11, 12, 13, 14, 17, 18 and more: scan).
Scratch `2_Project_Files/fleet/state/s292/d1737/`. No cd; zsh. First line of your reply: STARTABLE: YES|NO - why.
