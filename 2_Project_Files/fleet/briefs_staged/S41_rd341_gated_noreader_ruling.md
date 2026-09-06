## BLUF
**RD-341 @ `cbc8812c4f547e48e5615385f655919afc5de314` RECEIVED → under a tier-2 through-code gate (launched 12:10:06 (pane %85 QA/NexusAI-s41-rd341, wrapper --check rc 0, red-proofs rc 6 / rc 7 read bare)). Three rulings: (1) `no-reader` stays a DISTINCT verdict and is NOT an offence — but its count is PINNED to a literal naming the file (1 today: `sustainability-settings.test.js:51`), so a loss OR a gain reds by name; the shipped cell's `toBeGreaterThanOrEqual(0)` is a floor that cannot fail and comes out in the fix. (2) The counts-file conflict with RD-339: REGENERATE at the merged tip, never hand-pick — ratified, S40's precedent. (3) RD-334: YES, write the design as a proposal on the ticket + a mail to Wednesday BEFORE any build — after the RD-339 fix round.**

## 1. `no-reader` — the ruling
Your reasoning holds: the guard's rule is about UNLABELLED readers, and a stand with no reader cannot serve rows, so it is not an offence. **What is missing is the pin.** `expect(noReader.length).toBeGreaterThanOrEqual(0)` is decoration — a check that cannot fail — and a `no-reader` reporting path that stopped pushing would leave the cell green over an empty filter (the gate is told to measure exactly that pair). Fix-shape, small: pin the count to a literal with the file named in the message (`expect(noReader.map(s => s.file + ':' + s.line)).toEqual(['sustainability-settings.test.js:51'])` or the equivalent), so the day a stand loses its `getRows` by accident the cell names it, and the day :51 gains a reader the pin is edited on purpose. **Wait for the gate's verdict before committing it** — if the gate confirms the pair, the fix rides in the round-1 fix commit with whatever else it finds; if the gate finds nothing else, it is a one-commit fix round. Do not touch `rd-341-label-guard-s41` until the verdict.

## 2. The counts file
Whichever of `rd-339-python-gate-s41` (→ 2123/111) and `rd-341-label-guard-s41` (→ 2111/110) merges second conflicts on `scripts/verify-expected-counts.json`; the resolution is `npm run verify -- --update-counts` at the merged tip and the regenerated number committed — never a number chosen by hand. Ratified; the gate measures the conflict now so the GO can name the order.

## 3. RD-334 — design first, yes
Write it up as the ticket's own standing ruling asks: classify-and-name (the way `dark-ground-luminance` does) rather than the subtractive filter that killed a control on the first attempt; the proposal on the ticket AND a mail to Wednesday with the design, its controls, and what it cannot see. **After the RD-339 fix round** (12:02 ruling; round 2 of 2 under the cap) — that round is first. No build on RD-334 until Wednesday rules on the design.

## 4. State
HELD: `7eac4ff` (RD-339 — the fix round lands on that branch), `7def418` (RD-180+251, browser gate since 11:47), `cbc8812` (RD-341, this gate). Campaign tip `9c8e63a…` unmoved. `s40-history-docs` parked. No deploy; the RD-333 pairs hold stands; nothing ships without Kam's word.

PROVENANCE:
- `refs/heads/rd-341-label-guard-s41` = `cbc8812…`; tip `9c8e63a…`; rev-list 1; 2 files +121/−12 + 2/2 | `git ls-remote origin` + local objects from Wednesday's seat, NO fetch | read 2026-09-06 12:0x
- The diff READ WHOLE by Wednesday (incl. the `>= 0` cell) | `git diff 9c8e63a...cbc8812` | read 2026-09-06 12:0x
- Your READY (the seven rows; the live stand; the three fixes; the conflict; gate 2111/2111; RD-341 Testing 37211; the two questions) | 2026-09-06T02:01:50Z, read whole | read 2026-09-06 12:0x
- The RD-339 fix-round ruling this sequences after | `briefs_staged/S41_rd339_nogo_fixround.md`, sent 02:02:53Z | 12:0x
- The gate launch | `cockpit.sh add` receipt in Wednesday's own output | 12:10:06 (pane %85 QA/NexusAI-s41-rd341, wrapper --check rc 0, red-proofs rc 6 / rc 7 read bare)

SELF-CHECK: re-read end-to-end | 2026-09-06 12:10
(checked: the no-reader ruling answers the question asked with a default and a fix-shape sized in one line; the pin fix is held until the verdict so the branch under gate does not move; the counts resolution is the repo's own precedent; RD-334's order is after the fix round already ruled at 12:02, no contradiction; the launch line is from the receipt; no Secuura content.)
