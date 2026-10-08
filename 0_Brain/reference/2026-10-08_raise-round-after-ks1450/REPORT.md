---
date: 2026-10-08
type: reference
source: raise-round drafter sub-agent commissioned by Wednesday 14:3x; saved by Wednesday from the agent's returned text (the harness refused the agent's own write)
status: live
---

# Raise round after KS-1450: partition and briefs

**develop used:** `0a6177ea5482227e83d5045b68b8577a56326ffc` (read with `ls-remote` at 05:12:22Z and 05:26:15Z, unmoved). The shared checkout's `rev-parse --all` was identical before and after the drafter's scratch work.

**The four briefs** (in `2_Project_Files/fleet/briefs_staged/`; each SELF-CHECK reads `@FILL@` and each pane id reads `%<id at launch>`):
- `2026-10-08_seatR18_raise_r2_r5_ks1450done.md`
- `2026-10-08_seatE11_raise_openapi_ks591_ks1364_ks1449.md`
- `2026-10-08_seatG4_raise_originate_ks593_ks1171.md`
- `2026-10-08_seatF5_raise_scripts_ks808_ks1355_ks1328.md`

Evidence and the drafter's scripts are in `evidence/`.

## Seats
**28 unraised items: 23 go to four seats, 5 wait for a review.** All 28 apply forward at develop; none reverse-applies. Controls: KS-1164 now reads MERGED via #1423, and KS-998 and KS-723 read MERGED.

| Seat | Items | PRs | Flow numbers (proposed) |
|---|---|---|---|
| R 18th (`-R`, `ra18`, `.push-lock-d8`) | KS-1274 re-cut, KS-1410 ×2 in one PR, KS-1139, plus KS-1450 → Done | 3 | 35, 36, 37 |
| E 11th (`-E`, `e11`, `.push-lock-e4`) | all 12 openapi passes | 3: the KS-1449 nft pair, KS-591 ×5, KS-1364 ×5 | 38, 33, 34 |
| G 4th (`-G`, `g4`, `.push-lock-g1`) | KS-593 ×3, KS-1171 | 2 | 39, 40 |
| F 5th (`-F`, `f5`, `.push-lock-f3`) | KS-808, KS-1355 stack-guard, KS-1328 | 3 | 41, 42, 43 |

- 11 PRs in total.
- No payload file is shared between seats: all 6 seat pairs were checked, with a control.
- The two platform HTML docs are shared by every seat (the skill requires both in the same commit), so they are append-only with flow numbers allocated in advance, and keep-both merge-ins are expected at merge time.
- Flow 32 stays reserved for KS-1432.

**Excluded until a REVIEW:** KS-865-r2, KS-948-r3, KS-1355 dev-reload-r2, KS-1432, KS-591 platform-tenant-id-uuid. The last shares a file with E's tenants pass, so it goes to the E lane once reviewed.

## Where the census and the pickup were wrong
1. **The openapi split.** Every openapi raise also touches `Blockchain/Dev/docs/openapi/secuura-api.yaml`, so all 12 passes form ONE seat, not 7 seats plus 3 pairs.
2. **The YAML companion diffs land on the wrong operations.** At this develop, 5 of 12 put `required: true` on the wrong operation, and `git apply` gives no error (for example, billing-credits-use lands on `POST /api/billing/admin/credits`). 8 of 12 also re-apply on top of themselves. The E brief forbids applying them: the seat regenerates the YAML and proves the diff.
3. **`docblockra3.py` refuses a key already present in either doc.** KS-591 and KS-1364 are already present, so E's KS-591 and KS-1364 PRs cannot write their doc blocks as the tool stands.
4. **Two census rows are stale.** KS-1164 is now MERGED. KS-998 now fails in reverse too, because #1422 amended its file.
5. **The parallel-seat standing block is not in STANDING_LINES.** It lives only in `learnings/2026-09-09_parallel-seats-on-one-project-grant.md:86-91`; the briefs quote it from there.
6. **Minor:** the KS-1355 stack-guard review names its READY with the `ornith35b-q4` tag, but the file is tagged `spark-dsv4flash`.

## Open questions (drafter's recommendation → default)
1. **E doc key for KS-591/KS-1364:** a re-keyed doc-block tool with a required count-before knob, so the second section is declared. Until ruled, E builds only the KS-1449 pair.
2. **E YAML:** regenerate it, check it with a structural reader plus two firing controls, never apply a companion diff.
3. **E and G PR shape:** one PR per ticket (3 in E, 2 in G).
4. **E Refs:** the transfer-delegation-posts review asks for two Refs. Use Refs KS-591 only, with "KS 1364" in words.
5. **Missing READY files:** analytics-r4, billing-credits-r4, adminconfig-r2, share-cp2 and KS-1171 have a HOLD review but no READY. Recommended: Wednesday writes them before send. Default: the seat raises from the review plus the patch and states the gap.
6. **share-cp2 and KS-808:** their reviews say Wednesday reads them herself. The seat mails the built diff before the push and waits.
7. **F has no raise tools.** It borrows E 10th's, re-keyed to `f5`. Fallback: drop F and give its three items to a later G seat.
8. **R lock tools:** use R 17th's, with the diff against R 14th's reported. R 14th's KS-1274 worktree and branch stay untouched. Objects: a recorded no-op if already present.
9. **E worktrees:** fresh ones. E 10th's two old ones (their PRs merged) are left for Wednesday to route.
10. **Flow numbers:** as in the table above.
11. **STANDING_LINES:** copy the parallel-seat block in.
12. **Checks at send:** confirm no seat holds KS-1364 or KS-1171, and hold KS-808 if anyone is on it (In Progress, Kamil). If a read is unclear, hold that PR, not the seat.

## NOT measured by the drafter
- PR state: no GitHub token. It fetched PR heads 1300–1426 instead; only #1360 still applies forward, and it touches none of these files.
- Linear: every ticket line says "to be read by Wednesday at send".
- Tests: none run, including npm, `generate-openapi` and `check:openapi`.
- Lane tools for E, G and F: hashed and inbox-matcher-parsed only. Sweep classes and lock wait-sets not read.
- Whether the launcher's boot pull goes READ-ONLY when four seats launch at once.
