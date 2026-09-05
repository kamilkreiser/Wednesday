## BLUF

**You are S35, the SUCCESSOR to S34. S34 did NOT wrap: its pane was killed at 13:09 AEST when the cockpit was relaunched fresh (Wednesday's coordinator seat had itself died at ~11:2x; not S34's doing, and nothing S34 pushed is lost). There is no handover mail from S34 and Wednesday could not find a `HANDOVER-CURRENT.md` at your repo root from outside — reconstruct from origin, `2_Project_Files/HISTORY.md` (S33's entry is the last; the file appends at the BOTTOM) and this mail. The 2026-08-28 run-until-empty grant is IN FORCE.**

**Your first item is a WAIT with a deploy at the end of it:** the NARROW RE-GATE (2) on `a554e52` was commissioned by Wednesday at 13:3x (QA pane `QA/NexusAI-s34-regate2` in the cockpit; report path `projects/nexusai/reports/2026-09-05-s34-regate2-a554e52-narrow/`). When it reports, Wednesday does the completion check, SCORES S33's round (0.85 at wrap, amendable), and — on PASS — gives the GO for **ONE deploy of the branch head to the DEV APP** (Kam's `once-after-rd245` ruling, 09:28). **S35 executes that deploy on Wednesday's GO mail and nothing before it.** If the gate returns a fix round, it is S35's, inside the same branch, then READY FOR RE-GATE (3).

## STATE S35 INHERITS (verified by Wednesday at 13:2x AEST)
- Branch `rd-136-nga-defaults-s12` head **`a554e52`** at origin (= local tip; 2026-09-05 11:11:43 +1000), tree clean; one commit above `32e4dac`; gate at head `1600/1600 across 96` per S34's mail. RD-306 on `rd-306-law-window-s34` @ `edb81c5` and RD-304 on `rd-304-dataspan-s34` @ `69d5e47` are on their OWN branches at origin, not in this one.
- **Kam's rulings, all spent, none to re-ask:** RD-245 proceed · erasure DELETES all copies (10:52, on RD-308) · one dev-app deploy after RD-245 (09:28) · RD-303/307 untrack-and-quarantine · RD-297 leave.
- **Wednesday's rulings on S34's open offers:** (a) KEEP `JsonStorage.MIGRATED_AWAY_KEYS` — S34 measured that the idempotent form converges without it, so the static list is belt-and-braces; the gate weighs it, S35 does not remove it unless the gate says so. (b) **RD-310's classification (which of `.machine-id`, `.persistence-sentinel.json`, `agentmail-cursors.json` is customer data) is Kam's decision** — Wednesday cards it; S35 leaves RD-310 at To Do untouched.
- Board (Jira, read by Wednesday 13:2x): RD-245 Testing/High · RD-308 Testing/High · RD-309 Testing/Medium · RD-296 Testing/Highest · RD-304 Testing/Low · RD-306 Testing/Medium · RD-305 To Do/Medium (UNMEASURED — needs a live workspace with credentials this session does not have; do not go looking) · RD-310 To Do/Medium.
- Quarantines (never delete): `NexusAI/quarantine/` and `2_Project_Files/data/_quarantine_2026-09-05/`. `data/.machine-id` should not be recreated by the suite (F-6) — if it appears, that is a finding.
- **Port 3111 is DEAD** (Wednesday's pane close at 10:28 took S33's surface; nothing listens on 3111–3117 now — measured 13:2x). Re-stand a local surface only if the deploy recipe or a probe needs one, detached (`setsid`/`nohup`, tty `??`), and say which port.

## QUEUE
**0. Plan-confirmation mail to Wednesday** (`[Datasec/NexusAI -> Wednesday] QUESTION: plan confirmation`), launcher preflight warnings VERBATIM, then item 1.

**1. HOLD for re-gate (2) → Wednesday's GO → ONE DEPLOY to the dev app.** Recipe = `DEPLOYMENT_GUIDE.md`'s ordered procedure (present at your repo root, checked 13:3x), not memory. **The RD-302 rule: the deploy is live when the OLD revision STOPS, not when the new one starts** — verify after the old revision is gone; **the receipt NAMES the revision measured** (revision id, image/SHA, the probe and its timestamp). Content probe, not just /health. **Demo is NOT S35's — Kam's separate word.** After the deploy: tickets from Testing to the board's deployed state with the revision in the comment; mail Wednesday the receipt.

**2. While holding (the deploy branch untouched): the standing category-1 queue** — read the RD board yourself (Wednesday hands no stale id): the highest-priority open ticket that needs nobody outside Kam, Wednesday and S35, on a NEW branch off `a554e52`. Every round ends at READY FOR QA; nothing merges into the deploy branch before the deploy is done. If the only candidates are RD-305 (unmeasured) and RD-310 (Kam's decision), say so and hold — do not manufacture work.

## HOLDS (unchanged)
- Signature classes pause for Kam: prod/demo, money, external comms, irreversible. The dev-app deploy happens only on Wednesday's explicit GO mail.
- Every round ends at READY FOR QA; no merge/deploy before the gate and GO. Palette from the style guide only. Never delete — quarantine. Never `--no-verify`. QUESTIONs by mail, not the pane. Checkpoint at 50%; rotation on Wednesday's call inside 70–80%; wrap by mail `[Datasec/NexusAI -> Wednesday] Session wrap 2026-09-05 (S35)`, open round FIRST. **Write your HANDOVER block to disk at every checkpoint** — S34's death with no handover is why this mail is longer than it should be.

PROVENANCE:
- a554e52 at origin = local tip, dated 11:11:43 +1000; tree clean; edb81c5 / 69d5e47 on their own branches; DEPLOYMENT_GUIDE.md and HISTORY.md present (HISTORY appends at the bottom — its own convention, S33's entry at line 6664) | `git ls-remote --heads origin`, `git for-each-ref`, `git status --short`, `git log -1`, `ls` on your repo (read-only) | read 2026-09-05
- S34's claims (1600/96; N-1..N-7 closed; MIGRATED_AWAY_KEYS offer; RD-310 filed; no deploy taken) | S34's mail `READY FOR RE-GATE (2) @ a554e52` at wednesday-agent@agentmail.to, 2026-09-05T01:12Z | read 2026-09-05
- S34's pane killed 13:09:32 by the cockpit relaunch (new tmux server pid 19865); Wednesday's 11:06 seat gone by 11:29 | `ps -o lstart` on the tmux server; `cockpit/logs/tap_wednesday.log` + `wake_watch_runner.log` — Wednesday's project, not yours | read 2026-09-05
- Re-gate (2) commissioned: brief `qa-agent/briefs/2026-09-05_nexusai-regate2-a554e52-narrow.md`, wrapper `--check` passed, pane added 13:3x | Wednesday's cockpit — Wednesday's project, not yours | read 2026-09-05
- Kam's rulings (RD-245 proceed 09:15; once-after-rd245 09:28; RD-303/307 untrack-and-quarantine 09:15; RD-297 leave 09:16; erasure proceed 10:52) | `0_Brain/dashboard/data/decisions.json` ruled cards — Wednesday's project, not yours | read 2026-09-05
- RD-245/308/309/296/304/306 Testing, RD-305/310 To Do, with priorities and update times | Jira REST `/rest/api/3/search/jql`, project RD, read-only | read 2026-09-05
- 3111–3117 nothing listening | `lsof -nP -iTCP -sTCP:LISTEN` from Wednesday's seat — Wednesday's project, not yours | read 2026-09-05
- The RD-302 rule and the RD-294 200-throughout-outage precedent | S33's deploy-timing ACK 2026-09-04T23:30:31Z and Wednesday's S34 brief 10:26 — Wednesday's project, not yours | read 2026-09-05

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 13:29
(checked: "HOLD for re-gate (2)" against "standing queue on a NEW branch while holding" — consistent, the deploy branch is untouched; "deploy on Wednesday's GO" against "demo is Kam's" — two targets, stated; "no handover file found" against "reconstruct from HISTORY.md + origin" — consistent; the QA pane named as commissioned — it exists (%3) as of this send.)
