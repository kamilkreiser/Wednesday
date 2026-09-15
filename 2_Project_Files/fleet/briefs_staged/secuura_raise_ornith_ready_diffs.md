# STAGED — NOT SENT. Brief for the ONE Secuura/Blockchain seat that raises Ornith's held diffs as PRs when the allowance renews (~Sat 2026-09-19 11:xx AEST) or on Kam's word earlier.
# Drafted 2026-09-15 15:5x by Wednesday (the 15:1x seat). Send through `send_brief.sh --kind brief` (the gates add provenance, the RULED-BY-KAM section and the SELF-CHECK). Re-derive every fact marked ⟲ at send time.

## BLUF
Ornith (the local model) has produced **21 distinct pins across 15 tickets**, each PASS 7/7 under the code_patch checker at develop M55 `48e65c435` and each source-read by Wednesday, held as files in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/READY_*.diff.md` (23 files — KS-1120-F2 and KS-1171-8j carry a q4 AND a q8 copy; they are byte-identical in intent, pick either). **Your job: raise them as PRs under the project's normal gate, ONE PR PER TICKET (bundles below), each on a branch from the develop of the minute, each with a Test Evidence block; then hand each PR to a tier-2 through-code QA gate via Wednesday.** You hold the Secuura GitHub/Linear identity; Wednesday holds none. Merges follow the 2026-09-11 TESTED grant on Wednesday's GO — one at a time, head pinned.

## WHOSE / WHERE (the field that says whose it is)
Remote `kksecura/…` (the project's `git remote -v` at send time ⟲), branches `feature/ks-<n>-ornith-<slug>` from `origin/develop` ⟲ (M55 at drafting; if develop has moved, every diff is re-applied at the new tip with `git apply --3way` and the ticket's cells re-run BEFORE the PR opens — the checker's verdict is pinned to M55). Tickets on team KS, assignee = the project's own account (Kam's) — Peter's/Stuart's tickets are not in this set.

## THE BUNDLES (one PR each; the READY filename → the diff to apply)
1. **KS-1130** — three TEST-ONLY pins (tier-2 twins of #969's guards): `READY_KS-1130-E1twin_*`, `READY_KS-1130-E7twin_*DECLSPLICED*` (use the DECL-SPLICED body — it is the runnable one), `READY_KS-1130-E3twin_*`. No product change. Branch note: the ticket's P2/P3 comment items are NOT in the diffs — do them in the same PR if the ticket's words are met, else leave a facts comment.
2. **KS-1123** — two TEST-ONLY pins: `READY_KS-1123-F3_*`, `READY_KS-1123-F2_*`. F1 is KS-1073's cell (bundle 5). P1–P3 comment items as above.
3. **KS-864** — two product halves + two tests: `READY_KS-864-PartA-helper_*` (helper E1+E2; the model added one harmless comment line above the const — keep or drop) and `READY_KS-864-PartB-portals_*` (E3–E5). After both: `grep -c 'ashypond\|westeurope\|secuura-staging-' system-status.ts` must equal the 17 untouched call-site arguments only. Part A's test file kept the name `ks864-dead-estate-pointers-in-runtime-source.test.ts`; Part B's is `ks864b-…` — rename A's to `ks864a-…` for symmetry if you like.
4. **KS-871** — two product halves + two tests: `READY_KS-871-PartA-details-path_*` (entry capture + :280) and `READY_KS-871-PartB-deriveAction_*` (:108). Both tests drive the KS-843 door in-process; after both, the ticket's Acceptance ("a refused erasure is audited with /api/gdpr/erasures … the fix is at the capture point") is met. Line 274 (`req.path === '/api/auth/login'`) is a third inside-finish read the ticket did not name — mention it in the PR body as out of scope.
5. **KS-1073** — `READY_KS-1073_*` (product one-liner + test; the tier-2 statusless cell = KS-1123 F1).
6. **KS-1120** — `READY_KS-1120-F1_*` + `READY_KS-1120-F2_*` (either quant copy) — TEST-ONLY; F-3 is a comment reword the ticket asks for — do it in the PR.
7. **KS-1171** — `READY_KS-1171-8j_*` (either quant copy) — TEST-ONLY, item 8j only; the ticket's design decision (two files) stays open — say so on the ticket.
8. **KS-1018** — `READY_KS-1018_*REANCHORED-TDZINLINED*` — the diff body IS the reanchored + TDZ-inlined section (apply it, not the model's raw hunks).
9. **KS-1050** — `READY_KS-1050_*` (decision stated from the ticket's own words — the wallet precedent; say so in the PR body).
10. **KS-1072**, 11. **KS-1087** (item 1 only — item 2 is a design call, untouched), 12. **KS-1165**, 13. **KS-932**, 14. **KS-844** (`*REANCHORED*` body), 15. **KS-908** (`*REANCHORED*` body) — one PR each.

## HOW TO APPLY A READY FILE
The fenced ```diff block is the patch. `git apply --3way --recount --ignore-whitespace <patch>` from the repo root (paths are repo-relative `Blockchain/Dev/...`; a few sections are service-relative — apply those with `--directory=Blockchain/Dev`). Then run the ticket's new test file and the service suite + `tsc --noEmit`; the checker's 7/7 at M55 is evidence, not a substitute for your own run at the branch tip. Each PR body carries: the ticket, the READY filename, the checker run dir (in the READY header), "authored by the local model (Ornith) from a Wednesday-written brief; source-read by Wednesday; re-run by <you> at <sha>", and the Test Evidence block the TESTED grant requires.

## HOLDS (standing lines apply — see STANDING_LINES.md; the ones that bite here)
Client-facing communication = ticket comments only; no @-mentions to Peter/Stuart except the ONE BLUF comment on the review-stream parent per the ruled wrap step; never delete — quarantine; kintsugi first, demo behind gates (no deploy in this brief); every PR waits for Wednesday's GO after its gate; `.github/workflows` untouched.

## QUEUE
ITEM 0: plan confirmation (this list re-derived at the tip; any diff that no longer applies is named, not forced). ITEMS 1–15: the bundles above, cheapest first (TEST-ONLY bundles 1, 2, 6, 7 first — no product risk), each ending at READY FOR QA. Wednesday commissions one tier-2 through-code gate per PR (batchable by tier) and GOs merges one at a time.
