# C3 findings — audit C (rule accuracy + status), listC.txt lines 39-57

| file | audit | what was wrong | evidence |
|---|---|---|---|
| 2026-10-08_sonnet-trials-and-a-shared-model-routing-definition.md | C | Rule tells the seat to "switch a seat with /model in its pane". That is the lesson's 10-08 mechanism (lesson line 23), but it is not the current form: the routing spec the same rule points to now forbids it, because /model in a pane overwrites Kam's global default model. The lesson file itself was never corrected, so the row copied a stale and harmful instruction. Also "Sonnet seats are measured trials" predates routing v1.0 (in force 2026-10-18), and the lesson's own status line says its Spark half is dead. | `2_Project_Files/fleet/specs/model-routing.md:136` "A seat's model is set AT LAUNCH: pass `SEAT_MODEL_ENV=<id>` ... **Never send `/model` into a seat's pane:** it writes Kam's global `~/.claude/settings.json` default (ledger, 2026-11-03). A seat on the wrong model is relaunched." · `_ledger_archive.md:346` (2026-11-03 row: /model in a seat's pane wrote Kam's user-global settings.json) · lesson line 23 "A trial switches ONE seat after launch with `/model claude-sonnet-5-5` in that seat's pane" · lesson line 5 "PARTLY SUPERSEDED ... every Spark clause is dead" · model-routing.md:1 "v1.0 (2026-10-18) -- IN FORCE" |
| 2026-09-29_regenerable-build-leftovers-are-not-kept.md | C | Rule drops the load-bearing limit in the lesson's own headline: a seat removes only ITS OWN leftovers; anything touching other seats' trees or more than one project is a card for Kam. As written ("deleted by the project's own seat") it reads as a standing licence to delete any stale regenerable artefact in the project. | lesson line 9 headline "...but only Kam's word authorises a deletion, and records are never in scope" · line 24 "a seat's handover names the regenerable leftovers it created and removes them (its own only)" · line 25 "it still goes to Kam as a card if it touches other seats' trees or more than one project" |
| 2026-09-20_a-control-in-the-wrong-scan-mode-buys-confidence.md | C | Rule covers the control/canary half but omits the file's w=3 root, which the lesson gives failing-test treatment and which is the half that fires at the `brief` trigger the row carries: before an instruction names a path, file or dependency, read the governing property (config, contents, clause), not existence/size/location. "Commission measurements not actions" was kept instead; the w>=3 rule outranks it. (12 KB file; not everything fits: branch-push-is-shared-CI and commit-before-a-destructive-control stay in the file.) | lesson lines 129-134 "**The failing-test treatment (w≥3):** before any instruction that names a PATH, a FILE or a DEPENDENCY, write down ... fill the blank with a property I have actually read ... If the blank can only be filled with existence, size or location, I have not checked the governing property" · lines 59-60 "before commissioning a file into a scanned or built repo, ask what the tooling will SEE in it" |

CHECKED: 19  WRONG: 3

Status checks inside this slice (all found correct): 5 dead (2026-09-15 q4 week, 2026-09-18 no-claude-agents, 2026-10-05 october-deploy, 2026-10-06 use-to-100pct, 2026-10-08 new-account) and 5 superseded (2026-09-23 spark-kit, 2026-09-23 use-the-local-model, 2026-09-25 spark-calibrate, 2026-10-05 spark-50, 2026-10-06 past-70pct). Each dead row has an `expires:` date/event in the lesson that has passed, or frontmatter `status: expired`; each superseded row's frontmatter says superseded and names the newer file; both target files exist in learnings/ (2026-11-15_the-spark-is-gone-checks-retired-no-local-spark-tier.md, 2026-10-14_80-to-90pct-limited-cloud-wednesday-and-spark.md). Note: four dead grant files still carry `status: live` in their own frontmatter (09-15 q4, 09-18 no-claude-agents, 10-05 october-deploy, 10-08 new-account) with an expiry that has passed; the index is right, the lesson frontmatter is stale (not edited, out of scope).

Found correct (16):
- 2026-09-15_ornith-q4-only-volume-week-qa-sunday-merge-once.md (dead)
- 2026-09-16_never-edit-a-bash-script-that-is-currently-running.md
- 2026-09-18_a-premise-under-a-question-to-kam-is-load-bearing-verify-it.md
- 2026-09-18_no-claude-agents-local-model-only-until-sunday.md (dead)
- 2026-09-18_ornith-works-constantly-standing-rule.md
- 2026-09-20_most-of-a-project-folder-is-outside-its-git-repo.md
- 2026-09-23_build-seats-run-in-cockpit-panes.md
- 2026-09-23_spark-kit-running-a-local-coding-model.md (superseded)
- 2026-09-23_use-the-local-model-as-much-as-possible.md (superseded)
- 2026-09-25_spark-calibrate-like-ornith-start-high-oversight.md (superseded)
- 2026-10-05_board-taps-suffice-for-audit-redates.md
- 2026-10-05_october-deploy-both-boxes-when-ready.md (dead)
- 2026-10-05_spark-target-50-tasks-a-day.md (superseded)
- 2026-10-06_past-70pct-spark-takes-80pct-of-tasks.md (superseded)
- 2026-10-06_use-to-100pct-spark-all-tickets-one-or-two-deployers.md (dead)
- 2026-10-08_new-account-push-merge-test-as-much-as-possible.md (dead)

Out of scope, noted for audit A: 2026-10-05_board-taps-suffice-for-audit-redates.md is seats=wednesday but is a Secuura-client grant (lesson line 19 "Secuura seats treated a re-date as approval-class").
Not checked: seats and enforced_by fields; the EXPIRING-GRANTS.md rows for the dead grants (dead status judged from each lesson's own expiry line against today's date 2026-11-18).
