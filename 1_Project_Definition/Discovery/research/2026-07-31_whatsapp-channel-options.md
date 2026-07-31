# Research: WhatsApp identity for Wednesday (Australia, July 2026)

Date: 2026-07-31. Question from Kam: is the dedicated old-phone + new-SIM plan
necessary, or is there a no-phone-number approach? Preference: own number, added
to selected groups; Wednesday never sees Kam's personal WhatsApp.

## Findings

1. **No phone-number-free path exists.** Every WhatsApp account requires a real,
   SMS/voice-verifiable number at registration. The 2026 "usernames" feature only
   hides the number from contacts — registration still needs one. The number is
   needed only at (re)registration; after that WhatsApp runs on Wi-Fi, no SIM
   inserted.

2. **Official Business/Cloud API is eliminated for this use case.** The Groups
   API (launched Oct 2025) only supports *business-created* groups: max 8
   members, invite-link joins only, and it requires an Official Business Account
   (verified-business tier a personal assistant won't get). **A Cloud API number
   cannot be added to existing consumer-created group chats at all.** The
   24h-window/template rules would also hobble proactive pings. So the official
   route fails the core requirement regardless of cost.

3. **Unofficial bridges are the only way the Mac can drive a real account.**
   mautrix-whatsapp (most production-hardened, Docker/Matrix) or Baileys
   (lightest, Node). Full capability: joins any group it's added to, 1:1, media,
   no windows, no fees. **Ban risk is real** (May 2025 enforcement wave hit even
   low-volume personal users) but mitigated by: real AU carrier SIM (not VoIP —
   WhatsApp rejects VoIP numbers at registration now), registering on a physical
   phone, letting the account age before bridging, messaging only Kam + groups
   it's added to, moderate volume. Blast radius if banned: Wednesday's number
   only (~$17 to rebuild) — never Kam's account.

4. **The dedicated device stays in service permanently, not just for setup:**
   WhatsApp logs out linked devices if the primary phone is offline >14 days.
   Old phone lives on home Wi-Fi, plugged in, in a drawer — it also lowers ban
   heuristics by looking like a normal device.

5. **SIM economics (AU):** ALDI Mobile PAYG — $2 starter SIM, $15 recharge with
   365-day expiry (Telstra network) ≈ **$15/year** to keep the number. Letting
   credit lapse risks the number being recycled and the WhatsApp account taken
   over by a stranger — pay the $15/year as account insurance.

## Recommendation (matrix in full report history)

**Go with Kam's original plan — it's the only viable one:**
old phone + ALDI $2 PAYG SIM ($15/365-day recharge) → register WhatsApp on the
phone → phone lives on home Wi-Fi permanently → let the account age ~1-2 weeks
with light human use → pair the Mac Studio via **mautrix-whatsapp** (or Baileys
for a lighter first version) → Wednesday participates in groups she's added to.
Accept the residual, ring-fenced ban risk knowingly. Cloud API not worth keeping
even as a fallback (can't do groups).

Sources: Meta Groups API docs, 9to5Google/Forbes/Al Jazeera (usernames), Sanuker/
imBee/iSlash (groups limits), mautrix docs (ban heuristics), SporeSec + Cloudron
forum (2025 enforcement wave), ALDI Mobile, Finder/WhistleOut (AU prepaid),
Princeton CITP (number recycling), Cape/smspinverify (VoIP rejection).
