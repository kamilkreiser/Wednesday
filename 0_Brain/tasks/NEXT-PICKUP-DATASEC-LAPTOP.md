---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced WHOLESALE at ~21:15 by the 19:51 seat
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, ~21:15 AEST Monday 2026-09-07. TWO SEATS LIVE. KAM IS ASLEEP.

**Run `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh` before
writing anything — read EVERY line.** Mail UTC ≈ AEST−10. **ROTATION BAND 80–90%; 70% is a
CHECKPOINT ONLY.**

## 🔴 KAM'S LAST INSTRUCTION, 2026-09-07 ~21:00, verbatim
> *"keep working on security review and I will review in the morning when I wake"*

He is asleep. **Nothing tonight is worth waking him.** Both live seats were launched under this
instruction plus his 21:00 ruling. Everything else holds.

## FLEET — 2 live, both verified at rung 5 (pane CONTENT, never a non-zero ctx)
- **`%10` — `Datasec/SecurityReview`.** Five Step-2 delta reviews.
  Mechanism, BY PATH: `/Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/launch_secreview_delta_batch2.sh`
  (`--check` runs every guard without launching). Brief and prompt beside each other in
  `2_Project_Files/fleet/briefs_staged/2026-09-07_secreview-delta-batch2{.md,.prompt.txt}`.
  **Its report lands at a FILE, not in mail** — this project has no inbox and `send_brief.sh`
  refuses it by design:
  `/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/_Working/delta-review-2026-09/_BATCH2_REPORT.md`
- **`%11` — `Datasec/NexusAI`.** RD-361 **ROUND 4**, on Kam's 21:00 `deadlock` ruling.
  Launched via the project's own `Launch_Claude.command`; brief delivered by MAIL and read back
  non-null in BOTH `datasec-nexusai@` and `coagent@` before the launch.
  Brief: `2_Project_Files/fleet/briefs_staged/2026-09-07_nexusai-rd361-round4.md`

## 🔴 KAM'S TWO RULINGS TONIGHT — one is DONE, one is WAITING ON HIM
| Card | Ruling | State |
|---|---|---|
| `rd104-gh-identity-acceptance-false-premise` | **`youcheck`** @ 19:58 | **WAITING ON KAM.** Step-by-step delivered to his panel with both links on their own lines. **His two answers unblock three gate-passed merges. Nothing else does.** |
| `nexusai-rd361-round3-blocker-survives` | **`deadlock`** @ 21:00 | Executed — round 4 briefed and launched. **Delivery still OWED:** the seat writes the ruling onto RD-361 as a comment in its first turn and reports the comment id; then `decision_queue.sh --delivered nexusai-rd361-round3-blocker-survives "<comment id>"`. |

**The two answers Kam owes, so you can act the moment he gives them:**
1. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/environments` — is there a
   **required reviewer** on the `demo` environment?
2. `https://github.com/datasecau/Reporting_Dashboard_Au/settings/variables/actions` — does
   **`CI_DEPLOY_ENABLED`** exist, and what is its value?
**If the switch is ON and `demo` has NO required reviewer, HOLD the merges** — a merge to `main`
then deploys to the demo with no human gate. Any other combination and the merges go on his
existing week-scoped authority. Repo confirmed from the git remote, not composed.

**🔴 THOSE TWO CLICKS ARE WORTH MORE THAN THREE MERGES, and the chain is measured link by link:**
NexusAI releases through `main` (RD-367) · `main` is frozen since 09-01 and **250** commits behind
(the gate's measurement, not the stale 248) · Kam ruled **`mergeup`** on it at 18:58 · the mergeup
is what is blocked · behind it sits a **Release Ready column of 46**, counted through
`2_Project_Files/fleet/board_count.sh` which certified *"limit was 250, so this is a real count and
not a cap"*. Those 46 are the *"tested but not deployed"* items Kam pointed at on 09-07 13:40.
**Do not quote a NexusAI board number from a hand-written query — `board_count.sh jira` takes the
site with NO scheme (`${JIRA_SITE#https://}`), and it correctly REFUSED to total
`statusCategory != Done` because more pages exist.**

**RD-321 — CLOSED, no action.** S45 flagged it as Highest-priority and unmentioned in any artefact,
which is the shape that goes missing. Wednesday read it: **Release Ready, assigned to Kam, updated
2026-09-06** — finished and sitting in the column above, nothing missing. Good raise, boring answer.
(`JIRA_SITE` in the NexusAI `.env` carries **no scheme**; a bare `curl` to it returns HTTP 301 and an
empty body, which reads exactly like an auth failure. Prefix `https://`.)

## 🔴 RD-361 ROUND 3 WAS A NO GO — and round 4 must not repeat its shape
Round 3's fix relaxes the gate only while `firstRunComplete` is absent. **That flag is also written
by three FRONTEND sites during ordinary setup** (`static/js/first-run-setup.js:2796` connection test,
`:3069` validation, `:3494` the "don't show again" checkbox), all before auth is enforced, and the
wizard's tab order puts Log Analytics **before** User Access. **So the bricking path is the intended
journey.** Round 3 also opened **F-2 (Major)**: a deployment that HAD auth enforced serves **open
mode across all 175 routes** if `settings.json` is emptied with backups gone.
**Genuinely closed, and recorded as closed:** F-B / M10, proved by contrast (mutation reds exactly
cell D; restore 23/23). Single-write-site premise verified across **all 678 tracked files**.
**Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round3-tier1/report.md`

## ✅ F-2 CENSUS CELL — **GO WITH FINDINGS @ `f93730c`** (tier-2 re-gate, 22:51). **F-B MUST BE FIXED.**
The cell **can** fail against the real `server.js` — M-A and M-B reproduced on disk. F-2 is answered.

**🔴 F-B (Major), and it is NOT acceptable as a stated limit:** the cell's `stripComments()` runs
`line.replace(/\/\/.*$/,'')` — **and `https://` contains `//`.** It corrupts parsing in **18 of the 80
files, `server.js` and `jsonStorage.js` among them.** The census reads damaged text, so **a writer
sharing its line with a URL is deleted before it is counted** (M-G2 — byte-identical hazard to the
M-B2 the cell catches, **green, in frame**). **acorn is already a dependency.** The gate's closing
line is why it matters: *"fix F-B before the next round rests on this census the way round 4 rested on
the comment."*

**F-A (Major)** — docblock claims *"all 678 tracked files, every extension"*; the cell guards **80
`backend/**.js` = 11.8%.** **But the claim is TRUE today** (re-measured across all 678: exactly two
write sites) — **sound claim, undersized guard.** The docblock must stop claiming 678, and the frame
must at minimum cover **what ships** (M-E2 one directory up and M-H `.mjs` are shipped paths).
**F-C** textual counters miss a computed key, a key-in-variable bulk write, and `??=`.
**F-D (Minor)** the control's title claims *"EACH WAY a writer could bypass"* — a completeness claim
over three shapes when eight more exist; **rename it an instrument-liveness proof, which is what it
is.** **F-E (Polish)** M-B never reaches `bulkWrites`.

**The control question answered properly:** NOT the RD-329 pathology — under M-B2 the census went red
while the control **passed**. **But they are always BLIND together: 0 of 6 blind spots, by
construction**, because the control drives the same `censusOf()` over the same regexes.

**Correction to the builder's red-proof, in both directions:** M-B reddens on `setSettingWrites` 2→1,
so jest stops and **`bulkWrites` — the counter M-B exists to exercise — is never evaluated.** The
red-proof would read identically if that counter were dead. The gate isolated M-B2 (additive) and
proved it live.

**COMMISSIONED to S45 as its LAST item before handover, F-B FIRST if context is short:** acorn instead
of regex stripping, **red-proofed with the matched pair (M-B2 stays RED, M-G2 turns RED)** · docblock
and guard made to agree · control cell renamed · an additive bulk-write cell so `bulkWrites` is
exercised.

**Process note filed as a habit, not a finding:** S45's checkout **moved during the live gate**
(`f93730c` → `ea4d229`). No harm — the gate resolved every SHA by object and never wrote to the tree —
but **when a gate is live on your work, use a separate worktree for the next branch.**

## ✅ RD-148 ROUND 2 — **GO WITH FINDINGS @ `ea4d229`, all three closed** (gate 22:41)
F-1 (Blocker), F-2, F-3 genuinely closed, each verified on a real DOM with a negative control that
flips. **None of the residue is a regression** — every finding proved byte-identical between
`aea410c` and `ea4d229`, per-function. **The cap is spent and did not need a third round.**
Report: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd148-round2-tier1/report.md`
**MERGE HELD — Kam's two GitHub answers gate it, not the verdict.**

**The gate out-built the builder's own argument.** It re-ran A/B/C and added **B2**: round-1 product
code byte-identical, round-1 cells, **only the fixture line changed** — three revoke cells red, seven
render/date cells GREEN. **B1 moves 140 lines so "the fixture did it" stays an inference; B2 moves one
statement and the untouched cells are the control.** Technique worth reusing: when you argue *only X
changed*, build the arm that changes only X.

**N-1 (Major) — the CLASS is still live**: the same defect shape survives in `load()` in the same
file; a failed provisioning load is silent, misrepresents tenant state, and a later unguarded Save
switches SCIM provisioning **off**. Instance fixed, class not. **N-4 — the round's own new STRUCTURE
cell does not guard the risk it appears to guard**: a check that cannot fail, inside the suite built
to stop exactly that. N-2/N-3/N-5 minor. **Commissioned:** N-1 its own ticket (class, not instance);
N-2/3/4/5 aggregated as one per Kam's rule; N-4's cell fixed so it can fail.

**🔴 THE GATE'S VERDICT MAIL ARRIVED WITH A ZERO-BYTE BODY.** Subject carried "GO with findings"; the
findings did not travel. **Measured, not assumed:** the `preview` discriminator with a **same-read
control** — null on that message, 200 chars on all four neighbours in one listing.
**Nothing was lost ONLY because the brief specified a report path on disk.**
**The gap is in the path, and it is Wednesday's to close:** `send_brief.sh` refuses a body under 40
non-space characters, **but the QA agent does not send through it**, so a tier-1 verdict can evaporate
into a subject line. Until that is fixed: **every gate brief keeps the report-path requirement, and a
verdict is read from the report, never from the mail alone.** *(The mail was also tagged
`[Datasec/NexusAI ->]` rather than `[QA ->]`; routing is by subject.)*

**✅ AND THE FIX FROM THE ROUND-4 GATE WORKED, MEASURABLY.** The round-4 brief lacked *"stop any server
you start and prove the port reads 000"*; its gate left a listener that died with its pane. **That line
was added to the RD-148 brief, and at its close both ports already read 000 and listeners held 13 → 13.**
One brief to the next, same night. **Put the line in every QA brief.**

## ✅ ROUND-4 FOLLOW-UP DONE @ `f93730c` — and F-2's cell is at a TIER-2 RE-GATE
All four commissioned items complete, **PASS 2185/2185**. Boundary corrected in **all three**
artefacts (docblock · a superseding commit note, history NOT rewritten · **RD-361 comment 37271 as a
NEW comment superseding 37266**). PREV2 and PREVGEN added to RD-368 (comment 37272) **kept distinct**
— PREV2 charged to round 4, PREVGEN pre-existing and unattributed. F-2's census cell built to the
gate's design and red-proofed **on disk against the real `server.js`** (M-A a third writer → RED;
M-B `server.js:3349` → bulk `writeFile` → RED).
**Re-gate mechanism, BY PATH:** `2_Project_Files/fleet/launch_qa_nexusai_rd361_f2.sh`
(tier 2 = through-code only; wrong-SHA path red-proofed at rc 9 before launch).
**The one question it must answer:** the cell's frame is `backend/**.js`, which is **narrower than
"everywhere the key can be written"** — and round 3 died because a `backend/` sweep could not see
`static/`. **A narrower-than-the-guarantee frame is a finding even though the cell passes.**
It must also rule on the builder's own disclosure that its **control reddens under both mutations** —
sound, or one instrument wearing two names?

**S45 also closed RD-322** (root-guard vacuity; chose RED over `test.skip(asRoot)` and **measured the
thing the choice depends on** — `build.yml` is `runs-on: ubuntu-latest` with no `container:`, so CI is
not root; call accepted) and **parked RD-323 cleanly in a labelled stash**, now resumed.
**RD-130 flagged as possibly stale and correctly NOT touched** — at the campaign tip `DEFAULT_URLS` is
the Container Apps demo URL, not the dead VM, but its frame is the SOURCE at that SHA, not a deployed
revision. Category 2; Wednesday carries it; the tenant question gates that pass anyway.

## 🔴 THE STUDIO SEAT FIXED A REAL BUG IN WEDNESDAY'S OWN TOOL — `safe_push.sh`
Wednesday shipped `safe_push.sh` with **`W=/Volumes/KK_T9_External_HDD/WEDNESDAY` hardcoded**. That
volume is **not mounted on the Studio**, so every run of it there would have exited. She made `W`
self-locating from `BASH_SOURCE` (commit `812008ec`) and kept the dead line one away with the reason,
per the revert rule. **Verified from this seat: it resolves to the same path, so the fix is correct on
both machines.** This is Wednesday violating the portability rule it holds the whole fleet to
([[2026-08-25_travel-drive-stale-pointers]]) inside a tool built to travel — **the second time tonight
a Wednesday seat caught the other's error.** Any new tool gets a self-located root, never a volume.

## ✅ RD-361 ROUND 4 — **GO WITH FINDINGS, THE BLOCKER IS CLOSED** (gate reported 22:21)
`rd-361-round4-s45` @ `400718f`. 2 Major, 2 Minor, 1 Polish — **neither Major blocks.** The Blocker
closes on BOTH forms of the wizard's ordinary path, the `/api/auth/enforce` deadlock closes with it,
**no regression** on F/C2b/E/L1/RST, and **round 4 also closed a hole round 3 had** (state C3: key
stripped, stamp left — r3 SERVED, r4 DENIES). **L4 CONFIRMED UNCHANGED** — identical key list,
identical 5236 bytes, both heads. Report + 24 per-state evidence records:
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round4-tier1/`

**🔴 WEDNESDAY'S COMPLETION CHECK FOUND A THIRD ARTEFACT — the hop earned its place.** The gate named
its frame honestly: *"I read the docblock and the commit message. RD-361 and RD-370 are Jira and I did
not read them."* Wednesday read them. **RD-361 comment 37268 and RD-370's summary are both correct**
(they say the round does NOT close F-2/L4). **But F-1's false sentence is also in RD-361 comment
37266** — *"where they survive, `restoreFromBackupsIfNeeded` already restores authEnforced and the
question never arises. Measured: state L1 comes out ENFORCED."* **The measurement is true; the
generalisation is false** — PREV2 has backups surviving and the question arises. One state measured,
the conclusion written about all of them. **So F-1 lives in THREE places, not two.**

**F-1 (Major)** — the residue BOUNDARY is understated; fix is documentation + RD-368 scope, **no code
change**. The residue is not *"settings lost AND the backup layer with it"*; it is *"the settings state
the gate reads carries no evidence"*, which **includes a restore from any recovery generation
predating the enforce write** — a shape the product itself produces (`writeFile()` backs up before
overwriting, `jsonStorage.js:1817-1820`). **The gate was scrupulous about what it would NOT charge to
round 4:** PREVGEN (that generation surviving alone) serves on BOTH heads, so it is pre-existing.
**F-2 (Major)** — the load-bearing census is guarded by **no test**; *"round 3's failure class one
level down — a census correct when written and undefended afterwards."* Cheap fix, design supplied.

**COMMISSIONED to S45 as a tier-2 follow-up (not a round; the cap is untouched by a GO):** correct the
boundary in all THREE artefacts (docblock · commit message · a NEW RD-361 comment superseding 37266,
never an edit) · add PREV2 **and** PREVGEN to RD-368 comment 37267 keeping them distinct · build F-2's
guard cell with its own tampered-copy control · then mail Wednesday. **Scored 1.0 / 1.0** (scoreboard).

**⚠️ `pane_close.sh` caught a listener dying with the round-4 gate's pane (16 → 15).** Diagnosed, not
waved off: the gate booted 24 servers and **its housekeeping section never claims to have stopped
them**. Harmless — its work was delivered and the two surviving listeners (3098/3099) are the LIVE
RD-148 gate's. **The line is already in the RD-148 brief:** *stop any server you start and prove the
port reads 000.* Put it in every future QA brief.

**🔴 GHOST TEXT THREE TIMES TONIGHT, ALL AT WRAPPED PANES** — NexusAI (`good night`), Security Review
(*"check the Bearer scheme defect in SharePoint, MailFlow and UniversalPrint"* — three components
already reviewed and outside the brief), and the round-4 gate (*"Send Kam a one-paragraph summary of
the verdict"*, an action aimed at the principal). **Detector first, every time; close the pane rather
than clear the line when the agent has wrapped.** All three closed cleanly.

## 🔴 HOW ROUND 4 GOT ITS SHAPE — item 1 FALSIFIED Wednesday and the round is better for it
**Wednesday's inference was HALF right, and the wrong half was the one that mattered.** S45 measured
every byte of every file under the data directory across the full state space, after the second
`new JsonStorage(dir)` returns.

- **CONFIRMED:** for whole-file loss with both backup layers gone (**state L4**), a lost deployment
  is **byte-identical** to a fresh deploy. No predicate over the volume separates them. Measured now,
  not inferred.
- **🔴 FALSIFIED:** that is **not the state the Blocker is about.** `jsonStorage.setSetting()`
  (`backend/jsonStorage.js:1865`) stamps **`authEnforced_updated_at`** in the same write, and **it
  survives deletion of the key itself** — positive evidence auth was once enforced. Rounds 2 and 3
  both walked past it.
- **The candidate:** relax only when `authEnforced` is absent **AND** `authEnforced_updated_at` is
  absent. Correct on F, I, I2, C2 — **it closes the Blocker** — wrong only on L4.

**WEDNESDAY'S CALL, 21:32, reported to Kam and NOT asked of him:** round 4 **continues on the sidecar
predicate**; **item 2's `/api/auth/enforce` carve-out is WITHDRAWN.** Reasoning, so a successor can
check it rather than inherit it: Kam ruled `deadlock` to spend a round **closing the Blocker** — that
objective is unchanged; only the means changed, and the new means is strictly narrower and safer
(no door opened on an auth route, so the takeover question never arises). That is v1.3 execution —
a technical route inside work he commissioned. **The risk trade underneath it was already his:** he
saw F-2 in the BLUF of the card he ruled and authorised the round anyway.

**🔴 ROUND 4 CLOSES F-1. IT DOES NOT CLOSE F-2.** The sidecar dies with the file, so **L4 still
resolves to `allow-open-mode`, exactly as under round 3.** The residue is ticketed in the same
action, routed to the platform layer (RD-363 / RD-368) where round 3's own docblock already pointed.
**Do not let any artefact record round 4 as closing SEC-01 or F-2.** The gate decides F-1.

**What Wednesday ratified and did NOT ratify:** the SHAPE of S45's reasoning is ratified; **the
predicate's correctness in the product is the tier-1 gate's question, not Wednesday's.**

**S45's own control is the best thing in the exchange, and it is now a standing brief line:** its
first run showed F and L4 differing in `.machine-id` and the sentinel — which reads as "a
discriminator exists" and is the opposite of the truth. Both were artefacts of its harness giving
each state a **fresh temp directory**. Re-run with those preserved, as a real restart preserves them,
the two came back byte-identical. **An enumeration harness that constructs its states in different
places manufactures differences that look exactly like findings.**

## ✅ SECURITY REVIEW — DONE, QUEUE DRY, AND IT CORRECTED WEDNESDAY'S OWN CENSUS
**Report (the deliverable Kam reads):**
`/Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/_Working/delta-review-2026-09/_BATCH2_REPORT.md`

**Delivered:** four delta reviews — CypherOneDrive, Teams, CommonValueLibraryCypher,
Cyphercard-Enrolment-App — plus an HPSM **scope verdict**. Headline: **D-OD-01 (High)** — CypherOneDrive's
Graph service root is now supplied at RUNTIME over IPC, the only predicate is `!= CloudConfig.Empty`, and the
OkHttp interceptor attaches the user's delegated Entra token to every request without inspecting the
destination. Three consumers, **one of them a `.java` file a Kotlin-only sweep would have missed.**

**🔴 WEDNESDAY'S CENSUS WAS WRONG, one level above where it caught the predecessor's.** Wednesday
enumerated `Deliverables/Components/*.md` → 32 and treated ALL of them as June baselines. **Only 19 are.
The other 13 were written TODAY by this re-run.** HPSM's "baseline" was written this morning and the
component was scaffolded **2026-08-12**, two months after June — so no June state exists to diff.
The agent proved it three ways (a clean mtime split with no intermediate dates, `README.md:3` scaffold date,
and its own delivery recorded at `PROGRESS.md:123`), not by file date alone.
**CORRECTED ARITHMETIC: the June-baseline delta set is COMPLETE at 19/19. It was never going to be 20.**
*(`delta-review-2026-09/` holds 20 non-`_` files — the 19 deltas plus `hpsm-main.md`, which is the scope
verdict, not a delta. Do not count it as a twentieth.)*

**🔴 CARDED FOR KAM — `hpsm-credential-bearing-prd-outside-every-snapshot`** (rec `structural-look`,
**default HOLD**). `Source_Code/HPSM-main/.gitignore:11-13` says in the developers' own words that a
**credential-bearing document** lives at `../1_Project_Definition/Source_Documents/` — outside the repo and
outside every snapshot either review was built from. **Nobody has ever opened it.** The agent reported it
structurally and correctly did not go looking. *(The prior-ruling gate refused this card on the words
"hpsm"/"credential"; Wednesday read all seven matches — telemetry/SOW, a Secuura password, and panel messages
about slides, Purview and Attio — and none is this subject. Override reason is stated as that measurement in
the card's BLUF.)*

**THE QUEUE IS DRY — say so rather than manufacture study.** What remains is decisions, not agent work:
RD-18 (Australian Privacy Act package), whether to re-issue the June deliverables 00/03/04/09/10 against the
219-finding register or let 12+13 stand, and the live GitHub/Azure/Entra pass still blocked on the unresolved
tenant question (`fc05dcdd` vs `0c57ab37`).

## SECURITY REVIEW — the ORIGINAL frame, kept because the correction above is the lesson
    32  components with a June baseline (Deliverables/Components/*.md)
    15  have a 2026-09 DELTA review
    10  have a 2026-09 VERIFICATION pass
     2  PARKED by Kam 2026-09-07 10:44 (both Vision components)
     5  REMAIN — CypherOneDrive · Teams · CommonValueLibraryCypher · Cyphercard-Enrolment-App · HPSM

**🔴 `hpsm-main` was NOT in the predecessor's list of four.** It has a June baseline and no 2026-09
output; Wednesday found it only by enumerating the frame. The brief names it as Wednesday's
inference and gives the agent permission to skip it with a reason. **This is the census family
firing on Wednesday's own handover** — the list was right about batch 2 and silent about the tree.

## WHAT THIS SEAT DID, and the one thing worth carrying
- **Caught a `good night` at the wrapped NexusAI pane's prompt** — detector said ghost text, nobody
  typed it. Rung 2 of the ladder. **Closed the pane rather than clearing the line** (a cleared prompt
  can be re-populated; a closed pane cannot). Listeners 13→13, port 3001 dead before and after.
- **🔴 THE CHAT-LOG UNION IS NOT OPTIONAL, AND HERE IS THE MEASUREMENT.** A push conflicted with the
  Studio seat. Union on `(ts, text)` across **both conflict sides AND a pre-flight backup**:
  **1663 / 1664 / 1665 in — 1667 out.** Every source was missing something, and **the backup alone
  held one message neither conflict side had.** Taking either side — the default resolution — would
  have deleted it. Back BOTH `chat_log.json` and `decisions.json` to the scratchpad before any
  multi-step git sequence, every time. The union script is at
  `/private/tmp/.../scratchpad/union_chat.py` for this session only — **rewrite it, do not hunt for it.**
- **Digests were conflicted too. Resolved from SOURCE** (re-ran `boot_digest.py` on the lesson files)
  rather than picking a side — a derived artefact comes from its source, not from whoever won.
- **Boot measured `ctx:27%`** on the by-tier digest (WED-139 duty).

## ⚠️ TRAPS — the first one FIRED tonight exactly as written
1. **🔴 A T9 LAUNCH HITS A FOLDER-TRUST DIALOG AND NO GUARD CAN SEE IT.** The Security Review launch
   showed *"Is this a project you created or one you trust?"* with **`No, exit` preselected**, and
   sat there. Every wrapper guard had passed. **Only reading the pane caught it.** Answer with
   `tmux send-keys Down` then `Enter`. Once trusted, later launches skip it. **Verify EVERY launch at
   the pane, always** — a check that cannot observe a dialog appearing after `exec` cannot fail.
2. **`launchers.conf` points at DevMASTER, which is not mounted here**, so `cockpit.sh launch` and
   `brief_and_launch.sh` cannot start a T9 seat. Launch by hand with `tmux split-window`, then
   **`tmux set-option -p -t <pane> @cockpit_name '<Client/Project>'`** or `cockpit.sh say` cannot
   find the pane. **Do NOT rewrite `launchers.conf`** — it is shared and correct for the Studio.
3. **`send_brief.sh` has three gates and all three fired on me tonight, correctly:** a literal
   `PROVENANCE:` line (not `## PROVENANCE`); **absolute** paths or an explicit owner in every
   citation; and the heading `RULED BY KAM, NOT YET IN AN ARTEFACT` with bullets shaped
   `- <card-id>: "<ruling verbatim>" -> must land in <artefact>`. Budget three refusals.
4. **No `cd` in a Bash call** (`pretooluse_no_cd.sh`). A wrapper that legitimately needs `cd` is
   written with the **Write tool**. **`git -C $VARIABLE <writeverb>` is refused** — write git paths
   literally.
5. **Before pulling, discard the ten regenerated dashboard feeds**, then pull, then push. Never
   `git add -A 0_Brain/dashboard/data` — stage `chat_log.json` and `decisions.json` BY NAME.
   **Never `git checkout <sha> -- 0_Brain/dashboard/data`** — that is what destroyed four of Kam's
   rulings this afternoon.
6. **Ghost text has now appeared three times at NexusAI prompts.** Run
   `2_Project_Files/fleet/cockpit/pane_prompt_check.sh <pane-%ID>` before reading anything at a
   prompt. `pane_close.sh` refuses a name that does not resolve to a tty — pass the `%ID`.

## STANDING
**Kam's week-scoped grants (read as through Sunday 2026-09-13):** merge on Wednesday's word once the
gate passes · deploy · board judgement calls. **🔴 THE PRODUCTION LIFT IS SECUURA ONLY** — 12:07
lifted, **narrowed at 12:10 to *"Only secure"*. Datasec has NO production grant. This is the Datasec
seat.** Ticket CREATION aggregates (one larger ticket per logical path, 13:23). Every analysis record
carries **FOUND / TESTED / HOW** with the controls named under HOW (18:56:36). **Kill anything that
queries Azure credits** (13:06 — five raises, closed).

**NAME THE FRAME** in any sentence claiming completeness — the third failure family, filed today,
and it beats both existing defences because both controls pass and the number really is read from
the source. It caught Wednesday's own handover tonight (the missing fifth component).

Taps ≤200 chars, pointer only, mail FIRST and verified by non-null `preview`, THEN tap.
`<<'EOF'` or the Write tool for every body. **Never delete — quarantine.** Search before you file,
by SYMBOL / PATH / ERROR STRING.

**TWO WEDNESDAYS LIVE:** Studio owns **Secuura**, this seat owns **Datasec**. One repo, one
dashboard, one chat panel, **ONE USAGE LIMIT**. Do not write the shared files (`NEXT-PICKUP.md`, the
daily note, `_ledger.md`) — they are hers this session. Panel messages open `[LAPTOP / Datasec]`.
Secuura mail in the shared inbox: **read the subject, not the body, and leave it.**
