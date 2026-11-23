# OXPd 2 kick-off: the meeting pack (v4: only what is still open)

Datasec, Tuesday 2026-11-24, for the team kick-off this evening. For Kam to drive the meeting: Part 1 is what needs a decision, Part 2 is what we need from the Workpath team. Every answer box can be typed into in Word.

**This version holds only what is still open. 66 of pack v3's 112 numbered items are left out as answered, assigned or actioned (32 answered by your file or your taps, 31 ticketed to Steve M, 1 actioned on a card of yours, 2 sent to HP), and so are the eight HP asks (H1 to H8), which you are sending. The answers map (ANSWERS-MAP.md, section 4) lists every one of them with its reason. Counted by program.**

### Settle these tonight

1. **Q1, Q9 and Q10: pick an option.** Your words on each are shown under it; none picks one of its options.
2. **Q26 (HP's OXPdLib or our own client for older printers).** You left it for the kick-off.
3. **W2 (Universal Print counts).** Your words say where reports go, not whether the counts are for Secure printers only.
4. **W6 (the migration runbook).** You chose to take it in tonight's meeting.

### How to use this pack

- Each question is one question. Its block or row says why it matters, the options, what we recommend and what the build does meanwhile. If a question gets no answer tonight, the build keeps that default.

- Type into the box under each question (in Word, click the grey text). A short answer is enough: "b", "yes", "Steve M, by Friday".

- Ids are new in this version (v4). Each item's source line gives its id in pack v3. Items that need only you, not the team, are at the end of Part 1.

### The questions at a glance

| Theme | Items | Numbers |
|---|---|---|
| Part 1: Scope and phasing (sets the work from tomorrow) | 8 | Q1 to Q8 |
| Part 1: Hosting and deployment | 8 | Q9 to Q16 |
| Part 1: Sign-in and identity | 9 | Q17 to Q25 |
| Part 1: Licensing and HP code | 2 | Q26 to Q27 |
| Part 1: Printers and lab | 2 | Q28 to Q29 |
| Part 1: For Kam alone, after the meeting (defaults stand until then) | 12 | Q30 to Q41 |
| Part 2: Universal Print, licensing and deployment | 2 | W1 to W2 |
| Part 2: Scope, pilot and operations | 4 | W3 to W6 |
| Part 2: HP accounts and earlier work | 1 | W7 |

## Part 1: questions that need discussion or a decision

Questions for the team or for you to decide, each still open. "Meanwhile" is what the build does until the question is answered.

### Scope and phasing (sets the work from tomorrow)

**Q1. From tomorrow, beyond the no-hardware work, what printer and lab work may the build do without asking you each time?**

**Why it matters: **The no-hardware lanes continue under C-42. What needs your word is the printer work beyond the M577 first-run list (C-72), and the OXPd 2 lab work.  
**Options: **(a) The M577 first-run list (C-72) and its panel sign-in test (C-76), each step gated, and no more. (b) (a), plus any read-only work on lab printers the team lends. (c) (b), plus OXPd 2 lab work once a FutureSmart 6 printer or the simulator is here.  
**We recommend:** (c). **Meanwhile the build:** No-hardware lanes, and the M577 runs you approved.  
<sub>Source: C-42; C-60 message 7; C-68; C-71; C-72; C-76; Tuesday EXPIRING-GRANTS (its reading of C-71); pack v3 id Q1</sub>


| Answer Q1 |
|---|
| **Your words, 2026-11-24 (verbatim):** q1 - Steve M has multiple printers and a full test lab.  He will be in charge of testing. <br>**The choice left:** Your words name Steve M as in charge of testing; they pick none of (a), (b), (c). The choice left: (a), (b) or (c). <br>**Decision:** &nbsp; |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q2** | **Who runs the pilot: the build team or the Workpath team?** The pilot needs a customer site, a person at the printers and a defect threshold (Q3). Its owner sets all three. <sub>Source: QUESTIONS_BY_OWNER v2 P4-3; 03 phase 6; pack v3 id Q4</sub> | (a) The build team. (b) The Workpath team. (c) Jointly: Workpath owns the customer, the build team owns the fixes. **We recommend: (c). Meanwhile: None. Phase 6 (the pilot) is not started.** | &nbsp; |
| **Q3** | **What defect level ends the four-week pilot successfully?** Your answer A24 sets the aim ("as close to commercial ready as possible") but not a number. Phase 6 cannot exit without one. <sub>Source: 05:150 (question 14); 05:213 (N-13); C-58 paragraph 32 (A24); pack v3 id Q5</sub> | A number of open defects by severity, for example: 0 critical, 0 high, up to N medium. The Workpath team can say what it accepts for a Workpath pilot today (W26 of pack v3 (ticketed to Steve M)). **We recommend: Use the Workpath team's own pilot threshold (W26 of pack v3 (ticketed to Steve M)). Meanwhile: None set. It must be set before the pilot starts.** | &nbsp; |
| **Q4** | **Is OneDrive personal (consumer accounts) in release 1?** The code has a build variant for it, but the release pipeline does not build it and consumer sign-in is switched off. The test is your C-48 words: is it live in Workpath deployments today? <sub>Source: 05:74 (question 4); 03 section 8.3 (OQ-4); pack v3 id Q7</sub> | (a) Out: it is not a shipped product. (b) In: it is sold or wanted. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q5** | **Is HP Authentication Manager's role as the sign-in for HP Advance and LRS VPSX in release 1?** The product documents this role today. The test is your C-48 words: is it live in Workpath deployments today? "Ours only" (C-19, no other vendor's print solution) would exclude it. Whether any customer uses it is W3. <sub>Source: 05:81 (question 5); 03 section 8.3 (OQ-5); pack v3 id Q8</sub> | (a) Out. (b) In, which is new design and build work. **We recommend: (a), unless a customer you intend to sell to uses it (W3). Meanwhile: (a).** | &nbsp; |
| **Q6** | **When scanning into a SharePoint library, does each tile keep its own behaviour of today?** A library opens from two tiles: SharePoint and OneDrive's "Shared libraries". Today the SharePoint app asks for the library's fields at scan and the OneDrive app does not. <sub>Source: 05:184 (OP-19); pack v3 id Q9</sub> | (a) Yes, each matches its own Workpath app. (b) Make them the same. **We recommend: (a): each tile matches what is live today (C-48). Meanwhile: (a).** | &nbsp; |
| **Q7** | **Should the OneDrive work package be re-sized before it is scheduled?** Reading the code showed four places, not one: My Drive, Recent, Shared with me and Shared libraries. Under C-16 all four are rebuilt. The package was sized from the manual, for My Drive only. <sub>Source: QUESTIONS_BY_OWNER v2 B12; 05:22; 05:294; pack v3 id Q10</sub> | (a) Re-size now. (b) Re-size when phase 3 is planned. **We recommend: (b). Meanwhile: Unsized.** | &nbsp; |
| **Q8** | **In your brief, does "integration into intra-environments" mean "Entra environments"?** It is a one-word check on the brief of 2026-11-18. The one intranet item the other reading would add, an outbound web proxy, is designed in either way. <sub>Source: 05:155 (question 15); 03 section 8.3 (OQ-15); pack v3 id Q11</sub> | (a) Entra. (b) The customer's intranet as well. **We recommend, and meanwhile: (a).** | &nbsp; |

### Hosting and deployment

**Q9. In phase 1, what shape is "hosted through Azure"?**

**Why it matters: **Every older printer (OXPd 1.x) needs two-way traffic with the server, cannot work through address translation and uses fixed port 7627. The answer decides the network design, the packaging and test 2 (the one Azure test VM of C-78).  
**Options: **(i) A server in the client's Azure for each site, joined to that site's network. (ii) A machine at each site, deployed and governed through the client's Azure. (iii) Servers in Azure in phase 1, and the on-site server in phase 2.  
**We recommend:** Expect (i); test 2 confirms or refutes it (C-75, C-78). **Meanwhile the build:** The code stays hosting-neutral. Test 2 is written but has not been run.  
<sub>Source: 05:199 (P-4, N-5); 03 section 8.5; C-26; C-60 messages 3 to 5; C-75; C-78; pack v3 id Q12</sub>


| Answer Q9 |
|---|
| **Your words, 2026-11-24 (verbatim):** q12 - clients will deploy the solution through the Azure marketplace using services and components automatically deployed by the configuration scripts we create and submit.  During development, we will mirror this structure as closely as possible so the deployment is tested through dev.  Use the same subscription as HPSM-Poc.  Tied to kamil@datasec-rd.com <br>**The choice left:** Your words name the Azure Marketplace route. For development, your tap of 10:32 keeps the agent-controllable environment, not HPSM-POC's subscription ("b — No, keep the agent-controllable environment"). His note with it, as Tuesday relays it (the decision store's print shows the choice only): "create a new resource group under kamil@datase-rd.com. issue new steps so agents have full control to spin up and create services/ vms etc". Tuesday's reading: new steps (v3) were issued with a group oxpd2-dev-rg, and you pick the subscription in their step 3. Neither picks one of (i), (ii), (iii). The choice left: (i), (ii) or (iii). By Tuesday's reading your words point to (i) or (iii). <br>**Decision:** &nbsp; |

**Q10. Which packagings ship in release 1, now that phase 1 is hosted in Azure?**

**Why it matters: **C-17 ("Both equally") meant container, appliance and Windows, all at release. Your words "different hosting options for the client" (C-60) add an Azure route. Your note A7 ("Azure marketplace") was about how customers deploy today's Azure side, and may point the same way.  
**Options: **(a) All three, as C-17 says. (b) An Azure deployment (template or Marketplace offer) first, the others later. (c) Azure plus one on-site packaging.  
**We recommend:** (b): Azure first, since phase 1 is hosted in Azure. **Meanwhile the build:** The C-17 wording stands. Both build legs are kept and nothing Azure-specific is built.  
<sub>Source: 05:200 (P-5, N-6); 03 section 8.5; pack v3 id Q13</sub>


| Answer Q10 |
|---|
| **Your words, 2026-11-24 (verbatim):** q13 - phase 1 needs to be a fully operational build. <br>**The choice left:** Your words say phase 1 must be fully operational; they name no packaging. The choice left: (a), (b) or (c). By Tuesday's reading your q12 ("through the Azure marketplace") points to (b). <br>**Decision:** &nbsp; |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q11** | **Does the deployment tool only start and follow jobs, with the server doing the work on each printer?** The server has to keep each printer's token, records and repair loop. A desktop tool that is closed after the job cannot do that. <sub>Source: 05:166 (OP-1); 03 section 8.4; WP0.10:73; pack v3 id Q15</sub> | (a) Yes: the tool is the operator's front end and the server does the work. (b) The tool does the device steps itself. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q12** | **Does the deployment tool also install the OXPd server itself?** Neither Datasec tool has code that installs software on a machine (report D2 section 3.3). If the server is deployed into Azure (Q10), the tool may not need to. <sub>Source: 05:167 (OP-2); 03 section 8.4; pack v3 id Q16</sub> | (a) No: the server has its own packaging. (b) Yes: the tool is amended to install it. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q13** | **Is a batch of printers started from the deployment tool only, with the server console showing status and repairing one printer?** This decides whether the server console needs its own onboarding pages. <sub>Source: 05:169 (OP-4); 03 section 8.4; WP0.10:82; pack v3 id Q17</sub> | (a) Tool only. (b) The console also gets onboarding pages. **We recommend, and meanwhile: (a).** | &nbsp; |
| **Q14** | **Does the deployment-tool work (WP0.10) join the first build list now?** It was not one of the twelve no-hardware packages your word to build covered (C-42). Its design note is a draft. <sub>Source: 05:272 (WP0.10 row); WP0.10:79; 03 section 4, Phase 0; pack v3 id Q18</sub> | (a) Yes, start it now. (b) Wait until Q11 to Q13 are settled (the tool itself is chosen: your q14). **We recommend: (b). Meanwhile: Only the draft note exists. No build work has started.** | &nbsp; |
| **Q15** | **For a two-server setup in the client's Azure, which availability method do we use?** The on-site design pairs two servers behind a virtual IP. Azure has its own load-balancing services that could do this instead. <sub>Source: 02 N-7 (03 section 8.5); pack v3 id Q20</sub> | (a) The virtual-IP pair, as designed. (b) Azure's own load balancing. **We recommend: (b) if Q9 puts servers in Azure. Meanwhile: Unchanged. This is phase-5 work and has not started.** | &nbsp; |
| **Q16** | **When the server runs in the client's Azure, does Azure Key Vault become its default secret store?** Only the local encrypted store is built (pull requests 5, 11, 24). Key Vault would be a second provider. <sub>Source: 02 change log, B1817 open questions (N-8); pack v3 id Q21</sub> | (a) Yes, Key Vault by default in Azure. (b) The local store everywhere. **We recommend: (a) for Azure hosting, once Q9 is settled. Meanwhile: The local store stays the only one built.** | &nbsp; |

### Sign-in and identity

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q17** | **If Microsoft's sign-in page cannot run safely on a printer panel, what do we do instead?** You ruled that the Microsoft number step stays on the panel, as Entra sets it (C-60 message 1). The first panel test may show that users share cookies, that the page does not render, or that it needs a pop-up. Another HP partner's on-panel Microsoft sign-in failed on OXPd 1.x because of memory and certificate trust (05:196). <sub>Source: 05:210 (N-3); 03 section 8.5; C-60 message 1; C-76; pack v3 id Q23</sub> | (a) The phone-link route (M2), which needs the relay on each customer's gateway (Q23). (b) No Microsoft step on that printer generation, so card or QR sign-in only. (c) Decide when the test result is in. **We recommend: (c). The result comes to you with options. Meanwhile: The panel route only. The phone routes and the relay stay unbuilt.** | &nbsp; |
| **Q18** | **Must older (OXPd 1.x) and newer (OXPd 2) printers use the same sign-in step?** You chose to test the panel on the M577 first (C-76). That decides how the test is run, not what the target is. The older panel browser is old and small. The design's sign-in table (02 section 5.5) still offers phone methods for 1.x, against D10 and N-1 (B2019). <sub>Source: 05:196 (P-1, N-1); 03 section 8.5; C-76; pack v3 id Q24</sub> | (a) Same target on both: the Microsoft step on the panel. (b) Older printers may use a different route if their panel test fails. **We recommend: (a), and come back to this with the M577 result. Meanwhile: Same target on both. Nothing of a phone route is built for 1.x before the panel test reports.** | &nbsp; |
| **Q19** | **Does "we cannot interfere with ... the token management done by microsoft" stop the server from holding and refreshing users' tokens?** The design's server obtains, holds, refreshes and uses each user's Microsoft tokens so that scan and print can act as that user. No-MFA mode (C-7) redeems a stored token with no user present. <sub>Source: 05:198 (P-3, N-4); 03 section 8.5; C-60 message 1; C-7; pack v3 id Q25</sub> | (a) No: the server uses Microsoft's own library and the tokens Microsoft issues, encrypted, and never sent to a printer. That counts as using Microsoft's token management, not interfering with it. (b) Yes: redesign so the server keeps no user tokens. **We recommend: (a). Meanwhile: (a). Nothing new is designed.** | &nbsp; |
| **Q20** | **Is QR sign-in without MFA offered on OXPd printers?** The customer's existing sign-in gateway does not check who sends an unlock message. In No-MFA mode a QR message is a full sign-in (report A9, 05:118). This weakness is in today's gateway, not something OXPd adds. <sub>Source: 05:117 (question 10); 05:215 (N-15); 03 section 8.3; pack v3 id Q26</sub> | (a) Offer it as Workpath does, with the risk recorded. (b) Switch it off on OXPd until the gateway is fixed. Your "may change" answer (C-27) allows this. **We recommend: (b). Meanwhile: (a), as Workpath. Nothing of QR sign-in is built before phase 3.** | &nbsp; |
| **Q21** | **If the panel refuses to show Microsoft's page inside a frame, is a full-page sign-in acceptable?** Your words were "display 2 digit in iframe". Whether Microsoft's page can be framed is not measured. Test 1 tries the frame first. <sub>Source: 05:197 (P-2, N-2); 03 section 8.5; C-60 message 1; pack v3 id Q27</sub> | (a) Yes, a full page is acceptable. (b) No, it must be a frame. **We recommend: (a). Meanwhile: The panel page is written for either.** | &nbsp; |
| **Q22** | **May the server keep an encrypted copy of a newer printer's admin password?** Your tap C-24 said "Store it encrypted". The option's own text said newer printers discard it. If a newer printer loses its access token on reboot (asked of HP in H8), someone would have to re-enter the password for each printer after each reboot. <sub>Source: 05:62 (question 2); 03 section 8.3 (OQ-2); WP0.10:81; C-24; pack v3 id Q28</sub> | (a) Never stored on newer printers. (b) Stored as a per-site choice, off by default. **We recommend: Wait for the phase-0 test of what a reboot does, then (b) if tokens are lost. Meanwhile: (a).** | &nbsp; |
| **Q23** | **May each customer's gateway get one address that accepts a request without a token, for the phone-link relay?** The phone-link route needs it. Customers who deployed by script need a second update route. Since the Microsoft step went back to the panel (C-60), the relay is only needed if Q17 picks the phone route. <sub>Source: 05:177 (OP-12); 05:210 (N-3); pack v3 id Q29</sub> | (a) Yes, under "may change" (C-27), with the test the plan describes. (b) No. **We recommend: Wait for test 1 (Q17). Meanwhile: Not before test 1 reports.** | &nbsp; |
| **Q24** | **Does OXPd offer today's unattended Universal Print registration from a stored account?** Today a fleet can be registered without a person present, from a stored account (how it works today is W1). The design registers interactively. <sub>Source: 02 change log, B1817 open questions (N-12); pack v3 id Q30</sub> | (a) Interactive only. (b) Unattended as well. **We recommend: (a) for release 1. Meanwhile: (a).** | &nbsp; |
| **Q25** | **Do you approve the six design differences from Workpath in the deviation register (DEV-14 to DEV-19)?** They are not forced by the platform or by your answers. Phase 3 cannot exit until they are approved or struck. You approved DEV-22 and DEV-23 on 2026-11-23 (C-70). The six are: DEV-14, pull release matches the user exactly, not by substring; DEV-15, card emulation moves to the server admin console; DEV-16, app settings move to the server console; DEV-17, Universal Print counts are reported for all three printer types, not Secure only; DEV-18, in No-MFA mode a refreshed token is written back, only if spike S5 passes; DEV-19, error screens show the help address as text and QR. <sub>Source: DEVIATION-REGISTER_DRAFT.md:32-37 and :50; 05:87 (question 6); 03 section 8.3 (OQ-6); pack v3 id Q31</sub> | Approve all six, strike any by number (a struck row then follows Workpath exactly), or approve all but DEV-18 until its test. **We recommend: Approve all except DEV-18, which waits for its phase-0 test. Meanwhile: As designed, pending approval before phase 3 exits.** | &nbsp; |

### Licensing and HP code

**Q26. For older printers, does the shipped product use HP's own OXPdLib library or Datasec's own client?**

**Why it matters: **Your note settled the licence question: "our license / commercial agreement allows us to use HP code as part of our code" (C-74). Which client ships is still open, and C-74 leaves it as a design choice for the kick-off. Of lane A's five, this is the real kick-off choice (K-1). The client on main (pull requests 37, 41) is Datasec's own; its service files were taken from HP's OXPdLib jar (B2024 F4).  
**Options: **(a) HP's OXPdLib (.NET), shipped unchanged as the design first said. (b) Datasec's own client, the one the lab uses now.  
**We recommend:** (b): it is built, reviewed and tested, and it is the code the M577 run will prove. **Meanwhile the build:** Datasec's own client, for the lab only. The product adapter waits for this answer.  
<sub>Source: C-74; 02 change log B2019 (K-1); history.md 2026-11-23 20:47; B1996 design review 5 question 3 and amendments A9, A10, A15; 02 C3 and R16; pack v3 id Q32</sub>


| Answer Q26 |
|---|
| **Your words, 2026-11-24 (verbatim):** q32 - left for kickoff  <br>**The choice left:** You left this for the kick-off. The choice left: (a) or (b). <br>**Decision:** &nbsp; |

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q27** | **Is a Datasec-hosted licence server an allowed exception to "everything is deployed in the client's tenant"?** A6 gives two licence-server options, through Azure or through Datasec (C-58 paragraph 17). A4 puts everything in the client's tenant (paragraph 15). The Datasec-hosted option is not in the client's tenant. <sub>Source: 05:202 (P-7); C-58 paragraphs 15 and 17; pack v3 id Q33</sub> | (a) Yes, the licence server is the one exception. (b) No, it is always deployed in the client's tenant. **We recommend: (a), since the licence service is Datasec's own control point. Meanwhile: Datasec's own licence service, as designed. Nothing new is built.** | &nbsp; |

### Printers and lab

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q28** | **Which certificate authority does the lab use for the M577: our own development CA, or one you name?** HP warns that self-signed certificates are "not recommended/supported" in a printer's OXPd CA store (report B2012 section 4, relayed). The first-run step that imports a CA waits on this. <sub>Source: 03 section 0, row 5 (B2020); report B2012 section 4; pack v3 id Q37</sub> | (a) Our development CA, removed after the test. (b) A CA you name. **We recommend, and meanwhile: (a), on the M577 only.** | &nbsp; |
| **Q29** | **How do we stay current with HP firmware updates?** Your own question, with your ruling to accept unknown values (C-61): "how do we stay up to date with updates". HP controls what reaches the printer, and a new firmware can change what a printer sends. <sub>Source: C-61 (his note, recorded as not answered); pack v3 id Q38</sub> | (a) The Workpath team's existing watch on HP releases also covers OXPd (W27 of pack v3 (ticketed to Steve M) asks how they do it today). (b) The build team re-runs the lab tests on each new firmware. **We recommend: (a), with (b) for each firmware the lab printers take. Meanwhile: Unknown values are read as unknown and never count as success (C-61).** | &nbsp; |

### For Kam alone, after the meeting (defaults stand until then)

Engineering defaults and points about your own PC or files. None needs the team. K-3, K-4 and K-5 are gaps not yet built, not choices made against the design.

Smaller points in this theme: confirm the default or change it.

| Id | Question, why it matters, source | Options; what we recommend; meanwhile | Answer |
|---|---|---|---|
| **Q30** | **Is the adapter-to-core event and command interface built before more printer work, or after the M577 first run?** The device model and registry are built (pull requests 12, 25, 30). The interface through which both printer adapters talk to the core (02 section 5.4, D2) is not, and the server host references only the OXPd 2 adapter; the lab tool references the 1.x adapter. A gap not yet built (K-3). <sub>Source: 02 section 5.4 and D2; 02 change log B2019 (K-3); pack v3 id Q42</sub> | (a) Next, before the step 2-4 write lanes. (b) After the M577 first run, so both generations shape it. **We recommend: (b). Meanwhile: Not built.** | &nbsp; |
| **Q31** | **On a Linux server, what makes the secret store's key file "sealed" to the machine?** The design says "sealed" and no more (C15, D28). Built today: a key file only its owner can read, which nothing binds to the machine, and no TPM or Key Vault provider. A gap not yet built (K-4). <sub>Source: Jira OXPD2-1 comment 41450 (RP-2); 02 change log B2019 (K-4); WP1.1; pack v3 id Q43</sub> | (a) The owner-only file, as built, on an encrypted disk. (b) A key bound to the machine (TPM). (c) Azure Key Vault where the server runs in Azure (Q16). These options are this pack's, not the review's. **We recommend: (c) in Azure and (b) on site, settled with the packaging (Q10). Meanwhile: The owner-only key file.** | &nbsp; |
| **Q32** | **Which DPAPI-NG protection descriptor does a stand-alone Windows server get?** The design names a domain group for the pair only. The library call with no descriptor was refused on the hosted Windows build, so that test skips itself. <sub>Source: Jira OXPD2-1 comment 41450 (RP-3); WP1.1; WP5.1; pack v3 id Q44</sub> | (a) The machine itself. (b) A domain group. **We recommend: (a), settled in packaging (WP5.1). Meanwhile: No descriptor; the Windows test is skipped.** | &nbsp; |
| **Q33** | **Which descriptor does a two-server Windows pair get?** As the item above. <sub>Source: Jira OXPD2-1 comment 41450 (RP-3); WP1.1; WP5.1; pack v3 id Q45</sub> | (a) A domain group, as the design names. (b) Another you name. **We recommend: (a). Meanwhile: Not built.** | &nbsp; |
| **Q34** | **Is the logging filter's cost acceptable? On 230 sample events holding no secret, 108 lost at least one harmless value.** The filter strips anything that could be a secret from the logs. It also strips harmless values (223 of 1,210), which makes support harder. <sub>Source: Jira OXPD2-1 comment 41450 (RP-5); WP1.10; pack v3 id Q46</sub> | (a) Accept: privacy first. (b) Tune the filter so fewer harmless values go, with a new review. **We recommend: (a) now; tune once real printer logs exist. Meanwhile: The filter as built.** | &nbsp; |
| **Q35** | **Should the print-job stream have a ceiling on fetches, or on time, per document?** There is none. An answer that gives one byte and then fails resets the retry count, so one document can be fetched without end. <sub>Source: Jira OXPD2-1 comment 41450 (RP-7); WP4.2; BACKLOG.md owed item 40; pack v3 id Q47</sub> | (a) Yes, a ceiling. (b) No ceiling. **We recommend: (a). Meanwhile: No ceiling.** | &nbsp; |
| **Q36** | **Confirm only: Do your words "we can store them where we want" also cover HP's older-printer (OXPd 1.x) service files, now in the repository?** C-56 named HP's OXPd 2 specification files. Pull requests 37 and 43 added HP's OXPd 1.x description files on the coordinator's reading of C-56, with leave for you to correct it (owed item 86). <sub>Source: C-56; history.md 2026-11-23 20:47 (pull request 37); BACKLOG.md owed item 86; B1996 design review 5 question 5; pack v3 id Q48</sub> | (a) Yes, they stay. (b) No, they move out of the repository. **We recommend: (a). Meanwhile: (a), as the coordinator read it.** | &nbsp; |
| **Q37** | **For older printers, does the client default to WS-Addressing 1.0 (as built, from HP's service files) or to the 2004 version (as the design says)?** Two HP sources disagree: HP's prose specification says the 2004 version, HP's service files use 1.0. The built client sends 1.0 by default with a 2004 switch (pull requests 37, 40). Neither is measured (K-2). <sub>Source: 02 section 4 (K-2); 02 change log B2019; B1996 amendment A11; pack v3 id Q49</sub> | (a) Keep 1.0 as the default, and let the M577 first run decide. (b) Change the default to 2004. **We recommend: (a). Meanwhile: 1.0, with the 2004 switch.** | &nbsp; |
| **Q38** | **Should the older-printer client judge the model and firmware it reads (for example refuse below FutureSmart 4.7) before the write lanes?** The built read returns the model and firmware, but nothing judges them; the discovery tree is fetched but not interpreted. A gap not yet built (K-5). <sub>Source: 02 change log B2019 (K-5); pack v3 id Q50</sub> | (a) Yes, before the write lanes. (b) Later. **We recommend: (a). Meanwhile: Read, not judged.** | &nbsp; |
| **Q39** | **Your ruling to revisit strict reading after the printer test (C-63): does that revisit move to the first OXPd 2 printer or simulator run?** C-63 concerns OXPd 2 printer answers. The M577 is OXPd 1.x, so Monday's test cannot meet the revisit point. <sub>Source: C-63; B1996 amendment A16; BACKLOG.md owed item 92; pack v3 id Q51</sub> | (a) Yes, revisit at the first OXPd 2 run. (b) Revisit now, without traffic. **We recommend: (a). Meanwhile: Strict, as ruled.** | &nbsp; |
| **Q40** | **May Virtual Machine Platform be switched off on the Windows PC used for HP's simulators?** The older-printer simulator needs Windows with VMware. Virtual Machine Platform was ticked, and the VMware evaluation had ended (C-53). The change was asked and not answered (C-54). <sub>Source: C-49; C-52; C-53; C-54; 05:226 (kit item 2); pack v3 id Q52</sub> | (a) Yes. (b) No, use another machine. **We recommend: (a). Meanwhile: Nothing is changed on the PC.** | &nbsp; |
| **Q41** | **May VMware on that PC move from the evaluation to the free licence?** As the item above. <sub>Source: C-49; C-52; C-53; C-54; 05:226 (kit item 2); pack v3 id Q53</sub> | (a) Yes. (b) No, use another machine. **We recommend: (a). Meanwhile: Nothing is changed on the PC.** | &nbsp; |

## Part 2: information we need from the Workpath team

What only the Workpath team (Datasec's own team behind the HP Workpath apps and HPAM; C-45) can give us. Each row is a place where the design states how today's product behaves from a video, the manual or a reading of code, rather than from the product's own people, configuration or a printer. In the meeting give each row an owner and a date; the team can fill the boxes in afterwards. Format: A = an answer in words, D = a document or file, C = a configuration or sample data, T = a test account or device, S = a walkthrough session.

### Universal Print, licensing and deployment

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W1** | How does today's unattended Universal Print registration from a stored account work? | Needed for Q24. <sub>Source: 02 change log, B1817 open questions (N-12); pack v3 id W14</sub> | S or D | &nbsp; |
| **W2** | Are Universal Print job status and page counts reported for Secure printers only today, or for Direct and Standard as well? | This rests on an assumption in an analysis report. It decides whether DEV-17 (Q25) is a deviation at all. <sub>Source: 02 section 3.4; DEVIATION-REGISTER_DRAFT.md:35; pack v3 id W15</sub> | A | **Your words, 2026-11-24 (verbatim):** w15 - all reporting is done through microsoft log analytics.  Clients can use Nexus for added clarity and reports but they have choice <br>**The choice left:** Your words say where reports go. The question left: are Universal Print counts reported for Secure printers only, or for Direct and Standard as well? <br>**Decision:** &nbsp; |

### Scope, pilot and operations

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W3** | Does any customer use HPAM as the sign-in for HP Advance or LRS VPSX? | Needed for Q5. <sub>Source: 05:81; QUESTIONS_BY_OWNER v2 A3-1 to A3-3; pack v3 id W25 (split: one question per question)</sub> | A | &nbsp; |
| **W4** | If so, how many customers? | As the item above. <sub>Source: 05:81; QUESTIONS_BY_OWNER v2 A3-1 to A3-3; pack v3 id W25 (split: one question per question)</sub> | A | &nbsp; |
| **W5** | For which of the two? | As the item above. <sub>Source: 05:81; QUESTIONS_BY_OWNER v2 A3-1 to A3-3; pack v3 id W25 (split: one question per question)</sub> | A | &nbsp; |
| **W6** | Datasec's runbook for moving a customer from one sign-in solution to another (Workpath to OXPd). | The design assumes the advice today is "a format", plus removing the printer's cloud record in Command Centre. <sub>Source: 02 section 8.5; pack v3 id W29</sub> | D | **Your words, 2026-11-24 (verbatim):** w29 - needs discussion.  action on Kamil <br>**The choice left:** You said it needs discussion and chose to take it tonight. The question left: does a runbook exist, and if not, is "format, then remove the cloud record in Command Centre" what customers are told today? <br>**Decision:** &nbsp; |

### HP accounts and earlier work

| Id | What we need | Why (what it unblocks) and source | Format | Owner, date, answer |
|---|---|---|---|---|
| **W7** | Is the empty repository OXPD1 meant to receive anything? | Ignored meanwhile; new work goes to datasecau/OXPd_2. <sub>Source: 05:183 (OP-18); pack v3 id W52</sub> | A | &nbsp; |

## Appendix: sources read

- OXPd_2: CLAUDE.md; CLARIFICATIONS.md C-1 to C-78 (whole); your notes of 2026-11-20 21:04; Design 05 (lines 1 to 300), 02 and 03 (open-question sections, 8.7, change logs; their before-copies .pre-1124), WP0.8, WP0.10; Registers (deviation register, HP questions, questions v2 model: 157 questions, 26 answered, 8 in part); Review B1812 and B1817; BACKLOG.md (97 owed items, 67 open); history.md; Briefs B1788 and B1810 STATUS.

- Also: GitHub pull requests 1 to 44 and main b0b26b60 (GET); Jira OXPD2-1 (GET); Tuesday NEXT-PICKUP DELTA 1381 to 1389; gate verdict B2016; design review B1996; lane A’s B2019 contradictions K-1 to K-5 (relayed by Tuesday).

## Appendix: what this pack could not establish

- Nothing here was checked on a printer, a simulator or a tenant; how today's product behaves comes from documents, transcripts or code, which is why Part 2 exists.

- The test count (2,093, 0 failed) is relayed from Tuesday's landing read of b0b26b60; history.md stops at pull request 42 (2,054). The M577's generation is one reader's finding from HP's firmware readme (B1996), not read from the device.

- BACKLOG.md holds further engineering points "decided by nobody" (owed items 34, 40, 41, 44, 46, 49, 57, 72, 73 among them), left to the coordinator. Jira OXPD2-1 was read by GET only; RP-4 (the log scanner and a named pipe) is left to the coordinator.

- The Word file was not opened in Word or Pages (neither is installed here); it was checked by program: every part well-formed, each answer box an unlocked content control with a unique id. The PDF is a reading copy (headless Chrome), without form fields.

- Citations of 02 and 03 are by section, mapped from their before-copies (.pre-1124), since today's updates moved the lines. K-1 to K-5 follow lane A’s 02 as worded after review B2024: K-1 is a kick-off choice; K-3, K-4 and K-5 are gaps not yet built; K-2 is two HP sources that disagree, neither measured.

- The recommendations, and the TONIGHT cut (from review B2023), are proposals for Tuesday and for you, not findings of fact.

