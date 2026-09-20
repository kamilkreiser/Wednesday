# BRIEF (STAGED, NOT SENT) — RD-574: rescue the 28 seam-dependent cells on their OWN branch

> 🔴 **RE-VERIFY BEFORE SENDING. Four things move and this brief is written ahead of time on purpose:**
> 1. **`main`'s head** and **RD-516's branch head** — read `git ls-remote origin` in the same action as the send.
> 2. **The 27 named in §6 (plus NEW-1 = 28 in total)** — re-read §6 of `docs/rd516/RD-516-gate-brief.md` **at the then-current head**. That is the IN-REPO path (the repo root IS `2_Project_Files`); a `git show <sha>:2_Project_Files/docs/...` returns "does not exist".
> 3. **The usage gauge** — `fleet/usage_gate.sh --check` in the same action as the launch decision. Kam's lift of the 95% stop was for the night of 2026-09-20 only, undated; it is RE-ASKED, never assumed.
> 4. **Whether S73 or a successor already took some of them.** The three already done (rd545 `A4`, rd523 `E2`, `E2-happy`) are NOT in scope; check nothing else has been.

## BLUF — what this seat does, and why it merges FIRST

**Rescue the 28 seam-dependent test cells — the 27 named in §6 of the gate brief PLUS NEW-1 (the 28th, classified after that file was committed; see its own section below), on a NEW branch off current `main`, which merges BEFORE RD-516.** They pass on `main` today and break the moment RD-516's endpoint policy merges, so they are a **MERGE BLOCKER, not follow-up** — and because each fixture change is **inert** (it passes with and without the policy), the branch lands on `main` harmlessly ahead of the policy.

**RD-516's own acceptance clause depends on this work:** *"The seam-dependent cells listed in §6 are on `main`."* **Read that as 28: S73 classified NEW-1 by reading it after the brief was committed, and deliberately did NOT edit §8 because committing would have moved the head the gate was measuring. The §8 "unclassified" line is a ONE-LINE FIX OWED after the verdict.**

## 🔴 YOUR BRANCH MUST CARRY THE TEST HELPER TOO — the gate PROVED this and it corrects the earlier ruling
**The rescue recipe needs `__tests__/helpers/rd516-net-harness-preload.js`, and that file does NOT EXIST at `60c76d7`** — it is added by RD-516's branch, along with `backend/services/aiEndpointPolicy.js`. The tier-1 gate measured this as §5(a).

**So "the 28 merge first" is not executable as a fixture-only change.** The shape that works, and it keeps every property the split was for:

> **Your branch = the TEST-SIDE additions only: `rd516-net-harness-preload.js` (and any helper it needs) PLUS the 28 fixture edits. No `backend/` product file. All of it inert.**

**Why that is still inert, and how you prove it:** nothing in the product imports the preload — it is loaded only by a suite that asks for it (`-r` or `preload:`), and the suites that ask for it are in your own branch. **The acceptance criterion is unchanged: each affected suite run BEFORE and AFTER at current `main`, identical results, empty per-cell diff.** The gate's own control is your reference point — with the policy absent, all 105 cells across the four suites PASS.

⚠️ **Tell me if RD-516's branch and yours both add the preload** — they will, and the resolution (same content, one of them becomes a no-op at merge) is mine to sequence, not yours to improvise.

## THE RECIPE — do not re-derive it; it is proven on R7 in RD-516's branch

Read it from §6 of `docs/rd516/RD-516-gate-brief.md` rather than from this brief, so there is one copy and it cannot drift. In outline, per cell:
1. load `__tests__/helpers/rd516-net-harness-preload.js` as the boot's `preload`;
2. `RD516_HOSTS` → map the allowed Azure NAME to a **TEST-NET-1** address (`192.0.2.x`) — the policy reads it as PUBLIC and allows it on the strict branch;
3. `RD516_INTERCEPT` → map the same NAME to `127.0.0.1:<that suite's existing listener port>`;
4. point the boot/cell at that NAME.

🔴 **CHANGE NOTHING ELSE. THE ASSERTION DOES NOT MOVE.** Only the endpoint's spelling changes.

## 🟢 THE 28th — NEW-1, AND IT IS THE LIGHTEST OF THE SET
**`ai-config-aoai-save.test.js:160-161`** drives ai-test anonymously with `azureOpenAIEndpoint: http://127.0.0.1:${refusing}` plus a key, and asserts `status 200` / `provider azure-openai`. **A caller-named loopback literal, so the policy refuses it `ADDRESS_LOOPBACK` → 400. It IS in the set.**

🟢 **It needs `RD516_HOSTS` ONLY — NO `RD516_INTERCEPT`, no listener, no seam.** Its subject is *which provider was tested*, not whether the endpoint answered; the port it names is **deliberately a refusing one**, so the cell already tolerates a failed dial and a refused connection still returns `200 success:false`. **It only needs the endpoint to PASS the policy.** Do not add an interception it does not need.

⚠️ **AND IT WILL LOOK DIFFERENT FROM THE OTHER FOUR FILES:** that suite **spawns the server itself** (`spawn(process.execPath, [SERVER])` at `:62`) instead of using `bootServer`. **So the preload is wired by adding `-r <preload>` to the spawn ARGS, not by a `preload:` option.** Expect that difference; it is not a mistake.

## ACCEPTANCE — inertness, per suite, measured not asserted

**For every suite you touch: run it BEFORE and AFTER at current `main`, and show identical results with an EMPTY per-cell diff.** If any result moves, the fixture changed behaviour and **that is a finding, not a fixture** — stop and mail it. This is the criterion the three completed cells were held to (`f09836d`, `f4ef7a7`); match it.

## HARD STOPS — mail and STOP, do not work around

1. 🔴 **A cell whose SUBJECT really is the loopback address** cannot have its endpoint moved with its assertion intact. **Stop and name it.** It is not yours to convert into something else.
2. 🔴 **Do NOT touch `backend/services/aiEndpointPolicy.js`, `backend/server.js`, or `backend/services/aiTestCredentials.js`.** The policy is RD-516's and **RD-518's fix round (round 2 of 2 — a third is Kam's, C-62) is queued on `server.js`.** Your scope is the four test suites' fixtures.
3. 🔴 **Do NOT "tidy up" `SEAM_OFF` into `RD516_INTERCEPT`.** Its ABSENCE is SEAM-2's control. Adding it destroys the only thing that makes a silently-inactive interception loud. The cell says so; believe it.
4. 🔴 **The seam serves `http://` only.** It redirects a TCP socket to a plain-HTTP listener, so an `https://` endpoint fails the TLS handshake (measured: it presents as a boot hang). Every affected harness uses `http://` today. **A cell that needs `https` is RD-583's TLS work — stop and say so; the two are one dependency.**
5. **Do NOT write `R3`.** Its subject is the address pinning that does not exist (RD-584), and **it must never be built on the interception seam** — the harness's interception is the same manoeuvre R3 exists to detect, so such a cell tests the harness against itself.
6. **Do NOT fix `R7`, `R8` or `R10(i)`.** They are ticketed elsewhere (RD-585, RD-541/C-106, RD-583) and are deliberately left failing or skipped so the gaps stay visible.

## THE PARTITION, from both sides

**Yours:** `__tests__/rd464-aoai-health-routes.test.js`, `__tests__/rd486-ai-test-key-forwarding.test.js`, `__tests__/rd523-aoai-redirect-refused.test.js`, `__tests__/rd545-ai-test-limit-survives-ai-off.test.js` — fixtures only.
**NOT yours, and another seat may be live in it:** RD-516's branch and every `backend/` path above. **If you need a change there, mail me — do not reach in.**

## PRIOR-WORK CHECK (standing line, and it is in-path here)

Before changing any cell, read what it was built to prove — `git log -S` on the assertion, the suite's own header, and `1_Project_Definition/CLARIFICATIONS.md` for the ticket ids it names. **Your READY must carry a PRIOR WORK section or it comes back.** Three cells are already done to this standard; read one of them first as the worked example.

## REPORTING

Mail `tuesday-agent@agentmail.to`, subject `[Datasec/NexusAI -> Tuesday] ...`. **Your first mail precedes your first hold; a turn never ends on an unmailed report.** Send the per-suite inertness pairs as numbers, the cells done by name, and anything you stopped on. **Ends at READY FOR QA** — the gate is mine to commission.


RULED BY KAM, NOT YET IN AN ARTEFACT
- rd104-gh-identity-acceptance-false-premise: "(ruled; see the card for his words)" -> must land in the RD-104 ticket as a comment. NOT this brief's subject and NOT yours to action — carried here because the gate is right that you should know an undelivered ruling exists on your project. If you touch RD-104 for any reason, land it first and mail me the comment id.

(Discharged since the last brief, for completeness: nexusai-degraded-flip-and-live-deployments — his 2026-09-21 08:32 words released the deployment-count requirement, and nexusai-rd516-undici-dependency-for-address-pinning — ruled (c), already in force.)

PROVENANCE:
- The named 27 cells in §6, by suite and cell (NEW-1 is the 28th and is NOT in that file) | `docs/rd516/RD-516-gate-brief.md` §6 at `f4264e5` (in-repo path; the repo root IS `2_Project_Files`) | read 2026-09-21
- The four-step rescue recipe, proven on R7 | same file, §6 | read 2026-09-21
- The acceptance clause "the seam-dependent cells are on main" | same file, §5 | read 2026-09-21
- The three cells already done (rd545 A4; rd523 E2, E2-happy) | commits `f09836d` and `f4ef7a7` | read 2026-09-21
- `rd516-net-harness-preload.js` is ABSENT at `60c76d7`, so your branch must carry it | tier-1 GATE VERDICT §5(a), mail `[QA/Datasec-NexusAI -> Tuesday]` 2026-09-20T15:02:12Z, DKIM-verified | read 2026-09-21
- The §6 27 pass on main with the policy neutralised (105/105 across the four suites) and exactly 27 red with it on | same gate verdict, §5(c) | read 2026-09-21
- The seam serves `http://` only; an `https://` endpoint fails the TLS handshake | S73 mail 2026-09-20T14:00:41Z, DKIM-verified | read 2026-09-21
- `SEAM_OFF`'s ABSENCE from `RD516_INTERCEPT` is SEAM-2's control — do not "tidy" it in | same mail | read 2026-09-21
- NEW-1 is the 28th, needs `RD516_HOSTS` only, and its suite SPAWNS its own server (`spawn(process.execPath,[SERVER])` at `:62`) so the preload wires as `-r` | S73 wrap mail 2026-09-20T14:33:25Z, DKIM-verified | read 2026-09-21
- `main` = `60c76d7`; `rd-516-ai-test-ssrf-s73` = `f4264e5`; no rd574/rescue branch exists at origin | `git ls-remote origin` | read 2026-09-21 08:3x
- The 28 are a MERGE BLOCKER on their own branch merging BEFORE RD-516 | Tuesday's ruling 2026-09-20T14:03:09Z, quoted verbatim in the gate brief §5 | read 2026-09-21
- The usage stop is lifted and the priority is resubmission | Kam, panel 2026-09-21 ~08:3x: "Don't worry about the usage gate... Please do everything you can to get Nexus AI ready for resubmission." | read 2026-09-21
- RD-518's fix round is queued on `backend/server.js` (round 2 of 2; a third is Kam's, C-62), which is why your scope is test-side only | `fleet/briefs_staged/nexusai_rd518_fix_round2.md` + NEXT-PICKUP DELTA 46 | read 2026-09-21

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 08:57
