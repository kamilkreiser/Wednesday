# QA RE-GATE — Datasec/NexusAI RD-361 **F-2 census cell**, `rd-361-round4-s45` @ `f93730c`. **TIER 2.**

## Scope — narrow on purpose, and TIER 2 means through-code only
This is a **follow-up on an already-gated mechanism**, so it is tier 2: **read the code, run the
suite, tamper the guard. No browser, no rendered surface, no state matrix.** The predicate itself was
gated at tier 1 at `400718f` and came back **GO with findings**; this re-gate covers **one finding's
remedy** and nothing else.

**Only F-2's cell is in scope.** The documentation corrections shipped in the same commit are NOT
gated — they were verified by Wednesday against the artefacts directly.

    f93730c   rd-361-round4-s45   THE SUBJECT (pushed)
    400718f   same branch          the tier-1-gated predicate. Base: `400718f..f93730c`.
    NOT main — ~251 behind.

Builder's claim: **PASS 2185/2185 across 113 suites** (2182 → 2185, three cells added).

## What F-2 was
The tier-1 gate found the round's **load-bearing census** — *"`authEnforced` has exactly two writers,
both via `setSetting`"* — was **guarded by no test at all**. Its framing is the one that matters:
***"round 3's failure class one level down — a census correct when written and undefended
afterwards."*** Add a bulk import, a seed path, a migration, or convert `server.js:3349` to
`writeFile`, and **all 2182 tests stay green while the gate relaxes on a deployment that had auth
enforced.**

## 🔴 THE ONE QUESTION THIS RE-GATE EXISTS TO ANSWER
**Can this cell actually fail, for the right reason, against the REAL `server.js` — not against a
copy it authored?** A guard that asserts a string is present is not a guard
(*"a string in a file is not a behaviour"*). Ask what would make it fail, and then make it fail.

The builder says it red-proofed **on disk against the real `server.js`**, not only in-cell copies:

    M-A  a THIRD setSetting writer added ................ census RED
    M-B  server.js:3349 converted to a bulk writeFile ... census RED
    both restored, 0 markers left

**Re-run both yourself**, asserting each tamper LANDED before reading its result, and restore.
**Then find a third mutation the cell does NOT catch** and say so — that is the finding if it exists.
Candidates worth trying: a writer in a file the cell's glob misses; a computed key
(`setSetting(k, …)` where `k` resolves to `authEnforced`); a writer reached through a helper or a
re-export; a write in a `.mjs`/`.ts`/generated file; a bulk `saveSettings` that carries the key
inside an object.

## THE CELL'S OWN FRAME — the thing most likely to be wrong
The cell counts over **all 80 `backend/**.js` files**, comments stripped, `node_modules` excluded,
and the builder states four object-literal occurrences are `res.json(...)` response payloads rather
than leaving them uncounted. **Check that frame against the question it is supposed to answer.**
`backend/**.js` is narrower than "everywhere the key can be written" — round 3 died precisely because
a `backend/` sweep could not see `static/`. **If the frame is narrower than the guarantee, that is a
finding even though the cell passes**, and the honest remedy may be a stated limit rather than a
wider glob.

## THE CONTROL — the builder disclosed something about it; verify the disclosure
Its control drives the same `censusOf()` over tampered copies. It says: *"the control cell also
reddens under both M-A and M-B — correct, it asserts its own baseline of 2 before tampering, and I
say so rather than let it read as a broken control."* **Decide whether that is sound or whether the
control and the census are one instrument wearing two names** — two layers that fail together are one
layer, and this project has shipped exactly that before (RD-329's F-2).

## ALSO IN THE COMMIT, in scope only as regression
- The docblock's corrected residue boundary (Wednesday verified the wording directly).
- Nothing else may have moved: confirm `400718f..f93730c` touches only the test file, the docblock
  and the counts JSON. **If it touches the predicate, that is a finding and it changes the tier.**

## Evidence rules
Positive control on the instrument · every tamper asserted **LANDED** before its effect is read ·
read every hit before counting it · **NAME THE FRAME** in any completeness claim · **FOUND / TESTED /
HOW with the controls named under HOW** · state what you did NOT test.
**Stop any server you start and prove the port reads 000** — the round-4 gate's housekeeping omitted
this and `pane_close.sh` caught a listener dying with its pane.
No `az`, no registry, no demo, no staging. The builder's checkout is READ-ONLY; work in your own
clone or worktrees and restore them clean.

## Verdict
**GO · GO-with-findings · NO GO.** A guard that is real but narrow is **GO-with-findings** — say so
plainly rather than failing it for a stated limit. Report to **Wednesday**. Write the report under
`projects/nexusai/reports/2026-09-07-rd361-f2-census-tier2/` and name the path in your mail.

PROVENANCE:
- Head f93730c | `git -C <NexusAI>/2_Project_Files ls-remote origin refs/heads/rd-361-round4-s45` run by Wednesday - Wednesday's read, not yours | read 2026-09-07
- F-2's statement and the cell design | /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-rd361-round4-tier1/report.md finding F-2 | read 2026-09-07
- The M-A / M-B red-proof and the control disclosure | the builder's follow-up mail 2026-09-07T12:32:22Z, DKIM-verified - relayed, not re-measured by Wednesday | read 2026-09-07
- The tier rule (through-code only for an already-gated follow-up) | /Volumes/KK_T9_External_HDD/WEDNESDAY/0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md - Wednesday's tree, not yours | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 22:40
