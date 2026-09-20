# READY — KS-1284-T13-ATTACHPOINT-1 (Ornith, briefed, test_only NEW FILE, vitest, anchoring) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1284-ornith35b-night3/out.md.checker/patch.diff`** (from `ls` at 02:38 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp`, Wednesday).

**Held 02:38 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402` (develop at the hold). Adds a NEW test file `ks1284-attach-point.test.ts` (43 lines) that runs the REAL `buildAnchorTransaction` in-process — `vi.mock('../cardano/provider')` (one lovelace UTxO), a CSL-generated ed25519 wallet, fabricated 12-field protocol params — and asserts the built tx's label 674/675 metadata carries the codec's output (a ≥65-byte string as chunks; a boolean as `"true"`). The #1105 gate's NOT-PINNED row T13-ATTACHPOINT: no test file imported `cardano/transaction.ts` before this. No network, no real key, nothing anchored. Refs KS-1284 (Refs KS-721); NEVER Closes.

**Source read (Wednesday, same action):** 43 `+` lines (`--- /dev/null`), all 43 byte-equal (ordered) to the brief; 0 `-`; one new file; patch BYTE-IDENTICAL to the golden. First sample, round 1.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** ATTACHPOINTRAW `transaction.ts:114` (the gate's: `JSON.stringify(metadataPayload)` without the codec) → reds `label674` AND `label675` (received `bools not allowed in metadata` — CSL rejects the boolean before the 90-byte string; the gate had predicted the string error — a finding for the gate's record, stated); From byte-matches the tip, count 1, control `toCardanoMetadatum` 2, checked by Wednesday; T8 restored by bytes. The helper catches the build throw so the red is an assertion. Controls: 1. 3/3 cells green at the tip (fee 175489, 906-hex cbor — drafter's measure).

**Checker:** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 (`runs/2026-09-21_wave3-drafter-precheck/`).

**Collision (drafter, 8 orders on a fresh clone; Wednesday re-derived the tamper lines and key sets):** NEW files collide with nothing by construction; the tamper files (`index.ts`, `transaction.ts`) are planted-and-restored. With the three held readback/identity READYs, every order applies rc 0 (held files `431b51cb378e933c` / `ee1cbe52ea87bc02` unchanged); whole anchoring with all six cells **329/328/1** (the 1 red = develop's own `threadTokenMint`, the gate's count). `grep night/READY_*` for `anchoring/src/index.ts`, `cardano/transaction.ts` and the three new names: 0. No live seat owns anchoring.

**For the raise seat:** strict apply (`--- /dev/null` new file); TEST-ONLY (STOP on any product byte); anchoring vitest at the tip 319 → with all SIX anchoring READYs 329 (+3 cells here across the three new files + 3 in the held two); tier 2 unless the gate says otherwise; **raise all six anchoring READYs as ONE PR** (readback pair first in the diff, then identity, then the three new files) — no sequencing needed.

---
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1284-attach-point.test.ts
@@ -0,0 +1,43 @@
+/**
+ * KS-1284 - the ONE attach point: buildAnchorTransaction runs the logical payload through toCardanoMetadatum before
+ * add_json_metadatum_with_schema (the #1105 gate's T13-ATTACHPOINT seam: no test imported cardano/transaction.ts, so
+ * the codec removed at that line left all 319 cells green while every >64-byte string and every boolean threw at
+ * tx build again - KS-721's original defect). Runs in-process: the provider is mocked (no Blockfrost, no network),
+ * the wallet is generated from CSL, and the protocol parameters are fabricated numbers a fee algorithm accepts.
+ * A throw at tx build is CAUGHT and returned as text so every red below is an assertion, never an uncaught error.
+ */
+import { describe, it, expect, vi } from 'vitest';
+import * as CSL from '@emurgo/cardano-serialization-lib-nodejs';
+vi.mock('../cardano/provider', () => ({
+  fetchUtxos: vi.fn(async () => [{ tx_hash: '0'.repeat(64), output_index: 0, amount: [{ unit: 'lovelace', quantity: '20000000' }] }]),
+}));
+import { buildAnchorTransaction } from '../cardano/transaction';
+const key = CSL.PrivateKey.generate_ed25519();
+const keyHash = key.to_public().hash();
+const wallet = { address: CSL.EnterpriseAddress.new(0, CSL.Credential.from_keyhash(keyHash)).to_address().to_bech32(), paymentKey: key, paymentKeyHash: keyHash, networkId: 0 };
+const params = { minFeeA: '44', minFeeB: '155381', poolDeposit: '500000000', keyDeposit: '2000000', maxValSize: 5000, maxTxSize: 16384, coinsPerUtxoByte: '4310', priceMem: 0.0577, priceStep: 0.0000721, collateralPercent: 150, maxCollateralInputs: 3, slot: 1000 };
+const COMMITMENT = 'identity-commitment-l2.v1:' + 'b'.repeat(64);
+async function anchored(label: number, secuura: object): Promise<any> {
+  try {
+    const built = await buildAnchorTransaction(wallet as any, params as any, label, { secuura });
+    const metadata = CSL.Transaction.from_hex(built.txCborHex).auxiliary_data()!.metadata()!.get(CSL.BigNum.from_str(String(label)))!;
+    return JSON.parse(CSL.decode_metadatum_to_json_str(metadata, CSL.MetadataJsonSchema.BasicConversions));
+  } catch (err: any) {
+    return { threw: String(err) };
+  }
+}
+function shape(anchoredPayload: any): unknown[] {
+  const commitment = anchoredPayload?.secuura?.identityCommitment;
+  return [Array.isArray(commitment), Array.isArray(commitment) ? commitment.join('') : anchoredPayload?.threw, anchoredPayload?.secuura?.actorVerified];
+}
+describe('KS-1284 buildAnchorTransaction encodes through the codec at the ONE attach point', () => {
+  it('RED KS-1284: a 90-byte identityCommitment and a boolean reach label 674 as chunks and the string "true", nothing throws', async () => {
+    expect(shape(await anchored(674, { hash: 'c'.repeat(64), identityCommitment: COMMITMENT, actorVerified: true }))).toEqual([true, COMMITMENT, 'true']);
+  });
+  it('RED KS-1284: the batch label 675 goes through the same attach point', async () => {
+    expect(shape(await anchored(675, { hash: 'c'.repeat(64), identityCommitment: COMMITMENT, actorVerified: true }))).toEqual([true, COMMITMENT, 'true']);
+  });
+  it('CONTROL: a payload that is already chain-legal (all-short, boolean-free) is anchored byte-identical under label 674', async () => {
+    expect(await anchored(674, { hash: 'c'.repeat(64), version: '1.0' })).toEqual({ secuura: { hash: 'c'.repeat(64), version: '1.0' } });
+  });
+});
