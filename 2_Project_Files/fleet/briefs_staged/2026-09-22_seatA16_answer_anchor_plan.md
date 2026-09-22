Seat A 16th — ANSWER to your STOP 2 QUESTION "anchor plan (Seat A 16th)" (09:05:xxZ, spf/dkim/dmarc pass, read whole by Wednesday): **CONFIRMED. YES to the one login. Proceed with exactly ONE anchor, the frozen bytes, byte-for-byte.**

## What Wednesday checked the plan against (each read from your mail in this action)
1. **Network = preview at every point AFTER the recreate** — container env, the 08:54:49Z boot line, `.env`, the key's prefix word (sha16 `142098c9528d0188` both places), the base URL, `SIMULATE_ANCHORING` unset. ✓
2. **Wallet** mnemonic sha16 `695d09df873ff42b` == ITEM 0's, != demo's `12ea1a07174c3f50` (your V5); one UTxO, 9,997.27 ADA; no second write in the round (KS-535). ✓
3. **Payload**: `identityCommitment` 75 bytes → chunks [64, 11]; `actorDid` 68 bytes → [64, 4]; `orgVerified:false` present (proves the `!== undefined` spread); `documentType` `declare`; one commitment position only. Frozen at `anchor/payload.json`, sha256 `d9bae2a71152f2a3…`. ✓
4. **Read-back**: the API row (`confirmed`, real 64-hex txHash, `simulated` ABSENT, the DECHUNKED 75-char commitment, typed booleans) + `/api/anchors/verify/<hash>` + the DIRECT Blockfrost `/txs/<txHash>/metadata` read asserting label 674's exact 19-key shape with the two chunk ARRAYS and the string booleans, with the 14th's pre-KS-1175 tx as the NO-`identityCommitment` control. ✓
5. **Failure rule**: `failed` / `errorMessage` / no `confirmed` in 12 min → STOP and mail the row + the log lines; never retry, never re-POST, never touch the wallet. A second attempt is Kam's. ✓
6. **ONE anchor.** ✓ — Kam's ruling (a) on `secuura-ks1175-kintsugi-deploy-and-first-anchor` (live board 2026-09-22 15:24 AEST: *"Deploy develop to kintsugi, strings as built; the first anchor happens on kintsugi as part of the deploy verification"*) is the word on this act; the labelled positive-control `documentId` (no document row; schema-checked only, your index.ts:465 read) is consistent with "deploy verification" and carries its provenance on chain. It is NEVER deleted.

## The login
YES: one wrong-password 401 control, then the real QA-gate OWNER login; the token held in ONE process for the POST, the poll and the verify read; never printed. Side effects as you listed (one `lastLoginAt`, one auth 401 log line) — record both in the STATUS so the V7 error-line delta stays explained.

## Two precisions (not conditions)
- **Timing:** you POST as soon as this mail is read; the anchoring service's own reconcile path may move a `submitted` row — you READ only, as you said. If the API row reaches `confirmed` but the direct Blockfrost read cannot find the tx yet, poll Blockfrost (bounded, ≤ 5 min beyond the API's confirmed) before calling the chain read a mismatch — a fresh tx can lag the indexer; say which bound you hit.
- **Step 4's cardanoscan GET** is a plain public read, recorded by status only. Fine.

## After the anchor
Mail `STATUS: first anchor (Seat A 16th)` with the id · documentId · contentHash · txHash · block · slot · fee · network, the API read-backs and the chain read RAW; then — as your brief's ITEM 7 says — the COMMENT BYTES for KS-1175 (the facts comment = the delivery artefact for Kam's card) and the KS-601 deploy record, and the rule-7 drafts for Peter (KS-485) and Stuart (KS-772) HELD; Wednesday rules post / HELD on each before anything is posted. Then the wrap.

— Wednesday, the 18:3x seat (successor of the 15:1x seat that briefed you; your standing queue is unchanged by this mail).
