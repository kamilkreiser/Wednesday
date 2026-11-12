STARTABLE: YES (after Tuesday stamps; the kit's own checker and `stamp_check.py` both pass; Tuesday should look at Q-1, Q-3 and Q-4 first)

# B1550 drafter report (SEAT-AT3, ATTIO: why two daily digests did not arrive)
Drafted 2026-11-13 08:45-08:55 AEDT (`date` at start 08:45:01, at the last check 08:52:10). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-13_B1550_SEAT-AT3_attio-missing-digest-logs.md` (+ `.measured`). Work folder: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s274/d_attio/` (checker, the 13 command lines, ten damaged control copies, the sidecar builder).

## BLUF
- The kit sends a Sonnet seat, with Vision's service principal (read only), to read the bridge's site, log configuration, deployment history, activity log and Kudu log files, plus ONE `GET /healthz`, and to say for each missed day which of six causes (H1-H6) fits or "not determinable".
- **Mechanism, from the code (MEASURED, local checkout `fae239b`):** the digest is an in-process `setTimeout` armed for the next 21:00Z at every process start (`schedule.js:107-117`), no cron, no WebJob. **A restart or recycle after 21:00Z and before the next arm skips that day, and nothing catches it up.** A job that cannot read deals logs `run FAILED` and sends no mail; a failed send logs `digest mail FAILED`; **a successful send is not logged at all**, so "summary line present, no FAILED" means the bridge handed over the mail.
- **The cheapest decisive read is the health payload:** `followup.lastRunAt` and `lastSummary.mailed` describe the fire of 2026-11-12 21:00Z if the current process has not restarted since. The 2026-11-07 case needs the logs.
- I did NOT use `az webapp show` or `az webapp log download` as asked: DRAFTER_RULES (2026-11-06 s247 line) says `az webapp show` fetches the publish profile and leaves a `publishxml/action` row per call. The kit uses plain ARM GETs (`az rest --method get`) and Kudu file reads, and proves no secrets read happened (R12 must show 0; R11 is a positive control that must show the 2026-11-01 setting write and its `az webapp show`).
- Nothing hosted was measured by me. Every hosted fact is marked UNMEASURED; the biggest risks are listed under UNMEASURED.

## Facts re-measured (instrument; control)
| # | Fact | Instrument | Control / result |
|---|---|---|---|
| F1 | Vision config dir exists; one subscription: `0c57ab37`, tenant `d500ebad`, `servicePrincipal`, name prefix `bc1e3581`, isDefault True | `python3 -I -B` over `azureProfile.json` printing id/tenant/type/8-char prefix only | the path was `ls`-found first; matches B1035's expectation exactly. The old `/Volumes/Laptop-DEV` path is replaced everywhere in the kit |
| F2 | ATTIO has no `.azure` dir | `ls` of `ATTIO/4_Credentials/` listing | `ls -a` of `ATTIO/4_Credentials/` prints `.attio-sync-state.json .env` only; `ls .azure/azureProfile.json` -> No such file (control: Vision's same-named file exists, F1) |
| F3 | Digest = in-process timer; log strings and line numbers | `/usr/bin/grep -n -F` and `awk NR==n` over the raw files just before writing (schedule.js 29, 41-42, 104, 107, 110, 117, 70, 76, 83, 102; run.js 103, 280, 284-286; index.js 161, 203, 206; mailer.js 30; config.js 72-73, 94) | every pointer in the kit also has a sidecar line (grep -c -F -> 1 or NR==n check -> 1); `run.js:261-276` checked by `awk` (summary object 261-278) |
| F4 | Local ATTIO checkout is at `fae239b` (2026-09-07); origin NOT read | `git log -1`; `git ls-remote origin` | **ls-remote FAILED rc 128** ("Identity file /Volumes/DevMASTER/... github_deploy_rw not accessible", the stale deploy-key path in the repo-local `core.sshCommand`). So "deployed code equals local" rests on B1035's relayed 2026-11-01 proof for three files; the kit tells the seat to trust source over the pointers |
| F5 | ATTIO root `.gitignore` ignores `4_Credentials/` but NOT `.tools/` or `session-tools/` | `git check-ignore -v` on three paths | `4_Credentials/.tools/b1550/raw/x.log` -> `.gitignore:3:4_Credentials/`, rc 0; `session-tools/b1550/x` and `.tools/b1550/x` -> nothing, rc 1 (control: the first path fires, so the instrument works) |
| F6 | Checker works | `python3 -I -B check_lines.py` over the real 13-line file and ten damaged copies | real file rc 0 ("lines 13, refused 0"); ten copies each rc 1 (other app name, other group, missing prefix, `--method post`, other Kudu host, added `webapp restart`, added `appsettings list`, added `webapp show`, `--output-file` under `/tmp/`, R5 removed). Ten copies built from the 14-line variant (13 + one example K2 line); both variants rc 0 on the real file |
| F7 | The kit's two embedded blocks equal the files | extracted both fenced blocks from the finished kit; ran the extracted checker on the extracted lines; `cmp` of the checker block to the work-folder file | rc 0; `cmp` rc 0 |
| F8 | No `Datasec/Vision*` or ATTIO pane | `tmux list-panes -a -F '#{pane_id} #{@cockpit_name}'` | `%0 tuesday`, `%1 fleet-monitor`, two unnamed panes; no Vision, no ATTIO pane (control: `tuesday` is listed) |
| F9 | B1550 not yet in ATTIO Briefs; AT3 name unused | `ls Briefs \| grep -i -c B1550` -> 0; control `B1035` -> 3; `grep -rl 'ATTIO-AT3'` over `tuesday/briefs/` -> no file | |
| F10 | Model row | `model-routing.md` rows C2 (line 92), C8 (98), C6 (96), G1 (108), gap list line 145; `models_latest.json` lines 22-23 `claude-sonnet-5-5` | **no row names read-only diagnosis of hosted logs**; Sonnet chosen as the table's default for non-deploy, non-gate work (see Q-3) |
| F11 | `stamp_check.py` | `--init` wrote 71 claim lines; filled by `mk_measured.py` (greps, awk, checker runs, check-ignore) | `stamp_check: 71 claims, 71 measured, 0 not measured`, rc 0 |

## D-decisions (mine; Tuesday accepts or changes at the stamp)
- **D-1 ARM GET and Kudu instead of `az webapp show` / `log download`** (rule above). `az webapp log download` goes through the publishing-credentials call, so it is excluded for the same reason (unmeasured here; I did not run it).
- **D-2 Raw logs go under `ATTIO/4_Credentials/.tools/b1550/` (ignored), not `ATTIO/.tools/b1550/`** as the commission named: F5 shows the root path is not ignored.
- **D-3 One exact form per line, not "every line names `-g` and `-n`".** An `az rest` line carries the group and the app in its URL path; the activity-log lines can only take `-g` (the group). The checker matches eight exact forms by regex, then adds the banned substring/token scans and a `--method get` check, so it is stricter than "names both".
- **D-4 Fixed lines written once (R1-R12, K1); K2 lines (one per log file) generated by the seat from K1's list and re-checked as a whole** before each run. Size guard 50 MB.
- **D-5 Two controls on the activity-log instrument:** R11 (window of the 2026-11-01 write, expected to show a `config/write` row and a `publishxml` row) and R12 at the end (last three hours; `publishxml` and write rows must be 0).
- **D-6 Success-line control for the log reader:** the day that arrived (2026-11-11 21:00Z, label `follow-up 2026-11-12:`) must show its summary line, else the log is not holding fires and "no line" proves nothing.
- **D-7 Evidence is shape-allow-listed** (timestamps, counts, True/False, two message shapes `attio-bridge: ...` and `agentmail send failed: HTTP ...`); no name scan, so rule 7's underscore-aware name-scan item does not apply (stated in the kit).

## Chain inputs table (MEASURED RULE 4)
| Step | Inputs | Made by |
|---|---|---|
| 0 | the kit; B1035, B1032, B1035 STATUS, runbook, source files | exist at BASE (read-only) |
| 1 (R1, R2) | `commands.txt`, checker, runner, config dir | step 0 / exists |
| 2 (R3, R4, R5, R7, R8) | step 1 pass; `raw/R*.json` | step 1 and the runner |
| 3 (health) | default host name from R3 (in memory or `evidence/host.txt`) | step 2 |
| 4 (R6, R9-R11, K1, K2) | K1's list produces the K2 lines; `raw/K2-*.log` | K1 in step 4 itself |
| 5 (R12) | `evidence/t0.txt` (not required by R12, which is relative: last 3 hours) | step 0 |
| 6 | all `evidence/` files | steps 1-5 |
No cell needs a file that a later step makes.

## Questions for Tuesday (each with a default)
- **Q-1 Raw log location.** Default: `ATTIO/4_Credentials/.tools/b1550/` as in the kit. Alternative: add `.tools/` to the ATTIO `.gitignore` (a tracked change, not the seat's) and use the root path.
- **Q-2 Should the seat file a ticket?** Default as commissioned: no Jira from the seat; Tuesday decides after reading the STATUS.
- **Q-3 Model.** Default: Sonnet (no row fits; the table's Opus rows are deploy and tier-1 gate, which this is not). If you read "hosted production diagnosis" as Opus-class, change the stamp line and the launch level together.
- **Q-4 Kudu auth route.** The kit reads Kudu with `az rest --resource https://management.azure.com/`. The runbook says Kudu worked with "an Entra bearer" (line 216) but I could not verify which audience; if K1 answers 401/403 the seat records it and ends "not determinable" for the logs (the health read still answers the 11-13 case). Default: accept that risk; the alternative (`az webapp log download`) re-opens the publish-profile read.
- **Q-5 `WED_USAGE_STOP=100`** is in the launch line as B1035 had it. Default: keep only if a usage ruling covers it (slot 2 asks you to name it).
- **Q-6 Launch form.** I followed B1035's `launch_when_cool.sh` form with `CLAUDE_CONFIG_DIR=/Volumes/Datasec_DEV/TUESDAY/4_Credentials/.claude`; DRAFTER_RULES still shows a `cockpit.sh add` form and `/Volumes/Laptop-DEV` paths. Default: the commission's form. (DRAFTER_RULES.md itself needs its paths updated; not touched by me.)

## UNMEASURED (the drafter ran no `az` and made no HTTP request)
- Everything about the live bridge: state, log configuration, whether the container log is kept, whether the 11-06 and 11-12 files still exist, the log line timestamp format, the platform restart wording.
- That `az rest --resource https://management.azure.com/` is accepted by Kudu (Q-4); that `--output-file` exists in the installed `az` (the kit says STOP with that question if not).
- That R11 shows the expected `config/write` and `publishxml` rows (relayed from B1035's C3 and DRAFTER_RULES line 52); the grant still being present today.
- That the deployed code equals local `fae239b` (origin unreadable, F4).
- The Kudu scm host being exactly `datasec-attio-bridge.scm.azurewebsites.net` (the kit checks it against R3's host list and skips K1/K2 if not).
- Whether the missing mails were sent by the bridge and lost downstream (H4): only the inbox side can show it, and that is Tuesday's.

## Outside-the-fences disclosure
- Read: DRAFTER_RULES, B1035 kit, B1032 report, B1035 STATUS (tail), ATTIO runbook lines 195-236 and 295-320, ATTIO `src` files, `model-routing.md`, `models_latest.json`, `stamp_check.py` header, `tuesday/briefs/` and ATTIO Briefs listings, Vision's `azureProfile.json` (id/tenant/type/prefix only, no tokens), the ATTIO `.gitignore`.
- Ran: `git rev-parse/log/check-ignore/ls-remote` (read verbs) in ATTIO, `tmux list-panes`, `lsof` count of listening TCP sockets (12; no ports are assigned or used by this kit), `ls`, `awk`, `grep`, python over files.
- `git ls-remote` was attempted against ATTIO's origin (a read verb) and failed on a missing key path; no ref or file in ATTIO changed.
- Wrote only: the kit, its `.measured` sidecar, this report, and the files in the work folder. No Artifact/Docs/mail tool, no Jira, no card store, no `az`, no HTTP, no `cd`.

`stamp_check: 71 claims, 71 measured, 0 not measured` (rc 0, run 2026-11-13 08:52 AEDT after the last kit edit)
