# B287 drafter report (2026-10-19 ~18:25 AEDT)

Brief: `2026-10-19_B287_SEAT-R1_composer-demo-minio-read-and-fix-draft.md` (3 slots: STAMP_TIME, B_NUMBER_CONFIRM, PORT_BLOCK; propose PORT_BLOCK = none). Shape copied from B278 SEAT-W2.

## Access route found (copied exactly)
`az vm run-command invoke -g HPSM-DEV-RG -n hpsm-demo-vm --command-id RunShellScript` with the project's `AZURE_CONFIG_DIR` (= `<project>/4_Credentials/.azure`, exists). Identity check: `az account show` must show kreiser.org@me.com, tenant d500ebad-..., sub 0c57ab37-... (B155 STATUS :55, route :97; read-only script shape `B155_evidence/step2_read_r2.sh`). No SSH/NSG route exists; the brief forbids inventing one.

## Measured at drafting (read-only, nothing sent to any host)
- Root main = b57b607114cc... (B278's local fold); last C-entry is C-78 so new ones are C-79, C-80; highest BACKLOG id 318 so new row = 319 expected.
- BACKLOG: no row on the demo overlay (0 hits "overlay", 0 "compose.demo"; "minio" only in unrelated #84). Brief tells the seat to grep again and append instead if one appears.
- Branch `b285/ci-timing-tests-b281-1` exists (B285 live); brief fences it and `.tools/b285*`.
- Both cards ruled in the store: overlay card b at 18:20:47 (board time you quoted 18:19:50), terms card a at 18:20:50 (you quoted 18:20:01). Brief tells the seat to quote both and not reconcile.
- No mail key (count 0). Load 8.69.

## Judgement calls for Tuesday
1. `az vm run-command` itself leaves script/output files in the VM agent directory (B155 :94). That is the copied route; flagged as R-R1-1 for you to accept.
2. Plain `docker compose config` would print interpolated secrets, so the brief allows only `config --images`, plus an on-box redaction filter with a planted-canary test, and a self-check (overlay sha256 printed first and last).
3. If the VM image has no RepoDigest (tarball-loaded) the seat STOPs with one question rather than pin by id.
4. Records go on branch `records/b287` (not main) for you to fold; C-80 is written as settling B278's recommendation for local/CI only, not the demo.
5. The drafted pin is a one-line diff plus apply/rollback "DRAFT, NOT RUN" (in-place edit, never mv, no restart), and the deploy card text defaults to hold.

Nothing run against the VM, no mail, no chat, no git writes, no decision_queue verb except `show`.
