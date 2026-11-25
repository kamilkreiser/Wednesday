# B2082 ANSWER: can other Datasec staff get access to "Security Manager"?
Read-only desk answer, 2026-11-25. No az, no network, nothing changed, nothing sent. HPSM-POC is on hold to 2026-12-10 (Kam 2026-11-19); nothing here is built.
Marks: RELAYED = read from a project STATUS/record, not re-measured today. READ = I read it in HP's own text file today.

## BLUF
**Yes, it can be done, and it is cheap, but the access is controlled by Kam (his tenant and his one HP NFR instance), so nothing happens without his word. Recommended: option 2 below. Give each person their own named SM login (a local Windows account on the SM server in the right HP role) and reach it through the existing Azure Bastion route, after Kam invites them as guests to the datasec-rd tenant. Cost A$0. Keep each person at Analyst or Guest, not Administrator.** The one real limit is that Bastion Developer allows ONE session at a time; if several staff need it together, the next step is Bastion Basic (about A$203/month) or Entra Application Proxy (needs Entra P1).

## Which "Security Manager"
| # | Candidate | What it is | Likely what Kam means |
|---|---|---|---|
| A | **HP Security Manager 3.16.0.395** on Azure VM `vm-hpsm-sm` | HP's own product, installed by Datasec on Terry's 10-device NFR licence. | **Yes, most likely.** "Access for Paul and other Datasec members" was his own framing on 2026-10-03. |
| B | HPSM-POC hosted web app (Playbook POC, UAT/demo) | Datasec's own web app. Name only resembles "HPSM". Separate access path (Entra app sign-in). | Less likely. Out of scope; say so if he means this. |
| C | HPSM Composer demo VM `hpsm-demo-vm` (RG `hpsm-dev-rg`, tenant `d500ebad`, sub `0c57ab37`) | Datasec's Composer, public demo. Not HP's product. | No. |
| D | B08 `hpsm-selfhost-vm` (same RG as C) | Planned 2026-10-02 to hold the licence; BLOCKED on quota and nothing was created (B08 STATUS). Superseded by A in a different tenant. | No. Not a live instance. |

Ask Kam to confirm A in one line if his words leave doubt. Everything below is about A.

## Instance A: facts and sources
- **Where it runs.** Tenant `ec01829b-fdcb-4503-9834-eb2ffbd99169` (`kamildatasecrd.onmicrosoft.com`, the "datasec-rd" directory), subscription "Azure subscription 1" `a6b8fe11-d1b5-4293-8727-b34aba08a705`, RG `hpsm-poc-sm-rg`, australiaeast. VM `vm-hpsm-sm` (D4as_v5, Windows Server 2022), VNet `vnet-hpsm-sm`, NSG `nsg-hpsm-sm`, public IP `pip-hpsm-sm` = 52.187.238.167, Bastion `bas-hpsm-sm` (Developer SKU), budget `budget-hpsm-poc-sm` A$250. Controller: `kamil@datasec-rd.com` (Owner). Source: HPSM-POC `1_Project_Definition/Briefs/2026-10-03_B106_STATUS.md` (CHECKPOINT 1) and `2026-10-20_B306_STATUS.md` (Identity). RELAYED.
- **Workspace-rules flag.** This tenant/subscription is NOT among the five Datasec environments listed in workspace `CLAUDE.md` hard rule 4 (#5 is `d500ebad`). Datasec's HPSM-POC CLARIFICATIONS line 24/28 say Kam's own Azure/Entra host Dev/UAT/Demo and he is the payer. So treat it as Kam's own tenant: any `az` or Entra change needs his word and the project's own `AZURE_CONFIG_DIR`. Which of Production/Dev/Sales-demo it maps to is not recorded; I do not assert one.
- **How a person reaches it today (two routes).**
  1. **Bastion Developer.** Portal sign-in, then VM, Connect, Bastion, which opens an RDP desktop in the browser; then Edge to `https://hpsm-sm:7637/`. One RDP session at a time. (B106 STATUS "How Paul gets in".)
  2. **Direct internet.** Since 2026-10-20 Kam ruled "no IP limit, keep SM's sign-in" (card `hpsmpoc-sm-open-without-ip-1020`, choice a, 10:07:27). NSG rule `allow-sm-7637-internet-1020` plus Windows Firewall rule `B306-allow-sm-7637-in` open TCP 7637, so the console is at `https://52.187.238.167:7637/` (self-signed cert, login page, API answers 401 without a token). RDP 3389 stays closed. (B306 STATUS BLUF.) RELAYED, state as of 2026-10-20; not re-measured.
  - The VM's 20:00 auto-shutdown was DISABLED on 2026-10-20 for Paul (B337 STATUS): it runs 24x7, about A$416/month VM alone, over the A$250 budget; Windows Update may reboot it.
- **How sign-in works.** Every SM login is a local Windows account on the VM, in one of four local groups. READ, HP user guide v3.16 `hpsm_3.16_user_guide_en-US.txt` (p3 per B106; lines 235-255): `HPIPSC` Administrator, `HPIPSC_Analyst` all features, limited operations, `HPIPSC_Operator` devices/tasks/alerts only, `HPIPSC_Guest` Dashboard and Reports view-only. Five bad passwords lock an account for 30 minutes (user guide line 255; install guide line 2371, p64 per B106). Console port 7637 (install guide line 2430, p65 per B106). Optional Entra SSO (install guide pp66-83): single-tenant SPA app registration, app roles Administrator/Analyst/Guest, "Assignment Required = Yes"; the guide does not say whether local Windows login stays on once SSO is enabled (B163 STATUS, RELAYED).
- **Who has access today (per records).** SM accounts: `hpsm-sm\kam.kreiser` (HPIPSC, Administrator), `hpsm-sm\paul.waite` (made Administrator 2026-10-20, B337), and the VM admin `hpsmadmin`. Azure/Entra: Kam is Owner; as at 2026-10-06 the tenant had 3 users (Kam's guest, two test users) and Paul had NO Entra account (B163 STATUS). Whether Paul accepted a guest invite since is UNMEASURED. Passwords are only in HPSM-POC `4_Credentials/.env` (`HPSM_SM_USER_*`, `HPSM_SM_VM_ADMIN_*`).
- **Licensing.** The 10 seats are **device** licences, not user seats (install guide p53 per B106; licence confirmed `Full`, `IPSC_DEVICES` 10). Extra staff reviewers consume none. Only printers added to SM do. No user cap is recorded. NFR terms for broader use/Azure hosting are an open ask to Terry (Q6, B106). Do not read this as permission for use beyond Datasec's own staff.
- **Directory facts (B163, 2026-10-06, RELAYED).** The datasec-rd directory is Entra ID Free: no P1, no Conditional Access, no Application Proxy; every real user is a guest. SM holds 8 devices, 5 tasks and 1 scheduled report (B337); Kam's HP-facing demo/POC material may be visible to anyone given a login.
- **Not recorded anywhere I read:** any other Datasec staff accounts; whether Paul's guest invite went out; whether Entra P1 was ever bought (B163's recommendation; Kam's later choice to open the port suggests no).

## Options
Common precondition for all: Kam's word, and the work run by an HPSM-POC seat with the project's own `AZURE_CONFIG_DIR` (never a global login). The 2026-11-19 hold means it waits until 2026-12-10 unless he explicitly asks for it now.

| # | Option | Steps (who) | Security | Cost | Touches |
|---|---|---|---|---|---|
| 1 | Shared existing logins (give people kam/paul/hpsmadmin) | Hand over passwords. | **No.** Shared accounts, no audit trail, hands out Administrator. Do not do this. | 0 | Kam's tenant |
| **2** | **Per-person SM login + Bastion** (recommended) | (a) Kam names the people and role for each (default Analyst, Guest for viewers). (b) Kam invites each as a guest to datasec-rd (his send; it emails them) and Reader on `hpsm-poc-sm-rg`. (c) A seat creates one local Windows account each via run-command, adds it to `HPIPSC_Analyst` or `_Guest` plus `Remote Desktop Users`, hands the password over a secure channel. (d) Person starts at portal, VM, Connect, Bastion. | Named identity at two gates (Entra then Windows/SM), no shared password, least privilege by group. MFA depends on the tenant (no Conditional Access on Free; Azure portal MFA is Microsoft's, not re-verified). Remove an account on leave. | A$0 extra (Bastion Developer free). VM now 24x7 already. | Kam's datasec-rd tenant and subscription (not production by record, but his; and HP is shown from it) |
| 3 | Per-person SM login via the open port 7637 | Same as 2(c), no invite needed; person uses `https://52.187.238.167:7637/`. | Already exposed since 2026-10-20 by Kam's ruling; no Entra gate, so SM login alone stands between the internet and the console (5-try lockout). Fine for a few named people; weaker than 2. | A$0 | Same |
| 4 | Bastion Basic (several at once) | Portal upgrade by Kam/seat; then as 2. | As 2, plus 2 concurrent sessions (Windows limit without RDS licences, B163). | about A$203/month | Same |
| 5 | Entra Application Proxy + P1 (B163 S1) | Buy Entra ID P1 (AU$10.50/user/month, yearly), install connector on VM, assign users, add MFA policy. | Best: Entra pre-auth plus MFA plus SM login, no inbound port. | about AU$126 per licensed user per year | Same; Kam's purchase |

## Recommendation
**Option 2**, with Analyst as the default role (Guest for people who only look). It meets the criteria Kam already accepted on 2026-10-03: named identities, no shared passwords, no open admin port, cheapest, normal browser. It keeps the Administrator pair at Kam and Paul only. If it must serve more than one person at a time, escalate to option 4 (cheap) or 5 (best). Option 3 is the fallback only if the people cannot be invited as guests.

## What Tuesday should tell Kam (say-back, one question)
"Yes, it can be done at no cost: named invites plus a per-person Security Manager login on the existing server, one person at a time. I need from you: which colleagues, and Analyst or view-only for each. Nothing changes until you answer, and HPSM work is on hold to 10 Dec unless you want this now."

## Limits of this answer
Read-only desk research on 2026-11-25; Azure state NOT re-measured (az forbidden). Facts dated 2026-10-03 to 2026-10-20 are RELAYED from project STATUS files and may have moved (VM state, Paul's invite, firewall rule). A 2026-11 check by a seat before any action is required.
