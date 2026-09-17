SUBJECT: [Secuura/Blockchain -> Wednesday] MERGED: #1028 KS-744 @0a2b1603fe52f0f3b8152588af78bbeab0237be7; F-1 KS-1221, N-2 KS-1222, N-3 KS-1223, N-1 on KS-1208
TS: 2026-09-17T11:55:50.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
**MERGED #1028 (KS-744) on your GO (11:48:22Z): squash `0a2b1603fe52f0f3b8152588af78bbeab0237be7`, merged_at 11:50:57Z.**
- Verified at origin. Develop = the squash; its parent `75ad0e55c` is the pre-merge develop; its tree `557aa4de89bcd53e01b3916d2a46986e36dd4e65` equals your prediction.
- All three blob targets are equal: `auth.ts` 6e1668362, the ks744 test 2ed41a338, the ks1207 test f56bd48b9.
- KS-744 stays In Progress. The facts comment, the KS-1208 N-1 comment and three new tickets are posted: **F-1 → KS-1221** (test-only, for the local model), **N-2 → KS-1222**, **N-3 → KS-1223**.
The slot is free. Next: KS-1194 into it (merge develop in again, re-run, push, READY). The KS-1215 step (a) run has finished; its analysis comes in its own mail before any cell is written.

## Recommendation
1. Route **KS-1221** to the local model (test-only; it is the gate's G-UNDEFONLY row).
2. No other action needed on this receipt.

## Detail
- **Pre-step** (`merges/merge-1028.prestep.out`), then the same script with `--do-merge` (`merges/merge-1028.out`):
  - ls-remote: develop 75ad0e55c, pull/1028 e39521cfb (= GO); develop unmoved since the gate.
  - PR open at the GO head, mergeable true (state unstable).
  - merge-tree rc 0, predicted `557aa4de8` = the GO's.
  - Predicted blobs: auth.ts 6e1668362 OK, ks744 2ed41a338 OK, ks1207 f56bd48b9 OK.
  - Predicted api-gateway subtree 0b77c0a24 = the head's (= the GO's 0b77c0a24). develop→predicted files: `auth.ts` and the ks744 test only.
  - attachmentsForURL(pull/1028) = [KS-744 contributes In Progress]. Closing-phrase scan: 0 hits over 7 texts; the control fires on "Closes KS-1".
  - Merge PUT with sha pin e39521cfb: http 200 merged true.
- **At origin after the merge:**
  - develop = 0a2b1603f (== squash); parent 75ad0e55c (== pre-merge develop); tree 557aa4de8 (== predicted).
  - Merged blobs: auth.ts, ks744 and ks1207 all OK.
  - The merged api-gateway subtree 0b77c0a24 == the head's.
- **Suite count on the merged tree:** 57 files / 555 tests, carried from the gate. Not re-run by me: per your GO, a re-measure applies only if the merged api-gateway subtree differs from the head's, and it is byte-identical.
- **Squash message:** `merges/squash-1028-body.txt` (Refs KS-744; no closing verb; Claude co-author line). Title = the PR title + " (#1028)".
- **Linear after the merge** (re-read 11:55Z): KS-744 In Progress, attachmentsForURL(pull/1028) = KS-744 contributes In Progress.
  - **KS-744 facts comment `71474b10-6485-4396-94c3-1b736b60e507`**, carrying the gate's records: the generic 500 with no leak in any mode; the falsy drop; the non-string coercion; the email guard resting on the edge strip (ks1041); the 500 specific to http-proxy mounts; the client level on non-verified optional paths; KS-1208 residue. Readback 6/6 anchors. I first wrote the merge time as "~11:52Z" and corrected it with commentUpdate to "11:50:57Z" (readback confirmed).
  - **N-1 on KS-1208: comment `5eec75a6-393b-4f9e-a0be-64033ebfcaf4`** (U+0142 email / U+0142 or CR-LF level → generic 500, 0 hits, every http-proxy mount and mode, identical on all three trees; `auth.ts:393` / `:398` guard presence only). Readback 3/3.
  - **KS-1221** (F-1, Low, Backlog, related KS-744): add ks744 cells for a verificationLevel of '' and null asserting no forwarded header; G-UNDEFONLY must red them.
  - **KS-1222** (N-2, Medium provisional, Backlog, related KS-744): `proxy.ts:551-620` upload screen unreachable, 415 with a multipart body / 405 empty; severity and the alternative upload path unmeasured.
  - **KS-1223** (N-3, Medium provisional, Backlog, related KS-744): client x-wallet-address forwarded; `referrals.ts:51-55` fallback under the "spoofable" comment; `verification.ts:1286` hand-forwards it; the referral mount unprobed.
- **Board search before filing** (`tickets/search-1028-findings.txt`; literal matches, archived included):
  - `falsy` 15 (none on gateway claim headers);
  - `x-verification-level` 2 (KS-744, KS-742);
  - `U+0142` 0; `ERR_HTTP_INVALID_HEADER` 3 (KS-744, KS-1208, KS-742); `legal header value` 0;
  - `documents/upload` 2 (PS-449, PS-424, archived Platform S); `BLOCKED_EXTENSIONS` 0; `UNSUPPORTED_MEDIA_TYPE` 3 (KS-663, KS-439, KS-781);
  - `x-wallet-address` 0; `referrals.ts` 1 (KS-202).
  - No duplicates. KS-439 is archived, so it is named in KS-1222 without a relation.
- **KS-1215 step (a):** the BASE / O1 / O3 run over three probes finished (rc 0 each, restored by blob sha, porcelain 0; records `ks1215/out-a/`). I have not analysed it yet; it gets its own mail before any cell is written.

