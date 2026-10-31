STARTABLE: NO (PCOMP-40 / L3-2 is already built and merged; no builder lane exists as commissioned)

BLUF: Composer main d70edf70 holds `packages/db/migrations/0025_attribute_overrides.sql` + `rollback/0025_attribute_overrides.down.sql`, merged by PR #87 (sha e019ac3a, "migrations 0023-0025"), covering L3-2 (PCOMP-40), L3-3 (PCOMP-41) and L3-5 (PCOMP-43). The sweep's "cheapest real work: PCOMP-40..44" is stale: the tickets sit in Backlog because no rule moves them on merge, and PCOMP-40's text still says "NOT started" and names `0022_*`. Best action: a records seat (option A in the kit), not a builder. The kit file is a shape-holder with REFUSE 1 (stops at once); it is not stamped and should not be launched.

Measured (read-only, 12:0x AEDT 2026-10-31):
- gh GET: commits/main = d70edf70fc43bb69737b2a242ba56480ce79f0d8; migrations list 0001-0027; pulls/87 merged; document.ts: ATTRIBUTE_OVERRIDE_NOT_BUILT 1 hit (a comment at line 114; control putControl 3).
- Jira GET (jira791.py `get`, in-process creds): PCOMP-40, -41, -42, -43, -44 all Backlog, 0 comments; PCOMP-999999 HTTP 404.
- PCOMP-44 (L3-6): OUTPUT_KINDS has 12 kinds, 0 sm_policy; but `apps/api/src/outputs.ts:33-37` forces contract enum == renderer union both ways, so a contract-only add does not compile: needs a ruling (stub renderer or widened union). No DB file names an output kind.
- Open PRs #95 #85 #91 #86: 0 files each under packages/db or packages/api-contract. Branches: 177 heads; only b917/... is b9x of note (landed as main d70edf70).
- tmux panes: tuesday, fleet-monitor, HPSM-POC-R94, HPSM-POC-H79 (no Composer pane). lsof 9710-9719: no listener, but the range is named by 16 recent HPSM-POC kit mentions, so do not give it to Composer; Composer needs no ports. load1 7.73 at 12:03 (above the launch gate of 7).
- Seat: J33 is the highest Composer seat; next free J34. Routing: model row C2 (claude-sonnet-5-5, models_latest.json); a migration/contract change is a G1 (tier 1) gate, Opus first.
- Not read: PRs' test coverage of overrides round trip (unmeasured), SOW, Source_Documents, inbound.

Q-questions:
- Q-1: Re-point B975 to option A (records seat closing PCOMP-40/-41/-43 as "merged, not deployed")? Default: YES, but only after the product owner confirms the close rule the sweep names.
- Q-2: Rule PCOMP-44 shape (stub renderers vs widen union) before any builder? Default: HOLD; not a structure-only lane.
- Q-3: Drop this kit? Default: YES, keep as record only.

Stamp values: none to fill; if ever re-pointed: seat J34, pane Datasec/Security-Composer-J34, ports none, model claude-sonnet-5-5 (C2), gate G1 tier 1, base main d70edf70fc43bb69737b2a242ba56480ce79f0d8, load1 7.73 (12:03) so wait for launch_when_cool.

Files: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-31_B975_SEAT-J34_composer-pcomp40-attribute-overrides-storage.md
