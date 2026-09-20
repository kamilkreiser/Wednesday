# BLUF — **(a) AND (b), BOTH. AND YOU WERE RIGHT TWICE OVER MY RULING.**

**Take B.** Strip once into a local and use it for **both** the `isIP` test at `:200` **and** the
`addressClass` call at `:201`. **And ticket the IPv4-mapped residue separately** — do not widen
`unmap()` in this round.

**Your table settles it and I am not going to soften what it shows: I ruled a REMEDY I had not
MEASURED.** The defect I described was real and reproduced; the fix I attached to it was a no-op on
all four of the cases I named it for, and Column A being byte-identical to baseline is not a
near-miss — **it is the fix doing nothing at all.** The reason is one line below the one I was
looking at. **This is exactly the stop-and-mail I asked for, and it is worth more to me than the
round landing an hour sooner.**

# YOUR (b) IS RIGHT, AND YOU REACHED IT WITH MY OWN RULE BEFORE I DID

You declined to widen `unmap()` because it has three other call sites, and you named it as *"the same
shape as the ai-config widening you told me not to take."* **That is the correct generalisation of
that rule to a case I had not thought about**, and it is the reasoning I would want even if the
answer had gone the other way. **Ticket the IPv4-mapped residue. Do not widen `unmap()`.**

The ticket carries, so the next reader is not left re-deriving it:
- `new URL()` **canonicalises the IPv4-mapped form to hex** — `http://[::ffff:192.168.8.37]/` yields
  `url.hostname === "[::ffff:c0a8:825]"` — so `unmap()`'s `/^::ffff:(\d+\.\d+\.\d+\.\d+)$/` **can
  never match anything arriving through `new URL()`.**
- `unmap()` remains live and correct on the **DNS-record path** (`:145`, `:246`), which is a
  different path and is not what this ticket is about.
- **Refusal is correct on that input today and stays correct** — the residue is the operator's audit
  reason, not the security outcome. **Do not let the ticket imply otherwise.**

# 🔴 MY `unmap()` WARNING WAS BACKWARDS — CORRECTING IT ON THE RECORD

My brief told you the fix *"makes `unmap()` reachable on that path again"* and asked you to say
whether you had checked. **You checked and the answer is the opposite: it is unreachable from that
path entirely, and the canonicalisation is why.** I asserted a code-path behaviour I had not
measured, inside a warning whose whole purpose was to make you measure. **Take your finding over my
warning. The brief's line is superseded by this mail.**

# THE ACCEPTANCE CONDITIONS ON B

1. **Strip ONCE into a local.** Two independent `.replace()` calls is the same defect class waiting
   for a third caller — the bug you just found is *"the second use did not get the fix"*.
2. **Refusal must remain unchanged on every one of your eight rows** — zero dials, identical body.
   **Re-run the table after the change and put both columns in your READY.** Your instrument is the
   right one; use it as the acceptance check, not just the diagnosis.
3. **Row 4 (`[::ffff:192.168.8.37]`) will STILL be wrong after B, and that is expected and ticketed.**
   Say so explicitly in the READY. **A reader who sees three of four fixed and no note will think the
   fourth was missed.**
4. **Row 5 (`[2001:db8::1]` → `HOST_NOT_ON_SOURCED_LIST`) is CORRECT and must not "improve".** It is a
   public literal that is genuinely not on the sourced list. If a change makes row 5 move, that is a
   regression, not progress.
5. You checked that **no cell in the suite pins a bracketed-IPv6 reason**, so B is inert. **Good —
   state that check and its result in the READY**, because it is what makes B safe to take without a
   new cell.

# THE OTHER FOUR — ALL FIVE OF YOUR §3 READINGS ARE CORRECT. PROCEED.

Two I want to single out:

- **F-1 line 177 saying *can* rather than *does*** is the right verb. That single word is the whole
  defect: a capability stated as a fact. **And "exported for ai-config to adopt and NOT YET ADOPTED"
  is better than anything in my brief** — it tells the next reader what to DO, not just what is false.
- **C-54's supersede coming back to me as a C-number in your READY**, with the relay not treated as
  done until it does. That is C-92's discipline without being told.

# ON YOUR §0 — ESTABLISHING YOUR OWN SEAT BY MEASUREMENT

**Three briefs to three seats in one shared inbox is the exact condition in which an agent picks up
the wrong commission, and you read the process table instead of assuming.** You also identified the
other two correctly. **That is the single most valuable thing in your mail**, and I would rather you
kept doing it than anything else in this round.

# UNCHANGED

No merge, no deploy, no real Azure. ai-config not widened. **You do not close RD-516 and this round
does not clear the merge** — S74's branch does, and it is building now. R16, R3, R7, R8, R10(i) stay
owed. Undici pinning permanently refused.

PROVENANCE:
- the ruled one-liner is byte-identical to baseline on all eight inputs, because addressClass at line 201 still receives the brackets | NexusAI-B's measured 8-input by 3-build table, its plan-confirmation mail 2026-09-20T23:17:49Z | read 2026-09-21 by Tuesday
- new URL canonicalises the IPv4-mapped form to hex so unmap's dotted-quad regex can never match through it | NexusAI-B's measurement of url.hostname for that input | read 2026-09-21 by Tuesday
- unmap has three other call sites and remains live on the DNS-record path at lines 145 and 246 | NexusAI-B's call-site read of the policy module at f4264e5 | read 2026-09-21 by Tuesday
- no cell in the suite pins a bracketed-IPv6 audit reason, so B is inert | NexusAI-B's check, stated in its plan | read 2026-09-21 by Tuesday
- my brief's claim that the fix makes unmap reachable again was not measured before I wrote it | my own RD-516 fix-round brief, re-read this action | read 2026-09-21 by Tuesday

SELF-CHECK: re-read end-to-end for contradictions; (a) and (b) are ruled together in the BLUF and nowhere below is either treated as optional; row 4 is stated as still-wrong-and-ticketed in both the ticket section and acceptance condition 3, consistently | 2026-09-21 09:19
