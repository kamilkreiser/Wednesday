STARTABLE: NO (as drafted). PCOMP-42 is dropped; PCOMP-44 becomes startable when Tuesday fills two Stamp slots (Q2 sentence or NONE, Q3 status/code). Under the Q2 default (b) the kit is not launched at all.

# B1001 drafter report (claude-sonnet-5-5, 2026-11-01 about 01:2x-02:1x AEDT, read-only)

Kit: /Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-01_B1001_SEAT-J36_composer-pcomp42-44.md

## BLUF
1. PCOMP-42 cannot be built without new words, and its own dependency is unbuilt. Dropped from the lane.
2. PCOMP-44 is bigger than the sweep said: not "one line in renderers" but five code places (contract, renderer union and set, stored-output map, web exhaustive record with a pinned test, generated openapi/schema files). All are keys, no words, EXCEPT one thing: the API's answer to a request for the two kinds before renderers exist. No existing sentence is true (existing refusals say "no signing key" or "no earlier release"); left alone it is a 500 INTERNAL on a contract-valid request. That is one new refusal sentence = a words card (C-95, C-71). Hence Q2.
3. Migration number: the next free is 0028, but this lane writes none (PCOMP-44 needs no migration; 0028 is reserved for the future PCOMP-42 lane).
4. Nothing is already built: sm_policy_json 0 files, sm_policy_csv 0 files.

## Facts re-measured (instrument; control)
- Main `075b2b232b1501361b78bca362095ea969c04c3b` (`gh api -X GET commits/main` = `git/ref/heads/main`). Project checkout is stale (`origin/main` d70edf70; `cat-file -t 075b2b23` fails). `compare d70edf70...075b2b23`: 1 commit, 2 test files only, so source reads at d70edf70 (local `git grep`/`git show`) hold for the lane's paths.
- Migrations: `git/trees/main:packages/db/migrations` lists 0001..0027 (last `0027_audit_event_entity_index.sql`); `.../rollback` lists 0019..0027 (9 files). Control: 0025 name printed. No open PR touches packages/db; `git/matching-refs/heads/b1001` length 0. Tickets' `0022_*` is stale (0022 is exception_review_and_scope).
- Existence: `git grep -l -i` at d70edf70: sm_policy_json 0, sm_policy_csv 0. Controls: change_report_pdf 20 files, attribute_override 44 files. The bare token `sm_policy` hits 10 files, all `hpsm_policy...` substrings (a word-bounded scan prints 0): the kit warns the builder off that false hit. after_validation: 3 test files (attribute overrides, a different feature); controlled_staged, remediation_state: 0.
- Jira GET (jira791.py `get`, in-process creds): PCOMP-42 and PCOMP-44 both Backlog, 0 comments, last updated 2026-10-23, no links. Control: PCOMP-999999 HTTP 404. Neither has a "Done-when" paragraph; the Done rule is C-111 (3) at CLARIFICATIONS.md:2049.
- Rulings quoted with file:line (1_Project_Definition/CLARIFICATIONS.md): C-91 :1671-1677 (K5 a; "L3-4 also waits on L2 (not built)" at :1677; migration number is Tuesday's call at :1676); C-95 :1715-1719 (words card per lane, "nothing ships"); C-71 :1286-1289 (new words before any demo deploy); C-88 :1635-1640 (L7 needs "L3-6 (the contract output kinds)"); C-101 :1799 (landing rule); C-111 (3) :2049; C-112 :2046; deploy only on the product owner's card :1804, :1869.
- Code (d70edf70): contract `OUTPUT_KINDS` document.ts:284-297 (12 kinds; CONTRACT_VERSION 0.37.0 at :122); renderers `OutputKind` model.ts:227-239 and set render.ts:107-120; apps/api/src/outputs.ts:33-37 forces contract==renderer both ways; `STORED_OUTPUT_KINDS` Record<StorableKind,...> exhaustive (stored-outputs.ts:16-34); web `KINDS: Record<OutputKind,true>` exports.ts:19-31 and exports.test.ts:41-44 asserting every kind sits on a card and the list length is 12; app.ts:173-205 maps unclassified errors to 500 INTERNAL; no handler names RenderRecordError. PCOMP-42 side: 0025 CHECK at line 29 (designed to be widened), document.ts:842/871, answers.ts:38-42, projection.ts:102-106, discovery-typing.ts:261, resolve.ts:93 exhaustive REMEDIATION_RANK, types.ts:17-18.
- Open PRs (`pulls?state=open`): #95, #91, #86, #85 (draft). Intersection with the lane's directories (full `pulls/N/files`): #95 2 files, 0 hits; #91 2, 0; #86 2, 0; #85 57 files, 14 under the lane's directories but 0 of its files; control: #95's engagements.ts prints 1. #85 touches packages/renderers/test/render.test.ts, so the kit forbids editing it. Branch b985 is 2 ahead, 2 test files, not the lane's.
- Ports: block 9490-9499 free. Word-boundary scan `-w -E '949[0-9]'` over 213 non-.pre- kits dated 10-30..11-01: 0 files (controls: `971[0-9]` prints the B975 kit; `echo 9491 | grep -c -w -E '949[0-9]'` prints 1). `lsof -nP -iTCP:9490-9499 -sTCP:LISTEN` rc 1 (control: plain LISTEN list prints *:7000). Block taken (reserved, none needed; builder is --network none).
- Model: row C2 (model-routing.md:92: multi-file build, not auth-design, not a destroying path; Sonnet first). Not C3 (:93, no auth/credential/money design) and not C4 (:94, nothing dropped, no migration). Gate G1 (:108, tier 1: contract/API surface; plan tier 1). Id `claude-sonnet-5-5` (models_latest.json:23). Launch line carries BRIEF_SEAT_LEVEL=sonnet inside the quotes.
- Seat J36: 0 hits in kits (control: J35 prints B985 kit).

## D-decisions (in the kit)
D1 migration 0028, none written here. D2 drop PCOMP-42. D3 PCOMP-44 shape and nothing pre-built. D4 five code places, default "declared, not rendered, not offered" (no card, no button). D5 routing C2 + G1.

## Q-questions for Tuesday (each with default)
- Q1 PCOMP-42: keep out until (a) a words card for "after validation" / "controlled/staged", (b) a ruling on the order of four remediation states (resolve.ts:93), (c) L2 exists. Default: out.
- Q2 PCOMP-44 refusal: (a) one declared refusal sentence approved on a words card first, or (b) hold -44 until L7 delivers renderers and add the enum then. Default: (b) (no existing sentence is true). Under (a) the sentence goes in the Stamp slot and the builder uses it byte for byte.
- Q3 under (a): status and code. Default HTTP 501 `OUTPUT_KIND_NOT_AVAILABLE`.

## UNMEASURED
- Regenerate command for apps/web/src/api/schema.d.ts (not found; kit makes it a builder STOP-or-print step).
- Whether `npm run contract:write` plus prettier reproduces the committed openapi.json byte-for-byte at main (not run; fenced).
- The exact method of the sha256 pin in openapi.test.ts:523-543 (builder copies it from the neighbouring comment).
- Whether any other web file iterates OutputKind besides exports.ts (grep of OUTPUT_KIND_LIST/CARD_OUTPUTS shows exports.test.ts, storedOutputs.ts only).
- Host core count for the load rule (builder prints it). Hosted site state (not probed, fenced). No Composer pane list taken by the drafter (no tmux); the kit makes it a Step-0 read, the "no other Composer seat live" fact is the caller's.
- Local test runs: none (no vitest/docker, per fences).

## Outside-the-fences disclosure
No file written except these two. Scratch files in the session scratchpad only (a Jira reader script and PR file lists). Jira: GET only through the project's own helper, no token printed. gh: `-X GET` only, under the Composer GH_CONFIG_DIR. Git in the project repo: `--no-optional-locks` show/grep/cat-file/rev-parse only; no fetch. No az/ssh/docker; no HTTP to any hosted host. One hook refusal met and complied with (a `cd` attempt; zsh word-split); no state changed by either.
