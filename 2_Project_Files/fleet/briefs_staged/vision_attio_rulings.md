# Datasec/ATTIO — TWO KAM RULINGS, both from this morning's follow-up digest. Bounded work, then wrap.

## BLUF
Your scheduled digest (21:00Z) reported two blockers honestly instead of returning zeros, Wednesday put
both to Kam, and **he ruled both within the hour.** Two bounded items below. **Item 1 is a read-only
REPORT and produces no change. Item 2 is one attribute.** Nothing else in the workspace moves, and
when these two are done, **wrap** — there is no standing queue behind them.

**Your digest's discipline is why this happened.** Putting *"their zero means nothing"* and *"this is
not the question Kam asked"* ABOVE the numbers is what made both blockers visible and rulable. Keep it.

## KAM RULING 1 — `attio-entra-consent-m365` => **scopes-first**
> *"Have the agent report the exact scopes first, then decide"*

**This is a REPORT. Grant nothing, request nothing, change nothing in the tenant.**
Kam will not click a consent screen without knowing what it covers, and Wednesday explicitly refused
to recommend that he just grant it — because Wednesday has not read the connector and will not hand
him a permission prompt with a shrug attached.

**Produce, from the connector's own configuration read at source:**
1. **Every Graph permission the M365 email/calendar sync requests**, by its exact scope name.
2. **For each: what it actually reads.** In particular and stated plainly — **does anything read
   message BODIES, or only metadata, headers and calendar events?** That is the question Kam will
   decide on.
3. **Whether each scope is delegated or application-level**, and whose mailboxes it reaches — his
   alone, or every mailbox in the tenant.
4. **Anything you could NOT establish**, named as unmeasured rather than assumed benign.
5. Where the consent is granted (the exact place Kam clicks) — **but do not pre-fill or trigger it.**

Report by mail. Wednesday cards it to Kam with your findings as the body. **He decides; nobody else.**

## KAM RULING 2 — `attio-renewal-date-vs-attr-cap` => **one-field**
> *"Lift the cap by exactly one, for a renewal date"*

Your renewals leg reported it **cannot run**: no renewal-date attribute exists on Deal, and adding one
would be the 28th attribute, outside the cap Kam ruled HOLD on 2026-08-22. **You were right to refuse
to work around his ruling and to say the signal could not run rather than return a zero.** He has now
lifted it — **by exactly one, for exactly this.**

1. **ONE attribute: a renewal DATE on Deal. Nothing else.** 27 becomes 28 and stops there. If the work
   appears to need a second attribute, **stop and mail Wednesday** — that is a new decision, not a
   detail.
2. **CHECK YOUR OWN WRITE PATH FIRST.** Kam ruled `attio-agent-browser` => **reads** on 2026-08-22 —
   your browser access is READ-ONLY. **Before creating anything, establish how you are entitled to
   create it** (an API token with write scope is a different grant from browser reads). **If you do
   not hold a write path Kam has granted, STOP and mail Wednesday — do not use the browser to write.**
   That boundary is his and Wednesday will not widen it for you.
3. **Populating it is a separate question, not assumed.** 6 of 18 deals are marked under an MPS
   contract, so the population is real and undated. **Do not invent dates.** If the dates are not
   derivable from data you already hold, say so — a populated-with-guesses field is worse than an
   empty one.
4. **Then prove the leg RUNS.** The point of the attribute is that
   `FOLLOWUP_RENEWAL_HORIZON_DAYS` has something to compute against. A next digest that still says
   "cannot run" means this is not finished. **Say which of the three signals now runs and which
   still cannot.**

RULED BY KAM, NOT YET IN AN ARTEFACT
The two rulings this brief carries are themselves the undelivered ones — **your work IS their
delivery**, and each names the artefact it must land in:
- attio-entra-consent-m365: "Have the agent report the exact scopes first, then decide" -> must land in your scopes REPORT mail, which Wednesday puts in front of Kam as the card body. No tenant change is part of this delivery.
- attio-renewal-date-vs-attr-cap: "Lift the cap by exactly one, for a renewal date" -> must land in the Deal object as ONE new renewal-date attribute, and be evidenced by the next digest's renewals leg RUNNING instead of reporting it cannot.
Older ATTIO rulings still standing and NOT actions for you (listed so you do not re-raise them):
attio-attr-cap => hold (now lifted by exactly one, above) · attio-agent-browser => reads (your write
path is NOT granted by it — see item 2) · attio-security-pack => send · attio-prod-db => bridge ·
attio-rate-card => quickquote · attio-nfr-onhold => newstage · attio-contact-data => accept ·
attio-pro-vs-free => free · attio-companies-report => delete.

## HOLDS
- **No external communication to any human.** Nothing to a client, nothing sent from the workspace.
- **No consent granted, no permission requested, no tenant change** — ruling 1 is a report.
- **Never delete** — quarantine by rename. **No secret in any ticket, PR, mail or commit message.**
- **Attio is a live workspace Kam uses.** One attribute is the whole authorisation; anything that
  changes existing records, views, reports or other attributes is outside it.
- Wednesday is running a busy Secuura queue in parallel. **Mid-round questions come to Wednesday, not
  to Kam.**

## WRAP WHEN DONE
There is no queue behind these two. Wrap at your normal ritual with a resumable handover and a wrap
mail. **Say in it which signals now run and which are still blocked, and by what.**

PROVENANCE:
- Both rulings, verbatim | `kam_rulings_today.sh` at 07:07 AEST, from Kam's own panel messages, recorded on their cards with `decision_queue.sh rule` in the same action | read 2026-09-07
- The two blockers and their wording | YOUR digest mail `[Datasec/ATTIO -> Wednesday] DAILY FOLLOW-UP DIGEST 2026-09-07`, 2026-09-06T21:00:08Z, quoted not paraphrased | read 2026-09-07
- That browser access is ruled READS ONLY | card `attio-agent-browser` => reads, 2026-08-22, in Wednesday's decision queue | read 2026-09-07
- That the cap was 27 and a renewal date would be the 28th | YOUR digest's own renewals section | read 2026-09-07
- Which Graph scopes the connector requests, and whether it reads message bodies | NOT ESTABLISHED — Wednesday never opened the connector; that is your item 1 | read 2026-09-07
- Whether you hold an Attio WRITE path | NOT ESTABLISHED — Wednesday checked only the browser-reads ruling, not your credentials; establish it before creating anything | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 07:10
