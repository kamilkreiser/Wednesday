# PR #1482 gate rerun - GO WITH NOTE
Head b5077012c012c1daa41a27a325dcd5f6a3e88129 (bundle sha256/16 2a4c824b64ab3201 verified). Merge predicted over develop 8cfab55b0 (newest available, from worktree s-v3-l05g; no credentials for ls-remote). Test file untouched on develop since 524db0ce6.
- Diff: exactly 1 file, test only. File: ks1061-shared-mock-completeness.test.ts. Develop's 3-cell version 3/3; head 10/10.
- Merged tree full originate suite x2: 98 suites/1121 (=develop + 7 new cells), both runs. tsc src clean; tests typechecked via temp tsconfig (tests excluded in originate tsconfig) clean, control error caught. eslint head and merged exit 0, control caught.
- Seat mutations reproduced: single 3, mock-only 2, non-recursive 3, one-level 1, develop patterns 2 (T8 + exact-set).
- Own: double-only (6 red), scan disabled (6), skip-subdir (3) all red. SURVIVORS: VIA_HELPER loosened to `require(`: 10/10 green; ROOT_MOCK without /g: 10/10 green.
- Regex probe: no vacuous pass on corpus forms; comments/spread/block-body = conservative false-red.
Defects
1 Minor, test.ts:~55 (VIA_HELPER): no negative twin for a wrong helper path/name; loosening survives.
2 Minor, test.ts:~54 (ROOT_MOCK /g): no two-factory-in-one-file cell; dropping /g survives.
3 Minor: claim "T6b/T6c/T7 red on develop's patterns" is only true vs pre-#1256 patterns; develop's already have them; only T8 is red there.
4 Minor (pre-existing): blind to setMock, unstable_mockModule, aliased jest, non-literal names; none present in corpus.
