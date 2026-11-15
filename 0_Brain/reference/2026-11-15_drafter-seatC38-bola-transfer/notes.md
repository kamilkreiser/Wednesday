# Drafter notes, Seat C 38th brief (KS-1703 transfer BOLA), 2026-11-15 23:1x

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-15_seatC38_bola_transfer.md (35288 bytes, STAMP blank).
Raw material: _work/ (KS-1703.txt, handler copies, callers_raw.txt, open_prs.tsv, pr_files.tsv, lin_read.py).

Pins: develop 61a3953e6d66 (2026-11-15T11:59:43Z), Q 1st's 025185e0a21e is 5 commits behind with none in the touched paths.
KS-1703: Backlog, priority 0, 5 comments, 7 ACs. Six AC/route facts in the brief.

Things the commission did not know (surfaced in the brief):
1. History door (/api/transfers/:id/history, in KS-1703's title) and /api/transfers/document/:documentId are unscoped too; the latter is already read as STRANGER by three KS-2081 cells that will change by design (R5, control R5, control P7).
2. Neither svc_transfers nor svc_transfer_delegations has a tenant column: "same-tenant admins" (W1 option b) is not buildable without a migration.
3. The service's own write rules refuse a non-party platform admin (transferAccess.ts:79); the commissioned read arm for platform admins is an asymmetry (W2).
4. No same-tenant consumer of any by-id GET exists in frontends, other services, gateway, Extranet or e2e; the issuer UI only lists with its own ownerId.
5. PRs 2231 and 2236 (C 37th's kyc work) are merged, so C 37th's NEXT STEP (KS-2189 + KS-2188 coupled kyc PR) is unblocked and competes for C 38th (W5).
6. Only PR 2170 (approvalWorkflowService.ts) and two dependabot PRs touch services/transfer; no overlap with the files to change.
7. Delegation /document and transfers /document have no 404 in their contract: the brief uses a filtered empty list byte-equal to an unknown document (D5).

Suite not run by the drafter (load1 7.5 to 8.1).

UNMEASURED
