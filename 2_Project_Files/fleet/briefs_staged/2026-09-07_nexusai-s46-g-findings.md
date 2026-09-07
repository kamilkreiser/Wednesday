# BRIEF — Datasec/NexusAI seat S46: both moved heads passed, and the gate found FIVE things in the guard we built to stop exactly this

## BLUF
**You are the successor to S45, which handed over cleanly at 23:03.** Its handover is
`HANDOVER-S45.md` at the NexusAI **project root** (outside the repo). **Read it before this brief's
queue** — especially its **§0**, which it promoted above the branch table on Wednesday's instruction.

**Both moved heads came back GO WITH FINDINGS.** Nothing is broken, nothing is live, **and nothing
here is urgent.** Your queue is five findings on a *guard*, not on the product.

    rd-361-round4-s45  @ 731aa6e   GO with findings   G-1 · G-2 Major, G-3 · G-4 · G-5 Minor
    rd-148-round2-s45  @ 690bed9   GO with findings   the cleaner of the two

**Gate report — read it, do not work from this summary alone:**
`/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-moved-heads-tier2/report.md`

**NO MERGE, NO DEPLOY.** Kam's two GitHub answers gate all three merges and have done all evening.
**Datasec has NO production grant** — his 12:07 lift was narrowed at 12:10 to Secuura only.

## THE SHAPE OF WHAT HAPPENED, because it is the point
Round 4 fixed a bricking Blocker. Its census claim was then guarded by a cell (F-2). **That cell's
comment-stripper was blind in 18 of 80 files because `https://` contains `//`.** The cell was rewritten
on an AST. **The AST version now misses three shapes the regex caught.** Each fix has been real; each
has opened something narrower. **You are not being asked to end that regress — you are being asked to
close these five and to make the record honest about what remains.**

## THE QUEUE

**1. G-1 (MAJOR) — the AST census misses what the regex caught.** The old counter took any
`authEnforced` substring within 400 chars of a `writeFile(`. The new one needs a syntactic `Property`
node. Three additive, in-frame shapes in `backend/server.js` bypass the stamp and pass:
`writeFileSync(p, ` + a **template literal** + `)`; the same with a **string literal**; and a **spread
carrying a variable named for the key**. **`T-A8b` passes the entire file — 33/33.** Its matched pair
`T-MB2` (identical hazard, object literal) is **RED**; the only variable is **serialisation**.
*Credit the gate recorded: the spread case IS caught, by the object-literal cell — a real second net —
but that cell reads `server.js` only and cannot see a string.*
**Fix so the guard covers serialised writes, and red-proof with the T-A8b / T-MB2 pair** — one
variable, both directions.

**2. G-2 (MAJOR) — and read this one carefully, because the defect is in the RECORD, not the code.**
S45 kept `stripComments()` for the WIRING cells, reasoning that a URL on a line cannot hide what those
cells count. **The gate ruled that reason FALSE twice over.** (a) A URL *can*. (b) **The live damage
needs no URL at all**: two ordinary prose comments contain `/*` — `server.js:638`
(`// static/js/*.js …`) and `server.js:1097` (`// an /api/setup/* route.`) — each opening a bogus
block that runs to the next `*/`. Measured against acorn's own comment ranges: **31,845 non-comment
characters deleted across 116 ranges; lines 638–713 and 1097–2062 gone — about 1,040 lines.**
Proven with a byte-identical payload in three placements: outside the hole → **RED**; **inside the
hole → GREEN**; with a URL on the line → **GREEN**. **`THE BUG` is a `not.toMatch`, so deleting text
makes it PASS — it fails OPEN.**
**🔴 STATED PLAINLY AND YOU MUST NOT OVERSTATE IT:** **no current deciding site sits in a deleted
span** (all nine are at line 2349+), the four WIRING patterns count identically raw and stripped
today, and the WIRING cells are **byte-unchanged** in this diff. **There is no live defect and this is
NOT a regression from `731aa6e`.** What is wrong is that the commit records the question as considered
and settled on a reason that does not hold.
**Fix: remove `stripComments()` and read those cells off the AST too. And put this sentence on the
record, which is the gate's own and Wednesday endorses it:**
> *No future round may cite the WIRING cells as a completeness claim over `server.js` until
> `stripComments()` is gone.*

**3. G-4 (Minor) — the `__tests__` exclusion cell's title claims a property of the image; its
assertion checks a spelling.** `D-1` (append `COPY __tests__/ …`) → **RED**, good. But `D-2`
(`COPY . .`) → **GREEN** — ships tests and never says so — and `D-3` (`ADD` instead of `COPY`) →
**GREEN**. *Fairly stated by the gate: `.dockerignore` does exclude `__tests__` today, so `D-2` would
not in fact ship them — **but the cell does not read `.dockerignore`, so that green is luck.*** It
also reads only the root `Dockerfile`; `docker/Dockerfile.backend` is tracked and unasserted (copies
`backend/` only — no live hole). **Either widen it or retitle it to what it checks.**

**4. G-5 (Minor) — the "256 computed assignments" names the wrong frame.** Re-derived over three
frames the gate names: **239** over the guard's own frame (148 tracked JS minus `__tests__`), **256**
over all 269 tracked JS *including* `__tests__`, **145** over `backend/**`. **256 reproduces exactly —
over a frame 121 files wider than the guard the sentence qualifies.** The limit itself is **sound**
(239 > 0, so asserting zero really is unavailable) — **the number just names the wrong frame, in a
docblock whose entire stated purpose is that round 3 died of exactly that.** Say **239**, or say which
frame 256 is over.

**5. G-3 (Minor) — a supply-chain fragility in the guard.** The cell does `require('acorn-walk')` and
**`acorn-walk` is declared nowhere in `package.json`.** `acorn` is (devDeps 8.18.0); `acorn-walk`
arrives only as a **transitive dev dependency of `acorn-globals`**. The lockfile pins it today, so it
works — but a guard that depends on someone else's transitive dep is one `npm` change from silently
not running. **Declare it explicitly.**

## HOW TO WORK
**One ticket per logical path** (Kam's 13:23 rule) — the five are one story: *the F-2 guard's
coverage and its record.* **Search the board by SYMBOL / PATH / ERROR STRING before filing** and say
what you searched. **Build in a worktree, not by switching the checkout** — S45 took that note after
its checkout moved under a live gate.

**Every claim carries FOUND / TESTED / HOW with the controls named under HOW** (Kam's standing
instruction). **NAME THE FRAME** in any completeness claim — three separate findings tonight were
frames that were narrower than the sentence they supported, including two of Wednesday's own.
**Never delete — quarantine.** **A GO names a head:** if you push, say so and say which verdicts your
push has just made stale.

**When your queue is dry, say so and stop.** Overnight is permission, not a quota, and an honest
"nothing left that needs no one else" is a real answer.

PROVENANCE:
- Both verdicts, G-1…G-5, the 31,845/116/1,040 measurements, the three-frame re-derivation | the tier-2 gate's mail 2026-09-07T13:34:32Z and its report at /Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-07-moved-heads-tier2/report.md | read 2026-09-07
- Both heads resolved by the gate's own `git ls-remote`, and by Wednesday's launch wrapper before it started | /Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/fleet/launch_qa_nexusai_moved_heads.sh - Wednesday's tree, not yours | read 2026-09-07
- Kam's merge/deploy grants and the Secuura-only production narrowing | /Volumes/KK_T9_External_HDD/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh output - Wednesday's tree, not yours | read 2026-09-07
- S45's handover | HANDOVER-S45.md at your own project root, outside the repo | read 2026-09-07

RULED BY KAM, NOT YET IN AN ARTEFACT

- rd104-gh-identity-acceptance-false-premise: "You check the two settings pages yourself - two clicks, links below (recommended)" -> must land nowhere by your hand; it is Kam's own action and the three merges wait on it. Do not merge anything.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 23:45
