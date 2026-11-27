PR 2296: GO WITH NOTES (at head 329fae8c395fc624033def570058bb8b65e6b990; tier 1)

# QA GATE 421, tier 1: KS-2366 one-off SQL repair for the certifications made before the fix

Gate: claude-opus-5-5, findings-only. Started 2026-11-27 15:05:18 AEDT, finished 15:42:15 AEDT (both from `date`).

**PR state:**
- Read at the start (gh as kksecura, 04:05:29Z) and again at the end (04:42:10Z). Both reads agree:
  - OPEN, head 329fae8c395fc624033def570058bb8b65e6b990 (1 commit, parent 4764b2cf);
  - base develop 4764b2cfbc28768ef9c7b684e2af2e0f2f1438e5;
  - 6 files, +964 -0.
- `git diff --name-only` over `services`, `packages` and `migrations`: 0 files. No product code is in the PR.
- The PR body was read as raw JSON through urllib (`_work/out/pr2296.json`).

**My setup:**
- Clone: a fresh `gh repo clone` (`_work/repo`).
- Worktrees: `_work/head` (329fae8c) and `_work/dev` (4764b2cf, plus the 3 test files for the red-first run).
- node_modules: cloned with `cp -c` from the builder's `s-w78-fix`, after checking that the root, originate and shared lockfile sha256s are equal. I built packages/shared `dist` myself on each arm.
- Postgres 15.19 (my own throwaway):
  - data at `/private/tmp/g421/pg`, socket at `/private/tmp/g421/sock`;
  - `listen_addresses=''`, TimeZone UTC;
  - schema built the suite's way: docker/init 11 files plus 59 main-DB migrations, giving 115 tables.

**Where things are:**
- My fixtures: `_work/g421/fx.sql`, 63 rows, written by me.
- Raw outputs: `_work/out/`.
- Mutant copies: `_work/mut/`.
- The real script's sha256 is `ced08f1c7a5a04ca…`, which equals the blob at HEAD. It stayed unchanged through all 30 mutants.

## BLUF

- **The script does what it says, and its guards held under every attack I made.** On my 63 hostile fixtures:
  - **Dry run** writes nothing. The hash of all 115 tables is equal before and after. Control: apply on a read-only session fails with rc 3.
  - **Apply** writes exactly the 20 WRITE rows and nothing else. The other 114 tables are hash-equal, and the other 43 documents rows are md5-equal.
  - **The written blob** equals originate's REAL `confirmedBlobOf` on 20 of 20 rows. The REAL honest rule reads false before and true after on 20 of 20.
  - **Reverse** restores the whole database hash-equal, even when run with a session time zone of +14 h.
  - **A re-run** writes 0.
  - **The count guard** rolls back every wrong count with 0 rows changed (hash-proven). Injection through `mode` and `expected` is refused every time.
  - **Two concurrent applies** land exactly one.
  - **Run as an RLS app role**, it writes nothing. A missing column fails before any write.
  - **No dry run or apply wrote a row outside the class** under any input I built.
- **One Major (G421-1): the evidence cannot tell a real chain confirmation from a DEMO_MODE mock confirmation.**
  - anchoring's `MockAnchoringProvider` stores a BARE 64-hex sha256 as the "transaction", with status confirmed and `simulated` false. The repository says so itself (`anchoring/src/cardano/index.ts:253`; KS-587 is open).
  - Such a row passes every predicate. I built one and it reads WRITE.
  - DESIGN 2.1, S 129th, S 130th and the PR body do not name this path.
  - The merged live path (gate 420) applies the same rule, so this is not a defect in this PR's code. It is an unproven precondition for running the script on a box.
  - **The GO is conditional:** before the Kintsugi apply, the deploy seat must establish that anchoring on Kintsugi was NOT in DEMO_MODE over the stuck range (2026-09-17 to 2026-11-16), or check at least one of the 10 transaction hashes on Cardano preview.
- **Two Mediums:**
  - G421-2: reverse writes ANY non-lineage documents row that a manifest names, as long as the manifest's AFTER values equal that row's live columns. I demonstrated it on a non-certification row.
  - G421-3: the PR body's reverse command fails when run literally (it fails closed), and it would put box data on a process command line.
- **The bind, re-derived:**
  - 2.2 a, c, d and e hold at the head and at c50d033c6 and 8cbadd8d4.
  - My census adds three paths that DESIGN 2.1 lacks and corrects two of its rows (table below).
  - E2's claim that an event's replaced payload falls outside the window is false for an event within 10 s of issue (G421-4, Low). Such a row is written, but its confirmed transaction still carries this certification's id and content hash, so the meaning ("confirmed on chain") holds.
- **Re-runs (mine):**
  - new suite: 65/65 at the head, also run 20 more times: 20/20 green, R10 never flaked;
  - red by absence on develop, an honest label;
  - run-shell-suites WHOLE: 133 passed, 0 failed, 1 SKIPPED. The skip is environmental (the next line explains it), so this is not quite the builder's 134/134;
  - originate jest WHOLE: 251 files, 3770/3770; tsc rc 0;
  - shared vitest: 1746/1747, the only failure being KS-278;
  - docs-fragments: OK on both arms.

  The skip: the ratchet-leg suite's default cells need a nested `@types/node`, which my copied node_modules lack. It is not related to this PR.
- **Mutants:**
  - 13 of the builder's 40, re-made with the same edits: 13 KILLED, each by its named cell.
  - 14 of my own: 13 KILLED (8 of them only by my fixtures, which is a gap in the builder's suite) and 1 survived both judges.
  - The builder's 3 "equivalent by construction" terms: the two apply-target terms are NOT equivalent. Each changes the outcome under a concurrent writer. The dry run's READ ONLY is equivalent today.

## Findings

### G421-1 (Major): a DEMO_MODE mock confirmation passes every predicate; nobody has excluded it for the box
- **FOUND:**
  - `MockAnchoringProvider.submitAnchor` sets `txHash = sha256('mock-tx:'+payload+':'+n)` in hex, with status `confirmed` (`anchoring/src/mocks/mockProvider.ts` 54-80). It runs when the anchoring container has `DEMO_MODE=true` (`cardano/index.ts` 60-68, 270-273).
  - The repository's own comment says this hash is a BARE 64-hex that does NOT match `FABRICATED_TX_PREFIX` and DOES match the 64-hex tests (`cardano/index.ts` 253-257). It also says "The label itself is KS-587's to fix".
  - So such a row is `status confirmed`, `simulated` false, 64-hex, single, and its payload is stored with the issue's timestamp. It satisfies the link and E1 to E5 exactly.
  - The script then writes `confirmed` with that fake hash, and verify answers anchored **true** for a certification that never touched a chain.
  - DESIGN 2.2 a ("a single-path transaction always carries the stored payload") assumes that a chain transaction exists.
  - S 130th and S 129th excluded only the fabricated PREFIXES (`tx_sim_|mock_tx_|…`). Both state "the table's word, not a chain lookup".
  - Anchoring's compose default is `DEMO_MODE=${ANCHORING_DEMO_MODE:-false}` (`docker-compose.yml` 1325, since 846717ecf, 2026-04-27). So a box is exposed only if its env sets `ANCHORING_DEMO_MODE=true`. I could not check that (NO BOX, and it is a secrets file).
- **TESTED:** `g_mock` database: my W_BASE anchor row was given the mock provider's exact shape (sha256 `mock-tx:` hash, block 10500047, slot 131000020, `simulated` f, confirmed). Its verdict is WRITE with `refuse=-`.
- **Why Major and not Blocker:**
  - The PR's code applies exactly the product rule that the merged live path applies. `isAnchoredHonestly` plus the resolver would confirm the same row for a new certification, so this is no new class.
  - Kam's card states the limit ("this is each box's table saying confirmed, not a chain lookup").
  - The remedy is a precondition on the box run, not a code change.
  - The commission's severity rule ("marked confirmed without the evidence the design claims") arguably reaches it. Wednesday may read it as a Blocker.
- **Ask:**
  - Add a precondition to the run instructions: show that anchoring was not in DEMO_MODE on the box over the stuck range, or look up one of the hashes on Cardano preview.
  - Optionally, have the dry run print each row's `block_number` and `transaction_hash`, so a seat can spot the mock pattern (block 10_500_000 + 47n).

### G421-2 (Medium): reverse restores whatever a manifest says onto any non-lineage documents row whose live columns match the manifest's AFTER values
- **FOUND:**
  - Reverse's UPDATE checks only `id`, `tenant_id`, `external_id IS NULL` and `(updated_at, metadata, certification_metadata) = AFTER` (`ks2366-legacy-certification-anchor-repair.sql` 376-386).
  - It does not check:
    - that the row is a certification (`certificationType`);
    - that BEFORE and AFTER differ only in the `blockchain` key and `updated_at`;
    - that `manifest.box.db` equals `current_database()`;
    - that each id appears in the manifest only once. With a duplicated id, `UPDATE … FROM` picks an arbitrary BEFORE.
- **TESTED (forged manifest):** on `g_b`, I built a one-row manifest whose AFTER values are the live columns of `U_NO_CTYPE` (a row with no certificationType, outside the class), with BEFORE = `{"forged":true}`.
  - Reverse answered `reversed=1 drift=0`.
  - The row's `certification_metadata` became `{"forged": true}` and its `updated_at` became 2000-01-01.
- **Controls (all failed safe, all hash-checked: DB unchanged):**
  - a truncated manifest: invalid json, rc 3;
  - `rows` not an array: rc 3;
  - a bad uuid: rc 3;
  - ids rewritten as from another box: drift=20, reversed 0;
  - quotes, `\`, `$$`, `:'manifest'` and `\!` inside JSON values: treated as data, no shell file created;
  - a raw `\!` manifest: invalid json;
  - a stale manifest: drift (builder R5, and my updated_at-only touch).
- **Severity:**
  - Only a manifest forged with a row's exact live columns, to the microsecond, can do this, and the person running it is the box superuser.
  - An accidental, stale, truncated or other-box manifest cannot do it, and I proved each of those.
  - It is still a write outside the class through the script's own reverse path, and a cheap guard would close it (class plus box plus blockchain-only diff, inside the UPDATE).
- Also: reverse exits rc 0 when drift > 0, and `{}` as the manifest exits rc 0 with `manifest_rows=0`. A scripted caller has to parse the SUMMARY line to notice either case.

### G421-3 (Medium): the PR body's reverse command fails when run literally, and puts box data on a command line
- **FOUND:** PR body step 3 (also script header line 61) reads `docker exec -i -e KS2366_MANIFEST="<manifest JSON>" … -v manifest="$KS2366_MANIFEST"`.
  - The manifest is JSON full of `"`. Pasted inside a double-quoted shell word, the host shell strips those quotes, and also expands any `$`, backtick or `\` in the values.
- **TESTED, literally:** I replaced `docker exec -i … secuura-postgres sh -c` with `env … sh -c` and added only `-h <sock> -p 54421 -d g_lit -U g421`.
  - Dry and apply ran literally: dry rc 0, write=20; apply rc 0, COMMITTED 20.
  - The literal reverse (`_work/g421/lit_reverse.sh`) gave rc 3: `invalid input syntax for type json … Token "box" is invalid`.
  - The database kept its 20 confirmed rows. It fails closed.
  - The only rollback path is therefore broken as written, at exactly the moment a seat needs it.
- The literal form would also expose the manifest. Section A3 says the manifest is box data, but this form puts it on the host's `docker` argv and the container's `psql` argv (visible in `ps`), and in shell history if typed.
- Nothing in the run instructions says where to keep the apply output. It goes to the seat's terminal and wherever it is redirected, and no file mode is suggested.
- **The other run-instruction points hold:**
  - ON_ERROR_STOP is set inside the script (line 65), so a missing flag on the command line does not matter. Passing `-v ON_ERROR_STOP=0` still refuses a bogus mode: rc 3.
  - Apply cannot run without `expected`, which forces a dry run first.
  - A2 and A3 appear in the script header (lines 52-56) and in the PR body.
  - A4: the BEGIN line names the database, user, server time (UTC) and stuck-class count (measured).

### G421-4 (Low): E2 does not exclude an event that replaced the payload within 10 s of issue
- **FOUND:**
  - The issue route returns the certification's id only after `saveCertification` (`certifications.ts` 763), so any client can act on it within about a second.
  - From then on, a lifecycle event by the issuer's organisation (P3, `documents.ts` 1462-1520 via 2563/2983/3089/3216) can, since 8cbadd8d4, replace the stored payload. The replacement has the same `documentId` and `hash`, and its `certId` defaults to `documentId`.
  - Its `timestamp` is the event's arrival time. If that is under 10 s after `certified_at`, it is INSIDE the window, and `created_at` keeps the issue's time.
  - DESIGN 2.4 E2 says "a replaced payload (P3) carries the event's time, which falls outside that window". That is not always true.
- **TESTED:** fixture `W_EVENT_IN_WINDOW`: the payload was replaced 6 s after issue, with `issuerOrgId` dropped and everything else as an event sends it. Verdict: WRITE (`pt_minus_certified_ms=6000`).
- **Impact:** the transaction that confirmed is the event's. It still attests this certification's id and content hash on chain, so "anchored = confirmed on chain" is true. Only the design's stronger claim ("carried the create's payload") is false.
- **Possible tightener:** require the issue's own `secuura.issuerOrgId` to be present. The issue POST always sends it (`certifications.ts` 678); a lifecycle POST does not, unless the KS-1385 (b) merge keeps the issuer fields. That makes it a heuristic only.

### G421-5 (Low): the builder's "equivalent by construction" terms are not equivalent
- **FOUND and TESTED** (`_work/g421/equiv_cc.sh`, `_work/out/equiv_cc.txt`): a concurrent writer changed ONLY `external_id`, or ONLY `tenant_id`, on W_BASE while apply waited on its row lock. Apply was run with expected=20.

| script | writer changed external_id | writer changed tenant_id |
|---|---|---|
| real | rc 3, written=19, ROLLED_BACK | rc 3, written=19, ROLLED_BACK |
| tenant term removed | rolls back | **rc 0, written=20, COMMITTED**: a row that moved tenant is written |
| external_id term removed | **rc 0, written=20, COMMITTED**: a row that became a lineage document is written | rolls back |

- The code at the head is right. The gap is that no cell pins either term, so a later edit could drop them silently.
- The dry run's READ ONLY (mutant E) changed nothing observable, so it is equivalent today; it only defends against a future edit.

### G421-6 (Low): a timestamp that passes the regex but is impossible aborts the whole run for the box
- **FOUND:** the strict regex (`.sql` 178 and 301) accepts `2026-02-30T00:00:00Z`, `2026-13-01T…`, `T25:00:00Z` and `0000-01-01…`, and the cast then raises.
- **TESTED:** each of these four, placed on one REFUSE row's anchor, made the whole dry run fail with rc 3 (`date/time field value out of range`). Apply would fail the same way, before any write. `T24:00:00Z` is accepted by Postgres and the run is unaffected.
- **Impact:** it fails closed, but one bad stored payload anywhere in the class blocks the repair of every row on the box. DESIGN 3.2 says "a malformed one refuses, never raises", which is not quite true.
- Anchoring stamps timestamps with `toISOString()`, so the product never produces one of these.

### G421-7 (Note): stored text is printed raw into the sentinel lines
- An anchorId containing a space shifts the ROW line's fields: `anchor= g421_R_AID_SPACE` broke my own awk parse.
- An anchorId containing a newline forges a line. Tested: a stored anchorId of `zz\nKS2366_REPAIR_SUMMARY mode=dry stuck_class=1 write=0 refuse=0 live=0` printed a fake SUMMARY line at line 11, ahead of the real one at line 57.
- A1 still protects apply: the real written count must equal `expected`. A seat should read the LAST SUMMARY line, or the dry run should quote its values (for example with `to_json`). The product never writes such an anchorId.

### G421-8 (Note): the census corrections, and what is outside the predicate's reach
- **The census corrections** (table below):
  - P5 at `anchors.ts` 269 refuses a document that already has an anchor row (`anchorExistsInDb`, 117-126). That check fails OPEN on a DB error.
  - P5 at 384 mints a fresh uuid (393).
  - The demo-service seed (`seed/generators/anchors.ts`) and the legacy copy (`docker/init/06-consolidate-anchors.sql` 62; `deployment/azure/migrate/init.sql` 2104) insert confirmed 64-hex single rows with NO `metadata_payload`. E1 refuses them; the seed's documents also carry `certification_metadata '{}'`, so they are outside the class too.
- **Other notes:**
  - A `W_DOCUMENT_SHAPED` row (document_type pdf, status anchored, external_id NULL, with a certificationType) is written. The class predicate cannot tell it from a certification, but its anchor evidence is as strong as any other row's.
  - `anchor_store.simulated` NULL passes (`IS NOT TRUE`), which matches the product's truthy test.
  - The apply reads `anchor_store` from its statement snapshot and does not lock it. An anchor reset that commits during the apply does not stop the write. The evidence that was read was a confirmation that had already happened, so this is safe.

## Caller census (mine, re-derived from the code at head) beside DESIGN 2.1

| # | path (file:line at head) | documentId posted | can it change an EXISTING certification's anchor row? | DESIGN 2.1 |
|---|---|---|---|---|
| 1 | originate `routes/certifications.ts` 669 (issue), id from 475 | fresh uuid | no: this is the create | P1, agrees |
| 2 | `certifications.ts` 1606 (recertify), `newCertId` 1591; no timeout | fresh uuid | no | P2, agrees |
| 3 | `documents.ts` `emitLifecycleAnchor` 1462-1520, called at 2563/2983/3089/3216; `getDocument` falls back to the PK, `documentRepo.ts` 250-257 | the URL id | YES: resets status and tx; the payload is replaced only via the KS-1385 guard (index.ts 1638-1659) | P3, agrees |
| 4 | `documents.ts` 931 (create), 1776 (re-anchor) | own id / URL id | create no; re-anchor yes for an in-flight row | P4, agrees |
| 5a | `anchors.ts` 269 (flat) | caller-supplied | only if no anchor row exists, or `anchorExistsInDb` fails open on a DB error | P5 says "yes": overstated |
| 5b | `anchors.ts` 384 (submit) | fresh uuid (393) | no | P5 says "caller-supplied": wrong |
| 6 | gateway `proxy.ts` 996-1006, `POST /api/anchors` and `/batch` direct to anchoring | caller-supplied | single: yes for a same-tenant caller (`mayWriteAnchorRows`, guard 536); batch: no, minted `anchor_<uuid>_<i>` ids | P6, agrees |
| 7 | anchoring retry, reconciler and re-poll: `index.ts` 2046-2055; `anchorSubmission.ts` 775; `reconciler.ts` 200-215 (adopts a chain tx whose payload equals the STORED one) and 300-330 (guarded); `anchorSubmission.ts` 605-629 re-poll confirm (UNGUARDED: the 2.2 b race) | the row's own | rebuilds from the stored payload | P7, agrees |
| 8 | anchoring DEMO_MODE `MockAnchoringProvider` (`cardano/index.ts` 270-273) | the row's own | confirms the row with a bare 64-hex hash and no chain | **MISSING** (G421-1) |
| 9 | demo-service seed `seed/generators/anchors.ts`, `seed/index.ts` 162 | the seeded doc | inserts confirmed, `mockTxHash` 64-hex, payload NULL | **MISSING** (refused by E1) |
| 10 | `docker/init/06-consolidate-anchors.sql` 62, `azure/migrate/init.sql` 2104 (from `blockchain_anchors`) | legacy | inserts with no payload | **MISSING** (refused by E1) |
| - | `thread-mint` 1104, `own-create` 946, `/api/anchors/verify` 1301, `/api/anchoring/submit` 1380 | - | no anchor_store write found (read of the handlers) | - |

**2.2, checked:**
- **2.2 a holds** at the head (`processAnchorDriven` reads by id, then `submitAnchorToChain` builds from `current.metadataPayload`). It also holds at c50d033c6 (`processAnchor` 1512-1530 reads via `dbGetAnchorById` and submits `anchor.metadataPayload`; the upsert at 1242 never sets `metadata_payload`, so the payload was write-once then) and at 8cbadd8d4 (the CASE at 1424).
- **2.2 b, the race:** the re-poll confirm write is unguarded, so a row can read confirmed beside a newer payload. Only an in-window payload passes the window test (G421-4). I found no route that confirms a row while its stored payload is the create's but the confirmed transaction carried a different payload. A payload is only ever replaced by a newer, server-stamped one; it never reverts.
- **2.2 c holds** (batch ids are minted).
- **2.2 d holds:** `content_hash` is never in the SET list (head 1590-1601; c50 1243-1253).
- **2.2 e holds:** there is no `id` in the SET list.

**Bound for Platform S in K:** only 6 (or 5a): `mayWriteAnchorRows` refuses another tenant's id, and the payload is replaced only on owner plus same hash plus same type (`anchorOverwriteGuard.ts` 350 and 536). The S repository was not searched by me either.

**E2, checked:**
- `certified_at` is the route's own `now`, minted before the POST: 476, then `issuedAt: now` 602, then INSERT `certified_at` (`certificationRepo.ts` 266). The ON CONFLICT never updates it (272-276).
- The issue route has a 10 s timeout (687). Recertify has none (1606), so a slow recertify is refused, which is safe.
- The lineage and legacy-certify paths write rows with `external_id`, which the class excludes (`certifications.ts` 880-893 matches `external_id = …`).
- Anchoring stamps on arrival (`index.ts` 514-515).
- The window is TimeZone-invariant: all four columns are `timestamptz`, and verdicts were identical in UTC, Pacific/Kiritimati, America/Adak, Australia/Sydney and UTC+12.
- Clock difference: containers on one VM share the host clock. On a multi-host deployment, skew would only shift legitimate rows out of the window (refused), unless it were as large as an event's delay.

## Predicate table (my fixtures, `_work/g421/fx.sql`; measured verdicts from `_work/out/g_dry_utc.out`)

| term | my violating fixture | verdict (refuse reason) | neighbour that satisfies it | builder cell that pins it |
|---|---|---|---|---|
| external_id IS NULL | U_EXTERNAL | unlisted, untouched | W_BASE WRITE | O_LINEAGE (R1/R8) |
| certificationType set | U_NO_CTYPE; U_CTYPE_JSONNULL | unlisted (both) | W_BASE | O_NOT_CERT |
| blob is an object | U_BLOB_ARRAY; U_BLOB_STRING | unlisted (both) | W_CM_BLOB_JSONNULL (falls back to the metadata copy) WRITE | none (my mutants: none needed) |
| anchoringStatus = 'submitted' | U_AS_CASE ('Submitted') | unlisted | W_BASE | O_ANCHORING_FAILED |
| status absent or JSON null | U_STATUS_STRNULL ("null"); U_STATUS_CONFIRMED | unlisted (both) | W_STATUS_JSONNULL WRITE | O_STATUS_*; gate mutant G:class_status_strnull SURVIVES the builder suite |
| txHash absent or null | U_TX_EMPTY ("") | unlisted | W_TX_ABSENT WRITE | O_TXHASH |
| no createAttempts | L_CA_JSONNULL (`createAttempts: null`) | LIVE | W_BASE | N_LIVE |
| anchoredAt null | R_ANCHOREDAT_STRNULL ("null") | REFUSE blob_anchoredAt_set | W_ANCHOREDAT_ABSENT WRITE | N_ANCHOREDAT |
| blob not simulated | R_SIM_TRUE, R_SIM_STR_TRUE, R_SIM_ONE, R_SIM_STR_FALSE, R_SIM_ZERO | REFUSE blob_simulated (each) | W_SIM_FALSE, W_SIM_NULL WRITE | N_BLOB_SIM_*; 0 is not pinned (G:blob_sim_zero_ok survives the builder suite) |
| anchorId a non-empty string, exact | R_AID_EMPTY (blob_anchorId_not_a_string); R_AID_SPACE, R_AID_CASE (no_anchor_row and every row term) | REFUSE | W_BASE | N_ANCHORID_NUM; case is not pinned (G:anchorid_join_ci survives) |
| same row (document_id) | R_DOCID_UPPER; R_FOREIGN_ANCHOR (another certification's anchor) | REFUSE row_names_another_document (+ hash/window terms for the foreign one) | W_BASE | N_OTHER_DOC |
| row confirmed | R_STATUS_UPPER ('CONFIRMED'); R_DEMO_FAILED_ONLY | REFUSE row_not_confirmed | W_BASE | N_ROW_SUBMITTED |
| row not simulated | R_DEMO_SIM_ONLY | REFUSE row_simulated | W_ROW_SIM_NULL WRITE | N_ROW_SIM |
| tx 64-hex | R_TX_0X, R_TX_NEWLINE, R_DEMO_MOCKTX_ONLY | REFUSE row_tx_not_64_hex | W_TX_UPPER WRITE | N_TX_PREFIX, N_TX_63 |
| single, no merkle | R_TYPE_UPPER ('SINGLE'); R_MERKLE_EMPTY ('') | REFUSE row_not_single | W_BASE | N_BATCH_TYPE, N_MERKLE |
| content hash (normalised) | R_ROWHASH_SPACE | REFUSE row_content_hash_differs | W_HASH_PREFIX_ROW, W_HASH_PREFIX_CERT WRITE | N_ROW_HASH; normalisation is not pinned (G:rowhash_no_lower survives) |
| payload is an object | R_SECUURA_ARRAY; R_PAYLOAD_NULL | REFUSE payload_without_secuura, …, malformed, outside | - | N_NO_SECUURA |
| payload documentId | R_PAYDOC_UPPER | REFUSE payload_names_another_document | W_BASE | N_PAYLOAD_DOC |
| payload hash | (covered by R_FOREIGN_ANCHOR) | REFUSE payload_hash_differs | W_PAYHASH_PREFIX WRITE | N_PAYLOAD_HASH |
| timestamp format | R_TS_PLUS0000, R_TS_PLUS1100, R_TS_7FRAC, R_TS_LOWER_Z | REFUSE payload_timestamp_malformed, outside | W_TS_NOFRAC WRITE | N_TS_MALFORMED; offsets are not pinned (G:ts_regex_offsets survives) |
| payload in window | R_TS_HIGH_PLUS_1US (+10.000001 s), R_TS_LOW_MINUS_1US, R_EVENT_OUTSIDE (+10.5 s), R_CERTIFIED_NULL | REFUSE payload_timestamp_outside_issue_window | W_TS_LOWEDGE (+0), W_TS_HIGHEDGE_US (+10.000000 s) WRITE; W_EVENT_IN_WINDOW (+6 s) WRITE (G421-4) | N_TS_LATE (11 s), N_TS_EARLY, EDGE; +10.5 s is not pinned (G:pt_upper_half_s survives) |
| created_at in window | R_CREATED_HIGH_PLUS_1US | REFUSE row_created_outside_issue_window | W_TS_LOWEDGE | N_CREATED_LATE, N_CREATED_EARLY |
| demo failed+simulated, all three terms | R_DEMO_ALL3 | REFUSE row_not_confirmed, row_simulated, row_tx_not_64_hex; **each term proven independently** by the three *_ONLY rows above | - | D37 |
| revoked / expired | W_REVOKED, W_EXPIRED | WRITE, status column kept (revoked/expired), expired=true flagged | - | R01, E01 |

Totals (my dry run, UTC): stuck_class=54, write=20, refuse=33, live=1. 9 rows are outside the class and unlisted. **No row in my set was written that should not be**, except the two rows the design cannot tell apart (G421-1 mock shape, G421-4 in-window event); both are explained above.

## Re-runs (my clone; each rc read from its own command)

| stage | head | develop (+3 test files) |
|---|---|---|
| new suite | 65/65, rc 0, 7 s (also 65/65 under `/bin/bash` 3.2.57, and inside run-shell-suites) | rc 1: `repair script not found`, 0 passed, 1 failed. **Red by absence**, an honest label. No behavioural red exists anywhere: the product code is identical (0 service files in the diff). The REAL honest rule reads false on all 20 of my WRITE fixtures on both arms; R6 equals confirmedBlobOf 20/20 on the develop tree too. |
| new suite x20 (R10 flake check) | 20 runs, 20 rc 0, R10 ok 20/20, 0 flakes | - |
| run-shell-suites.sh WHOLE | 133 passed, 0 failed, 1 SKIPPED (of 134), rc 0. The skip is `preflight_test_types_ratchet_leg`: nested `@types/node` absent in my copied node_modules (environmental, not this PR) | not run (no service change; the builder's A arm reads 133/134, the new suite only) |
| originate tsc --noEmit | rc 0 (plant control: rc 2, 1 TS error, file moved out, tree porcelain 0) | identical by diff |
| originate jest WHOLE | 251 suites, 3770/3770, rc 0, 49.9 s | identical by diff |
| packages/shared vitest WHOLE | 1747: 1746 passed, 1 failed (KS-278 wallet-signature) | identical by diff |
| docs-fragments check | OK, 323 new entries per page; 2 ADVISORY lines | OK, 322; the same 2 ADVISORY lines |
| portability rules on the suite | a copy outside `__tests__`: OK, 7 rules hold (rc 0); a planted `readarray` gives rc 1. The real `__tests__` dir is skipped: the guard says "No shell scripts found … vacuous" (rc 2). **The builder's correction is confirmed.** | - |

**Shells:** bash 3.2.57 (`/bin/bash`, also the `bash` on PATH) ran the suite green. The documented `sh -c` invocation ran under macOS `/bin/sh`, but not under the box container's sh (NOT TESTED).

## Mutants

Instrument: `_work/g421/mut_g421.py`, results in `_work/out/mutants_g421_run1.json` and `mutants_g421_only.json`.

How each mutant was run:
1. It is one counted edit on a copy.
2. A probe follows: dry, apply and reverse must each reach their SUMMARY line. A parse failure is not a kill.
3. Two judges then run: (A) the builder's suite through its seam, and (B) my fixtures (a verdict diff against the real script, apply expected=19 and =20, a reverse after an updated_at-only touch, and the no-mode run).

The real file's sha256 stayed unchanged throughout.

| mutant | builder suite | gate fixtures |
|---|---|---|
| B: p_row_confirmed / p_row_not_simulated / p_row_tx64 / p_same_row / p_payload_names_cert / window_pt_upper / window_created_lower / class_external_id / apply_unchanged_guard / apply_count_guard / reverse_cas_guard / default_mode / blob_block_zero (13) | **13 KILLED, each by its NAMED cell** (N_ROW_SUBMITTED, N_ROW_SIM, N_TX_PREFIX, N_OTHER_DOC, N_PAYLOAD_DOC, N_TS_LATE, N_CREATED_EARLY, O_* listed, R10, A1, R5, R9, R2 values) | 10 killed |
| G: tx_unanchored, created_upper_1ms, count_ge, default_mode_reverse, anchoredat_no_ms2 | KILLED | KILLED |
| G: class_status_strnull, blob_sim_zero_ok, anchorid_join_ci, rowhash_no_lower, paydoc_ci, pt_upper_half_s, ts_regex_offsets, reverse_cas_no_updated_at | **SURVIVED** (8) | KILLED |
| G: blob_network_const (`network` written as the constant 'preview') | **SURVIVED** | **SURVIVED**. Every fixture on both sides uses network 'preview'; R6 cannot see it |
| E: apply_tenant_term, apply_external_id_term | survived | survived as a static check; **observable under a concurrent writer** (G421-5) |
| E: dry_read_only | survived | survived; equivalent today |

Result: 30 mutants. Of my 14, 13 were killed by my fixtures but only 5 by the builder's suite. The builder's suite has gaps on normalisation, case, sim 0, timestamp offsets, a +0.5 s window, `status:"null"`, the updated_at part of reverse's CAS, and network. None of these is a code defect at the head.

## NOT TESTED (listed, not attempted)

- Any box (Kintsugi, demo, production); whether `ANCHORING_DEMO_MODE` was ever true on Kintsugi or demo (G421-1).
- The real anchoring service; a chain lookup of any transaction; demo's order of deploy and repair (Kam's and Stuart's, a later card).
- The verify ROUTE end to end over HTTP. I drove the real `isAnchoredHonestly(presentBlockchainHonestly(blob))` and `certificationAnchorInFlight` over tsx instead:
  - repaired rows: in-flight 0 of 20, so **G420-1's re-reads stop for repaired rows**;
  - the 43 non-written rows: honest false on 43 of 43.

  What a later reader sees on a repaired row: `metadata` gains `blockchain`, `updated_at` moves, no `createAttempts`. That matches what the live writer produces for a legacy blob. The stale reconcile does not run for it, because it is no longer in flight.
- The box container's `sh` and psql version; `docker exec` itself.
- Platform S's repository (unsearched by anyone).
- Pre-push legs 3, 4 and 8; the four platform suites; eslint (no TS product file changed).
- The builder's other 27 mutants.

## Process disclosures

- In one command (the urllib fetch of the PR JSON) I wrote `gh auth token 2>/dev/null`. That discarded the stderr of the token lookup, against the rule. The call succeeded (the body was read) and nothing else was affected.
- No `cd`, no `rm`, no shell word starting with `=`. The tsc plant file was MOVED to `_work/moved/`.
- I created databases on my own cluster and dropped them there. Nothing outside my cluster was touched.
- My Postgres (`/private/tmp/g421/pg`, socket only) was stopped at 15:42 AEDT (`pg_ctl stop` rc 0). After that, 0 processes reference `/private/tmp/g421` and 0 processes match ks2366 or g421. The data directory is kept.
- I only read the builder's trees and cluster. node_modules were copied out of `s-w78-fix` with `cp -c`, and no postgres of the builder's was running or touched.
- Nothing was pushed, commented, written to Linear or GitHub, merged or deployed.
- I wrote only inside this gate folder (plus scratch logs under `/private/tmp/g421`).
