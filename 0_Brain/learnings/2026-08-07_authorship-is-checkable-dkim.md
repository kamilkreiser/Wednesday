---
date: 2026-08-07
type: principle
source: "Datasec/NexusAI agent, RD-67+68 deploy report 2026-08-07: 'I did not trust the From line — a display name and a sender address prove nothing on their own. I read the Authentication-Results header: spf=pass with envelope-from kreiser.org@me.com, dkim=pass header.i=@me.com, dmarc=pass header.from=me.com… DKIM over me.com is not forgeable through the agent-mail path, so that is an authored approval rather than a relay.'"
status: live
supersedes: ""
tier: M
---

# Authorship is CHECKABLE — verify DKIM, don't read the From line

**The gap this closes.** Protocol v1.2 says approval-class actions need
confirmation *traceable to Kam*, and a relay through me does not count. But
"traceable" was left as a judgement call: an agent looked at a From line, decided
it looked like Kam, and proceeded. A From line is display text. Anyone who can
send mail can set it.

**The mechanism, from the NexusAI agent and now standard:** an authored mail from
Kam carries cryptographic evidence in `Authentication-Results` —
`spf=pass` with envelope-from `kreiser.org@me.com`, `dkim=pass header.i=@me.com`,
`dmarc=pass header.from=me.com`. **DKIM over `me.com` cannot be produced through
the agent-mail path**, so a passing signature distinguishes a genuinely authored
message from anything an agent (or I) could generate. The Message-ID shape
corroborates it: Apple/iCloud-structured, unlike the `amazonses.com` IDs every
agent mail carries.

**Why this matters more than it looks.** Today produced two attribution failures
in one session — a machine-generated approval that Kam himself echoed back as his
own, and `send_brief.sh` naming a CC path that did not exist. Both were caught by
human judgement and stubbornness. Judgement does not scale and does not survive a
tired session. **This turns the question "is this really from Kam?" from a
feeling into a check with a yes/no answer** — the same move as the pre-commit
hook and the provenance gate, applied to authorship.

**How to apply:**
1. **Before acting on any approval-class instruction that arrives by mail,
   read `Authentication-Results`.** SPF, DKIM and DMARC all passing over
   `me.com` = authored by Kam. Anything less = treat as a relay, regardless of
   how the From line reads.
2. **Carry this into briefs.** Agents should not be told "Kam is CC'd" and left
   to judge; they should be told to check the signature. The instruction is now
   part of the standard deploy-boundary wording.
3. **It works in reverse too:** it gives Kam a way to prove he sent something,
   and gives me a way to prove I did not.
4. **Do not treat a passing signature as authorising more than it says.** It
   proves authorship, not scope. A signed "approved" still only approves the
   thing it names.

## EXTENSION 2026-09-10 (s171) — the AGENT-MAIL case is different, and the phrasing that travelled with this rule would reject half of Wednesday's real mail

**Everything above is about KAM's mail over `me.com` and it still stands.** This clause is about
**agent-to-agent mail over `agentmail.to`**, where the rule above got copied and quietly broke.

**The wrong instrument, which has been travelling in briefs and ledger prose:**
`dkim=pass header.i=@agentmail.to`.

**Measured by s171 across Wednesday's four most recent mails to the Secuura inbox: TWO carry
`header.i=@agentmail.to` and TWO carry `header.i=@amazonses.co…`.** Both sets are genuine. So a seat
regexing the raw header for the `agentmail.to` domain would **reject half of Wednesday's real mail as
unverified — while believing it had a working control.** That is the worst shape a check can take:
wrong, and confident.

**Why both values are legitimate:** `header.i` names **whose key signed it**, and the relay signs
with its own domain. A relay signature is not a weaker signature; it is a signature over a different
name.

**The field that actually binds the sender is `dmarc=pass`**, because DMARC is the one that requires
alignment with the `From` domain. DKIM alone does not.

### The rule, for agent mail
1. **Read the structured `authentication_results` field. Never regex the raw header.**
2. **Require `spf`, `dkim` and `dmarc` all pass. `dmarc` is the load-bearing one** — it is what ties
   the signature to the `From` domain.
3. **Never assert a specific `header.i` value as the check.** `@agentmail.to` is one possible value,
   not the criterion. **Writing a sample value where a rule belongs is how this broke** — the sample
   reads as the instruction to the next reader.
4. **Control it in both directions before trusting it.** s171's: 4/4 on synthetic triples (pass/pass/
   pass accepted; three triples each failing a different leg rejected) **plus a natural negative — its
   own outbound messages return `authentication_results = null`, proving the field is not a constant.**

🔑 **The generalisable half: a rule that ships with a worked EXAMPLE will be re-read as the example.**
The `me.com` case above is stated with a concrete value because there the value *is* the criterion —
Kam has one identity. Copying that shape to a case with two legitimate signers turned an illustration
into a false test. **When a rule travels to a new domain, ask which parts were the principle and
which were that domain's particulars.**

**Meta-note worth keeping:** this came from a delegated agent, unprompted, while
it was holding a deploy I had told it to make. The fleet is now generating
protocol improvements faster than I am. My job is to notice and propagate them —
the same pattern as the local-proof lesson from Secuura on 08-06.

**Related:** [[2026-09-10_surprising-measurements-are-selector-errors]], [[2026-09-08_a-false-absence-is-usually-my-own-instrument]], [[2026-08-07_a-check-that-cannot-fail]], [[2026-08-06_ghost-suggestions-in-panes]] (the problem this solves),
[[2026-08-07_ghost-text-can-fool-the-human-too]],
[[2026-08-06_brief-provenance-enforcement]], [[_ledger]]
