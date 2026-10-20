# B399 drafter report (2026-10-21, 10:49-10:55 AEDT, clock from `date`)

Brief: `2026-10-21_B399_SEAT-G23_hpsmpoc-pr173-gate-round2.md` (36 lines, long lines). Slots: exactly 2 (`@STAMP_TIME@`, `@LAUNCH_AUTH@`; `grep -o -E '@[A-Z_]+@' | wc -l` = 2). Last line `READ-WHOLE-BY-TUESDAY: PENDING`. Read whole: B396 brief, B393 STATUS, B398 brief and STATUS, model-routing.md:104-112.

## Measurements (all read-only; `GH_CONFIG_DIR` = HPSM-POC's; `git --no-optional-locks -C <2_Project_Files> ls-remote origin ...`)
- ls-remote 10:49:54: main `9f196f20…`; branch and `refs/pull/173/head` `549e6b95…`; #175 `89bdb18e`; #170 `b5ea627e`; #171 `cc3eae47`; #174 `cd2f788e`. `refs/heads/b399*` none (b386* = 1). `.tools/*b399*` none. Ports 7570-7579: lsof rc 1 (no listener).
- `gh api pulls/173`: open, draft false, mergeable_state blocked, commits 9, files 22, +754/-43, base `9f196f20`.
- `pulls/173/commits`: 701147e8, a668c014, 52dc7710, f6f3624c, e5a5c217, 687246aa, 67cc03a4, 85d15af7 (parent 67cc03a4), merge 549e6b95 (parents 85d15af7, 9f196f20). Matches the task.
- `compare 67cc03a4...85d15af7`: 4 files, +25/+3-1/+66/+7 (matches B398).
- `compare 85d15af7...549e6b95`: 9 files (3 Feedback api files from #168, `web/package-lock.json`, `bff.formstream.test.ts`, `formGate.ts`, `formMeter.test.ts`, `mock/follow-up.ts`, `mock/follow-up.test.ts`); intersection with #173's 22 (from `pulls/173/files`, sorted, `comm -12`) = 0; control self-intersection = 22. Note: #173 has no `package*.json`/lock in its 22, so the lock change is main's only.
- `compare 9f196f20...549e6b95`: ahead 9, behind 0, 22 files, +754/-43.
- `compare 3aeeacc5...9f196f20`: 5 files (#169's), all web/server, none in the 22.
- Open-PR file overlap with the 22: #175 (9 files) 0, #170 (13) 0, #171 (1) 0, #174 (1) 0.
- Required contexts (`branches/main/protection/required_status_checks`): the five named in the task, confirmed verbatim.
- Check-runs at 549e6b95 (10:50:14): 5 only; CodeQL neutral, Analyze (actions) success, Analyze csharp/javascript-typescript/python in_progress; nothing else created yet. So CI is NOT readable yet; the brief tells the seat to re-read at start, mid, verdict.
- Code-scanning analyses `ref=refs/pull/173/head`: 549e6b95 actions (0); 85d15af7 javascript-typescript, python, actions (0 each); 67cc03a4 four (0). Open alerts at the ref: 0.
- `models_latest.json` `levels.opus.model_id` = `claude-opus-5-5` (key path confirmed). G-cap row is `model-routing.md:111` (G1 = :108, G2 = :109, G3 = :110); the brief cites :108 for G1 and :111 for the cap.

## Not measured (no npm/node/dotnet allowed)
Main `9f196f20`'s own web test count. The brief has the seat run the base and compute expected = base + 91 (B393 70 + B398 21), with names added exactly 91. I did not guess a number for #169's rows.

## Questions, with recommended answers
1. CI is mostly not started at 549e6b95 (5 of ~16 runs). Launch now or wait? Recommend: launch now; the seat's local checks (identity, mutants, suites) take most of the time and CI is re-read at start/mid/verdict. If CI is still pending at verdict the suffix `(CI pending: ...)` applies and Tuesday decides.
2. The gate counts mutant survivors against committed rows (B393's reading, which Tuesday did not overrule). Recommend keeping that reading in round 2 (the brief states it). If Tuesday wants the union reading, change check 2.
3. B398's open note (SignInScreen.test.tsx `beforeEach` does not reset `replace`) is left as a possible Note, not a finding, unless a new row is vacuous because of it. Recommend that.
4. `web e2e` shards: the brief requires them green incl. `hosted-entra.spec.ts`; if they are skipped or absent, that is "NOT TESTED in CI", and the seat may run the hosted project locally as B393 did (ports 7570-7579; the brief lists the ports but I did not spell out the Playwright run, since CI is expected to cover it). Recommend: add nothing unless CI e2e is absent at verdict.
5. Launch line is B396's form with pane G23, level opus, and the new path. Tuesday fills the two slots at stamp time (authority text as in B396/B398: Kam's 2026-10-16 grant, his 2026-10-21 ~07:2x words, the 2026-09-01 three-hop rule tiered 2026-09-05).
