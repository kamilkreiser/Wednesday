# B376 DRAFTER REPORT (read-only drafter, 2026-10-21, clock from `date`: 06:45:21 at the last read before drafting)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-21_B376_SEAT-G31_mps-pr93-gate-tier1.md` (104 lines; tier 1, routing row G1, Opus, `BRIEF_SEAT_LEVEL=opus`, pane `Datasec/MPS-G31`, STATUS `…/1_Project_Definition/Briefs/2026-10-21_B376_STATUS.md`, no ports, MERGE line and "nothing deploys" carried). Two stamp slots (main sha; head + stamp time + launch authority), each once: the slot count reads 2 now (checked by `grep -o -E '@[A-Z_]+@' | wc -l`). Last line is `READ-WHOLE-BY-TUESDAY: PENDING`. **Not created: the `.pre-stamp` copy** (outside my two-file fence): Tuesday must `cp` the brief unchanged to `…B376_SEAT-G31_mps-pr93-gate-tier1.md.pre-stamp` before stamping, or the gate's slot-count control cannot fire.

## Reads
B365 brief (110 lines, whole, the shape); builder STATUS `B373_STATUS.md` (178 lines, whole); builder brief `B373_SEAT-W23_mps-289-292.md` (128 lines, whole); `B318_STATUS.md:335-365`; `model-routing.md` G1/G2 rows (grep); `models_latest.json` `levels.opus.model_id` = `claude-opus-5-5` (grep; the brief tells the gate never to type an id); the B324 tier-1 brief's model line (grep: launch carries no level var there, because `brief_seat.sh` defaulted to opus; this brief sets `BRIEF_SEAT_LEVEL=opus` explicitly as you asked, harmless).

## Facts: all of the PR facts (head `a3cfda72…`, base `1eccbc8b…`, ahead 1 / behind 0, 4 files and their +/-) are TUESDAY's 06:45 measurements, stated as such. I measured nothing against the repo, PR, Jira or CI.

## Built into the brief beyond the B365 shape (tier-1 weight)
- r2 red-at-base/green-at-head re-run by the gate's own copy of the head test files over base src (expect 3 red / 9 green).
- r3 property sweep: base body inlined as oracle, rebuilt by the gate from `git show <base>:…` (not from the brief); exhaustive grid (lengths 0-140 x pair at every index, incl. ASCII, BMP, two-pair, whitespace-only), 200k seeded random sources incl. lone surrogates, an independent "longest prefix not splitting a pair" oracle, and three controls (harness vs itself at base = 0 diffs; planted off-by-one flagged; predicted split-pair count equals observed diffs).
- r4 builder's m1-m4 plus own n1-n10 (index shifts, `||`, step 2, fitting-limit edges, only-length-96, high-only mirror, null branch, no-suffix branch); each survivor needs an equivalence argument plus reachability through the create path.
- r5 in-process HTTP: create/duplicate/GET under both hosts, raw-byte strict UTF-8 decode, explicit body quoteRef, create rule 100/101 at base vs head, raw lone-surrogate create bodies (closes the builder's "one of six lines lost").
- r6 where `quoteRef` is printed/cut/encoded (grep over src, web/src, docs, tests) plus the proposal path proven in process.
- r7 docs sentence truth, including that "split a character" over-claims against a pair-only rule (combining marks/ZWJ stay out of scope, said as such, not a defect).

## What I could not verify (UNMEASURED by me)
1. The code at the head (`CopyRef` body, the 99-line `CopyRefTests.cs`, the +29 in `V0Duplicate.cs`, the docs sentence): every description is the builder's, RELAYED. I did not open the PR diff.
2. PR #93 number, state, draft flag, commit count, title/body (Tuesday gave head/base/files; the PR number and `mergeable` are not in my facts, and the "+140/-3" total is my arithmetic from per-file counts, flagged UNMEASURED in the brief).
3. Whether `b373/copyref-surrogate-289` is the PR's branch name (taken from the builder STATUS), and `refs/pull/93/head` being listed.
4. `AGENTMAIL_API_KEY`, the machine load, tmux panes, `.tools` contents (no `b376` entry check), heavy slots.
5. Whether the create path's 400 for lone surrogates comes from the contract binder or the product `Validate` (the builder says binder text; r5(8) asks the gate to read it).
6. Where `quoteRef` is printed besides `Proposal.cs:430/565` (builder said `:67` is a field-map entry), and whether any web view slices it (r6 is the gate's).
7. Line numbers in `QuoteEndpoints.cs` after the PR's +9 lines (the brief says to re-read).
8. Whether the Import 156 / Engine 394 / Api 1811 totals hold (builder's own run only).

## Questions for Tuesday (each with a recommended answer)
1. **Launch timing:** load1 was 6.4-7.9 at the builder's runs; the gate waits for under 8 by itself. Launch now? Recommend: yes, the LOAD rule governs.
2. **Stamp slot 2** holds head sha + stamp time + authority + answers in one slot (per your "@MAIN@/@HEAD@" instruction). Fill it with the head sha you measured (`a3cfda72…`) and a named authority (Kam board 2026-10-20 18:55:31 item 3 + 08-12 morning autostart grant, as B373 used). Recommend: yes; the REFUSE check refuses a stamp that names no authority.
3. **Make the `.pre-stamp` copy** before stamping (my fence forbade it). Recommend: yes, `cp` unchanged first.
4. **m3 survivor handling:** brief rules Note when the input is unreachable (create path 400), Minor when reachable but base-identical, Major only if U+FFFD reaches a user. Accept? Recommend: yes; it never yields NO GO on m3 alone unless a reachable user-visible defect appears.
5. **Docs wording ("one unit fewer when the cut would split a character")** over-claims for combining marks; the brief makes it Note if wording only, Minor if it asserts behaviour the code lacks. Accept? Recommend: yes.
6. **Sweep scope:** 200k random + the exhaustive grid is heavy-ish for one in-process test; recommend keeping it (string work only, seconds), run in one slot.
7. **CodeQL pending at verdict:** use the conditional-suffix rule (suffix on first and last line, 45 minutes polling)? Recommend: yes, as written.
8. **Landing text:** PR body unread by me; recommend leaving the missing-ticket-key check to the gate as Minor at most (r12b).
9. **`BRIEF_SEAT_LEVEL=opus` explicit** (as you specified) versus omitting it as the B324 brief did. Recommend: keep explicit, it is the safer form.
