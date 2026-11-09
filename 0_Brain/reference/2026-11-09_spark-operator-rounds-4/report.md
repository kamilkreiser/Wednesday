# Spark rounds o117: 4 briefed, 4 PASS (4 held), 0 FAIL, 0 still queued
Saved by Wednesday 18:0x from the operator's final message (its own Write was refused). Develop e8d23ce366e2 at both ends; 57 open PRs / 304 files identical at both ends, none lists a file below; tunnel up; drainer run twice inside run_in_background (no nohup, no &).

| Ticket | Tier / rung | Files | done.md | READY (local-model/night/) |
|---|---|---|---|---|
| KS-2123 (types + ADMIN survivors only) | test_only_input, two-hunk (rung up) | api-gateway ks1448-notification-create-own-id-only.test.ts | 17:58:04 PASS 95 s | READY_KS-2123-...-O117-P1_...NOTIFICATIONS-PASS-9of9 |
| KS-2027 | doc_only | three ks1868 originate tests (unused eslint-disable lines) | 17:58:33 PASS 28 s | READY_KS-2027-...-O117-P1_... |
| KS-2089 item 1 | doc_only | scripts/check-shared-relink.sh line 522 comment | 17:59:02 PASS 28 s | READY_KS-2089-...-O117-P1_... |
| KS-2150 | doc_only + docs-fragments check | Projects Documents/fragments cheat+flow KS-2109 | 18:00:16 PASS 42 s | READY_KS-2150-...-O117-P1_...PASS-10of10 |

Operator's brief defect fixed before any model round: KS-2027's first control failed A4/A7 (expect_present lines already true at the tip); removed and re-run.
Rejected after reading: KS-2132/2133/2134/2016/2012/2053/2022/2107 (raise PRs already open); KS-1947 (file in PR 2052); KS-1980/2033/1587 (need real Postgres); KS-1945/2065/1712 (first step is a measurement); KS-2085 (too large).

## Wednesday's source read of the four diffs (18:0x) — flags for the raise seat and its gate
- KS-2123: the four new cells are labelled 'RED KS-2123 R6'. If develop already refuses those types, they are PINS, not red cells: the gate shows red-on-develop or the label changes. ADMIN survivor row fine.
- KS-2027: removes three eslint-disable-next-line lines; 'unused' rests on Seat V 22nd's record, not re-run: the gate shows eslint no worse.
- KS-2089: the new comment states a mechanism ('refused later, when its name is not found in NON_JS_BASES (see image_name_component above)') Wednesday has not read in the script; the gate checks it. The line is now overlong.
- KS-2150: the cheat figure becomes '4 files, +32 -2'; the gate checks it against PR 2111's real numstat.
