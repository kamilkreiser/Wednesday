# B475 drafter report (Sonnet, read-only), 2026-10-22 about 19:15-19:40 AEDT

Brief: `2026-10-22_B475_SEAT-H5_hpsmpoc-b461-fixround1.md` (113 lines), fix round 1 of 2 on `b461/hpsmpoc-296-297-live-api-e2e` from `52bd6e7c`, pane `Datasec/HPSM-POC-H5`, Sonnet C2, ports 8260-8269.

## Measured (read verbs, `gh api` GETs, `lsof`, `tmux`, `ls`)
- `ls-remote`: main `d70f9dc1`, b461 `52bd6e7c` (= the gated head), b465 `c65a5ab6`, b467 `3b2a8240`, b462 `e8ecb8ae`, b429 `4c02e8b9`; no `b475*`, `b466*`, `b471*`, `b472*`, `b474*` ref. `.tools/b475` and `wt-b475-*` absent. Pane `Datasec/HPSM-POC-H5` not in `tmux list-panes`.
- b461 compare vs main: ahead 1, behind 2, 14 files (13 M + the new `live-api-preconditions.mjs`), matching the gate's 14.
- Ports 8260-8269: `lsof` rc 1 (nothing). No brief in `tuesday/briefs` names 826x (`grep -E -w '826[0-9]'` = no hit); control: 8250-8259 and 8240-8249 appear. Positive bind-and-free control NOT run by me (I only confirmed unfiltered `lsof` lists listeners: 12 lines).
- Intersection program (`grep -x -F -f`) of b461's 14 paths against: b429 (43 paths; the gate said 45, 43 is the compare against current main), b465 (19), b467 (2), b462 (6), B466 declared (14, parsed from its Yours line), B472 (1, `Auth/UatOpenTests.cs`), B467's declared directories: **0 shared in each**. Controls: a planted shared path appended to the b465 list was found (1); `web/src/instrumentation.ts` is in the b429 list (1); self-compare `main...main` lists 0 files.
- Line anchors at head `52bd6e7c` (all agree with the gate): `live-api-preconditions.mjs:56` (E16), `e2e.mjs:230` (readMode headers), `:291` (`--api-port`), `:311-312` (unit status ignored), `:146-157` (refusals), `playbook-action-plan-live-api.spec.ts:155` (`"Partner Dashboard"`, only live-spec hit), `web/README.md:60`, override spec C-29 at :110 with `sha` equalities :128/:149/:158. Unit file: 35 `it(` rows; row "every refusal at once" (:194-197) expects exactly 6.
- B465 head: `PartnerDashboard.tsx:50` has `<PageHeader title="Home"`, so the `"Home"` line is right once B465 lands.
- Shared lock `.tools/.git-lock` directory EXISTS (mtime 19:10); contents unreadable/empty; B468 saw it held 10+ minutes. The brief says poll, never break it. `.tools/b198/lock.sh` = `.tools/b267/lock.sh` (cmp same); `.tools/b267/waitload.sh` = `.tools/b461/waitload.sh` (cmp same). Load1 12.1 at 19:17.

## Corrections to my instructions / things you should know
1. **Ordering vs B465's own STATUS.** B465 STATUS FOR TUESDAY 1 says "B465 must not merge before that follow-up is ready". Your order (B465 first, then b461) is consistent only if the follow-up exists on b461 (it will after this round) and you accept a window in which main's live spec says `Partner Dashboard` against a `Home` page. The live set is outside CI, so nothing red appears. The brief states the order and quotes this tension for the builder's STATUS.
2. **B468-1 may have no clean fix from existing reads.** Showcase-ON other-owner and showcase-OFF both give an empty customer list to `showcase-partner`, and `/api/v1/me` returned a GUID `userId` (not the user name) in the gate's probe. The brief therefore makes item 2 measure first (three API shapes), enforce at least the default caller's roles, and, if nothing existing separates the two, write "stated, not enforced" plus ONE question to you (an `--api-mode` declaration on the command is the option; it changes the command surface, so I did not authorise it). This is the item most likely to come back as `STOPPED`.
3. **B468-6 versus an existing row.** "Print the cause once" would break the row expecting 6 refusals if done naively. The brief requires a structural `notProbed` flag from `readMode` so that row stays unedited.
4. **B468-3 sizing.** Left to the builder with an explicit "defer to FOR TUESDAY if larger"; the loop wiring may be read-proof only (UNMEASURED as the gate's was).
5. b429 is 43 paths today (gate: 45 at 19:12); partition text uses the compare against current main.
6. A zsh trap hit me: `$H:web/...` expands `:w` as a modifier; the brief's shell line says to write `${VAR}:path`.

## Slot count with a control
`/usr/bin/grep -c -E '_''_''_''_'` on the brief: **8** (seven stamp slots: stamp time, launch authority, hard stop/target, main, b461 head, b465 head, model/load1; plus the last line `READ-WHOLE-BY-TUESDAY: ____`). Control: a scratch file `x____` reads **1**. The REFUSE line itself uses the split pattern and does not match. No person name in the brief (`grep -c -i -E 'kam|kamil|kreiser'` = 0).

## Unmeasured
Anything that needs a run: `/me` and `/showcase/summary` shapes per API mode; the 409 problem's JSON field; whether item 4 is small; the action-plan line against a B465 build; whether `.git-lock` is stale; that `brief_seat.sh` and `cockpit.sh add` accept the launch line (copied from B461's shape, not executed); the bind-and-free positive control for 8260-8269.
