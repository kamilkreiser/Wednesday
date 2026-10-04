# gateD2 COMMISSION — ONE Secuura PR: KS-1404 (T1, round 1); author and merger Seat D 3rd

Drafted 2026-10-05 AEST (work 2026-10-04 14:2xZ – 15:0xZ UTC). PR number and FINAL head are INPUTS: `repin_and_launch_gateD2.sh <PR> <HEAD>` pins them at launch from the PULLS API and `ls-remote`. Nothing below is a pin.

## The PR
| field | value | source |
|---|---|---|
| PR | not raised at drafting (census 14:3xZ: no open PR on the branch) | gh_census_ex1.out |
| title | `KS-1404: real RFC 3161 verification, node-forge out of timestamping` | commit 9884b5588d7c |
| commits | **2**: 9884b5588d7c (12 paths, pushed to the branch at drafting) + a SECOND commit (Wednesday 14:2xZ) adding `services/timestamping/config/tsa-trust-anchors.crt` + `config/README.md` and correcting three code comments. Pin the FINAL head. | Wednesday's messages |
| branch | `feature/ks-1404-rfc3161-real-verification-d3-1` (rule: exact) | ls-remote 14:3xZ |
| base | kit base `e6daa806e79a` (the builder's). **develop has ALREADY MOVED** to `2d85b84e1012` (#1374 KS-1402 squash, tree 082190611d1f = gate54a's END_TREE). The launch refuses rc 10 until `repin_base_gateD2.py --new-develop <sha> --write` (README §7) and the builder has rebased. | ls-remote; repin_base_1374_ex1.out |
| files | 14 (kit.json `files`) | kit.json |
| tier | T1 security | Wednesday |
| pane | `QA/Secuura-ks1404-<PR>` | kit.json |
| report dir | `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-10-05-ks1404-<PR>-gD2/` | kit.json |
| GO string | `GO (Seat D 3rd): merge <n> on gateD2` | Wednesday |
| verdict mail | FROM coagent@agentmail.to TO wednesday-agent@agentmail.to, subject `[QA -> Wednesday] GATED2 #<n> (Seat D3 author and merger; T1 security: real RFC 3161 verification, node-forge out of timestamping, KS-1404)` | kit.json |
| authority | Kam: `secuura-tsa-accepts-unsigned-tokens-1004`=a, `secuura-freeze5-high-no-fix-1004`=b, `secuura-ks1404-tsa-trust-and-library-1004`=a | brief |
| previous round | gate54f report, sha256 `55e0bc148a59…` | kit.json |

## Rulings (each is a check)
Wednesday: mock tokens verify only via the DB-row branch (C3 PF3/PF3b, mock probe; C4 V12/V13); BER indefinite refused (cell 11 indefiniteLength / 11f; V10; mutation `indef`); isQualified dropped (V11); fail closed on empty/unset anchors (PF4/PF4b, cell 7, V8, mutation `anchors`); request bytes byte-identical to forge, quirks pinned (cell 16 + the 72-case base-vs-head differential, V17); the bundle is a `.crt` because preflight leg 9 refuses a tracked `.pem` (C1 P9 + leg 9 in C2 legs); no `.gitignore` negation (C1 P9).

## Checks
- **C1** `c1_pin_gateD2.py`: P1–P9 (two-commit shape, 14-path gate with PR 0 must-hit, trailers on both commits, keys, PR 0 locks absent, modes, credential / .gitignore).
- **C2** `c2_lockdiff_gateD2.py`, `c2_integrity_gateD2.py`, `c2_baseline_gateD2.py`, `c2_legs_gateD2.sh` (legs 2/6/7/9; the CLEANUP must-hit).
- **C3** `c3_cells_gateD2.sh` (+ parser, mutation planter, three probes, OpenSSL PKI, request-bytes judge).
- **C4** `c4_security_gateD2.py --fetch-anchors` (V1–V17, the bundle's two fingerprints recomputed from the providers).
- **C5** `c5_docs_gateD2.py --measured …` (§4, figures re-measured, keep-both, response shape).
- **C6** `c6_notcovered_gateD2.py --body-file …` (the nine items).
- **Census** `gh_census_gateD2.py`. Findings only.

## GO
Subject `GO (Seat D 3rd): merge <n> on gateD2`, else NO GO with its blockers. END_TREE is the FINAL head's tree, valid while develop == the re-pinned base.
