# COMMISSION — DRAFT the round-20 TIER-1 QA gate set for Seat B 21st/22nd (PRs 3, 6, 7, 8, 9, 10) — do NOT launch

Written by Wednesday (the 17:0x seat of 2026-09-23). **Copy the shape, discipline and file set of
`../2026-09-23_gate20T2_seatB/` exactly** (read its COMMISSION.md, README.md, `gen_launcher_gate20T2.py`, `repin_and_launch_gate20T2.sh`,
`launcher_controls_gate20T2.sh`, `prompt_gate20T2.DRAFT.txt`, and `2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md` + the charter
beside it) — changing only what this file says. Its gate ran clean (verdict 07:35:15Z) — that set is the proven template.

## Authority
Kam, live board 2026-09-23 14:24:05: *"I sign those to the Claude agent then, and after you do merge, push, and deploy what
you can."* The 90% usage cut is lifted for THIS lane only (0_Brain/tasks/EXPIRING-GRANTS.md row) — the gate is part of it.

## The batch — TIER 1 (full weight: product/guard surfaces), ONE gate (2026-09-18 minimise-duplication rule)
From the READY mails in wednesday-agent@agentmail.to (Seat B 21st for #1204/#1207/#1208; Seat B 22nd for #1209/#1210/#1211) —
read every READY WHOLE and every PR at source:
- PR 3 #1204 — KS-851 QUOTEDNAME, test_only + script tamper (kyc)
- PR 6 #1208 — KS-1287 PATHREQUIRED, code_patch (vc-issuer) — **THREE files**: the regenerated `docs/openapi/secuura-api.yaml` rides
  on Wednesday's 06:52Z ruling (a) (repo preflight leg 1, spec drift). The gate verifies the YAML is exactly what `npm run
  generate-openapi` produces from the head.
- PR 7 #1207 — KS-1245 DEGRADEDWARN, bash_patch (Kam's ruling `a`)
- PR 8 #1209 — KS-1033 MISSINGBASE, bash_patch — a fail-closed DESIGN change (unresolvable base exits 2, was exit 0); the gate
  checks the body says so and that its push-path reach is NONE as the READY claims
- PR 9 #1210 — KS-1239 RAWAUTHDEAD, code_patch, a pure product removal (api-gateway); the ruled dangling-comment FINDING must be
  in the body as stated, nothing fixed or filed
- PR 10 #1211 — KS-1084 SIGTENANT + TPVTENANT, code_patch, TWO stages on ONE product file (`proxy.ts`), the P0; the cross-tenant
  effect is NOT measured and the body must say so; Part B (`/api/batch`) OUT. The raise engine's per-file cumulative-count fix
  (Wednesday's ruling (a) 07:5xZ) is the seat's tooling, not the product — note it, do not grade it.
Seat B 22nd's measured tier-1 sub-tree over develop 2bc5ccf63: `655c450d8f3eee7a45db23ad8c9ebd317314e4b4` (13 files, +498/-25,
three orders). Expected GO string: `GO: merge #1204, #1207, #1208, #1209, #1210, #1211 batch`.

## 🔴 THE BASE WILL HAVE MOVED
Tier 2 (#1202/#1203/#1205/#1206) is being merged NOW on Wednesday's GO. The launch script must READ develop at launch and grade
every PR's merged tree and the chained END_TREE over THAT develop (the tier-2 gate asserted tier1 ∩ tier2 paths = EMPTY — re-assert
it). 0 bytes under `services/auth/` across all 13 paths — assert it. Pin develop and each head by READING them at launch
(`ls-remote` + refs/pull/N/head) in the same action — never from a mail.

## Deliver (do NOT launch, send, tap, commit or push)
The gate set files in THIS directory, a `repin_and_launch_gate20T1.sh` + generated launcher that REFUSE to start unless they
re-read the six heads and develop at launch, the launcher controls run (a stale head must refuse), and your report as TEXT in
your final message (the harness refuses report files from subagents). Opus 5.5 by the configured default (no `--model` pin).
Never `cd`; no `timeout`; never discard stderr; read verbs only in the Secuura checkout; Secuura content only.
