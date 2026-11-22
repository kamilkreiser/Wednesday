# FOR RECORDS: OXPd 2 adapter README limits (kit B1922, lane E, owed items 45 and 46), gate G2 round 1, reader B1926

Not repository text. For the next OXPd records pass (backlog owed items 45 and 46); nothing here was written into the
project. No person is named.

## What lands

- ONE commit `b1079275` (parent `4a0a9717`), one file: `src/Datasec.Suite.Adapters.Oxpd2/README.md` (+49 -1, the
  re-cut of ANSWER-1, byte for byte its `1-readme-limits.diff`, sha256 `bc903822...`). It lands on main `7b0f4f55`
  (pull request 20 in between, two test files; merge tree `9302f7bf`, measured). C# totals do not move: main's 1581
  + 0 on both legs; skipped 4 / 19; RULES 500 files; unit tests 111, floor 111.
- Owed item 45: the README now names limits (1), (2), (3) and (5) to (11) beside (4), which was already there.
  (10)'s doc-comment line on `IDeviceSecretVault.TryGet` is NOT added (a `.cs` file) and stays owed to a later code
  lane. "Whether to keep a late grant" is named as an open question, not answered (no clarification touches it:
  `refresh`, `timeout` and `late` count 0 in the register; `grant` counts 1, at line 688, not about a token).
- Owed item 46: the full stop inside the list of semicolons is corrected; the map line is added as a census (206
  `additionalProperties`, all `false`, 37 inputs; the generator does not read the keyword; a map input UNMEASURED);
  the enum wire-name limit is added; what a printer does with a refused or tolerated callback is named UNMEASURED.
  NOT DECIDED 1 was ruled on 2026-11-22 (C-63, option a, keep both strict for now, to be revisited after the printer
  test; recorded as a decision that can change): the README's parse step says device answers are read strictly as a
  choice for now, to be looked at again once a printer's traffic is seen. Records (1), (3), (5) and NOT DECIDED 3 are
  untouched. C-63 also answers NOT DECIDED 2 (a callback with a new kind of result stays refused); the README does
  not mention it. `BACKLOG.md:306` still reads NOT DECIDED 1 and 2 as open: stale against the register.
- Item 45 closes on this landing but for (10)'s `.cs` line; item 46's README part closes.

## From this gate

1. **Minor, the map sentence (G1) is true of a declared map only.** Over the 37 tracked inputs under
   `contracts/oxpd2/hp/`: 1616 schemas of `type: object`, 1442 with `properties`, 206 with `additionalProperties`
   (all `false`), `patternProperties` 0, `propertyNames` 0, and **150 that declare neither `properties` nor
   `additionalProperties`** (open by JSON Schema's default; 94 of them empty request objects such as `beepRequest`,
   54 named `value`). At least one is generated as a raw `JsonElement`: `CapabilitiesImplInfoItem.Value`
   (`Generated/Application/Models.cs:886`, from `capabilities/properties/implInfo/items/properties/value`). Owed: one
   README line (a later docs lane) naming the open objects and how they are read.
2. **Info, an unnamed limit beside E4 (late grant).** `RefreshAsync` hands the refresh array to the endpoint as
   `ReadOnlyMemory<byte>` (`DeviceTokenHolder.cs:331`) and zeroes it in its `finally` (`:398`) when the wait times
   out, while an endpoint that ignores its cancellation may still be reading it. DERIVED, not run. For item 45's
   follow-up (a later lane: a README line, or a copy for the endpoint).
3. **Info, E1's edges.** `StoreRefreshValue` clears the held access value (`:68`), but a refresh in flight that then
   succeeds keeps its own access value (generation unchanged, `:356`, `:387`): the README sentence does not claim
   otherwise. A refresh between its generation read (`:294`) and its vault read (`:314`) reads the new value: the
   good case, not named.
4. **Info, E5 holds while that failed refresh is the last completed flight.** A flight that completes successfully
   later is reused instead (`:287` to `:289`), as the README's existing paragraph on waiting requests says.
5. **Info, the commit subject is 262 bytes, over GitHub's 256-character title.** The pull request title and the squash
   subject are shortened (243 and 252 bytes); the squash is therefore not the commit subject byte for byte.
6. **The seat's DEVIATIONS 1 (Step 1 baseline not run) is superseded by its own RE-CUT section**: the baseline ran
   22:00 to 22:04 (restore, build, 58 / 0 failed), and Step 4's survivor mutant ran (58 / 0 failed, the assembly
   written after the edit). The seat did NOT run the positive control; this gate did (A06 red alone).
