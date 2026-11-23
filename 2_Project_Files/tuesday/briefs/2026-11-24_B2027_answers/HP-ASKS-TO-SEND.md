# HP asks to send (H1 to H8), ready to paste into HP's portal

For Kam, 2026-11-24. Your tap of 10:33 on the card about sending the HP asks: "a — Send with the three edits". Each block below is one message. Paste it as it stands into HP's developer portal (or send it through your escalation contact). Fill in the square brackets first; only you can. Nothing here has been sent. Your tap of 10:35 (on chasing HP for the OXPd 2 tools): "a — I'll send H5 and H3 now | note: email me text". So H5 and H3 come first. Every block is self-contained: a subject line, then the body, so each can be emailed on its own.

What changed from the drafts, as you ruled:
- **H2** item 1 is cut down to whether your existing App Center enrolment covers OXPd 2.
- **H6** keeps only the beta confidentiality question. The licence points are struck, because your own ruling of 23 November settles using HP code in our code.
- **H7** now asks for any OXPd 1.x SDK newer than 1.8.4.1, as your 10:26 note asked: "but I will request whether there is anything more recent".

Two small fixes so that every message is true today, marked for your check:
- H4 no longer says we have the simulator. We do not have it yet; H5 asks for it.
- H5 drops the optional line about our own printer. Our own printer is an OXPd 1.x printer.

The sign-off on each block is yours, "Kamil Kreiser, CTO, Datasec". Change it if you prefer.

---

### H5. OXPd 2 developer access

```
Subject: Datasec: OXPd 2 developer access (debug bridge key, simulator, simulator guide, pilot firmware)

Hello,

We are setting up our OXPd 2 lab and are missing four things. Could you help
us get them, or tell us whom to ask?

1. LaserJet Debug Bridge service key. We understand it is requested from the
   developer portal and tied to a developer account. Is our account
   [your HP developer account e-mail] enabled for it, and is one key enough
   for a small team or does each developer need their own?
2. The OXPd 2 simulator image for the current beta (the file we expect is
   HPExtSim_6.38.0.793.ova). Is that still the current image, and where do we
   download it?
3. The HP Extensibility Simulator Guide. The download was refused for our
   account (HTTP 403). Could access be granted, or the document be sent?
   The portal also has a section marked limited access that our account
   cannot open: what is in it, and do we need it for a solution that does
   sign-in, scanning and printing?
4. FutureSmart 6 pilot firmware at or above 6.38.0.793 for a physical printer.
   How does a partner obtain it, for which models, and under what conditions?

We understand that switching developer mode on or off removes every solution
from the printer, and that it needs someone at the control panel and outbound
internet access from the printer to HP. If there is anything else we should
know before we do it to a printer, please say.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H3. OXPd 2 production dates

```
Subject: Datasec: OXPd 2 production dates (firmware, platform version, signing)

Hello,

We are planning the release of an OXPd 2 solution and need to know what we
can tell our customers about timing. As far as we can see from the developer
portal, four things have to be in place before an OXPd 2 solution can be
installed on a customer's printer, and we have not found a date for any of
them. Could you give us HP's current dates, or best estimates, in writing?

1. Production FutureSmart 6 firmware that customers may run with OXPd 2
   solutions. (The firmware we can see is marked as beta, for internal testing
   only and not for distribution to customers.)
2. An OXPd 2 platform version that HP validation accepts. (The platform
   versions table on the portal lists every version as pre-release and "Not
   Supported" for validation, and does not yet list Beta 10.)
3. A signing service whose signed bundle installs on a printer that is not in
   developer mode. (A thread on the developer forum in November 2026 describes
   a bundle signed through the App Center that the Beta 10 firmware and the
   simulator still rejected. Has that been resolved?)
4. HP's turnaround for validation and signing once a bundle is submitted, for
   a first submission and for a later update.

Two related questions:

5. When will the list of printer models that support OXPd 2 be published?
6. Is there a date for a production (non-beta) OXPd 2 SDK?

If a date is not known, the dependency would help us as much: what has to
happen first, and who decides.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H1. Written confirmation of our approach

```
Subject: Datasec: written confirmation of our OXPd approach (server-side Microsoft 365 integration)

Hello,

Datasec is building an OXPd version of our HP Authentication Manager suite
(sign-in with Microsoft Entra, plus our Mailflow, Teams, OneDrive, SharePoint
and Universal Print applications). It is a server on the customer's own
network. The printer never talks to Microsoft: our server does, and the panel
only shows pages our server serves.

[When and how HP told us: for example "When we spoke on <date>" or "In your
e-mail of <date>"], my understanding was that HP is comfortable with this
approach for OXPd. Could you confirm that in writing? Specifically:

1. Is an OXPd solution whose server calls Microsoft 365 (Entra sign-in,
   Microsoft Graph, Universal Print) acceptable to HP on OXPd 2 and on
   OXPd 1.x?
2. Is such a solution eligible for HP validation and signing on OXPd 2, on the
   same terms as any other OXPd 2 solution?
3. We are aware of a 2023 statement on the developer forum that OXPd does not
   support direct integration with public cloud services and that Workpath is
   the route for that. Is our reading correct that this concerned the printer
   connecting to the cloud service itself, and does not apply to a design
   where only the solution's server does?

A short reply by e-mail is all we need. We would like to keep it on file and
refer to it when we submit for validation.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H2. App Center enrolment for OXPd 2, and a contact for validation and signing

```
Subject: Datasec: HP App Center for OXPd 2, and a contact for OXPd 2 validation and signing

Hello,

Datasec intends to submit an OXPd 2 solution for HP validation and signing.
Before we do, could you help us with the following?

1. Datasec is already enrolled in HP App Center. Does our enrolment cover
   OXPd 2 solutions, or is something more needed for OXPd 2? If more is
   needed, what are the steps and how long do they usually take?
2. Who is our contact at HP for validation and signing questions, and what is
   the right channel for them (the developer forum, a support ticket, or a
   named person)?
3. What is the submission route today: what we upload, what HP checks, and
   what comes back to us?
4. What does HP want to see with a submission besides the bundle itself (for
   example a user guide, a statement of the data the solution handles, the
   list of printers we tested on)?
5. Is there anything Datasec has to sign or accept before a first submission
   (an agreement, programme terms, a fee)?

We would like to start this early, in parallel with development, so that the
process is not new to us on the day the solution is ready.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H4. A first validation round with fewer than seven tested printer groups

```
Subject: Datasec: first OXPd 2 validation round with fewer than seven tested printer groups

Hello,

HP's publishing guidance for OXPd 2 asks for a solution to be tested on at
least one printer from each of five multifunction groups (A to E), and, for a
solution that handles sign-in, also on one from each of two printer groups
(F and G), on the latest firmware at the time of submission.

Our solution handles sign-in, so that is seven groups. Today we do not yet
have a FutureSmart 6 printer or the simulator in our lab
[adjust if this has changed]. We will not declare a group as tested when it
was not.

1. Can a first validation and signing round go ahead with fewer than the
   seven groups tested, for example for a pilot limited to the models we did
   test, with the remaining groups added in a later round?
2. If all seven are required for any signing at all, can HP help with access
   to printers from the groups we lack (loan units, a partner lab, remote
   access)?
3. Does a test on the simulator count for any group?
4. Does "latest firmware at the time of submission" mean pilot firmware today?

We would like to submit early so that problems in the process show up while
there is still time to fix them.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H6. OXPd 2 beta confidentiality

```
Subject: Datasec: OXPd 2 beta confidentiality

Hello,

We are building an OXPd 2 solution on the Beta 10 SDK and will start talking
to customers about it. Are there confidentiality terms for the beta that limit
what we may tell our customers about OXPd 2 before its production release?
If so, where can we read them?

A pointer to the documents is enough if this is already written down.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H7. OXPd 1.x: anything newer than 1.8.4.1

```
Subject: Datasec: OXPd 1.x SDK newer than 1.8.4.1, and OXPd 1.9 availability

Hello,

We are building on the OXPd 1.8.4.1 SDK for FutureSmart 4.7 to 5 printers.
An HP reply on the developer forum in March 2026 mentioned a "soon to be
released OXPd 1.9".

1. Is there any OXPd 1.x SDK newer than 1.8.4.1, released or in preview? If
   so, could we have it, or how do we get it?
2. Is OXPd 1.9 available to partners, as a release or a preview? If so, how
   do we get it?
3. If it is not out yet, is there a date, and what does it change for a
   solution that does sign-in with card readers, scanning and printing?
4. Would 1.9 change the lowest firmware a printer needs, or the rule that an
   OXPd 1.x solution needs no HP approval before it is deployed?
5. Is there a stated support period for OXPd 1.x on FutureSmart 4 and 5?

If nothing newer is available, we carry on with 1.8.4.1.

Thank you,
Kamil Kreiser
CTO, Datasec
```

### H8. Six OXPd 2 behaviour questions

```
Subject: Datasec: six OXPd 2 behaviour questions (Beta 10)

Hello,

While designing against the Beta 10 SDK we found six points where the guides
are silent or disagree with each other. We will test each on a printer, but a
word from engineering would save time and tell us what is intended.

1. Tokens after a reboot. Does the solution's token (and its refresh token)
   survive a printer reboot, a power loss and a firmware update? If it can be
   lost, can the solution request a new install code with its own token, or
   does that always need the printer administrator's credentials?
2. Upgrading an installed solution. If we install a bundle with the same
   solution id over an installed one, is it replaced in place, refused, or
   something else? Is uninstall then install the intended upgrade route?
3. Printing while the user is at the panel. The IPP extensions guide says
   that submitting a job to a printer in priority print mode is currently not
   supported, by value and by reference; the pull print demo appears to do
   it. Which is right on current firmware?
4. Browser session data between users. When one walk-up user signs out and
   the next signs in, are cookies and cached data of the embedded browser
   cleared? Is that guaranteed, or still under development?
5. Certificate trust in the embedded browser. For pages on third-party sites
   listed as trusted sites, does the browser use the solution's own
   certificate authority store only, or also a public root store?
6. Card reader registration record. The Beta 10 release note deprecates one
   USB accessories record type in favour of another, while the guide says the
   newer one is not supported. Which one should a Beta 10 bundle carry?

Thank you,
Kamil Kreiser
CTO, Datasec
```
