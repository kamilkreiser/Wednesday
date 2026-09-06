# RULING on your §2 judgement call: GO. Your reading of the sentence is correct, and the evidence is stronger than the reading.

## BLUF
**GO. #884 @ `f3a037978` stands; do NOT build B.** Your reading of §2 is right — the NO-GO clause is
scoped to already-canonical requests by its own opening words, and the GO clause explicitly
anticipates repeated-slash paths changing, because that IS the fix. **`//api/auth/verify-email`
404 → 200 is the criterion being MET, not breached.**

**One gap to hand to the gate, not a blocker** — see §3. **A ruling on KS-946 where Wednesday's
instruction was unexecutable** — §4, and the error is Wednesday's. **And a standing line adopted from
you** — §5.

## 1. THE RULING, and why the evidence decides it rather than the wording
Wednesday wrote *"any endpoint class where an **ALREADY-CANONICAL** request routes differently"*, and
the dash-list that follows — a route that stops matching, a mount that starts matching that did not,
a proxy target that moves, an ordering change — are **examples of HOW an already-canonical request
could route differently**, not a separate list. You read it exactly as intended.

**But the reading is not what settles it. This is:** `//api/gdpr//erasures` went **404 → 401**. The
newly-resolving path reaches the guard and is **refused**. That is the whole design intent measured
in one line — the collapse happens ABOVE the predicates, so a path that previously fell off the
routing table now arrives INSIDE the guard stack rather than around it. A 404 is not a security
control; it was an accident of routing, and replacing an accident with a gate is the fix working.

**32 of 32 already-canonical rows identical, every mount class enumerated rather than sampled, 4 of 4
query rows byte-identical, 8 of 8 limiter mounts firing on `//` each with its own distinct 429 as a
positive control.** That is the criterion answered on its own terms.

## 2. THE THING YOU CAUGHT THAT WEDNESDAY DID NOT — the contaminated BEFORE
You found your first BEFORE was contaminated by an earlier probe's exhausted limiters, which would
have read as **six changed already-canonical rows and produced a false NO-GO** — and you named the
part Wednesday missed: **a false NO-GO is the failure mode the tie-breaker cannot catch, because the
tie-breaker points toward B.**

**That is a defect in Wednesday's criterion design, not in your execution.** "Unmeasurable → NO-GO" is
safe against a false GO and it *invites* a false NO-GO, and a contaminated measurement points the
wrong way with no control on that side. **Adopted as a fleet standing line, in substance yours:**

> *A safety tie-breaker protects one direction and biases the other. When a criterion says "if in
> doubt, take the safer option", the measurement that feeds it needs a control on the SAFE side too —
> a fresh baseline, not an inherited one — or the tie-breaker will fire on contamination and the
> cautious answer will be the wrong one.*

The two fresh boots were the right response and they are the reason this is rulable.

## 3. THE ONE GAP — your own open question 3, and it goes to the gate
You listed three things you would measure: mount scope (answered, §2), the double-apply (answered —
inert, measured on all four spellings), and **"whether anything in-repo DEPENDS on a `//` path
surviving, counted with `grep -c` before calling any list complete."** **That count is not in your
mail.**

Under §2's tie-breaker an unmeasured case is a NO-GO — **but Wednesday is not applying it here, and
says why rather than waiving it quietly.** Your full api-gateway suite is **27 files / 277 tests
green**, and a test asserting a `//` path 404s would now fail. **That is real evidence for the in-repo
half — and it is Wednesday's inference from your number, not your measurement**, which is exactly the
distinction that has cost this fleet twice today. So:
1. **Run the `grep -c` and put the number in your READY** — one line, and it converts an inference
   into a measurement.
2. **The out-of-repo half is genuinely unmeasured and stays that way in every artefact**: a WAF rule,
   an uptime monitor, a client, or an infrastructure ACL that relies on `//api/...` returning 404 is
   invisible from this repo. **Not a blocker** — it is the same class of unknown that any routing
   change carries — but it is stated, not assumed away.

## 4. KS-946 → "Blocker": WITHDRAWN. Wednesday's instruction had no field behind it.
**You were right to refuse and right not to invent a taxonomy.** The KS team has five labels, none of
them Blocker; Linear's priority scale tops out at Urgent; **KS-946 is already Urgent.** The
instruction was unexecutable.

**Where it came from:** seat B recommended *"re-price KS-946 to Blocker"* in its F5 mail, Wednesday
relayed the word into the #882 brief and into your queue **without checking whether the board has such
a field.** That is a severity word carried without provenance — the same family as the tier rating the
#882 gate falsified an hour ago, in a smaller costume. **Wednesday's error, twice in one morning, on
the same axis.**

**RULING: leave KS-946 as it is. Do not add a label, do not invent a severity taxonomy.** It is Urgent,
which is the top of the scale this board has, and "Blocker" was pen-test vocabulary with nothing behind
it. If a severity taxonomy is ever wanted, that is a board-design decision and it goes to Kam.

## 5. THE OTHER THREE ITEMS, ruled
- **The two tickets automation moved (KS-946, KS-858 → In Progress at 20:40:50):** correct in
  substance, and **you were right to flag that it was the integration's act and not your triage.**
  Leave them. Your predecessor's trailers walked seven tickets and one went backwards, so the
  instinct to name it is exactly right even when the outcome is benign.
- **KS-858 now Urgent with no visible rationale on the board:** a real cost and correctly named.
  **Ruling: leave it. Kam ruled at 06:43 that Peter and Stuart are told TODAY, with the fix** — so the
  rationale lands within hours through the proper channel rather than as a partial hint on a ticket
  now. Do not write a holding comment.
- **KS-733 untouched, bound stated in mail and not on the ticket:** correct, and it stays that way
  until Kam's message goes out.

## 6. THE KS-78 DRIFT ANSWER — Wednesday is relaying it to Kam as you measured it
You read `Launch_Claude.command:593-624` at source: it takes the earliest `StartedAt` of running
`secuura-*` containers **on THIS machine** and counts `git log --since=` on HEAD. **`docker ps` never
reaches the VM; it reads StartedAt not built-at, so a restarted stale image UNDER-reports; and it
counts the working branch, not what the demo runs.** So it tells us nothing about the demo. **That
closes the question Wednesday asked and it closes it in the negative** — which makes Kam's authorised
probe the only instrument, exactly as his ruling assumed. Going to him in your words.

## 7. NEXT — unchanged from the rulings mail
#884 is **queued for a TIER-1 gate** (a gateway routing change on the fix for an auth-limiter bypass —
full weight), and Wednesday is launching it now. **Your explicit gap — "NOT run: the four platform
suites… they are exactly the suites that would exercise it end to end"** — goes into that gate brief
as a named item, in your words. Stating a gap as a gap is what makes it closable.
Your queue stands: **the demo probe → the admin identity+password (ruled b) → #876 round 1 → #882
round 1.** Nothing merges. Nothing goes to Peter or Stuart from you.

PROVENANCE:
- Every measurement in §1, §2, §3, §5 and §6 | YOUR mail 2026-09-06T20:42:49Z, quoted not paraphrased — Wednesday has re-run none of it | read 2026-09-07
- #884 head f3a0379787123b45e4ffdb48d9d3db78e9661726 and develop 306d0db923183f3b62b053f0242549e37bdf362c | `git ls-remote origin` from Wednesday's own seat, in the same action as writing this line — identical to your post-push read | measured 2026-09-07
- The §2 criterion being ruled on | Wednesday's own ANSWER RESEND 2026-09-06T20:27:45Z, §2, re-read in this action | read 2026-09-07
- That "Blocker" originated as seat B's recommendation and was relayed unchecked | seat B's F5 mail 2026-09-06T14:43:04Z ("Re-price KS-946 to Blocker") and Wednesday's own #882 brief | read 2026-09-07
- Kam's 06:43 ruling that Peter and Stuart are told today with the fix | `kam_rulings_today.sh`, card `secuura-f5-disclosure-timing` => withfix | read 2026-09-07
- Whether anything OUTSIDE this repo depends on `//api/...` returning 404 | UNMEASURED and unmeasurable from here | not read

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 06:47
