## BLUF
**Reading (a) — ALREADY DONE. Wednesday read the project's own CLAUDE.md this action (`/Volumes/DevMASTER/!CODING/Datasec/NexusAI/CLAUDE.md`, YOUR tree, read-only): line 5 "Live (demo): https://nexusaidev-app.politeforest-…", line 26 "The current demo is the Container Apps env: nexusaidev-app", line 135 "demos now run on the Container Apps env (nexusaidev-app)", line 22 the demo VM RETIRED 2026-05-22. The record and your `az containerapp list` agree: the demo IS `nexusaidev-app`, and `48e092c` has served it as `0000097` since 10:53:40Z. Kam's "Deploy to both" is satisfied by the deploy Wednesday already accepted. NOTHING further to deploy. Your stop was correct and Wednesday's brief was wrong to name a second container target — the "demo app served `--0000092`" provenance line was Wednesday's record, and you have now shown it was a revision of the same app.**

## What to do
1. Record it: one line on RD-308 and on RD-318's evidence comment — "demo = dev = `nexusaidev-app`; `0000097` (`48e092c`, digest `5d6187df…`) is the demo revision; no second target exists on this subscription (S36's `az containerapp list`, 2026-09-05)". No board state change.
2. **Do NOT touch `nexusai-staging`.** It is an App Service on a different Log Analytics workspace with a different auth surface — your reading (b) would be a NEW commission with a deploy path nobody has written, and it is not commissioned. Your two GETs of `/api/health` are the whole of what happens there.
3. Kam is being told on his panel now, with a DEFAULT: nothing more is owed on "both"; if he names a second demo target, it comes back to you as a new ticket-led commission, not as an extension of this GO. RD-329 goes to him as a finding in the same line.
4. Then your 50% checkpoint + wrap as you planned. RD-306's merge (on the tester's `48e092c`-verified verdict) and RD-304's tier-1 pass on `rd-304-rebase-s36` @ `69e837b` are the next seat's; the wrap names them under their own headings.

## Holds
Nothing on the demo/dev app since `0000097`; `:latest` unmoved; nothing on `nexusai-staging`; no template re-run; no deletions.

PROVENANCE:
- The demo IS nexusaidev-app (lines 5, 22, 26, 135) | /Volumes/DevMASTER/!CODING/Datasec/NexusAI/CLAUDE.md — YOUR project's file, read read-only from Wednesday's seat | read 2026-09-05 21:11
- Two container apps on the subscription; 0000092/ca98a55 in nexusaidev-app's own history; nexusai-staging = Microsoft.Web/sites, workspace 0fd13d45…; RD-329 filed | your QUESTION mail 2026-09-05T11:04:36Z, read whole — YOUR measurements, not re-derived | read 2026-09-05 21:11
- Kam's word "Deploy to both" (panel 21:00) and no later message | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh output (39 messages, newest 21:00) | read 2026-09-05 21:11

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 21:11
(checked: "nothing further to deploy" against Kam's "both" — the record says both names are one app; Kam gets the default and can name a second target; consistent. "do not touch staging" against "(b)" — (b) is refused as uncommissioned, not chosen; consistent.)
