# B282 drafter report (read-only drafter, 2026-10-19)

**Brief:** `2026-10-19_B282_SEAT-W4_hpsmpoc-291-fix-round2.md` (about 100 lines). Structure copied from B276 (REFUSE checks, standing lines 1-8, BASE/BRANCH/IDENTITY, HOLDS incl. the HP Restricted hold verbatim, slot convention, STATUS, last line).

**Read:** the B276 brief (whole), B279 STATUS (whole), B276 STATUS lines 1-88. No code, no git, no dotnet, no HTTP, no Jira run by the drafter.

**Slots to fill (8):** CODE_MAIN_SHA (RELAYED befd45e77b391467a1313af8b7b5e0fc580f7b63), HEAD_SHA (RELAYED b8362d7e1ad1632c4a9c2409d62a117493c2bcda), MODEL, STAMP_TIME, PANE (Datasec/HPSM-POC-W4), PANE_SUFFIX (W4), PORT_BLOCK, B_NUMBER_CONFIRM. The drafter did not check the folder for B282/B283 hits beyond `ls | grep -c B282` = 0 at drafting.

**All facts RELAYED** (gate B279 and builder B276): line numbers `:128-140`, `:178-184`, the 14/0/0 and 1,462/13/0 counts, the SDK/pack facts, mutants a1-a5 results. The brief makes the seat re-measure the SDK facts (401 pack 10.0.12 and m1 green; 402 and m1 red; in-tree `dotnet --version` 402) before writing, and STOP on disagreement.

**Judgment calls:**
- Brief names the Major.Minor rule as "the pin's Major.Minor" (not hardcoded 10.0); new-row shape left to the builder (the existing Theory cannot express DoesNotContain).
- Added a mutant dropping the Major.Minor check, and re-runs of a2/a3/m291/m291b, beyond the commission's a1/a4/a5.
- Jira comment goes after the push read-back; no transition.
- No records work this round; the PR #161 body text, commit-7c87bdf note and the Done-when / B271-6 amendment are in FOR TUESDAY with corrected text.
- Seat told to read `BundledVersions.props` / pack manifest as a named exception to the `.tools/dotnet` internals hold.

**Top doubt:** the B279-3 fix compares to "the pin's Major.Minor", but the helper may not receive the pin at the point where it maps a file version to a package (RELAYED only that RaiseThePin takes a pin). If `PackageVersionOf` is pin-free, the seat may need a signature change inside the test file; the brief allows it (test file only) but does not say so explicitly.
