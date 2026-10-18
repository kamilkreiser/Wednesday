# Gate 26 kit: DRAFTER REPORT (2026-10-18, from 13:55:49 AEDT; read-only drafter, Opus 5.5)

**BLUF:** The kit for **gate 26** is drafted (routing name `QA/NexusAI-gate26`, tags `qa-g26-*`). It is a TIER-1 re-gate AS MERGED of C-170 / RD-460 (`be0fe37`) onto main `c7ca0ed`: one merged tree M170, one verdict line, plus a SHIPPED TEXT line and a LANDING CHECKLIST line.
- `bash -n` is clean. `--check` passes every content guard and refuses only on your stamps (11 placeholders) and the route line.
- **The merged tree rebuilds exactly** in my scratch mirror to the pin `0f4602e`: the mechanical merge plus the seat's counts blob.
- **Heads-up for your word-pack decision.** README.md and DEPLOYMENT_GUIDE.md at be0fe37 are most likely NOT what the released 2.2.1 image ships (WRONG 7, read-only inference). T4 decides whether the gate measures the image itself.

## Files
- Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-gate26-c170-be0fe37-merged.md`
- Launcher: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate26.sh` (mode +x)
- READY body (saved from the AgentMail GET, sha256 `0e479fd5…9ea3`; the launcher pins it): `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-18_nexusai-c170-merged-READY-mail.txt`
- This report.
- Scratch only (my session scratchpad, not the project): one `--mirror` clone `g26m.git`, the READY JSON, query scripts, one corrupted READY copy used as a negative control.

## Stamps Tuesday owes (the launcher refuses until all are done)
1. **T1-T9** `RULED:` slots: write "default" or the ruling (9 slots).
   - **T4 is the one to read twice.** Default (a) lets the gate read ONE layer of the released image anonymously by `curl`: token, manifest, config, the markdown layer, and the registry's blob-storage redirect. That is a contact beyond the build's own two requests.
   - **T2** decides how the 19 B-side ids are paired without gate 5b's §9.9 table, which is on the T9.
   - **T3** names the build's two registry requests as allowed.
2. **The SELF-CHECK line and the Self-check note**, last and by hand. With the T-slots that makes 11 `@STAMP@` placeholders.
3. **The route line** `QA/NexusAI-gate26|tuesday-agent@agentmail.to|no` in `fleet/inbox_routing.conf`. I did not edit that file.
4. Nothing to copy: the READY is already in `briefs/`.

## Launch command
```
bash /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/NexusAI-gate26' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate26.sh'"
```
Pre-flight: `bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_gate26.sh' --check`

`--check` result at ~14:15 AEDT: guards `9 MODEL 40 6 7 8 18T 18 90 91 22 93 94 95 70 70N 31 39 10 17 11 12 13 14 15 20 41 82 19 24 53 71 76 77 78 79 81 38R 86` all pass.
- ls-remote took 1 attempt: main `c7ca0ed`, branch `be0fe37`.
- The seat's object `88153c0` is present. Its parents, tree, counts, lockfile and workflows match the pins, and so does **every one of the 154 changed paths**: each carries the changing side's blob.
- The negative-control seats are `78171` (Datasec/NexusAI-O), `86424` (tuesday) and `99015` (QA/NexusAI-gate25).
- The jest lock is held by `qa-g25-V761`; the launcher reports this as a NOTE (FIFO).
- It refused only on 32 (11 placeholders) and 40 (route).
- **Negative control:** a READY copy with `be0fe37` replaced is refused at guard 31.

## Sequencing
Gate 25 is live on the same lock base. Gate 26 can launch now: it does its lock-free rows (the tree, the interaction reads, both package builds, shipped text, workflows, deploy, audit, gitleaks) and then queues FIFO behind gate 25's and S101O's holds, which is your ANSWER-7's "after gate 25 frees the jest lock". **If gate 25's members land on main first, main moves and this launcher refuses**, because every row is pinned to `c7ca0ed`. You would then re-brief on the new main.

## Key findings while drafting (all in the brief's WRONG list)
1. **ADDENDUM-1 is load-bearing here (MEASURED).** In NexusAI, `be0fe37` is named ONLY by `refs/remotes/t9-drive-2026-10-15/heads/rd-460-pkg-into-main-s84m`. In a `--mirror` clone, `git remote remove origin` dropped every `refs/remotes/*` ref (484 refs went down to 94). Only a `g26/rd460` ref made beforehand kept the head named. T6 makes that order mandatory.
2. **The tree rebuild (MEASURED in scratch).**
   - merge-tree conflicts in the counts file only (the both-sides set is the counts file alone: 34 head paths, 121 main paths).
   - With the seat's blob `fc7937b` substituted, the tree is `0f4602e`, which equals the pin.
   - Negative controls: main's and the head's counts blobs give different ids. Positive control: `c7ca0ed`'s own merge rebuilds to its own tree.
   - **The raw merge tree id depends on how the arguments are spelled** (conflict-marker labels). Full shas with main first reproduce the seat's `65457f9`; short shas give `2cbf7fd`. All of them differ from the pin in the counts path only.
3. **The commission's "ONE outbound call" is TWO requests (MEASURED, script source).** The build makes an anonymous token GET and then a manifest GET, both to `nexusaireleaseacr.azurecr.io`, and only when the image is usable. **The `c7ca0ed` control makes ZERO requests**, so it doubles as the curl-shim's negative control. `MKT_ANON_PULL_PROBE` must stay unset for the acceptance run, because a stub would forge the "(HTTP 200)" line. The launcher unsets it before exec.
4. **The interaction, by input (MEASURED; the conclusion is read-only).**
   - Main changed NONE of the build's inputs since base: the 3 plan files, release-policy, the build script and all 7 listed media files.
   - Main DID change the Dockerfile, the .dockerignore and the image guards (`image-content-exposure`, `rd385`, plus the new `rd418` and `helpers/dockerfile-stages.js`). Those guards read the head's changed README.md and DEPLOYMENT_GUIDE.md through main's new recipe, and no gate has run that combination.
   - The seat's "only the counts file is shared" is true of file names and silent on this. **T8's four plants** make the guards prove they see it.
5. **SHIPPED TEXT (read-only inference from four measured reads).**
   - The 2.2.1 image is the 2.2.0 image (`fdda3309…`).
   - It was built by `az acr build` from a local tree with `BUILD_COMMIT_SHA=0677388`. `build-commit-sha.sh` prints a sha only for a clean tree.
   - `0677388` carries README `f129ff3` and DEPLOYMENT_GUIDE `01c7c46`, the same as base and main.
   - be0fe37's `e23999f`/`3753a82` came from the package line, which `0677388` does not contain.
   - **So the released image most likely ships main's text, not be0fe37's, and the head's guide text would be new customer words once an image is built from main.** Examples: "The deployment always creates its own Key Vault; there is no option to use an existing one", and the setup-checks section. That matches gate 5b's A-N1.
   - Under your C-216 that points to a word pack for Kam, unless T4's image read says otherwise.
6. **arm-ttk.yml (MEASURED).**
   - Its blob equals the released `3f79e9c`'s, and it is the only workflow M170 adds.
   - The landing push WILL start it (its paths match). It has `contents: read`, a single `${{ env.PWSH_VERSION }}` expression, `checkout@v4` (a tag, the same as main's other workflows), and both downloads are sha256-checked.
   - It is not a required check (the seat's ruleset reading, relayed). CodeQL has never analysed it.
7. **deploy-demo (MEASURED).** Its `paths-ignore` (`**.md`, `docs/**`, `tests/**`) does NOT cover this merge, so the landing push STARTS deploy-demo. Only the two `vars.CI_DEPLOY_ENABLED == 'true'` conditions keep it from deploying.
8. **The 24 ids (MEASURED per file).** All six files meet C-216(1)'s blob conditions.
   - A-side: jsdom, rd327 and image-content-exposure have head = base, merged = main.
   - B-side: marketplace-package-build, rd461 and rd503 have main = base, merged = head.
   - The per-id and new-title-passes halves are the gate's.

## Corrections to the commission
- **"ONE outbound call"** is two requests to the same host (item 3). The brief allows exactly those two and records them.
- **"The 19 B-side ids … gate 5b's table"**: the §9.9 table is on the unmounted T9 (L-B7). T2 defaults to re-deriving the pairs and matching the six retired ids by text to `session-tools/s78g/c57-accounting.txt`, which is on this drive.
- **"Docker NONE … default NOT RUN"** for the shipped-text row: it can be done without docker or az, by anonymous `curl` of the one layer. I made that T4's default (a) because it measures rather than infers. Option (b) is the read-only chain with the image read named NOT RUN. Pick (b) if you do not want the extra registry and storage-host contact.
- **The build's inputs vs the guards' inputs:** the commission asks whether main touched what "the package build or the image guards read". The answer splits. The build: no. The guards: yes. The kit measures each separately (r2 A/B/C).

## Holds I did not break
- In the NexusAI repo I used read verbs only. No fetch, worktree, merge or write verb ran there; `merge-tree --write-tree`, `hash-object -w` and `commit-tree` ran only in my scratch mirror.
- No az, docker, gh, npm, jest, gitleaks, package build, registry request or lock ticket.
- The only network calls were AgentMail GETs and `git ls-remote`.
- No secret was printed. Nothing was deleted. Nothing was written outside the three output files and the READY body, and `inbox_routing.conf` was not touched.
- Gate 25's dirs and panes were not touched; I only read its kit and its pane list.
