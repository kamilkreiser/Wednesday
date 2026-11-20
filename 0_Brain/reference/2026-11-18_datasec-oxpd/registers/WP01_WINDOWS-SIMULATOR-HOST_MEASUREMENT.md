# WP0.1 Windows simulator host: measurement (B1784)

Measured 2026-11-20 (AEDT) by a read-only researcher for Tuesday. Nothing was created or changed in Azure. ASCII.

## BLUF
1. Azure's own sizes pages say nested virtualization is Supported for Dsv5 and Dasv5; but the page on nested virtualization says apps other than Hyper-V are "not supported in Hyper-V virtual machines, and are likely to fail" (that page speaks of Hyper-V VMs; that an Azure VM is such a VM was not stated on any page I fetched, so UNMEASURED; see answer 1). No Microsoft or Broadcom page says VMware Workstation works inside an Azure VM. So VMware inside Azure is UNPROVEN and officially unsupported on the pages fetched.
2. HP's simulator forum answer (as reported, B3:351) says the simulator "cannot run inside a Hyper-V VM", which points the same way. Whether it runs on a converted Hyper-V image: UNMEASURED.
3. The HPSM subscription (a6b8fe11-...) in australiaeast has quota (DSv5 0 of 65, DASv5 4 of 65) and the sizes exist; zone 3 is restricted for these sizes, zones 1 and 2 are not.
4. Recommended size if the owner approves a trial: Standard_D8s_v5 (8 vCPU, 32 GiB, Intel), Windows licence included: AUD 1.2051/h, AUD 879.72/month always on + disk AUD 54.02 = AUD 933.74; about AUD 319.14/month if run 10 h x 22 days and deallocated otherwise.
5. The one thing to try: a short paid trial (about 4 h, about AUD 5 for compute plus AUD 1 disk): install VMware Workstation on a D8s_v5, import the OVA, see whether it boots and gets an address. That spend is the owner's to approve; it was not run.

## Azure facts read (subscription id confirmed a6b8fe11-d1b5-4293-8727-b34aba08a705, "Azure subscription 1", Enabled)
- Resource groups, all australiaeast: hpsm-poc-rg, hpsm-poc-sm-rg, NetworkWatcherRG, mpscalc-showcase-rg, hpsm-poc-uat-rg.
- One VM: vm-hpsm-sm, group HPSM-POC-SM-RG, australiaeast, Standard_D4as_v5 ("a" = AMD), OS Windows.
- Quota (az vm list-usage, australiaeast): Total Regional vCPUs 4 of 65; DASv5 family 4 of 65; DSv5 family 0 of 65; DDSv5, DADSv5, Dv5 0 of 65; Dsv6 0 of 350.
- az vm list-skus (resource-type virtualMachines, australiaeast), filtered to 4-8 vCPU and 16-32 GiB, x64: Standard_D4s_v5, D8s_v5, D4as_v5, D8as_v5, D4ds_v5, D8ds_v5, D4s_v6, D8s_v6 and others. Fields read: capabilities vCPUs, MemoryGB, HyperVGenerations (V1,V2), CpuArchitectureType (x64), PremiumIO, AcceleratedNetworkingEnabled, and restrictions. The SKU listing has NO nested-virtualization capability field (the only capability names containing "virt" are SupportedVirtualizationTypes; I found none naming nested). So which sizes can host a hypervisor: from the listing alone, UNMEASURED; from Microsoft's sizes pages, see answer 1.
- Restriction on all these D sizes: reasonCode NotAvailableForSubscription, type Zone, zone 3 only. vm-hpsm-sm runs on a restricted-size family, so zones 1 and 2 (or no zone) are the expectation; an actual allocation was not tried: UNMEASURED.

## 1. Does Microsoft document nested virtualization for the candidate sizes; VMware Workstation?
Microsoft, sizes pages (fetched 2026-11-20):
- Dsv5/Dv5 page (https://learn.microsoft.com/en-us/azure/virtual-machines/dv5-dsv5-series, redirected to .../sizes/general-purpose/dv5-series, updated_at 2026-07-27), Feature support table: "Nested Virtualization | Supported". Table lists Standard_D4_v5 4 vCPU 16 GiB and Standard_D8_v5 8 vCPU 32 GiB (the page covers Dv5 and Dsv5).
- Dasv5 page (https://learn.microsoft.com/en-us/azure/virtual-machines/dasv5-dadsv5-series, redirected to .../dasv5-series, updated_at 2026-07-27): "Nested Virtualization | Supported"; D4as_v5 4 vCPU 16 GiB, D8as_v5 8 vCPU 32 GiB.
Microsoft, nested virtualization page (https://learn.microsoft.com/en-us/virtualization/hyper-v-on-windows/user-guide/nested-virtualization, redirected to https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/nested-virtualization, ms.date 2025-06-10):
- "Virtualization applications other than Hyper-V aren't supported in Hyper-V virtual machines, and are likely to fail. Virtualization applications include any software that requires hardware virtualization extensions."
- "Non-Microsoft virtualization on Hyper-V virtualization isn't supported. Ensure your hypervisor vendor supports this scenario."
- "Using a nested Hyper-V VM in production is supported for both Azure and on-premises in the following scenarios."
VMware Workstation specifically: no Microsoft page fetched names it. A Microsoft Q&A thread (https://learn.microsoft.com/en-us/answers/questions/1073903/cant-run-vmware-on-azure-vm, community answers dated 2022-11-03, NOT official documentation) says: "You can not run VMware workstation in Azure VM (atleast as of now). The only Virtualization application that supports in an Azure Virtual Machine is Hyper-V." The asker reports Workstation on Windows Server 2016 in Azure failing with "VMware Workstation and Hyper-V are not compatible".
Broadcom KB 313547 (https://knowledge.broadcom.com/external/article/313547/support-for-running-esxi-as-a-nested-vir.html, no date shown): "Broadcom does not support running nested hypervisors within a virtual machine on VMware vSphere ESXi" ... "VMware Workstation or VMware Fusion with the exception of the following limited scenarios" (Hyper-V with Windows guests, VBS, WSL 2 and others). That page is about Workstation as the HOST of a nested hypervisor; it does not mention Azure or any cloud host. Whether Broadcom supports Workstation running inside a cloud guest: UNMEASURED.
Conclusion: nested virtualization on Dsv5/Dasv5 is documented for Hyper-V; Workstation inside Azure has no supporting page and the pages that bear on it point to "not supported".

## 2. What the simulator needs, as the reports give it
- OXPd 2 image HPExtSim_6.38.0.793.ova: "an x86-64 PC with VMware, nested virtualization available (Hyper-V off on Windows), a wired network, generous memory. One simulator per VM if distinct IP addresses are needed." (analysis/B3_oxpd2-sdk-demos-forum.md line 391). Forum row (B3:351): "give the VM more memory (20 Oct). Use a wired network: Wi-Fi adapters may not support multiple MAC addresses. Nested virtualization is required; on a Windows host Hyper-V must be disabled; the simulator cannot run inside a Hyper-V VM (21 Oct 2026). The partner got it working on a wired desktop."
- SPU on same machine: WSL 1 required "because the simulator needs nested virtualization and Hyper-V allows only one user of it" (B3:348); HP suggested a second machine.
- OXPd 1.x Simulator 1.3: Windows desktop program; "Windows, .NET Framework 4.6-4.7, IIS 7+", certificate bound with netsh to ports 7627 and 443 (C1:339-340).
- Network: "The device must reach the server over HTTPS on that port, by a name or IP address that matches the server certificate ... The server must reach the device over HTTPS. A device simulator on Wi-Fi does not work reliably" (B3:302). Each simulator VM gets its own MAC and IP (B3:351, 355).
- The word "bridged" appears in none of the three reports; bridged networking is my inference from "own MAC address / own IP", not a quoted statement: UNMEASURED as a stated requirement.
- Hypervisor version, exact CPU features beyond nested virtualization, RAM figure, disk size: UNMEASURED (the HP Simulator Guide was not obtained, B3:402).
Awkward or impossible in Azure, as far as the documents allow: (a) VMware inside a Hyper-V guest (answer 1); (b) "Hyper-V must be disabled" while an Azure guest sits on Hyper-V (reports' own conflict; not tested); (c) a real printer on a LAN: an Azure virtual network is not that LAN; reaching one needs a VPN or a device on a reachable address. No page was fetched on Azure bridging or VPN: UNMEASURED; (d) USB card readers cannot be plugged into an Azure machine; the reports describe a "simulated HID" for the first milestone (B3:408), so a physical reader is not needed for the simulator itself.

## 3. Hyper-V instead of VMware (OVA converted)?
The documents say nothing about converting the OVA. The reports quote only that "the simulator cannot run inside a Hyper-V VM" (B3:351, a forum partner's statement, ambiguous between host and guest). UNMEASURED.

## 4. Candidate sizes, australiaeast, AUD, pay-as-you-go, Windows included
Query: GET https://prices.azure.com/api/retail/prices?currencyCode=AUD&$filter=serviceName eq 'Virtual Machines' and armRegionName eq 'australiaeast' and armSkuName eq '<size>' and priceType eq 'Consumption'  (fetched 2026-11-20 16:36 AEDT). Rows read: productName "... Series Windows", unit 1 Hour.
| Size | vCPU/GiB | Meter (meterId) | AUD/hour | AUD/month, 730 h | AUD/month, 220 h* |
| D4s_v5 (Intel) | 4/16 | D4s v5 Windows (365540ec-4a2d-5bd0-9e54-ba0651a33a86) | 0.6026 | 439.90 | 132.57 |
| D8s_v5 (Intel) | 8/32 | D8s v5 Windows (5f4a383c-0cf3-54ea-90a9-094a71df9cd9) | 1.2051 | 879.72 | 265.12 |
| D8as_v5 (AMD) | 8/32 | D8as v5 Windows (918b0017-4efd-5f30-b5ef-a9de21e21f51) | 1.1369 | 829.94 | 250.12 |
| D4as_v5 (AMD; same as vm-hpsm-sm) | 4/16 | D4as v5 Windows (69aa5ab3-77d8-5cf1-b8e3-2fb7b19fc850) | 0.5685 | 414.99 | 125.07 |
Disk (Storage service, same API, AUD per month): Premium SSD P10 (128 GiB) 28.0111; P15 (256 GiB) 54.0214; P20 (512 GiB) 104.0574; Standard SSD E15 37.1094; transaction charges are small (E15 0.0028 per 10K). A deallocated machine still pays its disk.
*Assumption: 10 h a day x 22 working days = 220 h, deallocated otherwise (compute not billed when deallocated: UNMEASURED here, no Microsoft page fetched on this; it is the usual understanding, not a quoted fact). Disk always billed.
With a P15 disk: D4s_v5 493.92 always on / 186.59 part-time; D8s_v5 933.74 / 319.14; D8as_v5 883.96 / 304.14; D4as_v5 469.01 / 179.09. Not included: public IP, network, backup, bandwidth, and whether a Windows 11 client image carries the licence at this price (the rows are Windows Server licence): UNMEASURED. Disk size needed for the OVA and the OXPd 1.x simulator: UNMEASURED (P15 256 GiB is my assumption).
Zone note: sizes restricted in zone 3 only. Quota allows 8 vCPU on DSv5 (0 of 65) and on DASv5 (4 of 65).

## 5. The owner's alternatives, from the documents only
- His old Windows PC (C-35: "I am looking for a reader and will connect my old windows PC to see if its suitable"): must be x86-64 Windows on a wired network with VMware, nested virtualization (VT-x or equivalent) available, Hyper-V off, generous memory (B3:391; Plan phase 0 line 36); for the OXPd 1.x simulator also .NET Framework 4.6 or later and IIS (C1:340). Minimum RAM, disk and CPU generation: UNMEASURED. It is the route the reports actually describe: "The partner got it working on a wired desktop" (B3:351).
- A Windows emulator on the Mac (C-35: "I can also run a windows emulator on your machine"): the reports say the Mac cannot host the simulators. Quote (B3:403): "This workstation is a Mac. The SPU ships no macOS build, and the simulator is an x86 Linux VM needing nested virtualization (the simulator log path contains linux-x86_32 ...). On an Apple-silicon Mac neither is expected to work (inferred, not tested). An x86-64 Windows or Linux PC is needed." The reason is x86 guest plus nested virtualization on a non-x86 host; it is marked inferred, not tested. Which Mac chip he means: UNMEASURED.

## 6. Recommendation
- Do not create anything yet; the documents give no support for VMware Workstation inside Azure, and the old Windows PC is the route the forum reports show working.
- If the owner wants Azure anyway: Standard_D8s_v5, Windows, P15 256 GiB, zone 1 or 2, deallocated outside work hours: about AUD 319 a month (AUD 934 always on).
- The ONE trial: create that D8s_v5 for about 4 hours, install VMware Workstation, import HPExtSim_6.38.0.793.ova, and see whether it boots and reports an IP address. Cost about AUD 4.82 compute + about AUD 1 disk, then delete. Needs the owner's approval first; also needs the OVA, not yet downloaded.

## Commands run (all read verbs; AZURE_CONFIG_DIR = HPSM-POC settings folder)
| Time (AEDT, 2026-11-20) | Command | Returned |
| 16:34:13 | az account show --query id,name,state | id a6b8fe11-d1b5-4293-8727-b34aba08a705, Azure subscription 1, Enabled |
| 16:34:22 | az group list | 5 groups, all australiaeast |
| 16:34:23 | az vm list | one VM vm-hpsm-sm D4as_v5 Windows |
| 16:34:25 | az vm list-usage --location australiaeast | quota rows above |
| 16:34:30 to 16:35:22 | az vm list-skus --location australiaeast --resource-type virtualMachines | 3.2 MB json; filtered offline |
| 16:36:08 | curl prices.azure.com retail prices (no sign-in), 4 VM sizes + disks, AUD | prices above |

## URLs fetched
- https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/dv5-series (via dv5-dsv5-series)
- https://learn.microsoft.com/en-us/azure/virtual-machines/sizes/general-purpose/dasv5-series (via dasv5-dadsv5-series)
- https://learn.microsoft.com/en-us/windows-server/virtualization/hyper-v/nested-virtualization (via the virtualization/... URL)
- https://learn.microsoft.com/en-us/answers/questions/1073903/cant-run-vmware-on-azure-vm (community thread)
- https://knowledge.broadcom.com/external/article/313547/support-for-running-esxi-as-a-nested-vir.html
- https://prices.azure.com/api/retail/prices (queries above)
- https://learn.microsoft.com/en-us/azure/virtual-machines/nested-virtualization: 404, nothing read. https://learn.microsoft.com/en-us/azure/virtual-machines/acu returned an unrelated resize page, not used. Two web searches were run; their summaries were not relied on.

## WHAT I DID NOT MEASURE
- Whether VMware Workstation or the OVA runs in any Azure VM (no trial run; costs money).
- Any Microsoft statement naming VMware Workstation on Azure; any Broadcom statement about cloud guests.
- Whether the SKU listing marks nested virtualization (it has no such field); allocation success in zone 1, 2 or none.
- Simulator RAM, disk, CPU, hypervisor version (HP guide not obtained); whether "bridged" networking is required.
- OVA conversion to Hyper-V; Azure to LAN printer connectivity (VPN); USB readers.
- Windows 11 licence terms on Azure; billing when deallocated (no page fetched); disk size; extra charges.
- The old PC's specs and the Mac's chip.
