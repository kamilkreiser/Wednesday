# QA Agent Invocation Brief — Secuura / Blockchain (Platform K), S130 FOLLOW-UPS through-code pass: PR #822 @ `56f42f5ab` — six items from the two-head re-gate, one of them (F-6) NOT fixed the way the report prescribed, and one one-import-line change the code's own header asked not to slip into a follow-up

**TIER 2 — through-code ONLY (no stood-up surface, no browser): tests, comments, citations, one adapter guard, one import-line change whose blast radius the builder measured.** **ROUND 1** of this class under the cap (Kam 2026-09-05 20:19).

**R0 (client isolation):** exactly one client's content — Secuura / Blockchain (Platform K). Report under `projects/secuura/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 0. Context
The two-head re-gate on #815 + #820 (`projects/secuura/reports/2026-09-05-s130-ks795-815-and-820-regate-06e79adab-48694b1c9/report.md`, §A3 S130-F1…F5 and §B S130-F6) found six residual items; #815/#820 are MERGED (develop `cd5262dc3`). This PR closes the six. READ THAT REPORT'S S130-F1…F6 SECTIONS FIRST; they are your instruments. **Two Secuura QA seats run concurrently** (KS-800 on #817; KS-722 on #821) — own copy, own ports if any; never their trees.

## 1. Target
- **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` (the builder s131 LIVE; stack `:6882` off-limits). Own `mktemp -d`; your subject from the git objects.
- **Subject:** **PR #822 head `56f42f5ab`** (`refs/pull/822/head` at origin = `56f42f5ab5c742dbf23155607213573dc871a839`; develop `cd5262dc3`; `git ls-remote origin` from Wednesday's seat, no fetch, 21:0x AEST). Ahead/behind and the per-file stat are in the PROVENANCE block below — re-derive them. Review state "unread".

## 2. The builder's claims at `56f42f5ab` (s131's READY 2026-09-05T11:00:49Z, 5,126 chars, read whole)
1. **F-6 — the report's fix-shape ("one test that merely imports `auth.openapi.ts`") DOES NOT WORK:** the import fails under vitest (`MFA_CODE_ACCEPTED.optional(...).openapi is not a function` — `passwordLoginGate.ts` imports `z` from `'zod'`, so `extendZodWithOpenApi` never landed on it; the CJS generator unifies the two resolutions and hid it). That is WHY #820's canary never fired. **The builder then took the one-import-line fix the module's own header asks NOT to slip into a follow-up — and measured its blast radius: `z.` used twice in `passwordLoginGate.ts`; the generated yaml BYTE-IDENTICAL before/after (`md5 8edab8e1…`); `check:openapi` PASS (307/405).** The builder names this as the judgement it most wants checked; "revert and file the canary as still-open" costs one commit.
2. **F-1 — run against the UNFIXED product first:** `!profile.email` is TRUE for whitespace-only addresses while `getUserByEmail`/`getUserByEmailLookup`/`createUser` normalise `.toLowerCase().trim()`; parameterised case over `''`, `' '`, `'\t\t'`, `'  \n '` → predicted 3 of 4 red pre-fix, measured 3 failed / 32 passed; 4 of 4 after. **Behavioural change beyond the findings, called out: the create path now stores the TRIMMED email.**
3. **F-3** — the comment on the guard rewritten (the CREATE branch is a bare `if (!user)`; the F-4 guard is the ONLY thing between an empty key and a row). **F-2** — `google.ts` `?? ''`; the other five adapters checked (four guard; github initialises safely). **F-4** — the doc block moved onto `SocialEmailUnavailableError`. **F-5** — citations re-anchored to SYMBOLS (`const fieldMap`, `socialIdField`) after a third drift.
4. Counts: `services/auth` 37 files / 493 / 0 (488 on develop; +3 F-1 rows, +2 the canary file); build rc 0; `tsc` clean; eslint 0/0; yaml byte-identical; `check:openapi` PASS.
5. **NOT tested by the builder:** no red-proof for F-2/F-4/F-5 (unreachable / documentation); **F-6's canary NOT test-fired** (imports and holds `/api/auth/*` routes; no module-scope throw inserted); the merge-order note: #822 and #821 both touch `errorHandler.ts` in different regions — #821 merges first, #822 rebases after.

## 3. Scope — through-code
- **F-6, the builder's own nomination:** (a) reproduce the failure of the prescribed shape on the PARENT `cd5262dc3` (the import throws under vitest — show the message); (b) at the head, the import succeeds; (c) **FIRE the canary** — a module-scope throw in `auth.openapi.ts` in your copy → predicted set/count → the new canary file reds (the thing #820's guard could not do); restore by hash; (d) the one-import-line change: read `passwordLoginGate.ts`'s two `z.` uses and the header's blast-radius warning; reproduce the yaml byte-identity (`generate-openapi` before/after → md5) and `check:openapi`; state whether the header's warning was right or over-cautious, with the measurement — this is the verdict the builder asked for.
- **F-1:** reproduce the parameterised case at the parent (3 of 4 red) and the head (4 of 4 green) from the git blobs; then the trimmed-email storage change — what else reads the stored email (lookup hash agreement; any display; any comparison) — one tamper: store untrimmed → which cases red?
- **F-3/F-4/F-5:** read the comments against the code (Explainability oracle) — is each now TRUE; the citations resolve to the named symbols at the head; the doc block sits on the class it describes.
- **F-2:** read the six adapters; confirm the claim about the other five from source.
- **The introduced-defect hunt** on the 7 files (+157/−34): anything beyond the six items; the `errorHandler.ts` region vs #821's (read #821's diff at `ca4db0b1c` for the collision the builder predicts — textual overlap yes/no).
- Suites in your copy beside 37/493/0; build rc; palette n/a.

**Out of scope:** #817, #821 (their own testers), provider enablement, the demo, the builder's tree, anything stood up.

## 4–7. Boundary and carried — as the KS-800/KS-722 briefs
Own `mktemp -d`; never `rm`; `${VAR:?}`; quarantine by rename; tampers restored by hash; predict SET and COUNT before every run; findings/report/recommendations ONLY; no board or GitHub reads. Carried: a fix-shape in a report is a hypothesis (the builder just proved one wrong — reproduce the proof); a header's warning is a claim with a date (measure the blast radius yourself); "armed but not fired" is the builder's own honest gap — fire it.

## 8. Logistics
- **Time-box:** narrow, through-code — the F-6 quartet, the F-1 pair, the reads, the suite.
- **Findings sink:** `projects/secuura/reports/2026-09-05-s131-followups-822-56f42f5ab/report.md` + `evidence/`.
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] S130 follow-ups PASS 1 @ 56f42f5ab (PR #822)` — BLUF (PASS or NO GO first line; the F-6 verdict named), report path, closure table, red-proofs, new findings, NOT-TESTED, the head at the end.

---

PROVENANCE:
- `refs/pull/822/head` = `56f42f5ab`, develop `cd5262dc3`; a local commit object; the ahead/behind count and per-file stat as read | `git ls-remote origin`, `git cat-file -t`, `git rev-list --left-right --count`, `git diff --stat`/`--name-status --diff-filter=A` — local objects, Wednesday's seat, no fetch | read 2026-09-05 21:0x
- Claims 1–5 | s131's READY 2026-09-05T11:00:49Z (5,126 chars, read whole) | read 2026-09-05 21:02
- S130-F1…F6 and their evidence | the two-head re-gate report §A3/§B, read by Wednesday at 19:4x | read 2026-09-05 19:4x
- The concurrent testers on #817 and #821 | Wednesday's pane list at 2026-09-05 21:02 | read 2026-09-05 21:02
- Kam's 20:19 ruling (tiers + cap) | `tools/kam_rulings_today.sh`; `learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md` | read 2026-09-05 20:2x
- Review state of #822 | NOT read — "unread" | —
- scope: TIER 2 through-code, round 1 = the six closures (F-6 by firing the canary and measuring the import-line change) + the F-1 trimmed-email consequence + the hunt on `cd5262dc3..56f42f5ab`; nothing stood up; nothing on #817/#821 | this brief's §3 | read 2026-09-05 21:02
