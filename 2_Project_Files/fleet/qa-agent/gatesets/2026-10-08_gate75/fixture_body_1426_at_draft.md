**BLUF:** `develop` has failed its own pre-push preflight on **leg 14** since `89dff83aa` (#1424), so every push carrying a `Blockchain/Dev/` path was refused. This unblocks it. Leg 14 goes from **8 passed / 1 failed (rc 1)** at develop's tip to **11 passed / 0 failed (rc 0)** at this head. The two run-id lines that cannot carry the guard's marker get a **narrow, structurally-bounded** exemption — not a file exclusion.

Refs KS-1450 · Refs KS-1451

## The defect, re-measured at develop's tip

The KS-1386 guard reported **8** unmarked slot-2 literals, all in `systemTest/schemathesis/config/schemathesis-baseline.json`, at lines **10, 11, 854, 859, 864, 869, 874, 879**. Reproduced by rebuilding the guard's forbidden set from `support/slot-expect.sh` (45 patterns = the guard's own want of 45, `SE_MAX_SLOT` 4 × (11 port families + 4 name shapes)). The line numbers had **not** moved since the ticket was filed, because neither squash since touched that file.

- Six are prose inside `accepted.*.reason` strings — those can take an inline marker.
- Two are run-id string elements in `$generated.from_runs`. A JSON string element cannot carry an inline marker, and renaming the ids would falsify the record of which sweep produced a row.

## What changed

1. **Baseline, the six `reason` lines:** each carries the guard's own marker, `slot-literal-ok: names the sweep's slot, not a target`. `$generated.from_runs` is **unchanged**.
2. **Guard, one extra filter stage in `scan()`:** matches only a **lone JSON string element** of the exact shape the baseline writes (`"(full|pre-merge)-…-slot<N>"`), in that **one** file. No file exclusion, no extension exclusion. A `"key": "value"` line, a `"reason":` line, a run id of any other shape, and every other file still scan normally.
3. **Guard, a new membership cell (+ its non-vacuity control):** every line the exemption drops must be a member of that file's `$generated.from_runs`, checked with `jq`. A line-based filter cannot tell `from_runs[5]` from a lone string in some other array; this cell can, so the exemption's scope is a **check, not a comment**. `jq` is required, not optional — a membership check that skipped silently would unbound the exemption exactly when nobody is looking.
4. **Both platform HTML docs** gain the **same one clause** naming the exemption's scope, in this commit, per `.claude/skills/secuura-test-discipline/SKILL.md` §4 (`:365` same commit · `:378` both files, every time · `:415` a changed gate must be reflected). D1 `:1268` bounded "No slot 2–4 value is typed anywhere"; D2 `:2169` bounded "never typed". Left alone, D1's sentence would be actively misleading, which is what `:379` is about.

## Test Evidence

**Touched:** `systemTest/__tests__/no_hardcoded_slot_literals.test.sh` · `systemTest/schemathesis/config/schemathesis-baseline.json` · the two `Projects Documents/*.html`. No `Blockchain/Dev/` path, no service, no frontend, no migration.

**Migrations + config:** none. No migration, no lockfile, no manifest, no OpenAPI spec, no env template. `$generated.from_runs` byte-unchanged.

**RAN — all on this head unless stated:**

| check | result |
| --- | --- |
| leg-14 guard at develop's tip, before any edit (RED) | rc 1 — `8 passed, 1 failed`, the 8 lines above |
| leg-14 guard at this head (GREEN) | rc 0 — `11 passed, 0 failed` (9 cells → 11) |
| full preflight by hand, hook's exact invocation | see the verbatim block below |
| `html_docs_matrix.test.sh` | rc 0 — 12 passed, 0 failed (10 of them its own controls) |
| HTML tag balance, measured separately | base and head both balanced (`<code…>`/`</code>` 1199/1199→1201/1201 and 759/759→761/761); my inserted fragment 2/2 in each; exactly **one** differing line per file; every other line byte-identical to base |
| `jq -e .` on the edited baseline | rc 0, with a deliberately-broken copy returning rc 5 so `jq` discriminates |
| `baseline_gate.load_baseline()` on tip vs head | 171 entries both ways, identical key set, exactly **6** differ, and the only change is `reason` gaining exactly the marker suffix |

**Arms — each tamper must red the guard with its own reason, restored from saved copies of the fixed files afterwards:**

| arm | expectation | result |
| --- | --- | --- |
| A0 untampered head | green | rc 0, `11p+0f` |
| A1 slot value in a **different key** of the baseline | red | rc 1, `10p+1f`, names `ks1450_arm_note` |
| A2 `from_runs` id of a **non-`(full\|pre-merge)`** shape | red | rc 1, `10p+1f`, names the planted id |
| A3 literal in an **ordinary systemTest file** | red | rc 1, `10p+1f`, names the probe file |
| A4 lone provenance shape in **another array** | red | rc 1, `10p+1f` — caught by the **jq membership cell only** |
| A5 marker with an **empty reason** | red | **GREEN — see the named limitation below** |
| A6 marker removed from `:859` | red | rc 1, `10p+1f`, names `:859` |
| A7 the **exemption stage itself** removed | red | rc 1, `10p+1f`, **2** lines (not 8 — the six reasons now carry markers), so the exemption is load-bearing |
| A8 `jq` broken by an exit-127 shim | red | rc 1, refuses, never a silent pass |

Every red arm reads `10p+1f`: one cell, the tampered one, so none is a load failure rather than a tamper.

**NAMED LIMITATION — A5, and it is pre-existing, not introduced here.** The guard's marker test is `grep -vE 'slot-literal-ok:[[:space:]]*[^[:space:]]'`, i.e. "one non-whitespace character after the colon". On a `.ts` line a bare marker sits at true end-of-line, so nothing follows and the line is correctly reported. **On a JSON line the value's own closing quote follows it**, so ` slot-literal-ok:",` satisfies the test and the line is exempted. Driven both ways against the same regex:

```
  "reason": "x 6982 slot-literal-ok:",      -> EXEMPTED   (wrong: the reason is empty)
const p = 6982; // slot-literal-ok:          -> reported   (right)
```

That contradicts `systemTest/CLAUDE.md:1169` ("a bare marker exempts nothing"). It is **not** a regression from this PR: the baseline carried **zero** markers before it (`git show HEAD~1:…baseline.json | grep -c slot-literal-ok` = 0), so this is the first change to put a marker inside a JSON string and the first place the gap becomes load-bearing. The same `\s*\S` shape exists in at least four other harness guards. **Filed as KS-1451** rather than fixed here, because a one-guard tightening would make the five guards disagree about what a bare marker means. Measured blast radius of the eventual fix: exactly 2 existing marker lines repo-wide, neither of which needs its exemption.

**NOT RUN, and why:**

- **The Schemathesis package's own pytest suite.** `pyproject.toml:18` is `requires-python = ">=3.14.8"`; this host is **3.14.5**, so the floor is not met, and the venv is built by `python3 scripts/run.py setup`, which needs Docker and mints an API token. Run instead: the baseline's **real consumer**, `scripts/runner/baseline_gate.py` (stdlib-only), per the table above.
- **Preflight legs 3, 4 and 8** — the local Docker stack was not up. Named by the preflight itself.
- **The guard's behaviour under a `jq` older than `--arg`/`index`** — not probed; `jq` presence is asserted, its version is not.

**The full preflight, verbatim — and it is explicitly NOT a pass:**

```
shell suites: 71 passed, 0 failed, 0 skipped (of 71)
shell suites wall-clock: 346s

PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```

Leg 14 inside that run: `no_hardcoded_slot_literals: 11 passed, 0 failed`. **No other leg newly red vs develop:** develop's own recorded figures (KS-1450's body, same machine) are rc 1, shell suites **70 passed / 1 failed** / 0 skipped (of 71), `PREFLIGHT FAILED on leg(s) 14`, **12/15 legs ran** — the same 12 legs and the same 3 stack SKIPs, and the one failing shell suite is the one this PR fixes. S-1 install first: `npm ci` in `Blockchain/Dev`, 1937 packages, both leg-1 artefacts present.

**What the pre-push hook printed on the push — and it corrected an assumption of mine.** I expected the hook to skip the preflight, because this commit carries only `Projects Documents/` and `systemTest/` paths and **zero** `^Blockchain/Dev/` paths. It did **not** skip. On a first push of a new branch there is no computable base, and the hook fails *safe* rather than open (its own `:104-108`), so it printed `[pre-push] Blockchain/Dev changes detected → running preflight gate` and ran the whole thing. Its result, independently of my two by-hand runs:

```
[format-gate] systemTest/performance — format:check OK
[format-gate] 1 package(s) checked, 0 skipped, 0 failed
shell suites: 71 passed, 0 failed, 0 skipped (of 71)
shell suites wall-clock: 340s
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
```

Leg 14 in the hook's own run: `no_hardcoded_slot_literals: 11 passed, 0 failed`. So this head has now been through the full preflight **three times** — twice by hand (the second after the doc amend) and once in-hook — with the same verdict each time.

**The first push attempt was REFUSED, and the refusal was correct.** `[format-gate] NOTHING CHECKED — every selected package was skipped, so no file's formatting was examined` / `SKIP — systemTest/performance deps not installed`. The gate declined to pass vacuously, which is exactly right. Fixed by `npm ci` in `systemTest/performance` (270 packages) and pushed again — **not** bypassed with `--no-verify`. Second attempt: `1 package(s) checked, 0 skipped, 0 failed`.

## Known neighbour

**#1383 (KS-1401) is held and also edits both platform HTML docs**, so it is a known doc-conflict neighbour of this PR. It is not mine and was not touched. Its conflict with develop pre-dates this round (measured by a previous seat: `merge-tree` rc 1 against the current develop, the pre-#1423 develop, and #1423's own base alike).
