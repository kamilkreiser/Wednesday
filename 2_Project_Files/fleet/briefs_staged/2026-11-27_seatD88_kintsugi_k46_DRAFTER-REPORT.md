# DRAFTER REPORT: Seat D 88th, Kintsugi round k46 (drafted 2026-11-27, Sonnet; no box touched, no mail, nothing posted)

Brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-27_seatD88_kintsugi_k46.md (STAMP left empty).
Read method for GitHub: `gh api` under GH_CONFIG_DIR=/Volumes/DevMASTER/!CODING/Secuura/Blockchain/4_Credentials/.gh-config (gh auth status = kksecura). No git clone, no fetch; reads only. (The Wednesday shell's own gh login is a different identity; I exported the project config per command.)

## COMMISSION FACTS I MEASURED AS WRONG
1. **Fact 7, "Kam ruled yesterday" (card secuura-ks2366-old-stuck-certifications-1126 = a):** `decision_queue.sh show` prints `ruling: choice='a' ruled_ts=2026-11-27T09:59:36.398358+11:00`, i.e. TODAY, after the 26th's wrap (the card's own default and the 11-26 daily note both predate it). The brief quotes the ruled_ts. Substance (a = measure demo first, read-only, by a different seat; the D seat repairs nothing) is as commissioned.
2. **Fact 2, "'the rest' at a different base ee1e1b832115":** only the residue is at ee1e1b832115. D 87th's HANDOVER FOR A SUCCESSOR item 3 gives per-service bases (issuer-frontend bcc2d8a53ffd; vc-issuer and billing aff83df1b23d; mcp-server 8389ed294629; nft-certificate and timestamping 038425cafaec; auth d4ffc8308249; transfer fab4edcdcd07; staking, security, analytics, verifier-frontend caace2ef3d61; prism 8292da2c9dbc; m365-integration db2b80073264; wallet-connector, kyc, anchoring 6185f0f1ace8; tokenisation, governance 4e4347818772; migrations c5c26b2835df). Does not change the derived set (all those services' owed items are the same option-(i) held list as k45; none of the 3 new commits touches them).
3. **Fact 3's quoted row title** ("DEPLOY EVERYTHING as soon as it is tested and ready, for the rest of the week") is the register ROW TITLE, not Kam's words. Kam's verbatim (column 2 of the same row, line 20 of EXPIRING-GRANTS.md): "deploy everything as soon as its tested and ready.  This stands for the rest of the week" (two spaces after "ready."). The brief quotes Kam's words and names the row title separately. Board time 2026-11-23 10:14:18 and end of Sunday 2026-11-29 are as commissioned.
4. **Fact 4, "equals the template's":** the host-key pin SHA256:gl2JBs7KpV7/wrYd/7bzqTNQ+wyFQJomCtQkfUs8nuU is NOT in the k45 template (0 hits, /usr/bin/grep -F). It equals (exact string) D 87th's tools/boxrun_d87.sh line 48, D80_status_a.txt, and S127's brief/q_plan. D 87th's other records (STATUS/wrap/HANDOVER) do not carry it. I added a BOX ACCESS PIN paragraph to the brief. A related trap: boxrun_d87.sh hard-codes D 87th's scratchpad known_hosts path; the new seat must repoint it.
5. **Fact 6 (implicit: an anonymous verify is a free read):** an anonymous verify is `POST /api/certifications/<id>/verify` and writes one `audit_logs` row per request (S 125th measured +4 for four anonymous requests, charge rows 0). The brief makes LC-C a named, licensed item whose only state left is that one audit row; default NOT RUN. Not a wrong fact so much as a hidden cost.
6. **Routing row C6:** NOT checked against a routing table (I could not find one by a bounded search); today's daily note line 27 calls the drafter row C8, which is a different row. The model line is as commissioned.

Facts re-measured and CORRECT: develop tip = 4764b2cfbc28768ef9c7b684e2af2e0f2f1438e5 (no later commit); PR 2295 merged, 10 files; gate 420 GO WITH NOTES at head dbceb300851b; originate/admin-frontend/api-gateway base 9c1ecde5abd6; no migration; grant end Sunday 2026-11-29; ordinal 88th.

## FACT TABLE (fact | source file:line or command | read today?)
| fact | source | read today |
|---|---|---|
| develop tip 4764b2cfbc28, committer date 2026-11-26T01:26:25Z, nothing newer | `gh api repos/Secuura/Distributed_Secuura/commits/develop`; `commits?sha=develop&per_page=5` (4764b2cf, 59e89c87, d024a978, 9c1ecde5, ce0a767a) | yes |
| squash parent 59e89c87719e, tree 6ec6995d0d0a, 10 files, merged | `gh api commits/4764b2cf`, `pulls/2295` | yes |
| range 9c1ecde5..4764b2cf: ahead 3, behind 0, 18 files, 14 under Blockchain/Dev (7 test-named, 7 not), 0 `.sql`/migrations/Dockerfile/package/compose/dockerignore/shared/yaml | `gh api compare/9c1ecde5...4764b2cf` plus jq filters | yes |
| commits: d024a9788e87 KS-1209 (7 files, parent 9c1ecde5, tree 15d91e5955b3), 59e89c87719e KS-2142 (1 file, tree 6048e6233557), 4764b2cfbc28 KS-2366 | `gh api commits/<sha>`, compare commit list | yes |
| wrong-range controls b69addc39652 21 (10 non-test), bcc2d8a53ffd 30 (13), aff83df1b23d 41 (21) | compare per base, jq | yes |
| only COPYs of `scripts` in any Dockerfile: originate run-migrations.sh (line 47) and auth's own folder (line 67); originate COPY dist line 62 | `/usr/bin/grep -H -n -E "^\s*COPY.*(scripts\|audit)"` over 36 Dockerfiles fetched at the pin | yes |
| `.dockerignore` has `**/__tests__` (line 14) and `tests` (line 13) | contents API at the pin | yes |
| originate tsconfig declaration true, sourceMap true, tests excluded | contents API at the pin, tsconfig.json | yes |
| originate Dockerfile structure (builder COPY src line 41, scripts 47; runner lines 62-68) | fetched at the pin | yes |
| security's only path is a test under `__tests__` | compare file list | yes |
| 4 originate src files, their literals and logger strings | `gh api commits/4764b2cf` patches | yes |
| gate 420: GO WITH NOTES at dbceb300851b, G420-1..9, 84-call matrix, 226 not 220, deploy-grep count 2 (lines 194, 197) | .../0_Brain/reference/2026-11-26_gate420-tier1-ks2366-cert-anchored-confirmed/verdict.md; `/usr/bin/grep -a -c -i deploy` = 2, control 0 for a made-up string | yes |
| K 94th: squash line count 1, tree, parent, 10 files | briefs_staged/2026-11-26_K94_verify_merge.txt; K94_wrap.txt | yes |
| W 77th: jest 3770/3770 (develop 3738), shared 1746/1747 KS-278 | briefs_staged/2026-11-26_W77_ready.txt, W77_wrap.txt; gate 420 re-runs table | yes |
| k45 end state: ids, containers, StartedAts, REVISION 308,061 B 813838f350bde0f9 49 lines, priors 34, idfp ae603f091ea65d53, free 75,270, build cache, cost 4.2 GB / 15 min and cause | 2026-11-24_D87_status_b.txt, _wrap.txt; D 87th HANDOVER.md FINAL + FOR A SUCCESSOR 1-7 | yes (CARRIED; box not touched) |
| REVISION `.pre-*` sizes and sha16 | D 87th HANDOVER.md line 15 (item 2) | yes (carried) |
| census values (users 31 etc.), KS-535 sha16s, yaml/compose/config sha16, nginx conf sha | 2026-11-24_D87_q_plan.txt section 3, status_c | yes (carried) |
| host-key pin string equal across records | `/usr/bin/grep -o -E "SHA256:..."` over boxrun_d87.sh line 48, D80_status_a.txt line 29, S127_q_plan.txt line 13 | yes |
| hostname guard `secuura02-kintsugi-vm`; keyscan method | briefs_staged/2026-11-26_seatS127_ks1971_ks2366.md line 45 | yes (not run) |
| swap tool places: swapset_d87.py line 77 TEMPLATE, line 83 conditional assert; swap_driver_d87.sh lines 68, 72, 73, 90, 94-98 (H2 only for api-gateway); swaplaunch_d87.sh lines 42, 48, 52; buildlaunch_d87.sh line 42; healthwin_d87.sh line 23 | files under .../2026-11-24_seatD-87th/tools/ read with grep -n / sed | yes |
| sha16 of the one-service order file `330cd23a278a243b`; method reproduces 5a1e13291b6783aa (3-order) and af388302658ad2e2 (2-order) | `printf ... \| shasum -a 256 \| cut -c1-16` x3 | yes |
| Kintsugi certification rows 11 (10 submitted, 1 failed, 0 confirmed), 105 confirmed docs | briefs_staged/2026-11-26_S127_wrap.txt; the card bluf | yes (carried) |
| anonymous verify = POST /api/certifications/<id>/verify; audit_logs +4 for 4 requests, user null; billing/charge rows 0; id 2b2f5b95-... answered blockchainAnchored true at k45 | S125_status1.txt lines 25-37; S125_wrap.txt line 11; S125 evidence/expected_table_s125.md; tools/req_s125.py | yes (carried) |
| the two ruled cards verbatim | `decision_queue.sh show` (read verb) | yes |
| grant row, end Sunday 2026-11-29, Kintsugi-first reading | 0_Brain/tasks/EXPIRING-GRANTS.md line 20 | yes |
| ordinal: `Seat D 88` 0, `Seat D 87` 1 (history.md line 104), no seatD-88th folder; D 85th/86th/87th headings at lines 200/159/104 | `/usr/bin/grep -a -i -c`, `grep -n`, `ls 5_Project_History \| grep -c seatD-88` | yes |
| originate-only precedent (D 54th: swap 13 s, census 1 of 35; "build 2 / swap 1" when migrations carries SQL) | history.md lines 6918-6938, 11087 | yes |
| No D seat has run since k45; S 125th's box read (2026-11-25 19:25Z) equalled the k45 record | no seatD-88th folder, history top entries (K94, W77, S127, S126, S125, K93, ...); S125_status1.txt line 14 | yes (inference: absence of a D record) |

## NOT MEASURED
- Anything on the box (REVISION, ids, StartedAts, free MB, box date, census, certification rows, dev-migrations, the host tree being exactly 9c1ecde5abd6).
- The real compiled originate `dist` file set and literal counts: I ran NO local build (Docker-layout npm ci + tsc was out of a lean drafter's scope and would need a clone); section 7 is code reading from the patch. Whether tsc keeps comments in originate's output; whether `tsc` leaves `blockchainAnchored: !!certification.blockchain` text identical or unique in the base file; how contentfp prints an ADDED file.
- No suites were run (gate 420 and W 77th ran them at the head).
- Linear state of KS-2366; GitHub CI; usage gauge; routing row C6.
- That the host key still equals the pin (no ssh-keyscan run).
- Whether 2b2f5b95-d76e-48d9-a936-737661867bd0 is a pending row.
- Why S 125th's `documents` count (151) differs from k45's census figure (76).

## QUESTIONS FOR WEDNESDAY
1. **security, test-only path (inclusion uncertain):** `services/security/src/__tests__/ks1370-...integration.test.ts` (KS-2142) is the only path under services/security. I excluded security (dockerignore + tsconfig exclude). The seat's derive tool may still list it by path; confirm the rule "a `__tests__` path is not a build input".
2. **The two non-KS-2366 commits (d024a9788e87 KS-1209, 59e89c87719e KS-2142) ride into the pin with no gate verdict named in the commission.** Their 8 files reach the host tree via rsync (7 under Blockchain/Dev count in the 14 sends); the brief's H6/D88-W9 makes "a first-parent commit with no gate verdict" a STOP unless her GO names them. Do they have gates, or do you accept them by name in the GO?
3. **Anonymous verify writes an audit_logs row (POST, audited).** Do you want LC-C licensed (one request, one existing submitted certification, one audit row), or LC-A/LC-B only? Brief default: LC-C NOT RUN unless the GO LIVE-CHECK names it.
4. **A NEW certification confirming on chain** is listed under D88-W6 as not a seat step (needs a signed-in identity, creates documents/anchor_store/charge/audit rows, spends the anchoring wallet's preview-network funds, irreversible). Confirm it stays out, or card it.
5. **contentfp for originate** now has changed AND ADDED paths (about 15; 4 new). The brief asks the seat for its local-build measurement and your ruling (D88-W13/Q4) rather than pre-ruling a count.
6. **Gateway not recreated:** after an originate-only swap the gateway keeps its process; the brief asks for docker-exec `/health/ready` and error-level counts only (no request). Is that proof enough, or should the GO consider a gateway restart (not in this brief; the precedent D 54th swapped originate alone)?
7. **Costs:** originate-only build cost is UNMEASURED; I estimated up to about 4 GB (k45's figure for three; the runner-layer re-run is originate-wide). Free was 75,270 MB at k45's end; floor and gate carried.
8. **Box date trap:** at 10:36 AEDT today the box (UTC) date is still the 26th. The brief says the tag is the box's date and extends the zero-read stamps.

## DIFF-STYLE SUMMARY VERSUS THE k45 TEMPLATE
Section numbering kept (STAMP, WHAT, model, NEW SEAT, AUTHORITY, 0, 1, 2, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, RULED BY KAM, PROVENANCE, UNMEASURED).
- **Title/header:** 3 services -> 1 (`originate`); pin 9c1ecde5abd6 -> 4764b2cfbc28 (default); k45 -> k46; 87th -> 88th; KS-2111/KS-1988/KS-2075 -> KS-2366.
- **STAMP:** emptied (template carried D 87th's stamp).
- **WHAT:** rewritten: k45 summary; 3 commits since; five findings now (one-service set and no migration; originate-only precedent and dormant H2; old certifications read false, repaired by no one; anonymous verify writes an audit row; new anchoring is not a seat step). Kit paragraph: frontend tools DROPPED; kit re-key `_d87 -> _d88` with F4 write-after-dry rule; added `mkdir evidence/phase2` (F12), zsh `set --` (F6).
- **AUTHORITY:** re-quoted from EXPIRING-GRANTS.md (Kam's words vs row title); ADDED BOX ACCESS PIN (host key, known_hosts re-point, hostname guard).
- **0:** disk figures re-based (75,270); cost estimate re-reasoned for originate alone; unmeasured.
- **1:** H2 gate no longer runs (gateway not in set); H3 pin; H4 suites re-based (originate jest 3770, no gateway/admin suites, KS-1209 audit tests as a QUESTION-only item); H5 migrations NONE re-measured; H6 gate 420 grep (2, lines 194/197) and a rule for the two commits with no gate verdict; H8 carried.
- **2:** whole section re-derived: range, per-file consumer table, security test-only, bases (per-service, correcting the "ee1e..." fact), config, rsync 14 with new wrong-range controls (21/30/41), REBUILT 1 / UNCHANGED 32 / NOIMAGE 3.
- **3:** ONE batch; swap set in FOUR places (H2 place dropped); order sha16 330cd23a278a243b; allow-list "1-service"; planted controls re-keyed; rollback originate only; REVISION naming `.pre-<SHORT>-k46` and line counts 49 -> 50; Redis/vouch for originate only; a4x, healthwin, watch15 lists re-keyed; box-date trap.
- **5, 6:** re-keyed to originate (gateway/vc-issuer/billing controls).
- **7:** whole matrix replaced: originate `/app/dist` changed + ADDED paths (about 15, seat measures), `/shared/dist` identical, scripts unchanged control, literal prior from the patch (7 rows + flag expression + 2 controls), unmoved-control rows for gateway and admin; the gateway/admin predictions dropped.
- **8:** replaced with KS-2366 consequences (old certifications read false; new ones confirm; gate 420 Lows/Notes), KS-1209/KS-2142 deploy nothing.
- **9:** traps re-keyed: four places, 3-service literals, service-list readers, contentfp ADDED files, gatemap glob (add gate 420), boxrun known_hosts, scripts unchanged; D 87th's F4 and F11 added as standing faults.
- **10:** Q1-Q13 re-based; Q13 (certification rows, id 2b2f5b95, TimeZone) NEW; Q9 (gateway after originate-only swap) NEW.
- **11:** LC-A rows re-keyed; LC-B adds certification counts and TimeZone; LC-C now the ONE anonymous POST verify (named request, one audit row, default NOT RUN); gate 420 notes that a live box can exercise (G420-7, G420-8 only) listed; LC-D labels re-written.
- **12:** D88-W1..W13 (W5 licence form; W6 NEW "new certification confirming" with what it would touch; W8, W9, W12 NEW).
- **13:** holds extended (no certification repair; no tx hash printed; a `.sql` at the pin is a QUESTION first); stop list re-keyed to one service.
- **14, 15, 16:** re-keyed (k47, priors 35, originate container, the G420 board ticket and the old-certification card on the wrap's next rows).
- **RULED BY KAM:** grant re-quoted; ADDED the two ruled cards verbatim (what-anchored-means = a; old-stuck-certifications = a with ruled_ts today).
- **PROVENANCE:** all lines rewritten in `fact | source | read 2026-11-27`; UNMEASURED paragraph rewritten.
- **DROPPED:** admin-frontend and api-gateway build/verify/predictions, frontend kit tools, H2 live gate, five-place swap list, k45 consequences (KS-2111, KS-1988/2075), the k45 SELF-CHECK line (Wednesday stamps).
