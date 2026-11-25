---
date: 2026-11-25
type: correction
source: "Kam, live board 2026-11-25 11:47 (view=tuesday), verbatim: \"this is not a small oversight. Please be more careful in checking things.\" — after four unchecked statements from the Tuesday seat in one morning"
status: live
tier: W
supersedes: ""
---

# Check every sentence to Kam at its source before it goes; a tool's warning on it is a stop, not advice

**The lesson:** A statement to Kam (or steps for anyone he passes them to) is sent only after the fact in it has been checked at its live source in the same action. When my own tooling warns on a sentence (an absence claim, an unmeasured count), I either name the measurement or rewrite it; I never send past the warning. A wrong statement corrected afterwards is not "small": it is the thing he relies on being right.

**Context:** In one Tuesday session (s326, 2026-11-25) four things I sent Kam were unchecked: (1) "in a terminal on the Mac mini" (from a stale pickup note; the seat runs on Kamil's Mac Studio, M5 Max, 128 GB); (2) "the OXPd design needs updating for 1.9" before reading his own 24 Nov ruling on that subject; (3) Security Manager sign-in steps saying `https://localhost:7637/` with no word that this is opened inside the Bastion desktop, which confused him and would confuse the two staff; (4) "there's no direct Azure link to Security Manager", false (the console port he kept open is one). chat_reply.sh printed an ADVISORY absence-claim warning on exactly sentence (4) and I sent it anyway; I then framed the fix as a "small correction". He corrected the framing: it is not small.

**Diagnosis:** Many parallel threads (five agents, four new Kam requests in an hour) at a fast reply pace; replies were composed from my notes, kits and memory instead of a read made for the sentence. The guards that exist were advisory and I treated them as noise. Not context saturation: ctx read 52-59% by the statusline over these errors.

**How to apply:**
1. Before any message to Kam: each fact in it (machine, path, URL, ruling state, "no/none/only/never") has a read in the same action, or the sentence says "unmeasured". Rulings: run `decision_queue.sh prior` on the subject before a conclusion about design or scope.
2. Steps for people outside the team (staff, HP, customers) are read once by an independent checker (an agent with no context but the steps and the system's record) for "would this person know where to type this?" before they reach Kam.
3. chat_reply.sh's absence-claim check is a REFUSAL (rc 6) unless the sentence states what was measured or `CHAT_ALLOW_ABSENCE="<measurement or reason, 15+ chars>"` is set, which is logged to fleet/state/absence_overrides.log (BUILT same day, 2026-11-25; proved by Tuesday in CHAT_DRY=1: fire rc 6, quiet rc 0; arms A1-A11 pass; .pre-1125-absenceblock copies kept). A quotation of a retracted claim is the expected override case.
4. Corrections are named for what they are, never minimised ("small", "minor") in a message to Kam.
5. One Kam thread answered at a time; agent wakes wait behind his message.
6. **Test, don't hedge (Kam, live board 11:53, verbatim: "You should have tested. I did. It works").** When a fact can be measured quickly and safely (a GET of a sign-in page, a read-only list), measure it before the message; "I haven't tested it" is acceptable only when the test is unsafe, approval-class or out of reach, and the message says why.

**Related:** [[2026-08-14_i-read-representations-they-read-sources]], [[2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it]], [[2026-09-10_steps-to-kam-are-a-claim-about-his-screen]], [[2026-09-04_decisions-held-narration-drifted]], [[../people/kam]]
