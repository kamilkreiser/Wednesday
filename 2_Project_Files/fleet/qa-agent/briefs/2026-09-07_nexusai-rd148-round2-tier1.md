# QA GATE — Datasec/NexusAI RD-148 **ROUND 2**, `rd-148-round2-s45` @ `ea4d229`. **TIER 1.**

## Why this round exists, and what a NO GO costs
Round 1 was NO GO on a **Blocker**: the revoke outcome message was destroyed ~12 ms after it was
written, **on every path including token-still-live**, because `revokeScimToken` calls `setStatus()`
then `finally { render() }` — and `render()` wipes the container holding the only `#rd135-status`.
Every sibling handler calls `render()` BEFORE `setStatus()`; revoke was the only inversion.

**This is round 2 of 2. The cap is spent.** A NO GO does not open a round 3: the closed instances
ship and the residue is ticketed, or it goes to Kam. So say clearly which findings, if any, would
survive that.

## 1. Target
    ea4d229   rd-148-round2-s45   THE SUBJECT. Parent aea410c, pushed.
    aea410c   rd-148-...-s43      round 1's tip = the base. The Blocker is LIVE here.
    Base every diff on `aea410c..ea4d229`. NOT main — main is ~251 behind and diffing
    against it reads other people's merged work as this change.

3 files, +241/−21: `static/js/entra-provisioning-ui.js`,
`__tests__/entra-provisioning-revoke-ui.test.js`, `scripts/verify-expected-counts.json`.
Builder's claim: **PASS 2174/2174 across 113 suites**; closes **F-1 (Blocker), F-2, F-3**.
F-4/F-5/F-6 were scoped out by Wednesday and filed as **RD-371** (`Relates` → RD-148) with the board
search recorded in the ticket — **not silently dropped**.

## 2. 🔴 THE CENTRAL QUESTION — does the message survive, on a real DOM, on BOTH paths?
This was a real-DOM **timing** defect, so **jsdom is not the artefact.** Reproduce in a real browser
on both heads. The builder's own measurement, to beat rather than to trust:

    SUCCESS  t=2011 "Revoking token…" -> t=2036 full server note, HELD to t=5002
    FAILURE  t=1662 "Revoking token…" -> t=1680 "TREAT THE TOKEN AS STILL LIVE…", held to t=5001
    ROUND 1  same scenario: t=3036 -> ""  and "STILL LIVE present anywhere" = false

**The failure path is the one that matters**: the server returned 500 with
`scimTokenConfigured: true`, so the token really was still live while the admin was being told so.
**To force it:** `chmod 444` on `<DATA_DIR>/settings.json` → `REVOKE_VERIFY_FAILED`. **Assert the
tamper LANDED (PermissionError 13) before reading any result**, and revert it afterwards.

**Measure the RENDERED artefact, not the DOM text.** The builder measured box geometry and colour
(success 827×42, `rgb(25,135,84)`; failure 712×84, `rgb(220,53,69)`, plus a 904×125 alert, both
in-viewport). A node whose text is right and whose box is 0×0 is the same defect wearing a different
costume.

## 3. 🔴 THE FIXTURE — the builder names this as its own weakest point and it is right
Round 1's suite was **10/10 green over a product that was broken**, because its fixture supplied
`#rd135-status` and `#rd135-result` as **SIBLINGS of the container**. `render()` wipes only the
container, so those nodes survived the re-render that destroys the real one — **every cell asserted
against a live region the product does not have.**

The builder proved the fix by contrast rather than assertion:

    A  round-1 code + round-1 fixture .... 10/10 GREEN   <- what shipped
    B  round-1 code + the NEW fixture .... 10 FAILED     <- same product code
    C  round-2 code + the new fixture .... 20/20 GREEN

**Re-run B yourself. It is the whole argument** — only the fixture changed. Then ask the question the
builder asked of itself: *a fixture I chose is still a fixture I chose.* **Confirm against the real
page** that there is exactly ONE `#rd135-status` and that it is INSIDE the container. If the real
page ever gains its own, these cells go blind in the opposite direction — say whether anything
prevents that.

**And look for siblings of the defect:** any other cell in that file still hand-building DOM the
product actually renders.

## 4. THE BUILDER'S OTHER TWO WORRIES — carried verbatim, they are well chosen
1. **Is there a path where `outcome` stays null** and the admin gets a silent panel again? The fix
   computes the outcome and applies it in `finally`; find the branch where it is never computed.
2. **`F-3`'s `confirm()` in non-browser contexts.** It matched the house idiom exactly rather than
   inventing a guarded variant — *"a deliberate consistency choice and arguably the wrong one."*
   Rule on it: this is the most destructive control in a UI carrying **17 `confirm()` guards for
   milder things**, so consistency is a real argument — but say whether the house idiom is adequate
   *here*, not merely usual.

## 5. WEDNESDAY'S ADDITIONS
- **Regression on the siblings.** The fix aligns revoke to the file's own pattern. Confirm no OTHER
  handler's ordering changed, and that none of them relied on the old behaviour.
- **Re-verify the DECLINE path independently.** The builder claims ZERO requests when the confirm is
  declined, measured by URL — **and it self-caught a first attempt that counted its own probe and
  read as 1.** Measure it your own way; a probe that pollutes its own count is exactly this file's
  family of defect.
- **The counts.** 2174/2174 with 20 cells where round 1 had 10. Check the reconciliation rather than
  accepting the total.

## 6. EVIDENCE — and one thing about the builder's screenshots you must know
**Its screenshots are GITIGNORED** (`tests/screenshots/.gitignore` is `*`), so they are local
artefacts on its machine and **do not travel with the branch. Take your own.**

**It quarantined two of its own screenshots rather than filing them**, at
`tests/screenshots/quarantine-2026-09-07-s45-identical-viewport-shots/` with a `WHY.md`: they were
**byte-identical** (same md5, same 104636 B), viewport shots of a panel that sits below the fold
inside a `display:none` section — so neither contained the message it was named for and one was
actively mislabelled. **It caught this by hashing them instead of trusting them.** Read the `WHY.md`;
then, if you take screenshots, **hash yours** and confirm the panel is actually visible before you
cite one. The panel is inside a hidden section until you click the `a[data-section="provisioning"]`
nav link on `settings.html`.

**The drivable surface:** a LOCAL run at this commit, fresh `DATA_DIR`, open mode — **NOT the demo**
(RD-76: the demo's `/login` carries zero `<form>` and zero `<input>`). Say *"same commit, not the
demo image."* The builder's recipe, verbatim:

    DATA_DIR=<fresh> PORT=3099 SESSION_SECRET=<throwaway> ENCRYPTION_KEY=<throwaway> \
      HEALTH_SWEEP_URLS=" " node backend/server.js
    POST /api/setup/entra-provisioning/scim-token          (cookie jar + X-CSRF-Token)
    POST /api/setup/entra-provisioning {mode:"scim", scimBearerToken:...}

**`HEALTH_SWEEP_URLS=" "` is mandatory** — `healthSweeperScheduler.js:31` hardcodes the demo URL as
its default sweep target. **No `az`, no registry, no contact with `nexusai-staging` or the demo.**
The builder's checkout is READ-ONLY; work in your own clone or worktrees and restore them clean.
**Stop any server you start and prove the port is 000 afterwards.**

**Mandatory:** a positive control on the instrument and a negative control that flips with the
subject · every tamper asserted LANDED before its effect is read · read every hit before counting it
· **NAME THE FRAME** in any completeness claim · **FOUND / TESTED / HOW with the controls named under
HOW** (Kam's standing instruction, 2026-09-07 18:56:36) · state what you did NOT test.

## 7. Verdict
**GO · GO-with-findings · NO GO**, with severities. A guard that is real but narrow is
**GO-with-findings**. **The cap is spent, so a NO GO must say what ships anyway and what gets
ticketed** — that decision then comes to Wednesday, and to Kam if it changes scope.

Report to **Wednesday**, not to the builder. Write the report and evidence under
`projects/nexusai/reports/2026-09-07-rd148-round2-tier1/` and name the path in your mail.

PROVENANCE:
- Head ea4d229 and its parent | `git -C <NexusAI>/2_Project_Files ls-remote origin refs/heads/rd-148-round2-s45` run by Wednesday - Wednesday's read, not yours | read 2026-09-07
- The A/B/C contrast, the timings, the box geometry, the quarantined screenshots, the three worries | the builder's READY mail 2026-09-07T12:08:06Z, DKIM-verified - relayed, not re-measured by Wednesday | read 2026-09-07
- F-1's cause, F-2, F-3 and the 17 confirm() guards | the RD-148 round-1 tier-1 gate verdict, recorded in /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/tasks/NEXT-PICKUP-DATASEC-LAPTOP.md - Wednesday's tree, not yours | read 2026-09-07
- RD-76 demo login unusable; main ~251 behind | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round3-tier1/report.md sections 1 and 8 | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 22:12
