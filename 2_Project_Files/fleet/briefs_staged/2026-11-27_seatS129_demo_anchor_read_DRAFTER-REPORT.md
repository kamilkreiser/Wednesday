# DRAFTER-REPORT: Seat S 129th brief (demo anchor read), 2026-11-27

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_seatS129_demo_anchor_read.md
Touched: no box, no ssh, no keyscan, no mail, no post. One throwaway PostgreSQL 15 in the drafter's scratchpad (local socket, synthetic data) to prove the SQL parses and joins; stopped afterwards.

## COMMISSION FACTS I MEASURED AS WRONG
None materially wrong. What I checked, and three places where the commission's wording needed care:
- Checked and TRUE: S 128th wrapped today (history.md top entry; ordinals 129th 0, 128th 1, 127th 1, 126th 1); 37 stuck of 37; census 296 / 11 / 83; role row `on|secuura|t|t|f` = rolsuper t, rolbypassrls t; scan equalled the pin at 2026-11-27T00:29:30Z; REVISION head `d4ffc8308249`, anchoring image `0f2b322518fe`; S 128th's answer_plan and answer_wrap rulings F1 to F5.
- Ruling time: the live-board row is stamped 11:43:55.646+11:00 (matches "11:43:55 AEDT"); the STORE's `ruled_ts` is 11:44:49.881596+11:00. Not an error, but the brief quotes both so nobody "corrects" one to the other.
- "W 77th's finding suggests there may be NO reliable link": W 77th's finding (q_plan line 28) is about the RESOLVER's `isBoundToCreate` rule (createAttempts or anchoredAt within 2 ms), not about the absence of an id link. Old certification blobs do carry `anchorId`, and the certification id equals `anchor_store.document_id`. So the brief takes the "link exists" branch, with the no-link fallback kept as 5.8.
- "Read the repo at the commit demo runs": `d4ffc8308249` (and `eb27110fc6e4`, `4764b2cfbc28`, `918f5e6d312a`) are NOT objects in the local repo (`git cat-file -t` fails). Nearest state used and named: develop `0e6479d7b6c0` (2026-11-10), plus AA 8th's saved copy of anchoring at `eb27110fc6e4`, plus commit `c50d033c6` (2026-07-30) to show the same code existed the day before the oldest stuck row. Local develop is also older than PR 2295's merge.

## THE LINK (established; commit read: 0e6479d7b6c0, nearest state; unvalidated on demo's exact commit)
Paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/.
1. Certification id and anchor request: `services/originate/src/routes/certifications.ts` line 423 `const id = uuidv4()`; lines 618-619 body `documentId: id`, `certId: id`.
2. Key in the blob: line 633 `upstreamAnchorId = j?.data?.id || null`; `buildCertification` lines 538-562, `anchorId` at 557, `txHash: null` 558, `anchoringStatus` 562. Written into `documents.certification_metadata` by `services/originate/src/repositories/certificationRepo.ts` `insertCertificationRow` (function line 223, `blockchain: cert.blockchain` line 234, row id `${cert.id}::uuid` line 255).
3. Same code the day before the oldest stuck row: commit `c50d033c6` (2026-07-30) certifications.ts lines 389, 402, 437 (`documentId: id`, `upstreamAnchorId = j?.data?.id`, `anchorId: upstreamAnchorId`); first appearance of `upstreamAnchorId` is 2026-04-27 (`18306248b`).
4. Anchor row: anchoring returns `id: persistedId` (saved copy 5_Project_History/2026-11-25_seatAA-8th/evidence/src_eb27110fc6e4_anchoring_index.ts line 593; `RETURNING id`, comments at 1548, 1666); upsert `ON CONFLICT (document_id, network)` line 1590. Migration 050 lines 4-6 state "a certification's anchors send its `id`".
5. Two keys: K1 `blob->>'anchorId' = anchor_store.id`; K2 `documents.id::text = anchor_store.document_id`.
6. "Confirmed on chain": status `confirmed`, `simulated` not true, `transaction_hash` 64-hex. Sources: saved copy line 1033 (`verified: !txView.simulated && anchor.status === 'confirmed'`), honestAnchor.ts lines 17 and 33 (fabricated prefixes), saved copy 1842 ("only a 64-hex ref is a REAL chain transaction"), gate 420 verdict line 10; mock path sets `confirmed` with a `mock_tx_` hash (saved copy 2072, 2086).
Limits (in the brief, section 1 and 7): one row per (document_id, network), a re-anchor overwrites in place, so a match says "this certification's anchor row confirmed", not "this exact create confirmed"; lineage documents have their own rows keyed to the certification id (W 77th q_plan line 74); `anchor_store` has no tenant column.

## EVERY FACT IN THE BRIEF
| fact | source | read today? |
|---|---|---|
| Kam ruled a, live row 11:43:55.646+11:00 | kam_msgs.sh 12 --source live (command read) | yes |
| store ruled_ts 11:44:49.881596+11:00; option a detail; default b | decision_queue.sh show secuura-ks2366-stuck-certs-anchor-read-demo-1127 (command read) | yes |
| 37 stuck of 37, two tenants, oldest 2026-07-31, newest 2026-11-26, createAttempts 0 of 37 | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_S128_status_number.txt | yes |
| 3a `on|secuura|t|t|f`, census 296/11/83, documents 276 hash 6b7c8262..., 155 confirmed document rows, schema guard 5 | same file, raw output | yes |
| box time of the count 00:29:55Z to 00:29:56Z (used as the `created_after_s128_count` literal) | /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-27_seatS-128th/evidence/R3_cnt.out and the status file | yes |
| pin, scan equal 00:29:30Z, throwaway-key control | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_S128_status_keyscan.txt | yes |
| identity expectations (d4ffc8308249, 0f2b322518fe, 2026-11-16T23:55:34Z, secuura-postgres) | S128_status_number.txt; S 128th tools/demo_id_s128.sh | yes |
| rulings F1 to F5, census STOP, role correction | 2026-11-27_S128_answer_plan.md, 2026-11-27_S128_answer_wrap.md | yes |
| kit sha256 and sizes (demo_run b7b54101..., hostkey 98738455..., id 615d66d4..., am 89c048ed..., cnt e8aa4d10..., rekey f42c794e...) | shasum -a 256 over S 128th's tools folder (matches its DECLARED.md) | yes |
| re-key token counts (run s128 x3, REC 1, scratchpad id 1; hostkey s128 x7, REC 1, id 1; am 1, 4, 4; id tool 1, 1; cnt frame lines 1-50: s128 x4, S 128th x1, 285 x2) | counting script over the same files (non-history lines) | yes |
| predicate (demo_cnt_s128.sh lines 91-98; blob expression S 127th box_cnt_s127.sh line 48) | those files | yes (line numbers: 88 `read -r -d '' Q4`, 97-98 the WHERE) |
| frame line ranges of demo_cnt_s128.sh (1-50 kept, 26 bsum, 52-125 replaced) | the file | yes |
| anchor_store and documents column lines | git show 0e6479d7b6c0 of the migrations | yes |
| commit objects d4ffc8308249 etc. absent locally | git cat-file -t (command read) | yes |
| anchor columns present on demo (AA 8th header row) | 5_Project_History/2026-11-25_seatAA-8th/evidence/R2b_rows.out line 13 | yes |
| W 77th finding, lineage documents | 2026-11-26_W77_q_plan.txt lines 28, 44-45, 74 | yes |
| gate 420 "64-hex hash" | gate420 verdict.md line 10 | yes |
| S 128th rulings on role, ordinals, Seat D 88th note | S128 answer files; history.md | yes |
| SELECTs parse and join | local throwaway PostgreSQL 15.19, synthetic data | yes |
| model line claude-sonnet-5-5 | models_latest.json (per S 128th's brief, not re-read by me) | carried |
| Seat D 88th may be live | commission and S 128th's brief W6 | carried, not measured |
| demo box state, whether anything moved | n/a | NOT read (no box contact) |

## SQL COLUMNS: VALIDATED or UNVALIDATED
Source for all: migrations at `0e6479d7b6c0` under Blockchain/Dev/migrations/.
- documents.id UUID: VALIDATED 001_initial-schema.sql:95; also used by S 128th's hash statement on demo (`order by d.id`).
- documents.external_id VARCHAR: VALIDATED 001:96; demo-guarded by S 128th (4.2 read 5).
- documents.tenant_id UUID: VALIDATED 011_documents_tenant_id.sql:85; demo-guarded by S 128th.
- documents.metadata JSONB: VALIDATED 001:109; demo-guarded. documents.certification_metadata JSONB: VALIDATED 001:110; demo-guarded.
- documents.created_at TIMESTAMPTZ: VALIDATED 001:111; demo-guarded.
- anchor_store.id TEXT PK: VALIDATED 001:705. document_id TEXT: 001:706. status TEXT: 001:714. transaction_hash TEXT: 001:715. simulated BOOLEAN: 001:724. created_at TIMESTAMPTZ: 001:725. All also appear in AA 8th's demo output header (R2b_rows.out:13) except that file does not prove data types.
- Blob keys `anchorId`, `anchoringStatus`, `status`, `txHash`, `createAttempts`: `anchorId`, `anchoringStatus`, `txHash` VALIDATED in source (certifications.ts 554-562); `status` and `anchoringStatus` blob keys also read on demo through S 128th's predicate (37 rows matched); `createAttempts` still never seen in a blob (S 128th read 0 of 37; UNVALIDATED key name, used only as a presence count).
- No unvalidated column name is used. The guard (5.1) re-checks 12 names and 10 data types on the box and fails closed.

## NOT MEASURED
Anything on demo (no contact): whether the blobs carry `anchorId`, shape of anchor ids and document ids, data types, whether the 37 moved. The demo commit's own source (objects absent). Whether lineage documents share anchor rows with certifications (taken from W 77th's plan, not from data). Seat D 88th's liveness.

## QUESTIONS FOR WEDNESDAY
1. Census STOP on any non-final `anchor_store` bucket (your S 128th ruling R3) can fire on a transient `pending` or `submitted` row of a brand-new demo certification and cost a round trip; keep it as ruled, or report-and-continue for non-final buckets this round?
2. F4: this round runs no bucket statement, so the SQL carries no uuid literal and the brief allows NO uuid-shaped string. Confirm that dropping S 128th's single-constant exemption is wanted.
3. Pin acceptance: the brief carries your S 128th W1 condition (fingerprint equals the pin and address 20.212.118.59) through R1. Confirm it extends to this read, or add a different gate.
4. A total below 37 is written as a STOP; above 37 is reported with `created_after_s128_count` and continues. Agree?
5. Positive control: `doc_rows >= 155` and `match_by_external_id > 0` pass; `match_by_anchorid` is reported only. If you want a hard floor on the document-side anchorId match, say so.
