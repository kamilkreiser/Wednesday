# B283 DRAFTER REPORT (read-only drafter, 2026-10-19)

Brief: `2026-10-19_B283_SEAT-G9_hpsmpoc-gate-pr161-round2.md` (round 2 of 2 gate for HPSMPOC-291, PR #161 @ 7329804, tier 2, Sonnet). Structure copied from B279 (REFUSE, LOAD, PINS, objects/worktrees, charter, HOLDS, VERDICT, slots). Read: B279 brief and STATUS, B282 brief and STATUS. Nothing else read; no tool other than Read and Write used; no git, gh, Jira, HTTP, az, docker or dotnet run. Every sha, count and line number in the brief is RELAYED from B282/B279 STATUS and marked for re-measurement by the gate.

## Slots (the brief carries 8 tokens; each appears once in the header or REFUSE line)
| Slot | Default / source |
|---|---|
| `MODEL` | `claude-sonnet-5-5` (launched with BRIEF_SEAT_LEVEL=sonnet; brief_seat pins Opus, so Tuesday `/model`-switches after launch, or the STATUS says which ran) |
| `STAMP_TIME` | Tuesday's clock at stamping, `YYYY-MM-DD HH:MM AEDT` |
| `PANE` | `Datasec/HPSM-POC-G9` |
| `PANE_SUFFIX` | `G9` |
| `PORT_BLOCK` | `7210-7219 (none expected)`. DRAFTER GUESS: B279 used 7190-7199, B282 7200-7209; confirm the next free block |
| `CODE_MAIN_SHA` | `befd45e77b391467a1313af8b7b5e0fc580f7b63` (RELAYED; re-read by ls-remote at stamp) |
| `HEAD_SHA` | `7329804e7b31d5fd8a84de9056ed81731d2ba859` (RELAYED; re-read by ls-remote at stamp) |
| `B_NUMBER_CONFIRM` | `B283 confirmed` after a folder check for B283 hits |

The brief names the SHAs literally as well as in slot form, so a stamped copy and the `.pre-stamp` copy both carry them; if the head moves before launch, edit both places.

## Design choices
- Scope is round 2's one commit plus carried rows (r0..r7 mirror the task's list). -227 is excluded and said so; r0 keeps a byte-equality control on the 3 specs.
- The first-round fixture probe is reused (19 versions x pin 10.0.13) with extra cells for the new helper (`10.0.9999.0`, `10.0.10000.0`, `10.1`, `10.1.0.0`, `11.0.26.1`) and two extra pins, because the signature now takes the pin.
- Mutants: the task's a1, a4, a5 and Major.Minor-drop, plus Major-only / Minor-only / constant-10.0 variants, the b1-b3 third-branch mutants, and the still-red a2, a3, m291, m291b.
- Added four traps beyond the task: T-a partial RED at the round-1 helper (builder admits only 2 rows red), T-b honesty of the direct-helper Fact for `>= 0`, T-c per-sentence classing of the new comment (m3/m4a/m4b are cited to B262, not measured), T-d the stale row comments at `:208`/`:231`.
- Round-cap wording: a NO GO goes to Tuesday and Kam, not to a round 3.

## Top doubts
1. Port block is a guess (see slots); no server is needed, so low harm.
2. The builder's line numbers (`:181-189`, `:139-141`, `:279-305`, `:308-320`) and the "added 6 names" count are RELAYED only; the brief tells the gate to re-read them.
3. B282 says it did not post-amend or rewrite `7c87bdf`'s message, so the stale round-1 sentence remains there by design; the brief records this as a known note, not a finding. Tuesday may prefer it as a Minor.
4. The brief is about 70 dense paragraph-lines rather than 75 short ones, because the B279 shape uses long lines.
