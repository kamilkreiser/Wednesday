# A3 findings - audit A, listA lines 57-84

| file | audit | what was wrong | evidence |
|---|---|---|---|
| 2026-10-12_secuura-done-when-tested-works-deployed-and-never-idle.md | A | seats `wednesday` -> `wednesday,friday` (firm). Secuura client rule (the definition of Done for a Secuura ticket), narrowed to the seat it was said to. Friday serves Secuura and would not see it. | L18: "Close when unit tests pass on develop AND the fix is in the running Kintsugi build; the closing comment says 'no live check possible'" - a rule about the client's tickets, not about Studio hardware |
| 2026-10-16_tuesday-boot-sweeps-project-feedback-into-tickets.md | A | seats `tuesday` -> `tuesday,friday` (medium). The boot sweep is Tuesday's ritual, but the row also carries two Datasec-wide safety rules (no GET on production hosts; check Kam's cards before raising a finding) that any seat serving Datasec needs. Rule text keeps 'Tuesday' so Friday does not duplicate the sweep. | L21: "Production is out of bounds for the sweep ... a GET on the Vision Sales Portal's live feedback report ran `CREATE TABLE IF NOT EXISTS` on the production database" / "Before raising any finding, check Kam's cards" |
| 2026-10-23_hpsmpoc-build-only-this-phase-next-phase-funds-it.md | A | seats `tuesday` -> `tuesday,friday` (firm). Datasec client-project rule (commercial scope of HPSM-POC), not a Mac-mini thing. Friday serves Datasec. | L19: "Why (the reason is commercial, not technical): HP funds the next phase." L22: "Every HPSM-POC brief carries the standing line" |
| 2026-10-23_tuesday-never-wait-on-kam-cards-morning-card-48h-email-priorities.md | A | seats `tuesday` -> `tuesday,friday` (medium). The card/morning-card half reaches Friday through the wednesday,friday twin, but the Datasec project priority order (HPSM-POC, Calculator, Composer) exists only in this row and is a client rule; the twin row drops it as 'Datasec's'. | L24: "allocated in the order **HPSM-POC -> MPS Calculator -> Security Composer**"; twin file L23: "project priorities HPSM-POC/Calculator/Composer are Datasec's and not this seat's anyway" |
| 2026-10-30_kam-and-stuart-meet-monthly-on-long-term-development.md | A | seats `wednesday` -> `wednesday,friday` (firm). Secuura client rule (where long-term Secuura questions go); applies to any seat serving Secuura. | L13: "Wednesday or a Secuura seat is about to put a LONG-TERM development question in front of Kam or Stuart ... That class now has a home: the monthly Kam-Stuart meeting." |
| 2026-11-06_clear-the-secuura-board-over-one-to-two-weeks.md | A | seats `wednesday` -> `wednesday,friday` (firm). Secuura board order and exit rule, live to 2026-11-20; a client-project grant, not a Studio-owned thing. | L12: "choosing what the Secuura floor does next ... The answer is the board. In Review and In Progress first, then Todo and Backlog." |
| 2026-11-11_wednesday-lives-on-the-mac-mini.md | A | seats `wednesday` -> `all` (firm). The row's own rule is general conduct on any new machine (check alias/binary/volume; rc 1 = wrong binary; /usr/bin/log in zsh). The only seat-specific fact in the lesson (Wednesday on the mini) is the part the row already calls stale. | L18: "A tool that names a host alias, a binary path or a volume is checked on the mini before it is trusted. A `rc 1` from a copy tool is first read as 'wrong binary'" L19: "In zsh, `log` is a builtin" |
| 2026-11-13_premerge-do-not-merge-sentence-dropped-nine-released.md | A | seats `wednesday` -> `wednesday,friday` (firm). Rule about Secuura PR text and merge holds; applies to any seat briefing or merging Secuura work. | L17: "Every Secuura raise/build brief carries the standing line in `2_Project_Files/fleet/STANDING_LINES.md`" |
| 2026-11-15_mirror-peters-tests-so-we-catch-everything.md | A | seats `wednesday` -> `wednesday,friday` (firm). What 'tested' means for a Secuura PR; client rule. The local-slot hardware note is a condition inside the rule, not its scope. | L11: "'Tested' for a Secuura PR means tested the way Peter's process tests it" |
| 2026-11-15_recent-merge-rules-override-historic-holds.md | A | seats `wednesday` -> `wednesday,friday` (firm). Kam's word was given on Secuura PRs and rests on Secuura merge grants; it applies to any seat issuing a Secuura GO, not to the Studio alone. (Not widened to all: every rule it cites is a Secuura grant/card.) | L11: "the self-hold sentence never blocks (card secuura-premerge-block-nine-prs-1113 = c). An OLD hold carried forward brief to brief ... does NOT keep a ready PR out." |
| 2026-11-16_audit-records-and-verification-public-read-creator-write.md | A | seats `wednesday` -> `wednesday,friday` (firm). Standing Secuura access-control ruling 'for all related tasks and tickets'; Friday briefing or gating Secuura work must see it. | L14: "new rule for all related tasks and tickets. Audit records and verification can be read by anyone in the world." |
| 2026-11-16_preflight-failure-must-not-kill-a-rotation.md | A | seats `wednesday` -> `all` (firm). The mechanism lives in shared tooling every seat runs: wednesday_rotate.sh maps all three seats and Launch_Friday/Launch_Tuesday both `exec` Launch_Wednesday.command. On Friday's card this row is listed as 'other seats only'. | wednesday_rotate.sh L58-60: `tuesday) SEAT_LAUNCHER=.../Launch_Tuesday.command` `friday) SEAT_LAUNCHER=.../Launch_Friday.command`; Launch_Friday.command L36,L68: `SHARED="$HERE/Launch_Wednesday.command"` `exec bash "$SHARED"`; lesson L12: "a human-answered gate must never sit in an unattended path" |

CHECKED: 28  WRONG: 12 (10 firm, 2 medium)

## Found correct (16)
- 2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark.md (live, wednesday)
- 2026-10-15_storage-policy-for-old-blockchain-files-and-tests-monday.md (dead, wednesday)
- 2026-10-16_tuesday-inherits-push-to-demo-hpsmpoc-unfrozen-account-controls-datasec.md (live, tuesday)
- 2026-10-18_new-account-tickets-backlog-routing-definition-spark-max.md (live, wednesday)
- 2026-10-20_tuesday-no-90pct-line-two-accounts.md (live, tuesday)
- 2026-10-22_tuesday-sonnet-default-usage-is-a-guide.md (live, tuesday)
- 2026-10-23_kam-items-on-fleet-activity-morning-card-48h-email.md (live, wednesday,friday)
- 2026-10-24_every-boot-works-the-actionable-tickets-unprompted.md (live, tuesday)
- 2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice.md (superseded, wednesday)
- 2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md (dead, wednesday)
- 2026-10-30_wednesday-go-counts-as-kams-word-for-starting-work.md (live, wednesday)
- 2026-11-11_nas-dev-working-dated-offload.md (live, tuesday)
- 2026-11-11_wednesday-offloads-to-dev-working-nas.md (live, wednesday)
- 2026-11-12_spark-for-harness-and-token-heavy-simple-tasks.md (superseded, wednesday)
- 2026-11-16_architecture-agents-run-on-the-newest-fable.md (live, friday)
- 2026-11-16_grant-build-coagent-overnight-until-the-morning-review.md (dead, friday)

## Principle used
Narrow stays when the row is (a) a grant of authority or a usage/launch allowance given to one named seat or account (not widened by inference: widening a grant hands a seat authority Kam did not give it), (b) a seat-owned tool or path (the two nas_offload copies), (c) dead/superseded (not on any card, seats moot). Widened when the rule is about the CLIENT'S project (what Done means, what is built, PR text, access rulings, where questions go) or about fleet-wide tooling/general conduct.

## Borderline, kept narrow (parent may overrule)
- 2026-10-16_tuesday-inherits-push-to-demo-...: grant "tied to this account" (L23); Friday has its own live row 2026-10-06_push-to-demo-when-ready-no-card (friday). Kept `tuesday`. Note this lesson's headline says Friday's grant "now applies to Tuesday" - whether Friday's 10-06 row is still Friday's was not checked.
- 2026-10-18_new-account-tickets-backlog-...: Secuura work order, but an account-event grant to Wednesday and mostly overtaken by the 11-06 board grant. Kept `wednesday`.
- 2026-10-14_80-to-90pct-...: "for this seat" (frontmatter L7); the band is about Wednesday + Ornith doing the work. Kept `wednesday`.
- 2026-10-20, 2026-10-22 (tuesday), 2026-10-24: Tuesday's own usage line / routing / boot ritual; the general forms exist as `all` rows (2026-10-22_usage-is-a-guide..., 2026-09-02_coo-actionable...). Kept `tuesday`.
- 2026-10-30_wednesday-go-counts-as-kams-word: the grant is to Wednesday's GO by name. Kept `wednesday`.

## Incidental (not my audit; no fix row written, to avoid colliding with B/C fixes)
- B: 2026-10-23_kam-items-on-fleet-activity-morning-card-48h-email.md enforced_by stale_card_escalate.sh: the script covers only the 48 h email clause, and only for Wednesday's cards (lesson L22: "Datasec and Friday cards are their seats' to escalate"). The card/morning-card/never-wait clauses are not enforced, and on Friday's card the rule is cut to 120 chars under "the tool remembers".
- B: 2026-11-16_preflight-failure-must-not-kill-a-rotation.md enforced_by Launch_Wednesday.command (L387-394, L888-897 do carry the failures forward mechanically); the "fix them first" clause is the seat's duty and is not enforced. My fix row leaves enforced_by unchanged.
- C: 2026-10-15_storage-policy-... (dead): the rule's tail "later removals follow the never-delete quarantine rule, not this grant" may be wrong. Lesson L17 says the policy NARROWS never-delete for the classes it names, and _audits/2026-10-19_consolidation.md L62 records the policy was written (WED-154). Whether Kam approved it was not checked.
- C: 2026-11-06_clear-the-secuura-board lesson L23 still says "A ticket with no live check possible stays open", contradicting the amended 10-12 rule (L21). The row does not repeat the stale clause; the lesson file does.
- C (cosmetic): 2026-10-24 row rule is missing a full stop: "launch in waves Signature classes and gates stand".
- 2026-11-11_wednesday-lives-on-the-mac-mini.md: lesson says Wednesday's home is the Mac mini; the brief for this review says wednesday = Mac Studio. The row already hedges ("seat home may have moved since"); the lesson file itself is stale.
