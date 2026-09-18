---
date: 2026-09-18
type: reference
source: S65's measured answers (this folder's README.md + its 00:34:50Z dependency measurement); Kam's instruction "let me know when the push is unblocked"
status: live
updated: 2026-09-18 — the open question is RESOLVED; the push waits on step 10 ONLY
---

# "Kam's push is unblocked" — the predicate, so it is a CHECKLIST and not a judgement

**Kam's instruction, verbatim (2026-09-18):** *"keep going and let me know when the push is unblocked"*.

**This file exists because "unblocked" is the kind of word a tired seat decides by feel.** It is
evaluated line by line at every MERGED mail and every checkpoint, **on `origin/main`, never on a
branch**. A seat that cannot tick every line does not tell him.

## THE PRECONDITION, in one sentence

> **Kam can push as soon as the minimum set is merged to main, the release version string is agreed
> (`2.2.0`), and RD-529 O-8 has landed on main. Step 11 gates the ZIP, not the image.**

**RESOLVED 2026-09-18 00:34:50Z, and it recovered a whole step of his time.** S65's chain was drawn
linear (push waits for 10 AND 11); Tuesday challenged it; S65 measured the Dockerfile and `.dockerignore`
and confirmed step 11's artefacts — `scripts/deploy-dev.sh`, `scripts/provision-customer.sh`,
`azure-marketplace/**`, `docs/MARKETPLACE_TEST_PROCEDURE.md`, `docs/REFERENCE_ARCHITECTURE.md` — are
**not shipped in the image**. So step 11 runs in parallel with his round trip.

## 🔴 SAFETY RULE — build from MAIN at the merged head, NEVER from the package branch

The package branch has not merged main since RD-470 landed. Relative to main it **re-adds the
`ADMIN_RESET_KEY` break-glass route** (`/api/setup/admin-reset`) that **Kam himself ruled removed** —
C-48, `CLARIFICATIONS.md:291-292`, his panel words 2026-09-17 08:05:14: *"Decision
nexusai-rd470-break-glass-remove: remove — Remove the route (Recommended)"*.

**An image built from the package branch would not be a regression — it would silently reverse the
principal's own decision, inside the artefact he was about to submit, with nobody positioned to notice.**
The image is opaque and "the package branch" is the obvious ref to pick when building a package. This is
a safety rule with his name on it, not a build preference.

## The wake, so this does not rest on remembering

- **`2_Project_Files/fleet/watch_nexusai_main.sh <baseline-sha> <poll-s> <max-min>`** — reads
  `origin/main` directly and **exits** when it moves. The harness re-invokes the seat on a background
  job's exit, so the exit IS the wake. **Armed 2026-09-18 ~10:3x, baseline `e0ea198a`, poll 60s, max
  180m.** Independent of every agent's liveness: a seat that dies quietly produces no merge and no mail,
  and this still reports. Both branches exercised before arming (fire rc 0 with the SHAs; quiet rc 3
  after a full minute of real polling, no false fire).
- The agents' own MERGED mails remain the primary signal. This is the backstop, not a replacement.
- **If it has expired, re-arm it from the current head.** Do not replace it with an intention to check.

## THE CHECKLIST — every line ticked, or he is not told

### The minimum set, MERGED to `origin/main`
- [ ] RD-436 + 452 + 501 + 499 **+ RD-535** — restore reopens a configured deployment to anonymous takeover
- [ ] RD-486 + RD-523 — stored Azure OpenAI key sendable to a caller-named host and to a redirect target
      ✅ **GATED: GO at `2d83967`, worst severity Low (2026-09-18 01:38:50Z). DO NOT RE-GATE IT.**
      B-1 closed at every caller incl. `GET /api/chat/stream` (not in the brief); mutation Q4 proved the
      'count at first byte' relaxation CANNOT hide a real leak; 10/10 mutations, sha256-identical
      reverts; verify PASS 3275/3275. **Merge-eligible and deliberately QUEUED BEHIND RD-436+RD-535**
      — the release image is built from `main`, so merging it before RD-516 exists would put the
      ai-test dial path for a planted endpoint onto the exact ref the customer image is built from.
      Second merge hand-resolves the mechanical overlap under C-57; **any logic/product conflict STOPS.**
      Its MERGE commit must state that the branch commit's PRIOR WORK claims a change the diff does not
      contain (RD-551 O-3) — corrected FORWARD, never by amending a gated head (C-68).
- [ ] RD-516 — anonymous SSRF via ai-test (same class as RD-486; one without the other half-closes it)
- [ ] RD-518 — `KEYVAULT_NAME` vs `KEY_VAULT_NAME`: Key Vault silently does nothing in every deployment
- [ ] RD-503 + 442 — SUPPORT.md's only AI-settings fix does nothing on a real deployment
- [ ] RD-464 round 3 — kept in (Kam approved it, it is built)
      ⚠ **NO LONGER A DROP CANDIDATE, and it is now COUPLED.** See RD-545 below.
- [ ] 🔴 **RD-545 — lands WITH or BEFORE RD-464 round 3; r3 does not merge without it.**
      **This is a regression OUR OWN work introduces, not a pre-existing defect.** It does not
      exist on `e0ea198`: the C-70 one-limiter collapse is what removes the surviving limiter.
      An anonymous caller in the open window POSTs `/api/setup/ai-config {aiEnabled:false}`,
      RD-464 r3's limiter then SKIPS under the C-59 AI-off rule, and the boot metadata call still
      runs because `aiReadiness.js` calls `healthcheck()` before consulting the gate — so
      **AI off = unlimited anonymous outbound to any caller-named host.** Every component is
      correct; the pair is the hole. Measured by S65's RD-516 design pass, 2026-09-18.
      **Closed by BOTH:** RD-516's host policy (WHERE it can connect) and a limiter keyed to the
      REQUEST rather than to the AI-enabled state (HOW MANY). C-59 permits the metadata call; it
      says nothing about its VOLUME, and reading 'permitted' as 'unlimited' is the gap.
      If they must merge as one change, merge them as one change.
- [ ] The listing folds — RD-465 O-4, RD-454 O-4

### The two additions the dependency measurement turned up
- [ ] 🔴 **RD-549 — CONFIRMED AND IN THE MINIMUM SET. Data exfiltration, measured end-to-end on BOTH heads.**
      A stranger anonymously saves their own Azure-suffixed endpoint and key during the open window; it
      survives setup; the admin configures Entra and enforces sign-in (the window genuinely shuts —
      anonymous GET then 401); **and the next chat a SIGNED-IN admin sends goes to the attacker.**
      Captured on the wire, identical on `e0ea198` and `2d83967`: 21,855-byte POST to the attacker's
      host with the attacker's api-key, carrying **38 distinct REAL user names** plus real usage
      figures — extracted from the captured prompt, not inferred. Dial proven with the
      `diagnostics_channel` oracle and its positive control.
      **NO DNS CONTROL NEEDED** — the attacker creates their own Azure OpenAI resource, Microsoft issues
      the hostname and certificate, so it is on RD-516's sourced list BY CONSTRUCTION, resolves public,
      and layer 3 PINS and dials it. **RD-516 allows this correctly by its own rule; it is a different
      property and RD-516 is not the remedy.**
      `first-run-setup.js:282-296` paints a GREEN 'Configured' badge for the attacker's settings, so an
      admin completes setup without touching the AI step. No provenance is recorded anywhere.
      **REMEDY SHAPE RULED (Tuesday):** write-time provenance, then anonymously-written config is
      PERSISTED BUT INERT until an authenticated admin positively confirms it, and no green badge until
      then. **Not warn-and-continue** — a warning whose default leaves the attacker active is a notice,
      not a control.
      ⏳ **OUTSTANDING AND KAM IS WAITING ON IT: does the LIVE 2.1.1 listing carry this?** Measuring at
      head `6fb497d`. **Report it to him whichever way it goes — a NO is as urgent as a YES.** Anything
      about the live listing or telling anyone outside is HIS signature class; state facts only.
- [ ] **RD-550 — tier pending ONE measurement:** which data-source path a MARKETPLACE deployment takes.
      Local-database path → saved AI config is lost on every restart for every customer we ship to, which
      is blocker/minimum-set. Log Analytics → a real defect on a path our customers do not take, ticket.
      It only ACCIDENTALLY bounds RD-549 on the local path — **luck, not a control; never counted as
      mitigation.**
      An anonymous caller in the open window can persist an Azure-suffixed endpoint **plus an
      encrypted key** (measured: 200, read-back confirms; a literal RFC1918 value is refused 400).
      **RD-516 does NOT cover it** — it refuses PRIVATE addresses, and a planted host that passes the
      sourced suffix list resolves public, so layer 3 pins it and the guard faithfully dials the
      attacker. S65 accepted that its 'RD-516 refuses the dial' sentence implied coverage it does not
      have. **C-42's accept covered takeover of an UNCONFIGURED deployment, not data leaving a
      CONFIGURED one** — so this is outside it. RD-474's family, different field.
      **The measurement running now:** plant anonymously → complete first-run as an admin would →
      configure sign-in → sign in → trigger a real chat call and whatever `tools.js` sends job rows
      through → observe where the request goes and whether the planted key travels with it, proven at
      the listener with the diagnostics_channel oracle and its positive control.
      **Verdict shape agreed:** YES → blocker, joins the minimum set, remedy is clear-at-setup or
      surface-to-admin, **never RD-516's host policy**. NO → withdrawn to a ticket, with the
      measurement and the file:line of whatever stops it.
- [x] **RD-529 O-8 — MERGED to main as `d881f953`, CI ALL GREEN (Build 35293779197, Gitleaks 35293779244, npm-audit 35293779237, all complete 02:05Z). Merged tree byte-identical to the branch tree (`91cbf6b` both, tree ids COMPARED not assumed), so the branch's PASS 3207/3207 IS the merged tree's run. No static files touched, so nothing for S66 to re-run.**
      **✅ 2 OF 3 PUSH PRECONDITIONS ARE NOW MET** — version `2.2.0` (Kam's ruling) and RD-529 O-8 on main. **Only THE MINIMUM SET remains.**
      _(original line)_ **RD-529 O-8 — merged 01:04:46Z** (merge of `470510e`; one file, one line, verified wording-only by Tuesday at source before and after). **RD-529 O-8** — the one-line placeholder wording fix in `DEPLOYMENT_GUIDE.md`, **which IS shipped
      in the image**. Ruled by Tuesday: it lands on main BEFORE the push rather than being baked in.
- [x] **The release version string is `2.2.0` — RULED BY KAM.**
      **His words, verbatim, TERMINAL channel (not the panel): *"2.2.0 is fine, keep going"*.**
      Received and receipted by this seat at 2026-09-18 10:43 AEST; that stamp is this seat's PROCESSING time,
      generated from the clock, **not his send time, which this seat cannot observe.**
      ⚠ **It is NOT in `chat_kam.json`** — he typed it in the terminal, which is invisible to
      `kam_rulings_today.sh`, `reconcile_rulings.py` and every panel-derived instrument
      (this seat's ledger, 2026-09-13, w=4). **A successor looking for it on the panel will find
      nothing and must not conclude it was never said.**
      **This supersedes Tuesday's own call.** It was mine under v1.3 sequencing until 10:4x; it is
      now his ruling, so the push message NO LONGER offers a correction on it — it states it.
      The build checker requires the image tag to EQUAL the package version; both are pinned to
      `2.2.0` before anything is built.
- [ ] ~~The release version string is agreed~~ — superseded by the line above.

### The telling
- [ ] **ONE LINE OF INFORMATION HE IS OWED AT THE PUSH, not a question:** an Azure OpenAI host on a
      suffix we could not SOURCE is refused by the RD-516 policy. **Commercial and Government are
      unaffected** (`openai.azure.com`, `cognitiveservices.azure.com`, `services.ai.azure.com`,
      `cognitiveservices.azure.us` are all sourced). What is refused is any unsourced form —
      the unconfirmed `openai.azure.us`, and China, which has no CognitiveServices row at all.
      The admin-extendable allow-list is TICKETED, not built. **He should not learn this from a
      customer**, and stating it narrowly matters: 'Gov and China are refused' overstates it and
      an overstated record gets discounted wholesale.
- [ ] Every box above ticked and **re-read on `origin/main` in the same action as writing to him**
- [ ] His push steps from 2026-09-17 23:23:47Z re-confirmed as still correct. **S65 confirms they are,
      with TWO AMENDMENTS that must reach him or the message is wrong:**
      1. **The registry is measured empty again today, so his step 3 is a FIRST push, not a re-push.**
         Wording that implies an existing image will read as wrong on his screen
         ([[../../learnings/2026-09-10_steps-to-kam-are-a-claim-about-his-screen]]).
      2. **His step 5's anonymous-pull proof is now the ONLY thing that proves the customer path**,
         because he has ruled there is no pre-submission test deploy. Say that, so he knows the check
         is load-bearing rather than ceremonial, and does not skip it to save a minute.
- [ ] Told on the panel, **action first**, steps on their own lines, **the version named**, no date attached

## NOT in the predicate — gates the ZIP, runs in parallel with his push

⚠ **THE RELEASE GATE BRIEF MUST CARRY THESE THREE, ruled 2026-09-18 ~12:0x when RD-505's READY was
folded into it rather than given its own session** (Kam's 09:22 minimise-duplication rule). The release
gate runs on the package branch **with main merged in and the real digest**, so it is a DIFFERENT TREE
from `a643fe1` and none of these survive the fold by themselves:
1. **The 18 wizard arm-ttk tests re-asserted AT THE RELEASE HEAD** — not the 49/49 measured at `a643fe1`.
2. **The one-step revert re-verified at the release head.** This is the property promised to Kam in his
   own terms; merging main in is exactly what could break it.
3. **The fail-closed (C-40) proof re-run, not cited** — at the release head the old run is evidence
   about a tree that no longer exists.


main merged into the package branch · the RD-505 removal on that branch · the dev scripts ·
the listing folds in `azure-marketplace/**` · RD-526..RD-528 · RD-543.

## NOT in the predicate at all

RD-524, 525, 531, 537, RD-495, RD-497, RD-510, 492, 519, 471/472/475/487/457/438, lock v3, HISTORY
entries. All real, all ticketed, none deploy-blocking. **Do not let them creep into the gate** — they are
the difference between telling him today and telling him next week.

**OBSERVATION for the push message (Tuesday, 2026-09-18 13:0x; read from Partner Center's "Previously published packages" tab by Chrome's own AppleScript, not from memory):** the listing reads `2.1.0 | 9/15/26 | NexusAI_plan-managed-ai_2.1.1_6fb497d.zip` and `2.0.0 | 5/12/26 | plan-managed-ai.zip`, plus a "Load more". **The VERSION column says 2.1.0 beside a file named 2.1.1**, so Partner Center's version field may be entered separately from the package. When Kam uploads the 2.2.0 zip, the push message should tell him to set that field to **2.2.0** (his ruling) and check it matches the file. UNMEASURED: whether "Load more" lists older packages; the tab stopped answering scripted reads after the list was expanded.
