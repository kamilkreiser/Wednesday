STARTABLE: YES (after Tuesday's stamp; X90 is READY and the X91 pane is gone)

# B2179 DRAFTER REPORT | OXPd: kit X91 re-drafted as X92 for a Relay lockdown route Azure offers

Read-only drafter for Tuesday s335. Clocks by `date`: start Fri 27 Nov 2026 22:04:00 AEDT; REST reference read 22:05 to 22:06; tool built and tested 22:05 to 22:08; kit written about 22:09; last check 22:13:35. Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/d2179/`.

## Outputs
- Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2179_SEAT-X92_oxpd2-azure-mock-foundation-r2.md` (168 lines). Its first line says it SUPERSEDES B2176's X91. Sidecar `.measured`: 81 of 81 measured, `stamp_check.py` rc 0.
- Seat tools (`d2179/seat-tools/`): `az2179.py` (sha256 `293d7be5273935a2c8a0e09e7c1eeeac50c71330e6ce2f5491e1cb58de1c6a29`, 783 lines) and `cost2176.py` (copied unchanged, `3f0e7c4b3658eeee8c8f95e92b99aafe15e7addf37e459426385d45a306b85ec`).
- Seat X92 is free. A program scanned Tuesday's briefs for `X92` and found 1 file, this commission. The control `X91` found 5. OXPd Briefs file names: `X92` 0, `X91` 2. `.tools`: no `x92` folder, `b2176-x91` present. Panes: 9 live, none OXPd. New lane `.tools/b2179-x92`: absent (`ls` rc 1).

## BLUF
1. **Step 9 route (frozen):** `az resource update --ids /subscriptions/a6b8fe11-d1b5-4293-8727-b34aba08a705/resourceGroups/oxpd2-dev-rg/providers/Microsoft.Relay/namespaces/oxpd2-mock-relay --api-version 2021-11-01 --set properties.publicNetworkAccess=Disabled`. It is read back by `resource show --ids <same> --api-version 2021-11-01` with an EXPECT on `properties.publicNetworkAccess==Disabled`. Step 14 re-reads it after the private endpoint, and there it is now a STOP, no longer a FOR TUESDAY note.
   - **Source:** Microsoft's Relay REST reference, Namespaces - Create Or Update at 2021-11-01 (https://learn.microsoft.com/en-us/rest/api/relay/namespaces/create-or-update?view=rest-relay-2021-11-01, read 2026-11-27 22:05 AEDT). The `RelayNamespace` body has `properties.publicNetworkAccess`, type `PublicNetworkAccess`, default `Enabled`, values `Disabled | Enabled | SecuredByPerimeter`. X90's saved read shows `namespaces` offers 2021-11-01.
   - The installed CLI 2.92.0 has no public-access flag on `relay namespace create` or `update`: their `--help` pages have 0 lines naming `public` or `network`. `relay namespace update` offers only generic `--set`, which works on the CLI's own model at an API version I could not pin. So I chose `az resource update` with an explicit offered `--api-version`.
2. **The IP-rule mechanism is unavailable here.** The REST reference documents `namespaces/{ns}/networkRuleSets/default` at 2021-11-01 (https://learn.microsoft.com/en-us/rest/api/relay/namespaces/create-or-update-network-rule-set?view=rest-relay-2021-11-01, read 22:06). This subscription's provider lists no such type in any spelling. The kit keeps the fail-closed goal: public access Disabled, reachable only through the private endpoint, no IP rule. Q4 and NOT DECIDED 3 now leave "how the Mac's listener reaches the namespace" to the lab kit.
3. **Step 2's filter** compares types lower-cased. Its required set is the five types the kit actually uses, re-derived from X90's file: `namespaces`, `namespaces/authorizationrules`, `namespaces/hybridconnections`, `namespaces/hybridconnections/authorizationrules`, `namespaces/privateendpointconnections`. `networkRuleSets` is gone from the set. The 13 listed types are printed in FACT 9, and the seat also checks the file's sha256.
4. **The tool changed in ONE entry.** All other counts are unchanged: 19 writes, 38 agent entries, 11 inventory rows, A$11.80 for the kit, plan A$116.28 of A$120. The STOP list, grant row, Owner/agent split, ceiling and holds are X91's text.

## Facts re-measured (instrument, control)
- **X90's provider read** (`<x90>/logs/relay-after.out`, sha256 `10e41804...`, 22,417 bytes), by a python program: `Registered`, 13 types. Each of the eight `namespaces*` types offers 2021-11-01 and lists australiaeast. No type contains `networkrule`.
- **Kit Step-2 program**, extracted from the kit text by regex:
  - On the real file it prints 5 lines, each `listed: True | 2021-11-01 offered: True`.
  - Control: a fixture with `namespaces/hybridconnections` removed prints that line `listed: False | 2021-11-01 offered: False`.
- **`az2179.py` vs `az2176.py`** (`diff`): one hunk, `153,155c153,155`, the Step 9 W(...) entry only.
  ```
  < W(["resource", "create", *G, *NRS, "--properties", NRS_PROPS, *S], "netrules", ...network rule set... )
  > W(["resource", "update", "--ids", NSID, "--api-version", "2021-11-01", "--set", "properties.publicNetworkAccess=Disabled"], "netrules",
  >   "(no delete: public network access is a property of the namespace; to reopen, the product owner's word and a later kit: az resource update --ids " + NSID + " --api-version 2021-11-01 --set properties.publicNetworkAccess=Enabled; NOT run by this kit)",
  >   "OXPd mock client: Relay namespace @NS@ public network access Disabled (a namespace property, API 2021-11-01), reached only through its private endpoint; no IP rule (the provider offers no network-rule-set type); A$0/month"),
  ```
  Full diff: `d2179/az2179.diff`.
- **Selftests:** `az2179.py --selftest` prints `SELFTEST: 48 of 48 PASS` (rc 0, 0 FAIL lines). `cost2176.py --selftest` prints `SELFTEST: 5 of 5 PASS`.
- **Mutants of az2179** (`d2179/mutants/`):
  - new entry given `--debug`: 47 of 48. The failing row is "every entry of both lists is accepted exactly as printed", which shows the selftest covers the new entry.
  - identity check removed: 42 of 48.
  - cost check removed: 47 of 48.
  - redaction removed: 46 of 48.
- **Flags** (`flagcheck2179.py`, `--help` only, scratch config):
  - `FLAGCHECK: 48 entries, 0 with a flag absent`; `az resource update | flags 3` is OK.
  - Control: `--sets` for `--set` gives `missing --sets` and `1 with a flag absent`.
- **Kit-to-tool match:** every `RUN` command in the kit was tokenised (G, S, T expanded) and passed to `find_entry`. az2179 accepted 41 and refused 0; the only rows it did not match were the `RUN <label> -- <args>` shorthand placeholder. `relay-pna` is accepted by az2179 as a write and refused by az2176 (control). 37 of the 38 agent entries are used. The unused one is X91's network-rule-set `resource show` read, left in because the commission allows only one changed entry (Q-B).
- **EXPECT on fixtures** (the kit's own `relay-pna-show` assertions through `do_expect`): `publicNetworkAccess: Disabled` PASS; `Enabled` FAIL (control).
- **Inventory:** `len(INVENTORY_AFTER)` is 11 and equals az2176's list. A namespace property adds no row, so the after-set and Step 14's count of 11 stand.
- **Other checks:**
  - `<sp>` stat: `-rw------- 204`; `.azure-oxpd2-sp` is `drwx------`.
  - X90 STATUS last line holds `READY B2176-X90:` (1).
  - X91 STATUS last line is the `STOPPED: NEEDS TUESDAY X90 output:` line.
  - `<x91>` holds `_quarantine` (empty), `gate` and `logs`; `ledger.json` is absent (rc 1).
  - `models_latest` opus = `claude-opus-5-5`; OXPd `CLAUDE.md` is 89 lines and line 7 holds the Opus sentence (1).
  - The grant row holds `NOT granted:` (1).

## Chain inputs
| Step | Input | Produced by / present at |
|---|---|---|
| 1 | `<src>` (az2179.py, cost2176.py); records; `<sp>` mode; `<x91>` listing | d2179 scratch (MEASURED); project; kit X91 (MEASURED) |
| 2 | X90 STATUS; `relay-after.out` (sha pinned); `prov-*` | kit X90, READY (MEASURED present) |
| 3 | cost2176.py; retail API | Step 1; Microsoft |
| 4-5 | az2179.py; `<sp>`; `.azure-oxpd2-sp` | Step 1; present |
| 6-14 | login (5), names.json (4), costs.json (3, which holds the `netrules` key: cost2176.py line 79) | earlier steps |
| 9 | the namespace | Step 8 |
| 10 | snet-pe (7), namespace (8), private zone (10a) | in order |

## D-decisions (mine, in the kit)
- **D1.** I used `az resource update` with an explicit offered `--api-version 2021-11-01`, not `relay namespace update --set`. The CLI command's generic update follows its own model and API version, which the help page does not show. `resource update` does a GET then a PUT of the full namespace body at a version the provider offers (DERIVED; NEVER RUN against Azure).
- **D2.** Step 9 keeps its place (after the hybrid connections, before the private endpoint) and its cost key `netrules` (A$0), so `costs.json` from the unchanged cost2176.py still covers it.
- **D3.** Step 14's re-read is now an EXPECT. A value other than `Disabled` after the private endpoint means logout, then STOP. Before, it was a FOR TUESDAY finding that leaned on the rule set.
- **D4.** Added three small read-only checks: the sha256 of X90's file in Step 2; `<x91>/ledger.json` absent, in PRIOR WORK and REFUSE; no live X91 pane, in REFUSE. Added `B2179` to the PRIOR-WORK counts.
- **D5.** The tool's docstring still says B2176, and its tags still write `brief=B2176`, so the `tags.brief==B2176` EXPECTs stand. Changing either would have been a second change to the tool.

## Questions for Tuesday (each with a default)
- **Q-A (Step 9 route).** Default: freeze `az resource update ... --set properties.publicNetworkAccess=Disabled` at 2021-11-01. Alternative: 2024-01-01 or 2026-01-01, both offered by `namespaces` (FACT 9). Neither was read in the REST reference by me.
- **Q-B (unused read entry).** Default: leave X91's `resource show ... networkRuleSets` read on az2179's list unused. It is a read and harmless, and the commission allows only one changed entry. Alternative: remove it in a later tool.
- **Q-C (how the lab connects).** Default: the lab kit decides how the Mac's azbridge listener reaches a namespace with public access Disabled. The options are through the private network, or a later provider read that offers networkRuleSets. Until then, nothing reaches the namespace from the Internet, which is intended. Alternative: a ruling now to plan public `Enabled` without IP rules. That would not be fail-closed and I do not recommend it.
- **Q-D (lane re-use).** Default: new lane `b2179-x92`; X91's lane stays as evidence. Alternative: re-use `b2176-x91` (it holds no ledger). That would need X91's names in the kit and would mix two kits' gates.

## UNMEASURED
- Every Azure answer, carried from X91. New in this kit:
  - whether ARM accepts the PUT that `resource update` builds from the GET body at 2021-11-01;
  - whether the response echoes `publicNetworkAccess`;
  - whether creating the private endpoint later leaves it `Disabled`. Step 14 checks this.
- Whether disabling public access blocks any control-plane call the kit makes afterwards. Steps 10 to 14 are ARM calls, which by design public access does not gate. DERIVED, not run.
- Global name availability, prices since 21:37, and the network-rule-set write's real behaviour (not used).

## Outside-the-fences disclosure
- **az:** only `--help` pages for `relay namespace create|update|show` and `resource update|show`, plus the flag check's `--help` calls, all under my new scratch config folder `d2179/azcfg-help`. No az call against Azure and no az call under either OXPd identity folder. On the first help call the CLI printed "You have 2 update(s) available", so it may have made its built-in version-check request before I set `core.check_cli_version=false` and `core.collect_telemetry=false` in that scratch folder.
- **HTTP:** WebFetch GETs of two learn.microsoft.com REST reference pages. No other host.
- **Reads in the OXPd project:**
  - X90's lane logs and STATUS; X91's lane listing and STATUS;
  - `CLAUDE.md` (line count, line 7);
  - `stat` of the login file's mode and size, and of the agent state folder's mode. The login file was never opened.
- **No writes outside the fences.** I wrote only the kit, its `.measured` and this report, plus scratch under `d2179/` (seat-tools, mutants, proto fixtures, help pages, diffs, check outputs). The selftests made their own temp folders under the system temp, as the tool is built to.
- Nothing written in OXPd, Jira, GitHub, cards or mail. No `cd`, nothing deleted.
- The kit's name scan uses the underscore-aware pattern, with no hits; no planted control was run.
