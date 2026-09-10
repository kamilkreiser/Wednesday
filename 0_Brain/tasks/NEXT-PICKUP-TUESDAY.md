---
date: 2026-09-10
type: pickup
scope: DATASEC ONLY — Tuesday, on Kamils-Mac-mini. Secuura and general are Wednesday's, on the Studio.
source: written at s5's 66% checkpoint, 2026-09-10 ~13:55 AEST
status: live
supersede: replace WHOLESALE at the next pickup; never append. It replaced the s4 pickup.
---

# NEXT PICKUP — Tuesday, s5. Three rounds delivered and verified. Kam owes four decisions. Nothing is on fire.

**`2_Project_Files/tools/kam_rulings_today.sh` before writing anything.** Rotation band **80–90**; 70% is a checkpoint only.
**Kam reads the pane on the MAC STUDIO. Verify every message AT ORIGIN** (`git show origin/main:0_Brain/dashboard/data/chat_tuesday.json`) — never on `127.0.0.1`, which is this machine and proves nothing. That cost him four unanswered messages this morning.

## 🔴 WITH KAM — four, and only the NAS blocks me

🔴 **s6 CHECKPOINT, 20:2x — KAM RULED SEVEN CARDS; ALL RECORDED AND RECEIPTED.**
- **NexusAI:** `nexusai-marketplace-screenshot-reshoot` = **reshoot** (19:42) — Tuesday's receipt states the reading **AFTER tomorrow's build**, so the branch he builds from and tonight's QA verdict do not move; he may say sooner. · `nexusai-authorized-users-md-remove` = **keep** (19:43) — the file ships in tomorrow's build. · `nexusai-main-tree-is-a-stale-snapshot` = **investigate** (re-tapped 20:15; same as 10:48). **Both 19:42/19:43 receipts went out 33 minutes late** — ledger row: the wake handler filtered on the `received` label and Kam's panel mails are `sent`. **On every wake: list the inbox UNFILTERED and route on subject.**
- **HPSM:** Q-05 **new-repo** · Q-19 **hpsm-severities** · Q-20 **spec** (Kam over the agent's rec: always remediate High) · the other 16 **accept**. All four cards `delivered` via the build brief.
- **HPSM BUILD COMMISSIONED:** brief `2_Project_Files/fleet/briefs_staged/2026-09-10_hpsm-composer-build-wp0-2.md` sent through `send_brief.sh --kind brief` (passed every gate), read back at `datasec-hpsm@` 10:21:20Z; **seat launched 20:21:21 through HPSM's OWN `Launch_Claude.command`** via `cockpit.sh add "Datasec/HPSM"` (pane `%2`). Queue: WP0 harness, WP1 content + provisional seed, WP2 schema + cardinality; the GitHub repo and Jira project need identities — the seat mails a QUESTION with exact steps and does not block. **LOCAL FIRST.** **Tuesday owes Kam one confirmation when the seat has the commission** (rung 5/6), folding in his 20:19 "Thank you. Good luck." **Its plan confirmation comes to tuesday-agent@ — answer it.**
- ⚠ **THE HPSM PANE PARKED AT CLAUDE CODE'S FOLDER-TRUST DIALOG for 12 minutes** (fresh machine; earlier HPSM seats ran headless, which skips it). **Tuesday accepted it at 20:33:31**, cursor checked in code before Enter, after MEASURING what it enables: HPSM `.claude/settings.local.json` = three permission allows (`az ad *`, `python3 -c`, `cat /tmp_sp_err.txt`) + the fleet statusline command; no hooks, no MCP, no env; the seat runs with permissions bypassed anyway. **Disclose to Kam in the build confirmation. Any future interactive launch on this Mac into an untrusted folder will park the same way — check the pane at launch, not ten minutes later.**
- **NAS:** Kam ruled `stop-partition-rerun` on Wednesday's card (20:27:58) — she is re-running HER leg tonight with `DEVNAS_IGNORE_NAMES="Datasec TUESDAY"` as a per-run env var, no change to `nas_sync.sh`; Tuesday replied no objection. She reports back: throughput, `Deleting` count, whether the ignore took. **Fold her numbers into the design's section 4 when they land.** NAS share listing 20:3x: `!CODING/Datasec` and `Secuura` single-case; no `TUESDAY` at the share root.

🔴 **NAS — STATE CHANGED AT s6, 19:19. READ THIS BEFORE ITEM 1.** The share IS mounted on this Mac (`mount` shows `//KAMILADMIN@192.168.20.221/Development`; the mount point is dated ~17:02), so item 1's connection half looks DONE — but Kam has not said "done" on the panel. **Kam's 17:16 ask — a good check, because Tuesday and Wednesday sync to the NAS at different times — sat unanswered until 19:14. Tuesday s6 acknowledged it and claimed it by mail to Wednesday (coordination only).** **`com.tuesday.nassync` (23:00) was BOOTED OUT at 19:19:19 ON PURPOSE**, so no unattended leg runs before that check exists. `doctor.sh` will warn that it is not loaded: **do NOT reload it until the check is built, red-proofed, and Kam has heard what it covers and what it cannot.** Revert, when that is true: `launchctl bootstrap gui/$(id -u) ~/Library/LaunchAgents/com.tuesday.nassync.plist`. **The by-hand run promised in item 1 also waits for the check.**

🔴 **s6 UPDATE, 19:3x — what changed since this pickup was written.**
- **HPSM:** Kam ruled both flags (19:01 `excluded` for image.png; 19:02 **`derive` defaults from the Essential Eight SOW**). Relayed to `datasec-hpsm@` at 09:07Z with **SUPERSEDES** of s5's flag-2 "do not invent" line; read back at the destination; both cards `ruled` + `delivered`. **RECEIPT 19:39 (09:39Z), VERIFIED IN THE FILES by Tuesday:** derive lives in `2026-09-10_policy-composer_ARCHITECTURE.md` A-52/A-53 + Q-01 RULED and `2026-09-10_seed-data-CONTRACT.md` "The one rule" + §D; excluded lives in the ARCHITECTURE sources section + Q-02. 🔴 **The agent's coverage count matters for Kam's derive ruling: the E8 SOW seeds domain 69/123, remediation 122/123, high-impact 98/123, and severity / unsupported / ISO-NIST-SOC2-HIPAA mappings 0/123.** New open questions Q-19 (silent columns) and Q-20 (remediation conflict) — carry them to Kam as cards WITH the agent's recommendations when its wrap lands, not before. **WRAP LANDED 19:42 (session 32) and CARDED 19:4x:** `hpsm-composer-repo-and-jira-home` (Q-05, **blocks the BUILD start**, rec new private repo + Jira project) · `hpsm-composer-silent-columns-severity` (Q-19, **blocks RELEASE**, rec HPSM's own Preview severities as a second derived source) · `hpsm-composer-remediation-sow-vs-spec` (Q-20, rec SOW governs) · `hpsm-composer-remaining-16-questions` (rec accept as working assumptions). Kam told. **On Q-05's ruling: commission WP0+WP1+WP2 through HPSM's OWN `Launch_Claude.command`, environment checked at boot.** Architecture committed locally only (`f824c76`, `af65839`; no remote, HPSM-40 — if it gets one it must be PRIVATE). Agent's correction to Tuesday's relay: the Policy Preview prints NO framework-mapping columns (Policy Item/Value/Severity/Remediation/UnSupported); the missing mapping columns are Appendix C's. **Score session 32 on the scoreboard at the next checkpoint.** (body: `briefs_staged/2026-09-10_hpsm-rulings-derive-exclude.answer.md`).
- **NexusAI S52 WRAPPED** (`evidence-s52-marketplace-verification/REPORT-S52.md`). Item 1: `docs/Authorized_Users.md` NOT removed. The passwords are legacy and nothing reads them, but **first-run completion does NOT enforce Entra** (the page-1 "Don't show" checkbox leaves `/` and the APIs open until Enforce). **Kam was told 19:3x.** Cards with Kam: `nexusai-authorized-users-md-remove` (rec remove) · `nexusai-marketplace-screenshot-reshoot` (rec reshoot). Branch `ed8b208` in `wt-s51-mktremed` is **NOT PUSHED**. **OWED to a NexusAI seat:** push the branch · the tier-1 QA gate on `ed8b208` (not yet commissioned) · file S52 §5's six tickets **search-before-create** (RD-361/SEC-01 may already carry the open-first-run one) · the RD-369 G1 pinned-list hazard. **Score S52 after the gate.**
- **QA TIER-1 GATE ON `ed8b208` — LAUNCHED 19:36:06, commission receipt verified at rung 5** (the agent's own transcript names its brief). Launcher `2_Project_Files/fleet/qa-agent/launchers/launch_qa_nexusai_s51remed.sh` (guards red-proofed rc 6/7/8/14; the head is LOCAL-ONLY and Tuesday deliberately does not push into NexusAI's repo) · brief `2_Project_Files/fleet/qa-agent/briefs/2026-09-10_nexusai-s51remed-ed8b208-tier1.md` · stdout `2_Project_Files/fleet/briefs_staged/2026-09-10_qa-s51remed-ed8b208.out` (gitignored). **Verdict mails to tuesday-agent@ as `[QA/Datasec-NexusAI -> Tuesday] GATE VERDICT — Marketplace remediation @ ed8b208 (tier 1)`, leading with GO/NO GO for Kam's build.** Its first question is OVER-exclusion: does the new `.dockerignore` drop a file the running product needs. **When it lands: completion check, score S52 on the scoreboard, tell Kam the verdict in one short panel message before his build.** Feature-branch pushes do NOT deploy (`deploy-demo.yml` fires on `main` only, read at `ed8b208`), so the morning seat may push.
- **NAS:** WED-149 · design `1_Project_Definition/Architecture/2026-09-10_nas-two-seat-sync-check.md` · card `nas-shared-folders-owner` (rec Wednesday) · Wednesday released the claim to Tuesday and has the design (mail 09:3xZ).

1. **THE NAS, unchanged since 09:00.** Finder ⌘K → `smb://KAMILADMIN@192.168.20.221/Development`, password, **tick "Remember this password in my keychain"** · then **System Settings → Privacy & Security → Full Disk Access → add Terminal.** Both required, they fail in that order. ✅ **PROMISED: the moment he says done, run `/Volumes/KK_T9_External_HDD/!SYNC FILES/devnas-sync.sh` BY HAND and watch it.** **KAM ANSWERED 15:30: *"I will action nas when I get back home."* So it is WAITING, not blocked — do NOT re-ask him for it; he has it. Watch for his word, then run the sync.**
2. **NEXUSAI MARKETPLACE — he prepares containers TOMORROW.** Verdict: **GO-WITH-CONDITIONS to build, NOT READY to submit.** 🔴 **The first thing he must not do is build from `2_Project_Files`** — that tree's `.dockerignore` is the 26-April version (1042 B vs main's 4074 B), so a build there ships an **untracked RSA private key**, the pen-test report, all six runbooks and 24 extra files. Four more carriers: plaintext passwords + PII (`docs/Authorized_Users.md`), real tenant/app GUIDs **in the setup wizard UI**, a real person named in an LLM tool description sent on every AI request, and 2 of 8 marketplace listing screenshots showing a real person's name. Report: `!CODING/Datasec/NexusAI/evidence-s50-marketplace-review/`.
3. **RD-369 at its cap** — tier-1 gate returned NO GO. Ship-and-ticket recommended, **default if he stays silent**. No round 4 without him.
4. **13B COUNTS 132 FINDINGS AND ENUMERATES ~52.** 80 are tallied and never described. Four INTAKE tickets carry the gap (CWP-4, CPKEY-168, MYP-40, SEC-3). **This also bounds the evidence appendix** — 14 entries because 14 is what the register describes. I told him the appendix covered every finding before I knew this, and corrected it.

## 🔴 LIVE AT HANDOVER (18:5x) — TWO AGENTS RUNNING, both report to tuesday-agent@

1. **HPSM Phase 1 ARCHITECTURE** (pid 56605). Kam commissioned Phase 1 and answered the scoping
   questions himself, verbatim in `briefs_staged/2026-09-10_hpsm-phase1-architecture.md`:
   **"internal" = a COMMERCIAL, DATASEC-BRANDED product sold to Datasec's clients — NOT internal-use**
   (Tuesday read it wrong first); scope is **ALL**, bounded by "everything needed to generate the
   attached outputs"; every attached output included and **branding must be flexible**;
   **full authority to build BUT LOCAL FIRST — no cloud, nothing billable, until he approves.**
   The CRM/finance discovery docx was **attached by accident** — excluded, and the launcher refuses
   if that exclusion, LOCAL FIRST, or architecture-only goes missing (all three red-proofed).
   **Kam has said "go ahead and start building once you're ready" — the build is authorised to
   follow the architecture.**
2. **NexusAI remediation SUCCESSOR** (pid 58713), worktree `wt-s51-mktremed` @ `58184aa`, clean.
   **DONE + committed:** `.dockerignore` at-any-depth · item 2 masking · item 2b publisher IDs out
   of the wizard · item 4 surnames blurred (7 screenshots).
   🔴 **NOT DONE: item 1 — `docs/Authorized_Users.md` is STILL PRESENT.** The check never completed.
   Predecessor **ended its turn waiting on background jobs that never woke it** — work committed
   first, nothing lost. Successor is finishing item 1, verifying what landed, and owes Kam the
   screenshot re-shoot recommendation.

⚠ **THE LAUNCHER GUARDS MATCH LITERAL PHRASES.** Rewriting a prompt silently drops Kam's rulings:
this seat's successor prompt was refused twice — rc 18 (lost "CHECK, NOT AN ACTION") and rc 19
(lost his item-3 "ACCEPTED"). **Both refusals were correct.** Keep those phrases verbatim.

## 🚦 DEPLOYMENT STATE — measured 15:20, not recalled

**NOTHING DEPLOYED TODAY, NOTHING MERGED**, and that is by design: the day was documents, a review
and ticketing, none of which ships code.

    NexusAI origin/main          cd2b543 — unchanged all day
    RD-369 round 3               7cd0907 on rd-369-round3-s49, NOT merged (at its cap)
    branches ahead of main       8, incl. rd-362 (pen-test report exposure) and rd-363 (Key Vault)
    Partner Center               nothing submitted
    Vision Sales Portal (LIVE)   HTTP 302 to login — control: a non-existent azurewebsites host returns 000

🔑 **`rd-362` being unmerged is the SAME GAP the marketplace review found from the other side** —
the exclusions missing from `2_Project_Files`'s 26-April `.dockerignore` are the ones that branch
carries. Two findings, one cause. Worth stating together when Kam rules on either.

⚠ **NOT MEASURED and offered to him: the Azure resource state of NexusAI dev/staging.** No `az` was
run today. If a successor is asked "is it deployed", that is the gap — verify the tenant first
(`az account show`), the launcher scopes `AZURE_CONFIG_DIR` per project.

**Summary + deployment status emailed to Kam 15:21** (his ask arrived by email; answered there and
mirrored to the panel).

## ✅ DELIVERED TODAY, all verified independently rather than on an agent's word

- **Security Review 13A/13B rebuilt + emailed** (to `kamil.kreiser@datasec.com.au` — Datasec deliverables go to the Datasec address, NOT `kreiser.org@me.com`; he corrected me on that). Appendix E/D evidence locations, 147 entries, 663 file:line citations; 185 tables re-widthed, left column 6.00 cm; two blank lines before `###`. Verified against the pre-edit files as controls: page breaks 175→146 and 50→25, exactly the `###` counts; tables/rows unchanged.
- **NexusAI marketplace review** — see above.
- **Jira round** — 16 tickets, 5 projects; **CWP** (10555) and **TDP** (10556) created. Verified in Jira myself: CWP 4 · TDP 4 · CPKEY 3 · MYP 2 · SEC 3 · **RD 0**. 🔑 **Search-before-create saved 17 duplicates: NexusAI's entire 17 findings were already filed (RD-361/362/363 + 2).**

## ⚠ TRAPS — s4's still hold except where struck. These are s5's.

1. 🔴 **NEVER `git pull --rebase --autostash` in this tree.** Still true.
2. 🔴 **`git rebase --continue` WEDGES HERE — three times today, each with ZERO unmerged files** (`git ls-files -u` empty, `--continue` still refusing). **Do not fight it: `git rebase --abort`, then `git -c core.editor=true merge origin/main`.** Resolve collector JSON with `--theirs`, regenerate the two boot digests from source (they are GENERATED — never hand-merge), and **back up `chat_tuesday.json` first and union-check it after**: the merge silently dropped a chat row once today and only the union caught it.
3. ~~Stop putting `0_Brain/dashboard/data/` in your own commits~~ **AMENDED**: still the rule, but when `panel_sync` is dead and Kam is not receiving messages, commit it deliberately and say so. Verify at ORIGIN afterwards.
4. **`panel_sync` FIXED TODAY by Wednesday** — it no longer deadlocks on a conflict, and it advances the other seat's stream from origin when a dirty tree blocks the rebase. **The `(N paths)` undercount is also fixed.** If it skips, look for **your own** dirty files.
5. 🔴 **`setsid` DOES NOT EXIST ON macOS.** `nohup bash … &` only. I killed a healthy loop and its replacement silently failed; Kam's sync was down a minute. Always re-read `ps -o tty=` and branch on it **in code**.
6. **`cockpit.sh launch` still dead here** (registry pins DevMASTER). Launchers under `2_Project_Files/fleet/launch_*.sh` are self-locating and work — copy that pattern.
7. **Agent stdout is now gitignored** (`briefs_staged/*.out`) and the two previously-TRACKED plain `.out` files are untracked (`1a7c5aed`, copies quarantined). **A `.gitignore` rule cannot exclude what git already tracks** — check `git ls-files`, not just the rule.
8. **`board_count.sh` cannot page Jira.** For counts use `POST /rest/api/3/search/approximate-count` — and **a nonexistent project key also returns `{"count":0}`**, so discriminate with `GET /rest/api/3/project/<KEY>` (404 = absent) before believing a zero.

9. 🔴 **BEFORE CHANGING A RECENTLY-REPAIRED FILE, `git log -p` THE REPAIR — do not read the file as it stands.** **The constraint a fix introduces is invisible in the final text; the diff is the only place it is stated** (Wednesday's formulation, 2026-09-10). Reading `wake_watch.sh` today would not tell you that seat-specific hardcoded paths are exactly what was removed from it this morning (`a66e3793`) — and she had read it, then proposed a `~/.claude/...` path that would have re-introduced the family. **A remediated file is at its most fragile in the hours AFTER the fix**, because the repair consumes the attention that would have caught the next change, and **being the person who repaired it is not protection — it is what makes you confident enough to change it quickly.** This is the FILE-level twin of [[2026-09-08_a-new-rule-is-most-dangerous-just-after-adoption]]: same clock, different object.

10. ⚠ **`wednesday_rotate.sh --self` DEFAULTS TO `Launch_Wednesday.command` (line 45) AND BOTH LAUNCHERS EXIST IN THIS TREE.** It is safe ONLY because `Launch_Wednesday.command` does not hardcode a seat: it reads `WED_AGENT` and, when unset, **THE TREE DECIDES** (`basename $PROJECT_DIR` -> `TUESDAY` -> `tuesday`) — this seat's own 2026-09-09 fix. **Verified before rotating: `WED_AGENT=tuesday` in-shell, unset in the tmux server env, so both paths resolve to tuesday.** 🔴 **If that tree-resolver is ever removed or the tree renamed, `--self` respawns a WEDNESDAY seat in Tuesday's tree** — the exact 2026-09-09 misboot. The script's `ROTATE_LAUNCH_CMD` override exists but requires `ROTATE_TMUX_SESSION` set too (both or neither, line 41). **Check the resolver before trusting `--self`; do not assume the default is seat-aware.**

## STANDING

🔴 **Kam reads the STUDIO pane. Verify at ORIGIN, every time.**
🔴 **Datasec client documents → `kamil.kreiser@datasec.com.au`. Fleet/coordination → `kreiser.org@me.com`.**
**Confirm receipt when an instruction lands AND confirm completion when it is done** — both, his 2026-09-10 rule.
**He dictates (Superwhisper).** Read through the noise; where a dictated word decides an action, state your reading and check it, or ask him to type that one word.
**Cross-seat mail is COORDINATION ONLY. Names, not pronouns. Never delete — quarantine.**
🔴 **DO NOT run the wrap's vault step** (`end-of-session.md:50` is `git add -A`; the vault holds Secuura paths).
**Coordinate claims with Wednesday before starting shared work** (Kam, 12:06). She holds: `panel_sync`, the cockpit conversation heldbar, and the decision-panel freeze — **all shipped; the guard CLASS is closed** (swept `cockpit.html`: two deferral guards at `:521` and `:1245`, both fixed, `chat.html` clean). **One untested seam remains and it is `feedBusy` alone** — her harness could not move focus into a collapsed card. `convoBusy` needs no test: Kam's frozen screenshot IS its positive control. If the FEED looks stale, the first question is whether the banner appeared at all.

## WHAT s5 WOULD SAY IF IT COULD SAY ONE THING

**I was wrong twice about why Kam could not see my messages — the project filter, then latency — and both times I was fitting ONE sentence of his rather than all of it.** His screenshot carried the disproof of both in a detail neither Wednesday nor I had mentioned: the panel beside the frozen one was live. **The fix was in code I could have read at any point in those forty minutes.**
**The counterweight, and it is the day's real lesson: every delegated round came back better than the brief.** The document agent found my premise about the spacing was false. The Jira agent found 80 findings the register counts and never describes. The marketplace agent found a private key in the default build. **None of those were things I asked for — they came from briefs that told the agent to check the brief.**
