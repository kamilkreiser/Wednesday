# B1744 commission — MPS Calculator: which v13.4.1 tickets are BUILDABLE NOW under C-45, in lanes (read-only sweep)
Commissioned by Tuesday (s293), 2026-11-19. Model: Sonnet (routing row C8). You write ONE document; you change nothing.

WHY: today's sweeps excluded 35 MPS tickets as "waiting on customer-facing words". Drafter B of the decision pack
(`2026-11-19_B1742_decision_pack/B_REPORT.md` and `MPS_words_pack_v13-4-1.md`: read both whole) found there is no words
pack to approve because the standing process is different. Tuesday read the ruling at source: the project's
`1_Project_Definition/CLARIFICATIONS.md` entry C-45 (heading line 654), the product owner's 2026-10-20 acceptance of all
15 recommendations of the v13.4.1 build plan, option a detail, verbatim: "Lanes start in waves as soon as you tap. Every
new customer-facing word still comes to you as a word pack before it ships, and nothing is deployed without your card."
So a lane may be BUILT and its words go to him as a word pack BEFORE IT SHIPS; the words do not block the build.
Kam, 2026-11-19 16:26:43: "keep working on other outstanding tickets and the backlog."

Output: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-19_B1744_mps-v13-buildable-lanes.md`.
Project: '/Volumes/Datasec_DEV/!CODING/Datasec/Datasec MPS Commercial Calculator' (Jira MPSCALC; repo
datasecau/MPS-Commercial-Calculator; its local `2_Project_Files` checkout is STALE: read code at origin main by
`gh api ... contents?ref=<sha>` or a tarball in your scratch, and print the sha).

DO:
1. THE RULE, both directions. Quote word for word, with line numbers, C-45 whole (all fifteen D-rows), C-44, C-109,
   C-116 and every later entry or ruled card that narrows or widens what a v13.4.1 lane may do before the product owner
   sees its words: may it be built? merged to main? Is "ships" the hosted deploy, or the merge? Find how the lanes that
   ALREADY landed under C-45 handled it (which landed with new words on main and a word pack sent after: name the pull
   requests and the pack). C-116 is said to hold "every contract change until you approve the exact name": list which
   tickets that stops. State the rule you conclude and what is NOT settled.
2. THE BUILD PLAN. Find the v13.4.1 build plan and gap analysis (the 12 planned lanes, V2 to V11 and others) in the
   project folder or Tuesday's briefs, and state per lane: built and landed (pull request), partly built, not started.
3. THE TICKETS. For each of the 35 (121 129 130 139 154 156 161 169 194 233 237 243 246 264 265 267 268 270 271 272 273
   274 275 276 277 278 279 280 281 282 283 286 287 368 402) and any other open v13 lane ticket you find: status; what it
   asks; whether main already does it (read the code); whether the words it needs exist as source text (the reviewer's
   prototype, list W, an earlier approved pack) so a builder can use them unchanged and list them for the word pack, or
   are NOT drafted anywhere (then the build needs words nobody wrote: not buildable, say what is missing); whether it
   needs a ruling of its own, outside data, or a contract name (C-116); its unbuilt predecessors.
4. LANES. Group the buildable tickets into lanes that share no file (name the files, read at main), in dependency
   order, at most 6 lanes in a first wave; per lane: keys, files, size, gate tier guess, the words it will introduce
   (count and source), what would STOP it, and whether two lanes can run at once (does MPS have a shared test lock or a
   shared counts file? read the project's CLAUDE.md and a recent MPS builder kit, e.g.
   `2026-11-19_B1741_SEAT-M163_mps-lane-mg-accepted-wording.md` and a larger one from 11-11 to 11-16 found with ls).
5. Say plainly if the answer is "few or none are buildable" and why. Check drafter B's claims in both directions.

RULES: read-only everywhere except the output file and scratch
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s293/d1744/`. Jira GET only (JIRA_BASE_URL, JIRA_EMAIL,
JIRA_API_TOKEN by name in-process from the project's `4_Credentials/.env`, never printed); gh `-X GET` only under the
project's own GH_CONFIG_DIR; git read verbs only. NEVER read `.local/`, `Source_Documents/**`, any price book or real
price store of that project. Nothing of HPSM-POC or any other project is read or named. No az, no request to any app
host, no mail, no build, no test run, no server; `decision_queue.sh` only with `show` and `list`. No `cd`; no unquoted
word starting with `=`; zsh; absolute paths; never delete; clocks from `date`; every zero with a positive control;
counts through `2_Project_Files/fleet/board_count.sh`. ASCII; built whole, temp file, os.replace. End with
FOUND / TESTED (and NOT tested) / HOW.
First line of your reply: `MPS-V13: <n> buildable keys in <m> lanes` or `MPS-V13: nothing buildable - <why>`.
