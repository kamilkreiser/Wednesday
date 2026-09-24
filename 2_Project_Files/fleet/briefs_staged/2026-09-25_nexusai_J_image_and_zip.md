# BLUF — NEW SEAT Datasec/NexusAI-J: build the resubmission. Kam has asked, in a DKIM-signed email, for the zip to be built. (1) Build and push the 2.2.0 image to `nexusaireleaseacr` from main `0677388`, using handover §5.1. (2) Read back the digest. (3) Forward-merge main `0677388` into the package line `mkt-release-gate-s78g` (at `df70a96`, which is main `c0788b1` plus lane C). (4) Set the digest. (5) Do the anonymous-pull read-back (C-58 item 1). (6) Run the non-draft package build. Then stop at READY FOR PACKAGE GATE to Tuesday. Tuesday runs the gate and emails the zip. You never touch Partner Center.

**This brief is addressed to the cockpit seat `Datasec/NexusAI-J` only.** No other NexusAI seat is live at the moment (the machine rebooted about 08:55 AEST today and every pane died). The inbox `datasec-nexusai@agentmail.to` is shared, and older mails in it addressed to `-G`, `-H` or `-I` are not yours.

## AUTHORITY (read this before step 1)
- **Kam, email to tuesday-agent@, 2026-09-24 09:04 AEST.** Message-ID `<33D54FEB-D8F0-4220-866D-7182B4094E92@me.com>`. `authentication_results` spf=pass, dkim=pass, dmarc=pass. His words, verbatim: *"Please build the zip or send me instructions on what to do. Don't forget I am away for 1 more day and can't access your machine."* He was replying to Tuesday's mail, which said *"build from 0677388, not 34f11f4"*. He restated it on the live board on 2026-09-24 at 09:51 (*"can you please build the package or give me instructions on what to do"*).
- **C-27** requires Kam's own signed mail for a registry push and its cost. **This mail is that authority**, for the 2.2.0 build and push to `nexusaireleaseacr` from `0677388`, and for nothing wider. Quote it in your plan confirmation and in your commit/Jira evidence.
- Earlier on the live board he ruled card `nexusai-220-image-build-timing` = (a) "Build now" (2026-09-23 09:26:15).
- C-127 (Kam 2026-09-21 18:18:12) covers merges and demo redeploys on a gated head. **Not covered, and it stays that way:** production, Partner Center / Marketplace upload, external comms, anything irreversible beyond the push he asked for.

## 🔴 IF YOUR IDENTITY CANNOT PUSH TO `nexusaireleaseacr`, STOP
If `az acr build` returns an authorization error (or any RBAC refusal), do not request rights, borrow an identity or try another registry. The workspace rule says the boundary is working. Report it to Tuesday at once. **In that case, write the exact steps Kam can run from Azure Cloud Shell in a browser**, because he is travelling without this machine. Put them in `docs/resubmission/2026-09-25_kam-cloud-shell-image-steps.md` on a new branch, pushed. Name the clone URL and commit, each command on its own line, and the digest read-back. Measure every precondition you can (anonymous clone? SSH vs HTTPS?) and mark what you could not. **Mail Tuesday the branch and path. Tuesday posts them to Kam.**

## THE ORDER
0. **Establish your seat from the process table (C-111).** Walk your shell's parents to the `zsh -c` launcher whose command line ends `[cockpit] Datasec/NexusAI-J exited`. Record the launcher pid, your claude pid and your pane id. Use session tag **S81J**.
1. **Re-read the state yourself.** `ls-remote` main (expected `0677388ab031ffaf569a52f6c0301af48f44aece`), `mkt-release-gate-s78g` (expected `df70a96`) and `resubmission-handover-s78g` (expected `dfbd55b`). Read the CI Build on `0677388` (S80I reported 35811343989 GREEN, 3974/3974, 234 suites; that is relayed, so re-read it). **If main moved or CI is not green, STOP and mail.**
2. **§5.1 as written, from a CLEAN checkout of `0677388`** (`git status --porcelain` empty). Use `az account show` in the project's own AZURE_CONFIG_DIR and confirm sub `0c57ab37`, tenant `d500ebad`. Then run `az acr build … --image nexusai:2.2.0 --build-arg BUILD_COMMIT_SHA=…`, then the digest read-back. **Check first whether `nexusai:2.2.0` already exists in the registry.** If it does, STOP and mail. Never overwrite a tag.
3. **Forward-merge `0677388` into the package line**, on a new branch off `df70a96`. Forward, never rebase (C-68). Counts are regenerated once (C-57, with C-133 beside it). Verify on the merged tree.
4. **Set the digest** at `azure-marketplace/combined/mainTemplate.json` (the placeholder line, which G measured at :106 on `df70a96`; re-read it) and README:40. `release-policy.json` keeps the refusal rule.
5. **C-58 item 1: the anonymous-pull read-back** of the digest. Pull it without credentials and prove that is what a customer gets.
6. **The non-draft package build:** `scripts/marketplace-package-build.sh <repo> <commit> 2.2.0 <empty-out> azure-marketplace/listing-assets.txt`. Record the zip's sha256 and the source head. **Fold handover doc `dfbd55b` in and fill its `<filled at build>` values.**
7. **READY FOR PACKAGE GATE → tuesday-agent@**, with: the image digest, the build log id, the package branch and head, the zip path (inside the project tree, never /tmp) and its sha256, the verify numbers, and the full residual list for Kam, carried from HANDOVER-S78G, CLARIFICATIONS and the handover doc (C-124 Key Vault success path unproven on real Azure, the template never validated against real Azure (C-20), and every item your predecessors listed "for Kam WITH the package").

## ⚠ THE DEMO PIN — flag it, do not act on it alone
HANDOVER-S80I says the demo runs `34f11f4` and *"the demo deliberately matches the resubmission"*. Building from `0677388` breaks that match. **Do not redeploy the demo in this brief.** Say in your READY whether a demo redeploy to `0677388` is needed to restore the match, and Tuesday will GO it under C-127.

## HELD — not yours in this seat
Partner Center, anything production, any Azure change beyond the one `az acr build` push, merges to main, and anything to Peter or HP.

RULED BY KAM, NOT YET IN AN ARTEFACT
- (none undelivered for `nexusai-` at 09:2x AEST 2026-09-25, per `decision_queue.sh list ruled --undelivered nexusai-`). **Record the signed-mail authority above as a new C-number in CLARIFICATIONS in your first turn, and send the number back.**

RULED BY TUESDAY FOR THIS PROJECT, STILL OPERATIVE
- The build commit is `0677388`: it is what Tuesday's mail to Kam named, and what his signed reply answered. 34f11f4 is superseded as the resubmission pin.
- C-142: "green" means the local lock verify AND the CI failing set equal to the known set, by name.

## PRIOR-WORK CHECK (C-49)
Before step 3, read HANDOVER-S78G.md whole (lane C's state, the package-gate flags, the 23-id C-133 table) and HANDOVER-S80I.md §1, 2b.

## PLAN CONFIRMATION, then START
Mail your plan to tuesday-agent@ with the subject `[Datasec/NexusAI-J -> Tuesday] QUESTION: plan confirmation`, then start step 1 without waiting. It is read-only. **Step 2 (the push) waits for Tuesday's GO reply to that plan.**

PROVENANCE:
- Kam signed mail text and auth | agentmail GET tuesday-agent@ message `<33D54FEB-D8F0-4220-866D-7182B4094E92@me.com>`, authentication_results spf/dkim/dmarc pass | read 2026-09-25 09:2x AEST
- Kam live board 2026-09-24 09:51:12 and card ruling 2026-09-23 09:26:15 | `tools/kam_msgs.sh 40 --source live` | read 2026-09-25 09:2x AEST
- main 0677388, mkt-release-gate-s78g df70a96, resubmission-handover-s78g dfbd55b | `git ls-remote origin` (read-only) in the NexusAI repo | read 2026-09-25 09:2x AEST
- §5.1 commands | `git show dfbd55b:docs/resubmission/2026-09-22_resubmission-handover-for-kam.md` lines 158-179 | read 2026-09-25
- C-27 signed-mail requirement; nexusaireleaseacr created with no images | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/1_Project_Definition/CLARIFICATIONS.md lines 403-407 | read 2026-09-25
- demo on 34f11f4, resubmission pin, queue empty | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S80I.md §1-2 | read 2026-09-25
- package line state, digest placeholder :106, step list | /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/HANDOVER-S78G.md CURRENT STATE | read 2026-09-25
- floor: only %0 tuesday and %1 fleet-monitor; uptime 32 min at 09:27 | `tmux list-panes -a`, `uptime` | read 2026-09-25 09:27 AEST
Self-check note: re-read whole by Tuesday; the push waits for the plan GO in both places it is mentioned; the demo is flagged, not acted on.
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-25 09:30
