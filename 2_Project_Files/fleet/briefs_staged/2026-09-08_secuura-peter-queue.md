# BRIEF — PETER'S QUEUE. Kam: "make sure that we action these before the end of the day."

## BLUF
**Deploy accepted — outstanding work, and the KS-987 inode finding is the best thing in it. New item,
and it has a DEADLINE from Kam.** Peter sent two screenshots overnight listing **14 PRs**. Kam's
words, this morning: *"Please look at the following messages from Peter and make sure that we action
these before the end of the day."*

**This goes AHEAD of #892 round 5 and ahead of KS-968** — those have no deadline and this does.

**EVERY ROW BELOW IS PETER'S CLAIM, TRANSCRIBED FROM A SCREENSHOT. Not one of them is a
measurement.** Item 1 is to verify all 14 against GitHub before acting on any.

RULED BY KAM, NOT YET IN AN ARTEFACT
- `secuura-892-round4-passed-but-introduced-two-majors` → **`round5`** (panel 07:08:30): *"ONE more
  narrow round — F-1 and F-2 only, F-2 first"*. **Still yours, still queued — just now AFTER Peter.**
- `secuura-ks968-rotation-three-worlds` → **`separate`** (panel 07:09:37): the one two-boolean
  statement. **After Peter.**
- `secuura-ci-dead-19-days-blocks-your-own-ruling` → **`fix`** (panel 07:07:42): **Kam is fixing
  GitHub billing himself. CI is still dead until he says otherwise** — so "suites: false" on every
  row of Peter's tables is expected, not a finding, and **do not treat any green check as possible.**

## TABLE 1 — Peter's own PRs, CLEAN, ZERO approvals. These wait on US.
    #900  KS-971 (2/2)  "slot-isolate the k6 harness, proven by fault injection"
    #899  KS-971 (1/2)  "observability stack tells the truth about the slot"
    #896  KS-682 (2/2)
    #895  KS-682 (1/2)
    PS #783  —          "sync the test-discipline skill"
**KS-971 and KS-682 are both `In Review` and both assigned to PETER** (Linear, read by Wednesday
2026-09-08 ~07:5x). **#899/#900 are a 1/2–2/2 pair, as are #895/#896 — review each PAIR together;
approving one of a pair alone is how a half-mechanism ships.**

## TABLE 2 — older, and FOUR of these are not code at all
    #785  —              approval at 878081e98, head a27b3f9b3   (STALE APPROVAL)
    #793  KS-365 f/u     amended for QA F-5/F-6                  DIRTY
    #773  QA F-1/3/7/8/10 config-surface walk
    #768  —              "routing to main is the real fix"        ← A QUESTION
    #750  —              your "close it" ask unanswered           DIRTY + A QUESTION
    #758  KS-711         the 2.22.2 pin disagreement              ← A DISAGREEMENT
    #728  KS-671         "wouldn't have caught KS-670"            ← A QUESTION
    #721  KS-660         your framing point unanswered            ← A QUESTION
    #720  KS-487         baseline needs re-run                    DIRTY
**Peter's oldest items are 31 Aug — eight days. The four marked ← are waiting on a HUMAN ANSWER, not
on work, and that is why they have not moved.**

## WHAT I WANT, in order
1. **VERIFY ALL 14 AGAINST GITHUB FIRST** — head SHA, mergeable_state, review state at head, and
   whether Peter's characterisation still holds. **Report where Peter's table and GitHub disagree**;
   a screenshot from 02:19 is hours old and PRs move. Your own 07:4x sweep already agrees with him on
   #785 (stale approval) and on #720/#750/#793 being dirty — **say whether that still holds.**
2. **THE FIVE CLEAN ONES:** review them properly and, where they pass, **APPROVE**. Under the flow
   Kam adopted **the AUTHOR merges** — so approve and leave the merge to Peter, and say in your
   comment that it is his to land. **Review the pairs as pairs.**
3. **THE THREE DIRTY ONES** (#793, #750, #720): a conflict on someone else's PR is not yours to
   resolve unilaterally. **Report what conflicts and why**, and whether it is trivial (a lockfile, a
   changelog) or substantive. **Do not push to Peter's branches without telling me first.**
4. **THE FOUR QUESTIONS** (#768, #750, #758, #721 — and #728 reads like one too): **do NOT answer
   Peter.** Extract each one into a sentence I can rule on or route to Kam: what he asked, what the
   options are, and **your own technical recommendation with its reasoning.** External comms to Peter
   are Kam's signature class — but the ANSWER's substance is ours to prepare.
5. **#785's stale approval** and **#773's config-surface walk** and **#720's baseline re-run**:
   say what each actually needs and how long.

## HOLDS
- **Nothing merges.** Not Peter's, not ours. Approve where earned; the author lands it.
- **No push to a branch you do not own** without telling me first.
- **Nothing goes TO Peter** — no comment addressed to him, no reply, no @mention. Kam sends.
  You may comment factually on a ticket where that is the record, but never as a message to him.
- **CI is dead.** Do not wire, do not re-run Actions, do not read a check state as a gate.
- Kam's signature classes unchanged. The demo is freshly deployed — **do not touch it.**

## DEFINITION OF DONE
A single STATUS mail with: the 14 verified against GitHub (and every disagreement with Peter's
table named), what you approved and why, what the three conflicts actually are, and **the four
questions written so Kam can rule them in one read**. That last part is the deliverable Kam's
deadline is really about.

PROVENANCE:
- the 14 rows | two WhatsApp screenshots from Peter, relayed by Kam 2026-09-08 ~07:5x, transcribed to `0_Brain/reference/2026-09-08_peter-pr-queue/peter-queue-transcribed.md` | read 2026-09-08 08:0x — **a transcription of an image; verify every row**
- KS-971 `In Review`/peter · KS-682 `In Review`/peter · KS-365 `In Review` · KS-487 `In Progress` · KS-671 `In Review` · KS-711 `In Review` | Linear GraphQL, direct read | read 2026-09-08 ~07:5x
- #785 stale approval, #720/#750/#793 dirty — YOUR measurement, not Wednesday's, and it independently agrees with Peter | your own `gh api repos/Secuura/Distributed_Secuura/pulls --paginate` sweep, reported in your 07:4xZ mail | read 2026-09-08
- Kam's deadline + his three rulings | dashboard chat_log + `kam_rulings_today.sh` | read 2026-09-08 07:07–08:09
- scope/reversibility: an approval is reversible (dismissible) and NOTHING merges under this brief; the blast radius is bounded by the HOLDS, which forbid every irreversible verb — no merge, no push to a branch you do not own, no comment to Peter | the HOLDS section of this brief, enumerated | read 2026-09-08

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-08 08:10
