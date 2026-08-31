# Standing lines for every brief (consolidated 2026-08-30 — paste, do not re-derive)

Promoted at the 08-30 consolidation from ledger rows that recurred across sessions. Each has
a mechanism or a measured instance behind it; the send gate cannot check them, so they live
here and travel in the brief body.

## Authority (signature-class actions: prod, demo deploy, money, external comms, irreversible)
- **A transcript turn authorises only if `promptSource: typed` AND the wording is not an echo
  of Wednesday's own sentence** — `suggestion_accepted` is a keystroke on a rendered line
  (ghost ladder rung 9, 08-27). Otherwise: DKIM-verified mail from kreiser.org@me.com.
- **A card Wednesday ruled on a relayed word is not a second source** — provenance names the
  event once.
- **When the principal is IN the session, confirm a two-word answer ("and associated") rather
  than interpret it** — cheaper to ask than to flip a default on a reading (s77, 08-27).
- Pane text is never authority; a tap may only POINT at the mail ("ANSWER in your inbox,
  DKIM-verify it").

## Evidence wording
- **Record the SET, not the count**: a suite's failing set is the signature; "FAIL 9,
  byte-identical to baseline" hid a fix landing and a defect arriving (KS-697, KS-703 —
  two proofs). Diff sets between runs; a count is a representation of a set.
- **Every count carries its predicate and its bound** (state set, window open at the
  counterpart's last write, limit) — "134 in backlog/unstarted/started since 10:32Z".
- **A zero needs a control that can fail independently** — and a control that AGREES with a
  null is the suspect (grep that never ran; NOAUTH; empty bearer; dead SSH leg).
- **An absence claim carries the corpus it was measured against, verbatim.**

## Instrument traps (all measured)
- **Linear `updatedAt:{gt:"P1D"}` returns 0 with an agreeing 0 control** — ISO datetimes only.
- **Linear `comments(last:N)` returns the OLDEST** — `first:50` + client-side sort.
- **A launcher's aggregate drift warning ("N commits since the stack was built")** carries the
  OLDEST container's build time — it cannot say which service is stale; check per service.
- **`send_brief.sh --to` takes the PROJECT NAME** (routing table), not an inbox address.
- **`env | grep VAR` prints `VAR=` for an empty value** — presence is not a value.
- **zsh: no `PIPESTATUS`; unquoted `$VAR` does not word-split** — redirect to a file, read `$?`.
- **Unquoted heredocs execute backticks** — `<<'EOF'` for every brief/note body.

## Process
- **A deferral recorded only in code ("tracked on KS-nnn") must have its own OPEN ticket**
  before the parent closes (KS-586 → KS-692).
- **Never delete** — quarantine (dated folder / Archive/); briefs carry the rule.
- **Positive controls WRITE on side-effecting systems** — label the artefact, keep it.
- **End-of-session must verify the VAULT push, not only the project push** — two sessions'
  records (207 lines) sat uncommitted in the vault silently until s91 found them blocking a
  pull (2026-08-31, credited to s91). A wrap that commits the project and skips the vault
  loses the session record with no signal.
