---
date: 2026-09-07
type: pickup
scope: DATASEC ONLY — laptop seat. Secuura belongs to the Studio seat; do not touch it.
source: replaced wholesale at the 17:0x pickup (previous version claimed a gate was running that was not)
status: live
supersede: replace wholesale at the next pickup; do not append
---

# NEXT PICKUP — Datasec laptop seat, 17:4x AEST Monday 2026-09-07

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
gate output existed.** Both gates are genuinely running now (below), each verified by its pane
naming its own brief — **rung 5, never a non-zero ctx.**

**The general rule this earns, and it is already a lesson:** a handover records a mechanism by its
**PATH**. Every launch wrapper below is named by path for exactly that reason.

## FLEET — 3 live, AT THE CAP (max 3 concurrent; the SESSION rate is what broke at 11:17, not the weekly budget)
- **`Datasec/NexusAI` `%2`** — the builder. Working **RD-329** (unauthenticated `/api/health` on
  `nexusai-staging` serving workspace IDs and component status). No gate needed. **Do not close it.**
- **`%3` — QA gate, RD-361 round 2, TIER 1, round 2 of 2 under Kam's cap.**
  Branch `rd-361-fail-closed-unknown-s43` @ `1149d1c332b6ebaac68393ba0afdeb8c65ebdd29`.
  Launch: `2_Project_Files/fleet/state/launch_qa_nexusai_rd361_r2.sh` (`--check` for guards).
  Brief: `2_Project_Files/fleet/qa-agent/briefs/2026-09-07_nexusai-rd361-r2-tier1.md`.
- **`%4` — QA gate, RD-363 / SEC-07, TIER 1 (UPGRADED from 2), round 1 of 2.**
  Branch `rd-363-keyvault-purge-protection-s43` @ `b0dec96fc1f498b309cee692b6441ed9e9b0b043`.
  Launch: `2_Project_Files/fleet/state/launch_qa_nexusai_rd363_sec07.sh`.
  Brief: `2_Project_Files/fleet/qa-agent/briefs/2026-09-07_nexusai-rd363-sec07-tier1.md`.

**GATE QUEUE AFTER THESE TWO, in order:**
1. **RD-362 @ `920e067`** (`rd-362-pentest-report-exposure-s43`) — **MOVED UP ahead of RD-148 by this
   seat.** It closes a live exposure: the pen-test report carrying the SSH-key recovery commit and
   blob path shipped inside the customer image twice over. **Exposure outranks queue age.** The
   builder was told and invited to disagree.
2. **RD-148 @ `aea410c`** (`rd-148-scim-revoke-ui-s43`, 2164/2164).

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

## 🔴 AN OPEN QUESTION PUT TO THE BUILDER, AND IT MAY MATTER MORE THAN ANY GATE
Measured read-only in the builder's checkout:

    origin/main                            a9a8cb6e3fc62b8c08e1f3aadecb08519f1f6ddc
    rd-361-fail-closed-unknown-s43         249 commits AHEAD of main
    rd-363-keyvault-purge-protection-s43   248 commits AHEAD of main
    RD-363's OWN change (vs its parent)    3 files, +118 / -5
    RD-363 diffed against main             254 files, +59,000 / -1,034

**What is NexusAI's actual integration branch?** If it is `main`, `main` is 248 commits behind the
work and the word "base" in every gate brief is close to meaningless. **Neither running gate depends
on the answer** — both are scoped to the right baseline (`e4d9147` → `1149d1c` for RD-361; the parent
`9546da5` for RD-363), and both were told explicitly **not** to diff against `main`.
NexusAI's mainline is **`main`, NOT `develop`** — do not carry the Secuura convention across.

## CLOSED SINCE THE LAST PICKUP
- **The cat-1 count is settled: 96, not 97.** Category-2 is 18 → 19. **Only RD-50 moves** — its own
  scope note puts execution in the Feedback System and Lead Bot folders, a hard-rule-1 boundary, not
  a capacity question. RD-69 and RD-364 were checked and are genuinely category 1; RD-362 is MIXED
  (its in-repo half shipped, its rotation half was always category 2). **This is the number Kam is
  held to and it has been mirrored to his panel.**
- **RD-362's in-repo half SHIPPED @ `920e067`** — SEC-04 closed, SEC-03 partly. SEC-02 and both
  rotation halves stay open (rotation needs the dev-tenant admin: category 2).

## 🔴 STILL STANDING — four conclusions given to Kam that CHANGED, carried forward verbatim
1. **THE CI SECRET GATE MAY BE DECORATIVE.** All 25 `gitleaks.yml` workflows pin
   `actions/checkout@v7` — a major that does not exist. Verified spread: v4×35, **v7×25**, v2×8,
   v3×3, v5×1, no v6; all 25 v7 files are gitleaks workflows. A workflow whose checkout cannot
   resolve **fails before the scanner runs.** Corroborated: `terraform.tfstate.backup` still carries
   F-16 credentials in a repo whose gitleaks nominally runs on every push. **SUSPECTED, high
   confidence — one look at Actions run history settles it.** This RETRACTS the one improvement
   credited all day. (The RD-363 brief asks its gate to establish cheaply whether NexusAI's own
   counts gate actually executes — same class, different repo.)
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

## SECURITY REVIEW — step 1 complete, step 2 in flight
**219 findings: 31 June (27 unremediated, ZERO fixed) + 188 new. 16 new Criticals.**
**STEP 1 (verify): all 10 files written; Wednesday has READ 4** — HP-AuthSuite (12 conf/1 upgraded),
Cryptix (28 conf/1 down, all 4 Criticals stand), HPSA (16 conf/2 down), infra-admin-portal
(6 conf/1 down/1 upgraded/1 unverif/+6 new). **62 re-derived, ZERO refuted.**
**UNREAD — the cheapest high-value task available, do it when a gate slot frees:** OneTimePad ·
myPKI · SecurePDF · pdf-api · OXPd1 · Reporting Dashboard, all in `_Working/verification-2026-09/`.
**INFRA-03 (High 7.5 → ~9.3):** the admin portal's committed encryption key is **AES-ECB** (no IV, no
auth, deterministic, raw-UTF-8 key, no KDF) over **customer tenants' Entra app-registration
credentials**. Unauthenticated webhooks are worse than the seed said: `onboarding-cleanup`
irreversibly null-writes credentials on every row older than 7 days; `saas-refresh` lets an anonymous
caller trigger outbound customer email. No compensating control at any layer (proven three ways).
dev ≡ staging on all three Entra secrets; production separate on all nine.
**STEP 2 (delta on the 19 June components): 8 done, 11 COMMISSIONED.** Wednesday recommended dropping
them; **Kam overruled — "yes, queue the eleven three at a time."** He was right. **BATCH 2 STILL TO
LAUNCH (4):** CypherOneDrive + Teams (gate INTACT — the control group for F-13) ·
CommonValueLibraryCypher · Cyphercard-Enrolment-App. **Do not let the in-flight state harden into a
claim of completeness** — register §7.1 says "commissioned, in flight".

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
