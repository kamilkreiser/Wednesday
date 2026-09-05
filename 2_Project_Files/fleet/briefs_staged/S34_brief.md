## BLUF

**You are S34, the SUCCESSOR to S33, rotated by Wednesday at the 50% checkpoint boundary (S33 wrapped 00:24Z, scored 0.85 pending the re-gate). Your standing state is S33's `HANDOVER-CURRENT.md`, unchanged unless this mail says otherwise. The 2026-08-28 run-until-empty grant is IN FORCE (Kam reopened the fleet 2026-09-05 08:1x).**

**Your first item is a WAIT with a deploy at the end of it:** the NARROW RE-GATE on `6dc400a` is running now (QA pane launched 10:2x). When it reports, Wednesday does the completion check, SCORES the round, and — on PASS — gives the GO for **ONE deploy of the branch head to the DEV APP** (Kam's `once-after-rd245` ruling, 09:28). **You execute that deploy on Wednesday's GO and nothing before it.** If the gate returns a fix round, it is yours, inside the same branch, then READY FOR RE-GATE again.

**Read first:** your own `HANDOVER-CURRENT.md` (S33's cold-seat block: head, the six findings and fixes, the two veto cards, the deploy recipe, the quarantine paths, the instrument mistakes, the ignore-rule trap), then `2_Project_Files/HISTORY.md` (S33's entry at the BOTTOM — that file's convention), then this mail.

## STATE YOU INHERIT (verified by Wednesday at 10:3x AEST)
- Branch `rd-136-nga-defaults-s12` head `32e4dac` at origin (= `6dc400a` code + the HISTORY entry); tree clean; gate at head `1577/94`.
- **Veto cards:** RD-245 (e)+(a) → Kam ruled proceed (spent). **Erasure DELETES backup copies (RD-308) → PENDING with Kam, default proceed.** If Kam rules otherwise, Wednesday tells you and the commit is REVERTED, not patched.
- Board: RD-296/245/303/307 Testing; RD-308 High + RD-309 filed and fixed at 6dc400a; RD-297 Done; RD-304/305/306 To Do with the gate's sharpenings; RD-295 carries the resolved-by note (human moves it).
- Quarantines (never delete): `NexusAI/quarantine/` (S32's sync artefact) and `2_Project_Files/data/_quarantine_2026-09-05/` (two `.machine-id` instances + README). `data/.machine-id` should no longer be recreated by the suite (F-6 fix) — if you see it appear, that is a finding, not a file to move.
- The local surface on 3111 (`node backend/server.js`, detached) is the previous seat's; leave it or retire it (stop the process, never the tree) — say which.

## QUEUE
**0. Plan-confirmation mail to Wednesday** (`[Datasec/NexusAI -> Wednesday] QUESTION: plan confirmation`), preflight warnings verbatim, then item 1.

**1. HOLD for the narrow re-gate → Wednesday's GO → ONE DEPLOY to the dev app.** The recipe is DEPLOYMENT_GUIDE.md's ordered procedure, not memory. **The RD-302 rule: the deploy is live when the OLD revision STOPS, not when the new one starts** — two revisions served one hostname for 66 s on 09-04; verify after the old revision is gone, and **the receipt NAMES the revision measured** (revision id, image/SHA, the probe and its timestamp). Content probe, not just /health (RD-294 returned 200 throughout its own outage). **Demo is NOT yours — Kam's separate word.** After the deploy: tickets from Testing to the board's deployed state, with the revision in the comment; mail Wednesday the receipt.

**2. While holding (do NOT touch the deploy branch): RD-306 on a NEW branch off the current head** — the LAW path discards the requested window and `take 10000` runs before the sort (arbitrary sample above the cap; the truncated banner makes it loud). Cheapest half first: `order by TimeGenerated desc | take N` so the cap bites on the newest rows; then the `created_at`-defaults-to-now hazard (a LAW row with no timestamp lands in today's window). READ ONLY on the LAW path is all this environment allows — say so; unit tests through the product's own KQL builder. Ends at READY FOR QA. Do NOT merge it into the deploy branch before the deploy is done.

**3. RD-304** (getDataSpan SQLite-only — one string, no figure), then **RD-305 stays UNMEASURED** (needs one probe against a live workspace with credentials this session does not have — do not go looking; it is on the ticket for whoever has them), then the standing category-1 queue by priority then identifier.

## HOLDS (unchanged)
- Signature classes pause for Kam: prod/demo, money, external comms, irreversible. The dev-app deploy happens only on Wednesday's explicit GO mail.
- Every round ends at READY FOR QA; no merge/deploy before the gate and GO. Palette from the style guide only. Never delete — quarantine. Never `--no-verify`. QUESTIONs by mail, not the pane. Checkpoint at 50%; rotation on Wednesday's call inside 70–80%; wrap by mail `[Datasec/NexusAI -> Wednesday] Session wrap 2026-09-05 (S34)`, open round FIRST.

PROVENANCE:
- S33's wrap: the open item is a WAIT; head 32e4dac = 6dc400a + HISTORY; the sets with SHAs; both veto cards; the HISTORY convention (bottom-append per the file's own header) | `[Datasec/NexusAI -> Wednesday] Session wrap 2026-09-05 (S33)` at wednesday-agent@agentmail.to, 2026-09-05T00:24:04Z, and S33's HANDOVER-CURRENT.md (your own tree, mtime 10:22) | read 2026-09-05
- 32e4dac at origin; tree clean | `git ls-remote` + `git status -sb` on your repo (read-only) | read 2026-09-05
- The narrow re-gate on 6dc400a running (QA pane `%9`) with report path `projects/nexusai/reports/2026-09-05-s33-regate-6dc400a-narrow/` | Wednesday's brief `qa-agent/briefs/2026-09-05_nexusai-regate-6dc400a-narrow.md` — my project, not yours | read 2026-09-05
- Kam's once-after-rd245 ruling (09:28) and the erasure veto card (pending, default proceed) | Kam's panel message 2026-09-05 09:28 and Wednesday's decision queue `0_Brain/dashboard/data/decisions.json` — my project, not yours | read 2026-09-05
- RD-306 To Do (scope: LAW path discards the window; take-before-order; created_at default hazard), RD-304 To Do (scope: getDataSpan SQLite-only), RD-305 To Do (scope: timespan format — two consumers; unmeasured), RD-308 To Do/High (scope: erasure reverted by restart — fixed at 6dc400a), RD-309 To Do/Medium (scope: per-run key seed — fixed at 6dc400a) | Jira REST search, project RD | read 2026-09-05
- The RD-302 rule and the RD-294 200-throughout-outage precedent | S33's ACK deploy-timing mail 2026-09-04T23:30:31Z and your HANDOVER-CURRENT.md | read 2026-09-05
- The 3111 surface (pid 59826, detached, tty ??) | `lsof`/`ps` from Wednesday's seat — my project, not yours | read 2026-09-05

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 10:26
(checked: "HOLD for the re-gate" against "RD-306 on a NEW branch while holding" — consistent, the deploy branch is untouched; "deploy on Wednesday's GO" against "demo is Kam's" — two different targets, stated; "S33 scored 0.85 pending the re-gate" against "round score follows the re-gate" — the same statement.)
