---
date: 2026-10-03
type: grant
source: Kam, email forward to friday-laptop-agent@ 2026-10-03 09:58 AEST + live board 12:1x
status: live
tier: W
---

# Grant: deploy what HP Security Manager needs in Azure (subscription kamil@datasec-rd.com), get it working, then integration and contents — review with Kam Tuesday 6 Oct; a working copy in 10 days (Tue 13 Oct)

**The operative case, so the headline matches it:** Friday is about to create Azure resources for HP Security Manager 3.16 (Datasec / HPSM-POC, the Playbook POC). **Inside this grant: create what the install needs in the `kamil@datasec-rd.com` subscription, install SM 3.16 with Terry's 10-seat NFR licence, then study integration and contents.** Report every resource and its monthly cost as it is created.

**His words, verbatim (email, 09:58 AEST):** *"Please deploy what you need in Azure (subscription kamil@datasec-rd.com) and get it working. Once you do, look into integration and contents. We can review it together on Tuesday. If you need anything else from Terry, please let me know what the ask is."*
**Live board 12:1x, verbatim:** *"…I want to have a working copy within 10 days so we can start testing and finetuning. I also sent an email with details to security manager, you have my approval to deploy resources in azure to set things up, install, look at integration, etc."* (`date -j`: 2026-10-13 is a Tuesday; 2026-10-06 is a Tuesday.)

**Access for people, ruled 12:24:08 (live board), verbatim:** *"no need.  you choose a reasonable option and deploy.  no need for me to delay things"* (his 12:21:44: Paul and other Datasec members will want to look at it). So the access route is Friday's choice, made against stated criteria (named identities, no admin port open to the whole internet, the cheapest browser route), created and reported. Invitations to people stay Kam's sends.

**What it covers (Friday's reading):** resources in the datasec-rd subscription for the SM install (a Windows VM sized to HP's minimums, its disk, network, a budget alert), the install itself, and integration study/builds inside HPSM-POC. **Not covered:** anything to HP or any human (Kam relays asks to Terry), exposing the SM console to anonymous internet access, other subscriptions/tenants, production, the HP Restricted-documents hold (pickup standing hold), and changing licence terms. **No expiry stated:** it is tied to this setup; re-read if the scope moves past Security Manager.

**Secrets:** the SFTP login lives only in `4_Credentials/clients/datasec/inbound/2026-10-03_hp-security-manager-3.16/sftp.env` (0600); the drop expires 2026-11-01. Never copied into a brief, a note or a tracked file.

**Family:** [[2026-08-07_protocol-v1.3-signed-delegation]] (money is his, and he granted it here) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5) · [[2026-09-08_name-the-field-that-says-whose-it-is]] (every resource names its subscription and RG).
