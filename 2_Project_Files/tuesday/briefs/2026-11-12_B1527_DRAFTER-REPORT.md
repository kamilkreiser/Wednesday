STARTABLE: YES (after the Stamp; 7 lines read four underscores by `grep -c` on the unstamped kit, 0 `@X@` tokens, 0 non-ASCII bytes; the kit is 99 lines)

# B1527 drafter report (2026-11-12, about 09:09-09:20 AEDT by `date`)

## BLUF
Kit for SEAT-M126, MPSCALC-160 clause 6, the product owner's option a: the server stamps `PriceAudit.DefaultSectionRebate` (0.07, already in the code) on new sections for a caller without pricing rights; Duplicate copies hidden inputs unchanged (no stamp on a copy); typing a rebate stays refused. Model: row C3 (`model-routing.md:93`), Opus `claude-opus-5-5` (`models_latest.json:17`), launch `BRIEF_SEAT_LEVEL=opus`; gate row G1 (`model-routing.md:108`). Branch `b1527/mps-160-rebate-default-no-rights`, port block 9830-9839. Red-first rows L1-L9 plus unit rows, seven plants, a leak sweep over every endpoint that builds from a quote, the docs rewrite (ENGINE.md X-32 and four other sentences) in the same commit.

## Facts re-measured (instrument; control)
- Main `baf0aabec3c02457072ee848b166b17d3d7b0e80` (`gh api -X GET .../branches/main`, 09:10); open PRs 0 (control `pulls?state=closed` printed 184, 183; `pulls/99999` 404). `global.json` 10.0.404.
- Ticket MPSCALC-160 read whole by GET, 1 description + 4 comments (copy `fleet/state/s270/draft1527/MPSCALC-160.txt`; reader reads `.env` in-process; control MPSCALC-361 Done). Newest comment 2026-11-01.
- The earlier measurement of this case is the B1511 STATUS ("Part 3 ... THE HAZARD") and its ANSWER-1: naive stamp makes plain's duplicate of their own quote 201 -> 403 `INTERNAL_INPUT_FORBIDDEN`. The drafter re-read the cause in source (`QuoteEndpoints.cs:538` against `PricingPolicy.cs:48`), did not run it (no dotnet run by the drafter).
- `PriceAudit.DefaultSectionRebate = 0.07m` exists (`PriceAudit.cs:24`), and `PriceAudit.cs:58` already exempts a section added on a save at that value (the earlier answers at `CLARIFICATIONS.md:886-887`). The kit says reuse it.
- Docs carrying the old rule (`grep -n` over raw files at the sha): `docs/ENGINE.md:159` (X-32; also carries a person's name and a card id, so the rewrite drops both), `docs/API.md:184`, `:239`, `:431`, `docs/api/openapi.json:369`, `:1677`.
- Existing row the ruling flips: `QuoteApiTests.Duplicate.cs:150`, its second (purchase) block only.
- Branch census: 9 pushed `b15*` branches, `compare main...<b>` files read; none touches a file of this partition. `b1526` touches `tests/.../Infrastructure/ApiHost.cs` and `EntraHost.cs` (the kit forbids helpers there). `b1511` and `b1520` touch `docs/ENGINE.md` (the kit says re-read X-32 at your main).
- Ports: `lsof -nP -iTCP:9830-9839 -sTCP:LISTEN` 0 rows (control: 11 listeners machine-wide). Scan of the 42 non-`.pre-` SEAT kits of 11 and 12 Nov for `983[0-9]` with `-w`: 2 hits, both HPSM-POC, B1490 and B1497, no live pane (panes: `tuesday`, `fleet-monitor`). The B1528 drafter's files were not touched or read; the kits' paths are disjoint (this one has nothing under `web/`).
- `.tools/.heavy-lock-1` was held by a gate at 09:12:52 (holder text read); `.heavy-lock-2` absent; load1 24.23, 18 CPUs; `df` 1282 GiB free; `.tools/b1527` absent; side SDK dir present.

## D-decisions
- D1: "hidden inputs" = the set `PricingPolicy.Apply` step 4 keeps today (section markup and rebate, line `pricingMethod`, rates `supplies`, deal `usage.supplies`). Reason: the ruling says "the same way an edit already keeps them". Markup is included because a manager-set markup would otherwise still make plain's duplicate fail for the same reason.
- D2: visible-price refusals (sell override, fixed rate, manual item) stay on Duplicate: the ruling reaches hidden inputs only. The kit measures the refusal code in row L7.
- D3: target GP on Duplicate is HELD, unchanged (`QuoteEndpoints.cs:534`): not a stamp, not in the ruling. The seat reports its base behaviour.
- D4: no change to `PriceAudit.cs`. Create records the stamped value in the audit as set by the caller (B1511 measured it); internal-metrics only; left as is, raised as Q-1.
- D5: gate tier set to G1 in the kit (permission rule on a money input), Tuesday confirms in the Stamp. Model row follows the commission's expectation (C3). Note for Tuesday: the C3 row's words are "design ... (the decision, not a spelled-out edit)"; the ruling spells the rule out, but it changes who may set a money input and it names a side effect, so the kit sits on the row the commission named.
- D6: existing-test edit permitted for one block only (`Duplicate.cs:150`, purchase block); any other red is named, and edited only if it pins the old X-32 sentence, else STOP.
- D7: READY target 150 minutes from Step 0; Hard stop is a Stamp slot.

## Q-questions for Tuesday (each with a default)
- Q-1: Should the create audit record the stamped 7% as "set by" a caller who never sent it? Default: unchanged (recorded, internal-metrics only). The alternative is a one-line exemption in `PriceAudit.cs`, a separate change.
- Q-2: Target GP on Duplicate for a caller without rights (a manager-set rental or purchase target) still refuses. Default: HELD, report only. The product owner may want the same copy rule for it.
- Q-3: Should the web (`web/**`) change? Default: no; the web keeps stamping for rights holders and sends nothing for others.
- Q-4: Is the model row C3 plus gate G1 as you expect? Default: yes, as written.

## UNMEASURED
- No dotnet command was run by the drafter: whether the new rows are red at main, and which existing rows go red when the stamp lands (the kit tells the seat to run the whole suite and name them), are unmeasured.
- Whether the Python demo stub (`tools/demo/test/stub_api.py:252`, mirrors the create/edit refusal) needs any change: derived no.
- Whether `Infrastructure_Contract.cs` or other docs-reading Api rows break on the docs edit: unmeasured; the kit makes the seat run them.
- The live MPS pane list and the live heavy locks at launch: Tuesday's Stamp slot.
- The rights-holder side of the quote (the analyst's view of the stamped value) is asserted by the rows, not observed.

## Outside-the-fences disclosure
- Jira: GET only, MPSCALC-160 and the control MPSCALC-361, in-process `.env` read by a scratch script (`fleet/state/s270/draft1527/jira_get.py`; it prints no token). No JQL used.
- GitHub: `gh api -X GET` only, under the project's `GH_CONFIG_DIR`: branches, tree, raw contents at the sha, open PRs, matching-refs, `compare` for nine branches. No clone, fetch, or git write in the project repo.
- Read in the project tree (not the repo): `1_Project_Definition/Briefs/2026-11-11_B1511_STATUS.md`, `CLARIFICATIONS.md` (grep and short sed ranges), `CLAUDE.md` (lines 1-12 and 50-51), `JIRA.md` (grep). `ls`/`df`/`uptime`/`lsof`/`tmux list-panes` for the machine facts, and `ls -a .tools` plus one `holder.txt` read.
- No card was read (no `decision_queue.sh` call); the card text in the commission was used as given. No `fleet/briefs_staged/`, scoreboard, ledger, or other project tree read. Scratch only under `fleet/state/s270/draft1527/` (raw source copies, ticket text, tree list); the two output files are the kit and this report.
- Two shell commands were refused by hooks (a `cd` in a first line; an `=====` separator) and re-issued without them; no effect.
