# KS-1175 EXPLORERBASE-PER-NETWORK-1 PIN THAT buildVerifyResponse's cardanoScanUrl HAS NO SUBDOMAIN ON mainnet AND IS PREFIXED WITH THE NETWORK NAME ON EVERY OTHER NETWORK — the explorer base the #1105 gate measured by call and found unpinned for mainnet — Wednesday's task for Ornith, TEST_ONLY, **ONE existing test file, one hunk, one cell added, no product file** (written 01:51 on 2026-09-21, #1105 gate NOT-PINNED row EXPLORERBASE-PER-NETWORK)

File: `Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts`
Tip: `cbae988dbe90ebe556459ada2cb437eaf80e2402`
Runner: `vitest`

Written from develop `cbae988dbe90ebe556459ada2cb437eaf80e2402` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 01:51 on 2026-09-21, read verbs only; the #1105 squash-merge of KS-1175 + KS-1284, the commit that CREATED every file named here). The test file at that tip is **121 lines**, read whole; its full content is in `files[...]` of your input. The product the cell pins is `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (**130 lines**, read whole): `buildVerifyResponse` at `:68-130`, its FIRST statement **`const explorerBase = ctx.network === 'mainnet'` at `:74`**, the mainnet arm **`? 'https://cardanoscan.io/transaction'` at `:75`**, the other arm `` : `https://${ctx.network}.cardanoscan.io/transaction` `` at `:76`, `txHash` at `:85` (a `tx_sim_`/`mock_tx_`/`tx_` placeholder becomes `null`, KS-522), and `cardanoScanUrl: txHash ? `${explorerBase}/${txHash}` : null` at `:102`. This service runs **VITEST** (`package.json` `"test": "vitest run"`, `vitest ^4.1.9`, `vitest.config.ts` present, no jest).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the test file above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above). You never touch `anchorReadback.ts` or any other product file: the behaviour is already what it is at the tip, and this cell PINS it.

## What the cell pins (one paragraph)

KS-1175 extracted GET /api/anchors/verify/:hash's response builder out of `index.ts` into `anchorReadback.ts` so it can be tested without booting the service. Its first statement picks the explorer base by network: `mainnet` gets the bare `https://cardanoscan.io/transaction`, every other network gets `https://<network>.cardanoscan.io/transaction` (`:74-76`), and `cardanoScanUrl` is `<base>/<txHash>` (`:102`). The #1105 gate measured this by call (mainnet and preview URLs) and found the MAINNET arm unpinned: at the tip the ONLY cell that names a cardanoscan URL is the `CONTROL:` cell at `:113`, which asserts the PREVIEW URL (`grep -c -i cardanoscan` over the test file: 2 lines, `:113` the URL and `:119` a `toBeNull`; the gate's row said "none names cardanoscan" — that was its grep slip, the preview half IS pinned by `:113`). So the two ways this could silently loosen are unpinned or half-pinned: the branch inverted (`!==` — mainnet gets `https://mainnet.cardanoscan.io/...`, which does not exist, and preview gets the bare host; `:113` catches the preview half only), or the mainnet arm "normalised" to carry a subdomain (`https://mainnet.cardanoscan.io/...` — no existing cell reaches the mainnet arm at all). This change adds ONE cell directly above the `CONTROL:` cell in the `describe('buildVerifyResponse — GET /api/anchors/verify/:hash (R9)', ...)` block that calls `buildVerifyResponse('db', {}, { transaction_hash: tx }, { hash: HASH, network: n })` for `mainnet`, `preview` and `preprod` and asserts the three `cardanoScanUrl` strings in one array: `[https://cardanoscan.io/transaction/<tx>, https://preview.cardanoscan.io/transaction/<tx>, https://preprod.cardanoscan.io/transaction/<tx>]`. Every existing cell is unchanged. **It pins TODAY's explorer base for mainnet and for the two testnets in one cell.**

## The exact change — ONE hunk in the test file

The new cell goes directly above the LAST cell of the `describe('buildVerifyResponse — GET /api/anchors/verify/:hash (R9)', ...)` block (`:107`, `  it('CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction', () => {`, the ONE trailing context line — it occurs exactly once in the file). There is NO leading context: the line above (`:106`, a blank line — which is why it is not your anchor) stays and is not written. Copy every line byte for byte. Every `+` line is ASCII only. There is no blank line anywhere in the fence. Keep the header exactly as shown. **Your diff MUST begin with the two file-header lines, above the `@@` line: `--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts` then `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts`.**

```
@@ -107,1 +107,6 @@
+  it('RED KS-1175: cardanoScanUrl: mainnet has no subdomain, every other network is prefixed with its own name', () => {
+    const tx = 'h'.repeat(64);
+    const urls = ['mainnet', 'preview', 'preprod'].map((n) => buildVerifyResponse('db', {}, { transaction_hash: tx }, { hash: HASH, network: n }).cardanoScanUrl);
+    expect(urls).toEqual(['https://cardanoscan.io/transaction/' + tx, 'https://preview.cardanoscan.io/transaction/' + tx, 'https://preprod.cardanoscan.io/transaction/' + tx]);
+  });
   it('CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction', () => {
```

`describe`, `it` and `expect` are already imported by the file at `:14`, `buildVerifyResponse` at `:16`, and `HASH` is the file's own constant at `:19` — you add NO import and NO helper. The cell needs no app boot, no port, no chain and no database: `buildVerifyResponse` is a pure function called exactly as `:81`, `:95`, `:102-104`, `:108` and `:116` already call it (`:116` is the same `row`-override idiom, with `transaction_hash` on the row).

## Cells

- `explorer` = `RED KS-1175: cardanoScanUrl: mainnet has no subdomain, every other network is prefixed with its own name`

## Red cells

The cell below is a GENUINE assertion-red: it fails under each tamper and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only.

- RED KS-1175: cardanoScanUrl: mainnet has no subdomain, every other network is prefixed with its own name

## Tampers

Two single-line tampers on consecutive lines of `anchorReadback.ts` (`:74` and `:75`; each occurs EXACTLY ONCE in the file — counted with `grep -c -F -x`, 1 and 1; positive control `grep -c -i cardanoscan` over the same file is 3: `:75`, `:76` and `:102`). They are the two shapes a loosening can take: the branch INVERTED (the gate's named tamper — mainnet gets a `mainnet.` subdomain that does not exist and every testnet gets the bare host), or the mainnet arm given a subdomain (a "consistency" edit that breaks only mainnet, which no existing cell reaches). Each `From` is the tip's line at that number, byte for byte, and each `To` is valid TypeScript (a boolean expression either way; a string literal either way), so nothing fails to load and no cell reds for the wrong reason. The checker plants them ONE AT A TIME and restores the file by bytes between them. The first tamper ALSO reds the file's existing `CONTROL:` cell (`:113` asserts the preview URL, which the inversion turns into the bare host) — that cell is declared in its Reds and is NOT a control of this brief.

### NETWORKINVERTED — the mainnet test is inverted (mainnet gets a subdomain, every testnet gets the bare host)
File: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts`
Line: 74
From:
```
  const explorerBase = ctx.network === 'mainnet'
```
To:
```
  const explorerBase = ctx.network !== 'mainnet'
```
Reds: `explorer`, `CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction`

### MAINNETPREFIXED — the mainnet arm carries a subdomain that does not exist
File: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts`
Line: 75
From:
```
    ? 'https://cardanoscan.io/transaction'
```
To:
```
    ? 'https://mainnet.cardanoscan.io/transaction'
```
Reds: `explorer`

## Controls

- `db source: metadata.identity beside metadata.identityCommitment, from the logical payload`
- `chain source: the same object from a chunked chain payload once the reader has joined it`
- `an anchor that predates the field reads identity: null and identityCommitment: null (both sources)`

*(All three are FULL `it(...)` titles, copied byte for byte from the file at the tip — `:80`, `:88` and `:101` before and after this hunk (the hunk inserts BELOW all three) — each occurs exactly once in the file and none is a prefix of any other title. For a VITEST suite the checker matches a declared cell by its FULL title, never by a prefix. The 6 `anchorIdentityView` cells (`:52-76`) are also green under both tampers but are left undeclared; the `CONTROL:` cell at `:107` is RED under NETWORKINVERTED and is declared there, never here. The three controls prove the db source, the chain source and the null path of the same builder still hold beside the new cell — none of them reads `cardanoScanUrl`.)*

## THE CELLS — state it to yourself before you write a line

At the untouched tip the new cell passes: for each network `:74` compares `ctx.network` with `'mainnet'`; `mainnet` takes the `:75` arm (`https://cardanoscan.io/transaction`), `preview` and `preprod` take the `:76` template (`https://preview.cardanoscan.io/transaction`, `https://preprod.cardanoscan.io/transaction`); `rawTxHash` (`:78`) is the row's `transaction_hash` = 64 `h`s, which matches none of the KS-522 placeholder prefixes (`:84`), so `txHash` is the hash and `:102` returns `<base>/<tx>`. The asserted array is the three URLs, and `toEqual` holds string for string (measured: exactly those three strings).

Under **NETWORKINVERTED** `:74` is true for the two testnets and false for mainnet, so the array reads `[https://mainnet.cardanoscan.io/..., https://cardanoscan.io/..., https://cardanoscan.io/...]` — assertion red on all three slots; the existing `CONTROL:` cell at `:113` also reds (`https://cardanoscan.io/transaction/fff…` vs the expected preview URL — assertion, not a load error). Under **MAINNETPREFIXED** only the first slot changes (`https://mainnet.cardanoscan.io/transaction/<tx>`) — assertion red; `:113` stays green because preview takes the untouched `:76` arm. Under BOTH, every declared control stays green: `:80`, `:88` and `:101` never read `cardanoScanUrl`.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From lines.** `anchorReadback.ts` at `cbae988db`, line 74 is `  const explorerBase = ctx.network === 'mainnet'` (2-space indent) and line 75 is `    ? 'https://cardanoscan.io/transaction'` (4-space indent), byte for byte; each occurs **exactly once** in the file (`grep -c -F -x`, 1 and 1). The checker plants and restores them one tamper at a time (T8 by sha256 after each; tip blob id `f49ffb6afaa…`).
- **Premise: the gate's claim, re-derived.** The #1105 gate's NOT-PINNED row says "no cell asserts either URL string (grep of the 10 R9 cells: none names cardanoscan)". Re-read at the tip: `grep -c -i cardanoscan` over the test file is **2** — `:113` (`expect(body.cardanoScanUrl).toBe(`https://preview.cardanoscan.io/transaction/${'f'.repeat(64)}`)`, inside the `CONTROL:` cell) and `:119` (`expect(sim.cardanoScanUrl).toBeNull()`). So the PREVIEW URL is pinned by `:113` and the gate's "none" is a slip; the MAINNET arm (`:75`) is reached by no cell (measured: MAINNETPREFIXED reds 0 existing cells). The gate's own tamper (`===` → `!==`) reds the `:113` control as well as the new cell — declared honestly above.
- **Premise: the anchor.** The test file is **121** lines; `:107` is `  it('CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction', () => {` (2-space indent, occurs exactly once in the file) and `:106` is blank. The trailing context line is non-blank and unique, and the insertion is pure, so no blank line is asked of you anywhere.
- **Premise: `+` lines that also occur at the tip.** One, added by this brief (so T4 accepts it): `  });` (`:54` and others — unavoidable for a new cell). Every other `+` line is new to the file. No `-` line anywhere, so nothing of the tip is removed.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No template literal** in any `+` line (no backtick — the URLs are built with `+`, unlike `:113`, which uses a template). The title uses `:` and `,`, no em dash.
- **Premise: the runner.** `anchoring/package.json` at the tip has `"test": "vitest run"` and `vitest ^4.1.9` in devDependencies, with no `jest` / `ts-jest`; `vitest.config.ts` includes `src/__tests__/**/*.test.ts` — the builder auto-detects vitest and the `Runner:` line above agrees with it. `tsconfig.json` excludes `src/__tests__`, so no gate runs tsc on this cell.
- **Premise: no live-lane collision.** `services/anchoring/**` was the #1105 builder's lane; #1105 is MERGED at this tip (`cbae988db` is the squash), so the lane's PR is closed — Wednesday confirms no other live seat owns anchoring before queueing. Held `READY_*` files whose diffs touch `services/anchoring/`: **2** (`READY_KS-1171-8j` — a NEW test file; `READY_KS-1172-B3` — `anchorSchema.ts` + `anchorSchema.test.ts`); READYs or briefs naming `anchorReadback` or `ks1175-anchor-readback`: **0** (positive control: READYs touching `services/api-gateway/`: 55). `git log` on the test file and on `anchorReadback.ts` at the tip: both CREATED by `cbae988db`.
- **Premise: the surface.** The cell calls one pure response builder three times with inline fixtures. No user store, no session, no JWT, no chain, no product bytes. ANCHORING read-back surface, test-only pin (allowed).

## Collision

**Same test file as the sibling brief `KS-1284-CHUNKED-DOCUMENTID-ROUNDTRIP-1` (this round) — DISJOINT hunks, same product file, DIFFERENT tamper lines.** That brief's hunk is `@@ -80,1 +80,8 @@` (inserts at the START of the same `describe`, trailing context `:80`); this hunk is `@@ -107,1 +107,6 @@` (inserts directly above the `CONTROL:` cell, trailing context `:107`). Both orders apply with `git apply` — measured in the MEASURED section: **CHUNKED first, then this** applies CHUNKED at `:80` and this at `:114` (offset +7 — the `:107` context line is unique, so git locates it seven lines down); **this first, then CHUNKED** applies both at their stated lines (CHUNKED's `:80` is above this insertion, so it never shifts). The resulting file is byte-identical in both orders (sha256 compared) and runs 12/12 green at the tip. Tamper lines: this brief plants `:74` and `:75`; CHUNKED plants `:111`, `:112` and `cardanoMetadatum.ts:81` — no shared line; each is planted-and-restored, none moves the other. Cross-reds: neither of this brief's tampers reds CHUNKED's cell (it asserts only `metadata.documentId` / `certId`); none of CHUNKED's tampers reds this cell (it asserts only `cardanoScanUrl`). The third brief of this round (`KS-1175-IDENTITY-EMPTY-OBJECT-1`) is in a DIFFERENT test file (`ks1175-identity-anchoring.test.ts`) and plants `anchorReadback.ts:52` — not a line this brief touches, and this cell does not reach `:52`'s outcome (`identity` is not asserted). The two held READYs under `services/anchoring/` (`KS-1171-8j`, `KS-1172-B3`) touch neither this test file nor any tamper line. Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 01:51, `--shared` scratch clone at `cbae988db`, node_modules farmed from the source checkout, source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_ks1105rows-drafter-precheck/`)

- Whole anchoring suite at the untouched tip: **319 cells, 318 passed, 1 failed** — the 1 red is `threadTokenMint.test.ts` "parameterises mint + spend with a deterministic per-seed policyId" (develop's own; the gate's count is the same 318/319). `full_suite_tip.out`.
- The proposed cell as a probe file at the tip: **GREEN** (`probe_tip.out`; console: the three URLs exactly as asserted).
- Tampers planted by bytes on the probe + the two existing KS-1175 files (`tamper_probe.log`): NETWORKINVERTED → probe's row-3 cell red + `CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction` red (`expected 'https://cardanoscan.io/transaction/ff…' to be 'https://preview.cardanoscan…'`), nothing else; MAINNETPREFIXED → probe's row-3 cell red, 0 existing red. File restored clean (git diff --quiet) after each.
- (the golden checker run and the both-orders apply are appended below after the run)

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts` / `+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1175-anchor-readback.test.ts`, then the hunk above exactly as shown (`@@ -107,1 +107,6 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 1 at the gate (anchoring read-back surface, test-only pin — allowed). Refs KS-1175** (and KS-522, whose placeholder rule sits two lines below the explorer base). **NEVER Closes** — KS-1175 stays In Progress (the §5f live sweep is owed; deploy/anchor are Kam's); this cell pins a pure builder, not the live GET.
- **From the #1105 gate's NOT-PINNED table** (report `2026-09-20-pr1105-tier1-r1/report.md`, row EXPLORERBASE-PER-NETWORK). The gate's proposed cell was kept in substance; template literals were replaced by `+` concatenation so no `+` line carries a backtick. The gate's "none names cardanoscan" was re-derived and found to be a grep slip (`:113` pins the preview URL) — the mainnet arm is what was unpinned, and the second tamper (MAINNETPREFIXED) is the one that isolates it.
- **Not pinned here, said plainly:** the live GET /api/anchors/verify/:hash (a boot; the §5f sweep); `CARDANO_NETWORK` values other than the three named (the `:76` template handles any string — a typo network yields a typo host, by design unpinned); the `null` for a KS-522 placeholder (already pinned by `:119`).
- **Collision: same test file as `KS-1284-CHUNKED-DOCUMENTID-ROUNDTRIP-1`, disjoint hunks, both orders measured; two tamper lines, none shared** (measured above and in the MEASURED section).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1175 night/inputs/test_only_1175EXPLORERBASE-PER-NETWORK-1.json night/briefs/KS-1175-EXPLORERBASE-PER-NETWORK-1.md ctx=65536
```

## MEASURED — appended after the golden run (01:56, artefacts `runs/2026-09-21_ks1105rows-drafter-precheck/EXPLORERBASE-PER-NETWORK/`)

- Golden checker (`tasks/test_only/checker.sh` on the golden `out.md`, fresh `--shared` clone at `cbae988db`): **RESULT: PASS (8/8)** — T5 green at the tip 11/11 cells (10 + the new one); T6 NETWORKINVERTED red set == {explorer, CONTROL: the rest of the KS-522/KS-726 shape is unchanged by the extraction}; MAINNETPREFIXED == {explorer}; every red an assertion failure; T7 controls green under both; T8 `anchorReadback.ts` restored to sha256 `9a41f455eb22` after each. Source tracked-modified count 0 before and after.
- All-orders apply with the two sibling briefs (`collision_all_orders.log`, 6 permutations): this hunk applies at `:107` when it precedes CHUNKED and at `:114` (offset +7, `git apply --verbose`: "Hunk #1 succeeded at 114 (offset 7 lines)") when CHUNKED is already in; `ks1175-anchor-readback.test.ts` is **133 lines, sha256 `431b51cb378e933c`** and `ks1175-identity-anchoring.test.ts` **227 lines, sha256 `ee1cbe52ea87bc02`** after EVERY permutation.
- Both files with all three cells at the tip (`combined_run.log`): **64/64 green** (12 + 52); under each of the 6 tampers of the round the red set is exactly what each brief declares (this brief's two: 2, 1). Whole anchoring suite with all three cells: **322 cells, 321 passed, 1 failed** — the same develop-own `threadTokenMint` red as at the tip (319/318/1).
