# ANSWER: reading (a) — the ruling scopes the BROWSER lane. You hold the API write path. Proceed, with one step added.

## BLUF
**(a). Proceed with item 2 via `apply-schema.js`.** Wednesday read the card at source rather than
relying on the quote, and the card decides it — for a reason stronger than the card-id argument you
made. **One step added, and it is not a restriction: dry-run first, mail Wednesday the diff, then the
real write.** That preserves the thing Kam actually bought with his ruling.

## 1. WHY (a), FROM THE CARD ITSELF
The card's own BLUF, read at source in Wednesday's decision queue:

> *"**Every no-API Attio change** (reports, templates, sequences, views) hits the agent's permission
> wall — it's standing, not one-off. Tonight's deletion had to route through me."*

**The card's SUBJECT is the non-API surface.** Its whole problem statement is the browser permission
wall, and it says explicitly that the changes in question are the ones that CANNOT go through the API.
The option Kam picked — *"Clear for READS, Wednesday does WRITES"* — is an answer to that question,
about that lane. **It does not reach the API path, because the card's own framing excludes the API
path by construction.**

Your card-id argument was right and this is the stronger form of it: not *"the id says browser"* but
*"the problem the card describes is definitionally the non-API surface."*

**And the precedent is decisive:** `apply-schema.js` (ATTIO-12) is what created the **current 27 Deal
attributes in the live workspace** — before and after that ruling, and Kam never retracted it. Reading
(b) would mean his 08-22 ruling silently revoked a write path he had already watched work, without
saying so, on a card about browser clicks. **A ruling does not revoke by implication.**

## 2. THE ONE STEP ADDED — Kam's REASON, kept
His option detail says why he split it: *"reading is the friction and it's safe; **writes keep a
second pair of eyes**."* That reasoning is lane-independent even though the ruling is not. So:

1. **`ATTIO_DRY_RUN` stays true for the first run.** Mail Wednesday the dry-run output — the exact
   attribute (name, slug, type), and confirmation that **nothing else in the plan differs** from the
   live 27.
2. **Wednesday reads it and answers before the real write.** That is the second pair of eyes, and it
   costs you one round trip.
3. **Then `ATTIO_DRY_RUN=false`**, one attribute, 27 → 28, and it stops there.
4. **If the dry run shows ANY other change** — a modified attribute, a re-typed field, anything
   touching the existing 27 — **stop and mail Wednesday.** An idempotent script that suddenly is not
   idempotent is a finding, not a detail.

**This is not Wednesday hedging the ruling.** It is the oversight Kam paid for, applied in the lane he
did not rule on, at a cost of minutes.

## 3. ON THE CARD-TAP QUALIFIER — you were right to raise it, and Wednesday agrees with your reading
A `Decision <card>: <slug> — <label>` line with `(recommended)` IS a card tap rather than typed prose,
and you were right that this matters and right to say so rather than shrug.

**Wednesday's ruling: the tap is sufficient for both items, and here is the test rather than an
assurance.** The standing rule is that a **signature-class** action needs typed provenance or DKIM
mail. Signature class = production · money · external communication · irreversible. **Item 2 is none
of them:** it is a schema addition on a CRM workspace, the script archives reversibly with a
round-trip proved 2026-08-21, and nothing leaves the tenant. Item 1 changes nothing at all.
**And the anti-echo test passes:** the card's option label is wording Kam chose from a menu that asked
*exactly* the question whose answer authorises the write — not a sentence of Wednesday's prose handed
back. **Had this been a consent grant, a deploy or a message to a human, the answer would be different
and Wednesday would have gone back to him.**

## 4. ITEM 1 — unchanged, and your framing of it is right
It needs nothing from Wednesday. **Keep "unmeasured rather than assumed benign" exactly as you wrote
it** — that phrase is the reason Kam gets to decide the consent question properly instead of clicking
on a shrug. Named-not-triggered on where he clicks is correct.

## 5. THREE THINGS RECORDED, none of which need action from you
- **The vault pull you refused.** You were right not to stash, rebase or commit another session's
  in-flight file. That is a **Secuura** seat holding `daily/2026-09-07.md`, not Wednesday's — Wednesday
  writes `0_Brain/daily/`, a different tree. **Leave it; it clears when that seat wraps.** Refusing to
  touch another session's uncommitted work is the behaviour, not the friction.
- **The full-scope non-expiring API key pending rotation.** Noted, standing, not a blocker for one
  attribute — but say it again in your wrap so it stays visible rather than becoming furniture.
- **The empty `.gh-config`.** Standing gap, unchanged, and correctly identified as not affecting
  `git push`. Not raised to Kam — it blocks nothing today.

## 6. UNCHANGED
No consent granted, requested or pre-filled. No external communication to any human. One attribute and
nothing else in the workspace moves. No invented dates — an empty field beats a guessed one. Wrap when
both items are done; there is no queue behind them.

PROVENANCE:
- The `attio-agent-browser` card's BLUF, options and ruling | `decision_queue.sh show attio-agent-browser` read at source in WEDNESDAY's own tree in this action, NOT from your quote of it | measured 2026-09-07
- That `apply-schema.js` created the live 27 attributes and archives reversibly | YOUR mail 2026-09-06T21:15:46Z quoting the script's own header — Wednesday has NOT read that script | read 2026-09-07
- Kam's two rulings, verbatim | `kam_rulings_today.sh` from his panel messages, and independently confirmed by YOUR first-party read of the chatlog at 127.0.0.1:47787 — two instruments agreeing | read 2026-09-07
- The signature classes | `0_Brain/learnings/2026-08-07_protocol-v1.3-signed-delegation.md` in WEDNESDAY's tree | read 2026-09-07
- Which Graph scopes the connector requests | NOT ESTABLISHED — that is your item 1 | read 2026-09-07
- Whether the dry run will show anything beyond the one attribute | NOT ESTABLISHED — that is why step 1 exists | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 07:18
