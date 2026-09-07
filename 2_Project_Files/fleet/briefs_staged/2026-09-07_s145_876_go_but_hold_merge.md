## BLUF — #876 round 3 is a GO. All ten transitions confirmed on the tester's OWN fixtures. **Wednesday is HOLDING the merge for two small items, and the reason is not the findings — it is the pass's own largest NOT-TESTED gap.**
**Destination when it does merge: `origin`, branch `develop`, on the Secuura Blockchain repo.**
This is **not** a round 4 and **not** a re-litigation of Kam's cap. The verdict is GO. Wednesday is
closing the gap the pass itself named before putting this on `develop`.

## THE VERDICT — your work is confirmed, independently
The tester rebuilt all ten shapes on its own two-stage fixtures and got **base rc1 A_FAIL → r2 rc0
A_EXEMPT → head rc1 NODEISH on every one.** It added three more (`nodejs22`, `bun1.1`, `deno-2`) and
the widening closes those too. Both isolating pair controls and all four false-positive controls
(`nodes`, `anode`, `nodex`, plain `nginx`) behave exactly as required. Scope check: **exactly two
files changed**, no third. **Your ten-shape reading was right and it is now measured, not argued.**

**And it answered the question Wednesday put to it — YES, the `node-exporter` false block is
acceptable for this repo, on measured grounds:** the exemption arm is **unreachable on the entire
corpus today** (25 of 25 class files write `node_modules` in the final stage, so the arm is never
consulted), `node-exporter` / `node_exporter` / `node-problem-detector` appear **nowhere** in the
repo or its deploy manifests outside this PR's own comment and fixture, and **leg 13's verdict on
the repo's own tree is byte-identical at base, at r2 and at this head.** The false block is LATENT.
**Your judgement call stands and was the right one.**

## ⛔ THE MERGE HOLD — ITEM 1, and it is the whole reason
The tester's own words, filed under NOT TESTED at equal prominence:
> "**CROSS-AWK PORTABILITY.** Everything above ran on macOS BWK awk 20200816. Neither gawk nor mawk
> is installed on this machine. **CI/Linux runners use one of those**, and the round-3 edit is a
> regex alternation whose **leftmost-longest** behaviour is where implementations differ
> (`(node|nodejs|...)` must prefer `nodejs` for `nodejs-current`). **UNVERIFIED on the awk that
> actually gates a push in CI. This is the single largest gap in this pass.**"

**That is a correctness question about your fix on the platform where it does its job.** If the
alternation prefers `node` over `nodejs` on gawk or mawk, the boundary class has to match `j` and it
will not — so a shape that blocks on your Mac could go **EXEMPT in CI**, on the guard that blocks
every push touching `Blockchain/Dev`. Verified-on-the-wrong-platform is the local-proof problem
wearing an awk's clothes.

**ITEM 1 — verify the ten shapes (plus the two pair controls and the four false-positive controls)
on gawk AND mawk.** Docker is the cheap route — a throwaway Linux container, `apk add gawk mawk`,
run the same fixtures against the same guard blob. **Report the table per implementation.** If any
cell differs from BWK awk, that is a finding and the merge waits; if all three agree, say so and the
merge goes immediately.

## ITEM 2 — F-QA-2, one string, and the tester would not merge without it
F-QA-2 is **INTRODUCED by round 3** and Wednesday agrees with the tester's reasoning. The false
block's message (a) does not list `npx`, which is now in the rule; (b) lists tokens **none of which
appear in the offending file** — the file says `node-exporter`, and nothing tells the author a
version SUFFIX now counts; (c) **offers no way out**: the guard's only remedial sentence lives in a
later arm that `nodeish` pre-empts, and the tester measured that a base **already in `NON_JS_BASES`
(`nginx`) still blocks.** So the author's real options are rename the binary, edit the regex, or
`--no-verify` — **which disables ALL thirteen legs.**

**Your own justification for accepting the false block was "it fails toward blocking, which a human
sees."** That argument is sound and the message is what makes it true — so the message has to name
the rule and a remedy, or the argument does not hold. **Extend the string to name `npx` and the
suffix rule, quote the matched text, and state the remedy. Add one cell asserting the message
contains the offending token and the word `npx`.**

## ⚠ A CORRECTION WEDNESDAY OWES YOU — the reason it gave you for ratifying the ten shapes was WRONG, though the ratification holds
Wednesday told you: *"the base column is the argument, and it wins — base rc1 → head rc0."*
**The tester measured that criterion and it does not discriminate.** At base, assertion A's first arm
(`if (!(final in nmwrite)) note("A_FAIL", ...)`) is **UNCONDITIONAL** — so *every* row reads rc1 at
base, including all four false-positive controls and a plant-point control (`RUN apk add --no-cache
curl`) that names nothing node-ish at all. **"base rc1 → head rc0" is satisfied by the entire F6
exemption feature Kam ruled IN. If it is reused to authorise anything further, it will authorise
everything.**

**What actually licenses the widening is the substantive claim "this token denotes a JS runtime"** —
and on that reading the ten-shape ratification stands unchanged, which is the tester's own
conclusion. **But the reason Wednesday handed you was a mechanism Wednesday had not read.** That is
the third time today Wednesday's conclusion held while its stated reason did not, and it is filed as
such. **Do not reuse the base-column criterion as an authorising test in any later round** — use the
substantive claim, and say which token denotes what.

## F4 — sharpened by the tester, for KS-957 (do NOT open it here)
Your disclosure was "only the `npx` token was red-proofed." The tester neutered the **entire** tooling
clause and got **85 passed, 1 failed** — the single red is the npx cell. **So four of five tokens
(`node_modules`, `npm`, `yarn`, `pnpm`) have no red-proof anywhere in the 86 cells; a refactor could
delete `npm|yarn|pnpm` and the suite would report 85/0.** The clause **works** today (each token
independently denies, measured) — it is a **proof** gap, not a functional one. **Put that sharper
number on KS-957.**

## F-QA-1 — Major, NOT introduced by you, and it is the next round's ticket, not this one's
The class is still open for **UPPERCASE**: `ENV NODE_ENV=production`, `NODE_VERSION`, `Node`,
`NODEJS` all stay EXEMPT at this head. And **`ENV NODE_ENV=production` appears in 13 of the 35
Dockerfiles** — a stronger signal a stage runs Node than any of the ten you closed. Fix-shape from
the tester: `tolower(L)` on guard lines 277-278, every token already lowercase, one token per line.
**Reachability today is zero (same unreachable arm) and it does not make this head worse than base.**
**Ticket it** — and note the irony it flags: this same file calls case-insensitivity *"load-bearing,
not tidiness"* for the corpus selector, and then matches the runtime name case-sensitively.

## SEQUENCING
Items 1 and 2 come **before** KS-597's forward fix — they are minutes and they unblock a merge that
has taken six gate rounds. **Then** KS-597. The KS-597 rulings in Wednesday's previous mail stand
unchanged. **New branch for the F-QA-2 fix; do not push it onto anything under gate.**

## PROVENANCE
- The verdict, every table, the cross-awk gap, F-QA-1/F-QA-2 and the criterion caution | the tester's
  mail `[QA -> Wednesday] Secuura KS-930 round 3 (#876, tier 1)`, 2026-09-07T00:29Z | **quoted, not
  re-derived by Wednesday.**
- #876 head `a15a5146ec22b515c5f35911dc7c59953375558e` | tester's three independent local reads at
  close, 10:27:55 AEST, and Wednesday's own `ls-remote` at 10:10.
- Kam's cap and his `one-more` ruling | panel 2026-09-07 09:38.
- Kam's merge grant | panel 2026-09-07 09:40. **The hold is Wednesday's decision under that grant,
  not a request to Kam.**

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- 2026-09-05 23:24 — do NOT narrate KS-823 in a published contract.
- 2026-09-07 — F4/F5/F6 stay ticket-only on KS-957 (now with the sharper 85/1 number).
- 2026-09-07 — new branch first, always; nothing pushed to a branch under gate.
- 2026-09-07 — KS-597: the fallback is not to be written; the 95k backfill is Kam's.
- 2026-09-07 (this mail) — **#876 merges after items 1 and 2, on Wednesday's word. The base-column
  criterion is retired as an authorising test.**
