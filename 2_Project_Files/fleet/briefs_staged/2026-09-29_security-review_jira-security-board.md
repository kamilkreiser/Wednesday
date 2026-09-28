BLUF: Kam wants ONE Jira board for security holding every Datasec security ticket raised from the Security Review, shared with Steve. You are the right seat: this project ran the 2026-09-10 ticketing round and knows where every ticket went. Build it non-destructively (a board over a saved filter, NOT by moving tickets), share it with Steve, report back. This brief authorises the Jira writes named below and nothing else; it SUPERSEDES the launcher's "Jira is READ-ONLY" line for these writes only (your BACKLOG already records that line as stale).

RULED BY KAM, NOT YET IN AN ARTEFACT
- Live board, 2026-09-29 08:07:22 AEST, verbatim: "With regards to the Security Review - Create a jira board for security. Place all datasec security tickets from security review and share with Steve"
  -> record it in this project's CLARIFICATIONS (create the file in NexusAI's format if it does not exist) and mail Tuesday the C-number.

RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE
- (none since the last brief; this seat's rulings come from Tuesday.)

QUEUE
1. ENUMERATE first (read): every Jira ticket this project raised or that carries a Security Review finding, across ALL projects on the Datasec Jira site (RD, HPAM, CWP, CPKEY, MYP, SEC and any other), including the four intake tickets (CWP-4, CPKEY-168, MYP-40, SEC-3). Build the list from your own records (_Working/jira-2026-09-10, the ticketing report) AND a JQL search; say what each source found and reconcile the two. "Datasec security tickets from the security review" = the review's findings as filed; say plainly anything you are unsure belongs.
2. LABEL each one `security-review` (additive only; do not change status, assignee, priority or text).
3. CREATE a saved filter (`labels = security-review`) and a board over it named "Datasec Security Review". Prefer a board over the filter; do NOT move tickets between projects and do NOT create a new Jira project unless a board cannot be made without one (then STOP and mail).
4. SHARE with Steve: find his Jira account (read the user search; HPAM-115 "Review HPAM Tokens with Steve" names him). If exactly one Datasec Steve exists, share the filter and board with him (view). If none, or more than one, STOP and mail Tuesday the candidates: inviting a new Jira user is a licence (money) and is Kam's.
5. Report: the board URL, the filter id, the ticket count by project (a real count, not a cap), who it is shared with and how, and anything you left out and why.

HOLDS
- No ticket moved, deleted, transitioned or edited beyond the label. No new Jira project, no user invitation, no permission-scheme change, no mail to Steve or any human (sharing through Jira is the only contact). Never delete.
- No source code writes; the review deliverables stay read-only.
- Wrap to tuesday-agent@agentmail.to, subject tag [Datasec/Security Review -> Tuesday].


CHANNEL AND CREDENTIALS (this project is not wired into the fleet's mail on this machine)
- This brief reaches you as a FILE committed in Tuesday's repo (the path in your launch tap). Treat it as the brief; its author is the Tuesday coordinator seat.
- Jira: use the method your own HANDOFF_AND_NEXT_SESSION.md records (REST against the Datasec Atlassian site, with the Datasec Jira credentials it names; on this drive the NexusAI project's 4_Credentials/.env). Source them transiently; never copy them into this project's files or print them.
- Report: write it to _Working/2026-09-29_SECURITY_BOARD_REPORT.md (your own folder). If you can send AgentMail, also mail it to tuesday-agent@agentmail.to; if you cannot, say so in the report and stop at the prompt; Tuesday reads the file.

PROVENANCE
- Kam's instruction: live board message 2026-09-29T08:07:22+10:00, view=tuesday | kam_msgs.sh --source live | read 08:07
- ticketing round + intake tickets: /Volumes/KK_T9_External_HDD/!CODING/Datasec/Security Review/BACKLOG.md lines 36-80 | read by Tuesday 08:1x
- Steve named in HPAM-115: _Working/reconciliation-seed.md | grep by Tuesday 08:1x
SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 08:08
