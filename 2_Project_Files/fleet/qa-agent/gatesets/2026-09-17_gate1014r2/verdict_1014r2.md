matches 1
=====MSG 2026-09-16T22:38:54.000Z {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'} chars 13467
QA -> Wednesday — TIER 1 GATE #1014 ROUND 2 of 2 (KS-1176) — composed 2026-09-17 08:38:52 AEST (clock from `date`)

VERDICT: GO WITH FINDINGS on 9ba0caf78b8ddb737541df38303b776c982521d2, as the delta over round-1 head 616c766a5 and base e0f41a8fa, AND on the merged tree 5748a1d68318ed2e310a360fb79e7a1ebc63c785 = head + develop 7e89318bcedbc9a35757d4298ace54a6a23020bd (#1016's squash; develop unchanged 08:22:19 -> 08:36:38).

Report: /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1176-1014r2-9ba0caf78-tier1-r2/report.md (evidence/ beside it; NOT-TESTED.written-first.md written 08:22, before any run)

== BLUF ==
- F-1 CLOSED for well-formed (array) allow-lists at the gateway, for every spelling.
  - 0 admitted disallowed types on head and merged over 3 array configs x 59 body shapes; the same census shows 32 at r1 and 32 under TF.
  - Every allow-list refusal ran with enforcement 0 / workflow 0 / forwarded 0 (151 on head).
  - Allow-list vs enforcement key: 0 mismatches on head (94 at r1 and base; 31 under G-REV).
- Level axis unchanged since round 1: r1->head 32 create diffs, all F-1 closures; 0 verify diffs; 0 pure flips; oracle mismatches 0.
- Tampers exact: seat 0/1/4/4/9/1/0; gate G-F3CTRL 1, G-REV 0, G-BOTH 2. tsc rc 0, 49/428, pending 0, restores sha-identical on every row.
- No Blocker. New, all TICKET class:
  - N-1 Major, pre-existing (served `data.documentType` unchecked);
  - N-2 Minor (a STRING allow-list substring-matches; #1014's level change admits DOCUMENT);
  - N-3 Minor (no cell pins both-present precedence);
  - N-4 Minor, pre-existing (an untyped body from a restricted connector is stored as DOCUMENT).
- Round-2 cap: the F-1 closure SHIPS WITH #1014; the residue is TICKET.

== Plain statements, items 1-11 ==

(1) F-1 per spelling class — MEASURED AT RUNTIME.
- Instrument:
  - the real index.ts app + real redis fallback + real admin seed route;
  - hit counters via vi.mock('../services/enforcement', importOriginal);
  - a body-read Proxy probe on the REAL enforceDocumentTypeRules;
  - 8 principals x 59 shapes = 472 rows/tree.
- Array allow-lists, disallowed types admitted: base 0 / r1 32 / head 0 / merged 0; TF 32; G-REV 4; G-BOTH 47.
- With the STRING config: 0 / 47 / 11 / 11.
- Classes at head:
  - `type`: SSD / PROPERTY_DEED / approval / REFERENCE / unregistered / case variants / ids / whitespace / tab / ZWSP / 123 / arrays -> 403 FORBIDDEN naming the value, enf 0 / wf 0 / fwd 0.
  - Both present, disagreeing, either key order: `documentType` wins at both layers.
  - `documentType` ''/null/false/0 + `type:SSD`: 201 at r1 -> 403 at head.
  - Duplicate `type` (last wins SSD) and the JSON-escaped key `typ\u0065`: 201 at r1 -> 403 at head.
  - Ignored keys / `__proto__` / untyped: untyped 201 on all trees.
- Legitimate shapes S1-S9: all as expected. S10 (`type:'document'`) is 403 fail-closed: RECORD R-10.
- Unrestricted sk_, the Bearer JWT, the NONE human and the empty array: 0 diffs r1->head. The empty array = unrestricted on 59/59.
- Layer judged: the gateway (enforcement's resolved type on an admitted request). No restricted array-config connector got a disallowed type at that layer on head or merged.
- Originate layer (READ ONLY): N-1 and N-4.
- Oracle planted controls (V1 plant, clean refusal, two same-key plants): all True.
- On the drafter's own 7x55 universe my rows reproduce every drafter count exactly.

(2) Level axis vs round 1 — round 1's harness (sha be59a3ae8272) and oracle (sha f9a4b8435c0f) verbatim on base / r1 / head / merged.
- base->head 674 = 661 PERMITTED + 13 refusal-code changes, all sk_restricted_DOCUMENT x `type` -> 403 FORBIDDEN (incl. QA_TYPO / QA_NONE_SPACE 201->403).
- r1->head: 32 diffs = 32 F-1-CLOSED under my amended oracle; findings 0; verify diffs 0 (:557 region byte-identical on all 5 trees); pure flips 0; admissions above none 0; known-level changes 0.
- head->merged 0/0/0.
- Planted: an F-1-class ADMISSION flagged True; a FORBIDDEN F-1 row not flagged True; a known-level change flagged True.
- F-2 reproduces (real app 201x5 at r1/head/merged, 403x5 at base; control 200,200,429,429,429).
- F-3 reproduces (same_id True on base and head).
- F-4 identical on all trees (500x124, verify timeout x22).

(3) Precedence and same key — MEASURED.
- Real enforcement reads `documentType`, and `type` only when `documentType` is falsy.
- The allow-list's 403 names exactly that value on every refusal, and every admission passes membership for it. Head: same 204 + falsy 32, mismatch 0. The instrument fires on base/r1 (94) and G-REV (31).
- Duplicate keys are last-wins at the gateway; the forwarded body is byte-identical. Originate uses express.json (READ).
- Originate persists/serves a type neither checked (READ ONLY): the untyped default DOCUMENT (:565) = N-4; `data.documentType` served first (:311, :1053) and matched by the verify gate (:546) = N-1.

(4) Comment-only by parser.
- enforcement.ts r1 vs r2: printer (removeComments) equal True; scanner token stream equal True.
- Controls: type-only edit flagged; `>=`->`>` flagged; comment-only edit not flagged.
- The ks1176 header alone is comment-only (r1-with-r2-header == r1 on both instruments); the rest is describe-F code.
- R-c CLOSED.

(5) Tampers and red-before-green.
- T0 0 / TF 1 (F1) / TA 4 / TW 4 / TK 9 / TR 1 / TI 0 / G-F3CTRL 1 / G-REV 0 (no cell sees it = N-3) / G-BOTH 2 (F1, F2).
- Every row: anchor 1, marker 1, tsc rc 0, 49/428, pending 0, sha-restored. Project-tsc VOID control: a non-compiling plant gives rc 2.
- Census under TF = r1 exactly (0 diffs); under G-REV and G-BOTH it flips as above.
- Red before green: r2 test file in my r1 tree 18 run / 1 red (`expected 201 to be 403`); in my base tree 18 / 5 red.

(6) Including tsc and eslint.
- listFiles 584 / 585 / 585 / dev 588 / merged 589; the PR files are in the program.
- Errors 30/10 on base/r1/head; 31/11 on dev and merged. NEW in PR files 0 everywhere; NEW vs base 0 and vs r1 0.
- merged +1 = #1016's own ks1072 test TS18046, present on develop (a record for #1016).
- Plant TS2322 gives +1 at the plant; restored identical.
- eslint: enforcement.ts 0; ks1176 test 0; verification.ts 5 (4 no-unused-vars + 1 no-useless-assignment). The rule + message multisets are identical on base/r1/head/merged. The firing control fires (3 / 8).

(7) Merged tree.
- Merged tree 5748a1d68318ed2e310a360fb79e7a1ebc63c785 = merge-tree --write-tree in my clone (True; = drafter). My local merge commit is 9542c7158.
- Merged blobs: verification.ts 28fb58343, enforcement.ts be466fbf4, ks1176 test 43cebf8d7.
- Allow-list block head = merged (56aff647b4f2); verify gate identical on all 5 trees (3790b8286709).
- #1016's only verification.ts hunk is @@ -301 makeFetchDocFromAnchorStore.
- Suites (all pass, pending 0, tsc 0): base 48/410, r1 49/423, head 49/428, dev 52/424, merged 53/442.
- Items 1 and 2 ran on the merged tree: 0 row diffs vs head.

(8) Linear / GitHub.
- attachmentsForURL(pull/1014) = exactly KS-1176 `contributes`, read 08:27:00 and again 08:37:06.
- KS-1176 In Progress — it STAYS In Progress on merge (§5f).
- Closing phrases 0 in title, body, both commits and the comment (controls hit).
- KS-1187 named 0 times (control KS-1190 x6).
- At-mentions 0 in the seat's text; the linear[bot] comment's two regex hits are `@k-live` test tags.
- New since drafting: KS-1195 is In Progress with #1017 `contributes` (open).

(9) Schemathesis / Akto: NOT APPLICABLE (measured).
- DocumentCreateRequest declares documentType and data but NOT `type`; security is bearerAuth only; the 403 text names neither FORBIDDEN nor the allow-list.
- The change is reachable only under an sk_ key and an undeclared `type`, so a spec-driven run cannot reach it. Not run (NOT COMMISSIONED).

(10) Table below.

(11) Checkout bounds, 08:22:19 / 08:31:25 / 08:36:38.
- pull/1014/head 9ba0caf78 x3; develop 7e89318bc x3; pull/1016/head a226d94fe x3.
- porcelain 0; .git/config d7e7298b02c45f52... x3; worktrees 110 / list 111; branch feature/ks-597-b-caller-scoped-externalref @355d82c8b.
- api-gateway results.json 5907 b @01:02:02.
- .vite entries newer than my marker: 0 (control 9).
- for-each-ref 906 / 907 / 908: not written by this gate (read verbs only), consistent with #1017's refs.
- docker info rc:
0
- No container created or touched.

== CLOSED / STILL OPEN / NEW ==
- F-1: CLOSED (array allow-lists, every spelling, gateway layer; MEASURED head + merged). SHIPS WITH #1014.
- F-2 KS-1195: STILL OPEN (fix PR #1017 open). Major. TICKET.
- F-3 KS-1196: STILL OPEN. Minor. TICKET.
- F-4 KS-1197: STILL OPEN. Minor. TICKET.
- F-5 KS-1198: STILL OPEN — the Bearer connector JWT for c-restricted gets SSD_DOCUMENT and PROPERTY_DEED 201 where its sk_ key is 403. Minor. TICKET.
- N-1 NEW: served `data.documentType` unchecked. A document stored as an allowed type is served as a disallowed or above-rank type (untyped carrier `{"data":{"documentType":"DEGREE"}}` 201 for EVERY principal incl. the NONE human at base = head; #1014 adds typed carriers for connectors).
  - Class / severity: gateway MEASURED + originate READ ONLY. Major.
  - Disposition: TICKET + ESCALATION CANDIDATE. Not a Blocker against #1014 (pre-existing capability).
- N-2 NEW: `allowedDocumentTypes` stored as a STRING is a substring match; #1014's level change admits DOCUMENT (base 0 -> head 11 rows).
  - Needs an admin PUT /api/admin/settings with a non-array (verbatim merge, READ; portal types string[]).
  - Class / severity: MEASURED. Minor.
  - Disposition: TICKET; escalation candidate for consistency with the F-1 ruling only.
- N-3 NEW: G-REV (reversed precedence) reds 0/428 while the census admits {documentType: SSD_DOCUMENT, type: DOCUMENT} as SSD_DOCUMENT for a DOCUMENT-restricted connector.
  - Class / severity: MEASURED. Minor.
  - Disposition: SHIPS-WITH optional (owner's), else TICKET.
- N-4 STILL OPEN residue: an untyped body (and the ignored keys, `__proto__`, '' values) from an SSD-restricted connector is 201 and stored DOCUMENT (READ); 16 rows, base = head.
  - Class / severity: MEASURED + READ. Minor.
  - Disposition: TICKET.
- R-10 RECORD: the exact-match allow-list refuses case/id spellings enforcement would resolve (fail-closed; S10).
- R-c CLOSED by the reword.
- R-g extended: `type` absent from DocumentCreateRequest.
- R-a, R-b, R-d, R-e (reproduces), R-f, R-i carried.

== PREDICTION SLIPS ==
- None against the READY or the drafter on any measured count: tampers, suites, tsc, eslint, merged OID, blobs, all 6 disagreements; the drafter's 7x55 counts reproduce exactly.
- Instrument differences, not slips:
  - same-key firing counts (G-REV 31 mine / 8 drafter);
  - F-3 collides on base+head in my run vs merged in the drafter's (a ms race);
  - refs 905 -> 906..908;
  - .vite entry counts 3 vs 16;
  - region-hash anchors.
- READY F4 cannot see N-4.
- Self-audit: the item-4 parser run used a subshell `cd` into my own clone (a brief rule breach); no stray logs/, nothing touched in the checkout.

== MERGE ADDENDUM ==
squash `9ba0caf78` onto develop `7e89318bcedbc9a35757d4298ace54a6a23020bd` (= #1016's squash; merged tree `5748a1d68318ed2e310a360fb79e7a1ebc63c785`; #1016 landed first, #1014 merges second, judged by content against it — allow-list block and verify gate byte-identical on head and merged); #1014 attaches to KS-1176 only, linkKind `contributes` (read 08:37:06) — KS-1176 stays In Progress on merge (§5f: runtime behaviour — connector keys now create none-rank document types and a restricted connector's allow-list applies to `type`; the live Platform-S sweep is owed); KS-1187 not named; equality targets after the squash onto 7e89318bc: enforcement.ts blob `be466fbf4` / verification.ts blob `28fb58343` / ks1176 test blob `43cebf8d7`; api-gateway 48/410 at e0f41a8fa -> 49/428 at head, 52/424 at develop 7e89318bc -> 53/442 merged (re-measured 08:29-08:30); dispositions: F-1 CLOSED (ships with #1014), F-2 KS-1195 STILL OPEN, F-3 KS-1196 STILL OPEN, F-4 KS-1197 STILL OPEN, F-5 KS-1198 STILL OPEN; NEW: N-1 Major TICKET + escalation candidate (served data.documentType unchecked, pre-existing), N-2 Minor TICKET (string allow-list substring admits DOCUMENT after #1014's level change), N-3 Minor SHIPS-WITH optional else TICKET (no both-present precedence cell), N-4 Minor TICKET (untyped from a restricted connector stored DOCUMENT, base = head); Records: R-10 fail-closed exact match, R-c CLOSED, R-g extended, #1016's ks1072 TS18046 on develop (for #1016), R-a/R-b/R-d/R-e/R-f/R-i carried.

== NOT TESTED (same prominence) ==
1. Any live stack (KS-535 HOLD).
2. The live Platform-S upload under a connector key against a seeded K + POST /api/verification/verify (§5f) — KS-1176 stays In Progress.
3. A REAL originate (persistence of `type` / `data.documentType`, its body parser's duplicate-key handling, its documents:write re-check, what it actually serves) — N-1 / N-4 are READ ONLY at that layer.
4. A real Redis integration config and the shape production platform-settings holds for allowedDocumentTypes (N-2's premise).
5. The admin portal settings writer end to end.
6. Real security validate and the real connector-token mint.
7. nginx / Container Apps.
8. Schemathesis / Akto / Playwright / k6 (NOT COMMISSIONED).
9. Preflight legs 3/4/8.
10. packages/shared 44/851 and auth suites.
11. A real browser.
12. The verify gate end to end on an N-1 document.
13. R-a / R-f / R-i not re-measured.
14. docker info rc 0 only.

