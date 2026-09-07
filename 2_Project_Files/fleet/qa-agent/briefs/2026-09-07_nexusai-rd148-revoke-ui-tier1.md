# QA GATE — Datasec/NexusAI RD-148 (P2-06), `rd-148-scim-revoke-ui-s43` @ `aea410c`. **TIER 1, round 1 of 2.**

**Charter first, in full:** `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/CLAUDE.md`
(T9 seat — DevMASTER is not mounted. Every path here is a T9 path.)

## 🔴 TIER: 1, and it was queued as the tail-end item — here is why Wednesday moved it
The change **adds a REVOKE control to the admin UI**. It is not a display tweak: it is a **destructive
action on a security surface**, put in front of a human, with 103 lines of new product JavaScript
behind it. Three ways a mistake here costs more than the diff suggests:
1. **It revokes the wrong subject** — the button's row and the request's target are two different
   things, and a UI list that re-sorts or re-renders between render and click is the classic way they
   diverge.
2. **It does not actually revoke** — the control reports success from an HTTP 200 rather than from the
   revocation, which is this estate's most-repeated defect class today.
3. **It is reachable by a role that should not have it** — a UI affordance is not an authorisation
   boundary, and the server route behind it is what decides.

**Round 1 of 2 under Kam's cap.** No product-behaviour claim is being taken on trust here.

## 1. Target
- **Branch:** `rd-148-scim-revoke-ui-s43` · **Head:** `aea410cc0432638b6a8698ae659197599915c2c2`
- **Parent (the baseline):** `9546da5f5585eb6e215d935c4cae2a55c339104b`
- **`origin/main`:** `a9a8cb6e3fc62b8c08e1f3aadecb08519f1f6ddc` — 🔴 **branch is 248 commits ahead.
  DIFF AGAINST THE PARENT, NEVER AGAINST `main`** (RD-367: main is the integration branch but is ~247
  commits behind; diffing against it reads other people's merged work as the change under test).
- **Change:** 3 files, +296/−6 — `static/js/entra-provisioning-ui.js` (**+103, the product change**),
  `__tests__/entra-provisioning-revoke-ui.test.js` (new, 193 lines), `scripts/verify-expected-counts.json`.
- **Repo:** `/Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files` — **read-only to
  you.** Work in your own worktree or clone.
- **NON-PROD. NO DEPLOY. NO `az`, no tenant, no registry, at any point.** Kam's 2026-09-07 production
  lift is **Secuura only**. Datasec production is out of scope entirely.
- 🔴 **Do not contact `nexusai-staging` or any live box.** It serves a stale build and its exposure is
  already recorded elsewhere; it is not this gate's business.

## 2. 🔴 THE CENTRAL QUESTION — does the revoke revoke the thing the admin is looking at?
**Trace the whole path, and do it at the source rather than from the test:**
1. **From the clicked element to the request payload.** Which identifier is sent — the one bound at
   render, or one re-read from the DOM at click time? **Construct the divergence:** re-sort, filter,
   paginate or re-render the list between render and click and show which subject the request names.
   If the id is captured at render into a closure, say so and say what re-render does to it.
2. **From the request to the effect.** Does the UI report success from the **HTTP status**, or from
   something that proves the revocation? **What does it show if the server returns 200 with a body
   saying nothing was revoked?** Construct that case.
3. **Confirm-before-destroy.** Is there one, is it defeatable by a double-submit or an Enter key, and
   does a second click while the first is in flight send a second revoke?
4. **The authorisation boundary is the SERVER route, not the button.** Find the route the control
   calls and read its guard. **A hidden or disabled button is not a control.** If the route has no
   role check, that is a Major regardless of what the UI does — and note the sibling finding on this
   repo today: `POST/PUT /api/data-sources` carry no role guard at all, so do not assume this family
   of routes is guarded.

## 3. The issue-date half — smaller, still checkable
The change also surfaces an issue date to the admin. **Is the date the one the record holds, or one
the browser computed?** Check the timezone handling and what renders when the field is absent or
malformed — an "Invalid Date" or a silent blank in a security console is a real defect, and a date
composed client-side from `Date.now()` is a fabricated fact
([[the estate's own rule: generate timestamps, never type them]]).

## 4. The browser half — and an honest constraint you must state
The charter says anything browser-related is driven in a real browser. **Wednesday cannot promise you
a drivable surface here:** the builder has wrapped, `localhost:3001` is **down** (verified: no
listener), and the deployed hosts are out of scope.
**So: if you can stand the app up locally from THIS commit cheaply, do — and say it is a local run of
the same commit, never that the deployed app was tested.** If you cannot, **say so plainly and do the
code + DOM-level pass**, then **name exactly what that cannot prove** (rendered state, event ordering,
focus and double-submit behaviour, what a real click does). *"Unit-proven; the click path could not be
exercised"* beats a green tick implying coverage it does not have. **Do not skip the question — answer
it with its boundary.**

## 5. Evidence rules — mandatory
1. **Every cell: say what it MOCKS and therefore what it cannot prove.** A JSDOM test proves handler
   wiring, never that a user can reach the control.
2. **Both controls on every negative claim** — a positive control proving your instrument fires, and a
   **negative control (an impossible pattern)** so a zero is one your reader can vouch for.
3. **Assert each tamper LANDED before asserting its effect.** **A uniform non-zero across variants is
   as suspect as a uniform zero** — a sibling gate's matrix returned rc=1 on all five variants and
   looked like a clean red-proof; it was a config error and the runs never executed. **Establish the
   command RAN before reading its exit code.**
4. **Counts file:** confirm the delta matches the cells added *and that they ran*; report skipped and
   disabled counts explicitly.
5. **Never delete.** Cleanup means quarantine. **Findings-only — you never fix.**

## 6. Verdict
**GO** · **GO-with-findings** (mark Majors vs advisory) · **NO GO**. Severity yours, priority
Wednesday's. Round 1 of 2 — if NO GO, name which parts could ship and what the residue's ticket says.

Report by mail to `wednesday-agent@agentmail.to`, subject
`[QA -> Wednesday] Datasec RD-148 revoke UI (@ aea410c, tier 1)`.

PROVENANCE:
- head `aea410cc0432638b6a8698ae659197599915c2c2`, parent `9546da5f…`, 3 files +296/−6 with +103 in `static/js/entra-provisioning-ui.js` | `git ls-remote` + `git show --stat`, run by Wednesday in the same action as writing this | read 2026-09-07
- 248 commits ahead of `origin/main` `a9a8cb6e…` | `git rev-list --count` | read 2026-09-07
- `localhost:3001` has no listener | `lsof -nP -iTCP:3001 -sTCP:LISTEN`, run by Wednesday | read 2026-09-07
- `POST/PUT /api/data-sources` carry no role guard | the Reporting Dashboard verification file `_Working/verification-2026-09/reporting-dashboard-au-main.md`, RD-10 (UPGRADED Medium→High), read by Wednesday | read 2026-09-07. **A sibling component, cited as a reason not to ASSUME this family is guarded — not as a claim about this route.**
- the crashed-tamper-matrix rule | the RD-362 gate's verdict mail, 2026-09-07T08:14:21Z | read 2026-09-07
- tier cap of two NO GO rounds | Kam, 2026-09-05 20:19 | read 2026-09-07
- production lift is Secuura-only | Kam, panel 2026-09-07 12:07 + 12:10 | read 2026-09-07
- **UNMEASURED, stated as such:** which identifier the control sends, whether the server route is guarded, and whether a drivable browser surface can be stood up. Those are this gate's questions, and Wednesday has read none of the 103 changed lines.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 18:45
