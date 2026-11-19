# B1740 census commission — NexusAI RD-1006: every audit-row write site, bounded or not (read-only)
Commissioned by Tuesday (s293), 2026-11-19. Model: Sonnet (routing row C8). You write ONE document; you change nothing.

WHY: RD-1006 (Task, Medium, To Do) says the audit rows the RD-994 guard does not bound can still grow without limit.
Its build waits for the product owner's word on the ticket's open question. Tuesday's decision (a default, not the product
owner's): produce the census now so that the question, when it goes to the product owner, carries measured facts.
NOTHING is built, ticketed, commented or decided by this pass.

OUTPUT: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1740_RD-1006_audit-write-census.md`
(ASCII; built whole, written to a temp file beside it, then os.replace). Return a short report as TEXT in your reply.

SCOPE, at NexusAI main (read `branches/main` first and print the sha; expected 9373976efc7d93f522f97648beb608b4d3e16fb2
or a descendant; every file read as `contents/<path>?ref=<that sha>` or from a scratch clone at that sha, never the
project's working tree):
1. Read RD-1006 whole by Jira GET and quote its scope sentence and its open question word for word. Read RD-994's
   landed guard (the AUDIT-FIELDS block in `backend/server.js`) and state exactly which fields of which rows it bounds.
2. Enumerate EVERY site that writes an audit row or audit entry: start from the audit writer(s) (find them: `auditLog(`,
   `audit(`, `logSecurityEvent(`, the STATE_MUTATION and REQUEST_DENIED writers, router-local `audit` helpers such as
   the one in `backend/routes/entraProvisioning.js`) and list every call site by file and line, BY PROGRAM. State the
   frame in the sentence that gives the total: which directories and file types were searched, and what lies outside it
   (other languages, scripts, generated files); then look outside it once.
3. For each site, one row: file:line | event name | each caller-influenced field it records (request path, ids, names,
   body values, header values, error text) | bounded HERE (cite the line) / bounded ELSEWHERE (cite) / UNBOUNDED |
   who can reach it (anonymous, any signed-in session, administrator only: cite the check, or write "not traced").
   A row you could not establish says so; never a confident guess. Check both directions on anything RD-1006 or the
   RD-994 records already claim (less true or more true than written).
4. The storage side: where the rows go (file, table, external sink), whether the store itself caps a row or the file
   (rotation, size limit), with the line that shows it or "not found in the frame".
5. A short DESIGN NOTE at the end, clearly marked as options and not decisions: the two or three shapes a fix could take
   (one shared cap in the writer; per-field caps at the sites; a cap at the store), what each would change for existing
   tests (count by program the tests that pin a long value in an audit row), and what is NOT known.
6. Sections FOUND / TESTED (scope, and what was NOT tested) / HOW (instrument, commands, positive and negative controls).

HOW: read-only everywhere. NexusAI GH_CONFIG_DIR '/Volumes/Datasec_DEV/!CODING/Datasec/NexusAI/4_Credentials/.gh-config'
(verify the account reads kamilDatasec; every gh call `-X GET`). Jira GET only; credentials read by name in-process from
the project's `4_Credentials/.env`, never printed, never on argv. In the project checkout: git read verbs only; a clone
for your own use goes in your scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1740/` with its
push URL set to `invalid://no-push`. No server, no jest, no request to any app host. No `cd`; zsh; absolute paths; every
count with `/usr/bin/grep -i` and a positive control; never read an absence through head or cut. Clocks from `date`.
No person's name, no client name and no credential value in the document.
First line of your reply: `CENSUS: <n> sites, <u> unbounded, main <sha8>` or `STOPPED: <why>`.
