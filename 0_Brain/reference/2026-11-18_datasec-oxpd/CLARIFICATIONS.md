# Datasec / OXPd — CLARIFICATIONS (Kam's words and rulings, numbered)

Kept here until the project has its own folder; then this file moves to that project's `1_Project_Definition/CLARIFICATIONS.md` (the Datasec standing rule, confirmed by the Tuesday seat's mail of 2026-11-18). Entries are copied by a program from the live board's own export, never retyped. Nothing is edited after it is written; a later ruling is a new entry that names the one it changes.

## C-1

Source line of the export: `2026-11-18T21:18:33.950000+11:00 | [live] view=friday     | chars=1877  | att=0`

> This is a new project.  During architecture and design, we need fable so keep latest fable running for you and the sub agents used for this task.  New project  The new project is a Datasec project where we are trying to create an OXPD, which is a different architecture design for different printers, more focused to a localized server rather than a web server deployment, and porting the existing suite of applications, namely HP Authentication Manager to facilitate logon to Entra and a company's repositories, Mailflow, which is the Outlook or Mail product, Teams, OneDrive, SharePoint, Universal Print, and I think one or two others, and creating an equivalent, or a carbon copy of these applications which currently work and are commercially deployed through the workflow apps and deploy these through OXPD. The deployment will need to facilitate OXPD 2 as well as OXPD 1, whatever the latest version is.  The following folder has a copy of all the source code for the existing WorkPath apps, a very early attempt of the OXPD migration project, as well as SDK documentation, everything else necessary for OXPD. Please start with a very thorough analyzation of this folder, and once you do, please create an architecture and a very specific plan of attack of how to migrate the existing project to the new structure, including deployment methodologies, integration into intra-environments, integration into the existing WorkPath as some clients will have a mixed fleet and the actual componentry of the solution. Create a thorough architecture document with that as well as a plan of attack and build.  After you analyze the folder completely, create a list of questions that you need clarification, put them on my fleet board. And if there are any that I cannot answer, I'll have a meeting with the team to do so.   the folder is '/Volumes/Laptop-DEV/!CODING/Datasec/OXPd'

## C-2

Source line of the export: `2026-11-18T21:18:56.501000+11:00 | [live] view=friday     | chars=56    | att=0`

> spin up as many agents as you can manage to do this work

## C-3

Source line of the export: `2026-11-18T21:37:59.071000+11:00 | [live] view=friday`

> keys will be old and rotated so don't worrry

Context: Friday's panel message of the same evening reporting that the licence service source holds files its readme calls the root licence-signing private key and the API private key, and that other repositories hold a client secret, a hardcoded card key and a release keystore (locations only, from the analysis reports). Friday's reading: no rotation action is asked; the keys found in the library are not live. The architecture still states that the new server keeps no secret in source.

## C-4

Kam, Friday's terminal, about 21:36: "fable limit hit.  if fable does not work.  use opus" (typed in the terminal, recorded from the session, not from a board export). Friday's reading: agents for this project run on the newest Fable while it answers and on Opus when it does not.

## C-5

Kam, Friday's terminal, 2026-11-18 evening: "no problem.  use opus now and we will run a fable run to review" (typed in the terminal, recorded from the session). Friday's reading: the remaining analysis, the synthesis (architecture document, plan of attack and build) and the question list are produced on Opus now; once Fable answers again (its limit resets 2026-11-20 09:00 AEDT) a Fable review pass reads the documents and reports corrections before they are final. This narrows C-1's "keep latest fable running" for this stage only.


## C-6

Live board, view=friday, card datasec-oxpd-q25-test-devices-1118, his tap verbatim from the board export:

> 03:29 [live] | Decision datasec-oxpd-q25-test-devices-1118: a — As assumed

## C-7

Live board, view=friday, card datasec-oxpd-q24-no-mfa-token-storage-1118, his tap verbatim from the board export:

> 03:29 [live] | Decision datasec-oxpd-q24-no-mfa-token-storage-1118: a — As is, off by default

## C-8

Live board, view=friday, card datasec-oxpd-q23-admin-view-location-1118, his tap verbatim from the board export:

> 03:30 [live] | Decision datasec-oxpd-q23-admin-view-location-1118: a — Licence portal plus consoles

## C-9

Live board, view=friday, card datasec-oxpd-q22-tls-certificate-1118, his tap verbatim from the board export:

> 03:30 [live] | Decision datasec-oxpd-q22-tls-certificate-1118: a — Customer internal authority

## C-10

Live board, view=friday, card datasec-oxpd-q21-job-audit-supplies-1118, his tap verbatim from the board export:

> 03:30 [live] | Decision datasec-oxpd-q21-job-audit-supplies-1118: a — Best effort, no 1.x supplies

## C-11

Live board, view=friday, card datasec-oxpd-q20-hp-code-rights-1118, his tap verbatim from the board export:

> 03:30 [live] | Decision datasec-oxpd-q20-hp-code-rights-1118: a — As assumed

## C-12

Live board, view=friday, card datasec-oxpd-q19-workpath-deploy-today-1118, his tap verbatim from the board export:

> 03:30 [live] | Decision datasec-oxpd-q19-workpath-deploy-today-1118: a — Yes, as assumed

## C-13

Live board, view=friday, card datasec-oxpd-q18-pull-sharing-ipps-1118, his tap verbatim from the board export:

> 03:30 [live] | Decision datasec-oxpd-q18-pull-sharing-ipps-1118: a — Yes, as assumed

## C-14

Live board, view=friday, card datasec-oxpd-q17-universal-print-model-1118, his tap verbatim from the board export:

> 03:30 [live] | Decision datasec-oxpd-q17-universal-print-model-1118: a — As assumed

## C-15

Live board, view=friday, card datasec-oxpd-q16-scan-print-behaviour-1118, his tap verbatim from the board export:

> 03:30 [live] | Decision datasec-oxpd-q16-scan-print-behaviour-1118: a — As assumed

## C-16

Live board, view=friday, card datasec-oxpd-q15-release-one-scope-1118, his tap verbatim from the board export:

> 03:31 [live] | Decision datasec-oxpd-q15-release-one-scope-1118: b — Full match of everything

## C-17

Live board, view=friday, card datasec-oxpd-q14-server-packaging-1118, his tap verbatim from the board export:

> 03:31 [live] | Decision datasec-oxpd-q14-server-packaging-1118: c — Both equally

## C-18

Live board, view=friday, card datasec-oxpd-q13-legacy-keycloak-1118, his tap verbatim from the board export:

> 03:31 [live] | Decision datasec-oxpd-q13-legacy-keycloak-1118: a — No, none are

## C-19

Live board, view=friday, card datasec-oxpd-q12-other-vendor-coexist-1118, his tap verbatim from the board export:

> 03:32 [live] | Decision datasec-oxpd-q12-other-vendor-coexist-1118: b — No, ours only

## C-20

Live board, view=friday, card datasec-oxpd-q11-licensing-model-1118, his tap verbatim from the board export:

> 03:32 [live] | Decision datasec-oxpd-q11-licensing-model-1118: a — Same seat, any platform

## C-21

Live board, view=friday, card datasec-oxpd-q10-site-size-1118, his tap verbatim from the board export:

> 03:32 [live] | Decision datasec-oxpd-q10-site-size-1118: a — Yes, as assumed

## C-22

Live board, view=friday, card datasec-oxpd-q09-printer-generations-1118, his tap verbatim from the board export:

> 03:32 [live] | Decision datasec-oxpd-q09-printer-generations-1118: a — FutureSmart 4.7 and up only

## C-23

Live board, view=friday, card datasec-oxpd-q08-card-reader-models-1118, his tap verbatim from the board export:

> 03:32 [live] | Decision datasec-oxpd-q08-card-reader-models-1118: a — The six existing readers

## C-24

Live board, view=friday, card datasec-oxpd-q07-store-device-admin-pw-1118, his tap verbatim from the board export:

> 03:32 [live] | Decision datasec-oxpd-q07-store-device-admin-pw-1118: a — Store it encrypted

## C-25

Live board, view=friday, card datasec-oxpd-q06-reuse-entra-registration-1118, his tap verbatim from the board export:

> 03:32 [live] | Decision datasec-oxpd-q06-reuse-entra-registration-1118: a — Reuse the existing one

## C-26

Live board, view=friday, card datasec-oxpd-q05-server-location-1118, his tap verbatim from the board export:

> 03:33 [live] | Decision datasec-oxpd-q05-server-location-1118: a — On each site's network

## C-27

Live board, view=friday, card datasec-oxpd-q04-azure-backend-frozen-1118, his tap verbatim from the board export:

> 03:33 [live] | Decision datasec-oxpd-q04-azure-backend-frozen-1118: c — May change

## C-28

Live board, view=friday, card datasec-oxpd-q03-card-interop-1118, his tap verbatim from the board export:

> 03:33 [live] | Decision datasec-oxpd-q03-card-interop-1118: a — Full sharing

## C-29

Live board, view=friday, card datasec-oxpd-q02-phone-signin-step-1118, his tap verbatim from the board export:

> 03:33 [live] | Decision datasec-oxpd-q02-phone-signin-step-1118: a — Phone code or phone link

## C-30

Live board, view=friday, card datasec-oxpd-q01-hp-confirm-m365-1118, his tap verbatim from the board export:

> 03:34 [live] | Decision datasec-oxpd-q01-hp-confirm-m365-1118: a — Yes, HP confirmed

## C-31

Tuesday terminal, 2026-11-20 (after his /login), the instruction that moved the project to the Fable review, verbatim:

> please use fable to review the oxpd project, architecture and plan of attack.  continue where friday left off and let me know when you are ready to build

## C-32

Live board, view=tuesday, card datasec-oxpd-thirteen-defaults-1120, his tap verbatim (kam_msgs, live):

> 2026-11-20T09:38:43.436000+11:00 [live] | Decision datasec-oxpd-thirteen-defaults-1120: a — Accept the defaults for now

The option's detail, word for word from the card: "The design proceeds on each default; I bring each question back before the phase it blocks." The thirteen are questions 1 to 6 and 9 to 15 of `05_readiness-to-build.md` (OQ-1 to OQ-6 and OQ-9 to OQ-15 in the documents). Each stays an OPEN question on its default: this answer accepts the defaults for now and rules none of them.

## C-33

Live board, view=tuesday, 2026-11-20T10:22:20.717000+11:00, with six attachments (CypherSharePoint-main.zip twice, CypherSharePoint-main_2.zip, CommonValueLibraryCypher-master-2.zip, two PDF prints of the organisation's repository list), his words verbatim (kam_msgs, live):

> here are the Sharepoint repo.  and a screenshot of the orgs repositories.  I was not sure what you meant by gateway

This answers the SharePoint half of the card datasec-oxpd-sharepoint-source-1120 (OQ-7): the source is supplied. The gateway half is not answered: he asks what was meant. The files are kept outside git under `2_Project_Files/fleet/state/kam_attachments_1120/` (the archives hold a keystore file: location only, never opened).

## C-34

Live board, view=tuesday, 2026-11-20T10:22:30.516000+11:00, his words verbatim (kam_msgs, live):

> I have a printer that can run oxpd

Which model, firmware and OXPd generation (1.x or 2) it is has not been said: asked, not assumed.

## C-35

Live board, view=tuesday, 2026-11-20T10:23:04.108000+11:00, his words verbatim (kam_msgs, live):

> I am looking for a reader and will connect my old windows PC to see if its suitable.  I can also run a windows emulator on your machine
