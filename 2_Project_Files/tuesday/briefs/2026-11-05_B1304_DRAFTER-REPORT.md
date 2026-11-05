STARTABLE: YES once Tuesday stamps (builder branch unmoved at drafting, main unmoved, 0 open PRs, ports free); one schedule-neutral risk in Q-3.

**BLUF.** Kit B1304 (seat H126, Sonnet, row C2 `model-routing.md:92`) is a one-commit fix round on `b1295/hpsmpoc-html-layout-round-2` @ `9d34ad68`: the Major (`html-layout.spec.ts:151`, header 72 px at 768 px Admin, 128 px under Verdana/DejaVu) becomes a same-run property (button weight 600 AND bar height equal to the height with buttons forced to 600; no literal), proved green at default font and under the repo's `WIDE_FONT` (`playbook-quality.spec.ts:108`), with plant P-1 (header button weight to 740) red. Three optional Minors (a severity probe inside T13, `pr-10` instead of the inline style, a guard on the print `.page-head`) each only if proved presentation-equal, else NOT DONE. Lane: 4 paths. It adds no test, so the worst hosted job (`prototype-tablet-1`, gate projection 951 s of 960) must not rise; the seat re-projects and STOPs if it does.

## Facts re-measured (instrument; control)
- Clocks (`date`): start 13:41:50, files read by 13:43, kit written 13:44, slots 13:44:43.
- Refs (`gh api -X GET`, 13:42:13): branch `9d34ad6819681d683bd8f286cd074f7962d649e8`; main `73adb50c9d06fd4587143ecfaab1014708afd722`; open PRs 0 (`--jq length`). The local project checkout lacks both objects (`cat-file -t` fatal), so every pointer was read from raw blobs fetched at the pinned sha (control: the fetched spec is 310 lines and its `:145` is the Admin test, `:151` the 72 literal).
- Pointers by `grep -n` over those blobs: `html-layout.spec.ts` :142, :145, :151, :152-153, T13 :199-215; `Card.tsx:17`; `Card.test.tsx:68` (no style) and `:74` (`toHaveStyle paddingRight 40px`: this unit test must change with the class swap); `globals.css` :162 (header guard), :166 (`.page-head,` bare), :167-169 (guarded neighbours), :182-185 (`edge-customer-*`); `Button.tsx:9` (`[header_&]:font-semibold`); `playbook-quality.spec.ts:108` (`WIDE_FONT`).
- Which hosted job: B1301 STATUS `:64` table, `prototype-tablet-1` 951 s worst-setup projection (79.3 percent), next `prototype-desktop-2` 936, `journey-and-prototype` 877; the spec runs in journey-and-prototype (desktop) and prototype-tablet-1 (tablet) (STATUS `:56`). RELAYED, not re-run.
- Model: routing row C2 `:92`, gate-NO-GO column "one fix round on the same seat model" via C1 `:91`; `models_latest.json:23` sonnet id; launch carries `BRIEF_SEAT_LEVEL=sonnet` inside the quotes (`brief_seat.sh:24` defaults to opus).
- Ports 9280-9289: `lsof -nP -iTCP:9280-9289 -sTCP:LISTEN | wc -l` 0 (control all listeners 13); `-w -E '928[0-9]'` scan of 55 non-`.pre-` SEAT kits of 11-04 and 11-05 hit 0 (control `9240|9813` hit 2). Panes: %0, %244, %245, %1.
- Kit checks: 48 lines (long lines), four-underscore lines 10 (9 slots + last line), non-ASCII lines 0 (`LC_ALL=C grep -c -v -x -E '[ -~]*'`), slots.json 10 keys parse. Kit text has no person's name and no card id.

## D-decisions
- D-1: the same-run property (weight 600 plus height equal to forced-600 height) rather than "72 px from 1024 up": it keeps the 768 px claim the row exists for; the gate offered both.
- D-2: Minors are conditional on a presentation-equality proof each, because the gate called them optional; NOT DONE is an allowed outcome and is named in the READY line.
- D-3: the severity probe appends four `li` elements with the `edge-customer-*` classes inside the existing T13 test instead of reviewing four findings in the journey (a journey review costs seconds on the tightest job); no new test.
- D-4: the unit test `Card.test.tsx` is in the lane because `:74` pins the inline style and would go red with the class swap.
- D-5: `pr-10` is conditional on computing 40 px (rem versus px); fallback `pr-[40px]`.

## Q for Tuesday (each with a default)
- Q-1: `html-layout.spec.ts:142` (header 72 at 1280 px, Partner) is also a literal; the gate named only `:151` and measured 24 of 24 wide frames equal. Default: leave it.
- Q-2: do the print guard and the class swap ride this round? Default: yes if proved equal, else NOT DONE (they do not block the landing).
- Q-3: the projection is a projection; a hosted run is the proof. Default: the seat stops if its re-projection passes 960 s, and does not move the tablet copy of the spec (outside the lane).

## UNMEASURED
- Whether the forced-600 reference height equals the real height under the hosted Linux font (the property needs only equality; a hosted run will show it). Verdana is not DejaVu Sans. The new projection. Whether `pr-10` computes 40 px on the built page. Landing form (squash) RELAYED from the B1295 kit `:95`, not re-read at source.

## Outside the fences
None crossed. Read: DRAFTER_RULES, B1301 STATUS and evidence, B1295 kit and STATUS pointer lines, B1298 kit and slots (shape), model-routing, models_latest, raw blobs via `gh api -X GET`. Scratch copies of 4 blobs written into the session scratchpad (overwrote same-named earlier scratch files there). No card read, no ledger, no other client.
