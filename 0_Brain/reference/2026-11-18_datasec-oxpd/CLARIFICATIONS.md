# Datasec / OXPd — CLARIFICATIONS (Kam's words and rulings, numbered)

Kept here until the project has its own folder; then this file moves to that project's `1_Project_Definition/CLARIFICATIONS.md` (the Datasec standing rule, confirmed by the Tuesday seat's mail of 2026-11-18). Entries are copied by a program from the live board's own export, never retyped. Nothing is edited after it is written; a later ruling is a new entry that names the one it changes.

## C-1

Source line of the export: `2026-11-18T21:18:33.950000+11:00 | [live] view=friday     | chars=1877  | att=0`

> This is a new project.  During architecture and design, we need fable so keep latest fable running for you and the sub agents used for this task.  New project  The new project is a Datasec project where we are trying to create an OXPD, which is a different architecture design for different printers, more focused to a localized server rather than a web server deployment, and porting the existing suite of applications, namely HP Authentication Manager to facilitate logon to Entra and a company's repositories, Mailflow, which is the Outlook or Mail product, Teams, OneDrive, SharePoint, Universal Print, and I think one or two others, and creating an equivalent, or a carbon copy of these applications which currently work and are commercially deployed through the workflow apps and deploy these through OXPD. The deployment will need to facilitate OXPD 2 as well as OXPD 1, whatever the latest version is.  The following folder has a copy of all the source code for the existing WorkPath apps, a very early attempt of the OXPD migration project, as well as SDK documentation, everything else necessary for OXPD. Please start with a very thorough analyzation of this folder, and once you do, please create an architecture and a very specific plan of attack of how to migrate the existing project to the new structure, including deployment methodologies, integration into intra-environments, integration into the existing WorkPath as some clients will have a mixed fleet and the actual componentry of the solution. Create a thorough architecture document with that as well as a plan of attack and build.  After you analyze the folder completely, create a list of questions that you need clarification, put them on my fleet board. And if there are any that I cannot answer, I'll have a meeting with the team to do so.   the folder is '/Volumes/Laptop-DEV/!CODING/Datasec/OXPd'

## C-2

Source line of the export: `2026-11-18T21:18:56.501000+11:00 | [live] view=friday     | chars=56    | att=0`

> spin up as many agents as you can manage to do this work

