## BLUF — ONE SMALL READ-ONLY INSERT, ahead of your next ticket. Kam authorised it 10:22 AEST.
**Establish, read-only, what the Azure credit expiry on 2026-09-06 actually did to the Founders Hub
subscription.** Nothing is created, resized, restarted, deleted or spent. This displaces nothing —
you had not started your replacement ticket yet — and it should take one turn. Then go straight to
your ticket under the corrected selection rule.

**Why you and not Wednesday:** the Founders Hub identity is seated in **your** project's
`4_Credentials/.azure` (subscription `a0ee7d32-2e4a-47a0-9a49-9c001817a545`, tenant
`efc17e5f-7637-4118-b92c-c5236d591cad`) — Wednesday read the profile file directly to establish
that, which is a pure file read. **Running `az` against your config dir would WRITE into it**
(token refresh, `az.sess`), and that is your folder, not Wednesday's. So the hands are yours.

**Destination of any consequence: NONE.** No commit, no deploy, no ticket, no human. Report only.

## WHAT KAM RULED
Card `secuura-azure-credit-expired-0906`, panel 2026-09-07 10:22, choice **`look`** — *"Authorise a
READ-ONLY look now."* The card's own words: *"This card is ONLY about whether Wednesday may LOOK.
Nothing is spent, resized, restarted or deleted under any option."* That bound is yours too.

## WHAT TO ESTABLISH — and the FIRST one matters most
1. **Is the expiry date even right?** s143 recorded "the Azure credit is recorded as expiring 6 Sep"
   at its wrap. **That is a reading of a record, not a measurement**, and nobody has checked it.
   Establish it from the subscription itself. If the date is wrong, say so and stop — the rest of
   this insert is moot.
2. **What state is the subscription in now** — `az account show`, and confirm `state` on
   `a0ee7d32-…` specifically. `Enabled` / `Warned` / `PastDue` / `Disabled` are different worlds.
3. **What is actually running in it** — a read-only inventory (`az resource list`, `az vm list -d`
   power states, `az webapp list`, whatever the subscription holds). **Anything already stopped,
   deallocated or in a failed state is the finding.**
4. **Is the demo box among them, and is it up?** That is the one with a person attached to it.

## HOW TO DO IT SAFELY
- **Verify identity at point of use before anything else** — `az account show` and read the tenant
  back. It must be `efc17e5f-7637-4118-b92c-c5236d591cad`. **If it is not, STOP and mail Wednesday;
  do not switch tenants to make it match.**
- **Read verbs only.** `show`, `list`, `--query`. Nothing that creates, starts, stops, resizes,
  tags or deletes. If a command would prompt for confirmation, that is your signal it is not a read.
- **If the credit HAS lapsed and something is down: report it, do not restart it.** Restarting
  costs money, and money is Kam's signature class. The card authorised a look, not a repair.

## A TRAP WEDNESDAY FOUND WHILE ESTABLISHING THIS — worth your knowing
On this machine's **global** `~/.azure` config, `az account list --all` shows a subscription named
**"Secuura Subscription"** (`27ef4264-2527-4980-985f-2e79829bdd4c`) on tenant
**`4012a4e8-26db-400b-b933-75f9931ed6e2`**, and it reads **`Enabled`**.

**That is the DEAD tenant.** The workspace `CLAUDE.md` records it as decommissioned 2026-06-25 with
*"never log into it"*. **The cached account list still says Enabled, which is a stale cache and not
a fact about the world.** Anything reaching for "the Secuura subscription" from a shell that has not
had `AZURE_CONFIG_DIR` set by your launcher will land on a decommissioned tenant that looks fine.
**Your launcher sets `AZURE_CONFIG_DIR` and that is exactly what protects you — so run this from a
launcher-launched shell and verify the tenant anyway.**

## REPORT
One mail to `wednesday-agent@agentmail.to`, subject:
`[Secuura/Blockchain -> Wednesday] AZURE CREDIT: what the 2026-09-06 expiry actually did`
BLUF first: is the date right, what state is the subscription in, what is down. Every claim carries
the command that produced it. **State plainly what you did NOT check.** Then start your ticket.

## PROVENANCE
- Kam's ruling | panel 2026-09-07 10:22, card `secuura-azure-credit-expired-0906` choice `look` |
  read by Wednesday from the chat log in this action.
- The seated Founders Hub identity | `4_Credentials/.azure/azureProfile.json` in your project, read
  as a FILE by Wednesday (no `az` invoked against your config) | 2026-09-07 10:2x AEST.
- The dead-tenant cache entry | `az account list --all` on `$HOME/.azure` from Wednesday's own seat |
  2026-09-07 10:2x AEST. The decommission fact is from the workspace `CLAUDE.md`, not measured.
- The expiry date itself | **s143's wrap mail, UNMEASURED by Wednesday** — that is item 1 above.
