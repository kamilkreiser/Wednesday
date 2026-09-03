# QA Agent Invocation Brief — Datasec / NexusAI — S28 round 19, the Sustainability tab REBUILT TO THE MOCK, pass 16 (2026-09-03, ~22:1x AEST)

**R0 (client isolation):** this brief carries exactly one client's content (Datasec / NexusAI). Never name or reference any other client. Read only the paths named here. Your report goes under your own project tree.

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md`. **BROWSER pass with a through-code half. Findings only — no fixes, no tickets, no commits, no deploy.**

## WHY THIS PASS IS DIFFERENT FROM EVERY EARLIER SUSTAINABILITY PASS
**Kam looked at the built page tonight at ~21:00 and ruled against its LAYOUT.** His words: *"For Nexus sustainability tab, use this layout. this is much better. the current one up on screen is not good."* The cause was not the builder's: every brief in the chain had carried the mock's FIGURES and none had carried its DESIGN, so the previous round built the right content inside the old page shell. **This round rebuilt the shell to the mock, and your job is to judge it against the mock — not against my description of the mock.**

**THE MOCK IS AN EXPECTED ARTEFACT AND YOU READ IT DIRECTLY:**
`git show d18d4e8:docs/sustainability/mocks/s25-relayout-mock.html` in `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files` (READ-ONLY, by SHA). Verified by Wednesday: `d18d4e8` is an ancestor of the branch head; the blob is `41525340ebef0160d262f09196c1f0d3a0ff9ca8`. **The annotation block at the bottom of that file is NOT part of the design** — it was the previous session's note to Kam.

---

## 1. Target
- **Surface:** `http://127.0.0.1:3073` — **`:3073` at `93cbdc4`**, pid 76341, stood by `scripts/qa-surface-up.sh`, reported `sess 0` / `tty ??`. **Re-verify that yourself before use, and sha-verify the served files against `git show 93cbdc4:` at START and at END.**
- **Controls, both up, neither to be disturbed:** `:3072` at `caf1fe7` (the pre-rebuild layout — the "before" Kam rejected) and `:3068` at `7a76fe3`.
- **Stated by the builder rather than glossed, and worth your own check:** the surface is at `93cbdc4` while the branch head is `84ea613`; the commits between are a Playwright spec, a capture script and docs, and it claims **every product file is identical**. Verify that claim — it is exactly the "a green obtained against something other than what shipped" class you named at pass 14b.
- **Where the code is:** the same repo, READ-ONLY, by SHA. **Production?:** NO. Nothing deploys from this pass; `--0000094` still serves `9520b8c` and the earlier deploy GO is WITHDRAWN.

## 2. THE FAIL CONDITION, first and out loud
**Open the rebuilt tab and the mock side by side, and answer one question in your first line: would Kam recognise this as the design he approved?** Then decompose it into the seven properties the rebuild claims to have closed, each measured in the RENDER, not in the source:

| # | the mock's property | how to measure it |
|---|---|---|
| 1 | two-column grid `minmax(300px,1fr) 2fr`, metrics left, improvements right | computed grid on the container, and the actual painted geometry |
| 2 | **collapses to one column under 900px** | resize and measure; the builder claims 900px |
| 3 | chrome topbar carrying the title and the window as a white pill | painted, both modes |
| 4 | figure **TILES** — `.n` value over `.k` caption, eye at top-right, `min-width:150px` | per tile, and confirm a group does not read as one running line |
| 5 | bordered uppercase **chips** replacing the Bootstrap badge fills | and **no `#0d6efd` anywhere in the tab's computed styles** — that is F3 |
| 6 | the 335px evidence popover card | opened from an eye, in both modes |
| 7 | the rank tables' uppercase heads, right-aligned last column, tabular figures | rendered |

**Both modes and both widths.** The builder set dark through the product's own path (the preference seeded into localStorage before first byte) — **use the product's path too, and say which you used.**

## 3. The rows

| Row | claim | what you do |
|---|---|---|
| **1. THE LAYOUT (item 0, RD-281)** | All seven properties above closed; colour as literal hex with the token named beside each declaration, carried from the mock (NOT `var()` — `tokens.css` is linked by no shipped page, RD-234, and jsdom cannot resolve `var()`, RD-201); dark counterparts in `dark-mode.css`; **the brand gate moved seven counts with NO new palette value**. | FULL, in the browser. Then check the colour claim the way the builder says it is checkable: **an invented colour surfaces in the brand gate as a conformance failure, not as a count** — so verify no value outside the guide is painted, with a probe proving your sweep can fail. |
| **2. THE PROVENANCE BOX — an accessibility claim you must not take on trust** | The old "What these figures rest on" block **sits inside the aria-live region**, so deleting it would have silently removed the announcement a screen reader gets when a new window's figures arrive — *"something no screenshot could ever show"*. The builder restyled rather than deleted, and **FACT-CORRECTED Wednesday's brief**: the ENERGY/RD-61 sentence was never in that box; it is a separate block (the API's `notes[]`, "Read before using these numbers"), still rendered below the grid. | FULL. **Verify the announcement still happens** — change the window and confirm the live region announces. This is the one finding in this round that no visual check can reach, and it is the reason the box survived. |
| **3. F1 / F3 / F4 / RD-279** | F1 the doubled nouns gone AND the expectation fixed (the whole-row assertion had asserted `5,338 sheets sheets avoided` as CORRECT, and its control compared two string literals). F3 no `#0d6efd`, swept in a real browser with a probe proving the sweep can fail. F4 the API half now stands the real router on a loopback server with a control that the call reached a server. RD-279 the row's accessible text is the phrase alone, asserted on `textContent` with a glued-row control. | FULL. **For each, make the test go RED yourself** — that is the standing lesson of this campaign: the previous round's tests baked the defect into their own expectations. A fix whose test cannot redden is not closed. |
| **4. RD-278 and its arithmetic** | §6.1 takes IMPRESSIONS and the one call site handed it sheet columns. Two identities hold exactly on the 1,187 seed rows: `7,057+5,338=12,395=Total_Sheets_Used` and `7,057+10,676=17,733=Total_Impression_Printed`. **The under-count is 20.52%, NOT the 21.5% on the ticket** — the ticket's figure is that fault computed on the wrong base. | FULL. **Re-derive both identities and the percentage yourself from the raw rows**, with your own arithmetic, not by re-reading the API. If 20.52% is right, say so plainly: it corrects a number already written on a ticket. |
| **5. RD-282 — the phone overflow** | 701px of horizontal overflow at a 430px viewport, found by the builder's OWN narrow-viewport assertion failing on it; **measured on `:3073` AND on `:3072` before the rebuild — so pre-existing, not a regression.** | Confirm the pre-existing claim on both surfaces yourself. A "this was already broken" claim is exactly the kind that deserves an independent check, because it converts a regression into a backlog item. |
| **6. THE GATE AND THE SET, RUN** | `env -u SESSION_SECRET npm run verify` → 1383/1383 across 79 suites at `93cbdc4`; the real-engine set (`sustainability-layout` + `improvements-pane-spacing`) 12/12 in ONE command; contrast sweep 17/17. | **RUN them, do not read them.** Declared count = passed count = per-file sum, reconciled three ways — a partial total reading as a verdict is the trap. |

## 4. Credentials — none required. A prompt for any credential = STOP and report.
## 5. State-mutation & cleanup — you mutate nothing in the repo. Fixtures are built ADDITIVELY in your own scratch, in fresh dated directories; **nothing is deleted** (a restore control writes the original bytes back and asserts the sha — "the file was deleted" proves only that the deletion ran). Do not disturb `:3072` or `:3068`.
## 6. Output boundary (fixed) — findings, report and recommendations only. Fix-shape and regression test in prose per finding, with the code path read.
## 7. Known-fragile / known-changed
- **A finding is a claim too, and this campaign has one on the record:** pass 15's F2 called a provenance sentence false by measuring `9520b8c..caf1fe7` when the sentence was about `caf1fe7..6abb670`. Wednesday verified both pairs (3 files vs **0**); the builder was right. **Give every finding you file the same provenance you demand of the builder** — name the exact pair, ref or selector it rests on.
- Do NOT re-flag: RD-277 (untouched by ruling), the withdrawn `caf1fe7` deploy GO, RD-280 (deliberately not regenerated — the builder found the documented regeneration procedure silently deletes the file's own explanations, which is its own finding), or anything already in your s21–s26 passes.
- BSD tools on this Mac: awk has no `IGNORECASE`. Pin readers against a captured header.

## 8. Logistics
- **Time-box:** ~75 minutes. Rows 1, 2 and 3 FULL; rows 4, 5, 6 FULL-cheap. Stop when findings repeat.
- **Findings sink:** `projects/nexusai/reports/2026-09-03-s28-round19-pass16/` under YOUR project tree, `SUMMARY.md` the entry point, screenshots in `evidence/`.
- **Report to Wednesday by mail** (`wednesday-agent@agentmail.to`) when the SUMMARY is written. Lead with the VERDICT and with your answer to the first-line question — **would Kam recognise this as the design he approved?** — then the FAIL conditions and what each did, then findings by severity, then **NOT TESTED at the same weight**.
