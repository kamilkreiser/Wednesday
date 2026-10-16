# Vision gate 18 (QuickQuote PR #8 @ 4d6ed6e, puppeteer-core 25.0.2 + node:22 image): drafter's report

Drafted 2026-10-16, 12:58 to ~13:40 AEDT, by a read-only drafter for Tuesday.
Outputs:
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/briefs/2026-10-16_vision-gate18-qq-pr8-puppeteer25.md`
- `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate18.sh` (chmod +x, `bash -n` clean)
- this report

Nothing else was written, apart from scratch copies of two lockfiles in the session scratchpad. There was no push, merge, `az`, mail, docker build or run, browser, or product process. The launcher was run only with `--check`.

## Numbering
This is **gate 18**. The QuickQuote gates moved onto the unified Vision numbering after `qq gate 8`: gate 9 handled qqpurge, then gates 16 and 17. The last report on disk is `2026-10-13-vision-gate17-qq-quality-round` on the T9. There is no gate after 17 in either drive's `briefs/` or reports, and `inbox_routing.conf` stops at `QA/Vision-gate17`.

## What I copied, and from where
- **Section shape and QuickQuote standing rules come from gate 17's brief:** PIN-HEADS table, WRONG list, the READY's NOT TESTED kept verbatim, 2a, the N-sections, the floor and port rules, `env -i` and the forbidden env list, the egress wrapper and census, the RD-606 floor count, deadline and heartbeat, HELD, THE MODEL RULE, the question route and the verdict format. The GET-only `gh` shim (D1) is gate 17's, copied unchanged.
- **The required template sections come from BRIEF_TEMPLATE:** Charter, 2a, the PRIOR ROUND pointer block with a report path, evidence classes, PROVENANCE, and the three-reading head rule.
- **The launcher started from gate 17's launcher:** the PIN parser, guards 6/7/8/9/18/22/74/31/10/17/12/78/13-15/20/70/82/19/24/53-75/44, and the pending-guard pattern (46/41/32 reported together).
- **These parts came from the NexusAI batch-23 launcher:** the Laptop-DEV re-base and the matching "no T9 TUESDAY in prompt" guard; the model id read from `models_latest.json` and refused unless it is `claude-opus-5-5`; the 38R negative-control seats taken live from cockpit panes, here requiring the `tuesday` pane and the `Datasec/Vision_Sales_Portal` builder pane; guard 86 (no live gate pane); the docker-daemon guard; and the H-35-style docker discipline in the brief (own tags only, no prune or rm or push, containers stopped and left).
- **I did not use `gen_launcher_from_template.py`.** It is a single-purpose generator for one Secuura launcher, with hard-coded anchors for that case. It is not how the Vision launchers were made.

## What is new compared with gate 17
- **Docker is in scope** for the first time on a Vision gate, because C-19 requires the image to be built locally and the commission requires amd64. New sections: §N2 builds the base and head images for amd64, §N3 runs the CI suites inside the images, §N4 builds the real-user-path artefacts inside the images and compares them, and §13.5 sets the docker discipline. Launcher guard 45D replaces gate 17's NODE20-LEG.
- **Network exceptions NX-1 to NX-4** (decision D3). Gate 17 banned docker, npm audit and the registry. This commission needs all three.
- **AZ-READ-LEG (decision D2, guard 47, new).** The options are TUESDAY-READS, GATE-SHIM or NOT-RUN. I recommend TUESDAY-READS. The GATE-SHIM option gives an `az` shim that allows only three fixed read commands.
- **The chain contains two merges** (`0d45100` and `4d6ed6e`). Gate 17's "no merges" rule became exact parent pins for each commit, plus a tree pin for the head (`01bdc92`).
- **Guard 23 now pins the exact non-comment change in each file.** In the Dockerfile that is only the FROM line. In package.json it is only the puppeteer-core line. In the two test files it is only the CdpBrowser require.

## Traps found while drafting (all in the brief's WRONG list)
1. **The T9 is no longer the master.** The T9 copy of the QuickQuote repo does not contain `4d6ed6e`, and this drive's Testing Agent MAIN has no `projects/vision`. Gate 4 and gate 17 reports and tools exist only on the T9. The brief and launcher therefore read them there and write only to Laptop-DEV. Gate 17's launcher still points every path at the T9, so it could not be reused unchanged.
2. **The production image ships `stage3/test/`.** `.dockerignore` does not exclude it, and the Dockerfile has `COPY stage3/ /app/stage3/`. So the two test files that now reach `puppeteer-core/internal/...` are inside the image, as the `lib/cjs` versions were at base. The READY's "no shipped file" grep covered only lib/, server.js and strip.js. This is a pre-existing pattern, not a defect of PR #8. The gate reports what the image contains and what it loads at runtime as separate things (WRONG (b)).
3. **The `lib-close-shared` cell passes whether or not its stub hits.** Every assertion it makes also holds when `close()` is not hung. If puppeteer-core 25 is ESM-only and loaded through `require(esm)`, the stub could patch a different class instance, and the cell would still pass. The gate proves class identity at runtime and runs disarm mutants G-M1 and G-M2 (WRONG (c)). This is an inference from reading the code; I did not measure it.
4. **Base-vs-head image comparisons are only valid when both images come from one build window.** Debian `chromium` is unpinned and the `node:*-bookworm-slim` tags float. The gate builds both images back to back with `--pull --no-cache`, records versions, and treats any comparison as VOID if Chromium or font versions differ (WRONG (e)).
5. **The box is badly overloaded.** Load was 224.77 at 13:07 and 219-236 at 13:26, on an 8-core M2 running eight MPS lanes, Composer-A, HPSM-POC-F, NexusAI-O and QA/NexusAI-batch23 (which also runs dind containers on the same Docker daemon). Building and running Chromium under amd64 emulation at this load may take a very long time or hit deadlines. Image deadlines are up to 2400 s. Under D4, an amd64 leg that is NOT RUN makes the verdict PROVISIONAL, never a GO based on arm64. **Tuesday should consider launching after the MPS lanes and batch 23 have cleared.** The launcher prints a NOTE when the 1-minute load is above 40.
6. **Builder objects are on the shared Docker daemon:** four `qq-evidence-local:*` images, including the builder's own `amd64-main-e4ce536` and `amd64-prb`, plus a builder container that was running at 13:07. The brief forbids touching any of them or treating them as evidence.
7. **The emailed-PDF route cannot be booted through the image's CMD.** It needs SESSION_SECRET and an unlock secret, and `ensureTables()` needs a real `TABLES_CONNECTION_STRING`. The brief therefore runs the image's own `createApp()` inside the image, with an in-memory store, a capturing stub mail and throwaway secrets. It drives the image's own Chromium through the page's own email control. The report must say this is a substitute for the real boot (WRONG (m)).
8. **The session cookie is `Secure`.** Logging in from Chromium over `http://127.0.0.1` inside the container should work, because loopback counts as a secure context. That is my expectation, not a measurement. The brief gives a CDP-cookie fallback and requires the gate to say if it used it.
9. **No ImageMagick, PIL or numpy on this Mac.** Pixel diffs must use `pdftoppm` PPM output and plain python.
10. **PR #7 (`e4ce536`, this gate's base) was never QA-gated.** Tuesday checked it at source as tier 2 (daily note, 12:37 and 12:57). It has an open item: the server path and the printed page price the same inputs differently, and 7 unknown print-mode fields (`pmBoth`..`cpPct`) were found. Both appeared before and after PR #7. The brief has the gate measure both in base and head and report them as pre-existing, not as PR #8 regressions.
11. **Zsh trap:** `"$H:stage3/…"` fails under zsh with "bad substitution", because `:s` is a zsh modifier. The brief repeats gate 17's rule to use bash for every `git show <sha>:<path>`.

## Verified at source (drafter)
- **Heads:** main `e4ce536…`, branch `4d6ed6e…`, `refs/pull/8/head` = `4d6ed6e`, and `refs/pull/8/merge` = `80747c81…`. Instrument: `ls-remote` at about 13:00.
- **Chain and history:** the chain and its parents; 3 ahead and 0 behind; merge-base `e4ce536`; `d030674` and `51e9286` are on main.
- **Diff:** 5 files, numstat +85/−522, which matches the READY. The only non-comment changes are the four lines listed above.
- **Unchanged blobs:** index.html, the hosted server module, lib/pdf.js, lib/xlsx.js, strip.js, .dockerignore, tests.yml and the other tests have the same blobs in base and head.
- **Lockfile diff:** exactly as the READY says: 40 removed, 1 added, 13 changed. puppeteer-core 25.0.2 and @puppeteer/browsers 3.0.2 declare engines `node >=22.12.0`.
- **GitHub, via `gh api` GET with Vision's gh-config** (the file mtimes in that directory did not change):
  - PR #8 is open and clean.
  - CI runs 38837565972 and 38837589895 are both success, 5/5 jobs, on `4d6ed6e`.
  - Dependabot shows #1 and #4 open (extract-zip, high).
  - Main has 0 open code-scanning alerts and 0 hooks.
  - Workflows: tests, Dependabot, CodeQL.
- **Clarifications:** C-19 is present, with the wording the launcher checks for.
- **npm cache:** holds puppeteer-core 25.0.2 and 23.11.1, @puppeteer/browsers 3.0.2, chromium-bidi 16.0.1, webdriver-bidi-protocol 0.4.1 and extract-zip 2.0.1.
- **Local tools:** Docker 29.7.2 on linux/arm64, with buildx listing `linux/amd64`. Chrome 155.0.8059.84. Node v26.8.1. The Azurite image is present locally.
- **Model:** `models_latest.json` opus is `claude-opus-5-5`.

## What I could not verify
- **Whether amd64 Chromium runs reliably under emulation here.** I don't know if Docker Desktop is using QEMU or Rosetta for it, or whether builds fit the deadlines at this load.
- **Whether Vision's `.azure` is logged in, and whether its identity can read `hpas-quickquote` config or `hpasqqacr` tags.** I did not run `az`, because it writes into Vision's `4_Credentials`. I also do not know the live webapp's current `linuxFxVersion`. Gate 17 relayed `v0.6.2-tool2.34-108bbb4`, but I do not know whether v2.35 was published since. Tuesday's AZ-PRE-READ will establish it.
- **Whether Node 22's `require(esm)` prints an ExperimentalWarning.**
- **Whether the `CdpBrowser` from `internal/` is the same class instance as the renderer's.** This is trap 3, and it is only an inference.
- **puppeteer-core 25.0.2's publish date, and whether it is at least two weeks old.** I did not read the registry. The brief makes this §N6.3, conditional on NX-2.
- **The shims restrict `gh` and `az` only through PATH.** The agent could still call the real binaries with the exported config dir. Only the brief's rules prevent that, as in gate 17.
## `--check` output on the real files, verbatim (final run, 2026-10-16 13:2x AEDT)

```
NOTE: the builder's images are on the daemon (qq-evidence-local:amd64-main-e4ce536 qq-evidence-local:amd64-prb qq-evidence-local:prb-node22-pptr25 qq-evidence-local:main-e4ce536 ) — never touched by the gate (brief §13.5)
NOTE: 1-minute load is 223.20 (drafting read 224.77) — amd64 emulation will be slow; Tuesday decides whether to launch now (drafter's report)
NOTE: fleet-monitor has no single live claude — not a negative control
REFUSING: the brief's GH-API-LEG line is still TUESDAY-DECIDES — Tuesday sets READ-ONLY-VISION-TOKEN or NOT-RUN (decision D1) before launch
REFUSING: the brief's AZ-READ-LEG line is still TUESDAY-DECIDES — Tuesday sets TUESDAY-READS, GATE-SHIM or NOT-RUN (decision D2) before launch
REFUSING: no 'QA/Vision-gate18|tuesday-agent@agentmail.to|…' line in /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/inbox_routing.conf — answers to the gate would have no route. Add it (pattern: the QA/Vision-gate17 line) before launch.
REFUSING: the brief still carries 7 @STAMP@ placeholder(s) (Self-check line and note, AZ-PRE-READ, the RULED lines of D1-D4) — the coordinator re-reads end-to-end and stamps all of them before launch
guards pass (MODEL 40 6 9 7 8 18 22 23 74 63 31 39 10 17 12 78 13 14 15 20 70 82 19 24 53 60 61 62 64 69 75 44 45D 38R 86); coordinator to-do pending (46 47 41 32 as listed above); exiting 46.
  origin re-read 2026-10-16 13:23:23 AEDT: main e4ce536, QQPB 4d6ed6e, refs/pull/8/head 4d6ed6e; docker 29.7.2 linux/arm64; model claude-opus-5-5
  NEG seats (38R, derived live): `74294` (tuesday); `34873` (Datasec/Vision_Sales_Portal); `27153` (QA/NexusAI-batch23);
rc=46
```

Under this load a `--check` run takes about 3 minutes; most of that is the docker reads.

Earlier refusals during drafting were fixed before the final run:
- rc 63: `npm ci --offline --ignore-scripts` was split across two lines in the brief.
- rc 78: the prompt did not contain `linuxFxVersion`.

## Tests on scratch copies (session scratchpad; nothing in `fleet/` touched)
- **Fully stamped brief:** all placeholders filled, GH set to READ-ONLY-VISION-TOKEN, AZ set to TUESDAY-READS with a `linuxFxVersion` AZ-PRE-READ, routing line added. **rc 0, "all guards pass"**, with the pinned-heads block printed. Origin was re-read at 13:27:54.
- **az shim** (fake real binary):
  - Allowed: `account show --query …`, `webapp config show --name hpas-quickquote --resource-group hpas-quickquote-rg --query linuxFxVersion -o tsv`, and `acr repository show-tags --name hpasqqacr --repository hpas-quickquote --orderby … --top 5 -o tsv`.
  - Refused with rc 64: `webapp config set …`, `webapp config show … --linux-fx-version x`, `acr build …`, and `account set …`.
- **gh shim:**
  - Allowed: `api <path>`.
  - Refused with rc 64: `api -X POST …` and `pr view 8`.

## To launch, Tuesday:
1. Re-reads the brief end-to-end. Stamps the SELF-CHECK line and note, the RULED lines of D1-D4, `GH-API-LEG`, `AZ-READ-LEG`, and `AZ-PRE-READ` (under TUESDAY-READS, write the linuxFxVersion she read; otherwise `n/a`).
2. Adds the routing line `QA/Vision-gate18|tuesday-agent@agentmail.to|no` to `fleet/inbox_routing.conf`.
3. Decides whether to launch at the current load (trap 5).
4. Runs: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/cockpit/cockpit.sh add 'QA/Vision-gate18' "bash '/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/fleet/qa-agent/launchers/launch_qa_vision_qq_gate18.sh'"`
