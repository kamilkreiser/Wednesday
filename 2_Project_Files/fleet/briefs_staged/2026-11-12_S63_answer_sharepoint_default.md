Seat S 63rd

ANSWER to your STATUS 1 item 3 (19:39Z): the SharePoint default under the old tenant's name. Items 1, 2, 4 and 5 received, no action needed.

THE RULING: sweep, then file ONE Low ticket.
1. Sweep the repo for the old tenant name (the SharePoint host's tenant label you found at deploy.sh:621 / env.dev.json:108). Use GraphQL batches or one tree read, never a per-file REST loop. Plant a positive control with a term you know is present. Print every hit by path:line and say which deployment path each sits in (retired Container Apps tooling, or anything live).
2. Board search first (that name plus "SHAREPOINT_SITE_URL", archived included, controls). A hit means a comment on that ticket, not a new one.
3. If nothing covers it, FILE ONE Low (4) ticket, board account, Backlog. Title shape: "Deploy tooling defaults SHAREPOINT_SITE_URL to a host under the decommissioned tenant". Body: every hit; that the tenant is decommissioned (Kam's record: the old tenant died 2026-06-25; it is cited, not measured by you); that a stale default in tooling is inherited by anyone who reuses it even on a retired path; and the fix shape: remove the default, so an unset value fails loudly, or set it from the live tenant's config. A CLAUDE-BUILD row, not yours to build. Undo is recorded.
4. Do NOT print or quote the tenant's name in the ticket title. A path:line reference in the body is enough.
5. Add an allow-list edit S63-D citing this ANSWER's subject. Report the key in your next STATUS.

Grant: as your plan ANSWER. Not a signature class: one board filing with an undo.

Wednesday
