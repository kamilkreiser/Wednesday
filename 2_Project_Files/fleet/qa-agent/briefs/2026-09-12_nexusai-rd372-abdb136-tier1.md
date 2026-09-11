# QA GATE — TIER 1, round 1 — Datasec/NexusAI RD-372 @ abdb136

**Head:** `rd-372-provisioning-load-silent-s55` @ `abdb136f860048911fa79c54a7fbb78332b5ca0e` (on origin). **Base:** `main` @ `cd2b54397b0e83ccbd51e5b030c2ad614eb0e811`. **Range:** `cd2b543..abdb136`, **1 commit, 3 files** (`static/js/entra-provisioning-ui.js` +45/−4 region, `__tests__/rd372-provisioning-load-failure-is-visible.test.js` new, `scripts/verify-expected-counts.json`). **Why tier 1:** the defect's consequence is live **SCIM provisioning switched OFF for a tenant**: a failed load paints defaults as the tenant's state, and one Save POSTs `{"mode":"off"}` over the live config. Round 1 of 2 under the cap.

**Worktree under test:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/worktrees/rd-372-s55` (dependencies installed). **Clone it with `git clone --no-hardlinks` into your own `mktemp -d` and work only there.** Never write the worktree, and never write `NexusAI/2_Project_Files` (a stale snapshot under Kam's `investigate` hold).

## The builder's claims (NexusAI S55, READY FOR QA mail 2026-09-11T22:06:02Z) — claims, not evidence
- **FOUND (two defects, one outcome, both in `load()`):**
  - (a) the catch wrote a status message, then `render()` rebuilt `#rd135-status` empty, destroying it;
  - (b) `if (res.ok)` had no else, and `fetch` does not reject on HTTP errors, so a 401/500/502 silently painted DEFAULTS (`mode: 'off'`, no token) as the tenant's.
- **HOW:** the outcome is computed in `load()` and applied after the final `render()`. A new `loadFailed` state records whether the screen shows the tenant's config or defaults. **Save now REFUSES when the panel never read the state it would write over** (chosen over a confirm dialog).
- **TESTED:** jsdom runs the REAL module against a stubbed fetch. RED at base: A 502 → `""`; B → message destroyed; **C → the destructive `mode:off` POST was sent**. Three controls pass at base (healthy load renders; the status node lives inside the container `render()` empties; Save really POSTs on the healthy path). Suite 2284/118 (+6 / +1).
- **NOT TESTED, by its own account:** no real browser (jsdom cannot speak to how it LOOKS); no real Entra tenant or SCIM token.

## 🔴 WHAT TO ATTACK FIRST
1. **Reproduce RED and GREEN yourself** at `abdb136` and at `cd2b543`, and read why each control is green.
2. **A REAL-BROWSER render** (your default driver; fingerprint the browser to this machine before any localhost use) of the provisioning panel against a stubbed backend, with the load failing as **401, 403, 500, 502, a network error, a 200 with malformed JSON, and a 200 with a partial `{}` body**. For each: is the error VISIBLE and does it STAY; is anything on screen presented as the tenant's state? Screenshot evidence.
3. **The Save refusal, on every path that can write:** the Save button, keyboard submit (Enter), any mode toggle, and the token generate/rotate/revoke controls, after a failed load. **Any request that changes provisioning config after a failed load is a Blocker.** Count the requests that actually leave the page.
4. **Recovery, and the false refusal:** fail the load, then let a retry or reload succeed. Does `loadFailed` clear, and does Save work? **A Save that stays refused after a good reload is a Major** (it blocks a legitimate admin).
5. **The server side, READ ONLY:** does the backend endpoint accept `mode: off` from any caller without the UI's guard? The fix is client-only. Say what protects the tenant if another client, or a stale tab, POSTs. Report it as its own item with an evidence class, not as a regression of this range.
6. **Class census, READ ONLY:** other `static/js` components where `if (res.ok)` has no else before painting state. List them by file:line. Not findings against this range.
7. **Suite:** `npm run verify` at head, run IN THE FOREGROUND: 2284/118, and the counts-file change matches exactly.

## KNOWN — do NOT report as new
RD-293 (`599058b`) and RD-150 (`bec76f6`) are separate branches, and all three edit `scripts/verify-expected-counts.json` (a merge concern) · the Marketplace package findings · the stale main tree · 109 direct `console.*` calls · `gitleaks` absent on this machine (RD-342).

## Output
Findings-only. FOUND / TESTED / HOW with an evidence class (MEASURED AT RUNTIME · PROBED · READ ONLY). A control for every zero; never `rm`; head readings at start, mid and end. Remove only processes, containers and temp directories YOU create. **Run long commands in the FOREGROUND; never end a turn waiting on a background notice.** **Report:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-12-rd372-abdb136-tier1/report.md`. **MAIL YOUR VERDICT** to `tuesday-agent@agentmail.to`, subject `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — RD-372 @ abdb136 (tier 1)`, leading with GO, GO WITH FINDINGS or NO GO. **Never `wednesday-agent@`.** You have no inbox.
