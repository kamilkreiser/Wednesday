# QA Agent Invocation Brief — Datasec/NexusAI, S30's FIX ROUND on pass 20, STATIC THROUGH-CODE

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

**Then read your own pass 20, in full — it defines every F id below:**
`/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-04-s29-guard-round-through-code/SUMMARY.md`
(3 Major: F-1 one "corrected wording" control is double-excused and isolates nothing, and the DATED
excuse has no pass-side control at all · F-2 the paragraph-scoped excuse is up to 10 367 characters
wide in comment-shaped files, missing the exact wording the guard's own negative control proves it
catches · F-3 `docs/BRAND.md` says "The other **nine** clear it" where seven is right. 3 Minor: F-4
the guard silently drops any scanned file that moves and the positive control has slack of exactly
one file · F-5 `verify-suite.sh` floors 241/10 against an actual 1399/82 — **PRE-EXISTING** · F-6 the
handover's "Gates at the head" is one commit stale by construction.)

## 1. Target
- **Client / Project:** `Datasec / NexusAI`
- **Running target:** **NONE — STATIC pass, read by SHA.** Do not stand up a surface, do not deploy,
  do not drive a browser. **This round changed no rendered surface** (see §2) and the question is
  code and prose, not pixels.
- **SURFACES YOU MUST LEAVE ALONE — do not restand, restart or kill any of them:** `:3068` `:3072`
  (controls) and `:3073` `:3075` `:3076` `:3077`. **`:3077` serves `7e5faa9` and is the source of the
  frames Kam is reviewing this morning.** All seven were verified 200 at 06:05 today.
- **Environment:** none contacted. **Zero writes to the NexusAI tree.**
- **Production?:** nothing is deployed and no finding of yours triggers a deploy. **`caf1fe7`'s deploy
  GO is WITHDRAWN and is never re-issued** — Kam's eye is that gate.

## 2. Subject and the claims to falsify

**S30's round, head `3dda4ec`**, over S29's `11cdf5a` (read from `git log` in the NexusAI checkout at
06:07 on 2026-09-04). **Six files, 472 insertions:** `__tests__/muted-4-16-attribution.test.js`
(+212/−26), `__tests__/brand-md-accent-count.test.js` (NEW, 131 lines), `docs/BRAND.md` (1 line),
`docs/sustainability/S29_RESTAND_HANDOVER.md`, `JIRA.md`, `HISTORY.md`.

**Nothing under `static/`, `templates/`, `backend/` or `public/` is touched** — the builder states
zero rendered pixels **structurally**, which is what keeps Kam's frames from `7e5faa9` valid.
**Confirm that structurally yourself; it is the load-bearing claim of this pass.**

**All claims below are the builder's. Falsify them.**

1. **F-1 — the isolation test. The builder CORRECTED the brief rather than satisfying it.** Wednesday's
   brief said the test should *"assert every case flips to 1"*; the builder said plainly that is not
   achievable and not what isolation means — `e-fixed-mirror` is attribution-only, so disabling
   `DATED` correctly leaves it at 0. **Its formulation, which Wednesday accepted as stronger:** each
   case flips when **its own** family is deleted and **holds** when the other is, **plus a both-off run
   where all three go red** — which catches a case excused by the WRONG mechanism, the actual F-1
   defect. **Judge the formulation and the implementation separately.** Does the both-off run actually
   discriminate? Would a case excused by the wrong mechanism now fail?
2. **F-2 — the `datedScopeAt` rewrite.** `DATED_WINDOW = 500` is claimed **MEASURED**, from all 12 live
   co-occurrences (only 3 rely on `DATED`, at **305 / 312 / 242**), clearing the real need by ~190. The
   builder states **both bounds are load-bearing** so a later seat cannot "simplify" one away, and its
   rule of thumb: *"too-tight fails LOUD and too-wide fails SILENT, and silent is what we just
   removed."* **Re-derive the 12 co-occurrences and the three distances yourself.** Then ask the
   question the builder did not: **what does a 501-character gap do**, and is there a real one today?
3. **F-3 — one word in `docs/BRAND.md`.** "nine" → "seven". **It is live prose; confirm the whole
   sentence is now right, not just the numeral** — pass 20 found this error *inside the paragraph a
   previous round rewrote to fix a count error*, so the class is "a correction that introduces a
   correction". **Re-derive the denominator too.**
4. **F-4 / F-6 — accepted or carried?** The builder reports it **found a SECOND F-6 instance one
   section up**. Confirm both instances and confirm F-4's disposition.
5. **F-5 — carried to `RD-291` (To Do), with an honest gap the builder wrote down and Wednesday is
   passing to you verbatim:** *"I measured the arithmetic, I did NOT red-proof that the gate actually
   fails at the floor. Nobody has. That proof belongs with the fix."* **You are not asked to fix it.
   You ARE asked to say whether the arithmetic is right and whether anything else in the repo depends
   on that floor.**
6. **The second red-proof, adopted as a fleet rule and worth judging on its own:** *"a parser that can
   no longer find its subject must not report a pass"* — the builder broke the anchor wording so the
   check reports *"anchor not found … this check measured nothing"* instead of passing. **This is the
   first time in this fleet a round got AHEAD of an apparatus-displaces-subject defect rather than
   behind it. Verify it works: make the anchor unfindable and confirm the check refuses rather than
   greens.**
7. **The gate: 1403/1403 across 83 suites** (up from 1399/82). The builder states it confirmed the
   gate measured **that exact tree** by comparing the diff sha before and after the run rather than
   assuming no edit landed mid-run. **Measure at both ends yourself, as you did in pass 20.**
8. **NOT CLAIMED — the builder's own boundary, kept:** *"nothing this seat did is a rendered check;
   1403/83 green is evidence about code and prose, not about a page."* **Do not let the green stand in
   for a render claim, and say so in your report.**

- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files`

## 3. Scope — and the standing hypothesis

**Charter:** judge whether the three Majors are genuinely closed, and **hunt the class rather than the
instances.** On this project the class has been the same for four rounds running: **a guard or a
control that reads green because it cannot see, cannot reach, or cannot fail** — a census, a writer
and a verifier descending from one parse; a guard perfectly implemented on the wrong axis; a control
that isolated nothing. **Assume one more instance exists, and look for it in the fix round itself.**

**THE LOAD-BEARING QUESTION FOR THIS PASS.** F-1 was a control that isolated nothing. The fix is a new
set of controls. So:

> **Judge the CONTROLS at least as hard as the fixes.** For every new assertion, name the tamper it
> exists to catch, **predict the failing SET before running it**, and compare — a count of failures is
> weaker than a list of them. Run a **green baseline first** (the assertion against unmodified code)
> before any tamper; a red there is a defect in the assertion, not a discovery. A control that has
> never been made to fail is a claim; a control that isolates nothing measures nothing.

- **Out of scope:** any rendered surface, any deploy, any browser driving, any Jira transition or
  ticket, and any file in the NexusAI tree.

## 4. Credentials (POINTER ONLY — never values)
- **Path:** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/4_Credentials/` — **you should not need any.**
  This is a static read plus a local jest run. If you believe you need a credential, that is a
  QUESTION to Wednesday, not a step.

## 5. State-mutation & cleanup
- **Sanctioned pattern:** **exclude-and-report-only.** Nothing outside your own scratchpad changes.
- **NEVER `rm`, in your scratchpad or anywhere else — STANDING, all projects** (Kam's rule: cleanup
  means quarantine, not removal). **Build each attempt in its own `mktemp -d` and abandon the old
  one.** If a path genuinely must be cleared, **move it into a dated `_quarantine_YYYY-MM-DD/` beside
  it and say so in the report.** Guard every expansion — `"${DIR:?unset}/${SUB:?unset}/…"`. **If
  cleanup is costing real budget, stop building the fixture and report the affected checks as NOT RUN
  with the blocker named.**

## 6. Output boundary (fixed — not a choice)
- **Findings, reports and recommendations ONLY.** No code, no tests, no fixtures, no tickets, no
  config. Describe the fix-shape and the regression test the owner should add, in prose. The NexusAI
  agent authors and commits everything. (Kam ruling 2026-08-11, absolute.)

## 7. Known-fragile / known-changed areas
- **Known-fragile:** the 4.16 attribution guard and every control around it · `verify-suite.sh`'s
  floors · `docs/BRAND.md`'s counts (three separate count errors across three rounds) · handover docs
  that quote "gates at the head" · any check whose subject is prose the author also wrote.
- **Recent changes — do NOT flag as new:** the six files in §2; `RD-290` (Testing) and `RD-291`
  (To Do) filed 2026-09-04 04:31; the `JIRA.md` correction (a `jira issue create` hang whose real
  cause is a summary over Jira's 255-character limit).
- **Known open gaps carried, not re-discovered:** F-5's un-red-proofed floor (RD-291) · RD-285 /
  RD-286 / RD-288 / RD-289 / RD-197, all filed with a NEXT and none in this round's scope.

## 8. Logistics
- **Time-box:** one bounded session; wrap at your own context boundary with a SUMMARY.
- **Findings sink:** your own report tree,
  `projects/nexusai/reports/2026-09-04-s30-fixround-through-code/`. **File no tickets.** Priority on
  any finding is the humans' call, never yours.
- **Escalation:** back through Wednesday (`wednesday-agent@agentmail.to`, subject
  `[Testing Agent MAIN -> Wednesday] QUESTION: <topic>`). Approval-class items ALWAYS pause for Kam.

---

PROVENANCE:
- S30 head `3dda4ec` over `11cdf5a`; the six files and their line counts | `git log --oneline -8 3dda4ec` and `git diff --stat 11cdf5a..3dda4ec` in the NexusAI checkout | read 2026-09-04 06:07
- Nothing under static/templates/backend/public touched | the same `git diff --stat` | read 2026-09-04 06:07
- F-1..F-6 definitions, the pass-20 attack table, the 1399/82 baseline | your own SUMMARY.md at the report path named above | read 2026-09-04 06:08
- The seven surfaces all answering 200, including `:3077` | `curl -o /dev/null -w %{http_code}` from Wednesday's seat | read 2026-09-04 06:05
- RD-290 Testing / RD-291 To Do, updated 2026-09-04T04:31 | Jira REST `search/jql`, project RD, paged exhaustively | read 2026-09-04 06:07
- The builder's claims in §2 (the 12 co-occurrences, 305/312/242, DATED_WINDOW 500, the both-off run, the anchor red-proof, 1403/83, the diff-sha check, the second F-6) | the NexusAI agent's own QUEUE COMPLETE and wrap mails to wednesday-agent@, 2026-09-03 18:32:07Z and 18:35:00Z | read 2026-09-04 06:05 — **these are its claims, not Wednesday's measurements**
