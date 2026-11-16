# B1603 G1 gate commission (Tuesday s282, 2026-11-16)

RE-COMMISSION from this file if `2026-11-16_B1603_verify/VERDICT.md` is absent at the next boot (an in-session gate dies with the seat).

You are an independent QA gate (tier G1, Opus) for Tuesday, the Datasec coordinator seat. Read WHOLE first and follow:
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-10_GATE-VERIFIER-STANDARD.md`
(its Output folder pattern is replaced here by `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1603_verify/`).

- **Project:** NexusAI, folder `/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI`, repo `datasecau/Reporting_Dashboard_Au`, `GH_CONFIG_DIR=<P>/4_Credentials/.gh-config`. Landing form: MERGE COMMIT, head-pinned. Report whether the merge would start `deploy-demo.yml` and whether its jobs would read skipped.
- **KIT:** `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-16_B1603_SEAT-N136_nexusai-nx-s1-server-security-2.md`, plus its ADDENDUM-1 and ANSWER-1..4 beside it (same folder, `2026-11-16_B1603_*`).
- **READY sha:** `a8358d923d8461f6668f05b3be6c934de91ec98e` on branch `b1603/nexusai-nx-s1-server-security-2`; BASE = NexusAI main `d1152289f7c0f2d97b4bd82187488c47d51c65fc` (read by Tuesday at 11:23 AEDT, 0 open PRs). Re-read main before writing VERDICT.md.
- **Builder STATUS:** `<P>/1_Project_Definition/Briefs/2026-11-16_B1603_STATUS.md` (1,855 lines; READY section at line 165; the full patch from line 216). Its claims are claims.
- **Tier G1** (security surfaces: rate limiting, host matching, regex linearity, prototype keys, GUID refusals, audit flush). Rule on: every RD row in the kit; the builder's local CodeQL numbers (head 47/15, new rows 0) by running the CLI yourself (`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/codeql/codeql/codeql`, javascript, the repo's suite); red-without-the-fix for each new test file; the five "linear" claims with your own timing probe at the boundaries; that the open window (`adminGateRefuses`, `authEnforcement.js`) is byte-unchanged; the counts file (5707/361 or what the plain verify prints at the merge).
- **Heavy work:** the plain verify takes ~24 min. Take the project's shared jest lock the way the kit's chain does (read the kit for its path) and release it; start a heavy run only when `uptime` load1 < 7 (wait up to 15 min, record it). Ports, if any server is started: 10110-10119 only (`lsof` first); kill by pid only.
- **Fences:** as the standard. Nothing pushed, no PR, no merge, no Jira, no mail, no board, no `az`, no hosted HTTP. Write only in the verify folder and your session scratchpad.
- **Final reply:** the verdict line and the file list.
