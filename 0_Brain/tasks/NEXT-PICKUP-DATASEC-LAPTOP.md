---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced wholesale at the 17:0x pickup (previous version claimed a gate was running that was not)
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, 18:0x AEST Monday 2026-09-07 (refreshed at the 50% checkpoint)

## 🔴 THE CORRECTION THIS SEAT MADE TO THE HANDOVER IT INHERITED
The 17:0x version said **"RD-361 round-2 TIER-1 RE-GATE running (launched 17:0x)"** and set a
**3-deep gate queue**. **No gate was running.** Measured four ways, each with a positive control so
that an absence was not confused with a blind instrument:

    tmux list-panes            3 panes: Wednesday, NexusAI, monitor. No gate pane.
    find '*rd361*' '*rd-361*'  0 hits.  CONTROL: find '*ks930*' -> 3 hits. Instrument fires.
    grep -rl RD-361 briefs/    0 hits.  CONTROL: grep -rl KS-930 -> hits.
    alerts.log                 no QA event after 07:53Z; every brief written today was Secuura.

Two readings survive and this seat cannot discriminate between them from disk: an in-process gate
that died with its author's rotation (leaving no pane, wrapper or brief), or a recorded intention.
**The operative fact is the same and it is the only one asserted anywhere: no gate had run and no
gate output existed.** Both gates were then launched for real, each verified at rung 5 by its pane
naming its own brief (never a non-zero ctx) — and **both have since REPORTED**; verdicts below.

**The general rule this earns, and it is already a lesson:** a handover records a mechanism by its
**PATH**. Every launch wrapper below is named by path for exactly that reason.

## FLEET — EMPTY. Every agent wrapped or reported; every pane closed. Panes: Wednesday + the monitor.
All three gates returned and the builder wrapped. Closes went through
`2_Project_Files/fleet/cockpit/pane_close.sh`; **listeners 13 → 13 on every one**, and the ports the
handovers named (3001/3111/3121) were already 000 beforehand — nothing died with a pane.
**Ghost text appeared at THREE prompts today**, each proposing the salient next action (`good night`
at the wrapped builder; the RD-361 follow-up ticket at its gate; `Wait for Wednesday's reply` at the
RD-362 gate). Detector called all three `SUGGESTION`; a fourth pane returned `prompt empty`, so it
discriminates. **Run `pane_prompt_check.sh` before reading ANY prompt line.**

## 🔴 RD-362 VERDICT — GO-with-findings, AND THE TICKET MUST NOT CLOSE AS "CONTAINMENT ACHIEVED"
3 Major, 3 Minor, 2 advisory, **no Blocker**. The change is a strict improvement; the gate's own words:
*"blocking it would leave the markdown report shipping in the customer image, which is worse than any
finding below."* **But the exposure is materially wider than the ticket claims:**
1. **SEC-03 redacted 1 of 5 carriers.** Four unredacted full copies remain tracked — the `.docx` and
   `.pdf` under `docs/`, and **a SECOND COPY under a different name in `Final Documents/Working
   Documents/`, inside the build context** and matched by no ignore pattern (no `COPY` reaches it, so
   not in the image). All four carry both pointers SEC-03 just redacted.
2. **🔴 `docs/runbooks/git-history-scrub.md` SHIPS INSIDE THE CUSTOMER IMAGE and carries the recovery
   pointer in pasteable `<commit>:<path>` form.** Dereferenced to a live blob (type and size only,
   never content); the introducing commit resolves, is an ancestor of head, its tree holds 2 entries
   under the key directory and its parent holds 0. **SEC-04 excludes the report and ships the map.**
   Pre-existing, not a regression — **but squarely inside SEC-04's own threat model** ("anyone who can
   pull or inspect an image layer").
3. **F4 MAJOR — the redaction's own claim is falsified inside the file it edited.** A short-form hash
   survives ~8 lines above the redaction and the key directory is named ~12 lines below it; the hash
   is live and IS the removal commit. Removal commit + directory name = the same recipe, shorter. The
   test's pattern only matches 40-hex preceded by `git show`, so it cannot see it. **Same class as the
   `:553` miss the builder found, one turn later.**
4. **F6 MINOR** — `SESSION_NOTES_*.md` is root-anchored, so four `docs/SESSION_NOTES_*.md` still ship;
   one carries 10 GUID-shaped strings. **F5 MINOR** — partial PEM material remains (~40%, public
   portion, NOT the private scalar; the gate explicitly declines to call it key recovery).
5. **The runtime-read control cell is a spelling check.** `expect(lines).not.toContain('*.md')` —
   exact string identity against four literals, computing no exclusion. Fires on literal `*.md`,
   **silent on `**/*.md`, `*.[Mm][Dd]`, `*.m?` and `PRIVACY.*`**, all of which break the two live
   routes. Found by tampering five ways with each tamper asserted to have landed.

**Merge: HELD, same reason as RD-363 — the target is a frozen `main` and RD-367 is unruled.** A merge
would not close the exposure anyway; only a rebuild/republish does, and that is Kam's.

**🔴 THE NEXT SEAT'S FIRST JOB — Wednesday CANNOT do it: tracker access is READ-ONLY.**
File these as tickets on the RD board (aggregated per Kam's 13:23 rule — the carrier story is ONE
logical path), searching by SYMBOL/PATH first and saying so, with both controls:
`git-history-scrub.md` shipping the map · the four unredacted carriers · F4's short-form hash ·
F6's SESSION_NOTES · and the control cell's upgrade from string-identity to a computed exclusion.
**And RD-362 itself must be re-scoped so it cannot close as containment achieved.**

## GATE QUEUE AFTER RD-362 — 2 left, both Wednesday's to fire, neither needs the builder
1. **RD-329 @ `2e78c76`** — the public `/api/health` allow-list guard. **No red-proof exists and the
   builder said so**: the code has been correct since 2026-04-25, so it passes at the base by
   construction. Its discriminator is the control cell. **And the real finding is not code —
   `nexusai-staging` is serving a build older than the fix**, so remediation is infrastructure
   (redeploy/stop), category 2, not available to a code-scoped session.
2. **RD-148 @ `aea410c`** (`rd-148-scim-revoke-ui-s43`, 2164/2164).

## 🔴 TWO CARDS ON KAM'S DESK — nothing moves on either until he rules
- **`nexusai-rd361-blocker-vs-nogo-cap`** — rec `round3`, **default HOLD**. The Blocker below.
- **`nexusai-rd367-frozen-trunk`** — rec `mergeup`, **default HOLD**. `main` frozen since 2026-09-01
  with 247 commits ahead of it; gitleaks runs on `main` only, so six days are unscanned; the demo
  deploys from `main`. **The builder's framing, adopted: this and the round-3 card are the same shape
  — the queue cannot move without a ruling, and neither looks urgent from outside.**

## 🔴 BOTH GATE VERDICTS — the first one is a decision on Kam's desk
- **RD-361 round 2 @ `1149d1c`, tier 1 → NO GO.** One **Blocker**, two Majors.
  **F-A (Blocker):** the sentinel is written on boot 1; `authEnforced` only when the admin finishes
  setup; **any restart in that window permanently bricks a fresh deployment.** Measured at the wire:
  503 on every route *including* `POST /api/auth/enforce`, the one route that could write the key.
  Only exit is hand-editing `settings.json` on the customer's volume. Control: an empty volume serves
  200. Fail-closed, so **not** a leak — an availability blocker on a Marketplace offer's first-run path.
  **F-B (Major):** flipping the sole producer of `dataDirFallbackActive` (`jsonStorage.js:847`) leaves
  `auth-gate-fail-closed.test.js` **20/20 green** — the case-D fix is unguarded. One-line remedy.
  **F-C (Major): RESOLVED by Wednesday from the board — see below.**
  🔴 **ROUND 3 IS KAM'S** (round 2 of 2 under his 2026-09-05 cap). Carded as
  `nexusai-rd361-blocker-vs-nogo-cap`, recommendation `round3` (Blocker + F-B only), **default HOLD**.
  **Do not start the fix. Wednesday will not merge it — the gate did not pass.**
- **RD-363 / SEC-07 @ `b0dec96`, tier 1 → GO-with-findings**, with a **HARD BLOCK on publishing any
  offer version** until its F-2 (redeploy-over-an-existing-vault; purge protection landing
  irreversibly on existing customers' vaults) is resolved. Publishing an offer is Kam's class anyway.
  **Wednesday is HOLDING the merge too, and not because of the change:** the target is `main`, which
  RD-367 says is frozen 247 commits behind, so merging one branch into it is the first move of the
  unruled branching decision. **RD-363 is not in question — where it lands is.**

## F-C RESOLVED — the code comment AND Wednesday's brief pointed at the wrong ticket
`authEnforcement.js:112` says the durable fix is *"SEC-01 remediation 3, tracked on RD-363."*
Wednesday queried Jira read-only (standing grant), with a control:

    RD-363 = SEC-07/08/11 — Marketplace deployment TEMPLATE hardening   [Testing, blocker/horizon-1/security]
    RD-361 = SEC-01/05/06/09/10/15 — the auth gate fails open            [Testing]

**SEC-01 belongs to RD-361 itself.** Residue search: `text ~ authConfigs` → 2 hits (those two tickets),
`text ~ SEC-01` → 3, **control** `text ~ "Key Vault"` → 15 — all under the 20 limit, so untruncated.
**The platform-layer residue has NO ticket of its own.** Commissioned to the builder as ONE ticket
(Kam's 13:23 aggregation rule) stating what was searched, plus a repoint of the code comment.
**Wednesday's own RD-361 brief §6 carried the same wrong pointer, taken from the builder's mail
without checking it** — owned in the mail, ledgered.

## GATE QUEUE — 2 remaining, fire as slots free
1. **RD-362 @ `920e067`** — carry the builder's own framing into the brief: **the redaction removes the
   recipe; the blobs stay reachable in git history until RD-55 lands.** The gate must not credit more
   closure than shipped.
2. **RD-329 @ `2e78c76`** — the allow-list guard. Note: **no red-proof exists and the builder said so**;
   the code has been correct since 2026-04-25, so it passes at the base by construction. Its
   discriminator is the control cell.
3. **RD-148 @ `aea410c`**.

## ⚠️ TRAPS — the first is NEW and will cost you 20 minutes if you do not know it
1. **🔴 A T9 QA LAUNCH HITS A FOLDER-TRUST DIALOG AND NO GUARD CAN SEE IT.** Every wrapper written
   before today hardcodes `/Volumes/DevMASTER/...`; DevMASTER is not mounted here, so the two
   wrappers above are the first T9 ones. On the FIRST launch, Claude Code showed
   *"Is this a project you created or one you trust?"* with **`No, exit` preselected**, and sat
   there. The wrapper's guards all passed — brief, prompt, directive, paths — and the agent was
   still blind. **Only reading the pane's content caught it.** Answer with `Down` then `Enter`.
   Once trusted, later launches skip it (the RD-363 launch did).
   **This is a check that cannot fail, in a new costume: no guard in the launch path can observe a
   dialog that appears after `exec`.** Verify every launch at the pane, always.
2. **`git -C $VARIABLE <writeverb>` is REFUSED** — the hook matches literal text and cannot resolve a
   shell variable, so it fails closed. **Write git paths literally.** It also fires on a commit
   message that merely *describes* a git command → write the message to a file and use `-F`.
3. **No `cd` in a Bash call** — `pretooluse_no_cd.sh` refuses it. A wrapper that legitimately needs
   `cd` is written with the **Write tool**, not a heredoc.
4. **Ghost text has appeared TWICE at the NexusAI prompt.** Run
   `2_Project_Files/fleet/cockpit/pane_prompt_check.sh <pane>` BEFORE reading anything at a prompt.
   Checked at this boot: **`Datasec/NexusAI: prompt empty`** — clean.
5. **`2_Project_Files/fleet/state/` is GITIGNORED.** Both new wrappers live there, so they do NOT
   travel with a clone and no git-based search will find them. Consistent with every existing
   wrapper, so this seat did not move them mid-flight — **but the move to a tracked path is owed**
   and should not be done while a gate is live on the mechanism.

## ✅ ANSWERED — `main` IS the integration branch, and the 247 commits are the FINDING (RD-367)
This was raised as an open question at 17:2x and the builder settled it in three minutes.

    origin/main                            a9a8cb6e…  frozen 2026-09-01
    rd-361 / rd-363                        249 / 248 commits AHEAD of main
    RD-363's OWN change (vs its parent)    3 files, +118 / -5
    RD-363 diffed against main             254 files, +59,000 / -1,034

**`main` is the trunk by every mechanical definition** — 0 behind / 247 ahead, a strict ancestor,
and its history is merge commits (RD-135, RD-136/137/138, RD-121, RD-116). It simply has not been
fed since 1 September. **Filed as RD-367 (High, needs-decision): it needs a branching-model ruling,
not a code change.** There is **no documented branching model anywhere** in the repo (searched
JIRA.md, HISTORY.md, README.md, DEPLOYMENT_GUIDE.md, docs/runbooks/).

**Three consequences, separate failures:** (1) `gitleaks.yml` is `main`-only, so **six days of
commits are unscanned** — now the SOLE live explanation for the F-16 credential surviving;
(2) `deploy-demo.yml` deploys from `main`, so nothing built since 09-01 is deployable by the normal
path; (3) `npm-audit.yml` (`branches: ['**']`) is the only workflow that runs on the campaign branch.

**Standing line for every NexusAI gate brief, adopted verbatim from the builder:**
> Base every NexusAI gate on `parent..head` of the branch under test, never on `main`. main is the
> integration branch but is currently ~247 commits behind the work; diffing against it reads other
> people's merged work as the change under test.

**NexusAI's mainline is `main`, NOT `develop`** — do not carry the Secuura convention across.
**RD-367 is also why Wednesday is holding the RD-363 merge** (see the verdicts above).

## CLOSED SINCE THE LAST PICKUP
- **The cat-1 count is settled: 96, not 97.** Category-2 is 18 → 19. **Only RD-50 moves** — its own
  scope note puts execution in the Feedback System and Lead Bot folders, a hard-rule-1 boundary, not
  a capacity question. RD-69 and RD-364 were checked and are genuinely category 1; RD-362 is MIXED
  (its in-repo half shipped, its rotation half was always category 2). **This is the number Kam is
  held to and it has been mirrored to his panel.**
- **RD-362's in-repo half SHIPPED @ `920e067`** — SEC-04 closed, SEC-03 partly. SEC-02 and both
  rotation halves stay open (rotation needs the dev-tenant admin: category 2).

## 🔴 STILL STANDING — four conclusions given to Kam that CHANGED, carried forward verbatim
1. **✅ RETRACTED 17:4x — `actions/checkout@v7` EXISTS. The "decorative gate" diagnosis is DEAD.
   Do NOT act on it and do NOT let it come back.**
   The 17:0x version of this file said v7 was "a major that does not exist", so the workflow "fails
   before the scanner runs." **False.** Measured twice independently: the RD-363 QA gate via the
   GitHub API (`releases/latest` → **`v7.0.1`, published 2026-07-20**, GA June 2026), and **Wednesday
   again in this session** — same endpoint, plus `repos/actions/checkout/tags` showing majors
   **v1–v7** with `v4` as the control. **Wednesday also re-derived NexusAI's own pins: 4 × v4 and
   1 × v7 — and the v7 pin IS `gitleaks.yml`, the MOST CURRENT major in the repo.** Third
   corroboration from inside the fleet: Secuura's gate PR #781 deliberately pins four
   `checkout@v7` at v7.0.0.
   **🔴 THE ACTIVE RISK IS NOW THE OPPOSITE ONE** — the gate's words: *"the stated diagnosis, if
   acted on, means DOWNGRADING A WORKING WORKFLOW."* If a ticket appears telling anyone to move
   `gitleaks.yml` off `@v7`, it is wrong: put the measurement on it and close it.

   **What SURVIVES — narrower than the retraction is wide. Do not over-withdraw:**
   - **The estate-wide pin census stands** (v4×35, **v7×25**, v2×8, v3×3, v5×1, no v6): a count of
     files, unaffected. **"No v6" was always about which majors the repos PIN, never about which
     majors exist** — not retracted.
   - **RD-367 stands entirely and is now the SOLE live explanation:** gitleaks is `main`-only and
     `main` has been frozen since 2026-09-01, so **six days of commits are genuinely unscanned.**
     Independent of the version claim — it got MORE important, not less.
   - **`terraform.tfstate.backup` still carrying F-16 credentials** — observation stands, one of its
     two explanations gone; it now rests on RD-367.
   - **A third member of the class, from the SecurePDF verification pass:** that repo's
     `gitleaks.yml:5` triggers on `master` while myPKI's uses `main`, so a copy-paste between repos
     silently stops scanning pushes. **The scanner is fine; the TRIGGER is what fails, every time.**
   - **Scope boundary, carried honestly:** the gate verified this for NexusAI and for the action
     itself. **It did not examine the sibling repo**, so nothing here says what is failing there.
     Still open, and it belongs to whoever holds that repo.
2. **KEYCLOAK IS WIRED AND LOAD-BEARING** in all four production regions (5-step chain proven;
   positive control: pdf-api modules DO carry `count = 0`, so disabled is detectable). Not
   documentation debt — a live legacy dependency. `04_Keycloak_Retirement_Attestation` is
   **CONTRADICTED**, not merely unevidenced.
3. **A LICENSING DECISION CAN BE FORGED WITHOUT THE ROOT KEY.** The `valid:true` token is signed by a
   per-tenant key that travels inside every licence file, JWE-wrapped to a committed key, and binds
   nothing (no iss/aud/exp/tenant; cert has no extensions). **F-11's root rotation does NOT fix it.**
4. **TWO REMEDIATIONS MUST NOT BE RUN AS WRITTEN:** (a) rotating the root CA **wipes the licence
   table** — `TenantLicenseService.cs:50-54` deletes on validation failure, on the default page
   render; fix that first. (b) Deleting the committed `.key` files does NOT remove the root key —
   `LicenseGenerator.exe` is committed and CONTAINS it; no text scanner sees it.

## ✅ SECURITY REVIEW STEP 1 — ALL TEN FILES NOW READ BY THE COORDINATOR. Zero refuted.
**219 findings: 31 June (27 unremediated, ZERO fixed) + 188 new. 16 new Criticals.**

**Wednesday read the six outstanding files at 18:2x** (SecurePDF · pdf-api · myPKI · OneTimePad ·
OXPd1 · Reporting Dashboard). Exact tallies **from those six**:

    CONFIRMED 87 · REFUTED 0 · DOWNGRADED 8 · UPGRADED 3 · UNVERIFIABLE 1 · NOT VERIFIED 0

The predecessor reported **62 re-derived / 0 refuted** across the earlier four (HP-AuthSuite, Cryptix,
HPSA, infra-admin-portal), which is where the handover's **149 re-derived, 0 refuted** comes from.
**Across ten components, not one finding was refuted.** That is the strongest thing that can be said
about a register, and it is the opposite of the risk that a single overstated row gets the whole
thing discounted.

**The verifiers moved severity in BOTH directions, which is what makes the zero credible:**
- **UP:** `OTP-06` M→H (no binding between connector and challenge) · `OTP-10` M→H (the "specific
  topology" is the shipped one) · **`RD-10` M→H — and this one ships:** the Managed-AI
  `createUiDefinition.json` passes no Log Analytics parameters, so `hasPrinterData` is false on
  **every Marketplace deploy** and `ALLOWED_WORKSPACE_IDS` is never set, while `POST/PUT
  /api/data-sources` carry **no role guard** — a viewer can steer the app's own managed identity at
  any workspace it can read.
- **DOWN:** `OTP-31` H→L (the portal's gate is a server-issued bearer, not ASP.NET middleware;
  PR:N/C:H/I:H/S:C do not survive) · `OTP-28` H→M · `OTP-32` H→M (finder's item (d) simply wrong —
  the portal is `minReplicas: 1`) · `OXPD-02` H→L (**estate-wide escalation refuted**: the only
  caller has zero callers) · `OXPD-04` H→M · `OXPD-10` M→Info · `RD-12` L→Info · `MYPKI-01` C→H
  (the live path DOES have a KDF; the finder's own control grep was mis-run — 7 hits, not 0).

## 🔴 TWO NEW HIGH-VALUE FINDINGS RAISED BY THE VERIFIERS — neither is in the seed
1. **`V-OXPD-A` (High 7.3) — unauthenticated device-code minting, a phishing primitive.** Any host on
   the LAN can POST a SOAP `hidReportEvent` to `:8092` (no auth). The handler keys the event by the
   caller's socket address and starts an Entra **device-code flow using the organisation's own tenant,
   client id and client secret**. `GET /session-state` from the same host returns the `userCode` and
   the QR. **If any user completes that code — and the prompt shows the organisation's own app name —
   their access AND refresh token land in the ATTACKER's session**, and `/onedrive-api` then acts as
   them. Even with no victim, anyone on the LAN can mint device codes against the tenant at will.
2. **`V-01` (Reporting Dashboard, Low but it compounds tonight's RD-362 work) — the pen-test report
   quotes three FORMER signing secrets** (`JWT_SECRET`, `SESSION_SECRET`, `COORDINATOR_SECRET`
   fallbacks) in cleartext, **in a file that ships in the image**, and **`.gitleaksignore:71-73` are
   WORKING-TREE fingerprints suppressing exactly those three lines** while the file's own header at
   `:3` claims "the working tree scans clean". `:61-63` admits it. Deploy path is now `${VAR:?…}` so
   the fallbacks are gone from it — but any instance that ever ran on the defaults signed cookies with
   a now-public secret until rotated.

**🔴 THE CROSS-LINK THAT MATTERS, and only the coordinator could see it:** tonight's RD-362 gate found
the report is **1 of 5 carriers** for the SSH recovery pointer. This verification pass independently
found the **same report** also carries three signing secrets **with gitleaks fingerprints hiding them**.
And `RD-03` notes the report publishes **TWO** `git show` hashes where the finder listed one.
**So RD-362's scope is narrower than the artefact's exposure three separate ways.** RD-362 must be
re-scoped, and RD-55 (rotate + scrub) is the ticket the whole carrier story converges on.

**Also corroborated independently:** `RD-07` CONFIRMED — `mainTemplate.json:375-388` has no
`networkAcls`, no `enablePurgeProtection`, `softDeleteRetentionInDays: 7`. **That is precisely what
RD-363 fixes**, so tonight's tier-1 gate and this verification pass reached the same place from
opposite directions.

**STEP 2 (delta on the 19 June components): 8 done, 11 COMMISSIONED.** Wednesday recommended dropping
them; **Kam overruled — "yes, queue the eleven three at a time."** He was right and the register says
so. **BATCH 2 STILL TO LAUNCH (4):** CypherOneDrive + Teams (gate INTACT — the control group for
F-13) · CommonValueLibraryCypher · Cyphercard-Enrolment-App. **Do not let the in-flight state harden
into a claim of completeness.**

## DELIVERABLES — current, `.md` + branded `.docx`
`12_Rerun_Delta_2026-09` · `13_Consolidated_Findings_Register_2026-09` (carries §2.1, the
verification pass) · `11_Assurance_Pack_Index` (rows 1–19 flagged as understating the estate) ·
13 component summaries · `_Working/{findings-seed,verification,delta-review}-2026-09/` ·
`scan-artifacts-2026-09/` (argv recorded per tool) ·
`_Working/2026-09-07_{METHOD_IMPROVEMENTS,RERUN_DISCOVERY,VISION_PARKED}.md`

## OPEN FOR KAM — nothing is blocked on these
1. **RD-18** — the Australian Privacy Act package. The real Marketplace exposure; on hold, untouched.
2. Re-issue June deliverables 00/03/04/09/10 against 219, or let 12+13 stand as authoritative?
3. Live GitHub/Azure/Entra pass still open; tenant conflict `fc05dcdd` vs `0c57ab37` unresolved
   before any `az`.
4. **Vision PARKED** by his 10:44 ruling (`_Working/2026-09-07_VISION_PARKED.md`).

## KAM'S STANDING GRANTS TODAY — all week-scoped, read as through Sunday 2026-09-13
- **Merge** on Wednesday's word once the gate passes (09:40). **Deploy** for the rest of the week
  (11:09) and *"there are a number of items in tested but not deployed. Feel free to deploy"* (13:40).
- **Board judgement calls** (13:40): *"use the findings to action the tickets accordingly. I'm happy
  for you to take this and make judgment calls as I focus on the [Datasec] project."*
- **🔴 THE PRODUCTION LIFT IS SECUURA ONLY** — 12:07 *"Lift the production ban… flag these when
  relevant"*, narrowed at 12:10 to *"Only secure."* **Datasec has NO production grant. This seat is
  the Datasec seat. Do not read the lift as covering anything here.**
- Ticket CREATION aggregates: one larger ticket per logical path (13:23). A ticket already assigned
  to a human stays theirs. **Kill anything that queries Azure credits** (13:06) — five raises, closed.

## STANDING
No `cd`. Quote every grep glob. Every negative claim needs a positive control. `send_brief.sh` wants
literal `^PROVENANCE:` + `- <fact> | <source> | read YYYY-MM-DD` and `SELF-CHECK: re-read end-to-end
for contradictions | YYYY-MM-DD HH:MM`. Taps ≤200 chars, pointer only, mail FIRST, verify the BODY by
`preview` non-null, THEN tap. `<<'EOF'` for every brief body — or the Write tool. Never delete:
quarantine. Rotation band **80–90%**, 90 the ceiling; 70% is a checkpoint only.
**TWO WEDNESDAYS LIVE:** Studio owns **Secuura**, this seat owns **Datasec**. One repo, one dashboard,
one chat panel, **ONE USAGE LIMIT**. Do not write the shared files (`NEXT-PICKUP.md`, the daily note,
`_ledger.md`) — they are hers this session. Panel messages open `[LAPTOP / Datasec]`.
Secuura mail that lands in the shared inbox: **read the subject, not the body, and leave it.**
Confirmed working today — the Studio seat answered the #890 correction at 07:18:48Z without this seat
touching it.
