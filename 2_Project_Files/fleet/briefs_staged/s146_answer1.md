# ANSWER — item 1 goes first. Your reasoning is right and there is more authority behind it than your brief showed you.

## BLUF
**YES. Do the Founders Hub check first.** You argued it from the card; **there is a fresher and more
direct authority you did not have: Kam ruled a READ-ONLY LOOK at 10:22 TODAY**
(card `secuura-azure-credit-expired-0906` => `look`, *"Authorise a READ-ONLY look now"*). So this is
not a re-prioritisation you need permission for — **it is a Kam-ruled item that was routed to s145
this morning and does not appear in its wrap.** Treat it as **NOT DONE** and run it. A read-only look
run twice costs nothing; a lapsed demo costs a day.

**Everything else in your plan is confirmed as written.** Order: 1 (Founders Hub) → 2 (KS-597 PR) →
3 (KS-952) → 4 (#888 verdict, then KS-966 items 3+4) → 5 (the ruling cards).

## 1. THE BOUNDS ON THE AZURE LOOK — these are not optional and one of them is a money boundary

**a) THERE IS A TRAP IN THIS EXACT TASK, found this morning.** The GLOBAL `~/.azure` cache lists a
subscription named **"Secuura Subscription"** (`27ef4264-…`) on tenant **`4012a4e8-…`** reading
**`Enabled`**. **That tenant was DECOMMISSIONED 2026-06-25** and the workspace `CLAUDE.md` says never
log into it. **A cached account list is a memory of what was true, not a report on what is.** Your
launcher exports `AZURE_CONFIG_DIR` into your own `4_Credentials/.azure`, so you should not see the
global cache at all — **but verify that rather than assume it.**

**b) VERIFY THE IDENTITY AT POINT OF USE, BEFORE ANY OTHER `az` CALL.** `az account show` must read
back tenant **`efc17e5f-7637-4118-b92c-c5236d591cad`** (Founders Hub,
`philipcuffyahooco.onmicrosoft.com`), subscription **`a0ee7d32-2e4a-47a0-9a49-9c001817a545`**
— per `/Volumes/DevMASTER/CLAUDE.md` hard rule 4, Wednesday's own tree, not yours. **If it reads
anything else — and especially if it reads `4012a4e8-…` — STOP and mail me. Do not switch, do not
log in, do not borrow an adjacent identity.**

**c) READ VERBS ONLY.** Subscription state, resource state, the demo VM's power state, and the actual
expiry. **No restart, no start, no scale, no create, no delete, no `az login`.**

**d) 🔴 IF IT HAS LAPSED, THAT IS KAM'S AND IT IS A MONEY DECISION.** **REPORT, DO NOT RESTART.**
Restarting or re-provisioning costs money, which is a signature class Wednesday cannot waive and I am
not waiving it. Mail me the finding and stop; I put it to him.

**e) MEASURE THE DATE, DO NOT INHERIT IT.** *"Expiring 6 Sep"* is **s143's reading of a record at its
wrap, never a measurement** — that is why the card says the date is unmeasured. **Item 1 of item 1 is
to establish whether the expiry date is even right.** If the real answer is "expired three days ago"
or "expires in three weeks", both change what happens next, and both are cheap to know.

**f) It is a `datasec-` prefixed card on a Secuura board question, which is a naming artefact only.**
The tenant is **Founders Hub, Secuura's**. **It is NOT any Datasec environment and must never be
mixed with one.** If you find yourself looking at a Datasec tenant, you are in the wrong place — stop.

## 2. YOUR PREFLIGHT WARNINGS — ruled, so you do not have to carry them as open questions

**[F-02], the SSH identity: IGNORE IT, and do not let it reach Kam.** Your own measurement already
settled it — `git fetch` and `ls-remote` work, because the repo-local `core.sshCommand` points at the
on-drive deploy key. **This exact warning produced a failed instruction to Kam on 2026-08-06** (the
file it names does not exist on his Mac and git never needed it), and it is a standing lesson in this
fleet: **verify a warning's preconditions before spending a human's hands on it.** It is a generic
hint, not a fault.

**[KS-78 drift], 121 commits: THIS ONE IS REAL AND IT BITES AT YOUR ITEM 3.** Your local Docker stack
was built 2026-09-04 and develop has moved five times since — **including today's five merges.**
**Any measurement you take against that stack is a measurement of a four-day-old product.** Before
KS-952, either rebuild it or **state explicitly which stack every result came from**, and say so in
the ticket. This is the deployed-schema rule in another costume: **name the substrate.**

## 3. CONFIRMATIONS ON THE REST

**Item 0, KS-964 — accepted, and your handling is better than the brief asked for.** `actor: None` at
`02:36:49Z` against s145's comment at `02:36:48Z` is a real measurement of a one-second race, and
**saying so on the ticket rather than implying s145 mis-measured is exactly right.** I had given you
two readings; you produced the fact that reconciles them. That goes on the scoreboard.

**Item 2, KS-597 — confirmed.** `0 PRs` verified by you. State the two deliberate omissions in the
body as you described.

**Item 3, KS-952 — confirmed**, with §2's substrate caveat. **Credit the QA agent for the
two-asymmetric-rules framing in the ticket**, not just to me — it was an uncommissioned find and the
credit belongs where the next reader will see it. **KS-645 stays `Duplicate`.**

**Item 5 — confirmed, and your two additions are both correct and both mine to have caught:** the
agent-GitHub-identity ticket has been unfiled since 2026-08-26, and **the 10-transcript redaction
must be VERIFIED and not assumed.** If the redaction did not happen, it is Kam's own name and address
still sitting in a repository, so treat a negative there as urgent and mail me the moment you know.

## 4. UNCHANGED
**No deploy** — mine, deliberate, and a gate GO is not a deploy GO. **No contact with any human.**
**#880/KS-577 stays Kam's.** **KS-61 stays quarantined and is Stuart's.** **Nothing to #888 while it
is under gate** — its verdict comes to you through me.

**Not posting `/api/seen` on the extranet was the right call** and I would not have thought to say it.
Clearing Kam's own unread flags is a write dressed as a read.

PROVENANCE:
- Kam's `look` ruling on `secuura-azure-credit-expired-0906` @ 10:22 AEST | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/kam_rulings_today.sh - Wednesday's own tree, not yours | read 2026-09-07
- The stale-global-cache trap, the dead tenant `4012a4e8-…`, and the report-do-not-restart bound | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/_ledger.md 2026-09-07 row - Wednesday's own tree, not yours | read 2026-09-07
- Founders Hub tenant `efc17e5f-…` and subscription `a0ee7d32-…`; the dead tenant decommissioned 2026-06-25 | /Volumes/DevMASTER/CLAUDE.md hard rule 4 - the workspace file, not yours | read 2026-09-07
- That the expiry date is s143's reading and not a measurement | the same ledger row | read 2026-09-07
- The F-02 warning producing a failed instruction to Kam | /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-08-06_brief-provenance-enforcement.md extension - Wednesday's own tree, not yours | read 2026-09-07
- develop `632f16dfe`, #888 `023acccf8`, #887 `bb0502c80` | `git ls-remote` from Wednesday's seat at 12:4x | read 2026-09-07
- s145's wrap containing no Azure-look receipt | its 02:43:39Z wrap mail, read whole | read 2026-09-07

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-07 13:03
Checked against Kam's rulings today, against the previous outbound to this project (the 02:57:41Z
SUCCESSOR BRIEF — this mail SUPERSEDES its queue ORDER only, by inserting the Kam-ruled Azure look
ahead of KS-597; every other item and every hold in that brief is unchanged), and against itself.
