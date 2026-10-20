# B337 DRAFTER REPORT (2026-10-20 ~19:05 AEDT)

Brief: `/Volumes/Laptop-DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-10-20_B337_SEAT-D5_hpsmpoc-sm-24h-and-paul-admin.md`. Seat SEAT-D5, pane `Datasec/HPSM-POC-D5`, Opus 5.5, no stamp slot (nothing for Tuesday to fill), last line `READ-WHOLE-BY-TUESDAY: PENDING`. I ran no az, sent nothing to the VM, wrote only these two files.

## Sources read
B306 final brief (whole), B306 ADDENDUM-1, B306_STATUS (whole), B329 brief lines 24-97, B329_STATUS (whole), B329 ANSWER-1, grep of B106/B108/B161 STATUS, the grant learning, grep of HPSM-POC CLAUDE.md and CLARIFICATIONS.md. Not opened: the superseded B306 allowlist brief (only its line-12 identity text via grep), anything under the HP-hold paths.

## Facts measured (file:line)
- RG `hpsm-poc-sm-rg`, VM `vm-hpsm-sm` Standard_D4as_v5, `pip-hpsm-sm` 52.187.238.167, `nsg-hpsm-sm`, `bas-hpsm-sm`: `B306_STATUS.md:23`; re-confirmed running at 14:12: `B329_STATUS.md:21`. Both names VERIFIED from records; the brief tells the seat to re-verify by az.
- Identity: kamil@datasec-rd.com, tenant ec01829b-..., sub a6b8fe11-... "Azure subscription 1": `B306_STATUS.md:20`, `B329_STATUS.md:55-58`.
- Auto-shutdown `shutdown-computevm-vm-hpsm-sm`: Enabled, 2000, AUS Eastern Standard Time, a DevTest schedule set via `az rest`: `B306_STATUS.md:27`; `B106_STATUS.md:37,132`.
- Budget `budget-hpsm-poc-sm` A$250 monthly, notify-only emails at 50/80/100% actual and 100% forecast: `B106_STATUS.md:38`. "At 24x7 the VM alone exceeds the A$250 budget": `B106_STATUS.md:53`.
- Prices (A$, retail, 2026-10-03): VM A$0.5698/h, 24x7 about A$415.95, 220 h plan about A$125.36, P10 disk A$28.08, PIP A$5.18: `B106_STATUS.md:183-186`. So the delta vs the 20:00 plan is roughly A$290/month (my arithmetic from those lines; the seat re-measures and labels it an estimate).
- SM 3.16 roles are local Windows groups: HPIPSC = Administrator, HPIPSC_Analyst = "all features, with limited operations", HPIPSC_Operator = "no policy or system changes", HPIPSC_Guest = view only: `B106_STATUS.md:60-63`.
- Paul = local user `paul.waite`, member of HPIPSC_Analyst only: `B306_STATUS.md:52`; B106 sign-in role "Analyst": `B106_STATUS.md:126`. Kam's kam.kreiser = HPIPSC Administrator: `B106_STATUS.md:126`, `B161_STATUS.md:107`. hpsmadmin signs in as Administrator: `B329_STATUS.md:69`.
- Lockout 10 failures / 10 min / 10 min (B106 said 5/30; VM reads 10/10): `B306_STATUS.md:53`.
- SM state at 14:33: 8 devices, 5 tasks, 1 scheduled report, 0 policies, Instant-On off, licences assigned 0 of 10: `B329_STATUS.md:46,63-68`. Idle sign-out 20 min: `B329_STATUS.md:70`.
- B329 collision: its step 8 asserts exactly its own two ZZ-DATASEC rows were added (`B329 brief:58`); run-commands must not interleave (B108 FOUND 9, cited at `B329 brief:51`); it uses managed run-command `b106-probe` updated in place (`B329_STATUS.md:122`); VM-local DevTools port 9339 (`B329_STATUS.md` kit, `t02_bodytest`). B329 has been resumed under ANSWER-1 and its evidence folder already holds `step8-assert.txt`, so it is near its end. `pgrep -fl b329` on this laptop printed nothing at 18:58 (no local process; its VM work runs inside the VM, so this proves little).
- The 20:00 shutdown is 55 minutes after Kam's message (18:55): the brief puts Step 1 first and says to launch before 19:30.

## Judgement calls (so you can overrule)
1. Disable, not delete, the schedule (exact prior config recorded, one-flip undo). Kam said "remove".
2. Root cause is stated as a hypothesis (Analyst "limited operations" excludes policy create), to be measured, not assumed. Fix = add `paul.waite` to `HPIPSC`; if SM still reports Analyst, remove him from `HPIPSC_Analyst`. Never local Administrators.
3. Paul's test sign-in and the test-policy create WAIT for B329 to finish (a third ZZ-DATASEC row would break B329's step 8 assertion). The schedule change and the group change do not wait.
4. New managed run-command `b337-probe` instead of reusing B329's `b106-probe`. VM-local DevTools port 9361 (not 9339; no laptop ports).
5. Budget left alone; Windows Update auto-reboot reported, not changed.

## Open questions for Tuesday (recommended answer)
1. Disable or delete the schedule? **Disable** (reversible; same effect).
2. Launch now ahead of B329 finishing? **Yes, immediately**: Step 1 is Azure-side and must beat 20:00; the seat is told to wait on B329 for any SM sign-in or create.
3. Will a second sign-in as Paul end Paul's live session? UNMEASURED. **Proceed** (the role change needs his re-login anyway), but the seat stops if SM warns. Tell Kam to ask Paul to sign out and in again.
4. Budget: 24x7 (about A$416 VM alone, about A$450 all-in) will cross the A$250 budget's 80/100% alerts and email Kam. **Leave the budget; tell Kam the figure** (he authorised cost by instruction). Raising the budget is a separate ask.
5. Tell B329's seat (ANSWER-2) that a B337 policy `ZZ-DATASEC-SYNTHETIC-B337` may appear after it finishes? **Not needed** if the wait rule holds; add only if B329 is still running at 19:30.
6. Check the VM power state yourself at 20:05 (the seat cannot test the 20:00 pass).

## Not verified by me
Whether the VM is running now; whether the schedule is still the only down rule (a budget action, runbook or in-guest task would be found by the seat's enumeration); the exact SM role resolution when a user is in two HPIPSC groups.
