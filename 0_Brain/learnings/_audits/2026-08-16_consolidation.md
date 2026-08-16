# Consolidation audit — 2026-08-16 (Sunday, run mid-morning after the fleet stood down)

Window: **2026-08-10 → 2026-08-16** (six days since the last audit). Run after both
agents were stood down and the fleet floor was clean, so nothing was competing for
attention. **Kam skims this — nothing below took silent effect except where marked
BUILT, and those were exercised first.**

---

## 🔴 THE HEADLINE: boot cost is ~155K tokens, and it is NOT the lessons

**This is the standing item Kam set on 2026-08-10** ("report the boot cost, number and
trend at every consolidation"). His ruling that day was made at **46 lessons / ~65K
tokens**. Measured today:

| Component | Bytes | ~Tokens | Share |
|---|---|---|---|
| **Lessons** (62 files) | 216,703 | ~54,175 | **35%** |
| **Last 2 daily notes** | 180,181 | ~45,045 | **29%** |
| **Ledger** (`_ledger.md`) | 118,273 | ~29,568 | **19%** |
| **INDEX + decision_queue** | 92,264 | ~23,066 | **15%** |
| identity + people + CLAUDE.md | 11,735 | ~2,933 | 2% |
| **TOTAL** | **619,156** | **~154,789** | |

**Lesson growth:** 34 (08-06) → 48 (08-10) → 56 (08-13) → 59 (08-15) → **62 (08-16)**.

### The finding, and it is good news for Kam's ruling

**Kam ruled: no cutting lessons until a system is found that keeps the best result AND
reduces load.** Six days later the measurement says **the lessons are a minority of the
cost — 35%.** The other **65% sits in three artefacts nobody has been tracking**, and
`CLAUDE.md` already authorises trimming one of them explicitly:

> *"Episodic reads are the bounded ones (Kam, 2026-08-06): read the last TWO daily
> notes in full… Daily notes are what grow without bound — trim there, never in
> `learnings/`."*

**That instruction is not being honoured.** Daily notes ran ~24KB on 08-10/11/12 and then
**103KB (08-13), 117KB (08-14), 63KB (08-15)** — a 4–5× step change. The two read at boot
today cost **45K tokens on their own, nearly as much as all 62 lessons.**

### Proposal to Kam — three deltas, none touching `learnings/`

1. **Daily notes (~45K → ~10K).** Add a short **`## Boot digest`** block at the top of
   each daily note, written at wrap, and have the boot read *the digest of the last two
   days plus today's full note* instead of two full days. The long notes stay on disk,
   greppable and unabridged — only the *default read* narrows.
   **Recommendation: do this first.** Biggest lever, explicitly pre-authorised, and it
   loses nothing because the source is untouched.
2. **Ledger (~29.5K).** It is append-only and has never been trimmed; weights are retired
   at consolidation but rows are not archived. Move rows older than ~14 days into
   `learnings/_archive/_ledger_2026-08.md` — **outside the boot read** (same pattern as
   `_audits/`, which is already a subdirectory and already not loaded), leaving a pointer
   line and keeping every unretired w≥2 row live. **Grep still finds everything.**
3. **decision_queue.md (~23K of the 23K index total).** It still carries the fully-ruled
   **2026-08-04 sitting** as an ARCHIVE section. Move ruled/archived sittings to a dated
   file. **Purely mechanical.**

**Combined, these would take boot from ~155K to roughly ~75K without deleting a single
lesson or losing a single fact.** That is the system Kam asked for before any cutting —
so **(1) needs his nod on changing what boot reads, (2) and (3) are mechanical and I will
do them on his word.** **Nothing has been changed yet.**

⚠️ **Honest caveat:** the token figures are bytes÷4, not a real tokeniser count. Directionally
sound, ±15%. **Stated as an estimate rather than a measurement.**

---

## Ledger review (step 5) — the health metric

**Rows by type, this week:**

| Date | corrections | praise/insight |
|---|---|---|
| 08-10 | 3 | 1 |
| 08-11 | 1 | 0 |
| 08-12 | 3 | 0 |
| 08-13 | **12** | 3 |
| 08-14 | 7 | 1 |
| 08-15 | 4 | 0 |
| 08-16 | 5 | **4** |

All-time: **67 corrections, 19 praise/insight.**

**Reading it honestly.** The 08-13 spike (12) and the decline after it look like
improvement and **I do not think that is what it is.** Correction count tracks *how much
work was under review*, not error rate — 08-13 ran four sessions across two clients.
**The number I actually trust is the one from 08-14 and it has not moved: every single
correction this week was caught by an agent or by a gate, none by noticing.** Today added
five more of mine, all caught by agents.

**So the health metric is not the correction count. It is the ratio of corrections caught
by a MECHANISM to those caught by a reader** — and I have no instrumentation for that.
**Flagged as the metric to build, not claimed as measured.**

**No weights retired this week.** The representations family (w=12) and the provenance
family (now w=9) are both live and both earned promotions rather than retirement.

---

## Changes made (deltas, per the anti-collapse guard)

### 1. BUILT + ARMED — `send_brief.sh` scope-claim gate (w=9 promotion)
**The earned enforcement.** The provenance gate refuses briefs whose **facts** lack a
source; it cannot see a **characterisation appended to a sourced fact** — and *reversible*
is the exact word separating what v1.3 lets me authorise from what needs Kam's signature.
This morning I wrote *"Board config, reversible"* onto a fact the source never
characterised, and **manufactured my own permission to delegate it.**

Now: a brief asserting low risk (`reversible`, `board config`, `low-risk`, `blast radius`,
`contained change`, `local change`) is **refused** unless PROVENANCE carries a line
establishing the blast radius. Narrow by design, per the w=8 lesson that a gate blocking
legitimate sends is worse than no gate.

🔴 **Exercised before arming — and exercising it against REAL briefs found two false
positives that synthetic tests missed:**
- **`demo-only` fired on two legitimate briefs**, where it is a *restriction I impose*
  ("the Kintsugi lift is demo-only"), not a risk claim → **trigger dropped.**
- **`reversible` matched inside `irreversible`** — in the sentence listing what pauses for
  Kam, which is the *opposite* of a low-risk claim → **word-boundary fix**, with `\b`
  support on this grep confirmed by a positive control rather than assumed.

**Final state, all verified:** fires on the one brief that carried the real defect ·
passes the two legitimate briefs · passes all four synthetic branches · does not apply to
`--kind answer`. **In-path (it IS the send path), so it cannot be left unarmed** — no
doctor check needed, unlike the watcher.

### 2. BUILT — `SEND_BRIEF_DRY_RUN=1`
Stops after every gate, before any network call. **Added because a gate whose pass path
can only be tested by really sending is a gate that gets tested in production, once, on
someone else** — on 2026-08-14 a junk gate-test mail reached a working agent and cost a
disavowal.

### 3. New lessons filed (3) and existing ones extended (4)
**New:** `classification-is-the-field-that-grants-authority` ·
`a-recorded-blocker-is-not-a-boundary` (widened same day with *"a recorded exclusion is a
claim too"*) · `an-overstated-record-gets-discounted-wholesale`.
**Extended:** `a-cap-is-never-neutral` (an exclusion set is not neutral either — state the
predicate, not just the bound) · `i-read-representations-they-read-sources` (**the third
switch is EXPECTATION**, and it is the quietest) · `a-check-that-cannot-fail` (**a control
only discriminates if it can fail independently of the check**) · `we-each-have-strengths`
(*"an instrument cannot certify itself, and neither can a session"*).

### 4. NOT merged — deliberately, and it is the week's clearest merge candidate
**Four of this week's lessons are arguably one shape:** a recorded blocker, a recorded
exclusion, an appended classification, and an overstated register row — **each riding on
the credibility of an adjacent verified thing.** They would merge cleanly.

**Kam's 2026-08-10 ruling forbids it** until a system exists that reduces load without
losing anything. **I have cross-linked them tightly instead.** Recorded here as the
standing candidate so the next consolidation does not rediscover it — and note that the
boot-cost proposal above **removes the pressure to merge at all**, since lessons are only
35% of the cost.

---

## Validation of earlier self-changes (DGM guard)

- **Close bell wrap-check (08-10):** ✅ **validated.** Fired 2026-08-13 catching an
  unwritten retro, and **passed cleanly on 2026-08-15** because the retro was written at
  the 50% tripwire. Working as designed in both directions.
- **`board_count.sh` (08-14):** ⚠️ **partially validated, and this week found its limit.**
  It correctly refused caps all week — **and it could not catch today's error**, because
  a correct count of the *wrong set* is invisible to a guard that only asks about
  truncation. Extension filed, no code change (an allow-list discipline, not a mechanism).
- **`wake_watch` ghost-text awareness (08-10, flagged unvalidated):** ✅ **validated
  today** — it fired six times cleanly on real mail and once on a genuinely idle pane
  (NexusAI, ~3 min), which is exactly its purpose. **Still no live ghost-text fire**, so
  that specific branch remains unproven.
- **`cockpit.sh rotate`:** 🔴 **defect found.** It polls for a wrap mail *newer than its
  start*, so **it cannot rotate a session that has already wrapped** — the agent correctly
  declines to re-run the ritual and no such mail ever arrives. **A mechanism whose success
  condition is an event the correct behaviour prevents.** Worked around by hand
  (`tmux kill-pane` + `cockpit.sh launch`); **not fixed in code, deliberately — I would
  rather Kam saw the diagnosis than have me edit the rotation path unsupervised on a
  Sunday.** Next session's item.

---

## For Kam — decisions in this note

1. **The boot-cost proposal (1)–(3) above.** (1) changes what boot reads and is his; (2)
   and (3) are mechanical and I will run them on his word. **Recommendation: all three,
   (1) first.**
2. Everything else in this audit is recorded, not asked.

**Nothing in `learnings/` was deleted, merged or rewritten this week.**
