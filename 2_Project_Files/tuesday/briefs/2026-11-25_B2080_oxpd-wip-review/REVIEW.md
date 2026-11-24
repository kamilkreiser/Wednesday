# B2080 REVIEW: every claim of WIP-REVIEW.md with its source

Clocks: `date` printed `Wed 25 Nov 2026 10:37:30 AEDT` at the start and `10:46:10 AEDT` before writing. Read-only on the NAS. Nothing was executed from WIP. The only things unpacked went into scratch: the STB guides and Manifest, the two simulator MSIs (never run), and the `.odt` content.xml.

Shorthand:
- `W/` = `/Volumes/DEV-Working/Datasec/WIP/`
- `P/` = `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/`
- `LIB/` = `P/1_Project_Definition/Source_Documents/2026-11-19_library-from-friday-nas-backup/OXPd/`
- `PO/` = `P/1_Project_Definition/Source_Documents/2026-11-20_from-product-owner/`
- `02`, `03`, `05` = `P/1_Project_Definition/Design/0x_*.md`
- `C1`, `C2`, `B4` = `P/1_Project_Definition/Analysis/<id>_*.md`
- `X/` = scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s326/b2080/`

`MEASURED` = I ran the read; `READ` = quoted from the file; `DERIVED` = my inference from the cited lines.

## Inventory and "already held"

| Claim | Source | Kind |
|---|---|---|
| 2,652 files in WIP (607 + 1,514 + 74 + 5 + 7 + 442 + 2 + 1) | `find W -maxdepth 25 -type f` into `X/inventory.tsv` (2,652 rows) | MEASURED |
| 35,223 library files compared | `find P/1_Project_Definition/Source_Documents -maxdepth 25 -type f` into `X/library_inventory.tsv` | MEASURED |
| 2,630 identical by sha256; 13 NEW by name and size; 9 same name, different content | `X/scripts/compare.py` run with `python3 -I`, output `X/compare.tsv` (counts by `cut -f1 \| uniq -c`) | MEASURED |
| OXPd2 Beta 10: 1,514 of 1,514 identical (to `PO/OXPd2-SDK-Beta-10-20260416/`) | `X/compare.tsv` | MEASURED |
| oxpd-javascript-2: 74 of 74 identical to `LIB/OXPd-JavaScript/SDK/oxpd-javascript-2.6.0` | `X/compare.tsv` | MEASURED |
| OXpd1.9 demos: 603 identical; file lists equal; `TestPDFFile.pdf` and `MoreOptions Demo Communications Model.vsd` differ | `X/compare.tsv`; `diff` of sorted file lists of `LIB/OXPd1-NET-Java/Demos/hp-ext-oxpd-demos-1.9` and `W/OXpd1.9/hp-ext-oxpd-demos-1.9` (empty) | MEASURED |
| Jedi resource kit: 439 identical, 2 labelled, 1 new (`.pfx`) | `X/compare.tsv`; `ls` of `LIB/.../DirtyUtilities/Configuration/` shows no `.pfx` | MEASURED |
| Simulator inner zip identical to the library zip member | `unzip -p LIB/OXPd1-NET-Java/Simulator/Jedi_Simulator_SDK1.zip Jedi_Simulator_SDK_New/Sdk_…zip \| shasum -a 256` = `6b7bdf99…09f1` = `shasum` of `W/Jedi_Simulator_SDK1/…/Sdk_20210603_2502226_009029_jedi-simulator-sdk.zip`; `md5 -q` = `79d1927e…` = its `.MD5` file | MEASURED |
| STB new to the project | 0 hits for `test bench\|STBInstall\|STBClient\|badge box\|ACT certification` in `X/library_inventory.tsv`; 0 files under `P/1_Project_Definition/{Design,Analysis,Registers}` for `solution test bench\|badge box` | MEASURED |
| STB integrity | `md5 -q W/STBInstall-Base-files4/STBInstall-Base-4.17.2.0_20190507.zip` = `ab8615b2…56e`, the same as the `.md5` file | MEASURED |

## Labels and encryption

| Claim | Source | Kind |
|---|---|---|
| Steve's notes and "Understanding the HP OXPd 1.9SDK.docx" are IRM-encrypted (`EncryptedPackage`, `DRMEncryptedDataSpace`, label text "Internal Use Only", `siteId` `ae7a1e46-02d7-4035-9a3f-dc6d9e172217`) | `file`: "CDFV2 Encrypted"; `X/scripts/u16grep.py` on both; `strings` siteId line | MEASURED |
| `ae7a1e46-…` is Datasec Corporate | `/Volumes/Datasec_DEV/CLAUDE.md`, hard rule 4, environment 1 | READ |
| 11 labelled files in all: the 2 above, the Jedi worksheet `.docx`, 8 PDFs | `X/compare.tsv` rows scanned for "Internal Use Only" (UTF-8 and UTF-16) = 11 | MEASURED |
| Labelled PDFs are 1-page wrappers ("This PDF file is protected…"); label set `2026-11-24T23:27:57Z`, name "Internal Use Only", method Standard | `pdftotext` of `W/Jedi_ResourceAnalysis_1.2.1/JediResourceAnalysisSDK.pdf`; its XMP `MSIP_Label_205418c5-…_SetDate/_Name/_Extended_MSFT_Method` | MEASURED |
| The library holds the unlabelled originals (same creation and modification dates; 30, 16, 13, 36 pages) | `pdfinfo` on WIP and `LIB/General/Package-Readmes/Jedi_Simulator_SDK1/…/Documentation/*.pdf` and `LIB/OXPd1-NET-Java/Tools/Jedi_ResourceAnalysis_1.2.1/JediResourceAnalysisSDK.pdf` | MEASURED |
| The `.vsd` that differs carries no label | `X/scripts/u16grep.py` returned no marker | MEASURED |
| textutil output of the encrypted docx was unreadable; quarantined, not deleted | `X/quarantine/steves_readme_notes.textutil-garbage.txt` | MEASURED |

## Item 1: OXPd 1.9

| Claim | Source | Kind |
|---|---|---|
| "Released Version 1.9", "HP Confidential", "February 9, 2026" | `W/OXpd1.9/1.9.0 Release Notes.txt:4,5,7` | READ |
| Help paths `OXPdLib-1.9.chm`, Java docs | same file `:15-17` | READ |
| FutureSmart 4.7 floor | same file `:28` | READ |
| JS 2.6 "does not support the 1.9 release" | same file `:37` | READ |
| Action Service text (replaces Callback Operation; filtering and polling; public cloud and zero trust) | same file `:38` | READ |
| Security Service text | same file `:39` | READ |
| "No known issues" | same file `:45` | READ |
| Demos 1.9 built 2024-05-01, revision `6350435c`, ships OXPdLib 1.8.4 | `W/OXpd1.9/hp-ext-oxpd-demos-1.9/Revision.txt`; `find … -iname 'OXPdLib*'` shows `OXPdLib-1.8.4.dll`; C1:48, C1:387 | MEASURED / READ |
| No OXPdLib 1.9 in WIP | the same `find` returns only 1.8.4 files and one `OXPdLib.dll` | MEASURED |
| OXPdLib 1.8.4.1 has no Action, Security or CallbackOperation proxy (12 services plus IPP) | `ls LIB/OXPd1-NET-Java/SDK/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/DotNet \| grep -i proxy`; the only name starting Action/Security/CallbackOperation is `SecurityDomainHelpers.cs` | MEASURED |
| M577 offers `OXPd:Action` and `OXPd:Security` at revision 2025/01/29, CallbackOperation at 2019/11/11 | `P/.tools/b2044/ews/m1/m07__DevMgmt_DiscoveryTree.xml.html` (6,119 bytes, saved 24 Nov 14:37), regex on service names and revisions | MEASURED (read of a saved file) |
| B2044 listed `OXPd:Action` | `P/1_Project_Definition/Briefs/2026-11-24_B2044_SEAT-X62_oxpd2-m577-first-run.md:95` | READ |
| No record ties Action/Security to 1.9 | `grep -r -l -i 'OXPd:Action\|service/action/\|OXPd:Security\|service/security/2025'` over `P/1_Project_Definition` and `P/5_Project_History` (`*.md`) = the B2044 brief only; control `OXPd:Test` = 3 files | MEASURED |
| 02 contradiction: "Mature, frozen; OXPd 1.9 "soon" since 2017, treat as absent" | `02:266` | READ |
| 03 contradiction: "OXPd 1.9: build on 1.8.4.1 … "soon to be released" in March 2026" | `03:466` | READ |
| Kam's note "but I will request whether there is anything more recent" | `03:93` | READ |
| C1 "No 1.9 SDK in the library" | `C1:515`; question `C1:530` | READ |
| 02 network row "a cloud-only server is not viable without a site relay" | `02:249` | READ |
| N-5 open | `02:1274` | READ |
| H7 current wording asks whether 1.9 exists | `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-25_B2078_hp-questions/HP-QUESTIONS.md:239-272` | READ |
| Accept-all certificate callback in Demos 1.9 | `C1:369`, `C1:546` | READ |
| Demo users' plain-text passwords | `C1:536` (`…/AuthnAuthz/AuthenticationAgent/users.xml`) | READ |

## Item 2: OXPd 2 Beta 10

| Claim | Source | Kind |
|---|---|---|
| Already analysed from this path on 2026-11-20 | `B4:4` | READ |
| Licence file has no HP terms | `B4:11` (BLUF 1), `B4:18` onward (§2) | READ |
| Build 20260416.1, release 1 June 2026, firmware 6.38.0.793 | `B4:61` | READ |
| No printer simulator in the folder | `B4:82`, `B4:123` | READ |
| 02 says "Beta 10 (1 Jun 2026)" | `02:266` | READ |
| HP dev root CA private key location | `W/OXPd2-SDK-Beta-10-20260416/tools/certificates/ExtSDKRootCA.key`; `B4:16` (BLUF 6), `B4:165` | MEASURED (name only) / READ |
| No passkey, WebAuthn, FIDO or Bluetooth text in specifications, examples, demos (json, md, txt, cs, js, html, java) | scoped `grep -r -l -i` = 0 files; control `usbAccessories` = 6 files | MEASURED |

## Item 3: OXPd JavaScript

| Claim | Source | Kind |
|---|---|---|
| Not needed by the project | `C2:11` | READ |
| Not supported on 1.9 | `W/OXpd1.9/1.9.0 Release Notes.txt:37` | READ |

## Item 4: Button Manager

| Claim | Source | Kind |
|---|---|---|
| exe = zip member | `shasum -a 256` both = `1555ed63…b313` | MEASURED |
| Version 1.1.0.0, © HP 2016, built on OXPdLib 1.7.2, zip member dated 2017-07-29 | UTF-16 version resource of `W/OXPD Button/ButtonManager.exe` (read as data, not run); `unzip -l` | MEASURED |
| Library build 2025-09-17 on OXPdLib 1.8.4 | `LIB/OXPd1-NET-Java/Tools/HP_OXPd1_ButtonManager-1.1.0/Revision.txt`, `Manifest.txt` | READ |
| Steve's note text | `W/OXPD Button/steves Readme.txt:1` | READ |
| Guide: LibreOffice, created 2025-06-12 | `.odt` `meta.xml` | READ |
| Scope "All FutureSmart versions 3 and 4"; port 7627 | `X/text/button_manager_howto.txt:9`, `:12` (from the `.odt` content.xml) | READ |
| Error codes 45.00.1C, .06, .33, .23 and causes | same file `:67-113` | READ |
| Our lab registers its own test button (first-run step 4, contracts in PR 43) | `03:79` (row 5, write lanes for steps 2 to 4) | READ |
| Partner failed on 45.00.33 / 45.00.CB | `02:419` | READ |

## Item 5: Jedi simulator

| Claim | Source | Kind |
|---|---|---|
| MSIs: `JediSimulator.msi` (HP, 2021-06-03), IRIS OCR 12.3.4 (2010) | `unzip -l` of the inner zip; `file` on the unpacked MSIs in `X/unpack_jedisim/` (not run) | MEASURED |
| "product=Cordoba" | `strings` of `JediSimulator.msi` ("Launch Jedi Simulator ^(product^=Cordoba configuration^=release)") | MEASURED |
| Simulated firmware or OXPd revision not found | regex for OXPd service revisions, FutureSmart versions in the MSI strings = 0 | MEASURED (absence in uncompressed strings only) |
| Windows 7 Enterprise x64 SP1; IE 8 only; firewall disabled; EWS at localhost:4242; RAM min 384 MB | library original `LIB/General/Package-Readmes/Jedi_Simulator_SDK1/…/Jedi_Simulator_User_Guide.pdf` as `X/text/Jedi_Simulator_User_Guide.txt:209-210, 316, 423, 629, 197` | READ |
| .NET CF 2.0/3.5, .NET 3.5.1/4.0, SQL CE 3.5, WSE 2.0 | same `:221-230` | READ |
| TLS 1.2 failure note | `C1:116` | READ |
| HP's OXPd Simulator 1.3 (Chromium panel, not device WebKit) | `C1:336-345`; `02:956` (R4) | READ |
| `GetMemCounters.exe` installed under `C:\jedi-simulator\System` | `X/text/Jedi_Memory_Use_Tool_User_Guide.txt:126-127` | READ |
| Windows PC kit item | `05:226` | READ |

## Item 6: Jedi resource kit

| Claim | Source | Kind |
|---|---|---|
| Release 1.2.0, 2 Sep 2014, HP Confidential; FW from FutureSmart 22.1; 2014 model list without the M577 | `W/Jedi_ResourceAnalysis_1.2.1/JediResourceAnalysisSDK_1.2.1_ReleaseNotes.txt:3-5, 7, 22-44, 51` | READ |
| Test service needed after each reboot | same notes item 7; `X/text/JediResourceAnalysisSDK.txt:160-162` | READ |
| "Solutions that interact with the browser using the OXPd API will allocate memory out of this quota"; high-water subtraction | `X/text/JediResourceAnalysisSDK.txt:824-831` (from the library original PDF) | READ |
| "OXPd Browser Apps: 3MB + Noise Factor + SDK Contribution"; SDK contribution 4.955 MB; total <= 8 MB example | same `:1010`, `:1042`, `:1081` | READ |
| Tool usage, admin password, `-memleak` default true | `X/text/Jedi_Memory_Use_Tool_User_Guide.txt:136-173` | READ |
| "works on CE-based devices" | same `:79` | READ |
| `GetMemCounters.exe` present in WIP | `W/Jedi_ResourceAnalysis_1.2.1/MemoryProfiler09-25-2014/DirtyUtilities/HP.Tools.Diagnostics.GetMemCounters.exe` (20,480 bytes; name only) | MEASURED |
| Profiler "dirties" the printer | `RunMemoryProfileTest.bat` (read with passwords masked); `DirtyPrint.exe`, `DirtyDigitalSend.exe`, `DirtyWebServices.exe` names | READ |
| FS5 CE-based vs Linux-based; 2-3 MB budget | `02:257`, `02:370` | READ |
| E2.5 2 MB soak gate | `03:221` | READ |
| C1 judged it not needed | `C1:418` | READ |
| C-72 limits to the first-run list; C-76 needs memory and certificate trust measured | `P/1_Project_Definition/CLARIFICATIONS.md` sections `## C-72`, `## C-76`; `03:78`, `03:104` | READ |

## Item 7: Solution Test Bench

| Claim | Source | Kind |
|---|---|---|
| Contents: 2 exe, 4 PDFs, Manifest; 2019-05-07 | `unzip -l W/STBInstall-Base-files4/STBInstall-Base-4.17.2.0_20190507.zip`; `X/unpack_stb/Manifest.txt` | MEASURED |
| SQL Express; client and server; DAT library | `X/text/STB_HP Solution Test Bench - User Guide.txt:29-31, 41` | READ |
| Plug-in SDK "may not be available" | same `:59-60` | READ |
| ACT automation from 4.12.1.0; FutureSmart supported, Oz and Pro not | `X/text/STB_Guide to Automated Tests for ACT Certification.txt:37, 47` | READ |
| Capability tables; Badge Box needs HP hardware; partner plugins needed; "Dirtying only" without plugins | same `:52-87` | READ |
| Soak gates in 03 | `03:221` (E2.5), `03:347` (WP6.3), `03:348` (WP6.4), `03:362` (1,000-tap soak) | READ |
| No HP approval step for OXPd 1.x | `03:115`; `C1:405` | READ |

## Item 8 and credentials

| Claim | Source | Kind |
|---|---|---|
| `hpservercertificate.pfx` location, 1,803 bytes, `file` says "data" | `X/inventory.tsv`; `file` | MEASURED (not opened) |
| Password elements in profiler XMLs are HP placeholders (`adminpw`, `{userpw}`) | `X/text/JediResourceAnalysisSDK.txt:191, 198, 201, 297, 322-326` | READ (no WIP value printed) |
| Files with password keywords (names only) | `find … -size -2M \| xargs grep -l -i 'password\|secret\|apikey\|api_key\|privatekey'` | MEASURED |
| Credential-class files by name | `find W -maxdepth 25 -iname '*.pfx' -o '*.key' -o '*.pem' …` = `.pfx`, `ExtSDKRootCA.key`, `.pem` (+2 UserSecrets DLLs, irrelevant) | MEASURED |

## What I did not do

- I did not run, install or open in a GUI any `.exe`, `.msi`, `.bat` or `.AppImage`.
- I did not open the `.pfx` or the `.key`.
- I did not try to remove any label or decrypt any file.
- I did not contact the printer.
- I wrote nothing to the NAS or to the OXPd project. Writes went only to this folder and to scratch `X/`.
