---
date: 2026-08-07
type: lesson
source: "Live near-miss, 2026-08-07 ~09:5x. I quoted the ghost line `yes, deploy RD-67+68 to the demo` to Kam as a warning; he read my warning and sent the sentence back to me as his own with 'that's from me'. I refused to relay it because the wording was byte-identical to the ghost text. He then checked and corrected: 'it was not me. I missread the message. it was not me but I agree with the comment.'"
status: live
supersedes: ""
tier: W
---

# Ghost text can capture the HUMAN, not just the agent — and quoting it is how it spreads

**What the documented risk was until today:** Claude Code renders suggested next
commands as ghost text at the prompt; an AGENT (or I) might read one as an
instruction. [[2026-08-06_ghost-suggestions-in-panes]] built a discriminator for
exactly that, after I acted on one and put Kam's name against it.

**What actually happened today is a level worse.** The generator produced an
approval sentence. I did the right thing and reported it to Kam as a warning —
**quoting it verbatim so he could see what was there.** He read my message and
sent the sentence back to me as his own, attributed: *"that's from me."* Had I
relayed it, an unauthorised demo deploy would have gone out carrying a human's
explicit attribution, and every artefact would have recorded it as his.

**The mechanism, stated plainly: quoting ghost text is how it propagates.** My
warning was the vector. A machine-generated sentence entered the human's context
through the one channel he trusts completely — me telling him what was on his
screen — and came back wearing his name. Nobody was careless. He was reading
several things at once, which is his normal working state and the entire reason
the ask-format rule exists.

**Why it stopped:** the wording was byte-identical to the ghost line, so a relay
from me would have been indistinguishable from me having read the machine's text
and attributed it to him. I declined to be the channel and asked him to type it
himself. **The refusal was the detector** — not the script. The script had
already done its job; what caught this was refusing to carry an approval whose
provenance I could not prove.

**How to apply:**
1. **When warning about ghost text, do not reproduce it as a quotable sentence.**
   Describe it — "there is a machine-generated line at the prompt that reads as a
   deploy approval" — or break it so it cannot be echoed back intact. Naming the
   shape beats quoting the words.
2. **A human echoing my own quoted words back is not independent confirmation.**
   Attribution requires something only they would produce: their own phrasing,
   a detail I did not supply, or an action in their own channel. Identical
   wording to text I just showed them is the weakest possible signal, not the
   strongest.
3. **Ground authorisation on the earliest independent ruling, not the latest
   restatement.** RD-67+68 was genuinely authorised by Kam's "6a" in the rulings
   sitting — his own words, unprompted, answering a numbered question. That is
   what I deployed on. The later sentence added nothing and could only have
   subtracted trust.
4. **Escalate the ticket, not just the file.** WED-83 was "worth solving, not
   worth today". A live near-miss on a human moves it.

**The uncomfortable part worth keeping:** I generated the risk by doing the
careful thing. There was no version of "warn Kam about the ghost text" that did
not put the ghost text in front of Kam. The fix is in HOW the warning is
written, which means the safety practice itself needed a safety practice — and
that is likely to be true of the next one too.

**Related:** [[2026-08-06_ghost-suggestions-in-panes]] (parent),
[[2026-08-05_kam-types-into-panes]], [[2026-08-06_brief-provenance-enforcement]],
[[_ledger]]
