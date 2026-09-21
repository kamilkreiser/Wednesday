# REPORT — Ornith FEED 3: the next briefs from `night/candidates.md` (easy -> hard), inputs built + golden-prechecked, queue PROPOSAL
Drafter subagent (commissioned by Wednesday, `2026-09-22_ornith_feed3.COMMISSION.md`). Written 2026-09-22 02:10:16 AEST. Files only — nothing appended to `night/queue.md`, `night/candidates.md` / `candidates_rounds.md` / `PAUSE_QUEUE` untouched, nothing under `!CODING/` touched, no runner launched, no mail, no Linear/GitHub write.

## 0. SLIPS (first, by rule)
1. **Two briefs, not ~12.** The commission targeted ~12; the pool does not hold them. Of the 37 T1-T4 rows (26 + 5 + 5 + 1), 35 are decision-class, features, diagnosis tickets, multi-file, or blocked (the SKIPPED table in the proposal names each in one line, in the ticket's own words where it has them). The census's `[resolved:basename/route, a HINT]` rows are MENTIONS of a file, not edit targets — 9 of the 26 T1 rows carry that tag and none of the 9 briefed. Round note for `candidates_rounds.md` (Wednesday writes it — not my file): a census row that would survive a "fix spelled out AND one file AND no decision offered" predicate is the briefable subset; measured here it is 2 of 37 (KS-947, KS-1265), plus KS-1239 which is one file and spelled out but a measured cross-package trap (slip 5).
2. **My first KS-947 tamper line was off by one** (`Line: 1019`; the users mount's `standardHeaders` line is :1020 — I read a `cat -n` offset listing and mis-added). The builder refused it (rc 2, the From/tip mismatch named) before any golden ran; fixed in the brief (4 sites) at 01:59.
3. **My first KS-947 golden FAILED T6[F4USERS]** — the F3 option-set cell redded under the F4USERS tamper too, because the tamper's trailing `// TAMPER: ...` comment reads as an option key `TAMPER` to my `optionKeys` helper (F4AUTH did not show it: its comment sat on the AUTH mount, and the cell only reports keys the USERS mount has that the auth mount lacks). Fixed on both sides: `optionKeys` now drops `//` line comments (a real mount comment would otherwise false-red the cell — a robustness gain, not just a golden fix) and the three tamper comments carry no colon. Second golden PASS 8/8. The brief carries a "Golden precheck fix" premise bullet saying so. This is exactly the defect class the golden method exists for; it is still a slip in a design I authored.
4. **I made THREE outbound connections, not two:** `git ls-remote` (the checkout's own ssh road, allowed), the read-only Linear GraphQL read the commission allows — done TWICE (one POST for the 38 T1-T4 candidates at 01:52, one POST for 8 T5 rows at 02:1x) — and a THIRD Linear POST made by `night/build_input.sh` itself for KS-1265 (the code_patch builder reads the ticket; the commission names that builder, so the call is inside the allowance, but it is a call I did not make by hand). No GitHub REST call was made (KS-1265 has no attachment; the build log carries no PR-state line). The key was read by NAME into a local variable in `feed3/linear_read.py` and by `build_input.sh`'s own `source`; never echoed, never written: a `grep -c` for the key's prefix = 0 over every output file (§5).
5. **KS-1239 looked like the easiest brief on the list and is a trap; I nearly wrote it.** A one-line dead-code deletion at `index.ts:347` (with its 10-line comment) shifts every line below by -15, and `packages/shared`'s ks781 test pins `services/api-gateway/src/index.ts:845/858/891` BY LINE NUMBER (:2024-2026 at 64ab10513 — measured, not inherited from KS-953). The code_patch checker's A6 runs only the api-gateway suite, so Ornith would PASS and the PR would redden another package (KS-953's third instance). Skipped with that reason; it is a two-package change for a Claude seat.
6. **Files written outside the named deliverables:** (a) a run directory under the WEDNESDAY tree, `local-model/runs/2026-09-22_feed3-drafter-precheck/` (the FEED 2 precedent: harness copies + per-row logs); (b) a BUILD-FACING COPY of the KS-1265 brief at `night/briefs/r16_KS-1265/KS-1265.md`, byte-identical (sha256[:16] `0fbc70e0a4412cc4` both), because `build_input.sh` reads `NIGHT_BRIEFS_DIR/<id>.md` and the R16 naming puts the brief at `KS-1265-R16-EARLYGUARD.md`. Two copies is a drift risk: the `# build:` line reads the copy; if Wednesday edits the brief, the copy must be re-copied (or the build line pointed elsewhere). Candidate harness fix, not built: let `build_input.sh` take `brief=<path>` like the test_only builder takes the brief path positionally.
7. **KS-1265's shape deviates from the ticket's verb.** The ticket says "Move the issuerName check above the save"; the brief INSERTS an early guard and LEAVES the late guard (:836-841) in place, unreachable for an "@" value. Reason: the late block's message line :839 carries a non-ASCII em dash that a `-` line would have to reproduce byte for byte (the KS-1133 / KS-1180 escape class); the outcome the ticket asks for ("a refused create writes nothing") is met and golden-proven. Stated in the brief header, the proposal line and here; Wednesday may veto.
8. **Nothing else.** Source checkout: `source tracked-modified after: 0` in both prepare logs; `count-objects -v` identical before/after (§1). No file deleted, renamed or overwritten; the two briefs are new files (checked `-e` before writing); every stamp from `$(date)`.

## 1. Tip, clone, hygiene
- Tip pinned: `64ab105132eada0621622acf4d6053bc59926780` by `git ls-remote origin refs/heads/develop` at **01:51:57 AEST** (== local `refs/remotes/origin/develop`; commit 2026-09-22 01:03:33 +1000 "KS-1156 A3: comment-only - the mount-shape comment's count and its arrows (#1146)"). The commission's 01:46 reading was the same sha — develop did not move during this session's reads.
- Clone: `git clone --shared --no-checkout` + `checkout --detach 64ab10513` from `feed3/clone.sh` into `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/b24cb7de-7a4a-4dad-80d5-bd3b1a9cc168/scratchpad/feed3/clones/bc` (rc 0). Read verbs only on the source checkout.
- `count-objects -v` on the source checkout, BEFORE (01:50:57) and AFTER (§7): identical — see §7 for both verbatim.
- Harness: `local-model/runs/2026-09-22_feed3-drafter-precheck/golden_one.sh` (test_only: build into the drafter scratchpad -> `mk_golden.py` (the feed2 copy with the new-file header fix) -> `tasks/test_only/prepare_clone.sh` -> `tasks/test_only/checker.sh`) and `golden_code.sh` + `mk_golden_code.py` (code_patch, NEW this feed: the brief is copied to a scratch briefs dir as `<id>.md`, `night/build_input.sh` builds the input, the golden out.md = the brief's product fence + test fence under `--- a/` / `+++ b/` headers, then `tasks/code_patch/prepare_clone.sh` + `checker.sh`). Per-row logs under `<TAG>/` (`build.log`, `mk_golden.log`, `out.md`, `prepare.log`, `checker.log`, `out.md.checker/`); batch logs `golden_947.log`, `golden_1265.log`.
- Key sets (the 09-20 rule, `feed3/logs/keyset.log`): `test_only_947F3F4-R16.json` vs the newest PASSING test_only input `test_only_1229VERSIONTRIM-R15.json` (done 01:13): set(good)-set(mine) = [] and set(mine)-set(good) = []; `code_patch_1265EARLYGUARD-R16.json` vs the newest PASSING code_patch input `code_1234.json` (done 09-20 22:49): both deltas []. Neither code_patch input carries a `task_type` key (the same as the comparator) — the `task=` pin on the queue line routes it.
- Board read (read-only, two POSTs, `feed3/tickets.json`): all 38 KS candidates of T1-T4 are Backlog/Todo, none on Peter/Stuart, none archived, none with a PR attachment. The `PS-*` rows the number filter also returned (PS-746/789/837/851/915/934, Stuart's, Done/In Review) are a number collision in another team and were ignored.

## 2. Method per brief
Read the ticket (board) and the file(s) at the tip in the clone; decide the task type by the `tasks/*/task.md` contract (test_only when the product is right at the tip and the ticket asks for a pin; code_patch when the ticket spells a one-file fix); write the brief in the skeleton's shape with ASCII-only, backslash-free `+` lines, non-blank context, trailing context on insertions, LITERAL rendered cell titles, tampers by LINE at the tip with their reds stated and reachability argued; build with the task's own builder into the scratchpad (rc 0); golden = the brief's own fence(s) as the model output through the harness checker in the clone; a golden that does not PASS is a brief defect (fixed once, KS-947; never proposed otherwise).

## 3. Per-row table
| # | ticket | brief file | task / mode | tampers -> reds / controls | builder rc | golden verdict (tag under runs/2026-09-22_feed3-drafter-precheck/) |
|---|---|---|---|---|---|---|
| 1 | KS-947 (T1 P2, Backlog) | `night/briefs/KS-947-R16-F3F4.md` (13,325 B, sha256[:16] `1959286d5311211e`) | test_only, MODIFY IN PLACE of `services/api-gateway/src/__tests__/ks733-users-mfa-rate-limit-mount.test.ts` (99 -> 161 lines; one hunk `@@ -96,4 +96,66 @@`, 62 '+', 0 '-'); Runner pinned vitest | 3 tampers on `index.ts`: F3SKIP :1020 -> 1 red; F4AUTH :993 -> 2 reds (the new F4-auth cell + the EXISTING PARITY cell); F4USERS :1018 -> 2 reds (F4-users + PARITY) / 4 controls (order, spec-walk, window, the file's existing CONTROL) | rc 0 (after the :1019 -> :1020 fix, slip 2) | `947F3F4-R16`: **PASS 8/8**, T3 strict, T5 10/10 cells, T6 exact x3, T7 x3, T8 restored x3 (first golden FAIL T6[F4USERS] — slip 3 — fixed, re-run PASS) |
| 2 | KS-1265 (T3 P3, Backlog) | `night/briefs/KS-1265-R16-EARLYGUARD.md` (8,041 B, sha256[:16] `0fbc70e0a4412cc4`; build-facing copy `night/briefs/r16_KS-1265/KS-1265.md`) | code_patch, originate (jest): ONE insert-only product hunk `@@ -614,3 +614,11 @@` in `routes/documents.ts` (8 '+', trailing context :614-616) + ONE test hunk `@@ -141,11 +141,8 @@` MODIFYING `__tests__/ks549-documents-create-issuer-name-persist.test.ts` (test_file= pin; 4 '+' / 7 '-'); ref= ks1228 | no tamper (code_patch): 1 declared red cell (`## Red cells`, the ks549 file's existing '@' cell tightened to 400 + saveDocument x0) / 3 existing cells as controls | rc 0 (188,780 B input, ~47k prompt tokens at ctx 65536) | `1265EARLYGUARD-R16`: **PASS 7/7** — A2 strict, A3 two files, A3c 8/8 '+', A4 red-first 1 failed / 4 run (assertion; controls green), A5 4/4, A6 whole originate suite no NEW red, A7 tsc rc 0 (baseline rc 0) |

Counts (python `len`): briefs written **2**; goldens **PASS 2 / FAIL 0** (final; 1 interim FAIL on KS-947, fixed); inputs built **2** (rc 0 x2); skipped **36** rows named in the proposal's table (35 of T1-T4 + KS-1227 as the commission asked, plus one T5 line covering the 3 T5 rows read); T5 rows not read: 27.

## 4. Skipped — top three reasons (the full table is in the proposal)
1. **Decision-class by the ticket's own words** (14 rows): KS-678, 953, 955, 1168, 1190, 1222, 934, 1163, 1245, 630, 1263, 1189, 1262, 1231 — "pick one", "decide", "the owners decide", "not chosen".
2. **A feature / design / diagnosis, not a patch** (10 rows): KS-579, 581, 627, 746, 758, 915, 784, 837, 1084, 1019.
3. **Multi-file or cross-package** (7 rows): KS-987, 1197, 759, 965, 851, 748, and KS-1239 (the measured ks781 line-pin trap). Then: blocked by infrastructure (KS-1145 needs :5432), two rounds already failed (KS-789, the KS-1227 class), a test file as the product (KS-1143), an unverified generator quirk (KS-1287), a 4-item ticket whose only spelled item is label-only polish (KS-998), a doc ruled "do not edit yet" (KS-986).

## 5. Secrets and connections
- `grep -c` for the key's prefix over `feed3/logs/linear_read.log`, `linear_read_t5.log`, `tickets.json`, `golden_1265.log`, `1265EARLYGUARD-R16/build.log`: **0** each (the Linear key's prefix). Positive control for the grep: the key's NAME `LINEAR_API_KEY` occurs in `linear_read.py` (the regex that finds it by name) — the grep sees text.
- Connections: `ls-remote` x1 (01:51:57), Linear GraphQL POST x3 (two by `feed3/linear_read.py`, one inside `night/build_input.sh` for KS-1265). No GitHub REST, no `:5432`, no `nc`/`curl`. The vitest/jest cells the checker ran opened loopback listeners on ephemeral ports inside the harness (the tests' own express apps) — harness-internal, as in every night run.
- No Datasec file or mail touched.

## 6. NOT MEASURED
- **No model run.** A golden proves the brief is gradeable at the tip; it says nothing about Ornith reproducing 62 '+' lines inside an existing describe (KS-947) or a two-file diff whose product hunk is INSERT-ONLY (KS-1265 — the KS-747 / KS-976 09-15 class: "an insert-only hunk with no '-' line ... is the hunk it omits"; A3c will refuse the omission by name, so a miss is classified, not silent). The `--recount` header dialect is untouched by anything here.
- **KS-1265's "0 provenance rows"** is argued from :711 (`recordActionProvenance` only `if (onBehalfOf)`, and the cell sends none), not asserted by a cell.
- **The ks733 file's four existing cells** were run only through the golden (T5 10/10, T6/T7 per tamper) — no separate vitest run of the api-gateway suite; test_only's checker has no A6/A7 twin, so `tsc` over the modified test file was not run (the file's own `?.[1]` and `Set<string>` idioms already exist in api-gateway tests; not proven here).
- **Ticket states** were read once at 01:52 (T1-T4) and 02:1x (T5); a lane taking a ticket after that is Wednesday's re-derive.
- **KS-1287** was not tried against the generator; **KS-998 item 4** was not attempted; **the 27 unread T5 rows** may hide a one-file fix the census's two-file resolution masked.
- **The build-facing copy** (slip 6) is checked byte-identical NOW; nothing re-checks it after an edit.

## 7. count-objects (verbatim, source checkout `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files`)
```
Tue 22 Sep 2026 01:50:57 AEST
count: 8738
size: 58724
in-pack: 101422
packs: 47
size-pack: 297855
prune-packable: 435
garbage: 0
size-garbage: 0
--- AFTER (filled by the final step) ---
Tue 22 Sep 2026 02:10:30 AEST
count: 8738
size: 58724
in-pack: 101422
packs: 47
size-pack: 297855
prune-packable: 435
garbage: 0
size-garbage: 0
```
diff of the two count blocks (date lines excluded): IDENTICAL
