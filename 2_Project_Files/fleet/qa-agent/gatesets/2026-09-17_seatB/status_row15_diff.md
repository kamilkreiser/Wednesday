SUBJECT: [Secuura/Blockchain -> Wednesday] STATUS: row 15 cardano-sdk ip-address diff (Seat B)
AUTH: {"spf": "pass", "dkim": "pass", "dmarc": "pass"}

Seat B

BLUF
@cardano-sdk/core moved ip-address ^9.0.5 -> ^10.2.0 in 0.46.15 with NO runtime code change.
- Its only ip-address consumer, Serialization/Certificates/PoolParams/Relay/ipUtils.js, is byte-identical between 0.46.14 and 0.46.15, in both the cjs and esm builds.
- Upstream ships the same code against ip-address 9 and 10.
- That supports card `secuura-audit-row-ip-address-high-override` option (a): the override API surface our tree would exercise is the one upstream already runs on 10.x.

RECOMMENDATION
Carry to Kam as evidence for (a), labelled as a measurement of upstream's code, not of our issuer's behaviour. Nothing is built until he taps.

DETAIL
Instrument: `npm pack @cardano-sdk/core@0.46.14 @cardano-sdk/core@0.46.15 --ignore-scripts` in a bounded node:24-alpine container (rc 0, 2.2 s), extracted on the host into records. Nothing was installed into any tree.

1. package.json dependencies, 0.46.14 -> 0.46.15: ip-address ^9.0.5 -> ^10.2.0; @cardano-sdk/crypto ~0.4.6 -> ~0.4.7; @cardano-sdk/util ~0.17.1 -> ~0.17.2. No peer changes.
2. Files referencing "ip-address" (grep -rl over *.js/*.cjs/*.mjs/*.d.ts): 2 in each version, the cjs and esm builds of ipUtils.js.
   Control: @cardano-sdk/util appears in 244 files of 0.46.15. My first run of this grep read 0 because zsh expanded the unquoted --include glob. That control exposed it, and the rerun uses quoted globs.
3. `diff` of ipUtils.js 0.46.14 vs 0.46.15: rc 0 (identical) for both cjs and esm.
4. The ip-address API it uses:
   - Address4.isValid;
   - Address6.isValid;
   - new Address6(s).toUnsignedByteArray();
   - Address6.fromUnsignedByteArray(bytes).canonicalForm().
   The IPv4 path validates with Address4.isValid, then splits and parseInts itself, as decimal.
5. The only importer of ipUtils is SingleHostAddr.js (stake-pool relay certificates).
6. The whole cjs dist differs in exactly 9 files, all Cardano/Address/*.d.ts, their .d.ts.map files, and tsconfig.tsbuildinfo. 0 runtime .js files differ.

NOT measured
- Whether any issuer code path serialises pool relay certificates (i.e. whether our bundle reaches ipUtils at all).
- ip-address 10.x's own behaviour for these four calls. The evidence is upstream's choice, not a test of ours.

Records: 5_Project_History/2026-09-17_seatB-audit/row15/ (tarballs, extracted trees, ipUtils-*.diff, cjs-differing-files.txt).

Seat B
