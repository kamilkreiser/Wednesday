# WP01 - VMware Workstation licence and hypervisor look-up

Fetch date: 2026-11-20. Method note: quotes below are as returned by the fetch tool (a small model summarising each page), so they are page text as relayed, not raw HTML. Search-result snippets are NOT treated as evidence.

## BLUF
1. Current Workstation Pro needs NO licence key and is free for commercial use (Broadcom FAQ, KB 368667, 26H1 blog 2026-05-14).
2. KB 368734 steps: Broadcom Support Portal account (basic is enough), My Downloads, "Free Software Downloads available HERE", search Workstation, pick latest. Export-compliance approval "can take several weeks".
3. With Hyper-V/VBS ON, Workstation runs (Hyper-V/WHP mode) but nested virtualisation (VT-x/EPT) is blocked; Broadcom KB 389469 says to turn Hyper-V/VBS off. The explicit "no nested virtualisation with Hyper-V" line was seen only on a third-party copy of 25H2u1 notes (UNMEASURED at Broadcom).
4. Microsoft pages confirm a memory-integrity toggle; no Microsoft page fetched says anything specific to Windows 11 HOME, and one Q&A reply claims 25H2 removed the toggle (registry edit instead).
5. Plan implication: the OVA host needs Hyper-V/VBS off; Home edition path is unproven by Microsoft documentation.

## Q1 Licence key / commercial use
- Broadcom FAQ, https://www.vmware.com/docs/desktop-hypervisor-faqs (no page date; text says "As of March 2025"):
  - "No subscription or license key is required."
  - "There's no need to select a usage type or enter a key"
  - "available at no charge for all use cases, including personal, educational, and commercial use."
  - "Customers using the free VMware Fusion and Workstation products are not entitled to support"
  - "future releases will adopt labels such as 25H2, 26H1, etc."
- Broadcom KB 368667, https://knowledge.broadcom.com/external/article/368667 (body date Nov 11, 2024; "Updated On" blank):
  - "No license key is required for the free version." (installer offers "FINISH (For free version)")
  - "available free for Commercial, Educational, and Personal users."
  - free version limited to "'Workstation Pro 17.5.2' and 'Fusion 13.5.2' and above."
- Broadcom blog 26H1, https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26H1/ (May 14, 2026):
  - "both products remain free for commercial, educational, and personal use."
- Current naming per Broadcom: 25H2 (blog dated October 14, 2025) and 26H1 (May 14, 2026). "26.0.1 / 26H1u1" itself: UNMEASURED (no page fetched names it).
- Answer: no key; free for commercial use; no Broadcom support entitlement.

## Q2 KB 368734 steps
https://knowledge.broadcom.com/external/article/368734 ("Updated On" blank; links a 25H2 blog dated 2025/10/14). Page's own numbered steps:
1. "Go to support.broadcom.com."
2. "In the upper right corner, select 'Support Portal'"
3. "Either log in by clicking 'Go To Portal' or 'Register' for a basic Broadcom account."
4. "Once logged in, go to support.broadcom.com if you're not redirected there."
5. "Click the dropdown to choose the VMware Cloud Foundation division."
6. "On the left, click 'My Downloads'."
7. "Click the hyperlink 'Free Software Downloads available HERE'"
8. "Search for 'Fusion' or 'Workstation' ... and click on 'Show Results'."
9. "Click on 'VMware Fusion' or "VMware Workstation' and select latest version to download."
Account: "You must be a registered user on the Broadcom Support Portal." "Site ID is not required for Basic users in order to download free products." Basic profiles must be approved by Internal Export Compliance; this "can take several weeks". Installation steps: the page "does not include any installation instructions". Licence-key statements: none on this page.

## Q3 Hyper-V / VBS and nested virtualisation
- Broadcom KB 389469, https://knowledge.broadcom.com/external/article/389469 (no date; Workstation Pro 15.x, 16.x, 17.x listed; 25H2/26.x NOT listed):
  - "The issue is caused by the host operating system (specifically Windows Hyper-V/VBS) or the physical hypervisor (ESXi)" reserving virtualisation features.
  - Symptom: "VMware Workstation or Fusion fails to power on a virtual machine when the "Virtualized Intel VT-x/EPT" feature is enabled."
  - "The error message VM Workstation and Device/Credential Guard are not compatible appears on Windows 10 or Windows 11 hosts."
  - Fix: "Turn off Memory Integrity", uncheck Hyper-V, Virtual Machine Platform, Windows Hypervisor Platform, Windows Sandbox; "bcdedit /set hypervisorlaunchtype off"; set EnableVirtualizationBasedSecurity to 0 under DeviceGuard; restart.
  - Log check: Monitor Mode "CPL0 is optimal. UML means the slower Hyper-V API is in use."
- Broadcom 25H2 blog, https://blogs.vmware.com/cloud-foundation/2025/10/14/vmware-workstation-fusion-25h2-embracing-calendar-versioning-and-new-features/ (October 14, 2025): "Hyper-V/WHP Detection (Workstation only)" (shows whether a VM runs in Hyper-V or WHP mode). Nested virtualisation: not mentioned.
- Third-party copy of 25H2u1 notes (NOT Broadcom; fetch blocked 403, so only a search snippet seen, not a fetched page): "When running on a Windows host with Hyper-V enabled, Workstation Pro 25H2 does not support nested virtualization." Treated as UNMEASURED at Broadcom.
- Answer: Workstation does run on Hyper-V/VBS hosts (Hyper-V/WHP mode, slower), but Broadcom's KB says VT-x/EPT guest virtualisation needs Hyper-V/VBS off. For this OVA, plan on VBS and Virtual Machine Platform OFF.

## Q4 Windows 11 Home: turning VBS / memory integrity off
- Microsoft, https://support.microsoft.com/en-us/windows/security/windows-security/device-security-in-the-windows-security-app (no date): can "turn memory integrity On or Off using the toggle button"; needs "hardware virtualization enabled in your system's UEFI or BIOS". Home: page "doesn't mention Home" for memory integrity.
- Microsoft Learn, https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity (ms.date 2026-10-21): memory integrity on Windows Security > Device security > Core isolation details; Windows RE recovery registry key `HypervisorEnforcedCodeIntegrity` Enabled = 0; "Existing explicit user or administrator settings are respected." Edition applicability: not stated.
- Microsoft Q&A, https://learn.microsoft.com/en-us/answers/questions/6009399/how-to-disable-memory-integrity-on-windows-11-home (2026-09-21; community Independent Advisor, not Microsoft staff): "Microsoft have removed the toggle switch to disable Memory integrity in 25H2 ... you need to edit the registry" (HypervisorEnforcedCodeIntegrity, Enabled 1 to 0, restart). Unofficial.
- Answer: Microsoft documents the toggle and registry key; no Microsoft page fetched states Home edition can or cannot do it.

## Every URL fetched (WebFetch, 2026-11-20)
- https://knowledge.broadcom.com/external/article/368734
- https://knowledge.broadcom.com/external/article/368667
- https://knowledge.broadcom.com/external/article/389469
- https://support.microsoft.com/en-us/topic/a255f612-2949-4373-a566-ff6f3f474613 (returned only a homepage; no usable content)
- https://learn.microsoft.com/en-us/windows/security/hardware-security/enable-virtualization-based-protection-of-code-integrity
- https://blogs.vmware.com/cloud-foundation/2025/10/14/vmware-workstation-fusion-25h2-embracing-calendar-versioning-and-new-features/
- https://www.vmware.com/docs/desktop-hypervisor-faqs
- https://blogs.vmware.com/cloud-foundation/2026/05/14/announcing-vmware-workstation-and-fusion-26H1/
- https://support.microsoft.com/en-us/windows/security/windows-security/device-security-in-the-windows-security-app
- https://learn.microsoft.com/en-us/answers/questions/6009399/how-to-disable-memory-integrity-on-windows-11-home
- https://www.neowin.net/amp/vmware-workstation-pro-25h2u1/ (403)
- https://www.neowin.net/software/vmware-workstation-pro-25h2u1/ (403)

## WHAT I COULD NOT CONFIRM
- Broadcom's own 25H2/26H1/26H1u1 release notes (techdocs) were not fetched: the nested-virtualisation-with-Hyper-V statement for current versions is UNMEASURED at Broadcom.
- KB 389469 lists only Workstation 15-17; whether it applies unchanged to 26.x is UNMEASURED.
- Any Broadcom page naming "26.0.1" / "26H1u1": UNMEASURED.
- KB 368734 and 368667 show no "Updated On" date; KB 368734 has no install steps.
- Any Microsoft page stating Windows 11 Home specifically can or cannot turn memory integrity / VBS / Virtual Machine Platform off: UNMEASURED. Whether the 26H2 toggle exists: UNMEASURED.
- Whether VBS stays active after Virtual Machine Platform is cleared (other features may keep the hypervisor): UNMEASURED from fetched pages.
- Commercial licence legal terms (EULA text) not read.
