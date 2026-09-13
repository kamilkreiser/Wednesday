BLUF. **Kam ruled both open HPSM cards at 18:02:05 and 18:02:28 AEST.** These are first-party card taps on Tuesday's tab, relayed to tuesday-agent@ as "[Kam -> Tuesday] panel message 2026-09-13T18:02:…".
- **`hpsm-composer-live-demo-upgrade-after-c12` → `upgrade-fresh-with-release`,** verbatim: *"After all merges upgrade the live demo and create fresh engagements, including a no-device-group one for the release walk-through"*.
- **`hpsm-composer-demo-release-with-device-groups` → `build-c11`,** verbatim: *"Commission fenced synthetic device-capability rows plus the code in four places now (new lane, will not land by Monday)"*.
- **YOU (session 43) operate the live-demo upgrade.** Session 40 has closed, and you are the only HPSM seat.
- **This SUPERSEDES the "No deploys" hold in your 07:05:44Z brief, for this one upgrade of pc-lane-a and the Azure demo only.** Every other hold stands.

## PRIORITY ORDER (Kam reviews Monday 2026-09-14)
1. **The Q re-chain → W → second READY,** as CONFIRMED at 08:07:30Z.
   - "After all merges" = after Q and W are on main with their chains green. Tuesday's reading; it is not a wait on the feedback lanes or C11.
   - If a feedback READY is already merged and chain-green when you reach step 2, include it, and say so in the report.
2. **The live-demo upgrade (below).** It must land in time for Monday.
3. **Feedback lanes F-API / F-WEB**, as confirmed.
4. **Lane C11**, starting NOW in parallel wherever its paths are disjoint. It will not land by Monday.
The load rules of 08:07:30Z apply to every docker-heavy step. A gate verdict still gets the docker lock first.

## THE UPGRADE: S42's prepared shape, executed by you
- **Starting point:** S42's drafted combined upgrade message `<S42 scratchpad>/s40-message-combined-upgrade.txt`.
  - Handover sections S2 and 4zg.
  - The deploy records `1_Project_Definition/Architecture/2026-09-10_policy-composer/qa-wp5/evidence/azure/README.md` and `qa-switch-on-s40/`.
  - **Read them; do not assume.** S42's scratchpad is purgeable, and S40's may be too.
- **Target head:** main after W merges. Name its SHA, commit count and chain evidence in the report **BEFORE touching either stack**.
- **Identity, before any `az`:**
  - `az account show` under HPSM's OWN `AZURE_CONFIG_DIR`: tenant `d500ebad…`, subscription `0c57ab37…`, service principal `hpsm-claude-deploy`, resource group `hpsm-dev-rg` ONLY.
  - **NEVER touch `datasec-sales-portal-rg`** (Vision's LIVE production in the same subscription).
  - **If an identity, an SSH key or the NSG source IP is missing or refuses:** STOP and report exactly what is needed. Kam supplies logins. Never work around a refusal.
- **Pre-checks, read-only, on both stacks:**
  - D1: `PC_PLATFORM_TENANT_ID` default; the `…da7a` row counts;
  - object store ready (lane Q's api refuses to start without it); the MinIO image/digest actually pullable on the VM (your I-04);
  - no new env beyond what the READY names.
- **Order:** pc-lane-a FIRST, then Azure. For each stack:
  - rollback command to `c2fbc36` stated and ready;
  - upgrade;
  - **~10-minute post-upgrade check:** api healthy; Azure root and `/api/health` answer 401 without credentials and with wrong credentials; one store + download round trip; the Preview and policy document rendered and opened;
  - **on failure, ROLL BACK FIRST, then report.**
- **Fresh engagements** on the SYNTHETIC tenant of each stack:
  - (a) one engagement WITH one device group, for drafts;
  - (b) one engagement with ZERO device groups, taken to RELEASE through the product's own workflow. Exceptions and both approvals are recorded by the synthetic personas, **never fabricated in the database.** The released PDFs carry SYNTHETIC and "Not signed".
  - **Existing engagements are left untouched.** They will answer 409 CONTENT_VERSION_CHANGED; the card said so and Kam accepted it.
- **Report to tuesday-agent@**, subject `REPORT (seat hpsm-28f5, session 43): live demo upgraded to <sha>`, carrying:
  - head;
  - per-stack pre-checks;
  - the post-check results;
  - the engagement names;
  - the release label reached on (b);
  - one output opened per stack, with where it is;
  - the rollback path.
- **Access control on Azure stays as it is:** basic auth on every request, and nothing public added.

## LANE C11 (new, fenced, synthetic only)
- **Scope:** fenced SYNTHETIC device-capability rows in `content/release-demo` ONLY, plus the code in the four places S42 measured:
  - `content-bundle.ts:54`
  - `apps/api/src/content.ts:320-322`
  - `packages/db/src/releases.ts:45,157-159`
  - `apps/api/src/routes/engagements.ts:50-57`

  Verify those lines at your head before citing them.
- **Fences, exactly like C12:**
  - `release-draft` byte-identical (its content:check hash is unchanged; prove it);
  - every row has SYNTHETIC `source_refs`;
  - **no invented real-HP facts;**
  - a real tenant never sees synthetic capability rows (the switch-ON fence).
- **The "unknown" support case (your I-02):** it must no longer be silent. Propose the issue code in your ACK. Tuesday rules it.
- **Partition, one agent per file:**
  - Lane C11 owns `packages/engine/**` and `content/release-demo/**`, plus EXACTLY the three files above in `apps/api` and `packages/db` (content.ts, routes/engagements.ts, releases.ts) and their tests.
  - F-API keeps its feedback modules and routes, `authz.ts` rows and `packages/db` migrations.
  - **If C11 needs a migration, it is 0017**, numbered by the seat after F-API's 0016, and you state that in the ACK.
  - Any file both would touch: stop and sequence it. Never let two lanes edit it.
- **Checks:** RED-first tests; mutants on the fence; a zero-group AND a one-group release both reachable on a seat stack with switch ON; the demo CONTENT_HASH change named; its own READY FOR QA (tier 1: content + engine + fence).
- **Not in the Monday upgrade.**

## ACK required
**One mail with:**
- the C11 lane's exact paths and branch;
- whether C11 needs a migration;
- the proposed issue code for "unknown" support;
- the planned time window for the upgrade.

**Then proceed. No wait for Tuesday is needed unless the ACK raises a question.**

Tuesday
