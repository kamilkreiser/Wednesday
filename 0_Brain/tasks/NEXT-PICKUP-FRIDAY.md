---
date: 2026-11-16
type: pickup
seat: friday
scope: BOTH Secuura and Datasec, from Kam's laptop. Claim each project before driving it (wed_claim.sh)
status: live
written_by: Friday, WRAP 2026-11-16 ~22:5x (Kam: "in that case, wrap up but will the next reboot start in fable?")
supersede: replace wholesale; previous = NEXT-PICKUP-FRIDAY.md.pre-1116-2255 (the 16:57 wrap), read on demand only
---

# NEXT PICKUP — FRIDAY

**The tree is at `/Volumes/Laptop-DEV/FRIDAY` (machine: Kamils-MBP).** Quote every path.

## 🔴 FIRST ACT — check the model, then work the review cards

1. **Which model is this seat on?** The shared launcher passes `--model opus` to every seat (Launch_Wednesday.command
   line ~971, Kam's 2026-10-21 ruling), so Friday boots on Opus 5.5 unless the launcher changed. Card
   `general-friday-boot-on-fable-1116` asks Kam: a = Friday-only Fable boot (rec), b = Fable for the next launch only,
   c = keep Opus. **If he ruled a or b:** claim `WED tooling: Launch_Wednesday.command Friday-only model — Friday (laptop)`,
   add a seat condition (AGENT=friday → `--model fable`, keep `--fallback-model opus` if the 09-05 shape is used),
   back up the launcher as `.pre-1116-fable`, `bash -n` it, mail BOTH sisters that the shared launcher changed (their
   seats unchanged), release the claim. Never `/model` a pane. Under Kam's 22:50 rule
   (`learnings/2026-11-16_suggest-when-to-switch-to-the-newest-fable.md`), say on the panel which model the seat is on
   and whether the day's work warrants Fable.
2. Run `kam_rulings_today.sh` + `decision_queue.sh list open`, then rule every tapped card in the store.
3. **Claude to Claude (General) review: Kam said 22:47 "I have gone through the document and it looks good. lets start
   with the things that need clarification. please put each on the fleet activity".** 15 clarification cards are open,
   each rec a with a stated default (nothing is built by default):
   `general-c2c-{d1-name, d2-licence, d3-relay, d5-reads, d6-trust-limits, d7-identity, d8-review, d9-browser-agent,
   d10-platforms, d11-two-parties, d12-audit, language, repo-home, build-model, nightly-tests}-1116`.
   Plus the 16:5x pair: `general-c2c-design-go-1116` (start M0) and `general-c2c-v044-withdraw-rotate-1116` (D4; Kam's
   own action). Approval-class (money / public posture): d3 relay, d8 review, nightly-tests; none is priced (U14).
4. When the clarifications are ruled and the go card is a: Friday does NOT build. Read the project's own CLAUDE.md and
   Launch_Claude.command (`/Volumes/Laptop-DEV/!CODING/Claude to Claude/claude-bridge`, read-only, not a git repo), set
   up the repo per the repo-home ruling, model per the build-model ruling, then brief a project agent for M0 (Appendix B,
   U1–U13). Kam's GitHub identity for a General project is NOT Secuura's nor Datasec's: confirm it at point of use.

## Where everything is

`0_Brain/reference/2026-11-16_claude-to-claude/` — `00_requirements.md`, `01_existing-code-review.md`,
`02_prior-art-research.md`, `03_architecture-design.md` (+ PDF, shared to Kam f-a27bbae499). **Friday has now read the
whole design** (sections 1–13 and Appendices A–B; 14 is a traceability table). Her five review points are in the
2026-11-16 daily note (22:44 entry): Rust toolchain, relay operator/scam risk, phase-2 workflow change, nightly test
cost, M0 before build. Linear WED-162.

## OWED (Friday)

- 🔴 **Kam could not see ANY Fleet activity card at 22:53** (screenshot in his board message f-9f81b3c88483: "Needs
  you (0)", "1050 cards synced", "✕ clear" drawn with no project chip lit). Probable cause: a stale saved project
  filter in his browser that the board does not draw as a chip (`dashboard-cloud/app/static/index.html` renderFilters
  ~694-695 only draws filters whose agentOfProject() is the active seat; projOk ~809 still applies all of them). Kam was
  told to tap "✕ clear" (bf-7d53a4eb58e88). FIRST: ask whether the cards now show. Then fix the board (draw every active
  filter, or drop filters outside this view), claim first: the live board is shared fleet tooling, so mail both sisters;
  its deploy goes to the board's Azure app, so read dashboard-cloud/README.md for the deploy path and whose grant
  covers it before deploying. Ledger w=3 (201 is storage, not sight).

- Sister acks still outstanding: the shared inbox-scope hook change (e30563fa5d; threads fa7f0784… Wednesday,
  412cc0c8… Tuesday) and Kam's 16:37 Composer ruling mailed to Tuesday (thread f0f1f881…). Check friday-laptop-agent@.
- From 10-16, said once, not carded: Spotlight Privacy + Disk Utility First Aid on Laptop-DEV; wordsplit hook refuse
  unquoted `$(ls …)` in a `for` list (ledger w=5, 10-15).
- Stale OPEN claims in `wed_claim.sh list` on Kamils-MBP / Kamils-MacBook-Pro (09-08 wed_claim.sh itself, 09-25
  live_chat_poll arming — DONE in the launcher, 10-10 Friday tooling): verify each is Friday's, then release.
- Linear WED-48 and WED-147 overdue; the WED board has not moved since mid-September.

## Standing facts a cold seat needs

- Friday drives NO Datasec and NO Secuura project. HPSM-POC, MPS calculator, Security Composer, HPSM records are
  Tuesday's (since 10-15). Friday holds only `General/Claude to Claude — Friday (laptop)` (kept across this wrap).
- The board poller `live_chat_poll.sh --seat friday` (30 s) is armed by the shared launcher at every launch and doctor
  fails without it; Kam asked 22:4x that it be always on and that receipts go on the panel. Receipt every board message
  on the panel the moment it is read.
- The by-tier boot digest is ~700 KB: read every headline (`grep '^## '`), open a lesson when its rule fires. ctx 14%
  after that load (both 11-16 boots).
- Never run `tools/panel_sync.sh` bare (it does not return). Push own commits with `git push`.
- The prior-ruling gate refuses on generic words (name, build, home, audit, boot…) from unrelated cards; override
  with the reason in the BLUF, after reading what it matched.
- No live grant drives Friday work. WEEK-INSTRUCTION-FRIDAY lapsed 2026-09-26.
