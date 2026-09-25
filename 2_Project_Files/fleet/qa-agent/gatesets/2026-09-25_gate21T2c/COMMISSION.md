# COMMISSION — DRAFT the round-21 THIRD TIER-2 batch QA gate kit ("gate21T2c") — do NOT launch

Relayed by Wednesday to the drafter on 2026-09-25 (~16:1x AEST), WIDENED mid-draft (~16:3x AEST: "INCLUDE #1223 KS-1118 ROUND 2 in gate21T2c (it now
makes eight; freeze there)"). Recorded here as the gate's commission; the QA agent reads it. Shape copied from the launched sibling tier-1 kit
`gatesets/2026-09-25_gate21T1b/` (base-invariant against a MOVED develop; pinned to the current develop; file NAMES checked per PR; the `mergeable`
refusal) with the tier-2 content of `gatesets/2026-09-25_gate21T2/`, BRIEF_TEMPLATE.md and QA_AGENT_CHARTER.md.

## The batch — ONE gate, EIGHT PRs (FROZEN at eight)
Heads as read by Wednesday with `ls-remote` at 16:0x / 16:3x AEST; the drafter re-read every one (lsremote_1.out, lsremote_2.out, predict_4.out).
TIER 2 (through-code; red proof RED at base / GREEN at head in the tester's own clone):
- #1218 KS-897 + KS-896 ROUND 2, head d971aa4f24665bb192765a0c6e82f719996efb92 (Seat L4). Round 1 NO GO (report
  `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-25-batch1215-t2-r1/report.md`, section "#1218"): FIXTURE-LASTCMD +
  FIXTURE-GITENV. The gate must re-run the round-1 T897b mid-build failure (-> rc 2 + a line STARTING `FIXTURE BUILD FAILED` + 0 cells) and the
  cwd-inside-a-scratch-repo case (-> rc 2 AND that repo's HEAD/refs/config byte-identical), and run it from a cwd OUTSIDE any git repo with any scratch
  repo's origin pointed at a local bare repo or `no-push://`, never a real remote. Round 2 of 2 under the cap. After this merges the suite's count
  changes; record the new pass count for the fleet STOP rule.
- #1223 KS-1118 ROUND 2, head 2892e528630d93a5b1b1482efa6978edce4211f1 (Seat L1; widened in). Round 1 NO GO for PRECEDENCE-DUP (same report, "#1223
  KS-1118"). The fix drops the P3 cell, so the net diff vs develop should be `services/originate/src/routes/verification.ts` comment-only (F-3a). The gate
  must: (1) confirm the net diff is exactly that one file and AST-equivalent (comment-only, with controls, as round 1 did); (2) re-run T5 over the WHOLE
  originate suite and confirm #1149's two cells are the only reds (2 failed / 861); (3) check the squash body carries the legs line. Round 2 of 2.
- #1233 KS-1133, head 6892124d9304ae014c52f7ea08a17e9468d411bf (Seat L1; openapi descriptions; its READY: `check:openapi` rc 0, 405 example blocks,
  yaml diff exactly its 4 descriptions). Spec surface -> legs 3/4/8 OWED unless a stack is up; if Docker is up the gate MAY bring the stack once (the
  tier-1 gate batch1224 may be using a slot — use a FREE slot, never touch another gate's stack).
- #1235 KS-1140 GF-1, head 1c899947ea31e7a6628f5256174c1c353e6587af (Seat B 25th; an Ornith local-model PASS held as READY).
- #1236 KS-1110 A+B, head 4296ba6d090c212d0849f488f882d00a2985245e (Seat B 25th; an Ornith PASS; two commits; its READY says it ran no Blockchain/Dev
  leg by path filter).
- #1237 KS-1229, head cfa16eb70ba28c5833101e39e4e1cb1680b8dd6c (Seat L1; the guard shape at three sites; red-proof tampering only `/version` -> QVT1-3
  red, controls green).
TIER 3 (hygiene: confirm comment-only / no behaviour by AST-equivalence with controls, no red proof):
- #1219 KS-1277, head 5d5129a03af0bf1586c26403a453ce283ae0be2f (Seat L1; comment-only per the gate queue; head read by the drafter).
- #1238 KS-1158, head 0f3ffbb0947a82b7ec1c2866fd1a82ff4c94b2c1 (Seat L1; stale header lines; its READY's record correction — four of five header
  citations wrong at d4cf7e3cf — verified against the file at head).
Develop at commissioning: 379c6eb1d45905f398fae67ee7dd2f46ad40432f. It MOVED during drafting: #1221 KS-1266 squashed as 9e744421a (06:35:59Z) — the
file #1237 edits (README section 6, item 1). Measure merge-bases, behind counts, pairwise path-disjointness across all eight and against develop's new
commits; base-invariant merge checks.

## Gate-specific rules the brief must carry (Wednesday's, in substance)
1. Per-PR GO / NO GO / GO WITH FINDINGS, findings-only; worktrees from refs/pull/<n>/head, never write the shared checkout.
2. Anchoring wording if anchoring runs; KS-1155 load false-red (re-run once; assertion failures are real).
3. Reap only the gate's own `login_stub.mjs` (cwd + ppid, never by name, never pid 1).
4. NO standalone run of `pre_push_hook_base.test.sh` or `run-shell-suites.sh` except #1218's required cells run as specified above.
5. HOLDS: no merge, push, ticket/PR write, deploy.
6. The GO string: `GO: merge #1218, #1219, #1223, #1233, #1235, #1236, #1237, #1238 batch` (adjusted for #1223 joining).
7. Routing `QA/Secuura-batch1218`; the PROPOSED line `QA/Secuura-batch1218|coagent@agentmail.to|yes` — NOT written by the drafter.

## Deliver (do NOT launch, send, tap, commit or push)
The prompt, the launcher (`bash -n` clean), the gate set contents per the precedent, controls run both ways, a `--dry-run` of the repin script, a
PROPOSED inbox_routing line, and a README.
