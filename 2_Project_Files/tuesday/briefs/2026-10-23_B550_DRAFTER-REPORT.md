# B550 drafter report (Sonnet, read-only) - written 2026-10-23 22:4x AEDT

Brief: `2026-10-23_B550_SEAT-M5R_mps-103-fix-round-2.md` (123 lines, 8 stamp-slot lines; `.pre-stamp` beside it, cmp rc 0, sha256 77132a81de2dc04b39ea38379682d259f73325a1f5dbad403fffc7990ff73755 before any stamp). 0 non-ASCII bytes (checked). Shape cloned from B541.

## Facts measured (MEASURED-BY-DRAFTER, 22:1x-22:3x)
- ls-remote: b527 = refs/pull/103/head = bf7ad7a18b6fdc598c06ae59e3029d6674a53949; main = e3624f009879a2efe88d1491364451f54573c61f; PR #103 open, 11 files, mergeable_state read `clean` by the REST call at 22:15 (the gate saw `unknown` earlier; the seat re-reads).
- `rev-list --left-right --count e3624f00...bf7ad7a` = `2 6`; merge-base is c4aa4cc7; both objects present locally (`cat-file -t` commit).
- Open PRs: #103 and #102 (b518 @ c7365aee); #102 has 0 paths under web/. Panes: %0 tuesday, %1 fleet-monitor, %347 HPSM-POC-G67, %348 MPS-M2R. No M5 / M5R pane. No `.tools/b550` or `wt-b550-*`.
- Ports: `lsof` empty for 8800-8920. B549 (HPSM-POC gate) names 8880-8889, so 8890-8899 is the next free block.
- load1 10.05 10.79 10.15 at 22:15; `heavy-slot-2` held by another seat.
- Blob counts at bf7ad7a, each 1: `keys.push(next++)`, `const remove = (i: number) => {` (FleetGrid.tsx); `updateBomLineAt(draft, at, patch)`, `removeBomLineAt(draft, at)` (PurchaseBomEditor.tsx); the P6 method check and `r.sectionId === l.sectionId` (consolidatedBomModel.ts); `const CASES = 220;` (BomClassColumn.test.tsx). Control zzz string 0.
- Sonnet model id `claude-sonnet-5-5` from models_latest.json.

## Judgement calls the stamp should know about
1. **Focus rule (B546-6).** The ruling says restore a focus target after Remove. The builder's two existing rows (`removing the first of two lines numbered 1 ...still focused`, `removing the middle of three ...`) assert the focus stays in a later row's INPUT after a scripted click, and existing rows are never edited. A blanket "always move focus to a Remove button" would turn them red. The brief therefore constrains the fix: move focus only when it was inside the removed row (keyboard Enter or pointer click on its own Remove), leave it alone otherwise. This is my reading of the ruling, not Tuesday's words. Rule if you disagree.
2. **Empty grid.** When the last remaining row is removed, base left focus on the body too; the brief says build nothing for it and records it as a Note. Tuesday may want the Add line button focused instead (no new words), which would need its own row and mutant.
3. **H5** is included in B546-4 as the ruling's "H5 as the gate graded it" (gate: Minor if alone). Built as rows, no src change.
4. **E4 split** into E4a (set, :382) and E4b (Remove, :471) so each row has its own named killer for the cap round. P6 split into P6a-c, focus mutants FO1-FO4 added (FO4 is killed by the builder's existing rows).
5. **Finding 1 margin.** I set "at most 2500 ms in every one of five full-suite runs" (half the limit) and require the reduced row still kills M527-G, M527-Gu and the eight per-class drops with example rows masked. The gate measured 3.1-5.5 s full-suite at 220 cases; 2500 ms is my number, not the gate's.
6. **gitleaks** was NOT RUN by the gate; the brief makes the canary + scan mandatory so the round-2 gate does not inherit the conditional.
7. **Heavy-slot load rule** adds "re-read load1 before EACH job inside a held slot" (the builder's disclosed lapse, Correction 6 in B527 STATUS).
8. Timing suggestion: target READY 2.5 h, hard stop 4 h after launch (the mutant matrix is the long pole; the gate's own matrix ran 2.5 h under load1 up to 14).
9. Unverified: the gate's scratch kill rows were not read (forbidden tree), so row sketches are mine from the finding text; the seat proves each row against its mutant.

## Not done / fences kept
Only the three files above were written, plus one `cp`. No Artifact, Docs, mail, chat, decision_queue, scoreboard, staging, fetch/worktree/checkout/commit/push, no HTTP to app hosts, no npm/node/vitest/dotnet. `gh api -X GET` only; no Jira call made. No builds or mutants run.
