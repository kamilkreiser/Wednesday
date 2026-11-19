# B1733 drafter commission — NexusAI lane N-S: RD-793 + RD-990 (SEAT-N157)
Draft ONE builder kit `2_Project_Files/tuesday/briefs/2026-11-19_B1733_SEAT-N157_nexusai-lane-ns-datasource-admin.md`
(+ `.measured` + `2026-11-19_B1733_DRAFTER-REPORT.md`) in the FORM of `2026-11-19_B1726_SEAT-N155_nexusai-lane-500-to-400-body-shapes.md`
(read it and its drafter report whole; the round-2 kit `2026-11-19_B1728_*` shows the CodeQL step). Follow DRAFTER_RULES.md whole.
Scope (sweep `2026-11-19_SWEEP-1115_datasec-actionable-lanes.md` lines 58-65; re-measure everything at NexusAI main 46050e25 or newer):
RD-793 = the four data-source handlers get the admin check (requireAdminFor or the repo's current equivalent: read how
neighbouring admin routes do it, setup-mode aware); RD-990 = the logged path expression at server.js ~556 and
services/accessAudit.js ~50. Regenerate docs/role-capabilities.json + docs/ROLE-CAPABILITIES.md with
scripts/role-capability-inventory.js and the expected-counts file. MUST carry a by-program census of every existing test and
generated field that pins the OLD answer of those four routes (a viewer/non-admin getting 200 today), each rewrite/unaffected.
Tuesday's rulings (`2026-11-19_SWEEP-1115_TUESDAY-ANSWERS.md` items 2 and 4): builder Sonnet C2; gate G1 Opus; the kit runs
`2_Project_Files/tuesday/tools/codeql/pr_codeql_check.sh` (see `tools/codeql/GATE_STEP.md`) on base vs head before READY and
puts the table in STATUS; one jest-lock acquisition (nexusai-lock.sh) for the full verify; HARD STOP proposed.
Prior-work check: what RD-793/RD-990 history and the #197/#200/#216 permission work already did (do not reinvent).
Read-only everywhere; NexusAI GH_CONFIG_DIR '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config' (verify
gh auth status = kamilDatasec). Jira GET only, credentials in-process by name. Scratch `2_Project_Files/fleet/state/s292/d1733/`.
No cd; zsh. First line of the report: STARTABLE: YES|NO - why.
