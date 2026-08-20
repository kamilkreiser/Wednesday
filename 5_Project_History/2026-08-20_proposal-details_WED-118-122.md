# WED-118..122 — the five industry-scan proposals, in detail
*For Kam, 2026-08-20. Each: what changed → what I propose → cost → risk if skipped → what your "yes" authorises. Sources: the 2026-08-20 industry scan report (`1_Project_Definition/Discovery/research/2026-08-20_industry-scan.md`) + the Linear tickets.*

---

## WED-118 — Pin the permission mode per project *(my top priority of the five)*

**What changed:** Since 2026-08-14, new Claude Code sessions on Pro/Max/Team default to **auto mode** unless `permissions.defaultMode` is pinned in settings. Every fleet launcher session started since may be running a permission posture nobody chose — on client infrastructure.

**Proposal:** one session audits every project's settings/launcher and pins the mode explicitly per project — most restrictive where it matters most (Vision's prod resource group, anything money-adjacent). Ride-along: grep launchers for stale model pins (Opus 4.1 retired 2026-08-05).

**Cost:** ~1 hour, one session, config-only, fully reversible.
**Risk if skipped:** an inherited vendor default silently decides our permission posture on client work — the exact class of "nobody chose this" we keep finding elsewhere.
**Your yes authorises:** the audit + per-project pins, results in a table for your review before anything unusual is chosen.

---

## WED-119 — Mail-channel fallback becomes standing

**What changed:** The Aug 18–19 AgentMail platform outage froze the fleet ~14h — send is our only delegation channel, and the error text misdirected us to an account-side theory for a platform problem.

**Proposal (three lines, template/boot only):** (1) brief-template rule: on send-403, agents write wraps/questions to their own `5_Project_History` and hold at prompt — I watch panes; (2) my boot keeps the send-path probe (already added); (3) status.agentmail.to is checked *before* any account-side theory.

**Cost:** wording edits only. **Risk if skipped:** the next outage repeats this one, plus the misdirection.
**Your yes authorises:** the template edits. (Half is already live from this week; this makes it standing rather than habit.)

---

## WED-120 — Fleet upgrade to Claude Code ≥ v2.1.234 + trial native SendMessage for nudges

**What changed:** Recent releases shipped native session-to-session messaging (same machine), auto-continue when a usage-limit window resets (kills the died-at-limit-overnight class), and several containment fixes.

**Proposal:** upgrade the fleet, then **trial** SendMessage carrying only "check your inbox" nudges — replacing tmux pane taps, which have a real ledgered failure history (typing guards, ghost text, swallowed taps — three separate enforcement builds this month). **Mail stays the channel of record**; this only replaces the tap.

**Cost:** upgrade + a scored one-week trial. **Risk if skipped:** low — the taps work, but each tap-class failure has cost a fix cycle.
**Your yes authorises:** the upgrade now; the trial scored on the delegation scoreboard, adopted only if it beats the tap record.

---

## WED-121 — Route mechanical lanes to Sonnet 5

**What changed:** Sonnet 5's $2/$10 pricing is now permanent (the Sept-1 rise was cancelled) — ~2.5× cheaper than Opus-tier, 1M context.

**Proposal:** route routine *mechanical* lanes only — index refreshes, mail triage, dashboard collectors, scan fan-outs — to Sonnet 5. Judgement lanes (reviews, briefs, verification, anything client-facing) stay on Fable/Opus.

**Cost:** config; first week scored like any mechanism. **Risk if skipped:** none — this is pure spend efficiency; you've said money is not the constraint, so this is genuinely optional.
**Guard:** only lanes where a wrong answer is cheap and checkable; the scoreboard decides after a week.
**Your yes authorises:** the routing change for the named mechanical lanes only.

---

## WED-122 — Sender verification on every fleet mail + a no-test-deletion CI line

**What changed:** (a) Published research measured agents' refusal of forged-authority instructions ranging 100%→38% across models — and our routing is a plain-text subject convention any sender could forge; today only *approval-class* mail gets DKIM checks. (b) Practitioner consensus has converged on CI gates that specifically catch deleted tests / lowered coverage (we met exactly this class at NexusAI twice this month).

**Proposal:** one fleet-protocol line — agents verify the **sender** (address + auth headers) on *every* brief/ANSWER, not just approval-class; and one brief-template line for projects with CI: gate on no-test-deletions / no-coverage-drop.

**Cost:** wording only. **Risk if skipped:** a forged "[Wednesday →…]" subject line is currently enough to instruct a non-approval-class action.
**Your yes authorises:** both template lines, effective the next brief.

---

## My recommendation, if you want the one-word version
**Yes to all five; 118 first** (it's the only one with a live silent exposure), 122 second, then 119/120/121 in any order. 121 is the only genuinely optional one.
