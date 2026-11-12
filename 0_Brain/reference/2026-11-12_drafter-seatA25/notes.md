# Drafter notes, Seat A 25th brief (2026-11-12 ~11:4x AEDT)

Deliverable: `brief_A25.md` in this folder (copy-and-change of A 24th's stamped brief, with the A 24th model line overridden). STAMP block blank, no SELF-CHECK line, one PROVENANCE: block covering every KS key named (14 keys: 1000, 1176, 1185, 1190, 1203, 1204, 1466, 1728, 1873, 2125, 2169, 388, 907, 925).

## Model row
Opus 5.5 (`claude-opus-5-5`, models_latest.json key `opus`, checked 2026-11-12 11:08:10 +1100). Row C3 (auth/security DESIGN surface; Sonnet is "no", proposal) plus section 3's rule that an auth-surface design decision never goes local; the live-box reads reinforce it. Gate row G1 tier 1 Opus. Confirms Wednesday's expectation. Counter-argument I considered and did not take: Kam's ruling already names the design, so it is nearly a spelled-out edit (Sonnet could build it). But the measurement is the hard part (judging whether a stored entry would lock callers out, proving a box route is a pure read), and routing v1.0 says "Opus builders also take NO GO rounds; whether Opus builds better here is unmeasured": the rule rests on caution, not on data. Your call at the stamp.

## Findings from my source reads (read-only, shared checkout at `0e6479d7b6c0`, 2026-11-10, BEHIND origin develop `697f422f1a39`; I did not fetch)
1. Card says `enforcement.ts:101`; in that checkout the untyped early return is at lines 116-118 (file is 280 lines). Line numbers are UNVERIFIED against develop; the brief tells the seat to re-read. The BLUF fact (untyped body returns `{ ok: true, docType: {} }` and nothing is enforced) is confirmed in the checkout.
2. The seed `DOCUMENT` entry (`routes/admin.ts`, dt-seed-8) is friction-free: active, all levels none, no MFA, no providers, no approval, empty metadata schema. The seed's own comment says both contract-critical types are deliberately friction-free. So enforcement would refuse nothing on a box holding the SEED entry. The real risk is elsewhere.
3. NOT IN THE TICKET: if the catalogue is non-empty but has no `DOCUMENT` entry, `resolveDocumentType('DOCUMENT')` returns null and enforcement returns 400 `UNKNOWN_DOCUMENT_TYPE` (KS-388 path). Resolving untyped to `DOCUMENT` would then 400 every untyped create. Brief names this as the likeliest lockout and as measurement item 2. Empty catalogue stays pass-through.
4. TRAP for the "demo reads only" rule: `GET /api/admin/document-types` calls `seedDocumentTypesIfEmpty()` which WRITES the seed catalogue to Redis when the catalogue is empty and `enableDemoSeed` is on. It is not a pure read in general. Brief forbids it on demo unless proven safe, and leaves the choice of route to the plan and Wednesday's ANSWER. I did not call anything on any box.
5. Existing cells that run or stub `enforceDocumentTypeRules` (ks1203, ks1204, ks1176, ks1185; found by grep, not run) will likely need re-running or changing.
6. Linear (read-only): KS-1466 is Backlog with description only, ZERO comments. KS-1000 is In Progress, items 1, 2, 4 delivered for auth (PRs 1480, 1499, 1506), item 3 (sibling sweep) open: 5 baselines, 20 service tsconfigs still contain `__tests__` (a grep). I did not paste any credential value.
7. o162's report: stopped on KS-1466 as the commission said; its other item KS-2169 G312-2182-7 is held and not A 25th's.

## Re-measured (read-only `ls-remote`)
develop `697f422f1a394ab00454ced051f018556573837e` (unchanged from Wednesday's 11:1x read); PR 2191 head `96ac07b0cd0daf45a8a27580ca0750de8c826f17` (head only; STATE NOT READ at the API: I have no gh, and A 24th read it OPEN at 00:11Z); PR 2202 head `3c2b6ebe2ab86e679038c50c508f63dc60b76adf`.

## Unmeasured / not done
- PR 2191 merged state; gate 324's verdict; everything on kintsugi and demo (entry fields, empty or missing DOCUMENT, untyped callers); the in-repo caller census; the open-PR census for the KS-1466 paths; lock, queue, drive health; develop's current line numbers; which read routes exist that are provably pure on each box (left to the seat's plan and your ANSWER).
- I did not re-read A 23rd's or A 19th-22nd briefs, nor the common reboot file; the A 24th brief's own pointers carry them. I did not read A 24th's wrap-mail point 5e beyond the text in `out_05_wrap.txt` (5e is quoted in the brief).
- Drafter did not verify the live pane floor; the brief carries Wednesday's 10:2x corrected floor and leaves the stamp to fill it.

## Questions for Wednesday (decide at the stamp)
1. **Scope of ticket item 2** (behavioural cells): the brief puts the gateway workflow-gate cell in scope only if it falls out of the same red test, and carries originate's eight-shape cell. Kam's option text lists only item 1 plus the operator note. OK, or widen?
2. **Box-read route and grant:** the brief makes the seat PROPOSE the route(s) and purity proof in its plan and waits for your ANSWER. Do you want to pre-name a route (and who holds the kintsugi admin token; the project's `4_Credentials/` has rotated admin token files, names only) in the STAMP "Grants" line to save the seat a round trip? Is any kintsugi log/row read already granted in the A 23rd stamp's four grants (I do not know their text)?
3. **Demo:** if no proven-pure route exists, the brief lets the seat leave demo UNMEASURED with the reason. Does Kam's "kintsugi and demo" require both before a build, or is kintsugi plus an accepted UNMEASURED demo enough? The brief says an ANSWER from you must accept it.
4. Pace arithmetic: I forecast READY at 48 to 58 points if the measurement clears (Opus, box-read overhead, tier-1 PR), so A2 is declared unreachable. If you prefer A2 to start even at the cost of KS-1466's build, say so at the stamp.
5. The brief says the only board write is the KS-1466 BLUF comment (Kam's ruling text), after your ANSWER. Confirm that is the intended "first board write".
