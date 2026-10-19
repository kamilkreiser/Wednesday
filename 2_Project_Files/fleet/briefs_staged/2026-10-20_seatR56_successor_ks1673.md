## SUCCESSOR — you are Seat R 56th (lane Secuura/Blockchain-R, a BUILD seat tonight)

**Why you exist:** Seat R 55th proposed its own rotation before a large tier-1 build, and Wednesday approved it. Wednesday measured its context at ~690K tokens. Its handover is `5_Project_History/2026-10-19_seatR-55th/HANDOVER.md` (111 lines): read its LATEST STATE and its KS-1673 build brief FIRST, whole. Develop is `390cc0a317c9bc36c19f3a1684c745836af485df` (#1628; Wednesday's ls-remote at 00:5x AEDT 2026-10-20).

**Live beside you:** Seat C 27th (Secuura/Blockchain-C, pane %8, Sonnet) is raising four Spark passes; its files are listed under PARTITION. No other Secuura seat is live. Send a short plan confirmation (preflight warnings verbatim) before your first write.

---
## BLUF

Build **KS-1673 PR A**: bind every org-owned m365 resource (connections, sites, onedrive, documents) to the caller's organisation, failing closed. Wednesday RULED the plan as R 55th wrote it. Ship it at READY FOR GATE (tier 1, Opus). Then the queue below.

## QUEUE

1. **KS-1673 PR A.** Build exactly the ruled plan in R 55th's handover (its sections 2a-2e). In short:
   - `ownedConnection(req, id)` returns the connection only when `req.user.organizationId` and `connection.organizationId` are both non-empty strings and are equal. Otherwise the route answers the SAME 404 it gives an unknown id.
   - `POST /api/connections/init` takes the org from the TOKEN; `organizationId` leaves the body schema. A token with no org gets 403.
   - Bind connections/complete, GET/DELETE /api/connections/:id and /refresh; sites (owned through their connection, and the list filtered); onedrive/files and files/:id/sync (bound BEFORE any Graph call); documents/sync, GET /api/documents and /:id.
   - **No admin bypass of any kind** (Wednesday's ruling, 2026-10-20). Rows with a null org are owned by nobody.
   - **Cells:** orgs A and B, seeded through gate AP1's seam (mocked initDb → loadFromDb, listen calls back), with `global.fetch` spied on.
     - As B, A's resources answer 404 with ZERO calls to graph.microsoft.com; as A, they work.
     - `GET /api/sites` as B excludes A's sites.
     - `init` as A with a body org of B creates an A-owned connection.
     - Fail-closed rows: a token with no org; a row with a null org.
     - Same-org controls.
     - The mutant (drop the equality) reds every cross-org cell.
   - **The two gate asks Wednesday will put to the gate, so build for them:**
     - a census over all 22 routes with a positive control;
     - the "not yours" 404 is BYTE-IDENTICAL to the "unknown id" 404.
   - `Refs KS-1673` (PR B, Teams, is still to come).
2. **#1629 (KS-1622):** it is at gate AR1 (Sonnet, tier 2) at head cb776bfc4b20. The verdict and any GO come to YOU by mail. Merge only on that head-pinned GO.
3. **KS-1673 PR B (Teams)**, after PR A merges. The org comes from the token, not the body (`:1215`). The GET listing never returns another org's `webhookUrl`: the cell asserts the URL string is ABSENT from the body. `DELETE` and `notify` are scoped to the caller's org.
4. **The AP1 N3 `code`-seam follow-up**, test-only, with its own tier-2 gate.
5. **KS-1634 N2/N3** test-only follow-up (see R 55th's handover for its state).
6. **Per PR:** READY FOR GATE (cause, cells, mutants, the suite at the landing parent, files, the predicted landing tree on live develop), and one BLUF ticket comment.

## PARTITION

**Yours:** `services/m365-integration/src/**` and its tests; for #1629's merge only, `services/api-gateway/src/routes/platform.ts`.

**NOT yours: Seat C 27th is in these files.**
- `services/auth/src/routes/users.ts` (the hasUsersStubScope hunk)
- `services/security/src/converters.ts`
- `services/originate/src/routes/verification.ts` and `verificationV2.ts` (heal hunks)
- `services/originate/src/utils/idNamespaceCollision.ts`
- their four new test files

You share one inbox with every Secuura seat. A mail naming C 27th is not yours. Establish your seat from your pane and process (the PINNED `tmux display-message -p -t "$TMUX_PANE"` form), never from which thread looks like yours.

## HOLDS

- **A fresh clone has NO pre-push gate.** Before any push: `git config core.hooksPath .githooks && chmod +x .githooks/pre-push`, read back `git config --get core.hooksPath` in your plan confirmation (KS-1646). R 55th's clone already has it; read it back anyway.
- **Identity:** `git config user.name 'Kam Kreiser'` and `git config user.email kamil.kreiser@secuura.ai` LOCALLY; read back `git config --show-origin user.email`.
- **Pushing:** your repo's hook refuses a push whose tip is not the checked-out HEAD (.githooks/pre-push:351-359, as Seat C 27th measured at its clone on 2026-10-20; re-read at yours) and a non-fast-forward push (:76-82). Never `--no-verify`; never `ALLOW_FORCE` without a mail from Wednesday naming it. Transport: `-c core.sshCommand='<the repo's ssh command> -o ServerAliveInterval=30'`.
- `tsc -p` in m365 may exclude test files (KS-1090): type-check the tests another way, and treat `Tests: 0 total` as a load failure. Build `packages/shared` first in a fresh clone (KS-846).
- **Nothing on any box tonight.** No deploy, no box reads; KS-1673's live reach is already measured.
- Merge only on Wednesday's head-pinned GO after a gate verdict. Ticket comments are the only client-facing channel. No Docker on this Studio.
- Rotate inside your 80-90 band at a clean boundary, handover first. Mail every state change; a turn never ends on an unmailed report.

## RULED BY KAM, NOT YET IN AN ARTEFACT

- None for these tickets.

## RULED BY WEDNESDAY FOR THIS PROJECT, STILL OPERATIVE

- KS-1673 (Wednesday's ANSWER "KS-1673 plan ruled - no bypass, Teams in, two PRs"; also recorded on KS-1673 comment 579562f3):
  - no admin bypass, fail closed;
  - Teams in KS-1673;
  - PR A (connections/sites/onedrive/documents), then PR B (Teams), each a tier-1 Opus gate;
  - the RLS finding is OUT, filed as KS-1675.
- #1629 is not merged by R 55th; its GO goes to this seat (Wednesday's ANSWER "rotation approved - wrap now; 1629 at gate AR1 for R 56th").

PROVENANCE:
- KS-1673 Backlog, priority 2, 2 comments, last 2026-10-19T13:54:47Z, scope: "nothing ties a Microsoft 365 connection to the organisation that owns it" | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- KS-1622 In Progress, priority 4, 0 comments | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- KS-1671 In Progress, priority 2, 1 comment, last 2026-10-19T13:38:32Z (named only as the m365 crash fix already merged) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- KS-1634 In Progress, priority 2, 9 comments, last 2026-10-19T12:40:03Z | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- KS-1675 Backlog, priority 3, 0 comments (named only as out of scope) | Linear GraphQL, read by Wednesday with the project's own key | read 2026-10-20
- develop 390cc0a317c9 and #1629 head cb776bfc4b20 | git ls-remote origin via Wednesday's cache clone | read 2026-10-20
- the m365 routes at :890-903 and :1087-1092 | Wednesday's source read of index.ts at a66cd6a4d172 | read 2026-10-20

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-20 00:58
