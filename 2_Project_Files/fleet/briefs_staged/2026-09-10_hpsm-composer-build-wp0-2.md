# BUILD COMMISSION — Datasec/HPSM, Policy Composer WP0 + WP1 + WP2

**BLUF.** Kam ruled the architecture's blocking question at 20:16: the Composer lives in a **NEW private repo and a separate Jira project**. The build is authorised. Kam, 18:01: *"full authority to build, spin up resources (local first until I approve)"*. Kam, 18:42: *"Please go ahead and start building once you're ready."* **Commission: WP0 Harness, WP1 Content model + provisional seed, WP2 Schema + cardinality, exactly as section 6.1 of your own architecture defines them, to their definitions of done. LOCAL FIRST: nothing in any cloud, nothing billable, until Kam approves.**

## HOW YOU BOOTED — CHECK IT FIRST

This session boots through HPSM's own `Launch_Claude.command` (session 32's flag 1, which was Tuesday's defect). **First action: confirm `AZURE_CONFIG_DIR` and `GH_CONFIG_DIR` point at HPSM's own `4_Credentials/`, and say so in the plan confirmation with the launcher's preflight lines verbatim.**

## QUEUE

1. **WP0 Harness** in a NEW local git repository for the Composer, inside the HPSM project folder. Propose the folder name in your plan confirmation. It must NOT be inside `2_Project_Files`, and the analysis repo at the project root must ignore it. Definition of done, from section 6.1: `docker compose up` gives all health endpoints green; CI green locally; secret scan on; **no cloud calls, proven by an egress test.**
2. **WP1 Content model + provisional seed**, per the seed contract and applying Kam's rulings below.
3. **WP2 Schema + cardinality**, from `schema/policy_composer_DRAFT.sql`: every section 2.2 check automated at the database layer, RLS negative tests, released-version immutability, one editable version, app role lacks INSERT on policy. **The RLS policies and the approval-voiding trigger branch were NOT exercised in session 32; proving them is WP2's.**
4. **The GitHub repository and the Jira project.** Kam ruled that they exist; creating them needs identities. HPSM's CLAUDE.md records this project's `gh` store as empty and the analysis repo's remote as waiting on Kam (HPSM-40). **Measure what your identities can do** (`gh auth status` in HPSM's store; whether the Jira credentials can create a project). For anything needing Kam's hands, send Tuesday ONE QUESTION mail with the exact steps: the page, the click, the command. **Do not block the local build on it.**

Order, from section 6.2: WP0 first; then WP1 and WP2 as parallel lanes.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- `hpsm-composer-repo-and-jira-home` — **new-repo** — *"New private repo and a separate Jira project"* (panel 20:16:00). Lands in: architecture section Q, Q-05 marked RULED; the new repo's README.
- `hpsm-composer-silent-columns-severity` — **hpsm-severities** — *"Yes - HPSM's own severities as a second derived source, frameworks left empty"* (20:15:54). Lands in: Q-19 RULED and seed contract section D. WP1's provisional seed carries HPSM's item severities from the Policy Preview as a DERIVED source with provenance; ISO 27001, NIST CSF, SOC 2, HIPAA and E8 maturity stay EMPTY and flagged.
- `hpsm-composer-remediation-sow-vs-spec` — **spec** — *"The spec governs - always remediate High"* (20:15:42). Lands in: Q-20 RULED; the content default follows spec UQ-001. **This is Kam's ruling over your recommendation. Record it as his, keep your reasoning in the Q-20 row as history, and do not re-raise it.**
- `hpsm-composer-remaining-16-questions` — **accept** — *"Accept all sixteen as working assumptions"* (20:15:19). Lands in: Q-03, Q-04 and Q-06 to Q-18 marked ACCEPTED AS WORKING ASSUMPTIONS.

Your wrap names the file and section where each landed.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- The output pipeline is manifest-first (Tuesday's ANSWER, 2026-09-10 08:54Z).
- Build sessions boot through HPSM's own `Launch_Claude.command`, never through a coordinator's wrapper (same ANSWER, flag 1).
- Today's earlier Kam rulings stand: Q-01 derive, Q-02 image.png excluded, and the CRM and finance discovery docx excluded.

## HOLDS

- **LOCAL FIRST.** No Azure resource, no cloud call, nothing billable, until Kam approves. WP0's egress test is the proof.
- **Nothing HP-facing.** No HP-NDA material enters the Composer. Q-04's condition stands: HP's private endpoints only if partner or NDA terms allow, and none of that is in WP0 to WP2.
- **No HP marks** in any brand profile (Q-03).
- **Composer code never goes into `2_Project_Files`.** The Composer repository is PRIVATE when it gets a remote.
- **Jira:** create only the Composer's own project and epics, and only once the identity question is answered. Nothing on the HP SOW-01 board.
- **Never `rm`** — quarantine. Never reproduce a secret value, prefix or length.
- **Mail Tuesday at `tuesday-agent@agentmail.to`**: the plan confirmation, QUESTIONs and the wrap. Not `wednesday-agent@`.

## REPORT

Per work package: the definition of done item by item, with the evidence (command, output, control). What was not tested. Where each Kam ruling landed.

PROVENANCE:
Kam's build authorisations and the Q-05 ruling | kam_rulings_today.sh and the panel relay mails in /Volumes/KK_T9_External_HDD/TUESDAY, panel 18:01, 18:42 and 20:16 | read 2026-09-10
the four ruled cards and their choices | decision_queue.sh show in /Volumes/KK_T9_External_HDD/TUESDAY | read 2026-09-10
WP0-WP2 definitions of done and their order | /Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/1_Project_Definition/Architecture/2026-09-10_policy-composer/2026-09-10_policy-composer_ARCHITECTURE.md sections 6.1 and 6.2 | read 2026-09-10
HPSM-40, the empty gh store, and no Composer code in 2_Project_Files | /Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/CLAUDE.md lines 89 and 229 | read 2026-09-10
RLS policies and the approval-voiding trigger not yet exercised | datasec-hpsm session 32 wrap mail to tuesday-agent@, 09:42Z | read 2026-09-10
the launcher exports per-project AZURE_CONFIG_DIR and GH_CONFIG_DIR | /Volumes/KK_T9_External_HDD/!CODING/Datasec/HPSM/Launch_Claude.command lines 128 and 142 | read 2026-09-10
scope of this round: local only, nothing billable | Kam panel 18:01 verbatim, full authority to build, local first until he approves | read 2026-09-10

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-10 20:21
