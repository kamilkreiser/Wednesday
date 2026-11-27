# B2158 COMMISSION (one in-session agent, Opus per OXPd CLAUDE.md line 7) -- Datasec/OXPd: a modern screen design for every OXPd app screen, for Kam's approval

Kam's words (Tuesday terminal, 2026-11-27, verbatim, relayed in s333's pickup OXPd block):
"with regards to the look and feel of the current apps, can you get an agent to design each screen using a similar style to the playbook for approval.  The functionality of the existing apps is right but they look dated.  Once the design is there, email me a PDF so I can approve or amend"

Commissioned by Tuesday (s334). Tuesday sends the email; you never send mail.

## Rules
- READ-ONLY everywhere except your outputs under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-27_B2158_screen-designs/` (create it) and scratch under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s334/d2158/`.
- No write in the OXPd project folder, Jira, GitHub, cards or mail. Never read `Source_Documents/` contents that are credentials, `4_Credentials/` or key folders. Never type `cd`; never delete (move to a dated `_quarantine` folder in your own output folder if you must).
- This is NOT HPSM-POC work: the HP Security Services playbook is only the STYLE reference. Nothing here is sent to HP or any human by you.
- Every clock you write is printed by `date`.

## Inputs (read, in this order)
1. Style reference (the playbook look): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1109/f-84472617d43a_HP_Cyber_Security_Services_Playbook_v2_1_Layout_Alignment.html` and `f-1c6fabb2c95c_HP_Security_Services_Playbook_v2_0_Aligned_Partner_Demo.html` (same folder). Extract the visual system: palette (hex values), type scale and families, spacing, corner radii, shadows, buttons, cards, chips, headers, icons. Write it as `STYLE.md` in your output folder with each token traced to the CSS line it came from.
2. What the apps must DO (functionality unchanged): `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/CLAUDE.md`, then `1_Project_Definition/Design/02_architecture.md` and `03_plan-of-attack-and-build.md` (the per-app feature lists, F-numbers, panel constraints: the panel row in 02 section 4 gives the M577 panel size, browser and page-weight limits), `1_Project_Definition/Analysis/` (the analysis of the existing Workpath apps: find the screen inventories and any screenshots or screen descriptions the project holds; list what you used), and `CLARIFICATIONS.md` (search it for screen, panel, button, home screen, look, UI).
3. The apps in scope: the sign-in hub (card and Microsoft sign-in), OneDrive, SharePoint, Teams, Mailflow, Universal Print. For each, enumerate EVERY screen the existing app has (from the analysis), with its source line. If a screen's existence is only inferred, mark it inferred.

## Output
- One HTML mock per screen, sized to the M577 panel's measured resolution (from 02; if 02 does not give pixels, find it in the analysis or HP's M577 documentation in the project, cite it, and if still unknown use 800x480 and say UNMEASURED on the cover page). Respect the panel's limits from 02 (touch targets, no heavy fonts or scripts the panel browser cannot run) and say on each page which constraint shaped it.
- Each screen keeps the existing app's functions, fields and actions (listed beside the mock as "Functions kept: ..." with the analysis line), restyled in the playbook's system. Use generic product names only (OneDrive, SharePoint, Teams, Outlook mail, Universal Print); no HP logos, no Workpath branding, no client names, no real user data (synthetic names like "Alex Test").
- Render ALL mocks to ONE PDF `OXPd_Screen_Designs_v1.pdf`: a cover page (what this is, the style source, the panel size used, what is inferred), a contents page, then one labelled page per screen (app, screen name, number) with a short "what changed from today" line. Use whatever headless renderer is available on this machine (check `which` for chrome/chromium, playwright, wkhtmltopdf, weasyprint; Google Chrome at `/Applications/Google Chrome.app` with `--headless --print-to-pdf` is likely). Never install system-wide; a tool you must add goes under your scratch folder.
- Also write `INDEX.md` (screen list with sources) and `REPORT.md` (10 lines max: DONE or BLOCKED, page count, the PDF path and byte count, what is inferred, questions with defaults).
- Before you report DONE: open the PDF (render page 1 and two random pages to PNG and look at them) and confirm the page count equals the screen count plus two.

Return 10 lines, first line `DONE` or `BLOCKED: <reason>`.
