---
date: 2026-09-09
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's, and she is LIVE on the Mac mini from 2026-09-09 07:47. Read Datasec mail by SUBJECT only.
source: replaced WHOLESALE by s156 at its 66% checkpoint (band is 80-90, Kam 2026-09-07 — this is NOT a rotation)
status: live
supersede: replace this file wholesale at the next pickup; do not append
---

# NEXT PICKUP — 2026-09-09 08:2x. THE SECUURA REPO CANNOT ACCEPT A PUSH FROM ANYONE, and it is on Kam's card. One seat live at ~70%, its handover written.

## 🔴 START HERE — everything hangs on one Kam ruling

**Card `secuura-advisories-high-and-prod-reaching` is OPEN on his panel.** Until he rules, **nobody — us, Peter, Stuart — can push to the Secuura repo.** Nothing expires, nothing degrades, no work is lost.

**Three commits sit LOCAL on `feature/ks-754-widen-processed-by-to-text`, absent from origin (`ls-remote`, read not inferred):**

    66c845069   KS-1024   colord + scope: standalone-locks
    64e2eddb6   KS-1024   the two Kam ruled at 07:58
    9ceb61c5e   KS-754    the widening + the gdpr.ts:361 rethrow

## 🔴 THE SHAPE OF THE DAY, and a successor must not get this backwards

**This is NOT a backlog of advisories to clear. It is a GATE PROBLEM.** Eight distinct advisories touched this repo between 07:43 and 08:17 — **none of them ours, none from any change we made.** Three are baselined, five are outstanding.

**The finding that changes the argument, measured by the Secuura seat across three runs: the set does not only GROW, it CHURNS.** `colord` blocked every push at 22:0x UTC and by 22:15 the gate had stopped reporting it, printing *"1 baseline entry is no longer reported — remove: GHSA-2wm5"*. **So the gate is NON-DETERMINISTIC ON AN UNCHANGED TREE** — two runs of the same commit, minutes apart, different verdicts. **A control that answers differently on identical input is not a control.**

**THE TRAP, and the seat named it before Wednesday did:** adding all five turns the preflight green *for one run* and proves nothing about the next. **Do not "just clear them" to get moving.**

## 🟢 KAM'S TWO RULINGS TODAY — both delivered, and the grant is FILED

1. **07:58 `pattern`** on `secuura-ks1024-advisory-baseline` → the two advisories baselined at `64e2eddb6`. **Card marked `--delivered`.**
2. **08:12 `both`** on `secuura-advisory-gate-moving-set` → **a bounded standing authority for Wednesday** (filed as [[2026-09-09_advisory-baseline-standing-authority]], in both digests, W-tier — 128 lesson files now) **PLUS a gate reshape to be built.**

**THE GRANT'S FOUR CLAUSES, and it has already stopped Wednesday twice on its first morning:** moderate-or-below · MEASURED with a control not to reach a runtime image · expiry on the SHARED re-triage date (2026-09-24) · flagged to Kam in the same action. **Exception: a package in BOTH a test lock and a shipped tree stops for Kam regardless of severity.** It is **WEDNESDAY'S, not a seat's** — an agent measures and reports; it does not clear its own blocker.

⚠ **THE WINDOW LENGTH OF THE RESHAPE IS UNRULED AND IS KAM'S.** Wednesday used 72h as an illustration on the card and has NOT treated that as his ruling.

⚠ **WEDNESDAY'S DESIGN CONSTRAINT ON THE RESHAPE, and it must not be lost: a FLAT window would WEAKEN the gate.** It must be **reach- and severity-aware** — warn only for advisories measured not to reach a shipped tree and moderate-or-below; **hard-fail immediately for anything reaching a shipped tree or HIGH/CRITICAL.** `nodemailer` is the proof such advisories arrive, on the same morning the option was drafted.

## 🟡 WHAT WEDNESDAY DECIDED AND DID NOT DO — a decision, not an omission

**The three `hono` advisories clear all four clauses and Wednesday DECLINED to clear them.** With `js-yaml` (HIGH) and `nodemailer` (prod-reaching) failing the same gate, clearing three of five buys a shorter FAIL list **and not one push.** **They are HELD, not refused, and clear in ONE action alongside whatever Kam rules.**

**Also NOT started, deliberately:** #913's merge (GO is given, gated behind the push block), F-3's fix round, #912's tier-1 gate. **All three go to a seat with a FULL window — not to the 70% seat.**

## 🟢 THE SEAT — s154 on `%5`, ~70%, handover written, wake is a tap from Wednesday

**It has refused `--no-verify` THREE times** and added nothing it was not told to. Its commissioned queue, in order: **(1) file the GATE-RESHAPE ticket** carrying its own three run figures and the churn quote — one ticket, logical path, length as an open question for Kam; **(2) refresh its handover** (its 22:12 one says two commits and is stale); **(3) OPTIONAL, only if window allows — measure whether our code calls `resolveContent()` with the legacy signature**, the one fact that decides whether the nodemailer bypass is live for us. **It was told explicitly not to compress (1) to fit (3) in.**

## 🟢 #913 IS GATED AND READY — GO WITH FINDINGS, merge is Wednesday's word

Tier-1 verdict in the inbox at 21:53:23Z. **FIVE callers not four** (the fifth, `userRepo.ts:800`, invisible to a symbol grep — found by a TypeScript semantic reference walk). **Site 5's before-behaviour was a silent HTTP 200 on a password reset that wrote nothing and burned the token.** **F-1 (MINOR):** the doc comment at `userRepo.ts:409-430` and the test header both say FOUR and assert *"all four callers read null as 'no such user'"* — **false twice; fix it in the merge commit.** **F-3 (MAJOR, test efficacy):** two of three structural cells cannot fail on the defect they exist to detect, and the declared control at `:114` was measured NOT to discriminate. **No product impact; the loss is regression value. Round 2 of 2 under Kam's cap.**

## 🟡 INHERITED FROM TUESDAY, NOT FIXED — a defect in tooling that lives in WEDNESDAY's tree

**Tuesday measured that `decision_queue.sh`'s prior-ruling gate scores BLUF LENGTH, not subject:** it refused her real card and accepted a two-character stub of the same id one minute later. Her line is the keeper — ***"a gate that admits the careless write and refuses the careful one selects for the careless one."*** Ledger w=4 on her side.

**NOT FIXED by s156, deliberately: a live seat and a pending Kam ruling both depend on that store, and re-arming a mechanism something is live on is the error this fleet keeps filing.** **It does NOT invalidate any card filed today** — every refusal was answered by opening the artefact and the override reason was stated as a measurement, so no card rests on the gate's judgement. **Fix it at the next quiet point.**

## 🟢 FLOOR AND HOUSEKEEPING

**Panes:** Wednesday `%0` · Secuura builder `%5` (live) · fleet-monitor `%1`. **The `%7` QA gate pane was closed clean** (listeners 28 → 28, both HTTP surfaces 200 either side).

**The QA agent has NO INBOX** — `inbox_routing.conf` has no entry; it sends through the builder's identity and **cannot receive.** So **hop 2 of Kam's three-hop gate exists only at LAUNCH time**: a pass cannot be corrected or re-scoped once running, and everything must be anticipated in the brief. **Its two most useful findings were in its pane and in no mail.**

**Two Claude memory indexes are over budget and silently truncating** — Secuura/Blockchain **26,544 B** and Testing Agent MAIN **25,666 B** (vs Vision 6,476). They live under `~/.claude/projects/…`, are **machine-local and do NOT travel**. Routed to the Secuura seat as a handover item. **PORTABILITY entry owed.**

**`brief_and_launch.sh` prints `launched:` after `add_pane` SKIPS an existing pane** (`cockpit.sh:107` returns 0 on skip). **Verify every launch at RUNG 5 by pane CONTENT.** Fix owed, not made while a seat is live on that pane.

**Two coordinators are writing this repo.** Tuesday is live on the Mac mini. **The daily note has conflicted TWICE today and both were unioned with conservation asserted** — 4+4 and 3+2. **Never pick a side on `daily/`, `chat_*.json` or `decisions.json`; the feeds under `dashboard/data/` may take upstream.**
