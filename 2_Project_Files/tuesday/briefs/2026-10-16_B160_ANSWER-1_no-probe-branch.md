From Tuesday, 2026-10-16 16:4x AEDT, to B160 SEAT-P. ANSWER to your QUESTION 05:43Z "B160 CI artifact on a branch".
# B160 ANSWER-1: NO probe branch. Take your alternative.

**Ruling:** do not push `b160/ci-artifact-probe` and do not change `ci.yml` on any branch. **SUPERSEDES DO 4's "download the CI package of my pushed branch"** in your brief (`2026-10-16_B160_SEAT-P_mps-pkcs-in-package.md`, DO 4). Your reading of `ci.yml` is right: the package artifact is kept on main only.

**Do instead (your alternative, plus one item):**
1. Prove it on CI with the dotnet job's new publish test, which runs on `ci.yml`'s own SDK, plus the package job's log on your `workflow_dispatch` run. Quote the log lines that show the SDK/runtime version and the Pkcs 10.0.13 file in the publish output, if the log prints them. If it does not, say so.
2. In STATUS, under NOT TESTED, write: "the main-built CI package artifact was not inspected; it exists only after merge". Add a **FOR TUESDAY** line saying the check to run on main's package after the merge, before the hosted deploy: the Pkcs DLL is present and `deps.json` has its entry. Give the exact commands (`gh run download` of main's package run; `unzip -l`; a `deps.json` grep). Tuesday puts that check into the hosted-deploy card's runbook.
3. Everything else in your brief stands: push `b160/pkcs-in-package` only, then the READY line.

Why: a CI change, even on a branch nobody merges, is outside this brief's scope, and it leaves a branch to clean up. The artifact that matters is the one the hosted deploy ships, and that gets checked at deploy time.
