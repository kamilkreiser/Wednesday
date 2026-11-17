**BLUF:** On the revenue calculator, the grey unit box beside each input (reps, customers, devices, %, USD / hour, hours, USD, USD / device / month) is now one slim fixed width (86 px). The number box beside it is wider (138 px, 1.6 times the grey box), and the labels and helper sentences keep the width they have on main. Styling only: one class string in one component, plus a unit test and a browser layout test. No label, hint, unit string, number or default changed. Nothing deployed; no integration with HP tools.

## What this changes against main
- `RevenueCalculator.tsx`, one line: the unit box goes from `max-w-32` (a cap and no width) to `w-[5.375rem] shrink-0 items-center justify-center` with `px-1.5 text-center text-[0.6875rem] leading-4` (86 px, never shrunk, centred, 11 px text; a long unit may take a second line). The control column keeps its existing `14rem`.
- `Revenue.restyle.test.tsx`: one new test group, "A5 input unit boxes", which checks the classes, the 14rem column and the unit text on all 16 boxes.
- `html-layout.spec.ts`: one new row, T20, measured in a real browser on the offline mock at 1280 and 390 px: one width for all 16 boxes, the number box at least 1.5 times the grey box, the label column at least as wide as before, every unit text fully visible, boxes as tall as their inputs, and the inputs and boxes on one left edge per step.

## Measured, main against this branch (steps 1, 3 and 4, local build)
| | main | this branch |
|---|---|---|
| unit box width, 1280 px | 28.1 to 85.0 px (spread 56.9 px) | 86.0 px, all 16 |
| lines in a unit box | up to 3 ("USD / device / month") | 1, and 2 for "USD / device / month" |
| box height | 44.0 px, 50.0 px on the 3-line box | 44.0 px, all 16 |
| number box width, 1280 px | 139.0 to 195.9 px | 138.0 px (1.6 times its grey box) |
| hint paragraph width, 1280 px | 203.2 px | 203.2 px |
| label and hint line counts | - | 0 of 96 rows differ from main (1280, 820 and 390 px) |
| 390 px | boxes 28.1 to 96.5 px | 86.0 px, 44.0 px tall |

The width is a tuning value and the properties are the contract. The smallest room round the longest unit was 2.75 px in the default font, and 0.13 px in the tightest of seven other system fonts tried.

## Tests
- The new unit test is red on main (the `w-[5.375rem]` class is missing) and green here. T20 is red on main (the unit boxes differ in width and left edge, and the long unit takes three lines) in desktop and tablet, and green here.
- Whole unit suite: main 4338 passed, this branch 4339 passed; one test added, none lost or changed.
- `html-layout.spec.ts`, desktop and tablet, retries 1: 42 passed. `playbook-partner.spec.ts`, desktop and mobile projects (the revenue walk, axe and no-side-scroll rows): 14 passed.
- lint, typecheck, build and the shard plan: exit 0. Infra tests 325 OK; `validate.sh` exit 0.
- Not run here: the other e2e shards (they carry no revenue row; the shard plan proves each test is in exactly one shard).

Styling only. Nothing deployed. No integration with HP tools.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
