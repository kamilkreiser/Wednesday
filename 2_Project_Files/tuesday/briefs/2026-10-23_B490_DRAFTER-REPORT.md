# B490 drafter report (Sonnet, read-only), 2026-10-23 about 01:00-01:40 AEDT

## BLUF
- **Brief:** `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B490_SEAT-K1_hpsmpoc-178-held-name-exactness-pins.md` (121 lines). Seat `Datasec/HPSM-POC-K1` (live panes at the read: `tuesday`, `Datasec/HPSM-POC-J1`, `fleet-monitor`; K1 free). Sonnet C2, tier-2 delta gate later. Branch `b490/hpsmpoc-178-held-name-exactness-pins` from main `4e77cf1d171a4d623ea97700e2c207f647c6c31f` (ls-remote / gh read; PR #187 merged 2026-10-22 13:52:06 UTC, merge sha = main).
- **Ports 8390-8399.** `lsof` over 8380-8399 empty (rc 1); `-w '839[0-9]'` over `tuesday/briefs/*.md` hits the B488 brief (names 8370-8399 unclaimed) and two NexusAI briefs where the match is not a port; B489 holds 8370-8379, B491 expected 8380-8389. No B490/B491 brief exists yet. Tests are in-process.
- **Property P:** every way the held-name allowance could be widened (case, edge white space on either side, length) is refused by at least one row, at the API and in the mock; the deliberate trim-on-save is pinned by a row that reads the stored text. Rows R1-R5 (API), M1-M3 (+ optional M4) (mock) are "at least these"; the closing battery A1, A2, A3, A4, A6 (+ mock analogues, + sanity re-run of A5/H1/H3/H4/M-mock1/M-mock2) must kill every named mutant.

## Edit sites read (all at `4e77cf1d` through `gh api contents`; the local clone does not hold that object)
- `api/src/HpsmPoc.Modules.Assessment/Endpoints/Requests.cs:141` `if (name.Length is < 1 or > 120) e.Add(new("customer.name-length", ...` ; `:146` `if (FollowUpShape.HasControl(name) && !string.Equals(name, heldName, StringComparison.Ordinal))`; `:137-138` signature with `heldName`.
- `CustomerEndpoints.cs:194` `Shape.Customer(... heldIndustry: customer.Industry, heldName: customer.Name)`; `:198` `customer.Name = body.Name.Trim();`.
- `web/src/server/mock/customer-detail.ts:58` `if (typeof b.name !== "string" || !hasControl(b.name) || b.name === held) return null;`; `:82-84` length check before `nameRefusal`; `:85` `nameRefusal(b, c.name)`; `:92` store `b.name.trim()`.
- `api/tests/.../Assessment/Hpsmpoc178CustomerNameTests.cs` (400 lines): `AssertRefused` :79, `HeldName` :239, `Plant` :243-257 (read-back equality at :255), `Save` :259, existing held rows :271-348 (length row :325 sends a NON-held 121-char name), append point after :348.
- `web/src/server/mock/customer-name.test.ts` (231 lines): `expectRefused` :41-47, `HELD` :165, `plant` :168-172, append point after :230.

## Corrections the brief carries (line numbers differ from the relay)
- Task text and gate: compare at `Requests.cs:147`, A3 block at `:144`, mock guard at `customer-detail.ts:57`. At main: compare `:146`, length rule `:141`, mock guard `:58` (`nameRefusal` itself starts `:57`). The brief states the main numbers and tells the builder to re-measure.

## Design points worth Tuesday's eye
- A planted held name MUST hold a refused character (U+202E), otherwise `HasControl` is false and the allowance is never exercised; the brief says so and a program check asserts it for every new text.
- Gate fix-shape row (2) kills A2 only (held + space vs `heldName.Trim()` is still unequal under A4). A4 needs a held name with edge spaces: R3 (sent back unchanged) kills A2 and A4 together; I added **R4** (edge-spaced held, TRIMMED text sent -> 400) as the independent A4 killer. R4 and mock rows M2, M3 (and the mock analogues A1m, A4m) are mine, not the gate's.
- A3 form: the gate's defined it as "whole name block skipped"; the brief gives the length-rule wrap and asks the builder to name the form it uses and kill both.
- Mock has no A3 analogue (length check runs before `nameRefusal` and ignores `held`); stated, no row invented. A7 (equivalent) and B488-5/-6 edge-scalar differences are fenced off.
- Additions only in both files, appended block, existing helpers reused; 2-path partition; no product change (STOP).

## UNMEASURED (and why)
- That the new rows are green at main and red under their mutants (no build/test/mutant allowed; kills reasoned from the files and the gate table).
- That `Plant` reads an edge-spaced stored name back untrimmed (gate planted ` H `, RELAYED), and that SQLite stores an over-120 name (RELAYED 125 units).
- Class test counts; whole-suite counts; Api-queue wait (B489 and the B491 gate will contend).
- Jira HPSMPOC-178 state (no Jira query by the drafter; builder records it; Tuesday fills the slot).
- `records/b490`: absent by `rev-parse` at the project root (control `records/b467` printed `7d723d13...`).
- Other branches' intersections (only #186, #184, b489 read): builder re-runs the program.

## Departures from the templates
- Fresh branch, new-ref plain push (B489 shape), but the commission follows B488's findings, not a ticket; Jira slot is HPSMPOC-178.
- Mutant battery is a first-class closing gate with named anchors (B482 style), plus a no-op mutant control, plus sanity re-run of the older H/A mutants.
- Whole web suite required (mock file touched); Feedback and Reporting projects not required (nothing there moves).
- Note: the brief contains one non-ASCII glyph (the `≤` quoted from the mock's 400 message); it is a brief, not a test file.

## `____` slots left for Tuesday (8 lines; count control reads 8)
1. Stamp time 2. Stamped by 3. Launch authority 4. Hard stop and target READY 5. Main at launch (expected `4e77cf1d`) 6. Jira HPSMPOC-178 state at launch 7. Model receipt line and load1 at launch 8. Last line `READ-WHOLE-BY-TUESDAY: ____`
