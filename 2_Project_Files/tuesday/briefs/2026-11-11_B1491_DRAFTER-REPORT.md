STARTABLE: YES (after the Stamp; five slots carry decisions D-1 to D-5 below, each with a recommendation)

# B1491 DRAFTER REPORT: SEAT-U4, HPSM-POC user guide v0.4

Drafted 2026-11-11 from 10:53:13 to 11:03:52 AEDT (`date` at the first and last reads). Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-11_B1491_SEAT-U4_hpsmpoc-user-guide-v04.md`, 137 lines, sha256 `3c9a99e36946d6f184c87d61b4aa17a6d63504fc3eb178c4b32b3b4b760959df`; `.pre-stamp` copy beside it, `cmp` rc 0, same sha256. Four-underscore slots: 11 in the Stamp section (10 slot lines + the READ-WHOLE line), 0 above it.

## BLUF
- The kit makes SEAT-U4 (Sonnet, rows C2 line 92 / C8 line 98) rebuild the guide as DRAFT v0.4 **from scratch**, not as a patch: v0.3's screen bodies are the v0.2 build's (code `01dd9e4b`), and the site now runs `009421a2`. Between those: 127 commits; `web/src` 319 files, +30,335/-1,145; pages 46 to 56 (10 new: the customer security workspace, 8 pages; Training & playbooks; the feedback review page). The menu became a sidebar; Assessments became Playbook Partner Readiness; Service offers became Delivery phases; the start page has a Demo Walkthrough option with a 14-step guided panel. So every v0.3 figure is stale, and the kit forbids reusing any v0.3 image.
- **The old toolchain is gone from this drive.** `.tools/b427`, `b442`, `b741` and the `b186` venv are absent. **python-docx and Pillow are not installed anywhere** I could find. The seat has to rebuild the toolchain. Playwright 1.63.0, Chromium 1243, node 24.21.0, `sharp` 0.35.4 (it loads) and poppler (`pdftotext`, `pdftoppm`) are present. Without an install the PDF can be built and the DOCX cannot (D-1).
- **Capture method:** a read-only walk of the review site using the B1466 walker's fence. The only non-GETs allowed are the sign-in and sign-out POSTs. Every request to `/admin/feedback(/review)` is aborted, GET included, because those pages hold HP reviewers' entries and a person's first name. WRITE features are shown before the step as "Shown without saving on the review copy". If allowed (D-2), a labelled local run of the same release (packages sha `9d6bb36c...`/`1fd65b62...`, BUILD_ID `NQga609FQ4iKZFwQ1rtsT`) covers what the site cannot show read-only.
- **Independent check before READY:** first, program checks (no v0.4 file equals any v0.3 file; every inventory row has a figure or a reason). Second, an end-of-run re-read of every captured route's text on the site. Third, a fresh read-only sub-agent opens every figure page against its caption and steps (`VERIFY.md`); fixed items get a second sub-agent pass.
- **One fence conflict, resolved toward the rules:** your commission let me GET the review site's public pages, but DRAFTER_RULES fence 4 says "No HTTP to any hosted, demo or production host, not even GET". I made **no request to the site**. Every "live" fact in the kit is RELAYED from the B1466 deploy record (2026-11-10 22:14) and marked UNMEASURED for today.

## Facts re-measured (instrument; control)
| Fact | Value | Instrument / control |
|---|---|---|
| Code main | `009421a28616c8b31dde86b59d4c4ca674c288fa` (10:54) | `gh api -X GET repos/datasecau/HPSM-POC/branches/main` under the project GH_CONFIG_DIR |
| Code source for reading | `.tools/b1466/repo` HEAD `009421a2`; the local `2_Project_Files` is at `8869b1a9` and lacks `009421a2` | `rev-parse HEAD`; `cat-file -t 009421a2` failed in `2_Project_Files` (control: `01dd9e4b`, `0413f25c` print `commit`) |
| Pages | 46 at `01dd9e4b`, 56 at `009421a2`, 10 added (listed in the kit) | `ls-tree -r` + `diff` (rc 1 = differences) |
| Commits / web delta | 127; 319 files +30,335/-1,145 | `rev-list --count`; `diff --stat` |
| Sidebar per level | Partner 9, Consultant 10, Admin 12, Demo 10 (derived from `GlobalNav.tsx:39-57`) | lines printed with `awk NR`; equals B1466 STATUS line 187 (RELAYED) |
| Walkthrough | 14 step ids; step 6 cue holds "View only: do not save an answer" once (`steps.ts:93`) | `git show` + `grep -c` (14, 1) |
| Security workspace | 7 built views + Framework alignment held (`customer-nav.ts:17-26`); "Not connected" at `FleetDevices.tsx:25`, `SecurityAssurance.tsx:14` | `git grep -n` |
| v0.3 files | DOCX `0a89d351..`, PDF `c09f7296..`, e-mail `20abc76f..`, SOURCES `d6f5e951..`, CHANGES `d9a7eaef..` = B741 STATUS 101-104; 180 files; v0.2 folder 245 | `shasum -a 256`; `find -type f | wc -l` |
| v0.3 shape | 42 pages, Title `HP Security Services Playbook: user guide to the review copy`; contents page printed | `pdfinfo`, `pdftotext -f 2 -l 2` |
| TARGET packages | web.zip `9d6bb36c...19f`, api.zip `1fd65b62...9ec`, `unz/t/web/.next/BUILD_ID` `NQga609FQ4iKZFwQ1rtsT` | `shasum`; `cat` (equal to B1466 STATUS lines 74, 76) |
| Tools present | Playwright 1.63.0 (package.json), `ms-playwright/chromium-1243`, node v24.21.0, sharp 0.35.4 (loads, vips 8.18.6), `pdftotext`/`pdftoppm`/`pdfinfo` in /opt/homebrew/bin | `require` test printed `pw ok function` / `sharp ok` |
| Tools absent | python-docx and Pillow (`.tools/venv`, system python3); `.tools/b427/b442/b741`, `b186/venv`; Word/LibreOffice (`ls /Applications` count 0, `which soffice` rc 1) | `ls -d` each "No such file"; `import` errors; `find /Volumes/Datasec_DEV -maxdepth 9` for `site-packages/docx`: nothing. **This zero has no control that fires.** A positive control would be a known docx install, and none exists to plant. |
| Ports 9530-9539 | free | `lsof` rc 1; control: a python listener on 9533 listed 1 line, then rc 1 after close. Kit scan of the 60 non-`.pre-` SEAT kits of 10-11 Nov for `953[0-9]`: 0 kits (control `997[0-9]`: 5 kits) |
| Panes (10:56) | wednesday, Datasec/HPSM-POC-D60 (B1490, copy-DB delete, no site write), Datasec/NexusAI-N122, fleet-monitor, two unnamed | `tmux list-panes -a` |
| Load | 1.84 at 10:59; hw.ncpu 18 (launch gate 24) | `uptime`, `sysctl` |
| Model | `claude-sonnet-5-5`, models_latest.json line 23; routing C2 line 92, C8 line 98 | `grep -n` |
| Names in kit | 0 hits of the 9-name ban list (`.tools/b1462/scan1462.py` line 10), underscore-aware | control `x_by_<name>_y` = 1 |
| Deliverables tracking | `?? 1_Project_Definition/Deliverables/`; `.gitignore:12` *.docx, `:16` *.pdf | `status --short`, `check-ignore -v` |

## Decisions for Tuesday (each a Stamp slot)
- **D-1 DOCX: `VENV` or `PDF-ONLY`. Recommend `VENV`.** The commission asks for a DOCX if the earlier guides had one, and all three did. The only way to build one is a seat-local `python3 -m venv` plus `pip install --only-binary :all: python-docx` (wheels only, each wheel's sha256 recorded), confined to `.tools/b1491/venv`. The product owner asked only for the PDF, so `PDF-ONLY` costs him nothing today and avoids a new download. Choose it if you would rather not have a seat pull from PyPI. UNMEASURED: whether PyPI is reachable from this machine.
- **D-2 LOCAL: `YES` or `NO`. Recommend `YES`.** A labelled local run of the identical packages is the only honest way to show a WRITE result or the Admin feedback pages. Every such caption carries the words "Local copy of the same release with sample data, not the review site." With `NO`, those items are described in words only.
- **D-3 REVIEW-PAGE: `DESCRIBE` or `LOCAL-MASKED`. Recommend `DESCRIBE`.** The approval page's title constant holds a person's first name (B1466 STATUS line 206), and its lead names Datasec's Jira board. Masking the title of a page whose title is its subject reads badly. A paragraph is enough.
- **D-4 EMAIL-SPLIT: `SPLIT` or `STOP`. Recommend `SPLIT`.** v0.3 fitted 56 figures into 4.0 MB at JPEG 82 / scale 0.70. v0.4 will have more figures (my guess is 70 to 100, UNMEASURED), so one file under 4,100,000 bytes may not stay legible. With `SPLIT`, two parts split at a Heading 1 break, each under the cap, are mailed as two messages. With `STOP`, the seat waits for you.
- **D-5 Clocks.** Suggested: target READY 5 h after Step 0, HARD STOP 7 h. This is a full re-shoot, a toolchain rebuild, about 15 sections of new prose and a verifier pass. v0.3, a narrow change, took about 55 min. A `PARTIAL:` last line exists for the hard stop.
- **D-6 (no slot; written into the kit).** `/design-system` is listed in the inventory and not covered in the guide (it is an internal page). Help and Settings are named in Known limits as "Not in this build yet", as v0.1 did.

## Questions for Tuesday (each with a default)
- **Q-1** Is a read-only sign-in walk on the review site still acceptable while HP reviews it? C-300's hold covers deploys, and the walk adds last-seen bookkeeping on the shared level users. **Default: yes.** The B427 and B442 guide walks and the B1460/B1466 deploy walks all did it, and the product owner looked at the site himself today.
- **Q-2** Should the guide carry the site URL? **Default: no**, as in v0.1 to v0.3. Put the link in your covering e-mail if he wants it.
- **Q-3** Should the guide's own cover carry an HP mark? **Default: no.** As in v0.3, the logo appears only in screenshots of the site's header. Branding (HPSMPOC-21) is still unsettled per C-191.
- **Q-4** Should the Demo pipeline panel's sample names (not aliases; HPSMPOC-467 is open) be shown as the site shows them? **Default: yes, described truthfully.** The guide never says "Demo shows only aliases".
- **Q-5** Model: is Sonnet enough for a guide this size? **Default: Sonnet** (routing C2/C8; three accepted guide seats). Choose Opus if you want fewer verify rounds.

## UNMEASURED (by me)
- Everything live today. This includes the build id the site serves now: I relayed `NQga609FQ4iKZFwQ1rtsT` from B1466 STATUS line 197, and REFUSE 3 makes the seat re-read it.
- Each page's role guard. Only the sidebar's roles were read.
- The READ/WRITE class of each control.
- Whether the local TARGET API seeds a fresh database by itself. B1466 seeded with PREV first; the kit names that fallback.
- PyPI reachability.
- Page count and e-mail size.
- That the CSP-workaround control is still needed.

## Outside-the-fences disclosure
1. I read files in another seat's tree (`.tools/b1466/`), all read-only:
   - git read verbs on `.tools/b1466/repo`;
   - `shasum` of its `target/` zips;
   - headers of `walk1466.cjs`, `webpair1466.py`, `pairseed1466.py`;
   - `ls` of `local/`, `unz/`, `shots-local/`.

   Fence 1 does not forbid this; I name it anyway.
2. I loaded the `sharp` and `playwright` modules from `2_Project_Files/web/node_modules` in node, to test that they load (no file was written).
3. **My slip:** I listed `/Volumes/Backup` at the top level, which is a personal backup volume and not Datasec's. I read only directory names, opened nothing, and did not repeat the names anywhere. I also listed `/Volumes/DEV-Working/Datasec/Tuesday` while looking for the old toolchains.
4. I started a 4-second loopback listener on 127.0.0.1:9533 as the port control. It exited on its own and the port read free afterwards.
5. I read records main's `CLARIFICATIONS.md` from GitHub (`gh api -X GET`, piped to grep; nothing saved).
6. No hosted HTTP of any kind, no Jira, no az, no mail, no decision-queue use. I wrote nothing besides the kit, its `.pre-stamp` copy and this report.
