# KS screen for the local models: 2026-10-09, 23:15 delta (3 briefs: rung 1 Ornith, rung 3 + rung 4 Spark)

Written 2026-10-09 23:27:49 AEDT (shell `date`) by a brief-writer sub-agent for Wednesday. Commission: Kam 23:10 "focus on secuura work with the local models", amended 23:12 "keep pushing harder and harder tickets to the spark as a way of testing it" (up to 2 harder Spark candidates, each with a checker that can fail). Secuura only. Method: SCREEN_1400's (delta first, positive control, exclusions before screening), the kit predicate, the kit 03 brief shape copied from `night/briefs/KS-998-format-gate-npm-stdin/` and the two 10-07 KS-1410 briefs.

**Read-only on client systems:**
- **Linear:** GraphQL reads only; key sourced from the Blockchain `4_Credentials/.env` in a `set -a` subshell, never printed. Instrument: `scratchpad/screen2315/q/lin.py` (paginated to `hasNextPage=false`), plus `fleet/board_count.sh`.
- **GitHub:** REST GET only (open PRs + their files), token from the same `.env` in a subshell, a scratch `GH_CONFIG_DIR`.
- **Git under `!CODING/`:** `ls-remote`, `cat-file`, `config --get` only. Every other git verb ran in a `git clone --shared --no-checkout` under `scratchpad/screen2315/clone`, develop fetched BY SHA. Files were measured in a `git archive` extraction (`scratchpad/screen2315/wt`, node_modules symlinked FROM the checkout).

**Not touched:** `spark/queue.md`, `night/queue.md`, `queue.sh`, `round.sh` (no `--dry-run`, no `--control`: they write `spark/state/`, outside this commission's write scope), Linear/GitHub writes, mail. Nothing created under `!CODING/`. Nothing deleted.

## BLUF

1. **Tip: develop moved twice during the screen.** The commission's `44753e3e7f4e` was superseded by **`e919265db717`** (#1438, KS-1455 Schemathesis 4.30.0; `ls-remote` 23:12:11) and then **`09a7b2ec8c11`** (#1439, `5_Project_History/history.md` only; `ls-remote` 23:22:53). Everything was measured at `e919265db717`. Every file the three briefs name has the **same blob** at both (checked with `rev-parse`), so the briefs carry `Tip: 09a7b2ec8c11…`.
2. **Delta: 20 open tickets** updated since 2026-10-09T03:00Z (Backlog/Todo/In Progress plus In Review, which shares Linear's `started` type), read 23:13. `board_count.sh` read **19** at 23:27:44 (`TOTAL=19 … a real count and not a cap`). The one-ticket drop is consistent with KS-1455 leaving In Review when #1438 merged; that is reasoned, not re-read. **Positive control:** the created-since set is KS-1454 and KS-1455, and both are in the updated set.
3. **Delivered: 3 briefs** (target 4). One is easy and two are harder, as amended. The fourth slot is empty because the remaining residue fails the predicate (see Rejects). It was not for lack of reading: 19 tickets were read in full.

   | brief dir (`local-model/night/briefs/…`) | ticket · carve | tier · rung · route | new test at tip → golden | golden apply at tip |
   |---|---|---|---|---|
   | `KS-1410-transfer-process-expired-500/` | KS-1410: `transfer/src/routes/delegations.ts:283`. The 1 transfer site of the 18 still open | code_patch · **rung 1** · **Ornith 1.5** (Spark fallback) | **4 failed / 2 passed** → **6/6**. Transfer suite 79/0 → 85/0. tsc rc 0; control: a typo reds tsc, rc 2 | `apply --check` **rc 0**; reverse at tip **rc 1** (control); applied files `cmp`-identical |
   | `KS-1346-apigw-fail500-type-and-field-names/` | KS-1346: gate77 N-1432-2. The three api-gateway `fail500` copies get the ruled "type and field names only" line | code_patch2 · **rung 3** (3 product files + 1 new test) · **Spark** | **9 failed / 6 passed** → **15/15**. With one file reverted: exactly that file's 3 reds | **rc 0**; reverse **rc 1**; 4 files `cmp`-identical |
   | `KS-1410-apigw-audit-export-502-loose/` | KS-1410: gate77 N-1432-1, the 502 half. `audit-export.ts:175` | code_patch · **rung 4** (looser: shape stated, product lines NOT given) · **Spark** | **5 failed / 3 passed** → golden **8/8**. An alternate wording **8/8**. A half fix **1 failed** (X2) | **rc 0**; reverse **rc 1**; stacks on the KS-1346 golden **rc 0** |

   The api-gateway suite was run with both api-gateway goldens and compared with the tip: the **same 9 pre-existing failures**, from the scratch tree's missing `docs/` and `migrations/`, and **0 new reds**. tsc returned rc 0. `brief_lint.py` returned **rc 0** on all three dirs. In every brief, the fences were compared byte for byte with the golden and with the measured test: identical.
4. **What blocks queueing (owner calls, none acted on):**
   - **(a) `started_ok`.** KS-1410 and KS-1346 are both **In Progress**, so `build_input.sh:164-173` refuses them without `started_ok=<reason>`, and that override is yours. Each `spark.pins` carries a proposed reason, **commented out**. The checks behind it: no attached PR is open (KS-1410 → #1432 merged; KS-1346 → #1296/#1297/#1311/#1312/#1316/#1317, none in the 23:14 open list), and no drafted lane names these files.
   - **(b) The dry run is owed.** Run `round.sh <dir> --dry-run`, then `--control`, per brief. Rung 4 is the one to watch: by my reading of `build_input.sh:515-525`, a fence-less `## The exact change` gives A3c an empty checklist, and A3b still grades `:175` by line. That is read from the source, not run. **If the builder refuses it, that refusal is the rung-4 finding.**
   - **(c) Ornith wiring.** The rung-1 brief uses the brief-dir layout. Ornith's last round (KS-937, `night/done.md`) ran from a pre-built `night/inputs/*.json`. Building that input from this dir is your step.
   - **(d) Shared file.** Both the rung-3 and rung-4 briefs touch `audit-export.ts`, at `:25` and `:170-179`. Each golden applies alone, and either applies on top of the other. Run them in either order. Raise them as separate PRs, or fold them together.

## Ladder (amended commission)

| rung | brief | what it tests | a PASS tells us | a FAIL tells us |
|---|---|---|---|---|
| 1 | KS-1410 transfer `:283` | Ornith 1.5 on the simplest code_patch shape: 2 hunks, one using the blank-line `-`/`+` rewrite, and a 116-line new test. Input is ~32 KB of files plus the task, under the ~28K-token ceiling | Ornith 1.5 holds the vitest code_patch tier that the Spark passed on 10-07 for the same class. It is a cheap second lane for one-site residues | Ornith's ceiling is below the Spark's on vitest. Read A2 (hunk shape) and A3b (the site) |
| 3 | KS-1346 apigw ×3 | Multi-file: one identical long `+` line into three files, each with its own header. A3 checks the declared set exactly, A3x byte identity per file, and A4 that each router's reds belong to its own hunk | The Spark carries a repeated edit across files without dropping or mutating one. Rung 3 is solid on vitest, not only on bash_patch2 (KS-1274) | **Which file** went wrong is the data. A dropped file shows as 3 reds (measured). A one-byte slip in the 300-char ruled line fails A3x. Either says multi-file repetition is the weak point |
| 4 | KS-1410 audit-export 502 | A looser brief: the fix is stated in three numbered rules with no product `+` lines. The verdict comes from tests that pin the contract, not the wording | The Spark can write a minimal, correct product edit from a stated shape. That opens briefs a writer cannot fully pre-solve. Expect `golden DIFFERS`; that is not a fail | One of three things. A refusal at build (the harness cannot yet express rung 4 on code_patch). An edit outside `:170-179` (XC1/XC2 red). Or a half fix (X2 red: measured that the cells catch it) |

Rung 2 (multi-hunk) is not separately briefed here: the rung-1 brief already has 2 hunks, and rung 2 (7-8 hunks) already PASSED on 10-07 (KS-1410 notifications). Rung 5 (prose ticket) was not attempted: no delta ticket has a stated shape without also needing a decision.

## Verdict per ticket (read in full: 19)

| Ticket | Verdict · predicate clause |
|---|---|
| **KS-1410** 28 unguarded err.message in 500 bodies | **PASS ×2 → briefed.** One brief takes the transfer site, and one takes N-1432-1's 502 half.<br>The other residue is **NOT**:<br>- **tenant-provisioning `index.ts` (7 sites):** no in-process harness. `app` is not exported, it `listen`s on import, it builds a `pg.Pool` at module load, and the service's only tests are a guard unit test and a placeholder. It is also the DB-admin service that holds PG credentials, so it routes to **Claude** to build a harness first.<br>- **mcp-server `http-server.ts` (10 sites):** no harness for the same reasons (`app.listen` at import, no export). It overlaps KS-1214 (an auth defect on `POST /hash`, which reads arbitrary `filePath`): **Claude, security surface**.<br>- **batch.ts per-item `:129-130`:** fits, but is held back so this screen does not put three briefs on one file. It is the next brief. |
| **KS-1346** fail500 non-Error throw | **PASS → briefed (rung 3)**, api-gateway copies only. The originate parts A-D have landed. The rotate-secret cell (`Done when` item 3) is a credential surface → **Claude**. |
| KS-1364 85 request bodies not `required` | NOT: **"decide whether"**. It is a per-operation decision ("whether each body *should* be required is this ticket's per-operation decision"), and the openapi files were the seat-E lane. |
| KS-1284 CSL metadata 64-byte limit | NOT: the remaining leg is a **live chain read** (the `source chain` verify path), with no in-process RED. |
| KS-1454 anchor `signatureHash` | NOT: a multi-file feature (schema + CIP-674 metadata + read-back + optional verb gating). It is new work, not a fix, and touches the anchoring chain write. Too wide for rung 3 as filed; a candidate for a later rung-5 trial once item 1 is carved. |
| KS-1175 non-PII actor fields | NOT: owned by a live chain deploy/anchor ruling (Kam 09-22); remaining legs are live. |
| KS-565 sweeps: untracked failures | NOT: a sweep register, with no single file or stated fix. Its 10-09 comment only records the KS-1455 branch. |
| KS-595 skips cite closed tickets | NOT: **"are the defects still live?"**, a question for a human. |
| KS-693 M365 503 when ENTRA unset | NOT: In Review (a lane has it); M365/Entra = auth-config surface → **Claude**. |
| KS-969 systemTest actor/credential path | NOT: In Review; credential provisioning → **Claude**. |
| KS-772 review stream S↔K | NOT: a review stream for Stuart. |
| KS-1357 OAuth rotate-secret omits `id` | NOT: an OAuth secret rotation, a **credential surface** → **Claude**. |
| KS-621 document reads by org | NOT: "deliberately NOT a fix spec", a security model not yet decided → **Claude/owner**. |
| KS-627 CIP-8 wallet signature verification | NOT: "It is not a patch", crypto + contract change, a **security surface** → **Claude**. |
| KS-1448 notifications BOLA | NOT: **security surface** (authz) → **Claude**; also #1440 open. |
| KS-1449 nft ipfs upload body required | NOT: merged at `1fba82ddb`; a gate77 lane row. |
| KS-1426 cleanroom scans four dirs | NOT: "Not claimed: … A fix", so there is no fix shape. A widened `find` has a named blast radius (install time, `--no-workspaces`, prettier scope). |
| KS-1427 unhandledRejection posture | NOT: "That's a ruling for you", a decision. |
| KS-1453 originate unused handlebars dep | NOT: two files (`package.json` + lock); dependency/supply-chain; and its own "Unmeasured: whether anything loads handlebars dynamically … That check comes first". |

**Excluded before reading (by title and assignee):**
- **Peter:** KS-492, KS-1396, KS-1455 (also In Review).
- **Lane K:** KS-1402 (also an auth surface).
- **Titles alone mark a security surface** (→ Claude): KS-1433 (connector-key scopes unenforced) and KS-1434 (`ApiKeyCreateRequest` rotate).
- **NOT on the 10-08 harder screen and unchanged since:** KS-1441 (classification decision), KS-1443 (red is Linux-only), KS-1444 (design + docker).

## Exclusions and collision checks (each zero with its control)

- **Live and drafted lanes** (`fleet/briefs_staged/2026-10-09_*`): `grep` for the three product files and `delegations.ts` across every 10-09 SEND/DRAFT returns only the R23 merge brief for #1432, which is merged. **Control:** the same grep finds that R23 brief, so the instrument works. The lanes U/W/K/KS-695/KS-1195 and R 26th (#1436 KS-808, #1431 KS-1355, #1430 KS-1328) and #1437 KS-1402 name none of these files.
- **Open PRs:** GitHub REST GET at 23:14:44 returned 28 open PRs and 137 file entries. **0** touch `api-gateway/src/routes/` or `transfer/src/`. **Control:** the same census lists 68 `Blockchain/Dev/services/` entries, including `api-gateway/src/utils/trustHeaders.ts` (#995) and `transfer/package.json` (#649, #575).
- **Round counters:** `spark/done.md` has 2 KS-1410 rows, both api-gateway (`:47`-`:48`, which shows the grep works), and 0 for transfer or N-1432-1. The KS-1346 rows and `READY_KS-1346-*` are all originate. That gives **0 rounds** on each carve.
- **Peter/Stuart:** none of the briefed tickets (both Kamil's).

## UNMEASURED

- **The builders were not run.** `night/build_input.sh`, `round.sh --dry-run` and `--control` were not run (see BLUF 4b). The only builder-adjacent gate run was `brief_lint.py`, which is read-only.
- **Scratch-tree fidelity.**
  - Only `services/{transfer,api-gateway}` and `shared` were extracted. The 9 api-gateway suite failures come from files they read (`docs/openapi/secuura-api.yaml`, `migrations/`) or from importing the real app; they are identical with and without the goldens.
  - node_modules and `@secuura/shared` resolve into the Secuura checkout's working tree, not the tip.
  - The 10-07 KS-1410 round (full clone) read 0 failed.
- **No live stack** for any brief. Every thrown value is planted (service mock, throwing getter, stubbed `fetch`).
- **Linear comments** were capped at `first:50` per ticket. The largest delta ticket, KS-772, did not reach the cap.
- **Ornith token count** was estimated from bytes (~32 KB of brief, product and reference). The tokenizer was not run.
- **Live seats' unpushed work** on these files was not checked; only open PRs and staged briefs were read.

## Scratch (session scratchpad, not durable)

`/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/abed0d42-c171-413b-8a16-140887a3dd87/scratchpad/screen2315/`:
- `q/` holds the Linear and PR lists.
- `t/` holds the ticket JSON.
- `g/` holds the goldens, the tip and fixed copies, and the suite failure lists.
- `clone/` and `wt/` are the scratch clone and the measured tree.

Brief file sha256/16:

| brief dir | KS md | golden.diff | spark.pins |
|---|---|---|---|
| KS-1410-transfer-process-expired-500 | `ce79374ca64b9cbb` | `a9b70cd45a25fd92` | `1fbe29527a6c2270` |
| KS-1346-apigw-fail500-type-and-field-names | `78b0f49153583ffa` | `e21ce6406079b6cc` | `b3202b2db7890eda` |
| KS-1410-apigw-audit-export-502-loose | `968ed2d65a61c848` | `85182ec0f77c4a4a` | `a36177adcb08cdb6` |
