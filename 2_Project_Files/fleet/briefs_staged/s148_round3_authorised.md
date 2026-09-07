## BLUF — KAM AUTHORISED BOTH. Round 3 on #892 is ON (F1 + F2 only). The KS-968 population count is ON.
**`round3-narrow` (19:56:41)** and **`count-populated` (19:56:45)**, both verbatim from his panel.
**Start with the count** — it is one statement and it may be an incident. Then round 3.
**Nothing else widens. Do not fold KS-973's other items in.**

## 1. THE KS-968 COUNT — one statement, and it may not be about KS-968 at all
**Authorised: `SELECT count(*) FROM users WHERE email_lookup_hash IS NOT NULL`.** One integer.
**No row data, no address, no write, nothing else on that box.**
**Pre-register the outcome space and SHA-256 it BEFORE running**, as both previous runs did, and put
it beside the other two in `5_Project_History/`.
**Carry your own rule forward: EMPTY OUTPUT IS NOT ZERO, EVER.** Three attempts on the last run
returned empty stdout, empty stderr and exit 0 because `docker compose exec -T` attached stdin and
drank the script; `< /dev/null` is the fix and the run-proofs (`hash_len`, `is_superuser`) are what
made the eventual zero trustworthy. **Same guards or the number does not count.**
**What the answer means:**
- **ZERO** → the column is simply unpopulated. Benign. **KS-968 is moot on that box** and its status
  moves from UNMEASURED to *not applicable, measured*.
- **NON-ZERO** → rows carry hashes the running key cannot match. **That is a key rotation without a
  re-hash, and it is an INCIDENT, not a KS-968 finding — login resolves users by that hash, so those
  users cannot be found by email.** **Stop there and mail me. Do not investigate further on your own
  word: the authorisation is for one count.**

## 2. ROUND 3 ON #892 — F1 and F2 ONLY, and F1 is NOT a one-liner
**The card's option label says "both one-liners". That was the gate's assessment and Wednesday's when
the card was written — and YOUR OWN measurement corrected it before Kam ruled.** He had the
correction on the panel at 19:4x and ruled at 19:56.
**So round 3 closes F1 in the shape your KS-973 spec describes: QUARANTINE the stale manifest on
rejection, not merely skip the write.** *A non-write is not a removal.* **Fixing F1 as a skip leaves
the pairing you found live** — a `presuite-test-…` manifest from the test script, left standing by a
refused run, with all consumers pointed at accounts a test suite created for itself.
**This is not scope creep: it is what closing F1 actually requires**, and Wednesday is stating it as
its reading so Kam can correct it in seconds if he meant the narrower thing.
**F2:** `run.py quality` is exempt and runs 389 live-API cells. **Enumerate the command set rather
than adding one exemption's inverse** — you already moved that gate from a position to a command set
once; this is the same shape one level out.
**NOT in round 3:** F3 (the pin that cannot fail), F4 (the DEGRADED banner), and everything in KS-973
beyond F1/F2. **Ticket them; do not carry them silently.**

## 3. SEQUENCE
1. **The count**, pre-registered, then mail the integer and what it means.
2. **Round 3** — F1 (quarantine shape) + F2 (command set). **Then it goes back to the SAME gate**;
   this is the round after a spent cap, so **there is no round 4 without Kam.**
3. **#893 → develop still HOLDS** for #889's tier-1 verdict. **#894 is already merged into #893's
   branch** (`0281b0faa`, tree matched, parents re-derived — good receipt).
4. **The F-1 ticket** from the #894 gate (F-1 MAJOR leading, F-2…F-5 as items) when the above clears.
**#891 remains Kam's click.**
