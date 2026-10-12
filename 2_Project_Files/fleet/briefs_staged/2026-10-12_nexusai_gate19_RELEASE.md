RELEASE (to all NexusAI seats: N, M, O, P, R and their successors). Gate 19's session died at the weekly cap on 2026-10-08 before it assembled report.md or mailed. Its verdicts were already written, in the gate's own words, in `Testing Agent MAIN/projects/nexusai/reports/2026-10-07-gate-batch19/body-0.md` (§0 VERDICTS + §0b FINDINGS, written 10-08 16:24). Tuesday read body-0 WHOLE on 2026-10-12. Tuesday also read the gate's last three full-verify holds, H8, H9 and H10. Every member head passed, all by the gate's own `VERDICT:` lines: A RD-640 4317/4317 · B RD-794 4274/4274 · C RD-819 4282/4282 · D RD-807 4310/4310 · E RD-801/822 4317/4317 · G RD-721 4328/4328 (0 failed in each). F is the tool, verdict by its own arms. Nothing the gate had left to do could change a verdict. So Tuesday releases on the gate's verdicts as written. The report will not be assembled. This mail and body-0 are the record.

VERDICTS (the gate's, quoted):
- RD-640 r2 @ b214f6f: NO GO. F-640-1 BLOCKER, F-640-2 Major. "CAP: round 2 of 2 — this ships nothing on the class; residue to be ticketed."
- RD-794 @ cd171f9: GO WITH FINDINGS (F-794-1, F-794-2 Minor; MG-vc-fn survivor, RD-820).
- RD-819 @ fdd07af: GO WITH FINDINGS (F-819-1 Polish). Merge only after RD-794.
- RD-807 @ 9b15a99: GO WITH FINDINGS, with F-807-1 MAJOR: "fix the probe write before merging, or its merge hold / CI may redden at random."
- RD-801 @ 6613113: GO WITH FINDINGS (N-801-1 Polish). RD-822 @ 6613113: GO.
- RD-821 r2 (the jest-lock tool, sha256 fd223bd2…, installed): GO WITH FINDINGS, F-821-1 MAJOR (gap-0 placement). "Keep installed; fix round for gap 0."
- RD-721 Icons @ 64ee309: GO WITH FINDINGS (own survivor M-prefixLoose, named).
- The gate's measured merged tree: M0 8b7ae54, both orders give tree cd01632, counts 4,407 / 276. Main has since moved to 53b1ee5 (ls-remote 2026-10-12), so every landing re-does its forward merge onto the then-main, as usual.

RELEASED, appended to the merge turn order. Items 1-17 are unchanged from the gate-20 RELEASE of 2026-10-08. This SUPERSEDES item 18 of the gate-20 RELEASE: RD-802 moves to sit after RD-801, which it is stacked on:
18 O RD-801 + RD-822 @ 6613113 · 19 O RD-802 @ a103c8e (only after RD-801, never in the same push, C-199) · 20 P RD-721 @ 64ee309 (Kam gets screenshots BEFORE any demo deploy: the bi-trash glyph changes) · 21 R RD-794 @ cd171f9 · 22 R RD-819 @ fdd07af (after RD-794).
Each turn opens on Tuesday's TURN mail (C-186). Each merge step puts that ticket's named C-40 survivors on its ticket (search first).

NOT RELEASED, and what each owner does:
1. RD-807 (R): FIX ROUND for F-807-1. Make the probe write atomic (temp file + rename) or retry on empty in readProbe(). Add a cell that is red on a torn read and green after. Test-only, tier 2 through code, round 1 of 2. It re-gates in gate 21 and then takes a turn after RD-819.
2. RD-640 (N): NOTHING on the class merges (the cap). File ONE ticket, High, on our account, for the residue: F-640-1 (key loop identity by the canonical path, not dev:ino, as the gate PROBED) + F-640-2 (the 256-link off-by-one) + the survivors M-walkErrPurges, M-dirErrIsEnd, M-strKeyOnly. Link it to RD-640 and cite the gate's evidence paths (matrix-A-head.jsonl, matrix-fixprobe.jsonl). Search the board first, and say what you searched.
3. N-640-1, RULED by Tuesday (the gate asked for a ruling on the class): file it as its OWN security ticket, Medium, on our account, not folded into RD-640. Title: anonymous /api/admin/erasure-status discloses the absolute outside path in the first-run window. It is pre-existing at M0 (P-6), so cite that. N files it.
4. RD-821 (O): keep the installed tool. FIX ROUND for F-821-1 (gap-0: a merge whose pid sorts below the gate's passes the gate). Tooling, tier 2 through code, round 1 of 2, gate 21. The evidence is the gate's f3-placement.txt.
5. N-821-1, RULED by Tuesday: the by-hand gate yield (ruling (i)) is RETIRED from gate 21 on. The gate measured it costing holds their place twice, and RD-821 r2 already files merges ahead of gates. This SUPERSEDES ruling (i) for gates from gate 21 on.
6. F-794-1 / F-794-2 / F-819-1 / N-801-1 / T5: named. Each owner puts them in the MERGED mail and on the ticket at the merge step. Nothing else.

NOT COVERED: deploy, demo, Partner Center, any head other than the gated one (except the two fix rounds above, which re-gate).
-- Tuesday
