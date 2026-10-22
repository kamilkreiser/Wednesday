# B494 drafter report

- Brief: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-23_B494_SEAT-G50_hpsmpoc-b490-round2-gate.md (35 KB; target was under 30 KB, over because the Standing and HOLD paragraphs were kept whole).
- Seat Datasec/HPSM-POC-G50 (free; panes: tuesday, fleet-monitor, K1, J2). Ports 8420-8429 (no listener 8380-8439; 8425 token belongs to finished B412). Model row G2.
- MEASURED 03:20 AEDT by GitHub API: main 4daa4054, branch 6708ac6b, compare main...b490 ahead 2 behind 2, no open PRs, no b494 ref, b493 not on origin (404). Read: B492 gate brief, B490 ADDENDUM-1, builder STATUS ADDENDUM-1, B492 findings.
- RELAYED: 74->82 Api, 97->105 mock, +23/+15, kill counts, whole-suite figures (left to the gate to read and re-measure).
- Departures: (1) ls-remote over ssh failed for me (stale identity path in the local clone), so refs came from the API; the brief tells the seat to fall back the same way and STOP if fetch fails. (2) Added counts: the 16 new cases are 8 Api + 8 mock, so whole-suite added is 8 per side, not 16; the brief says so. (3) Gate re-runs A1,A2,A3a,A3b,A4,A6 plus new variants X1-X3, Xm1 (my names). (4) Brief has 8 underscore-slot lines, 0 at-sign hits, 4 lines with non-ASCII punctuation.
- Slots left `____`: the 7 Stamp lines and the last line READ-WHOLE-BY-TUESDAY.
